# Maplewood Villa

A transitional-contemporary redesign of the Phoenix Homes *Maplewood* (2026 brochure: 2,923 sq ft, 4–7 bedrooms, 2.5 baths, 50 ft lot).

| File | What it is |
| --- | --- |
| `Maplewood-Villa.pdf` | Three 17 × 11 in presentation sheets: street elevation, floor plans, lower level, garden elevation, comparison and areas |
| `index.html` | The same folio as a web page (light and dark, phone-friendly, furniture toggle) |
| `drawings/*.svg` | Each plan and elevation as a standalone, scalable SVG |
| `src/` | The generator: one model in feet, so every drawing stays to scale |

## The scheme in brief

- **Arrival:** a recessed two-storey limestone portal opens into a 20-ft foyer, a 10-ft gallery, then the 20-ft great room. The front door, gallery and the great room's west French door share one axis.
- **Main floor:** kitchen and dining as one 20'-8" room facing a covered loggia; great room with three 20-ft glazed bays and a symmetrical hearth wall; study that doubles as a guest suite; service spine of garage, mudroom, scullery and kitchen.
- **Second floor:** gallery landing and library bridge over both double-height spaces; primary suite behind double doors, with entry gallery, dressing room and spa ensuite; three bedrooms, two baths and an upstairs laundry.
- **Lower level:** media lounge with wet bar, glass-walled gym, guest suite, wine room, games room.
- **Exterior:** honed limestone, white lime stucco, rift oak, black aluminum-clad windows, charcoal standing-seam metal.

| Area | sq ft |
| --- | ---: |
| Main floor | 1,680 |
| Second floor | 1,650 |
| **Total above grade** | **3,330** |
| Finished lower level | 1,375 |

Concept design for discussion, not for construction. Original dimensions are scaled from the brochure plans. Verify zoning, building code and structure before working drawings.

## Rebuild

```sh
cd src
python3 build.py      # drawings/*.svg, index.html, print.html
node render_pdf.js    # Maplewood-Villa.pdf (needs Playwright + Chromium)
```
