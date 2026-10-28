"""Build the Maplewood Villa folio: standalone SVG drawings, the web page and the print page.

    python3 build.py            # writes ../drawings/*.svg, ../index.html, ../print.html
    node render_pdf.js          # turns ../print.html into ../Maplewood-Villa.pdf
"""
import html
import os

import content as C
import elevations
import plans

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
CSS = open(os.path.join(HERE, "drawing.css")).read()

LIGHT = """
  --d-wall:#25231f; --d-paper:#fbfaf7; --d-line:#2d2a25; --d-glass:#7d9aa6; --d-ink:#1f1d1a; --d-muted:#8a857c;
  --d-counter:#e4ded3; --d-builtin:#ddd5c6; --d-stone2:#cfc6b6; --d-wet:#dfe7ea; --d-oak:#efe4d2; --d-stone:#ece8e1;
  --d-tile:#e9ebea; --d-carpet:#f3f0ea; --d-porch:#e6e0d4; --d-garage:#ecebe8; --d-void:#f7f6f3; --d-furn:#fbfaf7;
  --d-furnline:#a59d90; --d-rug:#f6efe3; --d-plant:#dfe6d6; --d-plantline:#8c9a7c; --d-accent:#8a6a3b; --d-on-accent:#fff;
  --e-stucco:#f6f3ee; --e-edge:#b9b1a3; --e-stone:#ddd3c2; --e-joint:#bfb39f; --e-oak:#c69c6d; --e-oakln:#a87d50;
  --e-roof:#3a3d40; --e-seam:#55595d; --e-steel:#1f2124; --e-glass:#46525c; --e-glint:rgba(255,255,255,.10);
  --e-shade:rgba(30,25,20,.28); --e-bronze:#6d5a3f; --e-earth:#e7e2d8; --e-tree:#cfd8c4; --e-treehi:rgba(255,255,255,.35);
  --e-treeln:#8c9a7c; --e-shrub:#c4cfb6; --e-person:#3a3833; --e-lamp:#f3d9a4;"""

DARK = """
  --d-wall:#e7e2d8; --d-paper:#1a1917; --d-line:#d8d2c6; --d-glass:#86aab9; --d-ink:#eeeae3; --d-muted:#948e83;
  --d-counter:#3a3631; --d-builtin:#403b34; --d-stone2:#4b463f; --d-wet:#22292c; --d-oak:#2a251f; --d-stone:#262421;
  --d-tile:#212527; --d-carpet:#23211e; --d-porch:#2e2b26; --d-garage:#201f1d; --d-void:#1d1c1a; --d-furn:#1a1917;
  --d-furnline:#7f786c; --d-rug:#29251f; --d-plant:#2b3326; --d-plantline:#7e8d6f; --d-accent:#cda86d; --d-on-accent:#1a1917;
  --e-stucco:#ddd8cd; --e-edge:#9d9586; --e-stone:#c7bba6; --e-joint:#a99c86; --e-oak:#b38959; --e-oakln:#946b40;
  --e-roof:#2f3236; --e-seam:#464a4f; --e-steel:#121315; --e-glass:#394550; --e-glint:rgba(255,255,255,.08);
  --e-shade:rgba(0,0,0,.32); --e-bronze:#6a573c; --e-earth:#26241f; --e-tree:#4f5b46; --e-treehi:rgba(255,255,255,.10);
  --e-treeln:#7e8d6f; --e-shrub:#47523f; --e-person:#cfc9be; --e-lamp:#f3d9a4;"""


def drawings():
    return {
        "front": elevations.front(),
        "rear": elevations.rear(),
        "main": plans.main_floor(),
        "second": plans.second_floor(),
        "lower": plans.lower_level(),
    }


def write_svgs(d):
    os.makedirs(os.path.join(OUT, "drawings"), exist_ok=True)
    style = f"<style>:root{{--f-label:'Jost','Futura','Helvetica Neue',Arial,sans-serif;{LIGHT}}}svg{{background:#fbfaf7}}{CSS}</style>"
    names = {"front": "elevation-front", "rear": "elevation-rear", "main": "plan-main-floor",
             "second": "plan-second-floor", "lower": "plan-lower-level"}
    for k, svg in d.items():
        head, rest = svg.split(">", 1)
        with open(os.path.join(OUT, "drawings", names[k] + ".svg"), "w") as f:
            f.write(head + ">" + style + rest + "\n")


def esc(s):
    return html.escape(s, quote=False)


def notes_html(level):
    items = []
    for n, title, body in C.NOTES[level]:
        items.append(f'<li><span class="num" aria-hidden="true">{n}</span><div><h4>{esc(title)}</h4>'
                     f'<p>{esc(body)}</p></div></li>')
    return '<ol class="notes">' + "".join(items) + "</ol>"


def stats_html():
    return "".join(f'<div class="stat"><span class="v">{esc(v)}</span><span class="k">{esc(k)}</span></div>'
                   for v, k in C.STATS)


def principles_html():
    return "".join(f'<div class="pr"><h3>{esc(t)}</h3><p>{esc(b)}</p></div>' for t, b in C.PRINCIPLES)


def compare_html():
    rows = "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>"
                   for a, b, c in C.COMPARE)
    return ('<table class="cmp"><thead><tr><th scope="col"></th><th scope="col">Maplewood (2026 brochure)</th>'
            f'<th scope="col">Maplewood Villa</th></tr></thead><tbody>{rows}</tbody></table>')


def materials_html():
    return "".join(f'<div class="sw"><span class="chip" style="background:var({v})"></span>'
                   f'<div><h4>{esc(n)}</h4><p>{esc(u)}</p></div></div>' for n, u, v in C.MATERIALS)


def areas_html():
    rows = "".join(f'<tr{" class=tot" if "Total" in k else ""}><th scope="row">{esc(k)}</th><td>{esc(v)}</td></tr>'
                   for k, v in C.AREAS)
    return f'<table class="areas"><tbody>{rows}</tbody></table>'


def caveats_html(items=None):
    return "<ul class=\"cav\">" + "".join(f"<li>{esc(c)}</li>" for c in (items or C.CAVEATS)) + "</ul>"


def fill(tpl, d):
    rep = {
        "@@CSS@@": CSS, "@@LIGHT@@": LIGHT, "@@DARK@@": DARK,
        "@@FRONT@@": d["front"], "@@REAR@@": d["rear"], "@@MAIN@@": d["main"],
        "@@SECOND@@": d["second"], "@@LOWER@@": d["lower"],
        "@@NOTES_MAIN@@": notes_html("main"), "@@NOTES_SECOND@@": notes_html("second"),
        "@@NOTES_LOWER@@": notes_html("lower"), "@@STATS@@": stats_html(),
        "@@PRINCIPLES@@": principles_html(), "@@COMPARE@@": compare_html(),
        "@@MATERIALS@@": materials_html(), "@@AREAS@@": areas_html(), "@@CAVEATS@@": caveats_html(), "@@CAVEATS_SHORT@@": caveats_html(C.CAVEATS_SHORT),
    }
    for k, v in rep.items():
        tpl = tpl.replace(k, v)
    assert "@@" not in tpl, tpl[tpl.index("@@"):tpl.index("@@") + 40]
    return tpl


if __name__ == "__main__":
    d = drawings()
    write_svgs(d)
    for name in ("index", "print"):
        tpl = open(os.path.join(HERE, f"{name}.tpl.html")).read()
        with open(os.path.join(OUT, f"{name}.html"), "w") as f:
            f.write(fill(tpl, d))
    print("built", ", ".join(sorted(d)))
