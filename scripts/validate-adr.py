#!/usr/bin/env python3
"""
Validate ADR YAML files against the ADR JSON Schema.

Usage:
    python3 validate-adr.py <file_or_directory> [<file_or_directory> ...]
    python3 validate-adr.py --strict decisions/ examples/

Flags:
    --strict    Warn on missing optional-but-recommended sections for accepted ADRs
                (audit_trail, risk_assessment, confirmation)

Requires: pip install jsonschema pyyaml
"""

import json
import re
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
    from jsonschema import validate, ValidationError, Draft202012Validator
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip install jsonschema pyyaml")
    sys.exit(2)

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "adr.schema.json"

# Regex to extract ADR-NNNN prefix from filenames
FILENAME_ID_RE = re.compile(r"^(ADR-\d{4})")


def load_schema():
    """Load the ADR JSON Schema."""
    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found at {SCHEMA_PATH}")
        sys.exit(2)
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)


def parse_iso_datetime(ts_str: str) -> datetime | None:
    """Parse an ISO 8601 datetime string to a timezone-aware datetime.

    Returns None if parsing fails.
    """
    if not ts_str:
        return None
    try:
        # Python 3.11+ handles most ISO 8601 strings directly
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def validate_file(filepath: Path, schema: dict, strict: bool = False) -> tuple[list[str], list[str]]:
    """Validate a single ADR YAML file.

    Returns:
        (errors, warnings) — errors are hard failures, warnings are advisory.
    """
    errors = []
    warnings = []
    try:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"], []

    if data is None:
        return ["File is empty"], []

    # --- JSON Schema validation ---
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.path) or "(root)"
        errors.append(f"  {path}: {error.message}")

    # --- Semantic checks ---
    if isinstance(data, dict):
        # Check chosen_alternative matches an alternative name
        alternatives = data.get("alternatives", [])
        decision = data.get("decision", {})
        chosen = decision.get("chosen_alternative", "")
        alt_names = [a.get("name", "") for a in alternatives if isinstance(a, dict)]
        if chosen and alt_names and chosen not in alt_names:
            errors.append(
                f"  decision.chosen_alternative: '{chosen}' does not match any alternative name: {alt_names}"
            )

        # Check status ↔ audit_trail consistency
        status = data.get("adr", {}).get("status", "")
        audit_trail = data.get("audit_trail", [])
        audit_events = [e.get("event", "") for e in audit_trail if isinstance(e, dict)]

        status_to_expected_event = {
            "accepted": "approved",
            "rejected": "rejected",
            "superseded": "superseded",
            "deprecated": "deprecated",
            "deferred": "deferred",
        }

        if status in status_to_expected_event and audit_trail:
            expected = status_to_expected_event[status]
            if expected not in audit_events:
                warnings.append(
                    f"  audit_trail: status is '{status}' but no '{expected}' event found in audit_trail"
                )

        # Check approvals ↔ audit_trail consistency
        approvals = data.get("approvals", [])
        if approvals and audit_trail:
            approvals_with_timestamp = [
                a for a in approvals
                if isinstance(a, dict) and a.get("approved_at") is not None
            ]
            approved_events = [e for e in audit_trail if isinstance(e, dict) and e.get("event") == "approved"]
            if approvals_with_timestamp and not approved_events:
                warnings.append(
                    f"  audit_trail: {len(approvals_with_timestamp)} approval(s) have timestamps but no 'approved' event in audit_trail"
                )

        # --- Strict mode checks ---
        if strict and status == "accepted":
            recommended_sections = ["audit_trail", "risk_assessment", "confirmation"]
            for section in recommended_sections:
                if section not in data or not data[section]:
                    warnings.append(
                        f"  [strict] '{section}' is missing or empty — recommended for accepted ADRs"
                    )

        # Check for invalid state transitions (status vs audit trail events)
        invalid_event_for_status = {
            "draft": {"approved", "superseded", "deprecated", "deferred"},
            "proposed": {"superseded", "deprecated"},
            "accepted": {"deferred"},
            "rejected": {"approved", "superseded", "deprecated", "deferred"},
            "deferred": {"approved", "superseded", "deprecated"},
        }
        if status in invalid_event_for_status and audit_trail:
            for bad_event in invalid_event_for_status[status]:
                if bad_event in audit_events:
                    warnings.append(
                        f"  audit_trail: status is '{status}' but audit_trail contains "
                        f"'{bad_event}' event — invalid state transition"
                    )

        # Check confidence ↔ review cycle consistency (strict only)
        if strict:
            confidence = decision.get("confidence", "")
            lifecycle = data.get("lifecycle", {})
            review_months = lifecycle.get("review_cycle_months")
            if confidence and review_months is not None:
                if confidence == "low" and review_months > 6:
                    warnings.append(
                        f"  [strict] decision.confidence is 'low' but lifecycle.review_cycle_months "
                        f"is {review_months} — recommended ≤6 months for low-confidence decisions"
                    )
                if confidence == "high" and review_months < 12:
                    warnings.append(
                        f"  [strict] decision.confidence is 'high' but lifecycle.review_cycle_months "
                        f"is {review_months} — extended cycle (≥12 months) is acceptable for high-confidence decisions"
                    )

        # --- [strict] Warn if adr.summary is missing on proposed/accepted ADRs ---
        if strict and status in {"proposed", "accepted"}:
            summary = data.get("adr", {}).get("summary", "")
            if not summary or not summary.strip():
                warnings.append(
                    f"  [strict] 'adr.summary' is missing or empty — recommended for {status} ADRs "
                    f"(elevator pitch for stakeholder triage)"
                )

        # --- [strict] Warn if schema_version is missing ---
        if strict:
            schema_version = data.get("adr", {}).get("schema_version", "")
            if not schema_version:
                warnings.append(
                    f"  [strict] 'adr.schema_version' is missing — recommended per schema versioning policy (§10)"
                )

        # --- Check audit_trail temporal ordering (proper datetime parsing) ---
        if audit_trail:
            prev_dt = None
            prev_ts_str = None
            for i, entry in enumerate(audit_trail):
                if isinstance(entry, dict):
                    ts_str = entry.get("at", "")
                    if ts_str:
                        current_dt = parse_iso_datetime(str(ts_str))
                        if current_dt and prev_dt and current_dt < prev_dt:
                            warnings.append(
                                f"  audit_trail[{i}]: event '{entry.get('event', '')}' at {ts_str} "
                                f"is earlier than previous event at {prev_ts_str} — events should be in chronological order"
                            )
                        if current_dt:
                            prev_dt = current_dt
                            prev_ts_str = ts_str

        # --- [strict] Warn if accepted ADR has no approval with timestamp ---
        if strict and status == "accepted":
            approvals_with_ts = [
                a for a in approvals
                if isinstance(a, dict) and a.get("approved_at") is not None
            ]
            if not approvals_with_ts:
                warnings.append(
                    f"  [strict] status is 'accepted' but no approval entry has an 'approved_at' timestamp"
                )

        # --- [strict] Warn if confidence is set on a draft ADR ---
        if strict and status == "draft":
            conf = decision.get("confidence", "")
            if conf:
                warnings.append(
                    f"  [strict] decision.confidence is '{conf}' but status is 'draft' — "
                    f"confidence is premature before the decision is proposed"
                )

        # --- [strict] Check decision_date within created_at → last_modified range ---
        if strict:
            decision_date = decision.get("decision_date", "")
            created_at = data.get("adr", {}).get("created_at", "")
            last_modified = data.get("adr", {}).get("last_modified", "")
            if decision_date and created_at:
                # Compare date strings (ISO 8601 sorts lexicographically)
                created_date = str(created_at)[:10]  # extract date portion
                if str(decision_date) < created_date:
                    warnings.append(
                        f"  [strict] decision.decision_date ({decision_date}) is before "
                        f"adr.created_at ({created_date}) — decision cannot predate the ADR"
                    )

        # --- [strict] Warn if consequences is one-sided ---
        if strict:
            consequences = data.get("consequences", {})
            if consequences:
                positive = consequences.get("positive", [])
                negative = consequences.get("negative", [])
                if not positive:
                    warnings.append(
                        f"  [strict] 'consequences.positive' is missing or empty — "
                        f"a balanced decision should acknowledge positive outcomes"
                    )
                if not negative:
                    warnings.append(
                        f"  [strict] 'consequences.negative' is missing or empty — "
                        f"a balanced decision should acknowledge negative outcomes or tradeoffs"
                    )

        # --- Check filename ↔ adr.id consistency ---
        adr_id = data.get("adr", {}).get("id", "")
        if adr_id:
            filename = filepath.stem  # e.g. "ADR-0001-dpop-over-mtls"
            match = FILENAME_ID_RE.match(filename)
            if match:
                filename_id = match.group(1)
                # Extract just the ADR-NNNN portion from the YAML id
                yaml_id_match = FILENAME_ID_RE.match(adr_id)
                yaml_id_prefix = yaml_id_match.group(1) if yaml_id_match else adr_id
                if filename_id != yaml_id_prefix:
                    errors.append(
                        f"  filename prefix '{filename_id}' does not match adr.id '{adr_id}'"
                    )

    return errors, warnings


