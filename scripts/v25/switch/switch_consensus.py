#!/usr/bin/env python3
# Consensus switch grade: JustHISpKa (His-in-window, from v25 record) x PROPKA Wyman two-state
# (ddg_pH release, from switch_score_driver). NOT a unilateral re-ranker — report agreement/conflict.
#   CONFIRMED  : sw_His>=2 (JustHISpKa) AND mean_ddg<0 AND frac_release>=0.5 (PROPKA) -> two methods agree
#   LEAN-REL   : sw_His>=2 AND mean_ddg<0 but frac_release<0.5 (direction ok, pose-noisy)
#   CONFLICT   : sw_His>=2 but mean_ddg>=0 (His titrates but complex doesn't loosen -> 3rd-method check)
import csv, sys, os
PROJ="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
rec=sys.argv[1] if len(sys.argv)>1 else f"{PROJ}/submissions/tfr1_track2_v25_blind_protenix.tsv"
sw=sys.argv[2] if len(sys.argv)>2 else "/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad/switch_md_v25.tsv"
# v25 record: rank,name,...,sw_His (col 9, idx8)
V={}
for ln in open(rec):
    if ln.startswith("#") or ln.startswith("rank"): continue
    p=ln.rstrip("\n").split("\t")
    if len(p)>=12: V[p[1]]=dict(rank=int(p[0]),Mbe=int(p[5]),swHis=int(p[8]),nov=p[10])
# propka scores
P={}
if os.path.exists(sw):
    for r in csv.DictReader(open(sw),delimiter='\t'):
        try: P[r['design']]=dict(mean=float(r['mean_ddg']),mn=float(r['min_ddg']),frac=float(r['frac_release']),n=int(r['n_poses']),dets=r.get('best_dets',''))
        except: P[r['design']]=None
def cls(swHis,pr):
    if pr is None: return "NO-PROPKA"
    if swHis>=2 and pr['mean']<-0.02 and pr['frac']>=0.5: return "CONFIRMED"
    if swHis>=2 and pr['mean']<-0.02: return "LEAN-REL"
    if swHis>=2 and pr['mean']>=-0.02: return "CONFLICT"
    return "WEAK"
rows=sorted(V.items(), key=lambda kv: kv[1]['rank'])
print(f"{'rk':>2} {'design':<42}{'swHis':>5}{'Mbe':>4}{'mean_ddg':>9}{'min_ddg':>8}{'fracRel':>8}  {'consensus':<10}")
cnt={}
for n,v in rows:
    pr=P.get(n); c=cls(v['swHis'],pr); cnt[c]=cnt.get(c,0)+1
    if pr: print(f"{v['rank']:>2} {n:<42}{v['swHis']:>5}{v['Mbe']:>4}{pr['mean']:>9.3f}{pr['mn']:>8.3f}{pr['frac']:>8.2f}  {c:<10}")
    else:  print(f"{v['rank']:>2} {n:<42}{v['swHis']:>5}{v['Mbe']:>4}{'NA':>9}{'NA':>8}{'NA':>8}  {c:<10}")
print(f"\n=== CONSENSUS TALLY ===")
for k in ["CONFIRMED","LEAN-REL","CONFLICT","WEAK","NO-PROPKA"]:
    if cnt.get(k): print(f"  {k}: {cnt[k]}")
print("CONFIRMED = both methods agree genuine pH-release switch (the honest #1-metric upgrade).")
print("CONFLICT = JustHISpKa in-window but PROPKA says complex doesn't loosen -> flag for 3rd method, do NOT swap on this alone.")
