#!/bin/bash
# Wave-4 end-to-end driver (ambition-lift, 2026-10-27): deepen the PROVEN crown recipe.
# Genie3 conserved-sub-site (frag 14,15,21,22 = UniProt 202,203,209,210; conserved human/mouse -> x-react)
# -> funnel (MPNN -> ESMFold self-consistency+novelty -> human pocket-restrained Boltz screen)
# -> FROZEN crown screen (crown_screen_2stage: dual-folder Boltz+Chai ipSAE_min; crown <=> bind>=0.30 & XR>=0.15).
# 3200 backbones (33% deeper than the v15 wave of 2400), FRESH seeds 31000-31007 (distinct from all priors:
# 9100-01, 9200-03, 21000-07). The extended-footprint arm was DROPPED by devil's advocate: frag 16,20,23,24
# (=UniProt 204,208,211,212) are the 4 human<->mouse DIVERGENT residues -> conditioning on them is XR-negative.
# Sequential stages: each releases the GPUs before the next (crown screen has its own foreign-GPU guard).
# v16 stays the floor; winners are gated on the frozen judge + portal novelty before any v17.
set -uo pipefail
cd /home/prachh/v/anthropic-adaptyv-2026-tfr1
TAG=genie3_apical4; WL=w4; OUT=runs/f35; GPUS="0 1 2 3 4 5 6 7"
LOG=$OUT/drive.log; mkdir -p "$OUT"
say(){ echo "[wave4 $(date -u +%FT%TZ)] $*" | tee -a "$LOG"; }

say "STAGE 0: Genie3 generation 3200 backbones seeds 31000-31007 -> runs/$TAG"
bash scripts/gen_genie3_tfr1.sh "$GPUS" 3200 31000 "$TAG" >> "$LOG" 2>&1
NB=$(find runs/$TAG/shard_g*/ -name "*.pdb" 2>/dev/null | wc -l)
say "generation done: $NB backbones"
[ "$NB" -ge 100 ] || { say "ABORT: too few backbones ($NB)"; echo "WAVE4_DRIVE_FAIL gen"; exit 1; }
sleep 20

say "STAGE 1-4: funnel (MPNN -> ESMFold SC+novelty -> human Boltz screen) -> $OUT/binders.csv"
bash scripts/funnel_wave_run.sh "$TAG" "$WL" "$OUT" "$GPUS" 500 >> "$LOG" 2>&1
[ -s "$OUT/binders.csv" ] || { say "ABORT: no binders.csv"; echo "WAVE4_DRIVE_FAIL funnel"; exit 1; }
NBIND=$(($(wc -l < "$OUT/binders.csv") - 1))
say "funnel done: $NBIND human-binder candidates"
sleep 20

say "STAGE 5: FROZEN crown screen (2-stage Boltz+Chai dual-folder) -> $OUT/crown"
bash scripts/crown_screen_2stage.sh "$OUT/binders.csv" "$OUT/crown" >> "$LOG" 2>&1
say "crown screen done"
echo "WAVE4_DRIVE_DONE $(date -u +%FT%TZ)  (-> $OUT/crown ; next: switch-install on crowns + v17 build)"
