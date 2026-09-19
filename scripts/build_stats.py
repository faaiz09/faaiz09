#!/usr/bin/env python3
"""Builds assets/stats-dark.svg and assets/stats-light.svg from live GitHub data.

Runs inside the "Profile stats" GitHub Actions workflow (it needs GITHUB_TOKEN for
the contribution count; the language breakdown works without a token). Locally:

    GITHUB_TOKEN=... python3 scripts/build_stats.py faaiz09

No third-party services and no dependencies: it talks to api.github.com directly
and draws the card in the same visual style as the rest of the profile.
"""
import json
import os
import sys
import urllib.request

from build_assets import MONO, OUT, SERIF, THEMES, f, svg_open

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
SKIP_LANGS = {"HTML", "CSS", "SCSS"}          # markup and styles would otherwise dominate the chart
LANG_COLOURS = ["accent", "warm", "#4fb0a5", "ink", "#b9683f", "mute", "mute"]


def call(url, payload=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch(user):
    profile = call(f"{API}/users/{user}")
    repos, page = [], 1
    while True:
        batch = call(f"{API}/users/{user}/repos?per_page=100&type=owner&page={page}")
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    langs = {}
    for repo in repos:
        if repo.get("fork"):
            continue
        try:
            repo_langs = call(repo["languages_url"])
        except Exception as err:  # one unreadable repository should not break the card
            print(f"warning: skipped {repo.get('name')}: {err}", file=sys.stderr)
            continue
        for name, size in repo_langs.items():
            if name not in SKIP_LANGS:
                langs[name] = langs.get(name, 0) + size
    contributions = None
    if TOKEN:
        try:
            query = "query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{totalContributions}}}}"
            result = call(f"{API}/graphql", {"query": query, "variables": {"u": user}})
            contributions = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        except Exception as err:  # the card still renders without this number
            print(f"warning: could not read contributions: {err}", file=sys.stderr)
    return dict(user=user, repos=profile.get("public_repos", len(repos)),
                since=(profile.get("created_at") or "")[:4], contributions=contributions, langs=langs)


def render(data, t):
    W, H = 840, 250
    facts = []
    if data["contributions"] is not None:
        facts.append((f'{data["contributions"]:,}', "contributions in the last year"))
    facts.append((str(data["repos"]), "public repositories"))
    if data["since"]:
        facts.append((data["since"], "joined GitHub"))
    parts = []
    for i, (big, small) in enumerate(facts[:3]):
        y = 78 + i * 62
        parts.append(f'<text x="40" y="{y}" font-family="{SERIF}" font-size="34" font-weight="600" fill="{t["ink"]}">{big}</text>'
                     f'<text x="40" y="{y + 20}" font-family="{MONO}" font-size="13" fill="{t["mute"]}">{small}</text>')

    ranked = sorted(data["langs"].items(), key=lambda kv: -kv[1])
    top, rest = ranked[:6], sum(v for _, v in ranked[6:])
    if rest:
        top.append(("Other", rest))
    total = sum(v for _, v in top) or 1
    bx, bw, by = 330, 470, 64
    parts.append(f'<text x="{bx}" y="44" font-family="{MONO}" font-size="14" fill="{t["accent"]}">Languages across my public repositories</text>')
    parts.append(f'<clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw}" height="16" rx="8">'
                 f'<animate attributeName="width" values="0;{bw}" dur="1.6s" calcMode="spline" keySplines=".2 .7 .2 1" fill="freeze"/></rect></clipPath>')
    x, segs, legend = bx, [], []
    for i, (name, size) in enumerate(top):
        colour = LANG_COLOURS[i] if i < len(LANG_COLOURS) else "mute"
        colour = t.get(colour, colour)
        w = bw * size / total
        segs.append(f'<rect x="{f(x)}" y="{by}" width="{f(w + 0.5)}" height="16" fill="{colour}"/>')
        x += w
        lx, ly = bx + (i % 2) * 240, by + 50 + (i // 2) * 30
        legend.append(f'<circle cx="{lx + 6}" cy="{ly - 5}" r="6" fill="{colour}"/>'
                      f'<text x="{lx + 22}" y="{ly}" font-family="{MONO}" font-size="14" fill="{t["ink"]}">{name}</text>'
                      f'<text x="{lx + 210}" y="{ly}" text-anchor="end" font-family="{MONO}" font-size="14" fill="{t["mute"]}">{100 * size / total:.1f}%</text>')
    nl = "\n"
    alt = ", ".join(f"{n} {100 * s / total:.0f}%" for n, s in top)
    return f'''{svg_open(W, H, "GitHub at a glance", "; ".join(f"{b} {s}" for b, s in facts) + ". Languages: " + alt)}
<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>
<line x1="290" y1="36" x2="290" y2="{H - 36}" stroke="{t["mute"]}" stroke-opacity=".3"/>
{nl.join(parts)}
<g clip-path="url(#bar)">{"".join(segs)}</g>
{nl.join(legend)}
</svg>
'''


def placeholder(t):
    W, H = 840, 120
    return f'''{svg_open(W, H, "GitHub at a glance", "This card is generated by the Profile stats workflow.")}
<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>
<text x="40" y="54" font-family="{SERIF}" font-size="24" font-weight="600" fill="{t["ink"]}">GitHub at a glance</text>
<text x="40" y="84" font-family="{MONO}" font-size="14" fill="{t["mute"]}">Run the "Profile stats" workflow once to fill this card with live data.</text>
</svg>
'''


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    os.makedirs(OUT, exist_ok=True)
    if "--placeholder" in sys.argv:
        for name, theme in THEMES.items():
            open(os.path.join(OUT, f"stats-{name}.svg"), "w").write(placeholder(theme))
        sys.exit(0)
    user = args[0] if args else os.environ.get("GITHUB_REPOSITORY_OWNER", "faaiz09")
    data = fetch(user)
    print(json.dumps({k: v for k, v in data.items() if k != "langs"}), sorted(data["langs"].items(), key=lambda kv: -kv[1])[:8])
    for name, theme in THEMES.items():
        open(os.path.join(OUT, f"stats-{name}.svg"), "w").write(render(data, theme))
