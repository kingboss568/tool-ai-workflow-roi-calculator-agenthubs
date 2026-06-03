# -*- coding: utf-8 -*-
"""Build orchestrator: writes the full ~50-page static site."""
import os, json
from shell import (icon, ad_unit, page, app_page, page_head_block, topbar, footer,
                   sidebar, head, site_config_script, prefix_for, breadcrumb, DOMAIN, BRAND, SITE)
import calculators as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TILE = {"ROI & Payback": "brand", "Token & API Cost": "teal", "Workforce & Planning": "amber"}

def tile_of(cat): return TILE.get(cat, "brand")

def related_for(calc):
    same = [c for c in C.CALCS if c["category"] == calc["category"] and c["slug"] != calc["slug"]]
    if len(same) < 3:
        same += [c for c in C.CALCS if c["slug"] != calc["slug"] and c not in same]
    out = []
    for c in same[:3]:
        out.append((c["title"], c["slug"], c["tagline"], c["icon"], tile_of(c["category"])))
    return out

PAGES_FOR_SITEMAP = []
def write(slug, html, priority="0.7"):
    folder = ROOT if slug == "" else os.path.join(ROOT, *slug.split("/"))
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    PAGES_FOR_SITEMAP.append((slug, priority))

# =========================================================================== HERO ART
HERO_ART = '''<div class="hero-art"><div class="glass" data-reveal>
<svg viewBox="0 0 420 300" role="img" aria-label="ROI dashboard illustration" style="border-radius:14px">
  <defs>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6366f1"/><stop offset="1" stop-color="#7c3aed"/></linearGradient>
    <linearGradient id="g2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#2dd4bf"/><stop offset="1" stop-color="#0ea5a4"/></linearGradient>
    <linearGradient id="g3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbbf24"/><stop offset="1" stop-color="#f59e0b"/></linearGradient>
  </defs>
  <rect x="0" y="0" width="420" height="300" rx="16" fill="#fbfcfe"/>
  <rect x="20" y="22" width="180" height="14" rx="7" fill="#e2e8f0"/>
  <rect x="20" y="46" width="120" height="10" rx="5" fill="#eef1f6"/>
  <rect x="20" y="78" width="180" height="120" rx="12" fill="#fff" stroke="#e4e8f0"/>
  <text x="34" y="104" font-family="Inter" font-size="11" fill="#64748b">Net monthly value</text>
  <text x="34" y="138" font-family="Inter" font-weight="800" font-size="26" fill="#4f46e5">$9,060</text>
  <rect x="34" y="156" width="150" height="9" rx="5" fill="#eef1f6"/>
  <rect x="34" y="156" width="120" height="9" rx="5" fill="url(#g1)"/>
  <rect x="34" y="172" width="150" height="9" rx="5" fill="#eef1f6"/>
  <rect x="34" y="172" width="78" height="9" rx="5" fill="url(#g2)"/>
  <rect x="216" y="78" width="184" height="120" rx="12" fill="#fff" stroke="#e4e8f0"/>
  <polyline points="230,176 256,150 282,158 308,120 334,128 360,86 386,72" fill="none" stroke="url(#g1)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="386" cy="72" r="5" fill="#4f46e5"/>
  <rect x="230" y="92" width="80" height="9" rx="5" fill="#eef1f6"/>
  <g>
    <rect x="20" y="214" width="120" height="64" rx="12" fill="url(#g1)"/>
    <text x="34" y="240" font-family="Inter" font-size="10" fill="#e0e7ff">ROI</text>
    <text x="34" y="262" font-family="Inter" font-weight="800" font-size="20" fill="#fff">503%</text>
    <rect x="150" y="214" width="120" height="64" rx="12" fill="#fff" stroke="#e4e8f0"/>
    <text x="164" y="240" font-family="Inter" font-size="10" fill="#64748b">Payback</text>
    <text x="164" y="262" font-family="Inter" font-weight="800" font-size="20" fill="#0ea5a4">2.4 mo</text>
    <rect x="280" y="214" width="120" height="64" rx="12" fill="#fff" stroke="#e4e8f0"/>
    <text x="294" y="240" font-family="Inter" font-size="10" fill="#64748b">Hours / mo</text>
    <text x="294" y="262" font-family="Inter" font-weight="800" font-size="20" fill="#f59e0b">168</text>
  </g>
</svg></div></div>'''

