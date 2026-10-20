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

## In progress
- **F02 target prep** — write FRESH (TNF `stage0_target_prep.py` is stale EGFR). (1) From `11QC.cif`
  emit a clean human apical TARGET PDB (single subunit, chain A, Gly142 — already correct) + a
  full-atom single-subunit af2ig target; (2) define apical/conserved-apical-subsite/conserved-non-apical
  epitope hotspot sets from `docs/conservation.json`; (3) build the mouse (Q62351, 123–763) model and
  align; (4) numbering asserts (640-aa window 121–760, UniProt 211 == Y). Fix the ~100 TNF absolute-root
  hardcodes on any ported script + add a repo-root assert.

## Next
- F04 generation (unblocked once F02 emits targets + hotspots).

## Key risks / lessons carried from TNF (Challenge 2) and GLP1R (Challenge 3)
- Cross-species pH-switch transfer is NOT free (only ~5/18 TNF designs held in mouse; strength did
  not predict transfer). Apical patch loses basic residues in mouse → favour mechanism **B** (buried
  intra-binder His network) for cross-reactivity. Test mouse ENERGETICALLY.
- Switch *magnitude* is in-silico-unrankable → select for DIVERSITY; gate on switch-DIRECTION purity
  (two-state MD + PROPKA/pKAI + GFN2-xTB, contact-gated).
- af2ig positive control must be a DE-NOVO binder; ipSAE_min for cross-species robustness.
- Novelty is structural + sequence; stay far from 6WRV/3DS18, TB14, viral VP1u/GP1.
- Don't over-optimise a single in-silico metric (the selector doesn't; method novelty counts).
