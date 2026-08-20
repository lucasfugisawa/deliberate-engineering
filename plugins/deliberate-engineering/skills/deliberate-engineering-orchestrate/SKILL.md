---
name: deliberate-engineering-orchestrate
description: "Use when the engineering work is a program too large for one session, to orchestrate or coordinate it across multiple sessions: you are running an orchestration session that decomposes the work into self-contained units, dispatches each to a fresh worker session (or, for a narrow earned band, a background subagent), verifies what comes back against primary evidence, dispositions it (accept/reject/follow-up), and tracks the whole program in one authoritative place. It is the across-session sibling of the router: the router conducts phases within one session; this orchestrates units across them. Manual-first: a fresh, human-watched session is the default dispatch, and automation is a narrow, earned exception. Skip it for work that fits one session, including single-session work you only want to parallelize into subagents (route that through the phases directly), and for research, prose, and ad-hoc analysis."
---

# Deliberate Engineering Orchestration

The deliberate layer of *running a program that will not fit in one session*. Where the router conducts the phases **within** a session and the four selectors each own one phase's method, this skill orchestrates the units of work **across** sessions: it decides what to dispatch, drafts the contract that lets a fresh session execute it, verifies what returns against primary evidence, dispositions it, and keeps one authoritative record of where the whole program stands. It is an **orchestrator, not an engine**: it decides shape and delegates mechanism, exactly as the router does, one altitude up.

The value it chases is **parallelism-without-blocking, human control, and human visibility**, in that spirit and not as labor-saving. The orchestration session stays unblocked while smaller units execute in parallel elsewhere; the operator keeps the ability to intervene when a unit stalls and stays conscious of each deliverable. If you find yourself optimizing for "dispatch more with less human attention," you have the wrong objective: that reframe drives every call below.

## vs the router: across sessions, not within one

`deliberate-engineering-router` is the front door for a single session: it classifies the work, names the phase sequence, and conducts plan, review, verify, and debug **inside** that session. This skill is its sibling one level up: the unit it moves is a whole piece of work handed to *another* session, and the loop it runs is dispatch, verify, track. The router's per-phase execution-shape call (does this phase parallelize into subagents, or sequence inline?) is the same judgment this skill makes per **unit across sessions**, plus the handoff and disposition that a cross-session unit needs and an in-session phase does not.

The boundary is also the trigger boundary: **work that fits one session is the router's, not this skill's.** Do not reach for orchestration because a single-session task has several phases, and do not reach for it merely to parallelize one session's work into subagents; route both through the phases directly. Reach for it when the program is genuinely too large for one context and its units will execute in separate sessions.

## vs superpowers/Workflow: judgment vs mechanism

A workflow engine such as `superpowers`/Workflow owns the *execution mechanism*: spawning agents, running a plan, the TDD loop. This skill does not reimplement any of it. What it adds is the *judgment* around a cross-session unit: whether to dispatch it at all, what its boundary is, what the handoff must contain, how deep to verify the return, and how to disposition it. Having decided, it **delegates** the firing to whoever owns the mechanism: a human-piloted fresh session by default, a background subagent for the narrow band below. Decide, don't execute.

## It rides on the rules; it does not restate them

Roughly two-thirds of this loop is the standing rules applied at a larger granularity, and it **cites** them rather than re-encoding them (a copy drifts from the catalog): Rule 1 keeps the human's hand on every outward or irreversible action a unit produces; Rule 3 governs verify-before-endorse and premise-freshness, and its re-derive-in-fresh-context clause is the backbone of the verify step; Rule 6 is why the program is recoverable and the orchestration session re-instantiable; Rule 8's earned-convergence is what widens the automation band; Rule 9's "resolvable by someone holding only this artifact" is exactly the self-contained-handoff bar. The genuinely new material is small: the loop, the dispatch heuristic, the disposition ritual, and the tracker, and that is all this skill adds.

## The three roles

The operator's old all-in-one "conduit" role, split so each part sits where it belongs:

