# adr-governance

A schema-governed, AI-assisted Architecture Decision Record (ADR) workflow for enterprise teams.

## Overview

This repository provides a **self-contained, YAML-based ADR meta-model** with:

- **JSON Schema** (Draft 2020-12) defining the complete ADR structure
- **Agent Skill** ([agentskills.io](https://agentskills.io) spec) for AI-assisted ADR authoring and review
- **Validation tooling** (Python script + GitHub Actions CI)
- **Repomix bundling** for LLM context injection
- **6 example ADRs** from a fictional IAM department (NovaTrust Financial Services) — low-level implementation decisions with contended alternatives

## Philosophy

Every ADR is **self-contained**. All context, requirements, alternatives, risk assessment, compliance implications, and audit trails are embedded directly in the YAML file. Related ADRs are cross-referenced by ID but never structurally depended upon.

## Quick Start

### 1. Create a new ADR

Copy the template and fill in all required sections:

```bash
cp .skills/adr-author/assets/adr-template.yaml decisions/ADR-0007-your-title.yaml
```

Or use an AI assistant with the `adr-author` skill installed.

### 2. Validate

```bash
pip install jsonschema pyyaml
python3 scripts/validate-adr.py decisions/ADR-0007-your-title.yaml
```

### 3. Submit a PR

The GitHub Actions workflow will automatically validate your ADR against the schema and lint the YAML.

## Directory Structure

```
.
├── schemas/
│   └── adr.schema.json          # JSON Schema (Draft 2020-12) for ADRs
├── docs/
│   └── glossary.md              # Terms, enum values, abbreviations
├── decisions/                   # Your ADRs go here (initially empty)
├── examples/                    # 6 well-formed example ADRs
│   ├── ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.yaml
│   ├── ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.yaml
│   ├── ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.yaml
│   ├── ADR-0004-ed25519-over-rsa-for-jwt-signing.yaml
│   ├── ADR-0005-bff-token-mediator-for-spa-token-acquisition.yaml
│   └── ADR-0006-session-enrichment-for-step-up-authentication.yaml
├── .skills/
│   └── adr-author/              # Agent Skill (agentskills.io spec)
│       ├── SKILL.md             # Skill instructions
│       ├── assets/
│       │   └── adr-template.yaml
│       └── references/
│           ├── GLOSSARY.md
│           └── SCHEMA_REFERENCE.md
├── scripts/
│   ├── validate-adr.py          # Schema validation script
│   └── bundle.sh                # Repomix bundling script
├── .github/
│   └── workflows/
│       └── validate-adr.yml     # PR validation CI
└── repomix.config.json          # Bundles core project (excludes examples + CI)
```

## ADR Meta-Model

Each ADR YAML file contains these sections:

| Section | Required | Description |
|---------|----------|-------------|
| `adr` | ✅ | ID, title, status, timestamps, project, tags, priority, decision type |
| `authors` | ✅ | Who drafted the ADR |
| `decision_owner` | ✅ | Single accountable person |
| `context` | ✅ | Problem summary, business/technical drivers, constraints, assumptions |
| `alternatives` | ✅ | At least 2 alternatives with pros, cons, cost, risk |
| `decision` | ✅ | Chosen alternative, rationale, tradeoffs, date |
| `consequences` | ✅ | Positive and negative outcomes |
| `reviewers` | | People who reviewed |
| `approvals` | | Formal approvals with timestamps |
| `requirements` | | Embedded functional and non-functional requirements |
| `risk_assessment` | | Risks with likelihood, impact, mitigations |
| `dependencies` | | Internal and external dependencies |
| `related_adrs` | | Cross-references (navigational only) |
| `lifecycle` | | Review cadence, supersession chain |
| `audit_trail` | | Immutable append-only event log |

## Agent Skill

The `.skills/adr-author/` directory follows the [agentskills.io specification](https://agentskills.io/specification) and works with:

- **Google Antigravity** (VS Code)
- **Claude Code** (terminal)
- **VS Code Copilot** (with skills support)
- Any agent implementing the Agent Skills standard

## Repomix Bundle

To create a single-file bundle of the core project (excluding examples and CI):

```bash
./scripts/bundle.sh
```

This generates `adr-governance-bundle.md` which can be pasted into any LLM context window.

## Example ADRs

The `examples/` directory contains 6 interconnected ADRs from a fictional IAM department. These are **low-level implementation decisions** — the kind of contended pattern choices you face *within* an already-adopted technology, with sizable pros and cons on each side:

| ID | Title | Status |
|----|-------|--------|
| ADR-0001 | Use DPoP over mTLS for Sender-Constrained Tokens | accepted |
| ADR-0002 | Use Reference Tokens over JWTs for Gateway Introspection | accepted |
| ADR-0003 | Use Pairwise Subject Identifiers for OIDC Relying Parties | accepted |
| ADR-0004 | Use Ed25519 over RSA-2048 for JWT Signing Keys | accepted |
| ADR-0005 | Use BFF Token Mediator for SPA Token Acquisition | accepted |
| ADR-0006 | Use Session Enrichment for Step-Up Authentication Proof | accepted |

## License

MIT
