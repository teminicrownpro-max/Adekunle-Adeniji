"""Interior elevations (3/8" = 1'-0") and roof / terrace edge details (1" = 1'-0")."""
from svgkit import INK, fi, drawing_title

CUT = '#1f1f1d'
OAK = '#e3cfae'
OAK_DARK = '#c9ad84'
SLAB = '#f3f0ea'
PLASTER = '#e7e0d5'
BRONZE = '#3c3530'
GLASS = '#dbe7ee'


class IE:
    """One interior elevation: u runs left to right on the sheet, z is height above the floor."""

    def __init__(self, svg, left, top, s, u0, u1, h=10.0):
        self.svg, self.s, self.u0, self.u1, self.h = svg, s, u0, u1, h
        self.left = left + 0.5 * s
        self.base = top + (h + 0.6) * s

    @property
    def width(self):
        return (self.u1 - self.u0 + 1.0) * self.s

    def X(self, u):
        return self.left + (u - self.u0) * self.s

    def Z(self, z):
        return self.base - z * self.s

    def rect(self, u0, z0, u1, z1, fill='none', stroke=INK, sw=0.7, **kw):
        self.svg.rect(self.X(min(u0, u1)), self.Z(max(z0, z1)), abs(u1 - u0) * self.s, abs(z1 - z0) * self.s,
                      fill=fill, stroke=stroke, sw=sw, **kw)

    def line(self, u0, z0, u1, z1, sw=0.6, c=INK, **kw):
        self.svg.line(self.X(u0), self.Z(z0), self.X(u1), self.Z(z1), sw=sw, c=c, **kw)

    def frame(self):
        self.rect(self.u0 - 0.5, -0.6, self.u1 + 0.5, 0, fill=CUT, stroke=None)
        self.rect(self.u0 - 0.5, self.h, self.u1 + 0.5, self.h + 0.6, fill=CUT, stroke=None)
        self.rect(self.u0 - 0.5, 0, self.u0, self.h, fill=CUT, stroke=None)
        self.rect(self.u1, 0, self.u1 + 0.5, self.h, fill=CUT, stroke=None)

    def wall(self, fill=PLASTER):
        self.rect(self.u0, 0, self.u1, self.h, fill=fill, stroke=None)

    def slab(self, u0, z0, u1, z1):
        self.rect(u0, z0, u1, z1, fill=SLAB, sw=0.5)
        cid = self.svg.clip_rect(self.X(u0), self.Z(z1), (u1 - u0) * self.s, (z1 - z0) * self.s)
        self.svg.g(f'clip-path="url(#{cid})"')
        k = 0
        u = u0 - 2
        while u < u1 + 2:
            x0, y0 = self.X(u), self.Z(z0)
            x1, y1 = self.X(u + 3.5), self.Z(z1)
            self.svg.path(f'M {x0:.1f} {y0:.1f} C {x0 + 30:.1f} {y0 - 60:.1f}, {x1 - 40:.1f} {y1 + 70:.1f}, {x1:.1f} {y1:.1f}',
                          stroke='#bdb5aa', sw=0.9 if k % 2 else 0.5, op=0.85)
            u += 2.2
            k += 1
        self.svg.end()

    def cabinets(self, u0, u1, z0, z1, n, fill=OAK, drawers=0):
        self.rect(u0, z0, u1, z1, fill=fill, sw=0.8)
        w = (u1 - u0) / n
        for i in range(1, n):
            self.line(u0 + i * w, z0, u0 + i * w, z1, sw=0.5, c='#8c7a62')
        for k in range(1, drawers + 1):
            zz = z0 + (z1 - z0) * k / (drawers + 1)
            self.line(u0, zz, u1, zz, sw=0.5, c='#8c7a62')

    def counter(self, u0, u1, z=3.0, t=0.17):
        self.rect(u0 - 0.06, z, u1 + 0.06, z + t, fill=SLAB, sw=0.8)

    def glass(self, u0, z0, u1, z1, mull=0):
        self.rect(u0, z0, u1, z1, fill=GLASS, sw=1.2, stroke=BRONZE)
        for i in range(1, mull + 1):
            uu = u0 + (u1 - u0) * i / (mull + 1)
            self.line(uu, z0, uu, z1, sw=1.2, c=BRONZE)
        self.line(u0 + (u1 - u0) * 0.15, z1 - 0.4, u0 + (u1 - u0) * 0.4, z1 - (z1 - z0) * 0.45, sw=0.5, c='#9fb4c2')

    def sconce(self, u, z):
        self.rect(u - 0.08, z - 0.5, u + 0.08, z + 0.5, fill=BRONZE, stroke=None)
        self.svg.ellipse(self.X(u), self.Z(z), 0.3 * self.s, 0.9 * self.s, fill='#ffe2a6', op=0.35)

    def note(self, u, z, text, tu, tz, anchor='start'):
        self.svg.line(self.X(u), self.Z(z), self.X(tu), self.Z(tz), sw=0.45, c='#555')
        self.svg.circle(self.X(u), self.Z(z), 1.6, fill='#555')
        dx = 4 if anchor == 'start' else -4
        self.svg.text(self.X(tu) + dx, self.Z(tz) + 3, text, size=7.2, anchor=anchor, fill='#333')

    def dim_v(self, u, z0, z1):
        x = self.X(u)
        self.svg.line(x, self.Z(z0), x, self.Z(z1), sw=0.5)
        for z in (z0, z1):
            self.svg.line(x - 3, self.Z(z) + 3, x + 3, self.Z(z) - 3, sw=0.9)
        self.svg.text(x - 4, (self.Z(z0) + self.Z(z1)) / 2, fi(z1 - z0), size=7, anchor='middle', rot=-90)

    def title(self, num_, text, scale='SCALE: 3/8" = 1\'-0"', width=None):
        drawing_title(self.svg, self.X(self.u0) - 0.5 * self.s, self.Z(-0.6) + 78, num_, text, scale,
                      width=width or min(self.width, 640))


