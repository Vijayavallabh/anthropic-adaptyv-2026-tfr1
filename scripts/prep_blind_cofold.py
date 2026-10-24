#!/usr/bin/env python3
"""BLIND co-fold YAMLs (binder=A, target=B, NO pocket constraint) — the organizers' setup: they predict
the complex blind against the FULL ectodomain and read the epitope from the model. Single-seq (msa:empty)
both chains. Auto-adds POS_3DS18 (real apical binder) + NEG scrambles for calibration.
Usage: prep_blind_cofold.py --seqs in.csv --target target.seq --out DIR [--no-controls]
"""
import argparse, csv, random
from pathlib import Path

POS_3DS18 = "DEREEEQRRRLEEVKEEAKRRERSEQDLAVLYLEAVNAAVVFVADSEEEAKRVADIVKKLVPEVIIFVHDNFVVFVVDSDEAARRVYEIVERA"

def yaml_for(binder, target):
    return f"""version: 1
sequences:
  - protein:
      id: A
      sequence: {binder}
      msa: empty
  - protein:
      id: B
      sequence: {target}
      msa: empty
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seqs", required=True); ap.add_argument("--target", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--no-controls", action="store_true")
    a = ap.parse_args()
    target = "".join(open(a.target).read().split())
    rows = [(r["name"], (r.get("sequence") or r.get("seq")).strip()) for r in csv.DictReader(open(a.seqs))]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    for nm, seq in rows:
        (out / f"{nm}.yaml").write_text(yaml_for(seq, target))
    if not a.no_controls:
        (out / "POS_3DS18.yaml").write_text(yaml_for(POS_3DS18, target))
        rng = random.Random(37)
        for i, (nm, seq) in enumerate(rows[:2]):
            sh = list(seq); rng.shuffle(sh)
            (out / f"NEG_scramble{i+1}.yaml").write_text(yaml_for("".join(sh), target))
    print(f"[prep_blind_cofold] {len(list(out.glob('*.yaml')))} blind YAMLs -> {out} (target {len(target)}aa)")

if __name__ == "__main__":
    main()
