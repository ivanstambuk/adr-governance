#!/usr/bin/env python3
"""
Pre-review quality gate for ADR YAML files.

Generates an LLM prompt that performs a Socratic review of an ADR draft,
probing for ambiguities, weak rationale, missing edge cases, and semantic
inconsistencies — before the ADR reaches a human reviewer.

This shifts review effort left: the proposer works with an AI assistant
through iterative refinement until the ADR is clear, complete, and
internally consistent. Human reviewers then focus on strategic judgement
rather than catching omissions.

Usage:
    # Generate a review prompt for a single ADR (pipe to your LLM)
    python3 review-adr.py architecture-decision-log/ADR-0001.yaml

    # Review with additional context from related ADRs
    python3 review-adr.py --context-from architecture-decision-log/ \
        architecture-decision-log/ADR-0001.yaml

    # Output the prompt to a file
    python3 review-adr.py -o review-prompt.md architecture-decision-log/ADR-0001.yaml

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
        print(f"ERROR: {filepath} is not a valid ADR file", file=sys.stderr)
        sys.exit(1)
    return data


def load_context_adrs(paths: list[str], exclude: str) -> list[dict]:
    """Load ADRs from directories for cross-reference context."""
    adrs = []
    for arg in paths:
        target = Path(arg)
        if target.is_dir():
            for f in sorted(target.glob("*.yaml")):
                if str(f) == exclude:
                    continue
                try:
                    with open(f, "r") as fh:
                        data = yaml.safe_load(fh)
                    if data and isinstance(data, dict) and "adr" in data:
                        adrs.append(data)
                except yaml.YAMLError:
                    pass
        elif target.is_file() and str(target) != exclude:
            try:
                with open(target, "r") as fh:
                    data = yaml.safe_load(fh)
                if data and isinstance(data, dict) and "adr" in data:
                    adrs.append(data)
            except yaml.YAMLError:
                pass
    return adrs


def format_adr_for_review(data: dict) -> str:
    """Format the full ADR YAML as a readable block for the prompt."""
    return yaml.dump(data, default_flow_style=False, allow_unicode=True,
                     width=200, sort_keys=False)


def format_context_summaries(context_adrs: list[dict]) -> str:
    """Format related ADRs as brief summaries for cross-reference."""
    if not context_adrs:
        return ""

    lines = [
        "",
        "## Existing Decisions (Cross-Reference Context)",
        "",
        "The following decisions already exist in the ADL. Check the reviewed ADR",
        "for consistency, conflicts, or dependencies with these:",
        "",
    ]
    for adr in context_adrs:
        meta = adr.get("adr", {})
        decision = adr.get("decision", {})
        adr_id = meta.get("id", "?")
        title = meta.get("title", "?")
        status = meta.get("status", "?")
        chosen = decision.get("chosen_alternative", "?")
        summary = meta.get("summary", "")

        lines.append(f"### {adr_id}: {title}")
        lines.append(f"**Status:** {status} | **Chosen:** {chosen}")
        if summary:
            lines.append(f"**Summary:** {summary}")
        lines.append("")

    return "\n".join(lines)


def generate_review_prompt(
    adr_yaml: str, context_section: str = ""
) -> str:
    """Generate the Socratic review prompt."""
    return f"""# ADR Semantic Review — Pre-Reviewer Quality Gate

You are an Architecture Review Board member performing a **Socratic review**
of the ADR draft below. Your goal is to ensure the ADR is clear, complete,
and internally consistent **before** it reaches human reviewers.

## Your Review Approach

You must be thorough but constructive. For each issue you find, explain
*why* it matters and suggest a concrete improvement. Organize your feedback
into the following categories:

### 1. Semantic Clarity
- Is the problem statement (`context.summary`) unambiguous? Could two readers
  interpret it differently?
- Does the rationale clearly connect the chosen alternative to the stated
  drivers and constraints?
- Are there vague terms ("scalable", "performant", "modern") that need
  quantification or definition?
- Would a new team member understand this decision without additional context?

