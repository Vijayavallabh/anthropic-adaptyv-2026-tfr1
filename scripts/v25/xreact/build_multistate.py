#!/usr/bin/env python3
# Build a ProteinMPNN multi-state construct for cross-reactive (human AND mouse) binder design.
# From a human-docked complex (chain A=binder, chain B=human apical 195aa), emit a 4-chain PDB:
#   A = binder (state-1 coords), B = human apical, C = binder (state-2, same coords), D = mouse apical
#   (B's backbone N/CA/C/O relabeled to the mouse apical sequence; sidechains dropped — MPNN is
#   backbone-based and encodes fixed-chain identity from resname). A and C are tied 1:1 downstream,
#   so MPNN designs ONE binder sequence compatible with BOTH targets.
# Usage: build_multistate.py <complex.pdb> <mouse_apical.seq> <out.pdb>  (prints BINDER_LEN=<n>)
import sys
AA3={'A':'ALA','R':'ARG','N':'ASN','D':'ASP','C':'CYS','Q':'GLN','E':'GLU','G':'GLY','H':'HIS',
     'I':'ILE','L':'LEU','K':'LYS','M':'MET','F':'PHE','P':'PRO','S':'SER','T':'THR','W':'TRP',
     'Y':'TYR','V':'VAL'}
BB={' N  ',' CA ',' C  ',' O  '}
cx, mouse_f, out = sys.argv[1], sys.argv[2], sys.argv[3]
mouse=open(mouse_f).read().strip()
# parse chains A (binder) and B (target) as ordered lists of (resseq, [atomlines])
def parse(pdb):
    chains={}
    for ln in open(pdb):
        if ln[:4]!="ATOM": continue
        ch=ln[21]; rs=ln[22:27]
        chains.setdefault(ch,{}).setdefault(rs,[]).append(ln)
    return chains
ch=parse(cx)
# pick binder chain = 'A', target = 'B' (Protenix convention)
bch='A' if 'A' in ch else sorted(ch)[0]
tch='B' if 'B' in ch else sorted(ch)[-1]
binder=list(ch[bch].items()); target=list(ch[tch].items())
Lb=len(binder); Lt=len(target)
if Lt!=len(mouse):
    sys.stderr.write(f"WARN target len {Lt} != mouse len {len(mouse)}; threading by min\n")
def emit(atomlines, newchain, newresnum, resname=None):
    o=[]
    for ln in atomlines:
        if resname is not None and ln[12:16] not in BB:  # drop sidechain for threaded target
            continue
        nn=ln[:17]+((resname+' ')[:3] if resname else ln[17:20])+ln[20:21]+newchain+f"{newresnum:>4} "+ln[27:]
        o.append(nn)
    return o
lines=[]; an=1
def renumber(block):  # reassign atom serials sequentially
    global an
    out=[]
    for ln in block:
        out.append(ln[:6]+f"{an:>5}"+ln[11:]); an+=1
    return out
# chain A: binder state1
for i,(rs,al) in enumerate(binder,1): lines+=renumber(emit(al,'A',i))
lines.append("TER\n")
# chain B: human apical (keep as-is)
for i,(rs,al) in enumerate(target,1): lines+=renumber(emit(al,'B',i))
lines.append("TER\n")
# chain C: binder state2 (same coords)
for i,(rs,al) in enumerate(binder,1): lines+=renumber(emit(al,'C',i))
lines.append("TER\n")
# chain D: mouse apical (backbone of B + mouse resnames)
for i,(rs,al) in enumerate(target,1):
    if i>len(mouse): break
    lines+=renumber(emit(al,'D',i,resname=AA3.get(mouse[i-1],'ALA')))
lines.append("TER\nEND\n")
open(out,'w').write("".join(lines))
print(f"BINDER_LEN={Lb}")
