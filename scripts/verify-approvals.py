#!/usr/bin/env python3
"""
Verify ADR Approval Identity — CI Pre-Merge Gate

Ensures that every person listed in an ADR's approvals[].identity has actually
approved the pull request on the Git platform. This closes the loop between
the ADR's declared approvers and the platform's recorded approvers.

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
  0  All approvals verified (or no ADRs with identity fields in this PR)
  1  One or more required approvers did not approve the PR
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


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def get_changed_yaml_files() -> list[str]:
    """Return ADR YAML files changed in the current PR (via git diff)."""
    # Try GitHub Actions merge base first
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        base = f"origin/{base_ref}"
    else:
        # Fallback: diff against main/master
        base = "origin/main"

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", base, "HEAD"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError:
        # If origin/main doesn't exist (e.g., fresh clone), diff against HEAD~1
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

    # Build map of latest review per user (a user can review multiple times)
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

    # vote == 10 means approved
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
    changed_files: list[str],
    dry_run: bool = False,
) -> int:
    """
    Verify that all ADR approval identities match actual PR approvers.

    Returns:
      0 if all OK (or no identity fields found)
      1 if mismatches found
    """
    if not changed_files:
        print("ℹ️  No ADR files changed in this PR — skipping approval verification.")
        return 0

    all_required: list[tuple[str, dict]] = []  # (filepath, identity_entry) pairs
    files_without_identity = []

    for filepath in changed_files:
        if not Path(filepath).exists():
            continue

        identities = extract_approval_identities(filepath)
        adr_id = filepath.split("/")[-1].replace(".yaml", "")

        if not identities:
            # Check if the ADR has approvals but without identity
            try:
                with open(filepath) as f:
                    data = yaml.safe_load(f)
                status = data.get("adr", {}).get("status", "")
                approvals = data.get("approvals", [])
                if status in ("proposed", "accepted") and approvals:
                    has_any_identity = any(
                        a.get("identity") for a in approvals if isinstance(a, dict)
                    )
                    if not has_any_identity:
                        files_without_identity.append(adr_id)
            except Exception:
                pass
            continue

        for entry in identities:
            all_required.append((adr_id, entry))

    # Report warnings for ADRs with approvals but no identity fields
    for adr_id in files_without_identity:
        print(
            f"⚠️  WARNING: {adr_id} has approvals but no identity fields — "
            f"CI cannot verify approvers. Add approvals[].identity for enforcement."
        )

    if not all_required:
        if files_without_identity:
            print(
                f"\nℹ️  {len(files_without_identity)} ADR(s) have approvals without identity fields. "
                f"Add identity fields to enable CI approval verification."
            )
        else:
            print("ℹ️  No ADR approval identities to verify in this PR.")
        return 0

    if dry_run:
        print(f"\n🔍 DRY RUN — Found {len(all_required)} approval identities to verify:\n")
        for adr_id, entry in all_required:
            print(f"  {adr_id}: {entry['name']} ({entry['role']}) → identity: @{entry['identity']}")
        print("\n✅ Dry run complete. No API calls made.")
        return 0

    if pr_approvers is None:
        print(
            "⚠️  WARNING: Could not retrieve PR approvers from platform API. "
            "Skipping approval identity verification.",
            file=sys.stderr,
        )
        return 0

    # Verify each required identity
    errors = []
    verified = []

    for adr_id, entry in all_required:
        identity = entry["identity"]
        if identity in pr_approvers:
            verified.append((adr_id, entry))
        else:
            errors.append((adr_id, entry))

    # Report results
    if verified:
        print(f"✅ Verified {len(verified)} approval identit{'y' if len(verified) == 1 else 'ies'}:\n")
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
        return 1

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Verify ADR approval identities match PR approvers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse ADRs and report required identities without calling platform APIs.",
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

    # Detect platform
    platform = args.platform or detect_platform()

    # Get changed files
    changed_files = get_changed_yaml_files()
    print(f"📋 ADR files changed in this PR: {len(changed_files)}")
    for f in changed_files:
        print(f"   • {f}")

    if args.dry_run:
        return verify_approvals(platform, None, changed_files, dry_run=True)

    # Get PR approvers from platform API
    pr_approvers: set[str] | None = None

    if platform == "github":
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
        repo = args.repo or os.environ.get("GITHUB_REPOSITORY", "")
        pr_number = args.pr

        if not pr_number:
            # Try to get from GITHUB_EVENT_PATH
            event_path = os.environ.get("GITHUB_EVENT_PATH", "")
            if event_path and Path(event_path).exists():
                with open(event_path) as f:
                    event = json.load(f)
                pr_number = event.get("pull_request", {}).get("number")

        if not pr_number:
            print("⚠️  No PR number detected. Set --pr or ensure GITHUB_EVENT_PATH is available.")
            return verify_approvals(platform, None, changed_files)

        if not token:
            print("⚠️  No GitHub token found. Set GH_TOKEN or GITHUB_TOKEN.")
            return verify_approvals(platform, None, changed_files)

        print(f"\n🔗 Querying GitHub API: {repo} PR #{pr_number}")
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
            print(f"\n🔗 Querying Azure DevOps API: {project} PR #{pr_number}")
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
            print(f"\n🔗 Querying GitLab API: project {project_id} MR !{mr_iid}")
            pr_approvers = gitlab_get_mr_approvers(project_id, mr_iid, token, gitlab_url)
            print(f"   MR approvers: {', '.join(f'@{a}' for a in sorted(pr_approvers)) or '(none)'}\n")
        else:
            print("⚠️  GitLab MR details not available.")

    else:
        print(f"⚠️  Platform not detected or unsupported: {platform}")

    return verify_approvals(platform, pr_approvers, changed_files)


if __name__ == "__main__":
    sys.exit(main())
