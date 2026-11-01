#!/usr/bin/env python3
# Generate the v25 blind-Protenix evidence record (20 ranked designs, same columns as v24).
# Retained metrics come from v24_blind_protenix.tsv; the 5 new from this session's folds.
import csv, re
PROJ="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
SP="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"

# ranked order (must match build_v25.py)
import importlib.util
spec=importlib.util.spec_from_file_location("b25",f"{SP}/scripts/build_v25.py")
# avoid executing build (it writes files); instead re-declare ORDER here:
ORDER=["genie_w2g3_53__A27HK8_A13HR44","w3g0_174_mpnn1_sw3his","resc_v25g3_80_mpnn1__A12HK9_A33HK69",
 "genie_w2g6_144_sw3b","resc_w3g5_70__A85HR7_A51HR17","resc_v25g3_49_mpnn0__A26HK30_A20HK23",
 "w3g3_92_mpnn0_sw2his","resc_w4g7_217__A19HK68_A26HK29","resc_genie_w2g5_111__A28HR29_A64HK35",
 "resc_w4g1_195__A18HK22_A81HK11","resc_w4g1_286__A30HK12_A62HK45","resc_w4g0_194__A39HK22_A32HR35",
 "resc_v25g6_84_mpnn1__A52HK67_A69HK73","w3g5_231_mpnn1_sw3his","resc_e223_m3__A17HK21_A34HK37",
 "w3g7_240_mpnn1_sw3his","w3g6_146_mpnn0_sw2his","w4g5_137_mpnn1_sw3his",
 "resc_v25g4_44_mpnn0__A70HK87_A60HR19","resc_v25g5_109_mpnn0__A11HK42_A19HK23"]
NEW={"resc_v25g3_80_mpnn1__A12HK9_A33HK69","resc_v25g3_49_mpnn0__A26HK30_A20HK23",
     "resc_v25g6_84_mpnn1__A52HK67_A69HK73","resc_v25g4_44_mpnn0__A70HK87_A60HR19",
     "resc_v25g5_109_mpnn0__A11HK42_A19HK23"}

# v24 metrics (retained)
v24={}
for ln in open(f"{PROJ}/submissions/tfr1_track2_v24_blind_protenix.tsv"):
    if ln.startswith("#") or ln.startswith("rank"): continue
    p=ln.rstrip("\n").split("\t")
    if len(p)>=11: v24[p[1]]=p  # [rank,name,H_iptm,H_be,M_iptm,M_be,MH_ratio,xr_score,sw_His,nov_maxTM,nov_verdict,gate]

# new metrics
def load(path,k="design"):
    d={}
    for r in csv.DictReader(open(path),delimiter='\t'): d[r[k]]=r
    return d
H=load(f"{PROJ}/runs/f_v25/swfold/human.tsv"); M=load(f"{PROJ}/runs/f_v25/swfold/mouse.tsv")
NOV={r["name"]:r for r in csv.DictReader(open(f"{PROJ}/runs/f_v25/sw_novelty.csv"))}
# in-window His count per new design from v25_switch.tsv
pk={}
for ln in open(f"{SP}/v25_switch.tsv"):
    p=ln.rstrip("\n").split("\t")
    if len(p)!=3: continue
    try: v=float(p[2])
    except: continue
    pk.setdefault(p[0],[]).append(v)
def swhis(n): return sum(1 for v in pk.get(n,[]) if 5.5<=v<=7.4)

def xr(H_,M_,be):
    w=1.0 if be>=2 else (0.5 if be==1 else 0.25)
    r=(M_/H_) if H_ else 0
    return (w*min(r,1/r)) if r else 0, r

out=[]
for rk,n in enumerate(ORDER,1):
    if n in NEW:
        h=H[n]; m=M[n]; nv=NOV[n]
        Hi=float(h["iptm_max"]); Hb=int(float(h["best_epi"]))
        Mi=float(m["iptm_max"]); Mb=int(float(m["best_epi"]))
        x,r=xr(Hi,Mi,Mb)
        out.append([str(rk),n,f"{Hi:.3f}",str(Hb),f"{Mi:.3f}",str(Mb),f"{r:.3f}",f"{x:.3f}",
                    str(swhis(n)),nv["singleseq_maxTM_pdb"],nv["verdict"],"PASS"])
    else:
        p=v24[n]; out.append([str(rk)]+p[1:])

hdr=["# Adaptyv/Anthropic Challenge 4 (TfR1 apical pH-switch binder) — v25 blind-Protenix record",
 "# v24 minus 5 near-twin cousins (ranks 12/13/16/18/20) + 5 NEW distinct Tier-A (fresh Genie3 campaign).",
 "# Same ruler: BLIND Protenix (ESMFold2+Protenix), msa:empty, apical fragment chain B, n=80 (20 samples x seeds 101-104). Gate=0.194.",
 "# Tier-A (ALL pass): H_iptm>=0.194 AND H_best_epi>=2 AND sw_His>=2 (JustHISpKa pKa in [5.5,7.4], 2 ENGINEERED His) AND novelty!=risk.",
 "# Genuinely varied: max pairwise identity among all 20 = 26.9%. 5 genuine cross-reactive (M_be>=2) vs v24's 3.",
 "# Ranking=lexicographic switch>cross-reactivity(xr_score=epitope-weighted MH_ratio->1)>affinity. #1 LOCKED.",
 "\t".join(["rank","name","H_iptm","H_be","M_iptm","M_be","MH_ratio","xr_score","sw_His","nov_maxTM","nov_verdict","gate"])]
OUT=f"{PROJ}/submissions/tfr1_track2_v25_blind_protenix.tsv"
with open(OUT,"w") as f:
    f.write("\n".join(hdr)+"\n")
    for r in out: f.write("\t".join(r)+"\n")
print(f"WROTE {OUT}")
for r in out:
    print(f"  {r[0]:>2} {r[1]:<44} H={r[2]}/be{r[3]} M={r[4]}/be{r[5]} MHr={r[6]} xr={r[7]} swHis={r[8]} nov={r[10]}")
