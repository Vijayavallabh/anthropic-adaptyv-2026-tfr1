#!/usr/bin/env python3
"""F02: build the mouse TfR1 model by threading mouse (Q62351) onto the 11QC chain-A backbone.

Runs in .venv-rosetta (pyrosetta; no biopython/numpy there). Reads the TRUSTED clean human target
(data/targets/tfr1_human_ecto_A.pdb, which this repo generated) + the deterministic human->mouse map
(docs/conservation.json -> human_to_mouse_122_760). Threading onto the real cryo-EM backbone (78% id,
identical fold) preserves the exact apical/conserved epitope geometry and keeps HUMAN numbering, so the
mouse model is structurally aligned to the human target by construction. Backbone is held fixed;
sidechains are repacked + minimized. The single human-only (mouse-gap) position is left unmutated.

Usage: .venv-rosetta/bin/python scripts/f02_mouse_model.py --human-pdb ... --map ... --out ...
"""
import argparse, json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human-pdb", default="data/targets/tfr1_human_ecto_A.pdb")
    ap.add_argument("--map", default="docs/conservation.json")
    ap.add_argument("--out", default="data/targets/tfr1_mouse_ecto_A.pdb")
    a = ap.parse_args()

    import pyrosetta
    from pyrosetta import pose_from_pdb, get_fa_scorefxn
    from pyrosetta.toolbox import mutate_residue
    from pyrosetta.rosetta.protocols.minimization_packing import PackRotamersMover, MinMover
    from pyrosetta.rosetta.core.pack.task import TaskFactory
    from pyrosetta.rosetta.core.pack.task.operation import RestrictToRepacking, InitializeFromCommandline
    from pyrosetta.rosetta.core.kinematics import MoveMap

    pyrosetta.init("-ignore_unrecognized_res -ignore_zero_occupancy false -mute all")
    pose = pose_from_pdb(a.human_pdb)
    pdbinfo = pose.pdb_info()
    full = json.loads(Path(a.map).read_text())["human_to_mouse_122_760"]
    sfx = get_fa_scorefxn()

    STD = set("ACDEFGHIKLMNPQRSTVWY")
    n_mut = n_skip = n_gap = 0
    for resnum_str, info in full.items():
        resnum = int(resnum_str)
        m_aa = info["mouse_aa"]
        if info["conserved"]:
            continue
        if m_aa in ("-", None) or m_aa not in STD:
            n_gap += 1
            continue
        pose_idx = pdbinfo.pdb2pose("A", resnum)
        if pose_idx == 0:
            n_skip += 1
            continue
        mutate_residue(pose, pose_idx, m_aa, pack_radius=0.0, pack_scorefxn=sfx)
        n_mut += 1
    print(f"threaded mutations applied: {n_mut}  (gap/non-std skipped: {n_gap}, unmapped: {n_skip})")

    # global sidechain repack (backbone fixed)
    tf = TaskFactory()
    tf.push_back(InitializeFromCommandline())
    tf.push_back(RestrictToRepacking())
    PackRotamersMover(sfx, tf.create_task_and_apply_taskoperations(pose)).apply(pose)

    # sidechain-only minimize (keep the cryo-EM backbone)
    mm = MoveMap(); mm.set_bb(False); mm.set_chi(True)
    minmover = MinMover(mm, sfx, "lbfgs_armijo_nonmonotone", 1e-4, True)
    minmover.apply(pose)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pose.dump_pdb(a.out)
    print(f"[wrote {a.out}]  score={sfx(pose):.1f}  nres={pose.total_residue()} (human numbering 122-760)")


if __name__ == "__main__":
    main()
