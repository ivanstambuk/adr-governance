#!/usr/bin/env python3
"""
Verify ADR Approval Identity — CI Pre-Merge Gate

Ensures that every person listed in an ADR's approvals[].identity has actually
approved the pull request on the Git platform. This closes the loop between
the ADR's declared approvers and the platform's recorded approvers.

Governance rules are loaded from .adr-governance/config.yaml:
  - Single ADR per PR (with supersession exception)
  - Change classification (substantive vs. maintenance)
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

  # Explicit PR number and repo (for testing):
  python3 scripts/verify-approvals.py --platform github --repo owner/repo --pr 42

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
            }

    # No config file — use defaults (no admins, no single-ADR rule)
    return {
        "admins": set(),
        "single_adr_per_pr": False,
        "substantive_fields": DEFAULT_SUBSTANTIVE_FIELDS,
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

def get_changed_yaml_files() -> list[str]:
    """Return ADR YAML files changed in the current PR (via git diff)."""
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        base = f"origin/{base_ref}"
    else:
        base = "origin/main"

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", base, "HEAD"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError:
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD~1", "HEAD"],
                capture_output=True, text=True, check=True,
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


def get_file_at_base(filepath: str) -> dict | None:
    """
    Get the YAML content of a file at the base branch (before PR changes).
    Returns parsed dict or None if file didn't exist at base.
    """
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        base = f"origin/{base_ref}"
    else:
        base = "origin/main"

    try:
        result = subprocess.run(
            ["git", "show", f"{base}:{filepath}"],
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

    old_flat = flatten_dict(old_data)
    new_flat = flatten_dict(new_data)

    all_keys = set(old_flat.keys()) | set(new_flat.keys())
    changed_keys = []

    for key in all_keys:
        old_val = old_flat.get(key)
        new_val = new_flat.get(key)
        if old_val != new_val:
            changed_keys.append(key)

    if not changed_keys:
        return False, []

    # Check if any changed key matches a substantive field prefix
    is_substantive = False
    changed_prefixes = set()

    for key in changed_keys:
        for prefix in substantive_fields:
            if key == prefix or key.startswith(prefix + ".") or key.startswith(prefix + "["):
                is_substantive = True
                changed_prefixes.add(prefix)
                break
        else:
            # Find the top-level prefix for reporting
            parts = key.split(".")
            changed_prefixes.add(parts[0] if len(parts) == 1 else f"{parts[0]}.{parts[1]}")

    return is_substantive, sorted(changed_prefixes)


# ---------------------------------------------------------------------------
# Single ADR per PR
# ---------------------------------------------------------------------------

def check_single_adr_per_pr(changed_files: list[str]) -> tuple[bool, str]:
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
            data_a = yaml.safe_load(open(changed_files[0]))
            data_b = yaml.safe_load(open(changed_files[1]))

            id_a = data_a.get("adr", {}).get("id", "")
            id_b = data_b.get("adr", {}).get("id", "")

            lifecycle_a = data_a.get("lifecycle", {})
            lifecycle_b = data_b.get("lifecycle", {})

            # Check if A supersedes B
            a_supersedes_b = (
                lifecycle_a.get("supersedes") == id_b
                and lifecycle_b.get("superseded_by") == id_a
            )
            # Check if B supersedes A
            b_supersedes_a = (
                lifecycle_b.get("supersedes") == id_a
                and lifecycle_a.get("superseded_by") == id_b
            )

            if a_supersedes_b or b_supersedes_a:
                return True, f"Supersession pair detected: {id_a} ↔ {id_b}"

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
    dry_run: bool = False,
) -> int:
    """
    Verify governance rules for ADR changes in this PR.

    Checks performed:
      1. Single ADR per PR (if enabled)
      2. Change classification (substantive vs. maintenance)
      3. Admin override (maintenance by admin → skip identity check)
      4. Approval identity verification (substantive changes → full check)

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

    # ── Check 1: Single ADR per PR ──────────────────────────────────────
    if config.get("single_adr_per_pr"):
        passed, message = check_single_adr_per_pr(changed_files)
        if passed:
            if message:
                print(f"✅ Single ADR per PR: {message}")
            else:
                print("✅ Single ADR per PR: OK")
        else:
            print(f"\n❌ GOVERNANCE VIOLATION: {message}")
            exit_code = 1

    # ── Check 2-4: Per-file analysis ────────────────────────────────────
    all_required: list[tuple[str, dict]] = []      # substantive changes needing approval
    maintenance_files: list[tuple[str, list]] = []  # maintenance-only changes
    files_without_identity: list[str] = []
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

        status = new_data.get("adr", {}).get("status", "")

        # Skip non-actionable statuses
        if status not in ("proposed", "accepted"):
            skipped_files.append(f"{adr_id} (status: {status})")
            continue

        # Classify changes
        old_data = get_file_at_base(filepath)
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
            approvals = new_data.get("approvals", [])
            if approvals:
                has_any_identity = any(
                    a.get("identity") for a in approvals if isinstance(a, dict)
                )
                if not has_any_identity:
                    files_without_identity.append(adr_id)
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

    # Report warnings for ADRs with approvals but no identity fields
    for adr_id in files_without_identity:
        print(
            f"⚠️  WARNING: {adr_id} has approvals but no identity fields — "
            f"CI cannot verify approvers. Add approvals[].identity for enforcement."
        )

    if not all_required:
        if files_without_identity:
            print(
                f"\nℹ️  {len(files_without_identity)} ADR(s) have approvals without identity fields."
            )
        elif not maintenance_files:
            print("ℹ️  No ADR approval identities to verify in this PR.")
        return exit_code

    if dry_run:
        print(f"\n🔍 DRY RUN — Found {len(all_required)} approval identities to verify:\n")
        for adr_id, entry in all_required:
            print(f"  {adr_id}: {entry['name']} ({entry['role']}) → identity: @{entry['identity']}")
        print("\n✅ Dry run complete. No API calls made.")
        return exit_code

    if pr_approvers is None:
        print(
            "⚠️  WARNING: Could not retrieve PR approvers from platform API. "
            "Skipping approval identity verification.",
            file=sys.stderr,
        )
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

    # Get PR author
    pr_author = get_pr_author()
    if pr_author and pr_author in config["admins"]:
        print(f"👤 PR author: @{pr_author} (ADR admin)")
    elif pr_author:
        print(f"👤 PR author: @{pr_author}")

    # Get changed files
    changed_files = get_changed_yaml_files()
    print(f"📋 ADR files changed in this PR: {len(changed_files)}")
    for f in changed_files:
        print(f"   • {f}")
    print()

    if args.dry_run:
        return verify_approvals(platform, None, pr_author, changed_files, config, dry_run=True)

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
            return verify_approvals(platform, None, pr_author, changed_files, config)

        if not token:
            print("⚠️  No GitHub token found. Set GH_TOKEN or GITHUB_TOKEN.")
            return verify_approvals(platform, None, pr_author, changed_files, config)

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

    return verify_approvals(platform, pr_approvers, pr_author, changed_files, config)


if __name__ == "__main__":
    sys.exit(main())