### 2. Completeness
- Are all required sections substantive (not just template placeholders)?
- Does each alternative have **balanced** pros and cons? (Watch for strawman
  alternatives with 1 pro and 5 cons.)
- Are constraints realistic and testable? (e.g., "low latency" → "< 10ms p99")
- Are negative consequences acknowledged honestly?
- Is the `confirmation.description` actionable — does it describe *how*
  compliance will be verified?
- Is the `adr.y_statement` a compelling elevator pitch that enables stakeholder
  triage without reading the full ADR?

### 3. Logical Consistency
- Does `decision.chosen_alternative` match an entry in `alternatives[].name`?
- Is the `decision.rationale` consistent with the pros/cons listed?
- Do the `consequences.negative` entries align with the cons of the chosen
  alternative?
- Are `audit_trail` events consistent with the `adr.status`?
- If `lifecycle.supersedes` is set, is there a valid supersession chain?

### 4. Assumption Risks
- Are assumptions (`context.assumptions`) explicitly stated?
- What happens if an assumption is wrong? Is that risk captured?
- Are there unstated assumptions hiding in the rationale?

### 5. Missing Perspectives
- Are there stakeholders who should be listed as reviewers but aren't?
- Are there alternatives that weren't considered but should be?
- Are there regulatory, compliance, or security implications not addressed?
- Would the rejected alternatives' teams agree with the `rejection_rationale`?

### 6. Cross-Reference Consistency
- Does this decision conflict with any existing decisions in the ADL?
- Does it create new dependencies that should be tracked?
- If it supersedes an existing decision, is the migration path clear?

## Output Format

Structure your review as:

```
## Summary Verdict
[READY FOR REVIEW | NEEDS REWORK | MAJOR GAPS]
Brief overall assessment (2-3 sentences).

## Issues Found

### [Category]: [Issue Title]
**Severity:** HIGH | MEDIUM | LOW
**Location:** [field path, e.g., decision.rationale]
**Issue:** [what's wrong]
**Suggestion:** [concrete improvement]

(repeat for each issue)

## Strengths
- [what the ADR does well — always include at least 2]

## Open Questions for the Proposer
1. [questions that the proposer should answer before submitting for review]
```

---

## ADR Under Review

```yaml
{adr_yaml}
```
{context_section}
---

Now perform your review. Be rigorous but fair — the goal is to help the
proposer strengthen the ADR before it reaches human reviewers.
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate an LLM semantic review prompt for an ADR.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Review a single ADR (prints prompt to stdout — pipe to your LLM)
  python3 review-adr.py architecture-decision-log/ADR-0001.yaml

  # Review with cross-reference context from the full ADL
  python3 review-adr.py --context-from architecture-decision-log/ \\
      architecture-decision-log/ADR-0009.yaml

  # Pipe to an LLM
  python3 review-adr.py architecture-decision-log/ADR-0009.yaml | \\
      llm -m gpt-4o

  # Save prompt to file
  python3 review-adr.py -o review.md architecture-decision-log/ADR-0009.yaml
        """,
    )

    parser.add_argument(
        "adr_file",
        help="Path to the ADR YAML file to review",
    )
    parser.add_argument(
        "--context-from",
        nargs="*",
        default=[],
        help="Directories or files containing related ADRs for cross-reference context",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    # Load the target ADR
    adr_path = Path(args.adr_file)
    if not adr_path.exists():
        print(f"ERROR: {adr_path} not found", file=sys.stderr)
        sys.exit(1)

    adr_data = load_adr(adr_path)
    adr_yaml = format_adr_for_review(adr_data)

    # Load context ADRs
    context_section = ""
    if args.context_from:
        context_adrs = load_context_adrs(args.context_from, str(adr_path))
        context_section = format_context_summaries(context_adrs)

    # Generate the prompt
    prompt = generate_review_prompt(adr_yaml, context_section)

    # Output
    if args.output:
        Path(args.output).write_text(prompt)
        meta = adr_data.get("adr", {})
        print(
            f"Review prompt for {meta.get('id', '?')} written to {args.output}",
            file=sys.stderr
        )
    else:
        print(prompt)


if __name__ == "__main__":
    main()
