/* DIP drawing kit: pixel grids, sliding kernels, histograms, transfer curves, real photos with live lookup tables,
   calculator screens. Everything is a pure function of scene time (the engine's rule), so scrubbing is exact. */
'use strict';
const fr = (v, d = 2) => (Math.round(v * 10 ** d) / 10 ** d).toString();
const roundHalfUp = (v) => Math.floor(v + 0.5);
const NUM = (k) => ANSWERS[k];
const grayOf = (v, L) => { const g = Math.round((255 * clamp(v, 0, L - 1)) / (L - 1)); return `rgb(${g},${g},${g})`; };

/* a matrix of numbers drawn as cells. M: 2-D array. o: {cs (cell size), L (shade cells as gray levels), size (font),
   idx (show row/col indices), color, fill, x0/y0 index offsets, hide: [[i,j]] blank cells}.
   Returns {g, cs, X(j), Y(i) (cell centres), cell(i,j) → {r, t}, box(i, j, h, w, col) → highlight rect} */
function mgrid(S, M, x, y, o = {}, parent) {
  const g = S.g({}, parent), cs = o.cs || 64, R = M.length, Cn = M[0].length, L = o.L;
  const cells = [];
  for (let i = 0; i < R; i++) {
    cells.push([]);
    for (let j = 0; j < Cn; j++) {
      const v = M[i][j];
      const fill = o.fillFn ? o.fillFn(v, i, j) : L ? grayOf(v, L) : o.fill || '#121a26';
      const r = S.el('rect', { x: x + j * cs, y: y + i * cs, width: cs, height: cs, fill, stroke: o.stroke || '#3a4658', 'stroke-width': 1.5 }, g);
      const light = L && v > (L - 1) * 0.55;
      const t = v === null || v === undefined || v === '' ? null : txt(S, x + j * cs + cs / 2, y + i * cs + cs / 2 + (o.size || cs * 0.36) * 0.36, typeof v === 'number' ? (o.fmt ? o.fmt(v) : String(v)) : v,
        { size: o.size || Math.round(cs * 0.36), color: o.colorFn ? o.colorFn(v, i, j) : L ? (light ? '#111' : '#f2f5f9') : o.color || C.text, weight: 700, anchor: 'middle', mono: true }, g);
      cells[i].push({ r, t });
    }
  }
  if (o.idx) {
    const x0 = o.x0 || 0, y0 = o.y0 || 0;
    for (let j = 0; j < Cn; j++) txt(S, x + j * cs + cs / 2, y - 10, String(j + y0), { size: 15, color: C.muted, anchor: 'middle' }, g);
    for (let i = 0; i < R; i++) txt(S, x - 12, y + i * cs + cs / 2 + 6, String(i + x0), { size: 15, color: C.muted, anchor: 'end' }, g);
    if (o.axes !== false) {
      txt(S, x + Cn * cs + 14, y - 8, o.ylab || 'y →', { size: 16, color: C.p, weight: 700 }, g);
      txt(S, x - 12, y + R * cs + 26, o.xlab || 'x ↓', { size: 16, color: C.n, weight: 700, anchor: 'end' }, g);
    }
  }
  const X = (j) => x + j * cs + cs / 2, Y = (i) => y + i * cs + cs / 2;
  const box = (i, j, h = 1, w = 1, col = C.amb, t0 = null, t1 = null, sw = 4) => {
    const r = S.el('rect', { x: x + j * cs, y: y + i * cs, width: w * cs, height: h * cs, fill: 'none', stroke: col, 'stroke-width': sw, rx: 4 });
    if (t0 !== null) { r.style.opacity = 0; S.fade(r, t0, 0.35); if (t1) S.out(r, t1, 0.3); }
    return r;
  };
  return { g, cs, X, Y, cells, cell: (i, j) => cells[i][j], box, x, y, R, Cn, w: Cn * cs, h: R * cs };
}

