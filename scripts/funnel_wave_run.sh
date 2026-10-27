#!/bin/bash
# Genie3 wave funnel stages 1-4 (chains proven scripts): MPNN -> ESMFold self-consistency+novelty ->
# join sc&novel survivors to sequences -> human pocket-restrained Boltz screen (calibrated POS/NEG).
# STOPS at the ranked human-binder list (runs/<out>/binders.csv) -- the checkpoint BEFORE the expensive
# 4-fold crown screen (crown_val.sh). Reuses: funnel_wave_mpnn.sh, sc_shard.sh, screen_human.sh.
# Usage: funnel_wave_run.sh <wave_tag> <wlabel> <out_dir> [gpus] [cap=400]
#   e.g. funnel_wave_run.sh genie3_apical3 w3 runs/f28 "0 1 2 3 4 5 6 7" 400
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
WAVE=${1:?wave_tag}; WL=${2:?wlabel}; OUT=${3:?out_dir}; GPUS="${4:-0 1 2 3 4 5 6 7}"; CAP="${5:-400}"
G0=$(echo "$GPUS" | awk '{print $1}')
mkdir -p "$OUT"

echo "### STAGE1 MPNN $(date -u +%FT%TZ)"
bash scripts/funnel_wave_mpnn.sh "$WAVE" "$WL" "$OUT" "$G0" 2
[ -s "$OUT/mpnn.csv" ] || { echo "STAGE1 FAIL: no mpnn.csv"; exit 1; }

echo "### STAGE2 ESMFold self-consistency + novelty (sharded) $(date -u +%FT%TZ)"
bash scripts/sc_shard.sh "$OUT/mpnn.csv" "$OUT/bb" "$OUT/sc" "$GPUS"
[ -s "$OUT/sc/all.csv" ] || { echo "STAGE2 FAIL: no sc/all.csv"; exit 1; }

echo "### STAGE3 filter sc&novel + rejoin sequences $(date -u +%FT%TZ)"
"$PY" - "$OUT" <<'PY'
import csv, sys
OUT=sys.argv[1]
seq={r['name']:r['sequence'] for r in csv.DictReader(open(f'{OUT}/mpnn.csv'))}
keep=[]
for r in csv.DictReader(open(f'{OUT}/sc/all.csv')):
    if r.get('self_consistent')=='1' and r.get('novel')=='1' and r['name'] in seq:
        keep.append((r['name'], seq[r['name']], float(r['novelty_covwTM'])))
keep.sort(key=lambda x:x[2])  # most novel first
w=csv.writer(open(f'{OUT}/screenset.csv','w')); w.writerow(['name','sequence'])
for n,s,_ in keep: w.writerow([n,s])
print(f'[stage3] sc&novel survivors -> {len(keep)} -> {OUT}/screenset.csv')
PY
[ -s "$OUT/screenset.csv" ] || { echo "STAGE3 FAIL: no screenset.csv"; exit 1; }

echo "### STAGE4 human pocket-restrained Boltz screen (calibrated) $(date -u +%FT%TZ)"
bash scripts/screen_human.sh "$OUT/screenset.csv" "$OUT/screen" "$GPUS"
[ -s "$OUT/screen/scores.tsv" ] || { echo "STAGE4 FAIL: no scores.tsv"; exit 1; }

echo "### SELECT human binders (ab_iptm > NEG ceiling), cap $CAP $(date -u +%FT%TZ)"
"$PY" - "$OUT" "$CAP" <<'PY'
import csv, sys
OUT, CAP = sys.argv[1], int(sys.argv[2])
rows=list(csv.DictReader(open(f'{OUT}/screen/scores.tsv'), delimiter='\t'))
d={r['name']:float(r['ab_iptm']) for r in rows}
seq={r['name']:r['sequence'] for r in csv.DictReader(open(f'{OUT}/screenset.csv'))}
neg=[d[n] for n in d if n.startswith('NEG_scramble')]
pos=d.get('POS_3DS18')
negmax=max(neg) if neg else 0.0
cands=sorted([(n,v) for n,v in d.items() if not n.startswith(('NEG_scramble','POS_3DS18')) and v>negmax and n in seq],
             key=lambda x:-x[1])[:CAP]
w=csv.writer(open(f'{OUT}/binders.csv','w')); w.writerow(['name','sequence'])
for n,_ in cands: w.writerow([n,seq[n]])
print(f'[select] POS_3DS18={pos}  NEGmax={negmax:.3f}  binders(>NEG, cap {CAP})={len(cands)} -> {OUT}/binders.csv')
print(f'[select] top: '+', '.join(f"{n}={v:.2f}" for n,v in cands[:8]))
PY
echo "FUNNEL_WAVE_RUN_DONE $(date -u +%FT%TZ)  (next: crown_val.sh $OUT/binders.csv $OUT/crown \"3 5 6 7\")"
