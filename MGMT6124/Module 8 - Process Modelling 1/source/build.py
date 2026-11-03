"""Build the Module 8 use case diagram (SVG/HTML for PDF + editable .drawio) from one model."""
import math, sys, html, os

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

W, H = 1100, 850
INK = "#1f2937"
MUTED = "#4b5563"
INC = "#1d4ed8"   # include arrows
EXT = "#b45309"   # extend arrows
BASE_FILL = "#e3ecf7"
FONT = "Inter, 'Liberation Sans', Arial, sans-serif"

TITLE = "Use Case Diagram: Dining at Denny's Restaurant"
SUB = "MGMT6124 Methods for Business Analysis  |  Module 8: Process Modelling 1  |  Adekunle Adeniji  |  November 3, 2026"
BOUNDARY = (170, 92, 905, 742)          # x1, y1, x2, y2
SYSTEM_NAME = "Denny's Restaurant (Dine-In Service)"

# id, name lines, cx, cy, rx, ry, kind
UCS = [
    ("UC01", ["Order Food"],                 320, 262, 84, 33, "base"),
    ("UC02", ["Eat Food"],                   320, 425, 84, 33, "base"),
    ("UC03", ["Pay for Food"],               320, 588, 84, 33, "base"),
    ("UC04", ["Prepare Food"],               575, 282, 78, 31, "inc"),
    ("UC05", ["Order Beer"],                 575, 152, 76, 31, "ext"),
    ("UC06", ["Verify Legal", "Drinking Age"], 790, 232, 86, 36, "inc"),
    ("UC07", ["Serve Food"],                 575, 425, 76, 31, "inc"),
    ("UC08", ["Present Bill"],               575, 545, 76, 31, "inc"),
    ("UC09", ["Process Card", "Payment"],    790, 664, 86, 36, "ext"),
    ("UC10", ["Add Tip"],                    440, 700, 64, 28, "ext"),
]
UC = {u[0]: u for u in UCS}

# id, name lines, role, x, y, kind
ACTORS = [
    ("customer",  ["Customer"],                    "Primary Actor",   82, 425, "human"),
    ("bartender", ["Bartender"],                   "Secondary Actor", 1008, 140, "human"),
    ("cook",      ["Cook"],                        "Secondary Actor", 1008, 300, "human"),
    ("server",    ["Server"],                      "Secondary Actor", 1008, 492, "human"),
    ("payment",   ["Card Payment", "Processor"],   "Secondary Actor", 1008, 664, "system"),
]
ACT = {a[0]: a for a in ACTORS}
SYS_W, SYS_H = 136, 62

ASSOC = [
    ("customer", "UC01"), ("customer", "UC02"), ("customer", "UC03"),
    ("bartender", "UC05"),
    ("cook", "UC04"),
    ("server", "UC01"), ("server", "UC07"), ("server", "UC08"),
    ("payment", "UC09"),
]
# kind, from, to, condition, label fraction along edge, perpendicular offset (+ = left of travel)
REL = [
    ("include", "UC01", "UC04", None, 0.50, 11, None),
    ("include", "UC02", "UC07", None, 0.50, 11, None),
    ("include", "UC03", "UC08", None, 0.50, 12, None),
    ("include", "UC05", "UC06", None, 0.50, 12, None),
    ("extend",  "UC05", "UC01", "[customer wants beer]", 0.50, 24, None),
    ("extend",  "UC09", "UC03", "[paying by debit/credit]", 0.45, -26, None),
    ("extend",  "UC10", "UC03", "[customer chooses to tip]", 0.5, 0, (300, 664)),
]


def ell_pt(cx, cy, rx, ry, tx, ty):
    dx, dy = tx - cx, ty - cy
    t = 1 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return cx + dx * t, cy + dy * t


def actor_anchor(a, tx, ty):
    _, _, _, x, y, kind = a
    if kind == "system":
        hw, hh = SYS_W / 2, SYS_H / 2
        dx, dy = tx - x, ty - y
        s = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
        return x + dx * s, y + dy * s
    cx, cy = x, y - 10
    dx, dy = tx - cx, ty - cy
    d = math.hypot(dx, dy)
    return cx + dx / d * 27, cy + dy / d * 27


def esc(s):
    return html.escape(s, quote=True)


