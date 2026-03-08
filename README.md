# adr-governance

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Schema Version](https://img.shields.io/badge/Schema-v1.0.0-green.svg)](schemas/adr.schema.json)
[![JSON Schema Draft](https://img.shields.io/badge/JSON_Schema-Draft_2020--12-orange.svg)](https://json-schema.org/draft/2020-12/schema)
[![Format: YAML](https://img.shields.io/badge/Format-YAML-yellow.svg)](schemas/adr.schema.json)

![ADR Governance — Schema-governed, AI-native Architecture Decision Records](visuals/01-hero-overview.jpg)

A schema-governed, AI-native **Architecture Decision Record (ADR)** framework for teams that want their architectural decisions to be **structured**, **traceable**, and **asynchronous** — not debated in meetings, forgotten in Slack threads, or buried in wiki pages nobody reads.

## The Problem

Most teams make **Architecture Decisions (ADs)** every week. Few document them well. Decisions happen in meetings, context is lost the moment people leave the room, and six months later nobody can explain *why* something was built the way it was.

<details>
<summary><strong>Why current approaches fail</strong> — broken processes, no traceability, tooling that can't scale</summary>

### 1. The decision-making process is broken

- **Meetings are the wrong medium for decisions.** They reward whoever is present and articulate in the moment, not whoever has done the deepest analysis. They produce no durable artifact. They don't scale across time zones.
- **Decisions without structure are decisions without quality.** When there's no template forcing you to consider alternatives, tradeoffs, and risks, corners get cut. Important ADs get made on gut feeling.
- **Stakeholder input is ad-hoc.** The right person wasn't in the room, the email got buried, the Slack thread moved on. Decisions get made without the people most affected by them ever weighing in.
- **The process is entirely human-centric.** AI can find gaps in reasoning, check consistency across decisions, suggest alternatives the team didn't consider, and validate conclusions against broad industry knowledge. But traditional decision-making doesn't leverage any of this — it relies solely on whoever is in the room and what they happen to remember. A process that isn't AI-native today is leaving compounding value on the table, and the gap will only widen as AI capabilities improve.

### 2. Decisions aren't traceable or enforceable

- **Undocumented decisions create compliance gaps.** Auditors ask for evidence of decision-making and get blank stares. New team members have no way to understand *why* the architecture looks the way it does.
- **Documented decisions that aren't enforced are just suggestions.** Even teams that write **Architecture Decision Records (ADRs)** rarely close the loop. The decision says "use DPoP," but nothing stops someone from committing mTLS code. Without a feedback mechanism from the **Architecture Decision Log (ADL)** back to the codebase, decisions and implementation drift apart silently.
- **Decisions rot.** A decision made 18 months ago under different constraints may no longer be the right call — but nobody scheduled a review, nobody re-evaluated, and by the time someone notices, the technical debt is structural.

### 3. Traditional tooling can't scale

- **Knowledge platforms are opaque to machines.** Decisions captured in Confluence pages, SharePoint wikis, PowerPoint decks, Notion databases, or meeting minutes in Microsoft Teams can't be schema-validated, can't support programmable multi-party approval workflows, can't be diffed or version-controlled with meaningful merges, and — critically — can't be consumed by AI agents or CI pipelines for automated enforcement.
- **SDLC artifacts are ephemeral by design.** Decisions buried in Jira ticket comments, user story refinement notes, Azure DevOps work item discussions, or sprint retrospective action items *feel* tracked because they live in a managed tool. But closed tickets are rarely revisited, decisions are scattered across hundreds of issues with no index, and there's no structured way to query "what did we decide about authentication?" six months later.
- **Proprietary formats are an integration liability.** As AI becomes central to the software delivery chain, decisions locked in formats that can't be programmatically queried, validated, or fed to agents become a bottleneck. A structured, Git-native, schema-governed ADL is AI-native by design — every improvement in AI tooling automatically makes your decision management better, because the data is already in the right shape.

</details>

<details>
<summary><strong>This framework's approach</strong> — shift-left decisions, AI-native authoring, architecture knowledge management</summary>

- **Shift-left decision-making.** Instead of debating in a meeting, the proposer prepares a well-structured ADR upfront — context, alternatives, risks, tradeoffs — and submits it as a pull request. Every stakeholder can review it asynchronously, on their own time, with full context in front of them. The decision process becomes a design review, not a calendar invite. And because it's GitOps-native, every approval by every relevant stakeholder is traceable — who approved what, when, and with what context — for free.
- **AI-native by design.** A well-structured schema means AI assistants can help **author** ADRs through Socratic dialogue (probing for gaps, challenging vague rationale, surfacing unstated assumptions), **review** them before any human sees them (verifying completeness, flagging ambiguities, checking cross-reference consistency), and **enforce** them against your codebase (validating code compliance with accepted decisions in CI). The proposer doesn't fill in a template manually — they have a *conversation* with an AI assistant that interrogates them until every section is clear, complete, and internally consistent. By the time the ADR reaches a human reviewer, the low-hanging issues are already resolved. And because the data is structured, every advance in AI capability automatically improves your decision-making — better models mean sharper reviews, deeper gap analysis, and the ability to revisit your entire decision log against new information at scale.
- **Architecture Knowledge Management (AKM).** Decisions are first-class engineering artifacts — not afterthoughts. Each AD is captured as an ADR, and the collection of all ADRs for a project forms the ADL — the `architecture-decision-log/` directory in this repository. This framework gives you the tooling and governance process to build an ADL that is schema-validated, Git-governed, AI-assisted, and auditable.

</details>

## What This Provides

<details>
<summary><strong>Schema, governance, validation, CI/CD, AI authoring, decision enforcement, and more</strong></summary>

- **JSON Schema** (Draft 2020-12) defining the complete ADR meta-model — every field, enum, and constraint
- **GitOps-based governance process** — ADR status transitions happen through Git commits and pull requests, not manual coordination
- **Validation tooling** — a Python validator that checks schema compliance, referential integrity, and semantic consistency on every PR
- **Pre-built CI/CD pipelines** for GitHub Actions, Azure DevOps, GCP Cloud Build, AWS CodeBuild, and GitLab CI — ready to copy into your repo and enforce as a merge gate
- **Approval identity enforcement** — out-of-the-box on GitHub Actions, Azure DevOps, and GitLab CI; AWS/GCP templates ship the verifier in dry-run mode until you add custom PR metadata wiring. This creates an auditable link between ADR approvals and Git platform approvals where the platform integration supports it
- **Governance rules** — configurable single-ADR-per-PR enforcement, substantive vs. maintenance change classification, and admin roster metadata — all defined in a platform-agnostic [`.adr-governance/config.yaml`](.adr-governance/config.yaml)
- **LLM-ready setup prompts** — copy-paste prompts for AI assistants to set up CI for your platform in minutes
- [`llms.txt`](llms.txt) + [`llms-full.txt`](llms-full.txt) — Machine-readable project summaries for AI assistants ([llms.txt convention](https://llmstxt.org/)). `llms.txt` provides a concise overview with links; `llms-full.txt` embeds a curated inline documentation set for context injection
- **Agent Skill** ([agentskills.io](https://agentskills.io) spec) for AI-assisted ADR authoring and review — works with Google Antigravity, Claude Code, VS Code Copilot, and any conforming agent. The skill knows the schema and the governance process, and will guide you through every field interactively
- **Decision enforcement** — the ADL YAML is the source of truth for Spec-Driven Development (SDD): AI coding agents can search the bundled ADL for context, and CI pipelines can validate compliance before merge using the repo's ADR YAML plus scripts such as `extract-decisions.py`
- **Repomix bundling** — the schema, ADR corpus, core authoring docs, skill assets, and validator guidance are concatenated into a single Markdown file that chat-based and coding agents can search with standard tools
- **Example ADRs** from a fictional IAM department (NovaTrust Financial Services) in [`examples-reference/`](examples-reference/) — real-world contended decisions with sizable pros and cons on each side, not strawman examples. Kept as a reference for quality and style; not real decisions

</details>

## Philosophy

Every ADR is **self-contained**. All context, **Architecturally Significant Requirements (ASRs)**, alternatives, consequences, and audit trails are embedded directly in the YAML file. There are no foreign-key dependencies between ADRs — the only explicit link is the `lifecycle.supersedes` / `superseded_by` chain for replacements. An ADR can *mention* other ADR IDs in prose, but it must be fully understandable on its own.

The ADL is an **append-only decision log**. ADRs are never deleted — they transition through a governed lifecycle. Rejected and superseded ADRs remain as historical records, preserving the decision-making trail for auditors, new team members, and your future self.

## ADR Lifecycle

Every ADR follows a governed state machine. All transitions happen through pull requests.

![ADR Lifecycle — Governed State Machine](visuals/02-lifecycle-state-machine.jpg)

See [`docs/adr-process.md`](docs/adr-process.md) for the full normative governance process, including review checklists, the Architectural Significance Test, branch protection rules, and CODEOWNERS configuration.

## AI-Assisted Authoring & Pre-Review

![AI-Native ADR Authoring — From Intent to Governed Decision](visuals/03-ai-socratic-authoring.jpg)

ADRs are not meant to be filled in manually like a form. The framework supports **two creation modes**:

- **Socratic interview** (default) — The AI walks you through every section via interactive questioning, probing for gaps, challenging weak rationale, and surfacing missing edge cases. Best when starting from scratch.
- **Artifact-driven** — Upload existing materials (meeting transcripts, PowerPoint slides, PDFs, design documents, architecture diagrams, images, email threads, etc.) and the AI extracts an ADR from them automatically, asking targeted questions only for what's missing. Best when the decision has already been discussed and context exists in documents.

This is a fundamental shift: instead of the proposer writing a draft in isolation and scheduling a meeting to "walk through" it (where reviewers discover ambiguities in real time), the AI assistant resolves those ambiguities *before the first human reviewer ever sees the document*.

The framework provides two paths to both modes:

- **Agent Skill** ([`.skills/adr-author/`](.skills/adr-author/)) — works with Google Antigravity, Claude Code, VS Code Copilot, and any [agentskills.io](https://agentskills.io)-conforming agent. The skill knows the full meta-model and governance lifecycle, and supports both interactive and artifact-driven authoring.
- **Web Chat** — upload the Repomix bundle (`adr-governance-bundle.md`) to any web-based AI chat (ChatGPT, Claude.ai, Gemini, Copilot). The bundle carries the schema, ADR corpus, core authoring docs, skill assets, and validator guidance; local validation and CI remain the final authority after you paste the YAML into your repo. For artifact-driven mode, upload the bundle plus your documents together. See [`docs/web-chat-quickstart.md`](docs/web-chat-quickstart.md).

A **pre-review quality gate** ([`scripts/review-adr.py`](scripts/review-adr.py)) generates a structured AI review prompt that covers semantic clarity, completeness, logical consistency, assumption risks, and cross-reference consistency. The result: human reviewers receive ADRs that are already coherent — review meetings become strategic discussions about the *decision*, not debugging sessions about what the proposer meant.

See **[`docs/ai-authoring.md`](docs/ai-authoring.md)** for agent skill setup, web chat quickstart, pre-review usage, and stakeholder summaries.


## ADL as Source of Truth

![ADL Enforcement Loop — Closing the Gap Between Decisions and Code](visuals/04-adl-enforcement-loop.jpg)

The Architecture Decision Log isn't just documentation — it's a **machine-readable specification** that AI agents and CI pipelines can enforce against your codebase. This closes the gap between *deciding* and *doing*.

- **Spec-Driven Development (SDD)** — AI coding agents can use the bundled ADL as a single source of truth during code generation. When the ADL says "use DPoP for sender-constrained tokens," the agent searches the bundled decision log, finds the decision with its full rationale and constraints, and generates code that aligns with it — without the developer having to explain the context in every prompt.
- **Semantic guardrails in CI** — the ADL can serve as a pre-merge guardrail in your *code* repositories. A CI step extracts active decisions, generates an LLM compliance prompt with the code diff, and flags architectural drift before merge.
- **Cross-repository enforcement** — the ADL repo and the code repo don't need to be the same. Point your agent at the ADL bundle from any repository. The decisions are self-contained.

| Scenario | Without ADL enforcement | With ADL enforcement |
|----------|------------------------|---------------------|
| New developer joins | Reads (or doesn't read) wiki docs | Agent has full ADL context; generates compliant code from day one |
| PR introduces mTLS | Merges — nobody notices the ADR says DPoP | CI flags the drift; reviewer is alerted |
| Architect proposes supersession | Searches Slack history for context | Searches the ADL bundle; full decision chain is traceable |
| Annual audit | Scramble to reconstruct decision history | ADL is the audit trail; every decision is timestamped, attributed, and version-controlled |
| LLM generates code | Guesses at patterns based on training data | Searches the ADL and follows your organization's actual decisions |

See **[`docs/decision-enforcement.md`](docs/decision-enforcement.md)** for SDD workflow, CI pipeline examples, decision extraction CLI, and Repomix bundle details.

## Quick Start — Adopting for Your Organization

> **⚡ Fastest path.** Paste the prompt below into any AI coding assistant (Codex, Claude Code, Antigravity, Copilot) to have it set up the entire framework for your organization in one shot. For manual step-by-step instructions, skip to [Manual Setup](#manual-setup).

```
I'm adopting the adr-governance framework (https://github.com/ivanstambuk/adr-governance) for my organization.

Please help me:
1. Fork or clone the repo into my organization as a new repository named "architecture-decisions".
2. Delete the examples-reference/ directory (those are fictional reference ADRs).
3. Update ADR-0000 (architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml):
   - Replace authors, decision_owner, reviewers, and approvals with my name/identity
   - Update adr.project to my organization name
   - Update timestamps and audit trail entries
4. Set up CI validation as a required merge gate for my platform.
5. Enable the pre-commit hook (git config core.hooksPath .githooks).
6. Configure CODEOWNERS with my team handle.
7. Verify the setup by creating a test branch with an intentionally malformed ADR and opening a PR to confirm the check fails.

My organization name is: [INSERT ORG NAME]
My CI platform is: [GitHub Actions / Azure DevOps / GCP Cloud Build / AWS CodeBuild / GitLab CI]
My architecture team handle is: [INSERT TEAM HANDLE, e.g., @myorg/architects]
My name is: [INSERT YOUR NAME]
My Git identity is: [INSERT YOUR GIT USERNAME]
```

---

<details>
<summary><h3>Manual Setup</h3> <em>If you used the AI prompt above, skip this section.</em></summary>

#### 1. Create your ADR repository

Create a new repository in your organization and clone this framework into it:

```bash
# Create a new repo in your org (GitHub example)
gh repo create your-org/architecture-decisions --private --clone

# Pull the framework into it
cd architecture-decisions
git remote add upstream https://github.com/ivanstambuk/adr-governance.git
git pull upstream main
git remote remove upstream
git push origin main
```

Or fork the repository directly from GitHub and rename it.

#### 2. Review examples *(optional cleanup)*

The [`examples-reference/`](examples-reference/) directory contains 8 fictional ADRs from "NovaTrust Financial Services" — they demonstrate the meta-model at production quality. **These are not real decisions.** You can:

- **Keep them** as a reference for your team (recommended initially)
- **Delete them** once your team is comfortable with the format:
  ```bash
  rm -rf examples-reference/
  git add -A && git commit -m "chore: remove reference examples"
  ```

By default, the shipped validation flow validates `architecture-decision-log/` and `examples-reference/` separately, so keeping the reference set does **not** reserve ADR IDs in your live corpus. If you explicitly validate both directories in a single `python3 scripts/validate-adr.py ...` invocation, they share one duplicate-ID and cross-reference namespace for that run.

#### 3. Customize ADR-0000

[`architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml`](architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml) is the **meta-ADR** — it documents the decision to adopt this governance framework. Update it for your organization:

- Replace the `authors`, `decision_owner`, `reviewers`, and `approvals` names and identities
- Update `adr.project` to your project or organisation name
- Update timestamps and audit trail entries
- Adjust the `context.description` if your adoption rationale differs

#### 4. Set up CI

Copy the pipeline file for your platform to the repository root:

| Platform | Copy from | Copy to |
|----------|-----------|---------|
| **GitHub Actions** | Already at [`.github/workflows/validate-adr.yml`](.github/workflows/validate-adr.yml) | *(nothing to do)* |
| Azure DevOps | [`ci/azure-devops/azure-pipelines.yml`](ci/azure-devops/azure-pipelines.yml) | `azure-pipelines.yml` |
| GCP Cloud Build | [`ci/gcp-cloud-build/cloudbuild.yaml`](ci/gcp-cloud-build/cloudbuild.yaml) | `cloudbuild.yaml` |
| AWS CodeBuild | [`ci/aws-codebuild/buildspec.yml`](ci/aws-codebuild/buildspec.yml) | `buildspec.yml` |
| GitLab CI | [`ci/gitlab-ci/.gitlab-ci.yml`](ci/gitlab-ci/.gitlab-ci.yml) | `.gitlab-ci.yml` |

Then configure branch protection to make the CI check a **required merge gate** — see **[`docs/ci-setup.md`](docs/ci-setup.md)** for platform-specific instructions and LLM-ready setup prompts.

#### 5. Enable the pre-commit hook

```bash
git config core.hooksPath .githooks
```

This activates automatic Markdown rendering — every commit that touches `architecture-decision-log/*.yaml` will regenerate the human-friendly files in `architecture-decision-log/rendered/` and the decision log index. Both the YAML source and its Markdown rendering are committed together, so reviewers approve both in the same PR.

#### 6. Configure CODEOWNERS *(optional but recommended)*

```bash
cp CODEOWNERS.example .github/CODEOWNERS
```

Edit `.github/CODEOWNERS` to replace the placeholder team handles (`@org/architecture-team`, etc.) with your real GitHub teams. This ensures ADRs and schema changes automatically request review from the right people.

#### 7. Copy the Agent Skill to your code repositories *(optional)*

The [`.skills/adr-author/`](.skills/adr-author/) directory is a portable AI skill. Copy it to any repository where developers will be authoring ADRs — agents like Antigravity, Claude Code, and Copilot will pick it up automatically and guide ADR creation through interactive questioning.

#### 8. Create your first real ADR

Use an AI assistant with the `adr-author` skill — it will guide you through every field via Socratic dialogue:

```
"I need to create a new ADR for [your decision]. Guide me through it."
```

Alternatively, if you have existing materials (meeting transcripts, slides, design documents), provide them to the AI and ask it to extract an ADR:

```
"Here are my meeting notes and architecture slides. Generate an ADR from these documents."
```

The AI will analyze your documents, present a structured extraction summary, and ask targeted questions only for what's missing.

Or copy the template manually:

```bash
cp .skills/adr-author/assets/adr-template.yaml \
   architecture-decision-log/ADR-0001-your-decision-title.yaml
```

#### 9. Validate and submit

```bash
# Install dependencies
pip install "jsonschema[format]" pyyaml yamllint

# Validate schema + semantic consistency
python3 scripts/validate-adr.py architecture-decision-log/ADR-0001-your-decision-title.yaml

# Pre-review quality gate (pipe to your LLM for Socratic feedback)
python3 scripts/review-adr.py architecture-decision-log/ADR-0001-your-decision-title.yaml

# Open a PR — CI validates automatically
git checkout -b adr/ADR-0001-your-decision-title
git add architecture-decision-log/ADR-0001-your-decision-title.yaml
git commit -m "feat(adr): ADR-0001 your decision title"
git push origin adr/ADR-0001-your-decision-title
```

The CI pipeline validates schema compliance and lints the YAML. Reviewers are auto-assigned via CODEOWNERS. On GitHub Actions, Azure DevOps, and GitLab CI, the shipped setup can also verify approval identities; AWS/GCP require custom PR metadata and base-ref wiring for that check to be enforceable instead of advisory. The PR becomes the decision forum — all discussion, feedback, and approval happens asynchronously in the PR thread.

</details>

## ADR Meta-Model

Each ADR YAML file captures a single **architecturally significant** decision — not every design choice, but the ones that shape the system's structure, quality attributes, and long-term constraints. Each file contains these sections:

| Section | Required | Description |
|---------|:--------:|-------------|
| `adr` | ✅ | ID, title, status, Y-Statement, timestamps, project, tags, priority, decision type, decision level (`strategic` / `tactical` / `operational`), schema version |
| `authors` | ✅ | Who drafted the ADR |
| `decision_owner` | ✅ | Single accountable person |
| `context` | ✅ | Problem description (Markdown), business/technical drivers, constraints, assumptions |
| `alternatives` | ✅ | ≥2 alternatives with description (Markdown), pros, cons, cost, risk, rejection rationale |
| `decision` | ✅ | Chosen alternative, rationale (Markdown), tradeoffs (Markdown), date, confidence |
| `consequences` | ✅ | Positive and negative outcomes |
| `confirmation` | ✅ | How the decision's implementation will be verified; artifact IDs (optional, backfilled later) |
| `reviewers` | | People who reviewed |
| `approvals` | | Formal approvals with timestamps and platform identities for CI verification |
| `architecturally_significant_requirements` | | **Architecturally Significant Requirements (ASRs)** — quality attributes, architectural constraints, and non-functional requirements that drove this decision. Not feature-level requirements |
| `dependencies` | | Internal and external dependencies |
| `references` | | External references, standards, evidence |
| `lifecycle` | | Review cadence, supersession chain, archival |
| `audit_trail` | | Immutable append-only event log |

> **Y-Statement** — the `adr.y_statement` field captures the full decision in a single sentence using the 7-clause Zimmermann/Fairbanks format: *"In the context of…, facing…, we decided for… and neglected…, to achieve…, accepting…, because…"*. Optional for `draft`/`proposed`; mandatory for `accepted` ADRs. Target length: 100–150 words.
>
> **Markdown-native fields** support full Markdown including embedded Mermaid diagrams via code fences. Use YAML literal block scalars (`|`) for multiline content.

## CI/CD Setup

Automated validation is the enforcement mechanism that makes the governance process real. Without it, the schema is a suggestion; with it, the schema is a contract.

**GitHub Actions** is preconfigured — the workflow at [`.github/workflows/validate-adr.yml`](.github/workflows/validate-adr.yml) runs on every PR and every push to `main`. It intentionally avoids narrow path filters so governance/tooling changes cannot bypass CI. You just need to [enable branch protection](docs/ci-setup.md#github-actions) to make it a merge gate.

**Other platforms** have ready-to-use pipeline files in the `ci/` directory:

| Platform | Pipeline file | Copy to |
|----------|---------------|---------|
| Azure DevOps | [`ci/azure-devops/azure-pipelines.yml`](ci/azure-devops/azure-pipelines.yml) | `azure-pipelines.yml` (repo root) |
| GCP Cloud Build | [`ci/gcp-cloud-build/cloudbuild.yaml`](ci/gcp-cloud-build/cloudbuild.yaml) | `cloudbuild.yaml` (repo root) |
| AWS CodeBuild | [`ci/aws-codebuild/buildspec.yml`](ci/aws-codebuild/buildspec.yml) | `buildspec.yml` (repo root) |
| GitLab CI | [`ci/gitlab-ci/.gitlab-ci.yml`](ci/gitlab-ci/.gitlab-ci.yml) | `.gitlab-ci.yml` (repo root) |

**Step-by-step setup instructions**, platform-specific enforcement configuration, troubleshooting, and **LLM-ready prompts** (copy-paste into any AI assistant to have it set up CI for you) are in **[`docs/ci-setup.md`](docs/ci-setup.md)**.

## Rendered Markdown (Human-Friendly Views)

ADRs are authored and stored as **structured YAML** — optimised for machine consumption, validation, and AI-assisted workflows. But humans need a readable format too. Every ADR YAML file has a corresponding **Markdown rendering** in [`architecture-decision-log/rendered/`](architecture-decision-log/rendered/), auto-generated via a Git pre-commit hook. Both the YAML source and its Markdown rendering are committed together — reviewers approve both in the same PR, and CI verifies that committed renderings and `llms-full.txt` stay current.

- **[`architecture-decision-log/rendered/architecture-decision-log.md`](architecture-decision-log/rendered/architecture-decision-log.md)** — the decision log index with status, dates, and clickable links
- **`architecture-decision-log/rendered/ADR-NNNN-*.md`** — individual ADR renderings with a provenance disclaimer

> **⚠️ Do not edit files in `architecture-decision-log/rendered/` directly.** They are auto-generated from the YAML source.

See **[`docs/rendering.md`](docs/rendering.md)** for pre-commit hook setup, manual rendering commands, CI freshness checks, and the rationale behind the dual-format model.


## Example ADRs

The [`examples-reference/`](examples-reference/) directory contains example ADRs organized in two categories:

### Fictional Examples

Interconnected ADRs from a **fictional** IAM department at NovaTrust Financial Services. These are **not real decisions** — they demonstrate the meta-model at production quality. Use them as a reference for style, depth, and interconnection:

| ID | Decision | Rendered | Source |
|----|----------|:--------:|:------:|
| ADR-0001 | Use DPoP over mTLS for Sender-Constrained Tokens | [Markdown](examples-reference/rendered/ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.md) | [YAML](examples-reference/fictional/ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.yaml) |
| ADR-0002 | Use Reference Tokens over JWTs for Gateway Introspection | [Markdown](examples-reference/rendered/ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.md) | [YAML](examples-reference/fictional/ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.yaml) |
| ADR-0003 | Use Pairwise Subject Identifiers for OIDC Relying Parties | [Markdown](examples-reference/rendered/ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.md) | [YAML](examples-reference/fictional/ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.yaml) |
| ADR-0004 | Use Ed25519 over RSA-2048 for JWT Signing Keys | [Markdown](examples-reference/rendered/ADR-0004-ed25519-over-rsa-for-jwt-signing.md) | [YAML](examples-reference/fictional/ADR-0004-ed25519-over-rsa-for-jwt-signing.yaml) |
| ADR-0005 | Use BFF Token Mediator for SPA Token Acquisition | [Markdown](examples-reference/rendered/ADR-0005-bff-token-mediator-for-spa-token-acquisition.md) | [YAML](examples-reference/fictional/ADR-0005-bff-token-mediator-for-spa-token-acquisition.yaml) |
| ADR-0006 | Use Session Enrichment for Step-Up Authentication Proof | [Markdown](examples-reference/rendered/ADR-0006-session-enrichment-for-step-up-authentication.md) | [YAML](examples-reference/fictional/ADR-0006-session-enrichment-for-step-up-authentication.yaml) |
| ADR-0007 | Reject Centralized HashiCorp Vault for API Runtime Secrets | [Markdown](examples-reference/rendered/ADR-0007-centralized-secret-store-for-api-keys.md) | [YAML](examples-reference/fictional/ADR-0007-centralized-secret-store-for-api-keys.yaml) |
| ADR-0008 | Defer OpenID Federation for Automated Trust Establishment | [Markdown](examples-reference/rendered/ADR-0008-defer-openid-federation-for-trust-establishment.md) | [YAML](examples-reference/fictional/ADR-0008-defer-openid-federation-for-trust-establishment.yaml) |

### Real-World Examples

Reverse-engineered ADRs from prominent open-source projects. These reconstruct real architectural decisions using publicly available design documents, RFCs, and community discussions, organized by decision level:

#### Strategic Decisions (ADR-0100 – ADR-0104)

| ID | Project | Decision | Rendered | Source |
|----|---------|----------|:--------:|:------:|
| ADR-0100 | **TypeScript** | Rewrite compiler in Go | [Markdown](examples-reference/rendered/ADR-0100-typescript-compiler-go-rewrite.md) | [YAML](examples-reference/real-world/ADR-0100-typescript-compiler-go-rewrite.yaml) |
| ADR-0101 | **Kubernetes** | Deprecate dockershim for CRI | [Markdown](examples-reference/rendered/ADR-0101-kubernetes-dockershim-deprecation.md) | [YAML](examples-reference/real-world/ADR-0101-kubernetes-dockershim-deprecation.yaml) |
| ADR-0102 | **React** | Server Components (RFC 0188) | [Markdown](examples-reference/rendered/ADR-0102-react-server-components.md) | [YAML](examples-reference/real-world/ADR-0102-react-server-components.yaml) |
| ADR-0103 | **Go** | Add generics via type parameters | [Markdown](examples-reference/rendered/ADR-0103-go-generics.md) | [YAML](examples-reference/real-world/ADR-0103-go-generics.yaml) |
| ADR-0104 | **Rust** | Async/await with stackless coroutines | [Markdown](examples-reference/rendered/ADR-0104-rust-async-await.md) | [YAML](examples-reference/real-world/ADR-0104-rust-async-await.yaml) |

#### Tactical Decisions (ADR-0105 – ADR-0109)

| ID | Project | Decision | Rendered | Source |
|----|---------|----------|:--------:|:------:|
| ADR-0105 | **Vue.js** | Composition API (RFC-0013) | [Markdown](examples-reference/rendered/ADR-0105-vue-composition-api.md) | [YAML](examples-reference/real-world/ADR-0105-vue-composition-api.yaml) |
| ADR-0106 | **ESLint** | Flat config system | [Markdown](examples-reference/rendered/ADR-0106-eslint-flat-config.md) | [YAML](examples-reference/real-world/ADR-0106-eslint-flat-config.yaml) |
| ADR-0107 | **Vite** | Rolldown unification | [Markdown](examples-reference/rendered/ADR-0107-vite-rolldown-unification.md) | [YAML](examples-reference/real-world/ADR-0107-vite-rolldown-unification.yaml) |
| ADR-0108 | **Svelte** | Runes reactivity system | [Markdown](examples-reference/rendered/ADR-0108-svelte-runes-reactivity.md) | [YAML](examples-reference/real-world/ADR-0108-svelte-runes-reactivity.yaml) |
| ADR-0109 | **Next.js** | Turbopack adoption | [Markdown](examples-reference/rendered/ADR-0109-nextjs-turbopack-adoption.md) | [YAML](examples-reference/real-world/ADR-0109-nextjs-turbopack-adoption.yaml) |

#### Operational Decisions (ADR-0110 – ADR-0114)

| ID | Project | Decision | Rendered | Source |
|----|---------|----------|:--------:|:------:|
| ADR-0110 | **Node.js** | Built-in test runner | [Markdown](examples-reference/rendered/ADR-0110-nodejs-built-in-test-runner.md) | [YAML](examples-reference/real-world/ADR-0110-nodejs-built-in-test-runner.yaml) |
| ADR-0111 | **Python** | pyproject.toml (PEP 621) | [Markdown](examples-reference/rendered/ADR-0111-python-pyproject-toml.md) | [YAML](examples-reference/real-world/ADR-0111-python-pyproject-toml.yaml) |
| ADR-0112 | **Docker** | Container base image selection | [Markdown](examples-reference/rendered/ADR-0112-container-base-image-selection.md) | [YAML](examples-reference/real-world/ADR-0112-container-base-image-selection.yaml) |
| ADR-0113 | **pnpm** | Content-addressable store | [Markdown](examples-reference/rendered/ADR-0113-pnpm-content-addressable-store.md) | [YAML](examples-reference/real-world/ADR-0113-pnpm-content-addressable-store.yaml) |
| ADR-0114 | **Deno** | npm compatibility layer | [Markdown](examples-reference/rendered/ADR-0114-deno-npm-compatibility.md) | [YAML](examples-reference/real-world/ADR-0114-deno-npm-compatibility.yaml) |

See the [rendered example index](examples-reference/rendered/architecture-decision-log.md) for a full overview, or [`examples-reference/README.md`](examples-reference/README.md) for details on each example.

Additionally, [`architecture-decision-log/ADR-0000`](architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml) is a meta-ADR documenting the AD to adopt this governance process itself.

> **Bootstrap exception:** ADR-0000 was self-approved by the initial author as the bootstrapping meta-decision. The "no self-approval" rule (§3.4) applies to all subsequent ADRs.

## Automated Quality Testing (Triple-LLM Harness)

The framework includes an automated testing harness ([`tests/llm_harness.py`](tests/llm_harness.py)) that validates ADR authoring quality by simulating realistic authoring conversations between three LLMs:

| Role | Purpose | Default Model |
|------|---------|---------------|
| **Interviewer** | Runs the Socratic ADR authoring dialogue | GPT-5.2 Medium |
| **User** | Plays a domain expert answering questions | GLM-5 |
| **Analyst** | Reviews the generated ADR for quality | GPT-5.4 High |

### How It Works

1. A YAML **scenario** defines the decision context, persona, and expected coverage
2. The **Interviewer** and **User** LLMs conduct a multi-turn ADR authoring conversation
3. The resulting ADR YAML is **validated** against the schema and **reviewed** by the Analyst LLM
4. Quality metrics are computed: schema compliance, field completeness, Y-Statement presence, ASR coverage

### Running the Harness

```bash
# Install dependencies
pip install google-genai anthropic pyyaml jsonschema

# Run a single scenario
python3 tests/llm_harness.py tests/scenarios/fictional-001-api-versioning.yaml

# Run all scenarios (results go to tests/llm_runs/)
python3 tests/llm_harness.py tests/scenarios/*.yaml
```

### Scenario Categories

| Category | Description | Examples |
|----------|-------------|---------|
| **Fictional** | Synthetic decision contexts | API versioning, monolith decomposition, secrets management |
| **GitHub PR-based** | Extracted from real PRs | *(planned)* |
| **Existing ADR-based** | Round-trip validation against reference ADRs | *(planned)* |

See [`docs/research/automated-triple-llm-testing.md`](docs/research/automated-triple-llm-testing.md) for the full design document.

## License

MIT
