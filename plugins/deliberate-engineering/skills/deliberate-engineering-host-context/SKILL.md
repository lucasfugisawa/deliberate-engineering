---
name: deliberate-engineering-host-context
description: Use when a Deliberate Engineering workflow needs host-local personal data, state, voice files, overrides, or the current session transcript in Claude Code or Codex.
---

# Deliberate Engineering Host Context

Resolve the host before reading or writing host-local data. Run `python3 scripts/resolve-host-context.py --host auto` when the runtime identity is unambiguous, or pass `claude` or `codex` explicitly when the host is already known. Parse its single JSON object as data; never turn output into shell code.

## Contract

| Host | Personal data root | Transcript roots | Session identity | Active thread store |
|---|---|---|---|---|
| Claude Code | `$HOME/.claude/deliberate-engineering` | `$HOME/.claude/projects` | `CLAUDE_CODE_SESSION_ID` | none |
| Codex | `${CODEX_HOME:-$HOME/.codex}/deliberate-engineering` | `${CODEX_HOME:-$HOME/.codex}/sessions` and `archived_sessions` | `CODEX_THREAD_ID` | highest numbered `state_*.sqlite` below the same Codex home, when present |

The resolver returns `host`, `data_root`, `transcript_root`, `archive_root` (Codex only), `session_id`, and `thread_store`. Roots are canonical absolute paths, environment values with control characters are rejected, and automatic detection fails rather than guessing when identity is absent or ambiguous. An explicit host may resolve personal data without a session identity; capture additionally requires one.

Never fall back from one host's personal root to the other. A missing Codex file means absent in Codex, not "look under `~/.claude`". Copying personal data between hosts is an explicit operator migration, never runtime discovery.

Project-local `.deliberate/state/` is host-independent and remains preferred when the state workflow can prove it is ignored by version control.

For Codex session capture, use `scripts/select-codex-rollouts.py` with the returned active root, archive root, and thread store, writing its JSON lineage manifest to a private scratch file. It follows the active rollout pointer, recursively reconstructs `history_base` after revert without restoring reverted turns, validates both ordinal and byte-offset boundaries, resolves plain or `.jsonl.zst` representations across active and archived storage, and accepts only operator-owned root threads. Reading compressed history requires the `zstd` executable; its absence is an explicit capture degradation, never a silent omission. Then run `scripts/extract-operator-messages.py --host codex --transcript-root <root> --archive-root <archive-root> --lineage-manifest <manifest>`. The extractor independently validates the complete bounded lineage before emitting anything, rejects off-root and symlink paths, and emits NUL-delimited operator messages. Codex messages pass only when structural provenance marks them as `user.text`. Older rollouts that predate this provenance are structurally unable to distinguish operator text from generated continuations, so the entire extraction fails closed and capture declares Degradation instead of contaminating personal overrides.

## Private file modes

Before creating host-local personal data, set a restrictive creation mask (`umask 077`), create directories as `0700`, and create files as `0600`. Check existing target permissions before writing; correct group/world access only for the exact Deliberate Engineering directory or file being used, and report a correction. Refuse a host-local write if the resolved target is inside a repository. These rules apply to overrides, fallback state, the voice profile, and the voice-build corpus.

## Failure behavior

Unreadable and absent are distinct. Report an unreadable host resource. For an absent opt-in file, remain silent as that file's owning workflow specifies. When a session identity or transcript cannot be resolved, the capture workflow degrades to the live context and says so.
