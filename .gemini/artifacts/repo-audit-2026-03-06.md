# ADR Governance — Repository Audit & Execution Tracker

> **Date:** 2026-03-06  
> **Auditor:** Antigravity  
> **Scope:** Full repository scan — schema, scripts, CI, docs, skills, examples, config, bundle  
> **Baseline:** Commit `02932a6` (latest on `main`)

---

## Summary

The repository is in **good shape** overall. The schema is solid, all 9 ADR YAML files pass validation with **0 errors and 0 warnings**, the CI pipelines are consistent across 5 platforms, and the documentation is comprehensive. However, the scan uncovered **24 findings** across 5 categories:

| Category | Critical | High | Medium | Low | Total |
|----------|:--------:|:----:|:------:|:---:|:-----:|
| Schema & Data Integrity | 1 | 2 | 2 | 1 | 6 |
| Documentation & Cross-Reference | 0 | 2 | 3 | 2 | 7 |
| Tooling & Scripts | 0 | 1 | 3 | 1 | 5 |
| CI/CD Pipelines | 0 | 0 | 2 | 1 | 3 |
| Developer Experience (DX) | 0 | 0 | 2 | 1 | 3 |

---

## Tier 1 — Critical & High Priority

### AUDIT-001 · CRITICAL · Schema: `archived` status missing from enum
- [ ] **Fixed**
- **File:** `schemas/adr.schema.json` (line 56–64)
- **Finding:** The `adr.status` enum lists 7 values: `draft`, `proposed`, `accepted`, `superseded`, `deprecated`, `rejected`, `deferred`. The `archived` status is **absent**, yet:
  - The glossary (`docs/glossary.md`) does NOT list `archived` in the status table either — consistent with schema, but...
  - The process doc (`docs/adr-process.md` §8) describes the archival workflow in detail — set `lifecycle.archival` fields + add `archived` audit event
  - The `audit_trail[].event` enum includes `archived`
  - The state diagram in README and adr-process.md does NOT include `archived` as a state
- **Assessment:** This is an intentional design choice (archival is tracked via `lifecycle.archival` fields + audit event, not via `adr.status`), but it is **under-documented and ambiguous**. The §8 Archival workflow says "Update the ADR YAML" with archival fields but never says "set `adr.status` to X". A user following §8 would wonder what status to set. Should `archived` be a status or not? If not, what status does an archived ADR have? (`superseded`? `deprecated`? — it should still have its pre-archival status).
- **Recommendation:** Add an explicit statement to §8 and the glossary clarifying that **archival is NOT a status value** — it's a metadata overlay. The ADR keeps its existing status (`superseded`, `deprecated`, etc.) and the `lifecycle.archival` fields mark it as archived. Alternatively, if `archived` IS meant to be a terminal status, add it to the schema enum and state diagram.

### AUDIT-002 · HIGH · Schema: `archived` state missing from state diagram
- [ ] **Fixed**
- **Files:** `README.md` (lines 46–65), `docs/adr-process.md` (lines 41–69)
- **Finding:** Both state diagrams show `superseded → [*]` and `deprecated → [*]` as terminal states. But section §8 describes an archival workflow that implies an `archived` state. The diagrams are inconsistent with the documentation.
- **Recommendation:** Either add `archived` transitions to the state diagram (`superseded → archived`, `deprecated → archived`, `rejected → archived`) or add a note below the diagram explaining that archival is not a status transition but a metadata annotation.

### AUDIT-003 · HIGH · Data: ADR-0000 has inconsistent email addresses
- [ ] **Fixed**
- **File:** `architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml`
- **Finding:** The `authors[0].email` is `ivan@example.com` while `decision_owner.email` is `ivan.stambuk@novatrust.example.com`. The NovaTrust reference was supposed to be fictional (removed in commit `4f4e1c7`), yet the decision owner still references it. Additionally, the email inconsistency between author and decision owner (same person) is a data quality issue.
- **Recommendation:** Normalize both emails to the same value (either both `ivan@example.com` or a real one), and specifically remove the `novatrust.example.com` reference from the decision owner.

