"""Building model for Villa Gooch (2316 Gooch Street, Dallas TX 75241).

Units are feet. X runs left to right as seen from Gooch Street, Y runs from the
front facade (Y=0) back toward the garden, Z is height above Level 1 finished floor.
The house is 50'-0" wide x 54'-0" deep on an assumed 60' x 145' lot (0.20 ac).
"""

# ------------------------------------------------------------------ datums
LV = {1: 0.0, 2: 11.0, 3: 22.0}          # finished floor of each level
ROOF, PARAPET, LANTERN_TOP, GRADE = 33.0, 34.5, 37.0, -0.67
CUT = 4.0                                 # plan cut height above each floor

EXT_T, INT_T, PARTY_T, GL_T, GUARD_T = 0.75, 0.42, 0.5, 0.2, 0.12

# Stair: stacked straight flights along the lantern's left wall, 18 risers @ 7.33",
# 17 treads @ 11" per 11'-0" floor. A glass bridge on Level 2 returns to the front.
RISERS, TREAD = 18, 11 / 12
RISER = 11.0 / RISERS
ST_X0, ST_X1 = 0.75, 4.42
ST_Y0 = 4.0
ST_Y1 = ST_Y0 + (RISERS - 1) * TREAD     # 19.58
CAT_X1 = 8.08                            # east edge of the Level 2 bridge
ELEV = (14.2, 18.5, 19.5, 24.0)          # elevator shaft


def Wl(o, c, a, b, t=INT_T, k='int'):
    """Axis-aligned wall: o='h' runs along X at Y=c, o='v' runs along Y at X=c."""
    return dict(o=o, c=c, a=a, b=b, t=t, k=k)


def Op(o, c, a, b, typ, **kw):
    d = dict(o=o, c=c, a=a, b=b, typ=typ)
    d.update(kw)
    return d


