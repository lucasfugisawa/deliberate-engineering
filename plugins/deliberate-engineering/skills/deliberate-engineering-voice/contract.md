# The voice profile directory contract

What a voice profile may contain, what gets loaded when, and how big each file should be. The profile lives at `~/.claude/deliberate-engineering/voice/`, in the operator's own space, alongside `overrides.md` and `state/`. Nothing here ships with the plugin: the plugin ships the mechanism, this contract, a template, and a method. Every profile is private to its author.

## Layout

```
~/.claude/deliberate-engineering/voice/
├── core.md                  # always loaded
├── registers/
│   ├── en.md                # loaded when writing in English
│   └── <lang>.md            # one per language you actually write in
├── archetypes/
│   ├── dm.md                # loaded when the artifact is a direct message
│   └── <type>.md            # one per communication type you write
└── chat-prompt.md           # optional; never part of a drafting load
```

## Getting started

The plugin ships a skeleton at `template/`, next to this file. A marketplace-installed plugin lives at a path you should not have to go hunting for, so the structure is faster to create than to find:

```bash
mkdir -p ~/.claude/deliberate-engineering/voice/registers
mkdir -p ~/.claude/deliberate-engineering/voice/archetypes
cd ~/.claude/deliberate-engineering/voice
touch core.md registers/en.md archetypes/dm.md
```

Rename `en.md` to a language you actually write in and `dm.md` to a communication type you actually produce. Then paste the template bodies in, or ask Claude to fetch them for you:

> Copy the `template/` directory from the `deliberate-engineering-voice` skill into `~/.claude/deliberate-engineering/voice/`.

Claude can resolve the installed skill path when you cannot. Either way the files arrive empty of rules, and the profile changes nothing until there are some: an empty `core.md` is an unwritten profile, not a broken one. `bootstrap.md` is the method for filling it (and `deliberate-engineering-voice-build`, the `/deliberate-engineering:voice-build` command, is the guided flow that runs that method for you), and `template/EXAMPLE-core.md` is a worked `core.md` for an invented persona, there to calibrate density, specificity and citation style. Do not copy that file into your profile; it describes someone who does not exist.

**Expect "no archetype matched", and expect it often at first.** A fresh copy of the template carries a single archetype, so nearly every draft falls back to core plus register and says so. That is the supported state described below, not a fault: each declaration names the artifact type that had no archetype, which is exactly the queue for which one to write next.

## What each file holds

**`core.md`** holds what is true of the voice everywhere: lexicon (the words reached for, the words never used), rhythm (sentence length distribution, fragments, punctuation and capitalization habits), structure (how a message opens, whether it front-loads, how it closes), stance (directness, warmth, formality defaults and how they move with audience distance and stakes), speech-act habits (how this author disagrees, asks, refuses, apologizes, hands off), the anti-patterns, and the trajectory. Each rule carries the evidence it came from, in the citation form below. The test for core membership is simple: if a rule would have to be restated in two registers or two archetypes, it belongs in core.

**`registers/<lang>.md`** holds only what changes with the language: greetings and sign-offs, the formality default, borrowed vocabulary the author does and does not use, punctuation and capitalization conventions specific to that language, and the constructions that read as translated. One file per language actually written in, named by its **ISO 639-1 code**: `en.md`, `de.md`, `ja.md`. Add a region subtag only where the variety genuinely differs in your own writing (`es-MX.md` alongside `es-ES.md`), never by default, since two register files that say the same thing cost more to maintain than one. A register cannot be inferred by translating findings from another language, so it is written from that language's own corpus.

**`archetypes/<type>.md`** holds what changes with the kind of communication: when the archetype applies, typical length and shape, opening and closing habits, the formality shift relative to core, and anything this artifact type forbids that core allows. A DM and a design doc are the same person writing in visibly different modes, and the archetype is where that difference lives.

**`chat-prompt.md`** (optional) is a condensed, self-contained rendering of the profile for pasting somewhere that cannot read a directory: another tool's custom-instructions field, a system prompt, a colleague's setup. It lives in the directory so it stays next to its source of truth, but it is **never** loaded during drafting: loading it alongside core and a register would restate the same rules at lower fidelity and spend context twice. `template/chat-prompt.md` is the stub, and it is rendered from the finished files rather than written alongside them: it is derived, so a rule that lives only there is a rule no draft will ever load.

