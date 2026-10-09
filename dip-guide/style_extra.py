"""CSS added to the guide: no scrollbars under formulas, a 24-inch-monitor layout, and the new teaching components."""
CSS = r'''
/* ── formulas never get scrollbars: let them take the room they need ── */
mjx-container, mjx-container[jax="SVG"]:not([display="true"]){overflow:visible!important;max-width:none!important}
.eq{overflow:visible!important}
.box p mjx-container{margin:2px 0}

/* ── 24-inch monitor (1920 px): wider page, bigger, airier text ── */
@media (min-width:1500px){
  body{font-size:18.5px;line-height:1.66}
  .shell{max-width:118rem;grid-template-columns:17rem minmax(0,1fr);gap:48px}
  main{padding-inline:8px;max-width:100rem}
  h2{font-size:2rem} h3{font-size:1.4rem;margin-top:2.2em}
}

/* ── teaching block: one idea at a time ── */
.lesson{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:22px 26px;margin:22px 0}
.lesson h4{font-family:var(--font-display);font-size:1.25rem;margin:0 0 6px;display:flex;align-items:center;gap:10px}
.lesson .ltag{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.06em;background:var(--accent-soft);color:var(--accent);border-radius:999px;padding:2px 10px}
.lesson p.what{font-size:1.12rem;margin:0 0 14px;color:var(--ink)}
.lesson .use{margin-top:16px;padding:10px 14px;border-radius:10px;background:var(--violet-soft);border-left:4px solid var(--violet)}
.lesson .cols{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:34px;align-items:start}
.lesson .cols > div > p:first-child{margin-top:0}
.lesson .formula{font-size:1.08rem;padding:10px 16px;background:var(--surface-2);border-radius:10px;margin:10px 0}
.lesson .formula .say{display:block;font-size:.95rem;color:var(--muted);margin-top:4px}
.lesson ol.how{margin:8px 0 4px;padding-left:1.4em}.lesson ol.how li{margin:7px 0}
.lesson .trap{margin-top:12px;padding:10px 14px;border-radius:10px;background:var(--trap-soft);border-left:4px solid var(--trap)}
.lesson .trap b:first-child{color:var(--trap)}

/* ── pixel-grid pictures ── */
.figrow{display:flex;flex-wrap:wrap;gap:26px;align-items:flex-start;margin:12px 0}
.gfig{margin:0;display:inline-flex;flex-direction:column;align-items:center}
.gfig figcaption{font-size:.95rem;color:var(--muted);margin-top:6px;max-width:300px;text-align:center;line-height:1.35}
.gsvg{display:block;height:auto}
.gsvg .g-cell{fill:var(--surface);stroke:var(--line);stroke-width:1.5}
.gsvg .g-out{fill:var(--surface-2)}
.gsvg .g-in{fill:#cfe8ff}
.gsvg .g-path{fill:#ffe08a}
.gsvg .g-p,.gsvg .g-q{fill:#ffc56b}
.gsvg .g-block{fill:#ffc9c2}
.gsvg .g-ctr{fill:#9aa6b5}
.gsvg .g-n4{fill:#9fe0b5}.gsvg .g-nd{fill:#ffb4a8}.gsvg .g-n8{fill:#cdbdff}
.gsvg .g-c1{fill:#9fe0b5}.gsvg .g-c2{fill:#ffd59a}.gsvg .g-c3{fill:#c9b8ff}.gsvg .g-c4{fill:#a7dcf5}
.gsvg .g-hl{fill:#ffe08a}.gsvg .g-c5{fill:#f7b2d3}
.gsvg .g-link{stroke:#c2410c;stroke-width:4;stroke-linecap:round;opacity:.85}
.gsvg .g-val{font-family:var(--font-mono);font-size:17px;dominant-baseline:auto;font-weight:600;text-anchor:middle;fill:var(--ink)}
.gsvg .g-val.dk{fill:#141922}.gsvg .g-val.mu{fill:var(--muted);font-weight:500}
.gsvg .g-idx{font-family:var(--font-mono);font-size:12px;text-anchor:middle;fill:var(--muted)}
.gsvg .g-small{font-family:var(--font-mono);font-size:10px;fill:#5b6575}
.gsvg .g-arrow{stroke:#c2410c;stroke-width:3.2;fill:none}
.gsvg .g-arrowhead{fill:#c2410c}
.gsvg .g-stepc{fill:#c2410c}.gsvg .g-step{font-family:var(--font-mono);font-size:10.5px;font-weight:700;text-anchor:middle;fill:#fff}
.gsvg .g-cross{stroke:#d92d20;stroke-width:3;stroke-dasharray:6 5}
.gsvg .g-crossc{fill:#d92d20}.gsvg .g-crosst{font-size:15px;font-weight:800;text-anchor:middle;fill:#fff}
.gsvg .g-ring{fill:none;stroke:#d92d20;stroke-width:3.5}

/* ── step-by-step solutions ── */
.walk{display:flex;flex-direction:column;gap:14px;margin:10px 0 6px}
.wstep{display:grid;grid-template-columns:40px minmax(0,1fr) auto;gap:16px;align-items:start;padding:14px 16px;background:var(--surface-2);border-radius:12px}
.wstep .wn{width:34px;height:34px;border-radius:50%;background:var(--accent);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-family:var(--font-mono)}
.wstep .wh{font-weight:700;margin-bottom:3px}
.wstep .wf{justify-self:end}
.ansbig{font-size:1.1rem;padding:12px 16px;border-radius:10px;background:var(--ok-soft);border-left:4px solid var(--ok);margin-top:10px}
.lab-help{background:var(--violet-soft);border-radius:12px;padding:14px 18px;margin:18px 0 8px}
.lab-help ol{margin:6px 0 0;padding-left:1.3em}
.legend{display:flex;flex-wrap:wrap;gap:16px;font-size:.95rem;margin:8px 0}
.lesson h4 > span sub,.lesson h4 > span sup{font-size:.7em}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{display:inline-block;width:18px;height:18px;border-radius:4px;border:1px solid var(--line)}
'''

CSS += r'''
.gsvg .a-bg{fill:var(--surface)}.gsvg .a-grid{stroke:var(--line);stroke-width:1}
.gsvg .a-axis{stroke:var(--muted);stroke-width:1.6}.gsvg .a-lab{font-size:12px;fill:var(--muted);font-family:var(--font-mono)}
.gsvg .a-o{fill:var(--muted)}
.gsvg .a-before{fill:#9aa6b5;fill-opacity:.35;stroke:#9aa6b5;stroke-width:1.5}
.gsvg .a-after{fill:#f59e0b;fill-opacity:.55;stroke:#c2410c;stroke-width:2}
.lesson table.t{margin:8px 0}
.mini{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px;margin:12px 0}
.mini > div{background:var(--surface-2);border-radius:12px;padding:12px 14px}
.mini h5{margin:0 0 6px;font-size:1.02rem}
'''