# ------------------------------------------------- exterior openings (3D)
# Shared by the plans (cut at each level), the elevations and the schedules.
# lvl 0 = lantern element that runs through all three levels.
EXT_OPS = [
    Op('v', 0, 1.75, 3.25, 'slot', lvl=0, z0=0, z1=35, desc='Full-height glazed light slot at lantern front'),
    Op('v', 0, 20, 23, 'slot', lvl=0, z0=0, z1=35, desc='Full-height glazed light slot at stair landings'),
    # Level 1
    Op('h', 0, 5, 9, 'pivot', lvl=1, z0=0, z1=10, hinge='a', swing=1, room='Foyer',
       desc='Pivot entry door, rift white oak, concealed pivot, 4\'-0" x 10\'-0"'),
    Op('h', 0, 15, 26, 'fixed', lvl=1, z0=0, z1=10, room='Office', desc='Fixed storefront behind wood fin screen'),
    Op('h', 0, 29.5, 47.5, 'garage', lvl=1, z0=0, z1=8, room='Garage',
       desc='Insulated overhead door, bronze frame, satin-etched glass'),
    Op('v', 0, 26, 35, 'win', lvl=1, z0=7.5, z1=10, room='Living', desc='Clerestory awning'),
    Op('v', 0, 47, 52.5, 'fixed', lvl=1, z0=0, z1=10, room='Living', desc='Floor-to-ceiling corner light'),
    Op('v', 50, 15.5, 18.5, 'door', lvl=1, z0=0, z1=7, hinge='b', swing=-1, room='Garage',
       desc='Insulated steel side door to service yard'),
    Op('v', 50, 26, 31, 'win', lvl=1, z0=4, z1=7, room='Scullery', desc='Casement over prep sink'),
    Op('v', 50, 47, 52.5, 'fixed', lvl=1, z0=0, z1=10, room='Kitchen', desc='Floor-to-ceiling corner light'),
    Op('h', 54, 1.0, 11.75, 'slider', lvl=1, z0=0, z1=10, room='Living', desc='Lift-slide, pocketing, to loggia'),
    Op('h', 54, 13.25, 24.25, 'slider', lvl=1, z0=0, z1=10, room='Living / Dining', desc='Lift-slide, pocketing, to loggia'),
    Op('h', 54, 25.75, 36.75, 'slider', lvl=1, z0=0, z1=10, room='Dining / Kitchen', desc='Lift-slide, pocketing, to loggia'),
    Op('h', 54, 38.25, 49.0, 'slider', lvl=1, z0=0, z1=10, room='Kitchen', desc='Lift-slide, pocketing, to outdoor kitchen'),
    # Level 2
    Op('h', 6, 15, 37.75, 'slider', lvl=2, z0=11, z1=21, room='Family Lounge', desc='Lift-slide to covered front balcony',
       mull=[20.67, 26.33, 32.0]),
    Op('h', 6, 38.25, 48.5, 'slider', lvl=2, z0=11, z1=21, room='Study', desc='Lift-slide to covered front balcony',
       mull=[43.25]),
    Op('v', 0, 24.5, 27.5, 'fixed', lvl=2, z0=11, z1=21, room='Hall', desc='Full-height hall slot'),
    Op('v', 0, 29, 33, 'win', lvl=2, z0=17.5, z1=21, room='Bath 2', desc='High awning, obscure glass'),
    Op('v', 0, 47, 52.5, 'win', lvl=2, z0=14, z1=21, room='Bedroom 2',
       desc='Egress casement over fritted fixed lower lite'),
    Op('v', 50, 8.5, 14.5, 'win', lvl=2, z0=14, z1=21, room='Study', desc='Casement pair'),
    Op('v', 50, 19, 23, 'win', lvl=2, z0=17.5, z1=21, room='Laundry', desc='High awning'),
    Op('v', 50, 29, 33, 'win', lvl=2, z0=17.5, z1=21, room='Bath 5', desc='High awning, obscure glass'),
    Op('v', 50, 47, 52.5, 'win', lvl=2, z0=14, z1=21, room='Bedroom 5',
       desc='Egress casement over fritted fixed lower lite'),
    Op('h', 54, 2.25, 10.25, 'slider', lvl=2, z0=11, z1=21, room='Bedroom 2', desc='Lift-slide to rear terrace'),
    Op('h', 54, 14.75, 22.75, 'slider', lvl=2, z0=11, z1=21, room='Bedroom 3', desc='Lift-slide to rear terrace'),
    Op('h', 54, 27.25, 35.25, 'slider', lvl=2, z0=11, z1=21, room='Bedroom 4', desc='Lift-slide to rear terrace'),
    Op('h', 54, 39.75, 47.75, 'slider', lvl=2, z0=11, z1=21, room='Bedroom 5', desc='Lift-slide to rear terrace'),
    # Level 3
    Op('h', 6, 15, 31.75, 'slider', lvl=3, z0=22, z1=31, room='Bedroom 6', desc='Lift-slide to front terrace',
       mull=[20.67, 26.33]),
    Op('h', 6, 32.25, 48.5, 'slider', lvl=3, z0=22, z1=31, room='Bedroom 7', desc='Lift-slide to front terrace',
       mull=[38.0, 43.25]),
    Op('v', 0, 24.5, 27.5, 'fixed', lvl=3, z0=22, z1=31, room='Hall', desc='Full-height hall slot'),
    Op('v', 0, 29, 44, 'win', lvl=3, z0=28.5, z1=31, room='Dressing Room', desc='Ribbon clerestory'),
    Op('v', 50, 8.5, 14.5, 'win', lvl=3, z0=25, z1=31, room='Bedroom 7', desc='Egress casement pair'),
    Op('v', 50, 19, 23, 'win', lvl=3, z0=28.5, z1=31, room='Bath 7', desc='High awning, obscure glass'),
    Op('v', 50, 29, 44, 'win', lvl=3, z0=28.5, z1=31, room='Primary Bath', desc='Ribbon clerestory'),
    Op('h', 46, 2.5, 11.5, 'win', lvl=3, z0=28.5, z1=31, room='Dressing Room', desc='Ribbon clerestory'),
    Op('h', 46, 16, 34, 'slider', lvl=3, z0=22, z1=31, room='Primary Bedroom', desc='Lift-slide, pocketing, to primary terrace'),
    Op('h', 46, 38.5, 47.5, 'fixed', lvl=3, z0=25, z1=31, room='Primary Bath',
       desc='Fixed picture window at tub, switchable (PDLC) privacy glass'),
    # appended so earlier marks keep their numbers
    Op('v', 0, 4.5, 19.5, 'slot', lvl=0, z0=11, z1=35, room='Lantern',
       desc='Translucent low-iron channel-glass band along the stair, bronze caps'),
    Op('h', 0, 29.5, 47.5, 'fixed', lvl=1, z0=8, z1=10, room='Garage', desc='Satin-etched transom in garage door frame'),
]
for _o in EXT_OPS:
    if _o['o'] == 'h':
        _o['n'] = '-y' if _o['c'] < 27 else '+y'
    else:
        _o['n'] = '-x' if _o['c'] < 25 else '+x'

# Lantern curtain wall (front of the stair lantern, full height).
LANTERN_CW = dict(o='h', c=0, a=1.25, b=12.75, z0=0, z1=35.5, typ='cw', n='-y',
                  mull_u=[5, 9], spandrels=[(10, 11), (21, 22)])

# ---------------------------------------------------------------- walls
FRONT_JAMBS = [(0, -1.5, 1.25, 0.75), (12.75, -1.5, 14, 0.75)]   # bronze lantern frame

