"""F02 target-prep checks: the human target + mouse model + epitope sets are correct.

These guard the prep logic (clean single-subunit target, Gly142, correct mouse threading, well-formed
3-arm hotspots). Skips if the artifacts haven't been generated yet (run scripts/f02_target_prep.py +
scripts/f02_mouse_model.py)."""
import json
import warnings
from pathlib import Path

import pytest

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
TGT = ROOT / "data" / "targets"
HUMAN = TGT / "tfr1_human_ecto_A.pdb"
MOUSE = TGT / "tfr1_mouse_ecto_A.pdb"
EPI = TGT / "epitopes.json"

pytestmark = pytest.mark.skipif(not HUMAN.exists(), reason="F02 artifacts not generated yet")


def _resmap(pdb):
    from Bio.PDB import PDBParser
    from Bio.PDB.Polypeptide import is_aa
    from Bio.Data.IUPACData import protein_letters_3to1
    t2o = {k.upper(): v for k, v in protein_letters_3to1.items()}
    s = PDBParser(QUIET=True).get_structure("x", str(pdb))
    chains = [c.id for c in s[0]]
    rmap = {r.id[1]: t2o.get(r.resname.upper(), "X")
            for c in s[0] for r in c if is_aa(r, standard=True) and not r.id[0].strip()}
    het = [r.resname for c in s[0] for r in c if r.id[0].strip()]
    return chains, rmap, het


def test_human_target_clean_single_subunit():
    chains, rmap, het = _resmap(HUMAN)
    assert chains == ["A"], f"expected single chain A, got {chains}"
    assert len(rmap) == 639, f"expected 639 aa, got {len(rmap)}"
    assert min(rmap) == 122 and max(rmap) == 760
    assert rmap[142] == "G", "allele invariant: 142 must be Gly"
    assert rmap[211] == "Y", "numbering invariant: UniProt 211 must be Tyr"
    assert not het, f"glycans/hetero should be stripped, found {het}"


@pytest.mark.skipif(not MOUSE.exists(), reason="mouse model not built yet")
def test_mouse_model_threaded_correctly():
    _, hmap, _ = _resmap(HUMAN)
    _, mmap, _ = _resmap(MOUSE)
    assert len(mmap) == 639
    # divergent apical positions must carry the mouse identity
    for rn, aa in [(204, "Q"), (208, "N"), (211, "D"), (348, "K"), (371, "Q")]:
        assert mmap[rn] == aa, f"mouse {rn} should be {aa}, got {mmap[rn]}"
    # conserved positions unchanged
    for rn in (202, 203, 209):
        assert mmap[rn] == hmap[rn], f"conserved {rn} changed: {hmap[rn]}->{mmap[rn]}"
    # overall identity ~78%
    same = sum(1 for rn in hmap if hmap[rn] == mmap.get(rn))
    assert 0.74 <= same / len(hmap) <= 0.82, f"identity {same/len(hmap):.3f} outside 74-82%"


def test_epitopes_three_arms():
    e = json.loads(EPI.read_text())
    for arm in ("armA_apical_human", "armC_conserved_apical_subsite", "armB_conserved_nonapical"):
        assert arm in e and e[arm]["hotspots"], f"{arm} missing/empty"
    # Arm C core is the conserved subset of the apical footprint
    assert set(e["armC_conserved_apical_subsite"]["hotspots"]) <= set(e["armA_apical_human"]["hotspots"])
    assert set(e["armC_conserved_apical_subsite"]["hotspots"]) == {202, 203, 209}
    # Arm B is outside the apical domain and the transferrin site, and avoids the dimer interface
    armB = set(e["armB_conserved_nonapical"]["hotspots"])
    assert armB, "Arm B empty"
    assert not (armB & set(range(189, 384))), "Arm B overlaps apical domain"
    assert not (armB & set(range(619, 671))), "Arm B overlaps transferrin site"
    assert not (armB & set(e["exclude"]["dimer_interface"])), "Arm B overlaps dimer interface"
