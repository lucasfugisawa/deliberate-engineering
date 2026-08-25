# Conductor template

The one contract that carries an irreversibility cluster, read from `SKILL.md` before you author a conduction's contract. Like the orchestration contracts, it **prescribes the fields, not the formatting**: keep the fields your cluster needs, and name the labels, columns, and stations for *your* cluster. The examples below span a git merge cascade, a batch data mutation, and a teardown on purpose, because the contract is cluster-kind-agnostic; the git set is never the schema.

One contract, rewritten as the cluster advances. The agent **generates** the world-state fields from a live read (git / gh / the relevant CLIs) and hand-writes the judgment fields; the operator executes every irreversible action.

The contract has a **required core**, and two **bookend sections whose necessity depends on the cluster's nature**: a pre-flight launch gate (required once the cluster has a point of no return, optional otherwise) and a post-state check (required for a data mutation, a lighter watch for a reversible rollout). Both are listed last below and **render first and last**, the launch gate opening the document and the post-state check closing it: the order here is the order they are explained, not the order they are read. The whole field set was seeded from a field record of *reversible* multi-repo git rollouts, one kind of cluster, and then hardened, by adversarial critique standing in for a pilot on a different kind, against the destructive hemisphere it originally missed; treat a field that does not fit your cluster as a prompt to generalize it, not a mandate.

---

## The CONDUCTOR contract

