# deliberate-engineering

> Don't go agentic as much as you can. Go agentic only as much as you should.

*Engineering discipline for AI-assisted development. Less vibe coding, more deliberate craft.*

## What it is

`deliberate-engineering` is a thin layer of deliberate judgment on top of a workflow engine. The thesis: interception + curated tactic catalogs + context-aware selection. It does not replace your workflow; it sharpens each step by classifying the change you're making and selecting the right review lenses for that specific case.

## Install

```bash
/plugin marketplace add lucasfugisawa/deliberate-engineering
```

Then enable it via `/plugin`. Note: this plugin requires `superpowers` (the discipline engine it orchestrates).

## What's inside (v0.1)

The initial release includes:

- **`deliberate-engineering-rules` skill** — the standing rules of deliberate practice, applied across every phase of engineering work: keep the human's hand on irreversible and outward-facing actions, stay read-only on systems you don't own, verify claims against primary evidence before endorsing, recommend with a reasoned pick rather than a bare menu, keep comments load-bearing, and checkpoint durable state before compacting context. Scoped to software work; it stays quiet on research, prose, and ad-hoc analysis.
- **`review-strategy-selector` skill** — classifies your change by risk, reversibility, requirement clarity, and size, then selects the appropriate review lenses from the catalog
- **53-strategy review catalog** — read on demand; organized into five groups covering process/meta-review (13 strategies), verification/evidence (7), failure & contradiction reasoning (6), engineering-quality lenses (12), and reviews beyond back-end (15)
- **`verification-strategy-selector` skill** — for establishing that something is *actually* true, with evidence from running systems — not just plausible on paper. Classifies what you're verifying and how irreversible being wrong is, then selects the right strategies. Distinct from review: review asks "does this look correct?"; verification asks "is it correct, and what's my evidence?"
- **21-strategy verification catalog** — read on demand; organized into five groups: evidence & ground truth (5), local & pre-merge verification (5), staged promotion & rollout (5), post-deploy production verification (4), and operational data-mutation verification (2)
- **`planning-strategy-selector` skill** — for *before* code exists: deciding what work is worth doing and how much process it calls for. Classifies the work by clarity, risk, reversibility, and reach, then selects planning lenses: scope to the real requirement (decide what *not* to build), ground the plan in the actual codebase, calibrate ceremony to risk, decompose and sequence safely, and capture the plan well. Judgment applied to planning — it delegates the *how-to-plan* discipline to your workflow engine.
- **16-strategy planning catalog** — read on demand; organized into five groups: scope / anti-over-engineering (4), ground the plan in reality (4), calibrate ceremony to risk (2), slice & sequence (3), and capture the plan (3)
- **`debug-operate-strategy-selector` skill** — for when a *live system* behaves unexpectedly and you must diagnose under uncertainty and respond. Classifies whether you even hold a reliable expectation (if not, this is discovery, not verification), how trustworthy the evidence is, and how reversible the response is — then selects the right lenses. Distinct from verification: verification confirms an expectation you already hold; this is discovery under failure, and it delegates the debugging *method* to your workflow engine.
- **16-strategy Debug/Operate catalog** — read on demand; organized into five groups: trust the evidence (3), diagnose under uncertainty (2), respond under pressure (3), keep the signal healthy (5), and learn from the failure (3)
- **`/deliberate-engineering:plan`, `:review`, `:verify`, and `:debug` commands** — invoke the selectors for the current work

The selectors use risk, reversibility, clarity, and reach — not line count — to pick the right depth and lenses, one mental model across the lifecycle. Planning decides what to build; review reasons about the artifact; verification confronts reality with a run, a query, a production metric, or a captured payload, stating each expected result before observing the actual one; and debug/operate takes over when a live system misbehaves — diagnosing under uncertainty and responding when no reliable expectation holds.

### Make the rules always-on (optional)

Skills load when the model judges them relevant to the task. If you want the
deliberate-engineering rules enforced on *every* engineering session — the way
the author runs them — add a short block to your personal `~/.claude/CLAUDE.md`:

```markdown
## Deliberate-engineering (always-on for engineering work)
On software-engineering tasks — writing, reviewing, debugging, planning,
migrating, shipping, or operating code with real consumers, risk, or
irreversibility — apply the deliberate-engineering-rules skill, not just on
description match. Skip it for research, prose, ad-hoc analysis, disposable
no-consumer scripting, and non-technical work.
```

This is your machine's choice, never a requirement of the plugin. The rules
themselves live entirely in the skill above; this block only changes *when* they
fire on your machine.

## Works alongside

`deliberate-engineering` is a thin layer of judgment, not a workflow engine. It is designed to coexist with the tools you already use:

- **Requires** [`superpowers`](https://github.com/obra/superpowers) as its discipline engine. `deliberate-engineering` orchestrates it; it does not replace it.
- **Complements** review tooling such as `pr-review-toolkit` — `deliberate-engineering` decides *which* review tactics a change calls for, and can invoke those agents as tactics.
- **Takes precedence, doesn't evict.** If you also run other workflow plugins (e.g. `feature-dev`), you don't need to remove anything. When multiple engines are available, `deliberate-engineering` decides which to invoke; on ambiguity it prefers the deliberate flow. A leaner environment is your choice, never a requirement.

## Prior art & influences

This plugin stands on the shoulders of:

- **[superpowers](https://github.com/obra/superpowers)** (Jesse Vincent) — the required discipline engine that makes deliberate interception possible
- **[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)** and **[mattpocock/skills](https://github.com/mattpocock/skills)** — pioneering work in curated skill catalogs for AI-assisted development
- **General engineering practice** — review strategies, threat modeling, FMEA, and deliberate practice

We study, we don't copy. Where design converges with existing work, we give credit. The catalog structure and composition patterns are original synthesis; the individual lenses draw from established engineering discipline.

## License

MIT
