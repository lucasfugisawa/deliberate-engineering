---
name: deliberate-engineering-router
description: "Use at the start of an engineering task when you're not sure which phase you're in, or for broad or multi-phase work — building a feature, changing a live system, chasing an incident, reviewing a diff, or shaping a design. It classifies the work, names the phase sequence and ceremony band, and routes to the matching selector (plan / review / verify / debug-operate), conducting between phases and stopping at the irreversible action. Skip for research, prose, and ad-hoc analysis."
---

# Deliberate Engineering Router

The deliberate layer of *where do I start*. Where the four selectors each own one phase, this skill operates *before any phase is chosen* — it reads the request, classifies the work, names the recommended phase sequence and how much ceremony it calls for, and routes to the selector that owns the method. It **dispatches; it does not select lenses.** It is the receptionist, not the manager: it decides which phase you are in and what shape the work takes, then hands the method to whoever already owns it.

## vs the rules — constitution vs dispatch

`deliberate-engineering-rules` is the always-on constitution: *how you behave* on every engineering task, at every altitude, regardless of phase. The router is per-session dispatch: *where you start* and *which phase you are in* for this particular request. Different altitudes. The router **references** the rules — it cites Rule 1's human gate, Rule 4's recommend-with-rationale, Rule 6's checkpoint-before-compacting — but it never supersedes them. When the two could appear to conflict, the rules win; the router only decides where to begin.

## vs superpowers/Workflow — judgment vs mechanism

A workflow engine such as `superpowers`/Workflow owns the *execution mechanism*: orchestration, spawning subagents, running a plan, the TDD loop. The router does **not** reimplement any of that. What it adds is the *judgment* layered on top: which phase this work is in, what the phase sequence should be, how heavy each phase should run, and whether the work inside a phase parallelizes or sequences. Having decided the shape, it **delegates** the mechanism to the engine that owns it. Decide, don't execute.

## When to use

- At the start of a task, before you have committed to a phase.
- When a request is broad or spans multiple phases (e.g. "ship feature X").
- When intent is unclear and no single phase is obviously implied.

It is triggered three ways: `/deliberate-engineering:start` at the start of a task (primary); by description as a safety net, when a request is broad or ambiguous and no phase is obviously implied; and optionally always-on, via the README recipe, for adopters who want it on every engineering session. Skip it for research, prose, and ad-hoc analysis — see "Ambiguity and edge cases."

## The honesty ruler

The router names only the phases that have a catalog — **plan, review, verify, debug-operate** — plus the standing rules, and the one cross-cutting catalog that is *not* a phase: `communication-collaboration-selector` (consulted by nature, never sequenced). It never invents a phase. When work touches release, rollout, infrastructure, or dependencies — phases that were never built as catalogs — it points at the *existing* lenses that already cover that ground: planning #12 (sequence so no intermediate state breaks), planning #13 (migration backward-compatibility per deploy), the verification staged-promotion / rollout lenses, and Rule 1 (the human gate on the irreversible, outward-facing action). It does **not** fake a "deploy" phase to look complete. Naming a phase that has no method behind it would be the dishonesty this plugin exists to prevent.

## When NOT to route heavy

Routing has a cost, and over-routing the trivial is the same misplaced ceremony as under-routing the dangerous, inverted. For **trivial-and-safe** work — clarity high, risk low, easily reversible, narrow reach — the router says so out loud: "this is light, a single phase, no ceremony," and dispatches directly to that one phase. Recommending little is also calibration. A stated light-touch decision is calibration; silence is not.

## Step 1 — Classify on two distinct dimensions

**Genre selects the route; the axes set how deep to go on it.** They are orthogonal questions; answer both. These two dimensions are kept separate on purpose. Conflating them — treating genre as if it carried intensity — is a category error.

