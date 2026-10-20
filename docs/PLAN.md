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
  BoltzGen, which floored on TNF, may work here). **Recommended lead for this concave precedented pocket
  (F01 `sota` scout): RFdiffusion3 (all-atom — best lever for building the buried-His network) +
  BindCraft**, PXDesign/Genie3 as proven arms, SeedProteo for novelty-max, Mosaic as an expert
  multi-objective arm. The apical cluster (~Tyr211, ≤~12 Å) is an ideal RFd hotspot cluster.
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
  target-independent, so it survives the mouse interface (the apical target cations do not). Baker 2025
  (Ahn/Coventry et al., bioRxiv 2025.09.29.678932): buried His-network up to **~10⁸×**; interface-His
  (mech A) up to **~1000×**. (NB: paper targets are EphA2/TNFR2/IL-6/PCSK9/Neo2 — the cached "79× on
  TNF-α" was a memory error.) Centre the OFF transition at pH 6.0 with **JustHISpKa** (MUE 0.4;
  in-repo), cross-checked by PROPKA/pKAI sign-consensus + GFN2-xTB + two-state MD.
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
Abs bind apical; but legacy de-novo VHH hit rate ≈ 1% and **no Chai-2 in the stack** — if included,
filter hard on ipTM ≥ 0.6 / ≥2-folder consensus). scFv/Fab dropped (conserved frameworks fail novelty).
Cap ≤ 2 per lineage.

### Portfolio allocation (F01 `portfolio` scout; planning defaults, rebalance by F06/F07/F08 yields)
Default 20 = **protein 18** (micro 3 / mini 12 / large 3) **+ nanobody 2 CONDITIONAL** (else slots →
protein mini). Every design installs a direction-pure pH switch (Obj1 is a hard gate, not an arm).
- **Arm C — conserved-apical SUBSITE, all three objectives, THE MAX-MIN CORE** (largest): 7 protein
  (6 mini + 1 large) + up to 2 nanobody. Contact conserved {202,203,209} + adjacent conserved surface;
  **mechanism B**; JOINT multi-state human+mouse MPNN.
- **Arm B — conserved NON-apical patch** (Obj2+Obj1 cross-reactive specialist): 6 protein (4 mini +
  2 large). Mechanism B. AVOID the Tf/helical site (619–670). (Conserved stretches from the alignment:
  461–486, 488–505, 543–560, 725–744, … — surface-filter in F02.)
- **Arm A — apical, human-focused** (Obj1+Obj3; Obj2 sacrificed): 5 protein (3 micro + 2 mini).
  Mechanism A (vs human R208/K371) or minimal B. The sure-binder + affinity/functional hedge.
Tilt to the hard axis: cross-reactive-capable (B+C = 13) > human-only (A = 5). Size gates switch core:
micro → mech-A/Arm-A only; large → richest buried-His core (B/C); mini = workhorse. Rank CSV by
per-design **max-min** = min(norm Obj1, Obj2, Obj3) desc; gates DEMOTE not cull; ≤2/lineage even at the head.

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
