// Pyxel Canvas desktop UI. All work happens in Python (window.pywebview.api);
// this file only builds the page and forwards user actions.
"use strict";

const $ = (id) => document.getElementById(id);
const state = {
  catalog: null,
  pattern: null,       // {name, number, animatable, category}
  controls: [],        // control specs for the current pattern
  rendered: false,
  busy: false,
  lastAction: Promise.resolve(),   // the self-test awaits this after each click
};
let api = null;

// ── helpers ───────────────────────────────────────────────────

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  }
  for (const c of children) node.append(c);
  return node;
}

function setStatus(text, kind = "", path = null) {
  const s = $("status");
  s.className = "status " + kind;
  s.textContent = text;
  if (path) {
    const link = el("a", { href: "#", onclick: (e) => { e.preventDefault(); api.open_exports_folder(); } }, "Open folder");
    s.append(" ", link);
  }
}

function setBusy(on, text = "Rendering…") {
  state.busy = on;
  $("busy").classList.toggle("hidden", !on);
  $("busy-text").textContent = text;
  $("render-btn").disabled = on;
  $("png-btn").disabled = on || !state.rendered;
  $("gif-btn").disabled = on || !state.pattern?.animatable;
}

// Run an async action; the self-test awaits state.lastAction after a click
function track(promise) {
  state.lastAction = promise.catch(() => {});
  return promise;
}

function renderMath(root) {
  root.querySelectorAll(".math").forEach((node) => {
    katex.render(node.textContent, node, {
      displayMode: node.classList.contains("math-display"),
      throwOnError: false, strict: "ignore",
    });
  });
}

// ── navigation ────────────────────────────────────────────────

function showView(id) {
  for (const v of document.querySelectorAll(".view")) v.classList.toggle("hidden", v.id !== id);
}

function buildSidebar(catalog) {
  const nav = $("nav");
  nav.innerHTML = "";
  for (const cat of catalog.categories) {
    const list = el("ul", { class: "cat-list" });
    const box = el("div", { class: "cat" },
      el("button", { class: "cat-btn", onclick: () => box.classList.toggle("open") },
        el("span", {}, el("span", { class: "chev" }, "›"), " ", cat.name),
        el("span", { class: "count" }, String(cat.patterns.length))),
      list);
    for (const p of cat.patterns) {
      p.category = cat.name;
      const btn = el("button", { class: "pat-btn", "data-name": p.name,
                                 onclick: () => track(openPattern(p)) },
        el("span", { class: "num" }, String(p.number)), p.name);
      if (p.animatable) btn.append(el("span", { class: "badge", title: "Supports GIF export" }, "GIF"));
      list.append(el("li", {}, btn));
    }
    nav.append(box);
  }
}

function buildWelcome(catalog) {
  const blurbs = {
    "Geometric & Mathematical": "Fractals, curves, tilings and strange attractors.",
    "Nature-Inspired": "Trees, lightning, galaxies, terrain and reaction-diffusion.",
    "Abstract & Artistic": "Mondrian, op-art, watercolour, glitch and pixel sorting.",
    "2D Game-Style": "Mazes, dungeons, Pac-Man pathfinding and bullet-hell.",
    "3D Objects & Sculptures": "Knots, minimal surfaces, crystal lattices and attractors.",
    "Scientific & Simulation": "Orbitals, fluids, quantum waves and flocking (animated).",
  };
  const box = $("category-cards");
  box.innerHTML = "";
  for (const cat of catalog.categories) {
    box.append(el("button", { class: "category-card",
                              onclick: () => track(openPattern(cat.patterns[0])) },
      el("h3", {}, `${cat.name} · ${cat.patterns.length}`),
      el("p", {}, blurbs[cat.name] || "")));
  }
  $("exports-path").textContent = catalog.app.exports;
  $("version").textContent = "v" + catalog.app.version;
}

function goHome() {
  document.querySelectorAll(".pat-btn.active").forEach((b) => b.classList.remove("active"));
  state.pattern = null;
  showView("welcome-view");
}