### AUDIT-004 · HIGH · Docs: `repomix-instruction.md` ID format regex is wrong
- [ ] **Fixed**
- **File:** `repomix-instruction.md` (line 294)
- **Finding:** The quick-reference says `ADR-NNNN` or `ADR-NNNN-slug` with the note that slug is optional: `^ADR-[0-9]{4}(-[a-z0-9]+)*$`. However, the actual schema in `adr.schema.json` (line 41) uses `^ADR-[0-9]{4}(-[a-z0-9]+)+$` (note: **`+`** not `*`), making the slug **mandatory** (at least one slug segment is required). The repomix instruction incorrectly tells the AI that `ADR-0001` alone (without slug) is valid, when the schema would reject it.
- **Recommendation:** Fix the regex in `repomix-instruction.md` line 294 to match the actual schema: `ADR-NNNN-slug` (slug is mandatory). Change the example from `ADR-0001` to `ADR-0001-dpop-over-mtls`.

### AUDIT-005 · HIGH · CI: `.yamllint.yml` exists but is not used by any CI pipeline
- [ ] **Fixed**
- **Files:** `.yamllint.yml`, `.github/workflows/validate-adr.yml`, `ci/azure-devops/azure-pipelines.yml`, `ci/gitlab-ci/.gitlab-ci.yml`, `ci/aws-codebuild/buildspec.yml`, `ci/gcp-cloud-build/cloudbuild.yaml`
- **Finding:** The repository has a root-level `.yamllint.yml` configuration file, and `CONTRIBUTING.md` instructs contributors to run `yamllint -c .yamllint.yml`. However, **no CI pipeline uses it**. Each pipeline inlines its own yamllint config (either via `config_data` in GitHub Actions or via a heredoc creating `/tmp/yamllint-config.yml`). The configs are functionally identical but the duplication means:
  1. If someone changes `.yamllint.yml`, CI behavior doesn't change
  2. If someone changes a CI pipeline's inline config, `.yamllint.yml` drifts
- **Recommendation:** Refactor all CI pipelines to use `yamllint -c .yamllint.yml` instead of inline configs. This makes `.yamllint.yml` the single source of truth.

---

## Tier 2 — Medium Priority

### AUDIT-006 · MEDIUM · Schema: No `archived` status but `lifecycle.archival` exists
- [ ] **Fixed**
- **Related to:** AUDIT-001
- **Finding:** The schema defines `lifecycle.archival.archived_at` and `lifecycle.archival.archive_reason` fields, plus an `archived` audit trail event — but no `archived` status. The validator (`validate-adr.py`) does not check for archival consistency either (e.g., if `lifecycle.archival.archived_at` is set, the status should arguably be terminal). This means an ADR with status `proposed` could have archival fields set without triggering any validation error.
- **Recommendation:** Add a validator check: if `lifecycle.archival.archived_at` is not null, warn if `adr.status` is not in `{superseded, deprecated, rejected}`. Document the constraint.

### AUDIT-007 · MEDIUM · Schema: `adr.summary` is optional but should arguably be required for `proposed`+ ADRs
- [ ] **Fixed**
- **Finding:** The schema makes `adr.summary` optional (no presence in `required` array). The validator warns when it's missing on `proposed`/`accepted` ADRs, but it's only a warning, not an error. The field is described as an "executive elevator pitch" and is essential for stakeholder triage — a core use case.
- **Recommendation:** Consider making `adr.summary` required in the next schema version. For now, the warning is appropriate, but document this as a planned v1.1 change.

### AUDIT-008 · MEDIUM · Docs: Glossary missing `archived` from status table
- [ ] **Fixed**
- **Related to:** AUDIT-001
- **File:** `docs/glossary.md` (lines 20–30)
- **Finding:** The glossary's "ADR Status Values" table has 7 entries (same as schema). This is consistent with the schema, but inconsistent with section §8 of `adr-process.md` which describes archival as a workflow. If archival is not a status, the glossary should have an explicit note explaining this.
- **Recommendation:** Add a note under the status table: `> Archival is not a status value — it is a metadata overlay tracked via lifecycle.archival fields. Archived ADRs retain their pre-archival status (superseded, deprecated, rejected).`

