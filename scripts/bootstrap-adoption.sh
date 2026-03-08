#!/usr/bin/env bash
# scripts/bootstrap-adoption.sh — One-shot adoption bootstrap
#
# Usage:
#   bash scripts/bootstrap-adoption.sh \
#     --platform github|azure|gcp|aws|gitlab \
#     --org "My Organisation" \
#     --name "Jane Doe" \
#     --email "jane.doe@contoso.com" \
#     --identity "@janedoe"              # or jane.doe@contoso.com for Azure
#     --team "@myorg/architects"         # or Azure group name
#     [--remove-examples]                # delete examples-reference/
#
# If ANY required flag is omitted the script prints usage and exits 1.
#
# What it does (idempotent — safe to re-run):
#   1. Updates ADR-0000: authors, decision_owner, approvals, adr.project,
#      timestamps, audit_trail, constraints, dependencies, confirmation
#   2. Updates .adr-governance/config.yaml admin identity
#   3. Copies the platform CI template to the repository root
#   4. Optionally removes examples-reference/
#   5. Renders architecture-decision-log/
#   6. Regenerates llms-full.txt
#   7. Sets git hooks path
#   8. Runs validation + generated-artifacts freshness check
set -euo pipefail

# ── Colour helpers ──────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${CYAN}ℹ${NC}  $*"; }
ok()    { echo -e "${GREEN}✅${NC} $*"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $*"; }
fail()  { echo -e "${RED}❌${NC} $*" >&2; exit 1; }

# ── Parse arguments ─────────────────────────────────────────────────────
PLATFORM="" ORG="" NAME="" EMAIL="" IDENTITY="" TEAM="" REMOVE_EXAMPLES=false

usage() {
  cat <<'EOF'
Usage: bash scripts/bootstrap-adoption.sh \
  --platform  github|azure|gcp|aws|gitlab \
  --org       "Organisation Name" \
  --name      "Your Full Name" \
  --email     "you@example.com" \
  --identity  "@ghuser | user@domain.com (Azure)" \
  --team      "@org/team | Azure group name" \
  [--remove-examples]
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform)         PLATFORM="$2"; shift 2 ;;
    --org)              ORG="$2";      shift 2 ;;
    --name)             NAME="$2";     shift 2 ;;
    --email)            EMAIL="$2";    shift 2 ;;
    --identity)         IDENTITY="$2"; shift 2 ;;
    --team)             TEAM="$2";     shift 2 ;;
    --remove-examples)  REMOVE_EXAMPLES=true; shift ;;
    -h|--help)          usage ;;
    *)                  fail "Unknown option: $1" ;;
  esac
done

[[ -z "$PLATFORM" || -z "$ORG" || -z "$NAME" || -z "$EMAIL" || -z "$IDENTITY" || -z "$TEAM" ]] && usage

# Normalise platform names
case "$PLATFORM" in
  github|gh)    PLATFORM=github ;;
  azure|azdo)   PLATFORM=azure ;;
  gcp|gcb)      PLATFORM=gcp ;;
  aws|cb)       PLATFORM=aws ;;
  gitlab|gl)    PLATFORM=gitlab ;;
  *)            fail "Unknown platform: $PLATFORM (expected github|azure|gcp|aws|gitlab)" ;;
esac

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# ── Determine today's ISO timestamp ─────────────────────────────────────
NOW="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
TODAY="$(date -u '+%Y-%m-%d')"

# ── 1. Update ADR-0000 ──────────────────────────────────────────────────
info "Updating ADR-0000 with your details..."
ADR0="architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml"

if [[ ! -f "$ADR0" ]]; then
  fail "ADR-0000 not found at $ADR0 — are you in the repo root?"
fi

# Use python3 for reliable YAML manipulation
python3 - "$ADR0" "$NAME" "$EMAIL" "$IDENTITY" "$ORG" "$NOW" "$TODAY" "$PLATFORM" <<'PYEOF'
import sys, yaml
from pathlib import Path

