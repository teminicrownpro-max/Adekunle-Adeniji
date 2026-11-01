"""Swimlane process map of the Furniture Request journey (who hands what data to whom), built from the team's
hand-off table, data-elements table and workflow walkthrough. Board units; frame placed right of the main frame."""
import sys

FX, FY = 64000, 0
EDGE = "#4262ff"; INK = "#1a1a1a"; BODY = "#3a3a3a"; PURPLE = "#6631d7"
el, ln = [], []


def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def rect(i, x, y, w, h, fill, html, f=200, color=INK, stroke=EDGE, sw=2, shape=None, align="center", valign="middle", dash=False, rx=60):
    sh = f' data-shape="{shape}"' if shape else ""
    d = ' stroke-dasharray="5,5"' if dash else ""
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke != "none" else ' stroke="none"'
    c = (f' data-content="{esc(html)}" data-text-color="{color}" data-font-family="Lato" data-font-size="{f}" '
         f'data-text-align="{align}" data-text-align-vertical="{valign}"') if html else ""
    el.append(f'<rect id="{i}"{sh} x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}{d}{c} />')


def text(i, x, y, w, body, f, color=INK):
    el.append(f'<textArea id="{i}" x="{x}" y="{y}" width="{w}" fill="{color}" font-family="noto_sans" font-size="{f}" text-align="left">{body}</textArea>')


def conn(a, b, label="", sa="right", eb="left", dash=False, color=EDGE, w=4):
    d = ' stroke-dasharray="5,5"' if dash else ""
    lab = f' data-content="{esc(label)}"' if label else ""
    ln.append(f'<line x1="0" y1="0" x2="1" y2="1" data-start="{a}" data-end="{b}" stroke="{color}" stroke-width="{w}" data-arrow="end"{d} '
              f'data-shape="elbowed" data-start-side="{sa}" data-end-side="{eb}"{lab} />')


W = 63000
text("pt", 1000, 400, 60000, "<b>PROCESS MAP: WHO HANDS WHAT DATA TO WHOM</b>", 640)
text("ps", 1000, 1400, 60000, "<b>The Furniture Request journey as a swimlane map. Each lane is a data source or owner (Step One); each arrow is a hand-off "
     "labelled with the data it carries (Step Two). Dashed purple arrows are leaks and loop-backs (Steps Four and Five).</b>", 240, BODY)

LBL, X0, Y0, LH, NW, NH, CS = 4600, 1000, 4300, 3000, 4300, 1900, 5650
lanes = [("Original requester", "person", "#fff6b6"), ("CMAC", "person", "#ffc6c6"),
         ("Furniture Request Coordinator (FRC)", "Infrastructure staff", "#f8d3af"),
         ("Furniture Coordinator (FC)", "Infrastructure staff", "#f8d3af"), ("Vendor or supplier", "third party", "#dedaff"),
         ("PRISM Requests record", "system (proposed)", "#e7e7e7"), ("Infrastructure management and evaluators", "sink consumers", "#adf0c7")]
GX = X0 + LBL + 300
for k, (nm, ty, col) in enumerate(lanes):
    y = Y0 + k * LH
    rect(f"lb{k}", X0, y, LBL, LH - 120, col, f"<b>{nm}</b><br><i>{ty}</i>", f=230, stroke="none", rx=40)
    rect(f"ln{k}", GX, y, W - GX - 1000, LH - 120, "#f7f7f7" if k % 2 == 0 else "#ffffff", "", stroke="#c6dcff", sw=2, rx=40)

# phase header across the top, mapped to pipeline stages
phases = [("Request", "Generate, Collect", 0, 1, "#d6b56a"), ("Intake review", "Keep and Shape", 2, 4, "#f9c999"),
          ("Fulfilment", "Collect, Store", 5, 7, "#f6a5a5"), ("Closure", "Store", 8, 8, "#cfc9f7"), ("Reporting", "Use, sinks", 9, 9, "#8fdda5")]
for i, (nm, st, c0, c1, col) in enumerate(phases):
    x = GX + 150 + c0 * CS
    rect(f"ph{i}", x, 2900, (c1 - c0) * CS + NW, 1150, col, f"<b>{nm}</b><br>pipeline stage: {st}", f=230, stroke="none", rx=40)


def cx(c): return GX + 150 + c * CS
def ny(l, h=NH): return Y0 + l * LH + (LH - 120 - h) // 2


