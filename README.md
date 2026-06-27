# deliberate-engineering

> Don't go agentic as much as you can. Go agentic only as much as you should.

*Engineering discipline for AI-assisted development. Less vibe coding, more deliberate craft.*

## Why this exists

I build software with coding agents every day, and the same failure kept recurring: the agent is *capable* of acting, so it acts — at full autonomy, with uniform effort, on every task. A one-line change to a money calculation gets the same shrug as a typo fix. "Done" gets reported before anything was actually checked against reality. The result reads productive and is quietly wrong.

I built `deliberate-engineering` to put judgment back in front of capability. It is the layer I wanted: one that decides *how much* ceremony a given change has earned, *which* lenses it actually calls for, and *whether* the work is really done — before the agent charges ahead.

It is a **judgment layer, not another how-to engine.** Three problems it targets:

- **Over-agentic by default** → the agent calibrates autonomy and depth to risk, reversibility, and blast radius, and stops at a human gate for anything irreversible or outward-facing.
- **One-size-fits-all review** → it classifies the change first, then selects the review/verification/planning lenses that fit *this* case, instead of running a generic pass on autopilot.
- **"Looks correct" mistaken for "is correct"** → verification confronts reality (a run, a query, a production metric) and states the expected result *before* observing the actual one.

## What it is

`deliberate-engineering` is a thin layer of deliberate judgment on top of a workflow engine. The thesis: **interception + curated tactic catalogs + context-aware selection.** It does not replace your workflow; it sharpens each step by classifying the work in front of you and selecting the right tactics for that specific case.

One mental model runs across the whole lifecycle — **risk, reversibility, requirement clarity, and reach decide the depth, not line count:**

| Phase | Selector | The question it answers |
|---|---|---|
| **Plan** | `planning-strategy-selector` | What's worth building, and how much process does it deserve? |
| **Review** | `review-strategy-selector` | Which lenses does *this* change actually call for? |
| **Verify** | `verification-strategy-selector` | Is it true against reality — and what's my evidence? |
| **Debug/Operate** | `debug-operate-strategy-selector` | A live system is misbehaving and I have no reliable expectation — now what? |

Planning decides what to build; review reasons about the artifact; verification confronts reality; and debug/operate takes over when a live system misbehaves and no reliable expectation holds.

## Requirements & compatibility

