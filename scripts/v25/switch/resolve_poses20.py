#!/usr/bin/env python3
# Resolve a bound-complex pose for each of the 20 v25 designs, preferring:
#   1) HUMAN Protenix fold DIR (seed_*/predictions with iptm jsons) -> top-K by iptm
#   2) MOUSE Protenix fold DIR (second choice; 75% id, direction check only)
#   3) Boltz model_0.pdb (single pose)
# Emits pose_map20.tsv: name<TAB>kind(cifdir|pdb)<TAB>path<TAB>src(human/mouse/boltz)
import os, glob, sys
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
NAMES=["genie_w2g3_53__A27HK8_A13HR44","w3g0_174_mpnn1_sw3his","resc_v25g3_80_mpnn1__A12HK9_A33HK69",
"genie_w2g6_144_sw3b","resc_w3g5_70__A85HR7_A51HR17","resc_v25g3_49_mpnn0__A26HK30_A20HK23",
"w3g3_92_mpnn0_sw2his","resc_w4g7_217__A19HK68_A26HK29","resc_genie_w2g5_111__A28HR29_A64HK35",
"resc_w4g1_195__A18HK22_A81HK11","resc_w4g1_286__A30HK12_A62HK45","resc_w4g0_194__A39HK22_A32HR35",
"resc_v25g6_84_mpnn1__A52HK67_A69HK73","w3g5_231_mpnn1_sw3his","resc_e223_m3__A17HK21_A34HK37",
"w3g7_240_mpnn1_sw3his","w3g6_146_mpnn0_sw2his","w4g5_137_mpnn1_sw3his",
"resc_v25g4_44_mpnn0__A70HK87_A60HR19","resc_v25g5_109_mpnn0__A11HK42_A19HK23"]
SEARCH_ROOTS=["runs", f"{SC}/fold_out", f"{SC}/rescue_out", f"{SC}/rescue2_out",
              f"{SC}/rescue3_out", f"{SC}/ms"]

def cif_dirs_for(name):
    """Find Protenix design dirs (containing seed_*/predictions/*_sample_*.cif) for this exact name."""
    hits=[]
    for root in SEARCH_ROOTS:
        base=root if os.path.isabs(root) else f"{REPO}/{root}"
        if not os.path.isdir(base): continue
        # a design dir is one whose basename == name and which has a seed_*/predictions child with cifs
        for d,_,_ in os.walk(base):
            if os.path.basename(d)==name:
                if glob.glob(f"{d}/**/*_sample_*.cif", recursive=True):
                    hits.append(d)
    return hits

def boltz_pdb_for(name):
    pats=[]
    for root in SEARCH_ROOTS:
        base=root if os.path.isabs(root) else f"{REPO}/{root}"
        pats += glob.glob(f"{base}/**/predictions/*{name}*/*{name}*_model_0.pdb", recursive=True)
    return pats

def classify_src(path):
    p=path.lower()
    if "/human/" in p or "boltz_h" in p or "/human" in p: return "human"
    if "/mouse/" in p or "boltz_m" in p or "/mouse" in p: return "mouse"
    return "?"

rows=[]
for n in NAMES:
    cifds=cif_dirs_for(n)
    human=[d for d in cifds if classify_src(d)=="human"]
    mouse=[d for d in cifds if classify_src(d)=="mouse"]
    other=[d for d in cifds if classify_src(d) not in ("human","mouse")]
    if human:
        rows.append((n,"cifdir",human[0],"human")); continue
    if other:
        rows.append((n,"cifdir",other[0],"protenix?")); continue
    # try boltz human pdb before falling to mouse cif
    bpdb=boltz_pdb_for(n)
    bh=[p for p in bpdb if classify_src(p)=="human"]
    if bh:
        rows.append((n,"pdb",bh[0],"boltz_h")); continue
    if mouse:
        rows.append((n,"cifdir",mouse[0],"mouse")); continue
    if bpdb:
        rows.append((n,"pdb",bpdb[0],classify_src(bpdb[0]) and ("boltz_"+classify_src(bpdb[0])[0]))); continue
    rows.append((n,"NONE","","-"))

out=f"{SC}/pose_map20.tsv"
with open(out,"w") as f:
    for r in rows: f.write("\t".join(r)+"\n")
for r in rows: print(f"{r[3]:<10} {r[1]:<7} {r[0]:<42} {r[2]}")
print(f"\nwrote {out}")
