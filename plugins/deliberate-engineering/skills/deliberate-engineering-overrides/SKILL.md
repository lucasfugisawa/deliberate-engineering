---
name: deliberate-engineering-overrides
description: "Use when applying any deliberate-engineering lens or standing rule. Reads ~/.claude/deliberate-engineering-overrides.md before applying catalog lenses or standing rules, honors disable/modify/add overrides, and declares each deviation. Stays silent when no override file exists or no override matches."
---

# Deliberate Engineering Overrides

The deliberate layer of *your practice takes precedence*. Where the four selectors and the rules skill ship judgment, this skill lets an operator's own practice override that shipped content. It reads and honors overrides from a personal file — disabling lenses, appending to them, or injecting operator-authored strategies — and declares the deviation out loud.

## vs the runtime precedence that already exists

The harness and the rules skill already establish a precedence order: explicit user instruction beats a rule (CLAUDE.md > skills > system). That runtime precedence governs the **one-off** — an instruction in the current session overrides the default. This skill is the **declarative, addressable, persistent** form, for what the operator wants held across sessions. Rather than restating "ship it without stopping for approval" every time, the operator writes `Rule 1 — modify` once, with a `**Add:**` annotation scoping the loosening to a named environment, and this skill applies it on every relevant session. This makes the runtime precedence durable, not a replacement for it.

## vs the write side

This skill is the **read side** of the override layer. It consults the file, honors the overrides, and declares them. Growing the file from observed practice — noticing that an operator routinely overrides planning #12, offering to persist that preference, and writing the entry — is the **write side**, a separate capability owned by the `deliberate-engineering-capture` skill (invoked on demand via `/deliberate-engineering:capture`). The boundary holds regardless: *this* skill only reads and applies overrides; it never writes them. The capture skill writes only on demand, only with approval, and only by appending — never by editing what is already there.

## The router is not a target

