#!/bin/bash
# Wave-5 partial-diffusion SMOKE (ambition-lift, 2026-10-27): confirm the partial-diffusion contig produces
# perturbed-but-docked binder variants of our best crown before committing a full wave. RFd outputs
# target=chainA, binder=chainB (mpnn_rfd convention) -> list TARGET segment first in the contig.
# Seed = w3g6_146 (best XR 0.397). 2 designs, 1 GPU, partial_T=10. Inspect: output binder len ~= 92, docked.
# Usage: wave5_smoke.sh [gpu=0]
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
G=${1:-0}
SEED=runs/f28/switch/complexes/w3g6_146_mpnn0.pdb
BL=$(awk '$1=="ATOM"&&$3=="CA"&&$5=="A"' "$SEED" | wc -l)   # binder = chain A in the seed
TL=$(awk '$1=="ATOM"&&$3=="CA"&&$5=="B"' "$SEED" | wc -l)   # target = chain B in the seed
echo "[smoke] seed=$SEED binderlen(A)=$BL targetlen(B)=$TL gpu=$G"
OUT=runs/rfdpd_smoke; rm -rf "$OUT"; mkdir -p "$OUT"
# contig: TARGET first (B1-TL -> output chainA), then BINDER (A1-BL -> output chainB); partial_T=10 light noise
bash scripts/gen_rfd1.sh "$OUT" "$SEED" "B1-${TL}/0 A1-${BL}" "B14,B15,B21,B22" 2 "$G" 10 2>&1 | tail -5
echo "=== smoke outputs ==="
for p in "$OUT"/des_*.pdb; do
  [ -f "$p" ] || { echo "NO OUTPUT PDB — contig likely wrong"; break; }
  a=$(awk '$1=="ATOM"&&$3=="CA"&&$5=="A"' "$p" | wc -l); b=$(awk '$1=="ATOM"&&$3=="CA"&&$5=="B"' "$p" | wc -l)
  echo "$(basename "$p"): chainA(target)=$a  chainB(binder)=$b"
done
echo "WAVE5_SMOKE_DONE $(date -u +%FT%TZ)  (expect chainA~$TL chainB~$BL; then scale to full wave5_drive)"
