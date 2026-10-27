#!/usr/bin/env python3
"""Thermodynamic switch-genuineness gate (objective #1), the piece v15 never had.
switch_frac proves a His SITS next to a cation (geometry); this proves the His pKa FIRES in the 6.0-7.4
window (thermodynamics). PROPKA3 His pKa on each crown's bound complex + free binder:
  - in-window: a switch-His needs 6.0 < pKa < 7.4 (neutral @7.4, protonated @6.0). pKa<6.0 = buried-
    suppressed DEAD switch (never protonates in-window); pKa>7.4 = breaks ON binding.
  - Wyman release linkage: dn_H(pH)=nH(complex)-nH(free); ddg_pH=RT*ln10*int_{6.0}^{7.4} sum dn_H dpH;
    ddg_pH<0 => weaker at low pH = RELEASE.
PROPKA is a WEAK His predictor -> use for sign/in-window as a DEMOTE filter, not a fine magnitude ranker.
Usage: propka_switch.py <name_TAB_complex.pdb .tsv> [out.tsv]. Drafted by assistant (ambition-lift, 2026-10-27)."""
import csv, subprocess, re, sys
from pathlib import Path
REPO=Path("/home/prachh/v/anthropic-adaptyv-2026-tfr1")
PROPKA=REPO/"tools/pka-venv/bin/propka3"
TMP=REPO/"runs/tmp/propka"; TMP.mkdir(parents=True,exist_ok=True)
RT_LN10=1.419; LO,HI=6.0,7.4
def nH(pka,pH): return 1.0/(1.0+10**(pH-pka))
def extract_chainA(pdb,out):
    with open(out,"w") as f:
        for l in open(pdb):
            if l.startswith("ATOM") and l[21]=="A": f.write(l)
        f.write("END\n")
def propka_his(pdb):
    stem=Path(pdb).stem
    subprocess.run([str(PROPKA),str(Path(pdb).resolve())],cwd=str(TMP),capture_output=True,text=True)
    pka=TMP/f"{stem}.pka"
    if not pka.exists(): return None
    out={}; insumm=False
    for l in open(pka):
        if "SUMMARY OF THIS PREDICTION" in l: insumm=True; continue
        if insumm:
            if l.strip().startswith("-") or l.strip().startswith("Free energy"): break
            m=re.match(r'\s*HIS\s+(\d+)\s+(\w)\s+(-?[\d.]+)',l)
            if m and m.group(2)=="A": out[int(m.group(1))]=float(m.group(3))
    return out
def integ(pkas_c,pkas_f):
    # sum over His of int_{LO}^{HI} (nH_complex - nH_free) dpH, trapezoid on 41 pts
    pHs=[LO+(HI-LO)*i/40 for i in range(41)]; tot=0.0
    for h,pc in pkas_c.items():
        pf=pkas_f.get(h,pc)
        ys=[nH(pc,p)-nH(pf,p) for p in pHs]
        area=sum((ys[i]+ys[i+1])/2*(pHs[i+1]-pHs[i]) for i in range(40))
        tot+=area
    return RT_LN10*tot
def main():
    tsv=sys.argv[1]; outp=sys.argv[2] if len(sys.argv)>2 else str(REPO/"runs/bench/switch_pka.tsv")
    rows=[l.split('\t') for l in open(tsv) if l.strip() and not l.startswith('#')]
    res=[]
    for name,pdb in rows:
        pdb=pdb.strip()
        pc=propka_his(pdb)
        bind=TMP/f"{name}_bind.pdb"; extract_chainA(pdb,bind)
        pf=propka_his(str(bind)) or {}
        if pc is None: res.append((name,None)); continue
        his=sorted(pc.items())
        inwin=[h for h,p in his if LO<=p<=HI]
        below=[h for h,p in his if p<LO]
        ddg=integ(pc,pf)
        verdict = ("GENUINE" if inwin and ddg<0 else
                   "DEAD(all<6)" if his and len(below)==len(his) else
                   "weak" if ddg<0 else "WRONG-SIGN")
        res.append((name,dict(nHis=len(his),pkas=[round(p,2) for _,p in his],
                              n_inwin=len(inwin),n_below6=len(below),ddg=round(ddg,3),verdict=verdict)))
    with open(outp,"w") as fo:
        fo.write("name\tnHis\tpKas_complex\tn_inwindow\tn_below6\tddg_pH\tverdict\n")
        for name,d in res:
            if d is None: fo.write(f"{name}\t\t\t\t\tNA\tno-pka\n"); continue
            fo.write(f"{name}\t{d['nHis']}\t{','.join(map(str,d['pkas']))}\t{d['n_inwin']}\t{d['n_below6']}\t{d['ddg']}\t{d['verdict']}\n")
    print(f"WROTE {outp}\n")
    print(f"{'name':34} {'nHis':>4} {'in6-7.4':>7} {'<6':>3} {'ddg_pH':>7} {'verdict':>12}  pKas")
    print("-"*96)
    for name,d in res:
        if d is None: print(f"{name[:34]:34}  no-pka"); continue
        print(f"{name[:34]:34} {d['nHis']:>4} {d['n_inwin']:>7} {d['n_below6']:>3} {d['ddg']:>7.3f} {d['verdict']:>12}  {d['pkas']}")
if __name__=="__main__": main()
