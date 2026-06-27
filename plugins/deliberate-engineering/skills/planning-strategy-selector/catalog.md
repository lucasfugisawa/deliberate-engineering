# Planning Strategy Catalog

This catalog contains 19 planning strategies organized into six groups plus composition patterns. Each strategy is a lens of *judgment applied to planning* — deciding what to build, how much process the work calls for, how to slice and sequence it, and how to capture it. The selector skill references these by number to build a planning approach tuned to the work's clarity, risk, and reach.

## What this catalog is — and is not

This is **not** a planning *engine*. It does not teach how to brainstorm, how to write a plan document, or how to author acceptance criteria — a workflow engine such as `superpowers` owns that discipline, and this layer delegates to it. This catalog is the **deliberate judgment** exercised *while* planning: the decisions about scope, ceremony, decomposition, sequencing, and artifact shape that separate a plan that builds the right thing from a plan that builds everything plausible.

It sits *before* code exists. Where review judges an artifact and verification confronts reality, planning decides **what work is worth doing at all** — and, just as importantly, what work is not.

## Master Principle

**Decide what *not* to build before deciding how to build.** The default failure of AI-assisted work is to produce everything plausibly useful; the deliberate move is to scope to the *real* requirement and the cost of being wrong, then plan in proportion to risk — not in proportion to how much the agent could generate. A plan's job is to make the right work obvious and the wrong work visible, before a line is written.

---

## Part A — Scope: the least that is truly required

*The anti-vibe spine. Most planning value is in what you decline to build.*

### 1. Simplest mechanism that meets the real requirement

- **How it works:** Start from the plainest construct that satisfies the actual need, and adopt anything heavier (a new abstraction, a service, a queue, a framework) only when a concrete, present requirement forces it. Name that forcing requirement out loud; if you can't, don't add the mechanism.
- **Objective:** Keep complexity proportional to need, not to imagination.
- **When most valuable:** Always, as the default posture; especially when the agent proposes infrastructure for a problem you don't yet have.

### 2. Strip the speculative (YAGNI)

- **How it works:** Audit the proposed scope and *remove* what isn't required now — speculative fields, flags, config knobs, metrics, abstractions, and acceptance criteria added "in case." Demand a concrete justification — a real, current consumer — before any element earns its place; an imagined future consumer does not. (Where strategy 1 declines to *add* heavy mechanism, this one *subtracts* what was already proposed.)
- **Objective:** Cut the cost of carrying features nobody needs yet (maintenance, surface area, confusion).
- **When most valuable:** Reviewing a proposed scope or spec that has grown beyond its requirement; a shared abstraction with a single real consumer.

### 3. The correctness counter-rule — don't under-scope what's required to work

- **How it works:** The opposite failure to over-engineering: hold the firm line that anything genuinely required for the change to *function correctly* stays in scope, even if it enlarges the diff. Cutting a needed validation, error path, or migration step is not "simplicity" — it is shipping broken work.
- **Objective:** Keep YAGNI from sliding into under-engineering; "minimal" means minimal-and-correct.
- **When most valuable:** Whenever scope is being trimmed; the moment "let's keep it simple" starts removing things the feature needs to be right.

### 4. Push work to its proper owner

- **How it works:** Distinguish a local fix from a shared-infrastructure or cross-team concern. Do the minimal local fix, alert the owning team to the real problem, and file a follow-up to remove any temporary workaround once it's fixed upstream. Declare a topic out of your scope once its right owner has it.
- **Objective:** Avoid both scope creep into others' domains and permanent local workarounds for non-local problems.
- **When most valuable:** A defect whose root cause lives in shared infra; work that straddles team boundaries.

---

## Part B — Ground the plan in reality

*Plan against what is actually on disk, in production, and provably possible — not against the prose or a guess.*

### 5. Verify repo reality before planning

