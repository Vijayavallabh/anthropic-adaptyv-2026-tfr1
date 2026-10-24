#!/usr/bin/env python3
"""Read the epitope from a BLIND co-fold against the FULL TfR1 ectodomain construct (binder=chain A,
target=chain B numbered 1..N for construct 121-760 human / 123-763 mouse). Reports which target residues
the binder contacts and whether it docks at the APICAL epitope (the organizers' functional-epitope goal)
vs an off-epitope surface (e.g. the transferrin/helical face it should avoid).

Construct numbering (human 121-760): UniProt res R -> chain-B resid (R-120).
  Apical epitope footprint (UniProt 202,203,204,208,209,210,211,212,348,371) -> {82,83,84,88,89,90,91,92,228,251}
  Apical DOMAIN (UniProt ~189-383) -> chain-B 69..263 ; Tyr211 -> 91
  Helical/transferrin face (UniProt ~608-760, avoid) -> chain-B 488..640
Usage: epitope_read.py <complex.(pdb|cif)> [cut=5.0]
"""
import sys
import numpy as np, gemmi

CUT = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
FOOTPRINT = {82, 83, 84, 88, 89, 90, 91, 92, 228, 251}
APICAL = set(range(69, 264))
HELICAL = set(range(488, 641))

def main():
    st = gemmi.read_structure(sys.argv[1]); st.setup_entities(); m = st[0]
    chains = sorted(m, key=lambda c: len([r for r in c]))
    binder = chains[0]                                    # shortest = binder
    targets = chains[1:]                                  # all others = target copy/copies (homodimer ok)
    ba = np.array([[a.pos.x, a.pos.y, a.pos.z] for r in binder for a in r])
    contacts = []                                         # union of construct positions across target chains
    for target in targets:
        for r in target:
            ra = np.array([[a.pos.x, a.pos.y, a.pos.z] for a in r])
            if len(ra) and np.sqrt(((ra[:, None, :] - ba[None, :, :]) ** 2).sum(-1)).min() <= CUT:
                contacts.append(r.seqid.num)
    contacts = sorted(set(contacts))
    n = len(contacts)
    fp = sum(1 for c in contacts if c in FOOTPRINT)
    ap = sum(1 for c in contacts if c in APICAL)
    hx = sum(1 for c in contacts if c in HELICAL)
    apical_frac = ap / n if n else 0.0
    # classify
    if n == 0:
        cls = "no_contact"
    elif apical_frac >= 0.5 and fp >= 1:
        cls = "APICAL"
    elif apical_frac >= 0.5:
        cls = "apical_domain_offsite"   # apical domain but misses the footprint
    elif hx / n >= 0.4:
        cls = "helical_face"            # the site to AVOID
    else:
        cls = "off_epitope"
    print(f"{sys.argv[1].split('/')[-1]}: class={cls} n_contact={n} footprint={fp} apical_frac={apical_frac:.2f} "
          f"helical={hx} contacts={sorted(contacts)[:20]}")

if __name__ == "__main__":
    main()
