"""Render the cut in one ffmpeg pass from a cut plan.

usage: python3 tools/cut.py .tmp/cut_plan.json .tmp/cut.mov [--crf 16]

Per piece trim/atrim + setpts/asetpts, then the concat *filter*: frame-exact
cuts (not keyframe-snapped) and video/audio cut in one graph, so they cannot
drift apart. Each piece gets a 15 ms audio fade at both ends to avoid clicks.
"""
import argparse
import subprocess

from audiolib import load_json

FADE = 0.015

ap = argparse.ArgumentParser()
ap.add_argument("plan")
ap.add_argument("out")
ap.add_argument("--crf", default="16")
a = ap.parse_args()

plan = load_json(a.plan)
fps = plan["fps"]
parts, labels = [], []
for i, p in enumerate(plan["pieces"]):
    t0, t1 = p["f_in"] / fps, p["f_out"] / fps
    d = t1 - t0
    parts.append(f"[0:v]trim=start_frame={p['f_in']}:end_frame={p['f_out']},setpts=PTS-STARTPTS[v{i}]")
    parts.append(
        f"[0:a]atrim=start={t0:.6f}:end={t1:.6f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:d={FADE},afade=t=out:st={d - FADE:.6f}:d={FADE}[a{i}]"
    )
    labels.append(f"[v{i}][a{i}]")
graph = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=1:a=1[v][a]"

subprocess.run([
    "ffmpeg", "-v", "error", "-y", "-i", plan["source"], "-filter_complex", graph,
    "-map", "[v]", "-map", "[a]", "-r", f"{fps:g}",
    "-c:v", "libx264", "-crf", a.crf, "-preset", "slow", "-pix_fmt", "yuv420p",
    "-c:a", "pcm_s24le", "-ar", "48000", a.out,
], check=True)
print(f"{a.out}: {len(labels)} pieces, expected {plan['total_frames']} frames = {plan['duration']:.3f}s")
