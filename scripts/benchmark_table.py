#!/usr/bin/env python3
"""Master every-metric benchmark table for the 20 v15 designs = the FROZEN baseline to beat.
Merges per-folder robust ipSAE (crown_table.tsv: b_h,c_h,b_m,c_m across f30/f31/f33), switch
genuineness (switchprob_pooled.tsv frac>=2 contacts over replicate folds), novelty (novelty.csv
single-seq ESMFold max-TM vs PDB), + GRAVY, length, nHis, lineage. v13-evidence fallback for the
RFD4/RFd1/wave-2-Genie hedges that predate the robust re-fold.
Output: runs/bench/v15_master.tsv  (one row per design, every evaluation axis side by side).
Drafted by the assistant (ambition-lift depth pass, 2026-10-27)."""
import csv, os, re
from pathlib import Path

REPO = "/home/prachh/v/anthropic-adaptyv-2026-tfr1"
KD = {'A':1.8,'R':-4.5,'N':-3.5,'D':-3.5,'C':2.5,'Q':-3.5,'E':-3.5,'G':-0.4,'H':-3.2,'I':4.5,
      'L':3.8,'K':-3.9,'M':1.9,'F':2.8,'P':-1.6,'S':-0.8,'T':-0.7,'W':-0.9,'Y':-1.3,'V':4.2}
def gravy(s): return round(sum(KD.get(c,0) for c in s)/len(s),3) if s else None
def ff(x):
    try: v=float(x); return v if v==v else None
    except: return None
def nhis(n):
    m=re.search(r'sw(\d)',n); return int(m.group(1)) if m else ''

# per-folder crown tables: name b_h c_h BIND b_m c_m XR crown
CT={}
for p in ["runs/f30/reval6/crown_table.tsv","runs/f31/reval6/crown_table.tsv","runs/f33/robust6/crown_table.tsv"]:
    fp=f"{REPO}/{p}"
    if os.path.exists(fp):
        for r in csv.DictReader(open(fp),delimiter='\t'):
            CT.setdefault(r['name'],{k:ff(r.get(k)) for k in ('b_h','c_h','b_m','c_m','BIND','XR')})
# switch genuineness (frac of replicate folds with >=2 His-cation contacts)
FR={}
for p in ["runs/f30/switchprob_pooled.tsv","runs/f31/switchprob_pooled.tsv","runs/f33/switchprob_pooled.tsv"]:
    fp=f"{REPO}/{p}"
    if os.path.exists(fp):
        for line in open(fp):
            q=line.split()
            if len(q)>=5 and q[0]!='design':
                try: FR.setdefault(q[0],{'n':q[1],'mean':q[2],'frac':float(q[3])})
                except: pass
# novelty
NOV={}
for p in ["runs/f32/novelty.csv","runs/f33/novelty.csv"]:
    fp=f"{REPO}/{p}"
    if os.path.exists(fp):
        for r in csv.DictReader(open(fp)): NOV.setdefault(r['name'],(r.get('singleseq_maxTM_pdb'),r.get('verdict')))
# v13 evidence fallback
V13={}
fp=f"{REPO}/submissions/tfr1_track2_v13_evidence.csv"
if os.path.exists(fp):
    for r in csv.DictReader(open(fp)): V13[r['name']]=r

rows=list(csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v15.csv")))
ev={r['name']:r for r in csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v15_evidence.csv"))}

out=Path(f"{REPO}/runs/bench"); out.mkdir(parents=True,exist_ok=True)
cols=["rank","name","lineage","len","nHis","b_h","c_h","b_m","c_m","bind_min","xreact_min",
      "switch_frac","switch_n","novelty_maxTM","novelty_verdict","GRAVY","source"]
with open(out/"v15_master.tsv","w",newline="") as fo:
    w=csv.writer(fo,delimiter='\t'); w.writerow(cols)
    for i,r in enumerate(rows,1):
        n=r['name']; seq=r['sequence']; e=ev.get(n,{})
        ct=CT.get(n,{}); fr=FR.get(n,{}); nov=NOV.get(n,(e.get('novelty_maxTM',''),e.get('novelty_verdict','')))
        src="robust-refold" if n in CT else "v13-evidence"
        bh,ch,bm,cm=ct.get('b_h'),ct.get('c_h'),ct.get('b_m'),ct.get('c_m')
        bind=ct.get('BIND'); xr=ct.get('XR')
        if bind is None: bind=ff(e.get('bind_min')) or ff(V13.get(n,{}).get('bind_min'))
        if xr is None: xr=ff(e.get('xreact_min')) or ff(V13.get(n,{}).get('xreact_min'))
        g=lambda x: ("" if x is None else (f"{x:.3f}" if isinstance(x,float) else x))
        sw = f"{fr['frac']:.2f}" if 'frac' in fr else (e.get('switch_frac','') or '')
        w.writerow([i,n,e.get('lineage',''),len(seq),nhis(n),g(bh),g(ch),g(bm),g(cm),g(bind),g(xr),
                    sw,fr.get('n',''),g(nov[0]) if nov[0] else '',nov[1] or '',gravy(seq),src])
print("WROTE runs/bench/v15_master.tsv\n")
hdr=f"{'#':>2} {'name':34} {'b_h':>5} {'c_h':>5} {'b_m':>5} {'c_m':>5} {'BIND':>5} {'XR':>5} {'sw':>4} {'nov':>5} {'GRAVY':>6}"
print(hdr); print("-"*len(hdr))
for r in csv.DictReader(open(out/"v15_master.tsv"),delimiter='\t'):
    d=lambda k: (r[k] if r[k] else '-')
    print(f"{r['rank']:>2} {r['name'][:34]:34} {d('b_h'):>5} {d('c_h'):>5} {d('b_m'):>5} {d('c_m'):>5} "
          f"{d('bind_min'):>5} {d('xreact_min'):>5} {d('switch_frac'):>4} {d('novelty_maxTM'):>5} {d('GRAVY'):>6}")
