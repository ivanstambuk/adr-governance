# Visual Prompt — AI-Native ADR Authoring Flow

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
"AI-Native ADR Authoring — From Intent to Governed Decision"

Goal:
- Draw a single infographic that visualizes the end-to-end authoring flow of an ADR, from the proposer's initial intent through AI-assisted Socratic dialogue to a governed, merged decision. This is the key differentiator of the framework and must clearly communicate why AI-native authoring is superior to manual template-filling or meeting-based decisions.
- The narrative arc is left→right, structured as a 3-stage pipeline: Intent → AI Dialogue → Governed Review.

Overall layout:
- Partition the canvas into three regions reading left→right, connected by bold directional arrows:
  - Left (~20% width): "Decision Intent" — the trigger.
  - Center (~50% width): "AI Socratic Dialogue" — the iterative authoring loop.
  - Right (~30% width): "Governed Review & Merge" — the human review and outcome.
- Place a title at the top center: "AI-Native ADR Authoring" in a prominent heading. Subtitle: "From intent to governed decision".

Left region — "Decision Intent":
- Region heading: "Decision needed".
- Show a person icon (an architect, engineer, or team lead silhouette — abstract, not gendered) with a thought bubble or callout containing a short phrase: "We need to decide on X".
- Below the person, show 2–3 small icons representing the raw inputs that feed into the process:
  1. A document icon labeled "Business drivers & constraints"
  2. A codebase/repo icon labeled "Existing ADL context"
  3. A standards/book icon labeled "Industry standards & patterns"
- An arrow leads from this region into the center, labeled "Proposer initiates".

Center region — "AI Socratic Dialogue" (the core — most visually rich):
- Region heading: "Iterative AI-assisted authoring".
- This is the heart of the diagram. Show a back-and-forth dialogue loop between two entities:
  - On one side: a person icon (the proposer) — same abstract style as the left region.
  - On the other side: an AI agent icon (brain, sparkle, or robot silhouette — abstract and clean).
- Between them, draw a cyclic loop (circular or oval flow) with 4–5 labeled stages around the loop:
  1. "AI probes for gaps" — with a small annotation: "What alternatives did you consider? What are the risks?"
  2. "Proposer responds" — annotation: "Provides context, rationale, constraints"
  3. "AI challenges assumptions" — annotation: "Is this consistent with ADR-0003? What if the constraint changes?"
  4. "Proposer refines" — annotation: "Strengthens rationale, adds missing tradeoffs"
  5. "AI validates completeness" — annotation: "All required fields populated, cross-references consistent"
- Show the ADR YAML document being progressively built during this loop — a small document icon near the center of the loop that grows or fills in with each iteration. Use a visual metaphor like a progress bar, sections lighting up, or layers being added to suggest progressive construction.
- Add 5–6 small callout labels around the loop highlighting what the AI does:
  - "Surfaces unstated assumptions"
  - "Demands ≥ 2 balanced alternatives"
  - "Checks cross-reference consistency"
  - "Verifies schema compliance"
  - "Auto-generates 7-clause Y-Statement"
  - "Classifies decision level (strategic / tactical / operational)"
- The loop should have a clear exit point (arrow out) labeled "ADR complete — ready for review" leading to the right region.
- Use teal/blue for the AI elements and a warm accent (orange or amber) for the proposer elements, creating a clear visual dialogue between the two parties.

Right region — "Governed Review & Merge":
- Region heading: "Asynchronous human review".
- Show a pipeline of 3 steps, top→bottom or arranged vertically:
  1. A PR/code-review icon with label: "Pull request opened" — annotation: "CI validates schema + semantics automatically"
  2. Multiple reviewer icons (2–3 small person silhouettes) with label: "Stakeholders review asynchronously" — annotation: "No meeting required — full context in the PR"
  3. A merge/checkmark icon with label: "Decision enacted" — annotation: "PR merged → status transitions to accepted"
- Below these steps, a small callout box with the key insight: "By the time human reviewers see the ADR, low-hanging issues are already resolved"
- Use green accents for the approval/merge elements to convey resolution and confidence.

Visual connections and flow:
- Bold arrow from left region → center region, labeled "Proposer initiates".
- The center region's internal loop is the visual centerpiece — it should be the largest, most eye-catching element.
- Bold arrow from center region → right region, labeled "ADR complete".
- Subtle thin arrow from right region back to center region (dashed), labeled "Changes requested → rework" — showing that review can send the ADR back into the Socratic loop.
- The overall left→right flow must be unmistakable: intent → AI dialogue → governed outcome.

Contrast callout (optional, if space permits):
- A small, muted "traditional approach" strip placed only at the bottom of the center region, directly above the footer sentence, showing the contrast:
  - "Traditional: fill template manually → schedule meeting → discover gaps live → iterate in meetings"
  - "AI-native: Socratic dialogue resolves gaps before any human review"
- Keep this very compact and visually subordinate — it's supporting context, not the main story.

Footer sentence (bottom strip):
AI resolves ambiguities before the first human reviewer sees the document — review meetings become strategic discussions, not debugging sessions.
