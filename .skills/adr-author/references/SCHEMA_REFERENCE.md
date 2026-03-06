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
| `approvals` | Formal approvals with timestamps, platform identities, and signature IDs |
| `requirements` | Embedded functional and non-functional requirements |
| `dependencies` | Internal and external dependencies |
| `references` | External links and evidence |
| `lifecycle` | Review cadence, supersession chain, archival |
| `audit_trail` | Immutable event log (events: created, updated, reviewed, approved, rejected, deferred, superseded, deprecated, archived) |

## Key Validation Rules

1. `adr.id` must match `^ADR-[0-9]{4}(-[a-z0-9]+)+$` — slug is mandatory (e.g. `ADR-0001-dpop-over-mtls`)
2. `adr.status` must be one of the defined enum values (see below)
3. `alternatives` must have `minItems: 2`
4. `decision.chosen_alternative` should match a name in `alternatives`
5. Requirement IDs: `^(F|NF)-[0-9]{3}$`
6. `audit_trail` events use defined enum values (see below)
7. Extension fields: any key starting with `x-` is allowed at the top level

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
| `alternatives[].summary` | Describe each option; embed comparison diagrams |
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
| `identity` | string | ❌ (needed for CI verification) |
| `approved_at` | string (date-time) or null | ❌ |
| `signature_id` | string or null | ❌ |
