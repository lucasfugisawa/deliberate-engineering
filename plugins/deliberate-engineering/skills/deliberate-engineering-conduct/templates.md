# Conductor template

The one contract that carries an irreversibility cluster, read on demand from `SKILL.md` when you conduct one, not loaded up front. Like the orchestration contracts, it **prescribes the fields, not the formatting**: keep the fields your cluster needs, and name the labels, columns, and stations for *your* cluster. The examples below span a git merge cascade, a batch data mutation, and a teardown on purpose, because the contract is cluster-kind-agnostic; the git set is never the schema.

One contract, rewritten as the cluster advances. The agent **generates** the world-state fields from a live read (git / gh / the relevant CLIs) and hand-writes the judgment fields; the operator executes every irreversible action.

The contract has a **required core**, and two **bookend sections whose necessity depends on the cluster's nature**: a pre-flight launch gate (required once the cluster has a point of no return, optional otherwise) and a post-state check (required for a data mutation, a lighter watch for a reversible rollout). The whole field set was seeded from a field record of *reversible* multi-repo git rollouts, one kind of cluster, and then hardened, by adversarial critique standing in for a pilot on a different kind, against the destructive hemisphere it originally missed; treat a field that does not fit your cluster as a prompt to generalize it, not a mandate.

---

## The CONDUCTOR contract

