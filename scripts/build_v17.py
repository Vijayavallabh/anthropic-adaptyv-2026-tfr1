#!/usr/bin/env python3
"""Assemble v17 from the robust master table (ambition-lift, 2026-10-27). Honest, robust-stats selection:
objective #1 switch(GENUINE) is a hard gate; within genuine robust crowns, rank by confidence-adjusted XR
(mean - 0.5*std, from n>=2 same-pipeline DIFF=6 folds); enforce TM<0.60 fold distinctness (one design per
cluster), one His-variant per backbone parent, and protect generator-lineage diversity (RFD4 kept). Ship a
ranked 20 (row order = ranking; front-load the highest-confidence genuine crowns). v16 members are already
portal-cleared; NEW Wave-4 members are flagged for a portal novelty check before upload.
Usage: build_v17.py [--out submissions/tfr1_track2_v17.csv]  (reads runs/f35/sel/master.tsv + clusters)"""
import csv, sys, os
R="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
OUT = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else f"{R}/submissions/tfr1_track2_v17.csv"

def parent(n):  # strip His-variant suffix so sw2his/sw3his of one backbone dedupe
    for suf in ("_sw2his","_sw3his","_sw2b","_sw3b"):
        if n.endswith(suf): return n[:-len(suf)]
    import re
    return re.sub(r'_sw\dhis.*$|__A\d.*$','',n)

master=list(csv.DictReader(open(f"{R}/runs/f35/sel/master.tsv"),delimiter='\t'))
seq={}
for r in csv.DictReader(open(f"{R}/submissions/tfr1_track2_v16.csv")): seq[r['name']]=r['sequence'].strip()
for r in csv.DictReader(open(f"{R}/runs/f35/switch/switched.csv")):     seq.setdefault(r['name'],r['sequence'].strip())

for r in master:
    r['conf']=float(r['conf']); r['xr_mean']=float(r['xr_mean']); r['xr_std']=float(r['xr_std'])
    r['bind']=float(r['bind']); r['crown_rate']=float(r['crown_rate'])
    # novelty-certainty tie-break for the hard-gated, front-loaded ranking: within the XR noise band a
    # portal-CERTAIN design should outrank a novelty-UNCERTAIN one (a design that fails novelty delivers 0).
    # tiers: v16 members = portal-cleared (v15); Wave-4 <0.80 = local-safe; 0.80-0.90 = borderline.
    try: tm=float(r['tm'])
    except: tm=None
    pen = 0.0
    if r['set']=='W4' and tm is not None and 0.80<=tm<0.90: pen=0.04   # borderline novelty -> demote within noise
    r['rankscore']=r['conf']-pen
master.sort(key=lambda r:-r['rankscore'])

# pool: genuine switch + robust crown + novelty<0.90 (gate=='Y')
pool=[r for r in master if r['gate']=='Y']

sel=[]; used_parent=set(); used_cluster=set(); lin_count={}
def try_add(r, allow_dupcluster=False):
    p=parent(r['name']); c=r['cluster']
    if p in used_parent: return False
    if not allow_dupcluster and c!='-' and c in used_cluster: return False
    sel.append(r); used_parent.add(p)
    if c!='-': used_cluster.add(c)
    lin_count[r['lineage']]=lin_count.get(r['lineage'],0)+1
    return True

# pass 1: greedy by confidence, distinct folds + distinct parents
for r in pool:
    if len(sel)>=20: break
    try_add(r)

# lineage protection: ensure >=1 RFD4 and >=1 Genie3-w2 in the set (generator diversity) if available & not present
def ensure_lineage(lin):
    if any(s['lineage']==lin for s in sel): return
    for r in pool:
        if r['lineage']==lin and parent(r['name']) not in used_parent and r['cluster'] not in used_cluster:
            # replace the weakest-conf current member of the most-represented lineage
            heavy=max(lin_count,key=lin_count.get)
            victims=[s for s in sel if s['lineage']==heavy]
            if victims:
                v=min(victims,key=lambda s:s['conf']); sel.remove(v)
                used_parent.discard(parent(v['name'])); used_cluster.discard(v['cluster']); lin_count[heavy]-=1
                try_add(r); return
for lin in ('RFD4','Genie3-w2'): ensure_lineage(lin)

# fill to 20 if short (diversity exhausted pool): allow same-cluster genuine crowns, then non-gated genuine
if len(sel)<20:
    for r in pool+ [m for m in master if m['gate']!='Y' and 'GENUINE' in m['sw'].upper()]:
        if len(sel)>=20: break
        try_add(r, allow_dupcluster=True)

sel=sel[:20]
# fail-loud: never silently emit a short/empty submission (e.g. from an empty master.tsv)
assert len(sel)==20, f"build_v17: selected {len(sel)} designs, expected 20 — check runs/f35/sel/master.tsv is populated"
sel.sort(key=lambda r:-r['rankscore'])  # final row order = confidence XR with novelty-certainty tie-break

# write v17 + evidence
with open(OUT,"w",newline="") as f:
    w=csv.writer(f); w.writerow(["name","sequence","molecule_class"])
    for r in sel:
        s=seq.get(r['name'])
        assert s and s.isalpha(), f"missing/bad seq for {r['name']}"
        w.writerow([r['name'], s, "protein"])
ev=OUT.replace(".csv","_evidence.csv")
with open(ev,"w",newline="") as f:
    w=csv.writer(f); w.writerow(["rank","name","set","lineage","xr_mean","xr_std","crown_rate","bind","conf","switch","novelty_tm","cluster","portal"])
    for i,r in enumerate(sel,1):
        portal="cleared(v15)" if r['set']=='V16' else "CHECK"
        w.writerow([i,r['name'],r['set'],r['lineage'],f"{r['xr_mean']:.3f}",f"{r['xr_std']:.3f}",f"{r['crown_rate']:.2f}",
                    f"{r['bind']:.3f}",f"{r['conf']:.3f}",r['sw'],r['tm'],r['cluster'],portal])

# report
v16names={r['name'] for r in csv.DictReader(open(f"{R}/submissions/tfr1_track2_v16.csv"))}
selnames={r['name'] for r in sel}
print(f"=== v17: {len(sel)} designs -> {OUT} ===")
print(f"{'#':>2} {'name':32}{'set':4}{'lin':11}{'xrμ':>6}{'σ':>6}{'bind':>6} {'sw':>8}{'tm':>6}{'clu':>4}")
for i,r in enumerate(sel,1):
    tag=' NEW' if r['name'] not in v16names else ''
    print(f"{i:2} {r['name']:32}{r['set']:4}{r['lineage']:11}{r['xr_mean']:6.3f}{r['xr_std']:6.3f}{r['bind']:6.3f} {r['sw']:>8}{r['tm']:>6}{str(r['cluster']):>4}{tag}")
newc=len(selnames-v16names); dropped=v16names-selnames
print(f"\nNEW vs v16: {newc} added | {len(dropped)} dropped: {sorted(dropped)}")
print(f"lineages: {lin_count} | distinct folds: {len(set(r['cluster'] for r in sel if r['cluster']!='-'))}")
print(f"portal-CHECK (new Wave-4) rows: {sum(1 for r in sel if r['set']=='W4')}")
