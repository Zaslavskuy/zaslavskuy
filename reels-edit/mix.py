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
CUES = [   # RU cut (v3 graphics)
    (2.98, 'transition/fs-702773-swipe-wav.ogg', -9, 'peak', 'strike-through РЕЗУЛЬТАТОВ'),
    (3.46, 'kit/whoosh.ogg', -6, 'peak', 'card expands -> results'),
    (3.84, 'typing/fs-511418-data-reveal-sound.ogg', -14, 'onset', 'revenue counter runs'),
    (4.74, 'kit/pop.ogg', -11, 'onset', '+38% badge'),
    (5.50, 'transition/fs-786514-swoosh-v2.ogg', -13, 'peak', 'card moves up'),
    (5.86, 'pop/kenney-interface-drop-001.ogg', -12, 'onset', 'client row 1'),
    (6.00, 'pop/kenney-interface-drop-002.ogg', -12, 'onset', 'client row 2'),
    (6.14, 'pop/kenney-interface-drop-003.ogg', -12, 'onset', 'client row 3'),
    (6.54, 'tick/fs528561.ogg', -13, 'onset', 'LIVE'),
    (6.82, 'ding/kenney-interface-glass-001.ogg', -12, 'onset', 'payment toast'),
    (7.42, 'whoosh/fs-264777-swoosh.ogg', -6, 'peak', 'zoom-blur back to face'),
    (9.86, 'kit/impact.ogg', -11, 'onset', 'ВСЁ (accent)'),
    (11.45, 'whoosh/fs-169867-swoosh.ogg', -6, 'peak', 'cut to chain'),
    (11.48, 'pop/fs-447910-plop.ogg', -10, 'onset', 'marketing badge'),
    (12.20, 'kit/click.ogg', -13, 'onset', 'check 1'),
    (12.70, 'pop/kenney-interface-pluck-001.ogg', -10, 'onset', 'product badge'),
    (13.40, 'click/kenney-interface-select-001.ogg', -13, 'onset', 'check 2'),
    (13.96, 'pop/fs527522.ogg', -10, 'onset', 'traffic badge'),
    (14.68, 'click/kenney-interface-select-002.ogg', -13, 'onset', 'check 3'),
    (14.95, 'impact/kenney-impact-impactsoft-heavy-001.ogg', -11, 'onset', '= РЕЗУЛЬТАТ'),
    (15.38, 'whoosh/fs830856.ogg', -7, 'peak', 'zoom-blur to face'),
    (16.04, 'kit/whoosh.ogg', -7, 'peak', 'slide-up -> phone'),
    (16.16, 'ui-blip/kenney-ui-rollover1.ogg', -15, 'onset', 'block 1'),
    (16.30, 'ui-blip/kenney-ui-rollover2.ogg', -15, 'onset', 'block 2'),
    (16.44, 'ui-blip/kenney-ui-rollover3.ogg', -15, 'onset', 'block 3'),
    (16.60, 'ui-blip/kenney-ui-rollover4.ogg', -15, 'onset', 'button block'),
    (16.80, 'pop/kenney-interface-pluck-002.ogg', -15, 'onset', 'cards row'),
    (17.56, 'impact/fs-177242-cinematic-impact.ogg', -10, 'onset', 'ЭФФЕКТИВНО + phone glow'),
    (18.40, 'whoosh/fs393811.ogg', -14, 'peak', 'visitors start flowing'),
    (19.36, 'pop/fs-824189-pop-in-sfx.ogg', -10, 'onset', 'Instagram Ads chip'),
    (20.02, 'pop/fs202230.ogg', -10, 'onset', 'Google Ads chip'),
    (20.30, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
    (24.96, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
    (28.80, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -11, 'onset', 'В ИНСТРУМЕНТ (accent)'),
    (32.12, 'ding/kenney-interface-glass-001.ogg', -12, 'onset', 'night lead 1'),
    (32.80, 'ding/kenney-interface-glass-002.ogg', -12, 'onset', 'night lead 2'),
    (33.58, 'ding/fs-634690-lil-pip.ogg', -12, 'onset', 'night lead 3'),
    (34.68, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
    (35.40, 'transition/fs-850347-swipe-various.ogg', -11, 'peak', 'request form slides in'),
    (35.62, 'typing/fs-323432-typing.ogg', -16, 'onset', 'typing name', 0.34),
    (35.98, 'typing/fs-447909-keyboard-typing.ogg', -16, 'onset', 'typing phone', 0.38),
    (36.64, 'click/fs788933.ogg', -8, 'onset', 'tap Оставить заявку'),
    (36.80, 'ding/kenney-interface-confirmation-001.ogg', -13, 'onset', 'request sent'),
]

CUTS = [3.42, 7.40, 11.40, 15.36, 15.90, 20.28, 35.36]
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
if os.environ.get('LANG_CUT') == 'uk':   # Ukrainian cut (v3 graphics)
    CUES = [
        (3.00, 'transition/fs-702773-swipe-wav.ogg', -9, 'peak', 'strike-through РЕЗУЛЬТАТІВ'),
        (3.46, 'kit/whoosh.ogg', -6, 'peak', 'card expands -> results'),
        (3.90, 'typing/fs-511418-data-reveal-sound.ogg', -14, 'onset', 'revenue counter runs'),
        (4.92, 'kit/pop.ogg', -11, 'onset', '+38% badge'),
        (5.56, 'transition/fs-786514-swoosh-v2.ogg', -13, 'peak', 'card moves up'),
        (5.90, 'pop/kenney-interface-drop-001.ogg', -12, 'onset', 'client row 1'),
        (6.04, 'pop/kenney-interface-drop-002.ogg', -12, 'onset', 'client row 2'),
        (6.18, 'pop/kenney-interface-drop-003.ogg', -12, 'onset', 'client row 3'),
        (6.58, 'tick/fs528561.ogg', -13, 'onset', 'LIVE'),
        (6.76, 'ding/kenney-interface-glass-001.ogg', -12, 'onset', 'payment toast'),
        (7.38, 'whoosh/fs-264777-swoosh.ogg', -6, 'peak', 'zoom-blur back to face'),
        (10.46, 'kit/impact.ogg', -11, 'onset', 'ВСЕ (accent)'),
        (11.61, 'whoosh/fs-169867-swoosh.ogg', -6, 'peak', 'cut to chain'),
        (11.64, 'pop/fs-447910-plop.ogg', -10, 'onset', 'marketing badge'),
        (12.38, 'kit/click.ogg', -13, 'onset', 'check 1'),
        (12.94, 'pop/kenney-interface-pluck-001.ogg', -10, 'onset', 'offer badge'),
        (13.48, 'click/kenney-interface-select-001.ogg', -13, 'onset', 'check 2'),
        (14.14, 'pop/fs527522.ogg', -10, 'onset', 'traffic badge'),
        (14.74, 'click/kenney-interface-select-002.ogg', -13, 'onset', 'check 3'),
        (15.01, 'impact/kenney-impact-impactsoft-heavy-001.ogg', -11, 'onset', '= РЕЗУЛЬТАТ'),
        (15.42, 'whoosh/fs830856.ogg', -7, 'peak', 'zoom-blur to face'),
        (16.08, 'kit/whoosh.ogg', -7, 'peak', 'slide-up -> phone'),
        (16.20, 'ui-blip/kenney-ui-rollover1.ogg', -15, 'onset', 'block 1'),
        (16.34, 'ui-blip/kenney-ui-rollover2.ogg', -15, 'onset', 'block 2'),
        (16.48, 'ui-blip/kenney-ui-rollover3.ogg', -15, 'onset', 'block 3'),
        (16.64, 'ui-blip/kenney-ui-rollover4.ogg', -15, 'onset', 'button block'),
        (16.84, 'pop/kenney-interface-pluck-002.ogg', -15, 'onset', 'cards row'),
        (17.14, 'impact/fs-177242-cinematic-impact.ogg', -10, 'onset', 'ЕФЕКТИВНО + phone glow'),
        (17.80, 'whoosh/fs393811.ogg', -14, 'peak', 'visitors start flowing'),
        (19.16, 'pop/fs-824189-pop-in-sfx.ogg', -10, 'onset', 'Facebook chip'),
        (19.70, 'pop/fs202230.ogg', -10, 'onset', 'Instagram chip'),
        (20.44, 'pop/fs-824189-pop-in-sfx.ogg', -10, 'onset', 'Google chip'),
        (20.86, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
        (28.30, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
        (31.66, 'transition/fs-702773-swipe-wav.ogg', -10, 'peak', 'strike-through ВИТРАТИ'),
        (33.10, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -11, 'onset', 'В ІНСТРУМЕНТ (accent)'),
        (34.60, 'transition/fs-850347-swipe-various.ogg', -12, 'peak', 'conversion card in'),
        (35.22, 'typing/fs-511418-data-reveal-sound.ogg', -15, 'onset', 'visitors counter'),
        (36.06, 'ding/kenney-interface-confirmation-002.ogg', -12, 'onset', 'clients counter'),
        (36.76, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
        (37.46, 'transition/fs-850347-swipe-various.ogg', -11, 'peak', 'request form slides in'),
        (38.10, 'typing/fs-323432-typing.ogg', -16, 'onset', 'typing name', 0.70),
        (38.90, 'typing/fs-447909-keyboard-typing.ogg', -16, 'onset', 'typing phone', 0.42),
        (40.26, 'click/fs788933.ogg', -8, 'onset', 'tap Залишити заявку'),
        (40.42, 'ding/kenney-interface-confirmation-001.ogg', -13, 'onset', 'request sent'),
    ]
    CUTS = [3.40, 7.36, 11.56, 15.40, 15.98, 20.84, 37.42]
if os.environ.get('LANG_CUT') == 'p2':   # portfolio reel
    CUES = [
        (4.06, 'kit/whoosh.ogg', -6, 'peak', 'card expands -> site showcase'),
        (4.38, 'transition/fs-786514-swoosh-v2.ogg', -11, 'peak', 'site 1 flies in'),
        (4.55, 'pop/kenney-interface-drop-001.ogg', -13, 'onset', 'tag 01'),
        (6.48, 'transition/fs-683096-woosh.ogg', -11, 'peak', 'site 2 flies in'),
        (6.65, 'pop/kenney-interface-drop-002.ogg', -13, 'onset', 'tag 02'),
        (7.00, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -12, 'onset', 'ИНСТРУМЕНТ (accent)'),
        (8.68, 'transition/fs-816262-broomstick-whoosh-3-quiet-okm1.ogg', -10, 'peak', 'site 3 flies in'),
        (8.85, 'pop/kenney-interface-drop-003.ogg', -13, 'onset', 'tag 03'),
        (10.88, 'transition/fs-850347-swipe-various.ogg', -11, 'peak', 'site 4 flies in'),
        (11.05, 'pop/kenney-interface-pluck-001.ogg', -13, 'onset', 'tag 04'),
        (13.42, 'ding/kenney-interface-glass-001.ogg', -12, 'onset', 'new request toast'),
        (14.66, 'whoosh/fs830856.ogg', -6, 'peak', 'zoom-blur to face'),
        (15.62, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
        (16.06, 'impact/kenney-impact-impactsoft-heavy-001.ogg', -12, 'onset', 'ГОТОВЫЙ САЙТ (accent)'),
        (17.10, 'kit/whoosh.ogg', -7, 'peak', 'slide-up -> features'),
        (17.10, 'click/kenney-interface-select-001.ogg', -12, 'onset', 'tick: adaptive'),
        (17.85, 'transition/fs-702773-swipe-wav.ogg', -12, 'peak', 'desktop morphs into phone'),
        (18.58, 'click/kenney-interface-select-002.ogg', -12, 'onset', 'tick: SEO'),
        (18.66, 'typing/fs-323432-typing.ogg', -16, 'onset', 'search query typing', 0.40),
        (19.14, 'pop/fs-824189-pop-in-sfx.ogg', -11, 'onset', 'site climbs to #1'),
        (19.88, 'click/kenney-interface-select-003.ogg', -12, 'onset', 'tick: structure'),
        (19.98, 'pop/fs-447910-plop.ogg', -12, 'onset', 'root node'),
        (20.26, 'ui-blip/kenney-ui-rollover1.ogg', -15, 'onset', 'node 1'),
        (20.34, 'ui-blip/kenney-ui-rollover2.ogg', -15, 'onset', 'node 2'),
        (20.42, 'ui-blip/kenney-ui-rollover3.ogg', -15, 'onset', 'node 3'),
        (20.50, 'ui-blip/kenney-ui-rollover4.ogg', -15, 'onset', 'node 4'),
        (21.22, 'kit/click.ogg', -12, 'onset', 'tick: forms'),
        (21.30, 'typing/fs-447909-keyboard-typing.ogg', -16, 'onset', 'form typing', 0.55),
        (21.96, 'click/fs788933.ogg', -8, 'onset', 'tap send'),
        (22.14, 'ding/kenney-interface-confirmation-001.ogg', -13, 'onset', 'request sent'),
        (22.76, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
        (24.12, 'transition/fs-850347-swipe-various.ogg', -12, 'peak', 'ads card in'),
        (24.94, 'pop/kenney-interface-pluck-001.ogg', -12, 'onset', 'Google Ads ready'),
        (25.34, 'pop/kenney-interface-pluck-002.ogg', -12, 'onset', 'Instagram Ads ready'),
        (27.16, 'transition/fs-786514-swoosh-v2.ogg', -12, 'peak', 'campaign card in'),
        (27.52, 'click/kenney-interface-toggle-001.ogg', -9, 'onset', 'campaign toggle on'),
        (29.10, 'typing/fs-511418-data-reveal-sound.ogg', -15, 'onset', 'leads counter'),
        (30.00, 'ding/kenney-interface-glass-002.ogg', -13, 'onset', '+38 leads'),
        (30.62, 'whoosh/fs393811.ogg', -17, 'peak', 'cut + punch-in'),
        (32.42, 'transition/fs-850347-swipe-various.ogg', -11, 'peak', 'request form slides in'),
        (32.62, 'typing/fs-323432-typing.ogg', -16, 'onset', 'typing name', 0.34),
        (32.98, 'typing/fs-447909-keyboard-typing.ogg', -16, 'onset', 'typing phone', 0.34),
        (33.56, 'click/fs788933.ogg', -8, 'onset', 'tap Оставить заявку'),
        (33.72, 'ding/kenney-interface-confirmation-001.ogg', -13, 'onset', 'request sent'),
    ]
    CUTS = [4.00, 6.20, 8.40, 10.60, 14.64, 17.00, 22.74, 32.38]
if os.environ.get('LANG_CUT') == 'p2uk':   # portfolio reel, Ukrainian cut
    CUES = [
        (4.06, 'kit/whoosh.ogg', -6, 'peak', 'card expands -> site showcase'),
        (4.38, 'transition/fs-786514-swoosh-v2.ogg', -11, 'peak', 'site 1 flies in'),
        (4.55, 'pop/kenney-interface-drop-001.ogg', -13, 'onset', 'tag 01'),
        (6.53, 'transition/fs-683096-woosh.ogg', -11, 'peak', 'site 2 flies in'),
        (6.70, 'pop/kenney-interface-drop-002.ogg', -13, 'onset', 'tag 02'),
        (7.38, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -12, 'onset', 'ІНСТРУМЕНТ (accent)'),
        (8.78, 'transition/fs-816262-broomstick-whoosh-3-quiet-okm1.ogg', -10, 'peak', 'site 3 flies in'),
        (8.95, 'pop/kenney-interface-drop-003.ogg', -13, 'onset', 'tag 03'),
        (11.03, 'transition/fs-850347-swipe-various.ogg', -11, 'peak', 'site 4 flies in'),
        (11.20, 'pop/kenney-interface-pluck-001.ogg', -13, 'onset', 'tag 04'),
        (13.64, 'ding/kenney-interface-glass-001.ogg', -12, 'onset', 'new request toast'),
        (14.58, 'whoosh/fs830856.ogg', -6, 'peak', 'zoom-blur to face'),
        (15.82, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
        (16.40, 'impact/kenney-impact-impactsoft-heavy-001.ogg', -12, 'onset', 'ГОТОВИЙ САЙТ (accent)'),
        (17.20, 'kit/whoosh.ogg', -7, 'peak', 'slide-up -> features'),
        (17.26, 'click/kenney-interface-select-001.ogg', -12, 'onset', 'tick: adaptive'),
        (17.97, 'transition/fs-702773-swipe-wav.ogg', -12, 'peak', 'desktop morphs into phone'),
        (18.68, 'click/kenney-interface-select-002.ogg', -12, 'onset', 'tick: SEO'),
        (18.76, 'typing/fs-323432-typing.ogg', -16, 'onset', 'search query typing', 0.40),
        (19.26, 'pop/fs-824189-pop-in-sfx.ogg', -11, 'onset', 'site climbs to #1'),
        (20.02, 'click/kenney-interface-select-003.ogg', -12, 'onset', 'tick: structure'),
        (20.12, 'pop/fs-447910-plop.ogg', -12, 'onset', 'root node'),
        (20.40, 'ui-blip/kenney-ui-rollover1.ogg', -15, 'onset', 'node 1'),
        (20.48, 'ui-blip/kenney-ui-rollover2.ogg', -15, 'onset', 'node 2'),
        (20.57, 'ui-blip/kenney-ui-rollover3.ogg', -15, 'onset', 'node 3'),
        (20.65, 'ui-blip/kenney-ui-rollover4.ogg', -15, 'onset', 'node 4'),
        (21.40, 'kit/click.ogg', -12, 'onset', 'tick: forms'),
        (21.48, 'typing/fs-447909-keyboard-typing.ogg', -16, 'onset', 'form typing', 0.55),
        (22.17, 'click/fs788933.ogg', -8, 'onset', 'tap send'),
        (22.26, 'ding/kenney-interface-confirmation-001.ogg', -13, 'onset', 'request sent'),
        (22.86, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
        (24.30, 'transition/fs-850347-swipe-various.ogg', -12, 'peak', 'ads card in'),
        (25.14, 'pop/kenney-interface-pluck-001.ogg', -12, 'onset', 'Google Ads ready'),
        (25.58, 'pop/kenney-interface-pluck-002.ogg', -12, 'onset', 'Instagram Ads ready'),
        (27.38, 'transition/fs-786514-swoosh-v2.ogg', -12, 'peak', 'campaign card in'),
        (27.94, 'click/kenney-interface-toggle-001.ogg', -9, 'onset', 'campaign toggle on'),
        (29.66, 'typing/fs-511418-data-reveal-sound.ogg', -15, 'onset', 'leads counter'),
        (30.60, 'ding/kenney-interface-glass-002.ogg', -13, 'onset', '+38 leads'),
        (31.26, 'whoosh/fs393811.ogg', -17, 'peak', 'cut + punch-in'),
        (33.12, 'transition/fs-850347-swipe-various.ogg', -11, 'peak', 'request form slides in'),
        (33.31, 'typing/fs-323432-typing.ogg', -16, 'onset', 'typing name', 0.34),
        (33.66, 'typing/fs-447909-keyboard-typing.ogg', -16, 'onset', 'typing phone', 0.34),
        (34.20, 'click/fs788933.ogg', -8, 'onset', 'tap Залишити заявку'),
        (34.36, 'ding/kenney-interface-confirmation-001.ogg', -13, 'onset', 'request sent'),
    ]
    CUTS = [4.00, 6.25, 8.50, 10.75, 14.56, 17.10, 22.84, 33.08]
if os.environ.get('LANG_CUT') == 'p3':   # "ads that don't bring clients" reel
    CUES = [
        (2.48, 'kit/impact.ogg', -11, 'onset', 'ХРЕНОВО (accent) + punch-in'),
        (4.28, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
        (6.84, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -12, 'onset', 'НЕ РАБОТАЕТ (accent)'),
        (7.36, 'kit/whoosh.ogg', -6, 'peak', 'card expands -> problems'),
        (7.62, 'glitch/kenney-interface-glitch-002.ogg', -14, 'onset', 'warning chip'),
        (9.00, 'transition/fs-786514-swoosh-v2.ogg', -13, 'peak', 'card: creatives'),
        (9.30, 'tick/fs528561.ogg', -12, 'onset', 'x mark 1'),
        (9.66, 'transition/fs-683096-woosh.ogg', -13, 'peak', 'card: offer'),
        (9.96, 'tick/fs384187.ogg', -12, 'onset', 'x mark 2'),
        (10.90, 'transition/fs-816262-broomstick-whoosh-3-quiet-okm1.ogg', -12, 'peak', 'card: settings'),
        (11.20, 'tick/fs721514.ogg', -12, 'onset', 'x mark 3'),
        (12.08, 'transition/fs-850347-swipe-various.ogg', -13, 'peak', 'card: landing page'),
        (12.38, 'tick/fs528561.ogg', -12, 'onset', 'x mark 4'),
        (14.12, 'whoosh/fs830856.ogg', -6, 'peak', 'zoom-blur to face'),
        (15.76, 'kit/whoosh.ogg', -7, 'peak', 'card expands -> ad cabinet'),
        (15.80, 'typing/fs-511418-data-reveal-sound.ogg', -15, 'onset', 'spend counter'),
        (16.56, 'glitch/kenney-interface-glitch-002.ogg', -12, 'onset', '$1 200 per lead'),
        (17.06, 'transition/fs-786514-swoosh-v2.ogg', -13, 'peak', 'motivation card in'),
        (17.40, 'riser/fs-174363-rewind.ogg', -16, 'onset', 'battery drains', 1.3),
        (18.52, 'impact/kenney-impact-impactsoft-heavy-001.ogg', -11, 'onset', 'ПРОПАДАЕТ (accent) + shake'),
        (20.22, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
        (22.26, 'kit/whoosh.ogg', -7, 'peak', 'slide-up -> results'),
        (23.30, 'pop/fs-447910-plop.ogg', -11, 'onset', 'Dubai real estate card'),
        (23.45, 'typing/fs-511418-data-reveal-sound.ogg', -16, 'onset', 'counters 1'),
        (25.10, 'pop/kenney-interface-pluck-001.ogg', -11, 'onset', 'Italy wholesale card'),
        (25.25, 'typing/fs-511418-data-reveal-sound.ogg', -16, 'onset', 'counters 2'),
        (27.30, 'pop/fs527522.ogg', -11, 'onset', 'services card'),
        (27.45, 'typing/fs-511418-data-reveal-sound.ogg', -16, 'onset', 'counters 3'),
        (29.00, 'transition/fs-856168-cyberpunk-glitch-hologram-tran.ogg', -12, 'onset', 'grey niche: spotlight + glitch'),
        (30.10, 'pop/fs-258269-mouth-pop.ogg', -12, 'onset', '🤫'),
        (30.32, 'impact/fs-222517-dramatic-hit.ogg', -12, 'onset', 'СЕКРЕТНО stamp'),
        (31.22, 'whoosh/fs830856.ogg', -6, 'peak', 'zoom-blur to face'),
        (33.14, 'whoosh/fs393811.ogg', -17, 'peak', 'cut'),
        (35.06, 'kit/whoosh.ogg', -7, 'peak', 'card expands -> chain'),
        (35.52, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -12, 'onset', 'ВСЮ СВЯЗКУ'),
        (36.58, 'pop/kenney-interface-drop-001.ogg', -11, 'onset', 'node: offer'),
        (37.34, 'pop/kenney-interface-drop-002.ogg', -11, 'onset', 'node: creatives'),
        (38.04, 'pop/kenney-interface-drop-003.ogg', -11, 'onset', 'node: website'),
        (38.54, 'pop/kenney-interface-pluck-002.ogg', -11, 'onset', 'node: instagram'),
        (39.34, 'riser/fs-685256-riser-sound-effect-short-wav.ogg', -16, 'onset', 'client travels the path', 0.85),
        (40.22, 'ding/kenney-interface-confirmation-001.ogg', -11, 'onset', 'ЗАЯВКА ✓'),
        (40.62, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
        (43.38, 'transition/fs-850347-swipe-various.ogg', -11, 'peak', 'request form slides in'),
        (43.50, 'typing/fs-323432-typing.ogg', -16, 'onset', 'typing', 0.50),
        (44.04, 'click/fs788933.ogg', -8, 'onset', 'tap Оставить заявку'),
        (44.20, 'ding/kenney-interface-confirmation-002.ogg', -13, 'onset', 'request sent'),
    ]
    CUTS = [7.30, 14.10, 15.70, 20.20, 22.20, 31.20, 35.00, 40.60]
if os.environ.get('LANG_CUT') == 'p3uk':   # "ads that don't bring clients" reel, Ukrainian cut
    CUES = [
        (2.30, 'kit/impact.ogg', -11, 'onset', 'ХРІНОВО (accent) + punch-in'),
        (4.26, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
        (6.46, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -12, 'onset', 'НЕ ПРАЦЮЄ (accent)'),
        (7.36, 'kit/whoosh.ogg', -6, 'peak', 'card expands -> problems'),
        (7.42, 'glitch/kenney-interface-glitch-002.ogg', -14, 'onset', 'warning chip'),
        (8.64, 'transition/fs-786514-swoosh-v2.ogg', -13, 'peak', 'card: creatives'),
        (8.92, 'tick/fs528561.ogg', -12, 'onset', 'x mark 1'),
        (9.34, 'transition/fs-683096-woosh.ogg', -13, 'peak', 'card: offer'),
        (9.62, 'tick/fs384187.ogg', -12, 'onset', 'x mark 2'),
        (10.60, 'transition/fs-816262-broomstick-whoosh-3-quiet-okm1.ogg', -12, 'peak', 'card: settings'),
        (10.88, 'tick/fs721514.ogg', -12, 'onset', 'x mark 3'),
        (11.70, 'transition/fs-850347-swipe-various.ogg', -13, 'peak', 'card: landing page'),
        (11.98, 'tick/fs528561.ogg', -12, 'onset', 'x mark 4'),
        (13.82, 'whoosh/fs830856.ogg', -6, 'peak', 'zoom-blur to face'),
        (15.56, 'kit/whoosh.ogg', -7, 'peak', 'card expands -> ad cabinet'),
        (15.60, 'typing/fs-511418-data-reveal-sound.ogg', -15, 'onset', 'spend counter'),
        (16.48, 'glitch/kenney-interface-glitch-002.ogg', -12, 'onset', '$1 200 per lead'),
        (16.92, 'transition/fs-786514-swoosh-v2.ogg', -13, 'peak', 'motivation card in'),
        (17.29, 'riser/fs-174363-rewind.ogg', -16, 'onset', 'battery drains', 1.3),
        (18.54, 'impact/kenney-impact-impactsoft-heavy-001.ogg', -11, 'onset', 'ПРОПАДАЄ (accent) + shake'),
        (19.54, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
        (23.16, 'kit/whoosh.ogg', -7, 'peak', 'slide-up -> results'),
        (24.04, 'pop/fs-447910-plop.ogg', -11, 'onset', 'Dubai real estate card'),
        (24.19, 'typing/fs-511418-data-reveal-sound.ogg', -16, 'onset', 'counters 1'),
        (25.68, 'pop/kenney-interface-pluck-001.ogg', -11, 'onset', 'Italy wholesale card'),
        (25.83, 'typing/fs-511418-data-reveal-sound.ogg', -16, 'onset', 'counters 2'),
        (27.64, 'pop/fs527522.ogg', -11, 'onset', 'services card'),
        (27.79, 'typing/fs-511418-data-reveal-sound.ogg', -16, 'onset', 'counters 3'),
        (29.32, 'transition/fs-856168-cyberpunk-glitch-hologram-tran.ogg', -12, 'onset', 'grey niche: spotlight + glitch'),
        (30.42, 'pop/fs-258269-mouth-pop.ogg', -12, 'onset', '🤫'),
        (30.72, 'impact/fs-222517-dramatic-hit.ogg', -12, 'onset', 'СЕКРЕТНО stamp'),
        (31.42, 'whoosh/fs830856.ogg', -6, 'peak', 'zoom-blur to face'),
        (33.58, 'whoosh/fs393811.ogg', -17, 'peak', 'cut'),
        (35.46, 'kit/whoosh.ogg', -7, 'peak', 'card expands -> chain'),
        (36.16, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -12, 'onset', "ВСЮ ЗВ'ЯЗКУ"),
        (36.92, 'pop/kenney-interface-drop-001.ogg', -11, 'onset', 'node: offer'),
        (37.94, 'pop/kenney-interface-drop-002.ogg', -11, 'onset', 'node: creatives'),
        (38.62, 'pop/kenney-interface-drop-003.ogg', -11, 'onset', 'node: website'),
        (39.18, 'pop/kenney-interface-pluck-002.ogg', -11, 'onset', 'node: instagram'),
        (40.04, 'riser/fs-685256-riser-sound-effect-short-wav.ogg', -16, 'onset', 'client travels the path', 0.85),
        (40.94, 'ding/kenney-interface-confirmation-001.ogg', -11, 'onset', 'ЗАЯВКА ✓'),
        (41.42, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
        (44.34, 'transition/fs-850347-swipe-various.ogg', -11, 'peak', 'request form slides in'),
        (44.45, 'typing/fs-323432-typing.ogg', -16, 'onset', 'typing', 0.50),
        (44.96, 'click/fs788933.ogg', -8, 'onset', 'tap Залишити заявку'),
        (45.12, 'ding/kenney-interface-confirmation-002.ogg', -13, 'onset', 'request sent'),
    ]
    CUTS = [7.30, 13.80, 15.50, 19.52, 23.10, 31.40, 35.40, 41.40]
if os.environ.get('LANG_CUT') in ('p4', 'p4uk'):   # four-niches reel
    CUES = [
        (0.90, 'ui-blip/kenney-ui-rollover1.ogg', -16, 'onset', 'sky chip: Dubai'),
        (2.06, 'ui-blip/kenney-ui-rollover2.ogg', -16, 'onset', 'sky chip: Italy'),
        (3.94, 'glitch/kenney-sci-computernoise-000.ogg', -20, 'onset', 'sky chip: ??? niche', 0.6),
        (6.10, 'pop/fs-824189-pop-in-sfx.ogg', -15, 'onset', 'question mark'),
        (6.82, 'whoosh/fs393811.ogg', -16, 'peak', 'cut'),
        (8.26, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
        (12.28, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -12, 'onset', 'РАЗНОЙ (accent)'),
        (12.76, 'kit/whoosh.ogg', -6, 'peak', 'card expands -> case 01'),
        (12.95, 'pop/fs-447910-plop.ogg', -12, 'onset', 'Dubai creative'),
        (13.66, 'typing/fs-511418-data-reveal-sound.ogg', -16, 'onset', 'KPI count 01'),
        (14.86, 'pop/kenney-interface-drop-001.ogg', -13, 'onset', 'qualified lead 1'),
        (15.04, 'pop/kenney-interface-drop-002.ogg', -13, 'onset', 'qualified lead 2'),
        (15.22, 'pop/kenney-interface-drop-003.ogg', -13, 'onset', 'qualified lead 3'),
        (16.70, 'transition/fs-702773-swipe-wav.ogg', -12, 'peak', 'vanity numbers struck out'),
        (17.58, 'transition/fs-786514-swoosh-v2.ogg', -10, 'peak', 'case 02 slides in'),
        (17.70, 'pop/kenney-interface-pluck-001.ogg', -13, 'onset', 'Italy creatives fan'),
        (18.78, 'typing/fs-511418-data-reveal-sound.ogg', -16, 'onset', 'KPI count 02'),
        (20.10, 'ding/kenney-interface-glass-001.ogg', -13, 'onset', 'wholesale buyers ✓'),
        (21.46, 'glitch/kenney-interface-glitch-002.ogg', -14, 'onset', 'random buyers ✕'),
        (22.58, 'transition/fs-683096-woosh.ogg', -10, 'peak', 'case 03 slides in'),
        (22.70, 'pop/kenney-interface-pluck-002.ogg', -13, 'onset', 'cleaning creatives fan'),
        (23.14, 'typing/fs-511418-data-reveal-sound.ogg', -16, 'onset', 'KPI count 03'),
        (24.34, 'pop/kenney-interface-drop-001.ogg', -13, 'onset', 'interest'),
        (24.90, 'whoosh/fs-683101-quick-woosh.ogg', -13, 'peak', 'fast arrow'),
        (25.98, 'ding/kenney-interface-confirmation-001.ogg', -12, 'onset', 'request ✓'),
        (26.46, 'transition/fs-856168-cyberpunk-glitch-hologram-tran.ogg', -11, 'onset', 'case 04: secret niche'),
        (27.84, 'pop/fs-258269-mouth-pop.ogg', -12, 'onset', '🤫'),
        (29.48, 'glitch/kenney-interface-glitch-002.ogg', -13, 'onset', 'name redacted'),
        (29.56, 'impact/fs-222517-dramatic-hit.ogg', -12, 'onset', 'БЕЗ НАЗВАНИЯ stamp'),
        (30.56, 'typing/fs-511418-data-reveal-sound.ogg', -15, 'onset', 'KPI count 04'),
        (31.94, 'whoosh/fs830856.ogg', -6, 'peak', 'zoom-blur to face'),
        (33.50, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
        (34.98, 'transition/fs-702773-swipe-wav.ogg', -12, 'peak', 'ШАБЛОНУ struck out'),
        (35.16, 'kit/whoosh.ogg', -7, 'peak', 'slide-up -> system'),
        (35.66, 'impact/kenney-impact-impactsoft-heavy-001.ogg', -14, 'onset', 'block: analysis'),
        (37.24, 'impact/kenney-impact-impactsoft-heavy-000.ogg', -15, 'onset', 'block: offer'),
        (37.94, 'pop/kenney-interface-drop-002.ogg', -12, 'onset', 'block: creatives'),
        (39.30, 'pop/kenney-interface-drop-003.ogg', -12, 'onset', 'block: website'),
        (39.82, 'pop/kenney-interface-pluck-002.ogg', -12, 'onset', 'block: instagram'),
        (40.52, 'riser/fs-685256-riser-sound-effect-short-wav.ogg', -16, 'onset', 'client path runs down', 1.15),
        (41.70, 'ding/kenney-interface-confirmation-002.ogg', -11, 'onset', '✓ Заявка'),
        (42.58, 'whoosh/fs810485.ogg', -6, 'peak', 'zoom-blur to face'),
        (44.02, 'whoosh/fs393811.ogg', -17, 'peak', 'punch-in'),
        (46.04, 'transition/fs-850347-swipe-various.ogg', -11, 'peak', 'request form slides in'),
        (46.18, 'typing/fs-323432-typing.ogg', -16, 'onset', 'typing', 0.46),
        (46.74, 'click/fs788933.ogg', -8, 'onset', 'tap Оставить заявку'),
        (46.90, 'ding/kenney-interface-confirmation-001.ogg', -13, 'onset', 'request sent'),
    ]
    CUTS = [6.80, 12.70, 17.56, 22.56, 26.44, 31.92, 35.10, 42.56]
    if os.environ.get('LANG_CUT') == 'p4uk':   # same cues, moved onto the Ukrainian speech timing
        _A = [(0, 0), (0.90, 0.90), (2.06, 2.06), (3.94, 3.92), (6.10, 5.88), (6.82, 6.70), (8.26, 8.20), (12.28, 12.28),
              (12.70, 12.70), (13.66, 13.62), (14.86, 14.88), (16.32, 16.18), (16.70, 16.56), (17.56, 17.24), (18.78, 18.32),
              (20.10, 19.74), (21.46, 21.66), (21.94, 22.18), (22.56, 22.76), (23.14, 23.32), (24.34, 24.62), (24.74, 25.06),
              (25.98, 26.30), (26.44, 26.70), (27.84, 28.08), (29.48, 29.44), (29.56, 29.58), (30.56, 30.58), (31.92, 32.04),
              (33.50, 33.46), (34.98, 34.50), (35.10, 34.70), (35.66, 35.20), (37.24, 36.96), (37.94, 37.68), (39.30, 39.10),
              (39.82, 39.56), (40.52, 40.42), (41.70, 41.60), (42.56, 42.40), (44.02, 43.76), (46.00, 45.86), (46.74, 46.50), (50.04, 49.96)]
        _f = lambda t: float(np.interp(t, [a for a, b in _A], [b for a, b in _A]))
        CUES = [(round(_f(c[0]), 2),) + tuple(c[1:]) for c in CUES]
        CUTS = [6.68, 12.70, 17.24, 22.76, 26.70, 32.04, 34.70, 42.40]
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
MUSIC_DB = float(os.environ.get('MUSIC_DB', -13))   # music bed vs voice
SFX_DB = float(os.environ.get('SFX_DB', 0))        # extra SFX boost
music = music * (v_rms / m_rms) * db(MUSIC_DB) * (1 - 0.45 * speech)[:, None]
fade = int(1.2 * SR); music[-fade:] *= np.linspace(1, 0, fade)[:, None]
music[:int(.05 * SR)] *= np.linspace(0, 1, int(.05 * SR))[:, None]

mix = voice + sfx_bus * (v_rms / 0.1) * 0.9 * db(SFX_DB) + music
mix.astype(np.float32).tofile(OUT + '.raw')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', OUT + '.raw', OUT], check=True)
os.remove(OUT + '.raw'); os.remove(vtmp)
json.dump({'music_offset_s': round(float(moff), 2),
           'cut_to_beat_error_ms': {str(c): round(e * 1000) for c, e in zip(CUTS, errs)},
           'cues': report}, open(os.path.splitext(OUT)[0] + '_report.json', 'w'), ensure_ascii=False, indent=1)
print('music offset', round(float(moff), 2), 'beat errors ms', [round(e * 1000) for e in errs])