/* a highlight window of h×w cells that jumps along a list of [i, j, t] stops on a grid made by mgrid */
function slideWin(S, G, path, h, w, col = C.amb, t1 = null) {
  const r = S.el('rect', { x: G.x + path[0][1] * G.cs, y: G.y + path[0][0] * G.cs, width: w * G.cs, height: h * G.cs, fill: col, 'fill-opacity': 0.12, stroke: col, 'stroke-width': 4, rx: 5 });
  r.style.opacity = 0; S.fade(r, path[0][2], 0.3);
  for (let k = 1; k < path.length; k++) {
    const [i0, j0] = path[k - 1], [i1, j1, t] = path[k];
    S.anim(t, 0.35, r.id + ':xy', (p) => { r.setAttribute('x', G.x + lerp(j0, j1, p) * G.cs); r.setAttribute('y', G.y + lerp(i0, i1, p) * G.cs); }, E.inout);
  }
  if (t1) S.out(r, t1, 0.3);
  return r;
}

/* set a cell's number (and optional colour) from time t: used to fill an output grid step by step */
function fillCell(S, G, i, j, v, t, col) {
  const c = G.cell(i, j);
  const tt = txt(S, G.X(j), G.Y(i) + G.cs * 0.13, String(v), { size: Math.round(G.cs * 0.36), color: col || C.amb, weight: 800, anchor: 'middle', mono: true }, G.g);
  tt.style.opacity = 0; S.pop(tt, t, 0.4);
  if (c.t) S.out(c.t, t, 0.2);
  return tt;
}

/* bar chart for a small histogram: vals (counts or probabilities), labels under bars, o: {max, color, fmt, valLab, t0, dt} */
function bars(S, x, y, w, h, vals, o = {}) {
  const g = S.g(), n = vals.length, gap = o.gap ?? 0.18, bw = w / n, mx = o.max || Math.max(...vals) || 1;
  S.el('line', { x1: x, y1: y + h, x2: x + w, y2: y + h, stroke: C.muted, 'stroke-width': 2 }, g);
  const out = [];
  vals.forEach((v, k) => {
    const bh = (v / mx) * h, bx = x + k * bw + (bw * gap) / 2;
    const col = Array.isArray(o.color) ? o.color[k] : o.color || C.volt;
    const r = S.el('rect', { x: bx, y: y + h - bh, width: bw * (1 - gap), height: bh, rx: 3, fill: col, 'fill-opacity': 0.85 }, g);
    if (o.labels !== false) txt(S, x + k * bw + bw / 2, y + h + 24, o.labels ? String(o.labels[k]) : String(k), { size: o.lsize || 17, color: C.muted, anchor: 'middle' }, g);
    let vt = null;
    if (o.valLab !== false && v > 0) vt = txt(S, x + k * bw + bw / 2, y + h - bh - 8, o.fmt ? o.fmt(v) : String(v), { size: o.vsize || 16, color: col, anchor: 'middle', weight: 700 }, g);
    if (o.t0 !== undefined) {
      const t = o.t0 + k * (o.dt ?? 0.12);
      S.anim(t, 0.5, r.id + ':h', (p) => { r.setAttribute('height', bh * p); r.setAttribute('y', y + h - bh * p); });
      if (vt) { vt.style.opacity = 0; S.fade(vt, t + 0.3, 0.3); }
    }
    out.push({ r, vt });
  });
  if (o.title) txt(S, x, y - 14, o.title, { size: 18, color: C.muted, weight: 600 }, g);
  return { g, bars: out, X: (k) => x + k * bw + bw / 2, bw };
}

