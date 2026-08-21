# Architecture & usage

This is the map and the manual for `deliberate-engineering`: what the pieces are, how they fit together, and how to drive each flow. It is written for two readers: the human adopting the plugin, and the agent running it (which reasons better from *what you're trying to do* than from a list of parts). For why the plugin is scoped the way it is, see the README's *Scope & boundaries*; for install and uninstall, see the [README](../README.md).

## How it fits together

The plugin is a thin layer of judgment over a workflow engine. Two views: the lifecycle flow (how engineering work moves through it) and the extensibility cycle (how you personalize it and grow the shared catalogs).

### The lifecycle flow

```mermaid
flowchart TD
    rules["deliberate-engineering-rules<br/>the always-on constitution"]
    start(["/deliberate-engineering:start<br/>the front-door router"])
    orchestrate(["/deliberate-engineering:orchestrate<br/>the across-session sibling: orchestrates units across sessions"])
    subgraph phases["the four deliberate phases: classify, then select the lenses that fit"]
        plan["planning-strategy-selector<br/>:plan"]
        review["review-strategy-selector<br/>:review"]
        verify["verification-strategy-selector<br/>:verify"]
        debug["debug-operate-strategy-selector<br/>:debug"]
    end
    engine["superpowers / Workflow<br/>the method engine"]
    comms["communication-collaboration-selector<br/>cross-cutting: consulted by nature, not a phase"]
    voice["deliberate-engineering-voice<br/>optional surface layer, silent with no profile"]

    rules -.->|posture under every phase| start
    rules -.->|holds across sessions too| orchestrate
    start --> phases
    orchestrate -.->|dispatches each unit to a fresh session,<br/>each running the phases| phases
    phases -.->|own the judgment,<br/>delegate the method| engine
    phases -.->|when the artifact is a communication| comms
    comms -.->|lenses decide substance,<br/>the profile decides surface| voice

    classDef constitution fill:#e8e0ff,stroke:#7c5cff,stroke-width:2px;
    classDef router fill:#fff0d9,stroke:#e0962e,stroke-width:2px;
    classDef phase fill:#e0f0ff,stroke:#3b82c4,stroke-width:1px;
    classDef engine fill:#e6f5e6,stroke:#4a9d4a,stroke-width:2px;
    classDef comms fill:#fff0d9,stroke:#e0962e,stroke-width:1px,stroke-dasharray:4 2;
    classDef voice fill:#f5eaf5,stroke:#9c5c9c,stroke-width:1px,stroke-dasharray:4 2;
    class rules constitution
    class start,orchestrate router
    class plan,review,verify,debug phase
    class engine engine
    class comms comms
    class voice voice
```

- **The rules are the constitution.** Nine standing postures held across every phase and never switched off during engineering work. They set *how you behave*; everything below sets *where you start and what you do*.
- **The router is the front door** (`/deliberate-engineering:start`). It classifies the work, names the phase sequence and the ceremony each phase earns, and routes (recommending, never forcing). The only hard stop is the Rule 1 human gate on an irreversible or outward-facing action.
- **Orchestration is its across-session sibling** (`/deliberate-engineering:orchestrate`). When the work is a program too large for one session, it runs an orchestration session that decomposes the work into units, dispatches each to a fresh worker session (a background subagent only for a narrow, earned band), verifies each return against primary evidence in a separate context, dispositions it, and tracks the whole program behind an always-current recovery anchor that lets any fresh session resume the orchestrator. The router conducts phases *within* a session; this orchestrates units *across* sessions. It is deliberately thin: it cites the standing rules and reuses the selectors and the state working-note rather than restating them, and it stops at the same Rule 1 gate for every outward action a unit produces.
- **Conduction is its sibling for irreversibility clusters** (`/deliberate-engineering:conductor`). When irreversibility concentrates into a cluster (a merge cascade, a deploy chain, a batch of production data mutations, a teardown), it runs the cluster from a CONDUCTOR contract: a fixed step order with a gate between each, world state re-derived before every gate, the gate state kept in a per-item station table rather than in memory, each irreversible step bounded by a dry-run and a blast-radius limit before it fires and verified after, and every irreversible trigger handed to the operator (Rule 1). The router conducts phases *within* a session, orchestrate units *across* sessions, and this conducts steps *across an irreversibility cluster*, usually in one. It cites the verification rollout and data-mutation lenses and the planning ordering lenses rather than restating them; a small cascade stays in a tracker queue, and a cluster earns its own cockpit only when the gate graph outgrows one.
- **The four phases share one pattern:** classify the work, then read only the lenses that fit from that phase's catalog (never the whole catalog at once). Planning decides what to build; review reasons about the artifact; verification confronts reality; debug/operate takes over when a live system misbehaves and no reliable expectation holds.
- **The method is delegated.** `superpowers` (TDD, systematic debugging, plan execution) and the Workflow tool (orchestration) own *how* the work is carried out. The plugin owns the judgment (which phase, which lenses, how much ceremony) and hands the mechanism to the engine.
- **Communication is cross-cutting, not a phase.** When the artifact you're producing is a communication (a PR description, a review comment, a stakeholder message, a writeup of alternatives), the router routes it *by nature* to `communication-collaboration-selector`, which classifies by audience and artifact (its own axes, not the four phase axes) and applies its seven lenses. You consult it from inside whatever phase you're in; it never becomes a fifth phase and adds no fifth axis. Once the lenses have shaped the message, the selector consults `deliberate-engineering-voice`, an optional surface layer that applies your personal voice profile over the result (the lenses decide what the message must accomplish, the profile decides how it sounds) and names the files it loaded; with no profile directory it does nothing and says nothing.

### The extensibility cycle

```mermaid
flowchart LR
    session(["a working session"])

    subgraph adapt["Adapt: make it yours"]
        direction LR
        capture["/deliberate-engineering:capture"]
        overrides["your overrides file<br/>runtime precedence"]
        capture --> overrides
    end

    subgraph share["Contribute: share it with everyone"]
        direction LR
        contribute["/deliberate-engineering:contribute"]
        queue["the candidates queue"]
        promote["/deliberate-engineering:promote"]
        catalog["the shared catalogs"]
        gate["human gate<br/>commit / PR / push"]
        contribute --> queue --> promote --> catalog --> gate
    end

    session --> capture
    session --> contribute
    overrides -.->|feeds your next session| session

    classDef session fill:#e8e0ff,stroke:#7c5cff,stroke-width:2px;
    classDef adopter fill:#e0f0ff,stroke:#3b82c4,stroke-width:1px;
    classDef author fill:#fff0d9,stroke:#e0962e,stroke-width:1px;
    classDef gate fill:#ffe0e0,stroke:#cc4444,stroke-width:2px;
    class session session
    class capture,overrides adopter
    class contribute,queue,promote,catalog author
    class gate gate
```

- **Your overrides file is the personal layer.** Read at runtime, it takes precedence over any shipped lens or rule; when it changes what the agent does, the agent says so. `/deliberate-engineering:capture` grows that file for you, distilling a session into ready-to-paste blocks.
- **The author tools grow the shared catalogs.** `/deliberate-engineering:contribute` generalizes a session's judgment into a candidate (dropping anything that can't be said without the specifics) and `/deliberate-engineering:promote` runs a blocking leak-audit and edits the catalog append-only. Both stop at the human gate: they edit only the working tree and never commit, open a PR, or push. That last step is always yours (Rule 1).

