#!/usr/bin/env bash
# scripts/create-validation-smoke-test.sh — CI smoke-test helper
#
# Creates a disposable branch with a deliberately malformed ADR so
# adopters can prove that the CI merge gate fails closed.
#
# Usage:
#   bash scripts/create-validation-smoke-test.sh
#
# After running, the script prints instructions to:
#   1. Push the branch
#   2. Open a PR and watch CI fail
#   3. Delete the branch
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info()  { echo -e "${CYAN}ℹ${NC}  $*"; }
ok()    { echo -e "${GREEN}✅${NC} $*"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $*"; }
fail()  { echo -e "${RED}❌${NC} $*" >&2; exit 1; }

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

BRANCH="test/adr-smoke-test-$(date +%s)"
MALFORMED_FILE="architecture-decision-log/ADR-9999-ci-smoke-test.yaml"

# Ensure working tree is clean
if ! git diff --quiet || ! git diff --cached --quiet; then
  fail "Working tree has uncommitted changes — commit or stash first"
fi

info "Creating branch: $BRANCH"
git checkout -b "$BRANCH"

info "Creating malformed ADR: $MALFORMED_FILE"
cat > "$MALFORMED_FILE" <<'YAML'
# This file is intentionally malformed to test CI validation.
# It should cause validate-adr.py to fail.
adr:
  id: ADR-9999-ci-smoke-test
  title: "Intentionally malformed ADR for CI smoke test"
  status: invalid-status-value
  created_at: "not-a-date"
YAML

git add "$MALFORMED_FILE"
git commit -m "test: CI smoke test — intentionally malformed ADR (delete this branch after)"

ok "Branch '$BRANCH' created with malformed ADR"

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  Next steps:                                           ║${NC}"
echo -e "${CYAN}╠══════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║                                                        ║${NC}"
echo -e "${CYAN}║  1. Push the branch:                                   ║${NC}"
echo -e "${CYAN}║     git push origin $BRANCH${NC}"
echo -e "${CYAN}║                                                        ║${NC}"
echo -e "${CYAN}║  2. Open a PR targeting main — CI should FAIL          ║${NC}"
echo -e "${CYAN}║                                                        ║${NC}"
echo -e "${CYAN}║  3. After verifying, clean up:                         ║${NC}"
echo -e "${CYAN}║     git checkout main                                  ║${NC}"
echo -e "${CYAN}║     git branch -D $BRANCH${NC}"
echo -e "${CYAN}║     git push origin --delete $BRANCH${NC}"
echo -e "${CYAN}║                                                        ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
