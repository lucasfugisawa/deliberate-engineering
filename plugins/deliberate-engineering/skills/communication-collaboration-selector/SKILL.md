---
name: communication-collaboration-selector
description: "Use when producing a communication around engineering work: a PR/MR title or description, a review comment or a reply to one, a work item (ticket title, description, or comment), a chat message to a colleague (a DM or a channel post), a message to a stakeholder, an email, a calendar invite, a design doc or a comment on one, a handoff, or a writeup presenting alternatives. Classifies the communication by audience and artifact, then selects and applies the matching lenses from the catalog so the message is tuned to its reader and artifact instead of generic. This is the substance layer and it runs FIRST: it decides what the message must accomplish, and only then consults `deliberate-engineering-voice`, which shapes how it sounds. Cross-cutting: consult it from any phase; it is not a phase itself. On a multi-phase or multi-session work unit it writes a short live note through `deliberate-engineering-state`, which lands in the repository under `.deliberate/state/` (and may add that path to `.gitignore`) or under `~/.claude/` when it cannot."
---

# Communication & Collaboration Selector

The deliberate layer of *how you communicate around the work*. Engineering is not only inward (code, systems, process) but also outward: the PR you open, the review comment you leave, the way you explain a decision to a stakeholder. This skill decides *which communication lenses THIS artifact and audience call for*, and applies them, so the message is tuned to its reader, not a generic dump.

It is **cross-cutting, not a phase.** Each phase selector (plan / review / verify / debug-operate) classifies engineering work on the axes proper to its own phase. This one classifies on a different pair entirely: what selects a lens here is **which artifact + which audience.** The ruler the whole plugin shares still reaches this work, through the weight of the subject the artifact carries (Step 1, axis 2), but the axis names are this selector's own. Consult it from *within* any phase the moment the next thing you produce is a communication.

The reference for every lens cited below is `catalog.md` in this directory (a handful of lenses + a composition note). This catalog is the small one and it is flat, with no Parts: you scan every lens's `**Tags:**` line to match artifact and audience, then read only the bodies you selected. Progressive disclosure applies to the bodies, not to the tag scan.

## When to use

- When writing a PR/MR description, a review comment, a commit message meant for humans, a work item (ticket title, description, or comment), a design doc or a comment on one, an RFC, an email, a calendar invite, or a message to a stakeholder.
- When presenting alternatives or a recommendation to anyone, including the operator.
- Whenever a communication will cross an audience boundary (engineer → product, team → outside-the-team).

## When NOT to pile on

This is calibration, not always-more. A one-line note whose every reference the reader can already resolve needs no ceremony. When you deliberately keep it light, **say so**: a stated light-touch decision is calibration; silence is not.

## Scope and re-derivation

Resolve the artifact and its reader from the **world**, never from conversation memory. What a PR description says the change does comes from the diff, the branch, or the ticket, not from what the session remembers doing; the reader comes from the review thread, the assignee, or the channel, not from a guess about who cares. On re-invocation, re-derive those facts from the same sources rather than relaying the earlier draft (Rule 3): a recalled "here is what this change does" is a memory artifact, and this artifact is outward-facing, so the error ships.

## Step 1: Classify on two axes: audience and artifact

1. **Audience**: who reads this? **code-agent** (another agent or tool consuming structured instruction), **engineering** (a technical peer, including the operator), **product**, or **business**. If the reader fits none of these cleanly, **ask the operator** which register fits rather than guessing, with your pick embedded in the question (Rule 4), e.g. "I'd write this for an engineering reader. Confirm?" (naming the edge of what you know beats fabricating it).
2. **Artifact**: what communication are you producing? A PR/MR description, a review comment, a design doc, an RFC, a stakeholder message, a handoff. The artifact carries the **weight of the underlying subject**: communicating an irreversible, high-risk deploy plan is a heavier artifact than a typo note, and deserves more depth.

Audience sets the *register and vocabulary*; artifact sets *which lenses and how much weight*.

## Step 2: Select lenses from the catalog

The map below governs the selection: find your artifact in it and read only the lenses it names. The catalog's `**Tags:**` lines are the reverse index, for finding a lens when your artifact is not in the map, and they are deliberately broad on the two register lenses (4 and 5), which apply to almost everything and are therefore selected by the conditions below rather than by tag match.

