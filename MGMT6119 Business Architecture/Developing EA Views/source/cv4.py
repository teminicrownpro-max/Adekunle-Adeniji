"""Generate the DoDAF CV-4 Capability Dependencies as SVG.  Usage: python3 cv4.py out.svg"""
import sys
from cv_common import Svg, GROUPS, CAPS, INK, QUIET, GAP

W, H = 1100, 1470
BW, BH = 200, 58
s = Svg(W, H)
s.open()
s.title("CV-4 Capability Dependencies",
        "Maritime Search and Rescue (SAR) · As-Is · notional · DoDAF 2.02 Capability Viewpoint")

POS = {
    "C1.1": (250, 150), "C1.2": (520, 150), "C6.1": (820, 150),
    "C1.3": (420, 262),
    "C2.1": (560, 374), "C2.3": (900, 374),
    "C2.2": (560, 486),
    "C3.1": (330, 598), "C3.2": (790, 598),
    "C3.3": (560, 704),
    "C4.1": (240, 840), "C4.2": (560, 840), "C4.3": (880, 840),
    "C5.2": (240, 970), "C5.1": (560, 970),
    "C5.3": (560, 1092), "C2.4": (960, 1092),
    "C6.3": (560, 1222), "C6.2": (960, 1222),
}
EDGE = "#46525e"

def top(c): x, y = POS[c]; return y - BH / 2
def bot(c): x, y = POS[c]; return y + BH / 2
def left(c): x, y = POS[c]; return x - BW / 2
def right(c): x, y = POS[c]; return x + BW / 2

def pill(x, y, label, color=EDGE):
    w = 12 + 7.6 * len(label)
    s.add(f'<rect x="{x - w/2}" y="{y - 10}" width="{w}" height="20" rx="10" fill="#ffffff" stroke="{color}" stroke-width="1.3"/>')
    s.text(x, y + 4.5, label, 11.5, 700, color)

# foundation band (drawn first, under everything)
s.rect(30, 1160, 1040, 110, "#f4f6f8", GROUPS["C6"][1], sw=1.6, rx=12, dash="8 5")
s.text(48, 1186, "C6 FOUNDATION ENABLERS", 13, 800, GROUPS["C6"][1], anchor="start", spacing="1")
s.text(48, 1208, "Underpin every capability above;", 13.5, 400, INK, anchor="start")
s.text(48, 1226, "drawn as one band, not 19 arrows each", 13.5, 400, INK, anchor="start")

# ---- dependencies (enabling -> dependent)
P = s.path
P(f"M335 {bot('C1.1')} V{top('C1.3')}", "#1b2a3a", 3.4, marker="cp")                                   # D1
P(f"M470 {bot('C1.2')} V{top('C1.3')}", EDGE)                                   # D2
P(f"M490 {bot('C1.3')} V{top('C2.1')}", "#1b2a3a", 3.4, marker="cp")                                   # D3
P(f"M760 {bot('C6.1')} V357 H{right('C2.1')}", EDGE)                             # D4
P(f"M{left('C2.3')} 390 H{right('C2.1')}", EDGE)                                 # D5
P(f"M560 {bot('C2.1')} V{top('C2.2')}", "#1b2a3a", 3.4, marker="cp")                                   # D6
P(f"M560 {bot('C2.2')} V542", "#1b2a3a", 3.4, end=False, marker="cp")                                  # D7/D8 trunk
P(f"M560 542 H330 V{top('C3.1')}", "#1b2a3a", 3.4, marker="cp")                                        # D7
P(f"M560 542 H790 V{top('C3.2')}", EDGE)                                        # D8
P(f"M{right('C3.1')} 606 H510 V{top('C3.3')}", "#1b2a3a", 3.4, marker="cp")                             # D9
P(f"M{left('C3.2')} 606 H610 V{top('C3.3')}", EDGE)                              # D10
P(f"M{right('C3.3')} 704 H960 V{bot('C2.3')}", EDGE)                             # D11
P(f"M560 {bot('C3.3')} V772", "#1b2a3a", 3.4, end=False, marker="cp")                                  # D12-14 trunk
P(f"M560 772 H240 V{top('C4.1')}", "#1b2a3a", 3.4, marker="cp")                                        # D12
P(f"M560 772 V{top('C4.2')}", EDGE)                                             # D13
P(f"M560 772 H880 V{top('C4.3')}", EDGE)                                        # D14
P(f"M240 {bot('C4.1')} V{top('C5.2')}", "#1b2a3a", 3.4, marker="cp")                                   # D15
P(f"M560 {bot('C4.2')} V{top('C5.1')}", EDGE)                                   # D16
P(f"M560 {bot('C5.1')} V{top('C5.3')}", EDGE)                                   # D17
P(f"M240 {bot('C5.2')} V1092 H{left('C5.3')}", "#1b2a3a", 3.4, marker="cp")                             # D18
P(f"M960 {top('C6.2')} V{bot('C2.4')}", EDGE)                                   # D19
P(f"M{left('C2.4')} 1092 H{right('C5.3')}", GAP, 2.4, dash="8 5", marker="gap")  # D20 gap
s.add(f'<circle cx="560" cy="542" r="3.5" fill="{EDGE}"/><circle cx="560" cy="772" r="3.5" fill="{EDGE}"/>')