### AUDIT-009 · MEDIUM · Docs: `CONTRIBUTING.md` references `assets/adr-template.yaml`
- [ ] **Fixed**
- **File:** `CONTRIBUTING.md` (line 38)
- **Finding:** Line 38 says: "**ADR template** (`assets/adr-template.yaml`) must stay in sync with the schema." The actual template path is `.skills/adr-author/assets/adr-template.yaml`. The `assets/` reference is ambiguous and might confuse a contributor who doesn't know the full directory structure.
- **Recommendation:** Update to the full relative path: `.skills/adr-author/assets/adr-template.yaml`.

### AUDIT-010 · MEDIUM · Docs: `CONTRIBUTING.md` references `SCHEMA_REFERENCE.md` without path
- [ ] **Fixed**
- **File:** `CONTRIBUTING.md` (line 39)
- **Finding:** Line 39 says: "**Glossary and SCHEMA_REFERENCE.md** must reflect any enum or field changes." The SCHEMA_REFERENCE is at `.skills/adr-author/references/SCHEMA_REFERENCE.md`. There are TWO glossary files: `docs/glossary.md` (full) and `.skills/adr-author/references/GLOSSARY.md` (subset). This line doesn't specify which glossary, nor the paths.
- **Recommendation:** Update to: "**Glossary** (`docs/glossary.md` + `.skills/adr-author/references/GLOSSARY.md`) and **Schema Reference** (`.skills/adr-author/references/SCHEMA_REFERENCE.md`) must reflect any enum or field changes."

### AUDIT-011 · ~~MEDIUM~~ VERIFIED OK · Scripts: `review-adr.py` — no stale field references
- [x] **Verified OK** — No references to `risk_assessment`, `related_adrs`, or `attachments` found in any script.
- **File:** `scripts/review-adr.py`
- **Finding:** Confirmed clean. No stale references to removed schema fields.
- **Status:** No action needed.

### AUDIT-012 · MEDIUM · CI: GitHub Actions workflow doesn't use `requirements.txt`
- [ ] **Fixed**
- **File:** `.github/workflows/validate-adr.yml` (line 37)
- **Finding:** The workflow runs `pip install jsonschema pyyaml yamllint` directly, rather than `pip install -r requirements.txt`. This creates a divergence risk: if `requirements.txt` is updated (e.g., minimum version bumps), CI won't pick up the change.
- **Recommendation:** Change to `pip install -r requirements.txt` in all CI pipelines. The `requirements.txt` already exists with pinned minimum versions.

### AUDIT-013 · ~~MEDIUM~~ VERIFIED OK · Scripts: `render-adr.py` handles `confirmation` correctly
- [x] **Verified OK** — `render-adr.py` lines 214–223 properly render `confirmation.description` and `confirmation.artifact_ids`.
- **File:** `scripts/render-adr.py`
- **Finding:** Confirmed correct. Both description and artifact IDs are rendered.
- **Status:** No action needed.

### AUDIT-014 · ~~MEDIUM~~ VERIFIED OK · DX: `.gitignore` correctly ignores bundle
- [x] **Verified OK** — `git ls-files adr-governance-bundle.md` returns empty; file is not tracked.
- **File:** `.gitignore` (line 26)
- **Finding:** The bundle is correctly gitignored and not tracked in git history.
- **Status:** No action needed.

### AUDIT-015 · MEDIUM · DX: No `Makefile` or task runner for common operations
- [ ] **Fixed**
- **Finding:** The README and docs reference many multi-step commands (validate, lint, render, bundle, install deps). There's no `Makefile`, `justfile`, or `package.json` scripts to simplify these. Contributors must copy commands from docs.
- **Recommendation:** Add a simple `Makefile` with targets: `install`, `validate`, `lint`, `render`, `bundle`, `review`, `summarize`, `all`. This is a quality-of-life improvement, not critical.

---

## Tier 3 — Low Priority

