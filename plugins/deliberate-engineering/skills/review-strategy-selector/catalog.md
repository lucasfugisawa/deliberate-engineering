# Review Strategy Catalog

This catalog contains 57 review strategies organized into five groups plus composition patterns. Each strategy is a lens through which to examine work. The selector skill references these by number to build custom review workflows.

## Master Principle

Strategies **compose**. The strongest pattern is to *rotate the lens each pass* (a new strategy per review), validate empirically where possible, and **close with a fresh-eyes pass that has no history of the edits** to break accumulated bias. This applies equally to documentation, design, and code.

---

## Part A — Process / Meta-review Strategies

*How to conduct the review, independent of the artifact's domain.*

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

---

## Part B — Verification / Evidence Strategies

*How to prove a claim is true rather than assume it.*

### 11. Empirical validation (actually execute)

- **How it works:** Instead of reasoning about what the code/SQL does, **execute** it in a disposable environment with constructed scenarios and assert on the real result.
- **Objective:** Trade "I think it works" for "I saw it work."
- **When most valuable:** Subtle-semantics logic (data-modifying CTEs, NULL handling, non-guaranteed ordering, idempotency, rollback).

### 12. Validation against real data/systems (ground truth)

- **How it works:** Confront the artifact's premises with the external source of truth — production/staging data, the real schema, the real API. You don't review the text; you review whether the text **matches reality**.
- **Objective:** Catch wrong factual premises (distributions, cardinality, types, volumes) that no internal reading would reveal.
- **When most valuable:** Specs/designs that depend on data characteristics; integrations; any cited number.

### 13. Source-of-truth verification (correct canonical reference)

- **How it works:** Ensure you review against the canonical reference (e.g. `origin/main`), not a stale local copy or a feature branch.
- **Objective:** Avoid correct conclusions about the wrong artifact.
- **When most valuable:** Multi-branch/multi-repo environments; worktrees; parallel checkouts.

### 14. Assumption / invariant audit

- **How it works:** Explicitly list every implicit premise ("this field is unique", "this runs after that") and validate each one.
- **Objective:** Make visible what is being assumed without proof.
- **When most valuable:** Premise-dense designs; integrations; behavior dependent on another system.

### 15. Coverage analysis (walk every case)

- **How it works:** Systematically enumerate all cases/branches/states and verify, one by one, which mechanism handles each — making explicit what is **left out** and why.
- **Objective:** Turn "I think it covers everything" into a proof by exhaustion; make tolerated gaps visible.
- **When most valuable:** State taxonomies, state machines, migration/backfill logic.

### 16. Boundary / edge-case review

- **How it works:** Focus on the extremes — empty, one, many, numeric limits, timezone/DST, encoding, off-by-one, nulls/absent.
- **Objective:** Bugs live at the edges, not on the happy path.
- **When most valuable:** Parsing, aggregations, time windows, pagination.

### 17. Test-quality review (review the tests, not just the code)

- **How it works:** Evaluate whether the tests actually exercise the behavior (meaningful assertions, edge cases, absence of tautological tests), branch coverage.
- **Objective:** Ensure the suite truly protects against regression.
- **When most valuable:** Before trusting "the tests pass"; in PRs that add tests alongside the feature.

---

## Part C — Failure & Contradiction Reasoning Strategies

### 18. Apparent-contradiction reconciliation

- **How it works:** On finding an apparent contradiction, don't fix it immediately — investigate until you classify it as (a) a real bug, (b) a false conflict due to different context/timing, or (c) imprecise wording.
- **Objective:** Avoid both ignoring bugs and "fixing" things that were correct.
- **When most valuable:** Rules with temporal/contextual nuance; when the artifact contradicts an established norm.

### 19. Failure-mode / pre-mortem / FMEA

- **How it works:** Assume the change failed in production and reason backward about the causes; or enumerate failure modes and rank them by severity × probability.
- **Objective:** Anticipate failures before they become expensive.
- **When most valuable:** High-impact / low-reversibility changes.

### 20. Silent-failure hunting

- **How it works:** Specifically look for paths where an error is swallowed, a fallback masks a problem, or a failure emits no signal at all.
- **Objective:** Ensure failures are detectable, not invisible.
- **When most valuable:** Error handling, retries, fallbacks, integrations that can degrade silently.

### 21. Concurrency / race review

- **How it works:** Analyze what happens when the operation runs **at the same time** as other writes — torn reads, locks, windows (e.g. export→merge), non-deterministic ordering, deadlocks.
- **Objective:** Find bugs that only appear under simultaneity.
- **When most valuable:** Systems live during the change; dual-write; jobs contending for rows with production traffic.

