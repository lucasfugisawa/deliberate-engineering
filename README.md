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

- **`review-strategy-selector` skill** — classifies your change by risk, reversibility, requirement clarity, and size, then selects the appropriate review lenses from the catalog
- **51-strategy review catalog** — read on demand; organized into five groups covering process/meta-review (11 strategies), verification/evidence (7), failure & contradiction reasoning (6), engineering-quality lenses (12), and reviews beyond back-end (15)
- **`/deliberate-engineering:review` command** — invoke the selector for the current change

The selector analyzes whether your change touches money, data, security, or production behavior; whether it's reversible; whether requirements are unambiguous; and its blast radius. It uses these axes — not line count — to pick the right depth and lenses.

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

## Roadmap

**Current (v0.1):** The spine is review — classify the change, apply the right lenses.

**Future catalogs:**

- **Ceremony router** — interception at the start: how much process does this task call for?
- **Planning** — matching planning tactics to problem structure
- **Debugging** — systematic fault isolation and hypothesis testing
- **Design** — architecture review and simplification
- **Verification / dynamic testing** — interception *after* the system is runnable, distinct from static review: pentest/DAST, load & stress, chaos, fuzzing, and end-to-end checks against a real deploy
- **Environment/setup audit** — sanity checks for local dev, CI, and production configs

These catalogs share the same architecture: classify, select from a curated menu, compose, close with fresh eyes.

## License

MIT
