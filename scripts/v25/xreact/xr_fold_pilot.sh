#!/bin/bash
# STAGED: cross-reactivity PILOT fold (human + mouse) on the dev-screen-clean, diverse pilot + POS/NEG
# controls, BLIND Protenix cuequivariance engine (the v25 ruler). Distributes across free GPUs 2-7.
# Refuses to start if CPU load is too high (Protenix hangs at model-build under contention).
# Usage: xr_fold_pilot.sh [maxload=120] [samples=20] [seeds=101,102]
set -uo pipefail
REPO=/home/prachh/v/anthropic-adaptyv-2026-tfr1
SC=/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad
PYP=/home/prachh/v/sepiq-2026-challenge/.venv-protenix/bin/python
MAXLOAD=${1:-120}; SAMP=${2:-20}; SEEDS=${3:-101,102}
LOAD=$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)
if [ "$LOAD" -gt "$MAXLOAD" ]; then
  echo "ABORT: load $LOAD > $MAXLOAD — Protenix will hang at model-build. Free the CPU first."; exit 3
fi
# build fold input = pilot + 3 controls
IN=$SC/xr_fold_input.csv
echo "name,sequence" > $IN
tail -n +2 $SC/ms_pilot.csv >> $IN
tail -n +2 $REPO/runs/prot/controls.csv 2>/dev/null | awk -F',' 'NF>=2{print $1","$2}' >> $IN
N=$(($(wc -l < $IN)-1)); echo "fold input: $N designs (pilot+controls) -> $IN"
# GPU shards (free GPUs 2-7; skip foreign 0-1)
GPUS=(2 3 4 5 6 7); NG=${#GPUS[@]}
mapfile -t NAMES < <(tail -n +2 $IN | cut -d',' -f1)
declare -A SHARD
for i in "${!NAMES[@]}"; do g=${GPUS[$((i % NG))]}; SHARD[$g]+="${NAMES[$i]},"; done
for SP in human mouse; do
  OUT=$SC/xr_fold/$SP; mkdir -p $OUT
  for g in "${GPUS[@]}"; do
    names=${SHARD[$g]%,}; [ -z "$names" ] && continue
    ( nice -n 10 $PYP $REPO/scripts/fold_protenix_tfr1.py --seqs $IN --species $SP \
        --out $OUT --gpu $g --samples $SAMP --seeds $SEEDS --names "$names" \
        > $SC/xr_fold/log_${SP}_g${g}.log 2>&1 ) &
    echo "launched $SP gpu=$g ($(echo $names | tr ',' '\n' | grep -c .) designs)"
  done
  wait   # finish this species (6 concurrent, one per GPU) before the next
  echo "$SP wave done $(date -u +%FT%TZ)"
done
echo "XR_FOLD_PILOT_DONE $(date -u +%FT%TZ)"
echo "human CIFs: $(find $SC/xr_fold/human -name '*_sample_*.cif' 2>/dev/null | wc -l)  mouse CIFs: $(find $SC/xr_fold/mouse -name '*_sample_*.cif' 2>/dev/null | wc -l)"
