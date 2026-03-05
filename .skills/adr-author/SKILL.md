---
name: adr-author
description: >
  Author, review, and validate Architecture Decision Records (ADRs) using a
  governed YAML meta-model. Use when the user asks to create a new ADR,
  review an existing ADR, validate ADR YAML files against the schema, or
  needs guidance on the ADR governance process. Covers the full lifecycle:
  drafting, review, approval, supersession, and archival.
license: MIT
metadata:
  author: "ivanstambuk"
  version: "1.0"
---

# ADR Author Skill

## When to use this skill

Use this skill when the user:
- Wants to **create a new ADR** (architecture decision record)
- Wants to **review or audit an existing ADR** for completeness
- Needs to **validate** an ADR YAML file against the schema
- Asks about the **ADR governance process** or lifecycle
- Wants to **supersede, deprecate, or archive** an existing ADR
- Needs to understand the **ADR meta-model** fields and allowed values

## Core principles

1. **Self-contained**: Every ADR must embed all context (requirements, alternatives, risk, compliance) so it can be understood without external documents.
2. **Schema-governed**: All ADRs must validate against `schemas/adr.schema.json` (JSON Schema Draft 2020-12).
3. **At least two alternatives**: Every decision requires evaluation of ≥2 alternatives with pros, cons, cost, and risk.
4. **Immutable audit trail**: The `audit_trail` section is append-only. Never delete or modify existing entries.
5. **Relationships are navigational, not structural**: `related_adrs` are cross-reference pointers. Each ADR remains fully self-contained.

## How to create a new ADR

### Step 1: Determine the next ADR ID

Check existing ADR files in the `decisions/` directory (or `examples/` for reference). The ID format is `ADR-NNNN` (zero-padded 4 digits). Use the next sequential number.

### Step 2: Gather context from the user

Ask the user for:
1. **Title**: What decision is being made? (10-200 characters)
2. **Decision type**: `technology` | `process` | `organizational` | `vendor` | `security` | `compliance`
3. **Priority**: `low` | `medium` | `high` | `critical`
4. **Context**: What problem are we solving? What are the business and technical drivers?
5. **Constraints**: What are the non-negotiable boundaries?
6. **Alternatives**: At least 2 options with pros, cons, estimated cost, and risk level
7. **Recommendation**: Which alternative and why?
8. **Summary** (`adr.summary`): 2-4 sentence elevator pitch for stakeholder triage (max 500 chars). This is distinct from `context.summary`, which is the full narrative problem statement.
9. **Confidence**: `low` | `medium` | `high` — how confident are we in this decision?

### Step 3: Generate the ADR YAML

Use the template at `assets/adr-template.yaml` as the starting point. Fill in all required sections:

- `adr` — metadata (id, title, status: `proposed`, timestamps, tags, priority, decision_type)
- `authors` — who is writing this
- `decision_owner` — who is accountable
- `context` — summary, business_drivers, technical_drivers, constraints, assumptions
- `requirements` — embedded functional and non-functional requirements
- `alternatives` — at least 2, each with name, summary, pros, cons, estimated_cost, risk, rejection_rationale (for non-chosen alternatives)
- `decision` — chosen_alternative, rationale, tradeoffs, decision_date, confidence
- `consequences` — positive, negative
- `risk_assessment` — identified risks with likelihood, impact, mitigation
- `audit_trail` — initial `created` event

### Step 4: Validate

Run the validation script to check the YAML against the JSON Schema:

```bash
python3 scripts/validate-adr.py decisions/ADR-NNNN-short-title.yaml
```

### Step 5: File naming convention

```
decisions/ADR-NNNN-short-kebab-case-title.yaml
```

Example: `decisions/ADR-0007-adopt-passkeys-for-workforce-mfa.yaml`

## How to review an existing ADR

When reviewing, check for:

1. **Completeness**: All required sections present (see schema `required` fields)
2. **Alternative quality**: At least 2 alternatives with substantive pros/cons (not just "good" / "bad")
3. **Rationale strength**: Does the rationale clearly connect to the drivers and requirements?
4. **Risk coverage**: Are the major risks identified with realistic mitigations?
5. **Compliance**: Are regulatory implications addressed if the decision touches data, access, or infrastructure?
6. **Consistency**: Does the `chosen_alternative` name match an entry in `alternatives`? Are `lifecycle.supersedes`/`superseded_by` consistent?
7. **Audit trail**: Is the trail consistent with the status?
8. **Rejection rationale**: For each non-chosen alternative, is `rejection_rationale` populated explaining why it was not selected?
9. **Diagram quality**: Are embedded Mermaid diagrams used where a visual would clarify architecture or flow?

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

- `context.summary` — narrative problem statement; embed architecture diagrams here
- `alternatives[].summary` — describe each option; embed comparison diagrams
- `decision.rationale` — explain *why*; use bullet lists, headers, or diagrams
- `decision.tradeoffs` — what was given up
- `confirmation.description` — verification evidence

Use YAML literal block scalars (`|`) for multiline content. Example:

```yaml
context:
  summary: |
    The system currently uses approach X.

    ```mermaid
    graph LR
        A --> B --> C
    ```

    We need to decide between X and Y.
```

## Reference documentation

- See [the glossary](../../docs/glossary.md) for all enum values and term definitions
- See [the JSON Schema](references/SCHEMA_REFERENCE.md) for the full meta-model specification
- See example ADRs in the repository's `examples/` directory for well-formed samples

## Validation

The `scripts/validate-adr.py` script validates any ADR YAML file against the JSON Schema:

```bash
# Validate a single ADR
python3 scripts/validate-adr.py path/to/ADR-0001.yaml

# Validate all ADRs in a directory
python3 scripts/validate-adr.py decisions/
```

The script exits with code 0 if valid, 1 if validation errors are found.
