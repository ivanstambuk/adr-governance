from __future__ import annotations

import json
import unittest

from _helpers import REPO_ROOT


def read_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text()


class AssetConsistencyTests(unittest.TestCase):
    def test_ai_instruction_assets_use_current_audit_trail_fields(self):
        for path in [
            ".skills/adr-author/SKILL.md",
            "repomix-instruction.md",
        ]:
            text = read_text(path)
            self.assertNotIn('date: "2026-03-06"', text, path)
            self.assertNotIn('author: "AI Assistant"', text, path)
            self.assertNotIn('description: "ADR generated from uploaded artifacts', text, path)
            self.assertIn('by: "AI Assistant"', text, path)
            self.assertIn('details: "ADR generated from uploaded artifacts', text, path)

    def test_instruction_assets_reference_description_not_summary_for_alternatives(self):
        text = read_text("repomix-instruction.md")
        self.assertNotIn("alternatives[].summary", text)
        self.assertIn("alternatives[].description", text)

    def test_branch_naming_examples_are_consistent(self):
        for path in [
            "README.md",
            "docs/web-chat-quickstart.md",
            "repomix-instruction.md",
        ]:
            text = read_text(path)
            self.assertNotIn("adr/NNNN-short-title", text, path)
            self.assertNotIn("adr/0001-your-decision-title", text, path)

        self.assertIn("adr/ADR-NNNN-short-title", read_text("repomix-instruction.md"))
        self.assertIn("adr/ADR-0001-your-decision-title", read_text("README.md"))

    def test_docs_reference_current_field_names_and_config_locations(self):
        readme = read_text("README.md")
        ci_setup = read_text("docs/ci-setup.md")

        self.assertNotIn("| `requirements` |", readme)
        self.assertIn("| `architecturally_significant_requirements` |", readme)
        self.assertNotIn("alternatives with summary", readme.lower())
        self.assertIn(".yamllint.yml", ci_setup)
        self.assertNotIn("edit the `yamllint` configuration in the pipeline file", ci_setup)

    def test_bundle_scope_matches_portable_authoring_query_boundary(self):
        config = json.loads(read_text("repomix.config.json"))

        self.assertEqual(
            config["include"],
            [
                "schemas/**",
                "architecture-decision-log/**",
                "examples-reference/**",
                ".skills/**",
                "docs/adr-process.md",
                "docs/glossary.md",
                "docs/ai-authoring.md",
                "scripts/validate-adr.py",
                "README.md",
            ],
        )

        ignored = set(config["ignore"]["customPatterns"])
        for pattern in [
            "docs/web-chat-quickstart.md",
            "docs/ci-setup.md",
            "scripts/verify-approvals.py",
            "scripts/render-adr.py",
            "scripts/extract-decisions.py",
            "scripts/bundle.sh",
            "docs/research/**",
            ".github/**",
        ]:
            self.assertIn(pattern, ignored)

        header_text = config["output"]["headerText"]
        self.assertIn("Repository-side CI setup and PR enforcement internals are intentionally not bundled.", header_text)
        self.assertIn("the repository's local validation and CI checks remain the final authority", header_text)

    def test_bundle_instruction_stays_within_bundle_boundary(self):
        text = read_text("repomix-instruction.md")

        self.assertNotIn("search for `review-adr.py`", text)
        self.assertNotIn("search for `verify-approvals.py`", text)
        self.assertNotIn("search for `extract-decisions.py`", text)
        self.assertNotIn("Branch protection and CODEOWNERS configuration", text)
        self.assertIn("repository-side concerns outside this bundle", text)
        self.assertIn("filename exactly matches `adr.id`", text)
        self.assertIn("PR approval identity binding is confirmed in-repo", text)


if __name__ == "__main__":
    unittest.main()
