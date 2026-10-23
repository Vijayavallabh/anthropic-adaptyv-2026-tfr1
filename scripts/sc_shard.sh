#!/bin/bash
# Shard self_consistency.py (ESMFold + TMalign self-consistency + foldseek novelty) across GPUs.
# Each shard gets its OWN struct-dir (self_consistency uses struct-dir/fs_tmp -> no concurrent collision).
# Usage: sc_shard.sh <seqs.csv name,sequence> <backbone_dir> <out_root> "<gpus>"
set -uo pipefail
ESMPY=/home/prachh/v/.venv-esmfold2/bin/python
REPO="$(cd "$(dirname "$0")/.." && pwd)"
CSV=${1:?seqs.csv}; BB=${2:?backbone_dir}; OUT=${3:?out_root}; GPUS=${4:-1 2 3 4 5 6 7}
read -r -a G <<< "$GPUS"; NG=${#G[@]}
mkdir -p "$OUT"
"$ESMPY" - "$CSV" "$OUT" "$NG" <<'PY'
import sys, csv, os
csvf, out, ng = sys.argv[1], sys.argv[2], int(sys.argv[3])
rows = list(csv.DictReader(open(csvf)))
for i in range(ng):
    os.makedirs(f"{out}/sh{i}", exist_ok=True)
    w = csv.writer(open(f"{out}/sh{i}/seqs.csv", "w")); w.writerow(["name", "sequence"])
    for r in rows[i::ng]:
        w.writerow([r["name"], r["sequence"]])
print("split", len(rows), "across", ng)
PY
echo "[sc] backbones=$BB gpus=[$GPUS] $(date -u +%FT%TZ)"
pids=()
for i in "${!G[@]}"; do
  g=${G[$i]}; [ -s "$OUT/sh$i/seqs.csv" ] || continue
  CUDA_VISIBLE_DEVICES=$g OMP_NUM_THREADS=8 "$ESMPY" "$REPO/scripts/self_consistency.py" \
    --seqs "$OUT/sh$i/seqs.csv" --backbones "$BB" --out "$OUT/sh$i.csv" --struct-dir "$OUT/sh$i/esm" \
    > "$OUT/sh$i.log" 2>&1 &
  pids+=($!); sleep 5
done
rc=0; for p in "${pids[@]}"; do wait "$p" || rc=1; done
cat "$OUT"/sh*.csv 2>/dev/null | awk 'NR==1 || !/^name,/' > "$OUT/all.csv"
echo "SC_DONE rc=$rc rows=$(( $(wc -l < "$OUT/all.csv") - 1 )) kept(sc&novel)=$(awk -F, 'NR>1 && $5==1 && $6==1' "$OUT/all.csv" | wc -l) -> $OUT/all.csv $(date -u +%FT%TZ)"
