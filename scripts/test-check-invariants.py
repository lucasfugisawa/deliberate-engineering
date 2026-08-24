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



def replace_line(t, relpath, prefix, new_line):
    """Swap the whole line starting with prefix, so a mutation cannot leave a tail behind."""
    p = os.path.join(t, relpath)
    with open(p, encoding="utf-8") as fh:
        lines = fh.readlines()
    hit = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(hit) == 1, f"setup failed: {prefix!r} matched {len(hit)} lines in {relpath}"
    lines[hit[0]] = new_line
    with open(p, "w", encoding="utf-8") as fh:
        fh.writelines(lines)



def replace_all_lines(t, relpath, pattern, replacement):
    """Rewrite every line matching pattern, for mutations that must hit a whole set."""
    import re as _re
    p = os.path.join(t, relpath)
    with open(p, encoding="utf-8") as fh:
        s = fh.read()
    new = _re.sub(pattern, replacement, s, flags=_re.M)
    assert new != s, f"setup failed: {pattern!r} matched nothing in {relpath}"
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(new)


CASES = []
ACCEPTS = []


def case(name, check, mutate, needs_git=False, expect=None):
    """expect: a substring the failure must contain.

    Without it a control only proves that SOME check fired, which let six of these
    pass on the reason gate rather than on the branch they name. Five fail() calls
    could be deleted with the suite still green.
    """
    CASES.append((name, check, mutate, needs_git, expect))


def accepts(name, mutate):
    """A positive control: this routing form must KEEP the guard green.

    Every mutation control asserts a check fires. That is half the contract, and
    the missing half is what let a broken routing form ship: `lenses?` parses as
    "lense" plus an optional s, so the documented `lens N` citation never matched
    and no control noticed, because none exercised the form.
    """
    ACCEPTS.append((name, mutate))


case("renumbering a catalog", "append-only",
     lambda t: edit(t, f"{SK}/review-strategy-selector/catalog.md", "### 35.", "### 135."),
     needs_git=True)

case("a citation pointing at no lens", "citations",
     lambda t: edit(t, f"{SK}/deliberate-engineering-capture/SKILL.md", "review #35", "review #999"))

case("a rule citation that is not a rule", "citations",
     lambda t: edit(t, f"{SK}/deliberate-engineering-router/SKILL.md", "Rule 1", "Rule 42"))

def drop_every_consult(t, relpath):
    """A selector now carries two consults, one for lenses and one for patterns.

    Removing only the first leaves the skill still consulting the override layer, which
    is what the consult check actually asks; that mutation is caught by the identical-block
    guard instead. To test the consult check's own claim, both have to go.
    """
    for old in ("Before applying the selected lenses, consult `deliberate-engineering-overrides`",
                "Before composing, consult `deliberate-engineering-overrides`"):
        edit(t, relpath, old, old.replace("consult `deliberate-engineering-overrides`", "think about it"))


case("dropping every override consult from a selector", "consult",
     lambda t: drop_every_consult(t, f"{SK}/review-strategy-selector/SKILL.md"))

case("dropping only the lens consult, leaving the pattern one", "identical",
     lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md",
                    "**Operator overrides.** Before applying the selected lenses, consult `deliberate-engineering-overrides`",
                    "**Operator overrides.** Before applying the selected lenses, think about it"),
     expect="Operator overrides consult")

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



EX = lambda t: os.path.join(t, "scripts", "routing-exemptions.txt")


def append_exemption(t, line):
    with open(EX(t), "a", encoding="utf-8") as fh:
        fh.write(line)


ONLY_14 = ("in play** \u2192 14 source-of-truth verification: confirm you are reading the "
           "canonical copy before judging it.")

accepts("the lens-N form routes",
        lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md", ONLY_14,
                       "in play** \u2192 apply lens 14 before judging anything."))

accepts("the plural lenses-N form routes",
        lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md", ONLY_14,
                       "in play** \u2192 among the lenses 14 belongs here."))

accepts("the numbers-only parenthesis form routes",
        lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md", ONLY_14,
                       "in play** \u2192 source-of-truth checking, lens (14)."))

accepts("the number-beside-its-title-word form routes",
        lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md", ONLY_14,
                       "in play** \u2192 14 source-of-truth checking."))

case("a lens heading that looks like a lens and is malformed", "reachability",
     lambda t: edit(t, f"{SK}/planning-strategy-selector/catalog.md",
                    "### 20.", "### 20"))

case("an exemption duplicated with different whitespace", "reachability",
     lambda t: append_exemption(t, "\nlens  review-strategy-selector  5: a second and contradictory reason stated for the same lens.\n"),
     expect="is exempted twice")

