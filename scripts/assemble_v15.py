#!/usr/bin/env python3
"""Unified v15 assembler: merge robust crown tables + switch genuineness + NOVELTY + sequences across
all waves (batch-1 f30, tier-2 f33, v13), apply the objective-priority gates, and propose a diverse top-20.

Gates (a winner clears all three + novelty hard gate):
  CROWN   : bind_min>=0.30 AND xreact_min>=0.15 (robust 6-sample mean)
  SWITCH  : switch_prob frac>=2 >= FRAC_MIN (clear switch; robust=>=0.8)   [objective #1]
  NOVELTY : single-seq max-TM vs PDB < NOV_MAX (~0.89 = L3/L2 boundary), OR v13-portal-verified-novel
Rank among qualified: robust-switch tier -> XR desc (obj#2) -> BIND desc (obj#3); 3-His breaks ties.
Diversity: dedup by parent backbone; cap <=2 per structural cluster; report generator-family mix.
Usage: assemble_v15.py [--frac-min 0.5] [--robust 0.8] [--nov-max 0.89] [cluster.tsv]
"""
import csv, sys, re, os, argparse
from collections import defaultdict

REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
CROWN_TABLES=[f"{REPO}/runs/f30/reval6/crown_table.tsv", f"{REPO}/runs/f31/reval6/crown_table.tsv", f"{REPO}/runs/f33/robust6/crown_table.tsv"]
SWITCHPROBS =[f"{REPO}/runs/f30/switchprob_pooled.tsv", f"{REPO}/runs/f31/switchprob_pooled.tsv", f"{REPO}/runs/f33/switchprob_pooled.tsv"]
NOVELTIES   =[f"{REPO}/runs/f32/novelty.csv", f"{REPO}/runs/f33/novelty.csv"]
SEQ_SRCS    =[f"{REPO}/runs/f29/combined_crowns.csv", f"{REPO}/runs/f31/exhaustive_all.csv",
              f"{REPO}/runs/f33/switch/reval/crowns.csv", f"{REPO}/submissions/tfr1_track2_v13.csv"]

def ffloat(x):
    try: v=float(x); return v if v==v else None
    except: return None

def lineage(n):
    if n.startswith('rfd4_'): return 'RFD4'
    if n.startswith('w3g'): return 'Genie3-w3'
    if n.startswith('genie_w'): return 'Genie3-v13'
    if n.startswith('e') and n[1:4].isdigit(): return 'RFd1'
    if n[0]=='d' and n[1:3].isdigit(): return 'RFd1'
    return 'other'

def his_count(n):
    m=re.search(r'_sw(\d)(his|b)', n);  return int(m.group(1)) if m else (3 if '3H' in n else 2)

def parent(n):
    n=re.sub(r'__A\d+H.*$','',n)      # exhaustive rescue suffix
    n=re.sub(r'_sw\d(his|b).*$','',n) # greedy/v13 switch suffix
    return n

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('cluster', nargs='?', default=f"{REPO}/runs/f34/cluster/clu_cluster.tsv")
    ap.add_argument('--frac-min', type=float, default=0.5)
    ap.add_argument('--robust', type=float, default=0.8)
    ap.add_argument('--nov-max', type=float, default=0.89)
    a=ap.parse_args()

    CT={}
    for p in CROWN_TABLES:
        if os.path.exists(p):
            for r in csv.DictReader(open(p),delimiter='\t'):
                CT[r['name']]={'BIND':ffloat(r['BIND']),'XR':ffloat(r['XR']),'crown':r['crown']=='1'}
    FR={}
    for p in SWITCHPROBS:
        if os.path.exists(p):
            for line in open(p):
                q=line.split()
                if len(q)<4 or q[0]=='design': continue
                try: FR[q[0]]=float(q[3])
                except: pass
    NOV={}
    for p in NOVELTIES:
        if os.path.exists(p):
            for r in csv.DictReader(open(p)):
                NOV[r['name']]=ffloat(r['singleseq_maxTM_pdb'])
    SEQ={}
    for p in SEQ_SRCS:
        if os.path.exists(p):
            for r in csv.DictReader(open(p)): SEQ.setdefault(r['name'], r['sequence'])
    V13NOVEL=set(r['name'] for r in csv.DictReader(open(f"{REPO}/submissions/tfr1_track2_v13.csv")))
    clu={}
    if os.path.exists(a.cluster):
        for line in open(a.cluster):
            q=line.split()
            if len(q)>=2: clu[q[1].replace('.pdb','')]=q[0]

    def novel_ok(n):
        if n in NOV and NOV[n] is not None: return NOV[n] < a.nov_max, NOV[n]
        if n in V13NOVEL: return True, None   # portal-verified
        return False, None

    rows=[]
    for n,c in CT.items():
        if not c['crown']: continue
        fr=FR.get(n,0.0)
        nok,nv=novel_ok(n)
        rows.append({'name':n,'lin':lineage(n),'his':his_count(n),'XR':c['XR'] or 0,'BIND':c['BIND'] or 0,
                     'frac':fr,'nov':nv,'clu':clu.get(n,n),'parent':parent(n),
                     'robust':fr>=a.robust,'qual':(c['crown'] and fr>=a.frac_min and nok)})
    # dedup by parent: keep best (robust, XR, frac)
    best={}
    for r in sorted(rows, key=lambda r:(-int(r['robust']),-r['XR'],-r['frac'])):
        best.setdefault(r['parent'], r)
    qual=[r for r in best.values() if r['qual']]
    qual.sort(key=lambda r:(-int(r['robust']), -r['XR'], -r['BIND'], -r['his']))

    print(f"=== QUALIFIED CROWNS (crown & frac>={a.frac_min} & novelty<{a.nov_max}) : {len(qual)} unique-parent ===")
    print(f"{'#':>2} {'name':44}{'lin':11}{'H':>2}{'XR':>7}{'BIND':>7}{'frac':>6}{'nov':>6}{'clu':>8}")
    for i,r in enumerate(qual,1):
        nv=f"{r['nov']:.3f}" if r['nov'] is not None else "v13"
        print(f"{i:>2} {r['name']:44}{r['lin']:11}{r['his']:>2}{r['XR']:>7.3f}{r['BIND']:>7.3f}{r['frac']:>6.2f}{nv:>6}{str(r['clu'])[:8]:>8}{' ROB' if r['robust'] else ''}")
    # cap <=2/cluster
    pick=[]; per=defaultdict(int)
    for r in qual:
        if per[r['clu']]>=2: continue
        pick.append(r); per[r['clu']]+=1
        if len(pick)>=20: break
    mix=defaultdict(int)
    for r in pick: mix[r['lin']]+=1
    print(f"\n=== PROPOSED v15 (<=2/cluster): {len(pick)} | mix {dict(mix)} ===")
    for i,r in enumerate(pick,1):
        print(f"  {i:>2} {r['name']:44}{r['lin']:11}H{r['his']} XR{r['XR']:.3f} BIND{r['BIND']:.3f} f{r['frac']:.2f}")

if __name__=='__main__': main()
