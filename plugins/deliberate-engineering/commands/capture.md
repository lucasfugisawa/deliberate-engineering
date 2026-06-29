---
description: Capture what you did this session into durable overrides — distill deviations and recurring patterns, then append approved ones to your override file
argument-hint: Optional focus (e.g., "the review steps", "this debugging session", a path)
---

# Capture practice into overrides

Invoke the `deliberate-engineering-capture` skill against $ARGUMENTS.

Observe this session for deviations (a deliberate-engineering lens or rule was applicable and you corrected, skipped, or contradicted it) and recurring patterns the catalog lacks. Map each to an addressable override target and operation, show the exact block that would be appended, and — only on your approval — append it to `~/.claude/deliberate-engineering/overrides.md`. Recommend, never force. If nothing is worth an override, say so and write nothing.
