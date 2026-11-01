#!/usr/bin/env python3
# Merge v25 record axes + two-state PROPKA Wyman reads (total-His and binder-His-only)
# into ONE committed evidence doc. This is a CONSENSUS/EVIDENCE layer, NOT a re-ranker:
# the portal-verified v25 ranking is preserved; PROPKA and JustHISpKa disagree > the pH window,
# so no swap/reorder is made on PROPKA alone (owner + side-agent directive).
import csv
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
REC=f"{REPO}/submissions/tfr1_track2_v25_blind_protenix.tsv"
TOT=f"{SC}/switch20.tsv"; BND=f"{SC}/switch20_bnd.tsv"
OUT=f"{REPO}/submissions/tfr1_track2_v25_switch_consensus.tsv"

rec={}
for ln in open(REC):
    if ln.startswith("#") or ln.startswith("rank"): continue
    p=ln.rstrip("\n").split("\t")
    if len(p)<12: continue
    rec[p[1]]=dict(rank=int(p[0]),H_iptm=p[2],M_be=int(p[5]),swHis=int(p[8]),nov=p[10])
def load(f):
    d={}
    for r in csv.DictReader(open(f),delimiter='\t'):
        d[r['design']]=r
    return d
tot=load(TOT); bnd=load(BND)

def cls(mb, mn, frac):
    try: mb=float(mb); mn=float(mn); frac=float(frac)
    except: return "NA"
    if mb>0 and mn<=-0.05: return "NOISY"          # pose-variable, one pose wrong-direction
    if mb<=-0.05 and frac>=0.5: return "INTERFACE-STRONG"  # binder-His pKa couples to binding, both methods agree
    if mb<=-0.015: return "INTERFACE-WEAK"         # borderline coupling
    return "TITRATABLE-ONLY"                        # JustHISpKa in-window but binding-decoupled in this test (intramolecular/surface His)

hdr=["rank","name","H_iptm","M_be","sw_His_JHP","nov","ddg_tot","fracRel_tot","ddg_bnd","min_bnd","fracRel_bnd","max_bnd_dpKa","switch_class"]
rows=[]
for n,v in rec.items():
    t=tot.get(n,{}); b=bnd.get(n,{})
    rows.append([v['rank'],n,v['H_iptm'],v['M_be'],v['swHis'],v['nov'],
                 t.get('mean_ddg','NA'),t.get('frac_release','NA'),
                 b.get('mean_bnd','NA'),b.get('min_bnd','NA'),b.get('frac_bnd','NA'),b.get('max_bnd_dpKa','NA'),
                 cls(b.get('mean_bnd','NA'),b.get('min_bnd','NA'),b.get('frac_bnd','NA'))])
rows.sort(key=lambda r:r[0])
HEAD=[
"# Adaptyv/Anthropic Challenge 4 (TfR1 apical pH-switch binder) — v25 TWO-STATE SWITCH CONSENSUS (evidence layer)",
"# Method: PROPKA3 Wyman linkage on EXISTING bound complexes (no new folds). Per-His n_H(pH)=1/(1+10^(pH-pKa));",
"#   ddg_pH = 1.419*INT_{6.0}^{7.4} dn_H dpH over top-2 iptm poses/design. ddg<0 = binds weaker at low pH = RELEASE-competent.",
"# ddg_tot = all His (binder+target); ddg_bnd = BINDER His only = the DESIGNED mechanism (drops incidental target-His chemistry).",
"# switch_class (binder-His): INTERFACE-STRONG (pKa couples to binding, both methods agree) | INTERFACE-WEAK (borderline) |",
"#   TITRATABLE-ONLY (JustHISpKa in-window but binding-decoupled in this pose = intramolecular/surface His, binding-linkage can't score) | NOISY (pose-variable).",
"# DISCIPLINE: this is a CONSENSUS/EVIDENCE layer, NOT a re-ranker. PROPKA and JustHISpKa disagree > the pH window; the",
"#   portal-verified v25 ranking (switch=JustHISpKa-in-window pass -> xreact -> affinity) is PRESERVED. No swap/reorder on PROPKA alone.",
"# Pose source: 18/20 human Protenix (organizer-ruler engine family), 2 Boltz human. Generated 2026-11-01.",
]
with open(OUT,"w") as f:
    f.write("\n".join(HEAD)+"\n"+"\t".join(hdr)+"\n")
    for r in rows: f.write("\t".join(str(x) for x in r)+"\n")
# print summary
from collections import Counter
c=Counter(r[-1] for r in rows)
print(f"wrote {OUT}")
for r in rows: print(f"{r[0]:>2} {r[1]:<42} Mbe{r[3]} JHP{r[4]} ddg_bnd={r[8]:>7} frac{r[10]:>4}  {r[-1]}")
print("\nclasses:", dict(c))
