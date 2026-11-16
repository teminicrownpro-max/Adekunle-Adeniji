"""Build the submission .docx from a markdown source: pandoc, then style with python-docx.

Run from this folder:
  python3 build_docx.py                      # CV-2 + CV-4 submission
  python3 build_docx.py submission_ov.md OUT.docx ov   # OV-1 + OV-2 backup
"""
import subprocess
import sys
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

SRC = sys.argv[1] if len(sys.argv) > 1 else "submission.md"
OUT = sys.argv[2] if len(sys.argv) > 2 else "../Adekunle_Adeniji_1378471_Developing_EA_Views.docx"
PROFILE = sys.argv[3] if len(sys.argv) > 3 else "cv"
subprocess.run(["pandoc", SRC, "-o", OUT, "--resource-path=.:..:../Backup - OV-1 and OV-2 version"], check=True)

doc = Document(OUT)
NAVY = RGBColor(0x1F, 0x4F, 0x80)
INK = RGBColor(0x1B, 0x2A, 0x3A)

for s in doc.sections:
    s.page_width, s.page_height = Inches(8.5), Inches(11)
    s.left_margin = s.right_margin = Inches(1)
    s.top_margin = s.bottom_margin = Inches(0.9)

def font(style_name, size, bold=None, color=None, italic=None):
    try:
        st = doc.styles[style_name]
    except KeyError:
        return
    st.font.name = "Calibri"
    rpr = st.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts"); rpr.append(rfonts)
    for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(k), "Calibri")
    for k in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rfonts.get(qn(k)) is not None:
            del rfonts.attrib[qn(k)]
    st.font.size = Pt(size)
    if bold is not None: st.font.bold = bold
    if italic is not None: st.font.italic = italic
    if color is not None: st.font.color.rgb = color

font("Normal", 11, color=INK)
for n in ("Body Text", "First Paragraph", "Compact"):
    font(n, 11, color=INK)
font("Title", 22, bold=True, color=NAVY)
font("Subtitle", 13, bold=False, color=INK, italic=False)
font("Author", 12, color=INK)
font("Date", 12, color=INK)
font("Heading 2", 15, bold=True, color=NAVY)
font("Heading 3", 12.5, bold=True, color=NAVY)
font("Image Caption", 10, italic=True, color=INK)
font("Captioned Figure", 11)

for n in ("Body Text", "First Paragraph"):
    try:
        pf = doc.styles[n].paragraph_format
        pf.space_after = Pt(5); pf.space_before = Pt(0); pf.line_spacing = 1.05
    except KeyError:
        pass

def set_cell_shading(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)

def set_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single"); el.set(qn("w:sz"), "4"); el.set(qn("w:space"), "0"); el.set(qn("w:color"), "9AA8B6")
        borders.append(el)
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    tblPr.append(borders)

WIDTHS = {  # inches per column, by column count; each sums to the 6.5 in text width
    2: [1.9, 4.6],
    3: [0.75, 1.15, 4.6],
    4: [0.35, 1.6, 2.15, 2.4],
    5: [0.55, 1.75, 0.8, 1.15, 2.25],
}

CV_TABLES = [  # per table, in document order
    [1.9, 4.6], [2.0, 4.5], [1.45, 3.45, 1.6], [2.0, 4.5],
    [0.5, 1.35, 4.65], [1.75, 1.55, 1.6, 1.6], [2.4, 4.1],
]

def set_widths(table, idx):
    cols = len(table.columns)
    widths = WIDTHS.get(cols)
    if PROFILE == "cv" and idx < len(CV_TABLES) and len(CV_TABLES[idx]) == cols:
        widths = CV_TABLES[idx]
    if not widths:
        return
    table.autofit = False
    tblPr = table._tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW"); tblPr.append(tblW)
    tblW.set(qn("w:type"), "dxa"); tblW.set(qn("w:w"), str(int(6.5 * 1440)))
    layout = OxmlElement("w:tblLayout"); layout.set(qn("w:type"), "fixed"); tblPr.append(layout)
    grid = table._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * 1440)))
    for row in table.rows:
        for cell, w in zip(row.cells, widths):
            cell.width = Inches(w)

for t_i, t in enumerate(doc.tables):
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(t)
    set_widths(t, t_i)
    for r_i, row in enumerate(t.rows):
        for cell in row.cells:
            if r_i == 0:
                set_cell_shading(cell, "DCEBF8")
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.space_before = Pt(2)
                for run in p.runs:
                    run.font.size = Pt(9.5)
                    if r_i == 0:
                        run.font.bold = True

# centre figures and their captions
for p in doc.paragraphs:
    if p._p.xpath(".//w:drawing"):
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if p.text.startswith("Figure "):
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.core_properties.author = "Adekunle Adeniji"
doc.core_properties.title = "Developing EA Views – DoDAF " + ("CV-2 and CV-4" if PROFILE == "cv" else "OV-1 and OV-2")
doc.save(OUT)
print("wrote", OUT)
