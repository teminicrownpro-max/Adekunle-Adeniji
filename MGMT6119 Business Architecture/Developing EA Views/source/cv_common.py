"""Shared drawing helpers and capability data for the CV-2 and CV-4 diagrams."""

FONT = "Inter, 'Liberation Sans', Arial, sans-serif"
INK = "#1b2a3a"
QUIET = "#5b6b7c"
NAVY = "#1f4f80"
GAP = "#c62828"

# group id -> (name lines, strong colour, light fill)
GROUPS = {
    "C1": (["Distress", "alerting"], "#b23a2e", "#fbeae7"),
    "C2": (["Mission", "coordination"], "#1f4f80", "#e4eef9"),
    "C3": (["Search"], "#0f766e", "#e0f2ef"),
    "C4": (["Rescue and", "recovery"], "#b45309", "#fdf0e2"),
    "C5": (["Medical response", "and hand-over"], "#6b3fa0", "#f0e9f8"),
    "C6": (["Enabling", "capabilities"], "#4b5a6a", "#eceff3"),
}

# capability id -> name lines
CAPS = {
    "C1.1": ["Satellite beacon", "detection, location"],
    "C1.2": ["Maritime distress", "radio watch"],
    "C1.3": ["Alert verification", "and classification"],
    "C2.1": ["Search planning"],
    "C2.2": ["Resource tasking"],
    "C2.3": ["Situational", "awareness"],
    "C2.4": ["Multi-agency", "coordination"],
    "C3.1": ["Aerial search"],
    "C3.2": ["Surface search"],
    "C3.3": ["On-scene", "coordination"],
    "C4.1": ["Aerial rescue (hoist)"],
    "C4.2": ["Surface recovery"],
    "C4.3": ["Survival equipment", "delivery"],
    "C5.1": ["On-scene first aid"],
    "C5.2": ["Medical evacuation"],
    "C5.3": ["Casualty hand-over", "to EMS"],
    "C6.1": ["Met-ocean", "intelligence"],
    "C6.2": ["Communications", "and information", "exchange"],
    "C6.3": ["Readiness: trained", "crews and available", "assets"],
}

MEASURES = {
    "C1": ["Time to detect and", "locate a distress"],
    "C2": ["Time from first alert", "to first tasking"],
    "C3": ["Probability of success", "(POS) of the search"],
    "C4": ["Lives saved as a share", "of persons at risk"],
    "C5": ["Time from rescue to", "hospital care"],
    "C6": ["Availability of assets", "and communications"],
}


class Svg:
    def __init__(self, w, h):
        self.w, self.h, self.o = w, h, []

    def add(self, s):
        self.o.append(s)

    def text(self, x, y, s, size=14, weight=400, fill=INK, anchor="middle", style="", spacing=None):
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        st = f' font-style="{style}"' if style else ""
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}{st}>{s}</text>')

    def rect(self, x, y, w, h, fill, stroke, sw=1.6, rx=9, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def path(self, d, color, width=2, dash=None, end=True, marker="ar"):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        me = f' marker-end="url(#{marker})"' if end else ""
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"{ds}{me}/>')

    def open(self):
        self.add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" font-family="{FONT}">')
        self.add('<defs>'
                 f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="11" markerHeight="11" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#46525e"/></marker>'
                 f'<marker id="cp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="13" markerHeight="13" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1b2a3a"/></marker>'
                 f'<marker id="gap" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{GAP}"/></marker>'
                 '</defs>')
        self.add(f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>')

    def title(self, title, subtitle):
        self.text(40, 46, title, 28, 700, anchor="start")
        self.text(40, 76, subtitle, 15, 400, QUIET, anchor="start")
        self.add(f'<line x1="40" y1="92" x2="{self.w-40}" y2="92" stroke="#d5dbe1" stroke-width="1"/>')

    def footer(self):
        self.add(f'<text x="{self.w-40}" y="{self.h-16}" font-size="12.5" fill="{QUIET}" text-anchor="end">Author: Adekunle Adeniji (1378471) · MGMT6119 · 16 Nov 2026</text>')

    def save(self, path):
        self.add('</svg>')
        open(path, "w").write("\n".join(self.o))
