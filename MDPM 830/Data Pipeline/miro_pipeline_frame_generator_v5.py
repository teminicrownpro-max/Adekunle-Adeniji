"""Excellent pipeline frame for board uXjVETT1rZQ= (natural Miro scale).
Tier A: native shapes and connectors (the pipeline model, used for the slide 4 image).
Tier B: Miro diagram widget (Mermaid flowchart) as the process map of hand-offs.
usage: python3 pipe_v5.py out_miro.svg out_preview.html"""
import sys, html

W, HA, H = 5060, 1915, 3100          # frame width, height of tier A (slide image), frame height
FX, FY = 0, -8400
TITLE = "DATA PIPELINE: FURNITURE REQUEST SERVICE"
INK, NAVY, LINE, LEAK, LOOP = "#1a1a1a", "#2d3e50", "#313131", "#305bab", "#6631d7"
GAP_F, LEAK_F, CONF_F, NOTE_F, NOTE_S = "#ffc6c6", "#c6dcff", "#fff6b6", "#f7f7f7", "#bfbfbf"

B, T, L = {}, [], []


def box(i, x, y, w, h, body, fill="#ffffff", font=18, color=INK, stroke=NAVY, shape=None, dash=False, align="center", valign="middle", sw=2):
    B[i] = dict(x=x, y=y, w=w, h=h, html=body, fill=fill, font=font, color=color, stroke=stroke, shape=shape, dash=dash, align=align, valign=valign, sw=sw)


def text(i, x, y, w, body, font, color=INK):
    T.append((i, x, y, w, body, font, color))


def link(a, b, sa="right", eb="left", label="", color=LINE, dash=False, via=None):
    L.append(dict(a=a, b=b, sa=sa, eb=eb, label=label, color=color, dash=dash, via=via))


def note(i, x, y, w, h, body, font=16, **kw):
    kw.setdefault("fill", NOTE_F)
    kw.setdefault("stroke", NOTE_S)
    box(i, x, y, w, h, body, font=font, align="left", valign="top", **kw)


# ---------------- title ----------------
text("t0", 30, 22, 3600, "<b>FURNITURE REQUEST DATA PIPELINE</b>", 52)
text("t1", 30, 102, 5000, "PRISM Requests Furniture Service: Furniture Request data from where it is born to where it creates value. "
     "Proposed or Open: to confirm with client.", 21, "#595959")

# ---------------- columns ----------------
SX, SW = 30, 560                       # sources
CX = [650 + i * 660 for i in range(5)]  # stages
CW = 560
KX, KW = 3930, 1100                    # sinks
box("bnd", 620, 165, 3260, 1480, "", stroke="#8c8c8c", dash=True)

stages = [("1. GENERATE", "Owner: each creator, for what they state"), ("2. COLLECT", "Owner: CMAC, for details submitted (Proposed)"),
          ("3. KEEP AND SHAPE", "Owner: Open (Proposed: FRC)"), ("4. STORE", "Owner: data owner (Open)"),
          ("5. USE", "Owner: data owner; report owners Open")]
for k, (n, o) in enumerate(stages):
    box(f"st{k}", CX[k], 190, CW, 130, f"<b>{n}</b><br>{o}", fill=NAVY, color="#ffffff", stroke=NAVY, font=21)
box("src", SX, 190, SW, 130, "<b>SOURCES (STEP ONE)</b><br>where each data item is born", fill=NAVY, color="#ffffff", stroke=NAVY, font=21)
box("snk", KX, 190, KW, 130, "<b>SINKS AND VALUE (STEP THREE)</b><br>consumer, value, what each sink needs", fill=NAVY, color="#ffffff", stroke=NAVY, font=21)

# ---------------- sources: where each is born ----------------
srcs = [("Original requester", "born when the furniture need is identified"),
        ("CMAC", "born at request preparation, submission and clarification"),
        ("FRC", "born at intake review, assignment, final review and closure"),
        ("FC", "born while coordinating fulfilment and recording progress"),
        ("Vendor or supplier", "born at quote, delivery scheduling and confirmation"),
        ("WORTS", "request ID, status and events as the request moves"),
        ("Outlook, shared inbox, Teams", "born in messages exchanged outside WORTS"),
        ("Reference data", "checklist, furniture selection reference, roles and authorization rules")]
