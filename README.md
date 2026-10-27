# anthropic-adaptyv-2026-tfr1

De-novo **conditional (pH-switch) binders for human TfR1 / CD71** — Anthropic × Adaptyv 2026
Protein Design Competition, **Challenge 4**. Designs bind human TfR1 at **pH 7.4** and release at
**pH 6.0** (the endosomal-recycling direction), **cross-react with mouse TfR1**, and the switch is
proven in silico before any wet-lab test.

Built on the reusable conditional-binder toolkit (generalised from the Challenge-1 EGFR and
Challenge-2 TNF projects); the TfR1-specific target, epitope, and switch live in
`configs/target.yaml` and `docs/`.

## Objective priority (a winner must clear all three)

1. **pH-selectivity** — bind human TfR1 at pH 7.4, **no detectable** binding at pH 6.0 (highest)
2. **Mouse cross-reactivity** — one sequence binds human and mouse TfR1 (KD ratio → 1)
3. **Affinity** at pH 7.4 — the **apical-domain** (functional) epitope counts in favour

Novelty (distance from known proteins, incl. the known TfR1 binders **6WRV/3DS18** and **TB14**) is a
hard gate; the Proteinbase portal is authoritative.

## Status

**COMPLETE (2026-10-27, latest) — v17 is the RECOMMENDED deliverable; PORTAL-VERIFIED 20/20, cleared for upload (user-gated).**
- **`submissions/tfr1_track2_v17.csv`** (RECOMMENDED) + `_v17_evidence.csv` — 20 genuine-switch crowns re-ranked
  on a ROBUST metric. Root-cause finding: v16's cross-reactivity numbers were the **max across diffusion
  samples** (optimistic); v17 re-scores all 20 v16 + 19 Wave-4 switched crowns in one same-pipeline DIFF=6
  dual-folder batch and ranks on the **mean** (aligned with the organizers' conservative ipSAE_min+ensemble
  judge). #1 `w3g2_70` (robust 0.349, stable, portal-cleared) replaces w3g6_146 (robust mean 0.19 — its 0.397
  was one lucky sample → #13). **8 new Wave-4 distinct-fold crowns** (deep 3,200-backbone Genie3 wave f35)
  replace 8 weak/dead-switch, non-crown, or structural-cousin v16 members. All 20 GENUINE switches
  (JustHisPKa); **19/20 distinct folds** (vs v16 15/20; max achievable); RFD4 lineage kept (#12/#14).
  **Portal-verified 2026-10-27 — all 20 Passed, "0 needing fixes", no novelty / "similar designs" flags
  (both borderline-novelty new designs cleared); byte-verified submitted==validated.** Validator PASS.
  New scripts: build_v17.py, build_master_v17.py, wave4_rescreen.sh, wave4_robust.sh, pose_subsite.py.

**UPDATED (2026-10-27, later) — v16 (now a fallback; superseded by v17).** v16 = the 20 portal-verified v15 sequences RE-RANKED on accurate new evidence; validator PASS; upload + push user-gated. Key:
- **`submissions/tfr1_track2_v16.csv`** (RECOMMENDED) + `_v16_evidence.csv` — same 20 sequences as v15
  (all portal-novelty-cleared), re-ordered by the ACCURATE switch tool. Objective #1 (pH-switch, 49%/39%
  selector weight) is now scored by **JustHisPKa** (MUE 0.4; AmberTools prep wired this session) instead of
  His-cation geometry. Ranking = genuine-switch tier gate → XR → bind, developability demotion, diversity.
  **#1 = w3g6_146** (genuine 2-His switch + best XR 0.397 + high bind — strongest on all three), replacing
  w3g5_70 (accurate tool shows only 1 of its 3 His fires). Weak/dead switches demoted to the tail
  (genie_w2g3_53 switch 0.31 #3→#16; genie_w1g0_112 dead →#18). Honest negatives: joint multi-state MPNN
  did NOT raise cross-reactivity (0/12; re-seq kills binding — XR ceiling ~0.40 holds); blind Protenix
  (organizers' folder) cannot localize the apical epitope even for the POS_3DS18 control → dropped as a
  ranker. New scripts: benchmark_table.py, dev_augment.py, propka_switch.py, justhispka_switch.py,
  fold/score_protenix_tfr1.py, joint_xreact_build_tfr1.py+joint_xreact_mpnn.sh, build_v16.py.
- **`submissions/tfr1_track2_v15.csv`** (fallback) — the same 20, ranked before the accurate-switch re-rank.

**UPDATED (2026-10-27) — v15 (now a fallback; superseded by v16).** All validator PASS.
- **`submissions/tfr1_track2_v15.csv`** (RECOMMENDED) + `_v15_evidence.csv` — 20 designs, **15 genuine
  robust-switch crowns** (clear all three objectives under 6-Boltz-sample robust folding + dual-folder
  min + switch_prob Baker-floor + max-TM novelty gate) front-loaded, then 2 weak-switch crowns + 3
  RFD4/RFd1 method-diversity hedges. Built from a fresh 2,400-backbone Genie3 wave (conserved-sub-site
  conditioned) → 2,735 self-consistent+novel → ~47 bind+xr crowns across two screening tiers → switch
  install (greedy + exhaustive rescue) → robust re-fold. Flagship **w3g6_146 XR 0.397** (vs v13 best
  0.322); #1 `w3g5_70` is comfortably-novel (0.690) for top-slot safety. Mix 16 Genie3 / 3 RFD4 / 1 RFd1.
  Honest same-pipeline finding: under this strict robust+novelty test v13's 10 "crowns" hold at only ~5,
  so v15 roughly doubles the robustly-real crowns. Borderline-novelty rows (ranks 2/4/8/9/15, max-TM
  0.81–0.85, pass the ≥L3 gate) are flagged — **run the Proteinbase novelty check before upload.**
- **`submissions/tfr1_track2_v14.csv`** (fallback) + `_v14_evidence.csv` — earlier cut of the same push
  (14 crowns + 6 hedges), validated PASS. Superseded by v15 (deeper crown set, higher top-10 XR).
- **`submissions/tfr1_track2_v13.csv`** (portal-verified fallback) + `_v13_evidence.csv` — see below.

**COMPLETE (2026-10-24) — v13 portal-verified + crowns validated; cleared for upload (user-gated).** Deliverables (all validator PASS):
- **`submissions/tfr1_track2_v13.csv`** (RECOMMENDED) + `_v13_evidence.csv` — the same 20 sequences as
  v12 (byte-identical), with **all 10 CROWNS now validated against a false-positive control** and the
  **top-10 interleaved by generator**. A decoy control (20 de-novo binders designed for *other* targets,
  folded through the exact pocket-restrained human+mouse metric) found that single-folder human binding
  is a weak gate (25% of decoys clear it) but **0/20 clear the crown conjunction** (human ≥0.30 AND mouse
  ≥0.15): max decoy mouse ipSAE 0.108 sits below the 0.15 bar and below every crown's cross-reactivity
  (0.145–0.37). A pose-contact check confirms all 6 Genie3 crowns bury the conserved sub-site (UniProt
  209/210) in *both* species. So the crowns are real — the mouse cross-reactivity axis is the filter
  de-novo non-binders cannot fake. The top-10 then interleaves generators (the four non-Genie3 crowns
  hold protected ranks 1/3/5/7: `d25` #1, `g1_133`/`g7_8`/`g5_14`) to hedge wet-lab correlation risk.
  **Portal-verified 2026-10-24 — all 20 Passed, "0 needing fixes", no novelty flags; the 10 new
  sequences (9 Genie3 crowns + `g7_8`) all cleared the authoritative novelty gate. Cleared for upload.**
- **`submissions/tfr1_track2_v12.csv`** (fallback) + `_v12_evidence.csv` — the same 20 sequences, ranked
  by raw cross-reactivity before the generator interleave. v11 (7 crowns) / v10 / v7 are further
  fallbacks (v10/v7 portal-verified).
- **`submissions/tfr1_track2_v10.csv`** (portal-verified fallback) + `_v10_evidence.csv` — 20 distinct backbones,
  **16 switch-designs incl. 3 all-three CROWNS** (`d25_sw2b_A9_A25` RFd1 x-react 0.37; `rfd4_g5_14_sw2b`
  RFD4 0.185; `rfd4_g1_133_sw2b` RFD4 0.244 — each robust switch + cross-reactive + binding, dual-folder
  confirmed). Standout binder-switch `rfd4_g5_120_sw2b` (ipSAE 0.853). Built by validating against the
  **organizers' exact judge** (selection prompt) + screening a 1567-design pool for switch-installable
  binders. **Portal-verified 2026-10-24 — all 20 accepted ("20 included • 0 needing fixes"), every row
  Passed, no novelty / "similar designs" flags; the 9 sequences new since v6 (the re-His'd `g5_14` crown
  + 8 pool switch-designs) all cleared.** Ready to upload (user-gated).
- **`submissions/tfr1_track2_v7.csv`** (fully portal-verified fallback) — same 20 sequences as v6
  (portal 20/20 PASS), re-ranked. Use if skipping the portal re-check. v9 (4 new) / v8 (2 crowns) are
  intermediate fallbacks; v6 is the original frozen fallback.

**Key validation finding:** the organizers co-fold **blind** against the full ectodomain; on this
flat/buried apical epitope that is unreliable even on the exact homodimer (ipSAE ≈ 0 and epitope drifts
for POS_3DS18 itself). So selection rests on **switch mechanism** (replicate-fold validated) >
**cross-reactivity** (fragment, dual-folder min) > **apical binding competence** (pocket-restrained
fragment), plus pLDDT (all pass), hydropathy, and novelty. Generators: RFdiffusion1 + RFD4-Proteina.
See `progress.md` / `session-handoff.md`.

## Quickstart

```bash
./init.sh                 # uv sync + compile + pytest smoke (the verification gate)
./init.sh --tools         # print shared design-tool locations (no heavy re-install)
uv run python scripts/validate_submission.py <designs.csv> --track 2
```

## Layout

- `configs/target.yaml` — target / epitope / trigger / cross-reactivity contract
- `docs/PLAN.md` — campaign strategy + stage map (stages ↔ `feature_list.json`)
- `scripts/`, `src/adaptyv_tfr1/` — pipeline implementation + submission contract
- `submissions/` — the ranked portfolio CSV (the deliverable; upload is user-gated)
