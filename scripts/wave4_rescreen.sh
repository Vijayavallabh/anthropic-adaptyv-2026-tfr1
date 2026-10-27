#!/bin/bash
# Wave-4 robust re-screen (ambition-lift, 2026-10-27): confirm BIND + XR on the SWITCHED (submittable)
# Wave-4 sequences under robust DIFF=6 dual-folder folding, and derive switch geometry (switch_prob) from
# the same Boltz human replicate fold. 4 folders, each sharded across 2 GPUs (all 8 used):
#   boltz_h [0 1]  boltz_m [2 3]  chai_h [4 5]  chai_m [6 7].
# XR = min(boltz_m, chai_m) ipSAE ; BIND = min(boltz_h, chai_h) ipSAE ; crown <=> BIND>=0.30 & XR>=0.15.
# Pocket-restrained to the apical epitope (same restraints as the frozen crown screen). _RAW rows = raw
# crowns (no His) carried as controls: raw-vs-switch tells "ceiling was wrong" from "switch install cost XR".
# Usage: wave4_rescreen.sh <cand.csv name,sequence> <out_dir> [DIFF=6]
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
C="${1:?cand.csv}"; OUT="${2:?outdir}"; DIFF="${3:-6}"; SEED="${4:-0}"
mkdir -p "$OUT"
NB=$(($(wc -l < "$C")-1))
echo "[rescreen $(date -u +%FT%TZ)] $NB candidates, DIFF=$DIFF, pocket-restrained dual-folder"

# foreign-GPU guard (shared box)
BUSY=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | wc -l)
[ "$BUSY" -eq 0 ] || { echo "ABORT: $BUSY foreign GPU procs"; exit 1; }

# prep Boltz pocket YAMLs (human + mouse)
$PY scripts/prep_boltz_pocket.py --seqs "$C" --out "$OUT/by_h" --force --no-controls
$PY scripts/prep_boltz_pocket.py --seqs "$C" --target data/targets/mouse_apical_189_383.seq --out "$OUT/bm_h" --force --no-controls

# 4 folders in parallel, 2 GPUs each
DIFF_SAMPLES=$DIFF bash scripts/run_boltz.sh "$OUT/by_h" "$OUT/boltz_h" "0 1" > "$OUT/bh.log" 2>&1 & P1=$!
DIFF_SAMPLES=$DIFF bash scripts/run_boltz.sh "$OUT/bm_h" "$OUT/boltz_m" "2 3" > "$OUT/bm.log" 2>&1 & P2=$!
CONSTRAINTS=runs/f12/pocket/apical_restraint.csv       bash scripts/run_chai.sh "$C" data/targets/apical_domain_189_383.seq "$OUT/chai_h" "4 5" "$SEED" 5 > "$OUT/ch.log" 2>&1 & P3=$!
CONSTRAINTS=runs/f12/pocket/apical_restraint_mouse.csv bash scripts/run_chai.sh "$C" data/targets/mouse_apical_189_383.seq "$OUT/chai_m" "6 7" "$SEED" 5 > "$OUT/cm.log" 2>&1 & P4=$!
wait $P1 $P2 $P3 $P4
echo "[rescreen] folds done $(date -u +%FT%TZ)"

for d in boltz_h boltz_m chai_h chai_m; do $PY scripts/score_ipsae.py "$OUT/$d" $d > "$OUT/$d.ip.log" 2>&1 || true; done
# switch geometry from the Boltz human DIFF replicate fold
$PY scripts/switch_prob.py "$OUT/boltz_h" > "$OUT/switch_prob.tsv" 2>"$OUT/sp.log" || true

# combined table
$PY - "$OUT" <<'PY'
import sys,csv,os
OUT=sys.argv[1]
def rd(p):
    d={}
    if os.path.exists(p):
        for r in csv.DictReader(open(p),delimiter='\t'):
            try: d[r['name']]=float(r['ipsae'])
            except: pass
    return d
bh=rd(f'{OUT}/boltz_h/ipsae.tsv');bm=rd(f'{OUT}/boltz_m/ipsae.tsv')
ch=rd(f'{OUT}/chai_h/ipsae.tsv');cm=rd(f'{OUT}/chai_m/ipsae.tsv')
sp={}
spp=f'{OUT}/switch_prob.tsv'
if os.path.exists(spp):
    for r in csv.DictReader(open(spp),delimiter='\t'):
        sp[r.get('name') or r.get('design')]=r
out=open(f'{OUT}/rescreen_table.tsv','w')
cols=['name','b_h','c_h','BIND','b_m','c_m','XR','crown','sw_frac','sw_mean']
out.write('\t'.join(cols)+'\n')
rows=[]
for n in sorted(set(bh)|set(ch)):
    b_h,c_h,b_m,c_m=bh.get(n),ch.get(n),bm.get(n),cm.get(n)
    BIND=min([x for x in [b_h,c_h] if x is not None],default=0.0)
    XR=min([x for x in [b_m,c_m] if x is not None],default=0.0)
    crown=1 if BIND>=0.30 and XR>=0.15 else 0
    s=sp.get(n,{})
    swf=s.get('frac_ge2') or s.get('frac') or s.get('n_high') or ''
    swm=s.get('mean') or s.get('mean_contacts') or ''
    rows.append((n,b_h,c_h,BIND,b_m,c_m,XR,crown,swf,swm))
def f(x): return f"{x:.3f}" if isinstance(x,float) else ("" if x is None else str(x))
for r in sorted(rows,key=lambda r:(-r[6],-r[3])):
    out.write('\t'.join(f(x) for x in r)+'\n')
out.close()
cr=[r for r in rows if r[7]==1]
print(f"RESCREEN: {len(rows)} folded, {len(cr)} crowns (BIND>=0.30 & XR>=0.15)")
print(f"  XR>=0.40: {sum(1 for r in cr if r[6]>=0.40)}  XR>=0.30: {sum(1 for r in cr if r[6]>=0.30)}  XR>=0.25: {sum(1 for r in cr if r[6]>=0.25)}")
print("  top-12 by XR:")
for r in sorted(rows,key=lambda r:(-r[6],-r[3]))[:12]:
    print(f"    {r[0]:34} BIND {r[3]:.3f}  XR {r[6]:.3f}  sw_frac {r[8]}")
PY
echo "WAVE4_RESCREEN_DONE $(date -u +%FT%TZ) -> $OUT/rescreen_table.tsv"
