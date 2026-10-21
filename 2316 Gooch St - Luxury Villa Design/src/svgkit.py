"""Minimal SVG writer plus the drafting conventions shared by every sheet."""
import math

INK = '#1d1d1b'
FURN = '#7a756d'
SOFT = '#a9a399'
BRONZE = '#6e5338'


def fi(v):
    """Feet to architectural text, e.g. 12'-6"."""
    neg = v < -1e-6
    t = int(round(abs(v) * 12))
    f, i = divmod(t, 12)
    return ('-' if neg else '') + f"{f}'-{i}\""


def num(v):
    s = ('%.2f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class Svg:
    """A 36" x 24" sheet drawn in hundredths of an inch (viewBox 3600 x 2400)."""

    def __init__(self, prefix, w=3600, h=2400):
        self.prefix, self.w, self.h = prefix, w, h
        self.defs, self.body, self._n = [], [], 0

    def uid(self, p='u'):
        self._n += 1
        return f'{self.prefix}{p}{self._n}'

    def add(self, s):
        self.body.append(s)

    @staticmethod
    def _st(fill='none', stroke=None, sw=1, dash=None, op=None, cap=None, join=None, extra=''):
        a = f' fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{num(sw)}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if op is not None:
            a += f' opacity="{num(op)}"'
        if cap:
            a += f' stroke-linecap="{cap}"'
        if join:
            a += f' stroke-linejoin="{join}"'
        return a + extra

    def line(self, x1, y1, x2, y2, sw=1, c=INK, dash=None, op=None, cap='butt'):
        self.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}"'
                 + self._st('none', c, sw, dash, op, cap) + '/>')

    def rect(self, x, y, w, h, fill='none', stroke=None, sw=1, dash=None, op=None, rx=0, extra=''):
        if w < 0:
            x, w = x + w, -w
        if h < 0:
            y, h = y + h, -h
        r = f' rx="{num(rx)}"' if rx else ''
        self.add(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}"{r}'
                 + self._st(fill, stroke, sw, dash, op, extra=extra) + '/>')

    def poly(self, pts, fill='none', stroke=None, sw=1, dash=None, op=None, close=True, join='miter', extra=''):
        d = ' '.join(f'{num(x)},{num(y)}' for x, y in pts)
        tag = 'polygon' if close else 'polyline'
        self.add(f'<{tag} points="{d}"' + self._st(fill, stroke, sw, dash, op, join=join, extra=extra) + '/>')

    def circle(self, cx, cy, r, fill='none', stroke=None, sw=1, dash=None, op=None):
        self.add(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(r)}"' + self._st(fill, stroke, sw, dash, op) + '/>')

    def ellipse(self, cx, cy, rx, ry, fill='none', stroke=None, sw=1, op=None):
        self.add(f'<ellipse cx="{num(cx)}" cy="{num(cy)}" rx="{num(rx)}" ry="{num(ry)}"'
                 + self._st(fill, stroke, sw, None, op) + '/>')

    def path(self, d, fill='none', stroke=None, sw=1, dash=None, op=None, cap=None, extra=''):
        self.add(f'<path d="{d}"' + self._st(fill, stroke, sw, dash, op, cap, extra=extra) + '/>')

    def text(self, x, y, s, size=10, weight=400, anchor='start', fill=INK, rot=0, ls=0, op=None, style=None,
             family='Inter'):
        t = f' transform="rotate({num(rot)} {num(x)} {num(y)})"' if rot else ''
        l_ = f' letter-spacing="{num(ls)}"' if ls else ''
        o = f' opacity="{num(op)}"' if op is not None else ''
        st = f' font-style="{style}"' if style else ''
        self.add(f'<text x="{num(x)}" y="{num(y)}" font-family="{family}" font-size="{num(size)}" '
                 f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}"{t}{l_}{o}{st}>{esc(s)}</text>')

    def g(self, attrs=''):
        self.add(f'<g {attrs}>')

    def end(self):
        self.add('</g>')

    def clip_rect(self, x, y, w, h):
        cid = self.uid('c')
        if w < 0:
            x, w = x + w, -w
        if h < 0:
            y, h = y + h, -h
        self.defs.append(f'<clipPath id="{cid}"><rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}"/></clipPath>')
        return cid

    def lin_grad(self, stops, x2=0, y2=1):
        gid = self.uid('g')
        s = ''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a is not None else '') + '/>'
                    for o, c, a in stops)
        self.defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>')
        return gid

    def render(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="36in" height="24in" viewBox="0 0 {self.w} {self.h}">'
                f'<defs>{"".join(self.defs)}</defs><rect width="{self.w}" height="{self.h}" fill="#ffffff"/>'
                f'{"".join(self.body)}</svg>')


