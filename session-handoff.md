# session-handoff

**Repo:** `/home/prachh/v/anthropic-adaptyv-2026-tfr1` — private GitHub `Vijayavallabh/anthropic-adaptyv-2026-tfr1` (`origin/main`)
**Challenge:** Anthropic × Adaptyv 2026 #4 — conditional TfR1 / CD71 binder.
**Deadline:** 2026-11-01 23:59 AoE. Track 2/3, ≤20 designs, Claude-selected (upload user-gated).

## To resume
1. `./init.sh` (uv sync + smoke gate). `./init.sh --tools` prints shared tool paths.
2. Read `AGENTS.md`, `docs/PLAN.md`, `configs/target.yaml`; check `feature_list.json` (`active`) +
   `progress.md`.
3. Continue the active feature.

## State (2026-10-27, ambition-lift) — COMPLETE; v19 RECOMMENDED (19/20 portal-verified + 1 new); validator PASS
- **DELIVERABLE STACK (upload + push USER-GATED):**
  - **`submissions/tfr1_track2_v19.csv`** (RECOMMENDED, strongest) + `_v19_evidence.csv` — v18 + ONE
    evidence-backed DESIGN upgrade: the switch-rescue winner `genie_w2g3_53__A13HR44_A31HK8` (robust mouse XR
    0.394 ± 0.007 over n=3 seeds, min 0.385 → BEATS the whole prior pool's 0.349 and the soft ~0.40 ceiling;
    GENUINE 2-in-window switch confirmed across 2 folds + sw_frac 1.00; bind 0.421; dev CLEAN; mouse pose on
    conserved 203/209; novelty 0.778 == its PORTAL-VERIFIED parent's 0.776) REPLACES `w4g1_286` (same fold)
    and ranks #1. 19/20 sequences BYTE-IDENTICAL to v17/v18; the winner is the ONLY new sequence → needs 1
    portal novelty check (fold cleared in v15 → pass expected). 19 distinct folds. validator PASS 20/0/0.
  - **`submissions/tfr1_track2_v18.csv`** (fully portal-verified fallback) + `_v18_evidence.csv` — v17's 20
    sequences, pure reorder: the one SEVERE-expression design (`w4g3_380`) demoted out of the tested top-10
    (clean `w4g5_147` promoted in). Inherits v17's 20/20 portal verification. Use for ZERO portal risk.
  - **`submissions/tfr1_track2_v17.csv`** (portal-verified 20/20) + fallbacks v16/v15/v13.
- v17 details below remain the basis for the v18/v19 sequence set. Row order = ranking.
- **v17 (the fallback basis): portal-verified 2026-10-27 (all 20 Passed, "0 needing fixes", NO novelty /
  "similar designs" flags; byte-verified submitted==validated).**
- **What changed vs v16 (the decisive finding):** v16's cross-reactivity (XR) ranking used the **MAX
  across diffusion samples** — optimistic small-n noise (e.g. old #1 w3g6_146 hit 0.397 in ONE fold of
  six; robust mean 0.19). v17 re-scored all 20 v16 + 19 Wave-4 switched crowns in **one same-pipeline
  DIFF=6 dual-folder batch** and ranks on the **robust MEAN** (score_ipsae.py means over samples; dual
  Boltz∧Chai min), which aligns with the organizers' conservative ipSAE_min+ensemble judge. Evidence in
  `runs/f35/robust/robust_xr.tsv` (n=2 V16 / n=3 W4) + `runs/f35/sel/master.tsv`.
- **v17 composition:** #1 `w3g2_70` (robust XR 0.349, std 0.001, GENUINE, BIND 0.65, portal-cleared)
  replaces w3g6_146 (→#13). **8 NEW Wave-4 distinct-fold crowns** (deep 3,200-backbone Genie3 wave
  `runs/f35`, conserved-sub-site conditioned → funnel → frozen crown screen → buried-His switch →
  robust re-screen) at ranks 3,6-11,15; they replaced 8 weak/dead-switch, non-crown, or cousin v16
  members. **All 20 GENUINE switches** (JustHisPKa, `runs/f35/sel/switch_justhispka.tsv`). **19/20
  distinct folds** (unified single-seq ESMFold + Foldseek TM<0.60, `runs/f35/sel/unified_div`; max
  achievable — remaining folds hold only novelty-failing designs). RFD4 lineage kept (#12 rfd4_g7_8,
  #14 rfd4_g5_14). Novelty-certainty tie-break front-loads portal-certain crowns in the top slots.
- **Fallbacks (all validator PASS):** `v16` (clean; the 20 portal-verified v15 seqs re-ranked by
  JustHisPKa switch) · `v15` / `v14` (FIXED 2026-10-27 — embedded-newline sequences stripped to
  byte-safe single-line) · `v13` (portal-verified 20/20) · v12/v10/v7 further back.
- **Build/scoring scripts (new this push):** `scripts/build_v17.py` (selection), `build_master_v17.py`
  (metric merge), `wave4_rescreen.sh` (DIFF=6 dual-folder re-screen, +seed), `wave4_robust.sh` (n-boot
  pool), `wave4_drive.sh` (gen→funnel→crown), `pose_subsite.py` (fragment-aware on-epitope/conserved-
  anchor check), `justhispka_switch.py` (+seqs arg). Methodology unchanged from F01→F11; the switch is
  mech-B buried-His, validation is pocket-restrained Boltz∧Chai (blind co-fold fails the positive
  control on this flat apical epitope → pocket restraints mandatory).
- **Key findings carried forward:** (1) XR is only coarsely rankable in-silico (~0.03 pipeline noise,
  larger for a few high-variance designs) — select robust MEAN + diversity, never a single lucky sample;
  (2) the ~0.40 XR "ceiling" is NOT a hard limit — the F37 switch-rescue produced a GENUINE-switch design at
  robust XR 0.394 (n=3) by relocating the buried His on the highest-XR backbone (genie_w2g3_53); it was a soft
  property of the un-rescued pool; (3) partial diffusion is a proven dud here (children inherit parent
  novelty); (4) switch magnitude is in-silico-unrankable WITHIN the genuine set (His-pKa err 2-3u >> 1.4u
  window; n_inwindow boundary-brittle) → gate genuine, then order by cross-reactivity + diversity, never
  fine-rank the switch (a switch-tier reorder was built and RETRACTED after a devil's-advocate review).
- **Remaining (user-gated):** (1) one Proteinbase novelty check on the single new v19 sequence
  (`genie_w2g3_53__A13HR44_A31HK8`; fold cleared in v15 → pass expected), then the owner's upload click —
  `v19.csv` (strongest) or `v18.csv`/`v17.csv` (fully portal-verified). (2) `git push` — this ambition-lift
  checkpoint is committed locally but NOT pushed (push user-gated; prior v17 push was 2026-10-27). No further
  compute needed.
