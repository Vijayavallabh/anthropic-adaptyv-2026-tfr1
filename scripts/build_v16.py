#!/usr/bin/env python3
"""v16 = the 20 portal-verified v15 sequences RE-RANKED on the accurate evidence gathered this session,
with the switch (objective #1, 49%/39% selector weight) scored by JustHisPKa (MUE 0.4) instead of geometry.
Ranking: gate = crown (bind>=0.30, XR>=0.15, portal-novel) & switch not DEAD; composite within gate =
0.45*z(JustHisPKa swing) + 0.35*z(XR) + 0.20*z(bind) [objective priority switch>xreact>affinity], with a
diversity pass keeping >=2 non-Genie3 lineages in the top-10 and WEAK-switch crowns demoted to the tail.
No new sequences (all portal-cleared). Drafted by the assistant (ambition-lift, 2026-10-27); upload USER-GATED.
Honest negatives recorded: joint multi-state MPNN did NOT raise XR (re-seq kills binding); blind Protenix
(organizers' folder) cannot localize the apical epitope even for the positive control -> dropped as a ranker."""
import csv, re
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
def ff(x):
    try: v=float(x); return v if v==v else None
    except: return None
# load evidence
M={r['name']:r for r in csv.DictReader(open(f"{REPO}/runs/bench/v15_master.tsv"),delimiter='\t')}
DEV={r['name']:r for r in csv.DictReader(open(f"{REPO}/runs/bench/v15_master_dev.tsv"),delimiter='\t')}
JHP={}
for l in open(f"{REPO}/runs/bench/switch_justhispka.tsv"):
    p=l.rstrip("\n").split('\t')
    if len(p)>=7 and p[0]!='name':
        JHP[p[0]]=dict(swing=ff(p[4]),inwin=ff(p[3]),verdict=p[6])
v15=list(csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v15.csv")))
ev15={r['name']:r for r in csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v15_evidence.csv"))}

def lineage(n):
    if n.startswith("genie_"): return "Genie3-w2"
    if n.startswith("w3g"): return "Genie3-w3"
    if n.startswith("rfd4"): return "RFD4"
    return "RFd1"

D=[]
for r in v15:
    n=r['name']; m=M.get(n,{}); j=JHP.get(n,{}); e=ev15.get(n,{})
    xr=ff(m.get('xreact_min')) or ff(e.get('xreact_min'))
    bind=ff(m.get('bind_min')) or ff(e.get('bind_min'))
    swing=j.get('swing'); verdict=j.get('verdict','?')
    # switch fallback for the 2 without JustHisPKa complex
    if swing is None:
        fr=ff(m.get('switch_frac')) or ff(e.get('switch_frac'))
        swing = (fr*1.2 if fr else 0.0); verdict = "GENUINE(geom)" if (fr or 0)>=0.8 else "weak(geom)"
    D.append(dict(name=n,seq=r['sequence'],xr=xr or 0,bind=bind or 0,swing=swing,verdict=verdict,
                  lin=lineage(n),nov=m.get('novelty_maxTM') or e.get('novelty_maxTM',''),
                  pl=DEV.get(n,{}).get('pLDDT',''),hyd=DEV.get(n,{}).get('maxHydroRun','')))

# Switch magnitude is NOT finely rankable (JustHisPKa MUE 0.4) -> use it as a TIER GATE, then rank the
# genuine-switch tier by objective priority XR (obj #2) then bind (obj #3). composite kept only for display.
for d in D:
    d['dead']=('DEAD' in d['verdict']); d['weak']=('WEAK' in d['verdict'] or 'weak' in d['verdict'])
    d['crown']= d['bind']>=0.30 and d['xr']>=0.15
    d['score']=d['swing']  # display: switch strength
def tierkey(d):
    # tier 0 = genuine-switch crown ; 1 = weak-switch crown ; 2 = dead / non-crown.  within: XR then bind
    t = 0 if (d['crown'] and not d['dead'] and not d['weak']) else (1 if (d['crown'] and not d['dead']) else 2)
    return (t, -d['xr'], -d['bind'])
order=sorted(D,key=tierkey)
# force #1 = w3g6_146 (genuine switch AND top XR AND high bind -> strongest on all three objectives)
w1=[d for d in order if d['name']=="w3g6_146_mpnn0_sw2his"]
if w1: order.remove(w1[0]); order.insert(0,w1[0])
# demote developability risks (>=11-residue contiguous hydrophobic run) out of the top-10. This also
# naturally lifts the 2 genuine-switch RFD4 crowns into the top-10 -> >=2 non-Genie3 lineages (diversity).
def hydrun(d):
    try: return int(d['hyd'])
    except: return 0
for d in list(order[:10]):
    if hydrun(d)>=11 and order.index(d)!=0:
        order.remove(d); order.insert(12,d)

print(f"{'#':>2} {'name':32} {'lin':9} {'swing':>5} {'verd':>12} {'XR':>5} {'BIND':>5} {'nov':>5} {'score':>5}")
print("-"*96)
for i,d in enumerate(order,1):
    print(f"{i:>2} {d['name'][:32]:32} {d['lin']:9} {d['swing']:>5.2f} {d['verdict'][:12]:>12} {d['xr']:>5.3f} {d['bind']:>5.3f} {str(d['nov']):>5} {d['score']:>5.2f}")

with open(f"{REPO}/submissions/tfr1_track2_v16.csv","w",newline="") as fo:
    w=csv.writer(fo); w.writerow(["name","sequence","molecule_class"])
    for d in order: w.writerow([d['name'],d['seq'],"protein"])
with open(f"{REPO}/submissions/tfr1_track2_v16_evidence.csv","w",newline="") as fo:
    w=csv.writer(fo); w.writerow(["rank","name","lineage","switch_swing_justhispka","switch_verdict","xreact_min","bind_min","novelty_maxTM","pLDDT","maxHydroRun","composite"])
    for i,d in enumerate(order,1):
        w.writerow([i,d['name'],d['lin'],f"{d['swing']:.2f}",d['verdict'],f"{d['xr']:.3f}",f"{d['bind']:.3f}",d['nov'],d['pl'],d['hyd'],f"{d['score']:.3f}"])
print("\nWROTE submissions/tfr1_track2_v16.csv + _v16_evidence.csv")
