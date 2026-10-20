#!/bin/bash
# adaptyv-tfr1 harness bootstrap + verification (uv-only).
#   ./init.sh          core env + smoke tests (fast, CPU-only) -- the verification gate
#   ./init.sh --tools  print shared design-tool locations (no heavy re-install)
set -euo pipefail
unset VIRTUAL_ENV 2>/dev/null || true
cd "$(dirname "$0")"

echo "=== adaptyv-tfr1 :: core environment (uv sync) ==="
uv sync

echo "=== compile check ==="
uv run python -m compileall -q src scripts || true

echo "=== tests (pytest) ==="
uv run pytest -q

echo "=== submission validator self-check ==="
if [ -f submissions/example_track2.csv ] && [ -f scripts/validate_submission.py ]; then
  uv run python scripts/validate_submission.py submissions/example_track2.csv --track 2
else
  echo "(validator / example CSV land in feature F03 — skipped)"
fi

if [[ "${1:-}" == "--tools" ]]; then
  echo ""
  echo "=== shared design-tool locations (reused across sibling repos; NOT re-installed) ==="
  echo "RFdiffusion3     : /home/prachh/work/cache/rfdiffusion3_opt"
  echo "RFdiffusion1     : /home/prachh/work/cache/rfdiffusion1_opt* (run scratch in work/tmp)"
  echo "Genie3           : /home/prachh/work/cache/genie3_opt"
  echo "BoltzGen         : /home/prachh/work/cache/huggingface/models--boltzgen--boltzgen-1"
  echo "                   (+ ../anthropic-adaptyv-2026-glp1r/third_party/boltzgen)"
  echo "Boltz-2          : ~/.boltz , ~/.cache/mosaic/boltz  (venv: ../sepiq-2026-challenge/.venv-boltz)"
  echo "Chai-1           : /home/prachh/work/cache/chai1_opt  (venv: ../sepiq-2026-challenge/.venv-chai)"
  echo "PXDesign/Protenix: /home/prachh/v/protenix_cache     (venv: ../sepiq-2026-challenge/.venv-protenix)"
  echo "ProteinMPNN      : /home/prachh/v/mva-track2-orthogonal-20261006-v29/ProteinMPNN"
  echo "AF2 initial-guess/BindCraft : /home/prachh/work/cache/bindcraft/alphafold"
  echo "MD / pKa         : conda envs ambertools, pmxfep, evobind ; justHisPKa (local tgz+lic)"
  echo "Reference pipeline: ../anthropic-adaptyv-2026-tnf (scripts/README.md is the manifest)"
  echo "Exact per-tool invocation: docs/TOOLS.md (lands in F01/F04)."
fi

echo ""
echo "=== Verification complete — environment is clean and restartable ==="
echo "Next: read AGENTS.md + docs/PLAN.md; check feature_list.json (active) + progress.md."
