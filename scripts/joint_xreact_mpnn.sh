#!/usr/bin/env bash
# Tied multi-state ProteinMPNN on the joint human<->mouse complexes: design interface (A,C tied), fix
# switch-His + core (fixed.jsonl), fix target chains B,D. One sequence optimized for BOTH orthologs.
# CA-only v_48_010 (consistent with how v15 backbones were designed). -> runs/jxr/jxr.csv
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
M=third_party/proteinmpnn/stock/src
OUT=runs/jxr; W=$OUT/mpnn; rm -rf "$W"; mkdir -p "$W"
NSEQ=${NSEQ:-8}; TEMP=${TEMP:-0.2}
export CUDA_VISIBLE_DEVICES=${GPU:-0} OMP_NUM_THREADS=8
$PY $M/helper_scripts/parse_multiple_chains.py --input_path "$OUT/pdb" --output_path "$W/parsed.jsonl" 2>&1 | tail -1
$PY $M/protein_mpnn_run.py --jsonl_path "$W/parsed.jsonl" \
  --chain_id_jsonl "$OUT/chains.jsonl" --fixed_positions_jsonl "$OUT/fixed.jsonl" \
  --tied_positions_jsonl "$OUT/tied.jsonl" \
  --ca_only --path_to_model_weights weights/proteinmpnn/ca_model_weights --model_name v_48_010 \
  --out_folder "$W" --num_seq_per_target "$NSEQ" --sampling_temp "$TEMP" --seed 37 --batch_size 1 --omit_AAs C 2>&1 | tail -3
# extract chain-A binder sequences (first segment before '/'), dedupe, keep valid length
$PY - "$OUT" <<'PY'
import glob, os, csv, sys
OUT=sys.argv[1]; rows=[]; seen=set()
for fa in sorted(glob.glob(f'{OUT}/mpnn/seqs/*.fa')):
    parent=os.path.basename(fa).replace('.fa','')
    lines=[l.rstrip() for l in open(fa)]; k=0
    for i in range(1,len(lines)):
        if lines[i].startswith('>') or i<2: continue   # skip WT (line1) + headers
        seq=lines[i].split('/')[0].strip()
        if seq and set(seq)<=set('ACDEFGHIKLMNPQRSTVWY') and 40<=len(seq)<=140 and seq not in seen:
            seen.add(seq); rows.append((f'jxr_{parent}_{k}', seq)); k+=1
with open(f'{OUT}/jxr.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['name','sequence','parent']);
    for n,s in rows: w.writerow([n,s,n.split('_',1)[1].rsplit('_',1)[0]])
print('joint-xreact candidate seqs:', len(rows))
PY
echo "JXR_MPNN_DONE $(date -u +%FT%TZ)"