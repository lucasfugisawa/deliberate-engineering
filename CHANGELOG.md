# Changelog

All notable changes to the `deliberate-engineering` plugin are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/), and the project aims at [Semantic Versioning](https://semver.org/) (pre-1.0: minor covers features and breaking changes, patch covers fixes).

## [0.7.0] - 2026-08-20

### Added
- **`deliberate-engineering-orchestrate`: a cross-session orchestrator.** The across-session sibling of the router. Where the router conducts the phases *within* one session, this orchestrates the units of work *across* sessions, for a program too large to fit a single context. It runs one loop: plan → dispatch decision → a self-contained handoff with its premise frozen against a live-state read → execute (a fresh, human-watched session by default) → WORK REPORT → verify at source, in a *separate* context for contested or high-stakes claims and at a scope as wide as the claim → disposition (accept/reject/follow-up) → a self-auditing tracker with a read-back → commit → capture any operator-caught gap. The worker is then done; a follow-up is a new self-contained handoff, never a kept-alive session. It is manual-first (Rule 8): a fresh session is the default dispatch, and a background subagent is an earned exception, allowed only for a unit that is self-contained and analytical/mechanical, has no stall-able access/tool/MCP prerequisite, is low-stakes and reversible, and ends in no outward action, widening only as trust converges and gated on a token budget. It is deliberately thin: roughly two-thirds of the loop is Rules 1/3/6/8/9 at a larger granularity, cited rather than restated, and it reuses the selectors (a worker runs its own plan/review/verify; the orchestrator's verify is the verification selector, its disposition the review selector), delegates the durable store to `deliberate-engineering-state` (the program tracker *is* the store that skill delegates to, not a second one), and routes its comms through `communication-collaboration-selector` and `deliberate-engineering-voice`. Explicit non-goals: no orchestration state-machine, no pre-built numbered-folder taxonomy, no maintained known-gotchas doc, no real-time messaging between the orchestration and worker sessions (it would kill the fresh-context boundary that makes a handoff worth writing), and no duplicate per-unit state beside the tracker. Placement was the open call: a DE capability rather than a standalone skill, because standalone would duplicate the rules, state, and selectors and drift out of sync with them, the one failure mode the design most wanted to avoid.
- **The orchestration templates.** `templates.md` beside the skill carries the three contracts, read on demand rather than up front: a handoff (mandate, premise freeze, exact scope, gates, verification steps, required report format, an explicit DO-NOT list), a work report (new state, what changed, gate/test evidence, judgment calls, an explicit "not done per dispatch"), and a program tracker with an always-current recovery anchor that lets any fresh session re-instantiate the orchestrator. They prescribe the *fields* (the part that made real handoffs work) and leave the *layout* free; the orchestrator generates the mechanical fields from a live-state read and hand-writes only the judgment fields. No program content ships: the plugin carries the mechanism and the skeletons, and every program's tracker lives in the operator's own private repo, the same split the voice layer already uses.

### Changed
- **README.** A "What's inside" entry for the cross-session orchestrator, and the summary line and command count updated (the front-door router now has an across-session sibling; nine commands became ten).
- **Architecture doc.** The lifecycle diagram gains an orchestrate node hanging off the router as its across-session sibling, and the command list under *drive the engineering flow* gains a `/deliberate-engineering:orchestrate` entry describing when the work is a program too large for one session.

## [0.6.0] - 2026-07-26

### Added
- **`deliberate-engineering-voice`: an optional operator voice profile layer.** A read-side skill built in the shape of `deliberate-engineering-overrides`: it reads a personal profile from `~/.claude/deliberate-engineering/voice/` and applies it as the surface layer over whatever the communication selector already decided. It loads only what the artifact needs (`core.md` always, the register matching the language, the archetype matching the communication type) rather than the whole directory, falls back to core plus register when no archetype matches and says so, and is a silent no-op when the directory is absent. Precedence: explicit instruction > voice profile > default style, with lenses winning on substance and the profile winning on surface where the two genuinely conflict. Two triggers, deliberately redundant: a one-line pointer from `communication-collaboration-selector`, and its own description for drafts requested outside the deliberate flow. Verified before release rather than asserted: a firing test on this build, with agents given only a natural-language request and no mention of any skill or profile, exercised fifteen artifact sub-types. All fifteen fired; fourteen loaded the archetype the profile intends. The negative case passed too, and it is the one that matters most: the profile is never applied to the agent's own replies to the operator, and the agent named the description text that excludes it. Both triggers were exercised independently, including a personal message that never touched the selector. What the test also found, and what this release fixes: the register was being chosen by the language of the request rather than the language the artifact ships in, a comment on a document was matching the archetype for commenting rather than for the document, and the selector's pointer was permissive enough to reach the profile without loading the skill that governs it.
- **The adopter kit for voice profiles.** `contract.md` (what the directory may contain, what loads when, the per-file size guidance, and why archetypes are named for communication types rather than for tools, with the pilot's nine as a suggested starting set), `bootstrap.md` (the generalized method: corpus collection, the analysis dimensions, an adversarial verification pass over the findings, the findings-driven style interview, synthesis, and blind A/B calibration, carrying the pilot's expensive lessons), and a `template/` skeleton. No profile content ships: the mechanism, the contract, the template and the method are public; every profile is private to its author.

### Changed
- **`communication-collaboration-selector` now consults the voice skill.** One line after the existing operator-overrides pointer and identical in form: after applying the selected lenses, consult `deliberate-engineering-voice`, apply the profile as the surface layer, and name the files loaded in the Output.
- **README.** A "What's inside" entry for the voice skill, a "Sound like yourself" section pointing at the contract, the template and the bootstrap guide, and a sentence in the optional always-on recipe covering engineering communications (the recipe's closing "skip" clause now names the router and the rules explicitly, since it had grown a third antecedent). That sentence carries its own scope: engineering communications only, and never the agent's own replies to the operator, so the recipe cannot be read as running the selector on every message the agent writes. The idempotent shell snippet is guarded on the begin marker and is therefore a no-op for anyone who pasted an earlier block, so the README now tells those readers to replace the content between the markers by hand.
- **Architecture doc, previously silent on voice while the README called it the full picture.** The lifecycle diagram gains a voice node hanging off the communication node, the communication bullet gains a sentence on the surface layer it applies, and the *Adapt* section, which described the personal layer as overrides only, now covers both personal layers under `~/.claude/deliberate-engineering/`.

## [0.5.0] - 2026-07-26

### Added
- **Rule 9: ship nothing the reader can't resolve.** A shipped artifact (code comment, commit message, PR/MR description) must be readable by someone holding that artifact and nothing else: no internal planning IDs, no pointers to a spec or design doc the reader can't open, no project-internal codename or jargon. Prompted by internal planning context leaking into PR descriptions and comments, where the reviewer (who never read the spec) cannot resolve it. The standing core moves 8 → 9.
- **Consistency harness: standing-rule count check.** `scripts/check-consistency.sh` now asserts that the rule count claimed in the rules skill, the README (twice), and the architecture doc (twice) matches the rules the skill actually defines, and that no rule number repeats. The harness previously guarded lens counts only, leaving the rule-count drift class (which shipped once already when Rule 7 landed) unguarded.

### Changed
- **Rule 5 now governs comment form, not just content.** Default to one line; a comment that ran to several is usually one that says too much, so cut the text before reflowing it. Width defers to whatever the repository actually uses (its formatter, its linter, the surrounding code) rather than an imported 80-column habit.
- **The authoring convention no longer endorses narrow comments.** It previously stated that fixed-column hard-wrapping *suits* code comments, licensing the exact fragmentation Rule 5 now discourages. Comment length and width have a single owner: Rule 5.
- **Review lens 34 sharpened and re-routed.** Comment judgment was half a clause inside a broad readability lens; it is now a named test with three parts (must the comment exist, is it as tight as it can be, do its references resolve). Routing moved off the "wide blast radius" axis (where it was the only entry point) to any diff that adds or edits source, because this defect class does not correlate with risk. At the trivial-and-safe band it collapses to a scan.
- **Communication lens 5 keys on reader resolvability, not audience distance.** It previously excluded "peers with equal access", using audience as a proxy for whether a reference resolves. So a PR read by a teammate, the most common leak path, fell outside it. Retitled from "No internal IDs" to cover unresolvable *context* (jargon and codenames, not only numbers), and its selector trigger widened to match.
- **Communication lens 1 (PR/MR description) now states the resolvability bar explicitly.** The case for the change must be stated in terms the reviewer can resolve unaided (no spec item numbers, no internal codenames), cross-referencing lens 5 and Rule 9.

### Fixed
- **Communication lens 5 pointed at a rule that did not exist.** Its Kin line claimed the rules skill governed internal IDs in shipped code artifacts; no such rule existed, so the delegation was a dead end. It now points at Rule 9.

## [0.4.2] - 2026-07-03

### Changed
- **Rule 3 readability**: the standing rule's dense single-paragraph "How to apply" (which packed ~9 distinct imperatives into one block) is broken into a lead sentence plus a labeled sub-list, so no directive is buried mid-paragraph. No content changed; every imperative is preserved verbatim.
- **`deliberate-engineering-overrides` `modify` concision**: the append-only / read-both instruction, previously asserted ~5 times in one bullet, is trimmed to the bold safety statement plus one operational sentence. Meaning unchanged. (The parallel selector "Step 4" restatement flagged in the same review was assessed and **kept**: on inspection only the verify selector genuinely restates its catalog Appendix; planning and debug Step 4s are selector-specific composition ordering, and review's is the load-bearing fresh-eyes discipline.)

## [0.4.1] - 2026-07-03

### Fixed
- **Four catalog lenses were unreachable from their own selectors**, the same drift class as the v0.4.0 lens-7 fix, surfaced by a full-plugin review: review #55 (blast-radius / change-impact), verify #22 (match-verification-scope-to-the-claim), verify #23 (differential verification), and debug #17 (contain the blast radius) each existed in a catalog but no selector's Step 3 routed to them, so an agent following the selector never picked them. Each is now routed from its selector.
- **Architecture doc shipped a stale override-file path**: `~/.claude/deliberate-engineering-overrides.md` (the pre-0.2.0 flat path) instead of the relocated `~/.claude/deliberate-engineering/overrides.md`; an adopter who followed it wrote overrides to a path the read-side never consults, a silent no-op. Also corrected two pointers to a non-existent README section ("Override a lens or rule" → "Make it yours").
- **Override safety guard could be bypassed by header string.** The elevated-autonomy acknowledgement fired only for targets literally named `Rule 1`/`Rule 2`; a gate-loosening `add: rules` (or `add: <catalog>`) entry (which the v0.4.0 capture calibration signal can propose) slipped through as a common one-line note. The guard now keys on the override's *content* (does it relax a Rule 1/Rule 2 gate?), not the header string.
- **Incident-path Rule 1 reconciliation**: debug #6 ("restore first; don't wait for the author") now clarifies that Rule 1 still governs the *trigger* for an AI agent: prepare the revert and hand it to the on-call responder; "don't wait for the author" means don't block on the *original author*, not that the agent pushes to a shared baseline autonomously.
- **Documentation nits**: corrected the `deliberate-engineering-state` working-note example (wrong lens glosses + a reference to a non-existent "contribution" catalog); aligned the structural-change design-cycle wording (the promote skill now says "build," matching CONTRIBUTING); removed an orphan `[0.2.1]` CHANGELOG link; trimmed one intra-paragraph duplication in the router.

## [0.4.0] - 2026-07-03

### Added
- **Consistency harness**: `scripts/check-consistency.sh` plus a `consistency` CI workflow assert that every lens-count claim agrees across the catalogs, the README, and the architecture doc, and that no lens number repeats. The catalogs are the single source of truth; the check fails loudly on the class of drift where a lens is added append-only while a routing table or a doc count goes stale. Runnable locally before pushing.
- **Verification lens #24: closeout obligations discharged** (Part D, post-deploy). After a flagged, staged, or temporary ship, verify with evidence that the cleanup it obligated was actually done (the flag removed, the stranded code deleted, the docs updated), not just that the feature works. The *doing* stays cross-referenced to review #35 and planning; this lens confirms it happened.
- **`deliberate-engineering-capture`: a third signal, calibration adjustments.** Alongside deviations and patterns, capture now surfaces recurring miscalibration (running a class of work heavier or lighter than the recommended ceremony) and proposes it as `planning #10: modify` or `add: rules`. It never targets the router's classification axes, which are architecture, not overridable content.

### Fixed
- **Communication selector routed handoffs nowhere.** The durable-handoff lens (7) existed in the catalog, but the selector's Step 2 routing stopped at lens 6 and the architecture doc miscounted the catalog as six lenses, so an agent following the routing never selected the lens built for handoffs. Handoffs, status updates, and working notes now route to lens 7; the count is corrected to seven.

### Changed
- **Meta-skill concision.** `capture`, `contribute`, and `promote` each stated their differentiator three times (frontmatter description, a "vs …" section, and an inline restatement); the "vs …" sections and "On demand only" collapse into one compact `## Boundaries` list per skill. All operational content (the transcript/bash/python steps, candidate formats, and gated-write/error-handling procedures) is unchanged.

## [0.3.0] - 2026-07-01

### Changed
- **`deliberate-engineering-capture`** now draws its signals from the **full session transcript on disk** instead of the live (compactable) context window, closing a gap where invoking capture late in a long session silently missed the early-session practice it exists to make durable. It resolves the current session's transcript via `CLAUDE_CODE_SESSION_ID`, filters to the operator's typed voice (`origin.kind == "human"`; agent output, tool-results, and harness-injected notifications never pass), chunks the result to a scratchpad, and mines it via a **fan-out of subagents** so the raw transcript never fills the main context. Scope defaults to the current session (project-wide only on explicit request), and it degrades to live-context observation when no transcript is reachable. This mirrors the methodology used for the plugin's original catalog harvest.

### Documentation
- **README**: added a *Keeping it up to date* section under Install: how to enable marketplace auto-update (`/plugin` → Marketplaces → select the marketplace → Enable auto-update) and why Claude Code leaves it off by default for third-party marketplaces (it never updates third-party code without consent). Docs-only; no change to shipped skills or commands.

## [0.2.0] - 2026-06-29

### Added
- **`deliberate-engineering-state`**: a consulted-only skill that owns a per-work-unit working-note, so process state (the phase sequence, current phase, chosen rituals, open pendings, and the decisions and why) survives across sessions. The router and Rule 6 delegate to it to rehydrate on resume and checkpoint as work proceeds; it delegates to a tracker or workflow engine when one already holds the work.

### Changed
- **Re-execution integrity**: re-invoking a review now re-executes from source by construction instead of reusing in-context conclusions: a recompute-on-reinvocation posture folded into Rule 3 (no new rule; the core stays at eight), fresh-context subagent dispatch as the depth-scaled default execution mode, evidence artifacts as the per-lens completion criterion, and world-derived scope resolution. The evidence-tied Output contract is now unified across the four phase selectors.
- **Override file relocated**: the personal override file moved from `~/.claude/deliberate-engineering-overrides.md` to `~/.claude/deliberate-engineering/overrides.md`, joining the common `~/.claude/deliberate-engineering/` namespace alongside the state working-note. Hard move, no migration shim.
- **README**: added the state skill to the inventory; fixed an internal contradiction where the prior-art line described `superpowers` as making the plugin "possible" while the install section (correctly) states the judgment layer degrades gracefully without it.

## [0.1.0] - 2026-06-27

### Added
- First public release. A standing-rules skill (eight rules), a front-door router (`:start`), four phase selectors backed by four read-on-demand catalogs (`:plan`, `:review`, `:verify`, `:debug`), one cross-cutting communication selector (`:communicate`), a personal override layer with an adopter capture tool (`:capture`), and an author contribution flow (`:contribute`, `:promote`). Includes the live-recalibration router step and the catalog lens-quality pass shipped on 2026-06-29 prior to versioned releases.

[0.6.0]: https://github.com/lucasfugisawa/deliberate-engineering/releases/tag/v0.6.0
[0.5.0]: https://github.com/lucasfugisawa/deliberate-engineering/releases/tag/v0.5.0
[0.4.2]: https://github.com/lucasfugisawa/deliberate-engineering/releases/tag/v0.4.2
[0.4.1]: https://github.com/lucasfugisawa/deliberate-engineering/releases/tag/v0.4.1
[0.4.0]: https://github.com/lucasfugisawa/deliberate-engineering/releases/tag/v0.4.0
[0.3.0]: https://github.com/lucasfugisawa/deliberate-engineering/releases/tag/v0.3.0
[0.2.0]: https://github.com/lucasfugisawa/deliberate-engineering/releases/tag/v0.2.0

<!-- 0.1.0 predates tagged releases (v0.2.0 is the first git tag), so it has no release link. -->

