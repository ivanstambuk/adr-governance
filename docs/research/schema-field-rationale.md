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

**Precedent:**

| Template | Title field | Length constraints? |
|---|---|---|
| Nygard | ✅ Short decision title | ❌ |
| MADR 4.0 | ✅ "# [short title]" | ❌ |
| smadr | ✅ `title` in frontmatter | ❌ |
| Tyree-Akerman | ✅ "Issue" | ❌ |
| All others | ✅ (13/13) | ❌ |
| **adr-governance** | ✅ `adr.title` | ✅ minLength: 10, maxLength: 200 |

**Rationale:** Present in every template surveyed (13/13) — the most universal ADR field. The `minLength: 10` constraint prevents placeholder titles; `maxLength: 200` prevents prose paragraphs masquerading as titles. These bounds were chosen empirically from our example ADRs (shortest: 36 chars, longest: 67 chars).

**Rejected alternatives:**
- *No length constraints* — allows empty or single-word titles ("Auth") and paragraph-length titles that belong in `context.description`
- *Pattern-enforced format (e.g., "Use X over Y")* — considered enforcing a Nygard-style "verb phrase" pattern. Rejected because not all decisions fit this format (e.g., "Defer OpenID Federation" is a valid title that doesn't follow "Use X over Y")

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

**Rejected alternatives:**
- *Dynamic generation from schema fields (render script)* — cannot summarize multi-paragraph Markdown fields into a single sentence; summarization requires authorial judgment
- *AI-generated on-the-fly (bundle capability)* — non-deterministic; hallucination risk; breaks reproducibility of the ADR record
- *Short form only (parts 1–4, omitting "because" clause)* — omits the rationale, which is the most important part of any decision record
- *Retained `adr.summary` alongside Y-Statement* — redundant; the Y-Statement is a strictly more informative summary

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

#### Literature Review: ADR Status Lifecycles

Our 7-status set is a **novel synthesis** — no template in our survey uses exactly this set. This section reviews the status values used across templates, analyzes the design of our state machine, and justifies each addition to and omission from the Nygard baseline.

##### 1. Multi-Template Status Comparison

| Template | Status values | Count | Unique additions |
|---|---|:---:|---|
| Nygard (2011) | proposed, accepted, deprecated, superseded | 4 | — (baseline) |
| MADR 4.0 | proposed, accepted, deprecated, superseded (+ custom) | 4+ | Allows custom statuses |
| smadr | proposed, accepted, deprecated, superseded | 4 | — |
| EdgeX | proposed, accepted, deprecated, superseded | 4 | — |
| Tyree-Akerman | — (no explicit status field) | 0 | — |
| Planguage | — (no explicit status field) | 0 | — |
| Merson (SEI) | proposed, accepted, deprecated, superseded | 4 | — |
| NHS Wales | proposed, under review, accepted, rejected, superseded, deprecated | 6 | `under review`, `rejected` |
| Gareth Morgan | *(unstructured)* | — | — |
| DRF | *(meta.status — details vary)* | — | — |
| UK GDS | draft, proposed, accepted, superseded | 4 | `draft` |
| **adr-governance** | **draft, proposed, accepted, superseded, deprecated, rejected, deferred** | **7** | **`draft`, `rejected`, `deferred`** |

**Key observations:**
- The **Nygard 4-status set** (proposed/accepted/deprecated/superseded) is the de facto standard — adopted by 5+ templates without modification
- Only **NHS Wales** and **UK GDS** extend beyond the Nygard baseline with structured additions
- **No template** includes `deferred` — this is entirely novel
- `rejected` appears only in **NHS Wales** (and MADR via custom extension)
- `draft` appears only in **UK GDS** and our schema

##### 2. Status Classification: Lifecycle Phases

Our 7 statuses decompose into three lifecycle phases, each with distinct semantics:

| Phase | Statuses | Mutability | PR State | Governance |
|---|---|---|---|---|
| **Pre-decision** | `draft`, `proposed`, `deferred` | ✅ Fully mutable | Open or closed | Author-owned → reviewer-owned |
| **Active** | `accepted` | 🟡 Decision core frozen; metadata mutable | Merged | Binding; changes require supersession |
| **Terminal** | `superseded`, `deprecated`, `rejected` | ❌ Frozen (except `lifecycle` overlay) | Merged | Historical record; queryable |

This three-phase model is novel. Most templates have only two phases: pre-decision (proposed) and post-decision (accepted + terminal). Our model explicitly separates **active** from **terminal**, enabling different governance rules for each.

##### 3. Per-Status Semantic Analysis

###### `draft` — Author-owned, pre-review

| Aspect | Detail |
|---|---|
| **Added by** | adr-governance (also UK GDS) |
| **Why needed** | Without `draft`, a half-written ADR must be either `proposed` (triggering premature review) or kept outside Git (losing version control). `draft` enables schema-valid work-in-progress on feature branches. |
| **Transition in** | `[*] → draft` (initial creation) |
| **Transition out** | `draft → proposed` (author opens PR) |
| **PR state** | No PR yet — ADR lives on a feature branch |
| **Schema behavior** | Fewest conditional requirements. `y_statement`, `approvals[].approved_at`, and `audit_trail` `approved` event are not required. |

**Why other templates omit it:** Most templates assume ADRs are created directly as "proposed" Markdown files. In a JSON Schema + CI validation pipeline, an ADR must be schema-valid even before review — `draft` provides the valid-but-not-yet-proposed state that makes this possible.

###### `proposed` — Under active review

| Aspect | Detail |
|---|---|
| **Present in** | Every template with a status field (universal) |
| **Semantics** | The ADR is submitted for formal review. The PR is open. Reviewers are evaluating it. |
| **Transition in** | `draft → proposed`, `deferred → proposed` (re-proposal) |
| **Transition out** | `proposed → accepted`, `proposed → rejected`, `proposed → deferred` |
| **PR state** | Open, under review |
| **Schema behavior** | `approvals[].identity` must be populated (CI verifies against PR approvers). |

**Key design choice:** `proposed → proposed` is a **self-transition** (reviewer requests changes, author reworks, pushes new commits). This avoids needing an intermediate "in review" or "rework" status.

> **Why not `under review` (NHS Wales)?** `under review` is a transient process state that duplicates the PR's "changes requested" mechanism. Our `audit_trail` captures review events without adding a status that would need back-and-forth transitions (`proposed ↔ under_review`), complicating the state machine.

###### `accepted` — Binding, decision core frozen

| Aspect | Detail |
|---|---|
| **Present in** | Every template with a status field (universal) |
| **Semantics** | The decision is binding. The decision core is immutable — changes require a new superseding ADR. |
| **Transition in** | `proposed → accepted` |
| **Transition out** | `accepted → superseded`, `accepted → deprecated` |
| **PR state** | Merged |
| **Schema behavior** | Maximum conditional requirements: `y_statement` required, `approvals[].approved_at` must have ≥1 non-null, `audit_trail` must contain `approved` event. |

**Immutability semantics:** Once accepted, the following fields are frozen:
- `adr.title`, `adr.y_statement`, `adr.project`, `adr.component`, `adr.priority`, `adr.decision_type`
- `authors`, `decision_owner`, `reviewers`, `approvals`
- `context`, `architecturally_significant_requirements`, `alternatives`, `decision`, `consequences`, `dependencies`

This is more rigorous than any template in our survey. Nygard recommends "accepted ADRs should not be changed" but doesn't enforce it. Our CI enforces it via diff-based change classification.

###### `rejected` — Formally evaluated and refused

| Aspect | Detail |
|---|---|
| **Added by** | adr-governance (also NHS Wales, MADR custom) |
| **Why needed** | Without `rejected`, formally evaluated proposals that didn't pass review are either deleted (losing knowledge) or left in `proposed` limbo (misleading). `rejected` explicitly records "we considered this and said no." |
| **Transition in** | `proposed → rejected` |
| **Transition out** | Terminal — `rejected → [*]` (may be archived via `lifecycle.archival`) |
| **PR state** | **Merged** (not closed) — rejected ADRs are merged to `main` to preserve the decision record |

**Why merge rejected ADRs?** This is our most counterintuitive process decision. Closing the PR without merging loses the ADR from `main`, making it invisible to future decision-makers who might re-propose the same rejected idea. Merging preserves the complete evaluation and rejection rationale.

**`chosen_alternative` on rejected ADRs:** When a proposal is rejected but the team selects a different approach (e.g., Vault was proposed but native cloud stores were chosen), `chosen_alternative` records the path forward. `status: rejected` signals that the *proposed approach* (not the ADR itself) was rejected.

###### `deferred` — Explicitly postponed

| Aspect | Detail |
|---|---|
| **Added by** | adr-governance only — **completely novel** |
| **Why needed** | Not every decision can be made now. Context may be insufficient, dependencies unresolved, or timing wrong. Without `deferred`, these decisions are either rejected (wrong — they weren't evaluated negatively) or left in `proposed` (misleading — nobody is reviewing them). |
| **Transition in** | `proposed → deferred` |
| **Transition out** | `deferred → proposed` (re-proposal when ready), or terminal `deferred → [*]` (archived if never revisited) |
| **PR state** | **Closed** with label (not merged and not deleted) |

**Academic support:** The concept of deferring architectural decisions is well-established in architecture literature:
- **Robert C. Martin ("Uncle Bob"):** "Good architecture allows major architectural decisions to be deferred" — the "Last Responsible Moment" principle
- **Jansen & Bosch (2005):** "Software architecture as a set of architectural design decisions" — decisions exist in states of uncertainty before commitment
- **Wirfs-Brock (2011):** "Agile Architecture Myths #2" — the "Most Responsible Moment" (MRM) concept, adapted in our START checklist

`deferred` is the schema-level manifestation of the MRM principle: if the Most Responsible Moment hasn't arrived, the decision should be explicitly parked, not prematurely forced.

###### `superseded` — Replaced by a newer decision

| Aspect | Detail |
|---|---|
| **Present in** | Every template with a status field (universal) |
| **Semantics** | This decision has been replaced by a newer ADR. The new decision is now binding. |
| **Transition in** | `accepted → superseded` |
| **Transition out** | Terminal — `superseded → [*]` (may be archived) |
| **Schema behavior** | `lifecycle.superseded_by` must be populated. Bidirectional: the new ADR's `lifecycle.supersedes` must match. CI validates symmetry. |

**Bidirectional enforcement** is unique to our schema. Other templates recommend linking to the successor but don't enforce it structurally or via CI.

###### `deprecated` — No longer recommended, not yet replaced

| Aspect | Detail |
|---|---|
| **Present in** | Most templates (Nygard baseline) |
| **Semantics** | The decision is outdated but no replacement has been decided yet. The decision remains technically in effect but is "on notice." |
| **Transition in** | `accepted → deprecated` |
| **Transition out** | Terminal — should eventually be superseded or left as historical record |

**Distinction from `superseded`:** `deprecated` = "we've outgrown this but haven't decided what's next." `superseded` = "we've decided what's next and it's ADR-MMMM."

**Timestamp note:** Deprecation has no dedicated timestamp field. The deprecation time is recorded via the `deprecated` event in `audit_trail`. This is intentional — deprecation is a transitional state that should eventually resolve to `superseded`, so it doesn't merit the same structural permanence as archival.

##### 4. State Machine Topology

Our state machine has deliberate topological constraints:

```
Design properties:
  - Directed acyclic graph (no cycles through terminal states)
  - Single entry point: [*] → draft
  - 4 terminal states: rejected, deferred (if never reopened), superseded, deprecated
  - 1 reversible transition: deferred → proposed (only non-terminal re-entry)
  - 1 self-loop: proposed → proposed (rework cycle)
  - Maximum path length: 5 (draft → proposed → accepted → superseded → [archived])
```

**Why no `rejected → proposed` transition?** If a rejected decision needs reconsideration, a **new ADR** should be created. This preserves the original rejection rationale and forces the author to re-evaluate with fresh context. The rejected ADR remains as evidence of what and why.

**Why no `deprecated → accepted` recovery?** If a deprecated decision is found to still be valid, reverting to `accepted` would create an unauditable state change. Instead, either (a) the deprecation was premature and should be reverted via PR discussion, or (b) a new ADR should confirm the original decision with updated context.

##### 5. The `archived` Non-Status

`archived` is deliberately **not** a status value. Archival is an administrative overlay tracked via `lifecycle.archival` fields. This is a key design decision:

| Design | How `archived` works | Consequence |
|---|---|---|
| **As a status** (rejected approach) | `superseded → archived` | Loses the terminal status information. A query for "all superseded ADRs" misses archived ones. |
| **As a metadata overlay** (our approach) | Archived ADRs retain their terminal status + have `lifecycle.archival.archived_at` | Queries work on both dimensions: "all superseded" and "all archived" are independent filters. |

This design was influenced by the observation that archival is an **administrative action** (removing from active consideration) while status represents a **decision lifecycle state** (what happened to this decision). Conflating the two would force a choice between querying by lifecycle outcome vs. querying by visibility.

##### 6. Schema Conditional Requirements by Status

Our schema uses `allOf/if/then` blocks to enforce progressive strictness as ADRs advance:

| Status | `y_statement` | `approvals[].identity` | `approvals[].approved_at` | `audit_trail` `approved` event |
|---|:---:|:---:|:---:|:---:|
| `draft` | ❌ Optional | ❌ Optional | ❌ Optional | ❌ Not required |
| `proposed` | ❌ Optional | ✅ Required | ❌ Optional | ❌ Not required |
| `accepted` | ✅ Required | ✅ Required | ✅ ≥1 non-null | ✅ Required |
| `rejected` | ❌ Optional | ❌ Optional | ❌ Optional | `rejected` event required |
| `deferred` | ❌ Optional | ❌ Optional | ❌ Optional | `deferred` event required |
| `superseded` | ✅ (frozen) | ✅ (frozen) | ✅ (frozen) | `superseded` event required |
| `deprecated` | ✅ (frozen) | ✅ (frozen) | ✅ (frozen) | `deprecated` event required |

This **progressive strictness** model is unique to our schema. Other templates apply the same validation regardless of status, which either over-constrains drafts or under-constrains accepted decisions.

#### Rejected Alternatives

- *Nygard 4-status baseline only (proposed/accepted/deprecated/superseded)* — insufficient for CI-driven governance. Lacks `draft` (needed for schema-valid work-in-progress), `rejected` (needed to preserve evaluation history), and `deferred` (needed for the Last Responsible Moment principle)
- *NHS Wales 6-status set (adding `under review`)* — `under review` is a transient process state that duplicates PR review mechanisms. Our `proposed → proposed` self-transition and `audit_trail` events cover this without a dedicated status
- *MADR custom statuses (open-ended)* — prevents programmatic lifecycle management. CI cannot enforce transition rules if the status set is unbounded. Schema validation cannot express conditional requirements for unknown statuses
- *Separate `in_review` / `rework` / `voting` process substates* — creates a state explosion. A 7-status machine that maps to Git PR states is already at the upper bound of useful complexity. Adding intermediate process states would require transitions like `in_review → rework → in_review → voting → accepted`, making the state machine harder to reason about than the Git PR flow it mirrors
- *`archived` as a status value (8th status)* — conflates lifecycle outcome with visibility. See §5 above for detailed analysis
- *Fewer terminal states (merge `deprecated` into `superseded`)* — semantically different. `deprecated` means "no replacement decided yet"; `superseded` means "replacement exists." The distinction matters for planning: deprecated ADRs need new decisions, superseded ones don't
- *`amended` status for in-place edits to accepted ADRs* — contradicts the immutability principle. Accepted ADRs are frozen; material changes require supersession. An `amended` status would create undiscoverable decision rewrites that bypass the full proposal/review cycle

#### Credits

| Concept | Source |
|---|---|
| 4-status baseline (proposed/accepted/deprecated/superseded) | Nygard, "Documenting Architecture Decisions" (2011) |
| `under review` status | NHS Wales ADR Template |
| `draft` status in ADRs | UK GDS Architecture Decision Records |
| Last Responsible Moment / decision deferral | Martin, *Clean Architecture* (2017); Wirfs-Brock, "Agile Architecture Myths #2" (2011) |
| Architectural decisions as first-class entities with lifecycle states | Jansen & Bosch, "Software Architecture as a Set of Architectural Design Decisions" (WICSA, 2005) |
| Progressive strictness via JSON Schema conditionals | adr-governance (novel) |
| `archived` as metadata overlay vs. status | adr-governance (novel) |



### 1.5 `adr.created_at` / `adr.last_modified`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.created_at`, `adr.last_modified` |
| **Type** | `string`, format: `date-time` (ISO 8601) |
| **Required?** | `created_at`: ✅ Yes; `last_modified`: Optional |

**Precedent:**

| Template | Timestamp field(s) | Format | Required? |
|---|---|---|---|
| Nygard | None — relies on Git history | — | ❌ |
| MADR 4.0 | `date` (single field in frontmatter) | ISO 8601 date | Optional |
| smadr | `created`, `updated` | ISO 8601 date-time | ✅ Both |
| Tyree-Akerman | None | — | ❌ |
| Planguage | `Date` (most recent revision) | Free-text | ✅ |
| EdgeX | Change Log dates | ISO 8601 date | ✅ |
| DRF | `meta.created_at`, `meta.updated_at` | ISO 8601 date-time | ✅ Both |
| NHS Wales | `Updated` (single date) | ISO 8601 date | ✅ |
| **adr-governance** | `created_at` + `last_modified` | ISO 8601 date-time | `created_at`: ✅; `last_modified`: Optional |

**Why ISO 8601?** Three reasons:
1. **Unambiguous sorting** — `2026-03-07T14:30:00Z` sorts lexicographically, unlike `March 7, 2026` or `07/03/2026` (which is ambiguous between DD/MM and MM/DD)
2. **Timezone-aware** — the `Z` suffix or `+HH:MM` offset prevents teams in different timezones from disagreeing on "when was this created?" JSON Schema's `date-time` format validates this automatically
3. **Machine-parseable** — every programming language, database, and CI tool can parse ISO 8601 natively. Free-text dates (Planguage's approach) require locale-specific parsing

**Why two fields, not one?** MADR and NHS Wales use a single `date` field. smadr and DRF use two. The distinction matters:
- **`created_at` is immutable** — set once when the ADR file is created; never changes even through supersession. This is the canonical "birth date" of the decision proposal
- **`last_modified` is mutable** — updated whenever the ADR file changes (draft iterations, post-acceptance updates to `confirmation`, `audit_trail` events). It answers: "when was this file last touched?"
- Together they answer different questions: `created_at` → "how old is this decision?" (useful for staleness analysis); `last_modified` → "is this file current?" (useful for review scheduling)

**Why `last_modified` is optional:** Git itself is a modification tracker — `git log --follow <file>` provides a definitive modification history. The `audit_trail` section captures event-level timestamps with semantic meaning ("reviewed on X", "approved on Y"). A top-level `last_modified` field is therefore *redundant* but not *useless* — it's convenient for non-Git consumers (databases, bundled documents, wiki exports) that lack Git history. Making it optional avoids mandatory bookkeeping while supporting use cases that need it.

**Rejected alternatives:**
- *Git-only timestamps (Nygard style)* — breaks when ADRs are stored outside Git repositories (wikis, databases, compliance systems, bundled documents shared via email). Our framework is Git-native but not Git-exclusive
- *Single `date` field (MADR/NHS Wales style)* — ambiguous: does it mean creation date, decision date, or last modification? Our schema separates these concerns: `created_at` (file birth), `decision.decision_date` (when the decision was made), and `last_modified` (last file change)
- *Free-text date format (Planguage style)* — prevents programmatic sorting, filtering, and validation. The `minLength: 10` pattern on Planguage's `Date` keyword accepts "March 2026" but not "2026-03-07T14:30:00Z"
- *Mandatory `last_modified`* — would force authors to update a field on every commit, creating merge conflicts and CI noise for a field that Git tracks natively

### 1.6 `adr.version` / `adr.schema_version`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.version` (MAJOR.MINOR), `adr.schema_version` (MAJOR.MINOR.PATCH) |
| **Type** | `string` with semver-like patterns |
| **Required?** | `version`: ✅ Yes; `schema_version`: Optional |

**Precedent:**

| Template | Document version? | Schema version? | Version format |
|---|---|---|---|
| Nygard | ❌ | ❌ | — |
| MADR 4.0 | ❌ | ❌ | — |
| smadr | ❌ | ✅ (implicit via JSON Schema `$id`) | URI-based |
| Tyree-Akerman | ❌ | ❌ | — |
| Planguage | ✅ (`Revision` keyword) | ❌ | Free-text increment |
| EdgeX | 🟡 (implicit via Change Log) | ❌ | — |
| DRF | ❌ | ✅ (`meta.schema_version`) | Semver |
| **adr-governance** | ✅ `adr.version` | ✅ `adr.schema_version` | MAJOR.MINOR / MAJOR.MINOR.PATCH |

**Why dual versioning?** The two version fields track different things:

1. **`adr.version` (document version)** — tracks the ADR document's own evolution during the draft and review cycle. When a reviewer says "I reviewed v1.2, but you've since published v1.3," the version field makes this unambiguous. Version bumps occur during the mutable phase (draft → proposed → review iterations). After acceptance, the version freezes along with the decision core — only post-acceptance updates to `confirmation`, `audit_trail`, or `lifecycle` would warrant a minor bump.
   - **MAJOR** increments represent substantive decision changes (during mutable phases only)
   - **MINOR** increments represent non-substantive updates (typos, added confirmation artifacts, review events)

2. **`adr.schema_version` (schema compatibility pin)** — pins the ADR to a specific version of `adr.schema.json`. As the schema evolves (new optional fields, changed constraints), this field enables:
   - **Forward compatibility** — a validator knows which rules to apply when checking an older ADR
   - **Migration tooling** — automated scripts can identify ADRs authored against schema v1.0 and upgrade them to v2.0
   - **Audit clarity** — a compliance reviewer knows which schema version's rules governed the ADR's creation

**Interaction with supersession:** When ADR-0002 supersedes ADR-0001, the *new* ADR starts at `version: "1.0"` — it's a new document. The old ADR's version freezes at whatever it reached before being superseded. Version continuity is *per-document*, not *per-decision-lineage*. The `lifecycle.supersedes` / `lifecycle.superseded_by` fields provide the lineage chain; version provides the document iteration count.

**Why `schema_version` is optional:** Most teams use a single schema version across all ADRs. The field becomes valuable only when the schema undergoes breaking changes and the ADR log contains documents authored against different schema generations. Making it optional avoids unnecessary bookkeeping for single-version deployments.

**Rejected alternatives:**
- *No document version (MADR/Nygard style)* — Git provides file history, but not a human-friendly "version 1.3" label. Review communications ("I approved v1.2") become ambiguous without an explicit version. Planguage recognized this need with its `Revision` keyword.
- *Single unified version field* — conflates document iterations with schema compatibility. A typo fix (document v1.1 → v1.2) should not be confused with a schema migration (schema v1.0 → v2.0)
- *Full semver (MAJOR.MINOR.PATCH) for document version* — PATCH is meaningless for a document that's either substantively changed (MAJOR) or cosmetically tweaked (MINOR). Two levels suffice for ADR documents. Schema version uses three levels because schema changes have a well-defined breaking/non-breaking/fix taxonomy
- *Auto-incrementing version from Git commits* — ties version identity to the VCS, breaking in non-Git contexts. Also produces noisy version numbers (v47 after 47 commits, most of which were whitespace fixes)

### 1.7 `adr.project` / `adr.component`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.project` (required), `adr.component` (optional) |
| **Type** | `string` |
| **Required?** | `project`: ✅ Yes; `component`: Optional |

**Precedent:**

| Template | Project scoping? | Component scoping? | Format |
|---|---|---|---|
| Nygard | ❌ | ❌ | — |
| MADR 4.0 | ❌ | ❌ | — |
| smadr | ✅ `project` (frontmatter) | ❌ | Free-text |
| Tyree-Akerman | ❌ | ❌ | — |
| Planguage | ❌ | ❌ | — |
| EdgeX | ❌ | ✅ (implicit — "Affected Services") | Enumerated service names |
| DRF | ❌ | ❌ (context via CRF entities) | — |
| **adr-governance** | ✅ `adr.project` | ✅ `adr.component` | Free-text strings |

**Why two-level scoping?** Architectural decisions operate at different organizational scopes:
- **`project`** scopes the ADR to a programme, product, or organizational unit — essential when a single ADR repository serves multiple projects (the enterprise monorepo pattern). Without this, filtering "show me all ADRs for the IAM platform" requires text search through context descriptions
- **`component`** narrows further to a specific module, service, or subsystem — e.g., "token-service" within the "IAM platform" project. This enables drill-down: `project: "iam-platform"` → `component: "token-service"` → all decisions affecting that component

Together they create a two-level hierarchy: `project` → `component` → individual ADR. This maps to how most organizations structure their code: organisation → repository/product → module/service.

**Why free-text, not enum?** This is the central design question. Three arguments for free-text:

1. **Organization-specific vocabularies.** Project and component names vary wildly across organizations — "IAM Platform," "Project Phoenix," "team-payments-core." No enum can anticipate these. A controlled vocabulary would require schema customization per deploying organization, defeating the goal of a portable, adopt-as-is schema.

2. **Evolution without schema changes.** Projects are born and retired; components are split, merged, and renamed. An enum requires a schema update (and potentially a schema version bump) for each organizational change. Free-text absorbs these changes without schema modification.

3. **Convention over enforcement.** Teams establish naming conventions through documentation and review, not schema constraints. Our example ADRs demonstrate the pattern: `project: "NovaTrust IAM"`, `component: "token-service"`. Validators can enforce naming patterns (e.g., kebab-case, maximum length) without hardcoding a vocabulary.

**Why `component` is optional:** Not all decisions are component-scoped. Strategic decisions (`decision_level: strategic`) typically affect the entire project or multiple components — forcing a component value would be misleading. The `decision_level` heuristics (§1.11) make this explicit: strategic decisions affect team boundaries and organizational structure, not individual components.

**Rejected alternatives:**
- *Enum-based project/component (EdgeX style)* — EdgeX can enumerate its services because it's a single, well-defined product. Our framework targets arbitrary organizations where the set of projects and components is unknown at schema design time. An enum-based approach would require every adopting organization to fork and customize the schema.
- *Single `scope` field combining project and component* — loses the hierarchical filtering capability. "IAM Platform / token-service" as a single string prevents querying "all ADRs for IAM Platform regardless of component"
- *CRF entity references (DRF style)* — DRF's Context Reasoning Format provides organizational entity references via a separate knowledge graph. This is architecturally elegant but requires CRF infrastructure that doesn't exist yet (DRF is at v0.1.0). A simple string field provides 80% of the value with 0% of the infrastructure overhead
- *No project scoping (Nygard/MADR style)* — works when one repository = one project. Breaks in enterprise environments where a central ADR log serves multiple products, or when ADRs are aggregated into cross-project dashboards
- *`tags`-based scoping (using tags like `project:iam`)* — conflates organizational scoping with freeform discovery. Tags are for cross-cutting concerns ("security," "performance"); project/component is a structural hierarchy. Mixing them prevents clean hierarchical queries

### 1.8 `adr.tags`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.tags` |
| **Type** | `array` of unique strings |
| **Required?** | Optional |

**Precedent:**

| Template | Tagging mechanism | Format | Controlled vocabulary? |
|---|---|---|---|
| Nygard | ❌ None | — | — |
| MADR 4.0 | ❌ None | — | — |
| smadr | ✅ `tags` (frontmatter array) | Free-text | ❌ |
| Tyree-Akerman | ✅ "Categories" (informal) | Prose | ❌ |
| Planguage | ❌ None | — | — |
| EdgeX | ❌ None | — | — |
| DRF | ❌ (uses CRF entity relationships) | — | — |
| **adr-governance** | ✅ `adr.tags` | Array of unique strings | ❌ |

**Why free-text array?** Tags serve a fundamentally different purpose from `decision_type` and `decision_level` (which are controlled enums). Tags enable **freeform, ad-hoc discovery** — organizational jargon, technology names, and project-specific labels that are impossible to anticipate at schema design time:
- Technology tags: `oauth2`, `kubernetes`, `graphql`, `event-sourcing`
- Organizational tags: `q3-initiative`, `platform-migration`, `compliance-2026`
- Cross-cutting concern tags: `performance`, `developer-experience`, `cost-optimization`

The `uniqueItems: true` constraint prevents duplicate tags. No other validation is applied — deliberately.

**Why not a controlled vocabulary (taxonomy)?** Four reasons:

1. **Vocabulary maintenance burden.** A controlled vocabulary requires governance — someone must own the taxonomy, approve new terms, merge synonyms, and retire stale tags. This creates process overhead disproportionate to the value. Tags are metadata, not the core decision record.

2. **Organization-specific terminology.** "DPoP," "BFF," "Step-Up Auth" are meaningful tags in an IAM team but meaningless in a payments team. No universal vocabulary can anticipate domain-specific terminology across all adopting organizations.

3. **Evolution rate mismatch.** Technology names and organizational initiatives change faster than schema releases. A controlled vocabulary frozen in the schema would be perpetually outdated. Free-text tags absorb change immediately.

4. **The enum fields cover the structured cases.** `decision_type` (technology/process/organizational/vendor/security/compliance) and `decision_level` (strategic/tactical/operational) provide the structured classification axes. Tags are the escape valve for everything else — making them controlled would eliminate the flexibility that justifies their existence.

**Relationship to `decision_type` and `decision_level`:** These three fields form a classification triad:

| Field | Purpose | Governance | Cardinality |
|---|---|---|---|
| `decision_type` | Domain classification (what kind) | Controlled enum | Single value |
| `decision_level` | Altitude classification (what scope) | Controlled enum | Single value |
| `tags` | Freeform discovery labels | Uncontrolled | Multiple values |

This is analogous to how content management systems separate structured metadata (categories, types) from freeform metadata (tags, keywords).

**Rejected alternatives:**
- *Controlled vocabulary (enum array)* — requires schema changes for every new tag category. The maintenance burden exceeds the benefit. Teams needing controlled vocabularies can enforce them via CI validation rules or linting without modifying the schema
- *Hierarchical tags (e.g., `security/authentication/oauth2`)* — introduces taxonomy design complexity (what's the hierarchy? who maintains it?). Flat tags with convention-based grouping (prefix patterns like `sec-oauth2`) provide similar discoverability without structural constraints
- *smadr-style `technologies` as separate field* — smadr separates `tags` from `technologies` in frontmatter. Our tags field intentionally subsumes technology labels because the distinction between a "tag" and a "technology" is fuzzy (is `event-sourcing` a technology or a pattern?). A single unstructured field avoids this classification debate
- *No tags field (Nygard/MADR style)* — forces all discovery through full-text search of context descriptions. Structured tags enable exact-match filtering: "show me all ADRs tagged `oauth2`" is faster and more precise than searching for "oauth2" across all prose fields
- *Tag validation via `pattern` constraint* — considered adding a regex pattern like `^[a-z0-9-]+$` to enforce kebab-case tags. Rejected because it prevents multi-word tags ("developer experience"), proper nouns ("OAuth2"), and version-specific tags ("spring-boot-3.x"). Convention guides in process documentation are sufficient

### 1.9 `adr.priority`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.priority` |
| **Type** | `enum`: `low`, `medium`, `high`, `critical` |
| **Required?** | Optional |

**Precedent:**

| Template | Priority field | Structured? | Levels |
|---|---|---|---|
| Planguage | ✅ Priority keyword | 🟡 Free-text | Unstructured |
| DRF | ✅ `priority` in context objectives | ✅ | Varies |
| MADR / Nygard / smadr | ❌ Absent | — | — |
| Tyree-Akerman / EdgeX / Merson | ❌ Absent | — | — |
| **adr-governance** | ✅ `adr.priority` | ✅ Enum | low / medium / high / critical |

**Rationale:** Priority signals review urgency and implementation ordering. A `critical` decision demands immediate attention; a `low` decision can wait for a convenient sprint. The four-level enum aligns with standard risk/priority scales used in ITSM and project management.

**Rejected alternatives:**
- *Three-level priority (low/medium/high)* — omits the "critical" tier needed for urgent decisions requiring immediate escalation (e.g., security incidents, compliance deadlines). Four levels match ITIL and most project management frameworks
- *Numeric priority (1–10)* — creates false precision; the difference between priority 6 and priority 7 is subjective. Categorical labels are easier to reason about
- *Required field* — not all decisions have inherent urgency differences. Making priority optional avoids forcing authors to guess a priority for routine operational decisions

### 1.10 `adr.decision_type`

| Attribute | Value |
|---|---|
| **Schema path** | `adr.decision_type` |
| **Type** | `enum`: `technology`, `process`, `organizational`, `vendor`, `security`, `compliance` |
| **Required?** | ✅ Yes |

#### Literature Review: Decision Classification Frameworks

No single academic framework prescribes our exact 6-value taxonomy. Our `decision_type` is a **novel synthesis** drawn from multiple classification traditions. This section reviews the major frameworks, explains why each was insufficient alone, and justifies our specific domain set.

##### 1. Kruchten's Ontology — Existence / Property / Executive (2004)

**Primary source:** Philippe Kruchten, "An Ontology of Architectural Design Decisions in Software-Intensive Systems" (WICSA, 2004)

Kruchten classifies decisions by their **nature** (what they *do* to the architecture):

| Type | Definition | Example |
|---|---|---|
| **Existence** | Introduces or bans a structural/behavioral element | "The system has three layers" / "No stored procedures" |
| **Property** | Defines an enduring quality or design rule | "All domain classes are in Layer 2" |
| **Executive** | Business/process/organizational — not about design elements | "Use J2EE" / "All interface changes require CCB approval" |

**Assessment:** Kruchten's types answer *"what kind of thing is this decision?"* — it classifies the **nature** of the decision (structural, qualitative, or environmental). Our `decision_type` answers a different question: *"which domain of concern does this decision address?"* — it classifies the **subject matter**. These are orthogonal dimensions:

| | Existence (structural) | Property (quality) | Executive (environmental) |
|---|---|---|---|
| `technology` | "Use PostgreSQL" | "All DB queries < 50ms" | "Standardize on PostgreSQL across teams" |
| `security` | "Add WAF layer" | "Zero critical CVEs per release" | "All security decisions require CISO sign-off" |
| `vendor` | "Deploy on AWS" | "99.9% SLA" | "Procure enterprise support contract" |

**Conclusion:** Kruchten's types are not alternatives to our `decision_type`; they classify a *different dimension*. We don't duplicate this dimension because it overlaps significantly with `decision_level` (executive ≈ strategic; existence ≈ operational). Adding Kruchten types would create three classification enums, which is excessive.

##### 2. Zimmermann SOA Decisions — Conceptual / Technology / Asset (2007–2012)

**Primary source:** Olaf Zimmermann, "An Architectural Decision Modeling Framework..." (WICSA, 2007)

Zimmermann groups decisions by **abstraction level**:

| Level | Focus | Example |
|---|---|---|
| **Conceptual** | Platform-independent patterns and styles | "Use microservices" |
| **Technology** | Platform-specific technology bindings | "Use Spring Boot" |
| **Asset** | Specific product/library/version | "Use Spring Boot 3.2.1" |

**Assessment:** This is an **abstraction hierarchy**, not a domain classification. It is the direct ancestor of our `decision_level` (Strategic/Tactical/Operational), not `decision_type`. The distinction is already captured in §1.11.

##### 3. TOGAF ADM — Business / Data / Application / Technology (The Open Group)

**Primary source:** TOGAF Standard, 10th Edition (The Open Group, 2022)

TOGAF's four architecture domains (BDAT):

| Domain | Focus | Stakeholders |
|---|---|---|
| **Business** | Strategy, governance, organizational structure | Business leaders, process owners |
| **Data** | Data structures, relationships, governance | Data architects, DPOs |
| **Application** | Application behavior, interactions, services | Solution architects, developers |
| **Technology** | Infrastructure, networks, platforms | Infrastructure architects, ops |

**Assessment:** BDAT is **enterprise architecture scoping**, not decision classification. It works well for EA planning but poorly for decision routing:
- **No security domain** — security decisions span all four TOGAF domains
- **No compliance domain** — regulatory decisions are orthogonal to BDAT
- **No vendor domain** — vendor choices cut across Application and Technology
- **"Data" as a domain** — in ADR practice, data decisions are almost always `technology` decisions (which database, which schema format). A separate "data" type would create category confusion.

TOGAF's BDAT is an architecture *scope* framework, not a decision *type* framework.

##### 4. Tyree-Akerman "Category" Field (IEEE Software, 2005)

**Primary source:** Tyree & Akerman, "Architecture Decisions: Demystifying Architecture" (IEEE Software, 2005)

Tyree-Akerman includes a free-text "Category" field in their ADR template. No prescribed categories — the field is intentionally open. Example categories from the paper: "Integration", "Persistence", "Security".

**Assessment:** Validates the need for domain classification but provides no guidance on *which* categories. Free-text prevents programmatic filtering and aggregation.

##### 5. Enterprise AI Decision Taxonomy (emerging, 2024–2025)

Enterprise AI governance frameworks are introducing decision taxonomies that include:
- Scope, Budget, Timeline, Resourcing, **Vendor/Tooling**, **Policy/Compliance**, Technical Architecture

**Assessment:** Convergent evidence that `vendor` and `compliance` are recognized as distinct decision categories in enterprise practice. Our taxonomy captures both.

##### 6. OWASP Secure by Design Framework (2024)

OWASP's framework treats security as an architectural concern orthogonal to all other domains — validating the need for `security` as a dedicated decision type rather than embedding it in `technology`.

#### Comparative Analysis

| Framework | # Categories | Classification Dimension | Overlap with Our `decision_type`? |
|---|:---:|---|---|
| Kruchten (2004) | 3 | Nature (existence/property/executive) | ❌ Orthogonal — classifies nature, not domain |
| Zimmermann SOA (2007) | 3 | Abstraction (conceptual/tech/asset) | ❌ Already captured in `decision_level` |
| TOGAF BDAT | 4 | EA scope (business/data/app/tech) | 🟡 Partial — lacks security, compliance, vendor |
| Tyree-Akerman (2005) | Open | Free-text (uncontrolled) | 🟡 Validates need, no specific values |
| Enterprise AI Taxonomy | ~7 | Enterprise governance | ✅ Includes vendor, compliance as distinct types |
| OWASP SbD (2024) | — | Security as cross-cutting concern | ✅ Validates security as distinct category |

#### Why These 6 Values

No existing framework maps directly to our taxonomy. Our 6 values are derived from **enterprise practice** — the domains that consistently emerge when organizations classify their architectural decisions for routing and governance:

| Value | What It Captures | Why It's Distinct | Primary Stakeholders |
|---|---|---|---|
| `technology` | Protocol, library, framework, algorithm, infrastructure | The default "what tool do we use?" category. Largest by volume. | Engineering leads, solution architects |
| `process` | Workflow, methodology, governance, SDLC | How teams *work*, not what they *build*. ADR-0000 itself is a process decision. | Engineering managers, process owners |
| `organizational` | Team structure, ownership, RACI, capability allocation | Conway's Law territory — org structure drives architecture. | VPs of Engineering, team leads |
| `vendor` | Third-party product, SaaS, cloud provider, licensing | Involves procurement, legal review, and long-term contracts — fundamentally different decision dynamics than technology choices. | Procurement, legal, finance, architects |
| `security` | Authentication, authorization, cryptography, encryption, identity | Cross-cutting concern requiring specialist review. OWASP, NIST, and regulatory frameworks all treat security decisions as requiring dedicated governance. | CISO, security architects, security champions |
| `compliance` | Regulatory (GDPR, SOC 2, HIPAA, eIDAS), legal, audit-driven | Decisions constrained by *external authority* rather than internal preference. Reversal may be legally impossible. | DPO, compliance officers, legal counsel |

#### The Decision Matrix: `decision_type` × `decision_level`

`decision_type` and `decision_level` are **independent, orthogonal dimensions**. Every ADR occupies one cell in this matrix:

```
                         decision_type (WHAT domain)
               ┌────────────┬────────────┬────────────┬────────────┬────────────┬────────────┐
               │ technology │  process   │   org      │  vendor    │ security   │ compliance │
  ┌────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┤
d │  strategic │ Adopt      │ Adopt ADR  │ Inverse    │ AWS vs     │ Zero-trust │ eIDAS 2.0  │
e │            │ micro-     │ governance │ Conway     │ Azure vs   │ network    │ wallet     │
c │            │ services   │ process    │ maneuver   │ GCP        │ model      │ adoption   │
i ├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┤
s │  tactical  │ Use        │ PR-based   │ Platform   │ Use Auth0  │ BFF Token  │ DPO        │
i │            │ Spring     │ ADR review │ team owns  │ for IdP    │ Mediator   │ approval   │
o │            │ Boot 3.x   │ flow       │ auth APIs  │            │ pattern    │ workflow   │
n ├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┤
  │operational │ Use        │ Trunk-     │ SRE on-    │ Procure    │ Ed25519    │ Audit log  │
_ │            │ Postgres   │ based      │ call       │ enterprise │ for JWT    │ retention  │
l │            │ 16         │ development│ rotation   │ support    │ signing    │ 7 years    │
  └────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘
```

This 3×6 matrix demonstrates that:
1. Every cell is a plausible ADR — there are no empty cells
2. No column is a subset of another — each `decision_type` has unique stakeholders
3. No row is a subset of another — each `decision_level` has unique reversal costs
4. The two dimensions provide independent information — knowing one doesn't predict the other

#### Term Selection

| Value | Chosen Because | Rejected Synonyms |
|---|---|---|
| `technology` | Universal industry term; immediately understood | `technical` (too broad — overlaps with security), `engineering` (too narrow) |
| `process` | Standard management term; covers workflow + methodology | `governance` (too narrow — we have governance mechanisms, process is broader), `methodology` (too academic) |
| `organizational` | Direct, unambiguous | `team` (too narrow), `people` (too informal), `structural` (confuses with code structure) |
| `vendor` | Standard procurement term | `commercial` (excludes OSS vendors), `third-party` (verbose), `supplier` (less common in tech) |
| `security` | Universal term; matches CISO role title | `cybersecurity` (too narrow — excludes physical security), `infosec` (jargon) |
| `compliance` | Standard regulatory term; matches compliance officer role | `regulatory` (excludes voluntary standards like SOC 2), `legal` (too narrow — not all compliance is law) |

#### Rejected Alternatives

- *Kruchten's three types (Existence/Property/Executive)* — classifies the **nature** of the decision, not the domain. These are orthogonal to our `decision_type` and would add a third classification axis with diminishing returns
- *TOGAF four domains (Business/Data/Application/Technology)* — EA scoping framework, not action-oriented. Lacks security, compliance, vendor. "Data" as a type is too specific for ADR practice
- *Unlimited free-text category (Tyree-Akerman style)* — prevents programmatic filtering, dashboard aggregation, and automated stakeholder routing
- *DDD-aligned categories (Domain/Infrastructure/Integration)* — too narrow for organizations not practicing DDD
- *Fewer categories (e.g., technical/non-technical binary)* — too coarse. `vendor` decisions have different stakeholders than `technology` decisions, even though both are "technical." A binary split loses routing value.
- *More categories (add "data", "integration", "performance", etc.)* — diminishing returns. Additional categories create classification uncertainty ("is this a data decision or a technology decision?"). The 6 values cover >95% of real-world ADRs without ambiguity. Edge cases use `tags` for finer-grained labeling.
- *Multi-select (allow multiple types per ADR)* — tempting, but creates classification drift. A decision tagged `security` + `compliance` + `technology` communicates nothing useful. Forcing single classification requires the author to identify the *primary* domain, which is the most valuable routing signal. Secondary concerns are captured in prose and tags.

#### Credits

| Concept | Source |
|---|---|
| Existence / Property / Executive ontology | Kruchten, "An Ontology of Architectural Design Decisions" (WICSA, 2004) |
| Conceptual / Technology / Asset levels | Zimmermann et al., SOA Decision Models (2007–2012) |
| BDAT architecture domains | TOGAF Standard, 10th Edition (The Open Group, 2022) |
| "Category" field in ADR templates | Tyree & Akerman, "Architecture Decisions" (IEEE Software, 2005) |
| Security as cross-cutting architectural concern | OWASP Secure by Design Framework (2024) |
| Vendor/Tooling as distinct decision category | Enterprise AI Decision Taxonomy (emerging, 2024–2025) |


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

### 2.0 `$defs/person` Reusable Type

| Attribute | Value |
|---|---|
| **Schema path** | `$defs/person` (referenced by `authors`, `decision_owner`, `reviewers`) |
| **Type** | `object`: `name` (required), `role` (required), `email` (optional) |
| **Used by** | `authors[]`, `decision_owner`, `reviewers[]` |

**Precedent:**

| Template | Person representation | Structured? | Role captured? |
|---|---|---|---|
| Nygard | None — no author field | ❌ | ❌ |
| MADR 4.0 | `decision-makers` (list of names in frontmatter) | 🟡 Flat strings | ❌ |
| smadr | `author` (name string) | 🟡 Single string | ❌ |
| Tyree-Akerman | None | ❌ | ❌ |
| Planguage | `Owner` / `Author` (name strings) | 🟡 Flat strings | ❌ |
| EdgeX | `Submitters` (list of names) | 🟡 Flat strings | ❌ |
| DRF | Participant objects with roles | ✅ | ✅ |
| **adr-governance** | `person` object: name + role + email | ✅ | ✅ |

**Why a structured type, not a plain string?** Three fields, three purposes:

1. **`name` (required)** — human-readable identifier. Self-evident.

2. **`role` (required)** — the person's organizational role *in the context of this decision*. This is the distinguishing design choice. Knowing the approver is a "CISO" vs. a "Senior Developer" changes how a reader interprets the approval's weight. The same person may serve different roles across ADRs — an engineer who authored ADR-0001 as a "Developer" might review ADR-0005 as a "Security Champion." Role is per-usage, not per-person.

3. **`email` (optional)** — contact channel. Optional because: (a) email addresses change when people leave organizations, (b) many organizations use Slack/Teams handles or platform usernames (`approvals[].identity`) instead, (c) privacy regulations (GDPR) may prohibit storing email in public repositories.

**Why a reusable `$defs` type?** The person structure appears in four places (`authors[]`, `decision_owner`, `reviewers[]`, and conceptually in `approvals[]` which extends it with `identity`/`approved_at`/`signature_id`). A `$ref` definition ensures consistency — changing the person structure updates all usages simultaneously.

**Rejected alternatives:**
- *Plain string per person (MADR/smadr/EdgeX style)* — loses role context. "Jane Doe" tells you nothing about her authority to approve. "Jane Doe, CISO" is more informative but requires parsing a convention
- *Separate `name` and `role` fields without `$defs` (inline per usage)* — duplicates the type definition in four places, creating drift risk when the schema evolves
- *Platform identity in person type (username/email as primary key)* — platform identities are volatile (people change jobs, rename GitHub accounts). The `name` + `role` combination is human-readable and platform-independent. Platform identity is reserved for `approvals[].identity` where CI verification needs it
- *Required email* — privacy risk in public repos; organizational churn makes emails stale. The `identity` field in `approvals` serves the CI verification purpose without requiring email

### 2.1 `authors`

| Attribute | Value |
|---|---|
| **Schema path** | `authors` (top-level) |
| **Type** | `array` of `$ref: person` (name + role + optional email), minItems: 1 |
| **Required?** | ✅ Yes |

**Precedent:**

| Template | Author field | Structured? | Multiple authors? |
|---|---|---|---|
| Nygard | ❌ None | — | — |
| MADR 4.0 | `decision-makers` (frontmatter) | 🟡 Flat strings | ✅ |
| smadr | `author` (frontmatter) | 🟡 Single string | ❌ |
| Tyree-Akerman | ❌ None | — | — |
| Planguage | `Author` keyword | 🟡 Single string | ❌ |
| EdgeX | `Submitters` | 🟡 Flat strings | ✅ |
| DRF | Participant with role | ✅ | ✅ |
| **adr-governance** | `authors[]` of `$ref: person` | ✅ | ✅ (minItems: 1) |

**Rationale:** Every decision has an author who can be consulted for context. The structured `person` type (name + role) enables organizational context — knowing the author is a "Security Architect" vs. "Junior Developer" informs how to weight the decision. The `minItems: 1` constraint ensures accountability — every ADR must have at least one named author.

**Rejected alternatives:**
- *Plain string author name (MADR/smadr style)* — loses the role context. The same person may author ADRs in different capacities across projects
- *Git author only (no schema field)* — Git tracks the committer, not the decision author. Decisions are often authored collaboratively or by someone different from the committer
- *Single author (smadr/Planguage style)* — architectural decisions are frequently co-authored; limiting to one author misrepresents collaborative authoring

### 2.2 `decision_owner`

| Attribute | Value |
|---|---|
| **Schema path** | `decision_owner` (top-level) |
| **Type** | `$ref: person` |
| **Required?** | ✅ Yes |

**Precedent:**

| Template | Ownership concept | Separate from author? |
|---|---|---|
| Planguage | `Owner` keyword | ✅ Yes — distinct from `Author` |
| MADR 4.0 | `decision-makers` | ❌ Conflated |
| NHS Wales | Informal "decision maker" | 🟡 Mentioned, not structured |
| **adr-governance** | `decision_owner` (structured person) | ✅ Yes |

**Rationale:** The author writes the ADR; the **decision owner** is accountable for the outcome. These are often different people — a senior architect may delegate authoring to a team member while retaining accountability. Enterprise governance requires knowing who holds the decision, not just who typed it.

**Rejected alternatives:**
- *Combined author/owner field (MADR `decision-makers` style)* — conflates who typed it with who is accountable. In enterprise governance, this distinction matters for escalation and compliance
- *Optional decision owner* — every decision must have someone accountable. An ownerless decision is an orphaned decision that nobody maintains

### 2.3 `reviewers`

| Attribute | Value |
|---|---|
| **Schema path** | `reviewers` (top-level) |
| **Type** | `array` of `$ref: person` |
| **Required?** | Optional |

**Precedent:**

| Template | Reviewer concept | Structured? | Separate from approvers? |
|---|---|---|---|
| MADR 4.0 | `consulted` + `informed` (RACI) | 🟡 Flat strings | ✅ |
| NHS Wales | Informal "reviewed by" | 🟡 | ❌ |
| **adr-governance** | `reviewers[]` of `$ref: person` | ✅ | ✅ |

**Rationale:** Records who reviewed the ADR without necessarily approving it. Important for auditability — "who looked at this?" is a different question from "who approved it?" Optional because not all ADRs go through formal review (operational/low-priority decisions may skip this).

**Rejected alternatives:**
- *RACI matrix (MADR style)* — MADR 4.0 uses `consulted` + `informed` in a RACI model. Our simpler `reviewers` + `approvals` split covers the same ground without RACI overhead. The four RACI roles (Responsible/Accountable/Consulted/Informed) are overkill for ADRs — `authors` = R, `decision_owner` = A, `reviewers` = C, and the PR notification system handles I.
- *Required field* — operational decisions often don't need formal review. Making reviewers mandatory would add friction to low-ceremony decisions.

### 2.4 `approvals`

| Attribute | Value |
|---|---|
| **Schema path** | `approvals` (top-level) |
| **Type** | `array` of objects: name, role, identity, approved_at, signature_id |
| **Required?** | Conditionally — required when `status` is `proposed` or `accepted` |

#### Literature Review: Approval and Governance Models

Our structured approval model with CI-verifiable identities is **completely novel** in the ADR space. No other template has formal approvals as a structured, machine-readable section. This section analyzes why, how we designed our model, and what governance traditions informed it.

##### 1. ADR Template Approval Mechanisms

| Template | Approval mechanism | Structured? | CI-verifiable? | Audit trail? |
|---|---|---|---|---|
| Nygard | ❌ None — status implicitly signals acceptance | — | ❌ | ❌ |
| MADR 4.0 | ❌ None (implicit via PR merge) | — | ❌ | ❌ |
| smadr | 🟡 Compliance table (optional) | Partially | ❌ | 🟡 |
| Tyree-Akerman | ❌ None (assumes ARB process) | — | ❌ | ❌ |
| Planguage | ❌ None (Owner field only) | — | ❌ | ❌ |
| Merson (SEI) | ❌ None | — | ❌ | ❌ |
| EdgeX | ❌ None (implicit via PR) | — | ❌ | ❌ |
| NHS Wales | 🟡 "More Information" mentions participants | Narrative | ❌ | ❌ |
| DRF | ❌ None | — | ❌ | ❌ |
| **adr-governance** | ✅ Structured array + CI verification | ✅ | ✅ | ✅ |

**Key finding:** Every existing ADR template relies on **out-of-band** approval mechanisms — either the Git platform's PR approval feature, an external Architecture Review Board (ARB) process, or informal consensus. None capture approvals *within* the ADR document as structured, verifiable data.

##### 2. Why In-Document Approvals?

The gap creates three practical problems:

| Problem | Without in-document approvals | With in-document approvals |
|---|---|---|
| **Portability** | Export an ADR to a wiki, bundle, or compliance report → approval history is lost. Who approved this decision? Check the PR — if it still exists. | Approval data travels with the ADR. |
| **Auditability** | SOC 2 / HIPAA auditors must cross-reference ADR files with PR histories across platforms. | Single source of truth: the ADR file is its own audit record. |
| **Discoverability** | "Which decisions did the CISO approve?" requires querying the Git platform API, which varies per platform. | `grep -r '"role": "CISO"' architecture-decision-log/` |

##### 3. Governance Model Comparison

Our approval model bridges ADR documentation with enterprise governance practices:

| Governance Model | Approval Pattern | What adr-governance Borrows |
|---|---|---|
| **Architecture Review Board (ARB)** | Standing committee reviews designs; formal approve/reject/defer with minutes | The three-outcome model (accepted/rejected/deferred) and the concept of named approvers with roles |
| **TOGAF Architecture Governance** | Phase G: governance board monitors compliance with approved architecture | Audit trail events, periodic review mechanism |
| **ISO/IEC/IEEE 42010:2022** | Architecture descriptions must document stakeholder concerns and decision rationale with traceability | Structured person types with roles; traceability from decision → approver → rationale |
| **SOC 2 Type II** | Requires evidence that controls were designed, approved by authorized personnel, and maintained over time | `approved_at` timestamps, `identity` verification, append-only `audit_trail` |
| **eIDAS/Qualified Electronic Signatures** | EU regulation requiring signature attribution for legal acts | `signature_id` field bridges to external e-signature services |
| **Git platform PR approvals** | Built-in approve/reject on pull requests — cryptographically attributed to a user account | `identity` field + CI script verifying ADR approvals match PR approvals |

##### 4. Per-Sub-Field Design Rationale

###### `name` + `role` (inherited from `$defs/person`)

| Aspect | Detail |
|---|---|
| **Why structured?** | Prose like "Approved by Jane Doe, Lead Architect" is not machine-parseable. Structured fields enable queries: "which decisions did the Lead Architect approve?" |
| **Why `role` matters** | An approval from the "CISO" carries different weight than one from "Junior Developer." Role context enables stakeholder routing and audit scoping. |
| **Cross-reference** | Same `person` type used in `authors`, `decision_owner`, `reviewers` — consistent schema. See §2.0 for `$defs/person` rationale. |

###### `identity` — Platform-resolvable handle

| Aspect | Detail |
|---|---|
| **What it is** | The platform-specific identifier that CI uses to verify the approval: GitHub `@username`, Azure DevOps email/UPN, GitLab `@username` |
| **Why it exists** | Without this, anyone can write arbitrary names in `approvals[]` and merge with a different set of PR approvers. `identity` creates a **binding** between the ADR's formal approval record and the Git platform's cryptographic approval record. |
| **How CI uses it** | (1) CI detects which ADR files changed in the PR → (2) extracts all `approvals[].identity` values → (3) queries the platform API for actual PR approvers → (4) verifies the sets match → (5) blocks merge if they don't |
| **Platform compatibility** | Tested patterns: GitHub `GET /repos/{owner}/{repo}/pulls/{number}/reviews`, Azure DevOps `GET /_apis/git/pullRequests/{id}/reviewers`, GitLab `GET /projects/:id/merge_requests/:iid/approval_state` |

**This is the most novel sub-field in the entire schema.** No other ADR template, and no other document-governance framework we surveyed, implements a CI-verified identity binding between a document-level approval record and a platform-level cryptographic approval.

The closest analogy is **code signing** in CI/CD pipelines — where a build artifact's cryptographic signature is verified against an expected signing key. Our `identity` verification operates at a higher level: it verifies that the *humans* who conceptually approved the decision are the same *humans* who technically approved the PR.

###### `approved_at` — ISO 8601 timestamp, nullable

| Aspect | Detail |
|---|---|
| **Why nullable?** | When an ADR enters `proposed` status, the `approvals[]` array is populated with expected approvers (name, role, identity) but approval hasn't happened yet. `approved_at: null` signals "pending." Once the PR is approved, the author fills in the timestamp. |
| **Why not omit until approved?** | Pre-populating the approvals list with `null` timestamps serves as a checklist: "these are the people who need to approve this." It makes the expected approval set discoverable before approval occurs. |
| **Progressive strictness** | `proposed` ADRs: `approved_at` may be null. `accepted` ADRs: at least one `approved_at` must be non-null (schema conditional). |
| **Why ISO 8601?** | Same rationale as `created_at` / `last_modified` — see §1.5. Unambiguous, timezone-aware, machine-parseable. |

###### `signature_id` — External signature reference, nullable

| Aspect | Detail |
|---|---|
| **What it is** | A reference to an external signing artifact: DocuSign envelope ID, Jira approval ticket, PGP signature hash, qualified electronic signature reference |
| **Why nullable?** | Most teams don't use formal signing. The field exists for **regulated environments** (financial services, healthcare, EU public sector) where decisions require qualified electronic signatures under eIDAS or equivalent. |
| **Why not a URL?** | Signature IDs are often opaque identifiers (DocuSign envelope GUIDs, PGP key fingerprints) that don't have stable URLs. A string field accommodates any format. |
| **When to use** | Use when your organization's compliance framework requires that architectural decisions have a formal sign-off trail beyond Git platform approvals — typically SOC 2, HIPAA, eIDAS, or internal audit requirements |

##### 5. Conditional Requirement Design

The `approvals` field uses JSON Schema's `allOf/if/then` for progressive enforcement:

| Status | `approvals[]` required? | `identity` required? | `approved_at` required? | `audit_trail` event? |
|---|:---:|:---:|:---:|:---:|
| `draft` | ❌ | ❌ | ❌ | ❌ |
| `proposed` | ✅ ≥1 entry | ✅ on every entry | ❌ (may be null) | ❌ |
| `accepted` | ✅ ≥1 entry | ✅ on every entry | ✅ ≥1 non-null | ✅ `approved` event |
| `rejected` | ❌ | ❌ | ❌ | ✅ `rejected` event |
| `deferred` | ❌ | ❌ | ❌ | ✅ `deferred` event |

**Why not always required?** Requiring approvals on `draft` ADRs would block early-stage authoring. Requiring them on `rejected` and `deferred` ADRs would be semantically wrong — these outcomes don't represent approval. The conditional model ensures schema requirements match governance semantics.

**Scope boundary for terminal states:** `rejected` and `deferred` ADRs don't use the `identity` verification model. Their authoritative disposition history lives in the PR/MR discussion plus the ADR's terminal `audit_trail` event, because Git platforms do not expose one portable cross-platform "rejected/deferred by these identities" signal equivalent to approval.

##### 6. The Approval–Audit Trail Duality

Our schema deliberately captures approval information in **two places**:

| Concern | Where captured | Why |
|---|---|---|
| **Who approved, when, in what role** | `approvals[]` array | Structured, queryable, CI-verifiable |
| **That approval happened as an event** | `audit_trail[]` with `event: "approved"` | Chronological event log, append-only |

This is intentional redundancy. The `approvals[]` array is a **state snapshot** (who has approved right now?). The `audit_trail` is a **event log** (what happened, in order?). Both perspectives are needed:
- **State perspective:** "Is this ADR fully approved?" → check `approvals[].approved_at`
- **Event perspective:** "When was this ADR approved relative to when it was proposed?" → check `audit_trail` chronology

#### Rejected Alternatives

- *Git-only approvals (implicit via PR approval)* — no audit trail in the ADR itself. When ADRs are exported, bundled, or stored outside Git, the approval history is lost. SOC 2 auditors must cross-reference ADR files with PR histories — fragile and platform-dependent
- *Simple boolean `approved: true/false`* — loses who, when, and in what capacity. Useless for regulated environments that need named approvers
- *Free-text "Approved by" field* — not machine-parseable. Cannot drive CI verification. Cannot answer "which decisions did the CISO approve?" without NLP
- *Always-required approvals* — drafts and deferred ADRs don't need approvals. Conditional requirement avoids blocking early-stage authoring
- *Single approver (not an array)* — many decisions require multi-party approval (e.g., technology choice needs Lead Architect + CISO). An array accommodates any approval matrix
- *RACI matrix as approvals model* — too heavyweight. RACI defines Responsible/Accountable/Consulted/Informed roles for every task. Our schema already captures the "A" (Accountable = `decision_owner`), "C" (Consulted = `reviewers`), and "R/A" (Responsible/Approving = `approvals`). A formal RACI matrix would over-structure a process that maps naturally to Git PR review/approve semantics
- *Architecture Review Board minutes as separate document* — creates a separate artifact that may diverge from the ADR. Our model embeds approvals in the ADR document, ensuring the decision record is its own single source of truth
- *Blockchain-based approval immutability* — technically interesting but adds deployment complexity far exceeding the value for ADR governance. Git's commit hash chain already provides cryptographic immutability. `audit_trail` append-only semantics + branch protection provide adequate tamper-evidence
- *`approved_at` as required (never null)* — prevents pre-populating the approvals checklist before approval occurs. Nullable `approved_at` enables the "expected approvers" pattern where the list is set during `proposed` and timestamps filled during `accepted`

#### Credits

| Concept | Source |
|---|---|
| No-approvals baseline (implicit via PR merge) | Nygard (2011), MADR 4.0, smadr, EdgeX |
| Optional compliance table | smadr (structured metadata) |
| Architecture Review Board governance | TOGAF ADM Phase G; enterprise architecture practice |
| Stakeholder concern traceability | ISO/IEC/IEEE 42010:2022 |
| Evidence-based control approval | SOC 2 Type II audit requirements |
| Qualified electronic signatures | eIDAS Regulation (EU) No 910/2014 |
| CI-verified identity binding | adr-governance (novel) |
| Approval–audit trail duality | adr-governance (novel) |
| Progressive conditional requirements | adr-governance (novel) |

---

## Section 3: `context` — Problem Space

### 3.1 `context.description`

| Attribute | Value |
|---|---|
| **Schema path** | `context.description` |
| **Type** | `string`, minLength: 20 (Markdown-native) |
| **Required?** | ✅ Yes |

**Precedent:**

| Template | Context section name | Markdown? | Required? |
|---|---|---|---|
| Nygard | "Context" | ❌ Plain text | ✅ |
| MADR 4.0 | "Context and Problem Statement" | 🟡 Basic | ✅ |
| smadr | "Context" | 🟡 Basic | ✅ |
| Tyree-Akerman | "Issue or Problem Statement" | ❌ | ✅ |
| Planguage | "Background" + "Impact" | ❌ | ✅ |
| Merson | "Context" | ❌ | ✅ |
| EdgeX | "Context" | 🟡 Basic | ✅ |
| DRF | `context.description` + `context.validation` | ✅ | ✅ |
| **adr-governance** | `context.description` (Markdown-native) | ✅ Full (Mermaid, code blocks) | ✅ |

**Rationale:** Present in every template surveyed (13/13) — the most universal ADR section alongside "Title." The Markdown-native type (supporting embedded Mermaid diagrams, code blocks, and rich formatting) enables architectural prose that goes beyond plain text. The `minLength: 20` constraint prevents stub contexts.

**Naming:** Originally `context.summary`; renamed to `context.description` to avoid confusion with the Y-Statement (which is the true decision "summary") and to use a more semantically accurate term for a problem narrative.

**Rejected alternatives:**
- *Separate "Problem Statement" and "Context" fields (MADR style)* — MADR 4.0 titles the section "Context and Problem Statement" suggesting these might be separate concerns. We merged them because: the problem statement *is* context, and separating them creates ambiguity about what goes where
- *`context.validation` field (DRF style)* — DRF adds a validation mechanism for checking whether the context is still accurate against organizational knowledge. Requires CRF infrastructure; deferred until DRF matures past v0.1.0
- *Plain text only (Nygard/Tyree-Akerman style)* — prevents embedding architectural diagrams. Mermaid sequence diagrams in context descriptions are among the most valuable visual aids in our example ADRs

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

**Precedent:**

| Template | Constraints concept | Structured? |
|---|---|---|
| Tyree-Akerman | ✅ Dedicated "Constraints" section | 🟡 Free-text |
| Planguage | ✅ "Constraints" keyword | 🟡 Free-text |
| Merson | 🟡 Informal in rationale | ❌ |
| DRF | ✅ Explicit field with "sourcing" | ✅ |
| MADR / Nygard / smadr | ❌ Absent | — |
| **adr-governance** | ✅ `context.constraints` array | ✅ Structured |

**Rationale:** Constraints bound the solution space and are non-negotiable — "we must use vendor X" or "deployment must be on-premises." Capturing them explicitly prevents evaluating alternatives that were never viable, and prevents future reviewers from asking "why didn't you consider Y?" when Y was constrained out.

**Rejected alternatives:**
- *Embed constraints in `context.description` prose (Nygard/MADR style)* — buries constraints in narrative where they're easy to miss. Structured arrays enable machine extraction ("what constraints apply to IAM decisions?") and explicit review during lifecycle checks
- *Typed constraints with categories (technical/regulatory/organizational)* — over-structures the field. A constraint like "must deploy on-premises" is simultaneously technical and regulatory. Categories would create classification debates without adding value
- *Required field* — not all decisions are externally constrained. Pure technology choices may have no non-negotiable constraints beyond team preferences

### 3.4 `context.assumptions`

| Attribute | Value |
|---|---|
| **Schema path** | `context.assumptions` |
| **Type** | `array` of strings |
| **Required?** | Optional |

**Precedent:**

| Template | Assumptions concept | Structured? |
|---|---|---|
| Tyree-Akerman | ✅ Dedicated "Assumptions" section | 🟡 Free-text |
| Planguage | ✅ "Assumptions" keyword | 🟡 Free-text |
| DRF | ✅ Explicit field | ✅ |
| MADR / Nygard / smadr | ❌ Absent | — |
| **adr-governance** | ✅ `context.assumptions` array | ✅ Structured array |

**Rationale:** Assumptions are the most dangerous hidden dependencies in any decision. "We assume the API gateway handles TLS termination" — if that assumption is wrong, the entire decision may be invalid. Explicit assumptions enable review ("is this assumption still true?") and serve as triggers for re-evaluation during lifecycle reviews.

**Rejected alternatives:**
- *Context Validation / CRF (DRF style)* — DRF proposes a Context Relevance Framework for validating assumptions against organizational knowledge graphs. Requires knowledge graph infrastructure that doesn't exist yet. Worth revisiting when DRF matures past v0.1.0.
- *Required field* — many operational decisions have no explicit assumptions worth documenting. Making it mandatory would produce noise ("we assume the internet exists")
- *Embed in `context.description` prose* — same argument as constraints: structured arrays enable machine extraction and explicit review during lifecycle checks

---

## Section 4: `architecturally_significant_requirements` — Requirement Traceability

### 4.0 `$defs/architecturally_significant_requirement` Reusable Type

| Attribute | Value |
|---|---|
| **Schema path** | `$defs/architecturally_significant_requirement` |
| **Type** | `object`: `id` (required, pattern: `^(F|NF)-[0-9]{3}$`), `description` (required, string) |
| **Used by** | `architecturally_significant_requirements.functional[]`, `.non_functional[]` |

**Rationale:** The ASR type is deliberately minimal — just `id` + `description`. This is a conscious design trade-off:

1. **Why `id`?** Enables cross-referencing ASRs from within `alternatives[].pros`, `alternatives[].cons`, `decision.rationale`, and `consequences`. Example: "Pro: Satisfies NF-002 (latency < 200ms)." Without IDs, cross-references become fragile text matches.

2. **Why the pattern `^(F|NF)-[0-9]{3}$`?** The `F-` / `NF-` prefix immediately communicates the requirement category without reading the description. Three digits (001–999) provide ample range per ADR — no known ADR has >50 requirements.

3. **Why per-ADR scoping?** Each ADR starts from F-001/NF-001. This avoids requiring a global requirement registry (which most teams don't have) and makes ADRs self-contained. The IDs are *local identifiers*, not globally unique — F-001 in ADR-0001 is unrelated to F-001 in ADR-0005.

4. **Why only `description`, not full QAS (6-part)?** The SEI Quality Attribute Scenario has 6 components (Source, Stimulus, Artifact, Environment, Response, Response Measure). Embedding all 6 in every ASR would make the ADR a requirements specification document rather than a decision record. A separate `measure` field was evaluated and rejected (see §4.2).

**Rejected alternatives:**
- *Full SEI QAS type (6 fields per requirement)* — over-structures ADRs into requirements documents. ADRs reference ASRs; they don't *specify* them
- *No `id` field (description only)* — prevents cross-referencing from other sections. "Satisfies NF-002" is more precise than "satisfies the latency requirement"
- *UUID or globally unique IDs* — requires a central registry. ADRs should be self-contained documents
- *Four-digit pattern (`F-0001`)* — no ADR realistically has >999 ASRs. Four digits add visual noise

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

**Rejected alternatives:**
- *No minimum (MADR/smadr style)* — allows single-option ADRs that are effectively fait accompli notifications rather than decision records
- *`minItems: 3` (force three options)* — overly prescriptive; for some decisions, two genuine alternatives is the reality. Forcing a third often produces a strawman option that wastes reviewer time

### 5.1.1 `alternatives[].name`

| Attribute | Value |
|---|---|
| **Schema path** | `alternatives[].name` |
| **Type** | `string` |
| **Required?** | ✅ Yes |

**Precedent:**

| Template | Alternative naming | Cross-referenced? |
|---|---|---|
| MADR 4.0 | Option titles (e.g., "Option 1 – Use Docker") | 🟡 Repeated in "Decision Outcome" |
| smadr | Option names | 🟡 Repeated |
| Tyree-Akerman | "Position" names | 🟡 Repeated |
| Business Case | "Candidate" names | 🟡 Repeated |
| **adr-governance** | `name` string, cross-referenced by `decision.chosen_alternative` | ✅ Name-matched |

**Rationale:** The name serves as the **human-readable identifier** for each alternative and is the key that `decision.chosen_alternative` references. Short, descriptive names ("DPoP", "mTLS", "BFF Token Mediator") enable scanning and comparison without reading full descriptions.

**Rejected alternatives:**
- *Numbered alternatives ("Alternative 1", "Alternative 2")* — generic numbers carry no semantic meaning. "DPoP" is immediately comprehensible; "Alternative 1" requires reading the description
- *No explicit name (description only)* — prevents concise cross-referencing from `decision.chosen_alternative`, pros/cons discussions, and Y-Statement composition
- *Slug-enforced naming pattern* — considered requiring `kebab-case` names for machine processing. Rejected because human-readable names ("BFF Token Mediator") are more important for ADR consumption than machine identifiers

### 5.2 `alternatives[].description` (Markdown-native)

| Attribute | Value |
|---|---|
| **Schema path** | `alternatives[].description` |
| **Type** | `string`, minLength: 20 (Markdown-native) |
| **Required?** | ✅ Yes |

**Precedent:** All templates that support alternatives have some form of description. MADR uses free-text per option; smadr has structured characteristics; Tyree-Akerman uses prose in "Positions." None explicitly require multi-paragraph architectural depth.

**Rationale:** Descriptions require **thorough** architectural explanation — not a one-liner, but multiple paragraphs with data flows, integration points, and ideally Mermaid diagrams. The `minLength: 20` prevents stubs. This field is explicitly documented as requiring the same depth as the ADR's context, ensuring rejected alternatives are described well enough for future teams to understand *what* was rejected and *could revisit it*.

**Rejected alternatives:**
- *Short description only (MADR "option title" style)* — a one-line description prevents future teams from understanding *what* was actually considered. The whole point of documenting alternatives is that someone might revisit them
- *Separate `description` and `architecture_diagram` fields* — over-structures the content. Markdown-native descriptions naturally support embedded Mermaid diagrams without a dedicated field

### 5.3 `alternatives[].pros` / `alternatives[].cons`

| Attribute | Value |
|---|---|
| **Schema path** | `alternatives[].pros`, `alternatives[].cons` |
| **Type** | `array` of strings (minItems: 1 each, minLength: 1 per item) |
| **Required?** | ✅ Yes |

**Precedent:**

| Template | Pros/Cons structure | Format |
|---|---|---|
| MADR 4.0 | "Good, because…" / "Bad, because…" | 🟡 Prefixed strings |
| smadr | Structured pros/cons per option | ✅ |
| NHS Wales | Structured evaluation | ✅ |
| Tyree-Akerman | Free-text in "Implications" | 🟡 |
| Nygard / Merson | ❌ Absent | — |
| **adr-governance** | `pros[]` + `cons[]` arrays (minItems: 1 each) | ✅ |

**Rationale:** Structured pros/cons force balanced evaluation. The `minItems: 1` constraints ensure that no option is presented as exclusively positive or negative — every real-world alternative has both.

**Rejected alternatives:**
- *MADR's three-way split (Good/Neutral/Bad)* — "Neutral" consequences are rarely informative and create authoring friction ("what goes in Neutral?"). The binary split is sufficient.
- *Weighted pros/cons (score per item)* — creates false precision. "How much does 'better security' weigh against 'slower deployment'?" These are incommensurable qualities best left to human judgment in the rationale.

### 5.4 `alternatives[].estimated_cost` / `alternatives[].risk`

| Attribute | Value |
|---|---|
| **Schema path** | `alternatives[].estimated_cost` (low/medium/high), `alternatives[].risk` (low/medium/high/critical) |
| **Required?** | Optional |

**Precedent:**

| Template | Per-option cost? | Per-option risk? | Risk dimensions |
|---|---|---|---|
| smadr | ❌ | ✅ 3D risk model | Technical / Schedule / Ecosystem |
| Business Case (Henderson) | ✅ SWOT with cost | ✅ SWOT with risk | SWOT matrix |
| MADR / Nygard / others | ❌ | ❌ | — |
| **adr-governance** | ✅ Enum (low/med/high) | ✅ Enum (low/med/high/critical) | Single dimension |

**Rationale:** Relative cost and risk enums provide machine-filterable decision metadata without requiring detailed financial analysis. An alternative with `estimated_cost: high` and `risk: critical` creates a very different decision context than `cost: low`, `risk: low`.

**Rejected alternatives:**
- *smadr's 3D risk model (Technical/Schedule/Ecosystem)* — interesting but our per-option `risk` field combined with pros/cons provides equivalent coverage with less schema complexity
- *SWOT per option (Business Case / Henderson)* — overlaps with pros/cons/cost/risk. SWOT is a management lens, not an engineering lens.
- *Numeric cost/risk (1–10)* — same false precision problem as numeric priority. Categorical labels are easier to reason about.

### 5.5 `alternatives[].rejection_rationale`

| Attribute | Value |
|---|---|
| **Schema path** | `alternatives[].rejection_rationale` |
| **Type** | `string` (Markdown-native) |
| **Required?** | Optional |

**Precedent:** Merson (explicit rationale for rejected alternatives in Rationale section), DRF (rejection reasoning in `synthesis`). No other template has per-option rejection reasoning.

**Rationale:** Pros/cons explain what's good and bad about each option. `rejection_rationale` explains **why this specific option was not chosen** — a more focused explanation that addresses the decision context rather than the option's abstract qualities. Future teams benefit most from knowing not just "what were the options" but "why didn't you pick this one?"

**Rejected alternatives:**
- *Mandatory rejection rationale for all alternatives* — the chosen alternative doesn't have a rejection rationale. Making it conditionally required (only for non-chosen alternatives) would require cross-field validation that JSON Schema can't express. Tooling-level enforcement is used instead.
- *Embed rejection reasoning in `cons` array* — conflates abstract disadvantages with the actual reason for rejection. An option's cons exist regardless of whether it was chosen; rejection rationale is decision-specific.

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

**Rejected alternatives:**
- *Index-based reference ("alternative #2")* — fragile; reordering the alternatives array breaks the reference
- *Prose-embedded choice (Nygard style)* — buries the decision in a paragraph; prevents programmatic extraction for dashboards and indexes
- *Schema-level cross-reference (`$ref` to alternatives array)* — JSON Schema 2020-12 cannot express "this string must match an `alternatives[].name` value." Tooling-level enforcement is the practical solution

### 6.2 `decision.rationale`

| Attribute | Value |
|---|---|
| **Schema path** | `decision.rationale` |
| **Type** | `string`, minLength: 20 (Markdown-native) |
| **Required?** | ✅ Yes |

**Precedent:**

| Template | Rationale section | Dedicated? | Markdown? |
|---|---|---|---|
| Nygard | Embedded in "Decision" prose | ❌ Combined | ❌ |
| MADR 4.0 | Embedded in "Decision Outcome" | ❌ Combined | 🟡 Basic |
| Merson | ✅ Dedicated "Rationale" section | ✅ | ❌ |
| Tyree-Akerman | ✅ "Justification" | ✅ | ❌ |
| smadr | Embedded in decision | ❌ Combined | 🟡 |
| **adr-governance** | ✅ `decision.rationale` (Markdown-native) | ✅ | ✅ Full |

**Rationale:** The rationale is the **most important field in the entire schema**. It answers "why" — the question that future architects will ask most often. Markdown-native formatting supports the depth this field deserves. Richards and Ford (*Fundamentals of Software Architecture*, 2020) explicitly advocate for rationale as the most important part of an ADR.

**Rejected alternatives:**
- *Embed rationale in `decision.chosen_alternative` prose (Nygard/MADR style)* — buries the "why" in a section primarily about the "what." Separating rationale makes it reviewable and searchable independently
- *Structured rationale (template with slots)* — rationale is inherently narrative; imposing structure would constrain the author's ability to build a coherent argument

### 6.3 `decision.tradeoffs`

| Attribute | Value |
|---|---|
| **Schema path** | `decision.tradeoffs` |
| **Type** | `string` (Markdown-native) |
| **Required?** | Optional |

**Precedent:**

| Template | Tradeoff concept | Dedicated field? |
|---|---|---|
| Y-Statements (Zimmermann) | "accepting that…" clause | ✅ Structural slot |
| MADR 4.0 | Informal in consequences | ❌ |
| Nygard | Implicit in prose | ❌ |
| **adr-governance** | `decision.tradeoffs` (Markdown-native) | ✅ |

**Rationale:** Every architectural decision involves tradeoffs — "we gained X but lost Y." Separating tradeoffs from rationale prevents the rationale from becoming defensive ("we chose X despite Y") and creates a clear space for acknowledging costs. This field maps directly to the "accepting that" clause in the Y-Statement.

**Rejected alternatives:**
- *Embed tradeoffs in `decision.rationale`* — conflates justification with acknowledged costs. Reviewers want to quickly scan "what are we giving up?" without parsing the rationale
- *Structured tradeoff matrix (gained/lost per quality attribute)* — over-structures the content. Tradeoffs are better expressed as narrative ("we accept higher latency in exchange for stronger isolation") than as cells in a matrix

### 6.4 `decision.decision_date`

| Attribute | Value |
|---|---|
| **Schema path** | `decision.decision_date` |
| **Type** | `string`, format: `date` |
| **Required?** | ✅ Yes |

**Precedent:** MADR has `date` in frontmatter. smadr, EdgeX change logs, and DRF `meta.created_at` all have dates. However, none distinguish *decision date* from *document creation date*.

**Rationale:** Distinct from `adr.created_at` — an ADR may be drafted on January 1 but the decision made on January 15. The decision date is the authoritative timestamp for "when was this decided?" which matters for compliance and lifecycle reviews.

**Rejected alternatives:**
- *Derive from `adr.created_at` or `adr.last_modified`* — conflates document lifecycle with decision lifecycle. An ADR may go through multiple draft iterations before the decision is actually made
- *ISO 8601 date-time (not just date)* — the exact time of a decision is rarely meaningful; decisions emerge from review processes, not at a precise moment. Date precision is sufficient and simpler for authors

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

**Precedent:**

| Template | Consequences section | Structure | Categories |
|---|---|---|---|
| Nygard | "Consequences" | 🟡 Flat prose | ❌ |
| MADR 4.0 | "Consequences" | ✅ Listed | Good / Neutral / Bad |
| smadr | "Consequences" | ✅ Listed | Positive / Negative |
| NHS Wales | "Consequences" | ✅ Listed | Positive / Negative |
| Merson | "Consequences" in rationale | 🟡 Informal | ❌ |
| **adr-governance** | `consequences.positive` / `.negative` | ✅ Separate arrays | Positive / Negative |

**Rationale:** The positive/negative split enables structured reasoning about outcomes. The `minProperties: 1` constraint ensures that consequences are not completely empty — at least one category must be populated.

**Rejected alternatives:**
- *Three-way split with "Neutral" (MADR style)* — excluded; neutral consequences are rarely informative and create authoring friction ("what's a neutral consequence?")
- *Categorized consequences (security/compliance/operational)* — evaluated and removed to keep ADRs focused on decisions rather than operational runbooks. See [template comparison §6.1](adr-template-comparison.md#61-no-template-has-structured-implications)
- *Single `consequences` array without polarity* — loses the structured positive/negative distinction that enables quick scanning ("what are we gaining? what are we losing?")
- *Markdown string (like rationale)* — prevents machine extraction. Consequences as structured arrays enable automated impact analysis across the ADR corpus

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

#### Literature Review: Architectural Decision Dependencies

**No other ADR template has explicit dependency tracking as a dedicated section.** This is entirely novel. However, the concept of inter-decision dependencies is well-established in architecture decision modeling literature. This section reviews the academic foundations, explains why existing models are too complex for practical ADRs, and justifies our deliberately simplified internal/external split.

##### 1. Academic Decision Relationship Models

###### Kruchten's Decision Network Graph (WICSA, 2004)

Kruchten defines 7 relationship types between architectural decisions:

| Relationship | Semantics | Directionality | Example |
|---|---|---|---|
| **Constrains** | D₁ restricts the choices available for D₂ | D₁ → D₂ | "Use J2EE" constrains app server to JBoss/WebSphere |
| **Forbids** | D₁ actively prevents D₂ from being made | D₁ → D₂ | "No stored procedures" forbids "Use stored proc for auth" |
| **Enables** | D₁ makes D₂ possible (weaker than constrains) | D₁ → D₂ | "Adopt microservices" enables "Independent deployment per team" |
| **Subsumes** | D₁ encompasses D₂ | D₁ → D₂ | "Use Kubernetes" subsumes "Use containers" |
| **Overrides** | D₁ supersedes D₂ | D₁ → D₂ | Captured by our `lifecycle.supersedes` |
| **Depends on** | D₁ requires D₂ to be valid | D₂ ← D₁ | "Use DPoP" depends on "Use OAuth 2.0" |
| **Is alternative for** | D₁ and D₂ are mutually exclusive options | D₁ ↔ D₂ | Captured by our `alternatives[]` within a single ADR |

**Assessment:** Kruchten's model is a **full ontology** designed for architectural knowledge management research tools. It models a directed graph of inter-decision relationships with typed edges. This is powerful for academic analysis but impractical for human-authored ADRs:
- Requires authors to classify *every* relationship with a specific semantic type
- Creates a dense dependency graph that needs specialized tooling to navigate
- "Constrains," "enables," and "depends on" are often difficult to distinguish in practice

###### Zimmermann's SOA Decision Models (2007–2012)

Zimmermann's framework models decisions as a DAG with:
- **Decomposition** relationships (high-level → specific)
- **Dependency** relationships (prerequisite → dependent)
- **Grouping** (decisions that are typically made together)

**Assessment:** The decomposition and grouping dimensions are partially captured by our `decision_level` (Strategic/Tactical/Operational hierarchy). The dependency dimension is what our `dependencies` field addresses — but Zimmermann models only *inter-decision* dependencies, not dependencies on external entities.

###### Jansen & Bosch — Decisions as First-Class Entities (WICSA, 2005)

Jansen & Bosch establish that architectural decisions have **tacit dependencies** that are often undocumented. Their key insight: most dependency information exists only in architects' heads and is lost during team transitions. Their solution: make dependency relationships explicit in architecture documentation.

**Assessment:** Our `dependencies` field is a direct response to this insight. We make dependencies explicit and portable — they travel with the ADR, not with the architect.

###### ISO/IEC/IEEE 42010:2022 — Correspondences

ISO 42010 uses **Correspondences** and **Correspondence Rules** to express relationships between architectural elements, including decisions. This is a formal mechanism for traceability:
- Stakeholder concern → architectural decision → architectural element
- Decision → decision (dependency, constraint, influence)

**Assessment:** ISO 42010's correspondence model is **schema-agnostic** — it defines that relationships *should* be documented but doesn't prescribe how. Our `dependencies` field is one concrete implementation of ISO 42010's correspondence concept.

##### 2. ADR Template Approaches

| Template | Dependency tracking | Mechanism | Relationship types |
|---|---|---|---|
| Nygard | ❌ Absent | — | — |
| MADR 4.0 | ❌ Absent | — | — |
| smadr | ❌ Absent | — | — |
| Tyree-Akerman | 🟡 "Related Decisions" | Prose list | Adjacency only (no typed relationships) |
| Planguage | ❌ Absent | — | — |
| EdgeX | 🟡 "Affected Services" | Product-specific list | Impact, not dependency |
| DRF | 🟡 Context Relevance Framework | Implicit in context | Not explicit |
| NHS Wales | 🟡 "More Information" | Prose cross-references | Unstructured |
| **adr-governance** | ✅ `dependencies.internal` + `.external` | **Structured, split by controllability** | Controllable vs. uncontrollable |

**Key finding:** Tyree-Akerman's "Related Decisions" is the closest precedent, but it tracks **adjacency** (these decisions are related) not **dependency** (this decision *requires* that thing). Our model captures directional dependency: "this ADR depends on X."

##### 3. The Controllability Classification

Our internal/external split is based on **controllability** — a concept from risk management and systems thinking:

| Dimension | `dependencies.internal` | `dependencies.external` |
|---|---|---|
| **Definition** | Dependencies on entities under organizational control | Dependencies on entities outside organizational control |
| **Examples** | Other ADRs, team APIs, internal services, platform teams | AWS services, vendor products, regulatory requirements, open-source libraries |
| **Risk profile** | Negotiable — you can escalate, schedule, or redesign | Non-negotiable — you must accept, work around, or abandon |
| **Impact of change** | Can trigger a superseding ADR via internal governance | May force a superseding ADR with no notice (vendor EOL, regulation change) |
| **Resolution path** | Internal coordination (sync meetings, RACI, roadmap alignment) | External monitoring (vendor roadmaps, regulatory calendars) |

**Why controllability, not Kruchten's 7 relationship types?** The primary purpose of dependency information in an ADR is **impact analysis**: "if X changes, what happens to this decision?" For impact analysis, the *type* of relationship (constrains vs. enables vs. depends on) matters less than whether the dependency is **within your control**:

```
Decision: Use DPoP for token binding
  internal: ["ADR-0003: Adopt OAuth 2.0 framework"]
    → If ADR-0003 changes, we can coordinate via our own governance process
  external: ["RFC 9449 (DPoP specification)", "AS vendor must support DPoP"]  
    → If RFC 9449 changes or vendor drops support, we react, not control
```

This two-bucket model captures **90% of the practical value** of Kruchten's full ontology with **10% of the authoring burden**.

##### 4. Why Not a Typed Dependency Graph?

We deliberately chose flat string arrays over a structured dependency model:

| Design | Schema complexity | Authoring burden | Tooling required | Practical value |
|---|---|---|---|---|
| **Kruchten-style typed edges** | High (relationship enum, source/target/type triples) | High (classify every relationship) | High (graph visualization) | High (for research) |
| **MADR-style prose cross-references** | Low (free text) | Low | Low | Low (not machine-parseable) |
| **Our string arrays** | Low (two arrays of strings) | Low (list what you depend on) | Low (grep, link validation) | **Medium-High** (controllability + impact analysis) |

The full Kruchten model would require:
```yaml
# What we DON'T do (too complex for human-authored ADRs):
dependencies:
  - target: "ADR-0003"
    relationship: "depends_on"
    strength: "strong"
    description: "Requires OAuth 2.0 as prerequisite"
  - target: "ADR-0005"
    relationship: "constrains" 
    strength: "weak"
    description: "Limits session management options"
```

Our model:
```yaml
# What we DO (simple, practical):
dependencies:
  internal:
    - "ADR-0003: Adopt OAuth 2.0 framework"
  external:
    - "RFC 9449 (DPoP specification)"
    - "Authorization Server vendor must support DPoP"
```

The simpler model is more likely to be populated by practitioners. An unpopulated complex model provides zero value; a populated simple model provides significant value.

##### 5. Relationship to Other Schema Fields

Several other schema fields capture dependency-adjacent concepts. Our `dependencies` field deliberately avoids duplicating them:

| Concept | Where captured | Why NOT in `dependencies` |
|---|---|---|
| **Supersession** (ADR replaces another) | `lifecycle.supersedes` / `lifecycle.superseded_by` | This is a *lifecycle transition*, not a dependency. The old ADR doesn't depend on the new one — it's replaced by it. |
| **Alternative exclusion** (choosing X means not Y) | `alternatives[]` within the same ADR | Mutual exclusion within a single decision is captured by alternative analysis, not inter-decision dependency. |
| **Constraint** (external limit on options) | `context.constraints` | Constraints describe the *problem space*. Dependencies describe *inter-decision relationships*. "Budget < $50k" is a constraint; "Requires ADR-0003 OAuth framework" is a dependency. |
| **Assumption** (uncertain belief) | `context.assumptions` | Assumptions may *become* dependencies once validated. "AWS will have eu-west-1 by Q4" is an assumption; once validated, "AWS eu-west-1 availability" goes in `dependencies.external`. |

#### Rejected Alternatives

- *No dependency tracking (Nygard/MADR approach)* — forces architects to maintain dependency knowledge in their heads. When team composition changes, dependency context is lost. Jansen & Bosch (2005) identified this as a critical knowledge management failure mode
- *Kruchten-style typed dependency graph* — too complex for human-authored ADRs. Requires relationship type classification, graph tooling, and introduces classification uncertainty ("is this 'constrains' or 'enables'?"). The controllability split captures most practical value with minimal burden
- *EdgeX-style structured impact assessment* — too specific to a single codebase. Our ADRs describe architectural patterns where impacted systems vary by adopter
- *Combined `dependencies` list (no internal/external split)* — loses the controllability distinction. "We depend on the IAM team" (negotiable, can be scheduled) vs. "we depend on AWS us-east-1" (non-negotiable, must accept) have fundamentally different risk profiles and resolution paths
- *Standalone `risk_assessment` section* — no ADR template has this as a standalone section. Risk is already distributed across `alternatives[].risk`, `alternatives[].cons`, `consequences.negative`, `decision.tradeoffs`, and `context.constraints`. A formal risk register belongs in threat models / ISMS artifacts, not in decision records
- *Required field* — not all decisions have explicit dependencies. Self-contained technology choices ("use Ed25519 for signing") may have no external or internal dependencies worth documenting
- *Structured objects with `id` + `description` + `type`* — adds schema complexity without proportional value. Free-text strings in two controllability-classified arrays hit the sweet spot of machine-parseable structure (array membership = controllability) with human-writable content (string = natural language description)
- *Bidirectional dependency tracking (both ADRs must reference each other)* — tempting (we do this for supersession), but too burdensome for dependencies. Supersession is a 1:1 relationship with clear symmetry; dependencies form a many-to-many DAG where bidirectional enforcement would require updating every depended-upon ADR whenever a new dependent ADR is created

#### Credits

| Concept | Source |
|---|---|
| 7 decision relationship types (constrains/forbids/enables/etc.) | Kruchten, "An Ontology of Architectural Design Decisions" (WICSA, 2004) |
| SOA decision decomposition and dependency graphs | Zimmermann et al., SOA Decision Models (2007–2012) |
| Tacit dependency knowledge loss during team transitions | Jansen & Bosch, "Software Architecture as a Set of Architectural Design Decisions" (WICSA, 2005) |
| Correspondences for architectural element relationships | ISO/IEC/IEEE 42010:2022 |
| "Related Decisions" adjacency concept | Tyree & Akerman, "Architecture Decisions" (IEEE Software, 2005) |
| Controllability-based risk classification | Systems thinking / risk management practice |
| Internal/external dependency split | adr-governance (novel) |

---

## Section 10: `references` — Evidence & Standards

### 10.1 `references[]`

| Attribute | Value |
|---|---|
| **Schema path** | `references[]` |
| **Type** | `array` of objects: `title` + `url` |
| **Required?** | Optional |

**Precedent:**

| Template | References section | Structured (title+URL)? |
|---|---|---|
| Nygard | 🟡 "Notes" (informal) | ❌ Free prose |
| MADR 4.0 | 🟡 "More Information" (links in prose) | ❌ Inline links |
| Tyree-Akerman | 🟡 "Related Artifacts" | ❌ Free-text |
| smadr | 🟡 "References" (Markdown links) | 🟡 |
| EdgeX | ✅ "References" section | 🟡 |
| **adr-governance** | ✅ `references[]` with `title` + `url` | ✅ |

**Rationale:** Structured references (title + URL) enable link validation and bibliography generation. RFCs, standards documents, vendor documentation, and research papers referenced in the decision rationale should be formally captured.

**Rejected alternatives:**
- *Unstructured prose links (MADR "More Information" style)* — prevents automated link checking and bibliography extraction
- *BibTeX-style citation format* — overly academic; architects are not researchers. Simple title + URL is sufficient for ADR contexts
- *Required field* — not all decisions reference external documents. Operational decisions ("use Ed25519 for signing") may be entirely self-contained
- *`title` + `url` + `type` (with category enum)* — considered adding a reference type (RFC, paper, vendor doc, internal wiki). Rejected because the categories are endless and the title is usually descriptive enough

---

## Section 11: `lifecycle` — Decision Management

#### Literature Review: Architectural Decision Lifecycle Management

The `lifecycle` block contains three sub-fields — review cadence, bidirectional supersession, and structured archival — all of which are **novel** in the ADR template landscape. This unified section reviews the academic foundations for decision lifecycle management and justifies each sub-field.

##### 1. The Decision Decay Problem

Architectural decisions have a **half-life**. Context changes, technologies evolve, teams turn over, and assumptions invalidate. Research on architectural decision staleness quantifies this:

| Finding | Source | Implication |
|---|---|---|
| 20–25% of architectural decisions had stale evidence within 2 months | Retrospective audit of projects using traditional ADRs (ReflectRally, 2024) | Decisions decay faster than most teams expect |
| Architectural decision staleness is a primary contributor to architectural technical debt | Architectural Decision Records with Evidence Decay Tracking (arXiv, 2024) | Decision maintenance is not optional — it's debt management |
| "ADR logs with more than 100 entries will probably put your readers to sleep" | Zimmermann (SATURN, 2012) | Long-lived repositories need lifecycle management to remain useful |
| "Good architecture allows major decisions to be deferred" | Robert C. Martin, *Clean Architecture* (2017) | Some decisions should explicitly wait — they need a `deferred` state |

Two academic traditions address this problem:

1. **Architectural Retrospectives** (Cervantes & Woods, InfoQ) — periodic review of accepted decisions to verify they're still valid, with structured retrospective questions
2. **After-Action Reviews** (Henderson) — post-implementation review to verify that decisions were implemented correctly and consequences matched predictions

Our `lifecycle` block provides the **schema-level infrastructure** for both practices.

##### 2. Multi-Template Lifecycle Feature Comparison

| Template | Review scheduling | Supersession linking | Archival | Lifecycle metadata? |
|---|---|---|---|---|
| Nygard | ❌ | 🟡 Inline prose ("Superseded by ADR-X") | ❌ | ❌ |
| MADR 4.0 | ❌ | 🟡 Inline prose in status header | ❌ | ❌ |
| smadr | ❌ | 🟡 Structured field | ❌ | 🟡 |
| Tyree-Akerman | ❌ | ❌ | ❌ | ❌ |
| Planguage | ❌ | ❌ | ❌ | ❌ |
| EdgeX | ❌ | 🟡 Change log entries | ❌ | 🟡 |
| NHS Wales | 🟡 Informal mention | 🟡 Inline prose | ❌ | ❌ |
| **adr-governance** | ✅ `review_cycle_months` + `next_review_date` | ✅ Bidirectional `supersedes` + `superseded_by` | ✅ `archival.archived_at` + `archive_reason` | ✅ |

**Key finding:** No template addresses all three lifecycle concerns. Most templates treat decisions as **write-once artifacts** that are either current or superseded, with no structured mechanisms for ongoing maintenance.

---

### 11.1 `lifecycle.review_cycle_months` / `lifecycle.next_review_date`

| Attribute | Value |
|---|---|
| **Schema path** | `lifecycle.review_cycle_months`, `lifecycle.next_review_date` |
| **Type** | `integer` (min: 1), `string` (date) |
| **Required?** | Optional |

##### Why Structured Review Cadence?

**No other template has structured review scheduling.** The concept exists as a *process recommendation* (Cervantes & Woods, Henderson) but never as a *schema field*. We schema-fy it because:

1. **Machine-readable review dates enable automation.** Without a structured field, review scheduling depends on human memory. With `next_review_date`, CI or external tooling can generate alerts: "3 ADRs are past their review date."
2. **Risk-based prioritization.** Combined with `decision.confidence`, review cadence becomes risk-proportional:

   | Confidence | Recommended `review_cycle_months` | Rationale |
   |---|---|---|
   | `low` | 6 | Decision made under pressure or with incomplete data — re-evaluate early |
   | `medium` | 12 | Standard review cycle |
   | `high` | 24 | Strong empirical evidence — extended cycle acceptable |

3. **Closing the lifecycle loop.** `review_cycle_months` triggers reviews; the `reviewed` event in `audit_trail` records that one occurred. This creates a verifiable review cadence: schedule → review → record → reschedule.

##### The Review Process (Not Schema-Enforced)

The schema captures *when* to review but not *how*. The review process is documented in `adr-process.md` §9 with 7 retrospective questions adapted from Cervantes & Woods:
1. Did the consequences we predicted actually occur?
2. Were there unforeseen consequences we should document?
3. Has the context changed since this decision was made?
4. Was the confidence level appropriate?
5. Have we accumulated technical debt from this decision?
6. Is this decision still the right choice given what we now know?
7. Should we trigger a superseding ADR?

This deliberate split — schema for scheduling, process doc for methodology — follows the principle that schemas should capture *data*, not *procedures*.

##### Rejected Alternatives

- *Review-as-process-only (no schema field)* — without machine-readable data, review scheduling depends on human memory. Automated CI reminders require structured fields
- *Single `next_review_date` without cycle* — loses the recurring nature of reviews. The cycle enables auto-computation of subsequent review dates after each review
- *Required field* — not all decisions need active review. Operational decisions with `confidence: high` may never need re-evaluation
- *Evidence decay tracking with TTL per evidence item* — promising academic concept (arXiv, 2024) but adds significant schema complexity. Each evidence claim would need its own expiration date, requiring structured evidence objects rather than prose. Future schema versions may adopt this if the concept matures
- *Automated review via CI (fail builds when review is overdue)* — too aggressive. Review dates are advisory, not blocking. A stale review date should generate a warning, not block deployments

---

### 11.2 `lifecycle.superseded_by` / `lifecycle.supersedes`

| Attribute | Value |
|---|---|
| **Schema path** | `lifecycle.superseded_by`, `lifecycle.supersedes` |
| **Type** | `string` or `null`, ADR ID pattern |
| **Required?** | Optional |

##### Why Bidirectional Supersession?

Every template that tracks supersession does so **unidirectionally** — the old ADR mentions the new one, but the new ADR doesn't formally link back. This creates a **broken navigation chain**:

```
Unidirectional (Nygard style):
  ADR-0003 [status: superseded, "see ADR-0008"]
  ADR-0008 [no reference to ADR-0003]
  → Finding ADR-0003 from ADR-0008 requires searching the entire corpus

Bidirectional (our model):
  ADR-0003 [superseded_by: "ADR-0008"]
  ADR-0008 [supersedes: "ADR-0003"]
  → Navigation works in both directions instantly
```

| Template | Supersession mechanism | Directionality | Structured? | CI-validated? |
|---|---|---|---|---|
| Nygard | Inline prose in status line | Old → New only | ❌ | ❌ |
| MADR 4.0 | Inline prose in status header | Old → New only | ❌ | ❌ |
| smadr | Structured field | 🟡 Partially bidirectional | ✅ | ❌ |
| EdgeX | Change log entries | Old → New only | 🟡 | ❌ |
| NHS Wales | Inline prose | Old → New only | ❌ | ❌ |
| **adr-governance** | `superseded_by` + `supersedes` | ✅ Fully bidirectional | ✅ | ✅ |

##### Symmetry Validation

The validator script enforces that supersession references are **symmetric**:
- If ADR-0003 has `lifecycle.superseded_by: "ADR-0008"`, then ADR-0008 must have `lifecycle.supersedes: "ADR-0003"`
- If either side is missing or mismatched, validation fails

This prevents orphaned supersession links — a common problem in long-lived ADR repositories where one side of the link is updated but the other is forgotten.

##### The Single-PR Supersession Rule

Supersession is the **only exception** to the single-ADR-per-PR rule (§3.4.2 in `adr-process.md`). A supersession PR must touch exactly two ADR files — the new and the old — to ensure atomic consistency:
- The new ADR (with `lifecycle.supersedes`)
- The old ADR (with `status: superseded` + `lifecycle.superseded_by`)

If either file were modified in a separate PR, there would be a window where the references are inconsistent.

##### Decision Chain Navigation

Bidirectional supersession enables **chain navigation** — tracing the evolution of a decision across multiple generations:

```
ADR-0001 [accepted] ← original decision
  └─ superseded_by: ADR-0003
      ADR-0003 [accepted] ← first revision
        └─ superseded_by: ADR-0008
            ADR-0008 [accepted] ← current decision
              └─ supersedes: ADR-0003
                  ADR-0003.supersedes: ADR-0001
```

A script or AI tool can traverse this chain in either direction to provide full decision history.

##### Rejected Alternatives

- *Unidirectional supersession (old → new only, Nygard style)* — navigating from new to old requires searching the entire corpus. Bidirectional references make the chain immediately traversable
- *Free-text supersession reference* — prevents validation. The ADR ID pattern constraint ensures the reference actually points to a valid ADR identifier
- *`related_adrs` / `attachments` (original schema)* — removed during schema refinement. ADR relationships are captured through `superseded_by`/`supersedes` for the most important relationship type (replacement). Other cross-references use `references` or prose in `context.description`
- *Multi-parent supersession (array of superseded ADRs)* — tempting for merge-style decisions where one new ADR replaces two old ones. Rejected because it complicates the symmetry rule (each old ADR's `superseded_by` points to one new ADR, but the new ADR's `supersedes` would need to be an array). Workaround: the new ADR supersedes the "primary" old ADR; the secondary old ADR is deprecated separately
- *Version bumping instead of supersession* — treating ADRs as mutable documents with version history (1.0 → 2.0 → 3.0). Violates the immutability principle: accepted decisions are frozen. Material changes require a new ADR with its own review cycle, not an anonymous edit

---

### 11.3 `lifecycle.archival`

| Attribute | Value |
|---|---|
| **Schema path** | `lifecycle.archival.archived_at`, `lifecycle.archival.archive_reason` |
| **Type** | `string` or `null` |
| **Required?** | Optional |

##### Why Structured Archival?

**No other template has archival as a structured concept.** Most templates treat `superseded` and `deprecated` as terminal — the ADR exists forever in the decision log with no visibility management. This doesn't scale:

| Repository Size | Active ADRs | Terminal ADRs | Problem |
|---|---|---|---|
| Small (< 20 ADRs) | ~15 | ~5 | No problem — all ADRs fit in one index |
| Medium (20–100 ADRs) | ~40 | ~60 | Terminal ADRs outnumber active ones; index becomes noisy |
| Large (100+ ADRs) | ~50 | ~100+ | "No more than 100 entries" (Zimmermann) — readers can't find what matters |

Archival solves this by providing a **visibility filter** orthogonal to status:

```
                     ┌─────────────┬────────────────┐
                     │  Not archived│   Archived     │
  ┌──────────────────┼─────────────┼────────────────┤
  │ accepted         │ ✅ Active    │ ❌ (accepted    │
  │                  │             │ can't be       │
  │                  │             │ archived)      │
  ├──────────────────┼─────────────┼────────────────┤
  │ superseded       │ In active   │ Hidden from    │
  │                  │ index       │ active index;  │
  │                  │ (may still  │ still query-   │
  │                  │ be useful)  │ able           │
  ├──────────────────┼─────────────┼────────────────┤
  │ deprecated       │ In active   │ Hidden from    │
  │                  │ index       │ active index   │
  ├──────────────────┼─────────────┼────────────────┤
  │ rejected         │ In active   │ Hidden from    │
  │                  │ index       │ active index   │
  └──────────────────┴─────────────┴────────────────┘
```

##### The Metadata Overlay Design

Archival is implemented as a **metadata overlay**, not an 8th status value. This is a key design decision documented in §1.4 (status deep research):

| Approach | Status query: "all superseded ADRs" | Visibility query: "all archived ADRs" | Both: "superseded but not archived" |
|---|---|---|---|
| `archived` as status | ❌ Misses archived-superseded ADRs | ✅ `status == archived` | ❌ Impossible — status is either `superseded` or `archived`, not both |
| **Metadata overlay** (our approach) | ✅ `status == superseded` (includes archived) | ✅ `archival.archived_at != null` | ✅ `status == superseded AND archival.archived_at == null` |

The overlay preserves **two independent query dimensions**: lifecycle outcome (what happened to this decision?) and visibility (should this appear in active listings?).

##### When to Archive

Archival is appropriate for ADRs in terminal states that no longer contribute to active decision-making:

| Terminal Status | Archive When | Example |
|---|---|---|
| `superseded` | Successor ADR is accepted **and** confirmed in production | ADR-0003 superseded by ADR-0008; ADR-0008 deployed and verified |
| `deprecated` | Replacement is fully operational or the technology is decommissioned | ADR-0001 deprecated; migrated off the deprecated framework |
| `rejected` | No longer relevant to revisit; team has moved on | ADR-0012 rejected 2 years ago; alternative technology chosen and stable |

##### Sub-Field Design

| Sub-field | Why it exists |
|---|---|
| `archived_at` | ISO 8601 timestamp — enables "when was this archived?" queries and provides a chronological record. Also serves as the boolean flag: `null` = not archived, non-null = archived. |
| `archive_reason` | Human-readable explanation. Critical for audit compliance: "why was this removed from active consideration?" Without a reason, archival could be misused to hide inconvenient decisions. |

##### Rejected Alternatives

- *Delete archived ADRs* — violates the principle that decision history should be immutable. Future teams may need to understand why a decision was made even if the decision is no longer active. "Never delete an ADR" is a core governance rule
- *Use `status: archived`* — considered adding an 8th status. Rejected because archival is orthogonal to status. See the metadata overlay analysis above for detailed justification
- *Archive by moving files to an `archive/` folder* — filesystem-level archival loses metadata (when, why) and breaks cross-references. An ADR referenced by `dependencies.internal` in another ADR would have a broken reference if the file moves
- *Soft-delete flag (boolean `archived: true`)* — simpler but loses the timestamp (when?) and reason (why?). Two structured fields provide meaningful audit data that a boolean cannot
- *Separate archival log (external to ADR file)* — creates a split-brain problem where the ADR file says one thing and the archival log says another. Embedding archival metadata in the ADR ensures the file is its own single source of truth

#### Credits (Section 11 — all three sub-fields)

| Concept | Source |
|---|---|
| Architectural retrospectives (periodic decision review) | Cervantes & Woods, "Architectural Retrospectives" (InfoQ) |
| After-action reviews for architecture | Henderson, software architecture maintenance practice |
| Decision decay / staleness as measurable concept | "ADRs with Evidence Decay Tracking" (arXiv, 2024) |
| "No more than 100 entries" heuristic | Zimmermann, SATURN 2012 |
| Decision immutability principle | Nygard, "Documenting Architecture Decisions" (2011) |
| Bidirectional supersession with symmetry validation | adr-governance (novel) |
| Structured review cadence as schema field | adr-governance (novel) |
| Archival as metadata overlay vs. status value | adr-governance (novel) |
| Risk-based review frequency tied to confidence | adr-governance (novel) |

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

**Precedent:**

| Standard/Template | Extension mechanism |
|---|---|
| OpenAPI 3.x | `x-` prefix for vendor extensions (the original inspiration) |
| HTTP Headers | `X-` prefix convention (deprecated in RFC 6648, but widely understood) |
| smadr | ✅ Pioneered `x-` prefix for ADR extensions |
| **adr-governance** | ✅ `patternProperties: "^x-"` (schema-validated) |

**Rationale:** Organizations have unique metadata needs (project codes, CMDB references, deployment regions, cost center IDs). Extension fields allow any `x-`-prefixed field without breaking schema validation — enabling customization without forking the schema.

**Rejected alternatives:**
- *`metadata` catch-all object* — creates an unstructured dumping ground. The `x-` prefix makes extensions visible and namespaced
- *Fork the schema for custom fields* — creates divergence. Forked schemas can't be validated against the original, breaking tooling interoperability
- *No extensions (strict schema only)* — too rigid for real-world adoption. Organizations will add custom fields regardless; better to provide a sanctioned mechanism

### 13.2 `additionalProperties: false`

Every object in the schema sets `additionalProperties: false`. This is a deliberate strictness choice — typos and undocumented fields are caught at validation time rather than silently accepted. Extension fields use the `x-` escape hatch.

**Rejected alternatives:**
- *`additionalProperties: true` (permissive)* — silently accepts typos and undocumented fields. A field named `desciption` (typo) would pass validation and never be rendered. Strictness catches these at authoring time.
- *Per-object `additionalProperties` (mixed)* — inconsistent developer experience. All-or-nothing strictness is easier to understand and maintain.

### 13.3 Conditional Requirements (`allOf/if/then`)

The schema uses JSON Schema 2020-12 conditional logic to enforce:
- When `status` is `proposed` or `accepted`, `approvals` is required with at least one entry, and each approval must have an `identity` field.

This enables a **progressive strictness** model — drafts are loose, proposed/accepted ADRs are strict.

**Rejected alternatives:**
- *Always-strict (require approvals for all statuses)* — blocks authors from creating drafts. The progressive model mirrors the natural ADR lifecycle: sketch → propose → approve.
- *No conditional requirements (always-optional approvals)* — defeats the purpose of governance. Accepted ADRs without approvals have no accountability.
- *Custom validation only (not schema-level)* — JSON Schema's `allOf/if/then` is the standard mechanism for conditional logic. Schema-level enforcement ensures any validator (AJV, Python jsonschema, IDE plugins) enforces the rule without custom code.

---

## Sources

Consolidated bibliography of all sources referenced across sections. Sections §1.11, §4.2, and §4.3 also include per-section credits for their deep research.

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
