# progress

**Updated:** 2026-10-20 (session cont., post-/clear)
**Active feature:** F02 — target prep

## Done
- **F00 repo + harness** (closing out) — clean uv project `adaptyv-tfr1` at the canonical path;
  `git init` + repo-local Vijayavallabh identity (global id here is wrong); `justHisPKa` salvaged;
  AGENTS.md / CLAUDE.md / init.sh / feature_list.json / target.yaml / PLAN.md / smoke test written.
  Stale raw-TNF copy moved to `../.stale-tfr1-tnfcopy-20261020`. Reference pipeline:
  `../anthropic-adaptyv-2026-tnf` (`scripts/README.md` is the manifest).
  Evidence: `./init.sh` -> INIT_EXIT=0 (uv sync 42 pkgs; compile ok; pytest now 14/14, incl. target seq = 640 aa). Recon Workflow launched (runId wf_419b8156-f71).
- **F03 submission contract** — Challenge-4 validator (`src/adaptyv_tfr1/submission.py` + `scripts/validate_submission.py`), 10 contract tests, `submissions/example_track2.csv`. molecule_class canonical = `protein` (`single_chain` accepted as a portal alias with a warning; re-verify on the live form). Evidence: pytest 14/14; validator self-check PASS.

- **F01 recon + strategy** (done) — structures byte-verified first-hand: `11QC` = human TfR1
  ectodomain (chain A, 122–760, **Gly142 already correct**, UniProt-numbered) = TARGET; `11RN` =
  TfR1(A/B)+B19V VP1u(X/Y), **TfR1 = chain A** = APICAL. Apical footprint byte-derived from 11RN
  (<5 Å to VP1u): {202,203,204,208,209,210,211,212,348,371}. Conservation deterministic
  (`scripts/conservation_epitope.py` → `docs/conservation.json`): ectodomain **78.1 %**; apical
  **3/10 conserved = {202,203,209}**, 7/10 divergent (loses R208/K371; center Y211 not conserved).
  Mouse **Q62351** = TFR1_MOUSE/Tfrc/763 aa VERIFIED. Strategy in `docs/RECON.md`: generator lead
  **RFd3 + BindCraft** (ranking inverts vs TNF), **mechanism-B** default, **JustHISpKa** primary pKa,
  3-arm portfolio (A apical / B conserved-non-apical / **C conserved-apical subsite = max-min core**),
  18 protein + 2 conditional nanobody. Corrected the "Baker 79× on TNF" memory error (real: ~1000×
  mech-A / ~10⁸× mech-B; targets EphA2/TNFR2/IL6/PCSK9). Evidence: pytest 14/14; `target.yaml` parses.

- **F02 target prep** (done) — written fresh. `data/targets/tfr1_human_ecto_A.pdb` = clean
  single-subunit full-atom human target (11QC chain A, 639 aa, Gly142, glycans stripped) = af2ig target.
  `data/targets/epitopes.json` = 3-arm hotspots: ArmA apical, ArmC conserved subset {202,203,209}, ArmB
  conserved non-apical compact cluster {694,696,704,705,706,714,717,718,725,728,729} (dimer-interface +
  Tf-site + apical-domain excluded). `data/targets/tfr1_mouse_ecto_A.pdb` = mouse (Q62351) threaded onto
  the 11QC backbone + PyRosetta repack/min (78.1% id, divergent epitope positions verified). pytest 17/17.

## In progress
- **F04 generation** — **availability reality** (`docs/TOOLS.md`, byte-audited): the recon's "RFd3 +
  BindCraft lead" is moot — RFd3/Genie3/PXDesign/af2ig installs were CLEANED; **BoltzGen is the only
  runnable generator today**. Kit SOURCE preserved at `/home/prachh/work/cache/uplifting-biomolecular-modeling`
  (1.1 GB) for rebuilds. **Smoke PASS**: BoltzGen docks binders on the conserved apical core (202/203 ~3 Å).
  **Wave-1 launched** across GPUs 1-7 (`scripts/gen_boltzgen.sh`): armC 240 (gpu1-3) / armA 140 (gpu4-5) /
  armB 140 (gpu6-7), `protein-anything`, design step, bs=2 (length diversity), kernels off.
  - **Ig-fold caveat:** `protein-anything` → ~50% VHH/Ig folds (2 Cys) + ~50% 0-Cys de-novo. Ig folds
    FAIL protein-class novelty (Ig is ubiquitous → high structural TM) → **filter: novel 0-Cys → protein
    arm; Ig → nanobody-candidate pool** (novelty judged on CDRH3, must pass ANARCI + ≥2-folder ipTM≥0.6).
    Usable protein yield ≈ half raw → generate more (`--reuse`) if short.
  - **Wave-1 triaged** (`scripts/triage_designs.py` → `runs/f04/triage.tsv`): **432 protein + 71 nanobody**
    candidates. armA 140 protein (30-95, apical, mech-A); armB 107 protein + 20 nb; armC 185 protein
    (incl. **60 large-novel >100 aa** for buried-His cores + 122 mini) + 51 nb. (armC_mini 65-95 wave
    still running on gpu4,5.) Confirms the switch-scaffold worry is moot: BoltzGen's large band is ~50%
    novel, so buried-His-capable large scaffolds ARE available — RFd3 stays conditional on F07.
  - **af2ig REBUILT + verified** (`docs/TOOLS.md`): the honest de-novo binding gate for F06. Next
    generator for lineage diversity = PXDesign (rebuild); RFd3 only if F07 needs it.

