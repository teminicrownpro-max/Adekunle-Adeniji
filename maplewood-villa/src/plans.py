"""Maplewood Villa — floor plans. Units: feet. Street is at the bottom (y = 52)."""
from draw import Sheet, EXT, INT, FDN, ftin

W, D = 42.0, 52.0
XA = 21.33   # garage / house spine; also kitchen | great room
XB = 31.33   # gallery | study & stair core
XS = 37.63   # powder & bath | stair
YR = 24.2    # rear living band | service band
YM = 30.6    # service band | garage
YF = 38.3    # stair core | study
YD = 47.25   # front door wall (portal recess behind it)

VIEW = (-7.5, -15.5, 57.5, 76.0)
VIEW_LOWER = (-7.5, -3.8, 57.5, 64.3)


def _shell(s, level):
    """Exterior walls shared by the main and second floor."""
    e = EXT
    h = e / 2
    if level == "main":
        rear = [("slide", 4.82, 16.82, {"panels": 3}),
                ("dbl", 23.83, 28.83, {"side": 1}),
                ("fixed", 30.0, 33.0),
                ("dbl", 34.2, 39.2, {"side": 1})]
        left = [("win", 2.8, 7.2), ("win", 12.4, 16.4), ("win", 39.5, 42.5)]
        right = [("win", 3.6, 5.6), ("win", 15.6, 17.6), ("win", 28.4, 31.4), ("win", 35.0, 37.6), ("win", 42.0, 46.0)]
        front_l = [("garage", 2.67, 18.67)]
        front_r = [("win", 33.5, 39.5, {"mullions": [35.5, 37.5]})]
        door = [("fixed", 23.08, 24.58), ("door", 24.58, 28.08, {"hinge": "a", "side": -1}), ("fixed", 28.08, 29.58)]
    else:
        rear = [("win", 7.0, 10.5), ("win", 14.5, 18.0),
                ("win", 23.83, 28.83), ("fixed", 30.0, 33.0), ("win", 34.2, 39.2)]
        left = [("win", 3.6, 7.6), ("win", 18.4, 21.4), ("win", 28.6, 31.0), ("win", 40.0, 42.2)]
        right = [("win", 3.6, 5.6), ("win", 15.6, 17.6), ("win", 35.2, 37.4)]
        front_l = [("win", 3.55, 7.55), ("win", 14.07, 18.07)]
        front_r = [("win", 34.0, 39.0, {"mullions": [36.5]})]
        door = [("fixed", 22.33, 30.33, {"mullions": [24.33, 26.33, 28.33]})]
    s.hwall(h, 0, W, e, rear)
    s.vwall(h, 0, D, e, left)
    s.vwall(W - h, 0, D, e, right)
    s.hwall(D - h, 0, XA + 0.25, e, front_l)
    s.hwall(D - h, XB - 0.25, W, e, front_r)
    # portal recess
    s.hwall(YD, XA, XB, e, door)
    s.vwall(XA, YD - 0.25, D, e)
    s.vwall(XB, YD - 0.25, D, e)


