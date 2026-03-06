# Contributing to ADR Governance

Thank you for considering contributing to the ADR Governance framework!

## How to contribute

### Reporting issues

- Open a [GitHub Issue](https://github.com/ivanstambuk/adr-governance/issues) describing the bug, gap, or improvement.
- Include the relevant file paths and, if applicable, a minimal reproduction case.

### Submitting changes

1. **Fork the repository** and create a feature branch.
2. **Make your changes.** Follow the existing code style:
   - Python: PEP 8, type hints encouraged
   - YAML: validated by `yamllint` with the repo's `.yamllint.yml` config
   - Markdown: one sentence per line preferred for clean diffs
3. **Validate** before submitting:
   ```bash
   pip install -r requirements.txt
   python3 scripts/validate-adr.py architecture-decision-log/ examples-reference/
   yamllint -c .yamllint.yml architecture-decision-log/ examples-reference/
   ```
4. **Open a pull request** against `main`. Describe what you changed and why.

### What can I contribute?

- **Schema improvements**: Changes to `schemas/adr.schema.json` — please include updated examples and validator checks.
- **Documentation**: Fixes, clarifications, or new guides in `docs/`.
- **Tooling**: Enhancements to the Python scripts in `scripts/`.
- **CI pipelines**: Improvements to platform-specific configs in `ci/` and `.github/workflows/`.
- **Examples**: New example ADRs in `examples-reference/` that demonstrate edge cases or new decision types.

### What requires special care?

- **Schema changes** must be backward-compatible or bump the `schema_version`.
- **ADR template** (`.skills/adr-author/assets/adr-template.yaml`) must stay in sync with the schema.
- **Glossary** (`docs/glossary.md` + `.skills/adr-author/references/GLOSSARY.md`) and **Schema Reference** (`.skills/adr-author/references/SCHEMA_REFERENCE.md`) must reflect any enum or field changes.

## Code of Conduct

Be respectful, constructive, and assume good intentions.
