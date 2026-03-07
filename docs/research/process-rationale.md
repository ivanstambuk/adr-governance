# ADR Process Design Rationale

> **Date:** 2026-03-07  
> **Author:** Ivan Stambuk  
> **Status:** Living document — updated as process elements are adopted or removed  
> **Repository:** `adr-governance`  
> **Related documents:**  
> - [`adr-process.md`](../adr-process.md) — the process itself  
> - [`schema-field-rationale.md`](schema-field-rationale.md) — field-level design rationale  
> - [`adr-template-comparison.md`](adr-template-comparison.md) — template-level survey  
> - [`schemas/adr.schema.json`](../../schemas/adr.schema.json) — schema source of truth

---

## Purpose

The [Schema Field Rationale](schema-field-rationale.md) answers: *"For every field in our schema, why does it exist?"*

**This document answers: *"For every process element in `adr-process.md`, why does it exist?"***

It provides the design rationale for each process section — justifying its inclusion against the academic literature, DPR (Design Practice Repository) method elements, and industry standards. It also records what was explicitly considered and rejected.

---

## Reading Guide

Each process element entry follows this structure:

| Element | Description |
|---|---|
| **Process location** | Section reference in `adr-process.md` |
| **What it does** | Brief description of the process element |
| **Academic lineage** | Where the concept comes from |
| **Coverage analysis** | How our framework maps to the source framework |
| **Design decisions** | Key choices made during adoption |
| **Sources** | Academic references, standards, or industry practices |

---

## 1. Y-Statement Rendering Capability — `adr.y_statement`

| Attribute | Value |
|---|---|
| **Process location** | Authoring guidance in `.skills/adr-author/SKILL.md`; rendered output via `render-adr.py` |
| **Schema field** | `adr.y_statement` — schema-optional; validator-enforced as mandatory when `status: accepted` |

### What It Does

The Y-Statement is a single structured sentence that captures the entire architectural decision — context, choice, rejected alternatives, benefits, and tradeoffs — in a self-contained format suitable for indexes, dashboards, and quick reference.

### Academic Lineage

The Y-Statement was introduced by Olaf Zimmermann at SATURN 2012, building on George Fairbanks' Architecture Haiku concept (WICSA 2011):

| # | Part | Maps to Schema Field | Purpose |
|---|---|---|---|
| 1 | "In the context of..." | `context.description` | Sets the decision scope |
| 2 | "facing..." | `context.business_drivers` + `context.technical_drivers` | Identifies the quality concern |
| 3 | "we decided for..." | `decision.chosen_alternative` | States the outcome |
| 4 | "and neglected..." | `alternatives[].name` (where not chosen) | Records what was considered |
| 5 | "to achieve..." | `consequences.positive` | Explains expected benefit |
| 6 | "accepting that..." | `decision.tradeoffs` or `consequences.negative` | Captures acknowledged cost |
| 7 | "because..." | `decision.rationale` | Provides the reasoning (long form) |

### Comparative Analysis

| Format | Standalone? | Includes Rejected? | Includes Tradeoffs? | Best For |
|---|:---:|:---:|:---:|---|
| **Y-Statement (long)** | ✅ | ✅ | ✅ | Indexes, chat, dashboards, full summary |
| MADR Decision Outcome | ❌ | ❌ | ❌ | Within full MADR documents |
| Nygard Decision section | ❌ | ❌ | ❌ | Within full Nygard ADRs |
| Architecture Haiku | ✅ | ✅ | ✅ | Architecture overview (1 page) |

**Conclusion:** The Y-Statement is the most information-dense standalone decision summary format available.

### Design Decisions

1. **Static field, not dynamic generation.** The constituent schema fields are multi-paragraph Markdown with Mermaid diagrams. Assembling a Y-Statement from these is a *summarization* task requiring authorial judgment, not a mechanical concatenation. Since accepted ADRs are immutable, there is no drift/maintenance burden.

2. **Long form only.** We use the "because" extension. The short form omits the rationale — the most important part of any decision record. The "because" clause maps to `decision.rationale`, the core "why."

3. **Replaced `adr.summary`.** The Y-Statement is a strictly more informative summary than a free-text elevator pitch. No established template uses both. The `adr.summary` field was removed to eliminate DRY violation.

### Sources

