#!/usr/bin/env python3
"""Build v19 = v18 with ONE evidence-backed DESIGN upgrade from the switch-rescue (ambition-lift, 2026-10-27).

The frontier experiment WORKED (against the physics prediction): relocating genie_w2g3_53's buried-His switch
off its pKa-depressed positions produced genie_w2g3_53__A13HR44_A31HK8 -- validated on EVERY axis, same
pipeline as the pool:
  * mouse cross-reactivity (obj #2): robust XR 0.394 +/- 0.007 over n=3 independent seeds (min 0.385) --
    BEATS the entire v17/v18 pool (prior best 0.349) and the soft ~0.40 "ceiling".
  * pH switch (obj #1): JustHisPKa GENUINE with 2 His in-window CONFIRMED across 2 folds (seed7 6.67/6.39;
    seed1 6.70/6.02), swing 1.41-1.47, geometry sw_frac 1.00 over 6 folds.
  * binding (obj #3): 0.421 ; developability CLEAN (liability 0, 0-Cys) ; pose: mouse binding anchored on
    conserved residues 203+209 across both mouse folds (cross-species-robust) ; novelty 0.778 (novel, ==
    parent genie_w2g3_53_sw2b's 0.776 which was PORTAL-VERIFIED in v15; same fold, ~94% seq id to a cleared seq).
It REPLACES w4g1_286 (same fold cluster 2: XR 0.270, 1 in-window) -- a strict upgrade that keeps fold diversity.
By XR it is the new #1. It is the ONLY new (portal-unverified) sequence in the set; the other 19 are the
portal-verified v18 sequences. Order = XR-first (conf = xr_mean - 0.5*std) with the v18 SEVERE-expression
demotion (w4g3_380 out of the tested top-10). v18 (all 20 portal-verified) is the fully-verified fallback.
Usage: build_v19.py"""
import csv
R = "/home/prachh/v/anthropic-adaptyv-2026-tfr1"
OUT = f"{R}/submissions/tfr1_track2_v19.csv"
TESTED_TOP = 10
WINNER = "genie_w2g3_53__A13HR44_A31HK8"
DROP = "w4g1_286_mpnn1_sw2his"     # same fold cluster 2; winner replaces it

v18 = list(csv.DictReader(open(f"{R}/submissions/tfr1_track2_v18.csv")))
seq = {r['name']: r['sequence'].strip() for r in v18}
for r in csv.DictReader(open(f"{R}/runs/f37_rescue/top.csv")):
    if r['name'] == WINNER: seq[WINNER] = r['sequence'].strip()
assert WINNER in seq and seq[WINNER].isalpha(), "winner sequence not found/invalid"

M = {r['name']: r for r in csv.DictReader(open(f"{R}/runs/f35/sel/master.tsv"), delimiter='\t')}
dev = {r['name']: r for r in csv.DictReader(open(f"{R}/results/developability_tfr1_track2_v17.csv"))}
wdev = next((r for r in csv.DictReader(open(f"{R}/results/developability_top.csv")) if r['name'] == WINNER), {})
wr = next(r for r in csv.DictReader(open(f"{R}/runs/f37_rescue/robust_xr.tsv"), delimiter='\t') if r['name'] == WINNER)
wnov = next((r['singleseq_maxTM_pdb'] for r in csv.DictReader(open(f"{R}/runs/f37_rescue/novelty.csv")) if r['name'] == WINNER), '')
jhp = {}
for p in ["runs/bench/switch_justhispka.tsv", "runs/f35/sel/switch_justhispka.tsv", "runs/f37_rescue/switch_jhp.tsv"]:
    try:
        for r in csv.DictReader(open(f"{R}/{p}"), delimiter='\t'): jhp[r['name']] = r.get('n_inwindow', '')
    except FileNotFoundError: pass

def ff(x, d=0.0):
    try: return float(x)
    except (ValueError, TypeError): return d

names = [r['name'] for r in v18 if r['name'] != DROP] + [WINNER]
assert len(names) == 20 and DROP not in names

