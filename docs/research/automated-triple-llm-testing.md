# Automated Triple-LLM Testing Harness for ADR Governance

> **Status**: Proposal — v0.1  
> **Date**: 2026-03-08  
> **Author**: AI-assisted design

---

## Table of Contents

- [1. Motivation](#1-motivation)
- **Architecture**
  - [2.1 Components](#21-components)
  - [2.2 LLM Selection Strategy](#22-llm-selection-strategy)
- **Scenario Design**
  - [3.1 Scenario Schema](#31-scenario-schema)
  - [3.2 Scenario Categories](#32-scenario-categories)
- **Conversation Orchestration**
  - [4.1 Turn-by-Turn Flow](#41-turn-by-turn-flow)
  - [4.2 Termination Conditions](#42-termination-conditions)
  - [4.3 Token & Cost Tracking](#43-token--cost-tracking)
- **Post-Conversation Analysis**
  - [5.1 Schema Validation](#51-schema-validation-deterministic)
  - [5.2 Quality Review](#52-quality-review-deterministic)
  - [5.3 Analyst LLM Review](#53-analyst-llm-review-ai-powered)
- [6. Output Structure](#6-output-structure)
- **Metrics & Success Criteria**
  - [7.1 Per-Run Metrics](#71-per-run-metrics)
  - [7.2 Cross-Run Goals](#72-cross-run-goals)
- **Implementation Plan**
  - [Phase 1: Core Harness](#phase-1-core-harness-mvp)
  - [Phase 2: Analyst & Metrics](#phase-2-analyst--metrics)
  - [Phase 3: Real-World Scenarios](#phase-3-real-world-scenarios)
  - [Phase 4: Feedback Loop](#phase-4-feedback-loop)
- **Technical Requirements**
  - [9.1 Dependencies](#91-dependencies)
  - [9.2 LiteLLM Configuration](#92-litellm-configuration)
  - [9.3 System Prompt Strategy](#93-system-prompt-strategy)
  - [9.4 Bundle Variants to Test](#94-bundle-variants-to-test)
- [10. README Integration](#10-readme-integration)
- **Design Decisions**
  - [Q1. Bundle size vs. quality](#q1-bundle-size-vs-quality-tradeoff)
  - [Q2. User LLM evasiveness](#q2-user-llm-evasiveness-calibration)
  - [Q3. Determinism & temperature](#q3-determinism--temperature-strategy)
  - [Q4. Cost control](#q4-cost-control)
  - [Q5. GitHub PR extraction](#q5-github-pr-extraction-attribution--ethics)
  - [Q6. Thinking/reasoning models](#q6-thinkingreasoning-models-for-the-analyst)
- [12. Next Steps](#12-next-steps)

---

## 1. Motivation

The ADR authoring skill (Socratic interview mode) is the framework's most complex capability. It involves multi-turn dialogue, schema adherence, Y-Statement synthesis, coherence checking, and YAML generation. Today this is tested manually — a human uploads the bundle and goes through the interview. This doesn't scale.

**We need a closed-loop testing harness** where:
1. One LLM plays the **Interviewer** (uses the bundle instructions)
2. Another LLM plays the **User** (simulates a developer with a scenario)
3. The full conversation trace is captured
4. The produced ADR artifact is validated
5. A third LLM pass (the **Analyst**) reviews the trace + artifact for quality improvements

This gives us reproducible, measurable ADR authoring quality — and a feedback loop to improve the instructions, schema, and process.

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Test Orchestrator                     │
│                  (Python script)                        │
│                                                         │
│  ┌──────────┐    conversation     ┌──────────────┐      │
│  │ User LLM │◄──────────────────►│ Interviewer  │      │
│  │ (GPT/    │   ping-pong turns  │     LLM      │      │
│  │  Gemini) │                    │ (system =    │      │
│  │          │                    │  bundle.md)  │      │
│  └──────────┘                    └──────────────┘      │
│       │                                │                │
│       │ scenario.yaml                  │ repomix-       │
│       │ (persona +                     │ instruction.md │
│       │  project context)              │ (full bundle)  │
│       │                                │                │
│       ▼                                ▼                │
│  ┌─────────────────────────────────────┐                │
│  │         Conversation Log            │                │
│  │    (JSON: role, content, tokens)    │                │
│  └──────────────┬──────────────────────┘                │
│                 │                                       │
│       ┌─────────┴─────────┐                             │
│       ▼                   ▼                             │
│  ┌──────────┐     ┌──────────────┐                      │
│  │ YAML     │     │  Analyst LLM │                      │
│  │ Extractor│     │ (reviews     │                      │
│  │ + Schema │     │  trace +     │                      │
│  │ Validator│     │  artifact)   │                      │
│  └─────┬────┘     └──────┬───────┘                      │
│        │                 │                              │
│        ▼                 ▼                              │
│  ┌─────────────────────────────────────┐                │
│  │           Run Report                │                │
│  │  - conversation_log.json            │                │
│  │  - produced_adr.yaml                │                │
│  │  - validation_result.json           │                │
│  │  - analysis_report.md               │                │
│  │  - metrics.json                     │                │
│  └─────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────┘
```

### 2.1 Components

| Component | Role | LLM / Tool |
|-----------|------|-----------|
| **Orchestrator** | Drives the conversation loop, extracts YAML, runs validation, triggers analysis | Python script (`tests/llm_harness.py`) |
| **Interviewer LLM** | Plays the ADR authoring skill — asks Socratic questions, generates YAML | Any model via LiteLLM (`localhost:4000`). System prompt = full `repomix-instruction.md` + bundle content |
| **User LLM** | Simulates a developer answering interview questions | Different model via LiteLLM. System prompt = scenario definition |
| **Analyst LLM** | Post-hoc review of the conversation trace + produced ADR | Can be same or different model. Produces structured analysis |
| **Schema Validator** | Existing `validate-adr.py` + `review-adr.py` | Python scripts (deterministic) |

### 2.2 LLM Selection Strategy

Use **different models** for Interviewer and User to avoid echo-chamber effects.

**Available models (via LiteLLM proxy at `localhost:4000`):**
- `gpt-5.2-{none,low,medium,high,xhigh}` — OpenAI GPT-5.2 with reasoning tiers
- `glm-5` / `glm-5-thinking` — GLM 5 (Z.ai)
- `glm-4.7` / `glm-4.7-thinking` — GLM 4.7 (Z.ai)
- `deepseek-v3` / `deepseek-speciale` — DeepSeek (OpenRouter)
- `kimi-k2` / `kimi-k2-thinking` — Moonshot Kimi K2
- `minimax-m2` — MiniMax M2

**Available via CLI only (Gemini CLI v0.29.6):**
- Gemini Flash / Pro — invoked via `gemini -p "<prompt>" -o json -m <model>`
- Requires subprocess wrapping in the harness

**Not available via API:** Claude (Opus/Sonnet) — no programmatic access.

| Run | Interviewer | User | Analyst |
|-----|-------------|------|---------|
| Default | `gpt-5.2-medium` | `glm-5` | `gpt-5.2-high` |
| Alt-1 | `glm-5` | `gpt-5.2-none` | `glm-5-thinking` |
| Alt-2 | `gpt-5.2-high` | `deepseek-v3` | `gpt-5.2-high` |
| Alt-3 | Gemini Pro (CLI) | `gpt-5.2-none` | `gpt-5.2-high` |

This tests instruction portability across model families (OpenAI, GLM, DeepSeek, optionally Gemini).

---

## 3. Scenario Design

### 3.1 Scenario Schema

Each test scenario is defined as a YAML file in `tests/scenarios/`:

```yaml
# tests/scenarios/fictional-001-api-versioning.yaml
scenario:
  id: fictional-001
  category: fictional          # fictional | github-pr | existing-adr
  title: "API Versioning Strategy"
  difficulty: medium            # easy | medium | hard

persona:
  name: "Alex Rivera"
  role: "Backend Lead"
  style: "concise, technically deep, occasionally evasive on cost questions"
  knowledge_level: senior       # junior | mid | senior | architect

project:
  name: "Nebula Commerce Platform"
  domain: "E-commerce"
  team_size: 12
  tech_stack: ["Go", "PostgreSQL", "gRPC", "Kubernetes"]

decision_context:
  problem: |
    Our REST API serves 200+ clients (mobile, web, partners). We need to
    evolve the API without breaking existing consumers. Currently using
    ad-hoc versioning with /v1/ prefix but no formal strategy.
  expected_decision_type: technology
  expected_decision_level: tactical
  expected_alternatives:
    - "URL path versioning (/v1/, /v2/)"
    - "Header-based versioning (Accept header)"
    - "Query parameter versioning"
  ground_truth_notes: |
    A good ADR should identify that URL path versioning is simplest but
    creates routing complexity. Header-based is RESTful but harder to test.
    The chosen approach should weigh developer experience vs. REST purity.

user_behavior:
  initial_message: |
    I want to create an ADR for our API versioning approach. We've been
    doing it ad-hoc and need a proper strategy.
  answer_style: |
    Answer questions directly but don't volunteer extra information unless
    asked. When asked about costs, be somewhat vague initially. When pushed
    on risks, acknowledge them honestly. Respond using numbered format
    matching the interviewer's questions.
  evasion_points:
    - "budget constraints"      # will be vague until pressed
    - "team capacity"           # will understate initially
```

### 3.2 Scenario Categories

#### A. Fictional Scenarios (5–8 scenarios)

Fully synthetic — designed to test specific aspects of the interview:

| ID | Title | Tests |
|----|-------|-------|
| `fictional-001` | API Versioning Strategy | Basic flow, technology decision |
| `fictional-002` | Monolith-to-Microservices Migration | Strategic decision, high complexity |
| `fictional-003` | Choosing a Secret Store | Vendor decision, security constraints |
| `fictional-004` | Adopting Trunk-Based Development | Process decision, organizational resistance |
| `fictional-005` | Event Sourcing for Audit Trail | Technology + compliance intersection |
| `fictional-006` | Deferred Decision: Quantum-Safe Crypto | Tests `deferred` status handling |
| `fictional-007` | Superseding Legacy Auth (references ADR-0001) | Tests supersession workflow |
| `fictional-008` | Junior Dev — Vague Requirements | Tests Socratic probing depth |

#### B. GitHub PR-Based Scenarios (3–5 scenarios)

Derived from real open-source pull requests. The orchestrator fetches PR metadata, diff, and discussion to construct a realistic scenario:

| Source Repo | PR | Decision Topic |
|-------------|-----|----------------|
| `kubernetes/kubernetes` | Large refactor PR | Infrastructure decision extracted from PR discussion |
| `hashicorp/terraform` | Provider architecture PR | Technology choice from design discussion |
| `grafana/grafana` | Auth refactor | Security decision from RFC-style PR description |

**Extraction process:**
1. Fetch PR description, body, and comments via GitHub API
2. Feed to an LLM to extract: problem statement, alternatives discussed, constraints mentioned, key participants
3. Construct a scenario YAML with `category: github-pr`
4. The User LLM role-plays as the PR author

#### C. Existing ADR Repositories (2–3 scenarios)

Find real projects that maintain ADRs, extract one, and see if our framework can reproduce it in our schema:

| Source | Format | Goal |
|--------|--------|------|
| `adr/madr` (ADR GitHub org) | MADR Markdown | Convert MADR → our YAML schema |
| `joelparkerhenderson/architecture-decision-record` | Mixed formats | Test format-agnostic extraction |
| Real corporate repos with public ADRs | Various | Stress-test alternative extraction + ASR capture |

---

## 4. Conversation Orchestration Protocol

### 4.1 Turn-by-Turn Flow

```python
# Pseudocode for the core loop
def run_conversation(scenario, interviewer_model, user_model):
    # 1. Initialize the Interviewer with the bundle as system prompt
    interviewer_messages = [
        {"role": "system", "content": load_bundle()},
    ]

    # 2. Initialize the User with the scenario as system prompt
    user_system = build_user_system_prompt(scenario)
    user_messages = [
        {"role": "system", "content": user_system},
    ]

    # 3. User sends the opening message (from scenario)
    current_message = scenario["user_behavior"]["initial_message"]
    conversation_log = []

    for turn in range(MAX_TURNS):  # safety cap: 30 turns
        # User → Interviewer
        interviewer_messages.append({"role": "user", "content": current_message})
        conversation_log.append({"role": "user", "content": current_message})

        interviewer_response = litellm.completion(
            model=interviewer_model,
            messages=interviewer_messages,
        )
        assistant_msg = interviewer_response.choices[0].message.content
        interviewer_messages.append({"role": "assistant", "content": assistant_msg})
        conversation_log.append({"role": "interviewer", "content": assistant_msg})

        # Check if the Interviewer produced final YAML (```yaml block)
        if contains_final_yaml(assistant_msg):
            break

        # Interviewer's questions → User LLM answers
        user_messages.append({"role": "user", "content": assistant_msg})
        user_response = litellm.completion(
            model=user_model,
            messages=user_messages,
        )
        current_message = user_response.choices[0].message.content
        user_messages.append({"role": "assistant", "content": current_message})

    return conversation_log, extract_yaml(assistant_msg)
```

### 4.2 Termination Conditions

The conversation ends when:
1. **YAML detected**: The interviewer produces a ```yaml code block containing `adr:` as a top-level key
2. **Max turns exceeded**: Safety cap of 30 turns (configurable)
3. **Model refuses or errors**: Captured as a failure case in the report

### 4.3 Token & Cost Tracking

Every LiteLLM call captures `usage` metadata:
- `prompt_tokens`, `completion_tokens`, `total_tokens`
- Aggregated per-role (interviewer vs. user) and per-conversation
- Cost estimation based on model pricing

---

## 5. Post-Conversation Analysis

After each conversation completes, three analysis steps run:

### 5.1 Schema Validation (Deterministic)

```bash
python3 scripts/validate-adr.py <extracted_adr.yaml>
python3 scripts/review-adr.py <extracted_adr.yaml>
```

Captures: pass/fail, error list, quality warnings.

### 5.2 Quality Review (Deterministic)

Automated checks on the produced ADR:
- **Structural completeness**: % of optional fields populated
- **Alternative depth**: avg word count in `alternatives[].description`
- **Y-Statement clause coverage**: all 7 clauses present?
- **Mermaid diagram count**: how many diagrams were generated?
- **Rejection rationale coverage**: all non-chosen alternatives have `rejection_rationale`?
- **ASR extraction**: were architecturally significant requirements captured?

### 5.3 Analyst LLM Review (AI-Powered)

A third LLM pass analyzes the full conversation trace + produced ADR:

```
Analyst System Prompt:

You are an ADR process analyst. You have been given:
1. The full conversation log between an AI interviewer and a simulated user
2. The ADR YAML produced by the interviewer
3. The schema validation results
4. The test scenario definition (ground truth)

Analyze the interaction and provide a structured report:

## Conversation Quality
- **Total turns**: N
- **Wasted turns**: turns that didn't advance the ADR (greetings, clarifications of questions)
- **Missed probes**: questions the interviewer should have asked but didn't
- **Redundant questions**: information asked twice or already provided by the user
- **Socratic depth score**: 1-10 rating of how well the interviewer challenged weak answers

## ADR Artifact Quality
- **Schema compliance**: pass/fail + issues
- **Information density**: how much of the scenario's ground truth was captured?
- **Hallucination check**: did the interviewer invent information not provided by the user?
- **Y-Statement quality**: structural conformance + semantic accuracy
- **Alternative balance**: are pros/cons balanced or strawman-like?

## Process Improvement Suggestions
For each suggestion, specify:
- What to change (instruction text, question order, probing strategy)
- Where in repomix-instruction.md or SKILL.md the change would go
- Expected impact (fewer turns, better coverage, stronger ADRs)
- Priority: P0 (critical) / P1 (important) / P2 (nice-to-have)
```

---

## 6. Output Structure

All outputs go to `tests/llm_runs/`:

```
tests/llm_runs/
├── run-2026-03-08T01-00-00/
│   ├── config.json                  # models used, scenario ID, parameters
│   ├── conversation_log.json        # full turn-by-turn trace
│   ├── produced_adr.yaml            # extracted YAML artifact
│   ├── validation_result.json       # validate-adr.py output
│   ├── review_result.json           # review-adr.py output
│   ├── quality_metrics.json         # automated quality measurements
│   ├── analysis_report.md           # Analyst LLM report
│   └── tokens_usage.json            # per-model token counts
├── run-2026-03-08T01-15-00/
│   └── ...
├── aggregate_report.md              # cross-run comparison
└── improvement_backlog.md           # consolidated improvement suggestions
```

### 6.1 Aggregate Report

After N runs, generate a cross-run comparison:

| Run | Scenario | Interviewer | User | Turns | Tokens | Schema Valid | Quality Score | Key Issue |
|-----|----------|-------------|------|-------|--------|-------------|---------------|-----------|
| 1 | fictional-001 | gemini-3-pro | claude-sonnet | 14 | 12,400 | ✅ | 8/10 | Missed cost probe |
| 2 | fictional-002 | claude-sonnet | gemini-3-flash | 22 | 28,100 | ❌ | 5/10 | Missing Y-Statement |
| 3 | github-pr-001 | gemini-3-pro | gpt-5.2 | 18 | 19,600 | ✅ | 7/10 | Weak rejection rationale |

---

## 7. Metrics & Success Criteria

### 7.1 Per-Run Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Schema validation pass rate | 100% | `validate-adr.py` exit code |
| Y-Statement 7-clause completeness | 100% | Regex/structural check |
| Alternative count | ≥ 2 | Count from YAML |
| All rejection_rationale populated | 100% | Field presence check |
| Conversation turns | ≤ 20 | Turn count |
| Hallucination rate | 0% | Analyst LLM check |
| ASR extraction | ≥ 1 functional + 1 non-functional | Field presence |
| Mermaid diagram count | ≥ 1 | Regex count in descriptions |

### 7.2 Cross-Run Goals

| Goal | Target |
|------|--------|
| Schema pass rate across 10 runs | ≥ 90% |
| Average conversation turns | ≤ 18 |
| Average quality score (analyst) | ≥ 7/10 |
| Consistent behavior across model families | variance < 2 points |

---

## 8. Implementation Plan

### Phase 1: Core Harness (MVP)

Build the orchestrator script and run 3 fictional scenarios:

1. Create `tests/llm_harness.py` — orchestrator script
2. Create `tests/scenarios/` — 3 fictional scenario YAMLs
3. Wire up LiteLLM calls (`localhost:4000`)
4. Implement YAML extraction from interviewer output
5. Integrate `validate-adr.py` + `review-adr.py` as subprocess
6. Produce `conversation_log.json` + `produced_adr.yaml`
7. Run 3 scenarios, manually inspect outputs

**Deliverable**: Working harness, 3 traced conversations, validation results.

### Phase 2: Analyst & Metrics

Add the analysis layer and quality metrics:

1. Add Analyst LLM pass with structured prompt
2. Implement automated quality metrics (Y-Statement check, field coverage)
3. Generate `analysis_report.md` per run
4. Build aggregate report generator
5. Run all 8 fictional scenarios

**Deliverable**: Full analysis pipeline, 8 analyzed runs, aggregate report.

### Phase 3: Real-World Scenarios

Add GitHub PR-based and existing ADR repository scenarios:

1. Build GitHub PR fetcher (API + diff extraction)
2. Create PR → scenario converter
3. Find 2-3 OSS repos with existing ADRs
4. Create reverse-engineering scenarios
5. Run and compare results

**Deliverable**: 3-5 real-world scenario runs with analysis.

### Phase 4: Feedback Loop

Use analysis insights to improve the framework:

1. Consolidate `improvement_backlog.md` from all analyst reports
2. Implement top-priority improvements to `repomix-instruction.md`
3. Re-run all scenarios with improved instructions
4. Compare before/after metrics
5. Document findings in this file

**Deliverable**: Measurable improvement in quality scores, updated instructions.

---

## 9. Technical Requirements

### 9.1 Dependencies

```
# Addition to requirements.txt (or separate test requirements)
litellm>=1.80          # already installed (v1.81.7)
pyyaml>=6.0            # already installed
jsonschema[format]     # already installed
```

### 9.2 LiteLLM Configuration

Uses the existing Alfred LiteLLM proxy at `localhost:4000`:

```python
LITELLM_BASE_URL = "http://localhost:4000/v1"
LITELLM_API_KEY = "alfred-litellm-key"

# Default models (all available via API)
DEFAULT_INTERVIEWER_MODEL = "gpt-5.2-medium"
DEFAULT_USER_MODEL = "glm-5"
DEFAULT_ANALYST_MODEL = "gpt-5.2-high"
```

### 9.3 System Prompt Strategy

**Interviewer system prompt** = the full content of `repomix-instruction.md` (the bundle header with all authoring instructions). This is exactly what a real user would paste into ChatGPT/Claude.ai.

> **Design decision**: We use the instruction header only (not the full 350KB bundle) because the bundle includes example ADRs that inflate the context window. For testing, the interviewer should work from instructions + schema alone, which matches the worst-case real-world scenario where the AI has to ask everything from scratch.

**User system prompt** = scenario definition with persona, project context, and behavioral guidelines. The key instruction:

> "You are role-playing as {persona.name}, a {persona.role}. You are being interviewed by an AI assistant to create an Architecture Decision Record. Answer the questions based on the project context below. Do NOT volunteer information that hasn't been asked. Answer using the numbered format the interviewer uses."

### 9.4 Bundle Variants to Test

| Variant | Description | Purpose |
|---------|-------------|---------|
| `full-bundle` | Complete `adr-governance-bundle.md` (~350KB) | Test with maximum context |
| `instructions-only` | `repomix-instruction.md` header (~28KB) | Test instruction clarity in isolation |
| `instructions+schema` | Header + `adr.schema.json` (~53KB) | Minimal viable bundle |

---

## 10. README Integration

Add a section to the project README:

```markdown
### 🧪 Automated Quality Testing (Triple-LLM Harness)

This framework includes an automated testing harness that validates the ADR
authoring skill using simulated conversations between two LLMs:

- **Interviewer LLM**: Receives the governance bundle and conducts the
  Socratic interview
- **User LLM**: Role-plays a developer with a predefined scenario
  (fictional, GitHub PR-derived, or real ADR reverse-engineering)

After each conversation, the produced ADR is schema-validated and analyzed
for quality. Results are stored in `tests/llm_runs/`.

```bash
# Run a single scenario
python3 tests/llm_harness.py --scenario tests/scenarios/fictional-001.yaml

# Run all scenarios
python3 tests/llm_harness.py --all

# Run with specific models
python3 tests/llm_harness.py --all \
  --interviewer gemini-3-pro \
  --user claude-sonnet \
  --analyst gemini-3-pro
```

See [docs/research/automated-triple-llm-testing.md](docs/research/automated-triple-llm-testing.md)
for full methodology.
```

---

## 11. Design Decisions (Resolved Open Questions)

### Q1. Bundle size vs. quality tradeoff

> **Should the Interviewer get the full 350KB bundle or just the instruction header?**

**Recommendation: Instructions + Schema + 1 Example ADR (~70KB) as default. Full bundle as optional comparison run.**

Reasoning:
- The full 350KB bundle is what a real user uploads to ChatGPT/Claude — but most of that is 8 example ADRs (~17KB each). The examples serve as style guides, not as structural instructions.
- The instruction header alone (~28KB) has all the rules but no concrete "what good looks like" reference. Models follow instructions better when they have one worked example to anchor on.
- **The sweet spot is: instruction header + schema + one reference ADR** (e.g., ADR-0001, the DPoP decision — it's the most complete example at ~17KB with Mermaid diagrams, balanced alternatives, and a well-formed Y-Statement).
- This ~70KB payload fits comfortably in any modern model's context window, is cheap to process per-turn, and closely matches a "minimal viable upload" that a real user might do.
- Run a subset of scenarios (2-3) with the **full bundle** as well, to measure whether the extra examples improve or degrade quality (some models may get confused by over-saturation).

Implementation:
```python
BUNDLE_VARIANTS = {
    "default": ["repomix-instruction.md", "schemas/adr.schema.json",
                 "examples-reference/ADR-0001-dpop-over-mtls....yaml"],  # ~70KB
    "minimal": ["repomix-instruction.md", "schemas/adr.schema.json"],    # ~53KB
    "full":    ["adr-governance-bundle.md"],                             # ~350KB
}
```

### Q2. User LLM evasiveness calibration

> **How evasive should the simulated user be?**

**Recommendation: Three-tier evasiveness mapped to scenario difficulty, with specific behavioral knobs.**

| Difficulty | Evasiveness | Behavior |
|------------|-------------|----------|
| **easy** | Cooperative | Answers fully, volunteers relevant context, provides concrete numbers when asked. May even suggest alternatives proactively. |
| **medium** | Realistic | Answers questions directly but doesn't volunteer extra info. Vague on costs/timelines until pressed specifically. Acknowledges risks when asked. This is the **default** — it simulates a typical busy developer. |
| **hard** | Evasive | Gives short answers (1-2 sentences). Pushes back on questions ("why do we need to document that?"). Contradicts self once mid-interview. Claims high confidence with weak justification. Provides only one alternative initially and says "we've already decided." |

Reasoning:
- The point of testing is not to pass every time — it's to find where the instructions break. Easy scenarios validate the happy path. Medium tests normal friction. Hard scenarios are adversarial stress tests that expose gaps in the Socratic probing instructions.
- A user who says "we've already decided, just write the ADR" is the **hardest real-world case** — the interviewer must push for alternatives and challenge the confidence level. This is exactly what section "Socratic probing guidelines" in the instructions is designed for.
- We should aim for: **easy = always produces valid ADR, medium = produces valid ADR 90%+ of the time, hard = produces valid ADR 70%+ of the time.** If hard scenarios pass at 90%+, our probing instructions are probably too weak (the user isn't really being evasive).

Implementation: The `answer_style` and `evasion_points` fields in the scenario YAML drive this. The User LLM system prompt gets explicit behavioral instructions:

```
# For hard difficulty:
You are a reluctant participant. You believe the team has already decided and
this documentation exercise is bureaucratic overhead. You will:
- Give minimal answers (1-2 sentences) unless the interviewer specifically
  asks for more detail
- When first asked about alternatives, say "we already evaluated options
  internally, [chosen option] is the clear winner"
- When asked about costs, say "I'd have to check with finance"
- When asked about risks, initially minimize them ("we've handled similar
  things before")
- Contradict yourself once: early in the interview mention that team capacity
  is "fine", but later when asked about timeline say "we're already stretched thin"
```

### Q3. Determinism & temperature strategy

> **Should we use temperature=0 for reproducibility or temperature=0.7 for realistic variance?**

**Recommendation: Split strategy — low temperature for User LLM, default for Interviewer. Run each scenario twice minimum.**

| Role | Temperature | Rationale |
|------|-------------|-----------|
| **User LLM** | `0.3` | The user's persona and answers should be consistent across runs. We're testing the interviewer, not the user. Low temperature keeps the user's answers stable so we can meaningfully compare interviewer behavior. |
| **Interviewer LLM** | `0.7` (default) | The interviewer should behave naturally. Real-world variance in how it phrases questions, what it probes, and how it structures the YAML is exactly what we want to observe. Using `temperature=0` would create unnaturally rigid conversations that don't reflect actual chat usage. |
| **Analyst LLM** | `0.3` | Analysis should be consistent and precise. Low temperature reduces hallucination risk in the quality assessment. |

Reasoning:
- `temperature=0` (greedy decoding) in practice makes conversations stilted and repetitive. It also tends to make models follow the most "obvious" path, which would inflate our quality scores artificially — a false positive.
- The variance itself is valuable data. If the same scenario produces a 9/10 ADR on one run and a 4/10 on another, that tells us the instructions have a fragile control point that needs strengthening.
- Running each scenario **exactly 2 times** keeps costs reasonable while capturing variance. If the two runs differ by >3 quality points, flag it and add a 3rd run to break the tie.

Implementation:
```python
TEMPERATURE_CONFIG = {
    "interviewer": 0.7,
    "user": 0.3,
    "analyst": 0.3,
}
RUNS_PER_SCENARIO = 2
VARIANCE_THRESHOLD = 3  # trigger 3rd run if quality delta > 3 points
```

### Q4. Cost control

> **Can we afford 10 scenarios × 2-3 runs × multiple LLM calls?**

**Recommendation: Cost is not a constraint. The user has unlimited subscriptions for GPT-5.2, GLM-5, and other models. Focus on quality, not cost optimization.**

Token budget estimate (for reference, not as a constraint):
- Average conversation: ~15 turns × 2 LLM calls/turn = ~30 API calls
- Average tokens per call: ~2K prompt + ~1K completion = ~3K tokens/call
- Per conversation: ~90K tokens (interviewer + user combined)
- Analyst pass: ~30K tokens (full trace as input + structured report)
- **Per scenario-run: ~120K tokens total**
- **10 scenarios × 2 runs = 20 runs → ~2.4M tokens**

Since cost is not a concern, the priority is **quality and diversity**:
1. **Use the best model available for each role** — `gpt-5.2-medium` or `gpt-5.2-high` for the Interviewer.
2. **Use a different model family for the User** — `glm-5` provides genuine cross-model diversity.
3. **Sequential execution with delays** — still needed to avoid burst rate limits on the proxy, not for cost reasons.
4. **429 handling** — the harness should still handle rate limits with exponential backoff, as shared proxy has burst limits.

Implementation:
```python
DEFAULT_USER_MODEL = "glm-5"                 # different family, good quality
DEFAULT_INTERVIEWER_MODEL = "gpt-5.2-medium" # high quality with moderate reasoning
DEFAULT_ANALYST_MODEL = "gpt-5.2-high"       # deep reasoning for analysis
INTER_RUN_DELAY_SECONDS = 5
MAX_RETRIES_ON_429 = 3
```

### Q5. GitHub PR extraction: attribution & ethics

> **Is it appropriate to use public GitHub PRs for test scenarios?**

**Recommendation: Yes — public PRs are public data. Attribute clearly, include disclaimers, and never imply the generated ADR represents the project's actual decision.**

Rules:
1. Every PR-derived scenario YAML includes a `source` block with the full PR URL, repo name, author attribution, and extraction date.
2. The generated ADR includes a clear disclaimer in the `audit_trail`:
   ```yaml
   audit_trail:
     - event: "created"
       by: "AI Test Harness"
       at: "2026-03-08T00:00:00Z"
       details: >-
         Synthetic ADR reverse-engineered from public GitHub PR discussion
         (https://github.com/org/repo/pull/NNN) for framework testing purposes.
         This does NOT represent an official decision of the source project.
   ```
3. Pick PRs with **rich discussion threads** — the more alternatives discussed in comments, the richer the scenario. PRs with only a description and no discussion are poor candidates.
4. Prefer PRs that are **merged** (the decision was actually made) rather than open/draft PRs.
5. The scenario stores only extracted context (problem, alternatives, constraints) — we don't copy the PR body verbatim. The User LLM role-plays with this extracted context as its knowledge.

Good candidate criteria:
- PR has 10+ comments with substantive technical discussion
- PR description includes a "why" section or references an RFC/design doc
- Multiple approaches were considered and compared
- The repo has a permissive license (Apache 2.0, MIT)

### Q6. Thinking/reasoning models for the Analyst

> **Should we use a reasoning-enabled model for the Analyst pass?**

**Recommendation: Yes — use a reasoning model for the Analyst. The analysis task is one-shot (runs once per conversation, not per-turn) and requires deep judgment, making it ideal for extended thinking.**

Reasoning:
- The Analyst's job requires **nuanced multi-step judgment**: detecting hallucinations (comparing every claim in the ADR against the conversation log), evaluating Socratic depth (did the interviewer challenge weak answers?), spotting missed probes (what should it have asked?), and diagnosing instruction gaps. These are exactly the tasks reasoning models excel at.
- The Analyst runs **once per conversation** — not per-turn. So the extra latency (30-90 seconds for a reasoning model vs. 5-10 seconds for a standard model) is acceptable. There's no interactive loop to slow down.
- The token overhead is ~2x for reasoning tokens on top of the output, but for a single-shot 30K-token input it's still well within reason.
- Using a **different model family** for the Analyst vs. the Interviewer adds a cross-model perspective. If Gemini interviews, having Claude analyze (or vice versa) catches blind spots.

Model selection for the Analyst:

| Preference | Model | Why |
|------------|-------|-----|
| Primary | `gpt-5.2-high` | High reasoning budget, excellent at structured analysis, catches subtle issues |
| Alt-1 | `glm-5-thinking` | Different model family — adds cross-model perspective to the analysis |
| Alt-2 | Gemini Pro (CLI) | If we add CLI wrapping — native Google model for diversity |

Implementation: Use `gpt-5.2-high` as the default Analyst from Phase 1 onward — cost is not a constraint, so no reason to start with a weaker model.

---

## 12. Next Steps

1. **Review this proposal** — align on scope and priorities
2. **Phase 1 implementation** — build the harness, write 3 scenarios, run them
3. **Evaluate Phase 1 results** — are the conversations realistic? Is the YAML valid?
4. **Iterate** — refine scenarios, add analysis, expand to real-world sources
