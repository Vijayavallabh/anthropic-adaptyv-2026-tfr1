# Methodology — de-novo pH-conditional TfR1 (CD71) apical binders

**Submission:** 20 ranked designs (Track 2). **Objective (lexicographic):** (1) pH-switch selectivity — bind at serum pH 7.4, release in the endosome at pH ~6.0; (2) mouse cross-reactivity; (3) affinity. Hard novelty gate.

## Why this target is hard, and the design philosophy

The TfR1 apical domain is the epitope used for receptor-mediated transcytosis (e.g. brain-shuttle delivery). A useful binder must **let go in the acidic endosome** so the receptor recycles rather than routing to the lysosome, so the central engineering problem is not affinity but an **endosomal pH switch**. The apical surface is flat and polar — a regime where helix-biased de-novo backbones fail — so generator choice and an explicit, physics-based switch mechanism drive the design.

## Design

- **Backbones.** Primary generator **Genie3**, conditioned on the conserved apical sub-site (UniProt 202/203/209/210); **RFdiffusion4 / Proteina** added for fold diversity. (RFdiffusion1 walls on this flat/polar epitope and was not used for the finals.)
- **Sequences.** **SolubleMPNN** (cysteine-free, solubility-optimized weights).
- **Cross-reactive designs.** A **multi-state tied ProteinMPNN** designs a single sequence against the human *and* mouse apical domains simultaneously (one construct, both species tied).
- **pH switch.** An engineered **histidine network at the binding interface**: histidines placed so that protonation near pH 6 electrostatically disrupts the interface while the neutral (pH 7.4) state binds.

## Validation

**Binding (organizers' blind regime).** Scored with **ESMFold2 + Protenix, empty MSA (blind)** against the apical fragment, **calibrated on every run** with a crystal-validated positive control (POS_3DS18) and scrambled-sequence negatives.

> **Openly stated, important finding.** On this flat human apical epitope the **epitope-overlap metrics (best-epitope / on-epitope / weighted-epitope) are uninformative**: the positive control scores *no better than scrambled decoys* on them. We therefore do **not** use them to judge human on-epitope binding. On the human target the blind co-fold confirms only that a design binds **above the scramble floor** (calibrated iptm ≥ 0.194; bootstrap scramble false-positive rate ≈ 0), *not* that it binds the exact apical site.

**Human apical-docking confirmation.** To get a human apical signal the blind ruler cannot provide, we additionally ran a **pocket-restrained Boltz-2 co-fold** that forces contact to the apical epitope, calibrated so the positive control separates from negatives (positive ab_iptm ≈ 0.75–0.86; scrambled negatives ≈ 0.20–0.36). All selected designs dock at the apical site **above the positive control** on this check.

**pH switch.** Validated two ways: a **histidine-pKa predictor** requiring **≥2 histidines titrating in [5.5, 7.4]**, and a **two-state PROPKA Wyman-linkage ddG** (binder-histidine-only, isolating the engineered mechanism).

**Mouse cross-reactivity.** Scored on the mouse apical domain — where the epitope read *is* calibrated and informative (positive control > scrambles). Used both to rank cross-reactivity and to **reject non-specific "collapse" artifacts** (high confidence with zero epitope engagement).

**Novelty & developability.** Structural single-sequence **max TM-score vs the PDB** (plus the Proteinbase novelty gate — all 20 passed). Cysteine-free; controlled hydrophobicity; no long homopolymer runs.

## Selection and audit

Final 20 ranked by the lexicographic objective, **front-loaded** (strongest first), kept **diverse** (maximum pairwise sequence identity ≈ 27%; no near-twins). We ran a **calibrated full-submission audit** (all 20 + controls folded in one run) with an **adversarial multi-model review**, and **replaced two members** that showed the mouse collapse signature (high confidence, no epitope engagement) with vetted clean binders — one of which is a confirmed mouse cross-reactive design.

## Honest limitations (what in-silico can and cannot settle here)

True **human on-epitope binding** and the **absolute switch magnitude** cannot be confirmed in-silico on this flat apical target — only the wet lab settles them. What we establish computationally, per design, is: **above-scramble binding** (blind iptm floor) + **apical-docking competence** (pocket-restrained, positive-control-calibrated) + a **≥2-histidine in-window pH switch** + **structural novelty** + **cysteine-free developability** + (for a subset) **genuine mouse cross-reactivity**. We selected for this conjunction and were deliberately conservative about the switch, which is gate-able but not finely rankable in-silico.