| Source | Year | Contribution |
|---|---|---|
| Zimmermann, Y-Statements (SATURN 2012) | 2012 | Canonical six-part template, "because" extension |
| Fairbanks, Architecture Haiku (WICSA 2011) | 2011 | Tradeoff structure ("to achieve / accepting that") |
| Zimmermann, AD Making Of (ozimmer.ch) | 2020 | Short/medium/long-form verbosity guidance |
| DPR Y-Statement Template (GitHub) | 2022 | Canonical template, examples, tool support |
| MADR 4.0.0 (adr.github.io) | Ongoing | Decision Outcome comparison — lacks standalone self-containment |
| Equal Experts, AI-assisted ADR | 2024 | LLM-generated summaries from structured input — validates approach |

---

## 2. Definition of Done — ecADR Checklist (`§3.3.1`)

| Attribute | Value |
|---|---|
| **Process location** | `adr-process.md` §3.3.1 — gates the `proposed` → `accepted` transition |

### What It Does

A 10-item checklist adapted from Zimmermann's **ecADR** framework. Maps five criteria — **E**vidence, **C**riteria, **A**greement, **D**ocumentation, **R**ealization/Review — to our schema fields and review process. Distinguishes "hard" (schema/CI enforced) and "soft" (reviewer/AI enforced) criteria.

### Academic Lineage: Zimmermann's ecADR Framework

Zimmermann's blog post [*"A Definition of Done for Architectural Decision Making"*](https://ozimmer.ch/practices/2020/05/22/ADDefinitionOfDone.html) (2020) proposes five criteria for when an AD can be considered "DONE-done":

| # | Criterion | Zimmermann's Definition | What It Asks |
|---|-----------|------------------------|-------------|
| **E** | **Evidence** | Design satisfies measurable quality requirements, doesn't break previous ADs, is actionable. | *"Are we confident this design will work?"* |
| **C** | **Criteria** | ≥ 2 alternatives compared by stakeholder concerns. One chosen, others rejected. | *"Have we compared options systematically?"* |
| **A** | **Agreement** | Peer/mentor/team have challenged the AD and agree with outcome. | *"Have we discussed and reached consensus?"* |
| **D** | **Documentation** | Decision captured in lean template and shared with affected parties. | *"Have we captured and shared the decision?"* |
| **R** | **Realization/Review** | Implementation scheduled. Review/retrospective planned. | *"Do we know when to realize and review this?"* |

**Key insight:** Zimmermann warns: *"It is not cost-effective to establish and evaluate 20+ criteria for 5+ alternatives per AD thoroughly."* The DoD must be proportional to decision significance.

### Coverage Analysis: ecADR vs. Our Framework

| ecADR | Sub-criterion | Our Coverage | Mechanism |
|:-----:|---|:---:|---|
| **E** | Design satisfies quality requirements | ⚠️ Soft | `architecturally_significant_requirements` optional; measures in prose |
| **E** | Doesn't break previous ADs | ⚠️ Soft | `review-adr.py` cross-reference prompt; manual review |
| **E** | Actionable/implementable | ⚠️ Soft | Implicit in `alternatives[].estimated_cost` |
| **C** | ≥ 2 alternatives considered | ✅ Hard | Schema `minItems: 2` on `alternatives` |
| **C** | Pros/cons per alternative | ✅ Hard | Schema `required: [pros, cons]` per alternative |
| **C** | One chosen, others compared | ✅ Hard | Schema `required: [chosen_alternative, rationale]` |
| **C** | Rejection rationale for unchosen | ⚠️ Soft | `alternatives[].rejection_rationale` is optional |
| **A** | Peer review occurred | ✅ Hard | PR-based workflow; `reviewers` field |
| **A** | Team agrees with outcome | ✅ Hard | PR approval via `approvals[].identity` |
| **A** | Review proportional to reach | ⚠️ Soft | Escalation guidance in §3.3 |
| **D** | Decision captured in template | ✅ Hard | Schema-valid YAML |
| **D** | Rationale references evidence | ⚠️ Soft | `decision.rationale` required but quality unchecked |
| **D** | Shared with affected parties | ✅ Hard | Git merge; PR notifications |
| **R** | Implementation scheduled | ⚠️ Soft | `confirmation.description` required but not artifact IDs |
| **R** | Review/retrospective planned | ✅ Soft | `lifecycle.review_cycle_months` optional but prompted |

