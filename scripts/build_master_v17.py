#!/usr/bin/env python3
"""Merge every v17 evidence stream into ONE master table for selection (ambition-lift, 2026-10-27).
Inputs (all optional-tolerant; prints which are missing):
  robust XR  : runs/f35/robust/robust_xr.tsv        (name,set,n,xr_mean,xr_std,xr_min,crown_rate,bind_mean)
  switch W4  : runs/f35/sel/switch_justhispka.tsv    (name..verdict,total_swing)
  switch V16 : runs/bench/switch_justhispka.tsv      (same schema; names have no V16_ prefix)
  novelty W4 : runs/f35/sel/novelty.csv              (name,singleseq_maxTM_pdb,..,verdict)
  novelty V16: runs/f35/sel/v16_novelty.csv          (same; produced by novelty_struct on v16 members)
  clusters   : runs/f35/sel/unified_div/clusters.tsv (cluster,name)  [unified single-seq TM<0.60]
  seqs       : submissions/tfr1_track2_v16.csv + runs/f35/switch/switched.csv
Objective priority: #1 switch(GENUINE) > #2 XR(robust, ties<0.05) > #3 bind. Novelty<0.90 HARD gate.
Emits runs/f35/sel/master.tsv sorted by confidence XR (xr_mean - 0.5*xr_std) and prints the gated pool.
Usage: build_master_v17.py"""
import csv, os
R="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
def tsv(p):
    return list(csv.DictReader(open(p),delimiter='\t')) if os.path.exists(p) else []
def comma(p):
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []
def norm(n): return n.replace("V16__","")

# --- sequences ---
seq={}
for r in comma(f"{R}/submissions/tfr1_track2_v16.csv"): seq[r['name']]=r['sequence'].strip()
for r in comma(f"{R}/runs/f35/switch/switched.csv"):     seq.setdefault(r['name'],r['sequence'].strip())

# --- robust XR ---
rob={}
for r in tsv(f"{R}/runs/f35/robust/robust_xr.tsv"):
    rob[norm(r['name'])]=r
if not rob: print("WARN: robust_xr.tsv missing -> run wave4_robust.sh first")

# --- switch verdicts: Wave-4 from justhispka tsv; v16 from its evidence CSV (authoritative, all 20) ---
sw={}
for r in tsv(f"{R}/runs/f35/sel/switch_justhispka.tsv"):
    sw[norm(r['name'])]=(r.get('verdict','').strip(), r.get('total_swing',''))
for r in comma(f"{R}/submissions/tfr1_track2_v16_evidence.csv"):
    sw.setdefault(norm(r['name']),(r.get('switch_verdict','').strip(), r.get('switch_swing_justhispka','')))

# --- novelty (both sets) ---
nov={}
for p in [f"{R}/runs/f35/sel/novelty.csv", f"{R}/runs/f35/sel/v16_novelty.csv"]:
    for r in comma(p):
        k=norm(r['name'])
        tm=r.get('singleseq_maxTM_pdb') or r.get('maxTM') or ''
        nov.setdefault(k,(tm, r.get('verdict','').strip()))

# --- clusters (unified) ---
clu={}
for r in tsv(f"{R}/runs/f35/sel/unified_div/clusters.tsv"):
    clu[norm(r['name'])]=r.get('cluster','')

def lineage(n):
    if n.startswith('w4'): return 'Genie3-w4'
    if n.startswith('w3'): return 'Genie3-w3'
    if n.startswith('genie_w2'): return 'Genie3-w2'
    if n.startswith('genie_w1'): return 'Genie3-w1'
    if n.startswith('rfd4'): return 'RFD4'
    if n.startswith('e22') or '_m' in n[:6]: return 'RFd1'
    return '?'

def swtier(v):
    v=v.upper()
    if 'GENUINE' in v: return 2
    if 'WEAK' in v: return 1
    return 0  # DEAD/empty

rows=[]
for n,rx in rob.items():
    xm=float(rx['xr_mean']); xs=float(rx['xr_std']); cr=float(rx['crown_rate']); bm=float(rx['bind_mean'])
    verd,swing=sw.get(n,('',''))
    tm,nvd=nov.get(n,('',''))
    tmf=float(tm) if tm not in ('',None) else None
    conf=xm-0.5*xs                      # confidence-adjusted XR (penalize unreliable)
    novel_ok = (tmf is None) or (tmf<0.90)
    genuine = swtier(verd)==2
    robust_crown = cr>=0.5
    gate = genuine and robust_crown and novel_ok
    rows.append(dict(name=n,set=rx['set'],lineage=lineage(n),xr_mean=xm,xr_std=xs,xr_min=float(rx['xr_min']),
                     crown_rate=cr,bind=bm,conf=conf,sw=verd or '-',swing=swing or '',tm=(f"{tmf:.3f}" if tmf is not None else '-'),
                     novband=nvd or '-',cluster=clu.get(n,'-'),gate=('Y' if gate else '')))
rows.sort(key=lambda r:-r['conf'])
with open(f"{R}/runs/f35/sel/master.tsv","w") as f:
    cols=['name','set','lineage','xr_mean','xr_std','xr_min','crown_rate','bind','conf','sw','swing','tm','novband','cluster','gate']
    f.write('\t'.join(cols)+'\n')
    for r in rows: f.write('\t'.join(f"{r[c]:.3f}" if isinstance(r[c],float) else str(r[c]) for c in cols)+'\n')
print(f"WROTE runs/f35/sel/master.tsv  ({len(rows)} designs; seqs available for {sum(1 for r in rows if r['name'] in seq)})")
print(f"\n{'name':32}{'set':4}{'lin':11}{'xrμ':>6}{'xrσ':>6}{'cr%':>5}{'bind':>6}{'conf':>6} {'sw':>8}{'tm':>6}{'clu':>4} gate")
for r in rows:
    print(f"{r['name']:32}{r['set']:4}{r['lineage']:11}{r['xr_mean']:6.3f}{r['xr_std']:6.3f}{r['crown_rate']*100:4.0f}%{r['bind']:6.3f}{r['conf']:6.3f} {r['sw']:>8}{r['tm']:>6}{str(r['cluster']):>4} {r['gate']}")
pool=[r for r in rows if r['gate']=='Y']
print(f"\nGATED POOL (genuine switch + robust crown + novelty<0.90): {len(pool)}")
print(f"  distinct folds in pool: {len(set(r['cluster'] for r in pool))}  | lineages: {sorted(set(r['lineage'] for r in pool))}")