WALLS = {
    1: [
        Wl('v', 0.375, 0, 54, EXT_T, 'ext'),
        Wl('h', 0.165, 1.25, 12.75, 0.33, 'cw'),
        Wl('h', 0.375, 14, 50, EXT_T, 'ext'),
        Wl('v', 49.625, 0, 54, EXT_T, 'ext'),
        Wl('h', 53.625, 0, 50, EXT_T, 'ext'),
        Wl('v', 14.1, 0.75, 13.5, GL_T, 'glass'),      # office glass wall
        Wl('h', 13.5, 14, 27),
        Wl('v', 14.2, 13.5, 24),                       # coat closet + elevator west
        Wl('h', 18.5, 14.2, 19.5),
        Wl('v', 19.5, 13.5, 24),
        Wl('h', 24, 14.2, 19.5),
        Wl('h', 19, 19.5, 27),
        Wl('v', 27, 0.75, 32, PARTY_T),                # garage separation (Type X)
        Wl('h', 24, 27, 49.25, PARTY_T),
        Wl('v', 36, 24, 32),
        Wl('h', 32, 27, 49.25),
        Wl('h', 12, 0.75, 4.42, 0.15, 'glass'),        # wine room under the stair
        Wl('v', 4.42, 12, ST_Y1, 0.15, 'glass'),
        Wl('v', ST_X1, ST_Y0, 12, GUARD_T, 'guard'),
        Wl('v', 46.25, 19.25, 23.75), Wl('h', 19.25, 46.25, 49.25),   # garage mech closet (AHU-1)
    ],
    2: [
        Wl('v', 0.375, 0, 54, EXT_T, 'ext'),
        Wl('h', 0.165, 1.25, 12.75, 0.33, 'cw'),
        Wl('v', 14.0, 0.75, 6.375, 0.5, 'ext'),
        Wl('h', 6.375, 14, 50, EXT_T, 'ext'),
        Wl('v', 49.375, 0, 6, 1.25, 'ext'),            # stone cheek wall
        Wl('v', 49.625, 6, 54, EXT_T, 'ext'),
        Wl('h', 53.625, 0, 50, EXT_T, 'ext'),
        Wl('v', 14.1, 6.75, 18.5, GL_T, 'glass'),      # lounge glass over the void
        Wl('v', 14.2, 18.5, 24),
        Wl('h', 18.5, 14.2, 19.5),
        Wl('v', 19.5, 18.5, 24),
        Wl('h', 24, 14.2, 49.25),
        Wl('v', 38, 6.75, 24),
        Wl('h', 15, 38, 49.25),
        Wl('h', 28, 0.75, 49.25),
        Wl('v', 12.5, 28, 53.25, PARTY_T), Wl('v', 25, 28, 53.25, PARTY_T), Wl('v', 37.5, 28, 53.25, PARTY_T),
        Wl('v', 9, 28, 41.0), Wl('h', 36, 0.75, 9), Wl('h', 41.0, 0.75, 9),
        Wl('v', 16, 28, 41.0), Wl('h', 36, 16, 24.75), Wl('h', 41.0, 16, 24.75),
        Wl('v', 34, 28, 41.0), Wl('h', 36, 25.25, 34), Wl('h', 41.0, 25.25, 34),
        Wl('v', 41, 28, 41.0), Wl('h', 36, 41, 49.25), Wl('h', 41.0, 41, 49.25),
        Wl('v', 44, 24, 28),
        Wl('v', CAT_X1, 0.5, ST_Y1, GUARD_T, 'guard'),
        Wl('h', ST_Y1, CAT_X1, 14.0, GUARD_T, 'guard'),
        Wl('v', ST_X1, ST_Y0 + 2, ST_Y1, GUARD_T, 'guard'),
    ],
    3: [
        Wl('v', 0.375, 0, 46, EXT_T, 'ext'),
        Wl('h', 0.165, 1.25, 12.75, 0.33, 'cw'),
        Wl('v', 14.0, 0.75, 6.375, 0.5, 'ext'),
        Wl('h', 6.375, 14, 50, EXT_T, 'ext'),
        Wl('v', 49.375, 0, 6, 1.25, 'ext'),
        Wl('v', 49.625, 6, 46, EXT_T, 'ext'),
        Wl('h', 45.625, 0, 50, EXT_T, 'ext'),
        Wl('v', 14.2, 6.375, 24),
        Wl('h', 18.5, 14.2, 19.5),
        Wl('v', 19.5, 17.5, 24),
        Wl('h', 17.5, 19.5, 49.25),
        Wl('v', 27, 17.5, 24),
        Wl('v', 32, 6.375, 24, PARTY_T),
        Wl('v', 39, 17.5, 24),
        Wl('h', 24, 14.2, 49.25),
        Wl('v', 39.5, 24, 28),
        Wl('h', 28, 0.75, 49.25),
        Wl('v', 14, 28, 45.25),
        Wl('v', 36, 28, 45.25),
        Wl('v', 45, 28.2, 33), Wl('h', 33, 45, 49.25),
        Wl('h', 34, 36.2, 41.5, 0.15, 'glass'), Wl('v', 41.5, 28.2, 34, 0.15, 'glass'),
        Wl('h', ST_Y1, ST_X1, 14.2, GUARD_T, 'guard'),
        Wl('v', ST_X1, ST_Y0, ST_Y1, GUARD_T, 'guard'),
    ],
}