- **How it works:** Before committing to a plan, confirm the codebase's actual structure, tooling, build mechanisms, and existing patterns — and re-plan around what is really there. When the ticket/spec prose and the code disagree, trust the code and adjust the plan.
- **Objective:** Stop planning against an imagined or stale picture of the system.
- **When most valuable:** Any change to existing code; whenever the plan rests on assumptions about how things currently work. (Evidence-gathering analog: verification-catalog strategy 1, *query the live canonical source* — use that to get the facts this lens plans around.)

### 6. Front-loaded classified inventory

- **How it works:** For parity, migration, or "make X match Y" work, make the *first deliverable* a complete inventory of the gap, classified (e.g. missing / extra / drift / cosmetic) and grouped by area — before any implementation. Scope the build against that evidence.
- **Objective:** Replace "we'll discover the work as we go" with a known, bounded work-list decided up front.
- **When most valuable:** Migrations, parity efforts, large refactors, anything where the true size is unknown until surveyed.

### 7. Blast-radius modeling for data-semantic changes

- **How it works:** Before renaming, repurposing, or changing the meaning of a field, enum, or source-of-truth, enumerate *every* reader and consumer — across services, reports, integrations, and warehouses — including by searching repos not checked out locally. Commission a systematic downstream survey before deciding the change is small.
- **Objective:** Surface the true reach of a semantically loaded change so it isn't scoped as "a one-line rename."
- **When most valuable:** Any change to the meaning of shared data; source-of-truth migrations; field repurposing. (Static analog: review-catalog lens 32, *cross-service consistency*, judges the change side-by-side; evidence analog: verification-catalog strategy 21, *quantify usage + cross-check truth*, proves it before mutating. This lens models the reach *while planning*, before either.)

### 8. Spike to retire the riskiest unknown

- **How it works:** When requirement clarity or feasibility is low because nobody yet knows whether the approach is even possible, run a *timeboxed* spike or throwaway prototype aimed squarely at the single riskiest assumption — enough to learn, not to keep. Commit to the real plan only after the spike has resolved the unknown; then discard the spike.
- **Objective:** Replace planning-on-a-guess with planning-on-a-finding; retire feasibility risk before committing to a full build.
- **When most valuable:** Low-clarity or novel-approach work; an unproven integration, library, or technique the whole plan depends on.

---

## Part C — Calibrate the ceremony to the risk

*How much process does THIS work call for? Match it, in both directions.*

### 9. Plan-before-code gate

- **How it works:** For non-trivial work, no implementation until the approach is presented and explicitly approved. Frame open-ended work as "help me understand and decide, not build yet" — explore, lay out options, agree on an approach, *then* build. If the agent starts editing prematurely, stop it and return to the decision.
- **Objective:** Prevent committing effort (and a sunk-cost bias) to an approach nobody agreed to.
- **When most valuable:** Ambiguous, risky, or large work; any time the right approach isn't obvious. (This is also a cross-cutting standing rule — present the plan, await approval.)

### 10. Calibrate ceremony to risk and blast radius

- **How it works:** Scale process to the actual risk and reach of the change. Complex/risky/irreversible work earns a full spec and repeated deep review; a trivial config or schema-only fix may skip the spec and lean on CI. Calibrate to who *really* consumes the change, not to how the spec is literally worded.
- **Objective:** Avoid both over-processing the trivial and under-processing the dangerous.
- **When most valuable:** At the start of every task, to set the planning depth. **The ruler is risk and reach, not size.**

---

## Part D — Slice and sequence the work

*Shape the units of change and their order so each step is safe and reviewable.*

### 11. Decompose for human reviewability

- **How it works:** Size units of change so each PR stays small-to-medium and easy to review, splitting along clean concern boundaries (e.g. schema migration / data-access / logic / wiring) — while avoiding an explosion of tickets that creates more overhead than it saves. Let granularity be chosen by what *reviews* best, not by a fixed dogma.
- **Objective:** Make each change independently understandable, testable, and revertible.
- **When most valuable:** Any change large enough to split; work spanning multiple concerns. (Static analog: review-catalog lens 11, *change-size / reviewability* — that judges a finished diff; this designs the split before the work starts.)

