#!/usr/bin/env python3
"""Cheap pre-filter for diffusion designs: fold each MPNN sequence single-seq (ESMFold), then in ONE pass get
(a) SELF-CONSISTENCY to the design backbone (TMalign CA-RMSD / TM: does the sequence fold to what was designed?)
and (b) NOVELTY (foldseek coverage-weighted max-TM vs PDB). Only self-consistent AND novel designs go on to the
expensive Chai∧Boltz binding check. Replaces af2ig self-consistency (broken on this install) with ESMFold+TMalign.

Backbone for <stem>_mpnnK is <backbone_dir>/<stem>.pdb (chain A). Usage:
  CUDA_VISIBLE_DEVICES=N self_consistency.py --seqs mpnn.csv --backbones runs/f11/rfd/denovo --out runs/f11/sc.csv
    [--struct-dir runs/f11/esmfold] [--pdb tools/foldseek_pdb/pdb]
Gates (tune): self-consistent = bb_TM>=0.80 & bb_rmsd<=2.5 ; novel = covwTM<0.80 (robust <0.65).
"""
import argparse, csv, os, re, glob, subprocess, warnings
warnings.filterwarnings("ignore")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FS = f"{REPO}/tools/foldseek/bin/foldseek"
TMALIGN = "/home/prachh/miniconda3/bin/TMalign"


def fold(seqs, struct_dir):
    os.makedirs(struct_dir, exist_ok=True)
    todo = {n: s for n, s in seqs.items() if not os.path.exists(f"{struct_dir}/{n}.pdb")}
    if todo:
        import torch
        from transformers import AutoTokenizer, EsmForProteinFolding
        print(f"[fold] esmfold_v1 ({len(todo)})...", flush=True)
        AutoTokenizer.from_pretrained("facebook/esmfold_v1")
        model = EsmForProteinFolding.from_pretrained("facebook/esmfold_v1", low_cpu_mem_usage=True).cuda().eval()
        model.esm = model.esm.half(); torch.backends.cuda.matmul.allow_tf32 = True
        for n, s in todo.items():
            try:
                with torch.no_grad():
                    open(f"{struct_dir}/{n}.pdb", "w").write(model.infer_pdb(s))
            except Exception as e:
                print(f"  FAIL {n}: {e}", flush=True)


def tmalign(a, b):
    """CA TM-score (norm by chain 2 = backbone) and RMSD of a onto b."""
    try:
        o = subprocess.run([TMALIGN, a, b], capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return 0.0, 99.0
    tms = re.findall(r"TM-score=\s*([\d.]+)", o)
    rmsd = re.search(r"RMSD=\s*([\d.]+)", o)
    tm = max(float(x) for x in tms) if tms else 0.0
    return tm, (float(rmsd.group(1)) if rmsd else 99.0)


def covw_maxtm(pdb, pdbdb, tmp):
    m8 = f"{tmp}/{os.path.basename(pdb)}.m8"
    try:
        subprocess.run([FS, "easy-search", pdb, pdbdb, m8, f"{tmp}/t", "--alignment-type", "1",
                        "--tmscore-threshold", "0.0", "--format-output", "query,target,alntmscore,qcov", "-v", "0"],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        return 0.0, ""
    best, hit = 0.0, ""
    for ln in open(m8):
        p = ln.split("\t")
        if len(p) >= 4:
            try:
                tm, qc = float(p[2]), float(p[3])
            except ValueError:
                continue
            if qc >= 0.70 and tm > best:
                best, hit = tm, p[1]
    return best, hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seqs", required=True)
    ap.add_argument("--backbones", required=True)
    ap.add_argument("--out", default="runs/f11/sc.csv")
    ap.add_argument("--struct-dir", default="runs/f11/esmfold")
    ap.add_argument("--pdb", default=f"{REPO}/tools/foldseek_pdb/pdb")
    a = ap.parse_args()
    seqs = {}
    for r in csv.DictReader(open(a.seqs)):
        n = r.get("name") or r.get("design"); s = (r.get("sequence") or r.get("seq") or "").strip().upper()
        if n and s:
            seqs[n] = s
    fold(seqs, a.struct_dir)
    tmp = f"{a.struct_dir}/fs_tmp"; os.makedirs(tmp, exist_ok=True)
    rows = []
    for n in seqs:
        pred = f"{a.struct_dir}/{n}.pdb"
        if not os.path.exists(pred):
            continue
        stem = re.sub(r"_mpnn\d+$", "", n)
        bb = f"{a.backbones}/{stem}.pdb"
        bb_tm, bb_rmsd = tmalign(pred, bb) if os.path.exists(bb) else (0.0, 99.0)
        nov, hit = covw_maxtm(pred, a.pdb, tmp)
        sc = bb_tm >= 0.80 and bb_rmsd <= 2.5
        novel = 0 < nov < 0.80
        rows.append((n, round(bb_tm, 3), round(bb_rmsd, 2), round(nov, 3), int(sc), int(novel), hit))
    rows.sort(key=lambda r: (-r[4] - r[5], r[3]))
    w = csv.writer(open(a.out, "w")); w.writerow(["name", "bb_TM", "bb_rmsd", "novelty_covwTM", "self_consistent", "novel", "hit"])
    for r in rows:
        w.writerow(r)
    keep = [r for r in rows if r[4] and r[5]]
    print(f"[sc] {len(rows)} designs | self-consistent AND novel: {len(keep)} -> {a.out}")
    for r in keep[:30]:
        print(f"  {r[0]:28} bbTM={r[1]} rmsd={r[2]} novTM={r[3]}")


if __name__ == "__main__":
    main()