def validate_cross_references(all_data: dict[str, dict]):
    """Check cross-file referential integrity.

    Checks:
    - Lifecycle supersession symmetry
    - Duplicate ADR IDs across all files

    Args:
        all_data: mapping of filepath → parsed YAML data
    """
    warnings = []
    errors = []
    # Collect all known ADR IDs and their lifecycle supersession fields
    known_ids = set()
    id_to_filepath = {}
    id_to_supersedes = {}       # adr_id -> supersedes value
    id_to_superseded_by = {}    # adr_id -> superseded_by value
    for filepath, data in all_data.items():
        if isinstance(data, dict):
            adr_id = data.get("adr", {}).get("id", "")
            if adr_id:
                # --- Check for duplicate ADR IDs ---
                if adr_id in known_ids:
                    errors.append(
                        f"  duplicate ADR ID '{adr_id}': found in both "
                        f"'{id_to_filepath[adr_id]}' and '{filepath}'"
                    )
                known_ids.add(adr_id)
                id_to_filepath[adr_id] = filepath
                lifecycle = data.get("lifecycle", {})
                sup = lifecycle.get("supersedes")
                sup_by = lifecycle.get("superseded_by")
                if sup:
                    id_to_supersedes[adr_id] = sup
                if sup_by:
                    id_to_superseded_by[adr_id] = sup_by

    # Check supersession symmetry: if A supersedes B, B should have superseded_by A
    for adr_id, target_id in id_to_supersedes.items():
        if target_id in known_ids:
            if target_id not in id_to_superseded_by or id_to_superseded_by[target_id] != adr_id:
                warnings.append(
                    f"  {id_to_filepath.get(adr_id, adr_id)}: '{adr_id}' declares "
                    f"lifecycle.supersedes '{target_id}', but '{target_id}' does not have "
                    f"lifecycle.superseded_by '{adr_id}'"
                )

    for adr_id, target_id in id_to_superseded_by.items():
        if target_id in known_ids:
            if target_id not in id_to_supersedes or id_to_supersedes[target_id] != adr_id:
                warnings.append(
                    f"  {id_to_filepath.get(adr_id, adr_id)}: '{adr_id}' declares "
                    f"lifecycle.superseded_by '{target_id}', but '{target_id}' does not have "
                    f"lifecycle.supersedes '{adr_id}'"
                )

    return errors, warnings


