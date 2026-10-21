"""Elevations (painter's algorithm over the massing model, with 45-degree sun shadows) and sections."""
import math

from model import (BOXES, RAILS, EXT_OPS, LANTERN_CW, GRADE, LV, ROOF, PARAPET, LANTERN_TOP, WALLS, ST_X0, ST_X1,
                   ST_Y0, ST_Y1, RISER, TREAD, RISERS)
from svgkit import INK, SOFT, fi, tag

FACE = {'front': '-y', 'rear': '+y', 'left': '-x', 'right': '+x'}

PALETTE = {
    'day': dict(stone='#e6dece', stone_j='#cfc4b2', wood='#b98a5c', wood_j='#9d7149', bronze='#3c3530',
                bronze_j='#2c2622', green='#7c9360', edge='#3b3631', shadow='#1f2731', shadow_op=0.30),
    'dusk': dict(stone='#9b958c', stone_j='#86807a', wood='#7d5b3f', wood_j='#664a33', bronze='#26221f',
                 bronze_j='#1a1714', green='#4b5b3e', edge='#1d1b19', shadow='#0d1220', shadow_op=0.35),
}

KEYNOTES = [
    (1, 'Sintered-stone rainscreen panels, 5\'x10\' warm limestone finish, 1/4" open joints'),
    (2, 'Thermally-modified ash cladding, vertical shiplap, natural oil finish'),
    (3, 'Dark bronze anodized aluminum: lantern frame, fascia and panels'),
    (4, 'Structural glass curtain wall, low-iron low-E insulated units, bronze caps'),
    (5, 'Lift-slide door system, thermally broken, dark bronze frame'),
    (6, 'Frameless glass guard, 42" A.F.F., laminated, bronze base shoe'),
    (7, 'Pivot entry door, rift white oak, 4\'-0" x 10\'-0", bronze pull'),
    (8, 'Overhead garage door, bronze frame, satin-etched glass'),
    (9, 'Wood fin screen, 2" x 10" thermally-modified ash @ 13" o.c.'),
    (10, 'Cantilevered bronze entry canopy with integral downlights'),
    (11, 'Wood slat soffit with continuous LED cove (2700K)'),
    (12, 'Extensive sedum green roof with stone ballast edge'),
    (13, 'Steel column, 8" square, bronze powder coat'),
    (14, 'Casement / awning windows, dark bronze frame'),
    (15, 'Wood privacy fins between terraces'),
]


def proj_box(b, v):
    if v == 'front':
        return b['x0'], b['x1'], b['y0'], b['y1']
    if v == 'rear':
        return -b['x1'], -b['x0'], -b['y1'], -b['y0']
    if v == 'left':
        return -b['y1'], -b['y0'], b['x0'], b['x1']
    return b['y0'], b['y1'], -b['x1'], -b['x0']


def proj_plane(o, c, a, b, v, nrm):
    if o == 'h':
        if v == 'front' and nrm in ('-y', 'both'):
            return a, b, c
        if v == 'rear' and nrm in ('+y', 'both'):
            return -b, -a, -c
    else:
        if v == 'left' and nrm in ('-x', 'both'):
            return -b, -a, c
        if v == 'right' and nrm in ('+x', 'both'):
            return a, b, -c
    return None


def build_items(v):
    items = []
    for b in BOXES:
        u0, u1, dn, df = proj_box(b, v)
        mat = b['f'].get(FACE[v], b['m'])
        items.append(dict(k='face', u0=u0, u1=u1, z0=b['z0'], z1=b['z1'], d=dn, df=df, mat=mat, cast=b['cast'],
                          n=b['n'], grp=b['grp'], order=0))
    for o in EXT_OPS + [LANTERN_CW]:
        pr = proj_plane(o['o'], o['c'], o['a'], o['b'], v, o['n'])
        if pr:
            u0, u1, d = pr
            depth = d - (0.03 if o['typ'] != 'cw' else 0.02)
            if o['typ'] == 'pivot':
                depth -= 0.01
            items.append(dict(k='panel', u0=u0, u1=u1, z0=o['z0'], z1=o['z1'], d=depth, df=depth, op=o,
                              typ=o['typ'], n=o.get('mark', 'cw'), grp='glass', order=1))
    for (o, c, a, b, z0, z1) in RAILS:
        pr = proj_plane(o, c, a, b, v, 'both')
        if pr:
            u0, u1, d = pr
            items.append(dict(k='rail', u0=u0, u1=u1, z0=z0, z1=z1, d=d, df=d, grp='rail', n='rail', order=2))
    items.sort(key=lambda it: (-it['d'], it['order']))
    return items


def extents(v):
    items = build_items(v)
    return min(i['u0'] for i in items), max(i['u1'] for i in items)


