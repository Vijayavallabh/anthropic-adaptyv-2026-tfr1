#!/usr/bin/env python3
"""Fragment-aware pose check for the pocket-restrained apical folds (chain A = binder, chain B = apical
fragment 189-383 numbered 1..195; UniProt R -> frag resid R-188). Tests whether a crown's MOUSE binding
is anchored on the CONSERVED cross-reactivity sub-site (identical in mouse) or leans on human<->mouse
DIVERGENT residues (which would make a high mouse ipSAE untrustworthy as cross-reactivity).

  CONSERVED anchors : frag {14,15,21,22} = UniProt 202(I),203(V),209(L),210
  DIVERGENT (mouse) : frag {16,20,23,24,183} = UniProt 204,208(R->N),211,212,371(K->Q)
Usage: pose_subsite.py <complex.pdb> [cut=5.0]  -> one line: n_contact cons div contacts
"""
import sys, numpy as np, gemmi
CUT = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
CONS = {14, 15, 21, 22}
DIV = {16, 20, 23, 24, 183}
st = gemmi.read_structure(sys.argv[1]); st.setup_entities(); m = st[0]
chains = sorted(m, key=lambda c: len([r for r in c]))
binder, targets = chains[0], chains[1:]
ba = np.array([[a.pos.x, a.pos.y, a.pos.z] for r in binder for a in r])
contacts = []
for t in targets:
    for r in t:
        ra = np.array([[a.pos.x, a.pos.y, a.pos.z] for a in r])
        if len(ra) and np.sqrt(((ra[:, None, :] - ba[None, :, :]) ** 2).sum(-1)).min() <= CUT:
            contacts.append(r.seqid.num)
contacts = sorted(set(contacts))
cons = sorted(c for c in contacts if c in CONS)
div = sorted(c for c in contacts if c in DIV)
print(f"n_contact={len(contacts)} cons={len(cons)}{cons} div={len(div)}{div} all={contacts}")
