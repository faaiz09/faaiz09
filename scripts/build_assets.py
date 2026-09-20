#!/usr/bin/env python3
"""Generates the animated SVGs used in the profile README.

    python3 scripts/build_assets.py

No dependencies. All motion is SMIL inside self-contained SVG files, because
GitHub renders SVGs referenced via <img> (animations included) but strips
scripts, external fonts and inline styles from the README itself.
Edit the data blocks below and re-run.
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

THEMES = {
    "dark":  dict(bg="#0c0e12", panel="#171b22", ink="#ece7dc", mute="#8d8a82", accent="#ff6a3d", warm="#f2c14e"),
    "light": dict(bg="#f4f0e6", panel="#e6dfcf", ink="#15171a", mute="#6f6b62", accent="#d9481c", warm="#a87400"),
}
SCREEN = dict(bg="#06080b", ink="#ece7dc", mute="#8d8a82", accent="#ff6a3d")  # kiosk screen: dark in both themes
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

ROLES = [
    "Full-stack developer and Founding Member at Frog8",
    "Kiosk, web and mobile systems for banking and transit",
    "Full stack by trade, front end by preference",
]

STATIONS = [  # place, line 1, line 2
    ("Chennai",   "SRM IST, B.Tech (CSE)",   "2017 to 2021"),
    ("Mumbai",    "Technocrafts Switchgear", "2022 to 2025"),
    ("Bengaluru", "Frog8, Founding Member",  "2025 to present"),
]

TERMINAL = [  # (command, output)
    ("whoami",           "Faaiz Akhtar, full-stack developer, Bengaluru"),
    ("cat role.txt",     "Founding Member, Frog8 Technology Services"),
    ("cat now.txt",      "Kiosk UI for metro QR ticketing and card recharge"),
    ("ls shipped/",      "transigo-2000/  veriphy/  f8ops/  cmms/  ocr-cheque-reader/"),
    ("cat learning.txt", "Laravel and PHP"),
]

SYSTEM_MAP = [  # column title, nodes
    ("Surfaces",     ["Kiosk UI", "Web apps", "Mobile apps", "WhatsApp flows"]),
    ("Intelligence", ["OCR (Tesseract)", "RAG assistants", "Bots and automation"]),
    ("Delivery",     ["Docker", "GCP (GKE)", "GitHub Actions"]),
]

TOOLBOX = ["React Native", "Tesseract OCR", "RAG pipelines", "OpenAI API", "Twilio", "WhatsApp Business API", "MCP automations",
           "Framer Motion", "SSMS", "Grafana", "CI/CD"]

SINE = ".37 0 .63 1"  # cubic-bezier that closely follows half a cosine wave


def f(x):
    s = f"{x:.1f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def svg_open(w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {f(h)}" width="{w}" height="{f(h)}" '
            f'role="img" aria-labelledby="t d">\n<title id="t">{title}</title>\n<desc id="d">{desc}</desc>')


# ---------------------------------------------------------------- header

def cos_anim(attr, hi, lo, period, phase):
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
        y = 1 - 2 * (i + 0.5) / n
        a = R * math.sqrt(1 - y * y)
        th0 = (i * golden) % (2 * math.pi)
        yc = cy0 - R * y * math.cos(tilt)
        b = a * math.sin(tilt)
        ph_x = th0 / (2 * math.pi)
        ph_y = ph_x - 0.25
        d = (math.sin(th0) + 1) / 2
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
        roles.append(
            f'<text x="58" y="250" font-family="{MONO}" font-size="18" fill="{t["mute"]}" opacity="{1 if i == 0 else 0}">{line}'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.04;.30;.34;1" dur="15s" '
            f'begin="{i * 5}s" repeatCount="indefinite"/></text>')
    rx = 208
    ry = f(rx * math.sin(math.radians(22)))
    nl = "\n"
    return f'''{svg_open(W, H, "Faaiz Akhtar", "Full-stack developer and Founding Member at Frog8, Bengaluru. A slowly rotating sphere of particles sits beside the name.")}
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


# ---------------------------------------------------------------- journey

def journey(t):
    W, H = 840, 230
    y, x0, x1 = 112, 70, 770
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
        parts.append(f'<circle cx="{f(x)}" cy="{y}" r="10" fill="{t["accent"] if last else t["bg"]}" '
                     f'stroke="{t["accent"] if last else t["ink"]}" stroke-width="3.5"/>')
        parts.append(f'<text x="{f(tx)}" y="{y - 32}" text-anchor="{anchor}" font-family="{SERIF}" font-size="26" '
                     f'font-weight="600" fill="{t["ink"]}">{place}</text>')
        parts.append(f'<text x="{f(tx)}" y="{y + 44}" text-anchor="{anchor}" font-family="{MONO}" font-size="14" fill="{t["ink"]}">{l1}</text>')
        parts.append(f'<text x="{f(tx)}" y="{y + 66}" text-anchor="{anchor}" font-family="{MONO}" font-size="14" fill="{t["mute"]}">{l2}</text>')
    alt = "; ".join(f"{p}: {a}, {b}" for p, a, b in STATIONS)
    nl = "\n"
    return f'''{svg_open(W, H, "Route so far", alt)}
<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>
<text x="58" y="36" font-family="{MONO}" font-size="14" fill="{t["accent"]}">Route so far</text>
<path id="line" d="M {x0} {y} H {x1}" stroke="{t["mute"]}" stroke-opacity=".55" stroke-width="5" stroke-linecap="round" fill="none"/>
<rect x="-13" y="-5" width="26" height="10" rx="5" fill="{t["warm"]}" opacity="0">
  <animateMotion dur="9s" repeatCount="indefinite" calcMode="spline" keyPoints="0;1;1" keyTimes="0;.8;1" keySplines=".45 0 .2 1;0 0 1 1"><mpath href="#line"/></animateMotion>
  <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.06;.74;.8;1" dur="9s" repeatCount="indefinite"/>
</rect>
{nl.join(parts)}
</svg>
'''


# ---------------------------------------------------------------- kiosk

def qr(x, y, cell, fill, n=9, seed=4):
    """A decorative QR-like glyph (not a scannable code)."""
    rnd = random.Random(seed)
    out = []
    for r in range(n):
        for c in range(n):
            in_finder = (r < 3 or r >= n - 3) and (c < 3 or c >= n - 3) and not (r >= n - 3 and c >= n - 3)
            if in_finder:
                if (r % (n - 3) if r >= n - 3 else r) == 1 and (c % (n - 3) if c >= n - 3 else c) == 1:
                    continue
            elif rnd.random() < 0.5:
                continue
            out.append(f'<rect x="{f(x + c * cell)}" y="{f(y + r * cell)}" width="{f(cell)}" height="{f(cell)}"/>')
    return f'<g fill="{fill}">' + "".join(out) + "</g>"


def kiosk_inner(t):
    """The kiosk drawing itself (no <svg> wrapper): three screens, then a ticket slides out."""
    W, H, D = 360, 450, "10s"
    S = SCREEN

    def state(vals, kts, base, body):
        return (f'<g opacity="{base}">{body}<animate attributeName="opacity" values="{vals}" keyTimes="{kts}" '
                f'dur="{D}" repeatCount="indefinite"/></g>')

    def heading(txt):
        return f'<text x="106" y="86" font-family="{SERIF}" font-size="21" font-weight="600" fill="{S["ink"]}">{txt}</text>'

    def btn(y, label, hot=False):
        return (f'<rect x="106" y="{y}" width="148" height="38" rx="8" fill="none" '
                f'stroke="{S["accent"] if hot else S["mute"]}" stroke-width="1.6"/>'
                f'<text x="180" y="{y + 24}" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{S["ink"]}">{label}</text>')

    s_a = (heading("Where to?") + btn(108, "QR ticket", hot=True) + btn(156, "Card recharge")
           + f'<circle cx="228" cy="127" r="4" fill="{S["accent"]}" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;.9;0;0" keyTimes="0;.20;.24;.30;1" dur="{D}" repeatCount="indefinite"/>'
             f'<animate attributeName="r" values="4;4;16;16" keyTimes="0;.20;.30;1" dur="{D}" repeatCount="indefinite"/></circle>')
    chips = ""
    for i, lab in enumerate(("UPI", "Card", "Cash")):
        x, hot = 106 + i * 51, i == 0
        chips += (f'<rect x="{x}" y="112" width="46" height="34" rx="7" fill="{S["accent"] if hot else "none"}" '
                  f'stroke="{S["accent"] if hot else S["mute"]}" stroke-width="1.6"/>'
                  f'<text x="{x + 23}" y="134" text-anchor="middle" font-family="{MONO}" font-size="13" '
                  f'fill="{S["bg"] if hot else S["ink"]}">{lab}</text>')
    s_b = (heading("Pay") + chips
           + f'<rect x="106" y="166" width="148" height="6" rx="3" fill="{S["mute"]}" opacity=".35"/>'
             f'<rect x="106" y="166" width="148" height="6" rx="3" fill="{S["accent"]}">'
             f'<animate attributeName="width" values="0;0;148;148" keyTimes="0;.36;.58;1" dur="{D}" repeatCount="indefinite"/></rect>'
             f'<text x="106" y="196" font-family="{MONO}" font-size="12" fill="{S["mute"]}">Waiting for payment</text>')
    s_c = (heading("Done") + qr(106, 104, 8, S["ink"])
           + "".join(f'<text x="190" y="{124 + 18 * k}" font-family="{MONO}" font-size="12" fill="{S["mute"]}">{w}</text>'
                     for k, w in enumerate(("Collect", "your", "ticket")))
           + f'<path d="M190 178 l7 7 l14 -16" fill="none" stroke="{S["accent"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    return f'''<defs><clipPath id="slot"><rect x="0" y="366" width="{W}" height="90"/></clipPath></defs>
<ellipse cx="180" cy="438" rx="128" ry="8" fill="{t["ink"]}" opacity=".10"/>
<rect x="66" y="16" width="228" height="418" rx="20" fill="{t["panel"]}" stroke="{t["mute"]}" stroke-opacity=".45" stroke-width="1.5"/>
<circle cx="180" cy="28" r="2.5" fill="{t["mute"]}"/>
<rect x="86" y="40" width="188" height="186" rx="10" fill="{S["bg"]}"/>
{state("1;1;0;0;1", "0;.30;.33;.96;1", 1, s_a)}
{state("0;0;1;1;0;0", "0;.30;.33;.60;.63;1", 0, s_b)}
{state("0;0;1;1;0;0", "0;.60;.63;.92;.95;1", 0, s_c)}
<rect x="100" y="252" width="84" height="56" rx="8" fill="{t["bg"]}" stroke="{t["mute"]}" stroke-opacity=".4"/>
<rect x="114" y="270" width="56" height="6" rx="3" fill="{t["ink"]}" opacity=".55"/>
<text x="142" y="298" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{t["mute"]}">card</text>
<rect x="198" y="252" width="62" height="56" rx="8" fill="{t["bg"]}" stroke="{t["mute"]}" stroke-opacity=".4"/>
<rect x="212" y="262" width="34" height="22" rx="3" fill="{t["accent"]}" opacity=".25">
  <animate attributeName="opacity" values=".25;.25;.9;.25;.25" keyTimes="0;.40;.48;.58;1" dur="{D}" repeatCount="indefinite"/></rect>
<text x="229" y="298" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{t["mute"]}">scan</text>
<text x="180" y="342" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{t["mute"]}">tickets</text>
<g clip-path="url(#slot)">
  <g opacity="0">
    <rect x="132" y="364" width="96" height="56" rx="4" fill="#f7f3e9" stroke="{t["mute"]}" stroke-opacity=".5"/>
    {qr(140, 374, 4, "#15171a", seed=11)}
    <rect x="184" y="378" width="34" height="4" fill="#15171a" opacity=".7"/>
    <rect x="184" y="388" width="26" height="4" fill="#15171a" opacity=".4"/>
    <rect x="184" y="398" width="30" height="4" fill="#15171a" opacity=".4"/>
    <animateTransform attributeName="transform" type="translate" values="0 -60;0 -60;0 0;0 0" keyTimes="0;.68;.80;1" dur="{D}" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.66;.67;.90;.94;1" dur="{D}" repeatCount="indefinite"/>
  </g>
</g>
<rect x="120" y="354" width="120" height="12" rx="6" fill="{S["bg"]}"/>
'''


def kiosk_strip(t):
    """Full-width banner: the kiosk on the left, the three steps on the right, highlighted in sync."""
    W, H, D = 840, 320, "10s"
    steps = [("Choose", "QR ticket or metro card recharge", "1;1;.45;.45;1", "0;.30;.33;.96;1"),
             ("Pay", "UPI, card or cash", ".45;.45;1;1;.45;.45", "0;.30;.33;.60;.63;1"),
             ("Collect", "A printed QR ticket, ready to scan", ".45;.45;1;1;.45;.45", "0;.60;.63;.92;.95;1")]
    rows = []
    for i, (title, text, vals, kts) in enumerate(steps):
        y = 112 + i * 70
        rows.append(
            f'<g opacity="{1 if i == 0 else .45}">'
            f'<circle cx="352" cy="{y - 8}" r="17" fill="none" stroke="{t["accent"]}" stroke-width="2"/>'
            f'<text x="352" y="{y - 2}" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{t["accent"]}">{i + 1}</text>'
            f'<text x="388" y="{y - 6}" font-family="{SERIF}" font-size="25" font-weight="600" fill="{t["ink"]}">{title}</text>'
            f'<text x="388" y="{y + 16}" font-family="{MONO}" font-size="14" fill="{t["mute"]}">{text}</text>'
            f'<animate attributeName="opacity" values="{vals}" keyTimes="{kts}" dur="{D}" repeatCount="indefinite"/></g>')
    nl = "\n"
    return f'''{svg_open(W, H, "A metro ticket, start to finish", "An illustrated self-service kiosk cycles through three steps. 1, Choose: QR ticket or metro card recharge. 2, Pay: UPI, card or cash. 3, Collect: a printed QR ticket, ready to scan.")}
<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>
<g transform="translate(34 14) scale(.65)">{kiosk_inner(t)}</g>
<text x="335" y="52" font-family="{MONO}" font-size="14" fill="{t["accent"]}">The kind of flow I build: a metro ticket, start to finish</text>
{nl.join(rows)}
</svg>
'''


# ---------------------------------------------------------------- terminal

def terminal(t):
    """A terminal that types out a short introduction, then loops."""
    W, FS, CW, LH, x0, y0 = 840, 15, 9.0, 25, 34, 78
    events, clock = [], 0.8
    for cmd, out in TERMINAL:
        dur = len(cmd) * 0.07
        events.append((cmd, out, clock, clock + dur))
        clock += dur + 1.3
    total = clock + 4.0
    T = f"{total:.1f}s"
    H = y0 + (len(TERMINAL) * 2 + 1) * LH + 6
    parts, defs, y = [], [], y0
    for i, (cmd, out, a, b) in enumerate(events):
        ka, kb = a / total, b / total
        w, px = len(cmd) * CW + 4, x0 + 2 * CW
        defs.append(f'<clipPath id="c{i}"><rect x="{f(px)}" y="{y - 16}" width="{f(w)}" height="22">'
                    f'<animate attributeName="width" values="0;0;{f(w)};{f(w)}" keyTimes="0;{ka:.4f};{kb:.4f};1" dur="{T}" repeatCount="indefinite"/></rect></clipPath>')
        parts.append(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{t["accent"]}">$'
                     f'<animate attributeName="opacity" calcMode="discrete" values="0;1" keyTimes="0;{max(ka - 0.01, 0.001):.4f}" dur="{T}" repeatCount="indefinite"/></text>')
        parts.append(f'<text x="{f(px)}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{t["ink"]}" '
                     f'textLength="{f(len(cmd) * CW)}" lengthAdjust="spacing" clip-path="url(#c{i})">{cmd}</text>')
        y += LH
        parts.append(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{t["mute"]}" '
                     f'textLength="{f(len(out) * CW)}" lengthAdjust="spacing">{out}'
                     f'<animate attributeName="opacity" calcMode="discrete" values="0;1" keyTimes="0;{(b + 0.3) / total:.4f}" dur="{T}" repeatCount="indefinite"/></text>')
        y += LH
    kend = (events[-1][3] + 1.0) / total
    parts.append(f'<g><text x="{x0}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{t["accent"]}">$</text>'
                 f'<rect x="{f(x0 + 2 * CW)}" y="{y - 13}" width="9" height="16" fill="{t["ink"]}">'
                 f'<animate attributeName="opacity" calcMode="discrete" values="1;0" keyTimes="0;.5" dur="1.1s" repeatCount="indefinite"/></rect>'
                 f'<animate attributeName="opacity" calcMode="discrete" values="0;1" keyTimes="0;{kend:.4f}" dur="{T}" repeatCount="indefinite"/></g>')
    alt = " ".join(f"{c}: {o}." for c, o in TERMINAL)
    nl = "\n"
    return f'''{svg_open(W, H, "Terminal introduction", alt)}
<defs>{"".join(defs)}</defs>
<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>
<path d="M0 40 V14 a14 14 0 0 1 14 -14 H{W - 14} a14 14 0 0 1 14 14 V40 Z" fill="{t["panel"]}"/>
<circle cx="26" cy="20" r="5.5" fill="{t["accent"]}"/><circle cx="46" cy="20" r="5.5" fill="{t["warm"]}"/><circle cx="66" cy="20" r="5.5" fill="{t["mute"]}"/>
<text x="{W // 2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["mute"]}">faaiz@bengaluru: ~</text>
{nl.join(parts)}
</svg>
'''


# ---------------------------------------------------------------- system map

def system_map(t):
    """Three columns of capabilities with data pulses travelling between them."""
    W, H = 840, 330
    col_x, col_w, node_h, top = [40, 320, 600], 200, 40, 84
    centres, parts = [], []
    for ci, (title, nodes) in enumerate(SYSTEM_MAP):
        x = col_x[ci]
        parts.append(f'<text x="{x}" y="58" font-family="{SERIF}" font-size="22" font-weight="600" fill="{t["ink"]}">{title}</text>')
        gap = (H - top - 30 - len(nodes) * node_h) / max(len(nodes) - 1, 1)
        ys = []
        for ni, label in enumerate(nodes):
            y = top + ni * (node_h + gap)
            ys.append(y + node_h / 2)
            parts.append(f'<rect x="{x}" y="{f(y)}" width="{col_w}" height="{node_h}" rx="9" fill="{t["panel"]}" stroke="{t["mute"]}" stroke-opacity=".45"/>'
                         f'<circle cx="{x + 18}" cy="{f(y + node_h / 2)}" r="4" fill="{t["accent"]}">'
                         f'<animate attributeName="opacity" values="1;.25;1" dur="2.6s" begin="{(ci * 3 + ni) * 0.37:.2f}s" repeatCount="indefinite"/></circle>'
                         f'<text x="{x + 34}" y="{f(y + node_h / 2 + 5)}" font-family="{MONO}" font-size="14" fill="{t["ink"]}">{label}</text>')
        centres.append(ys)
    wires, k = [], 0
    rnd = random.Random(3)
    for ci in range(2):
        xa, xb = col_x[ci] + col_w, col_x[ci + 1]
        xm = (xa + xb) / 2
        for ya in centres[ci]:
            for yb in centres[ci + 1]:
                pid = f"w{k}"
                wires.append(f'<path id="{pid}" d="M{xa} {f(ya)} C{f(xm)} {f(ya)} {f(xm)} {f(yb)} {xb} {f(yb)}" fill="none" '
                             f'stroke="{t["mute"]}" stroke-opacity=".22" stroke-width="1.2"/>')
                if rnd.random() < 0.6:
                    dur = 2.6 + rnd.random() * 2.4
                    wires.append(f'<circle r="3" fill="{t["warm"]}"><animateMotion dur="{dur:.1f}s" begin="-{rnd.random() * dur:.1f}s" '
                                 f'repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion></circle>')
                k += 1
    alt = ". ".join(f"{title}: {', '.join(nodes)}" for title, nodes in SYSTEM_MAP)
    nl = "\n"
    return f'''{svg_open(W, H, "What I work across", alt)}
<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>
{nl.join(wires)}
{nl.join(parts)}
</svg>
'''


# ---------------------------------------------------------------- toolbox chips

def toolbox(t):
    W, FS, CW, pad, gap, rowh = 840, 14, 8.4, 16, 10, 44
    x, y, parts = 34, 26, []
    for i, label in enumerate(TOOLBOX):
        w = len(label) * CW + 2 * pad
        if x + w > W - 34:
            x, y = 34, y + rowh
        parts.append(f'<rect x="{f(x)}" y="{y}" width="{f(w)}" height="32" rx="16" fill="{t["panel"]}" stroke="{t["accent"]}" stroke-opacity=".55">'
                     f'<animate attributeName="stroke-opacity" values=".25;.9;.25" dur="4s" begin="{i * 0.4:.1f}s" repeatCount="indefinite"/></rect>'
                     f'<text x="{f(x + w / 2)}" y="{y + 21}" text-anchor="middle" font-family="{MONO}" font-size="{FS}" fill="{t["ink"]}" '
                     f'textLength="{f(len(label) * CW)}" lengthAdjust="spacing">{label}</text>')
        x += w + gap
    H = y + 32 + 26
    nl = "\n"
    return f'''{svg_open(W, H, "Also in the toolbox", ", ".join(TOOLBOX))}
<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>
{nl.join(parts)}
</svg>
'''


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    kinds = (("header", header), ("journey", journey), ("kiosk-strip", kiosk_strip), ("terminal", terminal),
             ("system-map", system_map), ("toolbox", toolbox))
    for name, theme in THEMES.items():
        for kind, fn in kinds:
            p = os.path.normpath(os.path.join(OUT, f"{kind}-{name}.svg"))
            with open(p, "w") as fh:
                fh.write(fn(theme))
            print(f"{os.path.basename(p):24s} {os.path.getsize(p) / 1024:5.0f} KB")
