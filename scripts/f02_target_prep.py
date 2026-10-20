#!/usr/bin/env python3
"""F02 target prep (written fresh; the TNF stage0 is stale EGFR code).

From the byte-verified 11QC (apo human TfR1 ectodomain homodimer, chain A == TfR1, 122-760, Gly142,
UniProt-numbered, no gaps) produce:
  1. data/targets/tfr1_human_ecto_A.pdb  -- clean single-subunit full-atom human TARGET (== af2ig target).
  2. data/targets/epitopes.json          -- the 3-arm hotspot sets (apical / conserved-apical subsite /
     conserved non-apical), each surface-/conservation-/exclusion-filtered and spatially compact.
  3. data/targets/mouse_mutations.json   -- human_resnum -> mouse_aa threading map (for f02_mouse_model.py).
Asserts: single-subunit window 122-760 (639 aa), UniProt 211 == Y, 142 == G.

Exclusions for the cross-reactive Arm-B patch: must be exposed on the MONOMER *and* not buried at the
disulfide-linked homodimer interface (assay target is a homodimer), conserved human==mouse, outside the
apical neighbourhood and outside the transferrin/helical site (619-670).
"""
import argparse, json, warnings
from pathlib import Path
import numpy as np
from Bio.PDB import MMCIFParser, PDBIO, Select, NeighborSearch
from Bio.PDB.Polypeptide import is_aa
from Bio.PDB.SASA import ShrakeRupley
from Bio.Data.IUPACData import protein_letters_3to1

warnings.filterwarnings("ignore")
THREE2ONE = {k.upper(): v for k, v in protein_letters_3to1.items()}
# Tien et al. 2013 theoretical max ASA (A^2) for relative SASA.
MAXASA = {'A':129,'R':274,'N':195,'D':193,'C':167,'E':223,'Q':225,'G':104,'H':224,'I':197,
          'L':201,'K':236,'M':224,'F':240,'P':159,'S':155,'T':172,'W':285,'Y':263,'V':174}
APICAL_FP = [202,203,204,208,209,210,211,212,348,371]
CONSERVED_APICAL = [202,203,209]
TF_SITE = (619,670)
APICAL_DOMAIN = (189,383)  # TfR1 apical domain II (protomer)


class ChainResRange(Select):
    def __init__(self, chain_id, lo, hi):
        self.c, self.lo, self.hi = chain_id, lo, hi
    def accept_chain(self, ch): return ch.id == self.c
    def accept_residue(self, r): return (not r.id[0].strip()) and is_aa(r, standard=True) and self.lo <= r.id[1] <= self.hi
    def accept_atom(self, a): return a.element != 'H'


