#!/bin/bash
# Robust XR estimate (ambition-lift, 2026-10-27): the DIFF=6 pipeline is reproducible (~0.03) but a few
# designs are high-variance and v16's evidence XR did not reproduce. Fold the SAME combined set (20 v16 +
# 19 Wave-4, runs/f35/batchcmp/combined.csv) 3 MORE times with independent Chai seeds (1,2,3), then pool
# with the existing batchcmp (seed 0) -> n=4 same-pipeline DIFF=6 samples per design. Rank by MEAN XR with
# variance flagged (differences < ~0.08 are noise; high std = unreliable). All 8 GPUs, sequential batches.
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
C=runs/f35/batchcmp/combined.csv
mkdir -p runs/f35/robust
for s in 1 2 3; do
  BUSY=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | wc -l)
  [ "$BUSY" -eq 0 ] || { echo "ABORT seed $s: $BUSY foreign GPU procs"; exit 1; }
  echo "[robust $(date -u +%FT%TZ)] batch seed=$s -> runs/f35/robust/s$s"
  bash scripts/wave4_rescreen.sh "$C" "runs/f35/robust/s$s" 6 "$s" > "runs/f35/robust/s$s.drive.log" 2>&1
done
echo "[robust] pooling n=4 (batchcmp seed0 + s1 + s2 + s3)"
$PY - <<'PY'
import csv,glob,os,statistics as st
batches={'s0':'runs/f35/batchcmp/rescore/rescreen_table.tsv',
         's1':'runs/f35/robust/s1/rescreen_table.tsv',
         's2':'runs/f35/robust/s2/rescreen_table.tsv',
         's3':'runs/f35/robust/s3/rescreen_table.tsv'}
data={}  # name -> {'xr':[...], 'bind':[...]}
for tag,p in batches.items():
    if not os.path.exists(p): print("MISSING",p); continue
    for r in csv.DictReader(open(p),delimiter='\t'):
        n=r['name'].replace('V16__','')
        try: xr=float(r['XR']); b=float(r['BIND'])
        except: continue
        d=data.setdefault(n,{'xr':[],'bind':[]}); d['xr'].append(xr); d['bind'].append(b)
out=open('runs/f35/robust/robust_xr.tsv','w')
out.write("name\tset\tn\txr_mean\txr_std\txr_min\tcrown_rate\tbind_mean\n")
rows=[]
for n,d in data.items():
    xr=d['xr']; b=d['bind']
    mean=st.mean(xr); sd=st.pstdev(xr) if len(xr)>1 else 0.0
    cr=sum(1 for i in range(len(xr)) if xr[i]>=0.15 and b[i]>=0.30)/len(xr)
    s='W4' if n.startswith('w4') else 'V16'
    rows.append((n,s,len(xr),mean,sd,min(xr),cr,st.mean(b)))
for r in sorted(rows,key=lambda r:-r[3]):
    out.write("\t".join(str(x) if not isinstance(x,float) else f"{x:.3f}" for x in r)+"\n")
out.close()
print("WROTE runs/f35/robust/robust_xr.tsv")
print(f"{'name':32}{'set':4}{'n':>2} {'mean':>6}{'std':>6}{'min':>6} {'crown%':>7} {'bind':>6}")
for r in sorted(rows,key=lambda r:-r[3]):
    print(f"{r[0]:32}{r[1]:4}{r[2]:>2} {r[3]:6.3f}{r[4]:6.3f}{r[5]:6.3f} {r[6]*100:6.0f}% {r[7]:6.3f}")
PY
echo "WAVE4_ROBUST_DONE $(date -u +%FT%TZ)"
