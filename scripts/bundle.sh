#!/usr/bin/env bash
# Bundle the ADR governance project into a single markdown file using repomix.
# The bundle includes: schema, ADR corpus, core authoring docs, skill assets,
# validator guidance, and embedded AI instructions (via instructionFilePath).
#
# This single file is optimized for AI chats and agents that need ADR authoring,
# querying, summarization, and schema-aware validation without direct repo access.
# Repository-side CI setup and PR enforcement remain outside the bundle.
#
# Usage:
#   ./scripts/bundle.sh
#
# Prerequisites:
#   npx (comes with Node.js) — repomix is run via npx, no global install needed.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "==> Bundling adr-governance project..."
cd "$PROJECT_ROOT"

npx -y repomix

BUNDLE_SIZE=$(wc -c < "${PROJECT_ROOT}/adr-governance-bundle.md" | tr -d ' ')
BUNDLE_KB=$((BUNDLE_SIZE / 1024))

echo ""
echo "==> Bundle created: ${PROJECT_ROOT}/adr-governance-bundle.md (${BUNDLE_KB} KB)"
echo "    Includes: schema, ADR corpus, core authoring docs, skill assets, validator guidance, and embedded AI instructions."
echo ""
echo "    Usage:"
echo "    • Upload to any AI web chat (ChatGPT, Copilot, Claude, Gemini)"
echo "    • Paste into an LLM context window"
echo "    • Add to your coding agent's project knowledge"
echo "    • See docs/web-chat-quickstart.md for platform-specific prompts"
