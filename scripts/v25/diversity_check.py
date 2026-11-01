#!/usr/bin/env python3
# Pairwise identity among: retained-15 v24 roster, genie_w1g0_112_sw2b, and the 11 switch candidates.
# Flags any pair >=94% (the "quiet near-twin" bar the user wants gone) and >=95.5% (portal flag).
# Uses ungapped identity over max length (calibrated: v24 flagged pairs 97%+, quiet pairs 94%).
import csv, re
PROJ="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
SP="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
REMOVE={"genie_w2g3_53__A59HK21_A17HK48","genie_w2g6_144__A56HK48_A43HK39",
        "resc_w4g1_195__A12HR9_A81HK11","resc_w4g0_194__A39HK22_A30HK2",
        "resc_w4g1_286__A38HK70_A44HK47"}   # the 5 cousins being dropped
retained={}
for i,ln in enumerate(open(f"{PROJ}/submissions/tfr1_track2_v24.csv")):
    if i==0: continue
    p=ln.rstrip("\r\n").split(",")
    if len(p)>=2 and p[0] not in REMOVE: retained[p[0]]=p[1]
cand={}
for r in csv.DictReader(open(f"{SP}/v25_switch_select.csv")):
    cand[r["name"]]=r["sequence"].strip()
cand["genie_w1g0_112_sw2b"]="MKIEELNNFVAKLAAAGKSYAHIARAVLEKHGKEALEEWIKNMSEVDPEAAKEAEKALKEAE"

def ident(a,b):
    if not a or not b: return 0.0
    n=min(len(a),len(b)); m=max(len(a),len(b))
    return sum(1 for i in range(n) if a[i]==b[i])/m

print(f"retained roster: {len(retained)}   new candidates (incl genie_112): {len(cand)}")
print(f"\n=== each candidate: MAX identity vs retained-15 roster ===")
for c,cs in cand.items():
    bn,bi=max(((rn,ident(cs,rs)) for rn,rs in retained.items()), key=lambda x:x[1])
    flag="  <-- >=94%!" if bi>=0.94 else ""
    print(f"  {c:<40} max {bi*100:5.1f}% vs {bn}{flag}")
print(f"\n=== pairwise among the {len(cand)} new candidates (flag >=94%) ===")
names=list(cand)
hits=0
for i in range(len(names)):
    for j in range(i+1,len(names)):
        v=ident(cand[names[i]],cand[names[j]])
        if v>=0.90:
            hits+=1
            tag="PORTAL-FLAG" if v>=0.955 else ("NEAR-TWIN>=94%" if v>=0.94 else "90-94%")
            print(f"  {v*100:5.1f}%  [{tag}]  {names[i]} <-> {names[j]}")
if hits==0: print("  (no candidate pair >=90% — all mutually distinct)")
# lineage summary
def bb(n): return re.sub(r"__A.*$","",re.sub(r"^resc_","",n))
print(f"\n=== candidate backbones (same-backbone pairs must not both be picked) ===")
seen={}
for c in cand: seen.setdefault(bb(c),[]).append(c)
for b,cs in seen.items():
    mark=" <-- SAME BACKBONE, pick ONE" if len(cs)>1 else ""
    print(f"  {b:<22} {cs}{mark}")
