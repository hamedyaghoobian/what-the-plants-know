// The Animals, Counted: the atlas of What the Animals Know.
const BOOK_NAMES = ["Kalila wa Dimna", "The Birds", "The Shahnameh", "The Masnavi", "Marzban-nameh", "Parvin"];
const SPECTRUM = ["anthropectomy", "species-typical", "constructive", "gratuitous"];   // k1..k4
const SPECTRUM_SAY = { anthropectomy: "no mind", "species-typical": "what its kind does", constructive: "a mind read from the animal", gratuitous: "a human mind", none: "" };
const MODES = ["court", "guide", "kept", "ridden", "hunter", "hunted", "wild", "eaten", "sacrificed", "emblem", "none"];
const PAGE = 40;
const R = { book: 0, species: 1, cls: 2, figure: 3, mode: 4, fac: 5, spec: 6, unsure: 7, pass: 8, token: 9, evidence: 10 };

let D, drawings = {}, book = -1, page = 0;
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const klass = r => r[R.figure] === "figure" ? 5 : SPECTRUM.indexOf(r[R.spec]) + 1;
const inBook = r => book < 0 || r[R.book] === book;
const sil = s => drawings[s] ? `<i class="sil" style="--m:url('../data/naardoon/${esc(drawings[s].file)}')" aria-hidden="true"></i>` : `<i></i>`;

function render() {
  const rows = D.rows.filter(inBook);
  const books = book < 0 ? [0, 1, 2, 3, 4, 5] : [book];
  const figs = rows.filter(r => r[R.figure] === "figure").length;
  $("total").textContent = `${rows.length.toLocaleString("en")} animals in ${book < 0 ? "the six books" : BOOK_NAMES[book]}: ` +
    `${(rows.length - figs).toLocaleString("en")} as animals, ${figs.toLocaleString("en")} said of people or things`;

  // ---- species bars ----
  const by = new Map();
  for (const r of rows) {
    const s = r[R.species];
    if (!by.has(s)) by.set(s, books.map(() => ({ n: 0, k: [0, 0, 0, 0], fig: 0 })));
    const c = by.get(s)[books.indexOf(r[R.book])];
    if (r[R.figure] === "figure") c.fig++;
    else { c.n++; const k = SPECTRUM.indexOf(r[R.spec]); if (k >= 0) c.k[k]++; }
  }
  const top = [...by.entries()].map(([s, cs]) => [s, cs, cs.reduce((a, c) => a + c.n + c.fig, 0)])
    .sort((a, b) => b[2] - a[2]).slice(0, 32);
  const el = $("species");
  el.style.setProperty("--n", books.length);
  let h = `<div></div><div></div>` + books.map(b => `<div class="head">${BOOK_NAMES[b]}</div>`).join("");
  for (const [s, cs] of top) {
    h += sil(s) + `<button type="button" class="name" data-species="${esc(s)}">${esc(s)}</button>`;
    for (const c of cs) {
      const judged = c.k.reduce((a, b) => a + b, 0) || 1;
      const segs = [3, 2, 1, 0].map(k => `<span class="k${k + 1}" style="width:${100 * c.k[k] / judged}%;background:var(--k${k + 1})"></span>`).join("");
      const figW = c.n + c.fig ? 100 * c.fig / (c.n + c.fig) : 0;
      h += c.n + c.fig ? `<div class="cell" title="${c.n} as animals, ${c.fig} said of people"><div class="bar">${c.n ? segs : ""}</div>` +
        `<div class="fig"><span style="width:${figW}%"></span></div><span class="n">${c.n + c.fig}</span></div>` : `<div class="cell"></div>`;
    }
  }
  el.innerHTML = h;
  for (const b of el.querySelectorAll("[data-species]")) b.onclick = () => {
    $("f-species").value = b.dataset.species; page = 0; table(); $("rows").scrollIntoView({ behavior: "smooth", block: "start" });
  };

  // ---- relation x faculty ----
  const animals = rows.filter(r => r[R.figure] !== "figure");
  const counts = MODES.map(() => D.faculties.map(() => 0)), totals = MODES.map(() => 0);
  for (const r of animals) {
    const m = MODES.indexOf(r[R.mode]); if (m < 0) continue;
    totals[m]++;
    D.faculties.forEach((_, f) => { if (r[R.fac] & (1 << f)) counts[m][f]++; });
  }
  const max = Math.max(1, ...counts.flat());
  let t = `<table><thead><tr><th></th>${D.faculties.map(f => `<th><span>${f}</span></th>`).join("")}<th class="total"><span>animals</span></th></tr></thead><tbody>`;
  MODES.forEach((m, i) => {
    if (!totals[i]) return;
    t += `<tr><th>${m}</th>` + counts[i].map(n => n
      ? `<td style="background:color-mix(in srgb, var(--yellow) ${Math.round(12 + 80 * Math.sqrt(n / max))}%, transparent)">${n}</td>` : `<td class="z">0</td>`).join("") +
      `<td class="total">${totals[i]}</td></tr>`;
  });
  $("matrix").innerHTML = t + "</tbody></table>";

  // ---- figures ----
  const fig = new Map();
  for (const r of rows) if (r[R.figure] === "figure") fig.set(r[R.species], (fig.get(r[R.species]) || 0) + 1);
  const fs = [...fig.entries()].sort((a, b) => b[1] - a[1]).slice(0, 24), fmax = fs.length ? fs[0][1] : 1;
  $("figures").innerHTML = fs.map(([s, n]) => {
    const all = rows.filter(r => r[R.species] === s).length;
    return `<div class="row">${sil(s)}<span>${esc(s)}</span><span class="b" style="width:${100 * n / fmax}%"></span><span class="n">${n} · ${Math.round(100 * n / all)}%</span></div>`;
  }).join("");

  table();
}

