"""Word start times from whisper.cpp with DTW.

usage: python3 tools/words.py IN.wav OUT.json [--lang ru] [--model PATH]

Runs whisper-cli with -dtw -nfa -ml 1 -sow -ojf and keeps, per word, the DTW time of
its first token. -nfa is required: with flash attention on (the default), DTW
silently returns t_dtw = -1 for every token. With -ml 1 a word's end equals the next word's start, so only
start times are meaningful; "end" is stored for reference only.
"""
import argparse
import os
import re
import subprocess

from audiolib import load_json, save_json

ap = argparse.ArgumentParser()
ap.add_argument("wav")
ap.add_argument("out")
ap.add_argument("--lang", default="ru")
ap.add_argument("--model", default=".tmp/models/ggml-large-v3-turbo.bin")
ap.add_argument("--threads", default=str(os.cpu_count() or 4))
a = ap.parse_args()

base = os.path.splitext(a.out)[0] + ".raw"
subprocess.run(
    ["whisper-cli", "-m", a.model, "-f", a.wav, "-l", a.lang, "-t", a.threads,
     "-dtw", "large.v3.turbo", "-nfa", "-ml", "1", "-sow", "-ojf", "-of", base],
    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
raw = load_json(base + ".json")

words = []
for seg in raw["transcription"]:
    text = seg["text"].strip()
    if not text:
        continue
    toks = [t for t in seg.get("tokens", []) if not t["text"].startswith("[_")]
    dtw = [t["t_dtw"] for t in toks if t.get("t_dtw", -1) >= 0]
    start = dtw[0] / 100 if dtw else seg["offsets"]["from"] / 1000
    words.append({
        "w": text,
        "key": re.sub(r"^\W+|\W+$", "", text).lower(),
        "t": round(start, 3),
        "end": round(seg["offsets"]["to"] / 1000, 3),
        "dtw": bool(dtw),
    })

save_json(a.out, {"words": words})
missing = sum(not w["dtw"] for w in words)
print(f"{len(words)} words, {missing} without DTW time")
