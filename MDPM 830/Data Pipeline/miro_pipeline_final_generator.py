"""One coherent Furniture Request data pipeline for frame 3458764689102673046 on board uXjVETT1rZQ=.
Band A: the pipeline diagram (native shapes and connectors): sources, five stages with owners, hand-offs H1 to H5,
        sinks, feedback loops F1 to F3 from each sink back to its stages, gap and leak markers G1, L1, L2, V1.
Band B: key tables (hand-offs and controls, gaps and leaks, feedback loops, data generated through use) and notes.
Band C: process map (Miro diagram widget).
usage: python3 pipe_final.py create.svg preview.html slide.html"""
import sys, html, math

W = 4800
FRAME_ID, FX, FY = "3458764689102673046", 283309, -31901
TITLE = "FURNITURE REQUEST DATA PIPELINE (FINAL)"
INK, NAVY, LINE, LEAK, LOOP, GREY = "#1a1a1a", "#2d3e50", "#313131", "#305bab", "#6631d7", "#595959"
GAP_F, LEAK_F, CONF_F, NOTE_F, NOTE_S, LOOP_F = "#ffc6c6", "#c6dcff", "#fff6b6", "#f7f7f7", "#bfbfbf", "#efeafc"

B, T, L = {}, [], []          # boxes, text areas, connectors (in drawing order)


def box(i, x, y, w, h, body="", fill="#ffffff", font=20, color=INK, stroke=NAVY, shape=None, dash=False, align="center",
        valign="middle", sw=2, opacity=None):
    B[i] = dict(x=x, y=y, w=w, h=h, html=body, fill=fill, font=font, color=color, stroke=stroke, shape=shape, dash=dash,
                align=align, valign=valign, sw=sw, opacity=opacity)


def text(i, x, y, w, body, font, color=INK):
    T.append((i, x, y, w, body, font, color))


def link(a, b, sa="right", eb="left", label="", color=LINE, dash=False, via=None, arrow=True, kind="elbowed", width=2):
    L.append(dict(a=a, b=b, sa=sa, eb=eb, label=label, color=color, dash=dash, via=via, arrow=arrow, kind=kind, width=width))


def dot(i, x, y, visible=True):
    r = 5
    if visible:
        box(i, x - r, y - r, 2 * r, 2 * r, shape="circle", fill=LOOP, stroke=LOOP, sw=2)
    else:
        box(i, x - 1, y - 1, 2, 2, fill="#ffffff", stroke="none", sw=0, opacity=0)


def note(i, x, y, w, h, body, font=18, **kw):
    kw.setdefault("fill", NOTE_F)
    kw.setdefault("stroke", NOTE_S)
    box(i, x, y, w, h, body, font=font, align="left", valign="top", **kw)


# ======================= title =======================
text("t0", 30, 18, 3600, "<b>FURNITURE REQUEST DATA PIPELINE</b>", 48)
text("t1", 30, 82, 4700, "PRISM Requests Furniture Service. Sources, the five stages with owners, hand-offs H1 to H5, the three sinks, "
     "feedback loops F1 to F3 and findings G1, L1, L2, V1. Proposed or Open: to confirm with client.", 20, GREY)

# ======================= band A: the pipeline =======================
SX, SW = 30, 520
CX, CW = [620 + i * 640 for i in range(5)], 520
KX, KW = 3800, 900
HY, HH = 320, 130
R, SH = [490, 650, 810, 970], 130

box("bnd", 590, 300, 3140, 830, stroke="#8c8c8c", dash=True, fill="#ffffff")
heads = [("1  GENERATE", "Owner: whoever enters it, for what they provide"), ("2  COLLECT", "Owner: CMAC (Proposed); staff for what they capture"),
         ("3  KEEP AND SHAPE", "Owner: Open, to confirm (Proposed: FRC)"), ("4  STORE", "Owner: data owner (Open)"),
         ("5  USE", "Owner: data owner; report owners Open")]
for k, (n, o) in enumerate(heads):
    box(f"st{k}", CX[k], HY, CW, HH, f"<b>{n}</b><br>{o}", fill=NAVY, color="#ffffff", stroke=NAVY, font=20)
