#!/usr/bin/env bash
# Repository integrity checks for governance-critical tooling and committed
# generated artifacts that the main ADR validation flow would otherwise miss.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=== Python syntax checks ==="
python3 -m py_compile scripts/*.py

echo "=== Shell syntax checks ==="
for shell_script in scripts/*.sh; do
  if [ -f "$shell_script" ]; then
    bash -n "$shell_script"
  fi
done

REFERENCE_FILE=""
if [ -d "examples-reference/fictional" ] && ls examples-reference/fictional/*.yaml >/dev/null 2>&1; then
  REFERENCE_FILE="$(ls examples-reference/fictional/*.yaml | sort | head -n 1)"
elif [ -d "examples-reference/real-world" ] && ls examples-reference/real-world/*.yaml >/dev/null 2>&1; then
  REFERENCE_FILE="$(ls examples-reference/real-world/*.yaml | sort | head -n 1)"
elif [ -d "architecture-decision-log" ] && ls architecture-decision-log/*.yaml >/dev/null 2>&1; then
  REFERENCE_FILE="$(ls architecture-decision-log/*.yaml | sort | head -n 1)"
fi

EXTRACT_DIR=""
if [ -d "architecture-decision-log" ] && ls architecture-decision-log/*.yaml >/dev/null 2>&1; then
  EXTRACT_DIR="architecture-decision-log/"
elif [ -d "examples-reference/fictional" ] && ls examples-reference/fictional/*.yaml >/dev/null 2>&1; then
  EXTRACT_DIR="examples-reference/fictional/"
fi

if [ -z "$REFERENCE_FILE" ] || [ -z "$EXTRACT_DIR" ]; then
  echo "No ADR fixtures found for smoke tests — skipping runtime tool checks"
  exit 0
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

echo "=== Tool smoke tests ==="
python3 scripts/render-adr.py --output-dir "$TMP_DIR/rendered" "$REFERENCE_FILE" >/dev/null
python3 scripts/extract-decisions.py --format json "$EXTRACT_DIR" >/dev/null
python3 scripts/review-adr.py "$REFERENCE_FILE" >/dev/null
python3 scripts/summarize-adr.py "$REFERENCE_FILE" >/dev/null

if [ -d "tests" ]; then
  echo "=== Test suite ==="
  python3 -m unittest discover -s tests -v
fi

if [ -f "repomix.config.json" ]; then
  echo "=== repomix config syntax ==="
  python3 -m json.tool repomix.config.json >/dev/null
fi

bash scripts/check-generated-artifacts.sh

echo "Repository integrity checks passed."
