#!/usr/bin/env python3
"""Negative controls for check-invariants.py.

A check nobody has watched fail is not a check. This copies the repository to a
scratch tree, breaks one invariant at a time, and asserts that the guard both
notices (the right check fails) and is quiet otherwise (a clean tree passes).

Run from the repository root: python3 scripts/test-check-invariants.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = "plugins/deliberate-engineering/skills"
CM = "plugins/deliberate-engineering/commands"


def run_guard(tree, base=None):
    cmd = [sys.executable, os.path.join(tree, "scripts", "check-invariants.py")]
    if base:
        cmd += ["--base", base]
    return subprocess.run(cmd, cwd=tree, capture_output=True, text=True)


def edit(tree, relpath, old, new, count=1):
    p = os.path.join(tree, relpath)
    with open(p, encoding="utf-8") as fh:
        s = fh.read()
    assert old in s, f"setup failed: {old!r} not in {relpath}"
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(s.replace(old, new, count))


def fresh_tree(stack):
    tree = tempfile.mkdtemp(prefix="invariant-nc-")
    stack.append(tree)
    # The scratch tree must be a faithful copy: a file the guard reads but the
    # copy omits produces a failure that belongs to the harness, not to the code.
    for item in ("plugins", "scripts", "docs", "README.md", "CONTRIBUTING.md", "CHANGELOG.md"):
        src = os.path.join(ROOT, item)
        dst = os.path.join(tree, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    return tree


def git_snapshot(tree):
    env = dict(os.environ, GIT_AUTHOR_NAME="nc", GIT_AUTHOR_EMAIL="nc@x",
               GIT_COMMITTER_NAME="nc", GIT_COMMITTER_EMAIL="nc@x")
    for args in (["init", "-q"], ["add", "-A"], ["commit", "-qm", "base"]):
        subprocess.run(["git"] + args, cwd=tree, check=True, env=env, capture_output=True)


CASES = []


def case(name, check, mutate, needs_git=False):
    CASES.append((name, check, mutate, needs_git))


case("renumbering a catalog", "append-only",
     lambda t: edit(t, f"{SK}/review-strategy-selector/catalog.md", "### 35.", "### 135."),
     needs_git=True)

case("a citation pointing at no lens", "citations",
     lambda t: edit(t, f"{SK}/deliberate-engineering-capture/SKILL.md", "review #35", "review #999"))

case("a rule citation that is not a rule", "citations",
     lambda t: edit(t, f"{SK}/deliberate-engineering-router/SKILL.md", "Rule 1", "Rule 42"))

case("dropping the override consult from a selector", "consult",
     lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md",
                    "**Operator overrides.** Before applying the selected lenses, consult `deliberate-engineering-overrides`",
                    "**Operator overrides.** Before applying the selected lenses, think about it"))

case("an exemption with no reason", "consult",
     lambda t: open(os.path.join(t, "scripts", "consult-exemptions.txt"), "a").write(
         "\ndeliberate-engineering-conduct:\n"))

case("an exemption for a skill that does not exist", "consult",
     lambda t: open(os.path.join(t, "scripts", "consult-exemptions.txt"), "a").write(
         "\ndeliberate-engineering-ghost: no such skill\n"))

case("a sixth catalog the harness cannot see", "catalog-coverage",
     lambda t: (os.makedirs(os.path.join(t, SK, "sixth-strategy-selector"), exist_ok=True),
                open(os.path.join(t, SK, "sixth-strategy-selector", "catalog.md"), "w").write(
                    "# Sixth\n\nThis catalog contains 1 strategy.\n\n### 1. A lens\n"),
                open(os.path.join(t, SK, "sixth-strategy-selector", "SKILL.md"), "w").write(
                    "---\nname: sixth-strategy-selector\ndescription: \"x\"\n---\n\n# Sixth\n")))

case("a command invoking a skill that does not exist", "commands",
     lambda t: open(os.path.join(t, CM, "ghost.md"), "w").write(
         "---\ndescription: \"x\"\n---\n\n# Ghost\n\nInvoke the `deliberate-engineering-ghost` skill against $ARGUMENTS.\n"))

case("a thirteenth command while the README says twelve", "commands",
     lambda t: open(os.path.join(t, CM, "extra.md"), "w").write(
         "---\ndescription: \"x\"\n---\n\n# Extra\n\nInvoke the `deliberate-engineering-state` skill against $ARGUMENTS.\n"))

case("renaming a section and leaving the pointer", "section-refs",
     lambda t: edit(t, f"{SK}/deliberate-engineering-router/SKILL.md",
                    "## The altitude check: does this fit one session?",
                    "## Checking the altitude"))

case("diverging a passage claimed identical", "identical",
     lambda t: edit(t, f"{SK}/planning-strategy-selector/SKILL.md",
                    "**Operator overrides.** Before applying the selected lenses",
                    "**Operator overrides.** Before applying the picked lenses"))

case("a link to a file that does not exist", "links",
     lambda t: edit(t, "README.md", "](docs/guides/README.md)", "](docs/guides/READMEE.md)"))

case("an anchor that matches no heading", "links",
     lambda t: edit(t, "README.md", "](#whats-inside)", "](#whats-inside-nowhere)"))

case("a doubled word", "artifacts",
     lambda t: edit(t, "README.md", "One mental model runs", "One mental mental model runs"))



case("a lens no step of its selector routes", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md",
                    "in play** → 14 source-of-truth verification",
                    "in play** -> source-of-truth verification"))

case("a lens appended to a catalog and routed nowhere", "reachability",
     lambda t: edit(t, f"{SK}/planning-strategy-selector/catalog.md",
                    "\n## Part B",
                    "\n### 99. A lens nobody routed\n\n- **How it works:** it does not matter.\n"
                    "- **Objective:** to be unreachable.\n- **When most valuable:** never.\n\n## Part B"))

case("a group exemption with no reason", "reachability",
     lambda t: open(os.path.join(t, "scripts", "routing-exemptions.txt"), "a").write(
         "\ngroup planning-strategy-selector Part C:\n"))

case("a group exemption naming a Part that does not exist", "reachability",
     lambda t: open(os.path.join(t, "scripts", "routing-exemptions.txt"), "a").write(
         "\ngroup communication-collaboration-selector Part Q: the flat catalog has no Parts at all.\n"))

case("a lens exemption naming a lens that does not exist", "reachability",
     lambda t: open(os.path.join(t, "scripts", "routing-exemptions.txt"), "a").write(
         "\nlens review-strategy-selector 999: no such lens.\n"))


def main():
    stack = []
    failures = []
    try:
        clean = fresh_tree(stack)
        git_snapshot(clean)
        r = run_guard(clean, base="HEAD")
        if r.returncode != 0:
            print("FAIL: the guard does not pass on an unmodified tree")
            print(r.stdout[-2000:])
            return 1
        print("  ok: clean tree passes (the guard is quiet when nothing is broken)")

        for name, check, mutate, needs_git in CASES:
            tree = fresh_tree(stack)
            base = None
            if needs_git:
                git_snapshot(tree)
                base = "HEAD"
            mutate(tree)
            r = run_guard(tree, base=base)
            caught = r.returncode != 0 and re.search(rf"FAIL \[{re.escape(check)}\]", r.stdout)
            if caught:
                print(f"  ok: {name} -> caught by [{check}]")
            else:
                print(f"  FAIL: {name} -> NOT caught (expected [{check}])")
                failures.append(name)
    finally:
        for t in stack:
            shutil.rmtree(t, ignore_errors=True)

    print()
    if failures:
        print(f"Negative controls FAILED: {len(failures)} mutation(s) went unnoticed: {failures}")
        return 1
    print(f"Negative controls OK: {len(CASES)} mutations, each caught by its own check.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
