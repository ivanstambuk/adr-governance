# ADR Governance Repo — Comprehensive Audit Report

> **Date:** 2026-03-06  
> **Scope:** Full repository scan — schema, docs, scripts, CI, skill, examples, bundle, rendered output  
> **Total findings:** 27

---

## Execution Tracker

| # | Priority | Category | Finding | Status |
|---|:--------:|----------|---------|:------:|
| 1 | 🔴 P1 | Bug | GitHub Actions step name typo: "Validate examples-reference-reference/" | ⬜ TODO |
| 2 | 🔴 P1 | Bug | ADR-0000 uses fictional NovaTrust identity — should use real data | ⬜ TODO |
| 3 | 🔴 P1 | Inconsistency | `schema_version: 1.0.0` unquoted in 8 ADRs — YAML parses as float in some parsers | ⬜ TODO |
| 4 | 🟠 P2 | Gap | `examples-reference/` not included in `repomix.config.json` `include` array | ⬜ TODO |
| 5 | 🟠 P2 | Gap | GitHub Actions does NOT install `yamllint` via pip — uses external action but verify-approvals needs pyyaml only | ⬜ TODO |
| 6 | 🟠 P2 | Inconsistency | Review checklist (§3.3 #10) references "Risk assessment" but `risk_assessment` section was removed from schema | ⬜ TODO |
| 7 | 🟠 P2 | Inconsistency | Glossary lists `R-NNN` Risk ID format but schema has no Risk entity — stale reference | ⬜ TODO |
| 8 | 🟠 P2 | Gap | `ci-setup.md` identity example comment says "GitHub username (without @)" but the YAML shows `@janedoe` with @ | ⬜ TODO |
| 9 | ~~🟠 P2~~ | ~~Gap~~ | ~~`verify-approvals.py` does not skip `deferred` status~~ — **FALSE POSITIVE.** Line 533: `if status not in ("proposed", "accepted")` correctly skips deferred | ✅ VERIFIED OK |
| 10 | 🟠 P2 | Gap | No `requirements.txt` or `pyproject.toml` — Python dependencies not pinned | ⬜ TODO |
| 11 | 🟠 P2 | Gap | `repomix.config.json` excludes `examples-reference/*.yaml` from bundle — users lose reference examples | ⬜ TODO |
| 12 | 🟠 P2 | Under-spec | Azure DevOps pipeline uses `$(System.PullRequest.PullRequestId)` inside `$()` bash — syntax mismatch | ⬜ TODO |
| 13 | 🟡 P3 | Inconsistency | ADR-0000 `context.summary` still references "NovaTrust" in the production ADR log | ⬜ TODO |
| 14 | 🟡 P3 | Gap | No `.yamllint` config file in repo root — each pipeline creates its own inline config | ⬜ TODO |
| 15 | 🟡 P3 | Gap | SKILL.md references `references/GLOSSARY.md` which only exists as a partial file — no link to actual glossary | ⬜ TODO |
| 16 | 🟡 P3 | Improvement | SCHEMA_REFERENCE.md is minimal (39 lines) — doesn't cover extension fields, markdown-native fields list, or enum values | ⬜ TODO |
| 17 | 🟡 P3 | Gap | `docs/research/adr-governance-process-comparison.md` is modified (dirty in git) but never committed | ⬜ TODO |
| 18 | 🟡 P3 | Inconsistency | README Quick Start §3.1 says `cp examples-reference/ADR-0001-*.yaml` as template but main README §8 says `cp .skills/adr-author/assets/adr-template.yaml` | ⬜ TODO |
| 19 | 🟡 P3 | Gap | Pre-commit hook only renders `architecture-decision-log/` — doesn't render `examples-reference/` changes | ⬜ TODO |
| 20 | 🟡 P3 | Gap | No `CONTRIBUTING.md` — open-source repo has no contribution guide | ⬜ TODO |
| 21 | 🟡 P3 | Improvement | Bundle (`adr-governance-bundle.md`) committed to repo — 185KB tracked by git; should be in `.gitignore` | ⬜ TODO |
| 22 | 🟡 P3 | Improvement | `web-chat-adr-authoring.md` is a design notes doc (63 lines) that duplicates info already in quickstart — candidate for removal | ⬜ TODO |
| 23 | 🟡 P3 | Gap | CI pipelines (Azure, GCP, AWS) don't include `verify-approvals.py` in path triggers | ⬜ TODO |
| 24 | 🟢 P4 | Improvement | `scripts/__pycache__/` directory exists — should be cleaned up | ⬜ TODO |
| 25 | 🟢 P4 | Improvement | `llms.txt` links are all absolute GitHub URLs — will 404 until repo is public | ⬜ TODO |
| 26 | 🟢 P4 | Inconsistency | `adr-process.md` §3.1 says to copy from `examples-reference/ADR-0001-*` as the authoring starting point; `SKILL.md` says `assets/adr-template.yaml` | ⬜ TODO |
| 27 | 🟢 P4 | Improvement | Rendered examples index uses relative link `../architecture-decision-log/` but main ADL rendered index uses the same — both work but no consistency with `../examples-reference/` | ⬜ TODO |

---

## Detailed Findings

---

### Finding 1 — 🔴 P1 | Bug
#### GitHub Actions step name typo

**File:** `.github/workflows/validate-adr.yml` line 47  
**Issue:** The step name is `"Validate examples-reference-reference/"` — doubled suffix.  
**Impact:** Confusing CI output. Cosmetic but erodes trust in the CI setup that the README markets as "ready to use out of the box."  
**Fix:** Rename to `"Validate examples-reference/"`.

---

### Finding 2 — 🔴 P1 | Bug
#### ADR-0000 uses fictional NovaTrust identity

**File:** `architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml`  
**Issue:**
- `authors[0].email`: `ivan.stambuk@novatrust.example.com` — NovaTrust is the *fictional* company from the examples
- `decision_owner.email`: same fictional email
- `context.summary` starts with *"NovaTrust's architecture team..."*

ADR-0000 is the **real** meta-ADR in the production `architecture-decision-log/`. It should not reference the fictional NovaTrust company — that's only for `examples-reference/`.

**Impact:** Confusing for adopters. The README says "Update it for your organization" but the bootstrap ADR looks like a fiction example.  
**Fix:** Either:
- Replace NovaTrust references with generic/real data, or
- Add a clear `# TODO: Customize for your organization` comment

---

### Finding 3 — 🔴 P1 | Inconsistency
#### `schema_version` unquoted in YAML files

**Files:** All 8 example ADRs + ADR-0000  
**Issue:** `schema_version: 1.0.0` is written without quotes. YAML 1.1 parsers may interpret `1.0.0` as a string, but the inconsistency with `schema_version: "1.0.0"` (used in ADR-0001) is a latent parsing risk. The schema requires pattern `^[0-9]+\.[0-9]+\.[0-9]+$` — if any parser coerces `1.0.0` to float `1.0`, it would fail validation.  
**Impact:** Currently passes because PyYAML treats `1.0.0` as string. Could break with other parsers or YAML 1.2 strict mode.  
**Fix:** Quote all `schema_version` values: `schema_version: "1.0.0"`. Also update the template.

---

### Finding 4 — 🟠 P2 | Gap
#### Example ADR YAML files excluded from bundle

**File:** `repomix.config.json`  
**Issue:** The `include` array does NOT list `examples-reference/**`. The `ignore.customPatterns` excludes `examples-reference/rendered/**` and `examples-reference/README.md`, which implies the YAML files *should* be included. But since `include` is a whitelist and `examples-reference/**` isn't in it, **none of the example YAMLs make it into the bundle**.

The `web-chat-adr-authoring.md` design doc says "Example ADRs | examples-reference/*.yaml" is in the bundle. The README says the bundle includes "example ADRs from examples-reference/."

**Impact:** Web chat users don't get the reference examples. AI can't cite them. Major gap between documented and actual behavior.  
**Fix:** Add `"examples-reference/**"` to the `include` array.

---

### Finding 5 — 🟠 P2 | Gap
#### GitHub Actions doesn't pip-install `yamllint`

**File:** `.github/workflows/validate-adr.yml` line 37  
**Issue:** The install step runs `pip install jsonschema pyyaml` — it does **not** install `yamllint`. The YAML lint step uses the external `ibiqlik/action-yamllint@v3` action instead. This is fine for GitHub Actions, but documentation in `ci-setup.md` (line 31) says "pip packages: jsonschema, pyyaml (for validation), yamllint (for linting)." This creates confusion about whether yamllint is a pip dependency or an action dependency.

Meanwhile, all other CI pipelines (Azure, GCP, AWS, GitLab) DO install yamllint via pip.

**Impact:** Minor confusion. Not a functional bug — but inconsistent mental model.  
**Fix:** Either add `yamllint` to the pip install in GitHub Actions, or clarify in docs that GitHub uses a dedicated action.

---

### Finding 6 — 🟠 P2 | Inconsistency
#### Review checklist references removed `risk_assessment` section

**File:** `docs/adr-process.md` line 158  
**Issue:** The review checklist item says: *"Risk assessment covers realistic failure modes"*. But the `risk_assessment` section was **removed** from the schema (documented in `docs/research/adr-template-comparison.md` §7.4: "Removed in v1.1"). The schema has no `risk_assessment` field.

The skill's SKILL.md review checklist does NOT mention risk assessment (correct), so there's a gap between the two review checklists.

**Impact:** Reviewer confusion — they'll look for a section that doesn't exist in the schema.  
**Fix:** Rephrase to: "Risks are addressed via `alternatives[].risk`, pros/cons, and `consequences.negative`" or similar.

---

### Finding 7 — 🟠 P2 | Inconsistency
#### Glossary lists `R-NNN` Risk ID format with no corresponding schema entity

**File:** `docs/glossary.md` line 79  
**Issue:** The glossary lists `Risk | R-NNN | R-001` under ID Formats. But the schema has no `risk` entity with an `id` field. The `risk_assessment` section (which used `R-NNN` IDs) was removed. The remaining `risk` in the schema is just a string enum (`low/medium/high/critical`) on alternatives.

**Impact:** Users will try to use R-NNN IDs that have no home in the schema.  
**Fix:** Remove the Risk row from the glossary's ID Formats table.

---

### Finding 8 — 🟠 P2 | Inconsistency
#### `ci-setup.md` identity format contradiction

**File:** `docs/ci-setup.md` lines 417  
**Issue:** A YAML code example comment says `# GitHub username (without @)` but the actual value in the YAML is `identity: "@janedoe"` — **with** the `@` prefix. The `adr-process.md` consistently uses `@janedoe` *with* `@`. The schema description says "e.g., '@janedoe'."

**Impact:** Users unsure whether to include `@` or not. Verify-approvals.py normalizes the `@` prefix away, but the documentation should be consistent.  
**Fix:** Remove the misleading `(without @)` comment.

---

### Finding 9 — 🟠 P2 | Gap
#### `verify-approvals.py` doesn't explicitly handle `deferred` status

**File:** `scripts/verify-approvals.py`  
**Issue:** The `ci-setup.md` documentation (line 467) says: "ADRs in `draft`, `rejected`, `deferred`, or `superseded` status are **skipped**." But searching verify-approvals.py for "deferred" returns no results. Need to verify the actual status-filtering logic.

**Impact:** May incorrectly attempt to verify approvals on deferred ADRs.  
**Fix:** Verify and ensure the script skips deferred status. Add explicit handling if missing.

---

### Finding 10 — 🟠 P2 | Gap
#### No Python dependency management file

**Files:** Missing `requirements.txt`, `pyproject.toml`, or `setup.py`  
**Issue:** Python dependencies (`jsonschema`, `pyyaml`, `yamllint`) are only mentioned in CI pipeline files and README install commands. There's no standard Python dependency file.

**Impact:** Makes it harder for adopters to install dependencies, doesn't pin versions, and prevents container/virtualenv reproducibility.  
**Fix:** Add a `requirements.txt` with pinned versions:
```
jsonschema>=4.20
pyyaml>=6.0
yamllint>=1.33
```

---

### Finding 11 — 🟠 P2 | Gap
#### Example YAML files missing from bundle (duplicate of #4 — different angle)

**File:** `repomix.config.json`  
**Issue:** Cross-referencing Finding #4: The `repomix-instruction.md` embedded in the bundle tells the AI to "Search this bundle first for related context: existing ADRs, glossary terms, dependencies. Reference what you find." But if examples aren't in the bundle, the AI has no high-quality reference samples to learn from.

The `web-chat-adr-authoring.md` design doc explicitly lists "Example ADRs | examples-reference/*.yaml" as bundle content.

**Impact:** Same as #4. Covered here for completeness of the design gap.  
**Fix:** Same as #4.

---

### Finding 12 — 🟠 P2 | Under-spec
#### Azure DevOps pipeline shell syntax issue

**File:** `ci/azure-devops/azure-pipelines.yml` line 95  
**Issue:** The verify-approvals step uses:
```bash
if [ -n "$(System.PullRequest.PullRequestId)" ]; then
```
In Azure DevOps YAML, `$(System.PullRequest.PullRequestId)` is a pipeline macro expanded at compile time. But inside a `script:` block (bash), `$(...)` is also shell command substitution syntax. If Azure expands it first, fine. If the variable is empty/undefined, bash may try to execute `System.PullRequest.PullRequestId` as a command.

**Impact:** Potential false-positive skip of approval verification.  
**Fix:** Use `$SYSTEM_PULLREQUEST_PULLREQUESTID` (env var) or wrap in proper Azure pipeline condition: `condition: eq(variables['Build.Reason'], 'PullRequest')`.

---

### Finding 13 — 🟡 P3 | Inconsistency
#### ADR-0000 content still references NovaTrust (overlaps with #2 detail)

**File:** `architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml` line 37  
**Issue:** The `context.summary` reads: *"NovaTrust's architecture team makes dozens of significant decisions..."* — this blurs the line between the real governance ADR and the fictional examples.

**Impact:** Adopters may think the entire repo is a demo, not a real framework.  
**Fix:** Generalize: "Your architecture team makes..." or remove NovaTrust.

---

### Finding 14 — 🟡 P3 | Gap
#### No shared `.yamllint` config file

**Issue:** Every CI pipeline creates an inline yamllint config (`/tmp/yamllint-config.yml`) with the same settings (max line length 300, truthy check-keys false). The pre-commit hook doesn't lint at all.

**Impact:** Config duplication across 5 pipelines. If settings need to change, 4-5 files must be updated.  
**Fix:** Create `.yamllint.yml` at repo root with the shared config. Update all pipelines to use it.

---

### Finding 15 — 🟡 P3 | Gap
#### SKILL.md `references/GLOSSARY.md` doesn't exist as a standalone useful doc

**File:** `.skills/adr-author/references/GLOSSARY.md`  
**Issue:** The SKILL.md line 139 references `../../docs/glossary.md`. The `references/` directory has `GLOSSARY.md` but it's not clear if this is a copy or a symlink. Let me check...

Actually, the `references/` directory contains `GLOSSARY.md` and `SCHEMA_REFERENCE.md`. The SKILL.md points to `../../docs/glossary.md` directly. But the skill is portable — if copied to another repo as recommended (README §7), those relative links break.

**Impact:** When the skill is copied to a code repo, the `../../docs/glossary.md` link won't resolve.  
**Fix:** Either make the references self-contained within the skill, or document that the skill needs the full framework repo context.

---

### Finding 16 — 🟡 P3 | Improvement
#### SCHEMA_REFERENCE.md is under-specified

**File:** `.skills/adr-author/references/SCHEMA_REFERENCE.md` (39 lines)  
**Issue:** Only lists section names and a few key rules. Does not document:
- Extension fields (`x-` prefix)
- Markdown-native fields list
- All enum values (status, decision_type, priority, confidence, risk, cost)
- Person schema (`$defs/person`)
- Approval identity semantics

**Impact:** AI agents using the skill without the full schema.json have insufficient context.  
**Fix:** Expand to include all enum values, field constraints, and markdown-native field list.

---

### Finding 17 — 🟡 P3 | Gap
#### Uncommitted changes in research docs

**File:** `docs/research/adr-governance-process-comparison.md`  
**Issue:** `git status --short` shows this file as modified but uncommitted.

**Impact:** Changes may be lost; dirty working tree.  
**Fix:** Commit or stash the changes.

---

### Finding 18 — 🟡 P3 | Inconsistency
#### Two different "create your first ADR" instructions

**Files:** `docs/adr-process.md` §3.1 vs `README.md` §8  
**Issue:**
- `adr-process.md` says: `cp examples-reference/ADR-0001-*.yaml architecture-decision-log/ADR-NNNN-short-title.yaml`
- `README.md` says: `cp .skills/adr-author/assets/adr-template.yaml architecture-decision-log/ADR-0001-your-decision-title.yaml`

Both are valid approaches but they give conflicting guidance. One uses a full example as a starting point, the other uses a blank template.

**Impact:** Users get different instructions depending on which doc they read first.  
**Fix:** Standardize on the template approach (it's cleaner). Update adr-process.md to reference the template file.

---

### Finding 19 — 🟡 P3 | Gap
#### Pre-commit hook doesn't render example changes

**File:** `.githooks/pre-commit`  
**Issue:** The hook only watches `architecture-decision-log/*.yaml`. If someone modifies an ADR in `examples-reference/`, the rendered examples are not regenerated.

**Impact:** `examples-reference/rendered/` files can drift out of sync with the source YAML.  
**Fix:** Optionally extend the hook to also watch `examples-reference/`. Or document this as intentional.

---

### Finding 20 — 🟡 P3 | Gap
#### No `CONTRIBUTING.md`

**Issue:** The repo is MIT-licensed and pushed to GitHub, but has no contribution guide explaining how to submit issues, PRs, or what the review process is for the framework itself (as opposed to ADRs within the framework).

**Impact:** Open-source contributors don't know how to contribute.  
**Fix:** Add a `CONTRIBUTING.md` covering: issue reporting, PR process for framework changes, code style (Python), and testing expectations.

---

### Finding 21 — 🟡 P3 | Improvement
#### Bundle file committed to Git

**File:** `adr-governance-bundle.md` (185 KB)  
**Issue:** The generated bundle is committed to the repository. It's a derived artifact (~185 KB) that should be regenerated on demand. It inflates the repo and can cause merge conflicts.

The `.gitignore` does NOT exclude it. The `repomix.config.json` ignore patterns exclude the bundle from being *included inside itself*, but not from Git.

**Impact:** Unnecessary large file in git history. Re-bundling creates noisy diffs.  
**Fix:** Add `adr-governance-bundle.md` to `.gitignore` and remove from tracked files. Add a CI step or GitHub Release to publish the bundle as an artifact.

---

### Finding 22 — 🟡 P3 | Improvement
#### `web-chat-adr-authoring.md` is redundant

**File:** `docs/web-chat-adr-authoring.md` (63 lines)  
**Issue:** This is a design notes document that largely duplicates information in `docs/web-chat-quickstart.md` and `repomix-instruction.md`. It documents platform capabilities and deliverables that are now implemented.

**Impact:** Maintenance burden; potential for information drift.  
**Fix:** Merge any unique content into `web-chat-quickstart.md`, then delete or move to `docs/research/`.

---

### Finding 23 — 🟡 P3 | Gap
#### Non-GitHub CI pipelines missing `verify-approvals.py` in path triggers

**Files:** `ci/azure-devops/azure-pipelines.yml`, `ci/gcp-cloud-build/cloudbuild.yaml`, `ci/aws-codebuild/buildspec.yml`, `ci/gitlab-ci/.gitlab-ci.yml`  
**Issue:** GitHub Actions triggers on changes to `scripts/verify-approvals.py`. The other CI pipelines only trigger on `scripts/validate-adr.py` changes. If someone modifies `verify-approvals.py`, only GitHub Actions runs.

**Impact:** Changes to the approval verification script may not trigger CI on non-GitHub platforms.  
**Fix:** Add `scripts/verify-approvals.py` to the path triggers of all non-GitHub CI pipelines.

---

### Finding 24 — 🟢 P4 | Improvement
#### `__pycache__` directory in scripts

**File:** `scripts/__pycache__/`  
**Issue:** Python bytecode cache should be gitignored (it already is via `.gitignore: __pycache__/`), but the directory exists in the working tree.

**Impact:** No git impact (already ignored), but untidy working directory.  
**Fix:** `rm -rf scripts/__pycache__/` — already handled by .gitignore, just a cleanup.

---

### Finding 25 — 🟢 P4 | Improvement
#### `llms.txt` links are absolute GitHub URLs

**File:** `llms.txt`  
**Issue:** All links are `https://github.com/ivanstambuk/adr-governance/blob/main/...`. If the repo is private or hasn't been pushed yet, these URLs 404.

**Impact:** Cosmetic. The `llms.txt` standard expects absolute URLs, but they break until the repo is public.  
**Fix:** Ensure repo is public before publishing, or use a conditional/relative approach.

---

### Finding 26 — 🟢 P4 | Inconsistency
#### `adr-process.md` and `SKILL.md` give different starting points for ADR authoring

**Issue:** Duplicate of Finding 18 from a different angle.
- `adr-process.md` §3.1: copy from `examples-reference/ADR-0001-*.yaml`
- `SKILL.md` Step 3: use template at `assets/adr-template.yaml`
- `README.md` §8: copy from `.skills/adr-author/assets/adr-template.yaml`

Three sources, two different answers.

**Impact:** User confusion.  
**Fix:** Consolidate on the template approach everywhere.

---

### Finding 27 — 🟢 P4 | Improvement
#### Rendered example index source link path inconsistency

**Files:** `rendered/architecture-decision-log.md`, `examples-reference/rendered/architecture-decision-log.md`  
**Issue:** The main rendered index links sources as `../architecture-decision-log/ADR-NNNN.yaml` (correct relative path). The examples rendered index links to `../ADR-NNNN.yaml` (also correct for its location). Both work, but the column header is "Source" in both — no issue functionally, just documenting for completeness.

**Impact:** None — both resolve correctly.  
**Fix:** No action needed.

---

## Summary by Priority

| Priority | Count | Description |
|:--------:|:-----:|-------------|
| 🔴 P1 | 3 | Active bugs or data errors that should be fixed immediately |
| 🟠 P2 | 8 | Gaps or inconsistencies that affect usability or correctness |
| 🟡 P3 | 12 | Documentation gaps, improvements, and minor inconsistencies |
| 🟢 P4 | 4 | Polish, cleanup, and cosmetic improvements |
| **Total** | **27** | |

## Recommended Fix Order

1. **Quick wins (30 min):** #1, #3, #7, #8, #14, #17, #24
2. **ADR-0000 cleanup (15 min):** #2, #13
3. **Bundle & config fixes (20 min):** #4/11, #21
4. **Documentation alignment (30 min):** #6, #18/26, #15, #16
5. **CI pipeline fixes (20 min):** #5, #12, #23
6. **Script verification (15 min):** #9
7. **DX improvements (30 min):** #10, #20, #22
8. **Defer/skip:** #25, #27