for j, (n, d) in enumerate(srcs):
    box(f"so{j}", SX, 360 + j * 162, SW, 145, f"<b>{n}</b><br>{d}", fill=NOTE_F, stroke=NOTE_S, font=20)

# ---------------- work steps ----------------
R = [360, 510, 660, 810]
SH = 125


def step(i, col, row, title, sub, **kw):
    h = kw.pop("h", SH)
    kw.setdefault("font", 21)
    box(i, CX[col], R[row], CW, h, f"<b>{title}</b><br>{sub}", **kw)


step("g1", 0, 0, "Need identified", "original requester", shape="circle", fill=NOTE_F)
step("g2", 0, 1, "Need sent to CMAC", "email, Teams, phone")
step("c1", 1, 0, "CMAC prepares", "checklist, floor plan")
step("c2", 1, 1, "Form submitted", "Request ID, timestamp")
step("c3", 1, 3, "Email, Teams updates", "captured or linked by staff")
step("ka", 2, 0, "Original kept", "as received, never overwritten")
step("kb", 2, 1, "Completeness check", "FRC, against the checklist")
box("kd", CX[2], R[2] - 5, CW, 140, "<b>Complete?</b>", shape="rhombus", fill=NOTE_F, font=22)
step("s1", 3, 0, "Shared request record", "one Request ID, dated history", shape="can", fill="#e7e7e7")
step("s2", 3, 1, "FRC assigns FC", "status changed")
step("s3", 3, 2, "FC and vendor updates", "quote, delivery, approval")
step("s4", 3, 3, "Final review, close", "FRC")
step("u1", 4, 0, "Request views", "CMACs, coordinators")
step("u2", 4, 1, "Outcome evidence", "evaluators")
step("u4", 4, 2, "Vendor scheduling", "delivery contacts")
step("u3", 4, 3, "Operational reports", "Infrastructure management")

# ---------------- notes inside the boundary ----------------
NY, NH = 975, 235
note("ncon", CX[0], NY, CX[1] + CW - CX[0], NH,
     "<b>CONSTRAINTS (STEP TWO)</b><br>"
     "<b>Quality:</b> status meanings not yet agreed; some needs in free text; floor plans may be out of date<br>"
     "<b>Frequency:</b> human-generated and intermittent, one request at a time; updates at each decision<br>"
     "<b>Format:</b> form fields, attachments, email, Teams, phone<br>"
     "<b>Ownership:</b> Keep and Shape owner and data owner Open<br>"
     "<b>Access:</b> to confirm; Proposed: a CMAC sees only their own requests<br>"
     "<b>Retention:</b> to confirm with client", font=21)
note("ntr", CX[2], NY, CW, NH,
     "<b>TRUSTED MEANS</b><br>one Request ID; agreed status, one meaning; current responsible role or group; "
     "information needed for the next step; dates in true order; duplicates checked on an agreed key. "
     "A check confirms presence, not accuracy.", font=21)
note("nrec", CX[3], NY, CW, NH,
     "<b>RECORD HOLDS</b><br>Request ID; requester, CMAC, ministry; need, quantity, location; attachments; "
     "status and responsible role; decisions, ownership changes, dated updates with author; "
     "proposal, approval, delivery, closure kept as separate records.", font=21)
note("nacc", CX[4], NY, CW, NH,
     "<b>WHO SEES WHAT (Proposed)</b><br>CMAC: own requests, status, responsible role, next step<br>"
     "Coordinators: decisions, ownership changes<br>Evaluators: outcome evidence<br>Management: aggregated reports", font=21)

