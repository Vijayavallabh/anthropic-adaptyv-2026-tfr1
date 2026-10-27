#!/bin/bash
# F38 moonshot robust re-fold (2026-10-27 ambition-lift "non-mimetic moonshots"): fold top.csv with 2 extra
# independent seeds and pool with the seed-0 rescreen -> n=3 robust XR per candidate (same DIFF=6 pocket-
# restrained dual-folder pipeline as the frozen pool). Usage: f38_robust.sh <top.csv> [base_dir=runs/f38_moon]
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
TOP="${1:?top.csv name,sequence}"; BASE="${2:-runs/f38_moon}"
for s in 1 2; do
  BUSY=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | wc -l)
  [ "$BUSY" -eq 0 ] || { echo "ABORT seed $s: $BUSY foreign GPU procs"; exit 1; }
  echo "[f38-robust $(date -u +%FT%TZ)] seed=$s -> $BASE/s$s"
  bash scripts/wave4_rescreen.sh "$TOP" "$BASE/s$s" 6 "$s" > "$BASE/s$s.drive.log" 2>&1
done
$PY - "$BASE" <<'PY'
import csv,os,sys,statistics as st
BASE=sys.argv[1]
tabs={'s0':f'{BASE}/rescreen/rescreen_table.tsv','s1':f'{BASE}/s1/rescreen_table.tsv','s2':f'{BASE}/s2/rescreen_table.tsv'}
data={}
for tag,p in tabs.items():
    if not os.path.exists(p): print("MISSING",p); continue
    for r in csv.DictReader(open(p),delimiter='\t'):
        try: xr=float(r['XR']); b=float(r['BIND'])
        except: continue
        d=data.setdefault(r['name'],{'xr':[],'b':[]}); d['xr'].append(xr); d['b'].append(b)
rows=[]
for n,d in data.items():
    xr=d['xr']; b=d['b']
    rows.append((n,len(xr),st.mean(xr),st.pstdev(xr) if len(xr)>1 else 0.0,min(xr),st.mean(b),
                 sum(1 for i in range(len(xr)) if xr[i]>=0.15 and b[i]>=0.30)/len(xr)))
rows.sort(key=lambda r:-r[2])
with open(f'{BASE}/robust_xr.tsv','w') as out:
    out.write("name\tn\txr_mean\txr_std\txr_min\tbind_mean\tcrown_rate\n")
    for r in rows: out.write("\t".join(f"{x:.3f}" if isinstance(x,float) else str(x) for x in r)+"\n")
print("WROTE",f'{BASE}/robust_xr.tsv')
for r in rows[:15]: print(f"  {r[0]:38} n={r[1]} xr {r[2]:.3f}+/-{r[3]:.3f} min {r[4]:.3f} bind {r[5]:.3f} crown {r[6]*100:.0f}%")
PY
echo "F38_ROBUST_DONE $(date -u +%FT%TZ)"