1. **Genre of the work** (the router's own signal, *nominal* — a kind, not a degree). It selects the **entry phase and the sequence**. The five genres: G1 building something new; G2 changing something that already exists (including refactors); G3 a live system is failing and you must respond; G4 evaluating a finished artifact; G5 a design to discuss before any code. "New feature" is not *more* than "incident" — it is a different kind. Genre therefore carries no intensity and **never** enters the depth calculation. Genre is not an axis.

2. **The four canonical axes** (the shared vocabulary of the whole plugin, *ordinal* — each runs low→high): **requirement clarity, risk, reversibility, reach.** They set the **depth of each phase** and the **firmness of the sequence recommendation**, and they combine into one "how heavy is this" judgment. These are deliberately the *same* four axes the plan, review, and verify selectors use — the router adds **no fifth axis**, preserving one mental model across the lifecycle.

### The nature split — engineering vs communication

One mental model, applied honestly: *first the nature of the work, then the axes proper to that nature.* When the target artifact is an **engineering** artifact — code, a spec, a schema, a deploy — classify by the genre and the four canonical axes above; the genre→phase map below is unchanged. When the target artifact is a **communication** — a PR description, a review comment, a stakeholder message, an RFC, a writeup of alternatives — it does not classify by those four axes; what selects the method is **audience + artifact**. Route it to `communication-collaboration-selector`, which owns that classification. This adds no genre and no fifth axis: communication is a different *nature*, consulted cross-cutting, never a fifth phase.

Most communication is **embedded** in engineering work — you implement, then write the PR description. In that case the communication selector is a **cross-cutting consultation that does not change the current phase**: you are still in (say) review; you consult `communication-collaboration-selector` for the artifact you are about to write, then continue.

## Step 2 — Map genre → phase sequence

The router translates the genre into a recommended phase sequence. These are illustrations *inside* this skill, not a catalog:

- **G1 new feature / G2 non-trivial change** → **plan → (build) → review → verify**
- **G3 hotfix under pressure** → **debug-operate → (fix) → verify**; plan and review are compressed and *declared* as compressed, never silently dropped
- **G3 production incident** → **debug-operate** as the entry phase, with learn-from-failure at the end
- **G2 refactor** → **plan (scope / blast-radius) → review**; add **verify** only if it touches observable behavior
- **G4 standalone artifact review** → **review** (single phase)
- **G5 design to discuss** → **plan** (shaping / scoping), surfacing the decision before any code

`(build)` and `(fix)` are parenthesized because they are delegated to `superpowers` (TDD): the router *names* them in the sequence but does not execute them.

## Step 3 — Calibrate the ceremony band

The four axes from Step 1 decide *how much* of each phase to apply and *how firm* the sequence recommendation is. Trivial-and-safe → a single phase, a light recommendation (see "When NOT to route heavy"). Risky / irreversible / wide reach → the full sequence, a firm recommendation, Rule 1 gates active at the irreversible step. The router **cites** the planning lens for the method rather than copying it: see `planning-strategy-selector` catalog #10 (calibrate-ceremony-to-risk) for the full treatment of matching ceremony to stakes.

## Step 4 — Conduct

Having decided the sequence, the router invokes the selector skill for the current phase in-session — `planning-strategy-selector`, `review-strategy-selector`, `verification-strategy-selector`, or `debug-operate-strategy-selector`. When the next artifact to produce is a communication rather than code, it also consults `communication-collaboration-selector` — the cross-cutting selector, not a phase — without leaving the current phase. On completing a phase it returns, updates the live note (this phase done → next phase), and:

- if the transition does **not** involve an irreversible or outward-facing action → proceed to the next phase;
- if it does — Rule 1 fires, before a deploy, merge, publish, or tag → **stop at the gate**, hand over the prepared artifact and the recommendation, and let the human trigger the action.

State the boundary explicitly: **conduct between phases, stop at the irreversible action.** The router never crosses a Rule 1 gate autonomously; and between gates it does **not** ask permission at every step — that step-by-step friction is the shape this plugin rejects. **Recommend, never force:** the router scales the firmness of its recommendation to risk but blocks nothing. The only hard stop is Rule 1's gate on the irreversible *action* — never on the *process*. A trivial change is free to skip phases; a risky one gets a firm recommendation and, at the irreversible step, a real gate.

## The output step — visible judgment and execution shape

After classifying and sequencing, before invoking the first phase, the router emits one short output. These are two moments of that output, not separate features or formal sections — keep them concise.

**(a) Visible judgment.** Narrate *judgment*, not mechanics — "now I'll read the file" is noise, since the harness already shows tool calls. Report: the classification (genre + the four axes, one line); the recommended phase sequence and ceremony band; and **what was deliberately left out and why** — the most valuable part (e.g. "skipping verify: no observable-behavior change"). This is Rule 4's recommend-with-rationale posture, applied to routing itself.

**(b) Execution shape per phase.** For each phase, state parallel-vs-sequential and **delegate** the firing to `superpowers`/Workflow: "lenses 25/28/2 are independent → concurrent subagents via `superpowers`/Workflow"; "these phases depend on each other → sequential."

**Worked example** — request: "implement field X on the billing model":

> **Genre:** change to an existing system. **Axes:** clarity medium, risk high (billing), reversibility low, reach wide. **Sequence:** plan → build → review → verify, full ceremony. **Execution:** phases are sequential; within review, the security and migration lenses are independent → concurrent. **Skipping:** nothing — high risk allows no shortcut. **Gate (Rule 1):** I stop before deploy/merge for you to trigger. Starting with the **plan** phase.

## Live note and rehydration

When the router defines a multi-phase sequence, it **recommends recording** — where the work is *already* tracked (the plan, a working-note, the tracker; not a new file) — two things: the phase sequence, and the current phase plus the completed phases. On resume, after compaction or in a new session, the router **re-reads that anchor before reasoning** rather than guessing where it left off. This prevents the classic failures: re-planning something already planned, or skipping verify believing it already ran.

The boundary that keeps this lean: the router does **not** invent a file format or a persistence mechanism. It leans on **Rule 6** (checkpoint before compacting) and adds only the one piece outside Rule 6's stated scope — *the phase sequence and the current phase are part of what needs a durable home.* It decides and recommends; the persistence itself is delegated.

## Ambiguity and edge cases

- **Genuinely ambiguous intent → interview-by-exception.** Route by default; ask only when intent is truly undecidable from the request. One question, with a recommendation embedded (Rule 4: "I'd treat this as a change to existing behavior — confirm?"), never an interrogation. Most requests arrive with intent legible in the first message; asking there is the friction this plugin rejects.
- **Out-of-scope request** (research, prose, ad-hoc analysis) → the router goes quiet and stays out of the way, identical to the rules' scope gate. It does not force ceremony where it does not belong — that is the anti-pattern this plugin exists to prevent.
- **Phase with no catalog** (release / rollout / infra / dependencies) → the honesty ruler (above).

## Coexistence and precedence

When other workflow engines are present (`superpowers`, `feature-dev`), the router decides which phase and selector the work needs and invokes those engines as the *mechanism*; it never requires removing any of them. It references `deliberate-engineering-rules` — the constitution — rather than restating it, and routes to the four selectors for each phase's method rather than reimplementing it. The same coexistence-with-precedence stance the rest of the plugin takes: this layer decides and delegates.

## Output

Report, briefly: the classification (genre + the four axes), the recommended phase sequence and ceremony band, the per-phase execution shape, what was deliberately skipped and why (the most valuable part), and which phase the router is starting with.
