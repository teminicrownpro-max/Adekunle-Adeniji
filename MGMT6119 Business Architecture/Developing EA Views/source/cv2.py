"""Generate the DoDAF CV-2 Capability Taxonomy as SVG.  Usage: python3 cv2.py out.svg"""
import sys
from cv_common import Svg, GROUPS, CAPS, MEASURES, INK, QUIET, NAVY

W, H = 1240, 965
s = Svg(W, H)
s.open()
s.title("CV-2 Capability Taxonomy",
        "Maritime Search and Rescue (SAR) · As-Is · notional · DoDAF 2.02 Capability Viewpoint")

# root
RX, RY, RW, RH = W / 2, 112, 470, 64
s.rect(RX - RW / 2, RY, RW, RH, NAVY, NAVY, rx=10)
s.text(RX, RY + 27, "C0  Maritime Search and Rescue", 18, 700, "#ffffff")
s.text(RX, RY + 49, "Detect, locate and rescue people in distress at sea; deliver them to care", 13, 400, "#d8e6f5")

COLW, GAPW = 190, 12
X0 = (W - (6 * COLW + 5 * GAPW)) / 2
L1Y, L1H = 222, 70
L2Y0, L2H, L2GAP = 322, 72, 14
BUS = 198

cols = list(GROUPS)
centers = [X0 + i * (COLW + GAPW) + COLW / 2 for i in range(6)]
# bus from root to groups
s.path(f"M{RX} {RY+RH} V{BUS}", "#46525e", 2, end=False)
s.path(f"M{centers[0]} {BUS} H{centers[-1]}", "#46525e", 2, end=False)
for c in centers:
    s.path(f"M{c} {BUS} V{L1Y}", "#46525e", 2, end=False)

kids = {g: [k for k in CAPS if k.split(".")[0] == g] for g in cols}
for i, g in enumerate(cols):
    x = X0 + i * (COLW + GAPW)
    names, strong, light = GROUPS[g]
    enabling = g == "C6"
    # level-1 group box
    s.rect(x, L1Y, COLW, L1H, strong if not enabling else "#ffffff", strong, sw=2.2, dash="7 4" if enabling else None)
    tc = "#ffffff" if not enabling else strong
    s.text(x + COLW / 2, L1Y + 22, g, 13, 800, tc, spacing="0.6")
    for j, n in enumerate(names):
        s.text(x + COLW / 2, L1Y + 42 + j * 18, n, 15.5, 700, tc)
    # spine
    spine = x + 12
    last_mid = L2Y0 + (len(kids[g]) - 1) * (L2H + L2GAP) + L2H / 2
    s.path(f"M{spine} {L1Y+L1H} V{last_mid}", strong, 2, end=False)
    for k_i, cap in enumerate(kids[g]):
        y = L2Y0 + k_i * (L2H + L2GAP)
        bx = x + 26
        bw = COLW - 26
        s.path(f"M{spine} {y + L2H/2} H{bx}", strong, 2, end=False)
        s.rect(bx, y, bw, L2H, light, strong, sw=1.6, rx=8)
        lines = CAPS[cap]
        s.text(bx + 12, y + 20, cap, 12.5, 800, strong, anchor="start", spacing="0.4")
        ty = y + 40 if len(lines) < 3 else y + 37
        lh = 17 if len(lines) < 3 else 14.5
        fs = 14 if len(lines) < 3 else 13
        for li, ln in enumerate(lines):
            s.text(bx + 12, ty + li * lh, ln, fs, 600, INK, anchor="start")
    # measure of effectiveness
    my = L2Y0 + 4 * (L2H + L2GAP) + 6
    s.rect(x, my, COLW, 70, "#ffffff", strong, sw=1.4, rx=8, dash="5 4")
    s.text(x + 12, my + 20, "MEASURE", 11.5, 800, strong, anchor="start", spacing="0.8")
    for li, ln in enumerate(MEASURES[g]):
        s.text(x + 12, my + 39 + li * 17, ln, 13.5, 400, INK, anchor="start")

# brackets: mission vs enabling
BY = my + 96
s.path(f"M{X0} {BY-8} V{BY} H{centers[4] + COLW/2} V{BY-8}", QUIET, 1.4, end=False)
s.text((X0 + centers[4] + COLW / 2) / 2, BY + 22, "Mission capabilities, in the order of a rescue: alert → coordinate → search → rescue → treat", 14, 600, QUIET)
x6 = X0 + 5 * (COLW + GAPW)
s.path(f"M{x6} {BY-8} V{BY} H{x6 + COLW} V{BY-8}", QUIET, 1.4, end=False)
s.text(x6 + COLW / 2, BY + 22, "Support all of C1 to C5", 14, 600, QUIET)

# legend
LY = BY + 54
s.add(f'<line x1="40" y1="{LY}" x2="{W-40}" y2="{LY}" stroke="#d5dbe1" stroke-width="1"/>')
s.text(40, LY + 28, "LEGEND", 13.5, 800, QUIET, anchor="start", spacing="1.2")
ly = LY + 52
s.rect(40, ly - 16, 40, 24, NAVY, NAVY, rx=5)
s.text(90, ly + 1, "Root capability (level 0)", 14.5, 400, INK, anchor="start")
s.rect(300, ly - 16, 40, 24, GROUPS["C4"][1], GROUPS["C4"][1], rx=5)
s.text(350, ly + 1, "Capability group (level 1)", 14.5, 400, INK, anchor="start")
s.rect(570, ly - 16, 40, 24, GROUPS["C2"][2], GROUPS["C2"][1], rx=5)
s.text(620, ly + 1, "Sub-capability (level 2)", 14.5, 400, INK, anchor="start")
s.rect(830, ly - 16, 40, 24, "#ffffff", GROUPS["C6"][1], rx=5, dash="6 3")
s.text(880, ly + 1, "Enabling group / measure (dashed)", 14.5, 400, INK, anchor="start")
ly2 = ly + 34
s.path(f"M40 {ly2-4} H80", "#46525e", 2, end=False)
s.text(90, ly2 + 1, "Connector = \"is part of\" (whole–part hierarchy)", 14.5, 400, INK, anchor="start")
s.text(570, ly2 + 1, "IDs encode the parent: C2.1 is part of C2. Colours are reused in the CV-4.", 14.5, 400, INK, anchor="start")
s.footer()
s.save(sys.argv[1])
