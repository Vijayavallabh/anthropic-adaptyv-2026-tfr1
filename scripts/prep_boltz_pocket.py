#!/usr/bin/env python3
"""Pocket-RESTRAINED Boltz-2 cofold YAMLs: force the binder (chain A) to contact the apical epitope on
the target (chain B), so validation tests apical-binding COMPETENCE instead of blind docking (which drifts
every binder -- even the crystal-true 3DS18 positive control -- to the off-epitope 259-300 groove).

Target chain B = apical fragment (UniProt 189-383); chain-B resid = UniProt-188.
Apical epitope {202,203,204,208,209,210,211,212,348,371} -> chain B {14,15,16,20,21,22,23,24,160,183}.

Auto-adds controls: POS_3DS18 (known apical binder, 6WRV) + NEG scrambles (should score low if method works).
Usage: prep_boltz_pocket.py --seqs in.csv --target data/targets/apical_domain_189_383.seq --out DIR [--force] [--no-controls]
"""
import argparse, csv, random
from pathlib import Path

POS_3DS18 = "DEREEEQRRRLEEVKEEAKRRERSEQDLAVLYLEAVNAAVVFVADSEEEAKRVADIVKKLVPEVIIFVHDNFVVFVVDSDEAARRVYEIVERA"
APICAL_B = [14, 15, 16, 20, 21, 22, 23, 24, 160, 183]  # chain-B resids = UniProt-188


def yaml_for(binder, target, resids, force):
    contacts = ", ".join(f"[B, {r}]" for r in resids)
    f = "\n      force: true" if force else ""
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
constraints:
  - pocket:
      binder: A
      contacts: [{contacts}]
      max_distance: 6{f}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seqs", required=True)
    ap.add_argument("--target", default="data/targets/apical_domain_189_383.seq")
    ap.add_argument("--out", required=True)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-controls", action="store_true")
    a = ap.parse_args()
    target = open(a.target).read().strip()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rows = [(r["name"], (r.get("sequence") or r.get("seq")).strip())
            for r in csv.DictReader(open(a.seqs)) if (r.get("sequence") or r.get("seq"))]
    if not a.no_controls:
        rows.append(("POS_3DS18", POS_3DS18))
        rng = random.Random(37)
        for i in (1, 2):
            s = list(POS_3DS18); rng.shuffle(s)
            rows.append((f"NEG_scramble{i}", "".join(s)))
    for nm, seq in rows:
        (out / f"{nm}.yaml").write_text(yaml_for(seq, target, APICAL_B, a.force))
    print(f"[prep_boltz_pocket] {len(rows)} YAMLs -> {out} (force={a.force}, pocket=apical chainB {APICAL_B})")


if __name__ == "__main__":
    main()
