# ADR Governance — Glossary

## Core Concepts

| Term | Definition |
|------|-----------|
| **ADR** | Architecture Decision Record. A structured document capturing a significant architectural decision, its context, alternatives considered, and consequences. |
| **ADR Administrator** | A person listed in [`.adr-governance/config.yaml`](../.adr-governance/config.yaml) who is authorised to make maintenance (Tier 2) changes to any ADR without requiring re-approval from the original ADR approvers. See [`adr-process.md` §3.4.4](adr-process.md#344-adr-administrators). |
| **Approval Identity Rule** | Governance rule stating that every person listed in an ADR's `approvals[]` must have actually approved the associated pull request. Enforced via the `identity` field and CI validation. See `adr-process.md` §3.4.1. |
| **ASR** | Architecturally Significant Requirement. A requirement (functional or non-functional) that directly shapes or constrains the architecture. |
| **Change Classification** | The categorisation of ADR changes as either *substantive* (Tier 1 — requires original approver re-approval) or *maintenance* (Tier 2 — no re-approval required). See `adr-process.md` §3.4.3. |
| **Decision Owner** | The single accountable individual responsible for the final decision. Not necessarily the author. |
| **Identity** | The `approvals[].identity` field — a platform-resolvable handle (e.g., GitHub `@username`, Azure DevOps email) that CI pipelines use to verify the approver actually approved the pull request. |
| **Maintenance Change** | A Tier 2 change to an ADR that does not alter the architectural decision itself (e.g., typo fix, email correction, schema version bump). Does not require re-approval from original ADR approvers. |
| **Residual Risk** | The risk remaining after all identified mitigations have been applied. |
| **Single ADR per PR** | Governance rule requiring that each pull request modifies at most one ADR file. Exception: supersession pairs (new + old ADR). See `adr-process.md` §3.4.2. |
| **Substantive Change** | A Tier 1 change to an ADR that modifies the decision itself (e.g., status, rationale, alternatives, consequences). Requires re-approval from the original ADR approvers. |
| **Supersession** | When a new ADR replaces a previous one. The old ADR's status changes to `superseded` and the `lifecycle.superseded_by` field points to the replacement. |

## ADR Status Values

| Status | Meaning |
|--------|---------|
| `draft` | ADR is being authored. Not ready for review. |
| `proposed` | ADR is complete and under review. Not yet binding. |
| `accepted` | Decision has been formally approved and is in effect. |
| `superseded` | Replaced by a newer ADR (see `lifecycle.superseded_by`). |
| `deprecated` | Still technically active but no longer recommended. Will be superseded or rejected. |
| `rejected` | Explicitly rejected after evaluation. Preserved for historical record. |
| `deferred` | Decision postponed. Context or drivers are insufficient to decide now. |

> **Note:** `archived` is **not a status value** — it is a metadata overlay tracked via `lifecycle.archival` fields (`archived_at`, `archive_reason`) and the `archived` event in `audit_trail`. Archived ADRs retain their pre-archival status (`superseded`, `deprecated`, or `rejected`).

## Decision Type Classification

| Type | Description |
|------|-------------|
| `technology` | Selection of specific tools, frameworks, languages, databases, or platforms. |
| `process` | Changes to development, deployment, or operational workflows. |
| `organizational` | Team structure, ownership boundaries, or responsibility changes. |
| `vendor` | Third-party vendor or managed service selection and contracts. |
| `security` | Security controls, authentication/authorization mechanisms, key management. |
| `compliance` | Regulatory compliance, data residency, audit, and reporting decisions. |

## Priority Levels

| Level | Guidance |
|-------|----------|
| `low` | Localized impact. Reversible with minimal effort. |
| `medium` | Affects multiple components or teams. Moderate effort to reverse. |
| `high` | Cross-cutting decision. Significant effort and coordination to change. |
| `critical` | Foundational. Reversal would require major re-architecture or breach regulations. |

## Risk & Impact Scales

| Value | Likelihood Meaning | Impact Meaning |
|-------|--------------------|----|
| `low` | Unlikely to occur within the review cycle | Minor disruption; workarounds exist |
| `medium` | May occur; has happened in similar contexts | Noticeable service degradation; requires response |
| `high` | Likely to occur given current conditions | Significant outage, data loss, or compliance breach |
| `critical` | *(impact only)* | Catastrophic: regulatory penalties, major data breach, or total service loss |

## Decision Confidence Levels

| Level | Guidance |
|-------|---------|
| `low` | Decision made under time pressure or with incomplete information. Flag for early re-evaluation. |
| `medium` | Reasonable confidence based on available evidence. Standard review cycle. |
| `high` | Strong empirical evidence (PoC, benchmarks, prior experience). Extended review cycle acceptable. |

> **Confidence on rejected ADRs:** Confidence applies to the *decision outcome*, not the proposal. A `rejected` ADR with `confidence: high` means the team is highly confident in the rejection (e.g., strong evidence that the proposed approach is wrong). A rejected ADR with `confidence: low` means the rejection was made under uncertainty and may warrant re-evaluation.


## ID Formats

| Entity | Pattern | Example |
|--------|---------|---------|
| ADR | `ADR-NNNN-slug` (slug is mandatory) | `ADR-0001-dpop-over-mtls` |
| Functional Requirement | `F-NNN` | `F-001` |
| Non-Functional Requirement | `NF-NNN` | `NF-001` |

## ADR Supersession (Lifecycle)

Supersession is tracked via `lifecycle.supersedes` and `lifecycle.superseded_by` fields.

- **`lifecycle.supersedes`** — ADR ID that this decision replaces (set on the **new** ADR).
- **`lifecycle.superseded_by`** — ADR ID that replaces this decision (set on the **old** ADR).

> Both fields must be set symmetrically when one ADR supersedes another. The validator checks this.

## Deprecation vs. Archival Timestamps

| Action | Timestamp location | Notes |
|--------|--------------------|-------|
| **Deprecation** | `audit_trail` → `deprecated` event `at` field | Deprecation has no dedicated lifecycle field — query the audit trail for timing. |
| **Archival** | `lifecycle.archival.archived_at` | Archival has a dedicated field because it is a terminal, queryable state. |



## Audit Trail Events

| Event | When Recorded |
|-------|---------------|
| `created` | Initial draft committed. |
| `updated` | Material change to decision, alternatives, or consequences. |
| `approved` | Formal approval by a named authority. |
| `rejected` | Decision explicitly rejected. |
| `deferred` | Decision postponed — context or drivers insufficient to decide now. |
| `reviewed` | Periodic review completed. Decision re-evaluated against current context. |
| `superseded` | Replaced by a newer ADR. |
| `deprecated` | Marked as no longer recommended. |
| `archived` | Removed from active consideration. |

## Abbreviations

| Abbreviation | Full Form |
|--------------|-----------|
| AD | Architecture Decision |
| ADL | Architecture Decision Log |
| ADR | Architecture Decision Record |
| AKM | Architecture Knowledge Management |
| DPO | Data Protection Officer |
| HA | High Availability |
| HSM | Hardware Security Module |
| IAM | Identity and Access Management |
| IdP | Identity Provider |
| KMS | Key Management Service |
| MFA | Multi-Factor Authentication |
| OIDC | OpenID Connect |
| RBAC | Role-Based Access Control |
| RPO | Recovery Point Objective |
| RTO | Recovery Time Objective |
| SLA | Service Level Agreement |
| SSO | Single Sign-On |
| TLS | Transport Layer Security |
