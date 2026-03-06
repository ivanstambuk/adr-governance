# adr-governance

A schema-governed, AI-native **Architecture Decision Record (ADR)** framework for teams that want their architectural decisions to be **structured**, **traceable**, and **asynchronous** — not debated in meetings, forgotten in Slack threads, or buried in wiki pages nobody reads.

## The Problem

Most teams make **Architecture Decisions (ADs)** every week. Few document them well. Decisions happen in meetings, context is lost the moment people leave the room, and six months later nobody can explain *why* something was built the way it was.

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

### This framework's approach

**Shift-left decision-making.** Instead of debating in a meeting, the proposer prepares a well-structured ADR upfront — context, alternatives, risks, tradeoffs — and submits it as a pull request. Every stakeholder can review it asynchronously, on their own time, with full context in front of them. The decision process becomes a design review, not a calendar invite. And because it's GitOps-native, every approval by every relevant stakeholder is traceable — who approved what, when, and with what context — for free.

**AI-native by design.** A well-structured schema means AI assistants can help **author** ADRs through Socratic dialogue (probing for gaps, challenging vague rationale, surfacing unstated assumptions), **review** them before any human sees them (verifying completeness, flagging ambiguities, checking cross-reference consistency), and **enforce** them against your codebase (validating code compliance with accepted decisions in CI). The proposer doesn't fill in a template manually — they have a *conversation* with an AI assistant that interrogates them until every section is clear, complete, and internally consistent. By the time the ADR reaches a human reviewer, the low-hanging issues are already resolved. And because the data is structured, every advance in AI capability automatically improves your decision-making — better models mean sharper reviews, deeper gap analysis, and the ability to revisit your entire decision log against new information at scale.

**Architecture Knowledge Management (AKM).** Decisions are first-class engineering artifacts — not afterthoughts. Each AD is captured as an ADR, and the collection of all ADRs for a project forms the ADL — the `architecture-decision-log/` directory in this repository. This framework gives you the tooling and governance process to build an ADL that is schema-validated, Git-governed, AI-assisted, and auditable.

## What This Provides

