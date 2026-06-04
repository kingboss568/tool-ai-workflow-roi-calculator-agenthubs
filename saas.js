/* ===========================================================================
   Workspace layer — local save / export / settings / search.
   Browser-side only (localStorage). No backend, no credentials.
   =========================================================================== */
(function () {
  "use strict";
  const config = window.SITE_CONFIG || {};
  const key = "saas-projects:" + location.hostname;
  const settingsKey = "saas-settings:" + location.hostname;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = (v) => String(v || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[c]));
  const projects = () => { try { return JSON.parse(localStorage.getItem(key) || "[]"); } catch { return []; } };
  const setProjects = (items) => localStorage.setItem(key, JSON.stringify(items.slice(0, 60)));
  const settings = () => { try { return JSON.parse(localStorage.getItem(settingsKey) || "{}"); } catch { return {}; } };
  const setSettings = (v) => localStorage.setItem(settingsKey, JSON.stringify(v));

  function currentPayload() {
    const fields = {};
    $$("[data-field]").forEach((n) => (fields[n.dataset.field] = n.value));
    $$("[data-checkgroup]").forEach((n) => {
      if (!fields[n.dataset.checkgroup]) fields[n.dataset.checkgroup] = [];
      if (n.checked) fields[n.dataset.checkgroup].push(n.value);
    });
    return {
      title: (config.title || document.title),
      tool: location.pathname,
      createdAt: new Date().toISOString(),
      fields,
      output: window.lastExportText || ""
    };
  }
  function saveCurrent() {
    const item = currentPayload();
    const name = prompt("Name this saved scenario", item.title + " — " + new Date().toLocaleDateString());
    if (name === null) return;
    item.name = name || item.title;
    setProjects([item, ...projects()]);
    renderProjects();
    const btn = $("[data-save-current]");
    if (btn) { const o = btn.textContent; btn.textContent = "Saved ✓"; setTimeout(() => (btn.textContent = o), 1300); }
  }
  function downloadJson(payload, name) {
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = (name || "scenario").replace(/[^a-z0-9]+/gi, "-").toLowerCase() + ".json";
    a.click();
    URL.revokeObjectURL(a.href);
  }
  function renderProjects() {
    $$("[data-project-list]").forEach((root) => {
      const items = projects();
      root.innerHTML = items.length
        ? items.map((it, i) => `<article class="card"><span style="display:block;color:var(--muted-2);font-size:.76rem">${esc(new Date(it.createdAt).toLocaleString())}</span><h3>${esc(it.name || it.title)}</h3><p>${esc((it.output || "Saved scenario").slice(0, 160))}</p><div class="toolbar" style="margin-top:14px"><button class="btn btn-ghost btn-sm" data-download-project="${i}">Download JSON</button><button class="btn btn-ghost btn-sm" data-delete-project="${i}">Delete</button></div></article>`).join("")
        : `<div class="empty-state">No saved scenarios yet. Open any calculator, then press <strong>Save scenario</strong>.</div>`;
    });
    $$("[data-project-count]").forEach((n) => (n.textContent = String(projects().length)));
  }
  function renderSettings() {
    const data = settings();
    $$("[data-setting]").forEach((n) => (n.value = data[n.dataset.setting] || n.dataset.default || ""));
  }
  function saveSettings() {
    const data = {};
    $$("[data-setting]").forEach((n) => (data[n.dataset.setting] = n.value));
    setSettings(data);
    const note = $("[data-settings-status]");
    if (note) { note.textContent = "Saved locally ✓"; setTimeout(() => (note.textContent = ""), 1800); }
  }

  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-save-current]")) saveCurrent();
    if (e.target.closest("[data-download-current]")) downloadJson(currentPayload(), config.title || "scenario");
    const dl = e.target.closest("[data-download-project]");
    if (dl) { const it = projects()[+dl.dataset.downloadProject]; if (it) downloadJson(it, it.name || it.title); }
    const del = e.target.closest("[data-delete-project]");
    if (del) { const arr = projects(); arr.splice(+del.dataset.deleteProject, 1); setProjects(arr); renderProjects(); }
    const copy = e.target.closest("[data-copy-section]");
    if (copy) {
      const root = copy.closest("[data-copy-root]") || document.body;
      navigator.clipboard?.writeText(root.innerText.trim());
      const o = copy.textContent; copy.textContent = "Copied ✓"; setTimeout(() => (copy.textContent = o), 1300);
    }
    const clear = e.target.closest("[data-clear-projects]");
    if (clear && confirm("Clear all saved scenarios on this browser?")) { setProjects([]); renderProjects(); }
    if (e.target.closest("[data-save-settings]")) saveSettings();
  });

  document.addEventListener("input", (e) => {
    const s = e.target.closest("[data-template-search]");
    if (s) {
      const term = s.value.toLowerCase();
      $$("[data-template-card]").forEach((c) => (c.style.display = c.innerText.toLowerCase().includes(term) ? "" : "none"));
    }
  });

  // Reveal-on-scroll
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("reveal"); io.unobserve(en.target); } });
    }, { threshold: 0.08 });
    $$("[data-reveal]").forEach((el) => io.observe(el));
  }

  renderProjects();
  renderSettings();
})();
