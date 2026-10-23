#!/bin/bash
# Stage 2 screen: human pocket-restrained Boltz on a candidate set (clean config = default run_boltz.sh,
# the one that produced the 105-binder master.tsv). prep adds POS_3DS18 + NEG scrambles for calibration.
# Usage: screen_human.sh <seqs.csv name,sequence> <out_dir> "<gpus>"
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/prachh/v/sepiq-2026-challenge/.venv-boltz/bin/python
SEQS=${1:?seqs.csv}; OUT=${2:?out_dir}; GPUS=${3:-0 1 2 3 4 5 6 7}
mkdir -p "$OUT"
"$PY" scripts/prep_boltz_pocket.py --seqs "$SEQS" --out "$OUT/yaml" --force        # auto-adds POS/NEG
echo "[screen_human] $(ls "$OUT"/yaml/*.yaml | wc -l) YAMLs $(date -u +%FT%TZ)"
NOMSA=1 bash scripts/run_boltz.sh "$OUT/yaml" "$OUT/fold" "$GPUS"                   # single-seq (msa:empty, no network), 1 sample
"$PY" scripts/parse_boltz.py --rundir "$OUT/fold" --out "$OUT/scores.tsv"
echo "SCREEN_HUMAN_DONE $(date -u +%FT%TZ)"
echo "--- POS/NEG calibration + top human binders ---"
"$PY" - "$OUT/scores.tsv" <<'PY'
import sys, csv
rows=sorted(csv.DictReader(open(sys.argv[1]), delimiter='\t'), key=lambda r:-float(r['ab_iptm']))
for r in rows:
    if r['name'] in ('POS_3DS18','NEG_scramble1','NEG_scramble2'):
        print(f"  CTRL {r['name']:14} ab_iptm {float(r['ab_iptm']):.2f}")
print("  top10 candidates:")
for r in [x for x in rows if x['name'] not in ('POS_3DS18','NEG_scramble1','NEG_scramble2')][:10]:
    print(f"    {r['name']:34} ab_iptm {float(r['ab_iptm']):.2f} ipae {float(r['ipae']):.1f} hot {r['hot_contacts']}")
PY