# =========================================================================== HOME
def build_home():
    pfx = ""
    main = next(c for c in C.CALCS if c["slug"] == "ai-workflow-roi")
    cfg = C.calc_config(main)
    cats = [
        ("ROI & Payback", "calc", "brand", "Net value, ROI, payback and break-even for any AI workflow or tool.", "calculators/"),
        ("Token & API Cost", "coins", "teal", "Forecast and compare LLM token, prompt, RAG and provider costs.", "calculators/"),
        ("Workforce & Planning", "users", "amber", "Headcount-equivalent, meeting cost, TCO and capacity planning.", "calculators/"),
    ]
    cat_cards = "".join(
        f'<a class="card hoverable" href="{pfx}{href}" data-reveal><div class="icon-tile tile-{tile}">{icon(ic)}</div><h3>{name}</h3><p>{desc}</p><span class="card-link">Browse {icon("arrow")}</span></a>'
        for name, ic, tile, desc, href in cats)

    featured_slugs = ["llm-token-cost", "automation-savings", "break-even", "chatbot-deflection",
                      "developer-productivity", "api-cost-comparison", "payback-period",
                      "content-generation-roi", "three-year-tco"]
    fmap = {c["slug"]: c for c in C.CALCS}
    feat_cards = "".join(
        f'<a class="card hoverable" href="{pfx}calculators/{s}/"><span class="tag">{fmap[s]["category"]}</span><h3>{fmap[s]["title"]}</h3><p>{fmap[s]["tagline"]}</p><span class="card-link">Open calculator {icon("arrow")}</span></a>'
        for s in featured_slugs)

    steps = [("Enter your numbers", "Type hours saved, run volume, prices, or token counts. Every field has a plain-language hint."),
             ("See the math live", "Net value, ROI, payback and a visual breakdown update instantly as you type — no run button."),
             ("Save, export, decide", "Save named scenarios in your browser, export JSON, or copy a clean summary into your business case.")]
    step_cards = "".join(
        f'<div class="card" data-reveal><div class="icon-tile tile-brand" style="border-radius:999px">{i+1}</div><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(steps))

    hero = f'''<section class="hero"><div class="wrap"><div class="hero-inner">
  <div data-reveal>
    <p class="eyebrow">AI Ops Toolkit · 26 calculators</p>
    <h1>Prove the <span class="grad">ROI of AI</span> before you commit the budget.</h1>
    <p class="lede">A free suite of browser-side calculators that turn hours saved, tool spend, and token prices into clear net value, ROI, payback, and total-cost numbers your finance team will accept.</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="#calculator">Try the ROI calculator {icon("arrow")}</a>
      <a class="btn btn-ghost" href="{pfx}calculators/">Browse all calculators</a>
    </div>
    <div class="trust-row">
      <div><b>26</b><span>Functional calculators</span></div>
      <div><b>100%</b><span>Runs in your browser</span></div>
      <div><b>$0</b><span>Free, no sign-up</span></div>
    </div>
  </div>
  {HERO_ART}
</div></div></section>'''

    calc_section = f'''<section class="section" id="calculator"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Live tool</p><h2>AI Workflow ROI Calculator</h2><p>Adjust the inputs and watch net value, ROI and payback update in real time.</p></div>
  <div class="calc">
    <div class="panel"><div class="panel-head"><h2>Your inputs</h2><span class="chip">{len(main["fields"])} inputs</span></div>
      <div class="panel-body"><div class="fields" id="toolFields"></div></div></div>
    <div class="panel result-panel"><div class="panel-head"><h2>Result</h2>
      <div class="toolbar"><button class="btn btn-ghost btn-sm" id="copyExport" type="button">Copy</button>
      <button class="btn btn-ghost btn-sm" type="button" data-save-current>Save scenario</button>
      <a class="btn btn-primary btn-sm" href="{pfx}tool/">Full tool {icon("arrow")}</a></div></div>
      <div class="panel-body"><div id="toolResult"></div></div></div>
  </div>
</div></section>'''

    cats_section = f'<section class="section" style="background:var(--bg-2)"><div class="wrap"><div class="section-head"><p class="eyebrow">Categories</p><h2>Pick the decision you are modelling</h2><p>Every calculator is genuinely interactive — real formulas, live results, exportable output.</p></div><div class="grid grid-3">{cat_cards}</div></div></section>'

    feat_section = f'<section class="section"><div class="wrap"><div class="section-head"><h2>Popular calculators</h2><p>Nine of the most-used tools in the suite.</p></div><div class="grid grid-3">{feat_cards}</div><div style="text-align:center;margin-top:30px"><a class="btn btn-ghost" href="{pfx}calculators/">See all 26 calculators {icon("arrow")}</a></div></div></section>'

    steps_section = f'<section class="section" style="background:var(--bg-2)"><div class="wrap"><div class="section-head"><p class="eyebrow">How it works</p><h2>From numbers to a decision in three steps</h2></div><div class="grid grid-3">{step_cards}</div></div></section>'

    guides_teaser = f'''<section class="section"><div class="wrap"><div class="section-head"><p class="eyebrow">Learn</p><h2>Guides that make the numbers credible</h2></div>
    <div class="grid grid-3">
      <a class="card hoverable" href="{pfx}guides/how-to-calculate-ai-roi/"><div class="icon-tile tile-brand">{icon("book")}</div><h3>How to calculate AI ROI</h3><p>The full method, the formula, and the assumptions that make or break a case.</p><span class="card-link">Read {icon("arrow")}</span></a>
      <a class="card hoverable" href="{pfx}guides/llm-token-pricing-explained/"><div class="icon-tile tile-teal">{icon("coins")}</div><h3>LLM token pricing explained</h3><p>Input vs output tokens, per-million pricing, and where the bill really comes from.</p><span class="card-link">Read {icon("arrow")}</span></a>
      <a class="card hoverable" href="{pfx}guides/building-the-business-case/"><div class="icon-tile tile-amber">{icon("doc")}</div><h3>Building the business case</h3><p>Turn calculator output into a one-page proposal finance will approve.</p><span class="card-link">Read {icon("arrow")}</span></a>
    </div></div></section>'''

    faq_section = '<section class="section" style="background:var(--bg-2)"><div class="wrap" style="max-width:780px"><div class="section-head"><h2>Frequently asked</h2></div><div id="faq"></div></div></section>'

    body = (hero + f'<div class="wrap">{ad_unit()}</div>' + calc_section + cats_section
            + feat_section + steps_section + f'<div class="wrap">{ad_unit()}</div>' + guides_teaser + faq_section)
    scripts = site_config_script(cfg) + '<script src="app.js"></script><script src="saas.js"></script>'
    html = (head(f"{SITE} — Prove AI ROI Before You Buy | {BRAND}",
                 "Free browser-side AI ROI calculators: net value, payback, token cost, automation savings and more. 26 functional tools, no sign-up.",
                 "")
            + "<body>\n" + topbar(pfx) + "\n<main>\n" + body + "\n</main>\n" + footer(pfx) + "\n" + scripts + "\n</body>\n</html>")
    write("", html, "1.0")

# =========================================================================== FULL TOOL PAGE
def build_tool():
    main = next(c for c in C.CALCS if c["slug"] == "ai-workflow-roi")
    pfx = prefix_for("tool")
    cfg = C.calc_config(main)
    head_block = page_head_block(pfx, "Flagship tool", "AI Workflow ROI Calculator",
                                 "The full ROI workspace — inputs, live results, scenario saving and export.", "calc",
                                 trail=[("Home", ""), ("Tool", None)])
    tool = f'''<section class="calc">
  <div class="panel"><div class="panel-head"><h2>Your inputs</h2><span class="chip">{len(main["fields"])} inputs</span></div>
    <div class="panel-body"><div class="fields" id="toolFields"></div></div></div>
  <div class="panel result-panel"><div class="panel-head"><h2>Result</h2>
    <div class="toolbar"><button class="btn btn-ghost btn-sm" id="copyExport" type="button">Copy</button>
    <button class="btn btn-ghost btn-sm" type="button" data-save-current>Save scenario</button>
    <button class="btn btn-primary btn-sm" type="button" data-download-current>Download JSON</button></div></div>
    <div class="panel-body"><div id="toolResult"></div></div></div>
</section>'''
    method = f'''<section class="panel"><div class="panel-body prose">
  <h2>How the AI Workflow ROI Calculator works</h2>
  <div class="formula">{main["formula"]}</div>{main["about"]}
  <div class="callout"><strong>Tip:</strong> {main["advice"]}</div></div></section>'''
    examples = '<section><div class="section-head left"><h2>Ways to use it</h2><p>Built for repeat decisions.</p></div><div class="grid grid-3" id="examples"></div></section>'
    faq = '<section><div class="section-head left"><h2>Frequently asked</h2></div><div id="faq"></div></section>'
    limits = '<section class="panel"><div class="panel-body prose"><h2>Limits &amp; good practice</h2><ul class="advice-list" id="limits" style="list-style:none"></ul></div></section>'
    body = ad_unit() + tool + method + examples + ad_unit() + faq + limits
    scripts = site_config_script(cfg) + f'<script src="{pfx}app.js"></script><script src="{pfx}saas.js"></script>'
    html = app_page("AI Workflow ROI Calculator — Full Tool | " + BRAND,
                    "The full AI Workflow ROI workspace with live results, scenario saving and JSON export.",
                    "tool", "dashboard", head_block, body, scripts)
    write("tool", html, "0.9")

# =========================================================================== CALCULATORS HUB
def build_calc_hub():
    pfx = prefix_for("calculators")
    cats = {}
    for c in C.CALCS:
        cats.setdefault(c["category"], []).append(c)
    head_block = page_head_block(pfx, "26 functional calculators", "AI ROI & Cost Calculators",
                                 "Every tool runs live in your browser — real formulas, instant results, exportable output. Pick a category below.", "calc",
                                 trail=[("Home", ""), ("Calculators", None)])
    sections = ""
    order = ["ROI & Payback", "Token & API Cost", "Workforce & Planning"]
    for cat in order:
        items = cats.get(cat, [])
        cards = "".join(
            f'<a class="card hoverable" href="{pfx}calculators/{c["slug"]}/"><div class="icon-tile tile-{tile_of(cat)}">{icon(c["icon"])}</div><h3>{c["title"]}</h3><p>{c["tagline"]}</p><span class="card-link">Open {icon("arrow")}</span></a>'
            for c in items)
        sections += f'<section><div class="section-head left"><h2>{cat}</h2><p>{len(items)} calculators</p></div><div class="grid grid-3">{cards}</div></section>'
    body = ad_unit() + sections + ad_unit()
    html = app_page("AI ROI & Cost Calculators — 26 Tools | " + BRAND,
                    "Browse 26 free AI ROI and cost calculators: net value, payback, token cost, automation savings, TCO and more.",
                    "calculators", "calculators", head_block, body,
                    f'<script src="{pfx}saas.js"></script>')
    write("calculators", html, "0.9")

# =========================================================================== CALCULATOR PAGES
def build_calcs():
    for c in C.CALCS:
        html = C.render_calc(c, related_for(c))
        write("calculators/" + c["slug"], html, "0.8")

# =========================================================================== TOOLS
def tool_page(slug, title, tagline, icon_name, chip, cfg, body_extra, prose):
    pfx = prefix_for("tools/" + slug)
    head_block = page_head_block(pfx, "Interactive tool", title, tagline, icon_name,
                                 trail=[("Home", ""), ("Tools", "tools/"), (title, None)])
    tool = f'''<section class="calc">
  <div class="panel"><div class="panel-head"><h2>Inputs</h2><span class="chip">{chip}</span></div>
    <div class="panel-body"><div class="fields" id="toolFields"></div></div></div>
  <div class="panel result-panel"><div class="panel-head"><h2>Result</h2>
    <div class="toolbar"><button class="btn btn-ghost btn-sm" id="copyExport" type="button">Copy</button>
    <button class="btn btn-ghost btn-sm" type="button" data-save-current>Save scenario</button>
    <button class="btn btn-primary btn-sm" type="button" data-download-current>Download JSON</button></div></div>
    <div class="panel-body"><div id="toolResult"></div></div></div>
</section>'''
    method = f'<section class="panel"><div class="panel-body prose">{prose}</div></section>'
    body = ad_unit() + tool + body_extra + method + ad_unit()
    scripts = site_config_script(cfg) + f'<script src="{pfx}app.js"></script><script src="{pfx}saas.js"></script>'
    html = app_page(title + " | " + BRAND, tagline[:155], "tools/" + slug, "tools", head_block, body, scripts)
    write("tools/" + slug, html, "0.8")

def build_tools():
    # hub
    pfx = prefix_for("tools")
    tools = [
        ("comparison-matrix", "AI Tool Comparison Matrix", "Score and rank AI tools or vendors on weighted criteria.", "grid", "teal"),
        ("readiness-checklist", "AI Readiness Checklist", "Score how ready a workflow is to automate and surface the gaps.", "check", "brand"),
        ("business-case-builder", "AI Business Case Builder", "Generate a one-page business case draft from your numbers.", "doc", "amber"),
    ]
    cards = "".join(
        f'<a class="card hoverable" href="{pfx}tools/{s}/"><div class="icon-tile tile-{tile}">{icon(ic)}</div><h3>{t}</h3><p>{d}</p><span class="card-link">Open {icon("arrow")}</span></a>'
        for s, t, d, ic, tile in tools)
    head_block = page_head_block(pfx, "Interactive tools", "Decision Tools",
                                 "Beyond calculators — score vendors, check readiness, and draft your business case.", "puzzle",
                                 trail=[("Home", ""), ("Tools", None)])
    body = ad_unit() + f'<section><div class="grid grid-3">{cards}</div></section>'
    html = app_page("AI Decision Tools | " + BRAND, "Interactive AI decision tools: comparison matrix, readiness checklist, and business case builder.",
                    "tools", "tools", head_block, body, f'<script src="{pfx}saas.js"></script>')
    write("tools", html, "0.8")

    # comparison matrix (kind matrix)
    cfg_m = {"title": "AI Tool Comparison Matrix", "kind": "matrix",
             "fields": [{"id": "rows", "label": "Options (one per line: Name, Impact, Cost-efficiency, Ease)",
                         "type": "textarea", "rows": 8, "wide": True,
                         "default": "Copilot, 8, 6, 9\nClaude, 9, 7, 8\nIn-house RAG, 7, 9, 5"}],
             "engine": {"weights": {"Impact": 0.45, "Cost-efficiency": 0.3, "Ease": 0.25}},
             "examples": [], "faq": [], "limits": C.LIMITS}
    prose_m = ('<h2>How scoring works</h2><div class="formula"><b>Score</b> = Impact×0.45 + Cost-efficiency×0.30 + Ease×0.25</div>'
               '<p>Enter one option per line as <code>Name, Impact, Cost-efficiency, Ease</code> using a 0–10 scale. Each option is scored against the weighted criteria and ranked highest-first, so the strongest overall choice rises to the top.</p>'
               '<div class="callout"><strong>Tip:</strong> change the criteria meaning to match your decision — the weights stay fixed at 45/30/25, so map your most important factor to Impact.</div>')
    tool_page("comparison-matrix", "AI Tool Comparison Matrix",
              "Score and rank AI tools or vendors on weighted Impact, Cost-efficiency and Ease.",
              "grid", "Weighted scoring", cfg_m, "", prose_m)

    # readiness checklist (kind checklist)
    items = [
        ("The task is repetitive and high-volume", "Manual, repeated work", 3),
        ("Inputs and outputs are well defined", "Clear data contract", 2),
        ("There is enough historical data or examples", "Training / context ready", 2),
        ("A human review step is in place", "Quality gate exists", 2),
        ("Success metrics are agreed", "Measurable outcome", 2),
        ("Stakeholders are aligned on scope", "No scope drift", 1),
        ("Data privacy and compliance are checked", "Legal / security clear", 3),
        ("Error handling and fallbacks are designed", "Graceful failure", 2),
        ("Budget covers running cost, not just setup", "Sustainable funding", 2),
        ("An owner is accountable post-launch", "Clear ownership", 1),
    ]
    cfg_c = {"title": "AI Readiness Checklist", "kind": "checklist",
             "fields": [{"id": "items", "label": "Items still open (unchecked = a gap)", "type": "checklist", "wide": True,
                         "options": [t for t, _, _ in items], "default": [t for t, _, _ in items][:4]}],
             "data": {"items": [{"title": t, "note": n, "category": "Readiness", "weight": w} for t, n, w in items]},
             "examples": [], "faq": [], "limits": C.LIMITS}
    prose_c = ('<h2>How the score works</h2><p>Tick every item that is <strong>still open</strong>. Each open item carries a risk weight; the readiness score is 100% minus your share of total risk. Aim to close the heaviest items — privacy, repetitiveness, and human review — before you build.</p>'
               '<div class="callout"><strong>Tip:</strong> a score below 60% means scope or data work is needed before automation will pay off.</div>')
    tool_page("readiness-checklist", "AI Readiness Checklist",
              "Score how ready a workflow is to automate and surface the highest-risk gaps.",
              "check", "10-point scorer", cfg_c, "", prose_c)

    # business case builder (kind builder)
    cfg_b = {"title": "AI Business Case Builder", "kind": "builder",
             "fields": [
                 {"id": "project", "label": "Project name", "type": "text", "default": "Support copilot rollout", "wide": True},
                 {"id": "problem", "label": "Problem", "type": "textarea", "rows": 2, "default": "Agents spend hours on repetitive tier-1 tickets."},
                 {"id": "monthlyValue", "label": "Monthly value ($)", "type": "number", "default": 9000, "money": True},
                 {"id": "monthlyCost", "label": "Monthly cost ($)", "type": "number", "default": 1500, "money": True},
                 {"id": "setup", "label": "Setup cost ($)", "type": "number", "default": 12000, "money": True},
             ],
             "engine": {"sections": [
                 {"title": "{{project}} — Business Case", "body": "Problem: {{problem}}\nProposed solution: an AI-assisted workflow to remove repetitive effort and reclaim capacity."},
                 {"title": "The numbers", "body": "Estimated monthly value: ${{monthlyValue}}\nEstimated monthly cost: ${{monthlyCost}}\nOne-time setup: ${{setup}}\nNet monthly benefit is the value minus the running cost; payback is setup divided by that net benefit."},
                 {"title": "Recommendation", "body": "Approve a time-boxed pilot, instrument the success metric, and review actuals against this projection before scaling."},
             ]},
             "examples": [], "faq": [], "limits": C.LIMITS}
    prose_b = ('<h2>From numbers to a one-pager</h2><p>Fill in the problem and the headline figures and the builder assembles a clean, copyable business-case draft — problem, numbers, and a recommendation. Use the Copy or Download buttons to drop it into a doc and refine.</p>'
               '<div class="callout"><strong>Tip:</strong> pair this with the <a href="../../calculators/payback-period/">Payback Period</a> and <a href="../../calculators/break-even/">Break-even</a> calculators to back the numbers.</div>')
    tool_page("business-case-builder", "AI Business Case Builder",
              "Generate a one-page AI business case draft from your problem statement and numbers.",
              "doc", "Document generator", cfg_b, "", prose_b)

# =========================================================================== GUIDES
GUIDES = []
def guide(slug, title, desc, icon_name, html):
    GUIDES.append((slug, title, desc, icon_name, html))

guide("how-to-calculate-ai-roi", "How to Calculate AI ROI",
      "A step-by-step method for turning AI tool spend and hours saved into a defensible ROI number.", "calc",
      """<h2>What ROI really measures</h2>
<p>Return on investment compares the value an initiative creates against what it costs. For AI workflows the value is almost always <em>reclaimed time</em> or <em>avoided cost</em>, and the cost is the subscription, usage, and the people who run the system. Get those two halves right and the ratio takes care of itself.</p>
<div class="formula"><b>ROI %</b> = (net benefit ÷ cost) × 100, where net benefit = value created − cost</div>
<h2>Step 1 — quantify the value</h2>
<p>Start with the unit of work the AI touches: a ticket, a draft, a translation, a code change. Estimate how much time or money the AI removes from each unit, then multiply by volume. Use a <strong>loaded</strong> hourly rate — salary plus benefits and overhead — because that is the true cost of the time you free up.</p>
<h2>Step 2 — count every cost</h2>
<p>List the subscription, per-token or per-call usage, integration and build effort, and ongoing maintenance. The most common mistake is counting only the licence fee and ignoring the engineer who keeps the pipeline alive.</p>
<h2>Step 3 — pick the right time horizon</h2>
<p>Monthly net value answers "does this pay each month?"; payback period answers "when do we recoup the build?"; three-year TCO answers "what does owning this really cost?". Strong cases show all three.</p>
<div class="callout">Run the numbers in the <a href="../../tool/">AI Workflow ROI Calculator</a> and save each scenario so you can compare conservative, expected, and optimistic cases.</div>
<h2>Step 4 — stress-test the assumptions</h2>
<p>Cut your value estimate by a third and double your cost estimate. If the case still holds, it is robust. If it collapses, you have found the assumption that needs real measurement before you commit budget.</p>""")

guide("llm-token-pricing-explained", "LLM Token Pricing Explained",
      "Input vs output tokens, per-million pricing, and the levers that actually move your bill.", "coins",
      """<h2>What a token is</h2>
<p>A token is a chunk of text — roughly ¾ of a word in English. Models bill by the token, and a single request is charged for both the tokens you send (input) and the tokens it generates (output).</p>
<div class="formula"><b>Request cost</b> = input÷1,000,000 × in-price + output÷1,000,000 × out-price</div>
<h2>Why output is the expensive half</h2>
<p>Output tokens typically cost three to five times more than input tokens. A verbose model that writes long answers can quietly double your bill even when prompts are short. Capping response length is often the single biggest saving available.</p>
<h2>Per-million pricing</h2>
<p>Prices are quoted per one million tokens because per-token numbers are unreadably small. To forecast spend, estimate average input and output size, multiply by monthly request volume, and apply both prices. The <a href="../../calculators/llm-token-cost/">LLM Token Cost Calculator</a> does this instantly.</p>
<h2>The levers that matter</h2>
<ul><li><strong>Trim prompts:</strong> remove boilerplate and redundant context.</li><li><strong>Cap output:</strong> set max tokens and ask for concise answers.</li><li><strong>Cache context:</strong> reuse retrieved or system content instead of resending it.</li><li><strong>Right-size the model:</strong> a smaller model at lower price often clears the quality bar.</li></ul>
<div class="callout">Comparing two providers? The <a href="../../calculators/api-cost-comparison/">API Cost Comparison</a> runs your real traffic through both price tables.</div>""")

guide("roi-formulas", "The AI ROI Formula Reference",
      "Every formula this site uses — ROI, payback, break-even, NPV-style projection — in one place.", "list",
      """<h2>Core formulas</h2>
<div class="formula"><b>Net monthly value</b> = (hours saved × runs × hourly value) − tool cost</div>
<div class="formula"><b>ROI %</b> = (net benefit ÷ cost) × 100</div>
<div class="formula"><b>Payback (months)</b> = investment ÷ net monthly benefit</div>
<div class="formula"><b>Break-even (months)</b> = upfront cost ÷ (monthly benefit − monthly running cost)</div>
<h2>Cost formulas</h2>
<div class="formula"><b>Token cost</b> = requests × (in÷1M × in-price + out÷1M × out-price)</div>
<div class="formula"><b>Cost per conversation</b> = (token cost + platform fee) ÷ conversations</div>
<div class="formula"><b>3-year TCO</b> = setup + monthly × 12 × (1 + (1+g) + (1+g)²)</div>
<h2>Capacity formulas</h2>
<div class="formula"><b>FTE equivalent</b> = hours automated ÷ productive hours per FTE</div>
<div class="formula"><b>Growing savings total</b> = saving × ((1+g)ⁿ − 1) ÷ g</div>
<h2>Choosing the right one</h2>
<p>Use <strong>net value</strong> for an ongoing-benefit case, <strong>payback</strong> and <strong>break-even</strong> when there is a meaningful upfront cost, and <strong>TCO</strong> for multi-year vendor comparisons. Capacity formulas translate hours into headcount language for leadership.</p>
<div class="callout">Each formula has a dedicated calculator. Browse them all on the <a href="../../calculators/">calculators page</a>.</div>""")

guide("ai-cost-optimization", "AI Cost Optimization Playbook",
      "Practical tactics to cut LLM and automation cost without hurting quality.", "trend",
      """<h2>Measure before you optimise</h2>
<p>You cannot cut what you cannot see. Break spend into token cost, platform fees, and human review time using the <a href="../../calculators/cost-per-conversation/">cost-per-conversation</a> and <a href="../../calculators/rag-pipeline-cost/">RAG pipeline</a> calculators before changing anything.</p>
<h2>Tactic 1 — shrink the prompt</h2>
<p>Long system prompts and oversized retrieved context inflate input tokens on every single call. Trim boilerplate, lower top-k retrieval, and tune chunk size.</p>
<h2>Tactic 2 — cap and shape output</h2>
<p>Set max tokens and instruct the model to be concise. Output is the priciest half of the bill, so this is usually the fastest win.</p>
<h2>Tactic 3 — match the model to the task</h2>
<p>Route simple requests to a cheaper, faster model and reserve the flagship model for hard cases. A tiered approach can halve cost at equal quality.</p>
<h2>Tactic 4 — decide flat vs usage</h2>
<p>As volume grows, a flat plan can beat pay-as-you-go — or the reverse. Re-check the crossover with the <a href="../../calculators/subscription-vs-usage/">subscription vs usage</a> tool whenever traffic shifts.</p>
<h2>Tactic 5 — consider fine-tuning at scale</h2>
<p>High request volume can amortise a one-time training cost into much shorter prompts. The <a href="../../calculators/fine-tuning-vs-prompting/">fine-tuning vs prompting</a> calculator shows the payback.</p>
<div class="callout">Optimise in order of impact: output length, prompt size, model choice, pricing model, then architecture.</div>""")

guide("measuring-productivity-gains", "Measuring AI Productivity Gains",
      "How to measure real productivity uplift instead of trusting vendor claims.", "rocket",
      """<h2>Why measurement matters</h2>
<p>Productivity uplift is the most abused number in AI business cases. Vendors quote best-case studies; reality depends on your team, task, and adoption. A 15% claim that turns out to be 4% can flip a project from winner to loser.</p>
<h2>Pick a hard metric</h2>
<p>Choose something countable: tickets resolved per hour, cycle time per pull request, drafts shipped per week, words translated per day. Avoid vague self-reported "time saved" surveys as your only evidence.</p>
<h2>Run a controlled pilot</h2>
<p>Measure a baseline for two to four weeks, introduce the AI tool to a subset of the team, and compare. Keep the work type constant so you isolate the tool's effect.</p>
<h2>Convert to dollars carefully</h2>
<p>Reclaimed time only becomes value if it is redeployed to useful work. Multiply measured uplift by loaded salary in the <a href="../../calculators/developer-productivity/">developer productivity</a> or <a href="../../calculators/automation-savings/">automation savings</a> calculators, and state the redeployment assumption explicitly.</p>
<div class="callout">A defensible case uses <em>your</em> measured uplift, not the vendor's. Pilot first, project second.</div>""")

guide("building-the-business-case", "Building the AI Business Case",
      "Turn calculator output into a one-page proposal that finance will approve.", "doc",
      """<h2>The one-page structure</h2>
<p>A strong AI business case fits on a page: the problem, the proposed workflow, the numbers, the risks, and a clear ask. Brevity signals confidence.</p>
<h2>Lead with the net number</h2>
<p>Open with net monthly value or first-year ROI — the single figure that matters. Back it with payback period so the reader knows when the spend is recovered.</p>
<h2>Show three scenarios</h2>
<p>Present conservative, expected, and optimistic cases. Saving each as a named scenario in the <a href="../../workspace/">workspace</a> makes this trivial and signals rigour.</p>
<h2>Name the assumptions</h2>
<p>List the two or three numbers the case hinges on — uplift, adoption, price — and where each came from. Reviewers trust a case that volunteers its own weak points.</p>
<h2>Make the ask specific</h2>
<p>Request a time-boxed pilot with a named owner and a success metric, not open-ended approval. Smaller asks get approved faster and de-risk the rollout.</p>
<div class="callout">Draft the page automatically with the <a href="../../tools/business-case-builder/">Business Case Builder</a>, then refine the wording.</div>""")

guide("benchmarks", "AI ROI Benchmarks & Assumptions",
      "Reasonable starting ranges for the inputs every AI ROI model needs.", "chart",
      """<h2>Use ranges, not single guesses</h2>
<p>Benchmarks are starting points, not facts. Always replace them with your own measurements before presenting. The ranges below are typical, broad, and meant only to sanity-check your inputs.</p>
<h2>Common input ranges</h2>
<div class="table-wrap"><table><thead><tr><th>Input</th><th>Typical range</th><th>Notes</th></tr></thead><tbody>
<tr><td>Support deflection rate</td><td>20–45%</td><td>Depends on knowledge-base quality and query mix.</td></tr>
<tr><td>Developer productivity uplift</td><td>5–20%</td><td>Measure from delivery metrics, never vendor claims.</td></tr>
<tr><td>Content drafting time saved</td><td>40–70%</td><td>Editing still required; rarely full elimination.</td></tr>
<tr><td>Translation post-edit share</td><td>50–100%</td><td>Higher for regulated or brand-critical content.</td></tr>
<tr><td>Tokens per English word</td><td>1.3–1.5</td><td>Use ~1.33 as a planning default.</td></tr>
<tr><td>Output vs input token price</td><td>3–5×</td><td>Output is the expensive half of the bill.</td></tr>
</tbody></table></div>
<h2>Loaded cost multipliers</h2>
<p>A fully-loaded employee cost is commonly 1.25–1.4× base salary once benefits and overhead are included. Use the loaded figure in every value calculation.</p>
<div class="callout">Plug these into the matching calculator, then tighten each number with real data from a pilot.</div>""")

def build_guides():
    pfx = prefix_for("guides")
    cards = "".join(
        f'<a class="card hoverable" href="{pfx}guides/{s}/"><div class="icon-tile tile-brand">{icon(ic)}</div><h3>{t}</h3><p>{d}</p><span class="card-link">Read {icon("arrow")}</span></a>'
        for s, t, d, ic, _ in GUIDES)
    head_block = page_head_block(pfx, "Learn", "Guides & Methodology",
                                 "The thinking behind the numbers — formulas, pricing, measurement, and how to win approval.", "book",
                                 trail=[("Home", ""), ("Guides", None)])
    body = ad_unit() + f'<section><div class="grid grid-3">{cards}</div></section>'
    html = app_page("AI ROI Guides & Methodology | " + BRAND,
                    "Guides on calculating AI ROI, LLM token pricing, cost optimization, measuring productivity, and building the business case.",
                    "guides", "guides", head_block, body, f'<script src="{pfx}saas.js"></script>')
    write("guides", html, "0.8")

    for i, (s, t, d, ic, content) in enumerate(GUIDES):
        pfx2 = prefix_for("guides/" + s)
        head_block = page_head_block(pfx2, "Guide", t, d, ic,
                                     trail=[("Home", ""), ("Guides", "guides/"), (t, None)])
        # related guides
        rel = [g for g in GUIDES if g[0] != s][:3]
        rel_cards = "".join(f'<a class="card hoverable" href="{pfx2}guides/{rs}/"><h3>{rt}</h3><p>{rd}</p><span class="card-link">Read {icon("arrow")}</span></a>' for rs, rt, rd, ric, _ in rel)
        body = (ad_unit() + f'<article class="panel"><div class="panel-body prose">{content}</div></article>'
                + ad_unit()
                + f'<section><div class="section-head left"><h2>More guides</h2></div><div class="grid grid-3">{rel_cards}</div></section>')
        html = app_page(t + " | " + BRAND, d, "guides/" + s, "guides", head_block, body,
                        f'<script src="{pfx2}saas.js"></script>')
        write("guides/" + s, html, "0.7")

# =========================================================================== GLOSSARY
def build_glossary():
    pfx = prefix_for("glossary")
    terms = [
        ("ROI", "ROI", "Return on investment — net benefit divided by cost, expressed as a percentage.", "Headline metric for any AI business case."),
        ("Payback period", "Metric", "The time for cumulative net returns to repay the initial investment.", "Use when there is a meaningful upfront cost."),
        ("Break-even", "Metric", "The point where cumulative benefit equals cumulative cost.", "Months until the project stops losing money."),
        ("Token", "LLM", "A chunk of text, roughly ¾ of a word, that models read and bill by.", "The unit of LLM pricing."),
        ("Input tokens", "LLM", "Tokens you send to the model — prompt plus context.", "Cheaper half of the bill."),
        ("Output tokens", "LLM", "Tokens the model generates in its response.", "Usually 3–5× the price of input."),
        ("Per-million pricing", "LLM", "Model prices quoted per 1,000,000 tokens.", "Multiply by token volume to forecast spend."),
        ("Loaded cost", "Finance", "Salary plus benefits and overhead — the true cost of an hour of work.", "Use this, not raw wage, in value calculations."),
        ("FTE", "Workforce", "Full-time equivalent — one person's worth of productive capacity.", "Translates automated hours into headcount."),
        ("TCO", "Finance", "Total cost of ownership including setup, usage, and maintenance over time.", "Fair basis for multi-year vendor comparison."),
        ("Deflection rate", "Support", "Share of support contacts resolved without a human agent.", "Key driver of chatbot savings."),
        ("RAG", "LLM", "Retrieval-augmented generation — answering with retrieved context.", "Has embedding and generation cost centres."),
        ("Fine-tuning", "LLM", "Training a model on your data to specialise it.", "Trades fixed cost for shorter prompts."),
        ("Embedding", "LLM", "A numeric vector representing text for search and retrieval.", "Cheap per token; powers RAG retrieval."),
        ("Prompt", "LLM", "The instruction and context sent to a model.", "Prompt size directly affects input cost."),
        ("Net benefit", "Finance", "Value created minus the cost to create it.", "The numerator of the ROI ratio."),
        ("Utilisation", "Workforce", "Share of paid time spent on productive work.", "Lowers real productive hours per FTE."),
        ("Overage", "Pricing", "Per-unit charge for usage beyond a plan allowance.", "Can erase the saving of a flat plan."),
        ("Post-editing", "Translation", "Human correction of machine-translated text.", "Added only on the share that needs it."),
        ("Crossover point", "Pricing", "Volume at which one pricing model becomes cheaper than another.", "Recompute when traffic changes."),
    ]
    cfg = {"title": "AI ROI Glossary", "kind": "library",
           "fields": [
               {"id": "query", "label": "Search terms", "type": "text", "default": "", "hint": "Type to filter the glossary", "wide": True},
               {"id": "category", "label": "Category", "type": "select",
                "options": ["All", "Metric", "Finance", "LLM", "Workforce", "Support", "Pricing", "Translation", "ROI"], "default": "All"},
           ],
           "data": {"items": [{"title": t, "category": cat, "note": note, "use": use} for t, cat, note, use in terms]},
           "examples": [], "faq": [], "limits": C.LIMITS}
    head_block = page_head_block(pfx, "Reference", "AI ROI Glossary",
                                 "Plain-language definitions for every term used across the calculators and guides. Search live.", "search",
                                 trail=[("Home", ""), ("Glossary", None)])
    tool = '''<section class="panel"><div class="panel-head"><h2>Search the glossary</h2><span class="chip">''' + str(len(terms)) + ''' terms</span></div>
      <div class="panel-body"><div class="fields" id="toolFields"></div><div id="toolResult" style="margin-top:18px"></div></div></section>'''
    body = ad_unit() + tool + ad_unit()
    scripts = site_config_script(cfg) + f'<script src="{pfx}app.js"></script><script src="{pfx}saas.js"></script>'
    html = app_page("AI ROI Glossary — 20 Terms Defined | " + BRAND,
                    "Searchable glossary of AI ROI, LLM token, and finance terms: ROI, payback, tokens, TCO, FTE, RAG and more.",
                    "glossary", "glossary", head_block, body, scripts)
    write("glossary", html, "0.7")

# =========================================================================== SAAS / SITE PAGES
def simple(slug, active, eyebrow, title, desc, icon_name, inner, trail_label, with_saas=True, extra_script=""):
    pfx = prefix_for(slug)
    head_block = page_head_block(pfx, eyebrow, title, desc, icon_name,
                                 trail=[("Home", ""), (trail_label, None)])
    body = ad_unit() + inner
    scripts = (f'<script src="{pfx}saas.js"></script>' if with_saas else "") + extra_script
    html = app_page(title + " | " + BRAND, desc[:155], slug, active, head_block, body, scripts)
    write(slug, html, "0.6")

def build_site_pages():
    # workspace
    simple("workspace", "workspace", "Workspace", "Saved Scenarios",
           "Your saved calculator scenarios live here, stored privately in this browser. Open a calculator and press Save scenario to add one.",
           "layers",
           '<section><div class="two-col grid grid-2"><article class="card"><h3>How it works</h3><p>Every calculator has a <strong>Save scenario</strong> button. Saved runs appear below with their exported summary, ready to re-download as JSON.</p></article>'
           '<article class="card"><h3>Private by design</h3><p>Scenarios are stored in your browser only. Nothing is uploaded, and clearing browser data removes them.</p></article></div></section>'
           '<section><div class="section-head left"><h2>Saved scenarios <span data-project-count>0</span></h2></div><div class="grid grid-3" data-project-list></div></section>',
           "Workspace")
    # reports
    simple("reports", "reports", "Reports", "Scenario Reports",
           "Review and export every scenario you have saved, or clear them all in one click.", "chart",
           '<section><div class="toolbar"><button class="btn btn-ghost btn-sm" data-clear-projects>Clear all scenarios</button></div></section>'
           '<section><div class="grid grid-3" data-project-list></div></section>',
           "Reports")
    # templates
    tpls = [("Starter ROI brief", "ai-workflow-roi", "A clean net-value, ROI and payback summary for any workflow."),
            ("Token budget", "llm-token-cost", "Monthly input/output token spend with a cost-per-request breakdown."),
            ("Automation case", "automation-savings", "Reclaimed hours and annual value from a repetitive task."),
            ("Support savings", "chatbot-deflection", "Net savings from deflecting a share of tickets."),
            ("Vendor comparison", "api-cost-comparison", "Two providers compared on identical traffic."),
            ("Coding assistant", "developer-productivity", "Team-level productivity ROI for an AI pair-programmer."),
            ("Break-even plan", "break-even", "Months until benefit covers your upfront investment."),
            ("3-year TCO", "three-year-tco", "Multi-year total cost with growth for vendor reviews."),
            ("Content pipeline", "content-generation-roi", "Manual vs AI-assisted content cost and time."),
            ("Conversation cost", "cost-per-conversation", "True per-conversation unit economics."),
            ("Translation savings", "translation-savings", "Human vs AI-plus-post-edit across word volume."),
            ("Headcount equivalent", "headcount-equivalent", "Automated hours expressed as FTE capacity.")]
    cards = "".join(
        f'<article class="card" data-template-card><span class="tag">Template</span><h3>{t}</h3><p>{d}</p><a class="card-link" href="../calculators/{s}/">Open calculator {icon("arrow")}</a></article>'
        for t, s, d in tpls)
    simple("templates", "templates", "Build", "Templates",
           "Pre-framed starting points that route you to the right calculator for a common job.", "doc",
           f'<section><div class="toolbar"><input data-template-search type="search" placeholder="Search templates…"></div></section>'
           f'<section><div class="grid grid-3">{cards}</div></section>',
           "Templates")
    # examples
    exs = [("Justify a Copilot rollout", "Use developer productivity ROI with a measured uplift, then a break-even on the seat cost."),
           ("Size a support bot", "Combine chatbot deflection savings with cost per conversation to see net impact and unit cost."),
           ("Choose a model provider", "Run identical traffic through the API cost comparison, then sanity-check with token cost."),
           ("Plan a RAG launch", "Estimate RAG pipeline cost, then convert to cost per conversation for a per-query budget."),
           ("Build a 3-year case", "Project 3-year TCO against an annual savings projection for a true multi-year ROI."),
           ("Decide flat vs usage", "Find your crossover point with subscription vs usage before signing a plan.")]
    ex_cards = "".join(f'<article class="card"><h3>{t}</h3><p>{d}</p></article>' for t, d in exs)
    simple("examples", "examples", "Build", "Worked Examples",
           "Real decisions and which combination of calculators answers them.", "list",
           f'<section><div class="grid grid-3">{ex_cards}</div></section>', "Examples")
    # settings
    simple("settings", "settings", "Build", "Settings",
           "Local preferences for currency and workspace naming. Stored in this browser only.", "gear",
           '<section class="panel"><div class="panel-body"><div class="mini-form" style="display:grid;gap:14px;max-width:520px">'
           '<label class="field"><span>Workspace name</span><input data-setting="workspaceName" data-default="My workspace"></label>'
           '<label class="field"><span>Currency</span><select data-setting="currency" data-default="USD"><option>USD</option><option>TWD</option><option>EUR</option><option>JPY</option><option>GBP</option></select></label>'
           '<label class="field"><span>Notes</span><textarea data-setting="notes" data-default="" rows="4"></textarea></label>'
           '<div class="toolbar"><button class="btn btn-primary" data-save-settings>Save settings</button><span class="hint" data-settings-status></span></div>'
           '</div><p class="hint" style="margin-top:14px">Currency changes the symbol used across all calculators.</p></div></section>',
           "Settings")
    # integrations
    simple("integrations", "integrations", "Build", "Integrations & Export",
           "Export formats today, and where this fits a larger workflow tomorrow.", "plug",
           '<section><div class="grid grid-2">'
           '<article class="card"><h3>Export formats</h3><p>Copy a clean text summary, download structured JSON, or save named scenarios in your browser workspace.</p></article>'
           '<article class="card"><h3>Drop into a sheet</h3><p>JSON exports map cleanly to spreadsheet columns for further modelling or board reporting.</p></article>'
           '<article class="card"><h3>No secrets required</h3><p>This static toolkit never asks for API keys, passwords, or credentials — there is no backend to send them to.</p></article>'
           '<article class="card"><h3>Roadmap</h3><p>Cloud scenario history, team sharing, and CSV batch runs are on the roadmap once usage justifies a backend.</p></article>'
           '</div></section>', "Integrations")
    # plans
    simple("plans", "plans", "Learn", "Plans",
           "What is free today and what a future Pro tier could add. No checkout, no dark patterns.", "tag",
           '<section><div class="grid grid-3">'
           f'<article class="card"><span class="tag">Current</span><h3>Free toolkit</h3><p>All 26 calculators, 3 decision tools, guides, glossary, browser workspace, and JSON export — completely free.</p><a class="card-link" href="../calculators/">Start now {icon("arrow")}</a></article>'
           '<article class="card"><span class="tag">Roadmap</span><h3>Pro workspace</h3><p>Cloud scenario history, team templates, CSV batch runs, and shareable report links once traffic justifies a backend.</p></article>'
           '<article class="card"><span class="tag">Always</span><h3>Privacy first</h3><p>Core calculators will always run client-side. Your numbers stay yours.</p></article>'
           '</div></section>', "Plans")
    # faq
    faqs = [("Is everything really free?", "Yes. All 26 calculators and 3 tools are free with no sign-up. The site is supported by ads."),
            ("Where is my data stored?", "In your browser's local storage. Nothing is uploaded to a server — calculations run entirely client-side."),
            ("How accurate are the results?", "The math is exact. Accuracy depends on your inputs, so validate rates, prices, and adoption with your own data."),
            ("Can I use this for work?", "Yes. Treat outputs as a rigorous first pass for a business case, then confirm assumptions before presenting."),
            ("Do you store my saved scenarios?", "No. Saved scenarios live only in the browser you used. Clearing site data removes them."),
            ("Which calculator should I start with?", "The AI Workflow ROI Calculator covers the most common case. Browse the categories for specific decisions.")]
    faq_html = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    simple("faq", "faq", "Learn", "Frequently Asked Questions",
           "Answers about pricing, privacy, accuracy, and how to use the toolkit.", "info",
           f'<section style="max-width:780px">{faq_html}</section>', "FAQ")
    # about
    simple("about", "dashboard", "Company", "About AgentHubs",
           "Why we built a free, privacy-first suite of AI ROI calculators.", "info",
           '<section class="panel"><div class="panel-body prose">'
           '<h2>The problem we kept hitting</h2><p>Every team adopting AI faces the same question from finance: <em>what is the return?</em> The answers were scattered across spreadsheets, vendor decks, and back-of-napkin math. We built AgentHubs to make those calculations fast, consistent, and credible.</p>'
           '<h2>Our principles</h2><ul><li><strong>Functional, not filler:</strong> every page is a working tool, not a wall of text.</li><li><strong>Privacy first:</strong> calculations run in your browser; your numbers never leave your device.</li><li><strong>Honest math:</strong> formulas are shown, assumptions are surfaced, and limits are stated.</li></ul>'
           '<h2>Who it is for</h2><p>Operators, founders, finance partners, and engineers who need a defensible number before committing budget to an AI initiative.</p>'
           '<div class="callout">Have feedback or a calculator request? Visit the <a href="../contact/">contact page</a>.</div>'
           '</div></section>', "About")
    # changelog
    cl = [("2026-06", "Major expansion", "Launched 26 functional calculators, 3 decision tools, 7 guides, and a searchable glossary with a redesigned interface."),
          ("2026-05", "Workspace & export", "Added browser-side scenario saving, JSON export, and currency settings."),
          ("2026-04", "Initial launch", "Released the first AI Workflow ROI Calculator pilot.")]
    cl_html = "".join(f'<article class="card"><span class="tag">{d}</span><h3>{t}</h3><p>{b}</p></article>' for d, t, b in cl)
    simple("changelog", "dashboard", "Company", "Changelog",
           "What we have shipped, newest first.", "list",
           f'<section><div class="grid grid-2">{cl_html}</div></section>', "Changelog")
    # contact
    simple("contact", "dashboard", "Company", "Contact",
           "Questions, feedback, or a calculator request — here is how to reach us.", "mail",
           '<section class="panel"><div class="panel-body prose">'
           '<h2>Get in touch</h2><p>This is a free, ad-supported static toolkit. The fastest way to suggest a new calculator or report an issue is by email.</p>'
           '<p><strong>Email:</strong> hello@agenthubs.org</p>'
           '<h2>Feature requests</h2><p>Tell us the decision you are trying to make and we will consider adding a calculator for it. Popular requests ship first.</p>'
           '</div></section>', "Contact")
    # privacy
    simple("privacy", "dashboard", "Legal", "Privacy Policy",
           "How this static, browser-side toolkit handles your data — short version: it stays on your device.", "shield",
           '<section class="panel"><div class="panel-body prose">'
           '<h2>Your calculator data</h2><p>All calculations run in your browser. Inputs, saved scenarios, and settings are stored in this device\'s local storage and are never transmitted to a server we control.</p>'
           '<h2>Advertising</h2><p>We use Google AdSense to keep the toolkit free. AdSense may set cookies and use device identifiers to serve and measure ads, subject to Google\'s policies and your regional consent settings. See Google\'s advertising privacy notice for details.</p>'
           '<h2>Analytics</h2><p>We may use privacy-respecting, aggregate analytics to understand which tools are used. No personally identifying calculator inputs are collected.</p>'
           '<h2>No accounts</h2><p>There is no login, so we do not collect names, passwords, or payment details.</p>'
           '<h2>Your control</h2><p>Clearing your browser\'s site data removes all saved scenarios and settings instantly.</p>'
           '</div></section>', "Privacy")
    # terms
    simple("terms", "dashboard", "Legal", "Terms of Use",
           "The terms for using this free AI ROI toolkit.", "doc",
           '<section class="panel"><div class="panel-body prose">'
           '<h2>Acceptance</h2><p>By using this site you agree to these terms. If you disagree, please do not use the toolkit.</p>'
           '<h2>Use of the calculators</h2><p>The calculators are provided for planning and estimation. Outputs are not financial, tax, legal, or accounting advice. You are responsible for validating inputs and decisions.</p>'
           '<h2>No warranty</h2><p>The toolkit is provided "as is" without warranties of any kind. We do not guarantee accuracy, availability, or fitness for a particular purpose.</p>'
           '<h2>Limitation of liability</h2><p>We are not liable for decisions made using these tools or for any direct or indirect losses arising from their use.</p>'
           '<h2>Changes</h2><p>We may update these terms and the toolkit at any time. Continued use constitutes acceptance of changes.</p>'
           '</div></section>', "Terms")

# =========================================================================== SITEMAP
def build_sitemap():
    rows = []
    seen = set()
    for slug, pri in PAGES_FOR_SITEMAP:
        if slug in seen: continue
        seen.add(slug)
        loc = DOMAIN + "/" + (slug + "/" if slug else "")
        rows.append(f'  <url><loc>{loc}</loc><changefreq>weekly</changefreq><priority>{pri}</priority></url>')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)

# =========================================================================== RUN
def run():
    build_home()
    build_tool()
    build_calc_hub()
    build_calcs()
    build_tools()
    build_guides()
    build_glossary()
    build_site_pages()
    build_sitemap()
    print(f"Built {len(PAGES_FOR_SITEMAP)} pages.")

if __name__ == "__main__":
    run()
