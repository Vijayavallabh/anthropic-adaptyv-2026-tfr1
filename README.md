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

**Campaign setup (2026-10-20).** Clean repo + harness initialised; recon/strategy (F01) underway.
See `feature_list.json`, `progress.md`, `session-handoff.md`, `docs/PLAN.md`.

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
