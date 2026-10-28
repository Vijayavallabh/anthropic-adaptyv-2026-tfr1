#!/usr/bin/env python3
"""v21 = v20 reordered by the organizers' BLIND Protenix judge (calibrated with POS_3DS18/NEG:
on_epi invalid [scramble=1.00], iptm_max valid [POS 0.271 vs NEG 0.12]). Pure reorder, same 20
sequences, #1 LOCKED (A27HK8_A13HR44 vindicated: best both-species, ratio 0.93).

Rule (max-min of #2 cross-react + human-binding gate, respecting lexicographic priority):
  #1 locked. Ranks 2-20: GATE_PASS (blind human iptm_max >= 0.18, a natural break) above GATE_FAIL,
  each group ordered by Boltz/Chai xr_mean (the validated #2 ranker). Diversity preserved (distinct folds).
"""
import csv
from pathlib import Path
REPO = Path("/home/prachh/v/anthropic-adaptyv-2026-tfr1")
LOCK1 = "genie_w2g3_53__A27HK8_A13HR44"
GATE = 0.18

def read_tsv(p, key, col):
    d = {}
    for r in csv.DictReader(open(p), delimiter="\t"): d[r[key]] = float(r[col])
    return d

v20 = list(csv.DictReader(open(REPO/"submissions/tfr1_track2_v20.csv")))
seq = {r["name"]: r["sequence"] for r in v20}
mcls = {r["name"]: r["molecule_class"] for r in v20}
ev = {r["name"]: r for r in csv.DictReader(open(REPO/"submissions/tfr1_track2_v19_evidence.csv"))}
Hip = read_tsv(REPO/"runs/prot/v20_judge/human.tsv", "design", "iptm_max")
Mip = read_tsv(REPO/"runs/prot/v20_judge/mouse.tsv", "design", "iptm_max")
import json
try: ESM = json.load(open(REPO/"runs/esm_v21judge/plddt.json"))  # ESMFold2 monomer pLDDT (2nd organizers' folder)
except Exception: ESM = {}

def xr(nm):
    try: return float(ev[nm]["xr_mean"])
    except: return 0.0
rest = [r["name"] for r in v20 if r["name"] != LOCK1]
# group 0 = gate pass, 1 = gate fail; then by -xr
rest.sort(key=lambda nm: (0 if Hip.get(nm,0) >= GATE else 1, -xr(nm)))
order = [LOCK1] + rest

# write v21 CSV (CRLF to match portal-verified v20 format)
with open(REPO/"submissions/tfr1_track2_v21.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\r\n")
    w.writerow(["name","sequence","molecule_class"])
    for nm in order: w.writerow([nm, seq[nm], mcls[nm]])

# evidence table
with open(REPO/"submissions/tfr1_track2_v21_evidence.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["rank","name","gate","xr_mean","bind","switch","nw","H_iptm_prot","M_iptm_prot","MH_ratio","esm2_plddt","lineage"])
    for i,nm in enumerate(order,1):
        e = ev.get(nm,{}); h = Hip.get(nm,0); m = Mip.get(nm,0)
        gate = "PASS" if h>=GATE else "fail"
        ratio = f"{m/h:.2f}" if h else "-"
        w.writerow([i,nm,gate,e.get("xr_mean","-"),e.get("bind","-"),(e.get("switch_verdict","-") or "-")[:4],
                    e.get("n_inwindow","-"),f"{h:.3f}",f"{m:.3f}",ratio,f"{ESM.get(nm,0):.2f}",e.get("lineage","-")])
print("v21 order:")
for i,nm in enumerate(order,1):
    print(f"  {i:>2} {nm:34} gate={'PASS' if Hip.get(nm,0)>=GATE else 'fail'} xr={xr(nm):.3f} Hiptm={Hip.get(nm,0):.3f}")
