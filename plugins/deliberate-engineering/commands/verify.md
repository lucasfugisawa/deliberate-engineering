---
description: Deliberately select and apply the right verification strategies to establish something is actually true
argument-hint: Optional target (e.g., a claim, a number, "this PR", "the backfill in prod")
---

# Deliberate Verification

Invoke the `verification-strategy-selector` skill.

$ARGUMENTS

Classify what's being verified (evidence type, irreversibility of being wrong, environment reach, your stake), then select and apply the matching strategies from the catalog. If the task is really "read this and tell me if it's right", that is review, not verification: say so and route it to `review-strategy-selector` instead. State each expectation before observing the actual result, and tie every finding to concrete evidence (the query, the run, the captured payload). If a read settles it and the stakes are low, say so and keep it light. Close with an independent second pass and log anything you deliberately skipped and why.
