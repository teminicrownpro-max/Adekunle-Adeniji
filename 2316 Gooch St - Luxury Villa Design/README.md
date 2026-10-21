# Villa Gooch — The Lantern House

Schematic design for a contemporary luxury villa at **2316 Gooch Street, Dallas, TX 75241**
(MLS 21372838 — sold 3-story spec house, 3,257 SF, 7 BR / 4.5 BA, 0.2 AC).

The redesign keeps what made the original memorable — the tall glass stair tower with its
cascading chandelier, the glass-railed balconies under stained wood soffits, the front-facing
glass garage door — and turns the all-black stucco box into a calm composition of three
materials: a warm limestone **stone base**, a thermally-modified ash **wood crown**, and a
**bronze lantern** under a thin floating roof plate.

**Open the drawing set:** [`drawings/Villa-Gooch_Schematic-Design-Set.pdf`](drawings/Villa-Gooch_Schematic-Design-Set.pdf)
(ARCH D, 36" x 24", vector). PNG previews of every sheet are in [`drawings/preview/`](drawings/preview/).

## Sheet index

| Sheet | Title | Contents |
|---|---|---|
| A0.0 | Cover | Dusk street rendering, project data, area summary, existing vs. proposed |
| A0.1 | Design narrative & materials | Six design principles, design-move diagrams, program stacking, material palette, systems, dusk garden rendering |
| A1.0 | Architectural site plan | 1/8" site plan, site data, landscape design, street-to-fence site section |
| A2.1 | Level 1 floor plan | Arrival & living; kitchen range wall and living fireplace interior elevations |
| A2.2 | Level 2 floor plan | Family lounge & four bedroom suites; wine bar, suite bath and lounge fireplace elevations |
| A2.3 | Level 3 floor plan | Primary retreat & Bedrooms 6–7; spa bath and primary fireplace elevations |
| A2.4 | Roof plan | Drainage, PV, equipment, lantern skylight; parapet and terrace-edge details |
| A3.1 | Front & rear elevations | 1/4" rendered elevations with keynotes and datums |
| A3.2 | Side elevations | Left and right elevations |
| A4.1 | Building sections | Longitudinal section through the lantern, living room and pool; transverse section through the great room, suites and primary suite |
| A5.1 | Schedules & areas | Door, window, room-finish schedules, area tabulation, preliminary code & zoning checklist |

## Program

- **Level 1 — arrival & living:** pivot door into the triple-height glass lantern (floating lit-tread stair,
  glass bridge, chandelier), office behind a wood-fin screen and reflecting pool, living with linear fireplace,
  dining for 10, chef's kitchen with 12-ft waterfall island, scullery & walk-in pantry, mudroom from the garage,
  wine room under the stair, powder & dry bar, 2-car garage with EV charging, 50 x 12 ft covered loggia with
  outdoor kitchen.
- **Level 2 — family & suites:** family lounge with fireplace and backlit wine wall opening to the covered
  front balcony, kids' study, laundry, linen, Bedrooms 2–5 each with private bath and walk-in closet opening to
  a rear terrace with a sedum green roof beyond.
- **Level 3 — primary retreat:** primary bedroom with fireplace and morning bar, island dressing room, spa
  bath (freestanding tub, rain shower, private WC), 400 SF primary terrace with outdoor shower; Bedrooms 6–7
  with baths and private front terraces; mechanical room with roof hatch.
- **Every level:** 4-stop residential elevator.
- **Garden:** heated salt pool with sun shelf, raised spillover spa, lawn, fire lounge.

## Assumptions to verify before design development

These drawings were developed from the listing photos and the two walkthrough videos. Nothing here
has been measured on site.

- Lot assumed 60' x 145' (0.20 AC); boundary and topographic survey required. True north not confirmed —
  drawings use plan north (street at bottom).
- Zoning assumed R-7.5(A). The design height (34'-6" parapet, 37'-0" lantern) exceeds a 30'-0" limit;
  confirm the actual district or seek relief.
- The listing notes expansive black clay; foundation (post-tensioned slab on drilled piers) to follow a
  geotechnical report.
- Code references are a preliminary IRC 2021 / Dallas amendment review, not a permit review.

## Regenerating the set

All sheets are generated from one building model, so plans, elevations, sections and schedules stay consistent.

```bash
cd src
python3 build_set.py ../build/svg                 # one SVG per sheet
node render.cjs ../build/svg ../drawings/Villa-Gooch_Schematic-Design-Set.pdf ../drawings/preview
```

`model.py` holds the geometry (walls, openings, rooms, massing), `plans.py` the plan / roof / site drawings,
`elev.py` the elevations and sections, `interiors.py` the interior elevations and details, and `build_set.py`
the sheet layouts. Rendering uses Playwright's Chromium.
