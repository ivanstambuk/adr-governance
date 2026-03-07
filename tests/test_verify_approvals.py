from __future__ import annotations

import contextlib
import copy
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from _helpers import load_module, write_yaml


def make_accepted_adr() -> dict:
    return {
        "adr": {
            "id": "ADR-1234-accepted-example",
            "status": "accepted",
            "title": "Accepted ADR",
            "summary": "Summary",
            "project": "project-x",
            "component": "auth",
            "priority": "high",
            "decision_type": "security",
            "created_at": "2026-03-01T10:00:00Z",
        },
        "authors": [{"name": "Author", "role": "Architect"}],
        "decision_owner": {"name": "Owner", "role": "Lead", "email": "owner@example.com"},
        "reviewers": [{"name": "Reviewer", "role": "Reviewer"}],
        "approvals": [
            {
                "name": "Approver",
                "role": "Architect",
                "identity": "@approver",
                "approved_at": "2026-03-02T10:00:00Z",
            }
        ],
        "context": {"summary": "Original context"},
        "architecturally_significant_requirements": [],
        "alternatives": [{"name": "Option A"}],
        "decision": {"chosen_alternative": "Option A", "rationale": "Because"},
        "consequences": {"positive": ["good"], "negative": ["bad"]},
        "dependencies": [],
        "references": [],
        "confirmation": {"description": None, "artifact_ids": []},
        "lifecycle": {"review_cycle_months": 12},
        "audit_trail": [{"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"}],
    }


def make_proposed_adr() -> dict:
    data = make_accepted_adr()
    data["adr"]["id"] = "ADR-1234-proposed-example"
    data["adr"]["status"] = "proposed"
    return data


def make_superseded_adr(replacement_id: str = "ADR-9999-replacement") -> dict:
    data = make_accepted_adr()
    data["adr"]["status"] = "superseded"
    data["approvals"] = []
    data["lifecycle"]["superseded_by"] = replacement_id
    data["audit_trail"].append(
        {"event": "superseded", "by": "Architect", "at": "2026-03-03T10:00:00Z"}
    )
    return data


class VerifyApprovalsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module("verify_approvals", "scripts/verify-approvals.py")

    def make_config(self) -> dict:
        return {
            "admins": set(),
            "single_adr_per_pr": False,
            "substantive_fields": self.module.DEFAULT_SUBSTANTIVE_FIELDS,
            "immutable_after_acceptance_fields": self.module.DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
        }

    def write_temp_adr(self, data: dict, directory: str) -> str:
        path = Path(directory) / f"{data['adr']['id']}.yaml"
        write_yaml(path, data)
        return str(path)

    def run_main_with(
        self,
        argv: list[str],
        env: dict[str, str],
        changed_files: list[str] | None = None,
    ) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        patchers = [
            mock.patch.object(self.module, "load_governance_config", return_value=self.make_config()),
            mock.patch.object(self.module, "get_pr_author", return_value=None),
            mock.patch.dict(self.module.os.environ, env, clear=True),
            mock.patch.object(sys, "argv", argv),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ]
        if changed_files is not None:
            patchers.append(
                mock.patch.object(self.module, "get_changed_yaml_files", return_value=changed_files)
            )

        with contextlib.ExitStack() as stack:
            for patcher in patchers:
                stack.enter_context(patcher)
            exit_code = self.module.main()
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_append_only_audit_trail_allows_append_but_rejects_edits_and_deletes(self):
        old = make_accepted_adr()

        edited = copy.deepcopy(old)
        edited["audit_trail"][0]["by"] = "Someone Else"
        ok, message = self.module.check_append_only_audit_trail(old, edited)
        self.assertFalse(ok)
        self.assertIn("edited or reordered", message)

        deleted = copy.deepcopy(old)
        deleted["audit_trail"] = []
        ok, message = self.module.check_append_only_audit_trail(old, deleted)
        self.assertFalse(ok)
        self.assertIn("deleted", message)

        appended = copy.deepcopy(old)
        appended["audit_trail"].append(
            {"event": "reviewed", "by": "Reviewer", "at": "2026-04-01T10:00:00Z"}
        )
        ok, message = self.module.check_append_only_audit_trail(old, appended)
        self.assertTrue(ok, message)

    def test_immutable_after_acceptance_blocks_decision_core_changes(self):
        old = make_accepted_adr()
        changed = copy.deepcopy(old)
        changed["decision"]["rationale"] = "Changed rationale"

        ok, message = self.module.check_immutable_after_acceptance(
            old,
            changed,
            self.module.DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
        )
        self.assertFalse(ok)
        self.assertIn("decision core is immutable", message)
        self.assertIn("decision.rationale", message)

    def test_immutable_after_acceptance_allows_confirmation_updates_and_supersession(self):
        old = make_accepted_adr()

        confirmation = copy.deepcopy(old)
        confirmation["confirmation"] = {
            "description": "Verified in production",
            "artifact_ids": ["PR-42"],
        }
        ok, message = self.module.check_immutable_after_acceptance(
            old,
            confirmation,
            self.module.DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
        )
        self.assertTrue(ok, message)

        superseded = copy.deepcopy(old)
        superseded["adr"]["status"] = "superseded"
        superseded["lifecycle"]["superseded_by"] = "ADR-9999-replacement"
        ok, message = self.module.check_immutable_after_acceptance(
            old,
            superseded,
            self.module.DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
        )
        self.assertTrue(ok, message)

        invalid_status = copy.deepcopy(old)
        invalid_status["adr"]["status"] = "draft"
        ok, message = self.module.check_immutable_after_acceptance(
            old,
            invalid_status,
            self.module.DEFAULT_IMMUTABLE_AFTER_ACCEPTANCE_FIELDS,
        )
        self.assertFalse(ok)
        self.assertIn("may only remain 'accepted' or transition", message)

    def test_single_adr_rule_rejects_two_brand_new_mutually_pointing_files(self):
        new_adr = make_proposed_adr()
        new_adr["adr"]["id"] = "ADR-2000-new-decision"
        new_adr["lifecycle"]["supersedes"] = "ADR-1999-old-decision"

        fake_old = make_superseded_adr("ADR-2000-new-decision")
        fake_old["adr"]["id"] = "ADR-1999-old-decision"

        with tempfile.TemporaryDirectory() as tmpdir:
            new_path = self.write_temp_adr(new_adr, tmpdir)
            old_path = self.write_temp_adr(fake_old, tmpdir)

            with mock.patch.object(self.module, "get_file_at_base", return_value=None):
                passed, message = self.module.check_single_adr_per_pr([new_path, old_path])

        self.assertFalse(passed)
        self.assertIn("single_adr_per_pr", message)

    def test_single_adr_rule_allows_real_supersession_pair(self):
        new_adr = make_proposed_adr()
        new_adr["adr"]["id"] = "ADR-2000-new-decision"
        new_adr["lifecycle"]["supersedes"] = "ADR-1999-old-decision"

        old_base = make_accepted_adr()
        old_base["adr"]["id"] = "ADR-1999-old-decision"
        old_base["adr"]["title"] = "Legacy decision"

        old_current = copy.deepcopy(old_base)
        old_current["adr"]["status"] = "superseded"
        old_current["approvals"] = []
        old_current["lifecycle"]["superseded_by"] = "ADR-2000-new-decision"
        old_current["audit_trail"].append(
            {"event": "superseded", "by": "Architect", "at": "2026-03-03T10:00:00Z"}
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            new_path = self.write_temp_adr(new_adr, tmpdir)
            old_path = self.write_temp_adr(old_current, tmpdir)

            def base_lookup(filepath: str, *_args, **_kwargs) -> dict | None:
                if filepath == old_path:
                    return old_base
                return None

            with mock.patch.object(self.module, "get_file_at_base", side_effect=base_lookup):
                passed, message = self.module.check_single_adr_per_pr([new_path, old_path])

        self.assertTrue(passed, message)
        self.assertIn("ADR-2000-new-decision", message)
        self.assertIn("ADR-1999-old-decision", message)

    def test_single_adr_rule_rejects_pair_when_both_files_already_existed(self):
        new_current = make_proposed_adr()
        new_current["adr"]["id"] = "ADR-2000-new-decision"
        new_current["lifecycle"]["supersedes"] = "ADR-1999-old-decision"

        new_base = copy.deepcopy(new_current)

        old_current = make_superseded_adr("ADR-2000-new-decision")
        old_current["adr"]["id"] = "ADR-1999-old-decision"
        old_base = make_accepted_adr()
        old_base["adr"]["id"] = "ADR-1999-old-decision"

        with tempfile.TemporaryDirectory() as tmpdir:
            new_path = self.write_temp_adr(new_current, tmpdir)
            old_path = self.write_temp_adr(old_current, tmpdir)

            def base_lookup(filepath: str, *_args, **_kwargs) -> dict | None:
                if filepath == new_path:
                    return new_base
                if filepath == old_path:
                    return old_base
                return None

            with mock.patch.object(self.module, "get_file_at_base", side_effect=base_lookup):
                passed, message = self.module.check_single_adr_per_pr([new_path, old_path])

        self.assertFalse(passed)
        self.assertIn("single_adr_per_pr", message)

    def test_single_adr_rule_rejects_pair_when_existing_file_is_not_superseded(self):
        new_adr = make_proposed_adr()
        new_adr["adr"]["id"] = "ADR-2000-new-decision"
        new_adr["lifecycle"]["supersedes"] = "ADR-1999-old-decision"

        old_base = make_accepted_adr()
        old_base["adr"]["id"] = "ADR-1999-old-decision"

        old_current = copy.deepcopy(old_base)
        old_current["lifecycle"]["superseded_by"] = "ADR-2000-new-decision"

        with tempfile.TemporaryDirectory() as tmpdir:
            new_path = self.write_temp_adr(new_adr, tmpdir)
            old_path = self.write_temp_adr(old_current, tmpdir)

            def base_lookup(filepath: str, *_args, **_kwargs) -> dict | None:
                if filepath == old_path:
                    return old_base
                return None

            with mock.patch.object(self.module, "get_file_at_base", side_effect=base_lookup):
                passed, message = self.module.check_single_adr_per_pr([new_path, old_path])

        self.assertFalse(passed)
        self.assertIn("single_adr_per_pr", message)

    def test_detect_base_ref_normalizes_platform_specific_values(self):
        cases = [
            ("github", {"GITHUB_BASE_REF": "main"}, None, "origin/main"),
            (
                "azure-devops",
                {"SYSTEM_PULLREQUEST_TARGETBRANCH": "refs/heads/release/2026"},
                None,
                "origin/release/2026",
            ),
            ("gitlab", {"CI_MERGE_REQUEST_TARGET_BRANCH_NAME": "develop"}, None, "origin/develop"),
            ("github", {"GITHUB_BASE_REF": "main"}, "release/2026", "origin/release/2026"),
        ]

        for platform, env, explicit_base_ref, expected in cases:
            with self.subTest(platform=platform, expected=expected):
                with mock.patch.dict(self.module.os.environ, env, clear=True):
                    actual = self.module.detect_base_ref(platform, explicit_base_ref)
                self.assertEqual(actual, expected)

    def test_main_fails_closed_when_base_ref_is_missing_for_enforced_run(self):
        cases = [
            ("azure-devops", ["verify-approvals.py"], {"SYSTEM_TEAMFOUNDATIONCOLLECTIONURI": "https://dev.azure.com/example"}),
            ("gitlab", ["verify-approvals.py"], {"GITLAB_CI": "true"}),
            ("github", ["verify-approvals.py", "--platform", "github", "--repo", "owner/repo", "--pr", "42"], {}),
        ]

        for platform, argv, env in cases:
            with self.subTest(platform=platform):
                exit_code, stdout, stderr = self.run_main_with(argv, env, changed_files=None)

                self.assertEqual(exit_code, 2)
                self.assertIn("No governance config found", stdout)
                self.assertIn("No base ref could be resolved", stderr)

    def test_main_dry_run_allows_missing_base_ref(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adr_path = self.write_temp_adr(make_proposed_adr(), tmpdir)
            exit_code, stdout, stderr = self.run_main_with(
                ["verify-approvals.py", "--dry-run"],
                {"GITLAB_CI": "true"},
                [adr_path],
            )

        self.assertEqual(exit_code, 0)
        self.assertIn("DRY RUN", stdout)
        self.assertIn("No base ref could be resolved", stderr)

    def test_main_accepts_explicit_base_ref_override(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adr_path = self.write_temp_adr(make_proposed_adr(), tmpdir)

            with (
                mock.patch.object(self.module, "ensure_base_ref_available", return_value=None),
                mock.patch.object(self.module, "get_file_at_base", return_value=None),
            ):
                exit_code, stdout, stderr = self.run_main_with(
                    ["verify-approvals.py", "--dry-run", "--base-ref", "release/2026"],
                    {"SYSTEM_TEAMFOUNDATIONCOLLECTIONURI": "https://dev.azure.com/example"},
                    [adr_path],
                )

        self.assertEqual(exit_code, 0)
        self.assertIn("🔀 Base ref: origin/release/2026", stdout)
        self.assertIn("DRY RUN", stdout)
        self.assertEqual("", stderr)

    def test_verify_approvals_fails_closed_when_approver_data_is_unavailable(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adr_path = self.write_temp_adr(make_proposed_adr(), tmpdir)
            stdout = io.StringIO()
            stderr = io.StringIO()

            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                with mock.patch.object(self.module, "get_file_at_base", return_value=None):
                    exit_code = self.module.verify_approvals(
                        "github",
                        None,
                        None,
                        [adr_path],
                        self.make_config(),
                    )

        self.assertEqual(exit_code, 1)
        self.assertIn("approval identity verification required", stdout.getvalue())
        self.assertIn("Use --dry-run for advisory mode", stderr.getvalue())

    def test_verify_approvals_dry_run_remains_advisory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adr_path = self.write_temp_adr(make_proposed_adr(), tmpdir)
            stdout = io.StringIO()
            stderr = io.StringIO()

            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = self.module.verify_approvals(
                    "github",
                    None,
                    None,
                    [adr_path],
                    self.make_config(),
                    allow_missing_base=True,
                    dry_run=True,
                )

        self.assertEqual(exit_code, 0)
        self.assertIn("DRY RUN", stdout.getvalue())
        self.assertEqual("", stderr.getvalue())

    def test_verify_approvals_maintenance_only_change_still_skips_identity_lookup(self):
        old = make_proposed_adr()
        updated = copy.deepcopy(old)
        updated["confirmation"]["description"] = "Linked rollout evidence"

        with tempfile.TemporaryDirectory() as tmpdir:
            adr_path = self.write_temp_adr(updated, tmpdir)
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                mock.patch.object(self.module, "get_file_at_base", return_value=old),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = self.module.verify_approvals(
                    "github",
                    None,
                    None,
                    [adr_path],
                    self.make_config(),
                )

        self.assertEqual(exit_code, 0)
        self.assertIn("Maintenance change detected", stdout.getvalue())
        self.assertEqual("", stderr.getvalue())

    def test_main_fails_closed_when_ci_metadata_is_missing(self):
        cases = [
            (
                "github",
                ["verify-approvals.py"],
                {"GITHUB_ACTIONS": "1", "GITHUB_BASE_REF": "main"},
            ),
            (
                "azure-devops",
                ["verify-approvals.py"],
                {
                    "SYSTEM_TEAMFOUNDATIONCOLLECTIONURI": "https://dev.azure.com/example",
                    "SYSTEM_PULLREQUEST_TARGETBRANCH": "refs/heads/main",
                },
            ),
            (
                "gitlab",
                ["verify-approvals.py"],
                {"GITLAB_CI": "true", "CI_MERGE_REQUEST_TARGET_BRANCH_NAME": "main"},
            ),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            adr_path = self.write_temp_adr(make_proposed_adr(), tmpdir)

            for platform, argv, env in cases:
                with self.subTest(platform=platform):
                    with mock.patch.object(self.module, "ensure_base_ref_available", return_value=None):
                        exit_code, stdout, stderr = self.run_main_with(argv, env, [adr_path])

                    self.assertEqual(exit_code, 1)
                    self.assertIn("approval identity verification required", stdout)
                    self.assertIn("Use --dry-run for advisory mode", stderr)

    def test_main_fails_closed_when_github_token_is_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adr_path = self.write_temp_adr(make_proposed_adr(), tmpdir)
            with mock.patch.object(self.module, "ensure_base_ref_available", return_value=None):
                exit_code, stdout, stderr = self.run_main_with(
                    [
                        "verify-approvals.py",
                        "--platform",
                        "github",
                        "--repo",
                        "owner/repo",
                        "--pr",
                        "42",
                        "--base-ref",
                        "main",
                    ],
                    {},
                    [adr_path],
                )

        self.assertEqual(exit_code, 1)
        self.assertIn("approval identity verification required", stdout)
        self.assertIn("Use --dry-run for advisory mode", stderr)


if __name__ == "__main__":
    unittest.main()
