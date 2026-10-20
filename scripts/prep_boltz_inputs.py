#!/usr/bin/env python3
"""F06: write Boltz-2 cofold YAMLs (binder=chain A : target=chain B, msa empty) for the protein pool,
plus a 3DS18 positive control and scrambled-sequence negatives, so the gate is calibrated before trust.

Reads runs/f04/triage.tsv (has arm/design/iface/pool/seq). Target = apical domain seq (arms A/C).
"""
import argparse, csv, random
from pathlib import Path

POS_3DS18 = "DEREEEQRRRLEEVKEEAKRRERSEQDLAVLYLEAVNAAVVFVADSEEEAKRVADIVKKLVPEVIIFVHDNFVVFVVDSDEAARRVYEIVERA"
YAML = ("version: 1\nsequences:\n  - protein:\n      id: A\n      sequence: {b}\n      msa: empty\n"
        "  - protein:\n      id: B\n      sequence: {t}\n      msa: empty\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--triage", default="runs/f04/triage.tsv")
    ap.add_argument("--target-seq-file", required=True)
    ap.add_argument("--outdir", default="runs/f06/boltz_in")
    ap.add_argument("--arms", nargs="+", default=["armA", "armC", "armC_mini"])
    ap.add_argument("--topn", type=int, default=8, help="top-N per arm by interface size")
    ap.add_argument("--controls", action="store_true")
    a = ap.parse_args()
    tgt = Path(a.target_seq_file).read_text().strip().replace("\n", "")
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    rows = [r for r in csv.DictReader(open(a.triage), delimiter="\t") if r["pool"] == "protein" and r["arm"] in a.arms]
    picked = []
    for arm in a.arms:
        ar = sorted((r for r in rows if r["arm"] == arm), key=lambda r: -int(r["iface"]))[:a.topn]
        picked += ar
    for r in picked:
        nm = f"{r['arm']}__{r['design']}"
        (out / f"{nm}.yaml").write_text(YAML.format(b=r["seq"], t=tgt))
    if a.controls:
        (out / "POS_3DS18.yaml").write_text(YAML.format(b=POS_3DS18, t=tgt))
        rng = random.Random(42)
        # scramble a few real design seqs (destroys fold/interface; composition-matched negative)
        for i, r in enumerate(picked[:3]):
            s = list(r["seq"]); rng.shuffle(s)
            (out / f"NEG_scramble{i}.yaml").write_text(YAML.format(b="".join(s), t=tgt))
    n = len(list(out.glob("*.yaml")))
    print(f"[prep_boltz] wrote {n} YAMLs to {out} (picked {len(picked)} designs + controls={a.controls})")


if __name__ == "__main__":
    main()