rows = []
for n in names:
    if n == WINNER:
        xm, xs, bd, tm = ff(wr['xr_mean']), ff(wr['xr_std']), ff(wr['bind_mean']), ff(wnov)
        risk, liab = (wdev.get('expr_risk') or 'CLEAN'), wdev.get('liability_score', '0')
        lineage, sett, sw, cluster, crown = 'Genie3-w2', 'F37-rescue', 'GENUINE', '2', '1.00'
    else:
        m = M.get(n, {})
        xm, xs, bd = ff(m.get('xr_mean')), ff(m.get('xr_std')), ff(m.get('bind'))
        tm = m.get('tm') if m.get('tm') not in (None, '-', '') else ''
        risk, liab = (dev.get(n, {}).get('expr_risk') or ''), dev.get(n, {}).get('liability_score', '')
        lineage, sett, sw, cluster, crown = m.get('lineage', ''), m.get('set', ''), m.get('sw', ''), m.get('cluster', ''), m.get('crown_rate', '')
    conf = xm - 0.5 * xs
    tmv = ff(tm, None) if tm not in ('', None) else None
    novpen = 0.04 if (sett == 'W4' and tmv is not None and 0.80 <= tmv < 0.90) else 0.0
    rows.append(dict(name=n, xm=xm, xs=xs, bd=bd, conf=conf, tm=tm, risk=risk, liab=liab, lineage=lineage,
                     set=sett, sw=sw, cluster=cluster, crown=crown, ninwin=jhp.get(n, ''), rankscore=conf - novpen))

rows.sort(key=lambda r: -r['rankscore'])
severe = [r for r in rows[:TESTED_TOP] if (r['risk'] or '').upper() == 'SEVERE']   # v18 developability demotion
rest = [r for r in rows if r not in severe]
rows = rest[:TESTED_TOP] + severe + rest[TESTED_TOP:]
assert len(rows) == 20

with open(OUT, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["name", "sequence", "molecule_class"])
    for r in rows:
        s = seq[r['name']]; assert s and s.isalpha(), f"bad seq {r['name']}"
        w.writerow([r['name'], s, "protein"])

ev = OUT.replace(".csv", "_evidence.csv")
with open(ev, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rank", "name", "set", "lineage", "tested_top10", "xr_mean", "xr_std", "bind", "crown_rate",
                "switch_verdict", "n_inwindow", "expr_risk", "liability", "novelty_tm", "cluster", "portal", "note"])
    for i, r in enumerate(rows, 1):
        portal = "CHECK (new seq; fold cleared v15)" if r['name'] == WINNER else "cleared(v15/v17)"
        note = "RESCUE WINNER: robust XR 0.394 (n=3) + 2-in-window switch (2 folds); replaces w4g1_286" if r['name'] == WINNER else \
               ("SEVERE expr risk -> out of tested top-10" if (r['risk'] or '').upper() == 'SEVERE' else "")
        w.writerow([i, r['name'], r['set'], r['lineage'], "Y" if i <= TESTED_TOP else "-", f"{r['xm']:.3f}",
                    f"{r['xs']:.3f}", f"{r['bd']:.3f}", r['crown'], r['sw'], r['ninwin'], r['risk'], r['liab'],
                    r['tm'], r['cluster'], portal, note])

print(f"=== v19: v18 + switch-rescue winner (replaces {DROP}) -> {OUT} ===")
hdr = f"{'#':>2} {'name':34}{'top10':>6}{'XRμ':>7}{'±':>6}{'bind':>6}{'inwin':>6}{'risk':>9}{'novTM':>7}{'portal':>8}"
print(hdr); print('-' * len(hdr))
for i, r in enumerate(rows, 1):
    tag = ' <= RESCUE WINNER' if r['name'] == WINNER else ''
    print(f"{i:2} {r['name']:34}{('Y' if i<=TESTED_TOP else '-'):>6}{r['xm']:7.3f}{r['xs']:6.3f}{r['bd']:6.3f}"
          f"{str(r['ninwin']):>6}{(r['risk'] or ''):>9}{str(r['tm']):>7}{('CHECK' if r['name']==WINNER else 'cleared'):>8}{tag}")
print(f"\nwinner novelty {wnov} (parent genie_w2g3_53_sw2b 0.776 was portal-verified in v15); dropped {DROP}")
print(f"distinct fold clusters: {len({r['cluster'] for r in rows if r['cluster']})}  (winner shares cluster 2, replacing w4g1_286)")
