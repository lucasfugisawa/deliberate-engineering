# Architecture & usage

This is the map and the manual for `deliberate-engineering`: what the pieces are, how they fit together, and how to drive each flow. It is written for two readers — the human adopting the plugin, and the agent running it (which reasons better from *what you're trying to do* than from a list of parts). For why the plugin is scoped the way it is, see the README's *Scope & boundaries*; for install and uninstall, see the [README](../README.md).

## How it fits together

The plugin is a thin layer of judgment over a workflow engine. Two views: the lifecycle flow (how engineering work moves through it) and the extensibility cycle (how you personalize it and grow the shared catalogs).

### The lifecycle flow

```mermaid
flowchart TD
    rules["deliberate-engineering-rules<br/>seven always-on standing rules<br/>(human gate · read-only · verify · recommend ·<br/>comments · checkpoint · know your edge)"]
    start(["/deliberate-engineering:start — the router<br/>classify the work, name the phases and the<br/>ceremony they earn, route to the right one"])
    subgraph phases["the four deliberate phases — each: classify the work, then select the lenses that fit from its catalog"]
        plan["planning-strategy-selector · :plan<br/>what is worth building?"]
        review["review-strategy-selector · :review<br/>which lenses does this change call for?"]
        verify["verification-strategy-selector · :verify<br/>is it true against reality, and what is the evidence?"]
        debug["debug-operate-strategy-selector · :debug<br/>a live system misbehaves — now what?"]
    end
    engine["superpowers / Workflow<br/>the method: TDD, systematic debugging,<br/>plan execution, orchestration"]

    rules -.->|posture held under every phase| start
    start --> phases
    phases -.->|own the judgment, delegate the method| engine
```

- **The rules are the constitution.** Seven standing postures held across every phase and never switched off during engineering work. They set *how you behave*; everything below sets *where you start and what you do*.
- **The router is the front door** (`/deliberate-engineering:start`). It classifies the work, names the phase sequence and the ceremony each phase earns, and routes — recommending, never forcing. The only hard stop is the Rule 1 human gate on an irreversible or outward-facing action.
- **The four phases share one pattern:** classify the work, then read only the lenses that fit from that phase's catalog (never the whole catalog at once). Planning decides what to build; review reasons about the artifact; verification confronts reality; debug/operate takes over when a live system misbehaves and no reliable expectation holds.
- **The method is delegated.** `superpowers` (TDD, systematic debugging, plan execution) and the Workflow tool (orchestration) own *how* the work is carried out. The plugin owns the judgment — which phase, which lenses, how much ceremony — and hands the mechanism to the engine.

### The extensibility cycle

```mermaid
flowchart LR
    session(["a working session"])
    overrides["your overrides file<br/>~/.claude/deliberate-engineering-overrides.md<br/>read at runtime, takes precedence"]
    capture["/deliberate-engineering:capture<br/>distill the session into override blocks"]
    contribute["/deliberate-engineering:contribute<br/>generalize-at-capture into a candidate"]
    queue["candidates/ queue<br/>pending, generalized"]
    promote["/deliberate-engineering:promote<br/>blocking leak-audit + append-only catalog edit"]
    catalog["the shared catalogs<br/>(working tree only)"]
    gate["human gate — you commit / PR / push<br/>Rule 1; the tools never do"]

    session --> capture --> overrides
    overrides -.->|precedence over lenses and rules| session
    session --> contribute --> queue --> promote --> catalog --> gate
```

- **Your overrides file is the personal layer.** Read at runtime, it takes precedence over any shipped lens or rule; when it changes what the agent does, the agent says so. `/deliberate-engineering:capture` grows that file for you, distilling a session into ready-to-paste blocks.
- **The author tools grow the shared catalogs.** `/deliberate-engineering:contribute` generalizes a session's judgment into a candidate — dropping anything that can't be said without the specifics — and `/deliberate-engineering:promote` runs a blocking leak-audit and edits the catalog append-only. Both stop at the human gate: they edit only the working tree and never commit, open a PR, or push. That last step is always yours (Rule 1).
