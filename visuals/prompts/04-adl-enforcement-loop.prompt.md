# Visual Prompt — ADL Enforcement Loop: From Decisions to Code Compliance

## Style Primer

The following instructions define the global visual style for a high-resolution 16:9 system-architecture infographic.
 
IMPORTANT META RULES (DO NOT DRAW THESE WORDS):
- Treat this entire block as style guidance only.
- Do NOT render any heading or label that mentions "style", "primer", "system architecture style", or other meta descriptions.
- The ONLY text that should appear inside the image is:
  • The diagram title given in the slide-specific prompt, without quotation marks.
  • The region/zone headings, component labels, connection labels, and short annotations described in the slide-specific prompt.
  • The one-line footer sentence provided in the slide-specific prompt (if any).
- Do NOT create any banner or caption that restates these style rules or calls the figure a "primer" or "style template".
 
GLOBAL VISUAL STYLE FOR SYSTEM ARCHITECTURE & DISTRIBUTED SYSTEMS
 
Create a high-resolution 16:9 architecture diagram suitable for engineering design reviews, platform blueprints, SRE docs, and technical strategy decks.
 
Overall look:
- Clean, flat, vector-based architecture style; think highly-readable system diagrams rather than marketing art.
- Palette: calm enterprise colors (slate, navy, teal, grey) with 1–2 accent colors (orange or lime) for emphasis.
- **WHITE BACKGROUND** (mandatory).
- Typography: geometric sans-serif; strong visual hierarchy for title → major zones → component labels → annotations.
- Keep borders and lines crisp and thin; avoid heavy gradients or 3D effects.
- No real company logos; use generic cloud shapes, compute nodes, databases, queues, and abstract icons.
 
Component grammar:
- Compute units (services, apps, functions) → rounded rectangles or capsules with clear labels, e.g. "Service A", "Auth Service", "Batch Worker".
- Data stores → cylinder icons or container blocks labeled "DB", "Data Lake", "Cache", "KV Store", etc.
- Integration points → API gateways, message brokers, event buses, queues shown as central connective components.
- Clients → browser, mobile, system-to-system icons grouped into a "Client / Consumer" zone.
- External dependencies → shaded boxes with dashed borders, labeled "3rd-party API", "External Partner", "Legacy System".
 
Connection / flow grammar:
- Use arrows for directional flows:
  - Solid arrows = synchronous request/response.
  - Dashed arrows = asynchronous or event-driven flows.
  - Dotted arrows = control, configuration, or monitoring channels.
- For high-throughput paths, use thicker arrows or multiple parallel arrow-lines.
- Label important flows with short text: "REST/JSON", "gRPC", "Events", "CDC", "Batch".
- Explicitly show boundaries:
  - "Trust boundary", "Network boundary", "Account/tenant boundary", or "Region boundary" using dashed rectangles.
 
Structural layout rules:
- Partition canvas into 3–4 horizontal or vertical zones with content-based headings, for example:
  - "Client and edge"
  - "Application and services"
  - "Data and infrastructure"
  - "Observability and control plane"
- Alternatively, use left→right to show ingress → processing → storage → analytics → external.
- Each zone should focus on one layer of responsibility with 3–10 components.
- Use consistent alignment and spacing to create a grid-like, readable layout.
 
Architecture-specific metaphors:
- Layers and tiers → horizontal bands (Edge, API, Domain Services, Data, Infra).
- Multi-region / HA → duplicated blocks with region labels (e.g. "Region A", "Region B") and arrows for replication/failover.
- Scalability → small stack of identical service blocks or scale-out arrows (e.g. "N instances").
- Resilience / redundancy → paired components with an "active/active" or "active/passive" annotation.
- Isolation / multi-tenancy → partitioned blocks per tenant or labeled tenant boundaries.
- Evolution / migration → legacy vs target sections side-by-side, with arrows showing migration paths.
- Security / compliance → shields and locks near gateways, boundary annotations, "Zero Trust" bubbles.
 
Non-functional focus:
- Surface latency-critical paths with slightly bolder styling or color.
- Highlight data consistency / integrity flows where relevant (e.g. "strong consistency", "eventual consistency").
- Show observability components explicitly: "Metrics", "Logs", "Tracing", "Alerting", "Dashboards".
- Show governance / control plane where relevant: "Config service", "Feature flags", "Policy engine".
 
Context focus (general system architecture):
- Suitable for microservices, monolith + strangler, event-driven architectures, data platforms, hybrid cloud, edge + core, platform engineering setups, CI/CD pipelines, or control planes.
- Make relationships between components explicit: which clients talk to which gateways, which services depend on which data stores, which components publish/subscribe to which topics.
- Always make separation of concerns visible: edge vs core, stateless vs stateful, control plane vs data plane.
 
Reading orientation & storytelling:
- For request/response architectures, favor left→right pipelines: client → edge → services → data → external.
- For platform overviews, favor layered top→bottom stacks: consumer → platform capabilities → underlying infra.
- For ecosystems, use a central "platform hub" with spokes outwards to consumers and external systems.
- The diagram should convey the main architectural story in 3–5 seconds of viewing.
- Group related elements with subtle background shapes or low-contrast bounding boxes instead of structural labels.
 
