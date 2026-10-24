# session-handoff

**Repo:** `/home/prachh/v/anthropic-adaptyv-2026-tfr1` — private GitHub `Vijayavallabh/anthropic-adaptyv-2026-tfr1` (`origin/main`)
**Challenge:** Anthropic × Adaptyv 2026 #4 — conditional TfR1 / CD71 binder.
**Deadline:** 2026-11-01 23:59 AoE. Track 2/3, ≤20 designs, Claude-selected (upload user-gated).

## To resume
1. `./init.sh` (uv sync + smoke gate). `./init.sh --tools` prints shared tool paths.
2. Read `AGENTS.md`, `docs/PLAN.md`, `configs/target.yaml`; check `feature_list.json` (`active`) +
   `progress.md`.
3. Continue the active feature.

## State (2026-10-24) — COMPLETE; v13 portal-verified + crowns validated; CLEARED FOR UPLOAD (user-gated)
- **Deliverable: `submissions/tfr1_track2_v13.csv`** (RECOMMENDED) + `_v13_evidence.csv` — SAME 20
  sequences as v12 (byte-identical, reordered). **All 10 CROWNS VALIDATED** by a decoy false-crown
  control + pose-contact check (see below), then the **top-10 INTERLEAVED by generator**: the 4
  non-Genie3 crowns hold PROTECTED ranks 1/3/5/7 (d25 RFd1 #1; g1_133, g7_8, g5_14 RFD4), Genie3 crowns
  at 2/4/6/8/9/10 — hedges generator-correlation wet-lab risk at the top without demoting any validated
  cross-reactive crown. Ranks 11-20 unchanged. Validator PASS (20/0/0, anarci yes).
- **PORTAL-VERIFIED 2026-10-24:** all 20 Passed, "20 included • 0 needing fixes", NO novelty / "similar
  designs" flags. The 10 sequences new since v10 (9 Genie3 crowns + g7_8) ALL cleared the authoritative
  novelty gate; portal output byte-matched v13.csv (name + rank order + seq endpoints + length, 20/20).
  **⇒ v13 is cleared for upload (upload itself remains user-gated).**
- **VALIDATION (runs/f27 + pose-contact) — why the crowns are real, not in-silico artifacts:**
  The red-team + a side-agent flagged Genie3 in-silico reliability (its lab-real TNF binders once scored
  as failures). Two decision-critical controls, both PASSED: (1) **decoy false-crown control** — 20
  de-novo binders for OTHER targets (TNF v27 + GLP1R, size-matched) folded through the exact
  pocket-restrained human+mouse metric: **25% clear human bind ≥0.30 (single-folder binding is a WEAK
  gate) but 0/20 = 0% clear the FALSE-CROWN conjunction (human ≥0.30 AND mouse ≥0.15)**; max decoy mouse
  ipSAE 0.108 < 0.15 bar < every crown's xreact_min (0.145–0.37). The mouse x-react axis is the
  discriminating filter de-novo non-binders cannot fake. (2) **pose-contact** — all 6 Genie3 crowns bury
  the conserved sub-site (UniProt 209/210 + 14/15) in BOTH species' poses. ⇒ no crown demoted.
- **(fallback) `submissions/tfr1_track2_v12.csv`** — same 20 seqs as v13, PRE-interleave ranking (top-10
  by raw x-react; 6 Genie3 at ranks 2-4/7-8-10). + `_v12_evidence.csv`.
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