- **Writing a PR/MR description** → lens 1 (the case, not the changelog); add lens 2 (smallest reviewable unit / stacking) when deciding how to slice the work.
- **Leaving a review comment, or replying to one** → lens 3 (invite, don't command), whose value peaks exactly where you disagree; add lens 6 when the reply weighs alternatives.
- **Any reader who is not a same-context peer** → lens 4 (speak the reader's language), the register modulator for everything else.
- **Any artifact whose reader lacks your planning context, including a PR read by a teammate** → lens 5 (no unresolvable context).
- **Presenting options or a recommendation** → lens 6 (expose the reasoning), phrased per lens 4.
- **Writing a handoff, status update, or working note** → lens 7 (the durable handoff, written so the next reader picks it up cold: state → done → remaining → risks → next).
- **Any other communication** (a commit message for humans, a design doc, an RFC, a work item, a chat message, an email, a calendar invite, a stakeholder message) → lens 4 is the floor; add lens 5 if the reader lacks your planning context, lens 6 if it weighs alternatives, and lens 7 if the reader has to pick the thread up cold.

**What the catalog supplies, and what it does not.** For a PR description and a handoff, a lens hands you a skeleton: what the message must contain and in what order. For everything else in that last row, the catalog supplies **register and resolvability, not substance**: it decides how the message reads and whether the reader can resolve every reference, and the content comes from the work, not from a lens. Say so when you apply it, so a thin selection reads as a deliberate floor rather than as a full pass.

**Entering here directly.** These lenses are the same whether you were consulted from inside a phase or called on your own, but two things a phase would have carried do not come with a direct call, so carry them here. The nine standing rules in `deliberate-engineering-rules` hold regardless, including the human gate on anything irreversible or outward-facing, which for this skill is the send. And when the communication belongs to work that spans phases or sessions, write your place at each checkpoint through `deliberate-engineering-state` (Rule 6), so a compaction or a new session resumes from what happened rather than from recall.

**Operator overrides.** Before applying the selected lenses, consult `deliberate-engineering-overrides`: honor any override on a lens you selected (disable / modify), and ask it for any operator-authored `add:` entry for this catalog, which carries no shipped number and so is invisible to a lookup keyed on your selection. Declare every deviation in the Output.

**Operator voice.** After applying the selected lenses, when the artifact is going to a human reader other than the operator, consult `deliberate-engineering-voice`. Not for the **code-agent** audience: structured output consumed by a tool is outside that skill's scope by its own terms, and a voice profile applied to it would corrupt the format. For every other reader, consult it **by invoking the skill, not by reading the profile directly**: its loading contract, its fallback states and its declaration protocol live in the skill, and reaching past it to the files applies the profile without the rules that govern it. Then: if a voice profile is present, apply it as the surface layer (core + register + archetype), and name the files loaded in the Output. A reply to the operator is outside that scope, including when the reply presents options (lens 6); how the agent talks to the operator follows the rules skill's authoring convention, not the operator's profile.

## Step 3: Coexistence and precedence

When other engines are present (a PR-description generator, commit-message tooling, a feature-development flow's PR step), **THIS skill decides what the artifact and its reader need** and may invoke them as *tactics*. It orchestrates; it never requires removing or disabling any of them. Where a present tool already owns the ground for a selected lens, delegate to it and note the delegation rather than duplicating the pass.

Precedence inside this skill runs in one order: the lenses set what the message must accomplish, an operator override adjusts a selected lens where one applies, and the voice profile shapes the surface last. A profile never licenses dropping a lens or breaking a standing rule.

## Step 4: Apply, stop at the gate, and output

1. **Apply** the selected lenses to the communication, then the voice profile as the surface layer if one is present and the reader is human (Step 2).
2. **Stop at the gate.** Most of what this selector produces is outward-facing, which is where Rule 1 lives: a PR description, a review comment, a ticket comment, a DM, a channel post, an email, a calendar invite. Draft it fully, **name the exact target** (which PR, which thread, which channel, which recipient), and stop. Posting, sending and commenting are the operator's to trigger, exactly as a merge or a deploy is. A message is easier to send than a deploy and just as impossible to unsend, which is why the gate is restated here rather than left to the constitution alone.
3. **Report**, briefly: the classification (audience + artifact), the lenses selected and why, anything deliberately skipped and why, whether the catalog supplied substance or only register and resolvability, any delegation to a present tool (Step 3), the voice files loaded or the reason none were, and, when you presented alternatives, the rationale exposed for critique (lens 6).
