#!/usr/bin/env python3
"""
Validate ADR YAML files against the ADR JSON Schema.

Usage:
    python3 validate-adr.py <file_or_directory> [<file_or_directory> ...]

Requires: pip install "jsonschema[format]" pyyaml
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print('  pip install "jsonschema[format]" pyyaml')
    sys.exit(2)

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "adr.schema.json"
REPO_ROOT = SCHEMA_PATH.parent.parent
GOVERNED_ADR_DIRECTORIES = ("architecture-decision-log", "examples-reference")
REQUIRED_SCHEMA_FORMATS = {"date-time", "date", "email", "uri"}


def load_schema():
    """Load the ADR JSON Schema."""
    if not SCHEMA_PATH.exists():
        print(f"ERROR: Schema not found at {SCHEMA_PATH}")
        sys.exit(2)
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)


def build_validator(schema: dict) -> Draft202012Validator:
    """Build a JSON Schema validator with format enforcement enabled."""
    format_checker = Draft202012Validator.FORMAT_CHECKER
    missing_formats = sorted(REQUIRED_SCHEMA_FORMATS - set(format_checker.checkers))
    if missing_formats:
        print(
            "ERROR: The installed jsonschema package does not provide all required "
            f"format checkers: {', '.join(missing_formats)}"
        )
        print("Install dependencies with: pip install -r requirements.txt")
        sys.exit(2)

    return Draft202012Validator(schema, format_checker=format_checker)


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


def is_within_directory(path: Path, directory: Path) -> bool:
    """Return True when path is inside directory (or equal to it)."""
    try:
        path.resolve(strict=False).relative_to(directory.resolve(strict=False))
        return True
    except ValueError:
        return False


def collect_input_files(targets: list[str]) -> list[Path]:
    """Collect explicit YAML files from positional CLI targets."""
    files = []
    for arg in targets:
        target = Path(arg)
        if target.is_file():
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(target.glob("*.yaml")))
            files.extend(sorted(target.glob("*.yml")))
        else:
            print(f"ERROR: {target} is not a file or directory")
            sys.exit(2)
    return files


def discover_repo_context_roots(primary_files: list[Path]) -> list[Path]:
    """Resolve which governed ADR directories should supplement the validation corpus."""
    governed_roots = [REPO_ROOT / name for name in GOVERNED_ADR_DIRECTORIES]
    selected_roots = []

    for filepath in primary_files:
        for governed_root in governed_roots:
            if governed_root in selected_roots:
                continue
            if is_within_directory(filepath, governed_root):
                selected_roots.append(governed_root)

    return selected_roots


def should_load_repo_context(primary_files: list[Path]) -> bool:
    """Only auto-load repo context for repo-local governed ADR files."""
    return bool(discover_repo_context_roots(primary_files))


def discover_repo_context_files(primary_files: list[Path]) -> list[Path]:
    """Load the governed ADR corpus to resolve cross-file references."""
    repo_context_roots = discover_repo_context_roots(primary_files)
    if not repo_context_roots:
        return []

    seen = {filepath.resolve(strict=False) for filepath in primary_files}
    supplemental = []
    for directory in repo_context_roots:
        if not directory.is_dir():
            continue
        for pattern in ("*.yaml", "*.yml"):
            for filepath in sorted(directory.glob(pattern)):
                resolved = filepath.resolve(strict=False)
                if resolved in seen:
                    continue
                supplemental.append(filepath)
                seen.add(resolved)
    return supplemental


def load_yaml_documents(files: list[Path]) -> dict[str, dict]:
    """Load parsed YAML documents for cross-reference validation."""
    documents = {}
    for filepath in files:
        try:
            with open(filepath, "r") as f:
                documents[str(filepath)] = yaml.safe_load(f)
        except yaml.YAMLError:
            continue
    return documents


def build_cross_reference_corpus(primary_files: list[Path]) -> tuple[dict[str, dict], set[str]]:
    """Build the YAML corpus used for duplicate-ID and lifecycle checks."""
    corpus_files = list(primary_files) + discover_repo_context_files(primary_files)
    return load_yaml_documents(corpus_files), {str(filepath) for filepath in primary_files}


def validate_file(
    filepath: Path,
    validator: Draft202012Validator,
) -> tuple[list[str], list[str]]:
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

        # Check approvals ↔ audit_trail consistency
        approvals = data.get("approvals", [])
        approvals_with_timestamp = [
            a for a in approvals
            if isinstance(a, dict) and a.get("approved_at") is not None
        ]
        approved_events = [
            e for e in audit_trail
            if isinstance(e, dict) and e.get("event") == "approved"
        ]

        status_to_expected_event = {
            "rejected": "rejected",
            "superseded": "superseded",
            "deprecated": "deprecated",
            "deferred": "deferred",
        }

        if status == "accepted":
            if not approvals_with_timestamp:
                errors.append(
                    "  status is 'accepted' but no approval entry has a non-null 'approved_at' timestamp"
                )
            if not approved_events:
                errors.append(
                    "  audit_trail: status is 'accepted' but no 'approved' event found in audit_trail"
                )
        elif approvals_with_timestamp and not approved_events:
            warnings.append(
                f"  audit_trail: {len(approvals_with_timestamp)} approval(s) have timestamps but no 'approved' event in audit_trail"
            )

        if status in status_to_expected_event:
            expected = status_to_expected_event[status]
            if expected not in audit_events:
                errors.append(
                    f"  audit_trail: status is '{status}' but no '{expected}' event found in audit_trail"
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
                    errors.append(
                        f"  audit_trail: status is '{status}' but audit_trail contains "
                        f"'{bad_event}' event — invalid state transition"
                    )



        # --- Require y_statement on accepted ADRs ---
        y_stmt = data.get("adr", {}).get("y_statement", "")
        if status in {"accepted", "superseded", "deprecated"}:
            if not y_stmt or not y_stmt.strip():
                errors.append(
                    "  'adr.y_statement' is missing or empty — required for accepted ADRs "
                    "(Zimmermann/Fairbanks Y-Statement, long form)"
                )
        elif status == "proposed":
            if not y_stmt or not y_stmt.strip():
                warnings.append(
                    "  'adr.y_statement' is missing or empty — recommended before acceptance "
                    "(will be mandatory when status changes to accepted)"
                )

        # --- Warn if schema_version is missing ---
        schema_version = data.get("adr", {}).get("schema_version", "")
        if not schema_version:
            warnings.append(
                "  'adr.schema_version' is missing — recommended per schema versioning policy (§10)"
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

        # --- Warn if confidence is set on a draft ADR ---
        if status == "draft":
            conf = decision.get("confidence", "")
            if conf:
                warnings.append(
                    f"  decision.confidence is '{conf}' but status is 'draft' — "
                    f"confidence is premature before the decision is proposed"
                )

        # --- Check decision_date within created_at → last_modified range ---
        decision_date = decision.get("decision_date", "")
        created_at = data.get("adr", {}).get("created_at", "")
        last_modified = data.get("adr", {}).get("last_modified", "")
        if decision_date and created_at:
            # Compare date strings (ISO 8601 sorts lexicographically)
            created_date = str(created_at)[:10]  # extract date portion
            if str(decision_date) < created_date:
                warnings.append(
                    f"  decision.decision_date ({decision_date}) is before "
                    f"adr.created_at ({created_date}) — decision cannot predate the ADR"
                )
        if created_at and last_modified:
            created_dt = parse_iso_datetime(str(created_at))
            last_modified_dt = parse_iso_datetime(str(last_modified))
            if created_dt and last_modified_dt and last_modified_dt < created_dt:
                warnings.append(
                    f"  adr.last_modified ({last_modified}) is earlier than "
                    f"adr.created_at ({created_at}) — modification time cannot predate creation"
                )

        # --- Check archival consistency ---
        archival = data.get("lifecycle", {}).get("archival", {})
        archived_at = archival.get("archived_at") if archival else None
        archived_events = [
            entry for entry in audit_trail
            if isinstance(entry, dict) and entry.get("event") == "archived"
        ]
        terminal_statuses = {"superseded", "deprecated", "rejected"}
        if archived_at or archived_events:
            if status and status not in terminal_statuses:
                errors.append(
                    f"  archival is recorded but adr.status is '{status}' "
                    f"— archived ADRs should have a terminal status ({', '.join(sorted(terminal_statuses))})"
                )
        if archived_at and not archived_events:
            errors.append(
                "  lifecycle.archival.archived_at is set but no 'archived' event found in audit_trail"
            )
        if archived_events and not archived_at:
            errors.append(
                "  audit_trail contains 'archived' event but lifecycle.archival.archived_at is missing"
            )

        lifecycle = data.get("lifecycle", {})
        superseded_by = lifecycle.get("superseded_by") if isinstance(lifecycle, dict) else None
        if status == "superseded" and not superseded_by:
            errors.append(
                "  adr.status is 'superseded' but lifecycle.superseded_by is missing"
            )


        # --- Check filename ↔ adr.id consistency ---
        adr_id = data.get("adr", {}).get("id", "")
        if adr_id:
            filename = filepath.stem  # e.g. "ADR-0001-dpop-over-mtls"
            if filename != adr_id:
                errors.append(
                    f"  filename '{filename}' does not exactly match adr.id '{adr_id}'"
                )

        # --- Check for collapsed code fences in description fields ---
        # YAML folded scalars (>) collapse newlines into spaces, breaking
        # fenced code blocks.  Detect "```lang content" on a single line —
        # this means the author used > when they should have used |.
        COLLAPSED_FENCE_RE = re.compile(r"```\w+[^\S\n]+\S")
        for idx, alt in enumerate(alternatives):
            if not isinstance(alt, dict):
                continue
            desc = alt.get("description", "")
            if isinstance(desc, str) and COLLAPSED_FENCE_RE.search(desc):
                alt_name = alt.get("name", f"#{idx}")
                warnings.append(
                    f"  alternatives[{idx}] '{alt_name}': description contains a collapsed "
                    f"code fence (e.g. ```mermaid graph TD on one line). "
                    f"Use YAML literal scalar (|) instead of folded scalar (>) "
                    f"for descriptions containing code blocks"
                )

        # --- Check for bare HTML tags in Markdown text fields ---
        # Bare <tag> sequences are interpreted as HTML when rendered to
        # Markdown, silently swallowing the content.  Authors must wrap
        # code references like <script setup> in backticks.
        #
        # Exempt: <br/>, <br>, and HTML entities like &lt;.
        # Strategy: strip code fences and backtick spans first, then scan.
        BARE_HTML_RE = re.compile(r"<(?!br\s*/?\s*>)([a-zA-Z][a-zA-Z0-9._-]*(?:\s[^>]*)?)>")
        CODE_FENCE_RE = re.compile(r"```[\s\S]*?```", re.MULTILINE)
        BACKTICK_SPAN_RE = re.compile(r"`[^`]+`")

        def _find_bare_html_tags(text: str) -> list[str]:
            """Return bare HTML-like tags found outside code fences/backticks."""
            if not text or not isinstance(text, str):
                return []
            stripped = CODE_FENCE_RE.sub("", text)
            stripped = BACKTICK_SPAN_RE.sub("", stripped)
            return [m.group(0) for m in BARE_HTML_RE.finditer(stripped)]

        markdown_fields: list[tuple[str, str]] = []

        # Top-level Markdown fields
        ctx = data.get("context", {})
        if isinstance(ctx, dict):
            ctx_desc = ctx.get("description", "")
            if isinstance(ctx_desc, str):
                markdown_fields.append(("context.description", ctx_desc))

        if isinstance(decision, dict):
            for field_name in ("rationale", "tradeoffs"):
                val = decision.get(field_name, "")
                if isinstance(val, str):
                    markdown_fields.append((f"decision.{field_name}", val))

        confirmation = data.get("confirmation", {})
        if isinstance(confirmation, dict):
            conf_desc = confirmation.get("description", "")
            if isinstance(conf_desc, str):
                markdown_fields.append(("confirmation.description", conf_desc))

        # Alternatives: description + pros/cons items
        for idx, alt in enumerate(alternatives):
            if not isinstance(alt, dict):
                continue
            alt_name = alt.get("name", f"#{idx}")
            desc = alt.get("description", "")
            if isinstance(desc, str):
                markdown_fields.append((f"alternatives[{idx}] '{alt_name}'.description", desc))
            for list_field in ("pros", "cons"):
                items = alt.get(list_field, [])
                if isinstance(items, list):
                    for j, item in enumerate(items):
                        if isinstance(item, str):
                            markdown_fields.append(
                                (f"alternatives[{idx}] '{alt_name}'.{list_field}[{j}]", item)
                            )

        # Audit trail details
        if audit_trail:
            for idx, entry in enumerate(audit_trail):
                if isinstance(entry, dict):
                    details = entry.get("details", "")
                    if isinstance(details, str):
                        markdown_fields.append((f"audit_trail[{idx}].details", details))

        # Consequences
        consequences = data.get("consequences", {})
        if isinstance(consequences, dict):
            for list_field in ("positive", "negative"):
                items = consequences.get(list_field, [])
                if isinstance(items, list):
                    for j, item in enumerate(items):
                        if isinstance(item, str):
                            markdown_fields.append(
                                (f"consequences.{list_field}[{j}]", item)
                            )

        for field_path, text in markdown_fields:
            bare_tags = _find_bare_html_tags(text)
            if bare_tags:
                shown = ", ".join(bare_tags[:3])
                suffix = f" (and {len(bare_tags) - 3} more)" if len(bare_tags) > 3 else ""
                errors.append(
                    f"  {field_path}: bare HTML tag(s) {shown}{suffix} — "
                    f"wrap in backticks (e.g. `<script setup>`) to prevent "
                    f"content from being swallowed when rendered to Markdown"
                )

    return errors, warnings


def validate_cross_references(
    all_data: dict[str, dict],
    primary_filepaths: set[str] | None = None,
):
    """Check cross-file referential integrity.

    Checks:
    - Lifecycle supersession symmetry
    - Duplicate ADR IDs across all files

    Args:
        all_data: mapping of filepath → parsed YAML data
        primary_filepaths: explicit validation targets; supplemental repo context
            is only used to resolve references and duplicate collisions for these
            files, not to report unrelated corpus issues.
    """
    warnings = []
    errors = []
    primary_filepaths = set(all_data) if primary_filepaths is None else set(primary_filepaths)

    # Collect all known ADR IDs and their lifecycle supersession fields.
    id_to_filepaths: dict[str, list[str]] = {}
    id_to_filepath: dict[str, str] = {}
    id_to_supersedes: dict[str, str] = {}
    id_to_superseded_by: dict[str, str] = {}
    for filepath, data in all_data.items():
        if isinstance(data, dict):
            adr_id = data.get("adr", {}).get("id", "")
            if adr_id:
                id_to_filepaths.setdefault(adr_id, []).append(filepath)
                id_to_filepath.setdefault(adr_id, filepath)
                lifecycle = data.get("lifecycle", {})
                sup = lifecycle.get("supersedes")
                sup_by = lifecycle.get("superseded_by")
                if sup:
                    id_to_supersedes[adr_id] = sup
                if sup_by:
                    id_to_superseded_by[adr_id] = sup_by

    # Check for duplicate ADR IDs, but only fail the command if an explicit
    # validation target participates in the collision.
    for adr_id, filepaths in sorted(id_to_filepaths.items()):
        if len(filepaths) <= 1 or not any(path in primary_filepaths for path in filepaths):
            continue
        first_path = filepaths[0]
        for duplicate_path in filepaths[1:]:
            errors.append(
                f"  duplicate ADR ID '{adr_id}': found in both "
                f"'{first_path}' and '{duplicate_path}'"
            )

    known_ids = set(id_to_filepaths)

    # Check supersession symmetry: if A supersedes B, B should have superseded_by A.
    for adr_id, target_id in id_to_supersedes.items():
        source_path = id_to_filepath.get(adr_id, adr_id)
        if source_path not in primary_filepaths:
            continue
        if target_id not in known_ids:
            errors.append(
                f"  {source_path}: '{adr_id}' declares lifecycle.supersedes "
                f"'{target_id}', but no ADR with id '{target_id}' was found in the validation corpus"
            )
            continue
        if target_id not in id_to_superseded_by or id_to_superseded_by[target_id] != adr_id:
            errors.append(
                f"  {source_path}: '{adr_id}' declares "
                f"lifecycle.supersedes '{target_id}', but '{target_id}' does not have "
                f"lifecycle.superseded_by '{adr_id}'"
            )

    for adr_id, target_id in id_to_superseded_by.items():
        source_path = id_to_filepath.get(adr_id, adr_id)
        if source_path not in primary_filepaths:
            continue
        if target_id not in known_ids:
            errors.append(
                f"  {source_path}: '{adr_id}' declares lifecycle.superseded_by "
                f"'{target_id}', but no ADR with id '{target_id}' was found in the validation corpus"
            )
            continue
        if target_id not in id_to_supersedes or id_to_supersedes[target_id] != adr_id:
            errors.append(
                f"  {source_path}: '{adr_id}' declares "
                f"lifecycle.superseded_by '{target_id}', but '{target_id}' does not have "
                f"lifecycle.supersedes '{adr_id}'"
            )

    return errors, warnings


def main():
    # Parse args
    args = sys.argv[1:]

    if len(args) < 1:
        print(f"Usage: {sys.argv[0]} <file_or_directory> [<file_or_directory> ...]")
        sys.exit(2)

    schema = load_schema()
    validator = build_validator(schema)

    files = collect_input_files(args)

    if not files:
        print(f"No YAML files found in: {', '.join(args)}")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0
    all_data, primary_filepaths = build_cross_reference_corpus(files)

    for filepath in files:
        errors, warnings = validate_file(filepath, validator)

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

    # Cross-file reference checks use the explicit input plus repo context when
    # the validation target is part of the governed ADR corpus.
    if all_data:
        xref_errors, xref_warnings = validate_cross_references(all_data, primary_filepaths)
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



    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
