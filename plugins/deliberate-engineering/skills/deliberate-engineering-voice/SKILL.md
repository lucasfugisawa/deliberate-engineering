---
name: deliberate-engineering-voice
description: "Use when drafting or revising any communication that goes out in the operator's name to some other reader, whether or not it concerns engineering work. Examples, not an exhaustive list: a PR/MR title or description, a review comment or a reply to one, a work item title, description or comment, a chat message such as a DM or a channel post, an email, a calendar invite, a design doc or a comment on one, a post, an article, a personal note to someone outside work. Reads the operator's voice profile from ~/.claude/deliberate-engineering/voice/ and applies it as the surface layer, loading only core.md plus the register for the language the communication will be written in and the archetype for the artifact type. Consulted by communication-collaboration-selector after its lenses are chosen, and reachable on its own when no deliberate-engineering phase was ever entered. Stays silent when no profile directory exists. Do not load it for the agent's own replies to the operator: those follow the rules skill's authoring convention instead."
---

# Deliberate Engineering Voice

The deliberate layer of *sounding like yourself*. Where the communication selector ships generalizable judgment about what a message must accomplish, this skill applies operator-specific personalization about how that message sounds. It reads a personal voice profile, loads only the parts the artifact at hand needs, and applies them as the last layer over whatever the selector already decided.

## vs the communication selector

The selector decides **which lenses this artifact and this audience call for**: the case for the change rather than its changelog, invite rather than command, speak the reader's language, no unresolvable context. This skill decides **how this particular operator sounds** while doing that. Two different axes, deliberately kept in two skills.

Folding the profile into the selector would mix shipped, generalizable judgment with operator-specific content inside one skill, which is exactly the separation the override layer already established. The precedent is close enough to be worth naming: `deliberate-engineering-overrides` is a read-side skill, reads from `~/.claude/deliberate-engineering/`, is invoked by a one-line pointer from each selector, does nothing and says nothing when its file is absent, and declares itself when it fires. This skill is the same shape aimed at a different target. An adopter who understands one understands the other.

The boundary holds in both directions: the selector never reads the profile, and this skill never re-decides which lenses apply. It receives a message that has already been shaped for its reader and changes its surface.

## When to use

Two triggers ship with the skill, deliberately redundant, because a mechanism that exists and does not fire is the same as no mechanism. A third is operator-side and optional: the always-on block the README offers for a personal `CLAUDE.md` names this skill alongside the selector, so an operator who adopted it has a standing pointer as well.

1. **Consulted by the selector.** `communication-collaboration-selector` carries a one-line pointer: after applying the selected lenses, consult this skill. This is the path when the deliberate flow is running, whether the selector was reached through the router or invoked directly.
2. **By description.** Any request to draft, rewrite, tighten, translate, or shorten a communication that will go out in the operator's name, whether or not any deliberate-engineering phase was entered. The most common use is a one-off ("help me write this message"), which never touches the router, so the profile must not be hostage to the selector being invoked. Translate means carrying a communication of the operator's own into another language; rendering someone else's inbound message is a quotation, and falls under the exclusion below.

Not for text the operator will not sign: source code, configuration, machine-consumed structured output, or a quotation of someone else's words. A voice profile describes a person writing to other people.

Not for the agent's own messages to the operator either, and this one is worth naming, because inside a chat harness it is the easiest boundary to cross. Talking to the operator is governed by the rules skill's authoring convention: communicate the judgment rather than the mechanics, concise and in a human voice. That convention is not the operator's profile, and the two collide here. In every artifact this skill does cover, the operator is the author and someone else is the reader; in a reply to the operator that is inverted, and an agent that answers you in your own voice is a defect, not personalization.

## What loads, and when

Load only what the artifact needs. Progressive disclosure is the pattern the catalogs already use, and it is what makes the profile cheap enough to apply on every draft rather than only on ceremony.

Archetype names are the operator's own invention, so start by listing `archetypes/` to see what this profile actually carries: a directory listing, not a read. Match on the filename and open exactly one. If two names are both plausible, reading only their **When this applies** sections is enough to decide between them. Listing is cheap; opening every file to find the match is what the last bullet rules out.

