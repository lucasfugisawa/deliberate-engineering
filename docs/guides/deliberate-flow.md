[deliberate-engineering](../../README.md) › [Guides](README.md) › **The deliberate flow**

# The deliberate flow

The everyday path: how a piece of engineering work travels through the plugin in a normal session. Unlike [orchestrate](orchestrate.md) and [conduct](conduct.md), this is not a flow you have to drive: most of it fires itself. What this guide gives you is the journey (so you recognize what is happening and why) and the map (so you know when to call a phase directly).

## When you don't need this guide

For research, prose, ad-hoc analysis, and disposable no-consumer scripts, the plugin deliberately stays out of the way. And for trivial-and-safe work it says so and routes light: a typo fix earns a single light phase, not a ceremony.

## The journey

You bring work; the router classifies it before anything acts. Say you ask for "implement field X on the billing model":

1. **[You]** Describe the work: through `/deliberate-engineering:start` if you want the front door explicitly, or just by asking; the router also fires on its own when the work is broad or ambiguous.
2. **[Agent]** Classifies genre (new thing? change? incident? review? design?) and the router's four routing axes: risk, reversibility, requirement clarity, reach. (Each phase selector then classifies again on the axes proper to that phase; what they all share is the ruler, the cost of being wrong rather than the size of the change.) Announces the phase sequence and the ceremony it earns, and, the most valuable part, what it is deliberately skipping and why. For the billing example: plan → build → review → verify, full ceremony, nothing skipped, and a stop before anything irreversible.
3. **[Agent]** Runs each phase through its selector, which reads only the lenses that fit this case from its catalog: `:plan` decides what is worth building and how much process; the build is delegated to your workflow engine; `:review` applies the review lenses the change calls for; `:verify` confronts the result with reality and brings evidence.
4. **[Agent]** When the next artifact is a communication (a PR description, a review comment, a message), consults `:communicate` from inside whatever phase it is in: audience and artifact pick the lenses, and your [voice profile](voice-build.md), if present, shapes how it sounds.
5. **[You]** Pull the trigger at the Rule 1 gate: merge, deploy, publish, tag. The agent prepares and stops; the irreversible action is always yours.

Mid-flight, the classification is a live hypothesis: if the work turns out riskier (or safer) than it looked, the agent re-classifies out loud, re-introduces a skipped phase or lightens an over-heavy one, and continues.

## Calling a phase directly

When you already know where you are, skip the front door:

| Command | Call it when | The question it answers |
|---|---|---|
| `/deliberate-engineering:start` | Unsure which phase, or the work spans several | Where do I start, and how much ceremony? |
| `/deliberate-engineering:plan` | Before code exists | What is worth building, and how much process? |
| `/deliberate-engineering:review` | A change, diff, or PR in hand | Which lenses does *this* change call for? |
| `/deliberate-engineering:verify` | A claim that must be established as fact | Is it true against reality, and what is the evidence? |
| `/deliberate-engineering:debug` | A live system misbehaving with no reliable expectation; also peacetime signal hygiene (alerts, error streams, thresholds, flow ownership) and the post-incident retrospective | What is actually going on, how do I respond, and how do I keep the signals worth trusting? |
| `/deliberate-engineering:communicate` | The next artifact is a communication | How should this read for its audience? |

Two rules of thumb the plugin holds throughout: **risk and uncertainty set the depth, not line count** (a one-line change to a fee calculation is high-depth; a 600-line isolated helper is not), and **review asks "does this look correct?" while verify asks "is it correct, and what is my evidence?"**.

## What runs underneath

The nine standing rules hold under every phase (the human gate, verify-before-endorse, recommend-with-rationale, checkpoint durable state, and the rest); your [overrides](capture.md) take precedence over any shipped lens, composition pattern or rule; and `deliberate-engineering-state` keeps a working-note so the phase sequence and pendings survive across sessions, written to `.deliberate/state/` in the repository root when it can confirm that directory is ignored by your VCS and to `~/.claude/deliberate-engineering/state/` otherwise, saying which it used each time: all consulted automatically, none of them yours to drive.

## Where to go next

- The program outgrew one session → [Orchestrate](orchestrate.md)
- Irreversible steps concentrated into a cluster → [Conduct](conduct.md)
- You corrected the agent repeatedly this session → [Capture](capture.md)
- The concepts behind all of this → [Architecture & usage](../architecture-and-usage.md)
