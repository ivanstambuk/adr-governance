# AI-Assisted Authoring & Pre-Review

ADRs are not meant to be filled in manually like a form. They are authored through **Socratic dialogue with an AI assistant** — the AI asks probing questions, challenges weak rationale, surfaces missing edge cases, and iteratively refines the document until it is clear, complete, and internally consistent.

This is a fundamental shift from traditional architecture governance: instead of the proposer writing a draft in isolation and then scheduling a meeting to "walk through" it (where reviewers discover ambiguities in real time and the meeting devolves into clarification rather than decision-making), the AI assistant resolves those ambiguities *before the first human reviewer ever sees the document*.

---

## Agent Skill

The [`.skills/adr-author/`](../.skills/adr-author/) directory follows the [agentskills.io specification](https://agentskills.io/specification) and works with:

- **Google Antigravity** (VS Code)
- **Claude Code** (terminal)
- **VS Code Copilot** (with skills support)
- Any agent implementing the Agent Skills standard

The skill guides AI assistants to author ADRs through interactive questioning — probing for Architecturally Significant Requirements (ASRs), demanding balanced alternatives (not strawmen), checking that constraints are testable, and verifying that the rationale actually connects to the stated drivers. It understands the full meta-model and governance lifecycle.

### What the skill does

1. **Author new ADRs** — The AI walks you through every section via Socratic dialogue. It doesn't accept vague answers — it pushes back on ambiguous terms, asks for measurable constraints, and demands that alternatives are genuinely competitive
2. **Review existing ADRs** — Structured semantic review: clarity, completeness, logical consistency, assumption risks, and cross-reference consistency with other decisions
3. **Supersede ADRs** — Guides the creation of a replacement ADR while maintaining the supersession chain (`lifecycle.supersedes` / `lifecycle.superseded_by`)
4. **Validate YAML** — Checks conformance against the JSON Schema and flags semantic issues

### Copying the skill to other repositories

The skill is designed to be portable. Copy the `.skills/adr-author/` directory into any repository where developers will be authoring ADRs:

```bash
cp -r path/to/adr-governance/.skills/adr-author/ your-repo/.skills/adr-author/
```

Agents like Antigravity, Claude Code, and Copilot will automatically discover the skill and offer ADR authoring capabilities when you ask them to create an ADR.

---

## Web Chat (No Skill Required)

Don't have access to a coding agent? The Repomix bundle (`adr-governance-bundle.md`) includes **embedded AI instructions** that replicate the full skill — upload the single file to any web-based AI chat:

- **ChatGPT** (with Code Interpreter for large file search)
- **Claude.ai** (200K–1M token context)
- **Google Gemini** (1M+ token context)
- **Microsoft Copilot** (web)

The AI will be able to author new ADRs through Socratic dialogue, query the decision log with citations, review ADRs for completeness, summarize decisions for stakeholders, and validate YAML against the schema — all from a single uploaded file.

See **[`docs/web-chat-quickstart.md`](web-chat-quickstart.md)** for platform-specific starter prompts and tips.

---

## Pre-Review Quality Gate

Before submitting an ADR for human review, run it through an AI semantic review using [`scripts/review-adr.py`](../scripts/review-adr.py). This ensures that the first draft a human reviewer sees is already semantically coherent and complete — turning review meetings into strategic discussions about the *decision*, not debugging sessions about what the proposer meant.

### Usage

```bash
# Generate a Socratic review prompt (pipe to your LLM)
python3 scripts/review-adr.py architecture-decision-log/ADR-0009.yaml

# Include cross-reference context from existing decisions
python3 scripts/review-adr.py architecture-decision-log/ADR-0009.yaml \
  --context-from architecture-decision-log/

# Pipe directly to an LLM
python3 scripts/review-adr.py architecture-decision-log/ADR-0009.yaml | \
  llm -m gpt-4o
```

### What the review covers

The generated prompt instructs the LLM to perform a structured review covering:

- **Semantic clarity** — are there ambiguous terms or vague claims?
- **Completeness** — are alternatives balanced, constraints testable, consequences honest?
- **Logical consistency** — does the rationale align with the pros/cons?
- **Assumption risks** — what happens if the assumptions are wrong?
- **Missing perspectives** — are there unconsidered stakeholders or alternatives?
- **Cross-reference consistency** — does this decision conflict with existing ADRs?

### Output

The AI outputs a verdict (**READY FOR REVIEW**, **NEEDS REWORK**, or **MAJOR GAPS**), a list of issues with severity, and open questions for the proposer. The proposer addresses the feedback, re-runs the check, and iterates until the ADR passes. *Then* they open the PR.

---

## Stakeholder Summaries

Not every stakeholder needs the full ADR. After a decision is made (or after an architecture review meeting), use [`scripts/summarize-adr.py`](../scripts/summarize-adr.py) to produce concise summaries for communication:

```bash
# Email-length summary (~10–15 lines: decision, rationale, alternatives, tradeoffs, impact)
python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml

# Ultra-short chat summary (3–5 lines for Slack/Teams)
python3 scripts/summarize-adr.py --format chat architecture-decision-log/ADR-0001.yaml

# Meeting recap — digest of multiple ADRs
python3 scripts/summarize-adr.py architecture-decision-log/ADR-0001.yaml \
    architecture-decision-log/ADR-0002.yaml

# Save to file
python3 scripts/summarize-adr.py -o meeting-recap.md architecture-decision-log/
```

Each summary links back to the full YAML source. For a richer, rendered view, point stakeholders to the auto-generated Markdown in [`rendered/`](../rendered/).
