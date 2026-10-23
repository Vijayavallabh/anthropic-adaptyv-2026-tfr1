#!/bin/bash
# Chai-1 single-seq cofold (architecturally INDEPENDENT of Boltz/BoltzGen) sharded across GPUs.
# binder=A : receptor=B. Writes Boltz-compatible confidence/pae (parse_boltz.py reads it).
# Usage: run_chai.sh <designs.csv name,sequence> <receptor.seq> <out_root> "<gpus>" [seeds] [samples]
set -uo pipefail
CHAIPY=/home/prachh/v/sepiq-2026-challenge/.venv-chai/bin/python
REPO="$(cd "$(dirname "$0")/.." && pwd)"
CSV=${1:?csv}; REC=${2:?receptor.seq}; OUT=${3:?out}; GPUS=${4:-1 2 3 4 5 6 7}; SEEDS=${5:-0}; SAMPLES=${6:-5}
read -r -a G <<< "$GPUS"; NG=${#G[@]}
mkdir -p "$OUT"
"$CHAIPY" - "$CSV" "$OUT" "$NG" <<'PY'
import sys, csv, os
csvf, out, ng = sys.argv[1], sys.argv[2], int(sys.argv[3])
rows = list(csv.DictReader(open(csvf)))
for i in range(ng):
    os.makedirs(f"{out}/sh{i}", exist_ok=True)
    w = csv.writer(open(f"{out}/sh{i}/designs.csv", "w")); w.writerow(["name", "sequence"])
    for r in rows[i::ng]:
        w.writerow([r["name"], r["sequence"]])
print("split", len(rows), "across", ng)
PY
export CHAI_DOWNLOADS_DIR=/home/prachh/v/chai_downloads OMP_NUM_THREADS=8
echo "[chai] receptor=$REC seeds=$SEEDS samples=$SAMPLES gpus=[$GPUS] $(date -u +%FT%TZ)"
pids=()
for i in "${!G[@]}"; do
  g=${G[$i]}; [ -s "$OUT/sh$i/designs.csv" ] || continue
  CUDA_VISIBLE_DEVICES=$g "$CHAIPY" "$REPO/scripts/chai_fold_adapt.py" \
    "$OUT/sh$i/designs.csv" "$REC" "$OUT/sh$i" --seeds "$SEEDS" --samples "$SAMPLES" \
    ${CONSTRAINTS:+--constraints "$CONSTRAINTS"} \
    > "$OUT/sh$i.log" 2>&1 &
  pids+=($!); sleep 8
done
rc=0; for p in "${pids[@]}"; do wait "$p" || rc=1; done
echo "CHAI_DONE rc=$rc confidence jsons: $(find "$OUT" -name 'confidence_*.json' 2>/dev/null | wc -l) $(date -u +%FT%TZ)"
