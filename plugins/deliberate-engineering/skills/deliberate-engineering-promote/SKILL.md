---
name: deliberate-engineering-promote
description: "Use on demand to drive a pending candidate into the catalog systematically. Runs the leak-audit gate, classifies isolated vs structural, then (isolated) edits the catalog append-only + runs skill-reviewer or (structural) stops and recommends the proper design cycle. This is the promotion step of the author contribution flow — it drives a candidate into the shared catalog (working tree only, gated). It is not the contribute skill, which captures candidates, nor the adopter feedback skill, which writes your personal override file. Stays silent unless invoked."
---

# Deliberate Engineering Promote

The third vertex of the authoring trio. Where `deliberate-engineering-feedback` grows the adopter's personal override file, and `deliberate-engineering-contribute` captures generalizable judgment into clean candidate files in `candidates/`, this skill drives an approved candidate from the queue into the shipped catalog. It is the promotion half: systematically elevate a candidate through a blocking leak-audit gate, classify it as isolated or structural, route to the correct path, and stop at the human gate before commit. All catalog edits happen in the working tree only. The skill NEVER commits, opens a PR, or pushes — that irreversible, outward-facing act is the human's.

## vs the contribute skill

`deliberate-engineering-contribute` is the **capture** half — it turns generalizable engineering judgment from a session into a clean candidate file and deposits it in `candidates/`. This skill is the **promote** half — it takes a candidate from the queue, runs the gated promotion (leak audit, classification, catalog fit, review), and moves it into the shipped catalog or recommends the proper design cycle. Two skills, one gated pipeline. The differentiator: This is the promotion step of the author contribution flow — it drives a candidate into the shared catalog (working tree only, gated). It is not the contribute skill, which captures candidates.

## vs the adopter feedback skill

`deliberate-engineering-feedback` grows the **adopter's personal override file** — `~/.claude/deliberate-engineering-overrides.md`, local and private. This skill edits the **shared catalog** — the shipped plugin content. Opposite write-targets. The differentiator: This is the promotion step of the author contribution flow — it drives a candidate into the shared catalog (working tree only, gated). It is not the adopter feedback skill, which writes your personal override file.

## On demand only

This skill never self-triggers. It runs only when invoked — via `/deliberate-engineering:promote` or an explicit natural-language request (e.g., "promote candidate X to the catalog" or "drive this candidate into the catalog"). Absence of invocation means total silence. The author decides when a candidate is ready for promotion; the skill does not decide for them.

## Flow overview

Five steps in sequence: (1) the leak-audit blocking gate audits the candidate for surviving real specifics FIRST; on suspicion it blocks and edits nothing; (2) classify the candidate as isolated (add/modify a lens in an existing catalog) or structural (new catalog, reorg, rule change); (3a) the isolated route edits the catalog file append-only, runs skill-reviewer, and removes the candidate file, all in the working tree; (3b) the structural route does NOT edit — it stops, summarizes why the candidate is structural, and recommends the proper brainstorm/spec/plan cycle, leaving the candidate pending; (4) the human gate — the skill ends WITHOUT commit/PR/push; (5) report what was done (isolated) or recommended (structural) and the candidate disposition. Nothing touches the catalog until the leak-audit gate passes.

## The leak-audit blocking gate

The first step, before any edit. Audit the candidate file for surviving real specifics — employer names, service names, vendor names, org structure, person names, ticket IDs, incident numbers, real quantities tied to one employer. This is a CHECK, not a scrub: the candidate was born generalized in `contribute`, so the presence of a real specific is a process failure that blocks promotion until the candidate is re-generalized.

On any suspicion — a name that looks like a service, a number that smells real, a vendor/tool name that ties to one employer's stack — the gate BLOCKS. The skill flags the suspect content, reports the block, and edits nothing. The candidate stays pending. The author fixes the leak in the candidate file and re-invokes promotion. The boundary is hard: nothing touches the catalog before the gate passes.

The gate audits the candidate file only — it does not audit the catalog itself (that is a separate maintenance act). Pass the gate → proceed to classify. Fail the gate → block, flag, edit nothing, stop.

## Classify — isolated vs structural

After the leak-audit gate passes, classify the candidate into one of two routes:

**Isolated:** the candidate adds a new lens to an existing catalog, or modifies an existing lens in place. The catalog file structure, the numbering system, and the group divisions stay unchanged. This is the common case — one lens in, one lens out, append-only.

**Structural:** the candidate requires a new catalog file, a reorganization of an existing catalog, a change to the numbering or grouping system, or a modification to the standing rules. Structural changes touch the plugin's architecture, not just its content, and they demand a full design cycle (brainstorm, spec, plan, review).

On ambiguity — the candidate could be read either way, or you cannot tell which route applies — default to structural. Do NOT edit when in doubt; ask the author which route applies and wait for confirmation. The conservative default is structural (do not edit) to prevent silent catalog corruption.

## The isolated route — edit, review, remove

For an isolated candidate (add or modify), proceed with catalog promotion in the working tree:

