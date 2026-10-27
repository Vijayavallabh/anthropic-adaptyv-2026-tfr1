#!/usr/bin/env bash
# Sharded BLIND-Protenix co-fold (organizers' outside judge) of every design in a CSV:
# human on GPU 0-3, mouse on GPU 4-7, ~5 designs/GPU, heavy inference-time sampling.
# Usage: SAMPLES=40 SEEDS=101,102 run_protenix_tfr1.sh [designs.csv] [out_dir]
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
CSV=${1:-submissions/tfr1_track2_v15.csv}
OUT=${2:-runs/prot/v15}
SAMPLES=${SAMPLES:-40}
SEEDS=${SEEDS:-101,102}
mapfile -t NAMES < <(tail -n +2 "$CSV" | cut -d, -f1)
N=${#NAMES[@]}
echo "sharding $N designs across 8 GPUs (human 0-3 / mouse 4-7) samples=$SAMPLES seeds=$SEEDS -> $OUT"
declare -a SH=( "" "" "" "" )
for i in "${!NAMES[@]}"; do s=$(( i % 4 )); SH[$s]="${SH[$s]:+${SH[$s]},}${NAMES[$i]}"; done
pids=()
for s in 0 1 2 3; do
  [ -z "${SH[$s]}" ] && continue
  python3 scripts/fold_protenix_tfr1.py --seqs "$CSV" --names "${SH[$s]}" --species human --gpu "$s" \
    --samples "$SAMPLES" --seeds "$SEEDS" --out "$OUT/human" > "runs/prot_h_$s.log" 2>&1 & pids+=($!)
  python3 scripts/fold_protenix_tfr1.py --seqs "$CSV" --names "${SH[$s]}" --species mouse --gpu "$((s+4))" \
    --samples "$SAMPLES" --seeds "$SEEDS" --out "$OUT/mouse" > "runs/prot_m_$s.log" 2>&1 & pids+=($!)
done
echo "launched ${#pids[@]} processes: ${pids[*]}"
fail=0
for p in "${pids[@]}"; do wait "$p" || fail=$((fail+1)); done
echo "ALL PROTENIX SHARDS DONE (failures=$fail)"
