#!/usr/bin/env python3
"""Villa Gooch / The Lantern House: build the schematic design drawing set as one SVG per ARCH D sheet.

Usage: python3 build_set.py <svg_out_dir>
"""
import math
import os
import sys

from model import (EXT_OPS, DOORS, ROOMS, FINISHES, FINISH_KEY, ZONE_COLORS, LV, LOT_W, LOT_D, HOUSE_AT, ELEV)
from svgkit import Svg, PT, INK, SOFT, BRONZE, fi, drawing_title, north_arrow, scale_bar, tag, para, wrap
import plans
from plans import floor_plan, roof_plan, site_plan, level_areas
from elev import Elev, KEYNOTES, extents, section_a, section_b, sect_datums
from interiors import INTERIORS, parapet_detail, terrace_detail, wall_section

OUT = sys.argv[1] if len(sys.argv) > 1 else 'svg'
os.makedirs(OUT, exist_ok=True)

PROJECT = 'VILLA GOOCH'
CONCEPT = 'THE LANTERN HOUSE'
ADDRESS = '2316 GOOCH STREET · DALLAS, TEXAS 75241'
ISSUE = 'SCHEMATIC DESIGN'
DATE = '10.21.2026'

SHEETS = [
    ('A0.0', 'COVER SHEET'),
    ('A0.1', 'DESIGN NARRATIVE & MATERIALS'),
    ('A1.0', 'ARCHITECTURAL SITE PLAN'),
    ('A2.1', 'LEVEL 1 FLOOR PLAN'),
    ('A2.2', 'LEVEL 2 FLOOR PLAN'),
    ('A2.3', 'LEVEL 3 FLOOR PLAN'),
    ('A2.4', 'ROOF PLAN'),
    ('A3.1', 'FRONT & REAR ELEVATIONS'),
    ('A3.2', 'SIDE ELEVATIONS'),
    ('A4.1', 'BUILDING SECTIONS'),
    ('A5.1', 'SCHEDULES & AREAS'),
]

AREAS = level_areas()
TOTAL = AREAS['L1'] + AREAS['L2'] + AREAS['L3']
PV_KW = len(plans.pv_modules()) * 0.40
GLASS_FT = sum(o['b'] - o['a'] for o in EXT_OPS if o['lvl'] == 1 and o['typ'] == 'slider' and o['c'] == 54)


def sf(v):
    return f'{int(round(v)):,} SF'


# ------------------------------------------------------------ sheet frame
def frame(num, title, scale=''):
    svg = Svg(num.replace('.', '_') + '_')
    svg.rect(40, 40, 3520, 2320, stroke=INK, sw=2.4)
    x0, x1 = 3250, 3560
    svg.line(x0, 40, x0, 2360, sw=1.6)
    svg.text(x0 + 20, 100, PROJECT, size=30, weight=800, ls=3)
    svg.text(x0 + 20, 124, CONCEPT, size=9.5, weight=600, ls=2.6, fill=BRONZE)
    svg.text(x0 + 20, 150, '2316 GOOCH STREET', size=9, ls=0.8)
    svg.text(x0 + 20, 164, 'DALLAS, TEXAS 75241', size=9, ls=0.8)
    svg.text(x0 + 20, 178, 'ALAMEDA HEIGHTS · DALLAS COUNTY', size=7.5, fill='#666', ls=0.6)
    svg.line(x0, 200, x1, 200, sw=1)
    y = 225
    for lab, val in (('OWNER', ''), ('ARCHITECT OF RECORD', ''), ('STRUCTURAL ENGINEER', ''), ('MEP ENGINEER', '')):
        svg.text(x0 + 20, y, lab, size=7, fill='#666', ls=0.8)
        svg.line(x0 + 20, y + 20, x1 - 20, y + 20, sw=0.5, c='#999')
        y += 42
    svg.line(x0, y, x1, y, sw=1)
    svg.rect(x0 + 18, y + 18, x1 - x0 - 36, 120, fill='#f7f2ea', stroke=BRONZE, sw=1)
    svg.text((x0 + x1) / 2, y + 46, ISSUE.upper(), size=12, weight=800, anchor='middle', ls=1.5, fill=BRONZE)
    svg.text((x0 + x1) / 2, y + 66, 'NOT FOR CONSTRUCTION', size=9, weight=700, anchor='middle', ls=1.2)
    for i, ln in enumerate(wrap('Developed from listing photos and walkthrough video. Verify survey, zoning, '
                               'geotechnical report and all dimensions before design development.', 46)):
        svg.text((x0 + x1) / 2, y + 86 + i * 11, ln, size=6.8, anchor='middle', fill='#555')
    y += 160
    svg.line(x0, y, x1, y, sw=1)
    svg.text(x0 + 20, y + 22, 'REVISIONS', size=8, weight=700, ls=1)
    svg.text(x0 + 20, y + 42, 'NO.', size=6.5, fill='#666')
    svg.text(x0 + 52, y + 42, 'DATE', size=6.5, fill='#666')
    svg.text(x0 + 130, y + 42, 'DESCRIPTION', size=6.5, fill='#666')
    svg.line(x0 + 18, y + 48, x1 - 18, y + 48, sw=0.5, c='#999')
    svg.text(x0 + 24, y + 64, '0', size=7.5)
    svg.text(x0 + 52, y + 64, DATE, size=7.5)
    svg.text(x0 + 130, y + 64, 'SCHEMATIC DESIGN ISSUE', size=7.5)
    for k in range(1, 6):
        svg.line(x0 + 18, y + 48 + k * 24, x1 - 18, y + 48 + k * 24, sw=0.4, c='#ccc')
    y += 200
    svg.line(x0, y, x1, y, sw=1)
    for i, (lab, val) in enumerate((('PROJECT NO.', '2316-GS'), ('ISSUE DATE', DATE), ('SCALE', scale or 'AS NOTED'),
                                    ('DRAWING SET', 'ARCH D · 36" x 24"'))):
        yy = y + 24 + i * 34
        svg.text(x0 + 20, yy, lab, size=6.8, fill='#666', ls=0.8)
        svg.text(x0 + 20, yy + 14, val, size=9, weight=600)
    y = 2360 - 330
    svg.line(x0, y, x1, y, sw=1)
    svg.text(x0 + 20, y + 30, 'SHEET TITLE', size=7, fill='#666', ls=1)
    for i, ln in enumerate(wrap(title, 20)):
        svg.text(x0 + 20, y + 60 + i * 24, ln, size=19, weight=800, ls=0.8)
    svg.line(x0, 2360 - 160, x1, 2360 - 160, sw=1)
    svg.text(x0 + 20, 2360 - 132, 'SHEET', size=7, fill='#666', ls=1)
    svg.text((x0 + x1) / 2, 2360 - 40, num, size=78, weight=800, anchor='middle', ls=1)
    return svg


def save(svg, idx, num):
    with open(os.path.join(OUT, f'{idx:02d}_{num}.svg'), 'w') as f:
        f.write(svg.render())


def heading(svg, x, y, text, size=13, color=INK, rule=None):
    svg.text(x, y, text, size=size, weight=800, ls=1.6, fill=color)
    if rule:
        svg.line(x, y + 8, x + rule, y + 8, sw=1.2, c=color)
    return y + size + 14


def bullets(svg, x, y, items, size=9.2, width=78, gap=5, lead=1.42):
    for it in items:
        svg.circle(x + 3, y - size * 0.33, 2.2, fill=BRONZE)
        lines = wrap(it, width)
        for i, ln in enumerate(lines):
            svg.text(x + 14, y + i * size * lead, ln, size=size)
        y += len(lines) * size * lead + gap
    return y


def table(svg, x, y, cols, rows, title=None, rh=20, size=8, head='#efe8dc'):
    if title:
        svg.text(x, y - 12, title, size=12, weight=800, ls=1.4)
    total = sum(w for _, w in cols)
    svg.rect(x, y, total, rh, fill=head)
    cx = x
    for h, w in cols:
        svg.text(cx + 6, y + rh * 0.66, h, size=size - 0.6, weight=700, ls=0.5)
        cx += w
    for i, row in enumerate(rows):
        ry = y + rh * (i + 1)
        if i % 2:
            svg.rect(x, ry, total, rh, fill='#faf8f4')
        cx = x
        for (h, w), val in zip(cols, row):
            s = str(val)
            maxc = int((w - 10) / (size * 0.56))
            if len(s) > maxc:
                s = s[:maxc - 1] + '…'
            bold = 700 if cx == x else 400
            svg.text(cx + 6, ry + rh * 0.66, s, size=size, weight=bold)
            cx += w
        svg.line(x, ry + rh, x + total, ry + rh, sw=0.3, c='#c9c2b6')
    cx = x
    for _, w in cols[:-1]:
        cx += w
        svg.line(cx, y, cx, y + rh * (len(rows) + 1), sw=0.4, c='#c9c2b6')
    svg.rect(x, y, total, rh * (len(rows) + 1), stroke=INK, sw=1)
    svg.line(x, y + rh, x + total, y + rh, sw=0.9)
    return y + rh * (len(rows) + 1)


