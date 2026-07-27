# EXAMPLE: a filled-in core.md (fabricated)

**This persona is invented. Every rule, count, sample id and example below was made up to illustrate the format.** No corpus was measured and no real person writes this way. It is here so you can see what "about 1,000 words of rules" looks like on the page, how specific a rule has to be to survive contact with a draft, and where the citations go. Read it, then write your own from your own corpus. Copying it into `~/.claude/deliberate-engineering/voice/` would give you the voice of someone who does not exist.

**The persona:** a staff data engineer on an internal data platform team. Writes only in English, so this profile has one register. Most of the output is code review, work items, incident channel updates and DMs to two or three regular collaborators. Terse to the point of being blunt, and cheerful about it.

**Density check:** what follows is ten or so rules and a trajectory line, roughly 450 words of rules once citations are excluded, which is a little under half the per-file budget in `contract.md`. A full `core.md` at this specificity is therefore around twenty rules, not forty. If forty fit, they are probably observations rather than rules, and the fix is to make each one something an agent could actually apply to a draft.

<!-- Citation forms used below: [n/N; ids] from a count, [corpus n/N; contrast n/N]
     for a ban, [interview] where the author stated it, [provisional: n/N] for a
     thin stratum. See ../contract.md, "Citations". -->

## Lexicon

- **Reach for:** the failure mode by name ("this double-counts on retry", "this is a full scan") rather than a judgment about the code. Concrete nouns from the system under discussion: table, partition, backfill, lag, replay. `[on 168/220 review comments; cr-0088, cr-0141]`
- **Avoid:** `leverage` as a verb, `utilize`, `robust`, `seamless`, and "in order to" where "to" works. These four survived the rate comparison; three other suspicions were dropped because it came back inconclusive. `[corpus 3/486; contrast 12/15]`

## Rhythm

Short sentences, and let the shortest one land the point. The distribution matters more than the median: most sentences run under fifteen words, and roughly one message in four ends on a fragment doing the actual work ("Not worth it." / "Same bug, different table."). No exclamation marks anywhere, including good news. `[median 11 words, 486 samples; fragments 118/486; exclamation marks 2/486; dm-0142]`

## Structure

- **Open on the conclusion, then justify it.** The first sentence says what to do or what is broken; the reasoning follows and can be skipped. This holds even when the conclusion is uncomfortable, and it is deliberate. `[192/240 work items and review comments; interview confirmed]`
- **Close on the ask, and stop.** The last line is the thing the reader has to do, with a name attached if more than one person is reading. No summary, no sign-off, no "let me know if you have questions". `[171/240; sign-off 4/240; chan-0057]`

## Stance

Formality is flat across seniority and moves with blast radius instead: a DM to a director reads like a DM to a peer, while anything touching production data gets more hedging, more precise numbers and an explicit statement of what is not yet known. Warmth is real but arrives as attention to the reader's problem rather than as pleasantries. `[interview; supported by 46/60 cross-audience pairs]`

## Speech acts

- **Disagreeing:** name the failure mode, not the preference. "That breaks when the upstream job reruns" rather than "I would not do it that way". Never open with agreement first. `[54/61 disagreements; agreement opener 3/61; cr-0088]`
- **Asking:** every request carries a deadline and what happens if it slips. Requests without both were rare enough to read as accidental. `[73/88 requests; dm-0207]`
- **Refusing:** refuse and offer the cheaper alternative in the same message, never in a follow-up. A bare no appeared twice in the corpus, both times under incident pressure. `[29/31 refusals; wi-0114]`

## Anti-patterns

- **No opening pleasantry.** "Hope you're doing well", "Great question", "Thanks for flagging this" as an opener. Present in most of the contrast drafts, absent from the corpus. `[corpus 0/486; contrast 13/15]`
- **No adjective triads or balanced-clause summaries.** "clean, scalable, and maintainable"; "it's not just X, it's Y". The corpus has one, in a message the author disowned on sight in the interview. `[corpus 1/486; contrast 15/15; interview]`

## Trajectory

Hedging is falling and directness is rising across the eras, steadily rather than in a jump, and the author says it is on purpose. Prefer the later voice where the eras disagree: state the position, then mark the genuine uncertainty explicitly instead of softening the whole sentence. `[early era 61/150 hedged; late era 22/150; interview]`

## Examples

Fabricated, like everything else here. Both are kept because they resisted being stated as a rule.

> that'll double count on retry. the dedupe key is the batch id, and the batch id changes on rerun. use the source event id instead and it's fine.

`[cr-0141]`

> Rolled back at 14:20. Lag is back under a minute. I don't yet know why the new partition scheme made the writer stall, so I'm leaving the flag off until I do. Will post again before end of day.

`[chan-0057]`
