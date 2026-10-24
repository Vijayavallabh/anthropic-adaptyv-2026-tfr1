# progress

**Updated:** 2026-10-20 (session cont., post-/clear)
**Active feature:** F02 — target prep

## Done
- **F00 repo + harness** (closing out) — clean uv project `adaptyv-tfr1` at the canonical path;
  `git init` + repo-local Vijayavallabh identity (global id here is wrong); `justHisPKa` salvaged;
  AGENTS.md / CLAUDE.md / init.sh / feature_list.json / target.yaml / PLAN.md / smoke test written.
  Stale raw-TNF copy moved to `../.stale-tfr1-tnfcopy-20261020`. Reference pipeline:
  `../anthropic-adaptyv-2026-tnf` (`scripts/README.md` is the manifest).
  Evidence: `./init.sh` -> INIT_EXIT=0 (uv sync 42 pkgs; compile ok; pytest now 14/14, incl. target seq = 640 aa). Recon Workflow launched (runId wf_419b8156-f71).
- **F03 submission contract** — Challenge-4 validator (`src/adaptyv_tfr1/submission.py` + `scripts/validate_submission.py`), 10 contract tests, `submissions/example_track2.csv`. molecule_class canonical = `protein` (`single_chain` accepted as a portal alias with a warning; re-verify on the live form). Evidence: pytest 14/14; validator self-check PASS.

- **F01 recon + strategy** (done) — structures byte-verified first-hand: `11QC` = human TfR1
  ectodomain (chain A, 122–760, **Gly142 already correct**, UniProt-numbered) = TARGET; `11RN` =
  TfR1(A/B)+B19V VP1u(X/Y), **TfR1 = chain A** = APICAL. Apical footprint byte-derived from 11RN
  (<5 Å to VP1u): {202,203,204,208,209,210,211,212,348,371}. Conservation deterministic
  (`scripts/conservation_epitope.py` → `docs/conservation.json`): ectodomain **78.1 %**; apical
  **3/10 conserved = {202,203,209}**, 7/10 divergent (loses R208/K371; center Y211 not conserved).
  Mouse **Q62351** = TFR1_MOUSE/Tfrc/763 aa VERIFIED. Strategy in `docs/RECON.md`: generator lead
  **RFd3 + BindCraft** (ranking inverts vs TNF), **mechanism-B** default, **JustHISpKa** primary pKa,
  3-arm portfolio (A apical / B conserved-non-apical / **C conserved-apical subsite = max-min core**),
  18 protein + 2 conditional nanobody. Corrected the "Baker 79× on TNF" memory error (real: ~1000×
  mech-A / ~10⁸× mech-B; targets EphA2/TNFR2/IL6/PCSK9). Evidence: pytest 14/14; `target.yaml` parses.

- **F02 target prep** (done) — written fresh. `data/targets/tfr1_human_ecto_A.pdb` = clean
  single-subunit full-atom human target (11QC chain A, 639 aa, Gly142, glycans stripped) = af2ig target.
  `data/targets/epitopes.json` = 3-arm hotspots: ArmA apical, ArmC conserved subset {202,203,209}, ArmB
  conserved non-apical compact cluster {694,696,704,705,706,714,717,718,725,728,729} (dimer-interface +
  Tf-site + apical-domain excluded). `data/targets/tfr1_mouse_ecto_A.pdb` = mouse (Q62351) threaded onto
  the 11QC backbone + PyRosetta repack/min (78.1% id, divergent epitope positions verified). pytest 17/17.

## In progress
- **F04 generation** — **availability reality** (`docs/TOOLS.md`, byte-audited): the recon's "RFd3 +
  BindCraft lead" is moot — RFd3/Genie3/PXDesign/af2ig installs were CLEANED; **BoltzGen is the only
  runnable generator today**. Kit SOURCE preserved at `/home/prachh/work/cache/uplifting-biomolecular-modeling`
  (1.1 GB) for rebuilds. **Smoke PASS**: BoltzGen docks binders on the conserved apical core (202/203 ~3 Å).
  **Wave-1 launched** across GPUs 1-7 (`scripts/gen_boltzgen.sh`): armC 240 (gpu1-3) / armA 140 (gpu4-5) /
  armB 140 (gpu6-7), `protein-anything`, design step, bs=2 (length diversity), kernels off.
  - **Ig-fold caveat:** `protein-anything` → ~50% VHH/Ig folds (2 Cys) + ~50% 0-Cys de-novo. Ig folds
    FAIL protein-class novelty (Ig is ubiquitous → high structural TM) → **filter: novel 0-Cys → protein
    arm; Ig → nanobody-candidate pool** (novelty judged on CDRH3, must pass ANARCI + ≥2-folder ipTM≥0.6).
    Usable protein yield ≈ half raw → generate more (`--reuse`) if short.
  - **Wave-1 triaged** (`scripts/triage_designs.py` → `runs/f04/triage.tsv`): **432 protein + 71 nanobody**
    candidates. armA 140 protein (30-95, apical, mech-A); armB 107 protein + 20 nb; armC 185 protein
    (incl. **60 large-novel >100 aa** for buried-His cores + 122 mini) + 51 nb. (armC_mini 65-95 wave
    still running on gpu4,5.) Confirms the switch-scaffold worry is moot: BoltzGen's large band is ~50%
    novel, so buried-His-capable large scaffolds ARE available — RFd3 stays conditional on F07.
  - **af2ig REBUILT + verified** (`docs/TOOLS.md`): the honest de-novo binding gate for F06. Next
    generator for lineage diversity = PXDesign (rebuild); RFd3 only if F07 needs it.

## In progress — F06 binding validation
- **af2ig status: CUDA crash FIXED, but af2_initial_guess output is UNRELIABLE on this install — DEFERRED.**
  - Fixed the GPU segfault (kit CUDA 12.9 vs this box's CUDA-13 driver → pinned venv to CUDA 12.8 +
    cudnn 9.8.0.87; `docs/TOOLS.md`). Core GPU ops now verified correct (matmul/conv/einsum/softmax, no NaN).
  - BUT the **6WRV/3DS18 positive control FAILS** (binder rmsd 6.3–6.7, pae_int 20–28, plddt_binder 73)
    and the kit's own barnase–barstar warm scores garbage (rmsd 10.8, plddt_binder 42) — af2ig RUNS
    (rc=0) but does not reproduce a known binder. Params sha256 MATCH the kit pin; inputs verified; CUDA
    ops correct ⇒ the fault is in af2_initial_guess's initial-guess application/patch, not CUDA/params/input.
    Needs deeper debug (uncertain time) — deferred, not trusted. **A gate that fails its positive control
    must not be used** (lesson: validation gates must fail loud + have a positive control).
- **PIVOT: F06 gate = Boltz-2 + Chai-1 two-folder consensus**, discriminated by (a) pose self-consistency
  (co-fold recapitulates the designed pose: binder RMSD-to-design after target-align), (b) ipSAE_min +
  iPAE, (c) 2-folder agreement — with a **6WRV positive control** and a **scrambled-sequence negative
  control** to prove the gate separates binders from the over-dock floor. Run on the 546 protein pool
  (pre-rank by triage iface, co-fold top subset first).

- **Boltz gate CALIBRATED + VALIDATED** (target MSA, binder single-seq; `scripts/{prep_boltz_inputs,run_boltz,parse_boltz}`):
  3DS18 positive control **ab_iptm 0.562 / ipae 15.0** (real-binder ceiling for single-seq-binder cofold)
  vs scrambled negatives **~0.20 / ipae ~23** (floor) — clean separation. On the top-8/arm calibration
  subset: **Arm A (apical/human) + Arm C-mini bind best** (armA_57 0.444, armC_mini_37 0.405, armA_49 0.34);
  **Arm C conserved-subsite is weak** (~0.20-0.25, near the floor) — the cross-reactive core is the hard axis.
  CAVEAT: `hot_contacts` metric is buggy (reads 0 even for the positive — chain-B numbering/offset) → not
  trusted yet; ab_iptm + ipae are the signals. Thresholds: promising ≈ ab_iptm > ~0.33 (well above the 0.20 floor).

## F06 CRITICAL FINDINGS (2026-10-20)
- **Full Boltz run (439+controls) is NOT trustworthy alone — generator/scorer circularity.** BoltzGen is
  built on Boltz-2, so Boltz-2 over-validates BoltzGen's own designs (hundreds at ab_iptm 0.8-0.92) while
  the INDEPENDENT 3DS18 binder scored 0.276 (below the design median 0.427). Target MSA was consistent
  (6518 seqs everywhere), so it's not MSA; it's shared inductive bias + single-sample diffusion noise.
  ⇒ Boltz ipTM alone cannot rank these designs.
- **3DS18 is a WEAK positive control for single-seq cofold** (β-sheet-EXTENSION topology; both Boltz 0.28
  and Chai 0.20 score it low — these binders are intrinsically hard without the binder's own MSA). The
  reliable calibrator is the SCRAMBLED NEGATIVE floor (~0.15-0.19); look for designs that clear it in the
  INDEPENDENT folder.
- **Running Chai-1 (independent architecture) as the honest gate** on top-40/arm by Boltz (124 + controls).
  Decision rule: real candidates must clear the scrambled floor in CHAI (not just Boltz) and ideally in both.

## F06 RESULT: 13 binders pass the independent 2-folder gate (runs/f06/f06_pass.tsv)
- Chai (independent of BoltzGen) SEPARATES a real tail: scramble floor ~0.16, weak 3DS18 positive 0.20,
  but top designs reach Chai **0.40-0.672**. **F06-PASS gate = Chai≥0.35 ∧ Boltz≥0.5 → 13 designs**:
  armC_mini 6, armC 3, armA 4; 12 mini (40-100) + 1 micro. Top: armC_mini gpu4_21 (chai 0.672/boltz 0.811/68aa),
  armC gpu2_31 (0.569/0.806/59aa), armC gpu2_18 (0.505/0.831/85aa), armC_mini gpu5_17 (0.475), armA gpu4_05 (0.466).
- **The cross-reactive core (Arm C) HAS real binders** (3) — the hard axis is reachable. All F06-pass are
  mini → buried-His (mechanism B) feasible.

## F07 feasibility (buried_switch_scan on the 13 F06-pass)
- **6/13 can host a buried-His mechanism-B switch** (His next to a buried binder cation → low-pH repulsion
  → release; variants in runs/f07/switchscan/): armC gpu2_18 (12 positions), armC gpu2_31 (9),
  armC_mini gpu5_12 (11), armC_mini gpu4_22 (7), armC_mini gpu4_21 (5), armA gpu4_05 (2). The other 7 lack
  buried cation anchors (would need a de-novo His-His/His-polar HBNet — harder). The top cross-reactive
  (armC) + armC_mini binders ARE switch-installable — good alignment of binding + switch.
- Next: combine 2-3 separated buried positions → multi-His switched sequences → re-fold (Boltz+Chai, confirm
  binding retained @pH7.4) → JustHISpKa in-window + PROPKA/pKAI sign + GFN2-xTB + two-state MD direction,
  contact-gated. Select for switch-mechanism DIVERSITY (magnitude is in-silico-unrankable).

## Next (F07+ on the 13 F06-pass, + expand)
- F07 pH-switch: install buried-His (mech B) on the 13 (esp. the Arm C cross-react core + Arm A apical) →
  validate direction/selectivity (JustHISpKa + PROPKA/pKAI + GFN2-xTB + two-state MD, contact-gated) on the
  EXACT sequence; re-fold. F08 mouse cross-species (energetic) on Arm C. F09 novelty (structural TM vs
  6WRV/TB14/PDB) + developability. F10 select ≤20 (relax gate to ~Chai≥0.30 / run Arm B region / more pool
  through Chai if more candidates needed). Fix hot_contacts (epitope landing) to support the apical/functional claim.

## Key risks / lessons carried from TNF (Challenge 2) and GLP1R (Challenge 3)
- Cross-species pH-switch transfer is NOT free (only ~5/18 TNF designs held in mouse; strength did
  not predict transfer). Apical patch loses basic residues in mouse → favour mechanism **B** (buried
  intra-binder His network) for cross-reactivity. Test mouse ENERGETICALLY.
- Switch *magnitude* is in-silico-unrankable → select for DIVERSITY; gate on switch-DIRECTION purity
  (two-state MD + PROPKA/pKAI + GFN2-xTB, contact-gated).
- af2ig positive control must be a DE-NOVO binder; ipSAE_min for cross-species robustness.
- Novelty is structural + sequence; stay far from 6WRV/3DS18, TB14, viral VP1u/GP1.
- Don't over-optimise a single in-silico metric (the selector doesn't; method novelty counts).

