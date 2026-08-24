---
name: deliberate-engineering-promote
description: "Use on demand to drive a pending candidate into the catalog systematically. Runs the leak-audit gate, classifies isolated vs structural, then (isolated) edits the catalog append-only, routes the new lens from its selector, runs skill-reviewer and deletes the promoted candidate file from the queue, or (structural) stops and recommends the proper design cycle. This is the promotion step of the author contribution flow: it drives a candidate into the shared catalog (working tree only, gated). Writes, all in the plugin repository's working tree and never committed: the catalog file, the selector that routes it, the counts those catalogs are stated in (README and the architecture doc), both version manifests, the CHANGELOG, and `scripts/routing-exemptions.txt` when a lens is deliberately left unrouted, plus the deletion of the promoted candidate; it also runs the consistency script. It is not the contribute skill, which captures candidates, nor the adopter capture skill, which writes your personal override file. Stays silent unless invoked."
---

# Deliberate Engineering Promote

The third vertex of the authoring trio. Where `deliberate-engineering-capture` grows the adopter's personal override file, and `deliberate-engineering-contribute` captures generalizable judgment into clean candidate files in `candidates/`, this skill drives an approved candidate from the queue into the shipped catalog. It is the promotion half: systematically elevate a candidate through a blocking leak-audit gate, classify it as isolated or structural, route to the correct path, and stop at the human gate before commit. All catalog edits happen in the working tree only. The skill NEVER commits, opens a PR, or pushes: that irreversible, outward-facing act is the human's. Like `contribute`, this is contributor tooling: it runs against a local clone of the plugin repository and edits that repo's catalog files, not your own project.

## Boundaries

- **vs `contribute` (the capture half)**: `contribute` turns session judgment into a clean candidate in `candidates/`; this is the **promote** half. It takes a candidate from the queue, runs the gated promotion (leak audit, classify, catalog fit, routing, review), and edits the catalog and the selector that routes it, or recommends a design cycle. One gated pipeline, two skills.
- **vs `deliberate-engineering-capture` (the adopter side)**: capture grows your *personal, private* override file; this edits the *shared, shipped* catalog. Opposite write-targets.
- **On demand only**: never self-triggers; runs only via `/deliberate-engineering:promote` or an explicit request (e.g. "promote candidate X to the catalog"). No invocation → total silence.

## Flow overview

Five steps in sequence: (1) the leak-audit blocking gate audits the candidate for surviving real specifics FIRST; on suspicion it blocks and edits nothing; (2) classify the candidate as isolated (add/modify a lens in an existing catalog) or structural (new catalog, reorg, rule change, and every `target: rules` candidate by construction); (3a) the isolated route edits the catalog file append-only, routes the new lens from its selector, runs skill-reviewer, and removes the candidate file, all in the working tree; (3b) the structural route does NOT edit: it stops, summarizes why the candidate is structural, and recommends the proper brainstorm/spec/plan/build cycle, leaving the candidate pending; (4) the human gate: the skill ends WITHOUT commit/PR/push; (5) report what was done (isolated) or recommended (structural) and the candidate disposition. Nothing touches the catalog until the leak-audit gate passes.

## The leak-audit blocking gate

The first step, before any edit. Audit the candidate file for surviving real specifics: employer names, service names, vendor names, org structure, person names, ticket IDs, incident numbers, real quantities tied to one employer. This is a CHECK, not a scrub: the candidate was born generalized in `contribute`, so the presence of a real specific is a process failure that blocks promotion until the candidate is re-generalized.

