---
name: planning-strategy-selector
description: "Use before building, when deciding what work to do and how to approach it: scoping a feature, shaping a spec or ticket, planning a migration or refactor, or choosing how much process a task calls for. Classifies the work by requirement clarity, risk, reversibility, and reach, then selects the right planning lenses: scope to the real requirement, ground the plan in the actual codebase, calibrate ceremony to risk, decompose and sequence safely, capture the plan well, and clear ambiguity before committing when the requirement itself is still foggy. Judgment applied to planning, not a planning engine. On a multi-phase or multi-session work unit it writes a short live note through `deliberate-engineering-state`, which lands in the repository under `.deliberate/state/` (and may add that path to `.gitignore`) or under `~/.claude/` when it cannot."
---

# Planning Strategy Selector

The deliberate layer of planning. Where review judges a finished artifact and verification confronts reality, this skill operates *before code exists*: it decides **what work is worth doing, and how much process it calls for**, so the plan builds the right thing instead of everything plausible.

The reference for every strategy cited below is `catalog.md` in this directory (six groups of strategies + composition patterns). Read **only** the sections you select: progressive disclosure, not the whole file.

## This is judgment, not a planning engine

This skill does not teach how to brainstorm or how to write a plan: a workflow engine such as `superpowers` owns that discipline, and this layer delegates to it. What this skill adds is the **judgment exercised while planning**: scope, ceremony, decomposition, sequencing, and artifact shape. If a planning/ brainstorming engine is present, run *its* process and apply these lenses to the decisions inside it; don't reimplement the process.

## When to use

- Scoping a feature, change, or fix: deciding what is in and out.
- Shaping a spec, ticket, or design doc before implementation.
- Planning a migration, refactor, or parity effort.
- Deciding how much process a task calls for, before starting it.

## When NOT to over-plan

Planning has a cost, and over-planning the trivial is the same misplaced ceremony as under-planning the dangerous, inverted. For a **trivial-and-safe** change (clarity high, risk low, easily reversible, narrow reach), skip the spec, do the work, and **say so**: state that you judged it low-ceremony. A stated decision to plan lightly is calibration; silence is not.

## Step 1: Classify the work on four axes

These set how much of the catalog you apply, and in which direction.

1. **Requirement clarity**: Is the intent unambiguous, or are you inferring what "correct" and "done" mean? Ambiguity is the first thing a plan must resolve.
2. **Risk**: Does the work touch money, data, security, or production behavior? What is the cost of building the wrong thing or building it wrong?
3. **Reversibility**: How hard is it to undo the *direction* once committed: a chosen abstraction, a data-model decision, a migration?
4. **Reach**: How many call sites, services, consumers, or teams does the work touch? (Not the diff size, the blast radius of the decision.)

**These four set the depth here, not how big the change looks.** They are the same four the router routes on and the review selector classifies on, applied *before* code rather than after; verification and debug-operate classify on their own, because each starts from a different epistemic footing (see `deliberate-engineering-router`, Step 1). The ruler underneath all of them is the cost of being wrong, and that, not the axis names, is what every phase shares. Planning leads with **clarity** because resolving ambiguity is planning's first job.

## Step 2: Map to a ceremony band

- **Trivial-and-safe** → minimal: calibrate (10), confirm there's no hidden reach, do it, and state the light-ceremony decision. See "When NOT to over-plan."
- **Standard** → scope to the real requirement (Part A), ground against the real codebase (5), and capture the plan with recommendations (14), a lightweight pass over the axes that scored non-trivial.
- **Ambiguous / risky / irreversible / wide reach** → full depth: clear the fog and triage the open questions first (17, 18) and gate readiness before committing (19), resolve scope hard (Part A incl. lens 3, the correctness counter-rule), spike any feasibility unknown (8), front-load a classified inventory when the true size is unknown (6) and, where the change alters the meaning of shared data, model its blast radius (7), gate before code (9), decompose and sequence (11, 12), keep a multi-deploy schema/data change backward-compatible (13), capture a self-contained dual-audience artifact (15, 16), and record a decision costly to recover (20).

## Step 3: Select lenses from the catalog

Open only the parts matching your non-trivial axes:

- **Always, standing** → 10 calibrate-ceremony-to-risk (it decides how much of the rest applies) and 14 recommend-don't-enumerate (every fork carries a pick); plus the Part A scope lenses: 1 simplest-mechanism, 2 strip-speculative, **3 the correctness counter-rule** (so trimming doesn't become under-scoping).
- **The requirement itself is still foggy** → the disambiguation lenses: 17 clear-the-fog-with-evidence-before-asking and 18 decide-early-what-is-costly-to-reverse, closing with 19 the readiness-and-viability gate before you commit to building.
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
- **A hard-to-reverse, surprising choice with real alternatives** → 20 record-the-decision (an ADR / decision-doc entry with its rationale).

**Worked example (plan a source-of-truth field migration):** Ambiguous-ish, high risk, hard to reverse, wide reach. Selected: **10** (full ceremony: it's risky and irreversible), **2 + 3** (strip anything speculative, but keep every step the migration needs to be correct), **7** (enumerate every downstream reader before calling it small), **6** (a classified inventory of all affected sites as the first deliverable), **9** (approve the approach before any code), **12** (sequence so no intermediate state is half-migrated and broken), **13** (expand→adopt→contract so the old code still reads and writes valid rows at every deploy step), **15** (a self-contained spec for the human and the executing agent), each fork carrying **14** a recommendation. Skipped frontend/altitude-heavy lenses, logged as not applicable.

**Entering here directly.** These lenses are the same whether you arrived through `/deliberate-engineering:start` or called this phase yourself, but four things the router would have carried do not come with a direct call, so carry them here. The nine standing rules in `deliberate-engineering-rules` hold regardless, including the human gate on anything irreversible or outward-facing. Write your place at each checkpoint through `deliberate-engineering-state` (Rule 6), so a compaction or a new session resumes from what happened rather than from recall; where the operator has asked you not to touch the tree, say so and use that skill's home outside the repository rather than dropping the checkpoint, which is the one thing Rule 6 exists to prevent. Re-classify out loud if the work turns out heavier or lighter than it looked, and say what moved. And when the next thing you produce is a communication rather than code, consult `communication-collaboration-selector` before writing it.

**Operator overrides.** Before applying the selected lenses, consult `deliberate-engineering-overrides`: honor any override on a lens you selected (disable / modify), and ask it for any operator-authored `add: <catalog>` lens entry for this catalog, which carries no shipped number and so is invisible to a lookup keyed on your selection. An `add: <catalog> pattern` entry is not one of these; it is honored where the patterns are composed. Declare every deviation in the Output.

## Step 4: Compose the plan

The composition patterns are numbered in the catalog's Appendix: **1** calibrate first, **2** scope down then ground up, **3** spike before you plan the unknown, **4** inventory before estimate, **5** slice along the sequence, **6** decisions carry recommendations, **7** don't over-plan the trivial. Apply them, and read them there rather than here. This step used to restate a partial list, and the two copies drifted: pattern 7 existed only in the Appendix. An operator override addresses one as `planning pattern #N`, and a pattern number is not a lens number, so cite a pattern as "pattern 5" and a lens as a bare "5".

Five of them name the lenses they compose, in the Appendix itself: pattern 1 through lens 10, pattern 3 through lens 8, pattern 4 through lens 6, pattern 5 through lenses 11, 12 and 13, and pattern 6 through lens 14. Two are worth naming here because they decide how much of the catalog you open at all: pattern 1, which sets ceremony before anything else, and pattern 7, which is the licence to stop early and say so.

**Operator overrides on patterns.** Before composing, consult `deliberate-engineering-overrides` twice over: for any `disable` or `modify` on a composition pattern you are about to apply, addressed as `<catalog> pattern #N`; and for any `add: <catalog> pattern` entry, which carries no shipped number and so is invisible to a lookup keyed on what you selected. Both are honored here rather than at lens selection, because a pattern is applied to the lenses and not to the artifact. Declare every deviation in the Output.

## Step 5: Coexistence and precedence

When a planning or brainstorming engine is present (e.g. `superpowers`), **run its process** and apply these lenses to the decisions within it: this skill decides *what to build and how much process*, the engine handles *how to plan*. It never requires removing any other tool. When the work then moves to implementation, the deliberate flow continues into review and verification.

## Output

Report, briefly: the classification (4 axes), the ceremony band, the lenses selected (by number) and why, what you scoped **out** and why (the most valuable part of a plan), anything deliberately skipped, and the plan itself: every decision point carrying a recommendation with its rationale. When a decision rests on a fact about the codebase, data, or feasibility, tie it to the evidence that established it in this pass (the `file:line` read, the spike run and its result) rather than to recalled belief: a plan built on an unverified premise is a hypothesis, not a plan.