## F07 multi-His build + F09 developability + novelty tooling (2026-10-20 late)
**F07 switch build** (`scripts/build_multihis.py`): 6 switched seqs from 4 of the 6 switch-viable designs —
gpu2_18 (sw2his A10H/K14+A15H/K64; sw3his +A49H/K53), gpu2_31 (sw2his A18H/K10+A30H/R59), gpu4_22
(sw2his A23H/K27+A30H/K65), gpu5_12 (sw2his A13H/R17+A49H/K89; sw3his +A75H/K78). Each His sits near a
DISTINCT buried cation (Lys **or Arg** — fixed a bug that dropped Arg anchors), pairwise Cβ>8Å so they
titrate additively, not anti-cooperatively. gpu4_21 (TOP binder, Chai 0.672) + gpu4_05 CANNOT host a clean
multi-His switch (K31/R32 adjacent; single R24) → they stay **plain** high-affinity binders. This is the
expected pool-thinning: the final 20 will MIX switch-binders + plain binders (not 20 acing every axis).
- Binding-retention re-fold (Chai, GPU0, bs1usp2au) launched on the 6 switched seqs vs apical receptor;
  keep only those whose Chai stays ≥ gate (parent Chai: gpu2_18 0.505, gpu2_31 0.569, gpu4_22 0.376, gpu5_12 0.407).

**F09 developability** (`scripts/developability_scan.py`, 13 parents + 6 switched → results/developability_dev_input.csv):
- Switch mutations IMPROVE developability — His lowers GRAVY (gpu5_12 +0.153→+0.03; gpu2_31 +0.76→+0.53;
  gpu4_22 +0.39→+0.26). Switch helps solubility.
- 4 expression-SEVERE (charge-blob/low-complexity, GRAVY>+0.9): gpu5_26, gpu5_34, gpu1_14, gpu4_28 → deprioritize.
- Unpaired Cys: gpu2_31, gpu5_34 (scrambling risk → C→S in final seq; gpu2_31 is a good switch-binder).
- Cleanest: gpu2_18 (LIAB 2), armA gpu4_33/35/05, gpu4_22.

**Novelty tooling** (de-risk the HARD ≥3/4 gate): foldseek installed (tools/foldseek, static binary) + PDB DB
downloading (b8d54a6ys); ESMFold2 env `.venv-esmfold2` available (single-seq fold); TMalign works. AFDB skipped
(disk 729G free, AFDB too large) — helical de-novo bundles cap at 3/4 anyway (passes), key check is vs PDB.

**Pool expansion**: Chai-expand on 317 remaining apical designs (bzduk45hg) running → when done, re-run
buried_switch_scan + build_multihis on the FULL F06-pass set (avoid rework on a partial pool).

## F07 switch re-fold RESULT + F08 mouse prep + F09 diversity (2026-10-20 late)
**Switch binding-retention re-fold** (Chai, paired vs parent iptm): switch-install is LOW-YIELD on retrofit —
| design | parent iptm | switched iptm | verdict |
|---|---|---|---|
| armC_mini gpu5_12 sw2his | 0.407 | **0.491** | ✓ survives & IMPROVES (95aa, largest) |
| armC gpu2_18 sw3his | 0.505 | 0.312 | marginal |
| armC gpu2_31 sw2his | 0.569 | 0.300 | fail |
| armC gpu2_18 sw2his | 0.505 | 0.190 | broke |
| armC_mini gpu4_22 sw2his | 0.376 | 0.170 | broke |
Root cause of breakage: burying His deletes a core hydrophobic -> fold destabilizes (not an interface clash;
positions were >9Å from the interface). The one clean win is the LARGEST binder (more core to absorb His).
- Fix 1 (`build_multihis.py`): interface-distance filter (His only >9Å from target contact).
- Fix 2 (`mpnn_switch_repair.py`): install His -> ProteinMPNN repacks the CORE around them, FIXING target +
  interface contacts + His sites (canonical Baker install). Test on gpu2_18_sw3his / gpu2_31_sw2his: His
  retained, 55/85 (resp. core) positions redesigned -> re-fold pending (bc46c2iq0). Rescue decision test-first.

**F09 fold diversity** (foldseek all-vs-all, TM≥0.6): 13 binders -> 6 clusters, but 8/13 share ONE fold
(cluster 1: gpu4_21,gpu2_18,gpu5_34,gpu5_12,gpu1_14,gpu4_33,gpu4_28,gpu4_22 — helical bundles). Selection caps
this lineage (~2 best: gpu4_21 top-affinity + gpu5_12 switch) + keeps the 5 singletons. SEVERE-dev members
(gpu5_34,gpu1_14,gpu4_28) drop from cluster 1 naturally.

**F08 mouse cross-species prep**: mouse apical receptor `data/targets/mouse_apical_189_383.seq` (human 189-383
equiv from threaded mouse ecto; 75.4% id to human apical — more divergent than 78% ecto-wide). Co-fold ready.

**Strategy (honest)**: switch yield is low on retrofit -> rely on (a) expanded pool (more + larger parents),
(b) MPNN core-repair (if the test rescues binding), (c) prioritize large binders. Final 20 = MIX of
switch-binders + strong plain binders (gpu4_21 etc.), as the switch step thins its own pool.

## F07 SOTA pivot: mechanism A (interface His-cation) — 2026-10-20 late
Consensus/lit search surfaced Ahn/Baker 2025 "Computational design of pH-sensitive binders" (bioRxiv
2025.09.29): TWO methods — (i) interface His adjacent to a TARGET cation (repel at low pH, weakens
INTERFACE) and (ii) buried His core networks (destabilize fold). Buried-His designs ([Goldbach 2023],
[Shen 2024]) are built DE-NOVO with the network designed in — hence my mech-B retrofit yield is low.
- **MPNN core-repair = DEAD END**: re-fold of repaired gpu2_18/gpu2_31 got WORSE (0.31→0.22, 0.30→0.28).
  Dropped. (Redesigning core changes the binder; confirms af2-binding-is-sequence-specific.)
- **Mech A is the gentle, high-yield retrofit** (`scripts/mech_a_scan.py`): apical epitope HAS target
  cations (R208,K344,K371,K374 + more). 18 interface-His point-mutant seqs from 11/13 designs; re-fold
  vs apical domain running (bhmf2we3p) to confirm pH7.4 binding kept. Mech A for HUMAN objective #1;
  mech B (conserved cation / large binder) reserved for x-species.
- Note: `runs/f07/complexes` are full-ecto GENERATION poses; `runs/f07/complexes_apical` are the VALIDATED
  F06 apical-domain poses (binder=A 1-N, target=B 1-195, resnum1=UniProt189) — use these for placement.

## F07 switch_contacts validator + first validated switch-binder (2026-10-20 late)
`scripts/switch_contacts.py` (Baker His-cation metric, dep-free) on the RE-FOLDED model confirms the His
actually sits by a cation (re-fold can move it away). First fully-validated switch-binder:
- **armC_mini gpu5_12 sw2his**: binding kept (Chai iptm 0.491 > parent 0.407) AND His A13 makes 4 buried
  contacts to binder R17 (mech-B, >Baker floor 2). (2nd His A49 lost its K89 contact on re-fold — 1 strong
  buried His-Arg pair still = a real switch.) 95aa, developability CLEAN (Nglyc2 only).
Switch-binder gate = binding-retained (Chai≥~0.35) ∧ switch_contacts total≥2 on the re-folded model.
Next: mech-A re-fold (18 seqs, bhmf2we3p) -> same gate; then pKa in-window check (JustHISpKa, env deferred).

## F07 mech-A RESULT: 4 validated switch-binders (2026-10-20 late)
Mech-A single-His (mA1) retains binding 8/9 (vs mech-B retrofit 1/6) — SOTA pivot validated. 2-His (mA2)
mostly broke binding -> single interface His is the gentle, binding-safe switch. Switch GEOMETRY check
(switch_contacts on the re-folded model) narrows to those whose His actually sits by a cation:
| switch-binder | mech | His->cation | dist | bind iptm (parent) |
|---|---|---|---|---|
| armC_mini gpu5_17 mA1 | A | His36->K194(tgt) | 6.0Å | 0.702 (0.475) |
| armC gpu2_31 mA1 | A | His37->K287(tgt,apical99) | 5.6Å | 0.616 (0.569) |
| armC gpu2_18 mA1 | A | His47->K287(tgt) | 4.9Å | 0.554 (0.505) |
| armC_mini gpu5_12 sw2his | B | His13->R17(binder) | 3-4Å ×4 | 0.491 (0.407) |
(armA gpu5_34 mA1 works 0.504 but dev-SEVERE -> deprioritize.) K287 (apical resnum 99) is a recurring
interface target lysine (gpu2_18/gpu2_31/gpu5_34 all switch on it). Honest: single-His mech-A ≈ 1 pH unit,
modest; magnitude in-silico-unrankable -> select for mechanism DIVERSITY (mech-A + mech-B) + binding + novelty.
TODO: His pKa in-window check (nearby K+ lowers His pKa; verify transition stays ≥6.0) — JustHISpKa env deferred.
Mouse co-fold (13 plain binders) running on GPU0; expand 297/317 (full pool imminent).

## F07 switch-His pKa (PROPKA first-pass) — 2026-10-20 late
PROPKA (tools/pka-venv, uv) His pKa on the re-folded complex (model ref 6.50; higher=stronger in-window switch):
- gpu5_12_sw2his His13 pKa **6.23** — BEST (near midpoint, buried His13-R17, binding IMPROVED) = flagship switch
- gpu2_18_mA1 His47 **5.76** — good mech-A switch (bind 0.554)
- gpu5_17_mA1 His36 **5.59** — acceptable mech-A (bind 0.702, best binding)
- gpu2_31_mA1 His37 **5.28** — weak switch (nearby K287 lowered pKa; confirms the mech-A pKa-depression risk) → keep as a binder, switch marginal
All have correct DIRECTION (Δn_H>0 across 7.4→6.0). Caveat: PROPKA is the weakest His predictor (R²~0.05,
±1u) → treat as first-pass; confirm flagship(s) with JustHISpKa/pKAI before final. Magnitude unrankable →
select for mechanism diversity. Switch-binder ranking so far: gpu5_12_sw2his > gpu2_18_mA1 ≈ gpu5_17_mA1 > gpu2_31_mA1.