IMPORTANT LABELING RULES:
- Do not use generic structural labels such as "Panel 1", "Panel 2", "Panel A", "Upper panel", "Lower panel", "Top mini-panel", "Bottom mini-panel", or similar phrases anywhere in the image.
- Do not label zones or regions with bare ordinals only (e.g. just "Layer 1", "Zone A") unless they are clearly tied to a descriptive phrase like "Layer 1 – client and edge".
- Every zone, region, or major grouping that has a heading must use a descriptive, content-based title that reflects its architectural role, e.g. "Client and edge", "Application services", "Data layer", "Observability and control plane".
- When multiple regions are related, distinguish them by concept, not by number, e.g. "Online path" vs "Offline/batch path", "Control plane" vs "Data plane", "Primary region" vs "Failover region".
- Apply these rules consistently to all titles, captions, legends, and labels inside the figure so that labels describe the architecture rather than its layout structure.
 
Bottom strip:
- Reserve a narrow footer area for exactly one 1-sentence key takeaway that summarizes the architecture, without quotation marks.
- The footer must contain only that single sentence, with no extra prefix such as "The diagram shows…", "This figure illustrates…", or "Summary:", unless the slide-specific prompt explicitly includes those words.
- When a slide-specific prompt provides a footer sentence, copy that sentence verbatim into the bottom strip without modification.

---

## Slide-Specific Instantiation

NOW INSTANTIATE THIS STYLE FOR:
"ADL Enforcement — Closing the Loop Between Decisions and Code"

Goal:
- Draw a single system-architecture infographic that shows how the Architecture Decision Log (ADL) serves as a machine-readable source of truth that AI agents and CI pipelines enforce against application code. This is the "closed-loop" story: decisions don't just get documented — they get enforced.
- The diagram must show three interacting systems (ADL repository, code repository, CI pipeline) and the circular flow between them.

Overall layout:
- Use a circular / closed-loop arrangement across three zones, reading clockwise:
  - Top zone: "Architecture Decision Log" — the ADL repository where decisions live.
  - Bottom-left zone: "Development" — the code repository where implementation happens.
  - Bottom-right zone: "CI Enforcement" — the pipeline that validates code against decisions.
- A prominent circular flow connects all three zones clockwise, with a feedback arrow completing the loop.
- Place a title at the top center: "ADL Enforcement Loop" in a prominent heading. Subtitle: "Closing the gap between deciding and doing".

Top zone — "Architecture Decision Log":
- Region heading: "Architecture Decision Log".
- Show a Git repository icon containing:
  - A stack of 3–4 ADR document icons labeled "ADR-0001", "ADR-0002", "ADR-0003", etc.
  - A schema validation shield icon with label: "JSON Schema validated"
  - A bundle/package icon labeled "ADL Bundle" with annotation: "Machine-readable, single-file export"
- Two outgoing arrows from this zone:
  1. Arrow going down-left to the Development zone, labeled "AI agent queries ADL during code generation"
  2. Arrow going down-right to the CI Enforcement zone, labeled "CI extracts active decisions"
- Use navy/teal coloring for this zone — it's the authoritative source.

Bottom-left zone — "Development":
- Region heading: "Code repository".
- Show components representing the development workflow:
  1. A developer icon (abstract person silhouette) at a workstation.
  2. An AI coding agent icon (brain/sparkle) next to the developer, with a bidirectional arrow between them labeled "AI-assisted development".
  3. A code file / repository icon representing the application codebase.
  4. A connection from the AI agent icon upward to the ADL zone (the incoming arrow from above), with a small callout: "Agent searches bundled ADL for relevant decisions before generating code".
- Show the developer + AI agent producing a code change, with an arrow going right toward the CI zone, labeled "PR opened with code changes".
- Use a warm accent (amber or orange) for the developer elements and teal for the AI elements.

Bottom-right zone — "CI Enforcement":
- Region heading: "CI compliance check".
- Show a pipeline with 3 sequential steps:
  1. A diff/comparison icon labeled "Extract code diff" — annotation: "What changed in this PR?"
  2. A crosscheck icon (two overlapping documents) labeled "Match against active ADRs" — annotation: "Which decisions apply to this change?"
  3. A verdict icon that branches into two outcomes:
     - Green checkmark path: "Compliant — PR passes" — annotation: "Code aligns with architectural decisions"
     - Red warning path: "Drift detected — PR flagged" — annotation: "Code contradicts ADR-0001: use DPoP, not mTLS"
- The green path leads to a merge icon.
- The red path has a feedback arrow going left back to the Development zone, labeled "Developer notified — fix required".
- Use green for the pass path and red/orange for the drift-detected path.

Closing the loop:
- From the Development zone, show a dashed arrow going back up to the ADL zone, labeled "New ADR proposed if decision needs updating". This is the feedback path: if enforcement reveals that a decision is outdated, the team creates a new ADR that supersedes the old one.
- This arrow completes the circular flow: ADL → Development → CI → (feedback) → ADL.

Scenario callout (compact, inside the diagram):
- Place a small, visually distinct callout box near the CI zone showing a concrete example scenario:
  - "Example: ADR-0001 says 'Use DPoP for sender-constrained tokens'"
  - "PR introduces mTLS code"
  - "CI flags: architectural drift detected"
- Keep this compact — 3 short lines in a rounded box with a subtle background.

Comparison strip (optional, below the main diagram, above the footer):
- A narrow horizontal strip with two side-by-side mini-comparisons:
  - Left mini-box (muted/grey): "Without enforcement" — "Decisions documented but ignored; code drifts silently"
  - Right mini-box (green/teal): "With ADL enforcement" — "Decisions enforced in CI; drift caught before merge"
- Keep this subordinate to the main diagram — it's supporting context.

Footer sentence (bottom strip):
Decisions are not just documented — they are enforced against code in CI, closing the gap between deciding and doing.
