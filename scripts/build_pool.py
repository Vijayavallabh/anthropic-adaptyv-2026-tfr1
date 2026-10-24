#!/usr/bin/env python3
"""Consolidate the full candidate pool (RFD4 f16 + RFd1 f12 + current submission) into one master table
with novelty (singleseq maxTM) + Kyte-Doolittle mean hydropathy (an organizer screen) + length.
Filters: length 60-140, novel (0 < maxTM < 0.80). Output: runs/f18/pool_master.csv
"""
import csv, glob, os

KD = {'A':1.8,'R':-4.5,'N':-3.5,'D':-3.5,'C':2.5,'Q':-3.5,'E':-3.5,'G':-0.4,'H':-3.2,'I':4.5,
      'L':3.8,'K':-3.9,'M':1.9,'F':2.8,'P':-1.6,'S':-0.8,'T':-0.7,'W':-0.9,'Y':-1.3,'V':4.2}
def hydropathy(s): return sum(KD.get(c,0) for c in s)/len(s) if s else 0.0

REPO = "/home/prachh/v/anthropic-adaptyv-2026-tfr1"
seqs = {}
seq_sources = [
    ("RFD4", f"{REPO}/runs/f16/wave_seqs.csv"),
    *[("RFD4", p) for p in glob.glob(f"{REPO}/runs/f16/w2_nov_sh*.csv") if ".out." not in p],
    *[("RFD4", p) for p in glob.glob(f"{REPO}/runs/f16/nov_sh*.csv") if ".out." not in p],
    ("RFd1", f"{REPO}/runs/f12/chai/long2_surv.csv"),
    ("RFd1", f"{REPO}/runs/f12/chai/long1r_surv.csv"),
    ("RFd1", f"{REPO}/runs/f12/pocket/passers_seqs.csv"),
]
src = {}
for tag, p in seq_sources:
    if not os.path.exists(p): continue
    for r in csv.DictReader(open(p)):
        s = (r.get("sequence") or r.get("seq") or "").strip()
        n = r["name"]
        if s and n not in seqs:
            seqs[n] = s; src[n] = tag
# novelty
nov = {}
for p in glob.glob(f"{REPO}/runs/f16/*nov*.out.csv") + [f"{REPO}/runs/f16/wave_novelty.csv"]:
    if not os.path.exists(p): continue
    for r in csv.DictReader(open(p)):
        try: nov[r["name"]] = float(r["singleseq_maxTM_pdb"])
        except (KeyError, ValueError): pass
rows = []
for n, s in seqs.items():
    L = len(s)
    if not (60 <= L <= 140): continue
    tm = nov.get(n)
    novel = (tm is not None and 0.0 < tm < 0.80)
    rows.append(dict(name=n, sequence=s, len=L, maxTM=(tm if tm is not None else ""),
                     novel=int(novel), hydro=round(hydropathy(s), 3), source=src[n]))
rows.sort(key=lambda r: (r["hydro"]))   # most soluble first
with open(f"{REPO}/runs/f18/pool_master.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name","sequence","len","maxTM","novel","hydro","source"])
    w.writeheader(); w.writerows(rows)
nnov = sum(r["novel"] for r in rows)
print(f"pool_master: {len(rows)} designs (len 60-140) | novel(0<TM<0.80 & scored): {nnov} | "
      f"RFD4={sum(r['source']=='RFD4' for r in rows)} RFd1={sum(r['source']=='RFd1' for r in rows)}")
print(f"hydropathy range: {rows[0]['hydro']} .. {rows[-1]['hydro']} (negative=soluble)")
