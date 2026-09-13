# Deliberate Engineering Multi-Host Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the same Deliberate Engineering methodology independently installable and command-invocable in Claude Code and Codex 0.154.

**Architecture:** Keep one plugin payload and one methodology source tree. Add host-specific manifests, marketplaces, and minimal paired command entry points; isolate personal storage and transcript extraction behind a shared consulted host-context workflow.

**Tech Stack:** Markdown skills/commands, JSON manifests, Python 3 standard-library validation, Bash host fixtures, Claude Code 2.1.247, Codex 0.154.

**Spec:** `docs/superpowers/specs/2026-09-12-multi-host-plugin-design.md`

## Global Constraints

- Preserve all 12 existing Claude command names and behavior.
- Codex runtime must not depend on `~/.claude`, `${CLAUDE_PLUGIN_ROOT}`, Claude caches, or Claude marketplace state.
- Shared methodology must have one source of truth. Host command adapters may differ only where the native invocation contracts require it.
- No agents or hooks are added without an evidenced need.
- Personal data never migrates across hosts automatically.
- Do not remove or reinstall the user's current Codex plugin until repository and isolated runtime validation pass.
- Do not commit, push, tag, or release without the operator's gate.

---

### Task 1: Executable multi-host contract

**Files:**
- Create: `scripts/check-host-compatibility.py`
- Create: `scripts/test-host-compatibility.py`
- Modify: `.github/workflows/consistency.yml`

**Interfaces:**
- Consumes: the repository tree and both hosts' JSON manifests.
- Produces: a zero-dependency validator with `check_repository(root: Path) -> list[str]` and fixture-tested host helpers.

- [x] Write tests that fail because native Codex metadata, host-context helpers, and Codex transcript extraction do not exist.
- [x] Run `python3 scripts/test-host-compatibility.py` and confirm failures name those missing contracts.
- [x] Implement the minimum validator/helper behavior and wire both checks into CI.
- [x] Run both host checks and all existing invariant suites.

### Task 2: Native host metadata over one payload

**Files:**
- Create: `.agents/plugins/marketplace.json`
- Create: `plugins/deliberate-engineering/.codex-plugin/plugin.json`
- Create: `plugins/deliberate-engineering/codex/commands/*/SKILL.md`
- Modify: `plugins/deliberate-engineering/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

**Interfaces:**
- Consumes: Codex 0.154's `.agents` marketplace and `.codex-plugin` loader contracts.
- Produces: native Codex discovery with both manifests pointing to shared `./skills/`, Claude Code pointing to `./commands/`, and Codex pointing to `./codex/commands/`, version `0.18.0`.

- [x] Add failing manifest-parity and shared-path fixture cases to the host compatibility suite.
- [x] Run the targeted tests and confirm the expected failures.
- [x] Add the Codex marketplace/plugin manifests and update Claude metadata version only.
- [x] Run the targeted tests, repository validator, and both Claude validators.

### Task 3: Host context and independent personal data

**Files:**
- Create: `plugins/deliberate-engineering/skills/deliberate-engineering-host-context/SKILL.md`
- Create: `plugins/deliberate-engineering/skills/deliberate-engineering-host-context/scripts/resolve-host-context.py`
- Create: `plugins/deliberate-engineering/skills/deliberate-engineering-host-context/scripts/select-codex-rollouts.py`
- Create: `plugins/deliberate-engineering/skills/deliberate-engineering-host-context/scripts/extract-operator-messages.py`
- Modify: path-sensitive skills and command `commands/capture.md`

**Interfaces:**
- Produces: a JSON host context (`host`, `data_root`, active/archive transcript roots, session id, thread store), a bounded Codex lineage manifest, and an extractor that emits NUL-delimited operator messages for `--host claude|codex`.
- Consumes: `CLAUDE_CODE_SESSION_ID`, `CODEX_THREAD_ID`, optional `CODEX_HOME`, and one host transcript file.

- [x] Add fixture tests for Claude/Codex root separation, missing identity, injected-message filtering, tool-result filtering, NUL record separation, bounded fork/revert lineage, byte offsets, archived compression, provenance rejection, and atomic output.
- [x] Run the targeted tests and confirm failures because the scripts are absent.
- [x] Implement the helpers and the smallest consulted skill contract.
- [x] Update capture, overrides, state, voice, and voice-build to resolve their personal paths through that contract.
- [x] Run targeted fixture tests, all invariant suites, and inspect every remaining Claude-specific occurrence for intent.

### Task 4: Multi-host documentation and release record

**Files:**
- Modify: `README.md`
- Modify: `docs/architecture-and-usage.md`
- Modify: `docs/guides/voice-build.md`
- Modify: `CONTRIBUTING.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Produces: separate verified Claude/Codex install, update, invocation, limitation, and uninstall instructions; architecture and contributor docs matching the two-adapter layout.

- [x] Update the human documentation without claiming slash-command support for `codex exec`.
- [x] Record `0.18.0` and the compatibility boundary in the changelog.
- [x] Run link/count/invariant tests and a stale-claim search.

### Task 5: Isolated and host runtime validation

**Files:**
- No production files expected; capture evidence in command output and the plan checkboxes.

**Interfaces:**
- Consumes: the completed checkout and installed `claude`/`codex` CLIs.
- Produces: native discovery/install evidence independent of the user's Claude installation.

- [x] Validate both manifests and marketplaces statically.
- [x] Install from the checkout into an isolated `CODEX_HOME` with no `.claude` content.
- [x] Verify the cache chose `.codex-plugin/plugin.json`, loaded all 12 native command skills, and preserved accompanying invocation context.
- [x] Exercise representative `start`, `plan`, `review`, `verify`, and `debug` commands through supported Codex surfaces.
- [x] Run the Claude validators and regression suites again.

### Task 6: Migrate the user's Codex installation

**Files:**
- Modify only Codex-managed plugin configuration/cache through `codex plugin` commands.
- Preserve: all `~/.claude` configuration, marketplace state, caches, and personal Deliberate Engineering data.

**Interfaces:**
- Produces: one enabled native Codex installation sourced from this checkout, with the previous compatibility-fallback install removed.

- [x] Re-inspect current plugin/marketplace paths and version immediately before mutation.
- [x] Remove only `deliberate-engineering@deliberate-engineering` through `codex plugin remove`.
- [x] Point the Codex marketplace at the validated checkout and reinstall through `codex plugin add`.
- [x] Verify native manifest selection, command inventory, independent data paths, and representative command behavior.
- [x] Confirm Claude Code still lists and validates its own installation.

### Task 7: Final review and verification

**Files:**
- Review every changed file; no new scope unless a defect blocks acceptance.

- [x] Run the review selector against the complete diff and fix material findings.
- [x] Run the verification selector against every acceptance claim using fresh commands.
- [x] Report architecture before/after, relevant tree, shared core, both adapters, evidence, and any publication/local-marketplace limitation.
