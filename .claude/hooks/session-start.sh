#!/bin/bash
# Installs the media toolchain (ffmpeg, whisper.cpp + base model, HyperFrames + Chrome)
# at the start of a cloud session. Each step is skipped when already present.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

log() { echo "[session-start] $*" >&2; }

# Node 22+ is preinstalled in the cloud image; only report if it is not.
node_major=$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)
if [ "$node_major" -lt 22 ]; then
  log "Node 22+ required, found major version $node_major"
fi

# ffmpeg
if ! command -v ffmpeg >/dev/null; then
  log "installing ffmpeg"
  apt-get update -qq >/dev/null
  apt-get install -y -qq ffmpeg >/dev/null
fi

# whisper.cpp binary
if ! command -v whisper-cli >/dev/null; then
  log "building whisper.cpp"
  src=/opt/src/whisper.cpp
  [ -d "$src" ] || git clone --depth 1 https://github.com/ggml-org/whisper.cpp.git "$src"
  cmake -S "$src" -B "$src/build" -DCMAKE_BUILD_TYPE=Release -DWHISPER_BUILD_TESTS=OFF >/dev/null
  cmake --build "$src/build" -j"$(nproc)" --config Release >/dev/null
  cmake --install "$src/build" --prefix /usr/local >/dev/null
  ldconfig
fi

# whisper base model
model=/usr/local/share/whisper/ggml-base.bin
if [ ! -s "$model" ]; then
  log "downloading whisper base model"
  mkdir -p "$(dirname "$model")"
  curl -sSL --fail -o "$model.part" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin
  mv "$model.part" "$model"
fi

# HyperFrames CLI + headless Chrome for rendering
if ! command -v hyperframes >/dev/null; then
  log "installing hyperframes CLI"
  npm install -g hyperframes >/dev/null
fi
hyperframes browser ensure >/dev/null 2>&1 || log "hyperframes browser ensure failed"

log "done"
