#!/bin/bash
# Confirm binding + x-react (dual-folder, DIFF=1) on robust-switch crown candidates.
# Usage: crown_val.sh <cand.csv> <outdir> "<gH gM cH cM gpus>"
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
C="${1:?cand.csv}"; OUT="${2:?outdir}"; read -r gH gM cH cM <<< "${3:-3 5 6 7}"
mkdir -p "$OUT"
$PY scripts/prep_boltz_pocket.py --seqs "$C" --out "$OUT/by_h" --force --no-controls
$PY scripts/prep_boltz_pocket.py --seqs "$C" --target data/targets/mouse_apical_189_383.seq --out "$OUT/bm_h" --force --no-controls
bash scripts/run_boltz.sh "$OUT/by_h" "$OUT/boltz_h" "$gH" > "$OUT/bh.log" 2>&1 & P1=$!
bash scripts/run_boltz.sh "$OUT/bm_h" "$OUT/boltz_m" "$gM" > "$OUT/bm.log" 2>&1 & P2=$!
CONSTRAINTS=runs/f12/pocket/apical_restraint.csv       bash scripts/run_chai.sh "$C" data/targets/apical_domain_189_383.seq "$OUT/chai_h" "$cH" 0 5 > "$OUT/ch.log" 2>&1 & P3=$!
CONSTRAINTS=runs/f12/pocket/apical_restraint_mouse.csv bash scripts/run_chai.sh "$C" data/targets/mouse_apical_189_383.seq "$OUT/chai_m" "$cM" 0 5 > "$OUT/cm.log" 2>&1 & P4=$!
wait $P1 $P2 $P3 $P4
for d in boltz_h boltz_m chai_h chai_m; do $PY scripts/score_ipsae.py "$OUT/$d" $d > "$OUT/$d.ip.log" 2>&1 || true; done
echo "CROWN_VAL_DONE $(date -u +%FT%TZ)"
$PY - "$OUT" <<'PY'
import sys,csv,os
OUT=sys.argv[1]
def rd(p):
    d={}
    if os.path.exists(p):
        for r in csv.DictReader(open(p),delimiter='\t'):
            try:d[r['name']]=float(r['ipsae'])
            except:pass
    return d
bh=rd(f'{OUT}/boltz_h/ipsae.tsv');bm=rd(f'{OUT}/boltz_m/ipsae.tsv');ch=rd(f'{OUT}/chai_h/ipsae.tsv');cm=rd(f'{OUT}/chai_m/ipsae.tsv')
print(f"{'cand':60}{'bH':6}{'cH':6}{'BIND':7}{'bM':6}{'cM':6}{'XR':7}")
for n in sorted(set(bh)|set(ch)):
    b_h,c_h,b_m,c_m=bh.get(n),ch.get(n),bm.get(n),cm.get(n)
    bmin=min([x for x in [b_h,c_h] if x is not None],default=0)
    xr=min([x for x in [b_m,c_m] if x is not None],default=0)
    g=lambda x:f"{x:.3f}" if x is not None else "  -  "
    tag=' <== CROWN' if bmin>=0.30 and xr>=0.15 else ''
    print(f"{n:60}{g(b_h):6}{g(c_h):6}{g(bmin):7}{g(b_m):6}{g(c_m):6}{g(xr):7}{tag}")
PY