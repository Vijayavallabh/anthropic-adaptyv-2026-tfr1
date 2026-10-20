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
- **F04 generation** — re-rank generators on the concave apical pocket (do NOT inherit TNF). Lead
  **RFdiffusion3 + BindCraft**; proven arms PXDesign/Genie3; re-test RFd3/BoltzGen; SeedProteo for
  novelty-max. Generate backbones at the 3 epitope sets (ArmA apical, ArmC conserved subsite, ArmB
  conserved non-apical). Port the reusable drivers (`gen_rfd3_tnf.sh`, `gen_boltzgen_tnf.sh`) — FIX the
  ~100 TNF absolute-root hardcodes + add a repo-root assert. Queue across the 8× H100 idle GPUs.

## Next
- F05 sequence (ProteinMPNN; joint multi-state h+m for Arm B/C) → F06 binding (3-folder consensus).

## Key risks / lessons carried from TNF (Challenge 2) and GLP1R (Challenge 3)
- Cross-species pH-switch transfer is NOT free (only ~5/18 TNF designs held in mouse; strength did
  not predict transfer). Apical patch loses basic residues in mouse → favour mechanism **B** (buried
  intra-binder His network) for cross-reactivity. Test mouse ENERGETICALLY.
- Switch *magnitude* is in-silico-unrankable → select for DIVERSITY; gate on switch-DIRECTION purity
  (two-state MD + PROPKA/pKAI + GFN2-xTB, contact-gated).
- af2ig positive control must be a DE-NOVO binder; ipSAE_min for cross-species robustness.
- Novelty is structural + sequence; stay far from 6WRV/3DS18, TB14, viral VP1u/GP1.
- Don't over-optimise a single in-silico metric (the selector doesn't; method novelty counts).
