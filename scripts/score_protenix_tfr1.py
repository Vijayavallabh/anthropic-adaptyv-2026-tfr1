#!/usr/bin/env python3
"""Score the Protenix blind co-folds (organizers' outside judge). Inference-time scaling: rank poses
by ipTM and read the TOP ones (not the diffuse mean). For each design report:
  - ipTM max / median (binding confidence on the apical fragment)
  - apical-epitope overlap of the best pose + top-k ipTM-weighted (did it land on the epitope?)
  - on_epitope_rate = fraction of top-k poses that bury >=2 epitope residues
A design that holds the apical epitope under BLIND Protenix with heavy sampling is strongly validated;
one that drifts is a pocket-restraint artifact the organizers' blind judge will miss.

Target chain B = apical fragment (resid = UniProt-188). Human epitope chainB resids
{14,15,16,20,21,22,23,24,160,183}; mouse widened +-3 past the 210-212 indel.
Usage: score_protenix_tfr1.py <protenix_out_dir> --species human|mouse [--topk 10] [--tsv out.tsv]
Drafted by the assistant (ambition-lift depth pass, 2026-10-27)."""
import argparse, glob, json, re, sys
from pathlib import Path
from collections import defaultdict
import numpy as np
import gemmi

#  The repo's mouse apical fragment is a SAME-LENGTH (195 aa) point-mutation surrogate (human fragment +
#  6 divergent apical residues 204Q/208N/211D/212P/348K/371Q), NOT the indel-containing true mouse seq,
#  so chain-B numbering is identical to human -> same epitope residue set for both species.
_EPI = {14,15,16,20,21,22,23,24,160,183}
EPI = {"human": _EPI, "mouse": _EPI}

def chains_target_binder(model):
    by = {c.name: c for c in model}
    if "B" in by and "A" in by: return by["B"], by["A"]          # B=target, A=binder (job id order)
    cs = sorted(model, key=lambda c: -sum(1 for _ in c)); return cs[0], cs[1]  # fallback: longest=target

def target_contacts(cif, cutoff=5.0):
    st = gemmi.read_structure(cif); m = st[0]
    tgt, bnd = chains_target_binder(m)
    ba = np.array([[a.pos.x,a.pos.y,a.pos.z] for r in bnd for a in r])
    if not len(ba): return []
    hits=[]
    for r in tgt:
        ra = np.array([[a.pos.x,a.pos.y,a.pos.z] for a in r])
        if len(ra) and np.sqrt(((ra[:,None,:]-ba[None,:,:])**2).sum(-1)).min() <= cutoff:
            hits.append(r.seqid.num)
    return hits

def poses(fold):
    out=[]
    for cj in glob.glob(f"{fold}/**/*_summary_confidence_sample_*.json", recursive=True):
        try: d=json.load(open(cj))
        except: continue
        cif=cj.replace("_summary_confidence_sample_","_sample_").replace(".json",".cif")
        if Path(cif).exists(): out.append((float(d.get("iptm",0.0)), float(d.get("ptm",0.0)), cif))
    out.sort(reverse=True); return out

def score_design(fold, epi, topk=10):
    ps=poses(fold)
    if not ps: return None
    iptms=[p[0] for p in ps]
    best_rc=set(target_contacts(ps[0][2]))
    best_epi=len(best_rc & epi)
    # top-k ipTM-weighted epitope fraction + on-epitope rate
    on=0; wepi=0.0; wtot=0.0
    for iptm,ptm,cif in ps[:topk]:
        rc=set(target_contacts(cif))
        ne=len(rc & epi)
        if ne>=2: on+=1
        if rc: wepi += iptm*ne/len(rc)
        wtot += iptm
    return dict(n=len(ps), iptm_max=max(iptms), iptm_med=float(np.median(iptms)),
                best_iptm=ps[0][0], best_epi=best_epi, best_ncontact=len(best_rc),
                topk=min(topk,len(ps)), on_epi_rate=on/min(topk,len(ps)),
                wepi_frac=(wepi/wtot if wtot else 0.0))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("outdir"); ap.add_argument("--species",required=True,choices=["human","mouse"])
    ap.add_argument("--topk",type=int,default=10); ap.add_argument("--tsv",default="")
    ap.add_argument("--epitope",default="")   # override chain-B epitope resids (comma list), e.g. full-ecto numbering
    a=ap.parse_args()
    epi=set(int(x) for x in a.epitope.split(",")) if a.epitope else EPI[a.species]
    base=Path(a.outdir)
    folds=sorted(d for d in base.iterdir() if d.is_dir()) if base.exists() else []
    rows=[]
    hdr=f"{'design':36} {'n':>3} {'iptm_max':>8} {'iptm_med':>8} {'best_epi':>8} {'on_rate':>7} {'wepi':>5}"
    print(hdr); print("-"*len(hdr))
    for f in folds:
        s=score_design(str(f), epi, a.topk)
        if not s: continue
        rows.append((f.name,s))
        print(f"{f.name[:36]:36} {s['n']:>3} {s['iptm_max']:>8.3f} {s['iptm_med']:>8.3f} "
              f"{s['best_epi']:>8} {s['on_epi_rate']:>7.2f} {s['wepi_frac']:>5.2f}")
    if a.tsv and rows:
        with open(a.tsv,"w") as fo:
            fo.write("design\tn\tiptm_max\tiptm_med\tbest_iptm\tbest_epi\tbest_ncontact\ton_epi_rate\twepi_frac\n")
            for n,s in rows:
                fo.write(f"{n}\t{s['n']}\t{s['iptm_max']:.4f}\t{s['iptm_med']:.4f}\t{s['best_iptm']:.4f}\t"
                         f"{s['best_epi']}\t{s['best_ncontact']}\t{s['on_epi_rate']:.3f}\t{s['wepi_frac']:.4f}\n")
        print(f"\nWROTE {a.tsv} ({len(rows)} designs)")

if __name__=="__main__": main()
