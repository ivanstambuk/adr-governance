# ADR Governance Audit Report

Date: 2026-03-06

Repository: `adr-governance`

Audit scope: source-of-truth files, governance model, schema, scripts, CI templates, skill assets, and documentation.

Out of scope: generated artifacts as deliverables (`rendered/`, `adr-governance-bundle.md`, `llms-full.txt`, `llms.txt`) except where their generation path creates governance, quality, or drift risk.

No code changes were made as part of this audit.

---

## Executive Summary

This project has a strong concept, a good documentation surface, realistic example ADRs, and a useful initial tooling stack.
The main weaknesses are not cosmetic.
They are trust-model weaknesses:

1. Several governance guarantees are described as if they are enforced, but are currently only advisory or partially implemented.
2. The AI-facing assets (skill, repomix instruction, bundle config) have already drifted from the schema and validator.
3. The repository lacks automated regression checks that would catch exactly this kind of drift.

The highest-risk issues are:

- schema `format` constraints are not actually enforced by the validator
- accepted/proposed ADR approval evidence is too optional to support the claimed governance model
- the "immutable append-only audit trail" is not enforced and can be edited as a maintenance change
- the project is internally inconsistent about whether accepted ADRs are immutable or living documents
- CI does not cover several source-of-truth governance files
- the web-chat / bundle story is materially less complete than the docs claim

Overall assessment:

- Strategy and product direction: strong
- Baseline implementation quality: good
- Governance enforceability: currently weaker than advertised
- Documentation/tooling consistency: currently too drift-prone

---

## What Is Already Strong

- The core repository shape is coherent: schema, docs, examples, CI templates, skill assets, and helper scripts all exist in one place.
- The example ADRs are substantive and useful.
- The validator and approval-verification scripts are a solid foundation rather than toy examples.
- The governance config in [`.adr-governance/config.yaml`](.adr-governance/config.yaml) is the right idea.
- The docs are ambitious and cover more than most ADR repositories do.

These strengths are worth preserving.
Most recommendations below are about tightening enforcement and reducing drift, not changing the overall direction.

---

## Method

I reviewed the following areas directly:

- Core docs: [README.md](README.md), [docs/adr-process.md](docs/adr-process.md), [docs/ci-setup.md](docs/ci-setup.md), [docs/decision-enforcement.md](docs/decision-enforcement.md), [docs/ai-authoring.md](docs/ai-authoring.md), [docs/rendering.md](docs/rendering.md), [docs/web-chat-quickstart.md](docs/web-chat-quickstart.md), [docs/glossary.md](docs/glossary.md)
- Schema and governance: [schemas/adr.schema.json](schemas/adr.schema.json), [`.adr-governance/config.yaml`](.adr-governance/config.yaml)
- Tooling: [scripts/validate-adr.py](scripts/validate-adr.py), [scripts/verify-approvals.py](scripts/verify-approvals.py), [scripts/render-adr.py](scripts/render-adr.py), [scripts/extract-decisions.py](scripts/extract-decisions.py), [scripts/review-adr.py](scripts/review-adr.py), [scripts/summarize-adr.py](scripts/summarize-adr.py), [scripts/bundle.sh](scripts/bundle.sh), [scripts/generate-llms-full.sh](scripts/generate-llms-full.sh)
- CI templates: [`.github/workflows/validate-adr.yml`](.github/workflows/validate-adr.yml), [ci/azure-devops/azure-pipelines.yml](ci/azure-devops/azure-pipelines.yml), [ci/gcp-cloud-build/cloudbuild.yaml](ci/gcp-cloud-build/cloudbuild.yaml), [ci/aws-codebuild/buildspec.yml](ci/aws-codebuild/buildspec.yml), [ci/gitlab-ci/.gitlab-ci.yml](ci/gitlab-ci/.gitlab-ci.yml)
- Skill and AI bundle assets: [`.skills/adr-author/SKILL.md`](.skills/adr-author/SKILL.md), [`.skills/adr-author/assets/adr-template.yaml`](.skills/adr-author/assets/adr-template.yaml), [`.skills/adr-author/references/SCHEMA_REFERENCE.md`](.skills/adr-author/references/SCHEMA_REFERENCE.md), [repomix.config.json](repomix.config.json), [repomix-instruction.md](repomix-instruction.md)

I also ran local validation and several targeted repro cases against the current scripts.

---

## Priority Scale

- `Critical`: undermines a core governance/security/integrity claim
- `High`: materially weakens reliability, portability, or trust in the framework
- `Medium`: meaningful gap or design weakness that should be addressed soon
- `Low`: useful cleanup or UX improvement

