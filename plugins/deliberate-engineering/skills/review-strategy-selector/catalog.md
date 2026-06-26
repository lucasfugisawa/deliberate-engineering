# Review Strategy Catalog

This catalog contains 51 review strategies organized into five groups plus composition patterns. Each strategy is a lens through which to examine work. The selector skill references these by number to build custom review workflows. No lens is mandatory — apply only the ones the change's context, risk, and scope actually call for.

## Master Principle

Strategies **compose**. The strongest pattern is to *rotate the lens each pass* (a new strategy per review), validate empirically where possible, and **close with a fresh-eyes pass that has no history of the edits** to break accumulated bias. This applies equally to documentation, design, and code.

---

## Part A — Process / Meta-review Strategies

*How to conduct the review, independent of the artifact's domain. This is the core: technique, not domain knowledge.*

### 1. Baseline review (correctness / resilience / consistency)

- **How it works:** A first broad pass, reading the whole artifact for logic errors, failures under adverse conditions, and internal contradictions.
- **Objective:** Establish a quality floor and map the terrain before going deep.
- **When most valuable:** Always, as the first pass; it is the point the others diverge from.

### 2. Adversarial review (try to refute, not confirm)

- **How it works:** Adopt the stance of someone who wants to *break* the claim — hunt the counterexample, the input that violates the invariant, the event ordering that produces the bug. Default: "this is wrong until proven otherwise."
- **Objective:** Neutralize confirmation bias, which makes one "validate" what one already believes.
- **When most valuable:** Plausible-but-unverified claims; security/correctness decisions where the cost of a false "it's fine" is high.

### 3. Independent fresh-eyes pass

- **How it works:** A review deliberately *without* the history of prior edits, so as not to inherit rationalizations already made (e.g. dispatch a reviewer with no context of who edited).
- **Objective:** Break the "each pass finds less because it is already convinced" loop; see what the author can no longer see.
- **When most valuable:** After several of your own passes; before a merge; whenever you are both author and reviewer.

### 4. Self-review of regressions introduced by your own fixes

- **How it works:** After applying fixes, review specifically **what those fixes might have broken**.
- **Objective:** Prevent the repair of one defect from planting another.
- **When most valuable:** Always, after a round of non-trivial edits.

### 5. Devil's advocate / red team (rotated role)

- **How it works:** Formally designate someone to attack the proposal; rotate the role so it does not go stale.
- **Objective:** Institutionalize productive dissent.
- **When most valuable:** Group decisions at risk of groupthink.

### 6. Loop-until-dry (unknown-size discovery)

- **How it works:** Repeat review rounds until K consecutive rounds find nothing new, instead of stopping at a fixed number.
- **Objective:** Don't leave the "tail" of defects unfound out of a lazy stopping rule.
- **When most valuable:** "Find all bugs/edge cases" audits where the total is unknown.

### 7. Checklist-based review

- **How it works:** Review against a standardized list (input validation, error handling, logging, pagination, timeouts, idempotency, etc.).
- **Objective:** Consistent minimum coverage, independent of who reviews.
- **When most valuable:** Large teams, onboarding, areas prone to recurring oversights.

### 8. Judge panel / multiple independent attempts

- **How it works:** Generate N independent approaches from different angles (MVP-first, risk-first, user-first), score them, and synthesize the best (grafting good ideas from the others).
- **Objective:** Avoid fixating on the first idea; explore the solution space.
- **When most valuable:** Architecture/design decisions with a wide space and a high cost of being wrong.

### 9. Adversarial majority-refute voting

- **How it works:** For each finding, dispatch N independent skeptics, each instructed to *refute* it; kill the finding if the majority refute.
- **Objective:** Prevent plausible-but-wrong findings from surviving.
- **When most valuable:** When the cost of acting on a false positive is high; automated/at-scale reviews.

### 10. Completeness critic

- **How it works:** A final pass asking "what is missing? — a modality not exercised, a claim not verified, a source not read?" What it finds becomes the next round.
- **Objective:** Close coverage gaps the themed passes did not catch.
- **When most valuable:** At the end of long audits; before declaring "done."

### 11. Change-size / reviewability review

- **How it works:** Before reviewing content, assess whether the change is small enough to review well. Flag oversized diffs that mix unrelated concerns, and recommend splitting them into focused, independently reviewable units.
- **Objective:** Keep changes small enough that a reviewer can actually understand them — large changes hide defects and get rubber-stamped.
- **When most valuable:** Any PR/CL; especially ones touching many files or mixing refactor with behavior change.

