#!/usr/bin/env python3
"""Summarize ADR YAML files for stakeholder communication.

Produces concise, skimmable summaries designed for email or chat — not the
full decision document. Points readers to the rendered Markdown or YAML
source for the complete record.

Usage:
    # Email-length summary (default)
    python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml

    # Ultra-short chat summary (Slack/Teams)
    python3 scripts/summarize-adr.py --format chat architecture-decision-log/ADR-0001.yaml

    # Summarize multiple ADRs (e.g., after a review session)
    python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml \
        architecture-decision-log/ADR-0002.yaml

    # All ADRs in a directory
    python3 scripts/summarize-adr.py architecture-decision-log/

    # Save to file
    python3 scripts/summarize-adr.py -o summary.md architecture-decision-log/ADR-0001.yaml

Requires: pip install pyyaml
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: Missing dependency. Install with:")
    print("  pip install pyyaml")
    sys.exit(2)


def load_adr(filepath: Path) -> dict:
    """Load a single ADR YAML file."""
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    if not data or not isinstance(data, dict) or "adr" not in data:
        return {}
    return data


def summarize_email(data: dict, source_path: str = "") -> str:
    """Produce an email-length stakeholder summary.

    Designed to be pasted into an email or document after a meeting.
    Covers: what was decided, why, what alternatives were considered,
    key tradeoffs, and what happens next.
    """
    adr = data.get("adr", {})
    context = data.get("context", {})
    decision = data.get("decision", {})
    alternatives = data.get("alternatives", [])
    consequences = data.get("consequences", {})
    confirmation = data.get("confirmation", {})
    owner = data.get("decision_owner", {})

    adr_id = adr.get("id", "ADR-????")
    title = adr.get("title", "Untitled")
    status = adr.get("status", "unknown")
    priority = adr.get("priority", "—")
    decision_date = decision.get("decision_date", "—")
    confidence = decision.get("confidence", "—")
    chosen = decision.get("chosen_alternative", "—")
    owner_name = owner.get("name", "—")
    owner_role = owner.get("role", "")

    lines = []

    # Header
    lines.append(f"## {adr_id}: {title}")
    lines.append("")
    lines.append(f"**Status:** `{status}` · **Priority:** `{priority}` · "
                 f"**Confidence:** `{confidence}` · **Date:** {decision_date}")
    lines.append(f"**Decision Owner:** {owner_name}" +
                 (f" ({owner_role})" if owner_role else ""))
    lines.append("")

    # Summary / elevator pitch
    summary = adr.get("description", "")
    if summary:
        lines.append(f"> {summary.strip()}")
        lines.append("")

    # What was decided
    lines.append(f"**Decision:** {chosen}")
    lines.append("")

    # Brief rationale (first meaningful paragraph only)
    rationale = decision.get("rationale", "")
    if rationale:
        rationale_text = rationale.strip()
        # Take the first paragraph or first 3 lines, whichever is shorter
        paragraphs = rationale_text.split("\n\n")
        first_para = paragraphs[0].strip()
        # If it's a bullet list, take up to 3 bullets
        if first_para.startswith("-") or first_para.startswith("*"):
            bullet_lines = [l for l in first_para.split("\n") if l.strip()][:3]
            first_para = "\n".join(bullet_lines)
            if len([l for l in rationale_text.split("\n") if l.strip()]) > 3:
                first_para += "\n- *(…more in full document)*"
        lines.append("**Why:**")
        lines.append(first_para)
        lines.append("")

    # Alternatives considered (one-liner each)
    if alternatives:
        lines.append("**Alternatives considered:**")
        for alt in alternatives:
            name = alt.get("name", "?")
            is_chosen = name == chosen
            marker = " ✅" if is_chosen else ""
            risk = alt.get("risk", "")
            cost = alt.get("estimated_cost", "")
            rejection = alt.get("rejection_rationale", "")

            parts = [f"- **{name}**{marker}"]
            meta = []
            if cost:
                meta.append(f"cost: {cost}")
            if risk:
                meta.append(f"risk: {risk}")
            if meta:
                parts.append(f"({', '.join(meta)})")
            if rejection and not is_chosen:
                # Truncate rejection rationale to first sentence
                first_sentence = rejection.strip().split(". ")[0]
                if not first_sentence.endswith("."):
                    first_sentence += "."
                parts.append(f"— *{first_sentence}*")

            lines.append(" ".join(parts))
        lines.append("")

    # Key tradeoffs
    tradeoffs = decision.get("tradeoffs", "")
    if tradeoffs:
        tradeoff_text = tradeoffs.strip()
        # Take first 3 lines/bullets
        tradeoff_lines = [l for l in tradeoff_text.split("\n") if l.strip()][:3]
        lines.append("**Key tradeoffs:**")
        for tl in tradeoff_lines:
            if not tl.startswith("-") and not tl.startswith("*"):
                tl = f"- {tl}"
            lines.append(tl)
        lines.append("")

    # Consequences (top positive + negative)
    positive = consequences.get("positive", [])
    negative = consequences.get("negative", [])
    if positive or negative:
        lines.append("**Impact:**")
        for item in positive[:2]:
            lines.append(f"- ✅ {item}")
        for item in negative[:2]:
            lines.append(f"- ⚠️ {item}")
        lines.append("")

    # What happens next
    if confirmation.get("description"):
        lines.append(f"**Next steps:** {confirmation['description'].strip()}")
        lines.append("")

    # Source link
    if source_path:
        lines.append(f"📄 *Full decision: [{source_path}]({source_path})*")
        lines.append("")

    return "\n".join(lines)


def summarize_chat(data: dict, source_path: str = "") -> str:
    """Produce an ultra-short chat summary (Slack/Teams).

    3-5 lines maximum. Just the headline, the decision, and a link.
    """
    adr = data.get("adr", {})
    decision = data.get("decision", {})
    consequences = data.get("consequences", {})

    adr_id = adr.get("id", "ADR-????")
    title = adr.get("title", "Untitled")
    status = adr.get("status", "unknown")
    chosen = decision.get("chosen_alternative", "—")
    decision_date = decision.get("decision_date", "—")

    lines = []
    lines.append(f"**{adr_id}: {title}**")

    summary = adr.get("description", "")
    if summary:
        # First sentence only
        first_sentence = summary.strip().split(". ")[0]
        if not first_sentence.endswith("."):
            first_sentence += "."
        lines.append(first_sentence)

    lines.append(f"→ **{chosen}** (`{status}`, {decision_date})")

    # One positive, one negative consequence
    positive = consequences.get("positive", [])
    negative = consequences.get("negative", [])
    if positive:
        lines.append(f"  ✅ {positive[0]}")
    if negative:
        lines.append(f"  ⚠️ {negative[0]}")

    if source_path:
        lines.append(f"📄 {source_path}")

    return "\n".join(lines)


def summarize_digest(entries: list[tuple[dict, str]]) -> str:
    """Produce a multi-ADR digest — a meeting recap or batch summary.

    One section per ADR, designed for stakeholders who missed the meeting.
    """
    lines = []
    lines.append("# Architecture Decision Digest")
    lines.append("")
    lines.append(f"*{len(entries)} decision(s) summarized below.*")
    lines.append("")
    lines.append("---")
    lines.append("")

    for data, source_path in entries:
        lines.append(summarize_email(data, source_path))
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def collect_files(targets: list[str]) -> list[Path]:
    """Collect ADR YAML files from targets (files and/or directories)."""
    files = []
    for target in targets:
        p = Path(target)
        if p.is_dir():
            for f in sorted(p.glob("*.yaml")):
                files.append(f)
            for f in sorted(p.glob("*.yml")):
                files.append(f)
        elif p.is_file():
            files.append(p)
        else:
            print(f"WARNING: {target} not found, skipping", file=sys.stderr)
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Summarize ADR YAML files for stakeholder communication.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # Email summary (default)
  python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml

  # Chat summary (Slack/Teams — ultra-short)
  python3 scripts/summarize-adr.py --format chat architecture-decision-log/ADR-0001.yaml

  # Digest of multiple ADRs (after a review session)
  python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml \\
      architecture-decision-log/ADR-0002.yaml

  # All ADRs in a directory
  python3 scripts/summarize-adr.py architecture-decision-log/

  # Save to file
  python3 scripts/summarize-adr.py -o summary.md architecture-decision-log/ADR-0001.yaml
        """,
    )

    parser.add_argument(
        "targets",
        nargs="+",
        help="ADR YAML files or directories to summarize",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["email", "chat"],
        default="email",
        help="Summary format: 'email' (default, ~10–15 lines) or 'chat' (3–5 lines for Slack/Teams)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    files = collect_files(args.targets)
    if not files:
        print("No YAML files found.", file=sys.stderr)
        sys.exit(1)

    # Load all ADRs
    entries = []
    for filepath in files:
        data = load_adr(filepath)
        if not data:
            print(f"SKIP: {filepath} (not an ADR file)", file=sys.stderr)
            continue
        entries.append((data, str(filepath)))

    if not entries:
        print("No valid ADR files found.", file=sys.stderr)
        sys.exit(1)

    # Generate output
    if len(entries) == 1 and args.format == "email":
        output = summarize_email(entries[0][0], entries[0][1])
    elif len(entries) == 1 and args.format == "chat":
        output = summarize_chat(entries[0][0], entries[0][1])
    elif args.format == "chat":
        # Multiple ADRs in chat format — one per block
        blocks = []
        for data, path in entries:
            blocks.append(summarize_chat(data, path))
        output = "\n\n---\n\n".join(blocks)
    else:
        # Multiple ADRs — produce a digest
        output = summarize_digest(entries)

    # Output
    if args.output:
        Path(args.output).write_text(output)
        print(f"Summary written to {args.output} ({len(entries)} ADR(s))", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
