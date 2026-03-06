#!/usr/bin/env python3
"""
Extract active Architecture Decisions from the ADL into structured formats
for use by AI agents, CI pipelines, and compliance tooling.

This script bridges the gap between the ADL (Architecture Decision Log) and
downstream enforcement: it reads ADR YAML files, filters to active decisions,
and outputs a compact representation that any tool — from grep to a full LLM —
can consume for Spec-Driven Development (SDD) and pre-merge compliance checks.

Usage:
    # Markdown summary of active decisions (default)
    python3 extract-decisions.py architecture-decision-log/

    # JSON output for programmatic consumption
    python3 extract-decisions.py --format json architecture-decision-log/

    # Generate an LLM compliance-check prompt for a code diff
    python3 extract-decisions.py --compliance-prompt --diff <(git diff main) architecture-decision-log/

    # Filter by tags
    python3 extract-decisions.py --tags oauth,security architecture-decision-log/

    # Filter by decision type
    python3 extract-decisions.py --decision-type technology architecture-decision-log/

    # Include only specific statuses (default: accepted)
    python3 extract-decisions.py --status accepted,proposed architecture-decision-log/

Requires: pip install pyyaml
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: Missing dependency. Install with:")
    print("  pip install pyyaml")
    sys.exit(2)


def load_adrs(paths: list[str]) -> list[dict]:
    """Load ADR YAML files from files and directories."""
    files = []
    for arg in paths:
        target = Path(arg)
        if target.is_file():
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(target.glob("*.yaml")))
            files.extend(sorted(target.glob("*.yml")))
        else:
            print(f"WARNING: {target} is not a file or directory — skipping",
                  file=sys.stderr)

    adrs = []
    for filepath in files:
        try:
            with open(filepath, "r") as f:
                data = yaml.safe_load(f)
            if data and isinstance(data, dict) and "adr" in data:
                data["_source_file"] = str(filepath)
                adrs.append(data)
        except yaml.YAMLError as e:
            print(f"WARNING: Failed to parse {filepath}: {e}", file=sys.stderr)
    return adrs


def filter_adrs(
    adrs: list[dict],
    statuses: set[str],
    tags: set[str] | None = None,
    decision_type: str | None = None,
) -> list[dict]:
    """Filter ADRs by status, tags, and decision type."""
    filtered = []
    for adr in adrs:
        meta = adr.get("adr", {})
        status = meta.get("status", "")
        if status not in statuses:
            continue
        if tags:
            adr_tags = set(meta.get("tags", []))
            if not tags & adr_tags:
                continue
        if decision_type and meta.get("decision_type", "") != decision_type:
            continue
        filtered.append(adr)
    return filtered


def extract_decision_summary(adr: dict) -> dict:
    """Extract a compact decision summary from a full ADR."""
    meta = adr.get("adr", {})
    decision = adr.get("decision", {})
    context = adr.get("context", {})
    consequences = adr.get("consequences", {})

    # Get rejected alternatives for contrast
    alternatives = adr.get("alternatives", [])
    chosen = decision.get("chosen_alternative", "")
    rejected = [
        {
            "name": alt.get("name", ""),
            "rejection_rationale": alt.get("rejection_rationale", ""),
        }
        for alt in alternatives
        if isinstance(alt, dict) and alt.get("name", "") != chosen
    ]

    return {
        "id": meta.get("id", ""),
        "title": meta.get("title", ""),
        "summary": meta.get("summary", ""),
        "status": meta.get("status", ""),
        "decision_type": meta.get("decision_type", ""),
        "tags": meta.get("tags", []),
        "project": meta.get("project", ""),
        "component": meta.get("component", ""),
        "confidence": decision.get("confidence", ""),
        "decision_date": decision.get("decision_date", ""),
        "chosen_alternative": chosen,
        "rationale": decision.get("rationale", ""),
        "tradeoffs": decision.get("tradeoffs", ""),
        "constraints": context.get("constraints", []),
        "rejected_alternatives": rejected,
        "consequences_positive": consequences.get("positive", []),
        "consequences_negative": consequences.get("negative", []),
    }


def format_markdown(decisions: list[dict]) -> str:
    """Format decisions as a Markdown document optimized for LLM consumption."""
    lines = [
        "# Architecture Decision Log — Active Decisions",
        "",
        f"> {len(decisions)} active decision(s) extracted from the ADL.",
        "> Use this as a source of truth for code generation, reviews, and compliance checks.",
        "",
        "---",
        "",
    ]

    for d in decisions:
        lines.append(f"## {d['id']}: {d['title']}")
        lines.append("")
        lines.append(
            f"**Status:** {d['status']} | "
            f"**Confidence:** {d.get('confidence', 'n/a')} | "
            f"**Date:** {d.get('decision_date', 'n/a')} | "
            f"**Type:** {d.get('decision_type', 'n/a')}"
        )

        if d.get("tags"):
            lines.append(f"**Tags:** {', '.join(d['tags'])}")

        if d.get("project"):
            lines.append(f"**Project:** {d['project']}")

        if d.get("component"):
            lines.append(f"**Component:** {d['component']}")

        lines.append("")

        if d.get("summary"):
            lines.append(f"**Summary:** {d['summary'].strip()}")
            lines.append("")

        lines.append(f"**Chosen Alternative:** {d['chosen_alternative']}")
        lines.append("")

        if d.get("rationale"):
            lines.append("**Rationale:**")
            lines.append(d["rationale"].strip())
            lines.append("")

        if d.get("constraints"):
            lines.append("**Constraints:**")
            for c in d["constraints"]:
                lines.append(f"- {c}")
            lines.append("")

        if d.get("tradeoffs"):
            lines.append("**Accepted Tradeoffs:**")
            lines.append(d["tradeoffs"].strip())
            lines.append("")

        if d.get("rejected_alternatives"):
            lines.append("**Rejected Alternatives:**")
            for rej in d["rejected_alternatives"]:
                rationale = rej.get("rejection_rationale", "")
                if rationale:
                    lines.append(f"- ~~{rej['name']}~~ — {rationale}")
                else:
                    lines.append(f"- ~~{rej['name']}~~")
            lines.append("")

        if d.get("consequences_positive"):
            lines.append("**Expected Outcomes:**")
            for c in d["consequences_positive"]:
                lines.append(f"- ✅ {c}")
            for c in d.get("consequences_negative", []):
                lines.append(f"- ⚠️ {c}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def format_json(decisions: list[dict]) -> str:
    """Format decisions as JSON for programmatic consumption."""
    return json.dumps(
        {"active_decisions": decisions, "count": len(decisions)},
        indent=2,
        default=str,
    )


def generate_compliance_prompt(
    decisions_md: str, diff_content: str | None = None
) -> str:
    """Generate an LLM prompt for compliance checking."""
    prompt_parts = [
        "# Architecture Decision Compliance Review",
        "",
        "You are an architecture compliance reviewer. Your job is to check whether",
        "code changes are consistent with the active Architecture Decisions listed below.",
        "",
        "## Instructions",
        "",
        "1. Read the active Architecture Decisions carefully.",
        "2. Review the code changes (diff) provided below.",
        "3. For each decision that is relevant to the changed code, assess whether",
        "   the code is **compliant**, **non-compliant**, or **not applicable**.",
        "4. If non-compliant, explain which decision is violated and what should change.",
        "5. If the code uses a *rejected* alternative, flag it explicitly.",
        "6. Consider constraints and tradeoffs — the decision was made with specific",
        "   context that may affect compliance interpretation.",
        "",
        "## Output Format",
        "",
        "For each relevant decision, output:",
        "",
        "```",
        "ADR-NNNN: <title>",
        "Status: COMPLIANT | NON-COMPLIANT | NOT APPLICABLE",
        "Explanation: <brief explanation>",
        "```",
        "",
        "If no decisions are relevant to the changes, state that explicitly.",
        "",
        "---",
        "",
        decisions_md,
    ]

    if diff_content:
        prompt_parts.extend([
            "",
            "---",
            "",
            "## Code Changes (Diff)",
            "",
            "```diff",
            diff_content.strip(),
            "```",
        ])
    else:
        prompt_parts.extend([
            "",
            "---",
            "",
            "## Code Changes",
            "",
            "*[Paste your code diff here, or pipe it via --diff]*",
        ])

    return "\n".join(prompt_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Extract active Architecture Decisions from the ADL.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Markdown summary of accepted decisions
  python3 extract-decisions.py architecture-decision-log/

  # JSON output for programmatic use
  python3 extract-decisions.py --format json architecture-decision-log/

  # Generate LLM compliance prompt with a diff
  python3 extract-decisions.py --compliance-prompt \\
    --diff <(git diff main) architecture-decision-log/

  # Filter by tags
  python3 extract-decisions.py --tags oauth,security architecture-decision-log/

  # Pipe to an LLM for automated review (example with OpenAI)
  python3 extract-decisions.py --compliance-prompt \\
    --diff <(git diff main) architecture-decision-log/ | \\
    llm -m gpt-4o "Review this for compliance"
        """,
    )

    parser.add_argument(
        "paths",
        nargs="+",
        help="ADR YAML files or directories containing them",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--status",
        default="accepted",
        help="Comma-separated statuses to include (default: accepted)",
    )
    parser.add_argument(
        "--tags",
        default=None,
        help="Comma-separated tags to filter by (decisions must match at least one)",
    )
    parser.add_argument(
        "--decision-type",
        default=None,
        choices=["technology", "process", "organizational", "vendor",
                 "security", "compliance"],
        help="Filter by decision type",
    )
    parser.add_argument(
        "--compliance-prompt",
        action="store_true",
        help="Generate an LLM compliance-check prompt instead of raw extraction",
    )
    parser.add_argument(
        "--diff",
        default=None,
        help="Path to a diff file to include in the compliance prompt",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    # Parse filter arguments
    statuses = set(args.status.split(","))
    tags = set(args.tags.split(",")) if args.tags else None

    # Load and filter ADRs
    adrs = load_adrs(args.paths)
    if not adrs:
        print("No ADR files found.", file=sys.stderr)
        sys.exit(0)

    filtered = filter_adrs(adrs, statuses, tags, args.decision_type)
    if not filtered:
        print(
            f"No ADRs match filters (status={statuses}, tags={tags}, "
            f"decision_type={args.decision_type}). "
            f"Total ADRs loaded: {len(adrs)}.",
            file=sys.stderr
        )
        sys.exit(0)

    # Extract summaries
    decisions = [extract_decision_summary(adr) for adr in filtered]

    # Format output
    if args.compliance_prompt:
        decisions_md = format_markdown(decisions)
        diff_content = None
        if args.diff:
            diff_path = Path(args.diff)
            if diff_path.exists():
                diff_content = diff_path.read_text()
            else:
                # Try reading from stdin-like path (e.g., /dev/fd/63 from
                # process substitution)
                try:
                    with open(args.diff, "r") as f:
                        diff_content = f.read()
                except OSError:
                    print(
                        f"WARNING: Could not read diff from {args.diff}",
                        file=sys.stderr
                    )
        output = generate_compliance_prompt(decisions_md, diff_content)
    elif args.format == "json":
        output = format_json(decisions)
    else:
        output = format_markdown(decisions)

    # Write output
    if args.output:
        Path(args.output).write_text(output)
        print(
            f"Wrote {len(decisions)} decision(s) to {args.output}",
            file=sys.stderr
        )
    else:
        print(output)


if __name__ == "__main__":
    main()
