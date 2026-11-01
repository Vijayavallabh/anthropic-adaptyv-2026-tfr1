#!/usr/bin/env python3
# Two-state pH-release switch score via PROPKA Wyman linkage (adapted from the TNF Challenge-2
# ph_release_score.py — same release physics TfR1 wants: bind pH7.4, RELEASE pH6.0).
# Splits binder(A):target(B) complex, runs propka3 on complex/binder/target, computes per-His
# n_H(pH)=1/(1+10^(pH-pKa)); dn_H = n_H(complex)-n_H(free); ddg_pH = 1.419*int_{6.0}^{7.4} dn_H dpH.
# ddg_pH < 0  => binds WEAKER at low pH = RELEASE-competent (genuine TfR1 switch); |ddg_pH| ~ strength.
# Usage: ph_release_tfr1.py <complex.pdb> [bch=A] [tch=B] [lo=6.0] [hi=7.4]   (prints RESULT\t line)
import sys, os, subprocess, tempfile, numpy as np
PROPKA = "/home/prachh/v/anthropic-adaptyv-2026-tfr1/.venv/bin/propka3"
RT_LN10 = 1.419
def run_propka(pdb, wd):
    b = os.path.basename(pdb)
    r = subprocess.run([PROPKA, b], cwd=wd, capture_output=True, timeout=600)
    pka = os.path.join(wd, b[:-4] + ".pka")
    if not os.path.exists(pka):
        sys.stderr.write(f"PROPKA-FAIL {b}: rc={r.returncode} {r.stderr.decode()[-200:]}\n")
        return None
    return pka
def parse_his(pkafile):
    out = {}
    if not pkafile or not os.path.exists(pkafile): return out
    inblock = False
    for ln in open(pkafile):
        if ln.startswith("SUMMARY OF THIS PREDICTION"): inblock = True; continue
        if inblock:
            p = ln.split()
            if len(p) >= 4 and p[0] == "HIS":
                try: out[(p[2], int(p[1]))] = float(p[3])
                except: pass
            if ln.strip().startswith("-") or ln.strip() == "":
                if out: break
    return out
def split_write(pdb, wd, bch, tch):
    A = []; B = []
    for ln in open(pdb):
        if ln[:4] == "ATOM":
            c = ln[21]
            if c == bch: A.append(ln)
            elif c == tch: B.append(ln)
    open(os.path.join(wd, "cx.pdb"), 'w').write("".join(A + B) + "END\n")
    open(os.path.join(wd, "bd.pdb"), 'w').write("".join(A) + "END\n")
    open(os.path.join(wd, "tg.pdb"), 'w').write("".join(B) + "END\n")
    return len(A) > 0 and len(B) > 0
def nH(pka, pH): return 1.0 / (1.0 + 10 ** (pH - pka))
def score(pdb, bch='A', tch='B', lo=6.0, hi=7.4):
    lo = float(lo); hi = float(hi)
    with tempfile.TemporaryDirectory() as wd:
        if not split_write(pdb, wd, bch, tch): return None
        hcx = parse_his(run_propka("cx.pdb", wd))
        hbd = parse_his(run_propka("bd.pdb", wd))
        htg = parse_his(run_propka("tg.pdb", wd))
        free = {**hbd, **htg}
        pHs = np.linspace(lo, hi, 15)
        tot = 0.0; dets = []; n_release_his = 0
        for key in sorted(hcx):
            ch, rn = key; pc = hcx[key]; pf = free.get(key)
            if pf is None: continue
            dn = np.array([nH(pc, p) - nH(pf, p) for p in pHs])
            contrib = RT_LN10 * np.trapezoid(dn, pHs)
            tot += contrib
            if contrib < -0.02: n_release_his += 1   # this His suppressed in complex => releases
            side = "bnd" if ch == bch else "tgt"
            dets.append(f"{ch}{rn}({side}):dpKa{pc-pf:+.2f},ddg{contrib:+.3f}")
        return dict(ddg=tot, n_his=len(dets), n_release=n_release_his, dets=";".join(dets))
if __name__ == "__main__":
    r = score(sys.argv[1], *(sys.argv[2:6]))
    if r is None: print("RESULT\tNA\tNA\tNA\t-"); sys.exit(1)
    print(f"RESULT\t{r['ddg']:+.3f}\t{r['n_his']}\t{r['n_release']}\t{r['dets']}")
