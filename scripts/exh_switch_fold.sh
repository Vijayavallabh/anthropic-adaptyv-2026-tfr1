#!/bin/bash
# Exhaustive switch-fold search for g7_8/g6_7: fold all 52 His-combos (DIFF=5 replicate) -> switch_prob,
# to find a combo with a ROBUST 2-His switch (frac>=2 high) that the greedy pick missed. Usage: [gpus]
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
OUT=runs/f21/exh
G="${1:-5 6 7}"
(head -1 $OUT/rfd4_g7_tfr1_apical_xreact_mini_8_combos.csv; tail -n+2 -q $OUT/*_combos.csv) > $OUT/all_combos.csv
echo "[exh] $(($(wc -l < $OUT/all_combos.csv)-1)) combos"
$PY scripts/prep_boltz_pocket.py --seqs $OUT/all_combos.csv --out $OUT/by_h --force --no-controls
DIFF_SAMPLES=5 bash scripts/run_boltz.sh $OUT/by_h $OUT/sw5 "$G" > $OUT/sw5.log 2>&1
$PY scripts/switch_prob.py $OUT/sw5 > $OUT/switch_prob.tsv 2>$OUT/sp.log || true
echo "F21_EXH_SWITCH_DONE $(date -u +%FT%TZ)"
echo "=== switch combos sorted by frac>=2 (col4), then mean (col3) ==="
(head -1 $OUT/switch_prob.tsv; tail -n+2 $OUT/switch_prob.tsv | sort -k4,4 -rn -k3,3) | head -16