# ---------------- gap, leak and to-confirm cards (Gaps, Leaks and Feasibility) ----------------
cards = {0: [("GAP", "Floor-plan currentness", "Data, governance. Phase it or scope it out.")],
         1: [("GAP", "Incomplete request information", "Data, process. Change the workflow."),
             ("GAP", "Unclear contact purposes", "Data, governance. Change the workflow.")],
         2: [("TO CONFIRM", "Reusable requirement structure", "Data, process. Phase it.")],
         3: [("LEAK", "Incomplete shared request history", "Collect to Store. Process, readiness. Change the workflow.")],
         4: [("LEAK", "Delivery information is requested again", "Store to Use. Process, readiness. Change the workflow."),
             ("GAP", "Notification failure feedback", "Data, process. Phase it."),
             ("TO CONFIRM", "Stage-duration measurement", "Data, process. Phase it.")]}
FILL = {"GAP": GAP_F, "LEAK": LEAK_F, "TO CONFIRM": CONF_F}
for col, lst in cards.items():
    for j, (kind, name, sub) in enumerate(lst):
        box(f"x{col}{j}", CX[col], 1245 + j * 130, CW, 118, f"<b>{kind}:</b> {name}<br>{sub}",
            fill=FILL[kind], stroke=FILL[kind], font=19, align="left")

# ---------------- sinks ----------------
note("k1", KX, 360, KW, 250,
     "<b>SINK 1: PRODUCT FUNCTIONALITY</b><br>P1 guided submission; P2 connected request visibility; P3 coordinator hand-off support (Proposed)<br>"
     "<b>Consumer:</b> CMACs and coordinators<br><b>Value:</b> fewer missing details; status without chasing; continuity when owners change<br>"
     "<b>Needs:</b> latest confirmed status, ownership, next action and relevant history; authorized roles only",
     font=21, fill="#f0f5fd", stroke="#659df2")
note("k2", KX, 630, KW, 240,
     "<b>SINK 2: OUTCOME MEASUREMENT</b><br>M1: DVO 1 first-pass completeness; DVO 2 status comprehension and follow-up; DVO 6 reporting effort<br>"
     "<b>Consumer:</b> product owner and evaluators<br><b>Value:</b> shows whether the product improves its outcomes<br>"
     "<b>Needs:</b> consistent definitions, timestamps, missing-data flags",
     font=21, fill="#eaf9ef", stroke="#2dc75c")
note("k3", KX, 890, KW, 215,
     "<b>SINK 3: BUSINESS VALUE</b><br>B1 operational reporting<br><b>Consumer:</b> Infrastructure management<br>"
     "<b>Value:</b> find recurring delays and bottlenecks<br><b>Needs:</b> consistent counts and stages, aggregation, period comparison",
     font=21, fill="#fffbed", stroke="#ffdc4a")
note("gen", KX, 1125, KW, 520,
     "<b>DATA GENERATED THROUGH USE (THE LOOP)</b><br>"
     "<b>Activity:</b> submission, assignment, status, proposal and closure events. Service records them (Proposed). Value: visibility, hand-off history<br>"
     "<b>Corrections:</b> missing information, clarifications, resubmissions. CMACs and coordinators. Value: better guidance<br>"
     "<b>Outcomes:</b> completion and delivery outcomes. Coordinators. Value: visibility, reporting<br>"
     "<b>Feedback (Proposed):</b> CMAC comments. Evaluators. Value: better request experience<br>"
     "<b>Derived:</b> completeness, time in stage, trends. Owner or evaluators. Value: M1, B1<br>"
     "<b>Compounds:</b> one request gives a timeline; many show what is missed and where requests wait; each cycle starts from better data. Who records each item: to confirm",
     font=22, fill="#ffffff", stroke=LOOP)

# ---------------- bottom band ----------------
BY, BH = 1685, 200
note("out", 30, BY, 1850, BH,
     "<b>OUTSIDE THE BOUNDARY, WITH REASONS (STEP ONE)</b><br>"
     "<b>Direct integrations</b> with SnapTracker, OneGX/SAP, BLIMS, EAMS, AutoCAD: not assumed; authorized staff capture or link the information<br>"
     "<b>Other WORTS and PRISM Core services:</b> different workflows, not the Furniture Request lifecycle<br>"
     "<b>Historical WORTS migration:</b> outside our current proposal; any future migration needs client confirmation<br>"
     "<b>Vendor-facing application:</b> vendor information is needed; a vendor application is not",
     font=20, fill="#ffffff", stroke="#8c8c8c", dash=True)