class Elev:
    """Draw one elevation. left = sheet x for the minimum u; base = sheet y for Z = 0."""

    def __init__(self, svg, v, left, base, s, mode='day', hl=None, shadows=True, interior=True):
        self.svg, self.v, self.s, self.mode = svg, v, s, mode
        self.items = build_items(v)
        self.umin = min(i['u0'] for i in self.items)
        self.umax = max(i['u1'] for i in self.items)
        self.ox = left - self.umin * s
        self.oy = base
        self.hl = hl
        self.shadows = shadows and hl is None
        self.interior = interior
        self.pal = PALETTE['dusk' if mode == 'dusk' else 'day']
        if mode == 'dusk':
            self.g_glass = svg.lin_grad([(0, '#ffe6b6', None), (0.55, '#f6c27c', None), (1, '#e59a4f', None)])
            self.g_frost = svg.lin_grad([(0, '#f5d9a8', None), (1, '#d79a5c', None)])
        else:
            self.g_glass = svg.lin_grad([(0, '#c9d5dd', None), (0.45, '#93a7b6', None), (1, '#5a6c7c', None)])
            self.g_frost = svg.lin_grad([(0, '#e3e8eb', None), (1, '#c3ccd2', None)])
        self.g_rail = svg.lin_grad([(0, '#d4e4ec', 0.45), (1, '#a9c4d2', 0.25)])

    def X(self, u):
        return self.ox + u * self.s

    def Z(self, z):
        return self.oy - z * self.s

    def R(self, u0, z0, u1, z1):
        return self.X(u0), self.Z(z1), (u1 - u0) * self.s, (z1 - z0) * self.s

    @property
    def width(self):
        return (self.umax - self.umin) * self.s

    def u_of(self, x, y):
        return {'front': x, 'rear': -x, 'left': -y, 'right': y}[self.v]

    # ------------------------------------------------------------ draw
    def draw(self):
        for it in self.items:
            if it['k'] == 'face':
                self.face(it)
            elif it['k'] == 'panel':
                self.panel(it)
            else:
                self.rail(it)
        if self.mode == 'dusk':
            self.lights()

    def lit(self, it):
        return self.hl is None or self.hl(it)

    def face(self, it):
        svg, p = self.svg, self.pal
        x, y, w, h = self.R(it['u0'], it['z0'], it['u1'], it['z1'])
        if w <= 0.01 or h <= 0.01:
            return
        if not self.lit(it):
            svg.rect(x, y, w, h, fill='#f1f0ed', stroke='#c9c6c0', sw=0.6)
            return
        mat = it['mat']
        svg.rect(x, y, w, h, fill=p.get(mat, '#ccc'))
        cid = svg.clip_rect(x, y, w, h)
        if self.hl is None:
            svg.g(f'clip-path="url(#{cid})"')
            self.texture(mat, it)
            svg.end()
            self.cast_shadows(it, cid)
        svg.rect(x, y, w, h, stroke=p['edge'], sw=0.7)

    def texture(self, mat, it):
        svg, p = self.svg, self.pal
        u0, u1, z0, z1 = it['u0'], it['u1'], it['z0'], it['z1']
        if mat == 'stone':
            z = math.floor(z0 / 2.5) * 2.5 + 2.5
            row = 0
            while z < z1:
                svg.line(self.X(u0), self.Z(z), self.X(u1), self.Z(z), sw=0.5, c=p['stone_j'])
                z += 2.5
            zz = math.floor(z0 / 2.5) * 2.5
            while zz < z1:
                off = 2.5 if int(round(zz / 2.5)) % 2 else 0
                u = math.floor((u0 - off) / 5) * 5 + off
                while u < u1:
                    if u > u0:
                        svg.line(self.X(u), self.Z(max(zz, z0)), self.X(u), self.Z(min(zz + 2.5, z1)), sw=0.5,
                                 c=p['stone_j'])
                    u += 5
                zz += 2.5
                row += 1
        elif mat == 'wood':
            u = math.floor(u0 / 0.5) * 0.5
            while u < u1:
                if u > u0:
                    svg.line(self.X(u), self.Z(z0), self.X(u), self.Z(z1), sw=0.35, c=p['wood_j'])
                u += 0.5
        elif mat == 'bronze':
            u = math.floor(u0 / 3) * 3
            while u < u1:
                if u > u0:
                    svg.line(self.X(u), self.Z(z0), self.X(u), self.Z(z1), sw=0.45, c=p['bronze_j'])
                u += 3
        elif mat == 'green':
            u = u0 + 0.4
            while u < u1:
                self.svg.circle(self.X(u), self.Z(z1 - 0.1), 0.35 * self.s, fill='#93ab73' if self.mode == 'day' else '#5f7449')
                u += 0.9

    def cast_shadows(self, it, cid):
        if not self.shadows:
            return
        polys = []
        for c in self.items:
            if c['k'] != 'face' or not c['cast'] or c is it:
                continue
            if c['d'] >= it['d'] - 0.05:
                continue
            tmax = min(it['d'] - c['d'], 40)
            tmin = max(0.0, it['d'] - c['df'])
            if tmax <= tmin:
                continue
            u0, u1, z0, z1 = c['u0'], c['u1'], c['z0'], c['z1']
            if u1 + tmax < it['u0'] or u0 + tmin > it['u1'] or z1 - tmin < it['z0'] or z0 - tmax > it['z1']:
                continue
            pts = [(u0 + tmin, z1 - tmin), (u1 + tmin, z1 - tmin), (u1 + tmax, z1 - tmax), (u1 + tmax, z0 - tmax),
                   (u0 + tmax, z0 - tmax), (u0 + tmin, z0 - tmin)]
            polys.append([(self.X(a), self.Z(b)) for a, b in pts])
        if polys:
            self.svg.g(f'clip-path="url(#{cid})" opacity="{self.pal["shadow_op"]}"')
            for pts in polys:
                self.svg.poly(pts, fill=self.pal['shadow'])
            self.svg.end()

    def panel(self, it):
        svg, p = self.svg, self.pal
        x, y, w, h = self.R(it['u0'], it['z0'], it['u1'], it['z1'])
        typ = it['typ']
        if not self.lit(it):
            svg.rect(x, y, w, h, fill='#e4eaee', stroke='#bfc6cc', sw=0.6)
            return
        frame = '#2d2824' if self.mode == 'day' else '#1b1714'
        cid = svg.clip_rect(x, y, w, h)
        if typ == 'pivot':
            svg.rect(x, y, w, h, fill='#c79a68' if self.mode == 'day' else '#8e6542')
            uu = it['u0'] + 0.18
            while uu < it['u1']:
                svg.line(self.X(uu), y, self.X(uu), y + h, sw=0.3, c='#a57a4f' if self.mode == 'day' else '#704f33')
                uu += 0.33
            px = self.X(it['u0'] + (it['u1'] - it['u0']) * 0.82)
            svg.rect(px - 0.08 * self.s, self.Z(7.0), 0.16 * self.s, 4 * self.s, fill=frame)
        elif typ == 'garage':
            svg.rect(x, y, w, h, fill=f'url(#{self.g_frost})')
            cols, rows = 6, 4
            for i in range(1, cols):
                svg.line(x + w * i / cols, y, x + w * i / cols, y + h, sw=1.6, c=frame)
            for j in range(1, rows):
                svg.line(x, y + h * j / rows, x + w, y + h * j / rows, sw=1.6, c=frame)
        elif typ == 'door':
            svg.rect(x, y, w, h, fill=p['bronze'])
            svg.rect(x + w * 0.78, y + h * 0.45, w * 0.06, h * 0.12, fill='#8a7a66')
        else:
            svg.rect(x, y, w, h, fill=f'url(#{self.g_glass})')
            if self.interior and typ == 'cw':
                self.lantern_interior(it, cid)
            if self.mode == 'day':
                svg.g(f'clip-path="url(#{cid})"')
                svg.poly([(x + w * 0.15, y), (x + w * 0.42, y), (x + w * 0.05, y + h), (x - w * 0.22, y + h)],
                         fill='#ffffff', op=0.16)
                svg.end()
        self.cast_shadows(it, cid)
        # mullions
        if typ == 'cw':
            for m in LANTERN_CW['mull_u']:
                svg.line(self.X(self.u_cw(m)), y, self.X(self.u_cw(m)), y + h, sw=2.0, c=frame)
            for z0, z1 in LANTERN_CW['spandrels']:
                svg.rect(x, self.Z(z1), w, (z1 - z0) * self.s, fill=p['bronze'])
            svg.line(x, self.Z(10), x + w, self.Z(10), sw=1.6, c=frame)
            svg.line(x, self.Z(32), x + w, self.Z(32), sw=1.6, c=frame)
        elif typ in ('slider', 'fixed', 'win', 'slot'):
            span = it['u1'] - it['u0']
            n = max(1, int(round(span / 5.0))) if typ == 'slider' else max(1, int(round(span / 6.0)))
            if typ == 'slider':
                n = max(2, n)
            for i in range(1, n):
                xx = x + w * i / n
                svg.line(xx, y, xx, y + h, sw=1.8 if typ == 'slider' else 1.3, c=frame)
            if typ == 'slot':
                for z in (11, 22):
                    svg.line(x, self.Z(z), x + w, self.Z(z), sw=1.6, c=frame)
            if typ == 'win' and (it['z1'] - it['z0']) > 4:
                svg.line(x, self.Z(it['z1'] - 2.0), x + w, self.Z(it['z1'] - 2.0), sw=1.0, c=frame)
        svg.rect(x, y, w, h, stroke=frame, sw=1.8 if typ != 'cw' else 2.4)

    def u_cw(self, m):
        return m if self.v == 'front' else -m

    def lantern_interior(self, it, cid):
        """Stair treads seen end-on, bridge slabs and the cascading chandelier behind the lantern glass."""
        if self.v != 'front':
            return
        svg = self.svg
        c = '#3a3632' if self.mode == 'day' else '#7a4a24'
        svg.g(f'clip-path="url(#{cid})" opacity="{0.55 if self.mode == "day" else 0.75}"')
        for lvl in (0, 11):
            for i in range(1, RISERS + 1):
                z = lvl + i * RISER
                svg.line(self.X(ST_X0), self.Z(z), self.X(ST_X1), self.Z(z), sw=1.1, c=c)
                if self.mode == 'dusk':
                    svg.line(self.X(ST_X0), self.Z(z) + 1.2, self.X(ST_X1), self.Z(z) + 1.2, sw=0.8, c='#fff3c4')
        for z in (10.6, 21.6):
            svg.rect(self.X(ST_X0), self.Z(z + 0.4), (8.08 - ST_X0) * self.s, 0.4 * self.s, fill=c)
            svg.line(self.X(8.08), self.Z(z + 0.4), self.X(8.08), self.Z(z + 3.9), sw=0.8, c=c)
            svg.line(self.X(ST_X0), self.Z(z + 3.9), self.X(8.08), self.Z(z + 3.9), sw=0.8, c=c)
        # chandelier strands
        for k, u in enumerate((9.6, 10.4, 11.2, 12.0, 12.8)):
            top, bot = 35.0, 8.0 + (k % 3) * 3.0
            svg.line(self.X(u), self.Z(top), self.X(u), self.Z(bot), sw=0.35, c=c)
            z = top - 2.5 - k * 0.7
            while z > bot:
                svg.circle(self.X(u), self.Z(z), 0.42 * self.s, stroke='#fff7dc' if self.mode == 'dusk' else '#f4f2ea',
                           sw=1.4)
                z -= 2.6
        svg.end()

    def rail(self, it):
        svg = self.svg
        x, y, w, h = self.R(it['u0'], it['z0'], it['u1'], it['z1'])
        if not self.lit(it):
            svg.rect(x, y, w, h, fill='#eef3f5', op=0.6, stroke='#c5ccd0', sw=0.4)
            return
        svg.rect(x, y, w, h, fill=f'url(#{self.g_rail})')
        frame = '#2d2824' if self.mode == 'day' else '#1b1714'
        svg.line(x, y, x + w, y, sw=0.8, c='#7f8c93')
        svg.rect(x, y + h - 0.35 * self.s, w, 0.35 * self.s, fill=frame)

    def lights(self):
        """Dusk extras: LED soffit coves, sconces and uplights."""
        svg = self.svg
        glow = svg.uid('f')
        svg.defs.append(f'<filter id="{glow}" x="-50%" y="-50%" width="200%" height="200%">'
                        f'<feGaussianBlur stdDeviation="{0.35 * self.s}"/></filter>')
        lines = []
        if self.v == 'front':
            lines = [(14, 48.75, 21.0), (14, 50, 32.0), (2.5, 11.5, 9.5)]
            spots = [(14.6, 7.0), (27.6, 7.0), (49.2, 7.0)]
        elif self.v == 'rear':
            lines = [(-50, 0, 10.0), (-50, 0, 32.0)]
            spots = []
        else:
            spots = []
        for u0, u1, z in lines:
            svg.add(f'<line x1="{self.X(u0):.1f}" y1="{self.Z(z) + 1.8:.1f}" x2="{self.X(u1):.1f}" y2="{self.Z(z) + 1.8:.1f}" '
                    f'stroke="#ffcf8a" stroke-width="{0.5 * self.s:.1f}" filter="url(#{glow})" opacity="0.95"/>')
            svg.line(self.X(u0), self.Z(z) + 1.0, self.X(u1), self.Z(z) + 1.0, sw=1.4, c='#fff4dc')
        for u, z in spots:
            svg.add(f'<ellipse cx="{self.X(u):.1f}" cy="{self.Z(z):.1f}" rx="{0.45 * self.s:.1f}" ry="{2.6 * self.s:.1f}" '
                    f'fill="#ffd79a" filter="url(#{glow})" opacity="0.9"/>')
            svg.rect(self.X(u) - 0.18 * self.s, self.Z(z + 0.4), 0.36 * self.s, 0.8 * self.s, fill='#1b1714')

    # ------------------------------------------------------------ notes
    def grade(self, extend=6, c=INK):
        svg = self.svg
        svg.line(self.X(self.umin - extend), self.Z(GRADE), self.X(self.umax + extend), self.Z(GRADE), sw=2.6, c=c)

    def datums(self, right_pad=3.0, items=None):
        svg = self.svg
        items = items or [(LANTERN_TOP, 'T.O. LANTERN', "+37'-0\""), (PARAPET, 'T.O. PARAPET', "+34'-6\""),
                          (ROOF, 'ROOF', "+33'-0\""), (LV[3], 'LEVEL 3 F.F.', "+22'-0\""),
                          (LV[2], 'LEVEL 2 F.F.', "+11'-0\""), (LV[1], 'LEVEL 1 F.F.', "+0'-0\""),
                          (GRADE, 'AVG. GRADE', "-0'-8\"")]
        x0 = self.X(self.umax + 0.8)
        x1 = self.X(self.umax + right_pad)
        last_y = None
        for z, label, val in items:
            y = self.Z(z)
            svg.line(x0, y, x1, y, sw=0.5, dash='8 3', c='#555')
            r = 7
            svg.circle(x1 + r, y, r, fill='#fff', stroke=INK, sw=0.9)
            svg.path(f'M {x1:.1f} {y:.1f} A {r} {r} 0 0 1 {x1 + r:.1f} {y - r:.1f} L {x1 + r:.1f} {y:.1f} Z', fill=INK)
            svg.path(f'M {x1 + r:.1f} {y:.1f} A {r} {r} 0 0 1 {x1 + 2 * r:.1f} {y + r:.1f} L {x1 + r:.1f} {y:.1f} Z', fill=INK)
            ty = y - 3 if last_y is None or abs(last_y - y) > 24 else y + 10
            svg.text(x1 + 2 * r + 6, ty, label, size=8, weight=700)
            svg.text(x1 + 2 * r + 6, ty + 10, val, size=8, fill='#555')
            last_y = y

    def keynote(self, x, y, z, n):
        tag(self.svg, self.X(self.u_of(x, y)), self.Z(z), str(n), shape='hex', size=8, r=10.5)


