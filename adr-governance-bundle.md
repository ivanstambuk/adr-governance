This file is a merged representation of a subset of the codebase, containing specifically included files and files not matching ignore patterns, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

- Pay special attention to the Repository Instruction. These contain important context and guidelines specific to this project.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: schemas/**, docs/**, architecture-decision-log/**, examples-reference/*.yaml, .skills/**, .adr-governance/**, scripts/**, README.md, CODEOWNERS.example, llms.txt
- Files matching these patterns are excluded: examples-reference/rendered/**, examples-reference/README.md, docs/web-chat-adr-authoring.md, docs/web-chat-quickstart.md, docs/ci-setup.md, scripts/verify-approvals.py, scripts/render-adr.py, scripts/extract-decisions.py, scripts/bundle.sh, rendered/**, docs/research/**, .github/**, *.lock, node_modules/**, adr-governance-bundle.md
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.adr-governance/
  config.yaml
.skills/
  adr-author/
    assets/
      adr-template.yaml
    references/
      GLOSSARY.md
      SCHEMA_REFERENCE.md
    SKILL.md
architecture-decision-log/
  ADR-0000-adopt-governed-adr-process.yaml
docs/
  adr-process.md
  glossary.md
examples-reference/
  ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.yaml
  ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.yaml
  ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.yaml
  ADR-0004-ed25519-over-rsa-for-jwt-signing.yaml
  ADR-0005-bff-token-mediator-for-spa-token-acquisition.yaml
  ADR-0006-session-enrichment-for-step-up-authentication.yaml
  ADR-0007-centralized-secret-store-for-api-keys.yaml
  ADR-0008-defer-openid-federation-for-trust-establishment.yaml
schemas/
  adr.schema.json
scripts/
  review-adr.py
  summarize-adr.py
  validate-adr.py
CODEOWNERS.example
llms.txt
README.md
```

# Files

## File: .adr-governance/config.yaml
````yaml
# ADR Governance Configuration
#
# This file is the single source of truth for governance rules that the CI
# pipeline enforces. It is platform-agnostic — the same config works on
# GitHub, Azure DevOps, GitLab, and any other Git platform.
#
# Changes to this file should be reviewed by the architecture team.

governance:
  # ──────────────────────────────────────────────────────────────────────
  # Administrators
  # ──────────────────────────────────────────────────────────────────────
  # ADR Administrators can make maintenance (non-substantive) changes to
  # any ADR without requiring the original ADR approvers to re-approve.
  # They still need a standard PR approval via branch protection, but the
  # verify-approvals.py identity check is skipped for maintenance changes.
  #
  # Identity format: use the same format as approvals[].identity — the
  # platform handle without the '@' prefix.
  admins:
    - identity: "ivanstambuk"
      name: "Ivan Stambuk"

  # ──────────────────────────────────────────────────────────────────────
  # Single ADR per PR
  # ──────────────────────────────────────────────────────────────────────
  # When true, a PR may only modify ONE ADR file. This ensures each merge
  # commit maps to exactly one architectural decision, keeping the audit
  # trail clean.
  #
  # Exception: supersession pairs. When a new ADR supersedes an old one,
  # the PR must touch exactly two ADRs: the new one (with lifecycle.supersedes)
  # and the old one (with status: superseded and lifecycle.superseded_by).
  # The CI script validates this automatically.
  single_adr_per_pr: true

  # ──────────────────────────────────────────────────────────────────────
  # Change Classification — Substantive Fields
  # ──────────────────────────────────────────────────────────────────────
  # Changes to these YAML fields are classified as "substantive" (Tier 1)
  # and require the original ADR approvers (via approvals[].identity) to
  # re-approve. All other field changes are "maintenance" (Tier 2) and
  # can be made by an ADR Administrator without re-approval.
  #
  # These are dotted YAML paths. A change to any key under these prefixes
  # is considered substantive.
  substantive_fields:
    - "adr.status"
    - "adr.title"
    - "decision" # decision.chosen_alternative, decision.rationale, etc.
    - "alternatives" # any change to alternatives array
    - "consequences" # positive or negative consequences
    - "approvals" # adding/removing/changing approvers
    - "context.summary" # changing the problem statement (not drivers/constraints)


  # ──────────────────────────────────────────────────────────────────────
  # Maintenance Fields (implicit)
  # ──────────────────────────────────────────────────────────────────────
  # Any field NOT listed in substantive_fields is automatically Tier 2
  # (maintenance). Common maintenance changes include:
  #
  #   - adr.schema_version         (schema migration)
  #   - adr.last_modified          (timestamp update)
  #   - adr.tags                   (adding/removing tags)
  #   - adr.component              (renaming component)
  #   - authors[].email            (email correction)
  #   - reviewers                  (adding reviewers)
  #   - context.business_drivers   (clarification, not reframing)
  #   - context.technical_drivers  (clarification)
  #   - context.constraints        (adding discovered constraints)
  #   - context.assumptions        (adding discovered assumptions)
  #   - requirements               (adding/updating requirements)
  #   - dependencies               (updating dependency list)
  #   - references                 (adding links)
  #   - lifecycle.next_review_date (review cadence update)
  #   - lifecycle.review_cycle_months
  #   - audit_trail                (adding events)
  #   - confirmation               (backfilling artifact IDs)
````

## File: examples-reference/ADR-0007-centralized-secret-store-for-api-keys.yaml
````yaml
adr:
  id: ADR-0007
  title: Reject centralized HashiCorp Vault for API runtime secrets in favor of native cloud provider secret stores
  summary: Rejected proposal to centralize all API runtime secrets (DB credentials, API keys, signing keys) in HashiCorp Vault.
    Native cloud provider secret stores (AWS Secrets Manager, Azure Key Vault) chosen instead due to lower operational burden
    and tighter IAM integration.
  status: rejected
  created_at: '2026-03-01T10:00:00Z'
  last_modified: '2026-03-05T14:00:00Z'
  version: '1.0'
  schema_version: 1.0.0
  project: Platform Infrastructure — Secrets Management
  component: API Runtime Secret Store
  tags:
  - secrets
  - vault
  - key-management
  - cloud-native
  - operational-complexity
  priority: high
  decision_type: technology
authors:
- name: Priya Sharma
  role: API Platform Lead
  email: priya.sharma@novatrust.example.com
decision_owner:
  name: Marcus Chen
  role: Head of IAM
  email: marcus.chen@novatrust.example.com
reviewers:
- name: Jonas Eriksen
  role: CISO
  email: jonas.eriksen@novatrust.example.com
- name: Tomasz Kowalski
  role: Network Security Architect
  email: tomasz.kowalski@novatrust.example.com
- name: Elena Vasquez
  role: IAM Architect
  email: elena.vasquez@novatrust.example.com
context:
  summary: 'NovaTrust''s 50+ microservices currently retrieve runtime secrets (database credentials, third-party API keys,
    JWT signing keys) from environment variables injected at deployment time. This approach has scaling and rotation pain
    points: rotating a database password requires redeploying all dependent services. Two approaches were considered — centralizing
    on HashiCorp Vault as a universal secrets engine, or adopting native cloud provider secret stores (AWS Secrets Manager,
    Azure Key Vault) with CSI driver integration for Kubernetes.'
  business_drivers:
  - Credential rotation currently requires coordinated redeployment of 15+ services — 4-hour change window
  - Audit compliance requires proving secrets are encrypted at rest and access-logged
  - Multi-cloud strategy (AWS primary, Azure DR) requires secrets accessible from both environments
  technical_drivers:
  - Environment variable injection does not support automatic rotation
  - No centralized audit trail for secret access (who accessed which secret, when)
  - HSM-backed signing keys (ADR-0004) need a secure key store with PKCS#11 or KMIP interface
  - Kubernetes CSI Secret Store Driver can mount secrets as volumes without application changes
  constraints:
  - Must support AWS and Azure simultaneously (multi-cloud DR requirement)
  - Maximum 5ms latency for secret retrieval at application startup
  - Must integrate with existing Kubernetes RBAC for access control
  - Team of 3 SREs must be able to operate the solution without dedicated Vault expertise
  assumptions:
  - Both AWS Secrets Manager and Azure Key Vault support automatic rotation for database credentials
  - Kubernetes CSI Secret Store Driver is production-ready for both cloud providers
  - Secret access logging satisfies SOC 2 Type II audit requirements
requirements:
  functional:
  - id: F-001
    description: All API runtime secrets retrievable without application code changes (volume mount or sidecar)
  - id: F-002
    description: Database credential rotation without service redeployment
  - id: F-003
    description: Centralized audit log of all secret access events with caller identity
  non_functional:
  - id: NF-001
    description: Secret retrieval latency < 5ms at application startup
  - id: NF-002
    description: 99.99% availability of secret store (must not be a single point of failure)
  - id: NF-003
    description: Operable by existing SRE team without specialized training > 2 days
alternatives:
- name: HashiCorp Vault (centralized secrets engine)
  summary: Deploy a self-managed HashiCorp Vault cluster as the universal secrets engine for all environments. All services
    retrieve secrets via Vault Agent sidecar or CSI driver. Vault manages encryption, rotation, dynamic credentials, and audit
    logging.
  pros:
  - Single unified secrets API across all cloud providers and on-premises
  - Dynamic secrets — generates short-lived database credentials on demand
  - Rich policy engine (Vault policies + Sentinel) for fine-grained access control
  - Transit secrets engine provides encryption-as-a-service without exposing keys
  - Large ecosystem and community support
  cons:
  - Significant operational burden — requires dedicated Vault cluster management (3-5 node HA, unsealing, upgrades)
  - Team lacks Vault expertise — estimated 4-6 weeks ramp-up for 3 SREs
  - Vault becomes a critical infrastructure dependency — outage blocks all service startups
  - 'Cost: $150K/year for Vault Enterprise (required for HSM auto-unseal and namespaces) + infrastructure'
  - Complex disaster recovery — Vault replication across cloud providers requires careful design
  - Seal/unseal ceremony adds operational risk — automated unseal requires HSM or cloud KMS integration
  estimated_cost: high
  risk: high
  rejection_rationale: Operational burden exceeds team capacity. 3-person SRE team cannot absorb Vault cluster management
    (HA, unsealing, upgrades, DR replication) alongside existing responsibilities. $150K/year Enterprise license cost is not
    justified when native cloud secret stores provide equivalent functionality for secrets retrieval and rotation. Dynamic
    secrets — Vault's strongest differentiator — are not required for our use case (long-lived service accounts with periodic
    rotation are sufficient).
- name: Native cloud provider secret stores (AWS Secrets Manager + Azure Key Vault)
  summary: Use each cloud provider's native secret store — AWS Secrets Manager in primary, Azure Key Vault in DR. Kubernetes
    CSI Secret Store Driver mounts secrets as volumes. Cross-cloud secret synchronization handled by CI/CD pipeline with encrypted
    transit.
  pros:
  - Zero operational overhead — fully managed services with provider SLAs
  - Native IAM integration — Kubernetes service accounts map directly to cloud IAM roles
  - Built-in automatic rotation for RDS/Aurora credentials (AWS) and SQL Database (Azure)
  - Per-secret audit logging via CloudTrail (AWS) and Azure Monitor
  - No additional licensing cost — included in cloud contract
  - SRE team already has AWS/Azure expertise — no ramp-up needed
  cons:
  - Two separate APIs and configurations for multi-cloud
  - Cross-cloud secret sync requires custom CI/CD pipeline
  - No dynamic secrets — rotation is periodic, not on-demand
  - Policy engine is less granular than Vault policies
  - Vendor lock-in per cloud provider for secret store API
  estimated_cost: low
  risk: low
- name: Sealed Secrets + External Secrets Operator (GitOps-native)
  summary: Use Bitnami Sealed Secrets for static secrets (encrypted in Git) and External Secrets Operator to sync secrets
    from cloud provider stores into Kubernetes. Fully GitOps-driven — secrets are declarative.
  pros:
  - GitOps-native — secrets defined alongside application manifests
  - No additional infrastructure to manage beyond Kubernetes
  - External Secrets Operator supports both AWS and Azure backends
  cons:
  - Sealed Secrets controller is a single point of failure in each cluster
  - Encryption key management for sealed secrets adds complexity
  - No built-in rotation — depends on external provider rotation
  - Two layers of abstraction (Sealed Secrets + External Secrets Operator) increases debugging complexity
  - Less mature than Vault or native cloud stores
  estimated_cost: low
  risk: medium
  rejection_rationale: Two layers of abstraction (Sealed Secrets + External Secrets Operator) are unnecessarily complex for
    our use case. The Sealed Secrets controller is a single point of failure per cluster. Native cloud provider secret stores
    provide the same Kubernetes integration via CSI driver with fewer moving parts.
decision:
  chosen_alternative: Native cloud provider secret stores (AWS Secrets Manager + Azure Key Vault)
  rationale: |
    - Zero operational overhead aligns with 3-person SRE team capacity constraint
    - Native IAM integration eliminates an additional identity and access management layer
    - Built-in rotation for database credentials satisfies F-002 without custom automation
    - CloudTrail and Azure Monitor satisfy audit logging requirement (F-003) with no additional tooling
    - No additional licensing cost vs. $150K/year for Vault Enterprise
    - Team already has cloud provider expertise — zero ramp-up time
  tradeoffs: |
    - Two separate configurations for multi-cloud — accepted because each environment is independently operated
    - No dynamic secrets — accepted because periodic rotation (every 30 days) is sufficient for our threat model
    - Cross-cloud sync via CI/CD pipeline adds deployment complexity — accepted as lower risk than Vault HA replication
    - Vendor lock-in per provider — mitigated by CSI Secret Store Driver abstraction at the Kubernetes layer
  decision_date: '2026-03-05'
  confidence: high
consequences:
  positive:
  - SRE team capacity preserved — no new infrastructure to learn or operate
  - $150K/year cost avoidance from Vault Enterprise licensing
  - Database credential rotation automated via native provider mechanisms
  - Audit logging available via existing cloud monitoring tools the team already uses
  negative:
  - Cross-cloud secret sync requires maintaining a custom CI/CD pipeline step
  - Two sets of IaC (Terraform) modules for AWS Secrets Manager and Azure Key Vault
  - Dynamic secrets not available — must use periodic rotation with 30-day cycle
confirmation:
  description: "Verify all API keys migrated to centralized vault. Scan codebase for hardcoded secrets. Audit vault access policies."

dependencies:
  internal:
  - Kubernetes clusters (AWS EKS, Azure AKS) with CSI Secret Store Driver
  - CI/CD pipeline (GitHub Actions) for cross-cloud secret synchronization
  - Terraform modules for AWS Secrets Manager and Azure Key Vault
  external:
  - AWS Secrets Manager service availability
  - Azure Key Vault service availability
references:
- title: AWS Secrets Manager Documentation
  url: https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html
- title: Azure Key Vault Documentation
  url: https://learn.microsoft.com/en-us/azure/key-vault/general/overview
- title: Kubernetes Secrets Store CSI Driver
  url: https://secrets-store-csi-driver.sigs.k8s.io/
- title: HashiCorp Vault Enterprise Pricing
  url: https://www.hashicorp.com/products/vault/pricing
lifecycle:
  review_cycle_months: 24
  next_review_date: '2028-03-05'
  superseded_by: null
  supersedes: null
  archival:
    archived_at: null
    archive_reason: null
audit_trail:
- event: created
  by: Priya Sharma
  at: '2026-03-01T10:00:00Z'
- event: updated
  by: Priya Sharma
  at: '2026-03-03T16:00:00Z'
  details: Added Sealed Secrets alternative after SRE team suggestion, expanded Vault cost analysis
- event: rejected
  by: Marcus Chen
  at: '2026-03-05T14:00:00Z'
  details: Vault proposal rejected due to operational burden exceeding SRE capacity. Native cloud stores selected. Re-evaluate
    if dynamic secrets become a hard requirement.
````

## File: examples-reference/ADR-0008-defer-openid-federation-for-trust-establishment.yaml
````yaml
adr:
  id: ADR-0008
  title: Defer adoption of OpenID Federation 1.0 for automated trust establishment
  summary:
    Deferred proposal to adopt OpenID Federation 1.0 for automated trust establishment between NovaTrust
    and partner identity providers. Specification is not yet final and PingFederate support is roadmapped
    but not GA.
  status: deferred
  created_at: "2026-02-01T10:00:00Z"
  last_modified: "2026-02-15T16:00:00Z"
  version: "0.1"
  schema_version: 1.0.0
  project: API Authorization Layer — Federation
  component: Trust Establishment
  tags:
    - openid
    - federation
    - trust
    - deferred
    - identity-provider
  priority: medium
  decision_type: technology
authors:
  - name: Elena Vasquez
    role: IAM Architect
    email: elena.vasquez@novatrust.example.com
decision_owner:
  name: Marcus Chen
  role: Head of IAM
  email: marcus.chen@novatrust.example.com
reviewers:
  - name: Jonas Eriksen
    role: CISO
    email: jonas.eriksen@novatrust.example.com
  - name: Priya Sharma
    role: API Platform Lead
    email: priya.sharma@novatrust.example.com
context:
  summary: |
    NovaTrust currently establishes trust with partner identity providers (banks, fintechs, insurance
    companies) through manual metadata exchange — downloading SAML/OIDC metadata XML, verifying
    certificates out-of-band, and configuring each partner connection in PingFederate manually.

    With 40+ partner connections and 5–10 new partners onboarding per quarter, the manual process
    creates operational bottlenecks and human error risks (expired certificates, stale metadata).

    OpenID Federation 1.0 promises automated trust establishment via trust chains — federating entities
    publish signed entity statements, and trust anchors (e.g., national banking authorities) vouch
    for subordinate entities. This would eliminate manual metadata exchange.
  business_drivers:
    - Partner onboarding takes 2–4 weeks due to manual metadata exchange and certificate verification
    - 3 incidents in the past year caused by expired partner certificates that were not rotated in time
    - Regulatory push toward automated trust frameworks in PSD2 and eIDAS 2.0 ecosystems
  technical_drivers:
    - Manual metadata exchange does not scale beyond 50 partner connections without dedicated staff
    - OpenID Federation 1.0 trust chains enable automated certificate rotation and metadata refresh
    - PingFederate has OpenID Federation support on its product roadmap (expected H2 2026)
  constraints:
    - Must not break existing partner connections during any transition
    - PingFederate is the authorization server — mechanism must be natively supported or plugin-compatible
    - Partners must also support the chosen mechanism — unilateral adoption is not possible
  assumptions:
    - OpenID Federation 1.0 specification will reach final status in 2026
    - PingFederate will ship GA support for OpenID Federation by end of 2026
    - At least 5 key partners are willing to pilot the new trust establishment mechanism
requirements:
  functional:
    - id: F-001
      description: Automated discovery and validation of partner identity provider metadata via trust chains
    - id: F-002
      description: Automated certificate rotation without manual intervention or service disruption
    - id: F-003
      description: Fallback to manual metadata exchange for partners that do not support federation
  non_functional:
    - id: NF-001
      description: Trust chain resolution must complete in < 2 seconds
    - id: NF-002
      description: Federation metadata must be cached with configurable TTL (default 24 hours)
    - id: NF-003
      description: Must not introduce a single point of failure in the trust resolution chain
alternatives:
  - name: OpenID Federation 1.0 trust chains
    summary:
      Adopt OpenID Federation 1.0 for automated trust establishment. NovaTrust registers as a
      subordinate entity under a trust anchor (e.g., national banking authority). Partners do the same.
      Trust is established automatically via signed entity statements and trust chain resolution.
    pros:
      - Eliminates manual metadata exchange — trust established automatically via trust chains
      - Automated certificate rotation via entity statement refresh
      - Standards-based — aligns with eIDAS 2.0 and PSD2 regulatory direction
      - Scales to hundreds of partners without additional operational overhead
    cons:
      - Specification is not yet final (draft stage as of February 2026)
      - PingFederate support is roadmapped but not GA — requires waiting for vendor
      - Requires trust anchor infrastructure (national banking authority or equivalent)
      - Partner adoption is uncertain — unilateral adoption provides no benefit
      - Limited production deployments to learn from — early adopter risk
    estimated_cost: medium
    risk: high
  - name: Automated metadata exchange via well-known endpoints
    summary: |
      Use OIDC Discovery (/.well-known/openid-configuration) with automated polling and certificate
      pinning. A custom service periodically fetches partner metadata, validates certificates against
      a pinned trust store, and updates PingFederate configuration via admin API.
    pros:
      - Can be built today — no dependency on unfinished specifications
      - Leverages existing OIDC Discovery that all partners already support
      - Incremental improvement over manual exchange
    cons:
      - Custom automation code to build and maintain
      - Certificate pinning requires manual trust store updates when partners rotate CAs
      - No formal trust chain — trust is based on TLS and manual CA pinning, not cryptographic attestation
      - Does not address the fundamental scaling problem — just automates parts of it
    estimated_cost: low
    risk: low
    rejection_rationale:
      This is a tactical improvement, not a strategic solution. It automates metadata
      fetching but does not solve the trust establishment problem — certificate pinning still requires
      manual trust store management. However, it could serve as a bridge while waiting for OpenID Federation.
decision:
  chosen_alternative: OpenID Federation 1.0 trust chains
  rationale: |
    - Standards-based approach aligns with regulatory direction (eIDAS 2.0, PSD2)
    - Eliminates the root cause of operational bottlenecks — manual trust establishment
    - Automated certificate rotation addresses the recurring incident pattern
    - Scales to hundreds of partners, supporting NovaTrust's growth trajectory

    However, the decision is **deferred** because:
    - The specification is not yet final — adopting a draft standard carries specification change risk
    - PingFederate GA support is not available — building on pre-release features is not production-ready
    - Partner readiness is unknown — unilateral adoption provides zero value
  tradeoffs: |
    - Deferring means continued manual metadata exchange for 6–12 months
    - Risk of 2–3 more certificate expiry incidents during the deferral period
    - May need to implement the tactical alternative (Option 2) as a bridge if deferral extends beyond 12 months
  decision_date: "2026-02-15"
  confidence: low
consequences:
  positive:
    - No investment in an immature specification that may change before finalization
    - No dependency on pre-release vendor features
    - Time to build partner consensus and pilot readiness
  negative:
    - Continued manual metadata exchange — operational bottleneck persists
    - Ongoing certificate expiry risk for existing partner connections
    - Potential competitive disadvantage if peers adopt federation earlier
confirmation:
  description: "Periodic review of OpenID Federation specification maturity. Track industry adoption via references and revisit when specification reaches stable status."

dependencies:
  internal:
    - PingFederate 12.x (authorization server — pending OpenID Federation support)
  external:
    - OpenID Federation 1.0 specification finalization
    - PingFederate product roadmap (OpenID Federation GA)
    - Partner bank readiness for federation
references:
  - title: OpenID Federation 1.0 — Draft Specification
    url: https://openid.net/specs/openid-federation-1_0.html
  - title: eIDAS 2.0 Technical Architecture Reference Framework
    url: https://eu-digital-identity-wallet.github.io/eudi-doc-architecture-and-reference-framework/latest/arf/
  - title: PingFederate Product Roadmap (internal)
    url: https://docs.pingidentity.com/pingfederate/latest/release-notes.html
lifecycle:
  review_cycle_months: 6
  next_review_date: "2026-08-15"
  superseded_by: null
  supersedes: null
  archival:
    archived_at: null
    archive_reason: null
audit_trail:
  - event: created
    by: Elena Vasquez
    at: "2026-02-01T10:00:00Z"
    details: Initial proposal for OpenID Federation adoption
  - event: updated
    by: Elena Vasquez
    at: "2026-02-10T11:00:00Z"
    details: Added tactical alternative (automated metadata exchange) after discussion with API platform team
  - event: deferred
    by: Marcus Chen
    at: "2026-02-15T16:00:00Z"
    details:
      Deferred until OpenID Federation 1.0 reaches final specification status and PingFederate ships
      GA support. Re-evaluate in August 2026. PR closed with 'deferred' label.
````

## File: scripts/review-adr.py
````python
#!/usr/bin/env python3
"""
Pre-review quality gate for ADR YAML files.

Generates an LLM prompt that performs a Socratic review of an ADR draft,
probing for ambiguities, weak rationale, missing edge cases, and semantic
inconsistencies — before the ADR reaches a human reviewer.

This shifts review effort left: the proposer works with an AI assistant
through iterative refinement until the ADR is clear, complete, and
internally consistent. Human reviewers then focus on strategic judgement
rather than catching omissions.

Usage:
    # Generate a review prompt for a single ADR (pipe to your LLM)
    python3 review-adr.py architecture-decision-log/ADR-0001.yaml

    # Review with additional context from related ADRs
    python3 review-adr.py --context-from architecture-decision-log/ \
        architecture-decision-log/ADR-0001.yaml

    # Output the prompt to a file
    python3 review-adr.py -o review-prompt.md architecture-decision-log/ADR-0001.yaml

Requires: pip install pyyaml
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: Missing dependency. Install with:")
    print("  pip install pyyaml")
    sys.exit(2)


def load_adr(filepath: Path) -> dict:
    """Load a single ADR YAML file."""
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    if not data or not isinstance(data, dict) or "adr" not in data:
        print(f"ERROR: {filepath} is not a valid ADR file", file=sys.stderr)
        sys.exit(1)
    return data


def load_context_adrs(paths: list[str], exclude: str) -> list[dict]:
    """Load ADRs from directories for cross-reference context."""
    adrs = []
    for arg in paths:
        target = Path(arg)
        if target.is_dir():
            for f in sorted(target.glob("*.yaml")):
                if str(f) == exclude:
                    continue
                try:
                    with open(f, "r") as fh:
                        data = yaml.safe_load(fh)
                    if data and isinstance(data, dict) and "adr" in data:
                        adrs.append(data)
                except yaml.YAMLError:
                    pass
        elif target.is_file() and str(target) != exclude:
            try:
                with open(target, "r") as fh:
                    data = yaml.safe_load(fh)
                if data and isinstance(data, dict) and "adr" in data:
                    adrs.append(data)
            except yaml.YAMLError:
                pass
    return adrs


def format_adr_for_review(data: dict) -> str:
    """Format the full ADR YAML as a readable block for the prompt."""
    return yaml.dump(data, default_flow_style=False, allow_unicode=True,
                     width=200, sort_keys=False)


def format_context_summaries(context_adrs: list[dict]) -> str:
    """Format related ADRs as brief summaries for cross-reference."""
    if not context_adrs:
        return ""

    lines = [
        "",
        "## Existing Decisions (Cross-Reference Context)",
        "",
        "The following decisions already exist in the ADL. Check the reviewed ADR",
        "for consistency, conflicts, or dependencies with these:",
        "",
    ]
    for adr in context_adrs:
        meta = adr.get("adr", {})
        decision = adr.get("decision", {})
        adr_id = meta.get("id", "?")
        title = meta.get("title", "?")
        status = meta.get("status", "?")
        chosen = decision.get("chosen_alternative", "?")
        summary = meta.get("summary", "")

        lines.append(f"### {adr_id}: {title}")
        lines.append(f"**Status:** {status} | **Chosen:** {chosen}")
        if summary:
            lines.append(f"**Summary:** {summary}")
        lines.append("")

    return "\n".join(lines)


def generate_review_prompt(
    adr_yaml: str, context_section: str = ""
) -> str:
    """Generate the Socratic review prompt."""
    return f"""# ADR Semantic Review — Pre-Reviewer Quality Gate

You are an Architecture Review Board member performing a **Socratic review**
of the ADR draft below. Your goal is to ensure the ADR is clear, complete,
and internally consistent **before** it reaches human reviewers.

## Your Review Approach

You must be thorough but constructive. For each issue you find, explain
*why* it matters and suggest a concrete improvement. Organize your feedback
into the following categories:

### 1. Semantic Clarity
- Is the problem statement (`context.summary`) unambiguous? Could two readers
  interpret it differently?
- Does the rationale clearly connect the chosen alternative to the stated
  drivers and constraints?
- Are there vague terms ("scalable", "performant", "modern") that need
  quantification or definition?
- Would a new team member understand this decision without additional context?

### 2. Completeness
- Are all required sections substantive (not just template placeholders)?
- Does each alternative have **balanced** pros and cons? (Watch for strawman
  alternatives with 1 pro and 5 cons.)
- Are constraints realistic and testable? (e.g., "low latency" → "< 10ms p99")
- Are negative consequences acknowledged honestly?
- Is the `confirmation.description` actionable — does it describe *how*
  compliance will be verified?
- Is the `adr.summary` a compelling elevator pitch that enables stakeholder
  triage without reading the full ADR?

### 3. Logical Consistency
- Does `decision.chosen_alternative` match an entry in `alternatives[].name`?
- Is the `decision.rationale` consistent with the pros/cons listed?
- Do the `consequences.negative` entries align with the cons of the chosen
  alternative?
- Are `audit_trail` events consistent with the `adr.status`?
- If `lifecycle.supersedes` is set, is there a valid supersession chain?

### 4. Assumption Risks
- Are assumptions (`context.assumptions`) explicitly stated?
- What happens if an assumption is wrong? Is that risk captured?
- Are there unstated assumptions hiding in the rationale?

### 5. Missing Perspectives
- Are there stakeholders who should be listed as reviewers but aren't?
- Are there alternatives that weren't considered but should be?
- Are there regulatory, compliance, or security implications not addressed?
- Would the rejected alternatives' teams agree with the `rejection_rationale`?

### 6. Cross-Reference Consistency
- Does this decision conflict with any existing decisions in the ADL?
- Does it create new dependencies that should be tracked?
- If it supersedes an existing decision, is the migration path clear?

## Output Format

Structure your review as:

```
## Summary Verdict
[READY FOR REVIEW | NEEDS REWORK | MAJOR GAPS]
Brief overall assessment (2-3 sentences).

## Issues Found

### [Category]: [Issue Title]
**Severity:** HIGH | MEDIUM | LOW
**Location:** [field path, e.g., decision.rationale]
**Issue:** [what's wrong]
**Suggestion:** [concrete improvement]

(repeat for each issue)

## Strengths
- [what the ADR does well — always include at least 2]

## Open Questions for the Proposer
1. [questions that the proposer should answer before submitting for review]
```

---

## ADR Under Review

```yaml
{adr_yaml}
```
{context_section}
---

Now perform your review. Be rigorous but fair — the goal is to help the
proposer strengthen the ADR before it reaches human reviewers.
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate an LLM semantic review prompt for an ADR.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Review a single ADR (prints prompt to stdout — pipe to your LLM)
  python3 review-adr.py architecture-decision-log/ADR-0001.yaml

  # Review with cross-reference context from the full ADL
  python3 review-adr.py --context-from architecture-decision-log/ \\
      architecture-decision-log/ADR-0009.yaml

  # Pipe to an LLM
  python3 review-adr.py architecture-decision-log/ADR-0009.yaml | \\
      llm -m gpt-4o

  # Save prompt to file
  python3 review-adr.py -o review.md architecture-decision-log/ADR-0009.yaml
        """,
    )

    parser.add_argument(
        "adr_file",
        help="Path to the ADR YAML file to review",
    )
    parser.add_argument(
        "--context-from",
        nargs="*",
        default=[],
        help="Directories or files containing related ADRs for cross-reference context",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    # Load the target ADR
    adr_path = Path(args.adr_file)
    if not adr_path.exists():
        print(f"ERROR: {adr_path} not found", file=sys.stderr)
        sys.exit(1)

    adr_data = load_adr(adr_path)
    adr_yaml = format_adr_for_review(adr_data)

    # Load context ADRs
    context_section = ""
    if args.context_from:
        context_adrs = load_context_adrs(args.context_from, str(adr_path))
        context_section = format_context_summaries(context_adrs)

    # Generate the prompt
    prompt = generate_review_prompt(adr_yaml, context_section)

    # Output
    if args.output:
        Path(args.output).write_text(prompt)
        meta = adr_data.get("adr", {})
        print(
            f"Review prompt for {meta.get('id', '?')} written to {args.output}",
            file=sys.stderr
        )
    else:
        print(prompt)


if __name__ == "__main__":
    main()
````

## File: scripts/summarize-adr.py
````python
#!/usr/bin/env python3
"""Summarize ADR YAML files for stakeholder communication.

Produces concise, skimmable summaries designed for email or chat — not the
full decision document. Points readers to the rendered Markdown or YAML
source for the complete record.

Usage:
    # Email-length summary (default)
    python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml

    # Ultra-short chat summary (Slack/Teams)
    python3 scripts/summarize-adr.py --format chat architecture-decision-log/ADR-0001.yaml

    # Summarize multiple ADRs (e.g., after a review session)
    python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml \
        architecture-decision-log/ADR-0002.yaml

    # All ADRs in a directory
    python3 scripts/summarize-adr.py architecture-decision-log/

    # Save to file
    python3 scripts/summarize-adr.py -o summary.md architecture-decision-log/ADR-0001.yaml

Requires: pip install pyyaml
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: Missing dependency. Install with:")
    print("  pip install pyyaml")
    sys.exit(2)


def load_adr(filepath: Path) -> dict:
    """Load a single ADR YAML file."""
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    if not data or not isinstance(data, dict) or "adr" not in data:
        return {}
    return data


def summarize_email(data: dict, source_path: str = "") -> str:
    """Produce an email-length stakeholder summary.

    Designed to be pasted into an email or document after a meeting.
    Covers: what was decided, why, what alternatives were considered,
    key tradeoffs, and what happens next.
    """
    adr = data.get("adr", {})
    context = data.get("context", {})
    decision = data.get("decision", {})
    alternatives = data.get("alternatives", [])
    consequences = data.get("consequences", {})
    confirmation = data.get("confirmation", {})
    owner = data.get("decision_owner", {})

    adr_id = adr.get("id", "ADR-????")
    title = adr.get("title", "Untitled")
    status = adr.get("status", "unknown")
    priority = adr.get("priority", "—")
    decision_date = decision.get("decision_date", "—")
    confidence = decision.get("confidence", "—")
    chosen = decision.get("chosen_alternative", "—")
    owner_name = owner.get("name", "—")
    owner_role = owner.get("role", "")

    lines = []

    # Header
    lines.append(f"## {adr_id}: {title}")
    lines.append("")
    lines.append(f"**Status:** `{status}` · **Priority:** `{priority}` · "
                 f"**Confidence:** `{confidence}` · **Date:** {decision_date}")
    lines.append(f"**Decision Owner:** {owner_name}" +
                 (f" ({owner_role})" if owner_role else ""))
    lines.append("")

    # Summary / elevator pitch
    summary = adr.get("summary", "")
    if summary:
        lines.append(f"> {summary.strip()}")
        lines.append("")

    # What was decided
    lines.append(f"**Decision:** {chosen}")
    lines.append("")

    # Brief rationale (first meaningful paragraph only)
    rationale = decision.get("rationale", "")
    if rationale:
        rationale_text = rationale.strip()
        # Take the first paragraph or first 3 lines, whichever is shorter
        paragraphs = rationale_text.split("\n\n")
        first_para = paragraphs[0].strip()
        # If it's a bullet list, take up to 3 bullets
        if first_para.startswith("-") or first_para.startswith("*"):
            bullet_lines = [l for l in first_para.split("\n") if l.strip()][:3]
            first_para = "\n".join(bullet_lines)
            if len([l for l in rationale_text.split("\n") if l.strip()]) > 3:
                first_para += "\n- *(…more in full document)*"
        lines.append("**Why:**")
        lines.append(first_para)
        lines.append("")

    # Alternatives considered (one-liner each)
    if alternatives:
        lines.append("**Alternatives considered:**")
        for alt in alternatives:
            name = alt.get("name", "?")
            is_chosen = name == chosen
            marker = " ✅" if is_chosen else ""
            risk = alt.get("risk", "")
            cost = alt.get("estimated_cost", "")
            rejection = alt.get("rejection_rationale", "")

            parts = [f"- **{name}**{marker}"]
            meta = []
            if cost:
                meta.append(f"cost: {cost}")
            if risk:
                meta.append(f"risk: {risk}")
            if meta:
                parts.append(f"({', '.join(meta)})")
            if rejection and not is_chosen:
                # Truncate rejection rationale to first sentence
                first_sentence = rejection.strip().split(". ")[0]
                if not first_sentence.endswith("."):
                    first_sentence += "."
                parts.append(f"— *{first_sentence}*")

            lines.append(" ".join(parts))
        lines.append("")

    # Key tradeoffs
    tradeoffs = decision.get("tradeoffs", "")
    if tradeoffs:
        tradeoff_text = tradeoffs.strip()
        # Take first 3 lines/bullets
        tradeoff_lines = [l for l in tradeoff_text.split("\n") if l.strip()][:3]
        lines.append("**Key tradeoffs:**")
        for tl in tradeoff_lines:
            if not tl.startswith("-") and not tl.startswith("*"):
                tl = f"- {tl}"
            lines.append(tl)
        lines.append("")

    # Consequences (top positive + negative)
    positive = consequences.get("positive", [])
    negative = consequences.get("negative", [])
    if positive or negative:
        lines.append("**Impact:**")
        for item in positive[:2]:
            lines.append(f"- ✅ {item}")
        for item in negative[:2]:
            lines.append(f"- ⚠️ {item}")
        lines.append("")

    # What happens next
    if confirmation.get("description"):
        lines.append(f"**Next steps:** {confirmation['description'].strip()}")
        lines.append("")

    # Source link
    if source_path:
        lines.append(f"📄 *Full decision: [{source_path}]({source_path})*")
        lines.append("")

    return "\n".join(lines)


def summarize_chat(data: dict, source_path: str = "") -> str:
    """Produce an ultra-short chat summary (Slack/Teams).

    3-5 lines maximum. Just the headline, the decision, and a link.
    """
    adr = data.get("adr", {})
    decision = data.get("decision", {})
    consequences = data.get("consequences", {})

    adr_id = adr.get("id", "ADR-????")
    title = adr.get("title", "Untitled")
    status = adr.get("status", "unknown")
    chosen = decision.get("chosen_alternative", "—")
    decision_date = decision.get("decision_date", "—")

    lines = []
    lines.append(f"**{adr_id}: {title}**")

    summary = adr.get("summary", "")
    if summary:
        # First sentence only
        first_sentence = summary.strip().split(". ")[0]
        if not first_sentence.endswith("."):
            first_sentence += "."
        lines.append(first_sentence)

    lines.append(f"→ **{chosen}** (`{status}`, {decision_date})")

    # One positive, one negative consequence
    positive = consequences.get("positive", [])
    negative = consequences.get("negative", [])
    if positive:
        lines.append(f"  ✅ {positive[0]}")
    if negative:
        lines.append(f"  ⚠️ {negative[0]}")

    if source_path:
        lines.append(f"📄 {source_path}")

    return "\n".join(lines)


def summarize_digest(entries: list[tuple[dict, str]]) -> str:
    """Produce a multi-ADR digest — a meeting recap or batch summary.

    One section per ADR, designed for stakeholders who missed the meeting.
    """
    lines = []
    lines.append("# Architecture Decision Digest")
    lines.append("")
    lines.append(f"*{len(entries)} decision(s) summarized below.*")
    lines.append("")
    lines.append("---")
    lines.append("")

    for data, source_path in entries:
        lines.append(summarize_email(data, source_path))
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def collect_files(targets: list[str]) -> list[Path]:
    """Collect ADR YAML files from targets (files and/or directories)."""
    files = []
    for target in targets:
        p = Path(target)
        if p.is_dir():
            for f in sorted(p.glob("*.yaml")):
                files.append(f)
            for f in sorted(p.glob("*.yml")):
                files.append(f)
        elif p.is_file():
            files.append(p)
        else:
            print(f"WARNING: {target} not found, skipping", file=sys.stderr)
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Summarize ADR YAML files for stakeholder communication.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # Email summary (default)
  python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml

  # Chat summary (Slack/Teams — ultra-short)
  python3 scripts/summarize-adr.py --format chat architecture-decision-log/ADR-0001.yaml

  # Digest of multiple ADRs (after a review session)
  python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml \\
      architecture-decision-log/ADR-0002.yaml

  # All ADRs in a directory
  python3 scripts/summarize-adr.py architecture-decision-log/

  # Save to file
  python3 scripts/summarize-adr.py -o summary.md architecture-decision-log/ADR-0001.yaml
        """,
    )

    parser.add_argument(
        "targets",
        nargs="+",
        help="ADR YAML files or directories to summarize",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["email", "chat"],
        default="email",
        help="Summary format: 'email' (default, ~10–15 lines) or 'chat' (3–5 lines for Slack/Teams)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    files = collect_files(args.targets)
    if not files:
        print("No YAML files found.", file=sys.stderr)
        sys.exit(1)

    # Load all ADRs
    entries = []
    for filepath in files:
        data = load_adr(filepath)
        if not data:
            print(f"SKIP: {filepath} (not an ADR file)", file=sys.stderr)
            continue
        entries.append((data, str(filepath)))

    if not entries:
        print("No valid ADR files found.", file=sys.stderr)
        sys.exit(1)

    # Generate output
    if len(entries) == 1 and args.format == "email":
        output = summarize_email(entries[0][0], entries[0][1])
    elif len(entries) == 1 and args.format == "chat":
        output = summarize_chat(entries[0][0], entries[0][1])
    elif args.format == "chat":
        # Multiple ADRs in chat format — one per block
        blocks = []
        for data, path in entries:
            blocks.append(summarize_chat(data, path))
        output = "\n\n---\n\n".join(blocks)
    else:
        # Multiple ADRs — produce a digest
        output = summarize_digest(entries)

    # Output
    if args.output:
        Path(args.output).write_text(output)
        print(f"Summary written to {args.output} ({len(entries)} ADR(s))", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
````

## File: examples-reference/ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.yaml
````yaml
adr:
  id: ADR-0001
  title: Use DPoP over mTLS as the sender-constraining mechanism for OAuth 2.1 access tokens
  summary: Adopt DPoP (RFC 9449) as the sole sender-constraining mechanism for all OAuth 2.1 client types, avoiding mTLS certificate provisioning and CDN passthrough costs.
  status: accepted
  created_at: "2026-01-10T09:00:00Z"
  last_modified: "2026-01-25T14:30:00Z"
  version: "1.0"
  schema_version: "1.0.0"
  project: API Authorization Layer — OAuth 2.1 Implementation
  component: Token Sender Constraining
  tags:
    - oauth
    - dpop
    - mtls
    - sender-constraining
    - token-binding
    - rfc9449
  priority: high
  decision_type: technology
authors:
  - name: Elena Vasquez
    role: IAM Architect
    email: elena.vasquez@novatrust.example.com
  - name: Kai Lindström
    role: Mobile Platform Lead
    email: kai.lindstrom@novatrust.example.com
decision_owner:
  name: Marcus Chen
  role: Head of Identity and Access Management
  email: marcus.chen@novatrust.example.com
reviewers:
  - name: Priya Sharma
    role: API Platform Lead
    email: priya.sharma@novatrust.example.com
  - name: Jonas Eriksen
    role: CISO
    email: jonas.eriksen@novatrust.example.com
  - name: Raj Patel
    role: CDN / Edge Infrastructure Lead
    email: raj.patel@novatrust.example.com
approvals:
  - name: Marcus Chen
    role: Head of IAM
    identity: "@marcuschen"
    approved_at: "2026-01-24T10:00:00Z"
    signature_id: sig-dpop-001
  - name: Jonas Eriksen
    role: CISO
    identity: "@jonaseriksen"
    approved_at: "2026-01-25T09:00:00Z"
    signature_id: sig-dpop-002
context:
  summary: |
    NovaTrust has adopted OAuth 2.1 (RFC 9700) as its API authorization framework. The specification
    mandates sender-constrained tokens to prevent token theft and replay. Two mechanisms are
    standardized: mTLS certificate-bound tokens (RFC 8705) and DPoP proof-of-possession (RFC 9449).

    Both bind a token to the client that requested it, but differ in *where* binding happens: mTLS
    at the TLS layer, DPoP at the application layer via signed JWTs.

    ```mermaid
    sequenceDiagram
        participant C as Client
        participant AS as PingFederate (AS)
        participant GW as PingAccess (Gateway)
        participant RS as Resource Server

        C->>C: Generate ephemeral keypair
        C->>AS: Token Request + DPoP Proof (JWT signed with ephemeral key)
        AS->>AS: Validate DPoP proof, bind token to JWK thumbprint
        AS->>C: Access Token (cnf.jkt = thumbprint)
        C->>GW: API Request + Authorization: DPoP <token> + DPoP: <proof>
        GW->>GW: Validate DPoP proof signature + cnf.jkt binding
        GW->>RS: Forward (authenticated, sender-verified)
    ```

    We must choose one mechanism as the primary sender-constraining method for all client types —
    public mobile apps, confidential backend services, and partner API consumers.
  business_drivers:
    - PSD2 SCA compliance requires sender-constrained tokens for payment APIs
    - Mobile banking app (3M+ users) cannot manage X.509 client certificates
    - CDN provider (Cloudflare) terminates TLS before traffic reaches our infrastructure
    - Partner banks need a mechanism that works through their corporate proxies
  technical_drivers:
    - mTLS requires client certificate provisioning and lifecycle management per device
    - CDN TLS termination strips client certificates — requires costly mTLS passthrough or re-origination
    - DPoP proofs are application-layer and survive any TLS termination or proxy chain
    - PingFederate 12.x supports both DPoP (RFC 9449) and mTLS (RFC 8705) natively
    - Existing API gateway (PingAccess) can validate DPoP proofs without TLS configuration changes
  constraints:
    - Must work for public clients (mobile app) that cannot hold X.509 certificates securely
    - Must survive CDN TLS termination (Cloudflare) without requiring mTLS passthrough configuration
    - Must not require changes to partner bank network egress proxies
    - PingFederate 12.x is the authorization server — mechanism must be natively supported
  assumptions:
    - Mobile app can generate and store an ephemeral asymmetric keypair in the device secure enclave
    - All resource servers can parse and validate the DPoP HTTP header
    - DPoP nonce support in PingFederate is available for replay protection
requirements:
  functional:
    - id: F-001
      description: Every access token issued by PingFederate must be bound to the requesting client's proof key
    - id: F-002
      description: Resource servers must validate the DPoP proof JWT on every request and reject tokens without valid proof
    - id: F-003
      description: Token binding must work for public clients (mobile), confidential clients (backend), and partner clients
  non_functional:
    - id: NF-001
      description: DPoP proof generation on mobile must complete in < 50ms (including secure enclave signature)
    - id: NF-002
      description: DPoP proof validation at the resource server must add < 5ms latency per request at p99
    - id: NF-003
      description: No changes to existing TLS termination or CDN configuration required
alternatives:
  - name: DPoP (RFC 9449)
    summary:
      "Application-layer proof of possession using signed JWTs. The client generates an ephemeral asymmetric keypair,
      includes the public key in token requests, and presents a signed DPoP proof JWT with every API call. The access token's
      `cnf` claim contains a `jkt` thumbprint of the DPoP key.

      "
    pros:
      - Works for public clients — no certificate provisioning needed; keypair generated locally
      - Application-layer mechanism survives any TLS termination, CDN, or proxy chain
      - Ephemeral keys reduce blast radius — compromise of one key affects only that session
      - Built-in replay protection via server-issued nonces (RFC 9449 §8)
      - No infrastructure changes to CDN, load balancers, or API gateways
      - Supported natively by PingFederate 12.x and PingAccess 8.x
    cons:
      - Every API request must include an additional DPoP header (bandwidth overhead ~500 bytes)
      - Client-side implementation complexity — must generate proof JWT per request with correct `ath`, `htm`, `htu` claims
      - Clock skew between client and server can cause proof rejection — requires nonce-based mitigation
      - Newer standard (2023) — less battle-tested than mTLS in production at scale
      - No hardware-level key protection guarantee unless explicitly using device secure enclave APIs
    estimated_cost: medium
    risk: low
  - name: mTLS Certificate-Bound Tokens (RFC 8705)
    summary:
      "TLS-layer proof of possession using X.509 client certificates. The client presents a certificate during the TLS
      handshake, and the access token's `cnf` claim contains an `x5t#S256` thumbprint of the certificate. Resource servers
      verify the certificate thumbprint matches.

      "
    pros:
      - Mature, well-understood mechanism — widely deployed in financial services
      - TLS-layer binding is transparent to application code
      - Stronger hardware binding when using smart cards or TPM-backed certificates
      - No per-request proof generation — certificate is presented once during TLS handshake
    cons:
      - Not viable for public clients (mobile app) — X.509 certificate provisioning at scale is impractical
      - CDN TLS termination strips client certificates — requires expensive mTLS passthrough ($50K/year Cloudflare Enterprise
        add-on)
      - Partner corporate proxies frequently strip or re-originate client certificates
      - Certificate lifecycle management (issuance, renewal, revocation) adds operational burden per client
      - Requires PKI infrastructure and CA trust chain management
      - Self-signed client certificates complicate trust validation at resource servers
    estimated_cost: high
    risk: medium
    rejection_rationale: Not viable for public clients (mobile) due to X.509 certificate provisioning at scale. CDN TLS termination strips client certificates, requiring a $50K/year mTLS passthrough add-on. Partner corporate proxies also strip certificates.
  - name: "Hybrid: DPoP for public clients, mTLS for confidential clients"
    summary:
      "Use DPoP for mobile/SPA public clients and mTLS for server-to-server confidential clients, choosing the mechanism
      per client type.

      "
    pros:
      - Each client type uses its optimal mechanism
      - Confidential servers benefit from TLS-layer binding without per-request overhead
    cons:
      - Dual validation logic at every resource server — must support both `jkt` and `x5t#S256` in `cnf` claims
      - Testing matrix doubles — every API flow must be validated with both mechanisms
      - CDN mTLS passthrough problem still exists for the confidential client path
      - "Operational complexity: two key management systems, two debugging procedures"
      - PingFederate token policies must branch on client type, increasing configuration surface
    estimated_cost: high
    risk: medium
    rejection_rationale: Dual validation logic at every resource server doubles the testing matrix. CDN mTLS passthrough problem persists for the confidential client path. Operational complexity of maintaining two key management systems outweighs the marginal benefit.
decision:
  chosen_alternative: DPoP (RFC 9449)
  rationale: |
    - Only mechanism that works for all three client types without infrastructure modifications
    - Survives CDN TLS termination — eliminates the $50K/year Cloudflare mTLS passthrough cost
    - Mobile app (3M+ users) cannot manage X.509 certificates — DPoP ephemeral keys are generated locally
    - Partner bank proxies frequently strip client certificates — DPoP is an HTTP header, not a TLS artifact
    - Single validation path at resource servers reduces testing surface and operational complexity
    - PingFederate 12.x DPoP nonce support provides replay protection equivalent to mTLS session binding
  tradeoffs: |
    - ~500 bytes additional overhead per API request for the DPoP proof header
    - Client SDKs must implement DPoP proof generation (`ath`, `htm`, `htu` claims) — added integration effort
    - Clock skew tolerance window (±60 seconds) may need tuning per client population
    - Foregoing mTLS's hardware-level binding for software-level ephemeral keys — accepted risk for mobile
  decision_date: "2026-01-24"
  confidence: high
consequences:
  positive:
    - Unified sender-constraining across mobile, backend, and partner clients
    - No CDN or proxy configuration changes required — tokens are bound at the application layer
    - Ephemeral keypairs limit blast radius — compromised key affects only one session
    - PSD2 sender-constraining requirement satisfied for all payment API flows
  negative:
    - Per-request DPoP proof generation adds latency on mobile (20-40ms in secure enclave)
    - Client SDK complexity increases — DPoP proof must be correctly constructed for every request
    - Resource server validation adds ~2ms per request for JWK thumbprint comparison and signature verification
confirmation:
  description: "Verified via integration test suite covering all three client types (mobile, backend, partner). PingFederate DPoP nonce enforcement confirmed in staging. CDN passthrough not required — validated with Cloudflare production configuration."
  artifact_ids:
    - "https://github.com/novatrust/iam-platform/pull/142"
    - "TEST-SUITE-dpop-e2e-all-clients"
    - "POC-2026-01-dpop-cloudflare-passthrough"
    - "BENCH-dpop-proof-gen-mobile-p99"
dependencies:
  internal:
    - PingFederate 12.x (authorization server with DPoP support)
    - PingAccess 8.x (API gateway with DPoP proof validation)
    - Mobile SDK team (iOS/Android DPoP proof generation)
    - HSM infrastructure for server-side token signing keys
  external:
    - Cloudflare CDN (no changes required — DPoP is application-layer)
    - Partner API consumers (must implement DPoP proof generation)

references:
  - title: Demonstrating Proof of Possession (DPoP) — RFC 9449
    url: https://datatracker.ietf.org/doc/html/rfc9449
  - title: OAuth 2.0 Mutual-TLS Client Authentication — RFC 8705
    url: https://datatracker.ietf.org/doc/html/rfc8705
  - title: OAuth 2.1 Authorization Framework — RFC 9700
    url: https://datatracker.ietf.org/doc/html/rfc9700
  - title: PingFederate DPoP Configuration Guide
    url: https://docs.pingidentity.com/pingfederate/latest/dpop.html
lifecycle:
  review_cycle_months: 12
  next_review_date: "2027-01-24"
  superseded_by: null
  supersedes: null
  archival:
    archived_at: null
    archive_reason: null
audit_trail:
  - event: created
    by: Elena Vasquez
    at: "2026-01-10T09:00:00Z"
  - event: updated
    by: Kai Lindström
    at: "2026-01-18T14:00:00Z"
    details: Added mobile secure enclave benchmarks and CDN cost analysis
  - event: approved
    by: Marcus Chen
    at: "2026-01-24T10:00:00Z"
  - event: approved
    by: Jonas Eriksen
    at: "2026-01-25T09:00:00Z"
    details: "CISO approval with condition: DPoP nonce must be mandatory, not optional"
````

## File: examples-reference/ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.yaml
````yaml
adr:
  id: ADR-0002
  title: Use opaque reference tokens with introspection over self-contained JWTs for API gateway authorization
  summary:
    Issue opaque reference tokens instead of self-contained JWTs, enabling instant revocation via introspection while
    keeping PII out of access logs.
  status: accepted
  created_at: "2026-01-15T10:00:00Z"
  last_modified: "2026-02-01T16:00:00Z"
  version: "1.0"
  schema_version: 1.0.0
  project: API Authorization Layer — Token Format Strategy
  component: Access Token Format
  tags:
    - oauth
    - token-introspection
    - reference-tokens
    - jwt
    - rfc7662
    - api-gateway
  priority: high
  decision_type: technology
authors:
  - name: Priya Sharma
    role: API Platform Lead
    email: priya.sharma@novatrust.example.com
  - name: Elena Vasquez
    role: IAM Architect
    email: elena.vasquez@novatrust.example.com
decision_owner:
  name: Marcus Chen
  role: Head of Identity and Access Management
  email: marcus.chen@novatrust.example.com
reviewers:
  - name: Tomasz Kowalski
    role: Network Security Architect
    email: tomasz.kowalski@novatrust.example.com
  - name: Jonas Eriksen
    role: CISO
    email: jonas.eriksen@novatrust.example.com
approvals:
  - name: Marcus Chen
    role: Head of IAM
    identity: "@marcuschen"
    approved_at: "2026-01-30T11:00:00Z"
    signature_id: sig-reftok-001
  - name: Jonas Eriksen
    role: CISO
    identity: "@jonaseriksen"
    approved_at: "2026-02-01T09:00:00Z"
    signature_id: sig-reftok-002
context:
  summary: |
    With OAuth 2.1 adopted, NovaTrust must decide the format of access tokens issued by PingFederate. Self-contained JWTs encode all claims (scopes, subject, cnf, expiry) directly in the token, allowing offline validation by resource servers. Opaque reference tokens are short random strings that resource servers resolve via the Token Introspection endpoint (RFC 7662). This is a classic tradeoff: JWTs give low-latency validation but cannot be instantly revoked, while reference tokens give instant revocation but require an introspection call per request. Our API gateway (PingAccess) sits in front of all 200+ APIs and is the primary enforcement point. The choice affects latency, revocation capability, token size in logs, and regulatory auditability.
  business_drivers:
    - PSD2 requires instant consent revocation — customer must be able to revoke bank access immediately
    - GDPR right to erasure implies immediate token invalidation upon account deletion
    - Fraud detection team needs ability to kill sessions within seconds, not minutes
    - Compliance audit requires centralized proof of token validity at time of access
  technical_drivers:
    - Self-contained JWTs cannot be revoked before expiry without a distributed deny-list
    - JWT deny-lists require propagation to all resource servers — eventual consistency problem
    - PingAccess already has a high-performance introspection client with caching support
    - Token introspection response is a single audit record of active/inactive status
    - JWTs in access logs leak PII (subject, email, scopes) — requires log scrubbing
  constraints:
    - API gateway (PingAccess) is the single enforcement point — all traffic is proxied
    - PingFederate introspection endpoint must handle 5000 QPS sustained
    - "Token validation latency budget: < 10ms at p99 (including introspection + cache)"
    - Must work with DPoP sender-constraining (ADR-0001)
  assumptions:
    - PingAccess introspection cache with 30-second TTL provides acceptable revocation latency
    - PingFederate introspection endpoint can sustain 5000 QPS with current cluster sizing
    - Reference tokens do not leak claims in client-side storage or network logs
requirements:
  functional:
    - id: F-001
      description: Access tokens must be revocable within 30 seconds of revocation request
    - id: F-002
      description: API gateway must resolve token to full claim set via introspection before forwarding request
    - id: F-003
      description: Introspection response must include DPoP confirmation (`cnf.jkt`) for sender validation
  non_functional:
    - id: NF-001
      description: Token introspection latency < 5ms at p99 with caching enabled
    - id: NF-002
      description: PingFederate introspection endpoint availability 99.99%
    - id: NF-003
      description: Token value must not contain PII when stored in access logs
alternatives:
  - name: Opaque reference tokens with introspection
    summary: |
      PingFederate issues short opaque strings (128-bit random). PingAccess calls the introspection endpoint (RFC 7662) on each request, caching the response for a configurable TTL (default 30 seconds). Revocation is immediate at the authorization server; cached entries expire within TTL.
    pros:
      - Instant revocation — token marked inactive immediately at PingFederate
      - No PII in the token itself — safe to log, store, and transmit
      - Smaller token size (~32 bytes vs ~800 bytes for JWT) — less bandwidth and storage
      - "Centralized audit: introspection logs prove token was active at time of access"
      - Token format changes (new claims) do not require client or resource server updates
    cons:
      - Every request requires an introspection call (mitigated by caching)
      - Introspection endpoint is a runtime dependency — outage blocks all API access
      - Cache TTL creates a revocation latency window (default 30 seconds)
      - No offline validation — disconnected resource servers cannot validate tokens
    estimated_cost: medium
    risk: medium
  - name: Self-contained JWTs with short lifetime
    summary: |
      PingFederate issues signed JWTs containing all claims. Resource servers validate the signature and expiry locally without contacting the authorization server. Short token lifetime (5 minutes) limits the revocation gap.
    pros:
      - No runtime dependency on introspection endpoint — fully offline validation
      - Zero additional latency per request — signature verification is ~0.5ms
      - Resource servers can extract claims directly from the token
      - Well-understood pattern with extensive library support
    cons:
      - Cannot be revoked before expiry — 5-minute window of unrevocable access
      - PII embedded in JWT (sub, email, scopes) appears in logs, browser history, and caches
      - 5-minute revocation gap violates PSD2 instant revocation interpretation
      - Large token size (~800 bytes) — multiplied by DPoP proof header, total overhead ~1.3KB per request
      - Adding or changing claims requires updating all resource server validation logic
      - "GDPR: token deletion does not remove PII already logged in transit"
    estimated_cost: low
    risk: high
    rejection_rationale:
      5-minute revocation gap violates PSD2 instant revocation interpretation. PII embedded in JWT appears
      in logs, violating GDPR data minimization. Adding or changing claims requires updating all resource server validation
      logic.
  - name: JWT with distributed deny-list (Redis)
    summary: |
      Issue JWTs but maintain a Redis-backed deny-list. Resource servers check the deny-list on every request. Revoked token JTIs are pushed to Redis; resource servers query before accepting.
    pros:
      - Adds revocation capability to JWTs
      - Resource servers still validate signature offline for non-revoked tokens
    cons:
      - Redis deny-list is a distributed runtime dependency — same availability concern as introspection
      - Deny-list propagation has eventual consistency — cache invalidation is hard
      - PII still embedded in JWT — logging and GDPR concerns remain
      - Custom implementation — no standardized protocol (unlike RFC 7662 introspection)
      - "Two validation steps per request: signature verification + deny-list lookup"
      - Deny-list grows unbounded unless TTL matches token expiry — memory pressure
    estimated_cost: medium
    risk: high
    rejection_rationale:
      Redis deny-list has the same availability concern as introspection but is a custom, non-standard solution.
      PII remains embedded in JWTs. Deny-list propagation has eventual consistency — same revocation gap problem as plain JWTs.
decision:
  chosen_alternative: Opaque reference tokens with introspection
  rationale: |
    - PSD2 instant revocation: opaque tokens can be revoked in < 1 second at PingFederate; cache TTL provides 30-second worst-case
    - No PII in the token: access logs can retain tokens without GDPR scrubbing obligations
    - PingAccess introspection caching (30s TTL) measured at 0.8ms p99 cache-hit latency in load test — well within 10ms budget
    - Centralized introspection provides auditable proof of token status at exact time of API access
    - Simpler operational model: one revocation mechanism (mark inactive) vs. distributed deny-list synchronization
    - Token format evolution (new claims, changed scopes) is transparent to resource servers — only introspection response changes
  tradeoffs: |
    - Runtime dependency on PingFederate introspection endpoint — mitigated by multi-node cluster and PingAccess cache
    - 30-second cache TTL means a revoked token may be accepted for up to 30 seconds after revocation
    - Introspection calls add ~0.8ms (cache hit) to ~4ms (cache miss) per request vs. ~0.5ms for local JWT validation
    - Cannot work in fully disconnected environments — accepted because PingAccess is always network-connected
  decision_date: "2026-01-30"
  confidence: high
consequences:
  positive:
    - Instant token revocation for fraud response and customer consent withdrawal
    - GDPR-safe token format — no PII leakage in logs, caches, or browser storage
    - Auditable introspection trail for every API access decision
    - Smaller wire format reduces bandwidth across 200+ APIs at 5000 QPS
  negative:
    - PingFederate introspection endpoint becomes Tier-0 dependency
    - 30-second revocation latency window due to PingAccess caching
    - Slightly higher per-request latency (0.8ms cache-hit vs 0.5ms JWT verification)
confirmation:
  description: "Code review of gateway introspection configuration. Validate token format in staging by inspecting Authorization header at API gateway."

dependencies:
  internal:
    - PingFederate 12.x (introspection endpoint)
    - PingAccess 8.x (introspection client with caching)
    - HSM infrastructure for token store encryption
  external:
    - None — introspection is an internal call between PingAccess and PingFederate
references:
  - title: OAuth 2.0 Token Introspection — RFC 7662
    url: https://datatracker.ietf.org/doc/html/rfc7662
  - title: OAuth 2.1 Authorization Framework — RFC 9700
    url: https://datatracker.ietf.org/doc/html/rfc9700
  - title: PingFederate Token Management Documentation
    url: https://docs.pingidentity.com/pingfederate/latest/token-management.html
lifecycle:
  review_cycle_months: 12
  next_review_date: "2027-01-30"
  superseded_by: null
  supersedes: null
  archival:
    archived_at: null
    archive_reason: null
audit_trail:
  - event: created
    by: Priya Sharma
    at: "2026-01-15T10:00:00Z"
  - event: updated
    by: Elena Vasquez
    at: "2026-01-22T09:00:00Z"
    details: Added introspection cache latency benchmarks from staging load test
  - event: approved
    by: Marcus Chen
    at: "2026-01-30T11:00:00Z"
  - event: approved
    by: Jonas Eriksen
    at: "2026-02-01T09:00:00Z"
    details: "CISO condition: emergency cache purge API must be implemented before GA"
````

## File: examples-reference/ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.yaml
````yaml
adr:
  id: ADR-0003
  title: Use pairwise pseudonymous subject identifiers over public subject identifiers for OIDC relying parties
  summary:
    Switch from public to pairwise pseudonymous subject identifiers (PPID) to prevent cross-RP user correlation, satisfying
    GDPR data minimization and eIDAS 2.0 unlinkability.
  status: accepted
  created_at: "2025-11-01T08:00:00Z"
  last_modified: "2025-12-15T11:00:00Z"
  version: "1.0"
  schema_version: 1.0.0
  project: Enterprise IdP — OIDC Claim Strategy
  component: Subject Identifier Type
  tags:
    - oidc
    - pairwise-sub
    - privacy
    - gdpr
    - claim-strategy
    - pseudonymization
  priority: high
  decision_type: security
authors:
  - name: Elena Vasquez
    role: IAM Architect
    email: elena.vasquez@novatrust.example.com
  - name: Aisha Mbeki
    role: Privacy Engineer
    email: aisha.mbeki@novatrust.example.com
decision_owner:
  name: Marcus Chen
  role: Head of Identity and Access Management
  email: marcus.chen@novatrust.example.com
reviewers:
  - name: Jonas Eriksen
    role: CISO
    email: jonas.eriksen@novatrust.example.com
  - name: DPO
    role: Data Protection Officer
    email: dpo@novatrust.example.com
  - name: Priya Sharma
    role: API Platform Lead
    email: priya.sharma@novatrust.example.com
approvals:
  - name: Marcus Chen
    role: Head of IAM
    identity: "@marcuschen"
    approved_at: "2025-12-10T09:00:00Z"
    signature_id: sig-ppid-001
  - name: DPO
    role: Data Protection Officer
    identity: "@dpo-novatrust"
    approved_at: "2025-12-14T11:00:00Z"
    signature_id: sig-ppid-002
context:
  summary: |
    NovaTrust's PingFederate IdP issues OIDC ID tokens with a `sub` claim to all relying parties (RPs). The OIDC Core specification (§8) defines two subject identifier types: `public` (same `sub` value for a user across all RPs) and `pairwise` (unique pseudonymous `sub` per RP). Currently, all RPs receive the same public `sub` — the user's internal UUID. This allows any two colluding RPs to correlate users across services. With 35+ internal RPs, 15 partner bank RPs, and upcoming EUDI Wallet relying party integrations, the GDPR data minimization principle and eIDAS 2.0 unlinkability requirements demand that we prevent cross-RP user correlation unless explicitly authorized.
  business_drivers:
    - GDPR Article 5(1)(c) data minimization — relying parties receive more identifying data than necessary
    - eIDAS 2.0 / EUDI Wallet unlinkability requirement — wallet RPs must not correlate users across verifiers
    - "Dutch DPA (Autoriteit Persoonsgegevens) audit finding: cross-RP correlation risk rated 'high'"
    - Partner bank RPs have contractual data silo obligations — public sub violates data partitioning agreements
  technical_drivers:
    - Public sub (internal UUID) leaks user identity to all RPs regardless of consent
    - Cross-RP correlation is trivially possible when all RPs share the same sub value
    - PingFederate supports pairwise sub natively via sector identifier and salt-based PPID generation
    - OIDC Core §8 pairwise algorithm is deterministic — same user always gets same sub for same RP
  constraints:
    - Internal workforce SSO RPs may need public sub for identity correlation (HR, payroll, helpdesk)
    - PingFederate must support both public and pairwise simultaneously per RP registration
    - Migration must not break existing RP user databases that key on the current public sub
    - Pairwise sub must be deterministic — user gets same sub for same RP across sessions
  assumptions:
    - PingFederate's PPID implementation uses HMAC-SHA256(sector_id + user_id + salt) — collision-resistant
    - RPs can re-key their user databases from public sub to pairwise sub with a one-time migration
    - Internal workforce RPs can be grouped in a shared sector identifier to maintain correlation within the sector
requirements:
  functional:
    - id: F-001
      description: All external and partner RPs must receive pairwise pseudonymous sub values
    - id: F-002
      description: Internal workforce RPs grouped by sector identifier may receive shared sub within their sector
    - id: F-003
      description: The same user must receive the same pairwise sub for the same RP across all sessions (deterministic)
  non_functional:
    - id: NF-001
      description: PPID generation must add < 1ms to token issuance latency
    - id: NF-002
      description: Pairwise sub must be a 128-bit hex string (32 characters) — no PII derivable from the value
    - id: NF-003
      description: PPID salt must be stored in HSM and never exposed to application layer
alternatives:
  - name: Pairwise pseudonymous subject identifiers (PPID)
    summary: |
      PingFederate generates a unique `sub` per RP using HMAC-SHA256(sector_id + user_id + salt). External and partner RPs each receive a distinct, unlinkable identifier. Internal workforce RPs share a sector identifier so HR, payroll, and helpdesk can still correlate users within their sector.
    pros:
      - Prevents cross-RP user correlation — two partner RPs cannot link the same user
      - "GDPR data minimization: sub value is pseudonymous — no PII derivable"
      - "eIDAS 2.0 unlinkability: satisfies wallet RP requirements for credential presentation"
      - "Deterministic: same user always gets same sub for same RP — no session-to-session drift"
      - Sector grouping allows controlled correlation for legitimate business needs (workforce apps)
      - PingFederate native support — no custom code required
    cons:
      - "Migration effort: existing RPs must re-key user databases from public sub to pairwise sub"
      - Account linking across RPs becomes impossible without explicit user consent and IdP mediation
      - "Debugging and support: 'which user is sub abc123?' requires IdP lookup — not human-readable"
      - PPID salt is a critical secret — compromise allows pre-computation of all pairwise values
      - Sector identifier assignment requires governance — incorrect grouping defeats purpose
    estimated_cost: medium
    risk: low
  - name: Public subject identifiers with contractual controls
    summary: |
      Continue using the user's internal UUID as the public sub for all RPs, but enforce cross-RP correlation restrictions via contractual agreements and API usage auditing.
    pros:
      - No migration effort — RPs continue using existing sub values
      - Simple debugging — sub is the user's UUID, directly queryable
      - Account linking across RPs is straightforward
    cons:
      - Cross-RP correlation is trivially possible despite contractual prohibitions
      - Contracts are not enforced technically — a colluding partner can correlate silently
      - "GDPR data minimization violation: providing full UUID when a pseudonym suffices"
      - Dutch DPA explicitly flagged this as high-risk in their 2025 audit
      - eIDAS 2.0 unlinkability requirement cannot be met with public identifiers
      - API auditing detects correlation after the fact, not preventing it
    estimated_cost: low
    risk: high
    rejection_rationale:
      Cross-RP correlation is trivially possible despite contractual controls. Dutch DPA explicitly flagged
      this as high-risk. eIDAS 2.0 unlinkability cannot be met with public identifiers. Contracts are not technically enforceable.
  - name: Encrypted subject identifiers (JWE-wrapped sub)
    summary: |
      Issue the sub as a JWE-encrypted blob per RP, where only the RP can decrypt its own sub. Different encryption keys per RP prevent cross-RP correlation.
    pros:
      - Prevents cross-RP correlation via encryption rather than pseudonymization
      - RP-specific decryption keys provide cryptographic isolation
    cons:
      - "Non-standard: OIDC Core does not define encrypted sub — breaks spec compliance"
      - RP must manage decryption keys and decrypt sub on every token receipt
      - "Significantly larger sub values (JWE overhead: ~200 bytes vs 32-byte PPID)"
      - Key rotation for JWE-encrypted subs requires coordinated rollover with every RP
      - PingFederate does not support this natively — requires custom plugin development
      - Debugging is harder than PPID — sub is opaque even to the IdP without RP key
    estimated_cost: high
    risk: high
    rejection_rationale:
      Non-standard — OIDC Core does not define encrypted sub, breaking spec compliance. JWE overhead makes
      sub ~200 bytes vs 32-byte PPID. PingFederate does not support this natively, requiring custom plugin development and per-RP
      key management.
decision:
  chosen_alternative: Pairwise pseudonymous subject identifiers (PPID)
  rationale: |
    - Standards-compliant: OIDC Core §8 defines pairwise as a first-class subject identifier type
    - Dutch DPA audit finding directly addressed — cross-RP correlation eliminated by design
    - eIDAS 2.0 unlinkability requirement met for upcoming EUDI Wallet RP integrations
    - PingFederate native support eliminates custom development — configuration-only change
    - Sector grouping provides pragmatic exception for internal workforce RPs that legitimately need correlation
    - HMAC-SHA256 PPID generation is deterministic and collision-resistant — no session-to-session drift
  tradeoffs: |
    - One-time migration: 35+ internal RPs and 15 partner RPs must re-key user databases
    - Support team loses ability to look up user by sub without IdP reverse-lookup tool
    - Cross-RP account linking requires explicit consent flow — cannot be done silently
    - PPID salt in HSM adds dependency on HSM availability for token issuance
  decision_date: "2025-12-10"
  confidence: high
consequences:
  positive:
    - Cross-RP user correlation eliminated for all external and partner RPs
    - "GDPR data minimization: sub values are pseudonymous with no derivable PII"
    - "eIDAS 2.0 readiness: pairwise sub satisfies unlinkability for wallet credential presentation"
    - Dutch DPA audit finding resolved — risk downgraded from 'high' to 'low'
  negative:
    - 3-month migration project for RP user database re-keying
    - Support team requires new tooling for user-to-sub reverse lookup
    - PPID salt in HSM creates an additional HSM dependency for token issuance
confirmation:
  description: "Verify pairwise subject identifiers in token responses across relying parties. Confirm no cross-RP correlation is possible via automated test suite."

dependencies:
  internal:
    - PingFederate 12.x (pairwise sub support)
    - HSM infrastructure (PPID salt storage)
    - IAM Architecture Board (sector identifier governance)
  external:
    - Partner bank RPs (must accept new sub values during migration)
references:
  - title: OpenID Connect Core 1.0 — §8 Subject Identifier Types
    url: https://openid.net/specs/openid-connect-core-1_0.html#SubjectIDTypes
  - title: GDPR Article 5(1)(c) — Data Minimization
    url: https://gdpr-info.eu/art-5-gdpr/
  - title: eIDAS 2.0 Regulation — Unlinkability Requirements
    url: https://eur-lex.europa.eu/eli/reg/2024/1183/oj
lifecycle:
  review_cycle_months: 12
  next_review_date: "2026-12-10"
  superseded_by: null
  supersedes: null
  archival:
    archived_at: null
    archive_reason: null
audit_trail:
  - event: created
    by: Elena Vasquez
    at: "2025-11-01T08:00:00Z"
  - event: updated
    by: Aisha Mbeki
    at: "2025-11-20T14:00:00Z"
    details: Added Dutch DPA audit finding reference and eIDAS 2.0 unlinkability analysis
  - event: approved
    by: Marcus Chen
    at: "2025-12-10T09:00:00Z"
  - event: approved
    by: DPO
    at: "2025-12-14T11:00:00Z"
    details: "DPO approval with condition: PPID salt must be in HSM, and reverse-lookup must be audit-logged"
````

## File: examples-reference/ADR-0004-ed25519-over-rsa-for-jwt-signing.yaml
````yaml
adr:
  id: ADR-0004
  title: Use Ed25519 (EdDSA) over RSA-2048 for JWT and assertion signing keys
  summary:
    Migrate from RSA-2048 (RS256) to Ed25519 (EdDSA) for all JWT/JWS signing to achieve 20x throughput improvement,
    eliminating the PingFederate CPU bottleneck.
  status: accepted
  created_at: "2025-11-20T09:00:00Z"
  last_modified: "2025-12-20T10:00:00Z"
  version: "1.0"
  schema_version: 1.0.0
  project: Cryptographic Infrastructure — Signing Key Strategy
  component: JWT Signing Algorithm
  tags:
    - cryptography
    - ed25519
    - eddsa
    - rsa
    - jwt
    - jws
    - rfc8037
    - performance
  priority: high
  decision_type: technology
authors:
  - name: Tomasz Kowalski
    role: Network Security Architect
    email: tomasz.kowalski@novatrust.example.com
  - name: Elena Vasquez
    role: IAM Architect
    email: elena.vasquez@novatrust.example.com
decision_owner:
  name: Jonas Eriksen
  role: CISO
  email: jonas.eriksen@novatrust.example.com
reviewers:
  - name: Marcus Chen
    role: Head of IAM
    email: marcus.chen@novatrust.example.com
  - name: Kai Lindström
    role: Mobile Platform Lead
    email: kai.lindstrom@novatrust.example.com
approvals:
  - name: Jonas Eriksen
    role: CISO
    identity: "@jonaseriksen"
    approved_at: "2025-12-18T14:00:00Z"
    signature_id: sig-ed25519-001
  - name: Marcus Chen
    role: Head of IAM
    identity: "@marcuschen"
    approved_at: "2025-12-19T10:00:00Z"
    signature_id: sig-ed25519-002
context:
  summary: |
    NovaTrust's PingFederate IdP and all JWT-producing services currently use RS256 (RSA-2048 with PKCS#1 v1.5 padding) for signing ID tokens, access tokens (when issued as JWTs), SAML assertions, and DPoP proofs. With 5000+ token issuances per second at peak, RSA-2048 signing is the primary CPU bottleneck on the PingFederate cluster. EdDSA with Ed25519 (RFC 8037, JWS algorithm "EdDSA") offers vastly superior signing performance, smaller key sizes, and resistance to implementation pitfalls (no padding oracle attacks, no nonce reuse vulnerabilities as in ECDSA). However, Ed25519 is newer and has less universal library support than RSA. We must choose the signing algorithm for all new JWT/JWS production.
  business_drivers:
    - PingFederate cluster CPU at 78% during peak — projected to exceed capacity in 6 months
    - Avoiding $120K/year in additional PingFederate cluster nodes by reducing signing CPU
    - Mobile app token validation latency impacts UX — faster verification is a competitive advantage
  technical_drivers:
    - "RSA-2048 signing: ~1500 ops/sec per core; Ed25519 signing: ~30,000 ops/sec per core (20x faster)"
    - "RSA-2048 verification: ~40,000 ops/sec per core; Ed25519 verification: ~15,000 ops/sec per core"
    - "Ed25519 key: 32 bytes; RSA-2048 key: 256 bytes — JWK set transmission is 8x smaller"
    - Ed25519 is deterministic (no random nonce) — eliminates ECDSA-style nonce reuse attacks
    - "JWS compact serialization with Ed25519 signature: 64 bytes vs RSA-2048: 256 bytes"
    - PingFederate 12.x added EdDSA support in Q3 2025
  constraints:
    - Cloud HSM must support Ed25519 key generation and signing (PKCS#11 with CKM_EDDSA)
    - All resource servers and relying parties must support Ed25519 verification
    - SAML assertion signing must use a supported XML signature algorithm
    - Must maintain RSA-2048 for legacy partner integrations that cannot upgrade
  assumptions:
    - Cloud HSM supports Ed25519 via CKM_EDDSA mechanism (verified in vendor documentation)
    - All modern JWT libraries (jose4j, nimbus-jose, PyJWT, jsonwebtoken) support EdDSA verification
    - SAML XML Signature for Ed25519 is supported via http://www.w3.org/2021/04/xmldsig-more#eddsa-ed25519
    - Legacy partners (3 of 15) will migrate to Ed25519 within 18 months
requirements:
  functional:
    - id: F-001
      description: All new JWT/JWS tokens signed with EdDSA (Ed25519) algorithm
    - id: F-002
      description: JWKS endpoint publishes both Ed25519 and RSA-2048 keys during transition period
    - id: F-003
      description: Legacy partners continue receiving RS256-signed tokens until they support EdDSA
  non_functional:
    - id: NF-001
      description: Token signing throughput must increase by at least 10x per core
    - id: NF-002
      description: Token signing latency p99 < 1ms (including HSM round-trip)
    - id: NF-003
      description: JWS compact serialization total size reduced by at least 30% compared to RS256
alternatives:
  - name: EdDSA with Ed25519 (RFC 8037)
    summary: |
      Use the EdDSA algorithm with Ed25519 curve for all JWT/JWS signing. Ed25519 provides 128-bit security with 32-byte keys and 64-byte signatures. Signing is deterministic (no random nonce), eliminating nonce-related vulnerabilities.
    pros:
      - 20x faster signing than RSA-2048 — directly addresses PingFederate CPU bottleneck
      - Deterministic signatures — no nonce reuse vulnerability (unlike ECDSA with P-256)
      - 64-byte signatures vs 256-byte RSA — 75% reduction in JWS signature size
      - 32-byte keys vs 256-byte RSA public keys — smaller JWKS responses
      - No padding oracle attacks — Ed25519 has no padding scheme
      - 128-bit security level — equivalent to RSA-3072 or ECDSA P-256
      - "Growing industry adoption: Signal, SSH, TLS 1.3, FIDO2 all use Ed25519"
    cons:
      - "Not universally supported: 3 legacy partner integrations require RS256"
      - Cloud HSM EdDSA support is newer — less operational track record
      - Verification is 2.5x slower than RSA-2048 verification (matters for resource servers)
      - SAML XML Signature Ed25519 support requires relying parties to upgrade XML libraries
      - Ed25519 is Curve25519-based — not NIST-approved (may matter for US government partners)
    estimated_cost: medium
    risk: low
  - name: ECDSA with P-256 (ES256)
    summary: |
      Use ECDSA with the NIST P-256 curve (JWS algorithm ES256). Provides 128-bit security with smaller keys and signatures than RSA.
    pros:
      - Widely supported — NIST P-256 is the most common elliptic curve
      - Smaller signatures than RSA (64 bytes DER-encoded, typically 70-72 bytes)
      - 5-10x faster signing than RSA-2048
      - NIST-approved curve — satisfies US government compliance requirements
    cons:
      - "Non-deterministic: requires a secure random nonce per signature — nonce reuse leaks the private key"
      - Sony PS3 and Bitcoin ECDSA nonce-reuse incidents demonstrate real-world risk
      - Requires RFC 6979 deterministic ECDSA for safety — not all libraries implement it by default
      - Signing is 3x slower than Ed25519
      - P-256 curve has concerns about NIST backdoor potential (Dual_EC_DRBG precedent)
      - HSM implementations may not use RFC 6979 — must verify per HSM vendor
    estimated_cost: medium
    risk: medium
    rejection_rationale:
      Non-deterministic signatures require secure random nonce per signature — nonce reuse leaks the private
      key (real-world incidents with Sony PS3 and Bitcoin). 3x slower signing than Ed25519. P-256 backdoor concerns from NIST
      Dual_EC_DRBG precedent.
  - name: RSA-2048 with PS256 (RSASSA-PSS)
    summary: |
      Upgrade from RS256 (PKCS#1 v1.5) to PS256 (RSASSA-PSS) padding while keeping RSA-2048 keys. Addresses padding oracle vulnerabilities without changing key type.
    pros:
      - No key type change — all libraries already support RSA
      - PSS padding eliminates PKCS#1 v1.5 padding oracle attacks
      - Universal partner compatibility
    cons:
      - Does not address the CPU bottleneck — signing throughput remains ~1500 ops/sec per core
      - PingFederate cluster still needs $120K/year in additional capacity
      - 256-byte signatures — no size reduction
      - RSA-2048 approaching end of recommended lifetime (NIST recommends RSA-3072 after 2030)
    estimated_cost: low
    risk: low
    rejection_rationale:
      Does not address the CPU bottleneck — signing throughput remains ~1500 ops/sec. PingFederate cluster
      would still require $120K/year in additional nodes. RSA-2048 approaching NIST end-of-life recommendation (RSA-3072 after
      2030).
decision:
  chosen_alternative: EdDSA with Ed25519 (RFC 8037)
  rationale: |
    - 20x signing throughput improvement directly solves PingFederate CPU bottleneck — avoids $120K/year in additional nodes
    - Deterministic signatures eliminate the nonce-reuse risk class entirely — superior to ECDSA P-256
    - 75% signature size reduction improves wire efficiency across 200+ APIs at 5000 QPS
    - 128-bit security equivalent to ECDSA P-256 without the nonce-related attack surface
    - Industry momentum: Ed25519 is the default in SSH, Signal, TLS 1.3, and FIDO2
    - Legacy partner compatibility maintained via dual-key JWKS (Ed25519 primary, RSA-2048 fallback)
  tradeoffs: |
    - Verification is 2.5x slower than RSA-2048 — accepted because resource servers are not CPU-bound on verification
    - 3 legacy partners require RS256 fallback — dual-key JWKS maintained for 18-month transition
    - Not NIST-approved — accepted because NovaTrust has no US government compliance requirement
    - Cloud HSM Ed25519 support is newer — mitigated by vendor SLA and pre-production validation
  decision_date: "2025-12-18"
  confidence: medium
consequences:
  positive:
    - PingFederate signing capacity increased 20x — cluster can handle 100K tokens/sec on current hardware
    - Estimated $120K/year savings by avoiding additional PingFederate nodes
    - JWS token size reduced by ~192 bytes per token (signature + key reference)
    - Nonce-reuse vulnerability class eliminated by design
  negative:
    - Dual-key JWKS management during 18-month RSA transition
    - Resource server verification ~0.5ms slower per token (15K vs 40K ops/sec)
    - SAML XML libraries at partner sites may need updating for Ed25519 support
confirmation:
  description:
    "Ed25519 signing validated in pre-production: 72-hour sustained load test at 50K ops/sec on Cloud HSM. All
    12 internal resource servers verified EdDSA token consumption. Three legacy partners confirmed RS256 fallback path. PingFederate
    per-RP algorithm override tested."
  artifact_ids:
    - BENCH-ed25519-hsm-72h-load-test
    - TEST-SUITE-jwt-signing-ed25519-all-rps
    - https://github.com/novatrust/iam-platform/pull/198
dependencies:
  internal:
    - Cloud HSM with CKM_EDDSA support
    - PingFederate 12.x (EdDSA signing support)
    - All resource servers (JWT verification library updates)
  external:
    - Cloud HSM provider (EdDSA firmware support)
    - Partner relying parties (EdDSA verification capability)
references:
  - title: CFRG Edwards-Curve Digital Signature Algorithm (EdDSA) — RFC 8032
    url: https://datatracker.ietf.org/doc/html/rfc8032
  - title: CFRG Elliptic Curves for JOSE — RFC 8037
    url: https://datatracker.ietf.org/doc/html/rfc8037
  - title: JSON Web Algorithms (JWA) — RFC 7518
    url: https://datatracker.ietf.org/doc/html/rfc7518
  - title: Ed25519 Performance Benchmarks — libsodium
    url: https://doc.libsodium.org/public-key_cryptography/public-key_signatures
lifecycle:
  review_cycle_months: 12
  next_review_date: "2026-12-18"
  superseded_by: null
  supersedes: null
  archival:
    archived_at: null
    archive_reason: null
audit_trail:
  - event: created
    by: Tomasz Kowalski
    at: "2025-11-20T09:00:00Z"
  - event: updated
    by: Elena Vasquez
    at: "2025-12-05T10:00:00Z"
    details: Added ECDSA P-256 nonce-reuse risk analysis and HSM CKM_EDDSA verification
  - event: approved
    by: Jonas Eriksen
    at: "2025-12-18T14:00:00Z"
    details: "CISO approval with condition: algorithm downgrade protection must be enforced at all resource servers"
  - event: approved
    by: Marcus Chen
    at: "2025-12-19T10:00:00Z"
````

## File: examples-reference/ADR-0005-bff-token-mediator-for-spa-token-acquisition.yaml
````yaml
adr:
  id: ADR-0005
  title: Use the Backend-for-Frontend token mediator pattern over direct SPA-to-AS authorization for single-page applications
  summary:
    Adopt the BFF/Token Mediator pattern so OAuth tokens never reach the browser, eliminating XSS-based token theft
    for the banking portal.
  status: accepted
  created_at: "2026-02-01T10:00:00Z"
  last_modified: "2026-02-20T09:00:00Z"
  version: "1.0"
  schema_version: 1.0.0
  project: Customer Portal — SPA Authentication Architecture
  component: SPA Token Acquisition Pattern
  tags:
    - bff
    - spa
    - oauth
    - token-handler
    - csrf
    - cookie
    - public-client
  priority: high
  decision_type: security
authors:
  - name: Priya Sharma
    role: API Platform Lead
    email: priya.sharma@novatrust.example.com
  - name: Kai Lindström
    role: Mobile Platform Lead
    email: kai.lindstrom@novatrust.example.com
decision_owner:
  name: Marcus Chen
  role: Head of Identity and Access Management
  email: marcus.chen@novatrust.example.com
reviewers:
  - name: Elena Vasquez
    role: IAM Architect
    email: elena.vasquez@novatrust.example.com
  - name: Jonas Eriksen
    role: CISO
    email: jonas.eriksen@novatrust.example.com
  - name: Frontend Development Lead
    role: Engineering
    email: frontend-lead@novatrust.example.com
approvals:
  - name: Marcus Chen
    role: Head of IAM
    identity: "@marcuschen"
    approved_at: "2026-02-18T10:00:00Z"
    signature_id: sig-bff-001
  - name: Jonas Eriksen
    role: CISO
    identity: "@jonaseriksen"
    approved_at: "2026-02-20T09:00:00Z"
    signature_id: sig-bff-002
context:
  summary: |
    NovaTrust is rebuilding the customer banking portal as a React single-page application (SPA). SPAs are public OAuth clients — they cannot hold a client secret because all code runs in the browser. The SPA needs to obtain access tokens to call backend APIs. Two patterns exist: (1) the SPA directly performs the OAuth 2.1 Authorization Code + PKCE flow and stores tokens in browser memory, or (2) a Backend-for-Frontend (BFF) / Token Mediator component performs the OAuth flow server-side and issues secure HTTP-only cookies to the SPA. The choice affects token storage security (XSS exposure), CSRF handling, and the overall security posture of the banking portal where high-value transactions are at stake.
  business_drivers:
    - Customer banking portal handles payments, account management, and PSD2 consent — high-value target
    - Cyber insurance underwriter flagged client-side token storage as a risk for the banking portal
    - Competitor breach involved XSS-based access token theft from SPA localStorage
    - PSD2 SCA and fraud prevention require defense-in-depth for token handling
  technical_drivers:
    - SPAs store tokens in JavaScript-accessible memory — vulnerable to XSS token extraction
    - Browser-based token renewal (silent refresh via iframe) is fragile with third-party cookie deprecation
    - BFF pattern keeps tokens server-side — SPA never sees or stores access/refresh tokens
    - HTTP-only, SameSite=Strict cookies are not accessible to JavaScript — immune to XSS token theft
    - BFF can be a confidential client (has a client secret) — eligible for stronger token binding
    - OAuth 2.0 for Browser-Based Applications (draft-ietf-oauth-browser-based-apps) recommends the BFF pattern
  constraints:
    - SPA is React-based, served from CDN (static hosting) — SPA itself has no server-side component
    - BFF must be deployed as a lightweight proxy alongside the API gateway
    - Cookie domain must be first-party (same-site) to the SPA origin
    - Must work with DPoP sender-constraining (ADR-0001) — BFF performs DPoP proof generation
  assumptions:
    - BFF can be a stateless reverse proxy (no session store) using encrypted cookie for state
    - SameSite=Strict cookies prevent CSRF for same-origin API calls
    - BFF adds < 5ms latency per proxied API request
    - Content Security Policy (CSP) mitigates XSS risk, but is not a sufficient sole defense
requirements:
  functional:
    - id: F-001
      description: SPA must never receive, store, or have JavaScript access to access tokens or refresh tokens
    - id: F-002
      description: BFF performs OAuth 2.1 Authorization Code + PKCE flow as a confidential client
    - id: F-003
      description: BFF issues HTTP-only, Secure, SameSite=Strict cookies to the SPA for session management
    - id: F-004
      description: BFF generates DPoP proofs server-side and attaches them when calling backend APIs
  non_functional:
    - id: NF-001
      description: BFF proxy latency < 5ms per request at p99
    - id: NF-002
      description: BFF must handle 2000 concurrent sessions without degradation
    - id: NF-003
      description: Cookie-based session must survive browser tab close and resume
alternatives:
  - name: Backend-for-Frontend (BFF) Token Mediator
    summary: |
      A lightweight server-side component sits between the SPA and the authorization server. The BFF performs the OAuth 2.1 flow as a confidential client, stores tokens server-side (or in encrypted HTTP-only cookies), and the SPA authenticates with the BFF using HTTP-only cookies. The SPA never touches OAuth tokens.
    pros:
      - Tokens never exposed to JavaScript — immune to XSS-based token theft
      - BFF is a confidential client — can hold a client secret and use stronger authentication
      - HTTP-only SameSite=Strict cookies prevent both XSS access and CSRF
      - Token renewal is server-side — no fragile iframe silent refresh
      - BFF can generate DPoP proofs server-side with a stable keypair
      - Recommended by IETF OAuth Browser-Based Applications BCP
      - Content Security Policy (CSP) + BFF provides defense-in-depth
    cons:
      - Additional component to deploy, monitor, and maintain
      - Adds ~2-3ms latency per proxied API request
      - "Cookie management adds complexity: domain alignment, expiry, rotation"
      - CORS configuration needed if BFF and SPA are on different subdomains
      - SPA cannot make direct API calls to third-party domains — all traffic proxied through BFF
    estimated_cost: medium
    risk: low
  - name: Direct SPA-to-AS with in-memory tokens
    summary: |
      The SPA performs the OAuth 2.1 Authorization Code + PKCE flow directly as a public client. Tokens are stored in JavaScript closures (in-memory) and never persisted to localStorage or sessionStorage. Token renewal uses refresh tokens with rotation.
    pros:
      - No additional server component — simpler deployment
      - SPA has direct access to token claims for UI decisions
      - Lower barrier to entry for frontend developers
      - No cookie management complexity
    cons:
      - Tokens in JavaScript memory are accessible to XSS — any injected script can extract them
      - In-memory storage means tokens lost on page reload — user must re-authenticate
      - Public client cannot hold client secret — weaker client authentication
      - Refresh token rotation is the only defense against token theft — single-use detection is not instant
      - Silent refresh via iframe breaks with third-party cookie deprecation (Chrome, Firefox)
      - DPoP proof generation must happen in browser JavaScript — key material in JS is XSS-extractable
      - Cyber insurance underwriter explicitly flagged this as unacceptable for banking portal
    estimated_cost: low
    risk: high
    rejection_rationale:
      Tokens in JavaScript memory are accessible to XSS. Cyber insurance underwriter explicitly flagged client-side
      token storage as unacceptable for the banking portal. Silent refresh breaks with third-party cookie deprecation.
  - name: Service Worker token cache with encrypted storage
    summary: |
      Tokens stored in the browser via Service Worker with encrypted IndexedDB. Service Worker intercepts API calls and attaches tokens, isolating them from the main JavaScript thread.
    pros:
      - Tokens isolated from main JS thread — Service Worker has its own scope
      - Encrypted storage adds a layer of protection
      - No server-side component needed
    cons:
      - Service Worker scope isolation is not a security boundary — XSS in the main thread can message the Service Worker
      - Encrypted IndexedDB key must be stored somewhere accessible — chicken-and-egg problem
      - Non-standard pattern — no industry consensus or IETF guidance
      - Service Worker lifecycle complexity (registration, update, activation)
      - "Does not address the fundamental issue: browser JS environment is untrusted"
      - No major financial institution has adopted this pattern in production
    estimated_cost: medium
    risk: high
    rejection_rationale:
      Service Worker scope isolation is not a security boundary — XSS in the main thread can message the
      Worker. Non-standard pattern with no industry consensus or IETF guidance. No major financial institution has adopted this
      in production.
decision:
  chosen_alternative: Backend-for-Frontend (BFF) Token Mediator
  rationale: |
    - Banking portal is a high-value target — tokens must not be accessible to JavaScript under any XSS scenario
    - HTTP-only cookies are not accessible to document.cookie or JavaScript APIs — defense-in-depth against XSS
    - BFF as confidential client enables stronger authentication with PingFederate (client_secret_jwt)
    - IETF OAuth Browser-Based Applications BCP explicitly recommends the BFF pattern for sensitive applications
    - Server-side DPoP proof generation with a stable keypair is more robust than browser-based key management
    - Cyber insurance underwriter requires server-side token storage for the banking portal
    - SameSite=Strict cookies eliminate CSRF without additional tokens or headers
  tradeoffs: |
    - Additional BFF component to operate (~2-3ms proxy latency per API request)
    - SPA cannot make direct API calls to third-party services — must proxy through BFF
    - Cookie domain must match SPA origin — limits multi-domain deployment flexibility
    - Frontend team must adapt to cookie-based session model instead of bearer token model
  decision_date: "2026-02-18"
  confidence: high
consequences:
  positive:
    - Access and refresh tokens never touch the browser — zero XSS token extraction risk
    - BFF confidential client authentication strengthens the OAuth client identity
    - Token renewal is invisible to the SPA — no iframe hacks or refresh token rotation logic in JS
    - Cyber insurance premium reduced by $30K/year with server-side token storage attestation
  negative:
    - "BFF is an additional component: deployment, monitoring, on-call rotation"
    - ~2-3ms added proxy latency per API request
    - "Frontend developers must use cookie-aware fetch (credentials: 'include') instead of Authorization headers"
confirmation:
  description: "Integration test: verify SPA receives tokens only via BFF, no tokens in browser storage. Security scan of BFF endpoints."

dependencies:
  internal:
    - PingFederate 12.x (authorization server)
    - CDN (SPA static asset hosting)
    - API Gateway (PingAccess) behind BFF
    - HSM (cookie encryption key)
  external:
    - None — BFF is an internal component
references:
  - title: OAuth 2.0 for Browser-Based Applications — IETF BCP
    url: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-browser-based-apps
  - title: Token Handler Pattern — Curity
    url: https://curity.io/resources/learn/the-token-handler-pattern/
  - title: OAuth 2.1 Authorization Framework — RFC 9700
    url: https://datatracker.ietf.org/doc/html/rfc9700
lifecycle:
  review_cycle_months: 12
  next_review_date: "2027-02-18"
  superseded_by: null
  supersedes: null
  archival:
    archived_at: null
    archive_reason: null
audit_trail:
  - event: created
    by: Priya Sharma
    at: "2026-02-01T10:00:00Z"
  - event: updated
    by: Kai Lindström
    at: "2026-02-12T15:00:00Z"
    details: Added Service Worker alternative analysis and cyber insurance underwriter requirements
  - event: approved
    by: Marcus Chen
    at: "2026-02-18T10:00:00Z"
  - event: approved
    by: Jonas Eriksen
    at: "2026-02-20T09:00:00Z"
    details: "CISO approval with condition: CSP must be deployed as defense-in-depth alongside BFF"
````

## File: examples-reference/ADR-0006-session-enrichment-for-step-up-authentication.yaml
````yaml
adr:
  id: ADR-0006
  title: Use IdP session enrichment over custom JWE cookies for persisting step-up authentication proof
  summary:
    Persist step-up authentication proof via PingFederate session enrichment and acr claims rather than custom JWE
    cookies, keeping all auth state in the IdP.
  status: accepted
  created_at: "2026-02-10T08:00:00Z"
  last_modified: "2026-02-28T14:00:00Z"
  version: "1.0"
  schema_version: 1.0.0
  project: Transaction Security — Step-Up Authentication
  component: Step-Up Proof Persistence Mechanism
  tags:
    - step-up
    - session-enrichment
    - jwe
    - rfc9470
    - transaction-signing
    - mfa
  priority: high
  decision_type: technology
authors:
  - name: Elena Vasquez
    role: IAM Architect
    email: elena.vasquez@novatrust.example.com
  - name: Marcus Chen
    role: Head of IAM
    email: marcus.chen@novatrust.example.com
decision_owner:
  name: Jonas Eriksen
  role: CISO
  email: jonas.eriksen@novatrust.example.com
reviewers:
  - name: Priya Sharma
    role: API Platform Lead
    email: priya.sharma@novatrust.example.com
  - name: Tomasz Kowalski
    role: Network Security Architect
    email: tomasz.kowalski@novatrust.example.com
  - name: DPO
    role: Data Protection Officer
    email: dpo@novatrust.example.com
approvals:
  - name: Jonas Eriksen
    role: CISO
    identity: "@jonaseriksen"
    approved_at: "2026-02-27T10:00:00Z"
    signature_id: sig-stepup-001
  - name: Marcus Chen
    role: Head of IAM
    identity: "@marcuschen"
    approved_at: "2026-02-28T09:00:00Z"
    signature_id: sig-stepup-002
context:
  summary: |
    NovaTrust's banking APIs require step-up authentication for high-value operations: wire transfers > €10K, beneficiary management, and PSD2 dynamic linking for payment initiation. When a user triggers a high-value operation, the API gateway (PingAccess) challenges the user for additional authentication (biometric, FIDO2, or OTP) via RFC 9470 `insufficient_user_authentication`. After successful step-up, the system must persist proof that the user has completed the higher authentication level so that subsequent high-value requests within a time window do not re-challenge. Two patterns exist: (A) enrich the IdP session (PingFederate) with the authentication level and let the access token's `acr` claim reflect it, or (B) issue a custom JWE-encrypted cookie directly from the API gateway containing the step-up proof. This decision determines how step-up proof is created, stored, validated, and eventually expired.
  business_drivers:
    - "PSD2 Dynamic Linking: payment initiation requires proof of SCA with transaction binding"
    - "Customer friction: re-challenging for every high-value operation within a session degrades UX"
    - Fraud team needs centralized visibility into step-up authentication events
    - Audit trail must prove authentication level at exact time of each high-value operation
  technical_drivers:
    - PingAccess can trigger step-up via RFC 9470 `insufficient_user_authentication` error response
    - PingFederate session supports authentication level tracking (ACR values) natively
    - JWE cookie approach requires custom crypto key management outside the IdP
    - Access token `acr` claim provides standards-based proof of authentication context class
    - Session enrichment integrates with PingFederate's built-in session timeout and ACR policies
  constraints:
    - "Step-up proof must expire independently of the base session (max_age for high assurance: 15 minutes)"
    - API gateway (PingAccess) is the enforcement point — must validate step-up proof before proxying
    - Must work with the BFF pattern (ADR-0005) — SPA does not manage tokens directly
    - PingFederate session store must handle the additional metadata without capacity issues
  assumptions:
    - PingFederate's session enrichment can store custom attributes (acr_at timestamp) per session
    - Token refresh via BFF will acquire a new access token with updated `acr` claim
    - PingAccess can evaluate `acr` claim in the access token for step-up enforcement
    - 15-minute max_age for high assurance is acceptable to the fraud team
requirements:
  functional:
    - id: F-001
      description: After successful step-up, access tokens must contain an acr claim reflecting the higher authentication level
    - id: F-002
      description: Step-up proof must expire after a configurable max_age (default 15 minutes) independent of the base session
    - id: F-003
      description: API gateway must reject high-value operations when acr claim does not meet the required level
    - id: F-004
      description: Step-up events must be logged in PingFederate audit trail with correlation to the triggering transaction
  non_functional:
    - id: NF-001
      description: Step-up challenge-to-proof latency < 2 seconds (including MFA verification)
    - id: NF-002
      description: Token refresh with enriched session must complete in < 500ms
    - id: NF-003
      description: No additional cookies or local storage beyond the existing BFF session cookie
alternatives:
  - name: IdP session enrichment (Approach A)
    summary: |
      After successful step-up MFA, PingFederate enriches the user's IdP session with the achieved authentication context class (e.g., `urn:novatrust:acr:high`) and the timestamp of the step-up event. On the next token refresh, the BFF obtains a new access token whose `acr` claim reflects the elevated level. PingAccess validates the `acr` claim and `auth_time` to enforce max_age. When max_age expires, the next high-value request triggers a new step-up challenge.
    pros:
      - "Standards-based: acr claim in access token is defined by OIDC Core §2"
      - "Centralized at the IdP: all step-up state managed by PingFederate — single source of truth"
      - "No custom crypto: no need to generate, encrypt, or manage JWE keys outside the IdP"
      - "Audit trail: PingFederate logs step-up events with session correlation — fraud team has visibility"
      - "max_age enforcement: PingFederate natively supports `max_age` parameter on authorize requests"
      - Token refresh via BFF acquires updated acr — no custom token issuance logic
      - Integrates with existing PingAccess token validation — acr claim check is a configuration change
    cons:
      - Requires a token refresh after step-up to get updated acr claim — brief delay (~300ms)
      - Step-up state is tied to the IdP session — if session is lost, step-up proof is lost
      - PingFederate session store must accommodate additional attributes per session
      - "Multi-region: session enrichment must replicate across PingFederate cluster nodes"
    estimated_cost: low
    risk: low
  - name: Custom JWE cookie (Approach B)
    summary: |
      After successful step-up MFA, the API gateway (PingAccess) issues a JWE-encrypted cookie containing the step-up proof: authentication level, timestamp, and transaction reference. PingAccess validates the JWE cookie on subsequent requests to high-value endpoints. The cookie has a short Max-Age (15 minutes) for expiry.
    pros:
      - No IdP session dependency — step-up proof is self-contained in the cookie
      - No token refresh delay — cookie is issued immediately after step-up
      - Works even if PingFederate session is lost or rotated
      - Gateway controls the full lifecycle — no IdP configuration changes needed
    cons:
      - "Custom crypto required: JWE key generation, rotation, and sharing across PingAccess nodes"
      - Cookie is an additional credential — increases the attack surface
      - JWE key management is outside PingFederate — not governed by IdP key lifecycle policies
      - "No centralized audit: step-up events logged at the gateway, not the IdP — fragmented audit trail"
      - "Non-standard: no IETF or OIDC specification for gateway-issued step-up cookies"
      - "CSRF protection: additional cookie requires careful SameSite configuration"
      - Cookie encryption key compromise allows forging step-up proofs — critical risk
      - Must implement custom max_age logic — PingAccess does not natively track cookie-based auth levels
    estimated_cost: high
    risk: medium
    rejection_rationale:
      Requires custom JWE key management outside the IdP — key compromise allows forging step-up proofs.
      Non-standard approach with no IETF or OIDC specification. Fragmented audit trail (gateway vs IdP) hinders fraud investigation.
  - name: "Hybrid: enriched session with JWE fallback for session loss"
    summary: |
      Primary path uses IdP session enrichment (Approach A). Additionally, the BFF issues a JWE-encrypted cookie as a fallback in case the PingFederate session is lost. PingAccess checks acr claim first, then falls back to JWE cookie.
    pros:
      - Resilient to PingFederate session loss
      - Standards-based primary path with fallback safety net
    cons:
      - All cons of both approaches combined
      - "Two validation paths at PingAccess: acr claim check + JWE cookie check"
      - JWE cookie fallback may mask session management issues instead of surfacing them
      - "Double the key management overhead: IdP signing keys + JWE encryption keys"
      - Testing matrix is doubled — must validate both paths independently
      - "Operational complexity: which path was used? Debugging requires checking both"
    estimated_cost: high
    risk: medium
    rejection_rationale:
      Combines the complexity of both approaches without clear benefit. Two validation paths double the testing
      matrix. JWE cookie fallback may mask session management issues rather than surfacing them for resolution.
decision:
  chosen_alternative: IdP session enrichment (Approach A)
  rationale: |
    - Standards-based: acr claim and max_age are OIDC Core primitives — no custom protocol needed
    - Single source of truth: PingFederate manages all authentication state — no parallel state outside IdP
    - No custom crypto: eliminates JWE key management, rotation, and the risk of key compromise
    - Centralized audit: PingFederate logs all step-up events with session IDs — fraud team query a single system
    - PingAccess policy configuration: 'require acr=urn:novatrust:acr:high with max_age=900 for /api/payments/** ' — declarative, not custom code
    - Token refresh delay (~300ms) is acceptable — BFF handles refresh transparently before proxying the request
    - Session replication across PingFederate cluster is already operational for base session — marginal additional load
  tradeoffs: |
    - Token refresh round-trip adds ~300ms after step-up — user sees brief delay before high-value operation proceeds
    - PingFederate session loss requires re-authentication including step-up — accepted as correct security behavior
    - Session store grows by ~100 bytes per enriched session — negligible at current scale (100K active sessions)
    - Multi-data-center: session replication lag (< 500ms) may cause brief inconsistency after step-up in cross-DC scenario
  decision_date: "2026-02-27"
  confidence: high
consequences:
  positive:
    - No custom cryptographic material to manage — step-up proof lifecycle governed by IdP
    - "PSD2 dynamic linking: acr claim provides auditable proof of SCA at transaction time"
    - Fraud team has single query point (PingFederate audit logs) for all step-up events
    - "PingAccess enforcement is declarative: ACR + max_age policy per URL pattern"
  negative:
    - ~300ms token refresh delay after step-up MFA
    - Session loss requires full re-authentication including step-up
    - PingFederate session store carries additional enrichment attributes
confirmation:
  description:
    Session enrichment validated in staging with PingFederate 12.x and PingAccess 8.x. Step-up flow tested end-to-end
    via BFF with FIDO2 and OTP. acr claim propagation confirmed across cluster nodes within 500ms.
  artifact_ids:
    - TEST-SUITE-step-up-e2e-fido2-otp
    - https://github.com/novatrust/iam-platform/pull/267
    - POC-2026-02-session-enrichment-replication
dependencies:
  internal:
    - PingFederate 12.x (session enrichment, acr claim issuance)
    - PingAccess 8.x (ACR policy enforcement)
    - BFF (ADR-0005) for step-up challenge mediation
    - MFA provider (FIDO2 / biometric / OTP)
  external:
    - None — all components are internal
references:
  - title: OAuth 2.0 Step-Up Authentication Challenge Protocol — RFC 9470
    url: https://datatracker.ietf.org/doc/html/rfc9470
  - title: OpenID Connect Core 1.0 — §2 acr Claim
    url: https://openid.net/specs/openid-connect-core-1_0.html#IDToken
  - title: PSD2 RTS on Strong Customer Authentication — EBA
    url: https://www.eba.europa.eu/regulation-and-policy/payment-services-and-electronic-money/regulatory-technical-standards-on-strong-customer-authentication-and-common-and-secure-communication
  - title: PingFederate Session Management Documentation
    url: https://docs.pingidentity.com/pingfederate/latest/session-management.html
lifecycle:
  review_cycle_months: 12
  next_review_date: "2027-02-27"
  superseded_by: null
  supersedes: null
  archival:
    archived_at: null
    archive_reason: null
audit_trail:
  - event: created
    by: Elena Vasquez
    at: "2026-02-10T08:00:00Z"
  - event: updated
    by: Marcus Chen
    at: "2026-02-20T11:00:00Z"
    details: Added hybrid approach analysis and PSD2 dynamic linking requirements
  - event: approved
    by: Jonas Eriksen
    at: "2026-02-27T10:00:00Z"
    details: "CISO approval with condition: max_age must be 15 minutes maximum for payment endpoints"
  - event: approved
    by: Marcus Chen
    at: "2026-02-28T09:00:00Z"
````

## File: .skills/adr-author/references/GLOSSARY.md
````markdown
# ADR Glossary — Quick Reference

> **Subset** of the full glossary at `docs/glossary.md`.
> This file covers enum values and ID formats only. Refer to the full glossary for definitions, guidance, and abbreviations.

## Status Values
`draft` | `proposed` | `accepted` | `superseded` | `deprecated` | `rejected` | `deferred`

## Decision Types
`technology` | `process` | `organizational` | `vendor` | `security` | `compliance`

## Priority Levels
`low` | `medium` | `high` | `critical`

## Confidence Levels
`low` | `medium` | `high`

## Risk / Impact Scales
- **Likelihood**: `low` | `medium` | `high`
- **Impact**: `low` | `medium` | `high` | `critical`

## ID Formats
- ADR: `ADR-NNNN` or `ADR-NNNN-slug` (e.g., `ADR-0001`, `ADR-0001-dpop-over-mtls`)
- Functional Requirement: `F-NNN` (e.g., `F-001`) — scoped per ADR
- Non-Functional Requirement: `NF-NNN` (e.g., `NF-001`) — scoped per ADR
- Risk: `R-NNN` (e.g., `R-001`) — scoped per ADR

## Lifecycle Supersession
Tracked via `lifecycle.supersedes` and `lifecycle.superseded_by` (ADR ID strings).

## Audit Trail Events
`created` | `updated` | `reviewed` | `approved` | `rejected` | `deferred` | `superseded` | `deprecated` | `archived`
````

## File: architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml
````yaml
adr:
  id: ADR-0000
  title: Adopt schema-governed ADR process for architectural decision management
  summary:
    Establish a formal, schema-validated ADR governance process using YAML files, JSON Schema validation, and GitOps
    workflows for managing architectural decisions.
  status: accepted
  created_at: "2026-03-05T09:00:00Z"
  last_modified: "2026-03-05T18:00:00Z"
  version: "1.0"
  schema_version: 1.0.0
  project: ADR Governance
  component: Decision Management Process
  tags:
    - governance
    - adr
    - process
    - meta
  priority: critical
  decision_type: process
authors:
  - name: Ivan Stambuk
    role: Principal Architect
    email: ivan.stambuk@novatrust.example.com
decision_owner:
  name: Ivan Stambuk
  role: Principal Architect
  email: ivan.stambuk@novatrust.example.com
approvals:
  - name: Ivan Stambuk
    role: Principal Architect
    identity: "@ivanstambuk"
    approved_at: "2026-03-05T18:00:00Z"
    signature_id: null
context:
  summary:
    NovaTrust's architecture team makes dozens of significant decisions per year — technology choices, security protocols,
    vendor selections, and process changes. These decisions are currently captured in meeting notes, Confluence pages, and
    Slack threads, leading to lost context, repeated discussions, and inconsistent application. We need a structured, version-controlled,
    machine-readable format for recording architectural decisions with full audit trails.
  business_drivers:
    - Regulatory auditors require proof of architectural decision rationale and approval chain
    - New team members spend weeks re-discovering decisions that were never formally documented
    - Repeated discussions on already-decided topics waste engineering time
  technical_drivers:
    - Machine-readable format enables automated validation, CI enforcement, and AI-assisted authoring
    - Git-based workflow provides immutable audit trail for free
    - Schema validation catches incomplete or inconsistent ADRs before they're merged
    - Structured YAML enables cross-referencing and lifecycle management
  constraints:
    - Must work with GitHub as the primary code hosting platform
    - Must be adoptable by teams without specialized tooling (YAML is human-readable)
    - Must support formal approval workflows for regulated financial services
  assumptions:
    - Teams are comfortable with Git-based workflows and pull requests
    - JSON Schema validation tooling is available in CI (Python, GitHub Actions)
    - ADR volume will remain under 100 active decisions per year
alternatives:
  - name: Schema-governed YAML ADRs with JSON Schema validation
    summary:
      Custom YAML-based ADR meta-model with JSON Schema (Draft 2020-12) validation. Each ADR is a self-contained YAML
      file validated against a comprehensive schema. GitOps workflow drives all state transitions.
    pros:
      - Machine-readable and human-readable — YAML is approachable for all team members
      - JSON Schema provides automated validation in CI — catches errors before merge
      - Self-contained — each ADR has all context needed to understand the decision
      - Formal approval workflow with signature IDs — satisfies regulatory audit requirements
      - Append-only audit trail — immutable record of all lifecycle events
      - Lifecycle management — periodic review, supersession chain, archival
      - Agent Skill integration — AI-assisted authoring with schema awareness
    cons:
      - More structured than lightweight markdown ADRs — higher authoring overhead
      - Schema evolution requires backward-compatible versioning
      - YAML syntax errors can be confusing for non-technical stakeholders
    estimated_cost: low
    risk: low
  - name: Markdown ADRs with MADR 4.0 template
    summary: Use the widely adopted MADR 4.0 markdown template. ADRs are markdown files with optional YAML frontmatter.
    pros:
      - Most widely adopted ADR format — largest community
      - Simple to author — just markdown
      - YAML frontmatter provides lightweight metadata
    cons:
      - No schema validation — inconsistency across ADRs is common
      - No formal approval workflow — decision-makers are informational only
      - No audit trail — lifecycle events are not tracked
      - No lifecycle management — no review cadence, no archival
      - Free-text format makes machine parsing unreliable
    estimated_cost: low
    risk: medium
    rejection_rationale:
      Lacks formal approval workflow, audit trail, and schema validation required for regulated financial
      services. Free-text markdown makes automated quality checks unreliable.
  - name: Confluence-based decision pages
    summary: Record decisions in Confluence pages with a standardized template. Approvals managed via Confluence page approvals.
    pros:
      - Familiar tool — already used by most teams
      - Rich formatting and embedded diagrams
      - Confluence page approval workflow exists
    cons:
      - Not version-controlled — no Git history, no immutable audit trail
      - No schema validation — template adherence is voluntary
      - Difficult to cross-reference decisions systematically
      - Vendor lock-in to Atlassian
      - No CI integration — cannot enforce quality gates
    estimated_cost: low
    risk: high
    rejection_rationale:
      Not version-controlled — no immutable audit trail for regulatory compliance. No schema validation.
      Vendor lock-in to Atlassian. Cannot integrate with CI for automated enforcement.
decision:
  chosen_alternative: Schema-governed YAML ADRs with JSON Schema validation
  rationale: |
    - Machine-readable YAML with JSON Schema validation catches errors automatically — essential at scale
    - Formal approval workflow with signature IDs satisfies SOC 2 and regulatory audit requirements
    - Append-only audit trail in each ADR provides immutable decision history
    - Lifecycle management prevents decision rot via periodic review triggers
    - GitOps workflow means all state transitions are Git commits — free immutable audit trail
    - Agent Skill enables AI-assisted ADR authoring with schema awareness
  tradeoffs: |
    - Higher authoring overhead than simple markdown — accepted because consistency and validation matter more at enterprise scale
    - Schema evolution requires careful backward-compatible versioning — managed via versioning policy
    - YAML syntax learning curve for non-technical stakeholders — mitigated by template and examples
  decision_date: "2026-03-05"
  confidence: high
consequences:
  positive:
    - All architectural decisions documented with full context and rationale
    - Automated validation ensures consistency across all ADRs
    - Formal approval chain satisfies regulatory audit requirements
    - Periodic review prevents decision rot
    - AI-assisted authoring reduces friction
  negative:
    - Higher authoring overhead than lightweight markdown ADRs
    - Teams must learn YAML and the ADR schema (mitigated by template and examples)
    - Schema evolution requires careful management
confirmation:
  description:
    ADR governance process validated by authoring 7 example ADRs (ADR-0001 through ADR-0007) covering technology,
    security, and process decisions across accepted and rejected statuses.
  artifact_ids:
    - examples-reference/ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.yaml
    - examples-reference/ADR-0007-centralized-secret-store-for-api-keys.yaml
    - TEST-SUITE-validate-adr-all-examples
dependencies:
  internal:
    - GitHub Actions CI pipeline for schema validation
    - Python 3.x with jsonschema and pyyaml libraries
  external:
    - JSON Schema specification (Draft 2020-12)
lifecycle:
  review_cycle_months: 24
  next_review_date: "2028-03-05"
  superseded_by: null
  supersedes: null
  archival:
    archived_at: null
    archive_reason: null
audit_trail:
  - event: created
    by: Ivan Stambuk
    at: "2026-03-05T09:00:00Z"
    details: Initial ADR governance process design based on research of 14 ADR templates and 6 governance processes
  - event: approved
    by: Ivan Stambuk
    at: "2026-03-05T18:00:00Z"
    details: Process adopted after authoring 7 example ADRs and validating schema, CI, and Agent Skill integration
````

## File: CODEOWNERS.example
````
# CODEOWNERS — ADR Governance
#
# Copy this file to `.github/CODEOWNERS` and customize the team handles
# to match your GitHub organization.
#
# See: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners

# All ADRs require architect approval
architecture-decision-log/                             @org/architecture-team

# Security decisions additionally require CISO
architecture-decision-log/ADR-*security*               @org/security-team

# Compliance decisions additionally require DPO
architecture-decision-log/ADR-*compliance*             @org/compliance-team

# Schema changes require architect approval
schemas/                         @org/architecture-team

# Process documentation changes require architect approval
docs/                            @org/architecture-team

# Validation script changes require architect approval
scripts/                         @org/architecture-team

# Governance config changes require architect approval
.adr-governance/                 @org/architecture-team

# NOTE: GitHub CODEOWNERS uses fnmatch-style patterns. The patterns above for
# security and compliance decisions match on *filename*, not YAML content.
# For reliable decision-type routing, include the domain in the ADR filename
# (e.g. ADR-0007-security-adopt-passkeys.yaml).
# For more sophisticated routing, implement a CI-based reviewer assignment step
# that reads `decision_type` from the YAML and requests the appropriate GitHub
# team via the GitHub API.

# RELATIONSHIP TO ADR APPROVAL IDENTITY ENFORCEMENT:
# CODEOWNERS determines who is *requested* to review an ADR PR.
# The `approvals[].identity` field in the ADR determines who *must* approve.
# CI (verify-approvals.py) validates that the identity-listed approvers
# have actually approved the PR — this is enforced even if CODEOWNERS does
# not match the same people. Both mechanisms complement each other:
#   - CODEOWNERS: "These people should be notified and asked to review"
#   - approvals[].identity: "These specific people must have approved"
````

## File: llms.txt
````
# adr-governance

> A schema-governed, AI-native Architecture Decision Record (ADR) framework. Provides a JSON Schema (Draft 2020-12) meta-model for structured YAML-based ADRs, a GitOps governance process, Python validation tooling, pre-built CI/CD pipelines for GitHub Actions, Azure DevOps, GCP Cloud Build, AWS CodeBuild, and GitLab CI, and an agentskills.io Agent Skill for AI-assisted authoring and review. The Architecture Decision Log (ADL) lives in `architecture-decision-log/`. Example ADRs cover IAM/security scenarios from a fictional enterprise.

## Documentation

- [README](https://github.com/ivanstambuk/adr-governance/blob/main/README.md): Project overview, problem statement, quick start, and directory structure
- [ADR Governance Process](https://github.com/ivanstambuk/adr-governance/blob/main/docs/adr-process.md): Normative process — roles, status lifecycle (Mermaid state diagram), workflows for proposing, reviewing, approving, rejecting, deferring, superseding, deprecating, archiving, and confirming ADRs. Includes the Architectural Significance Test, branch protection rules, CODEOWNERS setup, periodic review guidance, and schema versioning policy
- [CI/CD Setup Guide](https://github.com/ivanstambuk/adr-governance/blob/main/docs/ci-setup.md): Step-by-step setup for GitHub Actions, Azure DevOps, GCP Cloud Build, AWS CodeBuild, and GitLab CI — includes LLM-ready setup prompts
- [Glossary](https://github.com/ivanstambuk/adr-governance/blob/main/docs/glossary.md): All enum values (status, decision_type, priority, confidence, risk levels), ID formats, audit trail events, and abbreviations (AD, ADL, ADR, AKM, ASR)
- [JSON Schema](https://github.com/ivanstambuk/adr-governance/blob/main/schemas/adr.schema.json): The complete ADR meta-model — Draft 2020-12, defines all required/optional sections, field types, enums, and constraints
- [Agent Skill (SKILL.md)](https://github.com/ivanstambuk/adr-governance/blob/main/.skills/adr-author/SKILL.md): Instructions for AI assistants — how to author, review, validate, and supersede ADRs using the governed meta-model
- [Web Chat Quickstart](https://github.com/ivanstambuk/adr-governance/blob/main/docs/web-chat-quickstart.md): Platform-specific starter prompts for using the Repomix bundle with ChatGPT, Claude.ai, Google Gemini, and Microsoft Copilot — no skill execution required
- [ADR Template](https://github.com/ivanstambuk/adr-governance/blob/main/.skills/adr-author/assets/adr-template.yaml): Blank YAML template with all sections
- [Schema Reference](https://github.com/ivanstambuk/adr-governance/blob/main/.skills/adr-author/references/SCHEMA_REFERENCE.md): Human-readable schema documentation for the Agent Skill

## Decision Enforcement

The ADL (Architecture Decision Log) isn't just documentation — it's a machine-readable specification. The Repomix bundle (`adr-governance-bundle.md`) concatenates the entire ADL into a single searchable file that serves as a **single source of truth for Spec-Driven Development (SDD)**:

- **Agent context injection:** Point any coding agent (Copilot, Claude Code, Antigravity, Cursor) at the bundle file. The agent can search it using standard text search to find relevant architectural decisions and generate code that complies with them — across any repository.
- **CI pipeline guardrails:** Add a step in your code repository's CI pipeline that fetches the ADL bundle and validates code changes for architectural compliance before merge. The bundle is plain text — any tool from `grep` to an LLM can consume it.
- **Cross-repository enforcement:** The ADL repository and the code repository don't need to be the same. Fetch the bundle at CI time or include it in your agent's knowledge base.

## Examples

- [ADR-0000: Adopt Governed ADR Process (meta-ADR)](https://github.com/ivanstambuk/adr-governance/blob/main/architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml): Bootstrap decision adopting this governance framework
- [ADR-0001: DPoP over mTLS](https://github.com/ivanstambuk/adr-governance/blob/main/examples-reference/ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.yaml): Accepted — sender-constrained token strategy
- [ADR-0002: Reference Tokens over JWTs](https://github.com/ivanstambuk/adr-governance/blob/main/examples-reference/ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.yaml): Accepted — gateway introspection pattern
- [ADR-0003: Pairwise Subject Identifiers](https://github.com/ivanstambuk/adr-governance/blob/main/examples-reference/ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.yaml): Accepted — OIDC privacy pattern
- [ADR-0004: Ed25519 over RSA](https://github.com/ivanstambuk/adr-governance/blob/main/examples-reference/ADR-0004-ed25519-over-rsa-for-jwt-signing.yaml): Accepted — JWT signing key algorithm
- [ADR-0005: BFF Token Mediator](https://github.com/ivanstambuk/adr-governance/blob/main/examples-reference/ADR-0005-bff-token-mediator-for-spa-token-acquisition.yaml): Accepted — SPA token acquisition
- [ADR-0006: Session Enrichment for Step-Up](https://github.com/ivanstambuk/adr-governance/blob/main/examples-reference/ADR-0006-session-enrichment-for-step-up-authentication.yaml): Accepted — step-up authentication proof
- [ADR-0007: Centralized Vault (rejected)](https://github.com/ivanstambuk/adr-governance/blob/main/examples-reference/ADR-0007-centralized-secret-store-for-api-keys.yaml): Rejected — documents why HashiCorp Vault was not adopted
- [ADR-0008: OpenID Federation (deferred)](https://github.com/ivanstambuk/adr-governance/blob/main/examples-reference/ADR-0008-defer-openid-federation-for-trust-establishment.yaml): Deferred — postponed until ecosystem matures

## Tooling

- [Validator Script](https://github.com/ivanstambuk/adr-governance/blob/main/scripts/validate-adr.py): Python script — validates ADR YAML against JSON Schema, checks semantic consistency (chosen_alternative ↔ alternatives, status ↔ audit_trail, supersession symmetry, temporal ordering), and quality signals (missing summaries, premature confidence, decision date consistency)
- [Decision Extractor](https://github.com/ivanstambuk/adr-governance/blob/main/scripts/extract-decisions.py): Extracts active decisions into Markdown or JSON for agent context injection and CI enforcement. Includes `--compliance-prompt` mode that generates LLM-ready compliance review prompts with code diffs. Supports filtering by status, tags, and decision type.
- [Pre-Review Quality Gate](https://github.com/ivanstambuk/adr-governance/blob/main/scripts/review-adr.py): Generates an LLM Socratic review prompt for ADR drafts — probes for semantic clarity, completeness, logical consistency, assumption risks, and cross-reference consistency before the ADR reaches human reviewers.
- [Markdown Renderer](https://github.com/ivanstambuk/adr-governance/blob/main/scripts/render-adr.py): Renders ADR YAML to polished Markdown with Mermaid diagram passthrough
- [Repomix Bundle Script](https://github.com/ivanstambuk/adr-governance/blob/main/scripts/bundle.sh): Creates single-file bundle for LLM context injection

## CI/CD Pipelines

Pre-built pipeline files for enforcing ADR validation as a merge gate. Copy the file for your platform to the repo root and configure branch protection.

- [CI/CD Setup Guide](https://github.com/ivanstambuk/adr-governance/blob/main/docs/ci-setup.md): Step-by-step setup for all platforms, enforcement configuration, troubleshooting, and LLM-ready setup prompts
- [GitHub Actions](https://github.com/ivanstambuk/adr-governance/blob/main/.github/workflows/validate-adr.yml): Pre-configured — runs on every PR automatically
- [Azure DevOps](https://github.com/ivanstambuk/adr-governance/blob/main/ci/azure-devops/azure-pipelines.yml): Copy to repo root as `azure-pipelines.yml`
- [GCP Cloud Build](https://github.com/ivanstambuk/adr-governance/blob/main/ci/gcp-cloud-build/cloudbuild.yaml): Copy to repo root as `cloudbuild.yaml`
- [AWS CodeBuild](https://github.com/ivanstambuk/adr-governance/blob/main/ci/aws-codebuild/buildspec.yml): Copy to repo root as `buildspec.yml`
- [GitLab CI](https://github.com/ivanstambuk/adr-governance/blob/main/ci/gitlab-ci/.gitlab-ci.yml): Copy to repo root as `.gitlab-ci.yml`
````

## File: .skills/adr-author/references/SCHEMA_REFERENCE.md
````markdown
# ADR Schema Reference

The ADR meta-model is defined as a JSON Schema (Draft 2020-12) at `schemas/adr.schema.json`.

## Required Top-Level Sections

| Section | Description |
|---------|-------------|
| `adr` | Core metadata: id, title, status, timestamps, project, decision_type |
| `authors` | At least one author with name and role |
| `decision_owner` | Single accountable person |
| `context` | Problem summary, drivers, constraints, assumptions |
| `alternatives` | Minimum 2 alternatives with pros, cons, cost, risk |
| `decision` | Chosen alternative, rationale, tradeoffs, date, confidence level |
| `consequences` | Positive and negative outcomes |
| `confirmation` | How the decision's implementation will be verified (`description` required, `artifact_ids` optional) |

## Optional Top-Level Sections

| Section | Description |
|---------|-------------|
| `reviewers` | People who reviewed the ADR |
| `approvals` | Formal approvals with timestamps, platform identities, and signature IDs |
| `requirements` | Embedded functional and non-functional requirements |
| `dependencies` | Internal and external dependencies |

| `references` | External links and evidence |
| `lifecycle` | Review cadence, supersession chain, archival |
| `audit_trail` | Immutable event log (events: created, updated, reviewed, approved, rejected, superseded, deprecated, archived) |

## Key Validation Rules

1. `adr.id` must match `^ADR-[0-9]{4}(-[a-z0-9]+)*$` (e.g. `ADR-0001` or `ADR-0001-dpop-over-mtls`)
2. `adr.status` must be one of the defined enum values
3. `alternatives` must have `minItems: 2`
4. `decision.chosen_alternative` should match a name in `alternatives`
5. Requirement IDs: `^(F|NF)-[0-9]{3}$`
6. `audit_trail` events use defined enum values
````

## File: scripts/validate-adr.py
````python
#!/usr/bin/env python3
"""
Validate ADR YAML files against the ADR JSON Schema.

Usage:
    python3 validate-adr.py <file_or_directory> [<file_or_directory> ...]

Requires: pip install jsonschema pyyaml
"""

import json
import re
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
    from jsonschema import validate, ValidationError, Draft202012Validator
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip install jsonschema pyyaml")
    sys.exit(2)

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "adr.schema.json"

# Regex to extract ADR-NNNN prefix from filenames
FILENAME_ID_RE = re.compile(r"^(ADR-\d{4})")


def load_schema():
    """Load the ADR JSON Schema."""
    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found at {SCHEMA_PATH}")
        sys.exit(2)
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)


def parse_iso_datetime(ts_str: str) -> datetime | None:
    """Parse an ISO 8601 datetime string to a timezone-aware datetime.

    Returns None if parsing fails.
    """
    if not ts_str:
        return None
    try:
        # Python 3.11+ handles most ISO 8601 strings directly
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def validate_file(filepath: Path, schema: dict) -> tuple[list[str], list[str]]:
    """Validate a single ADR YAML file.

    Returns:
        (errors, warnings) — errors are hard failures, warnings are advisory.
    """
    errors = []
    warnings = []
    try:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"], []

    if data is None:
        return ["File is empty"], []

    # --- JSON Schema validation ---
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.path) or "(root)"
        errors.append(f"  {path}: {error.message}")

    # --- Semantic checks ---
    if isinstance(data, dict):
        # Check chosen_alternative matches an alternative name
        alternatives = data.get("alternatives", [])
        decision = data.get("decision", {})
        chosen = decision.get("chosen_alternative", "")
        alt_names = [a.get("name", "") for a in alternatives if isinstance(a, dict)]
        if chosen and alt_names and chosen not in alt_names:
            errors.append(
                f"  decision.chosen_alternative: '{chosen}' does not match any alternative name: {alt_names}"
            )

        # Check status ↔ audit_trail consistency
        status = data.get("adr", {}).get("status", "")
        audit_trail = data.get("audit_trail", [])
        audit_events = [e.get("event", "") for e in audit_trail if isinstance(e, dict)]

        status_to_expected_event = {
            "accepted": "approved",
            "rejected": "rejected",
            "superseded": "superseded",
            "deprecated": "deprecated",
            "deferred": "deferred",
        }

        if status in status_to_expected_event and audit_trail:
            expected = status_to_expected_event[status]
            if expected not in audit_events:
                warnings.append(
                    f"  audit_trail: status is '{status}' but no '{expected}' event found in audit_trail"
                )

        # Check approvals ↔ audit_trail consistency
        approvals = data.get("approvals", [])
        if approvals and audit_trail:
            approvals_with_timestamp = [
                a for a in approvals
                if isinstance(a, dict) and a.get("approved_at") is not None
            ]
            approved_events = [e for e in audit_trail if isinstance(e, dict) and e.get("event") == "approved"]
            if approvals_with_timestamp and not approved_events:
                warnings.append(
                    f"  audit_trail: {len(approvals_with_timestamp)} approval(s) have timestamps but no 'approved' event in audit_trail"
                )



        # Check for invalid state transitions (status vs audit trail events)
        invalid_event_for_status = {
            "draft": {"approved", "superseded", "deprecated", "deferred"},
            "proposed": {"superseded", "deprecated"},
            "accepted": {"deferred"},
            "rejected": {"approved", "superseded", "deprecated", "deferred"},
            "deferred": {"approved", "superseded", "deprecated"},
        }
        if status in invalid_event_for_status and audit_trail:
            for bad_event in invalid_event_for_status[status]:
                if bad_event in audit_events:
                    warnings.append(
                        f"  audit_trail: status is '{status}' but audit_trail contains "
                        f"'{bad_event}' event — invalid state transition"
                    )


        # --- Warn if adr.summary is missing on proposed/accepted ADRs ---
        if status in {"proposed", "accepted"}:
            summary = data.get("adr", {}).get("summary", "")
            if not summary or not summary.strip():
                warnings.append(
                    f"  'adr.summary' is missing or empty — recommended for {status} ADRs "
                    f"(elevator pitch for stakeholder triage)"
                )

        # --- Warn if schema_version is missing ---
        schema_version = data.get("adr", {}).get("schema_version", "")
        if not schema_version:
            warnings.append(
                "  'adr.schema_version' is missing — recommended per schema versioning policy (§10)"
            )

        # --- Check audit_trail temporal ordering (proper datetime parsing) ---
        if audit_trail:
            prev_dt = None
            prev_ts_str = None
            for i, entry in enumerate(audit_trail):
                if isinstance(entry, dict):
                    ts_str = entry.get("at", "")
                    if ts_str:
                        current_dt = parse_iso_datetime(str(ts_str))
                        if current_dt and prev_dt and current_dt < prev_dt:
                            warnings.append(
                                f"  audit_trail[{i}]: event '{entry.get('event', '')}' at {ts_str} "
                                f"is earlier than previous event at {prev_ts_str} — events should be in chronological order"
                            )
                        if current_dt:
                            prev_dt = current_dt
                            prev_ts_str = ts_str

        # --- Warn if accepted ADR has no approval with timestamp ---
        if status == "accepted":
            approvals_with_ts = [
                a for a in approvals
                if isinstance(a, dict) and a.get("approved_at") is not None
            ]
            if not approvals_with_ts:
                warnings.append(
                    "  status is 'accepted' but no approval entry has an 'approved_at' timestamp"
                )

        # --- Warn if confidence is set on a draft ADR ---
        if status == "draft":
            conf = decision.get("confidence", "")
            if conf:
                warnings.append(
                    f"  decision.confidence is '{conf}' but status is 'draft' — "
                    f"confidence is premature before the decision is proposed"
                )

        # --- Check decision_date within created_at → last_modified range ---
        decision_date = decision.get("decision_date", "")
        created_at = data.get("adr", {}).get("created_at", "")
        if decision_date and created_at:
            # Compare date strings (ISO 8601 sorts lexicographically)
            created_date = str(created_at)[:10]  # extract date portion
            if str(decision_date) < created_date:
                warnings.append(
                    f"  decision.decision_date ({decision_date}) is before "
                    f"adr.created_at ({created_date}) — decision cannot predate the ADR"
                )


        # --- Check filename ↔ adr.id consistency ---
        adr_id = data.get("adr", {}).get("id", "")
        if adr_id:
            filename = filepath.stem  # e.g. "ADR-0001-dpop-over-mtls"
            match = FILENAME_ID_RE.match(filename)
            if match:
                filename_id = match.group(1)
                # Extract just the ADR-NNNN portion from the YAML id
                yaml_id_match = FILENAME_ID_RE.match(adr_id)
                yaml_id_prefix = yaml_id_match.group(1) if yaml_id_match else adr_id
                if filename_id != yaml_id_prefix:
                    errors.append(
                        f"  filename prefix '{filename_id}' does not match adr.id '{adr_id}'"
                    )

    return errors, warnings


def validate_cross_references(all_data: dict[str, dict]):
    """Check cross-file referential integrity.

    Checks:
    - Lifecycle supersession symmetry
    - Duplicate ADR IDs across all files

    Args:
        all_data: mapping of filepath → parsed YAML data
    """
    warnings = []
    errors = []
    # Collect all known ADR IDs and their lifecycle supersession fields
    known_ids = set()
    id_to_filepath = {}
    id_to_supersedes = {}       # adr_id -> supersedes value
    id_to_superseded_by = {}    # adr_id -> superseded_by value
    for filepath, data in all_data.items():
        if isinstance(data, dict):
            adr_id = data.get("adr", {}).get("id", "")
            if adr_id:
                # --- Check for duplicate ADR IDs ---
                if adr_id in known_ids:
                    errors.append(
                        f"  duplicate ADR ID '{adr_id}': found in both "
                        f"'{id_to_filepath[adr_id]}' and '{filepath}'"
                    )
                known_ids.add(adr_id)
                id_to_filepath[adr_id] = filepath
                lifecycle = data.get("lifecycle", {})
                sup = lifecycle.get("supersedes")
                sup_by = lifecycle.get("superseded_by")
                if sup:
                    id_to_supersedes[adr_id] = sup
                if sup_by:
                    id_to_superseded_by[adr_id] = sup_by

    # Check supersession symmetry: if A supersedes B, B should have superseded_by A
    for adr_id, target_id in id_to_supersedes.items():
        if target_id in known_ids:
            if target_id not in id_to_superseded_by or id_to_superseded_by[target_id] != adr_id:
                warnings.append(
                    f"  {id_to_filepath.get(adr_id, adr_id)}: '{adr_id}' declares "
                    f"lifecycle.supersedes '{target_id}', but '{target_id}' does not have "
                    f"lifecycle.superseded_by '{adr_id}'"
                )

    for adr_id, target_id in id_to_superseded_by.items():
        if target_id in known_ids:
            if target_id not in id_to_supersedes or id_to_supersedes[target_id] != adr_id:
                warnings.append(
                    f"  {id_to_filepath.get(adr_id, adr_id)}: '{adr_id}' declares "
                    f"lifecycle.superseded_by '{target_id}', but '{target_id}' does not have "
                    f"lifecycle.supersedes '{adr_id}'"
                )

    return errors, warnings


def main():
    # Parse args
    args = sys.argv[1:]

    if len(args) < 1:
        print(f"Usage: {sys.argv[0]} <file_or_directory> [<file_or_directory> ...]")
        sys.exit(2)

    schema = load_schema()

    # Collect files from all positional arguments
    files = []
    for arg in args:
        target = Path(arg)
        if target.is_file():
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(target.glob("*.yaml")))
            files.extend(sorted(target.glob("*.yml")))
        else:
            print(f"ERROR: {target} is not a file or directory")
            sys.exit(2)

    if not files:
        print(f"No YAML files found in: {', '.join(args)}")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0
    all_data = {}

    for filepath in files:
        errors, warnings = validate_file(filepath, schema)

        # Load data for cross-reference checks
        try:
            with open(filepath, "r") as f:
                all_data[str(filepath)] = yaml.safe_load(f)
        except yaml.YAMLError:
            pass

        if errors:
            print(f"FAIL: {filepath}")
            for err in errors:
                print(err)
            total_errors += len(errors)
        elif warnings:
            print(f"OK:   {filepath}")
        else:
            print(f"OK:   {filepath}")

        if warnings:
            for warn in warnings:
                print(f"  WARN: {warn.strip()}")
            total_warnings += len(warnings)

    # Cross-file reference checks (when more than 1 file loaded)
    if len(all_data) > 1:
        xref_errors, xref_warnings = validate_cross_references(all_data)
        if xref_errors:
            print("\nCross-reference errors:")
            for err in xref_errors:
                print(f"  ERROR: {err.strip()}")
            total_errors += len(xref_errors)
        if xref_warnings:
            print("\nCross-reference warnings:")
            for warn in xref_warnings:
                print(f"  WARN: {warn.strip()}")
            total_warnings += len(xref_warnings)

    print(f"\n{'='*60}")
    print(f"Files checked:  {len(files)}")
    print(f"Total errors:   {total_errors}")
    print(f"Total warnings: {total_warnings}")



    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
````

## File: .skills/adr-author/assets/adr-template.yaml
````yaml
# ADR Template
# Copy this file and fill in all sections.
# Required sections are marked. Optional sections can be removed if not applicable.

# --- REQUIRED ---
adr:
  id: "ADR-NNNN" # Replace with next sequential ID
  title: "" # 10-200 characters
  summary: "" # Optional: 2-4 sentence elevator pitch (max 500 chars)
  status: "draft" # draft | proposed | accepted | superseded | deprecated | rejected | deferred
  created_at: "" # ISO 8601 datetime
  last_modified: "" # ISO 8601 datetime
  version: "0.1"
  schema_version: "1.0.0"
  project: ""
  component: "" # Optional: specific component affected
  tags: [] # Categorization tags
  priority: "medium" # low | medium | high | critical
  decision_type: "technology" # technology | process | organizational | vendor | security | compliance

# --- REQUIRED ---
authors:
  - name: ""
    role: ""
    email: ""

# --- REQUIRED ---
decision_owner:
  name: ""
  role: ""
  email: ""

# --- Optional ---
reviewers:
  - name: ""
    role: ""
    email: ""

# --- Optional ---
approvals:
  - name: ""
    role: ""
    identity: "" # Platform handle for CI verification (e.g., GitHub @username, Azure DevOps email)
    approved_at: null # ISO 8601 datetime when approved, null if pending
    signature_id: null

# --- REQUIRED ---
context:
  summary: >
    Describe the problem, the current state, and why a decision is needed.
  business_drivers:
    - ""
  technical_drivers:
    - ""
  constraints:
    - ""
  assumptions:
    - ""

# --- Optional ---
requirements:
  functional:
    - id: "F-001"
      description: ""
  non_functional:
    - id: "NF-001"
      description: ""

# --- REQUIRED: minimum 2 alternatives ---
alternatives:
  - name: ""
    summary: ""
    pros:
      - ""
    cons:
      - ""
    estimated_cost: "medium" # low | medium | high
    risk: "medium" # low | medium | high | critical

  - name: ""
    summary: ""
    pros:
      - ""
    cons:
      - ""
    estimated_cost: "medium"
    risk: "medium"

# --- REQUIRED ---
decision:
  chosen_alternative: "" # Must match a name in alternatives
  rationale:
    | # Markdown — explain why this alternative was chosen. Supports mermaid diagrams.
    Why this was chosen...
  tradeoffs: | # Markdown — acknowledged tradeoffs accepted with this decision.
    What we're giving up...
  decision_date: "" # ISO 8601 date (YYYY-MM-DD)
  confidence: "medium" # low | medium | high — low-confidence decisions get shorter review cycles

# --- REQUIRED ---
consequences:
  positive:
    - ""
  negative:
    - ""

# --- REQUIRED (artifact_ids can be added later) ---
confirmation:
  description: "" # How the implementation of this decision will be verified
  artifact_ids:
    - "" # Jira tickets, PR URLs, test suite IDs, PoC results, benchmarks

# --- Optional ---
dependencies:
  internal: []
  external: []

# --- Optional ---
references:
  - title: ""
    url: ""

# --- Optional ---
lifecycle:
  review_cycle_months: 12
  next_review_date: "" # ISO 8601 date
  superseded_by: null
  supersedes: null
  archival:
    archived_at: null
    archive_reason: null

# --- Strongly recommended: append-only (schema: optional, but expected for all non-draft ADRs) ---
audit_trail:
  - event: "created"
    by: ""
    at: "" # ISO 8601 datetime
````

## File: .skills/adr-author/SKILL.md
````markdown
---
name: adr-author
description: >
  Author, review, validate, and summarize Architecture Decision Records (ADRs)
  using a governed YAML meta-model. Use when the user asks to create a new ADR,
  review an existing ADR, validate ADR YAML files against the schema, summarize
  decisions for stakeholders (email/chat), or needs guidance on the ADR governance
  process. Covers the full lifecycle: drafting, review, approval, supersession,
  and archival.
license: MIT
metadata:
  author: "ivanstambuk"
  version: "1.0"
---

# ADR Author Skill

## When to use this skill

Use this skill when the user:
- Wants to **create a new ADR** (architecture decision record)
- Wants to **review or audit an existing ADR** for completeness
- Needs to **validate** an ADR YAML file against the schema
- Wants to **summarize** an ADR for stakeholders (email, chat, digest)
- Asks about the **ADR governance process** or lifecycle
- Wants to **supersede, deprecate, or archive** an existing ADR
- Needs to understand the **ADR meta-model** fields and allowed values

## Core principles

1. **Self-contained**: Every ADR must embed all context (requirements, alternatives, risk, compliance) so it can be understood without external documents.
2. **Schema-governed**: All ADRs must validate against `schemas/adr.schema.json` (JSON Schema Draft 2020-12).
3. **At least two alternatives**: Every decision requires evaluation of ≥2 alternatives with pros, cons, cost, and risk.
4. **Immutable audit trail**: The `audit_trail` section is append-only. Never delete or modify existing entries.
5. **Self-contained with navigational links**: Supersession is tracked via `lifecycle.supersedes`/`superseded_by`. Each ADR remains fully self-contained — no structural dependencies on other ADRs.

## How to create a new ADR

### Step 1: Determine the next ADR ID

Check existing ADR files in the `architecture-decision-log/` directory (or `examples-reference/` for reference). The ID format is `ADR-NNNN` (zero-padded 4 digits). Use the next sequential number.

### Step 2: Gather context from the user

Ask the user for:
1. **Title**: What decision is being made? (10-200 characters)
2. **Decision type**: `technology` | `process` | `organizational` | `vendor` | `security` | `compliance`
3. **Priority**: `low` | `medium` | `high` | `critical`
4. **Context**: What problem are we solving? What are the business and technical drivers?
5. **Constraints**: What are the non-negotiable boundaries?
6. **Alternatives**: At least 2 options with pros, cons, estimated cost, and risk level
7. **Recommendation**: Which alternative and why?
8. **Summary** (`adr.summary`): 2-4 sentence elevator pitch for stakeholder triage (max 500 chars). This is distinct from `context.summary`, which is the full narrative problem statement.
9. **Confidence**: `low` | `medium` | `high` — how confident are we in this decision?

### Step 3: Generate the ADR YAML

Use the template at `assets/adr-template.yaml` as the starting point. Fill in all required sections:

- `adr` — metadata (id, title, status: `proposed`, timestamps, tags, priority, decision_type)
- `authors` — who is writing this
- `decision_owner` — who is accountable
- `context` — summary, business_drivers, technical_drivers, constraints, assumptions
- `requirements` — embedded functional and non-functional requirements
- `alternatives` — at least 2, each with name, summary, pros, cons, estimated_cost, risk, rejection_rationale (for non-chosen alternatives)
- `decision` — chosen_alternative, rationale, tradeoffs, decision_date, confidence
- `consequences` — positive, negative
- `confirmation` — description of how implementation will be verified (artifact_ids added later)
- `dependencies` — internal and external dependency tracking
- `audit_trail` — initial `created` event

### Step 4: Validate

Run the validation script to check the YAML against the JSON Schema:

```bash
python3 scripts/validate-adr.py architecture-decision-log/ADR-NNNN-short-title.yaml
```

### Step 5: File naming convention

```
architecture-decision-log/ADR-NNNN-short-kebab-case-title.yaml
```

Example: `architecture-decision-log/ADR-0007-adopt-passkeys-for-workforce-mfa.yaml`

## How to review an existing ADR

When reviewing, check for:

1. **Completeness**: All required sections present (see schema `required` fields)
2. **Alternative quality**: At least 2 alternatives with substantive pros/cons (not just "good" / "bad")
3. **Rationale strength**: Does the rationale clearly connect to the drivers and requirements?
4. **Risk coverage**: Are the major risks identified with realistic mitigations?
5. **Compliance**: Are regulatory implications addressed if the decision touches data, access, or infrastructure?
6. **Consistency**: Does the `chosen_alternative` name match an entry in `alternatives`? Are `lifecycle.supersedes`/`superseded_by` consistent?
7. **Audit trail**: Is the trail consistent with the status?
8. **Rejection rationale**: For each non-chosen alternative, is `rejection_rationale` populated explaining why it was not selected?
9. **Diagram quality**: Are embedded Mermaid diagrams used where a visual would clarify architecture or flow?

## How to supersede an ADR

1. Create a new ADR (ADR-MMMM) following the standard proposal workflow.
2. In the **new** ADR:
   - Set `lifecycle.supersedes: "ADR-NNNN"`
3. When the new ADR is accepted, **update the old ADR** in the same PR:
   - Set `adr.status: "superseded"`
   - Set `lifecycle.superseded_by: "ADR-MMMM"`
   - Add an audit trail entry: `event: "superseded"`

## Markdown-native fields

The following fields support **full Markdown** including embedded Mermaid diagrams via code fences:

- `context.summary` — narrative problem statement; embed architecture diagrams here
- `alternatives[].summary` — describe each option; embed comparison diagrams
- `decision.rationale` — explain *why*; use bullet lists, headers, or diagrams
- `decision.tradeoffs` — what was given up
- `confirmation.description` — verification evidence

Use YAML literal block scalars (`|`) for multiline content. Example:

```yaml
context:
  summary: |
    The system currently uses approach X.

    ```mermaid
    graph LR
        A --> B --> C
    ```

    We need to decide between X and Y.
```

## Reference documentation

- See [the glossary](../../docs/glossary.md) for all enum values and term definitions
- See [the JSON Schema](references/SCHEMA_REFERENCE.md) for the full meta-model specification
- See example ADRs in the repository's `examples-reference/` directory for well-formed samples

## Summarizing ADRs for stakeholders

Sometimes the full ADR is too detailed for stakeholders who just need to know *what was decided and why*. Use `scripts/summarize-adr.py` to produce concise summaries.

### Email format (default)

A ~10–15 line summary covering: the decision, why it was chosen, what alternatives were considered, key tradeoffs, consequences, and next steps. Suitable for post-meeting emails, status updates, or stakeholder briefings.

```bash
# Single ADR
python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml

# Multiple ADRs → produces a numbered digest
python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml \
    architecture-decision-log/ADR-0002.yaml

# All ADRs in a directory → full digest
python3 scripts/summarize-adr.py architecture-decision-log/

# Save to file for emailing
python3 scripts/summarize-adr.py -o meeting-recap.md architecture-decision-log/
```

### Chat format

A 3–5 line ultra-short summary for Slack, Teams, or any chat platform. Just the headline, the decision, one positive and one negative consequence, and a link to the full document.

```bash
python3 scripts/summarize-adr.py --format chat architecture-decision-log/ADR-0001.yaml
```

### When to use which format

| Scenario | Format |
|----------|--------|
| Post-meeting email to stakeholders | `email` (default) |
| Slack/Teams announcement | `chat` |
| Weekly architecture digest | `email` with multiple ADRs |
| Quick reply to "what did you decide?" | `chat` |
| Architecture newsletter | `email` with all accepted ADRs |

### AI-assisted summarization

When the user asks you to summarize an ADR, **prefer running the script** — it extracts the most salient fields deterministically. If the user wants a *custom* summary (e.g., focused on security implications, or tailored for a specific audience like C-level or compliance), generate a custom summary using the ADR YAML as context, following the same structure: decision, rationale, alternatives, tradeoffs, impact, next steps.

## Validation

The `scripts/validate-adr.py` script validates any ADR YAML file against the JSON Schema:

```bash
# Validate a single ADR
python3 scripts/validate-adr.py path/to/ADR-0001.yaml

# Validate all ADRs in a directory
python3 scripts/validate-adr.py architecture-decision-log/
```

The script exits with code 0 if valid, 1 if validation errors are found.
````

## File: docs/glossary.md
````markdown
# ADR Governance — Glossary

## Core Concepts

| Term | Definition |
|------|-----------|
| **ADR** | Architecture Decision Record. A structured document capturing a significant architectural decision, its context, alternatives considered, and consequences. |
| **ADR Administrator** | A person listed in `.adr-governance/config.yaml` who is authorised to make maintenance (Tier 2) changes to any ADR without requiring re-approval from the original ADR approvers. See `adr-process.md` §3.4.4. |
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
| ADR | `ADR-NNNN` or `ADR-NNNN-slug` | `ADR-0001`, `ADR-0001-dpop-over-mtls` |
| Functional Requirement | `F-NNN` | `F-001` |
| Non-Functional Requirement | `NF-NNN` | `NF-001` |
| Risk | `R-NNN` | `R-001` |

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
````

## File: schemas/adr.schema.json
````json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://github.com/ivanstambuk/adr-governance/blob/main/schemas/adr.schema.json",
    "title": "Architecture Decision Record",
    "description": "Self-contained ADR meta-model for governed architectural decisions. Each ADR embeds all context, requirements, alternatives, consequences, and audit trails. All string fields support Markdown including embedded Mermaid diagrams via code fences.",
    "version": "1.0.0",
    "type": "object",
    "required": [
        "adr",
        "authors",
        "decision_owner",
        "context",
        "alternatives",
        "decision",
        "consequences",
        "confirmation"
    ],
    "additionalProperties": false,
    "patternProperties": {
        "^x-": {
            "description": "Extension fields. Teams may add custom metadata using the x- prefix without breaking schema validation."
        }
    },
    "properties": {
        "adr": {
            "type": "object",
            "description": "Core ADR metadata and identification.",
            "required": [
                "id",
                "title",
                "status",
                "created_at",
                "version",
                "project",
                "decision_type"
            ],
            "additionalProperties": false,
            "properties": {
                "id": {
                    "type": "string",
                    "pattern": "^ADR-[0-9]{4}(-[a-z0-9]+)*$",
                    "description": "Unique identifier in ADR-NNNN or ADR-NNNN-slug format."
                },
                "title": {
                    "type": "string",
                    "minLength": 10,
                    "maxLength": 200,
                    "description": "Human-readable decision title."
                },
                "summary": {
                    "type": "string",
                    "maxLength": 500,
                    "description": "Executive elevator pitch (2–4 sentences). Enables stakeholders to triage ADRs without reading the full document."
                },
                "status": {
                    "type": "string",
                    "enum": [
                        "draft",
                        "proposed",
                        "accepted",
                        "superseded",
                        "deprecated",
                        "rejected",
                        "deferred"
                    ],
                    "description": "Current lifecycle status of the decision."
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "ISO 8601 timestamp of initial creation."
                },
                "last_modified": {
                    "type": "string",
                    "format": "date-time",
                    "description": "ISO 8601 timestamp of last modification."
                },
                "version": {
                    "type": "string",
                    "pattern": "^[0-9]+\\.[0-9]+$",
                    "description": "Document version of this ADR (MAJOR.MINOR). Not to be confused with schema_version."
                },
                "schema_version": {
                    "type": "string",
                    "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
                    "description": "Version of the ADR schema this document conforms to (MAJOR.MINOR.PATCH)."
                },
                "project": {
                    "type": "string",
                    "minLength": 1,
                    "description": "Project or programme this decision belongs to."
                },
                "component": {
                    "type": "string",
                    "description": "Specific component, module, or subsystem affected."
                },
                "tags": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "uniqueItems": true,
                    "description": "Categorization tags for discovery and filtering."
                },
                "priority": {
                    "type": "string",
                    "enum": [
                        "low",
                        "medium",
                        "high",
                        "critical"
                    ],
                    "description": "Priority level of the decision."
                },
                "decision_type": {
                    "type": "string",
                    "enum": [
                        "technology",
                        "process",
                        "organizational",
                        "vendor",
                        "security",
                        "compliance"
                    ],
                    "description": "Classification of the decision domain."
                }
            }
        },
        "authors": {
            "type": "array",
            "minItems": 1,
            "items": {
                "$ref": "#/$defs/person"
            },
            "description": "Authors who drafted this ADR."
        },
        "decision_owner": {
            "$ref": "#/$defs/person",
            "description": "Accountable owner for this decision."
        },
        "reviewers": {
            "type": "array",
            "items": {
                "$ref": "#/$defs/person"
            },
            "description": "Individuals who reviewed this ADR."
        },
        "approvals": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "name",
                    "role"
                ],
                "additionalProperties": false,
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "role": {
                        "type": "string"
                    },
                    "identity": {
                        "type": "string",
                        "description": "Platform-resolvable handle for CI approval verification. Use the format your Git platform identifies approvers by: GitHub username (e.g., '@janedoe'), Azure DevOps email or UPN, GitLab username. CI pipelines use this field to verify that every listed approver actually approved the pull request before merge."
                    },
                    "approved_at": {
                        "type": [
                            "string",
                            "null"
                        ],
                        "format": "date-time",
                        "description": "ISO 8601 timestamp when approval was given, null if pending."
                    },
                    "signature_id": {
                        "type": [
                            "string",
                            "null"
                        ],
                        "description": "External signature or ticket ID for audit trail."
                    }
                }
            },
            "description": "Formal approvals with optional timestamps, platform identity for CI verification, and signature references. The identity field enables CI pipelines to verify that every listed approver actually approved the pull request."
        },
        "context": {
            "type": "object",
            "required": [
                "summary"
            ],
            "additionalProperties": false,
            "properties": {
                "summary": {
                    "type": "string",
                    "minLength": 20,
                    "description": "Narrative summary of the problem and context. Supports Markdown with embedded Mermaid diagrams, code blocks, and rich formatting."
                },
                "business_drivers": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Business motivations behind this decision."
                },
                "technical_drivers": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Technical motivations and quality attributes."
                },
                "constraints": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Non-negotiable constraints that bound the solution space."
                },
                "assumptions": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Assumptions made when evaluating alternatives."
                }
            },
            "description": "Context, drivers, constraints, and assumptions."
        },
        "requirements": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "functional": {
                    "type": "array",
                    "items": {
                        "$ref": "#/$defs/requirement"
                    },
                    "description": "Functional requirements addressed by this decision."
                },
                "non_functional": {
                    "type": "array",
                    "items": {
                        "$ref": "#/$defs/requirement"
                    },
                    "description": "Non-functional / quality attribute requirements."
                }
            },
            "description": "Architecturally significant requirements (ASRs) embedded in this ADR."
        },
        "alternatives": {
            "type": "array",
            "minItems": 2,
            "items": {
                "type": "object",
                "required": [
                    "name",
                    "summary",
                    "pros",
                    "cons"
                ],
                "additionalProperties": false,
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Short name for this alternative."
                    },
                    "summary": {
                        "type": "string",
                        "description": "Description of the alternative. Supports Markdown with embedded Mermaid diagrams, code blocks, and rich formatting."
                    },
                    "pros": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "minLength": 1
                        },
                        "minItems": 1,
                        "description": "Advantages of this alternative."
                    },
                    "cons": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "minLength": 1
                        },
                        "minItems": 1,
                        "description": "Disadvantages or risks of this alternative."
                    },
                    "estimated_cost": {
                        "type": "string",
                        "enum": [
                            "low",
                            "medium",
                            "high"
                        ],
                        "description": "Relative cost estimate."
                    },
                    "risk": {
                        "type": "string",
                        "enum": [
                            "low",
                            "medium",
                            "high",
                            "critical"
                        ],
                        "description": "Overall risk level of this alternative."
                    },
                    "rejection_rationale": {
                        "type": "string",
                        "description": "Why this alternative was not chosen. Only applicable to rejected alternatives. Inspired by Merson/DRF."
                    }
                }
            },
            "description": "At least two alternatives must be considered for every decision."
        },
        "decision": {
            "type": "object",
            "required": [
                "chosen_alternative",
                "rationale",
                "decision_date"
            ],
            "additionalProperties": false,
            "properties": {
                "chosen_alternative": {
                    "type": "string",
                    "description": "Name of the selected alternative. Should match a name in the alternatives array (enforced by tooling, not schema)."
                },
                "rationale": {
                    "type": "string",
                    "minLength": 20,
                    "description": "Reasons supporting this choice. Supports Markdown with embedded Mermaid diagrams, code blocks, and rich formatting."
                },
                "tradeoffs": {
                    "type": "string",
                    "description": "Acknowledged tradeoffs accepted with this decision. Supports Markdown."
                },
                "decision_date": {
                    "type": "string",
                    "format": "date",
                    "description": "ISO 8601 date when the decision was made."
                },
                "confidence": {
                    "type": "string",
                    "enum": [
                        "low",
                        "medium",
                        "high"
                    ],
                    "description": "Confidence level in this decision. Low-confidence decisions should have shorter review cycles and be prioritized for reconsideration."
                }
            },
            "description": "The chosen alternative and its justification."
        },
        "consequences": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": false,
            "properties": {
                "positive": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Expected positive outcomes."
                },
                "negative": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Expected negative outcomes or costs."
                }
            },
            "description": "Consequences and implications of the decision."
        },
        "confirmation": {
            "type": "object",
            "required": [
                "description"
            ],
            "additionalProperties": false,
            "properties": {
                "description": {
                    "type": "string",
                    "description": "How the implementation of this decision will be verified. Supports Markdown. E.g. code review, ArchUnit test, design review, load test."
                },
                "artifact_ids": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Delivery artifact references that confirm implementation. E.g. Jira tickets, PR URLs, test suite IDs, sprint items."
                }
            },
            "description": "How compliance with this ADR is confirmed. Links the decision to its verification evidence."
        },
        "dependencies": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "internal": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Internal service or team dependencies."
                },
                "external": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "External vendor or third-party dependencies."
                }
            },
            "description": "Internal and external dependencies."
        },
        "references": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "title",
                    "url"
                ],
                "additionalProperties": false,
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "url": {
                        "type": "string",
                        "format": "uri"
                    }
                }
            },
            "description": "External references, standards, and evidence."
        },
        "lifecycle": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "review_cycle_months": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "How often (in months) this decision should be reviewed."
                },
                "next_review_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Next scheduled review date."
                },
                "superseded_by": {
                    "type": [
                        "string",
                        "null"
                    ],
                    "pattern": "^ADR-[0-9]{4}(-[a-z0-9]+)*$",
                    "description": "ADR ID that supersedes this one, if any."
                },
                "supersedes": {
                    "type": [
                        "string",
                        "null"
                    ],
                    "pattern": "^ADR-[0-9]{4}(-[a-z0-9]+)*$",
                    "description": "ADR ID that this one supersedes, if any."
                },
                "archival": {
                    "type": "object",
                    "additionalProperties": false,
                    "properties": {
                        "archived_at": {
                            "type": [
                                "string",
                                "null"
                            ],
                            "format": "date-time"
                        },
                        "archive_reason": {
                            "type": [
                                "string",
                                "null"
                            ]
                        }
                    }
                }
            },
            "description": "Lifecycle management: review cadence, supersession chain, archival."
        },
        "audit_trail": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "event",
                    "by",
                    "at"
                ],
                "additionalProperties": false,
                "properties": {
                    "event": {
                        "type": "string",
                        "enum": [
                            "created",
                            "updated",
                            "reviewed",
                            "approved",
                            "rejected",
                            "deferred",
                            "superseded",
                            "deprecated",
                            "archived"
                        ],
                        "description": "Type of lifecycle event."
                    },
                    "by": {
                        "type": "string",
                        "description": "Person or system that triggered the event."
                    },
                    "at": {
                        "type": "string",
                        "format": "date-time",
                        "description": "ISO 8601 timestamp."
                    },
                    "details": {
                        "type": "string",
                        "description": "Optional additional context."
                    }
                }
            },
            "description": "Immutable audit trail of all lifecycle events."
        }
    },
    "$defs": {
        "person": {
            "type": "object",
            "required": [
                "name",
                "role"
            ],
            "additionalProperties": false,
            "properties": {
                "name": {
                    "type": "string",
                    "minLength": 1
                },
                "role": {
                    "type": "string",
                    "minLength": 1
                },
                "email": {
                    "type": "string",
                    "format": "email"
                }
            }
        },
        "requirement": {
            "type": "object",
            "required": [
                "id",
                "description"
            ],
            "additionalProperties": false,
            "properties": {
                "id": {
                    "type": "string",
                    "pattern": "^(F|NF)-[0-9]{3}$",
                    "description": "Functional (F-NNN) or Non-Functional (NF-NNN) requirement ID. Scoped per ADR — each ADR starts from F-001 / NF-001."
                },
                "description": {
                    "type": "string"
                }
            }
        }
    }
}
````

## File: docs/adr-process.md
````markdown
# ADR Governance Process

> **Status:** Normative
> **Last updated:** 2026-03-06

This document defines the process for proposing, reviewing, approving, and maintaining Architecture Decision Records (ADRs) in this repository. The process is **GitOps-based**: all state transitions happen through Git commits and pull requests.

### Quick Reference

| I want to... | Do this |
|--------------|---------|
| Start a new decision | Branch → create YAML in `architecture-decision-log/` with `status: draft` → iterate |
| Submit for review | Set `status: proposed` → open PR → assign reviewers |
| Approve a decision | Approve the PR → author sets `status: accepted` → merge |
| Reject a decision | Comment reason → author sets `status: rejected` → merge (preserve history) |
| Defer a decision | Comment reason → author sets `status: deferred` → close PR with label |
| Supersede a decision | Create new ADR referencing old one → accept new → update old to `superseded` |
| Deprecate a decision | Set `status: deprecated` + audit event → merge |
| Archive a decision | Set `lifecycle.archival` fields + `archived` audit event → merge |
| Confirm implementation | Add `confirmation.description` + `confirmation.artifact_ids` in follow-up PR |
| Periodic review | Check `lifecycle.next_review_date` → verify or supersede |

> See the full sections below for detailed workflows.

---

## 1. Roles

| Role | Responsibility |
|------|---------------|
| **Author** | Drafts the ADR. Populates all required fields. |
| **Decision Owner** | Single accountable person for the decision (named in `decision_owner`). Drives the review. May or may not be the author. |
| **Reviewer** | Reviews the ADR for technical correctness, completeness, and alignment with existing decisions. Named in `reviewers`. |
| **Approver** | Provides formal approval. Named in `approvals`. Typically: Tech Lead, Architect, CISO, or DPO depending on `decision_type`. |

---

## 2. Status Lifecycle


```mermaid
stateDiagram-v2
    [*] --> draft

    draft --> proposed : Author pushes branch,<br>opens PR

    proposed --> proposed : No decision reached —<br>reviewers Request Changes,<br>action items in PR comments,<br>author reworks & pushes
    proposed --> accepted : All approvers approve PR<br>→ PR merged
    proposed --> rejected : Rejected with documented reason<br>→ PR merged (preserves history)
    proposed --> deferred : Postponed<br>→ PR closed with label

    deferred --> proposed : Author reopens<br>or opens new PR

    accepted --> superseded : New ADR accepted<br>that replaces this one<br>→ PR merged
    accepted --> deprecated : No longer recommended<br>→ PR merged

    rejected --> [*]
    deferred --> [*]
    superseded --> [*]
    deprecated --> [*]

    note right of draft : WIP on feature branch.<br>Not ready for review.
    note right of proposed : PR is open.<br>Under active review.
    note right of deferred : Parked — revisit later.<br>PR is closed.
    note left of accepted : Decision is binding.<br>ADR is immutable.
    note right of rejected : Decision log entry.<br>Preserved for historical record.
    note left of superseded : Replaced by newer ADR.<br>See lifecycle.superseded_by.
    note left of deprecated : Still in codebase but<br>no longer recommended.
```

**Valid transitions:**

| ADR Status (from) | ADR Status (to) | PR State | Trigger |
|:------------------:|:----------------:|:--------:|---------|
| `draft` | `proposed` | **opened** | Author pushes branch and opens PR |
| `proposed` | `proposed` | **open** (changes requested) | Reviewed but no decision — reviewers request changes, author reworks |
| `proposed` | `accepted` | **merged** | All required approvers approve the PR |
| `proposed` | `rejected` | **merged** | Approvers reject — ADR is merged to preserve the historical record |
| `proposed` | `deferred` | **closed** | Decision postponed; PR closed with `deferred` label |
| `deferred` | `proposed` | **opened** (new or reopened) | Author reopens or opens new PR |
| `accepted` | `superseded` | **merged** (via superseding ADR's PR) | New ADR accepted that replaces this one |
| `accepted` | `deprecated` | **merged** (standalone PR) | Decision no longer recommended |

> **Why are rejected ADRs merged?** Rejected ADRs are part of the decision log — they document *why* an option was evaluated and not pursued. Closing the PR without merging would lose this history from `main`.

---

## 3. Workflow: Proposing a New ADR

### 3.0 Should You Write an ADR? — Architectural Significance Test

Not every technical decision needs a full ADR. Before starting, verify that **at least one** of the following applies:

| # | Significance Criterion |
|---|------------------------|
| 1 | The decision affects **multiple components, teams, or services** |
| 2 | The decision is **difficult or expensive to reverse** |
| 3 | The decision has **security, compliance, or regulatory** implications |
| 4 | The decision **establishes a pattern** that others will follow |
| 5 | The decision involves a **tradeoff between quality attributes** (e.g., security vs. usability, latency vs. consistency) |
| 6 | Someone will ask **"why did we do this?"** in 6 months |

If **none** of these apply, the decision is likely not architecturally significant — just make it, document it inline (code comment, wiki, commit message), and move on.

> **Source:** Adapted from Zimmermann's [Architectural Significance Test](https://ozimmer.ch/practices/2020/09/24/ASRTestECSADecisions.html). See also: *"An AD log with more than 100 entries will probably put your readers (and you) to sleep."*

### 3.1 Draft Phase

1. **Create a branch** from `main`:
   ```bash
   git checkout -b adr/ADR-NNNN-short-title
   ```

2. **Create the ADR file** in `architecture-decision-log/` using the schema:
   ```bash
   cp examples-reference/ADR-0001-*.yaml architecture-decision-log/ADR-NNNN-short-title.yaml
   ```

3. **Set status to `draft`** while authoring:
   ```yaml
   adr:
     id: "ADR-NNNN"
     status: "draft"
   ```

4. **Iterate locally.** Validate against the schema:
   ```bash
   python3 scripts/validate-adr.py architecture-decision-log/ADR-NNNN-short-title.yaml
   ```

### 3.2 Proposal Phase

5. **Set status to `proposed`** when the ADR is complete and ready for review:
   ```yaml
   adr:
     status: "proposed"
   ```

6. **Open a Pull Request.** The PR title should match the ADR title:
   ```
   ADR-NNNN: Short decision title
   ```

7. **Assign reviewers.** Add all stakeholders listed in the ADR's `reviewers` and `approvals` sections as PR reviewers.

8. **CI validates** the ADR automatically (schema validation runs on PR).

### 3.3 Review Phase

9. **Reviewers read the ADR** in the PR. They have **5 business days** to review (configurable per team).

10. **Review checklist** — reviewers should verify:
    - [ ] Context is clear and complete
    - [ ] At least 2 alternatives are genuinely considered (not strawmen)
    - [ ] Pros/cons are balanced and honest
    - [ ] Rationale explains *why* the chosen option is preferred
    - [ ] Tradeoffs are explicitly acknowledged
    - [ ] Risk assessment covers realistic failure modes
    - [ ] No conflict with existing `accepted` ADRs (search `architecture-decision-log/` for related decisions)
    - [ ] `approvals[].identity` is populated with the platform handle for each required approver (§3.4.1)

11. **Reviewers comment on the PR.** Discussions happen in PR comments.

12. **Author addresses feedback** by pushing new commits to the branch.

> **Note on `reviewed` audit events:** The initial proposal review happens through the PR process. Do **not** add a `reviewed` event to `audit_trail` during the initial review — the `approved` or `rejected` event records the outcome. The `reviewed` event is reserved for **periodic reviews** (§9) of already-accepted ADRs.

### 3.4 Approval Phase

13. **All required approvers must approve the PR** before merge. This is enforced via GitHub branch protection rules:
    - Require approvals from designated CODEOWNERS
    - Require passing CI (schema validation + approval identity verification)
    - No self-approval (author cannot be sole approver)

14. **Once approved:**
    - Author (or decision owner) sets status to `accepted`
    - Author populates `decision.decision_date`
    - Author adds entries to `approvals` with names, roles, **platform identities**, and timestamps
    - Author adds an `approved` event to `audit_trail`

    > **Who sets the status?** The author or decision owner updates the YAML. The branch protection rules prevent self-approval — the author cannot be the *sole* approver. Setting the status to `accepted` is a clerical action that happens *after* PR approval, not a governance action.

    > **Bootstrap exception:** ADR-0000 (the meta-ADR adopting this governance process) was self-approved by the initial author. The no-self-approval rule applies to all subsequent ADRs.

15. **Merge the PR** to `main`. The ADR is now binding.

### 3.4.1 Approval Identity Rule

> **Principle:** The ADR's `approvals[]` list and the pull request's actual approvers **must match**. Every person listed in `approvals` must have actually approved the pull request, and their `identity` field must resolve to their platform account.

The `identity` field on each approval entry is the **platform-resolvable handle** that CI uses to verify the approval:

| Platform | Identity format | Example | API used for verification |
|----------|----------------|---------|--------------------------|
| GitHub | `@username` | `@janedoe` | `GET /repos/{owner}/{repo}/pulls/{number}/reviews` |
| Azure DevOps | Email or UPN | `jane.doe@org.com` | `GET /_apis/git/pullRequests/{id}/reviewers` |
| GitLab | `@username` | `@janedoe` | `GET /projects/:id/merge_requests/:iid/approval_state` |
| AWS CodeBuild | *(uses GitHub/CodeCommit API)* | Depends on source | Depends on source provider |
| GCP Cloud Build | *(uses GitHub API)* | Depends on source | Depends on source provider |

**How CI enforcement works:**

1. The CI pipeline detects which ADR files were changed in the PR
2. For each changed ADR with `status: proposed` or `status: accepted`:
   - Extracts all `approvals[].identity` values
   - Queries the platform API for the list of users who **actually approved** the PR
   - Compares the two sets
3. **If any listed approver has not approved the PR**, the check fails and merge is blocked
4. **If the ADR has no `identity` fields**, the check emits a warning but does not block (backward-compatible)

> **Why this matters:** Without this rule, anyone can write arbitrary names in `approvals[]` and merge with a different set of PR approvers. The identity binding ensures that the ADR's formal approval record matches the Git platform's cryptographic approval record.

> **When to populate `identity`:** Add the `identity` field when the ADR enters `proposed` status and approvers are known. The field uses whatever format your Git platform identifies reviewers by — typically a username prefixed with `@`.

**Example:**

```yaml
approvals:
  - name: "Jane Doe"
    role: "Lead Architect"
    identity: "@janedoe"          # ← CI verifies this account approved the PR
    approved_at: "2026-03-15T10:00:00Z"
    signature_id: sig-example-001
```

### 3.4.2 Single ADR per PR

> **Rule:** A pull request may modify **at most one ADR file**.

This ensures each merge commit maps to exactly one architectural decision, keeping the git history clean and making individual decisions easy to revert.

**Exception — supersession pairs:** When a new ADR supersedes an existing one, the PR must touch exactly **two** ADR files:
- The **new ADR** (with `lifecycle.supersedes: ADR-NNNN`)
- The **old ADR** (with `status: superseded` and `lifecycle.superseded_by: ADR-MMMM`)

The CI script validates this automatically — if a PR modifies two ADRs that form a valid supersession chain (the symmetry is verified), the check passes. Any other multi-ADR PR is rejected.

This rule is configured in `.adr-governance/config.yaml`:

```yaml
governance:
  single_adr_per_pr: true
```

### 3.4.3 Change Classification

Not all changes to an ADR are equal. The governance framework distinguishes between **substantive** and **maintenance** changes:

#### Tier 1 — Substantive Changes (full approval required)

Changes to fields that affect the *decision itself*. These require the original ADR approvers (listed in `approvals[].identity`) to re-approve via the PR:

| Field | Why it's substantive |
|-------|---------------------|
| `adr.status` | Changes the governance state of the decision |
| `adr.title` | Reframes what the decision is about |
| `decision.*` | Alters the chosen alternative, rationale, tradeoffs, or confidence |
| `alternatives.*` | Changes the options that were evaluated |
| `consequences.*` | Modifies the expected outcomes |
| `approvals.*` | Adds, removes, or changes approver records |
| `context.summary` | Reframes the problem statement |

#### Tier 2 — Maintenance Changes (no ADR re-approval required)

Changes to non-decision fields. These are clerical or additive updates that don't alter the architectural decision:

- `adr.schema_version` — schema migration
- `adr.last_modified`, `adr.tags`, `adr.component` — metadata updates
- `authors[].email` — contact info correction
- `reviewers` — adding reviewers
- `context.business_drivers`, `context.technical_drivers`, `context.constraints`, `context.assumptions` — clarification, not reframing
- `requirements`, `dependencies`, `references` — adding supporting information
- `lifecycle.next_review_date`, `lifecycle.review_cycle_months` — review cadence
- `audit_trail` — adding events (always append-only)
- `confirmation.artifact_ids` — backfilling verification evidence

Maintenance changes still require a standard PR approval via branch protection, but the `verify-approvals.py` identity check is **skipped**. An `updated` event should be added to `audit_trail`:

```yaml
audit_trail:
  - event: updated
    by: Ivan Stambuk
    at: "2026-03-10T14:00:00Z"
    details: "Administrative: corrected reviewer email address"
```

The substantive fields list is configured in `.adr-governance/config.yaml` and can be customized per organisation.

### 3.4.4 ADR Administrator

An **ADR Administrator** is a person authorised to make Tier 2 (maintenance) changes to any ADR without obtaining the original ADR approvers' re-approval. This is useful for:

- Typo fixes and formatting corrections
- Schema version bumps during migrations
- Updating contact information (emails, names)
- Adding references or clarifying context
- Updating review cadence dates

Administrators are listed in `.adr-governance/config.yaml`:

```yaml
governance:
  admins:
    - identity: "ivanstambuk"
      name: "Ivan Stambuk"
    - identity: "elenavasquez"
      name: "Elena Vasquez"
```

**How it works in CI:**

1. The CI script detects the **PR author** from platform environment variables
2. If the PR author is listed as an admin in the governance config:
   - **Substantive changes** → full approval identity verification (same as non-admins)
   - **Maintenance changes** → approval identity check is skipped; only standard branch protection applies
3. If the PR author is **not** an admin:
   - **Substantive changes** → full approval identity verification
   - **Maintenance changes** → approval identity check is still skipped (maintenance changes never require ADR re-approval), but standard branch protection applies

> **Key point:** The admin role doesn't grant the ability to make substantive changes without approval. It only provides an explicit governance signal in CI output. Maintenance changes skip the identity check for *everyone* — the admin designation is primarily for auditability and clarity.

> **Governance of the config itself:** Changes to `.adr-governance/config.yaml` should be subject to the same review process as any governance artefact. Add it to `CODEOWNERS` so that admin roster changes require approval from the architecture team.


### 3.5 Rejection

16. If the PR is rejected:
    - Author sets status to `rejected`
    - Rejection reason is documented in the PR and in the ADR's `audit_trail`
    - PR is **merged** (not closed) — rejected ADRs are preserved for historical record

> **What does `chosen_alternative` mean for rejected ADRs?** When the *proposal* is rejected but the team selects a different approach (e.g., ADR-0007: Vault was proposed but native cloud stores were chosen), `chosen_alternative` records the alternative the team will actually pursue. The `status: rejected` signals that the *proposed approach* was rejected, not the ADR itself. The ADR serves as a record of both the rejection and the actual path forward.

---

## 4. Workflow: Re-proposing a Deferred ADR

A deferred ADR can be re-proposed when the blocking condition is resolved.

1. **Determine what changed.** The author or decision owner identifies why the ADR is now ready — new information, resolved dependency, changed priority, or elapsed time.
2. **Open a new PR** (preferred) or reopen the original PR:
   - Update `adr.status` to `proposed`
   - Update `context.summary` if the landscape has changed
   - Add an `updated` event to `audit_trail` explaining why the ADR is being re-proposed
3. Follow the standard review process (§3.3–3.4).

---

## 5. Workflow: Superseding an Existing ADR

1. **Create a new ADR** (ADR-MMMM) following the standard proposal workflow
2. In the new ADR, set the supersession field:
   ```yaml
   lifecycle:
     supersedes: "ADR-NNNN"
   ```
3. When the new ADR is accepted, **update the old ADR** in the same PR:
   - Set `adr.status: "superseded"`
   - Set `lifecycle.superseded_by: "ADR-MMMM"`
   - Add a `superseded` event to `audit_trail`

> **Symmetry rule:** Both fields must be set — the new ADR's `lifecycle.supersedes` and the old ADR's `lifecycle.superseded_by`. The validator checks this.

---

## 6. Workflow: Deprecating an ADR

Deprecation marks a decision as no longer recommended, but not yet replaced.

1. **Open a PR** that updates the existing ADR:
   - Set `adr.status: "deprecated"`
   - Add a `deprecated` event to `audit_trail` with reason
2. **When to deprecate** (vs. supersede):
   - **Deprecate** when the decision is outdated but no replacement has been decided yet
   - **Supersede** when a new ADR has been accepted that replaces this one
3. A deprecated ADR should eventually be either superseded by a new ADR or left as a historical record.

> **Timestamp convention:** Unlike archival (which has a dedicated `lifecycle.archival.archived_at` field), deprecation has no dedicated timestamp field. The deprecation time is recorded in the `audit_trail` via the `deprecated` event's `at` field. This is intentional — deprecation is a transitional state, not a terminal one.

---

## 7. Workflow: Confirming Implementation

After an ADR is accepted, the team must verify it was actually implemented.

1. **Populate the `confirmation` field** as implementation progresses:
   ```yaml
   confirmation:
     description: "Verified via integration test suite and code review of PR #142"
     artifact_ids:
       - "JIRA-1234"
       - "https://github.com/org/repo/pull/142"
       - "TEST-SUITE-auth-dpop-e2e"
   ```

2. Confirmation can be added in a follow-up PR after the ADR is accepted.

3. **Recommended artifact types** for `confirmation.artifact_ids`:

   | Prefix / Format | Example | Use When |
   |-----------------|---------|----------|
   | Jira / GitHub issue | `JIRA-1234`, `https://github.com/org/repo/issues/42` | Implementation tracked in an issue |
   | Pull request | `https://github.com/org/repo/pull/142` | Code change that implements the decision |
   | Test suite | `TEST-SUITE-auth-dpop-e2e` | Automated tests that verify the decision |
   | Fitness function | `archunit:no-direct-db-access` | ArchUnit / architectural lint rule |
   | PoC / Experiment | `POC-2026-03-dpop-latency-benchmark` | Proof-of-concept that validated the decision |
   | Benchmark | `BENCH-jwt-signing-ed25519-vs-rsa` | Performance data supporting the choice |
   | Sprint review | `SPRINT-42-review-notes` | Review meeting where implementation was demonstrated |

   > The strongest decision confirmations are **empirical** — PoC results, benchmarks, and passing fitness functions carry more weight than tickets alone.

   > **Schema note:** The `confirmation.artifact_ids` field in the schema accepts arbitrary strings. Use the prefixes above for consistency. See [`adr.schema.json`](../schemas/adr.schema.json) → `confirmation` definition.

4. **During code reviews**, reviewers should check if a proposed change **violates any accepted ADR**. If it does:
   - Link the relevant ADR in the review comment
   - Request the author to either update the code or propose a new superseding ADR

---

## 8. Archival

Archival is for decisions that are no longer active and should be removed from regular consideration. Archival is distinct from supersession (replaced by a newer ADR) and deprecation (no longer recommended).

**When to archive:**
- A `superseded` ADR whose successor has been accepted **and** confirmed
- A `deprecated` ADR whose replacement is fully operational
- A `rejected` ADR that is no longer relevant to revisit

**How to archive:**

1. Update the ADR YAML:
   ```yaml
   lifecycle:
     archival:
       archived_at: "2026-06-15T10:00:00Z"
       archive_reason: "Superseded by ADR-0008; original decision fully replaced and confirmed."
   ```
2. Add an `archived` event to `audit_trail`:
   ```yaml
   audit_trail:
     - event: archived
       by: Elena Vasquez
       at: "2026-06-15T10:00:00Z"
       details: "Superseded by ADR-0008. Successor confirmed in production."
   ```
3. Submit as a PR and merge.

> **Never delete an ADR.** Archival preserves the decision record for historical reference and audit compliance. Archived ADRs remain in the `architecture-decision-log/` directory.

---

## 9. Periodic Review

ADRs with `lifecycle.review_cycle_months` set will be flagged for periodic review.

1. When the `lifecycle.next_review_date` arrives, the decision owner should:
   - Verify the decision is still valid and the context hasn't changed
   - If still valid: update `next_review_date` and add a `reviewed` event to `audit_trail`
   - If no longer valid: propose a superseding ADR or deprecate

2. **Retrospective questions** — use these to guide the periodic review:

   | # | Question |
   |---|----------|
   | 1 | Did the **consequences we predicted** actually occur? |
   | 2 | Were there **unforeseen consequences** we should document? |
   | 3 | Has the **context changed** since this decision was made? |
   | 4 | Was the **confidence level** of this decision appropriate? |
   | 5 | Have we accumulated **technical debt** from this decision? |
   | 6 | Is this decision **still the right choice** given what we now know? |
   | 7 | Should we trigger a **superseding ADR**? |

   > These questions focus on improving the *decision-making process*, not just the architecture. Adapted from [Cervantes & Woods, "Architectural Retrospectives"](https://www.infoq.com/articles/architectural-retrospectives/).

3. **Confidence-driven review frequency.** Use `decision.confidence` to set default review cadence:

   | Confidence | Recommended `review_cycle_months` | Rationale |
   |------------|----------------------------------|----------|
   | `low` | 6 | Decision made under pressure or with incomplete data — re-evaluate early |
   | `medium` | 12 | Standard review cycle |
   | `high` | 24 | Strong empirical evidence — extended cycle acceptable |


---


## 10. Schema Versioning Policy

Each ADR records the schema version it was authored against in `adr.schema_version`.

| Rule | Detail |
|------|--------|
| **Schema version is pinned at creation time** | When an ADR is created, set `schema_version` to the current version of `adr.schema.json`. |
| **Existing ADRs are NOT updated** when the schema evolves | If the schema adds new optional fields, old ADRs remain valid without modification. |
| **Backward compatibility is required** | New schema versions MUST validate all existing ADRs without errors. Only add optional fields; never make previously-optional fields required. |
| **Breaking changes require migration** | If a required field is added or renamed, provide a migration script and bump the major version. Update `schema_version` in affected ADRs. |
| **Current version** | `1.0.0` (see `schemas/adr.schema.json`) |

---

## 11. Branch Protection Rules (Recommended)

Configure in GitHub repository settings → Branches → `main`:

```
✅ Require a pull request before merging
✅ Require approvals: 1 (minimum; increase per decision_type)
✅ Require review from Code Owners
✅ Require status checks to pass (CI: schema validation)
✅ Require conversation resolution before merging
❌ Allow force pushes (never)
❌ Allow deletions (never)
```

### CODEOWNERS (recommended)

Create a `CODEOWNERS` file to enforce that the right people review ADRs:

```
# All ADRs require architect approval
architecture-decision-log/    @org/architecture-team

# Security decisions additionally require CISO
architecture-decision-log/ADR-*security*    @org/security-team

# Compliance decisions additionally require DPO
architecture-decision-log/ADR-*compliance*  @org/compliance-team
```

> **Note:** CODEOWNERS wildcard patterns match on *filename*, not on `decision_type` inside the YAML. To ensure correct reviewer assignment, include the decision domain in the ADR filename (e.g., `ADR-0007-security-adopt-passkeys.yaml`). For more sophisticated routing, use a CI-based reviewer assignment step that reads `decision_type` from the YAML and requests the appropriate team via the GitHub API.
````

## File: README.md
````markdown
# adr-governance

A schema-governed, AI-native **Architecture Decision Record (ADR)** framework for teams that want their architectural decisions to be **structured**, **traceable**, and **asynchronous** — not debated in meetings, forgotten in Slack threads, or buried in wiki pages nobody reads.

## The Problem

Most teams make **Architecture Decisions (ADs)** every week. Few document them well. Decisions happen in meetings where the loudest voice wins, context is lost the moment people leave the room, and six months later nobody can explain *why* something was built the way it was.

- **Meetings are the wrong medium for decisions.** They reward whoever is present and articulate in the moment, not whoever has done the deepest analysis. They produce no durable artifact. They don't scale across time zones.
- **Decisions without structure are decisions without quality.** When there's no template forcing you to consider alternatives, tradeoffs, and risks, corners get cut. Important ADs get made on gut feeling.
- **Undocumented decisions create compliance gaps.** Auditors ask for evidence of decision-making and get blank stares. New team members have no way to understand *why* the architecture looks the way it does.
- **Documented decisions that aren't enforced are just suggestions.** Even teams that write **Architecture Decision Records (ADRs)** rarely close the loop. The decision says "use DPoP," but nothing stops someone from committing mTLS code. Without a feedback mechanism from the **Architecture Decision Log (ADL)** back to the codebase, decisions and implementation drift apart silently.
- **Traditional tooling is a dead end for scalable decision management.** Decisions captured in Confluence pages, SharePoint wikis, PowerPoint decks, Notion databases, or meeting minutes in Microsoft Teams are *opaque to machines*. They can't be schema-validated, they don't support programmable multi-party approval workflows, they can't be diffed or version-controlled with meaningful merges, and — critically — they can't be consumed by AI agents or CI pipelines for automated enforcement. As AI becomes central to the software delivery chain, decisions locked in proprietary formats become an integration liability. A structured, Git-native, schema-governed ADL is AI-native by design — every improvement in AI tooling automatically makes your decision management better, because the data is already in the right shape.

The alternative is **shift-left decision-making**: instead of debating in a meeting, the proposer prepares a well-structured ADR upfront — context, alternatives, risks, tradeoffs — and submits it as a pull request. Every stakeholder can review it asynchronously, on their own time, with full context in front of them. The decision process becomes a code review, not a calendar invite. And because it's GitOps-native, every approval by every relevant stakeholder is traceable — who approved what, when, and with what context — for free.

AI makes this dramatically better — and not just for validation. A well-structured schema means AI assistants can help **author** ADRs through Socratic dialogue (probing for gaps, challenging vague rationale, surfacing unstated assumptions), **review** them before any human sees them (verifying completeness, flagging ambiguities, checking cross-reference consistency), and **enforce** them against your codebase (validating code compliance with accepted decisions in CI). The proposer doesn't fill in a template manually — they have a *conversation* with an AI assistant that interrogates them until every section is clear, complete, and internally consistent. By the time the ADR reaches a human reviewer, the low-hanging issues are already resolved. The reviewer focuses on strategic judgement, not on asking "what do you mean by 'scalable'?" This is what shift-left means for architecture governance.

Good **Architecture Knowledge Management (AKM)** treats decisions as first-class engineering artifacts — not afterthoughts. Each AD is captured as an ADR, and the collection of all ADRs for a project forms the ADL — the `architecture-decision-log/` directory in this repository. This framework gives you the tooling and governance process to build an ADL that is schema-validated, Git-governed, AI-assisted, and auditable.

## What This Provides

- **JSON Schema** (Draft 2020-12) defining the complete ADR meta-model — every field, enum, and constraint
- **GitOps-based governance process** — ADR status transitions happen through Git commits and pull requests, not manual coordination
- **Validation tooling** — a Python validator that checks schema compliance, referential integrity, and semantic consistency on every PR
- **Pre-built CI/CD pipelines** for GitHub Actions, Azure DevOps, GCP Cloud Build, AWS CodeBuild, and GitLab CI — ready to copy into your repo and enforce as a merge gate
- **Approval identity enforcement** — CI verifies that the people listed in `approvals[]` have actually approved the pull request, creating an auditable link between ADR approvals and Git platform approvals
- **Governance rules** — configurable single-ADR-per-PR enforcement, substantive vs. maintenance change classification, and admin overrides — all defined in a platform-agnostic `.adr-governance/config.yaml`
- **LLM-ready setup prompts** — copy-paste prompts for AI assistants to set up CI for your platform in minutes
- **Agent Skill** ([agentskills.io](https://agentskills.io) spec) for AI-assisted ADR authoring and review — works with Google Antigravity, Claude Code, VS Code Copilot, and any conforming agent. The skill knows the schema and the governance process, and will guide you through every field interactively
- **Decision enforcement** — the ADL can serve as a single source of truth for Spec-Driven Development (SDD): AI coding agents can search the bundled ADL to align code with architectural decisions, and CI pipelines can validate compliance before merge
- **Repomix bundling** — the entire ADL is concatenated into a single Markdown file that agents can search with standard tools, enabling cross-repository decision enforcement
- **Example ADRs** from a fictional IAM department (NovaTrust Financial Services) in [`examples-reference/`](examples-reference/) — real-world contended decisions with sizable pros and cons on each side, not strawman examples. Kept as a reference for quality and style; not real decisions

## Philosophy

Every ADR is **self-contained**. All context, Architecturally Significant Requirements (ASRs), alternatives, consequences, and audit trails are embedded directly in the YAML file. There are no foreign-key dependencies between ADRs — the only explicit link is the `lifecycle.supersedes` / `superseded_by` chain for replacements. An ADR can *mention* other ADR IDs in prose, but it must be fully understandable on its own.

The ADL is an **append-only decision log**. ADRs are never deleted — they transition through a governed lifecycle. Rejected and superseded ADRs remain as historical records, preserving the decision-making trail for auditors, new team members, and your future self.

## ADR Lifecycle

Every ADR follows a governed state machine. All transitions happen through pull requests.

```mermaid
stateDiagram-v2
    [*] --> draft

    draft --> proposed : Open PR

    proposed --> proposed : Rework (changes requested)
    proposed --> accepted : Approved → PR merged
    proposed --> rejected : Rejected → PR merged
    proposed --> deferred : Postponed → PR closed

    deferred --> proposed : Reopened

    accepted --> superseded : Replaced by new ADR
    accepted --> deprecated : No longer recommended

    rejected --> [*]
    deferred --> [*]
    superseded --> [*]
    deprecated --> [*]
```

> **Why are rejected ADRs merged?** They are part of the ADL — they document *why* an option was evaluated and not pursued. Closing the PR without merging would lose this history from `main`.

See [`docs/adr-process.md`](docs/adr-process.md) for the full normative governance process, including review checklists, the Architectural Significance Test, branch protection rules, and CODEOWNERS configuration.

## Quick Start — Adopting for Your Organization

### 1. Create your ADR repository

Create a new repository in your organization and clone this framework into it:

```bash
# Create a new repo in your org (GitHub example)
gh repo create your-org/architecture-decisions --private --clone

# Pull the framework into it
cd architecture-decisions
git remote add upstream https://github.com/ivanstambuk/adr-governance.git
git pull upstream main
git remote remove upstream
git push origin main
```

Or fork the repository directly from GitHub and rename it.

### 2. Review examples *(optional cleanup)*

The [`examples-reference/`](examples-reference/) directory contains 8 fictional ADRs from "NovaTrust Financial Services" — they demonstrate the meta-model at production quality. **These are not real decisions.** You can:

- **Keep them** as a reference for your team (recommended initially)
- **Delete them** once your team is comfortable with the format:
  ```bash
  rm -rf examples-reference/
  git add -A && git commit -m "chore: remove reference examples"
  ```

### 3. Customize ADR-0000

[`architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml`](architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml) is the **meta-ADR** — it documents the decision to adopt this governance framework. Update it for your organization:

- Replace the `authors`, `decision_owner`, `reviewers`, and `approvals` names and identities
- Update `adr.project` to your project or organisation name
- Update timestamps and audit trail entries
- Adjust the `context.summary` if your adoption rationale differs

### 4. Set up CI

Copy the pipeline file for your platform to the repository root:

| Platform | Copy from | Copy to |
|----------|-----------|---------|
| **GitHub Actions** | Already at `.github/workflows/validate-adr.yml` | *(nothing to do)* |
| Azure DevOps | `ci/azure-devops/azure-pipelines.yml` | `azure-pipelines.yml` |
| GCP Cloud Build | `ci/gcp-cloud-build/cloudbuild.yaml` | `cloudbuild.yaml` |
| AWS CodeBuild | `ci/aws-codebuild/buildspec.yml` | `buildspec.yml` |
| GitLab CI | `ci/gitlab-ci/.gitlab-ci.yml` | `.gitlab-ci.yml` |

Then configure branch protection to make the CI check a **required merge gate** — see **[`docs/ci-setup.md`](docs/ci-setup.md)** for platform-specific instructions and LLM-ready setup prompts.

### 5. Enable the pre-commit hook

```bash
git config core.hooksPath .githooks
```

This activates automatic Markdown rendering — every commit that touches `architecture-decision-log/*.yaml` will regenerate the human-friendly files in `rendered/` and the decision log index. Both the YAML source and its Markdown rendering are committed together, so reviewers approve both in the same PR.

### 6. Configure CODEOWNERS *(optional but recommended)*

```bash
cp CODEOWNERS.example .github/CODEOWNERS
```

Edit `.github/CODEOWNERS` to replace the placeholder team handles (`@org/architecture-team`, etc.) with your real GitHub teams. This ensures ADRs and schema changes automatically request review from the right people.

### 7. Copy the Agent Skill to your code repositories *(optional)*

The `.skills/adr-author/` directory is a portable AI skill. Copy it to any repository where developers will be authoring ADRs — agents like Antigravity, Claude Code, and Copilot will pick it up automatically and guide ADR creation through interactive questioning.

### 8. Create your first real ADR

Use an AI assistant with the `adr-author` skill — it will guide you through every field via Socratic dialogue:

```
"I need to create a new ADR for [your decision]. Guide me through it."
```

Or copy the template manually:

```bash
cp .skills/adr-author/assets/adr-template.yaml \
   architecture-decision-log/ADR-0001-your-decision-title.yaml
```

### 9. Validate and submit

```bash
# Install dependencies
pip install jsonschema pyyaml yamllint

# Validate schema + semantic consistency
python3 scripts/validate-adr.py architecture-decision-log/ADR-0001-your-decision-title.yaml

# Pre-review quality gate (pipe to your LLM for Socratic feedback)
python3 scripts/review-adr.py architecture-decision-log/ADR-0001-your-decision-title.yaml

# Open a PR — CI validates automatically
git checkout -b adr/0001-your-decision-title
git add architecture-decision-log/ADR-0001-your-decision-title.yaml
git commit -m "feat(adr): ADR-0001 your decision title"
git push origin adr/0001-your-decision-title
```

The CI pipeline validates schema compliance and lints the YAML. Reviewers are auto-assigned via CODEOWNERS. The PR becomes the decision forum — all discussion, feedback, and approval happens asynchronously in the PR thread.

## ADR Meta-Model

Each ADR YAML file contains these sections:

| Section | Required | Description |
|---------|:--------:|-------------|
| `adr` | ✅ | ID, title, status, summary, timestamps, project, tags, priority, decision type, schema version |
| `authors` | ✅ | Who drafted the ADR |
| `decision_owner` | ✅ | Single accountable person |
| `context` | ✅ | Problem summary (**Markdown**), business/technical drivers, constraints |
| `alternatives` | ✅ | ≥2 alternatives with summary (**Markdown**), pros, cons, cost, risk, rejection rationale |
| `decision` | ✅ | Chosen alternative, rationale (**Markdown**), tradeoffs (**Markdown**), date, confidence |
| `consequences` | ✅ | Positive and negative outcomes |
| `confirmation` | ✅ | How the decision's implementation will be verified; artifact IDs (optional, backfilled later) |
| `reviewers` | | People who reviewed |
| `approvals` | | Formal approvals with timestamps and platform identities for CI verification |
| `requirements` | | Embedded functional and non-functional requirements (ASRs) |
| `dependencies` | | Internal and external dependencies |
| `references` | | External references, standards, evidence |
| `lifecycle` | | Review cadence, supersession chain, archival |
| `audit_trail` | | Immutable append-only event log |

> **Markdown-native fields** support full Markdown including embedded Mermaid diagrams via code fences. Use YAML literal block scalars (`|`) for multiline content.

## CI/CD Setup

Automated validation is the enforcement mechanism that makes the governance process real. Without it, the schema is a suggestion; with it, the schema is a contract.

**GitHub Actions** is preconfigured — the workflow at `.github/workflows/validate-adr.yml` runs on every PR. You just need to [enable branch protection](docs/ci-setup.md#github-actions) to make it a merge gate.

**Other platforms** have ready-to-use pipeline files in the `ci/` directory:

| Platform | Pipeline file | Copy to |
|----------|---------------|---------|
| Azure DevOps | [`ci/azure-devops/azure-pipelines.yml`](ci/azure-devops/azure-pipelines.yml) | `azure-pipelines.yml` (repo root) |
| GCP Cloud Build | [`ci/gcp-cloud-build/cloudbuild.yaml`](ci/gcp-cloud-build/cloudbuild.yaml) | `cloudbuild.yaml` (repo root) |
| AWS CodeBuild | [`ci/aws-codebuild/buildspec.yml`](ci/aws-codebuild/buildspec.yml) | `buildspec.yml` (repo root) |
| GitLab CI | [`ci/gitlab-ci/.gitlab-ci.yml`](ci/gitlab-ci/.gitlab-ci.yml) | `.gitlab-ci.yml` (repo root) |

**Step-by-step setup instructions**, platform-specific enforcement configuration, troubleshooting, and **LLM-ready prompts** (copy-paste into any AI assistant to have it set up CI for you) are in **[`docs/ci-setup.md`](docs/ci-setup.md)**.

## AI-Assisted Authoring & Pre-Review

ADRs are not meant to be filled in manually like a form. They are authored through **Socratic dialogue with an AI assistant** — the AI asks probing questions, challenges weak rationale, surfaces missing edge cases, and iteratively refines the document until it is clear, complete, and internally consistent.

This is a fundamental shift from traditional architecture governance: instead of the proposer writing a draft in isolation and then scheduling a meeting to "walk through" it (where reviewers discover ambiguities in real time and the meeting devolves into clarification rather than decision-making), the AI assistant resolves those ambiguities *before the first human reviewer ever sees the document*.

### Agent Skill

The `.skills/adr-author/` directory follows the [agentskills.io specification](https://agentskills.io/specification) and works with:

- **Google Antigravity** (VS Code)
- **Claude Code** (terminal)
- **VS Code Copilot** (with skills support)
- Any agent implementing the Agent Skills standard

The skill guides AI assistants to author ADRs through interactive questioning — probing for Architecturally Significant Requirements (ASRs), demanding balanced alternatives (not strawmen), checking that constraints are testable, and verifying that the rationale actually connects to the stated drivers. It understands the full meta-model and governance lifecycle.

### Web Chat (No Skill Required)

Don't have access to a coding agent? The Repomix bundle (`adr-governance-bundle.md`) includes **embedded AI instructions** that replicate the full skill — upload the single file to any web-based AI chat:

- **ChatGPT** (with Code Interpreter for large file search)
- **Claude.ai** (200K–1M token context)
- **Google Gemini** (1M+ token context)
- **Microsoft Copilot** (web)

The AI will be able to author new ADRs through Socratic dialogue, query the decision log with citations, review ADRs for completeness, summarize decisions for stakeholders, and validate YAML against the schema — all from a single uploaded file.

See **[`docs/web-chat-quickstart.md`](docs/web-chat-quickstart.md)** for platform-specific starter prompts and tips.


### Pre-Review Quality Gate

Before submitting an ADR for human review, run it through an AI semantic review using `scripts/review-adr.py`:

```bash
# Generate a Socratic review prompt (pipe to your LLM)
python3 scripts/review-adr.py architecture-decision-log/ADR-0009.yaml

# Include cross-reference context from existing decisions
python3 scripts/review-adr.py architecture-decision-log/ADR-0009.yaml \
  --context-from architecture-decision-log/

# Pipe directly to an LLM
python3 scripts/review-adr.py architecture-decision-log/ADR-0009.yaml | \
  llm -m gpt-4o
```

The generated prompt instructs the LLM to perform a structured review covering:
- **Semantic clarity** — are there ambiguous terms or vague claims?
- **Completeness** — are alternatives balanced, constraints testable, consequences honest?
- **Logical consistency** — does the rationale align with the pros/cons?
- **Assumption risks** — what happens if the assumptions are wrong?
- **Missing perspectives** — are there unconsidered stakeholders or alternatives?
- **Cross-reference consistency** — does this decision conflict with existing ADRs?

The AI outputs a verdict (**READY FOR REVIEW**, **NEEDS REWORK**, or **MAJOR GAPS**), a list of issues with severity, and open questions for the proposer. The proposer addresses the feedback, re-runs the check, and iterates until the ADR passes. *Then* they open the PR.

> **The result:** Human reviewers receive ADRs that are already semantically coherent and complete. Review meetings become strategic discussions about the *decision* — not debugging sessions about what the proposer meant.

## Stakeholder Summaries

Not every stakeholder needs the full ADR. After a decision is made (or after an architecture review meeting), use `scripts/summarize-adr.py` to produce concise summaries for communication:

```bash
# Email-length summary (~10–15 lines: decision, rationale, alternatives, tradeoffs, impact)
python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml

# Ultra-short chat summary (3–5 lines for Slack/Teams)
python3 scripts/summarize-adr.py --format chat architecture-decision-log/ADR-0001.yaml

# Meeting recap — digest of multiple ADRs
python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml \
    architecture-decision-log/ADR-0002.yaml

# Save to file
python3 scripts/summarize-adr.py -o meeting-recap.md architecture-decision-log/
```

Each summary links back to the full YAML source. For a richer, rendered view, point stakeholders to the auto-generated Markdown in [`rendered/`](rendered/).

## ADL as Source of Truth

The Architecture Decision Log isn't just documentation — it's a **machine-readable specification** that AI agents and CI pipelines can enforce against your codebase. This closes the gap between *deciding* and *doing*.

### Spec-Driven Development (SDD)

AI coding agents (Copilot, Claude Code, Antigravity, Cursor, etc.) can use the bundled ADL as a **single source of truth** during code generation. When the ADL says "use DPoP for sender-constrained tokens" (ADR-0001), the agent can search the bundled decision log, find the decision with its full rationale and constraints, and generate code that aligns with it — without the developer having to explain the architectural context in every prompt.

The workflow:

1. **Bundle the ADL** into a single file:
   ```bash
   ./scripts/bundle.sh
   ```
   This generates `adr-governance-bundle.md` — the entire governance framework, schema, and all accepted decisions in one searchable file.

2. **Point your agent to it.** Paste the bundle into an LLM context window, add it to your agent's project knowledge, or reference it as a file. The agent can then use standard text search (grep, semantic search, `Ctrl+F`) to find relevant decisions.

3. **Generate code that complies.** When the agent encounters an architectural question — which token format to use, which signing algorithm, which authentication pattern — it searches the ADL instead of guessing or asking you.

> **Cross-repository enforcement:** The ADL repo and the code repo don't need to be the same. Point your agent at the ADL bundle from *any* repository. The decisions are self-contained — each ADR includes the full context, rationale, and constraints needed to understand and apply it.

### Semantic Guardrails in CI

The ADL can also serve as a **pre-merge guardrail** in your *code* repositories — not just the ADR repository itself. Before a PR is merged, a CI step can validate that the code changes are consistent with accepted architectural decisions.

This works at two levels:

**1. Local enforcement (during development):**
Coding agents that have the ADL in context will naturally align with it. When you ask "implement the token endpoint," an agent with ADR-0001 in context will use DPoP, not mTLS — because the decision and its rationale are right there in the searchable bundle.

**2. CI pipeline enforcement (pre-merge):**
Use `scripts/extract-decisions.py` to extract active decisions and generate an LLM compliance prompt. Add a step in your code repository's CI pipeline:

```yaml
# Example: GitHub Actions step in your CODE repo (not this repo)
- name: Check ADR compliance
  run: |
    # Fetch the extraction script and ADR files from the governance repo
    git clone --depth 1 https://github.com/your-org/adr-governance.git /tmp/adl
    pip install pyyaml

    # Generate a compliance prompt with the code diff
    python3 /tmp/adl/scripts/extract-decisions.py \
      --compliance-prompt \
      --diff <(git diff origin/main...HEAD) \
      /tmp/adl/architecture-decision-log/ \
      > /tmp/compliance-prompt.md

    # Pipe to your LLM of choice for automated review
    # (replace with your preferred LLM CLI — openai, claude, gemini, llm, etc.)
    cat /tmp/compliance-prompt.md | your-llm-cli "Review this for compliance"
```

The key insight: **the ADL is structured YAML that any tool can parse**. The `extract-decisions.py` script handles the parsing and prompt generation — you just plug in your LLM provider.

### Decision Extraction

The `scripts/extract-decisions.py` script is the bridge between the ADL and downstream enforcement tooling:

```bash
# Markdown summary of all accepted decisions (for agent context)
python3 scripts/extract-decisions.py architecture-decision-log/

# JSON output for programmatic consumption
python3 scripts/extract-decisions.py --format json architecture-decision-log/

# Filter by tags (e.g., only OAuth-related decisions)
python3 scripts/extract-decisions.py --tags oauth,security architecture-decision-log/

# Generate an LLM compliance-check prompt with a code diff
python3 scripts/extract-decisions.py --compliance-prompt \
  --diff <(git diff main) architecture-decision-log/

# Save to a file for agent context injection
python3 scripts/extract-decisions.py -o active-decisions.md architecture-decision-log/
```

### What This Enables

| Scenario | Without ADL enforcement | With ADL enforcement |
|----------|------------------------|---------------------|
| New developer joins | Reads (or doesn't read) wiki docs | Agent has full ADL context; generates compliant code from day one |
| PR introduces mTLS | Merges — nobody notices the ADR says DPoP | CI flags the drift; reviewer is alerted |
| Architect proposes supersession | Searches Slack history for context | Searches the ADL bundle; full decision chain is traceable |
| Annual audit | Scramble to reconstruct decision history | ADL is the audit trail; every decision is timestamped, attributed, and version-controlled |
| LLM generates code | Guesses at patterns based on training data | Searches the ADL and follows your organization's actual decisions |

### Repomix Bundle

To create the single-file bundle:

```bash
./scripts/bundle.sh
```

This generates `adr-governance-bundle.md` — the entire ADR governance framework in one file. The bundle includes the schema, process documentation, glossary, skill instructions, YAML template, all ADRs in `architecture-decision-log/`, example ADRs from `examples-reference/`, validation scripts, and **embedded AI instructions** that enable web-based AI chats to emulate the full authoring skill.

**Usage options:**
- **Upload** to any AI web chat (ChatGPT, Claude, Gemini, Copilot) — see [`docs/web-chat-quickstart.md`](docs/web-chat-quickstart.md)
- **Paste** into any LLM context window for instant AKM context
- **Add** to your coding agent's project knowledge base
- **Fetch** from CI pipelines in other repositories (as shown above)
- **Commit** to other repositories as a versioned reference artifact

## Rendered Markdown (Auto-Generated)

Every ADR YAML file has a corresponding **human-friendly Markdown rendering** in [`rendered/`](rendered/). These are designed for browsing on GitHub, Azure DevOps, Azure Repos, and other platforms that render Markdown natively.

- **[`rendered/architecture-decision-log.md`](rendered/architecture-decision-log.md)** — the decision log index with clickable links, status, and decision dates
- **`rendered/ADR-NNNN-*.md`** — individual ADR renderings with a provenance disclaimer

> **⚠️ Do not edit files in `rendered/` directly.** They are auto-generated from the YAML source. Each rendered file includes a `[!CAUTION]` banner and HTML comment pointing to the source YAML.

### Pre-commit hook (automatic rendering)

A Git pre-commit hook automatically re-renders all ADR files and regenerates the index whenever you commit changes to `architecture-decision-log/`. This means both the YAML source and its Markdown rendering are part of the same commit and PR — **reviewers approve both together**.

**One-time setup** (per clone):

```bash
git config core.hooksPath .githooks
```

After this, any commit that touches `architecture-decision-log/*.yaml` will automatically:
1. Render all ADR YAML files to `rendered/*.md` with a provenance disclaimer
2. Regenerate `rendered/architecture-decision-log.md` (the decision log index)
3. Stage the rendered files alongside the YAML changes

### Manual rendering

```bash
# Single file to stdout (no disclaimer — useful for previewing)
python3 scripts/render-adr.py architecture-decision-log/ADR-0001-*.yaml

# Render to rendered/ with disclaimer + index
python3 scripts/render-adr.py --output-dir rendered/ --generate-index architecture-decision-log/
```

## Example ADRs

The [`examples-reference/`](examples-reference/) directory contains interconnected ADRs from a **fictional** IAM department at NovaTrust Financial Services. These are **not real decisions** — they demonstrate the meta-model at production quality. Use them as a reference for style, depth, and interconnection:

| ID | Title | Status |
|----|-------|--------|
| ADR-0001 | [Use DPoP over mTLS for Sender-Constrained Tokens](examples-reference/rendered/ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.md) | accepted |
| ADR-0002 | [Use Reference Tokens over JWTs for Gateway Introspection](examples-reference/rendered/ADR-0002-reference-tokens-over-jwt-for-gateway-introspection.md) | accepted |
| ADR-0003 | [Use Pairwise Subject Identifiers for OIDC Relying Parties](examples-reference/rendered/ADR-0003-pairwise-subject-identifiers-for-oidc-relying-parties.md) | accepted |
| ADR-0004 | [Use Ed25519 over RSA-2048 for JWT Signing Keys](examples-reference/rendered/ADR-0004-ed25519-over-rsa-for-jwt-signing.md) | accepted |
| ADR-0005 | [Use BFF Token Mediator for SPA Token Acquisition](examples-reference/rendered/ADR-0005-bff-token-mediator-for-spa-token-acquisition.md) | accepted |
| ADR-0006 | [Use Session Enrichment for Step-Up Authentication Proof](examples-reference/rendered/ADR-0006-session-enrichment-for-step-up-authentication.md) | accepted |
| ADR-0007 | [Reject Centralized HashiCorp Vault for API Runtime Secrets](examples-reference/rendered/ADR-0007-centralized-secret-store-for-api-keys.md) | **rejected** |
| ADR-0008 | [Defer OpenID Federation for Automated Trust Establishment](examples-reference/rendered/ADR-0008-defer-openid-federation-for-trust-establishment.md) | **deferred** |

See the [rendered example index](examples-reference/rendered/architecture-decision-log.md) for a full overview, or [`examples-reference/README.md`](examples-reference/README.md) for details on each example.

Additionally, [`architecture-decision-log/ADR-0000`](architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml) is a meta-ADR documenting the AD to adopt this governance process itself.

> **Bootstrap exception:** ADR-0000 was self-approved by the initial author as the bootstrapping meta-decision. The "no self-approval" rule (§3.4) applies to all subsequent ADRs.

## License

MIT
````




# Instruction
# ADR Governance — Instructions for AI Assistant

You have received the complete **adr-governance** framework — a schema-governed, AI-native Architecture Decision Record (ADR) system. This file contains everything: the JSON Schema, governance process, glossary, validation logic, example ADRs, a YAML template, and the AI skill specification.

**You are an ADR authoring, reviewing, querying, and summarizing assistant.** Follow the instructions below to help the user.

---

## How to navigate this file

This is a large bundle. **Do not attempt to read it all at once.** Use search/grep to locate sections on demand:

- **Schema** → search for `adr.schema.json` — the JSON Schema defining all valid ADR fields, enums, and constraints
- **Skill instructions** → search for `# ADR Author Skill` — the full step-by-step authoring workflow
- **Template** → search for `adr-template.yaml` — the blank YAML skeleton for new ADRs
- **Process** → search for `adr-process.md` — the governance lifecycle, state transitions, and review process
- **Glossary** → search for `glossary.md` — all enum values, term definitions, and abbreviations
- **Schema reference** → search for `SCHEMA_REFERENCE.md` — human-readable schema documentation
- **Existing ADRs** → search for `ADR-0000`, `ADR-0001`, ..., `ADR-0008` — real examples showing style and depth
- **Validation script** → search for `validate-adr.py` — the validation logic (schema + semantic checks)
- **Review script** → search for `review-adr.py` — the pre-review quality gate logic
- **README** → search for `# adr-governance` — project overview and philosophy

> **Tip for platforms with Code Interpreter / code execution:** Open the file programmatically and use Python string search or regex to extract specific sections. You do not need to load everything into your context window at once.

---

## Capabilities

You support these operations:

### 1. Create a new ADR (Socratic authoring)

Walk the user through creating a complete, schema-valid ADR using Socratic dialogue. **Do not ask for all information at once** — interview the user step by step, probing for gaps and challenging weak reasoning.

**Workflow:**

1. **Ask what decision needs to be made.** Get a clear, concise title (10–200 chars).
2. **Determine the next ADR ID.** Search this file for existing ADR IDs in `architecture-decision-log/` and `examples-reference/` to find the highest number, then increment. The format is `ADR-NNNN` (zero-padded, 4 digits).
3. **Classify the decision:**
   - Decision type: `technology` | `process` | `organizational` | `vendor` | `security` | `compliance`
   - Priority: `low` | `medium` | `high` | `critical`
4. **Gather context:**
   - What problem are we solving? (This becomes `context.summary` — a Markdown narrative)
   - What are the business drivers? (business outcomes, compliance needs, cost pressures)
   - What are the technical drivers? (scalability, performance, integration, security)
   - What are the constraints? (budget, timeline, regulatory, existing contracts, team skills)
   - What assumptions are we making?
5. **Elicit alternatives** (minimum 2, aim for 3):
   - For each: name, summary (Markdown), pros, cons, estimated cost (`low`|`medium`|`high`), risk level (`low`|`medium`|`high`|`critical`)
   - **Challenge strawman alternatives.** If one alternative has only cons and no pros, push back — every real option has *some* advantages.
   - **Challenge lopsided comparisons.** If the "obvious" choice has 5 pros and 0 cons, probe for hidden costs.
6. **Determine the recommendation:**
   - Which alternative and why? (This becomes `decision.rationale` — Markdown, can include diagrams)
   - What are we explicitly giving up? (This becomes `decision.tradeoffs` — Markdown)
   - Confidence level: `low` | `medium` | `high`
   - For each non-chosen alternative, why was it rejected? (`rejection_rationale`)
7. **Assess consequences:**
   - Positive outcomes (what gets better)
   - Negative outcomes (what gets worse or becomes a new risk)
8. **Define confirmation:**
   - How will we verify this decision was implemented correctly? (`confirmation.description`)
   - Are there artifact IDs to track? (Jira tickets, PR URLs, test suites — can be added later)
9. **Capture metadata:**
   - Authors (name, role, email)
   - Decision owner (single accountable person)
   - Project name
   - Tags for categorization
   - Summary (`adr.summary`): 2–4 sentence elevator pitch, max 500 chars — distinct from `context.summary`
10. **Generate the complete ADR YAML.**
    - Search for `adr-template.yaml` in this file to get the skeleton
    - Fill in all required sections
    - Set status to `draft` or `proposed`
    - Add an initial `audit_trail` entry: `event: "created"`
    - Use YAML literal block scalars (`|`) for Markdown fields
    - Use ISO 8601 for all timestamps
11. **Self-validate the output:**
    - Search for `adr.schema.json` and verify all `required` fields are present
    - Verify `chosen_alternative` matches an entry in `alternatives[].name`
    - Verify at least 2 alternatives exist
    - Verify `adr.id` matches `^ADR-[0-9]{4}(-[a-z0-9]+)*$`
    - Verify all enum values are valid (search for the glossary section)

**Socratic probing guidelines:**
- If the rationale says "it's the industry standard" → ask *why* the standard exists and whether the team's constraints match
- If a constraint says "must use X" → ask *whose* requirement this is and whether it's truly non-negotiable
- If there's no mention of cost → ask about licensing, operational overhead, migration effort
- If there's no mention of risk → ask what happens if the decision is wrong
- If confidence is `high` but only one alternative was seriously evaluated → challenge the confidence level

### 2. Query the Architecture Decision Log (ADL)

When the user asks a question about architectural decisions, **search the ADR files in this bundle** and provide a well-sourced answer.

**How to search:**
- Search for keywords in the file content (e.g., "DPoP", "mTLS", "token", "signing", "session")
- Look at `adr.title`, `adr.status`, `context.summary`, `decision.chosen_alternative`, and `decision.rationale` fields
- Match by tags in `adr.tags`

**How to respond:**
- **Always cite** the specific ADR IDs: "According to **ADR-0001** (*Use DPoP over mTLS for Sender-Constrained Tokens*)..."
- **Include the status**: "This decision is currently **accepted**."
- **Include the rationale summary**: briefly explain *why* the decision was made
- **Include caveats**: if the ADR is superseded, deprecated, or rejected, say so explicitly
- **Cross-reference**: if multiple ADRs are relevant, mention all of them and explain any interactions

**Example queries the user might ask:**
- "What did we decide about token binding?" → Search for DPoP, mTLS, sender-constrained, token binding
- "Why didn't we go with HashiCorp Vault?" → Find the rejected ADR, cite the rationale
- "What decisions affect our API gateway?" → Search for gateway, introspection, reference tokens
- "Are there any deferred decisions?" → Search for `status: "deferred"`
- "Show me all security-related decisions" → Filter by tags or decision_type

### 3. Review an existing ADR

When the user provides or asks you to review an ADR, perform a structured review covering:

1. **Completeness** — Are all required sections present? (Search for schema `required` fields)
2. **Alternative quality** — At least 2 alternatives with substantive, balanced pros/cons?
3. **Rationale strength** — Does the rationale clearly connect to the stated drivers and constraints?
4. **Risk coverage** — Are major risks identified with realistic mitigations?
5. **Compliance** — If the decision touches data, access, or infrastructure, are regulatory implications addressed?
6. **Consistency** — Does `chosen_alternative` match `alternatives[].name`? Is `lifecycle.supersedes`/`superseded_by` symmetric?
7. **Audit trail** — Is the trail consistent with the current status?
8. **Rejection rationale** — For each non-chosen alternative, is `rejection_rationale` populated?
9. **Diagram quality** — Are Mermaid diagrams used where a visual would clarify architecture or flow?

**Output a structured verdict:** `READY FOR REVIEW`, `NEEDS REWORK`, or `MAJOR GAPS` — with a numbered list of issues, each with severity (critical/major/minor) and a specific suggestion.

### 4. Summarize ADRs for stakeholders

When the user asks for a summary:

**Email format** (default): ~10–15 lines covering:
- What was decided (title + chosen alternative)
- Why (1–2 sentence rationale)
- What alternatives were considered (names only)
- Key tradeoffs acknowledged
- Positive and negative consequences
- Next steps / confirmation criteria

**Chat format** (for Slack/Teams): 3–5 lines:
- 🏗️ **[Title]** — [status]
- **Decision:** [chosen alternative in one sentence]
- **Why:** [one-sentence rationale]
- **Impact:** [one positive, one negative consequence]

### 5. Supersede, deprecate, or archive an ADR

Guide the user through the lifecycle transition:

**Supersession:**
- Create a new ADR (follow the authoring workflow above)
- In the new ADR: set `lifecycle.supersedes: "ADR-NNNN"`
- In the old ADR: set `adr.status: "superseded"`, `lifecycle.superseded_by: "ADR-MMMM"`, add audit trail entry

**Deprecation:**
- Set `adr.status: "deprecated"`, add audit trail entry with reason

**Archival:**
- Set `lifecycle.archival.archived_at` and `lifecycle.archival.archive_reason`

### 6. Explain the governance process

When the user asks about the ADR process, search for `adr-process.md` in this file and explain:
- The status lifecycle (draft → proposed → accepted/rejected/deferred, etc.)
- How pull requests map to state transitions
- Review checklists and the Architectural Significance Test
- Branch protection and CODEOWNERS configuration
- The single-ADR-per-PR governance rule
- Substantive vs. maintenance change classification

### 7. Validate an ADR

When the user provides ADR YAML content to validate:

1. Check against the JSON Schema (search for `adr.schema.json`):
   - All required top-level sections present
   - All required fields within each section present
   - All enum values valid
   - ID format matches `^ADR-[0-9]{4}(-[a-z0-9]+)*$`
   - At least 2 alternatives
2. Check semantic consistency:
   - `decision.chosen_alternative` matches an `alternatives[].name`
   - If status is `accepted`, an `approved` event should exist in `audit_trail`
   - If `lifecycle.supersedes` is set, the referenced ADR should have `superseded_by` pointing back
   - Temporal ordering: `created_at` ≤ `last_modified`, `decision_date` is reasonable
3. Check quality signals:
   - Is `adr.summary` populated? (Missing = warning)
   - Is confidence `high` with fewer than 3 alternatives? (Warning)
   - Are `rejection_rationale` fields populated for non-chosen alternatives?

Report issues as: `ERROR` (schema violation), `WARNING` (semantic concern), or `INFO` (quality suggestion).

---

## Key schema details (quick reference)

**Status values:** `draft` | `proposed` | `accepted` | `superseded` | `deprecated` | `rejected` | `deferred`

**Decision types:** `technology` | `process` | `organizational` | `vendor` | `security` | `compliance`

**Priority levels:** `low` | `medium` | `high` | `critical`

**Confidence levels:** `low` | `medium` | `high`

**Cost / Risk scales:** `low` | `medium` | `high` (risk also allows `critical`)

**ID format:** `ADR-NNNN` or `ADR-NNNN-slug` (e.g., `ADR-0001`, `ADR-0001-dpop-over-mtls`)

**Audit trail events:** `created` | `updated` | `reviewed` | `approved` | `rejected` | `deferred` | `superseded` | `deprecated` | `archived`

**Markdown-native fields** (support full Markdown + Mermaid diagrams via code fences):
- `context.summary`
- `alternatives[].summary`
- `decision.rationale`
- `decision.tradeoffs`
- `confirmation.description`

Use YAML literal block scalars (`|`) for multiline Markdown content.

---

## After generating ADR YAML

Once the user has a complete ADR YAML, advise them to:

1. **Save the file** as `architecture-decision-log/ADR-NNNN-short-kebab-case-title.yaml`
2. **Run validation:**
   ```bash
   pip install jsonschema pyyaml yamllint  # one-time setup
   python3 scripts/validate-adr.py architecture-decision-log/ADR-NNNN-title.yaml
   ```
3. **Run the pre-review quality gate:**
   ```bash
   python3 scripts/review-adr.py architecture-decision-log/ADR-NNNN-title.yaml
   ```
4. **Open a pull request** on a branch named `adr/NNNN-short-title`
5. **CI will validate automatically** — the PR becomes the decision forum

---

## Important: do not hallucinate schema fields

If you are unsure whether a field exists or what values are allowed, **search for `adr.schema.json` in this file** and verify. Do not invent fields, enum values, or structural patterns. The schema is the single source of truth.
