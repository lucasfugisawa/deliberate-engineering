---
description: "Conduct an irreversibility cluster (a merge cascade, a deploy chain, a batch of production data mutations, a teardown): a gated, re-derived runbook where the agent conducts and you pull every irreversible trigger"
argument-hint: Optional cluster description (e.g., "the 4-repo deploy chain", "the user-table backfill")
---

# Conduct an irreversibility cluster

Invoke the `deliberate-engineering-conductor` skill against $ARGUMENTS.

When a cluster of irreversible steps must fire in a fixed, gated order (a merge cascade, a deploy chain, a batch of production data mutations, a teardown), run it from the CONDUCTOR contract: re-derive world state before every gate, keep the gate state in a per-item station table rather than in memory, run a between-step verification battery with expected values, and queue each irreversible action for the operator to execute. The agent conducts; you pull every irreversible trigger (Rule 1). A sibling of `orchestrate` (which dispatches units of work across sessions); skip it for a single irreversible step, and for dispatching a program of work across sessions (that is `orchestrate`).
