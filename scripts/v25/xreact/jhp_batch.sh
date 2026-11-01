#!/bin/bash
# JustHISpKa (authoritative His-pKa) on a list of ms candidates: extract best human pose binder monomer,
# prep (AmberTools), run justHisPKa per His. Prints pKa + in-window[5.5,7.4] flag. Args: name1 name2 ...
set -uo pipefail
REPO=/home/prachh/v/anthropic-adaptyv-2026-tfr1
SC=/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad
PYP=/home/prachh/v/sepiq-2026-challenge/.venv-protenix/bin/python
EXE=$REPO/tools/justhispka/justHisPKa
for name in "$@"; do
  # locate human fold dir
  fd=""
  for base in xr_fold2 xr_fold xr_n80; do
    [ -d "$SC/$base/human/$name" ] && { fd="$SC/$base/human/$name"; break; }
  done
  [ -z "$fd" ] && { echo "$name: NO_FOLD"; continue; }
  wk=$SC/sw_assess/$name; mkdir -p $wk
  $PYP $SC/scripts/topk_pose_pdb.py "$fd" "$wk/pose" 1 >/dev/null 2>&1
  awk '$1=="ATOM" && substr($0,22,1)=="A"' $wk/pose_r1.pdb > $wk/binder.pdb; echo END >> $wk/binder.pdb
  bash $SC/scripts/prep_design.sh $wk/binder.pdb $wk/jhp > $wk/prep.log 2>&1 || { echo "$name: PREP_FAIL"; continue; }
  M=$wk/jhp/prep.mol2; P=$wk/jhp/p3.prmtop
  [ -s "$M" ] || { echo "$name: NOPREP"; continue; }
  nin=0; res=""
  for sid in $(awk '/@<TRIPOS>SUBSTRUCTURE/{f=1;next}/@<TRIPOS>/{f=0}f&&$NF=="HIS"{print $1}' "$M"); do
    out=$($EXE MOL="$M" SID=$sid PRM="$P" NUM_THREAD=2 2>&1)
    pk=$(echo "$out"|awk '/^PKA=/{v=$1} END{sub(/PKA=/,"",v);print v}')
    [ -z "$pk" ] && { res="$res H$sid=ERR"; continue; }
    inw=$(awk -v v="$pk" 'BEGIN{print (v>=5.5&&v<=7.4)?1:0}')
    [ "$inw" = "1" ] && nin=$((nin+1))
    res="$res H$sid=$pk$([ "$inw" = "1" ] && echo '*')"
  done
  echo "$name: in-window=$nin |$res   $([ "$nin" -ge 2 ] && echo 'SWITCH-PASS' || echo 'switch-fail')"
done
echo "JHP_BATCH_DONE"
