---
name: review-strategy-selector
description: "Use after any baseline code review, or when reviewing a change, to deliberately select the right review lenses for THIS change instead of running a generic pass. Classifies by risk, reversibility, requirement clarity, and size, then applies matching strategies from the catalog. Less vibe coding, more deliberate craft."
---

# Review Strategy Selector

The deliberate layer of review. A baseline pass (catalog strategy 1) finds the obvious. This skill decides *which additional lenses THIS change actually calls for* — and applies them — so review is tuned to the change, not a generic checklist run on autopilot.

The reference for every strategy cited below is `catalog.md` in this directory (53 strategies in five groups + composition patterns). Read **only** the sections you select — progressive disclosure, not the whole file.

## When to use

- After a baseline review (strategy 1) has mapped the terrain.
- When asked to review a change, PR, diff, spec, or design.
- Whenever you are both author and reviewer and need to break your own bias.

## When NOT to pile on

This is calibration, not always-more. For a **trivial-and-safe** change (typo, comment, log string, isolated pure function with tests, no money/data/security/production exposure) you may deliberately choose MINIMAL ceremony. When you do, **say so explicitly**: state that you classified it as trivial-and-safe and chose a light pass. Silence is not calibration — a stated decision is.

## Step 1 — Classify the change on four axes

Assess each axis. These, not line count, set the depth.

1. **Risk** — Does it touch money, customer/PII data, security/auth, or production behavior? Could a defect cause loss, leak, or outage?
2. **Reversibility** — Migrations, backfills, destructive or in-place writes, schema changes? Is there a bounded path back to the prior state?
3. **Requirement clarity** — Is the intent unambiguous, or are you inferring what "correct" means? Ambiguity is itself a risk.
4. **Size / scope** — Blast radius: how many call sites, services, or consumers does it reach? (Not the diff size — the reach.)

**The ruler is RISK AND UNCERTAINTY, not line count.** A one-line change to a fee calculation or a `DELETE` predicate is high-depth; a 600-line addition of an isolated, well-tested helper is not.

## Step 2 — Map to a depth band

- **Trivial-and-safe** → minimal: baseline (1) only, plus a stated rationale for stopping. See "When NOT to pile on."
- **Standard** → a small set of targeted lenses (typically 2–4) chosen for the axes that scored non-trivial, closed with fresh eyes (3).
- **Risky / irreversible / ambiguous / money-or-data** → full adversarial depth: a broad finder set, adversarial verification (2, 9), and the domain-specific lenses below.

## Step 3 — Select lenses from the catalog

Open the catalog **groups** matching your non-trivial axes and pick lenses. Read only those sections.

- **Always, first (Requirement)** → 25 functional correctness / requirement conformance — does it do what was actually asked? The most important lens.
- **Money / data / production (Risk)** → 26 security, 27 performance, 28 data integrity, 30 observability; add 2 adversarial, 20 pre-mortem.
- **Migrations / backfills / destructive (Reversibility)** → 23 concurrency, 24 reversibility/rollback, 28 data integrity, 31 operability/rollout, 16 coverage analysis.
- **Ambiguous intent (Requirement clarity)** → 15 assumption/invariant audit, 32 cross-document consistency, 13 validation against real data, 50 spec self-review.
- **Implementation reviewed against a spec/intent** → 52 spec-conformance audit (alignment-not-correctness, drift taxonomy, discovery-only), with 25.
- **Wide blast radius (Size/scope)** → 29 contract/API, 32 cross-service consistency, 18 test-quality, 34 readability.
- **External-dependency / error paths** → 21 silent-failure hunting, 22 error-handling adequacy.
- **Frontend / mobile / infra / data / experiments** → the matching Part-D / Part-E group; open only the relevant subsection.

**Worked example — change writes production data via a backfill:** Non-trivial on Risk + Reversibility + Size. Selected lenses: **25** (functional correctness — does it backfill what the requirement meant?), **23** (concurrency — backfill contends with live writes), **24** (reversibility — is there a bounded way back?), **28** (data integrity — invariants/transactions hold?), **2** (adversarial — try to break it), closed with **3** (fresh eyes). Skipped frontend/i18n groups — logged as not applicable.

**Operator overrides.** Before applying the selected lenses, consult `deliberate-engineering-overrides`: if any selected lens has an operator override (disable / modify / add), honor it and declare the deviation in the Output.

## Step 4 — Compose the passes

Apply the composition patterns from the catalog's Appendix:

- **Rotate the lens each pass** — one strategy per pass, never the same angle twice.
- **Find → verify** — find candidates broadly, then verify each adversarially (9 majority-refute) before acting on it. For unknown-size audits, loop until dry (6).
- **Self-review your own fixes** (4) — after editing, review what the fix may have broken.
- **CLOSE with a fresh-eyes pass (3)** — the final pass must be independent of the edit history. Always.
- **Never silently truncate** — if you limited coverage (sampled, capped, skipped a group), **log what you deliberately skipped and why.** Truncating silently reads as "covered everything," which is a lie of omission.

## Step 5 — Coexistence and precedence

When other reviewers or engines are present (e.g. a PR-review toolkit, a feature-development flow), **THIS skill decides which to invoke** for the change at hand. It may invoke their agents as *tactics* — e.g. dispatch a silent-failure hunter, a type-design analyzer, or a test analyzer to execute a selected lens.

This skill **never requires removing or disabling** any other reviewer. It orchestrates; it does not displace. If a present engine already covers a selected lens well, delegate to it and note the delegation rather than duplicating the pass.

## Output

Report, briefly: the classification (4 axes), the depth band, the lenses selected (by number) and why, anything deliberately skipped and why, and the findings — each tagged blocking vs. optional (53) — ending with the fresh-eyes close.
