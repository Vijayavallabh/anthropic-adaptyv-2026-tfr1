export const meta = {
  name: 'tfr1-binding-audit',
  description: 'Adversarially audit all 20 v26 members for true binding-collapse artifacts (positive-control-respecting)',
  phases: [{ title: 'Attack', detail: '3 independent skeptic lenses' }, { title: 'Synthesize', detail: 'conservative verdict' }],
}

const DATA = `
UNIFORM BINDING AUDIT — all 20 v26 TfR1 submission members, ONE calibrated blind-Protenix fold (cuequivariance ruler, n40 = 20 samples x seeds 101,102), human + mouse apical target, POS/NEG folded IN THE SAME RUN.

CALIBRATION ANCHORS (in-run):
  HUMAN: POS_3DS18 iptm 0.208 wepi 0.100 on_epi 0.80 | NEG_scramble floor iptm 0.120 wepi 0.136 | calibrated GATE iptm>=0.194
  MOUSE: POS_3DS18 iptm 0.230 wepi 0.120 on_epi 0.80 | NEG_scramble floor iptm 0.124 wepi 0.057
CRITICAL METRIC FACT: on HUMAN, POS wepi (0.100) is BELOW the NEG_scramble floor (0.136). So wepi/best_epi/on_epi are NOISE on the flat human apical epitope — a "wepi>scramble" or "best_epi>=2" gate FAILS the positive control and must NOT be used to condemn a member. The ONLY calibrated binding signal on human is iptm>=0.194 (POS 0.208 vs NEG 0.120). On MOUSE the epitope metric IS informative (POS wepi 0.120 > NEG 0.057).
KNOWN TRUE-COLLAPSE SIGNATURE (artifacts already excluded from v26 earlier): mouse g4_92 iptm 0.397 on_epi 0.20 be 0 wepi 0.032; g3_22_s2 iptm 0.245 wepi 0.022. Signature = iptm well ABOVE POS AND on_epi<=0.2 AND best_epi 0 AND wepi at/below the scramble FLOOR simultaneously. Marginal single-metric dips are NOT this signature (they are noise).

AUDIT TABLE (v26 rank order). cols: rank design | H_iptm H_wepi H_onepi H_be | M_iptm M_wepi M_onepi M_be
1  genie_w2g3_53__A27HK8_A13HR44        | 0.248 0.079 0.60 2 | 0.248 0.012 0.00 0
2  w3g0_174_mpnn1_sw3his                | 0.283 0.101 0.80 5 | 0.308 0.265 1.00 7
3  resc_v25g3_80_mpnn1__A12HK9_A33HK69  | 0.267 0.183 1.00 6 | 0.277 0.228 1.00 6
4  genie_w2g6_144_sw3b                  | 0.257 0.188 1.00 7 | 0.229 0.000 0.00 0
5  resc_w3g5_70__A85HR7_A51HR17         | 0.224 0.152 1.00 3 | 0.167 0.020 0.20 3
6  resc_v25g3_49_mpnn0__A26HK30_A20HK23 | 0.196 0.085 0.70 5 | 0.214 0.042 0.40 2
7  w3g3_92_mpnn0_sw2his                 | 0.240 0.177 1.00 7 | 0.221 0.029 0.10 0
8  resc_w4g7_217__A19HK68_A26HK29       | 0.290 0.087 0.90 4 | 0.181 0.000 0.00 0
9  resc_genie_w2g5_111__A28HR29_A64HK35 | 0.262 0.165 0.90 7 | 0.210 0.032 0.10 1
10 resc_w4g1_195__A18HK22_A81HK11       | 0.247 0.098 0.80 0 | 0.199 0.051 0.30 1
11 resc_w4g1_286__A30HK12_A62HK45       | 0.357 0.241 1.00 6 | 0.215 0.010 0.10 0
12 resc_w4g0_194__A39HK22_A32HR35       | 0.285 0.073 0.60 6 | 0.217 0.013 0.10 0
13 resc_v25g6_84_mpnn1__A52HK67_A69HK73 | 0.237 0.216 1.00 7 | 0.215 0.000 0.00 0
14 w3g5_231_mpnn1_sw3his                | 0.219 0.111 0.50 0 | 0.211 0.007 0.10 0
15 resc_e223_m3__A17HK21_A34HK37        | 0.209 0.041 0.20 1 | 0.269 0.024 0.10 0
16 w3g7_240_mpnn1_sw3his                | 0.241 0.104 0.80 4 | 0.216 0.019 0.10 0
17 ms_g3_65_xr__A28H_A43H               | 0.324 0.116 0.70 0 | 0.189 0.019 0.10 0
18 w4g5_137_mpnn1_sw3his                | 0.234 0.076 0.50 0 | 0.329 0.007 0.00 0
19 ms_g3_22v_xr__A20H_A44H_A66H         | 0.270 0.081 0.70 1 | 0.264 0.088 0.50 7
20 resc_v25g5_109_mpnn0__A11HK42_A19HK23| 0.218 0.155 1.00 7 | 0.192 0.065 0.50 5

CONTEXT: ranks 17 and 19 are NEW multi-state cross-reactive designs (the red-team note's "new designs that score high"); the other 18 are portal-verified v25 rows. Objective priority: pH-switch > mouse cross-reactivity > affinity. The submission requires each member to BIND the HUMAN apical epitope. Pulling a member is costly (forces portal re-run) and there is no better replacement (ceiling confirmed). Raw score TSVs on disk: /home/prachh/work/tmp/claude-1004/-home-prachh-v/437f5686-6960-4582-8739-fda6c6941e67/scratchpad/audit_{human,mouse}.tsv and audit_classified.tsv.
`

