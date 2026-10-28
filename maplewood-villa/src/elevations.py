"""Maplewood Villa — front (street) and rear (garden) elevations.

Units are feet. Drawing x matches plan x on the front elevation and is mirrored
(x' = 42 - x) on the rear one. Heights are above grade; SVG y = -height.
"""
from draw import Sheet

W = 42.0
FF1 = 1.5      # main floor
FF2 = 12.6     # second floor
EAVE = 22.6    # top of wall / underside of eave
HIP = 5 / 12   # main hip roof pitch
GAB = 14 / 12  # front gable pitch
OH = 1.0       # eave overhang

VIEW = (-20.5, -35.0, 85.0, 38.6)


def Y(h):
    return -h


class Elev(Sheet):
    """Elevations paint in call order (no plan layers)."""
    def add(self, layer, s):
        self.layers["floor"].append(s)

    def box(self, x, h0, w, h1, cls, layer="fixture"):
        self.rect(x, Y(h1), w, h1 - h0, cls, layer)

    def hline(self, x1, x2, h, cls, layer="fixture"):
        self.line(x1, Y(h), x2, Y(h), cls, layer)

    def vline(self, x, h0, h1, cls, layer="fixture"):
        self.line(x, Y(h0), x, Y(h1), cls, layer)

    def stone(self, x, h0, w, h1, course=0.9, joint=2.6):
        self.box(x, h0, w, h1, "m-stone", "floor")
        k, h = 0, h0 + course
        while h < h1 - 0.05:
            self.hline(x, x + w, h, "m-joint", "under")
            off = (joint / 2) * (k % 2)
            j = x + off + joint
            while j < x + w - 0.1:
                self.vline(j, h, min(h + course, h1), "m-joint", "under")
                j += joint
            h += course
            k += 1

    def stucco(self, x, h0, w, h1):
        self.box(x, h0, w, h1, "m-stucco", "floor")

    def oak(self, x, h0, w, h1, pitch=0.42):
        self.box(x, h0, w, h1, "m-oak", "floor")
        j = x + pitch
        while j < x + w - 0.05:
            self.vline(j, h0, h1, "m-oakln", "under")
            j += pitch

    def window(self, x, h0, w, h1, mullions=(), transoms=(), frame=0.22, door=False):
        self.box(x, h0, w, h1, "m-frame", "fixture")
        self.box(x + frame, h0 + (0 if door else frame), w - 2 * frame, h1 - frame, "m-glass", "fixture")
        # soft reflection
        gx0, gx1 = x + frame, x + w - frame
        self.poly([(gx0, Y(h1 - frame)), (gx0 + (gx1 - gx0) * 0.55, Y(h1 - frame)),
                   (gx0, Y(h1 - frame - (gx1 - gx0) * 0.9))], "m-glint", "fixture", closed=True)
        for m in mullions:
            self.box(m - frame / 2, h0, frame, h1, "m-frame", "fixture")
        for t in transoms:
            self.box(x, t - frame / 2, w, t + frame / 2, "m-frame", "fixture")

    def seam_roof(self, pts, spacing=1.15, cls="m-roof"):
        """Polygon of standing-seam roof with vertical seam lines clipped to it."""
        self.poly([(x, Y(h)) for x, h in pts], cls, "floor", closed=True)
        xs = [p[0] for p in pts]
        x = min(xs) + spacing
        while x < max(xs) - 0.05:
            hs = []
            n = len(pts)
            for i in range(n):
                (x1, h1), (x2, h2) = pts[i], pts[(i + 1) % n]
                if (x1 - x) * (x2 - x) < 0 and x1 != x2:
                    hs.append(h1 + (h2 - h1) * (x - x1) / (x2 - x1))
            hs.sort()
            for a, b in zip(hs[::2], hs[1::2]):
                self.vline(x, a, b, "m-seam", "under")
            x += spacing

    def tree(self, x, h, r, cls="m-tree"):
        self.vline(x, 0, h - r * 0.8, "m-trunk", "furn")
        self.ellipse(x, Y(h), r, r * 1.15, cls, "furn")
        self.ellipse(x - r * 0.35, Y(h + r * 0.3), r * 0.55, r * 0.6, "m-treehi", "furn")

    def shrub(self, x, w, h):
        self.ellipse(x, Y(h / 2), w / 2, h / 2, "m-shrub", "furn")

    def grass(self, x, h=2.6, n=9, spread=1.6):
        for k in range(n):
            t = k / (n - 1) - 0.5
            self.line(x, 0, x + t * spread, Y(h * (1 - abs(t) * 0.6)), "m-grass", "furn")

    def person(self, x, s=5.8):
        u = s / 5.8
        self.circle(x, Y(5.35 * u), 0.38 * u, "m-person", "furn")
        self.poly([(x - 0.55 * u, Y(4.85 * u)), (x + 0.55 * u, Y(4.85 * u)), (x + 0.42 * u, Y(2.7 * u)),
                   (x + 0.32 * u, 0), (x + 0.05 * u, 0), (x, Y(2.6 * u)), (x - 0.05 * u, 0),
                   (x - 0.32 * u, 0), (x - 0.42 * u, Y(2.7 * u))], "m-person", "furn", closed=True)

    def note(self, x, h, tx, th, lines, side="left"):
        """Leader from a point on the drawing to a margin note (lines: str or list)."""
        lines = [lines] if isinstance(lines, str) else lines
        end = tx - 1.0 if side == "left" else tx + 1.0
        self.poly([(x, Y(h)), (tx, Y(th)), (end, Y(th))], "m-leader", "note")
        self.circle(x, Y(h), 0.18, "m-dot", "note")
        anchor = "end" if side == "left" else "start"
        dx = -0.35 if side == "left" else 0.35
        for k, ln in enumerate(lines):
            self.text(end + dx, Y(th) + 0.27 + k * 0.95, ln, "m-note", "note", anchor=anchor)

    def level(self, h, label, x=W + 1.8):
        self.poly([(x - 0.5, Y(h) - 0.5), (x, Y(h)), (x + 0.5, Y(h) - 0.5)], "m-lvl", "note", closed=True)
        self.line(x - 0.6, Y(h), x + 6.4, Y(h), "m-lvlln", "note")
        self.text(x + 0.9, Y(h) - 0.35, label, "m-lvltxt", "note", anchor="start")


