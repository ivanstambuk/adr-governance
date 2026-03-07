from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from _helpers import REPO_ROOT, load_example_adr, load_module, write_yaml


class ValidateAdrTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module("validate_adr", "scripts/validate-adr.py")
        cls.validator = cls.module.build_validator(cls.module.load_schema())

    def test_format_errors_are_enforced(self):
        data = load_example_adr()
        data["adr"]["created_at"] = "not-a-datetime"
        data["authors"][0]["email"] = "not-an-email"
        data["decision_owner"]["email"] = "still-not-an-email"
        data["references"][0]["url"] = "not-a-uri"
        data["audit_trail"][0]["at"] = "not-a-datetime"

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
            errors, _warnings = self.module.validate_file(path, self.validator)

        joined = "\n".join(errors)
        self.assertIn("adr.created_at", joined)
        self.assertIn("authors.0.email", joined)
        self.assertIn("decision_owner.email", joined)
        self.assertIn("references.0.url", joined)
        self.assertIn("audit_trail.0.at", joined)

    def test_filename_must_exactly_match_adr_id(self):
        data = load_example_adr()
        data["adr"]["id"] = "ADR-9999-id-bar"

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / "ADR-9999-filename-foo.yaml", data)
            errors, _warnings = self.module.validate_file(path, self.validator)

        self.assertTrue(
            any("does not exactly match" in error for error in errors),
            errors,
        )

    def test_last_modified_before_created_at_warns(self):
        data = load_example_adr()
        data["adr"]["created_at"] = "2026-03-06T10:00:00Z"
        data["adr"]["last_modified"] = "2026-03-05T10:00:00Z"

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
            _errors, warnings = self.module.validate_file(path, self.validator)

        self.assertTrue(
            any("adr.last_modified" in warning for warning in warnings),
            warnings,
        )

    def test_duplicate_ids_fail_when_validating_multiple_directories(self):
        data_a = load_example_adr()
        data_b = load_example_adr()
        data_b["adr"]["title"] = "Duplicate ID in another directory"

        with tempfile.TemporaryDirectory() as tmp_dir:
            dir_a = Path(tmp_dir) / "architecture-decision-log"
            dir_b = Path(tmp_dir) / "examples-reference"
            dir_a.mkdir()
            dir_b.mkdir()
            write_yaml(dir_a / f"{data_a['adr']['id']}.yaml", data_a)
            write_yaml(dir_b / f"{data_b['adr']['id']}.yaml", data_b)

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/validate-adr.py",
                    str(dir_a),
                    str(dir_b),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("duplicate ADR ID", result.stdout)

    def test_terminal_status_without_matching_audit_event_fails(self):
        data = load_example_adr()
        data["adr"]["status"] = "rejected"
        data["audit_trail"] = [
            {"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"},
        ]
        data["approvals"] = []

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
            errors, _warnings = self.module.validate_file(path, self.validator)

        self.assertTrue(
            any("status is 'rejected' but no 'rejected' event" in error for error in errors),
            errors,
        )

    def test_invalid_status_audit_event_combination_fails(self):
        data = load_example_adr()
        data["adr"]["status"] = "draft"
        data["approvals"] = []
        data["audit_trail"] = [
            {"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"},
            {"event": "approved", "by": "Architect", "at": "2026-03-02T10:00:00Z"},
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
            errors, _warnings = self.module.validate_file(path, self.validator)

        self.assertTrue(
            any("invalid state transition" in error for error in errors),
            errors,
        )

    def test_rejected_and_deferred_do_not_require_approval_metadata(self):
        cases = [
            (
                "rejected",
                [
                    {"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"},
                    {"event": "rejected", "by": "Architect", "at": "2026-03-05T10:00:00Z"},
                ],
            ),
            (
                "deferred",
                [
                    {"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"},
                    {"event": "deferred", "by": "Architect", "at": "2026-03-05T10:00:00Z"},
                ],
            ),
        ]

        for status, audit_trail in cases:
            with self.subTest(status=status):
                data = load_example_adr()
                data["adr"]["status"] = status
                data["approvals"] = []
                data["audit_trail"] = audit_trail

                with tempfile.TemporaryDirectory() as tmp_dir:
                    path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
                    errors, _warnings = self.module.validate_file(path, self.validator)

                self.assertEqual(errors, [])

    def test_archival_on_non_terminal_status_fails(self):
        data = load_example_adr()
        data["adr"]["status"] = "accepted"
        data["lifecycle"]["archival"] = {
            "archived_at": "2026-03-06T10:00:00Z",
            "archive_reason": "Testing invalid archival",
        }
        data["audit_trail"].append(
            {"event": "archived", "by": "Architect", "at": "2026-03-06T10:00:00Z"}
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
            errors, _warnings = self.module.validate_file(path, self.validator)

        self.assertTrue(
            any("archived ADRs should have a terminal status" in error for error in errors),
            errors,
        )

    def test_archival_metadata_requires_archived_event(self):
        data = load_example_adr()
        data["adr"]["status"] = "rejected"
        data["approvals"] = []
        data["audit_trail"] = [
            {"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"},
            {"event": "rejected", "by": "Architect", "at": "2026-03-05T10:00:00Z"},
        ]
        data["lifecycle"]["archival"] = {
            "archived_at": "2026-03-06T10:00:00Z",
            "archive_reason": "No longer relevant",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
            errors, _warnings = self.module.validate_file(path, self.validator)

        self.assertTrue(
            any("no 'archived' event found in audit_trail" in error for error in errors),
            errors,
        )

    def test_archived_event_requires_archival_metadata(self):
        data = load_example_adr()
        data["adr"]["status"] = "rejected"
        data["approvals"] = []
        data["audit_trail"] = [
            {"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"},
            {"event": "rejected", "by": "Architect", "at": "2026-03-05T10:00:00Z"},
            {"event": "archived", "by": "Architect", "at": "2026-03-06T10:00:00Z"},
        ]
        data["lifecycle"]["archival"] = {
            "archived_at": None,
            "archive_reason": None,
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
            errors, _warnings = self.module.validate_file(path, self.validator)

        self.assertTrue(
            any("audit_trail contains 'archived' event but lifecycle.archival.archived_at is missing" in error for error in errors),
            errors,
        )

    def test_valid_archival_requires_metadata_and_event(self):
        data = load_example_adr()
        data["adr"]["status"] = "rejected"
        data["approvals"] = []
        data["audit_trail"] = [
            {"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"},
            {"event": "rejected", "by": "Architect", "at": "2026-03-05T10:00:00Z"},
            {"event": "archived", "by": "Architect", "at": "2026-03-06T10:00:00Z"},
        ]
        data["lifecycle"]["archival"] = {
            "archived_at": "2026-03-06T10:00:00Z",
            "archive_reason": "No longer relevant",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
            errors, _warnings = self.module.validate_file(path, self.validator)

        self.assertEqual(errors, [])

    def test_superseded_status_requires_superseded_by(self):
        data = load_example_adr()
        data["adr"]["status"] = "superseded"
        data["approvals"] = []
        data["lifecycle"]["superseded_by"] = None
        data["audit_trail"] = [
            {"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"},
            {"event": "superseded", "by": "Architect", "at": "2026-03-06T10:00:00Z"},
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
            errors, _warnings = self.module.validate_file(path, self.validator)

        self.assertTrue(
            any("adr.status is 'superseded' but lifecycle.superseded_by is missing" in error for error in errors),
            errors,
        )

    def test_supersession_symmetry_is_a_cross_reference_error(self):
        current = load_example_adr()
        current["adr"]["id"] = "ADR-9001-current-decision"
        current["adr"]["title"] = "Current decision"
        current["lifecycle"]["supersedes"] = "ADR-9000-old-decision"

        previous = load_example_adr()
        previous["adr"]["id"] = "ADR-9000-old-decision"
        previous["adr"]["title"] = "Old decision"
        previous["lifecycle"]["superseded_by"] = None

        with tempfile.TemporaryDirectory() as tmp_dir:
            path_current = write_yaml(Path(tmp_dir) / f"{current['adr']['id']}.yaml", current)
            path_previous = write_yaml(Path(tmp_dir) / f"{previous['adr']['id']}.yaml", previous)
            all_data = {}
            for path in [path_current, path_previous]:
                with open(path, "r") as f:
                    all_data[str(path)] = self.module.yaml.safe_load(f)

            errors, warnings = self.module.validate_cross_references(all_data)

        self.assertTrue(
            any("lifecycle.supersedes 'ADR-9000-old-decision'" in error for error in errors),
            errors,
        )
        self.assertEqual(warnings, [])

    def test_missing_supersedes_target_is_a_cross_reference_error(self):
        current = load_example_adr()
        current["adr"]["id"] = "ADR-9001-current-decision"
        current["adr"]["title"] = "Current decision"
        current["lifecycle"]["supersedes"] = "ADR-9999-missing-decision"

        with tempfile.TemporaryDirectory() as tmp_dir:
            path_current = write_yaml(Path(tmp_dir) / f"{current['adr']['id']}.yaml", current)
            all_data = {str(path_current): current}

            errors, warnings = self.module.validate_cross_references(
                all_data,
                {str(path_current)},
            )

        self.assertTrue(
            any("no ADR with id 'ADR-9999-missing-decision' was found" in error for error in errors),
            errors,
        )
        self.assertEqual(warnings, [])

    def test_missing_superseded_by_target_is_a_cross_reference_error(self):
        previous = load_example_adr()
        previous["adr"]["id"] = "ADR-9000-old-decision"
        previous["adr"]["title"] = "Old decision"
        previous["adr"]["status"] = "superseded"
        previous["approvals"] = []
        previous["lifecycle"]["superseded_by"] = "ADR-9001-current-decision"
        previous["audit_trail"] = [
            {"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"},
            {"event": "superseded", "by": "Architect", "at": "2026-03-06T10:00:00Z"},
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            path_previous = write_yaml(Path(tmp_dir) / f"{previous['adr']['id']}.yaml", previous)
            all_data = {str(path_previous): previous}

            errors, warnings = self.module.validate_cross_references(
                all_data,
                {str(path_previous)},
            )

        self.assertTrue(
            any("no ADR with id 'ADR-9001-current-decision' was found" in error for error in errors),
            errors,
        )
        self.assertEqual(warnings, [])

    def test_single_file_validation_loads_repo_context_for_supersession_targets(self):
        current = load_example_adr()
        current["adr"]["id"] = "ADR-9001-current-decision"
        current["adr"]["title"] = "Current decision"
        current["lifecycle"]["supersedes"] = "ADR-9000-old-decision"

        previous = load_example_adr()
        previous["adr"]["id"] = "ADR-9000-old-decision"
        previous["adr"]["title"] = "Old decision"
        previous["adr"]["status"] = "superseded"
        previous["approvals"] = []
        previous["lifecycle"]["superseded_by"] = "ADR-9001-current-decision"
        previous["audit_trail"] = [
            {"event": "created", "by": "Author", "at": "2026-03-01T10:00:00Z"},
            {"event": "superseded", "by": "Architect", "at": "2026-03-06T10:00:00Z"},
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            governed_dir = repo_root / "architecture-decision-log"
            governed_dir.mkdir()
            (repo_root / "examples-reference").mkdir()

            path_current = write_yaml(governed_dir / f"{current['adr']['id']}.yaml", current)
            path_previous = write_yaml(governed_dir / f"{previous['adr']['id']}.yaml", previous)

            with mock.patch.object(self.module, "REPO_ROOT", repo_root):
                all_data, primary_filepaths = self.module.build_cross_reference_corpus([path_current])
                errors, warnings = self.module.validate_cross_references(all_data, primary_filepaths)

        self.assertIn(str(path_current), primary_filepaths)
        self.assertIn(str(path_previous), all_data)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_single_file_validation_does_not_load_other_governed_directory_context(self):
        current = load_example_adr()
        current["adr"]["id"] = "ADR-9001-current-decision"
        current["adr"]["title"] = "Current decision"

        duplicate_in_examples = load_example_adr()
        duplicate_in_examples["adr"]["id"] = current["adr"]["id"]
        duplicate_in_examples["adr"]["title"] = "Duplicate ID in examples corpus"

        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            governed_dir = repo_root / "architecture-decision-log"
            examples_dir = repo_root / "examples-reference"
            governed_dir.mkdir()
            examples_dir.mkdir()

            path_current = write_yaml(governed_dir / f"{current['adr']['id']}.yaml", current)
            path_example = write_yaml(
                examples_dir / f"{duplicate_in_examples['adr']['id']}.yaml",
                duplicate_in_examples,
            )

            with mock.patch.object(self.module, "REPO_ROOT", repo_root):
                all_data, primary_filepaths = self.module.build_cross_reference_corpus([path_current])
                errors, warnings = self.module.validate_cross_references(all_data, primary_filepaths)

        self.assertIn(str(path_current), all_data)
        self.assertNotIn(str(path_example), all_data)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_missing_schema_version_remains_a_warning(self):
        data = load_example_adr()
        data["adr"].pop("schema_version", None)

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = write_yaml(Path(tmp_dir) / f"{data['adr']['id']}.yaml", data)
            errors, warnings = self.module.validate_file(path, self.validator)

        self.assertEqual(errors, [])
        self.assertTrue(
            any("adr.schema_version" in warning for warning in warnings),
            warnings,
        )


if __name__ == "__main__":
    unittest.main()
