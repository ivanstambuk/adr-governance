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

#### Zimmermann's Y-Statement (SATURN 2012)

The Y-Statement was introduced by Olaf Zimmermann at SATURN 2012. The canonical structure maps directly to our schema fields:

| # | Part | Maps to Schema Field | Purpose |
|---|---|---|---|
| 1 | "In the context of..." | `context.description` | Sets the decision scope |
| 2 | "facing..." | `context.business_drivers` + `context.technical_drivers` | Identifies the quality concern |
| 3 | "we decided for..." | `decision.chosen_alternative` | States the outcome |
| 4 | "and neglected..." | `alternatives[].name` (where not chosen) | Records what was considered |
| 5 | "to achieve..." | `consequences.positive` | Explains expected benefit |
| 6 | "accepting that..." | `decision.tradeoffs` or `consequences.negative` | Captures acknowledged cost |
| 7 | "because..." | `decision.rationale` | Provides the reasoning (long form) |

Zimmermann distinguishes three verbosity levels for Y-Statements:
- **Short form** (parts 1–4): Context + decision + rejected. Suitable for indexes.
- **Medium form** (parts 1–6): Adds consequences. Suitable for most uses.
- **Long form** (parts 1–7): Adds the "because" rationale. Our chosen format.

Zimmermann's practical advice: *"A convincing justification is key. The more evidence you can provide for your choice (...), the stronger your justification will be."*

#### Fairbanks' Architecture Haiku (WICSA 2011)

George Fairbanks introduced the **Architecture Haiku** — a one-page summary of an architecture's key decisions, constraints, and quality attribute tradeoffs. The Haiku's structure directly influenced the Y-Statement's tradeoff parts:

| Haiku Element | Y-Statement Mapping |
|---|---|
| "This system must..." (quality goals) | "to achieve..." (part 5) |
| "but we accept..." (tradeoffs) | "accepting that..." (part 6) |
| "because..." (rationale) | "because..." (part 7) |

The key insight: Fairbanks recognized that architecture is fundamentally about **tradeoffs**, not just choices. The Y-Statement inherits this by *requiring* the author to name what they're giving up — not just what they gain. This is the most important difference from MADR's Decision Outcome format, which captures only the positive.

#### MADR 4.0 — Decision Outcome (Comparison)

MADR's closest equivalent to the Y-Statement is the **"Decision Outcome"** section:

> *"Chosen option: '{title of option 1}', because {justification}."*

| Dimension | MADR Decision Outcome | Y-Statement (long) |
|---|---|---|
| **Standalone?** | ❌ Requires reading full MADR for context | ✅ Fully self-contained |
| **Includes rejected alternatives?** | ❌ Only names the chosen option | ✅ "and neglected [alternatives]" |
| **Includes tradeoffs?** | ❌ Only mentions positive justification | ✅ "accepting that [tradeoffs]" |
| **Includes context?** | ❌ Assumed from document heading | ✅ "In the context of [scope]" |
| **Machine-generable?** | ⚠️ Partially — just option + because | ✅ All 7 parts map to schema fields |

**Assessment:** MADR's Decision Outcome is a sentence fragment. The Y-Statement is a self-contained paragraph. For AI-generated summaries, chat messages, or decision indexes, the Y-Statement is strictly more informative.

#### Nygard Format — Decision Section (Comparison)

Michael Nygard's original ADR format (2011) uses three sections: **Context**, **Decision**, **Consequences**.

> *"We will use [technology/pattern]..."*

The Decision section is free-form prose that describes the choice but doesn't follow a structured template. It typically omits rejected alternatives and doesn't explicitly surface tradeoffs. It also lacks the "in the context of" framing — readers must infer context from the Context section above.

**Assessment:** Nygard's format works well as a full document but produces no extractable single-sentence summary. The Y-Statement provides exactly the missing "elevator pitch" layer.

#### Tyree-Akerman Template — Decision Field (Comparison)

The IEEE Software template (Tyree & Akerman, 2005) includes:

> *"The architecture decision made, with justification."*

This is the closest enterprise template to a structured decision summary. Its strength is thorough cross-referencing (Related Decisions, Related Requirements), but it has no single-sentence summary equivalent to the Y-Statement. Its comprehensiveness makes it ill-suited for quick communication — exactly the gap the Y-Statement fills.

#### Emerging Pattern: AI-Generated Decision Summaries

