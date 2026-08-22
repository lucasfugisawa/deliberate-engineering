---
description: Deliberately select and apply the right debug/operate strategies to diagnose a live system, respond to an incident, keep the signals healthy in peacetime, or learn from a failure after the fact
argument-hint: Optional target (e.g., "the climbing error rate", "this incident", "why is latency up", "our alerts keep crying wolf", "retro on yesterday's outage")
---

# Deliberate Debugging

Invoke the `debug-operate-strategy-selector` skill against $ARGUMENTS.

Classify what's being investigated (the entry gate: is there a reliable expectation? then evidence quality, live degradation and response reversibility, severity), then select and apply the matching lenses from the catalog. Restore before diagnosing under a live break, and hand every irreversible trigger to the human (Rule 1). Name the evidence quality at every inference. If the stakes are low and a read settles it, say so and keep it light. Close by learning from the incident if one occurred. Peacetime work belongs here too: alert and error-stream hygiene, thresholds, and flow ownership are the catalog's own band, not a lesser version of incident response.
