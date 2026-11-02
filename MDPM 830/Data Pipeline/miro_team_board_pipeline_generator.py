"""Data pipeline frame for the team board (uXjVHidlV4o=): boxes and arrows, little text, in the team's terms.
Writes the Miro Canvas Composer SVG and an HTML preview of the same layout (used for the slide 4 image).
usage: python3 pipe_team.py out_miro.svg out_preview.html"""
import sys, html

W, H = 32000, 11700
FX, FY = 130298, 826000
TITLE = "DATA PIPELINE: FURNITURE REQUEST SERVICE (SLIDE 4)"
INK, NAVY, LINE, LEAK, LOOP = "#1a1a1a", "#2d3e50", "#313131", "#305bab", "#6631d7"
GAP_F, LEAK_F, CONF_F = "#ffc6c6", "#c6dcff", "#fff6b6"

B = {}      # id -> dict(x,y,w,h,fill,html,font,color,stroke,shape,dash,align,valign)
T = []      # text areas: (id,x,y,w,html,font,color)
L = []      # connectors: dict(a,b,sa,eb,label,color,dash,via)


def box(i, x, y, w, h, body, fill="#ffffff", font=240, color=INK, stroke=NAVY, shape=None, dash=False, align="center", valign="middle", sw=2):
    B[i] = dict(x=x, y=y, w=w, h=h, html=body, fill=fill, font=font, color=color, stroke=stroke, shape=shape, dash=dash, align=align, valign=valign, sw=sw)


def text(i, x, y, w, body, font, color=INK):
    T.append((i, x, y, w, body, font, color))


def link(a, b, sa="right", eb="left", label="", color=LINE, dash=False, via=None):
    L.append(dict(a=a, b=b, sa=sa, eb=eb, label=label, color=color, dash=dash, via=via))


# ---------------- layout ----------------
text("t0", 250, 150, 24000, "<b>FURNITURE REQUEST DATA PIPELINE</b>", 460)
text("t1", 250, 780, 31500, "PRISM Requests Furniture Service. Boxes are stages and work steps; arrows show the data that moves. "
     "GAP, LEAK and TO CONFIRM cards come from the Gaps, Leaks and Feasibility section. Dashed outline: pipeline boundary.", 220, "#595959")

# pipeline boundary (Scope, Data Sources and Origin: submission to coordination and hand-offs to fulfilment to closure to reporting)
box("bnd", 3700, 1350, 22000, 10100, "", fill="#ffffff", stroke="#8c8c8c", dash=True, sw=2)

CX = [4100 + i * 4400 for i in range(5)]
CW, R = 3200, [3000, 4350, 5700, 7050]
SH = 1000

stages = [("1. GENERATE", "Owner: each creator"), ("2. COLLECT", "Owner: CMAC (Proposed)"),
          ("3. KEEP AND SHAPE", "Owner: Open (Proposed: FRC)"), ("4. STORE", "Owner: data owner (Open)"),
          ("5. USE", "Owner: data owner; report owners Open")]
for k, (n, o) in enumerate(stages):
    box(f"st{k}", CX[k], 1600, CW, 1000, f"<b>{n}</b><br>{o}", fill=NAVY, color="#ffffff", stroke=NAVY, font=240)

# sources (Step One) and sinks (Step Three)
box("src", 250, 1600, 3100, 1000, "<b>SOURCES</b><br>where data is born", fill=NAVY, color="#ffffff", stroke=NAVY)
box("sp", 250, 3000, 3100, 1500, "<b>People</b><br>original requester, CMAC, FRC, FC, vendor or supplier", fill="#f7f7f7", stroke="#bfbfbf", font=220)
box("sc", 250, 4700, 3100, 1500, "<b>Channels</b><br>WORTS, Outlook or shared inbox, Teams", fill="#f7f7f7", stroke="#bfbfbf", font=220)
box("sr", 250, 6400, 3100, 1500, "<b>Reference</b><br>request checklist, furniture selection reference, roles and authorization rules", fill="#f7f7f7", stroke="#bfbfbf", font=220)
box("out", 250, 8300, 3100, 3050, "<b>Outside the boundary</b><br>Not integrated: SnapTracker, OneGX/SAP, BLIMS, EAMS<br>Out: other WORTS services; historical WORTS migration",
    fill="#ffffff", stroke="#8c8c8c", dash=True, font=210, align="left", valign="top")

