# Orchestration templates

The three contracts that carry a program, read on demand from `SKILL.md` when you author one, not loaded up front. Each skeleton **prescribes the fields, not the formatting**: the fields are the part that made real handoffs work, so keep them all; the headings, order, and prose are yours to adapt. Start flat and grow a structure only when a section actually overflows.

Two of these are per-dispatch (handoff, work report); the tracker is per-program and rewritten on every disposition. The orchestration session **generates** the mechanical fields from a live-state read at dispatch and hand-writes only the judgment fields (marked below); a worker fills the whole work report.

---

## 1. Handoff (outbound contract)

The orchestration session writes this; a fresh session executes from it holding nothing else. It must be resolvable on its own (Rule 9), and its binding premise must be frozen against a live-state read taken **at dispatch time**, not from the orchestration session's last-known snapshot (Rule 3, premise-freshness).

```markdown
# Handoff: <one-line unit title>

## Mandate & why        (author-filled: the judgment)
<what this unit is for, and why it is worth dispatching now>

## Premise freeze        (generated: a live read taken at dispatch)
- Repo / branch: <name> @ <SHA read now>
- Base / target: <PR #, base branch @ SHA, or "n/a">
- Any fact this work binds to: <value + where it was read>
- Read at: <timestamp>            # if the premise has since moved, re-issue before dispatch

## Scope: exact change
<the specific change to make, concretely: files, behavior, boundary>

## DO NOT / out of scope  (author-filled: the judgment)
- <what to leave untouched; adjacent work that is explicitly not this unit>
- <no outward or irreversible action; that returns to the operator (Rule 1)>

## Gates to run
<the exact build/test/lint/type commands that must pass, copy-pasteable>

## Verification steps
<how to confirm the change is correct at the source, not just that a tool exited 0>

## Required WORK REPORT format
<point at section 2 below, or inline the fields you require back>
```

---

## 2. Work report (inbound contract)

The worker writes this and returns it; then it is done. The orchestration session verifies it at source before trusting any line of it.

```markdown
# Work report: <unit title>

## New state
- Repo / branch: <name> @ <new SHA>
- PR / commits: <links or SHAs the orchestration session can fetch>

## What changed
<what was actually done, concretely>

## Gate & test evidence
<the commands run and their real output: not "tests pass" but the pass line>

## Decisions & judgment calls
<anything decided that the handoff left open, and why>

## Not done per dispatch
<anything in scope that was deliberately not done, and why: explicit, never silent>
```

---

## 3. Program tracker (+ recovery anchor)

One per program, the single source of truth `deliberate-engineering-state` delegates to. Rewritten on every disposition, with a read-back after the write (Rule 6). The recovery anchor at the top is what lets any fresh session re-instantiate the orchestration role, so keep it always-current.

```markdown
# Program: <name>

## Recovery anchor        (always-current: read this first on resume)
- Goal / definition of done: <one or two lines>
- Where things stand: <the one-paragraph state of the whole program>
- Next action: <the single next thing the orchestration session would do>
- Key locations: <tracker, handoffs/, reports/, the work repo(s) + branches>

## Operator queue          (top: what needs a human now)
- [ ] <dispatch to approve / outward action to trigger / decision to make>

## Streams                 (per-unit status rows)
| Unit | Shape (inline/session/subagent) | State (queued/in-flight/verifying/done) | Disposition | Evidence |
|------|--------------------------------|------------------------------------------|-------------|----------|
| <unit> | <shape> | <state> | <accept/reject/FUP/-> | <link to report/commit> |

## Done log                (bottom: chronological, append-only)
- <date> <unit>: <disposition>, <one-line why + commit ref>
```

The tracker self-audits on each disposition: before committing, re-read it and reconcile any stale row, date, or recovery-anchor line rather than letting drift accumulate silently. Scrub or gitignore any credential a handoff may have pulled in before committing, especially once the repo is synced.
