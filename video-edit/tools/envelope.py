"""Build the loudness envelope + speech mask and list pauses.

usage: python3 tools/envelope.py IN.wav OUT.json [--gain DB] [--min-pause 0.3]

--gain lifts the envelope before thresholding, so a quiet recording is judged
at the level it will be mastered to (gain = -14 - measured integrated LUFS).
"""
import argparse

import numpy as np

from audiolib import HOP, envelope, read_wav, runs, save_json, speech_mask, speech_runs_sec

ap = argparse.ArgumentParser()
ap.add_argument("wav")
ap.add_argument("out")
ap.add_argument("--min-pause", type=float, default=0.3)
ap.add_argument("--gain", type=float, default=0.0)
a = ap.parse_args()

x, sr = read_wav(a.wav)
env = envelope(x, sr, a.gain)
speech, sdb = speech_mask(env)

quiet = env[~speech]
floor = float(np.percentile(quiet, 10)) if len(quiet) else float("nan")
save_json(a.out, {
    "hop": HOP,
    "gain_db": a.gain,
    "duration": len(x) / sr,
    "noise_floor_db": floor,
    "env_db": [round(float(v), 1) for v in env],
    "speech": [[round(s, 2), round(e, 2)] for s, e in speech_runs_sec(speech)],
})

print(f"duration {len(x)/sr:.2f}s  noise floor (p10 of non-speech) {floor:.1f} dBFS")
print(f"pauses >= {a.min_pause}s:")
for s, e in runs(~speech):
    if (e - s) * HOP >= a.min_pause:
        print(f"  {s*HOP:7.2f} - {e*HOP:7.2f}  ({(e-s)*HOP:.2f}s)")