### AUDIT-016 · LOW · Schema: `version` field comment says "not to be confused with schema_version" but no guidance when to bump
- [ ] **Fixed**
- **File:** `schemas/adr.schema.json` (line 81)
- **Finding:** The `adr.version` field uses MAJOR.MINOR pattern (`^[0-9]+\.[0-9]+$`). While the schema versioning policy (§10 in adr-process.md) covers `schema_version`, there is no documented policy for when to bump `adr.version` — when the ADR document itself changes.
- **Recommendation:** Add guidance to §10 or a new subsection specifying when to bump `adr.version` (e.g., MAJOR for substantive changes, MINOR for maintenance).

### AUDIT-017 · LOW · Data: ADR-0000 references "7 example ADRs" but there are 8
- [ ] **Fixed**
- **File:** `architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml` (lines 139, 167)
- **Finding:** The confirmation section says "7 example ADRs (ADR-0001 through ADR-0007)" and the audit trail says "7 example ADRs". However, there are 8 example ADRs (ADR-0001 through ADR-0008, including the deferred OpenID Federation one). ADR-0008 was presumably added after the initial bootstrap.
- **Recommendation:** Update references from 7 to 8 and include ADR-0008 in the range: "8 example ADRs (ADR-0001 through ADR-0008)".

### AUDIT-018 · LOW · Docs: Skill GLOSSARY.md is a barely-valuable subset
- [ ] **Fixed**  
- **File:** `.skills/adr-author/references/GLOSSARY.md`
- **Finding:** This file is a 32-line subset of `docs/glossary.md` containing only enum values — information that's already fully documented in `SCHEMA_REFERENCE.md` (also in the skill references). It adds maintenance burden (two files to update when enums change) without adding value.
- **Recommendation:** Either delete `GLOSSARY.md` and point agents to the full glossary, or accept the duplication as intentional (for agents with limited context window).

### AUDIT-019 · LOW · CI: GCP Cloud Build pip installs don't persist across steps
- [ ] **Fixed**
- **File:** `ci/gcp-cloud-build/cloudbuild.yaml`
- **Finding:** Each Cloud Build step uses a fresh `python:3.12-slim` container. The `install-deps` step (step 1) installs packages with `--user`, but the PATH export `$$HOME/.local/bin` in subsequent steps may or may not work depending on HOME being the same across steps. Cloud Build mounts `/workspace` as shared volume, but `~/.local` might not persist.
- **Recommendation:** Test the GCP pipeline. If packages don't persist, install in `/workspace/.local` instead or combine install + validate into a single step. Alternatively, use `pip install --target /workspace/pylibs` and set `PYTHONPATH`.

### AUDIT-020 · LOW · Docs: Research directory still has stale comparison matrix
- [ ] **Fixed**
- **File:** `docs/research/adr-template-comparison.md` (71 KB)
- **Finding:** This large research file (71 KB) was generated during the initial schema design phase. It may contain stale comparisons against features that were subsequently adopted or rejected. It's excluded from the repomix bundle (correct), but it's still in the repo.
- **Recommendation:** Either mark it with a clear "HISTORICAL — may be outdated" header, or review and update it, or move it to a `docs/research/archive/` subdirectory.

### AUDIT-021 · LOW · DX: `repomix.config.json` ignores `summarize-adr.py` but includes `review-adr.py`
- [ ] **Fixed**
- **File:** `repomix.config.json`
- **Finding:** The bundle includes `scripts/**` but explicitly ignores several scripts: `verify-approvals.py`, `render-adr.py`, `extract-decisions.py`, `bundle.sh`. However, `review-adr.py`, `summarize-adr.py`, and `validate-adr.py` are included. This is reasonable (include the scripts that AI chats can reference as logic), but `summarize-adr.py` is debatable — a web chat can summarize without knowing the script's implementation.
- **Recommendation:** No action required. The inclusion is reasonable for reference. Note for future token optimization if the bundle grows too large.

### AUDIT-022 · LOW · Schema: `confirmation.artifact_ids` allows empty strings
- [ ] **Fixed**
- **File:** `schemas/adr.schema.json` (lines 389–394)
- **Finding:** The `artifact_ids` array items are `type: string` with no `minLength`. An ADR could pass validation with `artifact_ids: ["", ""]`. The template also starts with `artifact_ids: [""]`.
- **Recommendation:** Add `minLength: 1` to `artifact_ids` items. Also update the template to use `artifact_ids: []` instead of `artifact_ids: [""]`.

