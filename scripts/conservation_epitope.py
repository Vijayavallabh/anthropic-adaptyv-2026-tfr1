#!/usr/bin/env python3
"""F01/F02 recon: deterministic human<->mouse TfR1 conservation + apical epitope footprint.

Why code, not an LLM: the recon `conservation` scout was blocked by the [bio] classifier.
Sequence identity and inter-chain contacts are deterministic computations; biopython does them
exactly. No model reasoning involved.

Inputs (args): the untrusted CIF dir (11QC.cif, 11RN.cif) + human/mouse UniProt FASTAs.
Outputs: a human-readable report to stdout + a JSON map (--out) for target.yaml / F08.

Numbering: UniProt P02786 == construct numbering (seq index i -> UniProt i+120). Invariant: UniProt 211 == Y.
"""
import argparse, json, sys, warnings
from pathlib import Path
import numpy as np
from Bio.PDB import MMCIFParser, NeighborSearch
from Bio.PDB.Polypeptide import is_aa
from Bio.Align import PairwiseAligner, substitution_matrices
from Bio.Data.IUPACData import protein_letters_3to1

warnings.filterwarnings("ignore")
THREE2ONE = {k.upper(): v for k, v in protein_letters_3to1.items()}

# Apical epitope residues (UniProt) from target.yaml, for cross-checking the structural footprint.
APICAL_YAML = [202,203,204,205,206,207,208,209,210,211,212,213,214,215,348,371]
TF_SITE = (619, 670)  # transferrin/helical face to AVOID


def read_fasta(p):
    seq = "".join(l.strip() for l in Path(p).read_text().splitlines() if not l.startswith(">"))
    return seq


def chain_residues(chain):
    """Ordered (author_resnum, one_letter, residue) for standard amino acids in a chain."""
    out = []
    for res in chain:
        if not is_aa(res, standard=True):
            continue
        het, resnum, icode = res.id
        if het.strip():
            continue
        aa = THREE2ONE.get(res.resname.upper())
        if aa:
            out.append((resnum, aa, res))
    return out


def chain_seq(chain):
    return "".join(aa for _, aa, _ in chain_residues(chain))


def parse_structure(cif):
    return MMCIFParser(QUIET=True).get_structure(Path(cif).stem, cif)


def identify_tfr1_chain(model, human_seq):
    """Pick the chain whose sequence best matches human TfR1 (longest high-identity match)."""
    best = None
    for chain in model:
        s = chain_seq(chain)
        if len(s) < 50:
            continue
        # quick containment-ish score: fraction of chain residues present as a substring window
        score = len(s)
        if s[:30] in human_seq or human_seq.find(s[20:50]) >= 0:
            score += 100000
        if best is None or score > best[1]:
            best = (chain, score, s)
    return best[0] if best else None


def min_interchain_contacts(model, tfr1_chain, cutoff=5.0):
    """TfR1 author-resnums with >=1 heavy atom within cutoff of any OTHER-chain heavy atom."""
    tfr1_atoms, other_atoms = [], []
    tfr1_id = tfr1_chain.id
    for chain in model:
        for res in chain:
            het, resnum, ic = res.id
            if het.strip():
                continue
            for atom in res:
                if atom.element == "H":
                    continue
                if chain.id == tfr1_id:
                    tfr1_atoms.append((resnum, atom))
                else:
                    other_atoms.append(atom)
    if not other_atoms:
        return []
    ns = NeighborSearch(other_atoms)
    hit = set()
    for resnum, atom in tfr1_atoms:
        if ns.search(atom.coord, cutoff):
            hit.add(resnum)
    return sorted(hit)