/* 256-bin histogram drawn as one path; returns {g, set(counts)} so it can follow a live transform */
function hist256(S, x, y, w, h, counts, o = {}) {
  const g = S.g();
  S.el('rect', { x, y, width: w, height: h, rx: 8, fill: '#0e141e', stroke: '#222c3b' }, g);
  const p = S.el('path', { fill: o.color || C.volt, 'fill-opacity': 0.85 }, g);
  [0, 64, 128, 192, 255].forEach((v) => txt(S, x + (v / 255) * w, y + h + 22, String(v), { size: 15, color: C.muted, anchor: 'middle' }, g));
  if (o.title) txt(S, x + 6, y - 12, o.title, { size: 18, color: C.muted, weight: 600 }, g);
  const set = (c) => {
    const mx = o.max || Math.max(...c);
    let d = `M${x} ${y + h}`;
    for (let k = 0; k < 256; k++) { const hh = Math.min(h - 4, (c[k] / mx) * (h - 4)); const x0 = x + (k / 256) * w, x1 = x + ((k + 1) / 256) * w; d += ` L${x0.toFixed(1)} ${(y + h - hh).toFixed(1)} L${x1.toFixed(1)} ${(y + h - hh).toFixed(1)}`; }
    p.setAttribute('d', d + ` L${x + w} ${y + h} Z`);
  };
  set(counts);
  return { g, set };
}
/* histogram after a point transform T (array of 256 output levels): counts move with their pixels */
const mapHist = (h, T) => { const o = new Array(256).fill(0); for (let r = 0; r < 256; r++) o[clamp(Math.round(T[r]), 0, 255)] += h[r]; return o; };
const lutOf = (f) => Array.from({ length: 256 }, (_, r) => clamp(f(r), 0, 255));
const eqLUT = (h) => { const n = h.reduce((a, b) => a + b, 0); let c = 0; return h.map((v) => { c += v; return roundHalfUp((255 * c) / n); }); };

/* a real photo (assets/*.webp) with an optional live lookup table (an SVG filter: exact per pixel, sRGB).
   returns {g, img, set(T)} where T is an array of 256 output levels (0..255) */
function photo(S, key, x, y, w, h, o = {}) {
  const g = S.g();
  let flt = null, funcs = [];
  if (o.lut) {
    flt = S.el('filter', { 'color-interpolation-filters': 'sRGB', x: 0, y: 0, width: 1, height: 1, filterUnits: 'objectBoundingBox' });
    const ct = S.el('feComponentTransfer', {}, flt);
    funcs = ['feFuncR', 'feFuncG', 'feFuncB'].map((f) => S.el(f, { type: 'table' }, ct));
  }
  if (o.frame !== false) S.el('rect', { x: x - 3, y: y - 3, width: w + 6, height: h + 6, rx: 6, fill: 'none', stroke: o.stroke || '#2b3647', 'stroke-width': 2 }, g);
  const img = S.el('image', { href: IMGS[key], x, y, width: w, height: h, preserveAspectRatio: 'none', 'image-rendering': o.pixel ? 'pixelated' : null, style: o.pixel ? 'image-rendering:pixelated' : null }, g);
  if (flt) img.setAttribute('filter', `url(#${flt.id})`);
  if (o.label) txt(S, x + w / 2, y + h + 28, o.label, { size: o.lsize || 18, color: o.lcol || C.muted, anchor: 'middle', weight: 600 }, g);
  const set = (T) => { const s = T.map((v) => (clamp(v, 0, 255) / 255).toFixed(4)).join(' '); funcs.forEach((f) => f.setAttribute('tableValues', s)); };
  if (o.lut && Array.isArray(o.lut)) set(o.lut);
  return { g, img, set, x, y, w, h };
}

