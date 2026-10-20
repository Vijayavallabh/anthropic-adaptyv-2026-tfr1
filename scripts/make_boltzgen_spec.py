#!/usr/bin/env python3
"""Emit per-arm BoltzGen specs from data/targets/epitopes.json.

BoltzGen spec (confirmed from the installed example glp1r_vestibule.yaml):
  entities:
    - protein: {id: G, sequence: <min>..<max>}   # binder, sampled length range
    - file:
        path: <target cif>
        include: [{chain: {id: A}}]
        binding_types: [{chain: {id: A, binding: "r1,r2,..."}}]   # hotspot residues (UniProt==author)
        structure_groups: "all"
Binder = entity G; target = chain A of the clean single-subunit human ectodomain.
"""
import argparse, json
from pathlib import Path

# per-arm binder length ranges (portfolio: micro<40 / mini 40-100 / large 100-250)
LEN = {
    "armA_apical_human":            "30..95",   # human arm: micro + mini
    "armC_conserved_apical_subsite":"55..135",  # max-min core: mini + large (room for buried-His net)
    "armB_conserved_nonapical":     "55..135",  # cross-reactive: mini + large
}


def spec_yaml(target_cif, binding, length):
    b = ",".join(str(x) for x in binding)
    return f"""# auto-generated BoltzGen spec (scripts/make_boltzgen_spec.py)
entities:
  - protein:
      id: G
      sequence: {length}
  - file:
      path: {target_cif}
      include:
        - chain:
            id: A
      binding_types:
        - chain:
            id: A
            binding: {b}
      structure_groups: "all"
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epitopes", default="data/targets/epitopes.json")
    ap.add_argument("--target", default="data/targets/tfr1_human_ecto_A.cif")
    ap.add_argument("--outdir", default="specs/boltzgen")
    a = ap.parse_args()
    target = str(Path(a.target).resolve())
    e = json.loads(Path(a.epitopes).read_text())
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    for arm, length in LEN.items():
        hot = e[arm]["hotspots"]
        p = out / f"{arm}.yaml"
        p.write_text(spec_yaml(target, hot, length))
        print(f"[wrote {p}]  len={length}  binding={hot}")


if __name__ == "__main__":
    main()
