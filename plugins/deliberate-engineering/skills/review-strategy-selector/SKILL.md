---
name: review-strategy-selector
description: "Use after any baseline review, or when reviewing a change, to deliberately select the right review lenses for THIS change instead of running a generic pass. The artifact need not be code: it also reviews a spec, a design or an architecture, and the catalog reaches past back-end code into accessibility, infrastructure, CI/CD, privacy and data protection, cost, disaster recovery, internationalization and experiments. Classifies by risk, reversibility, requirement clarity, and reach, then applies matching strategies from the catalog. Less vibe coding, more deliberate craft. On a multi-phase or multi-session work unit it writes a short live note through `deliberate-engineering-state`, which lands in the repository under `.deliberate/state/` (and may add that path to `.gitignore`) or under `~/.claude/` when it cannot."
---

# Review Strategy Selector

The deliberate layer of review. A baseline pass (catalog strategy 1) finds the obvious. This skill decides *which additional lenses THIS change actually calls for*, and applies them, so review is tuned to the change, not a generic checklist run on autopilot.

The reference for every strategy cited below is `catalog.md` in this directory (five groups of strategies + composition patterns). Read **only** the sections you select: progressive disclosure, not the whole file.

## Review vs. verification vs. debug/operate: stay on the right side of the line

- **Review** (this skill): reasons about a static artifact (a diff, a spec, a design) and judges whether it *looks* correct.
- **Verification** (`verification-strategy-selector`): establishes whether it *is* correct, with evidence from the running world. The moment a finding turns on a fact about reality (a number, an actual production behavior, the real schema), it stops being reviewable: hand it there instead of settling it by reading.
- **Debug/operate** (`debug-operate-strategy-selector`): owns a live system misbehaving with no reliable expectation yet. If a review turns into chasing a live break, you have left this skill.

They compose in that order: review finds candidates, verification confirms the ones that need reality. Reviewing is not verifying, and a lens that concludes "this reads correctly" has not established that it *is* correct.

## When to use

- After a baseline review (strategy 1) has mapped the terrain.
- When asked to review a change, PR, diff, spec, or design.
- Whenever you are both author and reviewer and need to break your own bias.

## When NOT to pile on

This is calibration, not always-more. For a **trivial-and-safe** change (typo, comment, log string, isolated pure function with tests, no money/data/security/production exposure) you may deliberately choose MINIMAL ceremony. When you do, **say so explicitly**: state that you classified it as trivial-and-safe and chose a light pass. Silence is not calibration: a stated decision is.

## Scope and re-invocation

Resolve what to review from the **world**, never from the conversation. Scope is a diff range, a branch, an explicit PR/file list, or the working-tree change: something re-derivable without trusting memory of "what we just discussed." If `$ARGUMENTS` is empty and the working tree is clean, do not guess: ask one question with an embedded recommendation (Rule 4), e.g. "I'd review the diff of `<branch>` against `origin/main`. Confirm?". On re-invocation in the same session, this is also the integrity gate (Rule 3): re-execute from the resolved scope in fresh context; a recalled scope ("the PRs I just reviewed") is itself a memory artifact, not a re-derived target.

## Step 1: Classify the change on four axes

Assess each axis. These, not line count, set the depth.

1. **Risk**: Does it touch money, customer/PII data, security/auth, or production behavior? Could a defect cause loss, leak, or outage?
2. **Reversibility**: Migrations, backfills, destructive or in-place writes, schema changes? Is there a bounded path back to the prior state?
3. **Requirement clarity**: Is the intent unambiguous, or are you inferring what "correct" means? Ambiguity is itself a risk.
4. **Reach**. Blast radius: how many call sites, services, or consumers does the change touch? (Not the diff size, the reach.)

**The ruler is RISK AND UNCERTAINTY, not line count.** A one-line change to a fee calculation or a `DELETE` predicate is high-depth; a 600-line addition of an isolated, well-tested helper is not. This is the plugin's one shared ruler stated in review's terms: depth follows the cost of being wrong, never the size of the change.

## Step 2: Map to a ceremony band

