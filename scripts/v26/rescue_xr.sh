#!/bin/bash
# Lever A: switch-INSTALL on the strongest switchless cross-reactive hits (buried-His, off-interface).
set -uo pipefail
REPO=/home/prachh/v/anthropic-adaptyv-2026-tfr1
SC=/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad
PYP=/home/prachh/v/sepiq-2026-challenge/.venv-protenix/bin/python
ESMPY=/home/prachh/v/.venv-esmfold2/bin/python
PREP=$SC/scripts/prep_design.sh
EXE=$REPO/tools/justhispka/justHisPKa
RB=$SC/rescue_xr
cd $REPO
mkdir -p $RB/combos $RB/esmfold $RB/jhp $RB/cplx $RB/scan
TARGETS="ms_v25g3_65_mpnn1_s6 ms_v25g3_65_mpnn1_s0 ms_v25g4_92_mpnn1_s0 ms_v25g4_92_mpnn1_s6 ms_v25g4_92_mpnn1_s9 ms_v25g4_44_mpnn0_s2"
echo "name,sequence" > $RB/all_combos.csv
for name in $TARGETS; do
  fd=""
  for base in xr_fold2 xr_fold; do [ -d "$SC/$base/human/$name" ] && { fd="$SC/$base/human/$name"; break; }; done
  [ -z "$fd" ] && { echo "$name NO_FOLD"; continue; }
  $PYP $SC/scripts/topk_pose_pdb.py "$fd" "$RB/cplx/$name" 1 >/dev/null 2>&1
  cpx="$RB/cplx/${name}_r1.pdb"
  [ -s "$cpx" ] || { echo "$name NO_POSE"; continue; }
  seq=$(awk -F',' -v n="$name" '$1==n{print $2}' $SC/ms/mpnn/ms_binders.csv)
  $PYP scripts/buried_switch_scan.py "$cpx" "$RB/scan/$name" 14 2>&1 | tail -1
  nscan=$(ls $RB/scan/$name/*.pdb 2>/dev/null | wc -l)
  $PYP scripts/exhaustive_switch.py --complex "$cpx" --scan "$RB/scan/$name" --name "xr_${name#ms_v25}" \
      --parent-seq "$seq" --out $RB/combos/$name.csv --max 10 2>&1 | tail -1
  nc=0; [ -f $RB/combos/$name.csv ] && { tail -n+2 $RB/combos/$name.csv >> $RB/all_combos.csv; nc=$(($(wc -l < $RB/combos/$name.csv)-1)); }
  echo "  $name: scan=$nscan combos=$nc"
done
NC=$(($(wc -l < $RB/all_combos.csv)-1)); echo "[rescue_xr] total combos: $NC"
[ "$NC" -eq 0 ] && { echo "NO COMBOS — Lever A yields nothing"; exit 0; }
CUDA_VISIBLE_DEVICES=4 $ESMPY scripts/esmfold_monomer.py $RB/all_combos.csv $RB/esmfold 2>&1 | tail -2
echo "[rescue_xr] esmfold: $(ls $RB/esmfold/*.pdb 2>/dev/null | wc -l)"
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
echo "RESCUE_XR_DONE rows=$(wc -l < "$OUT") $(date -u +%FT%TZ)"
