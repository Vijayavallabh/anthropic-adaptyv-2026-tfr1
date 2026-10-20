#!/usr/bin/env python3
"""ProteinMPNN sequences for RFdiffusion backbones: design the binder (chain A), FIX the target (chain B),
bias AWAY from Cys (0-Cys de-novo binders express better). Emits a name,sequence CSV to fold (Chai∧Boltz).

Usage: mpnn_rfd.py --pdbdir runs/f11/rfd/denovo --out runs/f11/rfd_seqs.csv [--nseq 2] [--temp 0.1]
"""
import argparse, csv, glob, os, re, subprocess, shutil
from pathlib import Path

MP = Path("/home/prachh/v/mva-track2-orthogonal-20261006-v29")
MPNN_PY = MP / ".venv/bin/python"
MPNN = MP / "ProteinMPNN"


def run_dir(pdbdir, outdir, nseq, temp):
    outdir = Path(outdir).resolve(); outdir.mkdir(parents=True, exist_ok=True)
    H = MPNN / "helper_scripts"
    parsed, chains = outdir / "parsed.jsonl", outdir / "chains.jsonl"
    sh = lambda *c: subprocess.run([str(MPNN_PY), *map(str, c)], check=True,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    sh(H / "parse_multiple_chains.py", "--input_path", pdbdir, "--output_path", parsed)
    # RFd1 output: target=chain A (kept), BINDER=chain B (designed). Design B, fix A.
    sh(H / "assign_fixed_chains.py", "--input_path", parsed, "--output_path", chains, "--chain_list", "B")
    subprocess.run([str(MPNN_PY), str(MPNN / "protein_mpnn_run.py"),
                    "--jsonl_path", str(parsed), "--chain_id_jsonl", str(chains),
                    "--out_folder", str(outdir), "--num_seq_per_target", str(nseq),
                    "--sampling_temp", str(temp), "--seed", "37", "--batch_size", "1",
                    "--omit_AAs", "C"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return outdir / "seqs"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdbdir", required=True)
    ap.add_argument("--out", default="runs/f11/rfd_seqs.csv")
    ap.add_argument("--work", default="runs/f11/mpnn")
    ap.add_argument("--nseq", type=int, default=2)
    ap.add_argument("--temp", type=float, default=0.1)
    a = ap.parse_args()
    # stage only binder+target pdbs (RFd writes des_0.pdb etc.)
    stage = Path(a.work) / "pdb"; stage.mkdir(parents=True, exist_ok=True)
    pdbs = sorted(glob.glob(f"{a.pdbdir}/des_*.pdb"))
    for p in pdbs:
        shutil.copy(p, stage / Path(p).name)
    if not pdbs:
        print(f"no des_*.pdb in {a.pdbdir}"); return
    seqdir = run_dir(stage, a.work, a.nseq, a.temp)
    rows = []
    for fa in sorted(glob.glob(f"{seqdir}/*.fa")):
        rec = list(open(fa)); base = Path(fa).stem
        k = 0
        for i in range(2, len(rec), 2):  # skip native (record 0), take designs
            parts = rec[i + 1].strip().split("/")
            seq = (parts[1] if len(parts) > 1 else parts[0]).strip()  # chain B = designed binder
            rows.append((f"{base}_mpnn{k}", seq)); k += 1
    w = csv.writer(open(a.out, "w")); w.writerow(["name", "sequence"])
    for n, s in rows:
        w.writerow([n, s])
    print(f"[mpnn_rfd] {len(pdbs)} backbones -> {len(rows)} seqs -> {a.out}")


if __name__ == "__main__":
    main()
