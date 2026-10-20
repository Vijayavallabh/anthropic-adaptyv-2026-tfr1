#!/bin/bash
# F04: BoltzGen de-novo binder generation for one arm, sharded across GPUs.
# BoltzGen co-designs seq+structure in the `design` step (binder=chain A, target=chain B in outputs).
# "designs in a batch share a length" -> small --diffusion_batch_size gives length diversity.
# No --seed on `boltzgen run`; per-process RNG differs across GPUs, so shards produce distinct designs.
# Usage: gen_boltzgen.sh <spec.yaml> <outdir> <total_designs> "<gpus>" [protocol] [batch_size]
set -uo pipefail
BG=/home/prachh/v/anthropic-adaptyv-2026-glp1r/third_party/boltzgen
REPO="$(cd "$(dirname "$0")/.." && pwd)"
SPEC="$1"; OUT="$2"; NTOT="${3:-210}"; GPUS="${4:-1 2 3 4 5 6 7}"; PROTO="${5:-protein-anything}"; BS="${6:-2}"
export HF_HOME=/home/prachh/work/cache/huggingface OMP_NUM_THREADS=8
[ -f "$SPEC" ] || { echo "spec not found: $SPEC" >&2; exit 2; }
mkdir -p "$OUT"
read -r -a G <<< "$GPUS"; NG=${#G[@]}
per=$(( (NTOT + NG - 1) / NG ))
echo "[boltzgen] arm=$(basename "$SPEC" .yaml) out=$OUT total=$NTOT per_gpu=$per gpus=[$GPUS] proto=$PROTO bs=$BS $(date -u +%FT%TZ)"
pids=()
for g in "${G[@]}"; do
  od="$OUT/gpu$g"; mkdir -p "$od" "$REPO/.jit/bg_g$g"
  CUDA_VISIBLE_DEVICES="$g" MODEL_OPT_JIT_ROOT="$REPO/.jit/bg_g$g" \
    TRITON_CACHE_DIR="$REPO/.jit/bg_g$g/cache" \
    "$BG/.venv/bin/boltzgen" run "$SPEC" \
      --output "$od" --num_designs "$per" --protocol "$PROTO" \
      --steps design --devices 1 --diffusion_batch_size "$BS" --use_kernels false \
      > "$OUT/gen_g$g.log" 2>&1 &
  pids+=($!); sleep 4
done
rc=0
for p in "${pids[@]}"; do wait "$p" || rc=1; done
n=$(find "$OUT" -path '*/intermediate_designs/*_[0-9]*.cif' 2>/dev/null | wc -l)
echo "[boltzgen] arm done rc=$rc designs=$n $(date -u +%FT%TZ)"
