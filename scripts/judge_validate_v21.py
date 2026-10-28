#!/usr/bin/env python3
"""Ambition-lift #4 (2026-10-28, "5 days, best 20 on all metrics"): validate v21 against the
organizers' ACTUAL in-silico judge + resolve the devil's-advocate sort-key finding.

Consolidates, for each of the 20 (+ the strongest pool contender w4g1_286):
  - blind-Protenix judge (ESMFold2+Protenix regime), n=48 samples: human/mouse iptm_med + 95% bootstrap
    CI (calibrated POS_3DS18 0.210[0.199,0.244] vs NEG 0.105-0.109 -> binder-gate ~0.15), and MH ratio.
  - coherent WITHIN-FOLDER pocket ratio (the project's #2 metric per lesson-crossreact-is-ratio-not-
    absolute): per folder mouse/human ipSAE, Boltz & Chai, then |mean-1| and |worst-1| + folder-disagree.
  - switch swing + n_His_in_window (JustHisPKa), cluster, lineage.
Writes submissions/tfr1_track2_v21_judge_validation.tsv.

FINDING: v21 sorts the gate-pass group by xr_mean = ABSOLUTE mouse ipSAE (a confound, rho~0.87 with
bind), not the ratio. But the coherent ratio is NOISE-DOMINATED (folders disagree 0.3-1.0; mean/worst
aggregation flips order; 3/12 sign-flip) -> no RELIABLE reorder; reorder changes only noise-distinguished
top-10 membership and never the locked #1. w4g1_286 (best binder, H_med 0.301) is a folder-averaging
"balance" artifact + weak switch (swing 0.50) + structural twin of the locked flagship -> not a swap.
"""
import csv, glob, json, os
import numpy as np
np.random.seed(7)
REPO = "/home/prachh/v/anthropic-adaptyv-2026-tfr1"