**Summary:** 8/15 sub-criteria fully satisfied through schema or CI. 7 are "soft gaps" — the framework supports but doesn't require them. A documented DoD checklist makes these expectations explicit.

### Design Decisions

1. **Placed at §3.3.1** (end of Review Phase, before Approval). Parallel to DoR at §3.1.1 (end of Draft Phase, before Proposal).

2. **10-item checklist, not 5.** Zimmermann's 5 high-level criteria were decomposed into 10 actionable questions to make them directly checkable.

3. **Hard vs. soft distinction.** Rather than making all 10 mandatory in schema, we document which are schema-enforced and which require human judgment. This avoids over-engineering the schema while still providing clear expectations.

4. **Proportionality principle.** The DoD explicitly states that not all 10 items must be fully satisfied for every ADR — low-priority operational decisions require less rigor than high-priority strategic ones. This prevents the checklist from becoming a bureaucratic burden.

5. **AI review integration.** Added Section 7 to `review-adr.py`'s prompt, checking the 5 ecADR criteria during AI-assisted review.

### What Other Templates Do

No ADR template in our survey includes a formal Definition of Done. Most templates are document formats, not process frameworks. The closest equivalents: MADR 4.0 has a `Confirmation` section (partial R-criterion), arc42 has quality target/actual comparison (partial E-criterion).

### Sources

| Source | Year | Contribution |
|---|---|---|
| Zimmermann, ecADR blog (ozimmer.ch) | 2020 | Five-criteria DoD framework |
| Zimmermann, ecADR (Medium) | 2020 | Expanded examples and proportionality warning |
| DPR `DPR-ArchitecturalDecisionCapturing.md` | 2022 | ecADR reference (line 71), quality properties (line 73) |
| DPR `DPR-ArchitecturalDecisionRecordYForm.md` | 2022 | DoD blog link (line 89) |

---

## 3. Architectural Significance Test (`§3.0`)

| Attribute | Value |
|---|---|
| **Process location** | `adr-process.md` §3.0 "Should You Write an ADR?" |

### What It Does

An 8-criteria checklist that helps teams determine whether a decision is architecturally significant enough to warrant a formal ADR. If the answer to any criterion is "yes," the decision likely deserves an ADR.

### Academic Lineage: Zimmermann's Seven Criteria

Zimmermann's [*"Architectural Significance Criteria and Some Core Decisions Required"*](https://ozimmer.ch/practices/2020/09/24/ASRTestECSADecisions.html) (2020) proposes seven criteria:

| # | Zimmermann's Criterion | Nature |
|---|------------------------|--------|
| 1 | Directly associated with **high business value/risk** | Objective |
| 2 | Concern of a **particularly important stakeholder** | Objective |
| 3 | Involves **runtime QoS** deviating substantially from current architecture | Objective |
| 4 | Creates/deals with **external dependencies** (uncontrollable/unpredictable) | Objective |
| 5 | Involves **design-time QoS** concerns (maintainability, portability, extensibility) | Objective |
| 6 | **First of a kind** (FOAK) — hasn't been done before on this project | Subjective |
| 7 | **Bad past experience** — team got burned with a similar decision before | Subjective |

### Coverage Analysis

Our §3.0 originally had 6 criteria. Analysis against Zimmermann's 7 revealed:

| Zimmermann # | Our Coverage | Assessment |
|:---:|:---:|---|
| 1 | ⚠️ Missing | **Added as #7** — business value/risk is textbook ADR material |
| 2 | ✅ Our #3 | "Concern of important stakeholder" = "contentious or politically sensitive" |
| 3 | ✅ Our #5 | "Runtime QoS deviation" = "affects quality attributes" |
| 4 | ⚠️ Missing | **Added as #8** — external dependencies (vendor lock-in, uncontrollable APIs) |
| 5 | ✅ Our #6 | "Design-time QoS" = "sets a precedent" |
| 6 | ✅ Our #4 | "FOAK" complemented by our "sets a precedent" |
| 7 | ❌ Excluded | Too context-specific for a template checklist |

**Result:** Expanded from 6 to 8 criteria, bringing our test to near-complete alignment with Zimmermann while remaining practical.

### Design Decisions

1. **Criterion #7 excluded.** "Bad past experience" is highly context-specific and doesn't work as a template checklist item. Teams that have been burned will naturally gravitate to ADRs without a checklist telling them to.

