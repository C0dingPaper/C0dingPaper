#!/usr/bin/env python3
# Generate locally-hosted GitHub SVG statistics without third-party image services.
import json
import os
from pathlib import Path
from collections import Counter
from urllib.request import Request, urlopen
from urllib.parse import urlencode

USER = "C0dingPaper"
API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)


def get(path, params=None):
    url = API + path + ("?" + urlencode(params) if params else "")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "sharingan-profile-analytics"}
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN
    with urlopen(Request(url, headers=headers), timeout=20) as response:
        return json.load(response)


def esc(s):
    from html import escape
    return escape(str(s), quote=True)


def frame(inner, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="290" viewBox="0 0 600 290" role="img" aria-label="{esc(title)}">
    <rect width="600" height="290" rx="18" fill="#090709"/>
    <rect x="2" y="2" width="596" height="286" rx="16" fill="none" stroke="#8e1829" stroke-width="2"/>
    <circle cx="560" cy="40" r="24" fill="none" stroke="#ec233b" stroke-width="3" opacity=".65"/>
    <circle cx="560" cy="40" r="9" fill="#a11828"/>
    <text x="30" y="47" font-family="monospace" font-size="24" fill="#ff5369" font-weight="bold">{esc(title)}</text>
    <line x1="30" y1="66" x2="570" y2="66" stroke="#592029"/>
    {inner}
    </svg>'''


def item(y, label, value):
    return f'<text x="36" y="{y}" font-size="20" fill="#d9a3aa" font-family="monospace">{esc(label)}</text><text x="555" y="{y}" font-size="23" font-weight="bold" text-anchor="end" fill="#ff4056" font-family="monospace">{esc(value)}</text>'


profile = get('/users/' + USER)
repos = []
page = 1
while True:
    batch = get('/users/' + USER + '/repos', {'per_page': 100, 'page': page, 'type': 'owner', 'sort': 'updated'})
    repos.extend(r for r in batch if not r.get('fork') and not r.get('private'))
    if len(batch) < 100 or page >= 15:
        break
    page += 1

stars = sum(int(r.get('stargazers_count') or 0) for r in repos)
forks = sum(int(r.get('forks_count') or 0) for r in repos)
body = item(105, 'Public original repositories', len(repos)) + item(147,'Stars earned',stars) + item(189,'Forks',forks) + item(231,'Followers',profile.get('followers',0))
(OUT/'github-stats.svg').write_text(frame(body,'GITHUB // METRICS'), encoding='utf-8')

langs = Counter(r['language'] for r in repos if r.get('language'))
total = sum(langs.values())
body = '<text x="36" y="94" fill="#d9a3aa" font-size="16" font-family="monospace">Top primary languages (repository count)</text>'
for i,(lang,count) in enumerate(langs.most_common(4)):
    y=130+i*39
    body += f'<text x="36" y="{y}" fill="#f0bac1" font-size="18" font-family="monospace">{esc(lang)}</text>'
    body += f'<rect x="230" y="{y-17}" width="265" height="14" rx="7" fill="#321219"/>'
    body += f'<rect x="230" y="{y-17}" width="{round(265*count/max(total,1))}" height="14" rx="7" fill="#ef3047"/>'
    body += f'<text x="554" y="{y}" text-anchor="end" fill="#ff586d" font-size="16" font-family="monospace">{count}</text>'
if not langs:
    body += '<text x="36" y="160" fill="#bd7f88" font-size="20" font-family="monospace">No language data yet</text>'
(OUT/'github-languages.svg').write_text(frame(body,'GITHUB // LANGUAGES'), encoding='utf-8')
print(f"Generated stats for {USER}: {len(repos)} public original repositories")
