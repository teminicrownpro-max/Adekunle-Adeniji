"""Words for the Maplewood Villa folio: shared by the web page and the print PDF."""

STATS = [
    ("3,330", "sq ft above grade"),
    ("+1,375", "sq ft finished lower level"),
    ("4–6", "bedrooms"),
    ("3.5 + 1", "baths"),
    ("42 × 52", "ft footprint, 50 ft lot"),
]

PRINCIPLES = [
    ("One axis", "The front door, the gallery and the great room's west French door sit on one line. "
                 "You see the garden from the doorstep."),
    ("Fewer, larger rooms", "Living, family, breakfast and dining collapse into a 20-ft great room and a "
                            "kitchen that seats ten. Each room keeps its own centreline."),
    ("No angled walls", "The original's 45° walls are gone. Every wall is orthogonal, so furniture, "
                        "millwork and ceilings line up."),
    ("Tall, low, tall", "A 20-ft foyer, a 10-ft gallery, then the 20-ft great room. The lower ceiling "
                        "between them makes both tall rooms feel taller."),
    ("A service spine", "Garage, mudroom, scullery, kitchen. Groceries and boots never cross the formal rooms."),
    ("Honest materials", "Honed limestone, white lime stucco, rift oak, black windows and standing-seam metal. "
                         "Five materials, used the same way on every face."),
]

NOTES = {
    "main": [
        (1, "Portal and foyer", "A two-storey limestone portal replaces the narrow porch. Inside, a 20-ft foyer "
            "steps down to a 10-ft gallery, then opens into the great room."),
        (2, "Great room", "20 ft wide with a 20-ft ceiling. Three glazed bays face the garden; the west French door "
            "sits on the front-door axis. A gallery landing overlooks it from above."),
        (3, "Kitchen and dining", "One 20'-8\" room facing the loggia. A 10-ft island looks at the garden, and the range is "
            "centred under a plaster hood between a fridge column and the scullery door."),
        (4, "Service spine", "Garage to mudroom (lockers, bench) to a walk-in scullery with a second sink and "
            "dishwasher, then the kitchen."),
        (5, "Stair core", "An L-stair with a landing window, open to the gallery. The powder room and the basement "
            "stair sit behind it, off a short back hall."),
        (6, "Hearth wall", "A linear gas fireplace in a limestone surround, flanked by built-ins and two narrow "
            "windows: one symmetrical composition."),
    ],
    "second": [
        (7, "Gallery landing", "The stair arrives at a balcony over the great room. It continues as a library "
            "bridge with built-in shelves, overlooking the foyer."),
        (8, "Primary entry", "Double doors open into an entry gallery and dressing room, so the bedroom is never "
            "seen from the hall."),
        (9, "Primary bedroom", "The bed faces two garden windows. The ensuite has a freestanding tub at the window, "
            "a 5-ft walk-in shower, a separate WC and a double vanity."),
        (10, "Bedrooms 2–4", "Three ~10 × 13 ft bedrooms, each with its own closet. Bedrooms 2 and 3 share a double-vanity "
             "bath; bedroom 4 has the bath beside it. Laundry moves upstairs."),
    ],
    "lower": [
        (11, "Guest suite and gym", "A guest suite with its own bath for parents or visitors, and a gym glazed to "
             "the lounge."),
        (12, "Media lounge", "Under the great room: a 20 × 23 ft lounge with a media wall and wet bar."),
        (13, "Wine room", "Glass-walled, on the way from the stair to the lounge, with the games room beside it."),
    ],
}

COMPARE = [
    ("Arrival", "Small porch tucked beside a projecting garage", "Two-storey limestone portal, 20-ft foyer, view straight to the garden"),
    ("Living rooms", "Living + family (both open to above), separate dining and breakfast", "One 20-ft great room, a kitchen that seats 10, a study"),
    ("Kitchen", "L-shaped, 66\" island, breakfast nook", "10-ft island facing the garden, centred range wall, walk-in scullery"),
    ("Geometry", "45° walls at the stair, primary entry and railing", "All walls orthogonal; every room symmetric on its own axis"),
    ("Mudroom + laundry", "Combined 5'-11\" × 8'-0\" room", "8'-6\" × 6'-0\" mudroom with lockers; laundry upstairs"),
    ("Primary suite", "Entered on a diagonal from the hall", "Double-door entry gallery, dressing room, spa ensuite"),
    ("Baths", "2.5", "3.5 above grade, plus a guest bath below"),
    ("Outdoors", "Patio slider and step", "21 × 12.5 ft covered loggia and a stone terrace"),
    ("Finished lower level", "1,102 sq ft", "≈1,375 sq ft: lounge, bar, gym, guest suite, wine room"),
    ("Area above grade", "2,923 sq ft", "≈3,330 sq ft on a similar 42 × 52 ft footprint"),
]

MATERIALS = [
    ("Honed limestone", "Portal frame, garage base, plinth, loggia columns", "--e-stone"),
    ("White lime stucco", "Main walls; smooth float finish", "--e-stucco"),
    ("Rift white oak", "Pivot door, carriage door, portal lining", "--e-oak"),
    ("Charcoal standing seam", "Roofs and canopies, 16\" pans", "--e-roof"),
    ("Black aluminum-clad", "Windows and doors, slim sightlines", "--e-steel"),
    ("Aged bronze", "Spandrels, lanterns, hardware", "--e-bronze"),
]

AREAS = [
    ("Main floor", "1,680"),
    ("Second floor", "1,650"),
    ("Total above grade", "3,330"),
    ("Finished lower level", "1,375"),
    ("Garage (2 cars)", "456"),
    ("Covered loggia", "267"),
]

CAVEATS = [
    "Original sizes are taken from the Maplewood 2026 brochure plans; its overall footprint scales to about 41'-6\" × 54'-0\".",
    "Areas are measured to exterior faces, with open-to-below space excluded. They will move a little in design development.",
    "The ≈400 sq ft gain comes mostly from the second floor now covering the whole garage. If 2,923 sq ft is a hard "
    "cap, shorten the rear rooms by 4 ft (about 340 sq ft over two floors); the plan keeps working.",
    "This is a concept. Check zoning (setbacks, height, coverage), the building code (stairs, guards, egress, garage "
    "fire separation) and structure (the ~18-ft beam between kitchen and great room) before working drawings.",
]

CAVEATS_SHORT = [
    "Original sizes scaled from the 2026 brochure. Areas to exterior faces, open-to-below excluded.",
    "The ≈400 sq ft gain is mostly the second floor over the garage; shorten the rear rooms 4 ft to return to 2,923.",
    "Concept only: verify zoning, building code and structure before working drawings.",
]