## How to use it

Three things you'll want to do, by intent.

### Use: drive the engineering flow

You arrived with work to do. The front door is `/deliberate-engineering:start`: describe the work and it classifies it, names the phases it deserves and how much ceremony each earns, and routes you. When you already know where you are, call a phase directly:

- `/deliberate-engineering:plan`: decide what's worth building and how much process it deserves, before code exists.
- `/deliberate-engineering:review`: classify a change, then apply the review lenses it actually calls for.
- `/deliberate-engineering:verify`: establish that something is true against reality, with evidence, not just plausible on paper.
- `/deliberate-engineering:debug`: diagnose a live system that's misbehaving when no reliable expectation holds.
- `/deliberate-engineering:communicate`: cross-cutting, not a phase: when the next artifact is a communication (a PR description, a review comment, a stakeholder message, a writeup of alternatives), classify it by audience and artifact and apply the matching lenses. Consult it from inside any phase.
- `/deliberate-engineering:orchestrate`: not a phase either: when the work is a program too large for one session, run it as an orchestration session that decomposes the work into units, dispatches each to a fresh worker session, verifies what returns against primary evidence, and tracks it all in one place. The across-session sibling of `:start`; skip it for work that fits one session.
- `/deliberate-engineering:conductor`: not a phase either: when a cluster of irreversible steps must fire in a fixed, gated order (a merge cascade, a deploy chain, a batch of production data mutations, a teardown), conduct it from a re-derived, gated runbook where you pull every irreversible trigger. A sibling of `:orchestrate` (orchestrate dispatches units across sessions; this conducts ordered steps across a cluster); skip it for a single step and for a program dispatched across sessions.