2. **Two additions, not wholesale replacement.** Our original 6 criteria were already well-adapted from Zimmermann. Adding business value/risk and external dependencies filled the genuine gaps while preserving our existing language.

3. **Multi-source attribution.** The test draws from three sources — Zimmermann (7 criteria), Richards & Ford (irreversibility heuristic), and Henderson (documentation motivation) — not just Zimmermann alone.

### Sources

| Source | Year | Contribution |
|---|---|---|
| Zimmermann, ASR Test blog (ozimmer.ch) | 2020 | Original 7 criteria |
| Zimmermann, ASR Test (Medium) | 2020 | Expanded examples |
| Richards & Ford, *Fundamentals of Software Architecture* | 2020 | Irreversibility heuristic |
| Henderson, Architecture Decision Record (GitHub) | Ongoing | Documentation motivation, "six months" heuristic |
| DPR `activities/futureWork/DPR-ASRTest.md` | 2022 | Stub linking to blog post |

---

## 4. Definition of Ready — START Checklist (`§3.1.1`)

| Attribute | Value |
|---|---|
| **Process location** | `adr-process.md` §3.1.1 — gates the `draft` → `proposed` transition |

### What It Does

A 5-item checklist adapted from Zimmermann's **START** framework. Maps five preconditions — **S**takeholders, **T**ime (MRM), **A**lternatives, **R**equirements, **T**emplate — to our schema fields and drafting process. Includes Most Responsible Moment (MRM) heuristic questions for timing decisions.

### Academic Lineage: Zimmermann's START Framework

Zimmermann's [*"A Definition of Ready for Architectural Decisions"*](https://medium.com/olzzio/a-definition-of-ready-for-architectural-decisions-ads-2814e399b09b) (2023) proposes five preconditions:

| # | Criterion | Zimmermann's Definition | What It Asks |
|---|-----------|------------------------|-------------|
| **S** | **Stakeholders** | All relevant stakeholders identified and contacted. | *"Do we know who is affected?"* |
| **T** | **Time** | The Most Responsible Moment (MRM) has arrived — not too early, not too late. | *"Is it the right time to decide?"* |
| **A** | **Alternatives** | At least two viable options identified. | *"Do we have genuine options?"* |
| **R** | **Requirements** | Problem context and decision drivers clearly defined. | *"Do we understand the problem?"* |
| **T** | **Template** | An ADR template has been chosen for the project. | *"Do we know how to capture this?"* |

**Key insight:** START is the *input gate* complementing ecADR (the *output gate*). Together: START → (decision-making work) → ecADR.

**The MRM concept** (Most Responsible Moment, from Rebecca Wirfs-Brock) warns against both premature decisions (insufficient data) and delayed decisions (analysis paralysis, technical debt).

### Coverage Analysis: START vs. Our Framework

| START | Our Coverage | Mechanism | Gap? |
|:-----:|:---:|---|:---:|
| **S: Stakeholders** | ✅ | `decision_owner` required; `reviewers`/`approvals` in schema; §3.2 step 7 | None |
| **T: Time (MRM)** | ⚠️ | Not addressed — no guidance on *when* to start | **Yes** |
| **A: Alternatives** | ✅ | Schema `minItems: 2` on `alternatives` | None |
| **R: Requirements** | ✅ | `context.description` required; drivers/constraints prompted | None |
| **T: Template** | ✅ | N/A — our framework *is* the template | None |

**Summary:** 4/5 already satisfied. One genuine gap: **Timing/MRM** — we didn't help teams decide *when* the right moment is.

### Design Decisions

1. **Placed at §3.1.1** (end of Draft Phase). Parallel to DoD at §3.3.1 (end of Review Phase). The lifecycle flow:
   ```
   §3.0    Significance Test     → "Should we write an ADR?"
   §3.1    Draft Phase
     §3.1.1  DoR (START)         → "Is this ready for review?"
   §3.2    Proposal Phase
   §3.3    Review Phase
     §3.3.1  DoD (ecADR)         → "Is this ready to accept?"
   §3.4    Approval Phase
   ```

2. **MRM heuristic questions** added for criterion 2 since timing is inherently context-specific. Four diagnostic questions help authors self-assess:
   - Enough information to compare alternatives?
   - Cost of delaying one more sprint/month?
   - Cost of wrong decision now vs. waiting?
   - Upcoming events creating urgency?

