#!/usr/bin/env python3
"""
Verify ADR Approval Identity — CI Pre-Merge Gate

Ensures that every person listed in an ADR's approvals[].identity has actually
approved the pull request on the Git platform. This closes the loop between
the ADR's declared approvers and the platform's recorded approvers.

Governance rules are loaded from .adr-governance/config.yaml:
  - Single ADR per PR (with supersession exception)
  - Change classification (substantive vs. maintenance)
  - Immutable decision core after acceptance
  - Admin override (admins can make maintenance changes without re-approval)

Supported platforms (auto-detected via environment variables):
  - GitHub Actions     (GITHUB_ACTIONS)
  - Azure DevOps       (SYSTEM_TEAMFOUNDATIONCOLLECTIONURI)
  - GitLab CI          (GITLAB_CI)

Usage:
  # In CI (auto-detects platform and PR number from env vars):
  python3 scripts/verify-approvals.py

  # Manual / dry-run (skip API calls, just parse ADRs):
  python3 scripts/verify-approvals.py --dry-run

  # Explicit PR number, repo, and base branch:
  python3 scripts/verify-approvals.py --platform github --repo owner/repo --pr 42 --base-ref main

Exit codes:
  0  All checks passed (or nothing to check)
  1  One or more governance checks failed
  2  Script error (bad arguments, API failure, etc.)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Governance config
# ---------------------------------------------------------------------------

DEFAULT_SUBSTANTIVE_FIELDS = [
    "adr.status",
    "adr.title",
    "decision",
    "alternatives",
    "consequences",
    "approvals",
    "context.summary",
]

DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS = [
    "adr.id",
    "adr.title",
    "adr.y_statement",
    "adr.project",
    "adr.component",
    "adr.priority",
    "adr.decision_type",
    "adr.created_at",
    "authors",
    "decision_owner",
    "reviewers",
    "approvals",
    "context",
    "architecturally_significant_requirements",
    "alternatives",
    "decision",
    "consequences",
    "dependencies",
]


class BaseRefError(RuntimeError):
    """Raised when the verifier cannot resolve or read the target base branch."""


def load_governance_config() -> dict:
    """Load governance config from .adr-governance/config.yaml."""
    config_paths = [
        Path(".adr-governance/config.yaml"),
        Path(".adr-governance/config.yml"),
    ]

    for config_path in config_paths:
        if config_path.exists():
            with open(config_path) as f:
                data = yaml.safe_load(f) or {}
            gov = data.get("governance", {})
            return {
                "admins": {
                    a.get("identity", "").strip().lstrip("@").lower()
                    for a in gov.get("admins", [])
                    if a.get("identity")
                },
                "single_adr_per_pr": gov.get("single_adr_per_pr", False),
                "substantive_fields": gov.get(
                    "substantive_fields", DEFAULT_SUBSTANTIVE_FIELDS
                ),
                "immutable_after_acceptance_fields": gov.get(
                    "immutable_after_acceptance_fields",
                    DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
                ),
            }

    # No config file — use defaults (no admins, no single-ADR rule)
    return {
        "admins": set(),
        "single_adr_per_pr": False,
        "substantive_fields": DEFAULT_SUBSTANTIVE_FIELDS,
        "immutable_after_acceptance_fields": DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
    }


# ---------------------------------------------------------------------------
# Platform detection
# ---------------------------------------------------------------------------

def detect_platform() -> str | None:
    """Auto-detect the CI platform from environment variables."""
    if os.environ.get("GITHUB_ACTIONS"):
        return "github"
    if os.environ.get("SYSTEM_TEAMFOUNDATIONCOLLECTIONURI"):
        return "azure-devops"
    if os.environ.get("GITLAB_CI"):
        return "gitlab"
    return None


def get_pr_author() -> str | None:
    """
    Get the PR/MR author identity from CI environment variables.
    Returns lowercase identity string or None.
    """
    # GitHub Actions
    actor = os.environ.get("GITHUB_ACTOR")
    if actor:
        return actor.lower()

    # Azure DevOps
    requestor = os.environ.get("BUILD_REQUESTEDFOR")
    if requestor:
        return requestor.lower()

    # GitLab CI
    gitlab_user = os.environ.get("GITLAB_USER_LOGIN")
    if gitlab_user:
        return gitlab_user.lower()

    return None


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def normalize_base_ref(base_ref: str | None) -> str | None:
    """Normalize a branch name or ref to the git ref used for diff/show."""
    if not base_ref:
        return None

    base_ref = base_ref.strip()
    if not base_ref:
        return None

    if base_ref.startswith("refs/heads/"):
        return f"origin/{base_ref.removeprefix('refs/heads/')}"
    if base_ref.startswith("refs/remotes/"):
        return base_ref.removeprefix("refs/remotes/")
    if base_ref.startswith("origin/") or base_ref.startswith("refs/"):
        return base_ref
    return f"origin/{base_ref}"


def detect_base_ref(platform: str | None, explicit_base_ref: str | None = None) -> str | None:
    """Resolve the target/base branch from explicit input, env override, or CI env."""
    candidates = [explicit_base_ref, os.environ.get("ADR_BASE_REF")]

    if platform == "github":
        candidates.append(os.environ.get("GITHUB_BASE_REF"))
    elif platform == "azure-devops":
        candidates.extend(
            [
                os.environ.get("SYSTEM_PULLREQUEST_TARGETBRANCH"),
                os.environ.get("SYSTEM_PULLREQUEST_TARGETBRANCHNAME"),
            ]
        )
    elif platform == "gitlab":
        candidates.append(os.environ.get("CI_MERGE_REQUEST_TARGET_BRANCH_NAME"))
    else:
        candidates.extend(
            [
                os.environ.get("GITHUB_BASE_REF"),
                os.environ.get("SYSTEM_PULLREQUEST_TARGETBRANCH"),
                os.environ.get("CI_MERGE_REQUEST_TARGET_BRANCH_NAME"),
            ]
        )

    for candidate in candidates:
        normalized = normalize_base_ref(candidate)
        if normalized:
            return normalized

    return None


def ensure_base_ref_available(base_ref: str) -> None:
    """Ensure the resolved base ref exists in the local checkout."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--verify", base_ref],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise BaseRefError(
            f"Base ref '{base_ref}' is not available in the checkout. "
            "Ensure the target branch is fetched or pass --base-ref / ADR_BASE_REF explicitly."
        ) from exc


