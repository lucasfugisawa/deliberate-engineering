---
name: verification-strategy-selector
description: "Use when you need to establish that something is actually true in reality — not just plausible on paper: verifying a claim, number, or assumption against primary evidence; getting a change ready to merge; promoting across environments; confirming production behavior after a deploy; or mutating production data safely. Classifies what's being verified and how irreversible being wrong is, then selects the right strategies from the catalog. Distinct from code review: review asks 'does this look correct?', verification asks 'is it correct, and what's my evidence?'"
---

# Verification Strategy Selector

The deliberate layer of verification. Where review reasons about a static artifact, this skill confronts a claim with **reality** — a run, a query, a production metric, a captured payload — and decides *which* evidence THIS claim actually needs before you trust or ship it.

The reference for every strategy cited below is `catalog.md` in this directory (five groups of strategies + composition patterns). Read **only** the sections you select — progressive disclosure, not the whole file.

## Review vs. verification — stay on the right side of the line

- **Review** (the `review-strategy-selector` skill): examines a diff, spec, or design and judges whether it *looks* correct. Reasoning about the artifact.
- **Verification** (this skill): establishes whether it *is* correct, with evidence from the running world. Confronting reality.

If the task is "read this and tell me if it's right," that's review. If it's "prove it's right" / "confirm it actually did X in production" / "is this number real," that's verification. They compose — review finds candidates; verification confirms them — but don't run a verification plan when a read would do, and don't call a code-read "verified" when reality was never consulted.

One shared concept, split cleanly: bias about whether the artifact *reads* correctly belongs to review (its fresh-eyes and adversarial lenses); bias about whether your *evidence/conclusion* is real belongs here (strategy 3).

## When a read suffices — don't over-verify

Verification has a cost and a symmetric failure mode to over-review: running production queries to check a doc typo is the same misplaced ceremony, inverted. When the claim is **cheap and reversible** and a direct read of current source or data settles it, do that and stop — and **say so**: state that you judged it low-stakes and confirmed by reading rather than by a full evidence pass. Reserve the staged/post-deploy/mutation machinery for claims whose wrong "it's fine" is expensive to undo.

## When to use

- A claim, number, or assumption needs to be established as fact before it feeds a decision or a review comment.
- Before merging or promoting a change across an environment boundary.
- After a deploy, to confirm production behavior matches intent.
- Before or during an operational data mutation.

## Step 1 — Classify what you're verifying

1. **Evidence type** — Is this an *epistemic* claim (a number, a behavior assertion, an assumption about the data/schema)? A *pre-merge* readiness question? A *post-deploy* reality check? An *operational mutation*? Each maps to a catalog part (A / B / C / D / E).
2. **Irreversibility of being wrong** — If this verification gives a false "it's fine," how hard is the consequence to undo? A stale doc is cheap; a wrong production deletion is not. **This sets the depth.**
3. **Environment reach** — Local-only? Crosses into pre-prod/prod? Spans multiple services or datastores?
4. **Your stake** — Do you *want* a particular answer? If so, bias-control (strategy 3) is mandatory, not optional.

**The ruler is the cost of a wrong "it's fine," not the size of the change.**

## Step 2 — Map to a depth band

The two classifications are **orthogonal**: *evidence type* (Step 1, axis 1) picks **which catalog Part(s)** apply; *irreversibility* (Step 1, axis 2) picks **how deep within them** you go. Pick the Part by what you're verifying, then set the depth by the cost of being wrong.

- **Cheap & reversible** (a local claim, a tweak you can undo trivially) → minimal: establish the fact from the live source/data (1, 2, 4), state the expectation, stop. Say you chose a light pass (see "When a read suffices").
- **Pre-merge / standard** → the relevant Part-B local gates (6, 7), reproduce-then-confirm for a fix (10), plus second-pass re-verification (5) before you endorse.
- **Crosses into production / irreversible / operates on real data** → full depth: staged gates (Part C), post-deploy confirmation with annotated expectations (Part D), and — for data mutations — the mutation protocol (Part E). Always close with the second pass (5) and a final confidence check (15).

