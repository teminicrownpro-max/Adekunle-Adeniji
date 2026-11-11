// Team DART · Client presentation, 13 November 2026 · Speaking notes (Word)
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, LevelFormat, ShadingType, BorderStyle, Footer, PageNumber, HeadingLevel,
} = require("docx");

const NAVY = "1F3A5F", TEAL = "0F6E6E", GREY = "5B6470", LIGHT = "F3F5F8", ADE = "E6F2F2", RULE = "C9D1DB";
const WPM = 140;

function runs(text, base = {}) {
  const out = [];
  String(text).split(/(\*\*[^*]+\*\*)/g).forEach((part) => {
    if (!part) return;
    if (part.startsWith("**") && part.endsWith("**")) out.push(new TextRun({ text: part.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: part, ...base }));
  });
  return out;
}
const P = (t, o = {}) => new Paragraph({ children: runs(t, o), spacing: { after: 100 } });
const B = (t) => new Paragraph({ children: runs(t), numbering: { reference: "bul", level: 0 }, spacing: { after: 60 } });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const META = (t) => new Paragraph({ children: runs(t, { color: GREY, size: 19, italics: true }), spacing: { after: 100 } });
const LBL = (t) => new Paragraph({ children: [new TextRun({ text: t.toUpperCase(), bold: true, color: TEAL, size: 18 })], spacing: { before: 100, after: 60 }, keepNext: true });

function BOX(paras, fill) {
  const side = { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 6 };
  const borders = { top: side, bottom: side, right: side, left: { style: BorderStyle.SINGLE, size: 18, color: TEAL, space: 6 } };
  const shade = { type: ShadingType.CLEAR, color: "auto", fill };
  return paras.map((t, i) => new Paragraph({
    children: runs(t, { size: 22 }), shading: shade, border: borders,
    spacing: { after: i === paras.length - 1 ? 220 : 120, line: 300 },
  }));
}
function TABLE(widths, rows) {
  const b = { style: BorderStyle.SINGLE, size: 4, color: RULE };
  return new Table({
    width: { size: widths.reduce((a, c) => a + c, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, ri) => new TableRow({ tableHeader: ri === 0, cantSplit: true, children: r.map((c, ci) => new TableCell({
      width: { size: widths[ci], type: WidthType.DXA }, borders: { top: b, bottom: b, left: b, right: b },
      shading: ri === 0 ? { type: ShadingType.CLEAR, color: "auto", fill: NAVY } : (ri % 2 === 0 ? { type: ShadingType.CLEAR, color: "auto", fill: LIGHT } : undefined),
      margins: { top: 50, bottom: 50, left: 90, right: 90 },
      children: [new Paragraph({ children: runs(c, ri === 0 ? { bold: true, color: "FFFFFF", size: 18 } : { size: 18 }), spacing: { after: 20 } })],
    })) })),
  });
}

const words = (paras) => paras.join(" ").replace(/\*\*/g, "").split(/\s+/).filter(Boolean).length;
const mmss = (sec) => Math.floor(sec / 60) + ":" + String(Math.round(sec % 60)).padStart(2, "0");
const toSec = (t) => { const [m, s] = t.split(":").map(Number); return m * 60 + s; };

