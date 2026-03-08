# Visual Prompt — Triple-LLM Testing Harness

## Style Primer

The following instructions define the global visual style for a high-resolution 16:9 technical infographic.
 
IMPORTANT META RULES (DO NOT DRAW THESE WORDS):
- Treat this entire block as style guidance only.
- Do NOT render any heading or label that mentions "style", "primer", "template", "technical systems", or similar meta concepts.
- The ONLY text that should appear inside the image is:
  • The diagram title given in the slide-specific prompt, without quotation marks.
  • The region/box headings and labels described in the slide-specific prompt.
  • The one-line footer sentence provided in the slide-specific prompt (if any).
- Do NOT invent any extra top banner, header bar, or tagline summarizing the style guidelines.
 
GLOBAL VISUAL STYLE FOR TECHNICAL SYSTEM / PROCESS DIAGRAMS
 
Create a high-resolution 16:9 infographic suitable for technical presentations, research decks, architectural reviews, or product-strategy briefings.
 
Overall look:
- Very clean, flat, vector-illustration style.
- Visual tone similar to product one-pagers from modern AI/tech companies and enterprise-architecture diagrams.
- Palette: calm, professional colors — desaturated blues, teals, purples, and greys — with 1–2 accent colors (orange, lime, or magenta) used sparingly for emphasis.
- **WHITE BACKGROUND** (mandatory).
- Typography: geometric sans-serif, highly legible, with a clear hierarchy between title, section headings, and labels.
- Use thin but readable callout text; avoid long paragraphs — prefer short phrases and labels attached to nodes.
- No real company logos; instead use abstract icons and generic labels like "Module A", "Service X", "Engine", "Component", "Layer 1".
 
Visual grammar / metaphors:
- For flows, data movement, and processes:
  - Use arrows, pipelines, branching paths, circuit-flow lines, or conveyor-belt metaphors.
  - Represent linear sequences as chains of nodes or boxes with numbered arrows.
  - Represent feedback loops as circular or spiral flows.
- For modules, engines, and services:
  - Use packaged blocks, containers, pods, gears, stacked layers, or nested shapes.
  - "Black box" components should appear as opaque modules; configurable logic may be shown as partially transparent or layered.
- For APIs, interfaces, and boundaries:
  - Use ports, sockets, connectors, lego-style pieces, plug-in edges, or adapter blocks.
- For trust, validation, and correctness:
  - Use shields, checkmarks, certificates, audit sheets, or sealed boxes.
  - For probabilistic/heuristic algorithms, consider gradients, fuzzy boundaries, or overlapping zones.
- For flexibility and extensibility:
  - Use branching trees, interchangeable puzzle pieces, modular grids, or adapter layers.
- For constraints and limitations:
  - Use padlocks, chains, narrow pipes, bottleneck icons, or boxed-in shapes.
- For comparisons and trade-offs:
  - Use dual tracks, split-screen layouts, 2×2 matrices, mirrored diagrams, or balance scales.
- For hierarchy or decomposition:
  - Use layered-architecture diagrams, nested boxes, pyramid stacks, onion models, or hub-and-spoke patterns.
 
Image structure rules:
- Partition the canvas into 2–4 clearly separated regions (e.g. left/right columns, top/middle/bottom bands, or quadrants).
- Ensure each region contains at most one core idea plus 3–6 short labeled visual elements.
- Use arrows, numbering, or other directional cues to make the reading order unambiguous (typically left→right or top→bottom).
- Maintain ample whitespace; avoid overcrowding and visual noise.
- Reserve a small bottom strip for a concise caption or "key takeaway" sentence that summarizes the whole diagram in one line.
- When a slide-specific prompt provides a footer sentence, copy that sentence verbatim into the bottom strip. Do not prepend or append any extra wording such as "The diagram shows…", "Summary:", or similar phrases unless explicitly included in the slide-specific instructions.
 
Context focus (general-purpose):
- The diagram should adapt to arbitrary technical domains, such as:
  - System architectures (distributed systems, microservices, data pipelines).
  - Algorithms (cryptographic protocols, ML training & inference flows, distributed consensus).
  - Relationships between entities (clients ↔ servers, producers ↔ consumers, modules ↔ subsystems).
  - Technical processes (onboarding flows, orchestration logic, lifecycle states).
  - Conceptual frameworks (taxonomies, capability maps, layered models).
  - Research or experimental setups.
- Always show at least two interacting entities (e.g. Client ↔ Engine, Component ↔ Database).
- Represent data, control, or process flow in a clearly directional way (with arrows or equivalent).
- Make constraints, dependencies, and execution order visually explicit where relevant.
- Make trade-offs, separation of concerns, and layering visually obvious.
 
Reading orientation & storytelling:
- Use top→bottom when depicting phases, lifecycles, or algorithmic steps.
- Use left→right when depicting flows, pipelines, or before/after comparisons.
- Use center→periphery (hub-and-spoke or concentric patterns) when depicting ecosystems, central engines, or platforms with surrounding components.
- Ensure the final image tells a coherent "micro-story" at a glance: what the system is, how it behaves, and why the structure matters.
 