---

## Part B — Verification / Evidence Strategies

*How to prove a claim is true rather than assume it.*

### 12. Empirical validation (actually execute)

- **How it works:** Instead of reasoning about what the code/SQL does, **execute** it in a disposable environment with constructed scenarios and assert on the real result.
- **Objective:** Trade "I think it works" for "I saw it work."
- **When most valuable:** Subtle-semantics logic (data-modifying CTEs, NULL handling, non-guaranteed ordering, idempotency, rollback).

### 13. Validation against real data/systems (ground truth)

- **How it works:** Confront the artifact's premises with the external source of truth — production/staging data, the real schema, the real API. You don't review the text; you review whether the text **matches reality**.
- **Objective:** Catch wrong factual premises (distributions, cardinality, types, volumes) that no internal reading would reveal.
- **When most valuable:** Specs/designs that depend on data characteristics; integrations; any cited number.

### 14. Source-of-truth verification (correct canonical reference)

- **How it works:** Ensure you review against the canonical reference (e.g. `origin/main`), not a stale local copy or a feature branch.
- **Objective:** Avoid correct conclusions about the wrong artifact.
- **When most valuable:** Multi-branch/multi-repo environments; worktrees; parallel checkouts.

### 15. Assumption / invariant audit

- **How it works:** Explicitly list every implicit premise ("this field is unique", "this runs after that") and validate each one.
- **Objective:** Make visible what is being assumed without proof.
- **When most valuable:** Premise-dense designs; integrations; behavior dependent on another system.

### 16. Coverage analysis (walk every case)

- **How it works:** Systematically enumerate all cases/branches/states and verify, one by one, which mechanism handles each — making explicit what is **left out** and why.
- **Objective:** Turn "I think it covers everything" into a proof by exhaustion; make tolerated gaps visible.
- **When most valuable:** State taxonomies, state machines, migration/backfill logic.

### 17. Boundary / edge-case review

- **How it works:** Focus on the extremes — empty, one, many, numeric limits, timezone/DST, encoding, off-by-one, nulls/absent.
- **Objective:** Bugs live at the edges, not on the happy path.
- **When most valuable:** Parsing, aggregations, time windows, pagination.

### 18. Test-quality review (review the tests, not just the code)

- **How it works:** Evaluate whether the tests actually exercise the behavior (meaningful assertions, edge cases, absence of tautological tests), branch coverage.
- **Objective:** Ensure the suite truly protects against regression.
- **When most valuable:** Before trusting "the tests pass"; in PRs that add tests alongside the feature.

---

## Part C — Failure & Contradiction Reasoning Strategies

### 19. Apparent-contradiction reconciliation

- **How it works:** On finding an apparent contradiction, don't fix it immediately — investigate until you classify it as (a) a real bug, (b) a false conflict due to different context/timing, or (c) imprecise wording.
- **Objective:** Avoid both ignoring bugs and "fixing" things that were correct.
- **When most valuable:** Rules with temporal/contextual nuance; when the artifact contradicts an established norm.

### 20. Failure-mode / pre-mortem / FMEA

- **How it works:** Assume the change failed in production and reason backward about the causes; or enumerate failure modes and rank them by severity × probability.
- **Objective:** Anticipate failures before they become expensive.
- **When most valuable:** High-impact / low-reversibility changes.

### 21. Silent-failure hunting

- **How it works:** Specifically look for paths where an error is swallowed, a fallback masks a problem, or a failure emits no signal at all.
- **Objective:** Ensure failures are detectable, not invisible.
- **When most valuable:** Error handling, retries, fallbacks, integrations that can degrade silently.

### 22. Error-handling adequacy review

- **How it works:** Trace each error path: are errors caught at the right level, propagated with context, and recoverable? Are timeouts, retries with backoff, and partial-failure handling present where external calls can fail?
- **Objective:** Ensure failures are handled deliberately — not just caught, but caught at a level that can do something useful about them.
- **When most valuable:** Network/IO boundaries, distributed calls, anything with external dependencies. (Complements silent-failure hunting, which looks for the *absence* of handling; this judges the *quality* of handling that exists.)

### 23. Concurrency / race review

- **How it works:** Analyze what happens when the operation runs **at the same time** as other writes — torn reads, locks, windows (e.g. export→merge), non-deterministic ordering, deadlocks.
- **Objective:** Find bugs that only appear under simultaneity.
- **When most valuable:** Systems live during the change; dual-write; jobs contending for rows with production traffic.

### 24. Reversibility / rollback review

