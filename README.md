#!/usr/bin/env python3
"""Generates the animated SVGs used in the profile README.

    python3 scripts/build_assets.py

No dependencies. Everything is SMIL inside self-contained SVG files, because
GitHub renders SVGs referenced via <img> (with their animations) but strips
scripts, external fonts and inline styles from the README itself.
Edit THEMES / ROLES / STATIONS below and re-run.
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

THEMES = {
    "dark":  dict(bg="#0c0e12", ink="#ece7dc", mute="#8d8a82", accent="#ff6a3d", warm="#f2c14e"),
    "light": dict(bg="#f4f0e6", ink="#15171a", mute="#6f6b62", accent="#d9481c", warm="#a87400"),
}
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

ROLES = [
    "full-stack developer, founding team at Frog8",
    "self-service kiosks for transit and banking",
    "three.js, webgl and generative visuals",
]

STATIONS = [  # place, line 1, line 2
    ("Chennai",   "SRM IST, B.Tech",         "2017 to 2021"),
    ("Boulder",   "CU Boulder, Master's",    "2021 to 2022"),
    ("Mumbai",    "Technocrafts",            "2022 to 2025"),
    ("Bengaluru", "Frog8, founding team",    "2025 to now"),
]

SINE = ".37 0 .63 1"  # cubic-bezier that closely follows half a cosine wave


def f(x):
    s = f"{x:.1f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def cos_anim(attr, hi, lo, period, phase):
    """Cosine wave between hi and lo. phase in turns = how far into the cycle we start."""
    begin = -(phase % 1.0) * period
    return (f'<animate attributeName="{attr}" values="{f(hi)};{f(lo)};{f(hi)}" keyTimes="0;.5;1" '
            f'calcMode="spline" keySplines="{SINE};{SINE}" dur="{period}s" begin="{begin:.2f}s" '
            f'repeatCount="indefinite"/>')


def sphere(t, cx0, cy0, R=150, n=170, tilt_deg=22, period=30, seed=9):
    """Fibonacci sphere of particles rotating about its vertical axis, seen from slightly above."""
    rnd = random.Random(seed)
    tilt = math.radians(tilt_deg)
    golden = math.pi * (3 - math.sqrt(5))
    out = []
    for i in range(n):
        y = 1 - 2 * (i + 0.5) / n               # sin(latitude)
        a = R * math.sqrt(1 - y * y)            # radius of this latitude circle
        th0 = (i * golden) % (2 * math.pi)      # starting longitude
        yc = cy0 - R * y * math.cos(tilt)       # centre of the projected ellipse
        b = a * math.sin(tilt)                  # its vertical radius
        ph_x = th0 / (2 * math.pi)              # x follows cos(theta)
        ph_y = ph_x - 0.25                      # y and depth follow sin(theta)
        d = (math.sin(th0) + 1) / 2             # 0 = far side, 1 = near side
        col = t["accent"] if rnd.random() < 0.16 else t["ink"]
        out.append(
            f'<circle cx="{f(cx0 + a * math.cos(th0))}" cy="{f(yc + b * math.sin(th0))}" '
            f'r="{f(1.0 + 1.3 * d)}" fill="{col}" opacity="{0.12 + 0.83 * d:.2f}">'
            + cos_anim("cx", cx0 + a, cx0 - a, period, ph_x)
            + cos_anim("cy", yc + b, yc - b, period, ph_y)
            + cos_anim("opacity", 0.95, 0.12, period, ph_y)
            + cos_anim("r", 2.3, 1.0, period, ph_y)
            + "</circle>")
    return "\n".join(out)


def header(t):
    W, H = 1000, 380
    cx, cy = 770, 192
    roles = []
    for i, line in enumerate(ROLES):
        base = 1 if i == 0 else 0
        roles.append(
            f'<text x="58" y="250" font-family="{MONO}" font-size="19" fill="{t["mute"]}" opacity="{base}">{line}'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.04;.30;.34;1" dur="15s" '
            f'begin="{i * 5}s" repeatCount="indefinite"/></text>')
    rx = 208
    ry = f(rx * math.sin(math.radians(22)))
    nl = "\n"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Faaiz Akhtar</title>
<desc id="d">Full-stack developer in Bengaluru. A slowly rotating sphere of particles sits beside the name.</desc>
<defs>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{t["accent"]}" stop-opacity=".20"/>
    <stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/>
  </radialGradient>
  <path id="orbit" d="M {cx - rx} {cy} a {rx} {ry} 0 1 0 {2 * rx} 0 a {rx} {ry} 0 1 0 {-2 * rx} 0"/>
</defs>
<rect width="{W}" height="{H}" rx="20" fill="{t["bg"]}"/>
<circle cx="{cx}" cy="{cy}" r="230" fill="url(#glow)"/>
<use href="#orbit" fill="none" stroke="{t["mute"]}" stroke-opacity=".28" stroke-width="1" stroke-dasharray="2 7"/>
{sphere(t, cx, cy)}
<circle r="4" fill="{t["warm"]}"><animateMotion dur="11s" repeatCount="indefinite"><mpath href="#orbit"/></animateMotion></circle>
<text x="58" y="104" font-family="{MONO}" font-size="16" fill="{t["accent"]}">github.com/faaiz09</text>
<text x="54" y="196" font-family="{SERIF}" font-size="86" font-weight="600" letter-spacing="-2" fill="{t["ink"]}">Faaiz Akhtar</text>
{nl.join(roles)}
<text x="58" y="322" font-family="{MONO}" font-size="15" fill="{t["mute"]}">Bengaluru, India (UTC+5:30)</text>
</svg>
'''


def journey(t):
    W, H = 840, 230
    y = 112
    x0, x1 = 70, 770
    n = len(STATIONS)
    parts = []
    for i, (place, l1, l2) in enumerate(STATIONS):
        x = x0 + (x1 - x0) * i / (n - 1)
        last = i == n - 1
        anchor = "start" if i == 0 else ("end" if last else "middle")
        tx = x - 12 if i == 0 else (x + 12 if last else x)
        if last:
            parts.append(
                f'<circle cx="{f(x)}" cy="{y}" r="10" fill="none" stroke="{t["accent"]}" stroke-width="2">'
                f'<animate attributeName="r" values="10;26" dur="2.4s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values=".7;0" dur="2.4s" repeatCount="indefinite"/></circle>')
        parts.append(
            f'<circle cx="{f(x)}" cy="{y}" r="10" fill="{t["accent"] if last else t["bg"]}" '
            f'stroke="{t["accent"] if last else t["ink"]}" stroke-width="3.5"/>')
        parts.append(f'<text x="{f(tx)}" y="{y - 32}" text-anchor="{anchor}" font-family="{SERIF}" font-size="26" '
                     f'font-weight="600" fill="{t["ink"]}">{place}</text>')
        parts.append(f'<text x="{f(tx)}" y="{y + 44}" text-anchor="{anchor}" font-family="{MONO}" font-size="14" '
                     f'fill="{t["ink"]}">{l1}</text>')
        parts.append(f'<text x="{f(tx)}" y="{y + 66}" text-anchor="{anchor}" font-family="{MONO}" font-size="14" '
                     f'fill="{t["mute"]}">{l2}</text>')
    alt = "; ".join(f"{p}: {a}, {b}" for p, a, b in STATIONS)
    nl = "\n"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Route so far</title>
<desc id="d">{alt}</desc>
<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>
<text x="58" y="36" font-family="{MONO}" font-size="14" fill="{t["accent"]}">route so far</text>
<path id="line" d="M {x0} {y} H {x1}" stroke="{t["mute"]}" stroke-opacity=".55" stroke-width="5" stroke-linecap="round" fill="none"/>
<rect x="-13" y="-5" width="26" height="10" rx="5" fill="{t["warm"]}" opacity="0">
  <animateMotion dur="9s" repeatCount="indefinite" calcMode="spline" keyPoints="0;1;1" keyTimes="0;.8;1" keySplines=".45 0 .2 1;0 0 1 1"><mpath href="#line"/></animateMotion>
  <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.06;.74;.8;1" dur="9s" repeatCount="indefinite"/>
</rect>
{nl.join(parts)}
</svg>
'''


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, theme in THEMES.items():
        for kind, fn in (("header", header), ("journey", journey)):
            p = os.path.normpath(os.path.join(OUT, f"{kind}-{name}.svg"))
            with open(p, "w") as fh:
                fh.write(fn(theme))
            print(f"{p}  {os.path.getsize(p) / 1024:.0f} KB")
