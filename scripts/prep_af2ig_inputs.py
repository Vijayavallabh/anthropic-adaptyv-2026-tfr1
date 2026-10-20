#!/usr/bin/env python3
"""F06: build af2ig input PDBs from BoltzGen design cifs (protein pool).

af2ig (AF2 initial-guess) can't fold the binder against the full 639-aa target x hundreds of designs, so
crop the target (chain B) to residues within R A of the binder (chain A) and emit a clean PDB per design
with binder=chain A, target=chain B (the dl_binder_design convention). Reads runs/f04/triage.tsv and
takes only pool=='protein' rows.
"""
import argparse, csv, warnings
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
import gemmi

warnings.filterwarnings("ignore")


def heavy(res_iter):
    pts = []
    for r in res_iter:
        for a in r:
            if a.element.name != "H":
                pts.append([a.pos.x, a.pos.y, a.pos.z])
    return np.asarray(pts, float) if pts else np.zeros((0, 3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--triage", default="runs/f04/triage.tsv")
    ap.add_argument("--outdir", default="runs/f06/af2in")
    ap.add_argument("--radius", type=float, default=12.0)
    ap.add_argument("--pools", nargs="+", default=["protein"])
    ap.add_argument("--max", type=int, default=0, help="cap per arm (0=all)")
    a = ap.parse_args()
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    rows = [r for r in csv.DictReader(open(a.triage), delimiter="\t") if r["pool"] in a.pools]
    per_arm, written, skipped = {}, 0, 0
    for r in rows:
        arm = r["arm"]
        if a.max and per_arm.get(arm, 0) >= a.max:
            continue
        cif = r["cif"]
        try:
            m = gemmi.read_structure(cif)[0]
        except Exception:
            skipped += 1; continue
        chains = {c.name: c for c in m}
        if not chains:
            skipped += 1; continue
        tname = max(chains, key=lambda k: len(chains[k]))
        bnames = [k for k in chains if k != tname]
        if not bnames:
            skipped += 1; continue
        bres = [res for k in bnames for res in chains[k]]
        bcoords = heavy(bres)
        if len(bcoords) < 10:
            skipped += 1; continue
        tree = cKDTree(bcoords)
        keep = [res for res in chains[tname] if len(heavy([res])) and tree.query(heavy([res]), k=1)[0].min() <= a.radius]
        if len(keep) < 5:
            skipped += 1; continue
        # build output: binder=chain A, target=chain B
        st = gemmi.Structure(); mo = gemmi.Model("1")
        cb = gemmi.Chain("A")
        for res in bres:
            cb.add_residue(res)
        ct = gemmi.Chain("B")
        for res in keep:
            ct.add_residue(res)
        mo.add_chain(cb); mo.add_chain(ct); st.add_model(mo)
        st.setup_entities()
        name = f"{arm}__{Path(cif).stem}.pdb"
        st.write_pdb(str(out / name))
        per_arm[arm] = per_arm.get(arm, 0) + 1
        written += 1
    print(f"[prep_af2ig] wrote {written} inputs to {out} (skipped {skipped}); per-arm {per_arm}")


if __name__ == "__main__":
    main()
