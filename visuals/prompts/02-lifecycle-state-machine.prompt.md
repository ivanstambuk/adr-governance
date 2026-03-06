# Visual Prompt — ADR Lifecycle State Machine

## Style Primer

The following instructions define the global visual style for a high-resolution 16:9 infographic that visualizes an algorithm or mathematical workflow.
 
IMPORTANT META RULES (DO NOT DRAW THESE WORDS):
- Treat this entire block as style guidance only.
- Do NOT render any heading or label that mentions "style", "primer", "algorithmic workflows style", or any other meta description.
- The ONLY text that should appear inside the image is:
  • The diagram title given in the slide-specific prompt, without quotation marks.
  • The region/box headings, variable names, and short annotations described in the slide-specific prompt.
  • The one-line footer sentence provided in the slide-specific prompt (if any).
- Do NOT create a banner or caption at the top that restates these style rules.
 
GLOBAL VISUAL STYLE FOR ALGORITHMS & MATHEMATICAL WORKFLOWS
 
Create a high-resolution 16:9 technical infographic that visualizes an algorithm or mathematical workflow. Target audience: researchers, quantitative engineers, algorithm designers, and mathematically literate stakeholders.
 
Overall look:
- Clean, flat, vector-based illustration with a "research notebook meets architecture diagram" aesthetic.
- Palette: mostly neutral (white, light grey, slate) with 1–2 accent colors (deep blue, teal, or amber) to highlight key steps or structures.
- **WHITE BACKGROUND** (mandatory).
- Typography: high-legibility sans-serif for labels plus math-friendly styling for symbols (e.g. LaTeX-like notation).
- Prefer sharp lines, crisp geometry, and consistent alignment over decorative elements.
- No logos; use neutral, abstract labels and symbols.
 
Visual grammar / metaphors:
- Algorithm steps → numbered boxes or nodes linked by directed arrows (flowchart-like but minimal).
- Mathematical operations → operator nodes (⊕, ⊗, ∑, ∏, ∫, f(·), g(·), ∇L, argmin) placed in circles or rounded boxes.
- Data/variables → rectangles or capsules labeled with symbols (x, y, z, θ, w, μ, σ², p(x), q(x), A, B, v₁,…,vₙ).
- States / iterations → layers or repeated blocks indexed by t, k, n (e.g. xₜ, θₖ).
- Branching / conditionals → split arrows or decision diamonds with concise conditions (e.g. "if ||Δθ|| < ε").
- Parallelism / vectorization → stacked or batched elements, or wide blocks labeled with "vectorized" or "batch".
- Probabilities / distributions → soft blobs, density curves, or nodes labeled p(·), q(·), π(·), with arrows showing sampling or transformation.
- Optimization loops → cyclic arrows around a core update rule (e.g. θ ← θ − η∇L(θ)).
- Convergence / stopping criteria → target region, tolerance band, or "stop" marker with ε, δ, or max_iter.
 
Structural rules:
- Decompose the canvas into 2–4 logical regions, for example:
  • Inputs & assumptions
  • Core iterative algorithm / computation graph
  • Outputs & metrics
  • Constraints / guarantees / failure modes
- Each region should show 3–10 algorithmic elements (variables, operators, transitions).
- Use clear directionality:
  • Left→right for forward computation or dataflow.
  • Top→bottom for derivations, refinement, or multi-stage processing.
  • Circular motifs for iterative loops and fixed-point procedures.
- Distinguish:
  • Dataflow arrows (solid, thicker).
  • Control/condition arrows (dashed).
  • Approximate or stochastic transitions (dotted).
- Maintain consistent visual encoding: same shape and color = same type of object (e.g. variables vs operators vs loss functions).
 
Context focus (general-purpose algorithms & math):
- Suitable for deterministic algorithms, stochastic methods, numerical schemes, ML pipelines, optimization routines, signal-processing chains, cryptographic primitives, and statistical procedures.
- Explicitly represent:
  • Inputs (raw data, parameters, hyperparameters, priors).
  • Transformations (linear maps, nonlinearities, aggregations, normalization, projections).
  • Objective(s) (loss L(θ), error metrics, cost functions, constraints).
  • Outputs (estimates, decisions, classifications, posterior distributions, optimized parameters).
- When relevant, show:
  • Time or iteration index (t = 0,1,2,…).
  • Complexity-driving dimensions (n, d, m, T).
  • Error or convergence indicators (||Δθ||, gap, residuals).
  • Randomness sources (ξ, ε, noise terms).
 
Reading orientation & narrative:
- The diagram should visually answer:
  • "What are the inputs?"
  • "What transformations are applied, in what order?"
  • "Where do decisions or randomness enter?"
  • "What is the objective and how is it optimized?"
  • "What is the final output or invariant?"
- Use labels and short annotations instead of long prose (e.g. "Projection onto feasible set", "Gradient step", "Normalization", "Sampling from p(z)").
- If the algorithm has multiple modes (e.g. training vs inference, encryption vs decryption), represent them as clearly separated but related paths.
 
Mathematical notation:
- Use standard symbols and LaTeX-like formatting where appropriate: f(x), g_θ(x), ∇L(θ), Eₓ[·], Var[X], P(A), KL(p‖q), σ(Wx + b).
- Place key equations near the region that visually implements them, but do not overcrowd; prefer one core equation per region with visual correspondence to nodes/arrows.
 