def blind(design, species, root):
    ipts = []
    for js in glob.glob(f"{root}/{species}/{design}/seed_*/predictions/*summary_confidence_sample_*.json"):
        try: ipts.append(float(json.load(open(js))["iptm"]))
        except Exception: pass
    if not ipts: return None
    a = np.array(ipts)
    boots = [float(np.median(np.random.choice(a, len(a), replace=True))) for _ in range(2000)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return dict(med=float(np.median(a)), lo=float(lo), hi=float(hi), n=len(a))

def load_ipsae(p):
    return {r["name"]: float(r["ipsae"]) for r in csv.DictReader(open(p), delimiter="\t")} if os.path.exists(p) else {}

# pocket per-folder source run for each design (where its pocket-restrained Boltz/Chai ipSAE lives)
SRC = {k: "runs/f35/robust/s1" for k in
       ["w4g1_195_mpnn0_sw2his","w4g7_217_mpnn1_sw3his","w4g0_194_mpnn1_sw2his","w4g5_147_mpnn0_sw3his",
        "w4g5_137_mpnn1_sw3his","w4g1_286_mpnn1_sw2his","w4g2_174_mpnn1_sw3his","w4g3_380_mpnn0_sw2his"]}
SRC.update({k: "runs/f30/reval6" for k in
       ["genie_w2g6_144_sw3b","w3g5_231_mpnn1_sw3his","w3g7_240_mpnn1_sw3his","w3g6_146_mpnn0_sw2his",
        "w3g2_225_mpnn0_sw3his","genie_w2g5_111_sw2b","w3g5_70_mpnn1_sw3his","w3g0_290_mpnn1_sw2his",
        "w3g5_249_mpnn0__A13HK16_A42HK69","rfd4_g7_8_sw2b_A14_A41","rfd4_g5_14_sw2b_A34_A50"]})
SRC["genie_w2g3_53__A27HK8_A13HR44"] = "runs/f37_rescue/s1"
_cache = {}
def pocket_ratio(design):
    base = SRC.get(design)
    if not base: return None
    if base not in _cache:
        _cache[base] = [load_ipsae(f"{base}/{f}/ipsae.tsv") for f in ["boltz_h","boltz_m","chai_h","chai_m"]]
    bh, bm, ch, cm = _cache[base]
    def g(d):
        if design in d: return d[design]
        for k in d:
            if design.startswith("genie_w2g3_53") and k.startswith("genie_w2g3_53"): return d[k]
        return None
    h_b, m_b, h_c, m_c = g(bh), g(bm), g(ch), g(cm)
    if None in (h_b, m_b, h_c, m_c) or h_b == 0 or h_c == 0: return None
    rb, rc = m_b/h_b, m_c/h_c
    return dict(rb=rb, rc=rc, mean=(abs(rb-1)+abs(rc-1))/2, worst=max(abs(rb-1),abs(rc-1)),
                disagree=(rb-1)*(rc-1) < 0)

def switch():
    d = {}
    for p in [f"{REPO}/runs/f35/sel/switch_justhispka.tsv"]:
        if os.path.exists(p):
            for r in csv.reader(open(p), delimiter="\t"):
                if len(r) >= 7: d[r[0]] = dict(nwin=r[1], swing=r[4], verdict=r[6])
    return d

def main():
    sub = [l.split(",")[0] for l in open(f"{REPO}/submissions/tfr1_track2_v21.csv").read().replace("\r","").splitlines()[1:] if l.strip()]
    ev = {r["name"]: r for r in csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v19_evidence.csv"))}
    f35 = {r["name"]: r for r in csv.DictReader(open(f"{REPO}/runs/f35/sel/master.tsv"), delimiter="\t")}
    SW = switch()
    rows = []
    for nm in sub + ["w4g1_286_mpnn1_sw2his"]:
        root = f"{REPO}/runs/prot/pool_judge" if nm == "w4g1_286_mpnn1_sw2his" else f"{REPO}/runs/prot/v20_judge"
        h, m = blind(nm, "human", root), blind(nm, "mouse", root)
        pr = pocket_ratio(nm)
        sw = SW.get(nm, {})
        rows.append(dict(name=nm, h=h, m=m, pr=pr, sw=sw,
                         xr=ev.get(nm,{}).get("xr_mean","-"), clus=f35.get(nm,{}).get("cluster","-"),
                         lin=ev.get(nm,{}).get("lineage", f35.get(nm,{}).get("lineage","-"))))
    out = f"{REPO}/submissions/tfr1_track2_v21_judge_validation.tsv"
    with open(out, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["# organizers'-judge + coherent-ratio validation of v21 (ambition-lift #4, 2026-10-28)"])
        w.writerow(["# blind calib POS_3DS18 Hmed 0.210[0.199,0.244] vs NEG 0.105-0.109; binder-gate ~0.15. pose/sc-DockQ proxy DISCARDED (POS 16.5A between NEG 15.2/19.3)."])
        w.writerow(["v21rank","name","blindH_med","blindH_CI","blindM_med","blindMH_ratio",
                    "pocket_Boltz_r","pocket_Chai_r","pocket|mean-1|","pocket_folders_disagree",
                    "xr_mean(abs_mouse,v21_sortkey)","switch_swing","switch_nwin","cluster","lineage"])
        for i, r in enumerate(rows, 1):
            rank = i if r["name"] != "w4g1_286_mpnn1_sw2his" else "POOL"
            h, m, pr, sw = r["h"], r["m"], r["pr"], r["sw"]
            w.writerow([rank, r["name"],
                        f"{h['med']:.3f}" if h else "-", f"[{h['lo']:.3f},{h['hi']:.3f}]" if h else "-",
                        f"{m['med']:.3f}" if m else "-", f"{m['med']/h['med']:.2f}" if (h and m and h['med']) else "-",
                        f"{pr['rb']:.2f}" if pr else "-", f"{pr['rc']:.2f}" if pr else "-",
                        f"{pr['mean']:.2f}" if pr else "-", ("YES" if pr and pr["disagree"] else "") ,
                        r["xr"], sw.get("swing","-"), sw.get("nwin","-"), r["clus"], r["lin"]])
    print("wrote", out)
    os.system(f"column -t -s'\t' {out} | head -30")

if __name__ == "__main__":
    main()
