// Team DART · MDPM 900 Strategic Product Vision · Slide Build Sheet v2 (Word)
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, LevelFormat, ShadingType, BorderStyle, Footer, PageNumber,
  HeadingLevel, PageBreak, ExternalHyperlink,
} = require("docx");

const NAVY = "1F3A5F", TEAL = "0F6E6E", GREY = "5B6470", LIGHT = "F3F5F8", ADE = "E6F2F2", RULE = "C9D1DB";
const W = 9360; // content width (Letter, 1 inch margins)

// "**bold**" markers inside strings become bold runs
function runs(text, base = {}) {
  const out = [];
  String(text).split(/(\*\*[^*]+\*\*)/g).forEach((part) => {
    if (!part) return;
    if (part.startsWith("**") && part.endsWith("**")) out.push(new TextRun({ text: part.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: part, ...base }));
  });
  return out;
}
const P = (t, o = {}) => new Paragraph({ children: runs(t, o.run || {}), spacing: { after: 100 }, ...(o.p || {}) });
const B = (t, lvl = 0) => new Paragraph({ children: runs(t), numbering: { reference: "bul", level: lvl }, spacing: { after: 60 } });
const N = (t) => new Paragraph({ children: runs(t), numbering: { reference: "num", level: 0 }, spacing: { after: 60 } });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const LBL = (t) => new Paragraph({ children: [new TextRun({ text: t.toUpperCase(), bold: true, color: TEAL, size: 18 })], spacing: { before: 140, after: 60 }, keepNext: true });
const META = (t) => new Paragraph({ children: runs(t, { color: GREY, size: 19, italics: true }), spacing: { after: 120 } });
const BREAK = () => new Paragraph({ children: [new PageBreak()] });
const RULEP = () => new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RULE, space: 1 } }, spacing: { after: 120 } });

function NOTES(who, paras) {
  const side = { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 6 };
  const borders = { top: side, bottom: side, right: side, left: { style: BorderStyle.SINGLE, size: 18, color: TEAL, space: 6 } };
  const shade = { type: ShadingType.CLEAR, color: "auto", fill: LIGHT };
  const out = [new Paragraph({
    children: [new TextRun({ text: "SPEAKER NOTES · " + who.toUpperCase(), bold: true, color: NAVY, size: 18 })],
    shading: shade, border: borders, spacing: { before: 160, after: 80 }, keepNext: true,
  })];
  paras.forEach((t, i) => out.push(new Paragraph({
    children: runs(t), shading: shade, border: borders,
    spacing: { after: i === paras.length - 1 ? 200 : 100 },
  })));
  return out;
}

function TABLE(widths, rows, opts = {}) {
  const border = { style: BorderStyle.SINGLE, size: 4, color: RULE };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      cantSplit: true,
      children: r.map((c, ci) => new TableCell({
        width: { size: widths[ci], type: WidthType.DXA },
        borders,
        shading: ri === 0 ? { type: ShadingType.CLEAR, color: "auto", fill: NAVY } : (opts.zebra && ri % 2 === 0 ? { type: ShadingType.CLEAR, color: "auto", fill: LIGHT } : undefined),
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: String(c).split("\n").map((line) => new Paragraph({
          children: runs(line, ri === 0 ? { bold: true, color: "FFFFFF", size: 18 } : { size: 18 }),
          spacing: { after: 40 },
        })),
      })),
    })),
  });
}
const GAP = () => new Paragraph({ children: [], spacing: { after: 80 } });

function SLIDE(s) {
  const out = [];
  if (s.pageBreak !== false) out.push(BREAK());
  out.push(H1(s.title));
  out.push(META(s.meta));
  if (s.ade) out.push(new Paragraph({
    children: [new TextRun({ text: "ADE SECTION · filled in full by the Product Architect", bold: true, color: TEAL, size: 18 })],
    shading: { type: ShadingType.CLEAR, color: "auto", fill: ADE }, spacing: { after: 120 },
  }));
  out.push(LBL("1 · Main message"));
  s.main.forEach((t) => out.push(P(t)));
  (s.blocks || []).forEach((b) => {
    out.push(LBL(b.label));
    (b.items || []).forEach((it) => out.push(Array.isArray(it) ? B(it[0], 1) : B(it)));
    if (b.table) { out.push(TABLE(b.table.w, b.table.rows, { zebra: true })); out.push(GAP()); }
    (b.after || []).forEach((it) => out.push(Array.isArray(it) ? B(it[0], 1) : B(it)));
  });
  out.push(LBL("2 · Evidence"));
  s.evidence.forEach((t) => out.push(B(t)));
  out.push(LBL("3 · Visual"));
  s.visual.forEach((t) => out.push(B(t)));
  out.push(LBL("4 · Move to appendix"));
  s.appendix.forEach((t) => out.push(B(t)));
  if (s.confirm && s.confirm.length) { out.push(LBL("To confirm before the slide is final")); s.confirm.forEach((t) => out.push(B(t))); }
  if (s.qa) { out.push(LBL("Reviewer question")); s.qa.forEach((t) => out.push(B(t))); }
  NOTES(s.notesBy, s.notes).forEach((p) => out.push(p));
  return out;
}

