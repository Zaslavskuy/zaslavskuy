import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[3] if len(sys.argv)>3 else "medium", device="cpu", compute_type="int8")
import subprocess, numpy as np
raw = subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
audio = np.frombuffer(raw, np.int16).astype(np.float32)/32768
segs, info = m.transcribe(audio, word_timestamps=True, beam_size=5, language=(sys.argv[4] if len(sys.argv)>4 else None))
out = {"lang": info.language, "segments": []}
for s in segs:
    out["segments"].append({"start": s.start, "end": s.end, "text": s.text,
        "words": [{"w": w.word, "s": w.start, "e": w.end} for w in s.words]})
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}", flush=True)
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
