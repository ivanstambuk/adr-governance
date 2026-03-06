# Example ADRs — Reference Only

> ⚠️ **These are fictional examples, not real architectural decisions.**

The ADRs in this directory are from a fictional organisation called **NovaTrust Financial Services**. They demonstrate the ADR meta-model using realistic Identity and Access Management (IAM) scenarios with contended alternatives, sizable pros and cons on each side, and interconnected decisions.

**Use these to:**
- Understand what a well-formed ADR looks like
- See how the schema fields work together (context → alternatives → decision → consequences → confirmation)
- Study interconnected decisions (e.g., ADR-0002 references ADR-0001's DPoP decision)
- Train AI agents on the expected quality level
- Test validation tooling (`scripts/validate-adr.py`)

**Do not** treat these as your organization's decisions. When adopting this framework, you can keep this directory as a reference or delete it — your real ADRs go in `architecture-decision-log/`.

## Example Decisions

| ADR | Decision | Status | Domain |
|-----|----------|--------|--------|
| ADR-0001 | DPoP over mTLS for sender-constrained tokens | Accepted | OAuth 2.1 |
| ADR-0002 | Opaque reference tokens over JWTs | Accepted | Token format |
| ADR-0003 | Pairwise pseudonymous subject identifiers | Accepted | OIDC privacy |
| ADR-0004 | Ed25519 over RSA for JWT signing | Accepted | Cryptography |
| ADR-0005 | BFF token mediator for SPA | Accepted | Frontend auth |
| ADR-0006 | Session enrichment for step-up auth | Accepted | Step-up |
| ADR-0007 | Reject centralized HashiCorp Vault | **Rejected** | Secrets mgmt |
| ADR-0008 | Defer OpenID Federation | **Deferred** | Trust establishment |
