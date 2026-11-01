#!/usr/bin/env python3
# CPU-free developability pre-screen of the 110 multi-state cross-reactivity candidates vs v25 baseline.
# Flags hydrophobic blobs (multi-state MPNN can over-pack the two interfaces) BEFORE spending folds.
import csv
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
HYD=set("AILMFVWYC"); POS=set("KR"); NEG=set("DE")
def metrics(s):
    n=len(s)
    fh=sum(c in HYD for c in s)/n
    net=sum(c in POS for c in s)-sum(c in NEG for c in s)
    # longest contiguous hydrophobic run
    run=mx=0
    for c in s:
        if c in HYD: run+=1; mx=max(mx,run)
        else: run=0
    return n,round(fh,3),net,mx
def load(path,seqcol='sequence',namecol='name'):
    out=[]
    for r in csv.DictReader(open(path)):
        s=(r.get(seqcol) or r.get('seq') or '').strip()
        if s: out.append((r.get(namecol,'?'),s))
    return out
# v25 baseline
v25=load(f"{REPO}/submissions/tfr1_track2_v25.csv")
import statistics as st
v25m=[metrics(s) for _,s in v25]
print("=== v25 baseline (passes expression) ===")
print(f"  n={len(v25)}  %hyd mean={st.mean(m[1] for m in v25m):.3f} [{min(m[1] for m in v25m):.3f},{max(m[1] for m in v25m):.3f}]"
      f"  net mean={st.mean(m[2] for m in v25m):+.1f}  maxHydRun mean={st.mean(m[3] for m in v25m):.1f} max={max(m[3] for m in v25m)}")
# ms candidates
ms=load(f"{SC}/ms/mpnn/ms_binders.csv")
rows=[]
for nm,s in ms:
    n,fh,net,mx=metrics(s)
    rows.append((nm,s,n,fh,net,mx))
# pass if within v25 envelope: %hyd<=0.52 (v25 max + margin), maxHydRun<=9, net in [-12,12]
V25_FH=max(m[1] for m in v25m); V25_RUN=max(m[3] for m in v25m)
fh_cut=max(0.50, V25_FH+0.02); run_cut=max(8, V25_RUN+1)
def ok(fh,net,mx): return fh<=fh_cut and mx<=run_cut and -14<=net<=14
npass=sum(1 for r in rows if ok(r[3],r[4],r[5]))
print(f"\n=== ms candidates (n={len(rows)}) ===")
print(f"  %hyd mean={st.mean(r[3] for r in rows):.3f} [{min(r[3] for r in rows):.3f},{max(r[3] for r in rows):.3f}]"
      f"  maxHydRun mean={st.mean(r[5] for r in rows):.1f} max={max(r[5] for r in rows)}")
print(f"  cutoffs: %hyd<={fh_cut:.2f}  maxHydRun<={run_cut}  net in[-14,14]")
print(f"  PASS dev-screen: {npass}/{len(rows)}")
# per-backbone pass count + best (lowest %hyd) per backbone
import re
bb={}
for nm,s,n,fh,net,mx in rows:
    b=re.sub(r'_s\d+$','',nm.replace('ms_',''))
    bb.setdefault(b,[]).append((fh,mx,net,nm,s,ok(fh,net,mx)))
print("\nbackbone  passed/total  best%hyd")
clean=[]
for b in sorted(bb):
    lst=sorted(bb[b])
    p=sum(1 for x in lst if x[5])
    print(f"  {b:<18} {p}/{len(lst)}   best={lst[0][0]:.3f}")
    for fh,mx,net,nm,s,passed in lst:
        if passed: clean.append((nm,s,fh,mx,net))
# write clean set
with open(f"{SC}/ms_clean.csv","w") as f:
    w=csv.writer(f); w.writerow(["name","sequence","pct_hyd","maxHydRun","net"])
    for r in clean: w.writerow(r)
print(f"\nwrote {SC}/ms_clean.csv  ({len(clean)} candidates pass dev-screen)")
