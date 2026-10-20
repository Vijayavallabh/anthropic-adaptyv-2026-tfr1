#!/usr/bin/env python3
"""Structural-novelty oracle: fold each binder SEQUENCE single-sequence (classic ESMFold facebook/esmfold_v1,
as the Adaptyv/Proteinbase portal does) then Foldseek TMalign-mode max-TM vs PDB. The structure axis is the
novelty discriminator for de-novo binders (sequence axis is trivially novel). Complex-derived structures read
~0.1 high and can't resolve the boundary (lesson-portal-novelty-structural-calibrate-oracle) -> must fold the
bare sequence.

Calibration (EGFR portal ground truth, classic ESMFold): single-seq max-TM ~0.89 is the 3-vs-2 boundary.
Here: <0.80 structurally novel (safe), 0.80-0.90 borderline, >0.90 likely fails the structure axis. Helical
bundles often cap at 3/4 (pass) via the 2 sequence axes even when structure-TM is high, but a clean low TM is
strictly safer -> prefer low-TM designs.

Usage: CUDA_VISIBLE_DEVICES=N novelty_struct.py --seqs <csv name,sequence> --out runs/f09/novelty.csv
       [--struct-dir runs/f09/esmfold] [--pdb tools/foldseek_pdb/pdb]
"""
import argparse, csv, os, glob, subprocess, warnings
warnings.filterwarnings("ignore")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FS = f"{REPO}/tools/foldseek/bin/foldseek"


def fold(seqs, struct_dir):
    os.makedirs(struct_dir, exist_ok=True)
    todo = {n: s for n, s in seqs.items() if not os.path.exists(f"{struct_dir}/{n}.pdb")}
    if not todo:
        print(f"[fold] all {len(seqs)} present"); return
    import torch
    from transformers import AutoTokenizer, EsmForProteinFolding
    print(f"[fold] loading facebook/esmfold_v1 ({len(todo)} to fold)...", flush=True)
    tok = AutoTokenizer.from_pretrained("facebook/esmfold_v1")
    model = EsmForProteinFolding.from_pretrained("facebook/esmfold_v1", low_cpu_mem_usage=True).cuda().eval()
    model.esm = model.esm.half()
    torch.backends.cuda.matmul.allow_tf32 = True
    for n, s in todo.items():
        try:
            with torch.no_grad():
                out = model.infer_pdb(s)
            open(f"{struct_dir}/{n}.pdb", "w").write(out)
            print(f"  folded {n} ({len(s)}aa)", flush=True)
        except Exception as e:
            print(f"  FAIL {n}: {e}", flush=True)


def max_tm(pdb, pdbdb, tmp):
    m8 = f"{tmp}/{os.path.basename(pdb)}.m8"
    subprocess.run([FS, "easy-search", pdb, pdbdb, m8, f"{tmp}/t",
                    "--alignment-type", "1", "--tmscore-threshold", "0.0",
                    "--format-output", "query,target,alntmscore", "-v", "0"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    best, hit = 0.0, ""
    for ln in open(m8):
        p = ln.rstrip("\n").split("\t")
        if len(p) >= 3:
            try:
                tm = float(p[2])
            except ValueError:
                continue
            if tm > best:
                best, hit = tm, p[1]
    return best, hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seqs", required=True)
    ap.add_argument("--out", default="runs/f09/novelty.csv")
    ap.add_argument("--struct-dir", default="runs/f09/esmfold")
    ap.add_argument("--pdb", default=f"{REPO}/tools/foldseek_pdb/pdb")
    a = ap.parse_args()
    seqs = {}
    for r in csv.DictReader(open(a.seqs)):
        n = r.get("name") or r.get("design")
        s = (r.get("sequence") or r.get("seq") or "").split(":")[0].strip().upper()
        if n and s:
            seqs[n] = s
    fold(seqs, a.struct_dir)
    tmp = f"{a.struct_dir}/fs_tmp"; os.makedirs(tmp, exist_ok=True)
    rows = []
    for n in seqs:
        pdb = f"{a.struct_dir}/{n}.pdb"
        if not os.path.exists(pdb):
            continue
        tm, hit = max_tm(pdb, a.pdb, tmp)
        verdict = "novel" if tm < 0.80 else ("borderline" if tm < 0.90 else "risk")
        rows.append((n, round(tm, 3), hit, verdict))
        print(f"{n:30} maxTM={tm:.3f} {verdict:10} {hit}")
    rows.sort(key=lambda r: r[1])
    w = csv.writer(open(a.out, "w")); w.writerow(["name", "singleseq_maxTM_pdb", "top_hit", "verdict"])
    for r in rows:
        w.writerow(r)
    print(f"[novelty] {len(rows)} -> {a.out}  (novel<0.80 | borderline<0.90 | risk>=0.90)")


if __name__ == "__main__":
    main()
