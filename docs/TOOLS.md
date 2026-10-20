# Design-tool availability (verified by bytes, 2026-10-20)

The sibling repos' `uplifting-biomolecular-modeling` installs (`third_party/`, `envs/`, `weights/`) were
**cleaned**. What runs NOW vs what must be rebuilt, with exact recipes. Re-verify before relying.

## Kit SOURCE preserved (keystone for every rebuild)
`/home/prachh/work/cache/uplifting-biomolecular-modeling/` (1.1 GB, copied from an ephemeral scratchpad
before GC). Contains af2ig, boltzgen, pxdesign, rfdiffusion3 (+`stock/foundry*.tar.gz`), genie3,
rfdiffusion1, proteinmpnn, common, + folders (boltz2, chai1, protenix, esmfold2, …). Each has `run.sh`
+ `environment/requirements.lock`. Canonical rebuild also = `git clone https://github.com/anthropics/uplifting-biomolecular-modeling` + `scripts/setup_uplifting.sh <kit> [--weights]` (Route C, isolated uv venv).

## RUNNABLE NOW
- **BoltzGen** (GENERATOR — primary for F04). Env `/home/prachh/v/anthropic-adaptyv-2026-glp1r/third_party/boltzgen/.venv` (py3.11). Weights `/home/prachh/work/cache/huggingface/models--boltzgen--boltzgen-1/snapshots/*/` (3 ckpts). Run: `HF_HOME=/home/prachh/work/cache/huggingface .venv/bin/boltzgen run SPEC --output DIR --num_designs N --protocol {protein-anything,nanobody-anything,…} --steps design [inverse_folding …] --diffusion_batch_size B --use_kernels false`. Co-designs seq+struct (binder=chain A, target=chain B). NO `--seed` (per-process RNG). Small batch size → length diversity. `protein-anything` yields a MIX: 0-Cys de-novo folds (protein arm) + VHH frameworks (nanobody arm). Driver: `scripts/gen_boltzgen.sh`. Spec gen: `scripts/make_boltzgen_spec.py` (target must be RCSB-format CIF with `_entity_poly_seq`; a gemmi/biopython PDB→CIF does NOT emit it — build FROM the raw RCSB cif).
- **Boltz-2** (FOLDER, F06). `/home/prachh/v/sepiq-2026-challenge/.venv-boltz` (`boltz 2.2.1`); weights `~/.boltz/`. `boltz predict`.
- **Chai-1** (FOLDER, F06). `/home/prachh/v/sepiq-2026-challenge/.venv-chai`; weights `/home/prachh/v/chai_downloads/` (9.5 GB).
- **Protenix** (FOLDER only, not a generator). `.venv-protenix`; ckpt `/home/prachh/checkpoint/protenix_base_default_v1.0.0.pt`.
- **ProteinMPNN** (F05). `/home/prachh/v/mva-track2-orthogonal-20261006-v29/ProteinMPNN` (+ weights); also vendored inside BoltzGen (`--inverse_fold_model solublempnn`).

## NEEDS REBUILD (source in the preserved kit; AF2 params already cached)
- **af2ig** (de-novo fold gate, F06 — the honest binding gate; Boltz/Chai over-dock). AF2 params present:
  `/home/prachh/work/cache/bindcraft/alphafold/params_model_1_ptm.npz` (point `AF2_PARAMS` there, skip DL).
  Build: `setup_uplifting.sh af2ig` (py3.11, jax 0.5.3 + CUDA-12.8 stack — pin cublas/runtime/nvrtc/cupti
  12.8 + cudnn 9.8, cf. memory), `run.sh install`, then `run.sh pred --config h100 --mode exact --pdbdir D --out D`.
  Proven drivers: tnf `scripts/run_af2ig.py` + `fold_af2ig.sh` (binder=chain A; rmsd<2 ∧ pae<10 ∧ plddt_binder>80).
- **PXDesign** (2nd generator). env `envs/uplifting-pxdesign`, ckpt `pxdesign_v0.1.0.pt`. `run.sh design --config h100 --mode fast -i tasks.json -o OUT` with `PXDESIGN_CKPT_DIR`+`PROTENIX_DATA_ROOT_DIR` (cf. memory env-pxdesign-activation-recsite).
- **RFdiffusion3** (best for the buried-His network; EXPENSIVE: apex wheel compile ~10 min + CUDA-13 toolkit + weight DL). `setup_rfd3.sh` (in tnf). Rebuild only if BoltzGen+PXDesign coverage is insufficient.
- **Genie3** (`setup_genie3.sh`), **RFdiffusion1** — moderate; diversity arms.

## MISSING (need upstream clone)
- **BindCraft** (only AF2 params cached, no code) — clone martinpacesa/BindCraft + ColabDesign/JAX. Non-trivial.
- **RFantibody** — nothing. Not blocking: BoltzGen `--protocol nanobody-anything` covers the VHH arm.

## F04 generator plan (reality-adjusted)
Recon's "RFd3 + BindCraft lead" assumed availability neither has today. **Actual wave-1 lead = BoltzGen**
(runnable, co-designs, covers protein + nanobody). Add **PXDesign** (rebuild, cheap-ish) for a 2nd lineage,
and **RFd3** (expensive rebuild) only if needed for the buried-His mechanism-B geometry or diversity.
Rebuild **af2ig** before trusting F06 binding numbers (Boltz/Chai over-dock; af2ig is the de-novo gate).