# ------------------------------------------------------------ interior doors
DOORS = {
    1: [
        Op('v', 14.1, 9.5, 12.5, 'swing', hinge='b', swing=1, room='Office', kind='Glass swing', size=(3, 9),
           note='Tempered glass in bronze frame, pivot hinges'),
        Op('v', 14.2, 14, 18, 'bifold', swing=-1, room='Coat Closet', kind='Bifold pair', size=(4, 8)),
        Op('v', 14.2, 20.0, 23.0, 'elev', room='Elevator', kind='Elevator entrance', size=(3, 7)),
        Op('h', 19, 20.25, 22.92, 'pocket', room='Powder', kind='Pocket', size=(2.67, 8)),
        Op('v', 46.25, 20.0, 22.67, 'swing', hinge='a', swing=-1, room='Garage Mech', kind='20-min self-closing',
           size=(2.67, 8), note='Steel, 20-min, self-closing (AHU-1 closet)'),
        Op('h', 24, 29, 32, 'swing', hinge='a', swing=1, room='Mudroom', kind='20-min self-closing', size=(3, 8),
           note='20-min rated, self-closing, gasketed; garage separation'),
        Op('v', 27, 25, 29, 'cased', room='Mudroom', kind='Cased opening', size=(4, 8)),
        Op('v', 36, 26, 29, 'pocket', room='Scullery', kind='Pocket', size=(3, 8)),
        Op('h', 32, 44, 47, 'cased', room='Scullery', kind='Cased opening', size=(3, 8)),
        Op('v', 4.42, 15, 17.5, 'swing', hinge='a', swing=-1, room='Wine Room', kind='Glass swing, insulated', size=(2.5, 7),
           note='Insulated tempered glass, gasketed, bronze frame'),
    ],
    2: [
        Op('v', 14.2, 20.0, 23.0, 'elev', room='Elevator', kind='Elevator entrance', size=(3, 7)),
        Op('h', 24, 20, 25, 'cased', room='Family Lounge', kind='Cased opening', size=(5, 9)),
        Op('h', 24, 40, 43, 'swing', hinge='b', swing=-1, room='Laundry', kind='Flush swing', size=(3, 8)),
        Op('v', 38, 7.25, 9.75, 'swing', hinge='a', swing=1, room='Study', kind='Flush swing', size=(2.5, 8)),
        Op('v', 44, 24.5, 27.5, 'swing', hinge='a', swing=-1, room='Mech / Linen', kind='Louvered swing', size=(3, 8),
           note='Louvered, paint-grade; out-swinging (AHU-2 closet)'),
        Op('h', 28, 9.33, 12.0, 'swing', hinge='b', swing=1, room='Bedroom 2', kind='Flush swing', size=(2.67, 8)),
        Op('h', 28, 13.0, 15.67, 'swing', hinge='a', swing=1, room='Bedroom 3', kind='Flush swing', size=(2.67, 8)),
        Op('h', 28, 34.33, 37.0, 'swing', hinge='b', swing=1, room='Bedroom 4', kind='Flush swing', size=(2.67, 8)),
        Op('h', 28, 38.0, 40.67, 'swing', hinge='a', swing=1, room='Bedroom 5', kind='Flush swing', size=(2.67, 8)),
        Op('v', 9, 30, 32.5, 'pocket', room='Bath 2', kind='Pocket', size=(2.5, 8)),
        Op('v', 16, 30, 32.5, 'pocket', room='Bath 3', kind='Pocket', size=(2.5, 8)),
        Op('v', 34, 30, 32.5, 'pocket', room='Bath 4', kind='Pocket', size=(2.5, 8)),
        Op('v', 41, 30, 32.5, 'pocket', room='Bath 5', kind='Pocket', size=(2.5, 8)),
        Op('v', 9, 36.4, 38.6, 'cased', room='Closet 2', kind='Cased opening', size=(2.2, 8)),
        Op('v', 16, 36.4, 38.6, 'cased', room='Closet 3', kind='Cased opening', size=(2.2, 8)),
        Op('v', 34, 36.4, 38.6, 'cased', room='Closet 4', kind='Cased opening', size=(2.2, 8)),
        Op('v', 41, 36.4, 38.6, 'cased', room='Closet 5', kind='Cased opening', size=(2.2, 8)),
    ],
    3: [
        Op('v', 14.2, 20.0, 23.0, 'elev', room='Elevator', kind='Elevator entrance', size=(3, 7)),
        Op('h', 17.5, 28, 31, 'cased', room='Bedroom 6', kind='Cased opening', size=(3, 8)),
        Op('h', 17.5, 33, 36, 'cased', room='Bedroom 7', kind='Cased opening', size=(3, 8)),
        Op('v', 27, 21.1, 23.6, 'pocket', room='Bath 6', kind='Pocket', size=(2.5, 8), tag_at=(25.9, 22.4)),
        Op('v', 39, 19.6, 22.27, 'swing', hinge='b', swing=1, room='Bath 7', kind='Flush swing', size=(2.67, 8)),
        Op('h', 24, 27.42, 29.92, 'swing', hinge='b', swing=-1, room='Bedroom 6', kind='Flush swing', size=(2.5, 8)),
        Op('h', 24, 34.5, 37.17, 'swing', hinge='b', swing=-1, room='Bedroom 7', kind='Flush swing', size=(2.67, 8)),
        Op('v', 39.5, 24.5, 27.17, 'swing', hinge='a', swing=-1, room='Mech / Storage', kind='Louvered swing',
           size=(2.67, 8), note='Louvered, paint-grade; out-swinging for AHU service'),
        Op('h', 28, 15, 19, 'double', swing=1, room='Primary Suite', kind='Pair, rift oak', size=(4, 9)),
        Op('v', 14, 29.5, 32.5, 'swing', hinge='a', swing=-1, room='Dressing Room', kind='Rift oak flush, 9 ft',
           size=(3, 9), note='Rift white oak, flush, concealed hinges'),
        Op('v', 36, 38.2, 41.2, 'pocket', room='Primary Bath', kind='Pocket, rift oak', size=(3, 9)),
        Op('h', 33, 45.3, 47.63, 'swing', hinge='a', swing=1, room='Primary WC', kind='Flush swing', size=(2.33, 8)),
        Op('h', 34, 38.75, 40.75, 'swing', hinge='a', swing=1, room='Primary Shower', kind='Frameless glass', size=(2, 7.5),
           note='3/8" tempered frameless, pivot hinges'),
    ],
}