# ------------------------------------------------------------------ level 1
def kitchen_range_wall(svg, left, top, s=37.5):
    """Looking south at the range wall; u = 50 - X."""
    e = IE(svg, left, top, s, 0.75, 20.0)
    e.wall()
    e.rect(3, 0, 6, 8, fill='#f4f2ee', sw=0.6)
    e.svg.text(e.X(4.5), e.Z(4.2), 'SCULLERY', size=6.5, anchor='middle', fill='#777')
    e.svg.text(e.X(4.5), e.Z(4.2) + 9, 'BEYOND', size=6.5, anchor='middle', fill='#777')
    e.cabinets(0.75, 2.75, 0, 8.5, 1, fill=OAK_DARK)
    e.slab(6.4, 3.17, 19.8, 10)
    e.cabinets(6.4, 10.6, 0.33, 3.0, 2, drawers=2)
    e.cabinets(15.4, 19.8, 0.33, 3.0, 3, drawers=1)
    e.rect(6.4, 0, 19.8, 0.33, fill='#5a524a', stroke=None)
    e.rect(10.6, 0.33, 15.4, 3.0, fill='#d4d6d6', sw=0.8)
    e.rect(10.85, 0.6, 15.15, 2.2, fill='#2b2b2b', sw=0.5)
    for k in range(6):
        e.svg.circle(e.X(11.1 + k * 0.78), e.Z(2.55), 0.11 * s, fill='#3a3a3a')
    e.counter(6.4, 19.8)
    e.svg.poly([(e.X(10.6), e.Z(6.4)), (e.X(15.4), e.Z(6.4)), (e.X(14.6), e.Z(10)), (e.X(11.4), e.Z(10))],
               fill=PLASTER, stroke=INK, sw=0.8)
    e.line(10.6, 6.6, 15.4, 6.6, sw=0.5, c='#9b9184')
    for u0, u1 in ((6.8, 10.2), (15.8, 19.4)):
        for z in (5.4, 7.1):
            e.rect(u0, z, u1, z + 0.15, fill=OAK_DARK, sw=0.6)
            e.line(u0 + 0.1, z - 0.05, u1 - 0.1, z - 0.05, sw=1.4, c='#ffd38f')
    e.rect(17.0, 3.17, 18.2, 3.3, fill='#bbb', sw=0.4)
    e.line(17.6, 3.3, 17.6, 4.4, sw=1.4, c=BRONZE)
    e.line(17.6, 4.4, 17.15, 4.1, sw=1.4, c=BRONZE)
    e.frame()
    e.dim_v(20.6, 0, 3.17)
    e.dim_v(20.6, 3.17, 10)
    e.note(13.0, 8.8, 'CUSTOM LIME-PLASTER HOOD', 8.0, 11.3, 'end')
    e.note(18.5, 8.5, 'T1 BOOK-MATCHED SLAB, FULL HEIGHT', 15.0, 11.3)
    e.note(8.5, 7.15, 'OAK FLOATING SHELVES W/ LED', 3.0, 9.5, 'end')
    e.note(13.0, 1.5, '48" DUAL-FUEL RANGE (INDUCTION)', 8.0, -1.6, 'end')
    e.note(17.0, 1.6, 'RIFT WHITE OAK, PUSH-LATCH', 16.0, -1.6)
    e.note(1.75, 4.2, 'REF. COLUMN END PANEL', 0.6, -1.6, 'end')
    e.title('2', 'KITCHEN — RANGE WALL ELEVATION (LOOKING SOUTH)')
    return e


