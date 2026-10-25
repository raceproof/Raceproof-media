"""Finish a race Reel: crossfade the standard end card onto the rendered body and keep the template's
closing line (#close) on screen over the end card's empty top area.

Usage:
  python3 scripts/add_endcard.py <template.html> <body.mp4> <out.mp4> [en|es]

<body.mp4> is the render_reel.py output for <template.html>. The template must define window.DURATION,
window.render(t) and a #close element inside #E (scenes #A to #D are hidden for the overlay).
Crossfade 0.4 s; the overlay starts 0.1 s before the fade so the line never flickers.
"""
import os, sys, subprocess, tempfile
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(template, body, out, lang='en'):
    template = os.path.abspath(template)
    tmp = tempfile.mkdtemp(prefix='endcard-')
    overlay = os.path.join(tmp, 'close.png')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto('file://' + template)
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        dur = pg.evaluate('window.DURATION')
        pg.evaluate(f"""render({dur} - 0.1);
          for (const el of [document.documentElement, document.body, document.querySelector('#stage')]) el.style.background = 'transparent';
          ['#A','#B','#C','#D'].forEach(s => {{ const e = document.querySelector(s); if (e) e.style.display = 'none'; }});""")
        pg.screenshot(path=overlay, omit_background=True)
        b.close()
    end = os.path.join(ROOT, 'assets', 'video', 'endcard', f'raceproof-endcard-{lang}.mp4')
    off = dur - 0.4
    fc = ("[0:v]settb=AVTB,fps=30,format=yuv420p[a];[1:v]settb=AVTB,fps=30,format=yuv420p[b];"
          f"[a][b]xfade=transition=fade:duration=0.4:offset={off}[x];[2:v]format=rgba[t];"
          f"[x][t]overlay=0:0:enable='gte(t,{off - 0.1})':shortest=1,format=yuv420p[v]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', body, '-i', end, '-loop', '1', '-i', overlay,
                    '-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                    '-crf', '18', '-movflags', '+faststart', '-an', out], check=True)
    print('wrote', out)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(*sys.argv[1:5])
