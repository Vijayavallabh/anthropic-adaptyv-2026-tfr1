#!/usr/bin/env python3
"""Epitope-class PROBABILITY across replicate blind folds (de-noises the single-fold epitope call).
For each design, runs epitope_read on every model_*.pdb and reports the fraction of folds that read
APICAL (apical-domain, the functional-epitope goal) vs HELICAL (the transferrin face to avoid) vs other,
plus mean apical_frac and mean contacts to the Tyr211 footprint neighbourhood.
Usage: epitope_prob.py <fold_root>
"""
import sys, glob, re, subprocess
from collections import defaultdict

PB = "/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python"
ER = "/home/prachh/v/anthropic-adaptyv-2026-tfr1/scripts/epitope_read.py"
root = sys.argv[1]

def read(pdb):
    try:
        out = subprocess.run([PB, ER, pdb, "5.0"], capture_output=True, text=True, timeout=120).stdout
        cls = re.search(r"class=(\S+)", out); af = re.search(r"apical_frac=([\d.]+)", out)
        fp = re.search(r"footprint=(\d+)", out)
        return (cls.group(1) if cls else "?", float(af.group(1)) if af else 0.0, int(fp.group(1)) if fp else 0)
    except Exception:
        return ("?", 0.0, 0)

by = defaultdict(list)
for pdb in glob.glob(f"{root}/**/*_model_*.pdb", recursive=True):
    nm = re.search(r"/([^/]+)_model_\d+\.pdb$", pdb)
    if nm: by[nm.group(1)].append(read(pdb))

rows = []
for nm, rs in by.items():
    n = len(rs)
    p_apical = sum(1 for c, _, _ in rs if c in ("APICAL", "apical_domain_offsite")) / n
    p_helical = sum(1 for c, _, _ in rs if c == "helical_face") / n
    p_footprint = sum(1 for _, _, fp in rs if fp >= 1) / n
    mean_af = sum(af for _, af, _ in rs) / n
    rows.append((nm, n, p_apical, p_helical, p_footprint, mean_af))
rows.sort(key=lambda r: (-r[2], r[3]))
print(f"{'design':26} {'n':>2} {'P_apical':>8} {'P_helical':>9} {'P_fp':>5} {'mean_af':>7}")
for nm, n, pa, ph, pf, af in rows:
    print(f"{nm:26} {n:>2} {pa:8.2f} {ph:9.2f} {pf:5.2f} {af:7.2f}")