IMPORTANT LABELING RULES:
- Do not use generic structural labels such as "Panel 1", "Panel 2", "Panel A", "Upper panel", "Lower panel", "Top mini-panel", "Bottom mini-panel", or any similar wording.
- Every region, sub-panel, or box that has a title must use a descriptive, content-based heading reflecting the mathematics or algorithmic role it depicts, e.g. "Input variables and assumptions", "Iterative update rule", "Loss function and gradients", "Convergence check", "Sampling step", "Output metrics".
- When multiple regions are related, distinguish them via meaning, not numbering, e.g. "Forward pass" vs "Backward pass", "Training loop" vs "Inference pipeline", "Time-domain view" vs "Frequency-domain view".
- Apply this rule consistently to all textual labels, legends, and captions within the figure so that no label is just a structural placeholder; every label should describe what is being shown.
 
Bottom strip:
- Add a narrow footer with exactly one concise, mathematically-informed summary sentence, without quotation marks.
- The footer must contain only that single sentence, with no automatically added preamble such as "The diagram shows the full data-to-solution pipeline…", "This figure illustrates…", or "Summary:", unless the slide-specific prompt explicitly includes those words.
- When a slide-specific prompt provides a footer sentence, copy it verbatim into the bottom strip without modification.

---

## Slide-Specific Instantiation

NOW INSTANTIATE THIS STYLE FOR:
"ADR Lifecycle — Governed State Machine"

Goal:
- Draw a single, visually polished state-machine diagram that shows the complete lifecycle of an Architecture Decision Record (ADR). This replaces a basic Mermaid stateDiagram — it must be significantly more readable, visually refined, and information-dense than what a text-based renderer can produce.
- The diagram must communicate two things simultaneously: (1) the states an ADR can be in, and (2) the Git operations that trigger each transition.

Overall layout:
- Partition the canvas into two regions:
  - Main region (~75% width, left/center): "ADR Lifecycle" — the full state machine.
  - Side panel (~25% width, right): "Git Operations" — a compact reference mapping each transition to the Git/PR action that triggers it.
- Place a title at the top center: "ADR Lifecycle" in a prominent heading. Subtitle: "Every status transition is a Git operation".

Main region — "ADR Lifecycle" (state machine):
- Draw 7 states as rounded rectangles or pill-shaped nodes, each with a distinct color:
  1. "draft" — color: light grey — the initial state. This is where the ADR is being authored locally. Place it at the far left.
  2. "proposed" — color: blue/teal — the ADR has been submitted as a pull request. Place it center-left.
  3. "accepted" — color: green — the ADR was approved and the PR merged. Place it center-right, upper track.
  4. "rejected" — color: red — the ADR was rejected, but the PR is still merged (to preserve the decision trail). Place it center-right, middle track.
  5. "deferred" — color: amber/yellow — the ADR was postponed; the PR is closed (not merged). Place it center-right, lower track.
  6. "superseded" — color: purple — an accepted ADR has been replaced by a newer ADR. Place it far right, upper area.
  7. "deprecated" — color: muted grey/purple — an accepted ADR is no longer recommended but not formally replaced. Place it far right, lower area.

- Draw an entry point (small filled circle, [*]) at the far left with an arrow into "draft".

- Draw transitions as labeled arrows between states:
  - [*] → draft (unlabeled or "Author begins ADR")
  - draft → proposed (label: "Open PR")
  - proposed → proposed (self-loop, label: "Rework — changes requested")
  - proposed → accepted (label: "Approved → PR merged")
  - proposed → rejected (label: "Rejected → PR merged")
  - proposed → deferred (label: "Postponed → PR closed")
  - deferred → proposed (label: "Reopened — new PR")
  - accepted → superseded (label: "Replaced by new ADR")
  - accepted → deprecated (label: "No longer recommended")

- Terminal states: "rejected", "deferred", "superseded", and "deprecated" should have a subtle visual cue that they are terminal (e.g., a small dot or end marker on their right edge, or a slightly thicker border).

- The self-loop on "proposed" should be visually prominent — it represents the iterative review cycle (the "Socratic dialogue" phase) and is the most common transition in practice. Use a curved arrow looping back into the same node.

- Spatial arrangement should flow generally left→right (lifecycle progression) with the three outcomes from "proposed" (accepted/rejected/deferred) fanning out vertically, and the two outcomes from "accepted" (superseded/deprecated) continuing rightward.

Side panel — "Git Operations Reference":
- A compact, table-like reference with 2 columns:
  - "Transition" — short label matching the arrow labels in the state machine.
  - "Git operation" — what actually happens in the repository.
- Rows:
  1. "Author begins" → "Local branch, YAML editing"
  2. "Open PR" → "Push branch, open pull request"
  3. "Rework" → "Push new commits to same PR branch"
  4. "Approved → merged" → "Reviewers approve, PR merged to main"
  5. "Rejected → merged" → "Decision: reject. PR merged to preserve trail"
  6. "Postponed → closed" → "PR closed without merge"
  7. "Reopened" → "New PR from existing branch or new branch"
  8. "Replaced by new ADR" → "New ADR sets supersedes; old ADR updated"
  9. "No longer recommended" → "Commit updates status to deprecated"
- Style this as a clean, minimal table with alternating light row backgrounds. Use the same state colors for the transition labels to visually connect them to the state machine.

Visual design notes:
- The state nodes should be large enough to be easily readable — this is the centerpiece of the diagram.
- Arrow labels should sit close to their arrows, not floating in ambiguous whitespace.
- The "proposed → proposed" self-loop should stand out — perhaps with a slightly thicker line or a distinct visual treatment — since iterative rework is the core of the review process.
- Use the same color coding consistently between the state machine and the side panel.
- The overall impression should be "governance process as engineering diagram" — precise, clean, confident.

Footer sentence (bottom strip):
Every ADR transition is a Git operation — status changes happen through pull requests, not manual coordination.
