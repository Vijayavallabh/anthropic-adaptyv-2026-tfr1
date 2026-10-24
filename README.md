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

**COMPLETE (2026-10-24) — v13 ready (crowns validated); upload user-gated.** Deliverables (all validator PASS):
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
  **10 new sequences → portal novelty re-check before upload** (local oracle: all novel, covwTM 0.64–0.78).
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
