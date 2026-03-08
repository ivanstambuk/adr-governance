#!/usr/bin/env python3
"""
Triple-LLM Testing Harness for ADR Governance Framework.

Orchestrates a conversation between an Interviewer LLM (playing the ADR authoring
skill) and a User LLM (simulating a developer with a scenario), then validates
the produced ADR and runs an Analyst LLM pass for quality scoring.

End-to-end flow:

    ┌──────────────┐
    │   Scenario   │  fictional-001.yaml, fictional-002.yaml, ...
    │   (YAML)     │  defines persona, context, difficulty
    └──────┬───────┘
           │
           ▼
    ┌──────────────────────────────────────────────┐
    │          Conversation Loop (≤30 turns)        │
    │                                              │
    │   ┌─────────────┐    question    ┌─────────┐ │
    │   │ Interviewer  │──────────────▶│  User   │ │
    │   │ (GPT-5.2)    │◀─────────────│ (GLM-5) │ │
    │   │ + ADR Bundle │    answer     │+Persona │ │
    │   └──────┬───────┘               └─────────┘ │
    │          │                                    │
    │          │ produces YAML                      │
    │          ▼                                    │
    │   ┌──────────────────┐                       │
    │   │ Chunked YAML     │  If output truncated: │
    │   │ Collection       │  Part 2 → alts        │
    │   │ (≤3 parts)       │  Part 3 → decision    │
    │   └──────┬───────────┘                       │
    └──────────┼───────────────────────────────────┘
               │
               ▼
    ┌──────────────────┐     ┌──────────────────┐
    │ Schema Validator │────▶│ Analyst LLM      │
    │ (validate-adr.py)│     │ (GPT-5.4-high)   │
    │ + review-adr.py  │     │ scores quality    │
    └──────────────────┘     └────────┬─────────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │  Run Report   │
                              │  (JSON + MD)  │
                              └───────────────┘

Usage:
    python3 tests/llm_harness.py --scenario tests/scenarios/fictional-001-api-versioning.yaml
    python3 tests/llm_harness.py --all
    python3 tests/llm_harness.py --scenario tests/scenarios/fictional-001-api-versioning.yaml \\
        --interviewer gpt-5.2-high --user glm-5 --analyst gpt-5.4-high
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]

LITELLM_BASE_URL = os.environ["LITELLM_BASE_URL"]
LITELLM_API_KEY = os.environ["LITELLM_API_KEY"]

DEFAULT_INTERVIEWER_MODEL = "gpt-5.2-medium"
DEFAULT_USER_MODEL = "glm-5"
DEFAULT_ANALYST_MODEL = "gpt-5.4-high"

MAX_TURNS = 30                  # safety cap
YAML_PRESSURE_TURN = 15         # inject "generate YAML now" at this turn
STALL_THRESHOLD = 3             # consecutive short responses before forcing YAML
INTER_RUN_DELAY_SECONDS = 5
MAX_RETRIES_ON_429 = 3

TEMPERATURE_CONFIG = {
    "interviewer": 0.7,
    "user": 0.3,
    "analyst": 0.3,
}

SCENARIOS_DIR = REPO_ROOT / "tests" / "scenarios"
RUNS_DIR = REPO_ROOT / "tests" / "llm_runs"

# Bundle components for the interviewer system prompt
BUNDLE_FILES = {
    "default": [
        REPO_ROOT / "repomix-instruction.md",
        REPO_ROOT / "schemas" / "adr.schema.json",
        REPO_ROOT / "examples-reference" / "ADR-0001-dpop-over-mtls-for-sender-constrained-tokens.yaml",
    ],
    "minimal": [
        REPO_ROOT / "repomix-instruction.md",
        REPO_ROOT / "schemas" / "adr.schema.json",
    ],
    "full": [
        REPO_ROOT / "adr-governance-bundle.md",
    ],
}


# ---------------------------------------------------------------------------
# LLM Client (uses openai SDK pointing at LiteLLM proxy)
# ---------------------------------------------------------------------------

def get_openai_client():
    """Get an OpenAI client configured for the LiteLLM proxy."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai")
        sys.exit(1)

    return OpenAI(
        base_url=LITELLM_BASE_URL,
        api_key=LITELLM_API_KEY,
    )


class ContextOverflowError(Exception):
    """Raised when the context window is exceeded."""
    pass


def chat_completion(
    client,
    model: str,
    messages: list[dict],
    temperature: float,
    max_retries: int = MAX_RETRIES_ON_429,
) -> dict:
    """
    Call the LLM with retry logic for 429 errors.
    Returns a dict with 'content', 'usage', and 'model'.
    Raises ContextOverflowError for context window / bad request errors.
    """
    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=32000,
            )
            choice = response.choices[0]
            return {
                "content": choice.message.content or "",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0,
                },
                "model": response.model or model,
                "finish_reason": choice.finish_reason,
            }
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "rate" in err_str.lower():
                wait = (2 ** attempt) * 5
                print(f"  ⏳ Rate limited (attempt {attempt + 1}/{max_retries + 1}), "
                      f"waiting {wait}s...")
                time.sleep(wait)
            elif any(code in err_str for code in ("500", "502", "503")):
                wait = (2 ** attempt) * 5
                print(f"  ⚠️  Server error (attempt {attempt + 1}/{max_retries + 1}), "
                      f"waiting {wait}s...")
                time.sleep(wait)
            elif "400" in err_str or "context" in err_str.lower() or "prompt" in err_str.lower():
                raise ContextOverflowError(
                    f"Context window overflow or bad request for {model}: {err_str[:200]}"
                )
            else:
                raise
    raise RuntimeError(f"Failed after {max_retries + 1} attempts due to rate limiting")


