#!/usr/bin/env python3
"""Mine the FULL crown pool (f30/f31/f33) for robust crowns and compare to what v15 shipped, to find
tail-upgrade candidates the ap diversity cap may have excluded. Robust = crown AND switch frac>=0.80 AND
BIND>=0.30 AND XR>=0.15 (the frozen judge). Reports: all robust crowns ranked by XR, flagged in/out of v15,
with parent-backbone lineage so the quality-vs-diversity trade-off is explicit.
Drafted by the assistant (ambition-lift depth pass, 2026-10-27)."""
import csv, os, re
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
def ff(x):
    try: v=float(x); return v if v==v else None
    except: return None
def parent(n):  # strip switch + mpnn suffixes -> backbone lineage key
    m=re.match(r'(w3g\d+_\d+|genie_w\d+g\d+_\d+|rfd4_g\d+_\d+|e\d+)',n)
    return m.group(1) if m else n

CT={}
for p in ["runs/f30/reval6/crown_table.tsv","runs/f31/reval6/crown_table.tsv","runs/f33/robust6/crown_table.tsv"]:
    fp=f"{REPO}/{p}"
    if os.path.exists(fp):
        for r in csv.DictReader(open(fp),delimiter='\t'):
            CT.setdefault(r['name'],{'BIND':ff(r.get('BIND')),'XR':ff(r.get('XR')),'crown':r.get('crown')})
FR={}
for p in ["runs/f30/switchprob_pooled.tsv","runs/f31/switchprob_pooled.tsv","runs/f33/switchprob_pooled.tsv"]:
    fp=f"{REPO}/{p}"
    if os.path.exists(fp):
        for line in open(fp):
            q=line.split()
            if len(q)>=4 and q[0]!='design':
                try: FR[q[0]]=float(q[3])
                except: pass
NOV={}
for p in ["runs/f32/novelty.csv","runs/f33/novelty.csv"]:
    fp=f"{REPO}/{p}"
    if os.path.exists(fp):
        for r in csv.DictReader(open(fp)): NOV[r['name']]=(ff(r.get('singleseq_maxTM_pdb')),r.get('verdict'))
v15=set(r['name'] for r in csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v15.csv")))

robust=[]
for n,d in CT.items():
    if d.get('crown')!='1': continue
    fr=FR.get(n); bind=d['BIND']; xr=d['XR']
    if fr is None or bind is None or xr is None: continue
    if fr>=0.80 and bind>=0.30 and xr>=0.15:
        robust.append((n,parent(n),bind,xr,fr,NOV.get(n,(None,None))))
robust.sort(key=lambda t:-t[3])  # by XR desc

print(f"ROBUST crowns in pool (frac>=0.80, BIND>=0.30, XR>=0.15): {len(robust)}  | distinct parents: {len({r[1] for r in robust})}")
print(f"{'XR':>5} {'BIND':>5} {'frac':>4} {'nov':>5} {'in_v15':>6}  name (parent)")
print("-"*78)
seen_parent_v15={parent(n) for n in v15}
for n,par,bind,xr,fr,(nov,ver) in robust:
    inv="YES" if n in v15 else ("par*" if par in seen_parent_v15 else "NEW")
    nv=f"{nov:.2f}" if nov else "-"
    print(f"{xr:>5.3f} {bind:>5.3f} {fr:>4.2f} {nv:>5} {inv:>6}  {n}  ({par})")
# tail of v15 (weak) for reference
print("\n--- v15 weak tail (ranks 14-20) XR for comparison ---")
ev={r['name']:r for r in csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v15_evidence.csv"))}
for i,r in enumerate(csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v15.csv")),1):
    if i>=14:
        e=ev.get(r['name'],{})
        print(f"  #{i} {r['name'][:34]:34} XR={e.get('xreact_min','-'):>6} frac={e.get('switch_frac','-')}")
