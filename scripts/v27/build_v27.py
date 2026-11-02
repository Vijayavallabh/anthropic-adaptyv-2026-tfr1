#!/usr/bin/env python3
# Build v27 = v26 with the 2 phantom-collapse members replaced by vetted clean binders.
#   rank15 resc_e223_m3 (phantom + borderline-novelty) -> resc_v25g3_130 (NOVEL 0.733, switch 2-in-window, mouse cross-reactive)
#   rank18 w4g5_137     (phantom)                        -> SECOND pick (set below after alt validation)
# Other 18 rows BYTE-PRESERVED from v26. molecule_class=protein. CRLF.
import csv, sys
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
V26=f"{REPO}/submissions/tfr1_track2_v26.csv"; V27=f"{REPO}/submissions/tfr1_track2_v27.csv"
MC="protein"
# load candidate seqs
seqs={}
for f in ["v27cands.csv","v27alt.csv"]:
    for r in csv.DictReader(open(f"{SC}/{f}")): seqs[r['name']]=r['sequence'].strip()
SECOND=sys.argv[1] if len(sys.argv)>1 else "resc_v25g5_13_mpnn1__A29HK32_A36HK40"  # overridable
SWAPS={  # OLD v26 name -> (new name, new seq)
 "resc_e223_m3__A17HK21_A34HK37": ("resc_v25g3_130_mpnn1__A80HK45_A49HK39", seqs["resc_v25g3_130_mpnn1__A80HK45_A49HK39"]),
 "w4g5_137_mpnn1_sw3his":          (SECOND, seqs[SECOND]),
}
for nn,ns in SWAPS.values():
    assert ns.isalpha() and ns.upper()==ns, f"bad seq {nn}"
raw=open(V26,"rb").read().split(b"\r\n")
out=[raw[0]]; swapped=0
for line in raw[1:]:
    if not line.strip(): continue
    name=line.split(b",")[0].decode()
    if name in SWAPS:
        nn,ns=SWAPS[name]; out.append(f"{nn},{ns},{MC}".encode()); swapped+=1
    else:
        out.append(line)  # byte-preserved
assert swapped==2, f"swapped={swapped}"
assert len(out)==21, f"rows={len(out)-1}"
open(V27,"wb").write(b"\r\n".join(out)+b"\r\n")
print(f"wrote {V27}: {len(out)-1} rows, {swapped} swaps, 2nd pick={SECOND}")
# verify
for i,r in enumerate(csv.DictReader(open(V27)),1):
    if r['molecule_class']!=MC or not r['sequence'].isalpha(): print(f"  !! rank{i} {r['name']} BAD")
print("v27 molecule_class uniform + sequences clean")