- **How it works:** Assume the change must be reverted and verify there is an exact, *bounded* path back to the prior state — no data loss, no side effects.
- **Objective:** Ensure every destructive/mutating operation has a way back.
- **When most valuable:** Migrations, backfills, production writes, any operation irreversible by default.

---

## Part D — Engineering-quality Lenses

*What to examine in the artifact itself — correctness, structure, and the qualities that keep a system healthy.*

### 25. Functional correctness / requirement conformance

- **How it works:** Set aside how the code is built and ask whether it does what was actually asked. Read the change against its requirement/spec/ticket; confirm it serves the intended user need and handles the cases the requirement implies.
- **Objective:** Catch the most expensive defect class — correctly built code that solves the wrong problem.
- **When most valuable:** Always; especially when the implementation is elegant (elegance hides "but is this what we needed?"). This is the single most important review dimension.

### 26. Security review / threat modeling (STRIDE, OWASP Top 10)

- **How it works:** Examine attack surfaces — injection, authn/authz, data exposure, SSRF, deserialization; model threats by category. Includes static analysis (SAST) for insecure patterns and committed secrets, and credential-handling hygiene (rotation, storage, scope, leakage in logs).
- **Objective:** Find vulnerabilities before the attacker does.
- **When most valuable:** Exposed endpoints, sensitive/financial data, external integrations, any code touching credentials.

### 27. Performance / scalability review

- **How it works:** Analyze algorithmic complexity, query patterns (N+1, full scans, indexes), allocation, behavior under load and data growth, resource limits and quotas, peak/autoscaling behavior. For frontend, include Core Web Vitals (LCP/CLS/INP), bundle size, and re-renders.
- **Objective:** Avoid degradation at production scale and under peak load.
- **When most valuable:** Hot paths, queries over large tables, request-path code, conversion-critical UI, and before high-load events.

### 28. Data integrity / consistency review

- **How it works:** Verify data invariants, constraints, transactions, isolation semantics, exactly-once vs at-least-once.
- **Objective:** Ensure data never becomes inconsistent.
- **When most valuable:** Transactional, financial, event-driven systems, sagas.

### 29. Contract / API review

- **How it works:** Review the contract (proto, OpenAPI, schema) for backward compatibility, versioning, nullability, field evolution.
- **Objective:** Don't break consumers.
- **When most valuable:** Public/inter-service APIs, proto/schema changes.

### 30. Observability review

- **How it works:** Verify the change is *diagnosable* in production — metrics, structured logs, traces, alerts, tag cardinality.
- **Objective:** Ensure you can detect and debug when it goes wrong.
- **When most valuable:** Changes with possible silent failures; critical systems; gradual rollouts.

### 31. Operability / deployability review (rollout, flags, migrations)

- **How it works:** Review deploy ordering, gates, dual-write/backfill/switchover, compatibility during rollout, the operational rollback plan.
- **Objective:** Ensure the change reaches production safely.
- **When most valuable:** Schema changes, online migrations, zero-downtime systems.

### 32. Cross-document / cross-service consistency

- **How it works:** Read the artifact side by side with its neighbors (dependent spec, upstream ticket, API contract) and look for divergence in vocabulary, premises, and numbers.
- **Objective:** Ensure pieces that must fit together actually fit.
- **When most valuable:** Coupled multi-document/multi-service systems; changes that cross team/repo boundaries.

### 33. Type-design / invariant-expression review

- **How it works:** Evaluate whether the types make invalid states unrepresentable (encapsulation, expressing invariants via the type rather than runtime checks).
- **Objective:** Move errors from runtime to compile time.
- **When most valuable:** Introducing new types/domain models; languages with rich type systems.

### 34. Readability / maintainability review

- **How it works:** Focus on clarity, names, unit size/responsibility, adherence to codebase conventions. Includes comment/documentation accuracy: comments and docstrings must faithfully describe the code, with no stale or misleading statements (comment rot).
- **Objective:** Reduce maintenance cost and the chance of future bugs; keep documentation from misleading the future reader.
- **When most valuable:** Code read far more than written; bases with many contributors; after generating bulky documentation.

### 35. Simplification / YAGNI review

- **How it works:** Look for over-engineering, premature abstraction, dead code, duplication, simpler alternatives.
- **Objective:** Remove complexity that doesn't pay for itself.
- **When most valuable:** After functionality is correct; before crystallizing a design.

### 36. Dependency / supply-chain review

- **How it works:** Review new/updated dependencies for CVEs, licenses, maintenance, size/transitivity, typosquatting risk.
- **Objective:** Avoid vulnerabilities and inherited third-party debt.
- **When most valuable:** When adding/updating libs; periodic audits; build security.

