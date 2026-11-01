#!/usr/bin/env python3
# Build v25: v24 minus the 5 near-twin cousins, plus 5 new distinct Tier-A designs,
# re-ranked by switch>cross-reactivity>affinity. Writes CRLF CSV (name,sequence,molecule_class),
# then verifies: 20 rows, all sequences valid AA, no pair >=94% identity (genuinely varied).
import csv, re, sys
PROJ="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
SP="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
AA=set("ACDEFGHIKLMNPQRSTVWY")

# --- sources ---
v24={}
for i,ln in enumerate(open(f"{PROJ}/submissions/tfr1_track2_v24.csv")):
    if i==0: continue
    p=ln.rstrip("\r\n").split(",")
    if len(p)>=3: v24[p[0]]=(p[1],p[2])
    elif len(p)>=2: v24[p[0]]=(p[1],"protein")
new={}
for r in csv.DictReader(open(f"{SP}/v25_switch_select.csv")):
    new[r["name"]]=r["sequence"].strip()

# --- final ranked order (20) ---
ORDER=[
 "genie_w2g3_53__A27HK8_A13HR44",            # 1  LOCKED flagship
 "w3g0_174_mpnn1_sw3his",                    # 2  x-react M7 (proven)
 "resc_v25g3_80_mpnn1__A12HK9_A33HK69",      # 3  x-react M6 NEW
 "genie_w2g6_144_sw3b",                      # 4  x-react M3 (proven)
 "resc_w3g5_70__A85HR7_A51HR17",             # 5  x-react M5 (proven)
 "resc_v25g3_49_mpnn0__A26HK30_A20HK23",     # 6  x-react M2 NEW
 "w3g3_92_mpnn0_sw2his",                     # 7  M1
 "resc_w4g7_217__A19HK68_A26HK29",           # 8  M1
 "resc_genie_w2g5_111__A28HR29_A64HK35",     # 9  M1
 "resc_w4g1_195__A18HK22_A81HK11",           # 10 M1
 "resc_w4g1_286__A30HK12_A62HK45",           # 11 M1
 "resc_w4g0_194__A39HK22_A32HR35",           # 12 M1
 "resc_v25g6_84_mpnn1__A52HK67_A69HK73",     # 13 M0 strong binder (be7) NEW
 "w3g5_231_mpnn1_sw3his",                    # 14 M0
 "resc_e223_m3__A17HK21_A34HK37",            # 15 M0
 "w3g7_240_mpnn1_sw3his",                    # 16 M0
 "w3g6_146_mpnn0_sw2his",                    # 17 M0
 "w4g5_137_mpnn1_sw3his",                    # 18 M0
 "resc_v25g4_44_mpnn0__A70HK87_A60HR19",     # 19 M0 NEW
 "resc_v25g5_109_mpnn0__A11HK42_A19HK23",    # 20 M0 NEW
]
NEW_SET={"resc_v25g3_80_mpnn1__A12HK9_A33HK69","resc_v25g3_49_mpnn0__A26HK30_A20HK23",
         "resc_v25g6_84_mpnn1__A52HK67_A69HK73","resc_v25g4_44_mpnn0__A70HK87_A60HR19",
         "resc_v25g5_109_mpnn0__A11HK42_A19HK23"}
REMOVED={"genie_w2g3_53__A59HK21_A17HK48","genie_w2g6_144__A56HK48_A43HK39",
         "resc_w4g1_195__A12HR9_A81HK11","resc_w4g0_194__A39HK22_A30HK2",
         "resc_w4g1_286__A38HK70_A44HK47"}

# --- assemble ---
rows=[]
for n in ORDER:
    if n in NEW_SET:
        seq=new.get(n); mc="protein"
        assert seq, f"missing NEW seq {n}"
    else:
        assert n in v24, f"retained {n} not in v24"
        seq,mc=v24[n]
    assert all(c in AA for c in seq), f"bad AA in {n}"
    rows.append((n,seq,mc))

# --- checks ---
assert len(rows)==20, f"expected 20 got {len(rows)}"
assert len(set(r[0] for r in rows))==20, "dup names"
# removed cousins absent, new present
for r in REMOVED: assert r not in set(x[0] for x in rows), f"removed cousin still present {r}"
for n in NEW_SET: assert n in set(x[0] for x in rows), f"new design missing {n}"
# diversity: no pair >=94%
def ident(a,b):
    n=min(len(a),len(b)); m=max(len(a),len(b))
    return sum(1 for i in range(n) if a[i]==b[i])/m
worst=(0,"","")
for i in range(20):
    for j in range(i+1,20):
        v=ident(rows[i][1],rows[j][1])
        if v>worst[0]: worst=(v,rows[i][0],rows[j][0])
assert worst[0]<0.94, f"PAIR >=94%: {worst}"

# --- write CRLF ---
OUT=f"{PROJ}/submissions/tfr1_track2_v25.csv"
with open(OUT,"w",newline="") as f:
    f.write("name,sequence,molecule_class\r\n")
    for n,s,mc in rows:
        f.write(f"{n},{s},{mc}\r\n")

print(f"WROTE {OUT}  ({len(rows)} rows)")
print(f"max pairwise identity among all 20: {worst[0]*100:.1f}%  ({worst[1]} <-> {worst[2]})")
print(f"\nrank  design                                         len  src")
for k,(n,s,mc) in enumerate(rows,1):
    src="NEW" if n in NEW_SET else "v24"
    print(f"{k:>3}   {n:<46}{len(s):>4}  {src}")