## In progress — F06 binding validation
- **af2ig status: CUDA crash FIXED, but af2_initial_guess output is UNRELIABLE on this install — DEFERRED.**
  - Fixed the GPU segfault (kit CUDA 12.9 vs this box's CUDA-13 driver → pinned venv to CUDA 12.8 +
    cudnn 9.8.0.87; `docs/TOOLS.md`). Core GPU ops now verified correct (matmul/conv/einsum/softmax, no NaN).
  - BUT the **6WRV/3DS18 positive control FAILS** (binder rmsd 6.3–6.7, pae_int 20–28, plddt_binder 73)
    and the kit's own barnase–barstar warm scores garbage (rmsd 10.8, plddt_binder 42) — af2ig RUNS
    (rc=0) but does not reproduce a known binder. Params sha256 MATCH the kit pin; inputs verified; CUDA
    ops correct ⇒ the fault is in af2_initial_guess's initial-guess application/patch, not CUDA/params/input.
    Needs deeper debug (uncertain time) — deferred, not trusted. **A gate that fails its positive control
    must not be used** (lesson: validation gates must fail loud + have a positive control).
- **PIVOT: F06 gate = Boltz-2 + Chai-1 two-folder consensus**, discriminated by (a) pose self-consistency
  (co-fold recapitulates the designed pose: binder RMSD-to-design after target-align), (b) ipSAE_min +
  iPAE, (c) 2-folder agreement — with a **6WRV positive control** and a **scrambled-sequence negative
  control** to prove the gate separates binders from the over-dock floor. Run on the 546 protein pool
  (pre-rank by triage iface, co-fold top subset first).

- **Boltz gate CALIBRATED + VALIDATED** (target MSA, binder single-seq; `scripts/{prep_boltz_inputs,run_boltz,parse_boltz}`):
  3DS18 positive control **ab_iptm 0.562 / ipae 15.0** (real-binder ceiling for single-seq-binder cofold)
  vs scrambled negatives **~0.20 / ipae ~23** (floor) — clean separation. On the top-8/arm calibration
  subset: **Arm A (apical/human) + Arm C-mini bind best** (armA_57 0.444, armC_mini_37 0.405, armA_49 0.34);
  **Arm C conserved-subsite is weak** (~0.20-0.25, near the floor) — the cross-reactive core is the hard axis.
  CAVEAT: `hot_contacts` metric is buggy (reads 0 even for the positive — chain-B numbering/offset) → not
  trusted yet; ab_iptm + ipae are the signals. Thresholds: promising ≈ ab_iptm > ~0.33 (well above the 0.20 floor).

## Next
- Precompute the target MSA once (avoid 439 server calls) → run the Boltz gate on the FULL apical pool
  (armA+armC+armC_mini = 439) + an Arm B region run → rank by ab_iptm → **Chai-1 2-folder consensus** on the
  top subset → fix hot_contacts (confirm the binder lands at the epitope, for the functional/apical claim) →
  F05 joint multi-state MPNN (cross-species rescue for the weak Arm C) → F07 switch → F08 → F09 → F10.

## Key risks / lessons carried from TNF (Challenge 2) and GLP1R (Challenge 3)
- Cross-species pH-switch transfer is NOT free (only ~5/18 TNF designs held in mouse; strength did
  not predict transfer). Apical patch loses basic residues in mouse → favour mechanism **B** (buried
  intra-binder His network) for cross-reactivity. Test mouse ENERGETICALLY.
- Switch *magnitude* is in-silico-unrankable → select for DIVERSITY; gate on switch-DIRECTION purity
  (two-state MD + PROPKA/pKAI + GFN2-xTB, contact-gated).
- af2ig positive control must be a DE-NOVO binder; ipSAE_min for cross-species robustness.
- Novelty is structural + sequence; stay far from 6WRV/3DS18, TB14, viral VP1u/GP1.
- Don't over-optimise a single in-silico metric (the selector doesn't; method novelty counts).
