#!/usr/bin/env python3
"""Compute ipSAE (Dunbrack 2025, the organizers' interface ranker) + ipTM for a fold dir.
Works on Boltz-2 and Chai-1 output (both write pae_*.npz + *.pdb + confidence_*.json, binder=A target=B).
Runs the reference ipsae_ref.py per design, parses the A-B 'max' line (symmetric ipSAE).
Usage: score_ipsae.py <fold_root> <label>  ->  prints TSV: name<TAB>iptm<TAB>ipsae  (also writes <fold_root>/ipsae.tsv)
"""
import sys, os, glob, json, re, subprocess, statistics as st
from collections import defaultdict

PY = "/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python"
IPSAE = "/home/prachh/v/anthropic-adaptyv-2026-tfr1/scripts/ipsae.py"

def design_name(pae_path):
    b = os.path.basename(pae_path)
    m = re.match(r"pae_(.+?)_model_\d+\.npz", b)
    return m.group(1) if m else None

def parse_ipsae_txt(txt):
    """Return symmetric ipSAE (d0res headline col) for the A-B pair from a *_10_10.txt."""
    if not os.path.exists(txt): return None
    best = None
    for ln in open(txt):
        p = ln.split()
        if len(p) < 6: continue
        if p[0] in ("Chn1", "#"): continue
        c1, c2, _pae, _dist, typ = p[0], p[1], p[2], p[3], p[4]
        if typ != "max": continue
        if {c1, c2} != {"A", "B"}: continue
        try: val = float(p[5])          # col 'ipSAE' (d0res headline)
        except (ValueError, IndexError): continue
        best = val if best is None else max(best, val)
    return best

def main():
    root, label = sys.argv[1], sys.argv[2]
    iptm = defaultdict(list); ipsae = defaultdict(list)
    paes = glob.glob(f"{root}/**/pae_*_model_*.npz", recursive=True)
    for pae in paes:
        nm = design_name(pae)
        if not nm: continue
        d = os.path.dirname(pae)
        pdb = glob.glob(f"{d}/{nm}_model_*.pdb")
        if not pdb:
            cif = glob.glob(f"{d}/{nm}_model_*.cif")
            if not cif: continue
            struct = cif[0]; stem = struct[:-4]
        else:
            struct = pdb[0]; stem = struct[:-4]
        # ipTM from confidence json
        cj = glob.glob(f"{d}/confidence_{nm}_model_*.json")
        if cj:
            try:
                j = json.load(open(cj[0])); iptm[nm].append(j.get("iptm", j.get("complex_iptm", 0.0)))
            except Exception: pass
        # ipSAE via reference script
        txt = f"{stem}_10_10.txt"
        if not os.path.exists(txt):
            try:
                subprocess.run([PY, IPSAE, pae, struct, "10", "10"], capture_output=True, timeout=300)
            except Exception: pass
        v = parse_ipsae_txt(txt)
        if v is not None: ipsae[nm].append(v)
    names = sorted(set(iptm) | set(ipsae))
    out = open(f"{root}/ipsae.tsv", "w"); out.write("name\tiptm\tipsae\n")
    rows = []
    for nm in names:
        it = st.mean(iptm[nm]) if iptm[nm] else float("nan")
        ip = st.mean(ipsae[nm]) if ipsae[nm] else float("nan")
        rows.append((nm, it, ip)); out.write(f"{nm}\t{it:.4f}\t{ip:.4f}\n")
    out.close()
    rows.sort(key=lambda r: (-(r[2] if r[2]==r[2] else -1)))
    print(f"[{label}] {len(rows)} designs  (fold_root={root})")
    print(f"{'ipSAE':>7} {'ipTM':>6}  name")
    for nm, it, ip in rows:
        print(f"{ip:7.3f} {it:6.3f}  {nm}")

if __name__ == "__main__":
    main()
