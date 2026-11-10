#!/usr/bin/env python3
from pathlib import Path
import json, math, html

ROOT = Path(__file__).resolve().parent.parent
items = json.loads((ROOT / 'focus.json').read_text())['areas']
if not items or any(not isinstance(i['weight'], (int, float)) or not 0 <= i['weight'] <= 10 for i in items):
    raise SystemExit('focus.json weights must be numbers between 0 and 10')

esc = lambda x: html.escape(str(x), quote=True)
font_css = 'Helvetica, Arial, sans-serif'
style = (
    '<style><![CDATA['
    f'.label{{font-family:{font_css};fill:#f6d9de}}'
    f'.sub{{font-family:{font_css};fill:#c9a1a7}}'
    f'.title{{font-family:{font_css};fill:#ff445e;font-weight:700;letter-spacing:1px}}'
    f'.value{{font-family:{font_css};fill:#ff9eab;font-weight:700}}'
    '.grid{stroke:#6b2732;stroke-width:1.5;fill:none}'
    '.axis{stroke:#6b2732;stroke-width:1.5}'
    '.poly{fill:#ff314e;fill-opacity:.22;stroke:#ff4f66;stroke-width:3}'
    '.barbg{fill:#351019}'
    '.barfg{fill:#f02b45}'
    '.grow{animation:appear 1.2s ease-out both}'
    '@keyframes appear{from{opacity:.18;transform:scaleX(.25)}to{opacity:1;transform:scaleX(1)}}'
    '@media(prefers-reduced-motion:reduce){*{animation:none!important}}'
    ']]></style>'
)

# bar chart
w, h = 860, 380
left_x, bar_x, bar_w = 36, 290, 470
row_top, row_h = 90, 44
bars = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Editable learning focus bars">',
    style,
    f'<rect width="{w}" height="{h}" rx="18" fill="#0b0709"/>',
    '<text x="36" y="44" font-size="18" class="title">LEARNING FOCUS / EDITABLE</text>'
]
for idx, item in enumerate(items):
    y = row_top + idx * row_h
    val = item['weight']
    bars.extend([
        f'<text x="{left_x}" y="{y}" font-size="14.5" class="label">{esc(item["name"])}</text>',
        f'<rect x="{bar_x}" y="{y-14}" width="{bar_w}" height="16" rx="6" class="barbg"/>',
        f'<rect x="{bar_x}" y="{y-14}" width="{bar_w*val/10:.1f}" height="16" rx="6" class="barfg grow" style="transform-origin:{bar_x}px {y}px"/>',
        f'<text x="{bar_x + bar_w + 18}" y="{y}" font-size="13.5" class="value">{val}/10</text>'
    ])
bars.append(f'<text x="36" y="{h-18}" font-size="13.5" class="sub">Editable learning priorities, not certified skill scores</text>')
bars.append('</svg>')
(ROOT / 'assets' / 'focus-bars.svg').write_text(''.join(bars))

# radar
rw, rh = 620, 380
cx, cy, R = 310, 192, 108
n = len(items)
ang = lambda i: -math.pi/2 + 2*math.pi*i/n
point = lambda i,r: (cx + math.cos(ang(i))*r, cy + math.sin(ang(i))*r)
def polygon(r):
    return ' '.join(f'{point(i, r)[0]:.1f},{point(i, r)[1]:.1f}' for i in range(n))

radar = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {rw} {rh}" width="{rw}" height="{rh}" role="img" aria-label="Learning focus radar">',
    style,
    f'<rect width="{rw}" height="{rh}" rx="18" fill="#0b0709"/>',
    '<text x="24" y="44" font-size="18" class="title">LEARNING FOCUS / RADAR</text>'
]
for j in (1,2,3,4,5):
    radar.append(f'<polygon points="{polygon(R*j/5)}" class="grid"/>')
for i, item in enumerate(items):
    px, py = point(i, R)
    lx, ly = point(i, R + 32)
    if i == 0:
        ly -= 4
    if i == 1:
        lx += 8
    if i == 2:
        lx += 12; ly += 6
    if i == 3:
        ly += 16
    if i == 4:
        lx -= 18; ly += 5
    if i == 5:
        lx -= 8
    anchor = 'middle'
    if lx < 120:
        anchor = 'start'
    elif lx > rw - 120:
        anchor = 'end'
    radar.extend([
        f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" class="axis"/>',
        f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="13.5" text-anchor="{anchor}" class="label">{esc(item["name"])}</text>'
    ])
pts = ' '.join(f'{point(i, R*item["weight"]/10)[0]:.1f},{point(i, R*item["weight"]/10)[1]:.1f}' for i, item in enumerate(items))
radar.extend([
    f'<polygon points="{pts}" class="poly grow" style="transform-origin:{cx}px {cy}px"/>',
    f'<text x="{rw/2}" y="{rh-18}" font-size="12.8" text-anchor="middle" class="sub">Editable learning emphasis, not certified skill scores</text>',
    '</svg>'
])
(ROOT / 'assets' / 'focus-radar.svg').write_text(''.join(radar))
print('Updated focus SVGs')
