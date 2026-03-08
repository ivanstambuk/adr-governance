#!/usr/bin/env bash
# scripts/adoption-doctor.sh — Post-bootstrap adoption health check
#
# Verifies that the repo is correctly set up for downstream use.
# Exits 0 if everything is healthy; exits 1 if any check fails.
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; CYAN='\033[0;36m'; NC='\033[0m'
pass()  { echo -e "  ${GREEN}✅${NC} $*"; }
warnc() { echo -e "  ${YELLOW}⚠${NC}  $*"; }
failc() { echo -e "  ${RED}❌${NC} $*"; FAILURES=$((FAILURES + 1)); }

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

FAILURES=0

echo -e "\n${CYAN}=== ADR Governance — Adoption Doctor ===${NC}\n"

# ── 1. CI file present ──────────────────────────────────────────────────
echo "CI configuration:"
FOUND_CI=false
for f in .github/workflows/validate-adr.yml azure-pipelines.yml cloudbuild.yaml buildspec.yml .gitlab-ci.yml; do
  if [ -f "$f" ]; then
    pass "CI file found: $f"
    FOUND_CI=true
  fi
done
if ! $FOUND_CI; then
  failc "No CI file found — copy a template from ci/ to the repo root (see docs/ci-setup.md)"
fi

# ── 2. ADR-0000 customised ──────────────────────────────────────────────
echo ""
echo "ADR-0000 customisation:"
ADR0="architecture-decision-log/ADR-0000-adopt-governed-adr-process.yaml"
if [ -f "$ADR0" ]; then
  if grep -q '"Ivan Stambuk"' "$ADR0" 2>/dev/null || grep -q "'Ivan Stambuk'" "$ADR0" 2>/dev/null; then
    warnc "ADR-0000 still has the upstream author (Ivan Stambuk) — personalise it for your org"
  else
    pass "ADR-0000 has been customised"
  fi

  if grep -q 'project: ADR Governance' "$ADR0" 2>/dev/null; then
    warnc "ADR-0000 adr.project is still 'ADR Governance' — update to your organisation name"
  else
    pass "ADR-0000 adr.project has been updated"
  fi
else
  failc "ADR-0000 not found at $ADR0"
fi

# ── 3. Governance config identity ────────────────────────────────────────
echo ""
echo "Governance configuration:"
CONFIG=".adr-governance/config.yaml"
if [ -f "$CONFIG" ]; then
  if grep -q 'identity: "ivanstambuk"' "$CONFIG" 2>/dev/null; then
    warnc "config.yaml admin identity is still 'ivanstambuk' — update to your identity"
  else
    pass "config.yaml admin identity has been updated"
  fi
else
  failc "Governance config not found at $CONFIG"
fi

# ── 4. Git hooks path ────────────────────────────────────────────────────
echo ""
echo "Git hooks:"
HOOKS_PATH="$(git config --get core.hooksPath 2>/dev/null || echo "")"
if [ "$HOOKS_PATH" = ".githooks" ]; then
  pass "Git hooks path is .githooks"
else
  failc "Git hooks path is '${HOOKS_PATH:-<unset>}' — run: git config core.hooksPath .githooks"
fi

# ── 5. Rendered artifacts ────────────────────────────────────────────────
echo ""
echo "Rendered artifacts:"
if [ -d "architecture-decision-log/rendered" ]; then
  COUNT=$(find architecture-decision-log/rendered -name '*.md' | wc -l)
  if [ "$COUNT" -gt 0 ]; then
    pass "Found $COUNT rendered Markdown file(s) in architecture-decision-log/rendered/"
  else
    failc "architecture-decision-log/rendered/ exists but is empty — run: make render"
  fi
else
  failc "architecture-decision-log/rendered/ not found — run: make render"
fi

if [ -f "llms-full.txt" ]; then
  pass "llms-full.txt exists"
else
  failc "llms-full.txt not found — run: bash scripts/generate-llms-full.sh"
fi

# ── 6. No-examples compatibility ─────────────────────────────────────────
echo ""
echo "Consumer-mode (no examples-reference/):"
if [ -d "examples-reference" ]; then
  pass "examples-reference/ is present (full upstream shape)"
else
  pass "examples-reference/ has been removed (consumer-mode adoption)"

  # Verify nothing is broken
  if bash scripts/run-validation.sh >/dev/null 2>&1; then
    pass "run-validation.sh passes without examples-reference/"
  else
    failc "run-validation.sh fails without examples-reference/ — this is a bug"
  fi
fi

# ── 7. Validation ─────────────────────────────────────────────────────────
echo ""
echo "Validation:"
if bash scripts/run-validation.sh >/dev/null 2>&1; then
  pass "run-validation.sh passes"
else
  failc "run-validation.sh fails — check for malformed ADRs"
fi

if bash scripts/check-generated-artifacts.sh >/dev/null 2>&1; then
  pass "Generated artifacts are current"
else
  failc "Generated artifacts are stale — re-render and regenerate"
fi

# ── Summary ──────────────────────────────────────────────────────────────
echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo -e "${GREEN}All checks passed.${NC}"
  exit 0
else
  echo -e "${RED}${FAILURES} check(s) failed. See above for details.${NC}"
  exit 1
fi
