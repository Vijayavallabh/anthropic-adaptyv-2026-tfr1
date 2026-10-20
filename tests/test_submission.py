"""Submission-contract tests (Challenge 4). ANARCI disabled so they run CPU-only."""
from adaptyv_tfr1 import submission as S


def _rows(rows):
    return S.validate_rows(rows, track=2, use_anarci=False)


def test_valid_protein_row_passes():
    r = _rows([{"name": "d1", "sequence": "A" * 60, "molecule_class": "protein"}])
    assert r.ok, S.format_report(r)


def test_bad_molecule_class_fails():
    assert not _rows([{"name": "d1", "sequence": "A" * 60, "molecule_class": "peptide"}]).ok


def test_single_chain_accepted_with_warning():
    r = _rows([{"name": "d1", "sequence": "A" * 60, "molecule_class": "single_chain"}])
    assert r.ok and r.n_warnings >= 1  # alias accepted, but warned (brief uses 'protein')


def test_length_bounds():
    assert not _rows([{"name": "d", "sequence": "A" * 9, "molecule_class": "protein"}]).ok
    assert not _rows([{"name": "d", "sequence": "A" * 251, "molecule_class": "protein"}]).ok


def test_non_standard_residues_fail():
    assert not _rows([{"name": "d", "sequence": "A" * 50 + "X" * 5, "molecule_class": "protein"}]).ok


def test_duplicate_name_and_sequence_fail():
    assert not _rows([
        {"name": "d", "sequence": "A" * 60, "molecule_class": "protein"},
        {"name": "d", "sequence": "C" * 60, "molecule_class": "protein"},
    ]).ok
    assert not _rows([
        {"name": "a", "sequence": "A" * 60, "molecule_class": "protein"},
        {"name": "b", "sequence": "A" * 60, "molecule_class": "protein"},
    ]).ok


def test_track_cap_20():
    rows = [{"name": f"d{i}", "sequence": "A" * (40 + i), "molecule_class": "protein"} for i in range(21)]
    assert not _rows(rows).ok  # 21 > 20


def test_fab_requires_vh_vl():
    assert not _rows([{"name": "f", "sequence": "A" * 120, "molecule_class": "fab_kappa"}]).ok


def test_single_chain_colon_rejected():
    assert not _rows([{"name": "d", "sequence": "A" * 30 + ":" + "A" * 30, "molecule_class": "protein"}]).ok


def test_length_category():
    assert S.length_category(30) == "protein_microbinder"
    assert S.length_category(80) == "protein_minibinder"
    assert S.length_category(150) == "large_protein"