3. **Template criterion (T) → schema validity.** In multi-template environments, template choice is a real precondition. Our framework standardizes on one template, so we repurpose this criterion as "is the ADR schema-valid and substantially complete?"

### Sources

| Source | Year | Contribution |
|---|---|---|
| Zimmermann, DoR for ADs (Medium) | 2023 | START framework |
| Wirfs-Brock, "Agile Architecture Myths #2" | 2011 | Most Responsible Moment (MRM) concept |
| DPR `DPR-ArchitecturalDecisionCapturing.md` | 2022 | DoR blog link (line 131) |

---

## 5. Verbosity Guidance (`§3.0.1`)

| Attribute | Value |
|---|---|
| **Process location** | `adr-process.md` §3.0.1 "How Much Detail?" |

### What It Does

A guidance table mapping `priority` × `decision_level` to expected documentation depth (minimal/medium/full). Includes the "don't over-document" principle from DPR.

### Academic Lineage: DPR's Three Verbosity Levels

DPR explicitly defines three verbosity levels for decision capturing (`activities/DPR-ArchitecturalDecisionCapturing.md`, lines 31–35):

| Level | What to Capture | When Appropriate |
|-------|----------------|-----------------|
| **Minimal** | Decision outcome + "because" rationale | Low-impact, easily reversible, team-internal |
| **Medium** | Lean ADR template (Y-Statement, MADR, Nygard) | Most architectural decisions |
| **Full** | Full-fledged decision model with comprehensive analysis | High-impact, regulatory, cross-org |

DPR's line 70 provides the guiding principle: *"Do not spend more time on capturing than on making."*

### How Our Schema Maps to Verbosity

Our schema's required/optional field structure naturally supports all three levels:

**Required fields (= "medium" baseline):**
`adr` (id, title, status, created_at, version, project, decision_type), `authors`, `decision_owner`, `context` (description), `alternatives` (≥2 with name, description, pros, cons), `decision` (chosen_alternative, rationale), `consequences` (positive ≥1, negative ≥1), `confirmation` (description)

**Optional fields (upgrade to "full"):**
`y_statement`, `priority`, `decision_level`, `tags`, `component`, `business_drivers`, `technical_drivers`, `constraints`, `assumptions`, `architecturally_significant_requirements`, `alternatives[].risk/estimated_cost/rejection_rationale`, `decision.tradeoffs/confidence`, `reviewers`, `dependencies`, `lifecycle`, `audit_trail`, `references`

### Design Decisions

1. **Mapping to existing fields.** Two existing fields drive verbosity expectations:

   | Priority | Decision Level | Verbosity | What to Populate |
   |:--------:|:--------------:|:---------:|-----------------|
   | `low` | `operational` | Minimal | Required fields only. Brief descriptions. |
   | `medium` | `tactical` | Medium | + drivers, constraints, tradeoffs, Y-statement |
   | `high`/`critical` | `strategic` | Full/Full+ | All sections. Mermaid diagrams. Detailed ASRs. |

2. **Independent axes acknowledged.** Priority and decision_level are independent — a `high` priority `operational` decision needs full technical analysis but not full governance ceremony. The table shows the typical diagonal, not a hard rule.

3. **Explicit anti-pattern warning.** AI-assisted authoring makes it easy to generate voluminous but shallow content. The guidance explicitly warns: "One well-reasoned paragraph in `rationale` beats five paragraphs of filler."

4. **Placed at §3.0.1** (after "Should You Write an ADR?", before "Draft Phase"). This calibrates effort *before* the author starts writing.

### Sources

| Source | Year | Contribution |
|---|---|---|
| DPR `DPR-ArchitecturalDecisionCapturing.md` | 2022 | Three verbosity levels (lines 31–35) |
| DPR (same file) | 2022 | "Don't over-document" (line 70) |
| DPR (same file) | 2022 | "Stick to one template" (line 67) |
| Zimmermann, ecADR blog | 2020 | "Not cost-effective to establish 20+ criteria for 5+ alternatives" |

---

> **Note:** Schema-level features that were evaluated and rejected (QAS `measure` field, `scope`/`phase` metadata, NFR Landing Zones) are documented inline in [`schema-field-rationale.md`](schema-field-rationale.md) alongside the adopted fields they relate to (§1.12, §4.2, §4.3).