---

## Part E — Beyond Back-end

*Domain-specific lenses for frontend, mobile, infrastructure, data, and cross-cutting concerns. Apply only the ones the artifact's domain calls for.*

### 37. Accessibility (a11y) review

- **How it works:** Check WCAG, ARIA semantics, keyboard navigation, contrast, screen readers.
- **Objective:** Ensure the UI is usable by everyone.
- **When most valuable:** Any public/regulated UI.

### 38. Responsiveness / cross-browser / cross-device review

- **How it works:** Behavior across breakpoints, browsers, and devices.
- **Objective:** Consistent experience across the audience's environments.
- **When most valuable:** UIs with a broad audience.

### 39. State / data-flow review

- **How it works:** State management, client-server synchronization, caching, UI race conditions.
- **Objective:** Keep UI state correct and predictable.
- **When most valuable:** Complex SPAs.

### 40. Mobile lifecycle / offline review

- **How it works:** Screen lifecycle, memory leaks, battery, background usage; behavior without network, sync queue, conflict resolution on reconnect.
- **Objective:** Keep the app efficient, stable, and correct on and off the network.
- **When most valuable:** Native and offline-first apps.

### 41. OS / device-version compatibility

- **How it works:** Android/iOS fragmentation, permissions, deprecated APIs.
- **Objective:** Work across the device matrix.
- **When most valuable:** Before store releases.

### 42. Privacy / compliance review (GDPR, LGPD, PCI)

- **How it works:** Data minimization, retention, consent, residency.
- **Objective:** Meet legal and regulatory obligations.
- **When most valuable:** Personal/financial data.

### 43. Infrastructure-as-Code review

- **How it works:** Idempotency, drift, blast radius, least-privilege IAM, state management.
- **Objective:** Safe, predictable infrastructure changes.
- **When most valuable:** Terraform/CloudFormation changes.

### 44. CI/CD pipeline review

- **How it works:** Pipeline security, gates, reproducibility, secrets in the build, supply chain.
- **Objective:** Keep delivery automation safe and reliable.
- **When most valuable:** When touching deploy automation.

### 45. Cost review (FinOps)

- **How it works:** Cost impact of provisioned resources, autoscaling, egress, data retention.
- **Objective:** Avoid runaway spend.
- **When most valuable:** Infra changes at scale.

### 46. Disaster-recovery / resilience review

- **How it works:** Backups, failover, RTO/RPO, chaos testing, graceful degradation.
- **Objective:** Survive failures with bounded loss.
- **When most valuable:** Critical services.

### 47. Data-pipeline / schema-evolution review

- **How it works:** Schema compatibility, backfill, data quality, lineage.
- **Objective:** Keep data correct as it evolves.
- **When most valuable:** ETL/ELT and data lakes.

### 48. Experiment / A-B test review

- **How it works:** Statistical power, guardrails, segmentation, validity.
- **Objective:** Ensure experiments yield trustworthy conclusions.
- **When most valuable:** Before running experiments.

### 49. Internationalization (i18n) / localization review

- **How it works:** Encoding, date/number/currency formatting, pluralization, RTL.
- **Objective:** Work correctly across locales.
- **When most valuable:** Multi-region products.

### 50. Documentation / spec self-review

- **How it works:** Placeholders, internal contradictions, ambiguity, scope.
- **Objective:** Ship clear, complete specs.
- **When most valuable:** When finalizing any spec/plan.

### 51. Architecture critic (adversarial)

- **How it works:** Review the target architecture against best practice, hunting over-engineering and simpler alternatives.
- **Objective:** Keep the design as simple as it can correctly be.
- **When most valuable:** Design proposals before implementation.

---

## Appendix — Composition Patterns

*How to chain strategies together.*

- **Lens rotation:** A different strategy per pass; do not repeat the same angle.
- **Find → verify pipeline:** Find candidates broadly, then verify each adversarially (voting/refutation) before acting.
- **Barrier when you need the whole:** Only synchronize between phases when the next phase needs *all* findings together (e.g. global dedup before expensive verification).
- **Scale to the ask:** "Find bugs" → few finders, simple vote. "Exhaustive audit" → large finder pool + 3–5 adversarial votes + synthesis.
- **No silent truncation:** If the review limited coverage (top-N, sampling, no retry), **log** what was left out — truncating silently reads as "covered everything."
- **Close with fresh eyes:** The last pass should be independent of the edit history.
