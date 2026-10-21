#!/usr/bin/env python3
"""Keep RFd1 backbones whose BINDER chain is compact (globular), dropping extended-helix junk.
Binder = chain B (RFd1 output: target=A, binder=B). Compact = Rg < FACTOR * Flory expectation
(Rg0 = 2.2 * N^0.38 A). Prints kept names; optionally copies kept PDBs to --out.

Usage: rg_filter.py --pdbdir runs/f11/rfd/long2 [--factor 1.35] [--out runs/f11/rfd/long2_compact]
"""
import argparse, glob, os, shutil
from pathlib import Path


def chain_b_ca(pdb):
    xs = []
    for ln in open(pdb):
        if ln.startswith("ATOM") and ln[12:16].strip() == "CA" and ln[21] == "B":
            xs.append((float(ln[30:38]), float(ln[38:46]), float(ln[46:54])))
    return xs


def rg(xs):
    n = len(xs)
    cx = sum(p[0] for p in xs) / n; cy = sum(p[1] for p in xs) / n; cz = sum(p[2] for p in xs) / n
    return (sum((p[0]-cx)**2 + (p[1]-cy)**2 + (p[2]-cz)**2 for p in xs) / n) ** 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdbdir", required=True)
    ap.add_argument("--factor", type=float, default=1.35)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    if a.out:
        Path(a.out).mkdir(parents=True, exist_ok=True)
    kept = 0; tot = 0
    for pdb in sorted(glob.glob(f"{a.pdbdir}/des_*.pdb")):
        xs = chain_b_ca(pdb)
        if len(xs) < 20:
            continue
        tot += 1
        n = len(xs); rg0 = 2.2 * n ** 0.38; r = rg(xs)
        if r < a.factor * rg0:
            kept += 1
            if a.out:
                shutil.copy(pdb, Path(a.out) / Path(pdb).name)
    print(f"[rg] {a.pdbdir}: {kept}/{tot} compact (Rg < {a.factor}*Flory) -> {a.out or '(count only)'}")


if __name__ == "__main__":
    main()
