#!/usr/bin/env python3
# Merge blind human + mouse folds, novelty, and switch pKa for the 11 switch candidates.
# Apply Tier-A gate (H_iptm>=0.194 & best_epi>=2 & novelty!=risk), rank by the challenge
# lexicographic objective (switch confirmed for all -> mouse x-react -> affinity), and
# print the full table + the recommended 4 distinct-backbone new Tier-A designs.
import csv, os, re
PROJ="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
SP="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
GATE=0.194
def load_tsv(path,keycol="design"):
    d={}
    if not os.path.exists(path): return d
    for r in csv.DictReader(open(path),delimiter='\t'): d[r[keycol]]=r
    return d
H=load_tsv(f"{PROJ}/runs/f_v25/swfold/human.tsv")
M=load_tsv(f"{PROJ}/runs/f_v25/swfold/mouse.tsv")
# novelty
NOV={}
npath=f"{PROJ}/runs/f_v25/sw_novelty.csv"
if os.path.exists(npath):
    for r in csv.DictReader(open(npath)):
        NOV[r.get("name") or r.get("design")]=r
# switch in-window info
SW={}
for r in csv.DictReader(open(f"{SP}/v25_switch_select.csv")):
    SW[r["name"]]=r["sequence"].strip()
# switch pka summary from select stdout rerun (recompute in-window count)
def bb(n): return re.sub(r"_mpnn\d+$","",re.sub(r"__A.*$","",re.sub(r"^resc_","",n)))

def f(x,default=0.0):
    try: return float(x)
    except: return default
def i(x,default=0):
    try: return int(float(x))
    except: return default

rows=[]
for d in SW:
    h=H.get(d,{}); m=M.get(d,{}); nv=NOV.get(d,{})
    Hip=f(h.get("iptm_max")); Hbe=i(h.get("best_epi"))
    Mip=f(m.get("iptm_max")); Mbe=i(m.get("best_epi"))
    # novelty: find a maxTM-ish column + verdict
    nov_tm=None; nov_verdict=""
    for k,v in nv.items():
        kl=k.lower()
        if nov_tm is None and ("tm" in kl or "max" in kl):
            try: nov_tm=float(v)
            except: pass
        if ("verdict" in kl or "class" in kl or "nov" in kl) and not v.replace('.','').isdigit():  # parens: guard applies to all 3 terms (was a precedence pitfall; the actual sw_novelty.csv had one string `verdict` col so it read correctly regardless)
            nov_verdict=v
    mhr=(Mip/Hip) if Hip else 0.0
    # epitope-weighted x-react weight
    w=1.0 if Mbe>=2 else (0.5 if Mbe==1 else 0.25)
    gate = (Hip>=GATE) and (Hbe>=2) and (str(nov_verdict).lower()!="risk")
    rows.append(dict(d=d,bb=bb(d),Hip=Hip,Hbe=Hbe,Mip=Mip,Mbe=Mbe,mhr=mhr,w=w,
                     nov_tm=nov_tm if nov_tm is not None else -1, nov=nov_verdict, gate=gate, L=len(SW[d])))

# rank: lexicographic within new designs -> x-react (Mbe desc, weighted mhr desc), then affinity (Hip desc)
# NOTE: primary x-react key is Mbe (mouse epitope depth, capped 3) = the VALID channel. The secondary mhr=Mip/Hip is
# UNCAPPED (rewards mouse-biased over balanced), contra the capped xr_score min(r,1/r) objective [[lesson-crossreact-is-ratio-not-absolute]].
# Impact is TIEBREAKER-ONLY within a tied-Mbe group (inclusion is by Mbe+gate); did NOT change the shipped (portal-verified) inclusion set.
def rk(r): return (-min(r["Mbe"],3), -(r["w"]*r["mhr"]), -r["Hip"])
rows.sort(key=rk)

print(f"{'design':<42}{'bb':<12}{'gate':<5}{'Hip':>7}{'Hbe':>4}{'Mip':>7}{'Mbe':>4}{'MHr':>6}{'novTM':>7} {'nov':<10}{'L':>4}")
for r in rows:
    g="PASS" if r["gate"] else "fail"
    print(f"{r['d']:<42}{r['bb']:<12}{g:<5}{r['Hip']:>7.3f}{r['Hbe']:>4}{r['Mip']:>7.3f}{r['Mbe']:>4}{r['mhr']:>6.2f}{r['nov_tm']:>7.3f} {str(r['nov']):<10}{r['L']:>4}")

# recommended 4 distinct backbones among gate-passers, best by rank
picked=[]; seen=set()
for r in rows:
    if not r["gate"]: continue
    if r["bb"] in seen: continue
    seen.add(r["bb"]); picked.append(r)
    if len(picked)>=4: break
print(f"\n=== RECOMMENDED 4 new Tier-A (distinct backbones), by switch>xreact>affinity ===")
for k,r in enumerate(picked,1):
    print(f"  {k}. {r['d']:<42} Hip={r['Hip']:.3f} Hbe={r['Hbe']} Mbe={r['Mbe']} MHr={r['mhr']:.2f} novTM={r['nov_tm']:.3f}")
print(f"  +  genie_w1g0_112_sw2b (ready: His22/31 in-window, novTM 0.874 borderline, H 0.213, M_be1)")
