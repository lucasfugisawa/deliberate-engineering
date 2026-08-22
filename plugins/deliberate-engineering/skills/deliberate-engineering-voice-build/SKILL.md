---
name: deliberate-engineering-voice-build
description: "Use on demand to build an operator's voice profile from scratch: the collection-and-extraction on-ramp for the voice layer. It walks the operator from raw writing samples to a profile that satisfies the voice contract (core, registers, archetypes). It helps the operator identify their own communication archetypes, collects samples typed by archetype and language, runs the analysis and an adversarial recount, drives a findings-based self-interview and a blind A/B calibration (both kept human), then synthesizes the profile files, delegating the method to the voice skill's bootstrap.md. This is the BUILD side; applying an existing profile to a draft is deliberate-engineering-voice, not this. The corpus and the finished profile are kept local, out of every repository, by a best-effort check this skill runs rather than by a guarantee it can enforce. Stays silent unless invoked, via /deliberate-engineering:voice-build or an explicit request to build, create, or bootstrap a voice profile."
---

# Deliberate Engineering Voice Build

The build side of the voice layer. Where `deliberate-engineering-voice` reads a finished profile and applies it as the surface layer over a draft, this skill helps the operator *produce* that profile in the first place: it turns `bootstrap.md`, the method written as prose to run by hand, into a guided, resumable flow. It assists the expensive mechanical steps and keeps the two steps that must stay human.

It delegates the method to `bootstrap.md` and the output format to `contract.md`, both in the sibling `deliberate-engineering-voice` skill directory (at `../deliberate-engineering-voice/`). It drives the flow and names the load-bearing guards where they apply, but delegates the full method to those files: when a phase needs the detail (the exact analysis passes, a saturation floor, the citation form, the size budget), read the delegated file rather than expecting it reproduced here. Keeping the method in one place is what keeps this guide from drifting out of sync with it.

## Boundaries

- **vs `deliberate-engineering-voice` (the apply side)**: that skill reads a profile at draft time and applies it; this skill builds the profile. Opposite directions on the same artifact. Applying a profile is not this skill's job, and building one is not that skill's.
- **vs the capture-back extension (future, not this)**: folding a rejected draft or a style correction back into an *existing* profile over time is the incremental path, a separate future write target for `deliberate-engineering-capture`. This is the *initial* path from nothing to a first profile. Keep them separate; neither absorbs the other.
- **On demand only**: never self-triggers. Runs via `/deliberate-engineering:voice-build` or an explicit request to build, create, or bootstrap a voice profile. No invocation, total silence.

## What this is, and what it costs

Set the expectation first, out loud, because it changes how the operator shows up: this is a project across sessions, not one sitting, and the corpus collection is most of the cost. A profile built from a thin or curated corpus produces a caricature, not the operator. `bootstrap.md`'s "What this costs" section is the honest budget; surface it before starting rather than after.

This skill is a state machine. At every moment it knows which phase it is in, and inside collection, which bucket it is filling and whether that bucket has reached its floor. That explicit state is what keeps its behavior consistent from session to session, and it is split by kind (see "Durable state").

## Phase 0: Frame and set up

Confirm the operator understands the shape (a multi-session project) and the privacy stance (the corpus is the most sensitive artifact in the whole process, more than the profile). Create a **local working directory** for the corpus and the intermediate analysis, outside any repository. Default it to `~/.claude/deliberate-engineering/voice-build/`, the operator's own space alongside the profile and state directories and not a repository, unless the operator names another location. Before writing anything into it, run the safety check on that exact directory (see "Keeping it out of every repository") and confirm it is not a tracked path. Ask which languages the profile must cover; each language is collected and analyzed on its own.

## Phase 1: Identify the archetype set (teach, then discover)

Do not assume the operator knows what a communication archetype is; many do not, and getting this set right is what the whole profile is organized around. So teach first, then discover:

- **Teach with examples.** The same person writes differently in a direct message, a PR comment, a design doc, and a formal email. An archetype is *the mode*, not the tool: name the `contract.md` rule out loud, that archetypes are communication types, never tools (one chat app carries both one-to-one DMs and one-to-many channel posts, and those two have different voices).
- **Offer the suggested set as an illustrated menu.** `contract.md` carries a starting set of nine (dm, channel, work-item, code-review, design-doc, email, calendar, social-post, article). Present it with a one-line "this is where you..." for each, so the operator recognizes their own modes rather than guessing at an abstraction.
- **Then derive their set** from where they actually write and to whom, adapting the menu: rename, split, drop, invent. The result is the operator's archetype set, and it becomes the collection buckets in phase 2 and the archetype files in phase 6.

