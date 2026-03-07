# CI/CD Setup Guide — ADR Validation

This guide explains how to set up automated ADR validation as a **pre-merge gate** on your CI/CD platform. Once configured, every pull request (or merge request) and every push to `main` will run the validation pipeline. The shipped CI templates intentionally do **not** narrow execution by file path, because governance-critical source changes live outside ADR YAML as well.

## What Gets Validated

The validation pipeline runs four checks:

| Check | Tool | Blocks merge? |
|-------|------|:-------------:|
| **Schema compliance** | `validate-adr.py` + JSON Schema | ✅ Yes (errors) |
| **Semantic consistency** | `validate-adr.py` (built-in) | ✅ Yes (errors) / ⚠️ No (warnings) |
| **YAML formatting** | `yamllint` | ✅ Yes |
| **Repository integrity** | `check-repo-integrity.sh` | ✅ Yes |

**Schema compliance** verifies every ADR YAML file conforms to the ADR meta-model ([`schemas/adr.schema.json`](../schemas/adr.schema.json)) — correct structure, types, required fields, and enum values.

**Semantic consistency** goes beyond the schema to check logical invariants:
- `decision.chosen_alternative` matches an entry in `alternatives[].name`
- `adr.status` is consistent with `audit_trail` events (no impossible state transitions)
- `audit_trail` entries are in chronological order
- Existing `audit_trail` entries are append-only across PRs (no edit, delete, or reorder of historical events)
- `lifecycle.supersedes` / `lifecycle.superseded_by` symmetry across files
- Duplicate ADR IDs across the ADL
- Quality signals: missing summaries, premature confidence on drafts, decision dates before creation dates

**YAML formatting** catches indentation errors, trailing whitespace, and overly long lines.

**Repository integrity** smoke-tests governance-critical tooling that would otherwise be outside the ADR-only validation path:
- Python script syntax across `scripts/*.py`
- Shell script syntax across `scripts/*.sh`
- Runtime smoke tests for `render-adr.py`, `extract-decisions.py`, `review-adr.py`, and `summarize-adr.py`
- The `tests/` regression suite via `python3 -m unittest discover`
- `repomix.config.json` JSON syntax when present
- Freshness checks for committed generated artifacts: `rendered/`, `examples-reference/rendered/`, and `llms-full.txt`

The Repomix web-chat bundle (`adr-governance-bundle.md`) is intentionally out of scope for freshness enforcement. It is treated as an on-demand export artifact, not a required committed deliverable.

Out-of-the-box full approval-identity verification is available in the shipped GitHub Actions, Azure DevOps, and GitLab CI setups. The AWS CodeBuild and GCP Cloud Build templates run the verifier in dry-run mode by default until you add custom PR metadata wiring.

## Prerequisites

All platforms need:
- **Python 3.11+** (the validator uses `datetime.fromisoformat` improvements and `X | Y` union syntax)
- **pip packages:** `jsonschema[format]`, `pyyaml` (for validation), `yamllint` (for linting)

The validator itself is [`scripts/validate-adr.py`](../scripts/validate-adr.py) and the schema is [`schemas/adr.schema.json`](../schemas/adr.schema.json) — both are included in this repository.

---

## LLM-Ready Setup Prompts

