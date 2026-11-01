#!/usr/bin/env python3
# Parse v25_switch.tsv (design \t sid \t pka), gate designs with >=2 His pKa in [5.5,7.4],
# pick the best switch combo per design-base (backbone+mpnn), attach the full switch sequence
# from the combos CSVs, and emit a ranked CSV ready for blind-Protenix folding.
import csv, os, re, glob, sys
B = "/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
TSV = f"{B}/v25_switch.tsv"
COMBO_DIR = f"{B}/v25sw/combos"
OUT = f"{B}/v25_switch_select.csv"
LO, HI = 5.5, 7.4            # physiological switch window
CENTER = 6.7                 # ideal His pKa for max Δn_H across serum7.4<->endosome6.0

# --- load pKa ---
pkas = {}   # design -> [(sid, pka), ...]
for row in open(TSV):
    p = row.rstrip("\n").split("\t")
    if len(p) != 3: continue
    d, sid, v = p
    try: v = float(v)
    except: continue
    pkas.setdefault(d, []).append((int(sid), v))

# --- load sequences from combos CSVs ---
seqs = {}
for cf in glob.glob(f"{COMBO_DIR}/*.csv"):
    for r in csv.DictReader(open(cf)):
        seqs[r["name"]] = r["sequence"].strip()   # source combos carry a trailing \n inside the field

def introduced(d):
    # positions mutated to His: naming is __A<p1>H<X><c1>_A<p2>H<Y><c2>
    # (double underscore before first block, single before second) -> match _A<pos>H[KR]
    return set(int(m) for m in re.findall(r"_A(\d+)H[KR]", d))

def base(d):   # backbone + mpnn variant (one sequence family)
    return re.sub(r"__A.*$", "", d)

def backbone(d):  # strip mpnn too -> lineage for diversity
    return re.sub(r"_mpnn\d+$", "", base(d))

rows = []
for d, lst in pkas.items():
    intro = introduced(d)
    inwin = [(s, v) for (s, v) in lst if LO <= v <= HI]
    n_in = len(inwin)
    # introduced His that landed in window (the designed switch residues)
    intro_in = [(s, v) for (s, v) in inwin if s in intro]
    if n_in < 2:
        continue
    seq = seqs.get(d)
    if not seq:
        continue
    # centeredness score: lower = better (sum of |pka-CENTER| over in-window His, best 2)
    best2 = sorted(inwin, key=lambda sv: abs(sv[1]-CENTER))[:2]
    center_pen = sum(abs(v-CENTER) for _, v in best2)
    rows.append(dict(design=d, base=base(d), backbone=backbone(d),
                     n_in=n_in, n_intro_in=len(intro_in),
                     inwin=";".join(f"{s}:{v:.2f}" for s, v in sorted(inwin)),
                     center_pen=round(center_pen, 3), seq=seq, L=len(seq)))

# best combo per base: prefer >=2 introduced-in-window, then n_in, then centered
def keyfn(r): return (-min(r["n_intro_in"],2), -r["n_in"], r["center_pen"])
bybase = {}
for r in rows:
    bybase.setdefault(r["base"], []).append(r)
best = [sorted(v, key=keyfn)[0] for v in bybase.values()]
best.sort(key=lambda r: (r["backbone"], keyfn(r)))

# write all gate-passing best-per-base
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name","sequence"])
    for r in best:
        w.writerow([r["design"], r["seq"]])

print(f"designs with >=2 His in [{LO},{HI}]: {len(rows)} combos across {len(bybase)} design-bases")
print(f"distinct backbones represented: {len(set(r['backbone'] for r in best))}")
print(f"\n{'design':<46} {'bb':<12} {'n_in':>4} {'nIin':>4} {'cpen':>5} {'L':>3}  in-window(sid:pka)")
for r in best:
    print(f"{r['design']:<46} {r['backbone']:<12} {r['n_in']:>4} {r['n_intro_in']:>4} {r['center_pen']:>5.2f} {r['L']:>3}  {r['inwin']}")
print(f"\n-> {OUT}")