def main():
    # Parse args
    strict = False
    args = sys.argv[1:]
    if "--strict" in args:
        strict = True
        args.remove("--strict")

    if len(args) < 1:
        print(f"Usage: {sys.argv[0]} [--strict] <file_or_directory> [<file_or_directory> ...]")
        sys.exit(2)

    schema = load_schema()

    # Collect files from all positional arguments
    files = []
    for arg in args:
        target = Path(arg)
        if target.is_file():
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(target.glob("*.yaml")))
            files.extend(sorted(target.glob("*.yml")))
        else:
            print(f"ERROR: {target} is not a file or directory")
            sys.exit(2)

    if not files:
        print(f"No YAML files found in: {', '.join(args)}")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0
    all_data = {}

    for filepath in files:
        errors, warnings = validate_file(filepath, schema, strict=strict)

        # Load data for cross-reference checks
        try:
            with open(filepath, "r") as f:
                all_data[str(filepath)] = yaml.safe_load(f)
        except yaml.YAMLError:
            pass

        if errors:
            print(f"FAIL: {filepath}")
            for err in errors:
                print(err)
            total_errors += len(errors)
        elif warnings:
            print(f"OK:   {filepath}")
        else:
            print(f"OK:   {filepath}")

        if warnings:
            for warn in warnings:
                print(f"  WARN: {warn.strip()}")
            total_warnings += len(warnings)

    # Cross-file reference checks (when more than 1 file loaded)
    if len(all_data) > 1:
        xref_errors, xref_warnings = validate_cross_references(all_data)
        if xref_errors:
            print("\nCross-reference errors:")
            for err in xref_errors:
                print(f"  ERROR: {err.strip()}")
            total_errors += len(xref_errors)
        if xref_warnings:
            print("\nCross-reference warnings:")
            for warn in xref_warnings:
                print(f"  WARN: {warn.strip()}")
            total_warnings += len(xref_warnings)

    print(f"\n{'='*60}")
    print(f"Files checked:  {len(files)}")
    print(f"Total errors:   {total_errors}")
    print(f"Total warnings: {total_warnings}")

    if strict:
        print("Mode: strict")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
