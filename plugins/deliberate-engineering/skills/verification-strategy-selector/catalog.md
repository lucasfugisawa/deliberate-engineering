# Verification Strategy Catalog

This catalog contains 22 verification strategies organized into five groups plus composition patterns. Each strategy is a way to establish that something is *actually* true — by confronting it with reality (a run, a query, the live system) rather than by reading the artifact and judging it plausible. The selector skill references these by number to build a verification plan tuned to what is being verified and how irreversible the consequence of being wrong is.

## What verification is — and how it differs from review

**Review** examines a static artifact and asks *does this look correct?* — reading a diff, a spec, a design for logic errors and contradictions. **Verification** asks *is this correct in reality?* — and answers it with evidence from running the thing: an executed test, a query against real data, a production metric, a captured payload. Review reasons about the code; verification confronts the world.

The review catalog's Part B (empirical validation, real-data validation, source-of-truth) names the *seeds* of this discipline. This catalog is that discipline at full depth, pointed at running systems and post-deploy reality. Where a strategy here has a static analog in the review catalog, it is noted — use the review lens to judge the artifact, this strategy to gather the evidence.

## Master Principle

**State the expected result before you observe the actual one.** Every verification — a test, a query, a metric check — should carry its expected answer up front, so a deviation is an immediate, unmissable signal rather than a number you rationalize after the fact. Verification without a pre-stated expectation is just looking. And: **the cost of a wrong "it's fine" scales with irreversibility** — calibrate verification depth to how hard the consequence is to undo.

---

## Part A — Evidence & Ground Truth

*The epistemics: what counts as proof, and where truth actually lives.*

### 1. Query the live canonical source as evidence