## Full-pool gate + novelty + Boltz dual-gate on switches (2026-10-21)
**Full pool (Chai iptm≥0.35 ∧ Boltz iptm≥0.5): 18 binders** (runs/f06/f06_pass_full.tsv). Expand added 5:
gpu2_13 (chai 0.697 NEW top), gpu1_08, gpu4_09, gpu4_00, gpu4_31. Dev: 4 new CLEAN, gpu1_08 SEVERE.
**Novelty (single-seq ESMFold + foldseek vs PDB) = SYSTEMIC high-TM** (BoltzGen makes PDB-like folds):
almost all 0.85-1.0 (risk/borderline); new binders too (gpu2_13 0.923). Most novel: gpu4_28 0.774,
gpu5_17 0.844, gpu5_26 0.882 (but these are dev-SEVERE or Chai-weak). ASSUMPTION (reference-adaptyv-novelty-metric):
de-novo helical bundles w/ low seq-id cap at 3/4 => PASS the ≥3/4 gate; 4/4 unreachable without a novel-fold
generator (RFd3/Genie3 not installed). Treat novelty as ~uniform 3/4 pass (not a differentiator); RISK noted.
**Boltz dual-gate on switch-binders** (His mutation can drop Boltz even when Chai holds):
- gpu2_31_mA1  chai .616 ∧ boltz .843  ✓✓ consensus (pKa 5.28 weak switch; novelty .895)
- gpu5_12_sw2his chai .491 ∧ boltz .566 ✓✓ consensus (pKa 6.23 BEST switch; novelty .945 risk; 95aa)
- gpu2_18_mA1  chai .554 BUT boltz .409 ✗ Chai-only (parent was .831 — His hurt Boltz)
- gpu5_17_mA1  chai .702 BUT boltz .437 ✗ Chai-only (parent .809)
=> 2 dual-consensus switch-binders + 2 Chai-only (riskier). Honest: no single design aces switch+novelty+binding.

## NOVELTY CRISIS (2026-10-21) — BoltzGen pool fails the HARD gate
Coverage-weighted novelty (Adaptyv-exact: max TM among hits qcov>=0.70; <0.80=PASS 3/4, >=0.80=DQ 2/4;
PDB-only = LOWER bound, AFDB would raise it). Of 18 binders, only **3 PASS**: gpu5_17 (0.757), gpu5_26
(0.761, dev-SEVERE), gpu4_28 (0.774, dev-SEVERE). gpu4_33=0.0 is a FAILED ESMFold fold (unfoldable, exclude).
ALL the good binders/switches are DQ: gpu2_31/gpu2_31_mA1 (0.895), gpu5_12/sw2his (0.942/0.945),
gpu2_13 (0.923), gpu4_21 (0.914), gpu2_18 (0.929). => **BoltzGen makes PDB-like folds; it fails Adaptyv novelty.**
ONLY clean novelty-pass + switch-capable binder = **gpu5_17 / gpu5_17_mA1** (0.757/0.764, dev-CLEAN, Chai 0.702).
Decision: (1) mine the FULL BoltzGen pool for lower-binding-but-novel folds; (2) if that's dry, PIVOT to a
structurally-novel generator (RFdiffusion/Genie3 — diffusion explores novel fold space; co-folding does not).
This is the side-agent-warned pivot. Runway to 2026-11-01 ~11 days = feasible.

## PIVOT DECISION (2026-10-21): diffusion generator for novelty
Mining the full BoltzGen pool for novel folds is DRY: designs with novel folds (raw TM<0.8) are Boltz-only
(Chai says they DON'T bind — circularity). The binding-novelty tradeoff is intrinsic to BoltzGen (co-folding
reproduces PDB folds). Real binders that PASS novelty: gpu5_17 (0.757, CLEAN, switch mA1, x-react mouse 0.475!),
gpu4_28 (0.774, dev-SEVERE), gpu5_26 (0.761, dev-SEVERE). = 1 clean design.
**PIVOT: install a DIFFUSION generator (RFdiffusion1 first; RFd3/Genie3 if it floors) to produce
structurally-novel binders to the TfR1 apical epitope.** Pipeline: RFd backbones -> ProteinMPNN (0-Cys) ->
Chai∧Boltz validate (fair for non-BoltzGen designs) -> novelty (expect LOW TM) -> mech-A/B switch -> x-species
-> select. FLOOR = gpu5_17 (+ cleaned SEVERE). Kit source: /home/prachh/work/cache/uplifting-biomolecular-modeling/
{rfdiffusion1,rfdiffusion3,genie3}. Note: af2ig broken here -> Chai∧Boltz is the binding gate.

## RFd1 installed + first-design novelty check (2026-10-21)
RFd1 (rfdiffusion1 opt-kit, route C) INSTALLED in third_party/rfd1kit (venv rfd1, weights OK, run.sh check
passes H100, mode=fast). Smoke (2 de-novo, apical hotspots A202/A209/A211, len 70-90): WORKS, ~3min cold-start
(Triton compile) then fast. BUT des_0 backbone foldseek covwTM=0.955 vs PDB = NOT novel (RFd1 default also makes
PDB-like helical bundles). => novelty is NOT automatic with RFd1 either; need the FRACTION of designs with TM<0.8.
Running batch1 (42 designs) to measure the novel-fold yield distribution.
Nuance (reference-adaptyv-novelty-metric): oracle TM is NOISY (portal estimates off up to 2 levels); the
USER-RUN PORTAL check on the final set is the only hard authority. Strategy: maximize novelty MARGIN (prefer
low-TM designs), keep gpu5_17 (oracle-novel 0.757) as floor, generate RFd1 low-TM designs, and gate the FINAL
set on the portal (user-run) pre-submission. Tooling added: self_consistency.py (ESMFold self-consistency +
novelty in one pass, replaces broken af2ig), gen_rfd1.sh, mpnn_rfd.py.

## RFd1 novelty-yield diagnosis + long-binder fix (2026-10-21)
Measured backbone Rg (compactness) + coverage-weighted foldseek novelty on RFd1 batches:
- **batch1 (65-90aa)**: ~70% EXTENDED (single long helices, Rg 26-34 for ~70aa = a straight helix, not a fold);
  only 1/42 compact&novel. SHORT binders to a 3-residue hotspot => RFd1 lays a single extended helix. GARBAGE.
- **batch_long (105-130aa)**: 5/10 compact, **3/10 compact&novel** (des_3 124aa covwTM 0.638 ROBUST, des_4 0.708,
  des_5 0.799). LONG binders fold into compact bundles AND are more novel (longer folds rarer in PDB).
- Extended issue is NOT mode-specific (off-mode des_0 also Rg 34.1) => inherent to short-binder setup, fixed by length.
- MPNN chain bug FIXED: RFd1 output is target=chain A, BINDER=chain B (design B not A).
DECISION: generate LONG binders (100-135aa); filter Rg (compact) + novelty; then MPNN(B,0-Cys) -> self_consistency
(ESMFold real-gate novelty + self-consist) -> Chai∧Boltz binding -> switch -> select. Launched long1 (240 designs).
Funnel yield est: 240 -> ~70 compact&novel -> ~10-30 novel binders. gpu5_17 remains the floor.

## RFd1 novel-binder funnel RESULT (2026-10-21)
long1 (240 long binders) -> 110 compact (Rg) -> 220 MPNN seqs (chain B, 0-Cys) -> self_consistency:
**187/220 self-consistent (85%), 49 novel, 31 self-consistent AND novel** (covwTM 0.70-0.80, PDB-only).
HUGE improvement over BoltzGen (~1 novel). Caveat: all 0.70-0.80 (3/4 PASS but near the line; AFDB would raise;
0 robust <0.65) -> user portal check is the final novelty authority. Chai binding validation launched on the 31
(b4sumfysu); Boltz YAMLs prepped for the dual gate. Next: Chai∧Boltz binders -> switch (mech-A/B) -> x-species
-> developability -> select ≤20 (novel RFd1 binders + gpu5_17 floor). The long-binder RFd1 path WORKS for novelty.

## Novel-binder yield reality + refined plan (2026-10-21)
- des_160_mpnn1 (the 1 novel RFd1 binder): Chai 0.639 but **Boltz 0.317 => Chai-ONLY** (fair, RFd1 is Boltz-independent).
- Partial diffusion from des_160: DUD — children drift to extended/non-novel (parent is marginal-novel 0.793, so children
  inherit marginal/worse). Dropped. Partial diffusion needs a ROBUSTLY-novel (<0.65) parent, which I don't have.
- **Brutal yields**: novel+binding ~0.5% de-novo, and those are mostly Chai-only + MARGINAL novelty (0.70-0.80, near DQ line).
- **Best design remains gpu5_17** (BoltzGen): novel 0.757 + dual-folder binding (Chai .475 ∧ Boltz .809) + mech-A/B switch +
  cross-reactive (mouse 0.475). The most complete single design across all axes.
**Refined plan**: scale de-novo RFd1 volume (long2 420 running + more rounds) with nseq=8 in the MPNN step (4x binding
chances/backbone — rescues near-miss backbones at Chai 0.25-0.30) -> accumulate marginal-novel Chai-confirmed binders.
Realistic target ~8-15 novel binders (not a forced 20). Portfolio: gpu5_17 (anchor) + des_160 + novel RFd1 binders;
switch where it survives; USER portal novelty check is the final gate (oracle is noisy). Honest: a 20-strong-on-every-axis
submission is not achievable with these tools; aim for the best legitimate novel+switch+xreact portfolio.

## Developability + spec-driven strategy pivot to BindCraft (2026-10-21)
Re-read configs/target.yaml (authoritative). Key facts that reshape the plan:
- **Epitope** apical [202,203,204,208,209,210,211,212,348,371]; **conserved-in-mouse = ONLY 202,203,209**
  (I/V/L, hydrophobic). Exposure (isolated-domain neighbor count): 202 BURIED, 203 mid, **209 EXPOSED**,
  211 EXPOSED(center), 204/208/212 exposed but DIVERGENT, 371 buried. => the conserved surface is small
  (209 the one well-exposed conserved anchor); full cross-reactivity is intrinsically hard.
- **Switch**: mech-A (interface His vs target cation) is HUMAN-SPECIFIC (apical basics R208,K371 diverge
  in mouse) -> my gpu5_17_mA1/gpu4_28_mA1 are human-only. mech-B (buried multi-His) = cross-reactive.
  Physics budget: single His ~=25x (near floor); **need 2-3 SEPARATED His**. Selector prefers a weak-but-
  clear switch over a strong non-switch -> pH-selectivity is THE highest-value property.
- **Novelty**: Adaptyv 1-4 LEVEL scale, hard gate >=3, BINDING-PART ONLY, target 4. NO-FLY 6WRV/3DS18/TB14/VP1u.
- **Submission**: ranked <=20, selector takes <=10 from the TOP (front-load best ~10), diversify ~2/lineage
  across 9 classes (miniprotein/small/peptide/Fab/nanobody/scFv/monobody/DARPin/affibody).

