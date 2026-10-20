# METHODS — in-silico validation playbook

A design's claims (binding, pH-switch, cross-reactivity, novelty) are only as good as the
validation. This is the gate each claim must clear. All validation is on the EXACT submitted
sequence (**submit == folded == simulated**). Scripts are adapted from the reference pipeline
`../anthropic-adaptyv-2026-tnf/scripts` (its `scripts/README.md` is the manifest).

## 1. Binding (human, ON state) — F06
- **af2ig** (AlphaFold2 initial-guess) is the load-bearing filter: `pae_interaction < ~10`,
  `plddt_binder > 80`, `rmsd < 2`. The positive control MUST be a DE-NOVO binder — natural binders
  fold to garbage single-seq, so a natural-binder "control" is meaningless.
- **Boltz-2** and **Chai-1** co-fold as independent folders; require ≥2-folder agreement.
- **ipSAE / ipSAE_min**: interface score; use the worst-case over {human, mouse} (ipSAE_min) as the
  robustness ranker — ipTM-delta hides weak interfaces.
- **Self-consistency**: design → MPNN → refold recovers the intended backbone.

## 2. pH-switch (direction AND selectivity) — F07
Folders are pH-blind; a good ipTM is NOT a switch. Four orthogonal method-classes, contact-gated:
- **Two-state explicit MD occupancy** (the decider): His-neutral interface intact @ pH 7.4,
  His-protonated (HIP) interface broken @ pH 6.0. Include a **Gln-isostere causal control**
  (His→Gln collapses the effect). Tune the transition to sit at pH 6.0.
- **PROPKA–Wyman linkage**: `ddG_pH = RT·ln10·∫ Δn_H dpH` over the window; sign = release direction.
- **pKAI** (and fixed-protonation MD) as an orthogonal pKa/sign predictor; require sign-consensus.
- **GFN2-xTB** interaction energy on the capped His···partner cluster (buried-limit vacuum; ALPB bulk
  water over-screens isolated 2-fragment clusters — sign resolves only for tight contacts).
- **Contact gate**: count a switch only if the ON-state His is < 8 Å from its partner AND
  `d_switch > 2·max(SEM incl. the Gln control)` — removes N-terminal-drift artifacts.
- Mechanism **B** (buried intra-binder His network) is preferred for cross-reactive designs;
  mechanism **A** (interface His vs conserved target cation) only where a conserved cation exists.
- Switch *magnitude* is in-silico-unrankable (alchemical FE + metadynamics agree) → select for
  DIVERSITY of mechanism; gate on direction PURITY (0 confirmed anti-switch).

## 3. Cross-species (mouse) — F08
- Build a mouse-TfR1 complex (thread the design onto the mouse model); the human switch does NOT
  transfer for free (TNF: ~5/18 held; strength ≠ transfer).
- Test the mouse leg ENERGETICALLY with matched protonation; gate pose-trust on paratope contacts +
  switch-His interfaciality (< 6 Å) first (ipTM alone is folder pessimism).
- Feature dual-species releasers; demote (not auto-cull) mouse anti-switchers.

## 4. Novelty + developability — F09
- Structural: single-seq fold; max TM to PDB + AFDB (and specifically to 6WRV/3DS18, TB14, viral
  VP1u/GP1) must be LOW; sequence id ≤ 30% (mmseqs). Portal ≥3/4 is authoritative.
- Developability: 0 Cys (no disulfide dependence), SAP aggregation, ESMFold-monomer pLDDT +
  orthogonal-consensus expression screen.

## 5. Definition of done (per design)
`submit == folded == simulated`; binding confirmed by ≥2 folders; switch direction-pure,
contact-gated, ≥2 sign-consensus methods; mouse leg tested; novelty re-checked; 0 Cys; validator PASS.
