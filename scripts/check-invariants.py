#!/usr/bin/env python3
"""Structural invariants of the deliberate-engineering plugin.

The sibling script, check-consistency.sh, guards every count the docs state.
This one guards the invariants that are not numbers: that a lens number is a
permanent address, that every citation resolves, that every skill applying a
lens consults the override layer, that prose counts of skills and commands
match what is on disk, that a named section referenced somewhere exists, and
that passages the text claims are identical are identical.

Run from the repository root: python3 scripts/check-invariants.py
Compare against a base revision (append-only numbering needs one):
    python3 scripts/check-invariants.py --base origin/main

Every check here was built with a negative control: the defect it names was
introduced deliberately in a scratch tree and the check was proved to fail
before it was trusted. A check nobody has seen fail is not a check.
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "plugins", "deliberate-engineering")
SKILLS = os.path.join(PLUGIN, "skills")
COMMANDS = os.path.join(PLUGIN, "commands")

failures = []
notes = []


def fail(check, msg):
    failures.append((check, msg))
    print(f"::error::{check}: {msg}")
    print(f"  FAIL [{check}] {msg}")


def ok(msg):
    print(f"  ok: {msg}")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def skill_dirs():
    return sorted(
        d for d in os.listdir(SKILLS) if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md"))
    )


def catalog_paths():
    """Derived from the filesystem, never hardcoded: a sixth catalog must not be invisible."""
    return {
        d: os.path.join(SKILLS, d, "catalog.md")
        for d in skill_dirs()
        if os.path.isfile(os.path.join(SKILLS, d, "catalog.md"))
    }


# Catalog nicknames as they are cited in prose, mapped to their directory.
CITE_NAMES = {
    "review": "review-strategy-selector",
    "verification": "verification-strategy-selector",
    "verify": "verification-strategy-selector",
    "planning": "planning-strategy-selector",
    "debug-operate": "debug-operate-strategy-selector",
    "debug": "debug-operate-strategy-selector",
    "communication": "communication-collaboration-selector",
}
CITE_RE = re.compile(
    r"\b(" + "|".join(sorted(CITE_NAMES, key=len, reverse=True)) + r")\s+#(\d+)"
)
HEADING_RE = re.compile(r"^### (\d+)\.", re.M)
RULE_RE = re.compile(r"\bRule (\d+)\b")


def markdown_files():
    out = []
    for base in (PLUGIN,):
        for dirpath, _dirs, files in os.walk(base):
            for f in files:
                if f.endswith(".md"):
                    out.append(os.path.join(dirpath, f))
    for extra in ("README.md", "CONTRIBUTING.md"):
        p = os.path.join(ROOT, extra)
        if os.path.isfile(p):
            out.append(p)
    docs = os.path.join(ROOT, "docs")
    for dirpath, _dirs, files in os.walk(docs):
        for f in files:
            if f.endswith(".md"):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


def rel(path):
    return os.path.relpath(path, ROOT)


def check_append_only(base):
    """A lens number is a permanent address; overrides cite it. Never renumber."""
    if not base:
        notes.append("append-only numbering: skipped, no --base given")
        print("  skipped: append-only numbering (no --base revision given)")
        return
    try:
        subprocess.run(
            ["git", "rev-parse", "--verify", base], cwd=ROOT,
            check=True, capture_output=True,
        )
    except subprocess.CalledProcessError:
        notes.append(f"append-only numbering: skipped, base {base} not resolvable")
        print(f"  skipped: append-only numbering (base {base} not resolvable here)")
        return
    for name, path in sorted(catalog_paths().items()):
        rp = rel(path)
        try:
            before = subprocess.run(
                ["git", "show", f"{base}:{rp}"], cwd=ROOT,
                check=True, capture_output=True, text=True,
            ).stdout
        except subprocess.CalledProcessError:
            ok(f"append-only {name}: new catalog, nothing to compare")
            continue
        old = set(int(n) for n in HEADING_RE.findall(before))
        new = set(int(n) for n in HEADING_RE.findall(read(path)))
        lost = sorted(old - new)
        if lost:
            fail(
                "append-only",
                f"{name}: lens number(s) {lost} existed at {base} and are gone. "
                "Numbers are permanent addresses that override files cite; append, never renumber.",
            )
        else:
            ok(f"append-only {name}: {len(old)} numbers at base, all still present")


def check_citations():
    """Every '<catalog> #N' and 'Rule N' must resolve to a real heading."""
    cats = catalog_paths()
    numbers = {d: set(int(n) for n in HEADING_RE.findall(read(p))) for d, p in cats.items()}
    rules_path = os.path.join(SKILLS, "deliberate-engineering-rules", "SKILL.md")
    rule_numbers = set(int(m) for m in re.findall(r"^## Rule (\d+):", read(rules_path), re.M))
    bad = 0
    total = 0
    for path in markdown_files():
        for i, line in enumerate(read(path).splitlines(), 1):
            for m in CITE_RE.finditer(line):
                target = CITE_NAMES[m.group(1)]
                n = int(m.group(2))
                total += 1
                if target not in numbers:
                    fail("citations", f"{rel(path)}:{i} cites {m.group(0)} but that catalog does not exist")
                    bad += 1
                elif n not in numbers[target]:
                    fail("citations", f"{rel(path)}:{i} cites {m.group(0)}, which resolves to no heading in {target}")
                    bad += 1
            for m in RULE_RE.finditer(line):
                n = int(m.group(1))
                total += 1
                if n not in rule_numbers:
                    fail("citations", f"{rel(path)}:{i} cites Rule {n}, which is not a standing rule")
                    bad += 1
    if not bad:
        ok(f"citations: {total} lens and rule citations, all resolve")


CONSULT_RE = re.compile(r"consult[^.\n]{0,60}`deliberate-engineering-overrides`", re.I)


def check_consult_presence():
    """Every skill that applies a numbered lens consults the override layer.

    Exemptions live in scripts/consult-exemptions.txt, one 'dir: reason' per
    line, so an exemption is a stated decision rather than a silent skip.
    """
    exempt = {}
    ex_path = os.path.join(ROOT, "scripts", "consult-exemptions.txt")
    if os.path.isfile(ex_path):
        for line in read(ex_path).splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                fail("consult", f"consult-exemptions.txt: '{line}' is not '<skill-dir>: <reason>'")
                continue
            d, reason = line.split(":", 1)
            if not reason.strip():
                fail("consult", f"consult-exemptions.txt: {d.strip()} is exempted with no reason")
            exempt[d.strip()] = reason.strip()
    missing = []
    for d in skill_dirs():
        files = [
            os.path.join(SKILLS, d, f)
            for f in os.listdir(os.path.join(SKILLS, d))
            if f.endswith(".md")
        ]
        # A skill that owns a catalog applies its own lenses, and cites them as bare
        # numbers ("25 functional correctness") rather than as "review #25", so the
        # citation pattern alone would never see the five files where this matters most.
        owns_catalog = os.path.isfile(os.path.join(SKILLS, d, "catalog.md"))
        applies = owns_catalog or any(CITE_RE.search(read(f)) for f in files)
        consults = any(CONSULT_RE.search(read(f)) for f in files)
        if applies and not consults and d != "deliberate-engineering-overrides":
            if d in exempt:
                ok(f"consult: {d} exempted ({exempt[d]})")
            else:
                missing.append(d)
    for d in missing:
        fail(
            "consult",
            f"{d} cites a numbered lens but never consults deliberate-engineering-overrides. "
            "Add the consult, or add it to scripts/consult-exemptions.txt with a reason.",
        )
    stale = sorted(set(exempt) - set(skill_dirs()))
    for d in stale:
        fail("consult", f"consult-exemptions.txt exempts {d}, which is not a skill directory")
    if not missing and not stale:
        ok(f"consult: every lens-applying skill consults the override layer ({len(exempt)} stated exemption(s))")


def check_catalog_coverage():
    """No catalog may be invisible to the count harness.

    check-consistency.sh enumerates catalogs in a hardcoded array, so a sixth
    catalog would be added and never counted. This is the check that mutation
    would have failed.
    """
    harness = os.path.join(ROOT, "scripts", "check-consistency.sh")
    text = read(harness)
    on_disk = set(catalog_paths())
    listed = set()
    for m in re.finditer(r"\[[a-z-]+\]=\"\$SKILLS/([a-z-]+)/catalog\.md\"", text):
        listed.add(m.group(1))
    missing = sorted(on_disk - listed)
    stale = sorted(listed - on_disk)
    for d in missing:
        fail("catalog-coverage",
             f"{d}/catalog.md exists but check-consistency.sh does not count it; "
             "its lens counts are unguarded")
    for d in stale:
        fail("catalog-coverage", f"check-consistency.sh lists {d}, which has no catalog.md")
    if not missing and not stale:
        ok(f"catalog-coverage: all {len(on_disk)} catalogs on disk are counted by the harness")


def check_command_targets():
    """Every command invokes a skill that exists, and no two claim the same one."""
    seen = {}
    bad = 0
    for f in sorted(os.listdir(COMMANDS)):
        if not f.endswith(".md"):
            continue
        text = read(os.path.join(COMMANDS, f))
        m = re.search(r"Invoke the `([^`]+)` skill", text)
        if not m:
            fail("commands", f"commands/{f} has no 'Invoke the `<skill>` skill' line")
            bad += 1
            continue
        target = m.group(1)
        if not os.path.isfile(os.path.join(SKILLS, target, "SKILL.md")):
            fail("commands", f"commands/{f} invokes {target}, which is not a skill directory")
            bad += 1
        if target in seen:
            fail("commands", f"commands/{f} and commands/{seen[target]} both invoke {target}")
            bad += 1
        seen[target] = f
    # The README states the command count in prose. A generic count check cannot
    # tell an inventory claim from a subset claim ("four skills have no command"),
    # so this pins the one claim that is an inventory claim.
    WORDS = {"ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
             "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18}
    readme = read(os.path.join(ROOT, "README.md"))
    m = re.search(r"plus (\w+) commands", readme)
    if not m:
        fail("commands", "README no longer states a command count; this check pinned 'plus <N> commands'")
        bad += 1
    else:
        tok = m.group(1).lower()
        claimed = int(tok) if tok.isdigit() else WORDS.get(tok)
        if claimed is None:
            fail("commands", f"README says 'plus {m.group(1)} commands', which this check cannot read as a number")
            bad += 1
        elif claimed != len(seen):
            fail("commands", f"README says 'plus {m.group(1)} commands' but {len(seen)} exist on disk")
            bad += 1
    if not bad:
        ok(f"commands: {len(seen)} command(s), each invoking a distinct existing skill, matching the README")


SECTION_REF_RE = re.compile(r'(?<!you )see "([^"]{4,80})"')


def check_section_refs():
    """A reference to a named section must resolve to a heading that exists."""
    headings = {}
    for path in markdown_files():
        headings[path] = set(
            h.strip().strip("*`") for h in re.findall(r"^#{2,4} (.+)$", read(path), re.M)
        )
    all_headings = set()
    for hs in headings.values():
        all_headings |= hs
    bad = 0
    checked = 0
    for path in markdown_files():
        for i, line in enumerate(read(path).splitlines(), 1):
            for m in SECTION_REF_RE.finditer(line):
                name = m.group(1).strip()
                checked += 1
                here = any(name in h for h in headings[path])
                anywhere = any(name in h for h in all_headings)
                if not here and not anywhere:
                    fail(
                        "section-refs",
                        f'{rel(path)}:{i} points at a section "{name}" that exists in no file',
                    )
                    bad += 1
    if not bad:
        ok(f"section-refs: {checked} named-section reference(s), all resolve")


IDENTICAL_BLOCKS = [
    (
        "Operator overrides consult",
        "**Operator overrides.** Before applying the selected lenses",
        [
            "planning-strategy-selector", "review-strategy-selector",
            "verification-strategy-selector", "debug-operate-strategy-selector",
            "communication-collaboration-selector",
        ],
    ),
    (
        "direct-entry paragraph",
        "**Entering here directly.** These lenses are the same whether you arrived",
        [
            "planning-strategy-selector", "review-strategy-selector",
            "verification-strategy-selector", "debug-operate-strategy-selector",
        ],
    ),
]


def check_identical_blocks():
    """Where the plugin claims a passage is identical across files, prove it."""
    for label, anchor, dirs in IDENTICAL_BLOCKS:
        seen = {}
        for d in dirs:
            path = os.path.join(SKILLS, d, "SKILL.md")
            text = read(path)
            idx = text.find(anchor)
            if idx < 0:
                fail("identical", f"{label}: {d} does not carry it at all")
                continue
            end = text.find("\n\n", idx)
            block = text[idx:end if end > 0 else len(text)]
            seen.setdefault(hashlib.md5(block.encode()).hexdigest(), []).append(d)
        if len(seen) > 1:
            groups = " | ".join(f"{','.join(v)}" for v in seen.values())
            fail("identical", f"{label}: diverged into {len(seen)} versions across {groups}")
        elif seen:
            ok(f"identical: {label} is byte-identical across {len(dirs)} files")


DOUBLED_RE = re.compile(r"\b(\w+)\s+\1\b", re.I)
DOUBLED_OK = {"had had", "that that"}


def check_text_artifacts():
    """Doubled words and unresolved conflict markers."""
    bad = 0
    for path in markdown_files():
        for i, line in enumerate(read(path).splitlines(), 1):
            if line.startswith(("<<<<<<<", ">>>>>>>")) or line.rstrip() == "=======":
                fail("artifacts", f"{rel(path)}:{i} looks like an unresolved conflict marker")
                bad += 1
            if re.match(r"^\s*class\s+[\w,]+\s+\w+;?\s*$", line):
                continue
            for m in DOUBLED_RE.finditer(line):
                if m.group(0).lower() in DOUBLED_OK or len(m.group(1)) < 3:
                    continue
                fail("artifacts", f"{rel(path)}:{i} doubled word: '{m.group(0)}'")
                bad += 1
    if not bad:
        ok("artifacts: no doubled words, no conflict markers")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=os.environ.get("INVARIANTS_BASE", ""),
                    help="revision to compare append-only numbering against")
    args = ap.parse_args()
    print("== Invariant 1: lens numbers are permanent addresses ==")
    check_append_only(args.base)
    print("== Invariant 2: every lens and rule citation resolves ==")
    check_citations()
    print("== Invariant 3: every lens-applying skill consults the override layer ==")
    check_consult_presence()
    print("== Invariant 4: no catalog or command is invisible ==")
    check_catalog_coverage()
    check_command_targets()
    print("== Invariant 5: named-section references resolve ==")
    check_section_refs()
    print("== Invariant 6: passages claimed identical are identical ==")
    check_identical_blocks()
    print("== Invariant 7: no doubled words or conflict markers ==")
    check_text_artifacts()
    print()
    for n in notes:
        print(f"  note: {n}")
    if failures:
        print(f"\nInvariant check FAILED: {len(failures)} problem(s).")
        return 1
    print("\nInvariant check OK: all seven invariants hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