// ------------------------------------------------------------------ content
const slides = [
  {
    title: "Slide 1 · Title, team and context",
    meta: "Rubric: Format and Audience · Lead: Anne-Marie (Product Strategist)",
    main: ["Team DART proposes a bounded Furniture Request Service on PRISM to replace the Furniture journey in WORTS."],
    blocks: [{ label: "On the slide", items: [
      "PRISM Requests: Furniture Request Service (working name; product name to confirm)",
      "Strategic Product Vision · Team DART · Queen's MDPM · Government of Alberta · 8 November 2026 (use 13 November 2026 on the client version)",
      "Context line: GoA directly manages more than 1,400 facilities. WORTS is the sole maintenance and furniture request service. It is end of life and planned to be replaced before March 2027.",
      "Team: Anne-Marie, Product Strategist · Adekunle, Product Architect · Warren, AI Steward · Fuyang, Product Designer · Mmenyene, Project Manager · Qiuchen, Product Enablement Lead",
    ] }],
    evidence: [
      "DPO deck (4 September 2026), Initial Problem Statement: 1,400+ facilities; WORTS sole service, end of life.",
      "GoA Capstone Scope Statement, recorded as confirmed facts on the systems map board: replacement planned before March 2027; PRISM Requests is the proposed replacement.",
    ],
    visual: ["Title, one context line and a row of six role names. Use the GoA logo and colours (Session 17 checklist)."],
    appendix: ["Nothing. Keep the slide light."],
    confirm: ["Product name for client-facing material.", "Whether to show the March 2027 date (PM decision, see slide 7)."],
    notesBy: "Anne-Marie",
    notes: ["We are Team DART. The Government of Alberta directly manages more than 1,400 facilities, and WORTS is the only service for requesting maintenance and furniture work. WORTS is end of life, and its replacement is planned before March 2027. We focused on one bounded part of that problem: the Furniture request journey. Today we show what we would build, why it is worth building, what we tested, and what we need from you to move forward."],
  },
  {
    title: "Slide 2 · The problem: from replacing a tool to improving the service",
    meta: "Rubric: Product Vision (a clear description of the problem) · Lead: Anne-Marie",
    main: ["The problem is the Furniture service, not only the tool. Requesters cannot see what is needed or what happens next, and staff coordinate outside the system."],
    blocks: [{ label: "On the slide", items: [
      "**Problem statement:** CMACs and other authorized requesters need a clearer and easier way to submit and follow Furniture requests, while Infrastructure staff need connected request information that supports both day-to-day service management and reporting.",
      "**Where the pain sits:**",
      ["Prepare: uncertainty about requirements"],
      ["Submit: a wrong pathway or missing information can trigger rework"],
      ["Review: status and timing are hard to see"],
      ["Fulfill: the conversation fragments across channels"],
      ["Close: closure is confirmed, but feedback on the service is limited"],
      "**The shift:** replacing a tool → improving the Furniture service · intake only → the full submit, follow and manage lifecycle · isolated records → connected information that also supports reporting",
    ] }],
    evidence: [
      "DPO deck: user journey, revised problem statement and From → To reframing.",
      "Systems map F2: eight manual seams where people carry information between systems by hand.",
    ],
    visual: ["A five-stage journey strip with the pain under each stage, and the three-row From → To reframing beside it."],
    appendix: ["Full journey table (DPO Appendix C) and the systems map F2 excerpt."],
    notesBy: "Anne-Marie",
    notes: ["We started by asking how to replace a tool. The evidence pointed to a service problem. Requesters are unsure what to submit, then cannot see what is happening after they submit. Staff fill the gaps by email and Teams, and that work often never returns to the record, so reporting is compiled twice. Our scope is the whole Furniture lifecycle, from preparing a request to closing it."],
  },
  {
    title: "Slide 3 · Users and the job to be done",
    meta: "Rubric: Product Vision (whom we solve the problem for) · Leads: Fuyang, Qiuchen",
    main: ["We design first for the occasional CMAC, who submits now and then and does not build fluency with the system."],
    blocks: [{ label: "On the slide", items: [
      "**Primary: occasional CMAC or other authorized requester.** Unsure what is required, cannot see status or timing after submitting, and chases updates.",
      "**Supporting: Request Coordinator (FRC).** Reviews incoming requests, assigns Furniture Coordinators and follows up missing information. Role definition to confirm with GoA.",
      "**Supporting: Furniture Coordinator (FC).** Coordinates fulfilment with the CMAC and vendor. The record of work lives outside the system, and reports are compiled twice.",
      "**Job to be done:** an occasional or authorized CMAC needs to understand requirements and submit a complete Furniture request, so it can be accepted and fulfilled without avoidable rework or repeat follow-up.",
      "**Strongest JTBD themes:** simplifies, informs, avoids hassles, connects.",
    ] }],
    evidence: [
      "GoA-supplied interviews, JTBD analysis (DPO Appendices A and B), MDPM 883 user characterization and personas.",
      "MDPM 826 usability test: six GoA accommodation and facilities staff, all with WORTS experience; two of them submit requests only occasionally.",
    ],
    visual: ["Three persona cards with the primary card larger, and the JTBD statement as a banner underneath."],
    appendix: ["Full persona table (pains, gains, evidence source) and the JTBD analysis."],
    confirm: ["Mark the Request Coordinator card “to validate”.", "First-time CMACs are not yet tested; say so on the slide."],
    notesBy: "Fuyang or Qiuchen",
    notes: ["Our primary user is the occasional CMAC. They submit a Furniture request now and then, so they never become fluent in the system. Their job is simple: get a complete request accepted without being sent back. Two staff roles support them: the coordinator who reviews and assigns requests, and the Furniture Coordinator who fulfils them. Everyone we tested with already knew WORTS, and two of the six submit only occasionally. Testing with first-time CMACs is our most important next step."],
  },
  {
    title: "Slide 4 · Vision and product concept",
    meta: "Rubric: Product Vision · Lead: Anne-Marie",
    main: ["Vision (as on the team's Vision Board): “Enable a Furniture Request Service that is simple to navigate, transparent where it matters and reliable across handoffs, helping Government of Alberta staff deliver and improve the service with greater confidence and accountability.”"],
    blocks: [{ label: "On the slide (Product Vision Board)", items: [
      "**Target group:** CMACs and authorized requesters (primary); Infrastructure Furniture Request processing staff; coordination staff; Infrastructure management (business stakeholders).",
      "**Needs:** clear submission guidance; meaningful progress visibility; knowing who is responsible and what happens next; reliable context during handoffs.",
      "**Product:** PRISM Requests, Furniture Request Service: a guided request experience; meaningful progress and next actions; relevant request history and operational information.",
      "**Business goals:** reduce avoidable submission rework; reduce unnecessary follow-up effort; increase productivity; streamline processes; improve coordination and accountability.",
      "**Guardrail:** preserve governed access, accessibility and auditability.",
    ] }],
    evidence: [
      "Vision Board, Target Group, Needs, Product and Business Goals frames on the Milestone 2 Miro board.",
      "DPO evaluation, JTBD themes and the usability test.",
    ],
    visual: ["The five-box Product Vision Board (Session 17 format), with the vision statement across the top."],
    appendix: ["Elevator pitch, and today's alternatives from the Vision Board: WORTS; email and Teams coordination; separate documents and manual workarounds."],
    confirm: [
      "Use one vision wording everywhere. The Vision Board says “helping Government of Alberta staff”; the earlier build sheet says “so Government of Alberta requesters and Infrastructure staff can”. Agree one.",
      "Say “built on PRISM Core, the confirmed host platform”. Whether PRISM can be configured for the Furniture workflow is still to confirm (slide 6).",
    ],
    notesBy: "Anne-Marie",
    notes: ["This is our vision on one page. For the occasional CMAC, the service makes clear what is needed and what happens next. For staff, it keeps the conversation and the record in one place, so the same information supports daily work and reporting. It is bounded on purpose: Furniture only, built on PRISM. The guardrail matters as much as the goals: governed access, accessibility and auditability must stay intact."],
  },
  {
    title: "Slide 5 · Business opportunity and OKRs",
    meta: "Rubric: Business Case (opportunity) · Lead: Anne-Marie",
    main: ["For a government service, the return is avoided effort and added capacity, not revenue. We measure it from the same case data the service creates."],
    blocks: [{ label: "On the slide", items: [
      "**User value:** easier requests for CMACs and other authorized requesters; clearer visibility after submission; less follow-up and uncertainty.",
      "**Business value:** less avoidable coordination effort; more service capacity; better operational measurement.",
      "**Technology value:** reuse existing case data; shared status and ownership; reporting from the same information.",
    ], table: { w: [2200, 4360, 2800], rows: [
      ["Objective", "Key results", "Baseline and target"],
      ["**User:** make Furniture requests easier to understand, complete and follow", "Fewer requests returned for avoidable corrections · clearer status and next-step understanding · less need to chase someone for an update", "Baseline: GoA data needed. Prototype evidence only: 14 of 24 test attempts unaided"],
      ["**Business:** reduce avoidable coordination effort while improving service management and reporting", "Less manual status follow-up · less duplicate reporting compilation · better visibility of volume, time open and delivery", "Baseline: GoA data needed"],
      ["**Technology:** keep request information usable across submission, status, operations and reporting", "Case status and ownership stay current · the same case data supports daily work and reporting · governed access and auditability preserved", "Baseline: GoA data needed. Guardrail, not a growth target"],
    ] }, after: ["Every target is set after the GoA baseline and CMAC validation (DPO)."] }],
    evidence: [
      "DPO: Identifying Value Opportunities, and Objectives and Key Results; service KPIs suggested by the GoA sponsor.",
      "Value opportunity evaluation: Staff capacity is the outcome opportunity (Real, Win, Worth It overall 4.65 of 5).",
      "MDPM 826 report for the 14 of 24 figure, which the report says is not a confirmed success rate.",
    ],
    visual: ["The three-row OKR table. Show “GoA data needed” tags, not invented numbers."],
    appendix: ["Benefit logic and the GoA inputs it needs: requests per year × follow-up touches avoided × minutes per touch × loaded hourly rate."],
    confirm: ["All baselines: volumes, staff time per request, return and rework rates, reporting hours (systems map open question Q-12)."],
    notesBy: "Anne-Marie",
    notes: ["There is no revenue here. The value is the time people stop spending on chasing, rework and rebuilding reports, and the capacity that frees. We set three objectives, for users, for the business and for technology. We only show numbers we have. In testing, 14 of 24 task attempts were completed without help, but that is prototype evidence, not a baseline. Every baseline and target needs GoA data first, and we would rather show that gap than fill it with guesses."],
  },
  {
    ade: true,
    title: "Slide 6 · Product viability: technical tailwinds and headwinds",
    meta: "Rubric: Business Case (viability) · Leads: Adekunle (technical tailwinds and headwinds); Mmenyene (risks)",
    main: [
      "GoA can deliver this as a bounded Furniture service on PRISM Core. Viability depends on three GoA decisions: who owns the workflow and master data, which rules apply, and when other systems connect.",
      "**Slide title (the insight):** The friction sits between systems, not inside WORTS. One shared record comes first; connections follow.",
    ],
    blocks: [
      { label: "On the slide · Tailwinds", items: [
        "**Clear mandate.** WORTS is end of life. The GoA Capstone Scope Statement plans its replacement before March 2027 and names PRISM Requests as the replacement.",
        "**Confirmed host.** PRISM Requests will run as a microservice on PRISM Core, which already holds building and asset data. That makes building auto-fill realistic.",
        "**One clean identifier today.** The shared building ID already links requests to building data.",
        "**GoA backs the highest-value seam.** In Demo 3 (2 April 2026, single session), GoA's modernization team named the reservation-to-work-order seam the highest-value opportunity.",
        "**Mapped landscape.** The main systems each have a recorded disposition: replace, integrate, retain or awaiting a GoA decision.",
        "**Core pattern tested.** 24 recorded task attempts: 14 unaided, 10 with help; mean ease 3.75 of 5. The guided form and auto-filled building details were the most liked features.",
      ] },
      { label: "On the slide · Headwinds", items: [
        "**People are the integration layer.** Eight manual seams: reservation IDs copied into comment fields; PO and WORTS numbers keyed by hand in both directions; floor plans and drawings sent as attachments; quotes, photos and invoices sent by email; closure bundles assembled by hand; warehouse receiving by visual identification; no status channel between submission and sign-off; reports rebuilt in Excel.",
        "**Nothing is connected, and key decisions are open.** SnapTracker and BLIMS/EAMS await a GoA decision. Whether SnapTracker exposes an API is unknown.",
        "**SnapTracker is queued behind other work.** In Demo 3 (single session) it sat behind data and financial migrations and a floor-plan handoff, roughly three to six months out. That window has passed, so a current date is needed.",
        "**Governance gaps.** Process ownership is not consistently defined, data stewardship is unassigned, naming standards differ across systems, and ownership of the master asset registry is unresolved.",
        "**Rules not yet agreed.** Status meanings, the duplicate-check rule and retention.",
        "**Legacy dependency.** CGI maintains WORTS on ColdFusion, so platform knowledge may be lost during the transition.",
        "**Foundations before AI.** The team's AI assessment recommends no AI in the initial workflow.",
      ] },
      { label: "On the slide · Top risks (Mmenyene; ratings to confirm by the PM)", table: { w: [3900, 1700, 3760], rows: [
        ["Risk", "Likelihood / impact", "Mitigation"],
        ["Workflow ownership and master data not settled", "High / High", "Escalate to GoA as an explicit dependency (ask 1, slide 12)"],
        ["CMAC validation does not support our framing", "Medium / High", "Treat the first-time CMAC retest as the next checkpoint"],
        ["PRISM capability is less than assumed", "Medium / High", "Architect to confirm configuration capacity with the PRISM team"],
        ["No access to first-time users", "Medium / Medium", "Secure introductions early through the GoA sponsor"],
      ] } },
    ],
    evidence: [
      "Systems map board: F2 (eight seams, system dispositions, shared building ID, PRISM Core as host, CGI and ColdFusion); F6 (governance gaps, confirmed); frame 6 (Demo 3, 2 April 2026); F9 open questions Q-03, Q-05 and Q-11.",
      "GoA Capstone Scope Statement (March 2027; PRISM Requests).",
      "MDPM 826 usability report; AI Steward input to the Strategic Product Vision; MDPM 830 data pipeline headwinds and tailwinds.",
      "DPO Real, Win, Worth It scores (1 to 5): Staff capacity 4.65 (outcome); Operations and reporting 4.6; Maintainability and governed access 4.2 (condition); Connected Furniture journey 2.6 (lowest).",
    ],
    visual: [
      "Two columns, tailwinds and headwinds, with short lines and icons only.",
      "Callout: “8 manual seams today → 1 shared record”.",
      "The four risks as a likelihood and impact strip underneath.",
    ],
    appendix: [
      "Systems map F2 with all eight seams labelled, and the disposition table.",
      "Demo 3 critical review (frame 6) and the full Real, Win, Worth It table.",
      "Full risk register.",
    ],
    confirm: [
      "A current SnapTracker integration date, and whether SnapTracker has an API (Q-05, Product Architect).",
      "PRISM Core configuration capacity for the Furniture workflow: statuses, forms, notifications, attachments.",
      "Risk ratings (PM).",
    ],
    qa: ["**“Which headwind is the biggest risk?”** Workflow ownership and master data. Status meanings, access rules and reporting all depend on it. The biggest technical unknown is whether PRISM Core can be configured for the Furniture workflow: it is confirmed as the host, not yet for this configuration."],
    notesBy: "Adekunle",
    notes: [
      "Can GoA actually deliver this? We think yes, with conditions. The platform question is largely settled. PRISM Requests will run as a microservice on PRISM Core, which already holds building and asset data. So filling in the building for the requester is realistic, and it was the feature our testers liked most.",
      "When we mapped the system, the main friction was between systems, not inside WORTS. Staff copy reservation IDs into comment fields, key PO numbers by hand in both directions, and rebuild reports in Excel. People are the integration layer. None of these systems is connected today, SnapTracker work was queued behind other migrations, and we still need a current date and an answer on whether it has an API.",
      "So we do not lead with integrations. We lead with one shared record that captures these references properly, as data, and systems connect later, once GoA decides. The biggest risk is not the technology. It is who owns the workflow and the master data, because status rules, access and reporting all depend on that decision.",
    ],
  },
  {
    title: "Slide 7 · Boundary conditions: cost and time",
    meta: "Rubric: Business Case (boundary conditions) · Lead: Mmenyene · Ade sizes integration and migration",
    main: ["(PM draft, kept) We have identified the main cost drivers. We cannot responsibly commit to a budget or schedule until GoA confirms its constraints."],
    blocks: [
      { label: "On the slide · Cost drivers", items: [
        "Build and PRISM configuration: workflow, forms, status model",
        "System integrations: depend on the path GoA chooses (architect input below)",
        "WORTS data migration: not in the current proposal; cost depends on the option chosen",
        "Testing and accessibility",
        "Training, change management and ongoing support",
        "Data quality and governance (Vision Board cost factor)",
        "Run and maintain, yearly: rule, role and authority upkeep. Show it apart from one-off costs.",
        "Budget envelope: not confirmed",
      ] },
      { label: "On the slide · Time drivers", items: [
        "WORTS replacement: planned before March 2027 (GoA Capstone Scope Statement); confirm the current date",
        "PRISM configuration effort: to assess with the PRISM team",
        "SnapTracker integration: queued behind concurrent migrations; the April 2026 estimate has lapsed",
        "Testing and adoption preparation: required before go-live",
        "Delivery timeframe: not confirmed",
      ] },
      { label: "Architect input (Ade) · integration and migration options", items: [
        "**Release 1, we suggest: no direct integrations.** Staff record the PO number and SnapTracker reservation ID as structured fields. This keeps integration cost out of Release 1 and matches the MDPM 830 scope boundary.",
        "**Later, on a GoA decision:** connections to OneGX/SAP (PR, PO), SnapTracker (reservations) and EIMS (floor plans and drawings). Sized from a PRISM team estimate once GoA picks the path and the SnapTracker API question is answered.",
        "**WORTS history:** a GoA decision with three options: none, recent history only, or all history. Each option changes cost and the legacy fields the data model must hold.",
      ] },
    ],
    evidence: ["Working document §3.3; Vision Board cost factors; systems map F2 and frame 6; MDPM 830 scope boundary (direct integrations and WORTS migration are outside the current proposal)."],
    visual: ["Two columns, cost and time, each ending in a “Not confirmed” tag, plus a small three-option strip for integration and migration."],
    appendix: ["Cost table with an “Estimate: to confirm with GoA” column and the basis for each category."],
    confirm: [
      "**Flag for the PM:** the draft shows the WORTS end-of-life date as “Unconfirmed”. The GoA Capstone Scope Statement plans replacement before March 2027, and the planning board records it as a confirmed fact. Show it with its source, or say why we are not relying on it.",
      "Title typo in the draft: “Boundary Conditions”, not “Boundaries Conditions”.",
    ],
    notesBy: "Mmenyene, with Adekunle on integration",
    notes: ["We know what drives the cost. We do not yet know the budget, so we will not invent one. Integration is the most variable cost, so we kept it out of the first release. Staff record the key references in structured fields, and system connections come later, once GoA chooses a path. Migration works the same way: it is your decision, and we have set out three options. On time, the scope statement plans the replacement before March 2027, and we ask GoA to confirm that date before we plan against it."],
  },
  {
    title: "Slide 8 · Prototype video and guiding scenarios",
    meta: "Rubric: Product Design (prototype design, scenarios) · Lead: Fuyang (Product Designer)",
    main: ["Guide the request before it is submitted, then make next steps, ownership and progress easy to read. The three-minute video shows this through two guiding scenarios."],
    blocks: [{ label: "On the slide", items: [
      "**Video (3 minutes),** embedded so it plays within PowerPoint.",
      "**Scenario 1, submit and follow (usability tasks 1 and 2):** the requester completes the four-step guided form (request type, request details, attachments, review and submit) with building details filled in, receives a reference number, then checks status, owner and next step.",
      "**Scenario 2, act and share (tasks 3 and 4):** the requester sees an Action Required update, replies inside the request, then shares the Furniture Coordinator's proposal with the client and sees that client approval is still pending.",
      "**Design rationale:** less uncertainty at preparation and submission; visible status builds trust; one record keeps coordination and reporting together.",
      "**In scope:** guided submission and review; status, owner and next step; messaging, quotes and approvals inside the request; operational reporting from the same record; governed access and audit.",
      "**Out of scope or later:** maintenance requests; AI features; procurement process redesign; direct system integrations; historical WORTS migration.",
      "**Label:** the prototype uses fictional names, facilities, costs and dates.",
    ] }],
    evidence: [
      "MDPM 883 scenarios and task model; MDPM 826 test plan (“What participants will see”) and report.",
      "Prototype: https://worts2-self-guided.vercel.app/#/tasks",
    ],
    visual: ["Video timeline: 0:00 to 0:30 problem and users; 0:30 to 1:40 scenario 1; 1:40 to 2:30 scenario 2; 2:30 to 3:00 rationale and what testing changed. Add an in-scope and out-of-scope strip."],
    appendix: ["MoSCoW backlog with release mapping; video script; prototype link."],
    confirm: [
      "The tested prototype had no coordinator or staff screens, so tasks 3 and 4 were done as the requester. If the video shows a coordinator view, label it as a later design that was not tested.",
      "Check the scenario wording against the refined prototype at the link above before the dry run.",
    ],
    notesBy: "Fuyang",
    notes: ["The video shows both scenarios. In the first, a requester prepares and submits a request through a guided four-step form, with the building details filled in, then checks status, owner and next step. In the second, the requester answers a request for information inside the request and shares a furniture proposal with their client, with a clear note that approval is still pending. The design guides the request before it is submitted and keeps everything after submission in one place. All names, costs and dates in the prototype are fictional."],
  },
  {
    ade: true,
    title: "Slide 9 · Requirements, data and architecture",
    meta: "Rubric: Product Design (requirements) · Leads: Adekunle (architecture, data, non-functional guardrails); Fuyang (functional requirements); Warren (ethics guardrails)",
    main: ["One Furniture Request record, keyed by one Request ID, lives inside PRISM Core. Information is captured once and reused for status, coordination and reporting, while governed access and audit history stay intact."],
    blocks: [
      { label: "On the slide · Architecture (Release 1, we suggest)", items: [
        "**Core:** PRISM Requests as a microservice on PRISM Core. PRISM Core building and asset data fills in the location.",
        "**Three user groups, one record:** CMACs and authorized requesters; Request Coordinators; Furniture Coordinators and management.",
        "**Notifications:** email notifications that open the right request (PRISM capability to confirm).",
        "**Later, on a GoA decision:** OneGX/SAP (PR, PO), SnapTracker (recycled stock and reservations), EIMS (floor plans and drawings).",
        "**Outside the product:** maintenance requests; other PRISM Core services; procurement, warehouse, installation and delivery work (the product may show their status); a vendor-facing workflow; historical WORTS migration.",
      ] },
      { label: "On the slide · Data model", items: [
        "**Core record:** the Furniture Request (case), keyed by Request ID.",
        "**Linked:** requester and requesting ministry; location (building code, address, floor and area, floor plan); furniture items and quote; attachments; messages and interaction history; approvals and decisions; status history with timestamps and owner; fulfilment and closure (scheduled event, PO reference, fulfilment date, closure confirmation, issue report).",
        "**Request ID:** we suggest mirroring today's work-order identity of work group, fiscal year and facility ID (Demo 3, screen-verified). Format to confirm.",
        "**New structured fields:** PO number, SnapTracker reservation ID and building ID. Today the PO number is keyed by hand and the reservation ID survives only as free text in a comment field.",
        "**Data principles:** capture once · keep the original and record corrections · link every update and document to the Request ID · define each status and its owner · report from the same record · give master data a named owner.",
      ] },
      { label: "On the slide · Guardrails (non-functional: Ade · ethics: Warren)", items: [
        "**Access:** role and portfolio based. Requesters see only requests they are permitted to view; internal notes stay restricted.",
        "**Authority:** approval thresholds are settings, not fixed values, because they vary by workgroup. People approve purchases and proposals; sharing a proposal is not approval.",
        "**Audit:** full history of creator, approver, assignee, timestamps, comments, attachments, status and sign-off. Completed stages are sealed.",
        "**Retention:** records are archived, never deleted, for the period GoA records requirements set (schedule to confirm).",
        "**Accessibility and design:** GoA design system; accessibility standard to confirm with GoA; supported modern browsers on desktop and mobile.",
        "**Maintainability:** rules, roles and thresholds can change without redevelopment.",
        "**Responsible reporting:** reports describe the service, not individual staff.",
      ] },
      { label: "On the slide · Top “Must” requirements (Fuyang), as one strip", items: [
        "Guided form with a one-page review that flags missing information · building details filled in with a visible cue · status with owner, next step and clear dates · messages and updates kept inside the request · proposal shared from the request with a clear confirmation · role-based access with approvals recorded · reporting from the same record",
      ] },
      { label: "On the slide · What must survive replacement", items: [
        "Role and portfolio access, authorization thresholds, full audit history, reservation locks that stop recycled stock being allocated twice, recycle-first search, sealed stages, unique-identifier traceability, archive-never-delete and client sign-off. The systems map warns that dropping these controls would get the product rejected.",
      ] },
    ],
    evidence: [
      "MDPM 883 requirements, mandated constraints (fit within PRISM Core; respect existing GoA roles, approvals and access rules) and data dictionary.",
      "MDPM 830 data pipeline: scope boundary, clean-data rules, controls, gaps and leaks.",
      "Systems map: F2 (PRISM Core, seams SM1 and SM2, shared building ID); F6 (preservation register, claim IC-5); frame 6 (work-order identity).",
      "MDPM 826 usability report; MDPM 850 ethical context analysis.",
    ],
    visual: [
      "Architecture diagram in the centre: the Request record inside PRISM Core; the three user groups on the left; OneGX/SAP, SnapTracker and EIMS on the right in dashed boxes marked “later, on a GoA decision”.",
      "A narrow side panel for the data model and the Must strip.",
    ],
    appendix: [
      "Full functional and non-functional requirement tables, with one agreed numbering.",
      "Data dictionary and entity table; the MDPM 830 data pipeline with controls at each hand-off; the preservation register; the ethics table.",
    ],
    confirm: [
      "Request ID format; the status list and meanings; the duplicate-check rule; retention schedule; accessibility standard.",
      "PRISM notification and attachment capability (PRISM team).",
      "The owner and source of master data for buildings and floor plans (Q-11).",
      "Keep requirement numbers off the slide until the PRD and MDPM 883 numbering are reconciled.",
    ],
    notesBy: "Adekunle, then Fuyang and Warren",
    notes: [
      "This is how the product works underneath. Everything hangs off one record per request, inside PRISM Core. The CMAC submits once, coordinators work in the same record, and reports come from it, so nobody compiles anything twice. PRISM Core already holds building data, which is why the building can be filled in for the requester.",
      "Today, PO numbers are keyed by hand and reservation IDs sit as free text in comment fields. We make them proper fields now, so whichever connections GoA chooses later have clean keys to connect to. Release 1 needs no direct integrations, which keeps cost and risk down.",
      "Some controls must survive the move: role-based access, approval thresholds, full audit history, reservation locks and sealed stages. The systems map shows that dropping them would get the product rejected, so we design them in from the start. Fuyang will now cover the top requirements, and Warren the ethics guardrails.",
    ],
  },
  {
    title: "Slide 10 · Product evaluation and changes",
    meta: "Rubric: Product Evaluation and Changes (emerging tech, ethics, system) · Leads: Fuyang (usability); Warren (ethics, emerging technology); Adekunle (systems map)",
    main: ["Testing confirmed the core pattern and set four major fixes. Ethics, emerging technology and the systems map each changed the design."],
    blocks: [
      { label: "On the slide · Usability (MDPM 826)", items: [
        "Six remote moderated sessions, 21 to 29 October 2026, with GoA accommodation and facilities staff, all experienced with WORTS.",
        "24 recorded task attempts: 14 unaided, 10 with moderator help. Mean ease 3.75 of 5.",
      ], table: { w: [3360, 1800, 1800, 2400], rows: [
        ["Task", "Unaided", "With help", "Mean ease (of 5)"],
        ["1 · Submit a request", "2", "4", "4.00"],
        ["2 · Check progress", "4", "2", "3.83"],
        ["3 · Handle a blocked request", "4", "2", "3.67"],
        ["4 · Share a quote", "4", "2", "3.50"],
      ] }, after: [
        "**Keep:** the guided, uncluttered form; auto-filled building details; the one-page review; messages kept inside the request.",
        "**Four major issues → changes (no critical issues):**",
        ["Date and timing wording unclear (disliked by 4 of 6) → “Date required on site”; requested, suggested and confirmed dates kept apart"],
        ["Checklist panel unclear (3 of 6) → required actions separated from guidance and linked to fields"],
        ["Request updates hard to follow (2 of 6 lost the request or needed extra effort) → update wording with the request number and required action, linked to the request"],
        ["Share confirmation unclear → confirmation naming the recipient, date and decision status, plus the next step"],
        "**Eight minor issues,** including hard-to-read status dates, an unclear stage owner and inconsistent labels.",
        "**Limits:** no first-time requesters; small sample; fictional data; some help concerned the test materials, so 14 of 24 is not a success rate; one task 3 outcome is still to confirm.",
      ] },
      { label: "On the slide · Ethics (MDPM 850) → changes", items: [
        "Collect only what is needed and restrict access by role.",
        "Show requesters their progress, but keep internal notes restricted.",
        "Make clear that sharing a proposal is not approval.",
        "Report at service level, with no individual staff ranking by default.",
        "Keep purchasing and proposal decisions with authorized people.",
      ] },
      { label: "On the slide · Emerging technology (MDPM 822) → change", items: [
        "No AI in the initial workflow. Build the data and process foundations first.",
        "Revisit AI only with a clear business need, reliable data and evidence that it adds value beyond simpler options. Possible later uses: summarizing request histories and spotting missing or inconsistent information.",
      ] },
      { label: "On the slide · Systems map (MMIE 884, Ade) → changes", items: [
        "Capture references as structured fields instead of free text.",
        "Design in the controls that must survive replacement.",
        "Do not remove a step until we know what it does: the reservation-to-work-order conversion step could not be explained even by the person who performs it.",
      ] },
    ],
    evidence: [
      "MDPM 826 usability report (issues I1 to I12, hypotheses SH1 to SH5).",
      "Ethical Context Analysis (Warren and Ade) on the Milestone 2 board; AI Steward input to the Strategic Product Vision.",
      "Systems map F2, F6 and frame 6.",
    ],
    visual: [
      "Four rows: source → what we learned → what changed.",
      "A small unaided versus with-help bar for each task.",
    ],
    appendix: [
      "Full usability report: twelve issues with severity, hypotheses (SH1 to SH4 partly supported, SH5 not observed), results by participant.",
      "Full ethics table and the MDPM 822 technology options comparison.",
    ],
    notesBy: "Fuyang, Warren and Adekunle",
    notes: [
      "In testing, six participants worked through all four tasks, and 14 of the 24 attempts needed no help. Submitting a request needed the most help but was rated the easiest, which in our reading suggests the form works once people understand what is required. We found four major issues and no critical ones, and each now has a design change.",
      "The ethics scan shaped what each role can see and made clear that sharing a proposal is not approval. Our technology assessment found no case for AI in the first release, so we build the foundations first. The systems map changed the data design: references become structured fields, and the controls GoA relies on are kept. The real test is still a first-time CMAC.",
    ],
  },
  {
    title: "Slide 11 · Product workplan and roadmap",
    meta: "Rubric: Product Workplan (plan of action) · Lead: Mmenyene · Ade adds technical dependencies",
    main: ["(PM draft, kept) The product moves in phases. Validation and foundational decisions come before implementation, and core capabilities come before enhancements."],
    blocks: [
      { label: "On the slide · What Team DART controls", items: [
        "**1 · Finalize the vision:** fold in the usability findings and the four major fixes. Milestones: Strategic Product Vision submitted 8 November 2026; client presentation 13 November 2026.",
        "**2 · Validate:** retest with first-time CMACs and confirm workflow states and ownership. The date depends on GoA introductions.",
        "**3 · Refine:** update requirements, data model, measures and the ethics scan. Milestone: final PRD 26 November 2026.",
      ] },
      { label: "On the slide · Potential GoA implementation path", items: [
        "**Foundation:** workflow, data, ownership, governance",
        "**Core submit and follow:** guided form, building auto-fill, status, messaging (Release 1)",
        "**Reporting:** operational reporting from the same record (Release 1 or 2, to decide)",
        "**Integrate, conditional:** OneGX/SAP, then SnapTracker, then EIMS; gated on a GoA decision and the SnapTracker API answer",
        "**Enhancements:** approvals inside the system, contextual help, alerts and feedback at close (later releases)",
      ] },
      { label: "Architect input (Ade)", items: [
        "**What Foundation must deliver technically:** the status model and its meanings; the Request ID scheme; the role and authority model; the source and owner of master data for buildings and floor plans; the retention rule. Core cannot start until these are agreed.",
        "**Add to dependencies:** PRISM Core configuration capacity (including notifications and attachments); SnapTracker API availability; a named owner for the building registry.",
      ] },
      { label: "On the slide · Dependencies", items: [
        "First-time CMAC access · workflow and master-data ownership · PRISM feasibility for the Furniture configuration · GoA implementation resources and funding · GoA baselines",
      ] },
    ],
    evidence: ["Working document §4; Milestone 2 integrated work plan; MDPM 822 (foundations before AI); systems map frame 6 (SnapTracker sequencing)."],
    visual: ["A horizontal roadmap: three capstone phases, then the GoA phases, with gates as diamonds. Show only the dates we control: 8, 13 and 26 November 2026."],
    appendix: ["Horizon table with owners, full risk register and the MoSCoW backlog."],
    confirm: ["Release numbers for the GoA path are our suggestion; GoA owns that plan."],
    notesBy: "Mmenyene",
    notes: ["We separate what we control from what GoA controls. Our next steps are clear: make the four major fixes, retest with first-time CMACs, and refine the requirements for the final PRD on 26 November. After that, a GoA build would start with foundations: status meanings, ownership, roles and master data. Only then come the core request flow, reporting and enhancements. System connections are a conditional phase, gated on your decision. The only dates we show are the ones we own."],
  },
  {
    title: "Slide 12 · What we need from GoA",
    meta: "Rubric: Product Workplan and Business Case (adoption conditions) · Leads: Qiuchen, Mmenyene · close by Anne-Marie",
    main: ["GoA decisions now set the pace. The first two, a named workflow owner and access to first-time CMACs, gate everything else."],
    blocks: [{ label: "On the slide · Five asks", items: [
      "**1 · People:** name the owner of the Furniture workflow and its master data, including the source for building and floor-plan data.",
      "**2 · Access:** introduce first-time CMACs for the retest.",
      "**3 · Rules:** confirm approval and funding rules, proposal content and who may receive a shared quote, retention, security classification and the accessibility standard.",
      "**4 · Architecture:** choose the integration and migration path: Release 1 without direct integrations, and WORTS history none, recent or all. Confirm whether SnapTracker has an API.",
      "**5 · Data:** share baselines (volumes, staff time per request, return and rework rates, reporting hours), the budget envelope and the current WORTS replacement date.",
    ] }],
    evidence: [
      "Working document §3.4 (adoption conditions) and §8 (open items log).",
      "MDPM 826 report, next steps: confirm proposal content, quote recipients, approval and funding rules with Alberta Infrastructure; retest with first-time requesters.",
      "Systems map F9 open questions (Q-03, Q-05, Q-11, Q-12).",
    ],
    visual: ["Five numbered asks, each with a one-word tag: people, access, rules, architecture, data. End with “Thank you. Questions?”"],
    appendix: ["The asks tracker (section 6 of this sheet) and the full open-items log."],
    notesBy: "Qiuchen, close by Anne-Marie",
    notes: ["To move forward we need five things from GoA. The most important is a named owner for the Furniture workflow and its master data, because status rules, access and reporting all depend on it. Next, introductions to first-time CMACs, so we can test with the people this is really for. Then the rules, the integration and migration choices, and the baselines and budget that let us put real numbers on the value. Thank you. We are happy to take your questions."],
  },
];