box("src", SX, HY, SW, HH, "<b>SOURCES (STEP ONE)</b><br>where each data item is born", fill=NAVY, color="#ffffff", stroke=NAVY, font=20)
box("snk", KX, HY, KW, HH, "<b>SINKS AND VALUE (STEP THREE)</b><br>where the flow ends; each sink is a data use case", fill=NAVY,
    color="#ffffff", stroke=NAVY, font=20)

srcs = [("S1  Original requester", "born when the need is noticed: item, quantity, location, reason"),
        ("S2  CMAC", "born at preparing and submitting: details, checklist, floor plan, attachments"),
        ("S3  FRC", "born at intake review, assignment and closure: completeness, status, owner"),
        ("S4  FC", "born in fulfilment and coordination: progress, quote, approval, delivery"),
        ("S5  Vendor or supplier", "born at quoting and delivery: quotes, dates, scheduling contacts"),
        ("S6  Channels", "WORTS, Outlook, Teams, phone: updates and approvals outside the record"),
        ("S7  Reference rules", "checklist, furniture selection reference, roles and authorization rules"),
        ("S8  PRISM Requests (Proposed)", "every recorded event: Request ID, timestamps, status history")]
for j, (n, d) in enumerate(srcs):
    box(f"so{j}", SX, 490 + j * 97, SW, 86, f"<b>{n}</b><br>{d}", fill=NOTE_F, stroke=NOTE_S, font=16)


def step(i, col, row, title, sub, **kw):
    kw.setdefault("font", 20)
    h = kw.pop("h", SH)
    box(i, CX[col], R[row] + kw.pop("dy", 0), CW, h, f"<b>{title}</b><br>{sub}", **kw)


step("g1", 0, 0, "Need identified", "original requester (S1)", shape="circle", fill=NOTE_F)
step("g2", 0, 1, "Need sent to CMAC", "email, Teams, phone (S6)")
step("c1", 1, 0, "CMAC prepares request", "checklist, floor plan (S2, S7)")
step("c2", 1, 1, "Form submitted", "Request ID, timestamp (S8)")
step("c3", 1, 3, "Email, Teams, vendor messages", "captured or linked by staff (S5, S6)")
step("ka", 2, 0, "Original kept, then linked", "raw kept as received; updates linked to the Request ID")
step("kb", 2, 1, "Completeness check", "FRC, against the checklist (S3, S7)")
box("kd", CX[2], R[2] - 5, CW, 140, "<b>Complete?</b>", shape="rhombus", fill=NOTE_F, font=21)
step("s1", 3, 0, "Shared request record", "one Request ID, dated history (S8)", shape="can", fill="#e7e7e7")
step("s2", 3, 1, "FRC assigns FC", "status and owner changed (S3)")
step("s3", 3, 2, "FC and vendor updates", "quote, delivery, approval (S4, S5)")
step("s4", 3, 3, "Final review and close", "closure and outcome (S3)")
step("u1", 4, 0, "Request views", "CMACs and coordinators")
step("u2", 4, 1, "Outcome evidence", "evaluators")
step("u4", 4, 2, "Vendor scheduling", "delivery contacts")
step("u3", 4, 3, "Operational reports", "Infrastructure management")

# sinks (aligned so each feedback riser leaves from its own sink)
note("k1", KX, 490, KW, 190, "<b>SINK 1: PRODUCT</b><br>P1 guided request submission<br>P2 connected request visibility<br>"
     "P3 coordinator hand-off support (Proposed)<br><b>For:</b> CMACs and coordinators", font=18, fill="#f0f5fd", stroke="#659df2")
note("k2", KX, 700, KW, 190, "<b>SINK 2: MEASUREMENT (M1)</b><br>First-pass submission completeness<br>Status comprehension, retrieval and follow-up effort<br>"
     "Manual reporting effort<br><b>For:</b> product owner and evaluators", font=18, fill="#eaf9ef", stroke="#2dc75c")