- **`core.md`, always.** What holds regardless of language and artifact type.
- **`registers/<lang>.md`**, the one matching the language **the communication will be written in**, which is often not the language the request was written in. An operator who asks in one language for an artifact that ships in another is common, and defaulting to the language of the request silently produces the wrong register. When the two differ and the artifact does not settle it, ask which language it goes out in before drafting; one question is cheaper than a draft in the wrong register. If the profile has no register for that language, load none and say so.
- **`archetypes/<type>.md`**, the one matching the communication's type. One archetype, the closest match; a DM is not a design doc, and loading both blurs the two. When the artifact is a *comment on* something, match the archetype of the thing being commented on rather than the act of commenting: a comment on a design document belongs with design documents, not with code review, and the archetype for that document type is where its comment habits will have been recorded.
- **Never the whole directory.** Reading every archetype to write one message spends context on rules that do not apply and dilutes the ones that do.

`contract.md` in this directory describes the layout in full, including `chat-prompt.md`, which is never part of a drafting load.

Where the three files disagree, the more specific one describes the situation more closely: archetype refines register, register refines core.

## When no archetype matches

Load core plus the register, apply those, and **say so** in the declaration. Do not stretch a distant archetype over an artifact it was not written for: an article archetype applied to a one-line chat reply produces a worse draft than no archetype at all, because it imports length and structure habits that belong to a different act.

A missing archetype is a gap in the profile, not a failure of the draft. Naming it is how the operator finds out which one to write next.

## Precedence

**Explicit instruction > voice profile > default style.**

The order of application: the selector's lenses decide what the message must accomplish and how it is structured for its reader; operator overrides adjust those lenses; the voice profile applies last, over the result. Lenses decide substance, the profile decides surface.

- **An explicit instruction in the session wins.** "Keep this one formal", "no lowercase here", "match the tone of the thread I pasted": these beat the profile, following the same precedence the rules skill and the override layer already use. The profile is durable preference, not a mandate.
- **Where a lens and the profile genuinely conflict**, the lens wins on substance and the profile wins on surface. If a lens asks for a structure the profile bans (a handoff needs its state / done / remaining / risks / next skeleton and the profile bans headings), keep the structure the lens requires and render it in the profile's voice. Declare the conflict and how it was resolved.
- **On a commit message, repository convention wins on form.** The operator signs commit messages, so the exclusion ruler above puts them in scope, but they are also parsed by tooling and governed by repository convention, and no `commit` archetype exists. Where the two disagree, the convention decides the form (subject shape, prefix, casing, length) and the profile applies to body prose only.
- **The profile does not license breaking a standing rule.** It describes habits, not permissions; the human gate on outward-facing actions (Rule 1) and the resolvability bar on shipped artifacts (Rule 9) hold regardless of how the operator writes.

## Silent when absent

If `~/.claude/deliberate-engineering/voice/` does not exist, this skill does nothing and says nothing. Personalization is opt-in, exactly as override is.

An absent profile is not an error and mid-draft is not the moment to build one. If the operator asks how, the guided path is `deliberate-engineering-voice-build` (the `/deliberate-engineering:voice-build` command), which walks the build and resumes across sessions; `bootstrap.md` in this directory is the underlying method it runs, and `template/` is the skeleton.

## The declaration protocol

When the profile fires, state it in one factual line naming the files that were loaded. This is a receipt, not an acknowledgement: applying a voice profile changes the surface of a draft the operator is about to read and edit, so it is not a safety-relevant deviation and does not earn the weight of the override layer's elevated-autonomy note.

One receipt per loaded set is enough. It is worth giving on the first draft of a session, and again whenever the set changes: a different archetype, a fallback to core plus register, a lens conflict resolved. Later drafts on the same set need no repeat line. A receipt reprinted on every draft is the mechanics-narration the same authoring convention asks you to leave out, and low stakes is a reason to keep the disclosure light rather than a reason to repeat it.

- Normal: *"Voice profile applied: core + registers/en + archetypes/code-review."*
- No archetype match: *"Voice profile applied: core + registers/en. No archetype matched a calendar invite, so surface is core plus register only."*
- No register match: *"Voice profile applied: core + archetypes/email. No register for this language; core only on language-bound habits."*
- Lens conflict resolved: add one clause. *"...lens 7's handoff skeleton kept, rendered without headings per the profile."*

When the profile did not fire because the directory is absent, say nothing at all.

## Output

When the profile fired, report the one-line declaration alongside whatever the selector was already reporting, plus the conflict clause if one applied. When no profile directory exists, report nothing: this skill is silent by default and speaks only when it changed how something sounds.
