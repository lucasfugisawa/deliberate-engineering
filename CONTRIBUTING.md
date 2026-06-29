# Contributing to deliberate-engineering

Thank you for your interest in contributing to `deliberate-engineering`. This plugin is built on the principle of **process, not prose** — every strategy is a lens through which to examine work, not a checklist to recite.

This file is the contributor *policy*: what a contribution must satisfy and how a lens is shaped. It deliberately does not re-describe the contribution flow or its mechanism — those have a single home each (see *Where the rest lives* at the end).

## What a contribution must satisfy

All contributions must adhere to these constraints:

- **Domain-agnostic** — a strategy must apply broadly across software engineering, not be specific to one language, framework, or domain. The plugin is a horizontal judgment layer; depth in any one domain belongs elsewhere.
- **Employer-neutral** — no company names, internal tools, ticket IDs, service names, incident numbers, real quantities, or proprietary processes. Anything that cannot be said without the specifics is dropped, not half-cleaned.
- **Public and shareable** — content must be suitable for open-source distribution under the MIT license.

## How a lens is structured

Each lens in a catalog follows a consistent three-part structure:

1. **How it works** — the concrete mechanism: what you do when applying this lens.
2. **Objective** — the engineering goal this lens achieves.
3. **When most valuable** — the contexts where this lens provides the most signal.

This structure makes lenses composable and context-aware: a selector reasons about which lenses a specific change calls for by matching the change's characteristics to each lens's *when most valuable* clause. A lens should teach a deliberate practice, not provide a static checklist — composable (rotate the lens each pass; find → verify; close with fresh eyes), context-aware (selected by risk, reversibility, requirement clarity, and reach), and empirically grounded (validate claims rather than assume them).

## How to contribute a lens

Contribution is assisted and gated — you do not hand-edit a catalog and open a PR. Run the author tools from a local clone of this repository (they operate on the repo's own catalogs and `candidates/` queue):

- `/deliberate-engineering:contribute` turns a session's generalizable judgment into a `pending` candidate (generalizing at capture — extracting the employer-neutral principle and discarding the specifics).
- `/deliberate-engineering:promote` drives a candidate into the catalog through a blocking leak-audit and an append-only edit, and stops before commit/PR/push — publication is your decision.

A **new catalog**, a reorganization, or a rule change is a *structural* change, not a single lens. It is not auto-applied: `/deliberate-engineering:promote` recommends the full design cycle (brainstorm → spec → plan → build) for it. Open an issue describing the classification axes, the lens structure, and how it composes with the existing catalogs before investing in implementation.

## Releasing (maintainer)

A release is any change to the shipped plugin that reaches adopters. The version is decided by a human — the CI gate only checks that the step was not forgotten; it never picks or applies a number for you.

When publishing a release:

1. **Bump the version in lockstep** — `plugins/deliberate-engineering/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` must carry the **same** version. Pre-1.0: a new skill, command, catalog, or lens is a **minor** (`0.x.0`); a pure fix is a **patch** (`0.x.y`). The override-file relocation in 0.2.0 was technically breaking, but pre-1.0 minor already covers that. The client offers an update only when the version *string* changes — without a bump, adopters never see the release.
2. **Update `CHANGELOG.md`** — a new section for the version (Added / Changed / Fixed), newest first.
3. **Tag the release** — annotated tag `vX.Y.Z` on the release commit, pushed alongside `main`.

The CI workflow `.github/workflows/version-gate.yml` enforces two of these: it fails if the two manifests disagree (Check A), and if anything under `plugins/deliberate-engineering/**` changed without a version bump (Check B). On a pull request these block the merge; on a push to `main` they flag the commit. They do not check the changelog or the tag — those stay your discipline.

## Questions?

Open an issue on the [GitHub repository](https://github.com/lucasfugisawa/deliberate-engineering) with your question or proposal.

## Where the rest lives

To keep one home per topic and avoid drift:

- **The contribution flow end to end** (the diagram and the walkthrough) — `docs/architecture-and-usage.md`, *Contribute — ship judgment to everyone*.
- **The mechanism** (generalize-at-capture, the leak-audit gate, append-only numbering, stop-before-commit) — the `deliberate-engineering-contribute` and `deliberate-engineering-promote` skills themselves.
- **Counts, install, scope, and the override-file format** — the [README](README.md).
