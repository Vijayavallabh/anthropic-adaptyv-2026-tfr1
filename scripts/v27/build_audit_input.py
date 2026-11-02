#!/usr/bin/env python3
# Build the uniform binding-audit input: the 20 EXACT v26 submission sequences (switch muts installed)
# + POS_3DS18 + NEG_scramble1 + NEG_scramble2, so all 23 fold in ONE calibrated blind-Protenix run.
import csv
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
V26=f"{REPO}/submissions/tfr1_track2_v26.csv"
OUT=f"{SC}/audit_input.csv"
BASE=[  # calibration anchors (exact seqs from prior ruler runs)
 ("POS_3DS18",   "DEREEEQRRRLEEVKEEAKRRERSEQDLAVLYLEAVNAAVVFVADSEEEAKRVADIVKKLVPEVIIFVHDNFVVFVVDSDEAARRVYEIVERA"),
 ("NEG_scramble1","EEVAEEVQFRENASEYVPARFRDVYEVKAAVHVDLAAVRVFRRRVKLERREKASVSEFLDIDLLIAIERRVEQKADENVKVVVEEEIAVDEDE"),
 ("NEG_scramble2","FAEEDFKVQDVENHRNEEVLRVKRVARPVIIYARSVEVIVDEALRLDSREEVAAIYRAKEEERVVLVEVEEDVKREAQVRVSEAFFDEKLAAD"),
]
rows=[]
for r in csv.DictReader(open(V26)):
    rows.append((r["name"].strip(), r["sequence"].strip()))
assert len(rows)==20, f"v26 has {len(rows)} rows"
with open(OUT,"w",newline="") as f:
    w=csv.writer(f); w.writerow(["name","sequence","molecule_class"])
    for n,s in rows: w.writerow([n,s,"protein"])
    for n,s in BASE:
        assert s.isalpha(); w.writerow([n,s,"protein"])
print(f"wrote {OUT}: {len(rows)} submission + {len(BASE)} calibration = {len(rows)+len(BASE)} rows")
