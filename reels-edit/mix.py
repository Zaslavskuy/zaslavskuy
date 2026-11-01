"""Sound pass: voice + SFX cues (CC0 library from Barty-Bart/motion-graphics sound-effects skill) + ducked music bed.
usage: python3 mix.py <source.mp4> <sfxDir> <music.mp3> <out.wav>
Writes cues_report.json next to out.wav (cue -> file, beat error).
"""
import sys, json, os, subprocess
import numpy as np, librosa

SRC, SFX, MUSIC, OUT = sys.argv[1:5]
SR = 48000


def load(path, mono=False):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1' if mono else '2', '-ar', str(SR),
                          '-f', 'f32le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32)
    return a if mono else a.reshape(-1, 2)


def db(x): return 10 ** (x / 20)


voice = load(SRC)
N = len(voice)
dur = N / SR

# ---------- cues: (time, file, gain_dB, align) align: 'peak' = loudest point lands on t, 'onset' = starts at t
CUES = [
    (2.98, 'transition/fs-702773-swipe-wav.ogg', -9, 'peak', 'strike-through РЕЗУЛЬТАТОВ'),
    (3.50, 'kit/whoosh.ogg', -6, 'peak', 'iris -> dashboard'),
    (3.84, 'kit/pop.ogg', -11, 'onset', 'glow card'),
    (4.44, 'transition/fs-786514-swoosh-v2.ogg', -13, 'peak', 'camera move'),
    (4.62, 'typing/fs-511418-data-reveal-sound.ogg', -15, 'onset', 'green chart draws'),
    (5.86, 'pop/fs-824189-pop-in-sfx.ogg', -11, 'onset', 'panel lights up'),
    (6.45, 'whoosh/fs-683101-quick-woosh.ogg', -13, 'peak', 'camera pan'),
    (6.54, 'pop/kenney-interface-drop-001.ogg', -11, 'onset', 'kpi glow 1'),
    (6.82, 'pop/kenney-interface-drop-002.ogg', -11, 'onset', 'kpi glow 2'),
    (7.42, 'whoosh/fs-264777-swoosh.ogg', -6, 'peak', 'zoom-blur back to face'),
    (9.86, 'kit/impact.ogg', -11, 'onset', 'ВСЁ (red)'),
    (11.45, 'whoosh/fs-169867-swoosh.ogg', -6, 'peak', 'cut to diagram'),
    (11.48, 'pop/fs-447910-plop.ogg', -10, 'onset', 'envelope'),
    (12.08, 'kit/click.ogg', -12, 'onset', 'label МАРКЕТИНГ'),
    (12.95, 'transition/fs-683096-woosh.ogg', -13, 'peak', 'camera move'),
    (13.28, 'pop/kenney-interface-pluck-001.ogg', -10, 'onset', 'cart'),
    (14.20, 'transition/fs-816262-broomstick-whoosh-3-quiet-okm1.ogg', -11, 'peak', 'camera move'),
    (14.56, 'pop/fs527522.ogg', -10, 'onset', 'magnet'),
    (15.38, 'whoosh/fs830856.ogg', -7, 'peak', 'zoom-blur to face'),
    (16.00, 'kit/whoosh.ogg', -7, 'peak', 'iris -> browser'),
    (16.16, 'typing/fs-447909-keyboard-typing.ogg', -15, 'onset', 'typing СОЗДАТЬ САЙТ', 0.72),
    (17.02, 'typing/fs-323432-typing.ogg', -15, 'onset', 'typing НА КОТОРЫЙ МОЖНО', 0.45),
    (17.56, 'impact/fs-177242-cinematic-impact.ogg', -10, 'onset', 'ЭФФЕКТИВНО'),
    (18.36, 'pop/kenney-interface-maximize-001.ogg', -12, 'onset', 'ВЕСТИ ЛЮДЕЙ'),
    (18.80, 'pop/kenney-interface-maximize-002.ogg', -12, 'onset', 'ПО РЕКЛАМЕ'),
    (19.36, 'pop/fs-824189-pop-in-sfx.ogg', -10, 'onset', 'Instagram icon'),
    (20.02, 'pop/fs202230.ogg', -10, 'onset', 'Google icon'),
    (20.30, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
    (24.96, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
    (28.80, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -11, 'onset', 'В ИНСТРУМЕНТ (red)'),
    (32.12, 'ding/fs-571513-soft-notifications-bell-ding-d.ogg', -13, 'onset', 'ЗАЯВКИ'),
    (33.62, 'kit/pop.ogg', -11, 'onset', 'avatar'),
    (33.84, 'glitch/kenney-interface-glitch-002.ogg', -15, 'onset', 'не онлайн'),
    (34.68, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
    (35.40, 'transition/fs-850347-swipe-various.ogg', -11, 'peak', 'profile card slides in'),
    (36.64, 'click/fs788933.ogg', -8, 'onset', 'cursor click'),
    (36.80, 'ding/kenney-interface-confirmation-001.ogg', -13, 'onset', 'request sent'),
]

CUTS = [3.42, 7.40, 11.40, 15.36, 15.90, 20.28, 36.06]
if os.environ.get('LANG_CUT') == 'en':
    CUES = [
        (3.00, 'transition/fs-702773-swipe-wav.ogg', -9, 'peak', 'strike-through RESULTS'),
        (3.46, 'kit/whoosh.ogg', -6, 'peak', 'iris -> dashboard'),
        (3.80, 'kit/pop.ogg', -11, 'onset', 'glow card'),
        (4.30, 'transition/fs-786514-swoosh-v2.ogg', -13, 'peak', 'camera move'),
        (4.50, 'typing/fs-511418-data-reveal-sound.ogg', -15, 'onset', 'green chart draws'),
        (4.86, 'pop/fs-824189-pop-in-sfx.ogg', -11, 'onset', 'panel lights up'),
        (5.62, 'whoosh/fs-683101-quick-woosh.ogg', -13, 'peak', 'camera pan'),
        (5.72, 'pop/kenney-interface-drop-001.ogg', -11, 'onset', 'kpi glow 1'),
        (5.92, 'pop/kenney-interface-drop-002.ogg', -11, 'onset', 'kpi glow 2'),
        (6.26, 'whoosh/fs-264777-swoosh.ogg', -6, 'peak', 'zoom-blur back to face'),
        (8.52, 'kit/impact.ogg', -11, 'onset', 'EVERYTHING (accent)'),
        (9.95, 'whoosh/fs-169867-swoosh.ogg', -6, 'peak', 'cut to diagram'),
        (9.98, 'pop/fs-447910-plop.ogg', -10, 'onset', 'envelope'),
        (10.46, 'kit/click.ogg', -12, 'onset', 'label MARKETING'),
        (11.31, 'transition/fs-683096-woosh.ogg', -13, 'peak', 'camera move'),
        (11.64, 'pop/kenney-interface-pluck-001.ogg', -10, 'onset', 'cart'),
        (12.67, 'transition/fs-816262-broomstick-whoosh-3-quiet-okm1.ogg', -11, 'peak', 'camera move'),
        (13.10, 'pop/fs527522.ogg', -10, 'onset', 'magnet'),
        (14.06, 'whoosh/fs830856.ogg', -7, 'peak', 'zoom-blur to face'),
        (14.66, 'kit/whoosh.ogg', -7, 'peak', 'iris -> browser'),
        (14.80, 'typing/fs-447909-keyboard-typing.ogg', -15, 'onset', 'typing CREATE A WEBSITE', 0.58),
        (15.46, 'typing/fs-323432-typing.ogg', -15, 'onset', 'typing TO WHICH WE CAN', 0.45),
        (16.12, 'impact/fs-177242-cinematic-impact.ogg', -10, 'onset', 'EFFECTIVELY'),
        (16.52, 'pop/kenney-interface-maximize-001.ogg', -12, 'onset', 'DRIVE TRAFFIC'),
        (17.26, 'pop/kenney-interface-maximize-002.ogg', -12, 'onset', 'VIA ADS'),
        (17.48, 'pop/fs-824189-pop-in-sfx.ogg', -10, 'onset', 'Instagram icon'),
        (18.22, 'pop/fs202230.ogg', -10, 'onset', 'Google icon'),
        (18.92, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
        (24.02, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
        (28.26, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -11, 'onset', 'IN A TOOL (accent)'),
        (30.78, 'ding/fs-571513-soft-notifications-bell-ding-d.ogg', -13, 'onset', 'LEADS'),
        (32.12, 'kit/pop.ogg', -11, 'onset', 'avatar'),
        (32.24, 'glitch/kenney-interface-glitch-002.ogg', -15, 'onset', 'not online'),
        (33.10, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
    ]
    CUTS = [3.40, 6.24, 9.90, 14.04, 14.56, 18.90]
sfx_bus = np.zeros((N, 2), np.float32)
report = []
for c in CUES:
    t, f, g, align, desc = c[:5]
    s = load(os.path.join(SFX, f))
    if len(c) > 5:                       # trim to length with a short fade
        L = int(c[5] * SR); s = s[:L].copy(); fl = min(len(s), int(.06 * SR)); s[-fl:] *= np.linspace(1, 0, fl)[:, None]
    off = int(np.argmax(np.abs(s).sum(1))) if align == 'peak' else 0
    start = int(t * SR) - off
    a, b = max(0, start), min(N, start + len(s))
    if b > a:
        sfx_bus[a:b] += s[a - start:b - start] * db(g)
    report.append({'t': t, 'file': f, 'gain_db': g, 'align': align, 'desc': desc})

# ---------- voice: high-pass + gentle compression via ffmpeg
vtmp = OUT + '.voice.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-ac', '2', '-ar', str(SR), '-af',
                'highpass=f=75,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=4dB,'
                'loudnorm=I=-16:TP=-3:LRA=7', vtmp], check=True)
voice = load(vtmp)[:N]
voice = np.pad(voice, ((0, N - len(voice)), (0, 0)))

# ---------- music: pick start offset so the big cuts land on beats
my, msr = librosa.load(MUSIC, sr=22050)
_, beats = librosa.beat.beat_track(y=my, sr=msr)
bt = librosa.frames_to_time(beats, sr=msr)
best = None
for off in np.arange(15.0, len(my) / msr - dur - 1, 0.01):    # skip the quiet intro
    rel = bt - off
    err = [np.min(np.abs(rel - c)) for c in CUTS]
    score = np.mean(err)
    if best is None or score < best[0]:
        best = (score, off, err)
_, moff, errs = best
music = load(MUSIC)
music = music[int(moff * SR):int(moff * SR) + N]
music = np.pad(music, ((0, N - len(music)), (0, 0)))
# music level ~ -12 dB under the voice, ducked further under speech
env = np.abs(voice).mean(1)
k = int(0.15 * SR)
env = np.convolve(env, np.ones(k) / k, mode='same')
speech = np.clip((20 * np.log10(env + 1e-6) + 45) / 15, 0, 1)        # 0 = silence, 1 = speaking
sm = int(0.12 * SR)
speech = np.convolve(speech, np.ones(sm) / sm, mode='same')
v_rms = np.sqrt(np.mean(voice ** 2)); m_rms = np.sqrt(np.mean(music ** 2))
music = music * (v_rms / m_rms) * db(-13) * (1 - 0.45 * speech)[:, None]
fade = int(1.2 * SR); music[-fade:] *= np.linspace(1, 0, fade)[:, None]
music[:int(.05 * SR)] *= np.linspace(0, 1, int(.05 * SR))[:, None]

mix = voice + sfx_bus * (v_rms / 0.1) * 0.9 + music
mix.astype(np.float32).tofile(OUT + '.raw')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', OUT + '.raw', OUT], check=True)
os.remove(OUT + '.raw'); os.remove(vtmp)
json.dump({'music_offset_s': round(float(moff), 2),
           'cut_to_beat_error_ms': {str(c): round(e * 1000) for c, e in zip(CUTS, errs)},
           'cues': report}, open(os.path.splitext(OUT)[0] + '_report.json', 'w'), ensure_ascii=False, indent=1)
print('music offset', round(float(moff), 2), 'beat errors ms', [round(e * 1000) for e in errs])
