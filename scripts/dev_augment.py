#!/usr/bin/env python3
"""Augment the v15 master table with developability axes: ESMFold monomer mean-pLDDT (best de-novo
success predictor per Garcia/Rocklin 2026) where a monomer exists, plus pure-sequence expression-risk
flags (longest contiguous hydrophobic run, Cys count, longest poly-X run, net charge, charged frac).
Output: runs/bench/v15_master_dev.tsv. Drafted by the assistant (ambition-lift depth pass, 2026-10-27)."""
import csv, glob, os
from pathlib import Path
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
HYD=set("AILMFWVYC")
def ca_plddt(pdb):
    vals=[]
    for ln in open(pdb):
        if ln.startswith("ATOM") and ln[12:16].strip()=="CA":
            try: vals.append(float(ln[60:66]))
            except: pass
    return round(sum(vals)/len(vals),1) if vals else None
def find_monomer(name):
    for p in glob.glob(f"{REPO}/runs/**/esmfold/{name}.pdb", recursive=True):
        return p
    return None
def maxrun(seq, charset=None):
    best=cur=0; prev=None
    for c in seq:
        inrun = (c in charset) if charset else (c==prev)
        cur = cur+1 if inrun else (1 if charset and c in charset else (1 if not charset else 0))
        if not charset:
            cur = cur+1 if c==prev else 1
        best=max(best,cur); prev=c
    return best
def max_poly(seq):
    best=cur=1
    for i in range(1,len(seq)):
        cur = cur+1 if seq[i]==seq[i-1] else 1; best=max(best,cur)
    return best if seq else 0
def max_hydro(seq):
    best=cur=0
    for c in seq:
        cur = cur+1 if c in HYD else 0; best=max(best,cur)
    return best

master={r['name']:r for r in csv.DictReader(open(f"{REPO}/runs/bench/v15_master.tsv"),delimiter='\t')}
rows=list(csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v15.csv")))
cols=["rank","name","len","bind_min","xreact_min","switch_frac","novelty_maxTM","GRAVY",
      "pLDDT","maxHydroRun","maxPolyRun","nCys","netCharge","fracCharged"]
out=[]
for i,r in enumerate(rows,1):
    n=r['name']; seq=r['sequence']; m=master.get(n,{})
    mono=find_monomer(n); pl=ca_plddt(mono) if mono else None
    net=sum(seq.count(x) for x in "KR")-sum(seq.count(x) for x in "DE")
    chg=round(sum(seq.count(x) for x in "KRDE")/len(seq),2)
    out.append([i,n,len(seq),m.get('bind_min',''),m.get('xreact_min',''),m.get('switch_frac',''),
                m.get('novelty_maxTM',''),m.get('GRAVY',''),pl if pl is not None else '',
                max_hydro(seq),max_poly(seq),seq.count('C'),net,chg])
with open(f"{REPO}/runs/bench/v15_master_dev.tsv","w",newline="") as fo:
    w=csv.writer(fo,delimiter='\t'); w.writerow(cols); w.writerows(out)
print("WROTE runs/bench/v15_master_dev.tsv\n")
hdr=f"{'#':>2} {'name':34} {'len':>3} {'pLDDT':>5} {'hydro':>5} {'poly':>4} {'Cys':>3} {'netQ':>4} {'fQ':>4} {'GRAVY':>6}"
print(hdr); print("-"*len(hdr))
for r in out:
    pl = f"{r[8]}" if r[8]!='' else '-'
    print(f"{r[0]:>2} {r[1][:34]:34} {r[2]:>3} {pl:>5} {r[9]:>5} {r[10]:>4} {r[11]:>3} {r[12]:>+4} {r[13]:>4} {str(r[7]):>6}")