One mental model runs across all of them: risk, reversibility, requirement clarity, and reach decide the depth, not line count. The plugin recommends a depth and a set of lenses *with its reasoning*, and you stay in control. Nothing is forced except one thing: it stops at a human gate before any irreversible or outward-facing action (a merge, a deploy, a push, a posted message). The nine standing rules hold underneath every phase the whole time.

### Adapt: make it think like you

The plugin is opinionated, and it's meant to become yours. A personal file at `~/.claude/deliberate-engineering/overrides.md` takes precedence over the shipped content, addressed by stable identifiers: `review #N`, `verify #N`, `planning #N`, `debug #N`, or `rule N`. Three operations: `disable` turns a lens or rule off; `modify` appends your annotation alongside the shipped text; `add` defines your own. The agent always declares when an override changed what it did (nothing happens silently), and you can even loosen a safety rule, which it honors while calling out the raised autonomy.

You can write that file by hand (the README's *Make it yours* section shows the format), or let the agent help: run `/deliberate-engineering:capture` (or just ask) and it distills the session you just had (the lenses you skipped or corrected, the practices the catalog lacks) into ready-to-paste blocks. On demand only, append-only, written only on your approval. This grows *your* file; it is the adopter's side, distinct from the author tools below.

Overrides are one of two personal layers under `~/.claude/deliberate-engineering/`, both opt-in, both absent by default. The override file changes *what the agent does*; the voice profile changes *how what it writes sounds*. The profile is a directory at `~/.claude/deliberate-engineering/voice/`: `core.md` for what's true of your writing everywhere, `registers/<lang>.md` for what changes with the language, `archetypes/<type>.md` for what changes with the kind of communication (a DM is not a design doc). `deliberate-engineering-voice` reads it after the communication lenses have shaped the message and applies it as the surface layer, loading at most three files per draft (the core, the matching register, the matching archetype) and falling back to two, declared, when one has no match. Precedence runs explicit instruction > voice profile > default style; where a lens and the profile genuinely conflict, the lens wins on substance and the profile wins on surface. It names the files it loaded when it fires, it never licenses breaking a standing rule (the Rule 1 gate and the Rule 9 resolvability bar hold regardless of how you write), and it does nothing and says nothing when the directory is absent. The plugin ships the mechanism, the contract, a template, a bootstrap method, and a guided build path (`deliberate-engineering-voice-build`, the `/deliberate-engineering:voice-build` command, which runs that method from collection to a finished profile and keeps the interview and the blind A/B human); no profile content ships, and the directory stays out of every repository. The README's *Sound like yourself* section is the overview; `contract.md` next to the skill is the full layout.

### Contribute: ship judgment to everyone

When a session surfaces judgment that generalizes beyond you, it can become a catalog lens for everyone. Two steps, with a hard wall between them and the public:

- `/deliberate-engineering:contribute` turns that judgment into a candidate. Its central act is *generalize at capture*: it extracts the employer-neutral principle and discards the specifics (services, incidents, names) before anything is written. Anything that can't survive that, it drops rather than half-cleans. Approved candidates land as `pending` files in the `candidates/` queue.
- `/deliberate-engineering:promote` drives a candidate into the catalog: a blocking leak-audit first (any surviving specific stops it), then an append-only edit (a new lens gets the next free number and existing lenses are never renumbered, so the override identifiers you cite stay stable) plus a skill-reviewer pass. A structural change (a new catalog, a reorganization, a rule change) is not auto-applied; promote recommends the full design cycle instead.

Both tools edit only the working tree and always stop before commit, PR, or push: publication is your decision (Rule 1). For the contributor workflow end to end, see [`CONTRIBUTING.md`](../CONTRIBUTING.md).

### Where to go next

- Install, uninstall, and the optional always-on recipe live in the [README](../README.md).
- The exact override-file format and an example are in the README's *Make it yours* section.
- Why the plugin stays horizontal and where it stops is the README's *Scope & boundaries* section.