### AUDIT-023 · LOW · Docs: `web-chat-quickstart.md` says "~80K tokens" 
- [ ] **Fixed**
- **File:** `docs/web-chat-quickstart.md` (line 33)
- **Finding:** The file says the bundle is "~350 KB, ~80K tokens". Since the bundle is rebuilt every time, these numbers are stale. The actual bundle file is 185 KB (per list_dir), but it may have been larger before exclusion improvements.
- **Recommendation:** Either remove the hardcoded numbers or update them. Better: have `bundle.sh` print the actual token estimate (chars/4 is a rough approximation).

### AUDIT-024 · LOW · DX: `llms.txt` follows an emerging standard but no link to spec
- [ ] **Fixed**
- **File:** `llms.txt`
- **Finding:** The `llms.txt` file follows the emerging `llms.txt` convention for providing LLM-friendly project summaries. However, there's no reference to this convention in README or docs — a user might not understand what this file is for.
- **Recommendation:** Add a brief mention in README or CONTRIBUTING: "The `llms.txt` file follows the [llms.txt convention](https://llmstxt.org/) to provide a machine-readable project summary for AI assistants."

---

## Execution Progress

| Status | Emoji | Meaning |
|--------|:-----:|---------|
| Pending | ⬜ | Not started |
| In Progress | 🔄 | Work in progress |
| Done | ✅ | Completed and verified |
| Skipped | ⏭️ | Intentionally deferred |

### Execution Order (recommended)

**Phase 1 — Data/Schema correctness (blocks everything else)**
1. ⬜ AUDIT-001 — Clarify `archived` status design decision
2. ⬜ AUDIT-002 — Fix state diagrams
3. ⬜ AUDIT-003 — Fix ADR-0000 email inconsistency
4. ⬜ AUDIT-004 — Fix repomix-instruction ID regex

**Phase 2 — CI/DX quick wins**
5. ⬜ AUDIT-005 — Centralize yamllint config
6. ⬜ AUDIT-012 — Use requirements.txt in CI
7. ⬜ AUDIT-017 — Update ADR-0000 example count

**Phase 3 — Documentation alignment**
8. ⬜ AUDIT-008 — Glossary archival clarification
9. ⬜ AUDIT-009 — Fix CONTRIBUTING.md template path
10. ⬜ AUDIT-010 — Fix CONTRIBUTING.md glossary/schema ref paths
11. ⬜ AUDIT-011 — Verify review-adr.py for stale field refs

**Phase 4 — Validator/tooling improvements**
12. ⬜ AUDIT-006 — Add archival consistency check to validator
13. ⬜ AUDIT-013 — Verify confirmation rendering
14. ⬜ AUDIT-022 — Add minLength to artifact_ids

**Phase 5 — Polish (optional)**
15. ⬜ AUDIT-007 — Document planned `adr.summary` required change
16. ⬜ AUDIT-014 — Verify bundle not tracked in git
17. ⬜ AUDIT-015 — Add Makefile
18. ⬜ AUDIT-016 — Document adr.version bump policy
19. ⬜ AUDIT-018 — Evaluate GLOSSARY.md redundancy
20. ⬜ AUDIT-019 — Test GCP Cloud Build pip persistence
21. ⬜ AUDIT-020 — Mark research docs as historical
22. ⬜ AUDIT-021 — No action (informational)
23. ⬜ AUDIT-023 — Fix token estimate in quickstart
24. ⬜ AUDIT-024 — Add llms.txt explanation

---

## Files Not Scanned (out of scope)

- `adr-governance-bundle.md` — auto-generated, not source of truth
- `rendered/**` — auto-generated from YAML sources
- `examples-reference/rendered/**` — auto-generated from YAML sources
- `.git/**` — git internals
- `docs/research/adr-template-comparison.md` — 72 KB research doc (flagged in AUDIT-020 but not line-by-line audited)
- `docs/research/adr-governance-process-comparison.md` — 33 KB research doc
- `docs/research/web-chat-adr-authoring.md` — 4 KB research doc
