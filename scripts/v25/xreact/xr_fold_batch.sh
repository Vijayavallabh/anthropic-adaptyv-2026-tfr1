#!/bin/bash
# Generic BLIND-Protenix fold of a CSV over free GPUs 2-7, both species, cuequivariance ruler.
# Usage: xr_fold_batch.sh <input.csv> <outdir> [samples=20] [seeds=101,102] [maxload=160]
set -uo pipefail
REPO=/home/prachh/v/anthropic-adaptyv-2026-tfr1
PYP=/home/prachh/v/sepiq-2026-challenge/.venv-protenix/bin/python
IN=${1:?input.csv}; OUTD=${2:?outdir}; SAMP=${3:-20}; SEEDS=${4:-101,102}; MAXLOAD=${5:-160}
LOAD=$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)
[ "$LOAD" -gt "$MAXLOAD" ] && { echo "ABORT load $LOAD>$MAXLOAD"; exit 3; }
GPUS=(2 3 4 5 6 7); NG=${#GPUS[@]}
mapfile -t NAMES < <(tail -n +2 $IN | cut -d',' -f1)
declare -A SHARD
for i in "${!NAMES[@]}"; do g=${GPUS[$((i % NG))]}; SHARD[$g]+="${NAMES[$i]},"; done
for SP in human mouse; do
  OUT=$OUTD/$SP; mkdir -p $OUT
  for g in "${GPUS[@]}"; do
    names=${SHARD[$g]%,}; [ -z "$names" ] && continue
    ( nice -n 10 $PYP $REPO/scripts/fold_protenix_tfr1.py --seqs $IN --species $SP \
        --out $OUT --gpu $g --samples $SAMP --seeds $SEEDS --names "$names" \
        > $OUTD/log_${SP}_g${g}.log 2>&1 ) &
  done
  wait; echo "$SP wave done $(date -u +%FT%TZ)"
done
echo "XR_FOLD_BATCH_DONE $OUTD $(date -u +%FT%TZ)"
echo "human CIFs:$(find $OUTD/human -name '*_sample_*.cif' 2>/dev/null|wc -l) mouse CIFs:$(find $OUTD/mouse -name '*_sample_*.cif' 2>/dev/null|wc -l)"
