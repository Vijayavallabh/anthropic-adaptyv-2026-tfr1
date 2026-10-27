#!/usr/bin/env python3
"""Build joint multi-state complexes for cross-reactivity MPNN (objective #2 lever).
For each crown backbone: chain A = binder docked on HUMAN apical, B = human target, C = binder docked on
MOUSE apical (same residue numbering), D = mouse target. Redesign ONLY binder interface positions (within
CUT of either target), TIE A_i<->C_i so one sequence serves both orthologs, and FIX the switch-His + all
non-interface core (preserve the validated fold + switch). Emits joint PDBs + ProteinMPNN chains/fixed/tied
jsonls. Run with the protenix venv (gemmi). Drafted by the assistant (ambition-lift depth pass, 2026-10-27)."""
import csv, glob, json, sys
from pathlib import Path
import gemmi

REPO = Path("/home/prachh/v/anthropic-adaptyv-2026-tfr1")
CUT = 6.0
OUT = REPO/"runs/jxr"; (OUT/"pdb").mkdir(parents=True, exist_ok=True)

def find_complex(name, species):
    roots = [f"runs/f33/robust6/boltz_{species[0]}", f"runs/f30/reval6/boltz_{species[0]}",
             f"runs/f33/switch/reval/boltz_{species[0]}"]
    for r in roots:
        g = sorted(glob.glob(f"{REPO}/{r}/**/predictions/{name}/{name}_model_*.pdb", recursive=True))
        if g: return g[0]
    return None

def load_bt(pdb):
    st = gemmi.read_structure(pdb); st.setup_entities(); m = st[0]
    chs = list(m)
    chs.sort(key=lambda c: -sum(1 for _ in c))     # target (bigger) first
    tgt, bnd = chs[0], chs[1]
    return bnd, tgt

def coords(res): return [[a.pos.x,a.pos.y,a.pos.z] for a in res]
def one(res):
    t = gemmi.find_tabulated_residue(res.name); return t.one_letter_code.upper() if t else "X"

def iface(binder, tgt):
    import math
    ta = [p for r in tgt for p in coords(r)]
    s = set()
    for i, r in enumerate(binder, 1):
        for p in coords(r):
            if any((p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2 <= CUT*CUT for q in ta):
                s.add(i); break
    return s

def addchain(M, name, src):
    ch = gemmi.Chain(name)
    for i, r in enumerate(src, 1):
        nr = gemmi.Residue(); nr.name = r.name; nr.seqid = gemmi.SeqId(i, ' ')
        for a in r:
            na = gemmi.Atom(); na.name=a.name; na.element=a.element; na.pos=a.pos; na.b_iso=a.b_iso; na.occ=1.0
            nr.add_atom(na)
        ch.add_residue(nr)
    M.add_chain(ch)

def main():
    names = sys.argv[1].split(",")
    chains={}; fixed={}; tied={}; meta={}
    for n in names:
        hp = find_complex(n,"human"); mp = find_complex(n,"mouse")
        if not hp or not mp:
            print(f"SKIP {n}: h={bool(hp)} m={bool(mp)}"); continue
        hb, ht = load_bt(hp); mb, mt = load_bt(mp)
        bseq = "".join(one(r) for r in hb); N = len(bseq)
        his = [i for i,c in enumerate(bseq,1) if c=="H"]
        ifh = iface(hb, ht); ifm = iface(mb, mt)
        design = sorted((ifh | ifm) - set(his))        # redesign interface, keep His
        if not design:
            print(f"SKIP {n}: no designable interface"); continue
        st = gemmi.Structure(); st.add_model(gemmi.Model("1")); M = st[0]
        addchain(M,"A",hb); addchain(M,"B",ht); addchain(M,"C",mb); addchain(M,"D",mt)
        pdb = OUT/"pdb"/f"{n}.pdb"; st.write_pdb(str(pdb))
        chains[n] = [["A","C"],["B","D"]]              # design A,C ; fix B,D
        fx = [p for p in range(1,N+1) if p not in design]   # fix His + non-interface on both A and C
        fixed[n] = {"A": fx, "C": fx}
        tied[n] = [{"A":[p], "C":[p]} for p in design]      # tie A_i <-> C_i
        meta[n] = dict(N=N, nHis=len(his), his=his, n_iface_h=len(ifh), n_iface_m=len(ifm),
                       n_design=len(design), design=design)
        print(f"{n}: N={N} His={len(his)} iface(h={len(ifh)},m={len(ifm)}) design={len(design)}")
    json.dump(chains, open(OUT/"chains.jsonl","w"))
    json.dump(fixed,  open(OUT/"fixed.jsonl","w"))
    json.dump(tied,   open(OUT/"tied.jsonl","w"))
    json.dump(meta,   open(OUT/"meta.json","w"), indent=1)
    print(f"\nwrote {len(meta)} joint complexes + chains/fixed/tied jsonls -> {OUT}")

if __name__ == "__main__": main()
