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
| `approvals` | Formal approvals with timestamps, platform identities, and signature IDs. Required when `adr.status` is `proposed` or `accepted` |
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
8. Existing `audit_trail` history is append-only across PRs: prior entries may not be edited, deleted, or reordered; new entries may only be appended
9. If an ADR is already `accepted`, its decision core is immutable in place; material changes require a new superseding ADR
10. Extension fields: any key starting with `x-` is allowed at the top level
11. `draft` still means a schema-valid, substantially complete ADR; the distinction from `proposed` is governance state, not missing core sections

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
| `alternatives[].description` | **Thorough** architectural description of each option. Not a summary — write multiple paragraphs covering how the design works, data flows, integration points. **Embedding Mermaid diagrams is strongly encouraged** (sequence, flowchart, C4). |
| `decision.rationale` | Explain *why*; use bullet lists, headers, diagrams |
| `decision.tradeoffs` | Acknowledged tradeoffs accepted with this decision |
| `confirmation.description` | Verification evidence and implementation proof |

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
| `approved_at` | string (date-time) or null | ❌ |
| `signature_id` | string or null | ❌ |
