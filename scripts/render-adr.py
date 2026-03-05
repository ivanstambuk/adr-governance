#!/usr/bin/env python3
"""Render ADR YAML files to Markdown documents.

Usage:
    python3 scripts/render-adr.py examples/ADR-0001-*.yaml
    python3 scripts/render-adr.py examples/           # render all in directory
    python3 scripts/render-adr.py --output-dir out/ examples/ADR-0001-*.yaml
"""

import argparse
import os
import sys

import yaml


def render_adr(data: dict) -> str:
    """Render a parsed ADR YAML dict to a Markdown string."""
    lines = []

    adr = data.get("adr", {})
    title = adr.get("title", "Untitled")
    adr_id = adr.get("id", "ADR-????")

    # --- Header ---
    lines.append(f"# {adr_id}: {title}")
    lines.append("")

    # Metadata table
    status = adr.get("status", "unknown")
    priority = adr.get("priority", "—")
    decision_type = adr.get("decision_type", "—")
    confidence = data.get("decision", {}).get("confidence", "—")
    decision_date = data.get("decision", {}).get("decision_date", "—")
    owner = data.get("decision_owner", {})
    owner_str = f"{owner.get('name', '—')} ({owner.get('role', '')})" if owner else "—"

    lines.append(f"> **Status:** `{status}` · **Priority:** `{priority}` · **Type:** `{decision_type}` · **Confidence:** `{confidence}`")
    lines.append(f"> **Decision Owner:** {owner_str} · **Decision Date:** {decision_date}")
    lines.append("")

    # Summary (elevator pitch)
    if adr.get("summary"):
        lines.append(f"*{adr['summary'].strip()}*")
        lines.append("")

    # --- Authors & Reviewers ---
    authors = data.get("authors", [])
    reviewers = data.get("reviewers", [])
    approvals = data.get("approvals", [])
    if authors or reviewers:
        lines.append("---")
        lines.append("")
        if authors:
            lines.append(f"**Authors:** {', '.join(a.get('name', '') + ' (' + a.get('role', '') + ')' for a in authors)}")
        if reviewers:
            lines.append(f"**Reviewers:** {', '.join(r.get('name', '') + ' (' + r.get('role', '') + ')' for r in reviewers)}")
        if approvals:
            approved = [a for a in approvals if a.get("approved_at")]
            if approved:
                lines.append(f"**Approvals:** {', '.join(a.get('name', '') + ' (' + str(a.get('approved_at', '')) + ')' for a in approved)}")
        lines.append("")

    # --- Context ---
    context = data.get("context", {})
    lines.append("---")
    lines.append("")
    lines.append("## Context")
    lines.append("")
    if context.get("summary"):
        lines.append(context["summary"].strip())
        lines.append("")

    for section_key, section_title in [("business_drivers", "Business Drivers"), ("technical_drivers", "Technical Drivers"),
                                        ("constraints", "Constraints"), ("assumptions", "Assumptions")]:
        items = context.get(section_key, [])
        if items:
            lines.append(f"### {section_title}")
            lines.append("")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

    # --- Requirements ---
    reqs = data.get("requirements", {})
    functional = reqs.get("functional", [])
    non_functional = reqs.get("non_functional", [])
    if functional or non_functional:
        lines.append("## Requirements")
        lines.append("")
        if functional:
            lines.append("### Functional")
            lines.append("")
            lines.append("| ID | Description |")
            lines.append("|----|-------------|")
            for r in functional:
                lines.append(f"| `{r.get('id', '')}` | {r.get('description', '')} |")
            lines.append("")
        if non_functional:
            lines.append("### Non-Functional")
            lines.append("")
            lines.append("| ID | Description |")
            lines.append("|----|-------------|")
            for r in non_functional:
                lines.append(f"| `{r.get('id', '')}` | {r.get('description', '')} |")
            lines.append("")

    # --- Alternatives ---
    alternatives = data.get("alternatives", [])
    if alternatives:
        lines.append("## Alternatives Considered")
        lines.append("")
        decision = data.get("decision", {})
        chosen = decision.get("chosen_alternative", "")

        for i, alt in enumerate(alternatives, 1):
            name = alt.get("name", f"Option {i}")
            is_chosen = name == chosen
            marker = " ✅" if is_chosen else ""
            lines.append(f"### {i}. {name}{marker}")
            lines.append("")
            if alt.get("summary"):
                lines.append(alt["summary"].strip())
                lines.append("")
            if alt.get("pros"):
                lines.append("**Pros:**")
                for p in alt["pros"]:
                    lines.append(f"- {p}")
                lines.append("")
            if alt.get("cons"):
                lines.append("**Cons:**")
                for c in alt["cons"]:
                    lines.append(f"- {c}")
                lines.append("")
            cost = alt.get("estimated_cost", "")
            risk = alt.get("risk", "")
            if cost or risk:
                lines.append(f"*Estimated cost: `{cost}` · Risk: `{risk}`*")
                lines.append("")
            if alt.get("rejection_rationale"):
                lines.append(f"> **Rejection rationale:** {alt['rejection_rationale'].strip()}")
                lines.append("")

    # --- Decision ---
    decision = data.get("decision", {})
    if decision:
        lines.append("## Decision")
        lines.append("")
        lines.append(f"**Chosen alternative:** {decision.get('chosen_alternative', '—')}")
        lines.append("")
        if decision.get("rationale"):
            lines.append("### Rationale")
            lines.append("")
            lines.append(decision["rationale"].strip())
            lines.append("")
        if decision.get("tradeoffs"):
            lines.append("### Tradeoffs")
            lines.append("")
            lines.append(decision["tradeoffs"].strip())
            lines.append("")

    # --- Consequences ---
    consequences = data.get("consequences", {})
    positive = consequences.get("positive", [])
    negative = consequences.get("negative", [])
    if positive or negative:
        lines.append("## Consequences")
        lines.append("")
        if positive:
            lines.append("### Positive")
            lines.append("")
            for item in positive:
                lines.append(f"- {item}")
            lines.append("")
        if negative:
            lines.append("### Negative")
            lines.append("")
            for item in negative:
                lines.append(f"- {item}")
            lines.append("")

    # --- Confirmation ---
    confirmation = data.get("confirmation", {})
    if confirmation:
        lines.append("## Confirmation")
        lines.append("")
        if confirmation.get("description"):
            lines.append(confirmation["description"].strip())
            lines.append("")
        if confirmation.get("artifact_ids"):
            lines.append("**Artifacts:**")
            for aid in confirmation["artifact_ids"]:
                if aid.startswith("http"):
                    lines.append(f"- [{aid}]({aid})")
                else:
                    lines.append(f"- `{aid}`")
            lines.append("")

    # --- Risk Assessment ---
    risk_assessment = data.get("risk_assessment", {})
    risks = risk_assessment.get("risks", [])
    if risks:
        lines.append("## Risk Assessment")
        lines.append("")
        lines.append("| ID | Description | Likelihood | Impact |")
        lines.append("|----|-------------|------------|--------|")
        for r in risks:
            lines.append(f"| `{r.get('id', '')}` | {r.get('description', '')} | {r.get('likelihood', '')} | {r.get('impact', '')} |")
        lines.append("")
        for r in risks:
            mitigations = r.get("mitigation", [])
            if mitigations:
                lines.append(f"**{r.get('id', '')} mitigations:**")
                for m in mitigations:
                    lines.append(f"- {m}")
                lines.append("")
        residual = risk_assessment.get("residual_risk", "")
        if residual:
            lines.append(f"**Residual risk:** `{residual}`")
            lines.append("")

    # --- Dependencies ---
    deps = data.get("dependencies", {})
    internal = deps.get("internal", [])
    external = deps.get("external", [])
    if internal or external:
        lines.append("## Dependencies")
        lines.append("")
        if internal:
            lines.append("**Internal:**")
            for d in internal:
                lines.append(f"- {d}")
            lines.append("")
        if external:
            lines.append("**External:**")
            for d in external:
                lines.append(f"- {d}")
            lines.append("")

    # --- References ---
    refs = data.get("references", [])
    if refs:
        lines.append("## References")
        lines.append("")
        for r in refs:
            title = r.get("title", "")
            url = r.get("url", "")
            lines.append(f"- [{title}]({url})")
        lines.append("")

    # --- Lifecycle ---
    lifecycle = data.get("lifecycle", {})
    if lifecycle:
        lines.append("## Lifecycle")
        lines.append("")
        review = lifecycle.get("review_cycle_months")
        next_review = lifecycle.get("next_review_date")
        sup_by = lifecycle.get("superseded_by")
        sup = lifecycle.get("supersedes")
        if review:
            lines.append(f"- **Review cycle:** {review} months")
        if next_review:
            lines.append(f"- **Next review:** {next_review}")
        if sup_by:
            lines.append(f"- **Superseded by:** {sup_by}")
        if sup:
            lines.append(f"- **Supersedes:** {sup}")
        lines.append("")

    # --- Audit Trail ---
    audit_trail = data.get("audit_trail", [])
    if audit_trail:
        lines.append("## Audit Trail")
        lines.append("")
        lines.append("| Event | By | Date | Details |")
        lines.append("|-------|----|------|---------|")
        for e in audit_trail:
            event = e.get("event", "")
            by = e.get("by", "")
            at = str(e.get("at", ""))[:10]  # date portion only
            details = e.get("details", "")
            lines.append(f"| `{event}` | {by} | {at} | {details} |")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Render ADR YAML files to Markdown")
    parser.add_argument("targets", nargs="+", help="YAML files or directories to render")
    parser.add_argument("--output-dir", "-o", help="Output directory (default: print to stdout)")
    args = parser.parse_args()

    # Collect files
    files = []
    for target in args.targets:
        if os.path.isdir(target):
            for f in sorted(os.listdir(target)):
                if f.endswith((".yaml", ".yml")):
                    files.append(os.path.join(target, f))
        elif os.path.isfile(target):
            files.append(target)
        else:
            print(f"WARNING: {target} not found, skipping", file=sys.stderr)

    if not files:
        print("No YAML files found.", file=sys.stderr)
        sys.exit(1)

    for filepath in files:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict) or "adr" not in data:
            print(f"SKIP: {filepath} (not an ADR file)", file=sys.stderr)
            continue

        markdown = render_adr(data)

        if args.output_dir:
            os.makedirs(args.output_dir, exist_ok=True)
            basename = os.path.splitext(os.path.basename(filepath))[0] + ".md"
            output_path = os.path.join(args.output_dir, basename)
            with open(output_path, "w") as f:
                f.write(markdown)
            print(f"  RENDERED: {filepath} → {output_path}")
        else:
            print(markdown)
            if len(files) > 1:
                print("\n" + "=" * 72 + "\n")


if __name__ == "__main__":
    main()
