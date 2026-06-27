# Debug/Operate Strategy Catalog

This catalog contains 16 strategies organized into five groups plus composition
patterns. Each strategy is a lens for the moment a *live system* behaves
unexpectedly and you must diagnose under uncertainty and respond — deciding
which evidence to trust, which failure-mode you're looking at, and how to act
while the system is degraded. The selector skill references these by number to
build a response tuned to the quality of the evidence and to how irreversible
the consequence of being wrong is.

## What this catalog is — and is not

This catalog is the *judgment* layer for diagnose-and-respond-under-failure. It
does **not** teach the *method* of debugging — hypothesis, bisection, isolation,
elimination. That belongs to `superpowers:systematic-debugging`, which this
catalog delegates to and cross-references. What it adds is judgment: which
signals are trustworthy, which failure-mode signature you're reading, and how to
calibrate a response when the system is degraded and the clock is running.

It is also **distinct from verification.** Verification *confirms an
expectation* you already hold, tied to a known change ("I shipped X; did it do
X?"). Debug/Operate begins where there is **no reliable expectation** — the
system is misbehaving and you don't yet know why, or an incident is live and you
must act before you fully understand. The dividing axis is the epistemic mode,
not the subject matter: verify is confirmation; this is discovery under failure.
Where the seam shows — kill-switches, post-deploy confirmation, production-
mutation protocols — the verify catalog owns that content, and this catalog
cross-references it rather than restating it.

## Master Principle

**When a live system behaves unexpectedly, establish what is true before you act
— and calibrate the response to the cost of staying wrong, not to the size of
the symptom.** Evidence from a production system is partial and misleading by
default (sampled, lossy, derived), so the quality of the evidence governs your
confidence; and when the service is degraded, restoring the shared baseline
outranks diagnosing the cause.

---

## Part A — Trust the Evidence

*The epistemics of diagnosis: which signals you can rely on when hunting a cause
in a live system.*

### 1. Distinguish sampled from unsampled data

- **How it works:** Before you read a number off a dashboard, know how it was produced. A count derived from sampled traces is not a count — it is an extrapolation that can be off by the sampling factor and skewed by which paths got sampled. Use unsampled aggregates when you need a magnitude ("how many requests failed?"); use traces to understand an individual path ("what did *this* request do?"). Don't let one stand in for the other.
- **Objective:** Stop treating an estimate as a measurement, the error that turns a small problem into a phantom large one (or hides a real large one).
- **When most valuable:** Any time a decision rests on "how much" or "how often" and the data behind it might be sampled; reconciling a trace-derived figure against a billed or logged total.

### 2. Treat logs as lossy by default

- **How it works:** The absence of a log line is not proof that the event didn't happen. Logging pipelines drop, buffer, sample, and lag — and they do it worst exactly when you need them most, under the load or outage you're investigating. Read a missing line as "I have no evidence either way," not as "it didn't occur," and corroborate with an independent signal before you build a conclusion on a silence.
- **Objective:** Prevent the seductive false inference — "there's no error log, so there was no error" — that sends an investigation down the wrong path.
- **When most valuable:** Investigating under high load or degradation (when the pipeline is most lossy); any conclusion that hinges on something *not* appearing. (Compare verify #19, which treats absence of an expected signal as itself worth investigating; that lens assumes a reliable channel — this one adds that the channel itself may be dropping events, so absence is weaker evidence still.)

### 3. Validate a finding against the effective version

- **How it works:** Before chasing a flagged vulnerability, regression, or suspicious dependency, confirm it actually affects the *resolved, effective* version your system runs — not the version a report names in the abstract. Resolution, transitive overrides, and pins frequently mean the flagged issue is already patched or never reachable in your build. Resolve the effective version first, then decide whether there's anything to chase.
- **Objective:** Spend investigation budget only on findings that are real for *your* running system, not on noise from a scanner reasoning about a version you don't ship.
- **When most valuable:** Triaging a security or dependency alert under pressure; any finding stated against a declared version rather than the resolved one. (Review #36 finds the candidate in the static artifact and verify #2 grounds the provenance; this lens decides, under live-investigation pressure, whether the candidate is even reachable before you act on it.)

---

## Part B — Diagnose Under Uncertainty

*Deliberately thin. `superpowers:systematic-debugging` owns the method —
hypothesis, bisection, isolation. This part adds only the judgment that sits on
top of the method.*

### 4. Read the failure-mode signature

- **How it works:** Some failures carry a tell that points to a cause faster than blind elimination. A resource climbing while incoming load stays flat is the signature of a feedback loop, not of demand — something is amplifying itself, not responding to traffic. Learn the recurring signatures and let them steer the hypothesis, and calibrate the *fix* to the signature too: a runaway loop is tamed by small, frequent increments and short cooldowns, not one large change, and that pattern generalizes to any warm-up-costly runtime where a big abrupt move overshoots. The method still belongs to superpowers; the signature just tells you where to point it.
- **Objective:** Use the shape of the failure to shorten the search and to size the response correctly, instead of treating every symptom as an undifferentiated mystery.
- **When most valuable:** Recurring or self-amplifying failures (resource exhaustion, retry storms, thundering herds) where the symptom's shape is itself diagnostic.

### 5. Recover original intent before changing unfamiliar code

- **How it works:** Under incident pressure the temptation is to rip out the thing that looks wrong. Resist it long enough to recover *why* the suspect code exists — its authors, the original design, the decision it encodes — so you don't remove a load-bearing constraint you don't yet understand and trade one incident for a worse one. This is Chesterton's fence at incident speed: understand the fence before you tear it down.
- **Objective:** Avoid a "fix" that breaks a deliberate, non-obvious decision, the failure mode of confident edits to unfamiliar code under stress.
- **When most valuable:** Editing code you didn't write, mid-incident, where the design rationale isn't obvious from the code alone. (Apply rule 3 — distrust derived docs, go to the primary source for the intent — and dispatch `superpowers:systematic-debugging` for the elimination method itself.)

---

## Part C — Respond Under Pressure

*The incident's one-way doors: decisions made while the system is degraded,
where the ruler is the cost of staying wrong, not the size of the symptom.*

### 6. Revert over roll-forward; don't wait for the author

- **How it works:** When the shared baseline — the mainline, the deployed state everyone depends on — is broken, restoring the known-good state outranks crafting a forward fix. A revert is fast, well-understood, and reversible; a forward fix is a fresh untested change made under stress. And any engineer can and should restore the baseline: a broken baseline blocks everyone, so waiting for the original author to wake up or weigh in costs the whole team. Restore first; understand later.
- **Objective:** Get the shared baseline back to known-good in the shortest, lowest-risk way, ahead of the slower satisfaction of a "proper" fix.
- **When most valuable:** A regression in a shared/mainline baseline that blocks others; any degraded state where a known-good prior version exists to fall back to.

### 7. Bias toward action on escalation when stakes are elevated

- **How it works:** When the stakes are elevated, over-escalating a borderline incident is preferable to hesitating. The cost of pulling in help that turned out unneeded is small and recoverable; the cost of sitting on something that turned out serious compounds while you deliberate. Calibrate the escalation threshold to the stakes — and the team's culture should explicitly permit erring toward action so no one fears looking alarmist.
- **Objective:** Resolve the hesitation that lets a serious incident grow during the minutes spent deciding whether it's serious.
- **When most valuable:** Borderline-severity incidents where stakes are high and the cost of a false alarm is low relative to the cost of a missed real one.

### 8. An un-actionable page is reassigned or escalated, never left to sit

- **How it works:** If a page reaches you and you can't act on it — wrong owner, missing context, missing access — your job is to route it: reassign it to who can, or escalate until someone owns it. What you must not do is let it sit because it isn't "yours." An active incident outranks routine work, and ownership of the *response* is explicit and transferred deliberately, never silently assumed to be someone else's problem.
- **Objective:** Guarantee every live page has an active owner, eliminating the dropped-page gap where everyone assumes someone else has it.
- **When most valuable:** On-call hand-offs; pages that land on the wrong person; any incident where response ownership is ambiguous.

---

## Part D — Keep the Signal Healthy

*The peacetime hygiene that makes Parts A–C possible next time. Review #30 judges
the diff — "does this change add adequate instrumentation?"; this part judges the
live system over time — "is this signal still trustworthy and actionable months
on?" Cross-reference at that seam, don't restate it.*

### 9. Every alert resolves to fix, tune, or delete

- **How it works:** An alert that fires and gets routinely ignored is worse than no alert: it breeds fatigue and quietly erodes trust in *every* alert, so the real one gets ignored too. Treat each firing alert as forcing one of three outcomes — fix the underlying problem, tune the alert so it only fires on something actionable, or delete it. "Acknowledge and move on" repeatedly is not a fourth option; it is decay.
- **Objective:** Keep the alert set fully actionable so a page always means "do something," preserving the signal that incident response depends on.
- **When most valuable:** Periodic alert review; any alert that has fired repeatedly without a corresponding action. (Review #30 checks that alerts *exist* in the diff; this keeps them *actionable* over time.)

### 10. Keep the error stream near-zero so a new error is high-signal

- **How it works:** Triage every error to a terminal state — fixed or explicitly backlogged with a reason — so the steady-state error stream sits near zero. When the baseline is zero, a freshly appearing error is unambiguous signal: it means a regression, and it stands out instantly. When the baseline is a constant roar of known-and-ignored errors, a new one drowns in it and you lose the cheapest early-warning system you have.
- **Objective:** Make new errors loud by keeping old ones out of the stream, turning the error feed into a regression detector.
- **When most valuable:** Services with an accumulated backlog of tolerated errors; anywhere the error feed has stopped being read because it's always noisy.

### 11. Tie alert thresholds to business recovery cadence

- **How it works:** Set staleness and age thresholds from how the business actually recovers, not from a generic default. The right question is "how far behind can this get before recovery becomes impossible or expensive?" — and the threshold is derived from that answer, not from a round number someone copied from another system. A threshold untethered from real recovery dynamics either cries wolf or fires too late to matter.
- **Objective:** Make a threshold mean something — fire with enough lead time to still recover, without firing on conditions that are operationally fine.
- **When most valuable:** Backlog/lag/age alerts; any threshold currently set to a generic default rather than derived from the cost of falling behind.

### 12. Own the observability of inputs you don't control

- **How it works:** If someone else's change to your *inputs* — a configuration value, a pricing table, partner or content data you consume — can break your user experience, then monitoring that surfaces such a change is your responsibility, even though the data isn't yours to author. You can't prevent the upstream change, but you can refuse to discover it only when a user complains. Instrument the inputs at your boundary so a bad one is visible to you immediately.
- **Objective:** Close the blind spot where your system breaks from an external input change you had no visibility into.
- **When most valuable:** Systems whose behavior is driven by externally-owned config or data; anywhere "it wasn't our change" has masked an outage you still owned the UX for.

### 13. Assign ownership for end-to-end flows, not just services

- **How it works:** Every individual component can be healthy while the journey across them is broken — a flow's failure lives in the seams that no single service owns. Assign explicit ownership to the end-to-end flows, not only to the services, so someone watches the journey as a whole. Unowned flows are the ones that surface for the first time mid-incident, when nobody can say whose job it was to be watching.
- **Objective:** Eliminate the gap between "all services green" and "the user can't complete the task," by giving the whole path an owner.
- **When most valuable:** Multi-service user journeys; anywhere component dashboards are all healthy but the outcome still fails.

---

## Part E — Learn from the Failure

*The opposite posture to Part C: deliberate, blameless, no pressure. Kept
separate on purpose, so the reflective stance isn't contaminated by the urgency
of the response that preceded it.*

### 14. Reconstruct the timeline while it's fresh

- **How it works:** As soon as the fire is out, reconstruct what happened and when — while memory is sharp and the logs haven't rotated away. This is the first peacetime act and the bridge from response to analysis: a concrete sequence of what was observed, decided, and done, with times, before any of it fades or gets retold into a tidier story than the truth.
- **Objective:** Capture an accurate record while it still exists, so the later analysis rests on facts rather than reconstructed memory.
- **When most valuable:** Immediately after restoration, before participants disperse and short-lived evidence (live logs, in-memory state, fresh recollection) is gone.

### 15. Run retrospectives blameless, aimed at systemic prevention

- **How it works:** Conduct the retrospective on the premise that people acted reasonably given what they knew and saw at the time. The aim is to find the systemic conditions that made the failure likely — the missing signal, the ambiguous ownership, the misleading evidence — and prevent recurrence, not to locate a person to fault. Blame doesn't just feel bad; it suppresses the candor the analysis depends on, and a retrospective people are afraid to be honest in learns nothing.
- **Objective:** Surface the real causes by making honesty safe, and fix the system rather than the individual.
- **When most valuable:** Every incident retrospective; especially after a high-visibility failure where the instinct to assign fault is strongest.

### 16. Convert only the highest-leverage learnings into tracked, single-owner action items

- **How it works:** Pick the few learnings with the most leverage and turn each into a tracked action item with exactly one owner — not a long wish-list, and not a set of good intentions with no home. A postmortem whose follow-ups have no owner and no tracking is theater: it produced the feeling of learning without the change. One owner per item makes "is this done?" answerable.
- **Objective:** Ensure the incident actually changes the system, by converting insight into owned, trackable follow-through rather than a document that's filed and forgotten.
- **When most valuable:** Closing out any retrospective; resisting the pull to either list everything (so nothing gets done) or list nothing (so nothing changes).

---

## Appendix — Composition Patterns

*How to chain these lenses together across the arc of an incident.*

- **Evidence before action:** Establish what's true (Part A) before you respond — but hold this in tension with restoration. When the service is degraded, you do *not* wait for perfect evidence; the Master Principle's second clause overrides the first, and you restore the shared baseline first. Name the tension explicitly so you know which way it resolves: degraded → restore; not degraded → keep gathering.
- **Restore, then diagnose:** Under a live break, Part C (revert/restore) precedes Part B (root-cause). Get the baseline back to known-good, *then* hunt the cause in peacetime — diagnosing a live outage while it burns trades the whole team's time for your curiosity.
- **Delegate the method, own the judgment:** Dispatch `superpowers:systematic-debugging` for the hypothesis-elimination mechanics; this catalog decides which evidence to trust (Part A) and how to respond (Parts B–C). The method and the judgment are different jobs — don't reinvent the method here.
- **Peacetime feeds wartime:** Part D's hygiene is what makes Part A's evidence trustworthy in the *next* incident — near-zero error streams, actionable alerts, owned flows, instrumented external inputs. The two are one loop across time: every shortcut taken in peacetime is a blind spot you inherit mid-incident.
- **Close the loop or it's theater:** An incident isn't done at restoration. Part E converts it into a timeline (14), a blameless analysis (15), and owned follow-through (16). Stop short of any of these and the next incident is the same incident.
- **No silent skipping:** If you couldn't establish a fact — lossy logs, sampled data, no access — say so and name the limit. Never let an absence read as confirmation; an unestablished fact is a known unknown, not a quiet "fine."
