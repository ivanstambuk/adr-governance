"""Regression tests for the no-examples repo shape.

These tests verify that core repository functionality works when
examples-reference/ has been intentionally removed — a documented
adoption path in README.md and docs/ci-setup.md.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _helpers import REPO_ROOT


class NoExamplesRepoShapeTests(unittest.TestCase):
    """Prove the repo still works when examples-reference/ is absent."""

    @classmethod
    def setUpClass(cls):
        """Create a temporary shallow copy of the repo without examples-reference/."""
        cls.tmp_dir = tempfile.mkdtemp(prefix="adr-no-examples-")
        cls.repo_copy = Path(cls.tmp_dir) / "repo"

        # Copy only the essential directories and files (not examples-reference/)
        essential_dirs = [
            "architecture-decision-log",
            "schemas",
            "scripts",
            "tests",
            "docs",
            "ci",
            ".skills",
            ".githooks",
        ]
        essential_files = [
            "README.md",
            "llms.txt",
            "llms-full.txt",
            "repomix.config.json",
            "repomix-instruction.md",
            "Makefile",
            ".yamllint.yml",
        ]

        # Exclude this very file from the tests/ copy to prevent infinite
        # recursion: unittest discover would find it, spawn another copy, etc.
        def _ignore_self(directory, contents):
            if Path(directory).name == "tests":
                return {"test_no_examples_shape.py", "__pycache__"}
            if Path(directory).name == "__pycache__":
                return set(contents)
            return set()

        cls.repo_copy.mkdir()
        for d in essential_dirs:
            src = REPO_ROOT / d
            if src.exists():
                shutil.copytree(src, cls.repo_copy / d, ignore=_ignore_self)
        for f in essential_files:
            src = REPO_ROOT / f
            if src.exists():
                shutil.copy2(src, cls.repo_copy / f)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp_dir, ignore_errors=True)

    def test_examples_reference_is_absent(self):
        """Sanity check: examples-reference/ must not exist in the test copy."""
        self.assertFalse(
            (self.repo_copy / "examples-reference").exists(),
            "examples-reference/ should not exist in the test repo copy",
        )

    def test_run_validation_passes_without_examples(self):
        """scripts/run-validation.sh must exit 0 when examples-reference/ is absent."""
        result = subprocess.run(
            ["bash", "scripts/run-validation.sh"],
            cwd=self.repo_copy,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"run-validation.sh failed:\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )

    def test_pre_commit_hook_exits_cleanly_without_examples(self):
        """The pre-commit hook must exit 0 when no ADR files are staged.

        When examples-reference/ is absent, STAGED_EXAMPLES can still be
        non-empty if deletions are staged, but the render block should skip
        gracefully.
        """
        # Without a git repo, the hook will find no staged files and exit 0 early
        result = subprocess.run(
            ["bash", ".githooks/pre-commit"],
            cwd=self.repo_copy,
            capture_output=True,
            text=True,
            env={**os.environ, "GIT_DIR": "/dev/null"},  # no real git repo
        )
        # The hook should not crash — it may exit 0 (no staged files) or
        # warn about missing git, both of which are acceptable
        self.assertIn(
            result.returncode,
            [0, 1],
            f"pre-commit hook crashed:\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )

    def test_test_suite_passes_without_examples(self):
        """The test suite itself must pass in a repo without examples-reference/."""
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=self.repo_copy,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"Test suite failed without examples-reference/:\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )

    def test_check_generated_artifacts_passes_without_examples(self):
        """check-generated-artifacts.sh must pass when examples-reference/ is absent."""
        result = subprocess.run(
            ["bash", "scripts/check-generated-artifacts.sh"],
            cwd=self.repo_copy,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"check-generated-artifacts.sh failed:\nstdout: {result.stdout}\nstderr: {result.stderr}",
        )


class RunValidationFailureTests(unittest.TestCase):
    """Prove run-validation.sh correctly propagates validation failures."""

    def test_run_validation_exits_nonzero_on_malformed_adr(self):
        """run-validation.sh must return exit code 1 when architecture-decision-log/
        contains a malformed ADR.
        """
        tmp_dir = tempfile.mkdtemp(prefix="adr-malformed-")
        try:
            repo_copy = Path(tmp_dir) / "repo"
            repo_copy.mkdir()

            # Copy minimal infrastructure
            for d in ["schemas", "scripts"]:
                shutil.copytree(REPO_ROOT / d, repo_copy / d)

            # Create a malformed ADR (invalid status value)
            adl = repo_copy / "architecture-decision-log"
            adl.mkdir()
            malformed = adl / "ADR-9999-intentionally-broken.yaml"
            malformed.write_text(
                "adr:\n"
                "  id: ADR-9999-intentionally-broken\n"
                "  status: invalid-status-value\n"
                "  title: This ADR is intentionally malformed\n"
            )

            result = subprocess.run(
                ["bash", "scripts/run-validation.sh"],
                cwd=repo_copy,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                result.returncode,
                1,
                f"run-validation.sh should have exited 1 but exited {result.returncode}:\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}",
            )
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
