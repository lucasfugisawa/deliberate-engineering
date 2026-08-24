---
name: deliberate-engineering-contribute
description: "Use on demand to turn generalizable engineering judgment from this session into clean catalog candidates. Observes review tactics, verification modes, planning disciplines, debugging strategies, and communication lenses, and more rarely a change to the standing rules themselves, extracts employer-neutral principles, and on approval deposits pending candidate files in candidates/ for later promotion, creating that directory and a README inside it on first use, in the plugin's own clone rather than in the project you are working on. This is the author/contributor write side: it proposes lenses for the shared catalog via the candidates/ queue. It is not the adopter capture skill, which grows your own personal override file. Stays silent unless invoked."
---

# Deliberate Engineering Contribute

The author write side of the judgment catalog. Where `deliberate-engineering-capture` grows the adopter's personal override file from what they did, this skill proposes generalizable lenses for the shared catalog. It observes engineering judgment worth catalog content (a review tactic, a verification mode, a planning discipline, a debugging strategy, a communication lens), extracts the employer-neutral principle, and on approval deposits a pending candidate file in the `candidates/` queue at the repo root. A sibling skill, `promote`, later drives approved candidates from the queue into the shipped catalog.

This is contributor tooling: it runs against a local clone of the `deliberate-engineering` plugin repository and writes to that repo's `candidates/` queue, not your own project. If you are tuning the plugin for your own work rather than contributing lenses back, use `deliberate-engineering-capture` and your overrides file instead.

## Boundaries

- **vs `deliberate-engineering-capture` (the adopter side)**: capture grows your *personal, private* override file from the deviations and patterns you brought; this proposes lenses for the *shared, shipped* catalog. Opposite write-targets.
- **vs `promote`**. This **captures**: it turns judgment into a clean candidate file in `candidates/`. `promote` **elevates**: leak-audit, classify, edit the catalog, route the lens from its selector. This skill writes candidates only: never the catalog, never a commit, PR, or push.
- **On demand only**: never self-triggers; runs only via `/deliberate-engineering:contribute` or an explicit request (e.g. "capture this as a catalog candidate," "propose this tactic for the catalog"). No invocation → total silence; it never proposes candidates unprompted.

## What it observes