case("a lens exemption for a lens its Part already blankets", "reachability",
     lambda t: append_exemption(t, "\nlens review-strategy-selector 44: this lens already sits inside the Part E blanket.\n"),
     expect="already blanketed by")

case("a covers range that runs backwards", "reachability",
     lambda t: edit(t, "scripts/routing-exemptions.txt", "covers 37-41", "covers 41-37"),
     expect="reversed, unbounded, or not numeric")

case("a lens heading numbered with a leading zero", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/catalog.md", "### 27.", "### 07."),
     expect="looks like a lens heading")

case("an exemption whose reason is a token, not a reason", "reachability",
     lambda t: replace_line(t, "scripts/routing-exemptions.txt",
                            "lens review-strategy-selector 5:",
                            "lens review-strategy-selector 5: xxx yyy.\n"))

case("a pattern bullet whose number sits outside the bold", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/catalog.md",
                    "- **7. Close with fresh eyes:**", "- 7. **Close with fresh eyes:**"),
     expect="does not match '- **N. Title:**'")

case("a composition appendix heading that appears twice", "reachability",
     lambda t: edit(t, f"{SK}/planning-strategy-selector/catalog.md",
                    "- **5. Slice along the sequence:**",
                    "## Appendix: Composition Patterns\n\n- **5. Slice along the sequence:**"),
     expect="appears more than once")

case("a composition appendix whose stated count is wrong", "reachability",
     lambda t: edit(t, f"{SK}/verification-strategy-selector/catalog.md",
                    "This appendix contains 8 composition patterns",
                    "This appendix contains 9 composition patterns"),
     expect="claims 9 patterns and carries 8")

case("a pattern citation that resolves to no pattern", "reachability",
     lambda t: edit(t, f"{SK}/deliberate-engineering-overrides/SKILL.md",
                    "review pattern #7", "review pattern #77"),
     expect="which is not a pattern in that catalog")

case("a pattern bullet the appendix parser cannot recognise", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/catalog.md",
                    "- **7. Close with fresh eyes:**", "- **7. Close with fresh eyes.**"),
     expect="does not match '- **N. Title:**'")

case("two composition patterns sharing one number", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/catalog.md",
                    "- **7. Close with fresh eyes:**", "- **6. Close with fresh eyes:**"),
     expect="is used twice")

case("a compose step whose catalog has no appendix to cite", "reachability",
     lambda t: edit(t, f"{SK}/planning-strategy-selector/catalog.md",
                    "## Appendix: Composition Patterns", "## Appendix: Ways to combine these"),
     expect="has no '## Appendix: Composition Patterns'")

case("an appendix whose patterns carry no numbers at all", "reachability",
     lambda t: replace_all_lines(t, f"{SK}/debug-operate-strategy-selector/catalog.md",
                                 r"^- \*\*(\d+)\. ", "- **"),
     expect="carry no numbers")

case("a composition pattern the compose step never cites", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md",
                    "**5** discovery before remediation, ", ""),
     expect="composition pattern 5 is cited nowhere")

case("a composition appendix whose patterns lost their numbers", "reachability",
     lambda t: edit(t, f"{SK}/planning-strategy-selector/catalog.md",
                    "- **1. Calibrate first:**", "- **Calibrate first:**"),
     expect="numbered [2, 3, 4, 5, 6, 7], not 1..N")

case("a compose step renamed so its patterns lose their home", "reachability",
     lambda t: edit(t, f"{SK}/debug-operate-strategy-selector/SKILL.md",
                    "## Step 4: Compose the response", "## Step 4: Put it together"),
     expect="has no compose step")

case("a lens left routed only by a composition-pattern citation", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md",
                    "in play** \u2192 14 source-of-truth verification",
                    "in play** \u2192 see pattern 14 source-of-truth verification"),
     expect="is cited nowhere in its selector")

case("a lens no step of its selector routes", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md",
                    "in play** \u2192 14 source-of-truth verification",
                    "in play** \u2192 source-of-truth verification"))

case("a lens left routed only by a coincidental numeral", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md",
                    "- **Self-review your own fixes** (4):",
                    "- **Self-review your own fixes**:"))

case("a lens left routed only by another catalog's citation", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md",
                    "22 error-handling adequacy",
                    "error-handling adequacy (verification #22)"))

case("a lens appended to a Part a group exemption blankets", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/catalog.md",
                    "\n## Appendix: Composition Patterns",
                    "\n### 56. A lens that joined the blanket\n\n- **How it works:** it appends.\n"
                    "- **Objective:** to slip in under Part E.\n- **When most valuable:** never.\n"
                    "\n## Appendix: Composition Patterns"),
     expect="joined it since it was written")