def main_floor():
    s = Sheet()
    # ---------- floor finishes ----------
    s.rect(0.5, 0.5, XA - 0.7, YR - 0.7, "oak", "floor")                      # kitchen + dining
    s.rect(XA - 0.2, 0.5, W - XA - 0.3, YR - 0.7, "oak", "floor")             # great room
    s.rect(XA + 0.2, YR + 0.2, XB - XA - 0.4, YD - YR - 0.45, "stone", "floor")  # gallery + foyer
    s.rect(XB + 0.2, YF + 0.2, W - XB - 0.7, D - YF - 0.7, "oak", "floor")    # study
    s.rect(0.5, YR + 0.2, XA - 0.7, YM - YR - 0.4, "tile", "floor")           # mud + scullery
    s.rect(XB + 0.2, YR + 0.2, XS - XB - 0.4, YF - YR - 0.4, "tile", "floor") # back hall / powder
    s.rect(XA + 0.25, YD + 0.25, XB - XA - 0.5, D - YD - 0.25, "porch", "floor")  # portico
    # rear loggia + terrace (outside)
    s.rect(0, -12.5, XA, 12.5, "porch", "floor")
    s.rect(XA, -10.0, W - XA, 10.0, "terrace", "floor")
    s.rect(0, -12.5, XA, 12.5, "roofline", "note")
    for px in (0.6, XA - 0.6):
        s.rect(px - 0.6, -12.5, 1.2, 1.2, "post", "wall")
    s.rect(9.6, -12.5, 1.2, 1.2, "post", "wall")
    s.counter(0.4, -11.4, 2.2, 8.5)           # outdoor kitchen
    s.rect(0.6, -8.0, 1.8, 3.0, "appl")
    s.table(13.5, -6.2, 7.5, 3.4, seats_long=3, seats_end=1)
    s.text(XA / 2 + 1.5, -1.6, "COVERED LOGGIA", "rname sm", "label")
    s.text(XA / 2 + 1.5, -0.7, "21'-4\" × 12'-6\"", "rdim sm", "label")
    s.text((XA + W) / 2, -5.0, "STONE TERRACE", "rname sm", "label")
    for k in range(5):
        s.line(XA + 0.0, -10.0 + 2.0 * k, W, -10.0 + 2.0 * k, "paver", "floor")

    _shell(s, "main")

    # ---------- interior walls ----------
    # spine: kitchen|great room pilasters, scullery|gallery, garage|gallery (with coat closet)
    s.vwall(XA, 0.5, YR, INT, [("open", 3.0, 21.5)])
    s.vwall(XA, YR, YD - 0.25, INT, [("dbl", 31.4, 35.1, {"side": 1})])
    s.vwall(18.93, YM, 35.9, INT)                       # coat closet carved from garage
    s.hwall(35.7, 18.73, XA, INT)
    # rear band | service band
    s.hwall(YR, 0.5, XA, INT, [("pocket", 16.32, 19.32)])
    s.hwall(YR, XA, W - 0.5, INT, [("open", 22.5, 30.16, {"cased": True})])
    # mudroom | scullery
    s.vwall(9.2, YR, YM, INT, [("door", 25.2, 27.9, {"hinge": "a", "side": 1})])
    # service band | garage
    s.hwall(YM, 0.5, XA, INT, [("door", 3.5, 6.3, {"hinge": "a", "side": -1})])
    # gallery | stair core | study
    s.vwall(XB, YR, YF, INT, [("open", YR + 0.2, 27.4), ("open", 34.3, YF)])
    s.vwall(XB, YF, YD - 0.25, INT, [("dbl", 40.0, 45.0, {"side": 1})])
    s.hwall(27.6, XB, XS + 0.2, INT, [("door", 34.0, 36.5, {"hinge": "b", "side": -1})])
    s.hwall(34.1, XB, XS + 0.2, INT)
    s.vwall(XS, YR, 34.3, INT, [("door", 24.6, 27.2, {"hinge": "a", "side": 1})])
    s.hwall(YF, XB, W - 0.5, INT)

    # ---------- kitchen ----------
    s.counter(0.5, 22.0, 1.82, 2.0)
    s.appliance(2.32, 22.0, 3.0, 2.0, "REF")
    s.counter(5.32, 22.0, 3.5, 2.0)
    s.range_(8.82, 22.0, 4.0, 2.0)
    s.counter(12.82, 22.0, 3.5, 2.0)
    s.appliance(19.32, 22.0, 1.81, 2.0, "OV")
    s.rect(8.32, 21.4, 5.0, 2.6, "overhead", "note")            # plaster hood
    s.rect(5.82, 13.5, 10.0, 4.0, "island")                     # island
    s.rect(9.82, 14.2, 2.0, 1.3, "fx", rx=0.15)                 # prep sink
    for k in range(4):
        s.stool(7.2 + k * 2.4, 12.6)
    # dining
    s.rug(4.6, 1.2, 12.4, 8.6)
    s.table(10.82, 5.6, 9.0, 3.6, seats_long=4, seats_end=1)
    s.circle(10.82, 5.6, 1.5, "overhead", "note")
    s.label(10.82, 19.8, "KITCHEN", "20'-8\" × 12'-6\"")
    s.label(17.9, 11.4, "DINING", "20'-8\" × 11'-0\"", size=0.85)

    # ---------- great room ----------
    s.rect(39.5, 5.6, 2.0, 10.0, "builtin", "fixture")          # hearth wall + built-ins
    s.rect(39.5, 7.6, 2.0, 6.0, "fireplace", "fixture")
    s.rect(40.2, 8.4, 1.3, 4.4, "firebox", "fixture")
    s.rect(38.3, 8.1, 1.2, 5.0, "hearth", "fixture")
    s.rug(26.8, 3.8, 10.4, 13.6)
    s.sofa(27.4, 6.6, 3.2, 8.0, back="l")
    s.chair(34.6, 5.6, 2.6, back="t")
    s.chair(34.6, 15.6, 2.6, back="b")
    s.rect(31.4, 8.6, 3.0, 4.0, "furn", "furn", rx=0.3)
    s.line(XA - 0.1, 3.0, XA - 0.1, 21.5, "beam", "note")
    s.rect(XA + 0.2, 20.5, W - XA - 0.7, 0.01, "overhead", "note")   # balcony edge above
    s.line(XA + 0.2, 20.7, W - 0.5, 20.7, "overheadln", "note")
    s.label(31.6, 18.6, "GREAT ROOM", "20'-0\" × 23'-6\"", "20-FT CEILING")

    # ---------- service band ----------
    s.rect(0.5, YR + 0.2, 1.6, YM - YR - 0.4, "builtin")       # lockers
    for k in range(1, 3):
        s.line(0.5, YR + 0.2 + k * 2.0, 2.1, YR + 0.2 + k * 2.0, "thin")
    s.rect(2.1, 25.4, 1.4, 3.6, "furn", "furn", rx=0.1)        # bench
    s.label(5.9, 27.0, "MUDROOM", "8'-6\" × 6'-0\"", size=0.8)
    s.counter(9.4, 28.4, XA - 9.6, 2.0)
    s.rect(13.3, 28.75, 2.2, 1.3, "fx", rx=0.15)
    s.appliance(15.7, 28.4, 2.0, 2.0, "DW")
    s.rect(9.4, 24.4, 6.6, 1.3, "shelf")
    s.label(14.2, 27.1, "SCULLERY", "11'-8\" × 6'-0\"", size=0.8)
    s.rect(19.13, YM + 0.2, 1.8, 4.9, "shelf")
    s.text(20.0, 33.4, "COAT", "tag", rot=-90)

    # ---------- garage ----------
    s.rect(0.5, YM + 0.2, XA - 0.7, D - YM - 0.7, "garagefl", "floor")
    s.car(5.9, 42.4)
    s.car(14.6, 42.4)
    s.rect(3.0, 31.0, 3.8, 1.4, "steps", "fixture")
    s.label(10.67, 49.3, "GARAGE", "20'-8\" × 20'-8\"")

    # ---------- gallery + foyer ----------
    s.label(26.33, 30.5, "GALLERY", "9'-7\" × 13'-8\"", size=0.9)
    s.label(26.33, 41.2, "FOYER", "9'-7\" × 8'-8\"", "20-FT CEILING")
    s.rect(XA + 0.45, YF - 0.05, XB - XA - 0.9, YD - YF - 0.45, "overhead", "note")
    s.rect(30.1, 28.2, 0.9, 5.2, "furn", "furn")
    s.label(26.33, 50.2, "PORTICO", None, size=0.85)
    s.planter(22.8, 50.6, 0.75)
    s.planter(29.86, 50.6, 0.75)

    # ---------- powder + stair core ----------
    s.toilet(XS - 0.2, 30.8, 90)
    s.counter(31.53, 28.6, 1.8, 4.4)
    s.basin(32.4, 30.8, 90)
    s.label(35.0, 33.2, "POWDER", None, size=0.75)
    # basement stair landing + down run (beneath)
    s.stairs(XS + 0.2, 27.4, W - 0.5 - XS - 0.2, 2.8, 3, "down", "treadlow")
    # main stair: flight 1 (L→R), landing, flight 2 (toward rear)
    s.stairs(34.5, 34.3, XS + 0.2 - 34.5, YF - 0.2 - 34.3, 4, "right")
    s.rect(XS + 0.2, 34.3, W - 0.5 - XS - 0.2, YF - 0.2 - 34.3, "landing", "fixture")
    s.stairs(XS + 0.2, 30.2, W - 0.5 - XS - 0.2, 4.1, 5, "up")
    s.poly([(XS + 0.2, 31.2), (W - 0.5, 29.6)], "breakln", "note")
    s.arrow([(33.4, 36.2), (39.6, 36.2), (39.6, 31.0)], "UP", 36.0, 37.6)
    s.arrow([(39.6, 25.9), (39.6, 29.4)])
    s.text(40.65, 25.5, "DN", "tag strong", "note")

    # ---------- study ----------
    s.rect(33.6, YF + 0.2, 7.9, 1.5, "builtin")                 # library wall
    s.rect(34.0, 46.0, 5.4, 2.4, "furn", "furn", rx=0.1)      # desk
    s.chair(36.7, 49.6, 2.0, back="b")
    s.label(36.6, 42.4, "STUDY", "10'-0\" × 13'-0\"", "OR GUEST SUITE", size=0.95)

    # ---------- annotations ----------
    s.hdim(-14.0, 0, W, "42'-0\"")
    s.vdim(-5.5, 0, D, "52'-0\"")
    s.hdim(54.6, 0, XA, ticks=[])
    s.hdim(54.6, XA, XB)
    s.hdim(54.6, XB, W)
    s.callout(26.33, 36.2, 1)
    s.callout(28.6, 22.4, 2)
    s.callout(13.4, 9.6, 3)
    s.callout(17.6, 26.3, 4)
    s.callout(36.8, 35.4, 5)
    s.callout(38.1, 10.6, 6)
    s.scalebar(0, 58.6)
    s.text(W, 59.1, "STREET", "streettxt", "note", anchor="end")
    return s.svg(VIEW, title="Main floor plan")


