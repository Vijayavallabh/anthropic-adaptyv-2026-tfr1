#!/usr/bin/env python3
"""ORGANIZERS' outside judge: co-fold v15 designs with Protenix (ByteDance, open AF3-class) BLIND
(no pocket constraint -> matches the organizers' regime) with heavy inference-time sampling.
A design whose BEST-ipTM poses land on the apical epitope under blind Protenix is far more
trustworthy than a pocket-restraint artifact -> a strong orthogonal third-folder check.

Chain A = binder (de-novo, single-seq a3m). Chain B = apical fragment (UniProt 189-383; human or
mouse; single-seq a3m to mirror the Boltz/Chai msa:empty pipeline -> symmetric across designs/species).
Usage: fold_protenix_tfr1.py --seqs v15.csv --species human|mouse --out DIR --gpu N
       [--samples 24 --seeds 101,102 --limit K --names a,b]
Drafted by the assistant (ambition-lift depth pass, 2026-10-27)."""
import argparse, csv, json, os, subprocess, sys
from pathlib import Path

REPO = Path("/home/prachh/v/anthropic-adaptyv-2026-tfr1")
PROT = Path("/home/prachh/v/sepiq-2026-challenge/.venv-protenix/bin/protenix")
FRAG = {"human": REPO/"data/targets/apical_domain_189_383.seq",
        "mouse": REPO/"data/targets/mouse_apical_189_383.seq"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seqs", required=True)
    ap.add_argument("--species", required=True, choices=["human","mouse"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--gpu", default="0")
    ap.add_argument("--samples", type=int, default=24)
    ap.add_argument("--seeds", default="101,102")
    ap.add_argument("--cycle", type=int, default=10)
    ap.add_argument("--step", type=int, default=200)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--names", default="")           # comma list to subset by design name
    ap.add_argument("--targetseq", default="")       # override apical fragment with explicit target .seq (e.g. full ectodomain)
    a = ap.parse_args()

    target = open(a.targetseq).read().strip() if a.targetseq else open(FRAG[a.species]).read().strip()
    od = (REPO/a.out); od.mkdir(parents=True, exist_ok=True)
    want = set(x for x in a.names.split(",") if x)
    rows = [(r["name"], (r.get("sequence") or r.get("seq")).strip())
            for r in csv.DictReader(open(a.seqs)) if (r.get("sequence") or r.get("seq"))]
    if want: rows = [r for r in rows if r[0] in want]
    if a.limit: rows = rows[:a.limit]

    jobs = []
    t_a3m = od/f"_target_{a.species}_g{a.gpu}.a3m"; t_a3m.write_text(f">target_{a.species}\n{target}\n")
    for nm, seq in rows:
        b_a3m = od/f"{nm}_binder.a3m"; b_a3m.write_text(f">{nm}\n{seq}\n")
        jobs.append({"name": nm, "sequences": [
            {"proteinChain": {"sequence": seq,    "count": 1, "id": ["A"], "unpairedMsaPath": str(b_a3m.resolve())}},
            {"proteinChain": {"sequence": target, "count": 1, "id": ["B"], "unpairedMsaPath": str(t_a3m.resolve())}},
        ]})
    ijson = od/f"jobs_{a.species}_g{a.gpu}.json"; ijson.write_text(json.dumps(jobs, indent=2))
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=a.gpu, OMP_NUM_THREADS="4", MKL_NUM_THREADS="4")
    cmd = [str(PROT), "pred", "-i", str(ijson), "-o", str(od), "-s", a.seeds, "-e", str(a.samples),
           "-c", str(a.cycle), "-p", str(a.step), "-n", "protenix_base_default_v1.0.0",
           "--use_msa", "true", "--use_template", "false"]
    print(f"RUN protenix {a.species} gpu={a.gpu} {len(jobs)} job(s) samples={a.samples} seeds={a.seeds}", flush=True)
    print("  " + " ".join(cmd), flush=True)
    raise SystemExit(subprocess.run(cmd, cwd=str(REPO), env=env).returncode)

if __name__ == "__main__":
    main()
