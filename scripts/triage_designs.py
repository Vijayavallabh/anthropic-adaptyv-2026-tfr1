#!/usr/bin/env python3
"""F04->F05 triage: fold-classify + hotspot-contact filter BoltzGen design outputs.

For each design cif (binder = chain A, target = chain B): extract binder seq/len/nCys, classify fold
(VHH/Ig vs de-novo), count on-target hotspot contacts (<5 A) and total interface residues, then route:
  - PROTEIN pool  : NOT Ig-fold, nCys<=1, >=1 hotspot contact (0-Cys de-novo docked at the site)
  - NANOBODY pool : Ig-fold (VHH framework) -- candidate for the conditional nanobody arm (CDRH3-novelty,
                    ANARCI, >=2-folder ipTM gated later)
  - DROP          : off-site (0 hotspot contacts) or degenerate

Emits <rundir>/triage.tsv + a per-arm summary. Deterministic; no model calls.
"""
import argparse, glob, json, warnings
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
import gemmi

warnings.filterwarnings("ignore")
ARM_KEY = {"armA": "armA_apical_human", "armB": "armB_conserved_nonapical",
           "armC": "armC_conserved_apical_subsite"}


def is_vhh(seq):
    """VHH/Ig framework signature: FR2 tetrad (W-x-R-Q) + >=2 Cys + Ig J-segment (WGxG)."""
    fr2 = any(m in seq for m in ("WFRQ", "WYRQ", "WVRQ", "WLRQ", "WFKQ"))
    jseg = any(m in seq for m in ("WGQG", "WGKG", "WGQGT", "WGRG"))
    return fr2 and jseg and seq.count("C") >= 2


def heavy_coords(res_list):
    pts = []
    for r in res_list:
        for a in r:
            if a.element.name != "H":
                pts.append([a.pos.x, a.pos.y, a.pos.z])
    return np.asarray(pts, float) if pts else np.zeros((0, 3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rundir", default="runs/f04")
    ap.add_argument("--epitopes", default="data/targets/epitopes.json")
    ap.add_argument("--arms", nargs="+", default=["armA", "armB", "armC"])
    ap.add_argument("--contact", type=float, default=5.0)
    a = ap.parse_args()
    epi = json.loads(Path(a.epitopes).read_text())
    rows = []
    for arm in a.arms:
        hot = set(epi[ARM_KEY[arm]]["hotspots"])
        cifs = sorted(glob.glob(f"{a.rundir}/{arm}/**/intermediate_designs/*_[0-9]*.cif", recursive=True))
        for cif in cifs:
            try:
                m = gemmi.read_structure(cif)[0]
            except Exception:
                continue
            chains = {c.name: [r for r in c] for c in m}
            if not chains:
                continue
            tgt = max(chains, key=lambda k: len(chains[k]))
            binders = [k for k in chains if k != tgt]
            if not binders:
                continue
            bres = [r for k in binders for r in chains[k]]
            seq = gemmi.one_letter_code([r.name for r in bres]).replace("X", "")
            blen, ncys = len(seq), seq.count("C")
            bcoords = heavy_coords(bres)
            if len(bcoords) == 0:
                continue
            tree = cKDTree(bcoords)
            # per-target-residue min distance to binder
            iface, hot_hits = 0, []
            for r in chains[tgt]:
                tc = heavy_coords([r])
                if len(tc) == 0:
                    continue
                d = tree.query(tc, k=1)[0].min()
                if d <= a.contact:
                    iface += 1
                    if r.seqid.num in hot:
                        hot_hits.append(r.seqid.num)
            vhh = is_vhh(seq)
            did = Path(cif).stem
            if len(hot_hits) == 0:
                pool = "DROP_offsite"
            elif vhh:
                pool = "nanobody"
            elif ncys <= 1:
                pool = "protein"
            else:
                pool = "protein_hasCys"   # de-novo but has internal Cys -> re-MPNN to 0-Cys in F05
            rows.append(dict(arm=arm, design=did, len=blen, nCys=ncys, vhh=int(vhh),
                             hot_contacts=len(hot_hits), iface=iface, pool=pool,
                             hotspots=",".join(map(str, sorted(hot_hits))), cif=cif, seq=seq))
    # write tsv
    out = Path(a.rundir) / "triage.tsv"
    cols = ["arm", "design", "len", "nCys", "vhh", "hot_contacts", "iface", "pool", "hotspots", "cif", "seq"]
    with out.open("w") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join(str(r[c]) for c in cols) + "\n")
    # summary
    print(f"[triage] {len(rows)} designs -> {out}")
    for arm in a.arms:
        ar = [r for r in rows if r["arm"] == arm]
        if not ar:
            continue
        from collections import Counter
        pc = Counter(r["pool"] for r in ar)
        prot = [r for r in ar if r["pool"] == "protein"]
        print(f"  {arm}: n={len(ar)} | {dict(pc)} | protein len range "
              f"{min((r['len'] for r in prot), default=0)}-{max((r['len'] for r in prot), default=0)}, "
              f"median iface {int(np.median([r['iface'] for r in prot])) if prot else 0}")


if __name__ == "__main__":
    main()
