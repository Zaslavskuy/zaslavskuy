"""Composite: source video -> camera moves (push-ins / punch-ins / zoom-blur whips) -> overlay frames.
usage: python3 composite.py <source.mp4> <overlayDir> <out_noaudio.mp4>
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
WHIP_LEN = 0.26


def cam_at(t):
    for t0, t1, s0, s1, a in CAM:
        if t0 <= t < t1:
            p = (t - t0) / max(1e-6, (min(t1, 40) - t0))
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
                           f'scale={W}:{H}:flags=lanczos,eq=contrast=1.04:saturation=1.08',
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
