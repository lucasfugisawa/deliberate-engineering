---
name: communication-collaboration-selector
description: "Use when producing a communication around engineering work — a PR/MR description, a review comment, a message to a stakeholder, a handoff, or a writeup presenting alternatives. Classifies the communication by audience and artifact, then selects and applies the matching lenses from the catalog so the message is tuned to its reader and artifact instead of generic. Cross-cutting: consult it from any phase; it is not a phase itself."
---

# Communication & Collaboration Selector

The deliberate layer of *how you communicate around the work*. Engineering is not only inward — code, systems, process — but also outward: the PR you open, the review comment you leave, the way you explain a decision to a stakeholder. This skill decides *which communication lenses THIS artifact and audience call for* — and applies them — so the message is tuned to its reader, not a generic dump.

It is **cross-cutting, not a phase.** The four phase selectors (plan / review / verify / debug-operate) classify engineering work by the four canonical axes. Communication does not classify by those axes — what selects a lens here is **which artifact + which audience.** So this selector has its own two-axis classification, and you consult it from *within* any phase the moment the next thing you produce is a communication.

The reference for every lens cited below is `catalog.md` in this directory (six lenses + a composition note). Read **only** the sections you select — progressive disclosure, not the whole file.

## When to use

- When writing a PR/MR description, a review comment, a commit message meant for humans, a design doc, an RFC, or a message to a stakeholder.
- When presenting alternatives or a recommendation to anyone — including the operator.
- Whenever a communication will cross an audience boundary (engineer → product, team → outside-the-team).

## When NOT to pile on

This is calibration, not always-more. A one-line note to a peer with equal context, or an internal comment among engineers who share the vocabulary, needs no ceremony. When you deliberately keep it light, **say so** — a stated light-touch decision is calibration; silence is not.

## Step 1 — Classify on two axes: audience and artifact

1. **Audience** — who reads this? **code-agent** (another agent or tool consuming structured instruction), **engineering** (a technical peer, including the operator), **product**, or **business**. If the reader fits none of these cleanly, **ask the operator** which register fits rather than guessing (naming the edge of what you know beats fabricating it).
2. **Artifact** — what communication are you producing? A PR/MR description, a review comment, a design doc, an RFC, a stakeholder message, a handoff. The artifact carries the **weight of the underlying subject**: communicating an irreversible, high-risk deploy plan is a heavier artifact than a typo note, and deserves more depth.

Audience sets the *register and vocabulary*; artifact sets *which lenses and how much weight*.

## Step 2 — Select lenses from the catalog

Open the catalog and pick the lenses whose **Tags** (artifacts + audiences) match your classification. Read only those sections.

- **Writing a PR/MR description** → lens 1 (the case, not the changelog); add lens 2 (smallest reviewable unit / stacking) when deciding how to slice the work.
- **Leaving a review comment** → lens 3 (invite, don't command).
- **Any reader who is not a same-context peer** → lens 4 (speak the reader's language) — the register modulator for everything else.
- **Anything leaving the team/org boundary** → lens 5 (no internal IDs outward).
- **Presenting options or a recommendation** → lens 6 (expose the reasoning), phrased per lens 4.

**Operator overrides.** Before applying the selected lenses, consult `deliberate-engineering-overrides`: if any selected lens has an operator override (disable / modify / add), honor it and declare the deviation in the Output.

## Step 3 — Apply and output

Apply the selected lenses to the communication, then report, briefly: the classification (audience + artifact), the lenses selected and why, anything deliberately skipped and why, and — when you presented alternatives — the rationale exposed for critique (lens 6).