/* transfer-curve plot s = T(r) over 0..L−1 on both axes; returns {g, X, Y, line, set(fn or array)} */
function tplot(S, x, y, w, h, o = {}) {
  const L = o.L || 256, g = S.g();
  S.el('rect', { x, y, width: w, height: h, rx: 8, fill: '#0e141e', stroke: '#222c3b' }, g);
  const X = (r) => x + (r / (L - 1)) * w, Y = (s) => y + h - (s / (L - 1)) * h;
  if (o.diag !== false) S.el('line', { x1: X(0), y1: Y(0), x2: X(L - 1), y2: Y(L - 1), stroke: '#2c3a4e', 'stroke-width': 1.6, 'stroke-dasharray': '6 6' }, g);
  (o.ticks || [0, L - 1]).forEach((v) => { txt(S, X(v), y + h + 22, String(v), { size: 15, color: C.muted, anchor: 'middle' }, g); txt(S, x - 8, Y(v) + 5, String(v), { size: 15, color: C.muted, anchor: 'end' }, g); });
  txt(S, x + w, y + h + 44, o.xl || 'input r →', { size: 16, color: C.muted, anchor: 'end' }, g);
  txt(S, x + 6, y - 10, o.yl || 'output s ↑', { size: 16, color: C.muted }, g);
  const line = S.el('polyline', { fill: 'none', stroke: o.color || C.amb, 'stroke-width': 4, 'stroke-linejoin': 'round' }, g);
  const set = (f) => { const pts = []; const n = o.n || 255; for (let k = 0; k <= n; k++) { const r = ((L - 1) * k) / n; const s = typeof f === 'function' ? f(r) : f[Math.round(r)]; pts.push(`${X(r).toFixed(1)},${Y(clamp(s, 0, L - 1)).toFixed(1)}`); } line.setAttribute('points', pts.join(' ')); };
  if (o.f) set(o.f);
  return { g, X, Y, line, set };
}

