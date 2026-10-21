"""Floor plans, roof plan and site plan."""
import math

from model import (LV, CUT, EXT_OPS, DOORS, WALLS, ROOMS, FRONT_JAMBS, LANTERN_CW, ST_X0, ST_X1, ST_Y0, ST_Y1,
                   TREAD, RISERS, CAT_X1, ELEV, LOT_W, LOT_D, HOUSE_AT, ZONE_COLORS, RAILS, GUARD_T)
from svgkit import INK, FURN, SOFT, Fr, fi, tag

POCHE_EXT = '#1e1e1c'
POCHE_INT = '#3e3d3a'
GLASS_FILL = '#dfeaf0'
WET_FILL = '#eef2f4'
DECK_FILL = '#f3f0e9'


# ------------------------------------------------------------ openings
def assign_marks():
    w = d = 0
    for o in EXT_OPS:
        if o['typ'] in ('pivot', 'garage', 'door'):
            d += 1
            o['mark'] = f'D{d:02d}'
        else:
            w += 1
            o['mark'] = f'W{w:02d}'
    for lvl in (1, 2, 3):
        for o in DOORS[lvl]:
            if o['typ'] == 'cased':
                o['mark'] = None
                continue
            d += 1
            o['mark'] = f'D{d:02d}'


assign_marks()


def ops_for_level(lvl):
    return [o for o in EXT_OPS if o['lvl'] in (0, lvl)] + DOORS[lvl]


def ops_on(w, ops):
    out = []
    for o in ops:
        if o['o'] != w['o'] or abs(o['c'] - w['c']) > w['t'] / 2 + 0.06:
            continue
        if o['b'] <= w['a'] + 1e-6 or o['a'] >= w['b'] - 1e-6:
            continue
        out.append(o)
    return out


def solid_segments(a, b, ops):
    cuts = sorted((max(a, o['a']), min(b, o['b'])) for o in ops)
    segs, cur = [], a
    for ca, cb in cuts:
        if ca > cur + 1e-6:
            segs.append((cur, ca))
        cur = max(cur, cb)
    if cur < b - 1e-6:
        segs.append((cur, b))
    return segs


def wall_box(w, a, b):
    t = w['t'] / 2
    if w['o'] == 'h':
        return a, w['c'] - t, b, w['c'] + t
    return w['c'] - t, a, w['c'] + t, b


def draw_opening(svg, T, w, o, ff):
    c, t = w['c'], w['t']
    lo, hi = c - t / 2, c + t / 2
    a, b = max(o['a'], w['a']), min(o['b'], w['b'])
    P = (lambda s, n: T.p(s, n)) if w['o'] == 'h' else (lambda s, n: T.p(n, s))

    def L(s0, n0, s1, n1, **kw):
        svg.line(*P(s0, n0), *P(s1, n1), **kw)

    typ, width = o['typ'], b - a
    if typ in ('win', 'fixed', 'slot'):
        high = o.get('z0', ff) - ff > CUT
        dash = '5 3' if high else None
        L(a, lo, a, hi, sw=0.9)
        L(b, lo, b, hi, sw=0.9)
        L(a, lo, b, lo, sw=0.5)
        L(a, hi, b, hi, sw=0.5)
        L(a, c - 0.06, b, c - 0.06, sw=0.8, dash=dash)
        L(a, c + 0.06, b, c + 0.06, sw=0.8, dash=dash)
    elif typ == 'slider':
        L(a, lo, a, hi, sw=0.9)
        L(b, lo, b, hi, sw=0.9)
        L(a, lo, b, lo, sw=0.4)
        npan = max(2, int(round(width / 5.0)))
        pw = width / npan
        for i in range(npan):
            s0 = a + i * pw - (0.25 if i else 0)
            s1 = a + (i + 1) * pw + (0.25 if i < npan - 1 else 0)
            off = -t * 0.17 if i % 2 == 0 else t * 0.17
            svg.poly([P(s0, c + off - 0.06), P(s1, c + off - 0.06), P(s1, c + off + 0.06), P(s0, c + off + 0.06)],
                     fill='#fff', stroke=INK, sw=0.7)
    elif typ in ('swing', 'door'):
        hinge = a if o.get('hinge', 'a') == 'a' else b
        other = b if hinge == a else a
        sd = o.get('swing', 1)
        face = hi if sd > 0 else lo
        dr = 1 if other > hinge else -1
        L(hinge, face, hinge, face + sd * width, sw=1.3)
        pts = [P(hinge + dr * width * math.sin(th), face + sd * width * math.cos(th))
               for th in [i * math.pi / 36 for i in range(19)]]
        svg.poly(pts, close=False, stroke=INK, sw=0.45)
        if w['k'] == 'glass' or o.get('glass'):
            L(hinge, face, hinge, face + sd * width, sw=0.6, c='#5b8aa3')
    elif typ == 'double':
        sd = o.get('swing', 1)
        face = hi if sd > 0 else lo
        hw = width / 2
        for hinge, dr in ((a, 1), (b, -1)):
            L(hinge, face, hinge, face + sd * hw, sw=1.3)
            pts = [P(hinge + dr * hw * math.sin(th), face + sd * hw * math.cos(th))
                   for th in [i * math.pi / 36 for i in range(19)]]
            svg.poly(pts, close=False, stroke=INK, sw=0.45)
    elif typ == 'pocket':
        if o['a'] - w['a'] >= width:
            L(a - width + 0.35, c, a + 0.35, c, sw=1.5)
            L(a - width, c - 0.09, a, c - 0.09, sw=0.4, dash='3 2', c='#fff')
        else:
            L(b - 0.35, c, b + width - 0.35, c, sw=1.5)
            L(b, c - 0.09, b + width, c - 0.09, sw=0.4, dash='3 2', c='#fff')
    elif typ == 'bifold':
        sd = o.get('swing', 1)
        face = hi if sd > 0 else lo
        pts = [P(a + i * width / 4, face + sd * (width / 7 if i % 2 else 0)) for i in range(5)]
        svg.poly(pts, close=False, stroke=INK, sw=1.0)
    elif typ == 'pivot':
        sd = o.get('swing', 1)
        p = a + width * 0.3
        L(p, c - sd * width * 0.3, p, c + sd * width * 0.7, sw=2.2, c='#6e5338')
        for r, end in ((width * 0.7, b), (width * 0.3, a)):
            sgn = sd if end == b else -sd
            pts = [P(p + (end - p) * math.sin(th), c + sgn * r * math.cos(th)) for th in [i * math.pi / 36 for i in range(19)]]
            svg.poly(pts, close=False, stroke=INK, sw=0.45)
    elif typ == 'garage':
        L(a, c - 0.12, b, c - 0.12, sw=0.8, dash='8 5')
        L(a, c + 0.12, b, c + 0.12, sw=0.8, dash='8 5')
    elif typ == 'elev':
        L(a, c - 0.07, b, c - 0.07, sw=0.8)
        L(a, c + 0.07, b, c + 0.07, sw=0.8)


def mark_tag(svg, T, w, o):
    if not o.get('mark'):
        return
    a, b = max(o['a'], w['a']), min(o['b'], w['b'])
    mid = (a + b) / 2
    ext = o in EXT_OPS
    if ext:
        if w['o'] == 'h':
            out = -1 if w['c'] < 27 else 1
            x, y = mid, w['c'] + out * (w['t'] / 2 + 1.25)
        else:
            out = -1 if w['c'] < 25 else 1
            x, y = w['c'] + out * (w['t'] / 2 + 1.25), mid
        is_door = o['typ'] in ('pivot', 'garage', 'door')
        tag(svg, *T.p(x, y), o['mark'], shape='circle' if is_door else 'hex', size=6.2, r=10.5)
    else:
        sd = o.get('swing', 1) or 1
        off = sd * (w['t'] / 2 + 0.9)
        if o['typ'] in ('pocket', 'bifold', 'elev', 'double'):
            off = sd * (w['t'] / 2 + 0.75)
        x, y = (mid, w['c'] + off) if w['o'] == 'h' else (w['c'] + off, mid)
        if o.get('tag_at'):
            tag(svg, *T.p(*o['tag_at']), o['mark'], shape='circle', size=5.2, r=8.5, fill='#fff')
            return
        if o['typ'] in ('swing',):
            # sit beside the leaf rather than on top of it
            if w['o'] == 'h':
                x = (a + 0.55) if o.get('hinge', 'a') == 'b' else (b - 0.55)
            else:
                y = (a + 0.55) if o.get('hinge', 'a') == 'b' else (b - 0.55)
        tag(svg, *T.p(x, y), o['mark'], shape='circle', size=5.2, r=8.5, fill='#fff')


