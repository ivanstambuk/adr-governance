#!/usr/bin/env bash
# Run ADR validation across all repository ADR directories in one invocation.
#
# This keeps duplicate-ID and cross-reference checks consistent between local
# usage and CI by validating all discovered ADR sources together.

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
else
  for candidate in architecture-decision-log examples-reference; do
    if [ -d "$candidate" ] && (ls "$candidate"/*.yaml >/dev/null 2>&1 || ls "$candidate"/*.yml >/dev/null 2>&1); then
      targets+=("$candidate")
    fi
  done
fi

if [ "${#targets[@]}" -eq 0 ]; then
  echo "No ADR files found — skipping validation"
  exit 0
fi

echo "=== Validating ADR sources ==="
printf '  • %s\n' "${targets[@]}"
python3 scripts/validate-adr.py "${targets[@]}"
