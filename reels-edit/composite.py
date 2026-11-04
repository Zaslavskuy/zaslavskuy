"""Composite: source video -> camera moves (push-ins / punch-ins / zoom-blur whips) -> overlay frames.
usage: python3 composite.py <source.mp4> <overlayDir> <out_noaudio.mp4> [en|uk|p2|p2uk|p3|p3uk|p4|p4uk|p5|p5uk|p6|p6uk|p8|p8uk|p9|p9uk]
"""
import sys, os, subprocess
import numpy as np, cv2

SRC, OVL, OUT = sys.argv[1:4]
W, H, FPS = 1080, 1920, 25
N = int(round(float(subprocess.check_output(
    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', SRC])) * FPS))

# face anchors (normalised) per shot
A, B, C, D = (0.50, 0.45), (0.50, 0.37), (0.50, 0.40), (0.49, 0.36)
# (t0, t1, scale0, scale1, anchor): slow push-in inside a segment, hard punch between segments
CAM = [
    (0.00, 1.16, 1.16, 1.20, A), (1.16, 3.64, 1.00, 1.06, A),
    (7.40, 9.34, 1.00, 1.05, B), (9.34, 11.56, 1.18, 1.22, B),
    (15.36, 16.2, 1.00, 1.03, D),
    (20.28, 22.58, 1.14, 1.18, D), (22.58, 24.96, 1.00, 1.04, D),
    (24.96, 27.20, 1.22, 1.27, D), (27.20, 31.28, 1.00, 1.06, D),
    (31.28, 33.58, 1.15, 1.19, D), (33.58, 34.68, 1.00, 1.03, D),
    (34.68, 36.06, 1.20, 1.24, D), (36.06, 99.0, 1.00, 1.06, D),
]
WHIPS = [7.40, 15.36, 20.28]   # zoom-blur back onto the face after a b-roll
if len(sys.argv) > 4 and sys.argv[4] == 'en':      # English cut: same shots, different speech timing
    CAM = [
        (0.00, 1.34, 1.16, 1.20, A), (1.34, 3.64, 1.00, 1.06, A),
        (6.24, 8.24, 1.00, 1.05, B), (8.24, 10.04, 1.18, 1.22, B),
        (14.04, 14.7, 1.00, 1.03, D),
        (18.90, 21.28, 1.14, 1.18, D), (21.28, 24.00, 1.00, 1.04, D),
        (24.00, 26.30, 1.22, 1.27, D), (26.30, 30.32, 1.00, 1.06, D),
        (30.32, 32.12, 1.15, 1.19, D), (32.12, 33.10, 1.00, 1.03, D),
        (33.10, 35.06, 1.20, 1.24, D), (35.06, 99.0, 1.00, 1.06, D),
    ]
    WHIPS = [6.24, 14.04, 18.90]
if len(sys.argv) > 4 and sys.argv[4] == 'uk':      # Ukrainian cut (shot C = sitting by the tree is on screen here)
    C = (0.46, 0.46)
    CAM = [
        (0.00, 1.30, 1.16, 1.20, A), (1.30, 3.64, 1.00, 1.06, A),
        (7.36, 9.12, 1.00, 1.05, B), (9.12, 10.26, 1.10, 1.13, B), (10.26, 11.56, 1.18, 1.22, B),
        (15.40, 15.98, 1.00, 1.03, C),
        (20.84, 21.12, 1.14, 1.15, C), (21.12, 23.52, 1.00, 1.04, C), (23.52, 24.98, 1.14, 1.18, C),
        (24.98, 27.94, 1.00, 1.05, C), (27.94, 28.28, 1.20, 1.22, C),
        (28.28, 30.44, 1.20, 1.25, D), (30.44, 31.92, 1.00, 1.04, D), (31.92, 34.56, 1.14, 1.19, D),
        (34.56, 36.74, 1.00, 1.04, D), (36.74, 39.64, 1.18, 1.23, D), (39.64, 99.0, 1.00, 1.06, D),
    ]
    WHIPS = [7.36, 15.40, 20.84]
if len(sys.argv) > 4 and sys.argv[4] == 'p2':      # portfolio reel (B shot fully covered by the site showcase)
    C = (0.46, 0.46)
    CAM = [
        (0.00, 1.78, 1.16, 1.20, A), (1.78, 4.10, 1.00, 1.06, A),
        (14.64, 15.62, 1.00, 1.03, C), (15.62, 17.10, 1.14, 1.18, C),
        (22.74, 25.64, 1.00, 1.04, C), (25.64, 28.42, 1.12, 1.16, C), (28.42, 30.60, 1.00, 1.04, C),
        (30.60, 32.38, 1.18, 1.23, D), (32.38, 99.0, 1.00, 1.06, D),
    ]
    WHIPS = [14.64, 22.74]
if len(sys.argv) > 4 and sys.argv[4] == 'p2uk':    # portfolio reel, Ukrainian cut
    C = (0.46, 0.46)
    CAM = [
        (0.00, 1.82, 1.16, 1.20, A), (1.82, 4.10, 1.00, 1.06, A),
        (14.56, 15.82, 1.00, 1.03, C), (15.82, 17.20, 1.14, 1.18, C),
        (22.84, 25.86, 1.00, 1.04, C), (25.86, 28.86, 1.12, 1.16, C), (28.86, 31.24, 1.00, 1.04, C),
        (31.24, 33.08, 1.18, 1.23, D), (33.08, 99.0, 1.00, 1.06, D),
    ]
    WHIPS = [14.56, 22.84]
if len(sys.argv) > 4 and sys.argv[4] == 'p3':      # "ads that don't bring clients" reel
    A, B, C, D = (0.45, 0.33), (0.50, 0.30), (0.50, 0.30), (0.47, 0.28)
    CAM = [
        (0.00, 2.04, 1.06, 1.10, A), (2.04, 3.36, 1.22, 1.26, A),
        (3.36, 4.28, 1.00, 1.03, B), (4.28, 5.48, 1.12, 1.15, B), (5.48, 7.40, 1.00, 1.04, B),
        (14.10, 15.80, 1.14, 1.18, B), (20.20, 22.30, 1.00, 1.05, B),
        (31.20, 33.12, 1.12, 1.16, C),
        (33.12, 35.10, 1.00, 1.04, D), (40.60, 43.34, 1.14, 1.18, D), (43.34, 99.0, 1.00, 1.05, D),
    ]
    WHIPS = [14.10, 20.20, 31.20, 40.60]
if len(sys.argv) > 4 and sys.argv[4] == 'p3uk':    # "ads that don't bring clients" reel, Ukrainian cut
    A, B, C, D = (0.45, 0.33), (0.50, 0.30), (0.50, 0.30), (0.47, 0.28)
    CAM = [
        (0.00, 2.06, 1.06, 1.10, A), (2.06, 3.16, 1.22, 1.26, A),
        (3.16, 4.26, 1.00, 1.03, B), (4.26, 5.26, 1.12, 1.15, B), (5.26, 7.40, 1.00, 1.04, B),
        (13.80, 15.60, 1.14, 1.18, B), (19.52, 21.22, 1.00, 1.04, B), (21.22, 23.20, 1.10, 1.13, B),
        (31.40, 33.56, 1.12, 1.16, B),
        (33.56, 35.50, 1.00, 1.04, D), (41.40, 44.30, 1.14, 1.18, D), (44.30, 99.0, 1.00, 1.05, D),
    ]
    WHIPS = [13.80, 19.52, 31.40, 41.40]
if len(sys.argv) > 4 and sys.argv[4] == 'p4':      # four-niches reel
    A, B, C, D = (0.50, 0.45), (0.50, 0.33), (0.46, 0.46), (0.49, 0.36)
    CAM = [
        (0.00, 6.80, 1.00, 1.06, A),
        (6.80, 8.26, 1.00, 1.03, B), (8.26, 10.48, 1.12, 1.15, B), (10.48, 12.80, 1.00, 1.04, B),
        (31.92, 33.50, 1.00, 1.03, C), (33.50, 35.20, 1.14, 1.18, C),
        (42.56, 44.02, 1.00, 1.03, D), (44.02, 46.00, 1.16, 1.20, D), (46.00, 99.0, 1.00, 1.05, D),
    ]
    WHIPS = [31.92, 42.56]
if len(sys.argv) > 4 and sys.argv[4] == 'p4uk':    # four-niches reel, Ukrainian cut
    A, B, C, D = (0.50, 0.45), (0.50, 0.33), (0.46, 0.46), (0.49, 0.36)
    CAM = [
        (0.00, 6.68, 1.00, 1.06, A),
        (6.68, 8.20, 1.00, 1.03, B), (8.20, 10.50, 1.12, 1.15, B), (10.50, 12.80, 1.00, 1.04, B),
        (32.04, 33.46, 1.00, 1.03, C), (33.46, 34.82, 1.14, 1.18, C),
        (42.40, 43.76, 1.00, 1.03, D), (43.76, 45.86, 1.16, 1.20, D), (45.86, 99.0, 1.00, 1.05, D),
    ]
    WHIPS = [32.04, 42.40]
if len(sys.argv) > 4 and sys.argv[4] == 'p5':      # affordable-sites reel
    A, B, D = (0.45, 0.33), (0.50, 0.30), (0.47, 0.28)
    CAM = [
        (0.00, 2.46, 1.04, 1.08, A), (2.46, 4.50, 1.18, 1.22, A),
        (17.40, 19.20, 1.10, 1.14, B),
        (26.60, 27.95, 1.00, 1.04, B),
        (33.00, 34.50, 1.00, 1.03, B), (34.50, 37.04, 1.14, 1.18, B),
        (37.04, 39.26, 1.00, 1.04, D), (39.26, 99.0, 1.06, 1.10, D),
    ]
    WHIPS = [17.40, 26.60, 33.00]
if len(sys.argv) > 4 and sys.argv[4] == 'p5uk':    # affordable-sites reel, Ukrainian cut
    A, B, D = (0.45, 0.33), (0.50, 0.30), (0.47, 0.28)
    CAM = [
        (0.00, 3.22, 1.04, 1.08, A), (3.22, 5.00, 1.18, 1.22, A),
        (17.20, 19.10, 1.10, 1.14, B),
        (26.84, 28.25, 1.00, 1.04, B),
        (33.50, 35.26, 1.00, 1.03, B), (35.26, 37.68, 1.14, 1.18, B),
        (37.68, 40.10, 1.00, 1.04, D), (40.10, 99.0, 1.06, 1.10, D),
    ]
    WHIPS = [17.20, 26.84, 33.50]
if len(sys.argv) > 4 and sys.argv[4] == 'p6':      # real-estate agency system reel
    A, B, C, D = (0.50, 0.40), (0.50, 0.33), (0.50, 0.40), (0.49, 0.36)
    CAM = [
        (0.00, 5.98, 1.00, 1.05, A), (5.98, 7.93, 1.12, 1.16, A),
        (7.93, 9.95, 1.00, 1.04, B),
        (22.10, 24.00, 1.12, 1.16, B),
        (31.37, 34.48, 1.00, 1.04, C), (34.48, 39.40, 1.12, 1.16, C),
        (47.20, 49.48, 1.00, 1.03, D), (49.48, 52.84, 1.14, 1.18, D), (52.84, 54.14, 1.00, 1.03, D), (54.14, 99.0, 1.00, 1.05, D),
    ]
    WHIPS = [22.10, 31.37, 47.20]
if len(sys.argv) > 4 and sys.argv[4] == 'p6uk':    # real-estate agency system reel, Ukrainian cut
    A, B, C, D = (0.50, 0.40), (0.50, 0.33), (0.50, 0.40), (0.49, 0.36)
    CAM = [
        (0.00, 5.98, 1.00, 1.05, A), (5.98, 7.80, 1.12, 1.16, A),
        (7.80, 9.75, 1.00, 1.04, B),
        (22.20, 24.25, 1.12, 1.16, B),
        (31.97, 34.82, 1.00, 1.04, C), (34.82, 39.85, 1.12, 1.16, C),
        (47.37, 49.58, 1.00, 1.03, D), (49.58, 52.88, 1.14, 1.18, D), (52.88, 54.58, 1.00, 1.03, D), (54.58, 99.0, 1.00, 1.05, D),
    ]
    WHIPS = [22.20, 31.97, 47.37]
if len(sys.argv) > 4 and sys.argv[4] == 'p8':      # "$1M in 3 months" reel
    A, B, C, D, E = (0.50, 0.42), (0.50, 0.33), (0.46, 0.46), (0.50, 0.40), (0.49, 0.36)
    CAM = [
        (0.00, 1.46, 1.00, 1.04, A), (1.46, 4.04, 1.12, 1.16, A), (4.04, 6.40, 1.00, 1.04, A),
        (6.40, 8.34, 1.00, 1.03, B), (8.34, 11.70, 1.12, 1.16, B), (11.70, 14.10, 1.00, 1.04, B),
        (22.96, 25.10, 1.12, 1.16, C),
        (42.08, 45.76, 1.00, 1.04, D), (45.76, 49.16, 1.14, 1.18, D),
        (49.16, 55.18, 1.00, 1.04, E), (55.18, 99.0, 1.12, 1.16, E),
    ]
    WHIPS = [22.96, 42.08]
if len(sys.argv) > 4 and sys.argv[4] == 'p8uk':    # "$1M in 3 months" reel, Ukrainian cut
    A, B, C, D, E = (0.50, 0.42), (0.50, 0.33), (0.46, 0.46), (0.50, 0.40), (0.49, 0.36)
    CAM = [
        (0.00, 1.40, 1.00, 1.04, A), (1.40, 3.90, 1.12, 1.16, A), (3.90, 6.52, 1.00, 1.04, A),
        (6.52, 8.56, 1.00, 1.03, B), (8.56, 11.88, 1.12, 1.16, B), (11.88, 14.16, 1.00, 1.04, B),
        (23.36, 25.62, 1.12, 1.16, C),
        (42.44, 46.06, 1.00, 1.04, D), (46.06, 49.72, 1.14, 1.18, D),
        (49.72, 55.86, 1.00, 1.04, E), (55.86, 99.0, 1.12, 1.16, E),
    ]
    WHIPS = [23.36, 42.44]
if len(sys.argv) > 4 and sys.argv[4] == 'p9':      # agency CRM reel
    A, B, C, E = (0.50, 0.42), (0.50, 0.33), (0.50, 0.40), (0.49, 0.36)
    CAM = [
        (0.00, 7.80, 1.00, 1.05, A),
        (7.80, 9.66, 1.00, 1.03, B), (9.66, 12.20, 1.12, 1.16, B),
        (34.88, 36.94, 1.12, 1.16, C),
        (44.32, 47.56, 1.00, 1.04, E), (47.56, 99.0, 1.12, 1.16, E),
    ]
    WHIPS = [34.88, 44.32]
if len(sys.argv) > 4 and sys.argv[4] == 'p9uk':    # agency CRM reel, Ukrainian cut
    A, B, C, E = (0.50, 0.42), (0.50, 0.33), (0.50, 0.40), (0.49, 0.36)
    CAM = [
        (0.00, 7.96, 1.00, 1.05, A),
        (7.96, 9.80, 1.00, 1.03, B), (9.80, 12.30, 1.12, 1.16, B),
        (35.28, 37.45, 1.12, 1.16, C),
        (45.28, 48.58, 1.00, 1.04, E), (48.58, 99.0, 1.12, 1.16, E),
    ]
    WHIPS = [35.28, 45.28]
WHIP_LEN = 0.26


def cam_at(t):
    for t0, t1, s0, s1, a in CAM:
        if t0 <= t < t1:
            p = min(1.0, max(0.0, (t - t0) / max(1e-6, (min(t1, N / FPS) - t0))))
            p = p * p * (3 - 2 * p)
            return s0 + (s1 - s0) * p, a
    return 1.0, (0.5, 0.42)


def zoom(img, s, a):
    ax, ay = a[0] * W, a[1] * H
    M = np.float32([[s, 0, ax * (1 - s)], [0, s, ay * (1 - s)]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def whip(img, t):
    for w in WHIPS:
        if w <= t < w + WHIP_LEN:
            p = (t - w) / WHIP_LEN
            e = 1 - (1 - p) ** 3
            k = 1 + 0.30 * (1 - e)          # extra zoom that settles to 1
            spread = 0.10 * (1 - e)         # radial blur amount
            acc = np.zeros_like(img, dtype=np.float32)
            n = 8
            for i in range(n):
                acc += zoom(img, k * (1 + spread * i / (n - 1)), (0.5, 0.42)).astype(np.float32)
            return (acc / n).astype(np.uint8)
    return img


reader = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', SRC, '-vf',
                           f'fps={FPS},scale={W}:{H}:flags=lanczos,eq=contrast=1.04:saturation=1.08',
                           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
writer = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                           '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
i = 0
while True:
    buf = reader.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    t = i / FPS
    frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    s, a = cam_at(t)
    if s != 1.0:
        frame = zoom(frame, s, a)
    ov_path = os.path.join(OVL, f'f_{i:05d}.png')
    if os.path.exists(ov_path):
        ov = cv2.imread(ov_path, cv2.IMREAD_UNCHANGED)          # BGRA, or BGR when fully opaque
        rgb = ov[:, :, 2::-1]
        if ov.ndim == 3 and ov.shape[2] == 4:
            alpha = ov[:, :, 3:4].astype(np.float32) / 255.0
            frame = (frame.astype(np.float32) * (1 - alpha) + rgb.astype(np.float32) * alpha).astype(np.uint8)
        else:
            frame = rgb.copy()
    frame = whip(frame, t)
    writer.stdin.write(np.ascontiguousarray(frame).tobytes())
    i += 1
    if i % 100 == 0:
        print(f'{i}/{N}', flush=True)
writer.stdin.close(); writer.wait(); reader.wait()
print('frames', i)