### 12. Sequence to avoid hidden intermediate states

- **How it works:** Stress-test the plan's ordering with non-leading questions: would this step leave the system in a state that is *neither* the old-correct *nor* the final-correct behavior? Is now even the right moment? Confirm prerequisites and dependency-unblocking before executing, and do the independent items first.
- **Objective:** Ensure every intermediate state of a multi-step change is itself safe — no window of brokenness between steps.
- **When most valuable:** Multi-step migrations, changes spanning services/datastores, anything that can't ship atomically. (Overlaps verification-catalog strategy 13, *deploy ordering* — plan the order here; verify it there.)

### 13. Migration backward-compatibility — the old code must survive

- **How it works:** Treat any schema or data change as something the *currently-running* code must survive: in a non-atomic deploy the old version keeps serving while the change rolls out, so backward-compatibility is judged against that live old code — it must still both *read* what it expects **and** *write* semantically valid rows (passing only one is not safe). When a change can't be made compatible in a single deploy — a rename, a drop of something still referenced, a `NOT NULL` without default, a type change — don't ship it as one step; phase it across explicit deploy boundaries and do only the safe step now, never trading safety for fewer PRs. The judgment is choosing the right multi-step shape: **expand → adopt → contract** for a non-additive change, or **dual-write + backfill** for a large *online* data move — keeping a proven fallback and advancing one *deployed* phase at a time. When in doubt, add a deploy boundary rather than remove one.
- **Objective:** Keep every step of a multi-deploy schema or data change compatible with the code running beside it, so a migration never becomes an outage even when the new code is correct.
- **When most valuable:** Any schema change to a live system; renames, drops, constraint/type tightening; large online data migrations; anywhere schema and code deploy separately. (Sequencing analog: lens 12, *avoid hidden intermediate states* — that keeps each step internally safe; this keeps each step compatible with the *old code still running*. Evidence analogs in verification: strategy 13 *deploy ordering*, 14 *kill-switch/fallback*, 21 *reconcile before cutover*.)

---

## Part E — Capture the plan

*The plan is itself an artifact; judge what altitude and self-containment it needs for its readers and decisions — not the templating mechanics of producing it.*

### 14. Recommend, don't enumerate

- **How it works:** When the plan presents alternatives, also state which one you recommend and why, naming the axis that decides it (best outcome / least risk / fastest) and the trade-off. Surface options *with* an opinion, never a neutral menu that pushes the whole judgment back to the reader. If you genuinely can't recommend, say what information would decide it.
- **Objective:** Make the planning judgment explicit and reviewable — the reader challenges your rationale, not just your list.
- **When most valuable:** Every decision point in a plan. (This is also a cross-cutting standing rule.)

### 15. Self-contained, dual-audience artifacts

- **How it works:** A spec or ticket carries a plain-language context/rationale section for humans *and* a detailed implementation/validation/deployment section for an autonomous agent — with no dangling references to external docs, internal IDs, or unexplained shorthand. A reader needs nothing else to understand it. Keep only work that will actually be done; a plan is not a wish list.
- **Objective:** A planning artifact that stands alone and serves both the human who approves it and the agent who executes it.
- **When most valuable:** Any spec/ticket that will outlive the conversation or be handed to someone (or an agent) without the original context.

### 16. Calibrate document altitude to audience

- **How it works:** Set the altitude of each planning/communication doc to its purpose. Aggressively cut implementation detail from an intent-communication artifact; present top-down, with detail living next to the item it concerns rather than in repeated passes at different altitudes; choose the representation (prose / table / diagram) that fits each point.
- **Objective:** Match the document's level of detail to the decision it supports, so readers aren't drowned or starved.
- **When most valuable:** Design docs and proposals with mixed audiences (deciders vs implementers); any doc that keeps drifting between "why" and "how."

---