- **JSON Schema** (Draft 2020-12) defining the complete ADR meta-model — every field, enum, and constraint
- **GitOps-based governance process** — ADR status transitions happen through Git commits and pull requests, not manual coordination
- **Validation tooling** — a Python validator that checks schema compliance, referential integrity, and semantic consistency on every PR
- **Pre-built CI/CD pipelines** for GitHub Actions, Azure DevOps, GCP Cloud Build, AWS CodeBuild, and GitLab CI — ready to copy into your repo and enforce as a merge gate
- **Approval identity enforcement** — CI verifies that the people listed in `approvals[]` have actually approved the pull request, creating an auditable link between ADR approvals and Git platform approvals
- **Governance rules** — configurable single-ADR-per-PR enforcement, substantive vs. maintenance change classification, and admin overrides — all defined in a platform-agnostic [`.adr-governance/config.yaml`](.adr-governance/config.yaml)
- **LLM-ready setup prompts** — copy-paste prompts for AI assistants to set up CI for your platform in minutes
- `llms.txt` — Machine-readable project summary for AI assistants ([llms.txt convention](https://llmstxt.org/))
- **Agent Skill** ([agentskills.io](https://agentskills.io) spec) for AI-assisted ADR authoring and review — works with Google Antigravity, Claude Code, VS Code Copilot, and any conforming agent. The skill knows the schema and the governance process, and will guide you through every field interactively
- **Decision enforcement** — the ADL can serve as a single source of truth for Spec-Driven Development (SDD): AI coding agents can search the bundled ADL to align code with architectural decisions, and CI pipelines can validate compliance before merge
- **Repomix bundling** — the entire ADL is concatenated into a single Markdown file that agents can search with standard tools, enabling cross-repository decision enforcement
- **Example ADRs** from a fictional IAM department (NovaTrust Financial Services) in [`examples-reference/`](examples-reference/) — real-world contended decisions with sizable pros and cons on each side, not strawman examples. Kept as a reference for quality and style; not real decisions

## Philosophy

Every ADR is **self-contained**. All context, Architecturally Significant Requirements (ASRs), alternatives, consequences, and audit trails are embedded directly in the YAML file. There are no foreign-key dependencies between ADRs — the only explicit link is the `lifecycle.supersedes` / `superseded_by` chain for replacements. An ADR can *mention* other ADR IDs in prose, but it must be fully understandable on its own.

The ADL is an **append-only decision log**. ADRs are never deleted — they transition through a governed lifecycle. Rejected and superseded ADRs remain as historical records, preserving the decision-making trail for auditors, new team members, and your future self.

## ADR Lifecycle

Every ADR follows a governed state machine. All transitions happen through pull requests.

```mermaid
stateDiagram-v2
    [*] --> draft

    draft --> proposed : Open PR

    proposed --> proposed : Rework (changes requested)
    proposed --> accepted : Approved → PR merged
    proposed --> rejected : Rejected → PR merged
    proposed --> deferred : Postponed → PR closed

    deferred --> proposed : Reopened

    accepted --> superseded : Replaced by new ADR
    accepted --> deprecated : No longer recommended

    rejected --> [*]
    deferred --> [*]
    superseded --> [*]
    deprecated --> [*]
```

> **Why are rejected ADRs merged?** They are part of the ADL — they document *why* an option was evaluated and not pursued. Closing the PR without merging would lose this history from `main`.

> **Where is `archived`?** Archival is **not a status value** — it is a metadata overlay. Archived ADRs retain their pre-archival status (`superseded`, `deprecated`, or `rejected`) and are annotated with `lifecycle.archival.archived_at` and `lifecycle.archival.archive_reason` fields, plus an `archived` event in `audit_trail`. See [§8 Archival](docs/adr-process.md#8-archival) for the full workflow.

See [`docs/adr-process.md`](docs/adr-process.md) for the full normative governance process, including review checklists, the Architectural Significance Test, branch protection rules, and CODEOWNERS configuration.

## Quick Start — Adopting for Your Organization

### 1. Create your ADR repository

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

### 2. Review examples *(optional cleanup)*

The [`examples-reference/`](examples-reference/) directory contains 8 fictional ADRs from "NovaTrust Financial Services" — they demonstrate the meta-model at production quality. **These are not real decisions.** You can:

- **Keep them** as a reference for your team (recommended initially)
- **Delete them** once your team is comfortable with the format:
  ```bash
  rm -rf examples-reference/
  git add -A && git commit -m "chore: remove reference examples"
  ```

### 3. Customize ADR-0000

[`architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml`](architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml) is the **meta-ADR** — it documents the decision to adopt this governance framework. Update it for your organization:

- Replace the `authors`, `decision_owner`, `reviewers`, and `approvals` names and identities
- Update `adr.project` to your project or organisation name
- Update timestamps and audit trail entries
- Adjust the `context.summary` if your adoption rationale differs

### 4. Set up CI

Copy the pipeline file for your platform to the repository root:

| Platform | Copy from | Copy to |
|----------|-----------|---------|
| **GitHub Actions** | Already at [`.github/workflows/validate-adr.yml`](.github/workflows/validate-adr.yml) | *(nothing to do)* |
| Azure DevOps | [`ci/azure-devops/azure-pipelines.yml`](ci/azure-devops/azure-pipelines.yml) | `azure-pipelines.yml` |
| GCP Cloud Build | [`ci/gcp-cloud-build/cloudbuild.yaml`](ci/gcp-cloud-build/cloudbuild.yaml) | `cloudbuild.yaml` |
| AWS CodeBuild | [`ci/aws-codebuild/buildspec.yml`](ci/aws-codebuild/buildspec.yml) | `buildspec.yml` |
| GitLab CI | [`ci/gitlab-ci/.gitlab-ci.yml`](ci/gitlab-ci/.gitlab-ci.yml) | `.gitlab-ci.yml` |

Then configure branch protection to make the CI check a **required merge gate** — see **[`docs/ci-setup.md`](docs/ci-setup.md)** for platform-specific instructions and LLM-ready setup prompts.

### 5. Enable the pre-commit hook

```bash
git config core.hooksPath .githooks
```

This activates automatic Markdown rendering — every commit that touches `architecture-decision-log/*.yaml` will regenerate the human-friendly files in `rendered/` and the decision log index. Both the YAML source and its Markdown rendering are committed together, so reviewers approve both in the same PR.

### 6. Configure CODEOWNERS *(optional but recommended)*

```bash
cp CODEOWNERS.example .github/CODEOWNERS
```

Edit `.github/CODEOWNERS` to replace the placeholder team handles (`@org/architecture-team`, etc.) with your real GitHub teams. This ensures ADRs and schema changes automatically request review from the right people.

### 7. Copy the Agent Skill to your code repositories *(optional)*

The [`.skills/adr-author/`](.skills/adr-author/) directory is a portable AI skill. Copy it to any repository where developers will be authoring ADRs — agents like Antigravity, Claude Code, and Copilot will pick it up automatically and guide ADR creation through interactive questioning.

### 8. Create your first real ADR

Use an AI assistant with the `adr-author` skill — it will guide you through every field via Socratic dialogue:

```
"I need to create a new ADR for [your decision]. Guide me through it."
```

Or copy the template manually:

```bash
cp .skills/adr-author/assets/adr-template.yaml \
   architecture-decision-log/ADR-0001-your-decision-title.yaml
```

### 9. Validate and submit

```bash
# Install dependencies
pip install jsonschema pyyaml yamllint

# Validate schema + semantic consistency
python3 scripts/validate-adr.py architecture-decision-log/ADR-0001-your-decision-title.yaml

# Pre-review quality gate (pipe to your LLM for Socratic feedback)
python3 scripts/review-adr.py architecture-decision-log/ADR-0001-your-decision-title.yaml

# Open a PR — CI validates automatically
git checkout -b adr/0001-your-decision-title
git add architecture-decision-log/ADR-0001-your-decision-title.yaml
git commit -m "feat(adr): ADR-0001 your decision title"
git push origin adr/0001-your-decision-title
```

The CI pipeline validates schema compliance and lints the YAML. Reviewers are auto-assigned via CODEOWNERS. The PR becomes the decision forum — all discussion, feedback, and approval happens asynchronously in the PR thread.

## ADR Meta-Model

Each ADR YAML file contains these sections:

| Section | Required | Description |
|---------|:--------:|-------------|
| `adr` | ✅ | ID, title, status, summary, timestamps, project, tags, priority, decision type, schema version |
| `authors` | ✅ | Who drafted the ADR |
| `decision_owner` | ✅ | Single accountable person |
| `context` | ✅ | Problem summary (**Markdown**), business/technical drivers, constraints |
| `alternatives` | ✅ | ≥2 alternatives with summary (**Markdown**), pros, cons, cost, risk, rejection rationale |
| `decision` | ✅ | Chosen alternative, rationale (**Markdown**), tradeoffs (**Markdown**), date, confidence |
| `consequences` | ✅ | Positive and negative outcomes |
| `confirmation` | ✅ | How the decision's implementation will be verified; artifact IDs (optional, backfilled later) |
| `reviewers` | | People who reviewed |
| `approvals` | | Formal approvals with timestamps and platform identities for CI verification |
| `requirements` | | Embedded functional and non-functional requirements (ASRs) |
| `dependencies` | | Internal and external dependencies |
| `references` | | External references, standards, evidence |
| `lifecycle` | | Review cadence, supersession chain, archival |
| `audit_trail` | | Immutable append-only event log |

> **Markdown-native fields** support full Markdown including embedded Mermaid diagrams via code fences. Use YAML literal block scalars (`|`) for multiline content.

## CI/CD Setup

Automated validation is the enforcement mechanism that makes the governance process real. Without it, the schema is a suggestion; with it, the schema is a contract.

**GitHub Actions** is preconfigured — the workflow at [`.github/workflows/validate-adr.yml`](.github/workflows/validate-adr.yml) runs on every PR. You just need to [enable branch protection](docs/ci-setup.md#github-actions) to make it a merge gate.

**Other platforms** have ready-to-use pipeline files in the `ci/` directory:

| Platform | Pipeline file | Copy to |
|----------|---------------|---------|
| Azure DevOps | [`ci/azure-devops/azure-pipelines.yml`](ci/azure-devops/azure-pipelines.yml) | `azure-pipelines.yml` (repo root) |
| GCP Cloud Build | [`ci/gcp-cloud-build/cloudbuild.yaml`](ci/gcp-cloud-build/cloudbuild.yaml) | `cloudbuild.yaml` (repo root) |
| AWS CodeBuild | [`ci/aws-codebuild/buildspec.yml`](ci/aws-codebuild/buildspec.yml) | `buildspec.yml` (repo root) |
| GitLab CI | [`ci/gitlab-ci/.gitlab-ci.yml`](ci/gitlab-ci/.gitlab-ci.yml) | `.gitlab-ci.yml` (repo root) |

**Step-by-step setup instructions**, platform-specific enforcement configuration, troubleshooting, and **LLM-ready prompts** (copy-paste into any AI assistant to have it set up CI for you) are in **[`docs/ci-setup.md`](docs/ci-setup.md)**.

## AI-Assisted Authoring & Pre-Review

ADRs are not meant to be filled in manually like a form. They are authored through **Socratic dialogue with an AI assistant** — the AI asks probing questions, challenges weak rationale, surfaces missing edge cases, and iteratively refines the document until it is clear, complete, and internally consistent.

This is a fundamental shift from traditional architecture governance: instead of the proposer writing a draft in isolation and then scheduling a meeting to "walk through" it (where reviewers discover ambiguities in real time and the meeting devolves into clarification rather than decision-making), the AI assistant resolves those ambiguities *before the first human reviewer ever sees the document*.

### Agent Skill

The [`.skills/adr-author/`](.skills/adr-author/) directory follows the [agentskills.io specification](https://agentskills.io/specification) and works with:

- **Google Antigravity** (VS Code)
- **Claude Code** (terminal)
- **VS Code Copilot** (with skills support)
- Any agent implementing the Agent Skills standard

The skill guides AI assistants to author ADRs through interactive questioning — probing for Architecturally Significant Requirements (ASRs), demanding balanced alternatives (not strawmen), checking that constraints are testable, and verifying that the rationale actually connects to the stated drivers. It understands the full meta-model and governance lifecycle.

### Web Chat (No Skill Required)

Don't have access to a coding agent? The Repomix bundle (`adr-governance-bundle.md`) includes **embedded AI instructions** that replicate the full skill — upload the single file to any web-based AI chat:

- **ChatGPT** (with Code Interpreter for large file search)
- **Claude.ai** (200K–1M token context)
- **Google Gemini** (1M+ token context)
- **Microsoft Copilot** (web)

The AI will be able to author new ADRs through Socratic dialogue, query the decision log with citations, review ADRs for completeness, summarize decisions for stakeholders, and validate YAML against the schema — all from a single uploaded file.

See **[`docs/web-chat-quickstart.md`](docs/web-chat-quickstart.md)** for platform-specific starter prompts and tips.


### Pre-Review Quality Gate

Before submitting an ADR for human review, run it through an AI semantic review using [`scripts/review-adr.py`](scripts/review-adr.py):

```bash
# Generate a Socratic review prompt (pipe to your LLM)
python3 scripts/review-adr.py architecture-decision-log/ADR-0009.yaml

# Include cross-reference context from existing decisions
python3 scripts/review-adr.py architecture-decision-log/ADR-0009.yaml \
  --context-from architecture-decision-log/

# Pipe directly to an LLM
python3 scripts/review-adr.py architecture-decision-log/ADR-0009.yaml | \
  llm -m gpt-4o
```

The generated prompt instructs the LLM to perform a structured review covering:
- **Semantic clarity** — are there ambiguous terms or vague claims?
- **Completeness** — are alternatives balanced, constraints testable, consequences honest?
- **Logical consistency** — does the rationale align with the pros/cons?
- **Assumption risks** — what happens if the assumptions are wrong?
- **Missing perspectives** — are there unconsidered stakeholders or alternatives?
- **Cross-reference consistency** — does this decision conflict with existing ADRs?

The AI outputs a verdict (**READY FOR REVIEW**, **NEEDS REWORK**, or **MAJOR GAPS**), a list of issues with severity, and open questions for the proposer. The proposer addresses the feedback, re-runs the check, and iterates until the ADR passes. *Then* they open the PR.

> **The result:** Human reviewers receive ADRs that are already semantically coherent and complete. Review meetings become strategic discussions about the *decision* — not debugging sessions about what the proposer meant.

## Stakeholder Summaries

Not every stakeholder needs the full ADR. After a decision is made (or after an architecture review meeting), use [`scripts/summarize-adr.py`](scripts/summarize-adr.py) to produce concise summaries for communication:

```bash
# Email-length summary (~10–15 lines: decision, rationale, alternatives, tradeoffs, impact)
python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml

# Ultra-short chat summary (3–5 lines for Slack/Teams)
python3 scripts/summarize-adr.py --format chat architecture-decision-log/ADR-0001.yaml

# Meeting recap — digest of multiple ADRs
python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml \
    architecture-decision-log/ADR-0002.yaml

# Save to file
python3 scripts/summarize-adr.py -o meeting-recap.md architecture-decision-log/
```

Each summary links back to the full YAML source. For a richer, rendered view, point stakeholders to the auto-generated Markdown in [`rendered/`](rendered/).

## ADL as Source of Truth

The Architecture Decision Log isn't just documentation — it's a **machine-readable specification** that AI agents and CI pipelines can enforce against your codebase. This closes the gap between *deciding* and *doing*.

### Spec-Driven Development (SDD)

AI coding agents (Copilot, Claude Code, Antigravity, Cursor, etc.) can use the bundled ADL as a **single source of truth** during code generation. When the ADL says "use DPoP for sender-constrained tokens" (ADR-0001), the agent can search the bundled decision log, find the decision with its full rationale and constraints, and generate code that aligns with it — without the developer having to explain the architectural context in every prompt.

The workflow:

1. **Bundle the ADL** into a single file:
   ```bash
   ./scripts/bundle.sh
   ```
   This generates `adr-governance-bundle.md` — the entire governance framework, schema, and all accepted decisions in one searchable file.

2. **Point your agent to it.** Paste the bundle into an LLM context window, add it to your agent's project knowledge, or reference it as a file. The agent can then use standard text search (grep, semantic search, `Ctrl+F`) to find relevant decisions.

3. **Generate code that complies.** When the agent encounters an architectural question — which token format to use, which signing algorithm, which authentication pattern — it searches the ADL instead of guessing or asking you.

> **Cross-repository enforcement:** The ADL repo and the code repo don't need to be the same. Point your agent at the ADL bundle from *any* repository. The decisions are self-contained — each ADR includes the full context, rationale, and constraints needed to understand and apply it.

### Semantic Guardrails in CI

The ADL can also serve as a **pre-merge guardrail** in your *code* repositories — not just the ADR repository itself. Before a PR is merged, a CI step can validate that the code changes are consistent with accepted architectural decisions.

This works at two levels:

**1. Local enforcement (during development):**
Coding agents that have the ADL in context will naturally align with it. When you ask "implement the token endpoint," an agent with ADR-0001 in context will use DPoP, not mTLS — because the decision and its rationale are right there in the searchable bundle.

**2. CI pipeline enforcement (pre-merge):**
Use [`scripts/extract-decisions.py`](scripts/extract-decisions.py) to extract active decisions and generate an LLM compliance prompt. Add a step in your code repository's CI pipeline:

```yaml
# Example: GitHub Actions step in your CODE repo (not this repo)
- name: Check ADR compliance
  run: |
    # Fetch the extraction script and ADR files from the governance repo
    git clone --depth 1 https://github.com/your-org/adr-governance.git /tmp/adl
    pip install pyyaml

    # Generate a compliance prompt with the code diff
    python3 /tmp/adl/scripts/extract-decisions.py \
      --compliance-prompt \
      --diff <(git diff origin/main...HEAD) \
      /tmp/adl/architecture-decision-log/ \
      > /tmp/compliance-prompt.md

    # Pipe to your LLM of choice for automated review
    # (replace with your preferred LLM CLI — openai, claude, gemini, llm, etc.)
    cat /tmp/compliance-prompt.md | your-llm-cli "Review this for compliance"
```

The key insight: **the ADL is structured YAML that any tool can parse**. The `extract-decisions.py` script handles the parsing and prompt generation — you just plug in your LLM provider.

### Decision Extraction

The [`scripts/extract-decisions.py`](scripts/extract-decisions.py) script is the bridge between the ADL and downstream enforcement tooling:

```bash
# Markdown summary of all accepted decisions (for agent context)
python3 scripts/extract-decisions.py architecture-decision-log/

# JSON output for programmatic consumption
python3 scripts/extract-decisions.py --format json architecture-decision-log/

# Filter by tags (e.g., only OAuth-related decisions)
python3 scripts/extract-decisions.py --tags oauth,security architecture-decision-log/

# Generate an LLM compliance-check prompt with a code diff
python3 scripts/extract-decisions.py --compliance-prompt \
  --diff <(git diff main) architecture-decision-log/

# Save to a file for agent context injection
python3 scripts/extract-decisions.py -o active-decisions.md architecture-decision-log/
```

### What This Enables

| Scenario | Without ADL enforcement | With ADL enforcement |
|----------|------------------------|---------------------|
| New developer joins | Reads (or doesn't read) wiki docs | Agent has full ADL context; generates compliant code from day one |
| PR introduces mTLS | Merges — nobody notices the ADR says DPoP | CI flags the drift; reviewer is alerted |
| Architect proposes supersession | Searches Slack history for context | Searches the ADL bundle; full decision chain is traceable |
| Annual audit | Scramble to reconstruct decision history | ADL is the audit trail; every decision is timestamped, attributed, and version-controlled |
| LLM generates code | Guesses at patterns based on training data | Searches the ADL and follows your organization's actual decisions |

### Repomix Bundle

To create the single-file bundle:

```bash
./scripts/bundle.sh
```

This generates `adr-governance-bundle.md` — the entire ADR governance framework in one file. The bundle includes the schema, process documentation, glossary, skill instructions, YAML template, all ADRs in `architecture-decision-log/`, example ADRs from `examples-reference/`, validation scripts, and **embedded AI instructions** that enable web-based AI chats to emulate the full authoring skill.

**Usage options:**
- **Upload** to any AI web chat (ChatGPT, Claude, Gemini, Copilot) — see [`docs/web-chat-quickstart.md`](docs/web-chat-quickstart.md)
- **Paste** into any LLM context window for instant AKM context
- **Add** to your coding agent's project knowledge base
- **Fetch** from CI pipelines in other repositories (as shown above)
- **Commit** to other repositories as a versioned reference artifact

## Rendered Markdown (Auto-Generated)

Every ADR YAML file has a corresponding **human-friendly Markdown rendering** in [`rendered/`](rendered/). These are designed for browsing on GitHub, Azure DevOps, Azure Repos, and other platforms that render Markdown natively.

- **[`rendered/architecture-decision-log.md`](rendered/architecture-decision-log.md)** — the decision log index with clickable links, status, and decision dates
- **`rendered/ADR-NNNN-*.md`** — individual ADR renderings with a provenance disclaimer

> **⚠️ Do not edit files in `rendered/` directly.** They are auto-generated from the YAML source. Each rendered file includes a `[!CAUTION]` banner and HTML comment pointing to the source YAML.

### Pre-commit hook (automatic rendering)

A Git pre-commit hook automatically re-renders all ADR files and regenerates the index whenever you commit changes to `architecture-decision-log/`. This means both the YAML source and its Markdown rendering are part of the same commit and PR — **reviewers approve both together**.

**One-time setup** (per clone):

```bash
git config core.hooksPath .githooks
```

After this, any commit that touches `architecture-decision-log/*.yaml` will automatically:
1. Render all ADR YAML files to `rendered/*.md` with a provenance disclaimer
2. Regenerate [`rendered/architecture-decision-log.md`](rendered/architecture-decision-log.md) (the decision log index)
3. Stage the rendered files alongside the YAML changes

### Manual rendering

```bash
# Single file to stdout (no disclaimer — useful for previewing)
python3 scripts/render-adr.py architecture-decision-log/ADR-0001-*.yaml

# Render to rendered/ with disclaimer + index
python3 scripts/render-adr.py --output-dir rendered/ --generate-index architecture-decision-log/
```

## Example ADRs

The [`examples-reference/`](examples-reference/) directory contains interconnected ADRs from a **fictional** IAM department at NovaTrust Financial Services. These are **not real decisions** — they demonstrate the meta-model at production quality. Use them as a reference for style, depth, and interconnection:

| ID | Title | Status |
|----|-------|--------|
| ADR-0001 | [Use DPoP over mTLS for Sender-Constrained Tokens](examples-reference/rendered/ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.md) | accepted |
| ADR-0002 | [Use Reference Tokens over JWTs for Gateway Introspection](examples-reference/rendered/ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.md) | accepted |
| ADR-0003 | [Use Pairwise Subject Identifiers for OIDC Relying Parties](examples-reference/rendered/ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.md) | accepted |
| ADR-0004 | [Use Ed25519 over RSA-2048 for JWT Signing Keys](examples-reference/rendered/ADR-0004-ed25519-over-rsa-for-jwt-signing.md) | accepted |
| ADR-0005 | [Use BFF Token Mediator for SPA Token Acquisition](examples-reference/rendered/ADR-0005-bff-token-mediator-for-spa-token-acquisition.md) | accepted |
| ADR-0006 | [Use Session Enrichment for Step-Up Authentication Proof](examples-reference/rendered/ADR-0006-session-enrichment-for-step-up-authentication.md) | accepted |
| ADR-0007 | [Reject Centralized HashiCorp Vault for API Runtime Secrets](examples-reference/rendered/ADR-0007-centralized-secret-store-for-api-keys.md) | **rejected** |
| ADR-0008 | [Defer OpenID Federation for Automated Trust Establishment](examples-reference/rendered/ADR-0008-defer-openid-federation-for-trust-establishment.md) | **deferred** |

See the [rendered example index](examples-reference/rendered/architecture-decision-log.md) for a full overview, or [`examples-reference/README.md`](examples-reference/README.md) for details on each example.

Additionally, [`architecture-decision-log/ADR-0000`](architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml) is a meta-ADR documenting the AD to adopt this governance process itself.

> **Bootstrap exception:** ADR-0000 was self-approved by the initial author as the bootstrapping meta-decision. The "no self-approval" rule (§3.4) applies to all subsequent ADRs.

## License

MIT