case("a blanketed lens routed by number, leaving its pin stale", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/SKILL.md",
                    "- **Frontend / mobile / infra / data / experiments** \u2192",
                    "- **Terraform or CloudFormation** \u2192 43 infrastructure-as-code review.\n"
                    "- **Frontend / mobile / infra / data / experiments** \u2192"),
     expect="no longer needs it")

case("a lens whose title carries no word a citation could name", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/catalog.md",
                    "### 30. Observability review", "### 30. Own the why, not the how"),
     expect="no word distinctive enough")

def duplicate_pinned_block(t, relpath, anchor):
    """Duplicate a pinned block verbatim.

    Verbatim matters: an edited copy also diverges, and the divergence branch would
    satisfy a control aimed at the duplicate branch. That is the wrong-branch defect
    this file has now fixed three times.
    """
    p = os.path.join(t, relpath)
    with open(p, encoding="utf-8") as fh:
        s = fh.read()
    i = s.index(anchor)
    block = s[i:s.index("\n\n", i)]
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(s[:i] + block + "\n\n" + s[i:])


case("a pinned passage carried twice", "identical",
     lambda t: duplicate_pinned_block(t, f"{SK}/review-strategy-selector/SKILL.md",
                                      "**Operator overrides on patterns.** Before composing"),
     expect="carries it more than once")

case("a pinned passage wrapped in a code fence, where it is inert", "identical",
     lambda t: edit(t, f"{SK}/planning-strategy-selector/SKILL.md",
                    "**Operator overrides on patterns.** Before composing",
                    "```text\n\n**Operator overrides on patterns.** Before composing"))

case("the pattern consult diverging in one selector", "identical",
     lambda t: edit(t, f"{SK}/verification-strategy-selector/SKILL.md",
                    "Before composing, consult `deliberate-engineering-overrides` twice over",
                    "Before composing, have a think about"),
     expect="Operator overrides on patterns consult")

case("a lens under a Part heading the guard does not recognize", "reachability",
     lambda t: edit(t, f"{SK}/review-strategy-selector/catalog.md",
                    "\n## Appendix: Composition Patterns",
                    "\n## Part F: Agent-authored change\n\n### 56. Provenance of an agent-written hunk"
                    "\n\n- **How it works:** it does not matter.\n- **Objective:** to inherit Part E.\n"
                    "- **When most valuable:** never.\n\n## Appendix: Composition Patterns"))

case("a group exemption with no reason", "reachability",
     lambda t: append_exemption(t, "\ngroup planning-strategy-selector Part C:\n"))

case("a group exemption that names no covered set", "reachability",
     lambda t: append_exemption(t, "\ngroup planning-strategy-selector Part C: this part is opened whole by the selector and never lens by lens.\n"),
     expect="must open its reason with")

case("a group exemption naming a Part its catalog does not have", "reachability",
     lambda t: append_exemption(t, "\ngroup review-strategy-selector Part Q: covers 1. there is no such part anywhere in this catalog.\n"),
     expect="has no Part Q")

case("a group exemption for a Part whose lenses are all routed", "reachability",
     lambda t: append_exemption(t, "\ngroup planning-strategy-selector Part A: covers 1. all four of these already route by number today.\n"),
     expect="every lens in it is routed")

case("an exemption for a directory that owns no catalog", "reachability",
     lambda t: append_exemption(t, "\nlens deliberate-engineering-router 3: this skill owns no catalog and routes nothing at all.\n"),
     expect="owns no catalog")

case("a lens exemption naming a lens that does not exist", "reachability",
     lambda t: append_exemption(t, "\nlens review-strategy-selector 999: there is no such lens in this catalog at all.\n"),
     expect="has no lens 999")

case("a lens exemption for a lens the selector does route", "reachability",
     lambda t: append_exemption(t, "\nlens review-strategy-selector 25: the selector routes this one already, so the entry is dead.\n"),
     expect="but the selector routes it")

case("an exemption stated twice", "reachability",
     lambda t: append_exemption(t, "\nlens review-strategy-selector 5: a contradictory second reason stated for a lens that already has one.\n"),
     expect="is exempted twice")


def delete_file(t, relpath):
    os.remove(os.path.join(t, relpath))


# Twelve branches that could be deleted with the suite green, measured by disarming each
# fail() in turn. The file's own principle is that a check nobody has seen fail is not a check.

case("a citation naming a catalog whose file is gone", "citations",
     lambda t: delete_file(t, f"{SK}/review-strategy-selector/catalog.md"),
     expect="but that catalog does not exist")

case("a catalog the count harness lists and the tree no longer has", "catalog-coverage",
     lambda t: delete_file(t, f"{SK}/communication-collaboration-selector/catalog.md"),
     expect="which has no catalog.md")