note("ctl", 1920, BY, 1320, BH,
     "<b>CONTROLS ON EVERY HAND-OFF (SESSION FOUR)</b><br>"
     "<b>Authenticate:</b> who may move it. <b>Validate:</b> is it acceptable. <b>Monitor:</b> would we know it stopped. "
     "<b>Mitigate:</b> what happens on failure. <b>Alarm:</b> who is told.<br>"
     "<b>Example, Collect to Keep and Shape:</b> reviewing roles only; completeness checked; time to first assignment monitored; "
     "original kept; CMAC told when action is required", font=20)
note("prd", 3280, BY, 790, BH,
     "<b>TO THE PRD AND MILESTONE 3</b><br>Each sink's needs (freshness, completeness, form, who may see it) become storage and access "
     "requirements. Requirements, not technology. Open items go to the client.", font=20)
note("leg", 4110, BY, 920, BH,
     "<b>HOW TO READ</b><br>Solid arrow: hand-off, labelled with its data<br>Dashed back arrow: return for missing information<br>"
     "Dashed blue: leak<br>Dashed purple: the loop<br>Dashed outline: pipeline boundary<br>Cards: Gaps, Leaks and Feasibility",
     font=18, fill="#ffffff")

# ---------------- connections ----------------
link("src", "st0")
for k in range(4):
    link(f"st{k}", f"st{k + 1}")
link("st4", "snk")
link("gen", "st1", "right", "top", "Loop: new data flows back to improve the form and checklist", LOOP, True)
link("g1", "g2", "bottom", "top")
link("g2", "c1", "right", "left", "need, quantity, location, reason", via=1260)
link("c1", "c2", "bottom", "top")
link("c2", "ka", "right", "left", "submitted request, attachments", via=1920)
link("ka", "kb", "bottom", "top")
link("kb", "kd", "bottom", "top")
link("kd", "c2", "left", "bottom", "No: missing information", LINE, True)
link("kd", "s1", "right", "left", "Yes: trusted request", via=2570)
link("s1", "s2", "bottom", "top")
link("s2", "s3", "bottom", "top")
link("s3", "s4", "bottom", "top")
link("c3", "s3", "right", "left", "Leak: not linked to shared history", LEAK, True, via=2600)
link("s1", "u1", "right", "left", "status, owner, next action")
link("s1", "u2", "right", "left", via=3225)
link("s4", "u3", "right", "left", "dated events, outcomes")
link("s3", "u4", "right", "left", "Leak: asked again", LEAK, True)
link("u1", "k1", "right", "left", via=3895)
link("u2", "k2", "right", "left", via=3895)
link("u3", "k3", "right", "left", via=3895)

