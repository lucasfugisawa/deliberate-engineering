---
description: Deliberately select and apply the right review lenses for the current change
argument-hint: Optional scope (e.g., a path, a diff range, or "staged")
---

# Deliberate Review

Invoke the `review-strategy-selector` skill against the current change $ARGUMENTS.

Classify the change by risk, reversibility, requirement clarity, and size, then select and apply the matching review lenses from the catalog. If the change is trivial and safe, say so and keep ceremony minimal. Close with a fresh-eyes pass and log any lens you deliberately skipped and why.