def draw_walls(svg, T, lvl):
    ops = ops_for_level(lvl)
    ff = LV[lvl]
    for x0, y0, x1, y1 in FRONT_JAMBS:
        T.rect(svg, x0, y0, x1, y1, fill=POCHE_EXT)
    tagged = []
    for w in WALLS[lvl]:
        mine = ops_on(w, ops)
        k = w['k']
        for a, b in solid_segments(w['a'], w['b'], mine):
            x0, y0, x1, y1 = wall_box(w, a, b)
            if k == 'ext':
                T.rect(svg, x0, y0, x1, y1, fill=POCHE_EXT)
            elif k == 'int':
                T.rect(svg, x0, y0, x1, y1, fill=POCHE_INT)
            elif k in ('glass', 'cw'):
                T.rect(svg, x0, y0, x1, y1, fill=GLASS_FILL, stroke=INK, sw=0.6)
            elif k == 'guard':
                T.rect(svg, x0, y0, x1, y1, fill='#fff', stroke='#444', sw=0.6)
        if k == 'cw':
            for m in [w['a']] + LANTERN_CW['mull_u'] + [w['b']]:
                T.rect(svg, m - 0.17, w['c'] - 0.2, m + 0.17, w['c'] + 0.2, fill=POCHE_EXT)
        for o in mine:
            draw_opening(svg, T, w, o, ff)
            tagged.append((w, o))
    for w, o in tagged:
        mark_tag(svg, T, w, o)


# ------------------------------------------------------------ furniture
def frect(svg, T, x0, y0, x1, y1, fill='#fff', sw=0.8, c=FURN, dash=None, rx=0):
    svg.rect(T.x(min(x0, x1)), T.y(max(y0, y1)), abs(x1 - x0) * T.s, abs(y1 - y0) * T.s,
             fill=fill, stroke=c, sw=sw, dash=dash, rx=rx * T.s)


def fline(svg, T, x0, y0, x1, y1, sw=0.6, c=FURN, dash=None):
    svg.line(*T.p(x0, y0), *T.p(x1, y1), sw=sw, c=c, dash=dash)


