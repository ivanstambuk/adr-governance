# Implementation Plan v2 — ADR Governance Deep Fixes

> **Created:** 2026-03-06
> **Status:** In Progress
> **Scope:** 28 issues identified from deep audit of schema, process, examples, skill, CI, and documentation

---

## Execution Tracker

| Phase | Description | Issues | Status |
|-------|-------------|--------|--------|
| 1 | Skill & Glossary Sync | #1, #2, #3, #4, #5, #6 | ⬜ Not started |
| 2 | Schema Hardening | #8, #10, #17, #21 | ⬜ Not started |
| 3 | Validator Enhancements | #9, #18, #20 | ⬜ Not started |
| 4 | Example ADRs | #7, #11, #27 | ⬜ Not started |
| 5 | Process Documentation | #15, #19, #25, #28 | ⬜ Not started |
| 6 | README & Directory Structure | #12, #16 | ⬜ Not started |
| 7 | CI & Tooling | #14, #22, #23 | ⬜ Not started |
| 8 | Final Verification | Validate all, commit | ⬜ Not started |

---

## Phase 1: Skill & Glossary Sync

Fix inconsistencies between the agent skill, its quick-reference glossary, the canonical glossary, SKILL.md, and the template.

### #1 — Fix GLOSSARY.md in skill: missing `draft` status
- **File:** `.skills/adr-author/references/GLOSSARY.md`
- **Action:** Add `draft` to the status values list
- **Line:** 7

### #2 — Remove phantom `data_classification` from skill GLOSSARY.md
- **File:** `.skills/adr-author/references/GLOSSARY.md`
- **Action:** Delete lines 19-20 (`## Data Classification` and its values)

### #3 — De-duplicate glossary: add note clarifying skill GLOSSARY.md is a subset
- **File:** `.skills/adr-author/references/GLOSSARY.md`
- **Action:** Ensure header note explicitly says "subset — see docs/glossary.md for full definitions"

### #4 — Align supersession instructions between SKILL.md and adr-process.md
- **File:** `.skills/adr-author/SKILL.md`
- **Action:** Update the "How to supersede an ADR" section to include **both** `lifecycle.supersedes` **and** `related_adrs` steps, matching adr-process.md §5

### #5 — Add `attachments.other` to template
- **File:** `.skills/adr-author/assets/adr-template.yaml`
- **Action:** Add `other: []` under `attachments` alongside `diagrams` and `runbooks`

### #6 — Clarify `adr.summary` vs `context.summary` distinction
- **File:** `.skills/adr-author/SKILL.md`
- **Action:** Add a note in Step 2 distinguishing the two summary fields:
  - `adr.summary` = executive elevator pitch (2-4 sentences, for stakeholder triage)
  - `context.summary` = narrative problem statement (detailed, for decision context)

**Commit message:** `fix(skill): sync glossary, align supersession, clarify summaries`

---

## Phase 2: Schema Hardening

Strengthen JSON Schema validation rules without breaking existing examples.

### #8 — Soften `chosen_alternative` description wording
- **File:** `schemas/adr.schema.json`
- **Action:** Change description from "must match" to "should match" with note that tooling-level validation enforces the cross-reference
- **Line:** ~320

### #10 — Add `deferred` event to `audit_trail` enum
- **File:** `schemas/adr.schema.json`
- **Action:** Add `"deferred"` to the `audit_trail.event` enum array (line ~622)
- **Also update:** `docs/glossary.md` audit trail events table, `.skills/adr-author/references/GLOSSARY.md`

### #17 — Add `minLength: 1` to pros/cons string items
- **File:** `schemas/adr.schema.json`
- **Action:** Add `"minLength": 1` to the string items in `alternatives[].pros` and `alternatives[].cons` arrays
- **Lines:** ~268-279
- **Note:** Template placeholders `""` will need to be updated to contain actual text or comments

### #21 — Document that risk/requirement IDs are ADR-scoped
- **File:** `schemas/adr.schema.json`
- **Action:** Update descriptions for risk ID and requirement ID patterns to note they are scoped per-ADR
- **Lines:** ~412, ~685

**Commit message:** `feat(schema): add deferred event, harden pros/cons, clarify ID scoping`

---

## Phase 3: Validator Enhancements

Add new semantic checks to the Python validation script.

### #9 — Add state transition validation
- **File:** `scripts/validate-adr.py`
- **Action:** Add a semantic check that warns if `audit_trail` events don't follow valid transitions:
  - Valid terminal events per status: accepted→approved, rejected→rejected, superseded→superseded, deprecated→deprecated
  - Warn if status is `draft` but `audit_trail` contains `approved`
  - Warn if status is `accepted` but no `approved` event exists (already done — extend)

### #18 — Add confidence ↔ review cycle consistency warning
- **File:** `scripts/validate-adr.py`
- **Action:** In strict mode, warn when:
  - `decision.confidence: "low"` but `lifecycle.review_cycle_months > 6`
  - `decision.confidence: "high"` but `lifecycle.review_cycle_months < 12`

