---
name: debug-operate-strategy-selector
description: "Use when a live system behaves unexpectedly and you must diagnose under uncertainty or respond to an incident — error rates climbing, a flow broken with no known cause, a page you have to act on. You don't yet hold a reliable expectation; you're discovering what's true while the system may be degraded. Classifies the evidence quality and how irreversible being wrong is, then selects strategies from the catalog and dispatches superpowers for the debugging method. Distinct from verify: verify confirms an expectation you already hold; this is discovery under failure."
---

# Debug/Operate Strategy Selector

The deliberate layer of diagnose-and-respond-under-failure. Where verify confronts a claim you already hold with reality, this skill begins where there is **no reliable expectation** — a live system is misbehaving and you don't yet know why, or an incident is live and you must act before you fully understand. It decides *which* evidence to trust when production signals lie, *which* failure signature you're reading, and *how* to respond while the system is degraded and the clock is running.

The reference for every strategy cited below is `catalog.md` in this directory (16 strategies in five Parts + composition patterns). Read **only** the Parts you select — progressive disclosure, not the whole file.

## Verify vs. debug/operate — stay on the right side of the line

- **Verify** (the `verification-strategy-selector` skill): you hold an expectation tied to a known change and gather evidence to *confirm* it. ("I shipped X; did it do X? Did my backfill set the rows I intended?") Confirmation.
- **Debug/operate** (this skill): you have no trustworthy expectation — you're hunting a cause in a live system, or deciding how to respond while it's degraded. ("Why are error rates climbing? Do I revert or roll forward?") Discovery under failure.

The dividing axis is the **epistemic mode**, not the subject matter. If you can state "it should do X" and you're checking whether it did, that's verify. If you can't yet state what it should be doing — you're forming that picture from partial signals — that's this skill. They **compose**: under a live break, restore and diagnose *here*, then verify the fix in the verify skill. Where the seam shows — kill-switches, post-deploy confirmation, production-mutation protocols — verify owns that content; this skill cross-references it rather than restating it.

## Superpowers vs. debug/operate — method vs. judgment

`superpowers:systematic-debugging` owns the *method* of debugging — hypothesis, bisection, isolation, elimination. This skill does **not** teach that method and never reinvents it. What it adds is the *judgment* the method sits on: which signals are trustworthy (Part A), which failure-mode signature you're reading (Part B), and how to respond under pressure (Part C). When the work reaches hypothesis-elimination mechanics, **dispatch `superpowers:systematic-debugging`** as a tactic and own the judgment around it.

## When a quick read suffices — don't over-respond

Incident-response posture has a cost, and it has a symmetric failure mode to over-verifying: standing up Parts C/E machinery for a single benign log line is the same misplaced ceremony, inverted. A one-off line with an obvious cause and **no live degradation** doesn't need a response posture — read it, fix or dismiss it directly, and **say so**: state that you judged it low-stakes and handled it by reading rather than by an incident pass. Reserve the restore-first, escalate, retrospective machinery for genuine live degradation. Silence is not calibration; a stated decision is.

## When to use

- A live system is behaving unexpectedly and you don't yet know why.
- Error rates, latency, or a backlog are degrading now and you must decide whether to revert or roll forward.
- A page or alert reaches you and you must act, route, or escalate.
- After the fire is out, to convert the incident into durable learning.
- In peacetime, to keep the signals that incident response depends on healthy.

## Step 1 — Classify the situation (four axes)

1. **Is there a reliable expectation?** No → this catalog (discovery under failure). Yes — you're confirming "it should do X" — → the `verification-strategy-selector`. **This is the entry gate.**
2. **Evidence quality** — is the signal you'd act on sampled, lossy, derived, or second-hand? A trace-derived count is an extrapolation, not a measurement; a missing log line is "no evidence either way," not proof of absence. **This sets how much Part A trust-work you need before you believe a number.**
3. **Live degradation & response reversibility** — is the service degraded *now*, and how reversible is the response (a revert to known-good vs. a fresh forward fix made under stress)? **This sets Part C depth. The ruler is the cost of staying wrong, not the size of the symptom.**
4. **Stake / severity** — elevated stakes shift the escalation threshold *toward* action: when the cost of a missed-real incident dwarfs the cost of a false alarm, bias toward escalating and restoring early.

**The ruler is the cost of staying wrong, not the size of the symptom.**

## Step 2 — Map to a depth band

The classifications are largely orthogonal: *evidence quality* (axis 2) sets how much Part A you do; *live degradation* (axis 3) sets whether Part C fires first.

