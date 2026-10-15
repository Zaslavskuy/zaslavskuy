"""Turn edl_spans.json into frame-accurate cut pieces.

usage: python3 tools/plan_cut.py edl_spans.json OUT.json [--density максимальная] [--gain DB]

For each span: tighten to speech (first speech - 20 ms, last speech + 30 ms),
compress inner pauses, then snap to the frame grid. Starts snap down, ends snap
up, so snapping can only add a few ms of air and never clips speech; pieces that
touch after snapping are merged. A span may carry "hold_out" (seconds): its last
piece then runs that much past the last speech, capped at the source's end, for
a clean silent tail on the final frame.
"""
import argparse
import json
import math
import subprocess

from audiolib import compress, envelope, load_json, read_wav, save_json, span_bounds, speech_mask

ap = argparse.ArgumentParser()
ap.add_argument("edl")
ap.add_argument("out")
ap.add_argument("--wav", default=".tmp/audio16k.wav")
ap.add_argument("--density", default="максимальная")
ap.add_argument("--gain", type=float, default=None, help="analysis gain, dB (default: from env.json)")
a = ap.parse_args()

edl = load_json(a.edl)
gain = a.gain if a.gain is not None else load_json(".tmp/env.json")["gain_db"]
probe = json.loads(subprocess.run(
    ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate,nb_frames",
     "-of", "json", edl["source"]], capture_output=True, text=True, check=True).stdout)
num, den = map(int, probe["streams"][0]["r_frame_rate"].split("/"))
fps = num / den
src_frames = int(probe["streams"][0]["nb_frames"])

x, sr = read_wav(a.wav)
speech, _ = speech_mask(envelope(x, sr, gain))

pieces, report = [], []
for sp in edl["spans"]:
    b = span_bounds(speech, sp["in"], sp["out"])
    if b is None:
        raise SystemExit(f"{sp['id']}: no speech inside {sp['in']}-{sp['out']}")
    parts = compress(speech, b[0], b[1], a.density)
    hold = sp.get("hold_out", 0.0)
    if hold:  # appended after compression, or the tail itself gets squeezed as a pause
        parts[-1] = (parts[-1][0], min(parts[-1][1] + hold, src_frames / fps))
        b = (b[0], parts[-1][1])
    snapped = []
    for p0, p1 in parts:
        f0, f1 = math.floor(p0 * fps), min(math.ceil(p1 * fps), src_frames)
        if snapped and f0 <= snapped[-1][1]:
            snapped[-1][1] = max(snapped[-1][1], f1)
        else:
            snapped.append([f0, f1])
    for f0, f1 in snapped:
        pieces.append({"span": sp["id"], "f_in": f0, "f_out": f1, "in": f0 / fps, "out": f1 / fps})
    report.append((sp["id"], b, len(snapped)))

total_frames = sum(p["f_out"] - p["f_in"] for p in pieces)
save_json(a.out, {"source": edl["source"], "fps": fps, "density": a.density,
                  "total_frames": total_frames, "duration": total_frames / fps, "pieces": pieces})

src = sum(sp["out"] - sp["in"] for sp in edl["spans"])
for sid, (t0, t1), n in report:
    print(f"{sid}: speech {t0:6.2f}-{t1:6.2f}  -> {n} piece(s)")
print(f"{len(pieces)} pieces, {total_frames} frames @ {fps:g} fps = {total_frames / fps:.2f}s "
      f"(spans {src:.2f}s)")
