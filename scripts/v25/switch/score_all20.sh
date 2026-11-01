#!/bin/bash
# Two-state PROPKA Wyman switch read across all 20 v25 designs on EXISTING bound poses (no new folds).
# Consensus layer only (not a re-ranker). Top-K iptm poses/design for fold-robustness.
# Usage: score_all20.sh [K=2] [single_name]
set -uo pipefail
REPO=/home/prachh/v/anthropic-adaptyv-2026-tfr1
SC=/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad
PYP=/home/prachh/v/sepiq-2026-challenge/.venv-protenix/bin/python   # gemmi (CIF->PDB)
PYS=/home/prachh/v/anthropic-adaptyv-2026-tfr1/.venv/bin/python     # numpy + propka
K=${1:-2}; ONLY=${2:-}
WORK=$SC/sw20; mkdir -p $WORK/poses
MAP=$SC/pose_map20.tsv
OUT=$SC/switch20.tsv
if [ -z "$ONLY" ]; then echo -e "design\tmean_ddg\tmin_ddg\tn_poses\tfrac_release\tbest_dets" > $OUT; fi

while IFS=$'\t' read -r name kind path src; do
  [ -n "$ONLY" ] && [ "$name" != "$ONLY" ] && continue
  pre=$WORK/poses/$name
  rm -f ${pre}_r*.pdb
  if [ "$kind" = "cifdir" ]; then
    nice -n 19 $PYP $SC/scripts/topk_pose_pdb.py "$path" "$pre" "$K" >/dev/null 2>&1
  elif [ "$kind" = "pdb" ]; then
    cp "$path" "${pre}_r1.pdb"
  else
    echo "SKIP $name (no pose)"; continue
  fi
  nice -n 19 $PYS - "$name" "$pre" "$OUT" "$src" <<'PY'
import sys, glob, numpy as np
sys.path.insert(0,"/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad/scripts")
from ph_release_tfr1 import score
name, pre, out, src = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
ddgs=[]; rels=[]; best=None; bestdd=1e9
for pdb in sorted(glob.glob(pre+"_r*.pdb")):
    r=score(pdb)
    if r is None: continue
    ddgs.append(r['ddg']); rels.append(1 if r['ddg']<-0.02 else 0)
    if r['ddg']<bestdd: bestdd=r['ddg']; best=r['dets']
if ddgs:
    mean=float(np.mean(ddgs)); mn=min(ddgs); frac=float(np.mean(rels)); n=len(ddgs)
    open(out,"a").write(f"{name}\t{mean:.3f}\t{mn:.3f}\t{n}\t{frac:.2f}\t{best}\n")
    print(f"{name:<42} mean{mean:+.3f} min{mn:+.3f} n{n} frac{frac:.2f} [{src}]")
else:
    open(out,"a").write(f"{name}\tNA\tNA\t0\tNA\t-\n"); print(f"{name:<42} NA [{src}]")
PY
done < $MAP
[ -z "$ONLY" ] && echo "SCORE_ALL20_DONE $(date -u +%FT%TZ) -> $OUT"
