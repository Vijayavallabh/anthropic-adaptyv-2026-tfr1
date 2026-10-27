#!/usr/bin/env python3
"""Build submissions/tfr1_track2_v15.csv + _v15_evidence.csv (20, row order = ranking, molecule_class=protein).
Merges robust crown tables + switch genuineness + novelty + sequences across all waves (f30 batch-1+v13,
f31 rescues, f33 tier-2, v13). Top-15 = qualified novel crowns; 16-20 complete the 20 with 2 more Genie3
crowns + RFD4/RFd1 method-diversity hedges. #1 leads with a COMFORTABLY-novel crown (novelty-safety on top-1)."""
import csv, os, re

REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
V15 = [
 ("w3g5_70_mpnn1_sw3his",            "Genie3-w3",  "CROWN"),
 ("w3g6_146_mpnn0_sw2his",           "Genie3-w3",  "CROWN (borderline-novelty)"),
 ("genie_w2g3_53_sw2b",              "Genie3",     "CROWN"),
 ("w3g2_70_mpnn1_sw2his",            "Genie3-w3",  "CROWN (borderline-novelty)"),
 ("genie_w2g6_144_sw3b",             "Genie3",     "CROWN"),
 ("w3g7_240_mpnn1_sw3his",           "Genie3-w3",  "CROWN"),
 ("w3g5_231_mpnn1_sw3his",           "Genie3-w3",  "CROWN"),
 ("w3g6_93_mpnn1_sw2his",            "Genie3-w3",  "CROWN (borderline-novelty)"),
 ("w3g7_6_mpnn0_sw3his",             "Genie3-w3",  "CROWN (borderline-novelty)"),
 ("w3g0_290_mpnn1_sw2his",           "Genie3-w3",  "CROWN"),
 ("rfd4_g5_14_sw2b_A34_A50",         "RFD4",       "CROWN (method-diversity)"),
 ("w3g5_249_mpnn0__A13HK16_A42HK69", "Genie3-w3",  "CROWN"),
 ("genie_w2g5_111_sw2b",             "Genie3",     "CROWN"),
 ("w3g5_264_mpnn1_sw2his",           "Genie3-w3",  "CROWN (moderate-switch)"),
 ("w3g2_225_mpnn0_sw3his",           "Genie3-w3",  "CROWN (borderline-novelty)"),
 ("genie_w1g0_112_sw2b",             "Genie3",     "crown (weak-switch)"),
 ("w3g0_218_mpnn1_sw2his",           "Genie3-w3",  "crown (weak-switch)"),
 ("rfd4_g7_8_sw2b_A14_A41",          "RFD4",       "crown/method-diversity"),
 ("rfd4_g1_133_sw2b_A10_A20",        "RFD4",       "near-crown/method-diversity"),
 ("e223_m3_sw3his",                  "RFd1",       "switch/lineage-diversity"),
]

def ff(x):
    try: v=float(x); return v if v==v else None
    except: return None

CT={}
for p in [f"{REPO}/runs/f30/reval6/crown_table.tsv", f"{REPO}/runs/f31/reval6/crown_table.tsv", f"{REPO}/runs/f33/robust6/crown_table.tsv"]:
    if os.path.exists(p):
        for r in csv.DictReader(open(p),delimiter='\t'):
            CT[r['name']]={'bind':ff(r['BIND']),'xr':ff(r['XR'])}
FR={}
for p in [f"{REPO}/runs/f30/switchprob_pooled.tsv", f"{REPO}/runs/f31/switchprob_pooled.tsv", f"{REPO}/runs/f33/switchprob_pooled.tsv"]:
    if os.path.exists(p):
        for line in open(p):
            q=line.split()
            if len(q)>=4 and q[0]!='design':
                try: FR[q[0]]=float(q[3])
                except: pass
NOV={}
for p in [f"{REPO}/runs/f32/novelty.csv", f"{REPO}/runs/f33/novelty.csv"]:
    if os.path.exists(p):
        for r in csv.DictReader(open(p)): NOV[r['name']]=(r['singleseq_maxTM_pdb'], r['verdict'])
SEQ={}
for p in [f"{REPO}/runs/f29/combined_crowns.csv", f"{REPO}/runs/f31/exhaustive_all.csv",
          f"{REPO}/runs/f33/switch/reval/crowns.csv", f"{REPO}/submissions/tfr1_track2_v13.csv"]:
    if os.path.exists(p):
        for r in csv.DictReader(open(p)): SEQ.setdefault(r['name'], r['sequence'])
V13EV={r['name']:r for r in csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v13_evidence.csv"))}

miss=[n for n,_,_ in V15 if n not in SEQ]
assert not miss, f"MISSING SEQUENCES: {miss}"

with open(f"{REPO}/submissions/tfr1_track2_v15.csv","w",newline="") as fo:
    w=csv.writer(fo); w.writerow(["name","sequence","molecule_class"])
    for n,_,_ in V15: w.writerow([n, SEQ[n], "protein"])

with open(f"{REPO}/submissions/tfr1_track2_v15_evidence.csv","w",newline="") as fo:
    w=csv.writer(fo); w.writerow(["rank","name","lineage","role","bind_min","xreact_min","switch_frac","novelty_maxTM","novelty_verdict","len","source"])
    for i,(n,lin,role) in enumerate(V15,1):
        ct=CT.get(n,{}); bind=ct.get('bind'); xr=ct.get('xr'); fr=FR.get(n)
        nov,verdict=NOV.get(n,("",""))
        src="robust-refold" if n in CT else "v13-validated"
        if bind is None and n in V13EV:
            bind=ff(V13EV[n].get('bind_min')); xr=ff(V13EV[n].get('xreact_min')); src="v13-validated"
            if not verdict: verdict="v13-portal-novel"
        g=lambda x: (f"{x:.3f}" if isinstance(x,float) else (x or ""))
        w.writerow([i,n,lin,role,g(bind),g(xr),(f"{fr:.2f}" if fr is not None else ""),nov,verdict,len(SEQ[n]),src])

from collections import Counter
print("WROTE submissions/tfr1_track2_v15.csv (20) + _v15_evidence.csv")
print("lineage mix:", dict(Counter(l for _,l,_ in V15)))