```markdown
# Conductor: <one-line cluster title>

## Role split & standing approvals        (required)
- **The agent conducts; the operator executes every irreversible action**: merge, release, deploy, data mutation, teardown. The agent prepares, re-derives, verifies, and queues; the human pulls each irreversible trigger (Rule 1). **An edit to a file that is itself the running artifact is a deploy.** Where a script, config or query runs straight from the checkout with no build or release step in between, saving the edit *is* the outward-facing action, so the prepare-then-execute line this split assumes does not exist there. Say which files in this cluster are like that, and put landing them on the operator's side with every other deploy.
- Standing approvals this run holds: <what the operator pre-authorized, and its bound>
- **Operator overrides in force**: <the lenses these fields cite that carry an operator override, plus the operator's standing rules in force for this session, both overrides of a shipped rule (Rule 1 included) and rules the operator added themselves; with the operation applied to each. **Three answers, not two**: the list; "none" when there are none; and "unreadable" when the file could not be consulted, saying why and that every shipped rule including Rule 1 was held in force. None means there is no calibration; unreadable means there may be one you did not see>, so a resumed session or a second operator inherits the calibration rather than rediscovering it, and is not handed a false clean.
- Legend: owner (who acts), status tokens; **last re-derivation**: <timestamp of the most recent world-state read>

## Never trust memory: re-derive before every gate        (required)
Re-derive world state (git / gh / CLIs) immediately before each gate and again at every resumption; a gate never runs against cached or remembered state (Rule 3, premise-freshness). At a resume, before re-running any step whose completion is uncertain, confirm it is safe to re-run (see the station table's re-run column): a non-idempotent step re-run (a second `balance = balance + X`, a partial batch) is worse than a gap.

## Verdict on the cluster as handed over        (required)
Before the gate table is fixed, say whether this cluster should run at all, against the world state you just re-derived rather than against the plan's own account of itself. **Run as given / run with these corrections / do not run**, plus the evidence that produced the verdict and, when it is not run-as-given, what changed and why. A conduction whose first real finding is that the plan is wrong is not a failed conduction, and this is where that lands: the gate graph below sequences a plan this field has already judged.
- **Corrections are cluster work, not preamble.** Anything you rewrote to make the plan runnable is new and unrehearsed, and it owes the same pre-write evidence, blast-radius bound and between-step checks as the steps it replaced. Carry it into the inventory below rather than treating it as done because you wrote it.
- **A do-not-run verdict is an output, not a stall.** Record it here, hand the operator what you would run instead, and stop. Do not park it in the launch gate below: that gate asks whether you are ready to begin, and it stops being required precisely when correcting the plan removes the point of no return.

## Definition of done, keystone, and point of no return        (required)
- **Inventory**: one row per remaining step, each with a concrete, verifiable done-condition. Done = every row checked.
- **Keystone**: the step after which rollback gets harder or changes shape.
- **Point of no return (PONR)**: the point after which rollback is *impossible*. It is a point, not necessarily a step you take: name every unrecallable side effect anywhere in this cluster's blast radius, both the steps you run (a hard delete, a destroyed snapshot) and the things that fire during the window without being steps at all (a scheduled job that pays out or emails, an external consumer that has already read, a webhook already dispatched, a partner system you cannot un-tell). For each, what makes it unrecallable and the last safe abort point before it. If nothing in the blast radius is unrecallable, say so explicitly: that is what makes its launch gate optional. **Say which kind of nothing it is.** Never having one (a pure git cascade you can revert) and having removed one while correcting the plan look identical here, and are not: the second rests on a correction the reader has not checked. When a correction removed it, name what the point of no return was under the plan as handed over, and what removed it.

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
- **Pre-write evidence**: run the step in no-op / dry-run / shadow mode first and record what it *would* touch, before pulling the trigger (verify #8: dry-run before executing; #4: check the real schema and real data before trusting what the write assumes; #23, only where the step must *preserve* behavior: differential, run old and new against the same input). For a git merge this is the diff and conflict check; for a data mutation, the `SELECT` the `UPDATE` will hit.
- **Expected scope / blast-radius bound + abort threshold**: the pre-declared bound that is itself a stop-rule (planning #7: blast-radius modeling, where the step changes the meaning of shared data; verify #21: quantify real usage and cross-check truth before mutating). "~1,200 rows; halt if the dry-run shows > 2,000"; "these 3 services, no more".

## Between-step verification battery: after each step        (required)
After each step and before the next, run these and record the result against its expected value; do not advance on a bare exit code (verify #17: annotate every verification with its expected value; #18: one change at a time, with named watch-fors; #3: name what would refute it, so the check can actually fail; #22: its breadth must cover the claim it backs). Escalate the staged-promotion and kill-switch checks where the cluster crosses environments (#11, #14), and run the final confidence check before the irreversible production action (#15). For a data mutation, **post-state verification is core, not optional**: a bad silent write is invisible until read back (verify #20).
**Expected is authored; Observed and Verdict are filled at execution**, by whoever runs the step. A table shipped with Expected complete and Observed empty is a finished deliverable, not an unfinished one, and the same holds for the post-state table below.

| After step | Check / metric | Expected | Observed | Verdict |
|------------|----------------|----------|----------|---------|
| <step>     | <the exact check or query> | <the value that means healthy> | <read now> | pass / hold / fail |

## Operator wave queue        (required)
The next irreversible actions, each as the exact action plus the inline division of labor.
- [ ] <exact action: "merge PR #123 into main" / "run batch 2 of the backfill" / "delete service X">, with the inline division of labor (<who does what: "I rebase, you merge">)

## Honesty rails        (required)
The conduction-specific slice, not general note-taking: **Deferred** (work pushed past this hot cluster, named so it is not forgetting), **Unverified** (hypotheses not yet confirmed; do not treat as fact mid-cluster), **Radar** (findings to keep watching that are not yet action).

## Session residue        (required on interruption)
The live state the re-derivation last read, the exact next action, any half-taken step, and its **re-run safety**, so a fresh session resumes the cockpit without trusting memory. **Three answers, not two**: safe to re-run; must be reconciled by hand; or fails safe, meaning re-running errors harmlessly and the check is to read the current state first rather than to reconcile anything. A schema migration is usually the third, and collapsing it into either of the others costs a resumed session either a needless reconciliation or a wrongly confident retry.

## Closure marker        (required at completion)
A frozen banner ("CLUSTER COMPLETE, <date>; this doc is closed"), confirmation that the closeout obligations were discharged (verify #24), and, if a program tracker handed the baton, the baton returned to it.

## Launch gate: pre-flight go / no-go        (REQUIRED once anything in the blast radius is unrecallable; optional otherwise)
The gate to begin at all: every precondition that must hold before the first irreversible step. For a reversible cascade this is optional (you can start and stop freely); for a teardown or a hard-delete batch it is *the* safety gate and is mandatory. Key it on the PONR field above: removing a destructive step from the plan does not make this gate optional while anything else in the blast radius is still unrecallable.
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
