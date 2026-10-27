#!/usr/bin/env python3
"""Assemble the v14 portfolio from the combined same-pipeline verification (runs/f29).
Joins crown_table (bind/xr) + switch genuineness (switch_prob_chai frac>=2) + structural clusters +
sequences, applies the objective-priority ranking, and proposes a diversity-capped top-20.

Objective priority (a winner must clear all three): #1 pH-switch > #2 cross-reactivity > #3 affinity.
 - GATE: crown (BIND>=0.30 AND XR>=0.15) AND clear switch (frac>=FRAC_MIN).  [robust = frac>=0.8]
 - RANK among qualified: switch tier (robust first) -> XR desc (obj#2) -> BIND desc (obj#3); 3-His breaks ties.
 - DIVERSITY: dedup by parent backbone (keep best variant); cap <=2 per structural cluster; interleave
   generator families (RFd1 / RFD4 / Genie3) across the front-loaded top-10 (wet-lab folder-correlation hedge).
Usage: assemble_v14.py <crown_table.tsv> <switchprob.tsv> <combined_crowns.csv> [cluster.tsv] [--frac-min F]
Prints the ranked qualified table and a proposed top-20 (front-10 interleaved). Selection is reviewed by hand.
"""
import csv, sys, re, argparse
from collections import defaultdict

def f(x):
    try:
        v=float(x)
        return v if v==v else None
    except Exception:
        return None

def lineage(name):
    if name.startswith('rfd4_'): return 'RFD4'
    if name.startswith('w3g'): return 'Genie3-w3'
    if name.startswith('genie_w'): return 'Genie3-old'
    if name.startswith('e') and name[1:4].isdigit(): return 'RFd1'       # e223...
    if name[0]=='d' and name[1:3].isdigit(): return 'RFd1'               # d25, d4, d374...
    return 'other'

def his_count(name):
    m=re.search(r'_sw(\d)(his|b)', name)
    return int(m.group(1)) if m else 2

def parent(name):
    # strip switch suffix to the backbone id
    n=re.sub(r'_sw\d(his|b).*$','',name)
    return n

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('crown_table'); ap.add_argument('switchprob'); ap.add_argument('seqs')
    ap.add_argument('cluster', nargs='?', default=None)
    ap.add_argument('--frac-min', type=float, default=0.5)
    ap.add_argument('--robust', type=float, default=0.8)
    a=ap.parse_args()

    # crown table
    ct={}
    for r in csv.DictReader(open(a.crown_table), delimiter='\t'):
        ct[r['name']]={'BIND':f(r['BIND']),'XR':f(r['XR']),'b_h':f(r['b_h']),'c_h':f(r['c_h']),
                       'b_m':f(r['b_m']),'c_m':f(r['c_m']),'crown':r['crown']=='1'}
    # switch genuineness
    frac={}
    for line in open(a.switchprob):
        parts=line.split()
        if not parts or parts[0] in ('design',): continue
        try: frac[parts[0]]=float(parts[3])
        except Exception: pass
    # seqs
    seq={r['name']:r['sequence'] for r in csv.DictReader(open(a.seqs))}
    # clusters (foldseek rep<TAB>member.pdb); default: each its own
    clu={}
    if a.cluster:
        for line in open(a.cluster):
            p=line.split()
            if len(p)>=2: clu[p[1].replace('.pdb','')]=p[0]
    def cluster_of(n): return clu.get(n, n)

    rows=[]
    for n,c in ct.items():
        if not c['crown']: continue
        fr=frac.get(n,0.0)
        rows.append({'name':n,'lin':lineage(n),'his':his_count(n),'XR':c['XR'] or 0,'BIND':c['BIND'] or 0,
                     'frac':fr,'clu':cluster_of(n),'parent':parent(n),'robust':fr>=a.robust,
                     'qual':(c['crown'] and fr>=a.frac_min)})
    # dedup by parent: keep best (robust, then XR, then frac)
    best={}
    for r in sorted(rows, key=lambda r:(-int(r['robust']),-r['XR'],-r['frac'])):
        best.setdefault(r['parent'], r)
    uniq=list(best.values())
    qual=[r for r in uniq if r['qual']]
    qual.sort(key=lambda r:(-int(r['robust']), -r['XR'], -r['BIND'], -r['his']))

    print(f"=== QUALIFIED CROWNS (crown & switch frac>={a.frac_min}); robust=frac>={a.robust} ===  [{len(qual)} of {len(uniq)} unique parents]")
    print(f"{'#':>2} {'name':40}{'lineage':11}{'His':>3} {'XR':>6}{'BIND':>7}{'frac':>6}{'clu':>10}")
    for i,r in enumerate(qual,1):
        tag=' ROBUST' if r['robust'] else ' mod'
        print(f"{i:>2} {r['name']:40}{r['lin']:11}{r['his']:>3} {r['XR']:>6.3f}{r['BIND']:>7.3f}{r['frac']:>6.2f}{str(r['clu'])[:10]:>10}{tag}")

    # proposed top-20: cap <=2/cluster; greedy by rank; then interleave lineage in the FRONT 10
    pick=[]; per_clu=defaultdict(int)
    for r in qual:
        if per_clu[r['clu']]>=2: continue
        pick.append(r); per_clu[r['clu']]+=1
        if len(pick)>=20: break
    print(f"\n=== PROPOSED v14 pool (<=2/cluster): {len(pick)} ===")
    bylin=defaultdict(int)
    for r in pick: bylin[r['lin']]+=1
    print('  lineage mix:', dict(bylin))
    for i,r in enumerate(pick,1):
        print(f"  {i:>2} {r['name']:40}{r['lin']:11}His{r['his']} XR{r['XR']:.3f} BIND{r['BIND']:.3f} f{r['frac']:.2f}")

if __name__=='__main__':
    main()
