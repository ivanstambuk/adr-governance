# ADR Governance Enrichment Proposals — from DPR (Design Practice Repository)

> **Source:** [socadk/design-practice-repository](https://github.com/socadk/design-practice-repository) (DPR) by Olaf Zimmermann (ZIO), OST/HSR  
> **Local clone:** `.research/design-practice-repository/` (gitignored)  
> **Analysis Date:** 2026-03-07  
> **Status:** Draft — pending refinement before execution

---

## Tracker

| # | Proposal | Type | Value | Effort | Status |
|---|----------|:----:|:-----:|:------:|:------:|
| P1 | [`decision_level` field](#p1-add-decision_level-field) | Schema | **High** | Low | ✅ Done |
| P2 | [Y-Statement rendering](#p2-add-y-statement-rendering-capability) | Capability | Medium | Low | ⬜ Not started |
| P3 | [QAS `measure` field on ASRs](#p3-add-quality-attribute-scenario-qas-measure-field) | Schema | Medium | Low | ⬜ Not started |
| P4 | [AD Definition of Done checklist](#p4-add-definition-of-done-for-architecture-decisions) | Docs | Medium | Low | ⬜ Not started |
| P5 | [Architectural Significance Test guidance](#p5-add-architectural-significance-test-guidance) | Docs | Low–Medium | Very low | ⬜ Not started |
| P6 | [`scope`/`phase` metadata](#p6-add-scope--phase-metadata) | Redundant | Low | Low | ⏭️ Skip |
| P7 | [AD Definition of Ready](#p7-add-definition-of-ready-for-architecture-decisions) | Docs | Medium | Low | ⬜ Not started |
| P8 | [ADR Verbosity Levels guidance](#p8-adr-verbosity-levels-guidance) | Docs | Low–Medium | Very low | ⬜ Not started |
| P9 | [NFR Landing Zones](#p9-nfr-landing-zones-for-quality-requirements) | Schema + Docs | Medium | Low | ⬜ Not started |

> **Legend:** ⬜ Not started · 🔄 In progress · ✅ Done · ⏭️ Skipped

---

## Background

The **Design Practice Repository (DPR)** is an academically grounded, openly licensed (CC-BY-4.0) collection of method elements for agile architecting and service design. The repository is organized as follows:

```
design-practice-repository/
├── activities/              # 8 published, 4 future work stubs
│   ├── DPR-ArchitecturalDecisionCapturing.md    ← core: decision logging
│   ├── DPR-ArchitectureModeling.md              ← 4-step modeling approach
│   ├── DPR-SMART-NFR-Elicitation.md             ← SMART criteria for NFRs
│   ├── DPR-StrategicDDD.md                      ← bounded contexts, context maps
│   ├── DPR-TacticDDD.md                         ← aggregates, entities, value objects
│   ├── SDPR-StepwiseServiceDesign.md            ← 7-step API design method
│   ├── DPR-StorySplitting.md                    ← user story decomposition
│   └── DPR-UserInterfaceMocking.md
├── artifact-templates/      # 16 published, 2 future work
│   ├── DPR-ArchitecturalDecisionRecordYForm.md  ← Y-Statement ADR template
│   ├── DPR-QualityAttributeScenario.md          ← QAS/SMART NFR template
│   ├── DPR-StrategicDDDContextMap.md            ← bounded context diagrams
│   ├── DPR-DomainModel.md                       ← OOA/OOD domain modeling
│   ├── DPR-CRCCard.md                           ← component responsibilities
│   ├── SDPR-CandidateEndpointList.md            ← API endpoint identification
│   ├── SDPR-RefinedEndpointList.md              ← API endpoint refinement
│   ├── SDPR-ServiceLevelAgreement.md            ← SLA/SLO patterns
│   └── SDPR-APIDescription.md                   ← OpenAPI/AsyncAPI contracts
├── roles/                   # 2 roles
│   ├── DPR-ApplicationArchitectRole.md
│   └── SDPR-APIProductOwner.md
├── background-information/  # Bibliography (31 academic references)
├── tutorials/               # Tutorial walkthroughs
└── contributing/            # Templates for adding new method elements
```

### DPR's Three-Level Design Hierarchy

DPR organizes design activities along three conceptual levels:

```
┌─────────────────────────────────────────────┐
│  Strategic DDD                              │
│  System landscape, bounded contexts,        │
│  team boundaries, context maps              │
├─────────────────────────────────────────────┤
│  Tactic DDD                                 │
│  Domain model internals, aggregates,        │
│  entities, value objects, domain events      │
├─────────────────────────────────────────────┤
│  Stepwise Service Design (7 steps)          │
│  API endpoints, protocols, data formats,    │
│  SLA, deployment technology                 │
└─────────────────────────────────────────────┘
```

> **Clarification:** "Stepwise" is the name of a 7-step API design *methodology* (`.research/design-practice-repository/activities/SDPR-StepwiseServiceDesign.md`), not a decision level. The actual hierarchy maps to: **Strategic → Tactical → Operational**.

### DPR's Three Verbosity Levels for Decision Capturing

From `activities/DPR-ArchitecturalDecisionCapturing.md` (lines 31–35):

| Level | Description | Template |
|-------|-------------|----------|
| **Minimal** | Decision outcome + "because" rationale | One sentence |
| **Medium** | Lean ADR template | MADR, Y-Statement, Nygard |
| **Full** | Full-fledged decision model | Academic templates |

### DPR's Five-Step Decision Capturing (EC-ADR)

From the same activity, Zimmermann proposes five steps:
1. Identify the decision to be made
2. Gather context and requirements
3. Identify alternatives
4. Make the decision (state outcome)
5. Record consequences and tradeoffs

This aligns well with our current schema structure but provides a pedagogical framing for the Socratic authoring process.

---

## P1: Add `decision_level` field

### Motivation

Our schema has `decision_type` (domain classification: `technology`, `security`, `process`, etc.) but lacks an **architectural altitude** dimension. DPR's strategic/tactical/stepwise distinction directly inspired this gap identification.

The same decision domain can span multiple levels:
- **Security + Strategic:** "Adopt zero-trust network architecture"
- **Security + Tactical:** "Use claim-based authorization in domain services"
- **Security + Operational:** "Use Ed25519 for JWT signing keys"

Without `decision_level`, these three decisions look identical when filtered by `decision_type: security`, but they have vastly different blast radii, stakeholder audiences, and reversal costs.

### Literature Review: How the Field Classifies Decision Scope

This proposal is grounded not only in DPR but in a broad landscape of academic and industry frameworks. Six major taxonomies for classifying architectural decisions by scope/altitude were identified.

---

#### 1. DPR — Strategic / Tactic / Stepwise (Zimmermann, 2020–2024)

**Primary source:** DPR repository, OST/HSR

DPR organizes design activities along three conceptual levels, derived from Domain-Driven Design and API design methodology:

| DPR Level | Focus | Artifacts |
|---|---|---|
| **Strategic DDD** | System landscape, bounded contexts, team boundaries, context maps | Context maps, bounded context diagrams |
| **Tactic DDD** | Domain model internals — aggregates, entities, value objects, domain events | Domain models, CRC cards |
| **Stepwise Service Design** | API endpoint design, protocol choices, SLA, deployment tech | CEL/REL tables, API descriptions, SLAs |

> **Clarification:** "Stepwise" is the name of a 7-step API design *methodology*, not a decision scope. The implicit hierarchy maps to: **Strategic → Tactical → Operational**.

**DPR Source Files:**

| File | Relevant Content |
|------|-----------------|
| `activities/DPR-StrategicDDD.md` | Bounded contexts as strategic units; relationship patterns (Shared Kernel, ACL, OHS, etc.) |
| `activities/DPR-TacticDDD.md` | Aggregates, entities, value objects; 3-step modeling process |
| `activities/SDPR-StepwiseServiceDesign.md` | 7-step API design — operational decisions emerge in Steps 4–7 |
| `artifact-templates/DPR-StrategicDDDContextMap.md` | Context map visualization — the canonical strategic DDD artifact |
| `roles/DPR-ApplicationArchitectRole.md` | Architect role table showing phase-aligned artifacts consumed/produced |

---

#### 2. Zimmermann's SOA Decision Model — Conceptual / Technology / Asset (Zimmermann et al., 2007–2012)

**Primary source:** [soadecisions.org](https://soadecisions.org); "An architectural decision modeling framework for service oriented architecture design" (University of Stuttgart, 2011)

In his **earlier** work (predating DPR), Zimmermann proposed a three-level abstraction model specifically for SOA decisions:

| Level | MDA Mapping | Focus | Example |
|---|---|---|---|
| **Conceptual** | High-level PIM | Strategic patterns, composition approaches, platform-independent design | "Use orchestration for multi-step business processes" |
| **Technology** | Hybrid PIM/PSM | Technology standards, platform mapping, protocol choices | "Use J2EE for enterprise services" or "Use GraphQL for client queries" |
| **Asset** | Low-level PSM | Vendor/product selection, library choices, framework versions | "Use IBM WebSphere Process Server" or "Use Spring Boot 3.x" |

> **Key insight:** This three-level model separates *rapidly changing* platform-specific concerns (asset level) from *enduring* conceptual decisions. It is the direct academic ancestor of DPR's Strategic/Tactic/Stepwise distinction, just named differently.

**Assessment:** Very close to our proposed `strategic`/`tactical`/`operational` but uses SOA-specific terminology ("asset" implies product selection, which is narrower than "operational"). The Conceptual/Technology/Asset names are less immediately intuitive for modern teams.

---

#### 3. Kruchten's Ontology — Existence / Property / Executive (Kruchten, 2004)

**Primary source:** "An Ontology of Architectural Design Decisions in Software-Intensive Systems," 2nd Groningen Workshop on Software Variability Management, 2004

Philippe Kruchten proposed a fundamentally different **type-based** (not scope-based) taxonomy:

| Type | Focus | Examples |
|---|---|---|
| **Existence** | What structural/behavioral elements exist (or must NOT exist: "ban" decisions) | "The system has 3 layers: data, business logic, UI"; "Communication between classes uses RMI" |
| **Property** | Quality traits, design rules, constraints | "All data at rest must be encrypted"; "Response time < 200ms" |
| **Executive** | Business-environment-driven: process, personnel, organization, technology mandates | "All API changes require CCB approval"; "The system must use J2EE" |

> **Key insight:** Kruchten's taxonomy is **orthogonal** to scope/altitude. A "strategic" decision could be an existence decision (creating a new bounded context), a property decision (defining enterprise-wide SLA targets), or an executive decision (mandating a cloud-first strategy). This means Kruchten's categories classify the *nature* of the decision, not its *altitude*.

**Assessment:** This taxonomy answers a different question. It's closer to our existing `decision_type` field than to the proposed `decision_level`. Kruchten's "executive" decisons roughly overlap with "strategic" level, but the mapping is not clean. **Not suitable as a replacement for scope-based classification**, but confirms that type and level are two independent dimensions.

---

#### 4. TOGAF ADM — Business / Data / Application / Technology Architecture (The Open Group)

**Primary source:** TOGAF Standard, The Open Group

TOGAF defines architecture across **four domains** (not scope levels per se, but related):

| Domain | Focus |
|---|---|
| **Business Architecture** | Business strategy, governance, organizational structure, key processes |
| **Data Architecture** | Data structures, relationships, governance, quality policies |
| **Application Architecture** | Application systems, interactions, relationships to business processes |
| **Technology Architecture** | Infrastructure — hardware, software, networks, platforms |

And the ADM phases iterate across these domains with increasing specificity:
- Phase A (Architecture Vision) → high-level strategic
- Phases B–D → domain-specific design
- Phases E–F → solution-level planning
- Phase G → implementation governance

> **Key insight:** TOGAF's four domains are **domain-parallel** (Business ↔ Data ↔ Application ↔ Technology), whereas our `decision_level` is a **vertical altitude** dimension. More importantly, TOGAF's concerns (enterprise-wide governance, regulatory alignment) map naturally to the "strategic" level, while their Technology Architecture maps to "operational." 

**Assessment:** TOGAF's four layers are too enterprise-architecture-specific. They describe *what domain* a decision affects, not *at what altitude* it's made. Our existing `decision_type` + `component` fields already cover this domain dimension. However, TOGAF confirms the validity of the strategic → operational gradient in architecture practice.

---

#### 5. C4 Model — System / Container / Component / Code (Brown, ~2006)

**Primary source:** [c4model.com](https://c4model.com/) by Simon Brown

The C4 model defines four abstraction levels for *visualizing* architecture:

| Level | Scope | Audience |
|---|---|---|
| **System Context** (Level 1) | How the system relates to users and external systems | Non-technical stakeholders, product owners |
| **Container** (Level 2) | Major runtime deployment units (services, databases, apps) | Developers, architects |
| **Component** (Level 3) | Internal structure within a container | Developers |
| **Code** (Level 4) | Class/function detail | Developers (often optional) |

> **Key insight:** C4's levels are for *diagramming/visualization*, not decision classification. However, they do suggest a **four-level model** for scope. Decisions at the System Context level = strategic; Container level = tactical; Component/Code level = operational.

**Assessment:** C4 confirms that the *visualization* community independently arrived at a similar 3–4 level hierarchy. But having four levels creates ambiguity: where do Container-level decisions end and Component-level ones begin? C4's own docs acknowledge that Level 4 (Code) is "often optional." For decision classification, the distinction between "component" and "code" is too granular — both are "operational" choices.

---

#### 6. Gregor Hohpe's Architect Elevator (2020)

**Primary source:** "The Software Architect Elevator" (O'Reilly, 2020); [architectelevator.com](https://architectelevator.com/)

Hohpe frames architecture as an **elevator** metaphor:

| Floor | Focus |
|---|---|
| **Penthouse** (Executive) | Business strategy, organizational design, "why are we building this?" |
| **Middle floors** (Architecture) | Cross-cutting technical decisions, trade-off analysis, "-ilities" |
| **Engine Room** (Implementation) | Specific technologies, frameworks, infrastructure details |

> **Key insight:** Hohpe explicitly argues architects must *ride the elevator* — the same person must understand decisions at all levels. He emphasizes "rate of change" as a key distinguishing factor: penthouse decisions change slowly (years), engine room decisions change fast (sprints). This directly aligns with our proposed "reversal cost" dimension.

**Assessment:** Hohpe's model strongly validates the three-level approach. His "penthouse/middle/engine room" maps perfectly to `strategic`/`tactical`/`operational`.

---

#### 7. Ford & Richards — Architectural Quantum (2021)

**Primary source:** "Software Architecture: The Hard Parts" (O'Reilly, 2021) by Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani

Ford and Richards introduce the concept of **architectural quantum** — the scope for a set of architecture characteristics. They emphasize:
- Decision scope varies from system-wide to component-specific
- Trade-off analysis is the core of architectural work
- **Fitness functions** provide measurable governance at each level

> **Key insight:** The "architectural quantum" concept validates that decisions have a natural *blast radius* and that this radius is a critical metadata dimension. Their approach doesn't prescribe fixed levels but supports the idea that decisions cluster into natural altitude bands.

---

#### 8. Jansen & Bosch — Architecture as Decision Composition (2005)

**Primary source:** "Software Architecture as a Set of Architectural Design Decisions" by Anton Jansen, Jan Bosch (University of Groningen, 2005)

Jansen and Bosch proposed that architecture should be viewed not as components-and-connectors but as the **cumulative outcome of design decisions** over time. They introduced the concept of decisions as first-class entities with:
- Relationships between decisions (constrains, follows-from, conflicts-with)
- Group decisions by shared topics and abstraction levels

This perspective reinforces that a `decision_level` field helps organize the decision log as a navigable knowledge base.

---

### Comparative Analysis: Three, Four, or More Levels?

| Framework | Number of Levels | Terms Used | Type of Classification |
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
| MADR Categories | N/A | Subfolder-based | Organizational (not altitude) |
| arc42 Section 9 | N/A | No prescribed categories | Freeform |
| ISO/IEC/IEEE 42010 | N/A | No prescribed taxonomy for decisions | Viewpoint-based |

#### Finding: Three Levels Is the Consensus

The evidence strongly converges on **three levels**:

1. **Every prescriptive framework that classifies by scope/altitude uses exactly three levels.** DPR→3, SOA Decisions→3, Hohpe→3, Management Science→3.

2. **Four-level models either have a redundant bottom level (C4's "Code" is optional) or classify by domain rather than altitude (TOGAF).** When C4 maps to decisions, practitioners naturally collapse it to 3: system-wide = strategic, container = tactical, component+code = operational.

3. **Kruchten's three-category ontology is orthogonal** — it classifies the *nature* of decisions (structural vs. quality vs. executive) rather than their altitude. This confirms that `decision_type` and `decision_level` are independent dimensions, and both are needed.

4. **Standards bodies (ISO 42010, arc42) deliberately don't prescribe categories**, confirming this is a design choice for each framework — there is no "standard" we're violating by choosing three.

5. **Management science universally uses the strategic/tactical/operational triad** for decision classification. This terminology is immediately understood across disciplines.

#### Why Not Four or Five Levels?

Several more granular options were considered:

| Candidate | Assessment |
|---|---|
| **Split "operational" into "technology" + "implementation"** | Zimmermann himself moved away from this (Conceptual/Technology/Asset → Strategic/Tactic/Stepwise). The distinction between "which technology" and "which specific product" is rarely worth capturing as separate metadata — both are "operational" in practice. |
| **Add "enterprise" above "strategic"** | Some EA frameworks distinguish enterprise-wide from system-specific strategic decisions. However, our framework targets a single product/system ADR repository, not an enterprise-wide decision log. If a decision is truly enterprise-wide, it's strategic for our purposes. |
| **Mirror C4 with four levels** | System/Container/Component/Code maps poorly to decision altitude. "Component" and "Code" level decisions cannot be meaningfully distinguished for ADR metadata purposes. |
| **Use Kruchten's types as levels** | Existence/Property/Executive are orthogonal to scope — applying them would conflate two independent dimensions. |

**Recommendation: Three levels (`strategic`, `tactical`, `operational`) is the correct choice.** This is:
- Grounded in the broadest academic consensus
- Immediately intuitive (standard management terminology)
- Consistent with Zimmermann's own evolution from SOA→DPR
- Validated by Hohpe's practitioner-oriented model
- Sufficient for filtering without overfitting

---

### Proposed Schema Change

Add to `adr.properties`:

```json
"decision_level": {
    "type": "string",
    "enum": ["strategic", "tactical", "operational"],
    "description": "Architectural scope/altitude. 'strategic' = system landscape, bounded contexts, team/org boundaries, cross-cutting enterprise concerns, multi-year impact. 'tactical' = domain model, component design patterns, cross-cutting technical patterns, subsystem-scoped. 'operational' = specific technology/library/protocol/product choices, API design decisions, deployment configuration, usually swappable."
}
```

**Required or optional?** Optional — same as `priority` and `confidence`.

### Why These Three Terms?

| Term | Chosen Because | Rejected Alternatives |
|---|---|---|
| `strategic` | Universal management term; used by DPR, Hohpe, TOGAF (implicitly), management science | `enterprise` (too EA-specific), `conceptual` (Zimmermann SOA term — too abstract), `penthouse` (Hohpe metaphor — not self-documenting) |
| `tactical` | Universal management term; used by DPR, management science, military doctrine | `technology` (Zimmermann SOA term — too narrow, implies tech-only), `middle` (Hohpe — not descriptive), `application` (TOGAF — conflates domain with altitude) |
| `operational` | Universal management term; used by management science, DPR (implied) | `asset` (Zimmermann SOA term — implies vendor/product selection only), `engine-room` (Hohpe metaphor), `implementation` (too code-level), `code` (C4 — too granular) |

### The Two Independent Dimensions

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

This matrix demonstrates why both dimensions are needed: "technology" decisions exist at all three altitude levels, and "strategic" decisions exist across all type domains.

### Proposed Glossary Entries

| Level | Scope | Typical Stakeholders | Reversal Cost | Rate of Change | DPR Mapping | Hohpe Mapping | Kruchten Overlap |
|-------|-------|---------------------|---------------|----------------|-------------|---------------|------------------|
| `strategic` | Enterprise/landscape, bounded contexts, team boundaries, cross-cutting enterprise architectural concerns | C-suite, Enterprise Architects, Product leadership | Very high — shapes roadmap and org design | Years | Strategic DDD | Penthouse | Often "executive" |
| `tactical` | Domain model, component patterns, cross-cutting technical patterns (caching, messaging, auth) | Software Architects, Tech Leads, Senior Engineers | Moderate — confined to subsystem boundaries | Quarters/months | Tactic DDD | Middle floors | Often "existence" |
| `operational` | Specific tech choices, API protocols, deployment configs, libraries, framework versions | Engineers, DevOps, API designers | Lower — usually swappable without architectural redesign | Sprints/weeks | Stepwise Service Design (Steps 4–7) | Engine Room | Often "property" |

### Discriminating Heuristics

To help ADR authors select the correct level, provide these heuristics:

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

### Classification of Existing ADRs

| Existing ADR | `decision_type` | Proposed `decision_level` | Rationale |
|---|---|---|---|
| ADR-0000 Adopt Governed ADR Process | `process` | `strategic` | Enterprise-wide process that shapes all future decisions |
| ADR-0001 DPoP over mTLS | `technology` | `operational` | Specific protocol/library choice |
| ADR-0002 Reference Tokens over JWT | `technology` | `tactical` | Token architecture pattern affecting multiple components |
| ADR-0004 Ed25519 over RSA for JWT Signing | `technology` | `operational` | Specific algorithm choice, easily swappable |
| ADR-0005 BFF Token Mediator for SPA | `security` | `tactical` | Architectural pattern (BFF) across frontend/backend |
| ADR-0006 Session Enrichment for Step-Up | `technology` | `tactical` | Cross-cutting session management pattern |
| ADR-0007 Centralized Secret Store | `technology` | `tactical` | Infrastructure pattern affecting all secret consumers |
| ADR-0008 Defer OpenID Federation | `technology` | `strategic` | Enterprise trust establishment decision with multi-year implications |

### Implementation Checklist

- [ ] Add `decision_level` to `adr.properties` in `schemas/adr.schema.json`
- [ ] Add glossary entries to `docs/glossary.md` (new "Decision Level Classification" section)
- [ ] Add discriminating heuristics table to `docs/SCHEMA_REFERENCE.md`
- [ ] Update `docs/SCHEMA_REFERENCE.md` with the new field and two-dimensional matrix
- [ ] Update example ADRs to include `decision_level` where appropriate
- [ ] Update ADR-0000 to include `decision_level: strategic`
- [ ] Update `repomix-instruction.md` / AI bundle instructions to reference `decision_level`
- [ ] Update Socratic interview to ask about decision altitude (using heuristics)
- [ ] Update rendered ADRs
- [ ] Regenerate bundle

### Secondary Sources Referenced

| Source | Year | Contribution to P1 |
|---|---|---|
| Zimmermann, "SOA Decision Models" | 2007–2012 | Conceptual/Technology/Asset — direct ancestor of three-level model |
| Kruchten, "Ontology of Architectural Design Decisions" | 2004 | Existence/Property/Executive — confirms type ≠ level (orthogonal) |
| Jansen & Bosch, "Architecture as Decision Composition" | 2005 | Decisions as first-class entities; grouping by abstraction level |
| TOGAF ADM | Ongoing | Business/Data/Application/Technology — domain-parallel, not altitude |
| Brown, C4 Model | ~2006 | System/Container/Component/Code — 4 visualization levels collapse to 3 for decisions |
| Hohpe, "The Software Architect Elevator" | 2020 | Penthouse/Middle/Engine Room — validates three levels, adds "rate of change" heuristic |
| Ford & Richards, "Software Architecture: The Hard Parts" | 2021 | Architectural quantum — confirms decisions have natural blast radius |
| Bass, Clements, Kazman, "Software Architecture in Practice" (ADD 3.0) | 2012 | Attribute-Driven Design iterates across abstraction levels |
| Zimmermann, DPR | 2020–2024 | Strategic DDD / Tactic DDD / Stepwise — the primary inspiration |
| ISO/IEC/IEEE 42010 | 2011 | No prescribed decision taxonomy — confirms this is a design choice |
| arc42 (Starke) | Ongoing | Section 9: no prescribed categories — same confirmation |
| MADR (adr.github.io) | Ongoing | Uses subfolder categories, not altitude metadata |

---

## P2: Add Y-Statement Rendering Capability

### Motivation

DPR's **Y-Statement** (also called "Why-Statement") template from `artifact-templates/DPR-ArchitecturalDecisionRecordYForm.md` is a single-sentence summary:

> *"In the context of **[use case/user story]**, facing **[concern/quality attribute]**, we decided for **[option]** and against **[rejected alternatives]**, to achieve **[quality goals/benefits]**, accepting that **[tradeoffs/downsides]**."*

The template's visual structure divides into an **upper part** (context: "In the context of", "facing") and a **bottom part** (tradeoffs: "to achieve", "accepting that"). The upper part was added by Zimmermann to George Fairbanks' Architecture Haiku concept (WICSA 2011).

Our schema already contains all constituent parts:

| Y-Statement Part | Schema Source |
|---|---|
| "In the context of..." | `context.summary` |
| "facing..." | `context.business_drivers` + `context.technical_drivers` |
| "we decided for..." | `decision.chosen_alternative` |
| "and against..." | `alternatives[].name` (where not chosen) |
| "to achieve..." | `consequences.positive` |
| "accepting that..." | `decision.tradeoffs` or `consequences.negative` |

### Literature Review

#### 1. The Y-Statement — Origins and Structure (Zimmermann, SATURN 2012)

**Primary source:** Olaf Zimmermann, "Making Architectural Knowledge Sustainable: Industrial Practice Report and Outlook", SATURN 2012; Blog post: [medium.com/@docsoc/y-statements](https://medium.com/@docsoc/y-statements-10eb07b5a177)

The Y-Statement was introduced at the SATURN 2012 conference and has been practiced at ABB and taught at HSR/OST since 2013. Its name comes from its purpose: answering **"WH(Y)"** questions about architecture.

**Canonical six-part structure:**

| # | Part | Maps to... | Purpose |
|---|---|---|---|
| 1 | **"In the context of..."** | Functional requirement, use case, or component | Sets the decision scope |
| 2 | **"facing..."** | Non-functional requirement or quality attribute need | Identifies the quality concern being addressed |
| 3 | **"we decided for..."** | Chosen option | States the outcome |
| 4 | **"and neglected..."** | Rejected alternatives | Records what was considered but not chosen |
| 5 | **"to achieve..."** | Benefits, quality satisfaction | Explains expected positive outcome |
| 6 | **"accepting that..."** | Drawbacks, costs, undesired consequences | Captures the acknowledged tradeoff |

**Variant: The "because" extension.** Zimmermann notes that an optional "because..." clause can be appended for additional rationale that doesn't fit the tradeoff format. This produces the **long form**:

> *"In the context of **[A]**, facing **[B]**, we decided for **[C]** and neglected **[D]**, to achieve **[E]**, accepting **[F]**, because **[G]**."*

**Practical observations from the DPR documentation:**
- Some readers find the single long sentence unwieldy; Zimmermann suggests **splitting into 2–3 sentences** when this feedback arises.
- The Y-Statement is positioned as a **"medium verbosity"** option in DPR's decision-capturing activity — lighter than full MADR logs, heavier than informal bullet points.
- AD Mentor (HSR/OST tool) has a native Y-Statement template for its solution space models.

#### 2. Architecture Haiku — The Intellectual Ancestor (Fairbanks, WICSA 2011)

**Primary source:** George Fairbanks, Architecture Haiku tutorial, CompArch/WICSA 2011; [georgefairbanks.com](https://www.georgefairbanks.com/blog/comparch-wicsa-2011-panel-discussion-and-haiku-tutorial/)

Fairbanks' Architecture Haiku is a **one-page, uber-terse design description** intended for quick communication in Agile contexts. Key elements:

| Element | Purpose |
|---|---|
| Brief solution description | What was built |
| Architectural drivers | Why it was built this way |
| Quality attribute priorities | What qualities matter most |
| Design rationales & tradeoffs | What was gained and lost |
| Constraints | Non-negotiable boundaries |
| Architectural styles/patterns | How it was structured |

> **Key insight:** Fairbanks' contribution to the Y-Statement was specifically the **tradeoff half**: "to achieve..., accepting that..." — the idea that every decision has a price. Zimmermann added the **context half**: "In the context of..., facing..." — providing the requirement-driven framing. Together they form the Y's upper and lower parts.

The Architecture Haiku's value is its **forced brevity** — fitting on one page means you must prioritize what matters. This same principle applies to the Y-Statement: a single sentence forces the author to distill the decision to its essence.

#### 3. MADR 4.0 — Decision Outcome Section (adr.github.io)

**Primary source:** [github.com/adr/madr](https://github.com/adr/madr); MADR 4.0.0 template

MADR's equivalent of the Y-Statement is its **"Decision Outcome"** section:

```markdown
## Decision Outcome

Chosen option: "{title of option 1}", because
{justification. e.g., only option, which meets k.o. criterion decision driver
| which resolves force {force} | … | comes out best (see below)}.
```

**Comparison with Y-Statement:**

| Aspect | Y-Statement | MADR Decision Outcome |
|---|---|---|
| Format | Single structured sentence | Section header + free-text |
| Context included? | ✅ Built into the sentence | ❌ Covered in separate section |
| Rejected alternatives? | ✅ "and neglected..." | ❌ Covered in separate section |
| Tradeoffs? | ✅ "accepting that..." | ❌ Covered in "Consequences" |
| Standalone? | ✅ Self-contained | ❌ Requires reading other sections |
| Machine-parseable? | ⚠️ Natural language | ⚠️ Natural language |
| Best for... | Decision logs, indexes, quick reference | Full ADR documents |

> **Key insight:** The Y-Statement is strictly superior for **standalone communication** — it can be extracted from any ADR and understood without reading anything else. MADR's Decision Outcome depends on preceding sections. This makes Y-Statements ideal for rendered summaries, Slack/chat sharing, and ADR indexes.

#### 4. Nygard — Context / Decision / Consequences (2011)

**Primary source:** Michael Nygard, ["Documenting Architecture Decisions"](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions), 2011

Nygard's original ADR format uses three sections that roughly map to the Y-Statement:

| Nygard Section | Y-Statement Equivalent |
|---|---|
| **Context** | "In the context of..., facing..." |
| **Decision** | "we decided for..." |
| **Consequences** | "to achieve..., accepting that..." |

Nygard does not include rejected alternatives in the core structure — they may appear in the context or consequences. This is a notable gap that the Y-Statement's "and neglected..." clause explicitly addresses.

#### 5. Tyree & Akerman — 15+ Section Template (IEEE Software, 2005)

**Primary source:** Jeff Tyree & Art Akerman, "Architecture Decisions: Demystifying Architecture", IEEE Software, 2005

The most comprehensive traditional template with 15+ sections including Assumptions, Constraints, Implications, Related Decisions, Related Requirements, and Notes. Its summary capability comes from the **"Decision"** section:

> "The architecture decision made, with justification."

This is close to MADR's Decision Outcome. The template's strength is thorough cross-referencing (Related Decisions, Related Requirements), but it has no single-sentence summary equivalent to the Y-Statement. Its comprehensiveness makes it ill-suited for quick communication.

#### 6. Emerging Pattern: AI-Generated Decision Summaries

Recent industry practice (2024–2026) shows growing use of LLMs for:
- **Generating Y-Statements from structured ADR data** — exactly what our P2 proposes
- **Producing audience-adapted summaries** — same decision, different phrasing for executives vs. engineers
- **Quality-checking Y-Statements** — verifying that the summary accurately reflects the full ADR content

Tools like Equal Experts' ADR approach and research (arxiv.org, "LLMs for Software Architecture") demonstrate that LLMs can produce Y-Statements that are "relevant and accurate" when given structured input, though they may "fall short of human-level performance" and occasionally generate justifications that don't fully align with the decision context.

> **Key insight for P2:** Our structured YAML schema provides *exactly* the kind of clean, well-separated input that LLMs need to generate accurate Y-Statements. The six constituent fields map directly to the six Y-Statement parts with no ambiguity.

### Comparative Analysis: Decision Summary Formats

| Format | Length | Standalone? | Includes Rejected? | Includes Tradeoffs? | Machine-Generable? | Best For |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Y-Statement (short)** | 1 sentence | ✅ | ✅ | ✅ | ✅ | Indexes, logs, chat, dashboards |
| **Y-Statement (long)** | 1–2 sentences | ✅ | ✅ | ✅ | ✅ | Full standalone summary |
| **MADR Decision Outcome** | 1–3 sentences | ❌ | ❌ | ❌ | ⚠️ | Within full MADR documents |
| **Nygard Decision section** | Free-text paragraph | ❌ | ❌ | ❌ | ⚠️ | Within full Nygard ADRs |
| **Tyree-Akerman Decision** | 1–2 sentences + justification | ❌ | ❌ | ❌ | ⚠️ | Enterprise governance |
| **Architecture Haiku** | 1 page | ✅ | ✅ | ✅ | ❌ | Architecture overview |

> **Conclusion:** The Y-Statement is the **most information-dense** standalone decision summary format available. No other format packs context, decision, rejected alternatives, benefits, and tradeoffs into a single sentence. This makes it uniquely suited for automated rendering from structured YAML.

### Design Decisions

#### Why Y-Statement over alternatives?

1. **Self-contained.** Unlike MADR's Decision Outcome, a Y-Statement can be understood without reading anything else. This is critical for AI-generated summaries sent via chat, email, or rendered in indexes.

2. **Deterministically generable.** Our YAML schema already contains all six constituent parts in separate, well-typed fields. A template-based renderer can assemble the Y-Statement with no ambiguity and no hallucination risk.

3. **Established lineage.** The format has a 13+ year track record (SATURN 2012) with industrial use at ABB and academic use at HSR/OST. It's not a novel invention — it's a proven standard.

4. **Replaces `adr.summary`.** The Y-Statement is a strictly more informative summary than the free-text elevator pitch. No established ADR template (MADR, Nygard, Tyree/Akerman, DPR) uses both a summary and a Y-Statement. Zimmermann explicitly positions the Y-Statement as a self-contained summary. The `adr.summary` field was removed to eliminate DRY violation.

#### Long form only

We use **long form only** (with the "because" clause). The "because" clause maps to `decision.rationale` — the most important field to surface for decision understanding. Since the Y-Statement is a static schema field (not dynamically generated), the extra clause adds critical context that makes the statement self-contained. The short form omits the rationale, which is the core "why" — unacceptable for a decision record.

#### Implementation approach: Schema field + rendering (static)

**Revised recommendation:** The Y-Statement should be a **schema field** (`adr.y_statement`), authored once when the ADR reaches `accepted` status. The render script then includes it in the Markdown output. No dynamic generation at render time.

**Why static over dynamic?**

The constituent schema fields (`context.summary`, `consequences.positive`, `decision.tradeoffs`, etc.) are **multi-paragraph Markdown** — often containing Mermaid diagrams, bullet lists, and detailed architectural prose. Assembling a Y-Statement from these fields is a *summarization* task, not a *concatenation* task. A deterministic script cannot distill 5 paragraphs of context into the single "In the context of..." clause — that requires authorial judgment (human or AI-assisted).

| Field | What it captures | How it's created | Sync concern? |
|---|---|---|---|
| `adr.y_statement` | Structured 7-part decision sentence (long form) | Auto-generated by AI from interview answers, confirmed by author | ❌ — accepted ADRs are immutable |

**Why the original DRY objection was wrong:** The DRY argument assumed the Y-Statement is a mechanical derivation. It isn't — it's a *curated distillation*, like any summary. And since accepted ADRs are immutable (status changes require supersession), there is no drift/maintenance burden.

| Component | What | Status |
|---|---|---|
| **Schema field** | Add optional `adr.y_statement` string | ✅ Recommended — static, authored once |
| **Render script** | Display Y-Statement in rendered Markdown | ✅ Reads from schema field |
| **AI Skill / Socratic interview** | Prompt author to craft Y-Statement when finalizing ADR | ✅ Authoring aid, not runtime generation |
| ~~AI Bundle capability~~ | ~~Generate on-the-fly from context~~ | ❌ Rejected — must be static |
| ~~Script template assembly~~ | ~~Concatenate from constituent fields~~ | ❌ Rejected — can't summarize multi-paragraph fields |

### DPR Source Files

| File | Relevant Content |
|------|-----------------| 
| `artifact-templates/DPR-ArchitecturalDecisionRecordYForm.md` | Full Y-Statement template, examples, and Wikipedia citation |
| `activities/DPR-ArchitecturalDecisionCapturing.md` | Y-Statement as a "medium verbosity" option (line 34) |

### Example Y-Statement Output

For ADR-0001 (DPoP over mTLS):

> *In the context of the OIDC-based IAM platform, facing the need for sender-constrained tokens across public (mobile), confidential (backend), and partner clients, we decided for DPoP (RFC 9449) and against mTLS (RFC 8705) and a hybrid approach, to achieve unified sender-constraining without CDN/proxy infrastructure changes, accepting per-request proof generation overhead (~500 bytes) and client-side implementation complexity, because DPoP is the only mechanism that works for all three client types without infrastructure modifications, survives CDN TLS termination (eliminating a $50K/year Cloudflare add-on), and provides a single validation path that reduces operational complexity.*

### Implementation Checklist

- [ ] Add optional `adr.y_statement` string field to `schemas/adr.schema.json`
- [ ] Add `y_statement` to `adr-template.yaml` with authoring guidance comment
- [ ] Update `render-adr.py` to render Y-Statement section in Markdown output (from schema field)
- [ ] Update `.skills/adr-author/SKILL.md` to prompt for Y-Statement when finalizing an ADR
- [ ] Update `repomix-instruction.md` Socratic interview to prompt for Y-Statement at acceptance
- [ ] Populate `y_statement` in all example ADRs and ADR-0000
- [ ] Credit DPR / Zimmermann / Fairbanks as sources (SATURN 2012, WICSA 2011)
- [ ] Re-render all ADRs
- [ ] Regenerate bundle

### Secondary Sources Referenced

| Source | Year | Contribution to P2 |
|---|---|---|
| Zimmermann, "Y-Statements" (SATURN 2012) | 2012 | Canonical six-part template, "because" extension, practical pitfalls |
| Fairbanks, "Architecture Haiku" (WICSA 2011) | 2011 | Intellectual ancestor — the "to achieve / accepting that" tradeoff structure |
| Zimmermann, "Y-Statements" (Medium blog) | 2020 | Expanded examples, known uses, advice on convincing justifications |
| Zimmermann, "AD Making Of" (ozimmer.ch) | 2020 | Historical context, short/medium/long-form verbosity guidance |
| DPR Y-Statement Template (GitHub) | 2022 | Canonical template structure, Wikipedia example, tool support |
| MADR 4.0.0 Template (adr.github.io) | Ongoing | Decision Outcome comparison — lacks standalone self-containment |
| Nygard, "Documenting Architecture Decisions" | 2011 | Original ADR format — Context/Decision/Consequences mapping |
| Tyree & Akerman, IEEE Software | 2005 | Comprehensive template — no single-sentence summary equivalent |
| Equal Experts, "AI-assisted ADR" | 2024 | LLM-generated summaries from structured input — validates our approach |
| Arxiv, "LLMs for Software Architecture" | 2024 | GPT-4 can generate "relevant and accurate" decisions from structured contexts |


## P3: Add Quality Attribute Scenario (QAS) `measure` Field

### Motivation

DPR emphasizes that ADR rationale should trace back to **measurable quality attribute scenarios**, not vague NFRs. The SMART NFR Elicitation activity (`activities/DPR-SMART-NFR-Elicitation.md`) defines "SMART" as:

| Letter | Meaning (DPR definition) |
|--------|-------------------------|
| **S** | **Specific** — Which feature or part of the system? Which environment (sunny day, peak, error)? |
| **M** | **Measurable** — How can testers verify it? Is it quantified? |
| **A** | **Agreed upon** — Do all stakeholders agree on S and M? |
| **R** | **Realistic** — Technically and economically feasible? |
| **T** | **Time-bound** — When must it be met? Growth path iteration to iteration? |

The QAS template from `artifact-templates/DPR-QualityAttributeScenario.md` adds structure:

| QAS Component | Purpose |
|---|---|
| **Stimulus** | What event triggers the quality concern? |
| **Environment** | Steady state, overload, or failure conditions? |
| **Response** | What should happen? |
| **Response Measure** | How is success measured? (quantitative) |

Our current `architecturally_significant_requirement` has only `id` + `description`. Teams frequently write vague NFRs:

> ❌ `"The system should be fast"`  
> ❌ `"High availability is required"`

Instead of:

> ✅ `"p95 API response latency < 200ms under 1000 concurrent users"`  
> ✅ `"99.9% uptime measured monthly, with RTO < 15 minutes"`

### DPR Source Files

| File | Relevant Content |
|------|-----------------|
| `artifact-templates/DPR-QualityAttributeScenario.md` | Full QAS template with annotated diagram and example |
| `activities/DPR-SMART-NFR-Elicitation.md` | 3-step NFR elicitation approach; SMART criteria definitions; assessment table template |

### Proposed Schema Change

Add an optional `measure` field to `#/$defs/architecturally_significant_requirement`:

```json
"measure": {
    "type": "string",
    "description": "Measurable acceptance criterion (SMART 'M'). For non-functional requirements, express as a quantitative threshold under specific conditions (QAS-style). Examples: 'p95 latency < 200ms under 1000 concurrent users', 'Recovery time < 15 minutes from single-node failure', '≥ 95% of API consumers can integrate within 1 sprint'."
}
```

### Implementation Checklist

- [ ] Add `measure` field to `#/$defs/architecturally_significant_requirement` in schema
- [ ] Update `docs/SCHEMA_REFERENCE.md` with new field and QAS/SMART guidance
- [ ] Add QAS and SMART NFR to glossary
- [ ] Add AI bundle Socratic prompting for measures during ASR capture
- [ ] Update 2–3 example ADRs with `measure` values on non-functional ASRs
- [ ] Credit SEI/CMU (Bass, Clements, Kazman) and DPR
- [ ] Regenerate bundle

---

## P4: Add "Definition of Done" for Architecture Decisions

### Motivation

DPR's `activities/DPR-ArchitecturalDecisionCapturing.md` (line 71) references Zimmermann's "ecADR" — a Definition of Done for AD making. From the linked blog post and `artifact-templates/DPR-ArchitecturalDecisionRecordYForm.md` (line 89), the DoD comprises:

| DoD Criterion | Our Coverage |
|---|---|
| ≥ 2 alternatives considered | ✅ Schema-enforced (`minItems: 2`) |
| Pros and cons for each alternative | ✅ Schema-enforced (`required: [pros, cons]`) |
| Decision outcome stated | ✅ Schema-enforced (`required: [chosen_alternative]`) |
| Rational/justification provided | ✅ Schema-enforced (`required: [rationale]`) |
| Consequences captured (positive + negative) | ✅ Schema-enforced (`required: [consequences]`) |
| NFRs/quality goals referenced | ⚠️ *Optional* (`architecturally_significant_requirements` not required) |
| Tradeoffs explicitly acknowledged | ⚠️ *Optional* (`decision.tradeoffs` not required) |
| Decision reviewed by peers | ⚠️ *Process-level* (PR workflow, not schema) |
| Alternatives given fair treatment | ⚠️ `review-adr.py` checks balance heuristically |
| Accountability established | ✅ `decision_owner` is required |
| Consistency between decisions checked | ⚠️ Manual / AI review |
| Status and timestamp assigned | ✅ Schema-enforced |

The DPR also emphasizes three quality properties for decision logs (line 73):
- **Accountability** of decision makers
- **Consistency** between decisions and implementations
- **Continuity** (currentness of all design artifacts)

### DPR Source Files

| File | Relevant Content |
|------|-----------------|
| `activities/DPR-ArchitecturalDecisionCapturing.md` | ecADR reference (line 71), quality properties (line 73), five-step EC-ADR process |
| `artifact-templates/DPR-ArchitecturalDecisionRecordYForm.md` | DoD blog link (line 89), "ADR = Any Decision Record?" (line 90) |

### Proposed Implementation

**Documentation-only change.** Add a "Definition of Done for ADRs" section to `docs/adr-process.md`:

1. List completeness criteria with enforcement mechanism (schema / script / manual)
2. Map DPR's ecADR to our existing validations
3. Credit Zimmermann's blog post as source

Optionally, enhance `review-adr.py` with soft warnings when:
- `architecturally_significant_requirements` is absent
- `decision.tradeoffs` is absent
- All alternatives have identical pros/cons count

### Implementation Checklist

- [ ] Add "Definition of Done for ADRs" section to `docs/adr-process.md`
- [ ] Add credit/reference to Zimmermann's ecADR blog post
- [ ] (Optional) Add soft warnings to `review-adr.py`
- [ ] Update AI bundle Socratic interview to check DoD before finalizing
- [ ] Regenerate bundle

---

## P5: Add Architectural Significance Test Guidance

### Motivation

Not every decision needs to be an ADR. DPR has a stub activity `activities/futureWork/DPR-ASRTest.md` that currently links to Zimmermann's [Architectural Significance Test](https://medium.com/olzzio/architectural-significance-test-9ff17a9b4490) blog post. The key criteria (derived from the blog post and the Architecture Modeling activity):

1. Does the decision affect the **system structure** (components, connectors)?
2. Does it affect **non-functional characteristics** (performance, security, scalability)?
3. Does it affect **external interfaces** (APIs, integrations)?
4. Is it **cross-cutting** (affects multiple components/teams)?
5. Is it **hard to reverse** (high reversal cost)?
6. Does it **set a precedent** or constrain future decisions?
7. Does it involve **risk or uncertainty**?
8. Are **multiple stakeholders** affected?

### DPR Source Files

| File | Relevant Content |
|------|-----------------|
| `activities/futureWork/DPR-ASRTest.md` | Stub — links to blog post |
| `activities/DPR-SMART-NFR-Elicitation.md` | Risk-based prioritization reference (Glinz 2006) |
| `activities/DPR-ArchitectureModeling.md` | Line 31: traces design to "architecturally significant requirements" |

### Proposed Implementation

**Documentation-only change.** Add "When to Write an ADR" section to `docs/adr-process.md`. Suggest: if ≥ 2 criteria are met, an ADR is warranted.

### Implementation Checklist

- [ ] Add "When to Write an ADR" section to `docs/adr-process.md`
- [ ] Credit Zimmermann/Fairbanks
- [ ] (Optional) Add significance test guidance to AI bundle Socratic interview
- [ ] Regenerate bundle

---

## P6: Add `scope` / `phase` Metadata

### Assessment: Skip (Redundant)

DPR artifact YAML frontmatter includes:

```yaml
Scope: Entire system, component, connector, class, ...
Phases: Design (all levels)
Abstraction/Refinement Level: All
```

**Why skip:**
- `Scope` → Covered by proposed `decision_level` (P1) + existing `adr.component`
- `Phases` → Maps to waterfall-style lifecycle; our `adr.status` lifecycle is more natural for GitOps
- `Abstraction/Refinement Level` → Subsumed by `decision_level`

---

## P7: Add "Definition of Ready" for Architecture Decisions

### Motivation

This is a **new proposal** discovered during the local deep scan. DPR's `activities/DPR-ArchitecturalDecisionCapturing.md` (line 131) links to Zimmermann's ["A Definition of Ready for Architectural Decisions (ADs)"](https://medium.com/olzzio/a-definition-of-ready-for-architectural-decisions-ads-2814e399b09b).

While the DoD (P4) answers "Is this ADR complete enough?", the **DoR answers "Is there enough context to *start* making this decision?"** — a precondition check that's useful for our `draft` → `proposed` transition.

A Definition of Ready could include:
1. Is the **problem statement** clear? (Do we know *why* a decision is needed?)
2. Are the **driving quality attributes** identified (even if not fully specified)?
3. Are there at least **two candidate alternatives** identified?
4. Is the **decision owner** identified?
5. Are the **affected stakeholders** identified?
6. Is there sufficient **information to evaluate** alternatives? (PoC results, benchmarks, prior art)

### DPR Source Files

| File | Relevant Content |
|------|-----------------|
| `activities/DPR-ArchitecturalDecisionCapturing.md` | Line 131: DoR blog post link |
| `activities/DPR-SMART-NFR-Elicitation.md` | Lines 51–55: SMART criteria provide readiness indicators |

### Proposed Implementation

**Documentation-only change.** Add a "Definition of Ready" section to `docs/adr-process.md`, complementing the DoD (P4). This guides teams on when an ADR is ready to move from `draft` to `proposed`.

### Implementation Checklist

- [ ] Add "Definition of Ready for ADRs" section to `docs/adr-process.md`
- [ ] Map DoR criteria to schema fields that should be populated before status = `proposed`
- [ ] Credit Zimmermann's DoR blog post
- [ ] (Optional) Add DoR check to validator as soft warning when status = `proposed`
- [ ] Regenerate bundle

---

## P8: ADR Verbosity Levels Guidance

### Motivation

**New proposal** from deep scan. DPR explicitly defines three verbosity levels for decision capturing (`activities/DPR-ArchitecturalDecisionCapturing.md`, lines 31–35):

| Level | What to capture | When appropriate |
|-------|----------------|------------------|
| **Minimal** | Decision outcome + "because" rationale | Low-impact, easily reversible, team-internal decisions |
| **Medium** | Lean ADR template (Y-Statement, MADR, Nygard) | Most architectural decisions |
| **Full** | Full-fledged decision model with comprehensive analysis | High-impact, regulatory, cross-org decisions |

Our schema is inherently "full" — it supports extensive detail. But not every decision needs all fields populated. This proposal adds *guidance* on when it's OK to be concise vs. when full rigor is expected.

This maps naturally to our existing `priority` field:
- `low` priority → minimal verbosity acceptable
- `medium` priority → medium verbosity expected
- `high`/`critical` priority → full verbosity expected

### DPR Source Files

| File | Relevant Content |
|------|-----------------|
| `activities/DPR-ArchitecturalDecisionCapturing.md` | Lines 31–35: verbosity levels; Line 67: "stick to one template"; Line 70: "do not spend more time on capturing than on making" |

### Proposed Implementation

**Documentation-only change.** Add "ADR Verbosity Guidance" section to `docs/adr-process.md` mapping priority levels to expected completeness.

### Implementation Checklist

- [ ] Add verbosity guidance section to `docs/adr-process.md`
- [ ] Map priority levels to expected field completeness
- [ ] Update AI bundle Socratic interview to calibrate depth based on stated priority
- [ ] Credit DPR's three-level verbosity model
- [ ] Regenerate bundle

---

## P9: NFR Landing Zones for Quality Requirements

### Motivation

**New proposal** from deep scan. DPR's SMART NFR Elicitation activity (`activities/DPR-SMART-NFR-Elicitation.md`, line 122) introduces the concept of **landing zones** (credited to Rebecca Wirfs-Brock):

> *Define landing zones if single numbers are hard to come up with and agree upon. For instance, a triplet of "minimal", "target", and "outstanding" quality goals may define such landing zone.*

This is directly applicable to our QAS `measure` field (P3). Instead of requiring a single threshold, allow teams to express a range:

```yaml
non_functional:
  - id: NF-001
    description: "API response time under normal load"
    measure: "p95 latency < 500ms (minimal), < 200ms (target), < 100ms (outstanding)"
```

### DPR Source Files

| File | Relevant Content |
|------|-----------------|
| `activities/DPR-SMART-NFR-Elicitation.md` | Line 122: landing zones concept, Wirfs-Brock credit |
| `artifact-templates/DPR-QualityAttributeScenario.md` | "Define the desired behavior in different environments such as steady state, high workload, and error cases" |
| `artifact-templates/SDPR-ServiceLevelAgreement.md` | SLO pattern — analogous measurable quality commitment |

### Proposed Implementation

**Documentation-only enhancement to P3.** Rather than adding schema fields for min/target/outstanding, document the landing zone pattern as a best practice in the `measure` field's guidance. The free-text `measure` field can accommodate this naturally.

### Implementation Checklist

- [ ] Include landing zone guidance in the `measure` field documentation (P3)
- [ ] Add landing zone examples to `docs/SCHEMA_REFERENCE.md`
- [ ] Update AI bundle to prompt for landing zones during QAS capture
- [ ] Credit Wirfs-Brock for the landing zone concept
- [ ] Regenerate bundle

---

## Cross-Reference: DPR Method Elements → ADR Governance Mapping

| DPR Element | DPR File | ADR Governance Equivalent | Gap? |
|---|---|---|---|
| Y-Statement ADR template | `artifact-templates/DPR-ArchitecturalDecisionRecordYForm.md` | All schema fields exist; rendering missing | P2 |
| QAS template | `artifact-templates/DPR-QualityAttributeScenario.md` | `architecturally_significant_requirements.non_functional` lacks `measure` | P3 |
| SMART NFR Elicitation | `activities/DPR-SMART-NFR-Elicitation.md` | Partially covered; no SMART criteria guidance | P3, P9 |
| AD Capturing | `activities/DPR-ArchitecturalDecisionCapturing.md` | Core schema ✅; missing DoD/DoR/verbosity guidance | P4, P7, P8 |
| Strategic DDD | `activities/DPR-StrategicDDD.md` | `decision_type` captures domain but not altitude | P1 |
| Tactic DDD | `activities/DPR-TacticDDD.md` | Same as above | P1 |
| Stepwise Service Design | `activities/SDPR-StepwiseServiceDesign.md` | Not directly mapped; operational decisions | P1 |
| Application Architect role | `roles/DPR-ApplicationArchitectRole.md` | `decision_owner.role` captures position | ✅ No gap |
| Context Diagram | `artifact-templates/DPR-ContextDiagram.md` | Mermaid in `context.summary` or descriptions | ✅ No gap |
| Domain Model | `artifact-templates/DPR-DomainModel.md` | Mermaid in `alternatives[].description` | ✅ No gap |
| CRC Card | `artifact-templates/DPR-CRCCard.md` | Not applicable to ADR governance | N/A |
| SLA template | `artifact-templates/SDPR-ServiceLevelAgreement.md` | QAS measure + landing zones = similar | P3, P9 |
| DDD Context Map | `artifact-templates/DPR-StrategicDDDContextMap.md` | `context.summary` can embed Mermaid diagrams | ✅ No gap |
| ASR Test | `activities/futureWork/DPR-ASRTest.md` | No "when to write an ADR" guidance | P5 |
| Arch. Refactoring | `activities/futureWork/DPR-ArchitecturalRefactoring.md` | Supersession mechanism covers this | ✅ No gap |

---

## References

### Primary Sources (DPR)

| Resource | URL |
|----------|-----|
| DPR Repository | https://github.com/socadk/design-practice-repository |
| DPR GitPages | https://socadk.github.io/design-practice-repository/ |
| DPR eBook | https://leanpub.com/dpr |
| Y-Statements blog | https://medium.com/@docsoc/y-statements-10eb07b5a177 |
| AD Definition of Done (ecADR) | https://ozimmer.ch/practices/2020/05/22/ADDefinitionOfDone.html |
| AD Definition of Ready | https://medium.com/olzzio/a-definition-of-ready-for-architectural-decisions-ads-2814e399b09b |
| Architectural Significance Test | https://medium.com/olzzio/architectural-significance-test-9ff17a9b4490 |
| AD Making Of blog | https://ozimmer.ch/practices/2020/04/27/ArchitectureDecisionMaking.html |
| Sustainable AD article | https://www.infoq.com/articles/sustainable-architectural-design-decisions |

### Secondary Sources (P1 Literature Review)

| Resource | Author(s) | Year | URL / Citation |
|----------|-----------|------|----------------|
| SOA Architectural Decision Modeling | Zimmermann et al. | 2007–2012 | https://soadecisions.org |
| "An Ontology of Architectural Design Decisions" | Kruchten, P. | 2004 | 2nd Groningen Workshop on Software Variability Management |
| "Architecture as a Set of Design Decisions" | Jansen, A. & Bosch, J. | 2005 | University of Groningen; doi:10.1109/WICSA.2005.61 |
| TOGAF Standard (ADM) | The Open Group | Ongoing | https://www.opengroup.org/togaf |
| C4 Model | Brown, S. | ~2006 | https://c4model.com/ |
| "The Software Architect Elevator" | Hohpe, G. | 2020 | O'Reilly; https://architectelevator.com/ |
| "Software Architecture: The Hard Parts" | Ford, Richards, Sadalage, Dehghani | 2021 | O'Reilly |
| "Software Architecture in Practice" (ADD 3.0) | Bass, Clements, Kazman | 2012 | Addison-Wesley (3rd ed.) |
| ISO/IEC/IEEE 42010:2011 | ISO | 2011 | Architecture description standard |
| arc42 Template | Starke, G. | Ongoing | https://arc42.org/ |
| MADR Template | adr.github.io | Ongoing | https://github.com/adr/madr |
| Tyree & Akerman ADR Template | Tyree, J. & Akerman, A. | 2005 | IEEE Software |
| "Patterns for API Design" | Zimmermann, Stocker, Lübke, Zdun, Pautasso | 2022 | Addison-Wesley |

### Secondary Sources (P2 Literature Review)

| Resource | Author(s) | Year | URL / Citation |
|----------|-----------|------|----------------|
| Architecture Haiku (WICSA 2011) | Fairbanks, G. | 2011 | https://www.georgefairbanks.com/blog/comparch-wicsa-2011-panel-discussion-and-haiku-tutorial/ |
| "AD — The Making Of" (blog) | Zimmermann, O. | 2020 | https://ozimmer.ch/practices/2020/04/27/ArchitectureDecisionMaking.html |
| Nygard original ADR blog | Nygard, M. | 2011 | https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions |
| "Architecture Decisions: Demystifying Architecture" | Tyree, J. & Akerman, A. | 2005 | IEEE Software, Vol. 22, No. 2 |
| MADR 4.0.0 Template | adr.github.io | Ongoing | https://github.com/adr/madr |
| AI-Assisted ADRs (Equal Experts) | Equal Experts | 2024 | https://equalexperts.com |
| "LLMs for Software Architecture" | Various (arxiv) | 2024 | https://arxiv.org |
| AD Mentor Tool (HSR/OST) | OST | Ongoing | https://www.ost.ch/de/forschung-und-dienstleistungen/informatik/ifs-institut-fuer-software/labs/cloud-application-lab/architectural-knowledge-management-akm/admentor-tool |

### Other References

| Resource | URL |
|----------|-----|
| SMART Requirements (Mannion/Keepence 1995) | https://doi.org/10.1145/224155.224157 |
| QAS / SMART NFR background | SEI/CMU — Bass, Clements, Kazman: "Software Architecture in Practice" |
| Landing Zones (Wirfs-Brock) | http://wirfs-brock.com/blog/2011/07/29/agile-landing-zones/ |
| Microservice API Patterns (MAP) | https://microservice-api-patterns.org/ |
| ADR GitHub organization | https://adr.github.io/ |
| Context Mapper | https://contextmapper.org/ |
