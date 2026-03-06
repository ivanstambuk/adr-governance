# Web Chat Quickstart — AI-Assisted ADR Authoring

> **Use this guide when you only have access to a web-based AI chat** (ChatGPT, Microsoft Copilot, Claude.ai, Google Gemini) and cannot run the `adr-author` skill locally.

## How It Works

The `adr-governance-bundle.md` file contains the **entire ADR governance framework** in a single file:

- The JSON Schema (all fields, enums, and constraints)
- The AI skill instructions (how to walk you through ADR creation)
- The governance process, glossary, and documentation
- All existing ADRs (decision log + reference examples)
- Validation logic and review scripts (as reference)
- A YAML template for new ADRs
- **Embedded instructions** that tell the AI how to act as your ADR authoring assistant

Upload it to any AI chat, and the AI will be able to:

1. **Author new ADRs** — through Socratic dialogue (probing questions, challenging rationale)
2. **Query the decision log** — "What did we decide about token binding?" → cited answer with ADR IDs
3. **Review ADRs** — structured completeness and quality audit
4. **Summarize ADRs** — email or chat format for stakeholder communication
5. **Explain the governance process** — lifecycle, status transitions, review rules
6. **Validate ADR YAML** — check against the schema and flag issues

## Step 1: Generate the Bundle

```bash
./scripts/bundle.sh
```

This creates `adr-governance-bundle.md`. The bundle file size varies as the ADL grows. Run `wc -c adr-governance-bundle.md` to check the size. Most AI platforms can handle it within their context windows:

## Step 2: Upload and Prompt

Upload `adr-governance-bundle.md` to your AI chat and paste one of the starter prompts below.

If your organization's decision log has additional ADRs beyond the examples, make sure they are in `architecture-decision-log/` before bundling — the bundle script includes them automatically.

---

## Starter Prompts

### Creating a New ADR (Interactive)

#### ChatGPT

```
I've uploaded the adr-governance bundle. This file contains a complete ADR governance
framework with embedded instructions at the end under "# Instruction".

Please read those instructions, then guide me through creating a new Architecture
Decision Record using Socratic dialogue — ask me questions one at a time, challenge
weak reasoning, and generate valid YAML at the end.

My decision is about: [describe your decision]
```

#### Claude.ai

```
I've attached the adr-governance framework bundle. It contains embedded instructions
(search for "# Instruction" near the end), a JSON Schema, process documentation,
example ADRs, and a YAML template.

Please follow those embedded instructions to guide me through authoring a new ADR
using Socratic dialogue. Interview me step by step — don't ask for everything at once.

The decision I need to document: [describe your decision]
```

#### Google Gemini

```
I've uploaded the ADR governance framework bundle. Please read the embedded instructions
(look for "# Instruction" at the end of the file), then walk me through creating a
new Architecture Decision Record step by step.

Search the file for "adr-template.yaml" to find the template, and for "adr.schema.json"
to understand the valid fields and values.

I need to decide: [describe your decision]
```

#### Microsoft Copilot

```
This file contains an ADR (Architecture Decision Record) governance framework. At the
end of the file there are instructions under "# Instruction" — please read them.

Then help me create a new ADR by asking me questions about my architectural decision,
following the step-by-step process described in those instructions.

My decision: [describe your decision]
```

---

### Creating an ADR from Documents (Artifact-Driven)

> **Use this when you have existing materials** — meeting transcripts, PowerPoint slides, design documents, PDFs, images, architecture diagrams, email threads, or any other reference materials — and want the AI to extract an ADR from them automatically.

Upload the `adr-governance-bundle.md` **plus** your artifact files, then paste one of these prompts:

#### ChatGPT

```
I've uploaded the adr-governance bundle and several additional documents.
The bundle contains the ADR governance framework with instructions under "# Instruction".

Please read those instructions (specifically the "Artifact-driven mode" section), then:
1. Read and analyze ALL the other uploaded files
2. Extract information relevant to an Architecture Decision Record
3. Show me a structured extraction summary — what you found mapped to each ADR section
4. Ask me targeted questions only for what's missing
5. Generate valid ADR YAML at the end

The uploaded documents are: [briefly describe what you uploaded, e.g., "meeting transcript
from our architecture review and the vendor comparison slides"]
```