Recent industry practice (2024–2026) shows growing use of LLMs for:
- **Generating Y-Statements from structured ADR data** — exactly what our framework supports
- **Producing audience-adapted summaries** — same decision, different phrasing for executives vs. engineers
- **Quality-checking Y-Statements** — verifying the summary accurately reflects the full ADR content

Equal Experts' ADR approach and research (arxiv.org, "LLMs for Software Architecture") demonstrate that LLMs can produce Y-Statements that are "relevant and accurate" when given structured input, though they may "fall short of human-level performance" for the justification clause.

> **Key insight:** Our structured YAML schema provides *exactly* the kind of clean, well-separated input that LLMs need to generate accurate Y-Statements. The six constituent fields map directly to the six Y-Statement parts with no ambiguity.

### Comparative Analysis

| Format | Length | Standalone? | Includes Rejected? | Includes Tradeoffs? | Machine-Generable? | Best For |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Y-Statement (long)** | 1–2 sentences | ✅ | ✅ | ✅ | ✅ | Indexes, chat, dashboards, full summary |
| **Y-Statement (short)** | 1 sentence | ✅ | ✅ | ❌ | ✅ | Quick indexes, log entries |
| MADR Decision Outcome | 1 sentence | ❌ | ❌ | ❌ | ⚠️ | Within full MADR documents |
| Nygard Decision section | Free-text paragraph | ❌ | ❌ | ❌ | ⚠️ | Within full Nygard ADRs |
| Tyree-Akerman Decision | 1–2 sentences + justification | ❌ | ❌ | ❌ | ⚠️ | Enterprise governance |
| Architecture Haiku | 1 page | ✅ | ✅ | ✅ | ❌ | Architecture overview |

**Conclusion:** The Y-Statement is the **most information-dense** standalone decision summary format available. No other format packs context, decision, rejected alternatives, benefits, and tradeoffs into a single sentence.

### Design Decisions

1. **Static field, not dynamic generation.** The constituent schema fields (`context.description`, `consequences.positive`, `decision.tradeoffs`, etc.) are **multi-paragraph Markdown** — often containing Mermaid diagrams, bullet lists, and detailed prose. Assembling a Y-Statement from these is a *summarization* task, not a *concatenation* task. A deterministic script cannot distill 5 paragraphs of context into the "In the context of..." clause — that requires authorial judgment (human or AI-assisted).

   | Approach | Assessment | Status |
   |---|---|---|
   | **Schema field** (authored once at acceptance) | Static, curated distillation | ✅ Adopted |
   | **Render script** (template assembly from fields) | Can't summarize multi-paragraph fields | ❌ Rejected |
   | **AI Bundle** (generate on-the-fly from context) | Non-deterministic, hallucination risk | ❌ Rejected |

   **Why the DRY objection was wrong:** The DRY argument assumed the Y-Statement is a mechanical derivation. It isn't — it's a *curated distillation*, like any summary. Since accepted ADRs are immutable (status changes require supersession), there is no drift/maintenance burden.

2. **Long form only.** We use the "because" extension. The short form omits the rationale — the most important part of any decision record. The "because" clause maps to `decision.rationale`, the core "why." Since the Y-Statement is a static field (not dynamically generated), the extra clause adds critical context that makes the statement self-contained.

3. **Replaced `adr.summary`.** The Y-Statement is a strictly more informative summary than a free-text elevator pitch. No established ADR template (MADR, Nygard, Tyree/Akerman, DPR) uses both a summary and a Y-Statement. Zimmermann explicitly positions the Y-Statement as a self-contained summary. The `adr.summary` field was removed to eliminate DRY violation.

### Example Y-Statement

For ADR-0001 (DPoP over mTLS):

> *In the context of the OIDC-based IAM platform, facing the need for sender-constrained tokens across public (mobile), confidential (backend), and partner clients, we decided for DPoP (RFC 9449) and against mTLS (RFC 8705) and a hybrid approach, to achieve unified sender-constraining without CDN/proxy infrastructure changes, accepting per-request proof generation overhead (~500 bytes) and client-side implementation complexity, because DPoP is the only mechanism that works for all three client types without infrastructure modifications, survives CDN TLS termination (eliminating a $50K/year Cloudflare add-on), and provides a single validation path that reduces operational complexity.*

### DPR Source Files

| File | Relevant Content |
|------|-----------------|
| `artifact-templates/DPR-ArchitecturalDecisionRecordYForm.md` | Full Y-Statement template, examples, and Wikipedia citation |
| `activities/DPR-ArchitecturalDecisionCapturing.md` | Y-Statement as a "medium verbosity" option (line 34) |

### Sources

