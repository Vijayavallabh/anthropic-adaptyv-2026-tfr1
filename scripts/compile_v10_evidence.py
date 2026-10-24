#!/usr/bin/env python3
"""Compile the v10 evidence table: per design pull switch (fold-count or replicate frac), binding
(fragment ipSAE_min over Boltz+Chai), x-react (mouse fragment ipSAE_min), hydropathy, novelty.
Sources differ by design group (current-20 = runs/f17; pool = runs/f18/pool{A,B}_*). Output: runs/f18/v10_evidence.csv
"""
import csv, glob, os, re
R="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
KD={'A':1.8,'R':-4.5,'N':-3.5,'D':-3.5,'C':2.5,'Q':-3.5,'E':-3.5,'G':-0.4,'H':-3.2,'I':4.5,'L':3.8,
    'K':-3.9,'M':1.9,'F':2.8,'P':-1.6,'S':-0.8,'T':-0.7,'W':-0.9,'Y':-1.3,'V':4.2}
def hyd(s): return round(sum(KD.get(c,0) for c in s)/len(s),2)
def ipsae(path):
    d={}
    if os.path.exists(path):
        for r in csv.DictReader(open(path),delimiter="\t"):
            try: d[r["name"]]=float(r["ipsae"])
            except: pass
    return d
def switchcount(dirs, name):   # fraction of folds with total>=2
    n=v=0
    for p in dirs:
        if os.path.exists(p):
            for r in csv.DictReader(open(p),delimiter="\t"):
                k=r.get("design") or r.get("combo")
                if k==name:
                    try:
                        n+=1; v+= (int(r["total"])>=2)
                    except: pass
    return (v,n)

# current-20 fragment data (f17)
f17bh,f17ch=ipsae(f"{R}/runs/f17/boltz_h/ipsae.tsv"),ipsae(f"{R}/runs/f17/chai_h/ipsae.tsv")
f17bm,f17cm=ipsae(f"{R}/runs/f17/boltz_m/ipsae.tsv"),ipsae(f"{R}/runs/f17/chai_m/ipsae.tsv")
f17sw=[f"{R}/runs/f17/switch_h.tsv",f"{R}/runs/f17/switch_m.tsv",f"{R}/runs/f17/switch_ch.tsv",f"{R}/runs/f17/switch_cm.tsv"]
# pool final data
pAh,pAch=ipsae(f"{R}/runs/f18/poolA_final/boltz_h/ipsae.tsv"),ipsae(f"{R}/runs/f18/poolA_final/chai_h/ipsae.tsv")
pAm=ipsae(f"{R}/runs/f18/poolA_final/boltz_m/ipsae.tsv")
pBh,pBch=ipsae(f"{R}/runs/f18/poolB_final/boltz_h/ipsae.tsv"),ipsae(f"{R}/runs/f18/poolB_final/chai_h/ipsae.tsv")
pBm=ipsae(f"{R}/runs/f18/poolB_final/boltz_m/ipsae.tsv")
nov={}
for p in [f"{R}/runs/f18/poolA_final/novelty.csv",f"{R}/runs/f18/poolB_final/novelty.csv"]:
    if os.path.exists(p):
        for r in csv.DictReader(open(p)): nov[r["name"]]=r["singleseq_maxTM_pdb"]
# map v10 pool clean-name -> (combo-name, group)
POOL={"rfd4_g2_138_sw2b_A14_A52":("g2_138__A52HR51_A14HK16","A"),"rfd4_g4_66_sw2b_A25_A41":("g4_66__A41HK11_A25HK28","A"),
      "rfd4_g1_133_sw2b_A10_A20":("g1_133__A20HK45_A10HK14","A"),"rfd4_g5_120_sw2b_A53_A61":("g5_120__A61HK24_A53HR57","B"),
      "rfd4_g6_72_sw2b_A11_A18":("g6_72__A18HR56_A11HR64","B"),"rfd4_g1_69_sw2b_A27_A64":("g1_69__A27HR5_A64HK68","B"),
      "rfd4_g1_76_sw2b_A24_A43":("g1_76__A24HR20_A43HK49","B"),"rfd4_g4_93_sw2b_A38_A48":("g4_93__A38HK47_A48HK69","B")}
CROWN2={"rfd4_g5_14_sw2b_A34_A50":(0.382,0.185,"4/4",0.737)}  # measured in f17 crown validation
v10=list(csv.DictReader(open(f"{R}/submissions/tfr1_track2_v10.csv")))
def mn(*xs):
    xs=[x for x in xs if x is not None]
    return round(min(xs),3) if xs else None
out=[]
for i,row in enumerate(v10,1):
    n=row["name"]; s=row["sequence"]
    if n in CROWN2:
        b,x,sw,nv=CROWN2[n]; src="RFD4"; portal="re-check"
    elif n in POOL:
        cn,grp=POOL[n]; (bh,ch,bm)=((pAh,pAch,pAm) if grp=="A" else (pBh,pBch,pBm))
        b=mn(bh.get(cn),ch.get(cn)); x=mn(bm.get(cn)); sw="robust"; nv=nov.get(cn,"?"); src="RFD4"; portal="re-check"
    else:
        b=mn(f17bh.get(n),f17ch.get(n)); x=mn(f17bm.get(n),f17cm.get(n))
        v,nf=switchcount(f17sw,n); sw=f"{v}/{nf}" if nf else "-"; nv="(v6:pass)"; src=("RFd1" if n[0] in "de" else "RFD4"); portal="verified(v6)"
    out.append(dict(rank=i,name=n,source=src,switch=sw,bind_min=b,xreact_min=x,hydro=hyd(s),novelty=nv,portal=portal))
with open(f"{R}/runs/f18/v10_evidence.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["rank","name","source","switch","bind_min","xreact_min","hydro","novelty","portal"]); w.writeheader(); w.writerows(out)
print(f"{'#':>2} {'name':26} {'src':4} {'switch':7} {'bind':>5} {'xreact':>6} {'hyd':>5} {'nov':>8} portal")
for o in out:
    print(f"{o['rank']:>2} {o['name']:26} {o['source']:4} {str(o['switch']):7} {str(o['bind_min']):>5} {str(o['xreact_min']):>6} {str(o['hydro']):>5} {str(o['novelty']):>8} {o['portal']}")
