# Contributing to deliberate-engineering

Thank you for your interest in contributing to `deliberate-engineering`. This plugin is built on the principle of **process, not prose** — every strategy is a lens through which to examine work, not a checklist to recite.

## How strategies are structured

Each strategy in the catalog follows a consistent three-part structure:

1. **How it works** — The concrete mechanism: what you do when applying this lens
2. **Objective** — The engineering goal this strategy achieves
3. **When most valuable** — The contexts where this lens provides the most signal

This structure makes strategies composable and context-aware. The selector can reason about which lenses a specific change calls for by matching the change's characteristics to each strategy's "when most valuable" clause.

## The "process, not prose" principle

Strategies describe **how to review**, not what to look for in isolation. They are meant to be:

- **Composable** — rotate the lens each pass; find → verify pipelines; close with fresh eyes
- **Context-aware** — select based on risk, reversibility, requirement clarity, and blast radius
- **Empirically grounded** — validate claims rather than assume them

A strategy should teach a deliberate practice, not provide a static checklist.

## Contribution requirements

All contributions must adhere to these constraints:

- **Domain-agnostic** — strategies must apply broadly across software engineering, not be specific to one language, framework, or domain
- **Employer-neutral** — no company names, internal tools, ticket IDs, or proprietary processes
- **Public and shareable** — content must be suitable for open-source distribution under the MIT license

## How to propose a new strategy

To propose a new review lens:

1. Add it to the appropriate group in `plugins/deliberate-engineering/skills/review-strategy-selector/catalog.md`
2. Follow the three-part structure: How it works / Objective / When most valuable
3. Keep it concise — each strategy should fit in 3-5 lines
4. Ensure it's composable with other lenses (can be applied in sequence, independently verifiable)

Submit your proposal as a pull request with a clear rationale for why this lens fills a gap in the existing catalog.

## How to propose a new catalog

Future catalogs (ceremony router, planning, debugging, design, environment/setup audit) will follow the same architecture as the review catalog: classify the context, select from a curated menu, compose tactics, close with verification.

If you have a catalog idea:

1. Describe the **classification axes** (analogous to risk/reversibility/clarity/size for review)
2. Outline the **tactic structure** (analogous to the three-part strategy structure)
3. Identify **5-10 core tactics** that would form the initial catalog
4. Explain how it **composes with existing catalogs** in the plugin

Open an issue with this proposal before investing in implementation.

## Questions?

Open an issue on the [GitHub repository](https://github.com/lucasfugisawa/deliberate-engineering) with your question or proposal.