Tracker status is currently `Open` for all items.

---

## Tracker Summary

| ID | Priority | Area | Title | Status |
|---|---|---|---|---|
| R-01 | Critical | Validation | Schema `format` constraints are not enforced | Resolved 2026-03-06 |
| R-02 | Critical | Governance | Approval evidence for proposed/accepted ADRs is too optional | Resolved 2026-03-06 |
| R-03 | Critical | Auditability | The audit trail is described as immutable but is editable as maintenance | Resolved 2026-03-06 |
| R-04 | High | Process model | Accepted ADR immutability is internally contradictory across docs and tooling | Resolved 2026-03-07 |
| R-05 | High | CI coverage | CI does not trigger on several governance-critical source files | Resolved 2026-03-07 |
| R-06 | High | Platform support | AWS/GCP approval-verification guidance is incomplete and currently overstated | Resolved 2026-03-07 |
| R-07 | High | AI bundle | The web-chat bundle is not actually a complete framework artifact | Needs decision 2026-03-07 |
| R-08 | High | AI assets | Skill and bundle instructions already drift from the schema/tooling | Resolved 2026-03-07 |
| R-09 | High | Quality engineering | No automated regression/sync test suite exists | Resolved 2026-03-07 |
| R-10 | Medium | Lifecycle semantics | `draft` does not behave like a true work-in-progress state | Needs decision 2026-03-07 |
| R-11 | Medium | Lifecycle automation | Periodic review is documented but not operationalized | Needs decision 2026-03-07 |
| R-12 | Medium | Identifier integrity | Identifier checks are incomplete in validation and CI | Resolved 2026-03-07 |
| R-13 | Medium | Policy enforcement | Too many normative governance failures are warnings, not errors | Needs decision 2026-03-07 |
| R-14 | Medium | Generated outputs | Generated docs/LLM assets rely on optional local hooks and are not checked in CI | Needs decision 2026-03-07 |
| R-15 | Low | Consistency/UX | Smaller documentation and rendering inconsistencies remain | Resolved 2026-03-07 |

---

## Detailed Tracker

### R-01 - Critical - Schema `format` constraints are not enforced

- Area: Validation
- Status: Resolved 2026-03-06
- Evidence:
  - [schemas/adr.schema.json](schemas/adr.schema.json) declares `format` on `date-time`, `date`, `email`, and `uri` fields.
  - [scripts/validate-adr.py](scripts/validate-adr.py) constructs `Draft202012Validator(schema)` without a `format_checker`.
  - Repro during audit: a test ADR with invalid `created_at`, invalid emails, invalid reference URL, and invalid `audit_trail.at` still validated as `OK`.
- Resolution:
  - [scripts/validate-adr.py](scripts/validate-adr.py) now builds `Draft202012Validator` with an enabled `format_checker`.
  - [scripts/validate-adr.py](scripts/validate-adr.py) now fails fast if required format checkers are unavailable.
  - [requirements.txt](requirements.txt) now requires `jsonschema[format]>=4.20`.
- Impact:
  - The project currently overstates the strength of schema validation.
  - Invalid timestamps, emails, and URLs can enter the repo and pass CI.
  - Downstream tooling may then fail or behave unpredictably on supposedly valid ADRs.
- Recommended actions:
  1. Add explicit format checking in [scripts/validate-adr.py](scripts/validate-adr.py).
  2. Add regression fixtures covering invalid `date-time`, `date`, `email`, and `uri`.
  3. Treat invalid formats as blocking errors, not warnings.
- Discussion notes:
  - This is a core trust issue because the schema advertises constraints that are not actually enforced.

### R-02 - Critical - Approval evidence for proposed/accepted ADRs is too optional

- Area: Governance
- Status: Resolved 2026-03-06
- Evidence:
  - [schemas/adr.schema.json](schemas/adr.schema.json) makes `approvals` optional and makes `identity` optional inside approval entries.
  - [docs/adr-process.md](docs/adr-process.md) treats approval identity binding as a central governance rule.
  - [scripts/verify-approvals.py](scripts/verify-approvals.py) only warns when approvals exist without `identity`; it does not fail.
  - Repro during audit:
    - a `proposed` ADR with approvals but no `identity` validated successfully
    - an `accepted` ADR with no approvals and no audit trail also validated successfully
- Impact:
  - A repo can claim governed approvals while allowing accepted ADRs that are missing enforceable approval evidence.
  - The strongest governance claim in the project becomes opt-in instead of default.