### Locate the target catalog

Each axis has one catalog file at `plugins/deliberate-engineering/skills/<axis>-strategy-selector/catalog.md` where axis is one of: review, verification (for `target: verify`), planning, debug-operate (for `target: debug`). The candidate's frontmatter `target` field selects the catalog: `target: review` → `review-strategy-selector/catalog.md`; `target: verify` → `verification-strategy-selector/catalog.md`; `target: planning` → `planning-strategy-selector/catalog.md`; `target: debug` → `debug-operate-strategy-selector/catalog.md`.

### Apply the operation append-only

Lenses are `### N. Title` blocks followed by three bullets (How it works / Objective / When most valuable), grouped into Parts (lettered sections like "Part A — Process Strategies"). The operation in the candidate frontmatter determines what to do:

**`operation: add`** — the candidate is a wholly new lens. Before assigning a number, scan the catalog for an existing lens with the same title or a nearly identical principle; on a hit, do not add — see add-duplicate handling in "Error handling." Otherwise assign the NEXT FREE NUMBER (scan the catalog for the highest existing `### N.` number and add one). PLACE the new lens block under the Part (group) that matches its theme — do NOT append at the end of the file; insert it in the thematically correct Part, even if that Part's numbers are no longer sequential. This is deliberate: a Part may run out of numeric order (e.g., Part A ends 1–11, 52, 53) because append-only numbering is prioritized over reading-order. Write the new `### N. Title` block with the three bullets, formatted identically to existing lenses in the catalog.

**`operation: modify` with `modifies: N`** — the candidate amends an existing lens. Locate the `### N.` block in the catalog (where N matches the `modifies` field) and edit it in place. Do NOT change the number, do NOT move it to a different Part. If the amendment changes the title, change the title on the `### N.` line; if it adjusts a bullet, edit that bullet; if it adds a bullet, add it. The lens stays where it is, under its original number and Part. If `### N.` does not exist in the catalog, STOP — this is a modify-nonexistent error (see "Error handling").

### Run skill-reviewer

After editing the catalog file in the working tree, invoke the `plugin-dev:skill-reviewer` agent to review the catalog file's quality. Pass the catalog file path (`plugins/deliberate-engineering/skills/<axis>-strategy-selector/catalog.md`) and the context that a new lens was added or an existing lens was modified. The reviewer checks for: consistency with existing lenses, formatting adherence, clarity of the principle, and whether the lens fits the catalog's voice.

If the skill-reviewer rejects the edit or flags a quality issue, report the findings and STOP. Do NOT proceed to remove the candidate file, do NOT commit over the rejection. The author addresses the reviewer's findings (either by editing the catalog in the working tree or by revising the candidate and re-promoting), then re-invokes promotion or commits manually.

### Remove the candidate file atomically

On skill-reviewer pass, the final step of the isolated route is to remove the candidate file from `candidates/`. This is the atomic pair: the catalog edit AND the candidate removal happen together in the working tree, ready to be committed as one unit by the human. The candidate file is removed because it has been promoted — its content now lives in the catalog.

On removal failure (permissions, file lock, anything), do NOT fail silently. Flag the half-applied state — the catalog edit succeeded, the candidate removal failed — and report both file paths so the author can remove the candidate manually. Never leave a half-applied state silently.

## The structural route — do not edit, recommend

For a structural candidate — one that requires a new catalog, a reorganization, a numbering change, or a rule modification — do NOT edit the catalog. The structural route is a stop-and-recommend: summarize the candidate, explain why it is structural (cite the specific reason: new catalog needed, reorg required, rule change), and recommend the proper design cycle. Structural changes are too invasive for an append-only skill to handle safely — they need the full brainstorm/spec/plan/review cycle that applies to any plugin architecture change.

The candidate file stays pending. The author takes the recommendation, runs the design cycle, and manually applies the structural change (or decides to drop it). The promote skill does not touch the catalog on the structural route — it only provides the analysis and the recommendation.

## The append-only invariant — never renumber existing lenses

This is a hard invariant binding all catalog edits: **NEVER renumber an existing lens.** Lens numbers are stable-for-life identifiers. Adopters cite them in override files (e.g., `review #35 — disable`), selectors cite them in session notes, and documentation links to them by number. Renumbering `### 35.` to `### 36.` would silently break every override, every citation, every link that references #35. This breakage is invisible and irreversible — the override file would disable the wrong lens, and the adopter would never know.

The invariant has two corollaries:

1. **New lens = next free number, placed thematically.** A new lens gets the next available number (highest existing + 1) but is PLACED under the Part (group) that matches its theme, not necessarily at the end of the file. This is why a Part may have non-sequential numbers (Part A ends 1–11, 52, 53) — new lenses are numbered sequentially but placed thematically. The number is the stable identifier; the physical location is for human reading.

2. **Modify = edit #N in place.** A `modify` operation edits the existing `### N.` block where it stands. It does NOT move the lens to a different Part, does NOT renumber it, does NOT reorder surrounding lenses. The lens stays under its original number and Part, even if the modification changes its title or content.

