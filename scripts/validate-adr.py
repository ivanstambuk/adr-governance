#!/usr/bin/env python3
"""
Validate ADR YAML files against the ADR JSON Schema.

Usage:
    python3 validate-adr.py <file_or_directory>

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


def validate_file(filepath: Path, schema: dict) -> list[str]:
    """Validate a single ADR YAML file. Returns list of error messages."""
    errors = []
    try:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]

    if data is None:
        return ["File is empty"]

    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.path) or "(root)"
        errors.append(f"  {path}: {error.message}")

    # Additional semantic checks
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

    return errors


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file_or_directory>")
        sys.exit(2)

    target = Path(sys.argv[1])
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
    for filepath in files:
        errors = validate_file(filepath, schema)
        if errors:
            print(f"FAIL: {filepath}")
            for err in errors:
                print(err)
            total_errors += len(errors)
        else:
            print(f"OK:   {filepath}")

    print(f"\n{'='*60}")
    print(f"Files checked: {len(files)}")
    print(f"Total errors:  {total_errors}")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
