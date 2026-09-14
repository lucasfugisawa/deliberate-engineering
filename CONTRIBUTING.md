# Contributing to deliberate-engineering

Thank you for your interest in contributing to `deliberate-engineering`. This plugin is built on the principle of **process, not prose**: every strategy is a lens through which to examine work, not a checklist to recite.

This file is the contributor *policy*: what a contribution must satisfy and how a lens is shaped. It deliberately does not re-describe the contribution flow or its mechanism: those have a single home each (see *Where the rest lives* at the end).

## What a contribution must satisfy

All contributions must adhere to these constraints:

- **Domain-agnostic**: a strategy must apply broadly across software engineering, not be specific to one language, framework, or domain. The plugin is a horizontal judgment layer; depth in any one domain belongs elsewhere.
- **Employer-neutral**: no company names, internal tools, ticket IDs, service names, incident numbers, real quantities, or proprietary processes. Anything that cannot be said without the specifics is dropped, not half-cleaned.
- **Public and shareable**: content must be suitable for open-source distribution under the MIT license.

## How a lens is structured

Each lens in a catalog follows a consistent three-part structure:

1. **How it works**: the concrete mechanism: what you do when applying this lens.
2. **Objective**: the engineering goal this lens achieves.
3. **When most valuable**: the contexts where this lens provides the most signal.

**Fresh-context review blocks promotion.** The `promote` workflow dispatches a separate reviewer through the active host's native subagent mechanism and treats an unavailable reviewer as a rejection. A specialized reviewer may be used when installed, but no second plugin is required. If the host cannot dispatch a fresh context, promotion stops before deleting the candidate.

**Two naming families, on purpose.** A skill that owns a catalog of numbered lenses is named for the job it does (`review-strategy-selector`, `planning-strategy-selector`, `verification-strategy-selector`, `debug-operate-strategy-selector`, `communication-collaboration-selector`), because that name is what an agent matches when it needs that kind of judgment. Everything else carries the `deliberate-engineering-` prefix, because those skills are mechanism rather than method and the prefix keeps them from colliding with anything else installed. A new skill takes whichever family fits what it is; do not rename an existing one, since a skill name is an address that override files and other skills cite.

Counts, structure, host compatibility, and versions are mechanically enforced: `scripts/check-consistency.sh` checks catalog counts; `scripts/check-invariants.py` checks the shared methodology; `scripts/check-host-compatibility.py` checks both host adapters; and the CI version gate keeps the three version-bearing metadata entries in lockstep (see *Releasing*). Run the full local suite below before opening a PR.

**Five checks run in CI, and you should run all five locally.** From the repo root:

```
./scripts/check-consistency.sh
python3 scripts/check-invariants.py --base origin/main
python3 scripts/test-check-invariants.py
python3 scripts/check-host-compatibility.py
python3 scripts/test-host-compatibility.py
```

The first needs bash 4 or newer. macOS ships bash 3.2 as `/bin/bash`, so if that is the only bash on your machine the script stops and tells you; install a newer one and invoke it directly, for example `/opt/homebrew/bin/bash scripts/check-consistency.sh`.

**`--base` is not optional in practice.** Without it the second check prints `skipped: append-only numbering` and still exits 0, so it reports success without having checked whether a published lens number moved, which is the one invariant an operator's override file depends on.

**The third and fifth checks test the checks, not your change.** They exercise negative controls, because a guard nobody has watched fail is not a guard. Their controls anchor on repository contracts; when a correct contribution changes one of those contracts, update the corresponding control rather than weakening the production check.

This structure makes lenses composable and context-aware: a selector reasons about which lenses a specific change calls for by matching the change's characteristics to each lens's *when most valuable* clause. A lens should teach a deliberate practice, not provide a static checklist: composable (rotate the lens each pass; find → verify; close with fresh eyes), context-aware (selected by the classification its own selector runs: risk, reversibility, requirement clarity, and reach for planning and review; evidence type and irreversibility for verification; the expectation gate for debug; audience and artifact for communication), and empirically grounded (validate claims rather than assume them).


**A composition pattern is shaped differently.** It lives as one numbered bullet in that catalog's `## Appendix: Composition Patterns`, `- **N. Title:** a sentence or a few, long enough to say when the pattern applies and why`, and it is numbered in its own namespace: `review pattern #7` is not `review #7`. The test that separates the two is what the thing acts on. A lens is applied to the artifact under review; a pattern is applied to the lenses. A pattern is not finished until every selector compose step that should run it cites it by number and name, which `scripts/check-invariants.py` enforces.
## How to contribute a lens