DEVELOPABILITY AUDIT (scripts/developability_scan.py on the novel core) — DECISIVE:
- gpu5_17 GRAVY +1.29, gpu5_26 +1.19 (SEVERE), gpu4_28 +0.95 (SEVERE, 11-res hydrophobic run). ALL 3
  BoltzGen novel binders are EXTREMELY hydrophobic (expression/aggregation risk) — because the conserved
  hotspots are hydrophobic AND MPNN made the WHOLE binder hydrophobic.
- des_160 (RFd1): LIAB=1, 52% charged, SOLUBLE. RFd1+MPNN binders are DEVELOPABLE; BoltzGen are not.
=> A binder that won't express can't win. This re-justifies de-novo (soluble) over BoltzGen, AND motivates
   BindCraft (built-in Surface_Hydrophobicity/liability filters keep the NON-interface surface polar).

Novelty table rebuilt (coverage-wtd foldseek + pLDDT gate, pLDDT is 0-1 scale):
- **Novel dual-binders (level 3)**: gpu5_17 (covwTM 0.757, pLDDT .70), gpu5_26 (0.761, .80),
  gpu4_28 (0.774, .90 = most trustworthy). All PDB-only lower bounds (AFDB raises) -> portal is the authority.
- gpu4_33 covwTM 0.000 = FALSE novelty (ESMFold garbage: 41aa, pLDDT 0.6, zero foldseek hits). EXCLUDED.
- Switches generated (mech-A, scripts/mech_a_scan.py -> runs/f07/mecha_novel.csv): gpu5_17_mA1(validated)/mA2,
  gpu4_28_mA1/mA2. gpu5_26 yields NO mech-A (no target cation near interface) -> plain-binder or mech-B only.

**BindCraft2 PIVOT** (SOTA, installed+proven in the glp1r project; TfR1 project had only AF2 params):
BindCraft gives soluble + AF2-validated (3rd folder beyond Chai/Boltz) + de-novo binders, with modalities
(binder/large_binder/VHH/scFv/Fab = the 9 submission classes) and properties (**mixed_topology** = alpha/beta
folds rarer in PDB -> beats the "helical bundle caps at 3/4" novelty ceiling; humanize; termini_accessible
for the C-term Twin-Strep tag). This fills the exact gap: BoltzGen=novel+strong+hydrophobic; RFd1=novel+
soluble+weak; **BindCraft target = novel(mixtopo)+soluble+strong**. Campaign prepared:
runs/f12/bc2/mixtopo.json (binder, apical hotspots A203,A209,A211=conserved-anchored, 60-120aa, 0-Cys,
non-helical weights, betasheet>=0.2, iptm>=0.6, 40 finals/400 traj) + smoke.json. Switch installed post-hoc.

GPU STATE: all 8 GPUs are running the USER's GLP1R BindCraft 4-arm campaign (deadline 2026-10-25 = SOONER
than TfR1 2026-11-01). NOT clobbering it. Watcher bcbwo5wzi waits for it to finish, then re-invokes.
Staged for the GPU window: (1) BindCraft TfR1 smoke -> full mixtopo campaign; (2) RFd1 funnel on 1472 staged
seqs (long2 nseq8 1136 + long1 rescue nseq16 336) via self_consistency -> Chai -> Boltz; (3) re-fold the new
switches (gpu5_17_mA2, gpu4_28_mA1/mA2) to confirm binding retained; (4) mech-B multi-His on survivors.
Current best complete design remains gpu5_17 (novel+dual-bind+switch, but hydrophobic). Portfolio target:
diverse soluble novel switch-binders, front-load ~10, user portal novelty check is the final gate.

## 2026-10-23 — GPU window opened; funnel + BindCraft launched
GLP1R campaign finished (watcher bcbwo5wzi hit 48h; live nvidia-smi: all 8 GPUs 0 MiB, no foreign compute apps). Launched three non-contending background jobs:
- **BindCraft smoke** (b6r0x3c86, GPU 0): `bindcraft design runs/f12/bc2/smoke.json` → gate for the full mixtopo campaign; log runs/f12/bc2/smoke.log
- **long2 self-consistency** (bup010hgx, GPUs 1-5): 1136 seqs, backbones=long2_compact → runs/f12/sc/long2/all.csv (ESMFold+TMalign SC + foldseek novelty)
- **long1_rescue self-consistency** (bcyghampl, GPUs 6-7): 336 seqs (21 proven-novel backbones @nseq16), backbones=long1_compact → runs/f12/sc/long1r/all.csv
Driver: scripts/sc_shard.sh (shards self_consistency.py; per-shard struct-dir avoids fs_tmp collision). venv=.venv-esmfold2 (torch2.14+cu130, tfm5.19).
SC gates: self-consistent bb_TM>=0.80 & rmsd<=2.5; novel covwTM<0.80 (robust<0.65).
**NB long2 & long1_rescue share stems** (des_160 etc. = DIFFERENT backbones per batch) → keep outputs namespaced; prefix l2_/l1_ when merging survivors for Chai∧Boltz.
Next: smoke passes → full mixtopo campaign; SC done → filter sc&novel → Chai∧Boltz dual-gate (receptor=data/targets/apical_domain_189_383.seq, mouse=mouse_apical_189_383.seq).

## 2026-10-23 — smoke verdict + funnel results (live)
**BindCraft smoke (b6r0x3c86, non-helical):** config VALID, pipeline works end-to-end (target 195aa, hotspots A203/209/211, forced-targeting lysinated 101/195). 0/4 accepted — 2 strong trajectories (anneal i_pTM 0.83, 0.64) COLLAPSED at harden (0.08, 0.20) = aggressive non-helical pressure fragile under sequence hardening. Helical already clears novelty GATE(≥3); non-helical only pushes toward level-4 target. → running moderate-helix diagnostic.
**smoke2 (bz245pdas, GPU0):** weights_non_helical 1.0→0.3, max_helix_fraction 0.5→0.7, 8 traj → decides full-campaign helix.
**long1_rescue SC (bcyghampl):** 336 seqs → 178 self-consistent&novel (53%, from 21 proven-novel backbones). Top novelty covwTM 0.667-0.72 (solid L3, nearing robust<0.65). bb_TM 0.85-0.98.
**long1r Chai triage (b6653bpwk, GPU6-7):** 178 survivors (l1_ prefix) vs human apical, samples=3 → runs/f12/chai/long1r. Chai-FIRST screen; Boltz-confirm shortlist only (avoids Boltz on ~500).
**long2 SC (bup010hgx, GPU1-5):** 1136 seqs, still running.
GPU map: 0=smoke2 | 1-5=long2 SC | 6-7=long1r Chai. Next: smoke2→campaign helix decision; long2 SC→long2 survivors→Chai; long1r Chai→rank→Boltz-confirm shortlist.

## 2026-10-23 — BindCraft harden-collapse is NOT helix; long2 survivors
**smoke2 (moderate-helix) 0/8** — SAME harden-collapse: every trajectory reaching good anneal i_pTM (0.60-0.75) collapsed at harden (0.09-0.33). → helix content NOT the cause. Systematic suspect: **forced_targeting lysinates 52% (101/195) of target surface** = artificial charge field the binder exploits soft-stage but can't hold when hardened.
**smoke3 (b2n2bjljp, GPU0):** forced_targeting=false, default helix, no final dev-filters = pure "can BindCraft bind this apical target at all" feasibility test. If 0/8 again → cut BindCraft (target too hard), go all-in RFd1 funnel + switch. If accepts → reintroduce constraints.
**long2 SC:** 255 sc&novel (8 robust covwTM<0.65: des_81_mpnn3 0.571, des_214_mpnn5 0.573...). 57 unique backbones. → Chai triage bkj0arm8o GPU1-5.
**parse_boltz.py:** added "apical" hotspot set + l1_/l2_→apical mapping (correct on-epitope contact counting for RFd1 designs).
GPU map: 0=smoke3 | 1-5=long2 Chai | 6-7=long1r Chai.

## 2026-10-23 — BindCraft root-caused via GLP1R working config
**smoke3 (forced_targeting OFF):** traj1 PASSED harden at i_pTM=0.79 (real AF2 interface!) then died at MUTATE (0.79→0.18, pLDDT→0.42). Two tunable killers: forced_targeting (harden) + mutate-stage MPNN interface-redesign (binding, = af2-seq-specific lesson).
**Root cause via GLP1R campaign_settings.json (produced 30 designs, same install):** my minimal configs left defaults. Key proven levers missing: **redesign_interface=false** (no interface MPNN-redesign at mutate), **sequence_candidates=10 / kept_sequences=1** (10 MPNN tries, keep best), **min_plddt_mutate=0.55** (I had 0.65), explicit min_iptm_harden/mutate=0.5, mpnn_variant=negative, full filters/losses/weights blocks.
**apical_test.json (bvzhr22fm, GPU0):** GLP1R config + overrides {modality binder, lengths 60-120, forced_targeting FALSE, hotspots A203/209/211, 30 traj, 5 designs}. Dev left permissive (aa_bias C:0) → post-filter. Go/no-go: >=2-3 accepts in 30 → full campaign (450 traj, 40 designs, multi-GPU); ~0 → cut BindCraft, all-in RFd1.
GPU map: 0=BindCraft test | 1-5=long2 Chai | 6-7=long1r Chai.

## 2026-10-23 — STRATEGIC INFLECTION: apical epitope walls de-novo confident binding
**long2 RFd1 Chai (255 survivors): ZERO on-epitope confident binders.** Confident ones (iptm 0.6-0.68) dock OFF-epitope at UniProt 259-300 (stickier patch); on-epitope ones (hot>=3) all iptm<=0.30, ipae>18. Verified NOT a pipeline bug: RFd1 correctly used input=tfr1_apical_189_383.pdb, hotspots=[A202,A209,A211]. De-novo binders simply aren't apical-specific (flat/polar/buried epitope — matches lesson-denovo-wall-flat-polar-target).
**BoltzGen "dual binders" re-examined (f06): weak 2-folder consensus** — gpu5_17 chai0.475/boltz0.809, gpu5_26 0.423/0.852, gpu4_28 0.394/0.812. High Boltz (lineage-biased) but Chai (independent)=0.4 weak. + hydrophobic. Not robustly confirmed.
**BindCraft proven-config test: 0/18 so far** (likely cut if 0/30).
**Conclusion forming:** no method yields a STRONG two-folder apical binder; epitope is the central wall. This is WET-LAB-judged → in-silico = prior, not verdict. Winning play = DIVERSE portfolio of best on-epitope binders (any lineage) + pH-switch, front-load best-evidence, trust wet lab.
**Unexploited lever = PARTIAL DIFFUSION from the BoltzGen apical binders** (pose-preserving; beats de-novo ~11% vs 0.3%; lesson-rfd-partial-diffusion-beats-denovo). Diversify fold toward novelty+solubility while KEEPING the one apical pose that scores. Pending refold (bi6lqhjci) confirms their on-epitope landing + switch-retention first.
GPU map: 0=BindCraft test | 1-5=best-asset refold Chai | 6-7=long1r Chai.