// ------------------------------------------------------------------ document
const children = [];
children.push(new Paragraph({ children: [new TextRun({ text: "Team DART · Strategic Product Vision", bold: true, size: 40, color: NAVY, font: "Arial" })], spacing: { after: 60 } }));
children.push(new Paragraph({ children: [new TextRun({ text: "Slide Build Sheet, filled · PRISM Requests: Furniture Request Service", size: 28, color: TEAL, font: "Arial" })], spacing: { after: 60 } }));
children.push(META("MDPM 900 · DPM Practicum: Discovery, Design and Build · Version 2 · 9 November 2026 · Ade section by the Product Architect"));
children.push(RULEP());

children.push(H2("How to read this sheet"));
[
  "Every slide answers the build sheet's four questions: the main message, the evidence, the visual, and what moves to the appendix. Every slide ends with speaker notes.",
  "**Ade's section is filled in full:** slide 6 (technical viability), slide 9 (requirements, data and architecture), the systems-map row on slide 10, the architect input on slides 7 and 11, the appendix plan and the Q&A bank for the client presentation.",
  "Other slides are filled from the team's sources so the deck tells one story. Each lead confirms their own slide.",
  "**Evidence rule:** every figure carries its source. Where GoA data does not exist yet, the slide says “GoA data needed”. No benefit, volume or cost figure appears until GoA supplies baselines.",
  "**Wording rule:** anything not yet agreed says “to confirm with GoA” or “we suggest”. No other labels.",
  "The deck runs to 12 slides plus an appendix, within the 10 to 12 slide limit. The order follows the rubric. Changes from the earlier sheet are listed in section 5.",
].forEach((t) => children.push(B(t)));

