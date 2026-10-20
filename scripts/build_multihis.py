#!/usr/bin/env python3
"""F07: build multi-His (mechanism-B) switched sequences from buried_switch_scan outputs.

Physics (Baker 2025 + install_sharp_his): 2-3 His each near a DISTINCT buried binder cation, SPATIALLY
SEPARATED (>SEP A Cb-Cb) so they titrate additively (not anti-cooperatively). At low pH each His+ repels
its buried Lys/Arg -> core destabilization -> release; target-independent -> cross-species-safe.

Reads runs/f07/switchscan/<name>/*.pdb filenames (encode posAA2H_vsK<anchor>), the complex PDB (Cb coords),
and the design's original binder seq (triage). Emits switched sequences: 2-His and 3-His combos (one His
per distinct anchor, pairwise Cb>SEP). Output: a CSV (name,sequence) to re-fold, + a map of mutations.
"""
import argparse, csv, re, glob, itertools, warnings
from pathlib import Path
import numpy as np
import gemmi

warnings.filterwarnings("ignore")
SEP = 8.0        # min Cb-Cb between two switch-His (additive, not anti-cooperative titration)
IFACE_CUT = 9.0  # min His-Cb -> target heavy-atom dist; keeps the switch OFF the binding interface
PAT = re.compile(r"__A(\d+)([A-Z])2H_vs([KR]\d+)")  # anchor = buried Lys OR Arg cation (both repel His+)


def cb_coords(pdb):
    m = gemmi.read_structure(pdb)[0]
    out = {}
    for r in m["A"]:
        a = r.find_atom("CB", "*") or r.find_atom("CA", "*")
        if a:
            out[r.seqid.num] = np.array([a.pos.x, a.pos.y, a.pos.z])
    return out


def target_heavy(pdb):
    """Heavy-atom coords of the target (every chain except the binder chain A)."""
    m = gemmi.read_structure(pdb)[0]
    pts = [[a.pos.x, a.pos.y, a.pos.z] for c in m if c.name != "A" for r in c for a in r
           if a.element.name != "H"]
    return np.asarray(pts, float) if pts else np.zeros((0, 3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default="runs/f07/switchscan")
    ap.add_argument("--complexes", default="runs/f07/complexes")
    ap.add_argument("--triage", default="runs/f04/triage.tsv")
    ap.add_argument("--out", default="runs/f07/multihis.csv")
    ap.add_argument("--map", default="runs/f07/multihis_map.tsv")
    a = ap.parse_args()
    seqs = {(r["arm"] + "__" + r["design"]): r["seq"] for r in csv.DictReader(open(a.triage), delimiter="\t")}
    out_rows, map_rows = [], []
    for d in sorted(glob.glob(f"{a.scan}/*")):
        name = Path(d).name
        variants = [PAT.search(Path(p).name) for p in glob.glob(f"{d}/*.pdb")]
        variants = [(int(m.group(1)), m.group(2), m.group(3)) for m in variants if m]  # (pos, origAA, anchor e.g. "K10"/"R59")
        if not variants or name not in seqs:
            continue
        seq = seqs[name]
        cpx = f"{a.complexes}/{name}.pdb"
        if not Path(cpx).exists():
            continue
        cb = cb_coords(cpx)
        tgt = target_heavy(cpx)
        # drop candidate His positions at/near the binding interface (a switch there kills binding on re-fold)
        if len(tgt):
            variants = [(p, o, a) for (p, o, a) in variants
                        if p in cb and float(np.min(np.linalg.norm(tgt - cb[p], axis=1))) > IFACE_CUT]
        if len(variants) < 2:
            continue
        # one best His position per distinct anchor (closest -> smallest |pos index proximity|; use first)
        by_anchor = {}
        for pos, orig, anc in variants:
            by_anchor.setdefault(anc, []).append(pos)
        # candidate positions: one per anchor
        anchor_pos = {anc: sorted(ps)[0] for anc, ps in by_anchor.items()}  # deterministic pick
        # greedily select separated positions (>SEP Cb-Cb)
        chosen = []
        for anc, pos in sorted(anchor_pos.items(), key=lambda kv: -len(by_anchor[kv[0]])):
            if pos not in cb:
                continue
            if all(np.linalg.norm(cb[pos] - cb[p]) > SEP for p, _ in chosen):
                chosen.append((pos, anc))
        if len(chosen) < 2:
            continue  # need >=2 separated His for a decisive switch
        # emit 2-His and (if available) 3-His combos
        for k in ([2, 3] if len(chosen) >= 3 else [2]):
            sel = chosen[:k]
            s = list(seq)
            for pos, anc in sel:
                if 1 <= pos <= len(s):
                    s[pos - 1] = "H"
            swname = f"{name}_sw{k}his"
            out_rows.append((swname, "".join(s)))
            map_rows.append((swname, name, k, ";".join(f"A{p}H/{anc}" for p, anc in sel)))
    w = csv.writer(open(a.out, "w")); w.writerow(["name", "sequence"])
    for n, s in out_rows:
        w.writerow([n, s])
    with open(a.map, "w") as f:
        f.write("sw_name\tparent\tn_his\tmutations\n")
        for r in map_rows:
            f.write("\t".join(map(str, r)) + "\n")
    print(f"[build_multihis] {len(out_rows)} switched seqs from {len(set(r[1] for r in map_rows))} designs -> {a.out}")
    for r in map_rows:
        print(f"  {r[0]:36} {r[3]}")


if __name__ == "__main__":
    main()
