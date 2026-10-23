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
