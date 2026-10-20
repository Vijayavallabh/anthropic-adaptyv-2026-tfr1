#!/usr/bin/env python3
"""F06: parse Boltz-2 cofold outputs -> per-design interface metrics for the 2-folder gate.

Metrics: iptm (global), pair A-B iptm (interface), complex_iplddt, interface iPAE (mean PAE over A<->B
contact pairs), and hotspot_contacts (does the predicted binder land on the arm's epitope). Target chain B
is the apical domain (UniProt 189-383): output B index j(1-based) -> UniProt 188+j.
"""
import argparse, csv, glob, json, warnings
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree

warnings.filterwarnings("ignore")
APICAL_OFFSET = 188  # output chain-B residue j -> UniProt 188+j
HOT = {"armA": {202,203,204,208,209,210,211,212,348,371},
       "armC": {202,203,206,207,209,214,344,374}, "armC_mini": {202,203,206,207,209,214,344,374},
       "POS": {202,203,206,207,209,214,344,374,348,371,204,208,210,211,212}, "NEG": set()}


def heavy(res):
    import gemmi  # noqa
    return [[a.pos.x, a.pos.y, a.pos.z] for a in res if a.element.name != "H"]


def arm_of(name):
    for k in ("armC_mini", "armA", "armC", "armB", "POS", "NEG"):
        if name.startswith(k):
            return k
    return "armC"


def main():
    import gemmi
    ap = argparse.ArgumentParser()
    ap.add_argument("--rundir", default="runs/f06/boltz_cal_out")
    ap.add_argument("--out", default="runs/f06/boltz_cal_scores.tsv")
    a = ap.parse_args()
    confs = glob.glob(f"{a.rundir}/**/confidence_*.json", recursive=True)
    rows = []
    for cj in confs:
        d = json.loads(Path(cj).read_text())
        name = Path(cj).stem.replace("confidence_", "").rsplit("_model_", 1)[0]
        pdbs = glob.glob(str(Path(cj).parent / f"{name}*model_0.pdb"))
        iptm = d.get("iptm"); pair = d.get("pair_chains_iptm", {})
        try:
            ab = float(pair["0"]["1"])
        except Exception:
            ab = iptm
        iplddt = d.get("complex_iplddt")
        # interface iPAE + hotspot contacts from the structure + pae npz
        hot_hits, ipae = 0, None
        if pdbs:
            m = gemmi.read_structure(pdbs[0])[0]
            ch = {c.name: [r for r in c] for c in m}
            if "A" in ch and "B" in ch:
                ba = np.array([p for r in ch["A"] for p in heavy(r)])
                arm = arm_of(name); hot = HOT.get(arm, set())
                if len(ba):
                    tree = cKDTree(ba)
                    for r in ch["B"]:
                        tc = heavy(r)
                        if tc and tree.query(np.array(tc), k=1)[0].min() <= 5.0:
                            if (APICAL_OFFSET + r.seqid.num) in hot:
                                hot_hits += 1
            pae_npz = glob.glob(str(Path(cj).parent / f"pae_{name}*model_0.npz"))
            if pae_npz:
                try:
                    P = np.load(pae_npz[0]); pae = P[P.files[0]]
                    na = len(ch["A"]);
                    sub = np.concatenate([pae[:na, na:].ravel(), pae[na:, :na].ravel()])
                    ipae = float(np.mean(sub))
                except Exception:
                    pass
        rows.append(dict(name=name, arm=arm_of(name), iptm=iptm, ab_iptm=round(ab,3) if ab else None,
                         iplddt=iplddt, ipae=round(ipae,2) if ipae else None, hot_contacts=hot_hits))
    rows.sort(key=lambda r: -(r["ab_iptm"] or 0))
    cols = ["name","arm","iptm","ab_iptm","iplddt","ipae","hot_contacts"]
    with open(a.out, "w") as f:
        f.write("\t".join(cols)+"\n")
        for r in rows: f.write("\t".join(str(r[c]) for c in cols)+"\n")
    print(f"[parse_boltz] {len(rows)} designs -> {a.out}")
    for r in rows:
        print(f"  {r['name'][:42]:42} ab_iptm={r['ab_iptm']} iplddt={r['iplddt']} ipae={r['ipae']} hot={r['hot_contacts']}")


if __name__ == "__main__":
    main()
