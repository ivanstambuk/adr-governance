# ADR Schema Reference

The ADR meta-model is defined as a JSON Schema (Draft 2020-12) at `schemas/adr.schema.json`.

## Required Top-Level Sections

| Section | Description |
|---------|-------------|
| `adr` | Core metadata: id, title, status, timestamps, project, decision_type |
| `authors` | At least one author with name and role |
| `decision_owner` | Single accountable person |
| `context` | Problem summary, drivers, constraints, assumptions |
| `alternatives` | Minimum 2 alternatives with pros, cons, cost, risk |
| `decision` | Chosen alternative, rationale, tradeoffs, date, confidence level |
| `consequences` | Positive and negative outcomes |
| `confirmation` | How the decision's implementation will be verified (`description` required, `artifact_ids` optional) |

## Optional Top-Level Sections

| Section | Description |
|---------|-------------|
| `reviewers` | People who reviewed the ADR |
| `approvals` | Formal approvals with timestamps, platform identities, and signature IDs. Required when `adr.status` is `proposed` or `accepted`; `rejected` / `deferred` outcomes rely on terminal audit events plus PR/MR history instead |
| `architecturally_significant_requirements` | Architecturally Significant Requirements (ASRs) — functional and non-functional |
| `dependencies` | Internal and external dependencies |
| `references` | External links and evidence |
| `lifecycle` | Review cadence metadata, supersession chain, archival. Review scheduling/reminders are outside this repo's scope |
| `audit_trail` | Immutable event log (events: created, updated, reviewed, approved, rejected, deferred, superseded, deprecated, archived) |

## Key Validation Rules

1. `adr.id` must match `^ADR-[0-9]{4}(-[a-z0-9]+)+$` — slug is mandatory (e.g. `ADR-0001-dpop-over-mtls`)
2. The filename stem must exactly match `adr.id` (for example `ADR-0001-dpop-over-mtls.yaml` ↔ `adr.id: ADR-0001-dpop-over-mtls`)
3. `adr.status` must be one of the defined enum values (see below)
4. `alternatives` must have `minItems: 2`
5. `decision.chosen_alternative` should match a name in `alternatives`
6. Requirement IDs: `^(F|NF)-[0-9]{3}$`
7. `proposed` and `accepted` ADRs must include `approvals` with at least one entry, and every approval entry must include `identity`
8. `rejected` and `deferred` ADRs do not require `approvals`, but they do require the matching terminal audit event and should preserve the disposition rationale in PR/MR history
9. Existing `audit_trail` history is append-only across PRs: prior entries may not be edited, deleted, or reordered; new entries may only be appended
10. If an ADR is already `accepted`, its decision core is immutable in place; material changes require a new superseding ADR
11. Extension fields: any key starting with `x-` is allowed at the top level
12. `draft` still means a schema-valid, substantially complete ADR; the distinction from `proposed` is governance state, not missing core sections
13. `adr.y_statement` should target **100–150 words**. It is the most information-dense *summary* of the decision — not a second rationale. Each of the 7 clauses should be concise: use just names in `neglected`, one headline in `facing`, top 2 tradeoffs in `accepting`, and one core reason in `because`. Detail belongs in the dedicated sections (`context.summary`, `decision.rationale`, `decision.tradeoffs`, `consequences`).

## Enum Values

### `adr.status`
`draft` | `proposed` | `accepted` | `superseded` | `deprecated` | `rejected` | `deferred`

### `adr.decision_type`
`technology` | `process` | `organizational` | `vendor` | `security` | `compliance`

### `adr.priority`
`low` | `medium` | `high` | `critical`

### `decision.confidence`
`low` | `medium` | `high`

### `alternatives[].risk`
`low` | `medium` | `high` | `critical`

### `alternatives[].estimated_cost`
`low` | `medium` | `high`

### `audit_trail[].event`
`created` | `updated` | `reviewed` | `approved` | `rejected` | `deferred` | `superseded` | `deprecated` | `archived`

## Markdown-Native Fields

The following fields support **full Markdown** including embedded Mermaid diagrams via fenced code blocks. Use YAML literal block scalars (`|`) for multiline content.

| Field | Description |
|-------|-------------|
| `context.summary` | Narrative problem statement; embed architecture diagrams |
| `alternatives[].description` | **Thorough** architectural description of each option. Not a summary — write multiple paragraphs covering how the design works, data flows, integration points. **Embedding Mermaid diagrams is strongly encouraged** (sequence, flowchart, C4). Include **code examples** for technology decisions, **evolution timeline tables** for multi-phase decisions, and **empirical evidence** for tried-and-removed alternatives (e.g., "36% FFI overhead"). Document **syntax/design debates** as architecturally significant choices. |
| `decision.rationale` | Explain *why*; use bullet lists, headers, diagrams |
| `decision.tradeoffs` | Acknowledged tradeoffs accepted with this decision |
| `confirmation.description` | Verification evidence and implementation proof |

⚠️ **YAML scalar pitfalls** — three common issues can silently corrupt ADR content:
1. **Folded scalars (`>`) destroy code blocks** — Always use `|` (literal) for these fields, never `>` (folded). The `>` indicator collapses newlines into spaces, breaking Mermaid fences. The validator will warn if collapsed code fences are detected.
2. **Leading `"` in list items breaks parsing** — A list item starting with `"` (e.g., a quoted phrase) opens a quoted string the parser expects closed. Use `>-` for items starting with `"`.
3. **`#` in plain scalars is a comment** — A `#` preceded by a space in a plain (unquoted) scalar is treated as a comment. Everything after it is silently dropped. Use `>-` for list items containing `#`. This does NOT affect `|` or `>` block scalars.

**Mermaid quality patterns:**
- Use **subgraphs** to group related concepts (e.g., "Native Outputs", "Measured Gains")
- Use **decision nodes** (`{Decision Point}`) for branching choices
- Use **styled nodes** to communicate outcomes: `fill:#2d8` (green = positive), `fill:#f66` (red = blocked)
- Use **`<br/>`** for line breaks in node labels (never `\n` — Mermaid renders it literally)
- Use **bidirectional arrows** (`<-->`) for cyclic or mutual dependencies
- Add **benchmark/comparison tables** alongside diagrams when quantitative data is available
- Include **side-by-side comparison tables** for tactical decisions where a competitor/inspiration exists (e.g., Vue vs. React Hooks) — tables communicate differentiators more efficiently than prose
- Label alternatives with **empirical evidence** markers — "actually prototyped and discarded" or "tried in production and removed" — to distinguish theoretical from empirical rejection rationale

## Person Schema (`$defs/person`)

Used for `authors[]`, `decision_owner`, `reviewers[]`:

| Field | Type | Required |
|-------|------|----------|
| `name` | string | ✅ |
| `role` | string | ✅ |
| `email` | string (email) | ❌ |

## Approval Entry Schema

| Field | Type | Required |
|-------|------|----------|
| `name` | string | ✅ |
| `role` | string | ✅ |
| `identity` | string | ❌ globally; ✅ when `adr.status` is `proposed` or `accepted` |
| `approved_at` | string (date-time) or null | ❌; semantically required only once an ADR becomes `accepted` |
| `signature_id` | string or null | ❌ |
