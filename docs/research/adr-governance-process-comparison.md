# ADR Governance Process Comparison Research

> **Date:** 2026-03-05
> **Author:** Ivan Stambuk
> **Status:** Final — HISTORICAL REFERENCE
> **Repository:** `adr-governance`

> ⚠️ **This document was created during the initial process design phase and may reference features that were subsequently adopted or modified (e.g., `draft` status was adopted). Refer to the current [`docs/adr-process.md`](../adr-process.md) as the source of truth.**

---

## 1. Purpose

This document surveys and compares the major **ADR governance processes** — the workflows, state machines, review protocols, and lifecycle models that govern how ADRs move from idea to accepted decision and beyond. This is distinct from the [template comparison](adr-template-comparison.md), which covers what goes *inside* an ADR.

The goal is to:

1. Catalogue the **state machines** and **status values** used by different process models
2. Compare **review and approval workflows** across organizations
3. Identify **immutability vs. living document** philosophies
4. Evaluate the **enforcement mechanisms** used in practice
5. Provide a **synthesis** with recommendations for our `adr-governance` schema and process

---

## 2. Processes Surveyed

| # | Process | Origin | Year | Scope | Primary Source |
|---|---------|--------|------|-------|----------------|
| 1 | **Nygard (Original)** | Michael Nygard | 2011 | Team-level | [cognitect.com](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions) |
| 2 | **AWS Prescriptive Guidance** | Darius Kunce & Dominik Goby, AWS | 2022 | Project/product teams | [docs.aws.amazon.com](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/welcome.html) |
| 3 | **ThoughtWorks Architecture Advice Process** | ThoughtWorks | ~2019 | Organization-wide | [thoughtworks.com](https://www.thoughtworks.com/en-gb/insights/articles/scaling-architecture-conversationally) |
| 4 | **Spotify RFC → ADR** | Spotify Engineering | 2020 | Squad/tribe | [engineering.atspotify.com](https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record/) |
| 5 | **UK GOV.UK Framework** | UK Cabinet Office / GDS | 2023 | Cross-departmental government | [gov.uk](https://www.gov.uk/guidance/architectural-decision-records) |
| 6 | **EIP/Decentraland Standards Track** | Decentraland / Ethereum | 2021 | Open-source community | [adr.decentraland.org](https://adr.decentraland.org) |

---

## 3. Process-by-Process Analysis

### 3.1 Nygard (2011) — The Original Process

The simplest possible lifecycle. No governance ceremony at all.

**State Machine:**

```
                ┌──────────┐
                │ proposed │
                └────┬─────┘
                     │ team agrees
                     ▼
                ┌──────────┐
                │ accepted │ ◄─── immutable from this point
                └────┬─────┘
                     │ new ADR supersedes
                     ▼
              ┌─────────────┐
              │ superseded  │
              └─────────────┘
```

**States:** `proposed` → `accepted` → `deprecated` / `superseded`

**Review Process:** None defined. The blog post says _"any team member can propose an ADR"_ but doesn't prescribe how review happens.

**Immutability:** ✅ Strict. _"If a decision is reversed, we keep the old one around, but mark it as superseded."_ ADRs are an append-only log.

**Enforcement:** None. The process relies on team discipline and culture.

**Key Principle:** _"We will keep a collection of records for architecturally significant decisions."_ — simplicity above all.

---

### 3.2 AWS Prescriptive Guidance (2022)

The most formally documented ADR process from a major cloud vendor. Defines three sub-processes: adoption, validation (code review), and update (supersession).

**State Machine:**

```
   Architecture decision
        identified
            │
            ▼
   Owner of ADR draft
        identified
            │
            ▼
   ┌────────────────┐
   │    Proposed    │◄───────────────────────────────────────┐
   └───────┬────────┘                                        │
           │                                                 │
           ▼                                                 │
   Owner organizes                                           │
   team review meeting                                       │
           │                                                 │
           ▼                                                 │
    ┌──────────────┐     No    ┌──────────────┐     No   Team identifies
    │  Accepted by ├──────────►│  Rejected by ├─────────►action points
    │   the team?  │           │   the team?  │          to improve ADR
    └──────┬───────┘           └──────┬───────┘              │
           │ Yes                      │ Yes                  │
           ▼                          ▼                      │
   ┌──────────────┐          Owner updates ADR               │
   │   Accepted   │          with rejection reason           │
   └──────────────┘                   │                      │
                                      ▼                      │
                              ┌──────────────┐               │
                              │   Rejected   │               │
                              └──────────────┘               │
```

**States:** `proposed` → `accepted` | `rejected`; `accepted` → `superseded`

**Review Process:**
1. Owner creates ADR in `Proposed` state
2. Owner organizes a **team review meeting**
3. Meeting starts with a **dedicated reading slot** (10–15 min)
4. Each team member reads the document and **adds comments**
5. Owner reads out and discusses each comment
6. **Three outcomes:**
   - **Accept** → owner adds timestamp, version, stakeholder list; status → `Accepted`
   - **Rework** → team identifies action points, assigns them; status stays `Proposed`; owner reschedules review
   - **Reject** → owner adds rejection reason; status → `Rejected`
7. Accepted ADRs are **immutable** — changes require a new ADR that supersedes the old one

**Validation Sub-Process (Code Review):**

AWS defines a second process where ADRs are applied during code reviews:
1. Code change goes through peer review
2. Reviewer checks if the change **violates any accepted ADRs**
3. If it does → reviewer links the ADR and asks author to update the code
4. Updated code is approved and merged

**Update Sub-Process (Supersession):**

1. New insights require a different decision
2. Team creates a **new ADR**
3. New ADR goes through the full review process
4. If accepted → old ADR status changes to `Superseded`

**Ownership Model:** Each ADR has a single **owner** who is responsible for maintaining and communicating the ADR. Other team members can contribute, but the owner approves changes before acceptance.

**Anti-Patterns Identified:**
1. No decision is made at all (fear of wrong choice)
2. Decision is made without justification (repeated discussions)
3. Decision isn't captured in a repository (forgotten)

**Key Principle:** _"ADRs align current and future team members. They set a strategic direction. They avoid decision anti-patterns."_

---

### 3.3 ThoughtWorks Architecture Advice Process (~2019)

A **decentralized** governance model where anyone can make an architectural decision, provided they follow the Advice Process. No central approval board.

**State Machine:**

```
   ┌──────────────────┐
   │  Need identified │
   └───────┬──────────┘
           │
           ▼
   ┌───────────────────────────┐
   │  Seek advice from:        │
   │  • Those affected         │
   │  • Those with expertise   │
   └───────┬───────────────────┘
           │
           ▼
   ┌───────────────────┐
   │  Architecture     │  (recurring, advisory)
   │  Advisory Forum   │
   └───────┬───────────┘
           │ discussed
           ▼
   ┌──────────────┐
   │   Proposed   │
   └──────┬───────┘
          │ decision-maker decides
          ▼
   ┌──────────────┐
   │   Accepted   │
   └──────────────┘
```

**States:** Informal — the process focuses on the *advice-seeking* phase rather than formal states.

**Review Process:**
1. **Anyone** can make an architectural decision
2. Before deciding, they **must seek advice** from:
   - People who will be **affected** by the decision
   - People with **relevant expertise**
3. The decision-maker is **not obligated to follow** the advice, but must acknowledge it
4. The **Architecture Advisory Forum (AAF)** provides a regular venue for discussions
5. The AAF is **advisory only** — it is not a decision-making body
6. ADRs are stored in source control alongside the code

**Enforcement:**
- **Cultural** — relies on trust and social norms
- The AAF provides **visibility** but not veto power
- ThoughtWorks' **Technology Radar** serves as a lightweight governance mechanism for technology choices

**Key Principle:** _"Balance team autonomy with architectural quality."_ The Advice Process is not a committee or approval gate — it's a social protocol.

---

### 3.4 Spotify RFC → ADR (2020)

A **two-stage** process where major decisions go through an RFC (Request for Comments) phase before being captured as an ADR.

**Decision Flow:**

```
   Do I have a problem?
        │ Yes
        ▼
   Is there a blessed solution?
        │ No
        ▼
   Do I have a solution?
        │ Yes
        ▼
   Is it a big change?
        │ Yes                              │ No
        ▼                                  ▼
   Write an RFC                   Write an ADR directly
        │
        │ RFC concludes
        │ with a solution
        ▼
   Write an ADR
```

**States:** Spotify doesn't prescribe formal states. In practice (via Backstage):
- `proposed` → `accepted` → `deprecated` / `superseded`

**Review Process:**
1. For **big changes**: write an RFC first, circulate for async feedback
2. RFCs go through discussions in meetings and comment threads
3. When the RFC **concludes with a solution** → write an ADR
4. For **small decisions with compound impact**: write an ADR directly
5. For **backfilling undocumented decisions**: write an ADR when a gap is discovered during code review
6. ADRs are submitted as **pull requests** (PR process provides review)

**Enforcement:**
- **Decision Guardian** — an open-source GitHub Action that automatically surfaces relevant ADRs during code reviews when protected files are modified
- ADRs are never deleted, only superseded

**Key Principle:** _"ADRs capture the agreed-upon solution after an RFC process has concluded."_ The RFC is for exploration; the ADR is for recording the decision.

---

### 3.5 UK GOV.UK Framework (2023)

A hierarchical, **multi-tier governance** model designed for cross-departmental government architecture.

**State Machine:**

```
   ┌───────────────┐
   │   Drafted     │
   └───────┬───────┘
           │
           ▼
   ┌───────────────────────────────┐
   │  Determine scope & decision   │
   │  level:                       │
   │  • Team/Project Lead          │
   │  • Programme Architecture     │
   │    Forum                      │
   │  • Departmental Architecture  │
   │    Board                      │
   │  • Technical Design Council   │
   │    (cross-departmental)       │
   └───────┬───────────────────────┘
           │
           ▼
   Engage stakeholders
           │
           ▼
   Submit for review & approval
   by appropriate decision-making body
           │
           ▼
   ┌──────────────┐      ┌──────────────┐
   │   Accepted   │      │  Superseded  │
   └──────────────┘      └──────────────┘
```

**States:** `accepted` → `superseded`

**Decision-Making Bodies (tiered):**

| Level | Body | Scope |
|-------|------|-------|
| 1 | **Team / Project Leads** | Decisions local to a single team |
| 2 | **Programme Architecture Forums** | Decisions affecting multiple teams or shared services |
| 3 | **Departmental Architecture Boards** | Decisions impacting multiple programmes or setting precedents |
| 4 | **Technical Design Council (TDC)** | Cross-departmental decisions; includes government CTO, departmental CTOs, chief architect |

**Review Process:**
1. Identify the **scope** of the decision and the appropriate **decision-making level**
2. Engage with relevant **stakeholders**
3. Use a standard ADR template to document the decision
4. Submit the ADR for **review and approval** by the appropriate decision-making body
5. **Share** the approved ADR with all stakeholders
6. **Regularly review and update** the ADR to reflect changes

**Key Principle:** _"Empower teams to make architectural decisions while providing guidance on escalation for broader impacts."_ Balances autonomy with hierarchical accountability.

---

### 3.6 Decentraland Standards Track (2021)

An **open-source community** ADR process inspired by Ethereum's EIP (Ethereum Improvement Proposal) process. Notable for having the most granular state machine.

**State Machine:**

```
   ┌────────┐
   │  Idea  │  (not formally tracked)
   └───┬────┘
       │
       ▼
   ┌────────┐
   │  Draft │  (formally submitted, under development)
   └───┬────┘
       │
       ▼
   ┌─────────┐
   │  Review │  (ready for and undergoing peer review)
   └───┬─────┘
       │
       ▼
   ┌────────────┐
   │  Last Call  │  (final review window before acceptance)
   └───┬────────┘
       │
       ├──────────────┐
       ▼              ▼
   ┌────────┐    ┌────────────┐
   │  Final │    │  Withdrawn │
   └────────┘    └────────────┘
```

**States:** `idea` → `draft` → `review` → `last_call` → `final` | `withdrawn`

This is the **most granular state machine** among all processes surveyed. Notably:
- **`review`** is an explicit state (most processes don't have this)
- **`last_call`** provides a formal final-comment window before acceptance
- **`withdrawn`** replaces "rejected" — author-initiated rather than team-initiated

**Review Process:**
1. Author submits ADR in `Draft` state
2. Community reviews and provides feedback
3. When ready, ADR moves to `Review` state
4. After review period, enters `Last Call` (time-boxed final review)
5. If no blocking issues → `Final` (accepted and immutable)
6. Author can `Withdraw` at any point

---

## 4. Status Values Comparison Matrix

| Status | Nygard | AWS | ThoughtWorks | Spotify | GOV.UK | Decentraland | **adr-governance** |
|--------|:------:|:---:|:------------:|:-------:|:------:|:------------:|:------------------:|
| `idea` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `draft` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| `proposed` | ✅ | ✅ | 🟡 | ✅ | ❌ | ❌ | ✅ |
| `review` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `last_call` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `accepted` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `rejected` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `withdrawn` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `deprecated` | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| `superseded` | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| `deferred` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

**Our schema** currently supports: `draft`, `proposed`, `accepted`, `superseded`, `deprecated`, `rejected`, `deferred`

---

## 5. Process Feature Comparison Matrix

| Feature | Nygard | AWS | ThoughtWorks | Spotify | GOV.UK | Decentraland | **adr-governance** |
|---------|:------:|:---:|:------------:|:-------:|:------:|:------------:|:------------------:|
| **Ownership** | | | | | | | |
| Named ADR owner | ❌ | ✅ | ✅ | 🟡 | ❌ | ✅ | ✅ |
| Decision owner ≠ author | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Review** | | | | | | | |
| Review meeting defined | ❌ | ✅ | 🟡 | ❌ | ❌ | ❌ | 🟡 |
| Reading slot in meeting | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Async review (comments) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| RFC phase before ADR | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Formal last-call window | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Approval** | | | | | | | |
| Team consensus | 🟡 | ✅ | ❌ | 🟡 | ❌ | ❌ | ❌ |
| Advisory (non-binding) | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Tiered approval bodies | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | 🟡 |
| Formal approval signatures | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| PR-based review | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Immutability** | | | | | | | |
| Accepted ADRs immutable | ✅ | ✅ | 🟡 | ✅ | 🟡 | ✅ | ✅ |
| Append-only log principle | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Supersession requires new ADR | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Enforcement** | | | | | | | |
| Code review validation | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Automated enforcement tool | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Technology Radar governance | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Lifecycle** | | | | | | | |
| Periodic review cycle | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Audit trail | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Rejection with reason | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Archival policy | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Scope / Governance** | | | | | | | |
| Team-level only | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Organization-level | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ |
| Cross-org / public | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |

---

## 6. Key Dimensions of Comparison

### 6.1 Centralized vs. Decentralized Approval

```
  Decentralized                                          Centralized
  (anyone decides)                                    (board approves)
       │                                                      │
       ▼                                                      ▼
   ThoughtWorks ◄────── Nygard ──── Spotify ──── AWS ──── GOV.UK
   (Advice Process)     (team)      (team+RFC)   (team    (tiered
                                                 meeting)  approval
                                                            boards)
```

| Approach | Pros | Cons |
|----------|------|------|
| **Decentralized** (ThoughtWorks) | Fast, high autonomy, low friction | Risk of inconsistency, hard to enforce |
| **Team consensus** (AWS, Nygard) | Balanced, team ownership | Can be slow for large teams, groupthink |
| **Tiered boards** (GOV.UK) | Enterprise accountability, cross-cutting alignment | Bureaucratic, bottleneck risk |

### 6.2 Immutability Model

All surveyed processes except ThoughtWorks agree: **accepted ADRs should be immutable.** The core decision cannot be edited once accepted — changes require a new ADR that supersedes the old one.

| Aspect | Immutable (Nygard, AWS, Spotify, Decentraland) | Living Document (some interpretations) |
|--------|------------------------------------------------|----------------------------------------|
| Historical accuracy | ✅ Preserved — original rationale always visible | ❌ Risk of losing original context |
| Status changes | ✅ Status field can change (`accepted` → `superseded`) | ✅ Status changes inline |
| Content changes | ❌ Content never edited after acceptance | ✅ New sections appended with datestamps |
| Supersession | New ADR created, old one marked `superseded` | In-place update (risk of confusion) |

**Our schema** strongly supports the immutable model via the `audit_trail` (append-only events), `lifecycle.superseded_by`/`supersedes` fields, and the `superseded` status.

### 6.3 RFC-Before-ADR Pattern

Only **Spotify** explicitly separates the exploration phase (RFC) from the decision recording phase (ADR):

| Phase | Purpose | Format | Output |
|-------|---------|--------|--------|
| **RFC** | Explore options, gather feedback, build consensus | Long-form document with options analysis | Agreed solution |
| **ADR** | Record the decision, its context, and consequences | Structured template | Permanent record |

This pattern is increasingly common at scale (Uber, Google, and many startups also use design docs / RFCs before ADRs). However, most processes conflate the two — the ADR itself serves as both the proposal and the record.

### 6.4 Enforcement Mechanisms

| Mechanism | Who Uses It | How It Works |
|-----------|-------------|--------------|
| **Review meetings** | AWS | Synchronous meeting with reading slot + discussion |
| **PR-based review** | Spotify, Decentraland | ADR submitted as a pull request; standard PR review process |
| **Decision Guardian** | Spotify | GitHub Action that surfaces relevant ADRs when protected files change |
| **Code review validation** | AWS | Code reviewers check changes against accepted ADRs |
| **Architecture Advisory Forum** | ThoughtWorks | Regular advisory meeting (non-binding) |
| **Technology Radar** | ThoughtWorks | Shared assessment of technologies as a governance tool |
| **Tiered approval boards** | GOV.UK | Escalation to appropriate decision-making body |
| **JSON Schema validation** | adr-governance, smadr | Automated validation that ADRs conform to schema |

---

## 7. Analysis: Where Standard Processes Fall Short

### 7.1 No Process Has a Complete State Machine

Most processes define only 2–3 states (`proposed` → `accepted` → `superseded`). Only Decentraland provides a full pipeline (`idea` → `draft` → `review` → `last_call` → `final`).

Our schema supports 6 states: `proposed`, `accepted`, `superseded`, `deprecated`, `rejected`, `deferred`. This is good coverage but could benefit from:

| Candidate State | Source | Value |
|----------------|--------|-------|
| `draft` | Decentraland, GOV.UK | Distinguishes "work in progress" from "ready for review" (`proposed`). Useful if we have complex ADRs that need multiple iterations before review. |
| `review` | Decentraland | Explicit "under review" state, separate from `proposed`. Could prevent ambiguity. |

### 7.2 No Process Documents the Process Itself Inside the ADR

None of the surveyed processes embed process metadata (review meeting dates, action items from review, approval timestamps) inside the ADR template. **Our schema is unique** in having:
- `approvals` — structured approval records with timestamps and signature IDs
- `audit_trail` — append-only event log capturing `created`, `reviewed`, `approved`, `superseded` events

### 7.3 No Process Has Periodic Review

Only **GOV.UK** mentions regular review of ADRs. Our schema has `lifecycle.review_cycle_months` and `lifecycle.next_review_date` — a unique feature that prevents decision rot.

---

## 8. Synthesis: Recommendations for Our Process

### 8.1 Our Process Should Be

Based on the comparison, the ideal ADR governance process for our regulated enterprise context should combine elements from multiple models:

| Aspect | Recommendation | Source Inspiration |
|--------|---------------|--------------------|
| **State Machine** | Keep our 6 states. Consider adding `draft` for pre-review work-in-progress. | Decentraland |
| **Ownership** | Single `decision_owner` per ADR (we already have this). Owner drives the review process. | AWS |
| **Review** | Define a review meeting protocol (reading slot + discussion). Record review outcomes in `audit_trail`. | AWS |
| **Approval** | Keep our `approvals` section with formal signatures. This is unique and essential for regulated environments. | Our schema |
| **Immutability** | Accepted ADRs are immutable. Changes require a new superseding ADR. Status and `audit_trail` can be updated. | Nygard, AWS, Spotify |
| **Enforcement** | Schema validation (already done). Consider defining a code review validation process where reviewers check against accepted ADRs. | AWS, Spotify |
| **Periodic Review** | Keep our `lifecycle.review_cycle_months`. Define a process for triggering reviews. | GOV.UK |

### 8.2 Recommended State Machine for `adr-governance`

```
   ┌────────┐
   │  draft │  (new — work in progress, not ready for review)
   └───┬────┘
       │ author marks ready
       ▼
   ┌──────────┐
   │ proposed │  (ready for review by decision-making body)
   └──┬───┬───┘
      │   │
      │   └────────────────────────┐
      │ review process completes   │ decision deferred
      │                            ▼
      │                     ┌──────────┐
      │                     │ deferred │
      │                     └──────────┘
      │
      ├─────────────────────────┐
      │ approved                │ not approved
      ▼                         ▼
   ┌──────────┐          ┌──────────┐
   │ accepted │          │ rejected │  (with documented reason)
   └──┬───────┘          └──────────┘
      │
      │ new ADR supersedes
      ▼
   ┌─────────────┐
   │ superseded  │
   └─────────────┘

      OR

      │ no longer relevant
      ▼
   ┌─────────────┐
   │ deprecated  │
   └─────────────┘
```

**Valid transitions:**
- `draft` → `proposed`
- `proposed` → `accepted` | `rejected` | `deferred`
- `deferred` → `proposed` (re-submitted)
- `accepted` → `superseded` | `deprecated`

### 8.3 Should We Add `draft`?

| Factor | For `draft` | Against `draft` |
|--------|------------|-----------------|
| Clarity | Distinguishes WIP from ready-for-review | Extra state to manage |
| Our context | Complex ADRs (security, compliance, deployment) need iteration before review | Most teams skip it |
| Schema impact | Easy to add — just extend the `status` enum | Breaking change if not optional |
| Precedent | Decentraland, GOV.UK both use it | AWS, Nygard, Spotify don't |

**Recommendation:** ✅ Add `draft` to the schema's status enum. It's low-cost and high-value for our enterprise context where ADRs are complex multi-section documents. A `proposed` ADR should be review-ready; a `draft` ADR is still being authored.

---

## 9. Our Schema's Process Coverage Today

| Process Feature | Schema Support | Where |
|-----------------|---------------|-------|
| Named owner | ✅ | `decision_owner` |
| Authors | ✅ | `authors` |
| Reviewers | ✅ | `reviewers` |
| Formal approvals | ✅ | `approvals` (timestamp + signature ID) |
| Status lifecycle | ✅ | `adr.status` (6 values) |
| Audit trail | ✅ | `audit_trail` (append-only events) |
| Supersession chain | ✅ | `lifecycle.superseded_by` / `supersedes` |
| Periodic review | ✅ | `lifecycle.review_cycle_months` + `next_review_date` |
| Archival | ✅ | `lifecycle.archival` |
| Schema validation | ✅ | `schemas/adr.schema.json` + `scripts/validate-adr.py` + CI |
| Code review validation | ✅ | `adr-process.md` §7.4 — enforcement tooling (CODEOWNERS, PR templates, fitness functions) is downstream, varies by organization |
| Review meeting protocol | 🟡 | `adr-process.md` §3.3 — escalation triggers + format tip (not a full protocol — meeting logistics are downstream) |
| RFC-before-ADR phase | ❌ | Not defined as a process |

**Conclusion:** Our schema already supports the most comprehensive process metadata of any ADR system surveyed. What we lack are **process definitions** (review meeting protocol) — these are organizational practices, not schema features. Enforcement tooling (Decision Guardian, ArchUnit, etc.) is explicitly a downstream concern: ADRs capture decisions; teams that depend on those decisions enforce them.

---

## 10. ADR Anti-Patterns (from AWS)

Worth documenting as they apply across all processes:

| Anti-Pattern | Description | Mitigation |
|-------------|-------------|------------|
| **No decision** | Fear of making the wrong choice paralyzes the team | ADRs are cheap to write and can be superseded. Bias toward action. |
| **Unjustified decision** | Decision made but no reasoning captured | ADR template forces `rationale` and `tradeoffs` fields |
| **Lost decision** | Decision made but not recorded; team forgets or disregards it | ADR repository with mandatory indexing and schema validation |
| **Decision rot** | Accepted ADR becomes stale as context changes | `lifecycle.review_cycle_months` triggers periodic re-evaluation |
| **Ghost decisions** | Undocumented decisions discovered during code review | Backfill ADRs for existing decisions (Spotify pattern) |

---

## 11. Conclusion

ADR governance processes vary along two axes:

1. **Formality:** From Nygard's "just write it" to GOV.UK's tiered approval boards
2. **State granularity:** From 3 states (Nygard) to 6 states (Decentraland)

Our `adr-governance` schema sits at the **high-formality, high-granularity** end — appropriate for regulated financial services. We already have the richest process metadata (approvals, audit trails, lifecycle management) of any system surveyed. The main gap is that we haven't formalized the **process itself** as a documented workflow (review meetings, code review validation, RFC phases).

### Actionable Next Steps

1. ✅ **Add `draft` status** to the schema — Done
2. ✅ **Document code review validation** — Done (`adr-process.md` §7.4). Enforcement tooling is downstream.
3. ✅ **Document review meeting guidance** — Done (`adr-process.md` §3.3). Escalation triggers + format tip, not a full protocol.
4. ⚠️ **Consider RFC-before-ADR** — useful at scale, but adds process weight; defer until we have >20 ADRs

---

## References

1. Nygard, M. (2011). "Documenting Architecture Decisions." [cognitect.com](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions)
2. Kunce, D. & Goby, D. (2022). "Using architectural decision records to streamline technical decision-making." [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/welcome.html)
3. Kunce, D. & Goby, D. (2022). "ADR process." [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
4. ThoughtWorks. "Scaling Architecture Conversationally." [thoughtworks.com](https://www.thoughtworks.com/en-gb/insights/articles/scaling-architecture-conversationally)
5. Spotify Engineering (2020). "When Should I Write an Architecture Decision Record?" [engineering.atspotify.com](https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record/)
6. UK Government Digital Service. "Architectural decision records." [gov.uk](https://www.gov.uk/guidance/architectural-decision-records)
7. Decentraland. "ADR Overview." [adr.decentraland.org](https://adr.decentraland.org)
8. Zimmermann, O. "ADR Tooling." [ozimmer.ch](https://ozimmer.ch)
9. Microsoft Azure (2024). "Architecture decision record." [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