# ------------------------------------------------------------ swatches
def swatch(svg, x, y, w, h, kind):
    fills = {'stone': '#e6dece', 'wood': '#b98a5c', 'bronze': '#3c3530', 'glass': '#9fb3c1', 'oak': '#cfae84',
             'porcelain': '#ddd5c7', 'slab': '#f3f0ea', 'plaster': '#d8cfc2'}
    svg.rect(x, y, w, h, fill=fills[kind])
    cid = svg.clip_rect(x, y, w, h)
    svg.g(f'clip-path="url(#{cid})"')
    if kind == 'stone':
        for j in range(0, int(h), 40):
            svg.line(x, y + j, x + w, y + j, sw=0.8, c='#cfc4b2')
            off = 40 if (j // 40) % 2 else 0
            for i in range(-40 + off, int(w), 80):
                svg.line(x + i, y + j, x + i, y + j + 40, sw=0.8, c='#cfc4b2')
        for k in range(60):
            svg.circle(x + (k * 37) % w, y + (k * 53) % h, 0.9, fill='#d6ccba')
    elif kind in ('wood', 'oak'):
        step = 9 if kind == 'wood' else 26
        for i in range(0, int(w), step):
            svg.line(x + i, y, x + i, y + h, sw=0.7, c='#9d7149' if kind == 'wood' else '#b8946a')
        for k in range(14):
            yy = y + (k * 29) % h
            svg.path(f'M {x} {yy} q {w / 3} 6 {w / 1.5} 0 t {w / 1.5} 0', stroke='#a8805a' if kind == 'oak' else '#8a6440',
                     sw=0.5, op=0.6)
    elif kind == 'bronze':
        for i in range(0, int(w), 30):
            svg.line(x + i, y, x + i, y + h, sw=0.8, c='#2a2420')
        svg.rect(x, y, w, h * 0.35, fill='#ffffff', op=0.05)
    elif kind == 'glass':
        g = svg.lin_grad([(0, '#c9d5dd', None), (1, '#5a6c7c', None)])
        svg.rect(x, y, w, h, fill=f'url(#{g})')
        svg.poly([(x + w * 0.2, y), (x + w * 0.45, y), (x + w * 0.1, y + h), (x - w * 0.15, y + h)], fill='#fff', op=0.2)
    elif kind == 'porcelain':
        svg.line(x + w / 2, y, x + w / 2, y + h, sw=0.8, c='#c9bfae')
        svg.line(x, y + h / 2, x + w, y + h / 2, sw=0.8, c='#c9bfae')
    elif kind == 'slab':
        for k in range(5):
            svg.path(f'M {x - 10} {y + 20 + k * 30} C {x + w * 0.3} {y + k * 30 - 10}, {x + w * 0.6} {y + 40 + k * 30}, '
                     f'{x + w + 10} {y + 10 + k * 30}', stroke='#b9b3aa', sw=1.1 - k * 0.12, op=0.8)
    elif kind == 'plaster':
        for k in range(40):
            svg.ellipse(x + (k * 41) % w, y + (k * 67) % h, 14, 5, fill='#e2dbcf', op=0.6)
    svg.end()
    svg.rect(x, y, w, h, stroke='#8c857a', sw=0.8)


# ------------------------------------------------------------ trees
def palm(svg, x, base, s, h=26, lean=1.2, c='#2a3324', op=1.0):
    top = (x + lean * s, base - h * s)
    svg.path(f'M {x - 0.45 * s} {base} Q {x + lean * 0.2 * s} {base - h * 0.5 * s} {top[0] - 0.25 * s} {top[1]} '
             f'L {top[0] + 0.25 * s} {top[1]} Q {x + lean * 0.3 * s} {base - h * 0.5 * s} {x + 0.45 * s} {base} Z',
             fill=c, op=op)
    for k in range(15):
        a = math.radians(-190 + k * 14 + (4 if k % 2 else 0))
        L = (5.5 + (k % 3) * 0.9) * s
        droop = 2.4 * s if abs(math.cos(a)) > 0.55 else 0.6 * s
        ex, ey = top[0] + L * math.cos(a), top[1] + L * math.sin(a) * 0.5 + droop
        mx, my = top[0] + L * 0.55 * math.cos(a), top[1] - 1.6 * s + L * 0.5 * math.sin(a) * 0.5
        svg.path(f'M {top[0]:.1f} {top[1]:.1f} Q {mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}', stroke=c, sw=0.32 * s, cap='round',
                 op=op)


def round_tree(svg, x, base, s, h=22, r=8, c='#33402c', op=0.95):
    svg.rect(x - 0.4 * s, base - h * 0.55 * s, 0.8 * s, h * 0.55 * s, fill='#3b2f25', op=op)
    for dx, dy, rr in ((0, -h + r * 0.9, r), (-r * 0.6, -h + r * 1.4, r * 0.7), (r * 0.65, -h + r * 1.5, r * 0.65)):
        svg.circle(x + dx * s, base + dy * s, rr * s, fill=c, op=op)


def shrubs(svg, x0, x1, base, s, c='#3e4a33'):
    x = x0
    k = 0
    while x < x1:
        r = (1.0 + (k % 3) * 0.35) * s
        svg.ellipse(x, base - r * 0.6, r * 1.3, r * 0.75, fill=c)
        x += 2.4 * s
        k += 1


# ============================================================ sheets
def sheet_cover():
    svg = frame('A0.0', 'COVER SHEET', 'NTS')
    dusk_panel(svg, 'front', 60, 60, 2440, 1640, 37.5, 1500, 'DUSK STREET ELEVATION · GOOCH STREET · ILLUSTRATIVE')
    svg.text(70, 1780, PROJECT, size=104, weight=800, ls=14)
    svg.text(76, 1838, CONCEPT + '  —  A CONTEMPORARY LUXURY VILLA', size=24, weight=600, ls=5, fill=BRONZE)
    svg.text(76, 1880, ADDRESS, size=16, weight=500, ls=3)
    para(svg, 76, 1940,
         'A complete redesign of the 3-story spec house at 2316 Gooch Street. The glass stair tower that defined the '
         'original becomes a bronze-framed lantern; around it, a warm limestone base, a thermally-modified wood crown and '
         'a floating bronze roof plate. Seven bedroom suites, an elevator, a chef\'s kitchen with scullery, a 50-foot '
         'pool loggia, pool and spa, and a top-floor primary retreat with its own terrace.', size=12.5, width_chars=150,
         lead=1.5, fill='#333')
    cols = [('', 300), ('EXISTING (MLS 21372838)', 400), ('PROPOSED', 520)]
    rows = [('Conditioned area', '3,257 SF', f'{TOTAL:,.0f} SF'),
            ('Bedrooms / baths', '7 BR / 4 full + 1 half', '7 BR / 7 full + 1 half · every bedroom en suite'),
            ('Stories', '3', '3 + 37-ft glass stair lantern'),
            ('Vertical circulation', 'Stair', 'Floating stair, glass bridge, 3-stop elevator'),
            ('Outdoor living', 'Covered balcony', 'Loggia, pool, spa, 4 terraces, green roof'),
            ('Garage', '2-car', '2-car, EV charging, storage, mudroom entry')]
    table(svg, 76, 2085, cols, rows, title='EXISTING vs. PROPOSED', rh=30, size=11)
    fx = 1360
    y = heading(svg, fx, 1712, 'SIGNATURE FEATURES', rule=1070)
    feats = [
        '37-ft bronze-framed glass lantern: floating lit-tread stair, glass bridge, cascading chandelier',
        '3-stop residential elevator serving every level',
        'Chef\'s kitchen: 12-ft waterfall island, 48" range, scullery and walk-in pantry',
        f'{GLASS_FT:.0f} ft of pocketing lift-slide glass in four bays to a covered loggia with outdoor kitchen',
        'Heated salt pool with sun shelf, raised spillover spa and electric fire lounge',
        'Seven bedroom suites, each with its own bath and closet',
        'Level 3 primary retreat: electric fireplace, island dressing room, spa bath, 400 SF terrace',
        'Family lounge with 198-bottle backlit wine wall; climate-controlled wine room under the stair',
        'Office behind a wood-fin screen and linear reflecting pool',
        f'All-electric: ±{PV_KW:.1f} kW solar, 27 kWh battery, heat pumps, ERV, EV charging',
    ]
    bullets(svg, fx, y + 8, feats[:5], size=11, width=48, gap=9)
    bullets(svg, fx + 545, y + 8, feats[5:], size=11, width=48, gap=9)
    x = 2490
    y = heading(svg, x, 110, 'SHEET INDEX', rule=700)
    for num_, t in SHEETS:
        svg.text(x, y + 8, num_, size=11.5, weight=700)
        svg.text(x + 90, y + 8, t, size=11.5)
        svg.line(x, y + 16, x + 700, y + 16, sw=0.4, c='#ccc')
        y += 34
    y += 40
    y = heading(svg, x, y, 'PROJECT DATA', rule=700)
    data = [('Address', '2316 Gooch St, Dallas TX 75241'), ('Subdivision', 'Alameda Heights'),
            ('Lot (assumed)', "60' x 145' = 8,700 SF (0.20 AC)"), ('Zoning', 'R-7.5(A) assumed — verify'),
            ('Code basis', 'IRC 2021 w/ Dallas amendments'), ('Construction', 'Type V-B · NFPA 13D sprinklers throughout'),
            ('Stories / height', "3 stories · 35'-2\" parapet · 37'-8\" lantern (avg. grade)"),
            ('Footprint', '2,700 SF + 600 SF loggia'), ('Lot coverage', f'{(2700 + 600) / 8700 * 100:.1f}%'),
            ('School district', 'Dallas ISD')]
    for k, v in data:
        svg.text(x, y + 8, k.upper(), size=8.5, weight=700, fill='#555', ls=0.6)
        svg.text(x + 230, y + 8, v, size=11)
        y += 30
    y += 30
    y = heading(svg, x, y, 'AREA SUMMARY', rule=700)
    for k, v in (('Level 1 — arrival & living', AREAS['L1']), ('Level 2 — family & suites', AREAS['L2']),
                 ('Level 3 — primary retreat', AREAS['L3'])):
        svg.text(x, y + 8, k, size=11)
        svg.text(x + 700, y + 8, sf(v), size=11, anchor='end', weight=600)
        y += 28
    svg.line(x, y - 6, x + 700, y - 6, sw=1)
    svg.text(x, y + 14, 'TOTAL CONDITIONED', size=12, weight=800)
    svg.text(x + 700, y + 14, sf(TOTAL), size=12, anchor='end', weight=800)
    y += 40
    for k, v in (('Garage', AREAS['garage']), ('Covered loggia', AREAS['loggia']),
                 ('Balconies & terraces', AREAS['balcony'] + AREAS['l2terrace'] + AREAS['l3front'] + AREAS['primaryterrace'])):
        svg.text(x, y + 8, k, size=10.5, fill='#444')
        svg.text(x + 700, y + 8, sf(v), size=10.5, anchor='end', fill='#444')
        y += 26
    y += 30
    y = heading(svg, x, y, 'KEY ASSUMPTIONS', rule=700)
    bullets(svg, x, y + 6, [
        'Lot size and setbacks are assumed from the listing (0.2 AC). A boundary and topographic survey is required.',
        'True north is not confirmed; drawings use plan north (street at bottom).',
        'Building height exceeds the 30\'-0" R-7.5(A) limit; confirm the site\'s actual zoning district or seek relief.',
        'Expansive black clay is noted in the listing; foundation to follow a geotechnical report.',
    ], size=10, width=62)
    save(svg, 0, 'A0.0')


def mini_elev(svg, left, base, s, hl, title, sub):
    e = Elev(svg, 'front', left, base, s, hl=hl, interior=False)
    e.draw()
    svg.line(e.X(-3), e.Z(-0.67), e.X(53), e.Z(-0.67), sw=1.6)
    svg.text(left, base + 40, title, size=12, weight=800, ls=1.4)
    for i, ln in enumerate(wrap(sub, 62)):
        svg.text(left, base + 58 + i * 13, ln, size=9, fill='#444')


def sheet_concept():
    svg = frame('A0.1', 'DESIGN NARRATIVE & MATERIALS', 'NTS')
    x = 80
    y = heading(svg, x, 110, 'DESIGN NARRATIVE', size=16, rule=1020)
    y = para(svg, x, y + 4,
             'The house on Gooch Street already had one great idea: a tall glass stair tower glowing at night. The redesign '
             'keeps that DNA and refines everything around it into a calm, contemporary villa organised around three '
             'materials and one sequence of space.', size=11.5, width_chars=150, fill='#222')
    y += 12
    principles = [
        ('THE LANTERN', 'A 37-foot bronze-framed glass volume holds the floating stair, a glass bridge, the cascading '
                        'chandelier and a 3-stop elevator beside it. It is the house\'s front door, its beacon at dusk and '
                        'the vertical spine connecting every level.'),
        ('STONE BASE · WOOD CROWN', 'Warm limestone sintered-stone panels wrap Levels 1-2; thermally-modified ash wraps the '
                                    'set-back Level 3; a thin bronze roof plate floats above with LED-lit wood soffits.'),
        ('INDOOR-OUTDOOR LIVING', f'{GLASS_FT:.0f} feet of pocketing lift-slide glass in four bays open the great room to a 50 x 12 ft loggia with '
                                  'outdoor kitchen, then pool, spa, lawn and an electric fire lounge.'),
        ('EVERY BEDROOM A SUITE', 'Seven bedrooms, each with a private bath. Four Level 2 suites open to a planted rear '
                                  'terrace; Level 3 holds the primary retreat with dressing room, spa bath and 400 SF terrace.'),
        ('FUNCTION FIRST', 'Garage to mudroom to scullery to kitchen; laundry on the bedroom level; kids\' study; wine room '
                           'under the stair; powder room off the gallery, not the foyer; mechanical room with roof access.'),
        ('BUILT FOR DALLAS', 'Deep overhangs and recessed glass, low-E glazing, all-electric heat pumps, ERV, roof PV, '
                             'green roof and a post-tensioned slab on drilled piers for expansive clay.'),
    ]
    for i, (h, t) in enumerate(principles):
        cx = x + (i % 2) * 520
        cy = y + (i // 2) * 120
        svg.text(cx, cy + 16, f'0{i + 1}', size=22, weight=800, fill=BRONZE)
        svg.text(cx + 44, cy + 12, h, size=11, weight=800, ls=1.2)
        for j, ln in enumerate(wrap(t, 64)):
            svg.text(cx + 44, cy + 30 + j * 13.5, ln, size=9.3, fill='#333')
    y += 3 * 120 + 10
    y = heading(svg, x, y + 10, 'DESIGN MOVES — STREET ELEVATION', size=13, rule=1020)
    moves = [
        (lambda it: it.get('grp') == 'base' and it.get('mat') == 'stone', '1  STONE BASE',
         'Levels 1-2 in warm limestone panels; recessed glass behind stone cheek walls.'),
        (lambda it: it.get('grp') in ('crown', 'fins') or (it.get('mat') == 'wood'), '2  WOOD CROWN',
         'Set-back Level 3 and recessed walls in thermally-modified ash; wood fins screen the office.'),
        (lambda it: it.get('grp') == 'lantern' or it.get('typ') in ('cw', 'pivot'), '3  BRONZE LANTERN',
         'Triple-height glass stair hall framed in dark bronze; pivot door under a blade canopy.'),
        (lambda it: it.get('grp') == 'roof' or it.get('n') == 'lanternHead', '4  FLOATING ROOF',
         'A thin bronze roof plate cantilevers over the terraces; LED coves wash the wood soffits.'),
    ]
    for i, (hl, t, sub) in enumerate(moves):
        mini_elev(svg, x + 10 + (i % 2) * 520, y + 350 + (i // 2) * 470, 9.0, hl, t, sub)
    y += 350 + 470 + 110
    y = heading(svg, x, y + 10, 'WHAT WE KEPT · WHAT WE CHANGED', size=13, rule=1020)
    bullets(svg, x, y + 6, [
        'KEPT — the glass stair tower, the cascading chandelier, lit stair treads, glass-railed balconies with stained wood '
        'soffits, front-facing glass garage door, palm-tree front yard and the 7-bedroom count.',
        'CHANGED — all-black stucco becomes a warmer stone / wood / bronze palette; the stair tower gains a bronze frame, a '
        'pivot door and a canopy; every bedroom gets its own bath; an elevator, pool loggia, pool and spa are added; the '
        'primary suite moves to the top floor with a private terrace and spa bath; laundry moves to the bedroom level.',
    ], size=9.8, width=140, gap=8)
    # program stacking
    X0 = 1180
    y2 = heading(svg, X0, 110, 'PROGRAM STACKING', size=16, rule=1000)
    titles = {1: 'LEVEL 1 · ARRIVAL & LIVING', 2: 'LEVEL 2 · FAMILY & SUITES', 3: 'LEVEL 3 · PRIMARY RETREAT'}
    for i, lvl in enumerate((1, 2, 3)):
        T = PT(X0 + 40 + i * 340, y2 + 440, 6.0)
        for r in ROOMS[lvl]:
            x0_, y0_, x1_, y1_ = r['rect']
            T.rect(svg, x0_, y0_, x1_, y1_, fill=ZONE_COLORS[r['zone']][0], stroke='#fff', sw=1.2)
        T.rect(svg, 0, 0, 14, 24, fill='none', stroke=BRONZE, sw=2.2)
        T.rect(svg, 0, 0, 50, 54, fill='none', stroke=INK, sw=1.4)
        svg.text(T.x(0), T.y(-5), titles[lvl], size=9.5, weight=800, ls=0.8)
        svg.text(T.x(0), T.y(-8.2), f'{sf(AREAS["L" + str(lvl)])} CONDITIONED', size=8, fill='#555')
    ly = y2 + 510
    for k, (key, (col, lab)) in enumerate(ZONE_COLORS.items()):
        lx = X0 + 40 + (k % 4) * 250
        yy = ly + (k // 4) * 24
        svg.rect(lx, yy - 11, 16, 14, fill=col, stroke='#888', sw=0.5)
        svg.text(lx + 24, yy, lab, size=9)
    my = heading(svg, X0, ly + 90, 'MATERIAL PALETTE', size=16, rule=1000)
    mats = [('stone', 'M1', 'SINTERED STONE', 'Warm limestone finish, 10\'x5\' panels'),
            ('wood', 'M2', 'THERMO-ASH CLADDING', 'Vertical shiplap, natural oil'),
            ('bronze', 'M3', 'DARK BRONZE ALUMINUM', 'Lantern frame, fascia, window frames'),
            ('glass', 'G1', 'LOW-IRON LOW-E GLASS', 'Curtain wall, lift-slides, guards'),
            ('oak', 'F1', 'WHITE OAK FLOORING', '10" plank, matte natural oil'),
            ('porcelain', 'F2', 'LIMESTONE PORCELAIN', '48" x 48", foyer / kitchen / mud'),
            ('slab', 'T1', 'BOOK-MATCHED SLAB', 'Fireplaces, baths, kitchen backsplash'),
            ('plaster', 'P2', 'VENETIAN PLASTER', 'Lantern & lounge feature walls')]
    for i, (kind, code, name, desc) in enumerate(mats):
        mx = X0 + (i % 4) * 252
        yy = my + (i // 4) * 215
        swatch(svg, mx, yy, 225, 130, kind)
        tag(svg, mx + 20, yy + 20, code, shape='box', size=8, r=11)
        svg.text(mx, yy + 152, name, size=10, weight=800, ls=0.8)
        svg.text(mx, yy + 168, desc, size=8.5, fill='#444')
    sx = 2250
    yy = heading(svg, sx, 110, 'SYSTEMS & SUSTAINABILITY', size=16, rule=950)
    yy = bullets(svg, sx, yy + 6, [
        'STRUCTURE — post-tensioned slab on drilled piers (expansive clay), wood platform framing, steel moment frames '
        'at the lantern and long-span glass openings, open-web floor trusses for MEP routing.',
        'ENVELOPE — ventilated rainscreen; R-23 cavity + R-7.5 continuous mineral wool; R-49 roof with tapered insulation; '
        'thermally broken bronze frames with low-E, argon-filled insulated glass.',
        'HVAC — three variable-speed heat pumps, one per level: AHU-1 in the garage mech closet, AHU-2 in the Level 2 '
        'mech/linen closet, AHU-3 in the Level 3 mech room; ERV for fresh air, dehumidification, MERV-13 filtration.',
        f'POWER — all-electric house, no gas service: ±{PV_KW:.1f} kW rooftop PV; 2 x 13.5 kWh UL 9540 batteries and '
        'inverter on the garage wall behind bollards (IRC R328); EV charger; smart panel. Fireplaces and fire table '
        'are electric (no combustion).',
        'WATER — heat-pump water heater with recirculation; drip irrigation; downspouts to rain gardens; salt pool with '
        'heat-pump heater and automatic safety cover.',
        'LIFE SAFETY — NFPA 13D sprinklers throughout, including the lantern, garage and covered terraces; hard-wired, '
        'interconnected smoke/CO alarms (lantern included) and a garage heat detector; casement escape windows in '
        'Bedrooms 2, 5 and 7; terrace-level rescue openings elsewhere subject to AHJ approval (R104.11).',
        'SMART HOME — lighting control with scene presets, motorized shades in the lantern, integrated AV and security.',
    ], size=9.8, width=168, gap=8)
    yy = heading(svg, sx, yy + 34, 'PROGRAM BY LEVEL', size=16, rule=950)
    program = [
        ('LEVEL 1 · ARRIVAL & LIVING', 'Foyer & stair lantern, office, powder & dry bar, living, dining for 10, chef\'s '
                                       'kitchen, scullery & pantry, mudroom, wine room, 2-car garage, covered loggia with '
                                       'outdoor kitchen.'),
        ('LEVEL 2 · FAMILY & SUITES', 'Glass bridge, family lounge & wine bar, kids\' study, laundry, linen, Bedrooms 2-5 '
                                      'each with bath and walk-in closet, covered front balcony, rear terrace, green roof.'),
        ('LEVEL 3 · PRIMARY RETREAT', 'Primary bedroom with fireplace & morning bar, island dressing room, spa bath, '
                                      'Bedrooms 6-7 with baths, mechanical / storage, front terraces, primary terrace.'),
        ('GARDEN', 'Heated pool with sun shelf, raised spa, electric fire lounge, lawn, reflecting pool at the entry.'),
    ]
    for h, t in program:
        svg.text(sx, yy + 4, h, size=10, weight=800, ls=0.8, fill=BRONZE)
        for j, ln in enumerate(wrap(t, 170)):
            svg.text(sx, yy + 20 + j * 13.5, ln, size=9.8, fill='#333')
        yy += 20 + len(wrap(t, 170)) * 13.5 + 16
    dusk_panel(svg, 'rear', 1180, 1300, 3200, 2330, 20, 2120, 'DUSK GARDEN ELEVATION · POOL & LOGGIA · ILLUSTRATIVE')
    save(svg, 1, 'A0.1')


PLAN_T = PT(457, 1800, 25)
LEVEL_TITLES = {1: 'LEVEL 1 · ARRIVAL & LIVING', 2: 'LEVEL 2 · FAMILY & SUITES', 3: 'LEVEL 3 · PRIMARY RETREAT'}
LEVEL_NOTES = {
    1: ['Pivot door opens into the triple-height glass lantern: floating stair, chandelier and a straight view through '
        'the great room to the pool.',
        'Office behind a wood-fin screen and reflecting pool; glass wall to the foyer.',
        'Great room 50 ft wide: living with electric linear fireplace, dining for 10, chef\'s kitchen with 12-ft waterfall '
        'island.',
        'Service spine: garage > mudroom lockers > scullery & walk-in pantry > kitchen. Groceries never cross the living room.',
        'Powder room and dry bar sit off a side gallery, not the front door.',
        '50 x 12 ft covered loggia with outdoor kitchen and electric fire table; four bays of pocketing lift-slide doors aligned '
        'under the Level 2 suites.',
        'Climate-controlled wine room under the stair: 1/2" gypsum on the enclosed side of walls and stair soffit (R302.7).'],
    2: ['Glass bridge crosses the lantern beside the chandelier; stacked flights continue to Level 3.',
        'Family lounge with game table, electric fireplace and backlit wine bar opens to the covered front balcony.',
        'Four bedroom suites (Bedrooms 2-5), each with private bath, walk-in closet and lift-slide door to the rear terrace.',
        'Rear terrace on the loggia roof, divided by wood privacy fins, bordered by a sedum green roof.',
        'Laundry with folding counter and kids\' study on the bedroom level; mech / linen closet (AHU-2) at the hall end.'],
    3: ['Primary retreat: 22 x 17 ft bedroom with electric fireplace and morning bar, dressing room with island, spa bath with '
        'freestanding tub, rain shower and private WC.',
        '400 SF primary terrace under a cantilevered roof, with outdoor shower and planters.',
        'Bedrooms 6 and 7 each with en-suite bath, walk-through closet and a private front terrace.',
        'Mechanical / storage room with air handler, heat-pump water heater and roof hatch.'],
}


def plan_sheet(lvl, idx):
    num_ = f'A2.{lvl}'
    svg = frame(num_, f'LEVEL {lvl} FLOOR PLAN', 'AS NOTED')
    T = PLAN_T
    floor_plan(svg, T, lvl)
    drawing_title(svg, 120, 2240, '1', f'LEVEL {lvl} FLOOR PLAN', 'SCALE: 1/4" = 1\'-0"', width=520)
    scale_bar(svg, 700, 2232, 25, feet=(0, 2, 4, 8, 16))
    north_arrow(svg, 1640, 2205, r=34)
    px = 1990
    y = heading(svg, px, 110, LEVEL_TITLES[lvl], size=16, rule=1230)
    y = bullets(svg, px, y + 6, LEVEL_NOTES[lvl], size=10, width=150, gap=5)
    rows = []
    for r in ROOMS[lvl]:
        x0, y0, x1, y1 = r['rect']
        area = (x1 - x0) * (y1 - y0)
        if r['fin'] != 'elev':
            ex0, ey0, ex1, ey1 = ELEV
            area -= max(0, min(x1, ex1) - max(x0, ex0)) * max(0, min(y1, ey1) - max(y0, ey0))
        rows.append((r['num'], r['name'].title().replace('Wic', 'WIC'), f'{fi(x1 - x0)} x {fi(y1 - y0)}',
                     f'{area:,.0f} SF' if r['area'] != 0 else 'EXTERIOR', FINISHES[r['fin']][0]))
    y = table(svg, px, y + 40, [('NO.', 80), ('ROOM', 330), ('APPROX. SIZE', 250), ('AREA (NET)', 180),
                                 ('FLOOR', 110)], rows, title='ROOM SCHEDULE', rh=20, size=8.6)
    svg.text(px, y + 18, f'LEVEL {lvl} GROSS CONDITIONED AREA: {sf(AREAS["L" + str(lvl)])}  ·  TOTAL HOUSE: {sf(TOTAL)}',
             size=10, weight=700)
    ly = heading(svg, px, y + 62, 'LEGEND', size=12, rule=1230)
    items = [('ext', 'EXTERIOR WALL — 2x6 STUD + RAINSCREEN CLADDING'), ('int', 'INTERIOR PARTITION'),
             ('glass', 'GLASS PARTITION / CURTAIN WALL'), ('guard', 'FRAMELESS GLASS GUARD 42" A.F.F.')]
    for i, (k, lab) in enumerate(items):
        yy = ly + i * 22
        if k == 'ext':
            svg.rect(px, yy - 10, 60, 12, fill=plans.POCHE_EXT)
        elif k == 'int':
            svg.rect(px, yy - 8, 60, 8, fill=plans.POCHE_INT)
        elif k == 'glass':
            svg.rect(px, yy - 8, 60, 6, fill=plans.GLASS_FILL, stroke=INK, sw=0.6)
        else:
            svg.rect(px, yy - 7, 60, 4, fill='#fff', stroke='#444', sw=0.6)
        svg.text(px + 76, yy, lab, size=8.8)
    lx2 = px + 620
    tag(svg, lx2 + 12, ly - 4, 'W01', shape='hex', size=6.2, r=10.5)
    svg.text(lx2 + 36, ly, 'WINDOW / GLAZED DOOR TAG — SEE A5.1', size=8.8)
    tag(svg, lx2 + 12, ly + 18, 'D01', shape='circle', size=6.2, r=10.5)
    svg.text(lx2 + 36, ly + 22, 'DOOR TAG — SEE A5.1', size=8.8)
    svg.circle(lx2 + 12, ly + 41, 10, fill='#fff', stroke=INK, sw=1)
    svg.line(lx2 + 2, ly + 41, lx2 + 22, ly + 41, sw=0.7)
    svg.text(lx2 + 36, ly + 45, 'SECTION / ELEVATION REFERENCE', size=8.8)
    svg.line(lx2, ly + 64, lx2 + 24, ly + 64, sw=0.6, dash='6 4')
    svg.text(lx2 + 36, ly + 68, 'OVERHEAD / ABOVE, OR HIGH WINDOW', size=8.8)
    lx3 = px + 900
    for i, (k, lab) in enumerate((('SD', 'SMOKE ALARM, INTERCONNECTED (R314)'), ('CO', 'CARBON MONOXIDE ALARM (R315)'),
                                  ('HD', 'HEAT DETECTOR, INTERCONNECTED (R328.7)'), ('EF', 'EXHAUST FAN TO EXTERIOR (R303.3)'))):
        yy = ly - 4 + i * 22
        if k == 'EF':
            svg.rect(lx3 + 2, yy - 10, 20, 20, fill='#fff', stroke=INK, sw=0.7)
            svg.text(lx3 + 12, yy + 3.5, k, size=7, weight=700, anchor='middle')
        else:
            svg.circle(lx3 + 12, yy, 11, fill='#fff', stroke='#b24a3a', sw=0.9)
            svg.text(lx3 + 12, yy + 3.5, k, size=7, weight=700, anchor='middle', fill='#b24a3a')
        svg.text(lx3 + 34, yy + 4, lab, size=8.8)
    ny = heading(svg, px, ly + 104, 'GENERAL NOTES', size=12, rule=1230)
    ny = bullets(svg, px, ny + 4, [
        'Dimensions to exterior face of sheathing and centerline of partitions. Ceilings 10\'-0" typ.; baths/closets 9\'-0".',
        'Stair: 18 risers @ 7-5/16", 17 treads @ 11", 3\'-8" clear, lit treads; continuous handrail at 36" on the wall '
        'side; 42" glass guards on open sides.',
        'Elevator: ASME A17.1 §5.3 residential, 3 stops, 3\'-0" entrance. Garage separation: 5/8" Type X, 20-min door.',
        'Egress: casement escape windows in Bedrooms 2, 5 and 7; every bedroom also opens to a balcony or terrace '
        '(terrace-level rescue openings subject to AHJ approval). NFPA 13D sprinklers throughout.',
        'Smoke alarms ≥ 3\'-0" from bath doors; windowless baths and WCs exhausted to exterior, 50 cfm intermittent '
        'or 20 cfm continuous. Under-stair wine room lined with 1/2" gypsum (R302.7).',
    ], size=9.2, width=160, gap=4)
    top = max(ny + 60, 1090)
    first, second = INTERIORS[lvl]
    if isinstance(first, tuple):
        e1 = first[0](svg, px, top)
        first[1](svg, px + e1.width + 70, top)
    else:
        first(svg, px, top)
    second(svg, px, top + 570)
    save(svg, idx, num_)


def roof_sheet(idx):
    svg = frame('A2.4', 'ROOF PLAN', 'AS NOTED')
    T = PLAN_T
    n_mod = roof_plan(svg, T)
    plans.dim_h(svg, T, [0, 14, 27, 36, 50], -6.75, ext_from=-1.6)
    plans.dim_h(svg, T, [0, 50], -8.5)
    plans.dim_v(svg, T, [0, 24, 46, 50, 54, 66], -5.5, ext_from=-1.5)
    plans.dim_v(svg, T, [0, 66], -8.5)
    plans.grid(svg, T, -12.2, -12.2, 66, 50)
    drawing_title(svg, 120, 2240, '1', 'ROOF PLAN', 'SCALE: 1/4" = 1\'-0"', width=520)
    scale_bar(svg, 700, 2232, 25, feet=(0, 2, 4, 8, 16))
    north_arrow(svg, 1640, 2205, r=34)
    px = 1990
    y = heading(svg, px, 110, 'ROOF STRATEGY', size=16, rule=1230)
    kw = n_mod * 0.40
    y = bullets(svg, px, y + 6, [
        'Main roof: single-ply PVC (white, SRI ≥ 100) over tapered polyiso to two internal drains (RD-1, RD-2), '
        '1/4" per foot minimum, each paired with a separate overflow drain (OD-1, OD-2) piped to daylight at grade; '
        'no exposed downspouts. Lantern roof drains through RD-3 / OD-3 in its solid side wall.',
        f'Photovoltaic array: {n_mod} modules x ±400 W = ±{kw:.1f} kW DC on ballasted racking, set back 3\'-0" from '
        'parapets for access; battery and inverter in the garage.',
        'Heat-pump condensers (one per level) on vibration-isolated rails behind a 42" bronze louver screen; refrigerant '
        'lines drop through the mechanical room.',
        'Roof hatch (30" x 36") with ship ladder and fall-protection rail from the Level 3 mechanical room.',
        'Lantern roof raised to +37\'-0" with a structural-glass skylight over the chandelier void (laminated, PVB '
        'interlayer ≥ 0.030", R308.6; U ≤ 0.55); motorized shade. Fritted linear skylight over the Level 3 hall.',
        'Terraces over conditioned space: porcelain pavers on pedestals over hot-applied waterproofing and tapered '
        'insulation; Level 2 terrace on the loggia roof with an extensive sedum green roof beyond.',
        'Parapet 1\'-6" above roof deck (no roof occupancy); 42" guards at all accessible terraces.',
    ], size=10, width=150, gap=6)
    rows = [('Lantern roof / parapet', "+36'-6\" / +37'-0\"", 'PVC, laminated glass skylight, U ≤ 0.55'),
            ('Main roof / parapet', "+33'-0\" / +34'-6\"", 'PVC, PV array, equipment'),
            ('Level 3 terraces', "+22'-0\"", 'Pavers on pedestals'),
            ('Level 2 terrace', "+11'-0\"", 'Pavers on pedestals'),
            ('Green roof (loggia)', "+11'-0\"", 'Sedum trays, gravel edge'),
            ('Entry canopy', "+10'-0\"", 'Bronze blade, integral drain')]
    y = table(svg, px, y + 40, [('ROOF AREA', 420), ('ELEVATION', 300), ('ASSEMBLY', 510)], rows, title='ROOF LEVELS',
              rh=24, size=9.5)
    top = y + 110
    parapet_detail(svg, px + 40, top)
    drawing_title(svg, px, top + 480, '2', 'PARAPET & ROOF EDGE DETAIL', 'SCALE: 1" = 1\'-0"', width=560)
    top2 = top + 700
    terrace_detail(svg, px + 40, top2)
    drawing_title(svg, px, top2 + 480, '3', 'TERRACE EDGE & GLASS GUARD DETAIL', 'SCALE: 1" = 1\'-0"', width=560)
    save(svg, idx, 'A2.4')


def site_sheet(idx):
    svg = frame('A1.0', 'ARCHITECTURAL SITE PLAN', 'AS NOTED')
    T = PT(400, 2000, 12.5)
    site_plan(svg, T)
    drawing_title(svg, 150, 2312, '1', 'ARCHITECTURAL SITE PLAN', 'SCALE: 1/8" = 1\'-0"', width=520)
    scale_bar(svg, 730, 2304, 12.5, feet=(0, 4, 8, 16, 32))
    north_arrow(svg, 1300, 1900, r=40)
    px = 1450
    y = heading(svg, px, 110, 'SITE DATA', size=16, rule=1750)
    hx, hy = HOUSE_AT
    rows = [('Address', '2316 Gooch Street, Dallas, TX 75241 (Dallas County)'),
            ('Legal / subdivision', 'Alameda Heights — lot & block per survey'),
            ('Lot area', '8,700 SF (0.20 AC) — 60\'-0" x 145\'-0" ASSUMED'),
            ('Zoning', 'R-7.5(A) single family ASSUMED — verify with City of Dallas'),
            ('Setbacks (assumed)', 'Front 25\'-0"  ·  Side 5\'-0"  ·  Rear 5\'-0"'),
            ('Provided', f'Front {hy:.0f}\'-0" to facade ({hy - 5:.0f}\'-0" to canopy)  ·  Sides 5\'-0"  ·  Rear {145 - hy - 66:.0f}\'-0" to loggia'),
            ('Building footprint', '2,700 SF enclosed + 600 SF covered loggia = 3,300 SF'),
            ('Lot coverage', f'{3300 / 8700 * 100:.1f}% (45% max typical — verify)'),
            ('Building height', '3 stories · 35\'-2" T.O. parapet · 37\'-8" T.O. lantern above avg. grade (-0\'-8"); '
             'rooftop equipment screen 37\'-2" — verify permitted projections'),
            ('Parking', '2 enclosed (garage) + 2 on driveway'),
            ('Utilities', 'City water & sewer, electric — all-electric house, no gas service'),
            ('Soils', 'Expansive black clay (per listing) — geotechnical report required')]
    y = table(svg, px, y + 20, [('ITEM', 330), ('DATA', 1420)], rows, rh=24, size=9.6)
    y = heading(svg, px, y + 60, 'SITE & LANDSCAPE DESIGN', size=16, rule=1750)
    y = bullets(svg, px, y + 6, [
        'Arrival: a 4\'-0" porcelain walk runs from the driveway along the reflecting pool to the pivot door under the '
        'bronze canopy; offset stepping pads cross the front lawn from the public sidewalk.',
        'The specimen Sabal palm (existing) is relocated as the centerpiece of the front lawn; low agave, muhly grass and '
        'boxwood beds line the facade with integrated uplights.',
        'Driveway: 20\'-0" concrete with stone bands; new curb cut and apron to City standards; EV-ready garage.',
        'Rear garden: covered loggia steps down to a porcelain pool deck, 30\' x 14\' heated salt pool with sun shelf, raised '
        '8\' x 8\' spillover spa, lawn and a circular fire lounge.',
        'Privacy: 8\'-0" cedar fence on side and rear property lines (verify height limits), smooth face and rails on '
        'the pool side so it cannot be climbed from outside the barrier; evergreen holly screen along the rear.',
        'Pool barrier gates at both side yards open away from the pool, self-closing and self-latching, latch release '
        '≥ 54" above grade (ISPSC 305.3); barrier ≥ 48", ≤ 2" clear at grade; power safety cover on pool and spa.',
        'Service: 2\'-0" bins pad against the fence keeps a 36" clear egress path and a 3\'x3\' landing at the garage '
        'side door; pool equipment screened at the rear right; outdoor shower by the loggia. '
        'Drainage: 5% slope for 10\'-0" away from the house; downspouts to rain gardens.',
    ], size=10, width=170, gap=5)
    y = heading(svg, px, y + 24, 'LEGEND', size=12, rule=1750)
    leg = [('#bfdbe8', 'Pool / spa / reflecting pool'), ('#e2ecd2', 'Lawn & planting'), ('#eceae5', 'Concrete paving'),
           ('#f3f0e9', 'Porcelain pavers'), ('#d9d3c8', 'Building footprint / roof'), ('#ece9e1', 'Gravel side yards')]
    for i, (c, lab) in enumerate(leg):
        lx = px + (i % 3) * 420
        yy = y + (i // 3) * 26
        svg.rect(lx, yy - 12, 30, 16, fill=c, stroke='#888', sw=0.5)
        svg.text(lx + 40, yy, lab, size=9.5)
    yy = y + 64
    svg.line(px, yy, px + 40, yy, sw=1.6, dash='26 6 4 6')
    svg.text(px + 50, yy + 4, 'PROPERTY LINE', size=9.5)
    svg.line(px + 420, yy, px + 460, yy, sw=0.8, c='#b24a3a', dash='10 4')
    svg.text(px + 470, yy + 4, 'BUILDING SETBACK (ASSUMED)', size=9.5)
    svg.line(px + 840, yy, px + 880, yy, sw=2.2, c='#7a5b3a')
    svg.text(px + 890, yy + 4, '8\'-0" CEDAR FENCE / GATE', size=9.5)
    svg.text(px + 1260, yy + 4, 'WM water meter · EM electric meter · CO cleanout', size=9.5, fill='#444')
    s = 9.375
    base = 1700
    site_section(svg, 1500 + 46 * s, base, s)
    svg.text(1500, base + 168, 'Fire separation: side walls are 5\'-0" to sheathing and about 4\'-8" to the cladding '
             'face; with NFPA 13D throughout, Table R302.1(2) applies (no rating at FSD ≥ 3\'-0").', size=9.4, fill='#444')
    drawing_title(svg, 1500, base + 120, '2', 'SITE SECTION — GOOCH STREET TO REAR FENCE', 'SCALE: 3/32" = 1\'-0"',
                  width=700)
    save(svg, idx, 'A1.0')


def elev_sheet(idx, num_, title, views):
    svg = frame(num_, title, '1/4" = 1\'-0"')
    s = 25
    kn = {
        'front': [(40, 0, 9.0, 1), (38, 6, 16, 2), (0.6, -1.5, 30, 3), (7, 0, 28, 4), (26, 6, 13, 5), (30, 0.25, 12.6, 6),
                  (7, 0, 5, 7), (38.5, 0, 4, 8), (20.5, -0.7, 6, 9), (10.6, -5, 11.2, 10), (44, 0, 21.5, 1),
                  (30, 0, 33.9, 3), (49.4, 0, 27, 1)],
        'rear': [(25, 66, 5, 13), (40, 65.5, 11.35, 12), (8, 54, 5, 5), (20, 60, 13.2, 6), (49.6, 54, 16, 1),
                 (36.25, 46, 27, 2), (20, 50, 33.9, 3), (7, 46, 30, 14), (12.5, 59.5, 15.6, 15)],
        'left': [(0, 12, 6, 3), (0, 21.5, 30, 4), (0, 40, 5, 1), (0, 47, 17.5, 14), (0, 35, 26, 2), (0, 65.7, 5, 13),
                 (0, 50, 24.2, 6), (0, 30, 33.9, 3), (0, 12, 26, 17)],
        'right': [(50, 40, 5, 1), (50, 11.5, 17, 14), (50, 30, 26, 2), (14, 10, 36, 3), (50, 65.7, 5, 13),
                  (50, 50, 24.2, 6), (50, 17.0, 3.5, 16), (50, 3, 16, 1)],
    }
    names = {'front': 'FRONT ELEVATION — GOOCH STREET', 'rear': 'REAR ELEVATION — GARDEN',
             'left': 'LEFT SIDE ELEVATION', 'right': 'RIGHT SIDE ELEVATION'}
    for i, (v, base) in enumerate(views):
        e = Elev(svg, v, 230, base, s)
        e.draw()
        e.grade(extend=3)
        e.datums(right_pad=4.0)
        for x, y, z, n in kn[v]:
            e.keynote(x, y, z, n)
        drawing_title(svg, 230, base + 82, str(i + 1), names[v], 'SCALE: 1/4" = 1\'-0"', width=560)
    px = 2080 if views[0][0] in ('front', 'rear') else 2480
    w = 3200 - px
    y = heading(svg, px, 110, 'KEYNOTES', size=16, rule=w)
    for n, t in KEYNOTES:
        tag(svg, px + 12, y - 4, str(n), shape='hex', size=8, r=10.5)
        lines = wrap(t, int((w - 40) / 5.3))
        for j, ln in enumerate(lines):
            svg.text(px + 34, y + j * 13, ln, size=9.3)
        y += 13 * len(lines) + 14
    y = heading(svg, px, y + 20, 'ELEVATION NOTES', size=12, rule=w)
    y = bullets(svg, px, y + 4, [
        'Shadows are cast at 45° for depth reading only; true solar orientation to be confirmed by survey.',
        'Stone panels 10\'-0" x 5\'-0" in stack bond, joints at mid-storey and at slab bands; 1/4" open joints, black EPDM backer.',
        'All glazing low-E, argon filled; low-iron glass at the lantern curtain wall and guards.',
        'Exterior lighting: 2700K, full cutoff, dark-sky compliant; LED coves at all wood soffits.',
        'Parapet tops capped in bronze. No exposed downspouts: roof and overflow drains are internal leaders to grade.',
        'Side walls: no projections (copings, conductor heads, meters, line sets) beyond the wall face within 5\'-0" of '
        'the side lot lines.',
    ], size=9.2, width=int((w - 20) / 5.1), gap=5)
    y = heading(svg, px, y + 30, 'EXTERIOR MATERIALS', size=12, rule=w)
    sw_ = (w - 3 * 20) / 4
    for i, (kind, code, name) in enumerate((('stone', 'M1', 'SINTERED STONE'), ('wood', 'M2', 'THERMO-ASH'),
                                             ('bronze', 'M3', 'DARK BRONZE'), ('glass', 'G1', 'LOW-IRON GLASS'))):
        mx = px + i * (sw_ + 20)
        swatch(svg, mx, y + 4, sw_, sw_ * 0.6, kind)
        tag(svg, mx + 20, y + 24, code, shape='box', size=8, r=11)
        svg.text(mx, y + 24 + sw_ * 0.6, name, size=9.5, weight=800, ls=0.6)
    if views[0][0] == 'front':
        regulating_lines(svg, px + 30, 2120)
    else:
        wall_section(svg, px + 190, 2160)
        drawing_title(svg, px, 2240, '3', 'TYPICAL WALL SECTION — RIGHT SIDE', 'SCALE: 3/8" = 1\'-0"', width=w - 20)
    save(svg, idx, num_)


def regulating_lines(svg, left, base):
    """Front elevation reduced, with the head lines and the shared mullion grid that order the street face."""
    s = 18.75
    e = Elev(svg, 'front', left, base, s, interior=False, shadows=False)
    e.draw()
    e.grade(extend=2)
    red = '#b24a3a'
    for z, lab in ((10, "HEAD / SPANDREL +10'-0\""), (21, "HEAD / SPANDREL +21'-0\""), (31, "HEAD +31'-0\""),
                   (33.25, "ROOF PLATE +33'-3\"")):
        svg.line(e.X(-1.5), e.Z(z), e.X(51.5), e.Z(z), sw=0.9, c=red, dash='10 4')
        svg.text(e.X(51.8), e.Z(z) + 3, lab, size=7.6, weight=700, fill=red)
    for x in (14, 20.67, 26.33, 32, 38, 43.25, 48.5):
        svg.line(e.X(x), e.Z(-1.6), e.X(x), e.Z(36), sw=0.7, c=red, dash='3 3')
    svg.text(e.X(14), e.Z(-1.6) + 14, 'SHARED MULLION GRID, LEVELS 2-3', size=7.6, weight=700, fill=red)
    for z0, z1 in ((0, 10), (11, 21), (22, 31)):
        y = (e.Z(z0) + e.Z(z1)) / 2
        svg.text(e.X(-2.2), y + 3, f'{fi(z1 - z0)} TO HEAD', size=7.6, anchor='end', fill=red)
    drawing_title(svg, left - 50, base + 82, '3', 'REGULATING LINES — STREET FACE', 'SCALE: 3/16" = 1\'-0"', width=560)
    return e


def section_sheet(idx):
    svg = frame('A4.1', 'BUILDING SECTIONS', '1/4" = 1\'-0"')
    s = 25
    X, Z = section_a(svg, 100, 1000, s)
    sect_datums(svg, X, Z, 92)
    drawing_title(svg, 120, 1225, 'A', 'LONGITUDINAL SECTION A — THROUGH LANTERN, LIVING & POOL',
                  'SCALE: 1/4" = 1\'-0"', width=860)
    X2, Z2 = section_b(svg, 100, 2160, s)
    sect_datums(svg, X2, Z2, 56, items=[(34.5, 'T.O. PARAPET', "+34'-6\""), (33, 'ROOF', "+33'-0\""),
                                        (22, 'LEVEL 3', "+22'-0\""), (11, 'LEVEL 2', "+11'-0\""),
                                        (0, 'LEVEL 1', "+0'-0\"")])
    drawing_title(svg, 120, 2290, 'B', 'TRANSVERSE SECTION B — GREAT ROOM, SUITES & PRIMARY', 'SCALE: 1/4" = 1\'-0"',
                  width=820)
    px = 2000
    y = heading(svg, px, 1380, 'TYPICAL ASSEMBLIES', size=14, rule=1180)
    bullets(svg, px, y + 4, [
        'ROOF: PVC membrane, 1/2" cover board, tapered polyiso R-49 min., vapor retarder, 3/4" sheathing on wood I-joists; '
        'gypsum ceiling. Parapet capped in bronze.',
        'EXTERIOR WALL: sintered stone or thermo-ash on aluminum rainscreen rails, 1-1/2" mineral wool c.i., WRB, '
        '1/2" sheathing, 2x6 studs @ 16" o.c. with R-23, 5/8" gypsum.',
        'FLOORS: 1/2" engineered oak (or porcelain), acoustic underlayment, 1-1/8" subfloor on 14" open-web trusses, '
        'R-19 sound batts, resilient channel, 5/8" gypsum.',
        'TERRACES OVER CONDITIONED SPACE: pavers on pedestals, drainage mat, hot-rubberized waterproofing, tapered XPS.',
        'FOUNDATION: post-tensioned slab on 15-mil vapor barrier, perimeter grade beams on drilled piers; final design '
        'per geotechnical report (expansive clay, PI > 40 anticipated). R-10 rigid slab-edge insulation, 2\'-0" deep '
        '(coordinate termite provisions, R318.4).',
        'LANTERN: steel moment frame, bronze-capped curtain wall with laminated low-iron IGUs, steel-plate glass bridge '
        'with 42" laminated glass guard.',
        'TRANSFERS: W-flange beam at grid 2 (Y 6\'-4") over the office and garage carries the Level 2-3 front walls; '
        'steel flush beams under the Level 2 party walls (X 12\'-6", 25\'-0", 37\'-6") bear on the rear piers between '
        'the lift-slide bays and on the service-core walls.',
        'PLUMBING: wet walls stack to chases — Bath 2 to the living media wall, Baths 3-4 to the mudroom wall, Bath 5 '
        'and the primary bath to the scullery, Bath 6 to the wine-bar wall, Bath 7 over the laundry.',
    ], size=9.4, width=150, gap=6)
    save(svg, idx, 'A4.1')


SAFETY_T = {'slider', 'pivot', 'garage'}


def safety_glazing(o):
    """R308.4 hazardous-location designation for a scheduled exterior opening."""
    if o['typ'] in SAFETY_T or o['lvl'] == 0 or o.get('room') in ('Lantern', 'Stair'):
        return 'T' if o['typ'] != 'slot' else 'L'
    ff = LV[o['lvl']]
    wet = any(k in (o.get('room') or '') for k in ('Bath', 'Spa', 'Shower', 'WC'))
    if o['z0'] - ff < 1.5 or wet:
        return 'T'
    return '—'


def schedules_sheet(idx):
    svg = frame('A5.1', 'SCHEDULES & AREAS', 'NTS')
    rows = []
    for o in EXT_OPS:
        if o['typ'] in ('pivot', 'garage', 'door'):
            kind = {'pivot': 'Pivot', 'garage': 'Overhead', 'door': 'Exterior swing'}[o['typ']]
            rows.append((o['mark'], 'L1', o['room'], kind, f'{fi(o["b"] - o["a"])} x {fi(o["z1"] - o["z0"])}',
                         o['desc']))
    for lvl in (1, 2, 3):
        for o in DOORS[lvl]:
            if not o.get('mark'):
                continue
            w, h = o['size']
            rows.append((o['mark'], f'L{lvl}', o['room'], o['kind'], f'{fi(w)} x {fi(h)}', o.get('note') or
                         {'swing': 'Solid-core, flush, paint-grade; concealed hinges', 'pocket': 'Solid-core pocket, soft-close',
                          'bifold': 'Rift oak bifold', 'elev': 'By elevator mfr.', 'double': 'Rift oak pair, 9\' tall'}
                         .get(o['typ'], '')))
    x = 70
    y = table(svg, x, 130, [('MARK', 70), ('LVL', 50), ('LOCATION', 210), ('TYPE', 230), ('SIZE W x H', 160),
                            ('NOTES', 360)], rows, title='DOOR SCHEDULE', rh=27, size=9.6)
    y += 60
    svg.text(x, y - 12, 'FINISH LEGEND', size=12, weight=800, ls=1.4)
    for code, desc in FINISH_KEY:
        svg.text(x, y + 8, code, size=10, weight=800)
        svg.text(x + 50, y + 8, desc, size=10)
        y += 23
    rows = []
    for o in EXT_OPS:
        if o['typ'] in ('pivot', 'garage', 'door'):
            continue
        ff = 0 if o['lvl'] == 0 else LV[o['lvl']]
        kind = {'slider': 'Lift-slide door', 'fixed': 'Fixed', 'win': 'Casement / awning', 'slot': 'Fixed slot'}[o['typ']]
        face = {'-y': 'FRONT', '+y': 'REAR', '-x': 'LEFT', '+x': 'RIGHT'}[o['n']]
        rows.append((o['mark'], 'ALL' if o['lvl'] == 0 else f'L{o["lvl"]}', face, o.get('room', 'Lantern'), kind,
                     f'{fi(o["b"] - o["a"])} x {fi(o["z1"] - o["z0"])}', fi(o['z0'] - ff), safety_glazing(o),
                     o['desc']))
    rows.append(('CW1', 'ALL', 'FRONT', 'Lantern', 'Curtain wall', "14'-0\" x 37'-0\"", '0"', 'L',
                 'Steel-backed bronze curtain wall, laminated low-iron IGUs; barrier at bridge'))
    x2 = 1200
    y2 = table(svg, x2, 130, [('MARK', 62), ('LVL', 46), ('ELEV.', 66), ('ROOM', 150), ('TYPE', 150), ('W x H', 140),
                              ('SILL', 66), ('SAF.', 50), ('NOTES', 316)], rows, title='WINDOW & GLAZED DOOR SCHEDULE',
               rh=27, size=9.2)
    y2 += 28
    svg.text(x2, y2, 'All units: thermally broken aluminum, dark bronze anodized; low-E argon IGU (U ≤ 0.30, SHGC ≤ 0.25);',
             size=9.4, fill='#444')
    svg.text(x2, y2 + 15, 'SAF.: T = tempered, L = laminated (R308.4); glass guards laminated (R308.4.4.1). Egress per R310.',
             size=9.4, fill='#444')
    y2 += 60
    rows = [('Level 1 — conditioned', sf(AREAS['L1'])), ('Level 2 — conditioned', sf(AREAS['L2'])),
            ('Level 3 — conditioned', sf(AREAS['L3'])), ('TOTAL CONDITIONED', sf(TOTAL)),
            ('Garage', sf(AREAS['garage'])), ('Covered loggia', sf(AREAS['loggia'])),
            ('Level 2 front balcony (covered)', sf(AREAS['balcony'])), ('Level 2 rear terrace', sf(AREAS['l2terrace'])),
            ('Green roof', sf(AREAS['green'])), ('Level 3 front terraces', sf(AREAS['l3front'])),
            ('Level 3 primary terrace', sf(AREAS['primaryterrace'])),
            ('Lot coverage (2,700 + 600 loggia / 8,700)', f'{3300 / 8700 * 100:.1f}%')]
    y2 = table(svg, x2, y2, [('AREA TABULATION', 640), ('AREA', 406)], rows, title='AREAS', rh=25, size=9.6)
    svg.text(x2, y2 + 20, 'Gross areas to exterior face of sheathing; open-to-below voids excluded; stair counted on each level it '
             'serves.', size=8.8, fill='#444')
    rows = []
    for lvl in (1, 2, 3):
        for r in ROOMS[lvl]:
            f = FINISHES[r['fin']]
            rows.append((r['num'], r['name'].title(), f[0], f[1], f[2], f[3], f[4]))
    x3 = 2300
    table(svg, x3, 130, [('NO.', 56), ('ROOM', 270), ('FLR', 60), ('BASE', 60), ('WALLS', 150), ('CLG', 90),
                         ('CLG HT', 114)], rows, title='ROOM FINISH SCHEDULE', rh=26, size=9.2)
    cy = max(y, y2 + 40) + 50
    code = [
        ('Emergency escape (R310)', '≥ 5.7 SF net, ≥ 24" clear H, ≥ 20" clear W, sill ≤ 44"; to yard/court ≥ 36" '
         'wide or public way', 'Casements BR 2, 5, 7; BR 3, 4, 6 & 308 via terraces — R104.11 alternate w/ 13D'),
        ('Handrails (R311.7.8)', '34"–38" high on at least one side of each flight', 'Continuous lit handrail at 36" '
         'on the wall side of every flight'),
        ('Stairs (R311.7)', 'Riser ≤ 7-3/4", tread ≥ 10", width ≥ 36", headroom ≥ 6\'-8"',
         '7-5/16" risers, 11" treads, 3\'-8" clear, ≥ 10\'-0" headroom'),
        ('Guards (R312)', '36" min (34" at stair from nosing); 4" sphere (4-3/8" stair sides)',
         '42" laminated glass guards at stair, bridge and terraces'),
        ('Garage separation (R302.6)', '1/2" gyp walls & supports; 5/8" Type X clg under habitable; ducts 26 ga',
         '5/8" Type X walls and ceiling; 20-min self-closing door; no duct openings in garage'),
        ('Fire separation distance (R302.1)', 'FSD < 5\'-0": 1-hr walls unless sprinklered (Table R302.1(2))',
         'FSD ≈ 4\'-8" to cladding; NFPA 13D → Table R302.1(2), no rating at FSD ≥ 3\'-0"'),
        ('Under-stair space (R302.7)', 'Enclosed accessible space: 1/2" gypsum on enclosed side',
         'Wine room walls and stair soffit 1/2" gypsum, oak / glass finish over'),
        ('Smoke & CO alarms (R314/R315)', 'Each bedroom, outside sleeping areas, each story; ≥ 3\' from bath doors',
         'Hard-wired, interconnected; SD in lantern; SD/CO in halls and at garage entry'),
        ('Bath exhaust (R303.3)', 'Windowless baths: 50 cfm intermittent / 20 cfm continuous',
         'EF ducted to exterior in Powder 105, Baths 211, 212, 303 and Primary WC'),
        ('Fire sprinklers (R313)', 'Per Dallas amendments', 'NFPA 13D throughout incl. lantern, garage, covered terraces'),
        ('Elevator (ASME A17.1 §5.3, R321)', 'Hoistway enclosed, interlocks, ≤ 4" door-to-car-gate space',
         '3 stops (L1-L3), 3\'-0" entrance, pit / overhead per mfr., dedicated circuit'),
        ('Safety glazing (R308)', 'Doors, wet areas, near stairs & landings, guards, skylights',
         'T / L per SAF. column; laminated guards, curtain wall and skylight'),
        ('Energy storage (R328)', 'Listed UL 9540, ≤ 20 kWh / unit, ≤ 80 kWh in garage; heat detector',
         '2 x 13.5 kWh units, interconnected HD, bollards (R328.8)'),
        ('Pool barrier (IRC R326 / ISPSC §305)', '48" barrier, gates open away from pool, self-closing & latching',
         'Gates swing away from pool; power safety cover on pool & spa; alarms on L1 lift-slides'),
        ('Energy (IECC 2021, zone 3A)', 'Clg R-49; wall R-20 or 13+5; slab R-10, 2\'; U ≤ 0.30, SHGC ≤ 0.25',
         'R-23 + R-7.5 c.i. walls, R-49 roof, R-10 slab edge; skylight U ≤ 0.55; ≤ 3.0 ACH50; R408 pkg'),
        ('Zoning height (assumed R-7.5(A))', '30\'-0" max., from grade', "35'-2\" / 37'-8\" above avg. grade — VERIFY DISTRICT; variance / SUP"),
        ('Lot coverage (assumed)', '45% maximum', f'{3300 / 8700 * 100:.1f}% provided'),
    ]
    table(svg, 70, cy, [('ITEM', 360), ('REQUIREMENT (VERIFY WITH CITY OF DALLAS)', 760), ('DESIGN RESPONSE', 1060)], code,
          title='CODE & ZONING CHECKLIST — IRC 2021 W/ DALLAS AMENDMENTS (PRELIMINARY)', rh=27, size=9.6)
    save(svg, idx, 'A5.1')


def dusk_panel(svg, view, x0, y0, x1, y1, s, grade_y, caption):
    """Illustrative dusk rendering of one elevation inside a clipped panel."""
    cid = svg.clip_rect(x0, y0, x1 - x0, y1 - y0)
    svg.g(f'clip-path="url(#{cid})"')
    sky = svg.lin_grad([(0, '#16213d', None), (0.45, '#33456f', None), (0.8, '#8a7d93', None), (1, '#d8a27a', None)])
    svg.rect(x0, y0, x1 - x0, grade_y - y0 + 2, fill=f'url(#{sky})')
    band = max(60, int((grade_y - y0) * 0.35))
    for k in range(44):
        svg.circle(x0 + (k * 157) % (x1 - x0), y0 + 18 + (k * 71) % band, 1.2 if k % 3 else 1.8, fill='#fff', op=0.6)
    umin, umax = extents(view)
    left = (x0 + x1) / 2 - (umax - umin) * s / 2
    e = Elev(svg, view, left, grade_y - 0.67 * s, s, mode='dusk')
    round_tree(svg, left - 6 * s, grade_y, s, h=24, r=6.5, c='#1c2533', op=0.8)
    round_tree(svg, left + e.width + 6 * s, grade_y, s, h=22, r=6.0, c='#1c2533', op=0.8)
    e.draw()
    svg.rect(x0, grade_y, x1 - x0, y1 - grade_y, fill='#1d2419')
    if view == 'front':
        svg.rect(x0, grade_y + 1.1 * s, x1 - x0, y1 - grade_y, fill='#27301f')
        dl, dr = e.X(29), e.X(47.5)
        svg.poly([(dl, grade_y), (dr, grade_y), (dr + 4.3 * s, y1), (dl - 1.6 * s, y1)], fill='#4b4945')
        wl, wr = e.X(5), e.X(9)
        for k in range(4):
            yy = grade_y + 0.3 * s + k * 0.8 * s
            svg.rect(wl - k * 0.37 * s, yy, (wr - wl) + k * 0.75 * s, 0.48 * s, fill='#5c5a55')
        svg.rect(e.X(15.2), grade_y + 0.16 * s, e.X(26) - e.X(15.2), 0.37 * s, fill='#e9b26f', op=0.55)
        shrubs(svg, e.X(-6), e.X(4.5), grade_y + 4, s * 0.8, c='#2e3a26')
        shrubs(svg, e.X(14), e.X(27), grade_y + 4, s * 0.55, c='#34412b')
        palm(svg, e.X(-4.5), grade_y + 8, s, h=27, lean=1.5, c='#101710')
        palm(svg, e.X(55.5), grade_y + 8, s, h=24, lean=-1.2, c='#101710')
    else:
        svg.rect(x0, grade_y, x1 - x0, 0.9 * s, fill='#4d4a45')
        water = svg.lin_grad([(0, '#8fe0ef', None), (1, '#1d6c88', None)])
        svg.rect(e.X(-35), grade_y + 0.9 * s, e.X(-5) - e.X(-35), 1.5 * s, fill=f'url(#{water})')
        svg.rect(x0, grade_y + 2.4 * s, x1 - x0, y1 - grade_y, fill='#27301f')
        svg.rect(e.X(-46), grade_y - 1.4 * s, e.X(-38) - e.X(-46), 2.3 * s, fill='#8f897f')
        svg.rect(e.X(-45.6), grade_y - 1.15 * s, e.X(-38.4) - e.X(-45.6), 0.3 * s, fill='#8fe0ef')
        for u in (-33.5, -29.0, -14.5, -10.0):
            svg.poly([(e.X(u), grade_y), (e.X(u + 3.2), grade_y), (e.X(u + 3.2), grade_y - 0.9 * s),
                      (e.X(u + 2.4), grade_y - 0.9 * s), (e.X(u + 1.6), grade_y - 0.5 * s), (e.X(u), grade_y - 0.5 * s)],
                     fill='#15130f')
        shrubs(svg, e.X(-50), e.X(-47), grade_y + 4, s * 0.8, c='#2e3a26')
        palm(svg, e.X(-55.5), grade_y + 8, s, h=24, lean=1.2, c='#101710')
        palm(svg, e.X(5.0), grade_y + 8, s, h=27, lean=-1.4, c='#101710')
    svg.end()
    svg.rect(x0, y0, x1 - x0, y1 - y0, stroke=INK, sw=1.2)
    svg.text(x0 + 30, y1 - 24, caption, size=10, weight=600, fill='#e8dcc8', ls=2)
    return e



def site_section(svg, left, base, s):
    """Street-to-fence site section built around Section A (house coordinates, u = Y)."""
    X = lambda u: left + (u + 6) * s  # noqa: E731
    Z = lambda z: base - z * s  # noqa: E731
    for a, b in ((-52, -6), (92, 118)):
        svg.rect(X(a), Z(-0.67), (b - a) * s, 5.33 * s, fill='#f1ede6')
    svg.rect(X(-52), Z(-1.1), 10 * s, 0.45 * s, fill='#8f8b84')
    svg.text(X(-47), Z(-3.2), 'GOOCH ST.', size=8, weight=700, anchor='middle', fill='#555')
    svg.rect(X(-42.4), Z(-1.1), 0.5 * s, 0.6 * s, fill=INK)
    svg.rect(X(-42), Z(-0.67), 6 * s, 0.1 * s, fill='#93ab73')
    svg.rect(X(-36), Z(-0.4), 5 * s, 0.35 * s, fill='#d9d3c8', stroke=INK, sw=0.5)
    svg.text(X(-33.5), Z(1.0), 'WALK', size=6.5, anchor='middle', fill='#555')
    for u in range(-29, -6, 4):
        svg.rect(X(u), Z(-0.45), 2.6 * s, 0.25 * s, fill='#d9d3c8', stroke=INK, sw=0.4)
    for u, lab in ((-30, 'P.L.'), (115, 'P.L.')):
        svg.line(X(u), Z(-3), X(u), Z(40), sw=0.8, dash='14 4 3 4', c='#555')
        svg.text(X(u), Z(40.6), lab, size=7.5, weight=700, anchor='middle')
    svg.line(X(-5), Z(-1), X(-5), Z(30), sw=0.7, dash='8 4', c='#b24a3a')
    svg.text(X(-5), Z(30.6), '25\'-0" SETBACK', size=6.5, anchor='middle', fill='#b24a3a')
    round_tree(svg, X(-20), Z(-0.67), s, h=18, r=4.5, c='#8fa677', op=0.85)
    svg.text(X(-20), Z(19.5), 'SPECIMEN TREE (BEYOND)', size=6.5, anchor='middle', fill='#555')
    for u in (109.0, 112.5):
        svg.circle(X(u), Z(8.0), 3.0 * s, fill='#8fa677', op=0.85)
        svg.rect(X(u) - 0.2 * s, Z(5.0), 0.4 * s, 5.7 * s, fill='#5b4a3a')
    svg.rect(X(114.8), Z(7.33), 0.3 * s, 8 * s, fill='#7a5b3a')
    svg.text(X(114.0), Z(11.5), '8\' FENCE', size=6.5, anchor='end', fill='#555')
    section_a(svg, left, base, s, tag_scale=0.8)


def main():
    sheet_cover()
    sheet_concept()
    site_sheet(2)
    for i, lvl in enumerate((1, 2, 3)):
        plan_sheet(lvl, 3 + i)
    roof_sheet(6)
    elev_sheet(7, 'A3.1', 'FRONT & REAR ELEVATIONS', [('front', 1023), ('rear', 2140)])
    elev_sheet(8, 'A3.2', 'SIDE ELEVATIONS', [('left', 1023), ('right', 2140)])
    section_sheet(9)
    schedules_sheet(10)
    print(f'built {len(SHEETS)} sheets · total conditioned {TOTAL:,.0f} SF')


if __name__ == '__main__':
    main()
