# Voice-build collection manifest

The authoritative state home for a voice-build project. It lives in your local working directory, never in a repository, alongside the corpus, and a fresh session reads it to resume. It holds the current phase and the per-bucket ledger (which buckets exist and whether each has reached its floor). It is not the profile and not the corpus; it is the ledger the build skill reads to know where you are. Everything below the phase (languages, archetypes, buckets, floors) is an example to replace with your own.

## Current phase

The phase the build is in, so a fresh session resumes here rather than restarting. One of: 0 frame, 1 archetypes, 2 collect, 3 analyze, 4 recount, 5 interview, 6 synthesize, 7 calibrate, 8 install.

- phase: 2 collect

## Languages

One line per language you actually write in; each is collected and analyzed on its own. (Example: replace with your own.)

- en
- de

## Archetype set

The communication modes chosen in phase 1, adapted from the suggested set (rename, split, drop, or invent as fits how you actually write). (Example set below: replace with yours.)

- dm: one-to-one direct messages, the shortest and least formal mode
- email: external correspondence and formal mail

## Buckets (archetype by language)

One row per bucket. `floor` is the minimum below which a finding is not safe to state: a floor, not a stop target, so keep sampling while new samples still move the picture. `count` is samples collected so far. `at-floor` becomes yes once the count has reached the floor and new samples stop moving the picture. The rows below are an example, and the floors are illustrative starting values, not defaults: replace them with your own buckets.

| archetype | language | floor | count | at-floor |
|---|---|---|---|---|
| dm | en | 40 | 0 | no |
| dm | de | 40 | 0 | no |
| email | en | 25 | 0 | no |
| email | de | 25 | 0 | no |

## Notes

- Representative, not curated: include the rushed one-liners and the messages you are not proud of, not only the polished ones.
- Each sample uses `corpus-sample.md`, with a stable `id`, and keeps the author's own text separate from any quoted counterparty text.