def text(x, y, s, size=12, weight=400, fill=INK, anchor="middle", italic=False, halo=False):
    style = f"font-style:italic;" if italic else ""
    h = ' stroke="#ffffff" stroke-width="5" stroke-linejoin="round" paint-order="stroke"' if halo else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" style="{style}"{h}>{esc(s)}</text>')


def arrowhead(x, y, fx, fy, color, size=11, spread=26):
    ang = math.atan2(y - fy, x - fx)
    pts = []
    for s in (-1, 1):
        a = ang + math.pi + s * math.radians(spread)
        pts.append((x + size * math.cos(a), y + size * math.sin(a)))
    return (f'<polyline points="{pts[0][0]:.1f},{pts[0][1]:.1f} {x:.1f},{y:.1f} {pts[1][0]:.1f},{pts[1][1]:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="1.6" stroke-linejoin="round"/>')


def stick(x, y, stroke=INK, sw=1.8):
    return "".join([
        f'<circle cx="{x}" cy="{y-38}" r="11" fill="#ffffff" stroke="{stroke}" stroke-width="{sw}"/>',
        f'<line x1="{x}" y1="{y-27}" x2="{x}" y2="{y+5}" stroke="{stroke}" stroke-width="{sw}"/>',
        f'<line x1="{x-21}" y1="{y-16}" x2="{x+21}" y2="{y-16}" stroke="{stroke}" stroke-width="{sw}"/>',
        f'<line x1="{x}" y1="{y+5}" x2="{x-16}" y2="{y+33}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>',
        f'<line x1="{x}" y1="{y+5}" x2="{x+16}" y2="{y+33}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>',
    ])