- **How it works:** When you need to know how the system actually behaves, get the answer from the live canonical source — freshly fetched current code, the running configuration, the actual schema — and quote it as evidence, rather than from a derived doc, a diagram, or a stale local checkout. Replace "I think it works like…" with "here is the current source, and it shows…".
- **Objective:** Ground every behavioral claim in primary, current evidence instead of a second-hand or stale picture.
- **When most valuable:** Any claim about how the system works that will feed a decision. (Static analog: review-catalog lens 14, *source-of-truth verification* — that lens checks you're reviewing the right artifact; this strategy gathers the live evidence from it.)

### 2. No guessing — evidence and provenance for every claim

- **How it works:** Refuse to deduce or assume. For every claim — especially every number — demand a concrete source: a run link, a query and its result, a file and line. Re-derive quantities from authoritative queries rather than estimating.
- **Objective:** Eliminate confident-but-unverified assertions, the dominant failure mode of fast work.
- **When most valuable:** Quantitative claims, impact estimates, "this is safe" assertions, anything that will feed a decision.

### 22. Match verification scope to the claim's scope

- **How it works:** Before vouching, compare the *breadth* of what you verified against the *breadth* of what you are about to claim. A pass on one environment does not support a claim about another; one case passing does not support "all cases"; a sampled check does not support a statement about the whole population. If the claim is wider than the evidence, either narrow the claim to exactly what was verified, or widen the verification until it covers the claim.
- **Objective:** Close the gap between calibrating verification *depth* (matching rigor to irreversibility, covered elsewhere in this catalog) and calibrating *breadth*: the scope of verification must be at least the scope of the claim.
- **When most valuable:** Any "it works / it's safe / it's done" statement that generalizes beyond what was directly observed — especially local-vs-production and one-case-vs-all-cases.

### 3. Name the refuting observation, then go run it

- **How it works:** State, up front, the specific observation or query that would prove your hypothesis *wrong* — then actually run it and look. Don't steer the query toward the answer you hoped for; the verification only counts if it had a real chance to refute. (This is the adversarial stance of review-lens 2, executed as evidence-gathering against the live system rather than as a read of the artifact.)
- **Objective:** Neutralize motivated reasoning; an investigation that could only confirm proves nothing.
- **When most valuable:** When you have a stake in the outcome, or when a prior pass already "confirmed" what you expected.

### 4. Validate assumptions against real data and real schema

- **How it works:** Introspect the actual schema for real column/enum/field names instead of guessing them; write exploratory queries against real (or production-like) data; iterate the query for correctness and cost; re-check conclusions against what the data actually shows. Verify that filter criteria still match the current code/spec, not a stale definition.
- **Objective:** Ground assumptions in the system as it really is, not as you remember it.
- **When most valuable:** Before any data-dependent change, backfill, or impact estimate; whenever a query encodes an assumption about meaning.

### 5. Independent second-pass re-verification

- **How it works:** After reaching a conclusion, re-verify it on a deliberate second pass — ideally with deep reasoning and without leaning on the first pass's notes. Re-confirm each finding against source directly; distrust a subagent's assertion on a contested point and re-read it yourself. Ask whether stopping now is actually warranted.
- **Objective:** Catch the error the first pass rationalized; raise confidence before you act or endorse.
- **When most valuable:** Before acting on findings, before a human reviews, before any irreversible step.

---

## Part B — Local & Pre-merge Verification

*Verify as much as possible before the change leaves your hands.*

### 6. Calibrate local-verification trust to the environment

- **How it works:** Know which checks your environment can actually run truthfully. Run compile, lint, and pure unit tests locally and trust them. For DB-backed or full-boot tests that the sandbox cannot run faithfully, run them locally when the environment allows; otherwise delegate to CI as the authority — never fake a pass or silently skip.
- **Objective:** Avoid both false confidence (trusting a check the environment couldn't really run) and false failure (a sandbox limitation read as a real defect).
- **When most valuable:** Any time local and CI environments differ in capability (databases, network, services).

### 7. Run the exact aggregate check that mirrors CI

- **How it works:** Before opening a PR, run the same aggregate verification gate CI will run — including lint/format — not a convenient subset. Mirror the command CI uses.
- **Objective:** Surface the failure on your machine, not in the pipeline after review has started.
- **When most valuable:** Before every PR; especially where CI bundles lint+format+test into one gate.

### 8. Dry-run before proposing or executing

- **How it works:** Run scripts and queries against the real (or a faithful) system in a read-only or no-op mode before proposing them for review or execution. See what they actually touch and return before they touch it for real.
- **Objective:** Replace "this should work" with "I ran it and here's what it did."
- **When most valuable:** Migrations, backfills, bulk queries, anything whose first real execution is hard to take back.

### 9. Establish a validation methodology before changes that affect others

- **How it works:** For a change whose value or safety is contested (a performance fix, a shared-behavior change), define how you will prove it works *before* proposing it: a proof-of-concept, a cold-vs-warm or before/after measurement, a named success metric. Propose only the variant that the methodology validated.
- **Objective:** Bring evidence, not a hypothesis, to a change that costs other people if it's wrong.
- **When most valuable:** Performance/optimization work; changes to shared infrastructure or contracts.

### 10. Reproduce, then confirm the change caused the fix

- **How it works:** Before changing anything, capture the failing state as concrete evidence — a failing test, the actual error, the bad payload/row. Make the change. Then re-capture the same evidence and show it flipped: the test now passes, the error is gone, the payload is correct. The before/after pair proves *this change* caused the fix — not that the code merely compiles or reads correctly. Where a real counterpart payload exists, replay it through the new code to confirm the contract holds in practice.
- **Objective:** Prove causation, not coincidence; defeat "it looks fixed" and fixes that address the wrong cause.
- **When most valuable:** Every bug fix; any change motivated by a specific observed failure. (Static analog: review judges whether the fix *reads* correct; this proves it actually resolves the reported failure.)

---

## Part C — Staged Promotion & Rollout Verification

*Each environment boundary is a gate; prove safety before crossing it.*

### 11. Staged environment-promotion gates

- **How it works:** Treat each boundary — local → pre-production → production — as a gate, and before crossing each one ask "what can I validate *here* that I can't validate after?" Validate in a real pre-production environment before merging or promoting.
- **Objective:** Catch each class of defect at the cheapest stage that can reveal it.
- **When most valuable:** Any change with a real pre-prod environment available; multi-stage deploys.

### 12. Red CI is a hard stop; distinguish flaky from real

- **How it works:** Never promote or merge on red CI until the cause is understood and fixed. When a check fails, determine whether it is a real failure or a flake *with evidence* (re-run, inspect the specific failure), rather than assuming either. Confirm a merge is safe against regressions before it lands.
- **Objective:** Refuse to launder an unexplained failure into a "probably fine."
- **When most valuable:** Always at the merge gate; especially in suites with known intermittent tests.

### 13. Verify deploy ordering and dependency availability

- **How it works:** For changes spanning services or datastores, verify that each dependency will exist *before* the code that needs it runs — schema before the reader, config before the consumer — so nothing starts into a missing dependency. Confirm the ordering, don't assume it.
- **Objective:** Prevent startup crash-loops and partial-deploy breakage from out-of-order rollout.
- **When most valuable:** Multi-service / multi-repo changes; schema-plus-code changes that can't deploy atomically.

### 14. Verify the kill-switch and its safe default

- **How it works:** Prefer a cheap, reversible config switch (defaulting to the safe / no-op state) over relying on code rollback, and *verify the switch actually works* — that flipping it changes behavior and that the default is genuinely safe — before depending on it as your way back.
- **Objective:** Guarantee a fast, tested path back that doesn't require a redeploy.
- **When most valuable:** Risky rollouts; behavior changes you may need to disable quickly under load.

### 15. Final confidence check before a production merge

- **How it works:** Treat the production merge/deploy as a hard gate demanding one last independent confidence check. Distrust a premature "safe to merge with confidence" — ask explicitly whether you are truly certain *because this is production*, and what specifically grounds that certainty.
- **Objective:** Insert one deliberate pause where over-confidence is most expensive.
- **When most valuable:** The moment before any irreversible production action.

---

## Part D — Post-deploy Production Verification

*The change shipped. Now confirm reality matches intent — with live evidence.*

### 16. Confirm with direct runtime evidence

- **How it works:** After shipping, confirm the change with live evidence from the running system — queries against production data, metrics, error rates, logs, and captured real payloads — not by re-reading the code you already merged. Capture the *actual* payload/artifact rather than inferring what it probably is.
- **Objective:** Prove the change does what was intended where it actually runs.
- **When most valuable:** After every non-trivial production change; especially data and behavior changes.

### 17. Annotate every verification with its expected value

- **How it works:** The mechanical practice behind the Master Principle: write each verification query/check with its expected result inline ("→ should return 0 / should now be ENUM_X / error rate < baseline"), and pre-classify which observations are *not* problems so noise doesn't trigger false alarms.
- **Objective:** Make any deviation an immediate signal instead of a number you interpret (and rationalize) after the fact.
- **When most valuable:** All post-deploy verification; any monitoring you'll re-run repeatedly.

### 18. One change at a time, with named watch-fors

- **How it works:** Ship one PR/stack, then verify both that the intended effect happened *and* that no unintended side effect did — naming the specific bad behaviors to watch for in advance — before advancing to the next change.
- **Objective:** Keep cause and effect attributable; isolate which change moved which signal.
- **When most valuable:** Sequenced rollouts, multi-step migrations, anything where a later change would mask an earlier regression.

### 19. Re-run over time; treat absence of signal as a signal

- **How it works:** Define monitoring you can re-run repeatably over hours/days, built around expected state transitions at known boundaries, and re-check it as more volume accumulates — a clean result at low volume isn't proof. Treat an *absence* of expected traffic/events as itself worth investigating, not as silence to ignore.
- **Objective:** Catch the defect that only appears at volume, and the failure that hides as "nothing happened."
- **When most valuable:** Low-initial-traffic features; event-driven flows; anything verified shortly after deploy.

---

## Part E — Operational Data-Mutation Verification

*Changing production data is the most irreversible act; verify at every step.*

### 20. Transactional, audited, reversible mutation protocol

- **How it works:** Wrap a production data change in an explicit transaction; lock the target rows first (against concurrent background writes); write a before/after audit record with rationale *before* mutating; run post-state verification against stated expected values; and withhold the final commit pending a last review. Keep a bounded path back.
- **Objective:** Make a high-stakes mutation observable, reversible, and provably correct before it becomes permanent.
- **When most valuable:** Any direct write/update/delete to production data outside the normal application path.

### 21. Quantify real usage and cross-check truth before mutating

- **How it works:** Before deleting or repurposing data, quantify its real usage from authoritative sources — delete only what is *provably* unused. Cross-check the target against the system of record before mutating, so you don't act on a stale or derived copy.
- **Objective:** Ensure "unused" and "safe to change" are established facts, not assumptions.
- **When most valuable:** Cleanups, deletions, field repurposing, source-of-truth migrations.

---

## Appendix — Composition Patterns

*How to chain verification strategies together.*

- **Expectation-first:** Pair every check with its pre-stated expected result (the Master Principle; mechanically, strategy 17). A check with no expectation can't fail loudly.
- **Reproduce → fix → re-confirm:** Capture the failing baseline as evidence before the change (10), so the after-state proves causation rather than coincidence.
- **Prove → re-prove:** Reach a conclusion, then re-verify it independently (5) before acting. The second pass is where the rationalized error dies.
- **Promotion ladder:** Run the cheapest faithful verification at each environment gate (Part C); never skip a gate because the next one "will catch it."
- **Calibrate depth to irreversibility:** A reversible config tweak needs a dry-run; a production data deletion needs the full mutation protocol (20–21) plus post-deploy confirmation (Part D).
- **Capture, don't infer:** When the real payload/metric is obtainable, capture it (16); inference is a hypothesis, not verification.
- **No silent skipping:** If a check couldn't be run faithfully (sandbox limit, no pre-prod), say so and name who/what is the authority for it (6) — never let an unrun check read as a passed one.
