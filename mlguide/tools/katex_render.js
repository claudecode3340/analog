// Pre-render all \( … \) and \[ … \] maths in an HTML file with KaTeX (build time).
// Skips <pre>, <code>, <script>, <style>, <textarea>. Exits non-zero on any LaTeX error.
const fs = require("fs"), katex = require("katex");
const [, , inF, outF] = process.argv;
let html = fs.readFileSync(inF, "utf8");
const macros = {
  "\\R": "\\mathbb{R}", "\\E": "\\mathbb{E}", "\\Var": "\\operatorname{Var}", "\\Cov": "\\operatorname{Cov}",
  "\\argmin": "\\operatorname*{argmin}", "\\argmax": "\\operatorname*{argmax}", "\\Pr": "\\operatorname{Pr}",
  "\\RSS": "\\mathrm{RSS}", "\\TSS": "\\mathrm{TSS}", "\\MSE": "\\mathrm{MSE}", "\\SE": "\\mathrm{SE}",
  "\\bx": "\\mathbf{x}", "\\by": "\\mathbf{y}", "\\bX": "\\mathbf{X}", "\\bw": "\\mathbf{w}", "\\bb": "\\mathbf{b}",
  "\\bh": "\\mathbf{h}", "\\bz": "\\mathbf{z}", "\\bW": "\\mathbf{W}", "\\bbeta": "\\boldsymbol{\\beta}",
  "\\bphi": "\\boldsymbol{\\phi}", "\\btheta": "\\boldsymbol{\\theta}", "\\bmu": "\\boldsymbol{\\mu}",
  "\\bOmega": "\\boldsymbol{\\Omega}", "\\bSigma": "\\boldsymbol{\\Sigma}", "\\T": "^{\\mathsf{T}}",
  "\\ReLU": "\\operatorname{ReLU}", "\\sig": "\\operatorname{sig}", "\\softmax": "\\operatorname{softmax}",
  "\\Norm": "\\operatorname{Norm}", "\\Bern": "\\operatorname{Bern}", "\\Cat": "\\operatorname{Cat}"
};
const dec = s => s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&");
const errors = [];
function render(tex, display, ctx) {
  try { return katex.renderToString(dec(tex), { displayMode: display, throwOnError: true, strict: "ignore", macros, trust: false }); }
  catch (e) { errors.push(`${e.message}\n   in: ${tex.slice(0, 160)}\n   near: ${ctx}`); return `<span style="color:red">[maths error]</span>`; }
}
const protect = /<(pre|code|script|style|textarea)\b[^>]*>[\s\S]*?<\/\1>/gi;
let out = "", last = 0, m;
function proc(chunk) {
  return chunk
    .replace(/\\\[([\s\S]+?)\\\]/g, (a, x, off) => render(x, true, chunk.slice(Math.max(0, off - 80), off).replace(/\s+/g, " ")))
    .replace(/\\\(([\s\S]+?)\\\)/g, (a, x, off) => render(x, false, chunk.slice(Math.max(0, off - 80), off).replace(/\s+/g, " ")));
}
while ((m = protect.exec(html))) { out += proc(html.slice(last, m.index)) + m[0]; last = m.index + m[0].length; }
out += proc(html.slice(last));
fs.writeFileSync(outF, out);
if (errors.length) { console.error(errors.length + " maths error(s):\n" + errors.join("\n")); process.exit(2); }
console.log("katex ok");
