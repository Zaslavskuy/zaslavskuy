#!/bin/bash
# Full rebuild after editing edl_spans.json or cues.json.
#   tools/build.sh            cut + graphics timings + audio (no render)
#   tools/build.sh preview    … + render out/preview.mp4
#   tools/build.sh master     … + render out/master.mp4 (--quality high)
# Run from video-edit/. Needs .tmp/raw.mp4 and .tmp/audio16k.wav from step 1.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 tools/plan_cut.py edl_spans.json .tmp/cut_plan.json
python3 tools/cut.py .tmp/cut_plan.json .tmp/cut.mov
ffmpeg -v error -y -i .tmp/cut.mov -vn -ac 1 -ar 16000 -c:a pcm_s16le .tmp/cut16k.wav
python3 tools/check_cut.py .tmp/cut16k.wav

# stage the cut for HyperFrames with a keyframe every second (sparse GOPs freeze on seek)
ffmpeg -v error -y -i .tmp/cut.mov -c:v libx264 -crf 16 -preset slow -g 25 -keyint_min 25 \
  -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart project/input-video.mp4

# word timings come from the CUT track, never the source
python3 tools/words.py .tmp/cut16k.wav transcripts/final_words.json
python3 tools/gen_cues.py
python3 tools/master_audio.py .tmp/cut.mov .tmp/audio_mixed.wav

mode="${1:-}"
[ -z "$mode" ] && exit 0
out="out/$mode.mp4"
quality=$([ "$mode" = master ] && echo high || echo looks)
(cd project && npx hyperframes check && npx hyperframes render -o "../.tmp/render_$mode.mp4" --quality "$quality")
# audio goes into the finished render without re-encoding the picture
ffmpeg -v error -y -i ".tmp/render_$mode.mp4" -i .tmp/audio_mixed.wav -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart "$out"
ffmpeg -hide_banner -i "$out" -af loudnorm=I=-14:TP=-1:print_format=json -f null - 2>&1 | grep -E '"input_(i|tp)"'
echo "$out"
