"""Complete Furniture Request pipeline that keeps the team board's layout (five stage containers in a row,
item cards inside, labelled flows, a data-store cylinder, a sinks tree on the right) and completes it to the rubric.
Monochrome: no stage colours, no bronze/silver/gold, no coloured status. Status is written as text."""
import math, re, sys, json

S = 10; SF = "Lato"; TF = "noto_sans"
INK = "#1a1a1a"; BODY = "#595959"; LINE = "#313131"; EDGE = "#b0b0b0"; SURF = "#f7f7f7"; WHITE = "#ffffff"
el, lines = [], []; n = [0]


def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def est(html, w, f, pad=18):
    cpl = max(1, (w - 2 * pad) / (0.53 * f)); k = 0
    for seg in re.split(r"<br\s*/?>", html):
        k += max(1, math.ceil(len(re.sub(r"<[^>]+>", "", seg)) / cpl))
    return int(k * 1.42 * f + 2 * pad + 0.4 * f)


def nid(p): n[0] += 1; return f"{p}{n[0]}"


def rect(x, y, w, h, fill=WHITE, html="", f=19, align="center", valign="middle", rx=6, stroke=EDGE, sw=2, dash=False, opacity=None,
         color=INK, name="r", shape=None):
    i = nid(name)
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke != "none" else ' stroke="none"'
    if dash: st += ' stroke-dasharray="14,10"'
    op = f' fill-opacity="{opacity}"' if opacity is not None else ""
    sh = f' data-shape="{shape}"' if shape else ""
    c = (f' data-content="{esc(html)}" data-text-color="{color}" data-font-family="{SF}" data-font-size="{f*S}" '
         f'data-text-align="{align}" data-text-align-vertical="{valign}"') if html else ""
    el.append(f'<rect id="{i}"{sh} x="{x*S:.0f}" y="{y*S:.0f}" width="{w*S:.0f}" height="{h*S:.0f}" rx="{rx*S}" fill="{fill}"{op}{st}{c} />')
    return i


def text(x, y, w, body, f, color=INK, align="left"):
    el.append(f'<textArea id="{nid("t")}" x="{x*S:.0f}" y="{y*S:.0f}" width="{w*S:.0f}" fill="{color}" font-family="{TF}" '
              f'font-size="{f*S}" text-align="{align}">{body}</textArea>')


def conn(a, b, sa="right", eb="left", width=4, shape="elbowed", dash=False):
    d = ' stroke-dasharray="14,10"' if dash else ""
    lines.append(f'<line x1="0" y1="0" x2="1" y2="1" data-start="{a}" data-end="{b}" stroke="{LINE}" stroke-width="{width}" data-arrow="end"{d} '
                 f'data-shape="{shape}" data-start-side="{sa}" data-end-side="{eb}" />')


def card(x, y, w, title, sub, f=18):
    html = f"<b>{title}</b><br><i>{sub}</i>" if sub else f"<b>{title}</b>"
    h = est(html, w, f)
    return rect(x, y, w, h, WHITE, html, f=f), h


def panel(x, y, w, html, f=17, fill=WHITE, h=None):
    h = h or est(html, w, f)
    rect(x, y, w, h, fill, html, f=f, align="left", valign="top")
    return h


W = 6100
# ---------- title ----------
text(100, 50, 5900, "<b>FURNITURE REQUEST DATA PIPELINE</b>", 72)
text(100, 160, 5900, "Team DART, MDPM 830. Furniture Request Service within PRISM Requests (PRISM Core), replacing the WORTS request experience. "
     "Stages follow the shape of every pipeline (Session Three); scope, owners, sinks, loop and controls follow the conceptual pipeline template (Session Four).", 22, BODY)
text(100, 232, 5900, "<b>How to read it:</b> dashed outline = scope boundary; dashed arrow = the loop; (Proposed) = our suggestion, not yet confirmed; "
     "Open = needs the client's confirmation. No colour carries meaning.", 20, BODY)