# ---------------- tier B: Miro diagram widget (process map) ----------------
TB_Y = HA + 70
text("t2", 30, TB_Y, 5000, "<b>PROCESS MAP: WHO HANDS WHAT DATA TO WHOM</b> (Miro diagram, from the team's hand-off table; one request, step by step)", 24)
MERMAID = """flowchart LR
    n1([Original requester: need identified])
    n2[CMAC: prepare and submit request]
    n3[FRC: intake review]
    d1{Complete?}
    n4[CMAC: respond to clarification]
    n5[FRC: assign FC]
    n6[FC: coordinate fulfilment]
    n7[Vendor: quote, schedule, deliver]
    n8([Original requester or site contact])
    n9[FC: completion evidence]
    n10[FRC: final review and close]
    n11[CMAC: relay status and outcome]
    r1[(Shared request record)]
    n12[Infrastructure management: reporting]
    n1 --> |need, quantity, location, reason| n2
    n2 --> |request details, supporting documents| n3
    n3 --> d1
    d1 --> |No: missing information| n4
    n4 --> |responses, updated documents| n3
    d1 --> |Yes| n5
    n5 --> |Request ID, requirements, assignment| n6
    n6 --> |specifications, quantities, location, dates| n7
    n7 --> |quotation, schedule, delivery confirmation| n6
    n7 --> |delivery arrangements, access, installation timing| n8
    n6 --> |fulfilment status, approvals, completion evidence| n9
    n9 --> n10
    n6 --> |status, options, decisions| n11
    n11 --> |completion outcome| n1
    n2 --> |creates| r1
    n10 --> |closure| r1
    n6 -.-> |Leak: email and Teams updates not linked| r1
    r1 --> |volumes, statuses, timestamps, outcomes| n12"""


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
        el.append(f'<rect id="{i}"{sh} x="{b["x"]}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" rx="8" fill="{b["fill"]}" '
                  f'stroke="{b["stroke"]}" stroke-width="{b["sw"]}"{d}{c} />')
    for i, x, y, w, body, f, col in T:
        el.append(f'<textArea id="{i}" x="{x}" y="{y}" width="{w}" fill="{col}" font-family="noto_sans" font-size="{f}" text-align="left">{body}</textArea>')
    el.append(f'<foreignObject id="pmap" data-type="diagram" data-title="Process map: who hands what data to whom" x="30" y="{TB_Y + 60}" width="1600" height="900">{esc(MERMAID)}</foreignObject>')
    for n, l in enumerate(L):
        d = ' stroke-dasharray="5,5"' if l["dash"] else ""
        lab = f' data-content="{esc(l["label"])}"' if l["label"] else ""
        el.append(f'<line id="l{n}" x1="0" y1="0" x2="1" y2="1" data-start="{l["a"]}" data-end="{l["b"]}" stroke="{l["color"]}" stroke-width="2" '
                  f'data-arrow="end"{d} data-shape="elbowed" data-start-side="{l["sa"]}" data-end-side="{l["eb"]}"{lab} />')
    return "\n".join(['<svg xmlns="http://www.w3.org/2000/svg">', f'<g id="fr" transform="translate({FX},{FY})" data-frame="{TITLE}">',
                      f'<rect data-type="frame" x="0" y="0" width="{W}" height="{H}" fill="#ffffff" data-title="{TITLE}" />'] + el + ["</g>", "</svg>"])


# ---------------- HTML preview of tier A ----------------
PX = 2400
S = PX / W
DASH = 'stroke-dasharray="6,4"'


def side(b, s):
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    return {"right": (x + w, y + h / 2), "left": (x, y + h / 2), "top": (x + w / 2, y), "bottom": (x + w / 2, y + h)}[s]


def route(l):
    p1, p2 = side(B[l["a"]], l["sa"]), side(B[l["b"]], l["eb"])
    sa, eb, v = l["sa"], l["eb"], l["via"]
    if l["a"] == "gen":   # loop: out to the right margin, up over the stages, down into Collect
        return [p1, (W - 12, p1[1]), (W - 12, 172), (p2[0], 172), p2]
    if sa in ("right", "left") and eb in ("right", "left"):
        if abs(p1[1] - p2[1]) < 1:
            return [p1, p2]
        mx = v if v else (p1[0] + p2[0]) / 2
        return [p1, (mx, p1[1]), (mx, p2[1]), p2]
    if sa in ("top", "bottom") and eb in ("top", "bottom"):
        if abs(p1[0] - p2[0]) < 1:
            return [p1, p2]
        my = v if v else (p1[1] + p2[1]) / 2
        return [p1, (p1[0], my), (p2[0], my), p2]
    if sa in ("right", "left"):
        return [p1, (p2[0], p1[1]), p2]
    return [p1, (p1[0], p2[1]), p2]


