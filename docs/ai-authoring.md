# AI-Assisted Authoring & Pre-Review

ADRs are not meant to be filled in manually like a form. They are authored through **AI-assisted dialogue** — the AI asks probing questions, challenges weak rationale, surfaces missing edge cases, and iteratively refines the document until it is clear, complete, and internally consistent.

The framework supports **two creation modes**:

- **Socratic interview** (default) — The AI walks you through every section via interactive questioning. Best when starting from scratch or when the decision is still forming.
- **Artifact-driven** — You upload existing materials (meeting transcripts, slides, design docs, images, etc.) and the AI extracts an ADR from them, asking targeted questions only for what's missing. Best when the decision has already been discussed and context exists in documents.

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

1. **Author new ADRs (Socratic mode)** — The AI walks you through every section via Socratic dialogue. It doesn't accept vague answers — it pushes back on ambiguous terms, asks for measurable constraints, and demands that alternatives are genuinely competitive
2. **Author new ADRs (artifact-driven mode)** — Upload meeting transcripts, PowerPoint slides, PDFs, design documents, architecture diagrams, images, email threads, or other reference materials. The AI extracts relevant information, presents a structured summary mapped to ADR schema sections, identifies gaps, and asks targeted questions only for what's missing
3. **Review existing ADRs** — Structured semantic review: clarity, completeness, logical consistency, assumption risks, and cross-reference consistency with other decisions
4. **Supersede ADRs** — Guides the creation of a replacement ADR while maintaining the supersession chain (`lifecycle.supersedes` / `lifecycle.superseded_by`)
5. **Validate YAML** — Checks conformance against the JSON Schema and flags semantic issues

### Artifact-driven mode — supported file types

The AI can process any file type supported by the platform:

| Category | Formats |
|---|---|
| **Text** | Meeting transcripts, notes, Markdown, plain text, chat exports |
| **Documents** | PDF, Word (.docx), PowerPoint (.pptx) |
| **Visual** | Architecture diagrams, whiteboard photos, screenshots, decision matrices, any image |
| **Structured** | RFC drafts, design documents, email threads, Slack/Teams exports |

The AI reads all uploaded files, maps extracted information to ADR schema sections, flags contradictions across documents, and asks only about what's missing.

### Copying the skill to other repositories

The skill is designed to be portable. Copy the `.skills/adr-author/` directory into any repository where developers will be authoring ADRs:

```bash
cp -r path/to/adr-governance/.skills/adr-author/ your-repo/.skills/adr-author/
```

Agents like Antigravity, Claude Code, and Copilot will automatically discover the skill and offer ADR authoring capabilities when you ask them to create an ADR.

---

## Web Chat (No Skill Required)

Don't have access to a coding agent? The Repomix bundle (`adr-governance-bundle.md`) includes **embedded AI instructions** that replicate the skill's portable authoring/query workflows — upload the single file to any web-based AI chat:

- **ChatGPT** (with Code Interpreter for large file search)
- **Claude.ai** (200K–1M token context)
- **Google Gemini** (1M+ token context)
- **Microsoft Copilot** (web)

The AI will be able to author new ADRs through Socratic dialogue or from uploaded documents, query the decision log with citations, review ADRs for completeness, summarize decisions for stakeholders, and validate YAML against the schema — all from a single uploaded file. Repository-side CI setup, approval verification, and PR enforcement still happen after the ADR is copied into your repo.

Repo-local helper scripts like [`scripts/review-adr.py`](../scripts/review-adr.py) and [`scripts/summarize-adr.py`](../scripts/summarize-adr.py) are documented below for native checkout workflows; they are not embedded in the web-chat bundle itself.

### Artifact-driven mode in web chat

To use artifact-driven mode, upload the `adr-governance-bundle.md` **plus** your reference documents (transcripts, slides, PDFs, images, etc.) in the same prompt. The AI will detect the additional files and switch to extraction mode automatically. See the starter prompts in the quickstart guide for copy-paste-ready examples.

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
