# Implementation Plan — ADR Governance Fixes

> **Created:** 2026-03-06
> **Status:** In Progress

## Tracker

| # | Issue | Severity | Status |
|---|-------|----------|--------|
| 1 | Remove stale `related_adrs` refs from SKILL.md, process doc, SCHEMA_REFERENCE.md, research docs | 🔴 Stale | ⬜ TODO |
| 2 | Rewrite `adr-process.md` §5 supersession YAML example (uses removed `related_adrs`) | 🔴 Broken | ⬜ TODO |
| 3 | README says "6 example ADRs" — should be 7 | 🟡 Cosmetic | ⬜ TODO |
| 4 | Template says audit_trail is "REQUIRED" but schema says optional — align | 🟡 Confusing | ⬜ TODO |
| 5 | `consequences` allows empty `{}` despite being required — add minProperties or anyOf | 🟡 Weak validation | ⬜ TODO |
| 6 | ADR-0000 self-approval violates §3.4 "no self-approval" rule — add exception note | 🟡 Bootstrap | ⬜ TODO |
| 7 | No strict warning for missing `adr.summary` on proposed/accepted ADRs | 🟢 Enhancement | ⬜ TODO |
| 8 | `decision.rationale` minLength 1 is too permissive — raise to 20 | 🟢 Enhancement | ⬜ TODO |
| 9 | No temporal ordering check on audit_trail events | 🟢 Enhancement | ⬜ TODO |
| 10 | CODEOWNERS example patterns may not work — add caveat | 🟢 Documentation | ⬜ TODO |
| 11 | ADR-0007 `status: rejected` with `chosen_alternative` — clarify semantics in process doc | 🟡 Ambiguous | ⬜ TODO |
| 12 | `adr.version` description says "Semantic version" but uses MAJOR.MINOR — fix desc | 🟢 Cosmetic | ⬜ TODO |
| 13 | Schema `$id` has unconventional `/1.0.0` suffix — fix URI | 🟢 Cosmetic | ⬜ TODO |
| 14 | Strict mode: warn if accepted ADR has no approval with timestamp | 🟢 Enhancement | ⬜ TODO |
| 15 | Strict mode: warn if `confidence` set on draft ADR | 🟢 Enhancement | ⬜ TODO |
| 16 | Validator: check `decision_date` within `created_at` → `last_modified` range | 🟢 Enhancement | ⬜ TODO |

## Phases

### Phase 1: Stale reference cleanup (Issues 1, 2)
### Phase 2: Schema hardening (Issues 5, 8, 12, 13)
### Phase 3: Documentation fixes (Issues 3, 4, 6, 10, 11)
### Phase 4: Validator enhancements (Issues 7, 9, 14, 15, 16)
### Phase 5: Validate & commit
