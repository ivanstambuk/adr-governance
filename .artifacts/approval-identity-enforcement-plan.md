# Implementation Plan: ADR Approval ↔ PR Approval Identity Enforcement

## Objective
Ensure that ADR `approvals[]` identities match actual PR approvers, enforced at CI time.

---

## Phase 1: Schema & Template Changes

- [ ] **1.1** Add `identity` field to `approvals` in `schemas/adr.schema.json`
  - Field: `identity` (string, optional)
  - Description: Platform-resolvable handle (e.g., GitHub `@username`, email, GitLab `@username`)
  - Keep backward compatible (not required)
- [ ] **1.2** Update `approvals` in `.skills/adr-author/assets/adr-template.yaml`
  - Add `identity: ""` field to the approvals entry
- [ ] **1.3** Update all example ADRs in `examples-reference/` to include `identity` in approvals
- [ ] **1.4** Update ADR-0000 in `architecture-decision-log/` to include `identity` in approvals
- [ ] **1.5** Run `validate-adr.py` to verify all files still pass validation

## Phase 2: Process Documentation Updates

- [ ] **2.1** Add "Approval Identity Rule" section to `docs/adr-process.md` (new §3.4a or expand §3.4)
  - Document: approvals[].identity must match PR approvers
  - Document: CI validates this pre-merge
  - Update the Mermaid state diagram annotation
- [ ] **2.2** Update the approval phase checklist in §3.4 to mention `identity`
- [ ] **2.3** Add glossary entry for `identity` in `docs/glossary.md`

## Phase 3: CI Enforcement Script

- [ ] **3.1** Create `scripts/verify-approvals.py`
  - Platform detection (GitHub, Azure DevOps, GitLab) via env vars
  - Parse ADR YAML files changed in the PR
  - Extract `approvals[].identity` from ADRs with status proposed/accepted
  - Query platform API for actual PR approvers
  - Compare and report mismatches
  - Exit with error if any mandatory approver is missing
- [ ] **3.2** Add verify-approvals step to `.github/workflows/validate-adr.yml`
- [ ] **3.3** Add verify-approvals step to `ci/azure-devops/azure-pipelines.yml`
- [ ] **3.4** Add verify-approvals step to `ci/gitlab-ci/.gitlab-ci.yml`
- [ ] **3.5** Add verify-approvals step to `ci/gcp-cloud-build/cloudbuild.yaml`
- [ ] **3.6** Add verify-approvals step to `ci/aws-codebuild/buildspec.yml`

## Phase 4: CI Setup Documentation

- [ ] **4.1** Add "Approval Identity Verification" section to `docs/ci-setup.md`
  - Per-platform configuration guidance
  - How to configure mandatory reviewers on each platform
  - How the CI script maps ADR identities to platform identities
- [ ] **4.2** Update `CODEOWNERS.example` with annotation about ADR approvals relationship

## Phase 5: README & Skill Updates

- [ ] **5.1** Update `README.md` — mention approval enforcement in features/overview
- [ ] **5.2** Update ADR author skill if it references approvals
- [ ] **5.3** Final validation pass — run validate-adr.py on all directories

## Phase 6: Commit

- [ ] **6.1** Stage and commit all changes

---

## Tracker

| Phase | Status |
|-------|--------|
| 1. Schema & Template | ⬜ Not started |
| 2. Process Docs | ⬜ Not started |
| 3. CI Script | ⬜ Not started |
| 4. CI Setup Docs | ⬜ Not started |
| 5. README & Skill | ⬜ Not started |
| 6. Commit | ⬜ Not started |