def second_floor():
    s = Sheet()
    s.rect(0.5, 0.5, XA - 0.7, 14.5, "carpet", "floor")
    s.rect(XA + 0.2, 20.7, W - XA - 0.7, YR - 20.5, "oak", "floor")
    s.rect(XA + 0.2, YR, XB - XA - 0.4, YF - YR - 0.2, "oak", "floor")
    s.rect(XB + 0.2, 34.3, W - XB - 0.7, YF - 34.5, "oak", "floor")
    s.rect(0.5, 15.4, 9.5, 11.6, "tile", "floor")
    s.rect(0.5, 27.4, 9.3, 6.0, "tile", "floor")
    s.rect(10.2, 27.4, XA - 10.4, 6.0, "tile", "floor")
    s.rect(XB + 0.2, 24.6, XS - XB - 0.4, 9.3, "tile", "floor")
    for x0, y0, w0, h0 in ((0.5, 37.7, 10.1, 13.8), (11.0, 37.7, XA - 11.2, 13.8), (XB + 0.2, YF + 0.2, W - XB - 0.7, D - YF - 0.7)):
        s.rect(x0, y0, w0, h0, "carpet", "floor")
    s.rect(10.4, 15.4, 6.6, 11.6, "carpet", "floor")
    s.rect(17.4, 15.4, XA - 17.6, 11.6, "oak", "floor")
    s.rect(4.6, 33.8, XA - 4.6, 3.5, "oak", "floor")

    # voids
    s.void(XA + 0.2, 0.5, W - XA - 0.7, 20.0)
    s.void(XA + 0.2, YF - 0.1, XB - XA - 0.4, YD - YF - 0.15)
    s.text(31.5, 10.0, "OPEN TO", "voidtxt", "label")
    s.text(31.5, 11.0, "GREAT ROOM", "voidtxt", "label")
    s.text(26.33, 42.3, "OPEN TO", "voidtxt", "label")
    s.text(26.33, 43.3, "FOYER", "voidtxt", "label")
    # roof below at the portico
    s.rect(XA + 0.25, YD + 0.25, XB - XA - 0.5, D - YD - 0.25, "roofbelow", "floor")
    s.rect(0, -12.5, XA, 12.5, "roofbelow", "floor")
    s.text(XA / 2, -6.6, "LOGGIA ROOF BELOW", "voidtxt", "label")
    s.text(XA / 2, -5.6, "STANDING-SEAM METAL", "voidtxt", "label")

    _shell(s, "upper")

    # guards
    s.line(XA + 0.2, 20.6, W - 0.5, 20.6, "guard", "wall")
    s.line(XA + 0.2, YF - 0.1, XB - 0.2, YF - 0.1, "guard", "wall")
    s.line(XS + 0.2, 34.3, W - 0.5, 34.3, "guard", "wall")

    # ---------- primary suite ----------
    s.vwall(XA, 0.5, 20.7, INT)
    s.vwall(XA, 20.7, 27.2, INT, [("dbl", 21.1, 25.1, {"side": -1})])
    s.hwall(15.2, 0.5, XA, INT, [("dbl", 3.25, 7.25, {"side": 1}), ("open", 17.8, 20.8, {"cased": True})])
    s.vwall(10.2, 15.2, 27.2, INT)
    s.vwall(17.2, 15.2, 27.2, INT, [("door", 22.6, 25.2, {"hinge": "b", "side": -1})])
    s.hwall(27.2, 0.5, XA, INT)
    # bedroom
    s.rug(6.4, 4.0, 12.2, 10.0)
    s.bed(12.5, 15.0, 6.6, 7.0, direction=-1)
    s.chair(3.3, 3.6, 2.6, back="l")
    s.chair(3.3, 7.6, 2.6, back="l")
    s.circle(5.6, 5.6, 0.8, "furn", "furn")
    s.label(12.5, 3.0, "PRIMARY BEDROOM", "20'-8\" × 14'-6\"")
    # ensuite
    s.freetub(2.5, 20.2, 5.6, 2.8, 90)
    s.counter(8.2, 16.0, 1.8, 6.6)
    s.basin(9.0, 17.6, 90)
    s.basin(9.0, 21.0, 90)
    s.shower(0.5, 23.2, 5.1, 3.8, "t")
    s.vwall(5.8, 23.0, 27.2, INT)
    s.hwall(23.0, 5.8, 10.2, INT, [("door", 6.6, 8.9, {"hinge": "a", "side": -1})])
    s.toilet(8.0, 26.95, 180)
    s.label(6.1, 19.0, "ENSUITE", "9'-6\" × 11'-8\"", size=0.8)
    # dressing room + entry gallery
    s.rect(10.4, 15.4, 1.9, 11.6, "shelf")
    s.rect(15.1, 15.4, 1.9, 11.6, "shelf")
    s.rect(11.8, 19.2, 2.8, 4.4, "island")
    s.label(13.7, 17.5, "DRESSING", None, size=0.7)
    s.label(19.2, 18.6, "ENTRY|GALLERY", None, size=0.7)

    # ---------- children's wing ----------
    s.vwall(XA, 27.2, YD - 0.25, INT, [("open", 33.6, 37.5)])
    s.vwall(10.0, 27.2, 33.6, INT)
    s.hwall(33.6, 0.5, XA, INT, [("door", 4.4, 7.0, {"hinge": "a", "side": -1}), ("door", 15.8, 18.4, {"hinge": "b", "side": -1})])
    s.vwall(4.6, 33.6, 37.5, INT, [("door", 34.0, 37.1, {"hinge": "a", "side": 1})])
    s.hwall(37.5, 0.5, XA, INT, [("door", 7.2, 9.9, {"hinge": "b", "side": 1}), ("door", 11.6, 14.3, {"hinge": "a", "side": 1})])
    s.vwall(10.8, 37.5, D - 0.5, INT)
    # bath
    s.tub(0.5, 27.4, 2.6, 5.4)
    s.counter(4.0, 27.4, 5.8, 1.8)
    s.basin(5.5, 28.3)
    s.basin(8.3, 28.3)
    s.toilet(9.8, 31.6, 90)
    s.label(5.6, 31.4, "BATH", None, size=0.75)
    s.rect(0.5, 33.8, 3.9, 3.5, "shelf")
    s.text(2.5, 35.8, "LINEN", "tag")
    # laundry
    s.appliance(10.4, 27.4, 2.6, 2.4, "W")
    s.appliance(13.1, 27.4, 2.6, 2.4, "D")
    s.counter(15.8, 27.4, XA - 16.0, 2.0)
    s.rect(17.4, 27.7, 1.8, 1.3, "fx", rx=0.15)
    s.label(15.6, 31.6, "LAUNDRY", "10'-11\" × 6'-0\"", size=0.75)
    s.text(12.8, 35.7, "HALL", "tag")
    # bedrooms 2 + 3
    s.rect(0.5, 37.7, 6.0, 2.0, "shelf")
    s.rect(15.0, 37.7, XA - 15.2, 2.0, "shelf")
    s.bed_x(0.5, 46.4, 4.6, 6.6, direction=1)
    s.bed_x(XA - 0.2, 46.4, 4.6, 6.6, direction=-1)
    s.label(6.5, 41.9, "BEDROOM 2", "10'-1\" × 13'-10\"", size=0.85)
    s.label(15.6, 41.9, "BEDROOM 3", "10'-1\" × 13'-10\"", size=0.85)

    # ---------- bridge + stair + bath + bedroom 4 ----------
    s.rect(XA + 0.2, 25.2, 1.2, 8.0, "shelf")
    s.chair(25.0, 29.2, 2.4, back="l")
    s.label(27.7, 31.9, "LIBRARY|BRIDGE", None, size=0.75)
    s.hwall(24.4, XB, XS + 0.2, INT)
    s.vwall(XB, 24.4, 34.3, INT, [("door", 28.0, 30.6, {"hinge": "a", "side": 1})])
    s.hwall(34.1, XB, XS + 0.2, INT)
    s.vwall(XS, 24.4, 34.3, INT)
    s.tub(XB + 0.2, 24.6, 5.9, 2.6)
    s.counter(XS - 2.0, 27.4, 1.8, 3.6)
    s.basin(XS - 1.1, 29.2, 90)
    s.toilet(XS - 0.2, 32.3, 90)
    s.label(34.0, 30.6, "BATH", None, size=0.75)
    s.stairs(XS + 0.2, 25.13, W - 0.5 - XS - 0.2, 9.17, 11, "down")
    s.arrow([(39.6, 23.2), (39.6, 30.0)], "DN", 40.8, 22.6)
    s.hwall(YF, XB, W - 0.5, INT, [("door", 38.8, 41.4, {"hinge": "b", "side": 1})])
    s.rect(XB + 0.2, 41.0, 2.0, 6.4, "shelf")
    s.bed_x(W - 0.5, 46.6, 4.6, 6.6, direction=-1)
    s.label(36.4, 41.6, "BEDROOM 4", "10'-0\" × 13'-0\"", size=0.85)
    s.text(36.4, 22.8, "GALLERY LANDING", "tag", "label")

    s.hdim(-14.0, 0, W, "42'-0\"")
    s.vdim(-5.5, 0, D, "52'-0\"")
    s.callout(28.6, 22.4, 7)
    s.callout(19.2, 21.8, 8)
    s.callout(3.0, 13.6, 9)
    s.callout(26.33, 36.0, 10)
    s.scalebar(0, 58.6)
    s.text(W, 59.1, "STREET", "streettxt", "note", anchor="end")
    return s.svg(VIEW, title="Second floor plan")