def living_fireplace_wall(svg, left, top, s=37.5):
    """Looking west at the living-room wall; u = Y."""
    e = IE(svg, left, top, s, 24.0, 53.25)
    e.wall()
    e.glass(26, 7.5, 35, 10, mull=1)
    e.cabinets(30.2, 36.2, 0, 2.5, 3)
    e.rect(30.2, 2.5, 36.2, 7.2, fill=OAK, sw=0.8)
    for z in (3.7, 4.9, 6.1):
        e.line(30.2, z, 36.2, z, sw=0.7, c='#8c7a62')
    e.line(33.2, 2.5, 33.2, 7.2, sw=0.6, c='#8c7a62')
    e.slab(36.5, 0, 45.5, 10)
    e.rect(36.5, 1.0, 45.5, 1.35, fill='#d8d1c6', sw=0.6)
    e.rect(38.0, 1.6, 44.0, 2.9, fill='#2a2522', sw=0.6)
    e.svg.path(f'M {e.X(38.4):.1f} {e.Z(1.8):.1f} q 20 -14 40 0 t 40 0 t 40 0 t 40 0 t 40 0', stroke='#f2a64f', sw=2.2)
    e.rect(38.75, 4.4, 43.25, 7.0, fill='#141414', sw=0.6)
    e.glass(47, 0, 52.5, 10, mull=0)
    e.frame()
    e.dim_v(53.9, 0, 10)
    e.note(41.0, 2.2, 'LINEAR 72" DIRECT-VENT FIREPLACE', 47.0, -1.6)
    e.note(41.0, 5.7, 'RECESSED 85" DISPLAY', 46.6, 8.3)
    e.note(44.6, 9.2, 'T1 BOOK-MATCHED SLAB SURROUND', 46.6, 11.3)
    e.note(33.2, 5.5, 'OAK BUILT-IN SHELVING W/ LED', 29.2, 11.3, 'end')
    e.note(40.0, 1.18, 'FLOATING STONE HEARTH BENCH', 33.0, -1.6, 'end')
    e.title('3', 'LIVING — FIREPLACE WALL ELEVATION (LOOKING WEST)')
    return e