# ---------------------------------------------------------------------------
# Bundle / Prompt Construction
# ---------------------------------------------------------------------------

def load_bundle(variant: str = "default") -> str:
    """Load and concatenate bundle files for the interviewer system prompt."""
    files = BUNDLE_FILES.get(variant, BUNDLE_FILES["default"])
    parts = []
    for f in files:
        if f.exists():
            parts.append(f"<!-- FILE: {f.name} -->\n{f.read_text()}")
        else:
            print(f"  ⚠️  Bundle file not found: {f}")
    return "\n\n---\n\n".join(parts)


def build_user_system_prompt(scenario: dict) -> str:
    """Build the User LLM system prompt from a scenario definition."""
    persona = scenario["persona"]
    project = scenario["project"]
    ctx = scenario["decision_context"]
    behavior = scenario["user_behavior"]

    evasion_instructions = ""
    if behavior.get("evasion_points"):
        evasion_list = "\n".join(f"  - {e}" for e in behavior["evasion_points"])
        evasion_instructions = f"""
When asked about the following topics, be initially vague or evasive. Only
give concrete details when the interviewer pushes back or asks a second time:
{evasion_list}
"""

    return f"""You are role-playing as **{persona['name']}**, a **{persona['role']}** \
with {persona['knowledge_level']}-level experience.

You are being interviewed by an AI assistant to create an Architecture Decision \
Record (ADR). Answer the questions based on the project context below.

## Your Communication Style
{behavior['answer_style']}
{evasion_instructions}

## Your Project Context
- **Project**: {project['name']}
- **Domain**: {project['domain']}
- **Team size**: {project['team_size']}
- **Tech stack**: {', '.join(project['tech_stack'])}

## The Decision You Need to Make
{ctx['problem']}

## Important Rules
1. Stay in character at all times. You are {persona['name']}, not an AI.
2. Do NOT mention that you are an LLM or that this is a simulation.
3. Do NOT generate ADR YAML yourself — that's the interviewer's job.
4. Answer using the numbered format the interviewer uses (e.g., "1. ...", "2. ...").
5. If the interviewer asks you to confirm or review generated YAML, respond as
   a human would — check if it looks right, point out any inaccuracies, approve
   if it matches what you said.
6. Keep your answers focused and appropriately sized — don't write essays unless
   the question warrants detail.
"""


# ---------------------------------------------------------------------------
# YAML Extraction
# ---------------------------------------------------------------------------

def contains_final_yaml(text: str) -> bool:
    """Check if the text contains a YAML block that looks like a (possibly partial) ADR.

    We accept any YAML code fence that contains 'adr:' plus at least one other
    top-level ADR section.  Models sometimes split large ADRs across multiple
    messages or hit max_tokens before completing the full YAML, so requiring
    *all* sections leads to false negatives.
    """
    yaml_blocks = re.findall(r"```ya?ml\s*\n(.*?)```", text, re.DOTALL)
    for block in yaml_blocks:
        if "adr:" not in block:
            continue
        # Count how many top-level ADR sections are present
        sections = ["context:", "alternatives:", "decision:", "consequences:",
                     "confirmation:", "audit_trail:", "dependencies:"]
        present = sum(1 for s in sections if s in block)
        if present >= 1 and len(block) > 500:
            return True
    return False


def extract_yaml(text: str) -> str | None:
    """Extract the last YAML code block that looks like an ADR.

    Uses the same relaxed matching as contains_final_yaml.
    """
    yaml_blocks = re.findall(r"```ya?ml\s*\n(.*?)```", text, re.DOTALL)
    sections = ["context:", "alternatives:", "decision:", "consequences:",
                 "confirmation:", "audit_trail:", "dependencies:"]
    # Return the last one that looks like an ADR (the final output)
    for block in reversed(yaml_blocks):
        if "adr:" not in block:
            continue
        present = sum(1 for s in sections if s in block)
        if present >= 1 and len(block) > 500:
            return block.strip()
    return None