### #20 — Add bidirectional relationship check
- **File:** `scripts/validate-adr.py`
- **Action:** In `validate_cross_references()`, check that `supersedes`/`superseded_by` relationships are symmetric:
  - If ADR-A says `supersedes ADR-B`, warn if ADR-B doesn't say `superseded_by ADR-A`
  - Same for `depends_on` (advisory warning only)

**Commit message:** `feat(validator): state transitions, confidence checks, bidirectional refs`

---

## Phase 4: Example ADRs

Fix existing examples and add lifecycle-demonstrating examples.

### #7 — Add `confirmation` to 3 example ADRs
- **Files:** `examples/ADR-0001-*.yaml`, `examples/ADR-0004-*.yaml`, `examples/ADR-0006-*.yaml`
- **Action:** Add realistic `confirmation` sections with `description` and `artifact_ids`

### #11 — Add a `rejected` example ADR (ADR-0007)
- **File:** `examples/ADR-0007-centralized-secret-store-for-api-keys.yaml` (new)
- **Action:** Create a new example ADR in `rejected` status with:
  - `rejection_rationale` on all non-chosen alternatives
  - `audit_trail` with `created` → `rejected` events
  - Demonstrates the rejection workflow

### #27 — Fix broken diagram reference in ADR-0001
- **File:** `examples/ADR-0001-*.yaml`
- **Action:** Either remove the `attachments.diagrams` reference to the non-existent file, or add a note that diagram paths are illustrative

**Commit message:** `feat(examples): add confirmation sections, rejected ADR, fix broken ref`

---

## Phase 5: Process Documentation

Fill gaps in the process document.

### #15 — Add archival workflow to adr-process.md
- **File:** `docs/adr-process.md`
- **Action:** Add a new section (§6.5 or new §7) documenting the archival workflow:
  - When to archive (superseded + no longer referenced, deprecated + confirmed replaced)
  - How to archive (set archival fields, add `archived` audit event)
  - Archival vs. deletion (never delete, only archive)

### #19 — Add schema versioning policy
- **File:** `docs/adr-process.md`
- **Action:** Add a new section documenting:
  - `schema_version` is pinned at ADR creation time
  - Existing ADRs are NOT updated when schema evolves
  - Backward compatibility policy: new schema versions should validate old ADRs
  - Migration path: only when adding required fields

### #25 — Cross-reference confirmation artifact guidance
- **File:** `docs/adr-process.md`
- **Action:** The artifact guidance table already exists in §7. Add a note in the schema description for `confirmation.artifact_ids` pointing to the process doc. Also reference it from SKILL.md.

### #28 — Add TL;DR quick reference at top of process doc
- **File:** `docs/adr-process.md`
- **Action:** Move or duplicate the Quick Reference table (currently §10) to the top of the document as a "Quick Reference" callout

**Commit message:** `docs(process): add archival workflow, versioning policy, quick reference`

---

## Phase 6: README & Directory Structure

### #12 — Consider adding meta-ADR (ADR-0000)
- **File:** `decisions/ADR-0000-adopt-governed-adr-process.yaml` (new, replacing `.gitkeep`)
- **Action:** Create a meta-ADR documenting the decision to use this governance process. Status: `accepted`. This populates the empty `decisions/` directory with a working example.

### #16 — Update README directory tree
- **File:** `README.md`
- **Action:** Add `adr-process.md` and `research/` to the directory structure listing. Add ADR-0007 to the examples table.

**Commit message:** `docs: add meta-ADR, update README directory tree`

---

## Phase 7: CI & Tooling

### #14 — Run `--strict` on examples in CI
- **File:** `.github/workflows/validate-adr.yml`
- **Action:** Change examples validation to use `--strict` flag (since examples should be best-practice references)

### #22 — Add CODEOWNERS.example
- **File:** `CODEOWNERS.example` (new)
- **Action:** Create an example CODEOWNERS file based on the recommendation in adr-process.md §9

### #23 — Review repomix config for research doc inclusion
- **File:** `repomix.config.json`
- **Action:** Add `docs/research/**` to the ignore list (research docs are ~100KB and not needed for LLM context of the core project)

**Commit message:** `fix(ci): strict examples, add CODEOWNERS.example, tune repomix`

---

## Phase 8: Final Verification

1. Run `python3 scripts/validate-adr.py --strict examples/` — expect 0 errors, 0 warnings
2. Run `python3 scripts/validate-adr.py --strict decisions/` — expect 0 errors, 0 warnings
3. Run `python3 scripts/validate-adr.py examples/ decisions/` — cross-reference check
4. Verify all git status clean
5. Delete this implementation plan
6. Final commit

**Commit message:** `chore: remove implementation plan after completion`

---

## Issues NOT Implemented (Deferred/Out of Scope)

| # | Issue | Reason |
|---|-------|--------|
| #13 | No CODEOWNERS file | Covered by #22 (CODEOWNERS.example instead — real CODEOWNERS depends on org) |
| #24 | ADR ID slug format docs | Current regex is fine; hyphen-separated slugs work. Low priority. |
| #26 | Requirement ID scoping docs | Covered by #21 (adding per-ADR scoping note to schema descriptions) |
