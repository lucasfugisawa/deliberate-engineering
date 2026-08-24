---
name: deliberate-engineering-overrides
description: "Use at the start of an engineering session to pick up the operator's standing-rule overrides, and again whenever any deliberate-engineering lens is about to be applied. Reads ~/.claude/deliberate-engineering/overrides.md, honors disable/modify/add overrides on lenses, composition patterns and standing rules, offers operator-authored lenses alongside the shipped ones, and declares each deviation. Stays silent when no override file exists or no override matches."
---

# Deliberate Engineering Overrides

The deliberate layer of *your practice takes precedence*. Where the shipped skills carry judgment, this skill lets an operator's own practice override that content, wherever it is applied. It reads and honors overrides from a personal file (disabling lenses, appending to them, or injecting operator-authored strategies) and declares the deviation out loud.

## vs the runtime precedence that already exists

The harness and the rules skill already establish a precedence order: explicit user instruction beats a rule (CLAUDE.md > skills > system). That runtime precedence governs the **one-off**: an instruction in the current session overrides the default. This skill is the **declarative, addressable, persistent** form, for what the operator wants held across sessions. Rather than restating "ship it without stopping for approval" every time, the operator writes `Rule 1: modify` once, with a `**Add:**` annotation scoping the loosening to a named environment, and this skill applies it on every relevant session. This makes the runtime precedence durable, not a replacement for it.

## vs the write side

