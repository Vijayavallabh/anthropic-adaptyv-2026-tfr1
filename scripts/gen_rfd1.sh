#!/bin/bash
# Sharded RFdiffusion1 binder generation across GPUs (novel folds for the Adaptyv novelty gate).
# Usage: gen_rfd1.sh <out_prefix_dir> <input_pdb> "<contigs>" "<hotspots>" <total_designs> "<gpus>" [partial_T]
#   partial_T empty/0 = de-novo; >0 = partial diffusion from the input complex (binding-preserving).
# Each GPU gets a contiguous design_startnum block so output indices never collide.
set -uo pipefail
KIT=/home/prachh/v/anthropic-adaptyv-2026-tfr1/third_party/rfd1kit
RUN="$KIT/rfdiffusion1/run.sh"
PY="$KIT/rfd1/bin"
OUT=${1:?out dir}; PDB=${2:?input pdb}; CONTIGS=${3:?contigs}; HOTSPOTS=${4:?hotspots}; N=${5:?total}; GPUS=${6:-0 1 2 3 4 5 6 7}; PT=${7:-0}
read -r -a G <<< "$GPUS"; NG=${#G[@]}
per=$(( (N + NG - 1) / NG ))
mkdir -p "$OUT"
export WEIGHTS="$KIT/weights" RFD_ROOT="$KIT/rfd1kit_RFdiffusion" PYTHONHASHSEED=0
[ -d "$KIT/RFdiffusion" ] && export RFD_ROOT="$KIT/RFdiffusion"
echo "[gen_rfd1] N=$N per-gpu=$per gpus=[$GPUS] partial_T=$PT $(date -u +%FT%TZ)"
pids=()
for i in "${!G[@]}"; do
  g=${G[$i]}; start=$(( i * per ))
  [ "$start" -ge "$N" ] && continue
  cnt=$per; [ $(( start + cnt )) -gt "$N" ] && cnt=$(( N - start ))
  EXTRA=(denoiser.noise_scale_ca=0 denoiser.noise_scale_frame=0)
  [ "$PT" != 0 ] && EXTRA+=(diffuser.partial_T="$PT")
  CUDA_VISIBLE_DEVICES=$g PATH="$PY:$PATH" bash "$RUN" design --config h100 --mode fast \
    inference.input_pdb="$PDB" \
    "contigmap.contigs=[$CONTIGS]" \
    "ppi.hotspot_res=[$HOTSPOTS]" \
    inference.num_designs="$cnt" inference.design_startnum="$start" \
    inference.output_prefix="$OUT/des" \
    > "$OUT/sh${g}.log" 2>&1 &
  pids+=($!); sleep 5
done
rc=0; for p in "${pids[@]}"; do wait "$p" || rc=1; done
echo "RFD1_DONE rc=$rc backbones: $(ls "$OUT"/des_*.pdb 2>/dev/null | wc -l) $(date -u +%FT%TZ)"
