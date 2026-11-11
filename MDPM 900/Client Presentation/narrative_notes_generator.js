const fs = require("fs");
const path = require("path");
const c = require(path.resolve(process.argv[2]));
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, ShadingType, BorderStyle, Footer, PageNumber, HeadingLevel, PageBreak } = require("docx");
const NAVY = "1F3A5F", TEAL = "0F6E6E", GREY = "5B6470", LIGHT = "F3F5F8", ADE = "E6F2F2", RULE = "C9D1DB", WPM = 140;
function runs(text, base = {}) { const out = []; String(text).split(/(\*\*[^*]+\*\*)/g).forEach((p) => { if (!p) return; if (p.startsWith("**") && p.endsWith("**")) out.push(new TextRun({ text: p.slice(2, -2), bold: true, ...base })); else out.push(new TextRun({ text: p, ...base })); }); return out; }
const P = (t, o = {}, sp = {}) => new Paragraph({ children: runs(t, o), spacing: { after: 140, line: 288, ...sp } });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const META = (t) => new Paragraph({ children: runs(t, { color: GREY, size: 19, italics: true }), spacing: { after: 100 } });
const LBL = (t) => new Paragraph({ children: [new TextRun({ text: t.toUpperCase(), bold: true, color: TEAL, size: 18 })], spacing: { before: 160, after: 80 }, keepNext: true });
const BREAK = () => new Paragraph({ children: [new PageBreak()] });
function BOX(paras, fill) {
  const side = { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 6 };
  const borders = { top: side, bottom: side, right: side, left: { style: BorderStyle.SINGLE, size: 18, color: TEAL, space: 6 } };
  return paras.map((t, i) => new Paragraph({ children: runs(t, { size: 22 }), shading: { type: ShadingType.CLEAR, color: "auto", fill }, border: borders, spacing: { after: i === paras.length - 1 ? 200 : 120, line: 300 } }));
}
function TABLE(widths, rows) {
  const b = { style: BorderStyle.SINGLE, size: 4, color: RULE };
  return new Table({ width: { size: widths.reduce((a, x) => a + x, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, ri) => new TableRow({ tableHeader: ri === 0, cantSplit: true, children: r.map((cell, ci) => new TableCell({
      width: { size: widths[ci], type: WidthType.DXA }, borders: { top: b, bottom: b, left: b, right: b },
      shading: ri === 0 ? { type: ShadingType.CLEAR, color: "auto", fill: NAVY } : (ri % 2 === 0 ? { type: ShadingType.CLEAR, color: "auto", fill: LIGHT } : undefined),
      margins: { top: 50, bottom: 50, left: 90, right: 90 },
      children: [new Paragraph({ children: runs(cell, ri === 0 ? { bold: true, color: "FFFFFF", size: 18 } : { size: 18 }), spacing: { after: 20 } })] })) })) });
}
const words = (a) => a.join(" ").replace(/\*\*/g, "").split(/\s+/).filter(Boolean).length;
const mmss = (sec) => Math.floor(sec / 60) + ":" + String(Math.round(sec % 60)).padStart(2, "0");
const toSec = (t) => { const [m, s] = t.split(":").map(Number); return m * 60 + s; };

const ch = [];
ch.push(new Paragraph({ children: [new TextRun({ text: "Team DART · Client Presentation", bold: true, size: 40, color: NAVY })], spacing: { after: 40 } }));
ch.push(new Paragraph({ children: [new TextRun({ text: "Speaking Notes: the narrative edition", size: 30, color: TEAL })], spacing: { after: 60 } }));
ch.push(META("PRISM / WORTS 2 · Government of Alberta · 13 November 2026 · Written to the final client deck and the team's Client Presentation Speaking Plan"));
ch.push(H2("The story we are telling"));
c.story.forEach((t) => ch.push(P(t)));
ch.push(H2("How to use these notes"));
ch.push(P("Each slide has two parts. The **spoken script** is what the presenter says. It is written as continuous prose that picks up the thread of the slide before and hands it to the next, and it is sized to the speaking plan at about 140 words a minute, so the whole talk fits within fifteen minutes with the video. The **deeper story** is not read aloud. It is the evidence and reasoning behind the slide, written so each presenter understands their slide well enough to speak naturally, recover if they lose their place, and answer questions with confidence. Words in bold in the scripts are anchors to remember."));
let total = 0;
const rows = [["Slide", "Presenter", "Title", "Plan", "Script"]];
c.slides.forEach((s) => { total += toSec(s.time); const w = words(s.script);
  rows.push([String(s.n), s.ade ? "**" + s.who + "**" : s.who, s.ade ? "**" + s.title + "**" : s.title, s.time, s.video ? "Video" : w + " words, about " + mmss(w / WPM * 60)]); });
rows.push(["", "", "**Slides, including the video**", "**" + mmss(total) + "**", ""]);
rows.push(["", "", "Transitions", "0:30", "Handoffs are written into the scripts"]);
rows.push(["", "", "**Total**", "**15:00**", ""]);
ch.push(TABLE([700, 1500, 3900, 900, 2360], rows));

c.slides.forEach((s) => {
  const w = words(s.script);
  ch.push(BREAK());
  ch.push(H1("Slide " + s.n + " · " + s.title));
  ch.push(META("Presenter: " + s.who + " · " + s.time + (s.video ? "" : " · " + w + " words, about " + mmss(w / WPM * 60))));
  if (s.ade) ch.push(new Paragraph({ children: [new TextRun({ text: "ADE'S SLIDE", bold: true, color: TEAL, size: 18 })], shading: { type: ShadingType.CLEAR, color: "auto", fill: ADE }, spacing: { after: 80 } }));
  ch.push(P("**Where it sits in the story.** " + s.place, { color: GREY }));
  ch.push(LBL(s.video ? "Cue" : "Spoken script"));
  BOX(s.script, s.ade ? ADE : LIGHT).forEach((p) => ch.push(p));
  ch.push(LBL("The deeper story"));
  s.deeper.forEach((t) => ch.push(P(t)));
});
ch.push(BREAK());
ch.push(H1("Questions the client may ask"));
ch.push(P("Ade holds the evidence, appendix and Q&A role for the presentation. The answers below are short enough to say in under thirty seconds and stay within what the team's evidence supports.", { color: GREY }));
c.qa.forEach(([q, a]) => { ch.push(new Paragraph({ children: runs("**" + q + "**"), spacing: { before: 120, after: 40 }, keepNext: true })); ch.push(P(a)); });
ch.push(H1("Before you present: points to align"));
ch.push(P("A few statements in the team's sources do not agree with each other. The notes follow the final deck in each case; the paragraphs below explain why, so everyone says the same thing.", { color: GREY }));
c.align.forEach((t) => ch.push(P(t)));

const doc = new Document({ creator: "Team DART", title: "Team DART Client Presentation Speaking Notes",
  styles: { default: { document: { run: { font: "Arial", size: 21 } } }, paragraphStyles: [
    { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: "Arial", size: 30, bold: true, color: NAVY }, paragraph: { spacing: { before: 120, after: 60 }, keepNext: true, outlineLevel: 0 } },
    { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: "Arial", size: 24, bold: true, color: NAVY }, paragraph: { spacing: { before: 240, after: 100 }, keepNext: true, outlineLevel: 1 } } ] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Team DART · Client Presentation Speaking Notes · page ", color: GREY, size: 16 }), new TextRun({ children: [PageNumber.CURRENT], color: GREY, size: 16 })] })] }) },
    children: ch }] });
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(process.argv[3], b); console.log("wrote", process.argv[3]); });
