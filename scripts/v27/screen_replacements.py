#!/usr/bin/env python3
# Shortlist clean switch-validated REPLACEMENT candidates for the 2 pulled v26 members (rank15 resc_e223_m3,
# rank18 w4g5_137). Source = v25 switch pool (diverse backbones) + rescue pools. Filter: >=2 His in-window
# [5.5,7.4]; NOT in v26; distinct backbone from v26 members. Output a diverse shortlist CSV to confirm-fold.
import csv, re, collections
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
LO,HI=5.5,7.4
# in-window His count per design from pKa pools
def inwin(f):
    cnt=collections.Counter()
    for ln in open(f):
        p=ln.rstrip("\n").split("\t")
        if len(p)<3: continue
        try: pk=float(p[2])
        except: continue
        if LO<=pk<=HI: cnt[p[0]]+=1
    return cnt
win=collections.Counter()
for f in ["v25_switch.tsv","rescue_switch.tsv","rescue2_switch.tsv","rescue3_switch.tsv"]:
    try: win.update(inwin(f"{SC}/{f}"))
    except FileNotFoundError: pass
# sequences from combo pools
seq={}
for f in ["v25sw/all_combos.csv","rescue/all_combos.csv","rescue2/all_combos.csv","rescue3/all_combos.csv"]:
    try:
        for r in csv.DictReader(open(f"{SC}/{f}")):
            n=r.get("name","").strip(); s=(r.get("sequence") or "").strip()
            if n and s and n not in seq: seq[n]=s
    except FileNotFoundError: pass
# v26 members + their backbones (base before __, and the vXXgY_NN core)
v26=[r["name"].strip() for r in csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v26.csv"))]
def backbone(n): return n.split("__")[0]
def core(n):
    m=re.search(r'(v25g\d+_\d+|w\dg\d+_\d+|g\d+_\d+|genie_w\dg\d+_\d+|e\d+)', n)
    return m.group(1) if m else backbone(n)
v26_bb=set(backbone(n) for n in v26); v26_core=set(core(n) for n in v26)
# HARD-EXCLUDE cores: g4_92 = known mouse-phantom artifact; g3_22/g3_65 = near-twins of the 2 swaps at ranks 17/19.
BAD=re.compile(r'g4_92|g3_22|g3_65')
cands=[]
for n,w in win.items():
    if w<2 or n not in seq: continue
    if n in v26: continue
    if backbone(n) in v26_bb or core(n) in v26_core: continue
    if BAD.search(n): continue
    cands.append((n, w, len(seq[n]), seq[n]))
# diversity: up to 2 best (max in-window His) per core; prefer distinct cores
bycore=collections.defaultdict(list)
for n,w,L,s in cands: bycore[core(n)].append((n,w,L,s))
picks=[]
for c,lst in bycore.items():
    lst.sort(key=lambda x:-x[1]); picks.extend(lst[:2])   # up to 2 best switch per core
picks.sort(key=lambda x:(-x[1], x[0]))
SHORT=picks[:16]
print(f"switch-validated(>=2 His) not-in-v26 distinct-core candidates: {len(picks)} cores; shortlisting {len(SHORT)}")
with open(f"{SC}/repl_shortlist.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["name","sequence","molecule_class"])
    for n,wi,L,s in SHORT: w.writerow([n,s,"protein"])
    # anchors
    for n,s in [("POS_3DS18","DEREEEQRRRLEEVKEEAKRRERSEQDLAVLYLEAVNAAVVFVADSEEEAKRVADIVKKLVPEVIIFVHDNFVVFVVDSDEAARRVYEIVERA"),
                ("NEG_scramble1","EEVAEEVQFRENASEYVPARFRDVYEVKAAVHVDLAAVRVFRRRVKLERREKASVSEFLDIDLLIAIERRVEQKADENVKVVVEEEIAVDEDE"),
                ("NEG_scramble2","FAEEDFKVQDVENHRNEEVLRVKRVARPVIIYARSVEVIVDEALRLDSREEVAAIYRAKEEERVVLVEVEEDVKREAQVRVSEAFFDEKLAAD")]:
        w.writerow([n,s,"protein"])
print(f"wrote {SC}/repl_shortlist.csv ({len(SHORT)} cands + 3 anchors)")
for n,wi,L,s in SHORT: print(f"  {n:46} His_in_win={wi} len={L}")