# ---------- layout constants ----------
BX, BY = 50, 320
cols = [100, 820, 1540, 2260, 2980]; CW = 520
HY = BY + 110; CY0 = HY + 140
SX0, SW = 3700, 2300

stages = [
    ("Generate", "someone or something creates data as work happens", [
        ("Original requester", "person: furniture need, quantity, location"), ("CMAC", "person: request details, documents"),
        ("Furniture Request Coordinator (FRC)", "staff: intake, assignment, closure decisions"), ("Furniture Coordinator (FC)", "staff: fulfilment progress, coordination"),
        ("Vendor or supplier", "third party: quotes, delivery updates"), ("PRISM Requests", "system (proposed): Request ID, timestamps, status history")]),
    ("Collect", "it gets captured, under someone's permission", [
        ("Request submission", "guided form fields, checklist, attachments"), ("Case activity", "FRC and FC decisions, status changes, messages"),
        ("Vendor correspondence", "relevant information captured by staff")]),
    ("Keep and Shape", "the original is kept; a consistent, trusted version is made", [
        ("Original data", "submission, attachments and messages, kept as submitted"), ("Check completeness", "required fields, documents, contacts; incomplete requests return to the CMAC"),
        ("Organize and link", "one Request ID, one status, a named owner, linked records"), ("Prepare reporting", "consistent definitions, reporting fields")]),
    ("Store", "it lives somewhere more than one consumer can reach", []),
    ("Use", "a feature, a model, a report, a decision", [
        ("Features", "request views for CMACs and coordinators"), ("Evaluation", "outcome measures for evaluators"), ("Reports", "operational reports for management")]),
]
owners = ["Owner: each creator, for what they state", "Owner: CMAC, for the details submitted (Proposed); staff, for what they capture",
          "Owner: Open (Proposed: Furniture Request Coordinator)", "Owner: data owner, Open", "Owner: data owner for views; report owners Open"]
cons = ["Intermittent, one request at a time; much is born in email, Teams and phone; floor plans may not be current",
        "Event-driven; prototype limits of 10MB per file and 5MB per reply; updates outside the service are lost unless staff capture them",
        "Status meanings and completion criteria not yet confirmed; no agreed match key for duplicate requests",
        "Retention requirements to confirm; historical WORTS migration an open decision",
        "Who may view, update or share each item is to be confirmed (Proposed: a CMAC sees only their own requests)"]

# item cards first, to size the containers
item_ids, ybottom = [], CY0
pending = []
for k, (name, sub, items) in enumerate(stages):
    x = cols[k]; y = CY0 + 30; ids = []
    for t, b in items:
        html = f"<b>{t}</b><br><i>{b}</i>"; h = est(html, CW - 60, 17)
        pending.append((k, x + 30, y, CW - 60, h, html)); y += h + 18
    ybottom = max(ybottom, y)
CH = max(ybottom - CY0 + 12, 760)

cont = []
for k, (name, sub, items) in enumerate(stages):
    x = cols[k]
    rect(x + 110, HY, CW - 220, 64, WHITE, f"<b>{name}</b>", f=28, stroke=INK, sw=3)
    text(x, HY + 72, CW, f"<i>{sub}</i>", 16, BODY, "center")
    cont.append(rect(x, CY0, CW, CH, SURF, stroke=EDGE, sw=3, rx=4, name="cont"))
    item_ids.append([])
for k, x, y, w, h, html in pending:
    item_ids[k].append(rect(x, y, w, h, WHITE, html, f=17))

# Store: cylinder and record list
sx = cols[3]
rect(sx + 150, CY0 + 30, 220, 250, "#595959", "<b>PRISM REQUEST CASE RECORDS</b>", f=17, stroke="#595959", sw=2, color=WHITE, shape="can")
lst = ("<b>One shared request record, keyed by Request ID</b><br>Request and contact data<br>Status history<br>Assignment and ownership<br>"
       "Supporting records<br>Completion records<br>Timestamps and audit history<br><i>The original is never overwritten</i>")
rect(sx + 30, CY0 + 310, CW - 60, est(lst, CW - 60, 17), WHITE, lst, f=17, align="left", valign="top")

