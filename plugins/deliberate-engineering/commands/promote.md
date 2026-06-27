---
description: Drive a pending candidate from candidates/ to the catalog — leak-audit gate, classify, then append-only edit + review (isolated) or recommend a full cycle (structural), stopping before commit
argument-hint: Optional candidate (e.g., a candidates/ filename or slug); omit to process the queue
---

# Promote a candidate to the catalog

Invoke the `deliberate-engineering-promote` skill against $ARGUMENTS.

Take a pending candidate from `candidates/`. First run the leak-audit gate — on any surviving specific, stop and edit nothing. Then classify: isolated (add or modify a single lens) → edit the catalog append-only (never renumber existing lenses), run the skill-reviewer, and remove the candidate; structural (new catalog, reorg, rule change) → do not edit, recommend the proper brainstorm/spec/plan cycle. Always stop before commit, PR, or push — publication is yours.