> **⚡ Fastest path.** Copy-paste the prompt for your platform into any AI assistant (ChatGPT, Claude, Gemini, Copilot, etc.) and it will set up ADR validation CI for your organization. For manual step-by-step instructions, see [Platform Setup (Manual)](#platform-setup-manual) below.

---

### Prompt: GitHub Actions

```
I'm adopting the adr-governance framework (https://github.com/ivanstambuk/adr-governance) for my organization's Architecture Decision Records.

The repository already includes a GitHub Actions workflow at .github/workflows/validate-adr.yml that validates ADR YAML files against a JSON Schema on every PR.

Please help me:
1. Fork or clone the adr-governance repo into my GitHub organization.
2. Delete the examples-reference/ directory if you want (those are fictional reference ADRs, not real decisions).
3. Keep the architecture-decision-log/ directory with ADR-0000 as the bootstrap meta-ADR, updating the authors and decision_owner fields to my name.
4. Set up branch protection on the main branch:
   - Require the "validate" status check to pass before merging
   - Require at least 1 reviewer
   - Require branches to be up to date
5. Copy CODEOWNERS.example to .github/CODEOWNERS and replace @org/architecture-team with our actual team handle: [INSERT YOUR TEAM HANDLE].
6. Verify the setup by creating a test branch with an intentionally malformed ADR and opening a PR to confirm the check fails.

Our organization name is: [INSERT ORG NAME]
Our architecture team handle is: [INSERT TEAM HANDLE, e.g., @myorg/architects]
```

---

### Prompt: Azure DevOps

```
I'm adopting the adr-governance framework (https://github.com/ivanstambuk/adr-governance) for my organization's Architecture Decision Records.

Please help me set this up in Azure DevOps:

1. Clone or import the adr-governance repo into our Azure DevOps project.
2. Delete the examples-reference/ directory if you want (those are fictional reference ADRs, not real decisions).
3. Keep the architecture-decision-log/ directory with ADR-0000 as the bootstrap meta-ADR, updating the authors and decision_owner fields to my name.
4. Copy ci/azure-devops/azure-pipelines.yml to the repository root as azure-pipelines.yml.
5. Create a new pipeline in Azure Pipelines pointing to this file.
6. Set up a branch policy on main:
   - Add the pipeline as a required Build Validation (automatic trigger, required policy)
   - Set minimum reviewers to at least 1
   - Disallow requestors from approving their own changes
7. Verify the setup by creating a test branch with an intentionally malformed ADR and opening a PR to confirm the build policy blocks merge.

Our Azure DevOps organization URL is: [INSERT URL, e.g., https://dev.azure.com/myorg]
Our project name is: [INSERT PROJECT NAME]
```

---

### Prompt: GCP Cloud Build

```
I'm adopting the adr-governance framework (https://github.com/ivanstambuk/adr-governance) for my organization's Architecture Decision Records.

Please help me set this up with GCP Cloud Build:

1. Clone or mirror the adr-governance repo into our source repository (GitHub or Cloud Source Repositories).
2. Delete the examples-reference/ directory if you want (those are fictional reference ADRs, not real decisions).
3. Keep the architecture-decision-log/ directory with ADR-0000 as the bootstrap meta-ADR, updating the authors and decision_owner fields to my name.
4. Copy ci/gcp-cloud-build/cloudbuild.yaml to the repository root.
5. Connect our repository to Cloud Build (2nd gen repository connection).
6. Create a Cloud Build trigger:
   - Name: validate-adr
   - Event: Pull Request (if GitHub) or Push to main (if Cloud Source Repos)
   - Configuration file: /cloudbuild.yaml
7. If using GitHub: enable branch protection requiring the Cloud Build status check to pass before merging.
8. Verify by opening a PR with an intentionally malformed ADR.

Our GCP project ID is: [INSERT PROJECT ID]
Our repository is hosted on: [GitHub / Cloud Source Repositories]
Our repository URL is: [INSERT REPO URL]
```

---

### Prompt: AWS CodeBuild

```
I'm adopting the adr-governance framework (https://github.com/ivanstambuk/adr-governance) for my organization's Architecture Decision Records.

Please help me set this up with AWS CodeBuild:

1. Clone the adr-governance repo into our source repository (GitHub or CodeCommit).
2. Delete the examples-reference/ directory if you want (those are fictional reference ADRs, not real decisions).
3. Keep the architecture-decision-log/ directory with ADR-0000 as the bootstrap meta-ADR, updating the authors and decision_owner fields to my name.
4. Copy ci/aws-codebuild/buildspec.yml to the repository root.
5. Create a CodeBuild project:
   - Name: validate-adr
   - Source: our repository (GitHub via CodeStar Connections or CodeCommit)
   - Environment: Managed image, Ubuntu, Standard, latest
   - Enable webhook for PULL_REQUEST_CREATED, PULL_REQUEST_UPDATED, PULL_REQUEST_REOPENED
   - Enable "Report build statuses to source provider"
6. If using GitHub: enable branch protection requiring the CodeBuild status check to pass before merging.
7. If using CodeCommit: set up EventBridge rules for PR events targeting the CodeBuild project.
8. Verify by opening a PR with an intentionally malformed ADR.

Our AWS region is: [INSERT REGION, e.g., eu-west-1]
Our repository is hosted on: [GitHub / CodeCommit]
Our repository URL is: [INSERT REPO URL]
```

---

### Prompt: GitLab CI/CD

```
I'm adopting the adr-governance framework (https://github.com/ivanstambuk/adr-governance) for my organization's Architecture Decision Records.

Please help me set this up in GitLab:

1. Import or mirror the adr-governance repo into our GitLab group.
2. Delete the examples-reference/ directory if you want (those are fictional reference ADRs, not real decisions).
3. Keep the architecture-decision-log/ directory with ADR-0000 as the bootstrap meta-ADR, updating the authors and decision_owner fields to my name.
4. Copy ci/gitlab-ci/.gitlab-ci.yml to the repository root as .gitlab-ci.yml.
5. Configure merge request settings:
   - Enable "Pipelines must succeed" under Merge checks
   - Enable "All threads must be resolved"
6. Protect the main branch:
   - Allowed to merge: Developers + Maintainers
   - Allowed to push and merge: No one (force merge requests)
7. Verify by creating a merge request with an intentionally malformed ADR.

Our GitLab instance URL is: [INSERT URL, e.g., https://gitlab.com or self-hosted]
Our group/namespace is: [INSERT GROUP NAME]
```

---

## Pipeline Comparison

| Feature | GitHub Actions | Azure DevOps | GCP Cloud Build | AWS CodeBuild | GitLab CI |
|---------|:-:|:-:|:-:|:-:|:-:|
| Pipeline file | `.github/workflows/*.yml` | `azure-pipelines.yml` | `cloudbuild.yaml` | `buildspec.yml` | `.gitlab-ci.yml` |
| Pre-configured in this repo | ✅ | Copy from `ci/` | Copy from `ci/` | Copy from `ci/` | Copy from `ci/` |
| PR trigger (native) | ✅ | ✅ | ✅ (via GitHub App) | ✅ (via webhook) | ✅ |
| Path filtering | ✅ | ✅ | ❌ (filter in trigger) | ❌ (filter in trigger) | ✅ |
| Merge gate enforcement | Branch protection | Branch policies | GitHub branch protection | GitHub branch protection | Merge checks |
| Status check reporting | Native | Native | GitHub Check | GitHub Check | Native |
| Self-hosted runners | ✅ | ✅ | ✅ (private pools) | ✅ (custom images) | ✅ |
| Free tier | 2,000 min/mo | 1 parallel job (free) | 120 min/day | 100 min/mo | 400 min/mo |

---

## Platform Setup (Manual)

> If you used an [LLM prompt above](#llm-ready-setup-prompts), you can skip this section. These are the detailed manual steps for each platform.

### GitHub Actions

> **Pipeline file:** [`.github/workflows/validate-adr.yml`](../.github/workflows/validate-adr.yml) (already included in this repository)

GitHub Actions is preconfigured out of the box. The only remaining step is to enable **branch protection** to enforce it as a merge gate.

#### Steps

1. **Verify the workflow exists.** The file [`.github/workflows/validate-adr.yml`](../.github/workflows/validate-adr.yml) is already in the repository. Push it to your GitHub remote and it will start running automatically on PRs.

2. **Enable branch protection** (merge gate):
   - Go to **Settings → Branches → Add branch ruleset** (or classic branch protection rule)
   - Branch name pattern: `main`
   - Enable: ✅ **Require status checks to pass before merging**
   - Search for and select the `validate` status check
   - Enable: ✅ **Require branches to be up to date before merging** (recommended)
   - Save

3. **(Optional) Configure CODEOWNERS:**
   - Copy `CODEOWNERS.example` to `.github/CODEOWNERS`
   - Replace `@org/architecture-team`, `@org/security-team`, `@org/compliance-team` with your actual GitHub team handles
   - In branch protection, enable: ✅ **Require review from Code Owners**

#### Verification

Create a branch, add or modify an ADR YAML file with an intentional error (e.g., set `status: invalid`), open a PR, and verify the `validate` check fails.

---

### Azure DevOps

> **Pipeline file:** [`ci/azure-devops/azure-pipelines.yml`](../ci/azure-devops/azure-pipelines.yml)

#### Steps

1. **Copy the pipeline file** to your repository root (or reference it by path):
   ```bash
   cp ci/azure-devops/azure-pipelines.yml azure-pipelines.yml
   ```

2. **Create the pipeline** in Azure DevOps:
   - Go to **Pipelines → New Pipeline**
   - Select your repository source (Azure Repos Git, GitHub, etc.)
   - Choose **"Existing Azure Pipelines YAML file"**
   - Select `/azure-pipelines.yml` (or the subdirectory path if you kept it in `ci/`)
   - Click **Run** to verify it works

3. **Enable branch policy** (merge gate):
   - Go to **Repos → Branches**
   - Click the `⋯` menu on the `main` branch → **Branch policies**
   - Under **Build Validation**, click **+ Add build policy**
   - Select the pipeline you just created
   - Trigger: **Automatic**
   - Policy requirement: **Required**
   - Build expiration: **Immediately when `main` is updated** (recommended)
   - Save

4. **(Optional) Require reviewers:**
   - In the same Branch policies page, set **Minimum number of reviewers** ≥ 1
   - Enable: ✅ **Allow requestors to approve their own changes** → No (mirrors the ADR "no self-approval" rule from §3.4)

#### Verification

Create a branch, push a malformed ADR, create a Pull Request targeting `main`, and confirm the build policy blocks completion.

---

### GCP Cloud Build

> **Pipeline file:** [`ci/gcp-cloud-build/cloudbuild.yaml`](../ci/gcp-cloud-build/cloudbuild.yaml)

#### Steps

1. **Copy the pipeline file** to your repository root:
   ```bash
   cp ci/gcp-cloud-build/cloudbuild.yaml cloudbuild.yaml
   ```

2. **Connect your repository** to Cloud Build:
   - Go to **Cloud Build → Repositories** (2nd gen)
   - Click **Create host connection** → select GitHub, GitLab, or Cloud Source Repos
   - Link your repository

3. **Create a build trigger:**
   - Go to **Cloud Build → Triggers → Create Trigger**
   - Name: `validate-adr`
   - Event: **Pull request** (for GitHub/GitLab)
     *For Cloud Source Repos: use "Push to a branch" with pattern `^main$`*
   - Source: select your linked repository
   - Configuration: **Cloud Build configuration file (yaml or json)**
   - Cloud Build configuration file location: `/cloudbuild.yaml`
   - Save

4. **Enable merge gating** (GitHub repos only):
   - The Cloud Build GitHub App automatically reports build status as a **GitHub Check**
   - In your GitHub repo: **Settings → Branches → Branch protection rule**
   - Enable: ✅ **Require status checks to pass before merging**
   - Select the Cloud Build status check
   - Save

#### IAM Permissions

The Cloud Build service account needs no special permissions beyond the defaults for this pipeline — it only runs Python scripts inside the checkout.

#### Verification

Open a PR on GitHub with a schema-violating ADR and confirm Cloud Build reports a failing check.

---

### AWS CodeBuild

> **Pipeline file:** [`ci/aws-codebuild/buildspec.yml`](../ci/aws-codebuild/buildspec.yml)

#### Steps

1. **Copy the buildspec** to your repository root:
   ```bash
   cp ci/aws-codebuild/buildspec.yml buildspec.yml
   ```

2. **Create a CodeBuild project:**
   - Go to **AWS Console → CodeBuild → Create build project**
   - Project name: `validate-adr`
   - Source: **GitHub** (connect via OAuth or AWS CodeStar Connections)
     - Repository: select your repo
     - Enable: ✅ **Rebuild every time a code change is pushed to this repository**
     - Event type: ✅ **PULL_REQUEST_CREATED**, ✅ **PULL_REQUEST_UPDATED**, ✅ **PULL_REQUEST_REOPENED**
   - Enable: ✅ **Report build statuses to source provider**
   - Environment:
     - Managed image → **Ubuntu** → Standard → `aws/codebuild/standard:7.0` (or latest)
     - Runtime: Standard
   - Buildspec: **Use a buildspec file** (defaults to `buildspec.yml` in the repo root)
   - Click **Create build project**

3. **Enable merge gating** (GitHub repos):
   - CodeBuild automatically reports status back to GitHub when "Report build statuses" is enabled
   - In your GitHub repo: **Settings → Branches → Branch protection rule**
   - Enable: ✅ **Require status checks to pass before merging**
   - Select the CodeBuild status check (appears as `CodeBuild:<region>:<account>:<project>`)
   - Save

4. **For AWS CodeCommit** (alternative):
   - Create an **EventBridge rule** that matches `pullRequestCreated` and `pullRequestSourceBranchUpdated` events from CodeCommit
   - Target: your CodeBuild project
   - For merge gating: use **CodePipeline** with an approval action, or use the CodeCommit approval rule templates API

#### IAM Permissions

The CodeBuild service role needs:
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents` (default)
- Source provider connection permissions (created automatically via OAuth/CodeStar)

#### Verification

Create a PR on GitHub, push a malformed ADR, and verify the CodeBuild check fails.

---

### GitLab CI/CD

> **Pipeline file:** [`ci/gitlab-ci/.gitlab-ci.yml`](../ci/gitlab-ci/.gitlab-ci.yml)

#### Steps

1. **Copy the pipeline file** to your repository root:
   ```bash
   cp ci/gitlab-ci/.gitlab-ci.yml .gitlab-ci.yml
   ```

2. **Push to GitLab.** GitLab CI automatically detects `.gitlab-ci.yml` and starts running pipelines — no additional setup needed.

3. **Enable merge gating:**
   - Go to **Settings → Merge Requests**
   - Under **Merge checks**, enable: ✅ **Pipelines must succeed**
   - (Recommended) Also enable: ✅ **All threads must be resolved**
   - Save

4. **(Optional) Protected branch:**
   - Go to **Settings → Repository → Protected branches**
   - Protect `main` with:
     - Allowed to merge: **Developers + Maintainers** (or restrict further)
     - Allowed to push and merge: **No one** (force merge requests)

#### Verification

Create a merge request with a schema-violating ADR and confirm the pipeline fails, blocking the MR.

---

## Customization

### Changing the ADL Directory

If you rename `architecture-decision-log/` to something else (e.g., `adrs/` or `decisions/`), update the path references in:
1. The pipeline file (trigger paths and script commands)
2. `CODEOWNERS` (if using GitHub)

### Adding Additional Validation

To add custom validation rules (e.g., enforcing naming conventions, checking for required tags), modify [`scripts/validate-adr.py`](../scripts/validate-adr.py). The validator is designed to be extended — add your checks in the `validate_file()` function between the schema validation and the return statement.

### Removing Example Validation

The shipped pipelines use [`scripts/run-validation.sh`](../scripts/run-validation.sh), which auto-discovers ADR directories. By default it validates `architecture-decision-log/` and `examples-reference/` separately, so the fictional reference ADRs do not reserve IDs in the live ADR namespace. If you delete `examples-reference/`, no pipeline edits are required — the helper simply skips missing directories.

---
## Approval Identity Verification

In addition to schema validation and YAML linting, CI pipelines can verify that the people listed in an ADR's `approvals[]` section have **actually approved the pull request**. This creates an auditable link between the ADR's approval record and the Git platform's approval record.

### How it works

The [`scripts/verify-approvals.py`](../scripts/verify-approvals.py) script:

1. **Detects the CI platform** (GitHub, Azure DevOps, GitLab) via environment variables
2. **Identifies changed ADR files** in the PR using `git diff`
3. **Extracts `approvals[].identity`** from each changed ADR with `status: proposed` or `accepted`
4. **Queries the platform API** for users who actually approved the PR
5. **Compares the two sets** and fails the build if any required approver has not approved

### Prerequisites

Each ADR approver needs an `identity` field matching their platform handle:

```yaml
approvals:
  - name: "Jane Doe"
    role: "Lead Architect"
    identity: "@janedoe"         # GitHub @username — CI normalizes the @ prefix for matching
    approved_at: "2026-03-15T10:00:00Z"
    signature_id: sig-example-001
```

### Platform-specific configuration

#### GitHub Actions

The workflow is already configured with the verify step. Ensure the following:

1. **Branch protection** must require the `Validate ADR` status check
2. **`GITHUB_TOKEN`** is automatically available — no additional secrets needed
3. The workflow triggers on `pull_request_review` events so re-checks happen when new reviews are submitted

#### Azure DevOps

1. **`System.AccessToken`** is passed as an environment variable to the verify step
2. Configure **Build Validation** as a required policy on the `main` branch
3. Identity format: use the reviewer's **email address** or **UPN** (e.g., `jane.doe@org.com`)

#### GitLab CI

1. **`CI_JOB_TOKEN`** is automatically available for API calls to the same GitLab instance
2. For cross-instance calls, set a `GITLAB_TOKEN` CI/CD variable with `api` scope
3. Enable **"Pipelines must succeed"** in Settings → Merge Requests → Merge checks
4. Identity format: use the reviewer's **GitLab username** (e.g., `janedoe`)

#### AWS CodeBuild / GCP Cloud Build

These platforms don't natively manage PR approvals, and the shipped templates therefore run [`scripts/verify-approvals.py`](../scripts/verify-approvals.py) in **dry-run mode** by default. Out-of-the-box full approval-identity verification is **not** currently wired for AWS/GCP templates.

If your source of truth is GitHub and your build environment can expose the required PR metadata, you can build a custom integration by invoking the verifier explicitly:
1. Provide a GitHub token (`GITHUB_TOKEN` or `GH_TOKEN`)
2. Pass the GitHub repository slug with `--repo owner/repo`
3. Pass the pull request number with `--pr <number>`
4. Force the platform with `--platform github`
5. Pass the target branch with `--base-ref <branch>` or `ADR_BASE_REF=<branch>` unless your CI already exposes a supported target-branch environment variable
6. Ensure the checkout has the PR branch and base branch available so the script can diff against the base revision

Example custom invocation:

```bash
python3 scripts/verify-approvals.py --platform github --repo owner/repo --pr 42 --base-ref main
```

Treat this as a manual integration path, not a built-in supported default of the AWS/GCP templates.

### Configuring mandatory reviewers

For the approval identity check to be meaningful, configure your platform to require approvals from specific people:

| Platform | Configuration |
|----------|--------------|
| **GitHub** | Settings → Branches → Branch protection → "Require pull request reviews" + CODEOWNERS |
| **Azure DevOps** | Repos → Branches → main → Branch policies → "Automatically included reviewers" |
| **GitLab** | Settings → Merge Requests → "Approval rules" → add required approvers |

### Validation behavior

- ADRs in `proposed` or `accepted` status must include `approvals[]` with `identity` on every approval entry; otherwise schema validation fails
- ADRs in `accepted` status must also include at least one non-null `approved_at` timestamp and an `approved` audit-trail event; otherwise semantic validation fails
- ADRs in `rejected` or `deferred` status are **not** identity-bound through `approvals[]`. They must carry the matching terminal audit event (`rejected` / `deferred`), and the detailed reviewer identities and rationale remain in the PR/MR history
- Existing `audit_trail` history is append-only. CI blocks PRs that edit, delete, or reorder historical audit-trail entries
- If an ADR was already `accepted` on the base branch, its decision core is immutable in place. CI only allows it to remain `accepted` or transition to `superseded` / `deprecated`, and blocks edits to frozen fields such as `context`, `decision`, `alternatives`, `consequences`, and `approvals`
- ADRs in `draft`, `rejected`, `deferred`, `superseded`, or `deprecated` status are **skipped for approval identity verification** after the base-vs-head governance checks run
- The shipped CI templates only invoke enforcing mode in PR/MR contexts. Manual non-`--dry-run` invocations must provide resolvable PR metadata and a base ref or the verifier fails closed
- **Maintenance changes** (non-substantive field edits) skip the identity check regardless of who authors the PR

### Governance config file

All governance rules are centralised in [`.adr-governance/config.yaml`](../.adr-governance/config.yaml). The CI script reads this file automatically. Key settings:

```yaml
governance:
  # Who can make maintenance changes without ADR re-approval
  admins:
    - identity: "ivanstambuk"
      name: "Ivan Stambuk"

  # Enforce one ADR per pull request
  single_adr_per_pr: true

  # Fields that trigger full approval identity verification when changed
  substantive_fields:
    - "adr.status"
    - "adr.title"
    - "decision"
    - "alternatives"
    - "consequences"
    - "approvals"
    - "context.summary"

  # Fields that become immutable once an ADR is already accepted
  immutable_after_acceptance_fields:
    - "adr.id"
    - "adr.title"
    - "adr.summary"
    - "adr.project"
    - "adr.component"
    - "adr.priority"
    - "adr.decision_type"
    - "adr.created_at"
    - "authors"
    - "decision_owner"
    - "reviewers"
    - "context"
    - "architecturally_significant_requirements"
    - "alternatives"
    - "decision"
    - "consequences"
    - "approvals"
    - "dependencies"
```

If the config file is missing, the script uses safe defaults: no admins, no single-ADR-per-PR enforcement, the standard substantive fields list, and the standard immutable-after-acceptance field list.

> **Treat the config as a governance artefact.** Add `.adr-governance/` to your `CODEOWNERS` file so changes to the admin roster and governance rules require architecture team review.


## Troubleshooting

### Pipeline passes but PR is not gated

The pipeline and the merge gate are **separate configurations**. If your pipeline runs but PRs can still be merged when it fails:
- **GitHub:** Check Settings → Branches → Branch protection → status checks are marked as "required"
- **Azure DevOps:** Check Repos → Branches → main → Branch policies → Build Validation is set to "Required" (not "Optional")
- **GCP Cloud Build:** The Cloud Build GitHub App must be installed on the repo *and* the check must be required in GitHub branch protection
- **AWS CodeBuild:** "Report build statuses" must be enabled on the project *and* the check must be required in GitHub branch protection
- **GitLab:** Check Settings → Merge Requests → "Pipelines must succeed" is enabled

### Validator reports Python version errors

The validator requires **Python 3.11+** for:
- `datetime.fromisoformat()` with timezone support (3.11+)
- `X | Y` union type syntax in type hints (3.10+)

If your CI environment defaults to an older Python, explicitly set the version in the pipeline configuration (all provided pipeline files already do this).

### `yamllint` reports line-length warnings

The default `yamllint` line-length limit is 80 characters. This repository sets the limit to **300 characters** in [`.yamllint.yml`](../.yamllint.yml) because ADR YAML files frequently contain long prose in Markdown fields. If you want a different limit, edit [`.yamllint.yml`](../.yamllint.yml).

### Validator warnings vs. errors

Only **errors** block the merge. Governance invariants such as invalid status/audit-trail combinations, missing required terminal-status audit events, archival on non-terminal ADRs, and broken supersession symmetry now fail as hard errors. **Warnings** are advisory quality signals — for example missing `adr.summary`, missing `adr.schema_version`, premature confidence on drafts, or suspicious chronology. To change the boundary further, modify the `validate_file()` function in [`scripts/validate-adr.py`](../scripts/validate-adr.py).
