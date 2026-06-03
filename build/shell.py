# -*- coding: utf-8 -*-
"""Shared layout, icons, navigation and ad units for the AgentHubs site build."""
import json

PUB = "ca-pub-0268893833921284"
DOMAIN = "https://workflow.agenthubs.org"
BRAND = "AgentHubs"
SITE = "AI Workflow ROI Calculator"

# --------------------------------------------------------------------------- icons (inline SVG, stroke style)
ICONS = {
    "calc": '<path d="M7 3h10a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M9 7h6M9 11h1m4 0h1M9 15h1m4 0h1"/>',
    "chart": '<path d="M3 3v18h18"/><rect x="7" y="11" width="3" height="6" rx="1"/><rect x="12" y="7" width="3" height="10" rx="1"/><rect x="17" y="13" width="3" height="4" rx="1"/>',
    "coins": '<circle cx="8" cy="8" r="5"/><path d="M14.5 6.5a5 5 0 1 1 0 11"/><path d="M8 6v4M6.5 8h3"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "rocket": '<path d="M5 15c-1 1-2 4-2 4s3-1 4-2 1-3 0-4-3 1-2 2z"/><path d="M9 11a8 8 0 0 1 7-7c2 0 3 1 3 3a8 8 0 0 1-7 7l-3 1-1-1 1-3z"/><circle cx="14.5" cy="9.5" r="1.5"/>',
    "bot": '<rect x="4" y="8" width="16" height="11" rx="3"/><path d="M12 8V4M8 4h8M9 13h.01M15 13h.01"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 5.5a3.5 3.5 0 0 1 0 7M21 20a6 6 0 0 0-4-5.6"/>',
    "scale": '<path d="M12 3v18M7 21h10"/><path d="M5 7h14M5 7l-2.5 6a3 3 0 0 0 5 0L5 7zm14 0l-2.5 6a3 3 0 0 0 5 0L19 7z"/>',
    "doc": '<path d="M7 3h7l5 5v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "check": '<path d="M4 12a8 8 0 1 1 16 0 8 8 0 0 1-16 0z"/><path d="M9 12l2 2 4-4"/>',
    "spark": '<path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19a2 2 0 0 1 2-2h13"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
    "plug": '<path d="M9 7V3M15 7V3M7 7h10v4a5 5 0 0 1-10 0z"/><path d="M12 16v5"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3 13 9 5 9-5M3 18l9 5 9-5"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M17 7h4v4"/>',
    "shield": '<path d="M12 3l8 3v5c0 5-3.5 8-8 10-4.5-2-8-5-8-10V6l8-3z"/><path d="M9 12l2 2 4-4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "translate": '<path d="M4 5h7M7 4v1c0 3-1.5 6-4 8M5 9c1 2 3 4 5 5"/><path d="m12 20 4-9 4 9M13.5 17h5"/>',
    "tag": '<path d="M3 12V5a2 2 0 0 1 2-2h7l9 9-9 9-9-9z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "puzzle": '<path d="M10 3a2 2 0 1 1 4 0v2h3a1 1 0 0 1 1 1v3h2a2 2 0 1 1 0 4h-2v3a1 1 0 0 1-1 1h-3v-2a2 2 0 1 0-4 0v2H6a1 1 0 0 1-1-1v-3H3a2 2 0 1 1 0-4h2V6a1 1 0 0 1 1-1h3z"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "map": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
}

def icon(name, cls=""):
    body = ICONS.get(name, ICONS["spark"])
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'

# --------------------------------------------------------------------------- primary + sidebar nav
PRIMARY = [
    ("Calculators", "calculators/"),
    ("Tools", "tools/"),
    ("Guides", "guides/"),
    ("Workspace", "workspace/"),
]
SIDEBAR = [
    ("Workspace", [
        ("dashboard", "Dashboard", "", "grid"),
        ("calculators", "Calculators", "calculators/", "calc"),
        ("tools", "Tools", "tools/", "puzzle"),
        ("workspace", "Saved scenarios", "workspace/", "layers"),
        ("reports", "Reports", "reports/", "chart"),
    ]),
    ("Build", [
        ("templates", "Templates", "templates/", "doc"),
        ("examples", "Examples", "examples/", "list"),
        ("settings", "Settings", "settings/", "gear"),
        ("integrations", "Integrations", "integrations/", "plug"),
    ]),
    ("Learn", [
        ("guides", "Guides", "guides/", "book"),
        ("glossary", "Glossary", "glossary/", "search"),
        ("faq", "FAQ", "faq/", "info"),
        ("plans", "Plans", "plans/", "tag"),
    ]),
]

def prefix_for(slug):
    return "" if not slug else "../" * len([s for s in slug.split("/") if s])

def adsense_head():
    return (f'<meta name="google-adsense-account" content="{PUB}">\n'
            f'  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB}" crossorigin="anonymous"></script>')

_ad_n = [1000]
def ad_unit():
    _ad_n[0] += 7
    slot = str(_ad_n[0] * 91 + 100000)
    return ('<aside class="ad-slot in-article" aria-label="Advertisement">'
            '<span class="ad-label">Sponsored</span>'
            f'<ins class="adsbygoogle" style="display:block" data-ad-client="{PUB}" data-ad-slot="{slot}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
            '<script>(adsbygoogle = window.adsbygoogle || []).push({});</script></aside>')

