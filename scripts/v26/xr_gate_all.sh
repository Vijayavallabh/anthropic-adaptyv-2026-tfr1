#!/bin/bash
# Gate ALL pilot cross-reactivity folds (xr_fold + xr_fold2), both species, and flag native-His
# switch candidates (>=2 His) among the genuine-XR hits (H_iptm>=0.194 AND M_be>=2).
set -uo pipefail
REPO=/home/prachh/v/anthropic-adaptyv-2026-tfr1
SC=/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad
PYP=/home/prachh/v/sepiq-2026-challenge/.venv-protenix/bin/python
for base in xr_fold xr_fold2; do
  for sp in human mouse; do
    [ -d $SC/$base/$sp ] && $PYP $REPO/scripts/score_protenix_tfr1.py $SC/$base/$sp --species $sp --tsv $SC/${base}_${sp}.tsv >/dev/null 2>&1
  done
done
/home/prachh/v/anthropic-adaptyv-2026-tfr1/.venv/bin/python - <<'PY'
import csv, os, glob, re
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
def load(f):
    d={}
    if os.path.exists(f):
        for r in csv.DictReader(open(f),delimiter='\t'): d[r['design']]=r
    return d
H={}; M={}
for base in ["xr_fold","xr_fold2"]:
    H.update(load(f"{SC}/{base}_human.tsv")); M.update(load(f"{SC}/{base}_mouse.tsv"))
seqs={r['name']:r['sequence'] for r in csv.DictReader(open(f"{SC}/ms/mpnn/ms_binders.csv"))}
GATE_H=0.194
rows=[]
for n in sorted(set(H)|set(M)):
    if 'POS' in n or 'NEG' in n: continue
    h=H.get(n,{}); m=M.get(n,{})
    hi=float(h.get('iptm_max',0) or 0); hbe=int(h.get('best_epi',0) or 0)
    mi=float(m.get('iptm_max',0) or 0); mbe=int(m.get('best_epi',0) or 0)
    s=seqs.get(n,''); nhis=s.count('H')
    genuine = hi>=GATE_H and mbe>=2
    both_epi = hi>=GATE_H and hbe>=2 and mbe>=2
    rows.append((n,hi,hbe,mi,mbe,(mi/hi if hi else 0),nhis,genuine,both_epi))
rows.sort(key=lambda r:(-r[8],-r[7]))
print(f"{'design':30}{'H_iptm':>7}{'Hbe':>4}{'M_iptm':>7}{'Mbe':>4}{'MH':>5}{'nHis':>5}  flag")
gen=[]; both=[]
for n,hi,hbe,mi,mbe,mh,nhis,g,b in rows:
    flag = "BOTH-EPI+XR" if b else ("GENUINE-XR" if g else "")
    if nhis>=2 and b: flag+=" *native-switch?"
    if b: both.append(n)
    if g: gen.append(n)
    if g or nhis>=2:
        print(f"{n[:30]:30}{hi:>7.3f}{hbe:>4}{mi:>7.3f}{mbe:>4}{mh:>5.2f}{nhis:>5}  {flag}")
print(f"\nGENUINE-XR (H>=0.194 & M_be>=2): {len(gen)}")
print(f"BOTH-species on-epitope (H_be>=2 & M_be>=2 & H>=0.194): {len(both)}")
print("native-switch candidates (BOTH-EPI + >=2 His):")
for n,hi,hbe,mi,mbe,mh,nhis,g,b in rows:
    if b and nhis>=2: print(f"  {n} (nHis={nhis}, H{hi:.3f}/be{hbe}, M{mi:.3f}/be{mbe}, MH{mh:.2f})")
PY
