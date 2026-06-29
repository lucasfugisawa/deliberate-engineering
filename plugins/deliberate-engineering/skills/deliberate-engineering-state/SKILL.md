---
name: deliberate-engineering-state
description: "Use when work spans phases or sessions and process state must survive — the current phase and phase sequence, the chosen ceremony band and rituals, open pendings, and the decisions made and why. Reads and rehydrates a per-work-unit working-note at the start of a session or phase, and rewrites it at Rule 6 checkpoints with a changed-since-read safety check. Delegates to a tracker or superpowers when one is present; falls back to its own note otherwise. Consulted by the router and Rule 6, not invoked directly; stays silent when there is no state to record."
---

# Deliberate Engineering State

The deliberate layer of *not losing your place*. Where the selectors and the rules skill own the method — the selected phase sequence, the ceremony band, the rituals to apply — this skill owns the working-note that carries that state across sessions and phases. It mirrors how `deliberate-engineering-overrides` owns the override file: one skill encapsulates location, naming, schema, and concurrency for the note, so the router and Rule 6 can recommend recording without inventing a file format inline. The note is agent-driven: it reads like a shared whiteboard, not a machine-parseable artifact, and it is read and rewritten by the agent at the router's start and Rule 6's checkpoints.

## vs Rule 6 and the router live-note

Rule 6 sets the checkpoint posture — compact judiciously, and checkpoint before you do. The router recommends recording state when the work spans phases or sessions. But neither defines where to write the note or what schema it follows — they recommend the act, not the mechanism. This skill IS that mechanism. It does not replace Rule 6's posture; it gives it a concrete home. The founding "decide and delegate, don't invent a file format" principle is preserved: the router and Rule 6 still don't invent format inline — they delegate here, and THIS skill is the one place the format and location logic live.

## vs the tracker / superpowers (hybrid with fallback)

When a tracker or a `superpowers` plan is present, delegate to it and record state there — the tracker or superpowers task already owns the work-unit's durable home, so use it. Fall back to the owned working-note only when there is no durable tracker home. Always declare which path was taken in the visible output: if state was delegated to a tracker, say so; if the fallback note was used, say so. The hybrid-with-fallback stance mirrors the override layer's awareness protocol — the deviation from the default is never silent.

## When to use

This skill is consulted, not invoked directly. It is read at two lifecycle moments: (a) at session or phase start, to rehydrate the work-unit's current state (the current phase, the phase sequence, the chosen ceremony band and rituals, and open pendings), and (b) at Rule 6 checkpoints, to rewrite the live state and append new decisions. When work is a single-shot task with no multi-phase or multi-session state — a one-commit trivial fix — this skill stays silent; there is nothing to record. The router's recommendation to record drives whether this skill is consulted; it does not decide for itself whether to run.

## The working-note — location

The working-note lives in a project-local directory that is ensured-ignored by the VCS, with a fallback to a global directory when no project-local home is available. The resolution order:

1. **Project-local preferred**: `.deliberate/state/` in the repository root. Before writing here, ensure the `.deliberate/` directory is ignored by the VCS in use. The concretely-implemented case is git: run `git check-ignore .deliberate` to confirm it is ignored; if not, add `.deliberate/` to `.gitignore` and declare the addition in the visible output. The generic principle is "ignored by the VCS in use" — git is the implemented case; other VCSes would follow the same principle but are not concretely implemented in this skill. If the working directory is not under version control, skip to the fallback.

2. **Fallback when project-local is unavailable**: `~/.claude/deliberate-engineering/state/`. Use this when there is no repository root or the project-local ignore setup failed.

Always declare which location was chosen in the visible output when a note is read or written. If the fallback was used, state why — "no repository root" or "VCS ignore setup could not be verified."

## The working-note — naming and granularity

One note per work-unit, named by a world-derived identifier in preference order: the current branch name, the PR number, or the ticket key. The filename is `<identifier>.md` — for example, `feat-waive-logic.md`, `pr-1234.md`, or `IOPS-5158.md`. By construction, parallel sessions working on different work-units never collide — each has its own note. The rare collision case is two sessions working on the same work-unit simultaneously; the write gate (below) handles that.

The naming preference order reflects the durability of the identifier: a branch name is stable across the work-unit's life and is local, so it is preferred. A PR number is stable once the PR is created. A ticket key is stable when the ticket exists but may predate the local branch. Choose the first available identifier in that order.