case("a consult exemption line with no colon at all", "consult",
     lambda t: open(os.path.join(t, "scripts", "consult-exemptions.txt"), "a").write(
         "\ndeliberate-engineering-conduct applies lenses and should consult\n"),
     expect="is not '<skill-dir>: <reason>'")

case("a command with no skill invocation line", "commands",
     lambda t: edit(t, f"{CM}/plan.md", "Invoke the `planning-strategy-selector` skill",
                    "Use the planning selector"),
     expect="has no 'Invoke the `<skill>` skill' line")

case("a command invoking a skill that does not exist", "commands",
     lambda t: edit(t, f"{CM}/plan.md", "Invoke the `planning-strategy-selector` skill",
                    "Invoke the `planning-strategy-chooser` skill"),
     expect="which is not a skill directory")

case("two commands invoking the same skill", "commands",
     lambda t: edit(t, f"{CM}/plan.md", "Invoke the `planning-strategy-selector` skill",
                    "Invoke the `review-strategy-selector` skill"),
     expect="both invoke")

case("the README dropping the command count this check pins", "commands",
     lambda t: edit(t, "README.md", "plus twelve commands", "plus a dozen commands"),
     expect="no longer states a command count")

case("a README command count no reader can turn into a number", "commands",
     lambda t: edit(t, "README.md", "plus twelve commands", "plus umpteen commands"),
     expect="cannot read as a number")

case("an unresolved conflict marker left in a shipped file", "artifacts",
     lambda t: edit(t, "README.md", "plus twelve commands",
                    "plus twelve commands\n\n<<<<<<< HEAD\n"),
     expect="looks like an unresolved conflict marker")

case("a routing exemption line with no colon at all", "reachability",
     lambda t: append_exemption(t, "\nlens review-strategy-selector 9 no colon anywhere in this line\n"),
     expect="is not '<kind> <dir> <target>: <reason>'")

case("an exemption that is neither a group nor a lens", "reachability",
     lambda t: append_exemption(t, "\nbanana review-strategy-selector 9: a kind that does not exist at all.\n"),
     expect="is neither a group nor a lens exemption")

case("a composition appendix that states no count", "reachability",
     # anchored on the sentence shape, not on the number, so adding a pattern does not stale it
     lambda t: replace_all_lines(t, f"{SK}/review-strategy-selector/catalog.md",
                                 r"This appendix contains \d+ composition patterns\. ", ""),
     expect="states no count")


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

        for name, mutate in ACCEPTS:
            tree = fresh_tree(stack)
            try:
                mutate(tree)
            except AssertionError as e:
                print(f"  FAIL: {name} -> this control could not set itself up: {e}")
                print(f"        Update its anchor in scripts/test-check-invariants.py.")
                failures.append(name)
                continue
            r = run_guard(tree)
            if r.returncode == 0:
                print(f"  ok: {name} -> accepted, as it must be")
            else:
                print(f"  FAIL: {name} -> the guard rejected a documented routing form")
                failures.append(name)

        for name, check, mutate, needs_git, expect in CASES:
            tree = fresh_tree(stack)
            base = None
            if needs_git:
                git_snapshot(tree)
                base = "HEAD"
            try:
                mutate(tree)
            except AssertionError as e:
                print(f"  FAIL: {name} -> this control could not set itself up: {e}")
                print(f"        A control anchors on literal text in the repository. If you changed "
                      f"that text deliberately, update this control's anchor in "
                      f"scripts/test-check-invariants.py; the control, not your change, is what is "
                      f"stale.")
                failures.append(name)
                continue
            r = run_guard(tree, base=base)
            caught = r.returncode != 0 and re.search(rf"FAIL \[{re.escape(check)}\]", r.stdout)
            right_branch = expect is None or expect in r.stdout
            if caught and right_branch:
                print(f"  ok: {name} -> caught by [{check}]")
            elif caught:
                print(f"  FAIL: {name} -> caught by [{check}] but on the wrong branch "
                      f"(expected {expect!r})")
                failures.append(name)
            else:
                print(f"  FAIL: {name} -> NOT caught (expected [{check}])")
                failures.append(name)
    finally:
        for t in stack:
            shutil.rmtree(t, ignore_errors=True)

    print()
    if failures:
        print(f"Controls FAILED: {len(failures)}: {failures}")
        print("A control fails either because the guard missed its mutation, or because the control "
              "could not set itself up against the current repository text. The lines above say "
              "which.")
        return 1
    print(f"Controls OK: {len(CASES)} mutations each caught by its own check, "
          f"{len(ACCEPTS)} documented routing forms each accepted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
