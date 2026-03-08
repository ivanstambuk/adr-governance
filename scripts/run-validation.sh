#!/usr/bin/env bash
# Run ADR validation across repository ADR directories.
#
# By default, the governed ADR corpus and the fictional example corpus are
# validated separately so example IDs do not reserve IDs in the live ADR
# namespace. If explicit files/directories are passed, they are validated in a
# single invocation so callers can opt into combined-corpus checks.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

declare -a targets=()

if [ "$#" -gt 0 ]; then
  for candidate in "$@"; do
    if [ -f "$candidate" ]; then
      targets+=("$candidate")
    elif [ -d "$candidate" ] && ls "$candidate"/*.yaml >/dev/null 2>&1; then
      targets+=("$candidate")
    elif [ -d "$candidate" ] && ls "$candidate"/*.yml >/dev/null 2>&1; then
      targets+=("$candidate")
    fi
  done
  if [ "${#targets[@]}" -eq 0 ]; then
    echo "No ADR files found — skipping validation"
    exit 0
  fi

  echo "=== Validating ADR sources together ==="
  printf '  • %s\n' "${targets[@]}"
  python3 scripts/validate-adr.py "${targets[@]}"
  exit 0
fi

run_default_target() {
  local label="$1"
  local target="$2"

  if [ -d "$target" ] && (ls "$target"/*.yaml >/dev/null 2>&1 || ls "$target"/*.yml >/dev/null 2>&1); then
    echo "=== $label ==="
    echo "  • $target"
    python3 scripts/validate-adr.py "$target"
    return 0
  fi

  return 1
}

found_default_targets=0

if run_default_target "Validating governed ADR corpus" "architecture-decision-log"; then
  found_default_targets=1
fi

if run_default_target "Validating fictional ADR examples" "examples-reference/fictional"; then
  found_default_targets=1
fi

if run_default_target "Validating real-world ADR examples" "examples-reference/real-world"; then
  found_default_targets=1
fi

if [ "$found_default_targets" -eq 0 ]; then
  echo "No ADR files found — skipping validation"
  exit 0
fi
