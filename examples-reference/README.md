# Example ADRs — Reference Only

> ⚠️ **These are fictional examples, not real architectural decisions.**

The ADRs in this directory are from a fictional organisation called **NovaTrust Financial Services**. They demonstrate the ADR meta-model using realistic Identity and Access Management (IAM) scenarios with contended alternatives, sizable pros and cons on each side, and interconnected decisions.

**Use these to:**
- Understand what a well-formed ADR looks like
- See how the schema fields work together (context → alternatives → decision → consequences → confirmation)
- Study interconnected decisions (e.g., ADR-0002 references ADR-0001's DPoP decision)
- Train AI agents on the expected quality level
- Test validation tooling ([`scripts/validate-adr.py`](../scripts/validate-adr.py))

**Do not** treat these as your organization's decisions. When adopting this framework, you can keep this directory as a reference or delete it — your real ADRs go in `architecture-decision-log/`.

## Example Decisions

| ADR | Decision | Status | Domain | Rendered | Source |
|-----|----------|--------|--------|:--------:|:------:|
| ADR-0001 | DPoP over mTLS for sender-constrained tokens | Accepted | OAuth 2.1 | [Markdown](rendered/ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.md) | [YAML](ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.yaml) |
| ADR-0002 | Opaque reference tokens over JWTs | Accepted | Token format | [Markdown](rendered/ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.md) | [YAML](ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.yaml) |
| ADR-0003 | Pairwise pseudonymous subject identifiers | Accepted | OIDC privacy | [Markdown](rendered/ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.md) | [YAML](ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.yaml) |
| ADR-0004 | Ed25519 over RSA for JWT signing | Accepted | Cryptography | [Markdown](rendered/ADR-0004-ed25519-over-rsa-for-jwt-signing.md) | [YAML](ADR-0004-ed25519-over-rsa-for-jwt-signing.yaml) |
| ADR-0005 | BFF token mediator for SPA | Accepted | Frontend auth | [Markdown](rendered/ADR-0005-bff-token-mediator-for-spa-token-acquisition.md) | [YAML](ADR-0005-bff-token-mediator-for-spa-token-acquisition.yaml) |
| ADR-0006 | Session enrichment for step-up auth | Accepted | Step-up | [Markdown](rendered/ADR-0006-session-enrichment-for-step-up-authentication.md) | [YAML](ADR-0006-session-enrichment-for-step-up-authentication.yaml) |
| ADR-0007 | Reject centralized HashiCorp Vault | **Rejected** | Secrets mgmt | [Markdown](rendered/ADR-0007-centralized-secret-store-for-api-keys.md) | [YAML](ADR-0007-centralized-secret-store-for-api-keys.yaml) |
| ADR-0008 | Defer OpenID Federation | **Deferred** | Trust establishment | [Markdown](rendered/ADR-0008-defer-openid-federation-for-trust-establishment.md) | [YAML](ADR-0008-defer-openid-federation-for-trust-establishment.yaml) |

