---
name: deliberate-engineering-capture
description: "Use on demand to capture what you did this session into durable overrides. Observes the full session transcript on disk (operator-typed messages only, extracted to a temporary working directory that it does not delete, then mined via subagent fan-out) for deviations (you corrected/skipped a catalog lens or rule), patterns (recurring practice the catalog lacks), and calibration adjustments (recurring ceremony heavier/lighter than the default for a class of work), discusses candidates, and on approval appends disable/modify/add entries to ~/.claude/deliberate-engineering/overrides.md. This is the adopter's write side: it grows YOUR personal override file. It is not the author contribution tools (contribute/promote), which propose lenses for the shared catalog. Stays silent unless invoked."
---

# Deliberate Engineering Capture

The adopter write side of the override layer. Where `deliberate-engineering-overrides` reads the personal override file and honors it at runtime, this skill helps you grow that file from what you actually did. It watches for three signals, deviations from the catalog (you skipped or corrected a lens/rule), patterns beyond it (you brought a recurring practice the catalog lacks), and calibration adjustments (you repeatedly ran a class of work heavier or lighter than the recommended ceremony), proposes override entries, and on approval appends them to `~/.claude/deliberate-engineering/overrides.md`.

## Boundaries

- **vs `deliberate-engineering-overrides` (the read side)**: that skill consults the file and honors overrides at runtime; this skill *proposes and appends* entries from observed signals. Different directions, same file.
- **vs `contribute`/`promote` (the author tools)**: those grow the *shared, shipped* catalog (a product act, with leak audit); this grows your *personal, private* override file at `~/.claude/deliberate-engineering/overrides.md`. Opposite targets.
- **On demand only**: never self-triggers; runs only via `/deliberate-engineering:capture` or an explicit request (e.g. "capture what we did as an override," "add this to my overrides"). No invocation → total silence; it never proposes overrides unprompted.

## What it observes

Three signals, all drawn from the **full session transcript on disk** (see "Where it reads from: the session transcript"), not the live context window:

1. **Deviations**: a catalog lens or standing rule was applicable, and you corrected it, skipped it, or contradicted it. The lens said one thing; you did another, with signs of intent (not a one-off accident). Candidate for `disable` if you rejected the lens outright, or `modify` if you used it with a recurring adjustment.

2. **Patterns**: a recurring practice or strategy you brought that the catalog lacks. Something you applied consistently, explained clearly, and that has the shape of a lens (a named strategy with a when-to-apply condition). Candidate for `add`.

3. **Calibration adjustments**: for a recognizable *class* of work, you repeatedly ran a ceremony depth different from the plugin's recommendation, with intent: consistently skipping a phase the router would have sequenced, or demanding full depth on a class the plugin would call standard. This is not a single-lens deviation: it is a recurring preference about *how much* process a class of work earns. Candidate for `planning #10: modify` (the calibrate-ceremony-to-risk lens), or `add: rules` for a standing calibration posture.

What does NOT produce a signal: a behavior seen once with no sign of intent, or a signal with no clear addressable target. One-session noise is dropped; recurring practice with intent is elevated.

## Where it reads from: the session transcript

The signals are drawn from the **full session transcript on disk**, not the live context window. The live window shrinks and compacts as you work; the transcript is durable. Reading from disk means capture sees the whole session even when invoked late, and compacting the live context never harms it. (This is why capture needs no "compact first" ritual: the raw material lives on disk, and the heavy reading is offloaded to subagents.)

**Scope.** By default, read only the **current session**. Widen to the whole project only when the operator explicitly asks (e.g., "capture across all my sessions on this project"). Never widen without an explicit request.

**Step 1: Resolve the transcript.** The current session id is in `CLAUDE_CODE_SESSION_ID`. Find the transcript by searching for that filename. Do NOT reconstruct the encoded project-dir path (it replaces both `/` and `.` with `-` and is fragile):

```bash
TRANSCRIPT=$(find ~/.claude/projects -name "$CLAUDE_CODE_SESSION_ID.jsonl" -not -path "*/subagents/*" | head -1)
```