- **Low-stakes / no live degradation** → minimal: establish the fact from a trustworthy signal (Part A), state what's true, stop. Say you chose a light pass (see "When a quick read suffices").
- **Active diagnosis, service stable** → Part A to calibrate which evidence you trust + Part B for the judgment on top of the method + **dispatch `superpowers:systematic-debugging`** for the hypothesis-elimination mechanics.
- **Live degradation / irreversible response** → **restore first** (Part C: revert to known-good, don't wait for the author), *then* diagnose in peacetime (Part B + superpowers), *then* learn (Part E). Part D is the peacetime band that prevents the recurrence — schedule it, don't run it mid-fire.

## Step 3 — Select strategies from the catalog

Open only the Parts matching your classification:

- **Trust the evidence** (Part A) → **1** sampled-vs-unsampled (use unsampled aggregates for "how much," traces for individual paths), **2** logs-are-lossy (absence is not proof), **3** validate-against-the-effective-version (does the flagged finding even reach your running build?).
- **Diagnose under uncertainty** (Part B) → **4** read-the-failure-signature (a resource climbing while load stays flat is a feedback loop, not demand — and it sizes the fix: small frequent increments, not one big move), **5** recover-original-intent before editing unfamiliar code under stress (Chesterton's fence at incident speed). Both sit *on top of* `superpowers:systematic-debugging`, which owns the elimination method.
- **Respond under pressure** (Part C) → **6** revert-over-roll-forward / don't wait for the author, **7** bias-toward-action on escalation when stakes are elevated, **8** an un-actionable page is reassigned or escalated, never left to sit.
- **Keep the signal healthy** (Part D, peacetime) → **9** every alert resolves to fix/tune/delete, **10** keep the error stream near-zero so a new error is high-signal, **11** tie thresholds to business recovery cadence, **12** own the observability of inputs you don't control, **13** assign ownership for end-to-end flows, not just services. (Part D judges the *live system over time* — "is this alert still actionable months on?"; review #30 judges the *diff* — "does this change add adequate instrumentation?" Cross-reference at that seam, don't restate it.)
- **Learn from the failure** (Part E) → **14** reconstruct the timeline while it's fresh, **15** run the retrospective blameless and aimed at systemic prevention, **16** convert only the highest-leverage learnings into tracked, single-owner action items.

**Worked example — mainline/shared baseline broken, cause unknown, error counts climbing:** Degraded now + no reliable expectation (axis 1 → this catalog; axis 3 → Part C fires first). Selected: **6** (revert to known-good immediately — don't wait for the original author; a broken baseline blocks everyone), then with the baseline restored, treat the evidence skeptically — **1** (the climbing count: is it from sampled traces? pull the unsampled aggregate before believing the magnitude), **2** (don't read the absence of an error log as "it didn't happen" — the pipeline is lossiest exactly under this load), **4** (read the failure signature to point the hypothesis). **Dispatched `superpowers:systematic-debugging`** for the elimination method itself. After restoration, closed the loop with **14** (timeline while fresh) → **15** (blameless retro) → **16** (one owned, tracked action item). Skipped Part D — it's peacetime hygiene, not a mid-incident task; logged as not-now, to revisit when deriving the follow-up.

**Operator overrides.** Before applying the selected lenses, consult `deliberate-engineering-overrides`: if any selected lens has an operator override (disable / modify / add), honor it and declare the deviation in the Output.

## Step 4 — Compose the response

Apply the catalog's Appendix patterns:

- **Evidence before action — except under degradation.** Establish what's true (Part A) before responding, but hold this in tension with restoration: when the service is degraded, you do *not* wait for perfect evidence — the Master Principle's second clause wins and you restore the baseline first. Name which way the tension resolves: degraded → restore; not degraded → keep gathering.
- **Restore, then diagnose.** Under a live break, Part C precedes Part B. Get the baseline back to known-good, *then* hunt the cause in peacetime — diagnosing a live outage while it burns trades the whole team's time for your curiosity.
- **Delegate the method, own the judgment.** Dispatch `superpowers:systematic-debugging` for the mechanics; this skill decides which evidence to trust and how to respond. Different jobs — don't reinvent the method.
- **Peacetime feeds wartime.** Part D's hygiene is what makes Part A's evidence trustworthy in the *next* incident. Every shortcut taken in peacetime is a blind spot inherited mid-incident.
- **No silent skipping.** If you couldn't establish a fact — lossy logs, sampled data, no access — **say so and name the limit**. An unestablished fact is a known unknown, never a quiet "fine"; never let an absence read as confirmation.

## Step 5 — Coexistence and precedence

When other tooling is present (CI, observability dashboards, a test runner, `superpowers:systematic-debugging`), **THIS skill decides what the situation needs** and invokes those tools as *tactics* — dispatch `superpowers:systematic-debugging` for the debugging method; treat CI and observability as *evidence sources*, calibrated through Part A (a dashboard number may be sampled; a missing log may be dropped). It never requires removing any other tool; it orchestrates and delegates, noting the delegation.

When the **`verification-strategy-selector`** is co-active on the same task, they compose in order: under a live break, **debug/operate restores and diagnoses here**, then **verify confirms the fix** (the epistemic mode flips from discovery back to confirmation once you hold an expectation again). Don't run an incident posture on something a read settles, and don't call a fix done until verify has produced the evidence that it holds.

## Output

Report, briefly: the classification (reliable expectation? evidence quality, live degradation & reversibility, stake), the depth band, the strategies selected (by number) and why, anything deliberately skipped and why (e.g. Part D logged as not-now), and the diagnosis or response — with **the evidence quality named** for every signal you acted on (sampled / lossy / derived, and any fact you could not establish). If an incident occurred, close with the learn step: timeline (14), blameless analysis (15), and the owned, tracked action item (16).
