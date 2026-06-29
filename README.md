# deliberate-engineering

*Engineering discipline for AI-assisted development. Less vibe coding, more deliberate craft.*

## What it is

Coding agents are good at *acting*. `deliberate-engineering` makes them good at *judging how much* — sizing each change to its risk, reversibility, and reach; applying the review, verification, and planning lenses that fit *this* case; and checking that "done" holds against reality before moving on. It is a thin **judgment layer** on top of your agent's raw capability, not another how-to engine.

Left to its defaults, an agent gives a one-line change to a money calculation the same effort as a typo fix, and can report "done" before anything met reality — not from carelessness, but because nothing told it this change was different. This layer is what tells it: it classifies the work first, then decides *how much* ceremony the change has earned, *which* lenses it actually calls for, and *whether* the result is really true — and it stops at a human gate for anything irreversible or outward-facing.

One mental model runs across the whole lifecycle — **risk, reversibility, requirement clarity, and reach decide the depth, not line count:**

| Phase | Selector | The question it answers |
|---|---|---|
| **Plan** | `planning-strategy-selector` | What's worth building, and how much process does it deserve? |
| **Review** | `review-strategy-selector` | Which lenses does *this* change actually call for? |
| **Verify** | `verification-strategy-selector` | Is it true against reality — and what's my evidence? |
| **Debug/Operate** | `debug-operate-strategy-selector` | A live system is misbehaving and I have no reliable expectation — now what? |

Planning decides what to build; review reasons about the artifact; verification confronts reality; and debug/operate takes over when a live system misbehaves and no reliable expectation holds.

## See it in action

Ask for something risky and it sizes the work *before* diving in. For "implement field X on the billing model," instead of charging ahead it leads with its judgment:

> **Genre:** change to an existing system. **Axes:** clarity medium, risk high (billing), reversibility low, reach wide.
> **Sequence:** plan → build → review → verify, full ceremony.
> **Skipping:** nothing — high risk allows no shortcut.
> **Gate (Rule 1):** I stop before deploy/merge for you to trigger. Starting with the **plan** phase.

For a typo fix it does the opposite — and says so: "trivial and safe, single phase, no ceremony." Calibration runs both ways; the point is that the depth is a deliberate, visible decision, not an autopilot default.

## Install

Inside Cloude Code:
```claude
/plugin marketplace add lucasfugisawa/deliberate-engineering
/plugin install deliberate-engineering@deliberate-engineering
/reload-plugins
```

or in terminal:
```bash
claude plugin marketplace add lucasfugisawa/deliberate-engineering
claude plugin install deliberate-engineering@deliberate-engineering
```