// ── pattern page ──────────────────────────────────────────────

function buildControl(spec) {
  if (spec.type === "slider") {
    const decimals = (x) => Math.min(4, (String(x).split(".")[1] || "").length);
    const places = spec.integer ? 0 : Math.max(decimals(spec.step), decimals(spec.value), 1);
    const fmt = (v) => Number(v).toFixed(places);
    // A native step would snap defaults that are off the step grid (e.g. Lorenz
    // beta 2.667 with step 0.05 -> 2.65), so the slider is continuous and snaps
    // here instead: to the step grid, or to the pattern's exact default.
    const snap = (v) => {
      const grid = Number((spec.min + Math.round((v - spec.min) / spec.step) * spec.step).toFixed(10));
      const best = Math.abs(v - spec.value) <= Math.abs(v - grid) ? spec.value : grid;
      return Math.min(spec.max, Math.max(spec.min, best));
    };
    const value = el("span", { class: "value" }, fmt(spec.value));
    const input = el("input", { type: "range", min: spec.min, max: spec.max, step: "any",
                                value: spec.value, "data-key": spec.key });
    input.addEventListener("input", () => {
      const v = snap(Number(input.value));
      if (Number(input.value) !== v) input.value = v;
      value.textContent = fmt(v);
    });
    return el("div", { class: "control" },
      el("div", { class: "row" }, el("label", {}, spec.label), value), input);
  }
  if (spec.type === "dropdown") {
    const sel = el("select", { "data-key": spec.key });
    spec.options.forEach((o, i) => sel.append(el("option", { value: i }, o)));
    sel.value = spec.value;
    return el("div", { class: "control" }, el("label", {}, spec.label), sel);
  }
  if (spec.type === "checkbox") {
    const box = el("input", { type: "checkbox", "data-key": spec.key });
    box.checked = spec.value;
    return el("div", { class: "control check" }, box, el("label", {}, spec.label));
  }
  return el("div", { class: "control" }, el("label", {}, spec.label),
    el("input", { type: "text", value: spec.value, "data-key": spec.key }));
}

// The input element for a control spec, and its value in the spec's terms
function controlNode(spec) {
  return $("controls").querySelector(`[data-key="${CSS.escape(spec.key)}"]`);
}

function isDefault(spec) {
  const node = controlNode(spec);
  if (!node) return true;
  if (spec.type === "checkbox") return node.checked === spec.value;
  if (spec.type === "slider" || spec.type === "dropdown") return Number(node.value) === Number(spec.value);
  return node.value === String(spec.value);
}

// "Reset to defaults" is only enabled once something differs from the defaults
function updateResetState() {
  $("reset-btn").disabled = state.controls.every(isDefault);
}

function resetControls() {
  for (const spec of state.controls) {
    const node = controlNode(spec);
    if (!node) continue;
    if (spec.type === "checkbox") node.checked = spec.value;
    else node.value = spec.value;
    node.dispatchEvent(new Event("input"));   // refresh slider readouts
  }
  updateResetState();
}

function readControls() {
  const values = {};
  for (const node of $("controls").querySelectorAll("[data-key]")) {
    const key = node.dataset.key;
    if (node.type === "checkbox") values[key] = node.checked;
    else if (node.type === "range") values[key] = Number(node.value);
    else if (node.tagName === "SELECT") values[key] = Number(node.value);
    else values[key] = node.value;
  }
  return values;
}

