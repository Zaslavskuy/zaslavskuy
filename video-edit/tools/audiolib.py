"""Shared audio analysis: RMS envelope, speech mask, span boundaries, pause compression.

All times are seconds. Envelope hop is 10 ms. Input audio is 16 kHz mono PCM WAV.
"""
import json
import wave

import numpy as np

HOP = 0.010            # envelope window, s
LOUD_DB = -30.0        # speech threshold on smoothed envelope, dBFS
SMOOTH = 3             # sliding max radius in hops (±30 ms)
MIN_RUN = 0.110        # loud run must hold this long to count as speech
TAIL = 0.250           # voiceless-ending pickup window
PAD_IN = 0.020         # span in  = first speech - 20 ms
PAD_OUT = 0.030        # span out = last speech + 30 ms

DENSITY = {
    # pause threshold, kept total per pause
    "максимальная": (0.160, 0.050),
    "естественная": (0.400, 0.220),
}


def read_wav(path):
    with wave.open(path, "rb") as w:
        assert w.getsampwidth() == 2, "expect 16-bit PCM"
        sr = w.getframerate()
        ch = w.getnchannels()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    return data.astype(np.float64) / 32768.0, sr


def envelope(samples, sr, gain_db=0.0):
    """RMS per 10 ms window in dBFS, after a static analysis gain."""
    n = int(round(sr * HOP))
    frames = len(samples) // n
    x = samples[: frames * n].reshape(frames, n)
    rms = np.sqrt((x ** 2).mean(axis=1))
    return 20 * np.log10(np.maximum(rms, 1e-10)) + gain_db


def sliding_max(env, r=SMOOTH):
    pad = np.pad(env, r, mode="edge")
    return np.max(np.lib.stride_tricks.sliding_window_view(pad, 2 * r + 1), axis=1)


def runs(mask):
    """[start, end) index pairs of True runs."""
    m = np.concatenate([[False], mask, [False]]).astype(np.int8)
    d = np.diff(m)
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def speech_mask(env):
    sdb = sliding_max(env)
    loud = sdb >= LOUD_DB
    speech = np.zeros_like(loud)
    min_len = int(round(MIN_RUN / HOP))
    for s, e in runs(loud):
        if e - s >= min_len:
            speech[s:e] = True
    # Voiceless-ending pickup lives in the mask so inner cuts get it too.
    # It only absorbs loud hops that failed the duration test (short blips such
    # as a final voiceless consonant) and never reaches into the next speech run:
    # otherwise any pause under 250 ms followed by speech gets bridged and the
    # 160 ms pause compression never sees it.
    tail = int(round(TAIL / HOP))
    core = speech.copy()
    blip = loud & ~core
    for s, e in runs(core):
        k = e - 1
        while True:
            win = slice(k + 1, min(k + 1 + tail, len(core)))
            nxt = np.where(core[win])[0]
            limit = nxt[0] if len(nxt) else win.stop - win.start
            ahead = np.where(blip[win][:limit])[0]
            if len(ahead) == 0:
                break
            nk = k + 1 + ahead[-1]
            speech[k + 1 : nk + 1] = True
            k = nk
    return speech, sdb


def speech_runs_sec(speech):
    return [(s * HOP, e * HOP) for s, e in runs(speech)]


def span_bounds(speech, t_in, t_out):
    """Tighten a span to its speech: first speech - 20 ms, last speech + 30 ms."""
    i0, i1 = int(t_in / HOP), int(np.ceil(t_out / HOP))
    idx = np.where(speech[i0:i1])[0]
    if len(idx) == 0:
        return None
    return (i0 + idx[0]) * HOP - PAD_IN, (i0 + idx[-1] + 1) * HOP + PAD_OUT


def compress(speech, t_in, t_out, density="максимальная"):
    """Split a span into kept pieces, shrinking each inner pause to the kept length."""
    thr, keep = DENSITY[density]
    i0, i1 = int(round(t_in / HOP)), int(round(t_out / HOP))
    pieces, cur = [], t_in
    for s, e in runs(~speech[i0:i1]):
        a, b = (i0 + s) * HOP, (i0 + e) * HOP
        if b - a < thr or a <= t_in or b >= t_out:
            continue
        pieces.append((cur, a + keep / 2))
        cur = b - keep / 2
    pieces.append((cur, t_out))
    return pieces


def snap(t, fps):
    return round(t * fps) / fps


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save_json(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