# ------------------------------------------------------------------ rooms
# name, rect (x0, y0, x1, y1), label point, zone, finish key
def Rm(num, name, rect, at=None, zone='social', fin='living', dims=True, area=None, sub=None, size=None):
    return dict(num=num, name=name, rect=rect, at=at, zone=zone, fin=fin, dims=dims, area=area, sub=sub, size=size)


ROOMS = {
    1: [
        Rm('101', 'FOYER', (0.75, 0.33, 14, 24), at=(9.4, 16.2), zone='social', fin='foyer', sub='STAIR LANTERN · 35\'-6" CLG.', dims=False),
        Rm('102', 'OFFICE', (14.2, 0.75, 26.75, 13.29), at=(20.5, 12.0), zone='social', fin='living'),
        Rm('103', 'COAT', (14.41, 13.71, 19.29, 18.29), at=(16.9, 16.2), zone='service', fin='closet', dims=False, size=8),
        Rm('104', 'ELEV.', (14.41, 18.71, 19.29, 23.79), at=(16.85, 21.1), zone='service', fin='elev', dims=False, size=8),
        Rm('105', 'POWDER', (19.71, 13.71, 26.75, 18.79), at=(23.4, 15.4), zone='service', fin='bath', dims=False, size=8.5),
        Rm('106', 'BAR', (19.71, 19.21, 26.75, 24), at=(22.4, 22.1), zone='social', fin='living', dims=False, size=8.5),
        Rm('107', 'WINE', (0.75, 12, 4.42, ST_Y1), at=None, zone='social', fin='wine', dims=False),
        Rm('108', 'LIVING', (0.75, 24, 16, 53.25), at=(8.4, 29.6), zone='social', fin='living'),
        Rm('109', 'DINING', (16, 32, 30, 53.25), at=(22.5, 50.6), zone='social', fin='living'),
        Rm('110', 'KITCHEN', (30, 32.21, 49.25, 53.25), at=(39, 50.6), zone='social', fin='kitchen'),
        Rm('111', 'SCULLERY / PANTRY', (36.21, 24.25, 49.25, 31.79), at=(41.6, 28.9), zone='service', fin='kitchen', size=9),
        Rm('112', 'MUDROOM', (27.25, 24.25, 35.79, 31.79), at=(31.4, 28.1), zone='service', fin='mud', size=9),
        Rm('113', 'GARAGE', (27.25, 0.75, 49.25, 23.75), at=(38.3, 22.0), zone='garage', fin='garage'),
        Rm('114', 'COVERED LOGGIA', (0, 54, 50, 66), at=(23.5, 64.3), zone='outdoor', fin='deck', area=0),
    ],
    2: [
        Rm('201', 'GLASS BRIDGE', (0.75, 0.33, 8.08, 24), at=None, zone='social', fin='foyer', dims=False),
        Rm('202', 'FAMILY LOUNGE', (14.2, 6.75, 37.79, 23.79), at=(22.8, 16.6), zone='family', fin='living', sub='WINE BAR · FIREPLACE'),
        Rm('203', 'STUDY', (38.21, 6.75, 49.25, 14.79), at=(43.6, 12.6), zone='family', fin='living', size=9.5),
        Rm('204', 'LAUNDRY', (38.21, 15.21, 49.25, 23.79), at=(42.6, 19.9), zone='service', fin='mud', size=9.5),
        Rm('205', 'HALL', (0.75, 24, 44, 28), at=(30.2, 26.2), zone='circ', fin='living', dims=False, size=8.5),
        Rm('206', 'BEDROOM 2', (0.75, 41.0, 12.25, 53.25), at=(6.5, 50.9), zone='bed', fin='bed', size=9.5),
        Rm('207', 'BEDROOM 3', (12.75, 41.0, 24.75, 53.25), at=(18.75, 50.9), zone='bed', fin='bed', size=9.5),
        Rm('208', 'BEDROOM 4', (25.25, 41.0, 37.25, 53.25), at=(31.25, 50.9), zone='bed', fin='bed', size=9.5),
        Rm('209', 'BEDROOM 5', (37.75, 41.0, 49.25, 53.25), at=(43.5, 50.9), zone='bed', fin='bed', size=9.5),
        Rm('210', 'BATH 2', (0.75, 28.21, 8.79, 35.79), at=None, zone='service', fin='bath', dims=False),
        Rm('211', 'BATH 3', (16.21, 28.21, 24.79, 35.79), at=None, zone='service', fin='bath', dims=False),
        Rm('212', 'BATH 4', (25.21, 28.21, 33.79, 35.79), at=None, zone='service', fin='bath', dims=False),
        Rm('213', 'BATH 5', (41.21, 28.21, 49.25, 35.79), at=None, zone='service', fin='bath', dims=False),
        Rm('214', 'MECH / LINEN', (44.21, 24.21, 49.25, 27.79), at=None, zone='service', fin='mech', dims=False, size=7.5),
        Rm('215', 'FRONT BALCONY', (14, 0, 48.75, 6), at=(31.5, 3.3), zone='outdoor', fin='deck', area=0, dims=False, size=9),
        Rm('216', 'REAR TERRACE', (0, 54, 50, 60), at=(10.8, 56.2), zone='outdoor', fin='deck', area=0, dims=False, size=7.5),
        Rm('217', 'GREEN ROOF', (0, 60, 50, 66), at=(25, 63.3), zone='outdoor', fin='green', area=0, dims=False, size=8.5),
    ],
    3: [
        Rm('301', 'LANDING', (0.75, ST_Y1, 14, 24), at=(9.2, 22.4), zone='circ', fin='foyer', dims=False, size=8.5),
        Rm('302', 'BEDROOM 6', (14.41, 6.75, 31.75, 17.29), at=(23.0, 9.3), zone='bed', fin='bed'),
        Rm('303', 'BATH 6', (19.71, 17.71, 26.79, 23.79), at=None, zone='service', fin='bath', dims=False),
        Rm('304', 'BEDROOM 7', (32.25, 6.75, 49.25, 17.29), at=(40.9, 9.3), zone='bed', fin='bed'),
        Rm('305', 'BATH 7', (39.21, 17.71, 49.25, 23.79), at=None, zone='service', fin='bath', dims=False),
        Rm('306', 'HALL', (0.75, 24, 39.5, 28), at=(26.0, 26.2), zone='circ', fin='living', dims=False, size=8.5),
        Rm('307', 'MECH.', (39.71, 24.21, 49.25, 27.79), at=None, zone='service', fin='mech', dims=False, size=7.5),
        Rm('308', 'PRIMARY BEDROOM', (14.21, 28.21, 35.79, 45.25), at=(29.0, 41.4), zone='primary', fin='bed'),
        Rm('309', 'DRESSING ROOM', (0.75, 28.21, 13.79, 45.25), at=(7.3, 41.6), zone='primary', fin='dressing', size=9.5),
        Rm('310', 'SPA BATH', (36.21, 28.21, 49.25, 45.25), at=(44.0, 38.4), zone='primary', fin='spa', size=9.5),
        Rm('311', 'FRONT TERRACES', (14, 0, 48.75, 6), at=(27.5, 3.2), zone='outdoor', fin='deck', area=0, dims=False, size=8.5),
        Rm('312', 'PRIMARY TERRACE', (0, 46, 50, 54), at=(34.0, 51.8), zone='outdoor', fin='deck', area=0, dims=False),
    ],
}

