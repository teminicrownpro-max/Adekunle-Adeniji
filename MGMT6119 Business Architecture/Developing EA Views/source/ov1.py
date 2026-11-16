"""Generate the DoDAF OV-1 High-Level Operational Concept Graphic as SVG."""
import sys

W, H = 1100, 1270
FONT = "Inter, 'Liberation Sans', Arial, sans-serif"
INK = "#1b2a3a"
QUIET = "#5b6b7c"
ALERT = "#c62828"     # distress alert / signal
INFO = "#1f4f80"      # coordination information
PHYS = "#d4691a"      # movement of personnel / materiel
HUB = "#1f4f80"

o = []
def a(s): o.append(s)

def text(x, y, s, size=15, weight=400, fill=INK, anchor="middle", style="", spacing=None, halo=False):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    st = f' font-style="{style}"' if style else ""
    h = ' stroke="#ffffff" stroke-width="5" stroke-linejoin="round" paint-order="stroke"' if halo else ""
    a(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}{st}{h}>{s}</text>')

def label(x, y, lines, size=14.5, weight=600, anchor="middle", fill=INK):
    """Label on a white rounded plate."""
    lh = size + 4
    wmax = max(len(t) for t in lines) * size * 0.56 + 16
    hh = lh * len(lines) + 8
    if anchor == "middle":
        x0 = x - wmax / 2
    elif anchor == "start":
        x0 = x - 8
    else:
        x0 = x - wmax + 8
    a(f'<rect x="{x0:.1f}" y="{y - size - 2:.1f}" width="{wmax:.1f}" height="{hh:.1f}" rx="6" fill="#ffffff" fill-opacity="0.92" stroke="#c9d3dc" stroke-width="0.8"/>')
    for i, t in enumerate(lines):
        text(x, y + i * lh + 2, t, size, weight if i == 0 else 400, fill, anchor)

def badge(x, y, n, color):
    a(f'<circle cx="{x}" cy="{y}" r="13" fill="{color}" stroke="#ffffff" stroke-width="2.5"/>')
    text(x, y + 5, str(n), 14, 800, "#ffffff")