def _hip(e):
    # Main 6:12 hip roof; from either long face it reads as a triangle.
    apex = EAVE + (W / 2 + OH) * HIP
    e.seam_roof([(-OH, EAVE), (W + OH, EAVE), (W / 2, apex)])
    e.box(-OH, EAVE - 0.45, W + 2 * OH, EAVE, "m-fascia")
    return apex


def _eave_shadow(e, x0, x1):
    e.box(x0, EAVE - 1.25, x1 - x0, EAVE - 0.45, "m-shadow")


def front():
    e = Elev()
    _hip(e)
    # ----- garage wing: limestone base storey, stucco above -----
    e.stucco(0, FF2 - 0.9, 21.58, EAVE - 0.55)
    e.stone(0, 0, 21.58, FF2 - 0.9)
    e.box(0, FF2 - 1.25, 21.58, FF2 - 0.85, "m-band")
    # garage door: rift-oak carriage panels with a glazed upper band
    e.box(2.67, 0, 16.0, 8.0, "m-frame")
    e.oak(2.92, 0, 15.5, 6.2, 0.55)
    e.window(2.92, 6.2, 15.5, 7.8, mullions=[2.92 + 15.5 * k / 6 for k in range(1, 6)], frame=0.14)
    e.vline(10.67, 0, 6.2, "m-frame2")
    # steel + standing-seam canopy
    e.seam_roof([(1.6, 9.0), (19.74, 9.0), (19.74, 9.85), (1.6, 9.85)], 0.9, "m-roof")
    e.box(1.6, 8.7, 18.14, 9.05, "m-steel")
    e.box(1.6, 8.35, 18.14, 8.7, "m-shadow")
    for lx in (1.45, 19.89):
        e.box(lx - 0.28, 5.6, 0.56, 7.3, "m-steel")
        e.box(lx - 0.18, 5.9, 0.36, 7.0, "m-lamp")
    # bedroom windows above the garage
    e.window(3.55, 14.6, 4.0, 21.4, mullions=[5.55], transoms=[19.8])
    e.window(14.07, 14.6, 4.0, 21.4, mullions=[16.07], transoms=[19.8])
    _eave_shadow(e, 0, 21.58)

    # ----- study wing: white lime stucco under a steep gable -----
    ga = EAVE + (W - 31.08) / 2 * GAB
    cx = (31.08 + W) / 2
    # flush rake: a thin charcoal edge around the white gable
    e.poly([(30.62, Y(EAVE - 0.45)), (cx, Y(ga + 0.5)), (W + 0.46, Y(EAVE - 0.45))], "m-rake", "fixture", closed=True)
    e.poly([(31.08, Y(0)), (W, Y(0)), (W, Y(EAVE - 0.45)), (cx, Y(ga)), (31.08, Y(EAVE - 0.45))], "m-stucco", "floor", closed=True)
    e.stone(31.08, 0, W - 31.08, FF1 + 0.6)
    e.window(33.5, 3.0, 6.0, 10.8, mullions=[35.5, 37.5], transoms=[9.2])
    e.window(34.0, 14.6, 5.0, 21.4, mullions=[36.5], transoms=[19.8])
    e.box(33.3, 2.65, 6.4, 3.0, "m-sill")
    e.box(cx - 0.45, EAVE + 0.9, 0.9, EAVE + 3.4, "m-frame")          # gable slot
    for k in range(5):
        e.hline(cx - 0.35, cx + 0.35, EAVE + 1.2 + k * 0.45, "m-louver")

    # ----- portal: recessed two-storey glass entry in a limestone frame -----
    px0, px1 = 21.58, 31.08
    e.oak(px0, FF1, px1 - px0, 23.0, 0.38)
    e.box(px0, FF1, px1 - px0, 23.0, "m-shade")
    e.window(23.08, FF1, 6.5, 11.6, mullions=[24.58, 28.08], transoms=[10.5], door=True)
    e.oak(24.8, FF1, 3.06, 10.3, 0.3)                                  # pivot door leaf
    e.box(27.3, 4.6, 0.12, 7.4, "m-steel")                             # pull
    e.window(22.33, 12.9, 8.0, 22.2, mullions=[24.33, 26.33, 28.33], transoms=[18.4])
    for sx in (22.55, 29.95):
        e.box(sx - 0.2, 7.1, 0.4, 8.3, "m-steel")
    for k, hh in enumerate((0.75, 1.5)):
        e.box(px0 - 0.1 - (1 - k) * 0.4, hh - 0.75, px1 - px0 + 0.2 + (1 - k) * 0.8, hh, "m-stone")
    # frame
    e.stone(20.45, 0, 1.13, 25.8, 0.9, 1.13)
    e.stone(31.08, 0, 1.13, 25.8, 0.9, 1.13)
    e.stone(20.45, 23.0, 11.76, 25.8, 0.9, 2.9)
    e.box(20.25, 25.8, 12.16, 26.15, "m-coping")
    e.box(20.45, 23.0, 11.76, 23.25, "m-shadow")
    e.grass(21.3, 2.4, 9, 1.4)
    e.grass(31.4, 2.4, 9, 1.4)

    # ----- landscape + scale -----
    for x, w, h in ((-0.4, 3.2, 2.2), (1.9, 1.6, 1.4), (19.7, 1.8, 1.6), (40.3, 3.4, 2.4), (32.6, 2.6, 1.7), (36.6, 2.6, 1.6)):
        e.shrub(x, w, h)
    e.tree(-4.4, 16.0, 3.6)
    e.person(26.9, 5.8)
    e.box(-8.5, -0.25, 61.0, 0.08, "m-ground", "wall")
    e.box(-8.5, -1.6, 61.0, -0.25, "m-earth", "floor")

    # ----- levels + notes -----
    e.level(0, "GRADE")
    e.level(FF1, "MAIN  +1'-6\"")
    e.level(FF2, "SECOND  +12'-7\"")
    e.level(EAVE, "EAVE  +22'-7\"")
    e.note(7.0, 3.4, -9.4, 2.4, ["Rift-oak carriage door,", "glazed upper band"])
    e.note(1.0, 6.4, -9.4, 6.4, "Honed limestone base")
    e.note(4.2, 9.4, -9.4, 9.8, "Steel canopy, metal roof")
    e.note(1.6, 14.2, -9.4, 14.6, "Smooth white lime stucco")
    e.note(12.0, 25.0, -9.4, 25.0, "Charcoal metal roof")
    e.note(31.62, 11.6, 52.4, 11.2, ["Two-storey limestone portal,", "oak pivot door"], "right")
    e.note(38.6, 24.2, 52.4, 25.4, ["Steep 14:12 gable,", "flush rake"], "right")
    e.note(38.2, 6.4, 52.4, 6.4, ["Black aluminum-clad", "windows"], "right")
    return e.svg(VIEW, cls="elev", title="Front elevation")


