/* ===========================================================================
   AI Workflow ROI Calculator — interactive engine
   Drives every calculator/tool page from an embedded window.SITE_CONFIG.
   Pure client-side, no dependencies.
   =========================================================================== */
(function () {
  "use strict";

  const config = window.SITE_CONFIG || {};
  const state = {};

  const qs = (s, r = document) => r.querySelector(s);
  const qsa = (s, r = document) => Array.from(r.querySelectorAll(s));

  function esc(v) {
    return String(v ?? "")
      .replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;").replaceAll("'", "&#039;");
  }

  const currencySymbol = () => {
    try {
      const s = JSON.parse(localStorage.getItem("saas-settings:" + location.hostname) || "{}");
      return { USD: "$", TWD: "NT$", EUR: "€", JPY: "¥", GBP: "£" }[s.currency] || "$";
    } catch { return "$"; }
  };

  function money(v) {
    const n = Number(v || 0);
    const sym = currencySymbol();
    const abs = Math.abs(n);
    let str;
    if (abs >= 1000000) str = (n / 1000000).toFixed(2).replace(/\.00$/, "") + "M";
    else if (abs >= 10000) str = Math.round(n).toLocaleString("en-US");
    else str = n.toLocaleString("en-US", { maximumFractionDigits: 2 });
    return sym + str;
  }
  function num(v, d = 2) {
    const n = Number(v || 0);
    return Number.isInteger(n) ? n.toLocaleString("en-US") : n.toLocaleString("en-US", { maximumFractionDigits: d });
  }

  function fmt(value, output) {
    const f = output.format;
    if (f === "money") return money(value);
    if (f === "percent") return num(value, 1) + "%";
    if (f === "integer") return num(Math.round(value), 0);
    if (f === "ratio") return num(value, 2) + "×";
    if (f === "months") return num(value, 1) + " mo";
    if (f === "hours") return num(value, 1) + " hrs";
    if (f === "days") return num(value, 1) + " days";
    return num(value, output.digits ?? 2) + (output.unit ? " " + output.unit : "");
  }

  /* ----------------------------------------------------------------- state */
  function initState() {
    (config.fields || []).forEach((field) => {
      state[field.id] = field.type === "checklist" ? (field.default || []) : (field.default ?? "");
    });
  }
  const selected = (id) => (Array.isArray(state[id]) ? state[id] : []);

  /* ----------------------------------------------------------------- fields */
  function renderField(field) {
    const hint = field.hint ? `<span class="hint">${esc(field.hint)}</span>` : "";
    const value = state[field.id] ?? "";
    if (field.type === "select") {
      return `<label class="field${field.wide ? " wide" : ""}"><span>${esc(field.label)}</span>${hint}<select data-field="${field.id}">${(field.options || []).map((o) => `<option value="${esc(o)}" ${o === value ? "selected" : ""}>${esc(o)}</option>`).join("")}</select></label>`;
    }
    if (field.type === "textarea") {
      return `<label class="field wide"><span>${esc(field.label)}</span>${hint}<textarea data-field="${field.id}" rows="${field.rows || 6}">${esc(value)}</textarea></label>`;
    }
    if (field.type === "color") {
      return `<label class="field"><span>${esc(field.label)}</span>${hint}<input type="color" data-field="${field.id}" value="${esc(value)}"></label>`;
    }
    if (field.type === "checklist") {
      return `<fieldset class="field wide"><legend>${esc(field.label)}</legend>${hint}<div class="check-grid">${(field.options || []).map((o) => `<label><input type="checkbox" data-checkgroup="${field.id}" value="${esc(o)}" ${selected(field.id).includes(o) ? "checked" : ""}> ${esc(o)}</label>`).join("")}</div></fieldset>`;
    }
    const t = field.type === "number" || field.type === "range" ? field.type : "text";
    const step = field.step ? ` step="${esc(field.step)}"` : "";
    const min = field.min !== undefined ? ` min="${esc(field.min)}"` : "";
    const max = field.max !== undefined ? ` max="${esc(field.max)}"` : "";
    const input = `<input type="${t}" data-field="${field.id}" value="${esc(value)}"${step}${min}${max} inputmode="${t === "number" ? "decimal" : "text"}">`;
    if (field.money) {
      return `<label class="field${field.wide ? " wide" : ""}"><span>${esc(field.label)}</span>${hint}<span class="input-prefix"><span>${currencySymbol()}</span>${input}</span></label>`;
    }
    return `<label class="field${field.wide ? " wide" : ""}"><span>${esc(field.label)}</span>${hint}${input}</label>`;
  }

  function renderForm() {
    const host = qs("#toolFields");
    if (host) host.innerHTML = (config.fields || []).map(renderField).join("");
  }

  function onInput(event) {
    const t = event.target;
    if (t.matches("[data-field]")) { state[t.dataset.field] = t.value; renderResult(); }
    if (t.matches("[data-checkgroup]")) {
      const g = t.dataset.checkgroup;
      state[g] = qsa("[data-checkgroup]").filter((n) => n.dataset.checkgroup === g && n.checked).map((n) => n.value);
      renderResult();
    }
  }

  function inputs() {
    const data = {};
    (config.fields || []).forEach((field) => {
      const v = state[field.id];
      if (field.type === "number" || field.type === "range") data[field.id] = Number(v || 0);
      else if (field.type === "checklist") data[field.id] = selected(field.id);
      else data[field.id] = v ?? "";
    });
    return data;
  }

  function evaluate(expr, data) {
    try {
      return Function("inputs", `"use strict"; const { ${Object.keys(data).join(", ")} } = inputs; const max=Math.max,min=Math.min,abs=Math.abs,round=Math.round,pow=Math.pow,ceil=Math.ceil,floor=Math.floor; return (${expr});`)(data);
    } catch { return 0; }
  }

  function tokens(text, data) {
    return String(text || "").replace(/\{\{([a-zA-Z0-9_]+)\}\}/g, (_, k) => {
      const v = data[k];
      return Array.isArray(v) ? v.join(", ") : String(v ?? "");
    });
  }

  function setExport(text) { window.lastExportText = text; }

  /* --------------------------------------------------------------- visuals */
  function barChart(rows) {
    const max = Math.max(1, ...rows.map((r) => Math.abs(r.value)));
    const palette = ["", "teal", "amber"];
    return `<div class="bars">${rows.map((r, i) => {
      const w = Math.min(100, (Math.abs(r.value) / max) * 100);
      return `<div class="bar-row"><span class="bl">${esc(r.label)}</span><span class="bar-track"><span class="bar-fill ${palette[i % palette.length]}" style="width:${w}%"></span></span><span class="bv">${esc(r.display)}</span></div>`;
    }).join("")}</div>`;
  }

  function summary(text) {
    return `<div class="result-summary"><span class="spark"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/></svg></span><span>${text}</span></div>`;
  }

  /* ----------------------------------------------------------------- kinds */
  function calculatorTool() {
    const data = inputs();
    const outputs = (config.engine?.outputs || []).map((o) => ({ ...o, value: evaluate(o.expr, data) }));
    const rules = (config.engine?.rules || [])
      .filter((r) => !r.if || Boolean(evaluate(r.if, data)))
      .map((r) => tokens(r.text, data));
    if (!rules.length) rules.push(config.engine?.defaultAdvice || "Inputs are within a normal planning range. Confirm your assumptions before acting on the result.");

    const hero = outputs.find((o) => o.hero) || outputs[0];
    const rest = outputs.filter((o) => o !== hero);
    const chartRows = outputs.filter((o) => o.chart).map((o) => ({ label: o.label, value: Number(o.value) || 0, display: fmt(o.value, o) }));

    const metrics = `<div class="metric-grid">${
      `<div class="metric hero-metric"><span>${esc(hero.label)}</span><strong>${esc(fmt(hero.value, hero))}</strong></div>` +
      rest.map((o) => `<div class="metric"><span>${esc(o.label)}</span><strong>${esc(fmt(o.value, o))}</strong></div>`).join("")
    }</div>`;

    const chart = chartRows.length >= 2 ? barChart(chartRows) : "";
    const advice = `<ul class="advice-list">${rules.map((r) => `<li>${esc(r)}</li>`).join("")}</ul>`;
    setExport(`${config.title}\n${outputs.map((o) => `${o.label}: ${fmt(o.value, o)}`).join("\n")}\n\nNotes\n- ${rules.join("\n- ")}`);
    return summary(`<strong>${esc(hero.label)}:</strong> ${esc(fmt(hero.value, hero))}`) + metrics + chart + advice;
  }

  function libraryTool() {
    const data = inputs();
    const q = String(data.query || "").toLowerCase();
    const cat = data.category || "All";
    const items = (config.data?.items || []).filter((it) => {
      const text = `${it.title} ${it.category} ${it.use} ${it.note} ${it.tags || ""}`.toLowerCase();
      return (!q || text.includes(q)) && (cat === "All" || it.category === cat);
    });
    const shown = items.slice(0, 30);
    const html = `<div class="result-list">${shown.map((it) => `<article><h3>${esc(it.title)}</h3><p>${esc(it.note)}</p><dl><dt>Use</dt><dd>${esc(it.use || "Reference")}</dd>${it.caution ? `<dt>Caution</dt><dd>${esc(it.caution)}</dd>` : ""}</dl></article>`).join("") || `<div class="empty-state">No match yet. Try a shorter keyword or the All category.</div>`}</div>`;
    setExport(shown.map((it) => `${it.title} — ${it.note}`).join("\n"));
    return summary(`<strong>${shown.length}</strong> of ${items.length} reference entries shown`) + html;
  }

  function checklistTool() {
    const data = inputs();
    const sel = data.items || data.checks || [];
    const items = config.data?.items || [];
    const picked = items.filter((it) => sel.includes(it.title));
    const risk = picked.reduce((s, it) => s + Number(it.weight || 1), 0);
    const maxRisk = items.reduce((s, it) => s + Number(it.weight || 1), 0) || 1;
    const score = Math.max(0, 100 - (risk / maxRisk) * 100);
    const metrics = `<div class="metric-grid"><div class="metric hero-metric"><span>Readiness score</span><strong>${score.toFixed(0)}%</strong></div><div class="metric"><span>Open items</span><strong>${picked.length}</strong></div><div class="metric"><span>Risk points</span><strong>${risk}</strong></div></div>`;
    const list = `<div class="result-list">${picked.map((it) => `<article><h3>${esc(it.title)}</h3><p>${esc(it.note || "Resolve before launch.")}</p><small>${esc(it.category || "Review")}</small></article>`).join("") || `<p class="good">No open risk items selected. Keep a final human review step.</p>`}</div>`;
    setExport(`${config.title}\nReadiness: ${score.toFixed(0)}%\nOpen items:\n- ${picked.map((it) => it.title).join("\n- ")}`);
    return summary(`Readiness score: <strong>${score.toFixed(0)}%</strong>`) + metrics + list;
  }

  function matrixTool() {
    const data = inputs();
    const rows = String(data.rows || "").split("\n").map((l) => l.split(",").map((p) => p.trim())).filter((r) => r.some(Boolean));
    const weights = config.engine?.weights || { Impact: 0.4, Cost: 0.3, Effort: 0.3 };
    const keys = Object.keys(weights);
    const wv = Object.values(weights);
    const ranked = rows.map((r) => {
      const score = wv.reduce((s, w, i) => s + Number(r[i + 1] || 0) * w, 0);
      return { name: r[0] || "Option", score };
    }).sort((a, b) => b.score - a.score);
    const chartRows = ranked.slice(0, 6).map((r) => ({ label: r.name, value: r.score, display: r.score.toFixed(2) }));
    const chart = chartRows.length ? barChart(chartRows) : `<div class="empty-state">Add one option per line: Name, ${keys.join(", ")}</div>`;
    setExport(ranked.map((r, i) => `${i + 1}. ${r.name}: ${r.score.toFixed(2)}`).join("\n"));
    return summary(`${ranked.length} options ranked by weighted score`) + chart;
  }

  function builderTool() {
    const data = inputs();
    const sections = config.engine?.sections || [{ title: "Draft", body: "{{summary}}" }];
    const html = `<div class="result-list">${sections.map((s) => `<article><h3>${esc(tokens(s.title, data))}</h3><p>${esc(tokens(s.body, data)).replace(/\n/g, "<br>")}</p></article>`).join("")}</div>`;
    setExport(sections.map((s) => `${tokens(s.title, data)}\n${tokens(s.body, data)}`).join("\n\n"));
    return summary(`${sections.length} sections generated`) + html;
  }

  function renderResult() {
    const host = qs("#toolResult");
    if (!host) return;
    const map = { calculator: calculatorTool, library: libraryTool, checklist: checklistTool, matrix: matrixTool, builder: builderTool };
    host.innerHTML = (map[config.kind] || calculatorTool)();
  }

  /* ----------------------------------------------------------- static blocks */
  function renderStatic() {
    const ex = qs("#examples");
    if (ex) ex.innerHTML = (config.examples || []).map((it) => `<article class="card"><h3>${esc(it.title)}</h3><p>${esc(it.body)}</p></article>`).join("");
    const faq = qs("#faq");
    if (faq) faq.innerHTML = (config.faq || []).map((it) => `<details><summary>${esc(it.q)}</summary><p>${esc(it.a)}</p></details>`).join("");
    const lim = qs("#limits");
    if (lim) lim.innerHTML = (config.limits || []).map((it) => `<li>${esc(it)}</li>`).join("");
  }

  async function copyExport() {
    const text = window.lastExportText || "";
    if (!text) return;
    const btn = qs("#copyExport");
    try {
      await navigator.clipboard.writeText(text);
      if (btn) { const o = btn.textContent; btn.textContent = "Copied ✓"; setTimeout(() => (btn.textContent = o), 1300); }
    } catch {
      const a = document.createElement("textarea"); a.value = text; document.body.appendChild(a); a.select();
      try { document.execCommand("copy"); } catch {}
      a.remove();
    }
  }

  function boot() {
    initState();
    renderForm();
    renderResult();
    renderStatic();
    const host = qs("#toolFields");
    if (host) { host.addEventListener("input", onInput); host.addEventListener("change", onInput); }
    const copy = qs("#copyExport");
    if (copy) copy.addEventListener("click", copyExport);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