### 22. Reversibility / rollback review

- **How it works:** Assume the change must be reverted and verify there is an exact, *bounded* path back to the prior state — no data loss, no side effects.
- **Objective:** Ensure every destructive/mutating operation has a way back.
- **When most valuable:** Migrations, backfills, production writes, any operation irreversible by default.

---

## Part D — Back-end-focused Reviews

### 23. Security review / threat modeling (STRIDE, OWASP Top 10)

- **How it works:** Examine attack surfaces — injection, authn/authz, data exposure, SSRF, deserialization; model threats by category.
- **Objective:** Find vulnerabilities before the attacker does.
- **When most valuable:** Exposed endpoints, sensitive/financial data, external integrations.

### 24. Performance / scalability review

- **How it works:** Analyze algorithmic complexity, query patterns (N+1, full scans, indexes), allocation, behavior under load and data growth.
- **Objective:** Avoid degradation at production scale.
- **When most valuable:** Hot paths, queries over large tables, code on the request path.

### 25. Data integrity / consistency review

- **How it works:** Verify data invariants, constraints, transactions, isolation semantics, exactly-once vs at-least-once.
- **Objective:** Ensure data never becomes inconsistent.
- **When most valuable:** Transactional, financial, event-driven systems, sagas.

### 26. Contract / API review

- **How it works:** Review the contract (proto, OpenAPI, schema) for backward compatibility, versioning, nullability, field evolution.
- **Objective:** Don't break consumers.
- **When most valuable:** Public/inter-service APIs, proto/schema changes.

### 27. Observability review

- **How it works:** Verify the change is *diagnosable* in production — metrics, structured logs, traces, alerts, tag cardinality.
- **Objective:** Ensure you can detect and debug when it goes wrong.
- **When most valuable:** Changes with possible silent failures; critical systems; gradual rollouts.

### 28. Operability / deployability review (rollout, flags, migrations)

- **How it works:** Review deploy ordering, gates, dual-write/backfill/switchover, compatibility during rollout, the operational rollback plan.
- **Objective:** Ensure the change reaches production safely.
- **When most valuable:** Schema changes, online migrations, zero-downtime systems.

### 29. Cross-document / cross-service consistency

- **How it works:** Read the artifact side by side with its neighbors (dependent spec, upstream ticket, API contract) and look for divergence in vocabulary, premises, and numbers.
- **Objective:** Ensure pieces that must fit together actually fit.
- **When most valuable:** Coupled multi-document/multi-service systems; changes that cross team/repo boundaries.

### 30. Type-design / invariant-expression review

- **How it works:** Evaluate whether the types make invalid states unrepresentable (encapsulation, expressing invariants via the type rather than runtime checks).
- **Objective:** Move errors from runtime to compile time.
- **When most valuable:** Introducing new types/domain models; languages with rich type systems.

### 31. Comment / documentation-accuracy review

- **How it works:** Verify that comments and docstrings faithfully describe the code (comment rot), with no stale or misleading statements.
- **Objective:** Avoid documentation debt that misleads the future reader.
- **When most valuable:** After generating bulky documentation; before finalizing PRs that touch comments.

### 32. Readability / maintainability review

- **How it works:** Focus on clarity, names, unit size/responsibility, adherence to codebase conventions.
- **Objective:** Reduce maintenance cost and the chance of future bugs.
- **When most valuable:** Code read far more than written; bases with many contributors.

### 33. Simplification / YAGNI review

- **How it works:** Look for over-engineering, premature abstraction, dead code, duplication, simpler alternatives.
- **Objective:** Remove complexity that doesn't pay for itself.
- **When most valuable:** After functionality is correct; before crystallizing a design.

### 34. Dependency / supply-chain review

- **How it works:** Review new/updated dependencies for CVEs, licenses, maintenance, size/transitivity, typosquatting risk.
- **Objective:** Avoid vulnerabilities and inherited third-party debt.
- **When most valuable:** When adding/updating libs; periodic audits; build security.

---

## Part E — Reviews Beyond Back-end

### Frontend / UX

### 35. Accessibility (a11y) review

- **How it works:** Check WCAG, ARIA semantics, keyboard navigation, contrast, screen readers.
- **Objective:** Ensure the UI is usable by everyone.
- **When most valuable:** Any public/regulated UI.

### 36. Responsiveness / cross-browser / cross-device review

- **How it works:** Behavior across breakpoints, browsers, and devices.
- **Objective:** Consistent experience across the audience's environments.
- **When most valuable:** UIs with a broad audience.

