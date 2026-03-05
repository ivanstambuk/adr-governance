#!/usr/bin/env python3
"""
Validate ADR YAML files against the ADR JSON Schema.

Usage:
    python3 validate-adr.py <file_or_directory>
    python3 validate-adr.py --strict <file_or_directory>

Flags:
    --strict    Warn on missing optional-but-recommended sections for accepted ADRs
                (audit_trail, risk_assessment, confirmation)

Requires: pip install jsonschema pyyaml
"""

import json
import sys
import os
from pathlib import Path

try:
    import yaml
    from jsonschema import validate, ValidationError, Draft202012Validator
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip install jsonschema pyyaml")
    sys.exit(2)

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "adr.schema.json"


def load_schema():
    """Load the ADR JSON Schema."""
    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found at {SCHEMA_PATH}")
        sys.exit(2)
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)


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
            "draft": {"approved", "superseded", "deprecated"},
            "proposed": {"superseded", "deprecated"},
            "rejected": {"approved", "superseded", "deprecated"},
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

    return errors, warnings


def validate_cross_references(all_data: dict[str, dict]):
    """Check cross-file referential integrity.

    Args:
        all_data: mapping of filepath → parsed YAML data
    """
    warnings = []
    # Collect all known ADR IDs and their related_adrs
    known_ids = set()
    id_to_filepath = {}
    id_to_related = {}  # adr_id -> list of (ref_id, relationship)
    for filepath, data in all_data.items():
        if isinstance(data, dict):
            adr_id = data.get("adr", {}).get("id", "")
            if adr_id:
                known_ids.add(adr_id)
                id_to_filepath[adr_id] = filepath
                related = data.get("related_adrs", [])
                id_to_related[adr_id] = [
                    (e.get("id", ""), e.get("relationship", ""))
                    for e in related if isinstance(e, dict)
                ]

    # Check related_adrs references exist
    for filepath, data in all_data.items():
        if not isinstance(data, dict):
            continue
        related = data.get("related_adrs", [])
        if not related:
            continue
        for entry in related:
            if isinstance(entry, dict):
                ref_id = entry.get("id", "")
                if ref_id and ref_id not in known_ids:
                    warnings.append(
                        f"  {filepath}: related_adrs references '{ref_id}' which is not found in the validated set"
                    )

    # Check bidirectional relationship symmetry
    inverse_relationship = {
        "supersedes": "superseded_by",
        "superseded_by": "supersedes",
    }
    for adr_id, relations in id_to_related.items():
        for ref_id, relationship in relations:
            if relationship in inverse_relationship and ref_id in id_to_related:
                expected_inverse = inverse_relationship[relationship]
                partner_rels = id_to_related[ref_id]
                has_inverse = any(
                    r_id == adr_id and r_rel == expected_inverse
                    for r_id, r_rel in partner_rels
                )
                if not has_inverse:
                    warnings.append(
                        f"  {id_to_filepath.get(adr_id, adr_id)}: '{adr_id}' declares "
                        f"'{relationship}' to '{ref_id}', but '{ref_id}' does not have "
                        f"matching '{expected_inverse}' back to '{adr_id}'"
                    )

    return warnings


def main():
    # Parse args
    strict = False
    args = sys.argv[1:]
    if "--strict" in args:
        strict = True
        args.remove("--strict")

    if len(args) < 1:
        print(f"Usage: {sys.argv[0]} [--strict] <file_or_directory>")
        sys.exit(2)

    target = Path(args[0])
    schema = load_schema()

    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = sorted(target.glob("*.yaml")) + sorted(target.glob("*.yml"))
    else:
        print(f"ERROR: {target} is not a file or directory")
        sys.exit(2)

    if not files:
        print(f"No YAML files found in {target}")
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

    # Cross-file reference checks (only when validating a directory)
    if target.is_dir() and len(all_data) > 1:
        xref_warnings = validate_cross_references(all_data)
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
