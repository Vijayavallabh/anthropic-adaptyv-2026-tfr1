#!/bin/bash
# Genie3 de-novo binder generation at the TfR1 CONSERVED apical sub-site (frag 14,15,21,22 =
# UniProt 202,203,209,210; conserved human/mouse -> x-react bias). Genie3 = organizers' top flat-target
# generator (gave ALL the cross-reactive TNF binders), never run for TfR1. Shards across GPUs, 1 proc/GPU,
# distinct seeds, per-GPU triton cache. VERIFY GPUs free first (never clobber a foreign job).
# Usage: gen_genie3_tfr1.sh "<gpu space-list>" [total_N=840] [seed_base=9100] [tag=genie3_apical]
set -uo pipefail
REPO=/home/prachh/v/anthropic-adaptyv-2026-tfr1; cd "$REPO"
G3="$REPO/third_party/genie3"
PY="$G3/venv_g3/bin/python"; BATCH="$G3/opt/genie3_opt/g3batch.py"
DS="$G3/stock_src/genie3/data/design/binder_design/tfr1_apicalbench"
CKPT="$REPO/weights/genie3/pretrained/v1/checkpoints/step=600000.ckpt"
CFG="$REPO/weights/genie3/pretrained/v1/config.yaml"
IFS=' ' read -ra GPUS <<< "${1:-}"; NG=${#GPUS[@]}
[ "$NG" -ge 1 ] || { echo "usage: gen_genie3_tfr1.sh \"<gpus>\" [N] [seedbase] [tag]"; exit 2; }
TOTAL="${2:-840}"; SEEDBASE="${3:-9100}"; TAG="${4:-genie3_apical}"
PERSHARD=$(( (TOTAL + NG - 1) / NG ))
[ -f "$CKPT" ] || { echo "no checkpoint $CKPT"; exit 3; }
echo "[gen-apical] $TOTAL designs across ${NG} GPUs (${GPUS[*]}) ~$PERSHARD/shard seedbase $SEEDBASE $(date -u +%FT%TZ)"
pids=(); i=0
for g in "${GPUS[@]}"; do
  SH="$REPO/runs/${TAG}/shard_g${g}"; mkdir -p "$SH" "$REPO/.jit/g3_triton_g${g}"
  REQ="$SH/request.yaml"
  python3 - "$SH" "$DS" "$((SEEDBASE + i))" "$PERSHARD" "$REQ" "$CKPT" "$CFG" <<'PY'
import sys
sh,ds,seed,n,req,ckpt,cfg=sys.argv[1:8]
open(req,"w").write(f"""experiment:
  name: tfr1_apical_g{seed}
  seed: {seed}
paths:
  rootdir: {sh}
  dataset: {ds}
generation:
  dataset:
    source: target
    selections: tfr1_apical
    n_sample: {n}
  sampler:
    sampler:
      direction_scale: 0.0
  base:
    checkpoint: {ckpt}
    config: {cfg}
""")
print("wrote",req)
PY
  ( CUDA_VISIBLE_DEVICES="$g" TRITON_CACHE_DIR="$REPO/.jit/g3_triton_g${g}/cache" TRITON_HOME="$REPO/.jit/g3_triton_g${g}" \
      OMP_NUM_THREADS=16 "$PY" "$BATCH" --config "$REQ" --outdir "$SH" --batch-size 1 \
      --cuda-graphs --hoist --reuse-graphs 16 --lean-pair --wide-capture --alloc expandable \
      --pt-chunk design --tf32 --trimul fpf --compile --timings "$SH/timings.json" ) > "$SH/design.log" 2>&1 &
  pids+=($!); i=$((i+1)); sleep 4
done
echo "[gen-apical] launched ${#pids[@]} shards; waiting..."
rc=0; for p in "${pids[@]}"; do wait "$p" || rc=1; done
NB=$(find "$REPO/runs/${TAG}"/shard_g*/ -name "*.pdb" 2>/dev/null | wc -l)
echo "GEN_GENIE3_TFR1_DONE rc=$rc backbones=$NB $(date -u +%FT%TZ)  (under runs/${TAG}/shard_g*/)"