| Source | Year | Contribution |
|---|---|---|
| Zimmermann, Y-Statements (SATURN 2012) | 2012 | Canonical six-part template, "because" extension, practical pitfalls |
| Fairbanks, Architecture Haiku (WICSA 2011) | 2011 | Intellectual ancestor — the "to achieve / accepting that" tradeoff structure |
| Zimmermann, Y-Statements (Medium blog) | 2020 | Expanded examples, known uses, advice on convincing justifications |
| Zimmermann, AD Making Of (ozimmer.ch) | 2020 | Historical context, short/medium/long-form verbosity guidance |
| DPR Y-Statement Template (GitHub) | 2022 | Canonical template structure, Wikipedia example, tool support |
| MADR 4.0.0 (adr.github.io) | Ongoing | Decision Outcome comparison — lacks standalone self-containment |
| Nygard, "Documenting Architecture Decisions" | 2011 | Original ADR format — Context/Decision/Consequences mapping |
| Tyree & Akerman, IEEE Software | 2005 | Comprehensive template — no single-sentence summary equivalent |
| Equal Experts, AI-assisted ADR | 2024 | LLM-generated summaries from structured input — validates approach |
| Arxiv, "LLMs for Software Architecture" | 2024 | GPT-4 can generate "relevant and accurate" decisions from structured contexts |

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

### Rejected Alternatives

- *Formal CI gate instead of a checklist.* Considered making all 10 DoD criteria hard CI checks (schema-enforced or script-checked) that gate the `proposed` → `accepted` transition. Rejected because 7 of the 15 sub-criteria (§2 coverage analysis) require human judgment — "does the rationale reference specific evidence?" and "is the review proportional to reach?" cannot be automated without AI review, which would introduce non-determinism into the CI pipeline. The hybrid hard/soft model gives CI what it can check and leaves judgment to reviewers.