async function openPattern(p) {
  state.pattern = p;
  state.rendered = false;
  document.querySelectorAll(".pat-btn").forEach((b) => b.classList.toggle("active", b.dataset.name === p.name));
  const cat = [...document.querySelectorAll(".cat")].find((c) => c.querySelector(`[data-name="${CSS.escape(p.name)}"]`));
  cat?.classList.add("open");

  $("pattern-meta").textContent = `Pattern ${p.number} · ${p.category}`;
  $("pattern-title").textContent = p.name;
  $("render-img").classList.add("hidden");
  $("placeholder").classList.remove("hidden");
  $("fps-wrap").classList.toggle("hidden", !p.animatable);
  $("gif-btn").title = p.animatable ? "" : "Only the 10 Scientific & Simulation patterns animate";
  setStatus("");
  setBusy(false);
  showView("pattern-view");

  const [controls, note] = await Promise.all([api.get_controls(p.name), api.get_note(p.name)]);
  if (state.pattern !== p) return;                 // user moved on meanwhile
  const box = $("controls");
  box.innerHTML = "";
  if (controls.ok) {
    state.controls = controls.controls;
    controls.controls.forEach((spec) => box.append(buildControl(spec)));
    updateResetState();
  } else {
    setStatus("Could not load controls: " + controls.error, "err");
  }
  const notes = $("notes");
  notes.innerHTML = note.ok ? note.html : `<p class="status err">${note.error}</p>`;
  renderMath(notes);
  $("notes").parentElement.scrollTop = 0;
}

async function render() {
  const p = state.pattern;
  if (!p || state.busy) return;
  setBusy(true, "Rendering…");
  setStatus("");
  const res = await api.render(p.name, $("palette").value, $("resolution").value, readControls());
  if (state.pattern !== p) return;
  if (res.ok) {
    const img = $("render-img");
    await new Promise((resolve) => { img.onload = resolve; img.onerror = resolve; img.src = res.image; });
    img.classList.remove("hidden");
    $("placeholder").classList.add("hidden");
    state.rendered = true;
    setStatus("Rendered.", "ok");
  } else {
    setStatus(res.error, "err");
  }
  setBusy(false);
}

async function exportPng() {
  const p = state.pattern;
  if (!p || state.busy) return;
  setBusy(true, "Saving PNG…");
  const res = await api.export_png(p.name);
  setBusy(false);
  res.ok ? setStatus("Saved " + res.path, "ok", res.path) : setStatus(res.error, "err");
}

async function exportGif() {
  const p = state.pattern;
  if (!p || state.busy || !p.animatable) return;
  const fps = Math.max(2, Math.min(30, Number($("fps").value) || 12));
  $("fps").value = fps;
  setBusy(true, `Creating ${state.catalog.gif_frames}-frame GIF…`);
  const res = await api.export_gif(p.name, $("palette").value, $("resolution").value, readControls(), fps);
  setBusy(false);
  res.ok ? setStatus("Saved " + res.path, "ok", res.path) : setStatus(res.error, "err");
}

// ── start-up ──────────────────────────────────────────────────

async function init() {
  api = window.pywebview.api;
  const cat = await api.get_catalog();
  if (!cat.ok) { $("nav").innerHTML = `<p class="status err pad">${cat.error}</p>`; return; }
  state.catalog = cat;
  buildSidebar(cat);
  buildWelcome(cat);
  for (const p of cat.palettes) $("palette").append(el("option", { value: p }, p));
  for (const r of cat.resolutions) $("resolution").append(el("option", { value: r }, r));

  $("home-link").addEventListener("click", goHome);
  $("start-btn").addEventListener("click", () => track(openPattern(cat.categories[0].patterns[0])));
  $("source-link").addEventListener("click", (e) => { e.preventDefault(); api.open_source(); });
  $("render-btn").addEventListener("click", () => track(render()));
  $("png-btn").addEventListener("click", () => track(exportPng()));
  $("gif-btn").addEventListener("click", () => track(exportGif()));
  $("reset-btn").addEventListener("click", resetControls);
  // Any edit to a control (slider drag, dropdown, checkbox, text) re-checks the button
  $("controls").addEventListener("input", updateResetState);
  $("controls").addEventListener("change", updateResetState);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && e.ctrlKey && state.pattern) track(render());
  });
  document.body.dataset.ready = "1";
}

window.addEventListener("pywebviewready", init);

