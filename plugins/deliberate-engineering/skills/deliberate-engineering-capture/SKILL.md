---
name: deliberate-engineering-capture
description: "Use on demand to capture what you did this session into durable overrides. Observes deviations (you corrected/skipped a catalog lens or rule) and patterns (recurring practice the catalog lacks), discusses candidates, and on approval appends disable/modify/add entries to ~/.claude/deliberate-engineering-overrides.md. This is the adopter's write side — it grows YOUR personal override file. It is not the author contribution tools (contribute/promote), which propose lenses for the shared catalog. Stays silent unless invoked."
---

# Deliberate Engineering Capture

The adopter write side of the override layer. Where `deliberate-engineering-overrides` reads the personal override file and honors it at runtime, this skill helps you grow that file from what you actually did. It watches for two signals — deviations from the catalog (you skipped or corrected a lens/rule) and patterns beyond it (you brought a recurring practice the catalog lacks) — proposes override entries, and on approval appends them to `~/.claude/deliberate-engineering-overrides.md`.

## vs the override read side

`deliberate-engineering-overrides` is the **read side** — it consults the file, honors the overrides, and declares them. This skill is the **write side** — it proposes entries based on observed signals and appends approved entries to the file. The read side runs whenever a selector or the rules skill applies content; the write side runs on demand only. Different moments, different directions, same file.

## vs the author contribution tools

The `contribute` and `promote` tools are for growing the **shared catalog** — proposing a lens for inclusion in the plugin's shipped content. That is a product act with leak audit and review. This skill grows the **adopter's personal override file** — `~/.claude/deliberate-engineering-overrides.md` — which stays local and private. Opposite targets. The differentiator: This is the adopter's write side — it grows YOUR personal override file. It is not the author contribution tools (contribute/promote), which propose lenses for the shared catalog.

## On demand only

This skill never self-triggers. It runs only when invoked — via `/deliberate-engineering:capture` or an explicit natural-language request. Absence of invocation means total silence. It does not insert itself into every session, does not run as a background observer, does not propose overrides unprompted. The adopter decides when to make a session's practice durable; the skill does not decide for them.

## When to use

Use this skill when you want to make the practice from this session durable — turning what you did into an override that will apply in future sessions. Trigger it via `/deliberate-engineering:capture` or by asking explicitly (e.g., "capture what we did as an override" or "add this to my overrides"). If you never invoke it, it does nothing.

## What it observes

Two signals, both drawn from the current session:

1. **Deviations** — a catalog lens or standing rule was applicable, and you corrected it, skipped it, or contradicted it. The lens said one thing; you did another, with signs of intent (not a one-off accident). Candidate for `disable` if you rejected the lens outright, or `modify` if you used it with a recurring adjustment.

2. **Patterns** — a recurring practice or strategy you brought that the catalog lacks. Something you applied consistently, explained clearly, and that has the shape of a lens (a named strategy with a when-to-apply condition). Candidate for `add`.

What does NOT produce a signal: a behavior seen once with no sign of intent, or a deviation that has no clear addressable target. One-session noise is dropped; recurring practice with intent is elevated.

## Triage and mapping

For each observed signal, identify the addressable target and the operation:

- **Targets** use the canonical form: `review #N`, `verify #N`, `planning #N`, `debug #N`, `Rule N` for specific lenses/rules; or `add — <catalog>` for operator-authored strategies where catalog is `review`, `planning`, `verify`, `debug`, or `rules`.
- **Operations** are `disable`, `modify`, or `add`.

If a signal has no clear target (ambiguous lens number, or a practice that does not fit any catalog), ask rather than force a wrong number, or propose an `add` entry. Drop candidates with no clear target or that are one-session noise — this skill does NOT propose an override of something seen once without a sign of recurring intent.

## The conversation protocol

For each candidate, present:

1. The observed signal — e.g., "you skipped review #35 twice, both times noting that a separate simplification pass handles that."
2. The target and operation — e.g., "review #35 — disable."
3. The **exact markdown block** that would be appended to the override file, in the format the override read side expects.

A `disable` candidate looks like this — it removes a lens entirely:

> **Candidate:** review #35 — disable
> 
> **Signal:** You skipped lens #35 (simplification check) twice, both times noting that a separate pass handles simplification.
> 
> **Block to append:**
> ```markdown
> ## review #35 — disable
> 
> **Why:** We run a separate simplification pass after the deliberate review.
> ```
> 
> Approve this candidate, edit it, or reject it?

A `modify` candidate appends an annotation — the lens stays active, but you applied a recurring adjustment that you want read alongside the shipped content:

> **Candidate:** verify #N — modify
> 
> **Signal:** You applied lens #N consistently, but each time added a check for [specific constraint the shipped lens omits].
> 
> **Block to append:**
> ```markdown
> ## verify #N — modify
> 
> **Add:** The recurring adjustment you applied — read alongside the shipped lens, never replacing it.
> ```
> 
> Approve this candidate, edit it, or reject it?

An `add` candidate is a full operator-authored lens — a recurring practice you brought that the catalog lacks, now formalized as a lens for future sessions:

> **Candidate:** add — <catalog>
> 
> **Signal:** You consistently applied [strategy name] across [two or more contexts], with a clear when-to-apply condition and repeatable pattern.
> 
> **Block to append:**
> ```markdown
> ## add — <catalog>
> 
> **Name:** A short name for the strategy.
> 
> **When:** The situation in which this operator-authored lens applies.
> 
> **Apply:** What to do when it applies — the lens content itself.
> ```
> 
> Approve this candidate, edit it, or reject it?

**Recommend, never force.** The candidate is a proposal; the adopter decides. Present all candidates, let the adopter approve/edit/reject each. Do not append anything without approval.

## The append-only write

For each approved candidate, **append** the block to `~/.claude/deliberate-engineering-overrides.md`. If the file does not exist, create it with this header:

```markdown
# Deliberate Engineering Overrides

Personal overrides for the deliberate-engineering plugin. Each entry disables, modifies, or adds to the shipped catalog.

See: deliberate-engineering-overrides skill for the format and the read-side behavior.

---
```

Then append the approved block. **Never rewrite or reorder existing entries.** Append only.

On an address conflict — an entry already exists for the same target — do NOT edit the existing entry. Either offer a coexisting block with a different `**Add:**` note, or warn the adopter and ask what to do. The file is append-only; this skill never touches an existing entry.

On write failure (permissions, file lock, anything), do not fail silently. Show the block to the adopter and ask them to paste it manually into the file. Degrade gracefully; do not drop the work.

After appending, declare what was written: the target, the operation, and the file path.

## No candidates

If no deviation or pattern from this session is worth an override, say so plainly and write nothing. No forced candidates, no theater, no "let me create an override for completeness." Silence is the correct output when nothing rises to the level of durable preference. The skill's job is to recognize the signal, not to manufacture one.

## Output

Report:

1. The candidates shown — target, operation, and the signal that produced each.
2. Which candidates were approved, edited, or rejected.
3. What was appended — for each approved candidate, state the target, the operation, and confirm it was written to `~/.claude/deliberate-engineering-overrides.md`.
4. If no candidates were identified, state that explicitly.

The contract: the caller knows what was observed, what was discussed, and exactly what was written to the file (or that nothing was written).