def ellipse_pts(F, cx, cy, rx, ry, n=24):
    return [F.p(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def bed(svg, T, cx, cy, w, l, head):
    F = Fr(T, cx, cy, head)
    F.rect(svg, -w / 2, -l / 2, w / 2, l / 2, fill='#fff', stroke=FURN, sw=0.9)
    F.rect(svg, -w / 2, -l / 2, w / 2, -l / 2 + 0.35, fill='#e7e2d9', stroke=FURN, sw=0.6)
    pw = (w - 0.9) / 2
    for x in (-w / 2 + 0.3, 0.15):
        F.rect(svg, x, -l / 2 + 0.6, x + pw, -l / 2 + 1.7, fill='#fff', stroke=FURN, sw=0.6)
    F.line(svg, -w / 2, -l / 2 + 2.4, w / 2, -l / 2 + 2.4, sw=0.6, c=FURN)
    svg.poly([F.p(w / 2, -l / 2 + 2.4), F.p(w / 2 - 1.3, -l / 2 + 2.4), F.p(w / 2, -l / 2 + 3.5)], fill='#f2efe9',
             stroke=FURN, sw=0.5)


def sofa(svg, T, cx, cy, w, d, back):
    F = Fr(T, cx, cy, back)
    F.rect(svg, -w / 2, -d / 2, w / 2, d / 2, fill='#fff', stroke=FURN, sw=0.9)
    F.rect(svg, -w / 2 + 0.55, -d / 2, w / 2 - 0.55, -d / 2 + 0.75, fill='#efebe4', stroke=FURN, sw=0.5)
    F.rect(svg, -w / 2, -d / 2, -w / 2 + 0.55, d / 2, fill='#efebe4', stroke=FURN, sw=0.5)
    F.rect(svg, w / 2 - 0.55, -d / 2, w / 2, d / 2, fill='#efebe4', stroke=FURN, sw=0.5)
    n = max(1, int(round((w - 1.1) / 2.6)))
    for i in range(1, n):
        x = -w / 2 + 0.55 + i * (w - 1.1) / n
        F.line(svg, x, -d / 2 + 0.75, x, d / 2, sw=0.4, c=FURN)


def chair(svg, T, cx, cy, s, back, round_=False):
    F = Fr(T, cx, cy, back)
    if round_:
        F.circle(svg, 0, 0, s / 2, fill='#fff', stroke=FURN, sw=0.7)
        return
    F.rect(svg, -s / 2, -s / 2, s / 2, s / 2, fill='#fff', stroke=FURN, sw=0.7)
    F.rect(svg, -s / 2, -s / 2, s / 2, -s / 2 + s * 0.22, fill='#efebe4', stroke=FURN, sw=0.5)


def chaise(svg, T, cx, cy, w, l, back):
    F = Fr(T, cx, cy, back)
    F.rect(svg, -w / 2, -l / 2, w / 2, l / 2, fill='#fff', stroke=FURN, sw=0.7)
    F.rect(svg, -w / 2, -l / 2, w / 2, -l / 2 + l * 0.32, fill='#efebe4', stroke=FURN, sw=0.5)


def table_chairs(svg, T, x0, y0, x1, y1, side_n, ends=True, cs=1.5):
    frect(svg, T, x0, y0, x1, y1, fill='#fbfaf7', sw=0.9)
    w, l = x1 - x0, y1 - y0
    if l >= w:
        for i in range(side_n):
            y = y0 + (i + 0.5) * l / side_n
            chair(svg, T, x0 - cs * 0.55, y, cs, 'W')
            chair(svg, T, x1 + cs * 0.55, y, cs, 'E')
        if ends:
            chair(svg, T, (x0 + x1) / 2, y0 - cs * 0.55, cs, 'S')
            chair(svg, T, (x0 + x1) / 2, y1 + cs * 0.55, cs, 'N')
    else:
        for i in range(side_n):
            x = x0 + (i + 0.5) * w / side_n
            chair(svg, T, x, y0 - cs * 0.55, cs, 'S')
            chair(svg, T, x, y1 + cs * 0.55, cs, 'N')
        if ends:
            chair(svg, T, x0 - cs * 0.55, (y0 + y1) / 2, cs, 'W')
            chair(svg, T, x1 + cs * 0.55, (y0 + y1) / 2, cs, 'E')


def round_table(svg, T, cx, cy, r, n, cs=1.4):
    for i in range(n):
        a = 2 * math.pi * (i + 0.5) / n
        x, y = cx + (r + cs * 0.45) * math.cos(a), cy + (r + cs * 0.45) * math.sin(a)
        T.circle(svg, x, y, cs / 2, fill='#fff', stroke=FURN, sw=0.6)
    T.circle(svg, cx, cy, r, fill='#fbfaf7', stroke=FURN, sw=0.9)


def rug(svg, T, x0, y0, x1, y1):
    frect(svg, T, x0, y0, x1, y1, fill='none', sw=0.5, dash='2 3', c=SOFT)


def counter(svg, T, x0, y0, x1, y1, fill='#f1eee8'):
    frect(svg, T, x0, y0, x1, y1, fill=fill, sw=0.8)


def sink(svg, T, cx, cy, w=2.0, d=1.3):
    frect(svg, T, cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2, fill='#fff', sw=0.7, rx=0.2)
    T.circle(svg, cx, cy, 0.12, stroke=FURN, sw=0.5)


def cooktop(svg, T, x0, y0, x1, y1):
    frect(svg, T, x0, y0, x1, y1, fill='#e9e6e0', sw=0.8)
    cols, rows = 3, 2
    for i in range(cols):
        for j in range(rows):
            T.circle(svg, x0 + (i + 0.5) * (x1 - x0) / cols, y0 + (j + 0.5) * (y1 - y0) / rows, 0.38, stroke=FURN, sw=0.6)


def wc(svg, T, cx, cy, back):
    F = Fr(T, cx, cy, back)
    F.rect(svg, -0.85, -1.2, 0.85, -0.6, fill='#fff', stroke=FURN, sw=0.7)
    svg.poly(ellipse_pts(F, 0, 0.25, 0.68, 0.85), fill='#fff', stroke=FURN, sw=0.7)


def lav(svg, T, cx, cy, back, w=1.7):
    F = Fr(T, cx, cy, back)
    svg.poly(ellipse_pts(F, 0, 0.05, w / 2 - 0.15, 0.5), fill='#fff', stroke=FURN, sw=0.6)


def vanity(svg, T, x0, y0, x1, y1, basins, back):
    counter(svg, T, x0, y0, x1, y1, fill='#f4f2ee')
    for cx, cy in basins:
        lav(svg, T, cx, cy, back)


def tub(svg, T, x0, y0, x1, y1):
    frect(svg, T, x0, y0, x1, y1, fill='#fff', sw=0.9, rx=0.9)
    frect(svg, T, x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3, fill='#fff', sw=0.5, rx=0.7)


def shower(svg, T, x0, y0, x1, y1):
    frect(svg, T, x0, y0, x1, y1, fill='#f6f8f9', sw=0.6)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        fline(svg, T, x, y, cx, cy, sw=0.35, c=SOFT)
    T.circle(svg, cx, cy, 0.18, fill='#fff', stroke=FURN, sw=0.6)


def car(svg, T, cx, cy, front):
    F = Fr(T, cx, cy, front)
    F.rect(svg, -3.1, -8.2, 3.1, 8.2, fill='#fff', stroke=SOFT, sw=0.8)
    F.rect(svg, -2.6, -3.6, 2.6, 3.0, fill='#f4f3f1', stroke=SOFT, sw=0.6)
    F.line(svg, -2.6, -3.6, -3.1, -5.4, sw=0.5, c=SOFT)
    F.line(svg, 2.6, -3.6, 3.1, -5.4, sw=0.5, c=SOFT)


def appliance(svg, T, cx, cy, s, label):
    frect(svg, T, cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2, fill='#fff', sw=0.7)
    T.circle(svg, cx, cy, s * 0.32, stroke=FURN, sw=0.6)
    svg.text(*T.p(cx, cy - 0.15), label, size=5.5, anchor='middle', fill=FURN)


def plant(svg, T, cx, cy, r, fill='#fff'):
    T.circle(svg, cx, cy, r, fill=fill, stroke=FURN, sw=0.6)
    for i in range(8):
        a = 2 * math.pi * i / 8
        fline(svg, T, cx + r * 0.25 * math.cos(a), cy + r * 0.25 * math.sin(a), cx + r * 0.9 * math.cos(a),
              cy + r * 0.9 * math.sin(a), sw=0.4)


def ftext(svg, T, x, y, s, size=6, rot=0, fill=FURN, weight=500):
    svg.text(*T.p(x, y), s, size=size, anchor='middle', fill=fill, rot=rot, weight=weight)


def fireplace(svg, T, x0, y0, x1, y1):
    frect(svg, T, x0, y0, x1, y1, fill='#d9d4cc', sw=0.8)
    n = 7
    for i in range(n + 1):
        t = i / n
        fline(svg, T, x0 + (x1 - x0) * t, y0, x0, y0 + (y1 - y0) * t, sw=0.3, c=FURN)


def closet_rod(svg, T, x0, y0, x1, y1):
    frect(svg, T, x0, y0, x1, y1, fill='#faf8f4', sw=0.6)
    if abs(x1 - x0) > abs(y1 - y0):
        ym = (y0 + y1) / 2
        fline(svg, T, x0 + 0.2, ym, x1 - 0.2, ym, sw=0.5, dash='4 2')
    else:
        xm = (x0 + x1) / 2
        fline(svg, T, xm, y0 + 0.2, xm, y1 - 0.2, sw=0.5, dash='4 2')


def pavers(svg, T, x0, y0, x1, y1, dx=2.0, dy=4.0, fill=DECK_FILL):
    T.rect(svg, x0, y0, x1, y1, fill=fill)
    x = x0 + dx
    while x < x1 - 1e-6:
        fline(svg, T, x, y0, x, y1, sw=0.3, c='#d3cdc1')
        x += dx
    y = y0 + dy
    while y < y1 - 1e-6:
        fline(svg, T, x0, y, x1, y, sw=0.3, c='#d3cdc1')
        y += dy


def sedum(svg, T, x0, y0, x1, y1):
    T.rect(svg, x0, y0, x1, y1, fill='#e8efdc')
    k = 0
    y = y0 + 0.7
    while y < y1 - 0.4:
        x = x0 + 0.6 + (k % 2) * 0.8
        while x < x1 - 0.4:
            T.circle(svg, x, y, 0.18, fill='#9db37e')
            x += 1.6
        y += 0.9
        k += 1


def stair(svg, T, x0, x1, y0, n_treads, tread, solid_to=None, up=None, dn=None, brk=None):
    """Straight flight; risers from y0 rising toward +Y. solid_to: last solid riser index (rest dashed)."""
    for i in range(n_treads + 1):
        y = y0 + i * tread
        dash = '4 3' if (solid_to is not None and i > solid_to) else None
        fline(svg, T, x0, y, x1, y, sw=0.75, c=INK, dash=dash)
    fline(svg, T, x0, y0, x0, y0 + n_treads * tread, sw=0.75, c=INK)
    fline(svg, T, x1, y0, x1, y0 + n_treads * tread, sw=0.75, c=INK)
    xm = (x0 + x1) / 2
    if brk is not None:
        yb = y0 + brk * tread
        pts = [T.p(x0 - 0.2, yb - 0.6), T.p(xm - 0.4, yb - 0.1), T.p(xm, yb - 0.6), T.p(xm + 0.4, yb + 0.1),
               T.p(x1 + 0.2, yb + 0.6)]
        svg.poly(pts, close=False, stroke=INK, sw=0.9)
    for spec, sign in ((up, 1), (dn, -1)):
        if not spec:
            continue
        ys, ye, label = spec
        svg.line(*T.p(xm, ys), *T.p(xm, ye), sw=0.8)
        T.circle(svg, xm, ys, 0.15, fill=INK)
        hy = ye
        d = 1 if ye > ys else -1
        svg.poly([T.p(xm, hy), T.p(xm - 0.35, hy - d * 0.8), T.p(xm + 0.35, hy - d * 0.8)], fill=INK)
        svg.text(*T.p(xm, ys - d * 0.9 - (0.35 if d > 0 else -0.6)), label, size=7, weight=700, anchor='middle')


def void_x(svg, T, x0, y0, x1, y1, label='OPEN TO BELOW'):
    fline(svg, T, x0, y0, x1, y1, sw=0.5, c=SOFT, dash='6 4')
    fline(svg, T, x0, y1, x1, y0, sw=0.5, c=SOFT, dash='6 4')
    if label:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        svg.rect(T.x(cx) - 34, T.y(cy) - 9, 68, 13, fill='#fff')
        svg.text(*T.p(cx, cy - 0.12), label, size=6.5, weight=600, anchor='middle', fill='#666', ls=0.4)


def elevator(svg, T):
    x0, y0, x1, y1 = ELEV
    frect(svg, T, x0 + 0.5, y0 + 0.5, x1 - 0.45, y1 - 0.45, fill='#fff', sw=0.6, c=INK)
    fline(svg, T, x0 + 0.5, y0 + 0.5, x1 - 0.45, y1 - 0.45, sw=0.4, c=SOFT)
    fline(svg, T, x0 + 0.5, y1 - 0.45, x1 - 0.45, y0 + 0.5, sw=0.4, c=SOFT)


# ------------------------------------------------------------ per level
def furnish_1(svg, T):
    # exterior context first
    pavers(svg, T, 0, 54, 50, 66, dx=4, dy=2)
    pavers(svg, T, 0.5, -6, 13.5, -1.5, dx=4, dy=2)
    frect(svg, T, 2.5, -5, 11.5, 0, fill='none', sw=0.7, dash='7 4', c=INK)
    ftext(svg, T, 7.0, -3.6, 'BRONZE CANOPY ABOVE', size=5.5)
    frect(svg, T, 0, 54, 50, 66, fill='none', sw=0.7, dash='7 4', c=INK)
    for x0, x1 in ((0, 0.67), (24.67, 25.33), (49.33, 50)):
        T.rect(svg, x0, 65.33, x1, 66, fill=POCHE_EXT)
    # wet rooms
    for r in ((19.71, 13.71, 26.79, 18.79), (36.21, 24.25, 49.25, 31.79), (27.25, 24.25, 35.79, 31.79)):
        T.rect(svg, *r, fill=WET_FILL)
    T.rect(svg, 27.25, 0.75, 49.25, 23.75, fill='#f2f1ee')
    # foyer
    round_table(svg, T, 11.1, 9.6, 1.5, 0)
    plant(svg, T, 11.1, 9.6, 0.8)
    T.circle(svg, 11.1, 9.6, 2.6, stroke=INK, sw=0.5, dash='5 3')
    ftext(svg, T, 11.1, 5.9, 'CASCADING CHANDELIER ABOVE', size=5.3)
    for i in range(8):
        fline(svg, T, 0.85, 12.6 + i * 0.85, 1.9, 12.6 + i * 0.85, sw=0.4)
    fline(svg, T, 1.9, 12.3, 1.9, 19.3, sw=0.5)
    ftext(svg, T, 3.1, 15.6, 'WINE', size=6.5, rot=-90, fill=INK, weight=700)
    # office
    rug(svg, T, 16.0, 3.0, 25.0, 12.6)
    frect(svg, T, 17.5, 7.0, 23.5, 9.4, fill='#fbfaf7', sw=0.9)
    chair(svg, T, 20.5, 10.25, 1.8, 'N')
    chair(svg, T, 19.0, 5.3, 1.7, 'S')
    chair(svg, T, 22.0, 5.3, 1.7, 'S')
    counter(svg, T, 25.4, 1.5, 26.75, 12.6, fill='#f6f3ee')
    ftext(svg, T, 26.1, 7.0, 'LIBRARY WALL', size=5, rot=-90)
    # powder + bar
    wc(svg, T, 20.9, 16.2, 'W')
    vanity(svg, T, 25.05, 14.4, 26.75, 17.6, [(25.95, 16.0)], 'E')
    counter(svg, T, 25.05, 19.6, 26.75, 23.6)
    sink(svg, T, 25.9, 21.9, 1.2, 1.0)
    ftext(svg, T, 25.9, 20.25, 'WINE FRIDGE', size=4.6)
    # living
    rug(svg, T, 3.2, 33.6, 14.4, 48.4)
    fireplace(svg, T, 0.75, 37.0, 2.0, 45.0)
    ftext(svg, T, 2.6, 41.0, 'LINEAR FIREPLACE / MEDIA', size=5, rot=-90)
    counter(svg, T, 0.75, 30.2, 2.0, 36.2, fill='#f6f3ee')
    sofa(svg, T, 12.6, 41.0, 9.0, 3.4, 'E')
    chair(svg, T, 5.8, 35.3, 2.6, 'S')
    chair(svg, T, 5.8, 46.7, 2.6, 'N')
    frect(svg, T, 6.3, 38.9, 9.3, 43.1, fill='#fbfaf7')
    # dining
    table_chairs(svg, T, 20.5, 36.8, 24.5, 47.2, 4)
    fline(svg, T, 22.5, 37.5, 22.5, 46.5, sw=0.5, c=SOFT, dash='2 2')
    # kitchen
    counter(svg, T, 30.2, 32.21, 43.6, 34.21)
    cooktop(svg, T, 35.0, 32.35, 39.0, 34.05)
    frect(svg, T, 34.6, 32.21, 39.4, 34.6, fill='none', sw=0.6, dash='4 3', c=INK)
    sink(svg, T, 32.4, 33.2, 1.6, 1.2)
    for y0_, y1_, lab in ((35.0, 38.0, 'REF'), (38.0, 40.5, 'FRZ'), (40.5, 43.2, 'OVENS'), (43.2, 46.0, 'PANTRY')):
        frect(svg, T, 47.25, y0_, 49.25, y1_, fill='#f1eee8', sw=0.8)
        ftext(svg, T, 48.25, (y0_ + y1_) / 2 - 0.2, lab, size=5)
    frect(svg, T, 31.5, 39.5, 43.5, 44.0, fill='#f4f1ea', sw=1.0)
    sink(svg, T, 36.3, 40.4, 2.6, 1.2)
    frect(svg, T, 38.1, 39.6, 40.1, 41.4, fill='none', sw=0.5, dash='2 2')
    ftext(svg, T, 37.5, 42.3, '12\' WATERFALL ISLAND', size=5.2)
    for x in (33.3, 36.3, 39.3, 42.3):
        chair(svg, T, x, 45.0, 1.3, 'N', round_=True)
    # scullery + mudroom
    counter(svg, T, 47.25, 24.25, 49.25, 31.79)
    sink(svg, T, 48.25, 28.5, 1.2, 1.8)
    counter(svg, T, 36.21, 24.25, 46.9, 25.75, fill='#faf8f4')
    ftext(svg, T, 41.5, 24.75, 'PANTRY SHELVING', size=4.8)
    counter(svg, T, 36.21, 29.79, 43.6, 31.79)
    ftext(svg, T, 39.9, 30.6, 'COFFEE / APPLIANCES', size=4.8)
    counter(svg, T, 27.25, 30.2, 35.79, 31.79, fill='#faf8f4')
    for i in range(1, 6):
        fline(svg, T, 27.25 + i * 1.42, 30.2, 27.25 + i * 1.42, 31.79, sw=0.4)
    ftext(svg, T, 31.5, 29.6, 'LOCKERS + BENCH', size=4.8)
    # garage
    car(svg, T, 32.8, 11.6, 'S')
    car(svg, T, 42.4, 11.6, 'S')
    counter(svg, T, 47.6, 1.3, 49.25, 14.8, fill='#faf8f4')
    ftext(svg, T, 48.45, 8.0, 'STORAGE CABINETS', size=4.8, rot=-90)
    frect(svg, T, 46.75, 19.75, 49.0, 23.5, fill='#f4f3f1', sw=0.7)
    ftext(svg, T, 47.9, 21.5, 'AHU-1', size=5)
    frect(svg, T, 27.25, 11.0, 28.0, 15.5, fill='#f4f3f1', sw=0.6)
    ftext(svg, T, 28.6, 13.25, 'PV INVERTER + BATTERY', size=4.6, rot=-90)
    for i in range(10):
        T.rect(svg, 15.35 + 1.15 * i, -0.7, 15.55 + 1.15 * i, 0, fill=POCHE_INT)
    frect(svg, T, 15.2, -4.6, 26.0, -2.0, fill='#bfdbe8', sw=0.7)
    ftext(svg, T, 20.6, -3.5, 'LINEAR REFLECTING POOL', size=5)
    frect(svg, T, 27.25, 8.6, 27.85, 9.6, fill='#fff', sw=0.6)
    ftext(svg, T, 28.6, 8.95, 'EV', size=5.5, weight=700)
    ftext(svg, T, 38.5, 1.6, "18'-0\" x 8'-0\" O.H. DOOR", size=5.2)
    # loggia
    counter(svg, T, 47.4, 55.3, 49.6, 64.6)
    cooktop(svg, T, 47.6, 58.0, 49.4, 61.0)
    ftext(svg, T, 46.6, 60.0, 'OUTDOOR KITCHEN', size=5, rot=-90)
    sofa(svg, T, 7.0, 63.4, 9.0, 3.0, 'N')
    chair(svg, T, 3.6, 57.4, 2.4, 'S')
    chair(svg, T, 10.4, 57.4, 2.4, 'S')
    frect(svg, T, 5.2, 59.4, 8.8, 61.2, fill='#e9e5de')
    ftext(svg, T, 7.0, 60.1, 'FIRE TABLE', size=4.8)
    table_chairs(svg, T, 27.5, 59.0, 35.5, 62.0, 3, ends=True)


def suite_layout(k):
    """Return bath x-range and vestibule x-range for Level 2 suite k (0..3)."""
    baths = [(0.75, 8.79), (16.21, 24.75), (25.25, 33.79), (41.21, 49.25)]
    vest = [(9.21, 12.29), (12.71, 15.79), (34.21, 37.29), (37.71, 40.79)]
    return baths[k], vest[k], k in (0, 2)


def suite_bed_x(k):
    """Bed centerline for Level 2 suite k, kept clear of the vestibule mouth."""
    _, _, bath_left = suite_layout(k)
    return 12.5 * k + (4.95 if bath_left else 7.55)


def furnish_2(svg, T):
    pavers(svg, T, 14, 0, 48.75, 6, dx=4, dy=2)
    pavers(svg, T, 0, 54, 50, 60, dx=4, dy=2)
    sedum(svg, T, 0, 60, 50, 66)
    for x in (12.5, 25, 37.5):
        T.rect(svg, x - 0.25, 54, x + 0.25, 57.0, fill='#c9b59a', stroke=FURN, sw=0.4)
    for k in range(4):
        (b0, b1), _, _ = suite_layout(k)
        T.rect(svg, b0, 28.21, b1, 35.79, fill=WET_FILL)
    T.rect(svg, 38.21, 15.21, 49.25, 23.79, fill=WET_FILL)
    # lantern: void, bridge, stair
    T.rect(svg, ST_X1, ST_Y0, CAT_X1, ST_Y1, fill='#f3f6f8')
    void_x(svg, T, CAT_X1 + 0.1, 0.5, 13.9, ST_Y1 - 0.1)
    stair(svg, T, ST_X0, ST_X1, ST_Y0, RISERS - 1, TREAD, up=(ST_Y0 + 0.4, ST_Y0 + 6.2 * TREAD, 'UP'),
          dn=(ST_Y1 - 0.3, ST_Y0 + 8.2 * TREAD, 'DN'), brk=7.2)
    ftext(svg, T, 6.25, 12.0, 'GLASS BRIDGE', size=6, rot=-90, fill=INK, weight=700)
    elevator(svg, T)
    # lounge
    round_table(svg, T, 18.4, 10.6, 1.9, 4)
    ftext(svg, T, 18.4, 13.6, 'GAME TABLE', size=5)
    rug(svg, T, 27.4, 8.0, 36.8, 19.4)
    sofa(svg, T, 29.3, 13.8, 9.2, 3.3, 'W')
    sofa(svg, T, 32.7, 9.4, 4.2, 2.9, 'S')
    frect(svg, T, 31.6, 12.2, 34.8, 15.8, fill='#fbfaf7')
    fireplace(svg, T, 36.95, 11.5, 37.79, 18.5)
    counter(svg, T, 26.0, 21.79, 37.79, 23.79)
    sink(svg, T, 31.0, 22.8, 1.6, 1.0)
    for i in range(14):
        fline(svg, T, 26.4 + i * 0.8, 23.4, 26.4 + i * 0.8, 23.79, sw=0.35)
    ftext(svg, T, 31.9, 21.1, 'WINE BAR · BACKLIT WINE WALL', size=5)
    # study
    counter(svg, T, 47.4, 7.2, 49.25, 14.4, fill='#fbfaf7')
    chair(svg, T, 46.5, 9.0, 1.6, 'W')
    chair(svg, T, 46.5, 12.6, 1.6, 'W')
    counter(svg, T, 38.6, 13.6, 45.6, 14.79, fill='#faf8f4')
    # laundry
    appliance(svg, T, 48.1, 17.4, 2.2, 'W')
    appliance(svg, T, 48.1, 19.7, 2.2, 'D')
    counter(svg, T, 38.21, 15.21, 46.6, 17.21)
    sink(svg, T, 41.6, 16.2, 1.8, 1.2)
    counter(svg, T, 38.21, 21.4, 39.8, 23.79, fill='#faf8f4')
    ftext(svg, T, 43.2, 18.0, 'FOLD / STEAM', size=4.8)
    closet_rod(svg, T, 44.4, 24.4, 46.3, 27.6)
    ftext(svg, T, 45.35, 26.0, 'LINEN', size=4.6, rot=-90)
    frect(svg, T, 46.7, 24.4, 49.04, 27.6, fill='#f4f3f1', sw=0.7)
    ftext(svg, T, 47.87, 25.85, 'AHU-2', size=5)
    # balcony
    for x in (18.2, 21.2):
        chaise(svg, T, x, 3.1, 2.2, 4.6, 'N')
    T.circle(svg, 19.7, 1.5, 0.6, fill='#fff', stroke=FURN, sw=0.6)
    round_table(svg, T, 43.8, 3.0, 1.1, 2, cs=1.3)
    # suites
    for k in range(4):
        (b0, b1), (v0, v1), bath_left = suite_layout(k)
        x0 = 12.5 * k
        if bath_left:
            shower(svg, T, b0, 28.21, b0 + 3.6, 32.3)
            wc(svg, T, b1 - 1.5, 29.3, 'S')
        else:
            shower(svg, T, b1 - 3.6, 28.21, b1, 32.3)
            wc(svg, T, b0 + 1.5, 29.3, 'S')
        vanity(svg, T, b0 + 0.3, 34.1, b1 - 0.3, 35.79, [(b0 + 2.4, 35.1), (b1 - 2.4, 35.1)], 'N')
        closet_rod(svg, T, b0, 38.79, b1, 40.79)
        cx = suite_bed_x(k)
        bed(svg, T, cx, 44.55, 5.33, 6.67, 'S')
        for dx in (-3.35, 3.35):
            frect(svg, T, cx + dx - 0.62, 41.4, cx + dx + 0.62, 42.65, fill='#fbfaf7', sw=0.6)
        chair(svg, T, x0 + (2.4 if not bath_left else 10.1), 51.6, 2.2, 'S' if k % 2 else 'S')
        chaise(svg, T, x0 + 4.4, 57.0, 2.1, 4.4, 'N')
        chaise(svg, T, x0 + 8.1, 57.0, 2.1, 4.4, 'N')
        svg.text(*T.p((b0 + b1) / 2, 32.9), f'BATH {k + 2}', size=6.5, weight=700, anchor='middle')
        svg.text(*T.p((b0 + b1) / 2, 37.3), 'WALK-IN CLOSET', size=5.5, anchor='middle', fill=FURN)


def furnish_3(svg, T):
    pavers(svg, T, 14, 0, 48.75, 6, dx=4, dy=2)
    pavers(svg, T, 0, 46, 50, 54, dx=4, dy=2)
    T.rect(svg, 31.75, 0.5, 32.25, 5.5, fill='#c9b59a', stroke=FURN, sw=0.4)
    frect(svg, T, 0, 46, 50, 50, fill='none', sw=0.7, dash='7 4', c=INK)
    ftext(svg, T, 38.5, 49.3, 'ROOF OVERHANG ABOVE', size=5.2)
    # lower roofs beyond
    frect(svg, T, 0, 54, 50, 66, fill='none', sw=0.6, c=SOFT)
    ftext(svg, T, 25, 60.3, 'LEVEL 2 TERRACE + GREEN ROOF BELOW', size=6, fill=SOFT)
    for r in ((19.71, 17.71, 26.79, 23.79), (39.21, 17.71, 49.25, 23.79), (36.21, 28.21, 49.25, 45.25)):
        T.rect(svg, *r, fill=WET_FILL)
    # lantern
    void_x(svg, T, ST_X1 + 0.2, 0.5, 13.9, ST_Y1 - 0.15)
    stair(svg, T, ST_X0, ST_X1, ST_Y0, RISERS - 1, TREAD, dn=(ST_Y1 - 0.3, ST_Y0 + 3.0, 'DN'))
    elevator(svg, T)
    # bedroom 6
    bed(svg, T, 22.6, 13.79, 6.33, 7.0, 'N')
    for dx in (-4.05, 4.05):
        frect(svg, T, 22.6 + dx - 0.8, 15.6, 22.6 + dx + 0.8, 17.2, fill='#fbfaf7', sw=0.6)
    counter(svg, T, 14.41, 8.0, 16.3, 12.8, fill='#fbfaf7')
    chair(svg, T, 17.2, 10.4, 1.6, 'E')
    chair(svg, T, 29.4, 8.4, 2.4, 'N')
    shower(svg, T, 19.71, 20.3, 23.3, 23.79)
    wc(svg, T, 25.4, 18.9, 'S')
    vanity(svg, T, 20.0, 17.71, 24.0, 19.4, [(22.0, 18.6)], 'S')
    closet_rod(svg, T, 29.96, 18.6, 31.79, 23.79)
    # bedroom 7
    bed(svg, T, 41.6, 13.79, 6.33, 7.0, 'N')
    for dx in (-4.05, 4.05):
        frect(svg, T, 41.6 + dx - 0.8, 15.6, 41.6 + dx + 0.8, 17.2, fill='#fbfaf7', sw=0.6)
    chair(svg, T, 34.6, 8.6, 2.4, 'N')
    closet_rod(svg, T, 32.21, 18.6, 34.21, 23.79)
    shower(svg, T, 45.6, 20.2, 49.25, 23.79)
    wc(svg, T, 43.6, 22.6, 'N')
    vanity(svg, T, 39.6, 17.71, 47.0, 19.4, [(41.6, 18.6), (45.0, 18.6)], 'S')
    # terraces (front)
    for x in (19.0, 22.0, 36.0, 39.0):
        chair(svg, T, x, 3.0, 2.2, 'N')
    # mech
    frect(svg, T, 40.0, 24.5, 42.5, 27.0, fill='#f4f3f1', sw=0.7)
    ftext(svg, T, 41.25, 25.6, 'AHU-3', size=5)
    T.circle(svg, 44.4, 26.0, 0.9, fill='#fff', stroke=FURN, sw=0.7)
    ftext(svg, T, 44.4, 25.85, 'HPWH', size=4.3)
    frect(svg, T, 46.4, 24.5, 48.9, 27.5, fill='none', sw=0.6, dash='3 2')
    for i in range(1, 6):
        fline(svg, T, 46.6, 24.5 + i * 0.5, 48.7, 24.5 + i * 0.5, sw=0.4)
    ftext(svg, T, 47.65, 23.0 + 5.0, 'SHIP LADDER / 30"x36" HATCH ABOVE', size=4.2)
    # primary bedroom
    rug(svg, T, 16.6, 35.4, 24.4, 44.4)
    bed(svg, T, 32.29, 33.0, 6.33, 7.0, 'E')
    for y in (29.05, 36.95):
        frect(svg, T, 34.2, y - 0.75, 35.79, y + 0.75, fill='#fbfaf7', sw=0.6)
    frect(svg, T, 27.4, 30.4, 28.4, 35.6, fill='#efebe4', sw=0.6)
    fireplace(svg, T, 14.21, 37.0, 15.0, 43.0)
    sofa(svg, T, 21.7, 40.0, 7.0, 3.0, 'E')
    frect(svg, T, 17.4, 38.6, 19.4, 41.4, fill='#fbfaf7')
    chair(svg, T, 18.0, 36.0, 2.2, 'S')
    counter(svg, T, 20.0, 28.21, 26.0, 29.8, fill='#f6f3ee')
    ftext(svg, T, 23.0, 29.0, 'MORNING BAR', size=4.8)
    # dressing room
    closet_rod(svg, T, 0.75, 28.6, 2.75, 44.85)
    closet_rod(svg, T, 3.4, 28.21, 10.6, 30.2)
    closet_rod(svg, T, 3.4, 43.25, 13.6, 45.25)
    frect(svg, T, 5.4, 33.6, 8.9, 39.4, fill='#f4f1ea', sw=0.9)
    ftext(svg, T, 7.15, 36.4, 'ISLAND', size=5)
    frect(svg, T, 11.8, 33.0, 13.79, 40.0, fill='#faf8f4', sw=0.6)
    ftext(svg, T, 12.8, 36.5, 'MIRROR / VANITY', size=4.6, rot=-90)
    # spa bath
    shower(svg, T, 36.21, 28.21, 41.5, 34.0)
    ftext(svg, T, 38.85, 30.0, 'RAIN SHOWER', size=4.8)
    wc(svg, T, 47.2, 29.4, 'S')
    vanity(svg, T, 47.35, 34.6, 49.25, 42.6, [(48.3, 36.6), (48.3, 40.6)], 'E')
    tub(svg, T, 38.6, 41.6, 44.6, 44.6)
    frect(svg, T, 42.6, 35.4, 44.4, 37.8, fill='#fbfaf7', sw=0.6)
    # primary terrace
    for x in (4.0, 7.0):
        chaise(svg, T, x, 50.0, 2.3, 5.8, 'S')
    sofa(svg, T, 24.0, 49.0, 8.0, 2.8, 'S')
    frect(svg, T, 22.0, 50.9, 26.0, 52.4, fill='#fbfaf7')
    for x in range(10, 48, 4):
        plant(svg, T, x + 1.3, 53.2, 0.55)
    shower(svg, T, 46.4, 46.4, 49.4, 49.2)
    ftext(svg, T, 47.9, 49.8, 'OUTDOOR SHOWER', size=4.6)


FURNISH = {1: furnish_1, 2: furnish_2, 3: furnish_3}


def room_labels(svg, T, lvl):
    for r in ROOMS[lvl]:
        if not r['at']:
            continue
        x, y = T.p(*r['at'])
        size = r['size'] or 10.5
        svg.text(x, y, r['name'], size=size, weight=700, anchor='middle', ls=0.6)
        line2 = []
        if r['dims']:
            x0, y0, x1, y1 = r['rect']
            line2.append(f'{fi(x1 - x0)} x {fi(y1 - y0)}')
        if r['sub']:
            line2.append(r['sub'])
        for i, s in enumerate(line2):
            svg.text(x, y + size * 1.05 + i * size * 0.95, s, size=size * 0.68, anchor='middle', fill='#5a5650', ls=0.3)


# ----------------------------------------------------------- dims / grid
GRID_X = [('A', 0), ('B', 14), ('C', 27), ('D', 36), ('E', 50)]
GRID_Y = [('1', 0), ('2', 6), ('3', 24), ('4', 32), ('5', 46), ('6', 54)]


def tick(svg, x, y):
    svg.line(x - 4, y + 4, x + 4, y - 4, sw=1.1)


def dim_h(svg, T, xs, yd, ext_from=None, above=True):
    for i, x in enumerate(xs):
        sx, sy = T.p(x, yd)
        if ext_from is not None:
            svg.line(sx, T.y(ext_from) + 6, sx, sy + 6, sw=0.4, c='#777')
        tick(svg, sx, sy)
        if i:
            px = T.x(xs[i - 1])
            svg.line(px, sy, sx, sy, sw=0.6)
            svg.text((px + sx) / 2, sy - 5, fi(x - xs[i - 1]), size=8.5, anchor='middle')


def dim_v(svg, T, ys, xd, ext_from=None):
    for i, y in enumerate(ys):
        sx, sy = T.p(xd, y)
        if ext_from is not None:
            svg.line(T.x(ext_from) - 6, sy, sx - 6, sy, sw=0.4, c='#777')
        tick(svg, sx, sy)
        if i:
            py = T.y(ys[i - 1])
            svg.line(sx, py, sx, sy, sw=0.6)
            svg.text(sx - 5, (py + sy) / 2, fi(y - ys[i - 1]), size=8.5, anchor='middle', rot=-90)


def grid(svg, T, ymin, xmin, ymax, xmax, ys=None):
    for lab, x in GRID_X:
        sx = T.x(x)
        svg.line(sx, T.y(ymin + 1.0), sx, T.y(ymin + 4.4), sw=0.5, dash='10 3 2 3', c='#555')
        svg.circle(sx, T.y(ymin), 15, fill='#fff', stroke=INK, sw=1)
        svg.text(sx, T.y(ymin) + 5, lab, size=12, weight=700, anchor='middle')
    for lab, y in (ys or GRID_Y):
        sy = T.y(y)
        svg.line(T.x(xmin + 1.0), sy, T.x(xmin + 4.4), sy, sw=0.5, dash='10 3 2 3', c='#555')
        svg.circle(T.x(xmin), sy, 15, fill='#fff', stroke=INK, sw=1)
        svg.text(T.x(xmin), sy + 5, lab, size=12, weight=700, anchor='middle')


def section_mark(svg, T, letter, sheet, a, b, along, at, look):
    """Section cut line. along='v' -> vertical line at X=at from Y=a to b; look gives arrow direction."""
    if along == 'v':
        p0, p1 = T.p(at, a), T.p(at, b)
    else:
        p0, p1 = T.p(a, at), T.p(b, at)
    svg.line(*p0, *p1, sw=1.1, dash='22 5 4 5', c='#333')
    for (x, y) in (p0, p1):
        dx, dy = {'-x': (-1, 0), '+x': (1, 0), '+y': (0, -1), '-y': (0, 1)}[look]
        r = 17
        svg.poly([(x + dx * r * 1.75 + dy * 0, y + dy * r * 1.75), (x - dy * r, y + dx * r), (x + dy * r, y - dx * r)],
                 fill=INK)
        svg.circle(x, y, r, fill='#fff', stroke=INK, sw=1.2)
        svg.line(x - r, y, x + r, y, sw=0.8)
        svg.text(x, y - 3.5, letter, size=11, weight=700, anchor='middle')
        svg.text(x, y + 11, sheet, size=6.5, anchor='middle')


def elev_mark(svg, T, x, y, look, num_, sheet):
    sx, sy = T.p(x, y)
    dx, dy = {'-x': (-1, 0), '+x': (1, 0), '+y': (0, -1), '-y': (0, 1)}[look]
    r = 16
    svg.poly([(sx + dx * r * 1.8, sy + dy * r * 1.8), (sx - dy * r * 1.05, sy + dx * r * 1.05),
              (sx + dy * r * 1.05, sy - dx * r * 1.05)], fill=INK)
    svg.circle(sx, sy, r, fill='#fff', stroke=INK, sw=1.2)
    svg.line(sx - r, sy, sx + r, sy, sw=0.8)
    svg.text(sx, sy - 3.5, num_, size=10.5, weight=700, anchor='middle')
    svg.text(sx, sy + 11, sheet, size=6.5, anchor='middle')


def floor_plan(svg, T, lvl):
    FURNISH[lvl](svg, T)
    draw_walls(svg, T, lvl)
    for (o, c, a, b, z0, _z1) in RAILS:
        if abs(z0 - LV[lvl]) < 0.01:
            if o == 'h':
                T.rect(svg, a, c - GUARD_T / 2, b, c + GUARD_T / 2, fill='#fff', stroke='#444', sw=0.6)
            else:
                T.rect(svg, c - GUARD_T / 2, a, c + GUARD_T / 2, b, fill='#fff', stroke='#444', sw=0.6)
    room_labels(svg, T, lvl)
    if lvl == 1:
        stair(svg, T, ST_X0, ST_X1, ST_Y0, RISERS - 1, TREAD, solid_to=7, up=(ST_Y0 + 0.4, ST_Y0 + 6.6 * TREAD, 'UP'),
              brk=7.3)
        elevator(svg, T)
    # dimensions
    depth = 66 if lvl < 3 else 54
    dim_h(svg, T, [0, 14, 27, 36, 50], -5.5, ext_from=-1.6)
    dim_h(svg, T, [0, 50], -8.5)
    ys = [0, 6, 24, 32, 46, 54] + ([66] if lvl < 3 else [])
    dim_v(svg, T, ys, -5.5, ext_from=-1.5)
    dim_v(svg, T, [0, depth], -8.5)
    grid(svg, T, -12.2, -12.2, depth, 50)
    section_mark(svg, T, 'A', 'A4.1', -10.5, depth + 3.5, 'v', 6.25, '-x')
    section_mark(svg, T, 'B', 'A4.1', -10.5, 57.0, 'h', 43, '+y')
    if lvl == 1:
        elev_mark(svg, T, 20.5, -11.4, '+y', '1', 'A3.1')
        elev_mark(svg, T, 25.0, 70.0, '-y', '2', 'A3.1')
        elev_mark(svg, T, -12.2, 39.0, '+x', '1', 'A3.2')
        elev_mark(svg, T, 56.5, 30.0, '-x', '2', 'A3.2')


# ------------------------------------------------------------ areas
def level_areas():
    """Gross conditioned area per level to exterior face of framing; voids excluded."""
    L1 = 50 * 54 - 23 * 24
    lantern2 = 8.08 * 24 + (14 - 8.08) * (24 - ST_Y1)
    L2 = 36 * 48 + 14 * 30 + lantern2
    lantern3 = ST_X1 * (ST_Y1 - ST_Y0) + 14 * (24 - ST_Y1)
    L3 = 36 * 40 + 14 * 22 + lantern3
    return {'L1': L1, 'L2': L2, 'L3': L3, 'garage': 23 * 24, 'loggia': 50 * 12,
            'balcony': 34.75 * 6, 'l2terrace': 50 * 6, 'green': 50 * 6, 'l3front': 34.75 * 6, 'primaryterrace': 50 * 8}


# ------------------------------------------------------------ roof plan
def roof_plan(svg, T):
    pavers(svg, T, 0, 50, 50, 54, dx=4, dy=2)
    pavers(svg, T, 0, 54, 50, 60, dx=4, dy=2)
    sedum(svg, T, 0, 60, 50, 66)
    T.rect(svg, 0, 59.85, 50, 60.15, fill='#fff', stroke='#444', sw=0.6)
    T.rect(svg, 0, 53.6, 50, 53.9, fill='#fff', stroke='#444', sw=0.6)
    for x in (12.5, 25, 37.5):
        T.rect(svg, x - 0.25, 54, x + 0.25, 57.0, fill='#c9b59a', stroke=FURN, sw=0.4)
    # main roof
    outline = [(14, 0), (50, 0), (50, 50), (0, 50), (0, 24), (14, 24)]
    T.poly(svg, outline, fill='#f4f3f0', stroke=INK, sw=2.2)
    inner = [(14.6, 0.6), (49.4, 0.6), (49.4, 49.4), (0.6, 49.4), (0.6, 24.6), (14.6, 24.6)]
    T.poly(svg, inner, fill='none', stroke=INK, sw=0.7)
    # crickets to drains
    for d in ((30, 13), (25, 37)):
        T.circle(svg, *d, 0.55, fill='#fff', stroke=INK, sw=0.9)
        T.circle(svg, *d, 0.2, fill=INK)
    for a, b in (((14.6, 0.6), (30, 13)), ((49.4, 0.6), (30, 13)), ((49.4, 24.0), (30, 13)), ((14.6, 24.6), (30, 13)),
                 ((0.6, 24.6), (25, 37)), ((49.4, 24.0), (25, 37)), ((49.4, 49.4), (25, 37)), ((0.6, 49.4), (25, 37))):
        fline(svg, T, *a, *b, sw=0.5, c=SOFT, dash='5 3')
    ftext(svg, T, 30, 11.6, 'RD-1 / OD-1', size=6, fill=INK, weight=700)
    ftext(svg, T, 25, 35.6, 'RD-2 / OD-2', size=6, fill=INK, weight=700)
    for d in ((31.4, 13), (26.4, 37), (4.6, 21.5)):
        T.circle(svg, *d, 0.45, fill='#fff', stroke=INK, sw=0.8, dash='2 1.5')
    # PV array
    mods = pv_modules()
    for x, y, mw, mh in mods:
        frect(svg, T, x, y, x + mw - 0.15, y + mh - 0.15, fill='#dbe3ec', sw=0.5, c='#6f7f91')
    n_mod = len(mods)
    # equipment
    frect(svg, T, 37.5, 29.0, 48.5, 36.5, fill='none', sw=0.7, dash='6 3', c=INK)
    for x in (38.5, 42.0, 45.5):
        appliance(svg, T, x + 1.25, 31.6, 2.6, '')
    ftext(svg, T, 43.0, 34.9, 'HEAT PUMP CONDENSERS (3) ON RAILS', size=5.2, fill=INK)
    ftext(svg, T, 43.0, 35.8, 'BEHIND 42" BRONZE LOUVER SCREEN', size=5.2, fill=INK)
    frect(svg, T, 46.4, 24.5, 48.9, 27.5, fill='#fff', sw=0.8, c=INK)
    fline(svg, T, 46.4, 24.5, 48.9, 27.5, sw=0.4)
    ftext(svg, T, 43.2, 25.6, 'ROOF HATCH 30"x36"', size=5.2, fill=INK)
    # lantern roof
    frect(svg, T, 0, -1.5, 14, 24, fill='#e6e0d6', sw=2.2, c=INK)
    frect(svg, T, 0.6, -0.9, 13.4, 23.4, fill='none', sw=0.7, c=INK)
    frect(svg, T, 8.3, 1.0, 13.4, 18.8, fill='#dfeaf0', sw=1.0, c=INK)
    fline(svg, T, 8.3, 1.0, 13.4, 18.8, sw=0.4, c='#5b8aa3')
    fline(svg, T, 8.3, 18.8, 13.4, 1.0, sw=0.4, c='#5b8aa3')
    ftext(svg, T, 4.4, 14.5, 'LANTERN ROOF', size=6.5, fill=INK, weight=700)
    ftext(svg, T, 4.4, 13.2, "T.O. PARAPET +37'-0\"", size=5.5, fill=INK)
    ftext(svg, T, 10.85, 21.0, 'STRUCTURAL GLASS SKYLIGHT', size=4.8, fill=INK)
    ftext(svg, T, 10.85, 20.1, 'OVER CHANDELIER VOID', size=4.8, fill=INK)
    T.circle(svg, 3.0, 21.5, 0.55, fill='#fff', stroke=INK, sw=0.9)
    T.circle(svg, 3.0, 21.5, 0.2, fill=INK)
    ftext(svg, T, 3.8, 19.9, 'RD-3 / OD-3', size=5, fill=INK, weight=700)
    # canopy
    frect(svg, T, 2.5, -5, 11.5, -1.5, fill='#e6e0d6', sw=0.9, c=INK)
    ftext(svg, T, 7.0, -3.5, 'ENTRY CANOPY +10\'-0"', size=5, fill=INK)
    return n_mod


def pv_modules():
    """PV module rectangles (x, y, w, h), held 3'-0" off every parapet and clear of drains and equipment."""
    mods = []
    for (x0, y0, x1, y1) in ((17.6, 3.6, 46.4, 11.0), (17.6, 15.5, 46.4, 22.5), (3.6, 39.0, 46.4, 46.4)):
        mw, mh = 5.6, 3.5
        y = y0
        while y + mh <= y1 + 1e-6:
            x = x0
            while x + mw <= x1 + 1e-6:
                mods.append((x, y, mw, mh))
                x += mw
            y += mh
    return mods


# ------------------------------------------------------------ site plan
def site_plan(svg, T):
    hx, hy = HOUSE_AT

    def H(x, y):
        return x + hx, y + hy
    # street
    T.rect(svg, -14, -22, LOT_W + 14, -12, fill='#e7e6e3')
    fline(svg, T, -14, -17, LOT_W + 14, -17, sw=0.8, c='#fff', dash='14 10')
    fline(svg, T, -14, -12, LOT_W + 14, -12, sw=1.4, c=INK)
    fline(svg, T, -14, -12.5, LOT_W + 14, -12.5, sw=0.5, c=INK)
    svg.text(*T.p(LOT_W / 2, -19.5), 'GOOCH STREET', size=14, weight=700, anchor='middle', ls=3)
    T.rect(svg, -14, -12, LOT_W + 14, -6, fill='#eef3e6')
    T.rect(svg, -14, -6, LOT_W + 14, -1, fill='#f2f1ed', stroke=SOFT, sw=0.5)
    x = -14
    while x < LOT_W + 14:
        fline(svg, T, x, -6, x, -1, sw=0.3, c=SOFT)
        x += 5
    ftext(svg, T, -7.5, -3.8, 'PUBLIC SIDEWALK', size=6)
    # lot
    T.rect(svg, 0, 0, LOT_W, LOT_D, fill='#f7faf2')
    # rear yard: lawn, deck, pool
    T.rect(svg, *H(0, 66), *H(50, 88), fill='#eaeae4')
    pavers(svg, T, *H(0, 66), *H(50, 88), dx=4, dy=2)
    pool = (*H(5, 69), *H(35, 83))
    T.rect(svg, *pool, fill='#bfdbe8', stroke=INK, sw=1.2)
    T.rect(svg, *H(29, 69), *H(35, 83), fill='#d5e8f0', stroke='#6a95ab', sw=0.6, dash='3 2')
    ftext(svg, T, *H(20, 76.3), 'POOL 30\' x 14\'', size=7, fill=INK, weight=700)
    ftext(svg, T, *H(20, 75.0), 'HEATED · SALT · AUTO COVER', size=5.5, fill=INK)
    ftext(svg, T, *H(32, 75.5), 'SUN SHELF', size=5, fill=INK, rot=-90)
    T.rect(svg, *H(38, 69), *H(46, 77), fill='#a9cfe0', stroke=INK, sw=1.2)
    ftext(svg, T, *H(42, 73.0), 'SPA', size=7, fill=INK, weight=700)
    ftext(svg, T, *H(42, 71.8), 'RAISED · SPILLOVER', size=4.6, fill=INK)
    T.rect(svg, *H(0, 88), *H(50, 108), fill='#e2ecd2')
    fp = H(40, 96.5)
    T.circle(svg, *fp, 6.5, fill='#efeae1', stroke=INK, sw=0.8)
    T.circle(svg, *fp, 5.2, fill='none', stroke=FURN, sw=0.5)
    T.circle(svg, *fp, 1.5, fill='#d6c6ae', stroke=INK, sw=0.7)
    ftext(svg, T, fp[0], fp[1] - 3.3, 'FIRE LOUNGE', size=5.5, fill=INK)
    ftext(svg, T, *H(17, 98), 'LAWN · ZOYSIA', size=6.5, fill='#5d7140')
    for x in range(3, 50, 7):
        T.circle(svg, *H(x, 111.5), 2.7, fill='#cfe0bd', stroke='#6c8752', sw=0.6)
    ftext(svg, T, *H(25, 109.0), 'EVERGREEN PRIVACY SCREEN (NELLIE R. STEVENS HOLLY)', size=5.2, fill='#5d7140')
    # front yard
    T.rect(svg, 0, 0, LOT_W, hy - 0.01, fill='#e2ecd2')
    T.rect(svg, *H(29, -hy - 12), *H(49, 0), fill='#eceae5', stroke=INK, sw=0.8)
    T.poly(svg, [H(26.5, -hy - 12), H(29, -hy - 9.5), H(29, -hy - 12)], fill='#eceae5', stroke=INK, sw=0.8)
    T.poly(svg, [H(51.5, -hy - 12), H(49, -hy - 9.5), H(49, -hy - 12)], fill='#eceae5', stroke=INK, sw=0.8)
    T.rect(svg, *H(29, -hy - 6), *H(49, -hy - 1), fill='#f2f1ed', stroke=SOFT, sw=0.5)
    for y in range(-int(hy) + 6, 0, 7):
        fline(svg, T, *H(29, y), *H(49, y), sw=0.35, c=SOFT)
    fline(svg, T, *H(39, -hy), *H(39, 0), sw=0.35, c=SOFT)
    ftext(svg, T, *H(39, -14), 'CONCRETE DRIVE', size=6.5, fill=INK)
    ftext(svg, T, *H(39, -15.3), 'w/ STONE BANDS', size=5.5, fill=INK)
    y = -hy + 1.5
    while y < -6:
        T.rect(svg, *H(5.0, y), *H(9.0, y + 2.6), fill='#efede8', stroke=INK, sw=0.6)
        y += 3.6
    T.rect(svg, *H(1.5, -6), *H(13.5, -0.2), fill='#efede8', stroke=INK, sw=0.6)
    T.rect(svg, *H(15.2, -4.6), *H(26.0, -2.0), fill='#bfdbe8', stroke=INK, sw=0.8)
    ftext(svg, T, *H(20.6, -6.4), 'LINEAR REFLECTING POOL', size=5, fill=INK)
    for x, y, r in ((22, -17, 4.5), (-1.0, -20, 3.0)):
        T.circle(svg, *H(x, y), r, fill='#d8e6c3', stroke='#6c8752', sw=0.7)
        for i in range(8):
            a = 2 * math.pi * i / 8
            fline(svg, T, *H(x, y), *H(x + r * 0.9 * math.cos(a), y + r * 0.9 * math.sin(a)), sw=0.4, c='#6c8752')
    ftext(svg, T, *H(22, -22.3), 'SPECIMEN SABAL PALM (RELOCATED)', size=5, fill='#5d7140')
    for x0, x1 in ((0, 4.8), (27, 28.8)):
        T.rect(svg, *H(x0, -3.5), *H(x1, -0.2), fill='#d2e1bd')
    # side yards
    T.rect(svg, 0, hy, hx, hy + 66, fill='#ece9e1')
    T.rect(svg, LOT_W - 5, hy, LOT_W, hy + 66, fill='#ece9e1')
    for y in range(int(hy) + 2, int(hy) + 64, 4):
        T.rect(svg, 1.0, y, 4.0, y + 2.2, fill='#f7f6f2', stroke=SOFT, sw=0.4)
    T.rect(svg, LOT_W - 4.6, hy + 6, LOT_W - 0.4, hy + 14, fill='#f0eee9', stroke=INK, sw=0.6)
    ftext(svg, T, LOT_W - 2.5, hy + 10, 'BINS', size=5, fill=INK, rot=-90)
    T.rect(svg, LOT_W - 4.6, hy + 88, LOT_W - 0.4, hy + 96, fill='#f0eee9', stroke=INK, sw=0.6)
    ftext(svg, T, LOT_W - 2.5, hy + 92, 'POOL EQUIP.', size=4.6, fill=INK, rot=-90)
    T.rect(svg, 0.6, hy + 58, 4.4, hy + 61.5, fill='#f6f8f9', stroke=INK, sw=0.6)
    ftext(svg, T, 2.5, hy + 59.6, 'OUTDOOR SHWR', size=4.2, fill=INK)
    # house footprint (roof plan simplified)
    T.rect(svg, *H(0, 54), *H(50, 66), fill='#ebe7df', stroke=INK, sw=0.9)
    ftext(svg, T, *H(25, 62.6), 'COVERED LOGGIA / L2 TERRACE & GREEN ROOF ABOVE', size=5.3, fill=INK)
    T.poly(svg, [H(0, 24), H(14, 24), H(14, 0), H(50, 0), H(50, 54), H(0, 54)], fill='#d9d3c8', stroke=INK, sw=2.0)
    T.poly(svg, [H(0, 24), H(14, 24), H(14, 0), H(50, 0), H(50, 50), H(0, 50)], fill='#cfc8bb', stroke=INK, sw=0.8)
    T.rect(svg, *H(0, -1.5), *H(14, 24), fill='#8c8073', stroke=INK, sw=2.0)
    T.rect(svg, *H(2.5, -5), *H(11.5, -1.5), fill='#b9ada0', stroke=INK, sw=0.8)
    for xx in range(0, 10):
        T.rect(svg, *H(15.35 + xx * 1.15, -0.7), *H(15.55 + xx * 1.15, 0), fill=INK)
    ftext(svg, T, *H(7, 12), 'GLASS', size=6, fill='#fff', weight=700)
    ftext(svg, T, *H(7, 10.8), 'LANTERN', size=6, fill='#fff', weight=700)
    svg.text(*T.p(*H(32, 30)), 'PROPOSED RESIDENCE', size=10, weight=700, anchor='middle', ls=1)
    a = level_areas()
    svg.text(*T.p(*H(32, 27.6)), f"3 STORIES · {a['L1'] + a['L2'] + a['L3']:,.0f} SF CONDITIONED", size=7.5,
             anchor='middle')
    svg.text(*T.p(*H(32, 25.6)), "L1 F.F. = 100'-0\" (ASSUMED DATUM)", size=7.5, anchor='middle')
    svg.text(*T.p(*H(32, 23.6)), "T.O. PARAPET 134'-6\" · LANTERN 137'-0\"", size=7.5, anchor='middle')
    # setbacks
    fline(svg, T, 0, 25, LOT_W, 25, sw=0.8, c='#b24a3a', dash='10 4')
    ftext(svg, T, 47.0, 25.5, "25'-0\" FRONT SETBACK", size=5.5, fill='#b24a3a')
    for x in (5, LOT_W - 5):
        fline(svg, T, x, 25, x, LOT_D - 5, sw=0.8, c='#b24a3a', dash='10 4')
    fline(svg, T, 5, LOT_D - 5, LOT_W - 5, LOT_D - 5, sw=0.8, c='#b24a3a', dash='10 4')
    ftext(svg, T, 30, LOT_D - 4.4, "5'-0\" REAR SETBACK", size=5.5, fill='#b24a3a')
    # fences & gates
    for x in (0.15, LOT_W - 0.15):
        fline(svg, T, x, hy + 26, x, LOT_D, sw=2.2, c='#7a5b3a')
    fline(svg, T, 0, LOT_D - 0.15, LOT_W, LOT_D - 0.15, sw=2.2, c='#7a5b3a')
    for x0, x1 in ((0, 5), (LOT_W - 5, LOT_W)):
        fline(svg, T, x0, hy + 26, x1, hy + 26, sw=2.2, c='#7a5b3a')
        fline(svg, T, x0 + 0.6, hy + 26, x0 + 0.6, hy + 30.2, sw=0.6, c='#7a5b3a')
        svg.path('M {} {} A {} {} 0 0 1 {} {}'.format(*T.p(x0 + 0.6, hy + 30.2), T.L(4.2), T.L(4.2),
                                                      *T.p(x1 - 0.2, hy + 26)), stroke='#7a5b3a', sw=0.5)
    # property line
    T.rect(svg, 0, 0, LOT_W, LOT_D, fill='none', stroke=INK, sw=1.8, dash='26 6 4 6')
    # utilities
    T.rect(svg, *H(23.5, -hy + 4.6), *H(25.5, -hy + 6.0), fill='#fff', stroke=INK, sw=0.7)
    ftext(svg, T, *H(24.5, -hy + 3.4), 'WM', size=5, fill=INK, weight=700)
    T.circle(svg, *H(50.9, 3.0), 0.6, fill=INK)
    ftext(svg, T, *H(52.6, 3.0), 'EM', size=5, fill=INK, weight=700)
    T.circle(svg, *H(-2.0, 50), 0.5, fill='#fff', stroke=INK, sw=0.7)
    ftext(svg, T, *H(-2.0, 48.3), 'CO', size=5, fill=INK, weight=700)
    # dimensions
    dim_h(svg, T, [0, 5, 55, 60], LOT_D + 4.5)
    dim_v(svg, T, [0, hy, hy + 54, hy + 66, LOT_D], -6.5)
    dim_v(svg, T, [0, LOT_D], -10.5)
    dim_h(svg, T, [0, LOT_W], LOT_D + 8)
