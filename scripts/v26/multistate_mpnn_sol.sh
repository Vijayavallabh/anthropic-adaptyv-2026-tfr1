#!/bin/bash
# Multi-state (human AND mouse) tied ProteinMPNN over a dir of 4-chain constructs.
# Designs ONE binder sequence per backbone compatible with BOTH apical targets -> cross-reactive.
# Usage: multistate_mpnn.sh <cons_dir> <out_dir> <nseq> <gpu|'' for cpu>
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
PYB=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
M=third_party/proteinmpnn/stock/src
CONS=${1:?cons_dir}; OUT=${2:?out_dir}; NSEQ=${3:-8}; GPU=${4:-}
mkdir -p "$OUT"
$PYB $M/helper_scripts/parse_multiple_chains.py --input_path "$CONS" --output_path "$OUT/parsed.jsonl" 2>&1 | tail -1
$PYB - "$OUT/parsed.jsonl" "$OUT/chains.jsonl" "$OUT/tied.jsonl" <<'PY'
import json,sys
parsed,cf,tf=sys.argv[1:4]
ch={}; tied={}
for l in open(parsed):
    d=json.loads(l); n=d['name']; Lb=len(d['seq_chain_A'])
    ch[n]=[["A","C"],["B","D"]]
    tied[n]=[{"A":[i],"C":[i]} for i in range(1,Lb+1)]
json.dump(ch,open(cf,'w')); json.dump(tied,open(tf,'w'))
print("chains+tied:",len(ch),"designs")
PY
CUDA_VISIBLE_DEVICES=$GPU $PYB $M/protein_mpnn_run.py \
  --jsonl_path "$OUT/parsed.jsonl" --chain_id_jsonl "$OUT/chains.jsonl" --tied_positions_jsonl "$OUT/tied.jsonl" \
  --path_to_model_weights weights/proteinmpnn/soluble_model_weights --model_name v_48_020 \
  --out_folder "$OUT" --num_seq_per_target "$NSEQ" --sampling_temp 0.15 --seed 37 --batch_size 1 --omit_AAs C 2>&1 | tail -3
# extract binder seqs (chain-A part, before '/'); skip the native (first) record per fa
$PYB - "$OUT" <<'PY'
import glob,os,csv
OUT=__import__('sys').argv[1]
rows=[]
for fa in sorted(glob.glob(f"{OUT}/seqs/*.fa")):
    stem=os.path.basename(fa)[:-3]; k=0
    lines=open(fa).read().strip().split("\n")
    for i in range(0,len(lines),2):
        h=lines[i]; s=lines[i+1] if i+1<len(lines) else ""
        if h.startswith(">") and "sample=" in h:
            binder=s.split("/")[0]
            if binder and all(c in "ACDEFGHIKLMNPQRSTVWY" for c in binder):
                rows.append((f"ms_{stem}_s{k}",binder)); k+=1
w=csv.writer(open(f"{OUT}/ms_binders.csv","w")); w.writerow(["name","sequence"])
w.writerows(rows); print("ms_binders:",len(rows),"->",f"{OUT}/ms_binders.csv")
PY
echo "MULTISTATE_MPNN_DONE $(date -u +%FT%TZ)"
