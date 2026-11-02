#!/bin/bash
# Validate the 2 v27 replacement picks for FULL Tier-A parity: switch (JustHISpKa, binder-alone, His in [5.5,7.4])
# + novelty (structural single-seq maxTM vs PDB). Binding already confirmed on calibrated ruler (repl_fold):
#   v25g5_13 H0.283/med0.227 non-phantom; v25g3_130 H0.210 both-epi-XR non-phantom.
set -uo pipefail
BASE=/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad
REPO=/home/prachh/v/anthropic-adaptyv-2026-tfr1
ESMPY=/home/prachh/v/.venv-esmfold2/bin/python
PREP=$BASE/scripts/prep_design.sh
EXE=$REPO/tools/justhispka/justHisPKa
W=$BASE/v27_val
CSV=$BASE/v27cands.csv
cd $REPO
mkdir -p $W/esmfold $W/jhp $W/nov
echo "[v27] esmfold monomer on GPU 2"
CUDA_VISIBLE_DEVICES=2 $ESMPY scripts/esmfold_monomer.py "$CSV" "$W/esmfold" 2>&1 | tail -1
echo "[v27] esmfold pdbs: $(ls $W/esmfold/*.pdb 2>/dev/null | wc -l)"
OUT=$BASE/v27_switch.tsv; : > "$OUT"
for pdb in "$W"/esmfold/*.pdb; do
  [ -e "$pdb" ] || continue
  n=$(basename "$pdb" .pdb)
  bash "$PREP" "$pdb" "$W/jhp/$n" >/dev/null 2>&1 || { echo -e "$n\tPREP_FAIL\t-" >> "$OUT"; continue; }
  m="$W/jhp/$n/prep.mol2"; p="$W/jhp/$n/p3.prmtop"
  [ -s "$m" ] || { echo -e "$n\tNOPREP\t-" >> "$OUT"; continue; }
  for sid in $(awk '/@<TRIPOS>SUBSTRUCTURE/{f=1;next}/@<TRIPOS>/{f=0}f&&$NF=="HIS"{print $1}' "$m"); do
    o=$("$EXE" MOL="$m" SID=$sid PRM="$p" NUM_THREAD=2 2>&1)
    pk=$(echo "$o"|awk '/^PKA=/{v=$1} END{sub(/PKA=/,"",v);print v}'); [ -z "$pk" ] && pk="ERR"
    echo -e "$n\t$sid\t$pk" >> "$OUT"
  done
done
echo "[v27] novelty (ESMFold single-seq maxTM vs PDB) on GPU 2"
CUDA_VISIBLE_DEVICES=2 $ESMPY scripts/novelty_struct.py --seqs "$CSV" --out "$BASE/v27_nov.csv" --struct-dir "$W/nov" --pdb "$REPO/tools/foldseek_pdb/pdb" 2>&1 | tail -3
echo "V27_VALIDATE_DONE"
echo "=== SWITCH (His pKa; in-window=[5.5,7.4]) ==="; cat "$OUT"
echo "=== NOVELTY ==="; cat "$BASE/v27_nov.csv" 2>/dev/null
