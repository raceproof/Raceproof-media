"""Render an animated reel template to MP4, plus a 9:16 cover and a 4:5 grid still.

Usage:
  python3 scripts/render_reel.py <template.html> <out_dir> <name> <duration_s> <cover_t_s> [still_y]

The template must define window.render(t) that draws the frame at t seconds,
and show its small logo when loaded with ?still=1.
Set REEL_QUERY to pass extra query params (e.g. lang=es).
Outputs: <out_dir>/<name>.mp4 (1080 x 1920, 30 fps, H.264, no audio),
         <out_dir>/<name>-cover.png, <out_dir>/<name>-still-4x5.png
"""
import os, sys, shutil, subprocess, tempfile
from playwright.sync_api import sync_playwright

FPS = 30
QUERY = os.environ.get('REEL_QUERY', '')   # e.g. REEL_QUERY='lang=es'


def main(template, out_dir, name, dur, cover_t, still_y=150):
    template = os.path.abspath(template)
    os.makedirs(out_dir, exist_ok=True)
    frames = tempfile.mkdtemp(prefix='frames-')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
        pg.goto(f'file://{template}?{QUERY}')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        n = int(round(dur * FPS))
        for i in range(n):
            pg.evaluate(f'render({i / FPS})')
            pg.screenshot(path=f'{frames}/{i:04d}.png', clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1920})
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{frames}/%04d.png',
                        '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '18',
                        '-movflags', '+faststart', '-an', f'{out_dir}/{name}.mp4'], check=True)
        pg.goto(f'file://{template}?{QUERY}&still=1&t={cover_t}')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{out_dir}/{name}-cover.png', clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1920})
        pg.screenshot(path=f'{out_dir}/{name}-still-4x5.png', clip={'x': 0, 'y': still_y, 'width': 1080, 'height': 1350})
        b.close()
    shutil.rmtree(frames, ignore_errors=True)
    print('wrote', name, n, 'frames')


if __name__ == '__main__':
    if len(sys.argv) < 6:
        sys.exit(__doc__)
    a = sys.argv
    main(a[1], a[2], a[3], float(a[4]), float(a[5]), int(a[6]) if len(a) > 6 else 150)
