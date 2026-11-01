#!/usr/bin/env python3
# Extract the top-K highest-iptm Protenix sample complexes for a design, write as PDBs.
# Usage: topk_pose_pdb.py <fold_dir> <out_prefix> [K=3]   -> <out_prefix>_r1.pdb ... _rK.pdb
import sys, glob, json
from pathlib import Path
import gemmi
fold, outpre = sys.argv[1], sys.argv[2]
K = int(sys.argv[3]) if len(sys.argv) > 3 else 3
cands = []
for cj in glob.glob(f"{fold}/**/*_summary_confidence_sample_*.json", recursive=True):
    try: d = json.load(open(cj))
    except: continue
    cif = cj.replace("_summary_confidence_sample_", "_sample_").replace(".json", ".cif")
    if Path(cif).exists():
        cands.append((float(d.get("iptm", 0.0)), cif))
cands.sort(key=lambda x: -x[0])
n = 0
for i, (ip, cif) in enumerate(cands[:K], 1):
    st = gemmi.read_structure(cif); st.setup_entities()
    out = f"{outpre}_r{i}.pdb"; st.write_pdb(out); n += 1
    print(f"r{i} iptm={ip:.3f} -> {out}")
if n == 0: print("NO_POSE"); sys.exit(1)
