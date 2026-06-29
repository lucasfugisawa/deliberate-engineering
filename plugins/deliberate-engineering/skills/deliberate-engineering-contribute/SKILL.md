---
name: deliberate-engineering-contribute
description: "Use on demand to turn generalizable engineering judgment from this session into clean catalog candidates. Observes review tactics, verification modes, planning disciplines, and debugging strategies, extracts employer-neutral principles, and on approval deposits pending candidate files in candidates/ for later promotion. This is the author/contributor write side — it proposes lenses for the shared catalog via the candidates/ queue. It is not the adopter capture skill, which grows your own personal override file. Stays silent unless invoked."
---

# Deliberate Engineering Contribute

The author write side of the judgment catalog. Where `deliberate-engineering-capture` grows the adopter's personal override file from what they did, this skill proposes generalizable lenses for the shared catalog. It observes engineering judgment worth catalog content — a review tactic, a verification mode, a planning discipline, a debugging strategy — extracts the employer-neutral principle, and on approval deposits a pending candidate file in the `candidates/` queue at the repo root. A sibling skill, `promote`, later drives approved candidates from the queue into the shipped catalog.

This is contributor tooling: it runs against a local clone of the `deliberate-engineering` plugin repository and writes to that repo's `candidates/` queue — not your own project. If you are tuning the plugin for your own work rather than contributing lenses back, use `deliberate-engineering-capture` and your overrides file instead.

## vs the adopter capture skill

`deliberate-engineering-capture` is for the **adopter** — it grows `~/.claude/deliberate-engineering-overrides.md`, your personal override file, from deviations and patterns you brought to this session. That file stays local and private. This skill is for the **author** — it proposes lenses for the shared catalog, which ships in the public plugin. Opposite write-targets. The differentiator: This is the author/contributor write side — it proposes lenses for the shared catalog via the candidates/ queue. It is not the adopter capture skill, which grows your own personal override file.

## vs the promote skill

This skill **captures** — it turns generalizable judgment into a clean candidate file and deposits it in `candidates/`. The `promote` skill **elevates** — it takes a candidate from the queue, runs the gated promotion (leak audit, catalog fit, review), and moves it into the shipped catalog. Two steps, two skills, one gated pipeline. This skill writes candidates; it never writes the catalog, never commits, never opens a PR, never pushes.

## On demand only

This skill never self-triggers. It runs only when invoked — via `/deliberate-engineering:contribute` or an explicit natural-language request. Absence of invocation means total silence. It does not insert itself into every session, does not run as a background observer, does not propose candidates unprompted. The author decides when session judgment is worth catalog content; the skill does not decide for them.

## When to use

Use this skill when you want to turn generalizable engineering judgment from this session into a candidate for the shared catalog. Trigger it via `/deliberate-engineering:contribute` or by asking explicitly (e.g., "capture this as a catalog candidate" or "propose this tactic for the catalog"). If you never invoke it, it does nothing.

## What it observes