/* an fx-991CW screen: title line + body (HTML, white-space kept) */
function lcd(S, x, y, w, h, title, body, t0, t1) {
  const fo = html(S, x, y, w, h, `<div class="lcdw"><div class="lcd"><span class="t">${title}</span>${body}</div></div>`);
  if (t0 !== undefined) { fo.style.opacity = 0; S.slideIn(fo, t0, 0.6, 0, 14); if (t1) S.out(fo, t1, 0.4); }
  return fo;
}
/* key-press line: "[SHIFT] [4]" → key caps; SHIFT is gold */
const keysHTML = (s) => s.replace(/\[([^\]]+)\]/g, (_m, k) => `<kbd${k === 'SHIFT' ? ' class="sh"' : ''}>${k}</kbd>`);
function keyBox(S, x, y, w, h, lines, t0, t1) {
  const fo = html(S, x, y, w, h, `<div class="keys">${lines.map((l) => `<div>${keysHTML(l)}</div>`).join('')}</div>`);
  if (t0 !== undefined) { fo.style.opacity = 0; S.slideIn(fo, t0, 0.6, 0, 14); if (t1) S.out(fo, t1, 0.4); }
  return fo;
}
/* a "what the symbols mean" box */
function decode(S, x, y, w, h, items, t0, t1, title = 'Reading the symbols') {
  const fo = html(S, x, y, w, h, `<div class="decode"><div class="h">${title}</div>${items.map((s) => `<div>${rt(s)}</div>`).join('')}</div>`);
  if (t0 !== undefined) { fo.style.opacity = 0; S.slideIn(fo, t0, 0.6, 0, 14); if (t1) S.out(fo, t1, 0.4); }
  return fo;
}
/* a data table on the stage: head = [..], rows = [[..]], rows appear one by one from t0 every dt */
function dtable(S, x, y, w, head, rows, t0, dt = 0.8, o = {}) {
  const inner = `<table class="dtbl"><thead><tr>${head.map((hh, k) => `<th${k === 0 && o.left ? ' class="l"' : ''}>${rt(String(hh))}</th>`).join('')}</tr></thead><tbody>${rows.map((r, i) => `<tr data-r="${i}">${r.map((c, k) => `<td${k === 0 && o.left ? ' class="l"' : ''}>${rt(String(c))}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
  const hgt = o.h || Math.ceil(measureHTML(inner, w)) + 6;
  const fo = html(S, x, y, w, hgt, inner);
  if (t0 !== undefined) {
    fo.style.opacity = 0; S.fade(fo, t0, 0.4);
    const trs = fo.querySelectorAll('tbody tr');
    trs.forEach((tr, i) => { tr.id = tr.id || 'e' + uid++; tr.style.opacity = 0; S.fade(tr, t0 + 0.3 + i * dt, 0.4); });
    if (o.cols) { // columns revealed later: o.cols = [[colIndex, t]]
      o.cols.forEach(([k, t]) => fo.querySelectorAll(`tr > :nth-child(${k + 1})`).forEach((c) => { c.id = c.id || 'e' + uid++; c.style.opacity = 0; S.fade(c, t, 0.4); }));
    }
  }
  return fo;
}
/* the four "how many" numbers of a k-bit image */
const levels = (k) => 2 ** k;

/* pixel neighbourhood picture: a grid of n×n squares centred on p, marking sets of offsets with colours */
function hood(S, x, y, cs, sets, o = {}) {
  const n = o.n || 3, a = Math.floor(n / 2), g = S.g();
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    const di = i - a, dj = j - a;
    const hit = sets.find((s) => s.cells.some(([u, v]) => u === di && v === dj));
    S.el('rect', { x: x + j * cs, y: y + i * cs, width: cs, height: cs, fill: hit ? hit.color : '#121a26', 'fill-opacity': hit ? 0.75 : 1, stroke: '#3a4658', 'stroke-width': 1.5 }, g);
    if (di === 0 && dj === 0) txt(S, x + j * cs + cs / 2, y + i * cs + cs / 2 + 9, 'p', { size: 26, color: '#fff', weight: 800, anchor: 'middle' }, g);
    else if (o.coords) txt(S, x + j * cs + cs / 2, y + i * cs + cs / 2 + 6, `(x${di ? (di > 0 ? '+' : '−') + Math.abs(di) : ''}, y${dj ? (dj > 0 ? '+' : '−') + Math.abs(dj) : ''})`, { size: Math.min(15, cs * 0.17), color: hit ? '#0b0f16' : C.muted, anchor: 'middle', weight: 600 }, g);
  }
  return g;
}
const N4 = [[-1, 0], [1, 0], [0, -1], [0, 1]], ND = [[-1, -1], [-1, 1], [1, -1], [1, 1]], N8 = N4.concat(ND);

/* the past-paper stop source with marks, e.g. src('Midsem 2023-24 Q2(a)', 5) */
const srcM = (s, marks) => (marks ? `${s} · ${marks} marks` : s);

/* bullet list revealed item by item: items = [[t, html]]; returns the group */
function bullets(S, x, y, w, items, o = {}) {
  const g = S.g(); let yy = y;
  items.forEach(([t, s]) => {
    const inner = `<div class="bl" style="font-size:${o.size || 22}px;line-height:1.42;color:${o.color || '#e7edf5'}">${o.mark === false ? '' : `<span style="color:${o.mc || C.amb};font-weight:800;margin-right:10px">${o.mark || '•'}</span>`}${rt(s)}</div>`;
    const h = Math.ceil(measureHTML(inner, w)) + (o.gap ?? 10);
    const fo = html(S, x, yy, w, h, inner, '', g); fo.style.opacity = 0; S.slideIn(fo, t, 0.5, 0, 10);
    yy += h;
  });
  return g;
}
/* a card with a title and body text */
function card(S, x, y, w, h, title, body, t0, col = C.volt, t1) {
  const fo = html(S, x, y, w, h, `<div style="height:100%;background:rgba(15,22,33,.92);border:1px solid ${col};border-radius:14px;padding:12px 16px;color:#e7edf5;font-size:20px;line-height:1.4"><div style="font-weight:800;color:${col};margin-bottom:6px">${rt(title)}</div>${rt(body)}</div>`);
  if (t0 !== undefined) { fo.style.opacity = 0; S.slideIn(fo, t0, 0.6, 0, 12); if (t1) S.out(fo, t1, 0.4); }
  return fo;
}
