#!/usr/bin/env python3
"""Switch-geometry probability across CHAI replicate samples (CIF), Baker floor frac>=2.
Chai writes raw/<NAME>/seed*/pred.model_idx_*.cif (N diffusion samples per seed). Pools samples
across all given roots (e.g. a human-bound AND a mouse-bound Chai dir) per design, runs
switch_contacts on each, reports n, mean total His-cation contacts, fraction>=2, max, min.
switch_prob.py (Boltz, *_model_*.pdb) misses these; this is the Chai/CIF counterpart.
Usage: switch_prob_chai.py <chai_root1> [chai_root2 ...]
"""
import sys, glob, re, subprocess, statistics as st
from collections import defaultdict

PB = "/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python"
SC = "/home/prachh/v/anthropic-adaptyv-2026-tfr1/scripts/switch_contacts.py"

def total_for(f):
    try:
        out = subprocess.run([PB, SC, f, "5.0"], capture_output=True, text=True, timeout=120).stdout
        m = re.search(r"total=(\d+)", out)
        return int(m.group(1)) if m else None
    except Exception:
        return None

by = defaultdict(list)
for root in sys.argv[1:]:
    for f in glob.glob(f"{root}/**/raw/*/seed*/pred.model_idx_*.cif", recursive=True):
        m = re.search(r"/raw/([^/]+)/seed", f)
        if not m:
            continue
        t = total_for(f)
        if t is not None:
            by[m.group(1)].append(t)

rows = []
for nm, ts in by.items():
    n = len(ts); frac = sum(1 for t in ts if t >= 2) / n if n else 0
    rows.append((nm, n, st.mean(ts) if ts else 0, frac, max(ts) if ts else 0, min(ts) if ts else 0))
rows.sort(key=lambda r: (-r[3], -r[2]))
print(f"{'design':36} {'n':>2} {'mean':>5} {'frac>=2':>7} {'max':>3} {'min':>3}")
for nm, n, mean, frac, mx, mn in rows:
    print(f"{nm:36} {n:>2} {mean:5.1f} {frac:7.2f} {mx:>3} {mn:>3}")