# ------------------------------------------------------------------ level 2
def wine_bar_wall(svg, left, top, s=37.5):
    """Family lounge north wall looking north; u = X."""
    e = IE(svg, left, top, s, 19.5, 37.79)
    e.wall()
    e.rect(20, 0, 25, 9, fill='#f4f2ee', sw=0.6)
    e.svg.text(e.X(22.5), e.Z(4.5), 'HALL BEYOND', size=6.5, anchor='middle', fill='#777')
    e.rect(26.0, 3.6, 37.6, 9.4, fill='#2b2420', sw=0.8)
    for r in range(9):
        for c in range(22):
            e.svg.circle(e.X(26.4 + c * 0.51), e.Z(4.0 + r * 0.6), 0.13 * s, fill='#7d2e2e' if (r + c) % 3 else '#c9b07a')
    e.line(26.0, 6.5, 37.6, 6.5, sw=1.2, c='#ffd38f')
    e.cabinets(26.0, 37.6, 0.33, 3.0, 5, fill=OAK_DARK)
    e.rect(26.0, 0, 37.6, 0.33, fill='#5a524a', stroke=None)
    e.counter(26.0, 37.6)
    e.rect(30.4, 3.17, 31.6, 3.3, fill='#bbb', sw=0.4)
    e.line(31.0, 3.3, 31.0, 4.1, sw=1.4, c='#c4a26b')
    e.frame()
    e.dim_v(38.3, 0, 10)
    e.note(32.0, 8.8, 'BACKLIT WINE WALL, 198 BOTTLES, BRONZE GLASS DOORS', 24.6, 11.3, 'end')
    e.note(28.0, 1.8, 'SMOKED OAK BAR CABINETRY, BEVERAGE FRIDGE', 25.6, -1.6, 'end')
    e.note(31.0, 3.1, 'QUARTZITE TOP, BAR SINK', 33.0, -1.6)
    e.title('2', 'FAMILY LOUNGE — WINE BAR ELEVATION')
    return e


def suite_vanity_wall(svg, left, top, s=37.5):
    """Typical Level 2 suite bath, vanity wall looking north; u = X (Bath 2)."""
    e = IE(svg, left, top, s, 0.75, 8.79, h=9.0)
    e.slab(0.75, 0, 8.79, 9.0)
    e.rect(1.05, 0.6, 8.49, 2.75, fill=OAK, sw=0.8)
    e.line(4.77, 0.6, 4.77, 2.75, sw=0.5, c='#8c7a62')
    e.counter(1.05, 8.49, z=2.75, t=0.2)
    for cx in (2.9, 6.6):
        e.rect(cx - 1.2, 3.6, cx + 1.2, 6.8, fill='#e9eef1', sw=0.8, stroke=BRONZE)
        e.line(cx, 2.95, cx, 3.45, sw=1.4, c=BRONZE)
    for u in (1.2, 4.77, 8.3):
        e.sconce(u, 5.6)
    e.frame()
    e.note(4.77, 1.7, 'FLOATING OAK VANITY', 6.0, -1.6)
    e.note(6.6, 6.0, 'BRONZE-FRAMED MIRRORS', 7.0, 9.9)
    e.title('3', 'TYP. SUITE BATH — VANITY', width=300)
    return e


def lounge_fireplace_wall(svg, left, top, s=37.5):
    """Family lounge east wall looking east; u = -Y (front at right)."""
    e = IE(svg, left, top, s, -24.0, -6.75)
    e.wall()
    e.rect(-9.25, 0, -6.75, 8, fill='#f1ede6', sw=0.6)
    e.svg.text(e.X(-8.0), e.Z(4.0), 'STUDY', size=6.5, anchor='middle', fill='#777')
    e.slab(-19.5, 0, -10.5, 10)
    e.rect(-18.5, 1.4, -11.5, 2.7, fill='#2a2522', sw=0.6)
    e.svg.path(f'M {e.X(-18.1):.1f} {e.Z(1.6):.1f} q 20 -14 40 0 t 40 0 t 40 0 t 40 0 t 40 0 t 40 0', stroke='#f2a64f',
               sw=2.2)
    e.rect(-17.6, 4.2, -12.4, 7.1, fill='#141414', sw=0.6)
    e.cabinets(-23.6, -19.9, 0, 2.2, 2)
    e.cabinets(-10.1, -9.5, 0, 2.2, 1)
    e.frame()
    e.dim_v(-6.1, 0, 10)
    e.note(-15.0, 2.0, 'LINEAR FIREPLACE IN HERRINGBONE-PATTERN SLAB', -20.0, -1.6, 'end')
    e.note(-15.0, 6.0, 'MEDIA DISPLAY', -11.0, 11.3)
    e.title('4', 'FAMILY LOUNGE — FIREPLACE WALL (LOOKING EAST)')
    return e