- **Trivial-and-safe** → minimal: baseline (1) plus a 34 *scan* (did this diff introduce a comment that shouldn't exist, or a reference the reader can't resolve?) and a stated rationale for stopping (see "When NOT to pile on"). A solo in-context pass is fine here, **but the reuse-vs-recompute declaration (Rule 3) is mandatory**: if this re-runs an earlier pass, say whether you recomputed or reused, and why.
- **Standard** → a small set of targeted lenses (typically 2–4) for the non-trivial axes; **dispatch each substantive lens to a fresh-context subagent** as the default unit of work so the lens recomputes rather than recalls, and each returns its evidence artifact (Task: see "Compose the passes"). Close with fresh eyes (3).
- **Risky / irreversible / ambiguous / money-or-data** → full adversarial depth in fresh-context fan-out: per-PR as the default unit, **per-(PR × lens) for the critical lenses (25, 28, 26)**; adversarial majority-refute (2, 9) on top; where the design space is wide and being wrong is expensive, run 8 judge panel (several independent attempts, scored, the best synthesized); close with a fresh-eyes pass (3) run as a *literally separate* fresh-context agent, not an in-context re-read.

## Step 3: Select lenses from the catalog

Open the catalog **groups** matching your non-trivial axes and pick lenses. Read only those sections.

- **Always, first (Requirement)** → 25 functional correctness / requirement conformance: does it do what was actually asked? The most important lens. Pair it with 11 change-size / reviewability before going deep: a change too large to review well hides defects from every lens that follows.
- **Any diff that adds or edits source (not keyed to an axis)** → 34 readability/maintainability: comment necessity and concision, plus the reader-resolvability check (Rule 9) on every comment the diff introduces. This defect class does not correlate with risk; it rides along in trivial changes as readily as in critical ones, which is why it is routed here rather than under an axis. Once the change is correct and before the design hardens, add 35 simplification / YAGNI.
- **Money / data / production (Risk)** → 26 security, 27 performance, 28 data integrity, 30 observability, and 42 privacy / compliance wherever personal or financial data is collected, stored, moved or newly logged; add 2 adversarial, 20 pre-mortem.
- **Migrations / backfills / destructive (Reversibility)** → 23 concurrency, 24 reversibility/rollback, 28 data integrity, 31 operability/rollout, 16 coverage analysis.
- **Ambiguous intent (Requirement clarity)** → 15 assumption/invariant audit, 32 cross-document consistency, 13 validation against real data, 50 spec self-review.
- **Implementation reviewed against a spec/intent** → 52 spec-conformance audit (alignment-not-correctness, drift taxonomy, discovery-only), with 25.
- **Wide blast radius (Reach)** → 55 blast-radius/change-impact (map every caller/consumer the change reaches), 29 contract/API, 32 cross-service consistency, 18 test-quality.
- **External dependencies and error paths** → 21 silent-failure hunting, 22 error-handling adequacy; and whenever a library is added or bumped, 36 dependency / supply-chain review (provenance, transitive reach, build security).
- **Parsing, aggregation, time windows, pagination, or semantics a reading cannot settle (NULL handling, non-guaranteed ordering, idempotence)** → 17 boundary / edge-case, and 12 empirical validation: execute it rather than reason about it.
- **Introduces or reshapes a type or a domain model** → 33 type-design / invariant-expression: can the type make the illegal state unrepresentable?
- **More than one branch, worktree, or repository in play** → 14 source-of-truth verification: confirm you are reading the canonical copy before judging it.
- **The artifact contradicts an established norm, or a rule carries temporal or contextual nuance** → 19 apparent-contradiction reconciliation: reconcile it before calling either side wrong.
- **A design proposal, a significant refactor, or a change that moves a boundary, introduces a component, or shifts who owns what** → 51 architecture critic (adversarial).
- **Frontend / mobile / infra / data / experiments** → the matching Part-E group; open only the relevant subsection.

**Worked example (change writes production data via a backfill):** Non-trivial on Risk + Reversibility + Reach. Selected lenses: **25** (functional correctness: does it backfill what the requirement meant?), **23** (concurrency: backfill contends with live writes), **24** (reversibility: is there a bounded way back?), **28** (data integrity: invariants/transactions hold?), **2** (adversarial: try to break it), closed with **3** (fresh eyes). Skipped frontend/i18n groups, logged as not applicable.