box("snk", 26100, 1600, 5650, 1000, "<b>SINKS AND VALUE</b>", fill=NAVY, color="#ffffff", stroke=NAVY)
box("k1", 26100, 3000, 5650, 1500, "<b>Sink 1: Product functionality</b><br>P1 guided submission<br>P2 connected request visibility<br>P3 hand-off support (Proposed)",
    fill="#f0f5fd", stroke="#659df2", font=220, align="left")
box("k2", 26100, 4700, 5650, 1500, "<b>Sink 2: Outcome measurement</b><br>M1: DVO 1, DVO 2, DVO 6", fill="#eaf9ef", stroke="#2dc75c", font=220, align="left")
box("k3", 26100, 6400, 5650, 1500, "<b>Sink 3: Business value</b><br>B1 operational reporting", fill="#fffbed", stroke="#ffdc4a", font=220, align="left")
box("leg", 26100, 8300, 5650, 3050,
    "<b>How to read</b><br>Solid arrow: data hand-off<br>Dashed arrow back: return for missing information<br>Dashed blue: leak<br>Dashed purple: the loop<br>"
    "Every hand-off: authenticate, validate, monitor, mitigate, alarm<br>Slide 9 groups the cards as input reliability, connected request history, information handoffs and measurement readiness",
    fill="#ffffff", stroke="#bfbfbf", font=190, align="left", valign="top")


def step(i, col, row, body, **kw):
    h = kw.pop("h", SH)
    kw.setdefault("font", 230)
    box(i, CX[col], R[row], CW, h, body, **kw)


step("g1", 0, 0, "<b>Need identified</b><br>original requester", shape="circle", fill="#f7f7f7")
step("g2", 0, 1, "<b>Need sent to CMAC</b><br>email, Teams, phone")
step("c1", 1, 0, "<b>CMAC prepares</b><br>checklist, floor plan")
step("c2", 1, 1, "<b>Form submitted</b><br>Request ID, timestamp")
step("c3", 1, 3, "<b>Email, Teams updates</b><br>captured or linked by staff")
step("ka", 2, 0, "<b>Original kept</b><br>as received")
step("kb", 2, 1, "<b>Completeness check</b><br>FRC")
step("kd", 2, 2, "<b>Complete?</b>", shape="rhombus", fill="#f7f7f7", h=1100)
step("s1", 3, 0, "<b>Shared request record</b><br>status, owner, history", shape="can", fill="#e7e7e7")
step("s2", 3, 1, "<b>FRC assigns FC</b><br>status changed")
step("s3", 3, 2, "<b>FC and vendor updates</b><br>quote, delivery, approval")
step("s4", 3, 3, "<b>Final review, close</b><br>FRC")
step("u1", 4, 0, "<b>Request views</b><br>CMACs, coordinators")
step("u2", 4, 1, "<b>Outcome evidence</b><br>evaluators")
step("u3", 4, 3, "<b>Operational reports</b><br>Infrastructure management")
step("u4", 4, 2, "<b>Vendor scheduling</b><br>delivery contacts")

# gap, leak and to-confirm cards, under the stage they belong to (Gaps, Leaks and Feasibility section)
cards = {0: [("GAP", "Floor-plan currentness")],
         1: [("GAP", "Incomplete request information"), ("GAP", "Unclear contact purposes")],
         2: [("TO CONFIRM", "Reusable requirement structure")],
         3: [("LEAK", "Incomplete shared request history")],
         4: [("LEAK", "Delivery information is requested again"), ("GAP", "Notification failure feedback"), ("TO CONFIRM", "Stage-duration measurement")]}
FILL = {"GAP": GAP_F, "LEAK": LEAK_F, "TO CONFIRM": CONF_F}
for col, lst in cards.items():
    for j, (kind, name) in enumerate(lst):
        box(f"x{col}{j}", CX[col], 8500 + j * 1000, CW, 900, f"<b>{kind}:</b> {name}", fill=FILL[kind], stroke=FILL[kind], font=240, align="left")

# ---------------- connections ----------------
link("src", "st0")
for k in range(4):
    link(f"st{k}", f"st{k + 1}")
link("st4", "snk")
link("snk", "st1", "top", "top", "Loop: use creates activity, outcomes and feedback that improve the form and checklist", LOOP, True, via=1420)

