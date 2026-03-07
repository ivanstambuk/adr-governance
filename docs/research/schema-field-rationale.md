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

### 1.3 `adr.y_statement`

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

### 1.11 `adr.decision_level`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.decision_level` |
| **Type** | `enum`: `strategic`, `tactical`, `operational` |
| **Required?** | Optional |

**Rationale:** Our schema has `decision_type` (domain: *what* kind of decision) but lacked an **altitude** dimension (scope: *at what level* the decision operates). The same domain spans multiple altitudes:
- **Security + Strategic:** "Adopt zero-trust network architecture"
- **Security + Tactical:** "Use claim-based authorization in domain services"
- **Security + Operational:** "Use Ed25519 for JWT signing keys"

Without `decision_level`, these three are indistinguishable when filtered by `decision_type: security`, but they have vastly different blast radii, stakeholder audiences, and reversal costs.

#### Literature Review: 8-Framework Comparative Analysis

##### 1. DPR — Strategic / Tactic / Stepwise (Zimmermann, 2020–2024)

DPR organizes design activities along three conceptual levels, derived from Domain-Driven Design and API design methodology:

| DPR Level | Focus | Artifacts |
|---|---|---|
| **Strategic DDD** | System landscape, bounded contexts, team boundaries, context maps | Context maps, bounded context diagrams |
| **Tactic DDD** | Domain model internals — aggregates, entities, value objects, domain events | Domain models, CRC cards |
| **Stepwise Service Design** | API endpoint design, protocol choices, SLA, deployment tech | CEL/REL tables, API descriptions, SLAs |

> **Clarification:** "Stepwise" is the name of a 7-step API design *methodology*, not a decision scope. The implicit hierarchy maps to: **Strategic → Tactical → Operational**.

##### 2. Zimmermann's SOA Decision Model — Conceptual / Technology / Asset (2007–2012)