- **Orchestrator** (the orchestration session): investigates, plans, decomposes work into dispatchable units, decides dispatch, drafts handoffs, verifies returns against source, dispositions them, and owns tracking and recoverability. It is **re-instantiable**: any fresh session can resume this role from the tracker plus recovery anchor (below), so a long-lived orchestration session is an optimization, never a requirement.
- **Worker** (a dispatched session): a fresh session (or, for the band below, a background subagent) given **one** self-contained unit via a handoff. It executes and returns a WORK REPORT, and then it is **done**. No idle-but-alive session held open "for later": any follow-up is a new self-contained handoff.
- **Operator** (the human): keeps the two jobs that stay human, which are the *decision and visibility* loop (approve dispatch, watch, intervene) and every *outward or irreversible* action (post, merge, tag, deploy), per Rule 1. The mechanical relay between those is a candidate to shed as trust converges, never the judgment or the gate.

## The loop

```
plan (the orchestration session, in-session via the router + selectors)
 -> DISPATCH DECISION: inline vs dispatch; if dispatch, manual session vs subagent (see the two Steps below)
 -> HANDOFF: fill the contract (templates.md) and FREEZE THE PREMISE against a live-state read taken now
 -> EXECUTE: a fresh human-watched session by default; a background subagent only for the earned band
 -> WORK REPORT returns (the inbound contract in templates.md)
 -> VERIFY at source; for a contested or high-stakes claim, re-verify in a SEPARATE context, scope = the claim (Rule 3)
 -> DISPOSITION: accept / reject / follow-up
 -> TRACKER: self-audit + read-back-after-write on this disposition checkpoint (Rule 6)
 -> COMMIT the disposition (its git history is the audit trail); the operator triggers anything outward (Rule 1)
 -> CAPTURE any operator-caught gap back into overrides/catalog (/deliberate-engineering:capture and :contribute)
The worker is now done. A follow-up is a NEW self-contained handoff, never a kept-alive session.
```

Comms the loop produces (a reviewer reply, an operator-facing paste, a status note) route through `communication-collaboration-selector` and `deliberate-engineering-voice`, the same as any other communication; whether a batch is handled interactively or fully delegated stays an operator choice.

## Step: the dispatch decision (the autonomy core)

These are heuristics, not a state machine; they are the planning selector's calibrate-and-decompose judgment (planning #10 and #11) applied one level up, to a unit instead of a task.

- **Dispatch-or-inline.** Dispatch a unit when it (i) is independently specifiable as a self-contained handoff, (ii) is enough work that it dwarfs the handoff-plus-verify overhead, and (iii) either parallelizes with other in-flight work, or needs a fresh context to escape the orchestration session's accreted context, or needs adversarial independence from that session's own prior conclusion. Do it inline when the unit is trivial-and-safe, is tightly coupled to live orchestration-session context, or when writing the handoff would cost more than just doing it.
- **Unit boundary.** A dispatchable unit is a verifiable done-condition, with minimal write-contention against other in-flight units (no shared files or branch, so parallel returns do not collide), and a premise that can be frozen into the handoff.
- **Disposition trigger.** Verify-at-source produced evidence as wide as the claim: accept. The evidence contradicts the report: reject. The evidence is partial: follow-up. The disposition *trigger* is mechanical; the *branch* is judgment, and it is a review, not a rubber stamp (disposition is the review selector applied to a returned unit).
- **Verification depth.** A contested or high-stakes accept earns a separate-context re-verification (Rule 3: re-reading in the context that produced the finding is confirmation, not recomputation); a trivial, low-stakes return is fine on an inline read. This is the compound failure the loop exists to prevent: a confidently-wrong report meeting a too-narrow check, and a wrong accept shipping.

## Step: manual session vs background subagent (the earned, narrow band)

The default dispatch is a **manual fresh session**: it maximizes control (you can intervene the moment a unit stalls on a missing access, tool, or MCP, or heads down a bad path), visibility (the operator stays conscious of each deliverable), and true independence (a separate context and token budget, and full fresh context for a large unit).

A **background subagent** is allowed only when the unit is **all** of:

- self-contained and **analytical or mechanical**: you want the result, there is nothing to pilot; and
- free of any **stall-able external prerequisite**: no access, tool, or MCP dependency that would need a human to unblock; and
- **low-stakes and reversible**; and
- ending in **no outward or irreversible action**.