Generalizable engineering judgment worth catalog content — **not** personal deviations or adopter-specific overrides (that is the capture skill's domain). What rises to catalog level:

1. **Review tactics** — a repeatable strategy for catching a class of defect, a forgotten integration, a deployment risk. Something that applies across codebases, expressed without the specific.

2. **Verification modes** — a test design, a staged-promotion pattern, a rollout discipline. A way of proving correctness or safety that is not tied to one employer's infrastructure.

3. **Planning disciplines** — a scoping heuristic, a dependency-sequencing rule, a migration backward-compatibility check. A judgment that shapes the approach before any code is written.

4. **Debugging strategies** — a diagnostic discipline, an incident-response tactic, a root-cause discipline. A recurring mode of reasoning under failure.

What does **not** produce a candidate: a one-session tactic with no sign of reuse; a judgment so specific to one employer/service/vendor that generalization destroys the principle; or a personal preference (that is an override, not a catalog entry).

## Generalize at capture

The central act and the hard anti-leak rule. Extract the employer-neutral principle and **DISCARD** the specifics before writing. No real employer name, service name, person name, ticket ID, vendor name, org structure, incident number, or real quantity ever reaches disk. A candidate that cannot be generalized without reintroducing the specific is **DROPPED** at capture — this skill writes NO "half-clean" candidate. This is a hard DROP, never a best-effort sanitize.

Worked transformation (use a neutral phrasing — do not name a real service): "in payments service X, migration Y broke because Z" becomes "when migrating a schema with legacy readers, verify each reader before repointing." The specific is gone; the principle survives.

The primary anti-leak defense is generalization at capture, not scrubbing after the fact. If the principle cannot stand without the specific, it is not catalog material — drop it and say so.

## The candidate file format

Each candidate is one markdown file with frontmatter and two prose sections. The format is frozen — the `promote` skill consumes it verbatim:

```markdown
---
target: review        # one of: review | verify | planning | debug
operation: add        # add | modify
modifies: null        # if operation is modify, the lens number, e.g. 35; else null
status: pending
date: 2026-06-27
---

# Feature-flag hygiene

**Principle (as it would enter the catalog):**
When a change is gated behind a flag, confirm the flag has an owner, a removal date, and a default-off safe state before merging.

**Rationale:**
Flags without an owner or a removal date accumulate as silent risk; a default-on flag turns an incomplete rollout into a live incident. This lens makes the hygiene explicit at review time.
```

Frontmatter carries `target` (review / verify / planning / debug), `operation` (add / modify), `modifies` (lens number if modify, else null), `status` (pending at capture), `date`. Body = the generalized principle + the rationale. All employer-neutral. All prose — no parser.

## The conversation protocol

For each candidate, present:

1. **The generalized principle** — the lens content as it would enter the catalog, fully employer-neutral. The specific is gone.
2. **Target catalog and operation** — which catalog (review / verify / planning / debug) and whether this is `add` (a new lens) or `modify` (an amendment to an existing lens, with the lens number).
3. **Rationale** — why this judgment matters, in one or two sentences.
4. **Confirmation that generalization preserved the principle and lost the specific** — explicitly state this for each candidate, so the author knows the transformation was sound.

A worked candidate presentation:

> **Candidate 1:**
> 
> **Generalized principle:** When a change is gated behind a feature flag, confirm the flag has an owner, a removal date, and a default-off safe state before merging.
> 
> **Target:** review — add
> 
> **Rationale:** Flags without an owner or a removal date accumulate as silent risk; a default-on flag turns an incomplete rollout into a live incident. This lens makes the hygiene explicit at review time.
> 
> **Confirmation:** Generalization preserved the principle (flag hygiene discipline) and discarded the specifics (the service name, the incident number, the vendor name).
> 
> Approve this candidate, edit it, or reject it?

**Recommend, never force.** The candidate is a proposal; the author decides. Present all candidates, let the author approve/edit/reject each. Do not write anything without approval.

## The gated write

For each approved candidate:

1. Generate a slug from the principle heading — lowercase, hyphens for spaces, otherwise alphanumeric.
2. Write the candidate file to `candidates/<slug>.md` at the root of your local checkout of the plugin repository — a path relative to that checkout, never an absolute path tied to one machine. If the directory does not exist, create it and add a `README.md` with a brief explanation of the queue.
3. On slug collision, differentiate the slug with a numeric suffix (e.g., `feature-flag-hygiene-2.md`) — never overwrite.
4. **NEVER commit, NEVER open a PR, NEVER push.** This skill deposits candidates in the queue; it does not elevate them to the catalog. Promotion is a separate, gated step.

After writing, declare what was written: the slug, the file path, and the reminder that promotion is a separate step handled by the `promote` skill.

On write failure (permissions, file lock, anything), do not fail silently. Show the generalized candidate and the frontmatter block to the author and ask them to save it manually to `candidates/<slug>.md`. Degrade gracefully; do not drop the work.

## No candidates

If no judgment from this session is generalizable or worth catalog content, say so plainly and write nothing. No forced candidates, no theater, no "let me create a candidate for completeness." Silence is the correct output when nothing rises to the level of shared catalog. The skill's job is to recognize the signal and generalize it; if neither applies, write nothing.

## Output

Report:

1. The candidates shown — for each, the generalized principle, the target catalog, the operation, the rationale, and the confirmation that generalization preserved the principle and lost the specific.
2. Which candidates were approved, edited, or rejected.
3. What was written — for each approved candidate, state the slug, the file path (`candidates/<slug>.md`), and confirm that promotion is a separate gated step.
4. If no candidates were identified, state that explicitly.

The contract: the caller knows what judgment was observed, what principle was generalized, and exactly which candidate files were deposited in the queue (or that nothing was written).