**Primary source:** [soadecisions.org](https://soadecisions.org); "An architectural decision modeling framework for service oriented architecture design" (University of Stuttgart, 2011)

| Level | MDA Mapping | Focus | Example |
|---|---|---|---|
| **Conceptual** | High-level PIM | Strategic patterns, platform-independent design | "Use orchestration for multi-step business processes" |
| **Technology** | Hybrid PIM/PSM | Technology standards, protocol choices | "Use GraphQL for client queries" |
| **Asset** | Low-level PSM | Vendor/product selection, library choices | "Use Spring Boot 3.x" |

> **Key insight:** This three-level model separates *rapidly changing* platform-specific concerns (asset level) from *enduring* conceptual decisions. It is the direct academic ancestor of DPR's Strategic/Tactic/Stepwise distinction.

**Assessment:** Very close to our `strategic`/`tactical`/`operational` but uses SOA-specific terminology ("asset" implies product selection, narrower than "operational").

##### 3. Kruchten's Ontology — Existence / Property / Executive (2004)

**Primary source:** "An Ontology of Architectural Design Decisions in Software-Intensive Systems," 2nd Groningen Workshop on Software Variability Management, 2004

| Type | Focus | Examples |
|---|---|---|
| **Existence** | What structural/behavioral elements exist (or must NOT exist: "ban" decisions) | "The system has 3 layers"; "Communication uses RMI" |
| **Property** | Quality traits, design rules, constraints | "All data at rest must be encrypted"; "Response time < 200ms" |
| **Executive** | Business-environment-driven: process, personnel, organization, technology mandates | "All API changes require CCB approval" |

> **Key insight:** Kruchten's taxonomy is **orthogonal** to scope/altitude. A "strategic" decision could be existence (creating a new bounded context), property (defining enterprise-wide SLA targets), or executive (mandating cloud-first). This confirms that `decision_type` and `decision_level` are **independent dimensions**.

**Assessment:** Not suitable as a replacement for scope-based classification, but validates that type and level are two independent dimensions.

##### 4. TOGAF ADM — Business / Data / Application / Technology (The Open Group)

| Domain | Focus |
|---|---|
| **Business Architecture** | Business strategy, governance, organizational structure |
| **Data Architecture** | Data structures, relationships, governance |
| **Application Architecture** | Application systems, interactions, business process relationships |
| **Technology Architecture** | Infrastructure — hardware, software, networks, platforms |

TOGAF's ADM phases iterate across these domains with increasing specificity (Phase A: architecture vision → Phases B–D: domain-specific → Phases E–F: solution-level → Phase G: governance).

> **Key insight:** TOGAF's four domains are **domain-parallel** (Business ↔ Data ↔ Application ↔ Technology), not a vertical altitude dimension. Our `decision_type` + `component` fields already cover this domain dimension.

**Assessment:** Too enterprise-architecture-specific. Confirms the validity of the strategic → operational gradient but doesn't provide the right classification axis.

##### 5. C4 Model — System / Container / Component / Code (Brown, ~2006)

| Level | Scope | Audience |
|---|---|---|
| **System Context** (Level 1) | How the system relates to users and external systems | Non-technical stakeholders |
| **Container** (Level 2) | Major runtime deployment units (services, databases) | Developers, architects |
| **Component** (Level 3) | Internal structure within a container | Developers |
| **Code** (Level 4) | Class/function detail | Developers (often optional) |

> **Key insight:** C4's levels are for *visualization*, not decision classification. When mapped to decisions: System Context = strategic, Container = tactical, Component/Code = operational. Level 4 is "often optional" — confirming that 3 effective levels suffice.

**Assessment:** Confirms the visualization community independently arrived at a similar 3–4 level hierarchy. For decisions, Component and Code collapse into "operational."

##### 6. Hohpe's Architect Elevator (2020)

**Primary source:** "The Software Architect Elevator" (O'Reilly, 2020)

| Floor | Focus |
|---|---|
| **Penthouse** (Executive) | Business strategy, organizational design, "why are we building this?" |
| **Middle floors** (Architecture) | Cross-cutting technical decisions, trade-off analysis, "-ilities" |
| **Engine Room** (Implementation) | Specific technologies, frameworks, infrastructure details |

> **Key insight:** Hohpe explicitly argues architects must *ride the elevator* — understanding decisions at all levels. He emphasizes **"rate of change"** as a distinguishing factor: penthouse decisions change slowly (years), engine room decisions change fast (sprints). This directly aligns with our "reversal cost" dimension.

**Assessment:** Strongly validates the three-level approach. Maps perfectly to `strategic`/`tactical`/`operational`.

##### 7. Ford & Richards — Architectural Quantum (2021)

**Primary source:** "Software Architecture: The Hard Parts" (O'Reilly, 2021)

Ford and Richards introduce the **architectural quantum** — the scope for a set of architecture characteristics. They emphasize: decision scope varies from system-wide to component-specific, trade-off analysis is the core of architectural work, and **fitness functions** provide measurable governance at each level.

> **Key insight:** The architectural quantum validates that decisions have a natural *blast radius* and that this radius is a critical metadata dimension. Their approach doesn't prescribe fixed levels but supports the idea that decisions cluster into natural altitude bands.

##### 8. Jansen & Bosch — Architecture as Decision Composition (2005)

**Primary source:** "Software Architecture as a Set of Architectural Design Decisions" (University of Groningen, 2005)

Jansen and Bosch proposed that architecture should be viewed not as components-and-connectors but as the **cumulative outcome of design decisions** over time. They introduced decisions as first-class entities with relationships (constrains, follows-from, conflicts-with) and grouping by shared topics and abstraction levels.

This perspective reinforces that a `decision_level` field helps organize the decision log as a navigable knowledge base.

#### Comparative Analysis

| Framework | # Levels | Terms | Classification Type |
|---|:---:|---|---|
| DPR (Zimmermann 2020) | 3 | Strategic / Tactic / Stepwise | Scope/altitude |
| SOA Decisions (Zimmermann 2007) | 3 | Conceptual / Technology / Asset | Abstraction/platform-independence |
| Kruchten Ontology (2004) | 3 | Existence / Property / Executive | Decision **nature** (orthogonal) |
| TOGAF | 4 | Business / Data / Application / Technology | Domain (parallel layers) |
| C4 Model (Brown ~2006) | 4 (3 effective) | System / Container / Component / (Code) | Visualization zoom |
| Hohpe's Elevator (2020) | 3 | Penthouse / Middle / Engine Room | Organizational altitude |
| Ford/Richards (2021) | Continuous | Architectural quantum (variable scope) | Blast radius |
| Jansen/Bosch (2005) | N/A (grouping) | Topics + abstraction levels | Decision relationships |
| Management Science | 3 | Strategic / Tactical / Operational | Standard management theory |

**Finding: Three levels is the consensus.** Every prescriptive framework that classifies by scope/altitude uses exactly three. Four-level models either have a redundant bottom level (C4's "Code") or classify by domain (TOGAF). Kruchten's three categories are orthogonal (type, not altitude). Standards bodies (ISO 42010, arc42) deliberately don't prescribe — confirming this is a design choice.

#### The Two Independent Dimensions

The research confirms that `decision_type` and `decision_level` capture **different, independent dimensions**:

```
                        decision_type (WHAT domain)
                 ┌──────────┬──────────┬──────────┬──────────┐
                 │technology│ security │ process  │  data    │
  ┌──────────────┼──────────┼──────────┼──────────┼──────────┤
  │  strategic   │ Cloud vs │ Zero-    │ Adopt    │ Event    │
  │              │ on-prem  │ trust    │ ADR      │ sourcing │
  │              │ strategy │ model    │ process  │ strategy │
  ├──────────────┼──────────┼──────────┼──────────┼──────────┤
d │  tactical    │ Use BFF  │ Claim-   │ Trunk-   │ CQRS for │
e │              │ pattern  │ based    │ based    │ read     │
c │              │ for SPA  │ authZ    │ develop  │ models   │
i ├──────────────┼──────────┼──────────┼──────────┼──────────┤
s │  operational │ Use      │ Ed25519  │ Use      │ Use      │
i │              │ Spring   │ for JWT  │ GitHub   │ Postgres │
o │              │ Boot 3.x │ signing  │ Actions  │ 16       │
n │              │          │          │          │          │
  │ _level       │          │          │          │          │
  │ (WHAT        │          │          │          │          │
  │  altitude)   │          │          │          │          │
  └──────────────┴──────────┴──────────┴──────────┴──────────┘
```

#### Why Not Four or Five Levels?

| Candidate | Assessment |
|---|---|
| **Split "operational" into "technology" + "implementation"** | Zimmermann himself moved away from this (Conceptual/Technology/Asset → Strategic/Tactic/Stepwise). Both are "operational" in practice. |
| **Add "enterprise" above "strategic"** | Our framework targets a single product/system ADR repository, not enterprise-wide. Enterprise-wide decisions are strategic for our purposes. |
| **Mirror C4 with four levels** | "Component" and "Code" level decisions cannot be meaningfully distinguished for ADR metadata purposes. |
| **Use Kruchten's types as levels** | Orthogonal to scope — would conflate two independent dimensions. |

#### Term Selection

| Term | Chosen Because | Rejected Alternatives |
|---|---|---|
| `strategic` | Universal management term; used by DPR, Hohpe, management science | `enterprise` (too EA-specific), `conceptual` (SOA — too abstract), `penthouse` (Hohpe — not self-documenting) |
| `tactical` | Universal management term; used by DPR, management science | `technology` (SOA — too narrow), `middle` (Hohpe — not descriptive), `application` (TOGAF — conflates domain with altitude) |
| `operational` | Universal management term; used by management science, DPR (implied) | `asset` (SOA — implies vendor selection only), `engine-room` (Hohpe — metaphorical), `implementation` (too code-level) |

#### Discriminating Heuristics

| Heuristic Question | If YES → |
|---|---|
| Does this affect **organizational structure** or team boundaries? | `strategic` |
| Does this constrain or enable **multiple future decisions**? | `strategic` |
| Would reversing this require **re-architecting** major system boundaries? | `strategic` |
| Does this define a **design pattern** used across multiple components? | `tactical` |
| Does this affect a **subsystem or bounded context** but not the whole landscape? | `tactical` |
| Would reversing this require **significant refactoring** but not re-architecture? | `tactical` |
| Is this a **specific product, library, or protocol** choice? | `operational` |
| Could a different team member **swap in an alternative** in one sprint? | `operational` |
| Is this primarily about **how** rather than **what** or **why**? | `operational` |

#### Glossary Reference

| Level | Scope | Typical Stakeholders | Reversal Cost | Rate of Change | DPR Mapping | Hohpe Mapping |
|-------|-------|---------------------|---------------|----------------|-------------|---------------|
| `strategic` | Enterprise/landscape, bounded contexts, team boundaries | C-suite, Enterprise Architects, Product leadership | Very high — shapes roadmap | Years | Strategic DDD | Penthouse |
| `tactical` | Domain model, component patterns, cross-cutting technical patterns | Software Architects, Tech Leads, Senior Engineers | Moderate — confined to subsystem | Quarters/months | Tactic DDD | Middle floors |
| `operational` | Specific tech choices, API protocols, deployment configs | Engineers, DevOps, API designers | Lower — usually swappable | Sprints/weeks | Stepwise Service Design | Engine Room |

#### Classification of Existing ADRs

| ADR | `decision_type` | `decision_level` | Rationale |
|---|---|---|---|
| ADR-0000 Adopt Governed ADR Process | `process` | `strategic` | Enterprise-wide process shaping all future decisions |
| ADR-0001 DPoP over mTLS | `technology` | `operational` | Specific protocol/library choice |
| ADR-0002 Reference Tokens over JWT | `technology` | `tactical` | Token architecture pattern affecting multiple components |
| ADR-0004 Ed25519 over RSA for JWT Signing | `technology` | `operational` | Specific algorithm choice, easily swappable |
| ADR-0005 BFF Token Mediator for SPA | `security` | `tactical` | Architectural pattern (BFF) across frontend/backend |
| ADR-0006 Session Enrichment for Step-Up | `technology` | `tactical` | Cross-cutting session management pattern |
| ADR-0007 Centralized Secret Store | `technology` | `tactical` | Infrastructure pattern affecting all secret consumers |
| ADR-0008 Defer OpenID Federation | `technology` | `strategic` | Enterprise trust establishment with multi-year implications |

#### Sources

| Source | Year | Contribution |
|---|---|---|
| Zimmermann, DPR | 2020–2024 | Strategic/Tactic/Stepwise — primary inspiration |
| Zimmermann, SOA Decision Models | 2007–2012 | Conceptual/Technology/Asset — direct ancestor |
| Kruchten, "Ontology of Architectural Design Decisions" | 2004 | Confirmed type ≠ level (orthogonal dimensions) |
| Jansen & Bosch, "Architecture as Decision Composition" | 2005 | Decisions as first-class entities; grouping by abstraction |
| TOGAF ADM | Ongoing | Domain-parallel layers; validates strategic→operational gradient |
| Brown, C4 Model | ~2006 | 4 visualization levels collapse to 3 for decisions |
| Hohpe, "The Software Architect Elevator" | 2020 | Penthouse/Middle/Engine Room; "rate of change" heuristic |
| Ford & Richards, "Software Architecture: The Hard Parts" | 2021 | Architectural quantum; blast radius as metadata |
| Bass, Clements, Kazman, "Software Architecture in Practice" | 2021 | Attribute-Driven Design iterates across abstraction levels |
| ISO/IEC/IEEE 42010 | 2011 | No prescribed taxonomy — confirms design choice |
| arc42 (Starke) | Ongoing | No prescribed categories — same confirmation |

### 1.12 `scope` / `phase` Metadata ⏭️ *Evaluated — Redundant*

**Proposal:** Add DPR-style YAML frontmatter fields (`Scope`, `Phases`, `Abstraction/Refinement Level`) to ADRs.

**DPR source:** Every DPR method element includes:

```yaml
Scope: Entire system, component, connector, class, ...
Phases: Design (all levels)
Abstraction/Refinement Level: All
```

**Why skipped (redundant with existing fields):**

| DPR Field | Our Equivalent | Assessment |
|---|---|---|
| `Scope` | `adr.decision_level` (§1.11) + `adr.component` (§1.7) | ✅ Covered — decision_level captures altitude, component captures specific scope |
| `Phases` | `adr.status` lifecycle (§1.4) | ✅ Covered — our status lifecycle is more natural for GitOps than waterfall-style phase labels |
| `Abstraction Level` | `adr.decision_level` (§1.11) | ✅ Subsumed — strategic/tactical/operational directly maps abstraction levels |

Adding these would create **three fields duplicating information already in `decision_level` and `component`**.

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

**Rejected alternative:** *RACI matrix (MADR style)* — MADR 4.0 uses `consulted` + `informed` in a RACI model. Our simpler `reviewers` + `approvals` split covers the same ground without RACI overhead.

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

**Rejected alternatives:**
- *Unified `decision_drivers` list (MADR style)* — simpler but loses the business/technical distinction that matters for enterprise governance
- *`related_principles` field (Tyree-Akerman)* — Tyree-Akerman has a dedicated "Related Principles" section. We excluded this because it assumes an external principles registry that most teams don't maintain. Use `references` or `x-related-principles` extension field instead.

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

**Rejected alternative:** *Context Validation / CRF (DRF style)* — DRF proposes a Context Relevance Framework for validating assumptions against organizational knowledge graphs. Requires knowledge graph infrastructure that doesn't exist yet. Worth revisiting when DRF matures past v0.1.0.

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
- *Full QAS template per requirement (SEI style)* — overengineering for an ADR. A lightweight `measure` field was evaluated and rejected (see §4.2 below).

### 4.2 QAS `measure` Field ❌ *Rejected*

**Proposal:** Add an optional `measure` field to `#/$defs/architecturally_significant_requirement` to capture quantitative acceptance criteria separately from the description.

#### Academic and Industry Lineage

##### SEI Quality Attribute Scenarios (Bass, Clements, Kazman)

The **Software Engineering Institute (CMU/SEI)** established the QAS template in the late 1990s, codified in *Software Architecture in Practice* (4th ed., 2021). The SEI model defines six scenario components:

| Component | Description | Example |
|---|---|---|
| **Source** | Entity that generates the stimulus | Authenticated user |
| **Stimulus** | Condition arriving at the system | Submits a payment order |
| **Artifact** | Part of the system stimulated | Payment processing service |
| **Environment** | Conditions under which stimulus occurs | Peak load (1000 concurrent users) |
| **Response** | System activity after stimulus | Process and confirm order |
| **Response Measure** | Measurable determination of success | p95 response < 1 second |

The Response Measure is the critical differentiator between a vague quality goal and a testable requirement. The SEI also introduced **Quality Utility Trees** for prioritizing QAS instances by (Business Value, Technical Risk).

##### arc42 Section 10 — Quality Requirements

arc42 places detailed quality requirements in **Section 10** with a simplified SEI QAS template (Context/Background, Source/Stimulus, Metric/Acceptance Criteria). Notably, arc42 distinguishes **usage scenarios** (runtime: performance, availability) from **change scenarios** (modification effort: maintainability, flexibility) — demonstrating that measurable criteria apply beyond runtime metrics. The **arc42 Quality Model (Q42)** catalogs 100+ quality characteristics across 9 system dimensions.

##### ISO/IEC 25010:2023 (SQuaRE)

ISO 25010:2023 defines 9 product quality characteristics (up from 8 in 2011):
1. Functional Suitability — correctness, completeness, appropriateness
2. Performance Efficiency — time behavior, resource utilization, capacity
3. Compatibility — co-existence, interoperability
4. Interaction Capability (formerly Usability) — inclusivity, self-descriptiveness
5. Reliability — faultlessness, availability, fault tolerance, recoverability
6. Security — confidentiality, integrity, non-repudiation, accountability
7. Maintainability — modularity, reusability, analyzability, modifiability, testability
8. Flexibility (formerly Portability) — adaptability, installability, replaceability
9. Safety (new) — operational constraint, risk identification, fail-safe

**All** can be made measurable — not just runtime performance. Maintainability: "new developer productive within N days." Security: "zero critical vulnerabilities per OWASP scan."

##### Planguage (Tom Gilb)

Gilb's Planguage takes measurability to its extreme: every quality requirement has mandatory **Scale** (unit), **Meter** (measurement method), and **Past/Must/Plan/Wish** values. The most rigorous approach but also the heaviest.

#### How Other ADR Templates Handle Quality Requirements

| Template | Quality requirement support | Measurability? |
|---|---|---|
| **Nygard** | None — implicit in "Context" prose | ❌ No |
| **MADR 4.0** | "Decision Drivers" — bullet list of concerns | ❌ Free text, no measure |
| **smadr** | 3D risk assessment per option | 🟡 Risk levels, not measures |
| **Tyree-Akerman** | "Assumptions" + "Constraints" | ❌ Prose only |
| **Planguage** | Full Scale/Meter/Must/Plan/Wish | ✅ Most rigorous |
| **arc42** | Section 10 quality scenarios with metric | ✅ Scenario + metric |
| **SEI/ATAM** | Full 6-part QAS with Response Measure | ✅ Most structured |
| **adr-governance** | `architecturally_significant_requirements` with `id` + `description` | ❌ No dedicated measure field |

**Finding:** No ADR template has a dedicated `measure` field on quality requirements. The SEI QAS and arc42 templates have measures, but they are *separate artifacts*, not embedded in decision records. **This would have been a novel addition.**

#### Analysis of Our Current Examples

Our example ADRs already embed measurable criteria within the description text:

| ADR | NF-ID | Description (with embedded measure) |
|---|---|---|
| ADR-0001 (DPoP) | NF-001 | "DPoP proof generation on mobile must complete in **< 50ms** (including secure enclave signature)" |
| ADR-0001 (DPoP) | NF-002 | "DPoP proof validation at the resource server must add **< 5ms** latency per request at **p99**" |
| ADR-0002 (Reference Tokens) | NF-001 | "Token introspection latency must be **< 10ms at p99** with **< 0.01% error rate**" |
| ADR-0004 (Ed25519) | NF-001 | "JWT signing must complete in **< 2ms** at p99" |

Authors *naturally write measurable NFRs* by embedding quantities in the description.

#### Rejection Rationale

**Status: ❌ Rejected** for three reasons:

1. **Altitude mismatch.** The `measure` field is primarily useful for **operational** ADRs where NFRs are naturally expressed as numeric thresholds (latency, throughput, error rates). For **strategic** ADRs, quality attributes that matter — organizational agility, time-to-market, architectural flexibility — resist single-threshold quantification. A field relevant to ~30% of ADRs doesn't justify the schema weight.

2. **Measure volatility vs. ADR immutability.** Measurable thresholds are *volatile* — a p95 latency target of "< 200ms" today may become "< 100ms" next quarter as traffic grows. But accepted ADRs have an **immutable decision core**. Pinning a measure in a frozen field creates a stale contract that either gets ignored or forces supersession for a non-architectural change. Measures belong in living documents (SLO definitions, observability dashboards, capacity planning artifacts).

3. **AI-native prose extraction.** Our framework is designed for LLM consumption. Modern LLMs trivially extract quantitative thresholds from prose — the machine-extractability argument that motivated a structured field evaporates in an AI-native context.

#### Credits

| Concept | Source |
|---|---|
| Quality Attribute Scenarios | SEI/CMU — Bass, Clements, Kazman, *Software Architecture in Practice* (4th ed., 2021) |
| SMART NFR Elicitation | DPR — Zimmermann, `activities/DPR-SMART-NFR-Elicitation.md` |
| QAS Template | DPR — `artifact-templates/DPR-QualityAttributeScenario.md` |
| arc42 Quality Requirements | Starke, Hruschka, arc42 Section 10 |
| ISO 25010:2023 | ISO/IEC 25010:2023 — Product quality model (9 characteristics) |
| Planguage | Gilb, "Rich Requirement Specs" (2006) |

### 4.3 NFR Landing Zones ❌ *Rejected*

**Proposal:** Add structured landing zone fields (minimal/target/outstanding) to ASR entries, as an extension to the §4.2 `measure` field.

#### Wirfs-Brock's Landing Zones Concept

Rebecca Wirfs-Brock introduced "agile landing zones" (2011) as a framework for defining and tracking product releasability. Instead of a single pass/fail threshold, define three levels:

| Level | Definition | Example (API latency) |
|-------|-----------|----------------------|
| **Minimal** | Lowest acceptable value — below this, not releasable | p95 < 500ms |
| **Target** | Desired value the team aims for | p95 < 200ms |
| **Outstanding** | Exceptional achievement, beyond expected | p95 < 50ms |

**Why landing zones help:**
1. **Negotiation tool** — stakeholders agree on a range rather than a single number
2. **Progressive refinement** — "make it work at minimal first, then optimize toward target"
3. **Trade-off visibility** — "if we invest 2 more sprints, we move from minimal to target"
4. **Risk calibration** — "we're at minimal for latency but outstanding for availability — is that OK?"

#### Relationship to QAS and SMART Criteria

DPR's QAS template (from SEI's Bass, Clements, Kazman) structures quality requirements as scenarios with six components. The response measure is where landing zones apply — replacing a single threshold with a triplet. DPR also emphasizes SMART criteria for NFRs (**S**pecific, **M**easurable, **A**greed upon, **R**ealistic, **T**ime-bound). Landing zones make the "M" criterion easier because agreeing on a range is easier than agreeing on a point.

#### Rejection Rationale

**Status: ❌ Rejected** for four reasons:

1. **Dependency on §4.2.** P9 was designed as an extension to P3's `measure` field. Without `measure`, adding `landing_zone` is even harder to justify.

2. **Same volatility problem as §4.2.** Landing zone thresholds change as systems scale. An immutable ADR field is the wrong home for living SLO targets.

3. **Prose is sufficient.** Authors can (and already do) embed threshold ranges in the `description` text:
   ```yaml
   non_functional:
     - id: NF-001
       description: >-
         API response time under normal load.
         Landing zone: minimal < 500ms, target < 200ms, outstanding < 100ms (p95).
   ```

4. **Right tool for the job.** Landing zones belong in SLO definitions, observability dashboards, and test suites — not in architectural decision records. The ADR captures *why we chose this architecture*; the SLO captures *how we measure it works*.

The landing zone **concept** is valuable educational content referenced in our verbosity guidance for writing quantitative NFR descriptions.

#### Credits

| Concept | Source |
|---|---|
| Agile Landing Zones | Wirfs-Brock, R. (2011). [*"Agile Landing Zones"*](http://wirfs-brock.com/blog/2011/07/29/agile-landing-zones/) |
| QAS template | SEI — Bass, Clements, Kazman: *Software Architecture in Practice* (3rd ed.) |
| SMART NFR Elicitation | DPR `activities/DPR-SMART-NFR-Elicitation.md` (line 122) |
| SLA template | DPR `artifact-templates/SDPR-ServiceLevelAgreement.md` |

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

**Rejected alternatives:**
- *smadr's 3D risk model (Technical/Schedule/Ecosystem)* — interesting but our per-option `risk` field combined with pros/cons provides equivalent coverage with less schema complexity
- *SWOT per option (Business Case / Henderson)* — overlaps with pros/cons/cost/risk. SWOT is a management lens, not an engineering lens.

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

**Rejected alternative:** *Governance enforcement field (Gareth Morgan)* — Morgan's template has a dedicated "Governance" section for compliance enforcement mechanisms. We excluded this because enforcement is downstream of the ADR — it belongs in CODEOWNERS, fitness functions, and CI pipelines. ADRs capture decisions, not enforcement mechanisms.

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

**Rejected alternatives:**
- *EdgeX-style structured impact assessment* — too specific to a single codebase. Our ADRs describe architectural patterns where impacted systems vary by adopter.
- *Standalone `risk_assessment` section* — no ADR template has this as a standalone section. Risk is already distributed across `alternatives[].risk`, `alternatives[].cons`, `consequences.negative`, `decision.tradeoffs`, and `context.constraints`. A formal risk register belongs in threat models / ISMS artifacts, not in decision records.

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

**Rejected alternative:** *`related_adrs` / `attachments` (original schema)* — removed during schema refinement. ADR relationships are captured through `lifecycle.superseded_by` / `lifecycle.supersedes` for the most important relationship type (replacement). Other cross-references use `references` or prose in `context.description`. Attachments are external references via `confirmation.artifact_ids` or `references`.

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

## Sources

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
