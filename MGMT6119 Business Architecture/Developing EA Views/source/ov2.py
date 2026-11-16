"""Generate the DoDAF OV-2 Operational Resource Flow Description as SVG."""
import sys

W, H = 1040, 1530
FONT = "Inter, 'Liberation Sans', Arial, sans-serif"

INK = "#1b2a3a"
QUIET = "#5b6b7c"
INFO = "#2f5d8a"      # information needline
PHYS = "#c2571a"      # needline also carrying personnel / materiel
INT_FILL = "#e8f1fa"
INT_STROKE = "#2f5d8a"
HUB_FILL = "#d3e6f7"
EXT_FILL = "#f6f6f4"
EXT_STROKE = "#8a949e"

out = []
def a(s):
    out.append(s)

def text(x, y, s, size=16, weight=400, fill=INK, anchor="start", style="", spacing=None):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    st = f' font-style="{style}"' if style else ""
    a(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}{st}>{s}</text>')

def box(x, y, w, h, opid, scope, names, loc, kind="int", role=None):
    if kind == "ext":
        fill, stroke, dash, sw = EXT_FILL, EXT_STROKE, ' stroke-dasharray="7 5"', 1.6
    elif kind == "hub":
        fill, stroke, dash, sw = HUB_FILL, INT_STROKE, "", 2.6
    else:
        fill, stroke, dash, sw = INT_FILL, INT_STROKE, "", 1.8
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')
    cx = x + w / 2
    tag_col = INT_STROKE if kind != "ext" else QUIET
    text(cx, y + 24, f"{opid} · {scope}", 13.5, 700, tag_col, "middle", spacing="0.6")
    yy = y + 50
    for n in names:
        text(cx, yy, n, 18, 700, INK, "middle")
        yy += 22
    if role:
        text(cx, yy + 1, role, 15, 500, INK, "middle")
        yy += 22
    text(cx, yy + 4, loc, 14, 400, QUIET, "middle", style="italic")

def line(points, color, start=False, end=True, width=2.2, dash=None):
    d = "M" + " L".join(f"{px} {py}" for px, py in points)
    mk = "phys" if color == PHYS else "info"
    ms = f' marker-start="url(#{mk}-a)"' if start else ""
    me = f' marker-end="url(#{mk}-a)"' if end else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"{ms}{me}{da}/>')

def pill(x, y, label, color):
    w = 14 + 9.2 * len(label)
    a(f'<rect x="{x - w/2}" y="{y - 12}" width="{w}" height="24" rx="12" fill="#ffffff" stroke="{color}" stroke-width="1.6"/>')
    text(x, y + 5, label, 13.5, 700, color, "middle")

a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
a('<defs>'
  f'<marker id="info-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M0 0L10 5L0 10z" fill="{INFO}"/></marker>'
  f'<marker id="phys-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M0 0L10 5L0 10z" fill="{PHYS}"/></marker>'
  '</defs>')
