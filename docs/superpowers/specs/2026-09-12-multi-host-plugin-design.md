# Deliberate Engineering Multi-Host Plugin Design

## Status

Accepted for implementation on 2026-09-12. The operator's brief authorizes proceeding after reconnaissance unless a major product trade-off appears.

## Problem

Deliberate Engineering is a host-independent methodology packaged only with Claude Code metadata. Codex 0.154 can install that package through its Claude-compatibility fallback, but that is not a first-class Codex distribution: the repository has no native Codex marketplace or plugin manifest, personal data paths point at `~/.claude`, and capture only understands Claude transcripts.

## Verified host contracts

- Claude Code 2.1.247 discovers `.claude-plugin/marketplace.json`, then the plugin's `.claude-plugin/plugin.json`.
- Codex 0.154 searches marketplace manifests in this order: `.agents/plugins/marketplace.json`, `.agents/plugins/api_marketplace.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`.
- Codex 0.154 searches plugin manifests in this order: `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`.
- Codex legacy-format plugin commands are migrated at install time into namespaced command skills, but templates containing `$ARGUMENTS`, positional placeholders, interpolation braces, shell injection, or file mentions are silently skipped. Deliberate Engineering's Claude commands require `$ARGUMENTS`, so sharing those files would produce an installed plugin with no command entry points.
- Codex desktop and the interactive CLI expose enabled namespaced skills through `/skills` and support explicit `$plugin-name:skill-name` invocation. Codex 0.154 does not create direct `/plugin-name:skill-name` aliases. `codex exec` accepts the namespaced skill form in its prompt but has no interactive composer.
- Codex 0.154 supplies `CODEX_THREAD_ID` to shell commands in the verified desktop runtime. Local rollouts live below `$CODEX_HOME/sessions/` or `archived_sessions/` (default home `~/.codex`) and use Codex response-item JSONL, not Claude's project transcript schema. Reverts create a replacement rollout whose `history_base` points at a bounded retained prefix; older rollouts may exist only as `.jsonl.zst`.

## Compatibility matrix

| Capability | Claude Code 2.1.247 | Codex 0.154 | Shared core | Adapter |
|---|---|---|---|---|
| Skills, selectors, catalogs, rules | Native skills | Native skills | Yes | No |
| Command discovery | `commands/*.md` as `/deliberate-engineering:<command>` | Namespaced command skills through `/skills` or `$deliberate-engineering:<command>` | Workflow target and semantics | Yes, thin entry points |
| Command arguments | `$ARGUMENTS` template | Accompanying user text | The target request | Yes |
| Marketplace | `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json` | No | Yes |
| Plugin manifest | `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json` | Both point at `skills/` | Yes |
| Personal data | `~/.claude/deliberate-engineering/` | `$CODEX_HOME/deliberate-engineering/` or `~/.codex/deliberate-engineering/` | File contracts | Host-context resolver |
| Session capture | Claude project transcript JSONL | Bounded active-root lineage from Codex's thread store, across active/archive and plain/compressed storage | Mining and approval workflow | Host-context selector and extractor |
| Agents | None | None | Not required | No |
| Hooks | None | None | Not required | No |

## Target architecture

The single payload remains `plugins/deliberate-engineering/`:

- `skills/` contains the shared methodology, selectors, catalogs, rules, workflows, templates, and one consulted host-context skill.
- `commands/` contains the 12 existing thin Claude Code entry points, including `$ARGUMENTS`.
- `codex/commands/` contains 12 minimal native Codex skill entry points with the same names and shared workflow targets. Accompanying prompt text carries arguments natively.
- `.claude-plugin/plugin.json` is the Claude Code adapter.
- `.codex-plugin/plugin.json` is the Codex adapter.
- the repository-level `.claude-plugin/marketplace.json` remains the Claude Code marketplace.
- the repository-level `.agents/plugins/marketplace.json` is the Codex marketplace.

The adapters select host-native metadata and runtime locations. They do not duplicate the methodology.

## Host context contract

A consulted `deliberate-engineering-host-context` skill resolves a host before any personal data or transcript access:

| Host | Personal data root | Current-session transcript |
|---|---|---|
| Claude Code | `~/.claude/deliberate-engineering/` | `CLAUDE_CODE_SESSION_ID` below `~/.claude/projects/` |
| Codex | `$CODEX_HOME/deliberate-engineering/` when set, otherwise `~/.codex/deliberate-engineering/` | `CODEX_THREAD_ID` resolved through the current `state_*.sqlite` pointer; bounded `history_base` segments constrained below the corresponding `sessions/` and `archived_sessions/` directories |

No host automatically reads the other host's personal root. Cross-host migration is an explicit user operation, never a runtime fallback. Project-local `.deliberate/state/` remains shared because it belongs to the work unit, not a host installation. Host-private directories use mode `0700`, files use `0600`, and a host-local target inside a repository is refused.

The host-context skill is consulted by the override, state, voice, voice-build, and capture workflows. Capture retains one shared analysis/approval flow but branches only for transcript discovery and JSONL filtering. The Codex branch validates both ordinal and decoded-byte bounds so reverted turns do not re-enter the corpus, requires structural `user.text` provenance, validates every selected thread before emitting any output, and fails the whole extraction when older rollouts lack that provenance. Compressed history uses the external `zstd` decoder and degrades explicitly when it is unavailable.

## Compatibility and scope

- Existing Claude command names and behavior remain unchanged.
- Existing Claude personal data stays at `~/.claude/deliberate-engineering/`; nothing migrates or deletes it.
- Codex starts with an independent personal data root. Optional manual copying may be documented, but is not performed automatically.
- No agents or hooks are added: the methodology does not currently require host-specific versions of either.
- The native Codex adapter targets the verified installed Codex 0.154 contract. The repository does not add a root Agent Plugins `plugin.json`; this release's Agent Plugins format neither accepts a custom skills path without an extension nor migrates commands. The `.codex-plugin` adapter can declare both the shared skill root and Codex command-skill root directly.

## Validation

Automated validation must prove:

1. both marketplace and plugin manifests parse and agree on name/version;
2. both host manifests resolve to the same shared methodology directory and their own thin command adapter directory;
3. every Claude and Codex command name is paired, invokes the same distinct shared skill, and the Codex adapter contains no unsupported template interpolation;
4. Codex-specific metadata contains no Claude runtime dependency;
5. host context resolves distinct data roots, active/archive transcript locations, and the active thread store;
6. host transcript fixtures produce the same NUL-delimited operator-message contract, including bounded user-fork and revert lineages, byte-offset validation, compressed archived rollouts, provenance rejection, and no partial output on failure;
7. all existing repository invariants and Claude validators remain green.

Runtime validation must use an isolated Codex home before modifying the user's installation, then validate native discovery and representative command execution in the real Codex installation. Local uninstall/reinstall happens only after repository validation is green.

## Release

This is a backward-compatible feature release: version `0.18.0`. Publishing (commit, push, tag, release) remains behind the operator's gate. A local checkout marketplace may be used for native installation validation before publication.
