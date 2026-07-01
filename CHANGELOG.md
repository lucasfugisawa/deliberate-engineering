# Changelog

All notable changes to the `deliberate-engineering` plugin are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/), and the project aims at [Semantic Versioning](https://semver.org/) (pre-1.0: minor covers features and breaking changes, patch covers fixes).

## [0.3.0] — 2026-07-01

### Changed
- **`deliberate-engineering-capture`** now draws its signals from the **full session transcript on disk** instead of the live (compactable) context window — closing a gap where invoking capture late in a long session silently missed the early-session practice it exists to make durable. It resolves the current session's transcript via `CLAUDE_CODE_SESSION_ID`, filters to the operator's typed voice (`origin.kind == "human"`; agent output, tool-results, and harness-injected notifications never pass), chunks the result to a scratchpad, and mines it via a **fan-out of subagents** so the raw transcript never fills the main context. Scope defaults to the current session (project-wide only on explicit request), and it degrades to live-context observation when no transcript is reachable. This mirrors the methodology used for the plugin's original catalog harvest.

### Documentation
- **README** — added a *Keeping it up to date* section under Install: how to enable marketplace auto-update (`/plugin` → Marketplaces → select the marketplace → Enable auto-update) and why Claude Code leaves it off by default for third-party marketplaces (it never updates third-party code without consent). Docs-only; no change to shipped skills or commands.

## [0.2.0] — 2026-06-29

### Added
- **`deliberate-engineering-state`** — a consulted-only skill that owns a per-work-unit working-note, so process state (the phase sequence, current phase, chosen rituals, open pendings, and the decisions and why) survives across sessions. The router and Rule 6 delegate to it to rehydrate on resume and checkpoint as work proceeds; it delegates to a tracker or workflow engine when one already holds the work.

### Changed
- **Re-execution integrity** — re-invoking a review now re-executes from source by construction instead of reusing in-context conclusions: a recompute-on-reinvocation posture folded into Rule 3 (no new rule; the core stays at eight), fresh-context subagent dispatch as the depth-scaled default execution mode, evidence artifacts as the per-lens completion criterion, and world-derived scope resolution. The evidence-tied Output contract is now unified across the four phase selectors.
- **Override file relocated** — the personal override file moved from `~/.claude/deliberate-engineering-overrides.md` to `~/.claude/deliberate-engineering/overrides.md`, joining the common `~/.claude/deliberate-engineering/` namespace alongside the state working-note. Hard move, no migration shim.
- **README** — added the state skill to the inventory; fixed an internal contradiction where the prior-art line described `superpowers` as making the plugin "possible" while the install section (correctly) states the judgment layer degrades gracefully without it.

## [0.1.0] — 2026-06-27

### Added
- First public release. A standing-rules skill (eight rules), a front-door router (`:start`), four phase selectors backed by four read-on-demand catalogs (`:plan`, `:review`, `:verify`, `:debug`), one cross-cutting communication selector (`:communicate`), a personal override layer with an adopter capture tool (`:capture`), and an author contribution flow (`:contribute`, `:promote`). Includes the live-recalibration router step and the catalog lens-quality pass shipped on 2026-06-29 prior to versioned releases.

[0.3.0]: https://github.com/lucasfugisawa/deliberate-engineering/releases/tag/v0.3.0
[0.2.1]: https://github.com/lucasfugisawa/deliberate-engineering/releases/tag/v0.2.1
[0.2.0]: https://github.com/lucasfugisawa/deliberate-engineering/releases/tag/v0.2.0

<!-- 0.1.0 predates tagged releases (v0.2.0 is the first git tag), so it has no release link. -->

