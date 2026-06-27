---
description: Deliberately select and apply the right debug/operate strategies to diagnose a live system and respond
argument-hint: Optional target (e.g., "the climbing error rate", "this incident", "why is latency up")
---

# Deliberate Debugging

Invoke the `debug-operate-strategy-selector` skill against $ARGUMENTS.

Classify what's being investigated (is there a reliable expectation? evidence quality? live degradation and response reversibility? severity), then select and apply the matching lenses from the catalog. Restore before diagnosing under a live break. Name the evidence quality at every inference. If the stakes are low and a read settles it, say so and keep it light. Close by learning from the incident if one occurred.