children.push(H2("1 · Rubric coverage"));
children.push(TABLE([2000, 2600, 1300, 3460], [
  ["Rubric criterion", "Level 4 asks for", "Slides", "Status"],
  ["Product Vision", "A clear description of the problem, and whom we solve it for", "2, 3, 4", "Covered. First-time CMACs untested; say so."],
  ["Business Case", "Opportunity, viability, boundary conditions", "5, 6, 7", "Covered. Baselines and budget are GoA inputs."],
  ["Product Design", "Prototype design, scenarios, requirements", "8, 9", "Covered. Check the video against the tested scope."],
  ["Product Evaluation and Changes", "Emerging tech, ethics, system", "10 (with 6 and 9)", "Covered: usability, ethics, AI and the systems map each drive a change."],
  ["Product Workplan", "Plan of action for moving forward", "11, 12", "Covered. Only dates we control are shown."],
  ["Format and Audience", "10 to 12 slides, client, style, appendix", "All", "12 slides; GoA logo and colours; client language; appendix plan in section 3."],
], { zebra: true }));
children.push(GAP());

children.push(H2("2 · Slide map"));
children.push(TABLE([700, 3500, 2700, 2460], [
  ["#", "Slide", "Lead", "Ade's part"],
  ["1", "Title, team and context", "Anne-Marie", "None"],
  ["2", "The problem", "Anne-Marie", "Systems map evidence (F2)"],
  ["3", "Users and the job to be done", "Fuyang, Qiuchen", "None"],
  ["4", "Vision and product concept", "Anne-Marie", "PRISM wording check"],
  ["5", "Business opportunity and OKRs", "Anne-Marie", "None"],
  ["**6**", "**Product viability: technical tailwinds and headwinds**", "**Adekunle**; Mmenyene (risks)", "**Lead**"],
  ["7", "Boundary conditions: cost and time", "Mmenyene", "Integration and migration options"],
  ["8", "Prototype video and guiding scenarios", "Fuyang", "None"],
  ["**9**", "**Requirements, data and architecture**", "**Adekunle**; Fuyang; Warren", "**Lead**"],
  ["10", "Product evaluation and changes", "Fuyang, Warren, Adekunle", "Systems-map row"],
  ["11", "Product workplan and roadmap", "Mmenyene", "Technical dependencies"],
  ["12", "What we need from GoA", "Qiuchen, Mmenyene", "Architecture ask"],
  ["A", "Appendix", "All", "Maintains it (client work plan)"],
], { zebra: true }));
children.push(GAP());
children.push(B("**Order change for the team to agree:** the roadmap moves from slide 8 to slide 11, so the audience sees the usability findings before the plan that responds to them. The team's own build-sheet notes suggested this, and it follows the rubric order."));
children.push(B("**Deck-wide checks (Session 17):** clean, uncluttered slides; GoA logo and colours; visuals over paragraphs; one story from problem to asks; scripted hand-offs; a timed run-through."));

