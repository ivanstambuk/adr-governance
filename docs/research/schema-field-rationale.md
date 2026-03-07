# ADR Schema Field-Level Design Rationale

> **Date:** 2026-03-07  
> **Author:** Ivan Stambuk  
> **Status:** Living document — updated as new fields are adopted or removed  
> **Repository:** `adr-governance`  
> **Related documents:**  
> - [`adr-template-comparison.md`](adr-template-comparison.md) — template-level survey (horizontal scan)  
> - [`process-rationale.md`](process-rationale.md) — process-level design rationale  
> - [`schemas/adr.schema.json`](../../schemas/adr.schema.json) — source of truth

---

## Purpose

The [ADR Template Comparison](adr-template-comparison.md) answers: *"What do other templates look like?"*  
The [Process Rationale](process-rationale.md) answers: *"For every process element, why does it exist?"*

**This document answers: *"For every field in our schema, why does it exist?"***

It provides the design rationale for each field in the `adr-governance` schema — justifying its inclusion against the landscape of 13+ surveyed ADR templates, academic literature, and industry standards. It also records what was explicitly considered and rejected for each schema section.

---

## Reading Guide

Each field entry follows this structure:

| Element | Description |
|---|---|
| **Schema path** | JSON Schema location (e.g., `adr.decision_level`) |
| **Type / constraints** | Data type, enum values, validation rules |
| **Required?** | Whether the field is mandatory in the schema |
| **Precedent** | Which other templates/standards have something equivalent |
| **Gap analysis** | Which templates lack this (and why it matters) |
| **Rationale** | Why we include this field in our schema |
| **Rejected alternatives** | Design options considered and dismissed |
| **Sources** | Academic references, standards, or industry practices |

---

## Section 1: `adr` — Core Metadata

The `adr` object contains identification and classification metadata. Its design philosophy is: **every ADR should be findable, filterable, and self-describing without reading its body.**

### 1.1 `adr.id`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.id` |
| **Type** | `string`, pattern: `^ADR-[0-9]{4}(-[a-z0-9]+)+$` |
| **Required?** | ✅ Yes |

**Precedent:**

| Template | ID format | Structured? |
|---|---|---|
| Nygard | Filename-based, no schema field | ❌ |
| MADR 4.0 | Filename-based (NNNN-title.md) | ❌ |
| smadr | No dedicated field | ❌ |
| Planguage | `Tag:` keyword | 🟡 |
| EdgeX | NNNN-title in filename | ❌ |
| Merson | No formal ID | 🟡 |
| DRF | `id` field | ✅ |
| **adr-governance** | `adr.id` with enforced pattern | ✅ |

**Rationale:** Most templates derive identity from filenames, which breaks when ADRs are stored in databases, bundled into documents, or transmitted via API. A schema-level ID with an enforced pattern (`ADR-NNNN-slug`) enables:
- **Cross-reference integrity** — `lifecycle.superseded_by` and `lifecycle.supersedes` reference IDs, not filenames
- **Slug readability** — the mandatory slug portion ensures IDs are self-describing (e.g., `ADR-0001-dpop-over-mtls` vs. bare `ADR-0001`)
- **CI validation** — validators can check ID uniqueness and cross-reference consistency programmatically

**Rejected alternatives:**
- *Filename-only identity (Nygard/MADR style)* — breaks in non-filesystem contexts
- *UUID-based IDs* — not human-readable; defeats the purpose of architectural documentation
- *Free-text IDs without pattern* — prevents programmatic validation and sorting

### 1.2 `adr.title`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.title` |
| **Type** | `string`, minLength: 10, maxLength: 200 |
| **Required?** | ✅ Yes |

**Precedent:** Present in every template surveyed (13/13). The most universal ADR field.

**Rationale:** Self-evident. The `minLength: 10` constraint prevents placeholder titles; `maxLength: 200` prevents prose paragraphs masquerading as titles. These bounds were chosen empirically from our example ADRs (shortest: 36 chars, longest: 67 chars).

### 1.3 `adr.y_statement` ⭐ *DPR-adopted (P2)*

| Attribute | Value |
|---|---|
| **Schema path** | `adr.y_statement` |
| **Type** | `string` (free-text, long-form Y-Statement) |
| **Required?** | Schema-optional; **validator-enforced** as mandatory when `status: accepted` |

**Precedent:**

| Template | Summary capability | Self-contained? |
|---|---|---|
| Y-Statements (Zimmermann, SATURN 2012) | Canonical 6-part structured sentence | ✅ Yes |
| MADR 4.0 — Decision Outcome | "Chosen option: X, because Y" | ❌ Requires context from other sections |
| Nygard — Decision section | Free-text paragraph | ❌ Requires Context section |
| Tyree-Akerman — Decision | 1–2 sentences + justification | ❌ Requires other sections |
| NHS Wales — Summary | Elevator pitch | 🟡 Summary, not structured decision |
| Architecture Haiku (Fairbanks, WICSA 2011) | 1-page terse design description | ✅ Yes (but 1 page, not 1 sentence) |
| **adr-governance** | Long-form Y-Statement (7 clauses) | ✅ Yes |

