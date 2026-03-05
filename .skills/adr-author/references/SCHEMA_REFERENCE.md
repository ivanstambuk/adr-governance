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

## Optional Top-Level Sections

| Section | Description |
|---------|-------------|
| `reviewers` | People who reviewed the ADR |
| `approvals` | Formal approvals with timestamps and signature IDs |
| `confirmation` | How the decision's implementation is verified; delivery artifact IDs |
| `requirements` | Embedded functional and non-functional requirements |
| `risk_assessment` | Identified risks with mitigation strategies |
| `dependencies` | Internal and external dependencies |
| `related_adrs` | Cross-references to other ADRs |
| `attachments` | Diagrams, runbooks, other supporting documents |
| `references` | External links and evidence |
| `lifecycle` | Review cadence, supersession chain, archival |
| `audit_trail` | Immutable event log (events: created, updated, reviewed, approved, rejected, superseded, deprecated, archived) |

## Key Validation Rules

1. `adr.id` must match `^ADR-[0-9]{4}$`
2. `adr.status` must be one of the defined enum values
3. `alternatives` must have `minItems: 2`
4. `decision.chosen_alternative` should match a name in `alternatives`
5. Requirement IDs: `^(F|NF)-[0-9]{3}$`
6. Risk IDs: `^R-[0-9]{3}$`
7. `audit_trail` events use defined enum values
