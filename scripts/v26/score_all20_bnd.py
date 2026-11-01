#!/usr/bin/env python3
# Re-score the 20 on CACHED poses (no folds), isolating the DESIGNED mechanism:
# binder-His-only two-state ddg (drop incidental target-His chemistry that adds pose noise).
# ddg_bnd = sum over chain-A (binder) His of the Wyman per-His contribution.
import sys, glob, re, numpy as np
sys.path.insert(0,"/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad/scripts")
from ph_release_tfr1 import score
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
MAP=f"{SC}/pose_map20.tsv"; OUT=f"{SC}/switch20_bnd.tsv"
DET=re.compile(r'([AB]\d+)\((bnd|tgt)\):dpKa([+-][\d.]+),ddg([+-][\d.]+)')
rows=[["design","mean_bnd","min_bnd","n_poses","frac_bnd","max_bnd_dpKa","bnd_dets"]]
for ln in open(MAP):
    name,kind,path,src=ln.rstrip("\n").split("\t")
    pre=f"{SC}/sw20/poses/{name}"
    poses=sorted(glob.glob(pre+"_r*.pdb"))
    if not poses:
        rows.append([name,"NA","NA","0","NA","NA","-"]); continue
    bnd_ddgs=[]; rels=[]; best=None; bestv=1e9; maxdp=0.0
    for pdb in poses:
        r=score(pdb)
        if r is None: continue
        bsum=0.0; bdets=[]
        for m in DET.finditer(r['dets']):
            res,side,dpka,ddg=m.group(1),m.group(2),float(m.group(3)),float(m.group(4))
            if side=="bnd":
                bsum+=ddg; bdets.append(f"{res}:dpKa{dpka:+.2f},ddg{ddg:+.3f}")
                if abs(dpka)>abs(maxdp): maxdp=dpka
        bnd_ddgs.append(bsum); rels.append(1 if bsum<-0.02 else 0)
        if bsum<bestv: bestv=bsum; best=";".join(bdets)
    if bnd_ddgs:
        rows.append([name,f"{np.mean(bnd_ddgs):.3f}",f"{min(bnd_ddgs):.3f}",str(len(bnd_ddgs)),
                     f"{np.mean(rels):.2f}",f"{maxdp:+.2f}",best or "-"])
        print(f"{name:<42} mean_bnd{np.mean(bnd_ddgs):+.3f} min{min(bnd_ddgs):+.3f} frac{np.mean(rels):.2f} maxdpKa{maxdp:+.2f}")
    else:
        rows.append([name,"NA","NA","0","NA","NA","-"]); print(f"{name:<42} NA")
open(OUT,"w").write("\n".join("\t".join(r) for r in rows)+"\n")
print(f"\nwrote {OUT}")
