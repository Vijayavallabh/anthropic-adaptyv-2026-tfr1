#!/bin/bash
# Build Genie3 (NVIDIA "uplifting" optimized kit) into the TfR1 project + fetch weights.
# CPU/network only (no GPU) -> safe to run alongside the f19 GPU screen. ~10-20 min.
# Copies the kit from the shared cache into project third_party so editable installs stay project-local.
set -uo pipefail
SRC=/home/prachh/work/cache/uplifting-biomolecular-modeling
TP=/home/prachh/v/anthropic-adaptyv-2026-tfr1/third_party
G="$TP/genie3"
W=/home/prachh/v/anthropic-adaptyv-2026-tfr1/weights/genie3
mkdir -p "$TP" "$W"
echo "[g3-build] $(date -u +%FT%TZ) copy kit (genie3 + common) -> project third_party"
[ -d "$G" ] || cp -r "$SRC/genie3" "$G"
[ -d "$TP/common" ] || cp -r "$SRC/common" "$TP/common"
cd "$G"
echo "[g3-build] uv venv py3.10"
uv venv --seed --managed-python --python 3.10 venv_g3 2>&1 | tail -3
. venv_g3/bin/activate
echo "[g3-build] pip install pinned stack (torch 2.7.1 + stock genie3 VCS) — long pole"
pip install -q -r environment/requirements.lock --src "$G/stock_src" 2>&1 | tail -15
echo "[g3-build] rc_lock=$? ; run.sh install (editable kit + weights fetch via hf download)"
bash run.sh install --weights "$W" 2>&1 | tail -25
echo "[g3-build] rc_install=$?"
export GENIE3_WEIGHTS="$W/pretrained/v1"
echo "[g3-build] check (h100/fast):"
bash run.sh check --config h100 --mode fast 2>&1 | tail -20
echo "GENIE3_BUILD_DONE rc=$? $(date -u +%FT%TZ)"
echo "weights tree:"; find "$W" -maxdepth 3 -name "*.ckpt" -o -maxdepth 3 -name "config.yaml" 2>/dev/null | head