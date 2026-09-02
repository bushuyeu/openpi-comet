#!/usr/bin/env python3
"""Render docs/src/*.md into the static pages served by GitHub Pages.

Usage:  pip install markdown && python3 docs/build.py
Edit the markdown in docs/src/. Do not edit the generated .html by hand.
"""

import os, re, markdown

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "src")
DOCS = HERE
os.makedirs(DOCS, exist_ok=True)

PAGES = [
    ("index.html",       "experiment.md",  "The experiment"),
    ("rft-dataset.html", "rft-dataset.md", "RFT dataset"),
    ("compute.html",     "hardware.md",    "Hardware"),
]

def nav(active):
    out = ['<nav class="nav">']
    for href, _, label in PAGES:
        cls = ' class="on"' if href == active else ''
        out.append('<a href="{}"{}>{}</a>'.format(href, cls, label))
    out.append('<a class="ext" href="https://github.com/bushuyeu/openpi-comet">repo &#8599;</a>')
    out.append('</nav>')
    return "".join(out)

# shared stylesheet, same tokens as the slides
CSS = """
:root{--ground:#FCFCFD;--surface:#F2F3F6;--surface-2:#E9EBF0;--ink:#14161B;--ink-mid:#3D434F;
--ink-mute:#5A606E;--rule:#DCDFE6;--rule-soft:#E8EAEF;--accent:#A85C08;--pass:#15654A;
--pass-bg:#DCEFE6;--fail:#8E2620;--fail-bg:#F6E1DF;
--sans:ui-sans-serif,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
--serif:ui-serif,"Iowan Old Style",Georgia,"Times New Roman",serif;
--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ground:#0E1014;--surface:#161920;
--surface-2:#1E222B;--ink:#E9EBF1;--ink-mid:#BFC5D2;--ink-mute:#939AAA;--rule:#272C36;
--rule-soft:#1E222B;--accent:#E0A040;--pass:#5DC79C;--pass-bg:#122C23;--fail:#E9827A;--fail-bg:#341A18}}
:root[data-theme="dark"]{--ground:#0E1014;--surface:#161920;--surface-2:#1E222B;--ink:#E9EBF1;
--ink-mid:#BFC5D2;--ink-mute:#939AAA;--rule:#272C36;--rule-soft:#1E222B;--accent:#E0A040;
--pass:#5DC79C;--pass-bg:#122C23;--fail:#E9827A;--fail-bg:#341A18}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--serif);
font-size:17px;line-height:1.62;-webkit-font-smoothing:antialiased}
.wrap{max-width:80ch;margin:0 auto;padding:0 26px 100px}
h1,h2,h3,h4,.nav{font-family:var(--sans)}
h1{font-size:2.1rem;line-height:1.1;letter-spacing:-.03em;font-weight:800;margin:8px 0 4px;text-wrap:balance}
h2{font-size:1.45rem;line-height:1.15;letter-spacing:-.02em;font-weight:750;margin:44px 0 2px;text-wrap:balance}
h3{font-size:1.1rem;font-weight:700;margin:30px 0 2px}
p,ul,ol{margin:14px 0}
a{color:var(--accent)}
strong{font-weight:640}
code{font-family:var(--mono);font-size:.87em;background:var(--surface-2);padding:.1em .38em;border-radius:3px}
pre{background:var(--surface-2);padding:13px 15px;border-radius:6px;overflow-x:auto}
pre code{background:none;padding:0;font-size:.82rem;line-height:1.5}
blockquote{margin:16px 0;padding:2px 0 2px 18px;border-left:3px solid var(--accent);color:var(--ink-mid)}
table{border-collapse:collapse;width:100%;font-family:var(--sans);font-size:.87rem;margin:6px 0}
th{text-align:left;font-size:.71rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-mute);
padding:11px 14px;border-bottom:1px solid var(--rule);background:var(--surface-2);white-space:nowrap}
td{padding:10px 14px;border-bottom:1px solid var(--rule-soft);vertical-align:top;font-variant-numeric:tabular-nums}
.tw{overflow-x:auto;border:1px solid var(--rule);border-radius:6px;background:var(--surface);margin:14px 0}
.nav{display:flex;flex-wrap:wrap;gap:6px 18px;padding:22px 0 18px;margin-bottom:26px;
border-bottom:1px solid var(--rule);font-size:.83rem}
.nav a{color:var(--ink-mute);text-decoration:none;font-weight:600}
.nav a:hover{color:var(--accent)}
.nav a.on{color:var(--accent)}
.nav a.ext{margin-left:auto;color:var(--ink-mute)}
img{max-width:100%;height:auto;display:block;margin:14px 0;border:1px solid var(--rule);border-radius:5px}
hr{border:0;border-top:1px solid var(--rule);margin:36px 0}
footer{margin-top:70px;padding-top:22px;border-top:1px solid var(--rule);
font-family:var(--mono);font-size:.75rem;color:var(--ink-mute)}
@media(max-width:640px){body{font-size:16px}.wrap{padding:0 16px 70px}.nav a.ext{margin-left:0}}
"""

def wrap_tables(html):
    return re.sub(r'(<table>.*?</table>)', r'<div class="tw">\1</div>', html, flags=re.S)

FOOT = ('<footer>Reproduction of <em>Openpi Comet</em> (arXiv:2512.10071v3) &middot; '
        'empiricist review &middot; sources in '
        '<a href="https://github.com/bushuyeu/openpi-comet">bushuyeu/openpi-comet</a></footer>')

for href, md, label in PAGES:
    body = markdown.markdown(open(os.path.join(SRC, md)).read(),
                             extensions=["tables", "fenced_code", "toc", "sane_lists"])
    body = wrap_tables(body)
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>{} &middot; Openpi Comet reproduction</title><style>{}</style></head><body>'
            '<div class="wrap">{}{}{}</div></body></html>').format(label, CSS, nav(href), body, FOOT)
    open(os.path.join(DOCS, href), "w").write(page)
    print("  wrote docs/{}  ({:,} bytes)".format(href, len(page)))

open(os.path.join(DOCS, ".nojekyll"), "w").write("")
print("  wrote docs/.nojekyll (serve files verbatim, no Jekyll)")
