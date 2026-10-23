#!/usr/bin/env python3
"""mech-B multi-His combos (reuses build_multihis physics, adapted to l1_/l2_ naming).
2-3 His each near a DISTINCT buried binder cation, SEPARATED (>SEP Cb-Cb) so they titrate additively,
and OFF the binding interface (>IFACE_CUT from target) so binding survives re-fold. Baker 2025 mech-ii.
Reads scan/<name>/*.pdb (A<pos><AA>2H_vs<AA><anchor>), complexes/<name>.pdb, seqs CSV. Emits switched seqs + map.
Usage: build_switch_combos.py --scan DIR --complexes DIR --seqs csv --out csv --map tsv
"""
import argparse, csv, re, glob
from pathlib import Path
import numpy as np, gemmi

SEP, IFACE_CUT = 8.0, 9.0
PAT = re.compile(r"__A(\d+)([A-Z])2H_vs([KR]\d+)")


def cb_coords(pdb):
    m = gemmi.read_structure(pdb)[0]; out = {}
    for r in m["A"]:
        a = r.find_atom("CB", "*") or r.find_atom("CA", "*")
        if a: out[r.seqid.num] = np.array([a.pos.x, a.pos.y, a.pos.z])
    return out


def target_heavy(pdb):
    m = gemmi.read_structure(pdb)[0]
    pts = [[a.pos.x, a.pos.y, a.pos.z] for c in m if c.name != "A" for r in c for a in r if a.element.name != "H"]
    return np.asarray(pts, float) if pts else np.zeros((0, 3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", required=True); ap.add_argument("--complexes", required=True)
    ap.add_argument("--seqs", required=True); ap.add_argument("--out", required=True); ap.add_argument("--map", required=True)
    a = ap.parse_args()
    seqs = {r["name"]: (r.get("sequence") or r.get("seq")).strip() for r in csv.DictReader(open(a.seqs))}
    out_rows, map_rows = [], []
    for d in sorted(glob.glob(f"{a.scan}/*")):
        name = Path(d).name
        cpx = f"{a.complexes}/{name}.pdb"
        if name not in seqs or not Path(cpx).exists():
            continue
        vs = [PAT.search(Path(p).name) for p in glob.glob(f"{d}/*.pdb")]
        vs = [(int(m.group(1)), m.group(2), m.group(3)) for m in vs if m]  # (pos, origAA, anchor)
        cb, tgt = cb_coords(cpx), target_heavy(cpx)
        if len(tgt):
            vs = [(p, o, an) for (p, o, an) in vs
                  if p in cb and float(np.min(np.linalg.norm(tgt - cb[p], axis=1))) > IFACE_CUT]
        by_anchor = {}
        for p, o, an in vs:
            by_anchor.setdefault(an, []).append(p)
        anchor_pos = {an: sorted(ps)[0] for an, ps in by_anchor.items()}
        chosen = []
        for an, p in sorted(anchor_pos.items(), key=lambda kv: -len(by_anchor[kv[0]])):
            if p in cb and all(np.linalg.norm(cb[p] - cb[q]) > SEP for q, _ in chosen):
                chosen.append((p, an))
        if len(chosen) < 2:
            continue
        seq = seqs[name]
        for k in ([2, 3] if len(chosen) >= 3 else [2]):
            sel = chosen[:k]; s = list(seq)
            for p, an in sel:
                if 1 <= p <= len(s): s[p - 1] = "H"
            swn = f"{name}_sw{k}his"
            out_rows.append((swn, "".join(s)))
            map_rows.append((swn, name, k, ";".join(f"A{p}H/{an}" for p, an in sel)))
    w = csv.writer(open(a.out, "w")); w.writerow(["name", "sequence"])
    for n, s in out_rows: w.writerow([n, s])
    with open(a.map, "w") as f:
        f.write("sw_name\tparent\tn_his\tmutations\n")
        for r in map_rows: f.write("\t".join(map(str, r)) + "\n")
    print(f"[build_switch_combos] {len(out_rows)} switched seqs from {len(set(r[1] for r in map_rows))} binders -> {a.out}")
    for r in map_rows: print(f"  {r[0]:34} {r[3]}")


if __name__ == "__main__":
    main()
