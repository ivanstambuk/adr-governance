# Example ADRs — Reference Collection

This directory contains two reference sets demonstrating the ADR meta-model at different scales and contexts.

> **Namespace note:** The shipped [`scripts/run-validation.sh`](../scripts/run-validation.sh) flow validates these examples separately from `architecture-decision-log/`, so keeping the reference set does **not** reserve live ADR IDs by default. If you explicitly validate both directories in a single [`scripts/validate-adr.py`](../scripts/validate-adr.py) invocation, they share a duplicate-ID and cross-reference namespace for that run.

---

## Fictional Examples (`fictional/`)

> ⚠️ **These are fictional examples, not real architectural decisions.**

The ADRs in `fictional/` are from a fictional organisation called **NovaTrust Financial Services**. They demonstrate the ADR meta-model using realistic Identity and Access Management (IAM) scenarios with contended alternatives, sizable pros and cons on each side, and interconnected decisions.

**Use these to:**
- Understand what a well-formed ADR looks like
- See how the schema fields work together (context → alternatives → decision → consequences → confirmation)
- Study interconnected decisions (e.g., ADR-0002 references ADR-0001's DPoP decision)
- Train AI agents on the expected quality level
- Test validation tooling ([`scripts/validate-adr.py`](../scripts/validate-adr.py))

| ADR | Decision | Status | Domain | Rendered | Source |
|-----|----------|--------|--------|:--------:|:------:|
| ADR-0001 | DPoP over mTLS for sender-constrained tokens | Accepted | OAuth 2.1 | [Markdown](rendered/ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.md) | [YAML](fictional/ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.yaml) |
| ADR-0002 | Opaque reference tokens over JWTs | Accepted | Token format | [Markdown](rendered/ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.md) | [YAML](fictional/ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.yaml) |
| ADR-0003 | Pairwise pseudonymous subject identifiers | Accepted | OIDC privacy | [Markdown](rendered/ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.md) | [YAML](fictional/ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.yaml) |
| ADR-0004 | Ed25519 over RSA for JWT signing | Accepted | Cryptography | [Markdown](rendered/ADR-0004-ed25519-over-rsa-for-jwt-signing.md) | [YAML](fictional/ADR-0004-ed25519-over-rsa-for-jwt-signing.yaml) |
| ADR-0005 | BFF token mediator for SPA | Accepted | Frontend auth | [Markdown](rendered/ADR-0005-bff-token-mediator-for-spa-token-acquisition.md) | [YAML](fictional/ADR-0005-bff-token-mediator-for-spa-token-acquisition.yaml) |
| ADR-0006 | Session enrichment for step-up auth | Accepted | Step-up | [Markdown](rendered/ADR-0006-session-enrichment-for-step-up-authentication.md) | [YAML](fictional/ADR-0006-session-enrichment-for-step-up-authentication.yaml) |
| ADR-0007 | Reject centralized HashiCorp Vault | **Rejected** | Secrets mgmt | [Markdown](rendered/ADR-0007-centralized-secret-store-for-api-keys.md) | [YAML](fictional/ADR-0007-centralized-secret-store-for-api-keys.yaml) |
| ADR-0008 | Defer OpenID Federation | **Deferred** | Trust establishment | [Markdown](rendered/ADR-0008-defer-openid-federation-for-trust-establishment.md) | [YAML](fictional/ADR-0008-defer-openid-federation-for-trust-establishment.yaml) |

---

## Real-World Examples (`real-world/`)

The ADRs in `real-world/` are **reverse-engineered** from prominent open-source project decisions. Each ADR reconstructs the decision as it would have been captured at decision time, using primary sources (RFCs, KEPs, blog posts, conference talks, community discussions).

**Use these to:**
- See how the schema handles real architectural decisions at scale — including multi-year design evolutions, community controversy, and competitive dynamics
- Study the full range of decision levels: **Strategic** (language/platform), **Tactical** (API/tooling), **Operational** (configuration/infrastructure)
- Learn from rich alternatives analysis with Mermaid diagrams, comparison tables, code examples, and empirical evidence
- Benchmark ADR quality — each ADR was validated against the schema and refined through a 15-ADR retrospective improvement loop

### Strategic Decisions (ADR-0100 – ADR-0104)

| ADR | Project | Decision | Rendered | Source |
|-----|---------|----------|:--------:|:------:|
| ADR-0100 | **TypeScript** | Rewrite compiler in Go | [Markdown](rendered/ADR-0100-typescript-compiler-go-rewrite.md) | [YAML](real-world/ADR-0100-typescript-compiler-go-rewrite.yaml) |
| ADR-0101 | **Kubernetes** | Deprecate dockershim for CRI | [Markdown](rendered/ADR-0101-kubernetes-dockershim-deprecation.md) | [YAML](real-world/ADR-0101-kubernetes-dockershim-deprecation.yaml) |
| ADR-0102 | **React** | Server Components (RFC 0188) | [Markdown](rendered/ADR-0102-react-server-components.md) | [YAML](real-world/ADR-0102-react-server-components.yaml) |
| ADR-0103 | **Go** | Add generics via type parameters | [Markdown](rendered/ADR-0103-go-generics.md) | [YAML](real-world/ADR-0103-go-generics.yaml) |
| ADR-0104 | **Rust** | Async/await with stackless coroutines | [Markdown](rendered/ADR-0104-rust-async-await.md) | [YAML](real-world/ADR-0104-rust-async-await.yaml) |

### Tactical Decisions (ADR-0105 – ADR-0109)

| ADR | Project | Decision | Rendered | Source |
|-----|---------|----------|:--------:|:------:|
| ADR-0105 | **Vue.js** | Composition API (RFC-0013) | [Markdown](rendered/ADR-0105-vue-composition-api.md) | [YAML](real-world/ADR-0105-vue-composition-api.yaml) |
| ADR-0106 | **ESLint** | Flat config system | [Markdown](rendered/ADR-0106-eslint-flat-config.md) | [YAML](real-world/ADR-0106-eslint-flat-config.yaml) |
| ADR-0107 | **Vite** | Rolldown unification | [Markdown](rendered/ADR-0107-vite-rolldown-unification.md) | [YAML](real-world/ADR-0107-vite-rolldown-unification.yaml) |
| ADR-0108 | **Svelte** | Runes reactivity system | [Markdown](rendered/ADR-0108-svelte-runes-reactivity.md) | [YAML](real-world/ADR-0108-svelte-runes-reactivity.yaml) |
| ADR-0109 | **Next.js** | Turbopack adoption | [Markdown](rendered/ADR-0109-nextjs-turbopack-adoption.md) | [YAML](real-world/ADR-0109-nextjs-turbopack-adoption.yaml) |

### Operational Decisions (ADR-0110 – ADR-0114)

| ADR | Project | Decision | Rendered | Source |
|-----|---------|----------|:--------:|:------:|
| ADR-0110 | **Node.js** | Built-in test runner | [Markdown](rendered/ADR-0110-nodejs-built-in-test-runner.md) | [YAML](real-world/ADR-0110-nodejs-built-in-test-runner.yaml) |
| ADR-0111 | **Python** | pyproject.toml (PEP 621) | [Markdown](rendered/ADR-0111-python-pyproject-toml.md) | [YAML](real-world/ADR-0111-python-pyproject-toml.yaml) |
| ADR-0112 | **Docker** | Container base image selection | [Markdown](rendered/ADR-0112-container-base-image-selection.md) | [YAML](real-world/ADR-0112-container-base-image-selection.yaml) |
| ADR-0113 | **pnpm** | Content-addressable store | [Markdown](rendered/ADR-0113-pnpm-content-addressable-store.md) | [YAML](real-world/ADR-0113-pnpm-content-addressable-store.yaml) |
| ADR-0114 | **Deno** | npm compatibility layer | [Markdown](rendered/ADR-0114-deno-npm-compatibility.md) | [YAML](real-world/ADR-0114-deno-npm-compatibility.yaml) |

---

**Do not** treat these as your organization's decisions. When adopting this framework, you can keep this directory as a reference or delete it — your real ADRs go in `architecture-decision-log/`.
