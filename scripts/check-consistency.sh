#!/usr/bin/env bash
# Consistency harness for the deliberate-engineering plugin.
#
# The catalogs are the single source of truth for lens counts and numbers.
# Every count claim stated elsewhere (a catalog's own intro, the README's
# "What's inside" block, the architecture doc) must agree with what the
# catalog files actually contain — and no lens number may appear twice.
#
# This guards the class of drift that shipped once already: a lens was added
# to a catalog append-only, but a routing table and a doc count went stale.
# It only fails loudly when a claim and the source of truth disagree — no
# judgment, no false positives. Run it locally before pushing, or in CI.
#
# Exit 0 = all invariants hold; exit 1 = at least one drift found.

set -euo pipefail

# Resolve repo root from this script's location, so it runs from anywhere.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS="$ROOT/plugins/deliberate-engineering/skills"
README="$ROOT/README.md"
ARCH="$ROOT/docs/architecture-and-usage.md"

fails=0
fail() { echo "::error::$*" >&2; echo "  FAIL: $*"; fails=$((fails + 1)); }
ok()   { echo "  ok: $*"; }

# Normalize a count token to a bare integer: digits pass through; the number
# words that actually appear in these docs are mapped. Unknown token -> empty.
to_int() {
  case "$1" in
    ''|*[!0-9]*)
      case "$1" in
        one) echo 1;; two) echo 2;; three) echo 3;; four) echo 4;;
        five) echo 5;; six) echo 6;; seven) echo 7;; eight) echo 8;;
        nine) echo 9;; ten) echo 10;; eleven) echo 11;; twelve) echo 12;;
        *) echo "";;
      esac ;;
    *) echo "$1";;
  esac
}

# catalog file -> actual number of "### N." lens headings
lens_count() { grep -cE '^### [0-9]+\.' "$1"; }

declare -A CATALOG=(
  [review]="$SKILLS/review-strategy-selector/catalog.md"
  [verification]="$SKILLS/verification-strategy-selector/catalog.md"
  [planning]="$SKILLS/planning-strategy-selector/catalog.md"
  [debug-operate]="$SKILLS/debug-operate-strategy-selector/catalog.md"
  [communication]="$SKILLS/communication-collaboration-selector/catalog.md"
)

echo "== Check 1 — each catalog's intro count matches its actual lens count =="
for name in "${!CATALOG[@]}"; do
  f="${CATALOG[$name]}"
  actual=$(lens_count "$f")
  # intro form: "This catalog contains <N> ..." where <N> is a digit or a word
  claim_tok=$(grep -oiE 'contains [0-9a-z]+' "$f" | head -1 | awk '{print $2}')
  claim=$(to_int "$claim_tok")
  if [ -z "$claim" ]; then
    fail "$name catalog: could not parse an intro count claim ('contains …')"
  elif [ "$claim" != "$actual" ]; then
    fail "$name catalog: intro says $claim lenses but the file has $actual"
  else
    ok "$name: intro $claim == actual $actual"
  fi
done

echo "== Check 2 — no duplicate lens numbers within a catalog =="
for name in "${!CATALOG[@]}"; do
  f="${CATALOG[$name]}"
  dups=$(grep -oE '^### [0-9]+\.' "$f" | grep -oE '[0-9]+' | sort -n | uniq -d || true)
  if [ -n "$dups" ]; then
    fail "$name catalog: duplicate lens number(s): $(echo "$dups" | tr '\n' ' ')"
  else
    ok "$name: all lens numbers unique"
  fi
done

r=$(lens_count "${CATALOG[review]}")
v=$(lens_count "${CATALOG[verification]}")
p=$(lens_count "${CATALOG[planning]}")
d=$(lens_count "${CATALOG[debug-operate]}")
c=$(lens_count "${CATALOG[communication]}")
total=$((r + v + p + d))

echo "== Check 3 — README 'What's inside' per-catalog counts match =="
readme_count() { grep -oE "\*\*$1 — [0-9]+ strategies\*\*" "$README" | grep -oE '[0-9]+' | head -1; }
while IFS='|' read -r label actual; do
  claim=$(readme_count "$label")
  if [ -z "$claim" ]; then
    fail "README: no '$label — N strategies' claim found"
  elif [ "$claim" != "$actual" ]; then
    fail "README: '$label' says $claim but catalog has $actual"
  else
    ok "README $label: $claim == $actual"
  fi
done <<EOF
Review|$r
Verification|$v
Planning|$p
Debug/Operate|$d
EOF

