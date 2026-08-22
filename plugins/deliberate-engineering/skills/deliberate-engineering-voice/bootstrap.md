# Building a voice profile from scratch

The method for producing a profile that satisfies `contract.md`: collect a corpus, analyze it, verify the findings, interview the author, synthesize, then calibrate blind. It is the generalized form of the method used to build the pilot profile, with that pilot's expensive lessons marked where they apply.

Set expectations before starting. This is a project, not an afternoon, and the corpus is most of the cost. A profile built from a thin or curated corpus produces a caricature: the loud habits get amplified, the quiet ones vanish, and the result reads like an impression of the author rather than the author.

**On the corpus and privacy.** The corpus is the most sensitive artifact in this process, more so than the profile it produces. Keep it local, keep it out of every repository and every shared drive, and delete it when the profile is built unless a later calibration round genuinely needs it.

## What this costs

The pilot is one data point rather than a requirement, but its shape is the honest way to budget:

- **Roughly a thousand collected samples**, spanning many years of writing rather than a recent window.
- **Six analyses run in parallel**, one per dimension, each producing its own findings.
- **A separate adversarial verification pass** over those findings, run somewhere it was not defending its own work.
- **A findings-driven interview** with the author, built from what the analysis had actually found.
- **Three rounds of blind calibration**, with profile edits between rounds.

The last of those is the one to take seriously. **The pilot's first blind round failed against its own target**: 5 profile wins, 3 losses and 1 tie, against a bar of 8 in 10. Two scenarios lost three consecutive times before they flipped. A reader who budgets one round will run it, see more wins than losses, and conclude the profile works when it does not.

None of these numbers is a threshold to hit. They are here so the effort is not mistaken for an afternoon, and so a first round that comes back mixed reads as normal rather than as failure.

## 1. Collect the corpus

- **Verbatim.** No summaries, no paraphrase, no reconstruction from memory. Rate comparison is the backbone of every later step, and a paraphrase destroys every count it touches.
- **Authored-only.** Only text the author actually wrote. Exclude forwarded content, pasted logs, boilerplate and templates, and anything an assistant drafted.
- **Exclude quoted counterparty text from every count.** Quoted replies, inline quotations, and thread history carry someone else's voice, and they inflate precisely the constructions being measured. This is the single most common source of a wrong rate. (Pilot lesson.)
- **Context is labelled as context.** Keep the surrounding thread where it changes how a sample reads, because what the author was replying to is real analysis input. Mark it so it can never enter a count.
- **Representative, not curated.** Collect what was actually written, including the rushed one-liners and the message the author is not proud of. A corpus of the author's best writing yields a profile of a person who does not exist, and every subsequent draft reads as effortful.
- **Stratified by situation.** Sample deliberately across the situations the profile has to cover: the quick reply, the long explanation, the disagreement, the request, the refusal, the apology, the announcement, the handoff. Voice varies far more by speech act than by topic.
- **Full history, stratified by era.** Do not take only the recent window. Slice the whole available history into eras and sample each one. The trajectory is itself a finding: where the voice is heading matters as much as where it currently sits, and a profile built from the last few months bakes in whatever the author happened to be doing that quarter. (Pilot lesson.)
- **Saturation floors are floors, not targets.** Set a minimum per stratum and treat it as the line below which a finding is not safe to state, not the line at which collection stops. Keep sampling a stratum while new samples still move the picture; stop when they stop. For magnitude, and as one data point rather than a requirement: the pilot's corpus ran to roughly a thousand samples in total across all its strata, languages and eras. A narrower voice, or one written in a single language, can saturate on considerably less.
- **Each language to its own floor.** An author who writes in more than one language collects each language separately, to its own floor, across its own situations. A register cannot be derived by translating findings from another language.

### Corpus format

The rules above only become mechanical if every sample has the same shape. Any format works as long as it separates the author's own words from everyone else's, and it is worth fixing the shape before collecting rather than after. One minimal schema that does the job:

```
---
id: dm-0142
archetype: dm
language: en
date: 2021-04-07
era: early
situation: refusing a request
---

## Counterparty context (never counted)

> [what the other person wrote, verbatim, as much of it as changes how the reply reads]

## Author text (the only block measured)

[exactly what the author wrote, verbatim, and nothing else]
```

One file per sample, or one file per stratum with samples separated by this header. What each field buys:

- **`id`** is stable, so every count and every rule in the finished profile can cite the samples behind it. Without it, "record what supports every claim" has no target and the adversarial pass has nothing to recount over.
- **`archetype`, `language`, `situation`** make the strata sliceable. They are how a floor gets checked per stratum, and how a register or archetype file gets written from its own material instead of by translation.
- **`date`** and its era band carry the trajectory. Sorting by date is most of the era analysis.

**Measure the author-text block and nothing else.** This is the whole point of the format, and it is what turns "exclude quoted counterparty text" from an intention into a mechanical rule: the exclusion is decided once, at collection time, per sample, rather than re-litigated on every count. In the pilot, counterparty text left inside the samples inflated the constructions being measured by up to 62%, and that error was found only because the author's text was mechanically separable from the quoted text. A corpus stored as undifferentiated blobs cannot be audited this way at all. (Pilot lesson.)