adr_path, name, email, identity, org, now, today, platform = sys.argv[1:9]

with open(adr_path) as f:
    data = yaml.safe_load(f)

# Authors / decision_owner / approvals
person = {"name": name, "role": "Principal Architect", "email": email}
data["authors"] = [person]
data["decision_owner"] = dict(person)
data["approvals"] = [{
    "name": name,
    "role": "Principal Architect",
    "identity": identity,
    "approved_at": now,
    "signature_id": None,
}]

# Project
data["adr"]["project"] = org
data["adr"]["last_modified"] = now

# Constraints — make platform-agnostic
new_constraints = [
    "Must be adoptable by teams without specialized tooling (YAML is human-readable)",
    "Must support formal approval workflows for regulated environments",
]
data["context"]["constraints"] = new_constraints

# Assumptions — make platform-agnostic
data["context"]["assumptions"] = [
    "Teams are comfortable with Git-based workflows and pull requests",
    "JSON Schema validation tooling is available in CI (Python 3.11+)",
    "ADR volume will remain under 100 active decisions per year",
]

# Dependencies — platform-agnostic
data["dependencies"] = {
    "internal": [
        "CI pipeline for schema validation (platform-specific template shipped)",
        "Python 3.11+ with jsonschema and pyyaml libraries",
    ],
    "external": [
        "JSON Schema specification (Draft 2020-12)",
    ],
}

# Confirmation — remove examples-reference references
data["confirmation"] = {
    "description": (
        "ADR governance process adopted. Validation confirmed by running "
        "scripts/run-validation.sh and scripts/check-repo-integrity.sh."
    ),
    "artifact_ids": [
        "TEST-SUITE-validate-adr",
        "scripts/run-validation.sh",
        "scripts/check-repo-integrity.sh",
    ],
}

# Always overwrite reviewers with adopter details
data["reviewers"] = [{
    "name": name,
    "role": "Adopter",
    "email": email,
}]

# Audit trail — replace with adoption event
data["audit_trail"] = [
    {
        "event": "created",
        "by": name,
        "at": now,
        "details": "ADR governance process adopted for " + org,
    },
    {
        "event": "approved",
        "by": name,
        "at": now,
        "details": (
            "Bootstrap self-approval (§3.4 exception for ADR-0000). "
            "Platform: " + platform
        ),
    },
]

# Decision date
data["decision"]["decision_date"] = today

# Lifecycle
data["lifecycle"]["next_review_date"] = str(int(today[:4]) + 5) + today[4:]

with open(adr_path, "w") as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=300)

print(f"  Updated {adr_path}")
PYEOF
ok "ADR-0000 updated"

# ── 2. Update .adr-governance/config.yaml ────────────────────────────────
info "Updating .adr-governance/config.yaml admin identity..."
CONFIG=".adr-governance/config.yaml"

python3 - "$CONFIG" "$IDENTITY" "$NAME" <<'PYEOF'
import sys, yaml
from pathlib import Path

config_path, identity, name = sys.argv[1:4]

# Strip leading @ for config identity (config uses bare handles)
bare_identity = identity.lstrip("@")

with open(config_path) as f:
    raw = f.read()

# Replace the identity line under admins
import re
raw = re.sub(
    r'(admins:\s*\n\s+-\s+identity:\s*)"[^"]*"',
    rf'\1"{bare_identity}"',
    raw,
)
raw = re.sub(
    r'(admins:\s*\n\s+-\s+identity:\s*"[^"]*"\s*\n\s+name:\s*)"[^"]*"',
    rf'\1"{name}"',
    raw,
)

with open(config_path, "w") as f:
    f.write(raw)

print(f"  Updated {config_path} → identity={bare_identity}")
PYEOF
ok "Config updated"