def path(d, color, width=2.6, dash=None, start=False, end=True):
    mk = {ALERT: "al", INFO: "in", PHYS: "ph"}[color]
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    ms = f' marker-start="url(#{mk})"' if start else ""
    me = f' marker-end="url(#{mk})"' if end else ""
    a(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="{width + 4}" stroke-linecap="round" opacity="0.85"/>')
    a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{ds}{ms}{me}/>')

# ---------------------------------------------------------------- icons
def satellite(x, y):
    a(f'<g transform="translate({x},{y}) rotate(-18)">'
      '<rect x="-62" y="-11" width="44" height="22" fill="#2b5c8a" stroke="#183552" stroke-width="1.5"/>'
      '<path d="M-51 -11V11M-40 -11V11M-29 -11V11M-62 0H-18" stroke="#9cc3e6" stroke-width="1"/>'
      '<rect x="18" y="-11" width="44" height="22" fill="#2b5c8a" stroke="#183552" stroke-width="1.5"/>'
      '<path d="M29 -11V11M40 -11V11M51 -11V11M18 0H62" stroke="#9cc3e6" stroke-width="1"/>'
      '<path d="M-18 0H-12M12 0H18" stroke="#183552" stroke-width="3"/>'
      '<rect x="-12" y="-15" width="24" height="30" rx="3" fill="#d9a441" stroke="#7a5a17" stroke-width="1.5"/>'
      '<path d="M0 15V24" stroke="#555" stroke-width="2"/><path d="M-8 30 Q0 20 8 30" fill="none" stroke="#555" stroke-width="2"/>'
      '</g>')

def dish(x, y):
    a(f'<g transform="translate({x},{y})">'
      '<path d="M-4 22 L4 22 L2 4 L-2 4Z" fill="#6b7785"/>'
      '<path d="M-22 -8 Q0 22 22 -8 Z" fill="#eef2f5" stroke="#55606b" stroke-width="1.8" transform="rotate(35)"/>'
      '<path d="M0 0 L14 -16" stroke="#55606b" stroke-width="1.6"/><circle cx="14" cy="-16" r="2.5" fill="#55606b"/>'
      '<rect x="-30" y="22" width="60" height="4" fill="#8a8f80"/>'
      '</g>')

def building(x, y, w, h, fill="#f1f3f5", stroke="#5c6670", rows=2, cols=3, roof=None):
    a(f'<rect x="{x - w/2}" y="{y - h}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
    if roof:
        a(f'<rect x="{x - w/2 - 3}" y="{y - h - 6}" width="{w + 6}" height="7" fill="{roof}"/>')
    ww, gh = w / (cols * 2 + 1), h / (rows * 2 + 1)
    for r in range(rows):
        for c in range(cols):
            a(f'<rect x="{x - w/2 + ww*(2*c+1):.1f}" y="{y - h + gh*(2*r+1):.1f}" width="{ww:.1f}" height="{gh:.1f}" fill="#9fc0dd"/>')

def jrcc(x, y):
    a(f'<rect x="{x-86}" y="{y-74}" width="172" height="90" rx="10" fill="#dcebf8" stroke="{HUB}" stroke-width="2.5"/>')
    building(x - 20, y + 4, 92, 58, fill="#ffffff", stroke="#3d4a57", rows=2, cols=4, roof="#3d4a57")
    a(f'<path d="M{x+44} {y+4} V{y-58}" stroke="#3d4a57" stroke-width="2"/>')
    a(f'<path d="M{x+44} {y-58} L{x+64} {y-52} L{x+44} {y-46}Z" fill="{ALERT}"/>')
    for r in (8, 15):
        a(f'<path d="M{x+44 - r} {y-62 - r*0.2} A{r} {r} 0 0 1 {x+44 + r} {y-62 - r*0.2}" fill="none" stroke="{HUB}" stroke-width="1.5"/>')

def met(x, y):
    building(x, y, 54, 40, rows=1, cols=2, roof="#5c6670")
    a(f'<g transform="translate({x+6},{y-62})"><path d="M-22 10 a10 10 0 0 1 6 -16 a13 13 0 0 1 24 -2 a10 10 0 0 1 14 18 z" fill="#ffffff" stroke="#6d7c8b" stroke-width="1.6"/>'
      f'<path d="M-12 16 l-4 8 M-2 16 l-4 8 M8 16 l-4 8" stroke="#3f88c5" stroke-width="2"/></g>')

def tower(x, y):
    a(f'<g transform="translate({x},{y})">'
      '<path d="M-16 0 L0 -86 L16 0 M-12 -20 L12 -20 M-8 -40 L8 -40 M-5 -60 L5 -60 M-12 -20 L8 -40 M12 -20 L-8 -40 M-8 -40 L5 -60 M8 -40 L-5 -60" fill="none" stroke="#3d4a57" stroke-width="2"/>'
      '<circle cx="0" cy="-88" r="3.5" fill="#c62828"/>'
      '<path d="M-14 -96 A16 16 0 0 1 -14 -80 M14 -96 A16 16 0 0 0 14 -80 M-22 -102 A26 26 0 0 1 -22 -74 M22 -102 A26 26 0 0 0 22 -74" fill="none" stroke="#1f4f80" stroke-width="1.6" transform="translate(0,0)"/>'
      '<rect x="18" y="-22" width="30" height="22" fill="#f1f3f5" stroke="#5c6670" stroke-width="1.5"/>'
      '</g>')

def hospital(x, y):
    building(x, y, 92, 50, rows=2, cols=4, roof="#5c6670")
    a(f'<rect x="{x-14}" y="{y-86}" width="28" height="28" rx="4" fill="#ffffff" stroke="#c62828" stroke-width="1.5"/>')
    a(f'<path d="M{x} {y-81}V{y-63}M{x-9} {y-72}H{x+9}" stroke="#c62828" stroke-width="5"/>')
    a(f'<path d="M{x+46} {y} h40 v-22 h-14 l-6 -10 h-20 z" fill="#ffffff" stroke="#5c6670" stroke-width="1.4"/>')
    a(f'<path d="M{x+64} {y-15} h10 M{x+69} {y-20} v10" stroke="#c62828" stroke-width="2.5"/>')
    a(f'<circle cx="{x+56}" cy="{y+1}" r="4" fill="#3d4a57"/><circle cx="{x+78}" cy="{y+1}" r="4" fill="#3d4a57"/>')

def aircraft(x, y):
    a(f'<g transform="translate({x},{y})">'
      '<path d="M-58 2 Q-60 -6 -48 -7 L44 -7 Q60 -6 64 0 Q60 6 44 7 L-48 7 Q-60 8 -58 2Z" fill="#f4f6f8" stroke="#3d4a57" stroke-width="1.6"/>'
      '<path d="M-6 -6 L-22 -42 L-8 -42 L18 -6Z" fill="#dfe5ea" stroke="#3d4a57" stroke-width="1.6"/>'
      '<path d="M-6 6 L-16 26 L-4 26 L14 6Z" fill="#dfe5ea" stroke="#3d4a57" stroke-width="1.6"/>'
      '<path d="M-48 -7 L-58 -30 L-48 -30 L-34 -7Z" fill="#c62828" stroke="#3d4a57" stroke-width="1.4"/>'
      '<path d="M48 -3 h8" stroke="#3d4a57" stroke-width="3"/>'
      '<rect x="-30" y="-4" width="56" height="3" fill="#c62828"/>'
      '<path d="M-14 -24 l-3 0 M-4 -24 l-3 0" stroke="#3d4a57" stroke-width="5"/>'
      '</g>')

def helicopter(x, y):
    a(f'<g transform="translate({x},{y})">'
      '<path d="M-60 -34 H60" stroke="#3d4a57" stroke-width="3"/><path d="M0 -34 V-24" stroke="#3d4a57" stroke-width="3"/>'
      '<path d="M-34 -8 Q-34 -26 -6 -26 L22 -26 Q40 -26 40 -8 Q40 8 22 8 L-20 8 Q-34 8 -34 -8Z" fill="#f2c12e" stroke="#3d4a57" stroke-width="1.6"/>'
      '<path d="M-34 -12 L-80 -16 L-80 -8 L-34 -2Z" fill="#f2c12e" stroke="#3d4a57" stroke-width="1.6"/>'
      '<path d="M-84 -30 V4" stroke="#3d4a57" stroke-width="3"/>'
      '<path d="M18 -22 Q34 -22 36 -10 L18 -10Z" fill="#9fc0dd"/>'
      '<rect x="-24" y="-12" width="22" height="3" fill="#c62828"/>'
      '<path d="M-22 8 V16 M22 8 V16 M-30 16 H30" stroke="#3d4a57" stroke-width="2.2"/>'
      '</g>')

def ship_cutter(x, y):
    a(f'<g transform="translate({x},{y})">'
      '<path d="M-78 -10 L78 -10 L64 14 L-70 14 Z" fill="#ffffff" stroke="#2d3740" stroke-width="1.8"/>'
      '<path d="M-74 -2 L76 -2 L72 4 L-71 4Z" fill="#c62828"/>'
      '<path d="M18 -10 L52 -10" stroke="#c62828" stroke-width="0"/>'
      '<rect x="-34" y="-34" width="56" height="24" fill="#ffffff" stroke="#2d3740" stroke-width="1.6"/>'
      '<rect x="-24" y="-48" width="34" height="14" fill="#ffffff" stroke="#2d3740" stroke-width="1.6"/>'
      '<path d="M-28 -28 h44" stroke="#9fc0dd" stroke-width="4"/>'
      '<path d="M-6 -48 V-72 M-16 -62 H4" stroke="#2d3740" stroke-width="2"/>'
      '<rect x="30" y="-22" width="22" height="12" fill="#e65c00" stroke="#2d3740" stroke-width="1.2"/>'
      '</g>')

def ship_voo(x, y):
    a(f'<g transform="translate({x},{y})">'
      '<path d="M-74 -8 L80 -8 L66 14 L-68 14 Z" fill="#37474f" stroke="#1f2a30" stroke-width="1.6"/>'
      '<rect x="-60" y="-24" width="20" height="16" fill="#c0392b"/><rect x="-38" y="-24" width="20" height="16" fill="#2e86c1"/>'
      '<rect x="-16" y="-24" width="20" height="16" fill="#27ae60"/><rect x="6" y="-24" width="20" height="16" fill="#d4ac0d"/>'
      '<rect x="-49" y="-38" width="20" height="14" fill="#2e86c1"/><rect x="-27" y="-38" width="20" height="14" fill="#c0392b"/>'
      '<rect x="40" y="-40" width="24" height="32" fill="#f1f3f5" stroke="#1f2a30" stroke-width="1.4"/>'
      '<path d="M44 -32 h16" stroke="#9fc0dd" stroke-width="4"/><path d="M58 -40 V-52" stroke="#1f2a30" stroke-width="2"/>'
      '</g>')

def fishing_vessel(x, y):
    a(f'<g transform="translate({x},{y}) rotate(-9)">'
      '<path d="M-56 -6 L52 -6 L40 16 L-48 16 Z" fill="#2e7d6b" stroke="#1d3b33" stroke-width="1.6"/>'
      '<rect x="12" y="-30" width="30" height="24" fill="#ffffff" stroke="#1d3b33" stroke-width="1.5"/>'
      '<path d="M-30 -6 V-46 M-30 -46 L4 -6" stroke="#1d3b33" stroke-width="2"/>'
      '</g>')
    # fire and smoke
    a(f'<path d="M{x+8} {y-26} q-6 -14 4 -26 q2 10 8 6 q4 -10 -2 -20 q16 8 14 28 q-2 10 -12 14 z" fill="#f39c12" stroke="#d35400" stroke-width="1.2"/>')
    a(f'<path d="M{x+14} {y-34} q-2 -8 3 -12 q3 6 4 10 z" fill="#f9e79f"/>')
    a(f'<path d="M{x+12} {y-66} q-14 -10 -4 -24 q10 -12 26 -6 q14 -10 22 6 q10 10 -2 20 q-18 12 -42 4z" fill="#7f8c8d" opacity="0.75"/>')

def raft(x, y):
    a(f'<g transform="translate({x},{y})">'
      '<ellipse cx="0" cy="6" rx="38" ry="11" fill="#ff7a00" stroke="#9c4a00" stroke-width="1.6"/>'
      '<path d="M-28 4 Q0 -30 28 4 Z" fill="#ff9a33" stroke="#9c4a00" stroke-width="1.6"/>'
      '<circle cx="-9" cy="-2" r="5" fill="#f1c27d" stroke="#6b4a2b"/><circle cx="7" cy="-3" r="5" fill="#f1c27d" stroke="#6b4a2b"/>'
      '<rect x="24" y="-10" width="7" height="14" rx="2" fill="#f2c12e" stroke="#3d4a57"/><path d="M27.5 -10 V-18" stroke="#3d4a57" stroke-width="1.5"/>'
      '</g>')

def waves(x, y, n=3, color="#ffffff"):
    for i in range(n):
        a(f'<path d="M{x + i*26} {y} q6.5 -6 13 0 t13 0" fill="none" stroke="{color}" stroke-width="1.4" opacity="0.7"/>')

# ---------------------------------------------------------------- canvas
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
a('<defs>'
  '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe2f3"/><stop offset="1" stop-color="#f3f8fc"/></linearGradient>'
  '<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ec0e4"/><stop offset="1" stop-color="#5d9bc9"/></linearGradient>'
  '<linearGradient id="land" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3edd3"/><stop offset="1" stop-color="#d2e1bd"/></linearGradient>'
  '<clipPath id="scene"><rect x="30" y="170" width="1040" height="660" rx="14"/></clipPath>'
  f'<marker id="al" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{ALERT}"/></marker>'
  f'<marker id="in" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{INFO}"/></marker>'
  f'<marker id="ph" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="15" markerHeight="15" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{PHYS}"/></marker>'
  '</defs>')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

# title block
text(40, 46, "OV-1 High-Level Operational Concept Graphic", 28, 700, anchor="start")
text(40, 76, "Maritime Search and Rescue (SAR) Coordination · As-Is · notional · DoDAF 2.02 Operational Viewpoint", 15, 400, QUIET, anchor="start")
a(f'<rect x="30" y="98" width="1040" height="56" rx="10" fill="#1f4f80"/>')
text(50, 132, "MISSION", 13, 800, "#a9c7e6", anchor="start", spacing="1.2")
text(130, 132, "Detect, locate and rescue persons in distress at sea, and deliver survivors to medical care ashore.", 16.5, 600, "#ffffff", anchor="start")

# scene background
a('<g clip-path="url(#scene)">')
a('<rect x="30" y="170" width="1040" height="660" fill="url(#sky)"/>')
a('<rect x="30" y="480" width="1040" height="350" fill="url(#sea)"/>')
a('<path d="M30 330 L240 330 C 320 336, 370 380, 380 450 C 388 520, 398 600, 396 690 C 394 750, 404 800, 412 830 L30 830 Z" fill="url(#land)" stroke="#b9c9a0" stroke-width="1.5"/>')
for wx, wy in [(470, 520), (760, 540), (980, 520), (520, 800), (900, 810), (650, 760), (1000, 760), (450, 640)]:
    waves(wx, wy)
# search area
a('<ellipse cx="850" cy="700" rx="200" ry="104" fill="#ffffff" fill-opacity="0.12" stroke="#ffffff" stroke-width="2" stroke-dasharray="9 7"/>')
a('</g>')
a('<rect x="30" y="170" width="1040" height="660" rx="14" fill="none" stroke="#b8c4cf" stroke-width="1.2"/>')
# zone labels
text(48, 196, "SPACE / AIR", 12.5, 800, "#6d89a5", anchor="start", spacing="1.5")
text(48, 352, "SHORE", 12.5, 800, "#7d9363", anchor="start", spacing="1.5")
text(1052, 506, "SEA", 12.5, 800, "#ffffff", anchor="end", spacing="1.5")
text(850, 822, "Search area around the distress datum", 12.5, 600, "#ffffff", spacing="0.3")

# ---------------------------------------------------------------- flows (under icons)
# 1 beacon uplink and Mayday
path("M985 598 L992 262", ALERT, dash="9 6")
path("M930 586 Q690 400 366 545", ALERT, dash="9 6")
# 2 downlink and MCC -> JRCC
path("M950 236 L258 382", ALERT, dash="9 6")
path("M290 446 L236 506", INFO)
# 3 MCTS <-> JRCC
path("M322 578 L258 578", INFO, start=True)
# 4 Met -> JRCC
path("M67 446 L108 506", INFO)
# 5 JRCC -> aircraft, JRCC -> cutter (two-way: SITREPs back)
path("M258 522 L520 402", INFO, start=True)
path("M258 590 L452 690", INFO, start=True)
# 6 MCTS -> vessels of opportunity
path("M372 590 L566 612", INFO)
# 7 OSC <-> helicopter, OSC <-> VOO
path("M590 690 L772 642", INFO, dash="3 5", start=True)
path("M556 672 L604 642", INFO, dash="3 5", start=True)
# 8 hoist, cutter recovers
path("M835 664 L835 730", PHYS, dash="7 5", start=True)
path("M600 716 L792 746", PHYS, dash="7 5")
# 9 cutter -> hospital
path("M460 726 Q330 780 210 778", PHYS)

# ---------------------------------------------------------------- icons
satellite(990, 228)
dish(245, 400); building(292, 440, 40, 30, rows=1, cols=2, roof="#5c6670")
met(67, 440)
jrcc(170, 580)
tower(340, 610)
hospital(120, 790)
aircraft(560, 392)
helicopter(835, 640)
ship_cutter(530, 700)
ship_voo(650, 625)
raft(835, 752)
fishing_vessel(960, 640)

# ---------------------------------------------------------------- labels
label(870, 292, ["Distress-alerting", "satellites"], 13.5)
label(376, 410, ["Ground station", "and MCC"], 13.5)
label(155, 418, ["Met and ocean", "service"], 13.5)
label(170, 636, ["JRCC", "SAR Mission Coordinator"], 14.5)
label(298, 548, ["MCTS"], 13.5)
label(120, 818, ["EMS and hospital"], 13.5)
label(600, 446, ["SAR fixed-wing aircraft"], 13.5)
label(835, 586, ["SAR helicopter"], 13.5)
label(530, 760, ["Coast Guard cutter", "On-Scene Coordinator"], 13.5)
label(660, 589, ["Vessel of opportunity"], 13.5)
label(968, 702, ["Fishing vessel", "in distress"], 13.5)
label(835, 790, ["Survivors in life raft"], 13.5)

# ---------------------------------------------------------------- badges
badge(988, 440, 1, ALERT)
badge(724, 490, 1, ALERT)
badge(600, 296, 2, ALERT)
badge(263, 476, 2, INFO)
badge(290, 578, 3, INFO)
badge(87, 476, 4, INFO)
badge(470, 425, 5, INFO)
badge(352, 640, 5, INFO)
badge(476, 603, 6, INFO)
badge(668, 670, 7, INFO)
badge(694, 731, 8, PHYS)
badge(330, 762, 9, PHYS)

# ---------------------------------------------------------------- legend + key
LY = 860
text(40, LY + 16, "LEGEND", 13.5, 800, QUIET, anchor="start", spacing="1.2")
def leg_line(x, y, color, dash, txt, width=2.6):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    mk = {ALERT: "al", INFO: "in", PHYS: "ph"}[color]
    a(f'<path d="M{x} {y} H{x+46}" stroke="{color}" stroke-width="{width}"{ds} marker-end="url(#{mk})"/>')
    text(x + 58, y + 5, txt, 14.5, 400, INK, anchor="start")
leg_line(40, LY + 44, ALERT, "9 6", "Distress alert or signal")
leg_line(300, LY + 44, INFO, None, "Coordination information")
leg_line(580, LY + 44, INFO, "3 5", "On-scene coordination")
leg_line(830, LY + 44, PHYS, "7 5", "Rescue of survivors")
a(f'<path d="M40 {LY+76} H86" stroke="{PHYS}" stroke-width="2.6" marker-end="url(#ph)"/>')
text(98, LY + 81, "Movement of survivors (personnel)", 14.5, 400, INK, anchor="start")
a(f'<rect x="372" y="{LY+64}" width="44" height="26" rx="6" fill="#dcebf8" stroke="{HUB}" stroke-width="2.5"/>')
text(428, LY + 81, "Coordination hub (in scope)", 14.5, 400, INK, anchor="start")
a(f'<ellipse cx="680" cy="{LY+77}" rx="24" ry="12" fill="#8ec0e4" stroke="#ffffff" stroke-width="0"/>')
a(f'<ellipse cx="680" cy="{LY+77}" rx="24" ry="12" fill="none" stroke="#3f6f99" stroke-width="1.6" stroke-dasharray="5 4"/>')
text(714, LY + 81, "Search area", 14.5, 400, INK, anchor="start")
a(f'<circle cx="870" cy="{LY+77}" r="12" fill="{INFO}"/>')
text(870, LY + 82, "n", 13, 800, "#ffffff")
text(892, LY + 81, "Interaction number", 14.5, 400, INK, anchor="start")

KY = LY + 118
a(f'<line x1="40" y1="{KY - 14}" x2="{W-40}" y2="{KY - 14}" stroke="#d5dbe1" stroke-width="1"/>')
text(40, KY + 10, "OPERATIONAL CONCEPT: NUMBERED INTERACTIONS", 13.5, 800, QUIET, anchor="start", spacing="1.2")
key = [
    (1, ALERT, "Fishing vessel in distress raises the alert: 406 MHz beacon to satellites, Mayday call to MCTS"),
    (2, ALERT, "Satellites locate the beacon; the ground station and Mission Control Centre (MCC) alert the JRCC"),
    (3, INFO, "MCTS acknowledges the Mayday and relays it to the JRCC"),
    (4, INFO, "Met and ocean service supplies wind, sea-state and drift data to plan the search area"),
    (5, INFO, "JRCC tasks the SAR aircraft and the Coast Guard cutter (named On-Scene Coordinator); SITREPs return"),
    (6, INFO, "At JRCC request, MCTS broadcasts a Mayday Relay; vessels of opportunity divert to assist"),
    (7, INFO, "On-Scene Coordinator directs the helicopter and vessels of opportunity in the search area"),
    (8, PHYS, "Air unit drops survival equipment and hoists survivors; the cutter recovers the rest"),
    (9, PHYS, "Survivors are landed ashore or flown by helicopter and handed to EMS and the hospital"),
]
y = KY + 42
for n, c, t in key:
    a(f'<circle cx="54" cy="{y - 5}" r="12" fill="{c}"/>')
    text(54, y, str(n), 13, 800, "#ffffff")
    text(78, y, t, 14.5, 400, INK, anchor="start")
    y += 27
a(f'<text x="{W-40}" y="{H-14}" font-size="12.5" fill="{QUIET}" text-anchor="end">Author: Adekunle Adeniji (1378471) · MGMT6119 · 16 Nov 2026</text>')
a('</svg>')
open(sys.argv[1], "w").write("\n".join(x for x in o if x))