def get_changed_yaml_files(
    base_ref: str | None,
    *,
    allow_head_fallback: bool = False,
) -> list[str]:
    """Return ADR YAML files changed in the current PR (via git diff)."""
    result = None

    if base_ref:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMR", base_ref, "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            if not allow_head_fallback:
                raise BaseRefError(
                    f"Could not diff against base ref '{base_ref}'. "
                    "Ensure the target branch is fetched or pass --base-ref / ADR_BASE_REF explicitly."
                ) from exc
    elif not allow_head_fallback:
        raise BaseRefError(
            "No base ref could be resolved. Pass --base-ref, set ADR_BASE_REF, "
            "or ensure the platform target-branch environment variable is available."
        )

    try:
        if result is None:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD~1", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
    except subprocess.CalledProcessError:
        return []

    changed = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.endswith(".yaml") and (
            line.startswith("architecture-decision-log/")
            or line.startswith("examples-reference/")
        ):
            changed.append(line)
    return changed


def get_file_at_base(
    filepath: str,
    base_ref: str | None = None,
    allow_missing_base: bool = False,
) -> dict | None:
    """
    Get the YAML content of a file at the base branch (before PR changes).
    Returns parsed dict or None if file didn't exist at base.
    """
    if not base_ref:
        if allow_missing_base:
            return None
        raise BaseRefError(
            "No base ref could be resolved for base-file comparisons. "
            "Pass --base-ref, set ADR_BASE_REF, or ensure the platform target-branch environment variable is available."
        )

    try:
        result = subprocess.run(
            ["git", "show", f"{base_ref}:{filepath}"],
            capture_output=True, text=True, check=True,
        )
        return yaml.safe_load(result.stdout)
    except (subprocess.CalledProcessError, yaml.YAMLError):
        return None


