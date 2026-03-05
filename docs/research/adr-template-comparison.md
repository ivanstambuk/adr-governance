# ADR Template Comparison Research

> **Date:** 2026-03-05
> **Author:** Ivan Stambuk
> **Status:** Final
> **Repository:** `adr-governance`

---

## 1. Purpose

This document surveys and compares the major Architecture Decision Record (ADR) template formats in use today. The goal is to:

1. Catalogue the **structural sections** of each template
2. Identify **where our `adr-governance` schema** stands relative to the field
3. Produce a **feature comparison matrix**
4. Provide a **synthesis** with recommendations for our schema

---

## 2. Templates Surveyed

| # | Template | Origin | Year | Format | Primary Source |
|---|----------|--------|------|--------|----------------|
| 1 | **Nygard** | Michael Nygard blog post | 2011 | Markdown | [cognitect.com](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions) |
| 2 | **MADR 4.0** | `adr/madr` GitHub org | 2024 | Markdown + YAML frontmatter | [adr.github.io/madr](https://adr.github.io/madr/) |
| 3 | **Structured MADR (smadr)** | Robert Allen (zircote) | 2025 | Markdown + YAML frontmatter + JSON Schema | [smadr.dev](https://smadr.dev) |
| 4 | **Tyree–Akerman** | Jeff Tyree & Art Akerman, IEEE Software | 2005 | Prose / Template | IEEE Software 22(2), 2005 |
| 5 | **Y-Statements** | Olaf Zimmermann, SATURN 2012 | 2012 | Single structured sentence | [ozimmer.ch](https://ozimmer.ch) |
| 6 | **Alexandrian** | Pattern language tradition | ~2015 | Markdown (Pattern form) | [github.com/joelparkerhenderson/adr](https://github.com/joelparkerhenderson/architecture-decision-record) |
| 7 | **Business Case** | Joel Parker Henderson | ~2018 | Markdown | [github.com/joelparkerhenderson/adr](https://github.com/joelparkerhenderson/architecture-decision-record) |
| 8 | **adr-governance** | NovaTrust / this repo | 2026 | YAML + JSON Schema (Draft 2020-12) | `schemas/adr.schema.json` |

---

## 3. Template-by-Template Analysis

### 3.1 Nygard (2011) — The Original

The foundational ADR format. Intentionally minimal.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| Title | ✅ | Short noun phrase |
| Status | ✅ | `proposed`, `accepted`, `deprecated`, `superseded` |
| Context | ✅ | Forces at play — technical, political, social. Value-neutral language |
| Decision | ✅ | "We will…" — active voice, full sentences |
| Consequences | ✅ | What becomes easier or harder. Positive and negative, no sub-structure |

**Characteristics:**
- **5 sections, all required.** No optional sections.
- **No metadata** — no date, no author, no tags, no ID.
- **No alternatives analysis** — only the chosen decision is recorded.
- **Flat consequences** — single narrative block, no structured sub-fields.
- **Design philosophy:** "Short enough to fit on one page." Append-only — never edit, only supersede.
- **Tooling:** `adr-tools` (npryce/adr-tools) provides CLI for file management.

**What it lacks:** Alternatives comparison, risk assessment, author tracking, dates, formal review/approval, compliance implications, deployment planning, monitoring, audit trail.

---

### 3.2 MADR 4.0 (2024) — Markdown Any Decision Record

The most widely adopted structured ADR template. Maintained by the `adr` GitHub organization. Olaf Zimmermann is a contributor.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| YAML Frontmatter | Optional | `status`, `date`, `decision-makers`, `consulted`, `informed` |
| Title (H1) | ✅ | Represents problem + solution |
| Context and Problem Statement | ✅ | Free-form or illustrative story |
| Decision Drivers | Optional | Bullet list of forces/concerns |
| Considered Options | ✅ | List of option titles |
| Decision Outcome | ✅ | Chosen option with `because` justification |
| → Consequences | Optional | `Good, because…` / `Bad, because…` / `Neutral, because…` |
| → Confirmation | Optional | How compliance with the ADR will be verified |
| Pros and Cons of the Options | Optional | Per-option breakdown: Good / Neutral / Bad bullets |
| More Information | Optional | Links, team agreement, realization timeline |

**Characteristics:**
- **~10 sections, 3 required.** Optional metadata in YAML frontmatter.
- **RACI-like stakeholder model** in frontmatter: `decision-makers`, `consulted`, `informed`.
- **Pros/Cons per option** — structured comparison of alternatives.
- **Consequences are labeled** — `Good, because…` / `Bad, because…` — but not sub-categorized (no security/compliance/operational split).
- **Confirmation section** — unique to MADR: "how will we verify this decision was implemented correctly?" (e.g., code review, ArchUnit test).
- **No risk assessment, no deployment plan, no monitoring, no audit trail.**
- **No formal approval workflow** — `decision-makers` is informational only.

---

### 3.3 Structured MADR / smadr (2025) — Machine-Readable Extension

An extension of MADR designed for machine consumption, AI tooling, and compliance auditing.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| YAML Frontmatter | ✅ | `title`, `description`, `type`, `category`, `tags`, `status`, `created`, `updated`, `author`, `project` |
| Optional Frontmatter | — | `technologies`, `audience`, `related` (links to other smadr files) |
| Extension Fields | — | `x-*` prefixed custom metadata |
| Status | ✅ | Markdown body — current decision status |
| Context | ✅ | Background, problem statement, current limitations |
| Decision Drivers | ✅ | Primary and secondary factors |
| Considered Options | ✅ | Per-option: description, characteristics, advantages, disadvantages, **risk assessment** |
| → Risk Assessment (per option) | ✅ | **Technical Risk** (Low/Med/High), **Schedule Risk**, **Ecosystem Risk** |
| Decision | ✅ | Chosen approach with implementation details |
| Consequences | ✅ | Positive, negative, neutral |
| Decision Outcome | ✅ | Summary with mitigations for negative consequences |
| Related Decisions | Optional | Links to related ADRs |
| Links | Optional | External resources |
| More Information | Optional | Date, source, references |
| **Audit** | Optional | **Compliance tracking with findings table** |

**Characteristics:**
- **Most structured of the Markdown-based templates.**
- **JSON Schema for frontmatter validation** — machine-parseable metadata.
- **Three-dimensional risk assessment per option** (Technical, Schedule, Ecosystem) — unique feature.
- **Audit section** for compliance tracking — SOC2, HIPAA, ISO 27001.
- **AI-ready** — explicitly designed for Claude Code, GitHub Copilot, Cursor integration.
- **No deployment plan, no monitoring, no SLA, no approval workflow.**
- **No structured security/compliance/operational implications** — these would go in free-text Consequences or Audit.

---

### 3.4 Tyree–Akerman (2005) — IEEE Enterprise Template

The most comprehensive traditional ADR template. Published in IEEE Software.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| Issue | ✅ | Design issue being addressed |
| Decision | ✅ | Chosen direction/position |
| Status | ✅ | `pending`, `decided`, `approved` |
| Group | ✅ | Category (integration, presentation, data, etc.) |
| Assumptions | ✅ | Cost, schedule, technology assumptions |
| Constraints | ✅ | Additional limitations imposed by the decision |
| Positions | ✅ | All viable alternatives with models/diagrams |
| Argument | ✅ | Reasoning for chosen position over alternatives |
| Implications | ✅ | Required follow-ups, new requirements, staff training |
| Related Decisions | ✅ | Links to connected architectural decisions |
| Related Requirements | ✅ | Mapping to business objectives |
| Related Artifacts | ✅ | Architecture/design/scope documents impacted |
| Related Principles | ✅ | Enterprise policies and principles influencing the decision |
| Notes | ✅ | Discussion items and issues raised |

**Characteristics:**
- **14 sections, most required.** The heaviest template.
- **Unique sections:** `Assumptions`, `Constraints`, `Related Principles`, `Related Artifacts`, `Notes`.
- **Enterprise governance-oriented:** explicit links to requirements, principles, and artifacts.
- **No structured consequences** — `Implications` is a single section.
- **No risk assessment, no deployment plan, no monitoring, no audit trail.**
- **No metadata** — no date, author, tags, or ID in the original template.
- **Criticism:** Feels bureaucratic for smaller decisions. 15+ sections is a high bar.

---

### 3.5 Y-Statements (2012) — Ultra-Minimal

A single structured sentence capturing the entire decision.

**Structure:**

```
In the context of {use case},
  facing {non-functional concern},
  we decided for {option}
  and neglected {alternatives},
  to achieve {quality benefit},
  accepting that {tradeoff/downside}
  [because {additional rationale}].
```

**Characteristics:**
- **1 "section" — a single sentence.** The most minimal format.
- **Forces extreme clarity** — you must compress the entire decision into one statement.
- **No metadata, no alternatives analysis, no risk assessment, no consequences breakdown.**
- **Best used as:** A summary or index entry, not as a standalone record.
- **Often combined with other templates** — Y-Statement as the abstract, MADR as the body.

---

### 3.6 Alexandrian (Pattern Language)

Inspired by Christopher Alexander's pattern language.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| Prologue (Summary) | ✅ | Brief overview |
| Discussion (Context) | ✅ | Problem, forces, background — written as a narrative |
| Solution (Decision) | ✅ | The architectural response |
| Consequences (Resulting Context) | ✅ | What changes after applying the solution |

**Characteristics:**
- **4 sections.** Narrative style — reads like a design pattern.
- **"Resulting Context"** explicitly frames consequences as the new context for future decisions.
- **Encourages linking** — patterns reference related patterns, forming a language.
- **No metadata, no alternatives, no risk, no approval, no deployment.**
- **Philosophy:** Decisions are patterns; the ADR log is a pattern language.

---

### 3.7 Business Case (Henderson)

Oriented toward management stakeholders and financial justification.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| Title | ✅ | Short imperative phrase |
| Status | ✅ | Standard status values |
| Evaluation Criteria | ✅ | What we're evaluating and why |
| Candidates to Consider | ✅ | All options with outlier notes |
| Research and Analysis | ✅ | Per-candidate deep dive |
| → Criteria Assessment | ✅ | Does/doesn't meet criteria and why |
| → Cost Analysis | ✅ | Licensing, training, operating, metering costs |
| → SWOT Analysis | ✅ | Strengths, Weaknesses, Opportunities, Threats per candidate |
| → Internal Opinions | ✅ | Team and stakeholder feedback |
| → External Opinions | Optional | Industry/community feedback |
| → Anecdotes | Optional | Real-world experience reports |
| Recommendation | ✅ | Final recommendation with specifics |

**Characteristics:**
- **Unique: SWOT analysis and cost analysis per candidate.** No other template does this.
- **Stakeholder-facing** — designed for management buy-in, not developer documentation.
- **No technical consequences, no risk assessment, no deployment, no monitoring.**
- **Heavy** — the deep-dive per candidate can be extensive.
- **Best used for:** Vendor selection, platform adoption, large-scale technology choices.

---

### 3.8 adr-governance (This Repo)

Our custom YAML-based meta-model with JSON Schema (Draft 2020-12) validation.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| `adr` (metadata) | ✅ | `id`, `title`, `status`, `created_at`, `last_modified`, `version`, `schema_version`, `project`, `component`, `tags`, `priority`, `decision_type` |
| `authors` | ✅ | Name, role, email (multiple) |
| `decision_owner` | ✅ | Single accountable person |
| `reviewers` | Optional | People who reviewed |
| `approvals` | Optional | Formal approvals with timestamps and signature IDs |
| `context` | ✅ | `summary`, `business_drivers`, `technical_drivers`, `constraints`, `assumptions` |
| `requirements` | Optional | `functional` (id + description), `non_functional` (id + description) |
| `alternatives` | ✅ | ≥2 options, each with `name`, `summary`, `pros`, `cons`, `estimated_cost`, `risk` |
| `decision` | ✅ | `chosen_alternative`, `rationale`, `tradeoffs`, `decision_date` |
| `consequences` | ✅ | `positive`, `negative` |
| → `security_implications` | Optional | `data_classification`, `encryption` (at_rest, in_transit, key_management), `access_control` (iam, least_priv), `audit` (logging, retention) |
| → `compliance_implications` | Optional | `regulatory_impact` (map), `required_controls` (list) |
| → `operational_implications` | Optional | `monitoring`, `runbooks`, `staffing` |
| `risk_assessment` | Optional | Risks with `id`, `description`, `likelihood`, `impact`, `mitigation`; `residual_risk` |
| `deployment` | Optional | `rollout_plan` (phases with criteria + duration), `testing` (unit, integration, performance, compliance), `rollback_plan` (criteria + steps) |
| `monitoring` | Optional | `metrics` (name, warning/critical thresholds), `alerts`, `sla` (availability, RPO, RTO) |
| `dependencies` | Optional | `internal`, `external` |
| `related_adrs` | Optional | `id`, `title`, `relationship` (supersedes, related, depends_on, etc.) |
| `attachments` | Optional | `diagrams`, `runbooks` |
| `references` | Optional | `title`, `url` |
| `lifecycle` | Optional | `review_cycle_months`, `next_review_date`, `superseded_by`, `supersedes`, `archival` |
| `audit_trail` | Optional | Append-only event log: `event`, `by`, `at`, `details` |

**Characteristics:**
- **Most comprehensive template in this survey.** 20+ top-level sections.
- **Machine-readable YAML** with JSON Schema validation.
- **Unique sections not found in any other template:**
  - `security_implications` (structured: encryption, access control, audit retention)
  - `compliance_implications` (structured: regulatory_impact map, required_controls list)
  - `operational_implications` (structured: monitoring, runbooks, staffing)
  - `deployment` (phased rollout plan with criteria, testing matrix, rollback plan)
  - `monitoring` (metrics with thresholds, alerts, SLA targets with RPO/RTO)
  - `audit_trail` (append-only event log with timestamps)
  - `approvals` (formal approval workflow with signature IDs)
  - `lifecycle` (review cadence, next review date, archival policy)
  - `schema_version` (pins ADR to specific schema version)
- **Formal approval workflow** — only template with `approvals` as a structured section.
- **Self-contained** — no external references needed to understand the decision.

---

## 4. Feature Comparison Matrix

Legend: ✅ = Present and structured | 🟡 = Present but free-text/minimal | ❌ = Absent

| Feature / Section | Nygard | MADR 4.0 | smadr | Tyree–Akerman | Y-Stmt | Alexandrian | Biz Case | **adr-governance** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Metadata** | | | | | | | | |
| Unique ID | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Title | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ | ✅ | ✅ |
| Status | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Date(s) | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Author(s) | ❌ | 🟡 | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Decision Owner | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Tags / Category | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Priority | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Decision Type | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Schema Version | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| JSON Schema Validation | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Context & Problem** | | | | | | | | |
| Problem Statement | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ | 🟡 | ✅ |
| Business Drivers | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Technical Drivers | ❌ | 🟡 | 🟡 | ❌ | ❌ | ❌ | ❌ | ✅ |
| Constraints | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Assumptions | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| Decision Drivers | ❌ | ✅ | ✅ | ❌ | 🟡 | ❌ | ❌ | ❌ |
| **Requirements** | | | | | | | | |
| Functional Requirements | ❌ | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | ✅ |
| Non-Functional Requirements | ❌ | ❌ | ❌ | 🟡 | 🟡 | ❌ | ❌ | ✅ |
| **Alternatives Analysis** | | | | | | | | |
| Multiple Options Listed | ❌ | ✅ | ✅ | ✅ | 🟡 | ❌ | ✅ | ✅ |
| Pros per Option | ❌ | ✅ | ✅ | 🟡 | ❌ | ❌ | 🟡 | ✅ |
| Cons per Option | ❌ | ✅ | ✅ | 🟡 | ❌ | ❌ | 🟡 | ✅ |
| Cost Estimate per Option | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Risk Rating per Option | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| SWOT per Option | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Decision** | | | | | | | | |
| Chosen Option | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Rationale | 🟡 | ✅ | ✅ | ✅ | 🟡 | 🟡 | ✅ | ✅ |
| Tradeoffs | 🟡 | 🟡 | 🟡 | ❌ | ✅ | ❌ | ❌ | ✅ |
| Decision Date | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Consequences** | | | | | | | | |
| Positive Consequences | 🟡 | ✅ | ✅ | 🟡 | 🟡 | 🟡 | ❌ | ✅ |
| Negative Consequences | 🟡 | ✅ | ✅ | 🟡 | ✅ | 🟡 | ❌ | ✅ |
| Neutral Consequences | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Security Implications (structured) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Compliance Implications (structured) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Operational Implications (structured) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Confirmation / Validation | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Governance** | | | | | | | | |
| Stakeholders (RACI-like) | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 |
| Reviewers | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Formal Approvals | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Audit Trail | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Risk & Compliance** | | | | | | | | |
| Risk Assessment (overall) | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ✅ |
| Risk per Option (3-dimensional) | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Residual Risk | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Compliance Audit Table | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Operational** | | | | | | | | |
| Deployment Plan (phased) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Testing Matrix | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Rollback Plan | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Monitoring (metrics + thresholds) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| SLA (availability, RPO, RTO) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Cross-References** | | | | | | | | |
| Related Decisions | ❌ | 🟡 | ✅ | ✅ | ❌ | 🟡 | ❌ | ✅ |
| Related Requirements | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | 🟡 |
| Related Principles | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Related Artifacts | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| External References | ❌ | 🟡 | ✅ | ❌ | ❌ | ❌ | 🟡 | ✅ |
| Dependencies (int/ext) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Lifecycle** | | | | | | | | |
| Review Cadence | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Supersession Chain | 🟡 | 🟡 | 🟡 | ❌ | ❌ | ❌ | ❌ | ✅ |
| Archival Policy | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 5. Unique Contributions of Each Template

| Template | Unique Contribution | Adoption |
|----------|-------------------|----------|
| **Nygard** | Invented the ADR concept. Proved that minimal format works. | Universal — basis for all others |
| **MADR** | `Confirmation` section ("how do we verify this?"). RACI-like stakeholder model. `Neutral` consequences. | Very high — most GitHub ADR repos use MADR |
| **smadr** | 3-dimensional risk assessment per option (Technical/Schedule/Ecosystem). JSON Schema validation. Audit table for compliance. AI-tooling-ready. Extension fields (`x-*`). | Emerging (2025) |
| **Tyree–Akerman** | `Related Principles`, `Related Artifacts`, `Related Requirements`, `Assumptions`. Enterprise governance depth. | Moderate — enterprise/academic |
| **Y-Statements** | Compression of entire decision into one sentence. Forces extreme clarity. | Niche — used as summaries |
| **Alexandrian** | "Resulting Context" framing — consequences as input for next decision. | Niche — pattern language community |
| **Business Case** | SWOT analysis and cost analysis per candidate. Management-facing. External opinions section. | Moderate — vendor selection |
| **adr-governance** | Structured security/compliance/operational implications. Phased deployment plans with rollback. Monitoring with metric thresholds and SLA. Formal approval workflow. Lifecycle management (review cadence, archival). Append-only audit trail. | New — this repo only |

---

## 6. Analysis: Where Standard Templates Fall Short

### 6.1 No Template Has Structured Implications

Every template treats consequences as prose or bullet points. No template in the field provides:
- **Structured security implications** with data classification, encryption specifics, access control details, and audit retention periods
- **Structured compliance implications** with regulatory-to-impact mapping and required controls
- **Structured operational implications** with monitoring requirements, runbook references, and staffing needs

These exist only in our `adr-governance` schema. The closest competitor is **smadr**'s Audit section, but it's a compliance findings table, not a structured implications model.

### 6.2 No Template Has Deployment/Rollback Planning

None of the seven standard templates include:
- Phased rollout criteria
- Testing matrices (unit, integration, performance, compliance)
- Rollback criteria and procedures

These are typically in separate runbooks. Our schema embeds them for self-containment.

### 6.3 No Template Has Monitoring or SLA

Only our schema links a decision to its runtime monitoring:
- Named metrics with warning/critical thresholds
- Alert routing
- SLA targets (availability, RPO, RTO)

### 6.4 Two Features We're Missing

| Feature | Source | Value |
|---------|--------|-------|
| **Confirmation** | MADR 4.0 | "How will we verify this decision was implemented correctly?" — links decision to validation (code review, automated test, ArchUnit). Useful for ensuring decisions don't rot. |
| **Decision Drivers** (explicit) | MADR 4.0, smadr | Our `context` has `business_drivers` and `technical_drivers` but not a unified `decision_drivers` list. MADR's approach of listing drivers as enumerated forces is slightly more scannable, though our split into business/technical is more informative. |

---

## 7. Synthesis: Recommendations for Our Schema

### 7.1 What to Keep (Our Schema is Best-in-Class)

Our `adr-governance` schema is the most comprehensive ADR meta-model in the field. The following sections are **unique and valuable** — no other template provides them:

1. **`security_implications`** — structured sub-fields for data classification, encryption, access control, and audit retention. Essential for regulated environments.
2. **`compliance_implications`** — regulatory impact mapping and required controls list. Critical for PSD2/GDPR/DORA compliance.
3. **`operational_implications`** — monitoring, runbooks, staffing. Bridges the gap between architecture decision and operational reality.
4. **`deployment`** — phased rollout, testing matrix, rollback plan. Ensures decisions are not just recorded but actionable.
5. **`monitoring`** — metrics with thresholds, alerts, SLA. Links decision to production observability.
6. **`approvals`** with signature IDs — formal governance for regulated environments.
7. **`audit_trail`** — append-only event log. Satisfies auditability requirements.
8. **`lifecycle`** — review cadence and archival. Prevents decision rot.
9. **`schema_version`** — pins each ADR to a specific schema version. Future-proofs the format.

These are all enterprise-grade extensions that we invented. They should be preserved and documented as the **"Enterprise ADR extensions"** of this project.

### 7.2 What to Consider Adding

| Candidate Field | Source Template | Recommendation | Rationale |
|----------------|----------------|----------------|-----------|
| **`confirmation`** | MADR 4.0 | ✅ **Add** | Answers "how do we verify this decision was implemented?" Lightweight field (free text) with high value for preventing decision rot. Could be a field under `decision` or a new top-level section. |
| **`neutral_consequences`** | MADR 4.0 | ❌ **Skip** | Neutral consequences are rarely informative. Our positive/negative split is sufficient. |
| **`decision_drivers`** (unified list) | MADR / smadr | ❌ **Skip** | Our `business_drivers` + `technical_drivers` split is more informative than a flat list. |
| **`related_principles`** | Tyree–Akerman | ⚠️ **Consider** | Links decisions to enterprise architecture principles. Valuable for organizations with a formal principles registry (e.g., TOGAF). Add if/when we have a principles registry. |
| **`swot_per_option`** | Business Case | ❌ **Skip** | Overlaps with our pros/cons/cost/risk per alternative. SWOT is a management lens, not an engineering lens. |
| **`risk_per_option` (3D)** | smadr | ⚠️ **Consider** | smadr's Technical/Schedule/Ecosystem risk model is interesting but our per-option `risk` field (low/medium/high/critical) combined with the overall `risk_assessment` section provides similar coverage. The 3D model could be adopted as an alternative structure for the per-option risk field if our users need more granularity. |
| **`extension_fields` (x-*)** | smadr | ✅ **Add** | Allowing custom `x-*` prefixed fields in the schema gives teams flexibility without breaking validation. Simple to implement in JSON Schema via `patternProperties`. |

### 7.3 What to Document

Our `security_implications`, `compliance_implications`, and `operational_implications` fields are **the most novel contribution** of this schema. They should be explicitly documented as:

> **Enterprise ADR Extensions** — structured consequence sub-sections designed for regulated environments where decisions must be traceable to security controls, regulatory requirements, and operational readiness. These are not part of any standard ADR template; they are a custom extension of the `adr-governance` meta-model.

This prevents future confusion about whether they come from a standard.

---

## 8. Template Positioning Map

```
                    ┌─────────────────────────────────────────────┐
                    │              COMPREHENSIVENESS               │
   Minimal ◄───────┼─────────────────────────────────────────────►│ Maximal
                    │                                             │
                    │  Y-Stmt    Nygard    Alexandrian    MADR    │
                    │   (1)      (5)        (4)          (10)    │
                    │                                             │
                    │                      smadr      Tyree-Akerman
                    │                      (15)         (14)      │
                    │                                             │
                    │                        Business Case        │
                    │                           (12)              │
                    │                                             │
                    │                          adr-governance     │
                    │                              (20+)          │
                    └─────────────────────────────────────────────┘

   Human-readable ◄──────────────────────────────────────────────► Machine-readable
                    │                                             │
                    │  Nygard  Alexandrian  MADR    smadr         │
                    │  Y-Stmt  Tyree-Ak    Biz Case              │
                    │                                             │
                    │                          adr-governance     │
                    │                          (YAML + JSON Schema)│
                    └─────────────────────────────────────────────┘
```

---

## 9. Conclusion

Our `adr-governance` schema sits at the **maximum comprehensiveness** end of the ADR template spectrum. It is the only template that combines:

- MADR-style alternatives analysis with pros/cons
- Tyree–Akerman-style enterprise governance (assumptions, constraints, related artifacts)
- Structured implications (security, compliance, operational) — **unique to us**
- Deployment planning with rollback — **unique to us**
- Runtime monitoring with SLA — **unique to us**
- Formal approval workflow — **unique to us**
- Machine-readable YAML with JSON Schema validation

The tradeoff is **weight**: a full `adr-governance` ADR is significantly heavier than a Nygard or MADR record. This is acceptable for our use case (enterprise IAM decisions in regulated financial services) but would be overkill for a startup documenting database choices.

The only gap worth closing immediately is the **`confirmation`** field from MADR 4.0, and optionally the **`x-*` extension fields** from smadr for custom metadata flexibility.

---

## References

1. Nygard, M. (2011). "Documenting Architecture Decisions." [cognitect.com](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions)
2. MADR 4.0 (2024). [adr.github.io/madr](https://adr.github.io/madr/)
3. Structured MADR (2025). [smadr.dev](https://smadr.dev)
4. Tyree, J. & Akerman, A. (2005). "Architecture Decisions: Demystifying Architecture." IEEE Software 22(2).
5. Zimmermann, O. (2012). "Architectural Decisions as Reusable Design Assets." SATURN 2012. [ozimmer.ch](https://ozimmer.ch)
6. Henderson, J.P. "Architecture Decision Record." [github.com/joelparkerhenderson](https://github.com/joelparkerhenderson/architecture-decision-record)
7. Alexander, C. (1977). "A Pattern Language." Oxford University Press.
8. ISO/IEC/IEEE 42030:2019. "Architecture Evaluation Framework."
9. ThoughtWorks Technology Radar. "Lightweight Architecture Decision Records." [thoughtworks.com](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
10. Spotify Engineering. "When Should I Write an Architecture Decision Record?" [atspotify.com](https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record/)
