#!/bin/bash
# f15 clean re-validation: does des_25_sw2b_A9_A25 (2-His cross-reactive) dual-confirm?
# Human + mouse, Boltz + Chai, pocket-restrained, 5 samples / 3 seeds. Calibrated by POS_3DS18 + NEG(seed37).
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
OUT=runs/f15; H=$OUT/reval_human.csv; M=$OUT/reval_mouse.csv
# Append identical controls to both CSVs (POS + NEG seed37 == all prior runs -> comparable calibration)
"$PY" - "$H" "$M" <<'PYEOF'
import sys, random
POS="DEREEEQRRRLEEVKEEAKRRERSEQDLAVLYLEAVNAAVVFVADSEEEAKRVADIVKKLVPEVIIFVHDNFVVFVVDSDEAARRVYEIVERA"
rng=random.Random(37); negs=[]
for i in (1,2):
    s=list(POS); rng.shuffle(s); negs.append("".join(s))
ctl=f"POS_3DS18,{POS}\nNEG_scramble1,{negs[0]}\nNEG_scramble2,{negs[1]}\n"
for f in sys.argv[1:]:
    if "POS_3DS18" not in open(f).read(): open(f,"a").write(ctl)
print("controls appended")
PYEOF
# Boltz pocket YAMLs (single-seq, force), controls already in CSV -> --no-controls
"$PY" scripts/prep_boltz_pocket.py --seqs "$H" --out $OUT/by_h --force --no-controls
"$PY" scripts/prep_boltz_pocket.py --seqs "$M" --target data/targets/mouse_apical_189_383.seq --out $OUT/bm_h --force --no-controls
echo "[reval] YAMLs h=$(ls $OUT/by_h/*.yaml|wc -l) m=$(ls $OUT/bm_h/*.yaml|wc -l) $(date -u +%FT%TZ)"
# 4 folds, 2 GPUs each, all concurrent
DIFF_SAMPLES=5 NOMSA=1 bash scripts/run_boltz.sh $OUT/by_h $OUT/boltz_h "0 1" > $OUT/boltz_h.log 2>&1 & P1=$!
DIFF_SAMPLES=5 NOMSA=1 bash scripts/run_boltz.sh $OUT/bm_h $OUT/boltz_m "2 3" > $OUT/boltz_m.log 2>&1 & P2=$!
CONSTRAINTS=runs/f12/pocket/apical_restraint.csv       bash scripts/run_chai.sh "$H" data/targets/apical_domain_189_383.seq $OUT/chai_h "4 5" 0,1,2 5 > $OUT/chai_h.log 2>&1 & P3=$!
CONSTRAINTS=runs/f12/pocket/apical_restraint_mouse.csv bash scripts/run_chai.sh "$M" data/targets/mouse_apical_189_383.seq $OUT/chai_m "6 7" 0,1,2 5 > $OUT/chai_m.log 2>&1 & P4=$!
wait $P1 $P2 $P3 $P4
echo "REVAL_DONE $(date -u +%FT%TZ) jsons: boltz_h=$(find $OUT/boltz_h -name 'confidence*json'|wc -l) boltz_m=$(find $OUT/boltz_m -name 'confidence*json'|wc -l) chai_h=$(find $OUT/chai_h -name 'confidence*json'|wc -l) chai_m=$(find $OUT/chai_m -name 'confidence*json'|wc -l)"
