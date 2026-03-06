# CI/CD Setup Guide — ADR Validation

This guide explains how to set up automated ADR validation as a **pre-merge gate** on your CI/CD platform. Once configured, every pull request (or merge request) that touches ADR files will be automatically validated against the JSON Schema, checked for semantic consistency, and linted — **before** it can be merged.

## What Gets Validated

The validation pipeline runs three checks:

| Check | Tool | Blocks merge? |
|-------|------|:-------------:|
| **Schema compliance** | `validate-adr.py` + JSON Schema | ✅ Yes (errors) |
| **Semantic consistency** | `validate-adr.py` (built-in) | ✅ Yes (errors) / ⚠️ No (warnings) |
| **YAML formatting** | `yamllint` | ✅ Yes |

**Schema compliance** verifies every ADR YAML file conforms to the ADR meta-model (`schemas/adr.schema.json`) — correct structure, types, required fields, and enum values.

**Semantic consistency** goes beyond the schema to check logical invariants:
- `decision.chosen_alternative` matches an entry in `alternatives[].name`
- `adr.status` is consistent with `audit_trail` events (no impossible state transitions)
- `audit_trail` entries are in chronological order
- `lifecycle.supersedes` / `lifecycle.superseded_by` symmetry across files
- Duplicate ADR IDs across the ADL
- Quality signals: missing summaries, premature confidence on drafts, decision dates before creation dates

**YAML formatting** catches indentation errors, trailing whitespace, and overly long lines.

## Prerequisites

All platforms need:
- **Python 3.11+** (the validator uses `datetime.fromisoformat` improvements and `X | Y` union syntax)
- **pip packages:** `jsonschema`, `pyyaml` (for validation), `yamllint` (for linting)

The validator itself is `scripts/validate-adr.py` and the schema is `schemas/adr.schema.json` — both are included in this repository.

---

## Platform Setup

### GitHub Actions

> **Pipeline file:** [`.github/workflows/validate-adr.yml`](../.github/workflows/validate-adr.yml) (already included in this repository)

GitHub Actions is preconfigured out of the box. The only remaining step is to enable **branch protection** to enforce it as a merge gate.

#### Steps

1. **Verify the workflow exists.** The file `.github/workflows/validate-adr.yml` is already in the repository. Push it to your GitHub remote and it will start running automatically on PRs.

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

## Customization

### Changing the ADL Directory

If you rename `architecture-decision-log/` to something else (e.g., `adrs/` or `decisions/`), update the path references in:
1. The pipeline file (trigger paths and script commands)
2. `CODEOWNERS` (if using GitHub)

### Adding Additional Validation

To add custom validation rules (e.g., enforcing naming conventions, checking for required tags), modify `scripts/validate-adr.py`. The validator is designed to be extended — add your checks in the `validate_file()` function between the schema validation and the return statement.

### Removing Example Validation

If you don't want CI to validate the `examples/` directory (e.g., you've deleted it), remove the corresponding step from the pipeline file.

---

## LLM-Ready Setup Prompts

The following prompts can be **copy-pasted into any AI assistant** (ChatGPT, Claude, Gemini, Copilot, etc.) to have it set up ADR validation CI for your organization. Pick the prompt matching your platform.

---

### Prompt: GitHub Actions

```
I'm adopting the adr-governance framework (https://github.com/ivanstambuk/adr-governance) for my organization's Architecture Decision Records.

The repository already includes a GitHub Actions workflow at .github/workflows/validate-adr.yml that validates ADR YAML files against a JSON Schema on every PR.

Please help me:
1. Fork or clone the adr-governance repo into my GitHub organization.
2. Delete the examples/ directory (those are sample ADRs, not ours).
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
2. Delete the examples/ directory (those are sample ADRs, not ours).
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
2. Delete the examples/ directory (those are sample ADRs, not ours).
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
2. Delete the examples/ directory (those are sample ADRs, not ours).
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
2. Delete the examples/ directory (those are sample ADRs, not ours).
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

The default `yamllint` line-length limit is 80 characters. The pipeline configurations override this to **300 characters** because ADR YAML files frequently contain long prose in Markdown fields. If you want a different limit, edit the `yamllint` configuration in the pipeline file.

### Validator warnings vs. errors

Only **errors** block the merge. **Warnings** are advisory — they flag potential issues (e.g., missing `adr.summary` on proposed ADRs, audit trail gaps) but do not cause the pipeline to fail. To promote a warning to a hard error, modify the `validate_file()` function in `scripts/validate-adr.py`.
