# session-handoff

**Repo:** `/home/prachh/v/anthropic-adaptyv-2026-tfr1` — private GitHub `Vijayavallabh/anthropic-adaptyv-2026-tfr1` (`origin/main`)
**Challenge:** Anthropic × Adaptyv 2026 #4 — conditional TfR1 / CD71 binder.
**Deadline:** 2026-11-01 23:59 AoE. Track 2/3, ≤20 designs, Claude-selected (upload user-gated).

## To resume
1. `./init.sh` (uv sync + smoke gate). `./init.sh --tools` prints shared tool paths.
2. Read `AGENTS.md`, `docs/PLAN.md`, `configs/target.yaml`; check `feature_list.json` (`active`) +
   `progress.md`.
3. Continue the active feature.

## State (2026-11-01) — v25 RECOMMENDED: genuinely-varied 20/20 Tier-A (max pairwise id 26.9%), 5 genuine cross-reactive; validator PASS
- **DELIVERABLE STACK (commit only; push + upload USER-GATED):**
  - **`submissions/tfr1_track2_v25.csv`** (RECOMMENDED — 2026-11-01). **20/20 GENUINE Tier-A, genuinely varied — max pairwise identity 26.9%** (zero near-twins; under both the ~95% portal-flag line and the 94% quiet-twin bar). Built per owner "remove all the similar flagged designs and replace them with new Tier-A" + "[the latter one]" (= genuinely varied set, not just clear the flag). **Removed 5 near-twin cousins** (v24 ranks 12/13/16/18/20 — the 3 portal-flagged ≥95% pairs + the 2 quiet 94% pairs incl. the locked-#1 cousin; all M_be0). **Added 5 NEW distinct Tier-A** from a fresh Genie3 campaign (840 backbones → 11 blind-gate-passers → switch-install → re-fold n=80 human+mouse+novelty): `resc_v25g3_80_mpnn1` (**M_be6 GENUINE x-react**, H0.267/be5, MHr1.07), `resc_v25g3_49_mpnn0` (M_be2 genuine x-react), `resc_v25g6_84_mpnn1` (H0.275/be7 strongest new binder), `resc_v25g4_44_mpnn0` (be6), `resc_v25g5_109_mpnn0` (be5) — all novel, deep-epitope, spanning generation shards g3/g4/g5/g6. **Genuine cross-reactive (M_be≥2) count 3 → 5** (axis-2 upgrade). Same uniform gate (blind Protenix n=80: H_iptm≥0.194 & best_epi≥2 & ≥2-ENGINEERED-His switch [5.5,7.4] & novelty≠risk). **#1 LOCKED `genie_w2g3_53__A27HK8_A13HR44` untouched.** Ranking lexicographic switch > epitope-weighted cross-reactivity (xr_score) > affinity; genuine-x-react tier ordered by cross-reactivity robustness (M_be depth + on_epi consistency). Record (all 20 PASS): `submissions/tfr1_track2_v25_blind_protenix.tsv`. Builders (in-repo): `scripts/v25/{select_switch,assemble_v25,build_v25,gen_v25_evidence,diversity_check}.py` (reference absolute scratchpad fold-output paths from this session; logic is the record). validator **PASS 20/0/0**. (Licensed JustHISpKa binary + `.lic` gitignored — never commit.)
  - **`submissions/tfr1_track2_v24.csv`** (FALLBACK — PORTAL-VERIFIED 20/20 2026-11-01; prior recommendation). **20/20 GENUINE Tier-A, 0 fillers, 0 off-epitope, 0 sub-gate.** Uniform gate on the organizers' BLIND Protenix ruler (n=80): H_iptm ≥ 0.194 AND **best_epi ≥ 2** (apical epitope in the BEST pose — not the misleading any-pose `on_epi_rate`) AND **≥ 2-His switch** (JustHISpKa binder-alone, pKa in physiological window [5.5,7.4]) AND novelty ≠ risk. **15 distinct lineages, ≤ 2/lineage — strict cap, ZERO relaxation.** Honest Tier-A count climbed **11 → 14 → 16 → 20** over three switch-rescue rounds (`buried_switch_scan → exhaustive_switch → ESMFold → JustHISpKa → blind re-fold`); round-3 added distinct-lineage rescues `w4g1_286` (iptm **0.405**, strongest in pool) + `w4g7_217` (dual-anchor hedge) so the cap never bent. The uniform re-fold **caught + removed `w3g2_225`** (off-epitope mirage: iptm 0.217 but best_epi 0). **#1 LOCKED** = `genie_w2g3_53__A27HK8_A13HR44` (portal-verified, multi-folder, raw MH_ratio ~1.0). Ranking = lexicographic **switch > cross-reactivity > affinity**, cross-reactivity = **epitope-weighted MH_ratio→1** (raw ratio inflated by off-epitope mouse poses); top of list = genuinely mouse-on-epitope designs (`w3g0_174` mouse be7 MHr 1.04; `genie_w2g6_144_sw3b` be3; `resc_w3g5_70` be5). Full record (all 20 PASS): `submissions/tfr1_track2_v24_blind_protenix.tsv`. Builder: `scratchpad/scripts/build_v24.py`. validator **PASS 20/0/0**. **`v22` remains the portal-verified fallback.** (Licensed JustHISpKa binary + `.lic` gitignored — never commit.)
  - **`submissions/tfr1_track2_v22.csv`** (RECOMMENDED — **PORTAL-PARSED 20/20 2026-10-31**: 20 included, 0 fixes, all Passed; byte-roster-confirmed local==portal). v21 with ONE swap — the dead-switch `w3g5_249` (JustHISpKa His pKa 2.4–3.1 on two folds + a 2.9 Å His–Lys salt-bridge + blind-gate fail 0.169) → **`genie_w2g3_53__A59HK21_A17HK48`** (blind Protenix H-iptm **0.264** > flagship #1's 0.246, human on-epitope **1.00**, blind MH-ratio **0.98**, genuine switch His17 6.60 / His59 6.91, novel 0.75). JustHISpKa (field-best His-pKa predictor; user-provided binary, validated ±0.1 pKa vs 2SIC experimental) confirmed 19/20 switches genuine and flagged only `w3g5_249`; a cold devil's-advocate corrected the cross-reactivity ruler to blind Protenix (v21 has **no** weak xreact links there), so exactly ONE surgical swap survived. rows 1–19 **byte-identical** to v21; validator PASS 20/0/0. Complete uniform n=80 blind-Protenix record (same-batch POS/NEG gate): `submissions/tfr1_track2_v22_blind_protenix.tsv`; per-design axes `_v22_evidence.csv`. **`v21` remains the unchanged, portal-verified fallback.** (The licensed JustHISpKa binary + `.lic` live in the repo dir but are gitignored — never commit.)
  - **`submissions/tfr1_track2_v21.csv`** (FALLBACK — **PORTAL-VERIFIED 20/20 byte-confirmed 2026-10-28**:
    20 included, 0 fixes, all Passed; portal-parsed == v21.csv on name+order+len+head+tail; portal independently
    confirms the SAME 20-seq set as v20, reordered) — a **pure reorder** of v20
    (IDENTICAL 20 sequences; **#1 unchanged**); order multi-folder-confirmed (ESMFold2+Protenix+Boltz-blind;
    Chai-blind discarded as broken). Scored the locked finals with the organizers'
    **blind** Protenix judge (our pocket-restrained Boltz∧Chai pipeline never applied it to the exact finals).
    Calibrated on POS_3DS18/NEG (`runs/prot/controls_out`): `on_epi_rate` **invalid** (scramble on_epi 1.00 >
    positive 0.50), `iptm_max` **valid** (POS 0.271 vs NEG ~0.12). **#1 lock VINDICATED** (A27HK8_A13HR44 blind
    human 0.260 / mouse 0.243, ratio 0.93 — best both-species; beats v19 twin). v20's xr order front-loaded
    blind-weak designs (#2 w3g2_70 iptm 0.167, pocket-restraint artifact). v21 rule: human-binding GATE
    (blind iptm ≥ 0.18) above GATE_FAIL, each by validated xr_mean. `scripts/build_v21.py` +
    `_v21_evidence.csv`. validator PASS 20/0/0. Limits: n=1 POS; iptm as ipSAE proxy (no PAE dump); w3g2_70
    #2→#13 is the one judgment call (flagged). Blind-judge tables: `runs/prot/v20_judge/{human,mouse}.tsv`.
  - **`submissions/tfr1_track2_v20.csv`** (PORTAL-VERIFIED fallback — validated pocket-restrained-pipeline order;
    #1 LOCKED 3-0; 20/20 Passed) — v19 with **only the rank-1 swapped** to the
    His-placement twin `genie_w2g3_53__A27HK8_A13HR44`. A devil's-advocate found the earlier cross-reactivity
    "ratio" was computed incoherently as `min(mouse-over-folders)/min(human-over-folders)` (numerator and
    denominator from different folders → faked a near-1 for the old #1). The correct WITHIN-folder ratio
    (robust across 3 folds × 2 folders) makes `A27HK8_A13HR44` the most cross-reactive (|ratio−1| 0.12 vs 0.38,
    by balancing species, not an affinity bump). On the ranked objectives it weakly dominates: #1 switch TIE
    (both GENUINE 2-in-window; not finely rankable), #2 cross-react challenger wins robustly, #3 affinity
    challenger ≥. Dev CLEAN (0-Cys, net charge −0.05); novelty 0.777. A **unanimous 3-0 independent
    adjudication LOCKED the rank-1** (ending a 3× flip). **v20 PORTAL-VERIFIED 20/20 (2026-10-28: 20 included,
    0 fixes, every row Passed incl. the new rank-1; byte-verified submitted==validated).** The other 19 designs
    are byte-identical in content to v19. validator PASS 20/0/0. **DO NOT re-open the rank-1 on in-silico
    grounds** (re-fold/seed/pKa-rerun/switch-reread/min-min recompute); re-open only on portal rejection
    (→ fall back to v19) or new wet-lab data.
  - **`submissions/tfr1_track2_v19.csv`** (PORTAL-VERIFIED fallback) + `_v19_evidence.csv` — the prior
    deliverable (former rank-1 `genie_w2g3_53__A13HR44_A31HK8`, switch-rescue winner, robust mouse XR 0.394
    n=3); retained intact as the zero-rework fallback.
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
- **Remaining (user-gated):** the owner's upload click — **`v21.csv`** (RECOMMENDED; organizers'-blind-judge
  order; pure reorder of the portal-verified set → ~zero portal risk) **or** `v20.csv` (zero-risk portal-verified
  fallback, validated-pipeline order) or `v19`/`v18`/`v17`. **All session work pushed to origin/main 2026-10-28**
  (owner-authorized). **#1 slot unchanged and vindicated** on the organizers' judge; the v21 vs v20 choice is the
  ranking-philosophy call (organizers' blind judge vs our validated pocket-restrained pipeline), decided at upload.
  Both are portal-verified 20/20, so v21 (better-ranked) is the recommendation.
