#!/usr/bin/env python3
"""Fold peptide:receptor complexes with Chai-1 (orthogonal to Boltz-2) in SINGLE-SEQUENCE mode
(ESM embeddings, NO MSA server) = the analog of the Boltz panel's `msa: empty`. Then ADAPT the
Chai outputs to Boltz filenames so the UNCHANGED scripts/iface_score.py can score them identically.

Per (design, seed): run Chai -> pick the top-aggregate_score candidate (Boltz model_0 analog),
and write into by_seed/<name>/s<seed>/:
    <name>_model_0.cif              (copy of pred.model_idx_<best>.cif)
    pae_<name>_model_0.npz          (cands.pae[best], N x N  -> key 'pae')
    confidence_<name>_model_0.json  ({"iptm": <iptm of best>})

NO scoring science here; pure fold + file-name adapter. Fail-loud.

Usage: chai_fold_adapt.py <designs.csv name,sequence> <receptor.seq> <out_root> \
         --seeds 0,1,2 [--samples 5] [--recycles 3]
"""
import argparse, csv, json, shutil, sys, os
from pathlib import Path
import numpy as np


def read_receptor(p):
    return "".join(l.strip() for l in open(p) if l.strip() and not l.startswith(">"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("designs")
    ap.add_argument("receptor")
    ap.add_argument("out_root")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--samples", type=int, default=5)
    ap.add_argument("--recycles", type=int, default=3)
    ap.add_argument("--constraints", default="")  # Chai pocket-restraint CSV (apical epitope)
    a = ap.parse_args()

    seeds = [int(s) for s in a.seeds.split(",")]
    receptor = read_receptor(a.receptor)
    assert len(receptor) > 150, f"receptor too short: {len(receptor)}"
    rows = [(r["name"], r["sequence"].strip().upper())
            for r in csv.DictReader(open(a.designs)) if r.get("sequence")]
    out_root = Path(a.out_root)
    raw_root = out_root / "raw"
    byseed_root = out_root / "by_seed"
    byseed_root.mkdir(parents=True, exist_ok=True)

    from chai_lab.chai1 import run_inference  # heavy import -> after arg parse

    for name, seq in rows:
        fasta = out_root / "fasta" / f"{name}.fasta"
        fasta.parent.mkdir(parents=True, exist_ok=True)
        fasta.write_text(f">protein|name=A\n{seq}\n>protein|name=B\n{receptor}\n")
        print(f"[{name}] fasta: chainA peptide {len(seq)}aa + chainB receptor {len(receptor)}aa", flush=True)
        for seed in seeds:
            dst = byseed_root / name / f"s{seed}"
            done_cif = dst / f"{name}_model_0.cif"
            done_pae = dst / f"pae_{name}_model_0.npz"
            done_conf = dst / f"confidence_{name}_model_0.json"
            if done_cif.exists() and done_pae.exists() and done_conf.exists():
                print(f"[{name} s{seed}] already adapted -> skip", flush=True)
                continue
            raw = raw_root / name / f"seed{seed}"
            if raw.exists():
                shutil.rmtree(raw)  # targeted scratch dir (Chai requires empty output_dir)
            raw.mkdir(parents=True, exist_ok=True)
            cands = run_inference(
                fasta_file=fasta, output_dir=raw,
                use_esm_embeddings=True, use_msa_server=False,
                num_diffn_samples=a.samples, num_trunk_recycles=a.recycles,
                seed=seed, device="cuda:0", low_memory=True,
                constraint_path=(Path(a.constraints) if a.constraints else None),
            )
            # pick best candidate = max aggregate_score (Chai's own ranking) = Boltz model_0 analog
            n = len(cands.cif_paths)
            aggs = []
            for i in range(n):
                sc = np.load(raw / f"scores.model_idx_{i}.npz")
                aggs.append(float(np.ravel(sc["aggregate_score"])[0]))
            best = int(np.argmax(aggs))
            iptm_best = float(np.ravel(np.load(raw / f"scores.model_idx_{best}.npz")["iptm"])[0])
            pae_best = np.asarray(cands.pae[best].cpu().numpy(), dtype=np.float32)
            assert pae_best.ndim == 2 and pae_best.shape[0] == pae_best.shape[1], f"bad pae shape {pae_best.shape}"
            dst.mkdir(parents=True, exist_ok=True)
            shutil.copy(cands.cif_paths[best], done_cif)
            np.savez(done_pae, pae=pae_best)
            json.dump({"iptm": iptm_best, "aggregate_score": aggs[best],
                       "chai_best_model_idx": best, "n_samples": n, "pae_dim": int(pae_best.shape[0])},
                      open(done_conf, "w"), indent=2)
            print(f"[{name} s{seed}] best=model_idx_{best} agg={aggs[best]:.3f} iptm={iptm_best:.3f} "
                  f"pae_dim={pae_best.shape[0]} -> {dst}", flush=True)
    print("CHAI_FOLD_ADAPT_DONE", flush=True)


if __name__ == "__main__":
    main()