On any suspicion (a name that looks like a service, a number that smells real, a vendor/tool name that ties to one employer's stack), the gate BLOCKS. The skill flags the suspect content, reports the block, and edits nothing. The candidate stays pending. The author fixes the leak in the candidate file and re-invokes promotion. The boundary is hard: nothing touches the catalog before the gate passes.

The gate audits the candidate file only: it does not audit the catalog itself (that is a separate maintenance act). Pass the gate → proceed to classify. Fail the gate → block, flag, edit nothing, stop.

## Classify: isolated vs structural

After the leak-audit gate passes, classify the candidate into one of two routes:

**Isolated:** the candidate adds a new lens to an existing catalog, or modifies an existing lens in place. The catalog file structure, the numbering system, and the group divisions stay unchanged. This is the common case: one lens in, one lens out, append-only.

**Structural:** the candidate requires a new catalog file, a reorganization of an existing catalog, a change to the numbering or grouping system, or a modification to the standing rules. Structural changes touch the plugin's architecture, not just its content, and they demand a full design cycle (brainstorm, spec, plan, build).

**`target: rules` is structural by construction**, whatever its `operation` and however small the wording change looks. A standing rule is constitutional content that every session loads, so it never takes the append-only catalog edit: send it to the design cycle.

On ambiguity (the candidate could be read either way, or you cannot tell which route applies), default to structural. Do NOT edit when in doubt; ask the author which route applies and wait for confirmation. The conservative default is structural (do not edit) to prevent silent catalog corruption.

## The isolated route: edit, route, review, remove

For an isolated candidate (add or modify), proceed with catalog promotion in the working tree:

### Locate the target catalog

Each catalog is one file under `plugins/deliberate-engineering/skills/`, and the candidate's frontmatter `target` field selects it: `target: review` → `review-strategy-selector/catalog.md`; `target: verify` → `verification-strategy-selector/catalog.md`; `target: planning` → `planning-strategy-selector/catalog.md`; `target: debug` → `debug-operate-strategy-selector/catalog.md`; `target: communication` → `communication-collaboration-selector/catalog.md`, the one whose directory is not named `<axis>-strategy-selector`. `target: rules` names no catalog and never reaches this route: it was classified structural above.

### Apply the operation append-only

Lenses are `### N. Title` blocks followed by three bullets (How it works / Objective / When most valuable), grouped into Parts (lettered sections like "Part A: Process / Meta-review Strategies"). Composition patterns are single numbered bullets in the appendix at the end, separately numbered from the lenses. The operation in the candidate frontmatter determines what to do.

**Match the shape of the catalog you are editing, not a remembered one.** Four catalogs (review, verification, planning, debug-operate) are Part-grouped with those three bullets. The communication catalog is different in two ways that matter here: it is **flat**, with no Parts at all, so there is no Part to place a lens under, and each lens carries a required fourth bullet, `**Tags:**` (the artifacts and audiences it applies to), which its selector reads to pick lenses. A communication lens written in the four-catalog shape is malformed and, worse, invisible to the selector that would have used it. Open the target catalog and copy the shape of the lenses already in it before writing anything.

**`kind: pattern`**. The candidate is a composition pattern, not a lens: it chains the phase's lenses rather than examining the artifact. It lands in the catalog's `## Appendix: Composition Patterns` as `- **N. Title:** one or two sentences`, appended with the next free pattern number, which is a namespace of its own (`review pattern #7` is not `review #7`). The four Part-grouped catalogs have that appendix; the communication catalog has a prose composition note instead and takes no pattern candidate, so stop and say so rather than inventing an appendix for it. A pattern is not finished until the selector's compose step cites it, the same obligation an added lens carries and enforced by the same invariant. Everything below about lens shape applies to `kind: lens`.

**`operation: add`**. The candidate is a wholly new lens. Before assigning a number, scan the catalog for an existing lens with the same title or a nearly identical principle; on a hit, do not add (see add-duplicate handling in "Error handling"). Otherwise assign the NEXT FREE NUMBER (scan the catalog for the highest existing `### N.` number and add one). PLACE the new lens block under the Part (group) that matches its theme: do NOT append at the end of the file; insert it in the thematically correct Part, even if that Part's numbers are no longer sequential. This is deliberate: a Part may run out of numeric order (its later-added lenses keep their assigned numbers rather than being renumbered) because append-only numbering is prioritized over reading-order. Write the new `### N. Title` block formatted identically to existing lenses in that catalog: the three bullets for a Part-grouped catalog, and for the flat communication catalog, no Part placement plus the required `**Tags:**` bullet.

**`operation: modify` with `modifies: N`**. The candidate amends an existing lens. Locate the `### N.` block in the catalog (where N matches the `modifies` field) and edit it in place. Do NOT change the number, do NOT move it to a different Part (the communication catalog has no Parts, so there is nothing to move it between; keep its `**Tags:**` bullet intact and current). If the amendment changes the title, change the title on the `### N.` line; if it adjusts a bullet, edit that bullet; if it adds a bullet, add it. The lens stays where it is, under its original number and Part. If `### N.` does not exist in the catalog, STOP: this is a modify-nonexistent error (see "Error handling").

### Route the new lens from its selector

A lens the selector never names is a lens never read: an agent opens only the sections a step points it to, so a catalog entry with no routing is shipped and unreachable. The same holds for a composition pattern, and it held so thoroughly that eight of them shipped in an appendix the selector said it applied and never cited. This has been the plugin's most repeated defect, fixed in v0.4.0, v0.4.1, v0.12.2 and v0.12.3. Those instances came from hand-authored catalog commits rather than from this flow. But this flow would produce the same state by construction, because it edited the catalog and stopped, and it is the one path where the gap can be closed instead of found later.

So an `add` is not finished until the new lens is reachable from `SKILL.md` in the same directory. For `kind: pattern`, that means the compose step, which cites every pattern by number and name; add yours to that enumeration rather than restating its text, since restating is what let the two copies drift. Put its number in the step that selects lenses, in the bullet whose trigger matches the lens's own "When most valuable", or in the ceremony-band or composition step when the lens governs depth or sequencing rather than a class of change. Read the target selector's own headings first: the five do not number their steps alike, and in the communication selector lens selection is Step 2, not Step 3. Do not invent a trigger: if the lens's own body names no condition a selector step could key on, that is a finding about the lens, not a licence to leave it unrouted.

If the lens genuinely should not be routed, say why in `scripts/routing-exemptions.txt`. That file is also where a Part routed as a whole group is declared. Invariant 9 in `scripts/check-invariants.py` fails on an unrouted, undeclared lens; on an exemption with no reason, stated twice, or naming a directory, Part or lens that does not exist; and on an exemption gone dead, whether because the selector now routes the lens or because a lens joined the Part a group exemption blankets. A citation has to carry the lens's identity: its number beside a word from its own title, a numbers-only parenthesis, or the number introduced by the word lens. A numeral loose in a sentence is not routing.

A `modify` does not require this, but check anyway: if the amendment changed the lens's trigger, the selector bullet that routes it may now be keyed to the wrong condition.

### Keep the counts and the harness green

Appending a lens changes numbers that several files state, and `scripts/check-consistency.sh` enforces them. Before handing the working tree over, from the repo root run `bash scripts/check-consistency.sh` with a bash 4 or newer (macOS ships bash 3.2 as `/bin/bash`, which cannot run it; use the one from your package manager) and fix what it names. Then run `python3 scripts/check-invariants.py --base origin/main` from the same root: it is the guard that proves the append-only numbering invariant above actually held, and that the lens you added is reachable from its selector; those are the two this flow can break. The obligations it enforces, so you can update them in the same edit rather than discovering them from a red run: the catalog's own intro count ("this catalog contains N"), the README's per-catalog count and its per-group parentheticals, the README's total across the four phase catalogs, and the communication count where the README and the architecture doc both state it. A change under `plugins/deliberate-engineering/` also requires a version bump in both manifests, in lockstep, and that pair is a separate CI gate. A CHANGELOG entry is required by convention and is not machine-checked, so nothing will stop you from forgetting it.

### Run skill-reviewer

After editing the catalog file in the working tree, invoke the `plugin-dev:skill-reviewer` agent to review the catalog file's quality. Pass the catalog file path resolved above, the selector file you routed it from, and the context that a new lens was added or an existing lens was modified. The reviewer checks for: consistency with existing lenses, formatting adherence, clarity of the principle, and whether the lens fits the catalog's voice.

If the skill-reviewer rejects the edit or flags a quality issue, report the findings and STOP. Do NOT proceed to remove the candidate file, do NOT commit over the rejection. The author addresses the reviewer's findings (either by editing the catalog in the working tree or by revising the candidate and re-promoting), then re-invokes promotion or commits manually.

### Remove the candidate file atomically

On skill-reviewer pass, and once the lens is routed or its exemption is stated, the final step of the isolated route is to remove the candidate file from `candidates/`. Do not remove it while the lens is still unrouted: an unreachable lens is not a promoted lens, and deleting the candidate is what makes the promotion look done. This is the atomic set: the catalog edit, the routing edit AND the candidate removal happen together in the working tree, ready to be committed as one unit by the human. The candidate file is removed because it has been promoted: its content now lives in the catalog.

On removal failure (permissions, file lock, anything), do NOT fail silently. Flag the half-applied state (the catalog edit succeeded, the candidate removal failed) and report both file paths so the author can remove the candidate manually. Never leave a half-applied state silently.

## The structural route: do not edit, recommend

For a structural candidate (one that requires a new catalog, a reorganization, a numbering change, or a rule modification, which includes every `target: rules` candidate), do NOT edit the catalog. The structural route is a stop-and-recommend: summarize the candidate, explain why it is structural (cite the specific reason: new catalog needed, reorg required, rule change), and recommend the proper design cycle. Structural changes are too invasive for an append-only skill to handle safely: they need the full brainstorm/spec/plan/build cycle that applies to any plugin architecture change.

The candidate file stays pending. The author takes the recommendation, runs the design cycle, and manually applies the structural change (or decides to drop it). The promote skill does not touch the catalog on the structural route: it only provides the analysis and the recommendation.

## The append-only invariant: never renumber existing lenses

This is a hard invariant binding all catalog edits: **NEVER renumber an existing lens.** Lens numbers are stable-for-life identifiers. Adopters cite them in override files (e.g., `review #35: disable`), selectors cite them in session notes, and documentation links to them by number. Renumbering `### 35.` to `### 36.` would silently break every override, every citation, every link that references #35. This breakage is invisible and irreversible: the override file would disable the wrong lens, and the adopter would never know.

The invariant has two corollaries:

1. **New lens = next free number, placed thematically.** A new lens gets the next available number (highest existing + 1) but is PLACED under the Part (group) that matches its theme, not necessarily at the end of the file. This is why a Part may have non-sequential numbers: a later-added lens keeps its high number while sitting in an earlier Part; new lenses are numbered sequentially but placed thematically. The number is the stable identifier; the physical location is for human reading.

2. **Modify = edit #N in place.** A `modify` operation edits the existing `### N.` block where it stands. It does NOT move the lens to a different Part, does NOT renumber it, does NOT reorder surrounding lenses. The lens stays under its original number and Part, even if the modification changes its title or content.

Renumbering is the one act this skill will never perform, under any circumstance. If a candidate implicitly requires renumbering (e.g., "insert this between #10 and #11"), classify it as structural and stop: that requires a reorg design, not an append-only edit.

## States, atomicity, the human gate

The promote skill edits the catalog, routes the lens from its selector, and removes the candidate file in the **working tree only**. It produces a git diff ready to be reviewed and committed by the human. It NEVER commits, NEVER opens a PR, NEVER pushes: those outward-facing, irreversible acts are the human's. This is the human gate (Rule 1): the skill prepares the artifact, the human triggers the publication.

The catalog edit, the routing edit and the candidate removal are **atomic in the working tree**: they happen together, ready to be committed as one unit. The candidate file is removed because its content has been promoted into the catalog: leaving it pending after a successful promotion would be a false signal. But the removal is reversible until the human commits (it is a working-tree deletion, not a pushed deletion), which is why removing the candidate before publication is safe.

On the isolated route, the state transitions are: candidate `pending` in `candidates/` → (after promotion) candidate removed from `candidates/` AND lens added/modified in `catalog.md` AND routed from `SKILL.md` or stated in `routing-exemptions.txt`, all three in the working tree → (after human commit) candidate gone, catalog published. On the structural route, the candidate stays `pending`: the promote skill does not touch it.

## Error handling

The promote skill degrades gracefully and reports failures explicitly. It never fails silently or leaves a half-applied state unannounced.

**Leak-audit failure:** block, flag the suspect content, edit nothing, stop. The candidate stays pending. Report the block and the suspect content so the author can re-generalize the candidate.

**Catalog edit failure (file lock, permissions, anything):** report the failure, do NOT attempt to remove the candidate file. The candidate stays pending. The working tree is unchanged. The author addresses the file-system issue and re-invokes promotion.

**skill-reviewer rejection:** report the reviewer's findings, do NOT remove the candidate file, do NOT commit over the rejection. The catalog edit sits in the working tree (reversible). The author addresses the findings (edit the catalog in place or revise the candidate) and either re-invokes promotion or commits manually.

**skill-reviewer unavailable (the `plugin-dev:skill-reviewer` agent is not installed or cannot be invoked):** treat it like a rejection: report that the review step could not run, leave the catalog edit in the working tree, and do NOT remove the candidate file. The review is not optional; never silently skip it and remove the candidate. The author installs the reviewer and re-invokes promotion, or reviews the edit by hand before committing.

**Candidate removal failure (after a successful catalog edit):** flag the half-applied state explicitly (the catalog edit succeeded, the removal failed). Report both file paths. Do NOT fail silently. The author removes the candidate file manually and commits both changes together.

**Malformed candidate (missing frontmatter, invalid `target`, unparseable):** report the malformation, do NOT guess, do NOT edit. A valid `target` is one of `review`, `verify`, `planning`, `debug`, `communication`, or `rules`; anything else is malformed. Ask the author to fix the candidate file and re-invoke promotion.

**Modify-nonexistent (`operation: modify` with `modifies: N` but `### N.` does not exist in the catalog):** stop, report the missing lens number, do NOT edit. The candidate likely cites the wrong number. Ask the author to correct the `modifies` field or change the operation to `add`, with your pick embedded (Rule 4): search the catalog for a lens already covering that ground, then recommend `modify` against the number you found, or `add` when nothing covers it.

**Add-duplicate (a lens with the same title or nearly identical principle already exists):** flag the duplication, suggest either converting the candidate to a `modify` operation (if the intent is to amend the existing lens) or dropping the candidate (if it is redundant). Do NOT silently add a duplicate lens.

**Ambiguous classification (cannot tell if isolated or structural):** default to structural, explain the ambiguity, ask the author which route applies. Do NOT edit when in doubt.

## Output

Report the contract: the caller knows what was done (isolated) or recommended (structural), the candidate disposition, and the reminder that commit/PR/push is the human's.

For an isolated promotion:

1. **Gate result:** leak-audit passed.
2. **Classification:** isolated. Add (with assigned lens number and placement) or modify (with lens number edited in place).
3. **What was edited:** the catalog file path, the specific lens block added/modified, the selector file and the bullet that now routes it (or the exemption stated for it in `scripts/routing-exemptions.txt`), the skill-reviewer result (pass or findings).
4. **Candidate disposition:** removed from `candidates/` (or removal-failure flag if the removal failed).
5. **Human gate reminder:** the catalog edit, the routing edit and the candidate removal are in the working tree; commit/PR/push is your decision.

For a structural promotion:

1. **Gate result:** leak-audit passed.
2. **Classification:** structural. Cite the specific reason (new catalog needed, reorg required, rule change, numbering change).
3. **Recommendation:** summarize the candidate and recommend the brainstorm/spec/plan/build cycle for structural changes.
4. **Candidate disposition:** stays pending in `candidates/`.
5. **Human gate reminder:** structural changes require a full design cycle; this skill does not edit the catalog on the structural route.

For a blocked promotion (leak-audit failed):

1. **Gate result:** leak-audit blocked.
2. **Suspect content:** the specific text that triggered the block (employer name, service name, vendor, ticket ID, real number).
3. **What was edited:** nothing (the gate blocks before any edit).
4. **Candidate disposition:** stays pending.
5. **Next step:** re-generalize the candidate to remove the real specific, then re-invoke promotion.
