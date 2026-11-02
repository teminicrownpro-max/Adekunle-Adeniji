"""Clean rendering of the team's FURNITURE REQUEST DATA PIPELINE frame (source of truth), for slide 4 and the Word notes.
Same structure, boxes and wording as the board; no collaborator tags. usage: python3 pipe_sot.py out.html"""
import sys, html

W, H = 4800, 1580
S = 2400 / W
INK, GREY = "#1a1a1a", "#595959"
PUR = "#6631d7"

DIV, SVG, LAB = [], [], []


def box(x, y, w, h, body="", fill="#ffffff", stroke="#e0e0e0", font=20, color=INK, bold_first=True, align="center", rx=10, dash=False, pad=6):
    st = (f'left:{x*S:.1f}px;top:{y*S:.1f}px;width:{w*S:.1f}px;height:{h*S:.1f}px;background:{fill};'
          f'border:1.1px {"dashed" if dash else "solid"} {stroke};color:{color};font-size:{font*S:.2f}px;'
          f'border-radius:{rx*S:.0f}px;text-align:{align};padding:0 {pad*S:.1f}px;')
    DIV.append(f'<div class="b" style="{st}"><span>{body}</span></div>')


def chip(x, y, w, h, body, fill, color=INK, font=19):
    box(x, y, w, h, f"<b>{body}</b>", fill=fill, stroke=fill, font=font, color=color, rx=22)


def line(pts, color, dash=True, arrow=True, width=1.4):
    d = " ".join(f"{x*S:.1f},{y*S:.1f}" for x, y in pts)
    SVG.append((d, color, dash, arrow, width))


def lab(x, y, w, body, color, font=17):
    LAB.append(f'<div class="lab" style="left:{x*S:.1f}px;top:{y*S:.1f}px;max-width:{w*S:.1f}px;color:{color};font-size:{font*S:.2f}px">{body}</div>')


# ---------- stage title tags ----------
tags = [(120, 620, "Generate", "#e8d9a8", "#5a4500"), (880, 620, "Collect", "#ffd2d2", "#7a1f1f"),
        (1640, 620, "Keep &amp; Shape", "#fbe3c8", "#7a4a00"), (2400, 620, "Store", "#e4e2ee", "#3d3a55"),
        (3160, 560, "Use", "#c9f2d6", "#0b5c2a"), (3860, 880, "Sinks", "#ccd9f0", "#1d3f7a")]
for x, w, name, f, c in tags:
    y = 200 if name != "Sinks" else 130
    chip(x + w / 2 - 110, y, 220, 54, name, f, c, font=24)

# ---------- panels ----------
P = {"G": (120, 620), "C": (880, 620), "K": (1640, 620), "S": (2400, 620), "U": (3160, 560)}
fills = {"G": ("#f6efdd", "#e3d4a8"), "C": ("#ffeded", "#f3bcbc"), "K": ("#fdf1e3", "#f3d4ae"),
         "S": ("#f4f3f8", "#d8d5e6"), "U": ("#eafaf0", "#bfe8cd")}
for k, (x, w) in P.items():
    f, st = fills[k]
    box(x, 270, w, 820, "", fill=f, stroke=st, rx=14)
box(3860, 200, 880, 1040, "", fill="#edf2fa", stroke="#c7d6ee", rx=14)


def inner(px, pw, y, h, title, sub, font=20, fill="#ffffff"):
    box(px + 30, y, pw - 60, h, f"<b>{title}</b><br><i style=\"color:{GREY}\">{sub}</i>", fill=fill, font=font)


gx, gw = P["G"]
items = [("Original requester", "furniture need, location"), ("CMAC", "request details, floor plans, pictures"),
         ("FRC", "intake, assignment decisions"), ("FC", "progress, coordination"), ("Vendor", "quotes, delivery updates")]
for i, (t, s) in enumerate(items):
    inner(gx, gw, 320 + i * 150, 126, t, s)

cx, cw = P["C"]
items = [("Request submission", "form fields, attachments"), ("Case activity", "FRC and FC status changes, messages, ownership, decisions"),
         ("Vendor correspondence", "key clarifications: email, Teams, phone, captured by staff")]
for i, (t, s) in enumerate(items):
    inner(cx, cw, 340 + i * 210, 170, t, s)

kx, kw = P["K"]
items = [("Raw data", "original submission, attachments, messages"), ("Check completeness", "required fields, contacts"),
         ("Organize and link", "associate updates and documents to the request"), ("Prepare reporting", "standardize key fields: status, owner, dates")]
for i, (t, s) in enumerate(items):
    inner(kx, kw, 320 + i * 185, 158, t, s)

sx, sw = P["S"]
box(sx + 80, 330, sw - 160, 140, "<b>PRISM REQUESTS<br>CASE RECORDS</b>", fill="#4a4560", stroke="#4a4560", color="#ffffff", font=21, rx=40)
box(sx + 30, 510, sw - 60, 500,
    "Request and contact data<br>Status history<br>Assignment and ownership<br>Supporting records<br>Completion records<br>Timestamps and audit history",
    font=21, align="left", pad=18)

ux, uw = P["U"]
items = [("Features", "request functions"), ("Evaluation", "outcome measures"), ("Reports", "business decisions")]
for i, (t, s) in enumerate(items):
    inner(ux, uw, 360 + i * 230, 160, t, s)