// ---- the table ----

function filtered() {
  const sp = $("f-species").value, fg = $("f-figure").value, md = $("f-mode").value, sc = $("f-spectrum").value, fa = $("f-faculty").value;
  return D.rows.filter(r => inBook(r) && (!sp || r[R.species] === sp) && (!fg || r[R.figure] === fg) && (!md || r[R.mode] === md) &&
    (!sc || r[R.spec] === sc) && (fa === "" || r[R.fac] & (1 << +fa)));
}

function table() {
  const rows = filtered(), pages = Math.max(1, Math.ceil(rows.length / PAGE));
  page = Math.min(page, pages - 1);
  $("count").textContent = `${rows.length.toLocaleString("en")} passages`;
  $("page").textContent = `${page + 1} / ${pages}`;
  $("rows").innerHTML = rows.slice(page * PAGE, (page + 1) * PAGE).map(r => {
    const [text, url, title] = D.passages[r[R.pass]];
    const fac = D.faculties.filter((_, f) => r[R.fac] & (1 << f)).join(", ");
    const tok = esc(r[R.token]);
    return `<tr><td class="book">${BOOK_NAMES[r[R.book]]}</td><td class="an">${esc(r[R.species])}</td>` +
      `<td class="lab">${r[R.figure]}${r[R.mode] !== "none" ? ` · ${r[R.mode]}` : ""}<br><b class="k${klass(r)}">${SPECTRUM_SAY[r[R.spec]] || "a figure of speech"}</b>${fac ? `<br>${fac}` : ""}${r[R.unsure] ? "<br>unsure" : ""}</td>` +
      `<td class="p">${esc(text).split(tok).join(`<mark>${tok}</mark>`)}<a href="${esc(url)}" title="${esc(title)}">ganjoor</a></td></tr>`;
  }).join("");
}

function credits() {
  $("credits").innerHTML = Object.entries(drawings).map(([s, d]) =>
    `<figure>${sil(s)}<figcaption><b>${esc(s)}</b>${esc(d.title)}, traced by ${esc(d.by)}${d.collection ? ` · ${esc(d.collection)}` : ""}<br>` +
    `${d.source.startsWith("http") ? `<a href="${esc(d.source)}">${esc(d.museum)}</a>` : esc(d.museum)} · <a href="https://library.eranshahr.com">NaarDoon</a></figcaption></figure>`).join("");
}

function fillSelects() {
  const sp = [...new Set(D.rows.map(r => r[R.species]))].sort((a, b) => a.localeCompare(b));
  $("f-species").insertAdjacentHTML("beforeend", sp.map(s => `<option>${esc(s)}</option>`).join(""));
  $("f-mode").insertAdjacentHTML("beforeend", MODES.map(m => `<option>${m}</option>`).join(""));
  $("f-faculty").insertAdjacentHTML("beforeend", D.faculties.map((f, i) => `<option value="${i}">${f}</option>`).join(""));
  for (const id of ["f-species", "f-figure", "f-mode", "f-spectrum", "f-faculty"]) $(id).onchange = () => { page = 0; table(); };
  $("f-clear").onclick = () => { for (const id of ["f-species", "f-figure", "f-mode", "f-spectrum", "f-faculty"]) $(id).value = ""; page = 0; table(); };
  $("prev").onclick = () => { page = Math.max(0, page - 1); table(); };
  $("next").onclick = () => { page++; table(); };
}

for (const b of document.querySelectorAll("[data-book]")) b.onclick = () => {
  book = +b.dataset.book;
  for (const x of document.querySelectorAll("[data-book]")) x.setAttribute("aria-pressed", x === b);
  page = 0; render();
};

Promise.all([
  fetch("data.json").then(r => r.json()),
  fetch("../data/naardoon/credits.json").then(r => r.json()).catch(() => ({})),
]).then(([d, c]) => { D = d; drawings = c; fillSelects(); render(); credits(); });
