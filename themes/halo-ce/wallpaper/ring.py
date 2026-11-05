#!/usr/bin/env python3
"""Halo CE wallpaper: a ring world across a starfield, a distant sun, a banded gas giant.

Writes ring.svg next to this script; make the PNG with:
    ./ring.py && rsvg-convert -o ring.png ring.svg
Used by hyprpaper (../hypr/hyprpaper.conf) and the lock screen (../hypr/hyprlock.conf).
Original drawing, no game assets. Light comes from the sun (upper right), so the planet's
day side and the ring's sunlit rims face that way.
"""
import math
import os
import random

W, H = 1920, 1080
SUN = (1720, 120)
rnd = random.Random(117)          # fixed seed: the same sky every rebuild
out = []


def add(s):
    out.append(s)


# ---------- sky ----------
add(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
add('<ellipse cx="420" cy="260" rx="700" ry="380" fill="url(#nebViolet)"/>')
add('<ellipse cx="1080" cy="700" rx="760" ry="300" fill="url(#nebTeal)" transform="rotate(-12 1080 700)"/>')

for _ in range(520):
    x, y = rnd.uniform(0, W), rnd.uniform(0, H)
    r = rnd.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.6])
    o = rnd.uniform(0.2, 0.85) if r < 1.4 else 0.95
    c = rnd.choice(["#dce9f8"] * 5 + ["#b8d4ff", "#ffe6c2"])
    add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}" opacity="{o:.2f}"/>')

# ---------- sun ----------
sx, sy = SUN
add(f'<circle cx="{sx}" cy="{sy}" r="420" fill="url(#sunHalo)"/>')
add(f'<circle cx="{sx}" cy="{sy}" r="60" fill="url(#sunCore)"/>')
add(f'<rect x="{sx - 380}" y="{sy - 1}" width="760" height="2" fill="url(#streak)"/>')
add(f'<rect x="{sx - 1}" y="{sy - 90}" width="2" height="180" fill="url(#streakV)"/>')