## 2. Analysis dimensions

Run each dimension as its own pass and record what supports every claim, as sample ids from the corpus format above. Six of these are independent and run in parallel (lexicon, syntax and rhythm, structure, tone, pragmatics, anti-patterns); the remaining two, cross-language and trajectory, are cross-cutting derivations that run over the others rather than in parallel with them. The dimensions:

- **Lexicon.** Words and phrases with a rate meaningfully above baseline, and the ones conspicuously absent. Hedges, intensifiers, discourse markers, connectives, terms of address, profanity or its absence, emoji and reaction habits.
- **Syntax and rhythm.** Sentence length distribution, meaning the shape rather than the mean: an author who alternates long and very short sentences has the same mean as one who writes uniformly medium ones, and they sound nothing alike. Clause structure, fragments, parentheticals, which punctuation marks appear and at what rate, capitalization habits.
- **Structure.** How a message opens, whether it front-loads the point or builds to it, paragraphing, list and heading usage, how it closes, length by situation, and whether the author sends one message or several.
- **Tone.** Warmth, directness, formality, humor, and how each of them moves with audience distance and with stakes. Tone is rarely constant; the finding is the function, not the value.
- **Pragmatics, per speech act.** How this author disagrees, asks, refuses, apologizes, praises, escalates, chases, and hands off. This is the highest-value dimension and the one most often skipped, because it is harder to count than lexicon. Two authors with identical vocabularies still disagree differently, and disagreement is where a draft in the wrong voice does the most damage.
- **Cross-language.** Which findings hold in every language (those belong in core) and which are language-bound (those belong in a register). Do not assume symmetry: formality, directness, and greeting habits commonly shift with language in the same author.
- **Trajectory.** How each dimension moved across the eras. Record the direction, not only the current value.
- **Anti-patterns.** The constructions this author does not produce. Establish them by **rate comparison against contrast material**: draft the same artifacts with an unaided assistant, then compare rates. A construction qualifies as an anti-pattern when it appears at a meaningful rate in the contrast set and at or near zero in the corpus. The pilot's contrast set was 15 AI-drafted articles, which is one data point rather than a required size; what matters is that the contrast material is the same artifact type as the corpus it is compared against, since a chat reply and an article do not share a baseline.

**Only ban a tic when a rate comparison supports it.** Banning something the author genuinely does is the most damaging error available in this whole process: the drafts come out feeling censored, and the author usually cannot say why. A suspicion is not a ban. Where the comparison is inconclusive, leave the construction alone. (Pilot lesson.)

## 3. Verify the findings adversarially

**In the pilot, an audit of 12 findings found 6 overstated and 1 false.** Analysis produces confident prose, and confident prose is not evidence. Before anything reaches the profile, run a pass whose explicit job is to break the findings rather than to present them.

- **Recount every frequency claim.** "Always", "never", "usually", "tends to" all need the number behind them. Go back to the corpus and get it, counting the author-text block of each sample and nothing else.
- **Downgrade or delete what the count does not support.** A "never" that turns out to be "rarely" becomes "rarely". A rule with no support becomes an example, or gets cut.
- **Re-check the exclusions.** Confirm that quoted counterparty text, templates, and assistant-drafted material stayed out of each count. This is where inflated rates come from.
- **Run the audit somewhere it is not defending itself.** A fresh context, or a different agent, or a different day. An analysis pass asked to check its own conclusions will ratify them.
- **Keep the counts with the claims.** A profile whose every rule traces back to a number is one that can be debugged when a draft comes out wrong. A profile built from impressions cannot be. Carry them in the citation form `contract.md` describes, so the count and the sample ids travel with the rule into the profile rather than being left behind in a working document.

## 4. The style interview

The corpus shows what the author does. The interview establishes which of it is intentional, and it is driven **by the findings**, never asked cold. A blank "how would you describe your tone?" gets the tone the author wishes they had. Put each finding in front of them instead:

- **Ambiguities.** Two habits appearing at similar rates in the same situation. Which one is the author and which one was the circumstance?
- **Deliberate or accidental.** "You open this way about half the time. On purpose?" A habit the author disowns on sight is a habit the profile should not enforce.
- **Bans the corpus cannot see.** Things the author avoids in writing, things they would refuse in a draft, and things they used to do and have deliberately stopped. The last of these will show up in the trajectory, and the interview confirms the direction.
- **Aspirations, marked as such.** Where the author wants the voice to go. Keep them separate from the descriptive findings and label them, so an aspiration never silently overwrites an observed habit.
- **Thin strata.** The situations and artifact types where the corpus had too little material to measure. Ask how they would handle them, and write those rules as provisional.

A dozen sharp questions built from findings beats a long generic questionnaire, and the author will answer them faster.

