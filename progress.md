# progress

**Updated:** 2026-11-01 (**v25 PORTAL-VERIFIED** — 20 included, 0 needing fixes, all 20 Passed, **ZERO "Similar designs in this upload" flags** [v24 had 3]; byte-matched to committed; genuinely-varied 20, max pairwise identity 26.9%; validator PASS 20/0/0)
**Active feature:** DELIVERABLE = **v25** (`submissions/tfr1_track2_v25.csv`) — **20/20 GENUINE Tier-A, genuinely varied** (max pairwise identity **26.9%** — zero near-twins; well under the ~95% portal-flag line AND the 94% quiet-twin bar). Built per owner directive "remove all the similar flagged designs and replace them with new Tier-A" + "[the latter one]" (= aim for a genuinely varied set, not just clearing the portal flag). **Removed 5 near-twin cousins** (v24 ranks 12/13/16/18/20: the 3 portal-flagged `genie_w2g6_144`#2 / `resc_w4g1_195`#2 / `resc_w4g0_194`#2 PLUS the 2 quiet 94% pairs `genie_w2g3_53`#2 / `resc_w4g1_286`#2; all were M_be0 lower-value members). **Added 5 NEW distinct Tier-A** from a fresh Genie3 campaign (840 backbones → 11 blind-gate-passers → switch-install → re-fold): `resc_v25g3_80` (M_be6 genuine x-react!), `resc_v25g3_49` (M_be2 genuine x-react), `resc_v25g6_84` (H 0.275/be7, strongest new binder), `resc_v25g4_44` (be6), `resc_v25g5_109` (be5) — spanning all 4 generation shards. Same uniform gate on the organizers' BLIND Protenix ruler (n=80): H_iptm ≥ 0.194 AND best_epi ≥ 2 AND ≥ 2-ENGINEERED-His switch (JustHISpKa [5.5,7.4]) AND novelty ≠ risk. #1 LOCKED = `genie_w2g3_53__A27HK8_A13HR44` (untouched). **Genuine cross-reactive (M_be≥2) count 3 → 5** (axis-2 upgrade). Ranking lexicographic switch > epitope-weighted-cross-reactivity (xr_score) > affinity. Record: `submissions/tfr1_track2_v25_blind_protenix.tsv` (all 20 PASS). validator PASS 20/0/0. **v24 = prior PORTAL-VERIFIED fallback** (unchanged, in history at `8a7bf48`). Push + Proteinbase upload USER-GATED. See the 2026-11-01 v25 entry below.

## 2026-11-01 — v25: genuinely-varied 20 (remove 5 near-twins, add 5 NEW distinct Tier-A)
- **Owner directive:** "remove all the similar flagged designs and replace them with new designs of tier A" → chose "Generate 2 new (full campaign)" → then (side-agent note: 2 MORE 94% pairs survive beyond the 3 portal-flagged) replied "[the latter one]" = aim for a **genuinely varied set of 20**, not just clear the portal flag.
- **Scope:** break all 5 near-twin pairs, not 3. Removed v24 ranks **12/13/16/18/20**: 3 portal-flagged cousins (`genie_w2g6_144`#2, `resc_w4g1_195`#2, `resc_w4g0_194`#2, ≥95% id) + 2 quiet 94% pairs (`genie_w2g3_53`#2 [cousin of locked #1], `resc_w4g1_286`#2). All 5 were M_be0 lower-value members; locked #1 untouched.
- **Fresh Genie3 campaign** (conserved apical sub-site bias): 840 backbones → CA-MPNN (0-Cys) → ESMFold sc + foldseek novelty → Boltz pocket pre-filter → **BLIND-Protenix gate n=80** → 11 confirmed gate-passers (10 distinct backbones; strongest `v25g6_84` iptm 0.480/be7 pre-switch, beats the entire prior pool).
- **Switch-install** on all 11 (buried-cation scan → exhaustive separated-His → ESMFold monomer → JustHISpKa): all 11 yielded a combo with **2 ENGINEERED His in [5.5,7.4]** (Baker separated-cation geometry, `n_intro_in=2`).
- **Re-fold n=80 (human+mouse) + novelty** of the 11 switch combos: **10/11 retain Tier-A binding** (H_iptm≥0.194 & best_epi≥2 survive the His muts); all 11 novelty ≠ risk (9 novel, 2 borderline).
- **2 NEW GENUINE cross-reactive** (mouse best_epi≥2, on-epitope): `resc_v25g3_80_mpnn1` **M_be6** (H 0.267/be5, MHr 1.07, on_epi 1.00 — rock-solid, comparable to the roster's best) and `resc_v25g3_49_mpnn0` **M_be2** (H 0.205/be6, MHr 1.04, on_epi 0.40 — marginal). **Genuine x-react count 3 → 5.** Rest M_be0 (expected blind-mouse drift; their high MHr is the off-epitope mirage — NOT ranked on it).
- **5 picks** (all from the one campaign, all novel, deep-epitope be5–7, spanning shards g3/g4/g5/g6): x-react `v25g3_80`(r3), `v25g3_49`(r6); strong binder `v25g6_84_mpnn1` H0.275/be7 (r13); `v25g4_44` be6 (r19), `v25g5_109` be5 (r20). Dropped the earlier "ready" `genie_w1g0_112_sw2b` (borderline nov 0.874, weak) in favor of stronger same-ruler campaign designs.
- **Ranking:** #1 LOCKED. Genuine-x-react tier (ranks 2–6) by cross-reactivity ROBUSTNESS (M_be depth + on_epi consistency, not just ratio): proven `w3g0_174`(M7) r2, new `v25g3_80`(M6) r3, proven `genie_w2g6_144`(M3) r4 / `resc_w3g5_70`(M5) r5, marginal new `v25g3_49`(M2) r6. M1 tier r7–12 (retained, unchanged). M0 tier r13–20 by affinity (xr illusory for M_be0). Retained relative order preserved throughout.
- **Diversity proven:** `scratchpad/scripts/diversity_check.py` + build-time check — max pairwise identity among all 20 = **26.9%** (`resc_w4g7_217` ↔ `w3g5_231`); zero pairs ≥90%, let alone the 94%/95% bars. All 5 new ≤22.9% vs retained roster.
- validator PASS 20/0/0; CRLF; class=protein. Record: `submissions/tfr1_track2_v25_blind_protenix.tsv` (all 20 PASS). **v24 remains the portal-verified fallback.** Committed LOCAL `c26090a`.
- **PORTAL-VERIFIED 2026-11-01** (owner pasted Proteinbase parse): **20 parsed, 20 included, 0 needing fixes, all 20 rows Passed, and ZERO "Similar designs in this upload" flags** (v24 carried 3 such flags on its cousin-pairs — v25 removes all near-twins). Byte-matched: committed v25 == portal parse on name+order+len+head+tail for all 20 (`scratchpad/scripts/` byte-check). The "[the latter one]" genuinely-varied goal is confirmed by the portal itself.
- **Adversarial pre-upload review (4-agent workflow, ultracode) → VERDICT: ship-as-is.** Three independent lenses (ranking optimality / regression-vs-v24 / new-design validity) + a completeness synthesizer, all findings verified against the raw fold/pKa/novelty files. **Zero blocking issues.** The one MAJOR finding — rank-6 `resc_v25g3_49` carries the table-high xr_score 0.961 yet sits at the genuine-CR tier bottom — was adjudicated **keep rank 6**: its xr is a near-floor artifact (both iptm barely clear the 0.194 gate; M_be=2 at threshold; mouse on_epi_rate 0.40 → 60% poses off-epitope), so promoting the most gate-marginal binder over three stronger genuine cross-reactives would risk score if the blind ruler re-samples (one residue → M_be1 collapses xr 0.96→0.48). Anti-mirage, consistent with the project's methodology. Completeness critic independently verified (all clean): name↔seq↔pKa consistency on all 5 new (named engineered-His are genuine His with in-window pKas in the submitted seq), submission-wide novelty (all 20 ≠ risk), correct g6_84 variant submitted (mpnn1 0.275 gate-passing, not mpnn0 0.1845), molecule_class=protein OK for this challenge. No changes to v25.
- USER-GATED next: push + Proteinbase upload.

## 2026-11-01 — v24: remove ALL Tier-B/C, replace with genuine Tier-A (owner: "at all drastic costs")
- Owner directive: "Remove all the Tier B and Tier C designs to replace them with new designs that would be in Tier A."
- **Honest re-audit on the uniform blind-Protenix ruler** (same n=80 regime as the judge): the correct on-epitope gate is **best_epi** (apical residues buried in the BEST/highest-iptm pose — what the judge's iptm reflects), NOT `on_epi_rate` (any grazing pose; scrambles score 0.6–0.9). Re-gating dropped the honest Tier-A count to 11, then rebuilt up.
- **Switch-rescue pipeline** (3 rounds): on-epitope binders with fragile switches → `buried_switch_scan` (buried cations near interface) → `exhaustive_switch` (2–3 His each near a DISTINCT cation = Baker separated-His SOTA) → `esmfold_monomer` (binder-alone) → JustHISpKa (count in physiological window [5.5,7.4]) → filter ≥2 → **blind-Protenix re-fold (human+mouse)** to confirm binding + best_epi ≥ 2 survive the His muts.
  - R1 (11→14): resc_w3g5_70, resc_w4g1_195, resc_w4g0_194. R2 (14→16): resc_genie_w2g5_111, resc_e223_m3 (w4g7_217 R2 variants broke — off-epitope/sub-gate). R3 (16→20): **distinct-lineage** resc_w4g1_286 (H 0.405, strongest in pool) + resc_w4g7_217 (A19 dual-anchor hedge; A48 anchor broke the pose), + within-cap 2nd cousins resc_w4g1_286#2 / resc_w4g0_194#2.
- **Uniform re-fold of the 8 original Tier-A** (same pipeline, for genuine cross-reactivity ranking) **caught `w3g2_225` off-epitope** (iptm 0.217, best_epi 0) → removed, replaced by resc_w4g1_195__A18HK22 (keeps cap ≤ 2).
- **Diversity cap resolved WITHOUT relaxation:** round-3 distinct-lineage rescues meant 20 genuine Tier-A fit across 15 lineages at ≤ 2 each — no genie_w2g6_144 over-stacking. The cap decision the side-agent flagged became moot.
- **Novelty** re-checked (`novelty_struct.py`) on all new rescues: all novel/borderline, none "risk".
- **Ranking:** #1 LOCKED (portal pedigree + raw MH_ratio ~1.0). Cross-reactivity read as epitope-weighted MH_ratio→1 — raw ratio→1 is gameable and inflated by off-epitope mouse poses (most designs' mouse drifts off-epitope on the blind fold, per lesson-tfr1-apical-blind-cofold-fails-poscontrol). Genuinely mouse-on-epitope designs (be≥2) front-loaded.
- validator PASS 20/0/0; CRLF; 20 unique names + seqs; class=protein. USER-GATED next: push + Proteinbase upload.

### 2026-11-01 (verification) — axis-2 (cross-reactivity) PROVEN optimal; candidate pool CLOSED
Responding to a side-agent flag that a high mouse score can be off-epitope (fake x-react), re-verified the whole pool by bytes (`scratchpad/scripts/screen_xr.py`, `mouse_gap.py`):
- **e223 flag neutralized by design:** `resc_e223_m3` has M_iptm 0.275 > H_iptm 0.241 (raw ratio 1.139 — looks ideal) but M_be=0 → epitope-weighting demotes xr_score to 0.215 → sits at **rank 14**, not near the top. The ranking is NOT built on fake x-react.
- **3/3 captured:** of 54 designs folded in both species (32 pass H gate), **exactly 3** have genuine mouse-on-epitope binding (M_be≥2): `w3g0_174` (be7), `resc_w3g5_70` (be5), `genie_w2g6_144_sw3b` (be3) — ALL already in roster at ranks 2,3,4. Zero genuine x-react designs left out.
- **No cheap gap:** 0 H-gate-passing designs lack a mouse fold (nothing more to check for free).
- **Reservoir closed:** 127 never-folded seqs = ~120 His-combo cousins of existing roster lineages (same backbone ⇒ same mouse grip, lineage-capped, anti-diversity) + 14 distinct new backbones = 3 controls (NEG/POS) + 7 Complexa/RFd4 (host-specific/binding-dead; sibling `cx_armA_deep_01` folded at H 0.158 sub-gate) + `w3g0_290` (known human-specific, ratio~0.01) + `w3g5_249` (confirmed dead switch). **None plausibly a new genuine x-react Tier-A.**
- **Conclusion:** the 3-genuine ceiling is a single-species-GENERATION limit (not a screening gap); breaking it needs multi-day joint multi-species design, infeasible+unvalidatable before deadline. v24 is optimal on axis #2 given the pool. **No further compute warranted** (more folding = ceiling-bound theater). Deliverable unchanged.

### 2026-11-01 (portal) — v24 PORTAL-VERIFIED; "similar in upload" flags investigated → ship v24 as-is
- **Owner pasted the Proteinbase portal parse of v24: 20 parsed, 20 included, 0 needing fixes, ALL 20 rows "Passed."** v24 is now PORTAL-VERIFIED (matches the v20/v21/v22 de-risking). Cleared for upload on owner's go.
- Portal flagged **"Similar designs in this upload"** on 3 cousin-pairs: genie_w2g6_144 (ranks 3+13), resc_w4g1_195 (8+16), resc_w4g0_194 (10+18) — **informational, all still Passed.** Expected: only 15 distinct lineages have genuine Tier-A members, so 5 within-cap 2nd-cousins were needed to reach 20/20 Tier-A.
- **Calibrated the portal similarity threshold** (`scratchpad/scripts/simcheck.py`): flagged pairs = 97.1–97.8% id; un-flagged cousin pairs (genie_w2g3_53, w4g1_286) = 94.1–94.3% → threshold ≈95–96%.
- **Investigated reducing redundancy** with 2 distinct-lineage candidates (both completely distinct, ≤15.5% id vs roster → would NOT re-flag): validated switch (JustHISpKa binder-alone) + novelty (`scratchpad/scripts/swap_validate.sh`):
  - `w4g5_147_mpnn0_sw2his` — **DEAD SWITCH** (His30 pKa 7.872, His38 8.824, both >7.4 window) → NOT Tier-A. ✗
  - `genie_w1g0_112_sw2b` — full Tier-A (His22 5.947 / His31 6.042 in-window; novelty 0.874 borderline; H 0.213, M_be1). ✓ but only a **single** swap possible (3→2 flags), and it inserts a borderline-novelty/weaker-binder into the top-10 on an M_be1-vs-M_be0 distinction that is within blind-mouse-fold noise.
- **Decision: SHIP v24 AS-IS.** The lone available swap is a noise-driven marginal change that would forfeit the portal verification for no robust axis gain; v24 already honors the ≤2/lineage cap. "Confirm, don't churn." Push + Proteinbase upload USER-GATED.

## 2026-10-27 — v15 "best-20" compute push (owner-authorized: replace v13's weak members) — **PORTAL-VERIFIED 20/20, byte-confirmed 2026-10-28**: 20 included, 0 fixes, every row Passed; portal-parsed == v21.csv on name+order+len+head+tail, and the portal independently confirms it is the SAME 20-sequence set as v20, reordered). v21 = v20 pure-reordered by the organizers' blind Protenix judge (calibrated POS/NEG); #1 UNCHANGED = genie_w2g3_53__A27HK8_A13HR44, vindicated (best both-species, ratio 0.93). Order multi-folder-confirmed (ESMFold2 foldability all-pass + Protenix sensitive ranker + Boltz-blind confirms the robust subset; Chai-blind discarded as broken). validator PASS 20/0/0. **v20** = portal-verified fallback. ONLY the owner's upload click remains USER-GATED. See the 2026-10-28 entries at the end of this log.

## 2026-10-27 — v15 "best-20" compute push (owner-authorized: replace v13's weak members)
- Fresh Genie3 wave (2,400 backbones, conserved-sub-site conditioned, seeds 21000) → funnel → 2,735
  self-consistent+novel → crown-screened two tiers (top 400 + next 1,200 of the pool) → ~47 bind+xr crowns.
- NEW lossless 2-stage crown screen (`scripts/crown_screen_2stage.sh`): Boltz necessary-condition filter on
  all candidates, Chai only on survivors — same verdict as full 4-fold crown_val, far less Chai. (Red-team
  found 2 latent false-negative bugs; verified ZERO exposure on the actual runs; fixed for robustness.)
- Switch install: greedy (`install_switch.sh`) + exhaustive His-pair rescue (`exhaustive_switch.py`) on the
  highest-XR backbones. switch genuineness via `scripts/switch_prob_chai.py` (Chai/CIF, Baker floor frac≥2).
- Robustness (Prong C): re-fold the crown pool at DIFF_SAMPLES=6 (6-Boltz-sample mean) — single-fold XR/bind
  proved noisy (v13 d25 bind 0.407→0.014; wave-3 XR ±0.19). Switch frac is stable across runs.
- Novelty: `novelty_struct.py` max-TM gate (portal-calibrated 0.89 = L3/L2 boundary). Caught that the funnel's
  covwTM<0.80 gate let non-novel designs through (w3g1_43/139 max-TM 0.92/0.95 → excluded).
- Result: **v15** = 15 genuine robust-switch novel crowns + 5 completing (2 weak-switch crowns + 3 RFD4/RFd1
  hedges). validate --track2 PASS. Flagship w3g6_146 XR 0.397. v14 (14 crowns+6 hedges) + v13 are fallbacks.
- Research workflow verdict: no better generator for this flat-apical target (PXDesign/BoltzGen/BindCraft
  wall; Genie3 is the one that crowns); Odin-Multi (multi-state co-design) documented as an optional future
  x-react lever (not pursued — 2–4 d setup, new backbones still face the switch gate).
- USER-GATED next: Proteinbase novelty re-check (watch borderline rows) → upload → push.

## (historical, 2026-10-20)

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

## F06 CRITICAL FINDINGS (2026-10-20)
- **Full Boltz run (439+controls) is NOT trustworthy alone — generator/scorer circularity.** BoltzGen is
  built on Boltz-2, so Boltz-2 over-validates BoltzGen's own designs (hundreds at ab_iptm 0.8-0.92) while
  the INDEPENDENT 3DS18 binder scored 0.276 (below the design median 0.427). Target MSA was consistent
  (6518 seqs everywhere), so it's not MSA; it's shared inductive bias + single-sample diffusion noise.
  ⇒ Boltz ipTM alone cannot rank these designs.
- **3DS18 is a WEAK positive control for single-seq cofold** (β-sheet-EXTENSION topology; both Boltz 0.28
  and Chai 0.20 score it low — these binders are intrinsically hard without the binder's own MSA). The
  reliable calibrator is the SCRAMBLED NEGATIVE floor (~0.15-0.19); look for designs that clear it in the
  INDEPENDENT folder.
- **Running Chai-1 (independent architecture) as the honest gate** on top-40/arm by Boltz (124 + controls).
  Decision rule: real candidates must clear the scrambled floor in CHAI (not just Boltz) and ideally in both.

## F06 RESULT: 13 binders pass the independent 2-folder gate (runs/f06/f06_pass.tsv)
- Chai (independent of BoltzGen) SEPARATES a real tail: scramble floor ~0.16, weak 3DS18 positive 0.20,
  but top designs reach Chai **0.40-0.672**. **F06-PASS gate = Chai≥0.35 ∧ Boltz≥0.5 → 13 designs**:
  armC_mini 6, armC 3, armA 4; 12 mini (40-100) + 1 micro. Top: armC_mini gpu4_21 (chai 0.672/boltz 0.811/68aa),
  armC gpu2_31 (0.569/0.806/59aa), armC gpu2_18 (0.505/0.831/85aa), armC_mini gpu5_17 (0.475), armA gpu4_05 (0.466).
- **The cross-reactive core (Arm C) HAS real binders** (3) — the hard axis is reachable. All F06-pass are
  mini → buried-His (mechanism B) feasible.

## F07 feasibility (buried_switch_scan on the 13 F06-pass)
- **6/13 can host a buried-His mechanism-B switch** (His next to a buried binder cation → low-pH repulsion
  → release; variants in runs/f07/switchscan/): armC gpu2_18 (12 positions), armC gpu2_31 (9),
  armC_mini gpu5_12 (11), armC_mini gpu4_22 (7), armC_mini gpu4_21 (5), armA gpu4_05 (2). The other 7 lack
  buried cation anchors (would need a de-novo His-His/His-polar HBNet — harder). The top cross-reactive
  (armC) + armC_mini binders ARE switch-installable — good alignment of binding + switch.
- Next: combine 2-3 separated buried positions → multi-His switched sequences → re-fold (Boltz+Chai, confirm
  binding retained @pH7.4) → JustHISpKa in-window + PROPKA/pKAI sign + GFN2-xTB + two-state MD direction,
  contact-gated. Select for switch-mechanism DIVERSITY (magnitude is in-silico-unrankable).

## Next (F07+ on the 13 F06-pass, + expand)
- F07 pH-switch: install buried-His (mech B) on the 13 (esp. the Arm C cross-react core + Arm A apical) →
  validate direction/selectivity (JustHISpKa + PROPKA/pKAI + GFN2-xTB + two-state MD, contact-gated) on the
  EXACT sequence; re-fold. F08 mouse cross-species (energetic) on Arm C. F09 novelty (structural TM vs
  6WRV/TB14/PDB) + developability. F10 select ≤20 (relax gate to ~Chai≥0.30 / run Arm B region / more pool
  through Chai if more candidates needed). Fix hot_contacts (epitope landing) to support the apical/functional claim.

## Key risks / lessons carried from TNF (Challenge 2) and GLP1R (Challenge 3)
- Cross-species pH-switch transfer is NOT free (only ~5/18 TNF designs held in mouse; strength did
  not predict transfer). Apical patch loses basic residues in mouse → favour mechanism **B** (buried
  intra-binder His network) for cross-reactivity. Test mouse ENERGETICALLY.
- Switch *magnitude* is in-silico-unrankable → select for DIVERSITY; gate on switch-DIRECTION purity
  (two-state MD + PROPKA/pKAI + GFN2-xTB, contact-gated).
- af2ig positive control must be a DE-NOVO binder; ipSAE_min for cross-species robustness.
- Novelty is structural + sequence; stay far from 6WRV/3DS18, TB14, viral VP1u/GP1.
- Don't over-optimise a single in-silico metric (the selector doesn't; method novelty counts).

## F07 multi-His build + F09 developability + novelty tooling (2026-10-20 late)
**F07 switch build** (`scripts/build_multihis.py`): 6 switched seqs from 4 of the 6 switch-viable designs —
gpu2_18 (sw2his A10H/K14+A15H/K64; sw3his +A49H/K53), gpu2_31 (sw2his A18H/K10+A30H/R59), gpu4_22
(sw2his A23H/K27+A30H/K65), gpu5_12 (sw2his A13H/R17+A49H/K89; sw3his +A75H/K78). Each His sits near a
DISTINCT buried cation (Lys **or Arg** — fixed a bug that dropped Arg anchors), pairwise Cβ>8Å so they
titrate additively, not anti-cooperatively. gpu4_21 (TOP binder, Chai 0.672) + gpu4_05 CANNOT host a clean
multi-His switch (K31/R32 adjacent; single R24) → they stay **plain** high-affinity binders. This is the
expected pool-thinning: the final 20 will MIX switch-binders + plain binders (not 20 acing every axis).
- Binding-retention re-fold (Chai, GPU0, bs1usp2au) launched on the 6 switched seqs vs apical receptor;
  keep only those whose Chai stays ≥ gate (parent Chai: gpu2_18 0.505, gpu2_31 0.569, gpu4_22 0.376, gpu5_12 0.407).

**F09 developability** (`scripts/developability_scan.py`, 13 parents + 6 switched → results/developability_dev_input.csv):
- Switch mutations IMPROVE developability — His lowers GRAVY (gpu5_12 +0.153→+0.03; gpu2_31 +0.76→+0.53;
  gpu4_22 +0.39→+0.26). Switch helps solubility.
- 4 expression-SEVERE (charge-blob/low-complexity, GRAVY>+0.9): gpu5_26, gpu5_34, gpu1_14, gpu4_28 → deprioritize.
- Unpaired Cys: gpu2_31, gpu5_34 (scrambling risk → C→S in final seq; gpu2_31 is a good switch-binder).
- Cleanest: gpu2_18 (LIAB 2), armA gpu4_33/35/05, gpu4_22.

**Novelty tooling** (de-risk the HARD ≥3/4 gate): foldseek installed (tools/foldseek, static binary) + PDB DB
downloading (b8d54a6ys); ESMFold2 env `.venv-esmfold2` available (single-seq fold); TMalign works. AFDB skipped
(disk 729G free, AFDB too large) — helical de-novo bundles cap at 3/4 anyway (passes), key check is vs PDB.

**Pool expansion**: Chai-expand on 317 remaining apical designs (bzduk45hg) running → when done, re-run
buried_switch_scan + build_multihis on the FULL F06-pass set (avoid rework on a partial pool).

## F07 switch re-fold RESULT + F08 mouse prep + F09 diversity (2026-10-20 late)
**Switch binding-retention re-fold** (Chai, paired vs parent iptm): switch-install is LOW-YIELD on retrofit —
| design | parent iptm | switched iptm | verdict |
|---|---|---|---|
| armC_mini gpu5_12 sw2his | 0.407 | **0.491** | ✓ survives & IMPROVES (95aa, largest) |
| armC gpu2_18 sw3his | 0.505 | 0.312 | marginal |
| armC gpu2_31 sw2his | 0.569 | 0.300 | fail |
| armC gpu2_18 sw2his | 0.505 | 0.190 | broke |
| armC_mini gpu4_22 sw2his | 0.376 | 0.170 | broke |
Root cause of breakage: burying His deletes a core hydrophobic -> fold destabilizes (not an interface clash;
positions were >9Å from the interface). The one clean win is the LARGEST binder (more core to absorb His).
- Fix 1 (`build_multihis.py`): interface-distance filter (His only >9Å from target contact).
- Fix 2 (`mpnn_switch_repair.py`): install His -> ProteinMPNN repacks the CORE around them, FIXING target +
  interface contacts + His sites (canonical Baker install). Test on gpu2_18_sw3his / gpu2_31_sw2his: His
  retained, 55/85 (resp. core) positions redesigned -> re-fold pending (bc46c2iq0). Rescue decision test-first.

**F09 fold diversity** (foldseek all-vs-all, TM≥0.6): 13 binders -> 6 clusters, but 8/13 share ONE fold
(cluster 1: gpu4_21,gpu2_18,gpu5_34,gpu5_12,gpu1_14,gpu4_33,gpu4_28,gpu4_22 — helical bundles). Selection caps
this lineage (~2 best: gpu4_21 top-affinity + gpu5_12 switch) + keeps the 5 singletons. SEVERE-dev members
(gpu5_34,gpu1_14,gpu4_28) drop from cluster 1 naturally.

**F08 mouse cross-species prep**: mouse apical receptor `data/targets/mouse_apical_189_383.seq` (human 189-383
equiv from threaded mouse ecto; 75.4% id to human apical — more divergent than 78% ecto-wide). Co-fold ready.

**Strategy (honest)**: switch yield is low on retrofit -> rely on (a) expanded pool (more + larger parents),
(b) MPNN core-repair (if the test rescues binding), (c) prioritize large binders. Final 20 = MIX of
switch-binders + strong plain binders (gpu4_21 etc.), as the switch step thins its own pool.

## F07 SOTA pivot: mechanism A (interface His-cation) — 2026-10-20 late
Consensus/lit search surfaced Ahn/Baker 2025 "Computational design of pH-sensitive binders" (bioRxiv
2025.09.29): TWO methods — (i) interface His adjacent to a TARGET cation (repel at low pH, weakens
INTERFACE) and (ii) buried His core networks (destabilize fold). Buried-His designs ([Goldbach 2023],
[Shen 2024]) are built DE-NOVO with the network designed in — hence my mech-B retrofit yield is low.
- **MPNN core-repair = DEAD END**: re-fold of repaired gpu2_18/gpu2_31 got WORSE (0.31→0.22, 0.30→0.28).
  Dropped. (Redesigning core changes the binder; confirms af2-binding-is-sequence-specific.)
- **Mech A is the gentle, high-yield retrofit** (`scripts/mech_a_scan.py`): apical epitope HAS target
  cations (R208,K344,K371,K374 + more). 18 interface-His point-mutant seqs from 11/13 designs; re-fold
  vs apical domain running (bhmf2we3p) to confirm pH7.4 binding kept. Mech A for HUMAN objective #1;
  mech B (conserved cation / large binder) reserved for x-species.
- Note: `runs/f07/complexes` are full-ecto GENERATION poses; `runs/f07/complexes_apical` are the VALIDATED
  F06 apical-domain poses (binder=A 1-N, target=B 1-195, resnum1=UniProt189) — use these for placement.

## F07 switch_contacts validator + first validated switch-binder (2026-10-20 late)
`scripts/switch_contacts.py` (Baker His-cation metric, dep-free) on the RE-FOLDED model confirms the His
actually sits by a cation (re-fold can move it away). First fully-validated switch-binder:
- **armC_mini gpu5_12 sw2his**: binding kept (Chai iptm 0.491 > parent 0.407) AND His A13 makes 4 buried
  contacts to binder R17 (mech-B, >Baker floor 2). (2nd His A49 lost its K89 contact on re-fold — 1 strong
  buried His-Arg pair still = a real switch.) 95aa, developability CLEAN (Nglyc2 only).
Switch-binder gate = binding-retained (Chai≥~0.35) ∧ switch_contacts total≥2 on the re-folded model.
Next: mech-A re-fold (18 seqs, bhmf2we3p) -> same gate; then pKa in-window check (JustHISpKa, env deferred).

## F07 mech-A RESULT: 4 validated switch-binders (2026-10-20 late)
Mech-A single-His (mA1) retains binding 8/9 (vs mech-B retrofit 1/6) — SOTA pivot validated. 2-His (mA2)
mostly broke binding -> single interface His is the gentle, binding-safe switch. Switch GEOMETRY check
(switch_contacts on the re-folded model) narrows to those whose His actually sits by a cation:
| switch-binder | mech | His->cation | dist | bind iptm (parent) |
|---|---|---|---|---|
| armC_mini gpu5_17 mA1 | A | His36->K194(tgt) | 6.0Å | 0.702 (0.475) |
| armC gpu2_31 mA1 | A | His37->K287(tgt,apical99) | 5.6Å | 0.616 (0.569) |
| armC gpu2_18 mA1 | A | His47->K287(tgt) | 4.9Å | 0.554 (0.505) |
| armC_mini gpu5_12 sw2his | B | His13->R17(binder) | 3-4Å ×4 | 0.491 (0.407) |
(armA gpu5_34 mA1 works 0.504 but dev-SEVERE -> deprioritize.) K287 (apical resnum 99) is a recurring
interface target lysine (gpu2_18/gpu2_31/gpu5_34 all switch on it). Honest: single-His mech-A ≈ 1 pH unit,
modest; magnitude in-silico-unrankable -> select for mechanism DIVERSITY (mech-A + mech-B) + binding + novelty.
TODO: His pKa in-window check (nearby K+ lowers His pKa; verify transition stays ≥6.0) — JustHISpKa env deferred.
Mouse co-fold (13 plain binders) running on GPU0; expand 297/317 (full pool imminent).

## F07 switch-His pKa (PROPKA first-pass) — 2026-10-20 late
PROPKA (tools/pka-venv, uv) His pKa on the re-folded complex (model ref 6.50; higher=stronger in-window switch):
- gpu5_12_sw2his His13 pKa **6.23** — BEST (near midpoint, buried His13-R17, binding IMPROVED) = flagship switch
- gpu2_18_mA1 His47 **5.76** — good mech-A switch (bind 0.554)
- gpu5_17_mA1 His36 **5.59** — acceptable mech-A (bind 0.702, best binding)
- gpu2_31_mA1 His37 **5.28** — weak switch (nearby K287 lowered pKa; confirms the mech-A pKa-depression risk) → keep as a binder, switch marginal
All have correct DIRECTION (Δn_H>0 across 7.4→6.0). Caveat: PROPKA is the weakest His predictor (R²~0.05,
±1u) → treat as first-pass; confirm flagship(s) with JustHISpKa/pKAI before final. Magnitude unrankable →
select for mechanism diversity. Switch-binder ranking so far: gpu5_12_sw2his > gpu2_18_mA1 ≈ gpu5_17_mA1 > gpu2_31_mA1.

## Full-pool gate + novelty + Boltz dual-gate on switches (2026-10-21)
**Full pool (Chai iptm≥0.35 ∧ Boltz iptm≥0.5): 18 binders** (runs/f06/f06_pass_full.tsv). Expand added 5:
gpu2_13 (chai 0.697 NEW top), gpu1_08, gpu4_09, gpu4_00, gpu4_31. Dev: 4 new CLEAN, gpu1_08 SEVERE.
**Novelty (single-seq ESMFold + foldseek vs PDB) = SYSTEMIC high-TM** (BoltzGen makes PDB-like folds):
almost all 0.85-1.0 (risk/borderline); new binders too (gpu2_13 0.923). Most novel: gpu4_28 0.774,
gpu5_17 0.844, gpu5_26 0.882 (but these are dev-SEVERE or Chai-weak). ASSUMPTION (reference-adaptyv-novelty-metric):
de-novo helical bundles w/ low seq-id cap at 3/4 => PASS the ≥3/4 gate; 4/4 unreachable without a novel-fold
generator (RFd3/Genie3 not installed). Treat novelty as ~uniform 3/4 pass (not a differentiator); RISK noted.
**Boltz dual-gate on switch-binders** (His mutation can drop Boltz even when Chai holds):
- gpu2_31_mA1  chai .616 ∧ boltz .843  ✓✓ consensus (pKa 5.28 weak switch; novelty .895)
- gpu5_12_sw2his chai .491 ∧ boltz .566 ✓✓ consensus (pKa 6.23 BEST switch; novelty .945 risk; 95aa)
- gpu2_18_mA1  chai .554 BUT boltz .409 ✗ Chai-only (parent was .831 — His hurt Boltz)
- gpu5_17_mA1  chai .702 BUT boltz .437 ✗ Chai-only (parent .809)
=> 2 dual-consensus switch-binders + 2 Chai-only (riskier). Honest: no single design aces switch+novelty+binding.

## NOVELTY CRISIS (2026-10-21) — BoltzGen pool fails the HARD gate
Coverage-weighted novelty (Adaptyv-exact: max TM among hits qcov>=0.70; <0.80=PASS 3/4, >=0.80=DQ 2/4;
PDB-only = LOWER bound, AFDB would raise it). Of 18 binders, only **3 PASS**: gpu5_17 (0.757), gpu5_26
(0.761, dev-SEVERE), gpu4_28 (0.774, dev-SEVERE). gpu4_33=0.0 is a FAILED ESMFold fold (unfoldable, exclude).
ALL the good binders/switches are DQ: gpu2_31/gpu2_31_mA1 (0.895), gpu5_12/sw2his (0.942/0.945),
gpu2_13 (0.923), gpu4_21 (0.914), gpu2_18 (0.929). => **BoltzGen makes PDB-like folds; it fails Adaptyv novelty.**
ONLY clean novelty-pass + switch-capable binder = **gpu5_17 / gpu5_17_mA1** (0.757/0.764, dev-CLEAN, Chai 0.702).
Decision: (1) mine the FULL BoltzGen pool for lower-binding-but-novel folds; (2) if that's dry, PIVOT to a
structurally-novel generator (RFdiffusion/Genie3 — diffusion explores novel fold space; co-folding does not).
This is the side-agent-warned pivot. Runway to 2026-11-01 ~11 days = feasible.

## PIVOT DECISION (2026-10-21): diffusion generator for novelty
Mining the full BoltzGen pool for novel folds is DRY: designs with novel folds (raw TM<0.8) are Boltz-only
(Chai says they DON'T bind — circularity). The binding-novelty tradeoff is intrinsic to BoltzGen (co-folding
reproduces PDB folds). Real binders that PASS novelty: gpu5_17 (0.757, CLEAN, switch mA1, x-react mouse 0.475!),
gpu4_28 (0.774, dev-SEVERE), gpu5_26 (0.761, dev-SEVERE). = 1 clean design.
**PIVOT: install a DIFFUSION generator (RFdiffusion1 first; RFd3/Genie3 if it floors) to produce
structurally-novel binders to the TfR1 apical epitope.** Pipeline: RFd backbones -> ProteinMPNN (0-Cys) ->
Chai∧Boltz validate (fair for non-BoltzGen designs) -> novelty (expect LOW TM) -> mech-A/B switch -> x-species
-> select. FLOOR = gpu5_17 (+ cleaned SEVERE). Kit source: /home/prachh/work/cache/uplifting-biomolecular-modeling/
{rfdiffusion1,rfdiffusion3,genie3}. Note: af2ig broken here -> Chai∧Boltz is the binding gate.

## RFd1 installed + first-design novelty check (2026-10-21)
RFd1 (rfdiffusion1 opt-kit, route C) INSTALLED in third_party/rfd1kit (venv rfd1, weights OK, run.sh check
passes H100, mode=fast). Smoke (2 de-novo, apical hotspots A202/A209/A211, len 70-90): WORKS, ~3min cold-start
(Triton compile) then fast. BUT des_0 backbone foldseek covwTM=0.955 vs PDB = NOT novel (RFd1 default also makes
PDB-like helical bundles). => novelty is NOT automatic with RFd1 either; need the FRACTION of designs with TM<0.8.
Running batch1 (42 designs) to measure the novel-fold yield distribution.
Nuance (reference-adaptyv-novelty-metric): oracle TM is NOISY (portal estimates off up to 2 levels); the
USER-RUN PORTAL check on the final set is the only hard authority. Strategy: maximize novelty MARGIN (prefer
low-TM designs), keep gpu5_17 (oracle-novel 0.757) as floor, generate RFd1 low-TM designs, and gate the FINAL
set on the portal (user-run) pre-submission. Tooling added: self_consistency.py (ESMFold self-consistency +
novelty in one pass, replaces broken af2ig), gen_rfd1.sh, mpnn_rfd.py.

## RFd1 novelty-yield diagnosis + long-binder fix (2026-10-21)
Measured backbone Rg (compactness) + coverage-weighted foldseek novelty on RFd1 batches:
- **batch1 (65-90aa)**: ~70% EXTENDED (single long helices, Rg 26-34 for ~70aa = a straight helix, not a fold);
  only 1/42 compact&novel. SHORT binders to a 3-residue hotspot => RFd1 lays a single extended helix. GARBAGE.
- **batch_long (105-130aa)**: 5/10 compact, **3/10 compact&novel** (des_3 124aa covwTM 0.638 ROBUST, des_4 0.708,
  des_5 0.799). LONG binders fold into compact bundles AND are more novel (longer folds rarer in PDB).
- Extended issue is NOT mode-specific (off-mode des_0 also Rg 34.1) => inherent to short-binder setup, fixed by length.
- MPNN chain bug FIXED: RFd1 output is target=chain A, BINDER=chain B (design B not A).
DECISION: generate LONG binders (100-135aa); filter Rg (compact) + novelty; then MPNN(B,0-Cys) -> self_consistency
(ESMFold real-gate novelty + self-consist) -> Chai∧Boltz binding -> switch -> select. Launched long1 (240 designs).
Funnel yield est: 240 -> ~70 compact&novel -> ~10-30 novel binders. gpu5_17 remains the floor.

## RFd1 novel-binder funnel RESULT (2026-10-21)
long1 (240 long binders) -> 110 compact (Rg) -> 220 MPNN seqs (chain B, 0-Cys) -> self_consistency:
**187/220 self-consistent (85%), 49 novel, 31 self-consistent AND novel** (covwTM 0.70-0.80, PDB-only).
HUGE improvement over BoltzGen (~1 novel). Caveat: all 0.70-0.80 (3/4 PASS but near the line; AFDB would raise;
0 robust <0.65) -> user portal check is the final novelty authority. Chai binding validation launched on the 31
(b4sumfysu); Boltz YAMLs prepped for the dual gate. Next: Chai∧Boltz binders -> switch (mech-A/B) -> x-species
-> developability -> select ≤20 (novel RFd1 binders + gpu5_17 floor). The long-binder RFd1 path WORKS for novelty.

## Novel-binder yield reality + refined plan (2026-10-21)
- des_160_mpnn1 (the 1 novel RFd1 binder): Chai 0.639 but **Boltz 0.317 => Chai-ONLY** (fair, RFd1 is Boltz-independent).
- Partial diffusion from des_160: DUD — children drift to extended/non-novel (parent is marginal-novel 0.793, so children
  inherit marginal/worse). Dropped. Partial diffusion needs a ROBUSTLY-novel (<0.65) parent, which I don't have.
- **Brutal yields**: novel+binding ~0.5% de-novo, and those are mostly Chai-only + MARGINAL novelty (0.70-0.80, near DQ line).
- **Best design remains gpu5_17** (BoltzGen): novel 0.757 + dual-folder binding (Chai .475 ∧ Boltz .809) + mech-A/B switch +
  cross-reactive (mouse 0.475). The most complete single design across all axes.
**Refined plan**: scale de-novo RFd1 volume (long2 420 running + more rounds) with nseq=8 in the MPNN step (4x binding
chances/backbone — rescues near-miss backbones at Chai 0.25-0.30) -> accumulate marginal-novel Chai-confirmed binders.
Realistic target ~8-15 novel binders (not a forced 20). Portfolio: gpu5_17 (anchor) + des_160 + novel RFd1 binders;
switch where it survives; USER portal novelty check is the final gate (oracle is noisy). Honest: a 20-strong-on-every-axis
submission is not achievable with these tools; aim for the best legitimate novel+switch+xreact portfolio.

## Developability + spec-driven strategy pivot to BindCraft (2026-10-21)
Re-read configs/target.yaml (authoritative). Key facts that reshape the plan:
- **Epitope** apical [202,203,204,208,209,210,211,212,348,371]; **conserved-in-mouse = ONLY 202,203,209**
  (I/V/L, hydrophobic). Exposure (isolated-domain neighbor count): 202 BURIED, 203 mid, **209 EXPOSED**,
  211 EXPOSED(center), 204/208/212 exposed but DIVERGENT, 371 buried. => the conserved surface is small
  (209 the one well-exposed conserved anchor); full cross-reactivity is intrinsically hard.
- **Switch**: mech-A (interface His vs target cation) is HUMAN-SPECIFIC (apical basics R208,K371 diverge
  in mouse) -> my gpu5_17_mA1/gpu4_28_mA1 are human-only. mech-B (buried multi-His) = cross-reactive.
  Physics budget: single His ~=25x (near floor); **need 2-3 SEPARATED His**. Selector prefers a weak-but-
  clear switch over a strong non-switch -> pH-selectivity is THE highest-value property.
- **Novelty**: Adaptyv 1-4 LEVEL scale, hard gate >=3, BINDING-PART ONLY, target 4. NO-FLY 6WRV/3DS18/TB14/VP1u.
- **Submission**: ranked <=20, selector takes <=10 from the TOP (front-load best ~10), diversify ~2/lineage
  across 9 classes (miniprotein/small/peptide/Fab/nanobody/scFv/monobody/DARPin/affibody).

DEVELOPABILITY AUDIT (scripts/developability_scan.py on the novel core) — DECISIVE:
- gpu5_17 GRAVY +1.29, gpu5_26 +1.19 (SEVERE), gpu4_28 +0.95 (SEVERE, 11-res hydrophobic run). ALL 3
  BoltzGen novel binders are EXTREMELY hydrophobic (expression/aggregation risk) — because the conserved
  hotspots are hydrophobic AND MPNN made the WHOLE binder hydrophobic.
- des_160 (RFd1): LIAB=1, 52% charged, SOLUBLE. RFd1+MPNN binders are DEVELOPABLE; BoltzGen are not.
=> A binder that won't express can't win. This re-justifies de-novo (soluble) over BoltzGen, AND motivates
   BindCraft (built-in Surface_Hydrophobicity/liability filters keep the NON-interface surface polar).

Novelty table rebuilt (coverage-wtd foldseek + pLDDT gate, pLDDT is 0-1 scale):
- **Novel dual-binders (level 3)**: gpu5_17 (covwTM 0.757, pLDDT .70), gpu5_26 (0.761, .80),
  gpu4_28 (0.774, .90 = most trustworthy). All PDB-only lower bounds (AFDB raises) -> portal is the authority.
- gpu4_33 covwTM 0.000 = FALSE novelty (ESMFold garbage: 41aa, pLDDT 0.6, zero foldseek hits). EXCLUDED.
- Switches generated (mech-A, scripts/mech_a_scan.py -> runs/f07/mecha_novel.csv): gpu5_17_mA1(validated)/mA2,
  gpu4_28_mA1/mA2. gpu5_26 yields NO mech-A (no target cation near interface) -> plain-binder or mech-B only.

**BindCraft2 PIVOT** (SOTA, installed+proven in the glp1r project; TfR1 project had only AF2 params):
BindCraft gives soluble + AF2-validated (3rd folder beyond Chai/Boltz) + de-novo binders, with modalities
(binder/large_binder/VHH/scFv/Fab = the 9 submission classes) and properties (**mixed_topology** = alpha/beta
folds rarer in PDB -> beats the "helical bundle caps at 3/4" novelty ceiling; humanize; termini_accessible
for the C-term Twin-Strep tag). This fills the exact gap: BoltzGen=novel+strong+hydrophobic; RFd1=novel+
soluble+weak; **BindCraft target = novel(mixtopo)+soluble+strong**. Campaign prepared:
runs/f12/bc2/mixtopo.json (binder, apical hotspots A203,A209,A211=conserved-anchored, 60-120aa, 0-Cys,
non-helical weights, betasheet>=0.2, iptm>=0.6, 40 finals/400 traj) + smoke.json. Switch installed post-hoc.

GPU STATE: all 8 GPUs are running the USER's GLP1R BindCraft 4-arm campaign (deadline 2026-10-25 = SOONER
than TfR1 2026-11-01). NOT clobbering it. Watcher bcbwo5wzi waits for it to finish, then re-invokes.
Staged for the GPU window: (1) BindCraft TfR1 smoke -> full mixtopo campaign; (2) RFd1 funnel on 1472 staged
seqs (long2 nseq8 1136 + long1 rescue nseq16 336) via self_consistency -> Chai -> Boltz; (3) re-fold the new
switches (gpu5_17_mA2, gpu4_28_mA1/mA2) to confirm binding retained; (4) mech-B multi-His on survivors.
Current best complete design remains gpu5_17 (novel+dual-bind+switch, but hydrophobic). Portfolio target:
diverse soluble novel switch-binders, front-load ~10, user portal novelty check is the final gate.

## 2026-10-23 — GPU window opened; funnel + BindCraft launched
GLP1R campaign finished (watcher bcbwo5wzi hit 48h; live nvidia-smi: all 8 GPUs 0 MiB, no foreign compute apps). Launched three non-contending background jobs:
- **BindCraft smoke** (b6r0x3c86, GPU 0): `bindcraft design runs/f12/bc2/smoke.json` → gate for the full mixtopo campaign; log runs/f12/bc2/smoke.log
- **long2 self-consistency** (bup010hgx, GPUs 1-5): 1136 seqs, backbones=long2_compact → runs/f12/sc/long2/all.csv (ESMFold+TMalign SC + foldseek novelty)
- **long1_rescue self-consistency** (bcyghampl, GPUs 6-7): 336 seqs (21 proven-novel backbones @nseq16), backbones=long1_compact → runs/f12/sc/long1r/all.csv
Driver: scripts/sc_shard.sh (shards self_consistency.py; per-shard struct-dir avoids fs_tmp collision). venv=.venv-esmfold2 (torch2.14+cu130, tfm5.19).
SC gates: self-consistent bb_TM>=0.80 & rmsd<=2.5; novel covwTM<0.80 (robust<0.65).
**NB long2 & long1_rescue share stems** (des_160 etc. = DIFFERENT backbones per batch) → keep outputs namespaced; prefix l2_/l1_ when merging survivors for Chai∧Boltz.
Next: smoke passes → full mixtopo campaign; SC done → filter sc&novel → Chai∧Boltz dual-gate (receptor=data/targets/apical_domain_189_383.seq, mouse=mouse_apical_189_383.seq).

## 2026-10-23 — smoke verdict + funnel results (live)
**BindCraft smoke (b6r0x3c86, non-helical):** config VALID, pipeline works end-to-end (target 195aa, hotspots A203/209/211, forced-targeting lysinated 101/195). 0/4 accepted — 2 strong trajectories (anneal i_pTM 0.83, 0.64) COLLAPSED at harden (0.08, 0.20) = aggressive non-helical pressure fragile under sequence hardening. Helical already clears novelty GATE(≥3); non-helical only pushes toward level-4 target. → running moderate-helix diagnostic.
**smoke2 (bz245pdas, GPU0):** weights_non_helical 1.0→0.3, max_helix_fraction 0.5→0.7, 8 traj → decides full-campaign helix.
**long1_rescue SC (bcyghampl):** 336 seqs → 178 self-consistent&novel (53%, from 21 proven-novel backbones). Top novelty covwTM 0.667-0.72 (solid L3, nearing robust<0.65). bb_TM 0.85-0.98.
**long1r Chai triage (b6653bpwk, GPU6-7):** 178 survivors (l1_ prefix) vs human apical, samples=3 → runs/f12/chai/long1r. Chai-FIRST screen; Boltz-confirm shortlist only (avoids Boltz on ~500).
**long2 SC (bup010hgx, GPU1-5):** 1136 seqs, still running.
GPU map: 0=smoke2 | 1-5=long2 SC | 6-7=long1r Chai. Next: smoke2→campaign helix decision; long2 SC→long2 survivors→Chai; long1r Chai→rank→Boltz-confirm shortlist.

## 2026-10-23 — BindCraft harden-collapse is NOT helix; long2 survivors
**smoke2 (moderate-helix) 0/8** — SAME harden-collapse: every trajectory reaching good anneal i_pTM (0.60-0.75) collapsed at harden (0.09-0.33). → helix content NOT the cause. Systematic suspect: **forced_targeting lysinates 52% (101/195) of target surface** = artificial charge field the binder exploits soft-stage but can't hold when hardened.
**smoke3 (b2n2bjljp, GPU0):** forced_targeting=false, default helix, no final dev-filters = pure "can BindCraft bind this apical target at all" feasibility test. If 0/8 again → cut BindCraft (target too hard), go all-in RFd1 funnel + switch. If accepts → reintroduce constraints.
**long2 SC:** 255 sc&novel (8 robust covwTM<0.65: des_81_mpnn3 0.571, des_214_mpnn5 0.573...). 57 unique backbones. → Chai triage bkj0arm8o GPU1-5.
**parse_boltz.py:** added "apical" hotspot set + l1_/l2_→apical mapping (correct on-epitope contact counting for RFd1 designs).
GPU map: 0=smoke3 | 1-5=long2 Chai | 6-7=long1r Chai.

## 2026-10-23 — BindCraft root-caused via GLP1R working config
**smoke3 (forced_targeting OFF):** traj1 PASSED harden at i_pTM=0.79 (real AF2 interface!) then died at MUTATE (0.79→0.18, pLDDT→0.42). Two tunable killers: forced_targeting (harden) + mutate-stage MPNN interface-redesign (binding, = af2-seq-specific lesson).
**Root cause via GLP1R campaign_settings.json (produced 30 designs, same install):** my minimal configs left defaults. Key proven levers missing: **redesign_interface=false** (no interface MPNN-redesign at mutate), **sequence_candidates=10 / kept_sequences=1** (10 MPNN tries, keep best), **min_plddt_mutate=0.55** (I had 0.65), explicit min_iptm_harden/mutate=0.5, mpnn_variant=negative, full filters/losses/weights blocks.
**apical_test.json (bvzhr22fm, GPU0):** GLP1R config + overrides {modality binder, lengths 60-120, forced_targeting FALSE, hotspots A203/209/211, 30 traj, 5 designs}. Dev left permissive (aa_bias C:0) → post-filter. Go/no-go: >=2-3 accepts in 30 → full campaign (450 traj, 40 designs, multi-GPU); ~0 → cut BindCraft, all-in RFd1.
GPU map: 0=BindCraft test | 1-5=long2 Chai | 6-7=long1r Chai.

## 2026-10-23 — STRATEGIC INFLECTION: apical epitope walls de-novo confident binding
**long2 RFd1 Chai (255 survivors): ZERO on-epitope confident binders.** Confident ones (iptm 0.6-0.68) dock OFF-epitope at UniProt 259-300 (stickier patch); on-epitope ones (hot>=3) all iptm<=0.30, ipae>18. Verified NOT a pipeline bug: RFd1 correctly used input=tfr1_apical_189_383.pdb, hotspots=[A202,A209,A211]. De-novo binders simply aren't apical-specific (flat/polar/buried epitope — matches lesson-denovo-wall-flat-polar-target).
**BoltzGen "dual binders" re-examined (f06): weak 2-folder consensus** — gpu5_17 chai0.475/boltz0.809, gpu5_26 0.423/0.852, gpu4_28 0.394/0.812. High Boltz (lineage-biased) but Chai (independent)=0.4 weak. + hydrophobic. Not robustly confirmed.
**BindCraft proven-config test: 0/18 so far** (likely cut if 0/30).
**Conclusion forming:** no method yields a STRONG two-folder apical binder; epitope is the central wall. This is WET-LAB-judged → in-silico = prior, not verdict. Winning play = DIVERSE portfolio of best on-epitope binders (any lineage) + pH-switch, front-load best-evidence, trust wet lab.
**Unexploited lever = PARTIAL DIFFUSION from the BoltzGen apical binders** (pose-preserving; beats de-novo ~11% vs 0.3%; lesson-rfd-partial-diffusion-beats-denovo). Diversify fold toward novelty+solubility while KEEPING the one apical pose that scores. Pending refold (bi6lqhjci) confirms their on-epitope landing + switch-retention first.
GPU map: 0=BindCraft test | 1-5=best-asset refold Chai | 6-7=long1r Chai.

## 2026-10-23 — VALIDATOR WAS BROKEN (positive control 3DS18 drifts to sink)
POSITIVE CONTROL: crystal-true apical binder 3DS18 (6WRV, footprint [199-215,340-376]) blind-co-folded (Chai) vs apical fragment -> docks 259-300 SINK, iptm 0.204, 0 apical contacts. f06 latent evidence: blind POS_3DS18 iptm 0.20 (chai)/0.28 (boltz) — never checked. => blind single-seq co-fold CANNOT validate apical binding here; ALL prior "binders" (RFd1+BoltzGen, both folders) scored the sink. My "nothing binds apical" conclusion was a validator artifact.
FIX: pocket-RESTRAINED Boltz (scripts/prep_boltz_pocket.py; apical chainB resids [14,15,16,20,21,22,23,24,160,183], max_distance 6, force true).
CALIBRATION (bb0dsrhgi, GPU0-5): 33 candidates (30 long2 + 3 BoltzGen) + POS_3DS18 + 2 NEG scrambles. Gate: POS high + NEG low => method discriminates => run full 433 survivors restrained.
BindCraft apical_test: 0/30 even with proven GLP1R config (set aside; AF2 hallucination can't make confident apical binder — but its internal validation is pose-aware so this is a truer 'hard' signal).
Saved memory [[lesson-tfr1-apical-blind-cofold-fails-poscontrol]].

## 2026-10-23 — BREAKTHROUGH: pocket-restrained validator works; real apical binders found
CALIBRATION (pocket-restrained Boltz, force=true): POS_3DS18 ab_iptm=0.863 ipae=5.95 hot=13 (vs 0.20 blind!); NEG scrambles 0.20-0.32 ipae>19 hot=0. Method DISCRIMINATES cleanly. Real apical binders in the 30-design calib subset: l2_des_344_mpnn1 (0.74/ipae8/hot6), l2_des_241_mpnn6 (0.72/hot8), l2_des_136_mpnn1 (0.69/hot10), gpu5_26 (0.76/hot5), ~13 pass ab_iptm>=0.55 & ipae<=12 & hot>=5 & iplddt>=0.8.
FULL VALIDATION (bbj7b5r2e, 8 GPUs): all 440 candidates (long2 255 + long1r 178 + BoltzGen 3 + mechA 4) + 3 controls, pocket-restrained Boltz -> runs/f12/pocket/full_out. Killed obsolete long1r blind Chai (b6653bpwk) to free GPUs.
NEXT: parse full_out -> gate (ab_iptm>=0.55,ipae<=12,hot>=5,iplddt>=0.8 vs POS0.86/NEG0.32) -> INDEPENDENT confirm (Chai pocket-restrained, add restraint support) -> developability -> switch (mech-B multi-His) -> mouse x-react (pocket-restrained vs mouse_apical) -> novelty -> select 20.

## 2026-10-23 — 105 apical binders found (pocket-restrained Boltz); funnel underway
FULL pocket-restrained Boltz (443): controls POS_3DS18 0.848 / NEG 0.23-0.27 (gate valid). 106 pass ab_iptm>=0.55 & ipae<=12 & hot>=5 & iplddt>=0.80 (=105 real + POS). Lineage: 68 long2, 37 long1r, 0 BoltzGen (RFd1 de-novo dominate = soluble+novel). TOP: l2_des_417_mpnn7 (0.892/ipae5.6/hot9/GRAVY-1.16), l1_des_50_mpnn1 (0.834/hot10), l2_des_386_mpnn2 (0.821), several BEAT the positive control.
DEVELOPABILITY (inline GRAVY/Cys/run/charge): 74/105 soluble (GRAVY<0, 0-Cys, hydrophobic-run<=6). All top candidates 0-Cys, GRAVY -0.5 to -1.6 (very soluble). vs BoltzGen +0.95..+1.29.
NOVELTY (covwTM from SC, PDB-only lower bound): 101 L3 (<0.80), only 2 robust (<0.65); most 0.73-0.80 (near edge). Prefer lower covwTM; portal = final authority.
master table: runs/f12/pocket/master.tsv (105 rows: abiptm,iplddt,ipae,hot,L,gravy,nCys,run,chg,covwTM).
IN PROGRESS: Chai pocket-restrained dual-confirm (chai_confirm_in: 48 cand <=2/backbone + controls; watcher b6vhgrhks). THEN: switch pipeline (buried_switch_scan -> build_multihis mech-B 2-3His -> re-fold pocket-restrained to confirm binding RETAINED -> ph_release_consensus) on dual-confirmed soluble novel; mouse x-react (pocket-restrained vs mouse_apical_189_383); select 20 (front-load, <=2/backbone, diversify).

## 2026-10-23 — mech-B switches installed; 12 bind+switch-valid
Dual-confirm (Boltz∧Chai restrained, 48 tested): 8 strong dual + Tier-2 Boltz-strong. Selected 12 (>=0.65 bolt & >=0.38 chai, <=3/bb) for switches.
buried_switch_scan: all 12 have abundant buried K/R anchors (10-24 each) despite net-acidic -> mech-B feasible.
build_switch_combos.py (mech-B, SEP 8A, IFACE_CUT 9A, 2+3 His): 24 switched seqs.
RE-FOLD (pocket-restrained Boltz): 16/24 RETAIN apical binding (ab>=0.55,ipae<=12,hot>=4). Controls POS 0.853/NEG 0.21-0.27.
switch_contacts geometry: 12/16 valid mech-B (His-cation contacts>=2). Strong: l1_des_223_mpnn3_sw3his(11), l2_des_206_mpnn6_sw3his(7), l2_des_374_mpnn7_sw3his(7), l2_des_25_mpnn0_sw3his(5). sw3his > sw2his switch decisiveness.
=> 12 designs: bind apical (dual) + retain binding post-switch + valid mech-B geometry + soluble + novel (L3). From ~9 backbones.
MOUSE X-REACT (b3nq1qsmt, running): pocket-restrained Boltz vs mouse_apical (only 4/10 epitope pos conserved: 202/203/209/210 hydrophobic; 6 divergent). mech-B is target-independent so switch transfers; binding transfers iff interface on conserved core.
NEXT: mouse results -> rank (binding+switch+xreact+novelty+dev) -> select <=20, front-load 10, <=2/bb.

## 2026-10-23 — PORTFOLIO: 14 switch-valid human-binding designs (9 backbones)
Switch cycle 2 (cross-reactive backbones l1_des_215,l2_417,l2_408,l2_270): adds l2_des_417_mpnn7_sw3his (hum0.84/mou0.72/ratio0.86/swG2 = strong triple-winner), l1_des_215 (xreact,marginal bind), l2_408_sw2his (0.75,swG7 human switch). (geom loop bug: switched.csv is COMMA-sep, cut needs -d,.)
FINAL TABLE (runs/f13/final_table.tsv): 14 switch-valid (swG>=2) & human-binding (hum>=0.55,ipae<=12,hot>=4), 9 backbones.
TIER A triple-winners (switch+xreact+bind): l2_des_25_mpnn0_sw3his(0.65/0.65/r0.99/swG5) & _sw2his(0.62/0.85/r1.38), l2_des_417_mpnn7_sw3his(0.84/0.72/r0.86), l2_des_206_mpnn6_sw3his(0.81/0.46/r0.56/swG7), l2_des_374_mpnn7_sw3his(0.69/r0.51/swG7/covwTM0.674 BEST-novelty).
TIER B switch+bind human-biased: l1_des_223(×3,swG8-11,GRAVY-1.68), l2_des_408, l2_des_107, l1_des_160, l2_des_386.
ALL soluble (0-Cys, GRAVY mostly neg), novel L3 (covwTM 0.67-0.82).
RUNNING: Chai-restrained dual-confirm of the 14 SWITCHED (submitted) seqs (btpm5ktlu) — final gate (esp l2_417 parent Chai-weak).
SUBMISSION fmt: name,sequence,molecule_class=protein; Track2/3 ranked<=20 front-load10 <=2/bb. Validate via scripts/validate_submission.py --track 2. Upload USER-GATED.
RANK PLAN (front-load): triple-winners first (by xreact,switch,bind,novelty), then switch+bind; <=2/bb.

## 2026-10-23 — DEFINITIVE FINAL: 16 switch-valid designs (12 bb, 7 dual-confirmed)
Expansion (10 new backbones): only 3 boltz-only keepers (His mutations broke binding or switch for most new bb). Single-His RESCUE of l2_des_25 -> sw1_A9 DUAL (0.62/0.63) + mouse 0.78 ratio 1.26 + swG3 = TRIPLE-WINNER flagship (#1).
FINAL submissions/tfr1_track2_final.csv (16, ranked, <=2/bb, PASS). Front-7 DUAL-confirmed; front-10 = 7 dual + 3 boltz-only xreact hedges (l2_des_417, l2_des_408). All: mech-B switch (swG>=2), soluble (0-Cys, GRAVY<0.3), novel covwTM 0.67-0.82 (PDB-only L3; portal=authority; lower=safer).
Objectives: #1 switch (all valid mech-B) / #2 xreact (flagship ratio 1.26, several 0.5-0.7) / #3 affinity (bolt 0.58-0.84, 7 dual). Baselines: v1(12), v2(12), final(16) all validated.
UPLOAD USER-GATED. Novelty portal check = final gate before upload.

## 2026-10-23 /ambition-lift reassessment (v3)
- **Flagship upgraded (evidence-based):** old #1 single-His d25_sw1_A9 -> NEW #1 d25_sw2b_A9_A25 (2 His: A9/R13 + A25/R28).
  Reval f15 (clean, POS_3DS18 Chai0.72/NEG0.14): Chai0.50 + Boltz0.53 (dual), x-react ratio 0.96 Chai / 1.50 Boltz (best), mech-B swG4-6.
  Root cause of earlier miss: "des_25 multi-His breaks Chai" was a BAD His pair (A9+A54 Chai0.31); A9+A25 passes (0.50).
- **Top-10 fixed:** dropped Chai-failing d408 (0.178) from top-10; demoted Boltz-only d417 (Chai0.29) + novelty-borderline d107 (covwTM0.82).
- **submissions/tfr1_track2_v3.csv** = 20 ranked, validate_submission --track 2 PASS (0 errors). Prior: final.csv(16), v1/v2.
- **SOTA scan (2 subagents):** keep Boltz/Chai + mech-B buried-His; switch magnitude still unrankable. Gap = generator diversity (organizers' own Aug-2026 protocol: PXDesign/RFd3/Genie3 lead; flat targets->Genie3/PXDesign; SolubleMPNN; ESMFold2+Protenix v2 ipSAEmin filter).
- **STRETCH (in progress):** RFD4-Proteina confirmed working (runs/f16; needs atomworks CIF w/ bonds+label_seq, not PDB/gemmi-cif). Full wave launched (8 GPU x128) targeting conserved apical sub-site (hotspots 202/203/209) for a 2nd x-react lineage + novel folds. Next: SolubleMPNN -> dual-species screen -> switch -> triple-confirm (Boltz+Chai+Protenix v2, ipSAEmin). +PXDesign/Genie3/RFd1-conserved planned.

## 2026-10-23 RFD4-Proteina generator-diversity campaign (v4)
- RFD4-Proteina (NVIDIA, user-flagged) run targeting the CONSERVED apical sub-site (hotspots 202/203/209). Input contract: atomworks CIF with bonds+label_seq (not PDB/gemmi-cif).
- wave1 1024 -> 982 soluble 0-Cys (92%, GRAVY med -0.18) -> 237 novel (maxTM<0.80) -> 154 human-binders (clean calib POS0.85/NEG0.23) -> 8 cross-reactive (ratio>=0.8) -> Chai: g7_1 dual-confirmed x-react (ratC0.92).
- wave2 900 -> 797 soluble -> 203 novel -> 117 human-binders -> 3 cross-reactive (g5_14 ratio1.15, g2_132, g2_137).
- KEY RESULT: RFD4 yields excellent NOVEL SOLUBLE cross-reactive BINDERS beyond des_25 (breaks the RFd1 x-react wall), BUT auto-placed mech-B buried-His switch loses geometry on these backbones (mechB 0-1 after refold) - same wall des_25 hit (only specific His pairs retain). Only g7_8_sw2his got a valid switch (mech-A, total4).
- v4 = v3 core (des_25_sw2b_A9_A25 flagship retained) + 4 RFD4 lineages (g7_8 valid-switch #6; g7_1/g5_14/g2_132 x-react depth) replacing 4 weakest v3 hedges. submissions/tfr1_track2_v4.csv validated PASS (20/0/0).
- All 8 GPUs utilized throughout (packed folding + 6-GPU generation waves).

## 2026-10-24 portal novelty + g7_1 switch rescue (v5)
- Portal novelty on v4: 19/20 PASSED; d107_m5_sw2his NOT PASSED ("contains a known binder fragment") - matches its covwTM 0.82 flag. Dropped.
- g7_1 per-backbone His-pair tuning (13 combos: singles+pairs across K15/R36/K42): NONE achieved valid mech-B geometry (mechB 0-1 after refold); g7_1 backbone cations don't retain His contact. mech-A would be species-specific. => g7_1 stays an x-react BINDER hedge, no designable switch. Reconfirms des_25_sw2b_A9_A25 as the unique switch+x-react design.
- v5 = v4 minus d107; g7_1/g5_14/g2_132 (no valid switch) demoted to hedge ranks 11-13; d386 promoted to #10; g6_32_sw2his added #20. Top-10 now all valid-switch designs. submissions/tfr1_track2_v5.csv validated PASS. (Re-run portal on v5: g6_32 is new, unchecked.)

## 2026-10-24 v6: 20 distinct backbones (remove within-upload redundancy)
- User: no "similar designs in this upload" (v5 reused des_25/206/223/4 across switch variants).
- Switch-installed + refolded 12 fresh distinct RFD4 backbones (top novel human binders): 8 dual-confirmed; g4_5_sw3his VALID-SWITCH (swG2); g1_15 (Bh0.95/Ch0.83), g0_96 (0.94/0.80) strong binders (swG0-1).
- v6 = 20 DISTINCT backbones, one design each, ranked by objective priority: valid-switch tier (des_25 flagship, des_206/223/374/4, g7_8, g4_5, des_386) -> x-react hedges (g7_1/g5_14/g2_132/d417) -> strong distinct binders (g1_15/g0_96/g7_73/g6_7/g4_91/g4_92/g5_24/g6_32). No shared backbones.
- submissions/tfr1_track2_v6.csv validated PASS. NOTE: 9 new RFD4 designs unchecked on portal novelty (from novel pool maxTM<0.80; re-run portal before upload).

## 2026-10-24 v7: 4-fold re-ranking of the 20 (organizers'-style ipSAE_min + switch cross-check)
- GOAL: align the front-loaded order (selector takes <=10 from TOP, row-order = ranking) to a rigorous
  re-score, since v6's within-tier order rested on the construction folds only. Re-scored ALL 20 v6
  designs on a UNIFORM 4-fold panel: {Boltz-2, Chai-1} x {human, mouse}, pocket-restrained, single-seq,
  POS_3DS18/NEG-scramble calibrated. runs/f17/. Scripts: score_ipsae.py (ipSAE via patched ipsae.py),
  switch_contacts.py on each fold, merge_rank.py (ipSAE_min = worst-case over folders per species).
- CALIBRATION: Boltz-h POS 0.55 / NEG 0.00; Chai-h POS 0.67 / NEG 0.00. Boltz-m POS_3DS18=0.00
  (correct: 3DS18 human-specific) but Chai-m POS=0.47 (Chai-mouse PERMISSIVE on x-species) -> use
  mouse ipSAE_min=min(Boltz-m,Chai-m), which correctly discounts Chai's spurious highs (g7_1 Chai-m 0.48
  but Boltz-m 0.01 -> min 0.01).
- #1 SWITCH (switch_contacts, Baker floor>=2, counted across all 4 folds): 4/4 ROBUST = d25, e223,
  d374, d206, g5_24; 3/4 = g7_73; 2/4 = g4_5, d4, d386; <=1/4 (did NOT hold) = g7_8 (v6 #6!), g7_1,
  g5_14, g2_132, d417, g1_15, g0_96, g6_7, g4_91, g4_92, g6_32. Switch validity is FOLD-DEPENDENT
  (cross-fold count is the robust signal). g7_73 & g5_24 (v6 bottom tier) have robust switches.
- #2 X-REACT (mouse ipSAE_min, floor ~0.15): d25 0.37, d417 0.23 (but barely binds human), g5_14 0.19;
  g4_92 borderline 0.11. Confirms x-react is rare; d25 the clear standout (also best on both folds).
- #3 AFFINITY (human ipSAE_min): robust strong binders g1_15 0.79, g0_96 0.77, g4_92 0.70, g6_7 0.69,
  g4_5 0.61, g7_73 0.58. FOLDER-DEPENDENT over-confidence CAUGHT: d386 (Boltz 0.73 but Chai 0.29 ->
  min 0.29), d4 (0.72->0.45). Weak binders (<0.40): d386, d374, d206, g5_24, g2_132, d417.
- CROWN: d25_sw2b_A9_A25 is the ONLY design valid on all three (switch 4/4, x-react 0.37, binds 0.41),
  robust across all 4 folds. Flagship #1 re-confirmed independently.
- v7 ORDER (affinity-floor ~0.40 gate, then lexicographic #1>#2>#3): d25, e223, g7_73, g4_5, d4,
  g5_14, g4_92, g1_15, g0_96, g6_7 (top-10) | d374, d206, g5_24, g6_32, d386, g7_1, g4_91, g7_8,
  d417, g2_132. SAME 20 SEQUENCES as v6 (re-order only) -> portal novelty 20/20 still holds.
  submissions/tfr1_track2_v7.csv validated PASS. v6 frozen as fallback. Upload USER-GATED.
- SWITCH SEARCH -> 2nd CROWN (runs/f17/sw_search, sw_rep, sw_mouse, sw_chai_*): exhaustive mech-B
  His-pair search (scripts/exhaustive_switch.py) on g5_14 (confirmed x-react dual-species binder whose
  v6 switch was marginal). 45 combos; found the v6 greedy pick (A13/R19+A39/K43) was marginal
  (frac>=2 = 0.20 across 5 replicate folds) while K31-anchored combos are ROBUST.
- KEY METHOD FIX: switch_contacts on a SINGLE Boltz fold is noisy (same seq gave total 1 vs 5 on
  different folds). Fixed by REPLICATE folding (DIFF_SAMPLES=5) + frac>=2 (scripts/switch_prob.py),
  calibrated: POSctrl e223 frac 1.00/d25 1.00, NEGctrl g0_96 0.00, marginal g5_14_sw2his 0.20. NOTE:
  DIFF=5 gives NOISY ipSAE (binding) -> use DIFF=1 for binding, DIFF=5 for switch probability.
- CROWN 2 = rfd4_g5_14_sw2b_A34_A50 (g5_14 + His A34/K31 + A50/K53). DUAL-FOLDER x DUAL-SPECIES
  confirmed: switch 4/4 folds valid (Boltz-h frac 1.00 mean4, Boltz-m 4, Chai-h 3, Chai-m 3);
  x-react ipSAE_min(Boltz-m,Chai-m)=0.185; binding ipSAE_min(Boltz-h,Chai-h)=0.382; novelty 0.737
  (NOVEL, = parent g5_14 which passed portal 20/20). A 2nd all-three design, DIFFERENT fold family
  (RFD4) than d25 (RFd1). (switch GEOMETRY validated, not magnitude — magnitude stays unrankable.)
- v8 = v7 with the crown REPLACING the old no-switch g5_14_sw2his (same backbone -> still 20 distinct):
  #1 d25 (x-react 0.37), #2 g5_14 crown (x-react 0.185), then e223/g7_73/g4_5/d4 (switch+binds),
  g4_92 (x-react+binds), g1_15/g0_96/g6_7 (binders) | 11-20 switch/binder hedges. validate PASS.
  submissions/tfr1_track2_v8.csv. **1 NEW sequence (the crown) vs the portal-checked v6/v7 set ->
  re-run Proteinbase portal novelty before upload** (local oracle novel 0.737; low risk). v7 = fully
  portal-verified fallback; v6 = original frozen fallback. Upload USER-GATED.

## 2026-10-24 v9 campaign (runs/f18): validate against the ORGANIZERS' EXACT JUDGE (selection prompt)
- User supplied the organizers' selection prompt. KEY: they co-fold BLIND vs the FULL ectodomain
  HOMODIMER (human 121-760 / mouse 123-763, UniProt-exact; my prior work used the apical FRAGMENT
  189-383) and score 3 screens: pLDDT, ipSAE, Kyte-Doolittle hydropathy. Built exact constructs from
  UniProt P02786/Q62351 (Tyr211 -> construct pos 91). Scripts: prep_blind_cofold, epitope_read,
  epitope_prob, build_pool, exhaustive_switch(reuse).
- DECISIVE CALIBRATION RESULT: the BLIND co-fold is UNRELIABLE on this target at EVERY scale.
  * ipSAE ~= 0.000 for ALL designs INCLUDING POS_3DS18 (the real crystal binder) on the full ectodomain
    -> the organizers' ipSAE screen CANNOT discriminate TfR1 apical designs.
  * ipTM does not separate signal from noise (NEG_scramble ipTM 0.75 > POS 0.58 on the homodimer).
  * Epitope read swings wildly: POS reads apical_frac 0.72 (monomer DIFF1), 0.20/helical0.80 (monomer
    DIFF5), apical 1.00 (homodimer DIFF1), 0.20/helical0.80 (homodimer DIFF5). The positive control
    drifts to the helical/transferrin face as much as the designs -> epitope read is NOISE, even on the
    organizers' exact homodimer construct, even de-noised over 5 replicates.
- CONSEQUENCE: the blind full-target signals (ipSAE/ipTM/epitope) are all non-discriminating. This
  CONFIRMS the fragment pocket-restrained methodology (v7/v8) was correct, and voids the "crowns drift
  helical" worry (POS drifts identically). The real-judge discriminators = SWITCH mechanism (physical,
  replicate-validated) > x-react (fragment) > apical binding competence (fragment pocket-restrained),
  plus developability (pLDDT: ALL pass 0.9-1.0; hydropathy: current 20 mostly soluble, g7_73 borderline
  +0.09) and novelty (L4). The organizers weight switch #1 and "no single in silico metric decides."
- POOL SWITCH-INSTALL (Phase A/B): screened a 1567-design pool (RFD4+RFd1, novel+soluble) -> 104
  fragment-binders -> exhaustive mech-B His-pair search (scripts/exhaustive_switch) -> replicate-fold
  switch P (scripts/switch_prob) -> dual-folder (Boltz+Chai) confirm binding + x-react + novelty.
  Yielded ~10 NEW dual-confirmed switch-designs (switch-vs-binding tension: strongest binders g0_146/
  g0_125 won't take a switch; switch-installable backbones are moderate binders; His install degrades
  binding for ~half). STANDOUT: rfd4_g5_120_sw2b (binding ipSAE_min 0.853 = strongest in the campaign +
  robust switch). 3rd CROWN found: rfd4_g1_133_sw2b_A10_A20 (switch Boltz-robust + x-react dual 0.244 +
  bind 0.349, novel 0.732).
- **v10 = FINAL/recommended (submissions/tfr1_track2_v10.csv + _evidence.csv), validate PASS.** 20
  distinct backbones, **16 switch-designs (incl 3 CROWNS: d25 xr0.37, g5_14 xr0.185, g1_133 xr0.244)**
  + 4 hedges (g4_92 xr+bind, g1_15/g0_96 strongest binders, d417 xr). Replaced 9 weak/no-switch v8
  designs with 8 new strong-binder switch-designs (g5_120/g2_138/g6_72/g1_69/g1_133/g1_76/g4_66/g4_93).
  Ranked switch(#1 clear mechanism) > x-react(#2) > fragment binding(#3), + pLDDT(all pass) + hydropathy
  + novelty. **8 NEW sequences -> re-run Proteinbase portal novelty before upload** (local oracle all
  NOVEL 0.69-0.74). Graduated fallbacks: v9 (4 new), v8 (2 crowns), v7 (same 20 seqs as v6, portal
  20/20 verified), v6. Upload USER-GATED.

## 2026-10-24 v10 PORTAL NOVELTY VERIFIED (20/20) — last gate cleared
- User ran the Proteinbase portal on v10's 20 sequences. Result: **"20 included • 0 needing fixes"**,
  every row Passed (all Single chain), **NO novelty / "similar designs" / "known binder fragment"
  flags** (that flag is what failed d107 in v4 — its absence = novelty gate clear).
- **Byte-verified the portal validated the EXACT v10 file:** all 20 names, row order (rows 2-21),
  sequence prefixes (first 12), suffixes (last 8), and lengths match submissions/tfr1_track2_v10.csv
  (d25=110, g5_14=71, g1_133=70, g5_120=99, e223=106, g4_5=94, g2_138=63, g6_72=69, d4=109, g1_69=83,
  g7_73=109, g1_76=94, g4_66=71, g4_93=72, d374=115, d206=124, g4_92=64, g1_15=70, g0_96=102, d417=106).
- The 9 sequences new since the portal-verified v6/v7 baseline (re-His'd g5_14 crown + 8 pool
  switch-designs g5_120/g2_138/g6_72/g1_69/g1_133/g1_76/g4_66/g4_93) ALL cleared. _v10_evidence.csv
  portal column updated re-check -> pass(2026-10-24).
- **v10 is now fully portal-verified (format + novelty). Ready to upload; upload remains USER-GATED.**
  Commit is LOCAL (push user-gated).

## 2026-10-24 v11 campaign (runs/f19): break the x-react floor (user: "replace a lot at all costs")
- **Why:** v10's weak axis is x-react (only 3 crowns) + 4 no-switch hedges (ranks 17-20). Revalidated the
  16 pool switch-designs on the COMPLETE dual-folder×dual-species panel (scratchpad/merge_xreact.py):
  robust x-react (ipSAE_min over Boltz∧Chai) is real for ONLY g1_133 (0.244, already in v10). The high
  Chai-mouse hits (g6_72 0.62, g5_120 0.41, g4_93 0.30, new g6_78 0.28, g0_37 0.21) are ALL contradicted
  by Boltz-mouse (~0.01) = folder-pessimism; ipSAE_min correctly rejects. POS_3DS18 human 0.595/mouse
  0.000, NEG 0.000 (calibrated).
- **Gap found:** x-react screen was INCOMPLETE — only the 16 switch-designs were mouse-folded, but the
  binder shortlist has 202 (104 human-scored, 62 with Boltz-h>=0.30, 27 with >=0.5 never x-tested).
- **LAUNCHED (bg bdxsz2vac):** exhaustive mouse x-react screen of the 62 strong binders + 3 controls,
  pocket-restrained dual-folder: Boltz-mouse {gpu0,2,3} + Chai-mouse {4,5} + Chai-human {6,7} (GPU1 =
  foreign job, untouched). runs/f19/{myaml,screen.csv,boltz_m,chai_m,chai_h}. On done: bind_min=
  min(frag_boltz_h,chai_h), xreact_min=min(boltz_m,chai_m); crowns = bind_min>=0.3 & xreact_min>=0.15.
- **Next (pending f19):** switch-install new crowns -> v11 (replace no-switch hedges + weakest). If the
  screen confirms the floor, run joint multi-state (human+mouse) MPNN to DESIGN x-react on crown
  backbones (the one untried SOTA lever). Genie3 (organizers' flat-target generator) available but needs
  a weights DOWNLOAD (user-gated). Judge frozen = v10 pipeline. Upload + push USER-GATED. v10 stands as
  the current best until v11 members are MEASURABLY better.
- **Genie3 APPROVED + BUILT (user: "pull the weights and run it too"):** scripts/setup_genie3.sh built the
  NVIDIA uplifting genie3 kit into third_party/genie3 (venv_g3, torch 2.7.1) + fetched weights
  (weights/genie3/pretrained/v1, step=600000.ckpt pinned OK); `run.sh check` h100/fast would_activate=True.
  Dataset `tfr1_apicalbench` (scripts: extract_apical.py + make_g3_dataset.py, staged runs/f20, copied into
  the kit) = apical fragment = UniProt 189-383 (contiguous), target PDB chain B renumbered 1-195. HOTSPOTS
  = conserved sub-site frag {14,15,21,22} = UniProt {202,203,209,210} = I,V,L,V, compact (max CA-CA 6.4A)
  -> biases toward CROSS-REACTIVE binders. scripts/gen_genie3_tfr1.sh (per-GPU shard, H100 fast line).
  Smoke test (n=2, GPU3) launched b78khpc0v; full gen (N=840, 7 GPUs) launches after f19 frees GPUs.
  Downstream funnel (MPNN->ESMFold/novelty->pocket Boltz∧Chai human+mouse->switch-install) reuses existing
  f12-f19 scripts. FUNNEL DE-RISKED (validated on smoke backbones):
  - Genie3 outputs CA-ONLY traces (binder=chain A, target=chain B, both CA). No PULCHRA available.
  - SOLUTION: ProteinMPNN CA-only model (weights/proteinmpnn/ca_model_weights/v_48_010.pt, --ca_only) runs
    directly on CA traces -> real binder seqs (fixed_chains=['B'], designed=['A']). No backbone rebuild.
  - proteinmpnn kit built (scripts/setup_proteinmpnn.sh -> third_party/proteinmpnn; 'check' step fails on
    torch-metadata but IRRELEVANT: stock third_party/proteinmpnn/stock/src/protein_mpnn_run.py + helper
    parse_multiple_chains.py + the fetched soluble/vanilla/ca weights all work via .venv-boltz python).
  - This fork LACKS assign_fixed_chains.py -> build chains.jsonl manually {name:[['A'],['B']]}.
  - MPNN seqs will be GRAVY/hydropathy-filtered downstream (CA model isn't soluble-biased).
  - Gotcha fixed: g3 problem JSON needs ABSOLUTE target paths (parse_pdb opens relative to CWD).

## 2026-10-24 f19 RESULT: 2 NEW x-react crowns + Genie3 waves running
- **f19 x-react screen DONE (bdxsz2vac, 65 designs scored).** Control calibration: Boltz-mouse is the
  RELIABLE discriminator (POS_3DS18 mouse=0.000 correct, NEG=0) while Chai-mouse is OPTIMISTIC (POS
  mouse=0.484 false-pos) -> xreact_min=min(boltz_m,chai_m) correctly rejects Chai false positives.
- **2 NEW ROBUST CROWNS** (bind_min>=0.3 & xreact_min>=0.15, BOTH folders agree on mouse):
  - rfd4_g7_tfr1_apical_xreact_mini_8: bind 0.517, xreact 0.240 (bM 0.305/cM 0.240), TM 0.74, 86aa
  - rfd4_g6_tfr1_apical_xreact_mini_7: bind 0.752, xreact 0.222 (bM 0.222/cM 0.243), TM 0.663(!), 105aa
  These were PRE-switch binders missed by the 16-design subset (only 16 of 202 were mouse-folded before).
  merge: scratchpad/merge_f19.py. Doubles the binder-level x-react yield (g1_133-class).
- **Switch-installed both** (scripts/install_switch.sh -> runs/f21/sw/switched.csv): g6_7_sw2his
  (A38H/K65;A69H/K104), g7_8_sw2his (A14H/K20;A39H/K72), g7_8_sw3his (+A78H/K82).
- **VALIDATING (beut5xsd4, GPU0):** scripts/val_switch_f21.sh — did bind+xreact survive His install +
  is switch robust? pocket dual-folder DIFF=1 (bind/xreact) + DIFF=5 switch_prob. Pass = bind_min>=0.3,
  xreact_min>=0.15, valid switch -> up to 2 NEW submission crowns for v11 (v10 has 3).
- **Genie3: wave1 DONE (240 backbones), wave2 RUNNING (bo6m428mi, GPUs 1,3,5,6, ~600).** Foreign jobs on
  GPUs 2,4(okc-muse-spark),7 -> avoided. Next: funnel both waves (CA-MPNN -> SC/novelty -> pocket fold
  human+mouse -> switch-install).

## 2026-10-24 f21 switch verdict (beut5xsd4) + exhaustive search + Genie3 funnel started
- **Switch-install verdict on the 2 new crowns (greedy pick):**
  - g7_8_sw2his: bind_min 0.379 ✓, xreact_min 0.205 ✓ (bM 0.205/cM 0.233 BOTH agree!) BUT switch = only
    1 robust His-cation contact (mean 1.0, frac>=2=0.00) = GENTLE single-His, not sharp 2-His. A valid
    gentle-switch x-react crown (better than v10's d417 sw1 hedge), upgrade pending.
  - g6_7_sw2his: bind 0.663 ✓ but xreact LOST (bM 0.014; His install killed mouse binding); no 2-His.
  - Same wall as RFD4 pool: sharp mech-B switch rarely holds on these backbones (only des_25, g5_14 cracked
    it via per-backbone exhaustive search).
- **EXHAUSTIVE His-pair search (b3abp4zty, GPU 5,6,7):** 52 combos (g7_8: 40 anchors K16/20/42/72/82;
  g6_7: 12 anchors K65/104) folded DIFF=5 -> switch_prob, to find a robust 2-His combo preserving x-react.
  runs/f21/exh/. Then confirm bind+xreact DIFF=1 dual-folder on the switch-robust combos.
- **Genie3 funnel stage1 (bswrakrxz, GPU1):** 840 backbones consolidated -> CA-MPNN (ca_model v_48_010,
  design A/fix B, 0-Cys) -> runs/f22/mpnn.csv. Next: self_consistency (ESMFold bb_TM>=0.80 + novelty
  covwTM<0.80) -> pocket Boltz∧Chai human -> binders -> mouse x-react -> switch-install.
- GPU contention HIGH (foreign jobs on 0,2,3,4 incl okc-muse-spark) -> steering to free GPUs only.
- v10 (3 crowns) STILL the baseline. v11 candidates so far: g7_8 (x-react, switch upgrade pending).

## 2026-10-24 4th CROWN confirmed + Genie3 funnel s2 (self-consistency)
- **NEW 4th CROWN: rfd4_g7_8_sw2b_A14_A41** (exhaustive His search cracked it, like g5_14):
  seq STEDEFNSLVDDIHEKINNKDALKTKYKWLYTDLVNSLNHHKSAELAIILLDLYDKNQTDTANELLKAVKEKDYTKAIDILKNSTS (86aa).
  Combo A14H/K20 + A41H/K42: ROBUST 2-His switch (frac>=2=1.00, always 2 contacts) + bind_min 0.513 +
  xreact_min 0.234 (bM 0.234/cM 0.239 BOTH agree) + novel (parent TM 0.74) + soluble (hyd -0.66).
  Matches v10's best crown (g1_133 0.244) on x-react. Alternates (same backbone, pick ONE): 3-His
  _A14_A41_A39 (sharper switch mean2.4, xreact 0.228), _A41_A12 (bind 0.610, xreact 0.223).
  -> v11 will have 4 CROWNS (d25, g5_14, g1_133, g7_8). g6_7 x-react died on His install (dropped).
  NEW SEQ -> portal novelty re-check before upload.
- **Genie3 funnel: MPNN done (840 bb -> 1680 seqs, runs/f22/mpnn.csv).** s2 self_consistency launched
  (sc_shard, ESMFold bb_TM>=0.80 + novelty covwTM<0.80, 7 GPUs) -> runs/f22/sc. NOTE: launched with a
  bad inner '&' -> verify sc_shard alive + relaunch clean if orphaned. Survivors -> pocket Boltz∧Chai
  human -> binders -> mouse x-react -> switch-install -> v11 Genie3 additions.
- **Funnel s2 DONE: 1680 seqs -> 1578 self-consistent (bb_TM>=0.80) + 1076 novel -> 1000 BOTH** (572
  unique backbones). Genie3+CA-MPNN fold back excellently. runs/f22/sc/all.csv.
- **Funnel s3 RUNNING (b9i9m44r8, GPU 1-7):** top 300 by novelty (covwTM 0.555-0.733, 54 robustly novel
  <0.65; deduped best-per-backbone) -> human pocket Boltz + score (runs/f23). Binders (ipSAE>=0.3) then
  go to mouse+Chai x-react -> switch-install. Then assemble v11 = 4 crowns + Genie3 switch-designs,
  replacing v10 no-switch hedges. All new seqs -> portal novelty re-check before upload (USER-GATED).

## 2026-10-24 f23 BREAKTHROUGH: Genie3 -> 6 dual-folder x-react CROWNS
- **Genie3 funnel s3 (runs/f23): 300 novel designs -> human Boltz: 156 binders (52%!), 74 ipSAE>=0.5**
  (far better than RFD4 pool). Top 0.82. Genie3 is the right generator for this flat apical target.
- **Mouse screen (Boltz, reliable) on 156 -> 9 with boltz_m>=0.15 -> Chai dual-folder confirm -> 6 CROWNS**
  (bind_min>=0.3 & xreact_min>=0.15, BOTH folders): w2g5_111 (bind0.418/xr0.325), w2g5_59 (0.520/0.310),
  w2g6_144 (0.707/0.242), w2g1_118 (0.506/0.204), w2g3_19 (0.511/0.194), w2g1_108 (0.583/0.162). Several
  BEAT v10's best crown (g1_133 0.244) on x-react. Targeting the CONSERVED sub-site (202/203/209/210)
  worked decisively. (Bug: first confirm job had $PY unset via '& ' subshell; re-scored clean.)
- **These 6 are PRE-SWITCH.** f24: install_switch + exhaustive His search -> 178 combos -> DIFF=5
  switch-fold search RUNNING (b1of5ruvr, GPU 2-7) -> switch_prob. Robust-switch combos then confirmed
  for bind+xreact retention. Each surviving switch = a v11 Genie3 crown.
- POTENTIAL v11: v10's 3 crowns + g7_8_sw2b + up to 6 Genie3 crowns = up to 10 CROWNS (vs v10's 3).
  Switch-install wall will cull some (RFD4 pattern). All new seqs -> portal novelty re-check (USER-GATED).

## 2026-10-24 f24 RESULT + v11 ASSEMBLED (7 CROWNS, validated PASS)
- **All 6 Genie3 crowns accepted a ROBUST switch** (frac>=2 0.8-1.0) — MUCH better than RFD4 (only g7_8
  cracked). After bind+xreact re-confirm (DIFF=1 dual-folder): **3 CONFIRMED Genie3 switch-crowns** +
  3 switch-binders:
  - genie_w2g6_144_sw3b: bind 0.710, xreact 0.311 (BEST new crown), covwTM 0.676, GRAVY -0.74
  - genie_w2g5_111_sw2b: bind 0.425, xreact 0.254, covwTM 0.640 (2-His; 3-His lost x-react)
  - genie_w2g3_19_sw2b:  bind 0.543, xreact 0.222, covwTM 0.703
  - switch-binders (x-react <0.15): w2g1_118 (0.532/0.146), w2g1_108 (0.582/0.144), w2g5_59 (0.497/0.013)
  All 0-Cys, soluble (GRAVY neg), 3 robustly novel (covwTM<0.68).
- **v11 = submissions/tfr1_track2_v11.csv + _v11_evidence.csv — validate PASS (20/0/0, anarci yes).**
  20 DISTINCT backbones, 7 CROWNS (front-loaded 1-7), ALL valid-switch, 6 Genie3 + g7_8 added, v10
  no-switch hedges (g4_92/g1_15/g0_96/d417) + weakest (g4_66/g4_93/g1_76) DROPPED. Ranked switch(#1,all
  valid)>x-react(#2)>binding(#3). Top crowns beat v10's best (w2g6_144 0.311, w2g5_111 0.254 vs 0.244).
  vs v10: 7 crowns (was 3), 20/20 switch (was 16), +6 fresh Genie3 lineages (robustly novel).
- **7 NEW seqs (6 Genie3 + g7_8) -> portal novelty re-check before upload (USER-GATED).** Genie3 crowns
  robustly novel (low risk). Fallbacks: v10 (portal 20/20), v7. Upload + push USER-GATED.

## 2026-10-24 f25/f26 + v12 FINAL: 10 CROWNS (Genie3 pool exhausted)
- **f25 (remaining 272 novel Genie3 backbones): 158 binders (58%) -> 7 mouse-positive -> Chai confirm
  -> 5 more dual-folder x-react crowns** (w2g3_53 xr0.381 = BEST of campaign, w1g0_112 0.309, w2g5_27
  0.295, w2g3_21 0.254, w2g6_99 ... pre-switch). **ALL 5 took ROBUST switches** (f26, frac>=2=1.00).
  After bind+xreact re-confirm: **3 CONFIRMED switch-crowns** (w2g3_53 bind0.481/xr0.280, w1g0_112
  0.302/0.217, w2g5_27 0.457/0.173) + 2 switch-binders (w2g6_99 xr0.246/bind0.24, w2g3_21 xr0.145).
- **Genie3 pool FULLY EXHAUSTED: 572 novel backbones folded -> 11 binder-level x-react crowns -> 6
  Genie3 switch-crowns total** (3 from f23 + 3 from f25). Genie3 takes His switches cleanly (unlike RFD4).
- **v12 = submissions/tfr1_track2_v12.csv + _v12_evidence.csv — validate PASS (20/0/0, anarci yes).**
  20 DISTINCT backbones, **10 CROWNS** (front-loaded 1-10, ranked by x-react), ALL valid-switch.
  Sources: 9 Genie3 / 6 RFD4 / 5 RFd1; top-10 = all crowns (6 G3, 3 RFD4, 1 RFd1). Ranks 11-20 =
  switch-binders + strongest-binder g5_120 (0.853) + diverse RFd1/RFD4 switch-designs (wet-lab hedge).
  vs v10: 10 crowns (was 3), 20/20 valid-switch (was 16).
- **10 NEW seqs (9 Genie3 + g7_8) -> portal novelty re-check before upload (USER-GATED).** Genie3 crowns
  robustly novel (covwTM 0.64-0.70). Fallbacks: v11 (7 crowns), v10 (portal 20/20), v7. Upload+push USER-GATED.
- CAMPAIGN CONVERGED: pool x-react screen + Genie3 both exhausted; 10 crowns fills the selector's top-10.

## 2026-10-24 v13 FINAL: crowns VALIDATED (decoy false-crown control) + generator-interleaved top-10
- **Red-team (3-agent workflow) + side-agent flagged Genie3 in-silico reliability** (Genie3's lab-real
  TNF binders once scored as failures). Addressed with TWO decision-critical controls, both PASSED:
  1. **Pose-contact (mechanism):** all 6 Genie3 crowns physically bury the CONSERVED sub-site
     (frag 21/22 = UniProt 209/210, + 14/15) in BOTH human AND mouse poses -> x-react is structurally
     realized, not a score artifact. Breaks the mechanism<->score circularity.
  2. **Decoy false-crown control (runs/f27):** 20 de-novo binders designed for OTHER targets (TNF v27 +
     GLP1R, size-matched 62-110 aa) folded through the EXACT pocket-restrained human+mouse metric.
     **human bind>=0.30: 5/20 = 25% FALSE-POSITIVE** (single-folder human binding is a WEAK gate, as
     warned) BUT **FALSE-CROWN (human>=0.30 AND mouse>=0.15): 0/20 = 0%**. Max decoy mouse ipSAE=0.108
     < 0.15 x-react bar < ALL 10 crowns' xreact_min (0.145-0.37). The MOUSE x-react axis is the
     discriminating filter de-novo non-binders cannot fake; every crown clears it above the decoy ceiling.
- **CONCLUSION: all 10 crowns VALIDATED** (statistically via false-crown=0% + mechanistically via pose).
  The "w1g0_112 bind 0.302 in the decoy band" concern is HUMAN-axis only; its crown rests on xreact
  0.217 > 0.108 ceiling = real. So NO crown demoted below a non-crown (evidence removed the distrust).
- **v13 = submissions/tfr1_track2_v13.csv + _v13_evidence.csv — validate PASS (20/0/0, anarci yes).**
  SAME 20 sequences as v12 (byte-identical, reordered). Top-10 = all 10 validated crowns, INTERLEAVED by
  generator: 4 non-Genie3 crowns at PROTECTED ranks 1/3/5/7 (d25 RFd1 #1, g1_133/g7_8/g5_14 RFD4),
  Genie3 at 2/4/6/8/9/10 -> hedges generator-correlation wet-lab risk at the top WITHOUT sacrificing any
  validated cross-reactive crown. Ranks 11-20 unchanged. evidence adds fc_val col (crown>ceiling on all 10).
- **10 NEW seqs (9 Genie3 + g7_8) -> portal novelty re-check before upload (USER-GATED).** Local oracle:
  all novel (covwTM 0.64-0.78 < 0.80 gate). Fallbacks: v12 (=v13 seqs, pre-interleave), v11, v10 (portal
  20/20), v7. Upload + push USER-GATED. CAMPAIGN COMPLETE: both pools exhausted; crowns validated.

## 2026-10-24 v13 PORTAL-VERIFIED — cleared for upload
- **Proteinbase portal on v13: all 20 Passed, "20 included • 0 needing fixes", NO novelty / "similar
  designs" flags.** The 10 sequences new since v10 (9 Genie3 crowns + g7_8) ALL cleared the authoritative
  novelty gate -> confirms the local oracle (covwTM 0.64-0.78) AND confirms Genie3 crowns are novel.
- Portal output BYTE-MATCHED v13.csv: name + rank order (Row2..Row21 = rank 1..20) + seq first12/last8 +
  length, 20/20 exact. Evidence CSV portal col updated: 10 verified(v10) + 10 verified(v13) = 20/20.
- **v13 is CLEARED FOR UPLOAD.** Upload to Proteinbase + git push remain USER-GATED. Fallbacks v12/v11/
  v10/v7 (all portal-verified). CAMPAIGN COMPLETE: crowns validated (decoy false-crown 0/20) + novel (portal).

## 2026-10-27 WAVE-4 launched — deepen the proven crown recipe (ambition-lift, autonomous)
- Decision: idle 8xH100 + 5 days to deadline + v16 locked as floor + frozen judge => fresh generation is
  asymmetric-EV (can only match/beat v16). Launched (job b2wjy7b3f, scripts/wave4_drive.sh):
  Genie3 conserved-sub-site (frag 14,15,21,22 = UniProt 202,203,209,210), 3200 backbones (33% deeper than
  the v15 wave of 2400), FRESH seeds 31000-31007 -> funnel (MPNN -> ESMFold SC+novelty -> human Boltz
  screen) -> FROZEN crown screen (crown_screen_2stage, dual-folder Boltz+Chai ipSAE_min) -> runs/f35/crown.
- Devil's-advocate REVISION (CLAUDE.md mandate): DROPPED the extended-footprint arm. Frag 16,20,23,24
  (=UniProt 204,208,211,212) are the 4 human<->mouse DIVERGENT residues -> conditioning Genie3 on them is
  XR-negative by construction (not ambiguous). All firepower -> the conserved-sub-site recipe that actually
  crowns + cross-reacts. Anthropic's footprint-COUNT rho=0.07 is about size, not deliberately targeting
  divergent positions, so it doesn't rescue that arm.
- Post-crown plan (pipeline confirmed ready): install_switch.sh -> robust re-fold (DIFF_SAMPLES=6) ->
  switch_prob + justhispka_switch -> novelty_struct (max-TM <0.80 safe) -> dedup vs v15/v16 -> v17 ONLY if
  genuine-switch+novel+robust NEW crowns beat v16's weak tail (e223_m3 XR 0.012, rfd4_g1_133 XR 0.120,
  weak/dead switches). v16/v15/v14/v13 stay intact as fallbacks. Upload + push remain USER-GATED.

## 2026-10-27 ADVERSARIAL REVIEW (workflow wd4wlu16z, 4 agents, repo-grounded) -> plan revised
- KILL Wave-5 (partial diffusion). DECISIVE: the project ALREADY ran PD this campaign (progress.md
  2026-10-21 des_160): DUD - children inherit parent novelty; "needs a ROBUSTLY-novel (<0.65) parent,
  which I don't have." All 3 Wave-5 seeds are 0.69/0.831/0.846; the two top-XR ones are the WORST on
  novelty. partial_T=10 + noise_scale_ca=0 => children ~= parent => fail <0.80 gate AND become the
  look-alikes that trip the "similar designs" flag. The ~0.40 XR CEILING is EPITOPE BIOPHYSICS (apical
  patch keeps only 3/9 residues in mouse, loses 2 basics) NOT a backbone property -> no perturbation can
  break it. SELF-CORRECTION: my prior claim that PD was the "best shot at XR>0.40" was WRONG.
- Joint human+mouse MPNN third lever: NO-GO (already ran, runs/jxr: 1 crown XR 0.235 < its v16 parent 0.315).
- "Replace all 20": EV-NEGATIVE. Discards v16's lineage diversity (3 RFD4 + 1 RFd1), maximizes similar-
  designs risk, re-exposes every row to the novelty gate before a user-gated deadline upload. WINNING move =
  keep the portal-verified genuine-switch CORE + swap the weak/redundant TAIL (ranks 16-20) with Wave-4's
  distinct new crowns + ADD the missing structural-diversity gate. Realistic: ~5 slots, more iff Wave-4/RFd3
  deliver distinct crowns that beat core members on key+novelty+distinctness.
- DIVERSITY RULE (corrected): STRUCTURAL pairwise Foldseek TM<0.60 across the 20 (NOT a per-generator cap -
  that would reject 8+ distinct Genie3 crowns). fold_diversity.py on v16 -> 15 distinct folds/20; the 5
  duplicates are each a weak-tail design sharing a fold with a top-10 member (genie_w2g3_53~w3g7_240/w3g5_231;
  genie_w1g0_112~w3g6_93; w3g0_218~w3g7_6; rfd4_g1_133~w3g5_264). Portal ALREADY passed these 20 (v15) => TM
  0.60 is conservative vs the portal; portal is authority. Replacing the weak tail -> 20 distinct folds.
- NEW orthogonal lever REPLACING PD: RFd3 (all-atom; "broke the flat-polar wall" ~0.4% per memory) for
  genuine NON-Genie3 distinct crowns + lineage balance. Queue AFTER Wave-4, CONDITIONAL on a smoke test
  (runs + produces docked backbones here) and yield. v17 selection = synthesis spec (gate switch-GENUINE+
  crown+novelty<0.80 -> TM<0.60 greedy fill -> lexicographic switch>XR>bind -> ship iff beats a v16 member).
- #1 row (49% wt): keep w3g6_146 (XR 0.397, already PORTAL-CLEARED in v15 so its local 0.831 is not a true
  risk); hold w3g5_70 (0.69, novel) as #1 fallback. Any Wave-4 crown takes #1 only if it beats on key AND <0.80.

## 2026-10-27 (later) — WAVE-4 CROWNS: the ~0.40 XR "ceiling" did NOT hold under deeper search
- Wave-4 (b2wjy7b3f, 3200 Genie3 backbones seeds 31000-31007) -> funnel -> FROZEN crown screen (runs/f35/crown):
  **37 crowns** (bind>=0.30 & XR>=0.15, dual-folder Boltz+Chai min, pocket-restrained). 11 at XR>=0.25, 5 at
  >=0.30, and **3 ABOVE 0.40**: w4g3_21 (XR 0.483, BIND 0.447), w4g1_208 (XR 0.426, BIND 0.673),
  w4g1_195 (XR 0.416, BIND 0.462). This DIRECTLY refutes my just-stated "XR ~0.40 is an unbreakable
  biophysical ceiling." CORRECTION: the ceiling was an artifact of shallow sampling, not a hard wall. A
  deeper 3200-backbone search found backbones the dual-folder screen scores >0.40 on mouse. (v16 best was
  w3g6_146 XR 0.397.) Honest caveat: still in-silico ipSAE; magnitude carries co-folder-calibration risk.
- POSE CHECK (scripts/pose_subsite.py, fragment-aware, CONS={14,15,21,22}=UniProt 202/203/209/210,
  DIV={16,20,23,24,183}=204/208/211/212/371): refutes the OFF-EPITOPE-artifact explanation. Every high-XR
  crown sits on the apical patch and contacts the CONSERVED anchors in BOTH species (mouse cons=2-3 incl.
  15/21/22). So high mouse ipSAE is on-epitope + conserved-anchored, NOT nonsense-pose drift. RESIDUAL RISK
  (honest): all crowns ALSO contact the divergent residues -> the mouse score rests on the co-folder scoring
  tolerance of the mouse substitutions (R208->N etc.). That is the real in-silico uncertainty, unprovable
  until wet-lab; dual-folder min is our best hedge.
- SWITCH INSTALL (scripts/install_switch.sh on the 36 crowns): 68 switched variants (each crown sw2his and,
  where >=3 separated buried cations, sw3his) -> runs/f35/switch/switched.csv. Switched seq is the SUBMITTABLE
  form (His substitutions change binding).
- ROBUST RE-SCREEN launched (b2r3o0b1z, scripts/wave4_rescreen.sh): 68 switched + 6 top raw crowns (as _RAW
  controls to separate "ceiling wrong" from "switch install cost XR") -> DIFF=6 dual-folder Boltz+Chai,
  pocket-restrained, all 8 GPUs (boltz_h[0,1] boltz_m[2,3] chai_h[4,5] chai_m[6,7]); switch_prob from the
  Boltz human DIFF=6 replicate fold in the same pass. -> runs/f35/rescreen/rescreen_table.tsv.
- NEXT after re-screen: JustHisPKa on switched survivors (genuine-switch tier gate) -> novelty_struct
  (ESMFold max-TM, HARD portal gate; these w4 seqs are UNSEEN by portal) -> fold_diversity (TM<0.60 vs each
  other + v16 core) -> build v17 iff a switched Wave-4 crown beats a v16 member on switch/XR/novelty/distinctness.

## 2026-10-27 (later still) — ROBUST re-screen + novelty + diversity TEMPER the headline; same-batch comparison launched
- ROBUST DIFF=6 re-screen of the 68 switched + 6 raw controls (runs/f35/rescreen): the raw "3 above 0.40"
  shrank to **1** (w4g1_195 raw 0.434). w4g3_21 0.483->0.344, w4g1_208 0.426->**0.120** (non-robust samples).
  Lesson reaffirmed: a single-screen XR is noisy (~0.14 swing); only DIFF=6 dual-folder is trustworthy.
  22 SWITCHED crowns survive robustly. Switch install costs ~0.08 XR -> best SUBMITTABLE Wave-4 crown
  w4g1_195_sw2his XR 0.352 (BELOW v16 champion w3g6_146 0.397 as measured earlier -> see same-batch caveat).
- NOVELTY (novelty_struct, single-seq ESMFold max-TM vs PDB; runs/f35/sel/novelty.csv): 12/22 novel(<0.80),
  7 borderline(0.80-0.90), 3 RISK(>0.90). The two HIGHEST-BIND crowns FAIL novelty (w4g3_109 BIND 0.82 @0.96;
  w4g1_208 BIND 0.66 @0.94) -> unsubmittable. w4g1_195 (champion XR 0.352) is borderline @0.825. Best
  NOVEL+strong: w4g3_155_sw2his (XR 0.274/BIND 0.702/nov 0.697), w4g7_217_sw3his (0.272/0.492/0.767),
  w4g2_174_sw3his (0.259/0.377/0.664), w4g1_286_sw3his (0.267/0.547/0.788).
- MUTUAL DIVERSITY (fold_diversity single-seq TM<0.60; runs/f35/sel/w4div): 13 distinct folds/22. KEY:
  cluster 1 ties w4g3_155 ~ w4g1_286 ~ w4g2_351 (same fold) -> pick ONE (w4g3_155, best). >=6 DISTINCT-fold
  novel crowns available for the tail swap -> ample.
- V16.csv BUG FIXED: w3g5_249's sequence had a trailing newline (forced CSV quoting; my awk corrupted it in a
  first combined set). Rewrote v16.csv with a proper CSV writer (whitespace-only change to 1 seq, biological
  seq unchanged; .prebakfix backup). Validator PASS, 20 rows. First batch re-score (bbh358zg9) KILLED for the
  corrupted input; GPUs cleaned.
- SAME-BATCH COMPARISON (side-agent's valid-comparison fix, correct): re-scoring all 20 v16 members + 19
  submittable Wave-4 crowns in ONE identical DIFF=6 dual-folder batch (ba8o5hiim -> runs/f35/batchcmp/rescore)
  so keep-or-swap rests on one set of dice, not two runs (XR noise ~0.14 >> the 0.05 gap it would decide).
- PENDING: justhispka (bnhfi5z9r, switch-genuineness tier) + same-batch table + v16 single-seq models for
  cross-set TM<0.60 -> then build v17 (keep validated core, swap weak tail w/ best distinct-fold novel
  genuine-switch Wave-4 crowns, 20 distinct folds, re-rank) IFF strictly stronger than v16 on same-batch numbers.

## 2026-10-27 — JustHisPKa: ALL 22 Wave-4 switched crowns are GENUINE switches; swap plan firmed
- JustHisPKa (runs/f35/sel/switch_justhispka.tsv): 22/22 GENUINE. Strongest: w4g2_174_sw3his (3 in-window,
  swing 2.42), w4g2_351_sw3his (1.79), w4g3_155_sw2his (3 in-window, 1.63), w4g5_147_sw3his (1.33). Switch
  gate does NOT narrow the field (good) -> binding + novelty + distinctness are the discriminators. Per
  lesson-switch-magnitude-not-rankable: swing is a TIER, not a fine ranker.
- v16 WEAK/DEAD-switch tail (replaceable, from v16 evidence): #16 genie_w2g3_53 WEAK(0.31), #17 w3g0_218
  WEAK(0.32), #18 genie_w1g0_112 DEAD(0.00), #20 e223_m3 DEAD(0.00, XR 0.012 non-crown), #19 rfd4_g1_133
  GENUINE but XR 0.120 non-crown (RFD4/RFd1 hedge). RFD4 lineage STAYS in core at #9 rfd4_g7_8 + #11
  rfd4_g5_14 (both GENUINE) -> replacing weak #19/#20 keeps lineage diversity.
- Wave-4 swap pool (novel<0.80 + GENUINE switch + distinct fold, same-batch XR pending): w4g3_155_sw2his
  (XR 0.274/BIND 0.702/nov 0.697/swing 1.63), w4g7_217_sw3his (0.272/0.492/0.767/0.70), w4g2_174_sw3his
  (0.259/0.377/0.664/2.42), w4g3_380_sw2his (0.228/0.604/0.692/1.11), w4g0_194_sw2his (0.231/0.460/0.68/0.92),
  w4g5_147_sw3his (0.225/0.638/0.672/1.33). cluster-1 cousins (155/286/351) -> keep only w4g3_155.
- GATED on ba8o5hiim (same-batch DIFF=6 of 20 v16 + 19 Wave-4): finalize keep/replace boundary on ONE set of
  dice, then v16 single-seq ESMFold (fill 8 blank novelties + unified TM<0.60 diversity) -> build_v17 ->
  ship IFF strictly stronger than v16 on same-batch numbers. Upload + push remain USER-GATED.

## 2026-10-27 — CRITICAL: v16's XR ranking rests on NON-REPRODUCIBLE numbers; robust n=4 campaign launched
- SAME-BATCH DIFF=6 (runs/f35/batchcmp/rescore, 20 v16 + 19 Wave-4, one batch): the picture INVERTS vs v16's
  evidence. v16 #1 FLAGSHIP w3g6_146 evidence-XR 0.397 -> same-batch 0.177 (-0.22). v16 "weak tail"
  genie_w2g3_53 -> TOP XR 0.379 (but WEAK switch -> stays demoted by objective #1). v16 "core" w3g5_70 0.320->
  0.102, w3g6_93 0.259->0.062, w3g0_290 0.197->0.012, w3g5_264 0.220->0.012 (now NON-crowns). Others rose:
  w3g5_231 0.257->0.367, genie_w2g6_144 0.315->0.374.
- REPRODUCIBILITY TEST (two independent DIFF=6 runs of the 19 Wave-4): mean |dXR|=0.029, 17/19 within 0.06.
  => the DIFF=6 pipeline IS reproducible (~0.03); v16's evidence XR came from a DIFFERENT/less-robust
  measurement and does NOT reproduce. The side-agent was right: v16 numbers vs fresh numbers are not
  comparable; the SAME-BATCH numbers are the trustworthy ones. CONSEQUENCE: v16's front-loading (49%/39%) is
  mis-ordered on the robust metric (its #1 is actually mid-pack XR).
- A few designs are genuinely HIGH-VARIANCE (unreliable): w4g1_286_sw3his 0.267->0.014; w3g6_146 0.397->0.177.
  Prefer the stable sister (w4g1_286_sw2his) / demote high-std designs from front ranks.
- STRATEGY REFINED (honest): XR is NOT finely rankable (ties < ~0.08 are noise) and the organizers' blind
  judge can't localize the apical epitope either. So DOMINATE = portfolio of ROBUST genuine-switch crowns
  (high crown-rate across folds + strong mean), maximally DIVERSE (folds+lineages, the scored axis), with
  FRONT-LOAD by CONFIDENCE (robust mean + low variance + genuine switch + novel + on-epitope), not by a
  single lucky XR. This REBUILDS the ranking, not just the tail.
- ROBUST n=4 CAMPAIGN (bih4fmqox, scripts/wave4_robust.sh): 3 more DIFF=6 batches of the combined 39 with
  independent Chai seeds 1/2/3, pooled with batchcmp(seed0) -> runs/f35/robust/robust_xr.tsv (per-design
  xr_mean, xr_std, crown_rate, bind_mean). Then: v16 single-seq ESMFold (novelty for 8 blanks + unified
  TM<0.60 diversity) -> build_v17 on robust stats. Upload+push USER-GATED.

## 2026-10-27 — ROOT CAUSE FOUND + v17 BUILT: v16 XR was MAX-of-samples; v17 re-ranks on robust MEAN
- SMOKING GUN (runs/f33 per-sample data for w3g6_146): its mouse XR across replicate folds = {0.000, 0.3975,
  0.0118, ...}. v16 recorded **0.397 = the MAX**. My wave4_rescreen takes the MEAN across DIFF=6 samples
  (score_ipsae.py line 67-68: st.mean over samples; per-sample standard symmetric-max ipSAE) -> w3g6_146
  robust MEAN ~0.19 (stable, std 0.013). => v16's XR ranking was MAX-of-samples (optimistic, small-n noise),
  over-ranking spiky designs (w3g6_146, w3g5_70, w3g0_290) and under-ranking consistent ones (w3g2_70,
  genie_w2g6_144). Devil's-advocate ("maybe MY pipeline is broken") ANSWERED: my rescreen matches the frozen
  crown-screen on Wave-4 (w4g1_195 0.416 vs 0.434) and is internally consistent across all 39. The organizers
  judge with ipSAE_MIN across folders + ensemble (CONSERVATIVE) -> robust mean aligns with them, max does not.
- v17 BUILT (submissions/tfr1_track2_v17.csv, validator PASS 20/0/0). Ranked by confidence-adjusted robust XR
  (mean - 0.5*std, n=2 V16 / n=3 W4 same-pipeline DIFF=6). #1 w3g2_70 (robust 0.349, std 0.001, GENUINE,
  BIND 0.65, portal-cleared) REPLACES w3g6_146 (robust 0.19, demoted to #14). 8 NEW Wave-4 genuine-switch
  distinct-fold crowns added (ranks 2,6,7,8,9,10,11,12); 8 dropped (genie_w2g3_53 WEAK despite top XR 0.356,
  w3g0_218 WEAK, genie_w1g0_112 DEAD, e223_m3/w3g5_264 non-crowns, w3g6_93/w3g7_6 cousins, rfd4_g1_133 low-XR).
  All 20 GENUINE switches. 19/20 distinct folds (MAX achievable — the 3 unused clusters hold only
  novelty-risk/non-crown designs; one cousin pair w3g5_231~w3g7_240 both strong crowns). RFD4 lineage kept
  (#13 rfd4_g7_8, #15 rfd4_g5_14). 2 HIVAR designs in the near-zero-weight tail (#17,#20) for fold diversity.
- v17 vs v16 (same robust metric): STRONGER on #1-switch (20/20 genuine vs 17/20), #2-XR front-load (0.349 vs
  0.19 at #1), diversity (19 vs 15 folds). CONDITIONAL on the 8 NEW designs passing the portal novelty check
  (6 safe <0.80: w4g1_286/w4g7_217/w4g2_174/w4g3_380/w4g0_194/w4g5_147; 2 borderline: w4g1_195 0.825,
  w4g5_137 0.806). v16 members all portal-cleared (v15). Scripts: build_master_v17.py, build_v17.py,
  wave4_rescreen.sh(+seed), wave4_robust.sh, pose_subsite.py. Fallbacks intact: v16/v15/v14/v13.
- PENDING: portal novelty check on the 8 NEW (USER-GATED upload); optional n=4 top-up (foreign BoltzGen job
  intermittently holds the shared box; n=2-3 mean already decisive vs v16's max).

## 2026-10-27 — v17 PORTAL-VERIFIED (20/20 Passed) — CLEARED FOR UPLOAD (user-gated)
- Proteinbase portal on v17 (owner paste): "20 included • 0 needing fixes"; EVERY row Passed; NO novelty or
  "similar designs" flags. Both borderline-novelty NEW designs cleared (w4g1_195 @row4, w4g5_137 @row16), and
  the 8 new Wave-4 designs + the 19/20-distinct-fold set passed the authoritative similarity gate.
- BYTE-VERIFIED submitted==validated: all 20 portal sequences match submissions/tfr1_track2_v17.csv by row
  order + length + head/tail. v17 is the RECOMMENDED deliverable. Fallbacks v16/v15/v13 intact.
- The only remaining step is the owner's upload click (USER-GATED). Nothing else pending.

## 2026-10-27 — SCORING METHOD VERIFIED (fresh primary source, not memory): organizers use AVERAGE ipSAE
- A side-agent correctly flagged that the v16->v17 mean-vs-max re-rank rested on a MEMORY of the scoring
  rule. Fresh web read of Adaptyv's own competitions: "the leaderboard was built from AVERAGE ipSAE score,
  computed via Boltz2" (Nipah); ipSAE is noisy across seeds/hardware and Adaptyv says the unpredictability
  is INTENTIONAL (anti-metric-gaming). The Anthropic autonomous-binder report (this competition family) used
  ESMFold2 + ipSAE_min + self-consistency DockQ. Local captured rules agree: ipSAE_min worst-case {human,
  mouse}, "never a single folder" (configs/target.yaml:111, docs/RECON.md:111, docs/METHODS.md:25).
- => v17's robust-MEAN ranking is ALIGNED with the organizers' AVERAGE-ipSAE scoring; v16's MAX-of-samples
  was mis-aligned. Under single-fold scoring the mean is still EV-optimal (mean = E[single draw]); only a
  "best-of-many" scoring would favor max, which contradicts the verified average/worst-case/never-single ethos.
  The #1 pick w3g2_70 (mean 0.349, std 0.001) scores ~0.35 under ANY aggregation -> robustly optimal front row.
  Reorder CONFIRMED (not just asserted). Sources: adaptyvbio.substack.com leaderboard posts; Anthropic Claude
  Science autonomous-binder report.

## 2026-10-27 — AMBITION-LIFT: complete every-metric matrix + SOTA scout -> v18 (objective-#1-first reorder)
- GOAL (user /ambition-lift): overhaul the 20 if evidence supports; deep-research the SOTA; benchmark every
  design against every metric; deliver the strongest set, trade-offs explicit, never fabricate.
- SOTA SCOUT (background workflow `tfr1-sota-scout`, 18 agents = 4 research + 13 adversarial-verify + synth,
  filtered vs the project NO-GO ledger): 13 candidates, **0 survivors -> CONFIRM CURRENT STACK**. Every
  generator (Odin-Multi/BindCraft AF2-halluc, PXDesign, BoltzGen, PPIFlow, Proteina-Complexa) hits the
  flat-apical wall or fails the hard novelty gate; every MPNN-reseq / protonation lever (Proton-PottsMPNN,
  PPIFlow maturation) reduces to the re-sequencing NO-GO (interface PAE 8->26; joint human+mouse MPNN XR
  0.235<0.315 parent, re-confirmed on disk in runs/jxr); every extra co-folder / His-pKa predictor
  (Protenix-v2, pKALM/GNN-GAT, Chamaileon) is a correlated/duplicate or state-invariant vote. Both top
  objectives sit at HARD CEILINGS no days-runnable method removes: #1 switch MAGNITUDE is in-silico-unrankable
  (His-pKa err 2-3u >> the 1.4u window -> only a coarse genuine/weak/dead + in-window COUNT is trustworthy);
  #2 mouse-XR ~0.40 is an epitope-biophysics ceiling (only 202/203/209 are mouse-identical). Independently
  reproduces the project's own NO-GO ledger. => no new DESIGN or METHOD beats the cleared set; the residual
  lever is the RANKING.
- COMPLETE EVERY-METRIC MATRIX (the depth lift): developability panel for all 20 (results/
  developability_tfr1_track2_v17.csv) + JustHisPKa per-His pKa / n_inwindow for the 8 Wave-4 members
  (runs/bench/switch_justhispka_w4.tsv -- SAME Boltz ON-state structure as runs/f35/sel, so the identical pKa
  confirm the pipeline is deterministic, NOT an independent 2nd fold). The matrix's one NON-NOISE discriminator
  beyond v17's axes is developability: w4g3_380 (v17 #9, INSIDE the tested top-10) is the only SEVERE
  expression risk (net charge -15 charge-blob + hydrophobic run).
- DEVIL'S-ADVOCATE (cold agent, P(mistake)=70%) + the SOTA scout + repo doctrine CONVERGED to kill an
  over-reach: an initial v18 reordered the gated crowns by a JustHisPKa n_inwindow "switch tier" (promote
  n_inwindow>=2; demote w4g7_217 n_inwindow=0; w4g2_174 #8->#5). That is CHURN -- within the genuine set the
  switch is NOT finely rankable (His-pKa err 2-3u >> the 1.4u window; n_inwindow is boundary-brittle:
  w4g7_217's His at 7.56/5.70 are within the 0.4 MUE of the window edges, so n=0 could be 2; the promoted
  designs are equally fragile), so it TRADES the reliable axis (XR, obj #2) for noise. CORRECTED mis-citation:
  "49%/39%" is POSITIONAL front-load weight (rank-1 vs top-10), NOT an objective-#1 weight; obj #1 is a GATE
  (all 20 GENUINE) so the correct WITHIN-gate order is by obj #2 (XR) = exactly v17's order. The switch-tier
  reorder AND a mooted w4g3_155-for-w4g1_286 swap (both rest on the same boundary-noisy switch signal;
  w4g3_155 also has LOWER XR 0.238<0.270) were RETRACTED.
- v18 BUILT (scripts/build_v18.py; submissions/tfr1_track2_v18.csv + _v18_evidence.csv; validator PASS 20/0/0)
  = v17's XR-first order with EXACTLY ONE evidence-backed change: demote the single SEVERE-expression design
  w4g3_380 from #9 to #11 (out of the likely-tested top-10), promoting the clean, ~equal-XR w4g5_147 (0.225 vs
  0.229) in. Only 3 rows move (w4g0_194 #10->#9, w4g5_147 #11->#10, w4g3_380 #9->#11); top-8 BYTE-IDENTICAL to
  v17. **PURE REORDER of v17's 20 -> inherits v17's portal 20/20 verification, zero new risk.** HONEST
  HEADLINE: the portfolio was already at the biophysical ceiling (scout: no new design/lever beats it; XR
  ~0.40 epitope-capped; switch only coarsely gateable) -> the one defensible improvement is this
  developability demotion, NOT a big overhaul.
- SWITCH-RESCUE SUCCEEDED (frontier win, AGAINST the physics prediction) -> v19. Relocating genie_w2g3_53's
  buried-His switch off its pKa-depressed positions (buried_switch_scan -> exhaustive_switch -> 24 combos ->
  guarded wave4_rescreen, runs/f37_rescue) produced genie_w2g3_53__A13HR44_A31HK8, validated on EVERY axis
  (same pipeline as the pool): robust mouse XR 0.394 +/- 0.007 over n=3 independent seeds (min 0.385) -- BEATS
  the whole v17/v18 pool (prior best 0.349) AND the soft ~0.40 ceiling; JustHisPKa GENUINE 2-in-window
  CONFIRMED across 2 folds (seed7 6.67/6.39, seed1 6.70/6.02), swing 1.41-1.47, sw_frac 1.00; bind 0.421; dev
  CLEAN (liability 0, 0-Cys); mouse pose anchored on CONSERVED 203+209 in both mouse folds; novelty 0.778
  (novel, == parent genie_w2g3_53_sw2b's PORTAL-VERIFIED 0.776; same fold, ~94% seq id). => the ~0.40 XR
  "ceiling" was a soft property of the UN-rescued pool, not a hard limit -- a targeted His-placement search on
  the highest-XR backbone broke it. (The parent was dropped earlier for a WEAK switch, not low XR; the rescue
  fixed the switch while keeping/raising the XR.)
- v19 BUILT (scripts/build_v19.py; submissions/tfr1_track2_v19.csv + _v19_evidence.csv; validator PASS 20/0/0):
  v18 with the rescue winner REPLACING w4g1_286 (same fold cluster 2; XR 0.270, 1-in-window) and ranked #1 by
  XR (0.394 > w3g2_70's 0.349; both 2-in-window switches). 19/20 sequences BYTE-IDENTICAL to the portal-verified
  v18/v17 set; the winner is the ONLY new sequence (portal CHECK -- its fold was cleared in v15, so a pass is
  expected). 19 distinct fold clusters (diversity preserved). This is the genuine top-rank OVERHAUL the
  ambition-lift was for -- a better DESIGN, not just a reorder.
- DELIVERABLE STACK: v19 (RECOMMENDED, strongest) > v18 (fully portal-verified fallback = v17 seqs + the
  SEVERE-dev demotion) > v17 (portal-verified 20/20) > v16/v15/v13. Upload + push remain USER-GATED.

## 2026-10-27 — v19 PORTAL-VERIFIED 20/20 (owner paste) — CLEARED FOR UPLOAD (user-gated)
- Proteinbase portal on v19 (owner paste): "20 included, 0 needing fixes"; EVERY row Passed, including the
  NEW switch-rescue winner genie_w2g3_53__A13HR44_A31HK8 (Row 2) — it CLEARED the hard novelty gate (as
  expected; its fold was portal-cleared in v15). The only remaining gate is closed -> v19 is fully portal-verified.
- BYTE-VERIFIED submitted==validated: all 20 portal rows match submissions/tfr1_track2_v19.csv by name + row
  order + length + head/tail (PASS). Net of the ambition-lift: a genuinely BETTER design (the rescue winner
  beats the entire prior pool on cross-reactivity 0.394>0.349 while matching the top 2-in-window switch) now
  sits portal-cleared at #1. Remaining: owner's upload click + git push (both USER-GATED); checkpoint committed.

## 2026-10-27 — Rules reconciliation (Oct-27 Slack summary, user-relayed) + prescreen cross-check
- KEY REFRAME (Slack, Oct 27): the HARD ENTRY GATE is the `adaptyvbio/binder-prescreen` tool (release v0.5,
  updated for TfR1 2026-10-27) — "passing the prescreen at submission means the design has entered." The
  **Proteinbase NOVELTY SCORE is INFORMATIONAL, NOT an exclusion criterion** (contra the long-held "novelty
  hard-gate level>=3" framing). Novelty is still a displayed ranking input the Claude-selector values, so keep
  it high — but it cannot exclude. The portal's per-row "Passed / 0 needing fixes" IS the prescreen result ->
  v19 already passed the authoritative gate.
- PRESCREEN STRUCTURE (PRESCREEN_SPEC.md v0.5): two arms. TARGET arm (no downloads) = whole-seq composite,
  >=8-aa verbatim containment, and binding-region vs the curated known-binder set; for NON-ANTIBODY
  miniproteins (our class) it flags `known_target_binder` (composite>=0.90), `verbatim_target_fragment`
  (>=8 aa of a named/confirmed binder), or `target_binder_homolog` (whole-seq id in [0.70,0.90)). PRIOR-ART
  arm = MMseqs vs PDB/SwissProt/PLAbDab/Thera-SAbDab/THPdb/Proteinbase/USPTO (>=0.95 -> known_sequence).
- INDEPENDENT CROSS-CHECK (data-only, my own code reading the tool's tfr1_binders.fasta = 6695 known binders;
  did NOT execute the external tool — permission-gated): all 20 of v19/v18/v17 show ZERO >=8-aa verbatim
  fragment and max homology-proxy (5-mer containment) = 0.03 -> no target-arm flag. Confirms the portal pass.
  (Prior-art arm needs the 4.6GB corpus build + runs the external tool, both out of scope here; the portal
  already ran the full prescreen, and de-novo seqs with structural novelty <0.80 can't be >=95% public id.)
- COMPLIANCE (v19 vs the Oct-27 rules): PASS — 0 unpaired Cys, len 62-109 (10-250), molecule_class=protein,
  unique names, 3-col CSV row-order=ranking, de-novo (His-switch on OUR OWN designs, not modified known
  binders), switch direction bind-7.4/release-6.0 (confirms the ProtonPottsMPNN NO-GO: it does the REVERSE).
  Minor notes (not blockers): all 20 share the apical epitope + protein class (epitope/class diversity is a
  rewarded axis we don't spread); non-Met-starting designs get an auto-Met we didn't fold with (far N-term,
  off-interface). Tool has registered targets tfr1/tnfa/glp1r/kras-pmhc -> same gate for Challenges 2/3/4/5.

## 2026-10-27 — F38 non-mimetic moonshot campaign (/ambition-lift "drastic moonshots") -> NO CHANGE; v19 STANDS
OUTCOME: an exhaustive moonshot campaign found NO design that strictly dominates the v19 rank-1. v19 is
CONFIRMED at the ceiling and ships unchanged. "Confirm, don't churn." Full raw data in runs/f38_moon/.
- SCOPE (all legitimate, all on the frozen pipeline): (A) extended the switch-rescue (which had only ever
  run on ONE backbone) to 4 backbones (genie_w2g3_53 3-His re-mine, genie_w2g6_144, w3g2_70, w4g2_174),
  112 unique 2-His+3-His candidates, DIFF=6 pocket-restrained dual-folder rescreen -> robust n=3 refold of
  the top 16 (with the incumbent folded on MATCHED seeds) + 2-fold JustHisPKa + pose + novelty + dev;
  (B) bivalent avidity moonshot; (C) first-principles non-mimetic-switch SOTA scan.
- (C) SOTA scan verdict: NO non-mimetic switch chemistry survives (His is the ONLY side chain with intrinsic
  pKa in [6.0,7.4]; reversed-polarity acid / His-His pair / cation-pi / metal all fail validation or physics).
  Separated buried-His STACKING is the 2024-2026 SOTA frontier (Baker bioRxiv 2025.09.29.678932). Confirms
  our approach; the only validatable lever is MORE separated His (= what (A) searched).
- (B) bivalent NO-GO (geometry + biology + kinetics + validatability): apical epitopes 83A apart, outward-
  facing; bivalent TfR1 -> LYSOSOME not recycling (Niewoehner 2014 Brain Shuttle); avidity SLOWS off-rate ->
  fights the pH-6 release (= objective #1). The most "radical" idea is actively counterproductive.
- (A) the apparent winner genie_w2g3_53__A27HK8_A13HR44 looked like a strict dominator (robust mouse ipSAE
  0.448+/-0.027 vs incumbent 0.395, 2-in-window both folds, human 0.501) -> BUT a cold devil's-advocate
  (P=60%) + my own verification KILLED the swap:
    * #2 cross-reactivity is a RATIO (config: mouse_crossreact_ratio_to_1). mouse/human ratio = incumbent
      0.92-0.94 vs challenger 0.85-0.89 (BOTH campaigns) -> the INCUMBENT is more cross-reactive; the
      challenger's higher ABSOLUTE mouse score is a confounded general-affinity bump (XR & BIND co-move,
      same co-folds, rho~0.87), NOT better cross-reactivity.
    * #1 switch is a TIE (incumbent swing 1.38-1.47 >= challenger 1.34-1.44, overlapping) -> not a win.
    * so the challenger's ONLY clean edge is #3 affinity (LOWEST priority; the judge prefers a clear switch
      over a strong binder). Evicting the PORTAL-VERIFIED rank-1 for a noisier (sigma 0.027 vs 0.007),
      un-verified cousin that's worse on the #2 ratio = a backwards trade. REJECTED. build_v20 deleted.
  NEGATIVE RESULTS (honest): g144 "deep-switch" standout COLLAPSED on robust (seed0 0.390 -> n=3 0.298+/-0.066,
  a lucky seed caught by the matched refold); all 3-His triples killed bind (0.03-0.08) or dropped XR; no
  non-g53 backbone beat g53 on cross-reactivity. The exhaustive search CONFIRMS v19 is at the biophysical
  ceiling on this epitope. DELIVERABLE UNCHANGED: v19 (portal-verified 20/20) > v18 > v17. Upload USER-GATED.

## 2026-10-28 — DEVIL'S-ADVOCATE RE-ATTACK OVERTURNS THE f38 REJECTION -> v20 (rank-1 corrected)
GOAL (user /devil-advocate "brutally, then optimistically revise"): attack "ship v19 unchanged; v19 at ceiling".
A cold advocate (claim block only) returned P(MISTAKE)=35% with a KILL SHOT: the obj-#2 metric was applied
INCONSISTENTLY (pool built/sorted by ABSOLUTE mouse ipSAE; the one challenger examined was rejected by the
RATIO). I ran all three checks against the files -> found a REAL, decision-changing BUG, and REVERSED.

THE BUG (methodological, verified): the "cross-reactivity ratio" used to reject A27HK8_A13HR44 in the f38
section ABOVE was `XR/BIND = min(boltz_m,chai_m) / min(boltz_h,chai_h)` -- an INCOHERENT ratio. The mouse-min
and human-min can come from DIFFERENT folders, so it divides mouse-under-one-folder by human-under-another.
For the incumbent this manufactured a spurious "near-1" (0.914): its folders DISAGREE on direction (Boltz
mouse/human 0.776 = human-preferring; Chai 1.384 = mouse-preferring), and min/min paired Boltz-mouse with
Chai-human. Neither folder alone calls the incumbent equipotent.

CORRECT metric = WITHIN-FOLDER mouse/human ratio, per folder, then aggregated (respecting "never a single
folder" by using BOTH). Recomputed from the per-folder ipSAE on disk (f38 rescreen/s1/s2), |ratio-1|:
  design                         Boltz |d|   Chai |d|   worst-case |d|   switch (coarse, >=2 folds)
  A27HK8_A13HR44 (challenger)     0.113       0.120     0.120            GENUINE 2-in-win 2/3 folds
  A13HR44_A31HK8 (incumbent)     0.224       0.384     0.384            GENUINE 2-in-win 2/2 folds
  A27HK8_A18HK52 (advocate pick) 0.226       0.650     0.650            fold-UNSTABLE (WEAK/0-in-win in f37)
  A12HK22_A17HK48                0.202       0.405     0.405            GENUINE (1->2 in-win)
  A13HR44_A59HK21                0.233       0.255     0.255            GENUINE 2-in-win 2/2 folds
=> under EVERY coherent statistic (Boltz-only = organizers' documented Boltz2-avg; Chai-only; worst-case),
A27HK8_A13HR44 is the MOST cross-reactive by a wide margin. NOT a confound: in Boltz it raises the LOW species
(mouse 0.448>incumbent 0.395, human ~tied) and in Chai it raises the LOW species (human 0.527>0.432, mouse
~tied) -> it BALANCES toward equipotency in both, the opposite of a uniform affinity bump. My earlier
"confounded affinity bump" claim was WRONG (it rested on the incoherent min/min ratio).

CORRECTED lexicographic ranking (#1 switch > #2 x-react RATIO > #3 affinity):
  #1 switch: TIE at the coarse gate (both robust GENUINE 2-in-window; pKa err 2-3u >> 1.4u window -> swing/
     fold-count not finely rankable; incumbent 2/2 vs challenger 2/3 is boundary-brittle: challenger f37
     His27 pKa 5.76, 0.24u under the line).
  #2 x-react: CHALLENGER WINS, robustly (|d| 0.11-0.12 vs 0.22-0.38, both folders + worst-case).
  #3 affinity: CHALLENGER >= incumbent (Chai human 0.527>0.432; Boltz ~tied; min-over-folders 0.501>0.431).
  -> A27HK8_A13HR44 OUTRANKS the incumbent. The advocate's SPECIFIC pick (A27HK8_A18HK52) is REFUTED: it is
     switch-UNSTABLE (WEAK, 0-in-window in f37) and the WORST on the coherent #2 ratio -> loses on #1 and #2.

ACTION: built submissions/tfr1_track2_v20.csv = v19 with rank-1 ONLY swapped (incumbent -> A27HK8_A13HR44);
all 19 other designs byte-identical CONTENT (verified by CR-stripped diff), CRLF format matched to the
portal-verified v19, molecule_class protein. Challenger dev CLEAN (68aa, 0-Cys, net charge -0.05, gravy
-0.79, liability 0), novel (singleseq maxTM 0.777 == incumbent portal-cleared 0.778, same backbone). seq
MLTKEEIKKHIEHIAKEHNLKKKLVSHEEWNAQVDAFIEAKLDREAIKESVKAYAELNNGEVLMPKPK.
VERDICT: REVISE. v20 (rank-1 = A27HK8_A13HR44) is the corrected RECOMMENDED deliverable; v19 (portal-verified)
is retained INTACT as the immediate fallback. OPEN (USER): (a) rank-1 reversal confirm + which variant
(clean 1-for-1 swap [built] vs keep incumbent at #2 as a hedge, drop #20); (b) owner re-run the Proteinbase
portal on v20's new rank-1 before upload (near-certain to clear: same backbone/novelty); (c) upload + git push
remain USER-GATED. Honest note: this REVERSES the 2026-10-27 f38 rejection, which rested on the incoherent
min/min ratio -- a genuine bug, not a new opinion; the within-folder fix is robust across 3 folds x 2 folders.

## 2026-10-28 — #1 SLOT LOCKED (3-0 independent adjudication; stop the churn)
A 4-agent adjudication (3 independent lenses: metric-purist / execution-realist / lower-regret-decider + synth,
each RE-VERIFYING the on-disk numbers) returned UNANIMOUS 3-0 for the CHALLENGER (v20 rank-1
genie_w2g3_53__A27HK8_A13HR44), synth confidence 0.80. They even corrected the incumbent's switch record UP to
3/3 2-in-window (f38-s1 1.38, f37-s0 1.41, f37-s1 1.47; my earlier "2/2" undercounted) -- STRENGTHENING the
incumbent on #1 -- and STILL all picked the challenger, because #1 is a coarse TIE (challenger's lone
sub-window reading = His27 pKa 5.76, 0.24u under the 6.0 line, ~10x inside the 2-3u predictor error) so #2
decides, and the challenger wins #2 robustly (within-folder |ratio-1| 0.12 vs 0.38, both folders + common
folds; mechanistically balancing, not an affinity bump). They reproduced the min/min BUG and confirmed it
INVERTS the comparison (buggy: incumbent 0.096 < challenger 0.126) -- the exact artifact behind the earlier
wrong rejection. #3 affinity challenger >= incumbent. Net: challenger WEAKLY DOMINATES.
=> **v20 is FINAL/LOCKED.** DO NOT RE-OPEN on ANY in-silico ground (re-fold, new seed, pKa re-run, switch/
in-window re-read, std/"noisier-cousin" argument, or min/min recompute). Re-open ONLY if: (1) the Proteinbase
portal REJECTS v20's rank-1 -> mechanically fall back to the intact portal-verified v19, NO re-litigation; or
(2) NEW wet-lab / validated-method data reverses a ranked axis (not expected before Nov-1 AoE). The slot flipped
3x; THIS IS THE LAST CHANGE. Protocol: owner runs the portal on v20 ONCE (near-certain: same backbone, same top
hit 8twa, novelty 0.777 vs cleared 0.778, 0-Cys), then freeze; v19 kept as labeled fallback. Upload+push USER-GATED.

## 2026-10-28 — v20 PORTAL-VERIFIED 20/20 (owner paste) — LOCK HOLDS; CLEARED FOR UPLOAD
Owner ran the Proteinbase portal on v20: "20 included • 0 needing fixes"; EVERY row Passed, including the new
rank-1 genie_w2g3_53__A27HK8_A13HR44 (Row 2, Single chain, Passed, 68 aa); NO novelty/"similar designs" flags.
BYTE-VERIFIED submitted==validated: all 20 portal (name, length, ORDER) identical to submissions/tfr1_track2_v20.csv
(CR-stripped diff clean); rank-1 head12 MLTKEEIKKHIE / tail8 EVLMPKPK / len 68 match. => the lock's only live
reopen condition (portal REJECTS v20 rank-1) resolved IN FAVOUR; the challenger cleared the same authoritative
gate the incumbent did. **v20 is the FINAL, LOCKED, PORTAL-VERIFIED deliverable (20/20).** v19 retained as the
portal-verified fallback. ONLY remaining step = the owner's upload click (USER-GATED); git push also USER-GATED.

## 2026-10-28 — ORGANIZERS'-JUDGE RE-SCORE (ambition-lift) → v21 REORDER (#1 UNCHANGED + VINDICATED)

**Ask:** owner "/ambition-lift — find any ways to improve/replace designs for a definitive dominating
submission at all costs." Lift chosen (doing mode): score the locked finals by the judge that will
ACTUALLY rank us — the organizers' **blind** Protenix (ESMFold2+Protenix regime) — which our internal
*pocket-restrained* Boltz∧Chai pipeline never applied to the exact final sequences.

**Run:** blind Protenix on 21 designs (v20's 20 + v19 rank-1 twin), human AND mouse, 48 poses/design,
GPUs 2-7 (0-1 foreign-held, untouched). `runs/prot/v20_judge/{human,mouse}.tsv`. Scorer
`scripts/score_protenix_tfr1.py`. ~11 min wall. All 42 folds OK.

**Calibration (the pivot) — POS_3DS18 / NEG_scramble on the SAME blind judge** (`runs/prot/controls_out`):
- `on_epi_rate` is **INVALID**: NEG_scramble2 scored on_epi **1.00** (> the true positive's 0.50). A sticky
  scramble lands on the flat apical epitope as often as a real binder → confirms & refines
  `lesson-tfr1-apical-blind-cofold-fails-poscontrol` (the *localization* fails, not necessarily binding).
- `iptm_max` is **VALID**: POS_3DS18 **0.271** vs NEG **0.121/0.125** — a clean 2.2× separation. So rank on
  blind **iptm_max**, discard on_epi. Natural binder/non-binder break in the design pool at iptm ≈ **0.18**
  (gap 0.194→0.172).

**Findings:**
1. **#1 LOCK VINDICATED.** genie_w2g3_53__A27HK8_A13HR44: blind human iptm **0.260**, mouse **0.243** →
   within-folder ratio **0.93** (best both-species balance in the pool); beats the v19 twin (0.260 vs 0.233,
   mouse 0.243 vs 0.231) on this independent third folder. The 3-0 adjudication holds on the organizers' judge.
2. **v20's xr-sorted order front-loaded blind-WEAK designs.** #2 `w3g2_70` (highest xr 0.349, highest Boltz
   bind) is blind iptm **0.167** (gate-fail — its strength is a pocket-restraint artifact the organizers'
   blind judge misses). Several genuine-switch designs strong on BOTH judges sat at ranks 7-19.
3. **Mouse blind = undifferentiated** (iptm ~0.13-0.26, near the human-NEG floor for all; no mouse POS to
   calibrate) → the blind judge gives NO #2 reorder signal; mouse cross-react stays as the known fragile axis.

**Action → `submissions/tfr1_track2_v21.csv` (RECOMMENDED).** Pure reorder of v20 (IDENTICAL 20 sequences,
#1 unchanged) by a transparent max-min rule respecting lexicographic priority: human-binding is the GATE
(AGENTS.md: #2 only counts among human-binders), so GATE_PASS (blind iptm ≥ 0.18) ranked above GATE_FAIL,
each group by the validated Boltz∧Chai **xr_mean** (#2 ranker). `scripts/build_v21.py`;
`submissions/tfr1_track2_v21_evidence.csv` has all axes per design. validator PASS 20/0/0. Diversity preserved
(all 20 are distinct folds, TM<0.60). v20 kept intact as the portal-verified fallback (validated-pipeline order).

**Limitations (honest):** n=1 positive control; used blind **iptm** (calibrated) as the ipSAE_min proxy
(Protenix PAE not dumped → true ipSAE would need a re-fold, low marginal value — iptm/ipSAE correlate and the
0.18 break is clean); the `w3g2_70` #2→#13 demotion is the one judgment call (validated-pipeline star vs
blind-judge weak) — flagged, and it sits in low-weight slots. **Upload USER-GATED** (v21 recommended, v20
zero-risk fallback). Not pushed (push remains user-gated).

**2026-10-28 — SECOND FOLDER (ESMFold2) COMPLETES THE ORGANIZERS' JUDGE → v21 CONFIRMED.** A side-agent
flagged that the organizers use TWO folders (ESMFold2 + Protenix) and I'd run only Protenix. Correct flag;
addressed. ESMFold2's role here is **monomer self-consistency / foldability** (our setup is monomer-native;
multimer infer errors — ESMFold is not an interface predictor), i.e. the sc-DockQ-adjacent "folds as designed"
component, complementary to Protenix's interface ipSAE. Ran ESMFold2 monomer on the 20 finals + the SAME
POS/NEG controls (`runs/esm_v21judge/plddt.json`): **calibration clean** — POS_3DS18 pLDDT **0.85** vs
NEG_scramble **0.37/0.41** (binder/scramble cleanly separated). **ALL 20 finals score 0.76-0.96** — every one
far above the scramble floor, most at/above the positive control → the ESMFold2 half flags **NO** design as
weak. So the two-folder organizers' judge is now complete and **CONFIRMS v21**: ESMFold2 (foldability, all
pass) + Protenix (interface, the discriminator + #1 vindication). v21 order unchanged (ESMFold2 is
confirmatory, not a reorder key — added as `esm2_plddt` in `_v21_evidence.csv`). The side-agent's "trading
verified-20 for unverified" risk does not apply: v21 is a PURE REORDER (0 swaps; 20 seqs still portal-verified).

**2026-10-28 — BLIND BOLTZ + BLIND CHAI (2nd/3rd interface folders, user-requested) → v21 CONFIRMED.**
Ran blind Boltz (GPUs 2-4) + blind Chai (5-7) on the 20 finals + POS/NEG controls, apical fragment, to test
whether Protenix's gate holds under multi-folder consensus. Scored ipSAE (`runs/blind2/{boltz,chai}/ipsae.tsv`);
full table `submissions/tfr1_track2_v21_multifolder.tsv`. **Calibration decided everything:**
- **Chai-blind FAILS the positive control** (POS_3DS18 ipSAE 0.011 ≈ NEG 0.011) → it cannot tell a real binder
  from a scramble on this target → **DISCARDED** (its high scores for w3g2_70/A27HK8/w3g0_290 are sink
  artifacts — note it also "likes" w3g0_290, our weakest on Protenix). Clean catch by the calibration rule;
  reinforces [[lesson-tfr1-apical-blind-cofold-fails-poscontrol]] and [[lesson-chai-mouse-iptm-is-folder-pessimism]].
- **Boltz-blind is VALID but harsh/low-sensitivity** (POS 0.565 vs NEG 0.000, but zeros most de-novo designs incl.
  known-binders genie_w2g5_111/w4g1_195 that Protenix+pocket-restrained rank high). So Boltz=0 is folder
  pessimism, usable to PROMOTE (confirm robustness) not to DEMOTE.
**Consensus → v21 CONFIRMED, not revised:** (1) all **6 "2-folder-robust" designs** (strong on Protenix AND
Boltz-blind: genie_w2g6_144, w3g5_231, w4g7_217, w4g5_147, w4g5_137, w3g6_146) are already in v21's **top-10**
(ranks 3,4,6,8,9,10); (2) the gate-fail group (13-20) is weak on the sensitive folder; (3) **#1 holds** — A27HK8
is "prot-only" (Boltz-blind pessimistic, shared with other good designs) but it is HIGHER on the sensitive
Protenix folder (0.260) than any 2-folder-robust design (w3g5_231 0.205), plus the validated pocket-restrained
pipeline + 3-0 lock. No reorder: demoting high-xr prot-only designs on low-sensitivity Boltz-zeros would be
churn. The organizers'-judge picture is now as complete as this target allows: ESMFold2 (foldability, all pass)
+ Protenix (sensitive interface, the ranker) + Boltz-blind (confirms the robust subset) + Chai-blind (broken,
discarded). v21 stands; v20 remains the portal-verified fallback. Upload + push USER-GATED.

**2026-10-28 — v21 PORTAL-VERIFIED 20/20 (byte-confirmed).** Owner ran v21 through Proteinbase: 20 included,
0 needing fixes, every row Passed (single chain). Byte-verified portal-parsed == `submissions/tfr1_track2_v21.csv`
on all 20 (name + row-order + length + head12 + tail8 identical), and the portal independently confirms the
SAME 20-sequence set as the already-verified v20 (the pure-reorder claim, externally validated). So v21 is now
**portal-verified AND multi-folder-confirmed AND #1-vindicated** — it strictly dominates v20 as the
recommendation (same verified status, organizers'-judge-aligned order). DELIVERABLE: v21 (RECOMMENDED,
portal-verified) > v20 (portal-verified fallback) > v19/v18/v17. Repo pushed to origin/main 2026-10-28
(owner-authorized); ONLY the owner's upload click remains USER-GATED. No further ranking change — the submission
is as validated as in-silico allows (4 structure folders + POS/NEG controls + portal).

**2026-10-28 — AMBITION-LIFT #4 ("5 days left, best 20 on all metrics") → v21 CONFIRMED (5th time), now
organizers'-judge + coherent-ratio + adversary validated. NO change.** Instead of a 5th generation wave
(ceiling confirmed 4×: v15 Genie3 wave, F38 4-backbone moonshot, 18-agent scout 0/13, v21 blind re-score), ran
the genuinely-unexploited lever: scored the 20 **robustly** on the organizers' ACTUAL in-silico judge (blind
Protenix, n=48 samples/design, 95% bootstrap CIs) — v21 had only GATED on a single blind stat; it had never
been RANKED by the judge's own metrics. Calibrated every axis on POS_3DS18/NEG_scramble.
- **Calibration:** blind `iptm_med` VALID (POS 0.210 [0.199,0.244] vs NEG 0.105-0.109, CIs disjoint, ~2×;
  binder-gate ≈0.15). A 2nd NEW interface axis — pose self-consistency / **sc-DockQ proxy** (binder COM spread
  across samples) — **FAILS calibration and is DISCARDED** (POS 16.5Å lies *between* NEG 15.2/19.3Å; same
  failure mode as `on_epi_rate` — blind folding scatters even real binders on this flat epitope).
- **Gate CONFIRMED:** the judge's binder-gate cleanly separates v21's top-12 (H_med 0.157-0.225) from the tail
  13-20 (0.119-0.144). v21's structure is right on the organizers' own judge.
- **Pool mine (NEW folds, GPUs 2-7):** 7 distinct-backbone genuine-switch candidates the judge had never seen.
  Only `w4g1_286` clears the gate — robustly the STRONGEST human binder anywhere (H_med 0.301 [0.281,0.309] >
  rank-1's 0.190 > POS 0.210). BUT it is DOMINATED on the lexicographic objective: #1 switch swing 0.50
  (weakest, effectively 1 in-window His @pKa 6.09) and #2 blind ratio 0.58 / coherent-pocket ratio FOLDER-
  DISAGREES (Boltz 0.48 human-skew + Chai 1.19 mouse-skew → its "balance" is an averaging artifact, worst-case
  |r-1|=0.52), and it is a **structural twin (cluster 2) of the LOCKED flagship** (correlated-failure risk on #1).
  It wins only #3 affinity (lowest). The other 6 are below the binding gate (no better than the current tail).
  Same trap as F38 (one-axis winner, worse on the ratio).
- **Devil's-advocate (cold, P(MISTAKE)=55%)** correctly caught that `build_v21.py` L36 sorts the gate-pass group
  by `xr_mean` = **absolute mouse ipSAE** (a confound, ρ~0.87 with bind per `lesson-crossreact-is-ratio-not-
  absolute`), NOT the objective-#2 ratio — the lesson-crossreact fix reached #1 but was never propagated to the
  portfolio sort. VERIFIED + taken seriously. **Resolution:** recomputed the coherent WITHIN-FOLDER pocket ratio
  (per folder m/h, Boltz & Chai) for the whole gate-pass group from per-folder ipSAE on disk (f30/reval6 +
  f35/robust + f37_rescue). The ratio is **NOISE-DOMINATED**: folders disagree by 0.3-1.0 on nearly every design,
  mean-vs-worst aggregation flips the order, 3/12 sign-flip (#1, genie_w2g5_111, w4g1_286). A ratio reorder
  differs from v21 but changes only noise-distinguished top-10 membership, never the locked #1 (49% of weight),
  and would forfeit v21's byte-level portal verification for ~zero expected gain. The advocate's Prong-B dilemma
  ("ratio decides → re-sort, OR ratio is noise → #2 ties → swap in w4g1_286") is a FALSE dilemma: the project's
  established third state holds — #2 is COARSELY (not finely, not zero) rankable, so neither a reliable fine
  re-sort nor a collapse to pure-#3 affinity is warranted.
- **VERDICT: ship v21 UNCHANGED** (5th independent confirmation of the ceiling), now additionally validated by
  the organizers' robust judge + the coherent #2 ratio + a 55% adversary. `w4g1_286` is surfaced as the single
  legitimate OWNER-OVERRIDE option (a pure strongest-human-binder *affinity hedge*, aligned with the organizers'
  affinity-front-loaded in-silico judge) — recommended AGAINST (dominated on #1 & #2; cluster-twin of #1).
  Evidence: `submissions/tfr1_track2_v21_judge_validation.tsv`, `scripts/judge_validate_v21.py`,
  `runs/prot/pool_judge/{human,mouse}` (7 pool folds). Validator PASS 20/0/0; v21 byte-unchanged + portal-verified.
  Committed this checkpoint; push remains USER-GATED (not requested this session).

## 2026-10-31 — JustHISpKa campaign + blind-Protenix judge → v22 (ONE swap over v21)

- **Mandate:** owner "best 20 logically possible, at all drastic costs, utilize all GPUs"; ~1d19h to deadline.
- **JustHISpKa** (NRC field-best His-pKa predictor; owner downloaded the licensed binary + `.lic` → repo dir, **GITIGNORED, never commit**). Validated **±0.1 pKa** vs 2SIC experimental (His43 3.26/3.25, His106 6.11/6.00). Prep: AmberTools `tleap`→`ambpdb`→Tripos mol2 (push_renum renum reformat for this env's pdb4amber); `FORCE_*` for the "multiple titratable groups" exit. Ran binder-alone AND bound-context on all 20 v21 + 43 pool designs (scratchpad scripts).
- **Finding:** 19/20 v21 switches **GENUINE**; only **#20 `w3g5_249` DEAD** (pKa 2.4–3.1 on two folds + a **2.89 Å** His–Lys salt-bridge geometry + blank `nw` in `_v21_evidence.csv`).
- **GPU work (2–7; 0–1 foreign-held):** folded 7 strong-switch pool candidates (adapted `wave4_rescreen`); ran the organizers' **BLIND Protenix** judge on candidates + all 20 members + POS/NEG controls at n=80.
- **Devil's-advocate (P=82%) caught the key error** → memory `lesson-score-swaps-on-the-ranking-ruler`: I'd ranked cross-reactivity on **pocket** Boltz/Chai, but v21 was gated/ordered by **blind Protenix** (`_v21_evidence.csv` cols H_iptm_prot/MH_ratio/gate). On the correct ruler ALL v21 members are cross-reactive (MH_ratio 0.71–1.46) — the pocket "weak links" #19/#12/#16 were artifacts → **NO swaps there**. The advocate's prediction that the candidate would fail the blind gate was **REFUTED** by direct fold.
- **The one swap:** `w3g5_249` → **`genie_w2g3_53__A59HK21_A17HK48`** — blind Protenix H-iptm **0.264** (PASS, > flagship #1's 0.246), human on-epitope **1.00**, blind MH-ratio **0.98**, genuine switch (His17 6.60 / His59 6.91), novel 0.75. Placed at **rank 20** (keeps one genie in the top-10 — satisfies every advocate condition; tradeoff = 2nd `genie_w2g3_53` cousin, diversity 20→19, within the 2/lineage cap). The triple-His #1-variant was NOT an upgrade (His59 crashed Chai-mouse XR to 0.105).
- **v22 built + verified:** rows 1–19 **byte-identical** to v21 (CRLF matched), `validate_submission.py` **PASS 20/0/0**, owner **PORTAL-PARSED** (20 included, 0 fixes, all Passed, byte-roster-confirmed). sha256 `2bce367395442e577720d6e78446b1826e77b1786ab135326ca76a082355497b`.
- **Complete uniform blind-Protenix record** (n=80, same-batch gate POS 0.258 / NEG 0.13 → 0.194): all 20 members in `submissions/tfr1_track2_v22_blind_protenix.tsv`; **14/20 blind-gate-PASS** (the 6 fails = the known rank-13–18 method-diversity tail incl. the RFD4 hedges and strongest-*switch* w4g2_174); swap-in confirmed top-tier.
- **VERDICT: ship v22** (v21 = unchanged, portal-verified fallback). JustHISpKa = the 7th confirmation leg; it changed exactly one bottom slot. Upload USER-GATED.

## 2026-11-02 — v23→v27: genuinely-varied set, cross-reactive-switch swaps, binding audit → v27 SUBMITTED

- **Arc (full per-version detail in `session-handoff.md` + `submissions/*_evidence.*`):** v22 → **v24** (3 switch-rescue rounds, uniform blind-Protenix n80 re-fold, 20/20 GENUINE Tier-A, portal-verified) → **v25** (RECOMMENDED 2026-11-01, PORTAL-VERIFIED: removed 5 near-twin cousins, added 5 NEW distinct Tier-A from a fresh Genie3 campaign; max pairwise id 26.9%, zero near-twins; genuine cross-reactive count 3→5) → **v26** (2 adversarially-validated cross-reactive-switch swaps at ranks 17/19 via multi-state tied-MPNN + buried-His install; 18 rows byte-identical to v25) → **v27 (FINAL)**.
- **v27 — calibrated full-submission binding audit** (triggered by a red-team note that the blind human epitope spot-check is broken). Re-folded ALL 20 final seqs + POS_3DS18/NEG_scramble in ONE calibrated blind-Protenix run (cuequivariance, n40→n80) + a 4-agent adversarial review (3 skeptic lenses + conservative synthesis; pull only on 2/3 consensus with positive-control-surviving evidence). Findings: (1) the red-team's high-iptm "suspects" were genuine binders (rank2 `w3g0_174` = best cross-reactive binder); all 20 clear the only calibrated human signal (iptm≥0.194, bootstrap scramble FPR≈0). (2) HUMAN epitope-overlap metric is NOISE — POS wepi 0.100 < NEG scramble floor 0.136 (scramble even posts higher best_epi/on_epi); only the iptm floor is valid on human; the MOUSE channel IS calibrated (POS 0.120 > NEG 0.057). (3) Exactly 2 members fire the median-confirmed mouse phantom-collapse signature (high iptm + ZERO epitope engagement, which POS never triggers): **rank18 `w4g5_137` + rank15 `resc_e223_m3`** (latter also borderline-novelty). → replaced with **`resc_v25g3_130`** (NOVEL 0.733, switch His49/His80 2-in-window, mouse cross-reactive) + **`resc_v25g5_13`** (strongest binder H iptm 0.283/med 0.227, switch His29/His36 2-in-window). Other 18 byte-identical to v26; validator PASS 20/0/0; CRLF. See `lesson-calibrated-audit-reveals-dead-metric-and-phantom-collapse`.
- **v27 picks maximally vetted:** n80 parity (both hold human floor + non-phantom) + **pocket-restrained Boltz human-apical docking ABOVE POS** (g5_13 ab_iptm 0.93, g3_130 0.79 vs POS 0.75, NEG 0.20–0.36) — closes the mandatory pocket-restrained validation. 0-Cys, controlled hydrophobicity, diverse (max id ~24% vs kept, 16% to each other).
- **PORTAL-VERIFIED (owner-run):** v27 parsed 20/20, 0 fixes, all Passed, zero similar-flags; both new picks PASSED incl. novelty-borderline g5_13 (portal accepted → caveat RESOLVED); byte-match portal == committed v27.csv.
- **/code-review (user-run):** no finding touched the shipped v27; fixed provenance-script honesty/correctness (annotated the miscalibrated `classify_audit.py` human-wepi gate as superseded, fixed a novelty-verdict precedence pitfall, documented the uncapped-mhr tiebreaker [verified tiebreaker-only → no reorder], fixed stale `build_v26.py` docstrings). Deprioritized findings 3/6/7/8 (scratchpad import paths; a comment bound; dead code — zero submission impact).
- **Methodology writeup:** `submissions/tfr1_track2_v27_methodology.md` (reviewer-facing; honest about the flat-epitope in-silico limits).
- **HONEST LIMIT (stated in the methodology):** true human on-epitope binding + absolute switch magnitude are wet-lab-only on this flat apical target; in-silico establishes above-scramble binding + apical-docking competence + ≥2-His in-window switch + novelty + developability (+ mouse cross-reactivity for a subset).
- **SUBMITTED 2026-11-02:** owner uploaded v27 to Proteinbase (challenge COMPLETE). Repo pushed to origin/main (owner-authorized). Deliverable stack: **v27 (FINAL / submitted) > v26 > v25 (portal-verified fallbacks)**. #1 LOCKED `genie_w2g3_53__A27HK8_A13HR44` throughout.