## Step 3 — Select strategies from the catalog

Open only the parts matching your classification:

- **Verifying a claim / number / assumption** (Part A) → 1 live-canonical-source, 2 no-guessing provenance, 4 real-data-and-schema; add 3 name-the-refuting-observation if you have a stake; close with 5 second-pass.
- **Getting a change ready to merge** (Part B) → 6 calibrate-local-trust, 7 mirror-CI aggregate check, 8 dry-run (if it touches data), 9 validation-methodology (if it affects others/performance), 10 reproduce-then-confirm (if it's a fix).
- **Promoting across environments** (Part C) → 11 promotion gates, 12 red-CI-is-a-stop / flaky-vs-real, 13 deploy-ordering, 14 kill-switch, 15 final-confidence-check.
- **Confirming after deploy** (Part D) → 16 runtime evidence, 17 annotate-expected-values, 18 one-change-at-a-time + named watch-fors, 19 re-run-over-time / absence-is-signal.
- **Mutating production data** (Part E) → 20 transactional-audited-reversible protocol, 21 quantify-usage + cross-check-truth; always pair with Part D confirmation.

**Worked example — confirming a shipped backfill did what was intended:** Post-deploy + operated on real data; high irreversibility. Selected: **16** (query production for the actual post-state, capture real rows), **17** (each query annotated with its expected result — "should now be 0 remaining"), **18** (verify the intended rows changed AND nothing unrelated did, watching for named side effects), **19** (re-run as volume accumulates; absence of expected updates is itself a flag), and because it mutated data, confirm the **20** audit trail reconciles. Closed with **5** (independent second pass). Skipped Part B/C — already merged and promoted; logged as not applicable.

**Operator overrides.** Before applying the selected lenses, consult `deliberate-engineering-overrides`: if any selected lens has an operator override (disable / modify / add), honor it and declare the deviation in the Output.

## Step 4 — Compose the verification

Apply the catalog's Appendix patterns:

- **Re-execute on re-invocation (Rule 3)** — resolve scope from a world-derived target, and recompute in fresh context rather than relaying a prior in-session conclusion.
- **Expectation-first** — every check carries its expected result *before* you observe the actual one. A check with no stated expectation can't fail loudly.
- **Prove → re-prove** — reach a conclusion, then re-verify it independently (5) before acting. The second pass is where the rationalized error dies.
- **Calibrate depth to irreversibility** — match the protocol to the cost of being wrong, not to the diff size.
- **Capture, don't infer** — when the real payload/metric is obtainable, capture it (15); inference is a hypothesis, not verification.
- **No silent skipping** — if a check couldn't be run faithfully (sandbox limit, no pre-prod), **say so and name the authority for it** (6). An unrun check must never read as a passed one.

## Step 5 — Coexistence and precedence

When other tooling is present (CI, a review toolkit, a test runner), **THIS skill decides what evidence the claim needs** and may invoke those tools as *tactics* — e.g. trust CI as the authority for DB-backed tests (6), or dispatch a test analyzer to judge a suite. It never requires removing any other tool; it orchestrates the evidence-gathering and delegates where a present tool is the right authority, noting the delegation.

When the **`review-strategy-selector`** is co-active on the same task, they compose in order: **review runs first** to read the artifact and surface candidates; **verification confirms** the ones that need reality. Don't run a verification plan on something a read would settle, and don't report a candidate as confirmed until verification has produced the evidence.

## Output

Report, briefly: the classification (evidence type, irreversibility, environment, stake), the depth band, the strategies selected (by number) and why, anything deliberately skipped and why, and the verification result — each finding tied to its concrete evidence (the query, the run, the captured payload), with expectations stated before actuals.
