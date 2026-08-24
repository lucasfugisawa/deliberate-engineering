# Communication & Collaboration Catalog

This catalog contains seven communication lenses plus a composition note. Each lens is a reusable principle for communicating around engineering work, not a checklist for one artifact type. The selector skill references these by number and reads each lens's **Tags** line (which artifacts and audiences it most applies to) to pick the ones THIS communication calls for. No lens is mandatory: apply only the ones the artifact and audience actually call for.

Lens **numbers are stable identifiers, not reading order**: a lens keeps its number for life, and a new lens is appended with the next free number. This keeps every published number citable (e.g. by an override) without renumbering.

## Master Principle

Communication is engineering *outward*: the same deliberate judgment applied to code applies to how the work is explained, reviewed, and handed off. What selects here is **who reads it and what artifact it is**, not how much there is to say; the plugin's ruler still sets the depth, through the weight of the subject the artifact carries. Match the message to the reader and the artifact; say less, with more cohesion; expose the reasoning so it can be challenged.

---

### 1. PR/MR description: the case for the change, not its changelog

- **How it works:** Write the description as the high-level *what* plus the business *why*, then add what the reviewer needs: suggested review focus, QA/testing notes, security considerations, and merge/deploy ordering (see lens 2 for how to *structure* dependent PRs). Do not restate the diff line by line: the diff is the log. State that case in terms the reviewer can resolve unaided: no spec item numbers, no internal codenames (lens 5; Rule 9 for the same discipline in the shipped artifact).
- **Objective:** Let a reviewer grasp the change's intent, risk, and how to review it without reverse-engineering it from the code.
- **When most valuable:** Any PR/MR; most of all when the change is large, risky, or crosses ownership boundaries.
- **Tags:** Artifacts: PR/MR. Audiences: engineering (primary); product/business (the business *why* rises when a stakeholder reads the PR).

### 2. Smallest reviewable unit: stack when work builds on work

- **How it works:** Size a PR to the minimum unit of cohesion needed to understand the change: small and simple to review, without splitting apart what only makes sense together. When work builds on not-yet-merged work, **stack** the PRs; otherwise branch off main.
- **Objective:** Keep each PR independently reviewable without losing the cohesion that makes the change make sense.
- **When most valuable:** Multi-step work that would otherwise become one unreviewable PR; dependent changes that build on each other.
- **Tags:** Artifacts: PR/MR, branch decomposition. Audiences: engineering.

### 3. Review comments invite, they don't command

- **How it works:** Frame review feedback as an invitation to change, not an order (e.g. "what do you think, does this make sense?", one phrasing of that register and not a script to recite). Be assertive, objective, and concise, but warm; aim for the feel of a chat thread, not a verdict handed down. Critique the code, not the author.
- **Objective:** Get the change improved while keeping the collaboration healthy and the author engaged.
- **When most valuable:** Every review comment; most of all on disagreement, or when pointing out a significant problem.
- **Tags:** Artifacts: review comment. Audiences: engineering.

### 4. Speak the reader's language

- **How it works:** Match register, vocabulary, and level of detail to the reader: code-agent, engineering, product, or business. When the reader is human, be human: clear, didactic, plain and widely-understood words, no needless jargon, concision with cohesion. When the reader fits none of these cleanly, ask the operator which register fits rather than guessing.
- **Objective:** The reader understands on the first read, at the depth they need, without translating.
- **When most valuable:** Any communication that crosses an audience boundary; handoffs from one role to another.
- **Tags:** Artifacts: any communication. Audiences: all (this lens is the audience axis operationalized).

### 5. No unresolvable context in outward communication

- **How it works:** Reference only what the reader of *this artifact* can resolve unaided: a ticket they can open, or the thing itself described in a line. Internal planning IDs ("item 1.3", "REQ-7", "phase 2"), pointers to a spec or design doc they cannot open, and project-internal codenames or jargon all fail the test. Apply the test to the reader, not to the org chart: a teammate with identical access still cannot resolve a number that lives only in your spec.
- **Objective:** The reader can follow every reference and every term without privileged access or a private glossary.
- **When most valuable:** Any communication whose reader lacks your planning context, which includes most PRs, not only what crosses a team or org boundary.
- **Tags:** Artifacts: any outward communication. Audiences: all. What decides this lens is resolvability by the reader, not their distance from the team. Kin: Rule 9 governs the same discipline inside shipped code artifacts (code comments, commit messages, PR descriptions); this lens is the broader case: any outward communication.

### 6. Present alternatives with the reasoning exposed

- **How it works:** When presenting options, explain each option's implications didactically, give a recommendation grounded in the known scenario, objectives, and constraints, and expose the *rationale* behind it, so the reader can critique not just the options and the pick, but the assumptions underneath. This is orthogonal to audience: always expose the reasoning; only the *form* varies by reader (apply lens 4 for that).
- **Objective:** Let the decision-maker challenge the reasoning, not just the conclusion, so the assumptions themselves get calibrated.
- **When most valuable:** Whenever there is a decision or recommendation to communicate: a design doc, an RFC, a recommendation to a stakeholder, or presenting options to the operator.
- **Tags:** Artifacts: design doc, RFC, recommendation, any presentation of alternatives. Audiences: all.

### 7. The durable handoff: written so it's picked up cold

- **How it works:** Write a handoff or status update for a reader with zero context: state where the work stands, what is done, what remains, what is blocked or risky, and the single next action. Anchor it to where the work already lives (the PR, the tracker, the working note), not a throwaway message. Favor a scannable shape (state → done → remaining → risks → next) over prose.
- **Objective:** Someone (a teammate, your future self, the next session) can resume the work without reconstructing its state from scratch.
- **When most valuable:** Ending a session or shift with work unfinished; passing work between people, roles, or agents; any pause where context that lives only in your head would otherwise be lost.
- **Tags:** Artifacts: handoff, status update, working note. Audiences: engineering (primary); the next operator or agent. Kin: Rule 6 (checkpoint durable state before compacting) governs *persisting* state across a context boundary; this lens governs *communicating* that state to a reader.

---

## Composition note

*The other four catalogs carry a numbered Appendix of composition patterns, each addressable as `<catalog> pattern #N`. This one carries a single note instead, because what there is to say here is one relationship between lenses rather than a set of alternatives to chain. That makes it the one catalog with no pattern targets, which is a stated exception and not an oversight.*

These lenses combine. Lens 4 (speak the reader's language) modulates the *form* of every other lens: a PR description (1) or an alternatives writeup (6) is phrased differently for an engineering versus a business reader. Lens 5 (no unresolvable context) is a constraint that rides on top of any outward-facing lens. Apply the lens that matches the artifact, then let audience set the register.