**If you hand-edit a catalog**, these are the obligations and the reasons behind them. Most are enforced by a guard and fail the build; the first two are conventions the guards do not parse, so nothing but review will catch them.

- **Shape.** A lens is `### N. Title` followed by exactly three bullets, `**How it works:**`, `**Objective:**`, `**When most valuable:**`. The title must contain at least one word of four letters or more that is not a stopword, because a citation is recognised by the lens's number beside a word from its own title; a title like "Own the why, not the how" cannot be cited at all.
- **The communication catalog is different.** It is flat, with no Parts, and every lens carries a required fourth bullet, `**Tags:**`, which its selector reads to pick lenses. A communication lens written in the four-catalog shape is invisible to the selector that would have used it.
- **Numbering is append-only.** Take the next free number and place the lens under the Part its theme belongs to, even if that leaves the Part out of numeric order. A published number is an address an operator may have written into their override file, so it never moves.
- **Route it.** A new lens is not finished until its own selector's `SKILL.md` cites it by number beside a word from its title. A lens no step names is a lens no agent reads. If it genuinely should not be routed, say why in `scripts/routing-exemptions.txt`; that file also declares a Part routed as a whole group, and it must pin the exact set it covers.
- **The same holds for a composition pattern**, cited from its selector's compose step as a bold number beside a word from its title.
- **A new skill that cites a lens number** acquires an obligation to consult the override layer, or to be listed in `scripts/consult-exemptions.txt` with a reason. Both exemption files fail the build on an entry with no reason or one naming something that does not exist. Only the routing file also fails on an entry that has gone dead, so a stale consult exemption survives until someone reads it.
- **A skill that delegates operative content to a companion file** must point at that file inside the first twelve lines of its `SKILL.md` body, in the imperative, or be listed in `scripts/companion-exemptions.txt` with a reason. An external run measured the descriptive form ("read on demand", forty-one lines into the body) producing no read at all: the agent authored the whole artifact and every required field of the delegated contract was missing. The word "read on demand" now fails the build.
- **Counts move together.** Adding one lens changes the catalog's own intro sentence, the README's per-catalog count, that catalog's group parentheticals in the README, and the README's total across the four phase catalogs. A communication lens moves a different set: its catalog intro, plus the two places the README and the architecture doc state the communication count. A standing-rule change moves five separate prose claims. The consistency check names each one it finds wrong.
- **A composition appendix states its own count** in the same shape, `This appendix contains N composition patterns`.
- **Three passages are pinned byte-identical** across the selectors: the override consult, the pattern-override consult, and the direct-entry paragraph. Copy-editing one file diverges it from the three or four others carrying it and fails the build; edit all of them or none.
- **Every command file** must carry the literal line `` Invoke the `<skill>` skill ``, target a real skill directory, and be the only command that targets it. The README's `plus <N> commands` is pinned to the real count.


