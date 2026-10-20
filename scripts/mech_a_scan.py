#!/usr/bin/env python3
"""Mechanism-A pH switch (Ahn/Baker 2025, bioRxiv 2025.09.29): place a His on the BINDER adjacent to a
TARGET cation (Lys/Arg) at the interface. At pH 7.4 the His is neutral (binding kept); at pH 6.0 His+
electrostatically repels the target cation -> interface weakens -> release. This weakens the INTERFACE,
not the binder fold, so it is a single gentle point mutation (unlike buried mech-B core burial).

For each complex (binder=A, target=B): find interface target cations (K-NZ / R-NE,NH1,NH2,CZ within
IFACE of the binder), then the binder residue whose CB is closest (<CUT) to that cation. Skip binder
D/E (preserve existing salt bridges) and C. Emit 1-His (best cation) and, if a 2nd well-separated cation
exists, 2-His point-mutant sequences -> runs/f07/mecha.csv (name,sequence) + mecha_map.tsv.
Usage: mech_a_scan.py [--complexes runs/f07/complexes] [--triage runs/f04/triage.tsv]
"""
import argparse, csv, glob, warnings
from pathlib import Path
import numpy as np
import gemmi

warnings.filterwarnings("ignore")
CUT = 8.0       # binder-CB -> target-cation charge-atom (His reach)
IFACE = 10.0    # cation counts as interface if within this of any binder heavy atom
SEP = 8.0       # min binder CB-CB between two His
CAT = {"LYS": ["NZ"], "ARG": ["NE", "NH1", "NH2", "CZ"]}
CATNAME = {"LYS": "K", "ARG": "R"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--complexes", default="runs/f07/complexes")
    ap.add_argument("--triage", default="runs/f04/triage.tsv")
    ap.add_argument("--out", default="runs/f07/mecha.csv")
    ap.add_argument("--map", default="runs/f07/mecha_map.tsv")
    a = ap.parse_args()
    seqs = {(r["arm"] + "__" + r["design"]): r["seq"] for r in csv.DictReader(open(a.triage), delimiter="\t")}
    out_rows, map_rows = [], []
    for cpx in sorted(glob.glob(f"{a.complexes}/*.pdb")):
        name = Path(cpx).stem
        if name not in seqs:
            continue
        seq = seqs[name]
        m = gemmi.read_structure(cpx)[0]
        chains = sorted(m, key=lambda c: len([r for r in c]))
        if len(chains) < 2:
            continue
        A, tgt_name = chains[0], chains[-1].name  # binder = shortest chain
        # binder CB coords by resnum; binder heavy coords for interface test
        bcb = {}
        bheavy = []
        for r in A:
            cb = r.find_atom("CB", "*") or r.find_atom("CA", "*")
            if cb:
                bcb[r.seqid.num] = (np.array([cb.pos.x, cb.pos.y, cb.pos.z]), r.name)
            for at in r:
                if at.element.name != "H":
                    bheavy.append([at.pos.x, at.pos.y, at.pos.z])
        bheavy = np.asarray(bheavy, float)
        # interface target cations
        cats = []
        for c in m:
            if c.name == A.name:
                continue
            for r in c:
                if r.name not in CAT:
                    continue
                for an in CAT[r.name]:
                    at = r.find_atom(an, "*")
                    if not at:
                        continue
                    p = np.array([at.pos.x, at.pos.y, at.pos.z])
                    if len(bheavy) and np.min(np.linalg.norm(bheavy - p, axis=1)) <= IFACE:
                        cats.append((f"{CATNAME[r.name]}{r.seqid.num}", p)); break
        if not cats:
            continue
        # for each cation, closest gentle binder position (not D/E/C), within CUT
        placements = []
        for cname, cp in cats:
            best = None
            for num, (cb, resn) in bcb.items():
                aa = gemmi.find_tabulated_residue(resn).one_letter_code.upper()
                if aa in "DEC":
                    continue
                d = float(np.linalg.norm(cb - cp))
                if d <= CUT and (best is None or d < best[1]):
                    best = (num, d, aa)
            if best:
                placements.append((best[0], cname, best[1], best[2]))  # (binderpos, cation, dist, origAA)
        # dedup by binder position (one His per position); sort by distance (closest = strongest repulsion)
        seenp = {}
        for pos, cn, d, aa in sorted(placements, key=lambda x: x[2]):
            if pos not in seenp:
                seenp[pos] = (cn, d, aa)
        chosen = list(seenp.items())  # [(pos,(cat,dist,aa))...]
        if not chosen:
            continue
        # 1-His (closest), and 2-His if a 2nd separated position exists
        def emit(sel, tag):
            s = list(seq)
            for pos, _ in sel:
                if 1 <= pos <= len(s):
                    s[pos - 1] = "H"
            out_rows.append((f"{name}_mA{tag}", "".join(s)))
            map_rows.append((f"{name}_mA{tag}", name, ";".join(f"A{p}H/{v[0]}@{v[1]:.1f}A" for p, v in sel)))
        emit(chosen[:1], "1")
        if len(chosen) >= 2:
            p0 = bcb[chosen[0][0]][0]
            for pos, v in chosen[1:]:
                if np.linalg.norm(bcb[pos][0] - p0) > SEP:
                    emit([chosen[0], (pos, v)], "2"); break
    w = csv.writer(open(a.out, "w")); w.writerow(["name", "sequence"])
    for n, s in out_rows:
        w.writerow([n, s])
    with open(a.map, "w") as f:
        f.write("name\tparent\tmutations\n")
        for r in map_rows:
            f.write("\t".join(r) + "\n")
    print(f"[mech_a] {len(out_rows)} interface-His seqs from {len(set(r[1] for r in map_rows))} designs -> {a.out}")
    for r in map_rows:
        print(f"  {r[0]:32} {r[2]}")


if __name__ == "__main__":
    main()