# ------------------------------------------------------------------ level 3
def spa_vanity_wall(svg, left, top, s=37.5):
    """Primary spa bath east wall looking east; u = -Y."""
    e = IE(svg, left, top, s, -45.25, -28.21)
    e.slab(-45.25, 0, -28.21, 10)
    e.glass(-44.0, 6.5, -30.0, 9.5, mull=2)
    e.rect(-42.6, 0.6, -34.6, 2.75, fill=OAK, sw=0.8)
    e.line(-38.6, 0.6, -38.6, 2.75, sw=0.5, c='#8c7a62')
    e.counter(-42.6, -34.6, z=2.75, t=0.2)
    for cu in (-40.6, -36.6):
        e.svg.ellipse(e.X(cu), e.Z(2.95), 0.9 * s, 0.25 * s, fill='#fff', stroke=INK, sw=0.6)
        e.rect(cu - 1.3, 3.5, cu + 1.3, 6.2, fill='#e9eef1', sw=0.8, stroke=BRONZE)
    for u in (-42.4, -38.6, -34.8):
        e.sconce(u, 5.2)
    e.rect(-33.0, 0, -28.21, 10, fill=PLASTER, sw=0.7)
    e.svg.text(e.X(-30.6), e.Z(5.0), 'WC', size=7, anchor='middle', fill='#777')
    e.svg.path(f'M {e.X(-44.6):.1f} {e.Z(0):.1f} L {e.X(-44.6):.1f} {e.Z(1.5):.1f} Q {e.X(-43.1):.1f} {e.Z(2.1):.1f} '
               f'{e.X(-41.6):.1f} {e.Z(1.5):.1f} L {e.X(-41.6):.1f} {e.Z(0):.1f} Z', fill='#fafafa', stroke=INK, sw=0.9)
    e.frame()
    e.dim_v(-27.6, 0, 10)
    e.note(-37.0, 8.2, 'RIBBON CLERESTORY 6\'-6" A.F.F.', -31.5, 11.3)
    e.note(-38.6, 1.6, '8\'-0" FLOATING DOUBLE VANITY', -33.0, -1.6)
    e.note(-43.1, 1.0, 'FREESTANDING STONE-RESIN TUB', -45.0, -1.6, 'end')
    e.title('2', 'PRIMARY SPA BATH — VANITY WALL (LOOKING EAST)')
    return e


def primary_fireplace_wall(svg, left, top, s=37.5):
    """Primary bedroom west wall looking west; u = Y."""
    e = IE(svg, left, top, s, 28.21, 45.25)
    e.wall(fill='#e3dbcf')
    e.rect(29.5, 0, 32.5, 9, fill=OAK, sw=0.8)
    e.line(32.2, 4.2, 32.2, 5.4, sw=1.6, c=BRONZE)
    e.rect(35.8, 0, 44.2, 10, fill=OAK_DARK, sw=0.6)
    for u in range(36, 44):
        e.line(u + 0.2, 0, u + 0.2, 10, sw=0.4, c='#a98c64')
    e.slab(37.0, 0, 43.0, 10)
    e.rect(37.5, 1.5, 42.5, 2.6, fill='#2a2522', sw=0.6)
    e.svg.path(f'M {e.X(37.8):.1f} {e.Z(1.7):.1f} q 20 -14 40 0 t 40 0 t 40 0 t 40 0', stroke='#f2a64f', sw=2.2)
    e.frame()
    e.dim_v(45.8, 0, 10)
    e.note(31.0, 6.5, '9\'-0" RIFT OAK DOOR TO DRESSING ROOM', 30.0, 11.3, 'end')
    e.note(40.0, 2.0, 'LINEAR FIREPLACE, SLAB SURROUND', 43.0, -1.6)
    e.note(36.4, 7.0, 'FLUTED OAK PANELING', 36.0, 11.3)
    e.title('3', 'PRIMARY BEDROOM — FIREPLACE WALL (LOOKING WEST)')
    return e


