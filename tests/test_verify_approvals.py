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
        changed_files: list[str],
    ) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(self.module, "load_governance_config", return_value=self.make_config()),
            mock.patch.object(self.module, "get_pr_author", return_value=None),
            mock.patch.object(self.module, "get_changed_yaml_files", return_value=changed_files),
            mock.patch.dict(self.module.os.environ, env, clear=True),
            mock.patch.object(sys, "argv", argv),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
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

    def test_verify_approvals_fails_closed_when_approver_data_is_unavailable(self):
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
            ("github", ["verify-approvals.py"], {"GITHUB_ACTIONS": "1"}),
            (
                "azure-devops",
                ["verify-approvals.py"],
                {"SYSTEM_TEAMFOUNDATIONCOLLECTIONURI": "https://dev.azure.com/example"},
            ),
            ("gitlab", ["verify-approvals.py"], {"GITLAB_CI": "true"}),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            adr_path = self.write_temp_adr(make_proposed_adr(), tmpdir)

            for platform, argv, env in cases:
                with self.subTest(platform=platform):
                    exit_code, stdout, stderr = self.run_main_with(argv, env, [adr_path])

                    self.assertEqual(exit_code, 1)
                    self.assertIn("approval identity verification required", stdout)
                    self.assertIn("Use --dry-run for advisory mode", stderr)

    def test_main_fails_closed_when_github_token_is_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adr_path = self.write_temp_adr(make_proposed_adr(), tmpdir)
            exit_code, stdout, stderr = self.run_main_with(
                ["verify-approvals.py", "--platform", "github", "--repo", "owner/repo", "--pr", "42"],
                {},
                [adr_path],
            )

        self.assertEqual(exit_code, 1)
        self.assertIn("approval identity verification required", stdout)
        self.assertIn("Use --dry-run for advisory mode", stderr)


if __name__ == "__main__":
    unittest.main()
