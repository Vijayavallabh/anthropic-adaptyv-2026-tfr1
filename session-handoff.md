# session-handoff

**Repo:** `/home/prachh/v/anthropic-adaptyv-2026-tfr1` — private GitHub `Vijayavallabh/anthropic-adaptyv-2026-tfr1` (`origin/main`)
**Challenge:** Anthropic × Adaptyv 2026 #4 — conditional TfR1 / CD71 binder.
**Deadline:** 2026-11-01 23:59 AoE. Track 2/3, ≤20 designs, Claude-selected (upload user-gated).

## To resume
1. `./init.sh` (uv sync + smoke gate). `./init.sh --tools` prints shared tool paths.
2. Read `AGENTS.md`, `docs/PLAN.md`, `configs/target.yaml`; check `feature_list.json` (`active`) +
   `progress.md`.
3. Continue the active feature.

## State (2026-10-24) — COMPLETE; v11 ready, upload user-gated
- **Deliverable: `submissions/tfr1_track2_v11.csv`** (RECOMMENDED) + `_v11_evidence.csv` — 20 DISTINCT
  backbones, **all valid-switch, 7 CROWNS**: d25 (0.37), Genie3 w2g6_144 (0.311), w2g5_111 (0.254),
  g1_133 (0.244), g7_8 (0.234), Genie3 w2g3_19 (0.222), g5_14 (0.185). Built by running **Genie3**
  (organizers' flat-target generator) at the conserved sub-site → 6 x-react crowns (3 switch-installed)
  + full-pool x-react screen → g7_8. 7 new seqs → portal novelty re-check (USER-GATED). v10/v7 =
  portal-verified fallbacks.
- **(fallback) `submissions/tfr1_track2_v10.csv`** (portal 20/20) + `_v10_evidence.csv` — 20 DISTINCT
  backbones, **16 switch-designs incl. 3 all-three CROWNS**: `d25_sw2b_A9_A25` (RFd1, x-react 0.37),
  `rfd4_g5_14_sw2b_A34_A50` (RFD4, 0.185), `rfd4_g1_133_sw2b_A10_A20` (RFD4, 0.244) — each robust switch
  + cross-reactive + binding, dual-folder confirmed. Standout binder-switch `rfd4_g5_120_sw2b` (bind
  0.853). Validator PASS. **Portal-verified 2026-10-24: all 20 accepted ("0 needing fixes"), every row
  Passed, no novelty flags — the 9 sequences new since v6 (re-His'd g5_14 crown + 8 pool switch-designs)
  cleared.** Ready to upload (user-gated).
- **Fallback `submissions/tfr1_track2_v7.csv`** — same 20 sequences as v6 (portal 20/20 PASS), re-ranked;
  use if skipping the portal re-check. v9 (4 new) / v8 (2 crowns) intermediate; v6 original frozen.
- **How v10 was built (runs/f17 + f18):** validated against the ORGANIZERS' EXACT JUDGE (selection
  prompt): blind co-fold vs the full ectodomain homodimer (human 121-760/mouse 123-763). FOUND the blind
  co-fold is UNRELIABLE on this target even on the exact homodimer (ipSAE≈0 and epitope drifts for
  POS_3DS18) → confirmed the pocket-restrained FRAGMENT methodology is correct. Ranked #1 switch
  (replicate-fold validated) > #2 x-react (fragment ipSAE_min, dual-folder) > #3 apical binding
  (fragment ipSAE_min), + pLDDT (all pass) + hydropathy + novelty. Screened a 1567-design pool for
  switch-installable binders (exhaustive His-pair search) → 8 new switch-designs + the 3rd crown.
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
- **Remaining (user-gated): upload `v10`** — portal novelty cleared 2026-10-24 (all 20 Passed, 0
  needing fixes). No further compute needed. (`v7` stays a fallback.) Commit is local; push user-gated.
