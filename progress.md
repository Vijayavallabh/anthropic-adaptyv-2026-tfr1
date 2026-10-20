# progress

**Updated:** 2026-10-20 (session S203 cont., post-/clear)
**Active feature:** F01 — recon + strategy

## Done
- **F00 repo + harness** (closing out) — clean uv project `adaptyv-tfr1` at the canonical path;
  `git init` + repo-local Vijayavallabh identity (global id here is wrong); `justHisPKa` salvaged;
  AGENTS.md / CLAUDE.md / init.sh / feature_list.json / target.yaml / PLAN.md / smoke test written.
  Stale raw-TNF copy moved to `../.stale-tfr1-tnfcopy-20261020`. Reference pipeline:
  `../anthropic-adaptyv-2026-tnf` (`scripts/README.md` is the manifest).
  Evidence: `./init.sh` -> INIT_EXIT=0 (uv sync 42 pkgs; compile ok; pytest now 14/14, incl. target seq = 640 aa). Recon Workflow launched (runId wf_419b8156-f71).
- **F03 submission contract** — Challenge-4 validator (`src/adaptyv_tfr1/submission.py` + `scripts/validate_submission.py`), 10 contract tests, `submissions/example_track2.csv`. molecule_class canonical = `protein` (`single_chain` accepted as a portal alias with a warning; re-verify on the live form). Evidence: pytest 14/14; validator self-check PASS.

## In progress
- **F01 recon + strategy** — (1) verify PDB structures BY BYTES (brief prints `11QC`/`11RN`; an
  earlier scout flagged `1IQC`/`1IRN` as wrong proteins and proposed `1CX8`/`3KAS`/`6WRV`, but the
  brief distinguishes "newer UniProt-exact 11QC/11RN" from "older Ser142 1CX8/3KAS/3S9L/6WRV" — so
  the correction itself is unresolved); (2) human↔mouse apical conservation table + conserved
  basic-residue map; (3) epitope choice (apical vs conserved patch — portfolio split); (4) selection
  + novelty rubric from the published selection prompt; (5) 2026 SOTA generators for a concave
  precedented epitope + pH-switch + cross-species joint design; (6) molecule-class portfolio.
  To run as a recon Workflow; findings → `docs/` and resolve `target.yaml` VERIFY flags.

## Next
- F02 target prep · F03 submission contract (both unblocked once F01 verifies structures).

## Key risks / lessons carried from TNF (Challenge 2) and GLP1R (Challenge 3)
- Cross-species pH-switch transfer is NOT free (only ~5/18 TNF designs held in mouse; strength did
  not predict transfer). Apical patch loses basic residues in mouse → favour mechanism **B** (buried
  intra-binder His network) for cross-reactivity. Test mouse ENERGETICALLY.
- Switch *magnitude* is in-silico-unrankable → select for DIVERSITY; gate on switch-DIRECTION purity
  (two-state MD + PROPKA/pKAI + GFN2-xTB, contact-gated).
- af2ig positive control must be a DE-NOVO binder; ipSAE_min for cross-species robustness.
- Novelty is structural + sequence; stay far from 6WRV/3DS18, TB14, viral VP1u/GP1.
- Don't over-optimise a single in-silico metric (the selector doesn't; method novelty counts).
