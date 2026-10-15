"""Master the voice: high-pass 80 Hz → static gain → true-peak limiter → two-pass loudnorm.

usage: python3 tools/master_audio.py IN(.mov/.wav) OUT.wav [--target -14] [--tp -1.5]

The gain lifts the voice to the target first, so the limiter (run at 4× sample
rate, so it catches inter-sample peaks) does the peak work and loudnorm's second
pass only trims a fraction of a dB in linear mode. Without the limiter a +20 dB
lift to −14 LUFS clips. No denoise: measure the floor first; below −50 dBFS it
only adds artifacts.
"""
import argparse
import json
import re
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("inp")
ap.add_argument("out")
ap.add_argument("--target", type=float, default=-14.0)
ap.add_argument("--tp", type=float, default=-1.5)  # AAC encoding adds inter-sample peaks: −1.0 in WAV measured −0.96 after AAC
a = ap.parse_args()


def measure(af):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", a.inp, "-vn", "-af",
                        f"{af},loudnorm=I={a.target}:TP={a.tp}:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr).group(0))


hp = "highpass=f=80"
m0 = measure(hp)
gain = a.target - float(m0["input_i"])
limit = 10 ** ((a.tp - 1.0) / 20)  # ceiling 1 dB under the target leaves room for the linear trim
pre = (f"{hp},volume={gain:.2f}dB,aresample=192000,"
       f"alimiter=limit={limit:.4f}:attack=2:release=60:level=false,aresample=48000")
m1 = measure(pre)
final = (f"{pre},loudnorm=I={a.target}:TP={a.tp}:LRA=11:linear=true:"
         f"measured_I={m1['input_i']}:measured_TP={m1['input_tp']}:measured_LRA={m1['input_lra']}:"
         f"measured_thresh={m1['input_thresh']}:offset={m1['target_offset']}:print_format=json")
r = subprocess.run(["ffmpeg", "-v", "info", "-hide_banner", "-y", "-i", a.inp, "-vn", "-af", final,
                    "-ar", "48000", "-c:a", "pcm_s24le", a.out], capture_output=True, text=True, check=True)
m2 = json.loads(re.search(r"\{[^{}]*\"normalization_type\"[^{}]*\}", r.stderr).group(0))
print(f"source {m0['input_i']} LUFS / TP {m0['input_tp']} → gain {gain:+.2f} dB → limited {m1['input_i']} LUFS / "
      f"TP {m1['input_tp']} → loudnorm {m2['normalization_type']}: {m2['output_i']} LUFS / TP {m2['output_tp']}")
