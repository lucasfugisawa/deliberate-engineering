---
description: "Run a program too large for one session: decompose it into units, dispatch each to a fresh session, verify what returns, and track it all in one place"
argument-hint: 'Optional target (e.g., a program, a milestone, "the migration across sessions", a repo)'
---

# Deliberate Orchestration

Invoke the `deliberate-engineering-orchestrate` skill against $ARGUMENTS.

Run the cross-session loop: plan the program (via the router and selectors), decide per unit whether to do it inline or dispatch it, and if dispatched whether to a fresh human-watched session (the default) or a background subagent (the narrow earned band). Author each handoff, verify every return at source (in a separate context for contested or high-stakes claims), disposition it, and keep the tracker current. The three contracts' required fields live with the skill; this description names the loop and is not a substitute for reading them. Stop at every irreversible or outward-facing action for the operator to trigger. If the work fits one session, say so and route it through the phases directly instead.
