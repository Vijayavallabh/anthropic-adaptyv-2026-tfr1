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

**COMPLETE (2026-10-24) — submission ready; upload user-gated.** Deliverables (all validator PASS):
- **`submissions/tfr1_track2_v8.csv`** (recommended) — 20 distinct backbones, **two all-three crowns**
  (`d25_sw2b_A9_A25`, RFd1, x-react 0.37; `rfd4_g5_14_sw2b_A34_A50`, RFD4, x-react 0.185 — both:
  robust switch + cross-reactive + binding, dual-folder × dual-species confirmed). Re-ranked by a
  uniform 4-fold validation. **1 new sequence (the 2nd crown) vs v6/v7 → re-run the portal novelty
  check before upload** (local oracle 0.737, novel; low risk).
- **`submissions/tfr1_track2_v7.csv`** (portal-safe fallback) — the same 20 sequences as v6 (portal
  novelty 20/20 PASS already) but re-ranked by the 4-fold validation; use if skipping the portal re-check.
- `submissions/tfr1_track2_v6.csv` — original frozen fallback (portal 20/20 PASS).

Flagships are **mech-B multi-His switches + cross-reactive + dual-confirmed**. Generators: RFdiffusion1
+ RFD4-Proteina. Validation is **pocket-restrained** Boltz-2 ∧ Chai-1 with **ipSAE_min** (worst-case
over folders/species) and **replicate-fold switch probability** (single-fold switch_contacts is noisy).
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
