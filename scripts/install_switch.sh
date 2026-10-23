#!/bin/bash
# Install mech-B buried-His switch into (cross-reactive) RFD4 survivor binders.
# Gathers each survivor's folded complex, scans for buried K/R cations, builds 2-3 His combos.
# Usage: install_switch.sh <survivors.csv name,sequence> <screen_fold_dir> <out_dir>
set -uo pipefail
cd "$(dirname "$0")/.."
PB=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
SURV=${1:?survivors.csv}; FOLD=${2:?fold_dir}; OUT=${3:?out_dir}
mkdir -p "$OUT/complexes" "$OUT/scan"
while IFS=, read -r name seq; do
  [ "$name" = "name" ] && continue
  cpx=$(find "$FOLD" -path "*predictions/$name/${name}_model_0.pdb" 2>/dev/null | head -1)
  [ -n "$cpx" ] || { echo "  no complex: $name"; continue; }
  cp "$cpx" "$OUT/complexes/$name.pdb"
  "$PB" scripts/buried_switch_scan.py "$OUT/complexes/$name.pdb" "$OUT/scan/$name" 12 >/dev/null 2>&1 || echo "  scan fail: $name"
done < "$SURV"
echo "[install_switch] complexes=$(ls "$OUT/complexes" 2>/dev/null | wc -l) scanned=$(ls "$OUT/scan" 2>/dev/null | wc -l)"
"$PB" scripts/build_switch_combos.py --scan "$OUT/scan" --complexes "$OUT/complexes" --seqs "$SURV" \
  --out "$OUT/switched.csv" --map "$OUT/switch_map.tsv"
echo "SWITCH_INSTALL_DONE $(($(wc -l < "$OUT/switched.csv" 2>/dev/null)-1)) switched seqs"