# ---------- gas giant (bottom right), day side toward the sun ----------
px, py, pr = 1700, 1420, 800
add(f'<clipPath id="planetClip"><circle cx="{px}" cy="{py}" r="{pr}"/></clipPath>')
add(f'<circle cx="{px}" cy="{py}" r="{pr + 34}" fill="url(#atmo)"/>')
add(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="url(#planet)"/>')
add(f'<g clip-path="url(#planetClip)"><g transform="rotate(-18 {px} {py})" filter="url(#blur8)">')
for i, (dy, ry, col, op) in enumerate([(-700, 60, "#7d6aa8", 0.18), (-610, 34, "#c9a7d8", 0.10),
                                       (-540, 80, "#4c3f7a", 0.22), (-430, 46, "#a58bc4", 0.12),
                                       (-360, 90, "#2e2758", 0.25), (-240, 40, "#8f7bb8", 0.10),
                                       (-170, 70, "#3a3168", 0.2)]):
    add(f'<ellipse cx="{px}" cy="{py + dy}" rx="{pr * 1.3:.0f}" ry="{ry}" fill="{col}" opacity="{op}"/>')
add("</g></g>")
add(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="url(#night)"/>')       # terminator: dark away from the sun

# ---------- the ring ----------
# A tilted ellipse. Far arc (top) = the inner surface facing us: ocean, land, clouds.
# Near arc (bottom) = the outer hull: dark metal with a sunlit rim, passing in front of the planet.
cx, cy, rx, ry, tilt = 960, 540, 880, 175, -11
g = f'transform="translate({cx} {cy}) rotate({tilt})" mask="url(#ends)"'
far = f"M {-rx} 0 A {rx} {ry} 0 0 1 {rx} 0"
near = f"M {-rx} 0 A {rx} {ry} 0 0 0 {rx} 0"


def dashes(seed, short, long_, n=60):
    r = random.Random(seed)
    return " ".join(f"{r.uniform(*short):.0f} {r.uniform(*long_):.0f}" for _ in range(n))


# Each half is a crescent between two ellipses that meet at the tips, so the band is widest
# nearest the viewer and tapers to nothing at the ends (real perspective, no step at the joins).
FAR_T, NEAR_T = 13, 22                       # widest thickness of the far surface / near hull
farShape = f"M {-rx} 0 A {rx} {ry} 0 0 1 {rx} 0 A {rx} {ry - FAR_T} 0 0 0 {-rx} 0 Z"
nearShape = f"M {-rx} 0 A {rx} {ry} 0 0 0 {rx} 0 A {rx} {ry + NEAR_T} 0 0 1 {-rx} 0 Z"
mid = f"M {-rx} 0 A {rx} {ry - FAR_T / 2} 0 0 1 {rx} 0"
add(f'<clipPath id="farClip"><path d="{farShape}"/></clipPath>')
add(f"<g {g}>")
# far arc: the inner surface facing us (ocean, land, clouds), clipped to its crescent
add(f'<path d="{farShape}" fill="#164a73"/>')
add('<g clip-path="url(#farClip)">')
add(f'<path d="{mid}" fill="none" stroke="#3f7a4a" stroke-width="{FAR_T + 2}" opacity="0.85" filter="url(#blur1)" stroke-dasharray="{dashes(1, (40, 160), (20, 90))}"/>')
add(f'<path d="{mid}" fill="none" stroke="#8fb87e" stroke-width="3" opacity="0.35" filter="url(#blur1)" stroke-dasharray="{dashes(2, (8, 40), (40, 160))}"/>')
add(f'<path d="{mid}" fill="none" stroke="#ffffff" stroke-width="{FAR_T}" opacity="0.4" filter="url(#blur2)" stroke-dasharray="{dashes(3, (10, 50), (30, 120))}"/>')
add("</g>")
add(f'<path d="M {-rx} 0 A {rx} {ry} 0 0 1 {rx} 0" fill="none" stroke="#cfe3ff" stroke-width="1" opacity="0.7"/>')   # wall edge
# near arc: the outer hull, dark metal, sunlit along its top rim
add(f'<path d="{nearShape}" fill="#2f8cff" opacity="0.12" filter="url(#soft)"/>')                              # faint glow
add(f'<path d="{nearShape}" fill="url(#hull)"/>')
add(f'<path d="M {-rx} 0 A {rx} {ry + NEAR_T * 0.6} 0 0 0 {rx} 0" fill="none" stroke="#3a4a63" stroke-width="1.5" stroke-dasharray="3 22" opacity="0.8"/>')  # plating
add(f'<path d="M {-rx} 0 A {rx} {ry} 0 0 0 {rx} 0" fill="none" stroke="#e6f1ff" stroke-width="1.8"/>')         # sunlit rim
add("</g>")

# readability veil: a touch darker under the bar and behind the eww dashboard (left)
add(f'<rect width="{W}" height="{H}" fill="url(#veil)"/>')

defs = f"""
<radialGradient id="sky" cx="{SUN[0] / W:.3f}" cy="{SUN[1] / H:.3f}" r="1.1">
  <stop offset="0" stop-color="#0b1d44"/><stop offset="0.35" stop-color="#050f28"/><stop offset="1" stop-color="#010309"/></radialGradient>
<radialGradient id="nebViolet"><stop offset="0" stop-color="#5a3d8a" stop-opacity="0.16"/><stop offset="1" stop-color="#5a3d8a" stop-opacity="0"/></radialGradient>
<radialGradient id="nebTeal"><stop offset="0" stop-color="#1f6f8a" stop-opacity="0.12"/><stop offset="1" stop-color="#1f6f8a" stop-opacity="0"/></radialGradient>
<radialGradient id="sunHalo"><stop offset="0" stop-color="#cfe6ff" stop-opacity="0.35"/><stop offset="0.25" stop-color="#4da3ff" stop-opacity="0.10"/><stop offset="1" stop-color="#2f8cff" stop-opacity="0"/></radialGradient>
<radialGradient id="sunCore"><stop offset="0" stop-color="#ffffff"/><stop offset="0.12" stop-color="#ffffff"/><stop offset="0.3" stop-color="#d8ecff" stop-opacity="0.6"/><stop offset="1" stop-color="#7fb8ff" stop-opacity="0"/></radialGradient>
<linearGradient id="streak"><stop offset="0" stop-color="#bfe0ff" stop-opacity="0"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.7"/><stop offset="1" stop-color="#bfe0ff" stop-opacity="0"/></linearGradient>
<linearGradient id="streakV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe0ff" stop-opacity="0"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.5"/><stop offset="1" stop-color="#bfe0ff" stop-opacity="0"/></linearGradient>
<radialGradient id="planet" cx="0.62" cy="0.18" r="0.9">
  <stop offset="0" stop-color="#5a4a8c"/><stop offset="0.45" stop-color="#2c2460"/><stop offset="1" stop-color="#0c0b24"/></radialGradient>
<radialGradient id="atmo" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0.94" stop-color="#4da3ff" stop-opacity="0"/><stop offset="0.965" stop-color="#8cc4ff" stop-opacity="0.28"/><stop offset="1" stop-color="#2f8cff" stop-opacity="0"/></radialGradient>
<linearGradient id="night" x1="0.85" y1="0.1" x2="0.25" y2="0.7">
  <stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="0.45" stop-color="#000" stop-opacity="0.15"/><stop offset="1" stop-color="#01030a" stop-opacity="0.85"/></linearGradient>
<linearGradient id="hull" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#6d83a3"/><stop offset="0.35" stop-color="#2a3850"/><stop offset="1" stop-color="#0f1624"/></linearGradient>
<filter id="blur1"><feGaussianBlur stdDeviation="0.8"/></filter>
<filter id="blur2"><feGaussianBlur stdDeviation="1.4"/></filter>
<filter id="blur8" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="soft" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<linearGradient id="endsFade" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.08" stop-color="#fff" stop-opacity="1"/>
  <stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="ends" maskUnits="userSpaceOnUse" x="-{rx + 20}" y="-{ry + 40}" width="{2 * rx + 40}" height="{2 * ry + 80}">
  <rect x="-{rx + 20}" y="-{ry + 40}" width="{2 * rx + 40}" height="{2 * ry + 80}" fill="url(#endsFade)"/></mask>
<linearGradient id="veil" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#03091a" stop-opacity="0.35"/><stop offset="0.22" stop-color="#03091a" stop-opacity="0"/></linearGradient>
"""

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
       f"<defs>{defs}</defs>\n" + "\n".join(out) + "\n</svg>\n")
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "ring.svg"), "w") as f:
    f.write(svg)
