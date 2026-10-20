#!/usr/bin/env python3
"""Rescue a switch that broke binding on re-fold: install the buried His, then let ProteinMPNN repack the
CORE around them while FIXING (a) the whole target, (b) the binder's interface contacts, (c) the His sites.

Why: retrofitting a buried His onto a de-novo binder often deletes a core hydrophobic -> fold destabilizes
-> binding lost. MPNN finds a core packing compatible with the buried His (the canonical Baker install),
keeping the interface + His fixed so binding + switch chemistry are preserved.

Reads runs/f07/multihis_map.tsv (sw_name,parent,n_his,mutations "A10H/K14;..."), the parent complex
(runs/f07/complexes/<parent>.pdb, binder=A target=B), emits ProteinMPNN-repaired binder sequences ->
runs/f07/repair/<sw_name>.fa and a combined runs/f07/repair_refold.csv (name,sequence) to re-fold.

Usage: mpnn_switch_repair.py [--only sw_name,...] [--nseq 8] [--temp 0.1]
"""
import argparse, csv, re, subprocess, json, shutil, os
from pathlib import Path
import numpy as np
import gemmi

REPO = Path(__file__).resolve().parents[1]
MP = Path("/home/prachh/v/mva-track2-orthogonal-20261006-v29")
MPNN_PY = MP / ".venv/bin/python"
MPNN = MP / "ProteinMPNN"
IFACE = 5.0  # chain-A residue within this of target = binding contact -> FIX
KEEP = {"N", "CA", "C", "O", "CB"}


def install_his(pdb, positions, out):
    """Rename chain-A residues at `positions` to HIS, dropping sidechain beyond CB (bb+CB kept)."""
    with open(out, "w") as fh:
        for ln in open(pdb):
            if ln[:4] != "ATOM":
                fh.write(ln); continue
            if ln[21] == "A" and int(ln[22:26]) in positions:
                if ln[12:16].strip() not in KEEP:
                    continue
                ln = ln[:17] + "HIS" + ln[20:]
            fh.write(ln)


def interface_resnums(pdb):
    """chain-A resnums with any heavy atom within IFACE of any target (non-A) heavy atom."""
    m = gemmi.read_structure(pdb)[0]
    tgt = np.array([[a.pos.x, a.pos.y, a.pos.z] for c in m if c.name != "A"
                    for r in c for a in r if a.element.name != "H"])
    if not len(tgt):
        return set()
    from scipy.spatial import cKDTree
    tree = cKDTree(tgt)
    out = set()
    for r in m["A"]:
        for a in r:
            if a.element.name == "H":
                continue
            if tree.query([a.pos.x, a.pos.y, a.pos.z])[0] <= IFACE:
                out.add(r.seqid.num); break
    return out


def run_mpnn(pdb, fixed_posA, outdir, nseq, temp):
    outdir = Path(outdir).resolve(); outdir.mkdir(parents=True, exist_ok=True)
    pdb = Path(pdb).resolve()
    pdir = outdir / "pdb"; pdir.mkdir(exist_ok=True)
    shutil.copy(pdb, pdir / Path(pdb).name)
    parsed, chains, fixed = outdir / "parsed.jsonl", outdir / "chains.jsonl", outdir / "fixed.jsonl"
    H = MPNN / "helper_scripts"
    sh = lambda *c: subprocess.run([str(MPNN_PY), *map(str, c)], check=True, cwd=outdir,
                                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    sh(H / "parse_multiple_chains.py", "--input_path", pdir, "--output_path", parsed)
    sh(H / "assign_fixed_chains.py", "--input_path", parsed, "--output_path", chains, "--chain_list", "A")
    sh(H / "make_fixed_positions_dict.py", "--input_path", parsed, "--output_path", fixed,
       "--chain_list", "A", "--position_list", " ".join(map(str, sorted(fixed_posA))))
    subprocess.run([str(MPNN_PY), str(MPNN / "protein_mpnn_run.py"),
                    "--jsonl_path", str(parsed), "--chain_id_jsonl", str(chains),
                    "--fixed_positions_jsonl", str(fixed), "--out_folder", str(outdir),
                    "--num_seq_per_target", str(nseq), "--sampling_temp", str(temp),
                    "--seed", "37", "--batch_size", "1"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # best (lowest global_score) designed seq from seqs/<name>.fa
    fa = next((outdir / "seqs").glob("*.fa"))
    best, best_sc = None, 1e9
    rec = list(open(fa))
    for i in range(2, len(rec), 2):  # skip native (first record), take designed
        head, seq = rec[i], rec[i + 1].strip()
        m = re.search(r"global_score=([\d.]+)", head)
        sc = float(m.group(1)) if m else 1e9
        if sc < best_sc:
            best_sc, best = sc, seq.split("/")[0].strip()  # chain A (design) part
    return best, best_sc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", default="runs/f07/multihis_map.tsv")
    ap.add_argument("--complexes", default="runs/f07/complexes")
    ap.add_argument("--out", default="runs/f07/repair")
    ap.add_argument("--refold_csv", default="runs/f07/repair_refold.csv")
    ap.add_argument("--only", default="")
    ap.add_argument("--nseq", type=int, default=8)
    ap.add_argument("--temp", type=float, default=0.1)
    a = ap.parse_args()
    only = set(x for x in a.only.split(",") if x)
    rows = list(csv.DictReader(open(a.map), delimiter="\t"))
    out_csv = []
    for r in rows:
        sw, parent, muts = r["sw_name"], r["parent"], r["mutations"]
        if only and sw not in only:
            continue
        his = sorted(int(x) for x in re.findall(r"A(\d+)H", muts))
        cpx = f"{a.complexes}/{parent}.pdb"
        if not Path(cpx).exists():
            print(f"  skip {sw}: no complex"); continue
        iface = interface_resnums(cpx)
        fixed = iface | set(his)
        od = Path(a.out) / sw
        his_pdb = od.parent / f"{sw}_hisinstalled.pdb"; od.mkdir(parents=True, exist_ok=True)
        install_his(cpx, set(his), his_pdb)
        try:
            seq, sc = run_mpnn(his_pdb, fixed, od, a.nseq, a.temp)
        except subprocess.CalledProcessError as e:
            print(f"  MPNN failed {sw}: {e}"); continue
        # sanity: His retained at the switch positions
        ok = all(1 <= p <= len(seq) and seq[p - 1] == "H" for p in his)
        print(f"  {sw:30} His@{his} iface={len(iface)} fixed={len(fixed)} score={sc:.3f} HisOK={ok}")
        out_csv.append((f"{sw}_rep", seq))
    w = csv.writer(open(a.refold_csv, "w")); w.writerow(["name", "sequence"])
    for n, s in out_csv:
        w.writerow([n, s])
    print(f"[repair] {len(out_csv)} repaired seqs -> {a.refold_csv}")


if __name__ == "__main__":
    main()
