#!/bin/bash
# Shard a dir of af2ig input complex PDBs across GPUs and run fold_af2ig (TNF kit) on each
# in parallel. af2ig is the primary de-novo binder gate (Boltz over-docks this target).
# Usage: af2ig_sharded.sh <af2in_dir> <out_base> ["g0 g1 ..."=1 2 3 4]
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"; cd "$REPO"
AF2IN=${1:?af2in dir}; OUTB=${2:?out base}; read -r -a G <<< "${3:-1 2 3 4}"; NG=${#G[@]}
FOLD="$REPO/scripts/fold_af2ig.sh"
[ -f "$FOLD" ] || { echo "no fold_af2ig.sh at $FOLD" >&2; exit 2; }
pdbs=( "$AF2IN"/*.pdb ); n=${#pdbs[@]}
[ "$n" -gt 0 ] || { echo "no input pdbs in $AF2IN" >&2; exit 2; }
echo "[af2ig_sharded] $n inputs across $NG gpus (${G[*]}) $(date -u +%FT%TZ)"
for i in $(seq 0 $((NG-1))); do mkdir -p "$OUTB/shard$i/in"; done
k=0; for p in "${pdbs[@]}"; do s=$((k % NG)); ln -sf "$(readlink -f "$p")" "$OUTB/shard$s/in/$(basename "$p")"; k=$((k+1)); done
pids=()
for i in $(seq 0 $((NG-1))); do
  g=${G[$i]}
  nohup bash "$FOLD" "$g" "$OUTB/shard$i/in" "$OUTB/shard$i/out" exact > "$OUTB/shard$i.log" 2>&1 &
  pids+=($!)
  # STAGGER: cuBLAS init races when many af2ig/jax procs start together
  # ("Failed to initialize BLAS support"); let each finish CUDA init before the next.
  [ "$i" -lt "$((NG-1))" ] && sleep 25
done
for p in "${pids[@]}"; do wait "$p" || true; done
echo "AF2IG_SHARDED_DONE $(date -u +%FT%TZ) | score files: $(find "$OUTB" -name '*.sc' | wc -l)"