const SCHEMA = {
  type: 'object',
  properties: {
    members_to_pull: { type: 'array', items: { type: 'object', properties: {
      rank: { type: 'integer' }, design: { type: 'string' },
      reason: { type: 'string' }, confidence: { type: 'number' } },
      required: ['rank', 'design', 'reason', 'confidence'] } },
    gate_valid: { type: 'string', description: 'Is iptm>=0.194 a trustworthy binding gate here? Could passing members be NEG-like noise?' },
    verdict: { type: 'string', description: 'One-line: does v26 binding hold, or must it change?' },
  },
  required: ['members_to_pull', 'gate_valid', 'verdict'],
}

const lenses = [
  { key: 'iptm-inflation', instr: 'LENS: iptm-inflation. The red-team claim is that HIGH iptm on a flat target means non-specific collapse, not better binding. Attack the high-iptm members (rank11 0.357, rank17 0.324, rank8 0.290, rank12 0.285, rank2 0.283). Make the STRONGEST case each is a collapse-inflated non-binder that should be pulled. But you may NOT use any epitope-overlap gate the HUMAN positive control fails (POS wepi 0.100 < scramble 0.136). Distinguish "iptm above POS" (could be real strong binding) from the true-collapse signature (iptm>>POS AND on_epi<=0.2 AND be0 AND wepi<=floor together).' },
  { key: 'off-epitope-reality', instr: 'LENS: off-epitope reality. Argue that specific members GENUINELY bind off the apical epitope (not metric noise). Focus on members with best_epi 0 and/or low on_epi (rank10 be0/oe0.80, rank14 be0/oe0.50, rank17 be0/oe0.70, rank18 be0/oe0.50, rank15 oe0.20/be1). For each, decide whether the pattern matches the KNOWN true-collapse signature or is within the documented noise (remember POS itself has be~5 but wepi 0.100<scramble 0.136). Only recommend pulling a member whose off-epitope evidence would survive applying the SAME test to POS_3DS18.' },
  { key: 'gate-validity', instr: 'LENS: gate validity / false-pass. Attack the gate itself: POS iptm 0.208 is only barely above the 0.194 gate and NEG is 0.120. Could some "passing" members actually be NEG-like noise that happened to clear 0.194 by chance at n40? Which members sit closest to the gate / least separated from NEG (rank6 0.196, rank15 0.209, rank20 0.218, rank14 0.219, rank5 0.224)? Is n40 enough, or is the separation within sampling noise? Recommend pulling ONLY if a member is statistically indistinguishable from the NEG scramble distribution.' },
]

phase('Attack')
const attacks = await parallel(lenses.map(L => () =>
  agent(`You are a skeptical structural-biology reviewer attacking a protein-design submission. Find real flaws; do not perform agreement.\n\n${DATA}\n\n${L.instr}\n\nReturn members_to_pull (only members you can defend pulling under the positive-control constraint), your gate_valid assessment, and a one-line verdict.`,
    { label: `attack:${L.key}`, phase: 'Attack', schema: SCHEMA })))

const valid = attacks.filter(Boolean)
phase('Synthesize')
const synth = await agent(
  `You are the conservative final arbiter for the TfR1 v26 submission binding audit. Three independent skeptics attacked it; their structured verdicts:\n\n${JSON.stringify(valid, null, 1)}\n\n${DATA}\n\nRULES: (1) A member is pulled ONLY if its binding failure evidence would ALSO condemn the positive control POS_3DS18 is NOT triggered — i.e. the evidence must be specific to that member and not an artifact of the noisy human epitope metric. (2) The only calibrated human binding signal is iptm>=0.194; all 20 pass it. (3) Pulling costs a portal re-run and there is NO better replacement (generation ceiling confirmed). (4) Only recommend a change if at least 2 of 3 skeptics independently flag the SAME member with a positive-control-surviving argument. Produce the final members_to_pull (consensus only), gate_valid, and a one-line verdict on whether v26 binding holds or must change.`,
  { label: 'synthesize', phase: 'Synthesize', schema: SCHEMA })

return { attacks: valid, synthesis: synth }
