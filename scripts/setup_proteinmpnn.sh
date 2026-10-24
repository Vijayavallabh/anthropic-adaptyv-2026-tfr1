#!/bin/bash
# Build ProteinMPNN (NVIDIA uplifting kit) into the TfR1 project + fetch SOLUBLE weights, for the
# Genie3 downstream funnel (design binder chain A, fix target chain B, 0-Cys, soluble). CPU/network only.
set -uo pipefail
SRC=/home/prachh/work/cache/uplifting-biomolecular-modeling/proteinmpnn
TP=/home/prachh/v/anthropic-adaptyv-2026-tfr1/third_party
P="$TP/proteinmpnn"
W=/home/prachh/v/anthropic-adaptyv-2026-tfr1/weights/proteinmpnn
mkdir -p "$TP" "$W"
[ -d "$TP/common" ] || cp -r /home/prachh/work/cache/uplifting-biomolecular-modeling/common "$TP/common"
[ -d "$P" ] || cp -r "$SRC" "$P"
cd "$P"
echo "[mpnn-build] $(date -u +%FT%TZ) uv venv py3.10"
uv venv --seed --managed-python --python 3.10 venv_mpnn 2>&1 | tail -3
. venv_mpnn/bin/activate
echo "[mpnn-build] pip install pinned stack"
pip install -q -r environment/requirements-mpnn.lock --src "$P/stock_src" 2>&1 | tail -12
echo "[mpnn-build] rc_lock=$? ; run.sh install (editable + ProteinMPNN clone + soluble weights)"
bash run.sh install --weights "$W" --variant soluble 2>&1 | tail -25
echo "[mpnn-build] rc_install=$?"
echo "[mpnn-build] check:"
bash run.sh check --config h100 --mode exact --variant soluble 2>&1 | tail -12
echo "PROTEINMPNN_BUILD_DONE rc=$? $(date -u +%FT%TZ)"
echo "weights:"; find "$W" -maxdepth 4 \( -iname "*.pt" -o -iname "*soluble*" \) 2>/dev/null | head
echo "protein_mpnn_run.py:"; find "$P/stock_src" -name "protein_mpnn_run.py" 2>/dev/null | head -1