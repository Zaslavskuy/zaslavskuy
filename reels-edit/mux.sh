#!/usr/bin/env bash
# usage: mux.sh <video_noaudio.mp4> <mix.wav> <final.mp4>
# Two-pass loudnorm to -14 LUFS / -2 dBTP (reference video measures -14.3 LUFS).
set -euo pipefail
V=$1; A=$2; OUT=$3
J=$(ffmpeg -nostats -i "$A" -af loudnorm=I=-14:TP=-2:LRA=9:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
MI=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -v error -y -i "$V" -i "$A" -af "loudnorm=I=-14:TP=-2:LRA=9:$MI:linear=true,aresample=48000" \
  -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$OUT"
echo "stereo:"; ffmpeg -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
echo "mono:";   ffmpeg -nostats -i "$OUT" -ac 1 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
