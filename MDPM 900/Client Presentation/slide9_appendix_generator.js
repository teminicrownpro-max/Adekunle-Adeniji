// Appendix slides for slide 9, Core Product Requirements and Data (Team DART client deck)
const pptxgen = require("pptxgenjs");
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const sharp = require("sharp");
const Fi = require("react-icons/fi");

const W = 10, X0 = 0.56, CW = 8.88;
const C = { bg: "F5F6F8", white: "FFFFFF", ink: "111827", muted: "5B6470", line: "DDE1E6", blue: "1F5FAF", blueL: "EAF2FC", blueB: "C5DAF3", navy: "0B4F9C", navyT: "D6E6F8" };
const FONT = "Arial";

async function icon(Comp, color, size = 256) {
  const svg = renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }));
  const png = await sharp(Buffer.from(svg)).resize(size, size).png().toBuffer();
  return "image/png;base64," + png.toString("base64");
}

function frame(pres, { label, title, subtitle, sources, note }) {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  s.addText("Government of Alberta", { x: X0, y: 0.26, w: 4, h: 0.22, fontFace: FONT, fontSize: 8, color: C.ink, margin: 0, isTextBox: true });
  s.addText("Appendix · Core Product Requirements and Data", { x: W - X0 - 5, y: 0.26, w: 5, h: 0.22, fontFace: FONT, fontSize: 8, color: C.blue, align: "right", margin: 0, isTextBox: true });
  s.addShape(pres.shapes.LINE, { x: X0, y: 0.56, w: CW, h: 0, line: { color: C.blue, width: 1.25 } });
  s.addText(title, { x: X0, y: 0.7, w: CW, h: 0.5, fontFace: FONT, fontSize: 26, color: C.ink, margin: 0, isTextBox: true, objectName: "Title" });
  s.addText(subtitle, { x: X0, y: 1.2, w: CW, h: 0.25, fontFace: FONT, fontSize: 10, color: C.muted, margin: 0, isTextBox: true });
  if (note) s.addText(note, { x: X0, y: 4.84, w: CW, h: 0.2, fontFace: FONT, fontSize: 7.5, italic: true, color: C.muted, margin: 0, isTextBox: true });
  s.addShape(pres.shapes.LINE, { x: X0, y: 5.08, w: CW, h: 0, line: { color: C.line, width: 0.75 } });
  s.addText(sources, { x: X0, y: 5.16, w: 6.3, h: 0.2, fontFace: FONT, fontSize: 7.5, color: C.muted, margin: 0, isTextBox: true });
  s.addText([{ text: "Queen's MDPM  /  Team DART   |   ", options: { color: C.ink } }, { text: label, options: { color: C.blue, bold: true } }],
    { x: W - X0 - 2.6, y: 5.16, w: 2.6, h: 0.2, fontFace: FONT, fontSize: 7.5, align: "right", margin: 0, isTextBox: true });
  return s;
}

function card(pres, s, x, y, w, h, fill = C.white, border = C.line) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: border, width: 0.75 } });
}

