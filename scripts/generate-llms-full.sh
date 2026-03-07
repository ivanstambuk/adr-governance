#!/usr/bin/env bash
# =============================================================================
# Generate llms-full.txt — complete inline documentation for AI assistants.
# =============================================================================
#
# Concatenates key documentation files into a single Markdown document
# following the llms-full.txt convention (https://llmstxt.org/).
#
# Sources (in order):
#   1. README.md
#   2. docs/adr-process.md
#   3. docs/glossary.md
#   4. .skills/adr-author/references/SCHEMA_REFERENCE.md
#   5. docs/ci-setup.md
#
# Usage:
#   ./scripts/generate-llms-full.sh
#   ./scripts/generate-llms-full.sh --output /tmp/llms-full.txt
#
# Called automatically by:
#   - make llms-full
#   - .githooks/pre-commit (when source docs change)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

OUTPUT="${PROJECT_ROOT}/llms-full.txt"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output)
            if [[ $# -lt 2 ]]; then
                echo "Error: --output requires a path" >&2
                exit 1
            fi
            OUTPUT="$2"
            shift 2
            ;;
        -h|--help)
            cat <<'EOF'
Usage: ./scripts/generate-llms-full.sh [--output PATH]

Options:
  -o, --output PATH   Write llms-full output to PATH instead of llms-full.txt
  -h, --help          Show this help text
EOF
            exit 0
            ;;
        *)
            echo "Error: unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

# Source documents — order matters (most general → most specific)
SOURCES=(
    "README.md"
    "docs/adr-process.md"
    "docs/glossary.md"
    ".skills/adr-author/references/SCHEMA_REFERENCE.md"
    "docs/ci-setup.md"
)

# Section titles matching each source
TITLES=(
    "README"
    "ADR Governance Process"
    "Glossary"
    "Schema Reference"
    "CI/CD Setup Guide"
)

cd "$PROJECT_ROOT"

mkdir -p "$(dirname "$OUTPUT")"

# Header
cat > "$OUTPUT" << 'HEADER'
# adr-governance

> A schema-governed, AI-native Architecture Decision Record (ADR) framework. This is the full documentation — for a concise overview with links, see [llms.txt](https://github.com/ivanstambuk/adr-governance/blob/main/llms.txt).

---

HEADER

# Concatenate each source with a section header
for i in "${!SOURCES[@]}"; do
    src="${SOURCES[$i]}"
    title="${TITLES[$i]}"

    if [ ! -f "$src" ]; then
        echo "⚠️  Skipping missing file: $src" >&2
        continue
    fi

    echo "## ${title}" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    cat "$src" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    echo "---" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
done

LINE_COUNT=$(wc -l < "$OUTPUT" | tr -d ' ')
echo "✅ Generated $(basename "$OUTPUT") (${LINE_COUNT} lines)"
