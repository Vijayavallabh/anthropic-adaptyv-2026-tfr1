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
- **Deliverable: `submissions/tfr1_track2_v8.csv`** (recommended) — 20 DISTINCT backbones, **TWO
  all-three crowns**: `d25_sw2b_A9_A25` (RFd1, x-react 0.37) + `rfd4_g5_14_sw2b_A34_A50` (RFD4,
  x-react 0.185) — each robust switch + cross-reactive + binding, dual-folder × dual-species confirmed.
  Validator PASS. **1 new sequence (the 2nd crown) → re-run portal novelty before upload** (local
  oracle 0.737 NOVEL = parent g5_14 which passed 20/20; low risk).
- **Fallback `submissions/tfr1_track2_v7.csv`** — same 20 sequences as v6 (portal 20/20 PASS already),
  re-ranked by the 4-fold validation; use if skipping the portal re-check. `v6` = original frozen
  fallback (portal 20/20). Prior v5/v4/v3, final/v1/v2 (older).
- **Re-ranking (runs/f17):** re-scored all 20 on a uniform 4-fold panel {Boltz-2,Chai-1}×{human,mouse},
  pocket-restrained, POS/NEG-calibrated; ranked by lexicographic #1 switch (4-fold valid) > #2 x-react
  (ipSAE_min) > #3 affinity (ipSAE_min), affinity-floor gated. ipSAE_min caught folder-dependent
  over-confidence (d386 Boltz 0.73/Chai 0.29); replicate-fold switch probability fixed single-fold
  switch noise. 2nd crown found via exhaustive mech-B His-pair search on g5_14.
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
- **Remaining (user-gated): re-run Proteinbase portal novelty on v8's 1 new crown sequence, then
  upload `v8`** (or upload `v7` directly — fully portal-verified). No further compute needed.