#### Claude.ai

```
I've attached the adr-governance framework bundle along with additional documents.
The bundle has embedded instructions — search for "Artifact-driven mode" in the
"# Instruction" section near the end.

Please follow the artifact-driven workflow:
- Analyze all the attached documents
- Present an extraction summary showing what ADR sections you could fill from my documents
- Ask me targeted questions only for gaps
- Generate the complete ADR YAML

The additional files are: [briefly describe what you uploaded]
```

#### Google Gemini

```
I've uploaded the ADR governance framework bundle plus additional reference documents.
Please read the embedded instructions (look for "# Instruction" at the end, specifically
the "Artifact-driven mode" section).

Analyze all uploaded documents and extract an Architecture Decision Record from them.
Show me what you found mapped to each ADR section, flag any gaps or contradictions,
ask me targeted questions for missing information, then generate valid YAML.

Search the bundle for "adr-template.yaml" for the template and "adr.schema.json"
for the schema.

The documents I uploaded are: [briefly describe what you uploaded]
```

#### Microsoft Copilot

```
I've uploaded an ADR governance framework file and additional documents. The framework
file has instructions under "# Instruction" at the end — please read the
"Artifact-driven mode" section.

Analyze my additional documents and extract an Architecture Decision Record:
1. Show me what information you found for each ADR section
2. Ask only about what's missing
3. Generate the ADR YAML

My documents are: [briefly describe what you uploaded]
```

---

### Querying the Decision Log

```
I've uploaded our ADR governance bundle. Please read the embedded instructions under
"# Instruction", then answer this question by searching the ADR files in the bundle:

[your question, e.g., "What did we decide about sender-constrained tokens and why?"]

Cite specific ADR IDs and include the status of each relevant decision.
```

---

### Reviewing an ADR

```
I've uploaded our ADR governance bundle for context. Please read the embedded
instructions under "# Instruction".

Now review the following ADR YAML for completeness, quality, and schema compliance.
Give me a structured verdict (READY FOR REVIEW / NEEDS REWORK / MAJOR GAPS) with
a numbered list of issues.

[paste your ADR YAML here]
```

---

## Platform Tips

| Platform | Tip |
|---|---|
| **ChatGPT** | If the response seems shallow, ask: "Use Code Interpreter to search the uploaded file for the relevant ADR sections." ChatGPT can use Python to `grep` through the file. |
| **Claude.ai** | Claude loads the full file into context. For long conversations, consider using a **Claude Project** with the bundle as pinned knowledge — then you don't need to re-upload every conversation. |
| **Google Gemini** | Gemini has 1M+ token context — it can ingest the entire bundle trivially. If you have additional context files, you can upload up to 10 files per prompt. |
| **Microsoft Copilot** | If your org limits file size to 1 MB, the bundle should fit (~350 KB). If the file needs to be `.txt`, rename it: `cp adr-governance-bundle.md adr-governance-bundle.txt`. Copilot's reasoning is more limited — be more explicit in follow-up prompts. |

## After the AI Generates Your ADR

The AI will output complete ADR YAML. To finalize:

1. **Copy the YAML** and save it as `architecture-decision-log/ADR-NNNN-short-kebab-case-title.yaml`
2. **Validate locally** (recommended):
   ```bash
   pip install jsonschema pyyaml yamllint
   python3 scripts/validate-adr.py architecture-decision-log/ADR-NNNN-title.yaml
   ```
3. **Open a pull request** on a branch named `adr/NNNN-short-title`
4. **CI validates automatically** — the PR becomes the decision forum

## Re-bundling After Changes

Whenever you add, modify, or supersede an ADR, re-run the bundle script to keep the bundle current:

```bash
./scripts/bundle.sh
```

The bundle always reflects the latest state of your decision log.
