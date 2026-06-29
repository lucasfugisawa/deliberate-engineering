# Communication & Collaboration Catalog

This catalog contains seven communication lenses plus a composition note. Each lens is a reusable principle for communicating around engineering work — not a checklist for one artifact type. The selector skill references these by number and reads each lens's **Tags** line (which artifacts and audiences it most applies to) to pick the ones THIS communication calls for. No lens is mandatory — apply only the ones the artifact and audience actually call for.

Lens **numbers are stable identifiers, not reading order**: a lens keeps its number for life, and a new lens is appended with the next free number. This keeps every published number citable (e.g. by an override) without renumbering.

## Master Principle

Communication is engineering *outward*: the same deliberate judgment applied to code applies to how the work is explained, reviewed, and handed off. The ruler is **who reads it and what artifact it is** — not how much there is to say. Match the message to the reader and the artifact; say less, with more cohesion; expose the reasoning so it can be challenged.

---

### 1. PR/MR description — the case for the change, not its changelog

- **How it works:** Write the description as the high-level *what* plus the business *why*, then add what the reviewer needs: suggested review focus, QA/testing notes, security considerations, and merge/deploy ordering (see lens 2 for how to *structure* dependent PRs). Do not restate the diff line by line — the diff is the log.
- **Objective:** Let a reviewer grasp the change's intent, risk, and how to review it without reverse-engineering it from the code.
- **When most valuable:** Any PR/MR; most of all when the change is large, risky, or crosses ownership boundaries.
- **Tags:** Artifacts: PR/MR. Audiences: engineering (primary); product/business (the business *why* rises when a stakeholder reads the PR).

### 2. Smallest reviewable unit — stack when work builds on work

- **How it works:** Size a PR to the minimum unit of cohesion needed to understand the change — small and simple to review, without splitting apart what only makes sense together. When work builds on not-yet-merged work, **stack** the PRs; otherwise branch off main.
- **Objective:** Keep each PR independently reviewable without losing the cohesion that makes the change make sense.
- **When most valuable:** Multi-step work that would otherwise become one unreviewable PR; dependent changes that build on each other.
- **Tags:** Artifacts: PR/MR, branch decomposition. Audiences: engineering.

### 3. Review comments invite, they don't command

- **How it works:** Frame review feedback as an invitation to change, not an order — e.g. "what do you think, does this make sense?", one phrasing of that register and not a script to recite. Be assertive, objective, and concise, but warm; aim for the feel of a chat thread, not a verdict handed down. Critique the code, not the author.
- **Objective:** Get the change improved while keeping the collaboration healthy and the author engaged.
- **When most valuable:** Every review comment; most of all on disagreement, or when pointing out a significant problem.
- **Tags:** Artifacts: review comment. Audiences: engineering.

### 4. Speak the reader's language

- **How it works:** Match register, vocabulary, and level of detail to the reader — code-agent, engineering, product, or business. When the reader is human, be human: clear, didactic, plain and widely-understood words, no needless jargon, concision with cohesion. When the reader fits none of these cleanly, ask the operator which register fits rather than guessing.
- **Objective:** The reader understands on the first read, at the depth they need, without translating.
- **When most valuable:** Any communication that crosses an audience boundary; handoffs from one role to another.
- **Tags:** Artifacts: any communication. Audiences: all (this lens is the audience axis operationalized).

### 5. No internal IDs in outward communication

- **How it works:** Reference only identifiers the reader can actually resolve — a publicly accessible ticket, say — or a brief description of the referenced item. Never use internal-only planning IDs or references the audience cannot reach.
- **Objective:** The reader can follow every reference without privileged access.
- **When most valuable:** Any communication leaving the team or org boundary; anything an external or cross-team audience reads.
- **Tags:** Artifacts: any outward communication. Audiences: product, business, outside-the-team (does not apply between peers with equal access). Kin: the rules skill governs internal IDs in shipped *code* artifacts (commits, PRs, code comments); this lens is the broader case — any outward communication.

### 6. Present alternatives with the reasoning exposed

- **How it works:** When presenting options, explain each option's implications didactically, give a recommendation grounded in the known scenario, objectives, and constraints, and expose the *rationale* behind it — so the reader can critique not just the options and the pick, but the assumptions underneath. This is orthogonal to audience: always expose the reasoning; only the *form* varies by reader (apply lens 4 for that).
- **Objective:** Let the decision-maker challenge the reasoning, not just the conclusion — so the assumptions themselves get calibrated.
- **When most valuable:** Whenever there is a decision or recommendation to communicate — a design doc, an RFC, a recommendation to a stakeholder, or presenting options to the operator.
- **Tags:** Artifacts: design doc, RFC, recommendation, any presentation of alternatives. Audiences: all.

### 7. The durable handoff — written so it's picked up cold

- **How it works:** Write a handoff or status update for a reader with zero context: state where the work stands, what is done, what remains, what is blocked or risky, and the single next action. Anchor it to where the work already lives — the PR, the tracker, the working note — not a throwaway message. Favor a scannable shape (state → done → remaining → risks → next) over prose.
- **Objective:** Someone — a teammate, your future self, the next session — can resume the work without reconstructing its state from scratch.
- **When most valuable:** Ending a session or shift with work unfinished; passing work between people, roles, or agents; any pause where context that lives only in your head would otherwise be lost.
- **Tags:** Artifacts: handoff, status update, working note. Audiences: engineering (primary); the next operator or agent. Kin: Rule 6 (checkpoint durable state before compacting) governs *persisting* state across a context boundary; this lens governs *communicating* that state to a reader.

---

## Composition note

These lenses combine. Lens 4 (speak the reader's language) modulates the *form* of every other lens — a PR description (1) or an alternatives writeup (6) is phrased differently for an engineering versus a business reader. Lens 5 (no internal IDs) is a constraint that rides on top of any outward-facing lens. Apply the lens that matches the artifact, then let audience set the register.