Renumbering is the one act this skill will never perform, under any circumstance. If a candidate implicitly requires renumbering (e.g., "insert this between #10 and #11"), classify it as structural and stop — that requires a reorg design, not an append-only edit.

## States, atomicity, the human gate

The promote skill edits the catalog and removes the candidate file in the **working tree only**. It produces a git diff ready to be reviewed and committed by the human. It NEVER commits, NEVER opens a PR, NEVER pushes — those outward-facing, irreversible acts are the human's. This is the human gate (Rule 1): the skill prepares the artifact, the human triggers the publication.

The catalog edit and the candidate removal are **atomic in the working tree**: they happen together, ready to be committed as one unit. The candidate file is removed because its content has been promoted into the catalog — leaving it pending after a successful promotion would be a false signal. But the removal is reversible until the human commits (it is a working-tree deletion, not a pushed deletion), which is why removing the candidate before publication is safe.

On the isolated route, the state transitions are: candidate `pending` in `candidates/` → (after promotion) candidate removed from `candidates/` AND lens added/modified in `catalog.md`, both in the working tree → (after human commit) candidate gone, catalog published. On the structural route, the candidate stays `pending` — the promote skill does not touch it.

## Error handling

The promote skill degrades gracefully and reports failures explicitly. It never fails silently or leaves a half-applied state unannounced.

**Leak-audit failure:** block, flag the suspect content, edit nothing, stop. The candidate stays pending. Report the block and the suspect content so the author can re-generalize the candidate.

**Catalog edit failure (file lock, permissions, anything):** report the failure, do NOT attempt to remove the candidate file. The candidate stays pending. The working tree is unchanged. The author addresses the file-system issue and re-invokes promotion.

**skill-reviewer rejection:** report the reviewer's findings, do NOT remove the candidate file, do NOT commit over the rejection. The catalog edit sits in the working tree (reversible). The author addresses the findings (edit the catalog in place or revise the candidate) and either re-invokes promotion or commits manually.

**skill-reviewer unavailable (the `plugin-dev:skill-reviewer` agent is not installed or cannot be invoked):** treat it like a rejection — report that the review step could not run, leave the catalog edit in the working tree, and do NOT remove the candidate file. The review is not optional; never silently skip it and remove the candidate. The author installs the reviewer and re-invokes promotion, or reviews the edit by hand before committing.

**Candidate removal failure (after a successful catalog edit):** flag the half-applied state explicitly — the catalog edit succeeded, the removal failed. Report both file paths. Do NOT fail silently. The author removes the candidate file manually and commits both changes together.

**Malformed candidate (missing frontmatter, invalid `target`, unparseable):** report the malformation, do NOT guess, do NOT edit. A valid `target` is one of `review`, `verify`, `planning`, or `debug`; anything else is malformed. Ask the author to fix the candidate file and re-invoke promotion.

**Modify-nonexistent (`operation: modify` with `modifies: N` but `### N.` does not exist in the catalog):** stop, report the missing lens number, do NOT edit. The candidate likely cites the wrong number. Ask the author to correct the `modifies` field or change the operation to `add`.

**Add-duplicate (a lens with the same title or nearly identical principle already exists):** flag the duplication, suggest either converting the candidate to a `modify` operation (if the intent is to amend the existing lens) or dropping the candidate (if it is redundant). Do NOT silently add a duplicate lens.

**Ambiguous classification (cannot tell if isolated or structural):** default to structural, explain the ambiguity, ask the author which route applies. Do NOT edit when in doubt.

## Output

Report the contract: the caller knows what was done (isolated) or recommended (structural), the candidate disposition, and the reminder that commit/PR/push is the human's.

For an isolated promotion:

1. **Gate result:** leak-audit passed.
2. **Classification:** isolated — add (with assigned lens number and placement) or modify (with lens number edited in place).
3. **What was edited:** the catalog file path, the specific lens block added/modified, the skill-reviewer result (pass or findings).
4. **Candidate disposition:** removed from `candidates/` (or removal-failure flag if the removal failed).
5. **Human gate reminder:** the catalog edit and candidate removal are in the working tree; commit/PR/push is your decision.

For a structural promotion:

1. **Gate result:** leak-audit passed.
2. **Classification:** structural — cite the specific reason (new catalog needed, reorg required, rule change, numbering change).
3. **Recommendation:** summarize the candidate and recommend the brainstorm/spec/plan/review cycle for structural changes.
4. **Candidate disposition:** stays pending in `candidates/`.
5. **Human gate reminder:** structural changes require a full design cycle; this skill does not edit the catalog on the structural route.

For a blocked promotion (leak-audit failed):

1. **Gate result:** leak-audit blocked.
2. **Suspect content:** the specific text that triggered the block (employer name, service name, vendor, ticket ID, real number).
3. **What was edited:** nothing — the gate blocks before any edit.
4. **Candidate disposition:** stays pending.
5. **Next step:** re-generalize the candidate to remove the real specific, then re-invoke promotion.