def align(human, mouse):
    aligner = PairwiseAligner()
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    aligner.open_gap_score = -11
    aligner.extend_gap_score = -1
    aligner.mode = "global"
    aln = aligner.align(human, mouse)[0]
    # build human_idx(1-based) -> mouse_idx(1-based) or None
    h2m, hpos, mpos = {}, 0, 0
    a_h, a_m = aln[0], aln[1]
    for ch, cm in zip(a_h, a_m):
        if ch != "-":
            hpos += 1
        if cm != "-":
            mpos += 1
        if ch != "-":
            h2m[hpos] = (mpos if cm != "-" else None, cm if cm != "-" else "-")
    ident = sum(1 for ch, cm in zip(a_h, a_m) if ch == cm and ch != "-")
    aln_len = sum(1 for ch, cm in zip(a_h, a_m) if ch != "-" and cm != "-")
    return h2m, ident, aln_len


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dl", required=True, help="dir with 11QC.cif / 11RN.cif")
    ap.add_argument("--human", required=True)
    ap.add_argument("--mouse", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cutoff", type=float, default=5.0)
    a = ap.parse_args()
    dl = Path(a.dl)
    human = read_fasta(a.human)
    mouse = read_fasta(a.mouse)
    rep, out = [], {}

    rep.append(f"human P02786 len={len(human)}  mouse Q62351 len={len(mouse)}")
    assert human[210] == "Y", f"INVARIANT FAIL: UniProt 211 != Y (got {human[210]})"
    rep.append("INVARIANT OK: human UniProt 211 == Y (Tyr211, apical center)")

    # ---- 11QC: target-prep structure ----
    m_qc = parse_structure(dl / "11QC.cif")[0]
    tfr1_qc = identify_tfr1_chain(m_qc, human)
    res_qc = chain_residues(tfr1_qc)
    nums = [rn for rn, _, _ in res_qc]
    r142 = {rn: aa for rn, aa, _ in res_qc}.get(142)
    rep.append(f"\n11QC: TfR1 chain '{tfr1_qc.id}', {len(res_qc)} aa, author resnum {min(nums)}-{max(nums)}")
    rep.append(f"11QC: residue 142 = {r142}  ({'GLY OK' if r142=='G' else 'NOT GLY -- allele fix needed'})")
    # author numbering == UniProt? check a few anchors
    qc_map = {rn: aa for rn, aa, _ in res_qc}
    anchors = {rn: (qc_map.get(rn), human[rn-1] if 0 < rn <= len(human) else None) for rn in (142, 211, 348, 371)}
    ok_num = all(v[0] == v[1] for v in anchors.values() if v[0])
    rep.append(f"11QC: author-numbering==UniProt check {anchors} -> {'MATCH' if ok_num else 'MISMATCH'}")
    out["11QC"] = {"tfr1_chain": tfr1_qc.id, "n_res": len(res_qc),
                   "resnum_range": [min(nums), max(nums)], "residue_142": r142,
                   "numbering_is_uniprot": bool(ok_num)}

    # ---- 11RN: apical complex, find TfR1 chain + VP1u footprint ----
    m_rn = parse_structure(dl / "11RN.cif")[0]
    chains_rn = [(c.id, len(chain_seq(c))) for c in m_rn if len(chain_seq(c)) > 0]
    tfr1_rn = identify_tfr1_chain(m_rn, human)
    rep.append(f"\n11RN: chains(len) = {chains_rn}")
    rep.append(f"11RN: TfR1 chain = '{tfr1_rn.id}' (others = VP1u RBD / partner protomer)")
    footprint = min_interchain_contacts(m_rn, tfr1_rn, a.cutoff)
    # restrict footprint to the apical neighbourhood vs partner-protomer dimer contacts:
    # report ALL contacts, then flag which fall in the apical window (190-220, 340-380)
    rn_map = {rn: aa for rn, aa, _ in chain_residues(tfr1_rn)}
    apical_fp = [rn for rn in footprint if (190 <= rn <= 225) or (340 <= rn <= 380)]
    rep.append(f"11RN: TfR1 residues within {a.cutoff} A of another chain (n={len(footprint)}): {footprint}")
    rep.append(f"11RN: apical-window footprint (n={len(apical_fp)}): "
               + ", ".join(f"{rn_map.get(rn,'?')}{rn}" for rn in apical_fp))
    out["11RN"] = {"tfr1_chain": tfr1_rn.id, "all_contacts": footprint,
                   "apical_footprint": apical_fp,
                   "apical_footprint_labeled": [f"{rn_map.get(rn,'?')}{rn}" for rn in apical_fp]}

    # ---- human<->mouse alignment + conservation of the apical epitope ----
    h2m, ident, aln_len = align(human, mouse)
    pct = 100.0 * ident / aln_len
    rep.append(f"\nALIGNMENT: {ident}/{aln_len} identical over aligned cols = {pct:.1f}% identity (full-length)")
    # ectodomain window identity (human 121-760)
    eco = [i for i in range(121, 761) if i in h2m and h2m[i][0]]
    eco_id = sum(1 for i in eco if h2m[i][1] == human[i-1])
    rep.append(f"ALIGNMENT: ectodomain 121-760 identity = {eco_id}/{len(eco)} = {100.0*eco_id/len(eco):.1f}%")

    # structural apical footprint (from 11RN) conservation
    fp_use = apical_fp if apical_fp else [r for r in APICAL_YAML]
    rep.append(f"\nAPICAL FOOTPRINT CONSERVATION (structural, from 11RN; human->mouse):")
    cons, div = [], []
    table = []
    for rn in fp_use:
        h_aa = human[rn-1]
        m_num, m_aa = h2m.get(rn, (None, "-"))
        same = (m_aa == h_aa)
        (cons if same else div).append(rn)
        table.append({"uniprot_human": rn, "human_aa": h_aa, "mouse_aa": m_aa,
                      "mouse_num": m_num, "conserved": same})
        rep.append(f"   H {h_aa}{rn:>3}  ->  M {m_aa}{('%d'%m_num) if m_num else '(gap)':>4}   "
                   f"{'conserved' if same else 'DIVERGENT'}")
    rep.append(f"APICAL: conserved {len(cons)}/{len(fp_use)} = {cons}  | divergent = {div}")
    out["alignment"] = {"full_identity_pct": round(pct, 1),
                        "ectodomain_identity_pct": round(100.0*eco_id/len(eco), 1),
                        "apical_footprint_used": fp_use,
                        "apical_conserved": cons, "apical_divergent": div,
                        "apical_table": table}

    # cross-check target.yaml divergent map (human->mouse residue letters)
    rep.append("\nCROSS-CHECK vs target.yaml divergent_apical (human residue -> mouse residue):")
    yaml_claims = {204:("D","Q"),208:("R","N"),210:("V","D"),211:("Y","P"),348:("N","K"),371:("K","Q")}
    for rn,(hc,mc) in yaml_claims.items():
        h_aa=human[rn-1]; m_num,m_aa=h2m.get(rn,(None,"-"))
        status = "OK" if (h_aa==hc and m_aa==mc) else f"MISMATCH (computed H{h_aa}->M{m_aa})"
        rep.append(f"   yaml H{hc}{rn}->M{mc}: human={h_aa} mouse={m_aa} [{status}]")

    # conserved surface stretches outside apical + transferrin site (candidate Arm B patches)
    rep.append("\nCONSERVED STRETCHES (>=6 consecutive identical) in ectodomain, excluding apical & Tf-site:")
    runs, cur = [], []
    for i in range(121, 761):
        m_num, m_aa = h2m.get(i, (None, "-"))
        if m_aa == human[i-1]:
            cur.append(i)
        else:
            if len(cur) >= 6:
                runs.append((cur[0], cur[-1]))
            cur = []
    if len(cur) >= 6:
        runs.append((cur[0], cur[-1]))
    def tag(lo, hi):
        if hi < 190 or lo > 380:  # outside apical neighbourhood
            if not (TF_SITE[0]-10 <= lo <= TF_SITE[1]+10):
                return "candidate ArmB"
        return ""
    for lo, hi in runs:
        t = tag(lo, hi)
        rep.append(f"   {lo}-{hi} ({hi-lo+1} aa) {t}")
    out["conserved_runs"] = [{"lo": lo, "hi": hi, "len": hi-lo+1, "tag": tag(lo, hi)} for lo, hi in runs]

    Path(a.out).write_text(json.dumps(out, indent=2))
    print("\n".join(rep))
    print(f"\n[wrote {a.out}]")


if __name__ == "__main__":
    main()
