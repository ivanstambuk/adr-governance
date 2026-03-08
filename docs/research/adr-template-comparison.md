# ADR Template Comparison Research

> **Date:** 2026-03-05
> **Author:** Ivan Stambuk
> **Status:** Final — HISTORICAL REFERENCE
> **Repository:** `adr-governance`

> ⚠️ **This document was created during the initial schema design phase and may reference features that were subsequently adopted, modified, or removed (e.g., `risk_assessment` was removed, `summary` and `rejection_rationale` were adopted). Refer to the current [`schemas/adr.schema.json`](../../schemas/adr.schema.json) as the source of truth.**

---

## Table of Contents

- [1. Purpose](#1-purpose)
- [2. Templates Surveyed](#2-templates-surveyed)
- **Template-by-Template Analysis**
  - [3.1 Nygard (2011)](#31-nygard-2011--the-original)
  - [3.2 MADR 4.0 (2024)](#32-madr-40-2024--markdown-any-decision-record)
  - [3.3 smadr (2025)](#33-structured-madr--smadr-2025--machine-readable-extension)
  - [3.4 Tyree–Akerman (2005)](#34-tyreeakerman-2005--ieee-enterprise-template)
  - [3.5 Y-Statements (2012)](#35-y-statements-2012--ultra-minimal)
  - [3.6 Alexandrian](#36-alexandrian-pattern-language)
  - [3.7 Business Case (Henderson)](#37-business-case-henderson)
  - [3.8 Planguage (Tom Gilb)](#38-planguage-tom-gilb)
  - [3.9 EdgeX Foundry](#39-edgex-foundry-linux-foundation)
  - [3.10 Merson (CMU/SEI)](#310-merson-cmusei)
  - [3.11 NHS Wales](#311-nhs-wales-gig-cymru)
  - [3.12 Gareth Morgan](#312-gareth-morgan-solution-architecture-decisions)
  - [3.13 DRF](#313-drf--decision-reasoning-format-reasoning-formats)
  - [3.14 adr-governance](#314-adr-governance-this-repo)
- [4. Feature Comparison Matrix](#4-feature-comparison-matrix)
- [5. Unique Contributions](#5-unique-contributions-of-each-template)
- **Analysis: Where Templates Fall Short**
  - [6.1 No Structured Implications](#61-no-template-has-structured-implications)
  - [6.2 No Deployment/Rollback Planning](#62-no-template-has-deploymentrollback-planning)
  - [6.3 No Monitoring or SLA](#63-no-template-has-monitoring-or-sla)
  - [6.4 No Governance Enforcement](#64-no-template-has-decision-governance-enforcement--except-morgan)
  - [6.5 No Structured Impact Assessment](#65-no-template-has-structured-impact-assessment--except-edgex)
  - [6.6 No Rejected Alternative Rationale](#66-no-template-captures-rationale-for-rejected-alternatives--except-merson-and-drf)
- **Synthesis**
  - [7.1 Where Our Schema Leads](#71-where-our-schema-leads)
  - [7.2 Features Inspired by Others](#72-features-inspired-by-other-templates)
  - [7.3 Features Evaluated and Excluded](#73-features-evaluated-and-excluded)
- [8. Template Positioning Map](#8-template-positioning-map)
- [9. Conclusion](#9-conclusion)
- **ADR Ecosystem Insights**
  - [10.1 Fitness Functions](#101-fitness-functions-for-decisions-as-code)
  - [10.2 Decision Guardian](#102-decision-guardian--pr-level-enforcement)
  - [10.3 Teamwork Advice](#103-teamwork-advice-henderson)
  - [10.4 Related Formalisms](#104-related-formalisms)
  - [10.5 Company-Specific Guidance](#105-company-specific-adr-guidance)
  - [10.6 Architectural Decisions — The Making Of](#106-architectural-decisions--the-making-of-zimmermann)
  - [10.7 Skeptical Architecture](#107-skeptical-architecture-cervantes--woods)
  - [10.8 Architectural Retrospectives](#108-architectural-retrospectives-cervantes--woods)
  - [10.9 Microsoft Azure — Confidence Level](#109-microsoft-azure--confidence-level)
- [References](#references)

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
| 8 | **Planguage** | Tom Gilb (via Henderson repo) | ~2012 | Keyword-structured text | [ICCGI 2012 Tutorial](https://www.iaria.org/conferences2012/filesICCGI12/Tutorial%20Specifying%20Effective%20Non-func.pdf) |
| 9 | **EdgeX Foundry** | Linux Foundation EdgeX project | ~2020 | Markdown | [edgexfoundry.org](https://docs.edgexfoundry.org/2.3/design/adr/template/) |
| 10 | **Merson** | Paulo Merson (CMU/SEI) | 2023 | Markdown | [github.com/pmerson/ADR-template](https://github.com/pmerson/ADR-template) |
| 11 | **NHS Wales** | GIG Cymru / NHS Wales | ~2024 | Markdown (MkDocs-flavored) | [github.com/joelparkerhenderson/adr](https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-gig-cymru-nhs-wales) |
| 12 | **Gareth Morgan** | Gareth Morgan (Solution Architecture) | 2024 | Markdown + HTML tables | [linkedin.com](https://www.linkedin.com/pulse/solution-architecture-decisions-gareth-morgan-0r5xe/) |
| 13 | **DRF** | reasoning-formats org | 2024 | YAML/JSON (dual spec: DRF + CRF) | [github.com/reasoning-formats](https://github.com/reasoning-formats/reasoning-formats) |
| 14 | **adr-governance** | NovaTrust / this repo | 2026 | YAML + JSON Schema (Draft 2020-12) | `schemas/adr.schema.json` |

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

### 3.8 Planguage (Tom Gilb)

A decision template adapted from Tom Gilb's "Planguage" — a planning language originally designed for specifying non-functional requirements with quantitative rigor.

**Sections (Keywords):**

| Section (Keyword) | Required | Content |
|---------|----------|---------|
| Tag | ✅ | Unique, persistent identifier |
| Gist | ✅ | Brief summary of the requirement or area addressed |
| Requirement | ✅ | The text detailing the requirement itself |
| Rationale | ✅ | Reasoning that justifies the requirement |
| Priority | ✅ | Statement of priority and claim on resources |
| Stakeholders | ✅ | Parties materially affected by the requirement |
| Status | ✅ | `draft`, `reviewed`, `committed`, etc. |
| Owner | ✅ | Person responsible for implementing |
| Author | ✅ | Person who wrote the requirement |
| Revision | ✅ | Version number for the statement |
| Date | ✅ | Date of the most recent revision |
| Assumptions | ✅ | Anything that could cause problems if untrue now or later |
| Risks | ✅ | Anything that could cause malfunction, delay, or negative impacts |
| Defined | Optional | Definition of a term (recommends using a glossary instead) |

**Characteristics:**
- **QA/requirements-engineering lens.** The only ADR template rooted in non-functional requirements specification methodology.
- **Quantitative mindset.** Planguage was designed for measurable quality attributes — e.g., "Response time ≤ 200ms for 95th percentile." This influences the template toward precision.
- **"Tag" as persistent ID** — similar to our `adr.id`, predating all other templates' use of IDs.
- **Explicit `Assumptions` and `Risks`** — shared with Tyree–Akerman. Unique among lightweight templates.
- **`Owner` vs `Author` distinction** — separates who wrote it from who is accountable. Only our schema and this template make this distinction.
- **No alternatives analysis, no consequences, no deployment, no monitoring.**
- **Niche adoption.** Primarily used in Gilb's consulting practice and academic settings. Not widely adopted in open-source ADR workflows.

---

### 3.9 EdgeX Foundry (Linux Foundation)

The official ADR template for EdgeX Foundry, a Linux Foundation open-source IoT platform. Used for all architecturally significant changes to the EdgeX codebase.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| Submitters | ✅ | Name (Organization) — who proposed the ADR |
| Change Log | ✅ | State transitions with dates and PR URLs |
| Referenced Use Case(s) | ✅ | Links to approved use case documents |
| Context | ✅ | Architectural significance justification + high-level approach |
| Proposed Design | ✅ | Services/modules impacted, model/DTO changes, API changes, config changes, devops impact |
| Considerations | ✅ | Alternatives, concerns, issues raised in debate; resolution status |
| Decision | ✅ | Implementation details, caveats, future considerations, unmet requirements |
| Other Related ADRs | Optional | Links with relevance annotations |
| References | Optional | External resources |

**Characteristics:**
- **Change Log with PR links.** The only template that mandates a structured change log with pull request URLs for each state transition. This creates a **built-in audit trail** via git.
- **Use case traceability.** Mandates `Referenced Use Case(s)` — the ADR must link to at least one approved use case. This enforces requirements traceability.
- **Impact-analysis-oriented `Proposed Design`.** Explicitly asks for: services/modules impacted, model/DTO changes, API impact, configuration impact, and devops impact. This is a structured **impact assessment** — unique among templates.
- **`Considerations` as debate log.** Records alternatives and concerns raised during review, with resolution notes. Functions as a lightweight decision journal.
- **No structured consequences, no risk assessment, no monitoring, no formal approval.**
- **Significant adoption.** Used by a major Linux Foundation project with dozens of contributors and enterprise backing.

---

### 3.10 Merson (CMU/SEI)

A Nygard-derived template by Paulo Merson of Carnegie Mellon's Software Engineering Institute. Famous for explicitly separating **Rationale** as its own section.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| Title (with number) | ✅ | "ADR N: brief decision title" |
| Context (in body) | ✅ | Forces that influence the decision (technological, cost, project-local) |
| Decision | ✅ | Response to the forces. Active voice: "We will…" |
| Rationale | ✅ | **Why** the decision was made. Also covers rationale for significant rejected alternatives. May include assumptions, constraints, evaluation results. |
| Status | ✅ | `Proposed`, `Accepted`, `Deprecated`, `Superseded` |
| Consequences | ✅ | Resulting context. All consequences, not just positive. |

**Characteristics:**
- **Explicit `Rationale` section** — the defining innovation. Merson's argument: "Why is more important than how" (Richards & Ford, *Fundamentals of Software Architecture*). In Nygard's template, rationale is buried in Context or Decision. Merson forces it to stand alone.
- **Rationale covers rejected alternatives** — the rationale section explicitly includes reasoning for significant alternatives that were *not* chosen. This partially compensates for the lack of a formal alternatives section.
- **Lean (5 sections).** Only one section more than Nygard, but the added section is arguably the most important.
- **SEI backing.** Associated with *Documenting Software Architectures: Views and Beyond* (Bass, Clements, Kazman). Used in O'Reilly architecture katas (Farmacy Food).
- **No metadata, no alternatives list, no risk assessment, no deployment, no monitoring.**
- **Moderate adoption.** Popular in educational settings and architecture kata competitions.

---

### 3.11 NHS Wales (GIG Cymru)

An ADR template designed by and for NHS Wales (GIG Cymru), a national healthcare system. Notable for coming from a **regulated public-sector** environment where decisions must withstand audit and governance scrutiny.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| Title | ✅ | Free-form title |
| Status (admonition) | ✅ | `Proposed`, `Under Review`, `Accepted`, `Rejected`, `Superseded`, `Deprecated` |
| Updated (date) | ✅ | ISO 8601 date |
| Summary | ✅ | Executive summary / elevator pitch (2–4 sentences) |
| Drivers | ✅ | Why this decision is being made *now* — motivations, needs, problems |
| Options | ✅ | Factual description of each option (no opinions — analysis is separate) |
| Options Analysis | ✅ | Per-option assessment: Pro / Con / Other; considers cost, complexity, risks, alignment, impact |
| Recommendation | ✅ | Final decision with explicit justification against drivers |
| → Consequences | Optional | Expected outcomes: Pro / Con / Other |
| → Confirmation | Optional | How implementation will be verified + ongoing compliance ensured + metrics for success + ownership |
| More Information | Optional | Supplementary context, participants, consensus process, re-evaluation triggers |

**Characteristics:**
- **Fact/opinion separation.** `Options` is strictly factual; `Options Analysis` is where judgment lives. This separation reduces cognitive bias during option presentation.
- **Extended `Confirmation` section.** Goes beyond MADR's confirmation by asking: "Who is responsible for overseeing this, and what happens if the decision is not followed?" — explicit ownership and enforcement.
- **`Drivers` as temporal motivator.** Not just "what are the forces" but "why *now*" — adds urgency context.
- **6 statuses** — includes `Under Review` and `Deprecated` alongside the standard set. Most templates have 3–4.
- **MkDocs integration.** Uses MkDocs admonition syntax for status display, suggesting tight integration with documentation-as-code pipelines.
- **Healthcare governance context.** Designed for NHS digital architecture teams where decisions must satisfy clinical safety, data protection (UK GDPR), and NHS Digital standards.

---

### 3.12 Gareth Morgan (Solution Architecture Decisions)

A template by Gareth Morgan focused on solution architecture decisions with a strong governance and visual comparison emphasis.

**Sections:**

| Section | Required | Content |
|---------|----------|---------|
| Title (with number) | ✅ | `[000] Title` — numbered for cataloging |
| Context | ✅ | Problem(s) the ADR addresses and why they exist |
| Decided Approach | ✅ | The architecturally significant decision and how it addresses the problems |
| Consequences | ✅ | Impact on architecture characteristics and functional requirements |
| Governance | ✅ | How outcomes will be monitored; how compliance will be ensured |
| Options Analysis | Optional | Trade-off analysis with traffic-light comparison matrices |
| → High-Level Overview | Optional | Summary matrix (Ease of Implementation, Timescales, Strategic Value) |
| → Functional Requirements | Optional | Per-scenario fit matrix across options |
| → Non-Functional Requirements | Optional | Per-architecture-characteristic fit matrix across options |

**Characteristics:**
- **Explicit `Governance` section.** The only template with a dedicated governance section asking: *"How will the outcomes of this decision be monitored? How will compliance with this decision be ensured?"* This bridges the gap between decision-making and decision-enforcement.
- **Traffic-light comparison matrices.** Uses color-coded HTML tables (green/amber/red with +/- prefixes) for visual option comparison across three dimensions: high-level summary, functional requirements, and non-functional requirements. Highly stakeholder-friendly.
- **Architecture characteristics framing.** Non-functional requirements are explicitly framed as "architecture characteristics" (à la Richards & Ford), assessed per option.
- **Strategic Value assessment.** The high-level overview matrix includes "Strategic Value" — no other template evaluates options against strategic/tactical positioning.
- **No metadata (beyond number), no risk assessment, no deployment, no monitoring, no audit trail.**

---

### 3.13 DRF — Decision Reasoning Format (reasoning-formats)

A vendor-neutral, machine-readable YAML/JSON format for structured decision documentation. Not an ADR template per se, but a **complementary specification** designed to add structured reasoning to decisions.

**Structure (two complementary specs):**

| Spec | Purpose | Key Fields |
|------|---------|------------|
| **DRF** (Decision Reasoning Format) | Documents what was decided and why | `id`, `title`, `intent`, `context` (constraints with source, objectives with priority), `reasoning` (patterns: risk-based, comparative), `assumptions`, `tensions` (tradeoffs), `synthesis` (decision + rationale + alternatives), `meta` (status, timestamps) |
| **CRF** (Context Reasoning Format) | Models organizational knowledge as a graph | `entities` (organizations, systems, policies, facts, capabilities), `relationships` (owns, depends_on, constrains, supersedes), `validity` (temporal bounds), `provenance` |

**Characteristics:**
- **Reasoning-first philosophy.** Captures *how* and *why*, not just *what*. Explicitly models assumptions, tensions/tradeoffs, and reasoning patterns used.
- **Organizational context as knowledge graph.** CRF creates a separate, referenceable graph of policies, systems, and constraints. Decisions are validated against this context.
- **Context validation.** DRF decisions can reference CRF entities for automatic conflict detection (e.g., "this decision conflicts with the Kubernetes Moratorium policy"). Advisory, not blocking.
- **Bidirectional updates.** Decisions produce new organizational facts that flow back into CRF — the decision log feeds the organizational knowledge base.
- **Constraint sourcing.** Each constraint carries a `source` (regulatory, budget, technical) — more granular than our `context.constraints` field.
- **Draft status (v0.1.0).** Still stabilizing core concepts. No significant adoption yet.
- **Closest to our schema** in philosophy (machine-readable, validation-oriented, structured reasoning) but with a different architectural bet: two complementary specs vs. one unified schema.

---

### 3.14 adr-governance (This Repo)

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
| `architecturally_significant_requirements` | Optional | `functional` (id + description), `non_functional` (id + description) |
| `alternatives` | ✅ | ≥2 options, each with `name`, `description`, `pros`, `cons`, `estimated_cost`, `risk` |
| `decision` | ✅ | `chosen_alternative`, `rationale`, `tradeoffs`, `decision_date` |
| `consequences` | ✅ | `positive`, `negative` |
| `confirmation` | Optional | `description` (free text), `artifacts` (list of verification artifact IDs) |
| `dependencies` | Optional | `internal`, `external` |
| `references` | Optional | External links and evidence |
| `lifecycle` | Optional | `review_cycle_months`, `next_review_date`, `superseded_by`, `supersedes`, `archival` |
| `audit_trail` | Optional | Append-only event log: `event`, `by`, `at`, `details` |

**Characteristics:**
- **Most comprehensive template in this survey.** ~15 top-level sections.
- **Machine-readable YAML** with JSON Schema validation.
- **Unique sections not found in any other template:**
  - `confirmation` (description + verification artifact IDs — inspired by MADR 4.0 / NHS Wales)
  - `audit_trail` (append-only event log with timestamps)
  - `approvals` (formal approval workflow with signature IDs)
  - `lifecycle` (review cadence, next review date, archival policy)
  - `schema_version` (pins ADR to specific schema version)
- **Formal approval workflow** — only template with `approvals` as a structured section.
- **Self-contained** — no external references needed to understand the decision.

---

## 4. Feature Comparison Matrix

Legend: ✅ = Present and structured | 🟡 = Present but free-text/minimal | ❌ = Absent

| Feature | Nygard | MADR | smadr | Tyree-Ak | Y-Stmt | Alexan. | BizCase | Plangu. | EdgeX | Merson | NHS-W | G.Morg | DRF | **ours** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Metadata** | | | | | | | | | | | | | | |
| Unique ID | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | 🟡 | ❌ | 🟡 | ✅ | ✅ |
| Title | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ | ✅ | 🟡 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Structured Decision Summary | ❌ | 🟡 | 🟡 | ❌ | ✅ | 🟡 | 🟡 | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Status | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Date(s) | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Author(s) | ❌ | 🟡 | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Decision Owner | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Tags / Category | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Priority | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | 🟡 | ✅ |
| Schema Version | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| JSON Schema Validation | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 | ✅ |
| **Context & Problem** | | | | | | | | | | | | | | |
| Problem Statement | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ | 🟡 | 🟡 | ✅ | ✅ | ✅ | ✅ | 🟡 | ✅ |
| Summary / Elevator Pitch | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Business Drivers | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Technical Drivers | ❌ | 🟡 | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Decision Drivers | ❌ | ✅ | ✅ | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | 🟡 | ❌ |
| Constraints | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 | ❌ | ❌ | ✅ | ✅ |
| Assumptions | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | 🟡 | ❌ | ❌ | ✅ | ✅ |
| **Requirements** | | | | | | | | | | | | | | |
| Functional Requirements | ❌ | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 | ❌ | ✅ |
| Non-Functional Requirements | ❌ | ❌ | ❌ | 🟡 | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 | ❌ | ✅ |
| **Alternatives Analysis** | | | | | | | | | | | | | | |
| Multiple Options | ❌ | ✅ | ✅ | ✅ | 🟡 | ❌ | ✅ | ❌ | 🟡 | ❌ | ✅ | ✅ | ✅ | ✅ |
| Pros per Option | ❌ | ✅ | ✅ | 🟡 | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ | ✅ |
| Cons per Option | ❌ | ✅ | ✅ | 🟡 | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | ✅ | 🟡 | ❌ | ✅ |
| Cost Estimate / Option | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Risk Rating / Option | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| SWOT per Option | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Fact/Opinion Separation | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Visual Comparison Matrix | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Decision** | | | | | | | | | | | | | | |
| Chosen Option | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Explicit Rationale Section | ❌ | 🟡 | 🟡 | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Tradeoffs | 🟡 | 🟡 | 🟡 | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Rationale for Rejected | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Decision Date | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Consequences** | | | | | | | | | | | | | | |
| Positive Consequences | 🟡 | ✅ | ✅ | 🟡 | 🟡 | 🟡 | ❌ | ❌ | ❌ | 🟡 | ✅ | 🟡 | ❌ | ✅ |
| Negative Consequences | 🟡 | ✅ | ✅ | 🟡 | ✅ | 🟡 | ❌ | ❌ | ❌ | 🟡 | ✅ | 🟡 | ❌ | ✅ |
| Confirmation / Validation | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| **Governance & Traceability** | | | | | | | | | | | | | | |
| Stakeholders | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | 🟡 | ❌ | ❌ | 🟡 |
| Formal Approvals | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Audit Trail | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Change Log (with PR links) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Use Case Traceability | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Governance Enforcement | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 | ✅ | ❌ | ❌ |
| Impact Assessment (structured) | ❌ | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Context Validation (policy) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Risk & Compliance** | | | | | | | | | | | | | | |
| Risk Assessment (overall) | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Residual Risk | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Compliance Audit Table | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Constraint Sourcing | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Cross-References** | | | | | | | | | | | | | | |
| Related Decisions | ❌ | 🟡 | ✅ | ✅ | ❌ | 🟡 | ❌ | ❌ | ✅ | ❌ | 🟡 | ❌ | 🟡 | ✅ |
| Related Principles | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Org Context Graph (CRF) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Dependencies (int/ext) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Lifecycle** | | | | | | | | | | | | | | |
| Review Cadence | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 | ❌ | ❌ | ✅ |
| Supersession Chain | 🟡 | 🟡 | 🟡 | ❌ | ❌ | ❌ | ❌ | ❌ | 🟡 | 🟡 | ✅ | ❌ | ❌ | ✅ |
| Archival Policy | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Bidirectional Updates | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

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
| **Planguage** | Owner/Author distinction. Priority as a structured field. QA-oriented keyword system from requirements engineering. | Niche — Gilb consulting/academic |
| **EdgeX Foundry** | Change Log with PR links (built-in audit trail). Mandatory use case traceability. Structured impact assessment (API, DTO, model, config, devops). | Significant — Linux Foundation IoT |
| **Merson** | Explicit standalone `Rationale` section. Rationale for rejected alternatives. "Why > How" philosophy (Richards & Ford). | Moderate — SEI/academic/katas |
| **NHS Wales** | Fact/opinion separation (Options vs. Analysis). Extended confirmation with ownership+enforcement. `Under Review` and `Deprecated` statuses. Healthcare governance context. Summary/elevator pitch. | Growing — UK public sector |
| **Gareth Morgan** | Dedicated `Governance` section (monitoring + compliance enforcement). Traffic-light visual comparison matrices. Strategic Value scoring per option. Architecture characteristics framing. | Moderate — solution architecture |
| **DRF** | Reasoning-first philosophy. Organizational context as knowledge graph (CRF). Context validation with conflict detection. Bidirectional updates (decisions → org facts). Constraint sourcing. | Pre-release (v0.1.0) |
| **adr-governance** | Confirmation with verification artifact IDs. Formal approval workflow with signature IDs. Append-only audit trail. Lifecycle management (review cadence, supersession, archival). Machine-readable YAML with JSON Schema validation. Per-alternative risk rating + rejection rationale. | New — this repo only |

---

## 6. Analysis: Where Standard Templates Fall Short

### 6.1 No Template Has Structured Implications

Every template treats consequences as prose or bullet points. No template in the field (including ours) provides:
- **Structured security implications** with data classification, encryption specifics, access control details, and audit retention periods
- **Structured compliance implications** with regulatory-to-impact mapping and required controls
- **Structured operational implications** with monitoring requirements, runbook references, and staffing needs

These were considered for our schema but ultimately removed to keep ADRs focused on decisions rather than operational runbooks. They remain a potential future enhancement for regulated-environment profiles.

### 6.2 No Template Has Deployment/Rollback Planning

No template includes:
- Phased rollout criteria
- Testing matrices (unit, integration, performance, compliance)
- Rollback criteria and procedures

These are typically in separate runbooks. Some organizations may wish to embed them in ADRs for self-containment, but no template (including ours) currently does this.

### 6.3 No Template Has Monitoring or SLA

No template links a decision to its runtime monitoring:
- Named metrics with warning/critical thresholds
- Alert routing
- SLA targets (availability, RPO, RTO)

These were considered for our schema but removed as they belong in operational runbooks rather than decision records.

### 6.4 No Template Has Decision Governance Enforcement — Except Morgan

Gareth Morgan is the only template that asks: *"How will compliance with this decision be ensured?"* This is distinct from MADR's `Confirmation` (which asks "how do we verify implementation?") — Morgan asks about **ongoing enforcement**, not just initial validation.

Our schema partially addresses this through `audit_trail` and `lifecycle.review_cycle_months`, but does not include a dedicated `governance_enforcement` field. ADRs capture decisions — enforcement is the responsibility of downstream tooling and processes. Architecture should not point to code; code should point to architecture. Teams enforce decisions through their own mechanisms: CODEOWNERS, PR templates with ADR compliance checklists, ArchUnit fitness functions, CI policies, etc. Our `confirmation` section captures *how implementation is verified*; ongoing enforcement is an operational concern, not a decision record concern.

### 6.5 No Template Has Structured Impact Assessment — Except EdgeX

EdgeX Foundry uniquely asks authors to enumerate: services/modules impacted, model/DTO changes, API impact, configuration changes, and devops impact. This is a lightweight **change impact analysis** that no other template captures.

Our schema does not include a dedicated `impact_assessment` section. EdgeX's context (change proposals for a specific, well-defined codebase with known services and DTOs) differs from ours (architectural pattern decisions where impacted systems depend on the adopting organization). Impact information is already captured across `dependencies.internal` (what systems are involved), `consequences.negative` (operational costs), and `decision.tradeoffs` (what teams must adapt). A dedicated section would create overlap and author confusion about field boundaries. Teams needing EdgeX-style structured impact can use `x-impact-assessment` via extension fields.

### 6.6 No Template Captures Rationale for Rejected Alternatives — Except Merson and DRF

Merson's template explicitly includes reasoning for significant alternatives that were *not* chosen in its `Rationale` section. DRF similarly stores alternatives with their rejection reasoning in `synthesis`. Our schema addresses this with the `alternatives[].rejection_rationale` field, which provides an explicit per-option explanation of why a rejected alternative was not chosen — complementing the pros/cons analysis.

---

## 7. Synthesis: Our Schema's Comparative Position

> **📄 Detailed field-level rationale:** For a comprehensive justification of every field in our schema — including precedent tables, rejected alternatives, and academic sources — see **[Schema Field-Level Design Rationale](schema-field-rationale.md)**.

This section provides a **high-level summary** of our schema's position. The field-level document provides the per-field evidence.

### 7.1 Where Our Schema Leads

Our `adr-governance` schema is the most comprehensive ADR meta-model in the survey. Seven sections are **unique** — no other template provides them: `confirmation` (with artifact IDs), `approvals` (with signature IDs), `audit_trail`, `lifecycle` (review cadence + archival), `schema_version`, `architecturally_significant_requirements` (with F/NF IDs), and `dependencies`. See [schema-field-rationale.md §8–§12](schema-field-rationale.md#section-8-confirmation--verification) for the full rationale behind each.

### 7.2 Features Inspired by Other Templates

Key features adopted from other templates (with full rationale in the field-level document):

| Feature | Inspired by | Rationale doc section |
|---------|-------------|----------------------|
| `adr.y_statement` | Y-Statements / Zimmermann (SATURN 2012) | [§1.3](schema-field-rationale.md#13-adry_statement) |
| `adr.decision_level` | DPR / Zimmermann + Hohpe + management science | [§1.11](schema-field-rationale.md#111-adrdecision_level) |
| `extension_fields` (x-*) | smadr | [§13.1](schema-field-rationale.md#131-x--extension-fields) |
| `alternatives[].rejection_rationale` | Merson / DRF | [§5.5](schema-field-rationale.md#55-alternativesrejection_rationale) |
| `decision.confidence` | Azure Well-Architected Framework | [§6.5](schema-field-rationale.md#65-decisionconfidence) |

Additionally, several insights were incorporated into **process documentation** rather than the schema: the Architectural Significance Test (Zimmermann §10.6 → `adr-process.md` §3.0), retrospective questions (Cervantes & Woods §10.8), and PoC/experiment artifact type prefixes for `confirmation.artifact_ids` (§10.7/§10.6).

### 7.3 Features Evaluated and Excluded

Features deliberately excluded, with rationale: `related_principles` (Tyree-Akerman), `governance_enforcement` (Morgan), `impact_assessment` (EdgeX), 3D `risk_per_option` (smadr), `neutral_consequences` (MADR), unified `decision_drivers` (MADR/smadr), `swot_per_option` (Henderson), `context_validation` (DRF), standalone `risk_assessment`, and Decision Guardian integration. Exclusion rationale is documented inline alongside related adopted fields — see §6.1 (no structured implications), §6.4 (no governance enforcement), and §6.5 (no structured impact assessment) in the [template comparison](adr-template-comparison.md#6-analysis-where-standard-templates-fall-short), as well as per-field rejected alternatives in [schema-field-rationale.md](schema-field-rationale.md).

---

## 8. Template Positioning Map

```
                    ┌───────────────────────────────────────────────────────┐
                    │                 COMPREHENSIVENESS                     │
   Minimal ◄────────┼──────────────────────────────────────────────────────►│ Maximal
                    │                                                       │
                    │  Y-Stmt    Nygard    Alexandrian    MADR    NHS Wales │
                    │   (1)    Merson(5)    (4)          (10)      (11)     │
                    │                                                       │
                    │           Planguage    EdgeX   smadr   Tyree-Akerman  │
                    │            (14)        (9)    (15)       (14)         │
                    │                                                       │
                    │                 G.Morgan    Business Case    DRF      │
                    │                  (6+)         (12)          (10)      │
                    │                                                       │
                    │                              adr-governance           │
                    │                                  (20+)                │
                    └───────────────────────────────────────────────────────┘

   Human-readable ◄────────────────────────────────────────────────────────► Machine-readable
                    │                                                       │
                    │  Nygard  Alexandrian  MADR  NHS Wales  EdgeX          │
                    │  Y-Stmt  Merson  Tyree-Ak  G.Morgan                   │
                    │  Planguage            Biz Case                        │
                    │                                                       │
                    │                          smadr    DRF                 │
                    │                                                       │
                    │                          adr-governance               │
                    │                          (YAML + JSON Schema)         │
                    └───────────────────────────────────────────────────────┘
```

---

## 9. Conclusion

Having surveyed **14 templates** (13 external + our own), `adr-governance` sits at the **maximum comprehensiveness** end of the ADR template spectrum (see §7.1 and the [Schema Field-Level Design Rationale](schema-field-rationale.md) for per-field justification).

The tradeoff is **weight**: a full `adr-governance` ADR is significantly heavier than a Nygard or MADR record. This is acceptable for enterprise use cases (e.g., IAM decisions in regulated financial services) but would be overkill for a startup documenting database choices.

The closest philosophical neighbor is **DRF** (reasoning-first, machine-readable, validation-oriented), but it takes a fundamentally different architectural approach (two complementary specs vs. one unified schema) and is still in early draft (v0.1.0). Its organizational context graph (CRF) is a promising concept worth monitoring as it matures.

---

## 10. ADR Ecosystem Insights

The Henderson repository and related sources contain several important concepts beyond templates that are relevant to ADR governance:

### 10.1 Fitness Functions for Decisions as Code

**Fitness functions** are objective automated checks that verify decisions are being maintained. They make decisions testable and assurable.

- **Connection:** A decision record documents the decision; a fitness function *assures* the decision.
- **Example:** Decision = "We use event sourcing for audit requirements." Fitness function = CI test that all state changes produce events.
- **Tools:** [ArchUnit](https://www.archunit.org/) (Java), [ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS) (TypeScript/JavaScript).
- **AI-assisted:** Henderson suggests using LLMs as fitness function evaluators, asking them to audit code/schemas against the decision log.
- **Relevance:** Our `confirmation` field can reference fitness functions as verification artifacts. Our CI pipeline already validates ADR YAML — this is itself a fitness function.

### 10.2 Decision Guardian — PR-Level Enforcement

[Decision Guardian](https://github.com/DecispherHQ/decision-guardian) automatically surfaces relevant ADRs on pull requests when a developer modifies code covered by those decisions. Works with any CI system and as a pre-commit hook.

- **Relevance:** Addresses Gareth Morgan's "governance enforcement" question — decisions are surfaced *at the moment they're most likely to be violated*.
- **Action:** Evaluate for integration with our GitHub Actions CI pipeline.

### 10.3 Teamwork Advice (Henderson)

Key practical insights from teams using ADRs at scale:

1. **Name the directory `decisions/` not `adrs/`** — teams document more (vendor decisions, planning decisions, scheduling decisions) when the directory name uses plain language.
2. **Mutability works better than immutability in practice** — insert new info with date stamps rather than creating a new ADR for every update. "Living document" approach.
3. **Lead with "why" not "what"** — ADRs are not valuable if they're just after-the-fact paperwork.
4. **After-action reviews** — review each ADR one month later to compare the documented expectations with actual practice.

### 10.4 Related Formalisms

The Henderson repo references several pre-ADR decision documentation formalisms that influenced the field:

| Formalism | Full Name | Relevance |
|-----------|-----------|----------|
| **IBIS** | Issue-Based Information System | Question → Position → Argument structure. Influenced dialogue mapping. |
| **QOC** | Questions, Options, Criteria | Similar to ADR alternatives analysis. Academic predecessor. |
| **DRL** | Decision Representation Language | Formal decision trees. More rigorous than ADR prose. |
| **REMAP** | Representation and Maintenance of Process Knowledge | Process-oriented decision capture. |
| **DRF** | Decision Reasoning Format | Modern YAML/JSON successor. See Section 3.13. |

### 10.5 Company-Specific ADR Guidance

- **[AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html):** Formal ADR process with lifecycle (Proposed → Review → Accepted/Rejected → Superseded). Recommends that ADRs are consulted during code and architectural reviews. Treats ADRs as immutable after acceptance.
- **[Microsoft Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record):** Positions ADRs as "one of the most important deliverables of a solution architect." Key advice: record **confidence level** per decision (low-confidence decisions get prioritized for reconsideration). Emphasizes **append-only** log and storing ADRs openly in the workload's documentation repository.
- **[RedHat](https://www.redhat.com/architect/architecture-decision-records):** Advocates ADRs for enterprise architects.
- **[GitHub ADR org](https://adr.github.io/):** Maintains MADR and the broader ADR standards ecosystem. Hosts the canonical template index and tooling list.

### 10.6 Architectural Decisions — The Making Of (Zimmermann)

[Olaf Zimmermann's comprehensive post](https://ozimmer.ch/practices/2020/04/27/ArchitectureDecisionMaking.html) provides a history of architecture decision recording since the late 1990s. Key insights:

1. **Y-Statements evolved from enterprise overengineering.** Zimmermann's earlier meta-models (IBM ARC-100, SOAD PhD project) were too heavy to maintain. The Y-statement was born from a sponsor saying: *"Can you fit each decision on one presentation slide?"*
2. **Good vs. bad justifications.** Good: "We performed a PoC and the results were convincing." Bad: "Everybody does it" or "Experience with this will look great on my resume."
3. **Don't overdo it.** "An AD log with more than 100 entries will probably put your readers (and you) to sleep." Focus on architecturally significant requirements only.
4. **Definition of Done for ADs.** Zimmermann proposes a [DoD for Architectural Decisions](https://ozimmer.ch/practices/2020/05/22/ADDefinitionOfDone.html) and an [Architectural Significance Test](https://ozimmer.ch/practices/2020/09/24/ASRTestECSADecisions.html).
- **Relevance:** Our process documentation includes an architectural significance test (adapted from Zimmermann) as a filter to prevent ADR inflation.

### 10.7 Skeptical Architecture (Cervantes & Woods)

[A Skeptic's Guide to Software Architecture Decisions](https://www.infoq.com/articles/architecture-skeptics-guide/) introduces **architectural skepticism** as a superpower:

1. **Every QAR is a hypothesis.** Quality Attribute Requirements (scalability, performance) are hypotheses about value, not facts. They must be tested empirically.
2. **Selective implementation for assumption testing.** Teams don't need to build the entire solution — build enough to run experiments that validate or refute assumptions.
3. **Skepticism breaks analysis paralysis.** If you accept that no decision can be proven right without experimentation, you short-circuit paralysis by identifying alternatives and testing them empirically.
4. **"When it comes to decisions about the solution, the only useful data comes from executing code; everything else is conjecture."**
- **Relevance:** Our process documentation recommends experiment results, PoC outcomes, and performance benchmarks as `confirmation.artifact_ids` types, with standardized prefixes (e.g., `POC-`, `BENCH-`).

### 10.8 Architectural Retrospectives (Cervantes & Woods)

[Architectural Retrospectives](https://www.infoq.com/articles/architectural-retrospectives/) are distinct from Architecture Reviews:

1. **Reviews improve the architecture; retrospectives improve the decision-making process.**
2. **Key retrospective questions:**
   - How were QARs established? Were they guesses or validated?
   - Was the whole team involved or did senior individuals dominate?
   - Have we ever reversed a decision based on new information?
   - Is technical debt growing, and is that acceptable?
3. **Should be separate from reviews** — team members won't discuss process problems with outsiders present.
4. **Frequency:** Every sprint/iteration. If there are no interesting answers, it's quick.
- **Relevance:** Our schema includes a `reviewed` event type in `audit_trail` for recording periodic review outcomes. `lifecycle.review_cycle_months` triggers the reviews; the process documentation includes adapted retrospective questions to guide them.

### 10.9 Microsoft Azure — Confidence Level

Azure's Well-Architected Framework uniquely recommends recording the **confidence level** of each decision:

> *"Sometimes an architecturally significant decision is made with relatively low confidence. Documenting that low confidence status could prove useful for future reconsideration decisions."*

- **Relevance:** Our schema includes a `decision.confidence` field (`low`, `medium`, `high`) inspired by this recommendation. Low-confidence decisions signal the need for shorter review cycles.

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
11. Gilb, T. (~2012). "Specifying Effective Non-functional Requirements." [ICCGI 2012 Tutorial](https://www.iaria.org/conferences2012/filesICCGI12/Tutorial%20Specifying%20Effective%20Non-func.pdf)
12. EdgeX Foundry. "ADR Template." [edgexfoundry.org](https://docs.edgexfoundry.org/2.3/design/adr/template/)
13. Merson, P. (2023). "ADR Template." [github.com/pmerson](https://github.com/pmerson/ADR-template)
14. Morgan, G. (2024). "Solution Architecture Decisions." [linkedin.com](https://www.linkedin.com/pulse/solution-architecture-decisions-gareth-morgan-0r5xe/)
15. GIG Cymru / NHS Wales. "ADR Template." [github.com/joelparkerhenderson](https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-gig-cymru-nhs-wales)
16. Reasoning Formats (2024). "Decision Reasoning Format (DRF) & Context Reasoning Format (CRF)." [github.com/reasoning-formats](https://github.com/reasoning-formats/reasoning-formats)
17. Richards, M. & Ford, N. (2020). "Fundamentals of Software Architecture." O'Reilly Media.
18. Bass, L., Clements, P. & Kazman, R. (2012). "Documenting Software Architectures: Views and Beyond." Addison-Wesley.
19. AWS Prescriptive Guidance. "ADR Process." [docs.aws.amazon.com](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
20. Decipher HQ. "Decision Guardian." [github.com/DecispherHQ](https://github.com/DecispherHQ/decision-guardian)
21. Zimmermann, O. (2020). "Architectural Decisions — The Making Of." [ozimmer.ch](https://ozimmer.ch/practices/2020/04/27/ArchitectureDecisionMaking.html)
22. Zimmermann, O. (2020). "Definition of Done for Architectural Decisions." [ozimmer.ch](https://ozimmer.ch/practices/2020/05/22/ADDefinitionOfDone.html)
23. Zimmermann, O. (2020). "Architectural Significance Test." [ozimmer.ch](https://ozimmer.ch/practices/2020/09/24/ASRTestECSADecisions.html)
24. Cervantes, H. & Woods, E. "A Skeptic's Guide to Software Architecture Decisions." [infoq.com](https://www.infoq.com/articles/architecture-skeptics-guide/)
25. Cervantes, H. & Woods, E. "Architectural Retrospectives: the Key to Getting Better at Architecting." [infoq.com](https://www.infoq.com/articles/architectural-retrospectives/)
26. Microsoft Azure (2024). "Maintain an architecture decision record (ADR)." [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
27. GitHub ADR Organization. "Architectural Decision Records." [adr.github.io](https://adr.github.io/)
28. Keeling, M. (2022). "Love Unrequited: The Story of Architecture, Agile, and How ADRs Brought Them Together." IEEE Software Vol. 39 Issue 4. [ieeexplore.ieee.org](https://ieeexplore.ieee.org/document/9801811)
29. Keeling, M. & Runde, J. "Architecture Decision Records in Action." [YouTube](https://www.youtube.com/watch?v=41NVge3_cYo)
30. Richards, M. "Software Architecture Monday — ADRs and Architecture Stories." [developertoarchitect.com](https://www.developertoarchitect.com/lessons/lesson168.html)
31. OST Cloud Application Lab. "Architectural Knowledge Management (AKM)." [ost.ch](https://www.ost.ch/en/research-and-consulting-services/computer-science/ifs-institute-for-software-new/cloud-application-lab/architectural-knowledge-management-akm)