# flows between stages, labels above the line
flows = ["Request details, documents, updates", "Submitted data and attachments", "Validated and structured data", "Authorized case data"]
for k in range(4):
    conn(cont[k], cont[k + 1], width=6)
    rect(cols[k] + CW + 12, CY0 + CH / 2 - 100, 176, 84, WHITE, flows[k], f=15)

# owners and constraints under each stage
OY = CY0 + CH + 24
ch = max(est(f"<b>Constraints:</b> {c}", CW, 16) for c in cons)
for k in range(5):
    rect(cols[k], OY, CW, 84, WHITE, f"<b>{owners[k]}</b>", f=16)
    rect(cols[k], OY + 98, CW, ch, WHITE, f"<b>Constraints:</b> {cons[k]}", f=16, align="left", valign="top")
ROWS_END = OY + 98 + ch

# ---------- sinks panel (tree, as on the team board) ----------
rect(SX0 + SW / 2 - 200, HY, 400, 64, WHITE, "<b>Sinks</b>", f=28, stroke=INK, sw=3)
text(SX0, HY + 72, SW, "<i>where data stops moving and starts creating value (Step Three)</i>", 16, BODY, "center")
CATX, CATW, ITX, ITW, VX, VW = SX0 + 40, 420, SX0 + 520, 600, SX0 + 1180, SW - 1220
groups = [
    ("Product", "request functions", [("P1", "Guided request submission"), ("P2", "Connected request visibility"), ("P3", "Coordinator hand-off support (proposed)")],
     "<b>Value:</b> clearer submissions, better visibility and smoother coordination.<br><b>Consumers:</b> CMACs; Infrastructure staff for P3.<br>"
     "<b>Needs:</b> current status, responsible party, next action, attachments and history; updated at every status or ownership change; "
     "visible to authorized users only.<br><b>PRD:</b> define what each role sees and how updates and missing information are shown."),
    ("Measurement", "M1, tied to the DPO", [("DVO 1", "First-pass submission completeness"), ("DVO 2", "Status comprehension"), ("DVO 2", "Information retrieval"),
                                             ("DVO 2", "Follow-up effort"), ("DVO 6", "Manual reporting effort")],
     "<b>Value:</b> evidence of whether the product improves its intended outcomes. Targets not yet set.<br><b>Consumers:</b> product or service owner and authorized evaluators.<br>"
     "<b>Needs:</b> consistent definitions, reliable dates, comparable periods; a follow-up baseline that includes communication outside the system.<br>"
     "<b>PRD:</b> define how each DVO is measured and what counts as success."),
    ("Business", "beyond the product", [("B1", "Operational reporting")],
     "<b>Value:</b> identify bottlenecks, understand workload and support operational improvements.<br><b>Consumer:</b> authorized Infrastructure management.<br>"
     "<b>Needs:</b> reliable counts, consistent stage definitions, stage-change timestamps and history; aggregated; current enough for decisions.<br>"
     "<b>PRD:</b> define the operational questions reports must answer."),
]
gy = CY0 + 30; cat_ids = []
tree = []
for gname, gsub, its, val in groups:
    vh = est(val, VW, 16); ih = len(its) * 76 - 16; gh = max(vh, ih)
    tree.append((gname, gsub, its, val, gy, gh, vh)); gy += gh + 44
SH = max(gy - CY0, ROWS_END - CY0)
sink_box = rect(SX0, CY0, SW, SH, SURF, stroke=EDGE, sw=3, rx=4, name="sinks")
for gname, gsub, its, val, y0, gh, vh in tree:
    ci = rect(CATX, y0 + gh / 2 - 50, CATW, 100, WHITE, f"<b>{gname}</b><br><i>{gsub}</i>", f=18); cat_ids.append(ci)
    for j, (code, label) in enumerate(its):
        ii = rect(ITX, y0 + j * 76, ITW, 60, WHITE, f"<b>{code}</b>  {label}", f=16)
        conn(ci, ii, width=3)
    rect(VX, y0, VW, gh, WHITE, val, f=16, align="left", valign="top")