def node(i, lane, col, html, fill="#ffffff", color=INK, w=NW, h=NH, shape=None, f=200):
    rect(i, cx(col) + (NW - w) // 2, ny(lane, h), w, h, fill, html, f=f, color=color, shape=shape)


node("s0", 0, 0, "<b>Need identified</b>", fill="#adf0c7", w=2600, h=2000, shape="circle")
node("n2", 1, 1, "<b>Prepare and submit request</b><br>guided form, checklist, attachments")
node("n3", 5, 1, "<b>Request record created</b><br>Request ID, timestamps; original kept", fill="#595959", color="#ffffff")
node("n4", 2, 2, "<b>Intake review</b><br>completeness check by request type")
node("d1", 2, 3, "<b>Complete?</b>", fill="#fff6b6", w=3000, h=2300, shape="rhombus")
node("n5", 1, 3, "<b>Respond to clarification</b><br>missing information, updated documents")
node("n6", 2, 4, "<b>Assign Furniture Coordinator</b><br>assignment and ownership recorded")
node("n7", 3, 5, "<b>Coordinate fulfilment</b><br>options, proposal, vendor instructions")
node("n8", 4, 5, "<b>Quote and availability</b>")
node("n9", 1, 6, "<b>Agree proposal</b><br>approval evidence, site contact")
node("d2", 3, 6, "<b>Approval evidence received?</b>", fill="#fff6b6", w=3200, h=2400, shape="rhombus", f=180)
node("n10", 4, 7, "<b>Deliver and install</b><br>delivery confirmation")
node("n11", 3, 7, "<b>Record completion evidence</b><br>delivery, approvals, issues")
node("n12", 2, 8, "<b>Final review and close</b>")
node("n13", 5, 8, "<b>Closure record</b><br>full dated history kept", fill="#595959", color="#ffffff")
node("e0", 0, 9, "<b>Outcome received</b><br>via the CMAC", fill="#adf0c7", w=3000, h=2200, shape="circle", f=180)
node("n15", 6, 9, "<b>Reports and measures</b><br>B1 operational reporting; M1 DVO 1, 2, 6; patterns loop back to the form")
# shared history band in the record lane
rect("hb", cx(3), ny(5, 1300), cx(7) + NW - cx(3), 1300, "#ffffff",
     "<b>Shared request history:</b> every decision, status change, ownership change and material update is dated, attributed and linked to the Request ID",
     f=200, stroke="#595959", sw=3)

conn("s0", "n2", "need, quantity, location, reason", "bottom", "top")
conn("n2", "n3", "submission and attachments", "bottom", "top")
conn("n3", "n4", "Request ID, requirements, documents", "right", "bottom")
conn("n4", "d1")
conn("d1", "n5", "No: missing information", "top", "bottom")
conn("n5", "n4", "updated documents", "left", "top")
conn("d1", "n6", "Yes")
conn("n6", "n7", "Request ID, requirements, assignment", "bottom", "top")
conn("n7", "n8", "specifications, quantities, location, dates", "bottom", "top")
conn("n8", "n7", "quotation, availability", "right", "right")
conn("n7", "n9", "proposal and options", "top", "bottom")
conn("n9", "d2", "agreement, evidence, site contact", "bottom", "top")
conn("d2", "n7", "No: evidence missing", "left", "right", dash=True, color=PURPLE)
conn("d2", "n10", "Yes: delivery details", "bottom", "top")
conn("n10", "n11", "delivery confirmation, issues", "top", "bottom")
conn("n11", "n12", "completion evidence", "right", "bottom")
conn("n12", "n13", "closure decision", "bottom", "top")
conn("n12", "e0", "status and outcome", "top", "bottom")
conn("n13", "n15", "volumes, stages, timestamps, outcomes", "bottom", "top")
conn("n10", "n9", "Potential leak: scheduler asks again for delivery contacts", "left", "bottom", dash=True, color=PURPLE)
conn("n7", "hb", "Leak: email and Teams updates not linked", "left", "top", dash=True, color=PURPLE)

NY = Y0 + len(lanes) * LH + 300
notes = [
    ("<b>How to read it</b><br>Lanes are the people and systems where data is born. Boxes are work steps; diamonds are decisions; circles start and end the journey. "
     "Solid blue arrows are hand-offs, each labelled with the data it carries. The dark grey boxes are the shared request record."),
    ("<b>Controls on every hand-off (Session Four)</b><br>Each arrow carries the five controls: A authenticate (who may move it), V validate (is it acceptable), "
     "F monitor (would we know it stopped), M mitigate (what happens on failure), S alarm (who is told). Detail: main frame, Controls row."),
    ("<b>Evidence and status</b><br>Built from the team's hand-off table and data-elements table, the furniture-service workflow walkthrough and CMAC usability sessions. "
     "Coordinator hand-offs, approval evidence and status meanings are Proposed until the client confirms them."),
]
nw = (W - 2000 - 2 * 600) // 3
for i, t in enumerate(notes):
    rect(f"nt{i}", X0 + i * (nw + 600), NY, nw, 2300, "#ffffff", t, f=210, align="left", valign="top")
H = NY + 2300 + 900

svg = ['<svg xmlns="http://www.w3.org/2000/svg">',
       f'<g id="pm" transform="translate({FX},{FY})" data-frame="PROCESS MAP: FURNITURE REQUEST HAND-OFFS">',
       f'<rect data-type="frame" x="0" y="0" width="{W}" height="{H}" fill="#ffffff" data-title="PROCESS MAP: FURNITURE REQUEST HAND-OFFS" />']
s = "\n".join(svg + el + ln + ["</g>", "</svg>"])
open(sys.argv[1], "w").write(s)
print("H", H, "len", len(s), "items", len(el), "lines", len(ln), "dash", s.count("—") + s.count("–"))
