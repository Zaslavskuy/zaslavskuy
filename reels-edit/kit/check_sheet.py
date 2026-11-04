"""Contact sheet of overlay stills composited over the source video frames.
usage: python3 check_sheet.py <source.mp4> <stillsDir> <out.png> [cols]
"""
import sys, glob, os, subprocess, io
from PIL import Image, ImageDraw

src, d, out = sys.argv[1:4]
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
files = sorted(glob.glob(os.path.join(d, 't_*.png')), key=lambda f: float(os.path.basename(f)[2:-4]))
tw, th = 240, 427
sheet = Image.new('RGB', (cols * tw, ((len(files) + cols - 1) // cols) * th), 'black')
for i, f in enumerate(files):
    t = float(os.path.basename(f)[2:-4])
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', src, '-frames:v', '1',
                          '-vf', 'scale=1080:1920', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
    base = Image.open(io.BytesIO(raw)).convert('RGBA')
    ov = Image.open(f).convert('RGBA')
    base.alpha_composite(ov)
    im = base.convert('RGB').resize((tw, th), Image.LANCZOS)
    ImageDraw.Draw(im).text((4, 4), f'{t:.2f}', fill='yellow')
    sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
sheet.save(out)