## Phase 2: Collect, typed (the expensive, multi-session phase)

The buckets are **archetype by language**, with **era** as a tag on each sample. Set up the working directory with one place per bucket and a collection manifest (the templates `template/collection-manifest.md` and `template/corpus-sample.md` beside this skill are the stubs to copy).

Each sample is captured in the corpus format `bootstrap.md` describes (the `corpus-sample.md` template beside this skill is the stub to copy), keeping the author's own text separate from any quoted counterparty text. Two points are load-bearing, not cosmetic:

- **`id` and the author/counterparty split.** Leaving counterparty text inside a count is the single most common source of a wrong rate; the split is decided once, per sample, at collection time. Every sample needs a stable `id`, because the phase-4 recount and every citation in the finished profile point back through it: a sample with no id has nothing to recount over. `date` carries the trajectory, and `era` is banded from it.
- **Why the typing is two-dimensional.** An archetype file is written from its archetype's buckets; a register file can only be written from that language's own samples (a register is never derived by translating another language's findings); core is written from what holds across archetypes and languages; the trajectory needs the era tags. Archetype-only typing cannot produce the registers or the trajectory.

Each bucket carries a **saturation floor**: a minimum below which a finding is not safe to state, not a target at which to stop collecting. The number is the operator's judgment rather than a shipped constant; `bootstrap.md` gives the rule (set a per-stratum minimum, and keep sampling while new samples still move the picture) with the pilot's rough thousand-in-total as one data point, not a requirement, and the template's floor numbers are illustrative starting values to replace. The manifest tracks which buckets have reached their floor. **Guard: representative, not curated.** Within each bucket, ask for the rushed one-liners and the messages the operator is not proud of, not only the polished ones; a corpus of best-writing yields a profile of a person who does not exist. **This phase stops and waits for the operator to bring the samples:** set up the buckets, floors, format, and manifest, then hand collection to the operator and do not proceed to analysis until the buckets reach their floors. This is the phase the flow most often resumes into.

## Phase 3: Analyze

Run the analysis dimensions `bootstrap.md` names in its section 2 over the collected buckets, each producing findings with sample counts and ids attached. That section also says which of them are **independent** and which are **cross-cutting derivations** that run *over* the others once those are in: run the independent ones concurrently via subagents or the Workflow engine when one is present, sequentially when it is not, and order the derivations after them. The state machine tracks every dimension in that list, not only the parallel ones.

## Phase 4: Verify the findings adversarially

Recount every frequency claim against the corpus in a **fresh context** (a separate agent or session, so the analysis is not asked to ratify its own conclusions), re-check that counterparty, template, and assistant-drafted text stayed out of each count, and downgrade or delete what the count does not support. Carry the counts with the claims. This mirrors the standing rule that trust is convergence, not a clean first pass.

## Phase 5: The style interview (human gate 1)

Build the questions *from the findings*, never cold, and put them one at a time, holding the interpretation back until the operator has answered. This gate stays human on purpose: the interview exists to catch a habit the operator disowns on sight, and agreement with a stated hypothesis is exactly what hides it. The skill rebuilds the facilitator/author separation a solo operator lacks by asking the question with the finding inside it but withholding the analysis's "why" until the answer is given. Wait for the operator's own answer to each question before showing the next or offering any interpretation, and never auto-answer on their behalf to keep momentum. The interview is done when the findings have been walked, per `bootstrap.md`'s section 4: the ambiguities, the deliberate-or-accidental calls, the bans the corpus cannot see, the aspirations, and the thin strata. Racing through because it feels slow is the failure this gate exists to prevent.

## Phase 6: Synthesize into the directory

Write `core.md`, `registers/<lang>.md`, and `archetypes/<type>.md` within the `contract.md` size budget, as rules (not raw measurements) each carrying its citation, with a few verbatim examples per file for the habits that resisted being stated as a rule. Put each rule where it belongs: true everywhere goes to core, language-bound to the register, type-bound to the archetype (a rule you would write into two archetypes was a core rule). Render `chat-prompt.md` last and only if needed, derived from the finished files (its stub is `../deliberate-engineering-voice/template/chat-prompt.md`).

## Phase 7: Calibrate with a blind A/B (human gate 2)

Run the blind A/B the way `bootstrap.md`'s section 6 describes, including its "running this on yourself" construction, which is where the load-bearing guard lives: the blind draft is generated in a fresh session that is never told a profile exists, so the asymmetry is structural rather than instructed. Drive it as follows:

- Shuffle the pair and **withhold the labels** until the operator has committed to a pick and said what is wrong with the other draft. Committing before the reveal is what makes the result mean anything.
- On a loss, fix the **profile**, not the draft (a loss is a missing rule, an overstated rule, or a ban that should not be there). Record wins, losses, and ties **per archetype**. Run rounds until it wins consistently across archetypes, and keep at least one round after the final edit. A persistent tie on an archetype means it carries nothing distinct: merge or drop it.

Fix the scenario count and the pass bar before the first round, and expect a first round that comes in mixed; that is the normal shape, not failure.

## Phase 8: Install and keep alive

Place the finished profile at `~/.claude/deliberate-engineering/voice/`, the operator's own space. Handle the corpus per privacy: delete it, or retain it locally only if a later calibration genuinely needs it, never committing it anywhere. Point at the keep-alive path: the cheapest signal is the edits the operator makes to drafts before sending, folded back on the next pass (that fold-back is the separate capture-back extension, not this skill).

## Durable state (split by kind)

The working directory's **collection manifest is the authoritative state home**, and it holds all of it: the current phase, the per-bucket ledger (which buckets exist, their floors, their counts), and the chosen archetypes and languages. It lives with the corpus, outside any repository, which is where a repo-less, privacy-bound project's state belongs. A fresh session rehydrates from it: read the manifest, then continue at the right phase and bucket rather than restarting.

`deliberate-engineering-state` is an **optional echo, not the home**. Its schema is a freeform whiteboard keyed by a code work-unit and resolved by the session's working directory, a poor structural fit for a repo-less build: no per-bucket store, no branch, PR, or ticket to key by, and no switch to force its global location while a session sits inside a repo. So do not depend on it. If the operator's `-state` resolves to a durable home this session, you may drop a one-line coarse-phase breadcrumb there under the identifier `voice-build`, declared; if it would land inside a repo, skip it. What a resume reads is the manifest, not `-state`.

## Keeping it out of every repository

The corpus is more sensitive than the profile it produces, and neither may reach a repository. This skill enforces that **by instruction, best-effort, not by a guarantee**: the plugin has no hooks, so nothing can technically block a write. Before writing corpus or profile content, run the check **against the exact target directory, not the shell's current directory**, because git resolves to the cwd unless told otherwise and the two can differ in repo-ness. Anchor every command with `git -C <target>`: run `git -C <target> rev-parse --is-inside-work-tree`; if it errors with `fatal: not a git repository`, the target is in no repository, so it is safe to write. Otherwise the target sits in some git context, so let `git -C <target> check-ignore -q <target>` decide: exit 0 means the path is ignored, so it is safe; anything else (exit 1, or an `outside repository` error) means it is not confirmed-ignored, so treat the target as tracked, decline, and explain rather than writing. Default the working directory outside any repo (phase 0) so the first check settles it cleanly. The honest limitation: an agent can ignore an instruction and nothing outside it blocks the write, so this lowers the risk of a leak, it does not remove it. Never echo corpus content into a public artifact.

## What this deliberately does not do

- **The two human gates stay human.** It does not run the interview or the blind pick unattended; a tool that did would produce a worse profile, confidently. It rebuilds the missing separation mechanically instead.
- **It does not build the corpus for the operator.** Collection is most of the cost and is the operator's to do; the skill structures and paces it (buckets, floors, the format, the representativeness guard), it does not invent samples.
- **Not end-to-end automation.** The value is lowering the cost of the mechanical steps, not removing the judgment.

## Output

Report, at each phase and on resume: the current phase and what it produced; on collection, the buckets and which have reached their floor; the state home used (the working-directory manifest, plus the optional `-state` breadcrumb if one was written), declared; and at the two gates, that the flow is stopping for the operator. When installing, name where the profile was written and how the corpus was handled. This skill is a guide with a durable place to stand, so its output is where the operator is in the project and what remains.
