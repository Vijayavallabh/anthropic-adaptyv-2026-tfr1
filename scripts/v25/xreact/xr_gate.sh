#!/bin/bash
# STAGED: gate the pilot cross-reactivity folds. Reuses the canonical scorer score_protenix_tfr1.py.
# Genuine cross-reactive = H_iptm_max >= 0.194 (v25 ruler gate) AND M_be >= 2 (mouse on-epitope, best pose).
# POS_3DS18 / NEG_scramble rows are printed for fail-loud calibration (gate must separate them).
set -uo pipefail
REPO=/home/prachh/v/anthropic-adaptyv-2026-tfr1
SC=/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad
PYP=/home/prachh/v/sepiq-2026-challenge/.venv-protenix/bin/python
$PYP $REPO/scripts/score_protenix_tfr1.py $SC/xr_fold/human --species human --tsv $SC/xr_human.tsv | tail -n +1 >/dev/null
$PYP $REPO/scripts/score_protenix_tfr1.py $SC/xr_fold/mouse --species mouse --tsv $SC/xr_mouse.tsv | tail -n +1 >/dev/null
/home/prachh/v/anthropic-adaptyv-2026-tfr1/.venv/bin/python - <<'PY'
import csv, os
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
def load(f):
    d={}
    if os.path.exists(f):
        for r in csv.DictReader(open(f),delimiter='\t'): d[r['design']]=r
    return d
H=load(f"{SC}/xr_human.tsv"); M=load(f"{SC}/xr_mouse.tsv")
GATE_H=0.194
names=sorted(set(H)|set(M))
print(f"{'design':30}{'H_iptm':>8}{'H_be':>5}{'M_iptm':>8}{'M_be':>5}{'MH':>6}  verdict")
print("-"*72)
gen=[]
for n in names:
    h=H.get(n,{}); m=M.get(n,{})
    hi=float(h.get('iptm_max',0) or 0); hbe=int(h.get('best_epi',0) or 0)
    mi=float(m.get('iptm_max',0) or 0); mbe=int(m.get('best_epi',0) or 0)
    mh=(mi/hi) if hi>0 else 0
    ctrl = ('POS' in n or 'NEG' in n)
    if ctrl: v="[control]"
    elif hi>=GATE_H and mbe>=2: v="GENUINE-XR"; gen.append(n)
    elif hi>=GATE_H and mbe==1: v="marginal"
    elif hi>=GATE_H: v="human-only"
    else: v="sub-gate"
    print(f"{n[:30]:30}{hi:>8.3f}{hbe:>5}{mi:>8.3f}{mbe:>5}{mh:>6.2f}  {v}")
print(f"\nGENUINE cross-reactive (H_iptm>={GATE_H} AND M_be>=2): {len(gen)}")
for n in gen: print("  "+n)
print("\nCALIBRATION CHECK: POS_3DS18 should clear H-gate; NEG_scramble should NOT. If not, gate is invalid.")
PY
