#!/usr/bin/env python3
"""Assemble submissions/tfr1_track2_v14.csv + _v14_evidence.csv from the robust (Prong C) + rescue +
novelty data. Row order = ranking. molecule_class=protein (matches v13). Sequences pulled from the
combined pool, the exhaustive-rescue pool, and v13 (for method/lineage-hedge tail designs)."""
import csv, math, os

REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
# ordered (rank) list: (name, lineage, role)
V14 = [
 ("w3g6_146_mpnn0_sw2his",          "Genie3-w3", "CROWN"),
 ("genie_w2g3_53_sw2b",             "Genie3",    "CROWN"),
 ("w3g6_59_mpnn1__A60HK44_A31HR72", "Genie3-w3", "CROWN"),
 ("genie_w2g6_144_sw3b",            "Genie3",    "CROWN"),
 ("w3g5_231_mpnn1_sw3his",          "Genie3-w3", "CROWN"),
 ("w3g5_263_mpnn0__A35HK56_A41HK26","Genie3-w3", "CROWN"),
 ("w3g0_290_mpnn1_sw2his",          "Genie3-w3", "CROWN"),
 ("rfd4_g5_14_sw2b_A34_A50",        "RFD4",      "CROWN"),
 ("w3g5_249_mpnn0__A13HK16_A42HK69","Genie3-w3", "CROWN"),
 ("genie_w2g5_111_sw2b",            "Genie3",    "CROWN"),
 ("w3g2_186_mpnn0__A13HK17_A62HK87","Genie3-w3", "CROWN"),
 ("w3g2_225_mpnn0_sw3his",          "Genie3-w3", "CROWN"),
 ("rfd4_g1_133_sw2b_A10_A20",       "RFD4",      "near-crown/method-hedge"),
 ("w3g6_87_mpnn0_sw2his",           "Genie3-w3", "near-crown"),
 ("d25_sw2b_A9_A25",                "RFd1",      "method-hedge"),
 ("rfd4_g7_8_sw2b_A14_A41",         "RFD4",      "method-hedge"),
 ("e223_m3_sw3his",                 "RFd1",      "lineage-hedge/switch"),
 ("d374_m7_sw3his",                 "RFd1",      "lineage-hedge/switch"),
 ("rfd4_g4_5_sw3his",               "RFD4",      "lineage-hedge/switch"),
 ("d4_m5_sw2his",                   "RFd1",      "lineage-hedge/switch"),
]

def rd_ct(p, d):
    if not os.path.exists(p): return
    for r in csv.DictReader(open(p), delimiter='\t'):
        def f(x):
            try: v=float(x); return v if v==v else None
            except: return None
        d[r['name']]={'bind':f(r['BIND']),'xr':f(r['XR'])}

def rd_frac(p, d):
    if not os.path.exists(p): return
    for line in open(p):
        q=line.split()
        if len(q)<4 or q[0]=='design': continue
        try: d[q[0]]=float(q[3])
        except: pass

# sequence lookup from all sources
SEQ={}
for p in [f"{REPO}/submissions/tfr1_track2_v13.csv", f"{REPO}/runs/f29/combined_crowns.csv", f"{REPO}/runs/f31/exhaustive_all.csv"]:
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            SEQ.setdefault(r['name'], r['sequence'])
# robust metrics (Prong C f30 + rescue f31)
CT={}; rd_ct(f"{REPO}/runs/f30/reval6/crown_table.tsv", CT); rd_ct(f"{REPO}/runs/f31/reval6/crown_table.tsv", CT)
FR={}; rd_frac(f"{REPO}/runs/f30/switchprob_pooled.tsv", FR); rd_frac(f"{REPO}/runs/f31/switchprob_pooled.tsv", FR)
# novelty (new designs) + v13 evidence (old)
NOV={}
if os.path.exists(f"{REPO}/runs/f32/novelty.csv"):
    for r in csv.DictReader(open(f"{REPO}/runs/f32/novelty.csv")):
        NOV[r['name']]=(r['singleseq_maxTM_pdb'], r['verdict'])
V13EV={}
for r in csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v13_evidence.csv")):
    V13EV[r['name']]=r

miss=[n for n,_,_ in V14 if n not in SEQ]
assert not miss, f"MISSING SEQUENCES: {miss}"

# write submission csv
with open(f"{REPO}/submissions/tfr1_track2_v14.csv","w",newline="") as fo:
    w=csv.writer(fo); w.writerow(["name","sequence","molecule_class"])
    for n,_,_ in V14: w.writerow([n, SEQ[n], "protein"])

# write evidence
with open(f"{REPO}/submissions/tfr1_track2_v14_evidence.csv","w",newline="") as fo:
    w=csv.writer(fo); w.writerow(["rank","name","lineage","role","bind_min","xreact_min","switch_frac","novelty_maxTM","novelty_verdict","len","source"])
    for i,(n,lin,role) in enumerate(V14,1):
        ct=CT.get(n,{}); bind=ct.get('bind'); xr=ct.get('xr'); fr=FR.get(n)
        nov,verdict=NOV.get(n,("",""))
        src="robust-refold" if n in CT else "v13-validated"
        # fall back to v13 evidence for tail designs not re-folded
        if bind is None and n in V13EV:
            bind=V13EV[n].get('bind_min'); xr=V13EV[n].get('xreact_min'); src="v13-validated"
            if not verdict: verdict="v13-portal-novel"
        g=lambda x: (f"{x:.3f}" if isinstance(x,float) else (x or ""))
        w.writerow([i,n,lin,role,g(bind),g(xr),(f"{fr:.2f}" if fr is not None else ""),nov,verdict,len(SEQ[n]),src])

print("WROTE submissions/tfr1_track2_v14.csv (20) + _v14_evidence.csv")
# quick mix summary
from collections import Counter
c=Counter(l for _,l,_ in V14)
print("lineage mix:", dict(c))
