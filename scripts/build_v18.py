#!/usr/bin/env python3
"""Build v18 = v17's cross-reactivity-first ranking with ONE evidence-backed change: demote any member of the
tested top-10 that is flagged SEVERE expression risk to just below the cut, pulling the next clean, ~equal-XR
design in. (ambition-lift, 2026-10-27; REVISED after a cold devil's-advocate review + the SOTA scout.)

WHY THIS IS MINIMAL (an earlier draft over-reached; this is the honest, disciplined version):
An initial v18 reordered the gated genuine-switch crowns by a JustHisPKa n_inwindow "switch tier." A cold
devil's-advocate (P(mistake)=70%), the independent 18-agent SOTA scout, AND repo doctrine all converged:
  * Within the genuine-crown set the switch is NOT finely rankable -- His-pKa predictor error is ~2-3 pH units,
    far wider than the 1.4-unit window, so n_inwindow is boundary-brittle. Example: w4g7_217's His are
    7.56/5.70/3.30; 7.56 is only 0.16 above the 7.4 edge and 5.70 only 0.30 below the 6.0 edge -- both inside
    the stated 0.4 MUE, so its n_inwindow=0 could be 2. The promoted designs (rfd4_g5_14 7.06/7.33/6.83;
    w4g5_147 has one His at 8.54) are equally boundary-fragile.
  * So re-ranking on the switch tier TRADES the one reliable axis (cross-reactivity, objective #2) for noise
    inside its own error bar = churn (repo lesson: "a swap trading a higher axis for a lower = churn").
  * Correction: the "49%/39%" figure is POSITIONAL front-loading (how much weight rank-1 vs the top-10 carry
    in selection), NOT an objective-#1 weight. Objective #1 (the pH switch) is a GATE -- all 20 are GENUINE
    (JustHisPKa) -- so the correct order WITHIN the gate is by objective #2 (XR), which is exactly v17's order.

The ONE real, non-noise signal the completed every-metric matrix added is developability: w4g3_380 (v17 #9,
inside the tested top-10) is SEVERE expression risk (net charge -15 "charge-blob" + a hydrophobic run) -- the
only SEVERE design in the set. Keeping it in the likely-tested top-10 risks a non-expressing null result. v18
demotes it just below the cut and promotes the clean, ~equal-XR w4g5_147 (v17 #11, XR 0.225 vs 0.229) in.
Every other design keeps its v17 rank. (The DA itself endorsed exactly this single swap.)

PURE REORDER of v17's 20 portal-verified sequences -> inherits v17's 20/20 portal verification, zero new risk.
Usage: build_v18.py"""
import csv
R = "/home/prachh/v/anthropic-adaptyv-2026-tfr1"
OUT = f"{R}/submissions/tfr1_track2_v18.csv"
TESTED_TOP = 10

v17 = list(csv.DictReader(open(f"{R}/submissions/tfr1_track2_v17.csv")))
seq = {r['name']: r['sequence'].strip() for r in v17}
order = [r['name'] for r in v17]                       # v17 row order == v17 ranking (XR-first)
dev = {r['name']: r for r in csv.DictReader(open(f"{R}/results/developability_tfr1_track2_v17.csv"))}

def severe(n): return (dev.get(n, {}).get('expr_risk') or '').upper() == 'SEVERE'

# demote SEVERE-expr-risk designs that sit in the tested top-10 to just below the cut; keep all else in order
severe_in_top = [n for n in order[:TESTED_TOP] if severe(n)]
rest = [n for n in order if n not in severe_in_top]
v18order = rest[:TESTED_TOP] + severe_in_top + rest[TESTED_TOP:]
assert len(v18order) == 20 and set(v18order) == set(order), "v18 must be a REORDER of v17's exact 20"

with open(OUT, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["name", "sequence", "molecule_class"])
    for n in v18order:
        s = seq[n]; assert s and s.isalpha(), f"bad seq {n}"
        w.writerow([n, s, "protein"])

# evidence (complete matrix, in v18 order) + report
v17rank = {n: i + 1 for i, n in enumerate(order)}
master = {r['name']: r for r in csv.DictReader(open(f"{R}/runs/f35/sel/master.tsv"), delimiter='\t')}
jhp = {}
for p in ["runs/bench/switch_justhispka.tsv", "runs/f35/sel/switch_justhispka.tsv"]:
    try:
        for r in csv.DictReader(open(f"{R}/{p}"), delimiter='\t'): jhp[r['name']] = r.get('n_inwindow', '')
    except FileNotFoundError: pass

ev = OUT.replace(".csv", "_evidence.csv")
with open(ev, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rank", "name", "v17_rank", "delta", "tested_top10", "xr_mean", "xr_std", "bind",
                "crown_rate", "switch_verdict", "n_inwindow", "expr_risk", "liability", "novelty_tm", "cluster", "note"])
    for i, n in enumerate(v18order, 1):
        m = master.get(n, {}); d = dev.get(n, {})
        note = ("DEMOTED: SEVERE expression risk out of tested top-10" if n in severe_in_top
                else "promoted into tested top-10 (clean, ~equal XR)" if (v17rank[n] > TESTED_TOP >= i) else "")
        w.writerow([i, n, v17rank[n], f"{v17rank[n]-i:+d}", "Y" if i <= TESTED_TOP else "-", m.get('xr_mean', ''),
                    m.get('xr_std', ''), m.get('bind', ''), m.get('crown_rate', ''), m.get('sw', ''),
                    jhp.get(n, ''), d.get('expr_risk', ''), d.get('liability_score', ''), m.get('tm', ''),
                    m.get('cluster', ''), note])

print(f"=== v18 (v17 XR-first order; ONE developability demotion) -> {OUT} ===")
print(f"SEVERE-expr-risk demoted out of tested top-{TESTED_TOP}: {severe_in_top or ['none']}")
hdr = f"{'#':>2} {'name':34}{'v17':>4}{'Δ':>4}{'top10':>6}{'XRμ':>7}{'bind':>6}{'inwin':>6}{'risk':>9}"
print(hdr); print('-' * len(hdr))
for i, n in enumerate(v18order, 1):
    m = master.get(n, {}); d = dev.get(n, {}); delta = v17rank[n] - i
    print(f"{i:2} {n:34}{v17rank[n]:>4}{(f'{delta:+d}' if delta else '0'):>4}{('Y' if i<=TESTED_TOP else '-'):>6}"
          f"{float(m.get('xr_mean') or 0):7.3f}{float(m.get('bind') or 0):6.3f}{str(jhp.get(n,'')):>6}{(d.get('expr_risk') or ''):>9}")