- Resolution:
  - [schemas/adr.schema.json](schemas/adr.schema.json) now requires `approvals[]` with at least one entry when `adr.status` is `proposed` or `accepted`.
  - [schemas/adr.schema.json](schemas/adr.schema.json) now requires `identity` on every approval entry when `adr.status` is `proposed` or `accepted`.
  - [scripts/validate-adr.py](scripts/validate-adr.py) now fails `accepted` ADRs that do not include at least one non-null `approved_at` timestamp.
  - [scripts/validate-adr.py](scripts/validate-adr.py) now fails `accepted` ADRs that do not include an `approved` audit-trail event.
  - Supporting docs and the ADR template comment were updated to reflect the stricter rule.
- Recommended actions:
  1. Decide the policy explicitly:
     - either require `approvals[].identity` for all `proposed`/`accepted` ADRs
     - or downgrade the public claims and describe the feature as optional
  2. Add status-aware validation so `accepted` ADRs require approval evidence.
  3. Consider making missing identities an error for new adopters while retaining a migration flag for legacy repos.
- Discussion notes:
  - This is especially important because the README markets approval identity enforcement as a core capability.

### R-03 - Critical - The audit trail is described as immutable but is editable as maintenance

- Area: Auditability
- Status: Resolved 2026-03-06
- Evidence:
  - [README.md](README.md), [docs/adr-process.md](docs/adr-process.md), [docs/glossary.md](docs/glossary.md), and [`.skills/adr-author/SKILL.md`](.skills/adr-author/SKILL.md) describe the audit trail as append-only / immutable.
  - [`.adr-governance/config.yaml`](.adr-governance/config.yaml) classifies `audit_trail` as maintenance by omission from `substantive_fields`.
  - [scripts/verify-approvals.py](scripts/verify-approvals.py) skips approval-identity checks for maintenance changes.
  - Repro during audit:
    - editing an existing `audit_trail` entry was classified as maintenance
    - deleting an `audit_trail` entry was classified as maintenance
    - appending a new `audit_trail` entry was also classified as maintenance
- Impact:
  - Historical evidence can be rewritten or deleted under the same rules as clerical edits.
  - This directly conflicts with the repo's auditability claims.
  - In regulated or forensic use cases, this weakens confidence substantially.
- Resolution:
  - [scripts/verify-approvals.py](scripts/verify-approvals.py) now enforces append-only `audit_trail` semantics for existing ADRs during PR comparison.
  - Existing audit-trail entries may remain unchanged or have new entries appended at the end.
  - CI now blocks editing, deleting, or reordering historical audit-trail entries.
  - Supporting docs and governance comments were updated to describe the rule as enforced behavior.
- Recommended actions:
  1. Enforce append-only semantics in [scripts/validate-adr.py](scripts/validate-adr.py) or [scripts/verify-approvals.py](scripts/verify-approvals.py):
     - allow append
     - block edits or deletions to existing entries
  2. Reclassify `audit_trail` handling:
     - either make all `audit_trail` changes substantive
     - or split append vs modify/delete into separate policy treatment
  3. Add explicit regression tests for edit/delete/append cases.
- Discussion notes:
  - This is one of the highest-value fixes in the repo because it closes the biggest gap between promise and enforcement.

### R-04 - High - Accepted ADR immutability is internally contradictory across docs and tooling

- Area: Process model
- Status: Resolved 2026-03-07
- Evidence:
  - [docs/adr-process.md](docs/adr-process.md) state diagram says accepted ADRs are immutable.
  - [README.md](README.md) describes the ADL as append-only.
  - The same process doc also defines substantive in-place edits to `decision.*`, `alternatives.*`, `consequences.*`, and `context.summary`, with re-approval instead of mandatory supersession.
  - [docs/adr-process.md](docs/adr-process.md) also defines ADR document versioning for substantive changes, which is a living-document model.
  - [`.adr-governance/config.yaml`](.adr-governance/config.yaml) and [scripts/verify-approvals.py](scripts/verify-approvals.py) operationalize that living-document model.
- Impact:
  - Reviewers and adopters cannot tell whether the intended model is:
    - immutable accepted ADRs with supersession for any real change, or
    - mutable accepted ADRs with versioning and re-approval
  - This ambiguity affects governance, auditability, tooling rules, and user expectations.
