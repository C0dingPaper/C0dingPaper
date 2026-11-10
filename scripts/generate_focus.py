#!/usr/bin/env python3
"""Regenerate static, animated-in-viewer SVG focus charts; stdlib only."""
from pathlib import Path
import json, math, html
ROOT = Path(__file__).resolve().parent.parent
items = json.loads((ROOT / 'focus.json').read_text())['areas']
if not items or any(not isinstance(i['weight'], (int, float)) or not 0 <= i['weight'] <= 10 for i in items):
    raise SystemExit('focus.json weights must be numbers between 0 and 10')
esc = lambda x: html.escape(str(x), quote=True)
style = '<style><![CDATA[.grow{animation:appear 1.8s ease-out both}@keyframes appear{from{opacity:.15}to{opacity:1}}@media(prefers-reduced-motion:reduce){*{animation:none!important}}]]></style>'
w, row_h = 1100, 55
height = 110 + row_h * len(items)
bars = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" role="img" aria-label="Editable learning emphasis chart">',style, f'<rect width="{w}" height="{height}" rx="18" fill="#0b0709"/>','<text x="45" y="54" fill="#ff4a61" font-size="29" font-family="monospace">LEARNING FOCUS / EDITABLE</text>']
for k,i in enumerate(items):
    y = 98 + k*row_h; percent = i['weight'] / 10
    bars += [f'<text x="48" y="{y+17}" fill="#f8dde0" font-size="19" font-family="monospace">{esc(i["name"])}</text>',f'<rect x="395" y="{y-2}" width="620" height="21" rx="5" fill="#32121a"/>',f'<rect class="grow" x="395" y="{y-2}" width="{620*percent:.1f}" height="21" rx="5" fill="#e32942"/>',f'<text x="1034" y="{y+16}" fill="#f07585" font-size="17" font-family="monospace">{i["weight"]}/10</text>']
bars += [f'<text x="48" y="{height-18}" fill="#b88c93" font-size="15" font-family="monospace">Self-edited priorities, not certified skill scores</text>','</svg>']
(ROOT / 'assets' / 'focus-bars.svg').write_text(''.join(bars))
# Radar intentionally describes focus weights, never proficiency.
cx, cy, R, n = 550, 320, 210, len(items)
ang = lambda i: -math.pi/2 + 2*math.pi*i/n
point = lambda i,r: (cx + math.cos(ang(i))*r, cy + math.sin(ang(i))*r)
polygon = lambda r: ' '.join(f'{point(i,r)[0]:.1f},{point(i,r)[1]:.1f}' for i in range(n))
radar=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="660" viewBox="0 0 1100 660" role="img" aria-label="Learning focus radar diagram">',style,'<rect width="1100" height="660" rx="18" fill="#0b0709"/>','<text x="35" y="52" font-size="28" font-family="monospace" fill="#ff4a61">LEARNING FOCUS / RADAR</text>']
for j in (1,2,3,4): radar.append(f'<polygon points="{polygon(R*j/4)}" fill="none" stroke="#63313b" stroke-width="2"/>')
for i,x in enumerate(items):
    px,py=point(i,R); lx,ly=point(i,R+68)
    radar.extend([f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="#63313b"/>',f'<text x="{lx:.1f}" y="{ly:.1f}" fill="#f2cbd0" text-anchor="middle" font-family="monospace" font-size="17">{esc(x["name"])}</text>'])
points=' '.join(f'{point(i,R*x["weight"]/10)[0]:.1f},{point(i,R*x["weight"]/10)[1]:.1f}' for i,x in enumerate(items))
radar.extend([f'<polygon class="grow" points="{points}" fill="#e32942" fill-opacity=".26" stroke="#ff4a61" stroke-width="4"/>','<text x="550" y="624" font-size="17" fill="#b88c93" text-anchor="middle" font-family="monospace">Editable learning emphasis, not certified skill scores</text>','</svg>'])
(ROOT / 'assets' / 'focus-radar.svg').write_text(''.join(radar))
print('Updated focus-bars.svg and focus-radar.svg')