slides.forEach((s) => SLIDE(s).forEach((p) => children.push(p)));

// Appendix plan
children.push(BREAK());
children.push(H1("3 · Appendix plan (Ade maintains)"));
children.push(META("The client work plan gives Ade the supporting evidence, the appendix and Q&A preparation."));
children.push(TABLE([700, 4200, 2200, 2260], [
  ["#", "Appendix slide", "Source", "Owner"],
  ["A1", "DPO evidence: the seven value opportunities and their Real, Win, Worth It scores", "DPO deck, Appendices E and F", "Anne-Marie"],
  ["A2", "Persona table and JTBD analysis", "DPO Appendices A to C; MDPM 883", "Fuyang"],
  ["A3", "Functional and non-functional requirements, one agreed numbering", "PRD; MDPM 883", "Warren, Fuyang"],
  ["A4", "Data model and data dictionary", "MDPM 883 dictionary; this sheet, slide 9", "Adekunle"],
  ["A5", "Data pipeline with controls, gaps and leaks", "MDPM 830 board (link below)", "Adekunle"],
  ["A6", "Systems map excerpts: F2 eight seams, F6 preservation register, frame 6 Demo 3", "Systems map board", "Adekunle"],
  ["A7", "Usability report: twelve issues, hypotheses, results by participant", "MDPM 826 report", "Fuyang, Qiuchen"],
  ["A8", "Ethics table and the MDPM 822 technology options comparison", "Ethical Context Analysis; AI Steward input", "Warren"],
  ["A9", "Risk register, open-items log and asks tracker", "Working document §4 and §8", "Mmenyene"],
  ["A10", "Backup answers for likely questions (section 4)", "This sheet", "Adekunle"],
], { zebra: true }));
children.push(GAP());
children.push(LBL("Board links"));
[
  ["MDPM 830 data pipeline board: ", "https://miro.com/app/board/uXjVEVTd8qQ=/?share_link_id=732592884802"],
  ["Milestone 2 board (Vision Board, client work plan, ethics): ", "https://miro.com/app/board/uXjVHidlV4o=/?share_link_id=981753140811"],
  ["Systems map board: ", "https://miro.com/app/board/uXjVH6PMnbE=/?share_link_id=289029811445"],
  ["Prototype: ", "https://worts2-self-guided.vercel.app/#/tasks"],
].forEach(([label, url]) => children.push(new Paragraph({
  numbering: { reference: "bul", level: 0 }, spacing: { after: 60 },
  children: [new TextRun({ text: label, bold: true }), new ExternalHyperlink({ link: url, children: [new TextRun({ text: url, style: "Hyperlink" })] })],
})));
children.push(B("**Handling:** the systems map board is marked Protected A (client material stays on the controlled board; no public share or external export). Use excerpts in the deck and do not add that board link to a public slide."));

