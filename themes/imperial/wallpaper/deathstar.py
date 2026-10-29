#!/usr/bin/env python3
"""Death Star wall lights as SVG.

Light pattern measured from Louie Mantia's "Death Star" wallpapers
(https://lmnt.me/blog/wallpapers/death-star.html), redrawn as vectors.

Rebuild the wallpaper:  ./deathstar.py 4 | rsvg-convert -o deathstar.png
(4 = light strips across the screen; rsvg-convert comes with librsvg)

Units: the original 6400px art scaled to 1600 wide. ROWS panels stack into
one long light strip that fills the screen height; the 16:9 width follows.
"""
import sys

ROWS = 3                    # panels stacked in each light strip
STRIP_W = 320               # a light strip holds 5 pills
PILL_W, PILL_PITCH, PILL_X0 = 30, 60, 25
PANEL_H = 440               # one wall panel, repeats vertically
SHORT, LONG, GAP = 128, 218, 43            # pill lengths inside a panel
PANEL_GAP = PANEL_H - (SHORT + GAP + LONG)  # space between panels (53)
CAP = 88                    # row of 5 equal short pills closing each end of a strip

TOP = PANEL_GAP / 2 + CAP + PANEL_GAP       # where the first panel starts
H = TOP + ROWS * PANEL_H + CAP + PANEL_GAP / 2
W = H * 16 / 9

BG = "#151718"
PILL_EDGE, PILL_CORE, GLOW = "#cfe6f0", "#f2ffff", "#cfe8ff"


def strip_xs(n):
    """Left edges of n strips, spread evenly and centred."""
    pitch = W / n
    return [pitch * (i + 0.5) - STRIP_W / 2 for i in range(n)]


def pills(n):
    for sx in strip_xs(n):
        for i in range(5):
            x = sx + PILL_X0 + i * PILL_PITCH
            # odd columns: short then long, even: long then short (the zig-zag)
            first, second = (SHORT, LONG) if i % 2 == 0 else (LONG, SHORT)
            yield x, PANEL_GAP / 2, CAP                  # top cap
            for k in range(ROWS):
                y = TOP + k * PANEL_H
                yield x, y, first
                yield x, y + first + GAP, second
            yield x, TOP + ROWS * PANEL_H, CAP           # bottom cap


def svg(n):
    rects = "".join(f'<rect x="{x:.1f}" y="{y:.1f}" width="{PILL_W}" height="{h}" '
                    f'rx="{PILL_W / 2}"/>' for x, y, h in pills(n))
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H}" '
        f'width="1920" height="1080">',
        '<defs>',
        f'<linearGradient id="pill" x1="0" x2="1">'
        f'<stop offset="0" stop-color="{PILL_EDGE}"/>'
        f'<stop offset=".5" stop-color="{PILL_CORE}"/>'
        f'<stop offset="1" stop-color="{PILL_EDGE}"/></linearGradient>',
        '<filter id="glow" x="-50%" y="-20%" width="200%" height="140%">'
        '<feGaussianBlur stdDeviation="6"/></filter>',
        '</defs>',
        f'<rect width="100%" height="100%" fill="{BG}"/>',
        # glow: a blurred copy under the sharp pills
        f'<g fill="{GLOW}" opacity=".6" filter="url(#glow)">{rects}</g>',
        f'<g fill="url(#pill)">{rects}</g>',
        '</svg>'])


if __name__ == "__main__":
    sys.stdout.write(svg(int(sys.argv[1]) if len(sys.argv) > 1 else 4))