# Finish key -> (floor, base, walls, ceiling, ceiling height)
FINISHES = {
    'foyer': ('F2', 'B1', 'P2', 'C1', 'TRIPLE HT.'),
    'living': ('F1', 'B1', 'P1', 'C1', "10'-0\""),
    'kitchen': ('F2', 'B1', 'P1 / T1', 'C1', "10'-0\""),
    'bath': ('F3', 'B2', 'T1 / P1', 'C1', "9'-0\""),
    'bed': ('F1', 'B1', 'P1', 'C1', "10'-0\""),
    'closet': ('F1', 'B1', 'P1 / W1', 'C1', "9'-0\""),
    'dressing': ('F1', 'B1', 'P1 / W1', 'C1', "10'-0\""),
    'spa': ('F3', 'B2', 'T1 / P1', 'C1', "10'-0\""),
    'mud': ('F2', 'B2', 'P1', 'C1', "9'-0\""),
    'garage': ('F4', '-', 'P3', 'C3', "10'-0\""),
    'mech': ('F4', '-', 'P3', 'C1', "9'-0\""),
    'elev': ('F2', '-', 'W1', 'BY MFR.', '-'),
    'wine': ('F2', '-', 'GYP + W1 / GLASS', 'GYP + W1', 'VARIES'),
    'deck': ('F5', '-', '-', 'C2', 'VARIES'),
    'green': ('F6', '-', '-', '-', '-'),
}