def rear():
    e = Elev()
    M = lambda x: W - x
    _hip(e)
    e.stucco(0, 0, W, EAVE - 0.45)
    e.stone(0, 0, W, FF1 + 0.6)
    _eave_shadow(e, 0, W)
    # great room: three two-storey glazed bays (doors, spandrel, clerestory)
    for x0, x1, kind in ((23.83, 28.83, "door"), (30.0, 33.0, "fixed"), (34.2, 39.2, "door")):
        a, b = M(x1), M(x0)
        e.box(a - 0.35, FF1 - 0.05, b - a + 0.7, 21.8, "m-stone")
        e.window(a, FF1, b - a, 21.4, mullions=[(a + b) / 2] if kind == "door" else [],
                 transoms=[10.4, 13.6], door=True)
        e.box(a + 0.22, 10.5, b - a - 0.44, 13.5, "m-spandrel")
    # primary bedroom windows (above the loggia roof)
    e.window(M(10.5), 15.4, 3.5, 21.4, mullions=[M(8.75)], transoms=[19.8])
    e.window(M(18.0), 15.4, 3.5, 21.4, mullions=[M(16.25)], transoms=[19.8])
    # kitchen slider under the loggia
    e.window(M(16.82), FF1, 12.0, 10.2, mullions=[M(12.82), M(8.82)], door=True)
    e.box(M(21.33), FF1, 21.33, 11.6, "m-shade")
    # loggia: limestone columns + standing-seam shed roof
    e.seam_roof([(M(21.33) - 0.6, 11.4), (W + 0.6, 11.4), (W + 0.6, 14.2), (M(21.33) - 0.6, 14.2)], 1.0)
    e.box(M(21.33) - 0.6, 10.6, 21.33 + 1.2, 11.45, "m-coping")
    e.box(M(21.33) - 0.6, 10.25, 21.33 + 1.2, 10.6, "m-shadow")
    for cx in (0.6, 10.2, 20.73):
        e.stone(M(cx) - 0.7, 0, 1.4, 10.6, 0.9, 1.4)
        e.box(M(cx) - 0.85, 10.25, 1.7, 10.6, "m-coping")
    # terrace edge + planting
    e.box(-1.0, -0.05, 21.0, 0.6, "m-stone")
    for x, w, h in ((-0.2, 2.6, 2.0), (20.0, 2.0, 1.4)):
        e.shrub(x, w, h)
    e.tree(-4.4, 16.0, 3.6)
    e.person(15.6, 5.8)
    e.box(-8.5, -0.25, 61.0, 0.08, "m-ground", "wall")
    e.box(-8.5, -1.6, 61.0, -0.25, "m-earth", "floor")
    e.level(0, "GRADE")
    e.level(FF1, "MAIN  +1'-6\"")
    e.level(FF2, "SECOND  +12'-7\"")
    e.level(EAVE, "EAVE  +22'-7\"")
    e.note(3.6, 17.6, -9.4, 18.6, ["Three 20-ft glazed bays", "to the great room"])
    e.note(3.6, 12.0, -9.4, 12.4, "Bronze spandrel panels")
    e.note(1.0, 5.0, -9.4, 5.4, ["French doors to the", "stone terrace"])
    e.note(M(0.6), 6.0, 52.4, 6.0, ["Covered loggia,", "limestone columns"], "right")
    e.note(40.6, 13.2, 52.4, 15.6, "Standing-seam shed roof", "right")
    e.note(33.25, 20.6, 52.4, 25.4, ["Primary bedroom", "garden windows"], "right")
    return e.svg(VIEW, cls="elev", title="Rear elevation")
