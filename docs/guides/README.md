[deliberate-engineering](../../README.md) › **Guides**

# Guides

Task-oriented walkthroughs: what you actually do, step by step, when driving each part of the plugin. For what the pieces *are* and how they fit together, see [Architecture & usage](../architecture-and-usage.md); for what ships in the box, the [README](../../README.md).

## What situation are you in?

| You have… | Go to |
|---|---|
| A piece of engineering work to do or change (the everyday case) | [The deliberate flow](deliberate-flow.md) |
| A program too large for one session | [Orchestrate](orchestrate.md) |
| A cluster of irreversible steps that must fire in a fixed, gated order (a merge cascade, a deploy chain, a batch data mutation, a teardown) | [Conduct](conduct.md) |
| A session where you repeatedly corrected the agent, and you want those corrections to stick | [Capture](capture.md) |
| Drafts that don't sound like you, and you want a personal voice profile | [Voice-build](voice-build.md) |
| A practice worth shipping to every adopter of this plugin | [CONTRIBUTING](../../CONTRIBUTING.md) |

## The guides, by intent

- **Use**: [The deliberate flow](deliberate-flow.md): how a normal session runs through `:start`, the four phases (`:plan`, `:review`, `:verify`, `:debug`), and the cross-cutting `:communicate`. Mostly self-firing; this guide is the journey and the map.
- **Scale**: [Orchestrate](orchestrate.md) for a program dispatched across sessions; [Conduct](conduct.md) for an irreversibility cluster. The two flow-heavy siblings: each is a flow you drive start to finish, and each gets a full walkthrough with the manual steps made explicit.
- **Adapt**: [Capture](capture.md) turns a session's corrections into personal overrides; [Voice-build](voice-build.md) builds your voice profile from your own writing. Both opt-in, both local, both keep the final say with you.
- **Contribute**: growing the *shared* catalog (a lens for everyone) is the author flow, and it lives in [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Everything else

- [Architecture & usage](../architecture-and-usage.md): the concepts: the constitution, the front door and its siblings, the four phases, communication and voice, the extensibility cycle, with diagrams.
- [README](../../README.md): what the plugin is, what's inside, install, uninstall.
- [CHANGELOG](../../CHANGELOG.md): what shipped, version by version.
