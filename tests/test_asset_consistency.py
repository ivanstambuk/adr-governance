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

    def test_draft_is_defined_as_complete_but_not_yet_proposed(self):
        process = read_text("docs/adr-process.md")
        glossary = read_text("docs/glossary.md")
        instruction = read_text("repomix-instruction.md")
        template = read_text(".skills/adr-author/assets/adr-template.yaml")

        self.assertNotIn("WIP on feature branch.<br>Not ready for review.", process)
        self.assertIn("Schema-valid, not yet proposed.", process)
        self.assertIn("schema-valid and substantially complete", process)
        self.assertIn("Schema-valid, substantially complete ADR", glossary)
        self.assertIn("schema-valid ADR that is complete enough to validate but not yet proposed", instruction)
        self.assertIn("`draft` means author-owned and not yet proposed", template)

    def test_llms_full_source_list_is_centralized(self):
        generator = read_text("scripts/generate-llms-full.sh")
        hook = read_text(".githooks/pre-commit")

        self.assertIn("--print-sources", generator)
        self.assertIn("generate-llms-full.sh --print-sources", hook)

    def test_periodic_review_is_documented_as_external_process(self):
        process = read_text("docs/adr-process.md")
        template = read_text(".skills/adr-author/assets/adr-template.yaml")
        schema_ref = read_text(".skills/adr-author/references/SCHEMA_REFERENCE.md")

        self.assertNotIn("will be flagged for periodic review", process)
        self.assertIn("does **not** schedule reminders, create tickets, open pull requests, or fail CI", process)
        self.assertIn("not automatically scheduled/enforced by this repo", template)
        self.assertIn("Review scheduling/reminders are outside this repo's scope", schema_ref)

    def test_committed_generated_artifacts_boundary_is_documented(self):
        readme = read_text("README.md")
        rendering = read_text("docs/rendering.md")
        ci_setup = read_text("docs/ci-setup.md")
        decision_enforcement = read_text("docs/decision-enforcement.md")
        web_chat = read_text("docs/web-chat-quickstart.md")

        self.assertIn("CI verifies that committed renderings and `llms-full.txt` stay current", readme)
        self.assertIn("CI also regenerates and verifies the committed artifacts", rendering)
        self.assertIn("`adr-governance-bundle.md`) is intentionally different", rendering)
        self.assertIn("Freshness checks for committed generated artifacts", ci_setup)
        self.assertIn("bundle is treated as an on-demand export artifact", decision_enforcement)
        self.assertIn("not as a freshness-checked committed deliverable", web_chat)

    def test_llm_and_ci_docs_describe_current_boundaries_honestly(self):
        readme = read_text("README.md")
        llms = read_text("llms.txt")
        process = read_text("docs/adr-process.md")
        ci_setup = read_text("docs/ci-setup.md")
        glossary = read_text("docs/glossary.md")
        generator = read_text("scripts/generate-llms-full.sh")

        self.assertIn("curated inline documentation", readme)
        self.assertIn("curated inline documentation", llms)
        self.assertIn("portable projection", llms)
        self.assertIn("extract-decisions.py", llms)
        self.assertIn("repository scripts do not currently add a second independent self-approval check", process)
        self.assertIn("This identity-binding rule applies to the proposal/acceptance path only", process)
        self.assertIn("Deferred ADRs likewise do not use approval-identity verification", process)
        self.assertIn("mainly improves auditability and CI messaging", process)
        self.assertIn("mainly affects auditability / CI messaging", glossary)
        self.assertIn("Rejected/deferred outcomes rely on terminal audit events plus PR/MR history", glossary)
        self.assertIn("custom PR metadata and base-ref wiring", readme)
        self.assertIn("AWS CodeBuild and GCP Cloud Build templates run the verifier in dry-run mode by default", ci_setup)
        self.assertIn("--base-ref <branch>", ci_setup)
        self.assertIn(
            "must provide resolvable PR metadata and a base ref or the verifier fails closed",
            ci_setup,
        )
        self.assertIn("identity-bound through `approvals[]`", ci_setup)
        self.assertIn("terminal audit events plus PR/MR history instead", read_text(".skills/adr-author/references/SCHEMA_REFERENCE.md"))
        self.assertIn("curated inline documentation set", generator)

    def test_ci_templates_fetch_history_for_base_branch_comparisons(self):
        azure = read_text("ci/azure-devops/azure-pipelines.yml")
        gitlab = read_text("ci/gitlab-ci/.gitlab-ci.yml")

        self.assertIn("fetchDepth: 0", azure)
        self.assertIn('GIT_DEPTH: "0"', gitlab)

    def test_examples_are_documented_and_validated_as_separate_default_corpus(self):
        readme = read_text("README.md")
        ci_setup = read_text("docs/ci-setup.md")
        examples = read_text("examples-reference/README.md")
        runner = read_text("scripts/run-validation.sh")

        self.assertIn("validates `architecture-decision-log/` and `examples-reference/` separately", readme)
        self.assertIn("validates `architecture-decision-log/` and `examples-reference/` separately", ci_setup)
        self.assertIn("validates these examples separately", examples)
        self.assertIn("single `python3 scripts/validate-adr.py ...` invocation", readme)
        self.assertIn("single [`scripts/validate-adr.py`", examples)
        self.assertIn("Validating governed ADR corpus", runner)
        self.assertIn("Validating fictional ADR examples", runner)
        self.assertIn("Validating real-world ADR examples", runner)


if __name__ == "__main__":
    unittest.main()