def topbar(pfx):
    links = "".join(f'<a href="{pfx}{href}">{label}</a>' for label, href in PRIMARY)
    return (f'<header class="topbar"><div class="topbar-inner">'
            f'<a class="brand" href="{pfx}"><span class="brand-mark">AH</span><span>{BRAND}<small>AI Ops Toolkit</small></span></a>'
            f'<nav class="nav" aria-label="Primary">{links}'
            f'<a class="cta" href="{pfx}calculators/">Open calculators</a></nav>'
            f'</div></header>')

def sidebar(pfx, active):
    out = ['<aside class="sidebar"><nav class="side-nav-wrap" aria-label="Sections">']
    for group, items in SIDEBAR:
        out.append(f'<div class="side-group"><p>{group}</p><div class="side-nav">')
        for key, label, href, ic in items:
            cur = ' aria-current="page"' if key == active else ""
            out.append(f'<a href="{pfx}{href}"{cur}>{icon(ic)}<span>{label}</span></a>')
        out.append('</div></div>')
    out.append('</nav></aside>')
    return "".join(out)

def footer(pfx):
    cols = [
        ("Calculators", [("AI Workflow ROI", "tool/"), ("LLM Token Cost", "calculators/llm-token-cost/"),
                          ("Automation Savings", "calculators/automation-savings/"), ("Break-even", "calculators/break-even/"),
                          ("All calculators", "calculators/")]),
        ("Learn", [("Guides", "guides/"), ("How to calculate AI ROI", "guides/how-to-calculate-ai-roi/"),
                   ("ROI formulas", "guides/roi-formulas/"), ("Glossary", "glossary/"), ("FAQ", "faq/")]),
        ("Workspace", [("Saved scenarios", "workspace/"), ("Reports", "reports/"), ("Templates", "templates/"),
                       ("Settings", "settings/"), ("Plans", "plans/")]),
    ]
    colhtml = ""
    for title, items in cols:
        lis = "".join(f'<li><a href="{pfx}{h}">{t}</a></li>' for t, h in items)
        colhtml += f'<div><h4>{title}</h4><ul>{lis}</ul></div>'
    return (f'<footer class="footer"><div class="wrap"><div class="footer-grid">'
            f'<div><a class="brand" href="{pfx}"><span class="brand-mark">AH</span><span>{BRAND}<small>AI Ops Toolkit</small></span></a>'
            f'<p>Free, browser-side calculators that turn AI-tool spend, hours saved, and token costs into clear ROI, payback, and cost numbers. No login, no data leaves your device.</p></div>'
            f'{colhtml}</div>'
            f'<div class="footer-bottom"><span>© 2026 {BRAND} · {SITE}</span>'
            f'<span><a href="{pfx}privacy/">Privacy</a> · <a href="{pfx}terms/">Terms</a> · <a href="{pfx}about/">About</a> · <a href="{pfx}contact/">Contact</a></span></div>'
            f'</div></footer>')

def head(title, desc, slug, extra=""):
    pfx = prefix_for(slug)
    canonical = DOMAIN + "/" + (slug + "/" if slug else "")
    return ('<!doctype html>\n<html lang="en">\n<head>\n'
            '  <meta charset="utf-8">\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'  <title>{title}</title>\n'
            f'  <meta name="description" content="{desc}">\n'
            f'  <link rel="canonical" href="{canonical}">\n'
            f'  <meta property="og:title" content="{title}">\n'
            f'  <meta property="og:description" content="{desc}">\n'
            f'  <meta property="og:type" content="website">\n'
            f'  <meta name="theme-color" content="#4f46e5">\n'
            '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;820&display=swap" rel="stylesheet">\n'
            f'  {adsense_head()}\n'
            f'  <link rel="stylesheet" href="{pfx}styles.css">\n'
            f'  {extra}\n'
            '</head>\n')

def site_config_script(cfg):
    return f'<script>window.SITE_CONFIG = {json.dumps(cfg, ensure_ascii=False)};</script>'

def page(title, desc, slug, body, scripts=""):
    pfx = prefix_for(slug)
    return (head(title, desc, slug)
            + "<body>\n" + topbar(pfx) + "\n<main>\n" + body + "\n</main>\n"
            + footer(pfx) + "\n" + scripts + "\n</body>\n</html>")

def app_page(title, desc, slug, active, head_html, body, scripts=""):
    """Sub-page with sidebar app shell."""
    pfx = prefix_for(slug)
    inner = (f'<div class="wrap"><div class="app">{sidebar(pfx, active)}'
             f'<div class="main-col">{head_html}{body}</div></div></div>')
    return (head(title, desc, slug)
            + "<body>\n" + topbar(pfx) + "\n<main>\n" + inner + "\n</main>\n"
            + footer(pfx) + "\n" + scripts + "\n</body>\n</html>")

def breadcrumb(pfx, trail):
    parts = []
    for i, (label, href) in enumerate(trail):
        if href is None:
            parts.append(f'<span>{label}</span>')
        else:
            parts.append(f'<a href="{pfx}{href}">{label}</a>')
        if i < len(trail) - 1:
            parts.append('<span>/</span>')
    return f'<nav class="breadcrumb">{"".join(parts)}</nav>'

def page_head_block(pfx, eyebrow, title, desc, icon_name="calc", trail=None):
    bc = breadcrumb(pfx, trail) if trail else ""
    art = f'<div class="head-art">{icon(icon_name)}</div>'
    return (f'<header class="page-head">{bc}<p class="eyebrow">{eyebrow}</p>'
            f'<h1>{title}</h1><p>{desc}</p></header>')
