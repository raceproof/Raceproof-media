"""Render a template mode as a muted website loop: MP4 (H.264) + WebM (VP9) + poster PNG.

Usage:
  python3 scripts/render_loop.py <template.html> <query> <W> <H> <out_dir> <name> <poster_t>

<query> is passed to the template (e.g. "mode=screen&lang=en"); the template sets window.DUR.
Targets under 3 MB per video file (re-encodes at a lower quality if needed).
"""
import os, sys, shutil, subprocess, tempfile
from playwright.sync_api import sync_playwright

FPS = 30
LIMIT = 3 * 1024 * 1024


def enc_mp4(frames, out, crf):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{frames}/%04d.png',
                    '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', str(crf),
                    '-preset', 'slow', '-tune', 'animation', '-movflags', '+faststart', '-an', out], check=True)


def enc_webm(frames, out, crf):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{frames}/%04d.png',
                    '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuv420p', '-b:v', '0', '-crf', str(crf),
                    '-row-mt', '1', '-deadline', 'good', '-cpu-used', '2', '-an', out], check=True)


def main(template, query, W, H, out_dir, name, poster_t):
    template = os.path.abspath(template)
    os.makedirs(out_dir, exist_ok=True)
    frames = tempfile.mkdtemp(prefix='frames-')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
        pg.goto(f'file://{template}?{query}')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        dur = pg.evaluate('window.DUR')
        n = int(round(dur * FPS))
        for i in range(n):
            pg.evaluate(f'render({i / FPS})')
            pg.screenshot(path=f'{frames}/{i:04d}.png', clip={'x': 0, 'y': 0, 'width': W, 'height': H})
        pg.evaluate(f'render({poster_t})')
        pg.screenshot(path=f'{out_dir}/{name}-poster.png', clip={'x': 0, 'y': 0, 'width': W, 'height': H})
        b.close()
    for crf in (24, 27, 30, 33):
        enc_mp4(frames, f'{out_dir}/{name}.mp4', crf)
        if os.path.getsize(f'{out_dir}/{name}.mp4') < LIMIT:
            break
    for crf in (36, 40, 44, 48):
        enc_webm(frames, f'{out_dir}/{name}.webm', crf)
        if os.path.getsize(f'{out_dir}/{name}.webm') < LIMIT:
            break
    shutil.rmtree(frames, ignore_errors=True)
    print('wrote', name, n, 'frames', dur, 's')


if __name__ == '__main__':
    if len(sys.argv) < 8:
        sys.exit(__doc__)
    a = sys.argv
    main(a[1], a[2], int(a[3]), int(a[4]), a[5], a[6], float(a[7]))