INTERIORS = {1: [kitchen_range_wall, living_fireplace_wall], 2: [(wine_bar_wall, suite_vanity_wall), lounge_fireplace_wall],
             3: [spa_vanity_wall, primary_fireplace_wall]}


# ------------------------------------------------------------------ details
class DT:
    def __init__(self, svg, left, top, s=100):
        self.svg, self.left, self.top, self.s = svg, left, top, s

    def X(self, u):
        return self.left + u * self.s

    def Z(self, z):
        return self.top + (4.0 - z) * self.s

    def rect(self, u0, z0, u1, z1, fill='none', stroke=INK, sw=0.8, **kw):
        self.svg.rect(self.X(min(u0, u1)), self.Z(max(z0, z1)), abs(u1 - u0) * self.s, abs(z1 - z0) * self.s, fill=fill,
                      stroke=stroke, sw=sw, **kw)

    def hatch(self, u0, z0, u1, z1, step=0.12, c='#999'):
        cid = self.svg.clip_rect(self.X(u0), self.Z(z1), (u1 - u0) * self.s, (z1 - z0) * self.s)
        self.svg.g(f'clip-path="url(#{cid})"')
        u = u0 - (z1 - z0)
        while u < u1:
            self.svg.line(self.X(u), self.Z(z0), self.X(u + (z1 - z0)), self.Z(z1), sw=0.4, c=c)
            u += step
        self.svg.end()

    def insul(self, u0, z0, u1, z1):
        self.rect(u0, z0, u1, z1, fill='#fbf7ee', sw=0.6)
        n = int((u1 - u0) / 0.18)
        pts = []
        for i in range(n + 1):
            pts.append((self.X(u0 + i * (u1 - u0) / n), self.Z(z0 if i % 2 == 0 else z1)))
        self.svg.poly(pts, close=False, stroke='#999', sw=0.5)

    def note(self, u, z, text, tz, tu=4.25):
        self.svg.circle(self.X(u), self.Z(z), 1.8, fill='#444')
        self.svg.line(self.X(u), self.Z(z), self.X(tu), self.Z(tz), sw=0.45, c='#555')
        self.svg.line(self.X(tu), self.Z(tz), self.X(tu) + 10, self.Z(tz), sw=0.45, c='#555')
        self.svg.text(self.X(tu) + 14, self.Z(tz) + 3, text, size=7.4, fill='#222')


def parapet_detail(svg, left, top):
    d = DT(svg, left, top)
    # roof assembly: joists (z 0.6..1.8), sheathing, insulation, cover board, membrane
    d.rect(0.0, 0.6, 2.6, 1.8, fill='#efe3cf')
    d.hatch(0.0, 0.6, 2.6, 1.8, step=0.35, c='#c9b08a')
    d.rect(0.0, 1.8, 2.6, 1.86, fill='#c9b08a')
    d.insul(0.0, 1.86, 2.6, 2.5)
    d.rect(0.0, 2.5, 2.6, 2.54, fill='#ddd')
    d.rect(0.0, 2.54, 2.6, 2.57, fill='#fff', stroke='#666', sw=0.8)
    # parapet framing up to 4'
    d.rect(2.6, 0.6, 3.1, 3.6, fill='#efe3cf')
    d.hatch(2.6, 0.6, 3.1, 3.6, step=0.25, c='#c9b08a')
    d.rect(2.6, 2.57, 2.66, 3.5, fill='#fff', stroke='#666', sw=0.6)
    d.rect(3.1, 0.3, 3.18, 3.6, fill='#c9b08a')
    d.rect(3.18, 0.3, 3.3, 3.6, fill='#fbf7ee', sw=0.5)
    d.rect(3.42, 0.3, 3.5, 3.72, fill='#3c3530', stroke=None)
    d.svg.poly([(d.X(2.5), d.Z(3.62)), (d.X(3.55), d.Z(3.72)), (d.X(3.55), d.Z(3.55)), (d.X(2.5), d.Z(3.52))],
               fill='#3c3530')
    # soffit + LED
    d.rect(1.2, 0.3, 3.5, 0.42, fill='#b98a5c', sw=0.6)
    d.rect(1.2, 0.42, 3.42, 0.6, fill='#fff', stroke='#888', sw=0.5)
    svg.circle(d.X(3.3), d.Z(0.36), 4, fill='#ffd38f')
    d.note(1.0, 2.55, 'PVC MEMBRANE ON 1/2" COVER BOARD', 3.9)
    d.note(0.6, 2.2, 'TAPERED POLYISO, R-49 AVG.', 3.4)
    d.note(0.9, 1.2, '14" WOOD I-JOISTS / 3/4" SHEATHING', 2.9)
    d.note(3.48, 3.65, 'BRONZE COPING, 1/4" SLOPE IN', 4.45, tu=4.25)
    d.note(3.46, 1.8, 'BRONZE FASCIA PANEL ON RAILS', 2.4)
    d.note(3.3, 0.36, 'LED COVE IN WOOD SLAT SOFFIT', 1.4)
    d.note(2.63, 3.2, 'MEMBRANE UP & OVER PARAPET', 4.0, tu=4.25)
    return d


