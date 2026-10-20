"""Smoke tests — the fast CPU-only verification gate (run by ./init.sh).

These catch the mechanical mistakes that silently poison a design campaign:
a mis-pasted target sequence, a wrong numbering window, a corrupted contract.
"""
from pathlib import Path

import yaml

import adaptyv_tfr1

ROOT = Path(__file__).resolve().parents[1]
AA = set("ACDEFGHIKLMNPQRSTVWY")


def _target():
    return yaml.safe_load((ROOT / "configs" / "target.yaml").read_text())


def test_package_imports():
    assert adaptyv_tfr1.__version__


def test_objective_priority():
    cfg = _target()
    assert cfg["objective_priority"] == ["ph_selective", "cross_reactive", "affinity"]
    assert cfg["target"]["uniprot"].startswith("P02786")


def test_target_sequence_window():
    cfg = _target()
    seq = cfg["target"]["sequence"].strip()
    lo, hi = cfg["target"]["construct_residues"]
    assert len(seq) == hi - lo + 1, (len(seq), hi - lo + 1)
    assert set(seq) <= AA, sorted(set(seq) - AA)


def test_submission_molecule_classes():
    # Challenge 4 allowed set — NOT "single_chain" (that was a different host).
    allowed = set(_target()["submission"]["molecule_class_allowed"])
    assert allowed == {"protein", "nanobody", "scfv", "fab_kappa", "fab_lambda"}