The archetype is an adversarial critique, a read-only survey, or a scoped search. A subagent shares the orchestration session's process and token budget, so a manual session stays better for large units and for adversarial independence. The band **widens only as trust converges** on a unit-type (Rule 8), never by default, and it carries a **token-budget gate**, because one orchestration session plus N subagents plus verification fan-out compounds fast. When you take the subagent path, say so and say why the unit clears all four conditions (the elevated-autonomy declaration the rules already ask for).

## The artifacts

Three contracts carry the program; their skeletons live in `templates.md` in this directory, read on demand when you author one rather than loaded up front. The skeletons **prescribe the required fields and leave the layout free**: the fields are what made real handoffs work, and the formatting is yours to adapt, and to grow only when a section actually overflows (start flat).

- **Handoff** (outbound): mandate and why; premise-freshness freeze (the live heads/PR/branch state, read *now*); exact change and scope; gates to run; verification steps; the required WORK REPORT format; an explicit DO-NOT / out-of-scope list. The orchestration session **generates** most of this from a live-state read at dispatch time; only the genuine-judgment fields (the mandate, the scope DO-NOTs) are author-filled. A handoff must be resolvable by a session holding *only* the handoff (Rule 9).
- **Work report** (inbound): the new state (SHAs/heads); what changed; gate and test evidence; decisions and judgment calls made; an explicit "not done per dispatch" list.
- **Program tracker** (state): an operator queue at the top, a chronological done-log at the bottom, per-stream status rows, and a **recovery anchor** kept always-current so any fresh session can re-instantiate the orchestration role. It self-audits on each disposition.

## Persistence: one store, delegated, scrubbed

The program tracker **is** the durable store that `deliberate-engineering-state` delegates to, not a second store beside it: when a program tracker exists, that skill records state there rather than in its own working-note (its hybrid-with-fallback stance already covers exactly this). Do not run two sources of truth.

Where the tracker lives is the operator's, and the plugin ships none of it: the recommended home is a dedicated, private, git-backed repo, one per program, synced across devices, the same precedent as the voice layer's private directory. **Start flat** (a `tracker.md`, a `handoffs/`, a `reports/`); add structure only when a folder actually overflows, never a pre-built numbered taxonomy. Handoffs are context extracts, so **scrub or gitignore any credential before committing**, especially once the repo is synced. Commit per disposition; the disposition history is the program's audit trail.

## Re-instantiable orchestration and recovery

Because context is volatile and a repo is not (Rule 6), the orchestration role's recoverability is continuous, not a compaction-time scramble. Keep the recovery anchor and tracker current on every disposition checkpoint, and on resume **re-read them before reasoning** rather than trusting a half-remembered snapshot. Verify your own persistence actions: a claim that a file was written is not proof it was (read it back). This is what lets the orchestration session be disposable and cheap to re-instantiate, which is the point: a long-lived orchestration session is an optimization, and designing for cheap re-instantiation is what stops context-rot and compaction from becoming program risks.

## Non-goals

Skip, deliberately: a formal orchestration **state-machine** (this is judgment, not an engine); a pre-built **numbered-folder taxonomy** (start flat, grow on demand); a maintained "known-gotchas" document; **real-time messaging between the orchestration and worker sessions** (it would kill the fresh-context boundary that makes a handoff worth writing); and a **duplicate per-unit state note** beside the tracker (one source of truth). Each of these trades the capability's honesty for machinery it does not need.

## Coexistence and precedence

When a workflow engine is present (`superpowers`, `feature-dev`, the Workflow tool), this skill decides the shape of the cross-session work and invokes that engine as the mechanism; it removes none of them. It references `deliberate-engineering-rules` rather than restating it, delegates the durable note to `deliberate-engineering-state`, routes each phase a worker runs to the four selectors, and routes its comms through `communication-collaboration-selector` and `deliberate-engineering-voice`. Same stance as the rest of the plugin: decide and delegate.

## Output

Report, briefly and as judgment rather than mechanics: for each unit, the dispatch decision (inline vs dispatch, and if dispatched, manual session vs subagent) with its reason; on a return, the verification depth chosen and the disposition (accept/reject/follow-up) with the evidence that decided it; and each Rule 1 gate where you stop and hand an outward action to the operator. When you take the earned subagent band, declare it and why the unit cleared all four conditions. Keep the tracker current on every disposition and say when a checkpoint was written.
