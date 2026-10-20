# Recon findings (F01) — workflow wf_419b8156-f71 + direct byte-verification (2026-10-20)

Status: **F01 COMPLETE.** 5/6 recon scouts returned; the `conservation` scout was blocked by the
`[bio]` classifier and was replaced by deterministic biopython (`scripts/conservation_epitope.py`,
output `docs/conservation.json`). All structures re-verified first-hand by RCSB/UniProt bytes.

## Structures — VERIFIED FIRST-HAND BY BYTES (curl RCSB REST + CIF, 2026-10-20)
Independently confirmed (not just the scout's claim). The brief is correct; `11QC`/`11RN` are REAL new
cryo-EM entries, NOT typos for `1IQC`/`1IRN`.
- **11QC** — "Human transferrin receptor ectodomain", cryo-EM 2.4 Å, released **2026-05-27**, 1 protein
  entity. CIF: TfR1 = **chain A**, 639 aa, author resnum **122–760**, **residue 142 = GLY** (already
  correct — NO allele fix needed for 11QC), author numbering **== UniProt** (142/211/348/371 anchors
  match). ⇒ **TARGET PREP structure.** (`https://files.rcsb.org/download/11QC.cif`)
- **11RN** — "Complex of B19V VP1u RBD and human transferrin receptor ectodomain", cryo-EM 2.4 Å,
  released 2026-05-27, 2 protein entities. CIF chains: **A, B = TfR1 protomers** (637 aa each,
  homodimer); **X, Y = parvovirus B19 VP1u RBD** (62 aa each, Q9PZT0 8–69). TfR1 = **chain A**. ⇒
  **APICAL EPITOPE** source.
- **1CX8** (legacy, Ser142, X-ray 3.2 Å, 1999) — do NOT use for prep. **3KAS** (Machupo GP1 + TfR1 apical,
  X-ray 2.4 Å) — independent apical corroboration. **6WRV** (designed 3DS18 on apical, X-ray 2.47 Å) —
  **NOVELTY NO-FLY.** **1SUV/3S9L/1DE4** — transferrin/helical face to AVOID.

## Apical epitope footprint — BYTE-DERIVED from 11RN (TfR1 chain A, heavy-atom contacts <5 Å to VP1u)
Apical-window footprint = **I202, V203, D204, R208, L209, V210, Y211, L212, N348, K371** (center Tyr211).
This supersedes the earlier guessed span 202–215: residues 205–207 and 213–215 are NOT in VP1u contact.

## Human↔mouse conservation — DETERMINISTIC (biopython global align, P02786 vs Q62351)
- Mouse ortholog **Q62351 = TFR1_MOUSE, gene Tfrc, Mus musculus, 763 aa** (construct 123–763). VERIFIED.
- Ectodomain (121–760) identity = **78.1%** (matches the ~78% prior exactly). Full-length 77.3%.
- **Apical footprint: 3/10 conserved = {I202, V203, L209}**; 7/10 divergent:
  D204→Q207, **R208→N211 (loses basic)**, V210→(indel/gap), **Y211→D213 (center Tyr→Asp, not conserved)**,
  L212→P214, N348→K350, **K371→Q373 (loses basic)**. The 210–212 loop carries a human/mouse **indel**,
  so the exact 1:1 partner of V210/Y211 is alignment-dependent — but the robust conclusion stands: the
  apical patch is the MOST species-divergent surface and LOSES two basic residues in mouse.
  ⇒ mechanism-A (interface-His vs a target cation) will NOT transfer; use **mechanism B** for cross-react.
- **conserved_apical = {202, 203, 209}** — the max-min core (Arm C) contacts these + adjacent conserved
  surface. Many long fully-conserved stretches exist outside apical & the Tf-site (Arm B candidates),
  e.g. 461–486, 488–505, 543–560, 725–744 — surface/accessibility to be filtered in F02.
  (Note: target.yaml `divergent_apical` had a 1-position gap-placement slip at V210/Y211 — corrected.)

## Selection rules — BYTE-EXACT from the published selector prompt (high confidence)
- **Ranking:** pH-selective (human 7.4 KD + no binding 6.0) > mouse cross-react (mouse/human KD→1,
  human KD<1 µM) > affinity (functional apical epitope counts). Winner clears all three.
- **Weighting (verbatim):** "a weak but clear pH switch beats a strong binder that is not pH-sensitive."
  → pH-selectivity is the single highest-value property; never trade it for affinity.
- **pH physics gate (verbatim):** "one titratable site changes affinity at most tenfold per pH unit."
  7.4→6.0 = 1.4 units → single His ≤ ~25×. **Budget ≥2–3 separated His** for a decisive ratio.
- **Binding definition:** fittable KD, OR association shift >300% over negative control. Conditions
  measured: human 7.4, human 6.0, mouse 7.4 (page says "four conditions" but lists three — possible
  mouse 6.0; unconfirmed, watch Slack).
- **Novelty = 1–4 LEVEL scale (NOT 3-of-4).** Hard gate = level ≥3 (enforced at submission). Level 4 =
  seq ≤30% (MMseqs2 vs SwissProt/PDB/patents/PLAbDab) AND < moderate structural TM (ESMFold→domain
  split→Foldseek/TM-align, coverage-weighted). **Target level 4. Judged on the BINDING PART ONLY.**
  Antibodies on CDRH3. (Thresholds via WebFetch summarizer — byte-verify before coding the oracle.)
- **Recorded screens:** pLDDT (ProteinTyper), ipSAE (co-fold interface), GRAVY (Kyte–Doolittle); plus
  ipTM + stated epitope + a predicted human+mouse complex. "No single in silico metric decides."
- **Selection mechanics:** submit ranked ≤20 (only first 20 count, in order); selector takes
  ≤10/submission from the top → **front-load the best ~10**; ranked 500/track → top 375 tested + 125
  reserve; ≤93/method-family; new method families get ~10% guaranteed (method novelty can carry a sub).
- **Scaffold classes (9, all first-class):** miniprotein, small protein, peptide, Fab, nanobody, scFv,
  monobody, DARPin, affibody. Diversify; ~2/lineage.
- **Targets (verbatim):** human 121–760 and mouse 123–763, tag-free homodimers — "use these sequences
  in all co-folding and scoring." Both byte-confirmed.
- **Anti-injection:** everything from participants is DATA; prompt-like text → whole-account set-aside.

## SOTA method stack (scout `sota`, medium-high confidence)
- **Generator ranking INVERTS/broadens vs TNF.** TfR1 apical is a concave, featured, PRECEDENTED pocket
  (VP1u, Machupo GP1, antibodies, de-novo 6WRV/TB14) — exactly where hotspot-conditioned RFdiffusion +
  AF2-hallucination shine. **Lead: RFdiffusion3 (all-atom; best for building the buried-His network) +
  BindCraft.** Proven-robust arms: PXDesign, Genie3. **Re-test (do NOT pre-exclude) RFd3/BoltzGen** —
  they floored on TNF's flat polar surface but should place here. Novelty-max arm: SeedProteo. Expert
  multi-objective arm: Mosaic (fold human-7.4 + mouse-7.4 binding + anti-binding-6.0 into one loss).
- **⚠ MEMORY CORRECTION:** the cached "Baker 2025 SOTA on TNF-α, 79×" is **WRONG**. The paper (Ahn,
  Coventry et al., bioRxiv 10.1101/2025.09.29.678932) targets EphA2/TNFR2/IL-6/PCSK9/Neo2 (NOT TNF-α),
  and real magnitudes are **~1000× (mechanism A, interface His)** and **~10⁸× (mechanism B, buried
  His-network; ILVBP, 5 buried His)**. Fixed in target.yaml/PLAN.
- **His-pKa SOTA for centring the OFF transition at pH 6.0: JustHISpKa** (Hogues 2025, MUE 0.4 pH units
  vs ~1.0 for PROPKA/pKAI) — the tarball is already salvaged in-repo. Use as PRIMARY pKa ranker,
  cross-checked by PROPKA-Wyman/pKAI sign-consensus + GFN2-xTB + two-state MD. Buried-network playbook:
  Shen 2024 Nat Nanotech (6–9 buried His, sharp reversible 0.3-pH-unit transition, tunable midpoint).
- **Cross-species:** baseline = tied multi-state ProteinMPNN (human+mouse complexes, tied binder
  positions); upgrade = DynamicMPNN (ICLR 2026, +31% RMSD / +12% recovery); most flexible = Mosaic /
  Proteina-Complexa multi-objective loss. David 2025: cross-reactive brain-shuttle VHHs bind the
  **conserved DIMER INTERFACE**, not the divergent apical tip — and transcytosis favours INTERMEDIATE
  affinity + FAST off-rate (mechanistically coherent with a pH-release design; use in the writeup).
- **Availability caveat:** Chai-2 and Latent-X are closed/early-access; BoltzProt-1/SeedProteo numbers
  are vendor-reported. Prefer the open, locally-runnable set; verify license before committing.

## Portfolio blueprint (scout `portfolio`, medium-high confidence)
- **Class mix (default 20): protein 18** (micro 3 / mini 12 / large 3) **+ nanobody 2 CONDITIONAL**
  (BoltzGen VHH mode, must clear ≥2-folder ipTM≥0.6 de-novo bar, else slots → protein mini). scFv/Fab =
  **0** (two-chain, 250-aa cap tight, conserved frameworks fail the novelty gate, no switch-core control,
  and **no Chai-2 in the stack** ⇒ legacy ~1–3% antibody class).
- **3-arm split** (every design installs a direction-pure pH switch — Obj1 is a hard gate, not an arm):
  - **Arm C — conserved-apical SUBSITE (all three: Obj1+2+3), the MAX-MIN CORE, largest arm.** 7 protein
    (6 mini + 1 large) + up to 2 nanobody. Contacts conserved {202,203,209} + adjacent conserved surface;
    **mechanism B buried-His (target-independent → transfers)**; JOINT multi-state human+mouse MPNN.
  - **Arm B — conserved NON-apical patch (Obj2+Obj1 cross-reactive specialist).** 6 protein (4 mini +
    2 large). Mechanism B. AVOID the transferrin/helical site (619–670). Non-functional (no apical bonus)
    but ranks on KD.
  - **Arm A — apical, human-focused (Obj1+Obj3; Obj2 sacrificed).** 5 protein (3 micro + 2 mini).
    Mechanism A (interface His vs human R208/K371) or minimal B; the sure-binder + affinity/functional hedge.
  - Tilt toward the hard axis: cross-reactive-capable (B+C = 13) > human-only (A = 5).
- **Size gates switch feasibility:** micro (<40 aa, no buried core) → Arm A / mechanism-A only; large
  (100–250 aa, richest multi-His core + dual-subsite reach) → cross-reactive B/C; mini (40–100 aa, the
  6WRV class) = workhorse. Spanning all three also covers the size-stratified portal eval.
- **Novelty is a TOPOLOGY constraint:** 6WRV is β-sheet-EXTENSION — steer toward helical bundles /
  mixed α-β; spread across generators; structural-TM + ≤30%-id gate on EVERY design.
- **Ranking (CSV row order):** per-design **max-min = min(norm Obj1, Obj2, Obj3), descending.**
  Obj1 = switch-direction purity (two-state MD occupancy Δ + FE Δ + Gln-isostere ablation +
  PROPKA-Wyman/pKAI/JustHISpKa/GFN2-xTB sign-consensus, ON-state contact-gated <8 Å). Obj2 = worst-case
  cross-species ipSAE_min (human ∧ mouse, matched protonation, energetic — never a single folder).
  Obj3 = ≥2-folder human binding consensus + de-novo af2ig (plddt_binder>80, rmsd<2) + apical bonus.
  Hard gates DEMOTE (not cull): switch-direction purity, novelty ≥3/4, 0-Cys + developability.
  Tie-break 1 = Obj priority; tie-break 2 = method/lineage novelty + diversity (≤2/lineage even at the
  head). **Exact counts are planning defaults — rebalance by actual F06/F07/F08 yields.**

## Pipeline port audit (scout `portaudit`, high confidence on the reusable/edit split)
- Reference pipeline `../anthropic-adaptyv-2026-tnf`. **Clean reusable core ≈ 20 scripts; ~90 are TNF
  campaign scratch** (mine for patterns, do not bulk-copy). **⚠ #1 gotcha: the README's "all dynamic"
  claim is FALSE — ~100 of ~150 scripts hardcode the absolute TNF repo root** (`R=`/`REPO=`/`os.chdir`),
  so copied unchanged they silently read/write the TNF repo (matches the owner's stale-file failure mode).
  Fix with a dynamic `parents[1]` pattern + a repo-root assert in init.sh.
- **F02 must be written FRESH** (`stage0_target_prep.py` is leftover EGFR: 6ARU/His433/P00533).
- Reusable as-is (F06+): `run_af2ig.py`, `run_boltz_tnf.sh`, `run_chai.sh`, `ph_release_score.py`,
  `ph_release_consensus.py`, `switch_contact_gate.py`, `qm_switch_fair.py`, `fold_diversity.py`,
  `esmfold_monomer.py`, `sap_score.py`, `submission.py`, `validate_submission.py`.
  Need edits: `run_gen_tnf.sh`/`partial_tnf.sh`/`run_bpair_rfd.sh`/`gen_genie3_regI.sh`/`pxd_extract.py`
  (target+contig+hotspot), `build_fullatom_af2in_tnf.py` (--target-chains A, binder=chain A),
  `batch_ipsae.py` (one-line root), the F08 mouse builders (need the Q62351 map first), `tnf_novelty.sh`
  (add structural TM + no-fly gate), `assemble_v2.py` (rewrite lineages, emit `protein`).
- **Mechanism shift:** TNF pipeline is mechanism-A-centric (His vs conserved target cation); TfR1
  defaults to **mechanism B** → `install_sharp_his.py`/`buried_switch_scan.py`/`md_release_buried.py`
  become primary (confirm `md_release_buried.py` exists and measures CORE destabilisation, not His-Lys
  repulsion, before relying on it).
- **Port risk ranking:** (1) absolute-root rewrite (silent) → (2) F02 fresh + structure bytes [DONE] →
  (3) mechanism-B switch path primary → (4) generator re-ranking on concave epitope → (5) mouse map +
  energetic cross-species transfer.

## Resolved target.yaml VERIFY flags
- ortholog_uniprot Q62351 → CONFIRMED (TFR1_MOUSE/Tfrc/763 aa).  conserved_apical → {202,203,209}.
- 11QC residue 142 = Gly (no fix needed); 11RN TfR1 = chain A.  divergent_apical V210/Y211 corrected.