IMPORTANT LABELING RULES:
- Never use generic, structural labels such as "Panel 1", "Panel 2", "Panel A", "Upper panel", "Lower panel", "Top mini-panel", "Bottom mini-panel", or similar phrases anywhere in the image.
- Every region, box, or sub-panel that needs a heading must use a short, content-based title that reflects its subject matter, e.g. "System overview", "Input–output mapping", "Linearity property", "Time-invariance property", "Control loop", "Failure modes", etc.
- If multiple regions are related, distinguish them by concept, not by number, e.g. "Continuous-time view" vs "Discrete-time view", "Training phase" vs "Inference phase", "Sender side" vs "Receiver side".
- Apply this rule consistently to all titles, captions, legends, and labels inside the figure. Do not invent ordinal panel names; always describe what the viewer is seeing.
 
Bottom strip (final synthesis):
- In the narrow footer area, include exactly one concise one-line takeaway summarizing the main insight of the diagram, without quotation marks.
- The footer must consist only of that single sentence, with no leading text like "The diagram shows…", "This figure illustrates…", or "Summary:", unless explicitly included in the slide-specific instructions.

---

## Slide-Specific Instantiation

NOW INSTANTIATE THIS STYLE FOR:
"Triple-LLM Testing Harness — Automated ADR Quality Validation"

Goal:
- Draw a single infographic that visualizes the architecture of the triple-LLM testing harness. This harness validates ADR authoring quality by simulating realistic multi-turn conversations between three LLM roles: an Interviewer that runs the Socratic dialogue, a User that plays a domain expert, and an Analyst that reviews the generated ADR.
- The narrative arc is left→right, structured as a 4-stage pipeline: Scenario → Dialogue → Validation → Report.

Overall layout:
- Partition the canvas into four regions reading left→right, connected by bold directional arrows:
  - Left (~15% width): "Scenario Input" — the test setup.
  - Center-left (~35% width): "Multi-Turn Dialogue" — the simulated authoring conversation.
  - Center-right (~25% width): "Automated Validation" — schema + semantic + quality checks.
  - Right (~25% width): "Quality Report" — the output.
- Place a title at the top center: "Triple-LLM Testing Harness" in a prominent heading. Subtitle: "Automated ADR quality validation".

Left region — "Scenario Input":
- Region heading: "Test scenario".
- Show a YAML document icon with small field previews: "decision_context", "persona", "expected_coverage".
- Below, show 3 small category badges:
  1. "Fictional" — with annotation: "Synthetic contexts (API versioning, secrets management)"
  2. "GitHub PR-based" — annotation: "Extracted from real pull requests"
  3. "Round-trip" — annotation: "Validate against existing reference ADRs"
- An arrow leads from this region into the center-left, labeled "Scenario loaded".

Center-left region — "Multi-Turn Dialogue" (the core — most visually rich):
- Region heading: "Simulated authoring conversation".
- Show three LLM entities arranged in a triangular or linear conversation flow:
  1. Top/left: An AI brain icon colored in **teal**, labeled "Interviewer" — with annotation: "Gemini 2.5 Pro — runs Socratic ADR dialogue"
  2. Bottom/left: A person-with-AI icon colored in **orange**, labeled "User" — with annotation: "Claude 3.5 Sonnet — plays domain expert"
  3. Right: An AI magnifying-glass icon colored in **purple**, labeled "Analyst" — with annotation: "Gemini 2.5 Pro — reviews generated ADR"
- Between Interviewer and User, draw a back-and-forth loop (cyclic arrows) labeled "Multi-turn conversation" with 3–4 speech bubbles along the loop:
  - "What alternatives did you consider?"
  - "We evaluated 3 options: A, B, C…"
  - "What are the tradeoffs of option A?"
  - "ADR complete — generating YAML"
- In the center of the loop, show an ADR YAML document being progressively built — use a document icon with sections filling in (context → alternatives → decision → consequences).
- An arrow leads from the completed ADR to the Analyst and to the center-right region.

Center-right region — "Automated Validation":
- Region heading: "Multi-layer quality gate".
- Show a vertical stack of 4 validation steps, each as a box with a check icon:
  1. "JSON Schema validation" — annotation: "Structure, types, required fields"
  2. "Semantic consistency" — annotation: "Status ↔ audit trail, supersession symmetry"
  3. "Analyst LLM review" — annotation: "Socratic depth, alternative balance, rationale quality"
  4. "Quality metrics" — annotation: "Field completeness, Y-Statement presence, ASR coverage"
- Use green checkmarks or red X marks to show pass/fail states.
- An arrow leads from this stack to the right region.

Right region — "Quality Report":
- Region heading: "Run report".
- Show a report document icon with sections:
  - "Score: 87/100"
  - "Schema: PASS"
  - "Completeness: 94%"
  - "Y-Statement: PRESENT"
  - "Issues: 2 warnings"
- Below, show a small file-tree icon with:
  - "tests/llm_runs/run-<timestamp>/"
  - "  conversation.log"
  - "  generated_adr.yaml"
  - "  analysis_report.md"
- A small aggregate icon below: "Multi-scenario benchmark matrix" suggesting aggregate reporting across runs.

Visual connections and flow:
- Bold arrows connecting the four regions left→right: Scenario → Dialogue → Validation → Report.
- The center-left dialogue region should be the largest and most visually striking — it's the core innovation.
- Use teal for the Interviewer, orange for the User, and purple for the Analyst throughout the diagram to maintain visual identity.
- A subtle dashed arrow from the Report back to the Scenario, labeled "Regression tracking" — suggesting scenarios can be re-run to track quality over time.

Footer sentence (bottom strip):
Three LLMs collaborate to test ADR authoring quality automatically — no human in the loop, full schema validation, reproducible quality benchmarks.