def lower_level():
    s = Sheet()
    f = FDN
    h = f / 2
    s.rect(f, f, W - 2 * f, YM - f, "oak", "floor")
    s.rect(XA + 0.2, YM - 0.2, W - XA - f - 0.2, YD - YM, "oak", "floor")
    s.rect(XB + 0.2, YD - 0.4, W - XB - f - 0.2, D - f - YD + 0.4, "oak", "floor")
    s.rect(0.67, 17.2, 20.46, 13.2, "garagefl", "floor")
    # foundation walls
    s.hwall(h, 0, W, f, [("win", 3.6, 8.4), ("win", 15.0, 19.0), ("win", 25.0, 29.0), ("win", 34.0, 38.0)])
    s.vwall(h, 0, YM + 0.2, f)
    s.hwall(YM, 0, XA + 0.2, f)
    s.vwall(XA, YM, D, f)
    s.vwall(W - h, 0, D, f, [("win", 46.4, 49.4)])
    s.hwall(D - h, XA, W, f, [("win", 34.0, 39.0)])
    # cold cellar under the portico
    s.hwall(YD, XA, XB, INT, [("door", 27.6, 30.2, {"hinge": "b", "side": 1})])
    s.rect(XA + 0.33, YD + 0.2, XB - XA - 0.53, D - YD - 0.53, "garagefl", "floor")
    s.label(26.33, 50.2, "COLD CELLAR", None, size=0.7)
    # unexcavated garage
    s.rect(0, YM + 0.33, XA - 0.33, D - YM - 0.33, "unex", "floor")
    s.line(0, YM + 0.33, XA - 0.33, D, "voidx", "floor")
    s.line(XA - 0.33, YM + 0.33, 0, D, "voidx", "floor")
    s.text(10.67, 41.4, "UNEXCAVATED", "voidtxt", "label")
    s.text(10.67, 42.4, "(GARAGE ABOVE)", "voidtxt", "label")

    # guest suite + gym + hall
    s.hwall(13.2, f, XA, INT, [("door", 4.2, 6.6, {"hinge": "b", "side": 1}),
                                ("door", 9.0, 11.6, {"hinge": "b", "side": -1}),
                                ("dbl", 14.6, 18.6, {"side": -1})])
    s.vwall(12.6, f, 13.2, INT)
    s.vwall(XA, f, 13.2, INT, cls="glasswall")
    s.hwall(17.0, 7.6, XA, INT, [("door", 17.8, 20.4, {"hinge": "b", "side": 1})])
    s.vwall(7.6, 13.2, 20.2, INT)
    s.hwall(20.2, f, 7.6, INT)
    s.vwall(XA, 17.0, YR, INT)
    s.bed_x(f, 6.6, 5.2, 6.8, direction=1)
    s.rect(9.8, f, 2.6, 6.0, "shelf")
    s.label(7.6, 10.7, "GUEST SUITE", "11'-11\" × 12'-6\"", size=0.85)
    s.shower(f, 16.6, 3.3, 3.4, "t")
    s.toilet(f, 14.2, -90)
    s.counter(5.6, 16.0, 1.8, 3.8)
    s.basin(6.5, 17.9, 90)
    s.text(2.9, 16.1, "BATH", "tag")
    s.label(14.4, 15.4, "LOWER HALL", None, size=0.65)
    s.rect(13.2, 1.4, 2.4, 5.2, "furn", "furn", rx=0.2)
    s.rect(17.4, 1.4, 2.4, 5.2, "furn", "furn", rx=0.2)
    s.rect(12.8, 1.4, 0.25, 10.8, "mirror", "fixture")
    s.label(16.9, 9.6, "GYM", "8'-4\" × 12'-6\"", "GLASS TO LOUNGE", size=0.85)
    # mechanical / storage
    s.rect(0.67, 20.4, 6.93, 10.0, "garagefl", "floor")
    s.rect(f, 13.4, 6.93, 6.6, "tile", "floor")
    s.rect(8.4, 18.0, 3.0, 3.0, "appl")
    s.text(9.9, 19.7, "FURN", "tag")
    s.rect(8.6, 22.2, 2.4, 2.4, "appl", rx=1.2)
    s.text(9.8, 23.6, "WH", "tag")
    s.rect(8.4, 25.6, 2.8, 1.8, "appl")
    s.text(9.8, 26.7, "HRV", "tag")
    s.rect(XA - 1.8, 21.0, 1.6, 7.4, "shelf")
    s.rect(14.0, 28.6, 6.9, 1.6, "shelf")
    s.label(15.6, 24.2, "MECHANICAL|+ STORAGE", None, size=0.7)

    # media lounge + bar
    s.hwall(YR, XA, XS + 0.2, INT, [("open", 27.2, XB - 0.2, {"cased": True}), ("dbl", 32.6, 36.4, {"side": -1})])
    s.hwall(YR, XS, W - f, INT, [("dbl", 38.4, 40.8, {"side": -1})])
    s.rect(39.6, 3.6, 1.7, 14.2, "builtin")
    s.rect(41.0, 5.4, 0.3, 10.6, "screen", "fixture")
    s.rug(27.4, 4.4, 10.8, 12.6)
    s.sofa(27.6, 4.6, 3.2, 12.2, back="l")
    s.sofa(30.8, 4.6, 6.2, 2.8, back="t")
    s.sofa(30.8, 14.0, 6.2, 2.8, back="b")
    s.rect(32.4, 8.8, 2.8, 3.8, "furn", "furn", rx=0.2)
    s.counter(XA + 0.2, 17.4, 2.0, 6.6)
    s.rect(21.9, 19.9, 1.3, 1.3, "fx", rx=0.15)
    s.rect(24.4, 17.8, 2.0, 5.4, "island")
    for k in range(3):
        s.stool(27.3, 18.7 + k * 1.8)
    s.label(32.2, 2.4, "MEDIA LOUNGE", "20'-0\" × 23'-4\"")
    s.text(26.6, 16.9, "WET BAR", "tag strong", "label")
    s.text(39.6, 26.2, "AV", "tag", "label")

    # games / wine / stair hall / flex
    s.vwall(XB, YR, 30.6, INT, cls="glasswall")
    s.hwall(30.6, XB, XS + 0.2, INT)
    s.vwall(XS, YR, YF + 2.43, INT)
    for k in range(5):
        s.rect(XB + 0.45 + k * 1.15, YR + 0.4, 0.9, 1.6, "shelf")
    s.rect(32.6, 26.8, 3.6, 2.0, "furn", "furn", rx=0.2)
    s.label(33.8, 29.6, "WINE ROOM", None, size=0.7)
    s.vwall(XB, 30.6, D - f, INT, [("door", 31.2, 33.8, {"hinge": "a", "side": 1}), ("open", 40.73, 44.0)])
    s.hwall(40.53, XB, XS + 0.2, INT)
    s.label(34.5, 36.4, "STORAGE", None, size=0.65)
    s.rect(22.2, 26.4, 2.2, 18.4, "furn", "furn", rx=0.3)
    s.rect(22.5, 26.8, 1.6, 17.6, "furnline", "furn", rx=0.2)
    s.chair(28.6, 30.4, 2.2, back="r")
    s.chair(28.6, 37.4, 2.2, back="r")
    s.label(27.6, 34.0, "GAMES", "9'-7\" × 22'-6\"", "SHUFFLEBOARD", size=0.85)
    s.stairs(XS + 0.2, 27.4, W - f - XS - 0.2, 13.33, 16, "up")
    s.arrow([(39.6, 39.6), (39.6, 29.0)], "UP", 39.6, 42.6)
    s.hwall(44.2, XB, W - f, INT, [("door", 32.4, 35.0, {"hinge": "a", "side": 1})])
    s.rect(36.6, 47.8, 4.4, 3.4, "furn", "furn", rx=0.2)
    s.label(36.4, 46.0, "HOBBY / BUNK", "9'-10\" × 7'-0\"", size=0.75)

    s.hdim(-2.0, 0, W, "42'-0\"")
    s.vdim(-5.5, 0, D, "52'-0\"")
    s.callout(16.9, 6.8, 11)
    s.callout(23.0, 15.4, 12)
    s.callout(36.2, 29.4, 13)
    s.scalebar(0, 58.6)
    s.text(W, 59.1, "STREET", "streettxt", "note", anchor="end")
    return s.svg(VIEW_LOWER, title="Lower level plan")