echo "== Check 4 — README per-group parentheticals sum to the catalog total =="
# Each "What's inside" bullet lists group sizes in parentheses; they must
# sum to that catalog's total. Extract the bullet line, sum its (N) tokens.
group_sum() {
  grep -E "^\- \*\*$1 — [0-9]+ strategies\*\*" "$README" \
    | grep -oE '\([0-9]+\)' | grep -oE '[0-9]+' | paste -sd+ - | bc
}
while IFS='|' read -r label actual; do
  s=$(group_sum "$label")
  if [ -z "$s" ]; then
    fail "README: could not read group counts for '$label'"
  elif [ "$s" != "$actual" ]; then
    fail "README: '$label' group counts sum to $s but the catalog total is $actual"
  else
    ok "README $label groups: sum $s == $actual"
  fi
done <<EOF
Review|$r
Verification|$v
Planning|$p
Debug/Operate|$d
EOF

echo "== Check 5 — README 'N strategies total' == sum of the four phase catalogs =="
readme_total=$(grep -oE '[0-9]+ strategies total' "$README" | grep -oE '[0-9]+' | head -1)
if [ -z "$readme_total" ]; then
  fail "README: no 'N strategies total' claim found"
elif [ "$readme_total" != "$total" ]; then
  fail "README: says $readme_total strategies total but the catalogs sum to $total"
else
  ok "README total: $readme_total == $total"
fi

echo "== Check 6 — communication lens count agrees across README and the arch doc =="
# README: "the cross-cutting communication catalog adds <word/number> lenses"
readme_comm_tok=$(grep -oiE 'communication catalog adds [0-9a-z]+ lenses' "$README" | awk '{print $(NF-1)}')
readme_comm=$(to_int "$readme_comm_tok")
if [ -z "$readme_comm" ]; then
  fail "README: could not parse the communication lens count"
elif [ "$readme_comm" != "$c" ]; then
  fail "README: communication catalog stated as $readme_comm lenses but it has $c"
else
  ok "README communication: $readme_comm == $c"
fi

# Arch doc: "applies its <word/number> lenses" (the communication selector)
arch_comm_tok=$(grep -oiE 'applies its [0-9a-z]+ lenses' "$ARCH" | awk '{print $3}')
arch_comm=$(to_int "$arch_comm_tok")
if [ -z "$arch_comm" ]; then
  fail "arch doc: could not parse the 'applies its N lenses' count"
elif [ "$arch_comm" != "$c" ]; then
  fail "arch doc: communication stated as $arch_comm lenses but the catalog has $c"
else
  ok "arch doc communication: $arch_comm == $c"
fi

echo "== Check 7 — the standing-rule count agrees everywhere it is claimed =="
RULES="$SKILLS/deliberate-engineering-rules/SKILL.md"
rules_actual=$(grep -cE '^## Rule [0-9]+ ' "$RULES")

# Each claim site states the count in words; compare every one to the number of
# "## Rule N" headings the skill actually defines. Same drift class as the lens
# counts above — a rule was added but a prose count or an enumeration went stale.
check_rule_claim() { # <file> <label> <case-insensitive regex> <awk field holding the count token>
  local tok n
  tok=$(grep -oiE "$3" "$1" | head -1 | awk "{print \$$4}" || true)
  n=$(to_int "$tok")
  if [ -z "$n" ]; then
    fail "$2: could not parse a standing-rule count claim"
  elif [ "$n" != "$rules_actual" ]; then
    fail "$2: says $n standing rules but the skill defines $rules_actual"
  else
    ok "$2: $n == $rules_actual"
  fi
}

check_rule_claim "$RULES"  "rules skill sharpened-core line" 'these [0-9a-z]+ are the sharpened core' 2
check_rule_claim "$README" "README what's-inside"            '[0-9a-z]+ standing rules held across'   1
check_rule_claim "$README" "README always-on core"           'the [0-9a-z]+ rules are the small'      2
check_rule_claim "$ARCH"   "arch doc"                        'the [0-9a-z]+ standing rules hold'      2

rule_dups=$(grep -oE '^## Rule [0-9]+ ' "$RULES" | grep -oE '[0-9]+' | sort -n | uniq -d || true)
if [ -n "$rule_dups" ]; then
  fail "rules skill: duplicate rule number(s): $(echo "$rule_dups" | tr '\n' ' ')"
else
  ok "rules skill: all rule numbers unique"
fi

echo
if [ "$fails" -ne 0 ]; then
  echo "Consistency check FAILED — $fails drift(s) found."
  exit 1
fi
echo "Consistency check OK — review=$r verification=$v planning=$p debug=$d communication=$c (total=$total)."