# ── 3. Copy platform CI template ────────────────────────────────────────
info "Copying CI template for $PLATFORM..."
case "$PLATFORM" in
  github)
    # Already at .github/workflows/validate-adr.yml — nothing to copy
    ok "GitHub Actions workflow already in place at .github/workflows/validate-adr.yml"
    ;;
  azure)
    cp ci/azure-devops/azure-pipelines.yml azure-pipelines.yml
    ok "Copied → azure-pipelines.yml"
    ;;
  gcp)
    cp ci/gcp-cloud-build/cloudbuild.yaml cloudbuild.yaml
    ok "Copied → cloudbuild.yaml"
    ;;
  aws)
    cp ci/aws-codebuild/buildspec.yml buildspec.yml
    ok "Copied → buildspec.yml"
    ;;
  gitlab)
    cp ci/gitlab-ci/.gitlab-ci.yml .gitlab-ci.yml
    ok "Copied → .gitlab-ci.yml"
    ;;
esac

# ── 4. Optionally remove examples-reference/ ─────────────────────────────
if $REMOVE_EXAMPLES; then
  if [ -d "examples-reference" ]; then
    info "Removing examples-reference/ (consumer-mode adoption)..."
    rm -rf examples-reference/
    ok "examples-reference/ removed"
  else
    warn "examples-reference/ already absent — nothing to remove"
  fi
fi

# ── 5. Render architecture-decision-log/ ─────────────────────────────────
info "Rendering ADRs..."
python3 scripts/render-adr.py --output-dir architecture-decision-log/rendered/ --generate-index architecture-decision-log/

if [ -d "examples-reference" ]; then
  python3 scripts/render-adr.py --output-dir examples-reference/rendered/ --generate-index examples-reference/
fi
ok "Rendering complete"

# ── 6. Regenerate llms-full.txt ──────────────────────────────────────────
info "Regenerating llms-full.txt..."
bash scripts/generate-llms-full.sh
ok "llms-full.txt regenerated"

# ── 7. Enable Git hooks ─────────────────────────────────────────────────
info "Enabling pre-commit hook..."
git config core.hooksPath .githooks
ok "Git hooks path set to .githooks"

# ── 8. Safe remote handling ──────────────────────────────────────────────
if git remote get-url origin 2>/dev/null | grep -q 'adr-governance'; then
  info "Renaming 'origin' to 'upstream-template' (safety: avoid accidental push to template repo)..."
  git remote rename origin upstream-template
  ok "Remote renamed: origin → upstream-template"
  warn "Add your own remote: git remote add origin <YOUR_REPO_URL>"
fi

# ── 8. Validate ──────────────────────────────────────────────────────────
info "Running validation..."
if bash scripts/run-validation.sh; then
  ok "Validation passed"
else
  fail "Validation failed — check the output above"
fi

info "Checking generated artifacts freshness..."
if bash scripts/check-generated-artifacts.sh; then
  ok "Generated artifacts are current"
else
  fail "Generated artifacts are stale — check the output above"
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🎉 Adoption bootstrap complete!                             ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}║  Next steps:                                                 ║${NC}"
echo -e "${GREEN}║  1. Review the updated ADR-0000                              ║${NC}"
echo -e "${GREEN}║  2. Add your remote:                                         ║${NC}"
echo -e "${GREEN}║     git remote add origin <YOUR_REPO_URL>                    ║${NC}"
echo -e "${GREEN}║  3. Commit:                                                  ║${NC}"
echo -e "${GREEN}║     git add -A && git commit -m 'chore: adopt ADR governance'║${NC}"
echo -e "${GREEN}║  4. Run: bash scripts/adoption-doctor.sh                     ║${NC}"
echo -e "${GREEN}║  5. Run: bash scripts/create-validation-smoke-test.sh        ║${NC}"
echo -e "${GREEN}║     (requires a clean working tree — commit first!)           ║${NC}"
echo -e "${GREEN}║  6. Configure branch protection (see docs/ci-setup.md)       ║${NC}"
echo -e "${GREEN}║  7. Push: git push -u origin main                            ║${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