FINISH_KEY = [
    ('F1', 'Wide-plank European white oak, engineered 10" plank, matte natural oil'),
    ('F2', 'Porcelain 48"x48", warm limestone finish, 1/16" joints'),
    ('F3', 'Book-matched porcelain slab floor, honed, sloped to linear drains'),
    ('F4', 'Sealed concrete with flake epoxy coating'),
    ('F5', 'Exterior porcelain pavers 24"x48" on pedestals over waterproofing'),
    ('F6', 'Extensive sedum tray green roof over root barrier'),
    ('B1', 'Flush reveal base (shadow line), painted'),
    ('B2', 'Porcelain cove base to match floor'),
    ('P1', 'Level 5 gypsum board, eggshell paint, warm white'),
    ('P2', 'Venetian lime plaster, hand-troweled, feature walls'),
    ('P3', '5/8" Type X gypsum board, painted (garage/dwelling separation)'),
    ('T1', 'Book-matched porcelain slab walls / backsplash, full height'),
    ('W1', 'Rift white oak paneling and millwork'),
    ('C1', 'Level 5 gypsum board ceiling, flat white, recessed trimless lighting'),
    ('C2', 'Exterior thermally-modified wood slat soffit with LED cove'),
    ('C3', '5/8" Type X gypsum board ceiling (habitable space above)'),
]

ZONE_COLORS = {
    'social': ('#d9b88f', 'Living & entertaining'),
    'family': ('#c9a2a0', 'Family lounge & study'),
    'bed': ('#a9b7c9', 'Bedroom suites'),
    'primary': ('#8fa58a', 'Primary retreat'),
    'service': ('#d8d4cc', 'Service & baths'),
    'circ': ('#ece7de', 'Circulation'),
    'garage': ('#bdbab4', 'Garage'),
    'outdoor': ('#e6efd9', 'Terraces & loggia'),
}

# --------------------------------------------------------------- massing
# Boxes drive the elevations, shadows, sections and roof plan.
def Bx(n, x0, x1, y0, y1, z0, z1, m='stone', f=None, cast=True, grp=None):
    return dict(n=n, x0=x0, x1=x1, y0=y0, y1=y1, z0=z0, z1=z1, m=m, f=f or {}, cast=cast, grp=grp or n)