// Client presentation
children.push(BREAK());
children.push(H1("4 · Client presentation, 13 November 2026"));
children.push(META("From the Client Presentation Work Plan: 15 minutes including the 3-minute video, then 10 to 15 minutes of Q&A. Faculty dry run 11 November."));
children.push(TABLE([3100, 1500, 900, 3860], [
  ["Section", "Owner", "Time", "Built from build-sheet slides"],
  ["1 · Introduction and purpose", "Anne-Marie", "0:45", "1"],
  ["2 · Problem and research findings", "Anne-Marie", "1:30", "2, 3"],
  ["3 · Product vision and value", "Anne-Marie", "1:30", "4, 5"],
  ["4 · Product experience and design", "Fuyang", "1:15", "8, with the Must strip from 9"],
  ["5 · Prototype demonstration (video)", "Fuyang", "3:00", "8"],
  ["6 · Usability testing findings", "Qiuchen", "2:00", "10"],
  ["7 · Business and operational value", "Qiuchen", "1:30", "5, 6"],
  ["8 · Limitations and future validation", "Warren", "1:00", "6, 7, 9 (open items)"],
  ["9 · Next steps and closing", "Mmenyene", "1:30", "11, 12"],
  ["**Total**", "", "**14:00**", "About 1 minute left for transitions"],
], { zebra: true }));
children.push(GAP());
children.push(LBL("Ade's role on the day"));
[
  "Check that every key claim on the slides is supported by project evidence (section 5 of this sheet).",
  "Maintain the appendix and its source references (section 3).",
  "Capture likely client questions and keep factual answers ready (Q&A bank below).",
  "Help each section owner check technical and data terms: PRISM Core, Request ID, structured reference fields, integration, migration.",
].forEach((t) => children.push(B(t)));
children.push(LBL("Final quality checks (client work plan)"));
[
  "Claims are supported by discovery or usability evidence.",
  "The presentation tells one consistent product story.",
  "The video matches the prototype being presented and plays within PowerPoint.",
  "Remaining assumptions are not presented as confirmed GoA requirements.",
  "The presentation fits within 15 minutes; transitions and likely questions are rehearsed.",
].forEach((t) => children.push(B(t)));