This skill is the **read side** of the override layer. It consults the file, honors the overrides, and declares them. Growing the file from observed practice (noticing that an operator routinely overrides planning #12, offering to persist that preference, and writing the entry) is the **write side**, a separate capability owned by the `deliberate-engineering-capture` skill (invoked on demand via `/deliberate-engineering:capture`). The boundary holds regardless: *this* skill only reads and applies overrides; it never writes them. The capture skill writes only on demand, only with approval, and only by appending, never by editing what is already there.

## What is a target, and what is architecture

Overrides target **named catalog lenses** (review #35, planning #12), **composition patterns** (review pattern #7, verification pattern #4), and **standing rules** (Rule 1, Rule 2). A composition pattern prescribes how the lenses of a phase chain together, which is method rather than dispatch, so it is content on the same footing as a lens: an operator who closes with two fresh passes, or who folds remediation into discovery, is expressing exactly the practice this layer holds. The communication catalog carries a prose composition note rather than a numbered list, so it has no pattern targets. Two things are deliberately not targets: the router's four routing axes (clarity, risk, reversibility, reach) and its genre → phase-sequence mapping. Those are the classification the whole dispatch rests on, so they are architecture rather than content, and this mechanism does not reach them.

The exemption is about *those two objects*, not about the router as a skill. The router does apply a named lens by citation: its ceremony-band step cites planning #10 for the method. Where it does, that lens's override applies exactly as it would inside the selector that owns the lens. An operator who has overridden planning #10 gets that override honored when the band is set, not only later when the planning selector runs.

## When to use

Two kinds of content, reached two different ways, because they fail in opposite directions.

1. **Standing rules, once at session start.** `deliberate-engineering-rules` takes this file's standing-rule entries (`Rule N: <operation>` and `add: rules`) before any work is classified, and `deliberate-engineering-conduct` does the same as it authors a contract, since a conduction can be invoked without the rules skill having run. Reading the file shows you its catalog entries too: note them and leave them unapplied. An unread standing rule is an absent one, which is why this does not wait for a lens to be selected.
2. **Catalog lenses, when they are applied.** Every skill that applies a numbered lens consults first: the five selectors, `conduct` at its contract fields, `orchestrate` at decomposition, the router at its ceremony band. An unread `disable` or `modify` leaves the stricter shipped text in force. An unread `add: <catalog>` entry does not: it is an operator-authored lens, and unread it is simply absent. It stays on demand anyway, since only the applier that opens that catalog can judge whether its `**When:**` fits, and the case that would actually hurt (an added lens whose body relaxes a gate) is caught by content in the declaration protocol below. The residual gap is real and bounded: an applier that skips its consult leaves an added lens unapplied and unmentioned.

**The honest limit.** Both paths depend on a skill firing. For adopters running the README's always-on recipe, the rules read happens every engineering session; otherwise it rides description matching, and a session where the rules skill does not load is a session where standing-rule overrides go unread. This skill can also fire on its own description as a last backstop. The file cannot make a skill fire.

When the file does not exist, this skill does nothing and says nothing. Override is opt-in.

## The override file

The override file lives at `~/.claude/deliberate-engineering/overrides.md`. Each entry has a header in one of three forms (`<target>: <operation>` for a specific lens, composition pattern or rule, `add: <catalog>` for an operator-authored lens, or `add: <catalog> pattern` for an operator-authored composition pattern) followed by a body that depends on the operation.

```markdown
## review #35: disable

**Why:** We run a separate simplification pass after the deliberate review.

## Rule 1: modify

**Add:** For deploys to the staging environment, skip the human gate. The rollback is instantaneous and the blast radius is the team.

## planning #12: modify

**Add:** For changes scoped to a single aggregate, verify the sequence only at the aggregate boundary, not at every internal step.

## add: review

**Name:** Public API schema validation

**When:** The change touches a public API contract and adds a new field.

**Apply:** Check the OpenAPI schema generation: confirm the new field appears in the generated schema with the correct type, that required-vs-optional matches the code, and that the example value (if present) is realistic. Remind the operator that clients relying on a fixed schema version will not see the field until they opt in to the new version.

## add: rules

**Name:** Commit message convention enforcement

**Apply:** On every commit message, check that the subject line follows the project's convention: imperative mood, lowercase, no trailing period, under 72 characters. Offer to rewrite it if it does not match, never silently skip.
```

**Reading contract:**
- Headers are `## <target>: <operation>` where target is `review #N`, `planning #N`, `verification #N` or `verify #N`, `debug-operate #N` or `debug #N`, `communication #N`, `<catalog> pattern #N` for a composition pattern, or `Rule N`, and operation is `disable`, `modify`, or `add`. A catalog may be cited by its catalog name or its command name (`verify` and `verification` mean the same catalog, as do `debug` and `debug-operate`), since this file is read by an agent, not a parser.
- For an `add` that contributes a composition pattern rather than a lens, the header is `## add: <catalog> pattern`, and the body takes the same fields as a catalog `add`. For all other `add` entries, the header is `## add: <catalog>` where catalog is `review`, `planning`, `verification` or `verify`, `debug-operate` or `debug`, `communication`, or `rules`.
- **disable** body: `**Why:**` (optional), the operator's note on why this lens, pattern or rule is skipped.
- **modify** body: `**Add:**` (required), the annotation to read alongside the shipped lens, pattern or rule text; the shipped text stays intact.
- **add** body: `**Name:**` (required), the strategy's name for reference; `**When:**` (required for a catalog `add`), when to apply this operator-authored lens; `**Apply:**` (required), the lens content itself.
- **`add: <catalog> pattern` and `add: rules` are the exceptions on `**When:**`**, and deliberately so: a standing rule holds unconditionally, the way the shipped nine do, and a composition pattern holds unconditionally too, the way the shipped ones do (every compose step says to apply them, and not one of them states a when-condition). Neither has a when-condition to state. `**Name:**` and `**Apply:**` are required; `**When:**` is optional, and where an operator writes one it is read as *scope* (the environment or class of work the rule covers), never as a gate that must be satisfied before the rule counts. A missing `**When:**` on an `add: rules` entry is correct, not malformed, and must never be treated as an ambiguity to stop and ask about: this is the entry most likely to carry a safety instruction, and turning it into a question at session start would defeat the read.

If the file does not exist, this skill is silent and does nothing. Override is opt-in.

**Older files still read.** Earlier versions of this skill documented the header separator as an em-dash (`## review #35 — disable`). Both forms are understood: the file is read as prose by an agent at inference time, not parsed, so an override file written against the older documentation keeps working and does not need to be rewritten.

## The three operations

- **disable**: when a selected lens, composition pattern or rule is disabled, do not apply it. In the output, say it was skipped because the operator disabled it, quoting the operator's `**Why:**` if present. The lens is not evaluated; its text is not read. It is as if the selector never picked it.

  **What a disable removes is a method, never a required field.** Where a skill's own contract requires an artifact and cites a lens for *how* to produce it, disabling the lens removes the method, not the obligation: the conductor contract requires a verified recovery path whether or not verify #14 is disabled, and the field still has to be filled by some other means the operator names. Say so when this happens, rather than reporting the field as satisfied or quietly dropping it.

- **modify (append-only)**: the shipped lens, pattern or rule text stays intact; read the operator's `**Add:**` annotation alongside it and apply both. **modify never rewrites the shipped text; it appends**, which is what keeps the override from rotting when the lens evolves in a future version of the plugin. That is a statement about the *file*, not about behavior: an annotation is free to narrow, widen, or redirect what the lens asks for, and the plugin's own example does exactly that (`planning #12: modify`, "verify the sequence only at the aggregate boundary, not at every internal step"). Read the shipped text in full, then honor the `**Add:**` annotation alongside it, and **where the two conflict, the annotation governs**: it is the operator's practice, which is the whole premise of this layer. One limit, judged by content and not by the header: an annotation reaches only the lens it is attached to. Where its body would instead change something this mechanism does not target (removing a phase from the router's sequence, redefining a routing axis), honor the rest of the annotation, decline that clause, and say which clause you declined and why. Addressing a lens does not extend an override's reach to the architecture behind it. Say what changed in the declaration, so a narrowing is visible rather than silently absorbed. What you must not do is quietly drop the annotation as "inert because the shipped text says otherwise", or report it as applied when it was not. The ability to cite stable identifiers like `review #35` or `Rule 1` depends on the plugin's append-only numbering policy: shipped content is never renumbered, only appended.

- **add**: an operator-authored strategy, composition pattern or rule that maps to no shipped number. A pattern `add` composes the phase's lenses rather than examining the artifact, so it applies at the compose step where the shipped patterns apply. Treat any other one as one more available lens in the named catalog, or, for `add: rules`, as one more standing rule, held for the whole session exactly like a shipped rule once the session-start read has picked it up (see "When to use" for who does that read and what it depends on). Read the `**When:**` text as human-readable guidance for when it applies, interpreted by you, not a formal condition to evaluate. The selector's classification and selection logic runs as normal, considering the `add` entries as part of the catalog. If an `add` entry's `**When:**` guidance fits the work, apply its `**Apply:**` content exactly as you would apply a shipped lens.

## The awareness step

The flow when this skill is invoked:

**For standing rules, once per session:**

1. The rules skill consults this skill at the start of an engineering session, before any work is classified. `deliberate-engineering-conduct` does the same as it authors a contract, since a conduction can be invoked without the rules skill having run and is where an unread loosening changes who pulls a trigger.
2. This skill reads `~/.claude/deliberate-engineering/overrides.md` if it exists and returns the standing-rule entries: `Rule N` overrides and `add: rules` entries. Catalog-lens entries are left for their appliers.
3. Those entries are held for the session alongside the shipped nine, and declared when they change behavior.

**For catalog lenses, per applier:**

1. The applier does its own work normally, using the shipped catalogs: a selector classifies and picks lenses, `conduct` authors its contract fields, `orchestrate` decomposes, the router sets the band. Not all of them are selectors, and not all of them "select": what they share is that they apply a numbered lens.
2. The applier consults this skill. This skill reads the file if it exists.
3. For each applied lens or pattern with an override, this skill applies the operation instead of the shipped content. Separately, and not conditioned on anything the applier selected, it offers every `add: <catalog>` entry for that catalog as an additional operator-authored lens, and every `add: <catalog> pattern` entry as an additional composition pattern at the compose step, applied when its `**When:**` guidance fits the work. An `add` entry maps to no shipped number, so a consult that only looks up the selected lenses will never find one: look for them explicitly.
4. This skill declares the deviation in the visible output: **always, never silent.** Every override that fires is reported.

This skill does not re-run the applier's own judgment; it honors what the applier chose and applies the overrides to those choices. For `add` entries, the applier's existing classification (its own axes, whichever it uses, plus the lenses it applied) informs whether the `add` entry's `**When:**` guidance fits; this skill does not second-guess that judgment.

## The declaration protocol

When an override fires, declare it in the visible output. The firmness of the declaration scales to the risk of the override:

- **Common override** (disabling or modifying a catalog lens): a one-line factual note. Example: *"Override active: review #35 disabled (your note: team runs a separate simplification pass). Skipping."* State what was overridden, which operation was applied, and if `**Why:**` is present, quote it.

- **Safety-loosening override (keyed to content, not the header string)**: an elevated-autonomy acknowledgement. This fires for *any* override whose content relaxes a safety rail, the human gate on an irreversible/outward action (Rule 1) or the read-only posture on a system you don't own (Rule 2), regardless of how it is addressed: a literal `Rule 1: modify`, an `add: rules` entry ("for staging, proceed without approval"), or even an `add: <catalog>` lens whose content says "skip the gate here." Do **not** classify a gate-loosening `add` entry as a common one-line note just because its header is not literally `Rule 1`/`Rule 2`. Judge the content. Example: *"Override active: you've loosened Rule 1 for deploys to staging. I'm proceeding without the human gate as you've instructed. This is elevated autonomy; speak up if this is unintended."* State the override, the implication (what behavior changes), and proceed: acknowledgement with an explicit invitation to interrupt, not a request for permission. Do not re-ask permission every session: the operator chose this once, and re-asking turns that into a recurring toll. Do not treat the acknowledgement as a formality either. `deliberate-engineering-capture` takes an explicit confirmation when it writes such an entry, but a hand-written file never had one, so this may be the first time the operator sees, in behavior terms, what they wrote. Rule 1 and Rule 2 are the plugin's safety rails, and loosening them is the operator's right, but it must be explicit and acknowledged, never silent.

The no-silent stance mirrors the plugin's existing no-silent-truncation ethic: when the plugin's behavior deviates from the default, whether by compacting a context or by honoring an override, that deviation is declared, not hidden. Silence is not an option.

## Safety rules are overridable

Rule 1 (the human gate on irreversible and outward-facing actions) and Rule 2 (read-only posture on systems you do not own) can be overridden like any other content in the plugin. It is the operator's machine. Refusing to honor an override of Rule 1 or Rule 2 would be paternalistic and would contradict the plugin's premise: the machine is theirs, and the judgment layer is there to help, not to constrain. This skill does not refuse safety-rule overrides; it honors them and acknowledges the elevated autonomy per the declaration protocol above.

The boundary: honoring an override is not the same as treating it as routine. A common override gets a factual note; a safety-rule override gets an explicit acknowledgement and a standing invitation to interrupt. The operator has the final say, and the plugin makes that say legible, at the moment it is written and again every time it fires.

## Ambiguity and conflict

If an override is ambiguous, malformed, or contradicts another override, do not guess. Name the conflict, describe why it is undecidable, and ask one question with an embedded recommendation, the Rule 4 posture. Never silently skip an override because it is unclear; that would be the same as ignoring it, which defeats the purpose of having a durable override file. Examples of conflict: two `modify` entries for the same lens with contradictory `**Add:**` annotations; an `add: <catalog>` lens entry with no `**When:**` field, or any `add` entry with no `**Apply:**` field (a missing `**When:**` on `add: rules` is correct, not a conflict); a `disable` and a `modify` for the same target in the same file. Ask once, recommend a resolution, proceed when the operator clarifies.

## Coexistence and precedence

This skill turns the plugin's "coexistence with precedence" stance inward, applied to the plugin's own content. The runtime precedence (user instruction > skill > system) already exists and governs the one-off; this skill makes it persistent and addressable. It leans on that precedence rather than replacing it. When an explicit user instruction in the current session contradicts a persistent override from the file, the instruction wins, the same precedence order the rules skill already follows. The override file is durable preference, not an immutable mandate. Adding this skill requires removing nothing; the selectors and the rules skill continue to work as they do now, and invoking this skill is a one-line addition to each.

## Output

When an override fired, report which target(s) were overridden, the operation applied, what changed where a `modify` annotation conflicted with the shipped text, and, for a safety-rule override, the elevated-autonomy acknowledgement with its invitation to interrupt. A standing rule read at session start is reported when it changes behavior, not merely because it was read. When no override file exists or no override matched the selected lenses or the patterns being composed, report nothing. This skill is silent by default and speaks only when an override changes behavior.