# ================================================================ sections
POCHE = '#1f1f1d'


def sect_rect(svg, X, Z, u0, z0, u1, z1, fill=POCHE, stroke=None, sw=0.6, op=None):
    svg.rect(X(min(u0, u1)), Z(max(z0, z1)), abs(u1 - u0) * (X(1) - X(0)), abs(z1 - z0) * (Z(0) - Z(1)), fill=fill,
             stroke=stroke, sw=sw, op=op)


def earth(svg, X, Z, u0, u1, depth=-6.0):
    sect_rect(svg, X, Z, u0, depth, u1, GRADE, fill='#f1ede6')
    u = u0
    while u < u1:
        svg.line(X(u), Z(GRADE - 0.3), X(u + 1.6), Z(GRADE - 1.9), sw=0.4, c='#b9b0a2')
        svg.line(X(u + 0.8), Z(GRADE - 2.6), X(u + 2.4), Z(GRADE - 4.2), sw=0.4, c='#b9b0a2')
        u += 2.0


def glass_cut(svg, X, Z, u0, u1, z0, z1):
    sect_rect(svg, X, Z, u0, z0, u1, z1, fill='#dfeaf0', stroke=INK, sw=0.6)


def beyond_window(svg, X, Z, u0, u1, z0, z1, mull=0):
    sect_rect(svg, X, Z, u0, z0, u1, z1, fill='#eef3f6', stroke='#8b8b8b', sw=0.6)
    for i in range(1, mull + 1):
        uu = u0 + (u1 - u0) * i / (mull + 1)
        svg.line(X(uu), Z(z0), X(uu), Z(z1), sw=0.6, c='#8b8b8b')
    svg.line(X(u0 + (u1 - u0) * 0.2), Z(z1 - (z1 - z0) * 0.15), X(u0 + (u1 - u0) * 0.35), Z(z1 - (z1 - z0) * 0.4),
             sw=0.4, c='#9fb4c2')


