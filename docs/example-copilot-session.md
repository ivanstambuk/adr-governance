# Example Copilot Session — ADR Authoring Walkthrough

> **Purpose:** Realistic step-by-step walkthrough of an ADR authoring session in Microsoft 365 Copilot (or any web chat). Shows the actual interview flow the AI follows, with example prompts and answers you can adapt to your own decision.
>
> This example uses a fictional scenario: **adopting an event-streaming platform for an e-commerce company**.

---

## Step 0: Upload the Bundle

Upload `adr-governance-bundle.md` as a file attachment in Copilot.

## Step 1: Opening Prompt

Paste this after uploading:

```
This file contains an ADR (Architecture Decision Record) authoring and query bundle.
At the end of the file there are instructions under "# Instruction" — please read them.

Then help me create a new ADR by asking me questions about my architectural decision,
following the step-by-step process described in those instructions.

My decision: We need to adopt an event-streaming platform for our e-commerce backend.
Our order processing is currently synchronous and we're hitting scaling limits during
flash sales — last Black Friday we dropped 12% of orders due to downstream timeouts.
```

---

## What Happens Next

The AI reads the bundle instructions, searches for related existing ADRs in the bundle,
and begins a structured interview in **batched sets of 5 numbered questions**. You reply
with matching numbers.

> **Tip:** The AI will reference any related ADRs it finds in the bundle. This is by
> design — it uses existing decisions as context to ask sharper questions.

---

## Set 1 — Decision Metadata

The AI starts with governance metadata to classify the decision correctly.

> **AI asks:**
> 1. What is the exact title for this decision?
> 2. What type of decision is this? (technology / process / vendor / ...)
> 3. What is the decision level? (strategic / tactical / operational)
> 4. What is the priority? (low / medium / high / critical)
> 5. What project or programme does this belong to?

**Your answer:**

```
1. Adopt Event-Streaming Platform for Asynchronous Order Processing
2. technology
3. tactical
4. high
5. Atlas Commerce Platform Modernization
```

---

## Set 2 — Stakeholders, Current State & Constraints

> **AI asks:**
> 1. Who are the author(s)? (name, role, email)
> 2. Who is the decision owner? (name, role, email)
> 3. What is the current state? (how does order processing work today, what breaks)
> 4. What are the main drivers beyond the scaling issue?
> 5. What are the non-negotiable constraints?

**Your answer:**

```
1. Carlos Mendez, Principal Engineer, carlos.mendez@atlascommerce.io
   Aisha Patel, Staff SRE, aisha.patel@atlascommerce.io

2. Carlos Mendez, Principal Engineer, carlos.mendez@atlascommerce.io

3. Orders flow synchronously through a REST chain: API Gateway → Order Service
   → Inventory Service → Payment Service → Fulfillment Service. If any
   downstream service is slow or down, the whole chain blocks. During peak
   events we see cascading timeouts. We also can't replay failed orders —
   they're just lost.

4. Besides scaling: we need event replay for debugging production issues,
   we want to decouple teams so they can deploy independently, and the
   data analytics team wants a real-time event feed for dashboards instead
   of polling our database.

5. Must run on AWS (3-year commitment signed), must handle at least 5,000
   events/second sustained with 50K burst during sales, maximum budget of
   $4K/month for the streaming infrastructure, and we need at-least-once
   delivery guarantees — we cannot silently drop orders.
```

---

## Set 3 — Architecture Landscape & Alternatives

The AI now asks about your runtime environment and the alternatives you've evaluated.
It may push back if you list fewer than 2 alternatives.

> **AI asks:**
> 1. What does your runtime/platform landscape look like?
> 2. What specific technical outcomes must this solution provide?
> 3. Alternative A — what is the strongest option you want to evaluate?
> 4. Alternative B — what is the second strongest option?
> 5. Do you have any more alternatives?

**Your answer:**

```
1. We run on AWS EKS (Kubernetes) with 14 microservices. Services
   communicate via REST today. We use PostgreSQL (RDS) for persistence
   and Redis for caching. Infrastructure is managed with Terraform.
   The team is 30 engineers across 5 squads.

2. Durable event log with at-least-once delivery, replay capability
   for debugging, consumer group support so multiple services can
   independently process the same events, and schema evolution support
   so producers can add fields without breaking consumers.

3. Amazon MSK (Managed Kafka) — fully managed Kafka on AWS. We get
   the Kafka ecosystem (consumer groups, log compaction, exactly-once
   semantics if needed) without managing brokers. Integrates with our
   existing AWS tooling. Cost estimate: ~$2.5K/month for 3-broker
   cluster.

4. Amazon EventBridge + SQS — serverless, no infrastructure to manage.
   EventBridge for routing, SQS for durable queues per consumer.
   Cheaper at low volume (~$500/month) but less control over replay
   and no log compaction. Schema registry is available separately.

5. We briefly looked at self-hosted Kafka and Pulsar, but ruled them
   out — we don't want to manage broker infrastructure with our current
   team. No more alternatives.
```

> **Note:** The AI may challenge you here: *"Are the self-hosted options truly
> uncompetitive, or are they strawmen?"* Be ready to defend your rejection with
> concrete reasoning (team size, ops burden, etc.).

---

## Set 4 — Recommendation, Risks & Tradeoffs