# ---------------------------------------------------------------------------
# Change classification
# ---------------------------------------------------------------------------

def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """Flatten a nested dict into dot-separated keys."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_changed_keys(old_data: dict | None, new_data: dict) -> list[str]:
    """Return flattened keys whose values differ between old and new data."""
    old_flat = flatten_dict(old_data or {})
    new_flat = flatten_dict(new_data)

    all_keys = set(old_flat.keys()) | set(new_flat.keys())
    return sorted(
        key for key in all_keys
        if old_flat.get(key) != new_flat.get(key)
    )


def key_matches_prefix(key: str, prefix: str) -> bool:
    """Check whether a flattened key matches a configured prefix."""
    return key == prefix or key.startswith(prefix + ".") or key.startswith(prefix + "[")


def classify_changes(
    old_data: dict | None,
    new_data: dict,
    substantive_fields: list[str],
) -> tuple[bool, list[str]]:
    """
    Compare old and new ADR data to determine if changes are substantive.

    Returns:
        (is_substantive, changed_field_prefixes)
        - is_substantive: True if any changed field matches a substantive prefix
        - changed_field_prefixes: list of top-level field paths that changed
    """
    if old_data is None:
        # New file — always substantive
        return True, ["(new file)"]

    changed_keys = get_changed_keys(old_data, new_data)

    if not changed_keys:
        return False, []

    # Check if any changed key matches a substantive field prefix
    is_substantive = False
    changed_prefixes = set()

    for key in changed_keys:
        for prefix in substantive_fields:
            if key_matches_prefix(key, prefix):
                is_substantive = True
                changed_prefixes.add(prefix)
                break
        else:
            # Find the top-level prefix for reporting
            parts = key.split(".")
            changed_prefixes.add(parts[0] if len(parts) == 1 else f"{parts[0]}.{parts[1]}")

    return is_substantive, sorted(changed_prefixes)


def check_immutable_after_acceptance(
    old_data: dict | None,
    new_data: dict,
    immutable_fields: list[str],
) -> tuple[bool, str]:
    """
    Prevent in-place edits to the decision core of already accepted ADRs.

    Accepted ADRs may remain accepted, or transition to superseded/deprecated,
    but their decision core must not be edited in place.
    """
    if old_data is None:
        return True, ""

    old_status = old_data.get("adr", {}).get("status", "")
    if old_status != "accepted":
        return True, ""

    new_status = new_data.get("adr", {}).get("status", "")
    allowed_statuses = {"accepted", "superseded", "deprecated"}
    if new_status not in allowed_statuses:
        return (
            False,
            "accepted ADRs may only remain 'accepted' or transition to "
            f"'superseded'/'deprecated', not '{new_status or '(missing)'}'",
        )

    changed_keys = get_changed_keys(old_data, new_data)
    violations = sorted({
        key
        for key in changed_keys
        if key != "adr.status"
        and any(key_matches_prefix(key, prefix) for prefix in immutable_fields)
    })

    if not violations:
        return True, ""

    shown = ", ".join(violations[:6])
    suffix = " ..." if len(violations) > 6 else ""
    return (
        False,
        "accepted ADR decision core is immutable; create a superseding ADR "
        f"instead of changing: {shown}{suffix}",
    )


def check_append_only_audit_trail(
    old_data: dict | None,
    new_data: dict,
) -> tuple[bool, str]:
    """
    Enforce append-only audit trail semantics for existing ADRs.

    Allowed:
      - no audit trail change
      - new_data.audit_trail extends old_data.audit_trail by appending entries

    Forbidden:
      - editing any existing audit trail entry
      - deleting entries
      - reordering entries
    """
    if old_data is None:
        return True, ""

    old_audit = old_data.get("audit_trail", [])
    new_audit = new_data.get("audit_trail", [])

    if old_audit is None:
        old_audit = []
    if new_audit is None:
        new_audit = []

    if not isinstance(old_audit, list) or not isinstance(new_audit, list):
        return False, "audit_trail must be a list in both the base and updated ADR"

    if len(new_audit) < len(old_audit):
        return (
            False,
            "audit_trail is append-only: existing entries may not be deleted",
        )

    if new_audit[:len(old_audit)] != old_audit:
        return (
            False,
            "audit_trail is append-only: existing entries may not be edited or reordered",
        )

    return True, ""


# ---------------------------------------------------------------------------
# Single ADR per PR
# ---------------------------------------------------------------------------

def check_single_adr_per_pr(
    changed_files: list[str],
    base_ref: str | None = None,
    *,
    allow_missing_base: bool = False,
) -> tuple[bool, str]:
    """
    Validate that at most one ADR is modified per PR.

    Exception: supersession pairs — if exactly two ADRs are changed and they
    form a valid supersession chain (new ADR supersedes old, old ADR is
    superseded by new), the check passes.

    Returns:
        (passed, message)
    """
    if len(changed_files) <= 1:
        return True, ""

    if len(changed_files) == 2:
        # Check for supersession pair
        try:
            changed_adrs = []
            for filepath in changed_files:
                with open(filepath) as f:
                    current_data = yaml.safe_load(f)
                if not isinstance(current_data, dict):
                    raise ValueError(f"{filepath} did not contain an ADR object")
                changed_adrs.append(
                    {
                        "filepath": filepath,
                        "current": current_data,
                        "base": get_file_at_base(
                            filepath,
                            base_ref,
                            allow_missing_base=allow_missing_base,
                        ),
                    }
                )

            existing = [entry for entry in changed_adrs if entry["base"] is not None]
            new = [entry for entry in changed_adrs if entry["base"] is None]

            if len(existing) == 1 and len(new) == 1:
                existing_entry = existing[0]
                new_entry = new[0]

                existing_current = existing_entry["current"]
                new_current = new_entry["current"]

                existing_id = existing_current.get("adr", {}).get("id", "")
                new_id = new_current.get("adr", {}).get("id", "")

                existing_lifecycle = existing_current.get("lifecycle", {})
                new_lifecycle = new_current.get("lifecycle", {})
                existing_status = existing_current.get("adr", {}).get("status", "")

                if (
                    new_lifecycle.get("supersedes") == existing_id
                    and existing_lifecycle.get("superseded_by") == new_id
                    and existing_status == "superseded"
                ):
                    return (
                        True,
                        f"Supersession pair detected: new {new_id} supersedes existing {existing_id}",
                    )

        except BaseRefError:
            raise
        except Exception:
            pass

    file_names = [f.split("/")[-1].replace(".yaml", "") for f in changed_files]
    return (
        False,
        f"This PR modifies {len(changed_files)} ADR files: {', '.join(file_names)}. "
        f"Governance rule 'single_adr_per_pr' requires at most one ADR per PR "
        f"(exception: supersession pairs).",
    )


# ---------------------------------------------------------------------------
# ADR parsing
# ---------------------------------------------------------------------------

def extract_approval_identities(filepath: str) -> list[dict]:
    """
    Parse an ADR YAML file and return approval entries that have an identity.

    Returns list of dicts: [{"name": ..., "identity": ..., "role": ...}, ...]
    Only includes entries where identity is a non-empty string.
    """
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        return []

    # Only check ADRs in proposed/accepted status
    status = data.get("adr", {}).get("status", "")
    if status not in ("proposed", "accepted"):
        return []

    approvals = data.get("approvals", [])
    if not approvals:
        return []

    result = []
    for entry in approvals:
        identity = entry.get("identity", "")
        if identity and isinstance(identity, str) and identity.strip():
            result.append({
                "name": entry.get("name", ""),
                "identity": identity.strip().lstrip("@").lower(),
                "role": entry.get("role", ""),
            })
    return result


# ---------------------------------------------------------------------------
# Platform API: GitHub
# ---------------------------------------------------------------------------

def github_get_pr_approvers(repo: str, pr_number: int, token: str) -> set[str]:
    """
    Query GitHub API for users who approved the given PR.
    Returns a set of lowercase GitHub usernames.
    """
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            reviews = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR: GitHub API returned {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(2)

    latest_by_user: dict[str, str] = {}
    for review in reviews:
        user = review.get("user", {}).get("login", "").lower()
        state = review.get("state", "")
        if user:
            latest_by_user[user] = state

    return {user for user, state in latest_by_user.items() if state == "APPROVED"}


# ---------------------------------------------------------------------------
# Platform API: Azure DevOps
# ---------------------------------------------------------------------------

def azdo_get_pr_approvers(org_url: str, project: str, repo_id: str,
                          pr_number: int, token: str) -> set[str]:
    """
    Query Azure DevOps API for users who approved the given PR.
    Returns a set of lowercase email addresses / UPNs.
    """
    url = (
        f"{org_url.rstrip('/')}/{project}/_apis/git/repositories/{repo_id}"
        f"/pullRequests/{pr_number}/reviewers?api-version=7.1"
    )
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR: Azure DevOps API returned {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(2)

    approvers = set()
    for reviewer in data.get("value", []):
        if reviewer.get("vote", 0) == 10:
            unique_name = reviewer.get("uniqueName", "").lower()
            if unique_name:
                approvers.add(unique_name)
    return approvers


# ---------------------------------------------------------------------------
# Platform API: GitLab
# ---------------------------------------------------------------------------

def gitlab_get_mr_approvers(project_id: str, mr_iid: str,
                            token: str, gitlab_url: str) -> set[str]:
    """
    Query GitLab API for users who approved the given MR.
    Returns a set of lowercase GitLab usernames.
    """
    url = (
        f"{gitlab_url.rstrip('/')}/api/v4/projects/{project_id}"
        f"/merge_requests/{mr_iid}/approval_state"
    )
    headers = {
        "PRIVATE-TOKEN": token,
        "Accept": "application/json",
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR: GitLab API returned {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(2)

    approvers = set()
    for rule in data.get("rules", []):
        for user in rule.get("approved_by", []):
            username = user.get("username", "").lower()
            if username:
                approvers.add(username)
    return approvers


# ---------------------------------------------------------------------------
# Main verification logic
# ---------------------------------------------------------------------------

def verify_approvals(
    platform: str | None,
    pr_approvers: set[str] | None,
    pr_author: str | None,
    changed_files: list[str],
    config: dict,
    base_ref: str | None = None,
    allow_missing_base: bool = False,
    dry_run: bool = False,
) -> int:
    """
    Verify governance rules for ADR changes in this PR.

    Checks performed:
      1. Single ADR per PR (if enabled)
      2. Append-only audit trail enforcement
      3. Immutable decision core enforcement for accepted ADRs
      4. Change classification (substantive vs. maintenance)
      5. Admin override (maintenance by admin → skip identity check)
      6. Approval identity verification (substantive changes → full check)

    Returns:
      0 if all OK
      1 if governance violations found
    """
    exit_code = 0

    if not changed_files:
        print("ℹ️  No ADR files changed in this PR — skipping governance checks.")
        return 0

    admins = config.get("admins", set())
    substantive_fields = config.get("substantive_fields", DEFAULT_SUBSTANTIVE_FIELDS)
    immutable_after_acceptance_fields = config.get(
        "immutable_after_acceptance_fields",
        DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
    )

    try:
        # ── Check 1: Single ADR per PR ──────────────────────────────────────
        if config.get("single_adr_per_pr"):
            passed, message = check_single_adr_per_pr(
                changed_files,
                base_ref,
                allow_missing_base=allow_missing_base,
            )
            if passed:
                if message:
                    print(f"✅ Single ADR per PR: {message}")
                else:
                    print("✅ Single ADR per PR: OK")
            else:
                print(f"\n❌ GOVERNANCE VIOLATION: {message}")
                exit_code = 1

        # ── Check 2-6: Per-file analysis ────────────────────────────────────
        all_required: list[tuple[str, dict]] = []      # substantive changes needing approval
        maintenance_files: list[tuple[str, list]] = []  # maintenance-only changes
        audit_trail_violations: list[str] = []
        immutable_after_acceptance_violations: list[str] = []
        invalid_approval_metadata: list[str] = []
        skipped_files: list[str] = []

        is_admin = pr_author is not None and pr_author in admins

        for filepath in changed_files:
            if not Path(filepath).exists():
                continue

            adr_id = filepath.split("/")[-1].replace(".yaml", "")

            # Load current file
            with open(filepath) as f:
                new_data = yaml.safe_load(f)
            if not isinstance(new_data, dict):
                continue

            old_data = get_file_at_base(
                filepath,
                base_ref,
                allow_missing_base=allow_missing_base,
            )
            audit_ok, audit_message = check_append_only_audit_trail(old_data, new_data)
            if not audit_ok:
                audit_trail_violations.append(f"{adr_id}: {audit_message}")
                exit_code = 1

            immutable_ok, immutable_message = check_immutable_after_acceptance(
                old_data, new_data, immutable_after_acceptance_fields
            )
            if not immutable_ok:
                immutable_after_acceptance_violations.append(f"{adr_id}: {immutable_message}")
                exit_code = 1

            if not audit_ok or not immutable_ok:
                continue

            status = new_data.get("adr", {}).get("status", "")

            # Skip non-actionable statuses
            if status not in ("proposed", "accepted"):
                skipped_files.append(f"{adr_id} (status: {status})")
                continue

            approvals = new_data.get("approvals", [])
            if not approvals:
                invalid_approval_metadata.append(
                    f"{adr_id}: status '{status}' requires approvals[] with at least one entry"
                )
                exit_code = 1
                continue

            missing_identity = [
                str(i + 1)
                for i, entry in enumerate(approvals)
                if not isinstance(entry, dict) or not str(entry.get("identity", "")).strip()
            ]
            if missing_identity:
                invalid_approval_metadata.append(
                    f"{adr_id}: approval entry/entries {', '.join(missing_identity)} "
                    f"missing required identity for status '{status}'"
                )
                exit_code = 1
                continue

            # Classify changes
            is_substantive, changed_prefixes = classify_changes(
                old_data, new_data, substantive_fields
            )

            if not is_substantive and old_data is not None:
                # Maintenance-only change
                maintenance_files.append((adr_id, changed_prefixes))

                if is_admin:
                    print(
                        f"🔧 {adr_id}: Maintenance change by admin @{pr_author} — "
                        f"approval identity check skipped"
                    )
                    if changed_prefixes:
                        print(f"   Changed: {', '.join(changed_prefixes)}")
                    continue
                else:
                    print(
                        f"🔧 {adr_id}: Maintenance change detected — "
                        f"approval identity check skipped"
                    )
                    if changed_prefixes:
                        print(f"   Changed: {', '.join(changed_prefixes)}")
                    continue

            # Substantive change — need identity verification
            identities = extract_approval_identities(filepath)

            if not identities:
                continue

            print(
                f"📝 {adr_id}: Substantive change detected — "
                f"approval identity verification required"
            )
            if changed_prefixes:
                print(f"   Changed fields: {', '.join(changed_prefixes)}")

            for entry in identities:
                all_required.append((adr_id, entry))

        # Report skipped files
        if skipped_files:
            for s in skipped_files:
                print(f"⏭️  {s} — skipped (non-actionable status)")

        for message in audit_trail_violations:
            print(f"❌ GOVERNANCE VIOLATION: {message}")

        for message in immutable_after_acceptance_violations:
            print(f"❌ GOVERNANCE VIOLATION: {message}")

        for message in invalid_approval_metadata:
            print(f"❌ GOVERNANCE VIOLATION: {message}")

        if not all_required:
            if (
                not maintenance_files
                and not invalid_approval_metadata
                and not audit_trail_violations
                and not immutable_after_acceptance_violations
            ):
                print("ℹ️  No ADR approval identities to verify in this PR.")
            return exit_code
    except BaseRefError as exc:
        print(f"❌ FAILED — {exc}", file=sys.stderr)
        return 2

    if dry_run:
        print(f"\n🔍 DRY RUN — Found {len(all_required)} approval identities to verify:\n")
        for adr_id, entry in all_required:
            print(f"  {adr_id}: {entry['name']} ({entry['role']}) → identity: @{entry['identity']}")
        print("\n✅ Dry run complete. No API calls made.")
        return exit_code

    if pr_approvers is None:
        platform_label = {
            "github": "GitHub",
            "azure-devops": "Azure DevOps",
            "gitlab": "GitLab",
        }.get(platform, "the configured platform")
        print(
            "❌ FAILED — approval identity verification was required, but "
            f"PR/MR approver data could not be retrieved from {platform_label}. "
            "Use --dry-run for advisory mode, or fix the CI/PR metadata wiring.",
            file=sys.stderr,
        )
        exit_code = 1
        return exit_code

    # ── Verify identities ───────────────────────────────────────────────
    errors = []
    verified = []

    for adr_id, entry in all_required:
        identity = entry["identity"]
        if identity in pr_approvers:
            verified.append((adr_id, entry))
        else:
            errors.append((adr_id, entry))

    if verified:
        print(f"\n✅ Verified {len(verified)} approval identit{'y' if len(verified) == 1 else 'ies'}:\n")
        for adr_id, entry in verified:
            print(f"  ✅ {adr_id}: {entry['name']} (@{entry['identity']}) — PR approval confirmed")

    if errors:
        print(f"\n❌ FAILED — {len(errors)} required approver(s) have NOT approved the PR:\n")
        for adr_id, entry in errors:
            print(
                f"  ❌ {adr_id}: {entry['name']} (@{entry['identity']}, {entry['role']}) "
                f"— NOT FOUND in PR approvers"
            )
        print(f"\n   PR approvers found: {', '.join(f'@{a}' for a in sorted(pr_approvers)) or '(none)'}")
        print(
            "\n   To fix: ensure the listed approvers review and approve the PR, "
            "or update approvals[].identity to match their platform handle."
        )
        exit_code = 1

    return exit_code


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Verify ADR governance rules: approval identities, single-ADR-per-PR, and change classification.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse ADRs and report findings without calling platform APIs.",
    )
    parser.add_argument(
        "--platform",
        choices=["github", "azure-devops", "gitlab"],
        help="Override platform detection.",
    )
    parser.add_argument(
        "--repo",
        help="Repository (e.g., owner/repo for GitHub). Auto-detected in CI.",
    )
    parser.add_argument(
        "--pr",
        type=int,
        help="Pull request number. Auto-detected in CI.",
    )
    parser.add_argument(
        "--base-ref",
        help="Target/base branch name or git ref (for example: main or origin/main). Auto-detected in supported CI platforms.",
    )
    args = parser.parse_args()

    # Load governance config
    config = load_governance_config()
    if config["admins"]:
        print(f"⚙️  Governance config loaded — {len(config['admins'])} admin(s), "
              f"single_adr_per_pr={'yes' if config.get('single_adr_per_pr') else 'no'}")
    else:
        print("⚙️  No governance config found — using defaults")

    # Detect platform
    platform = args.platform or detect_platform()

    base_ref = detect_base_ref(platform, args.base_ref)
    if base_ref:
        print(f"🔀 Base ref: {base_ref}")
        try:
            ensure_base_ref_available(base_ref)
        except BaseRefError as exc:
            if not args.dry_run:
                print(f"❌ FAILED — {exc}", file=sys.stderr)
                return 2
            print(f"⚠️  {exc} Dry-run will fall back to HEAD~1.", file=sys.stderr)
            base_ref = None
    elif not args.dry_run:
        print(
            "❌ FAILED — No base ref could be resolved. Pass --base-ref, set ADR_BASE_REF, "
            "or ensure the platform target-branch environment variable is available.",
            file=sys.stderr,
        )
        return 2
    else:
        print(
            "⚠️  No base ref could be resolved. Dry-run will fall back to HEAD~1 and treat base comparisons as best-effort.",
            file=sys.stderr,
        )

    # Get PR author
    pr_author = get_pr_author()
    if pr_author and pr_author in config["admins"]:
        print(f"👤 PR author: @{pr_author} (ADR admin)")
    elif pr_author:
        print(f"👤 PR author: @{pr_author}")

    # Get changed files
    try:
        changed_files = get_changed_yaml_files(
            base_ref,
            allow_head_fallback=args.dry_run,
        )
    except BaseRefError as exc:
        print(f"❌ FAILED — {exc}", file=sys.stderr)
        return 2
    print(f"📋 ADR files changed in this PR: {len(changed_files)}")
    for f in changed_files:
        print(f"   • {f}")
    print()

    if args.dry_run:
        return verify_approvals(
            platform,
            None,
            pr_author,
            changed_files,
            config,
            base_ref=base_ref,
            allow_missing_base=True,
            dry_run=True,
        )

    # Get PR approvers from platform API
    pr_approvers: set[str] | None = None

    if platform == "github":
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
        repo = args.repo or os.environ.get("GITHUB_REPOSITORY", "")
        pr_number = args.pr

        if not pr_number:
            event_path = os.environ.get("GITHUB_EVENT_PATH", "")
            if event_path and Path(event_path).exists():
                with open(event_path) as f:
                    event = json.load(f)
                pr_number = event.get("pull_request", {}).get("number")

        if not pr_number:
            print("⚠️  No PR number detected. Set --pr or ensure GITHUB_EVENT_PATH is available.")
            return verify_approvals(
                platform,
                None,
                pr_author,
                changed_files,
                config,
                base_ref=base_ref,
            )

        if not token:
            print("⚠️  No GitHub token found. Set GH_TOKEN or GITHUB_TOKEN.")
            return verify_approvals(
                platform,
                None,
                pr_author,
                changed_files,
                config,
                base_ref=base_ref,
            )

        print(f"🔗 Querying GitHub API: {repo} PR #{pr_number}")
        pr_approvers = github_get_pr_approvers(repo, pr_number, token)
        print(f"   PR approvers: {', '.join(f'@{a}' for a in sorted(pr_approvers)) or '(none)'}\n")

    elif platform == "azure-devops":
        org_url = os.environ.get("SYSTEM_TEAMFOUNDATIONCOLLECTIONURI", "")
        project = os.environ.get("SYSTEM_TEAMPROJECT", "")
        repo_id = os.environ.get("BUILD_REPOSITORY_ID", "")
        pr_number = args.pr or int(os.environ.get("SYSTEM_PULLREQUEST_PULLREQUESTID", "0"))
        token = os.environ.get("SYSTEM_ACCESSTOKEN", "")

        if pr_number and token:
            import base64
            b64_token = base64.b64encode(f":{token}".encode()).decode()
            print(f"🔗 Querying Azure DevOps API: {project} PR #{pr_number}")
            pr_approvers = azdo_get_pr_approvers(org_url, project, repo_id, pr_number, b64_token)
            print(f"   PR approvers: {', '.join(sorted(pr_approvers)) or '(none)'}\n")
        else:
            print("⚠️  Azure DevOps PR details not available.")

    elif platform == "gitlab":
        project_id = os.environ.get("CI_PROJECT_ID", "")
        mr_iid = os.environ.get("CI_MERGE_REQUEST_IID", "")
        token = os.environ.get("CI_JOB_TOKEN") or os.environ.get("GITLAB_TOKEN", "")
        gitlab_url = os.environ.get("CI_SERVER_URL", "https://gitlab.com")

        if mr_iid and token:
            print(f"🔗 Querying GitLab API: project {project_id} MR !{mr_iid}")
            pr_approvers = gitlab_get_mr_approvers(project_id, mr_iid, token, gitlab_url)
            print(f"   MR approvers: {', '.join(f'@{a}' for a in sorted(pr_approvers)) or '(none)'}\n")
        else:
            print("⚠️  GitLab MR details not available.")

    else:
        print(f"⚠️  Platform not detected or unsupported: {platform}")

    return verify_approvals(
        platform,
        pr_approvers,
        pr_author,
        changed_files,
        config,
        base_ref=base_ref,
    )


if __name__ == "__main__":
    sys.exit(main())