def slab(svg, X, Z, u0, u1, z0, z1):
    sect_rect(svg, X, Z, u0, z0, u1, z1)


def room_tag(svg, X, Z, u, z, name, size=9):
    svg.text(X(u), Z(z), name, size=size, weight=700, anchor='middle', ls=0.6, fill='#333')


def section_a(svg, left, base, s):
    """Longitudinal section at X = 6'-3" looking toward the left (west) wall. u = Y."""
    X = lambda u: left + (u + 6) * s  # noqa: E731
    Z = lambda z: base - z * s  # noqa: E731
    earth(svg, X, Z, -6, 92)
    # pool cut (pool spans X 5..35 in house coords, Y 69..83)
    sect_rect(svg, X, Z, 69, -5.2, 83, GRADE, fill='#fff')
    sect_rect(svg, X, Z, 69.6, -4.6, 82.4, GRADE - 0.4, fill='#cfe3ec')
    for (a, b) in ((68.4, 69.6), (82.4, 83.6)):
        sect_rect(svg, X, Z, a, -5.2, b, GRADE)
    sect_rect(svg, X, Z, 69.6, -5.2, 82.4, -4.6)
    svg.text(X(76), Z(-2.6), 'POOL', size=8, weight=700, anchor='middle', fill='#2e5d73')
    # paving
    sect_rect(svg, X, Z, -6, GRADE, 0, GRADE + 0.25, fill='#d9d3c8', stroke=INK, sw=0.5)
    sect_rect(svg, X, Z, 54, GRADE, 69, GRADE + 0.33, fill='#d9d3c8', stroke=INK, sw=0.5)
    sect_rect(svg, X, Z, 83, GRADE, 92, GRADE + 0.33, fill='#d9d3c8', stroke=INK, sw=0.5)
    # beyond: left wall openings, fireplace, stair, columns
    for o in EXT_OPS:
        if o['o'] == 'v' and o['c'] == 0:
            beyond_window(svg, X, Z, o['a'], o['b'], o['z0'], o['z1'], mull=1 if o['b'] - o['a'] > 6 else 0)
    sect_rect(svg, X, Z, 37, 0, 45, 2.2, fill='#d8d1c6', stroke='#777', sw=0.6)
    sect_rect(svg, X, Z, 38.5, 0.6, 43.5, 1.8, fill='#3a3530')
    sect_rect(svg, X, Z, 37.5, 3.6, 44.5, 7.4, fill='#2d2a27', op=0.85)
    sect_rect(svg, X, Z, 65.33, 0, 66, 10, fill='#5a524b')
    for base_z in (0, 11):
        prof = [(X(ST_Y0), Z(base_z))]
        for i in range(RISERS):
            y0 = ST_Y0 + i * TREAD
            z = base_z + (i + 1) * RISER
            prof += [(X(y0), Z(z)), (X(min(y0 + TREAD, ST_Y1)), Z(z))]
        svg.poly(prof, close=False, stroke='#55504a', sw=1.0)
        svg.line(X(ST_Y0), Z(base_z - 0.6 + RISER), X(ST_Y1), Z(base_z + 11 - 0.7), sw=0.8, c='#55504a')
        svg.line(X(ST_Y0), Z(base_z + 3.0), X(ST_Y1), Z(base_z + 14.0), sw=0.6, c='#7d97a6')
    sect_rect(svg, X, Z, 12, 0, ST_Y1, 6.2, fill='#f4efe6', stroke='#8b8b8b', sw=0.5)
    svg.text(X(15.8), Z(2.5), 'WINE', size=6.5, anchor='middle', fill='#666')
    # chandelier hint (beyond is behind the viewer; show dashed outline per convention)
    # cut: ground slab + foundations
    slab(svg, X, Z, -0.5, 54, -0.5, 0)
    for u in (-0.5, 53.0):
        sect_rect(svg, X, Z, u, -2.8, u + 1.5, -0.5)
        sect_rect(svg, X, Z, u + 0.4, -6.0, u + 1.1, -2.8, fill='#fff', stroke=INK, sw=0.6)
    # level 2
    slab(svg, X, Z, 0.33, ST_Y0, 10.0, 11.0)
    sect_rect(svg, X, Z, ST_Y0, 10.55, ST_Y1, 11.0, fill='#55504a')
    svg.line(X(ST_Y0), Z(14.5), X(ST_Y1), Z(14.5), sw=0.6, c='#5b8aa3')
    slab(svg, X, Z, ST_Y1, 54, 10.0, 11.0)
    slab(svg, X, Z, 54, 66, 10.0, 11.0)
    sect_rect(svg, X, Z, 60, 11.0, 66, 11.6, fill='#93ab73')
    sect_rect(svg, X, Z, 65.5, 11, 66, 11.9)
    glass_cut(svg, X, Z, 59.9, 60.1, 11, 14.5)
    # level 3
    slab(svg, X, Z, ST_Y1, 54, 21.0, 22.0)
    glass_cut(svg, X, Z, 53.65, 53.85, 22, 25.5)
    glass_cut(svg, X, Z, ST_Y1 - 0.1, ST_Y1 + 0.1, 22, 25.5)
    # roof
    slab(svg, X, Z, 24, 50, 32.0, 33.0)
    sect_rect(svg, X, Z, 49.3, 32.0, 50, PARAPET)
    sect_rect(svg, X, Z, 23.6, 32.0, 24.0, 35.5)
    slab(svg, X, Z, -1.5, 24, 35.5, 36.5)
    sect_rect(svg, X, Z, -1.5, 35.5, 0, LANTERN_TOP)
    sect_rect(svg, X, Z, 23.6, 36.5, 24, LANTERN_TOP)
    # front curtain wall + pivot door + canopy
    glass_cut(svg, X, Z, 0, 0.33, 10, 35.5)
    sect_rect(svg, X, Z, 0, 0, 0.33, 10, fill='#c79a68', stroke=INK, sw=0.6)
    sect_rect(svg, X, Z, -5, 9.5, 0, 10)
    # walls cut on levels 2 & 3 (constant-Y walls crossing X = 6.25)
    for lvl in (2, 3):
        for w in WALLS[lvl]:
            if w['o'] != 'h' or w['k'] not in ('ext', 'int') or not (w['a'] <= 6.25 <= w['b']):
                continue
            ff = LV[lvl]
            u0, u1 = w['c'] - w['t'] / 2, w['c'] + w['t'] / 2
            ops = [o for o in EXT_OPS if o['o'] == 'h' and abs(o['c'] - w['c']) < 0.6 and o['a'] <= 6.25 <= o['b']
                   and o['lvl'] == lvl]
            if ops:
                o = ops[0]
                if o['z0'] > ff:
                    sect_rect(svg, X, Z, u0, ff, u1, o['z0'])
                glass_cut(svg, X, Z, u0 + 0.2, u1 - 0.2, o['z0'], o['z1'])
                if o['z1'] < ff + 10:
                    sect_rect(svg, X, Z, u0, o['z1'], u1, ff + 10)
            elif w['c'] > 50:
                glass_cut(svg, X, Z, u0 + 0.2, u1 - 0.2, ff, ff + 10)
            else:
                sect_rect(svg, X, Z, u0, ff, u1, ff + 10)
    glass_cut(svg, X, Z, 53.45, 53.65, 0, 10)
    # labels
    room_tag(svg, X, Z, 9.5, 30.0, 'STAIR LANTERN', 9)
    svg.text(X(9.5), Z(28.8), 'TRIPLE HEIGHT · 35\'-6"', size=7, anchor='middle', fill='#555')
    room_tag(svg, X, Z, 9.0, 6.0, 'FOYER')
    room_tag(svg, X, Z, 31, 5.0, 'LIVING')
    room_tag(svg, X, Z, 60, 4.0, 'LOGGIA')
    room_tag(svg, X, Z, 21.8, 15.5, 'HALL', 8)
    room_tag(svg, X, Z, 32.0, 15.5, 'BATH 2', 8)
    room_tag(svg, X, Z, 38.3, 15.5, 'WIC', 8)
    room_tag(svg, X, Z, 47.2, 15.5, 'BEDROOM 2', 8)
    room_tag(svg, X, Z, 57, 15.5, 'TERRACE', 7.5)
    room_tag(svg, X, Z, 21.8, 26.5, 'LANDING', 8)
    room_tag(svg, X, Z, 37, 26.5, 'DRESSING ROOM', 8.5)
    room_tag(svg, X, Z, 50.0, 26.5, 'PRIMARY TERRACE', 7.5)
    return X, Z