# ---------- sinks ----------
def sink(cy, chip_fill, chip_txt, chip_sub, boxes, bh=96, gap=18, font=19):
    chip(3900, cy, 300, 120, f"{chip_txt}<br><span style=\"font-weight:400;font-size:{15*S:.2f}px\">{chip_sub}</span>", chip_fill, font=20)
    y = cy - 10
    for b in boxes:
        hh = bh * (2 if len(b) > 55 else 1) if False else bh
        box(4240, y, 460, hh, b, font=font)
        y += hh + gap


sink(260, "#8fdda5", "Product", "day-to-day use for CMACs and Infrastructure staff",
     ["Connected request visibility", "Guided request submission", "Coordinator hand-off support (proposed)"])
sink(640, "#ffc6c6", "Measurement", "digital value opportunities",
     ["Status comprehension, information retrieval and follow-up effort", "First-pass submission completeness", "Manual reporting effort"])
chip(3900, 1020, 300, 120, f"Business<br><span style=\"font-weight:400;font-size:{15*S:.2f}px\">operational reporting</span>", "#ffdc4a", font=20)
box(4240, 980, 460, 220, "<b>Operational reporting for the Infrastructure team</b><br>request volumes, stage and age; completion trends; recorded hand-offs", font=19)

# ---------- main arrows with H chips and control chips ----------
AY = 480
arrows = [("G", "C", "H1", "V"), ("C", "K", "H2", "V&nbsp;&nbsp;F"), ("K", "S", "H3", "F (proposed)"), ("S", "U", "H4", "A")]
for a, b, hcode, ctl in arrows:
    x1 = P[a][0] + P[a][1]; x2 = P[b][0]
    line([(x1, AY), (x2, AY)], "#333333", dash=False)
    chip((x1 + x2) / 2 - 42, AY - 76, 84, 48, hcode, "#efeafc", PUR)
    if ctl:
        wch = 90 if len(ctl) < 8 else 220
        chip((x1 + x2) / 2 - wch / 2, AY + 28, wch, 46, ctl, "#f8d3af", "#5a3200", font=17)
line([(ux + uw, AY), (3860, AY)], "#333333", dash=False)
chip((ux + uw + 3860) / 2 - 42, AY - 76, 84, 48, "H5", "#efeafc", PUR)

# mitigation return: FRC to CMAC
line([(cx + 180, 1090), (cx + 180, 1150), (gx + 420, 1150), (gx + 420, 1090)], "#8c8c8c", dash=True)
chip(cx - 210, 1128, 70, 44, "M", "#f8d3af", "#5a3200", font=17)
lab((gx + 420 + cx + 180) / 2, 1128, 900, "request returned by the FRC to the CMAC for correction", GREY, font=16)

# ---------- finding tags with span lines ----------
line([(1190, 270), (1190, 190), (2710, 190), (2710, 270)], "#305bab")
chip(1870, 166, 170, 48, "L1 &middot; Leak", "#c6dcff", "#143a66", font=17)
line([(1950, 270), (1950, 112), (3440, 112), (3440, 270)], "#b08900")
chip(2560, 88, 230, 48, "V1 &middot; To validate", "#fff6b6", "#5c4a00", font=17)
chip((gx + gw + cx) / 2 - 85, 350, 170, 48, "G1 &middot; Gap", "#ffc6c6", "#6e1414", font=17)
chip((sx + sw + ux) / 2 - 150, 350, 300, 48, "L2 &middot; Potential leak", "#c6dcff", "#143a66", font=17)

# ---------- feedback loops ----------
SB = (4300, 1240)   # sinks panel bottom
loops = [(1210, "#067429", [430, 1190], "Product: new or updated request information (clarifications, reassignments, status changes) returns to Generate and Collect"),
         (1290, "#c23a3a", [1950], "Measurement: evaluation findings (completeness, comprehension, retrieval, reporting effort) return to Keep and Shape as data and product changes"),
         (1370, "#8a6400", [430], "Business: operational insights and decisions (bottlenecks, workload, process changes) return to Generate as requirements"),
         (1450, "#8a6400", [1950], "Business: the same insights return to Keep and Shape as data and process updates")]
for i, (ly, col, targets, text) in enumerate(loops):
    x0 = SB[0] + i * 90
    line([(x0, SB[1]), (x0, ly), (min(targets), ly)], col, arrow=False)
    for t in targets:
        line([(t, ly), (t, 1090)], col)
    lab(2700, ly - 1, 3200, text, col, font=17)

tpl = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:#fff}}
.f{{position:relative;width:{W*S:.0f}px;height:{H*S:.0f}px;font-family:"Noto Sans","DejaVu Sans",Arial,sans-serif;overflow:hidden}}
.b{{position:absolute;box-sizing:border-box;display:flex;align-items:center;justify-content:center;line-height:1.25}}
.lab{{position:absolute;transform:translate(-50%,-50%);background:#fff;padding:0 4px;white-space:nowrap;line-height:1.1}}
</style></head><body><div class="f">
<svg style="position:absolute;left:0;top:0" width="{W*S:.0f}" height="{H*S:.0f}"><defs>MARKERS</defs>LINES</svg>
{''.join(DIV)}{''.join(LAB)}
</div></body></html>"""
cols = sorted({c for _, c, _, _, _ in SVG})
marks = "".join(f'<marker id="m{i}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>' for i, c in enumerate(cols))
lines = "".join('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" %s %s/>' % (d, c, w, 'stroke-dasharray="6,4"' if da else '', 'marker-end="url(#m%d)"' % cols.index(c) if ar else '') for d, c, da, ar, w in SVG)
out = tpl.replace("MARKERS", marks).replace("LINES", lines)
open(sys.argv[1], "w").write(out)
print("ok", W, H, "dashes", out.count("—") + out.count("–"))
