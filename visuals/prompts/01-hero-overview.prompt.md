# Visual Prompt — Hero Overview: What This Framework Does

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
"ADR Governance — Schema-Governed, AI-Native Architecture Decision Records"

Goal:
- Draw a single, visually striking infographic that communicates the full value proposition of the ADR governance framework at a glance. This is a "hero image" for the top of a GitHub README. It must be immediately engaging and tell the story in 5 seconds of viewing.
- The narrative arc is left→right: broken process → structured framework → governed outcomes.

Overall layout:
- Partition the canvas into three regions, reading left→right:
  - Left (~25% width): "The Problem" — why current approaches fail.
  - Center (~50% width): "The Framework" — what this system provides.
  - Right (~25% width): "The Outcome" — what you get.
- Use a subtle gradient or tonal shift across the three regions to reinforce the left→right narrative: the left region should feel slightly darker or muted (representing the broken status quo), the center should be the most visually rich and vibrant (the framework), and the right should feel clean and resolved (the outcome).
- Place a title at the top center of the canvas: "ADR Governance" in a large, bold heading.

Left region — "The Problem":
- Region heading: "Status quo" or "Without structured governance".
- Show 3–4 visual pain points, each as a small icon with a short label:
  1. A meeting-room / calendar icon with label: "Decisions made in meetings — context lost immediately"
  2. A scattered-documents / chat-bubbles icon with label: "Buried in Slack, wikis, and ticket comments"
  3. A broken-chain or disconnected-nodes icon with label: "No link between decisions and code"
  4. A clock or hourglass icon with label: "Decisions rot — no scheduled review"
- Use muted, desaturated styling for these icons — grey tones, dashed outlines — to visually convey that this is the "before" state.
- A large arrow leads from this region into the center region, implying transformation.

Center region — "The Framework" (hub-and-spoke):
- Region heading: "ADR Governance Framework".
- At the center, draw a prominent node representing the ADR YAML file — a document icon or structured-data block labeled "ADR" with small field previews: "context", "alternatives", "decision", "consequences", "approvals".
- Radiating outward from this central ADR node, draw 6 spokes connecting to surrounding capability nodes, each as a distinct small icon with a label:
  1. Shield/checkmark icon → "JSON Schema Validation" — with a tiny annotation: "Draft 2020-12 meta-model"
  2. Git branch / PR icon → "GitOps Governance" — annotation: "PR-based status transitions"
  3. Robot/AI brain icon → "AI Socratic Authoring" — annotation: "Probing questions, gap analysis"
  4. Pipeline/gear icon → "CI/CD Enforcement" — annotation: "5 platforms, merge gate"
  5. Document-render icon → "Rendered Markdown" — annotation: "Human-friendly views, auto-generated"
  6. Bundle/package icon → "ADL Bundle" — annotation: "Machine-readable, cross-repo"
- Use the full accent palette here — teal and blue for the spokes and nodes, with orange or magenta highlights on 1–2 key capabilities (AI Socratic Authoring and CI/CD Enforcement) to draw the eye.
- Keep lines thin and clean; don't overcrowd. Each spoke should have clear visual separation.

Right region — "The Outcome":
- Region heading: "What you get" or "Governed decisions".
- Show 4 outcome indicators, each as an icon with a short label:
  1. A traceable-chain or linked-nodes icon → "Every decision traceable — who, when, why"
  2. An audit/clipboard icon → "Audit-ready decision log"
  3. A code-compliance / shield-with-code icon → "AI-enforced code compliance"
  4. An async/distributed-team icon → "Asynchronous, timezone-proof review"
- Use clean, confident styling — solid outlines, green or teal accents — to convey that this is the "after" state, resolved and governed.
- Optionally, a subtle checkmark or seal near the bottom of this region reinforcing "governed".

Visual connections:
- A bold arrow from the left region into the center region, suggesting transformation.
- Thin arrows or flow lines from the center spokes toward the right region, suggesting that the framework produces the outcomes.
- The overall visual flow must be unmistakably left→right: problem → framework → outcome.

Footer sentence (bottom strip):
Schema-governed, AI-native Architecture Decision Records — structured, traceable, enforceable by design.