def _assemble_partial_yamls(parts: list[str]) -> str:
    """Assemble multiple YAML parts into a single ADR YAML document.

    Strategy:
    - The first part is the base (has adr: metadata, context, and usually 1 alternative)
    - Subsequent parts may contain additional alternatives (starting with '  - name:')
      or closing sections (decision:, consequences:, audit_trail:)
    - We try YAML-aware merging first; fall back to string concatenation.
    """
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]

    base = parts[0]

    # Try YAML-aware merging
    try:
        base_doc = yaml.safe_load(base)
        if not isinstance(base_doc, dict):
            raise ValueError("Base is not a dict")

        for part in parts[1:]:
            try:
                chunk = yaml.safe_load(part)
                if not isinstance(chunk, dict):
                    continue

                # If chunk has alternatives, extend the base alternatives
                if 'alternatives' in chunk and isinstance(chunk['alternatives'], list):
                    if 'alternatives' not in base_doc:
                        base_doc['alternatives'] = []
                    base_doc['alternatives'].extend(chunk['alternatives'])

                # Merge top-level sections that aren't in base yet
                for key in ['decision', 'consequences', 'confirmation', 'audit_trail',
                            'dependencies', 'notes']:
                    if key in chunk and key not in base_doc:
                        base_doc[key] = chunk[key]

            except Exception:
                continue

        return yaml.dump(base_doc, default_flow_style=False, allow_unicode=True, sort_keys=False)

    except Exception:
        # Fall back to simple concatenation
        return "\n".join(parts)


def _collect_remaining_yaml(
    client,
    model: str,
    interviewer_messages: list[dict],
    token_usage: dict,
    conversation_log: list[dict],
    base_turn: int,
) -> list[str]:
    """Tight loop to collect remaining YAML parts from the interviewer.

    After partial YAML (1 alternative) is detected, this function directly
    asks the interviewer for remaining parts WITHOUT involving the user LLM.
    Returns a list of YAML strings extracted from the responses.
    """
    collected: list[str] = []

    prompts = [
        (
            "The YAML output was cut off — only 1 alternative was included. "
            "Please now output the **remaining alternatives** in a ```yaml code block. "
            "Format them as a YAML list starting with `alternatives:` containing only "
            "the alternatives NOT yet output. Include their full descriptions and Mermaid "
            "diagrams. Do NOT repeat the first alternative or the adr metadata."
        ),
        (
            "Now please output the **closing sections** in a ```yaml code block: "
            "`decision:` (with chosen_alternative, rationale, tradeoffs, decision_date, confidence), "
            "`consequences:` (positive and negative lists), "
            "`confirmation:` (description), and "
            "`audit_trail:` (initial created event). "
            "These are the remaining top-level sections of the ADR YAML."
        ),
    ]

    for i, prompt in enumerate(prompts):
        part_num = i + 2  # Part 2, Part 3
        print(f"\n  📦 Requesting Part {part_num}...")

        # Add the request directly as user message
        interviewer_messages.append({"role": "user", "content": prompt})
        conversation_log.append({
            "role": "user",
            "content": f"[HARNESS: chunked YAML request Part {part_num}] {prompt}",
            "turn": base_turn,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        try:
            print(f"     → Interviewer ({model})...", end="", flush=True)
            t0 = time.time()
            result = chat_completion(client, model, interviewer_messages, temperature=0.3)
            elapsed = time.time() - t0
            print(f" {elapsed:.1f}s ({result['usage']['total_tokens']} tokens)")

            response = result["content"]
            interviewer_messages.append({"role": "assistant", "content": response})

            # Track tokens
            for k in token_usage["interviewer"]:
                token_usage["interviewer"][k] += result["usage"].get(k, 0)

            conversation_log.append({
                "role": "interviewer",
                "content": response,
                "turn": base_turn,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "tokens": result["usage"],
                "latency_seconds": round(elapsed, 2),
            })

            # Extract any YAML block (relaxed — don't require adr: header)
            yaml_blocks = re.findall(r"```ya?ml\s*\n(.*?)```", response, re.DOTALL)
            for block in yaml_blocks:
                if len(block.strip()) > 100:  # Skip trivially small blocks
                    collected.append(block.strip())
                    print(f"     ✅ Part {part_num} collected ({len(block)} chars)")
                    break
            else:
                print(f"     ⚠️  No YAML block in Part {part_num} response")

        except Exception as e:
            print(f"     ❌ Error collecting Part {part_num}: {e}")
            break

    return collected


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_adr_yaml(yaml_content: str, run_dir: Path) -> dict:
    """
    Write the YAML to a temp file and run validate-adr.py against it.
    Returns validation results as a dict.
    """
    adr_file = run_dir / "produced_adr.yaml"
    adr_file.write_text(yaml_content)

    result = {"schema_valid": False, "errors": [], "warnings": []}

    # Run validate-adr.py
    try:
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "validate-adr.py"),
             str(adr_file)],
            capture_output=True, text=True, timeout=30,
        )
        result["validate_stdout"] = proc.stdout
        result["validate_stderr"] = proc.stderr
        result["validate_exit_code"] = proc.returncode
        result["schema_valid"] = proc.returncode == 0

        # Parse errors from output
        for line in (proc.stdout + proc.stderr).splitlines():
            if "ERROR" in line.upper():
                result["errors"].append(line.strip())
            elif "WARNING" in line.upper() or "WARN" in line.upper():
                result["warnings"].append(line.strip())
    except subprocess.TimeoutExpired:
        result["errors"].append("validate-adr.py timed out after 30s")
    except Exception as e:
        result["errors"].append(f"validate-adr.py failed: {e}")

    # Run review-adr.py (quality check)
    try:
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "review-adr.py"),
             str(adr_file)],
            capture_output=True, text=True, timeout=30,
        )
        result["review_stdout"] = proc.stdout
        result["review_stderr"] = proc.stderr
        result["review_exit_code"] = proc.returncode
    except (subprocess.TimeoutExpired, Exception) as e:
        result["review_stdout"] = ""
        result["review_stderr"] = str(e)
        result["review_exit_code"] = -1

    return result