- Resolution:
  - The repo now adopts an explicit hybrid policy: accepted ADRs keep an immutable decision core, while controlled post-acceptance metadata updates remain allowed.
  - [scripts/verify-approvals.py](scripts/verify-approvals.py) now blocks in-place edits to configured immutable fields when the base ADR is already `accepted`.
  - [scripts/verify-approvals.py](scripts/verify-approvals.py) now only allows an already accepted ADR to remain `accepted` or transition to `superseded` / `deprecated`.
  - [`.adr-governance/config.yaml`](.adr-governance/config.yaml) now declares `immutable_after_acceptance_fields` separately from `substantive_fields`.
  - [docs/adr-process.md](docs/adr-process.md), [docs/glossary.md](docs/glossary.md), and [docs/ci-setup.md](docs/ci-setup.md) now describe accepted ADRs as having a frozen decision core rather than a fully read-only file.
  - ADR document versioning guidance now treats post-acceptance updates as maintenance-only minor bumps; material decision changes require a new superseding ADR.
- Recommended actions:
  1. Add regression coverage for accepted ADR edit attempts:
     - decision-core change should fail
     - confirmation/reference updates should pass
     - accepted → superseded/deprecated should pass
  2. Treat `immutable_after_acceptance_fields` in [`.adr-governance/config.yaml`](.adr-governance/config.yaml) as a governed interface; changes to it should be rare and architecture-team reviewed.
  3. Update contributor onboarding so authors understand that substantive post-acceptance changes require supersession, not in-place rewriting.
- Discussion notes:
  - This is a foundational product decision, not just a doc cleanup.

### R-05 - High - CI does not trigger on several governance-critical source files

- Area: CI coverage
- Status: Resolved 2026-03-07
- Evidence:
  - [`.github/workflows/validate-adr.yml`](.github/workflows/validate-adr.yml) and the platform templates trigger on ADR files, schema files, and only two scripts.
  - They do not trigger on key governance/tooling files such as:
    - [`.adr-governance/config.yaml`](.adr-governance/config.yaml)
    - [`.yamllint.yml`](.yamllint.yml)
    - [requirements.txt](requirements.txt)
    - [scripts/review-adr.py](scripts/review-adr.py)
    - [scripts/render-adr.py](scripts/render-adr.py)
    - [scripts/extract-decisions.py](scripts/extract-decisions.py)
    - [scripts/bundle.sh](scripts/bundle.sh)
    - [`.skills/adr-author/assets/adr-template.yaml`](.skills/adr-author/assets/adr-template.yaml)
    - [repomix-instruction.md](repomix-instruction.md)
  - Workflow/template changes themselves are also not covered.
- Impact:
  - Governance-critical source changes can merge without the repo's own validation path running.
  - This is one reason drift between docs, instructions, and tooling can accumulate silently.
- Resolution:
  - [`.github/workflows/validate-adr.yml`](.github/workflows/validate-adr.yml), [ci/azure-devops/azure-pipelines.yml](ci/azure-devops/azure-pipelines.yml), and [ci/gitlab-ci/.gitlab-ci.yml](ci/gitlab-ci/.gitlab-ci.yml) no longer use the narrow ADR-only path filters; they now run on every PR/MR and every push to the default branch.
  - All shipped CI templates now run [scripts/check-repo-integrity.sh](scripts/check-repo-integrity.sh) before ADR validation.
  - [scripts/check-repo-integrity.sh](scripts/check-repo-integrity.sh) adds lightweight smoke coverage for governance tooling outside the main validator:
    - Python syntax checks for `scripts/*.py`
    - shell syntax checks for `scripts/*.sh`
    - runtime smoke tests for `render-adr.py`, `extract-decisions.py`, `review-adr.py`, and `summarize-adr.py`
    - `repomix.config.json` syntax validation when present
  - Supporting docs now describe the broader CI coverage and the repository-integrity layer.
- Recommended actions:
  1. Keep the default-branch / PR pipelines broad; do not reintroduce ADR-only path filtering unless a replacement integrity mechanism exists.
  2. Expand `check-repo-integrity.sh` if more shipped tooling becomes governance-critical.
  3. If adopters insist on path filters in their own repos, document the minimum governance-source file set explicitly.
- Discussion notes:
  - This is less about more CI and more about covering the actual source of truth.

### R-06 - High - AWS/GCP approval-verification guidance is incomplete and currently overstated