class PT:
    """Plan transform: model feet (Y toward the rear) to sheet units (y down)."""

    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s = ox, oy, s

    def x(self, X):
        return self.ox + X * self.s

    def y(self, Y):
        return self.oy - Y * self.s

    def p(self, X, Y):
        return self.ox + X * self.s, self.oy - Y * self.s

    def L(self, v):
        return v * self.s

    def rect(self, svg, x0, y0, x1, y1, **kw):
        svg.rect(self.x(min(x0, x1)), self.y(max(y0, y1)), abs(x1 - x0) * self.s, abs(y1 - y0) * self.s, **kw)

    def line(self, svg, x0, y0, x1, y1, **kw):
        svg.line(*self.p(x0, y0), *self.p(x1, y1), **kw)

    def poly(self, svg, pts, **kw):
        svg.poly([self.p(x, y) for x, y in pts], **kw)

    def circle(self, svg, cx, cy, r, **kw):
        svg.circle(*self.p(cx, cy), r * self.s, **kw)


class Fr:
    """Local frame for furniture: origin at (cx, cy), rotated so local -y points 'toward'."""
    ROT = {'S': 0, 'E': 90, 'N': 180, 'W': 270}

    def __init__(self, T, cx, cy, toward='S'):
        self.T, self.cx, self.cy = T, cx, cy
        r = math.radians(self.ROT[toward])
        self.c, self.s = math.cos(r), math.sin(r)

    def p(self, lx, ly):
        X = self.cx + lx * self.c - ly * self.s
        Y = self.cy + lx * self.s + ly * self.c
        return self.T.p(X, Y)

    def rect(self, svg, x0, y0, x1, y1, **kw):
        svg.poly([self.p(x0, y0), self.p(x1, y0), self.p(x1, y1), self.p(x0, y1)], **kw)

    def line(self, svg, x0, y0, x1, y1, **kw):
        svg.line(*self.p(x0, y0), *self.p(x1, y1), **kw)

    def circle(self, svg, x, y, r, **kw):
        svg.circle(*self.p(x, y), r * self.T.s, **kw)


# ----------------------------------------------------------- annotations
def north_arrow(svg, x, y, r=46, label='PLAN NORTH'):
    svg.circle(x, y, r, stroke=INK, sw=1.4)
    svg.poly([(x, y - r * 0.92), (x + r * 0.32, y + r * 0.45), (x, y + r * 0.22)], fill=INK)
    svg.poly([(x, y - r * 0.92), (x - r * 0.32, y + r * 0.45), (x, y + r * 0.22)], fill='#fff', stroke=INK, sw=1)
    svg.text(x, y - r - 10, 'N', size=18, weight=700, anchor='middle')
    svg.text(x, y + r + 20, label, size=8.5, weight=600, anchor='middle', ls=1)
    svg.text(x, y + r + 32, 'TRUE NORTH PER SURVEY', size=7, anchor='middle', fill='#666', ls=0.5)


def scale_bar(svg, x, y, s, feet=(0, 4, 8, 16), label=None):
    """Graphic scale: s = sheet units per foot."""
    total = feet[-1]
    for i in range(len(feet) - 1):
        a, b = feet[i], feet[i + 1]
        svg.rect(x + a * s, y, (b - a) * s, 7, fill=INK if i % 2 == 0 else '#fff', stroke=INK, sw=0.8)
    for f in feet:
        svg.text(x + f * s, y + 20, f"{f}'", size=8, anchor='middle')
    if label:
        svg.text(x + total * s + 14, y + 7, label, size=8, fill='#555')


def drawing_title(svg, x, y, num_, title, scale, width=None):
    """Circle-number title used under every drawing."""
    svg.circle(x + 26, y, 24, stroke=INK, sw=1.6)
    svg.line(x + 2, y, x + 50, y, sw=1)
    svg.text(x + 26, y - 5, num_, size=14, weight=700, anchor='middle')
    svg.text(x + 64, y - 2, title, size=17, weight=700, ls=1.2)
    svg.text(x + 64, y + 18, scale, size=10, fill='#555', ls=0.6)
    if width:
        svg.line(x + 64, y + 4, x + 64 + width, y + 4, sw=1.2)


def tag(svg, x, y, text, shape='hex', size=8, r=11, fill='#fff', stroke=INK):
    if shape == 'hex':
        pts = [(x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))) for a in range(0, 360, 60)]
        svg.poly(pts, fill=fill, stroke=stroke, sw=0.9)
    elif shape == 'circle':
        svg.circle(x, y, r, fill=fill, stroke=stroke, sw=0.9)
    elif shape == 'box':
        svg.rect(x - r * 1.25, y - r * 0.75, r * 2.5, r * 1.5, fill=fill, stroke=stroke, sw=0.9, rx=2)
    elif shape == 'diamond':
        svg.poly([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=fill, stroke=stroke, sw=0.9)
    svg.text(x, y + size * 0.36, text, size=size, weight=600, anchor='middle')


def wrap(text, width_chars):
    words, lines, cur = text.split(), [], ''
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > width_chars:
            lines.append(cur)
            cur = w
        else:
            cur = f'{cur} {w}' if cur else w
    if cur:
        lines.append(cur)
    return lines


def para(svg, x, y, text, size=10, width_chars=80, lead=1.45, **kw):
    lines = wrap(text, width_chars)
    for i, ln in enumerate(lines):
        svg.text(x, y + i * size * lead, ln, size=size, **kw)
    return y + len(lines) * size * lead