def terrace_detail(svg, left, top):
    d = DT(svg, left, top)
    d.rect(0, 0.6, 3.0, 1.8, fill='#efe3cf')
    d.hatch(0, 0.6, 3.0, 1.8, step=0.35, c='#c9b08a')
    d.rect(0, 1.8, 3.0, 1.86, fill='#c9b08a')
    d.insul(0, 1.86, 3.0, 2.2)
    d.rect(0, 2.2, 3.0, 2.26, fill='#555', stroke=None)
    for u in (0.4, 1.4, 2.4):
        d.rect(u - 0.12, 2.26, u + 0.12, 2.55, fill='#888', stroke=None)
    for u0 in (0.0, 1.0, 2.0):
        d.rect(u0 + 0.02, 2.55, u0 + 0.98, 2.62, fill='#e6dfd2', sw=0.6)
    # edge: stone fascia, glass guard in base shoe
    d.rect(3.0, 0.6, 3.4, 2.62, fill='#e6dece')
    d.rect(3.4, 0.4, 3.48, 2.62, fill='#e6dece', sw=0.6)
    d.rect(2.85, 2.2, 3.35, 2.85, fill='#3c3530', stroke=None)
    d.rect(3.04, 2.6, 3.12, 4.3, fill='#cfe1ea', sw=0.6)
    bx, by = d.X(3.08), d.Z(4.3)
    d.svg.poly([(bx - 12, by + 4), (bx - 4, by + 4), (bx, by - 4), (bx + 4, by + 8), (bx + 8, by), (bx + 12, by)],
               close=False, stroke=INK, sw=0.8)
    d.rect(1.0, 0.25, 3.48, 0.4, fill='#b98a5c', sw=0.6)
    d.svg.circle(d.X(3.3), d.Z(0.32), 4, fill='#ffd38f')
    d.svg.text(d.X(3.15), d.Z(4.3) - 12, '42" GUARD ABOVE DECK', size=7, anchor='middle', fill='#333')
    d.note(0.5, 2.58, 'PORCELAIN PAVERS ON PEDESTALS', 3.95, tu=4.25)
    d.note(0.8, 2.23, 'HOT-RUBBERIZED WATERPROOFING', 3.5, tu=4.25)
    d.note(0.6, 2.0, 'TAPERED XPS', 3.1, tu=4.25)
    d.note(3.0, 2.5, 'BRONZE BASE SHOE, LAMINATED LOW-IRON GLASS', 2.7, tu=4.25)
    d.note(3.44, 1.4, 'SINTERED STONE FASCIA ON RAILS', 1.9, tu=4.25)
    d.note(3.3, 0.32, 'WOOD SLAT SOFFIT / LED COVE', 1.0, tu=4.25)
    return d