# ---------------------------------------------------------------------------
# Quality Metrics (deterministic)
# ---------------------------------------------------------------------------

def compute_quality_metrics(yaml_content: str) -> dict:
    """Compute deterministic quality metrics from the produced ADR YAML."""
    metrics = {
        "parseable_yaml": False,
        "alternative_count": 0,
        "avg_description_words": 0,
        "y_statement_present": False,
        "y_statement_clauses": 0,
        "rejection_rationale_coverage": 0.0,
        "mermaid_diagram_count": 0,
        "asr_functional_count": 0,
        "asr_nonfunctional_count": 0,
        "optional_fields_populated": 0,
        "total_optional_fields": 12,
    }

    try:
        data = yaml.safe_load(yaml_content)
        metrics["parseable_yaml"] = True
    except Exception:
        return metrics

    if not isinstance(data, dict):
        return metrics

    # Alternative count + description depth
    alts = data.get("alternatives", [])
    metrics["alternative_count"] = len(alts)
    if alts:
        desc_words = [len(a.get("description", "").split()) for a in alts]
        metrics["avg_description_words"] = sum(desc_words) / len(desc_words)

    # Y-Statement check
    adr_meta = data.get("adr", {})
    y_stmt = adr_meta.get("y_statement", "")
    metrics["y_statement_present"] = bool(y_stmt and len(y_stmt) > 20)
    if y_stmt:
        clause_markers = [
            "in the context of", "facing", "we decided for",
            "neglected", "to achieve", "accepting", "because"
        ]
        metrics["y_statement_clauses"] = sum(
            1 for m in clause_markers if m.lower() in y_stmt.lower()
        )

    # Rejection rationale coverage
    non_chosen = [a for a in alts
                  if a.get("name") != data.get("decision", {}).get("chosen_alternative")]
    if non_chosen:
        with_rationale = sum(1 for a in non_chosen if a.get("rejection_rationale"))
        metrics["rejection_rationale_coverage"] = with_rationale / len(non_chosen)

    # Mermaid diagrams
    yaml_str = yaml_content
    metrics["mermaid_diagram_count"] = len(re.findall(r"```mermaid", yaml_str))

    # ASRs
    asrs = data.get("architecturally_significant_requirements", {})
    metrics["asr_functional_count"] = len(asrs.get("functional", []))
    metrics["asr_nonfunctional_count"] = len(asrs.get("non_functional", []))

    # Optional fields populated
    optional_checks = [
        ("adr", "y_statement"), ("adr", "decision_level"), ("adr", "tags"),
        ("adr", "priority"), ("adr", "component"), ("adr", "schema_version"),
        ("decision", "tradeoffs"), ("decision", "confidence"),
        ("dependencies",), ("references",), ("lifecycle",),
        ("architecturally_significant_requirements",),
    ]
    count = 0
    for path in optional_checks:
        obj = data
        for key in path:
            obj = obj.get(key, {}) if isinstance(obj, dict) else {}
        if obj:
            count += 1
    metrics["optional_fields_populated"] = count

    return metrics


# ---------------------------------------------------------------------------
# Analyst LLM
# ---------------------------------------------------------------------------

ANALYST_SYSTEM_PROMPT = """\
You are an ADR process analyst. You have been given:
1. The full conversation log between an AI interviewer and a simulated user
2. The ADR YAML produced by the interviewer
3. The schema validation results
4. The test scenario definition (including ground truth expectations)

Analyze the interaction and provide a structured report using EXACTLY the
following format:

## Conversation Quality
- **Total turns**: (count of user + interviewer messages)
- **Wasted turns**: (turns that didn't advance the ADR — greetings, meta-talk, clarifications of the interview process itself)
- **Missed probes**: (specific questions the interviewer should have asked based on the scenario context but didn't)
- **Redundant questions**: (information that was asked for when the user had already provided it)
- **Socratic depth score**: X/10 (how well the interviewer challenged weak or evasive answers)
- **Instruction adherence score**: X/10 (how well the interviewer followed the batched-question format and interview structure from the instructions)

## ADR Artifact Quality
- **Schema compliance**: (pass/fail from validation results + any additional issues you spot)
- **Information density**: X/10 (how much of the scenario's ground truth was captured in the ADR)
- **Hallucination check**: (list any claims in the ADR that were NOT stated by the user during the conversation — the interviewer invented them)
- **Y-Statement quality**: (structural conformance — are all 7 clauses present? Semantic accuracy — does it faithfully represent the decision?)
- **Alternative balance**: (are the pros/cons balanced, or do rejected alternatives look like strawmen?)
- **Description depth**: (are alternatives described in sufficient architectural detail, or are they surface-level summaries?)

## Overall Quality Score
**X/10** with one-sentence justification.

## Process Improvement Suggestions
For each suggestion (up to 5), provide:
- **What to change**: (specific instruction text, question wording, or process step)
- **Where**: (which file: repomix-instruction.md, SKILL.md, or scenario design)
- **Expected impact**: (fewer turns, better coverage, stronger ADRs, etc.)
- **Priority**: P0 (critical) / P1 (important) / P2 (nice-to-have)
"""


