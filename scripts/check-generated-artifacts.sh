#!/usr/bin/env bash
# Verify committed generated artifacts are current without mutating the worktree.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
SNAPSHOT_ROOT="$TMP_DIR/snapshot"

cd "$PROJECT_ROOT"

list_adr_sources() {
    find "$1" -path '*/rendered' -prune -o -type f \( -name '*.yaml' -o -name '*.yml' \) -print | sort
}

check_directory() {
    local source_dir="$1"
    local actual_dir="$2"
    local label="$3"
    local regen_command="$4"
    local diff_file="$TMP_DIR/$(echo "$label" | tr ' /' '__').diff"
    local snapshot_source_dir="$SNAPSHOT_ROOT/${source_dir%/}"
    local expected_dir="$SNAPSHOT_ROOT/$actual_dir"

    rm -rf "$snapshot_source_dir" "$expected_dir"
    mkdir -p "$snapshot_source_dir" "$(dirname "$expected_dir")"

    if [ -d "$source_dir" ] && list_adr_sources "$source_dir" | grep -q .; then
        while IFS= read -r source_file; do
            cp "$source_file" "$snapshot_source_dir"/
        done < <(list_adr_sources "$source_dir")
        python3 scripts/render-adr.py --output-dir "$expected_dir" --generate-index "$snapshot_source_dir/" >/dev/null
    fi

    mkdir -p "$expected_dir"

    if [ ! -d "$actual_dir" ]; then
        if find "$expected_dir" -type f | grep -q .; then
            echo "ERROR: $label is missing or stale."
            echo "Regenerate it with: $regen_command"
            return 1
        fi
        return 0
    fi

    if ! diff -ruN "$expected_dir" "$actual_dir" >"$diff_file"; then
        echo "ERROR: $label is stale."
        cat "$diff_file"
        echo
        echo "Regenerate it with: $regen_command"
        return 1
    fi
}

check_file() {
    local actual_file="$1"
    local expected_file="$2"
    local label="$3"
    local regen_command="$4"
    local diff_file="$TMP_DIR/$(echo "$label" | tr ' /' '__').diff"

    if [ ! -f "$actual_file" ]; then
        echo "ERROR: $label is missing."
        echo "Regenerate it with: $regen_command"
        return 1
    fi

    if ! diff -u "$expected_file" "$actual_file" >"$diff_file"; then
        echo "ERROR: $label is stale."
        cat "$diff_file"
        echo
        echo "Regenerate it with: $regen_command"
        return 1
    fi
}

echo "=== Generated artifact freshness ==="

check_directory \
    "architecture-decision-log/" \
    "rendered" \
    "rendered ADR Markdown" \
    "make render"

check_directory \
    "examples-reference/" \
    "examples-reference/rendered" \
    "rendered example ADR Markdown" \
    "make render"

scripts/generate-llms-full.sh --output "$TMP_DIR/llms-full.txt" >/dev/null
check_file \
    "llms-full.txt" \
    "$TMP_DIR/llms-full.txt" \
    "llms-full.txt" \
    "make llms-full"

echo "Generated artifacts are current."