## The schema — two blocks

The working-note has two blocks: **Live state** (rewritten on each checkpoint) and **Decision log** (append-only). The live state is the current snapshot; the decision log is the history of what was decided and why.

**Live state** (rewritten):
- Current phase (e.g., "verification")
- Phase sequence (e.g., "planning → contribution → verification")
- Ceremony band (e.g., "medium")
- Chosen rituals (e.g., "planning #8, #12, #19; verification #3, #7")
- Open pendings (e.g., "✗ PR description needs ticket link; ✗ DB migration test pending prod schema")

**Decision log** (append-only):
- Each entry: timestamp, the decision made, and the why (the constraint, risk, or context that drove it). Format: `- YYYY-MM-DD HH:MM — <decision>. Why: <reason>.`

Example:

```markdown
# Work-unit: feat-waive-logic

## Live state

- **Phase**: verification
- **Sequence**: planning → contribution → verification
- **Ceremony band**: medium
- **Rituals**: planning #8, #12, #19; contribution #4, #11; verification #3, #7
- **Pendings**:
  - ✗ PR description needs ticket link
  - ✗ DB migration test pending prod schema fetch

## Decision log

- 2026-06-28 14:32 — Skipped the feature-flag ritual (planning #15). Why: The waive logic change is gated by the existing `fee_waive_enabled` flag; no new flag needed.
- 2026-06-28 16:45 — Chose verification #7 (cross-service impact check) over #9 (load test). Why: The waive endpoint is low-traffic; schema change risk is higher than volume risk.
- 2026-06-29 09:15 — Added verification #12 (prod read-only smoke test) to the sequence. Why: The prod DB schema differs from staging (legacy column still present); read-only query confirms compatibility.
```

## Rehydrate (the read operation)

At session or phase start, read the work-unit's note (or the delegated tracker task). Return the current phase, the phase sequence, the ceremony band, the chosen rituals, and the open pendings. If no note exists for this work-unit, return nothing — the work is starting from scratch. When resuming work, re-read the note before reasoning about what to do next, rather than guessing from memory or prior context. The rehydrated state is the source of truth for where the work stands.

## Checkpoint (the write operation)

At Rule 6 checkpoints, rewrite the live state block and append new decisions to the decision log. Before writing, apply the changed-since-read check: compare the file's current hash or mtime to the value when it was last read. If the file changed since the last read, re-read it, reconcile the changes (merge pendings, preserve newer decisions), and declare the reconciliation in the visible output. Never overwrite blindly. After the check passes (or reconciliation completes), write the updated live state and append new decision-log entries with timestamps.

The changed-since-read check is detect-and-reconcile, not lock-based. There is no daemon and no lock file. If the check fails, pause, re-read, reconcile, announce, and proceed. The rare collision case (two sessions writing to the same work-unit simultaneously) is resolved by the agent merging the states, not by one session silently clobbering the other.

## Concurrency

The per-work-unit naming provides by-construction isolation: parallel sessions on different work-units never collide. The rare case — two sessions on the same work-unit — is handled by the write gate's changed-since-read check. There is no locking; the gate is detect-and-reconcile. If a concurrent write is detected, re-read the note, reconcile the changes (preserve newer decisions, merge pendings without duplicating), and declare the reconciliation. The goal is to avoid losing work, not to prevent the collision — the collision is rare enough that detect-and-reconcile is sufficient.

## The declaration protocol

Always declare in the visible output when behavior deviated from the default: (a) the fallback location was used rather than the project-local directory, and why; (b) state was delegated to a tracker or superpowers task rather than written to the owned note; (c) a concurrent change was detected and reconciled at checkpoint. Mirror the override layer's no-silent stance: when the skill's behavior deviates — whether by using a fallback location or by reconciling a collision — that deviation is declared, not hidden. Silence is not an option.

## Output

On **rehydrate**, report the recovered state: the current phase, the phase sequence, the ceremony band, the chosen rituals, and the open pendings. If no note existed, say so — "no prior state found; starting fresh." On **checkpoint**, report what was written (the updated live state fields) and what was appended (the new decision-log entries), and declare any deviation (fallback location used, delegated to tracker, collision reconciled). When there is no multi-phase or multi-session state to record — a single-shot task — stay silent. This skill speaks only when there is state to persist or recover.