### 37. Visual regression review

- **How it works:** Compare before/after screenshots to catch unintended visual breaks.
- **Objective:** Prevent accidental visual regressions.
- **When most valuable:** Design systems and CSS refactors.

### 38. Frontend performance (Core Web Vitals)

- **How it works:** LCP/CLS/INP, bundle size, lazy-loading, re-renders.
- **Objective:** Keep the UI fast and stable.
- **When most valuable:** Conversion-critical pages.

### 39. State / data-flow review

- **How it works:** State management, client-server synchronization, caching, UI race conditions.
- **Objective:** Keep UI state correct and predictable.
- **When most valuable:** Complex SPAs.

### Mobile

### 40. Lifecycle / resource review

- **How it works:** Screen lifecycle, memory leaks, battery, background usage.
- **Objective:** Keep the app efficient and stable.
- **When most valuable:** Native apps.

### 41. Offline / sync review

- **How it works:** Behavior without network, sync queue, conflict resolution.
- **Objective:** Ensure correctness offline and on reconnect.
- **When most valuable:** Offline-first apps.

### 42. OS / device-version compatibility

- **How it works:** Android/iOS fragmentation, permissions, deprecated APIs.
- **Objective:** Work across the device matrix.
- **When most valuable:** Before store releases.

### Security (specialized)

### 43. Penetration testing / dynamic analysis (DAST)

- **How it works:** Attack the running system like a real attacker.
- **Objective:** Find exploitable vulnerabilities in the live system.
- **When most valuable:** Exposed systems pre-release.

### 44. Static analysis (SAST) / secret scanning

- **How it works:** Scan the code for insecure patterns and committed secrets.
- **Objective:** Catch issues early and continuously.
- **When most valuable:** In CI, continuously.

### 45. Secrets / credential-handling review

- **How it works:** Rotation, storage, scope, leakage in logs.
- **Objective:** Keep credentials safe.
- **When most valuable:** Any system with credentials.

### 46. Privacy / compliance review (GDPR, LGPD, PCI)

- **How it works:** Data minimization, retention, consent, residency.
- **Objective:** Meet legal and regulatory obligations.
- **When most valuable:** Personal/financial data.

### DevOps / Infra / Platform

### 47. Infrastructure-as-Code review

- **How it works:** Idempotency, drift, blast radius, least-privilege IAM, state management.
- **Objective:** Safe, predictable infrastructure changes.
- **When most valuable:** Terraform/CloudFormation changes.

### 48. CI/CD pipeline review

- **How it works:** Pipeline security, gates, reproducibility, secrets in the build, supply chain.
- **Objective:** Keep delivery automation safe and reliable.
- **When most valuable:** When touching deploy automation.

### 49. Cost review (FinOps)

- **How it works:** Cost impact of provisioned resources, autoscaling, egress, data retention.
- **Objective:** Avoid runaway spend.
- **When most valuable:** Infra changes at scale.

### 50. Disaster-recovery / resilience review

- **How it works:** Backups, failover, RTO/RPO, chaos testing, graceful degradation.
- **Objective:** Survive failures with bounded loss.
- **When most valuable:** Critical services.

### 51. Capacity / scalability review

- **How it works:** Resource limits, quotas, peak behavior, autoscaling.
- **Objective:** Handle load without falling over.
- **When most valuable:** Before high-load events.

### Data / ML

### 52. Data-pipeline / schema-evolution review

- **How it works:** Schema compatibility, backfill, data quality, lineage.
- **Objective:** Keep data correct as it evolves.
- **When most valuable:** ETL/ELT and data lakes.

### 53. ML model review

- **How it works:** Bias/fairness, data leakage, drift, reproducibility, honest evaluation metrics.
- **Objective:** Keep models correct and fair in production.
- **When most valuable:** Models in production.

### 54. Experiment / A-B test review

- **How it works:** Statistical power, guardrails, segmentation, validity.
- **Objective:** Ensure experiments yield trustworthy conclusions.
- **When most valuable:** Before running experiments.

### Cross-cutting

### 55. Internationalization (i18n) / localization review

- **How it works:** Encoding, date/number/currency formatting, pluralization, RTL.
- **Objective:** Work correctly across locales.
- **When most valuable:** Multi-region products.

### 56. Documentation / spec self-review

- **How it works:** Placeholders, internal contradictions, ambiguity, scope.
- **Objective:** Ship clear, complete specs.
- **When most valuable:** When finalizing any spec/plan.

### 57. Architecture critic (adversarial)

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
