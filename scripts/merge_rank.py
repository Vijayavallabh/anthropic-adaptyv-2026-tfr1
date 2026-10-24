#!/usr/bin/env python3
"""Merge f17 re-ranking signals into one table + lexicographic objective rank.
Objective priority: #1 pH-switch (valid Baker >=2, robust = holds across folds) > #2 mouse x-react
(ipSAE_min) > #3 human affinity (ipSAE_min). ipSAE_min = worst-case over available folders per species.
Reads whatever exists: boltz_h/ipsae.tsv, boltz_m/ipsae.tsv, chai_h/ipsae.tsv, chai_m/ipsae.tsv,
switch_h.tsv, switch_m.tsv, switch_ch.tsv, switch_cm.tsv. Robust to missing (Chai) files.
Usage: merge_rank.py <f17_dir>
"""
import sys, os, csv
R = sys.argv[1] if len(sys.argv) > 1 else "runs/f17"

def load_ipsae(p):
    d = {}
    if os.path.exists(p):
        for row in csv.DictReader(open(p), delimiter="\t"):
            try: d[row["name"]] = float(row["ipsae"])
            except Exception: pass
    return d

def load_switch(p):
    d = {}
    if os.path.exists(p):
        for row in csv.DictReader(open(p), delimiter="\t"):
            try: d[row["design"]] = int(row["total"])
            except Exception: pass
    return d

bh = load_ipsae(f"{R}/boltz_h/ipsae.tsv"); bm = load_ipsae(f"{R}/boltz_m/ipsae.tsv")
ch = load_ipsae(f"{R}/chai_h/ipsae.tsv"); cm = load_ipsae(f"{R}/chai_m/ipsae.tsv")
sbh = load_switch(f"{R}/switch_h.tsv"); sbm = load_switch(f"{R}/switch_m.tsv")
sch = load_switch(f"{R}/switch_ch.tsv"); scm = load_switch(f"{R}/switch_cm.tsv")

names = [r[0] for r in csv.reader(open(f"{R}/score_in.csv"))][1:]
rows = []
for n in names:
    hvals = [v for v in (bh.get(n), ch.get(n)) if v is not None]
    mvals = [v for v in (bm.get(n), cm.get(n)) if v is not None]
    h_min = min(hvals) if hvals else float("nan")
    m_min = min(mvals) if mvals else float("nan")
    sw = {"bh": sbh.get(n), "bm": sbm.get(n), "ch": sch.get(n), "cm": scm.get(n)}
    sw_folds = [v for v in sw.values() if v is not None]
    n_valid = sum(1 for v in sw_folds if v >= 2)          # folds where switch holds (>=2)
    n_folds = len(sw_folds)
    xreact = m_min >= 0.15 if m_min == m_min else False     # real mouse interface
    aff_ok = h_min >= 0.40 if h_min == h_min else False     # real human binder (POS~0.55, NEG~0.0)
    rows.append(dict(name=n, h=h_min, m=m_min, bh=bh.get(n), ch=ch.get(n), bm=bm.get(n), cm=cm.get(n),
                     nvalid=n_valid, nfolds=n_folds, sw=sw, xreact=xreact, aff_ok=aff_ok))

# lexicographic sort key: switch-robustness class, then x-react, then human affinity
def key(r):
    sw_class = 2 if r["nvalid"] >= 2 else (1 if r["nvalid"] == 1 else 0)   # robust / single-fold / none
    xr = 1 if r["xreact"] else 0
    m = r["m"] if (r["xreact"] and r["m"] == r["m"]) else 0.0              # mouse only counts if real x-react
    h = r["h"] if r["h"] == r["h"] else -1
    return (sw_class, xr, m, h)
rows.sort(key=key, reverse=True)

print(f"folds loaded: boltz_h={len(bh)} boltz_m={len(bm)} chai_h={len(ch)} chai_m={len(cm)}")
print(f"{'rk':>2} {'name':22} {'sw(bh/bm/ch/cm)':16} {'val':>3} {'H_min':>6} {'M_min':>6} {'xr':>2} {'aff':>3}  tags")
for i, r in enumerate(rows, 1):
    sw = r["sw"]
    sws = "/".join(str(sw[k]) if sw[k] is not None else "-" for k in ("bh","bm","ch","cm"))
    tags = []
    if r["nvalid"] >= 2: tags.append("SWITCH")
    elif r["nvalid"] == 1: tags.append("switch?")
    if r["xreact"]: tags.append("XREACT")
    if r["aff_ok"]: tags.append("binds")
    if r["nvalid"] >= 2 and r["xreact"]: tags = ["*CROWN*"] + tags
    h = r["h"]; m = r["m"]
    print(f"{i:>2} {r['name']:22} {sws:16} {r['nvalid']:>3} {h:6.3f} {m:6.3f} {'Y' if r['xreact'] else '.':>2} {'Y' if r['aff_ok'] else '.':>3}  {' '.join(tags)}")