for k in range(3):
    conn(item_ids[4][k], cat_ids[k], width=4)

# ---------- the loop (Step Four), inside the boundary ----------
LY = CY0 + SH + 50
loop_cols = [
    "<b>What it creates, and who collects it</b><br>Activity: recorded by PRISM Requests on the Request ID; no reviewer named yet<br>"
    "Outcomes (cost against quote, delivery, cycle time): recorded at fulfilment and closure; not aggregated<br>"
    "Feedback: no collection point or owner yet (to confirm)<br>Corrections (returns, reschedules, cancellations): recorded; not aggregated<br>"
    "Derived (durations, vendor trends, workload): calculated for B1; report owners Open",
    "<b>Where it goes</b><br>Back into this pipeline: better form and checklist, realistic service levels, suggested FC assignment (Proposed)<br>"
    "Other teams (potential): Finance, Procurement, Facilities, HR<br>Leadership: vendor, budget, purchasing policy and staffing decisions",
    "<b>How it builds over time</b><br>One request gives a dated timeline.<br>Many requests show which items are missed and where requests wait.<br>"
    "Comparable periods give the baselines DVO 1, 2 and 6 need.<br>Better forms then produce more complete requests, so each cycle starts from better data.",
]
lw = (W - 2 * BX - 60 - 2 * 40) / 3
lh = max(est(c, lw, 17) for c in loop_cols) + 80
loop_band = rect(BX + 20, LY, W - 2 * BX - 40, lh, WHITE, stroke=LINE, sw=3, dash=True, rx=8, name="loop")
text(BX + 50, LY + 14, 4000, "<b>THE LOOP (Step Four).</b> Using the service creates new data that did not exist before.", 22)
for j, c in enumerate(loop_cols):
    rect(BX + 50 + j * (lw + 40), LY + 64, lw, lh - 84, WHITE, c, f=17, align="left", valign="top")
conn(sink_box, loop_band, sa="bottom", eb="top", width=6, dash=True)
conn(loop_band, cont[0], sa="left", eb="left", width=6, dash=True)

# ---------- scope boundary ----------
BH = LY + lh + 40 - BY
text(BX + 30, BY + 22, 3600, "<b>SCOPE BOUNDARY (Step One).</b> Inside: the Furniture Request journey from need to closure, and the sinks it feeds.", 21)
rect(BX, BY, W - 2 * BX, BH, WHITE, opacity=0, stroke=INK, sw=5, dash=True, rx=12, name="scope")
OUT_Y = BY + BH + 40
outs = [
    "<b>Outside the boundary: out of scope</b><br>Direct integrations with SnapTracker, OneGX/SAP, BLIMS, EAMS and AutoCAD: none is integrated with WORTS today and the "
    "integration approach is not established. Other PRISM Core services. Ministry-wide floor-plan maintenance. A full vendor-facing workflow.",
    "<b>Outside the boundary: open decision</b><br>Historical WORTS migration is outside Team DART's implementation scope; legacy data requirements and access remain to be validated.",
    "<b>Conditional future opportunities, not sinks</b><br>Recycle Program reporting; asset and warranty history. Both need additional confirmed data and use cases.",
]
ow = (W - 2 * BX - 2 * 40) / 3
oh = max(est(o, ow, 17) for o in outs)
for j, o in enumerate(outs):
    rect(BX + j * (ow + 40), OUT_Y, ow, oh, WHITE, o, f=17, align="left", valign="top")
PART1_END = len(el)

# ---------- controls ----------
GY = OUT_Y + oh + 120
text(BX, GY, W - 2 * BX, "<b>CONTROLS AT EVERY HAND-OFF (Session Four).</b> Nodes do the work; connectors carry the data and its controls. "
     "Items marked Proposed or to confirm are not yet agreed.", 24)