def preview():
    out = [f'<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0;background:#fff}}'
           f'.f{{position:relative;width:{W*S:.0f}px;height:{HA*S:.0f}px;font-family:"Noto Sans","DejaVu Sans",Arial,sans-serif;overflow:hidden}}'
           f'.b{{position:absolute;box-sizing:border-box;display:flex;padding:0 {6*S*2:.1f}px;line-height:1.2;border-radius:3px}}'
           f'.t{{position:absolute;line-height:1.2}} .lab{{position:absolute;transform:translate(-50%,-50%);background:#fff;padding:0 2px;'
           f'font-size:{17*S:.1f}px;text-align:center;line-height:1.1}}</style></head><body><div class="f">']
    svg = [f'<svg style="position:absolute;left:0;top:0" width="{W*S:.0f}" height="{HA*S:.0f}"><defs>']
    cols = sorted({l["color"] for l in L})
    for k, c in enumerate(cols):
        svg.append(f'<marker id="m{k}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>')
    svg.append("</defs>")
    labs = []
    for l in L:
        pts = route(l)
        d = " ".join(f"{x*S:.1f},{y*S:.1f}" for x, y in pts)
        svg.append(f'<polyline points="{d}" fill="none" stroke="{l["color"]}" stroke-width="1.3" {DASH if l["dash"] else ""} marker-end="url(#m{cols.index(l["color"])})"/>')
        if l["label"]:
            segs = list(zip(pts, pts[1:]))
            (ax, ay), (bx, by) = max(segs, key=lambda s: abs(s[0][0] - s[1][0]) + abs(s[0][1] - s[1][1]))
            if l["a"] == "gen":
                (ax, ay), (bx, by) = segs[2]
            mw = max(95, abs(ax - bx) * 0.9)
            labs.append(f'<div class="lab" style="left:{(ax+bx)/2*S:.1f}px;top:{(ay+by)/2*S:.1f}px;max-width:{mw*S:.1f}px;color:{l["color"]}">{html.escape(l["label"])}</div>')
    svg.append("</svg>")
    out.append("".join(svg))
    for i, b in B.items():
        jc = {"left": "flex-start", "center": "center"}[b["align"]]
        ai = {"top": "flex-start", "middle": "center"}[b["valign"]]
        st = (f'left:{b["x"]*S:.1f}px;top:{b["y"]*S:.1f}px;width:{b["w"]*S:.1f}px;height:{b["h"]*S:.1f}px;background:{b["fill"]};'
              f'border:1.2px {"dashed" if b["dash"] else "solid"} {b["stroke"]};color:{b["color"]};'
              f'font-size:{b["font"]*S:.2f}px;justify-content:{jc};align-items:{ai};text-align:{b["align"]};')
        if i == "bnd":
            st += "background:transparent;"
        if b["valign"] == "top":
            st += f"padding-top:{8*S:.1f}px;"
        if b["shape"] == "circle":
            st += "border-radius:50%;"
        if b["shape"] == "can":
            st += "border-radius:50%/22%;"
        if b["shape"] == "rhombus":
            out.append(f'<div class="b" style="{st}background:none;border:none"><svg style="position:absolute;left:0;top:0" width="{b["w"]*S:.1f}" height="{b["h"]*S:.1f}">'
                       f'<polygon points="{b["w"]*S/2:.1f},1 {b["w"]*S-1:.1f},{b["h"]*S/2:.1f} {b["w"]*S/2:.1f},{b["h"]*S-1:.1f} 1,{b["h"]*S/2:.1f}" fill="{b["fill"]}" stroke="{b["stroke"]}" stroke-width="1.2"/></svg>'
                       f'<span style="position:relative">{b["html"]}</span></div>')
        else:
            out.append(f'<div class="b" style="{st}"><span>{b["html"]}</span></div>')
    for i, x, y, w, body, f, col in T:
        if y < HA:
            out.append(f'<div class="t" style="left:{x*S:.1f}px;top:{y*S:.1f}px;width:{w*S:.1f}px;font-size:{f*S:.2f}px;color:{col}">{body}</div>')
    out += labs
    out.append("</div></body></html>")
    return "\n".join(out)


m = miro()
open(sys.argv[1], "w").write(m)
open(sys.argv[2], "w").write(preview())
allt = m + "".join(b["html"] for b in B.values()) + MERMAID
print("boxes", len(B), "lines", len(L), "dashes", allt.count("—") + allt.count("–"), "len", len(m), "preview", PX, round(HA * S))
