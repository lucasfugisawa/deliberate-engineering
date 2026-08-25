---
description: "Conduct an irreversibility cluster (a merge cascade, a deploy chain, a batch of production data mutations, a teardown): a gated, re-derived runbook where the agent conducts and you pull the irreversible triggers, unless you have deliberately loosened Rule 1 yourself"
argument-hint: Optional cluster description (e.g., "the 4-repo deploy chain", "the user-table backfill")
---

# Conduct an irreversibility cluster

Invoke the `deliberate-engineering-conduct` skill.

$ARGUMENTS

When a cluster of irreversible steps must fire in a fixed, gated order (a merge cascade, a deploy chain, a batch of production data mutations, a teardown), conduct it from the CONDUCTOR contract, which the skill carries in full. This description names the skill and the shape of the job; it is not the contract, and it is not a substitute for reading it. The agent conducts; you pull every irreversible trigger (Rule 1). A sibling of `orchestrate` (which dispatches units of work across sessions); skip it for a single irreversible step, and for dispatching a program of work across sessions (that is `orchestrate`).
