---
name: adr-author
description: >
  Author, review, validate, and summarize Architecture Decision Records (ADRs)
  using a governed YAML meta-model. Use when the user asks to create a new ADR,
  review an existing ADR, validate ADR YAML files against the schema, summarize
  decisions for stakeholders (email/chat), or needs guidance on the ADR governance
  process. Supports two creation modes: interactive Socratic dialogue and
  artifact-driven extraction from uploaded documents (meeting transcripts,
  slides, design docs, images, etc.). Covers the full lifecycle: drafting,
  review, approval, supersession, and archival.
license: MIT
metadata:
  author: "ivanstambuk"
  version: "1.1"
---

# ADR Author Skill

## When to use this skill

Use this skill when the user:
- Wants to **create a new ADR** (architecture decision record) — either through interactive questioning or from uploaded documents
- Wants to **generate an ADR from artifacts** — meeting transcripts, PowerPoint slides, PDFs, design documents, images, or other reference materials
- Wants to **review or audit an existing ADR** for completeness
- Needs to **validate** an ADR YAML file against the schema
- Wants to **summarize** an ADR for stakeholders (email, chat, digest)
- Asks about the **ADR governance process** or lifecycle
- Wants to **supersede, deprecate, or archive** an existing ADR
- Needs to understand the **ADR meta-model** fields and allowed values

## Core principles

1. **Self-contained**: Every ADR must embed all context (architecturally significant requirements, alternatives, risk, compliance) so it can be understood without external documents.
2. **Schema-governed**: All ADRs must validate against `schemas/adr.schema.json` (JSON Schema Draft 2020-12).
3. **At least two alternatives**: Every decision requires evaluation of ≥2 alternatives with pros, cons, cost, and risk.
4. **Immutable audit trail**: The `audit_trail` section is append-only. Never delete or modify existing entries.
5. **Self-contained with navigational links**: Supersession is tracked via `lifecycle.supersedes`/`superseded_by`. Each ADR remains fully self-contained — no structural dependencies on other ADRs.

## How to create a new ADR

The skill supports two creation modes:

- **Mode A: Socratic interview** (default) — interactive questioning
- **Mode B: Artifact-driven** — extract from uploaded documents, then fill gaps

### Mode A: Socratic interview (default)

#### Step 1: Determine the next ADR ID

Check existing ADR files in the `architecture-decision-log/` directory (or `examples-reference/` for reference). The ID format is `ADR-NNNN` (zero-padded 4 digits). Use the next sequential number.

#### Step 2: Gather context from the user

Ask the user for:
1. **Title**: What decision is being made? (10-200 characters)
2. **Decision type**: `technology` | `process` | `organizational` | `vendor` | `security` | `compliance`
3. **Decision level** (optional): `strategic` | `tactical` | `operational` — the architectural altitude of the decision (see glossary for heuristics)
4. **Priority**: `low` | `medium` | `high` | `critical`
5. **Context**: What problem are we solving? What are the business and technical drivers?
6. **Constraints**: What are the non-negotiable boundaries?
7. **Alternatives**: At least 3 options (minimum 2 if the user insists after pushback) — for each, a **thorough architectural description** (multi-paragraph, with Mermaid diagrams showing data flows/integration points), pros, cons, estimated cost (only if the user provides it), and risk level (only if the user provides it)
8. **Recommendation**: Which alternative and why?
9. **Confidence**: `low` | `medium` | `high` — how confident are we in this decision?

#### Step 3: Generate the ADR YAML

Use the template at `assets/adr-template.yaml` as the starting point. Fill in all required sections:

- `adr` — metadata (id, title, status, timestamps, tags, priority, decision_type, decision_level, y_statement)
- `adr.y_statement` — **auto-generate** from the collected interview answers. Do NOT ask the user to write this. The Y-Statement **must** contain all 7 structural clauses in this exact order (see `docs/glossary.md` → "Y-Statement" for the canonical template mapping):
  1. "In the context of [context.description],"
  2. "facing [key driver],"
  3. "we decided for [decision.chosen_alternative]"
  4. "and neglected [rejected alternatives],"
  5. "to achieve [positive consequences],"
  6. "accepting [tradeoffs],"
  7. "because [decision.rationale]."
  If any clause is missing, rewrite until all 7 are present. Present to the user for confirmation. Always use "**and neglected**" — never "and rejected" — to match the canonical Y-Statement vocabulary.

  **Bold the clause keywords** in the YAML value to aid scanning: `**In the context of**`, `**facing**`, `**we decided for**`, `**and neglected**`, `**to achieve**`, `**accepting**`, `**because**`.

  **Target length: 100–150 words.** The Y-Statement is a *summary*, not a rationale — it must be a single scannable paragraph. If it exceeds 150 words, you are duplicating content that belongs in `context.description`, `decision.rationale`, or `decision.tradeoffs`. Apply these per-clause brevity rules:
  - **`facing`**: One headline problem (not a list of drivers) — the drivers belong in `context`
  - **`we decided for`**: Name + one key differentiator — the detailed description belongs in `alternatives[].description`
  - **`and neglected`**: Just alternative names — no parenthetical descriptions ("Vite" not "Vite (the community-favorite alternative backed by Evan You)")
  - **`to achieve`**: Top 2–3 outcomes — the full list belongs in `consequences.positive`
  - **`accepting`**: Top 2 tradeoffs — the full list belongs in `decision.tradeoffs`
  - **`because`**: One core reason — the full rationale belongs in `decision.rationale`