children.push(H2("Q&A bank (Ade): likely questions and factual answers"));
const qa = [
  ["Can PRISM actually support this?", "PRISM Core is the confirmed host: PRISM Requests runs on it as a microservice, and PRISM Core already holds building and asset data. What is not yet confirmed is the configuration capacity for the Furniture workflow: statuses, forms, notifications and attachments. We are asking for a working session with the PRISM team.", "Systems map F2 (SY-15, confirmed)"],
  ["Why no integrations in Release 1?", "Nothing is connected today. SnapTracker and BLIMS/EAMS await a GoA decision, and we do not yet know whether SnapTracker has an API. Release 1 records the PO number and reservation ID as structured fields, so later connections have clean keys.", "F2; F9 Q-03, Q-05; MDPM 830 scope"],
  ["Will WORTS history move over?", "Not in the current proposal. It is a GoA decision with three options: none, recent history only, or all. Each changes cost and the legacy fields the data model must hold.", "MDPM 830 scope boundary"],
  ["How do you know requesters want this?", "Six GoA staff tested it. 14 of 24 attempts needed no help, mean ease was 3.75 of 5, and the guided form and auto-filled building details were the most liked features. We also found four major issues, and each now has a design change.", "MDPM 826 report"],
  ["Did you test first-time CMACs?", "No. All six participants had WORTS experience, and two submit only occasionally. A retest with first-time requesters is our first validation step and needs GoA introductions.", "MDPM 826 report"],
  ["What will it cost, and when will it be ready?", "We have identified the cost drivers, but we will not commit to a budget or schedule without GoA's constraints. The scope statement plans WORTS replacement before March 2027; our own dates are 13 November (presentation) and 26 November (final PRD).", "Slide 7; scope statement; M2 work plan"],
  ["Where is AI?", "Not in the first release. Our assessment found the immediate problems are better solved by clearer submission, visible status and connected information. AI stays a future option once there is a clear need, reliable data and evidence it beats simpler options.", "AI Steward SPV input"],
  ["How will you measure success?", "From the same record the service creates: first-pass submission completeness; status comprehension, information retrieval and follow-up effort; and manual reporting effort. Targets are set once GoA shares baselines.", "MDPM 830 measurement sink; DPO OKRs"],
  ["Who can see what?", "Access is based on role and portfolio. Requesters see only requests they are permitted to view, internal notes stay restricted, and reports describe the service, not individual staff.", "MDPM 883 security requirements; ethics analysis"],
  ["What happens to the controls WORTS has today?", "We keep them: role and portfolio access, approval thresholds, full audit history, reservation locks, sealed stages, archive-never-delete and client sign-off. The systems map shows that dropping them would get the product rejected.", "Systems map F6 (IC-5)"],
  ["Why Furniture only?", "It is the journey our evidence covers, and a bounded first service lowers delivery risk. Maintenance requests are out of scope. The core workflow could be reused later, but that is a supporting opportunity, not part of this proposal.", "DPO; MDPM 883 scope"],
  ["Who owns the data?", "Not yet decided. Process ownership, data stewardship and the master asset registry are open, which is why a named owner is our first ask.", "Systems map F6; F9 Q-11"],
  ["Will notifications reach email?", "The design has email notifications that open the right request, because testers asked for them and one lost track of a request from an update. The exact PRISM notification capability is to confirm with the PRISM team.", "MDPM 826 issue I5; Appendix A"],
  ["How are duplicate requests handled?", "The requirements call for identifying and resolving duplicates while keeping the request history. The rule for deciding that two requests are the same is still to agree with GoA.", "MDPM 883 requirements; MDPM 830 clean-data rules"],
];
children.push(TABLE([2300, 5160, 1900], [["Question", "Answer", "Source"], ...qa], { zebra: true }));

