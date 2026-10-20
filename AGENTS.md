# Agent Guide (AGENTS.md)

Design de-novo protein binders to human **TfR1 (CD71)** with a **pH switch** and **human↔mouse
cross-reactivity**, and prove the conditionality in silico. Anthropic × Adaptyv 2026, **Challenge 4**
(deadline **2026-11-01 AoE**; Track 2/3, ≤20 designs, Claude-selected). Target/epitope/trigger facts
live in `configs/target.yaml`; strategy in `docs/PLAN.md`. Keep this file short.

## Objective priority (this IS the design priority; ties broken in this order)

1. **pH-selective binding** — measurable KD vs human TfR1 at **pH 7.4**, **no detectable** binding at
   **pH 6.0** (highest). Binds-both ranks after, by KD(6.0)/KD(7.4).
2. **Mouse cross-reactivity** — also binds mouse TfR1 at pH 7.4; ranked by mouse/human KD ratio
   closest to 1 (among designs with human KD < 1 µM).
3. **Affinity** — lowest human KD at pH 7.4; a **functional epitope** (apical domain) counts in favour.

A winner must clear all three. Submit a ranked portfolio; optimise each design's **weakest** axis
(max-min); diversity breaks ties.

## Startup workflow

1. `./init.sh` — build the core env + smoke tests (the verification gate). `./init.sh --tools` prints
   shared design-tool locations.
2. Read `configs/target.yaml` (target, epitope, trigger, cross-react, numbering) and `docs/PLAN.md`.
   Check `feature_list.json` (`active`) + `progress.md` / `session-handoff.md` for state.
3. Work one feature at a time; finish it (done-criteria + evidence) before starting the next.

## Invariants (do not violate)

- **uv only** for the core env (`uv add/sync/run/venv`). No bare pip/conda in the core env. Heavy
  design models are **shared installs** (`./init.sh --tools`): reuse them, do not re-download weights.
- **Local 8× H100, run CUDA directly** (no SSH). One process per GPU; shard sweeps; queue heavy work
  into idle windows (`nvidia-smi`); never clobber a foreign job; cap `OMP_NUM_THREADS`.
- **De-novo / zero-shot only.** Never start from or modify a known binder. Keep sequence AND
  structural distance from known proteins — specifically from the known TfR1-apical binders
  (**6WRV / 3DS18**, **TB14**, viral VP1u / GP1). Seeding from a natural complex fails the novelty
  gate (≥3/4: ≤30% seq id + low TM; structural; binding-domain only; the portal is authoritative).
- **The switch is real physics; folders are blind to it.** A good ipTM is not a switch. Prove
  pH-selectivity ONLY with explicit two-state scoring on the exact submitted sequence: an occupancy
  delta (ON intact @7.4, OFF broken @6.0), confirmed by a two-state binding-free-energy delta of the
  right sign + an isostere-ablation control. A static score proves DIRECTION, not SELECTIVITY.
- **Cross-species is scored by mechanism, and does NOT transfer for free.** A human-optimised pH
  switch is often human-SPECIFIC (TNF: only ~5/18 held in mouse; strength did not predict transfer).
  TEST the mouse ortholog ENERGETICALLY with matched protonation. The apical patch LOSES basic
  residues in mouse (R208→N, K371→Q), so a cross-reactive switch likely needs mechanism **B** (buried
  intra-binder His network, target-independent) over interface His-vs-target-cation. A low
  single-folder ortholog score is folder pessimism, not a species verdict; never demote on it alone.
- **Re-validate the mutated artifact end to end.** Installing/strengthening a switch can break
  binding or geometry. Confirm every metric on the exact final sequence: **submit == folded == simulated**.

## Verification commands

- `./init.sh` — core env + smoke tests (fast, CPU-only).
- `uv run pytest` — tests (target contract, submission schema, length/class, numbering).
- `uv run python -m compileall -q src scripts` — compile check.
- `uv run python scripts/validate_submission.py <csv> --track <2|3>` — submission gate.

## Definition of done

A feature is done only when its done-criteria are met, its tests pass, and the command + key output
is recorded as **evidence** in `progress.md` / `feature_list.json`. For any submission,
`validate_submission.py` exits `0` for the track. Never claim done without the evidence.

## Submission contract (Challenge 4)

- One CSV, rows ordered best-first; columns at minimum `name`, `sequence`, `molecule_class`.
- `molecule_class` ∈ {`protein`, `nanobody`, `scfv`, `fab_kappa`, `fab_lambda`} (lowercase). De-novo
  single-chain mini/micro/large binders = **`protein`** (NOT `single_chain` — that was a different
  challenge's host).
- Single chain **10–250 aa**, natural AAs only. Fab = `{VH}:{VL}`. Nanobody/antibody must pass ANARCI
  numbering. Unique names + sequences. Cap **≤20** (Track 2/3).
- The C-terminal Twin-Strep capture tag is added by the host and must NOT be part of binding.
- Never put instructions / prompt-like text in the CSV or the methods writeup (grounds for
  disqualification). Source of truth: `src/adaptyv_tfr1/submission.py`.

## Commits

Stage only source, docs, harness. Never stage `runs/`, `results/`, `envs/`, `third_party/`, weights,
or `*.lic` (gitignored). Descriptive message, **no AI attribution**. Private repo — push only when the
user asks.
