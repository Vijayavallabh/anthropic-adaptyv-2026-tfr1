#!/usr/bin/env python3
# Uniform binding audit of all 20 v26 members vs IN-RUN POS/NEG anchors (same calibrated fold).
# Primary gate = HUMAN on-epitope (the challenge requires binding human apical). Mouse = cross-react axis.
# Classify: REAL (iptm>=gate AND wepi>scramble-floor AND on_epi>0) / COLLAPSE (iptm high but wepi<=floor) / WEAK (iptm<gate).
#
# !!! WARNING — the HUMAN wepi<=scramble-floor COLLAPSE gate below (line ~lookup `hw <= Hn_w`) is MISCALIBRATED and its
#     output is SUPERSEDED. In-run calibration shows the POSITIVE CONTROL fails this exact gate (POS_3DS18 human wepi 0.100
#     < NEG scramble floor 0.136 — the human apical epitope-overlap metric is NOISE). So this script's "COLLAPSE-OFFEPI"
#     labels are FALSE POSITIVES on human (it flags ~12/20 incl. POS-like members). This first-pass table was DISCARDED.
#     Authoritative human-binding evidence = (a) blind iptm floor >=0.194 [not-scramble], (b) adversarial workflow audit_wf.js
#     [forbids any epitope gate the positive control fails], (c) pocket-restrained Boltz human-apical docking (POS-calibrated).
#     Phantom-collapse is adjudicated ONLY on the MOUSE channel (where POS wepi > NEG). Do NOT act on this file's human labels.
import csv, sys
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
GATE=0.194  # project-calibrated H_iptm gate (POS vs NEG on cuequivariance ruler)
def load(f):
    d={}
    for r in csv.DictReader(open(f),delimiter='\t'): d[r['design']]=r
    return d
H=load(f"{SC}/audit_human.tsv"); M=load(f"{SC}/audit_mouse.tsv")
def g(d,k):
    try: return float(d.get(k,0) or 0)
    except: return 0.0
# in-run anchors
def anchor(D):
    pos=D["POS_3DS18"]; n1=D["NEG_scramble1"]; n2=D["NEG_scramble2"]
    return (g(pos,'iptm_max'),g(pos,'wepi_frac'),g(pos,'on_epi_rate'),
            max(g(n1,'iptm_max'),g(n2,'iptm_max')), max(g(n1,'wepi_frac'),g(n2,'wepi_frac')))
Hp_i,Hp_w,Hp_o,Hn_i,Hn_w = anchor(H)
Mp_i,Mp_w,Mp_o,Mn_i,Mn_w = anchor(M)
print(f"# IN-RUN ANCHORS (n40, this calibrated fold)")
print(f"#  HUMAN: POS_3DS18 iptm {Hp_i:.3f} wepi {Hp_w:.3f} on_epi {Hp_o:.2f} | NEG floor iptm {Hn_i:.3f} wepi {Hn_w:.3f} | GATE iptm>={GATE}")
print(f"#  MOUSE: POS_3DS18 iptm {Mp_i:.3f} wepi {Mp_w:.3f} on_epi {Mp_o:.2f} | NEG floor iptm {Mn_i:.3f} wepi {Mn_w:.3f}")
print()
# v26 rank order
names=[r['name'].strip() for r in csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v26.csv"))]
hdr=f"{'rk':>2} {'design':44} {'H_ipt':>6}{'H_wepi':>7}{'H_oe':>5}{'H_be':>5}  {'M_ipt':>6}{'M_wepi':>7}{'M_oe':>5}{'M_be':>5}  {'HUMAN-CLASS':<14}{'XR'}"
print(hdr); print("-"*len(hdr))
nfail=0; summary=[]
for i,n in enumerate(names,1):
    h=H.get(n,{}); m=M.get(n,{})
    hi,hw,ho,hb = g(h,'iptm_max'),g(h,'wepi_frac'),g(h,'on_epi_rate'),int(g(h,'best_epi'))
    mi,mw,mo,mb = g(m,'iptm_max'),g(m,'wepi_frac'),g(m,'on_epi_rate'),int(g(m,'best_epi'))
    # HUMAN classification (primary)
    if hi < GATE:
        cls="WEAK-iptm"
    elif hw <= Hn_w:
        cls="COLLAPSE-OFFEPI";
    elif ho<=0:
        cls="OFFEPI(on_epi0)"
    else:
        cls="REAL-ONEPI"
    fail = cls not in ("REAL-ONEPI",)
    if fail: nfail+=1
    # XR (mouse cross-react): on-epitope on mouse too?
    xr = "both-epi" if (mi>=GATE and mw>Mn_w and mo>0) else ("m-weak" if mi<GATE else ("m-offepi" if mw<=Mn_w else "m-mid"))
    print(f"{i:>2} {n:44} {hi:6.3f}{hw:7.3f}{ho:5.2f}{hb:5d}  {mi:6.3f}{mw:7.3f}{mo:5.2f}{mb:5d}  {cls:<14}{xr}")
    summary.append((i,n,cls,xr,hi,hw,mi,mw))
print()
print(f"# HUMAN binding gate: {20-nfail}/20 REAL-ONEPI, {nfail}/20 FLAGGED")
flagged=[s for s in summary if s[2]!="REAL-ONEPI"]
if flagged:
    print("# FLAGGED (human):")
    for i,n,cls,xr,hi,hw,mi,mw in flagged: print(f"#   rank{i} {n}: {cls} (H_iptm {hi:.3f} H_wepi {hw:.3f} vs NEG floor {Hn_w:.3f})")
# save machine-readable
with open(f"{SC}/audit_classified.tsv","w") as f:
    f.write("rank\tdesign\thuman_class\txr\tH_iptm\tH_wepi\tM_iptm\tM_wepi\n")
    for i,n,cls,xr,hi,hw,mi,mw in summary: f.write(f"{i}\t{n}\t{cls}\t{xr}\t{hi:.3f}\t{hw:.3f}\t{mi:.3f}\t{mw:.3f}\n")
print(f"\n# wrote {SC}/audit_classified.tsv")
