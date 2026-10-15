"""Verify a cut: residual silence (number) and per-span fragment transcription.

usage: python3 tools/check_cut.py CUT.wav [--plan .tmp/cut_plan.json] [--asr]

Residual silence = longest run without speech on the cut's own speech mask.
--asr transcribes every span separately (with 0.5 s of lead-in silence), since
a whole-file pass collapses repeated takes into one line and cannot see them.
"""
import argparse
import os
import subprocess

import numpy as np

from audiolib import HOP, envelope, load_json, read_wav, runs, speech_mask

ap = argparse.ArgumentParser()
ap.add_argument("wav")
ap.add_argument("--plan", default=".tmp/cut_plan.json")
ap.add_argument("--gain", type=float, default=None)
ap.add_argument("--asr", action="store_true")
ap.add_argument("--model", default=".tmp/models/ggml-large-v3-turbo.bin")
ap.add_argument("--lang", default="ru")
a = ap.parse_args()

gain = a.gain if a.gain is not None else load_json(".tmp/env.json")["gain_db"]
x, sr = read_wav(a.wav)
speech, _ = speech_mask(envelope(x, sr, gain))
gaps = [((s * HOP), (e - s) * HOP) for s, e in runs(~speech)]
inner = [g for g in gaps if g[0] > 0 and g[0] + g[1] < len(speech) * HOP - HOP]
longest = max(inner, key=lambda g: g[1]) if inner else (0, 0)
print(f"cut duration {len(x)/sr:.3f}s, speech {speech.mean()*100:.1f}% of hops")
print(f"residual silence: longest inner gap {longest[1]*1000:.0f} ms at {longest[0]:.2f}s; "
      f"gaps >= 100 ms: {sum(g[1] >= 0.1 for g in inner)}, >= 150 ms: {sum(g[1] >= 0.15 for g in inner)}")
for t, d in inner:
    if d >= 0.1:
        print(f"  {t:6.2f}s  {d*1000:.0f} ms")

if a.asr:
    plan = load_json(a.plan)
    fps = plan["fps"]
    os.makedirs(".tmp/frag", exist_ok=True)
    pos, spans = 0, {}
    for p in plan["pieces"]:
        d = (p["f_out"] - p["f_in"]) / fps
        s = spans.setdefault(p["span"], [pos, pos])
        s[1] = pos + d
        pos += d
    for sid, (t0, t1) in spans.items():
        f = f".tmp/frag/cut_{sid}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", a.wav,
                        "-af", "adelay=500,apad=pad_dur=0.5", f], check=True)
        out = subprocess.run(["whisper-cli", "-m", a.model, "-f", f, "-l", a.lang, "-nt", "-t", str(os.cpu_count())],
                             capture_output=True, text=True).stdout
        print(f"{sid} {t0:6.2f}-{t1:6.2f}: {' '.join(out.split())}")