**Running this on yourself.** This section is written for a facilitator who is not the author, and a solo adopter is both at once. Rebuild the gap mechanically: have an agent build the question list from the findings and put the questions one at a time, and answer each before seeing the next. The finding belongs inside the question, since that is what makes it answerable, but the analysis's explanation of *why* you do it does not. Ask the agent to hold its interpretation back until you have given yours. Otherwise the interview becomes an hour of agreeing with a hypothesis, and the one thing the interview exists to catch, a habit you disown on sight, is exactly what agreement hides.

## 5. Synthesize into the directory

- **Write rules, not observations.** "Sentences average 23 words" is a measurement. "Keep most sentences short, and let a very short one carry the point" is something an agent can apply. Keep the measurement attached to the rule as its citation; it is the evidence, not the instruction.
- **Put each rule where it belongs.** True everywhere goes to `core.md`. Language-bound goes to the register. Type-bound goes to the archetype. Writing the same rule into two archetypes is the signal that it was a core rule.
- **Carry a few verbatim examples per file**, chosen because they resisted being stated as a rule. They do work prose cannot, and they anchor the file in something real. Real text, few, lightly redacted if needed, and cited back to the sample they came from.
- **Respect the size budget** in `contract.md`. The profile has to stay cheap enough to load on every draft.
- **State anti-patterns as bans with their evidence attached**, not as vague warnings. A ban whose evidence is recorded can be revisited; one that arrived as a hunch cannot.
- **Mark trajectory findings as direction**, so the profile ages toward the voice rather than away from it.
- **Render `chat-prompt.md` last, and only if you need it.** It is a condensed, self-contained version of the directory for pasting where a directory cannot be read, so it is written from the finished files rather than alongside them, and it is regenerated whenever they change. `template/chat-prompt.md` is the stub. It is derived, never a source: a rule that exists only there is a rule the drafting path will never load.

## 6. Calibrate with a blind A/B

The only test that matters is whether the author can tell.

- **Use real, upcoming artifacts**, spread across archetypes. Sample prompts produce sample writing.
- **Fix the scenario count and the pass bar before the first round.** The pilot used 10 scenarios per round against a bar of 8 in 10, stated as one data point rather than a requirement. Whatever numbers you pick, pick them in advance: a bar chosen after seeing the results is a bar the profile always clears, and the count has to be large enough that the profile is able to fail.
- **Two drafts per artifact**: one with the profile loaded, one without. Same request, same context, same length target.
- **Present them unlabelled and in randomized order.** The author picks which one sounds like them, and then says what is wrong with the other one.
- **When the profile's draft loses, ask the author what is wrong with it before theorising about why.** In the pilot, three facilitator hypotheses failed where two direct questions succeeded. The author can point at the wrong word in a second; an hour of derivation usually produces a well-argued wrong explanation. (Pilot lesson.)
- **Fix the profile, not the draft.** A loss is a profile bug: a missing rule, an overstated rule, or a ban that should not be there.
- **Run rounds until the profile wins consistently across archetypes**, and keep at least one round after the final edit, so the last measurement is not taken against the material that prompted the fix.
- **Ties are information.** A persistent tie on one artifact type usually means the voice barely differs there, which is a good reason to merge or drop that archetype rather than to keep tuning it.

**Running this on yourself.** Everything above assumes a facilitator holding the labels. A solo adopter is author, facilitator and operator at once, which is the exact arrangement a blind test exists to prevent, so recover the blind mechanically rather than by willpower:

- **Generate the blind draft in a fresh session given only the request**, with no mention that a profile exists, and generate the profile draft with the profile loaded. Same request, same context, same length target, one draft each. Do not build the asymmetry out of instructions: a dispatched subagent keeps its file access, so "forbidden to read the profile directory" is compliance, not access control. The no-context construction *is* the asymmetry, because an agent never told a profile exists has nothing to go looking for. If you must use an in-session subagent instead, confirm from its tool-call log that it never opened the profile directory rather than assuming it.
- **Have the agent shuffle the pair and withhold the labels.** It keeps the mapping to itself until you have committed to a pick and said what is wrong with the other draft. Committing before the reveal is the part that makes the result mean anything.
- **Do not read the generation step before choosing.** Run it in a separate session, or scroll past it without looking. Once you have seen which agent produced which draft, that scenario is spent and cannot be re-run.
- **Then take the labels and record wins, losses and ties per archetype.** Per archetype matters: a profile that wins overall while losing every code review is a profile with one broken archetype, and an aggregate score hides that.

Expect this to be uncomfortable rather than impossible. The pilot's first round came in under its own bar, which is the normal shape of a first round and the reason to plan for more than one.

## 7. Keep it alive

A voice profile describes a moving target. Re-run a short A/B when drafts start to feel off; add an archetype when a new artifact type becomes routine; revisit the trajectory findings periodically, since the direction they encoded eventually becomes the current value.

The cheapest signal available is the edits the author makes to drafts before sending them. Each one is either a rule the profile is missing or a rule it got wrong. Capturing them back into the profile is a manual step today: note the correction, and fold it in on the next pass rather than after every message.