- Area: Platform support
- Status: Resolved 2026-03-07
- Evidence:
  - [docs/ci-setup.md](docs/ci-setup.md) says AWS/GCP can enable full approval verification by storing `GITHUB_TOKEN` and removing `--dry-run`.
  - [ci/gcp-cloud-build/cloudbuild.yaml](ci/gcp-cloud-build/cloudbuild.yaml) and [ci/aws-codebuild/buildspec.yml](ci/aws-codebuild/buildspec.yml) both run [scripts/verify-approvals.py](scripts/verify-approvals.py) in `--dry-run` mode by default.
  - [scripts/verify-approvals.py](scripts/verify-approvals.py) only auto-detects `github`, `azure-devops`, or `gitlab` from platform-specific env vars; it does not auto-detect GitHub merely from a token in AWS/GCP environments.
  - The same script also depends on PR metadata (`repo`, `pr`, diff base) that the AWS/GCP templates do not provide.
- Impact:
  - The current docs make this capability sound easier and more complete than it is.
  - Adopters may believe they have approval identity enforcement on AWS/GCP when they actually only have a dry-run listing.
- Resolution:
  - [docs/ci-setup.md](docs/ci-setup.md) now states that the shipped AWS/GCP templates run approval verification in dry-run mode by default.
  - [docs/ci-setup.md](docs/ci-setup.md) now describes full GitHub-backed approval verification on AWS/GCP as a manual custom integration path that requires explicit `--platform`, `--repo`, and `--pr` wiring plus a token.
  - [ci/gcp-cloud-build/cloudbuild.yaml](ci/gcp-cloud-build/cloudbuild.yaml) and [ci/aws-codebuild/buildspec.yml](ci/aws-codebuild/buildspec.yml) now describe the same limitation in-template so adopters do not over-read the shipped defaults.
- Recommended actions:
  1. If first-class AWS/GCP approval verification is desired later, add end-to-end templates that pass PR metadata explicitly instead of relying on dry-run output.
  2. Keep the docs conservative until that integration is implemented and tested.
- Discussion notes:
  - This is a product-trust issue more than an implementation detail.

### R-07 - High - The web-chat bundle is not actually a complete framework artifact

- Area: AI bundle
- Status: Needs decision 2026-03-07
- Evidence:
  - [repomix.config.json](repomix.config.json) explicitly excludes:
    - [docs/web-chat-quickstart.md](docs/web-chat-quickstart.md)
    - [docs/ci-setup.md](docs/ci-setup.md)
    - [scripts/verify-approvals.py](scripts/verify-approvals.py)
    - [scripts/render-adr.py](scripts/render-adr.py)
    - [scripts/extract-decisions.py](scripts/extract-decisions.py)
    - [scripts/bundle.sh](scripts/bundle.sh)
    - [`.github/`](.github/)
  - [README.md](README.md), [docs/decision-enforcement.md](docs/decision-enforcement.md), and [docs/ai-authoring.md](docs/ai-authoring.md) describe the bundle as containing the complete framework or enabling full-surface use cases.
  - [repomix-instruction.md](repomix-instruction.md) tells the AI to search for excluded files.
- Impact:
  - The bundle is less self-sufficient than the docs imply.
  - Web-chat users may receive weaker or partially hallucinated guidance on excluded areas such as CI setup and enforcement scripts.
- Recommended actions:
  1. Decide what the bundle is supposed to be:
     - a full framework bundle, or
     - a narrowed authoring/query bundle
  2. Align [repomix.config.json](repomix.config.json), [repomix-instruction.md](repomix-instruction.md), and public docs to that decision.
  3. If "full framework" remains the promise, include the excluded source files or generate a second, larger bundle variant.
- Discussion notes:
  - This is especially important because AI/web-chat usage is one of the project's headline differentiators.
  - Not changed in this pass because it requires a product decision about bundle scope, not just a repo-alignment fix.

### R-08 - High - Skill and bundle instructions already drift from the schema and validator

- Area: AI assets
- Status: Resolved 2026-03-07
- Evidence:
  - [`.skills/adr-author/SKILL.md`](.skills/adr-author/SKILL.md) artifact-driven example uses `audit_trail` fields `date`, `author`, and `description`, but the schema requires `by`, `at`, and optional `details`.
  - [repomix-instruction.md](repomix-instruction.md) repeats the same schema-invalid `audit_trail` example.
  - [repomix-instruction.md](repomix-instruction.md) refers to `alternatives[].summary`, but the schema defines `alternatives[].description`.
  - [repomix-instruction.md](repomix-instruction.md) claims validation checks that are not currently implemented, such as `created_at <= last_modified`.
- Impact:
  - The AI-facing experience can actively generate invalid ADR content or misleading validation expectations.
  - This undermines the repo's "AI-native" positioning.
