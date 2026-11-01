#!/bin/bash
# Lever A stage 2: ESMFold the 29 switch-install combos -> JustHISpKa in-window gate.
set -uo pipefail
REPO=/home/prachh/v/anthropic-adaptyv-2026-tfr1
SC=/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad
ESMPY=/home/prachh/v/.venv-esmfold2/bin/python
PREP=$SC/scripts/prep_design.sh
EXE=$REPO/tools/justhispka/justHisPKa
RB=$SC/rescue_xr
cd $REPO
NC=$(($(wc -l < $RB/all_combos.csv)-1)); echo "[stage2] combos=$NC"
CUDA_VISIBLE_DEVICES=5 $ESMPY scripts/esmfold_monomer.py $RB/all_combos.csv $RB/esmfold 2>&1 | tail -2
echo "[stage2] esmfold pdbs: $(ls $RB/esmfold/*.pdb 2>/dev/null | wc -l)"
OUT=$SC/rescue_xr_switch.tsv; : > "$OUT"
for pdb in "$RB"/esmfold/*.pdb; do
  [ -e "$pdb" ] || continue
  n=$(basename "$pdb" .pdb)
  bash "$PREP" "$pdb" "$RB/jhp/$n" >/dev/null 2>&1 || { echo -e "$n\tPREP_FAIL" >> "$OUT"; continue; }
  m="$RB/jhp/$n/prep.mol2"; p="$RB/jhp/$n/p3.prmtop"
  [ -s "$m" ] || { echo -e "$n\tNOPREP" >> "$OUT"; continue; }
  for sid in $(awk '/@<TRIPOS>SUBSTRUCTURE/{f=1;next}/@<TRIPOS>/{f=0}f&&$NF=="HIS"{print $1}' "$m"); do
    out=$("$EXE" MOL="$m" SID=$sid PRM="$p" NUM_THREAD=2 2>&1)
    pk=$(echo "$out"|awk '/^PKA=/{v=$1} END{sub(/PKA=/,"",v);print v}'); [ -z "$pk" ] && pk="ERR"
    echo -e "$n\t$sid\t$pk" >> "$OUT"
  done
done
echo "RESCUE_XR_STAGE2_DONE rows=$(wc -l < "$OUT") $(date -u +%FT%TZ)"