**Entering here directly.** These lenses are the same whether you arrived through `/deliberate-engineering:start` or called this phase yourself, but four things the router would have carried do not come with a direct call, so carry them here. The nine standing rules in `deliberate-engineering-rules` hold regardless, including the human gate on anything irreversible or outward-facing. Write your place at each checkpoint through `deliberate-engineering-state` (Rule 6), so a compaction or a new session resumes from what happened rather than from recall. Re-classify out loud if the work turns out heavier or lighter than it looked, and say what moved. And when the next thing you produce is a communication rather than code, consult `communication-collaboration-selector` before writing it.

**Operator overrides.** Before applying the selected lenses, consult `deliberate-engineering-overrides`: honor any override on a lens you selected (disable / modify), and ask it for any operator-authored `add:` entry for this catalog, which carries no shipped number and so is invisible to a lookup keyed on your selection. Declare every deviation in the Output.

**Each substantive lens emits an evidence artifact, and the artifact IS its completion criterion.** A lens has not run until it has produced, from THIS pass, the concrete trace of what it examined:

- **25 functional correctness** → the requirement clause quoted from its source + the `file:line` implementing each clause + a per-clause verdict.
- **28 data integrity** → the invariant/transaction checked + the `file:line` it lives at + the concrete case that would violate it.
- **26 security** → the attack surface examined + the `file:line` + the check applied and its result.
- Other selected lenses follow the same shape: name what was examined, cite where (`file:line`, command + output), and state the verdict.

This is what makes a recalled review visibly incomplete: reused conclusions carry no fresh artifact, so a pass that only reformats prior findings produces empty artifacts and fails its own completion criterion. It is also what exposes overclaimed exhaustion: an artifact that lists three opened files cannot be presented as a whole-file audit of thirty.

## Step 4: Compose the passes

Apply the composition patterns from the catalog's Appendix:

- **Rotate the lens each pass**: one strategy per pass, never the same angle twice.
- **Find → verify**: find candidates broadly, then verify each adversarially (9 majority-refute) before acting on it. For unknown-size audits, loop until dry (6). ("Verify" here is lens 9's refutation vote *inside* review; confirming a candidate against reality is the `verification-strategy-selector`'s job, not this pattern's.)
- **Self-review your own fixes** (4): after editing, review what the fix may have broken, and first whether the fix reproduces the defect class it was fixing.
- **Check coverage, then decide when to stop (10, 54)**: before the closing pass, run the completeness critic (10: what is missing, a modality not exercised, a claim not verified, a source not read?) and send what it finds into another round; then apply the stopping criterion (54: which classes of defect went unexamined, and is that judgment stated rather than reached by fatigue?), which earns its full weight on an exhaustive audit or a high-stakes change.
- **CLOSE with a fresh-eyes pass (3) in a separate context**: the final pass must be independent of the edit history AND of the prior conclusions. In-context re-reading inherits what you already concluded, so it confirms rather than re-sees; dispatch it as a fresh-context agent (or defer to a new session). Always.
- **Never silently truncate**: if you limited coverage (sampled, capped, skipped a group), **log what you deliberately skipped and why.** Truncating silently reads as "covered everything," which is a lie of omission.

## Step 5: Coexistence and precedence

When other reviewers or engines are present (e.g. a PR-review toolkit, a feature-development flow), **THIS skill decides which to invoke** for the change at hand. It may invoke their agents as *tactics*: e.g. dispatch a silent-failure hunter, a type-design analyzer, or a test analyzer to execute a selected lens.

This skill **never requires removing or disabling** any other reviewer. It orchestrates; it does not displace. If a present engine already covers a selected lens well, delegate to it and note the delegation rather than duplicating the pass.

## Output

Report, briefly: the classification (4 axes), the ceremony band, the lenses selected (by number) and why, anything deliberately skipped and why, and the findings: each tagged blocking vs. optional (53), and each tied to the concrete evidence produced in this pass (the `file:line` actually opened, the command run and its output, the requirement clause quoted from source). A finding with no fresh-pass evidence is incomplete, not done: recompute it, don't relay it. End with the fresh-eyes close.