- Resolution:
  - [`.skills/adr-author/SKILL.md`](.skills/adr-author/SKILL.md) and [repomix-instruction.md](repomix-instruction.md) now use the correct `audit_trail` field names: `by`, `at`, and `details`.
  - [repomix-instruction.md](repomix-instruction.md) now references `alternatives[].description` instead of the nonexistent `alternatives[].summary`.
  - AI-facing instructions now use the correct ADR branch naming pattern and the current `jsonschema[format]` install command.
  - [`.skills/adr-author/references/SCHEMA_REFERENCE.md`](.skills/adr-author/references/SCHEMA_REFERENCE.md) was updated to reflect current validator behavior, including exact filename/`adr.id` matching and immutable-after-acceptance rules.
  - Machine-checked consistency coverage now exists in the new `tests/` suite to catch future schema/instruction drift.
- Recommended actions:
  1. Keep AI instruction assets under the same regression suite as validator/tooling changes.
  2. Treat schema-facing documentation as governed source, not passive prose.
- Discussion notes:
  - The drift is already real, not hypothetical.

### R-09 - High - No automated regression or sync test suite exists

- Area: Quality engineering
- Status: Resolved 2026-03-07
- Evidence:
  - The repo has no dedicated unit/golden/integration test directory.
  - CI currently validates example ADR data and runs linting, but does not test:
    - validator edge cases
    - approval-verification behavior
    - rendering output
    - summarize/review/extract script output contracts
    - schema/template/skill/reference sync
    - repomix bundle completeness
- Impact:
  - Regressions are likely to be found by users or by manual review after drift has already landed.
  - This is the systemic reason several current inconsistencies were able to accumulate.
- Resolution:
  - A new `tests/` suite now covers validator behavior, approval-verification rules, tool output contracts, and AI/doc asset consistency.
  - [scripts/check-repo-integrity.sh](scripts/check-repo-integrity.sh) now runs the regression suite via `python3 -m unittest discover -s tests -v`.
  - CI templates now run [scripts/check-repo-integrity.sh](scripts/check-repo-integrity.sh), so the regression suite executes on every shipped pipeline path.
  - Local developer ergonomics now include [Makefile](Makefile) targets for `test` and `integrity`.
- Recommended actions:
  1. Extend the suite incrementally as unresolved governance decisions become concrete.
  2. Add deeper golden/output coverage if renderer or bundle behavior becomes more central.
- Discussion notes:
  - This does not need to start big.
  - A focused fixture suite would deliver a lot of value quickly.

### R-10 - Medium - `draft` does not behave like a true work-in-progress state

- Area: Lifecycle semantics
- Status: Needs decision 2026-03-07
- Evidence:
  - [docs/adr-process.md](docs/adr-process.md) presents `draft` as WIP authoring state.
  - [schemas/adr.schema.json](schemas/adr.schema.json) always requires `decision.chosen_alternative`, `decision.rationale`, and `decision.decision_date`.
  - Repro during audit: an incomplete `draft` ADR failed validation because `decision_date` and substantive decision content were missing.
- Impact:
  - The lifecycle model is semantically weak because "draft" still requires near-final content.
  - This makes incremental authoring harder and blurs the difference between `draft` and `proposed`.
- Recommended actions:
  1. Decide whether validation should be status-aware.
  2. If yes, allow a weaker requirement set for `draft`.
  3. If no, change the docs to make it clear that `draft` means "complete but not yet proposed", not early WIP.
- Discussion notes:
  - This is mostly a product/UX decision, but it affects schema design directly.
  - Not changed in this pass because both "true WIP draft" and "complete-but-unproposed draft" are plausible models.

### R-11 - Medium - Periodic review is documented but not operationalized

- Area: Lifecycle automation
- Status: Needs decision 2026-03-07
- Evidence:
  - [docs/adr-process.md](docs/adr-process.md) says ADRs with review cadence "will be flagged for periodic review".
  - No script currently scans for overdue `lifecycle.next_review_date`.
  - No CI/template path exists for overdue review reporting.
  - [scripts/render-adr.py](scripts/render-adr.py) only renders review dates; it does not flag anything.
- Impact:
  - Review cadence exists as metadata, not as an active governance mechanism.
  - One of the project's core arguments against decision rot is therefore only partially realized.
- Recommended actions:
  1. Add a review-check script that:
     - lists overdue ADRs
     - can fail CI or open an issue on a schedule
  2. Decide whether overdue reviews are advisory or blocking.
  3. Surface overdue status in rendered Markdown and/or decision-log indexes.
