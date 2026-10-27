#!/bin/bash
# Lossless 2-stage crown screen (same verdict as a full 4-fold crown_val, far less Chai compute).
# crown <=> min(b_h,c_h)>=0.30 AND min(b_m,c_m)>=0.15. Because the min can only be <= either folder,
# a true crown MUST have Boltz-human>=0.30 AND Boltz-mouse>=0.15 (unless that Boltz fold is absent).
# So: STAGE A folds cheap Boltz (human+mouse) on ALL candidates across 8 GPUs and keeps only those that
# can still possibly crown; STAGE B runs the expensive Chai (human+mouse, 5 samples) ONLY on survivors.
# Non-survivors are provably non-crowns regardless of Chai, so skipping their Chai is lossless.
# Usage: crown_screen_2stage.sh <binders.csv> <out_root>
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
C=${1:?binders.csv}; OUT=${2:?out_root}; mkdir -p "$OUT"
BUSY=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | wc -l)
[ "$BUSY" -eq 0 ] || { echo "ABORT: $BUSY foreign GPU procs"; exit 1; }

echo "### STAGE A: Boltz human(0-3)+mouse(4-7) on ALL candidates $(date -u +%FT%TZ)"
$PY scripts/prep_boltz_pocket.py --seqs "$C" --out "$OUT/by_h" --force --no-controls
$PY scripts/prep_boltz_pocket.py --seqs "$C" --target data/targets/mouse_apical_189_383.seq --out "$OUT/bm_h" --force --no-controls
bash scripts/run_boltz.sh "$OUT/by_h" "$OUT/boltz_h" "0 1 2 3" > "$OUT/bh.log" 2>&1 & PBH=$!
bash scripts/run_boltz.sh "$OUT/bm_h" "$OUT/boltz_m" "4 5 6 7" > "$OUT/bm.log" 2>&1 & PBM=$!
wait $PBH; wait $PBM
$PY scripts/score_ipsae.py "$OUT/boltz_h" boltz_h > "$OUT/boltz_h.ip.log" 2>&1 || true
$PY scripts/score_ipsae.py "$OUT/boltz_m" boltz_m > "$OUT/boltz_m.ip.log" 2>&1 || true

echo "### FILTER: keep if NOT(b_h present & b_h<0.30) AND NOT(b_m present & b_m<0.15) $(date -u +%FT%TZ)"
$PY - "$C" "$OUT" <<'PY'
import csv,sys,os
C,OUT=sys.argv[1],sys.argv[2]
def rd(p):
    d={}
    if os.path.exists(p):
        for r in csv.DictReader(open(p),delimiter='\t'):
            try:
                v=float(r['ipsae'])
                if v==v: d[r['name']]=v   # skip NaN (parse-fail) -> treat as ABSENT, not present-below-bar
            except: pass
    return d
bh=rd(f'{OUT}/boltz_h/ipsae.tsv'); bm=rd(f'{OUT}/boltz_m/ipsae.tsv')
seq={r['name']:r['sequence'] for r in csv.DictReader(open(C))}
# full Boltz table (for near-crown / prong-B analysis later)
with open(f'{OUT}/stageA_boltz.tsv','w') as f:
    f.write("name\tb_h\tb_m\n")
    for n in sorted(seq, key=lambda n:-min(bh.get(n,0),bm.get(n,0))):
        f.write(f"{n}\t{bh.get(n,float('nan')):.4f}\t{bm.get(n,float('nan')):.4f}\n")
def keep(n):
    okh = (n not in bh) or bh[n]>=0.30
    okm = (n not in bm) or bm[n]>=0.15
    return okh and okm  # lossless: both-Boltz-absent defers to Chai (matches crown_val min-over-present)
surv=[n for n in seq if keep(n)]
surv.sort(key=lambda n:-min(bh.get(n,0),bm.get(n,0)))
w=csv.writer(open(f'{OUT}/stageA_survivors.csv','w')); w.writerow(['name','sequence'])
for n in surv: w.writerow([n,seq[n]])
nb_h=sum(1 for n in seq if bh.get(n,0)>=0.30); nb_m=sum(1 for n in seq if bm.get(n,0)>=0.15)
print(f'[stageA] input={len(seq)}  boltz_h>=0.30: {nb_h}  boltz_m>=0.15: {nb_m}  survivors(both): {len(surv)}')
print('[stageA] top survivors: '+', '.join(f"{n}(h{bh.get(n,0):.2f}/m{bm.get(n,0):.2f})" for n in surv[:12]))
PY
NS=$(($(wc -l < "$OUT/stageA_survivors.csv")-1))
echo "stageA survivors: $NS"
if [ "$NS" -le 0 ]; then echo "CROWNS=0 (no survivors)"; echo "CROWN_SCREEN_2STAGE_DONE $(date -u +%FT%TZ)"; exit 0; fi