ctrl = [
    ("Generate to Collect", ["only an authorized requester submits for their ministry", "required fields and documents by request type",
                             "needs kept in email or Teams stay invisible", "drafts are saved", "submission confirmed to the requester"]),
    ("Collect to Keep and Shape", ["reviewing roles only (to confirm)", "completeness checked at review; incomplete requests return to the CMAC",
                                   "time from submission to first assignment", "original kept as submitted", "CMAC told when action is required"]),
    ("Keep and Shape to Store", ["only coordinators change status or merge duplicates (Proposed)", "standard status list; duplicate check (key to define)",
                                 "every stage change time-stamped and attributed", "a merged duplicate keeps both histories", "coordinator alerted to a possible duplicate (Proposed)"]),
    ("Store to Use", ["role-based access to every view (permissions to confirm)", "views read the trusted record only",
                      "a request with no stage change is flagged (threshold to define)", "a failed update or upload is retried and the user told (Proposed)",
                      "stalled request visible to the coordinator (Proposed)"]),
    ("Use to the sinks", ["reports aggregated and role-restricted", "report figures traceable to the record", "report freshness on a set period (to confirm)",
                          "retention per the records schedule (to confirm)", "an unanswered Action Required item emails the requester"]),
]
Q = ["Authenticate", "Validate", "Monitor", "Mitigate", "Alarm"]
cw = (W - 2 * BX - 4 * 30) / 5
htmls = [f"<b>{hd}</b><br>" + "<br>".join(f"<b>{q}:</b> {r}" for q, r in zip(Q, rows)) for hd, rows in ctrl]
chh = max(est(h, cw, 17) for h in htmls)
for j, h in enumerate(htmls):
    rect(BX + j * (cw + 30), GY + 64, cw, chh, WHITE, h, f=17, align="left", valign="top")

# ---------- gaps and leaks by stage (Step Five) ----------
FY = GY + 64 + chh + 120
text(BX, FY, W - 2 * BX, "<b>GAPS AND LEAKS, BY STAGE (Step Five).</b> Gap: needed data not generated, collected, accessible or trustworthy. "
     "Leak: existing data not reaching its use. Potential leak: underuse whose cause needs confirmation. Validation need: a requirement not yet confirmed.", 22)
finds = [
    [("Gap", "Floor-plan currentness is hard to establish", "Plans come from different sources with uneven upkeep.", "Confirm the source, upkeep responsibility and review; record uncertainty.", "Data; Governance", "Change the submission and review workflow; scope out ministry-wide plan maintenance."),
     ("Gap", "Furniture inventory is not accessible", "A CMAC asked to filter and select furniture; SnapTracker holds inventory.", "Connect an inventory source; the integration approach is not established.", "Data; Process", "Scope it out now; budget for integration if brought into scope.")],
    [("Gap", "Required materials may be missing", "Plans, dimensions or attachments are absent at review, so requests are returned.", "Confirm requirements by request type; check completeness earlier.", "Data; Process", "Change the workflow."),
     ("Validation need", "Contact purposes and timing", "Requester, CMAC, proposal recipient and delivery contact may differ; some are known later.", "Confirm each contact's purpose, timing and who updates it.", "Data; Governance", "Validate, then change collection and hand-off steps."),
     ("Validation need", "Required approval evidence", "Signed quotes and approval emails precede work.", "Confirm the evidence, collection point and responsible role.", "Data; Process; Governance", "Validate, then change the workflow; do not assume one approval process.")],
    [("Validation need", "Rules for trusted status", "Status, responsibility and completion definitions are not confirmed.", "Agree each status meaning, who changes it and what supports it.", "Data; Governance", "Phase it: confirm rules and owners before fixing requirements."),
     ("Validation need", "Structure for recurring requirements", "Some furniture needs sit in open comments.", "Add structured fields only where an agreed use needs them.", "Data; Process", "Phase it.")],
    [("Leak", "Material updates stay outside the shared history", "Updates sit in email, Teams and PDF attachments.", "Agree which updates stay with the request and who records them; link to the Request ID.", "Process; Organizational readiness", "Change recording and hand-off practices.")],
    [("Potential leak", "Delivery information may not reach the next consumer", "Delivery contacts were requested again by the vendor's scheduler.", "Confirm why; assign responsibility for passing details on.", "Process; Organizational readiness", "Change the workflow."),
     ("Gap", "Failure feedback is not reliably available", "A failed email can still show as sent.", "Define the outcome information needed and a recovery action.", "Data; Process", "Phase it to the outcome data available."),
     ("Validation need", "Data for stage-duration reporting", "Dates exist, but event meanings and completeness are unverified.", "Inspect event histories first; missing history is not zero duration.", "Data; Process", "Phase measurement and reporting to verified data.")],
]
fy0 = FY + 110; fbottom = fy0
for k, items in enumerate(finds):
    x = cols[k] - 70; w = CW + 140; y = fy0
    rect(x + 170, y, w - 340, 54, WHITE, f"<b>{stages[k][0]}</b>", f=22, stroke=INK, sw=3); y += 72
    for typ, ttl, issue, close, dims, imp in items:
        html = f"<b>{typ}: {ttl}</b><br>{issue}<br><b>To close:</b> {close}<br><i>Dimensions: {dims}</i><br><b>Implication:</b> {imp}"
        y += panel(x, y, w, html, f=16) + 24
    fbottom = max(fbottom, y)