// ---------------------------------------------------------------- scripts
const slides = [
  { n: 1, who: "Warren", title: "Intro Page", time: "0:20",
    priority: "Briefly introduce Team DART, PRISM Requests and presentation purpose. Keep opening short.",
    script: ["Thank you for having us. We are Team DART, from Queen's Master of Digital Product Management program. We have worked with you on PRISM Requests, focused on the Furniture request service. Today we share our vision, the prototype, what testing told us, and what we need from you."] },
  { n: 2, who: "Warren", title: "Problem and Context", time: "1:10",
    priority: "Explain WORTS end of life, difficult submissions, limited visibility and fragmented coordination. Use the five stage journey.",
    script: [
      "The Government of Alberta directly manages more than 1,400 facilities, and WORTS has been the only service for requesting maintenance and furniture work. WORTS is end of life, and its replacement is planned before March 2027.",
      "We focused on the Furniture request journey, and the problem runs across five stages. In **Prepare**, requesters are unsure what is required. In **Submit**, a wrong pathway or missing information can send the request back. In **Review**, status and timing are hard to see, so people chase updates. In **Fulfill**, the conversation splits across email, Teams and separate documents. At **Close**, completion is confirmed, but there is little feedback on the service.",
      "The result is difficult submissions, limited visibility and coordination that happens outside the system, so reports are compiled twice. That is why we treat this as a service problem, not only a tool replacement.",
    ] },
  { n: 3, who: "Warren", title: "Users and Jobs to Be Done", time: "0:55",
    priority: "Identify three user groups and their needs. Emphasize CMACs submitting and following requests with less rework.",
    script: [
      "We designed for three user groups. The primary user is the **CMAC or other authorized requester**. Many submit only now and then, so they never become fluent in the system. Their job is simple: understand what is needed, submit a complete request, and have it accepted and fulfilled without rework or repeat follow-up.",
      "The second group is the **Request Coordinators**, who review incoming requests, assign them and follow up missing information. The third is the **Furniture Coordinators**, who fulfil the work and need its record in one place. All three share one need: clear requirements, visible progress and context that survives each handoff.",
      "Anne Marie will now take you through our vision.",
    ] },
  { n: 4, who: "Anne Marie", title: "Product Vision for Furniture Requests", time: "1:05",
    priority: "Present the product vision. Connect guided submission, progress visibility and shared information to user and business needs.",
    script: [
      "Our vision is a Furniture Request Service that is simple to navigate, transparent where it matters and reliable across handoffs, helping Government of Alberta staff deliver and improve the service with greater confidence and accountability.",
      "The product does three things. First, a **guided request experience**, which meets the need for clear submission guidance and reduces avoidable rework. Second, **meaningful progress and next actions**, so requesters know who is responsible and what happens next, and spend less time chasing. Third, **shared request history and operational information**, so context survives each handoff and staff can manage and report from the same information.",
      "It is built on PRISM Core and bounded on purpose: Furniture only. One guardrail holds throughout: governed access, accessibility and auditability stay intact.",
    ] },
  { n: 5, who: "Anne Marie", title: "Business Case: Opportunity and Objectives", time: "0:55",
    priority: "Explain user, business and technology value, with candidate measures rather than claimed benefits.",
    script: [
      "For a government service, the return is avoided effort and added capacity, not revenue. For **users**, that means easier requests, clearer visibility after submission and less follow-up. For the **business**, less avoidable coordination effort, more service capacity and better operational measurement. For **technology**, case data reused for status, ownership and reporting.",
      "We are showing candidate measures, not claimed benefits: fewer requests returned for corrections, less need to chase for updates, less duplicate reporting, and visibility of volume, time open and delivery. Each needs a GoA baseline first, and targets should follow those baselines.",
      "Chochen will now explain why we believe this is viable.",
    ] },
  { n: 6, who: "Chochen", title: "Business Case: Viability", time: "1:00",
    priority: "Explain Real, Win, Worth It priorities, tailwinds and headwinds; scores are Team DART judgments, not financial ROI.",
    script: [
      "We tested viability in two ways. First, we scored seven value opportunities with Real, Win, Worth It, from one to five. These scores are Team DART's judgments from our research, not a financial return on investment. Three form the priority set: easier requests for occasional CMACs at 3.8, clear communication and visibility at 3.9, and operations and reporting at 4.6. Staff capacity, at 4.65, is the outcome we expect, and maintainability with governed access, at 4.2, is a condition we must meet.",
      "Second, tailwinds and headwinds. In our favour: WORTS must be replaced, PRISM Core is the confirmed host and already holds building data, and testers liked the core design. Against us: staff carry information between systems by hand, workflow and data ownership are not settled, and system connections wait on GoA decisions.",
    ] },
  { n: 7, who: "Chochen", title: "Scope, Costs and Timing Boundaries", time: "1:00",
    priority: "Separate proposed scope from exclusions. Note cost drivers and dependencies requiring GOA confirmation.",
    script: [
      "Our proposed scope is the Furniture request lifecycle, from preparing a request to closing it, on PRISM Core: guided submission, status and next steps, communication inside the request, and reporting from the same record.",
      "Outside the current proposal are maintenance requests, direct integrations with systems such as SnapTracker and OneGX/SAP, migration of WORTS history, and the procurement, warehouse and delivery work itself.",
      "The main cost drivers are PRISM configuration, any future integrations, testing and accessibility, training and change management, and ongoing rule and role upkeep. We have not set a budget or schedule, because both depend on you: the budget envelope, the confirmed replacement date, PRISM configuration capacity, and the integration and migration decisions.",
      "This short video shows how the prototype works in practice.",
    ] },
  { n: 8, who: "Video only", title: "Prototype Walkthrough: Submit and Follow Up", time: "3:05", video: true,
    priority: "Play the embedded video showing submission and follow-up.",
    script: [
      "**Cue:** Chochen's last line introduces the video. Start it straight away; it plays within PowerPoint, so check the sound during the dry run.",
      "**After the video:** no recap. Ade starts slide 9 directly with “What you just saw rests on five core requirements.”",
    ] },
  { n: 9, who: "Ade", title: "Core Product Requirements and Data", time: "1:15", ade: true,
    priority: "Explain five key requirements and how a shared work-order record could support status, communication and reporting.",
    script: [
      "What you just saw rests on five core requirements. **First, guided submission:** the form shows what is required and flags missing information before sending. **Second, building details filled in** from data PRISM already holds, so requesters do not retype them. **Third, clear status:** every request shows where it is, who owns it and what happens next. **Fourth, communication inside the request:** messages, updates and approvals stay with the request, not in separate emails. **Fifth, role-based access:** people see only the requests they are permitted to see.",
      "All five depend on **one shared work-order record** with one ID. The requester submits once. Coordinators update the same record, so **status** stays current. Messages and decisions are kept with it, so **communication** has a complete history. And **reports** come from that same record, so nobody compiles them twice.",
      "Today, PO numbers are keyed by hand and reservation IDs sit in comment fields. We would capture them as proper fields, so future system connections have clean keys. Warren will now cover how we keep this design responsible.",
    ] },
  { n: 10, who: "Warren", title: "Responsible Design and Future AI Direction", time: "1:05",
    priority: "Cover access, human decision authority, accountability and reliable data. Core workflow first; AI only if later justified.",
    script: [
      "Good design here must also be responsible design, so we built in four commitments. **Access:** people see what their role allows. Requesters see their progress, while internal notes stay restricted. **Human decision authority:** purchases, approvals and proposals stay with authorized people, and sharing a proposal is clearly not approval. **Accountability:** changes, decisions and messages are recorded and attributed, so the history can be trusted. **Reliable data, used fairly:** service data improves operations; it is not used simply to measure individual staff.",
      "On AI, our assessment is that the immediate problems are better solved by clearer submission, visible status and connected information. So the core workflow comes first. AI could later help summarize request histories or spot missing information, but only with a clear need, reliable data and human oversight.",
      "Felix will now share what testing showed.",
    ] },
  { n: 11, who: "Felix", title: "Usability Findings and Planned Improvements", time: "1:40",
    priority: "Explain six testers, four tasks, aided versus unaided completion, main issues and planned design changes.",
    script: [
      "We ran six remote, moderated sessions between October 21 and 29 with Government of Alberta accommodation and facilities staff. Each person tried four tasks: submit a request, check an earlier request, handle a request that needed more information, and share a quote. Of the 24 attempts, **14 were completed without help and 10 with moderator help**, and the average ease rating was **3.75 out of 5**. Some of that help concerned the test materials rather than the design, so we do not read these numbers as a success rate.",
      "What worked: the guided, uncluttered form, building details filled in automatically, the one-page review, and messages kept inside the request.",
      "We found **four major issues and no critical ones**. Date wording was unclear, so we will label the date required on site and separate requested from confirmed dates. The checklist panel was confusing, so we will separate required actions from guidance. Updates were hard to follow, so each update will name the request and the action needed, and link straight to it. And after sharing a quote, people were unsure it had gone, so we will show a clear confirmation and the next step.",
      "One limit matters: everyone we tested already knew WORTS. Testing with first-time requesters is our next step.",
    ] },
  { n: 12, who: "Naynay", title: "Product Workplan and Roadmap", time: "1:00",
    priority: "Explain concept refinement, operational validation and delivery readiness. Identify GOA input and close.",
    script: [
      "Our plan moves in three stages. **Concept refinement:** we fold the usability findings into the design and finalize the requirements for our final PRD on November 26. **Operational validation:** we retest with first-time requesters and confirm workflow states, ownership and business rules with you. **Delivery readiness:** the foundations a build needs first, which are status meanings, roles and approval authority, master data and the record structure, before core features and any later system connections.",
      "To keep moving, we need your input in five areas: a named owner for the Furniture workflow and its data, introductions to first-time CMACs, confirmation of approval and funding rules, a decision on integrations and WORTS history, and baseline data.",
      "Thank you for your time and support. We are happy to take your questions.",
    ] },
];