// Corrections
children.push(BREAK());
children.push(H1("5 · Critical review: corrections in this version"));
children.push(META("Each fix brings the slides into line with the final sources, so the deck, the PRD and the boards say the same thing."));
const fixes = [
  ["“All 24 attempts were completed”", "24 recorded attempts: 14 unaided, 10 with help. One task 3 outcome is unconfirmed, and the report says the counts are not a success rate.", "MDPM 826 report"],
  ["“All six testers understood status” (6 of 6)", "Removed. Task 2 had 4 unaided and 2 with help; one participant could not read the dates and another was unsure who owned a stage.", "MDPM 826, task 2 and SH4"],
  ["Four major issues listed as date wording, status dates, thin proposal and no preview", "The final report's four major issues are date and timing wording, the checklist panel, update wording and navigation, and share confirmation. Status dates and the client preview are minor issues.", "MDPM 826, issues I1, I4, I5, I6"],
  ["Minor issue count unclear (8 or 15)", "Eight minor issues (I2, I3, I7 to I12). Twelve issues in total, none critical.", "MDPM 826 report"],
  ["Scenario 2 shown as a coordinator building a quote", "The tested prototype had no coordinator screens; tasks 3 and 4 were done as the requester. Any coordinator view in the video must be labelled as untested.", "MDPM 826 plan and report"],
  ["WORTS end-of-life date “Unconfirmed”", "The GoA Capstone Scope Statement plans replacement before March 2027 (a confirmed fact on the planning board). Show it with its source and confirm it is current.", "Systems map board, planning frame; F2 (C-002)"],
  ["Unsourced targets and limits: an unaided-rate target, a role-rule percentage, a named accessibility level, prototype file-size limits and a purchasing threshold", "Removed from slide text. These are team proposals, prototype settings or single-source figures. Targets follow the GoA baseline; limits and standards are confirmed with GoA.", "DPO OKRs; team evidence rule"],
  ["“4 of 6 testers still handle approvals by email”", "Three participants (P4, P5, P6) described approvals collected and returned by email.", "MDPM 826, task 4"],
  ["“4 of 6 wanted help for first-time users”", "Not in the final report. Replaced by its finding: guidance for first-time users needs testing with first-time requesters.", "MDPM 826, further validation"],
  ["Non-functional requirement: integrate with Outlook, SnapTracker and OneGX/SAP", "Release 1 has no direct integrations; references become structured fields; connections follow a GoA decision.", "MDPM 830 scope boundary"],
  ["EIMS named as the building system", "EIMS holds floor plans and drawings; BLIMS versus EAMS for building data is still open.", "Systems map frame 6, correction 3"],
  ["Requirement numbers (FR-01 and so on) on slides", "Removed. The PRD and MDPM 883 numberings differ; describe requirements by name until they are reconciled.", "Section-lead build sheet notes"],
  ["Value opportunities cited by number; client names in the asks tracker", "Opportunities named, with scores; the client is referred to as the GoA sponsor.", "Team feedback"],
  ["Roadmap at slide 8, before the findings it responds to", "Roadmap at slide 11, after the evidence; order follows the rubric.", "Section-lead notes; rubric"],
  ["Two versions of the vision statement", "Flagged on slide 4: agree one wording.", "Vision Board; earlier sheet"],
];
children.push(TABLE([2600, 4560, 2200], [["What the earlier sheet said", "Correction", "Source"], ...fixes], { zebra: true }));

// Asks tracker
children.push(H2("6 · Asks tracker (appendix)"));
children.push(TABLE([3000, 3700, 2660], [
  ["Ask", "Why it matters", "Evidence"],
  ["Name the owner of the Furniture workflow and master data", "Status rules, access and reporting depend on it", "Systems map F6 governance gaps"],
  ["Introduce first-time CMACs for the retest", "All six testers already used WORTS", "MDPM 826 limits"],
  ["Confirm proposal content and quote recipients", "Participants asked for more detail; the test proposal was fictional", "MDPM 826 next steps"],
  ["Confirm approval and funding rules", "Approvals still travel by email; participants expected different budget fields", "MDPM 826, task 4 and further validation"],
  ["Set the role and authority upkeep process", "Rules, roles and thresholds change over time", "DPO; systems map F6"],
  ["Choose the integration path and confirm the SnapTracker API", "The most variable cost and time driver", "F2; F9 Q-03, Q-05"],
  ["Decide WORTS history migration: none, recent or all", "Sets migration cost and legacy fields", "MDPM 830 scope"],
  ["Confirm retention, security classification and accessibility standard", "Sets the non-functional thresholds", "MDPM 883 requirements"],
  ["Share baselines: volume, staff time per request, return rate, reporting hours", "Turns the OKRs and benefit logic into numbers", "F9 Q-12"],
  ["Confirm the budget envelope and the current replacement date", "Bounds the plan", "Scope statement (before March 2027)"],
], { zebra: true }));

// Open items owned by Ade
children.push(H2("7 · Open items Ade owns"));
[
  "**Q-05:** does SnapTracker expose an API or integration surface? (Product Architect, open)",
  "**Q-07:** what digital audit trail would let the warehouse retire paper shadowing? (Product Architect, open)",
  "**Q-11:** does one governed FEMIS foundation underlie VFA, CMMS and EAMS, or are the registries fractured? (Product Architect, open)",
  "**PRISM configuration capacity:** statuses, forms, notifications, attachments. Book a session with the PRISM team.",
  "**Request ID format and the status list,** agreed with GoA before the final PRD.",
  "**Reconcile the data model** with the MDPM 883 data dictionary and the MDPM 830 pipeline before the final PRD on 26 November 2026.",
].forEach((t) => children.push(B(t)));

// Sources
children.push(H2("8 · Sources"));
[
  "MDPM 900 Strategic Product Vision rubric (Product Vision and Prototype dropbox) and Session 17: Developing the Product Vision and Client Presentation.",
  "Team DART Slide Build Sheet, section-lead version, and the Slide Build Sheet filled on 7 November 2026.",
  "Digital Product Opportunity deck, 4 September 2026 (problem, journey, value opportunities, OKRs, appendices A to G).",
  "MDPM 883 Requirements Document, 20 September 2026 (requirements, data dictionary, task model, scenarios, personas).",
  "MDPM 826 Usability Testing Plan (22 October 2026) and Usability Test Report (5 November 2026).",
  "MDPM 830 Data Pipeline deck and board.",
  "Milestone 2 board: Vision Board frames, Client Presentation Work Plan, AI Steward input to the Strategic Product Vision, Ethical Context Analysis.",
  "Systems map board: planning frame (scope statement facts), F2, F6, F9 and frame 6 (Demo 3, 2 April 2026).",
  "Prototype at https://worts2-self-guided.vercel.app/#/tasks. Its content here follows the MDPM 826 plan and report, which document the prototype as tested.",
  "Team DART Milestone 2 Work System (roles and dates).",
].forEach((t) => children.push(B(t)));

const doc = new Document({
  creator: "Team DART",
  title: "Team DART Strategic Product Vision Slide Build Sheet",
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Arial", size: 30, bold: true, color: NAVY }, paragraph: { spacing: { before: 120, after: 80 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Arial", size: 24, bold: true, color: NAVY }, paragraph: { spacing: { before: 240, after: 100 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [
    { reference: "bul", levels: [
      { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 260 } } } },
      { level: 1, format: LevelFormat.BULLET, text: "◦", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 760, hanging: 260 } } } },
    ] },
    { reference: "num", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 300 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      new TextRun({ text: "Team DART · Strategic Product Vision · Slide Build Sheet v2 · page ", color: GREY, size: 16 }),
      new TextRun({ children: [PageNumber.CURRENT], color: GREY, size: 16 }),
    ] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(process.argv[2], buf); console.log("wrote", process.argv[2]); });