def run_analyst(
    client,
    model: str,
    conversation_log: list[dict],
    yaml_content: str | None,
    validation: dict,
    scenario: dict,
) -> str:
    """Run the Analyst LLM to produce a quality report."""
    # Build the analyst input
    conv_text = "\n\n".join(
        f"### {entry['role'].upper()} (turn {i + 1})\n{entry['content']}"
        for i, entry in enumerate(conversation_log)
    )

    user_input = f"""## Conversation Log

{conv_text}

---

## Produced ADR YAML

```yaml
{yaml_content or "NO YAML WAS PRODUCED"}
```

---

## Schema Validation Results

- Schema valid: {validation.get('schema_valid', 'N/A')}
- Errors: {json.dumps(validation.get('errors', []))}
- Warnings: {json.dumps(validation.get('warnings', []))}

---

## Test Scenario (Ground Truth)

```yaml
{yaml.dump(scenario, default_flow_style=False, allow_unicode=True)}
```
"""

    messages = [
        {"role": "system", "content": ANALYST_SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    result = chat_completion(
        client, model, messages,
        temperature=TEMPERATURE_CONFIG["analyst"],
    )
    return result["content"]


# ---------------------------------------------------------------------------
# Main Conversation Loop
# ---------------------------------------------------------------------------

def run_conversation(
    client,
    scenario: dict,
    interviewer_model: str,
    user_model: str,
    bundle_variant: str = "default",
) -> tuple[list[dict], str | None, dict]:
    """
    Run the full interviewer ↔ user conversation.
    Returns (conversation_log, extracted_yaml, token_usage).
    """
    # Load bundle as interviewer system prompt
    bundle_content = load_bundle(bundle_variant)
    interviewer_messages: list[dict] = [
        {"role": "system", "content": bundle_content},
    ]

    # Build user system prompt
    user_system = build_user_system_prompt(scenario)
    user_messages: list[dict] = [
        {"role": "system", "content": user_system},
    ]

    # Start with user's opening message
    current_message = scenario["user_behavior"]["initial_message"].strip()
    conversation_log: list[dict] = []
    token_usage = {
        "interviewer": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "user": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }

    extracted_yaml = None
    consecutive_short = 0  # track stalled conversations
    partial_yamls = []     # collect partial YAML blocks for assembly
    termination_reason = None

    for turn in range(MAX_TURNS):
        turn_num = turn + 1
        print(f"\n  📝 Turn {turn_num}")

        # Log the user's message
        conversation_log.append({
            "role": "user",
            "content": current_message,
            "turn": turn_num,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        # User → Interviewer
        interviewer_messages.append({"role": "user", "content": current_message})

        print(f"     → Interviewer ({interviewer_model})...", end="", flush=True)
        t0 = time.time()
        try:
            interviewer_result = chat_completion(
                client, interviewer_model, interviewer_messages,
                temperature=TEMPERATURE_CONFIG["interviewer"],
            )
        except ContextOverflowError as e:
            print(f" ❌ Context overflow!")
            termination_reason = f"Context overflow on interviewer: {e}"
            break

        elapsed = time.time() - t0
        print(f" {elapsed:.1f}s ({interviewer_result['usage']['total_tokens']} tokens)")

        assistant_msg = interviewer_result["content"]
        interviewer_messages.append({"role": "assistant", "content": assistant_msg})

        # Accumulate token usage
        for k in token_usage["interviewer"]:
            token_usage["interviewer"][k] += interviewer_result["usage"].get(k, 0)

        # Log the interviewer's response
        conversation_log.append({
            "role": "interviewer",
            "content": assistant_msg,
            "turn": turn_num,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tokens": interviewer_result["usage"],
            "latency_seconds": round(elapsed, 2),
        })

         # Check for final YAML (or YAML chunk in multi-part mode)
        if contains_final_yaml(assistant_msg) or (partial_yamls and extract_yaml(assistant_msg)):
            candidate_yaml = extract_yaml(assistant_msg)
            if candidate_yaml:
                # Parse to count alternatives
                alt_count = 0
                has_alternatives = 'alternatives:' in candidate_yaml
                has_decision = 'decision:' in candidate_yaml
                if has_alternatives:
                    try:
                        parsed = yaml.safe_load(candidate_yaml)
                        if parsed and isinstance(parsed, dict):
                            alts = parsed.get('alternatives', [])
                            alt_count = len(alts) if isinstance(alts, list) else 0
                    except Exception:
                        alt_section = candidate_yaml.split('alternatives:')[1] if 'alternatives:' in candidate_yaml else ''
                        alt_count = len(re.findall(r'^  - name:', alt_section, re.MULTILINE))

                # Complete YAML: ≥2 alternatives + decision section
                if has_alternatives and alt_count >= 2 and has_decision:
                    extracted_yaml = candidate_yaml
                    print(f"\n  ✅ Complete YAML at turn {turn_num} ({alt_count} alternatives)")
                    termination_reason = "yaml_produced"
                    break

                # Acceptable YAML: ≥2 alternatives but no decision (close enough)
                if has_alternatives and alt_count >= 2:
                    extracted_yaml = candidate_yaml
                    print(f"\n  ✅ YAML at turn {turn_num} ({alt_count} alternatives, no decision section)")
                    termination_reason = "yaml_produced_partial"
                    break

                # Partial YAML (1 alt) — break and collect remaining parts
                partial_yamls.append(candidate_yaml)
                print(f"\n  📦 Partial YAML at turn {turn_num} ({alt_count} alternative). "
                      f"Entering chunked collection mode...")
                
                # Tight loop: ask for remaining parts directly (no user LLM)
                remaining_yaml = _collect_remaining_yaml(
                    client, interviewer_model, interviewer_messages,
                    token_usage, conversation_log, turn_num,
                )
                if remaining_yaml:
                    partial_yamls.extend(remaining_yaml)
                
                # Assemble
                extracted_yaml = _assemble_partial_yamls(partial_yamls)
                termination_reason = "yaml_assembled_from_parts"
                break

        # Turn-budget pressure: when approaching limit, force YAML generation
        if turn_num == YAML_PRESSURE_TURN:
            print(f"\n  ⏰ Turn {turn_num} reached — injecting YAML generation request...")
            current_message = (
                "I think we've covered all the key points. I'd like you to go ahead "
                "and generate the complete ADR YAML now based on everything we've "
                "discussed so far. We can review and adjust if needed."
            )
            continue

        # Stall detection: if interviewer responses are very short, the conversation
        # may be stuck in a loop (e.g., "anything else?" / "no" cycles)
        if len(assistant_msg.strip()) < 150:
            consecutive_short += 1
        else:
            consecutive_short = 0

        if consecutive_short >= STALL_THRESHOLD:
            print(f"\n  🔄 Stall detected ({consecutive_short} short responses). "
                  f"Injecting wrap-up request...")
            current_message = (
                "I think we've covered everything. Please go ahead and generate "
                "the complete ADR YAML based on everything we've discussed."
            )
            continue

        # Interviewer's response → User LLM
        user_messages.append({"role": "user", "content": assistant_msg})

        print(f"     → User ({user_model})...", end="", flush=True)
        t0 = time.time()
        try:
            user_result = chat_completion(
                client, user_model, user_messages,
                temperature=TEMPERATURE_CONFIG["user"],
            )
        except ContextOverflowError as e:
            print(f" ❌ Context overflow!")
            termination_reason = f"Context overflow on user model: {e}"
            # Try to salvage: ask the interviewer to generate YAML with what it has
            current_message = (
                "I think we've covered enough. Please generate the complete ADR YAML "
                "now based on all the information gathered so far."
            )
            continue

        elapsed = time.time() - t0
        print(f" {elapsed:.1f}s ({user_result['usage']['total_tokens']} tokens)")

        current_message = user_result["content"]
        user_messages.append({"role": "assistant", "content": current_message})

        # Accumulate token usage
        for k in token_usage["user"]:
            token_usage["user"][k] += user_result["usage"].get(k, 0)

    else:
        termination_reason = f"max_turns_exceeded ({MAX_TURNS})"
        print(f"\n  ⚠️  Max turns ({MAX_TURNS}) reached without producing YAML")
        # Last-ditch: scan ALL past interviewer messages for YAML we might have missed
        # (e.g., if the conversation continued past the YAML output)
        if not extracted_yaml:
            for entry in reversed(conversation_log):
                if entry["role"] == "interviewer" and contains_final_yaml(entry["content"]):
                    extracted_yaml = extract_yaml(entry["content"])
                    if extracted_yaml:
                        print(f"  🔍 Found YAML in earlier turn {entry['turn']}!")
                        termination_reason = f"yaml_found_retroactively_at_turn_{entry['turn']}"
                        break

    return conversation_log, extracted_yaml, token_usage


# ---------------------------------------------------------------------------
# Single Scenario Runner
# ---------------------------------------------------------------------------

def run_scenario(
    scenario_path: Path,
    interviewer_model: str,
    user_model: str,
    analyst_model: str = "gpt-5.2-xhigh",
    bundle_variant: str = "default",
) -> Path:
    """Run a single test scenario end-to-end.

    Analyst pass is always run — the primary value of this harness is the
    learning from analysis, not just schema validation.
    """
    # Load scenario
    scenario = yaml.safe_load(scenario_path.read_text())

    scenario_id = scenario["scenario"]["id"]
    scenario_title = scenario["scenario"]["title"]
    difficulty = scenario["scenario"]["difficulty"]

    print(f"\n{'='*70}")
    print(f"🧪 Scenario: {scenario_id} — {scenario_title}")
    print(f"   Difficulty: {difficulty}")
    print(f"   Interviewer: {interviewer_model}")
    print(f"   User: {user_model}")
    print(f"   Bundle: {bundle_variant}")
    print(f"{'='*70}")

    # Create run directory
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    run_dir = RUNS_DIR / f"run-{timestamp}-{scenario_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    # Save configuration
    config = {
        "scenario_id": scenario_id,
        "scenario_path": str(scenario_path),
        "scenario_title": scenario_title,
        "difficulty": difficulty,
        "interviewer_model": interviewer_model,
        "user_model": user_model,
        "analyst_model": analyst_model,
        "bundle_variant": bundle_variant,
        "temperature": TEMPERATURE_CONFIG,
        "max_turns": MAX_TURNS,
        "timestamp": timestamp,
    }
    (run_dir / "config.json").write_text(json.dumps(config, indent=2))

    # Get LLM client
    client = get_openai_client()

    # Run conversation
    print("\n📣 Starting conversation...")
    conversation_log, extracted_yaml, token_usage = run_conversation(
        client, scenario, interviewer_model, user_model, bundle_variant,
    )

    # Save conversation log
    (run_dir / "conversation_log.json").write_text(
        json.dumps(conversation_log, indent=2, ensure_ascii=False)
    )

    # Save token usage
    (run_dir / "token_usage.json").write_text(json.dumps(token_usage, indent=2))

    total_turns = max(e["turn"] for e in conversation_log) if conversation_log else 0
    total_tokens = (token_usage["interviewer"]["total_tokens"]
                    + token_usage["user"]["total_tokens"])
    print(f"\n📊 Conversation: {total_turns} turns, {total_tokens:,} total tokens")

    # Validate
    validation = {}
    quality_metrics = {}
    if extracted_yaml:
        print("\n🔍 Validating produced ADR...")
        validation = validate_adr_yaml(extracted_yaml, run_dir)
        quality_metrics = compute_quality_metrics(extracted_yaml)

        print(f"   Schema valid: {'✅' if validation['schema_valid'] else '❌'}")
        if validation["errors"]:
            for err in validation["errors"][:5]:
                print(f"   ❌ {err}")
        if validation["warnings"]:
            for warn in validation["warnings"][:3]:
                print(f"   ⚠️  {warn}")
        print(f"   Alternatives: {quality_metrics['alternative_count']}")
        print(f"   Y-Statement: {'✅' if quality_metrics['y_statement_present'] else '❌'} "
              f"({quality_metrics['y_statement_clauses']}/7 clauses)")
        print(f"   Mermaid diagrams: {quality_metrics['mermaid_diagram_count']}")
        print(f"   Rejection rationale: {quality_metrics['rejection_rationale_coverage']:.0%}")
        print(f"   ASRs: {quality_metrics['asr_functional_count']}F + "
              f"{quality_metrics['asr_nonfunctional_count']}NF")
    else:
        print("\n❌ No YAML was produced — skipping validation")
        (run_dir / "produced_adr.yaml").write_text("# No YAML was produced by the interviewer\n")

    (run_dir / "validation_result.json").write_text(
        json.dumps(validation, indent=2, default=str)
    )
    (run_dir / "quality_metrics.json").write_text(
        json.dumps(quality_metrics, indent=2)
    )

    # Analyst pass (always runs — primary learning mechanism)
    print(f"\n🔬 Running Analyst ({analyst_model})...")
    t0 = time.time()
    analysis_report = run_analyst(
        client, analyst_model,
        conversation_log, extracted_yaml,
        validation, scenario,
    )
    elapsed = time.time() - t0
    print(f"   Analyst completed in {elapsed:.1f}s")
    (run_dir / "analysis_report.md").write_text(analysis_report)

    # Extract overall quality score if present
    score_match = re.search(r"\*\*(\d+)/10\*\*", analysis_report)
    if score_match:
        print(f"   📈 Overall quality score: {score_match.group(1)}/10")

    # Summary
    print(f"\n📁 Results saved to: {run_dir.relative_to(REPO_ROOT)}")
    print(f"{'='*70}\n")

    return run_dir


# ---------------------------------------------------------------------------
# Aggregate Report
# ---------------------------------------------------------------------------

def generate_aggregate_report(run_dirs: list[Path]) -> str:
    """Generate a cross-run comparison table."""
    rows = []
    for run_dir in sorted(run_dirs):
        config_file = run_dir / "config.json"
        metrics_file = run_dir / "quality_metrics.json"
        validation_file = run_dir / "validation_result.json"
        analysis_file = run_dir / "analysis_report.md"
        token_file = run_dir / "token_usage.json"

        if not config_file.exists():
            continue

        config = json.loads(config_file.read_text())
        metrics = json.loads(metrics_file.read_text()) if metrics_file.exists() else {}
        validation = json.loads(validation_file.read_text()) if validation_file.exists() else {}
        tokens = json.loads(token_file.read_text()) if token_file.exists() else {}

        # Extract analyst score
        analyst_score = "N/A"
        if analysis_file.exists():
            text = analysis_file.read_text()
            score_match = re.search(r"\*\*(\d+)/10\*\*", text)
            if score_match:
                analyst_score = f"{score_match.group(1)}/10"

        total_tokens = (tokens.get("interviewer", {}).get("total_tokens", 0)
                        + tokens.get("user", {}).get("total_tokens", 0))

        # Count turns from conversation log
        conv_file = run_dir / "conversation_log.json"
        turns = 0
        if conv_file.exists():
            conv = json.loads(conv_file.read_text())
            turns = max(e.get("turn", 0) for e in conv) if conv else 0

        rows.append({
            "Scenario": config.get("scenario_id", "?"),
            "Difficulty": config.get("difficulty", "?"),
            "Interviewer": config.get("interviewer_model", "?"),
            "User": config.get("user_model", "?"),
            "Turns": turns,
            "Tokens": f"{total_tokens:,}",
            "Schema": "✅" if validation.get("schema_valid") else "❌",
            "Y-Stmt": f"{metrics.get('y_statement_clauses', 0)}/7",
            "Alts": metrics.get("alternative_count", 0),
            "Score": analyst_score,
        })

    if not rows:
        return "No runs found.\n"

    # Build markdown table
    headers = list(rows[0].keys())
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join("---" for _ in headers) + " |"
    body_lines = []
    for row in rows:
        body_lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")

    report = f"""# Aggregate Test Report

Generated: {datetime.now().isoformat()}

## Results

{header_line}
{sep_line}
{chr(10).join(body_lines)}

## Summary

- **Total runs**: {len(rows)}
- **Schema pass rate**: {sum(1 for r in rows if r['Schema'] == '✅')}/{len(rows)}
- **Average turns**: {sum(r['Turns'] for r in rows) / len(rows):.1f}
"""

    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Triple-LLM Testing Harness for ADR Governance",
    )
    parser.add_argument("--scenario", type=Path,
                        help="Path to a single scenario YAML file")
    parser.add_argument("--all", action="store_true",
                        help="Run all scenarios in tests/scenarios/")
    parser.add_argument("--interviewer", default=DEFAULT_INTERVIEWER_MODEL,
                        help=f"Interviewer model (default: {DEFAULT_INTERVIEWER_MODEL})")
    parser.add_argument("--user", default=DEFAULT_USER_MODEL,
                        help=f"User model (default: {DEFAULT_USER_MODEL})")
    parser.add_argument("--analyst", default=DEFAULT_ANALYST_MODEL,
                        help=f"Analyst model (default: {DEFAULT_ANALYST_MODEL})")
    parser.add_argument("--bundle", default="default",
                        choices=["default", "minimal", "full"],
                        help="Bundle variant for interviewer (default: default)")
    # Analyst pass is always run — it's the primary learning mechanism
    parser.add_argument("--aggregate", action="store_true",
                        help="Generate aggregate report from all existing runs")

    args = parser.parse_args()

    if args.aggregate:
        if not RUNS_DIR.exists():
            print("No runs directory found.")
            return
        run_dirs = [d for d in RUNS_DIR.iterdir() if d.is_dir()]
        report = generate_aggregate_report(run_dirs)
        report_path = RUNS_DIR / "aggregate_report.md"
        report_path.write_text(report)
        print(report)
        print(f"\nSaved to: {report_path}")
        return

    if not args.scenario and not args.all:
        parser.error("Specify --scenario <path> or --all")

    # Collect scenarios
    scenario_paths = []
    if args.all:
        scenario_paths = sorted(SCENARIOS_DIR.glob("*.yaml"))
        if not scenario_paths:
            print(f"No scenarios found in {SCENARIOS_DIR}")
            return
    elif args.scenario:
        if not args.scenario.exists():
            print(f"Scenario not found: {args.scenario}")
            return
        scenario_paths = [args.scenario]

    # Run each scenario
    run_dirs = []
    for i, scenario_path in enumerate(scenario_paths):
        if i > 0:
            print(f"\n⏳ Waiting {INTER_RUN_DELAY_SECONDS}s before next scenario...\n")
            time.sleep(INTER_RUN_DELAY_SECONDS)

        run_dir = run_scenario(
            scenario_path,
            args.interviewer, args.user, args.analyst,
            args.bundle,
        )
        run_dirs.append(run_dir)

    # Generate aggregate report if multiple runs
    if len(run_dirs) > 1:
        print("\n📊 Generating aggregate report...")
        report = generate_aggregate_report(run_dirs)
        report_path = RUNS_DIR / "aggregate_report.md"
        report_path.write_text(report)
        print(report)


if __name__ == "__main__":
    main()