# ---- capability boxes
for cap, (x, y) in POS.items():
    g = cap.split(".")[0]
    _, strong, light = GROUPS[g]
    s.rect(x - BW / 2, y - BH / 2, BW, BH, light, strong, sw=1.8, rx=9)
    lines = CAPS[cap]
    if cap == "C6.3":
        lines = ["Readiness: trained crews", "and available assets"]
    if cap == "C6.2":
        lines = ["Communications and", "information exchange"]
    s.text(x - BW / 2 + 10, y - BH / 2 + 17, cap, 11.5, 800, strong, anchor="start", spacing="0.4")
    if len(lines) == 1:
        s.text(x, y + 12, lines[0], 14, 600, INK)
    else:
        fs = 13 if max(len(l) for l in lines) > 19 else 14
        s.text(x, y + 4, lines[0], fs, 600, INK)
        s.text(x, y + 20, lines[1], fs, 600, INK)

# ---- dependency ids
for lab, x, y in [("D1", 335, 205), ("D2", 470, 205), ("D3", 490, 318), ("D4", 760, 262),
                  ("D5", 730, 390), ("D6", 560, 430), ("D7", 420, 542), ("D8", 700, 542),
                  ("D9", 470, 606), ("D10", 650, 606), ("D11", 960, 560), ("D12", 380, 772),
                  ("D13", 560, 792), ("D14", 740, 772), ("D15", 240, 905), ("D16", 560, 905),
                  ("D17", 560, 1032), ("D18", 240, 1040), ("D19", 960, 1150)]:
    pill(x, y, lab)
pill(760, 1092, "D20", GAP)
s.text(760, 1072, "GAP: hospital pre-alert", 12.5, 700, GAP)
s.text(760, 1124, "not supported today", 12.5, 400, GAP)
s.text(976, 470, "re-planning", 12.5, 600, QUIET, anchor="start", style="italic")
s.text(976, 486, "loop (D11, D5)", 12.5, 600, QUIET, anchor="start", style="italic")

# ---- legend
LY = 1292
s.add(f'<line x1="40" y1="{LY}" x2="{W-40}" y2="{LY}" stroke="#d5dbe1" stroke-width="1"/>')
s.text(40, LY + 26, "LEGEND", 13.5, 800, QUIET, anchor="start", spacing="1.2")
s.path(f"M40 {LY+50} H92", EDGE, 2)
s.text(102, LY + 55, "A → B: B depends on A (supported today)", 14, 400, INK, anchor="start")
s.path(f"M430 {LY+50} H482", GAP, 2.4, dash="8 5", marker="gap")
s.text(492, LY + 55, "Required dependency, not supported (gap)", 14, 400, INK, anchor="start")
pill(840, LY + 50, "D1")
s.text(864, LY + 55, "Dependency ID (see table)", 14, 400, INK, anchor="start")
s.path(f"M40 {LY+80} H92", "#1b2a3a", 3.4, marker="cp")
s.text(102, LY + 85, "Critical path: the longest chain, 9 capabilities from C1.1 to C5.3", 14, 400, INK, anchor="start")
gx = 40
SHORT = {"C1": "Alerting", "C2": "Coordination", "C3": "Search", "C4": "Rescue", "C5": "Medical", "C6": "Enablers"}
s.text(40, LY + 118, "Groups (CV-2 colours):", 13.5, 700, QUIET, anchor="start")
gx = 196
for g, (names, strong, light) in GROUPS.items():
    s.rect(gx, LY + 104, 22, 18, light, strong, sw=1.6, rx=4)
    s.text(gx + 30, LY + 118, f"{g} {SHORT[g]}", 13.5, 600, INK, anchor="start")
    gx += 147
s.footer()
s.save(sys.argv[1])