Generalizable engineering judgment worth catalog content, **not** personal deviations or adopter-specific overrides (that is the capture skill's domain). What rises to catalog level:

1. **Review tactics**: a repeatable strategy for catching a class of defect, a forgotten integration, a deployment risk. Something that applies across codebases, expressed without the specific.

2. **Verification modes**: a test design, a staged-promotion pattern, a rollout discipline. A way of proving correctness or safety that is not tied to one employer's infrastructure.

3. **Planning disciplines**: a scoping heuristic, a dependency-sequencing rule, a migration backward-compatibility check. A judgment that shapes the approach before any code is written.

4. **Debugging strategies**: a diagnostic discipline, an incident-response tactic, a root-cause discipline. A recurring mode of reasoning under failure.

5. **Communication lenses**: a way of tuning a message to its reader and its artifact, a disclosure discipline, a handoff shape. A judgment about how engineering work is told, not about how it is built.

Rarely the judgment is not a lens at all but a change to the standing rules every session loads. That is contributable too, as a `rules` candidate, and it leaves the queue by a different route (see the format below).

What does **not** produce a candidate: a one-session tactic with no sign of reuse; a judgment so specific to one employer/service/vendor that generalization destroys the principle; or a personal preference (that is an override, not a catalog entry).

## Generalize at capture

The central act and the hard anti-leak rule. Extract the employer-neutral principle and **DISCARD** the specifics before writing. No real employer name, service name, person name, ticket ID, vendor name, org structure, incident number, or real quantity ever reaches disk. A candidate that cannot be generalized without reintroducing the specific is **DROPPED** at capture: this skill writes NO "half-clean" candidate. This is a hard DROP, never a best-effort sanitize.

Worked transformation (use a neutral phrasing, do not name a real service): "in payments service X, migration Y broke because Z" becomes "when migrating a schema with legacy readers, verify each reader before repointing." The specific is gone; the principle survives. The defense is generalization at capture, not scrubbing after the fact: if the principle can't stand without the specific, drop it and say so.

## The candidate file format

Each candidate is one markdown file with frontmatter and two prose sections. The format is frozen. The `promote` skill consumes it verbatim:

```markdown
---
target: review        # one of: review | verify | planning | debug | communication | rules
operation: add        # add | modify
modifies: null        # if modify, the lens number, e.g. 35 (the rule number when target is rules); else null
status: pending
date: 2026-06-27
---

# Feature-flag hygiene

**Principle (as it would enter the catalog):**
When a change is gated behind a flag, confirm the flag has an owner, a removal date, and a default-off safe state before merging.

**Rationale:**
Flags without an owner or a removal date accumulate as silent risk; a default-on flag turns an incomplete rollout into a live incident. This lens makes the hygiene explicit at review time.
```

Frontmatter carries `target` (review / verify / planning / debug / communication, or `rules` for a standing-rule change), `operation` (add / modify), `modifies` (the lens number if modify, the rule number when `target: rules` amends `Rule N`, else null), `status` (pending at capture), `date`. Body = the generalized principle + the rationale. All employer-neutral. All prose, no parser.

`target: rules` is the one target that names no catalog: it carries a change to the standing rules themselves, either a new rule (`add`) or an amendment to `Rule N` (`modify`, with the rule number in `modifies`). Write it in the same shape, but expect a different exit: `promote` routes every `rules` candidate down the structural path, a full design cycle (brainstorm, spec, plan, build), never the append-only catalog edit. A standing rule is constitutional content that every session loads, so the shape that suits a catalog lens is the wrong shape for it.

## The conversation protocol

For each candidate, present:

1. **The generalized principle**: the lens content as it would enter the catalog, fully employer-neutral. The specific is gone.
2. **Target catalog and operation**: which catalog (review / verify / planning / debug / communication), or `rules` for a standing-rule change, and whether this is `add` (a new lens or rule) or `modify` (an amendment to an existing one, with its number). For a `rules` candidate, say plainly that it is a standing-rule change bound for a full design cycle, not a catalog edit, so the author approves it knowing what it costs.
3. **Rationale**: why this judgment matters, in one or two sentences.
4. **Confirmation that generalization preserved the principle and lost the specific**: explicitly state this for each candidate, so the author knows the transformation was sound.

A worked candidate presentation:

> **Candidate 1:**
> 
> **Generalized principle:** When a change is gated behind a feature flag, confirm the flag has an owner, a removal date, and a default-off safe state before merging.
> 
> **Target:** review (add)
> 
> **Rationale:** Flags without an owner or a removal date accumulate as silent risk; a default-on flag turns an incomplete rollout into a live incident. This lens makes the hygiene explicit at review time.
> 
> **Confirmation:** Generalization preserved the principle (flag hygiene discipline) and discarded the specifics (the service name, the incident number, the vendor name).
> 
> Approve this candidate, edit it, or reject it?

**Recommend, never force.** The candidate is a proposal; the author decides. Present all candidates, let the author approve/edit/reject each. Do not write anything without approval.

## The gated write

For each approved candidate:

1. Generate a slug from the principle heading: lowercase, hyphens for spaces, otherwise alphanumeric.
2. Write the candidate file to `candidates/<slug>.md` at the root of your local checkout of the plugin repository, a path relative to that checkout, never an absolute path tied to one machine. That checkout is a clone of the plugin's own repository and not the project you are working in; without one, say so and stop rather than writing a queue into the wrong repository. If the directory does not exist, create it and add a `README.md` with a brief explanation of the queue.
3. On slug collision, differentiate the slug with a numeric suffix (e.g., `feature-flag-hygiene-2.md`), never overwrite.
4. **NEVER commit, NEVER open a PR, NEVER push.** This skill deposits candidates in the queue; it does not elevate them to the catalog. Promotion is a separate, gated step.

After writing, declare what was written: the slug, the file path, and the reminder that promotion is a separate step handled by the `promote` skill.

On write failure (permissions, file lock, anything), do not fail silently. Show the generalized candidate and the frontmatter block to the author and ask them to save it manually to `candidates/<slug>.md`. Degrade gracefully; do not drop the work.

## No candidates

If no judgment from this session is generalizable or worth catalog content, say so plainly and write nothing. No forced candidates, no theater, no "let me create a candidate for completeness." Silence is the correct output when nothing rises to the level of shared catalog. The skill's job is to recognize the signal and generalize it; if neither applies, write nothing.

## Output

Report:

1. The candidates shown: for each, the generalized principle, the target catalog, the operation, the rationale, and the confirmation that generalization preserved the principle and lost the specific.
2. Which candidates were approved, edited, or rejected.
3. What was written: for each approved candidate, state the slug, the file path (`candidates/<slug>.md`), and confirm that promotion is a separate gated step.
4. If no candidates were identified, state that explicitly.

The contract: the caller knows what judgment was observed, what principle was generalized, and exactly which candidate files were deposited in the queue (or that nothing was written).
