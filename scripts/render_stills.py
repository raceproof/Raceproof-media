"""Render feed post slides (HTML, 1080 x 1350) to PNG.

Usage:
  python3 scripts/render_stills.py posts/2026-10-19/mon-research-pacing-1.html [more.html ...]
Writes a PNG next to each HTML file (same name, .png).
Each HTML file must draw one 1080 x 1350 slide starting at the top-left corner.
"""
import os, sys
from playwright.sync_api import sync_playwright


def main(paths):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
        for path in paths:
            path = os.path.abspath(path)
            pg.goto('file://' + path)
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(300)
            out = os.path.splitext(path)[0] + '.png'
            pg.screenshot(path=out, clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1350})
            print('wrote', os.path.relpath(out))
        b.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