**Two paths, and both are real.** The assisted path has never actually been used: no candidate file has ever been committed, and candidates are removed on promotion, so the queue is empty either way; what is certain is that the catalogs grew across thirty-odd direct commits. Hand-editing is the ordinary path and the rules for it are below. The assisted path exists because it carries a leak-audit gate and does the bookkeeping for you. Run the author tools from a local clone of this repository (they operate on the repo's own catalogs and `candidates/` queue):

**Command notation.** The slash forms below are Claude Code commands. In Codex 0.154, choose `contribute (deliberate-engineering)` or `promote (deliberate-engineering)` through `/skills`, or invoke `$deliberate-engineering:contribute` or `$deliberate-engineering:promote` directly.

- `/deliberate-engineering:contribute` turns a session's generalizable judgment into a `pending` candidate (generalizing at capture: extracting the employer-neutral principle and discarding the specifics). A candidate targets one of the catalogs (`review`, `verify`, `planning`, `debug`, `communication`) or, for a standing-rule change, `rules`.
- `/deliberate-engineering:promote` drives a candidate into the catalog through a blocking leak-audit, an append-only edit, and the routing that makes the new lens reachable, and stops before commit/PR/push: publication is your decision.

**The candidate file, if you write one by hand.** A candidate is one markdown file in `candidates/` with frontmatter and two prose sections. The frontmatter carries `target` (the catalog, or `rules`), `kind` (`lens` or `pattern`, and a file written before that field existed reads as `lens`), `operation` (`add` or `modify`), `modifies` (the number within that kind when modifying, else null), `status: pending`, and `date`. The body is a `# Title`, a `**Principle (as it would enter the catalog):**` and a `**Rationale:**`. Two combinations are malformed by construction: `kind: pattern` with `target: communication`, because that catalog has a prose composition note and no numbered patterns, and `target: rules` is valid but never takes the append-only route, because a standing rule is constitutional content that goes to a design cycle instead.

A **new catalog**, a reorganization, or a change to the standing rules is a *structural* change, not a single lens. It is not auto-applied: capture it as a candidate the same way (a rule change is a `rules` candidate, which `/deliberate-engineering:promote` always routes structurally, never into an append-only edit), and promotion stops at a recommendation for the full design cycle (brainstorm → spec → plan → build) instead of touching a catalog. Open an issue before investing in implementation: for a new catalog, describe the classification axes, the lens structure, and how it composes with the existing catalogs; for a rule change, describe what every session would then load and why the existing standing rules do not already cover it.

## Releasing (maintainer)

A release is any change to the shipped plugin that reaches adopters. The version is decided by a human: the CI gate only checks that the step was not forgotten; it never picks or applies a number for you.

When publishing a release:

1. **Bump the version in lockstep**: `plugins/deliberate-engineering/.claude-plugin/plugin.json`, `plugins/deliberate-engineering/.codex-plugin/plugin.json`, and the Deliberate Engineering entry in `.claude-plugin/marketplace.json` must carry the **same** version. The Codex marketplace schema has no version field. Pre-1.0: a new skill, command, catalog, lens, or composition pattern is a **minor** (`0.x.0`); a pure fix is a **patch** (`0.x.y`). So is anything that makes shipped content addressable that was not, since an adopter gains something they could not write before. The override-file relocation in 0.2.0 was technically breaking, but pre-1.0 minor already covers that. Claude Code offers an update only when the version *string* changes. Codex also uses the manifest version as the installed release identity and cache path, even though Codex 0.154 refreshes a Git marketplace and release by marketplace upgrade followed by remove/add.
2. **Update `CHANGELOG.md`**: a new section for the version, newest first, opening with a short prose paragraph saying what the release is about. The headings in use are Added, Changed, Fixed, Removed, Tooling and Documentation; a release whose version needed a judgment call also carries a short `**A note on the version.**` block saying why.
3. **Review every publication narrative for employer neutrality and reader resolvability**: this includes CHANGELOG entries, release notes, origin notes, examples, and other explanatory prose. Remove or generalize employer, customer, internal-tool, ticket, incident, private-service, proprietary-process, and external operational details that the public repository or a clearly public source cannot resolve, while preserving the technical lesson and its evidence level. Review by category and context; do not encode discovered values in a denylist.
4. **Tag the release**: annotated tag `vX.Y.Z` on the release commit, pushed alongside `main`.

The CI workflow `.github/workflows/version-gate.yml` checks two of these: it fails if the three version-bearing metadata entries disagree (Check A). Check B fails when a compared payload or marketplace path changed and the current and base Claude-manifest versions can be read but remain equal; it checks for a version difference, not a semantic increase. Check B reports a skip and exits successfully when no usable base commit is available, and it also cannot reject equality when the base manifest version cannot be read. On a pull request these jobs can report failure; whether that prevents merge depends on repository policy requiring their statuses. The workflow does not check the changelog or the tag: those stay your discipline.

## Questions?

Open an issue on the [GitHub repository](https://github.com/lucasfugisawa/deliberate-engineering) with your question or proposal.

## Where the rest lives

To keep one home per topic and avoid drift:

- **The contribution flow end to end** (the diagram and the walkthrough): `docs/architecture-and-usage.md`, *Contribute: ship judgment to everyone*.
- **The mechanism** (generalize-at-capture, the leak-audit gate, append-only numbering, stop-before-commit): the `deliberate-engineering-contribute` and `deliberate-engineering-promote` skills themselves.
- **Counts, install, and scope**: the [README](README.md). **The override-file format and an example**: `docs/architecture-and-usage.md`, *Adapt: make it think like you*.