link("g1", "g2", "bottom", "top")
link("g2", "c1", "right", "left", "need, location, reason", via=7950)
link("c1", "c2", "bottom", "top")
link("c2", "ka", "right", "left", "submitted request", via=12450)
link("ka", "kb", "bottom", "top")
link("kb", "kd", "bottom", "top")
link("kd", "c2", "left", "bottom", "No: missing information", LINE, True)
link("kd", "s1", "right", "left", "Yes: trusted request", via=16950)
link("s1", "s2", "bottom", "top")
link("s2", "s3", "bottom", "top")
link("s3", "s4", "bottom", "top")
link("c3", "s3", "right", "left", "Leak: not linked to shared history", LEAK, True, via=17300)
link("s1", "u1", "right", "left", "status, owner, next action")
link("s1", "u2", "right", "left", via=21250)
link("s4", "u3", "right", "left", "dated events, outcomes")
link("s3", "u4", "right", "left", "Leak: asked again", LEAK, True)
link("u1", "k1", "right", "left", via=25900)
link("u2", "k2", "right", "left", via=25900)
link("u3", "k3", "right", "left", via=25900)


# ---------------- Miro SVG ----------------
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def miro():
    el = []
    for i, b in B.items():
        sh = f' data-shape="{b["shape"]}"' if b["shape"] else ""
        d = ' stroke-dasharray="5,5"' if b["dash"] else ""
        c = (f' data-content="{esc(b["html"])}" data-text-color="{b["color"]}" data-font-family="noto_sans" data-font-size="{b["font"]}" '
             f'data-text-align="{b["align"]}" data-text-align-vertical="{b["valign"]}"') if b["html"] else ""
        el.append(f'<rect id="{i}"{sh} x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" rx="60" fill="{b["fill"]}" '
                  f'stroke="{b["stroke"]}" stroke-width="{b["sw"]}"{d}{c} />')
    for i, x, y, w, body, f, col in T:
        el.append(f'<textArea id="{i}" x="{x}" y="{y}" width="{w}" fill="{col}" font-family="noto_sans" font-size="{f}" text-align="left">{body}</textArea>')
    for n, l in enumerate(L):
        d = ' stroke-dasharray="5,5"' if l["dash"] else ""
        lab = f' data-content="{esc(l["label"])}"' if l["label"] else ""
        el.append(f'<line id="l{n}" x1="0" y1="0" x2="1" y2="1" data-start="{l["a"]}" data-end="{l["b"]}" stroke="{l["color"]}" stroke-width="4" '
                  f'data-arrow="end"{d} data-shape="elbowed" data-start-side="{l["sa"]}" data-end-side="{l["eb"]}"{lab} />')
    return "\n".join(['<svg xmlns="http://www.w3.org/2000/svg">', f'<g id="tp" transform="translate({FX},{FY})" data-frame="{TITLE}">',
                      f'<rect data-type="frame" x="0" y="0" width="{W}" height="{H}" fill="#ffffff" data-title="{TITLE}" />'] + el + ["</g>", "</svg>"])


# ---------------- HTML preview ----------------
S = 1920 / W


def side(b, s):
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    return {"right": (x + w, y + h / 2), "left": (x, y + h / 2), "top": (x + w / 2, y), "bottom": (x + w / 2, y + h)}[s]


def route(l):
    p1, p2 = side(B[l["a"]], l["sa"]), side(B[l["b"]], l["eb"])
    sa, eb, v = l["sa"], l["eb"], l["via"]
    if sa in ("right", "left") and eb in ("right", "left"):
        if abs(p1[1] - p2[1]) < 1:
            return [p1, p2]
        mx = v if v else (p1[0] + p2[0]) / 2
        return [p1, (mx, p1[1]), (mx, p2[1]), p2]
    if sa in ("top", "bottom") and eb in ("top", "bottom"):
        if sa == eb:
            y = v if v else (min(p1[1], p2[1]) - 300 if sa == "top" else max(p1[1], p2[1]) + 300)
            return [p1, (p1[0], y), (p2[0], y), p2]
        if abs(p1[0] - p2[0]) < 1:
            return [p1, p2]
        my = v if v else (p1[1] + p2[1]) / 2
        return [p1, (p1[0], my), (p2[0], my), p2]
    if sa in ("right", "left"):
        return [p1, (p2[0], p1[1]), p2]
    return [p1, (p1[0], p2[1]), p2]