// ---------------------------------------------------------------- document
const children = [];
children.push(new Paragraph({ children: [new TextRun({ text: "Team DART · Client Presentation Speaking Notes", bold: true, size: 40, color: NAVY })], spacing: { after: 60 } }));
children.push(new Paragraph({ children: [new TextRun({ text: "PRISM Requests: Furniture Request Service · Government of Alberta · 13 November 2026", size: 26, color: TEAL })], spacing: { after: 60 } }));
children.push(META("Written to the team's Client Presentation Speaking Plan on the Milestone 2 Miro board. Each script is sized to its time slot at about 140 words a minute. Handoff lines are built into the scripts."));

children.push(H2("Timing at a glance"));
let total = 0;
const rows = [["Slide", "Presenter", "Slide title", "Time", "Script"]];
slides.forEach((s) => {
  total += toSec(s.time);
  const w = words(s.script);
  rows.push([String(s.n), s.ade ? "**" + s.who + "**" : s.who, s.ade ? "**" + s.title + "**" : s.title, s.time,
    s.video ? "Video, 3:05" : w + " words, about " + mmss(w / WPM * 60)]);
});
rows.push(["", "", "**Total slide time**", "**" + mmss(total) + "**", "Includes the 3:05 video"]);
rows.push(["", "", "Transition allowance", "0:30", "Speaker handoffs"]);
rows.push(["", "", "**Total presentation**", "**15:00**", "Stay within the 15-minute limit"]);
children.push(TABLE([700, 1500, 3700, 900, 2560], rows));

