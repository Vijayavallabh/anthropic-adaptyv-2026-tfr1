# session-handoff

**Repo:** `/home/prachh/v/anthropic-adaptyv-2026-tfr1` (private; local git, no remote)
**Challenge:** Anthropic × Adaptyv 2026 #4 — conditional TfR1 / CD71 binder.
**Deadline:** 2026-11-01 23:59 AoE. Track 2/3, ≤20 designs, Claude-selected (upload user-gated).

## To resume
1. `./init.sh` (uv sync + smoke gate). `./init.sh --tools` prints shared tool paths.
2. Read `AGENTS.md`, `docs/PLAN.md`, `configs/target.yaml`; check `feature_list.json` (`active`) +
   `progress.md`.
3. Continue the active feature.

## State (2026-10-20)
- F00 done (repo + harness). F01 recon + strategy launched.
- Tools (shared): `/home/prachh/work/cache/{rfdiffusion3_opt,genie3_opt,chai1_opt}`, BoltzGen in
  `work/cache/huggingface/models--boltzgen--boltzgen-1` (+ `../glp1r/third_party/boltzgen`),
  Boltz-2 `~/.boltz`, PXDesign `v/protenix_cache`, ProteinMPNN `../mva-track2-orthogonal-*/ProteinMPNN`,
  AF/BindCraft `work/cache/bindcraft/alphafold`; per-tool venvs `../sepiq-2026-challenge/.venv-*`;
  MD/pKa conda envs `ambertools`/`pmxfep`/`evobind` + `justHisPKa`.
- Reference pipeline: `../anthropic-adaptyv-2026-tnf` (`scripts/README.md`).
- 8× H100: GPU0 lightly used, 1–7 idle (at setup).

## Open decisions (F01 synthesis / brainstorming)
- **Epitope:** apical (functional, Obj 3 bonus, de-novo-amenable, but 6/9 divergent h↔mouse) vs a
  conserved patch (cross-reactive, non-functional). Likely a portfolio split.
- **Switch mechanism:** A (interface His vs conserved target cation — but apical cations are
  species-divergent) vs B (buried intra-binder His network — cross-species-safe). Leaning B for
  cross-reactive designs.
- **Molecule-class mix:** de-novo `protein` minibinders (apical is de-novo-amenable, cf. 6WRV) ±
  microbinders ± a nanobody arm (brain-shuttle Abs bind apical; legacy de-novo VHH ~1% hit rate).