Compaction appends to the same file, so this one file holds the full history. For project scope, gather all `*.jsonl` directly under the project's `~/.claude/projects/<encoded>` directories (there may be several, one per worktree), excluding `subagents/`. If `$TRANSCRIPT` comes back empty, stop here and follow **Degradation** below instead of proceeding to Step 2.

**Step 2: Filter to the operator's voice.** Keep only the operator's typed messages; drop agent output, tool-results, and harness-injected messages. Establish a scratchpad directory for the intermediate artifacts (create one if you don't already have a session scratchpad):

```bash
SCRATCH=$(mktemp -d)
```

Then write the result to a scratchpad file:

```bash
python3 - "$TRANSCRIPT" > "$SCRATCH/operator_messages.txt" <<'PY'
import json, sys, re
WRAPPER_RE = re.compile(r'<(command-name|command-message|command-args|local-command-stdout|system-reminder)>.*?</\1>', re.DOTALL)
def extract_text(content):
    if isinstance(content, str): return content
    if isinstance(content, list):
        return '\n'.join(b.get('text','') for b in content if isinstance(b, dict) and b.get('type')=='text')
    return ''
for line in open(sys.argv[1]):
    line = line.strip()
    if not line: continue
    try: o = json.loads(line)
    except Exception: continue
    if o.get('type') != 'user': continue
    if o.get('isMeta') or o.get('isSidechain'): continue
    origin = o.get('origin')
    if isinstance(origin, dict) and origin.get('kind') not in (None, 'human'): continue
    c = o.get('message', {}).get('content')
    if isinstance(c, list) and any(isinstance(b, dict) and b.get('type')=='tool_result' for b in c): continue
    t = WRAPPER_RE.sub('', extract_text(c)).strip()
    if not t: continue
    print(t)
    print("\x00", end="")   # NUL record separator between messages
PY
```

The predicate: `type == "user"`, `origin.kind` is `human` (harness-injected messages like task-notifications carry a different `origin.kind` and are dropped; older transcripts without an `origin` field fall through this check), textual content (not a `tool_result`), `isMeta` false, `isSidechain` false, with `<command-*>`/`<local-command-stdout>`/`<system-reminder>` wrappers stripped and now-empty messages dropped. Agent output, tool-results, and harness notifications never pass.

**Step 3: Chunk to scratchpad.** Split `operator_messages.txt` (on the NUL separator) into chunk files small enough to fit a subagent context (on the order of a few hundred messages per chunk, fewer if messages run long), e.g. `$SCRATCH/chunk_001.txt`, `chunk_002.txt`, …. Keep only the chunk paths and message counts in your own context; never load the raw operator text into the main thread.

**Step 4: Fan-out mine and consolidate.** Dispatch one subagent per chunk (Task tool). Give each the chunk-file path and this brief:

> Read these operator-typed messages. Identify three kinds of signal: (a) **deviations**: a catalog lens or standing rule was applicable and the operator corrected, skipped, or contradicted it, with signs of recurring intent (not a one-off); (b) **patterns**: a recurring practice or strategy the operator brought that the catalog lacks; and (c) **calibration adjustments**: for a recognizable class of work, the operator repeatedly chose a ceremony depth heavier or lighter than the plugin's recommendation, with intent (e.g. consistently skipping a phase, or demanding full depth on a routine change). Return ONLY structured candidates. For each: the signal (one sentence), the supporting quoted operator lines, and the kind (deviation | pattern | calibration). Return nothing for one-off noise with no sign of intent.

Collect every subagent's returned candidates and **deduplicate** overlapping signals across chunks before triage.

**Degradation.** If `CLAUDE_CODE_SESSION_ID` is unset, the transcript is not found, or it cannot be read, fall back to observing the live context (the pre-refactor behavior) and **say so explicitly** in the output. Never fail silently.

## Triage and mapping

For each observed signal, identify the addressable target and the operation:

- **Targets** use the canonical form: `review #N`, `verify #N`, `planning #N`, `debug #N`, `communication #N`, `Rule N` for specific lenses/rules; or `add: <catalog>` for operator-authored strategies where catalog is `review`, `planning`, `verify`, `debug`, `communication`, or `rules`.
- **Operations** are `disable`, `modify`, or `add`.
- **A calibration adjustment** maps to `planning #10: modify` (annotate the recurring ceremony adjustment for that class of work) or `add: rules`. It never targets the router's classification axes (clarity / risk / reversibility / reach) **or its genre to phase-sequence mapping**: both are the plugin's architecture, not overridable content, so an override may make a phase lighter but never removes one from the sequence. The override rides on the *ceremony lens*, not on the classifier and not on the sequence.
- **A pattern that would generalize past you** (it holds beyond this employer, codebase, and stack, carries no private context, and has a lens's shape) is *also* a candidate for the shared catalog. Propose the `add` override as usual, and in the same breath say it looks contributable and that `/deliberate-engineering:contribute` is the path if the operator wants it shared. The two are not exclusive: the override is theirs today, the contribution is a separate, operator-approved act, and this skill never files one. Say nothing of the sort for a signal that is employer-specific or a personal preference: that is an override and only an override.

If a signal has no clear target (ambiguous lens number, or a practice that does not fit any catalog), ask rather than force a wrong number, and ask with your own pick embedded (Rule 4): name the target you would use, or the `add` entry you would propose, and why, so the operator confirms a proposal instead of answering an open question. Drop candidates with no clear target or that are one-session noise: this skill does NOT propose an override of something seen once without a sign of recurring intent.

## The conversation protocol

For each candidate, present:

1. The observed signal: e.g., "you skipped review #35 twice, both times noting that a separate simplification pass handles that."
2. The target and operation: e.g., "review #35: disable."
3. The **exact markdown block** that would be appended to the override file, in the format the override read side expects.

A `disable` candidate looks like this (it removes a lens entirely):

> **Candidate:** review #35: disable
> 
> **Signal:** You skipped lens #35 (simplification check) twice, both times noting that a separate pass handles simplification.
> 
> **Block to append:**
> ```markdown
> ## review #35: disable
> 
> **Why:** We run a separate simplification pass after the deliberate review.
> ```
> 
> Approve this candidate, edit it, or reject it?

A `modify` candidate appends an annotation (the lens stays active, but you applied a recurring adjustment that you want read alongside the shipped content):

> **Candidate:** verify #N: modify
> 
> **Signal:** You applied lens #N consistently, but each time added a check for [specific constraint the shipped lens omits].
> 
> **Block to append:**
> ```markdown
> ## verify #N: modify
> 
> **Add:** The recurring adjustment you applied, read alongside the shipped lens, never replacing it.
> ```
> 
> Approve this candidate, edit it, or reject it?

An `add` candidate is a full operator-authored lens (a recurring practice you brought that the catalog lacks, now formalized as a lens for future sessions):

> **Candidate:** add: <catalog>
> 
> **Signal:** You consistently applied [strategy name] across [two or more contexts], with a clear when-to-apply condition and repeatable pattern.
> 
> **Block to append:**
> ```markdown
> ## add: <catalog>
> 
> **Name:** A short name for the strategy.
> 
> **When:** The situation in which this operator-authored lens applies.
> 
> **Apply:** What to do when it applies: the lens content itself.
> ```
> 
> Approve this candidate, edit it, or reject it?

A calibration candidate is a `modify` on the ceremony lens (you want a class of work to earn a different depth than the plugin's default):

> **Candidate:** planning #10: modify
> 
> **Signal:** Across the session you skipped the plan phase for analytics-only event changes three times, each time noting they carry no user-facing behavior or data-model impact.
> 
> **Block to append:**
> ```markdown
> ## planning #10: modify
> 
> **Add:** For analytics-only changes with no user-facing behavior or data-model impact, run one band lighter than the default: keep planning to a scope check with no written spec, and treat review as standard, not full.
> ```
> 
> Approve this candidate, edit it, or reject it?

**Recommend, never force.** The candidate is a proposal; the adopter decides. Present all candidates, let the adopter approve/edit/reject each. Do not append anything without approval. One exception to the prompt, never to the stance: a candidate targeting the standing rules takes the heavier confirmation described in the next section. Still the adopter's call, asked more carefully.

## A standing rule is not a preference: the elevated step

A candidate targeting `Rule N` or `add: rules` is a change to the plugin's constitution, and it will be in force at the start of every future session, before any work is classified. Presenting it in the same words and the same shape as a formatting preference is what makes a safety rail easy to remove by accident. **Key this on content, not only on the header**, the same way the refusal below is keyed: an `add: <catalog>` lens whose body relaxes a gate is a constitutional change wearing a lens's address, and takes this step too. For those candidates, do three extra things before asking:

1. **Name what it is.** Say plainly that this is a standing-rule change, not a lens preference, and that it applies from the start of every session until the operator removes it.
2. **Say what it permits, in behavior.** Translate the entry into what the agent will now do without asking. "Once this is in, I will merge to shared branches in the staging pipeline without stopping for you" is the sentence that matters, not "Rule 1: modify".
3. **Take a distinct confirmation.** Not the ordinary approve/edit/reject: ask for the change in the operator's own words ("tell me to write it and I will"). The read side then honors it every session with an acknowledgement rather than re-asking, which is exactly why the one confirmation here has to be real.

The four worked candidates above all target catalog lenses, so they take the ordinary prompt. A standing-rule candidate looks like this instead:

> **Candidate:** Rule 2: modify **(standing-rule change, not a lens preference)**
>
> **Signal:** You asked for this one directly: "make it permanent that you can write to the reporting replica without asking, it is a nightly-rebuilt mirror our team owns." I am not inferring it from the session; a safety rail is only ever loosened because you said so, and you did.
>
> **What this would change in my behavior:** from the start of every future session, on that replica I would run writes without stopping to ask you first. Everywhere else, Rule 2's read-only posture stays as it is.
>
> **Block to append:**
> ```markdown
> ## Rule 2: modify
>
> **Add:** On the nightly-rebuilt reporting replica, write queries do not need per-query approval; treat it as a system we own.
> ```
>
> This is a standing rule, in force from the start of every session until you remove it. If you want it, tell me to write it.

**The one thing this skill will not propose.** It never *initiates* a loosening of a safety rail from an observed deviation: Rule 1 (the human gate on irreversible and outward-facing actions) or Rule 2 (read-only on systems you do not own). **Judge this by content, not by the header.** An `add: rules` entry saying "in staging, ship without stopping", or an `add: review` lens whose body says "skip the gate here", is a Rule 1 loosening whatever it is addressed as, and the same restraint applies. The read side already judges these by content; the write side has to, or the rule is a formality with a rename around it. Seeing the gate skipped twice in a session is not evidence the operator wants it gone; it is just as likely evidence of a session where the operator was moving fast. If the operator asks for that override in words, write it, with the elevated step above. Otherwise, name the pattern out loud and stop there: "you triggered these yourself each time, so I am not proposing a gate change; say the word if you want one." A gate an agent can remove by inference is not a gate.

## The append-only write

For each approved candidate, **append** the block to `~/.claude/deliberate-engineering/overrides.md`. If the file does not exist, create it with this header:

```markdown
# Deliberate Engineering Overrides

Personal overrides for the deliberate-engineering plugin. Each entry disables, modifies, or adds to the shipped catalog.

See: deliberate-engineering-overrides skill for the format and the read-side behavior.

---
```

Then append the approved block. **Never rewrite or reorder existing entries.** Append only.

On an address conflict (an entry already exists for the same target), do NOT edit the existing entry. Either offer a coexisting block with a different `**Add:**` note, or warn the adopter and ask what to do. The file is append-only; this skill never touches an existing entry.

On write failure (permissions, file lock, anything), do not fail silently. Show the block to the adopter and ask them to paste it manually into the file. Degrade gracefully; do not drop the work.

After appending, declare what was written: the target, the operation, and the file path.

## No candidates

If no deviation, pattern, or calibration adjustment from this session is worth an override, say so plainly and write nothing. No forced candidates, no theater, no "let me create an override for completeness." Silence is the correct output when nothing rises to the level of durable preference. The skill's job is to recognize the signal, not to manufacture one.

## Output

Report:

1. The candidates shown: target, operation, and the signal that produced each.
2. Which candidates were approved, edited, or rejected.
3. What was appended: for each approved candidate, state the target, the operation, and confirm it was written to `~/.claude/deliberate-engineering/overrides.md`.
4. If no candidates were identified, state that explicitly.

The contract: the caller knows what was observed, what was discussed, and exactly what was written to the file (or that nothing was written).
