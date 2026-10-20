# Campaign plan — TfR1 (CD71) conditional binder (Challenge 4)

**Deadline:** 2026-11-01 23:59 AoE. **Track:** 2/3 (≤20 designs, Claude-selected; upload user-gated).
**Status:** setup + recon (2026-10-20).

## The problem (3 ranked objectives — a winner clears ALL; ties break in order)

1. **pH-selective** — KD vs **human** TfR1 at pH 7.4, **no detectable** binding at pH 6.0.
   (Binds-both ranks after, by KD(6.0)/KD(7.4).)
2. **Mouse cross-reactivity** — also binds mouse TfR1 at pH 7.4; rank by mouse/human KD → 1
   (human KD < 1 µM).
3. **Affinity** — lowest human KD; the **apical** (functional) epitope counts in favour.

Measured in 4 conditions (human 7.4 / human 6.0 / mouse 7.4), design immobilised, target in solution.
"Binding" = a fittable KD, or an association shift > 300% over the negative control.

## Strategy (max-min: optimise each design's weakest axis; diversity breaks ties)

Same objective structure as the TNF challenge (Challenge 2) on a NEW geometry. The differences that
reshape the plan:

- **The epitope is a real, concave, precedented site** (apical domain, around Tyr211). Viruses
  (parvovirus B19 VP1u, Machupo GP1), brain-shuttle antibodies, AND de-novo designs (6WRV/3DS18, TB14)
  all bind it. De-novo minibinders are feasible here — unlike TNF's flat polar surface. ⇒ **Re-test
  ALL generators on this geometry; do NOT assume TNF's Genie3+PXDesign ranking transfers** (RFd3 /
  BoltzGen, which floored on TNF, may work here).
- **Novelty no-fly zone:** 6WRV/3DS18, TB14, viral VP1u/GP1. Stay far (sequence + structural TM).
- **Cross-reactivity is HARD at the apical patch** (6/9 residues divergent; loses basic residues
  R208→N, K371→Q in mouse).

### Epitope choice (the central tension)
- **Apical** → functional (Obj 3 bonus), de-novo-amenable, but species-divergent → cross-reactivity
  (Obj 2) is hard.
- **Conserved patch** (78% overall identity ⇒ conserved surfaces exist outside the apical tip) →
  cross-reactive, but non-functional (no Obj-3 bonus; watch for transferrin-site overlap).
- **Plan: portfolio SPLIT** — (a) apical, human-focused, strong pH-switch (Obj 1+3); (b) a conserved
  sub-patch / the conserved-apical-3 for cross-reactivity (Obj 2); (c) a few targeting a conserved
  apical sub-site aiming for all three. F01 recon fixes the exact residues.

### pH-switch mechanism
- **Mechanism B (buried intra-binder His network)** is the DEFAULT for cross-reactive designs —
  target-independent, so it survives the mouse interface (the apical target cations do not). Baker
  2025 SOTA (79× on TNF-α).
- **Mechanism A (interface His vs conserved target cation)** only where a CONSERVED basic residue sits
  at the interface (verify h↔mouse).
- Validate direction AND selectivity: two-state MD occupancy (+ Gln-isostere control) · PROPKA–Wyman &
  pKAI linkage · GFN2-xTB cluster energetics · ON-state contact gate. Switch *magnitude* is
  in-silico-unrankable → select for DIVERSITY of mechanism; gate on direction purity.

### Cross-species
Human-optimised switches often DON'T transfer (TNF: ~5/18; strength ≠ transfer). Build a mouse model;
test every design ENERGETICALLY with matched protonation; rank by worst-case (human ∧ mouse) ipSAE_min;
feature dual-species releasers; demote (not auto-cull) anti-switchers.

### Molecule classes
Primary: de-novo **`protein`** minibinders (40–100 aa) — best control for His-switch engineering and
strong de-novo precedent at this epitope. Hedge: microbinders (<40 aa) and a nanobody arm (brain-shuttle
Abs bind apical; but legacy de-novo VHH hit rate ≈ 1% — if included, filter hard on ipTM ≥ 0.6 /
Chai-2-class). Cap ≤ 2 per lineage.

## Pipeline (stages ↔ feature_list.json)

F02 target prep → F04 generation (RFd3 / Genie3 / BoltzGen / PXDesign at chosen epitope[s]; nanobody
arm optional) → F05 sequence (ProteinMPNN; cross-species JOINT multi-state MPNN) → F06 binding (af2ig +
Boltz-2 + Chai; ipSAE / ipSAE_min; self-consistency) → F07 pH-switch install + 4-class validation →
F08 mouse energetic cross-validation → F09 novelty + developability (0-Cys, SAP, expression) →
F10 assembly/selection (≤20, diverse, ranked, validator PASS) → F11 methods + submission (user-gated).

## Tools (shared installs — `./init.sh --tools`)
RFdiffusion3/1, Genie3, BoltzGen, PXDesign/Protenix, Boltz-2, Chai-1, ProteinMPNN, AF2-initial-guess /
BindCraft, OpenMM / AmberTools, pmxFEP, justHisPKa. Reference pipeline:
`../anthropic-adaptyv-2026-tnf` (`scripts/README.md` is the manifest).

## Top risks (carried from TNF / GLP1R)
1. **Cross-species switch transfer fails** → mechanism B + direct mouse energetics.
2. **Over-optimising one in-silico metric** (the selector does not rank on a single metric; method
   novelty matters) → a diverse, mechanistically-honest portfolio + a clear methods writeup.
3. **Novelty collision** with 6WRV/TB14 → structural TM gate on every design.
4. **Switch is folder-invisible** → explicit two-state physics only, on the exact submitted sequence.
5. **af2ig positive control must be de-novo** (natural binders fold to garbage single-seq; trust only
   plddt_binder > 80 & rmsd < 2).