side = [
    "<b>Headwinds and tailwinds, by dimension</b><br><b>Data.</b> Headwind: reference information hard to verify; dates may not give full event histories. "
    "Tailwind: records, contacts, attachments and dates exist, once checked. Implication: phase measures to verified data.<br>"
    "<b>Process.</b> Headwind: communication and evidence move across channels. Tailwind: checklists and staff review experience show common omissions. "
    "Implication: change the submission and hand-off workflow.<br>"
    "<b>Governance.</b> Headwind: contact purposes, approvals, status definitions, ownership and access not all confirmed. Tailwind: the agreed request journey "
    "gives a focused boundary. Implication: confirm rules and owners first.<br>"
    "<b>Organizational readiness.</b> Headwind: the workflow depends on staff keeping updates; practice differs between ministries. Tailwind: the client supports "
    "focusing on the workflow and the information each step needs. Implication: assign recording responsibility.",
    "<b>To confirm with the client</b><br>Authoritative sources for building, location and floor plans<br>Who is accountable for data quality and the request record<br>"
    "Who may view, update or share each item<br>Which material updates are retained, and for how long<br>A baseline for follow-up effort<br>"
    "The management decisions reporting must support",
]
sy = fy0
for h in side:
    sy += panel(SX0, sy, SW, h, f=17) + 30
H = max(fbottom, sy) + 80

frame = ['<svg xmlns="http://www.w3.org/2000/svg">', '<g id="pipe" transform="translate(0,0)" data-frame="FURNITURE REQUEST DATA PIPELINE (COMPLETE)">',
         f'<rect data-type="frame" x="0" y="0" width="{W*S}" height="{H*S:.0f}" fill="#ffffff" data-title="FURNITURE REQUEST DATA PIPELINE (COMPLETE)" />']
p1 = "\n".join(frame + el[:PART1_END] + lines + ["</g>", "</svg>"])
p2 = "\n".join(frame[:1] + ['<g id="pipe" transform="translate(0,0)" data-frame="FURNITURE REQUEST DATA PIPELINE (COMPLETE)" data-miro-id="FRAMEID">'] + el[PART1_END:] + ["</g>", "</svg>"])
open(sys.argv[1] + "_p1.svg", "w").write(p1); open(sys.argv[1] + "_p2.svg", "w").write(p2)
allsvg = p1 + p2; low = allsvg.lower()
print("W", W, "H", H, "p1", len(p1), "p2", len(p2), "items", len(el), "lines", len(lines),
      "dash", allsvg.count("—") + allsvg.count("–"), "bsg", sum(low.count(w) for w in ("bronze", "silver", "gold")),
      "fills", sorted(set(re.findall(r'fill="(#[0-9a-f]{6})"', allsvg))))