The router is dispatch, not named content. It classifies work and invokes the selector that owns the method; it applies no lenses of its own. Overrides target **named catalog lenses** (review #35, planning #12) and **standing rules** (Rule 1, Rule 2), not the router. The router's classification axes (clarity, risk, reversibility, reach) and its genre → phase-sequence mapping are part of the plugin's judgment architecture and are not overridable by this mechanism.

## When to use

Use this skill whenever a selector or the rules skill is about to apply content and an override file may be present. It is triggered two ways:

1. **Primary trigger** — a one-line pointer in each selector and the rules skill: before applying selected lenses or rules, consult this skill.
2. **By-description trigger** — when an override file is present and a request involves applying deliberate-engineering content.

The selectors and the rules skill own the decision to invoke this skill; it does not decide for itself whether to run. When invoked, it reads the file if it exists, applies any relevant overrides, and reports them. When the file does not exist, this skill does nothing and says nothing — override is opt-in.

## The override file

The override file lives at `~/.claude/deliberate-engineering-overrides.md`. Each entry has a header in one of two forms — `<target> — <operation>` for a specific lens or rule, or `add — <catalog>` for an operator-authored strategy — followed by a body that depends on the operation.

```markdown
## review #35 — disable

**Why:** We run a separate simplification pass after the deliberate review.

## Rule 1 — modify

**Add:** For deploys to the staging environment, skip the human gate — the rollback is instantaneous and the blast radius is the team.

## planning #12 — modify

**Add:** For changes scoped to a single aggregate, verify the sequence only at the aggregate boundary, not at every internal step.

## add — review

**Name:** Public API schema validation

**When:** The change touches a public API contract and adds a new field.

**Apply:** Check the OpenAPI schema generation: confirm the new field appears in the generated schema with the correct type, that required-vs-optional matches the code, and that the example value (if present) is realistic. Remind the operator that clients relying on a fixed schema version will not see the field until they opt in to the new version.

## add — rules

**Name:** Commit message convention enforcement

**Apply:** On every commit message, check that the subject line follows the project's convention: imperative mood, lowercase, no trailing period, under 72 characters. Offer to rewrite it if it does not match, never silently skip.
```

**Reading contract:**
- Headers are `## <target> — <operation>` where target is `review #N`, `planning #N`, `verification #N` or `verify #N`, `debug-operate #N` or `debug #N`, or `Rule N`, and operation is `disable`, `modify`, or `add`. A catalog may be cited by its catalog name or its command name — `verify` and `verification` mean the same catalog, as do `debug` and `debug-operate` — since this file is read by an agent, not a parser.
- For `add` entries, the header is `## add — <catalog>` where catalog is `review`, `planning`, `verification` or `verify`, `debug-operate` or `debug`, or `rules`.
- **disable** body: `**Why:**` (optional) — the operator's note on why this lens is skipped.
- **modify** body: `**Add:**` (required) — the annotation to read alongside the shipped lens/rule text; the shipped text stays intact.
- **add** body: `**Name:**` (required) — the strategy's name for reference; `**When:**` (required) — when to apply this operator-authored lens; `**Apply:**` (required) — the lens content itself.

If the file does not exist, this skill is silent and does nothing. Override is opt-in.

## The three operations

- **disable** — when a selected lens or rule is disabled, do not apply it. In the output, say it was skipped because the operator disabled it, quoting the operator's `**Why:**` if present. The lens is not evaluated; its text is not read. It is as if the selector never picked it.

- **modify (append-only)** — the shipped lens or rule text stays intact; read the operator's `**Add:**` annotation alongside it and apply both. **modify never replaces the shipped text; it appends.** This is what keeps the override from rotting when the lens evolves in a future version of the plugin. The shipped lens remains the baseline; the operator's annotation refines or scopes it for their context. When applying a modified lens, read the shipped text in full, then read the operator's `**Add:**` annotation alongside it and honor both — the shipped baseline plus the operator's refinement. Never replace the shipped text; always read both. The ability to cite stable identifiers like `review #35` or `Rule 1` depends on the plugin's append-only numbering policy — shipped content is never renumbered, only appended.

- **add** — an operator-authored strategy or rule that maps to no shipped number. Treat it as one more available lens in the named catalog (or one more standing rule for `add — rules`). Read the `**When:**` text as human-readable guidance for when it applies, interpreted by you — not a formal condition to evaluate. The selector's classification and selection logic runs as normal, considering the `add` entries as part of the catalog. If an `add` entry's `**When:**` guidance fits the work, apply its `**Apply:**` content exactly as you would apply a shipped lens.

## The awareness step

The flow when this skill is invoked:

1. The selector classifies the work and picks its lenses normally, using the shipped catalogs.
2. The selector consults this skill. This skill reads `~/.claude/deliberate-engineering-overrides.md` if the file exists.
3. For each selected lens with an override, this skill applies the operation instead of the shipped content. For `add` entries in the relevant catalog, this skill reads them as additional operator-authored lenses available in that catalog, applied when their `**When:**` guidance fits the work.
4. This skill declares the deviation in the visible output — **always, never silent.** Every override that fires is reported.

This skill does not re-run the selector's classification logic; it honors the selector's choices and applies the overrides to those choices. For `add` entries, the selector's existing classification (the four axes, the picked lenses) informs whether the `add` entry's `**When:**` guidance fits; this skill does not second-guess that classification.

## The declaration protocol

When an override fires, declare it in the visible output. The firmness of the declaration scales to the risk of the override:

- **Common override** (disabling or modifying a catalog lens) — a one-line factual note. Example: *"Override active: review #35 disabled (your note: team runs a separate simplification pass). Skipping."* State what was overridden, which operation was applied, and if `**Why:**` is present, quote it.

- **Safety-rule override (Rule 1 or Rule 2)** — an elevated-autonomy acknowledgement. Example: *"Override active: you've loosened Rule 1 for deploys to staging — I'm proceeding without the human gate as you've instructed. This is elevated autonomy; speak up if this is unintended."* State the override, the implication (what behavior changes), and proceed — this is acknowledgement with an explicit invitation to interrupt, not a request for permission. Rule 1 and Rule 2 are the plugin's safety rails, and loosening them is the operator's right, but it must be explicit and acknowledged, never silent.

The no-silent stance mirrors the plugin's existing no-silent-truncation ethic: when the plugin's behavior deviates from the default — whether by compacting a context or by honoring an override — that deviation is declared, not hidden. Silence is not an option.

## Safety rules are overridable

Rule 1 (the human gate on irreversible and outward-facing actions) and Rule 2 (read-only posture on systems you do not own) can be overridden like any other content in the plugin. It is the operator's machine. Refusing to honor an override of Rule 1 or Rule 2 would be paternalistic and would contradict the plugin's premise: the machine is theirs, and the judgment layer is there to help, not to constrain. This skill does not refuse safety-rule overrides; it honors them and acknowledges the elevated autonomy per the declaration protocol above.

The boundary: honoring an override is not the same as treating it as routine. A common override gets a factual note; a safety-rule override gets an explicit acknowledgement and a confirmation check. The operator has the final say, and the plugin makes that say legible.

## Ambiguity and conflict

If an override is ambiguous, malformed, or contradicts another override, do not guess. Name the conflict, describe why it is undecidable, and ask one question with an embedded recommendation — the Rule 4 posture. Never silently skip an override because it is unclear; that would be the same as ignoring it, which defeats the purpose of having a durable override file. Examples of conflict: two `modify` entries for the same lens with contradictory `**Add:**` annotations; an `add` entry with no `**When:**` or no `**Apply:**` field; a `disable` and a `modify` for the same target in the same file. Ask once, recommend a resolution, proceed when the operator clarifies.

## Coexistence and precedence

This skill turns the plugin's "coexistence with precedence" stance inward — applied to the plugin's own content. The runtime precedence (user instruction > skill > system) already exists and governs the one-off; this skill makes it persistent and addressable. It leans on that precedence rather than replacing it. When an explicit user instruction in the current session contradicts a persistent override from the file, the instruction wins — the same precedence order the rules skill already follows. The override file is durable preference, not an immutable mandate. Adding this skill requires removing nothing; the selectors and the rules skill continue to work as they do now, and invoking this skill is a one-line addition to each.

## Output

When an override fired, report which target(s) were overridden, the operation applied, and — for a safety-rule override — the elevated-autonomy acknowledgement with confirmation check. When no override file exists or no override matched the selected lenses, report nothing. This skill is silent by default and speaks only when an override changes behavior.