children.push(LBL("How to use these notes"));
[
  "Speak to the slide, not from it. Bold words are the anchors to remember if you lose your place.",
  "Each script ends with the handoff to the next presenter, so the 0:30 transition allowance stays free.",
  "Figures are taken from the usability report, the DPO evaluation and the scope statement. Say them exactly as written.",
  "Keep claims as candidate measures. Anything not yet confirmed by GoA is presented as a dependency, not a fact.",
].forEach((t) => children.push(B(t)));

slides.forEach((s) => {
  const w = words(s.script);
  children.push(H1("Slide " + s.n + " · " + s.title));
  children.push(META("Presenter: " + s.who + " · Time: " + s.time + (s.video ? "" : " · " + w + " words, about " + mmss(w / WPM * 60) + " at a steady pace")));
  if (s.ade) children.push(new Paragraph({ children: [new TextRun({ text: "ADE'S SLIDE", bold: true, color: TEAL, size: 18 })], shading: { type: ShadingType.CLEAR, color: "auto", fill: ADE }, spacing: { after: 80 } }));
  children.push(P("**Speaking priority:** " + s.priority, { color: GREY, size: 19 }));
  BOX(s.script, s.ade ? ADE : LIGHT).forEach((p) => children.push(p));
});

// Ade's Q&A quick answers
children.push(H1("Ade's quick answers for Q&A"));
children.push(META("Ade holds the evidence, appendix and Q&A role. Short answers, then point to the appendix."));
[
  "**Can PRISM support this?** PRISM Core is the confirmed host and already holds building and asset data. Its capacity to configure the Furniture workflow (statuses, forms, notifications, attachments) is still to confirm with the PRISM team.",
  "**Why no integrations in the first release?** Nothing is connected today, SnapTracker's API is unknown, and the integration path is a GoA decision. We capture PO numbers and reservation IDs as fields now, so later connections have clean keys.",
  "**Will WORTS history move over?** Not in the current proposal. It is your decision: none, recent history only, or all.",
  "**Who can see what?** Access is based on role and portfolio. Requesters see only requests they are permitted to view, and internal notes stay restricted.",
  "**What happens to today's controls?** We keep them: approval thresholds, full audit history, reservation locks, sealed stages and client sign-off.",
  "**Who owns the data?** Not yet decided. That is why a named owner for the workflow and its master data is our first ask.",
].forEach((t) => children.push(B(t)));

const doc = new Document({
  creator: "Team DART", title: "Team DART Client Presentation Speaking Notes",
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Arial", size: 28, bold: true, color: NAVY }, paragraph: { spacing: { before: 280, after: 60 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Arial", size: 24, bold: true, color: NAVY }, paragraph: { spacing: { before: 200, after: 100 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 260 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      new TextRun({ text: "Team DART · Client Presentation Speaking Notes · page ", color: GREY, size: 16 }),
      new TextRun({ children: [PageNumber.CURRENT], color: GREY, size: 16 }),
    ] })] }) },
    children,
  }],
});

slides.forEach((s) => { if (!s.video) { const w = words(s.script); console.log(s.n, s.who, s.time, w, mmss(w / WPM * 60)); } });
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(process.argv[2], buf); console.log("wrote", process.argv[2]); });