## 2026-10-23 — VALIDATOR WAS BROKEN (positive control 3DS18 drifts to sink)
POSITIVE CONTROL: crystal-true apical binder 3DS18 (6WRV, footprint [199-215,340-376]) blind-co-folded (Chai) vs apical fragment -> docks 259-300 SINK, iptm 0.204, 0 apical contacts. f06 latent evidence: blind POS_3DS18 iptm 0.20 (chai)/0.28 (boltz) — never checked. => blind single-seq co-fold CANNOT validate apical binding here; ALL prior "binders" (RFd1+BoltzGen, both folders) scored the sink. My "nothing binds apical" conclusion was a validator artifact.
FIX: pocket-RESTRAINED Boltz (scripts/prep_boltz_pocket.py; apical chainB resids [14,15,16,20,21,22,23,24,160,183], max_distance 6, force true).
CALIBRATION (bb0dsrhgi, GPU0-5): 33 candidates (30 long2 + 3 BoltzGen) + POS_3DS18 + 2 NEG scrambles. Gate: POS high + NEG low => method discriminates => run full 433 survivors restrained.
BindCraft apical_test: 0/30 even with proven GLP1R config (set aside; AF2 hallucination can't make confident apical binder — but its internal validation is pose-aware so this is a truer 'hard' signal).
Saved memory [[lesson-tfr1-apical-blind-cofold-fails-poscontrol]].

## 2026-10-23 — BREAKTHROUGH: pocket-restrained validator works; real apical binders found
CALIBRATION (pocket-restrained Boltz, force=true): POS_3DS18 ab_iptm=0.863 ipae=5.95 hot=13 (vs 0.20 blind!); NEG scrambles 0.20-0.32 ipae>19 hot=0. Method DISCRIMINATES cleanly. Real apical binders in the 30-design calib subset: l2_des_344_mpnn1 (0.74/ipae8/hot6), l2_des_241_mpnn6 (0.72/hot8), l2_des_136_mpnn1 (0.69/hot10), gpu5_26 (0.76/hot5), ~13 pass ab_iptm>=0.55 & ipae<=12 & hot>=5 & iplddt>=0.8.
FULL VALIDATION (bbj7b5r2e, 8 GPUs): all 440 candidates (long2 255 + long1r 178 + BoltzGen 3 + mechA 4) + 3 controls, pocket-restrained Boltz -> runs/f12/pocket/full_out. Killed obsolete long1r blind Chai (b6653bpwk) to free GPUs.
NEXT: parse full_out -> gate (ab_iptm>=0.55,ipae<=12,hot>=5,iplddt>=0.8 vs POS0.86/NEG0.32) -> INDEPENDENT confirm (Chai pocket-restrained, add restraint support) -> developability -> switch (mech-B multi-His) -> mouse x-react (pocket-restrained vs mouse_apical) -> novelty -> select 20.

## 2026-10-23 — 105 apical binders found (pocket-restrained Boltz); funnel underway
FULL pocket-restrained Boltz (443): controls POS_3DS18 0.848 / NEG 0.23-0.27 (gate valid). 106 pass ab_iptm>=0.55 & ipae<=12 & hot>=5 & iplddt>=0.80 (=105 real + POS). Lineage: 68 long2, 37 long1r, 0 BoltzGen (RFd1 de-novo dominate = soluble+novel). TOP: l2_des_417_mpnn7 (0.892/ipae5.6/hot9/GRAVY-1.16), l1_des_50_mpnn1 (0.834/hot10), l2_des_386_mpnn2 (0.821), several BEAT the positive control.
DEVELOPABILITY (inline GRAVY/Cys/run/charge): 74/105 soluble (GRAVY<0, 0-Cys, hydrophobic-run<=6). All top candidates 0-Cys, GRAVY -0.5 to -1.6 (very soluble). vs BoltzGen +0.95..+1.29.
NOVELTY (covwTM from SC, PDB-only lower bound): 101 L3 (<0.80), only 2 robust (<0.65); most 0.73-0.80 (near edge). Prefer lower covwTM; portal = final authority.
master table: runs/f12/pocket/master.tsv (105 rows: abiptm,iplddt,ipae,hot,L,gravy,nCys,run,chg,covwTM).
IN PROGRESS: Chai pocket-restrained dual-confirm (chai_confirm_in: 48 cand <=2/backbone + controls; watcher b6vhgrhks). THEN: switch pipeline (buried_switch_scan -> build_multihis mech-B 2-3His -> re-fold pocket-restrained to confirm binding RETAINED -> ph_release_consensus) on dual-confirmed soluble novel; mouse x-react (pocket-restrained vs mouse_apical_189_383); select 20 (front-load, <=2/backbone, diversify).

## 2026-10-23 — mech-B switches installed; 12 bind+switch-valid
Dual-confirm (Boltz∧Chai restrained, 48 tested): 8 strong dual + Tier-2 Boltz-strong. Selected 12 (>=0.65 bolt & >=0.38 chai, <=3/bb) for switches.
buried_switch_scan: all 12 have abundant buried K/R anchors (10-24 each) despite net-acidic -> mech-B feasible.
build_switch_combos.py (mech-B, SEP 8A, IFACE_CUT 9A, 2+3 His): 24 switched seqs.
RE-FOLD (pocket-restrained Boltz): 16/24 RETAIN apical binding (ab>=0.55,ipae<=12,hot>=4). Controls POS 0.853/NEG 0.21-0.27.
switch_contacts geometry: 12/16 valid mech-B (His-cation contacts>=2). Strong: l1_des_223_mpnn3_sw3his(11), l2_des_206_mpnn6_sw3his(7), l2_des_374_mpnn7_sw3his(7), l2_des_25_mpnn0_sw3his(5). sw3his > sw2his switch decisiveness.
=> 12 designs: bind apical (dual) + retain binding post-switch + valid mech-B geometry + soluble + novel (L3). From ~9 backbones.
MOUSE X-REACT (b3nq1qsmt, running): pocket-restrained Boltz vs mouse_apical (only 4/10 epitope pos conserved: 202/203/209/210 hydrophobic; 6 divergent). mech-B is target-independent so switch transfers; binding transfers iff interface on conserved core.
NEXT: mouse results -> rank (binding+switch+xreact+novelty+dev) -> select <=20, front-load 10, <=2/bb.

## 2026-10-23 — PORTFOLIO: 14 switch-valid human-binding designs (9 backbones)
Switch cycle 2 (cross-reactive backbones l1_des_215,l2_417,l2_408,l2_270): adds l2_des_417_mpnn7_sw3his (hum0.84/mou0.72/ratio0.86/swG2 = strong triple-winner), l1_des_215 (xreact,marginal bind), l2_408_sw2his (0.75,swG7 human switch). (geom loop bug: switched.csv is COMMA-sep, cut needs -d,.)
FINAL TABLE (runs/f13/final_table.tsv): 14 switch-valid (swG>=2) & human-binding (hum>=0.55,ipae<=12,hot>=4), 9 backbones.
TIER A triple-winners (switch+xreact+bind): l2_des_25_mpnn0_sw3his(0.65/0.65/r0.99/swG5) & _sw2his(0.62/0.85/r1.38), l2_des_417_mpnn7_sw3his(0.84/0.72/r0.86), l2_des_206_mpnn6_sw3his(0.81/0.46/r0.56/swG7), l2_des_374_mpnn7_sw3his(0.69/r0.51/swG7/covwTM0.674 BEST-novelty).
TIER B switch+bind human-biased: l1_des_223(×3,swG8-11,GRAVY-1.68), l2_des_408, l2_des_107, l1_des_160, l2_des_386.
ALL soluble (0-Cys, GRAVY mostly neg), novel L3 (covwTM 0.67-0.82).
RUNNING: Chai-restrained dual-confirm of the 14 SWITCHED (submitted) seqs (btpm5ktlu) — final gate (esp l2_417 parent Chai-weak).
SUBMISSION fmt: name,sequence,molecule_class=protein; Track2/3 ranked<=20 front-load10 <=2/bb. Validate via scripts/validate_submission.py --track 2. Upload USER-GATED.
RANK PLAN (front-load): triple-winners first (by xreact,switch,bind,novelty), then switch+bind; <=2/bb.

## 2026-10-23 — DEFINITIVE FINAL: 16 switch-valid designs (12 bb, 7 dual-confirmed)
Expansion (10 new backbones): only 3 boltz-only keepers (His mutations broke binding or switch for most new bb). Single-His RESCUE of l2_des_25 -> sw1_A9 DUAL (0.62/0.63) + mouse 0.78 ratio 1.26 + swG3 = TRIPLE-WINNER flagship (#1).
FINAL submissions/tfr1_track2_final.csv (16, ranked, <=2/bb, PASS). Front-7 DUAL-confirmed; front-10 = 7 dual + 3 boltz-only xreact hedges (l2_des_417, l2_des_408). All: mech-B switch (swG>=2), soluble (0-Cys, GRAVY<0.3), novel covwTM 0.67-0.82 (PDB-only L3; portal=authority; lower=safer).
Objectives: #1 switch (all valid mech-B) / #2 xreact (flagship ratio 1.26, several 0.5-0.7) / #3 affinity (bolt 0.58-0.84, 7 dual). Baselines: v1(12), v2(12), final(16) all validated.
UPLOAD USER-GATED. Novelty portal check = final gate before upload.

## 2026-10-23 /ambition-lift reassessment (v3)
- **Flagship upgraded (evidence-based):** old #1 single-His d25_sw1_A9 -> NEW #1 d25_sw2b_A9_A25 (2 His: A9/R13 + A25/R28).
  Reval f15 (clean, POS_3DS18 Chai0.72/NEG0.14): Chai0.50 + Boltz0.53 (dual), x-react ratio 0.96 Chai / 1.50 Boltz (best), mech-B swG4-6.
  Root cause of earlier miss: "des_25 multi-His breaks Chai" was a BAD His pair (A9+A54 Chai0.31); A9+A25 passes (0.50).
- **Top-10 fixed:** dropped Chai-failing d408 (0.178) from top-10; demoted Boltz-only d417 (Chai0.29) + novelty-borderline d107 (covwTM0.82).
- **submissions/tfr1_track2_v3.csv** = 20 ranked, validate_submission --track 2 PASS (0 errors). Prior: final.csv(16), v1/v2.
- **SOTA scan (2 subagents):** keep Boltz/Chai + mech-B buried-His; switch magnitude still unrankable. Gap = generator diversity (organizers' own Aug-2026 protocol: PXDesign/RFd3/Genie3 lead; flat targets->Genie3/PXDesign; SolubleMPNN; ESMFold2+Protenix v2 ipSAEmin filter).
- **STRETCH (in progress):** RFD4-Proteina confirmed working (runs/f16; needs atomworks CIF w/ bonds+label_seq, not PDB/gemmi-cif). Full wave launched (8 GPU x128) targeting conserved apical sub-site (hotspots 202/203/209) for a 2nd x-react lineage + novel folds. Next: SolubleMPNN -> dual-species screen -> switch -> triple-confirm (Boltz+Chai+Protenix v2, ipSAEmin). +PXDesign/Genie3/RFd1-conserved planned.

## 2026-10-23 RFD4-Proteina generator-diversity campaign (v4)
- RFD4-Proteina (NVIDIA, user-flagged) run targeting the CONSERVED apical sub-site (hotspots 202/203/209). Input contract: atomworks CIF with bonds+label_seq (not PDB/gemmi-cif).
- wave1 1024 -> 982 soluble 0-Cys (92%, GRAVY med -0.18) -> 237 novel (maxTM<0.80) -> 154 human-binders (clean calib POS0.85/NEG0.23) -> 8 cross-reactive (ratio>=0.8) -> Chai: g7_1 dual-confirmed x-react (ratC0.92).
- wave2 900 -> 797 soluble -> 203 novel -> 117 human-binders -> 3 cross-reactive (g5_14 ratio1.15, g2_132, g2_137).
- KEY RESULT: RFD4 yields excellent NOVEL SOLUBLE cross-reactive BINDERS beyond des_25 (breaks the RFd1 x-react wall), BUT auto-placed mech-B buried-His switch loses geometry on these backbones (mechB 0-1 after refold) - same wall des_25 hit (only specific His pairs retain). Only g7_8_sw2his got a valid switch (mech-A, total4).
- v4 = v3 core (des_25_sw2b_A9_A25 flagship retained) + 4 RFD4 lineages (g7_8 valid-switch #6; g7_1/g5_14/g2_132 x-react depth) replacing 4 weakest v3 hedges. submissions/tfr1_track2_v4.csv validated PASS (20/0/0).
- All 8 GPUs utilized throughout (packed folding + 6-GPU generation waves).

## 2026-10-24 portal novelty + g7_1 switch rescue (v5)
- Portal novelty on v4: 19/20 PASSED; d107_m5_sw2his NOT PASSED ("contains a known binder fragment") - matches its covwTM 0.82 flag. Dropped.
- g7_1 per-backbone His-pair tuning (13 combos: singles+pairs across K15/R36/K42): NONE achieved valid mech-B geometry (mechB 0-1 after refold); g7_1 backbone cations don't retain His contact. mech-A would be species-specific. => g7_1 stays an x-react BINDER hedge, no designable switch. Reconfirms des_25_sw2b_A9_A25 as the unique switch+x-react design.
- v5 = v4 minus d107; g7_1/g5_14/g2_132 (no valid switch) demoted to hedge ranks 11-13; d386 promoted to #10; g6_32_sw2his added #20. Top-10 now all valid-switch designs. submissions/tfr1_track2_v5.csv validated PASS. (Re-run portal on v5: g6_32 is new, unchecked.)

## 2026-10-24 v6: 20 distinct backbones (remove within-upload redundancy)
- User: no "similar designs in this upload" (v5 reused des_25/206/223/4 across switch variants).
- Switch-installed + refolded 12 fresh distinct RFD4 backbones (top novel human binders): 8 dual-confirmed; g4_5_sw3his VALID-SWITCH (swG2); g1_15 (Bh0.95/Ch0.83), g0_96 (0.94/0.80) strong binders (swG0-1).
- v6 = 20 DISTINCT backbones, one design each, ranked by objective priority: valid-switch tier (des_25 flagship, des_206/223/374/4, g7_8, g4_5, des_386) -> x-react hedges (g7_1/g5_14/g2_132/d417) -> strong distinct binders (g1_15/g0_96/g7_73/g6_7/g4_91/g4_92/g5_24/g6_32). No shared backbones.
- submissions/tfr1_track2_v6.csv validated PASS. NOTE: 9 new RFD4 designs unchecked on portal novelty (from novel pool maxTM<0.80; re-run portal before upload).

## 2026-10-24 v7: 4-fold re-ranking of the 20 (organizers'-style ipSAE_min + switch cross-check)
- GOAL: align the front-loaded order (selector takes <=10 from TOP, row-order = ranking) to a rigorous
  re-score, since v6's within-tier order rested on the construction folds only. Re-scored ALL 20 v6
  designs on a UNIFORM 4-fold panel: {Boltz-2, Chai-1} x {human, mouse}, pocket-restrained, single-seq,
  POS_3DS18/NEG-scramble calibrated. runs/f17/. Scripts: score_ipsae.py (ipSAE via patched ipsae.py),
  switch_contacts.py on each fold, merge_rank.py (ipSAE_min = worst-case over folders per species).
- CALIBRATION: Boltz-h POS 0.55 / NEG 0.00; Chai-h POS 0.67 / NEG 0.00. Boltz-m POS_3DS18=0.00
  (correct: 3DS18 human-specific) but Chai-m POS=0.47 (Chai-mouse PERMISSIVE on x-species) -> use
  mouse ipSAE_min=min(Boltz-m,Chai-m), which correctly discounts Chai's spurious highs (g7_1 Chai-m 0.48
  but Boltz-m 0.01 -> min 0.01).
- #1 SWITCH (switch_contacts, Baker floor>=2, counted across all 4 folds): 4/4 ROBUST = d25, e223,
  d374, d206, g5_24; 3/4 = g7_73; 2/4 = g4_5, d4, d386; <=1/4 (did NOT hold) = g7_8 (v6 #6!), g7_1,
  g5_14, g2_132, d417, g1_15, g0_96, g6_7, g4_91, g4_92, g6_32. Switch validity is FOLD-DEPENDENT
  (cross-fold count is the robust signal). g7_73 & g5_24 (v6 bottom tier) have robust switches.
- #2 X-REACT (mouse ipSAE_min, floor ~0.15): d25 0.37, d417 0.23 (but barely binds human), g5_14 0.19;
  g4_92 borderline 0.11. Confirms x-react is rare; d25 the clear standout (also best on both folds).
- #3 AFFINITY (human ipSAE_min): robust strong binders g1_15 0.79, g0_96 0.77, g4_92 0.70, g6_7 0.69,
  g4_5 0.61, g7_73 0.58. FOLDER-DEPENDENT over-confidence CAUGHT: d386 (Boltz 0.73 but Chai 0.29 ->
  min 0.29), d4 (0.72->0.45). Weak binders (<0.40): d386, d374, d206, g5_24, g2_132, d417.
- CROWN: d25_sw2b_A9_A25 is the ONLY design valid on all three (switch 4/4, x-react 0.37, binds 0.41),
  robust across all 4 folds. Flagship #1 re-confirmed independently.
- v7 ORDER (affinity-floor ~0.40 gate, then lexicographic #1>#2>#3): d25, e223, g7_73, g4_5, d4,
  g5_14, g4_92, g1_15, g0_96, g6_7 (top-10) | d374, d206, g5_24, g6_32, d386, g7_1, g4_91, g7_8,
  d417, g2_132. SAME 20 SEQUENCES as v6 (re-order only) -> portal novelty 20/20 still holds.
  submissions/tfr1_track2_v7.csv validated PASS. v6 frozen as fallback. Upload USER-GATED.
- SWITCH SEARCH -> 2nd CROWN (runs/f17/sw_search, sw_rep, sw_mouse, sw_chai_*): exhaustive mech-B
  His-pair search (scripts/exhaustive_switch.py) on g5_14 (confirmed x-react dual-species binder whose
  v6 switch was marginal). 45 combos; found the v6 greedy pick (A13/R19+A39/K43) was marginal
  (frac>=2 = 0.20 across 5 replicate folds) while K31-anchored combos are ROBUST.
- KEY METHOD FIX: switch_contacts on a SINGLE Boltz fold is noisy (same seq gave total 1 vs 5 on
  different folds). Fixed by REPLICATE folding (DIFF_SAMPLES=5) + frac>=2 (scripts/switch_prob.py),
  calibrated: POSctrl e223 frac 1.00/d25 1.00, NEGctrl g0_96 0.00, marginal g5_14_sw2his 0.20. NOTE:
  DIFF=5 gives NOISY ipSAE (binding) -> use DIFF=1 for binding, DIFF=5 for switch probability.
- CROWN 2 = rfd4_g5_14_sw2b_A34_A50 (g5_14 + His A34/K31 + A50/K53). DUAL-FOLDER x DUAL-SPECIES
  confirmed: switch 4/4 folds valid (Boltz-h frac 1.00 mean4, Boltz-m 4, Chai-h 3, Chai-m 3);
  x-react ipSAE_min(Boltz-m,Chai-m)=0.185; binding ipSAE_min(Boltz-h,Chai-h)=0.382; novelty 0.737
  (NOVEL, = parent g5_14 which passed portal 20/20). A 2nd all-three design, DIFFERENT fold family
  (RFD4) than d25 (RFd1). (switch GEOMETRY validated, not magnitude — magnitude stays unrankable.)
- v8 = v7 with the crown REPLACING the old no-switch g5_14_sw2his (same backbone -> still 20 distinct):
  #1 d25 (x-react 0.37), #2 g5_14 crown (x-react 0.185), then e223/g7_73/g4_5/d4 (switch+binds),
  g4_92 (x-react+binds), g1_15/g0_96/g6_7 (binders) | 11-20 switch/binder hedges. validate PASS.
  submissions/tfr1_track2_v8.csv. **1 NEW sequence (the crown) vs the portal-checked v6/v7 set ->
  re-run Proteinbase portal novelty before upload** (local oracle novel 0.737; low risk). v7 = fully
  portal-verified fallback; v6 = original frozen fallback. Upload USER-GATED.

## 2026-10-24 v9 campaign (runs/f18): validate against the ORGANIZERS' EXACT JUDGE (selection prompt)
- User supplied the organizers' selection prompt. KEY: they co-fold BLIND vs the FULL ectodomain
  HOMODIMER (human 121-760 / mouse 123-763, UniProt-exact; my prior work used the apical FRAGMENT
  189-383) and score 3 screens: pLDDT, ipSAE, Kyte-Doolittle hydropathy. Built exact constructs from
  UniProt P02786/Q62351 (Tyr211 -> construct pos 91). Scripts: prep_blind_cofold, epitope_read,
  epitope_prob, build_pool, exhaustive_switch(reuse).
- DECISIVE CALIBRATION RESULT: the BLIND co-fold is UNRELIABLE on this target at EVERY scale.
  * ipSAE ~= 0.000 for ALL designs INCLUDING POS_3DS18 (the real crystal binder) on the full ectodomain
    -> the organizers' ipSAE screen CANNOT discriminate TfR1 apical designs.
  * ipTM does not separate signal from noise (NEG_scramble ipTM 0.75 > POS 0.58 on the homodimer).
  * Epitope read swings wildly: POS reads apical_frac 0.72 (monomer DIFF1), 0.20/helical0.80 (monomer
    DIFF5), apical 1.00 (homodimer DIFF1), 0.20/helical0.80 (homodimer DIFF5). The positive control
    drifts to the helical/transferrin face as much as the designs -> epitope read is NOISE, even on the
    organizers' exact homodimer construct, even de-noised over 5 replicates.
- CONSEQUENCE: the blind full-target signals (ipSAE/ipTM/epitope) are all non-discriminating. This
  CONFIRMS the fragment pocket-restrained methodology (v7/v8) was correct, and voids the "crowns drift
  helical" worry (POS drifts identically). The real-judge discriminators = SWITCH mechanism (physical,
  replicate-validated) > x-react (fragment) > apical binding competence (fragment pocket-restrained),
  plus developability (pLDDT: ALL pass 0.9-1.0; hydropathy: current 20 mostly soluble, g7_73 borderline
  +0.09) and novelty (L4). The organizers weight switch #1 and "no single in silico metric decides."
- POOL SWITCH-INSTALL (Phase A/B): screened a 1567-design pool (RFD4+RFd1, novel+soluble) -> 104
  fragment-binders -> exhaustive mech-B His-pair search (scripts/exhaustive_switch) -> replicate-fold
  switch P (scripts/switch_prob) -> dual-folder (Boltz+Chai) confirm binding + x-react + novelty.
  Yielded ~10 NEW dual-confirmed switch-designs (switch-vs-binding tension: strongest binders g0_146/
  g0_125 won't take a switch; switch-installable backbones are moderate binders; His install degrades
  binding for ~half). STANDOUT: rfd4_g5_120_sw2b (binding ipSAE_min 0.853 = strongest in the campaign +
  robust switch). 3rd CROWN found: rfd4_g1_133_sw2b_A10_A20 (switch Boltz-robust + x-react dual 0.244 +
  bind 0.349, novel 0.732).
- **v10 = FINAL/recommended (submissions/tfr1_track2_v10.csv + _evidence.csv), validate PASS.** 20
  distinct backbones, **16 switch-designs (incl 3 CROWNS: d25 xr0.37, g5_14 xr0.185, g1_133 xr0.244)**
  + 4 hedges (g4_92 xr+bind, g1_15/g0_96 strongest binders, d417 xr). Replaced 9 weak/no-switch v8
  designs with 8 new strong-binder switch-designs (g5_120/g2_138/g6_72/g1_69/g1_133/g1_76/g4_66/g4_93).
  Ranked switch(#1 clear mechanism) > x-react(#2) > fragment binding(#3), + pLDDT(all pass) + hydropathy
  + novelty. **8 NEW sequences -> re-run Proteinbase portal novelty before upload** (local oracle all
  NOVEL 0.69-0.74). Graduated fallbacks: v9 (4 new), v8 (2 crowns), v7 (same 20 seqs as v6, portal
  20/20 verified), v6. Upload USER-GATED.

## 2026-10-24 v10 PORTAL NOVELTY VERIFIED (20/20) — last gate cleared
- User ran the Proteinbase portal on v10's 20 sequences. Result: **"20 included • 0 needing fixes"**,
  every row Passed (all Single chain), **NO novelty / "similar designs" / "known binder fragment"
  flags** (that flag is what failed d107 in v4 — its absence = novelty gate clear).
- **Byte-verified the portal validated the EXACT v10 file:** all 20 names, row order (rows 2-21),
  sequence prefixes (first 12), suffixes (last 8), and lengths match submissions/tfr1_track2_v10.csv
  (d25=110, g5_14=71, g1_133=70, g5_120=99, e223=106, g4_5=94, g2_138=63, g6_72=69, d4=109, g1_69=83,
  g7_73=109, g1_76=94, g4_66=71, g4_93=72, d374=115, d206=124, g4_92=64, g1_15=70, g0_96=102, d417=106).
- The 9 sequences new since the portal-verified v6/v7 baseline (re-His'd g5_14 crown + 8 pool
  switch-designs g5_120/g2_138/g6_72/g1_69/g1_133/g1_76/g4_66/g4_93) ALL cleared. _v10_evidence.csv
  portal column updated re-check -> pass(2026-10-24).
- **v10 is now fully portal-verified (format + novelty). Ready to upload; upload remains USER-GATED.**
  Commit is LOCAL (push user-gated).

## 2026-10-24 v11 campaign (runs/f19): break the x-react floor (user: "replace a lot at all costs")
- **Why:** v10's weak axis is x-react (only 3 crowns) + 4 no-switch hedges (ranks 17-20). Revalidated the
  16 pool switch-designs on the COMPLETE dual-folder×dual-species panel (scratchpad/merge_xreact.py):
  robust x-react (ipSAE_min over Boltz∧Chai) is real for ONLY g1_133 (0.244, already in v10). The high
  Chai-mouse hits (g6_72 0.62, g5_120 0.41, g4_93 0.30, new g6_78 0.28, g0_37 0.21) are ALL contradicted
  by Boltz-mouse (~0.01) = folder-pessimism; ipSAE_min correctly rejects. POS_3DS18 human 0.595/mouse
  0.000, NEG 0.000 (calibrated).
- **Gap found:** x-react screen was INCOMPLETE — only the 16 switch-designs were mouse-folded, but the
  binder shortlist has 202 (104 human-scored, 62 with Boltz-h>=0.30, 27 with >=0.5 never x-tested).
- **LAUNCHED (bg bdxsz2vac):** exhaustive mouse x-react screen of the 62 strong binders + 3 controls,
  pocket-restrained dual-folder: Boltz-mouse {gpu0,2,3} + Chai-mouse {4,5} + Chai-human {6,7} (GPU1 =
  foreign job, untouched). runs/f19/{myaml,screen.csv,boltz_m,chai_m,chai_h}. On done: bind_min=
  min(frag_boltz_h,chai_h), xreact_min=min(boltz_m,chai_m); crowns = bind_min>=0.3 & xreact_min>=0.15.
- **Next (pending f19):** switch-install new crowns -> v11 (replace no-switch hedges + weakest). If the
  screen confirms the floor, run joint multi-state (human+mouse) MPNN to DESIGN x-react on crown
  backbones (the one untried SOTA lever). Genie3 (organizers' flat-target generator) available but needs
  a weights DOWNLOAD (user-gated). Judge frozen = v10 pipeline. Upload + push USER-GATED. v10 stands as
  the current best until v11 members are MEASURABLY better.
- **Genie3 APPROVED + BUILT (user: "pull the weights and run it too"):** scripts/setup_genie3.sh built the
  NVIDIA uplifting genie3 kit into third_party/genie3 (venv_g3, torch 2.7.1) + fetched weights
  (weights/genie3/pretrained/v1, step=600000.ckpt pinned OK); `run.sh check` h100/fast would_activate=True.
  Dataset `tfr1_apicalbench` (scripts: extract_apical.py + make_g3_dataset.py, staged runs/f20, copied into
  the kit) = apical fragment = UniProt 189-383 (contiguous), target PDB chain B renumbered 1-195. HOTSPOTS
  = conserved sub-site frag {14,15,21,22} = UniProt {202,203,209,210} = I,V,L,V, compact (max CA-CA 6.4A)
  -> biases toward CROSS-REACTIVE binders. scripts/gen_genie3_tfr1.sh (per-GPU shard, H100 fast line).
  Smoke test (n=2, GPU3) launched b78khpc0v; full gen (N=840, 7 GPUs) launches after f19 frees GPUs.
  Downstream funnel (MPNN->ESMFold/novelty->pocket Boltz∧Chai human+mouse->switch-install) reuses existing
  f12-f19 scripts. FUNNEL DE-RISKED (validated on smoke backbones):
  - Genie3 outputs CA-ONLY traces (binder=chain A, target=chain B, both CA). No PULCHRA available.
  - SOLUTION: ProteinMPNN CA-only model (weights/proteinmpnn/ca_model_weights/v_48_010.pt, --ca_only) runs
    directly on CA traces -> real binder seqs (fixed_chains=['B'], designed=['A']). No backbone rebuild.
  - proteinmpnn kit built (scripts/setup_proteinmpnn.sh -> third_party/proteinmpnn; 'check' step fails on
    torch-metadata but IRRELEVANT: stock third_party/proteinmpnn/stock/src/protein_mpnn_run.py + helper
    parse_multiple_chains.py + the fetched soluble/vanilla/ca weights all work via .venv-boltz python).
  - This fork LACKS assign_fixed_chains.py -> build chains.jsonl manually {name:[['A'],['B']]}.
  - MPNN seqs will be GRAVY/hydropathy-filtered downstream (CA model isn't soluble-biased).
  - Gotcha fixed: g3 problem JSON needs ABSOLUTE target paths (parse_pdb opens relative to CWD).

## 2026-10-24 f19 RESULT: 2 NEW x-react crowns + Genie3 waves running
- **f19 x-react screen DONE (bdxsz2vac, 65 designs scored).** Control calibration: Boltz-mouse is the
  RELIABLE discriminator (POS_3DS18 mouse=0.000 correct, NEG=0) while Chai-mouse is OPTIMISTIC (POS
  mouse=0.484 false-pos) -> xreact_min=min(boltz_m,chai_m) correctly rejects Chai false positives.
- **2 NEW ROBUST CROWNS** (bind_min>=0.3 & xreact_min>=0.15, BOTH folders agree on mouse):
  - rfd4_g7_tfr1_apical_xreact_mini_8: bind 0.517, xreact 0.240 (bM 0.305/cM 0.240), TM 0.74, 86aa
  - rfd4_g6_tfr1_apical_xreact_mini_7: bind 0.752, xreact 0.222 (bM 0.222/cM 0.243), TM 0.663(!), 105aa
  These were PRE-switch binders missed by the 16-design subset (only 16 of 202 were mouse-folded before).
  merge: scratchpad/merge_f19.py. Doubles the binder-level x-react yield (g1_133-class).
- **Switch-installed both** (scripts/install_switch.sh -> runs/f21/sw/switched.csv): g6_7_sw2his
  (A38H/K65;A69H/K104), g7_8_sw2his (A14H/K20;A39H/K72), g7_8_sw3his (+A78H/K82).
- **VALIDATING (beut5xsd4, GPU0):** scripts/val_switch_f21.sh — did bind+xreact survive His install +
  is switch robust? pocket dual-folder DIFF=1 (bind/xreact) + DIFF=5 switch_prob. Pass = bind_min>=0.3,
  xreact_min>=0.15, valid switch -> up to 2 NEW submission crowns for v11 (v10 has 3).
- **Genie3: wave1 DONE (240 backbones), wave2 RUNNING (bo6m428mi, GPUs 1,3,5,6, ~600).** Foreign jobs on
  GPUs 2,4(okc-muse-spark),7 -> avoided. Next: funnel both waves (CA-MPNN -> SC/novelty -> pocket fold
  human+mouse -> switch-install).

## 2026-10-24 f21 switch verdict (beut5xsd4) + exhaustive search + Genie3 funnel started
- **Switch-install verdict on the 2 new crowns (greedy pick):**
  - g7_8_sw2his: bind_min 0.379 ✓, xreact_min 0.205 ✓ (bM 0.205/cM 0.233 BOTH agree!) BUT switch = only
    1 robust His-cation contact (mean 1.0, frac>=2=0.00) = GENTLE single-His, not sharp 2-His. A valid
    gentle-switch x-react crown (better than v10's d417 sw1 hedge), upgrade pending.
  - g6_7_sw2his: bind 0.663 ✓ but xreact LOST (bM 0.014; His install killed mouse binding); no 2-His.
  - Same wall as RFD4 pool: sharp mech-B switch rarely holds on these backbones (only des_25, g5_14 cracked
    it via per-backbone exhaustive search).
- **EXHAUSTIVE His-pair search (b3abp4zty, GPU 5,6,7):** 52 combos (g7_8: 40 anchors K16/20/42/72/82;
  g6_7: 12 anchors K65/104) folded DIFF=5 -> switch_prob, to find a robust 2-His combo preserving x-react.
  runs/f21/exh/. Then confirm bind+xreact DIFF=1 dual-folder on the switch-robust combos.
- **Genie3 funnel stage1 (bswrakrxz, GPU1):** 840 backbones consolidated -> CA-MPNN (ca_model v_48_010,
  design A/fix B, 0-Cys) -> runs/f22/mpnn.csv. Next: self_consistency (ESMFold bb_TM>=0.80 + novelty
  covwTM<0.80) -> pocket Boltz∧Chai human -> binders -> mouse x-react -> switch-install.
- GPU contention HIGH (foreign jobs on 0,2,3,4 incl okc-muse-spark) -> steering to free GPUs only.
- v10 (3 crowns) STILL the baseline. v11 candidates so far: g7_8 (x-react, switch upgrade pending).

## 2026-10-24 4th CROWN confirmed + Genie3 funnel s2 (self-consistency)
- **NEW 4th CROWN: rfd4_g7_8_sw2b_A14_A41** (exhaustive His search cracked it, like g5_14):
  seq STEDEFNSLVDDIHEKINNKDALKTKYKWLYTDLVNSLNHHKSAELAIILLDLYDKNQTDTANELLKAVKEKDYTKAIDILKNSTS (86aa).
  Combo A14H/K20 + A41H/K42: ROBUST 2-His switch (frac>=2=1.00, always 2 contacts) + bind_min 0.513 +
  xreact_min 0.234 (bM 0.234/cM 0.239 BOTH agree) + novel (parent TM 0.74) + soluble (hyd -0.66).
  Matches v10's best crown (g1_133 0.244) on x-react. Alternates (same backbone, pick ONE): 3-His
  _A14_A41_A39 (sharper switch mean2.4, xreact 0.228), _A41_A12 (bind 0.610, xreact 0.223).
  -> v11 will have 4 CROWNS (d25, g5_14, g1_133, g7_8). g6_7 x-react died on His install (dropped).
  NEW SEQ -> portal novelty re-check before upload.
- **Genie3 funnel: MPNN done (840 bb -> 1680 seqs, runs/f22/mpnn.csv).** s2 self_consistency launched
  (sc_shard, ESMFold bb_TM>=0.80 + novelty covwTM<0.80, 7 GPUs) -> runs/f22/sc. NOTE: launched with a
  bad inner '&' -> verify sc_shard alive + relaunch clean if orphaned. Survivors -> pocket Boltz∧Chai
  human -> binders -> mouse x-react -> switch-install -> v11 Genie3 additions.
- **Funnel s2 DONE: 1680 seqs -> 1578 self-consistent (bb_TM>=0.80) + 1076 novel -> 1000 BOTH** (572
  unique backbones). Genie3+CA-MPNN fold back excellently. runs/f22/sc/all.csv.
- **Funnel s3 RUNNING (b9i9m44r8, GPU 1-7):** top 300 by novelty (covwTM 0.555-0.733, 54 robustly novel
  <0.65; deduped best-per-backbone) -> human pocket Boltz + score (runs/f23). Binders (ipSAE>=0.3) then
  go to mouse+Chai x-react -> switch-install. Then assemble v11 = 4 crowns + Genie3 switch-designs,
  replacing v10 no-switch hedges. All new seqs -> portal novelty re-check before upload (USER-GATED).

## 2026-10-24 f23 BREAKTHROUGH: Genie3 -> 6 dual-folder x-react CROWNS
- **Genie3 funnel s3 (runs/f23): 300 novel designs -> human Boltz: 156 binders (52%!), 74 ipSAE>=0.5**
  (far better than RFD4 pool). Top 0.82. Genie3 is the right generator for this flat apical target.
- **Mouse screen (Boltz, reliable) on 156 -> 9 with boltz_m>=0.15 -> Chai dual-folder confirm -> 6 CROWNS**
  (bind_min>=0.3 & xreact_min>=0.15, BOTH folders): w2g5_111 (bind0.418/xr0.325), w2g5_59 (0.520/0.310),
  w2g6_144 (0.707/0.242), w2g1_118 (0.506/0.204), w2g3_19 (0.511/0.194), w2g1_108 (0.583/0.162). Several
  BEAT v10's best crown (g1_133 0.244) on x-react. Targeting the CONSERVED sub-site (202/203/209/210)
  worked decisively. (Bug: first confirm job had $PY unset via '& ' subshell; re-scored clean.)
- **These 6 are PRE-SWITCH.** f24: install_switch + exhaustive His search -> 178 combos -> DIFF=5
  switch-fold search RUNNING (b1of5ruvr, GPU 2-7) -> switch_prob. Robust-switch combos then confirmed
  for bind+xreact retention. Each surviving switch = a v11 Genie3 crown.
- POTENTIAL v11: v10's 3 crowns + g7_8_sw2b + up to 6 Genie3 crowns = up to 10 CROWNS (vs v10's 3).
  Switch-install wall will cull some (RFD4 pattern). All new seqs -> portal novelty re-check (USER-GATED).

## 2026-10-24 f24 RESULT + v11 ASSEMBLED (7 CROWNS, validated PASS)
- **All 6 Genie3 crowns accepted a ROBUST switch** (frac>=2 0.8-1.0) — MUCH better than RFD4 (only g7_8
  cracked). After bind+xreact re-confirm (DIFF=1 dual-folder): **3 CONFIRMED Genie3 switch-crowns** +
  3 switch-binders:
  - genie_w2g6_144_sw3b: bind 0.710, xreact 0.311 (BEST new crown), covwTM 0.676, GRAVY -0.74
  - genie_w2g5_111_sw2b: bind 0.425, xreact 0.254, covwTM 0.640 (2-His; 3-His lost x-react)
  - genie_w2g3_19_sw2b:  bind 0.543, xreact 0.222, covwTM 0.703
  - switch-binders (x-react <0.15): w2g1_118 (0.532/0.146), w2g1_108 (0.582/0.144), w2g5_59 (0.497/0.013)
  All 0-Cys, soluble (GRAVY neg), 3 robustly novel (covwTM<0.68).
- **v11 = submissions/tfr1_track2_v11.csv + _v11_evidence.csv — validate PASS (20/0/0, anarci yes).**
  20 DISTINCT backbones, 7 CROWNS (front-loaded 1-7), ALL valid-switch, 6 Genie3 + g7_8 added, v10
  no-switch hedges (g4_92/g1_15/g0_96/d417) + weakest (g4_66/g4_93/g1_76) DROPPED. Ranked switch(#1,all
  valid)>x-react(#2)>binding(#3). Top crowns beat v10's best (w2g6_144 0.311, w2g5_111 0.254 vs 0.244).
  vs v10: 7 crowns (was 3), 20/20 switch (was 16), +6 fresh Genie3 lineages (robustly novel).
- **7 NEW seqs (6 Genie3 + g7_8) -> portal novelty re-check before upload (USER-GATED).** Genie3 crowns
  robustly novel (low risk). Fallbacks: v10 (portal 20/20), v7. Upload + push USER-GATED.

## 2026-10-24 f25/f26 + v12 FINAL: 10 CROWNS (Genie3 pool exhausted)
- **f25 (remaining 272 novel Genie3 backbones): 158 binders (58%) -> 7 mouse-positive -> Chai confirm
  -> 5 more dual-folder x-react crowns** (w2g3_53 xr0.381 = BEST of campaign, w1g0_112 0.309, w2g5_27
  0.295, w2g3_21 0.254, w2g6_99 ... pre-switch). **ALL 5 took ROBUST switches** (f26, frac>=2=1.00).
  After bind+xreact re-confirm: **3 CONFIRMED switch-crowns** (w2g3_53 bind0.481/xr0.280, w1g0_112
  0.302/0.217, w2g5_27 0.457/0.173) + 2 switch-binders (w2g6_99 xr0.246/bind0.24, w2g3_21 xr0.145).
- **Genie3 pool FULLY EXHAUSTED: 572 novel backbones folded -> 11 binder-level x-react crowns -> 6
  Genie3 switch-crowns total** (3 from f23 + 3 from f25). Genie3 takes His switches cleanly (unlike RFD4).
- **v12 = submissions/tfr1_track2_v12.csv + _v12_evidence.csv — validate PASS (20/0/0, anarci yes).**
  20 DISTINCT backbones, **10 CROWNS** (front-loaded 1-10, ranked by x-react), ALL valid-switch.
  Sources: 9 Genie3 / 6 RFD4 / 5 RFd1; top-10 = all crowns (6 G3, 3 RFD4, 1 RFd1). Ranks 11-20 =
  switch-binders + strongest-binder g5_120 (0.853) + diverse RFd1/RFD4 switch-designs (wet-lab hedge).
  vs v10: 10 crowns (was 3), 20/20 valid-switch (was 16).
- **10 NEW seqs (9 Genie3 + g7_8) -> portal novelty re-check before upload (USER-GATED).** Genie3 crowns
  robustly novel (covwTM 0.64-0.70). Fallbacks: v11 (7 crowns), v10 (portal 20/20), v7. Upload+push USER-GATED.
- CAMPAIGN CONVERGED: pool x-react screen + Genie3 both exhausted; 10 crowns fills the selector's top-10.

## 2026-10-24 v13 FINAL: crowns VALIDATED (decoy false-crown control) + generator-interleaved top-10
- **Red-team (3-agent workflow) + side-agent flagged Genie3 in-silico reliability** (Genie3's lab-real
  TNF binders once scored as failures). Addressed with TWO decision-critical controls, both PASSED:
  1. **Pose-contact (mechanism):** all 6 Genie3 crowns physically bury the CONSERVED sub-site
     (frag 21/22 = UniProt 209/210, + 14/15) in BOTH human AND mouse poses -> x-react is structurally
     realized, not a score artifact. Breaks the mechanism<->score circularity.
  2. **Decoy false-crown control (runs/f27):** 20 de-novo binders designed for OTHER targets (TNF v27 +
     GLP1R, size-matched 62-110 aa) folded through the EXACT pocket-restrained human+mouse metric.
     **human bind>=0.30: 5/20 = 25% FALSE-POSITIVE** (single-folder human binding is a WEAK gate, as
     warned) BUT **FALSE-CROWN (human>=0.30 AND mouse>=0.15): 0/20 = 0%**. Max decoy mouse ipSAE=0.108
     < 0.15 x-react bar < ALL 10 crowns' xreact_min (0.145-0.37). The MOUSE x-react axis is the
     discriminating filter de-novo non-binders cannot fake; every crown clears it above the decoy ceiling.
- **CONCLUSION: all 10 crowns VALIDATED** (statistically via false-crown=0% + mechanistically via pose).
  The "w1g0_112 bind 0.302 in the decoy band" concern is HUMAN-axis only; its crown rests on xreact
  0.217 > 0.108 ceiling = real. So NO crown demoted below a non-crown (evidence removed the distrust).
- **v13 = submissions/tfr1_track2_v13.csv + _v13_evidence.csv — validate PASS (20/0/0, anarci yes).**
  SAME 20 sequences as v12 (byte-identical, reordered). Top-10 = all 10 validated crowns, INTERLEAVED by
  generator: 4 non-Genie3 crowns at PROTECTED ranks 1/3/5/7 (d25 RFd1 #1, g1_133/g7_8/g5_14 RFD4),
  Genie3 at 2/4/6/8/9/10 -> hedges generator-correlation wet-lab risk at the top WITHOUT sacrificing any
  validated cross-reactive crown. Ranks 11-20 unchanged. evidence adds fc_val col (crown>ceiling on all 10).
- **10 NEW seqs (9 Genie3 + g7_8) -> portal novelty re-check before upload (USER-GATED).** Local oracle:
  all novel (covwTM 0.64-0.78 < 0.80 gate). Fallbacks: v12 (=v13 seqs, pre-interleave), v11, v10 (portal
  20/20), v7. Upload + push USER-GATED. CAMPAIGN COMPLETE: both pools exhausted; crowns validated.