```markdown
# Conductor: <one-line cluster title>

## Role split & standing approvals        (required)
- **The agent conducts; the operator executes every irreversible action**: merge, release, deploy, data mutation, teardown. The agent prepares, re-derives, verifies, and queues; the human pulls each irreversible trigger (Rule 1).
- Standing approvals this run holds: <what the operator pre-authorized, and its bound>
- Legend: owner (who acts), status tokens; **last re-derivation**: <timestamp of the most recent world-state read>

## Never trust memory: re-derive before every gate        (required)
Re-derive world state (git / gh / CLIs) immediately before each gate and again at every resumption; a gate never runs against cached or remembered state (Rule 3, premise-freshness). At a resume, before re-running any step whose completion is uncertain, confirm it is safe to re-run (see the station table's re-run column): a non-idempotent step re-run (a second `balance = balance + X`, a partial batch) is worse than a gap.

## Definition of done, keystone, and point of no return        (required)
- **Inventory**: one row per remaining step, each with a concrete, verifiable done-condition. Done = every row checked.
- **Keystone**: the step after which rollback gets harder or changes shape.
- **Point of no return (PONR)**: the step after which rollback is *impossible* (a hard delete, a destroyed snapshot, an external side effect that cannot be recalled). Name it, what makes it irreversible, and the last safe abort point before it. If the cluster has no PONR (a pure git cascade you can revert), say so explicitly: that is what makes its launch gate optional.

## Gated groups: order, gates, recovery, holds, abort        (required)
- **Step order**: the fixed sequence and why (planning #12: sequence so no intermediate state breaks; #13: the old code must survive each deploy). Examples: merge/deploy order; "batch A verified complete before B starts"; "drain traffic before deleting the load balancer".
- **Inter-step gates**: the precondition per edge (verify #13: deploy ordering and dependency availability). "X live in prod before Y deploys"; "A's row-count verified before B".
- **Recovery path & its verification**: the way back in whatever form this cluster has, git revert / kill-switch / restore-from-snapshot, and evidence it was actually tested before the PONR (verify #14: the kill-switch and its safe default *work*; #20: a bounded, reversible path back). A recovery path assumed but untested is not a recovery path.
- **Holds (with expiry)**: any deliberate pause, and the explicit condition or time that releases it, so a hold does not rot into a silent block.
- **Abort / halt**: the emergency stop, distinct from a hold: who may halt, on what signal, and the safe state a halt must leave the system in. A hold is a planned pause; an abort is "something is wrong, stop now, here is where it is safe to stop".

## Per-item station table: where the gates live        (required)
Checkbox state, not memory or a prose note: in the field, the one gate recorded only as a reminder was the one that slipped. **Name the columns for the stations THIS cluster's items pass through.** One example set per cluster kind, not the schema:
- git rollout: `conflict-free / rebased / re-pinned / merged / deployed / verified`
- data batch: `dry-run-reviewed / snapshot-taken / mutated / row-count-verified / re-run-safe`
- teardown: `dependency-drained / snapshotted / deleted / confirmed-gone`

| Item | <station 1> | <station 2> | <station 3> | <verified> |
|------|-------------|-------------|-------------|------------|
| <PR / batch / resource> | [ ] | [ ] | [ ] | [ ] |

## Before each irreversible step: dry-run and scope bound        (required; the form varies by cluster)
- **Pre-write evidence**: run the step in no-op / dry-run / shadow mode first and record what it *would* touch, before pulling the trigger (verify #8: dry-run before executing; #23, only where the step must *preserve* behavior: differential, run old and new against the same input). For a git merge this is the diff and conflict check; for a data mutation, the `SELECT` the `UPDATE` will hit.
- **Expected scope / blast-radius bound + abort threshold**: the pre-declared bound that is itself a stop-rule (planning #7: blast-radius modeling; verify #21: quantify real usage and cross-check truth before mutating). "~1,200 rows; halt if the dry-run shows > 2,000"; "these 3 services, no more".

## Between-step verification battery: after each step        (required)
After each step and before the next, run these and record the result against its expected value; do not advance on a bare exit code (verify #17: annotate every verification with its expected value; #18: one change at a time, with named watch-fors). Escalate the staged-promotion and kill-switch checks where the cluster crosses environments (#11, #14), and run the final confidence check before the irreversible production action (#15). For a data mutation, **post-state verification is core, not optional**: a bad silent write is invisible until read back (verify #20).
| After step | Check / metric | Expected | Observed | Verdict |
|------------|----------------|----------|----------|---------|
| <step>     | <the exact check or query> | <the value that means healthy> | <read now> | pass / hold / fail |

## Operator wave queue        (required)
The next irreversible actions, each as the exact action plus the inline division of labor.
- [ ] <exact action: "merge PR #123 into main" / "run batch 2 of the backfill" / "delete service X">, with the inline division of labor (<who does what: "I rebase, you merge">)

## Honesty rails        (required)
The conduction-specific slice, not general note-taking: **Deferred** (work pushed past this hot cluster, named so it is not forgetting), **Unverified** (hypotheses not yet confirmed; do not treat as fact mid-cluster), **Radar** (findings to keep watching that are not yet action).

## Session residue        (required on interruption)
The live state the re-derivation last read, the exact next action, any half-taken step, and its **re-run safety** (safe to re-run, or must be reconciled by hand?), so a fresh session resumes the cockpit without trusting memory.

## Closure marker        (required at completion)
A frozen banner ("CLUSTER COMPLETE, <date>; this doc is closed"), confirmation that the closeout obligations were discharged (verify #24), and, if a program tracker handed the baton, the baton returned to it.

## Launch gate: pre-flight go / no-go        (REQUIRED once the cluster has a point of no return; optional otherwise)
The gate to begin at all: every precondition that must hold before the first irreversible step. For a reversible cascade this is optional (you can start and stop freely); for a teardown or a hard-delete batch it is *the* safety gate and is mandatory.
| Precondition | Holds? |
|--------------|--------|
| <recovery path verified; blast radius bounded; abort owner named; dry-run reviewed; CI green; flag in safe default> | [ ] |
- **Verdict**: GO / NO-GO, and who gave it.

## Post-state / post-rollout check        (REQUIRED for a data mutation; a lighter watch for a reversible rollout)
The aftermath: for a mutation, verify the write landed correctly by reading the post-state back (verify #20); for a rollout, the metrics and health to watch for a stated window, with expected values.
| Window | Check / metric | Expected | Observed | Verdict |
|--------|----------------|----------|----------|---------|
| <e.g. first hour, or immediately post-write> | <the metric or read-back> | <healthy value> | <read> | pass / regressed |
```