> **AI asks:**
> 1. Which alternative are you leaning toward, and why?
> 2. What are the most important architecturally significant requirements (ASRs)?
>    (at least 2 functional + 2 non-functional)
> 3. What are the biggest risks or downsides of your preferred option?
> 4. Why is the non-chosen alternative less suitable?
> 5. How will you verify the decision has been implemented correctly?

**Your answer:**

```
1. Amazon MSK (Managed Kafka). It gives us a durable, replayable event
   log — the single most important capability we need. The Kafka ecosystem
   is battle-tested at scale, consumer groups let our 5 squads process
   events independently, and the managed service removes the ops burden
   of running brokers ourselves.

2. Functional:
   - F-001: Order events must be durably stored and replayable for at
     least 7 days after publication.
   - F-002: Multiple consumer services must independently process the
     same event stream without coordination.
   Non-functional:
   - NF-001: The platform must sustain 5,000 events/second with bursts
     to 50,000 during flash sales without data loss.
   - NF-002: End-to-end latency from event publish to consumer receipt
     must be under 200ms at p99.

3. Risks: MSK costs more than EventBridge at low volume ($2.5K vs $500/month),
   creates some Kafka operational knowledge requirement even with managed
   service (topic configuration, partition strategy, consumer lag monitoring),
   and if we ever move off AWS, Kafka migration is non-trivial even though
   the protocol is open.

4. EventBridge + SQS is rejected because it doesn't provide a durable,
   replayable event log — SQS messages are consumed and deleted. We
   specifically need replay for debugging production order issues, which
   was a key driver. Also, at our target throughput (5K+/sec), SQS costs
   approach MSK anyway due to per-request pricing.

5. Verification: successful migration of the order processing pipeline
   to event-driven flow, load test proving 50K events/sec burst without
   loss, consumer lag dashboards in Grafana showing all consumers keeping
   up, and a replay drill where we reprocess 24 hours of order events
   from the log to prove the capability works.
```

---

## Set 5 — Consequences, Dependencies & Governance

The AI may ask one final round to capture consequences and governance details.

> **AI asks:**
> 1. What are the positive consequences of this decision?
> 2. What are the negative consequences or risks you're accepting?
> 3. Are there any dependencies on other decisions or systems?
> 4. When should this decision be reviewed? Any triggers for revisiting?
> 5. What confidence level do you have? (low / medium / high)

**Your answer:**

```
1. Positives: order processing survives downstream outages (events queue
   up), teams can deploy independently, analytics gets real-time data feed,
   failed orders can be replayed and recovered, and we eliminate the
   cascading timeout problem from Black Friday.

2. Negatives: higher infrastructure cost ($2.5K/month vs near-zero today),
   team needs Kafka training (consumer groups, partitioning, schema
   evolution), eventual consistency — services won't see updates instantly,
   and debugging distributed event flows is harder than tracing a
   synchronous REST chain.

3. Dependencies: we need to adopt a schema registry (AWS Glue Schema Registry
   or Confluent Schema Registry) before producers can safely evolve event
   schemas. This might warrant its own ADR.

4. Review in 12 months, or sooner if monthly cost exceeds $6K or if we
   start needing cross-region replication (which MSK supports but adds
   complexity).

5. High — we ran a 2-week proof of concept with the order service and
   confirmed throughput, latency, and replay all meet our requirements.
```

---

## Coherence Check

Before generating the YAML, the AI should present a brief coherence summary:
*"Here's what I've collected — let me check for any contradictions..."*

Review this carefully. If anything is wrong, correct it now — it's much easier
to fix at this stage than after the YAML is generated.

---

## YAML Output

The AI will:
1. **Generate a Y-Statement** and ask you to confirm it captures all 7 clauses
2. **Output the complete ADR YAML** — potentially in multiple labeled parts if it's too
   large for a single message

### If the YAML is split across messages

The AI should label parts: *"Part 1 of 3 — metadata and context"*, etc. If it doesn't,
prompt:

```
The YAML was cut off. Please output the remaining sections (the other alternatives,
decision, consequences, confirmation, audit_trail) in a new yaml code block.
```

### What to check in the output

- [ ] **Y-Statement** has all 7 clauses: context → driver → decision → neglected → achieve → accepting → because
- [ ] **At least 2 alternatives** with descriptions, pros, and cons
- [ ] **`decision.rationale`** reflects what you actually said
- [ ] **`consequences.negative`** is honest — not empty or sugar-coated
- [ ] **`confirmation.description`** is actionable (not just "we'll check")
- [ ] **`audit_trail`** has a `created` event with today's date
- [ ] **Status** is `draft` (not `proposed` — you haven't submitted for review yet)
- [ ] **No `null` values** — optional fields should be omitted, not null
- [ ] **Strings with colons are quoted** — e.g., `"Replay: order events"` not `Replay: order events`

---

## Common Follow-ups

**If the Y-Statement is missing clauses:**
```
The Y-Statement is missing the "neglected" clause. Please regenerate it
with all 7 structural clauses present.
```

**If you want a quality review:**
```
Now review this ADR for completeness and quality. Give me a structured
verdict: READY FOR REVIEW, NEEDS REWORK, or MAJOR GAPS.
```

**If you want a stakeholder summary:**
```
Summarize this ADR in 3 paragraphs for a VP who needs to understand
what we decided and why, without reading the full YAML.
```

**If you want to query existing decisions:**
```
Search the bundle for any existing ADRs related to event streaming,
message queues, or asynchronous processing. Summarize what we've
already decided in those areas.
```