## Part F — Disambiguation: turn a vague problem into a ready task

*Before any of the above can apply, the work has to be clear enough to plan. These lenses govern the front of planning: clearing the fog, deciding which open questions block, and judging when work is ready to become a task.*

### 17. Clear the fog with evidence before asking

- **How it works:** Faced with a vague, broad, or ill-defined problem, first exhaust what is already knowable — the code, the docs, the product docs, the discussion threads, the email trail (delegate the search to an agent where it scales) — not only to find the answer outright but to reach whoever *can* answer with grounded, context-loaded questions. Never arrive with a raw question you could have answered or sharpened yourself; help the people who help you by carrying the context to them.
- **Objective:** Convert ambiguity into precise, directed questions, minimizing round-trips and the burden you place on others.
- **When most valuable:** Any ill-defined problem before planning begins; any question you are about to address to a busy human. (Evidence analog: review-catalog lens 14 and verification strategy 1 gather facts from the canonical source; this lens uses that gathering to *disambiguate the requirement* before a plan exists, distinct from lens 5, which plans against the code once the requirement is clear.)

### 18. Decide early what's costly to reverse, late what's cheap to adjust

- **How it works:** Triage the open questions by reversibility. Anything that shapes architecture, design, or carries considerable risk is **blocking** — resolve it *before* proceeding, because a wrong call there is expensive to undo. Anything absorbable through incremental, low-commitment adjustment can stay open and resolve live as execution reveals the answer. Settle architecture and design deliberately up front; defer implementation micro-decisions that live execution may well change — a premature detail decision is waste waiting to happen.
- **Objective:** Spend deliberation early where being wrong is costly to reverse, and avoid premature commitment where the cost of changing course is low.
- **When most valuable:** The start of any ambiguous work; whenever a set of open questions has to be triaged into "block now" versus "answer later." (This is the plugin's reversibility thesis applied to *decision timing*; kin to lens 8, which retires feasibility risk with a spike, where this triages decision criticality.)

### 19. Readiness-and-viability gate

- **How it works:** Treat work as ready to become an executable task only when requirements, architecture, and design are clear and the critical open questions (lens 18) are resolved. Before that gate, survey complexity, effort, risk, and timeline to form a viable macro picture, and align that viability with the team, product, and stakeholders. A task should be as well-defined as it can be before execution begins; genuine implementation details may be left to resolve along the way.
- **Objective:** Let work cross from planning into execution only when it is near-autonomously actionable and agreed to be viable — not before.
- **When most valuable:** The gate between planning and executing; any work that will be sliced into tasks or handed to an agent or another engineer. (Kin to lens 10, calibrate ceremony to risk, and lens 11, decompose for reviewability — that sizes the slices; this decides the work is ready to be sliced at all.)

---

## Appendix — Composition Patterns

*How to chain planning strategies together.*

- **Calibrate first:** Set ceremony (10) early — it decides how much of the rest of the catalog you even apply. A trivial-and-safe change may use almost none of it; say so.
- **Scope down, then ground up:** First decline the speculative (Part A), then confirm what remains against the real codebase, data, and feasibility (Part B). Cutting before grounding wastes less investigation.
- **Spike before you plan the unknown:** If feasibility is the blocker, retire it with a timeboxed spike (8) *before* committing to a plan — don't plan a build on an unproven assumption.
- **Inventory before estimate:** For unknown-size work, the classified inventory (6) precedes any commitment to a plan or timeline — don't estimate what you haven't surveyed.
- **Slice along the sequence:** Decomposition (11) and sequencing (12) compose — split along concern boundaries, then order the splits so every intermediate state is safe.
- **Decisions carry recommendations:** Every fork captured in the plan pairs options with a recommendation (14); a plan full of open menus has deferred the planning, not done it.
- **Don't over-plan the trivial:** Planning has a cost. When the work is trivial-and-safe, skip the spec, do it, and state that you judged it low-ceremony — the same calibration (10) applied to planning itself.