// ---------- traceability tables
const HDR = ["Core requirement", "ID", "Requirement", "What we observed", "Priority"];
function traceTable(pres, s, groups) {
  const b = { type: "solid", pt: 0.75, color: C.line };
  const head = HDR.map((t) => ({ text: t, options: { bold: true, color: C.white, fill: { color: C.blue }, fontSize: 8.5, border: [b, b, b, b] } }));
  const rows = [head];
  groups.forEach((g) => {
    g.rows.forEach((r, i) => {
      const row = [];
      if (i === 0) row.push({ text: g.name, options: { rowspan: g.rows.length, bold: true, color: C.navy, fill: { color: C.blueL }, fontSize: 9.5, valign: "middle", border: [b, b, b, b] } });
      row.push({ text: r[0], options: { bold: true, color: C.blue, fontSize: 9, fill: { color: C.white }, border: [b, b, b, b] } });
      row.push({ text: r[1], options: { color: C.ink, fontSize: 9, fill: { color: C.white }, border: [b, b, b, b] } });
      row.push({ text: r[2], options: { color: C.muted, fontSize: 9, fill: { color: C.white }, border: [b, b, b, b] } });
      row.push({ text: r[3], options: { color: C.ink, fontSize: 9, bold: r[3] === "Must", fill: { color: C.white }, border: [b, b, b, b] } });
      rows.push(row);
    });
  });
  s.addTable(rows, { x: X0, y: 1.55, w: CW, colW: [1.45, 0.62, 3.1, 2.86, 0.85], fontFace: FONT, valign: "middle", margin: [0.04, 0.07, 0.04, 0.07], rowH: 0.3 });
}

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.title = "Team DART Appendix: Core Product Requirements and Data";
  pres.author = "Team DART";

  // ---------------------------------------------------------------- A1
  let s = frame(pres, {
    label: "A1", title: "Requirements Traceability (1 of 2)",
    subtitle: "How the core requirements on slide 9 break down, and what we observed for each.",
    sources: "Sources · SPV working draft §5.1 · PRISM usability sessions · WORTS journey mapping",
    note: "Numbering follows the Strategic Product Vision working draft and will be reconciled with the MDPM 883 requirements. Priorities are draft. P1 to P6 are usability participants.",
  });
  traceTable(pres, s, [
    { name: "Guided Submission", rows: [
      ["FR-01", "Guide the CMAC through the form, with a review before submission", "The guided form and review helped testers check a request (P1)", "Must"],
      ["FR-02", "Prefill available building details and make them easy to verify", "Four testers valued autofill; one questioned the prefilled floor (P6)", "Must"],
      ["FR-03", "Explain when to choose Recycle or Combination", "Two testers chose Recycle where both recycled and new were needed (P5, P6)", "Must"],
      ["FR-04", "Use “Date required on site” and explain suggested dates", "Two testers asked what “Requested date” meant (P1, P5)", "Must"],
      ["FR-11", "Separate required actions from reference guidance in the checklist", "Three testers were unsure what the checklist asked of them (P2, P4, P5)", "Should"],
    ] },
    { name: "Clear Status and Next Actions", rows: [
      ["FR-05", "Show stage, owner and next action; keep required, confirmed and update dates distinct", "A fulfilment date beside the requested date was hard to interpret (P5)", "Must"],
      ["FR-07", "Keep the attention cue; show current actions and files above history", "One tester spotted the cue but struggled to find the quote attachment (P2)", "Should"],
      ["FR-15", "Confirm closure; consider an optional service feedback prompt", "Journey mapping found little feedback after closure", "Could"],
    ] },
  ]);
  s.addNotes("Use this slide if asked where the five core requirements on slide 9 come from. Each core requirement groups several detailed requirements, and each detailed requirement traces to something we observed in the usability sessions or found in our discovery work. Guided Submission covers the form, the review step, verifiable prefill, request-type choices, date wording and the checklist. Clear Status and Next Actions covers the status view, pending actions and closure. The numbering follows our working draft and is still being reconciled with the MDPM 883 requirements, and the priorities are draft.");

  // ---------------------------------------------------------------- A2
  s = frame(pres, {
    label: "A2", title: "Requirements Traceability (2 of 2)",
    subtitle: "Continued: communication, governance, retrieval and reporting.",
    sources: "Sources · SPV working draft §5.1 · PRISM usability sessions · Digital Product Opportunity (DPO)",
    note: "Reporting from the record is proposed and was not part of the prototype test. Release timing for reporting is to confirm. P1 to P6 are usability participants.",
  });
  traceTable(pres, s, [
    { name: "Messages and Proposals", rows: [
      ["FR-06", "Keep messages on the work order, with a direct route from an update to its request", "One tester understood the update but struggled to reach the work order (P6)", "Must"],
      ["FR-08", "Show the item details, suitability, costs and timing needed to assess a quote", "Testers asked whether chairs would match and whether timing met the required date", "Must"],
      ["FR-09", "Confirm what was shared, with whom, and that the client decision is pending", "One tester was unsure whether sharing was complete (P2)", "Must"],
    ] },
    { name: "Governed Access and Decisions", rows: [
      ["FR-10", "Keep approval evidence and client decisions with the work order, with applicable reminders", "Three testers described approvals returning by email (P4, P5, P6)", "Should"],
      ["FR-12", "Apply role-based access and purchasing authority to each work order", "The DPO names governed access and purchasing authority as constraints", "Must"],
    ] },
    { name: "Request Retrieval and Reporting", rows: [
      ["FR-13", "Use the work-order record as the basis for reporting volume, time open and delivery", "Operations and reporting scored 4.6, a priority opportunity", "Must"],
      ["FR-14", "Keep the request list, work-order search and pagination", "One tester found an earlier request by its work-order number (P2)", "Could"],
    ] },
  ]);
  s.addNotes("Use this slide if asked how communication, approvals, access and reporting are covered. Messages and Proposals keeps every exchange on the work order and makes clear what was shared and that the client's decision is still pending. Governed Access and Decisions keeps approval evidence with the record, because three testers described approvals still returning by email, and applies role-based access and purchasing authority, which the DPO named as constraints. Retrieval and Reporting keeps search by work-order number, which a tester used naturally, and makes the record the basis for reporting. Be clear that reporting is proposed: it was not part of the prototype test.");

  // ---------------------------------------------------------------- A3
  s = frame(pres, {
    label: "A3", title: "The Work-Order Record",
    subtitle: "Submission creates one record; everything else links to it.",
    sources: "Sources · MDPM 883 data dictionary · SPV working draft §5.2 · Team DART systems map",
    note: "Sources marked “to confirm” depend on GoA decisions. External systems are referenced by fields in Release 1, not connected.",
  });
  const ico = {
    db: await icon(Fi.FiDatabase, "FFFFFF"), user: await icon(Fi.FiUser, C.blue), pin: await icon(Fi.FiMapPin, C.blue), pkg: await icon(Fi.FiPackage, C.blue),
    msg: await icon(Fi.FiMessageSquare, C.blue), chk: await icon(Fi.FiCheckSquare, C.blue), act: await icon(Fi.FiActivity, C.blue),
    shield: await icon(Fi.FiShield, C.blue), arrow: await icon(Fi.FiArrowRight, C.blue),
  };
  // record card
  const rx = X0, ry = 1.55, rw = 2.55, rh = 3.2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: rx, y: ry, w: rw, h: rh, rectRadius: 0.1, fill: { color: C.navy }, line: { color: C.navy, width: 0.75 } });
  s.addImage({ data: ico.db, x: rx + 0.2, y: ry + 0.2, w: 0.3, h: 0.3 });
  s.addText("Work-order record", { x: rx + 0.6, y: ry + 0.17, w: rw - 0.7, h: 0.36, fontFace: FONT, fontSize: 13, bold: true, color: C.white, margin: 0, valign: "middle", isTextBox: true });
  s.addText("Shared case history, inside PRISM Core", { x: rx + 0.2, y: ry + 0.58, w: rw - 0.35, h: 0.22, fontFace: FONT, fontSize: 8.5, color: C.navyT, margin: 0, isTextBox: true });
  s.addText([
    { text: "Request ID", options: { bullet: { indent: 10 }, breakLine: true } },
    { text: "Type and status", options: { bullet: { indent: 10 }, breakLine: true } },
    { text: "Owner and next action", options: { bullet: { indent: 10 }, breakLine: true } },
    { text: "Dates: required on site, confirmed, last updated", options: { bullet: { indent: 10 }, breakLine: true } },
    { text: "Description and funding", options: { bullet: { indent: 10 } } },
  ], { x: rx + 0.2, y: ry + 0.88, w: rw - 0.35, h: 1.25, fontFace: FONT, fontSize: 9, color: C.white, paraSpaceAfter: 3, margin: 0, valign: "top", isTextBox: true });
  s.addShape(pres.shapes.LINE, { x: rx + 0.2, y: ry + 2.2, w: rw - 0.4, h: 0, line: { color: "3D73B5", width: 0.75 } });
  s.addText([
    { text: "Principles", options: { bold: true, breakLine: true } },
    { text: "Capture once. Keep the original and record corrections. Link every update to the Request ID. Report from the same record." },
  ], { x: rx + 0.2, y: ry + 2.28, w: rw - 0.35, h: 0.85, fontFace: FONT, fontSize: 8.5, color: C.white, margin: 0, valign: "top", isTextBox: true });
  // entity grid
  const gx = rx + rw + 0.3, gw = (X0 + CW - gx - 0.4) / 3, gh = 1.5;
  const ents = [
    [ico.user, "Requester", "Name, ministry, role and authority, contact details", "Source: role directory (to confirm)"],
    [ico.pin, "Location", "Building, address, floor and area, floor plan", "Source: PRISM Core building data; floor plans in EIMS"],
    [ico.pkg, "Items and proposal", "Items, quantity, recycled or new, specifications, costs, lead time, reservation number", "Source: PRISM; SnapTracker reference"],
    [ico.msg, "Messages and files", "Text, sender, time and linked files for every exchange", "Source: PRISM Requests"],
    [ico.chk, "Approvals and decisions", "Approver, decision, time, evidence, PO number", "Source: PRISM; PO from OneGX/SAP"],
    [ico.act, "Status events", "Who, what and when for every change; feeds follow-up and reporting", "Source: PRISM audit history"],
  ];
  ents.forEach((e, i) => {
    const cx = gx + (i % 3) * (gw + 0.2), cy = ry + Math.floor(i / 3) * (gh + 0.2);
    card(pres, s, cx, cy, gw, gh);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx + 0.14, y: cy + 0.14, w: 0.34, h: 0.34, rectRadius: 0.06, fill: { color: C.blueL }, line: { color: C.blueB, width: 0.5 } });
    s.addImage({ data: e[0], x: cx + 0.2, y: cy + 0.2, w: 0.22, h: 0.22 });
    s.addText(e[1], { x: cx + 0.56, y: cy + 0.14, w: gw - 0.65, h: 0.34, fontFace: FONT, fontSize: 10, bold: true, color: C.ink, margin: 0, valign: "middle", isTextBox: true });
    s.addText(e[2], { x: cx + 0.14, y: cy + 0.56, w: gw - 0.26, h: 0.56, fontFace: FONT, fontSize: 8.5, color: C.ink, margin: 0, valign: "top", isTextBox: true });
    s.addText(e[3], { x: cx + 0.14, y: cy + gh - 0.36, w: gw - 0.26, h: 0.28, fontFace: FONT, fontSize: 7.5, italic: true, color: C.blue, margin: 0, valign: "bottom", isTextBox: true });
  });
  s.addNotes("Use this slide if asked what the work-order record actually holds. Submission creates one record inside PRISM Core, and every other kind of information links to it: the requester, the location, the items and proposal, messages and files, approvals and decisions, and a status event for every change. The status events are what make follow-up and reporting possible without a second compilation. Building details come from PRISM Core building data, which is why the form can prefill them. External systems such as OneGX/SAP and SnapTracker are referenced by fields in Release 1, not connected. The sources marked to confirm depend on GoA decisions, such as who owns the role directory and the building and floor-plan registry.");

  // ---------------------------------------------------------------- A4
  s = frame(pres, {
    label: "A4", title: "From Manual Seams to One Record",
    subtitle: "What the record replaces today, and the controls it must carry forward.",
    sources: "Sources · Team DART systems map (manual seams and preservation register) · GoA discovery sessions",
  });
  const b = { type: "solid", pt: 0.75, color: C.line };
  const seamRows = [
    [{ text: "Today: a manual seam", options: { bold: true, color: C.white, fill: { color: C.blue }, fontSize: 8.5, border: [b, b, b, b] } },
     { text: "", options: { fill: { color: C.blue }, border: [b, b, b, b] } },
     { text: "In the work-order record", options: { bold: true, color: C.white, fill: { color: C.blue }, fontSize: 8.5, border: [b, b, b, b] } }],
  ];
  [
    ["Reservation numbers copied into comment fields", "A reservation number field on the item line"],
    ["PO and WORTS numbers keyed by hand in both directions", "A PO number field, ready to link to OneGX/SAP later"],
    ["Floor plans and drawings passed around as attachments", "A floor plan linked to the location; source to confirm"],
    ["Quotes, photos and invoices sent by email", "Proposals and files kept on the record, with send confirmation"],
    ["No status channel between submission and sign-off", "Status, owner and next action on every request"],
    ["Reports rebuilt by hand in Excel", "Reporting from the record's status history"],
  ].forEach((r) => seamRows.push([
    { text: r[0], options: { color: C.muted, fontSize: 9, fill: { color: C.white }, border: [b, b, b, b] } },
    { text: "→", options: { color: C.blue, bold: true, fontSize: 11, align: "center", fill: { color: C.white }, border: [b, b, b, b] } },
    { text: r[1], options: { color: C.ink, fontSize: 9, fill: { color: C.white }, border: [b, b, b, b] } },
  ]));
  s.addTable(seamRows, { x: X0, y: 1.55, w: 5.6, colW: [2.55, 0.4, 2.65], fontFace: FONT, valign: "middle", margin: [0.05, 0.08, 0.05, 0.08], rowH: 0.457 });
  const kx = X0 + 5.6 + 0.3, kw = X0 + CW - kx, ky = 1.55, kh = 3.2;
  card(pres, s, kx, ky, kw, kh, C.blueL, C.blueB);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: kx + 0.16, y: ky + 0.16, w: 0.34, h: 0.34, rectRadius: 0.06, fill: { color: C.white }, line: { color: C.blueB, width: 0.5 } });
  s.addImage({ data: ico.shield, x: kx + 0.22, y: ky + 0.22, w: 0.22, h: 0.22 });
  s.addText("Controls that carry forward", { x: kx + 0.58, y: ky + 0.16, w: kw - 0.7, h: 0.34, fontFace: FONT, fontSize: 10.5, bold: true, color: C.navy, margin: 0, valign: "middle", isTextBox: true });
  const ctrls = ["Access by role and portfolio", "Approval thresholds as settings, not fixed values", "Full audit history", "Reservation locks against double allocation", "Recycle-first search", "Sealed workflow stages", "Archive, never delete", "Client sign-off and service comments"];
  s.addText(ctrls.map((t, i) => ({ text: t, options: { bullet: { indent: 10 }, breakLine: i < ctrls.length - 1 } })),
    { x: kx + 0.18, y: ky + 0.62, w: kw - 0.32, h: 1.95, fontFace: FONT, fontSize: 9, color: C.ink, paraSpaceAfter: 3, margin: 0, valign: "top", isTextBox: true });
  s.addText("Our systems map found that a replacement without these controls would not be accepted.", { x: kx + 0.18, y: ky + kh - 0.6, w: kw - 0.32, h: 0.46, fontFace: FONT, fontSize: 8, italic: true, color: C.navy, margin: 0, valign: "bottom", isTextBox: true });
  s.addNotes("Use this slide if asked what changes for staff, or why one record matters. Our systems map found eight places where people carry information between systems by hand; six of them are shown here with what the record does instead. The pattern is the same each time: a reference or update that today lives in a comment field, an inbox or a spreadsheet becomes part of the record. The right side matters just as much. WORTS has controls that work, and the record carries them forward: role and portfolio access, approval thresholds as settings, full audit history, reservation locks, recycle-first search, sealed stages, archiving rather than deletion, and client sign-off. A replacement that dropped them would not be accepted.");

  // ---------------------------------------------------------------- A5
  s = frame(pres, {
    label: "A5", title: "Data Flow and Decisions Before Build",
    subtitle: "How request data moves, where Release 1 stops, and what GoA needs to decide.",
    sources: "Sources · MDPM 830 data pipeline · Team DART systems map open questions · SPV working draft §4",
  });
  const stages = [
    ["01", "Generate", "Requesters, coordinators and vendors supply information; the system records events"],
    ["02", "Collect", "Request forms, attachments, case activity and relevant correspondence"],
    ["03", "Keep and shape", "Keep originals, check completeness, link updates, standardize status and dates"],
    ["04", "Store", "One connected work-order record with documents, changes and history"],
    ["05", "Use", "Request visibility, outcome measurement and operational reporting"],
  ];
  const sg = 0.24, sw = (CW - 4 * sg) / 5, sy = 1.55, sh = 1.12;
  stages.forEach((st, i) => {
    const sx = X0 + i * (sw + sg);
    card(pres, s, sx, sy, sw, sh, i === 3 ? C.blueL : C.white, i === 3 ? C.blueB : C.line);
    s.addText([{ text: st[0] + "  ", options: { color: C.blue, bold: true } }, { text: st[1], options: { color: C.ink, bold: true } }],
      { x: sx + 0.12, y: sy + 0.1, w: sw - 0.2, h: 0.26, fontFace: FONT, fontSize: 9.5, margin: 0, valign: "middle", isTextBox: true });
    s.addText(st[2], { x: sx + 0.12, y: sy + 0.4, w: sw - 0.22, h: 0.66, fontFace: FONT, fontSize: 8, color: C.muted, margin: 0, valign: "top", isTextBox: true });
    if (i < 4) s.addImage({ data: ico.arrow, x: sx + sw + 0.04, y: sy + sh / 2 - 0.08, w: 0.16, h: 0.16 });
  });
  // Release 1 boundary card
  const by = sy + sh + 0.25, bh = 4.89 - by;
  const bw = 3.25;
  card(pres, s, X0, by, bw, bh);
  s.addText("Release 1 boundary", { x: X0 + 0.16, y: by + 0.12, w: bw - 0.3, h: 0.26, fontFace: FONT, fontSize: 10.5, bold: true, color: C.navy, margin: 0, isTextBox: true });
  s.addText([
    { text: "In: ", options: { bold: true } }, { text: "the work-order record inside PRISM Core, with building details from PRISM Core data", options: { breakLine: true } },
    { text: "As fields: ", options: { bold: true } }, { text: "PO number and SnapTracker reservation number", options: { breakLine: true } },
    { text: "Later, on a GoA decision: ", options: { bold: true } }, { text: "OneGX/SAP, SnapTracker and EIMS connections", options: { breakLine: true } },
    { text: "Undecided: ", options: { bold: true } }, { text: "WORTS history, none, recent or all" },
  ], { x: X0 + 0.16, y: by + 0.44, w: bw - 0.3, h: bh - 0.54, fontFace: FONT, fontSize: 8.5, color: C.ink, paraSpaceAfter: 4, margin: 0, valign: "top", isTextBox: true });
  // decisions table
  const dx = X0 + bw + 0.3, dw = X0 + CW - dx;
  const dRows = [[
    { text: "Decision needed", options: { bold: true, color: C.white, fill: { color: C.blue }, fontSize: 8.5, border: [b, b, b, b] } },
    { text: "Why it matters", options: { bold: true, color: C.white, fill: { color: C.blue }, fontSize: 8.5, border: [b, b, b, b] } },
  ]];
  [
    ["Request ID format", "Keeps history traceable; today's work orders use work group, fiscal year and facility"],
    ["Status list and meanings", "Follow-up, status and reporting all read from it"],
    ["Owner of building and floor-plan data", "Prefill is only as reliable as its source"],
    ["Duplicate-check rule and retention", "Duplicates resolve without losing history; records are archived, not deleted"],
    ["PRISM notifications and attachments", "Confirms what the platform can configure for Release 1"],
  ].forEach((r) => dRows.push([
    { text: r[0], options: { bold: true, color: C.ink, fontSize: 8.5, fill: { color: C.white }, border: [b, b, b, b] } },
    { text: r[1], options: { color: C.muted, fontSize: 8.5, fill: { color: C.white }, border: [b, b, b, b] } },
  ]));
  s.addTable(dRows, { x: dx, y: by, w: dw, colW: [2.0, dw - 2.0], fontFace: FONT, valign: "middle", margin: [0.04, 0.08, 0.04, 0.08], rowH: 0.3 });
  s.addNotes("Use this slide if asked how the data flows, what Release 1 includes, or what has to be decided before a build. Request information moves through five stages, from the people and events that generate it to the uses it serves; the store stage is the work-order record. Release 1 keeps the record inside PRISM Core and captures references to other systems as fields, and connections to OneGX/SAP, SnapTracker and EIMS come later, only on a GoA decision. Whether WORTS history migrates is still undecided. The decisions on the right are the technical foundations a build needs first: the Request ID format, the status list, the owner of building and floor-plan data, the duplicate and retention rules, and confirmation of what PRISM can configure.");

  await pres.writeFile({ fileName: process.argv[2] });
  console.log("wrote", process.argv[2]);
})();
