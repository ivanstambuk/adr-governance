from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _helpers import EXAMPLE_ADR, REPO_ROOT, load_example_adr, write_yaml


class ToolOutputTests(unittest.TestCase):
    def test_render_output_shows_pending_approvers(self):
        data = load_example_adr()
        data["adr"]["status"] = "proposed"
        data["approvals"] = [
            {
                "name": "Jane Doe",
                "role": "Lead Architect",
                "identity": "@janedoe",
                "approved_at": None,
            }
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            adr_path = write_yaml(
                Path(tmp_dir) / f"{data['adr']['id']}.yaml",
                data,
            )
            result = subprocess.run(
                [sys.executable, "scripts/render-adr.py", str(adr_path)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True,
            )

        self.assertIn("**Approvals:** Jane Doe (Lead Architect) [@janedoe] — pending", result.stdout)

    def test_extract_decisions_json_contract(self):
        result = subprocess.run(
            [
                sys.executable,
                "scripts/extract-decisions.py",
                "--format",
                "json",
                "examples-reference/",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(result.stdout)

        self.assertEqual(payload["count"], 21)
        first = payload["active_decisions"][0]
        self.assertEqual(first["id"], "ADR-0001-dpop-over-mtls-for-sender-constrained-tokens")
        self.assertIn("chosen_alternative", first)
        self.assertIn("rationale", first)

    def test_summarize_output_contract(self):
        result = subprocess.run(
            [sys.executable, "scripts/summarize-adr.py", str(EXAMPLE_ADR)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertIn("## ADR-0001-dpop-over-mtls-for-sender-constrained-tokens", result.stdout)
        self.assertIn("**Decision:**", result.stdout)
        self.assertIn("**Alternatives considered:**", result.stdout)


if __name__ == "__main__":
    unittest.main()
