#!/bin/bash
# Generalized Genie3 wave funnel stage 1 (parameterized clone of funnel_s1_mpnn.sh for a single new wave).
# Consolidate ONE wave's backbones under unique names {wlabel}g{gpu}_{i} + CA-MPNN (design binder A,
# fix target B, 0-Cys, v_48_010 since Genie3 emits CA-only traces) -> <out>/mpnn.csv.
# Usage: funnel_wave_mpnn.sh <wave_tag> <wlabel> <out_dir> [gpu=0] [nseq=2]
#   e.g. funnel_wave_mpnn.sh genie3_apical3 w3 runs/f28 0 2
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
M=third_party/proteinmpnn/stock/src
WAVE=${1:?wave_tag e.g. genie3_apical3}; WL=${2:?wlabel e.g. w3}; OUT=${3:?out_dir e.g. runs/f28}
G="${4:-0}"; NSEQ="${5:-2}"
BB=$OUT/bb; mkdir -p "$BB" "$OUT/mpnn"
python3 - "$WAVE" "$WL" "$BB" <<'PY'
import glob, shutil, os, sys
wave, wl, BB = sys.argv[1:4]; n=0
for sh in sorted(glob.glob(f'runs/{wave}/shard_g*')):
    g=os.path.basename(sh).replace('shard_g','')
    for p in sorted(glob.glob(f'{sh}/tfr1_apical/pdbs/*.pdb')):
        i=os.path.basename(p).replace('tfr1_apical_','').replace('.pdb','')
        shutil.copy(p, f'{BB}/{wl}g{g}_{i}.pdb'); n+=1
print('consolidated',n,'backbones ->',BB)
PY
export CUDA_VISIBLE_DEVICES=$G OMP_NUM_THREADS=8
$PY $M/helper_scripts/parse_multiple_chains.py --input_path "$BB" --output_path "$OUT/mpnn/parsed.jsonl" 2>&1 | tail -1
$PY -c "
import json
names=[json.loads(l)['name'] for l in open('$OUT/mpnn/parsed.jsonl')]
json.dump({n:[['A'],['B']] for n in names}, open('$OUT/mpnn/chains.jsonl','w'))
print('chains.jsonl entries:',len(names))
"
$PY $M/protein_mpnn_run.py --jsonl_path "$OUT/mpnn/parsed.jsonl" --chain_id_jsonl "$OUT/mpnn/chains.jsonl" \
  --ca_only --path_to_model_weights weights/proteinmpnn/ca_model_weights --model_name v_48_010 \
  --out_folder "$OUT/mpnn" --num_seq_per_target "$NSEQ" --sampling_temp 0.15 --seed 37 --batch_size 1 --omit_AAs C 2>&1 | tail -3
$PY - "$OUT" <<'PY'
import glob, os, csv, sys
OUT=sys.argv[1]; rows=[]
for fa in sorted(glob.glob(f'{OUT}/mpnn/seqs/*.fa')):
    stem=os.path.basename(fa).replace('.fa',''); lines=[l.rstrip() for l in open(fa)]; k=0
    for i in range(1,len(lines)):
        if lines[i].startswith('>'): continue
        if i>=2:  # skip WT (line 1); keep sampled designs
            seq=lines[i].split('/')[0].strip()
            if seq and set(seq)<=set('ACDEFGHIKLMNPQRSTVWY') and 40<=len(seq)<=140:
                rows.append((f'{stem}_mpnn{k}', seq)); k+=1
w=csv.writer(open(f'{OUT}/mpnn.csv','w')); w.writerow(['name','sequence'])
for n,s in rows: w.writerow([n,s])
print('MPNN binder seqs ->',len(rows))
PY
echo "FUNNEL_WAVE_MPNN_DONE $(date -u +%FT%TZ)  (-> $OUT/mpnn.csv)"