DASH = 'stroke-dasharray="5,3"'


def preview():
    out = [f'<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0;background:#fff}}'
           f'.f{{position:relative;width:{W*S}px;height:{H*S}px;font-family:"Noto Sans","DejaVu Sans",Arial,sans-serif;overflow:hidden}}'
           f'.b{{position:absolute;box-sizing:border-box;display:flex;padding:0 6px;line-height:1.22;border-radius:4px}}'
           f'.t{{position:absolute;line-height:1.2}} .lab{{position:absolute;transform:translate(-50%,-50%);background:#fff;padding:0 3px;'
           f'font-size:{200*S:.1f}px;color:#1a1a1a;max-width:{1250*S:.1f}px;text-align:center;line-height:1.1}}</style></head><body><div class="f">']
    for i, b in B.items():
        if not b["html"] and i != "bnd":
            continue
        jc = {"left": "flex-start", "center": "center"}[b["align"]]
        ai = {"top": "flex-start", "middle": "center"}[b["valign"]]
        st = (f'left:{b["x"]*S}px;top:{b["y"]*S}px;width:{b["w"]*S}px;height:{b["h"]*S}px;background:{b["fill"]};'
              f'border:{1.4 if b["sw"] else 0}px {"dashed" if b["dash"] else "solid"} {b["stroke"]};color:{b["color"]};'
              f'font-size:{b["font"]*S:.1f}px;justify-content:{jc};align-items:{ai};text-align:{b["align"]};')
        if b["valign"] == "top":
            st += "padding-top:5px;"
        if b["shape"] == "circle":
            st += "border-radius:50%;"
        if b["shape"] == "can":
            st += "border-radius:50%/22%;"
        inner = b["html"]
        if i == "bnd":
            st += "background:transparent;"
        if b["shape"] == "rhombus":
            out.append(f'<div class="b" style="{st}background:none;border:none"><svg style="position:absolute;left:0;top:0" width="{b["w"]*S}" height="{b["h"]*S}">'
                       f'<polygon points="{b["w"]*S/2},1 {b["w"]*S-1},{b["h"]*S/2} {b["w"]*S/2},{b["h"]*S-1} 1,{b["h"]*S/2}" fill="{b["fill"]}" stroke="{b["stroke"]}" stroke-width="1.4"/></svg>'
                       f'<span style="position:relative">{inner}</span></div>')
        else:
            out.append(f'<div class="b" style="{st}"><span>{inner}</span></div>')
    for i, x, y, w, body, f, col in T:
        out.append(f'<div class="t" style="left:{x*S}px;top:{y*S}px;width:{w*S}px;font-size:{f*S:.1f}px;color:{col}">{body}</div>')
    svg = [f'<svg style="position:absolute;left:0;top:0" width="{W*S}" height="{H*S}"><defs>']
    cols = sorted({l["color"] for l in L})
    for k, c in enumerate(cols):
        svg.append(f'<marker id="m{k}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>')
    svg.append("</defs>")
    labs = []
    for l in L:
        pts = route(l)
        d = " ".join(f"{x*S:.1f},{y*S:.1f}" for x, y in pts)
        svg.append(f'<polyline points="{d}" fill="none" stroke="{l["color"]}" stroke-width="1.4" {DASH if l["dash"] else ""} marker-end="url(#m{cols.index(l["color"])})"/>')
        if l["label"]:
            segs = list(zip(pts, pts[1:]))
            (ax, ay), (bx, by) = max(segs, key=lambda s: abs(s[0][0] - s[1][0]) + abs(s[0][1] - s[1][1]))
            mw = max(1250, abs(ax - bx) * 0.9)
            labs.append(f'<div class="lab" style="left:{(ax+bx)/2*S:.1f}px;top:{(ay+by)/2*S:.1f}px;max-width:{mw*S:.1f}px;color:{l["color"]}">{html.escape(l["label"])}</div>')
    svg.append("</svg>")
    # boundary box first, lines, then boxes on top, then labels
    out.insert(1, "".join(svg))
    out += labs
    out.append("</div></body></html>")
    return "\n".join(out)


m = miro()
open(sys.argv[1], "w").write(m)
open(sys.argv[2], "w").write(preview())
allt = m + "".join(b["html"] for b in B.values())
print("boxes", len(B), "lines", len(L), "dashes", allt.count("—") + allt.count("–"), "len", len(m))