- `authors` — who is writing this
- `decision_owner` — who is accountable
- `context` — description, business_drivers, technical_drivers, constraints, assumptions
- `architecturally_significant_requirements` — embedded functional and non-functional ASRs
- `alternatives` — at least 2 (include more if naturally discussed), each with name, **thorough description** (multi-paragraph architecture explanation with Mermaid diagrams), pros, cons, estimated_cost (only if user-provided), risk (only if user-provided), rejection_rationale (for non-chosen alternatives)
- `decision` — chosen_alternative, rationale, tradeoffs, decision_date, confidence **(all values must come from the user's answers — do not invent defaults)**
- `consequences` — positive, negative

  **Target: 15–25 words per consequence item.** Each item should state a single clear outcome — not a paragraph. If it needs explanation, the detail belongs in `decision.rationale` or `decision.tradeoffs`.
- `confirmation` — description of how implementation will be verified (artifact_ids added later)
- `architecturally_significant_requirements` — extract functional and non-functional ASRs from the interview answers (technical drivers, constraints, performance targets, compliance mandates). Target 2-7 per category based on the decision's complexity — strategic/high-priority decisions typically need 4-6, simple operational decisions may need only 2. **Vary the count naturally; do NOT always use exactly 3 functional + 3 non-functional.** If none are obvious from the conversation, ask the user explicitly.
- `dependencies` — internal and external dependency tracking
- `audit_trail` — initial `created` event

  **Target: 15–30 words per entry's `details` field.** Audit trail entries are log entries, not essays. Format: "What happened + one sentence of significance." The full context belongs in `context.description` and `decision.rationale`.
- `lifecycle` — set `review_cycle_months` based on `decision_level` × `confidence`:

  | Level \\ Confidence | `low` | `medium` | `high` |
  |---------------------|:-----:|:--------:|:------:|
  | **Strategic** | 24 | 36 | 60 |
  | **Tactical** | 12 | 18 | 24 |
  | **Operational** | 6 | 12 | 18 |

  Set `review_cycle_months: 0` only for permanent decisions that never need review (e.g., "Use UTF-8"). Compute `next_review_date` = `decision_date` + `review_cycle_months`.

#### Step 4: Validate

Run the validation script to check the YAML against the JSON Schema:

```bash
python3 scripts/validate-adr.py architecture-decision-log/ADR-NNNN-short-title.yaml
```

#### Step 5: File naming convention

```
architecture-decision-log/ADR-NNNN-short-kebab-case-title.yaml
```

Example: `architecture-decision-log/ADR-0007-adopt-passkeys-for-workforce-mfa.yaml`

### Mode B: Artifact-driven authoring

Use this mode when the user provides **reference documents** instead of (or in addition to) answering questions interactively. Supported artifacts include:

- **Text-based**: Meeting transcripts, meeting notes, design documents, RFC drafts, email threads, Slack/Teams chat exports, Markdown files, plain text
- **Documents**: PDFs, Word documents (.docx), PowerPoint slides (.pptx)
- **Visual**: Architecture diagrams, whiteboard photos, screenshots, decision matrices, any image the platform can process

#### Step 1: Ingest and extract

Read/parse every provided artifact:
- For **text-based files**: extract decisions discussed, alternatives mentioned, arguments for/against, action items, participants (potential authors/decision owners), constraints, and drivers.
- For **slide decks and documents**: extract key claims, data points, comparison tables, architectural options, risk assessments, and recommendations.
- For **images**: describe what you see (architecture diagrams, whiteboard sketches, decision matrices) and extract visible text, labels, or structural information. If a diagram is identified, attempt to map it to a Mermaid representation for embedding in the ADR.

#### Step 2: Present extraction summary

Present a structured extraction summary organized by ADR schema section. For each section, show:
- Whether information was found (✅ / ❌)
- The source file/location
- A brief summary of what was extracted

Flag any **ambiguities or contradictions** across documents.

#### Step 3: Targeted gap-filling

For sections not covered by the artifacts (marked ❌) or flagged as ambiguous, ask targeted questions. Use the same batched numerical format (up to 5 per batch) as Mode A. Only ask about what's actually missing.

#### Step 4: Coherence check

Run the same coherence check as Mode A. Additionally:
- Flag **cross-document contradictions** (e.g., transcript says one thing, slides say another)
- Flag **stale information** (earlier thinking that may have been superseded)
- Surface **implicit assumptions** that should be made explicit

#### Step 5: Generate YAML

Follow the same YAML generation process as Mode A. In the `audit_trail` entry, note the source artifacts:
```yaml
audit_trail:
  - event: "created"
    by: "AI Assistant"
    at: "2026-03-06T00:00:00Z"
    details: "ADR generated from uploaded artifacts: [list filenames]. Gap-filling interview conducted for [list sections]."
```

#### Step 6: Validate and save

Same as Mode A Steps 4–5.

## How to review an existing ADR

When reviewing, check for:

1. **Completeness**: All required sections present (see schema `required` fields)
2. **Alternative quality**: At least 2 alternatives with substantive pros/cons (not just "good" / "bad")
3. **Rationale strength**: Does the rationale clearly connect to the drivers and architecturally significant requirements?
4. **Risk coverage**: Are the major risks identified with realistic mitigations?
5. **Compliance**: Are regulatory implications addressed if the decision touches data, access, or infrastructure?
6. **Consistency**: Does the `chosen_alternative` name match an entry in `alternatives`? Are `lifecycle.supersedes`/`superseded_by` consistent?
7. **Audit trail**: Is the trail consistent with the status?
8. **Rejection rationale**: For each non-chosen alternative, is `rejection_rationale` populated explaining why it was not selected?
9. **Diagram quality**: Are embedded Mermaid diagrams used where a visual would clarify architecture or flow?
10. **Code examples**: For technology decisions, do the alternative descriptions include concrete code snippets that demonstrate the developer experience? Code examples make the motivation visceral — a reader seeing verbose combinator chains immediately understands why a new syntax was needed.
11. **Empirical evidence**: If an alternative was actually tried and removed (not just theoretically rejected), is this prominently stated? This includes both "tried and removed from production" (e.g., Rust green threads) and "prototyped and discarded" (e.g., Vue Class API RFC that was dropped). An empirical rejection is far stronger than a theoretical one.
12. **Community backlash as evidence**: If a decision generated significant community controversy, is this captured as both a negative consequence and an acknowledged tradeoff? Community backlash reveals genuine philosophical disagreements (simplicity vs. power, prescriptive vs. flexible) that are architecturally significant, not mere noise.
13. **Coexistence/meta-decisions**: If the decision involves supporting multiple approaches simultaneously (e.g., Vue's Options + Composition API), is the coexistence strategy itself analyzed as an architectural choice? The "additive vs. replacement" decision deserves explicit rationale.
14. **Evolution timeline tables**: For decisions with multi-year or multi-phase design histories (e.g., Go generics: 12 years, 6 iterations), include a timeline table showing the progression. For multi-phase rollout plans (e.g., ESLint 4-year transition, Vite 3-phase rollout), the rollout strategy itself is an architectural decision worth analyzing.
15. **Before/after examples for configuration and migration ADRs**: When the decision replaces an existing configuration or API pattern (`.eslintrc` → `eslint.config.js`, `setup.py` → `pyproject.toml`), show the old and new side by side. Property mapping tables (what changed, what was removed, what's new) are more effective than prose for communicating scope.
16. **Creator quotes as primary sources**: Direct quotes from project creators or leads (e.g., "biggest regret," "afraid to touch") provide authenticity and weight that paraphrasing cannot match. Always attribute to official blog posts or talks, not secondhand sources.
17. **Selection rubric tables for cross-cutting decisions**: When the decision applies across multiple contexts (e.g., "which container base image for which workload?"), include a selection rubric table mapping workload characteristics to the appropriate option. This is the most actionable artifact for cross-cutting ADRs.
18. **Commercial entity and vendor dynamics as architectural tradeoffs**: When the tool is backed by a commercial entity (VC-funded company, single-vendor control), surface this as an explicit tradeoff — not just context. Include: vendor dependency risk, governance model, and commercial pressure as first-class architectural concerns alongside technical tradeoffs.

## How to supersede an ADR

1. Create a new ADR (ADR-MMMM) following the standard proposal workflow.
2. In the **new** ADR:
   - Set `lifecycle.supersedes: "ADR-NNNN"`
3. When the new ADR is accepted, **update the old ADR** in the same PR:
   - Set `adr.status: "superseded"`
   - Set `lifecycle.superseded_by: "ADR-MMMM"`
   - Add an audit trail entry: `event: "superseded"`

## Markdown-native fields

The following fields support **full Markdown** including embedded Mermaid diagrams via code fences:

- `context.description` — narrative problem statement; embed architecture diagrams here
- `alternatives[].description` — **thorough** architectural description of each option; write multiple paragraphs explaining how the design works, data flows, and integration points. **Embedding Mermaid diagrams (sequence, flowchart, C4) is strongly encouraged.** Include:
  - **Code examples** for technology decisions — show what the developer experience looks like with each alternative. Concrete code makes tradeoffs visceral.
  - **Evolution timeline tables** for decisions that evolved over multiple phases or years — a timeline table makes the design trajectory clear at a glance.
  - **Empirical evidence** for tried-and-removed or prototyped-and-discarded alternatives — if the project actually implemented and later removed an alternative, or built a prototype RFC that was dropped, state this prominently with specific details (e.g., "36% FFI overhead", "decorator spec instability").
  - **Syntax/design debates** as architecturally significant — surface tension points (e.g., postfix vs. prefix syntax) are genuine design decisions with real consequences, not trivial bikeshedding.
  - **Comparison tables between alternatives** — for tactical decisions where a direct competitor/inspiration exists (e.g., Vue Composition API vs. React Hooks), a side-by-side comparison table immediately communicates key differentiators without paragraphs of prose.
- `decision.rationale` — explain *why*; use bullet lists, headers, or diagrams
- `decision.tradeoffs` — what was given up
- `confirmation.description` — verification evidence

Use YAML literal block scalars (`|`) for multiline content. Example:

```yaml
context:
  description: |
    The system currently uses approach X.

    ```mermaid
    graph LR
        A --> B --> C
    ```

    We need to decide between X and Y.
```

### Mermaid diagram quality guide

Every alternative description **should** include a Mermaid diagram. Invest in diagram quality — rich visuals make ADRs dramatically more readable. Follow these patterns:

#### Use subgraphs to group related concepts

```mermaid
graph TD
    subgraph "Native Outputs"
      A[tsc CLI] --> B[Language Server]
    end
    subgraph "Measured Gains"
      A --> C["10x faster builds"]
    end
```

#### Use decision nodes (`{}`) for branching choices

```mermaid
graph TD
    A[Input] --> B{Decision Point}
    B -->|option 1| C[Outcome A]
    B -->|option 2| D[Outcome B]
```

#### Style nodes to communicate outcome quality

Use green for positive outcomes and red for failures/blockers:

```mermaid
graph TD
    A[Approach] --> B["✅ Positive outcome"]
    A --> C["❌ Blocked path"]
    style B fill:#2d8,stroke:#333,color:#000
    style C fill:#f66,stroke:#333,color:#000
```

#### Use bidirectional arrows for cyclic relationships

```mermaid
graph TD
    A[Component A] <-->|depends on| B[Component B]
    B <-->|references| C[Component C]
```

#### Add benchmark/comparison tables alongside diagrams

When quantitative data is available, add a Markdown table in the description:

```markdown
| Metric | Before | After | Improvement |
|--------|-------:|------:|------------:|
| Build time | 77.8 s | 7.5 s | 10.4x |
| Startup | 9.6 s | 1.2 s | 8.0x |
```

#### Line breaks inside node labels

Use `<br/>` for multi-line node text. **Never use `\n`** — Mermaid renders it literally:

```
# ✅ Correct
C --> F["❌ Ref-counting overhead<br/>negates performance gains"]

# ❌ Wrong — renders literal \n
C --> F["❌ Ref-counting overhead\nnegates performance gains"]
```

### YAML scalar pitfalls

Three common YAML pitfalls can silently corrupt ADR content. Learn all three to avoid debugging mysterious parse errors.

#### Pitfall 1: Folded scalars (`>`) destroy code blocks

⚠️ **Critical: use `|` (literal), never `>` (folded), for descriptions containing code blocks.**

The YAML folded scalar (`>`) collapses newlines into spaces, which destroys Mermaid code fences:

```yaml
# ❌ WRONG — > collapses ```mermaid and graph TD onto one line
description: >
  Some text.

  ```mermaid
  graph TD
      A --> B
  ```

# ✅ CORRECT — | preserves newlines exactly
description: |
  Some text.

  ```mermaid
  graph TD
      A --> B
  ```
```

The validator (`scripts/validate-adr.py`) will warn if it detects collapsed code fences caused by this mistake.

#### Pitfall 2: Leading `"` in list items breaks parsing

A YAML list item starting with a `"` character (e.g., a quoted phrase) opens a quoted string that the parser expects to be closed. This causes cryptic parse errors on subsequent lines.

```yaml
# ❌ WRONG — leading " opens a quoted string that never closes
cons:
  - "Reusability" is a counterproductive notion
  - Next item causes parse error here

# ✅ CORRECT — use >- folded scalar for items starting with "
cons:
  - >-
    "Reusability" is a counterproductive notion
  - Next item works fine
```

#### Pitfall 3: `#` in plain scalars is a comment

A `#` character preceded by a space inside a **plain (unquoted) scalar** is treated as an inline comment start. Everything after it is silently dropped, causing a parse error on the *next* line.

```yaml
# ❌ WRONG — " #1" becomes a comment; "complaint..." is dropped
business_drivers:
  - Generics was the #1 complaint in annual surveys
    for over a decade

# ✅ CORRECT — use >- to prevent # from being parsed as comment
business_drivers:
  - >-
    Generics was the #1 complaint in annual surveys
    for over a decade
```

**Note:** This pitfall does NOT apply inside `|` or `>` block scalars — only in plain (unquoted) scalars and list items. Inside block scalars, `#` is always literal text.

#### Pitfall 4: `$:` in plain scalars is a mapping value

The `$:` token (common in Svelte's reactive `$:` labels, jQuery selectors, etc.) contains a colon-space after `$`, which YAML interprets as a mapping value indicator inside a plain scalar.

```yaml
# ❌ WRONG — $: triggers YAML mapping interpretation
cons:
  - Svelte's $: reactivity labels are replaced by runes

# ✅ CORRECT — use >- to prevent $: from being parsed as mapping
cons:
  - >-
    Svelte's $: reactivity labels are replaced by runes
```

**Summary of all four pitfalls:**

| # | Trigger | Where | Fix |
|:-:|---------|-------|-----|
| 1 | `>` folded scalar | Description fields with code blocks | Use `\|` instead |
| 2 | Leading `"` | List items starting with a quote | Use `>-` |
| 3 | `#` after space | Plain scalars mid-text | Use `>-` |
| 4 | `$:` | Plain scalars with colon after `$` | Use `>-` |

## Reference documentation

- See [the glossary](../../docs/glossary.md) for all enum values and term definitions
- See [the JSON Schema](references/SCHEMA_REFERENCE.md) for the full meta-model specification
- See example ADRs in the repository's `examples-reference/` directory for well-formed samples

## Summarizing ADRs for stakeholders

Sometimes the full ADR is too detailed for stakeholders who just need to know *what was decided and why*. Use `scripts/summarize-adr.py` to produce concise summaries.

### Email format (default)

A ~10–15 line summary covering: the decision, why it was chosen, what alternatives were considered, key tradeoffs, consequences, and next steps. Suitable for post-meeting emails, status updates, or stakeholder briefings.

```bash
# Single ADR
python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml

# Multiple ADRs → produces a numbered digest
python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml \
    architecture-decision-log/ADR-0002.yaml

# All ADRs in a directory → full digest
python3 scripts/summarize-adr.py architecture-decision-log/

# Save to file for emailing
python3 scripts/summarize-adr.py -o meeting-recap.md architecture-decision-log/
```

### Chat format

A 3–5 line ultra-short summary for Slack, Teams, or any chat platform. Just the headline, the decision, one positive and one negative consequence, and a link to the full document.

```bash
python3 scripts/summarize-adr.py --format chat architecture-decision-log/ADR-0001.yaml
```

### When to use which format

| Scenario | Format |
|----------|--------|
| Post-meeting email to stakeholders | `email` (default) |
| Slack/Teams announcement | `chat` |
| Weekly architecture digest | `email` with multiple ADRs |
| Quick reply to "what did you decide?" | `chat` |
| Architecture newsletter | `email` with all accepted ADRs |

### AI-assisted summarization

When the user asks you to summarize an ADR, **prefer running the script** — it extracts the most salient fields deterministically. If the user wants a *custom* summary (e.g., focused on security implications, or tailored for a specific audience like C-level or compliance), generate a custom summary using the ADR YAML as context, following the same structure: decision, rationale, alternatives, tradeoffs, impact, next steps.

## Validation

The `scripts/validate-adr.py` script validates any ADR YAML file against the JSON Schema:

```bash
# Validate a single ADR
python3 scripts/validate-adr.py path/to/ADR-0001.yaml

# Validate all ADRs in a directory
python3 scripts/validate-adr.py architecture-decision-log/
```

The script exits with code 0 if valid, 1 if validation errors are found.