def one(res): return THREE2ONE.get(res.resname.upper(), 'X')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cif", required=True, help="11QC.cif")
    ap.add_argument("--conservation", required=True, help="docs/conservation.json")
    ap.add_argument("--outdir", default="data/targets")
    a = ap.parse_args()
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    struct = MMCIFParser(QUIET=True).get_structure("11QC", a.cif)
    model = struct[0]
    chA = model['A']

    resA = [r for r in chA if is_aa(r, standard=True) and not r.id[0].strip() and 122 <= r.id[1] <= 760]
    nums = [r.id[1] for r in resA]
    seq = "".join(one(r) for r in resA)
    assert len(resA) == 639, f"expected 639 aa, got {len(resA)}"
    assert (min(nums), max(nums)) == (122, 760), f"range {min(nums)}-{max(nums)}"
    by_num = {r.id[1]: r for r in resA}
    assert one(by_num[211]) == 'Y', "UniProt 211 != Y"
    assert one(by_num[142]) == 'G', "142 != Gly"
    print(f"ASSERTS OK: chain A single-subunit 122-760, 639 aa, 211==Y, 142==G")

    # 1) clean single-subunit target (chain A, no hetero/glycan, no H)
    io = PDBIO(); io.set_structure(struct)
    tgt = out / "tfr1_human_ecto_A.pdb"
    io.save(str(tgt), ChainResRange('A', 122, 760))
    print(f"[wrote {tgt}]  (clean single-subunit human target == af2ig target)")

    # 2a) per-residue SASA on MONOMER (chain A alone) and on DIMER (A+B)
    def rsasa_map(chain_ids):
        sub = model.__class__(model.id)
        for cid in chain_ids:
            sub.add(model[cid].copy())
        ShrakeRupley().compute(sub, level="R")
        m = {}
        for cid in chain_ids:
            for r in sub[cid]:
                if is_aa(r, standard=True) and not r.id[0].strip():
                    aa = one(r)
                    m[r.id[1]] = r.sasa / MAXASA.get(aa, 200)
        return m
    rsasa_mono = rsasa_map(['A'])
    # dimer rSASA uses chain A residues within the A+B assembly
    sub2 = model.__class__(model.id)
    for cid in ['A', 'B']:
        sub2.add(model[cid].copy())
    ShrakeRupley().compute(sub2, level="R")
    rsasa_dim = {r.id[1]: r.sasa / MAXASA.get(one(r), 200)
                 for r in sub2['A'] if is_aa(r, standard=True) and not r.id[0].strip()}

    # 2b) dimer-interface residues on chain A = exposed on monomer but buried on dimer (delta rSASA)
    dimer_iface = sorted(rn for rn in rsasa_mono
                         if rsasa_mono[rn] - rsasa_dim.get(rn, rsasa_mono[rn]) > 0.15)
    print(f"dimer-interface residues on A (Δexposure>0.15): n={len(dimer_iface)} "
          f"e.g. {dimer_iface[:12]}{'...' if len(dimer_iface)>12 else ''}")

    # 2c) conservation map (human->mouse identity)
    cons = json.loads(Path(a.conservation).read_text())
    # per-residue conservation from the full human->mouse map (individually identical positions,
    # NOT only >=6-runs — the coarse run-based set undercounts conserved surface residues).
    fm = cons["human_to_mouse_122_760"]
    conserved = {int(k) for k, v in fm.items() if v["conserved"]}

    # 2d) Arm-B candidate residues: surface on dimer (rSASA>0.25), conserved, outside apical & Tf-site & dimer-iface
    def surface_dim(rn): return rsasa_dim.get(rn, 0) > 0.25
    armB_pool = sorted(rn for rn in range(122, 761)
                       if surface_dim(rn) and rn in conserved
                       and not (APICAL_DOMAIN[0] <= rn <= APICAL_DOMAIN[1])
                       and not (TF_SITE[0] - 5 <= rn <= TF_SITE[1] + 5)
                       and rn not in dimer_iface)
    # COMPACT contactable patch (not single-linkage, which chains across the whole surface): take the
    # densest 10 A CB-neighbourhood as the Arm-B epitope; seed a few disjoint alternates for F04 choice.
    cb = lambda r: (r['CB'] if 'CB' in r else r['CA']).coord
    cbc = {rn: cb(by_num[rn]) for rn in armB_pool if rn in by_num}
    pool = list(cbc)
    RAD = 10.0
    neigh = lambda s: sorted(rn for rn in pool if np.linalg.norm(cbc[rn] - cbc[s]) <= RAD)
    armB = neigh(max(pool, key=lambda s: len(neigh(s)))) if pool else []
    used, clusters = set(armB), ([armB] if armB else [])
    for s in sorted(pool, key=lambda s: -len(neigh(s))):
        p = neigh(s)
        if s not in used and len(set(p) & used) < max(1, len(p) // 2):
            clusters.append(p); used |= set(p)
        if len(clusters) >= 5:
            break
    print(f"Arm-B conserved-surface COMPACT patch (densest 10A nbhd): n={len(armB)} {armB}")
    print(f"   (alternate compact patches: {[c[:6] for c in clusters[1:5]]})")

    # Arm-C: conserved apical-SURFACE patch near the {202,203,209} core, excluding the divergent tip.
    div_tip = {204, 208, 210, 211, 212, 348, 371}
    cen = np.mean([cb(by_num[i]) for i in CONSERVED_APICAL], axis=0)
    armC_patch = sorted(rn for rn in range(APICAL_DOMAIN[0], APICAL_DOMAIN[1] + 1)
                        if rn in by_num and rn in conserved and rn not in div_tip
                        and rsasa_mono.get(rn, 0) > 0.20
                        and np.linalg.norm(cb(by_num[rn]) - cen) < 13.0)
    armC_hot = sorted(set(CONSERVED_APICAL) | set(armC_patch))
    print(f"Arm-C conserved-apical-surface patch (<13A of core, surface, conserved, excl divergent tip): {armC_hot}")

    # 3) epitopes.json
    epitopes = {
        "target_pdb": "tfr1_human_ecto_A.pdb", "target_chain": "A", "numbering": "UniProt P02786 == construct",
        "armA_apical_human": {"hotspots": APICAL_FP, "center": 211, "domain": "apical (II)",
                              "note": "functional epitope (VP1u/GP1/6WRV site); Obj1+Obj3, Obj2 sacrificed"},
        "armC_conserved_apical_subsite": {"hotspots": armC_hot, "core": CONSERVED_APICAL,
                              "note": "conserved apical-surface patch near the {202,203,209} core (surface+conserved, excludes the divergent tip 204/208/210/211/212/348/371); max-min core, mechanism B, joint h+m MPNN"},
        "armB_conserved_nonapical": {"hotspots": armB,
                              "note": "largest compact conserved + dimer-surface-exposed cluster, outside apical & Tf-site(619-670) & dimer interface; cross-reactive specialist",
                              "alt_clusters": [c for c in clusters[1:5]]},
        "exclude": {"transferrin_helical_site": list(TF_SITE), "dimer_interface": dimer_iface,
                    "novelty_nofly_structures": ["6WRV", "3DS18", "TB14", "VP1u", "GP1"]},
    }
    (out / "epitopes.json").write_text(json.dumps(epitopes, indent=2))
    print(f"[wrote {out/'epitopes.json'}]")

    # 4) mouse threading map: human_resnum -> mouse_aa, from the apical table + we also need the full map.
    # The stored conservation.json has apical_table + conserved_runs but not the full per-residue map;
    # emit what we can deterministically: conserved positions map to the SAME aa; divergent apical from table.
    # (f02_mouse_model.py recomputes the full align from the FASTAs for completeness.)
    mut = {}
    for row in cons["alignment"]["apical_table"]:
        if not row["conserved"] and row["mouse_aa"] not in ("-", None):
            mut[row["uniprot_human"]] = row["mouse_aa"]
    (out / "mouse_mutations_apical.json").write_text(json.dumps(mut, indent=2))
    print(f"[wrote {out/'mouse_mutations_apical.json'}] (apical divergent subset; full map in f02_mouse_model.py)")
    print("\nF02 target-prep (human) done. Next: f02_mouse_model.py for the threaded mouse model.")


if __name__ == "__main__":
    main()
