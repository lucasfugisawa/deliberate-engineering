---
name: planning-strategy-selector
description: "Use before building, when deciding what work to do and how to approach it — scoping a feature, shaping a spec or ticket, planning a migration or refactor, or choosing how much process a task calls for. Classifies the work by requirement clarity, risk, reversibility, and reach, then selects the right planning lenses: scope to the real requirement, ground the plan in the actual codebase, calibrate ceremony to risk, decompose and sequence safely, and capture the plan well — judgment applied to planning, not a planning engine."
---

# Planning Strategy Selector

The deliberate layer of planning. Where review judges a finished artifact and verification confronts reality, this skill operates *before code exists* — it decides **what work is worth doing, and how much process it calls for**, so the plan builds the right thing instead of everything plausible.

The reference for every strategy cited below is `catalog.md` in this directory (six groups of strategies + composition patterns). Read **only** the sections you select — progressive disclosure, not the whole file.

## This is judgment, not a planning engine

This skill does not teach how to brainstorm or how to write a plan — a workflow engine such as `superpowers` owns that discipline, and this layer delegates to it. What this skill adds is the **judgment exercised while planning**: scope, ceremony, decomposition, sequencing, and artifact shape. If a planning/ brainstorming engine is present, run *its* process and apply these lenses to the decisions inside it; don't reimplement the process.

## When to use

- Scoping a feature, change, or fix — deciding what is in and out.
- Shaping a spec, ticket, or design doc before implementation.
- Planning a migration, refactor, or parity effort.
- Deciding how much process a task calls for, before starting it.

## When NOT to over-plan

Planning has a cost, and over-planning the trivial is the same misplaced ceremony as under-planning the dangerous, inverted. For a **trivial-and-safe** change (clarity high, risk low, easily reversible, narrow reach), skip the spec, do the work, and **say so** — state that you judged it low-ceremony. A stated decision to plan lightly is calibration; silence is not.

## Step 1 — Classify the work on four axes

These set how much of the catalog you apply — and in which direction.

1. **Requirement clarity** — Is the intent unambiguous, or are you inferring what "correct" and "done" mean? Ambiguity is the first thing a plan must resolve.
2. **Risk** — Does the work touch money, data, security, or production behavior? What is the cost of building the wrong thing or building it wrong?
3. **Reversibility** — How hard is it to undo the *direction* once committed — a chosen abstraction, a data-model decision, a migration?
4. **Reach** — How many call sites, services, consumers, or teams does the work touch? (Not the diff size — the blast radius of the decision.)

**The ruler is clarity, risk, reversibility, and reach — not how big the change looks.** These are deliberately the *same* risk / reversibility / clarity / reach axes the review and verification selectors use, applied here *before* code rather than after — one mental model, three lenses across the lifecycle. Planning leads with **clarity** because resolving ambiguity is planning's first job.

## Step 2 — Map to a planning depth

- **Trivial-and-safe** → minimal: calibrate (10), confirm there's no hidden reach, do it, and state the light-ceremony decision. See "When NOT to over-plan."
- **Standard** → scope to the real requirement (Part A), ground against the real codebase (5), and capture the plan with recommendations (14) — a lightweight pass over the axes that scored non-trivial.
- **Ambiguous / risky / irreversible / wide reach** → full depth: clear the fog and triage the open questions first (17, 18) and gate readiness before committing (19), resolve scope hard (Part A incl. the correctness counter-rule 3), spike any feasibility unknown (8), inventory and blast-radius the reach (6, 7), gate before code (9), decompose and sequence (11, 12), keep a multi-deploy schema/data change backward-compatible (13), and capture a self-contained dual-audience artifact (15, 16).

## Step 3 — Select lenses from the catalog

Open only the parts matching your non-trivial axes:

- **Always, standing** → 10 calibrate-ceremony-to-risk (it decides how much of the rest applies) and 14 recommend-don't-enumerate (every fork carries a pick); plus the Part A scope lenses: 1 simplest-mechanism, 2 strip-speculative, **3 the correctness counter-rule** (so trimming doesn't become under-scoping).
- **Touches existing code / rests on assumptions** → 5 verify-repo-reality.
- **Low clarity / unproven approach / feasibility unknown** → 8 spike-to-retire-the-riskiest-unknown.
- **Unknown-size / migration / parity** → 6 front-loaded-inventory.
- **Changes meaning of shared data / a source-of-truth** → 7 blast-radius-modeling.
- **Crosses team / infra boundaries** → 4 push-to-proper-owner.
- **Ambiguous or risky** → 9 plan-before-code gate.
- **Large or multi-concern** → 11 decompose-for-reviewability.
- **Multi-step / spans services / can't ship atomically** → 12 sequence-to-avoid-intermediate-states.
- **Schema or data change to a live system / deploys separately from code** → 13 migration-backward-compatibility.
- **Will be handed off or outlive the conversation** → 15 self-contained-dual-audience, 16 document-altitude.

**Worked example — plan a source-of-truth field migration:** Ambiguous-ish, high risk, hard to reverse, wide reach. Selected: **10** (full ceremony — it's risky and irreversible), **2 + 3** (strip anything speculative, but keep every step the migration needs to be correct), **7** (enumerate every downstream reader before calling it small), **6** (a classified inventory of all affected sites as the first deliverable), **9** (approve the approach before any code), **12** (sequence so no intermediate state is half-migrated and broken), **13** (expand→adopt→contract so the old code still reads and writes valid rows at every deploy step), **15** (a self-contained spec for the human and the executing agent), each fork carrying **14** a recommendation. Skipped frontend/altitude-heavy lenses — logged as not applicable.

**Operator overrides.** Before applying the selected lenses, consult `deliberate-engineering-overrides`: if any selected lens has an operator override (disable / modify / add), honor it and declare the deviation in the Output.

## Step 4 — Compose the plan

Apply the catalog's Appendix patterns:

- **Calibrate first** — set ceremony (10) before anything else; it decides how much of the catalog you even open.
- **Scope down, then ground up** — decline the speculative (Part A) *before* investigating what remains against the real codebase, data, and feasibility (Part B); spike (8) any feasibility unknown before planning the build on it.
- **Inventory before estimate** — for unknown-size work, the classified inventory (6) precedes any plan or timeline commitment.
- **Slice along the sequence** — decompose (11), then order the slices (12) so every intermediate state is safe; for a schema/data change, keep each deploy step backward-compatible with the running code (13).
- **Decisions carry recommendations** — every fork pairs options with a pick (14); a plan of open menus has deferred the planning, not done it.

## Step 5 — Coexistence and precedence

When a planning or brainstorming engine is present (e.g. `superpowers`), **run its process** and apply these lenses to the decisions within it — this skill decides *what to build and how much process*, the engine handles *how to plan*. It never requires removing any other tool. When the work then moves to implementation, the deliberate flow continues into review and verification.

## Output

Report, briefly: the classification (4 axes), the planning depth, the lenses selected (by number) and why, what you scoped **out** and why (the most valuable part of a plan), anything deliberately skipped, and the plan itself — every decision point carrying a recommendation with its rationale.
