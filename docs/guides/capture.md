[deliberate-engineering](../../README.md) › [Guides](README.md) › **Capture**

# Capture: turn a session's corrections into your overrides

`/deliberate-engineering:capture` mines the session you just had for the ways your practice diverged from the plugin's shipped judgment, and turns the ones worth keeping into personal overrides: durable, addressable, applied automatically from then on. It is the write side of the personalization layer; the read side (`deliberate-engineering-overrides`) consults your file at runtime and declares whenever an override changed what the agent did.

## When to reach for it, and when not

Reach for it at the end of a session where you repeatedly corrected the agent: disabled a lens's advice, adjusted a rule, applied a practice the catalog lacks. It never fires on its own, and it never captures a one-off: a single correction without recurring intent is noise, and it says so. For judgment that generalizes beyond you (a lens *everyone* should have), the author flow in [CONTRIBUTING](../../CONTRIBUTING.md) is the right door; capture's target is your personal file, never the shipped catalog.

## The walkthrough

1. **[You]** Invoke `/deliberate-engineering:capture` (optionally focused: "just the review steps"), or simply ask: "add this to my overrides."
2. **[Agent]** Reads the full session transcript from disk (not its own memory of the conversation) and mines your messages for three kinds of signal: deviations from shipped lenses or rules, recurring patterns the catalog lacks, and ceremony-calibration preferences. Scope is this session unless you explicitly widen it, which you do by asking for it in those terms ("capture across all my sessions on this project"), and which then reads every session transcript across every worktree of that project. The pass fans out: one subagent per chunk of transcript, each handed a file of your own messages. And where the session identifier is not available it says so and falls back to observing the live context instead of reading from disk.
3. **[Agent]** Triages each signal to a concrete target and operation: `review #35: disable`, `verify #14: modify`, `add: planning`, addressed by the stable identifiers the whole plugin uses.
4. **[Agent → You]** Presents each candidate one at a time: the observed signal, the target, and the exact markdown block that would be appended, then asks: approve, edit, or reject? One candidate takes a different prompt: a change to a standing rule (`Rule N` or `add: rules`, judged by what the entry does rather than by how it is addressed) is named as a constitutional change, translated into what the agent will now do without asking, and confirmed in your own words rather than by approve/edit/reject. It also never *proposes* loosening the human gate or the read-only posture from something it merely observed; you have to ask for that in words.
5. **[You]** Decide per candidate. Editing is a first-class option, not just yes/no. Nothing is ever appended without your approval.
6. **[Agent]** Appends the approved blocks to `~/.claude/deliberate-engineering/overrides.md` (creating it if absent), strictly append-only, and reports what was written. If nothing rose to a durable preference, it says so and writes nothing.

From the next session on, the overrides layer reads that file automatically and your practice takes precedence over the shipped content, with every deviation declared out loud.

## Artifacts

| Artifact | Written by | Lives |
|---|---|---|
| Your override file (`disable` / `modify` / `add` blocks, addressed by stable ids) | Capture, append-only, on your approval | `~/.claude/deliberate-engineering/overrides.md`, local, never in a repo |

The exact override format and an example live in [Architecture & usage](../architecture-and-usage.md).

## Where to go next

- Make the agent's *writing* yours too → [Voice-build](voice-build.md)
- Ship a practice to everyone instead → [CONTRIBUTING](../../CONTRIBUTING.md)
- Back to [the guide index](README.md)
