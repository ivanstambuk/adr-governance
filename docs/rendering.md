# Rendered Markdown — Human-Friendly ADR Views

ADRs are authored and stored as **structured YAML** — optimised for machine consumption, validation, and AI-assisted workflows. But humans need a readable format too. Every ADR YAML file has a corresponding **Markdown rendering** for browsing on GitHub, Azure DevOps, GitLab, and any platform that renders Markdown natively.

---

## Rendered files

| Path | Description |
|------|-------------|
| [`architecture-decision-log/rendered/architecture-decision-log.md`](../architecture-decision-log/rendered/architecture-decision-log.md) | Decision log index — clickable links, status, and decision dates |
| `architecture-decision-log/rendered/ADR-NNNN-*.md` | Individual ADR renderings with a provenance disclaimer |
| [`examples-reference/rendered/`](../examples-reference/rendered/) | Rendered example ADRs (fictional reference set) |

> **⚠️ Do not edit files in `rendered/` directly.** They are auto-generated from the YAML source. Each rendered file includes a `[!CAUTION]` banner and an HTML comment pointing to the authoritative source YAML.

---

## Pre-commit hook (automatic rendering)

A Git pre-commit hook automatically re-renders all ADR files and regenerates the index whenever you commit changes to `architecture-decision-log/`. This means both the YAML source and its Markdown rendering are part of the same commit and PR — **reviewers approve both together**.

**One-time setup** (per clone):

```bash
git config core.hooksPath .githooks
```

After this, any commit that touches `architecture-decision-log/*.yaml` will automatically:
1. Render all ADR YAML files to `architecture-decision-log/rendered/*.md` with a provenance disclaimer
2. Regenerate [`architecture-decision-log/rendered/architecture-decision-log.md`](../architecture-decision-log/rendered/architecture-decision-log.md) (the decision log index)
3. Stage the rendered files alongside the YAML changes

The hook also regenerates `llms-full.txt` when any source documentation file changes (README, adr-process, glossary, schema reference, or ci-setup).

The hook is a local convenience, not the trust boundary. CI also regenerates and verifies the committed artifacts below without mutating the worktree:
- `architecture-decision-log/rendered/`
- `examples-reference/rendered/`
- `llms-full.txt`

The Repomix web-chat bundle (`adr-governance-bundle.md`) is intentionally different: it is an on-demand export artifact generated when needed, not a freshness-checked committed deliverable in this repository.

---

## Manual rendering

```bash
# Single file to stdout (no disclaimer — useful for previewing)
python3 scripts/render-adr.py architecture-decision-log/ADR-0001-*.yaml

# Render to architecture-decision-log/rendered/ with disclaimer + index
python3 scripts/render-adr.py --output-dir architecture-decision-log/rendered/ --generate-index architecture-decision-log/

# Render example ADRs
python3 scripts/render-adr.py --output-dir examples-reference/rendered/ --generate-index examples-reference/
```

Or use the Makefile:

```bash
make render
make llms-full
make generated
```

---

## Why two formats?

| Format | Audience | Purpose |
|--------|----------|---------|
| **YAML source** | AI agents, validators, CI pipelines | Machine-readable structured data — the authoritative source of truth |
| **Rendered Markdown** | Human reviewers, stakeholders, auditors | Readable, browsable format for GitHub/GitLab/Azure DevOps — auto-generated from YAML |

The YAML source is the single source of truth. The rendered Markdown is a *view* — always regenerated, never hand-edited. This separation ensures that the same decision record drives both automated governance (validation, compliance checking, AI context) and human comprehension (PR reviews, audit trails, stakeholder communication).