note("k3", KX, 910, KW, 190, "<b>SINK 3: BUSINESS (B1)</b><br>Operational reporting: volumes, stage and age,<br>completion trends, recorded hand-offs<br>"
     "<b>For:</b> Infrastructure management", font=18, fill="#fffbed", stroke="#ffdc4a")

# finding tags on the boxes they belong to (detail in table T2)
def tag(i, target, label, fill):
    b = B[target]
    box(i, b["x"] + b["w"] - 205, b["y"] - 19, 200, 36, f"<b>{label}</b>", fill=fill, stroke=fill, font=15)


tag("tg1", "c2", "G1  GAP", GAP_F)
tag("tl1", "c3", "L1  LEAK", LEAK_F)
tag("tl2", "u4", "L2  POTENTIAL LEAK", LEAK_F)
tag("tv1", "u2", "V1  TO VALIDATE", CONF_F)

# main flow
link("src", "st0")
for k, hcode in enumerate(["H1", "H2", "H3", "H4"]):
    link(f"st{k}", f"st{k + 1}", label=hcode)
link("st4", "snk", label="H5")
link("g1", "g2", "bottom", "top")
link("g2", "c1", "right", "left", "need, location, reason", via=1200)
link("c1", "c2", "bottom", "top")
link("c2", "ka", "right", "left", "submitted request, attachments", via=1840)
link("ka", "kb", "bottom", "top")
link("kb", "kd", "bottom", "top")
link("kd", "c2", "left", "bottom", "No: missing information returns to the CMAC", LINE, True)
link("kd", "s1", "right", "left", "Yes: trusted request", via=2480)
link("s1", "s2", "bottom", "top")
link("s2", "s3", "bottom", "top")
link("s3", "s4", "bottom", "top")
link("c3", "s3", "right", "left", "L1: not linked to the shared history", LEAK, True, via=2500)
link("s1", "u1", "right", "left", "status, owner, next action")
link("s1", "u2", "right", "left", via=3120)
link("s4", "u3", "right", "left", "dated events, outcomes")
link("s3", "u4", "right", "left", "L2: asked again", LEAK, True)
link("u1", "k1", "right", "left", via=3750)
link("u2", "k2", "right", "left", via=3750)
link("u3", "k3", "right", "left", via=3750)

# feedback loops F1 to F3: from each sink, up the right margin, back along the top, down into the stage it changes
LANE = {"k1": 265, "k2": 215, "k3": 165}
RISE = {"k1": 4725, "k2": 4750, "k3": 4775}
loops = [("F1", "k1", [("st0", 940), ("st1", 1520)],
          "<b>F1  PRODUCT FEEDBACK:</b> new or updated request information (clarifications, reassignments, status changes) returns to Generate and Collect"),
         ("F2", "k2", [("st2", 2240)],
          "<b>F2  MEASUREMENT FEEDBACK:</b> evaluation findings (completeness, comprehension, retrieval, reporting effort) return to Keep and Shape as data and product changes"),
         ("F3", "k3", [("st0", 820), ("st2", 2040)],
          "<b>F3  BUSINESS FEEDBACK:</b> operational insights and decisions (bottlenecks, workload, process changes) return to Generate as requirements and to Keep and Shape as data and process updates")]
for code, sk, targets, lab in loops:
    y, rx = LANE[sk], RISE[sk]
    sy = B[sk]["y"] + B[sk]["h"] / 2
    dot(f"{code}a", rx, sy)
    dot(f"{code}b", rx, y)
    link(sk, f"{code}a", "right", "left", color=LOOP, dash=True, arrow=False, kind="straight", width=3)
    link(f"{code}a", f"{code}b", "top", "bottom", color=LOOP, dash=True, arrow=False, kind="straight", width=3)
    prev = f"{code}b"
    for n, (st, tx) in enumerate(sorted(targets, key=lambda t: -t[1])):
        j = f"{code}j{n}"
        dot(j, tx, y)
        link(prev, j, "left", "right", color=LOOP, dash=True, arrow=False, kind="straight", width=3)
        port = f"{code}p{n}"
        dot(port, tx, HY, visible=False)
        link(j, port, "bottom", "top", color=LOOP, dash=True, arrow=True, kind="straight", width=3)
        prev = j
    text(f"{code}t", 2300, y - 27, 2380, f"<span style=\"color:{LOOP}\">{lab}</span>", 16, LOOP)

