# Visual Prompt — Real-World ADR Showcase

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
"Real-World ADR Showcase — 15 Decisions Across Three Architectural Altitudes"

Goal:
- Draw a single infographic that visualizes the 15 reverse-engineered real-world ADRs organized by their decision level (strategic, tactical, operational). This showcases the breadth of the ADR meta-model by demonstrating it can capture real architectural decisions from prominent open-source projects across all three altitudes.
- The narrative arc is top→bottom, structured as a three-tier pyramid or layered stack representing architectural altitude.

Overall layout:
- Use a layered/tiered layout with three horizontal bands, reading top→bottom:
  - Top tier (~30% height): "Strategic" — highest-impact, platform-defining decisions.
  - Middle tier (~35% height): "Tactical" — API/tooling/design-level decisions.
  - Bottom tier (~35% height): "Operational" — configuration/infrastructure/build decisions.
- Place a title at the top center: "Real-World ADR Showcase" in a prominent heading. Subtitle: "15 decisions across three architectural altitudes".
- Use a visual metaphor of layers, strata, or altitude bands. The strategic tier should feel elevated (use deeper, bolder colors — navy blue or dark teal). The tactical tier should use medium tones (teal or slate blue). The operational tier should use lighter, more grounded tones (light teal or cool grey).

Top tier — "Strategic Decisions":
- Tier heading: "Strategic" with a small annotation: "Platform-defining, multi-year impact".
- Arrange 5 cards or nodes horizontally, each representing one ADR:
  1. TypeScript icon (abstract code/language icon) → "Rewrite compiler in Go"
  2. Kubernetes icon (abstract container/orchestration icon) → "Deprecate dockershim for CRI"
  3. React icon (abstract UI/component icon) → "Server Components"
  4. Go icon (abstract language/gopher icon) → "Add generics via type parameters"
  5. Rust icon (abstract systems/gear icon) → "Async/await with stackless coroutines"
- Each card should show the project name prominently and the decision as a subtitle.
- Use bold, confident styling — heavier borders, deeper colors — to convey these are the highest-impact decisions.

Middle tier — "Tactical Decisions":
- Tier heading: "Tactical" with annotation: "API design, tooling, framework-level".
- Arrange 5 cards horizontally:
  1. Vue.js (abstract framework icon) → "Composition API"
  2. ESLint (abstract lint/check icon) → "Flat config system"
  3. Vite (abstract build/lightning icon) → "Rolldown unification"
  4. Svelte (abstract compiler icon) → "Runes reactivity"
  5. Next.js (abstract SSR/web icon) → "Turbopack adoption"
- Medium-weight styling — balanced between strategic weight and operational lightness.

Bottom tier — "Operational Decisions":
- Tier heading: "Operational" with annotation: "Config, packaging, infrastructure".
- Arrange 5 cards horizontally:
  1. Node.js (abstract runtime icon) → "Built-in test runner"
  2. Python (abstract snake/language icon) → "pyproject.toml (PEP 621)"
  3. Docker (abstract container icon) → "Container base image selection"
  4. pnpm (abstract package icon) → "Content-addressable store"
  5. Deno (abstract runtime icon) → "npm compatibility layer"
- Lighter, more compact styling — thinner borders, lighter colors — to convey these are at the operational level.

Visual connections and annotations:
- A vertical axis or altitude indicator on the left side, labeled from top to bottom: "High impact / Long horizon" → "Medium impact / Multi-sprint" → "Low impact / Rapid cycle".
- Subtle connecting lines between tiers where decisions influence each other (e.g., TypeScript strategic decision relates to build tooling operational decisions).
- Each card could include a small "accepted" badge or status indicator.
- On the right side, a small annotation block: "Each ADR captures: context, alternatives, decision rationale, consequences, Y-Statement, review cycle, audit trail — all validated by JSON Schema + CI".

Footer sentence (bottom strip):
The same meta-model captures TypeScript's multi-year compiler rewrite and Docker's base-image selection — from boardroom strategy to pull-request operations.
