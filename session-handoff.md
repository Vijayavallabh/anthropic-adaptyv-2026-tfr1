# session-handoff

**Repo:** `/home/prachh/v/anthropic-adaptyv-2026-tfr1` — private GitHub `Vijayavallabh/anthropic-adaptyv-2026-tfr1` (`origin/main`)
**Challenge:** Anthropic × Adaptyv 2026 #4 — conditional TfR1 / CD71 binder.
**Deadline:** 2026-11-01 23:59 AoE. Track 2/3, ≤20 designs, Claude-selected (upload user-gated).

## To resume
1. `./init.sh` (uv sync + smoke gate). `./init.sh --tools` prints shared tool paths.
2. Read `AGENTS.md`, `docs/PLAN.md`, `configs/target.yaml`; check `feature_list.json` (`active`) +
   `progress.md`.
3. Continue the active feature.

## State (2026-10-24) — COMPLETE; submission ready, upload user-gated
- **Deliverable: `submissions/tfr1_track2_v6.csv`** — 20 DISTINCT backbones (one design each),
  validator PASS, Proteinbase portal novelty **20/20 PASS** (no "similar designs" flags). Prior:
  v5/v4/v3 (reused backbones for switch depth), final/v1/v2 (older).
- **Flagship #1 `d25_sw2b_A9_A25`** (l2_des_25_mpnn0 + 2 His: A9/R13 + A25/R28): dual-confirmed
  (Boltz∧Chai), cross-reactive (ratio 0.96), valid mech-B switch (swG 4–6). The one design strong on
  BOTH pH-switch (#1) and cross-reactivity (#2). Earlier "des_25 multi-His breaks Chai" was a bad His
  pair (A9+A54 fails; A9+A25 holds).
- **Pipeline F01→F11 executed** (see `progress.md`). Generators: **RFdiffusion1** (de-novo, the
  original 105-binder apical frontier) + **RFD4-Proteina** (NVIDIA; generator-diversity wave — 1924
  designs on the conserved sub-site → novel soluble cross-reactive binders beyond des_25). Sequences:
  ProteinMPNN 0-Cys (SolubleMPNN available). Validation: **pocket-restrained** Boltz-2 ∧ Chai-1
  (blind co-fold is broken here), calibrated by POS_3DS18 / NEG. Switch: mech-B buried-His.
- **Key findings:** (1) blind co-fold fails the positive control → pocket restraints mandatory;
  (2) RFD4 breaks the RFd1 cross-reactivity wall at the BINDER level, but auto buried-His switch loses
  geometry on new backbones (per-backbone His-pair search needed; only des_25 A9+A25 held);
  (3) switch magnitude is in-silico-unrankable → select mechanism diversity + direction.
- **Remaining (user-gated): upload `v6` to Proteinbase.** No further compute needed.