HA = 1290   # height of band A (slide image)

# ======================= band B: key tables and notes =======================
def est_lines(s, w, f):
    plain = html.unescape(__import__("re").sub(r"<[^>]+>", "", s.replace("<br>", "\n")))
    return sum(max(1, math.ceil(len(part) * f * 0.53 / max(10, w - 24))) for part in plain.split("\n"))


def table(tid, x, y, cols, head, rows, font=17, title=None, hfill=NAVY):
    if title:
        text(f"{tid}T", x, y, sum(cols), f"<b>{title}</b>", 24)
        y += 44
    hh = max(est_lines(h, c, font) for h, c in zip(head, cols)) * font * 1.3 + 22
    cx = x
    for k, (h, c) in enumerate(zip(head, cols)):
        box(f"{tid}h{k}", cx, y, c, hh, f"<b>{h}</b>", fill=hfill, color="#ffffff", stroke=hfill, font=font, align="left")
        cx += c
    y += hh
    for r, row in enumerate(rows):
        rh = max(est_lines(v, c, font) for v, c in zip(row, cols)) * font * 1.3 + 22
        cx = x
        for k, (v, c) in enumerate(zip(row, cols)):
            fill = "#ffffff"
            if k == 0 and isinstance(row, tuple) is False and len(row) and row[0].startswith(("<b>G", "<b>L", "<b>V")):
                fill = {"G": GAP_F, "L": LEAK_F, "V": CONF_F}[row[0][3]]
            box(f"{tid}r{r}c{k}", cx, y, c, rh, v if k else f"{v}", fill=fill, stroke=NOTE_S, font=font, align="left")
            cx += c
        y += rh
    return y


Y = HA + 30
# notes row
NW = [1000, 1000, 1220, 700, 740]
nx = 30
notes = [("ntr", "<b>TRUSTED MEANS (KEEP AND SHAPE)</b><br>One Request ID; an agreed status with one meaning; the current responsible role or group; "
          "the information needed for the next step; dates in true order; duplicates checked on an agreed key (Open). "
          "The original stays as submitted. A check proves presence, not accuracy."),
         ("nrec", "<b>THE SHARED RECORD HOLDS (STORE)</b><br>Request ID; requester, CMAC and ministry; item, quantity, reason, location; attachments; "
          "status and responsible role; decisions, ownership changes and dated updates with author; proposal, approval, delivery and closure "
          "kept as separate records. Added to, never overwritten."),
         ("ncon", "<b>CONSTRAINTS (STEP TWO)</b><br><b>Quality:</b> needs may arrive incomplete; floor plans may not be current; status meanings Open<br>"
          "<b>Frequency:</b> event-driven, one request at a time; reports on a set period (to confirm)<br>"
          "<b>Format:</b> form fields and attachments; free text in email, Teams, phone<br>"
          "<b>Ownership:</b> Keep and Shape owner and data owner Open<br><b>Access:</b> role-based (to confirm); retention per the records schedule (Open)"),
         ("nacc", "<b>WHO SEES WHAT (Proposed)</b><br>CMAC: own requests, status, responsible role, next step<br>Coordinators: decisions, ownership changes<br>"
          "Evaluators: outcome evidence<br>Management: aggregated reports only"),
         ("nneed", "<b>WHAT EACH SINK NEEDS (PRD, MILESTONE 3)</b><br><b>Product:</b> latest confirmed status, owner, next action, history<br>"
          "<b>Measurement:</b> consistent definitions, timestamps, missing-data flags<br><b>Business:</b> consistent counts, aggregation, period comparison<br>"
          "Requirements, not technology.")]
NH = 0
for (i, body), w in zip(notes, NW):
    NH = max(NH, est_lines(body, w, 17) * 17 * 1.3 + 30)