- *Lighter 5-item checklist (Zimmermann's original ecADR).* Considered using Zimmermann's five high-level criteria (E, C, A, D, R) directly as the DoD. Rejected because each criterion contains 2–4 sub-criteria that are independently checkable — e.g., the E-criterion covers quality requirements satisfaction, consistency with previous ADs, *and* actionability. A 5-item checklist at the meta-level is too abstract for reviewers to action; the decomposed 10-item version maps each check to a specific schema field or review activity.

- *Scoring matrix (weighted criteria).* Considered a weighted scoring system where each DoD criterion has a numeric weight and the ADR must exceed a threshold score. Rejected because: (a) weight assignment is arbitrary and creates false precision, (b) a "good enough" total score could mask critical failures in individual criteria (e.g., scoring 9/10 overall but failing the "alternatives compared" criterion), and (c) binary pass/fail per criterion is clearer for reviewers.

- *Per-priority DoD variants.* Considered separate DoD checklists for low/medium/high priority ADRs (e.g., operational decisions get 5 items, strategic get all 10). Rejected in favor of the proportionality principle stated in Design Decision #4 — it's simpler to have one checklist with explicit guidance that not all items need full satisfaction for every priority level, than to maintain multiple checklist variants that would inevitably drift.

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

### Rejected Alternatives

- *Scoring matrix instead of yes/no checklist.* Considered assigning weights to each criterion and requiring a threshold score (e.g., "if total weight ≥ 5, write an ADR"). Rejected because: (a) weight assignment is inherently arbitrary — is "high business value" worth 3 points or 5? (b) a single "yes" to criterion #1 ("affects multiple components, teams, or services") is independently sufficient to warrant an ADR, regardless of what other criteria score. The yes/no model correctly captures this: any single "yes" triggers the recommendation.

- *Decision tree instead of flat checklist.* Considered a branching flowchart: "Is it irreversible? → Yes → Write ADR. No → Does it cross team boundaries? → Yes → Write ADR. No → ..." Rejected because: (a) the ordering of criteria in a decision tree implies a priority hierarchy that doesn't exist — all 8 criteria are independently sufficient, (b) flowcharts are harder to maintain in Markdown documentation, and (c) a flat checklist is faster to scan during the "should I write an ADR?" moment.

- *Mandatory scoring with team calibration.* Considered requiring teams to calibrate the test against their first 10 ADRs ("did the test correctly identify which decisions needed ADRs?") with a formal calibration session. Rejected as over-engineering for a lightweight gate — the test is a heuristic aid, not a formal classification system. Teams will naturally calibrate through experience.

- *No significance test (write ADRs for everything).* Some teams advocate recording all decisions, not just architecturally significant ones. Zimmermann explicitly warns against this: "An AD log with more than 100 entries will probably put your readers (and you) to sleep." The significance test prevents ADR inflation and preserves the signal-to-noise ratio of the decision log.

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

### Rejected Alternatives

- *Skip DoR entirely and let schema enforce completeness.* Considered relying solely on JSON Schema validation (`required` fields, `minItems` constraints) as the implicit DoR — if the YAML validates, it's ready for review. Rejected because schema validation checks *structural* completeness, not *semantic* readiness. A schema-valid ADR can have a `context.description` that says "TODO: fill in context" — it passes `minLength: 20` but isn't ready for review. The DoR checklist adds semantic checks that schema cannot enforce: "are stakeholders identified?" and "is now the right time to decide?"

- *Automated DoR via CI script.* Considered writing a pre-PR script that checks all 5 START criteria automatically. Rejected because 2 of 5 criteria are inherently subjective: **T** (MRM — "is it the right time?") and **S** ("have affected stakeholders been *notified*?"). These require human judgment. The remaining 3 (Alternatives, Requirements, Template/schema) are already schema-enforced, making a dedicated DoR script redundant for the automatable portion.

- *More granular DoR (10+ items, matching DoD granularity).* Considered decomposing START into 10+ sub-criteria to mirror the DoD's granularity. Rejected because the DoR gates the draft → proposed transition (lower stakes than proposed → accepted), and Zimmermann's START is already comprehensive at 5 items. Over-granularity at the drafting stage creates friction that discourages ADR authoring — the opposite of the framework's goal.

- *Combined DoR/DoD as a single checklist.* Considered merging START and ecADR into one comprehensive checklist applied at a single gate (before acceptance). Rejected because the two checklists serve different lifecycle moments: DoR asks "should we start reviewing this?" and DoD asks "should we accept this?" Combining them would force authors to satisfy output-quality criteria ("does the rationale reference evidence?") before the review process has even begun — which is where that evidence typically surfaces.

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

### Rejected Alternatives

- *Schema-level enforcement (conditional required fields by priority).* Considered using JSON Schema `if/then` blocks to make additional fields required based on `adr.priority` — e.g., `priority: high` → `architecturally_significant_requirements` becomes required; `priority: low` → only core fields required. Rejected for three reasons: (a) JSON Schema 2020-12 conditional logic becomes exponentially complex with multiple trigger fields (`priority` × `decision_level` = 12 combinations), (b) it conflates "recommended" with "required" — a high-priority ADR *should* have ASRs but may have legitimate reasons not to, and (c) it removes authorial discretion, turning a guidance tool into a bureaucratic enforcement mechanism.

- *Separate lightweight template for low-priority decisions.* Considered maintaining two YAML templates: a full template and a "lite" template with fewer fields. Rejected because: (a) two templates double the maintenance burden (schema changes must be applied to both), (b) upgrading a decision from "lite" to "full" requires migrating between templates, and (c) DPR explicitly advises "stick to one template" (line 67) — multiple templates create confusion about which to use.

- *Automated verbosity scoring.* Considered a CI script that calculates a "verbosity score" based on field population and description lengths, then warns if the score is disproportionate to the priority/level. Rejected because verbosity is qualitative, not quantitative — a 200-word rationale may be more thorough than a 500-word rationale if it's well-reasoned vs. padded. Automated scoring would incentivize length over quality.

- *No verbosity guidance (let authors decide).* Considered omitting verbosity guidance entirely, trusting authors to calibrate naturally. Rejected because: (a) without guidance, the AI-assisted authoring workflow tends to maximize verbosity (LLMs generate more content when unconstrained), and (b) new framework adopters benefit from explicit expectations before writing their first ADR. Zimmermann's warning — "do not spend more time on capturing than on making" — deserves prominent placement.

### Sources

| Source | Year | Contribution |
|---|---|---|
| DPR `DPR-ArchitecturalDecisionCapturing.md` | 2022 | Three verbosity levels (lines 31–35) |
| DPR (same file) | 2022 | "Don't over-document" (line 70) |
| DPR (same file) | 2022 | "Stick to one template" (line 67) |
| Zimmermann, ecADR blog | 2020 | "Not cost-effective to establish 20+ criteria for 5+ alternatives" |

---

> **Note:** Schema-level features that were evaluated and rejected (QAS `measure` field, `scope`/`phase` metadata, NFR Landing Zones) are documented inline in [`schema-field-rationale.md`](schema-field-rationale.md) alongside the adopted fields they relate to (§1.12, §4.2, §4.3).
