# AgentHubs — AI Workflow ROI Calculator

A free, privacy-first suite of **browser-side AI ROI & cost calculators** for agenthubs.org.

- Live site: https://workflow.agenthubs.org/
- 52 static pages — 25 genuinely functional calculators, 3 decision tools, 7 guides, a searchable glossary, and a full workspace.
- Everything runs client-side. No login, no backend, no data leaves the visitor's device.

## What's inside

| Area | Pages |
| --- | --- |
| Calculators | 25 functional tools across ROI & Payback, Token & API Cost, Workforce & Planning |
| Tools | Comparison matrix, readiness checklist, business-case builder |
| Guides | How to calculate AI ROI, token pricing, formulas, cost optimization, productivity, business case, benchmarks |
| Reference | Searchable glossary, FAQ |
| Workspace | Saved scenarios, reports, templates, examples, settings, integrations, plans |
| Company / legal | About, changelog, contact, privacy, terms |

Each calculator computes real formulas live (net value, ROI, payback, break-even, token cost, TCO,
FTE-equivalent, …), renders a visual breakdown, and supports copy / save-scenario / JSON export.

## Tech

- Hand-built design system in `styles.css` (no framework) with inline SVG illustrations.
- `app.js` — the calculator engine (calculator / library / checklist / matrix / builder kinds),
  driven by an embedded `window.SITE_CONFIG` on each page.
- `saas.js` — browser-side scenario saving, export, settings, and template search.
- Google AdSense (`ca-pub-0268893833921284`): page-level auto ads plus in-content responsive units.

## Build

All pages are generated from a Python builder for consistency:

```bash
cd build && python3 main.py
```

This regenerates every `index.html` and `sitemap.xml`. Edit content and calculators in `build/`
(`shell.py`, `calculators.py`, `main.py`), then re-run.