# markerUnits userSpaceOnUse => size in px; enlarge
out[-1] = out[-1].replace('markerWidth="7" markerHeight="7"', 'markerWidth="13" markerHeight="13"').replace('markerWidth="8" markerHeight="8"', 'markerWidth="14" markerHeight="14"')
a(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')

# ---- title block
text(40, 46, "OV-2 Operational Resource Flow Description", 28, 700)
text(40, 76, "Maritime Search and Rescue (SAR) Coordination · As-Is · notional · DoDAF 2.02 Operational Viewpoint", 15, 400, QUIET)
a(f'<line x1="40" y1="92" x2="{W-40}" y2="92" stroke="#d5dbe1" stroke-width="1"/>')

# ---- architecture boundary
BX0, BY0, BX1, BY1 = 40, 250, 1000, 700
a(f'<rect x="{BX0}" y="{BY0}" width="{BX1-BX0}" height="{BY1-BY0}" rx="14" fill="none" stroke="{INT_STROKE}" stroke-width="1.6" stroke-dasharray="10 7"/>')
a(f'<rect x="{BX0}" y="{BY0}" width="250" height="28" rx="0" fill="{INT_STROKE}"/>')
text(BX0 + 12, BY0 + 19, "IN SCOPE: SAR COORDINATION", 13, 700, "#ffffff", spacing="0.8")

# ---- needlines (drawn before boxes so boxes sit on top of line ends)
# NL1 OP-1 -> OP-2 (external to external)
line([(360, 1065), (24, 1065), (24, 165), (60, 165)], INFO)
# NL2 OP-2 -> OP-3
line([(310, 220), (310, 345), (360, 345)], INFO)
# NL6 OP-8 -> OP-3
line([(730, 220), (730, 345), (680, 345)], INFO)
# NL4 OP-3 <-> OP-4
line([(360, 400), (230, 400), (230, 500)], INFO, start=True)
# NL7 OP-3 <-> OP-5
line([(680, 400), (810, 400), (810, 500)], INFO, start=True)
# NL8 OP-3 <-> OP-6
line([(520, 430), (520, 500)], INFO, start=True)
# NL9 OP-6 <-> OP-5
line([(645, 560), (720, 560)], INFO, start=True)
# NL3 OP-1 <-> OP-4
line([(360, 1020), (110, 1020), (110, 620)], INFO, start=True)
# NL5 OP-4 <-> OP-7
line([(260, 620), (260, 800)], INFO, start=True)
# NL10 OP-6 <-> OP-7
line([(420, 620), (420, 800)], INFO, start=True)
# NL12 OP-6 <-> OP-1 (personnel)
line([(505, 620), (505, 980)], PHYS, start=True, width=3.2)
# NL13 OP-6 -> OP-9 (personnel)
line([(600, 620), (600, 800)], PHYS, width=3.2)
# NL14 OP-5 -> OP-9 (personnel)
line([(760, 620), (760, 800)], PHYS, width=3.2)
# NL11 OP-5 <-> OP-1 (materiel + personnel)
line([(920, 620), (920, 1020), (680, 1020)], PHYS, start=True, width=3.2)

# ---- performers
box(60, 110, 280, 110, "OP-2", "EXTERNAL", ["Satellite distress-", "alerting service (MCC)"], "Space and ground segment", "ext")
box(700, 110, 280, 110, "OP-8", "EXTERNAL", ["Met and ocean", "service"], "Ashore", "ext")
box(360, 290, 320, 140, "OP-3", "IN SCOPE", ["Joint Rescue Coordination", "Centre (JRCC)"], "Ashore · coordination hub", "hub", role="SAR Mission Coordinator")
box(70, 500, 260, 120, "OP-4", "IN SCOPE", ["Maritime communications", "centre (MCTS)"], "Ashore, coastal", "int")
box(385, 500, 260, 120, "OP-6", "IN SCOPE", ["SAR surface unit", "On-Scene Coordinator"], "At sea", "int")
box(720, 500, 260, 120, "OP-5", "IN SCOPE", ["SAR air unit", "aircraft and helicopter"], "Airborne", "int")
box(190, 800, 260, 110, "OP-7", "EXTERNAL", ["Vessels of", "opportunity"], "At sea", "ext")
box(560, 800, 260, 110, "OP-9", "EXTERNAL", ["EMS and receiving", "hospital"], "Ashore", "ext")
box(360, 980, 320, 110, "OP-1", "EXTERNAL", ["Vessel and persons", "in distress"], "At sea", "ext")

# ---- needline labels
pill(240, 1065, "NL1", INFO)
pill(310, 300, "NL2", INFO)
pill(730, 300, "NL6", INFO)
pill(230, 455, "NL4", INFO)
pill(810, 455, "NL7", INFO)
pill(520, 465, "NL8", INFO)
pill(682, 560, "NL9", INFO)
pill(110, 750, "NL3", INFO)
pill(260, 750, "NL5", INFO)
pill(420, 750, "NL10", INFO)
pill(505, 945, "NL12", PHYS)
pill(600, 750, "NL13", PHYS)
pill(760, 750, "NL14", PHYS)
pill(920, 750, "NL11", PHYS)

# ---- legend
LY = 1130
a(f'<line x1="40" y1="{LY}" x2="{W-40}" y2="{LY}" stroke="#d5dbe1" stroke-width="1"/>')
text(40, LY + 30, "LEGEND", 14, 700, QUIET, spacing="1")
# row 1: performer kinds
a(f'<rect x="40" y="{LY+46}" width="44" height="26" rx="6" fill="{INT_FILL}" stroke="{INT_STROKE}" stroke-width="1.8"/>')
text(94, LY + 65, "Operational performer, in scope", 15)
a(f'<rect x="370" y="{LY+46}" width="44" height="26" rx="6" fill="{EXT_FILL}" stroke="{EXT_STROKE}" stroke-width="1.6" stroke-dasharray="7 5"/>')
text(424, LY + 65, "External operational performer", 15)
a(f'<rect x="700" y="{LY+46}" width="44" height="26" rx="6" fill="none" stroke="{INT_STROKE}" stroke-width="1.6" stroke-dasharray="10 7"/>')
text(754, LY + 65, "Architecture boundary", 15)
# row 2: needline kinds
a(f'<path d="M40 {LY+100} L84 {LY+100}" stroke="{INFO}" stroke-width="2.2" marker-end="url(#info-a)"/>')
text(94, LY + 105, "Needline: information flows", 15)
a(f'<path d="M370 {LY+100} L414 {LY+100}" stroke="{PHYS}" stroke-width="3.2" marker-end="url(#phys-a)"/>')
text(424, LY + 105, "Needline: also personnel or materiel", 15)
text(700, LY + 105, "Arrowhead = direction of resource flow", 15)

# ---- needline key (two columns)
KY = LY + 150
text(40, KY, "NEEDLINES AND RESOURCE FLOWS   (I = information, M = materiel, P = personnel)", 14, 700, QUIET, spacing="1")
left = [
    ("NL1", "Beacon alert (I)"),
    ("NL2", "Distress alert message (I)"),
    ("NL3", "Mayday call / acknowledgement (I)"),
    ("NL4", "Distress relay / broadcast request (I)"),
    ("NL5", "Mayday Relay / vessel replies (I)"),
    ("NL6", "Wind, sea-state and drift data (I)"),
    ("NL7", "Tasking, search plan / SITREPs (I)"),
]
right = [
    ("NL8", "Tasking, OSC designation / SITREPs (I)"),
    ("NL9", "Search assignments / sightings (I)"),
    ("NL10", "On-scene direction / search results (I)"),
    ("NL11", "Survival kit (M), signals (I), hoisted survivors (P)"),
    ("NL12", "Rescue instructions (I), survivors recovered (P)"),
    ("NL13", "Survivors landed (P), casualty report (I)"),
    ("NL14", "Medevac survivors (P), casualty report and ETA (I)"),
]
for col, items in ((40, left), (520, right)):
    y = KY + 32
    for nl, desc in items:
        c = PHYS if nl in ("NL11", "NL12", "NL13", "NL14") else INFO
        text(col, y, nl, 15, 700, c)
        text(col + 54, y, desc, 15)
        y += 27
a(f'<text x="{W-40}" y="{H-16}" font-size="12.5" fill="{QUIET}" text-anchor="end">Author: Adekunle Adeniji (1378471) · MGMT6119 · 16 Nov 2026</text>')
a('</svg>')

open(sys.argv[1], "w").write("\n".join(out))