- Discussion notes:
  - This is a good candidate for a scheduled CI workflow rather than PR-only validation.
  - Not changed in this pass because advisory versus blocking review enforcement is a policy choice.

### R-12 - Medium - Identifier checks are incomplete in validation and CI

- Area: Identifier integrity
- Status: Resolved 2026-03-07
- Evidence:
  - [scripts/validate-adr.py](scripts/validate-adr.py) only compares the `ADR-NNNN` prefix between filename and `adr.id`; it does not ensure the full slug matches.
  - Repro during audit: a file named `ADR-1234-filename-foo.yaml` with `adr.id: ADR-1234-id-bar` validated successfully.
  - Duplicate ADR ID detection exists, but GitHub/CI templates validate `architecture-decision-log/` and `examples-reference/` in separate invocations, so duplicates across both directories are not caught in CI.
  - Local `make validate` uses a combined invocation and is therefore stricter than CI.
- Impact:
  - Filename/source mismatches and cross-directory ID collisions can survive CI.
  - This weakens navigability and traceability.
- Resolution:
  - [scripts/validate-adr.py](scripts/validate-adr.py) now enforces exact filename-stem equality with `adr.id`, not just numeric-prefix equality.
  - A new shared CI helper, [scripts/run-validation.sh](scripts/run-validation.sh), validates all ADR directories in one invocation so duplicate IDs across `architecture-decision-log/` and `examples-reference/` are caught in CI.
  - [Makefile](Makefile) now uses the same shared validation helper locally, keeping local and CI behavior aligned.
  - Regression coverage now exists for slug mismatch and cross-directory duplicate-ID scenarios.
- Recommended actions:
  1. Keep all validation entry points routed through [scripts/run-validation.sh](scripts/run-validation.sh) unless a stronger shared alternative replaces it.
  2. Extend identifier checks further only if new ID-bearing sections are added to the schema.
- Discussion notes:
  - This is a good example of local tooling and CI behaving differently today.

### R-13 - Medium - Too many normative governance failures are warnings, not errors

- Area: Policy enforcement
- Status: Needs decision 2026-03-07
- Evidence:
  - [scripts/validate-adr.py](scripts/validate-adr.py) treats several normative governance conditions as warnings:
    - accepted/rejected/superseded status without matching audit event
    - accepted ADR without approval timestamps
    - archival on non-terminal status
    - supersession symmetry across files
    - missing `adr.schema_version`
  - [docs/adr-process.md](docs/adr-process.md) often describes these as expected governance rules, not optional suggestions.
- Impact:
  - The project's merge gate is weaker than the process docs imply.
  - Teams may assume these invariants are enforced when they are not.
- Recommended actions:
  1. Classify validation checks into three explicit tiers:
     - hard governance errors
     - soft warnings
     - informational quality hints
  2. Promote some current warnings to errors, especially around accepted-status evidence and supersession correctness.
  3. Make the severity policy configurable if flexibility is important.
- Discussion notes:
  - The main issue is not that warnings exist.
  - The issue is that some governance promises are currently only warnings.
  - Not changed in this pass because the correct error/warning boundary is a policy decision, not a purely mechanical fix.

### R-14 - Medium - Generated docs and LLM assets rely on optional local hooks and are not checked in CI

- Area: Generated outputs
- Status: Needs decision 2026-03-07
- Evidence:
  - [`.githooks/pre-commit`](.githooks/pre-commit) renders ADR Markdown and regenerates `llms-full.txt`, but enabling the hook is optional and per-clone.
  - CI does not verify that:
    - [rendered/](rendered/)
    - [examples-reference/rendered/](examples-reference/rendered/)
    - [llms-full.txt](llms-full.txt)
    - [adr-governance-bundle.md](adr-governance-bundle.md)
    are current with their sources.
  - CI also does not run [scripts/render-adr.py](scripts/render-adr.py) or [scripts/bundle.sh](scripts/bundle.sh) as integrity checks.
- Impact:
  - Human-facing rendered outputs and AI-facing bundles can drift from source-of-truth files without detection.
  - The repo currently relies on contributor discipline rather than repository enforcement.
- Recommended actions:
  1. Add a CI "generated artifacts are current" check.
  2. Keep the pre-commit hook as convenience, not as the only enforcement layer.
  3. Decide whether the bundle is versioned source, build artifact, or release artifact; then enforce accordingly.
- Discussion notes:
  - This matters because the project deliberately ships both human-facing and AI-facing derived assets.
  - Not changed in this pass because the right enforcement model depends on whether generated outputs are treated as committed source, build artifacts, or release artifacts.