def build_svg(standalone_legend=True):
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="11in" height="8.5in" '
             f'font-family="{FONT}">')
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')
    # title
    o.append(text(40, 44, TITLE, 22, 700, INK, "start"))
    o.append(text(40, 66, SUB, 11.5, 400, MUTED, "start"))
    # boundary
    x1, y1, x2, y2 = BOUNDARY
    o.append(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="4" fill="#fbfcfe" stroke="{INK}" stroke-width="1.8"/>')
    o.append(text(x1 + 16, y1 + 26, SYSTEM_NAME, 15, 700, INK, "start"))
    o.append(text(x1 + 16, y1 + 43, "System boundary", 10.5, 400, MUTED, "start", italic=True))

    # associations (under ovals)
    for aid, uid in ASSOC:
        a, u = ACT[aid], UC[uid]
        _, _, cx, cy, rx, ry, _ = u
        ax, ay = actor_anchor(a, cx, cy)
        ex, ey = ell_pt(cx, cy, rx, ry, ax, ay)
        o.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{INK}" stroke-width="1.5"/>')

    # relationships
    labels = []
    for kind, f, t, cond, frac, off, fixed in REL:
        _, _, fx, fy, frx, fry, _ = UC[f]
        _, _, tx, ty, trx, try_, _ = UC[t]
        sx, sy = ell_pt(fx, fy, frx, fry, tx, ty)
        ex, ey = ell_pt(tx, ty, trx, try_, fx, fy)
        color = INC if kind == "include" else EXT
        o.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{color}" '
                 f'stroke-width="1.6" stroke-dasharray="7 5"/>')
        o.append(arrowhead(ex, ey, sx, sy, color))
        mx, my = sx + (ex - sx) * frac, sy + (ey - sy) * frac
        d = math.hypot(ex - sx, ey - sy)
        nx, ny = (ey - sy) / d, -(ex - sx) / d   # left normal of travel
        if ny > 0:  # keep "+" meaning "above"
            nx, ny = -nx, -ny
        lx, ly = (mx + nx * off, my + ny * off) if not fixed else fixed
        tag = "«include»" if kind == "include" else "«extend»"
        if cond:
            labels.append(text(lx, ly - 2, tag, 11.5, 600, color, halo=True))
            labels.append(text(lx, ly + 12, cond, 10.5, 500, color, italic=True, halo=True))
        else:
            labels.append(text(lx, ly + 4, tag, 11.5, 600, color, halo=True))

    # use cases
    for uid, lines, cx, cy, rx, ry, kind in UCS:
        fill = BASE_FILL if kind == "base" else "#ffffff"
        sw = 2.0 if kind == "base" else 1.6
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>')
        ident = f"UC-{uid[2:]}"
        if len(lines) == 1:
            o.append(text(cx, cy - 6, ident, 9.5, 600, MUTED))
            o.append(text(cx, cy + 11, lines[0], 13.5, 700 if kind == "base" else 600, INK))
        else:
            o.append(text(cx, cy - 13, ident, 9.5, 600, MUTED))
            o.append(text(cx, cy + 3, lines[0], 13, 600, INK))
            o.append(text(cx, cy + 19, lines[1], 13, 600, INK))
    o.extend(labels)

    # actors
    for aid, lines, role, x, y, kind in ACTORS:
        primary = role.startswith("Primary")
        if kind == "human":
            o.append(stick(x, y, INK, 2.2 if primary else 1.8))
            o.append(text(x, y + 52, lines[0], 14 if primary else 13, 700, INK))
            o.append(text(x, y + 67, f"({role})", 10.5, 500, INC if primary else MUTED))
        else:
            o.append(f'<rect x="{x-SYS_W/2}" y="{y-SYS_H/2}" width="{SYS_W}" height="{SYS_H}" rx="3" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
            o.append(text(x, y - 13, "«system»", 10.5, 500, MUTED))
            o.append(text(x, y + 4, lines[0], 12.5, 700, INK))
            o.append(text(x, y + 19, lines[1], 12.5, 700, INK))
            o.append(text(x, y + SYS_H / 2 + 16, f"({role})", 10.5, 500, MUTED))

    # legend
    lx, ly, lw, lh = 40, 756, 1020, 82
    o.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="4" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>')
    o.append(text(lx + 14, ly + 26, "LEGEND", 10, 700, MUTED, "start"))
    r1, r2, r3 = ly + 22, ly + 44, ly + 66
    c1, c2 = lx + 84, lx + 506
    o.append(f'<line x1="{c1}" y1="{r1}" x2="{c1+48}" y2="{r1}" stroke="{INK}" stroke-width="1.5"/>')
    o.append(text(c1 + 58, r1 + 4, "Association: the actor takes part in the use case", 10.5, 400, INK, "start"))
    o.append(f'<ellipse cx="{c1+24}" cy="{r2}" rx="24" ry="9" fill="{BASE_FILL}" stroke="{INK}" stroke-width="1.6"/>')
    o.append(text(c1 + 58, r2 + 4, "Shaded oval: base use case (a customer goal in the scenario)", 10.5, 400, INK, "start"))
    o.append(f'<line x1="{c2}" y1="{r1}" x2="{c2+46}" y2="{r1}" stroke="{INC}" stroke-width="1.6" stroke-dasharray="7 5"/>')
    o.append(arrowhead(c2 + 48, r1, c2, r1, INC, 9))
    o.append(text(c2 + 58, r1 + 4, "\u00abinclude\u00bb  mandatory, always performed (points to the included use case)", 10.5, 400, INK, "start"))
    o.append(f'<line x1="{c2}" y1="{r2}" x2="{c2+46}" y2="{r2}" stroke="{EXT}" stroke-width="1.6" stroke-dasharray="7 5"/>')
    o.append(arrowhead(c2 + 48, r2, c2, r2, EXT, 9))
    o.append(text(c2 + 58, r2 + 4, "\u00abextend\u00bb  optional, only when the [condition] is true (points to the base)", 10.5, 400, INK, "start"))
    o.append(text(c1, r3 + 4, "Included and extending use cases run inside their base use case, so actors linked to the base (e.g. the Customer and Server) take part in them without a direct line.",
                  10, 400, MUTED, "start", italic=True))
    o.append("</svg>")
    return "\n".join(o)


svg = build_svg()
with open(os.path.join(OUT, "diagram.svg"), "w") as f:
    f.write(svg)

page1 = f"""<!doctype html><html><head><meta charset="utf-8"><title>Use Case Diagram</title>
<style>@page {{ size: 11in 8.5in; margin: 0; }} html,body {{ margin:0; padding:0; background:#fff; }}
svg {{ display:block; }}</style></head><body>{svg}</body></html>"""
with open(os.path.join(OUT, "page1.html"), "w") as f:
    f.write(page1)


# ---------------- draw.io export (same coordinates) ----------------
def x_(s):
    return html.escape(s, quote=True)


cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
def vcell(cid, value, style, x, y, w, h):
    cells.append(f'<mxCell id="{cid}" value="{x_(value)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>')
def ecell(cid, value, style, s, t):
    cells.append(f'<mxCell id="{cid}" value="{x_(value)}" style="{style}" edge="1" parent="1" source="{s}" target="{t}">'
                 f'<mxGeometry relative="1" as="geometry"/></mxCell>')

vcell("title", f"<b style='font-size:22px'>{TITLE}</b><br><span style='font-size:11px;color:#4b5563'>{SUB}</span>",
      "text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;fontFamily=Inter;", 40, 20, 900, 56)
x1, y1, x2, y2 = BOUNDARY
vcell("boundary", f"<b style='font-size:15px'>{SYSTEM_NAME}</b><br><i style='font-size:10px;color:#4b5563'>System boundary</i>",
      "rounded=0;whiteSpace=wrap;html=1;fillColor=#fbfcfe;strokeColor=#1f2937;strokeWidth=2;verticalAlign=top;align=left;"
      "spacingLeft=14;spacingTop=6;fontFamily=Inter;", x1, y1, x2 - x1, y2 - y1)
for uid, lines, cx, cy, rx, ry, kind in UCS:
    name = "<br>".join(lines)
    val = f"<span style='font-size:9px;color:#4b5563'>UC-{uid[2:]}</span><br><b>{name}</b>"
    fill = BASE_FILL if kind == "base" else "#ffffff"
    sw = 2 if kind == "base" else 1.5
    vcell(uid, val, f"ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=#1f2937;strokeWidth={sw};fontSize=13;fontFamily=Inter;",
          cx - rx, cy - ry, 2 * rx, 2 * ry)
for aid, lines, role, x, y, kind in ACTORS:
    if kind == "human":
        val = f"<b>{lines[0]}</b><br><span style='font-size:10px'>({role})</span>"
        vcell(aid, val, "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;"
              "strokeColor=#1f2937;strokeWidth=2;fontSize=13;fontFamily=Inter;", x - 18, y - 49, 36, 82)
    else:
        val = f"<span style='font-size:10px;color:#4b5563'>&laquo;system&raquo;</span><br><b>{'<br>'.join(lines)}</b>"
        vcell(aid, val, "rounded=0;whiteSpace=wrap;html=1;strokeColor=#1f2937;strokeWidth=1.5;fontSize=12;fontFamily=Inter;",
              x - SYS_W / 2, y - SYS_H / 2, SYS_W, SYS_H)
for i, (aid, uid) in enumerate(ASSOC):
    ecell(f"a{i}", "", "endArrow=none;html=1;strokeColor=#1f2937;strokeWidth=1.5;", aid, uid)
for i, (kind, f, t, cond, *_r) in enumerate(REL):
    color = INC if kind == "include" else EXT
    val = f"<b>&laquo;{kind}&raquo;</b>" + (f"<br><i>{cond}</i>" if cond else "")
    ecell(f"r{i}", val, f"endArrow=open;endFill=0;endSize=11;dashed=1;html=1;strokeColor={color};fontColor={color};"
          f"strokeWidth=1.5;labelBackgroundColor=#ffffff;fontSize=11;fontFamily=Inter;", f, t)
vcell("legend",
      "<b>LEGEND</b>&nbsp;&nbsp; Solid line = association &nbsp;|&nbsp; "
      f"<span style='color:{INC}'><b>&laquo;include&raquo;</b></span> dashed arrow = mandatory, points to the included use case &nbsp;|&nbsp; "
      f"<span style='color:{EXT}'><b>&laquo;extend&raquo;</b></span> dashed arrow = optional, runs only if [condition] is true, points to the base use case &nbsp;|&nbsp; "
      "Shaded oval = base use case",
      "text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;fillColor=#f8fafc;strokeColor=#cbd5e1;spacingLeft=10;fontSize=10.5;fontFamily=Inter;",
      40, 772, 1020, 50)

drawio = ('<mxfile host="app.diagrams.net"><diagram id="usecase" name="Use Case Diagram">'
          f'<mxGraphModel dx="1100" dy="850" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
          f'fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="850" math="0" shadow="0"><root>'
          + "".join(cells) + "</root></mxGraphModel></diagram></mxfile>")
with open(os.path.join(OUT, "Dennys-Use-Case-Diagram.drawio"), "w") as f:
    f.write(drawio)
print("built", OUT)
