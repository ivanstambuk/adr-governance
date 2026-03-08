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
    return $?
  fi

  # Directory missing or empty — not a failure, just nothing to validate
  return 255
}

found_default_targets=0
validation_failed=0

for spec in \
  "Validating governed ADR corpus|architecture-decision-log" \
  "Validating fictional ADR examples|examples-reference/fictional" \
  "Validating real-world ADR examples|examples-reference/real-world"; do

  label="${spec%%|*}"
  target="${spec##*|}"

  set +e
  run_default_target "$label" "$target"
  rc=$?
  set -e

  if [ "$rc" -eq 255 ]; then
    continue  # directory absent or empty — skip
  fi

  found_default_targets=1
  if [ "$rc" -ne 0 ]; then
    validation_failed=1
  fi
done

if [ "$found_default_targets" -eq 0 ]; then
  echo "No ADR files found — skipping validation"
  exit 0
fi

if [ "$validation_failed" -ne 0 ]; then
  echo "Validation failed for one or more ADR directories."
  exit 1
fi
