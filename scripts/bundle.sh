#!/usr/bin/env bash
# Bundle the ADR governance project into a single markdown file using repomix.
# Excludes examples-reference/ and .github/ (CI/CD) — see repomix.config.json.
#
# Usage:
#   ./scripts/bundle.sh
#
# Prerequisites:
#   npx (comes with Node.js) — repomix is run via npx, no global install needed.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "==> Bundling adr-governance project (excluding examples and CI/CD)..."
cd "$PROJECT_ROOT"

npx -y repomix

echo ""
echo "==> Bundle created: ${PROJECT_ROOT}/adr-governance-bundle.md"
echo "    You can now paste this into any LLM context window."
