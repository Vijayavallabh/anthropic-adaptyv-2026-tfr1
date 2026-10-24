#!/usr/bin/env python3
"""Exhaustive mech-B His-pair/triple search for ONE backbone (vs build_switch_combos' single greedy pick).
Enumerates ALL valid combos of 2-3 His, each near a DISTINCT buried binder cation, pairwise CB-CB > SEP,
each off the binding interface (> IFACE from target heavy atoms). Emits mutant seqs for folding + switch check.
Usage: exhaustive_switch.py --complex parent_complex.pdb --scan scan/<name>/ --name NAME --parent-seq SEQ
                            --out combos.csv [--max 40]
"""
import argparse, glob, re, itertools
from pathlib import Path
import numpy as np, gemmi

SEP, IFACE = 8.0, 9.0
PAT = re.compile(r"__A(\d+)([A-Z])2H_vs([KR]\d+)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--complex", required=True); ap.add_argument("--scan", required=True)
    ap.add_argument("--name", required=True); ap.add_argument("--parent-seq", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--max", type=int, default=40)
    a = ap.parse_args()
    m = gemmi.read_structure(a.complex)[0]
    cb = {}
    for r in m["A"]:
        at = r.find_atom("CB", "*") or r.find_atom("CA", "*")
        if at: cb[r.seqid.num] = np.array([at.pos.x, at.pos.y, at.pos.z])
    tgt = np.array([[at.pos.x, at.pos.y, at.pos.z] for c in m if c.name != "A" for r in c for at in r if at.element.name != "H"])
    # candidates: (pos, origAA, anchor)
    cand = []
    for p in glob.glob(f"{a.scan}/*.pdb"):
        mm = PAT.search(Path(p).name)
        if mm: cand.append((int(mm.group(1)), mm.group(2), mm.group(3)))
    # keep off-interface, de-dup by (pos,anchor)
    seen = set(); cand2 = []
    for pos, o, an in cand:
        if (pos, an) in seen or pos not in cb: continue
        seen.add((pos, an))
        if len(tgt) and float(np.min(np.linalg.norm(tgt - cb[pos], axis=1))) <= IFACE: continue
        cand2.append((pos, o, an))
    print(f"{a.name}: {len(cand2)} off-interface candidates across anchors {sorted(set(c[2] for c in cand2))}")
    seq = a.parent_seq
    rows = []
    # pairs + triples across DISTINCT anchors, pairwise CB-CB > SEP
    for k in (2, 3):
        for combo in itertools.combinations(cand2, k):
            anchors = [c[2] for c in combo]
            if len(set(anchors)) != k: continue                      # distinct cations
            ps = [c[0] for c in combo]
            ok = all(np.linalg.norm(cb[ps[i]] - cb[ps[j]]) > SEP for i in range(k) for j in range(i+1, k))
            if not ok: continue
            s = list(seq)
            for p in ps: s[p-1] = "H"
            tag = "_".join(f"A{p}H{an}" for (p, _, an) in combo)
            rows.append((f"{a.name}__{tag}", "".join(s)))
    # cap: prefer pairs (shorter tags) then triples; de-dup
    rows = list(dict(rows).items())[:a.max]
    import csv
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["name", "sequence"])
        for n, s in rows: w.writerow([n, s])
    print(f"emitted {len(rows)} combos -> {a.out}")

if __name__ == "__main__":
    main()