for (i, body), w in zip(notes, NW):
    note(i, nx, Y, w, NH, body, font=17)
    nx += w + 10
Y += NH + 50

# T1 hand-offs and controls
Y = table("t1", 30, Y, [560, 720, 440, 2990],
          ["Hand-off", "Data moved", "Frequency", "Controls on the hand-off (Session Four): A authenticate; V validate; F monitor; M mitigate; S alarm"],
          [["<b>H1</b>  Generate to Collect", "Request details and attachments", "Event-driven, intermittent",
            "A: only an authorized requester submits for their ministry. V: required fields and documents by request type. F: needs left in email or Teams stay invisible. M: drafts saved. S: submission confirmed to the requester."],
           ["<b>H2</b>  Collect to Keep and Shape", "Submitted forms, case updates", "Event-driven, intermittent",
            "A: reviewing roles only (to confirm). V: completeness checked; incomplete requests return to the CMAC. F: time from submission to first assignment. M: original kept as submitted. S: CMAC told when action is required."],
           ["<b>H3</b>  Keep and Shape to Store", "Structured case data and linked documents", "Event-driven (Proposed)",
            "A: only coordinators change status or merge duplicates (Proposed). V: standard status list; duplicate check (match key Open). F: every stage change time-stamped and attributed. M: a merged duplicate keeps both histories. S: coordinator alerted to a possible duplicate (Proposed)."],
           ["<b>H4</b>  Store to Use", "Case records and history", "On demand",
            "A: role-based access to every view (to confirm). V: views read the trusted record only. F: a request with no stage change is flagged (threshold Open). M: a failed update is retried and the user told (Proposed). S: stalled request shown to the coordinator (Proposed)."],
           ["<b>H5</b>  Use to the sinks", "Features, evaluation evidence, reporting data", "Varies by sink",
            "A: reports aggregated and role-restricted. V: report figures traceable to the record. F: report freshness on a set period (to confirm). M: retention per the records schedule (to confirm). S: an unanswered Action Required item emails the requester."]],
          title="HAND-OFFS AND CONTROLS (STEP TWO)")
Y += 50

# T2 gaps and leaks
Y = table("t2", 30, Y, [330, 560, 1380, 520, 1060, 860],
          ["Finding", "Where", "What we found", "Dimensions", "Headwind and tailwind", "Implication"],
          [["<b>G1  Gap</b>", "Generate to Collect", "Input reliability: required plans, dimensions and supporting documents may be missing or unreliable. Includes incomplete request information, floor-plan currentness and unclear contact purposes.",
            "Data, process, governance", "Headwind: found only after submission; plan upkeep sits beyond the form. Tailwind: review practice shows what is needed.",
            "Change the workflow: confirm requirements by request type and check completeness earlier. Floor-plan upkeep: phase it or scope it out."],
           ["<b>L1  Leak</b>", "Collect to Store", "Connected request history: updates and decisions are spread across email, Teams and phone and do not all reach the request.",
            "Process, organizational readiness", "Headwind: updates span people and channels. Tailwind: some records are already kept.",
            "Change the workflow: agree which material updates belong in the history and who records them."],
           ["<b>L2  Potential leak</b>", "Store to Use", "Information hand-offs: supplied information may not reach the next responsible person, for example delivery contacts asked for again; a failed notification is not visible to the sender.",
            "Process, organizational readiness, data", "Headwind: onward transfer is inconsistent; the sender cannot see a failed hand-off. Tailwind: contacts are already supplied.",
            "Change the workflow: assign who transfers delivery details and checks receipt. Phase it: failure feedback and recovery."],
           ["<b>V1  To validate</b>", "Keep and Shape to Store to Use", "Measurement readiness: event coverage, meanings and access are not verified. Includes stage-duration measurement and reusable requirement structure.",
            "Data, process", "Headwind: event meanings unverified; free text needs interpretation. Tailwind: existing dates are a starting point.",
            "Phase it: check existing history first; define prospective capture for missing events."]],
          title="GAPS AND LEAKS (STEP FIVE), FROM THE GAPS, LEAKS AND FEASIBILITY SECTION")
