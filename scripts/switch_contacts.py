#!/usr/bin/env python3
"""Baker His-cation contact metric on a RE-FOLDED switch complex (bioRxiv 2025.09.29.678932).

A working pH switch needs the switch-His to actually sit next to a cation IN THE FOLDED MODEL (re-folding
can move it away -> no switch). For each His in the binder (chain A, shortest chain), count cation charge
groups whose atom is within CUT of a His imidazole N (ND1/NE2):
  - target (chain B) Lys/Arg  => MECH A (interface repulsion, like-charge release at low pH)
  - binder (chain A) Lys/Arg  => MECH B (buried-core destabilization at low pH)
Baker floor = 2 contacts (best designs 8-11); a single strong mech-A contact gives ~1 pH unit.
Reads a folded complex (PDB or CIF). Usage: switch_contacts.py <complex.(pdb|cif)> [cut=5.0]
"""
import sys
import numpy as np
import gemmi

CUT = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
CAT = {"LYS": ["NZ"], "ARG": ["NE", "NH1", "NH2", "CZ"]}
HIS_N = ["ND1", "NE2"]


def main():
    st = gemmi.read_structure(sys.argv[1]); st.setup_entities()
    m = st[0]
    chains = sorted(m, key=lambda c: len([r for r in c]))
    binder = chains[0]
    # collect cation charge atoms: (chainlabel, resname, resnum, xyz)
    cats = []
    for c in m:
        for r in c:
            if r.name in CAT:
                for an in CAT[r.name]:
                    a = r.find_atom(an, "*")
                    if a:
                        cats.append((c.name, r.name, r.seqid.num,
                                     np.array([a.pos.x, a.pos.y, a.pos.z])))
    total_A = total_B = 0
    per_his = []
    for r in binder:
        if r.name not in ("HIS", "HID", "HIE", "HIP"):
            continue
        hns = [r.find_atom(n, "*") for n in HIS_N]
        hns = [np.array([a.pos.x, a.pos.y, a.pos.z]) for a in hns if a]
        if not hns:
            continue
        hits = []
        for cl, rn, num, cp in cats:
            if cl == binder.name and num == r.seqid.num:
                continue
            d = min(float(np.linalg.norm(hp - cp)) for hp in hns)
            if d <= CUT:
                mech = "B" if cl == binder.name else "A"
                hits.append((mech, f"{rn[0]}{num}({cl})", round(d, 1)))
                if mech == "A":
                    total_A += 1
                else:
                    total_B += 1
        per_his.append((r.seqid.num, hits))
    print(f"{sys.argv[1].split('/')[-1]}: His={len(per_his)} mechA_contacts={total_A} mechB_contacts={total_B} "
          f"total={total_A+total_B} (Baker floor>=2)")
    for num, hits in per_his:
        tag = ",".join(f"{m}:{c}@{d}" for m, c, d in hits) if hits else "no cation in reach"
        print(f"  His A{num}: {tag}")
    return total_A + total_B


if __name__ == "__main__":
    sys.exit(0 if main() >= 2 else 1)