**Rationale:** The Y-Statement is the **most information-dense standalone decision summary format available**. No other format packs context, decision, rejected alternatives, benefits, tradeoffs, and rationale into a single sentence. This makes it ideal for:
- ADR indexes and dashboards
- Chat/email sharing (the full decision in one paragraph)
- AI-generated summaries from structured data
- Rendered Markdown output

**Why a static field, not dynamic generation?** The constituent schema fields (`context.description`, `consequences.positive`, etc.) are multi-paragraph Markdown with Mermaid diagrams. Assembling a Y-Statement from these is a *summarization* task requiring authorial judgment, not a mechanical concatenation. Since accepted ADRs are immutable, there is no drift/maintenance burden.

**Why long form only (with "because" clause)?** The short form omits the rationale — the most important part of any decision record. The "because" clause maps to `decision.rationale`, which is the core "why."

**What it replaced:** The earlier `adr.summary` field (a free-text elevator pitch) was removed because the Y-Statement is a strictly more informative summary. No established template uses both.

**Key academic lineage:**
- Zimmermann, "Making Architectural Knowledge Sustainable" (SATURN 2012)
- Fairbanks, Architecture Haiku (WICSA 2011) — the "to achieve / accepting that" tradeoff structure
- See [Y-Statement process rationale](process-rationale.md#1-y-statement-rendering-capability--adry_statement) for full literature review

### 1.4 `adr.status`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.status` |
| **Type** | `enum`: `draft`, `proposed`, `accepted`, `superseded`, `deprecated`, `rejected`, `deferred` |
| **Required?** | ✅ Yes |

**Precedent:**

| Template | Status values |
|---|---|
| Nygard | proposed, accepted, deprecated, superseded |
| MADR 4.0 | proposed, accepted, deprecated, superseded (+ any custom) |
| smadr | proposed, accepted, deprecated, superseded |
| EdgeX | proposed, accepted, deprecated, superseded |
| NHS Wales | proposed, accepted, deprecated, superseded, **under review** |
| **adr-governance** | draft, proposed, accepted, superseded, deprecated, rejected, **deferred** |

**Rationale:** Our status set extends the Nygard baseline with three additions and one subtraction:
- **`draft`** — added because ADRs under active authoring should not appear as `proposed` before they're ready for review. Prevents premature review cycles.
- **`rejected`** — added because decisions that were formally evaluated and refused are valuable historical records. Without this status, rejected proposals are either deleted (losing knowledge) or left in `proposed` limbo.
- **`deferred`** — added because not every decision can be made now. Context may be insufficient, dependencies unresolved, or timing wrong. `deferred` explicitly communicates "we know about this but can't decide yet" — preventing repeated re-analysis.
- **`under review` (NHS Wales)** — excluded because it's a transient process state, not a durable decision state. Our `audit_trail` captures review events without polluting the status machine.

**The `archived` non-status:** `archived` is deliberately **not** a status value. Archival is an administrative overlay tracked via `lifecycle.archival` — archived ADRs retain their terminal status (`superseded`, `deprecated`, `rejected`) while becoming invisible in active listings.

### 1.5 `adr.created_at` / `adr.last_modified`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.created_at`, `adr.last_modified` |
| **Type** | `string`, format: `date-time` (ISO 8601) |
| **Required?** | `created_at`: ✅ Yes; `last_modified`: Optional |

**Precedent:** Present in MADR (as `date`), smadr, EdgeX, Planguage, DRF. Absent in Nygard (which relies on Git history).

**Rationale:** Explicit timestamps survive non-Git contexts (wikis, databases, bundled documents). `created_at` is required because every ADR has a creation moment; `last_modified` is optional because Git itself tracks modifications and the audit trail provides event-level timestamps.

### 1.6 `adr.version` / `adr.schema_version`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.version` (MAJOR.MINOR), `adr.schema_version` (MAJOR.MINOR.PATCH) |
| **Type** | `string` with semver-like patterns |
| **Required?** | `version`: ✅ Yes; `schema_version`: Optional |

**Precedent:** Only smadr and DRF have a schema version field. No other template has a document version.

**Rationale:** `version` tracks the ADR document's own evolution (useful for review communications: "I reviewed v1.2, but you've since published v1.3"). `schema_version` pins each ADR to a specific schema release, enabling forward/backward compatibility as the schema evolves.

### 1.7 `adr.project` / `adr.component`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.project` (required), `adr.component` (optional) |
| **Type** | `string` |
| **Required?** | `project`: ✅ Yes; `component`: Optional |

**Precedent:** Partially in EdgeX (which requires affected services). No other template has explicit project scoping.

**Rationale:** `project` scopes the ADR to a programme or product — essential when a single ADR repository serves multiple projects (enterprise pattern). `component` narrows further to a specific module/subsystem. Together they enable filtering: "show me all ADRs for Project X, Component Y."

### 1.8 `adr.tags`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.tags` |
| **Type** | `array` of unique strings |
| **Required?** | Optional |

**Precedent:** Present in smadr (as `tags` in frontmatter), Tyree-Akerman (via "Categories"). Absent in most templates.

**Rationale:** Tags enable freeform discovery and filtering beyond the fixed `decision_type`/`decision_level` taxonomy. Organizational jargon, technology names, and project-specific labels all belong here.

### 1.9 `adr.priority`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.priority` |
| **Type** | `enum`: `low`, `medium`, `high`, `critical` |
| **Required?** | Optional |

**Precedent:** Only Planguage has a structured priority field. DRF has a `priority` in context objectives.

**Rationale:** Priority signals review urgency and implementation ordering. A `critical` decision demands immediate attention; a `low` decision can wait for a convenient sprint. The four-level enum aligns with standard risk/priority scales used in ITSM and project management.

### 1.10 `adr.decision_type`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.decision_type` |
| **Type** | `enum`: `technology`, `process`, `organizational`, `vendor`, `security`, `compliance` |
| **Required?** | ✅ Yes |

**Precedent:** Tyree-Akerman uses a "Category" field. smadr uses tags. MADR has no domain classification.

**Rationale:** Domain classification enables stakeholder routing — security decisions go to the CISO, compliance decisions go to the DPO, vendor decisions go to procurement. The six values cover the domains that emerge in enterprise architecture practice.

**Rejected alternatives:**
- *TOGAF four domains (Business/Data/Application/Technology)* — too enterprise-architecture-specific and not action-oriented
- *Unlimited free-text category* — prevents programmatic filtering and dashboard aggregation
- *DDD-aligned categories (Domain/Infrastructure/Integration)* — too narrow for organizations not practicing DDD

### 1.11 `adr.decision_level` ⭐ *DPR-adopted (P1)*

| Attribute | Value |
|---|---|
| **Schema path** | `adr.decision_level` |
| **Type** | `enum`: `strategic`, `tactical`, `operational` |
| **Required?** | Optional |

**Precedent:**

| Framework | Equivalent concept | Levels |
|---|---|---|
| DPR (Zimmermann 2020) | Strategic / Tactic / Stepwise | 3 |
| SOA Decisions (Zimmermann 2007) | Conceptual / Technology / Asset | 3 |
| Hohpe's Architect Elevator (2020) | Penthouse / Middle / Engine Room | 3 |
| C4 Model (Brown ~2006) | System / Container / Component / (Code) | 4 → 3 effective |
| Kruchten's Ontology (2004) | Existence / Property / Executive | 3 (but orthogonal — type, not altitude) |
| TOGAF ADM | Business / Data / Application / Technology | 4 (domain-parallel, not altitude) |
| Ford & Richards (2021) | Architectural Quantum (variable scope) | Continuous |
| Management Science | Strategic / Tactical / Operational | 3 |

**Rationale:** Our schema has `decision_type` (domain: *what* kind of decision) but lacked an **altitude** dimension (scope: *at what level* the decision operates). The same domain spans multiple altitudes:
- **Security + Strategic:** "Adopt zero-trust network architecture"
- **Security + Tactical:** "Use claim-based authorization in domain services"
- **Security + Operational:** "Use Ed25519 for JWT signing keys"

Without `decision_level`, these three are indistinguishable when filtered by `decision_type: security`, but they have vastly different blast radii, stakeholder audiences, and reversal costs.

**Why three levels?** Every prescriptive framework that classifies by scope uses exactly three. Four-level models either have a redundant bottom level (C4's "Code" is optional) or classify by domain (TOGAF). Standards bodies (ISO 42010, arc42) deliberately don't prescribe — confirming this is a design choice. Three maps to the universal Strategic/Tactical/Operational triad from management science.

**Why these three terms?** `strategic`/`tactical`/`operational` are immediately understood across disciplines. Rejected: `conceptual`/`technology`/`asset` (Zimmermann SOA — too abstract), `penthouse`/`middle`/`engine-room` (Hohpe — metaphorical, not self-documenting).

**Key academic lineage:** Zimmermann DPR (2020), SOA Decision Models (2007), Kruchten Ontology (2004), TOGAF ADM, C4 Model (Brown), Hohpe Architect Elevator (2020), Ford & Richards (2021), Jansen & Bosch (2005). Full 8-framework comparative analysis preserved in Git history.

---

## Section 2: People & Governance

### 2.1 `authors`

| Attribute | Value |
|---|---|
| **Schema path** | `authors` (top-level) |
| **Type** | `array` of `$ref: person` (name + role + optional email), minItems: 1 |
| **Required?** | ✅ Yes |

**Precedent:** MADR (as `decision-makers` in frontmatter), smadr (structured `author`), EdgeX (as "Submitters"), Planguage (as "Owner"/"Author"). Absent in Nygard, Tyree-Akerman, Merson.

**Rationale:** Every decision has an author who can be consulted for context. The structured `person` type (name + role) enables organizational context — knowing the author is a "Security Architect" vs. "Junior Developer" informs how to weight the decision.

### 2.2 `decision_owner`

| Attribute | Value |
|---|---|
| **Schema path** | `decision_owner` (top-level) |
| **Type** | `$ref: person` |
| **Required?** | ✅ Yes |

**Precedent:** Only Planguage (as "Owner" vs. "Author") explicitly separates ownership from authorship. MADR conflates them in `decision-makers`.

**Rationale:** The author writes the ADR; the **decision owner** is accountable for the outcome. These are often different people — a senior architect may delegate authoring to a team member while retaining accountability. Enterprise governance requires knowing who holds the decision, not just who typed it.

### 2.3 `reviewers`

| Attribute | Value |
|---|---|
| **Schema path** | `reviewers` (top-level) |
| **Type** | `array` of `$ref: person` |
| **Required?** | Optional |

**Precedent:** MADR (as `consulted` + `informed` in RACI-style frontmatter), NHS Wales (informal reference). No other template separates reviewers from approvers.

**Rationale:** Records who reviewed the ADR without necessarily approving it. Important for auditability — "who looked at this?" is a different question from "who approved it?"

### 2.4 `approvals`

| Attribute | Value |
|---|---|
| **Schema path** | `approvals` (top-level) |
| **Type** | `array` of objects: name, role, identity, approved_at, signature_id |
| **Required?** | Conditionally — required when `status` is `proposed` or `accepted` |

**Precedent:** **No other ADR template has formal approvals as a structured section.** This is unique to adr-governance.

**Rationale:** Enterprise and regulated environments require formal sign-off trails. The `identity` field enables CI pipelines to verify that every listed approver actually approved the pull request — bridging the gap between the ADR document and the Git platform's approval mechanism. The `signature_id` field supports external signature references (e.g., DocuSign IDs, Jira ticket numbers) for fully auditable trails.

**Why conditional requirement?** Drafts don't need approvers; propositions and acceptances do. The JSON Schema `allOf/if/then` block enforces this — `proposed` and `accepted` ADRs *must* have at least one approval with an `identity` field.

---

## Section 3: `context` — Problem Space

### 3.1 `context.description`

| Attribute | Value |
|---|---|
| **Schema path** | `context.description` |
| **Type** | `string`, minLength: 20 (Markdown-native) |
| **Required?** | ✅ Yes |

**Precedent:** Present in every template (13/13) as "Context", "Problem Statement", or "Context and Problem Statement." The most universal ADR section alongside "Title."

**Rationale:** Self-evident — every architectural decision exists in a context. The Markdown-native type (supporting embedded Mermaid diagrams, code blocks, and rich formatting) enables architectural prose that goes beyond plain text. The `minLength: 20` constraint prevents stub contexts.

**Naming:** Originally `context.summary`; renamed to `context.description` to avoid confusion with the Y-Statement (which is the true decision "summary") and to use a more semantically accurate term for a problem narrative.

### 3.2 `context.business_drivers` / `context.technical_drivers`

| Attribute | Value |
|---|---|
| **Schema path** | `context.business_drivers`, `context.technical_drivers` |
| **Type** | `array` of strings |
| **Required?** | Optional |

**Precedent:**

| Template | Equivalent | Split? |
|---|---|---|
| MADR 4.0 | "Decision Drivers" (unified list) | ❌ Single list |
| smadr | "Decision Drivers" (unified list) | ❌ Single list |
| NHS Wales | "Decision Drivers" (unified list) | ❌ Single list |
| **adr-governance** | `business_drivers` + `technical_drivers` | ✅ Split |

**Rationale:** MADR's unified "Decision Drivers" conflates business motivations ("regulatory deadline," "customer churn") with technical forces ("existing tech debt," "latency requirements"). Splitting them serves two purposes:
1. **Stakeholder routing** — business stakeholders read business drivers; engineers read technical drivers
2. **Y-Statement composition** — the "facing [concern]" clause in the Y-Statement draws from both, but the split makes it clear which concern dominates

**Rejected alternative:** *Unified `decision_drivers` list (MADR style)* — simpler but loses the business/technical distinction that matters for enterprise governance.

### 3.3 `context.constraints`

| Attribute | Value |
|---|---|
| **Schema path** | `context.constraints` |
| **Type** | `array` of strings |
| **Required?** | Optional |

**Precedent:** Tyree-Akerman (dedicated "Constraints" section), Merson (informally in rationale), DRF (with "sourcing" — linking constraints to organizational facts). Absent in Nygard, MADR.

**Rationale:** Constraints bound the solution space and are non-negotiable — "we must use vendor X" or "deployment must be on-premises." Capturing them explicitly prevents evaluating alternatives that were never viable, and prevents future reviewers from asking "why didn't you consider Y?" when Y was constrained out.

### 3.4 `context.assumptions`

| Attribute | Value |
|---|---|
| **Schema path** | `context.assumptions` |
| **Type** | `array` of strings |
| **Required?** | Optional |

**Precedent:** Tyree-Akerman (dedicated "Assumptions" section), Planguage (as "Assumptions"), DRF (explicit field). Absent in Nygard, MADR.

**Rationale:** Assumptions are the most dangerous hidden dependencies in any decision. "We assume the API gateway handles TLS termination" — if that assumption is wrong, the entire decision may be invalid. Explicit assumptions enable review ("is this assumption still true?") and serve as triggers for re-evaluation during lifecycle reviews.

---

## Section 4: `architecturally_significant_requirements` — Requirement Traceability

### 4.1 ASR Structure: `functional[]` / `non_functional[]`

| Attribute | Value |
|---|---|
| **Schema path** | `architecturally_significant_requirements.functional[]`, `.non_functional[]` |
| **Type** | `array` of objects: `id` (F-NNN / NF-NNN), `description` |
| **Required?** | Optional (entire section) |

**Precedent:**

| Template | Requirement support | Structured? |
|---|---|---|
| Tyree-Akerman | "Related Requirements" section | 🟡 Free-text references |
| Gareth Morgan | Architecture characteristics per option | 🟡 Informal |
| Planguage | Quality requirements with Scale/Meter | ✅ Highly structured |
| **adr-governance** | F/NF split with IDs per ADR | ✅ Structured |

**Rationale:** **No other ADR template has embedded ASRs with IDs.** Yet the connection between decisions and requirements is the most important traceability vector — *why* was this decision made? The ASR section answers that directly.

The F/NF split mirrors the universal ISO 25010 distinction between functional suitability and quality attributes. The `id` pattern (`F-NNN`/`NF-NNN`) is **scoped per ADR** (each ADR starts from F-001/NF-001) — this avoids requiring a global requirement registry, which most teams don't have.

**Rejected alternatives:**
- *Global requirement IDs (referencing an external backlog)* — creates an external dependency that most teams can't satisfy. ADRs should be self-contained.
- *Unstructured prose (Nygard/MADR style)* — prevents machine extraction and traceability analysis
- *Full QAS template per requirement (SEI style)* — overengineering for an ADR. P3 proposes adding a `measure` field as a lightweight compromise.

---

## Section 5: `alternatives` — Option Analysis

### 5.1 Alternatives Array Structure

| Attribute | Value |
|---|---|
| **Schema path** | `alternatives[]` |
| **Type** | `array` of objects, minItems: 2 |
| **Required?** | ✅ Yes, with at least 2 options |

**Precedent:**

| Template | Alternatives required? | Min count? | Pros/Cons? |
|---|---|---|---|
| Nygard | ❌ No alternatives section | — | ❌ |
| MADR | ✅ "Considered Options" | No minimum | ✅ Per option |
| smadr | ✅ With risk assessment | No minimum | ✅ Per option |
| Tyree-Akerman | ✅ "Alternatives" | No minimum | 🟡 Free-text |
| Business Case | ✅ "Candidates" with SWOT | No minimum | ✅ SWOT per option |
| **adr-governance** | ✅ With min: 2 | ✅ 2 minimum | ✅ Per option |

**Rationale:** The `minItems: 2` constraint is the most controversial design decision in the schema. It enforces the principle that **every architectural decision is a choice between alternatives** — if there was only one option, no architectural decision was made. This prevents "decision" records that are actually implementation notifications.

### 5.2 `alternatives[].description` (Markdown-native)

| Attribute | Value |
|---|---|
| **Schema path** | `alternatives[].description` |
| **Type** | `string`, minLength: 20 (Markdown-native) |
| **Required?** | ✅ Yes |

**Rationale:** Descriptions require **thorough** architectural explanation — not a one-liner, but multiple paragraphs with data flows, integration points, and ideally Mermaid diagrams. The `minLength: 20` prevents stubs. This field is explicitly documented as requiring the same depth as the ADR's context, ensuring rejected alternatives are described well enough for future teams to understand *what* was rejected and *could revisit it*.

### 5.3 `alternatives[].pros` / `alternatives[].cons`

| Attribute | Value |
|---|---|
| **Schema path** | `alternatives[].pros`, `alternatives[].cons` |
| **Type** | `array` of strings (minItems: 1 each, minLength: 1 per item) |
| **Required?** | ✅ Yes |

**Precedent:** MADR ("Good, because…" / "Bad, because…"), smadr (structured), NHS Wales. Absent in Nygard, Merson.

**Rationale:** Structured pros/cons force balanced evaluation. The `minItems: 1` constraints ensure that no option is presented as exclusively positive or negative — every real-world alternative has both.

**Rejected alternative:** *MADR's three-way split (Good/Neutral/Bad)* — "Neutral" consequences are rarely informative and create authoring friction ("what goes in Neutral?"). The binary split is sufficient.

### 5.4 `alternatives[].estimated_cost` / `alternatives[].risk`

| Attribute | Value |
|---|---|
| **Schema path** | `alternatives[].estimated_cost` (low/medium/high), `alternatives[].risk` (low/medium/high/critical) |
| **Required?** | Optional |

**Precedent:** No other ADR template has per-option cost estimates. smadr has a 3D risk model (Technical/Schedule/Ecosystem). Business Case (Henderson) has SWOT with cost.

**Rationale:** Relative cost and risk enums provide machine-filterable decision metadata without requiring detailed financial analysis. An alternative with `estimated_cost: high` and `risk: critical` creates a very different decision context than `cost: low`, `risk: low`.

**Rejected alternative:** *smadr's 3D risk model (Technical/Schedule/Ecosystem)* — interesting but our per-option `risk` field combined with pros/cons provides equivalent coverage with less schema complexity.

### 5.5 `alternatives[].rejection_rationale`

| Attribute | Value |
|---|---|
| **Schema path** | `alternatives[].rejection_rationale` |
| **Type** | `string` (Markdown-native) |
| **Required?** | Optional |

**Precedent:** Merson (explicit rationale for rejected alternatives in Rationale section), DRF (rejection reasoning in `synthesis`). No other template has per-option rejection reasoning.

**Rationale:** Pros/cons explain what's good and bad about each option. `rejection_rationale` explains **why this specific option was not chosen** — a more focused explanation that addresses the decision context rather than the option's abstract qualities. Future teams benefit most from knowing not just "what were the options" but "why didn't you pick this one?"

---

## Section 6: `decision` — The Choice

### 6.1 `decision.chosen_alternative`

| Attribute | Value |
|---|---|
| **Schema path** | `decision.chosen_alternative` |
| **Type** | `string` (should match a name in `alternatives[]`, enforced by tooling) |
| **Required?** | ✅ Yes |

**Precedent:** Present in all templates that have alternatives analysis (MADR, smadr, Tyree-Akerman, Business Case). Absent in Nygard (which embeds the choice in prose).

**Rationale:** The chosen alternative must be explicitly and unambiguously stated. The name-matching requirement (enforced by tooling, not schema — due to JSON Schema limitations) creates traceability between the alternatives analysis and the decision.

### 6.2 `decision.rationale`

| Attribute | Value |
|---|---|
| **Schema path** | `decision.rationale` |
| **Type** | `string`, minLength: 20 (Markdown-native) |
| **Required?** | ✅ Yes |

**Precedent:** Merson has a dedicated "Rationale" section (unique at the time). Most templates embed rationale in the Decision section. Tyree-Akerman has "Justification." Richards and Ford explicitly advocate for rationale as the most important part of an ADR.

**Rationale:** The rationale is the **most important field in the entire schema**. It answers "why" — the question that future architects will ask most often. Markdown-native formatting supports the depth this field deserves.

### 6.3 `decision.tradeoffs`

| Attribute | Value |
|---|---|
| **Schema path** | `decision.tradeoffs` |
| **Type** | `string` (Markdown-native) |
| **Required?** | Optional |

**Precedent:** Y-Statements ("accepting that…"), MADR (informal in consequences). No template has a dedicated tradeoffs field.

**Rationale:** Every architectural decision involves tradeoffs — "we gained X but lost Y." Separating tradeoffs from rationale prevents the rationale from becoming defensive ("we chose X despite Y") and creates a clear space for acknowledging costs. This field maps directly to the "accepting that" clause in the Y-Statement.

### 6.4 `decision.decision_date`

| Attribute | Value |
|---|---|
| **Schema path** | `decision.decision_date` |
| **Type** | `string`, format: `date` |
| **Required?** | ✅ Yes |

**Rationale:** Distinct from `adr.created_at` — an ADR may be drafted on January 1 but the decision made on January 15. The decision date is the authoritative timestamp for "when was this decided?" which matters for compliance and lifecycle reviews.

### 6.5 `decision.confidence`

| Attribute | Value |
|---|---|
| **Schema path** | `decision.confidence` |
| **Type** | `enum`: `low`, `medium`, `high` |
| **Required?** | Optional |

**Precedent:** Azure Well-Architected Framework recommends confidence levels. No ADR template has this as a structured field.

**Rationale:** `confidence: low` signals that the decision was made under time pressure or with incomplete information, and should have a shorter review cycle. `confidence: high` signals strong empirical evidence (PoC, benchmarks) and can tolerate a longer review interval. This field directly influences the `lifecycle.review_cycle_months` — low-confidence decisions should be reviewed sooner.

---

## Section 7: `consequences` — Impact Assessment

### 7.1 `consequences.positive` / `consequences.negative`

| Attribute | Value |
|---|---|
| **Schema path** | `consequences.positive`, `consequences.negative` |
| **Type** | `array` of strings |
| **Required?** | At least one field required (via `minProperties: 1`) |

**Precedent:** MADR (Good/Neutral/Bad), smadr, NHS Wales, Nygard (flat prose). All templates have consequences; structuring varies.

**Rationale:** The positive/negative split enables structured reasoning about outcomes. The `minProperties: 1` constraint ensures that consequences are not completely empty — at least one category must be populated.

**Rejected alternatives:**
- *Three-way split with "Neutral" (MADR style)* — excluded; neutral consequences are rarely informative
- *Categorized consequences (security/compliance/operational)* — evaluated and removed to keep ADRs focused on decisions rather than operational runbooks. See [template comparison §6.1](adr-template-comparison.md#61-no-template-has-structured-implications)

---

## Section 8: `confirmation` — Verification

### 8.1 `confirmation.description` / `confirmation.artifact_ids`

| Attribute | Value |
|---|---|
| **Schema path** | `confirmation.description` (required), `confirmation.artifact_ids` (optional) |
| **Type** | `string` + `array` of strings |
| **Required?** | ✅ Yes (section); `artifact_ids` optional |

**Precedent:**

| Template | Verification section? | Artifact references? |
|---|---|---|
| MADR 4.0 | ✅ "Confirmation" (free text) | ❌ |
| NHS Wales | ✅ "Confirmation" with ownership | ❌ |
| Gareth Morgan | 🟡 "Governance" (compliance enforcement) | ❌ |
| **adr-governance** | ✅ Description + artifact IDs | ✅ |

**Rationale:** MADR introduced the crucial question: "How will we verify this decision was implemented correctly?" Our schema extends this with `artifact_ids` — concrete references (Jira tickets, PR URLs, ArchUnit test IDs, benchmark reports) that serve as **evidence** the decision was followed. This bridges the gap between "we decided" and "we did."

---

## Section 9: `dependencies` — Impact Scope

### 9.1 `dependencies.internal` / `dependencies.external`

| Attribute | Value |
|---|---|
| **Schema path** | `dependencies.internal`, `dependencies.external` |
| **Type** | `array` of strings |
| **Required?** | Optional |

**Precedent:** **No other ADR template has explicit dependency tracking.** EdgeX has "Affected Services" (similar to internal dependencies but limited to a specific product).

**Rationale:** Architectural decisions don't exist in isolation. Knowing that "this decision depends on the payment team's API migration" (internal) or "this decision requires AWS availability zones in eu-west-1" (external) enables impact analysis when dependencies change.

**Rejected alternative:** *EdgeX-style structured impact assessment* — too specific to a single codebase. Our ADRs describe architectural patterns where impacted systems vary by adopter.

---

## Section 10: `references` — Evidence & Standards

### 10.1 `references[]`

| Attribute | Value |
|---|---|
| **Schema path** | `references[]` |
| **Type** | `array` of objects: `title` + `url` |
| **Required?** | Optional |

**Precedent:** Present informally in most templates ("More Information" in MADR, "Related Artifacts" in Tyree-Akerman, "Notes" in Nygard).

**Rationale:** Structured references (title + URL) enable link validation and bibliography generation. RFCs, standards documents, vendor documentation, and research papers referenced in the decision rationale should be formally captured.

---

## Section 11: `lifecycle` — Decision Management

### 11.1 `lifecycle.review_cycle_months` / `lifecycle.next_review_date`

| Attribute | Value |
|---|---|
| **Schema path** | `lifecycle.review_cycle_months`, `lifecycle.next_review_date` |
| **Type** | `integer` (min: 1), `string` (date) |
| **Required?** | Optional |

**Precedent:** Only NHS Wales has informal review scheduling. **No other template has structured review cadence.**

**Rationale:** Architectural decisions decay — context changes, technologies evolve, teams turn over. Without explicit review triggers, decisions become fossilized. The `review_cycle_months` field enables automated reminders; `next_review_date` captures the concrete date for the next review.

### 11.2 `lifecycle.superseded_by` / `lifecycle.supersedes`

| Attribute | Value |
|---|---|
| **Schema path** | `lifecycle.superseded_by`, `lifecycle.supersedes` |
| **Type** | `string` or `null`, ADR ID pattern |
| **Required?** | Optional |

**Precedent:** Nygard (inline "Superseded by ADR-NNNN"), MADR (inline), smadr, EdgeX, NHS Wales. All handle supersession; structuring varies.

**Rationale:** Bidirectional cross-references (new ADR points to old via `supersedes`; old ADR points to new via `superseded_by`) create a navigable decision chain. Both fields are validated for symmetry by the validator script.

### 11.3 `lifecycle.archival`

| Attribute | Value |
|---|---|
| **Schema path** | `lifecycle.archival.archived_at`, `lifecycle.archival.archive_reason` |
| **Type** | `string` or `null` |
| **Required?** | Optional |

**Precedent:** **No other template has archival as a structured concept.** Most templates treat superseded/deprecated as terminal.

**Rationale:** Long-lived ADR repositories accumulate hundreds of decisions. Archival removes decisions from active consideration without deleting them — preserving the historical record while reducing noise. The `archived_at` timestamp and `archive_reason` provide queryable metadata.

---

## Section 12: `audit_trail` — Event Log

### 12.1 `audit_trail[]`

| Attribute | Value |
|---|---|
| **Schema path** | `audit_trail[]` |
| **Type** | `array` of objects: `event` (enum), `by`, `at`, `details` |
| **Required?** | Optional |

**Precedent:** smadr has a compliance audit table. EdgeX has a change log with PR links. **No other template has an append-only lifecycle event log.**

**Rationale:** The audit trail records *every* lifecycle event — creation, updates, reviews, approvals, rejections, supersessions, deprecations, and archival. Each event captures *who*, *when*, and *what happened*. This satisfies auditability requirements for regulated environments and provides a complete decision history.

The `reviewed` event type (inspired by Cervantes & Woods' architectural retrospectives and Henderson's after-action reviews) closes the lifecycle loop — `review_cycle_months` triggers reviews; the `reviewed` event records that one occurred.

---

## Section 13: Extension Fields & Schema Mechanics

### 13.1 `x-*` Extension Fields

| Attribute | Value |
|---|---|
| **Schema path** | Top-level `patternProperties: "^x-"` |
| **Required?** | Optional |

**Precedent:** smadr (pioneered `x-` prefix convention for ADRs, inspired by OpenAPI). HTTP headers use `X-` prefix convention.

**Rationale:** Organizations have unique metadata needs (project codes, CMDB references, deployment regions, cost center IDs). Extension fields allow any `x-`-prefixed field without breaking schema validation — enabling customization without forking the schema.

### 13.2 `additionalProperties: false`

Every object in the schema sets `additionalProperties: false`. This is a deliberate strictness choice — typos and undocumented fields are caught at validation time rather than silently accepted. Extension fields use the `x-` escape hatch.

### 13.3 Conditional Requirements (`allOf/if/then`)

The schema uses JSON Schema 2020-12 conditional logic to enforce:
- When `status` is `proposed` or `accepted`, `approvals` is required with at least one entry, and each approval must have an `identity` field.

This enables a **progressive strictness** model — drafts are loose, proposed/accepted ADRs are strict.

---

## Appendix A: Features Evaluated and Excluded

The following features were researched, evaluated, and deliberately excluded from the schema. Rationale for each exclusion is documented in the [template comparison §7.3](adr-template-comparison.md#73-features-evaluated-and-excluded).

| Feature | Found in | Why excluded |
|---|---|---|
| `related_principles` | Tyree-Akerman | Assumes external principles registry. Use `references` or `x-related-principles`. |
| `governance_enforcement` | Gareth Morgan | Enforcement is downstream (CODEOWNERS, fitness functions, CI). ADRs capture decisions, not enforcement mechanisms. |
| `impact_assessment` (structured) | EdgeX | Already covered across `dependencies`, `consequences`, `decision.tradeoffs`. EdgeX targets a specific codebase; our ADRs are pattern-level. |
| `risk_per_option` (3D) | smadr | Our per-option `risk` + pros/cons provides equivalent coverage, less complexity. |
| `neutral_consequences` | MADR | Rarely informative. Binary positive/negative is sufficient. |
| Unified `decision_drivers` | MADR/smadr | Our business/technical split is more informative. |
| `swot_per_option` | Business Case (Henderson) | Overlaps with pros/cons/cost/risk. SWOT is a management lens, not an engineering lens. |
| `context_validation` (CRF) | DRF | Requires knowledge graph infrastructure. Worth revisiting when DRF matures past v0.1.0. |
| Standalone `risk_assessment` | — (no template has this) | Risk is already distributed across `alternatives[].risk`, `alternatives[].cons`, `consequences.negative`, `decision.tradeoffs`, and `context.constraints`. A formal risk register belongs in threat models / ISMS artifacts. |
| `related_adrs` / `attachments` | — (original schema) | Removed during schema refinement. ADR relationships use `lifecycle.superseded_by` / `lifecycle.supersedes`. Attachments are external references. |
| `adr.summary` | NHS Wales (elevator pitch) | Replaced by `adr.y_statement` — a strictly more informative summary format. |

---

## Appendix B: Key Academic and Industry Sources

| Source | Year | Contribution to schema design |
|---|---|---|
| Nygard, "Documenting Architecture Decisions" | 2011 | Established the ADR format; validated minimal structure |
| Zimmermann, Y-Statements (SATURN 2012) | 2012 | `adr.y_statement` — standalone decision summary |
| Fairbanks, Architecture Haiku (WICSA 2011) | 2011 | Tradeoff structure ("to achieve / accepting that") |
| Zimmermann, DPR (OST/HSR) | 2020–2024 | `decision_level` (via Strategic/Tactic/Stepwise); QAS/SMART NFR inspiration |
| Zimmermann, SOA Decision Models | 2007–2012 | Three-level abstraction (Conceptual/Technology/Asset) |
| Kruchten, "Ontology of Architectural Design Decisions" | 2004 | Confirmed type ≠ level (orthogonal dimensions) |
| Jansen & Bosch, "Architecture as Decision Composition" | 2005 | Decisions as first-class navigable entities |
| Hohpe, "The Software Architect Elevator" | 2020 | Validated three-level altitude with "rate of change" heuristic |
| Ford & Richards, "Software Architecture: The Hard Parts" | 2021 | Architectural quantum; "Why > How" philosophy |
| Bass, Clements, Kazman, *Software Architecture in Practice* | 2021 (4th ed.) | QAS framework; attribute-driven design |
| Brown, C4 Model | ~2006 | Visualization levels validate 3-level decision scoping |
| Wirfs-Brock, "Agile Landing Zones" | 2011 | Three-tier quality targets (minimal/target/outstanding) |
| ISO/IEC 25010:2023 | 2023 | 9 quality characteristics; measurability framework |
| Gilb, Planguage | 2006 | Scale/Meter/Must/Plan/Wish — most rigorous quality specification |
| MADR 4.0 (adr.github.io) | 2024 | Confirmation section; RACI-style stakeholder model |
| smadr (smadr.dev) | 2025 | Extension fields (x-*); JSON Schema validation; 3D risk model |
| Merson, ADR Template (CMU/SEI) | 2023 | Dedicated rationale section; rejection rationale |
| DRF (reasoning-formats) | 2024 | Context validation; organizational knowledge graph (future reference) |