Y += 50

# T3 feedback loops and T4 generated data side by side
y3 = table("t3", 30, Y, [170, 470, 1050, 640],
           ["Loop", "From", "What flows back", "Returns to"],
           [["<b>F1</b>", "Sink 1: Product", "New or updated request information: clarifications, reassignments, status changes", "Generate and Collect"],
            ["<b>F2</b>", "Sink 2: Measurement", "Evaluation findings: completeness, comprehension, retrieval, reporting effort", "Keep and Shape, as data and product changes"],
            ["<b>F3</b>", "Sink 3: Business", "Operational insights and decisions: bottlenecks, workload, process changes", "Generate, as requirements; Keep and Shape, as data and process updates"]],
           title="FEEDBACK LOOPS (STEP FOUR)", hfill=LOOP)
y4 = table("t4", 2420, Y, [360, 760, 640, 590],
           ["Data generated", "Examples", "Who collects it", "Where it creates value"],
           [["<b>Activity</b>", "Submission, assignment, status changes, proposal sharing, closure events", "PRISM Requests service (Proposed)", "Request visibility; hand-off history"],
            ["<b>Corrections</b>", "Missing information, clarification requests, resubmissions", "CMACs and coordinators", "Submission guidance; first-pass completeness"],
            ["<b>Outcomes</b>", "Completion confirmations and delivery outcomes, where captured", "Authorized coordinators", "Request visibility; Infrastructure reporting"],
            ["<b>Feedback (Proposed)</b>", "CMAC comments on clarity and the request experience", "Evaluators; ongoing collection to confirm", "Request experience; usability evaluation"],
            ["<b>Derived</b>", "First-pass completeness, time in stage, request trends", "Product or service owner, evaluators", "Outcome measurement; operational reporting"]],
           title="DATA GENERATED THROUGH USE (STEP FOUR)", hfill=LOOP)
Y = max(y3, y4)
note("comp", 2420, Y + 10, 2350, 110,
     "<b>How it compounds:</b> one request gives a dated timeline; many show what is missed and where requests wait; comparable periods give "
     "the measurement baselines; better forms start each cycle from better data. <b>Other products and decisions (conditional, to confirm):</b> Recycle Program "
     "reporting; asset and warranty history. Who records each item: to confirm.", font=17, fill="#ffffff", stroke=LOOP)
note("out", 30, y3 + 10, 2330, Y + 120 - (y3 + 10),
     "<b>OUTSIDE THE BOUNDARY, WITH REASONS (STEP ONE)</b><br><b>Direct integrations</b> with SnapTracker, OneGX/SAP, BLIMS, EAMS, AutoCAD: not assumed; "
     "authorized staff capture or link the information<br><b>Other WORTS and PRISM Core services:</b> different workflows<br>"
     "<b>Historical WORTS migration:</b> outside our current proposal; any future migration needs client confirmation<br>"
     "<b>Vendor-facing application:</b> vendor information is needed; a vendor application is not", font=17, fill="#ffffff", stroke="#8c8c8c", dash=True)
Y += 150
note("leg", 30, Y, 4740, 70,
     "<b>HOW TO READ:</b> solid arrow = hand-off, labelled with its data (H1 to H5 between stages).  Dashed grey back arrow = return for missing information.  "
     "Dashed blue = leak.  Dashed purple = feedback loop from a sink (F1 to F3).  Dashed outline = pipeline boundary.  S1 to S8 = source.  "
     "Tags G1, L1, L2, V1 = findings in the Gaps and Leaks table.", font=17, fill="#ffffff")
Y += 110

