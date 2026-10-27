#!/usr/bin/env python3
"""ACCURATE switch-genuineness gate (objective #1) via JustHisPKa (Hogues/Sulea JCIM 2025, MUE 0.4 vs
PROPKA ~1.0). For each crown's binder (chain A of the ON-state complex): AmberTools prep (pdb4amber ->
tleap ff14SB -> ambpdb mol2 -> push_renum) then justHisPKa per switch-His. A switch-His must titrate
IN the 6.0-7.4 window (neutral @7.4, protonated @6.0). Reports per-His pKa, protonation swing
(nH(6.0)-nH(7.4)), in-window count, and total swing = the thermodynamic switch strength that geometry
(switch_frac) and PROPKA (weak, R^2~0.05) cannot rank. Drafted by the assistant (ambition-lift, 2026-10-27).
Usage: justhispka_switch.py <name_TAB_complex.pdb .tsv> [out.tsv]"""
import csv, subprocess, sys, os, shutil
from pathlib import Path
REPO=Path("/home/prachh/v/anthropic-adaptyv-2026-tfr1")
AMBER=Path("/home/prachh/miniconda3/envs/ambertools"); AB=AMBER/"bin"
JHP=REPO/"tools/justhispka/justHisPKa"
RENUM=REPO/"tools/justhispka/prep.dir/bin/push_renum.sh"
WORK=REPO/"runs/jhp"; WORK.mkdir(parents=True,exist_ok=True)
ENV=dict(os.environ, AMBERHOME=str(AMBER), PATH=f"{AB}:{os.environ.get('PATH','')}")
def nH(pka,pH): return 1.0/(1.0+10**(pH-pka))
def sh(cmd, cwd, inp=None):
    return subprocess.run(cmd, cwd=str(cwd), env=ENV, input=inp, capture_output=True, text=True, shell=isinstance(cmd,str))
def prep(name, cpdb, d):
    d.mkdir(parents=True, exist_ok=True)
    # extract binder chain A
    with open(d/"binder.pdb","w") as f:
        for l in open(cpdb):
            if l.startswith("ATOM") and l[21]=="A": f.write(l)
        f.write("TER\nEND\n")
    sh([str(AB/"pdb4amber"),"-i","binder.pdb","-o","p2.pdb"], d)
    if not (d/"p2.pdb").exists(): return None
    # synth renum.txt in push_renum format: resname origresnum chain seqindex
    seen=set(); i=0; lines=[]
    for l in open(d/"p2.pdb"):
        if l.startswith("ATOM"):
            rn,ch,rs=l[17:20].strip(),l[21],int(l[22:26])
            k=(ch,rs)
            if k not in seen: seen.add(k); i+=1; lines.append(f"{rn} {rs} {ch} {i}")
    (d/"p2_renum.txt").write_text("\n".join(lines)+"\n")
    sh([str(AB/"tleap"),"-f","-"], d, inp="source leaprc.protein.ff14SB\nm = loadpdb p2.pdb\nsaveamberparm m p3.prmtop p3.inpcrd\nquit\n")
    if not (d/"p3.prmtop").exists(): return None
    r=sh(f"{AB}/ambpdb -p p3.prmtop -c p3.inpcrd -mol2 -sybyl > p4.mol2", d)
    r=sh(f"bash {RENUM} p2.pdb p2_renum.txt p4.mol2 > prep.mol2", d)
    if not (d/"prep.mol2").stat().st_size: return None
    return d/"prep.mol2", d/"p3.prmtop"
def jhp(mol2, prmtop, sid):
    r=sh([str(JHP), f"MOL={mol2.name}", f"PRM={prmtop.name}", f"SID={sid}", "-b"], mol2.parent)
    out=(r.stdout or r.stderr).strip().splitlines()
    try: return float(out[0])
    except: return None
def main():
    tsv=sys.argv[1]; outp=sys.argv[2] if len(sys.argv)>2 else str(REPO/"runs/bench/switch_justhispka.tsv")
    # name->sequence source (3rd positional arg); defaults to v15 for backward compatibility.
    seqs_csv=sys.argv[3] if len(sys.argv)>3 else str(REPO/"submissions/tfr1_track2_v15.csv")
    seqs={r['name']:r['sequence'] for r in csv.DictReader(open(seqs_csv))}
    rows=[l.rstrip("\n").split('\t') for l in open(tsv) if l.strip() and not l.startswith('#')]
    res=[]
    for name,cpdb in rows:
        seq=seqs.get(name)
        if not seq: continue
        his=[i+1 for i,c in enumerate(seq) if c=='H']
        d=WORK/name
        p=prep(name,cpdb,d)
        if not p: res.append((name,None,his)); print(f"{name}: PREP FAILED"); continue
        mol2,prmtop=p
        pkas={}
        for h in his:
            pk=jhp(mol2,prmtop,h); pkas[h]=pk
        res.append((name,pkas,his))
        shown=" ".join(f"{h}:{(f'{v:.2f}' if v is not None else 'ERR')}" for h,v in pkas.items())
        print(f"{name}: {shown}")
    with open(outp,"w") as fo:
        fo.write("name\tnHis\tpKas\tn_inwindow\ttotal_swing\tmax_swing_pka\tverdict\n")
        for name,pkas,his in res:
            if not pkas: fo.write(f"{name}\t{len(his)}\t\t\t\t\tPREP-FAIL\n"); continue
            vals=[(h,v) for h,v in pkas.items() if v is not None]
            inwin=[v for h,v in vals if 6.0<=v<=7.4]
            swings=[(nH(v,6.0)-nH(v,7.4)) for h,v in vals]
            tot=sum(swings);
            best=max(((nH(v,6.0)-nH(v,7.4)),v) for h,v in vals) if vals else (0,None)
            verdict=("GENUINE" if (inwin or tot>=0.5) else "WEAK" if tot>=0.25 else "DEAD")
            pkstr=",".join(f"{h}:{v:.2f}" for h,v in vals)
            fo.write(f"{name}\t{len(his)}\t{pkstr}\t{len(inwin)}\t{tot:.2f}\t{best[1] if best[1] else ''}\t{verdict}\n")
    print(f"\nWROTE {outp}")
    print(f"\n{'name':34} {'nHis':>4} {'inwin':>5} {'swing':>5} {'verdict':>8}  pKas(JustHisPKa)")
    print("-"*92)
    for name,pkas,his in res:
        if not pkas: print(f"{name[:34]:34} {'':>4} {'':>5} {'':>5} {'PREP-FAIL':>8}"); continue
        vals=[(h,v) for h,v in pkas.items() if v is not None]
        inwin=sum(1 for h,v in vals if 6.0<=v<=7.4); tot=sum(nH(v,6.0)-nH(v,7.4) for h,v in vals)
        verdict=("GENUINE" if (inwin or tot>=0.5) else "WEAK" if tot>=0.25 else "DEAD")
        print(f"{name[:34]:34} {len(his):>4} {inwin:>5} {tot:>5.2f} {verdict:>8}  {[f'{v:.2f}' for h,v in vals]}")
if __name__=="__main__": main()
