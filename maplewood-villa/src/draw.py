"""Tiny SVG plan-drawing kit. All coordinates are in feet.

Plans are drawn street-side down: x runs left to right across the lot,
y runs from the rear wall (0) toward the street.
"""
import math

EXT = 0.5   # exterior stud wall, 6"
INT = 0.4   # interior partition, ~4.75"
FDN = 0.67  # foundation wall, 8"


def ftin(v):
    """10.82 -> 10'-10\""""
    inches = round(v * 12)
    f, i = divmod(inches, 12)
    return f"{f}'-{i}\""


class Sheet:
    def __init__(self):
        self.layers = {k: [] for k in
                       ("floor", "under", "fixture", "furn", "wall", "open", "dim", "label", "note")}

    # ---------- primitives ----------
    def add(self, layer, s):
        self.layers[layer].append(s)

    def rect(self, x, y, w, h, cls, layer="fixture", rx=0):
        r = f' rx="{rx:.3f}"' if rx else ""
        self.add(layer, f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}"{r} class="{cls}"/>')

    def line(self, x1, y1, x2, y2, cls, layer="fixture"):
        self.add(layer, f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" class="{cls}"/>')

    def poly(self, pts, cls, layer="fixture", closed=False):
        p = " ".join(f"{x:.3f},{y:.3f}" for x, y in pts)
        tag = "polygon" if closed else "polyline"
        self.add(layer, f'<{tag} points="{p}" class="{cls}"/>')

    def circle(self, cx, cy, r, cls, layer="fixture"):
        self.add(layer, f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}" class="{cls}"/>')

    def ellipse(self, cx, cy, rx, ry, cls, layer="fixture"):
        self.add(layer, f'<ellipse cx="{cx:.3f}" cy="{cy:.3f}" rx="{rx:.3f}" ry="{ry:.3f}" class="{cls}"/>')

    def text(self, x, y, s, cls, layer="label", anchor="middle", rot=0):
        t = f' transform="rotate({rot} {x:.3f} {y:.3f})"' if rot else ""
        self.add(layer, f'<text x="{x:.3f}" y="{y:.3f}" text-anchor="{anchor}" class="{cls}"{t}>{s}</text>')

    def arc(self, cx, cy, r, a0, a1, cls="swing", layer="open", n=18):
        pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
                cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
        self.poly(pts, cls, layer)

    # ---------- walls ----------
    def hwall(self, y, x1, x2, t=INT, ops=(), cls="wall"):
        self._wall("h", y, x1, x2, t, ops, cls)

    def vwall(self, x, y1, y2, t=INT, ops=(), cls="wall"):
        self._wall("v", x, y1, y2, t, ops, cls)

    def _wall(self, o, c, a0, a1, t, ops, cls):
        ops = sorted(ops, key=lambda op: op[1])
        cur = a0
        for op in ops:
            if op[1] > cur:
                self._seg(o, c, cur, op[1], t, cls)
            self._opening(o, c, t, op)
            cur = max(cur, op[2])
        if a1 > cur:
            self._seg(o, c, cur, a1, t, cls)

    def _seg(self, o, c, a, b, t, cls):
        if o == "h":
            self.rect(a, c - t / 2, b - a, t, cls, "wall")
        else:
            self.rect(c - t / 2, a, t, b - a, cls, "wall")

    def _xy(self, o, along, across):
        return (along, across) if o == "h" else (across, along)

    def _opening(self, o, c, t, op):
        kind, a, b = op[0], op[1], op[2]
        opt = op[3] if len(op) > 3 else {}
        lo, hi = c - t / 2, c + t / 2
        X = lambda al, ac: self._xy(o, al, ac)
        if kind in ("win", "fixed"):
            p = [X(a, lo), X(b, lo), X(b, hi), X(a, hi)]
            self.poly(p, "winframe", "open", closed=True)
            for f in (0.38, 0.62):
                self.line(*X(a, lo + t * f), *X(b, lo + t * f), "glass", "open")
            for m in opt.get("mullions", []):
                self.line(*X(m, lo), *X(m, hi), "mullion", "open")
        elif kind == "slide":
            mid = (a + b) / 2
            p = [X(a, lo), X(b, lo), X(b, hi), X(a, hi)]
            self.poly(p, "winframe", "open", closed=True)
            panels = opt.get("panels", 2)
            step = (b - a) / panels
            for k in range(panels):
                off = lo + t * (0.33 if k % 2 == 0 else 0.67)
                self.line(*X(a + k * step - (0.15 if k else 0), off), *X(a + (k + 1) * step + (0.15 if k < panels - 1 else 0), off), "glass2", "open")
        elif kind == "door":
            hinge = opt.get("hinge", "a")
            side = opt.get("side", 1)
            w = b - a
            face = hi if side > 0 else lo
            hx = a if hinge == "a" else b
            other = b if hinge == "a" else a
            self.line(*X(hx, face), *X(hx, face + side * w), "leaf", "open")
            self._swing(o, hx, face, other, side, w)
            self.line(*X(a, lo), *X(b, lo), "jamb", "open")
            self.line(*X(a, hi), *X(b, hi), "jamb", "open")
        elif kind == "dbl":
            side = opt.get("side", 1)
            w = (b - a) / 2
            face = hi if side > 0 else lo
            for hx, other in ((a, a + w), (b, b - w)):
                self.line(*X(hx, face), *X(hx, face + side * w), "leaf", "open")
                self._swing(o, hx, face, other, side, w)
            self.line(*X(a, lo), *X(b, lo), "jamb", "open")
            self.line(*X(a, hi), *X(b, hi), "jamb", "open")
        elif kind == "pocket":
            self.line(*X(a, c), *X(b, c), "pocketln", "open")
        elif kind == "garage":
            self.line(*X(a, c), *X(b, c), "garageln", "open")
            for e in (a, b):
                self.line(*X(e, lo - 0.6), *X(e, hi + 0.6), "thin", "open")
        elif kind == "open":
            if opt.get("cased"):
                self.line(*X(a, lo), *X(a, hi), "thin", "open")
                self.line(*X(b, lo), *X(b, hi), "thin", "open")

    def _swing(self, o, hx, face, other, side, w):
        # Arc centred on the hinge from the closed position (along wall) to open (perpendicular).
        if o == "h":
            a_closed = 0 if other > hx else 180
            a_open = 90 if side > 0 else -90
            cx, cy = hx, face
        else:
            a_closed = 90 if other > hx else -90
            a_open = 0 if side > 0 else 180
            cx, cy = face, hx
        a0, a1 = a_closed, a_open
        if abs(a1 - a0) > 180:
            a1 += 360 if a1 < a0 else -360
        self.arc(cx, cy, w, a0, a1)

    # ---------- composite symbols ----------
    def label(self, x, y, name, dims=None, sub=None, size=1.0):
        lines = name.split("|")
        dy = 0.95 * size
        y0 = y - (len(lines) - 1) * dy / 2 - (0.45 * size if dims else 0)
        for k, ln in enumerate(lines):
            self.text(x, y0 + k * dy, ln, "rname" if size >= 1 else "rname sm")
        if dims:
            self.text(x, y0 + (len(lines) - 1) * dy + 1.0 * size, dims, "rdim" if size >= 1 else "rdim sm")
        if sub:
            self.text(x, y0 + (len(lines) - 1) * dy + (1.95 if dims else 1.0) * size, sub, "rsub")

    def toilet(self, x, y, rot=0):
        g = f'<g transform="translate({x:.3f} {y:.3f}) rotate({rot})">' \
            '<rect x="-0.85" y="0" width="1.7" height="0.6" rx="0.1" class="fx"/>' \
            '<ellipse cx="0" cy="1.45" rx="0.68" ry="0.9" class="fx"/></g>'
        self.add("fixture", g)

    def basin(self, cx, cy, rot=0):
        self.add("fixture", f'<g transform="translate({cx:.3f} {cy:.3f}) rotate({rot})">'
                 '<ellipse cx="0" cy="0" rx="0.7" ry="0.5" class="fx"/>'
                 '<circle cx="0" cy="-0.05" r="0.06" class="fx"/></g>')

    def counter(self, x, y, w, h, layer="fixture"):
        self.rect(x, y, w, h, "counter", layer)

    def tub(self, x, y, w, h):
        self.rect(x, y, w, h, "fx", rx=0.15)
        self.rect(x + 0.25, y + 0.25, w - 0.5, h - 0.5, "fx", rx=0.6)

    def freetub(self, cx, cy, l, wd, rot=0):
        self.add("fixture", f'<g transform="translate({cx:.3f} {cy:.3f}) rotate({rot})">'
                 f'<rect x="{-l/2:.3f}" y="{-wd/2:.3f}" width="{l:.3f}" height="{wd:.3f}" rx="{wd/2:.3f}" class="fx"/>'
                 f'<rect x="{-l/2+0.3:.3f}" y="{-wd/2+0.3:.3f}" width="{l-0.6:.3f}" height="{wd-0.6:.3f}" rx="{wd/2-0.3:.3f}" class="fx"/></g>')

    def shower(self, x, y, w, h, glass_side="b"):
        self.rect(x, y, w, h, "wetzone", "floor")
        self.circle(x + w / 2, y + h / 2, 0.12, "fx")
        if glass_side == "b":
            self.line(x, y + h, x + w, y + h, "glassln")
        elif glass_side == "t":
            self.line(x, y, x + w, y, "glassln")
        elif glass_side == "r":
            self.line(x + w, y, x + w, y + h, "glassln")
        elif glass_side == "l":
            self.line(x, y, x, y + h, "glassln")

    def range_(self, x, y, w, h):
        self.rect(x, y, w, h, "appl")
        for i in range(3):
            for j in range(2):
                self.circle(x + w * (i + 0.5) / 3, y + h * (j + 0.5) / 2, min(w, h) * 0.13, "fx")

    def appliance(self, x, y, w, h, tag):
        self.rect(x, y, w, h, "appl")
        self.text(x + w / 2, y + h / 2 + 0.22, tag, "tag")

    def stairs(self, x, y, w, h, n, direction, cls="tread"):
        """Treads across a run. direction: 'up'/'down' along y, or 'left'/'right' along x."""
        self.rect(x, y, w, h, "stairbg", "floor")
        if direction in ("up", "down"):
            step = h / n
            for k in range(1, n):
                self.line(x, y + k * step, x + w, y + k * step, cls)
        else:
            step = w / n
            for k in range(1, n):
                self.line(x + k * step, y, x + k * step, y + h, cls)
        self.rect(x, y, w, h, "stairedge")

    def arrow(self, pts, label=None, lx=None, ly=None):
        self.poly(pts, "arrow", "note")
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        ang = math.atan2(y2 - y1, x2 - x1)
        L = 0.55
        a1 = (x2 - L * math.cos(ang - 0.45), y2 - L * math.sin(ang - 0.45))
        a2 = (x2 - L * math.cos(ang + 0.45), y2 - L * math.sin(ang + 0.45))
        self.poly([a1, (x2, y2), a2], "arrowhead", "note", closed=True)
        if label:
            self.text(lx, ly, label, "tag strong", "note")

    def void(self, x, y, w, h, text="OPEN TO BELOW"):
        self.rect(x, y, w, h, "voidfill", "floor")
        self.line(x, y, x + w, y + h, "voidx", "floor")
        self.line(x + w, y, x, y + h, "voidx", "floor")

    # ---------- furniture ----------
    def bed(self, cx, head_y, w, l, direction=1):
        """direction=1 bed extends toward +y from headboard; -1 toward -y."""
        y0 = head_y if direction > 0 else head_y - l
        self.rect(cx - w / 2, y0, w, l, "furn", "furn", rx=0.2)
        py = head_y + direction * 0.35
        ph = 1.2
        pys = py if direction > 0 else py - ph
        self.rect(cx - w / 2 + 0.35, pys, w / 2 - 0.55, ph, "furn", "furn", rx=0.25)
        self.rect(cx + 0.2, pys, w / 2 - 0.55, ph, "furn", "furn", rx=0.25)
        fy = head_y + direction * l * 0.62
        self.line(cx - w / 2, fy, cx + w / 2, fy, "furnln", "furn")
        for s in (-1, 1):
            nx = cx + s * (w / 2 + 1.0)
            ny = head_y + direction * 0.1 if direction > 0 else head_y - 1.7
            self.rect(nx - 0.85, ny, 1.7, 1.6, "furn", "furn", rx=0.1)

    def bed_x(self, head_x, cy, w, l, direction=1):
        """Bed with headboard on a vertical wall; extends toward +x (direction=1) or -x."""
        x0 = head_x if direction > 0 else head_x - l
        self.rect(x0, cy - w / 2, l, w, "furn", "furn", rx=0.2)
        px = head_x + direction * 0.35
        pw = 1.2
        pxs = px if direction > 0 else px - pw
        self.rect(pxs, cy - w / 2 + 0.35, pw, w / 2 - 0.55, "furn", "furn", rx=0.25)
        self.rect(pxs, cy + 0.2, pw, w / 2 - 0.55, "furn", "furn", rx=0.25)
        fx = head_x + direction * l * 0.62
        self.line(fx, cy - w / 2, fx, cy + w / 2, "furnln", "furn")
        for s in (-1, 1):
            ny = cy + s * (w / 2 + 1.0)
            nx = head_x + 0.1 if direction > 0 else head_x - 1.7
            self.rect(nx, ny - 0.85, 1.6, 1.7, "furn", "furn", rx=0.1)

    def sofa(self, x, y, w, h, back="t"):
        self.rect(x, y, w, h, "furn", "furn", rx=0.3)
        d = 0.75
        if back == "t":
            self.rect(x, y, w, d, "furnline", "furn", rx=0.3)
        elif back == "b":
            self.rect(x, y + h - d, w, d, "furnline", "furn", rx=0.3)
        elif back == "l":
            self.rect(x, y, d, h, "furnline", "furn", rx=0.3)
        elif back == "r":
            self.rect(x + w - d, y, d, h, "furnline", "furn", rx=0.3)

    def chair(self, cx, cy, s=2.4, back="t"):
        self.sofa(cx - s / 2, cy - s / 2, s, s, back)

    def table(self, cx, cy, w, h, seats_long=4, seats_end=1, round_=False):
        if round_:
            self.circle(cx, cy, w / 2, "furn", "furn")
        else:
            self.rect(cx - w / 2, cy - h / 2, w, h, "furn", "furn", rx=0.1)
        cw, cd = 1.5, 1.3
        if seats_long:
            for k in range(seats_long):
                px = cx - w / 2 + w * (k + 0.5) / seats_long
                self.rect(px - cw / 2, cy - h / 2 - cd - 0.15, cw, cd, "furn", "furn", rx=0.2)
                self.rect(px - cw / 2, cy + h / 2 + 0.15, cw, cd, "furn", "furn", rx=0.2)
        for s in (-1, 1)[:2] if seats_end else ():
            ex = cx + s * (w / 2 + 0.15 + cd / 2)
            self.rect(ex - cd / 2, cy - cw / 2, cd, cw, "furn", "furn", rx=0.2)

    def stool(self, cx, cy):
        self.circle(cx, cy, 0.6, "furn", "furn")

    def rug(self, x, y, w, h):
        self.rect(x, y, w, h, "rug", "under", rx=0.1)

    def car(self, cx, cy):
        w, l = 6.2, 15.5
        self.rect(cx - w / 2, cy - l / 2, w, l, "car", "furn", rx=1.6)
        self.rect(cx - w / 2 + 0.6, cy - l / 2 + 3.8, w - 1.2, 2.2, "car", "furn", rx=0.6)
        self.rect(cx - w / 2 + 0.6, cy + l / 2 - 4.6, w - 1.2, 1.6, "car", "furn", rx=0.5)

    def planter(self, cx, cy, r=1.0):
        self.circle(cx, cy, r, "plant", "furn")
        self.circle(cx, cy, r * 0.55, "plant", "furn")

    # ---------- dimension strings ----------
    def hdim(self, y, x1, x2, txt=None, ticks=None):
        self.line(x1, y, x2, y, "dimln", "dim")
        for xx in [x1, x2] + list(ticks or []):
            self.line(xx - 0.3, y + 0.3, xx + 0.3, y - 0.3, "dimtick", "dim")
            self.line(xx, y - 0.6, xx, y + 0.6, "dimln", "dim")
        self.text((x1 + x2) / 2, y - 0.45, txt or ftin(x2 - x1), "dimtxt", "dim")

    def vdim(self, x, y1, y2, txt=None):
        self.line(x, y1, x, y2, "dimln", "dim")
        for yy in (y1, y2):
            self.line(x - 0.3, yy + 0.3, x + 0.3, yy - 0.3, "dimtick", "dim")
            self.line(x - 0.6, yy, x + 0.6, yy, "dimln", "dim")
        self.text(x - 0.45, (y1 + y2) / 2, txt or ftin(y2 - y1), "dimtxt", "dim", rot=-90)

    def callout(self, x, y, n):
        self.circle(x, y, 0.95, "callout", "note")
        self.text(x, y + 0.42, str(n), "callnum", "note")

    def scalebar(self, x, y):
        for k, (a, b) in enumerate(((0, 4), (4, 8), (8, 16))):
            self.rect(x + a, y, b - a, 0.45, "sb" + ("1" if k % 2 == 0 else "0"), "note")
        for v in (0, 4, 8, 16):
            self.text(x + v, y + 1.5, str(v), "sbtxt", "note")
        self.text(x + 17.2, y + 1.5, "FT", "sbtxt", "note", anchor="start")

    def north(self, x, y):
        self.circle(x, y, 1.6, "thin", "note")
        self.poly([(x, y - 1.4), (x + 0.6, y + 0.9), (x, y + 0.4), (x - 0.6, y + 0.9)], "arrowhead", "note", closed=True)

    # ---------- output ----------
    def svg(self, vb, cls="plan", title=""):
        x, y, w, h = vb
        order = ("floor", "under", "fixture", "furn", "open", "wall", "dim", "label", "note")
        body = "\n".join("\n".join(self.layers[k]) for k in order)
        t = f"<title>{title}</title>" if title else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" class="{cls}" '
                f'role="img" aria-label="{title}">{t}\n{body}\n</svg>')
