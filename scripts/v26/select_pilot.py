#!/usr/bin/env python3
# Diverse cross-reactivity PILOT from the dev-screen-clean candidates: top-3 cleanest (lowest %hyd) per
# backbone, spanning all passing backbones. Keeps the fold batch small; expand only on genuine hits.
import csv, re
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
rows=list(csv.DictReader(open(f"{SC}/ms_clean.csv")))
bb={}
for r in rows:
    b=re.sub(r'_s\d+$','',r['name'].replace('ms_',''))
    bb.setdefault(b,[]).append(r)
pilot=[]
for b in sorted(bb):
    lst=sorted(bb[b], key=lambda r: float(r['pct_hyd']))[:3]   # 3 cleanest per backbone
    pilot += lst
with open(f"{SC}/ms_pilot.csv","w") as f:
    w=csv.writer(f); w.writerow(["name","sequence"])
    for r in pilot: w.writerow([r['name'], r['sequence']])
print(f"pilot: {len(pilot)} candidates across {len(bb)} backbones -> {SC}/ms_pilot.csv")
for r in pilot: print(f"  {r['name']:<28} %hyd={r['pct_hyd']} run={r['maxHydRun']} net={r['net']}")