def section_b(svg, left, base, s):
    """Transverse section at Y = 43'-0" looking toward the garden. u = X."""
    X = lambda u: left + (u + 6) * s  # noqa: E731
    Z = lambda z: base - z * s  # noqa: E731
    earth(svg, X, Z, -6, 56)
    # beyond: rear walls and openings
    sect_rect(svg, X, Z, 0, 0, 50, 10, fill='#faf8f4', stroke='#9a9a9a', sw=0.5)
    sect_rect(svg, X, Z, 0, 11, 50, 21, fill='#faf8f4', stroke='#9a9a9a', sw=0.5)
    sect_rect(svg, X, Z, 0, 22, 50, 32, fill='#faf8f4', stroke='#9a9a9a', sw=0.5)
    for o in EXT_OPS:
        if o['o'] == 'h' and o['c'] in (54, 46):
            n = max(1, int(round((o['b'] - o['a']) / 5))) - 1 if o['typ'] == 'slider' else 0
            beyond_window(svg, X, Z, o['a'], o['b'], o['z0'], o['z1'], mull=max(n, 0))
    # cut: slabs
    slab(svg, X, Z, -0.2, 50.2, -0.5, 0)
    for u in (-0.5, 49.0):
        sect_rect(svg, X, Z, u, -2.8, u + 1.5, -0.5)
        sect_rect(svg, X, Z, u + 0.4, -6.0, u + 1.1, -2.8, fill='#fff', stroke=INK, sw=0.6)
    slab(svg, X, Z, 0, 50, 10, 11)
    slab(svg, X, Z, 0, 50, 21, 22)
    slab(svg, X, Z, 0, 50, 32, 33)
    sect_rect(svg, X, Z, 0, 33, 0.75, PARAPET)
    sect_rect(svg, X, Z, 49.25, 33, 50, PARAPET)
    # exterior walls with openings at Y = 43
    def ext_wall(u0, u1, lvl, side_c):
        ff = LV[lvl]
        top = ff + 10
        ops = [o for o in EXT_OPS if o['o'] == 'v' and o['c'] == side_c and o['lvl'] == lvl and o['a'] <= 43 <= o['b']]
        if ops:
            o = ops[0]
            if o['z0'] > ff:
                sect_rect(svg, X, Z, u0, ff, u1, o['z0'])
            glass_cut(svg, X, Z, u0 + 0.25, u1 - 0.25, o['z0'], o['z1'])
            if o['z1'] < top:
                sect_rect(svg, X, Z, u0, o['z1'], u1, top)
        else:
            sect_rect(svg, X, Z, u0, ff, u1, top)
    for lvl in (1, 2, 3):
        ext_wall(0, 0.75, lvl, 0)
        ext_wall(49.25, 50, lvl, 50)
    for x in (12.5, 25, 37.5):
        sect_rect(svg, X, Z, x - 0.25, 11, x + 0.25, 21)
    for x in (14, 36):
        sect_rect(svg, X, Z, x - 0.21, 22, x + 0.21, 32)
    # cut furniture / millwork
    sect_rect(svg, X, Z, 0.75, 0, 2.0, 2.4, fill='#d8d1c6', stroke=INK, sw=0.6)
    sect_rect(svg, X, Z, 33, 0, 45, 3.0, fill='#e9e3d8', stroke=INK, sw=0.8)
    sect_rect(svg, X, Z, 33, 2.85, 45, 3.15, fill='#f4f1ea', stroke=INK, sw=0.6)
    sect_rect(svg, X, Z, 47.25, 0, 49.25, 8.5, fill='#e9e3d8', stroke=INK, sw=0.8)
    for k in range(4):
        cx = 12.5 * k + 6.25
        sect_rect(svg, X, Z, cx - 2.67, 11, cx + 2.67, 12.9, fill='#efeae2', stroke='#777', sw=0.6)
    sect_rect(svg, X, Z, 38.6, 22, 44.6, 24.0, fill='#fff', stroke=INK, sw=0.8)
    # pendants & ceiling lines
    for u in (36, 39, 42):
        svg.line(X(u), Z(10), X(u), Z(7.0), sw=0.5, c='#777')
        svg.circle(X(u), Z(6.8), 0.45 * s, fill='#d8c3a5', stroke='#777', sw=0.5)
    room_tag(svg, X, Z, 8.5, 5.5, 'LIVING')
    room_tag(svg, X, Z, 22.0, 5.5, 'DINING')
    room_tag(svg, X, Z, 39.0, 5.5, 'KITCHEN')
    for k in range(4):
        room_tag(svg, X, Z, 12.5 * k + 6.25, 16.0, f'BEDROOM {k + 2}', 8)
    room_tag(svg, X, Z, 7.0, 26.5, 'DRESSING', 8.5)
    room_tag(svg, X, Z, 25.0, 26.5, 'PRIMARY BEDROOM', 8.5)
    room_tag(svg, X, Z, 43.0, 26.5, 'SPA BATH', 8.5)
    return X, Z