// ── self-test: drives the real UI through every category ──────
// Started by `Pyxel.exe --selftest <report.json>` to verify a build.
window.runSelfTest = async function () {
  const report = { categories: [], errors: [] };
  const click = async (node) => { node.click(); await state.lastAction; };
  try {
    while (!state.catalog) await new Promise((r) => setTimeout(r, 100));
    report.welcome = !$("welcome-view").classList.contains("hidden")
      && $("category-cards").children.length === state.catalog.categories.length;
    let pngDone = false, gifDone = false;
    for (const cat of state.catalog.categories) {
      const picks = [cat.patterns[0]];
      if (!gifDone && cat.patterns.some((p) => p.animatable)) picks.push(cat.patterns.find((p) => p.animatable && p !== cat.patterns[0]) || cat.patterns[0]);
      for (const p of picks) {
        await click(document.querySelector(`.pat-btn[data-name="${CSS.escape(p.name)}"]`));
        const entry = { pattern: p.name, title: $("pattern-title").textContent === p.name,
                        controls: $("controls").querySelectorAll("[data-key]").length,
                        katex: $("notes").querySelectorAll(".katex").length,
                        katexErrors: $("notes").querySelectorAll(".katex-error").length,
                        resetDisabledOnLoad: $("reset-btn").disabled };
        await click($("render-btn"));
        const img = $("render-img");
        entry.rendered = !img.classList.contains("hidden") && img.naturalWidth > 0;
        entry.imageSize = [img.naturalWidth, img.naturalHeight];
        entry.splitEqual = Math.abs($("canvas").closest(".panel").offsetWidth - $("notes").closest(".panel").offsetWidth) <= 2;
        if (!pngDone) {
          await click($("png-btn")); entry.png = $("status").textContent; pngDone = true;
        }
        if (p.animatable && !gifDone) {
          $("fps").value = 10;
          await click($("gif-btn")); entry.gif = $("status").textContent; gifDone = true;
        }
        report.categories.push(entry);
      }
    }
    // Reset to defaults: exact off-grid default, enable on edit, restore on click
    {
      const lorenz = state.catalog.categories.flatMap((c) => c.patterns).find((p) => p.name === "Chaos Attractor (Lorenz)");
      await click(document.querySelector(`.pat-btn[data-name="${CSS.escape(lorenz.name)}"]`));
      const beta = $("controls").querySelector('[data-key="beta"]');
      const r = { pattern: lorenz.name, betaDefault: Number(beta.value), disabledAtStart: $("reset-btn").disabled };
      const rho = $("controls").querySelector('[data-key="rho"]');
      rho.value = rho.max; rho.dispatchEvent(new Event("input", { bubbles: true }));
      beta.value = Number(beta.min); beta.dispatchEvent(new Event("input", { bubbles: true }));
      r.enabledAfterEdit = !$("reset-btn").disabled;
      $("reset-btn").click();
      r.restored = Number(beta.value) === r.betaDefault && $("reset-btn").disabled
        && state.controls.every((spec) => isDefault(spec));
      report.reset = r;
    }
    // Every pattern must load with all controls at their exact defaults
    report.notAtDefault = [];
    for (const p of state.catalog.categories.flatMap((c) => c.patterns)) {
      await click(document.querySelector(`.pat-btn[data-name="${CSS.escape(p.name)}"]`));
      if (!$("reset-btn").disabled) report.notAtDefault.push(p.name);
    }
    // Every note: KaTeX must render without errors
    report.notes = { total: 0, katexErrors: [] };
    for (const cat of state.catalog.categories) for (const p of cat.patterns) {
      const n = await api.get_note(p.name);
      const div = el("div"); div.innerHTML = n.html; renderMath(div);
      report.notes.total += 1;
      const errs = [...div.querySelectorAll(".katex-error")].map((e) => e.title || e.textContent);
      if (errs.length) report.notes.katexErrors.push({ pattern: p.name, errors: errs });
    }
    $("home-link").click();
    report.backHome = !$("welcome-view").classList.contains("hidden");
  } catch (e) {
    report.errors.push(String(e && e.stack || e));
  }
  await api.selftest_report(report);
};
