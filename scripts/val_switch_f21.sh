#!/bin/bash
# f21: validate the switch-installed new crowns (g7_8, g6_7) — did binding + x-react survive His install,
# and is the switch robust? Pocket-restrained, dual-folder human+mouse (DIFF=1 binding), DIFF=5 switch_prob.
# Single free GPU (0). Calibration inherited from f19 (same targets/method): POS human-Boltz~0.57, mouse~0.0.
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
OUT=runs/f21/val; mkdir -p "$OUT"
SW=runs/f21/sw/switched.csv
G="${1:-0}"
$PY scripts/prep_boltz_pocket.py --seqs "$SW" --out "$OUT/by_h" --force --no-controls
$PY scripts/prep_boltz_pocket.py --seqs "$SW" --target data/targets/mouse_apical_189_383.seq --out "$OUT/bm_h" --force --no-controls
echo "[f21val] yamls h=$(ls $OUT/by_h/*.yaml 2>/dev/null|wc -l) m=$(ls $OUT/bm_h/*.yaml 2>/dev/null|wc -l) $(date -u +%FT%TZ)"
# binding + x-react (DIFF=1, msa server as in f19)
bash scripts/run_boltz.sh "$OUT/by_h" "$OUT/boltz_h" "$G" > "$OUT/bh.log" 2>&1
bash scripts/run_boltz.sh "$OUT/bm_h" "$OUT/boltz_m" "$G" > "$OUT/bm.log" 2>&1
CONSTRAINTS=runs/f12/pocket/apical_restraint.csv       bash scripts/run_chai.sh "$SW" data/targets/apical_domain_189_383.seq "$OUT/chai_h" "$G" 0 5 > "$OUT/ch.log" 2>&1
CONSTRAINTS=runs/f12/pocket/apical_restraint_mouse.csv bash scripts/run_chai.sh "$SW" data/targets/mouse_apical_189_383.seq "$OUT/chai_m" "$G" 0 5 > "$OUT/cm.log" 2>&1
# switch robustness (DIFF=5 replicate human)
DIFF_SAMPLES=5 bash scripts/run_boltz.sh "$OUT/by_h" "$OUT/sw5" "$G" > "$OUT/sw5.log" 2>&1
# score
$PY scripts/score_ipsae.py "$OUT/boltz_h" boltz_h > "$OUT/boltz_h.ip.log" 2>&1 || true
$PY scripts/score_ipsae.py "$OUT/boltz_m" boltz_m > "$OUT/boltz_m.ip.log" 2>&1 || true
$PY scripts/score_ipsae.py "$OUT/chai_h"  chai_h  > "$OUT/chai_h.ip.log"  2>&1 || true
$PY scripts/score_ipsae.py "$OUT/chai_m"  chai_m  > "$OUT/chai_m.ip.log"  2>&1 || true
$PY scripts/switch_prob.py "$OUT/sw5" > "$OUT/switch_prob.tsv" 2>"$OUT/sw_prob.log" || true
echo "F21_VAL_DONE $(date -u +%FT%TZ)"
echo "=== switch_prob ==="; cat "$OUT/switch_prob.tsv" 2>/dev/null
for d in boltz_h boltz_m chai_h chai_m; do echo "=== $d ==="; cat "$OUT/$d/ipsae.tsv" 2>/dev/null; done