def sect_datums(svg, X, Z, u_right, items=None):
    items = items or [(LANTERN_TOP, 'T.O. LANTERN', "+37'-0\""), (PARAPET, 'T.O. PARAPET', "+34'-6\""),
                      (ROOF, 'ROOF', "+33'-0\""), (LV[3], 'LEVEL 3', "+22'-0\""), (LV[2], 'LEVEL 2', "+11'-0\""),
                      (LV[1], 'LEVEL 1', "+0'-0\"")]
    x0, x1 = X(u_right + 1), X(u_right + 4)
    for z, label, val in items:
        y = Z(z)
        svg.line(x0, y, x1, y, sw=0.5, dash='8 3', c='#555')
        svg.circle(x1 + 7, y, 7, fill='#fff', stroke=INK, sw=0.9)
        svg.path(f'M {x1:.1f} {y:.1f} A 7 7 0 0 1 {x1 + 7:.1f} {y - 7:.1f} L {x1 + 7:.1f} {y:.1f} Z', fill=INK)
        svg.path(f'M {x1 + 7:.1f} {y:.1f} A 7 7 0 0 1 {x1 + 14:.1f} {y + 7:.1f} L {x1 + 7:.1f} {y:.1f} Z', fill=INK)
        svg.text(x1 + 20, y - 2, label, size=8, weight=700)
        svg.text(x1 + 20, y + 8, val, size=8, fill='#555')