- **Requires [`superpowers`](https://github.com/obra/superpowers)** (Jesse Vincent) as its discipline engine. `deliberate-engineering` orchestrates it — it owns the *judgment*, and delegates the *method* (TDD, systematic debugging, plan execution) to superpowers. It does not replace it.
- **Ships as a Claude Code plugin.** The selectors and rules are Claude Code skills/commands. It does not claim to run on other agents or IDEs — the honest scope is Claude Code today.
- **Complements** review tooling such as `pr-review-toolkit`: it decides *which* review tactics a change calls for, and can invoke those agents as tactics.
- **Takes precedence, doesn't evict.** If you also run other workflow plugins (e.g. `feature-dev`), you don't need to remove anything. When multiple engines are available, `deliberate-engineering` decides which to invoke; on ambiguity it prefers the deliberate flow. A leaner environment is your choice, never a requirement.

## Install

```bash
/plugin marketplace add lucasfugisawa/deliberate-engineering
```

Then enable it via `/plugin`. Install `superpowers` first (or alongside) — it's a hard prerequisite.

## Getting started

Not sure where to begin? Run `/deliberate-engineering:start` and describe the work — it's the front door. It classifies the work, names the phases and the ceremony they earn, and routes you to the right deliberate phase. You can also call a phase directly (`:plan`, `:review`, `:verify`, `:debug`) when you already know where you are.

## Uninstall

Both steps are independent, and undoing this never touches your code or your repos:

1. **Disable or remove the plugin** via `/plugin` — that's the whole product.
2. **If** you added the optional always-on block (below) to your personal `~/.claude/CLAUDE.md`, delete it — everything from `<!-- deliberate-engineering:begin -->` through `<!-- deliberate-engineering:end -->`, inclusive. Removing it is unrelated to disabling the plugin; the rules then load only on description match, like any normal skill.

## What's inside (v0.1)

A standing-rules skill, a front-door router, four phase selectors backed by four read-on-demand catalogs, and five commands.

- **`deliberate-engineering-rules` skill** — six standing rules held across every phase: keep the human's hand on irreversible and outward-facing actions; stay read-only on systems you don't own; verify claims against primary evidence before endorsing; recommend with a reasoned pick, not a bare menu; keep comments load-bearing; and checkpoint durable state before compacting context. Scoped to software work — it stays quiet on research, prose, and ad-hoc analysis.
- **`deliberate-engineering-router` skill** — the front door. It classifies the work, names the phase sequence and the ceremony it earns, and routes to the matching selector; where the rules set your posture, the router decides where you start. It recommends rather than forces — the only hard stop is the human gate on irreversible actions.
- **Four selector skills + four catalogs** — each selector classifies the work, then pulls the matching lenses from its catalog (read on demand, never all at once).
- **Five commands** — `/deliberate-engineering:start` routes you to the right phase; `:plan`, `:review`, `:verify`, and `:debug` invoke a selector directly.

<details>
<summary><strong>The four catalogs in detail</strong> (106 strategies total)</summary>

- **Review — 53 strategies** in five groups: process / meta-review (13), verification & evidence (7), failure & contradiction reasoning (6), engineering-quality lenses (12), and reviews beyond back-end (15). Classifies your change by risk, reversibility, requirement clarity, and size, then selects the lenses that fit.
- **Verification — 21 strategies** in five groups: evidence & ground truth (5), local & pre-merge (5), staged promotion & rollout (5), post-deploy production verification (4), and operational data-mutation verification (2). For establishing something is *actually* true, with evidence from running systems — not just plausible on paper. Review asks "does this look correct?"; verification asks "is it correct, and what's my evidence?"
- **Planning — 16 strategies** in five groups: scope / anti-over-engineering (4), ground the plan in reality (4), calibrate ceremony to risk (2), slice & sequence (3), and capture the plan (3). For *before* code exists: deciding what work is worth doing and how much process it calls for. It delegates the *how-to-plan* discipline to your workflow engine.
- **Debug/Operate — 16 strategies** in five groups: trust the evidence (3), diagnose under uncertainty (2), respond under pressure (3), keep the signal healthy (5), and learn from the failure (3). For when a *live system* misbehaves and you must diagnose under uncertainty and respond. Verification confirms an expectation you already hold; this is discovery under failure, and it delegates the debugging *method* to your workflow engine.

</details>

### Make the rules always-on (optional)

Skills load when the model judges them relevant to the task. If you want the deliberate-engineering rules enforced on *every* engineering session — the way I run them — add a short block to your personal `~/.claude/CLAUDE.md`:

```markdown
<!-- deliberate-engineering:begin -->
## Deliberate-engineering (always-on for engineering work)
On software-engineering tasks — writing, reviewing, debugging, planning,
migrating, shipping, or operating code with real consumers, risk, or
irreversibility — apply the deliberate-engineering-rules skill, not just on
description match. Skip it for research, prose, ad-hoc analysis, disposable
no-consumer scripting, and non-technical work.
<!-- deliberate-engineering:end -->
```

Or append it idempotently from your shell (bash/zsh — macOS/Linux). Safe to run more than once; it won't duplicate the block:

```bash
grep -q 'deliberate-engineering:begin' ~/.claude/CLAUDE.md 2>/dev/null || cat >> ~/.claude/CLAUDE.md <<'EOF'

<!-- deliberate-engineering:begin -->
## Deliberate-engineering (always-on for engineering work)
On software-engineering tasks — writing, reviewing, debugging, planning,
migrating, shipping, or operating code with real consumers, risk, or
irreversibility — apply the deliberate-engineering-rules skill, not just on
description match. Skip it for research, prose, ad-hoc analysis, disposable
no-consumer scripting, and non-technical work.
<!-- deliberate-engineering:end -->
EOF
```

This is your machine's choice, never a requirement of the plugin. The rules themselves live entirely in the skill above; this block only changes *when* they fire on your machine. To undo it, see [Uninstall](#uninstall).

## Prior art & influences

This plugin stands on the shoulders of:

- **[superpowers](https://github.com/obra/superpowers)** (Jesse Vincent) — the required discipline engine that makes deliberate interception possible.
- **[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)** and **[mattpocock/skills](https://github.com/mattpocock/skills)** — pioneering work in curated skill catalogs for AI-assisted development.
- **General engineering practice** — review strategies, threat modeling, FMEA, and deliberate practice.

We study, we don't copy. Where design converges with existing work, we give credit. The catalog structure and composition patterns are original synthesis; the individual lenses draw from established engineering discipline.

## License

MIT