## Citations

A rule that carries its evidence can be debugged when a draft comes out wrong. A rule that arrived as an impression cannot: there is nothing to re-check, so the only available repair is to delete it and hope. The recommended convention is a bracketed tag at the end of the rule:

| Source | Tag | Reads as |
|---|---|---|
| A count | `[n/N; ids]` | matching samples over samples measured, plus a sample id or two |
| An anti-pattern | `[corpus n/N; contrast n/N]` | both sides of the rate comparison |
| The interview | `[interview]` | stated by the author, no count behind it |
| An aspiration | `[aspiration]` | where the voice is going, not what it does |
| A thin stratum | `[provisional: n/N]` | too little material to be safe yet |

The ids point back into the corpus, whose format `bootstrap.md` describes. Both sides of an anti-pattern's comparison are load-bearing: a ban carrying only its corpus rate is a suspicion, and banning something the author genuinely does is the most damaging error this whole process offers.

Citations do not count against the size budget below. They cost a few characters per rule and they are what makes a later revision possible rather than a rewrite.

## What loads when

| File | Loaded |
|---|---|
| `core.md` | always |
| `registers/<lang>.md` | when the communication is written in `<lang>` |
| `archetypes/<type>.md` | when the communication's type matches `<type>` |
| `chat-prompt.md` | never, during drafting |

Three files on a typical draft. No archetype match falls back to core plus register, declared. No register match falls back to core plus archetype, declared. No directory at all is a silent no-op.

Where the loaded files disagree, the more specific one wins on the situation it describes: archetype refines register, register refines core. This is refinement, not replacement, so a core rule the archetype is silent about still holds.

## Size guidance

Aim for a **rules-only body of roughly 1,000 words per file**. Verbatim examples do not count toward that budget.

The reason is the load, not tidiness. A drafting load is core plus one register plus one archetype, so the per-use cost is roughly three files. Keep each file around 1,000 words of rules and the profile is cheap enough to apply on every message; let them sprawl and it becomes something you only load for important artifacts, which is the opposite of the point. A voice that only appears on ceremony is not a voice.

Examples sit outside the budget because they do work prose cannot: some habits are far cheaper to show than to state, and an example anchors a rule in something real. Keep them few, keep them verbatim, and choose them for the habits that resisted being written as a rule.

If a file will not fit, the usual cause is that it is carrying rules that belong somewhere else: a core rule duplicated into archetypes, or observations that were never turned into rules. Both are worth fixing before raising the budget.

## Archetype names are communication types, never tools

Name an archetype for the kind of communication (`dm`, `work-item`, `code-review`), not for the product it happens to travel through (`slack`, `jira`, `github`).

Tools change and profiles should not have to. More importantly, one tool carries several types: a chat app carries both one-to-one DMs and one-to-many channel posts, and those two have visibly different voices; an issue tracker carries titles, descriptions, and comments. Naming by tool collapses distinctions that matter and invents ones that do not. Naming by type also lets the skill match an artifact in a tool the profile has never heard of.

## A suggested starting set

The first profile built with this method (the pilot, described in `bootstrap.md`) used nine archetypes. This is a starting point, not a required set:

| Archetype | Covers |
|---|---|
| `dm` | one-to-one direct messages; the shortest and least formal mode |
| `channel` | posts to a group channel, where context has to be set up front |
| `work-item` | ticket and issue titles, descriptions, and comments |
| `code-review` | PR/MR descriptions, review comments, and replies to review |
| `design-doc` | longer internal documents and their comment threads |
| `email` | external correspondence and formal internal mail |
| `calendar` | invite titles, agendas, and descriptions |
| `social-post` | public short-form |
| `article` | public long-form |

Adopt, rename, split, drop, or invent. Someone who writes mostly one kind of thing may need three archetypes; someone whose voice genuinely does not change between two of these should merge them rather than maintain two files that say the same thing. A blind A/B that keeps producing ties on one artifact type is the signal that its archetype is not carrying anything (see `bootstrap.md`).

No match is a supported state, not a hole to be plugged with the nearest file. The skill falls back to core plus register and declares it.

## Keeping the profile

The directory is the operator's, and it stays out of every repository. A voice profile is built from a corpus of real writing and reads as a fairly precise description of a person, which is reason enough to keep it local. The corpus itself is more sensitive than the profile: see `bootstrap.md` for how to handle it.