echo "### STAGE B: Chai human(0-3)+mouse(4-7) on $NS survivors $(date -u +%FT%TZ)"
S="$OUT/stageA_survivors.csv"
CONSTRAINTS=runs/f12/pocket/apical_restraint.csv       bash scripts/run_chai.sh "$S" data/targets/apical_domain_189_383.seq "$OUT/chai_h" "0 1 2 3" 0 5 > "$OUT/ch.log" 2>&1 & PCH=$!
CONSTRAINTS=runs/f12/pocket/apical_restraint_mouse.csv bash scripts/run_chai.sh "$S" data/targets/mouse_apical_189_383.seq "$OUT/chai_m" "4 5 6 7" 0 5 > "$OUT/cm.log" 2>&1 & PCM=$!
wait $PCH; wait $PCM
$PY scripts/score_ipsae.py "$OUT/chai_h" chai_h > "$OUT/chai_h.ip.log" 2>&1 || true
$PY scripts/score_ipsae.py "$OUT/chai_m" chai_m > "$OUT/chai_m.ip.log" 2>&1 || true

echo "### CROWNS: min(bh,ch)>=0.30 AND min(bm,cm)>=0.15 $(date -u +%FT%TZ)"
$PY - "$C" "$OUT" <<'PY'
import csv,sys,os
C,OUT=sys.argv[1],sys.argv[2]
def rd(p):
    d={}
    if os.path.exists(p):
        for r in csv.DictReader(open(p),delimiter='\t'):
            try:
                v=float(r['ipsae'])
                if v==v: d[r['name']]=v   # skip NaN (parse-fail) -> treat as ABSENT, not present-below-bar
            except: pass
    return d
bh=rd(f'{OUT}/boltz_h/ipsae.tsv'); bm=rd(f'{OUT}/boltz_m/ipsae.tsv')
ch=rd(f'{OUT}/chai_h/ipsae.tsv'); cm=rd(f'{OUT}/chai_m/ipsae.tsv')
seq={r['name']:r['sequence'] for r in csv.DictReader(open(C))}
rows=[]
for n in seq:
    if n not in bh and n not in ch and n not in bm and n not in cm: continue
    b_h,c_h,b_m,c_m=bh.get(n),ch.get(n),bm.get(n),cm.get(n)
    bmin=min([x for x in [b_h,c_h] if x is not None],default=0.0)
    xr=min([x for x in [b_m,c_m] if x is not None],default=0.0)
    rows.append((n,b_h,c_h,bmin,b_m,c_m,xr,(bmin>=0.30 and xr>=0.15)))
rows.sort(key=lambda r:(-int(r[7]),-r[6],-r[3]))
g=lambda x:f"{x:.3f}" if x is not None else "  -  "
with open(f'{OUT}/crown_table.tsv','w') as f:
    f.write("name\tb_h\tc_h\tBIND\tb_m\tc_m\tXR\tcrown\n")
    for n,b_h,c_h,bmin,b_m,c_m,xr,cr in rows:
        f.write(f"{n}\t{g(b_h)}\t{g(c_h)}\t{g(bmin)}\t{g(b_m)}\t{g(c_m)}\t{g(xr)}\t{int(cr)}\n")
crowns=[r for r in rows if r[7]]
w=csv.writer(open(f'{OUT}/crowns.csv','w')); w.writerow(['name','sequence'])
for r in crowns: w.writerow([r[0],seq[r[0]]])
print(f'CROWNS={len(crowns)}  (folded {len(rows)}, input {len(seq)}) -> {OUT}/crowns.csv')
for n,b_h,c_h,bmin,b_m,c_m,xr,cr in crowns:
    print(f"  CROWN {n:40} BIND={g(bmin)} XR={g(xr)}  (bh{g(b_h)} ch{g(c_h)} bm{g(b_m)} cm{g(c_m)})")
# also show the strongest near-misses (survivors that folded but missed the bar)
near=[r for r in rows if not r[7]][:12]
print('--- near-misses (top by XR then BIND) ---')
for n,b_h,c_h,bmin,b_m,c_m,xr,cr in sorted(near,key=lambda r:(-r[6],-r[3]))[:12]:
    print(f"  near  {n:40} BIND={g(bmin)} XR={g(xr)}  (bh{g(b_h)} ch{g(c_h)} bm{g(b_m)} cm{g(c_m)})")
PY
echo "CROWN_SCREEN_2STAGE_DONE $(date -u +%FT%TZ)"
