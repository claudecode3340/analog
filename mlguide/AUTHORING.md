# Authoring guide · ML Foundations, Months 1–3

You are writing lessons for a single-file interactive study guide. Read this whole file, then read the
reference lesson `lessons/s0-how.html` (it uses every component) before writing anything.

## 1. The learner (non-negotiable)

- 4th-year Indian ECE/EEE undergraduate on a **Mac**. Strong at DSP/signals/communications maths, but
  **knows almost no Python and no PyTorch**, and has done none of these books or courses.
- Goal: become an exceptional, hireable ML / deep-learning / computer-vision engineer.
- What they told us they love (from their DIP, CME 295 and Hands-On-ML guides):
  - **Exact worked examples showing how every number changes, step by step.** Matrices written out as real
    matrices (`\begin{pmatrix}…\end{pmatrix}`, or the `.mgrid` HTML grids with highlighted cells when you want
    to show which entries combine). Nothing skipped, nothing cramped.
  - **Maths notation made easy**: every symbol read out loud the first time ("\(\hat\beta_1\) is read
    *beta-one-hat*: our *estimate* of the slope"). A formula is always followed by a plain-words reading and a
    tiny numeric example.
  - **Prerequisites taught just in time**, never assumed. If you need something not taught earlier, teach it
    inline in a short "New in this lesson" box (or link to the lesson that teaches it).
  - **Practice on everything**: predict-then-run cells, auto-checked exercises with hints, every book exercise
    with layered solutions, quizzes, flashcards.
  - **Visual explanations**: the books' own figures (cropped, already available) plus interactive widgets.
  - "Guide me like a kid": explicit, warm, patient, concrete. Short sentences. Second person. British spelling.
    Never "obviously", "simply", "it is easy to see". Never skip a step because it is "standard".
- Thoroughness beats brevity. A typical book-section lesson is **4,000–9,000 words** of prose plus
  10–25 code cells, 2–6 widgets, worked examples, 6–10 quiz questions and 8–15 flashcards. Exercise lessons
  contain **every** exercise of the book section (conceptual and applied) with full solutions.

## 2. Files you own (never edit anyone else's)

- `lessons/<lesson-id>.html` — exactly one `<section class="lesson" id="<lesson-id>" data-book="…">`.
  The id, title, month, week and kind come from `curriculum.json`; the build adds the header (chips + title).
  Start the section with `<p class="lede">` (2–3 sentences: why this lesson matters). `data-book` is a short
  source string such as `ISLP §3.1, pp. 70–80` or `Prince Ch. 3, pp. 25–40`.
- `widgets/<lesson-id>.js` — your interactive widgets. Register with `G.widget("<lesson-id>-name", fn)`.
  Prefix every widget name with your lesson id.
- `glossary/<lesson-id>.json` — `{ "key": {"term": "…", "def": "HTML with \\(maths\\)", "at": "<lesson-id>"} }`
  for the important terms you introduce (5–25 per lesson). Use `<dfn data-g="key">term</dfn>` in the text at
  the term's defining sentence to get a hover definition.
- `data/<file>` — only if your lesson needs a data file that is not already there (check first; ISLP datasets
  are already bundled — see §6). Keep files small (< 300 KB).
- All element ids inside your lesson must start with your lesson id or a prefix derived from it:
  cells `c-<lid>-NN`, exercises `x-<lid>-NN`, book problems `p-<lid>-NN`, headings `<lid>-slug`.

Do not edit `src/`, `tools/`, `curriculum.json`, other people's lessons, or `lessons/s0-how.html`.

## 3. Lesson structure (the rhythm)

1. `<p class="lede">` then optionally `<div class="uses"><b>You'll use</b> <a href="#np1">NumPy I</a> …</div>`
   and a `<div class="goals"><h4>By the end of this lesson you can</h4><ul>…</ul></div>`.
2. For book lessons, a `<div class="callout book"><blockquote>one or two sentences quoted from the book that
   start this section</blockquote><cite>ISLP p. 70</cite></div>` (short quotes only).
3. Sections `<h3 id="<lid>-slug">` in teaching order. Inside each idea: **plain words → precise version
   (formula in a `.mathblock`) → read it aloud → worked example with numbers → figure from the book →
   runnable code (with a prediction before the important cells) → widget (when a picture that moves helps) →
   pitfall box**.
4. Practice: auto-checked exercises (`.ex`) for code skills; book exercises (`.prob`) for the book's own
   problems; a `.quiz`; a `.cards` block; a `.checklist` of "I can…" items. The build appends the
   "I can do this lesson without help" bar and the notebook download.

Book lessons follow the book's section order and cover **everything** in the section: every equation, every
example, every figure (all figures of your chapter are in `figs/`), every table worth having (re-type tables as
HTML `.tw > table.t`). Explain more than the book does, never less. Where the book is terse (ISLP often is),
add the derivation; where Prince refers to a notebook, implement that notebook's idea as cells/exercises.

## 4. Components (exact markup)

Look at `lessons/s0-how.html` for live examples of each.

**Maths.** Inline `\( … \)`, display `\[ … \]` (KaTeX, pre-rendered at build). In HTML source write `<` as
`\lt` or `&lt;` inside maths, `&` as `&amp;` or plain `&` inside matrices (both work). Available macros:
`\R \E \Var \Cov \argmin \argmax \RSS \TSS \MSE \SE \bx \by \bX \bw \bb \bh \bz \bW \bbeta \bphi \btheta \bmu
\bSigma \bOmega \T`(transpose, use as `\bX\T`) `\ReLU \sig \softmax \Norm \Bern \Cat`. Use
`\begin{pmatrix}…\end{pmatrix}` for matrices, `\begin{aligned}…\end{aligned}` for multi-line derivations.
Boxed key formula (collected automatically into the formula sheet):
```html
<div class="mathblock" data-sheet="Least-squares slope"><div class="eqlabel">Least-squares estimates</div>
\[\hat\beta_1=\frac{\sum_i (x_i-\bar x)(y_i-\bar y)}{\sum_i (x_i-\bar x)^2}\]
<p class="say">Read: beta-one-hat equals … (plain words).</p></div>
```
**Symbol table** ("say it as"):
```html
<div class="symbols"><div class="row h"><span>Symbol</span><span>Say it as / meaning</span><span>Tiny example</span></div>
<div class="row"><span class="s">\(x_i\)</span><span>"x sub i": the i-th input</span><span class="eg">\(x_3=81\)</span></div></div>
```
**Worked example** (the heart of the guide; DIP style, every number written out):
```html
<div class="worked" data-reveal><div class="wt">Worked example · <b>title</b></div>
<div class="given">What we are given, with numbers.</div>
<ol class="steps"><li><div>Step text with \(maths\).<span class="why">why this step</span></div></li>…</ol>
<div class="result">\(\hat\beta_1 = 0.0475\)</div></div>
```
`data-reveal` shows one step at a time (use it for examples the learner should try to continue). Use
`<span class="hlc">…</span>` (yellow), `hlb` (blue), `hlr` (red), `hlg` (green) to colour-link numbers across
steps. To show a matrix operation cell by cell, use HTML grids:
```html
<div class="mrow"><span><span class="mgrid" style="grid-template-columns:repeat(2,auto)"><span class="h1">1</span><span>2</span><span>3</span><span>4</span></span><span class="lab">A</span></span>
<span class="op">×</span> … <span class="op">=</span> …</div>
```
**Book figure** (all figures of ISLP ch.1–6 and Prince ch.1–7 + appendices 23–24 exist as `figs/<id>.webp`;
see `figs/manifest.json` for their captions; LOOK at the images before writing about them):
```html
<figure class="book" data-fig="islp-3.1"><figcaption>Teaching caption: what to look at, and what it shows.</figcaption></figure>
```
Add `class="book small"` for small figures. The build adds the image, a "From the book" tag and the original
caption.

**Callouts**: `<div class="callout key|intuition|analogy|pitfall|ece|book|mac|exam"><p>…</p></div>` (the label
is automatic; or add `<div class="ct">Custom label</div>` first). Use `ece` to connect to the learner's
DSP/communications background (e.g. least squares ↔ matched filtering, convolution ↔ FIR filters). Use `exam`
for "how this shows up in ML interviews".

**Python cell** (runs in the browser via Pyodide; the build harness also runs it in CPython to make the
reference output, so it MUST run cleanly):
```html
<div class="py" id="c-<lid>-03"><pre class="src">
import numpy as np
x = np.array([1, 2, 3])
x * 2
</pre><div class="pynote"><b>Read the output:</b> explain what the learner sees and what to change next.</div></div>
```
Attributes: `data-mode="setup"` (rebuilds the lesson's state; put one at the start of every lesson whose cells
need data/imports so each lesson stands alone), `data-mode="expect-error" data-error="ValueError"` (a cell that
fails on purpose), `data-mode="local"` (PyTorch: runs only on the Mac; the harness still runs it here with
CPU PyTorch to produce the reference output). Cells in a lesson share one namespace, top to bottom, including
cells inside `<details>`. The last expression is displayed (pandas DataFrames render as tables). matplotlib
figures are captured automatically (don't call `plt.savefig`; `plt.show()` is harmless). Keep each cell
small (≤ 25 lines) and fast (< 5 s). Escape `<`, `>` and `&` in code as `&lt;`, `&gt;`, `&amp;`.

**Predict-first** (must come immediately before the `.py` or `.widget` it gates):
```html
<div class="predict" data-correct="2"><p>What will this print?</p><ol class="opts"><li>A</li><li>B</li><li>C</li></ol>
<div class="why">Why B is right, and what the tempting wrong answer misunderstands.</div></div>
```
**Exercise** (auto-checked; the harness checks that the starter FAILS and the solution PASSES):
```html
<div class="ex" id="x-<lid>-02" data-title="short title"><div class="task"><p>What to do, with an example input→output.</p></div>
<pre class="src">
def f(x):
    ...   # your code here
</pre>
<pre class="check">
assert f(2) == 4, f"f(2) should be 4, got {f(2)}"
</pre>
<div class="hint"><p>Gentle hint.</p></div><div class="hint"><p>Stronger hint.</p></div>
<pre class="solution">
def f(x):
    return 2 * x
</pre><div class="explain"><p>Why the solution works.</p></div></div>
```
Checks must test behaviour on several inputs (including edge cases), with assert messages that say what was
expected and what was got. Compare against NumPy/scikit-learn/statsmodels where possible.

**Book exercise** (pen-and-paper or applied; DIP-style layered answers):
```html
<div class="prob" id="p-<lid>-07" data-src="ISLP 3.7 · Conceptual 3" data-title="Salary model with interactions">
<div class="stmt"><p>The exercise as in the book (re-typed faithfully, with the book's numbers).</p></div>
<div class="ansin" data-answer="137.1" data-tol="0.01" data-unit="thousand $"></div>   (only for single-number answers)
<details class="hintd"><summary>Hint</summary><div>…</div></details>
<details class="ans"><summary>Final answer</summary><div>…</div></details>
<details class="sol"><summary>Full solution, step by step</summary><div>…worked steps, and for applied exercises
the code as .py cells (they are run and verified by the harness), with interpretation of the output…</div></details>
<details class="mist"><summary>Common mistakes</summary><div>…</div></details></div>
```
Applied ISLP exercises: solve them for real with code cells inside `details.sol` and explain the numbers the
code prints. Prince problems: full derivations with every algebra step; numeric checks in a code cell where
useful.

**Quiz** (6–10 questions; mix concept MCQs, numeric, one open question; each `.why` explains every option):
```html
<div class="quiz">
<div class="q" data-type="mcq" data-correct="1"><p class="stem">…</p><ol class="opts"><li>…</li>…</ol><div class="why">…</div></div>
<div class="q" data-type="num" data-answer="0.5" data-tol="0.01" data-unit=""><p class="stem">…</p><div class="why">…</div></div>
<div class="q" data-type="open"><p class="stem">…</p><div class="model">model answer</div></div></div>
```
**Flashcards** (8–15, atomic: one fact or formula each; maths allowed):
```html
<div class="cards"><div class="fc"><div class="f">front</div><div class="b">back</div></div>…</div>
```
**Checklist**: `<div class="checklist"><label><input type="checkbox"> I can …</label>…</div>`
**Tables**: `<div class="tw"><table class="t"><thead>…</thead><tbody>…</tbody></table></div>` (`td class="n"` for numbers).
**Glossary term**: `<dfn data-g="bias-variance">bias–variance trade-off</dfn>`.
**Widget**:
```html
<div class="widget" data-w="isl2-2-flex" data-title="Flexibility vs test error" data-args='{"seed":1}'>
<div class="wn">What to try and what they should notice.</div></div>
```
Write the widget in `widgets/<lid>.js`. Look at `widgets/s0-how.js`. Helpers on `G` (see `src/runtime.js`):
`G.plot(parent,{w,h,x:[a,b],y:[a,b],xlabel,ylabel})` returns `{svg,layer,X,Y,clear,line(pts,attrs),dot(x,y,attrs),text(x,y,t,attrs)}`;
`G.slider(parent,{label,min,max,step,value,fmt,onChange})`; `G.seg(parent,[[val,label],…],val,onChange)`;
`G.button(parent,label,fn)`; `G.rng(seed)` (seeded uniform), `G.randn(rng)`; `G.tex(latex,display)` → HTML;
`G.fmt(x,d)`; `G.el(tag,cls,html)`; `G.svg(tag,attrs,parent)`. Colours: always CSS variables
(`var(--accent)`, `var(--isl)`, `var(--udl)`, `var(--tool)`, `var(--math)`, `var(--proj)`, `var(--bad)`,
`var(--good)`, `var(--warn)`, `var(--muted)`, `var(--line)`, `var(--ink)`), so dark mode works. Widgets must
be deterministic (seeded), compute live (no network), open in an instructive default state, and be readable at
390px wide (SVG with viewBox scales). Use a `.readout` div for live numbers. Good widgets show the *mechanism*:
residuals as red segments, a sliding window, a loss surface with the current point, a decision boundary moving.

## 5. Writing rules

- Plain words first, then the precise version. Define every term at first use. One idea per paragraph.
- Read every new symbol aloud. Show a tiny numeric example right after every formula.
- Prefer concrete numbers from the book's datasets (Advertising, Income, Auto, Default, Smarket…).
- When code appears, explain each new Python construct the first time it is used ("`df.loc[...]` picks rows
  by label…"). The learner knows only what earlier lessons taught (see `curriculum.json` for the order).
- Use the learner's ECE background where it genuinely helps (callout `ece`), not as decoration.
- Interview relevance (callout `exam`) where a topic is a classic interview question.
- Never invent book content. Book page numbers in `data-book`/citations must be correct (ISLP PDF page =
  book page + 15 early on, drifting to +12 by ch.6 — use the running page numbers; Prince PDF page = book page + 14).
- Quote the books only briefly (a sentence or two at a time).
- No emoji. No lorem ipsum. No "TODO".

## 6. Data and code environment

- Browser: Pyodide 0.27.7 with numpy 2.0, pandas 2.2, matplotlib 3.8, scikit-learn 1.6, statsmodels 0.14,
  scipy, and the **ISLP** package (`from ISLP import load_data` works for Auto, Boston, Carseats, College,
  Credit, Default, Hitters, Portfolio, Smarket, Weekly, Caravan, OJ, Wage; `from ISLP.models import
  ModelSpec as MS, summarize, poly` works). No internet from Python. No PyTorch in the browser.
- Files in `data/` are copied into the working directory (both browser and harness), so
  `pd.read_csv('Advertising.csv')` works if `data/Advertising.csv` exists. Existing data files: run `ls data/`.
  ISLP's `Advertising.csv`, `Income1.csv`, `Income2.csv` are not in the ISLP package: if you need them,
  download from `https://www.statlearning.com/s/Advertising.csv` (and similar) with curl into `data/`.
- Harness Python (to verify your cells): activate
  `source /tmp/claude-0/-home-user-analog/f43a8c4b-e900-5b65-9888-7cda2c0d5ebc/scratchpad/mlenv/bin/activate`
  (Python 3.12 with the same library versions + ISLP + CPU PyTorch + PyMuPDF).
- Book text (for reading; `pdftotext -layout`):
  `/tmp/claude-0/-home-user-analog/f43a8c4b-e900-5b65-9888-7cda2c0d5ebc/scratchpad/bookstxt/ISLP_James_et_al_2023.txt`,
  `/tmp/claude-0/-home-user-analog/f43a8c4b-e900-5b65-9888-7cda2c0d5ebc/scratchpad/bookstxt/UDL_Prince_2025.txt`.
  For equations, render the PDF pages to images and look at them:
  PDFs in `/tmp/claude-0/-home-user-analog/f43a8c4b-e900-5b65-9888-7cda2c0d5ebc/scratchpad/books/`
  (`python -c "import pymupdf; d=pymupdf.open(PDF); d[PAGE].get_pixmap(dpi=110).save('/tmp/…/p.png')"`, then
  view the PNG). Do not run anything from inside the books folder; write scratch files under
  `/tmp/claude-0/-home-user-analog/f43a8c4b-e900-5b65-9888-7cda2c0d5ebc/scratchpad/work-<your-letter>/`.

## 7. Verify before you finish (mandatory)

```bash
source /tmp/claude-0/-home-user-analog/f43a8c4b-e900-5b65-9888-7cda2c0d5ebc/scratchpad/mlenv/bin/activate
cd /home/user/analog/mlguide
python tools/run_cells.py <lid1> <lid2>            # every cell runs; every exercise: starter fails, solution passes
python tools/build.py --only <lid1>,<lid2>         # validation + KaTeX; writes dist/preview-<ids>.html
node tools/shot.js dist/preview-<lid1>+<lid2>.html <lid1>   # screenshots in build/shots/<lid1>-NN.png
```
Fix every ERROR the build prints for your lessons (it also lists "lessons not written yet" for others: ignore
those, and ignore broken links that point at other lessons that don't exist yet only if the target id is a
lesson id in curriculum.json). LOOK at several screenshots (Read tool) including the dark and phone ones; fix
anything cramped, overflowing or ugly. Re-run until clean. Then report: what you wrote (lessons, word count,
cells, exercises, book exercises covered, widgets), and anything you could not do.