### R-15 - Low - Smaller documentation and rendering inconsistencies remain

- Area: Consistency / UX
- Status: Resolved 2026-03-07
- Evidence:
  - Branch naming is inconsistent across docs:
    - `adr/ADR-NNNN-short-title`
    - `adr/NNNN-short-title`
    - `adr/0001-your-decision-title`
  - [docs/ci-setup.md](docs/ci-setup.md) says line length is overridden in the pipeline file, but the setting actually lives in [`.yamllint.yml`](.yamllint.yml).
  - [scripts/render-adr.py](scripts/render-adr.py) only shows approvals with timestamps, so pending approvers are invisible in rendered proposed ADRs.
- Impact:
  - These are not trust-boundary issues, but they add friction and can confuse adopters.
- Resolution:
  - Branch naming guidance is now consistent on the `adr/ADR-NNNN-short-title` pattern across [README.md](README.md), [docs/web-chat-quickstart.md](docs/web-chat-quickstart.md), and [repomix-instruction.md](repomix-instruction.md).
  - [docs/ci-setup.md](docs/ci-setup.md) now correctly points line-length configuration guidance to [`.yamllint.yml`](.yamllint.yml), not to the pipeline files.
  - [README.md](README.md) now uses the correct field names for `alternatives[].description` and `architecturally_significant_requirements`.
  - [scripts/render-adr.py](scripts/render-adr.py) now renders pending approvers, not only already-approved entries, improving proposed-ADR review visibility.
- Recommended actions:
  1. Keep small UX consistency fixes folded into the regression suite so they do not regress quietly.
  2. Revisit approval rendering only if teams want different identity-visibility defaults.
- Discussion notes:
  - These are worth fixing, but only after the higher-priority trust and enforcement issues.

---

## Reproduction Notes

The following behaviors were reproduced during the audit:

### 1. Invalid schema formats pass validation

Observed:

- invalid `created_at`
- invalid author email
- invalid decision owner email
- invalid reference URL
- invalid `audit_trail.at`

All passed schema validation because `format` was not enforced.

### 2. Accepted ADRs can validate without governance evidence

Observed:

- `accepted` ADR with no `approvals` and no `audit_trail` validated successfully
- `proposed` ADR with approvals but without `approvals[].identity` validated successfully

### 3. Audit trail modifications are treated as maintenance

Observed:

- editing an existing audit trail entry
- deleting an audit trail entry
- appending an audit trail entry

All were classified by [scripts/verify-approvals.py](scripts/verify-approvals.py) as non-substantive maintenance changes.

### 4. Full filename/id slug mismatches pass validation

Observed:

- filename: `ADR-1234-filename-foo.yaml`
- `adr.id`: `ADR-1234-id-bar`

Validation passed because only the numeric prefix was checked.

### 5. Incomplete drafts do not validate

Observed:

- a `draft` ADR without `decision.decision_date` and substantive decision content failed validation

This confirms that `draft` is not currently modeled as an early WIP state.

---

## Recommended Sequencing

### Phase 1 - Trust boundary hardening

Address first:

1. R-01 format enforcement
2. R-02 approval evidence requirements
3. R-03 append-only audit trail enforcement
4. R-04 immutability model decision
5. R-13 warning-vs-error policy recalibration

### Phase 2 - Stop the drift

Address next:

1. R-05 CI trigger coverage
2. R-08 instruction/schema alignment
3. R-09 regression and sync tests
4. R-14 generated-artifact verification
5. R-12 identifier integrity

### Phase 3 - Product completeness

Address after that:

1. R-06 platform support cleanup
2. R-07 bundle scope definition
3. R-10 draft lifecycle redesign
4. R-11 periodic review automation
5. R-15 documentation/rendering cleanup

---

## Suggested Ownership Buckets

- Governance model / policy:
  - R-02, R-03, R-04, R-10, R-11, R-13
- Validator / enforcement:
  - R-01, R-02, R-03, R-12, R-13
- CI / automation:
  - R-05, R-06, R-09, R-14
- AI assets / bundle:
  - R-07, R-08, R-09
- Docs / UX:
  - R-04, R-06, R-07, R-08, R-15

---

## Final Assessment

The project is directionally strong and already more mature than most ADR repositories.
The main problem is not lack of ideas.
It is lack of closure between what the framework says it guarantees and what the repository actually enforces.

If the project tightens the validation boundary, resolves the immutability model, and adds a small regression/sync test suite, it will move from "well-documented framework with useful tooling" to "credible governed system."
