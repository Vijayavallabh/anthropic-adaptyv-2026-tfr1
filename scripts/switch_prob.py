#!/usr/bin/env python3
"""Switch-geometry PROBABILITY across replicate folds (addresses Boltz single-fold stochasticity).
For each design, runs switch_contacts on every model_*.pdb and reports mean total, fraction>=2 (Baker
floor), and max. A genuine switch forms consistently (high frac>=2); a marginal one only occasionally.
Usage: switch_prob.py <fold_root>
"""
import sys, glob, os, re, subprocess, statistics as st
from collections import defaultdict

PB = "/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python"
SC = "/home/prachh/v/anthropic-adaptyv-2026-tfr1/scripts/switch_contacts.py"
root = sys.argv[1]

def total_for(pdb):
    try:
        out = subprocess.run([PB, SC, pdb, "5.0"], capture_output=True, text=True, timeout=120).stdout
        m = re.search(r"total=(\d+)", out)
        return int(m.group(1)) if m else None
    except Exception:
        return None

by = defaultdict(list)
for pdb in glob.glob(f"{root}/**/*_model_*.pdb", recursive=True):
    nm = re.search(r"/([^/]+)_model_\d+\.pdb$", pdb)
    if not nm: continue
    t = total_for(pdb)
    if t is not None: by[nm.group(1)].append(t)

rows = []
for nm, ts in by.items():
    n = len(ts); frac = sum(1 for t in ts if t >= 2) / n if n else 0
    rows.append((nm, n, st.mean(ts) if ts else 0, frac, max(ts) if ts else 0, min(ts) if ts else 0))
rows.sort(key=lambda r: (-r[3], -r[2]))
print(f"{'design':34} {'n':>2} {'mean':>5} {'frac>=2':>7} {'max':>3} {'min':>3}")
for nm, n, mean, frac, mx, mn in rows:
    print(f"{nm:34} {n:>2} {mean:5.1f} {frac:7.2f} {mx:>3} {mn:>3}")
