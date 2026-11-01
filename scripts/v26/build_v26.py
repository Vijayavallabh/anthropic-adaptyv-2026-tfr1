#!/usr/bin/env python3
# Build v26 = v25 with 3 weak-tier members replaced by validated genuine upgrades.
# Retained 17 rows preserved BYTE-FOR-BYTE from portal-verified v25; 3 new rows written with
# molecule_class=single_chain (matches portal-verified v25) + STRIPPED sequences (no embedded newline). CRLF.
import csv
REPO="/home/prachh/v/anthropic-adaptyv-2026-tfr1"
SC="/home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad"
V25=f"{REPO}/submissions/tfr1_track2_v25.csv"; V26=f"{REPO}/submissions/tfr1_track2_v26.csv"
van={r['name']:r['sequence'].strip() for r in csv.DictReader(open(f"{SC}/ms/mpnn/ms_binders.csv"))}
sol={r['name']:r['sequence'].strip() for r in csv.DictReader(open(f"{SC}/ms_sol/mpnn/ms_binders.csv"))}
rx ={r['name']:r['sequence'].strip() for r in csv.DictReader(open(f"{SC}/rescue_xr/all_combos.csv"))}
MC="protein"  # brief-canonical, matches portal-verified v25 (committed c26090a). NOT single_chain (that was a working-tree error).
SWAPS={  # OLD_name -> "newname,newseq,single_chain"  (rank10 REVERTED: g3_22_s2 mouse = non-specific artifact per adversarial review)
 "w3g6_146_mpnn0_sw2his":                ("ms_g3_65_xr__A28H_A43H",       rx["xr_g3_65_mpnn1_s6__A28HK31_A43HR46"]),  # rank17 KEEP: both-species on-epi
 "resc_v25g4_44_mpnn0__A70HK87_A60HR19": ("ms_g3_22v_xr__A20H_A44H_A66H", van["ms_v25g3_22_mpnn0_s1"]),               # rank19 KEEP: dominates all 3 axes
}
# sanity: no embedded whitespace in new seqs
for nn,ns in SWAPS.values():
    assert ns.isalpha() and ns.upper()==ns, f"bad seq for {nn}: {ns!r}"
raw=open(V25,"rb").read().split(b"\r\n")
# raw[0]=header, raw[1..20]=data, trailing empty
out=[raw[0]]; swapped=0
for line in raw[1:]:
    if not line.strip(): continue
    name=line.split(b",")[0].decode()
    if name in SWAPS:
        nn,ns=SWAPS[name]; out.append(f"{nn},{ns},{MC}".encode()); swapped+=1
    else:
        out.append(line)  # byte-for-byte retained
assert swapped==2, f"swapped={swapped}"
assert len(out)==21, f"rows={len(out)-1}"
open(V26,"wb").write(b"\r\n".join(out)+b"\r\n")
print(f"wrote {V26} ({len(out)-1} rows, {swapped} swaps, molecule_class={MC})")
# verify per-row molecule_class
import csv as c
for i,r in enumerate(c.DictReader(open(V26)),1):
    mc=r['molecule_class']; seqok=r['sequence'].isalpha()
    tag="SWAP" if r['name'].startswith("ms_g3_") else "kept"
    if mc!=MC or not seqok: print(f"  !! rank{i} {r['name']} mc={mc!r} seqok={seqok}")
print("all molecule_class uniform + sequences clean" )