# ======================= band C: process map (Miro diagram widget) =======================
PM_Y = Y
text("tpm", 30, PM_Y, 4700, "<b>PROCESS MAP: WHO HANDS WHAT DATA TO WHOM</b>  (Miro diagram from the team hand-off table; the same flow, step by step, by role)", 24)
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
    n6 -.-> |L1: email and Teams updates not linked| r1
    r1 --> |volumes, statuses, timestamps, outcomes| n12"""
H = PM_Y + 60 + 1300


# ======================= writers =======================
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def miro_children():
    el = []
    for i, b in B.items():
        sh = f' data-shape="{b["shape"]}"' if b["shape"] else ""
        d = ' stroke-dasharray="5,5"' if b["dash"] else ""
        op = f' fill-opacity="{b["opacity"]}"' if b["opacity"] is not None else ""
        st = f' stroke="{b["stroke"]}" stroke-width="{b["sw"]}"' if b["stroke"] != "none" else ' stroke="none"'
        c = (f' data-content="{esc(b["html"])}" data-text-color="{b["color"]}" data-font-family="noto_sans" data-font-size="{b["font"]}" '
             f'data-text-align="{b["align"]}" data-text-align-vertical="{b["valign"]}"') if b["html"] else ""
        el.append(f'<rect id="{i}"{sh} x="{b["x"]:.0f}" y="{b["y"]:.0f}" width="{b["w"]:.0f}" height="{b["h"]:.0f}" rx="8" fill="{b["fill"]}"{op}{st}{d}{c} />')
    for i, x, y, w, body, f, col in T:
        el.append(f'<textArea id="{i}" x="{x}" y="{y}" width="{w}" fill="{col}" font-family="noto_sans" font-size="{f}" text-align="left">{body}</textArea>')
    el.append(f'<foreignObject id="pmap" data-type="diagram" data-title="Process map: who hands what data to whom" x="30" y="{PM_Y + 60}" width="1600" height="900">{esc(MERMAID)}</foreignObject>')
    for n, l in enumerate(L):
        d = ' stroke-dasharray="5,5"' if l["dash"] else ""
        lab = f' data-content="{esc(l["label"])}"' if l["label"] else ""
        arr = ' data-arrow="end"' if l["arrow"] else ''
        el.append(f'<line id="l{n}" x1="0" y1="0" x2="1" y2="1" data-start="{l["a"]}" data-end="{l["b"]}" stroke="{l["color"]}" '
                  f'stroke-width="{l["width"]}"{arr}{d} data-shape="{l["kind"]}" data-start-side="{l["sa"]}" data-end-side="{l["eb"]}"{lab} />')
    return el


def create_doc():
    return "\n".join(['<svg xmlns="http://www.w3.org/2000/svg">',
                      f'<g id="fr" data-miro-id="{FRAME_ID}" transform="translate({FX},{FY})" data-frame="{TITLE}">',
                      f'<rect data-type="frame" x="0" y="0" width="{W}" height="{H:.0f}" fill="#ffffff" data-title="{TITLE}" />']
                     + miro_children() + ["</g>", "</svg>"])


def side(b, s):
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    return {"right": (x + w, y + h / 2), "left": (x, y + h / 2), "top": (x + w / 2, y), "bottom": (x + w / 2, y + h)}[s]


def route(l):
    p1, p2 = side(B[l["a"]], l["sa"]), side(B[l["b"]], l["eb"])
    if l["kind"] == "straight":
        return [p1, p2]
    sa, eb, v = l["sa"], l["eb"], l["via"]
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


def preview(height, px):
    S = px / W
    out = [f'<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0;background:#fff}}'
           f'.f{{position:relative;width:{W*S:.0f}px;height:{height*S:.0f}px;font-family:"Noto Sans","DejaVu Sans",Arial,sans-serif;overflow:hidden}}'
           f'.b{{position:absolute;box-sizing:border-box;display:flex;padding:0 {10*S:.1f}px;line-height:1.22;border-radius:3px}}'
           f'.t{{position:absolute;line-height:1.2}} .lab{{position:absolute;transform:translate(-50%,-50%);background:#fff;padding:0 2px;'
           f'font-size:{15*S:.1f}px;text-align:center;line-height:1.1}}</style></head><body><div class="f">']
    svg = [f'<svg style="position:absolute;left:0;top:0" width="{W*S:.0f}" height="{height*S:.0f}"><defs>']
    cols = sorted({l["color"] for l in L})
    for k, c in enumerate(cols):
        svg.append(f'<marker id="m{k}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>')
    svg.append("</defs>")
    labs = []
    for l in L:
        pts = route(l)
        d = " ".join(f"{x*S:.1f},{y*S:.1f}" for x, y in pts)
        dash = 'stroke-dasharray="6,4"' if l["dash"] else ""
        mk = f'marker-end="url(#m{cols.index(l["color"])})"' if l["arrow"] else ""
        svg.append(f'<polyline points="{d}" fill="none" stroke="{l["color"]}" stroke-width="{1.1 if l["width"] < 3 else 1.6}" {dash} {mk}/>')
        if l["label"]:
            segs = list(zip(pts, pts[1:]))
            (ax, ay), (bx, by) = max(segs, key=lambda s: abs(s[0][0] - s[1][0]) + abs(s[0][1] - s[1][1]))
            mw = max(90, abs(ax - bx) * 0.9)
            labs.append(f'<div class="lab" style="left:{(ax+bx)/2*S:.1f}px;top:{(ay+by)/2*S:.1f}px;max-width:{mw*S:.1f}px;color:{l["color"]}">{html.escape(l["label"])}</div>')
    svg.append("</svg>")
    out.append("".join(svg))
    for i, b in B.items():
        if b["y"] > height:
            continue
        if b["opacity"] == 0:
            continue
        jc = {"left": "flex-start", "center": "center"}[b["align"]]
        ai = {"top": "flex-start", "middle": "center"}[b["valign"]]
        st = (f'left:{b["x"]*S:.1f}px;top:{b["y"]*S:.1f}px;width:{b["w"]*S:.1f}px;height:{b["h"]*S:.1f}px;background:{b["fill"]};'
              f'border:{1.1 if b["sw"] else 0}px {"dashed" if b["dash"] else "solid"} {b["stroke"] if b["stroke"] != "none" else "transparent"};color:{b["color"]};'
              f'font-size:{b["font"]*S:.2f}px;justify-content:{jc};align-items:{ai};text-align:{b["align"]};')
        if i == "bnd":
            st += "background:transparent;"
        if b["valign"] == "top":
            st += f"padding-top:{8*S:.1f}px;"
        if b["shape"] == "circle":
            st += "border-radius:50%;padding:0;"
        if b["shape"] == "can":
            st += "border-radius:50%/22%;"
        if b["shape"] == "rhombus":
            out.append(f'<div class="b" style="{st}background:none;border:none"><svg style="position:absolute;left:0;top:0" width="{b["w"]*S:.1f}" height="{b["h"]*S:.1f}">'
                       f'<polygon points="{b["w"]*S/2:.1f},1 {b["w"]*S-1:.1f},{b["h"]*S/2:.1f} {b["w"]*S/2:.1f},{b["h"]*S-1:.1f} 1,{b["h"]*S/2:.1f}" fill="{b["fill"]}" stroke="{b["stroke"]}" stroke-width="1.1"/></svg>'
                       f'<span style="position:relative">{b["html"]}</span></div>')
        else:
            out.append(f'<div class="b" style="{st}"><span>{b["html"]}</span></div>')
    for i, x, y, w, body, f, col in T:
        if y < height:
            out.append(f'<div class="t" style="left:{x*S:.1f}px;top:{y*S:.1f}px;width:{w*S:.1f}px;font-size:{f*S:.2f}px;color:{col}">{body}</div>')
    out += labs
    out.append("</div></body></html>")
    return "\n".join(out)


doc = create_doc()
open(sys.argv[1], "w").write(doc)
open(sys.argv[2], "w").write(preview(PM_Y, 2400))
open(sys.argv[3], "w").write(preview(HA, 2400))
allt = doc + MERMAID
print("boxes", len(B), "lines", len(L), "text", len(T), "H", round(H), "PM_Y", round(PM_Y), "len", len(doc),
      "dashes", allt.count("—") + allt.count("–"), "bsg", sum(allt.lower().count(w) for w in ("bronze", "silver", "gold")))