BOXES = [
    Bx('lantern', 0, 14, 0, 24, GRADE, 35.5, 'bronze', grp='lantern'),
    Bx('jambL', 0, 1.25, -1.5, 0, GRADE, LANTERN_TOP, 'bronze', grp='lantern'),
    Bx('jambR', 12.75, 14, -1.5, 0, GRADE, LANTERN_TOP, 'bronze', grp='lantern'),
    Bx('lanternHead', 0, 14, -1.5, 24, 35.5, LANTERN_TOP, 'bronze', grp='lantern'),
    Bx('canopy', 2.5, 11.5, -5, 0, 9.5, 10, 'bronze', grp='lantern'),
    Bx('L1', 14, 50, 0, 54, GRADE, 10, 'stone', grp='base'),
    Bx('L1w', 0, 14, 24, 54, GRADE, 10, 'stone', grp='base'),
    Bx('S2', 14, 50, 0, 54, 10, 11, 'stone', grp='base'),
    Bx('S2w', 0, 14, 24, 54, 10, 11, 'stone', grp='base'),
    Bx('L2', 14, 50, 6, 54, 11, 22, 'stone', f={'-y': 'wood'}, grp='base'),
    Bx('L2w', 0, 14, 24, 54, 11, 22, 'stone', grp='base'),
    Bx('cheek2', 48.75, 50, 0, 6, 11, 21, 'stone', grp='base'),
    Bx('S3', 14, 50, 0, 6, 21, 22, 'stone', grp='base'),
    Bx('L3', 14, 50, 6, 46, 22, 32, 'wood', grp='crown'),
    Bx('L3w', 0, 14, 24, 46, 22, 32, 'wood', grp='crown'),
    Bx('cheek3', 48.75, 50, 0, 6, 22, 32, 'stone', grp='base'),
    Bx('roof', 14, 50, 0, 50, 33.25, PARAPET, 'bronze', grp='roof'),          # thin floating plate
    Bx('roofGap', 14.5, 49.5, 0.5, 49.5, 32, 33.25, 'bronze', grp='roof'),    # recessed shadow reveal
    Bx('roofw', 0, 14, 24, 50, 33.25, PARAPET, 'bronze', grp='roof'),
    Bx('roofwGap', 0.5, 14.5, 24.5, 49.5, 32, 33.25, 'bronze', grp='roof'),
    Bx('eyebrow2', 0, 50, 54, 57, 21, 22, 'bronze', grp='base'),             # shades the Level 2 suite glass
    Bx('loggiaRoof', 0, 50, 54, 66, 10, 11, 'stone', grp='base'),
    Bx('green', 0.5, 49.5, 60.5, 65.5, 11, 11.7, 'green', cast=False, grp='base'),
    Bx('col1', 0, 0.67, 65.33, 66, 0, 10, 'bronze', grp='base'),
    Bx('col2', 24.67, 25.33, 65.33, 66, 0, 10, 'bronze', grp='base'),
    Bx('col3', 49.33, 50, 65.33, 66, 0, 10, 'bronze', grp='base'),
    Bx('div1', 12.4, 12.6, 54, 57, 11, 21, 'wood', grp='base'),
    Bx('div2', 24.9, 25.1, 54, 57, 11, 21, 'wood', grp='base'),
    Bx('div3', 37.4, 37.6, 54, 57, 11, 21, 'wood', grp='base'),
    Bx('planter3', 31.75, 32.25, 0.5, 5.5, 22, 25.5, 'wood', grp='crown'),
    Bx('shwrE', 49.45, 49.75, 50.3, 54, 22, 29, 'wood', grp='crown'),       # outdoor-shower screens
    Bx('shwrN', 46.3, 49.75, 53.45, 53.75, 22, 29, 'wood', grp='crown'),
]
# Vertical wood fins screening the office storefront.
for _i in range(10):
    _x = 15.35 + _i * 1.15
    BOXES.append(Bx(f'fin{_i}', _x, _x + 0.2, -0.7, 0, 0, 10, 'wood', grp='fins'))
# Thermo-ash sliding screens on the Level 3 terrace edge, drawn parked half-open over each bedroom.
L3_SCREENS = [24.0 + 1.15 * _k for _k in range(7)] + [41.5 + 1.15 * _k for _k in range(7)]
for _i, _x in enumerate(L3_SCREENS):
    BOXES.append(Bx(f'scr{_i}', _x, _x + 0.2, 0.6, 1.3, 22.5, 32, 'wood', grp='crown'))

# Frameless glass guards (o, plane, a, b, z0, z1)
RAILS = [
    ('h', 0.25, 14, 48.75, 11, 14.5),
    ('h', 0.25, 14, 48.75, 22, 25.5),
    ('h', 60, 0, 50, 11, 14.5),
    ('v', 0.25, 54, 60, 11, 14.5),
    ('v', 49.75, 54, 60, 11, 14.5),
    ('h', 53.75, 0, 50, 22, 25.5),
    ('v', 0.25, 46, 54, 22, 25.5),
    ('v', 49.75, 46, 54, 22, 25.5),
]

# ------------------------------------------------------------------ site
LOT_W, LOT_D = 60.0, 145.0
HOUSE_AT = (5.0, 30.0)          # lot coordinates of the house origin (front-left corner)