**Recommended companion:** install [`superpowers`](https://github.com/obra/superpowers) (Jesse Vincent) alongside it. `deliberate-engineering` owns the *judgment* and delegates the *method* — TDD, systematic debugging, plan execution — to `superpowers`. Without it the judgment layer still works: it classifies the work, calibrates the ceremony, and applies the rules and lenses; it simply delegates execution to whatever engine you have, including Claude Code's built-in abilities.

It ships as a Claude Code plugin — the honest scope is Claude Code today; it doesn't claim to run on other agents or IDEs. It complements review tooling such as `pr-review-toolkit` (it decides *which* tactics a change calls for and can invoke those agents as tactics) and coexists with other workflow plugins such as `feature-dev` (when several engines are present it decides which to invoke and removes nothing).

### Optional: make the deliberate layer always-on

Skills load when the model judges them relevant to the task. If you want the layer engaged on *every* engineering session — routing through `/deliberate-engineering:start` with the standing rules underneath, the way I run it — add a short block to your personal `~/.claude/CLAUDE.md`:

```markdown
<!-- deliberate-engineering:begin -->
## Deliberate-engineering (always-on for engineering work)
On software-engineering tasks — writing, reviewing, debugging, planning,
migrating, shipping, or operating code with real consumers, risk, or
irreversibility — begin by invoking `/deliberate-engineering:start` (the
`deliberate-engineering-router`) to classify the work and route to the right
phase, not just on description match. The `deliberate-engineering-rules` skill
is the always-on constitution underneath — it holds on every engineering task
regardless of phase, and the router cites it rather than replacing it. Skip
both for research, prose, ad-hoc analysis, disposable no-consumer scripting,
and non-technical work.
<!-- deliberate-engineering:end -->
```

Or append it idempotently from your shell (bash/zsh — macOS/Linux). Safe to run more than once; it won't duplicate the block:

```bash
grep -q 'deliberate-engineering:begin' ~/.claude/CLAUDE.md 2>/dev/null || cat >> ~/.claude/CLAUDE.md <<'EOF'

<!-- deliberate-engineering:begin -->
## Deliberate-engineering (always-on for engineering work)
On software-engineering tasks — writing, reviewing, debugging, planning,
migrating, shipping, or operating code with real consumers, risk, or
irreversibility — begin by invoking `/deliberate-engineering:start` (the
`deliberate-engineering-router`) to classify the work and route to the right
phase, not just on description match. The `deliberate-engineering-rules` skill
is the always-on constitution underneath — it holds on every engineering task
regardless of phase, and the router cites it rather than replacing it. Skip
both for research, prose, ad-hoc analysis, disposable no-consumer scripting,
and non-technical work.
<!-- deliberate-engineering:end -->
EOF
```

This is your machine's choice, never a requirement of the plugin — it only changes *when* the router and rules fire on your machine. To undo it, see [Uninstall](#uninstall).

## Getting started

Not sure where to begin? Run `/deliberate-engineering:start` and describe the work — it's the front door. It classifies the work, names the phases and the ceremony they earn, and routes you to the right phase. When you already know where you are, call a phase directly: `:plan`, `:review`, `:verify`, `:debug`.

For the full picture — how the pieces fit together and how to drive each flow, including personalizing and contributing — see **[Architecture & usage](docs/architecture-and-usage.md)**.

## What's inside

A standing-rules skill, a front-door router, four phase selectors backed by four read-on-demand catalogs, one cross-cutting communication selector, a personal override layer, a process-state working-note, and an author contribution flow — plus nine commands.

- **`deliberate-engineering-rules`** — eight standing rules held across every phase: keep the human's hand on irreversible and outward-facing actions; stay read-only on systems you don't own; verify claims against primary evidence before endorsing; recommend with a reasoned pick, not a bare menu; keep comments load-bearing; checkpoint durable state before compacting; name the edge of what you know rather than fabricate certainty; and treat trust in an output as earned by convergence — when review stabilizes and assumptions hold — not granted on a single pass. Scoped to software work; quiet on research, prose, and ad-hoc analysis.
- **`deliberate-engineering-router`** (`:start`) — the front door: it classifies the work, names the phase sequence and the ceremony it earns, and routes to the matching selector. It recommends rather than forces — the only hard stop is the human gate on irreversible actions.
- **Four phase selectors + catalogs** — `:plan`, `:review`, `:verify`, `:debug`. Each classifies the work, then pulls only the matching lenses from its catalog (read on demand, never all at once).
- **`communication-collaboration-selector`** (`:communicate`) — cross-cutting, not a phase: when the artifact you're producing is a *communication* — a PR description, a review comment, a stakeholder message, a writeup of alternatives — it classifies by audience and artifact (not the four phase axes) and applies the matching lenses. Consult it from inside any phase.
- **Make it yours** — a personal override layer lets your own practice take precedence over any shipped lens or rule; `/deliberate-engineering:capture` distills a session into ready-to-paste override blocks. See [Make it yours](#make-it-yours).
- **`deliberate-engineering-state`** — a consulted-only skill that owns a per-work-unit working-note, so process state (the phase sequence, current phase, chosen rituals, open pendings, and the decisions and why) survives across sessions. The router and Rule 6 delegate to it to rehydrate on resume and checkpoint as work proceeds; it delegates to your tracker or workflow engine when one already holds the work.
- **For contributors** — `/deliberate-engineering:contribute` and `:promote` grow the *shared* catalog from a local clone of this repo (generalize-at-capture, a blocking leak-audit, append-only numbering, and a stop before publish). This is the author side, distinct from your personal overrides; see [`CONTRIBUTING.md`](CONTRIBUTING.md).

<details>
<summary><strong>The four phase catalogs in detail</strong> (114 strategies total; the cross-cutting communication catalog adds seven lenses)</summary>

- **Review — 55 strategies** in five groups: process / meta-review (14), verification & evidence (7), failure & contradiction reasoning (6), engineering-quality lenses (13), and reviews beyond back-end (15). Classifies your change by risk, reversibility, requirement clarity, and size, then selects the lenses that fit.
- **Verification — 23 strategies** in five groups: evidence & ground truth (6), local & pre-merge (6), staged promotion & rollout (5), post-deploy production verification (4), and operational data-mutation verification (2). For establishing something is *actually* true, with evidence from running systems — not just plausible on paper. Review asks "does this look correct?"; verification asks "is it correct, and what's my evidence?"
- **Planning — 19 strategies** in six groups: scope / anti-over-engineering (4), ground the plan in reality (4), calibrate ceremony to risk (2), slice & sequence (3), capture the plan (3), and disambiguation / readiness (3). For *before* code exists: deciding what work is worth doing and how much process it calls for. It delegates the *how-to-plan* discipline to your workflow engine.
- **Debug/Operate — 17 strategies** in five groups: trust the evidence (3), diagnose under uncertainty (2), respond under pressure (4), keep the signal healthy (5), and learn from the failure (3). For when a *live system* misbehaves and you must diagnose under uncertainty and respond. Verification confirms an expectation you already hold; this is discovery under failure, and it delegates the debugging *method* to your workflow engine.

</details>

## Make it yours

The plugin is opinionated, and it's meant to become yours. A personal file at `~/.claude/deliberate-engineering/overrides.md` takes precedence over the shipped lenses and rules, addressed by stable identifiers — `review #35`, `verify #14`, `planning #8`, `debug #12`, or `rule 2`. Three operations: `disable` turns a lens or rule off; `modify` appends your own note alongside the shipped text (the shipped text stays, your annotation is read with it); and `add` defines your own strategy or rule. The agent always declares when an override changed what it did — nothing happens silently — and you can even loosen a safety rule, which it honors while calling out the raised autonomy. The layer is opt-in: if the file doesn't exist, nothing changes.

You can write that file by hand, or let `/deliberate-engineering:capture` (or just ask) distill the session you just had — the lenses you skipped or adjusted, the practice the catalog lacks — into ready-to-paste blocks, appended only on your approval.

**Example override file:**

```markdown
## review #35 — disable

**Why:** We run this lens manually in a separate security pass; not needed in the main review.

## add — review

**Name:** API backward-compatibility check — no breaking signature changes without major version bump

**When:** The change modifies a public API surface — REST endpoints, library exports, gRPC contracts

**Apply:** Review the diff for any breaking changes (removed endpoints, changed request/response shapes, deleted fields). If a breaking change is present and the version is not a major bump, flag it. Non-breaking additions (new optional fields, new endpoints) are fine.
```

For the override format in full and the adopter and author flows end to end, see **[Architecture & usage](docs/architecture-and-usage.md)**.

## Why a plugin, not a `CLAUDE.md`?

You could paste a few rules into your `CLAUDE.md` — and the always-on recipe above is exactly that for the always-on part. The plugin adds what a static file can't: it **classifies each change first** and reads only the lenses that fit (progressive disclosure — the catalogs load on demand, never as a wall of text in your context); it exposes **addressable, overridable** lenses and rules (`review #35`, `rule 2`) you can disable, annotate, or extend from your own file, and grow with `:capture`; and it ships a router that engages the right depth *just-in-time* instead of as standing instructions you pay for on every task. The eight rules are the small always-on core; everything else loads when the work calls for it.

## Scope & boundaries

`deliberate-engineering` is a **horizontal** layer: the judgment that holds across every domain — how to classify risk, calibrate ceremony, verify claims, and decide deliberately. It deliberately stops where domain *depth* begins, and that boundary is the design, not a gap. Process judgment is the same whether you're shipping an API, a database schema, or a mobile screen — so this layer stays transferable across all of them, and folding in any one domain's depth would only make it less so.

So it does not carry domain-specific knowledge — API design, data modeling, performance tuning, observability, security hardening, mobile, front-end, and the rest. At the edge where that depth matters, it does the honest thing: it names what it doesn't carry and points you to bring your own domain expertise, rather than fake a competence it doesn't have. That is the same discipline the rules ask of the agent (Rule 7 — name the edge of what you know), turned on the plugin itself.

## Uninstall

Both steps are independent, and undoing this never touches your code or your repos:

1. **Disable or remove the plugin** via `/plugin` — that's the whole product.
2. **If** you added the optional always-on block to your personal `~/.claude/CLAUDE.md`, delete it — everything from `<!-- deliberate-engineering:begin -->` through `<!-- deliberate-engineering:end -->`, inclusive. Removing it is unrelated to disabling the plugin; the router and rules then load only on description match, like any normal skill.

## Prior art & influences

This plugin stands on the shoulders of:

- **[superpowers](https://github.com/obra/superpowers)** (Jesse Vincent) — the recommended companion engine this layer delegates method to (TDD, systematic debugging, plan execution); the judgment layer degrades gracefully without it.
- **[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)** and **[mattpocock/skills](https://github.com/mattpocock/skills)** — pioneering work in curated skill catalogs for AI-assisted development. They also exemplify the vertical, domain-deep catalogs that complement this horizontal layer — the kind of depth the *Scope & boundaries* section points you to bring yourself.
- **General engineering practice** — review strategies, threat modeling, FMEA, and deliberate practice.

We study, we don't copy. Where design converges with existing work, we give credit. The catalog structure and composition patterns are original synthesis; the individual lenses draw from established engineering discipline.

## License

MIT
