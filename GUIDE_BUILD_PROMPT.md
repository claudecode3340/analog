# Prompt: build an exam study guide for CMOS digital circuits (Lectures 23–34)

Use this prompt to rebuild, or extend, the study guides in this repository. It records the sources that were read, the research done, the plan, the build pipeline, the teaching design, the checks run and the fixes made along the way.

---

## 1. Role and goal

You are a patient tutor and a careful engineer. A student taking *Analog & Digital VLSI Design (EEE/INSTR F313, BITS Pilani Goa)* has open-book quizzes on Lectures 23–34. The student found the lecture notes, and an earlier guide, hard to follow. Their goals, in their words:

- "Make me understand the lecture first, in short, then teach me."
- "By the end I should be able to solve all the tutorial questions and any question in my exam."
- "Teach it as if to a kid, with no prerequisites. Explain the question first, then the theory, then the plan, then solve."
- "Proper figures for everything, beautifully formatted, not congested."
- "Mark anything not taught in my lectures. Add similar Razavi problems and mark the extras as optional."
- "Do full-page screenshot checks, and walk through the guide as a kid. Fix anything a kid would get stuck on."

Deliverables: one HTML page (for phone and browser) and one printable A4 PDF (for the open-book exam) per lecture block. Commit them to the repo.

---

## 2. Sources and how each was read

### 2.1 Student uploads

| Source | Content | How it was read |
|---|---|---|
| `Lecture_25 … interactive.html` (2.9 MB) | An earlier interactive page on switching and delay (capacitances, average-current and exact methods, Example 25.2, problems 3.1–3.8, capstone, Razavi concepts) | Stripped scripts, styles and data URIs with Python; read the ~40 KB of text in full |
| `CMOS_Inverter_Guide_Revised.pdf` (41 pp.) | The student's main guide: Parts 0–4 (L23–L25), worked examples, practice 3.1–3.8 | `pdftotext -layout`; Part 3 (pp. 25–34) read line by line; pages 27–30 viewed as images to judge the figure style |
| `CMOS_Fast_Method.pdf` (20 pp.) | A factorised method for V_IL/V_IH (L23 only) | Text extraction, to reuse its notation |
| `CMOS_Inverter_Formula_Sheets.pdf` | DC and timing formula sheets, including the D(k,T) delay function and the general NMOS discharge integral | Text extraction; adopted its notation (V_T0,n, k_R, D(k,T)) |
| `Lecture_26` (1 handwritten page) | The PLH derivation, equal delays (k_n = k_p and V_Tn = abs(V_Tp)), the slow-input formula τ = √(τ_step² + (τ_r/2)²), a 3-stage ring with C1–C3 | Rendered at 200 dpi, cropped into strips, read visually |
| `Lecture_28` | Pseudo-NMOS, CMOS NOR2/NAND2 and truth tables, (W/L) series/parallel, V_th of NOR2/NAND2 with inputs tied, symmetric results (V_DD+V_T)/3 and (2V_DD−V_T)/3, stick diagrams | 220 dpi render, seven cropped strips at 1.5× zoom |
| `Lecture_29` | Complex gate Y = [A(D+E)+BC]', (W/L)_eq, Euler path, stick diagram | Full page plus zoomed crops |
| `Lecture_30` | t_pd/t_cd, RC low-pass (V_out/V_in = 1/(1+sRC)), the MOSFET RC model (R/k, 2R/k, kC per terminal), R = V_DS,avg/I_DS,avg, INVX1/X2, NAND2X1 capacitances | Full page plus two zoomed crops of the lower half |
| `Lecture_31` | Elmore delay, inverter driving m (and w-sized), d = gh + p, τ = 3RC, FO4 = 15 ps (R = 10 kΩ, C = 0.1 fF), NAND3 t_pdf = 12RC and t_cdf = 9RC | Full page |
| `Lecture_32` | NAND3 and NOR3 driving h identical gates: t_pdf, t_cdf, t_pdr, t_cdr with input patterns; general d = gh + p; logical effort definition; g_NAND3 = 5/3, g_NOR3 = 7/3 | Full page plus five cropped strips |
| `Lecture_33` | Linear delay model d = f + p, f = gh, its graph; inverter d = h + 1; the logical effort table (INV, NAND, NOR, tristate/mux, XOR/XNOR); drive x = C_in/g, INVX1/X2, NAND2X1 | Full page plus strips |
| `Lecture_34` | Limitations (input slope, arrival time, velocity saturation); the 4-stage path (INV 10 → NOR2 x → NAND2 y → INV z → 45); G, F, H, b, B; branching example (F = 36 vs GH = 18); D = D_F + P; equal stage effort f̂ = F^(1/N), D = NF^(1/N) + P; f = C_out/x | Full page plus strips |
| Tutorial 8 | Noise margins (two inverters), design for V_th = 1.4 V, threshold variation, a feedback-NMOS circuit | Text plus page render for the circuit figure. Uploaded twice; `cmp` showed the files were identical |
| Tutorial 9 | Fall time by both methods, delay from an I–V spec, three designs with timing specs, V_DD scaling, self-loading capacitance | Text. Uploaded twice; identical |
| Tutorial 10 | Weste & Harris problems: fanout, FO4, ring oscillator, path arrival-time optimisation (figure), NOR2 Elmore, AOI, NOR-n parasitic, 4x inverter, logical effort with 3× weaker PMOS | Text plus 200 dpi crops of the Q4 figure, which showed X4 has three inputs (a NOR3) |

### 2.2 Textbook research (in the repo)

- **Razavi, *Design of Analog CMOS Integrated Circuits*** (`Design-of-Analog-CMOS-Integrated-Circuits.pdf`, 801 pp.). Extracted the full text and searched it for "NAND", "Elmore", "logical effort", "ring oscillator" and "velocity saturation". Finding: Razavi has no logic gates, Euler paths, Elmore delay or logical effort. Relevant parts:
  - Ch. 2: device capacitances, overlap and junction (C_j, C_jsw), Table 2.1 values, folding (Ex. 2.10), Probs. 2.11 and 2.15, and triode on-resistance R_on = 1/(μC_ox(W/L)V_ov).
  - §15.2, ring oscillators: odd N; "three stages give a period of 6T_D"; a gain of at least 2 per stage is needed to start.
  - §11.2 (p. 461) and §17.2.3 (p. 698), velocity saturation: Fig. 11.3 (velocity vs field, E_crit), Fig. 11.4 (early saturation), Fig. 17.9, and Eq. 11.1/17.25, I_D = WC_ox(V_GS − V_TH)v_sat (current linear in overdrive, independent of L, g_m nearly constant). These pages were found by text search, rendered at 90 dpi and read in full.
- **Weste & Harris** (the source of Tutorial 10; not in the repo). Used from knowledge only, for: unit sizing, the g and p tables, Elmore with fully contacted diffusion, the n² + 2n parasitic delay of NOR-n, best stage effort ≈ 4 (N ≈ log₄F), and AOI21 as "the" AOI. Anything taken from here and not taught in lectures is labelled.
- `Learning RF circuit design from Razavi's book.zip`: listed, holding a markdown export plus the same Razavi PDF. Not needed.

### 2.3 Gaps found between the tutorials and the lectures (told to the student)

- 10–90 % rise/fall times (T9 Q1, Q4, Q5b): defined in the lectures but never derived. Derived here as the same integral with new limits.
- A fall between arbitrary voltages (T9 Q3: 2 V → 0.5 V): uses the linear-only integral.
- Reading k and V_T from an I–V description (T9 Q2).
- T8 Q4(c): the current cannot be a number in µA because only the width ratio is given. Answered per µm of W_n, plus an example.
- T9 Q4: the rise-time method is not specified. Gave the exact result (W_p = 14.8, W_n = 9.8 µm) and the average-current alternative (16.2 and 10.7 µm).
- T10 Q4: X4 is a NOR3 in the figure. The max() for reconvergent paths goes slightly beyond Lecture 34. Optimum ≈ 23.5τ (marked optional).
- T10 Q5: "fully contacted" means the internal node counts as 8C, giving t_pdr = (10 + 5h)RC and t_pdf = (6 + 5h)RC.
- T10 Q6: the gate is not specified. Used AOI21 (8RC fall, 11RC rise); practice P5 covers the AOI22 Euler path.
- T10 Q9: first marked "beyond lectures", then re-marked "in lectures" once Lecture 33's logical effort table arrived.

---

## 3. Verification research (every number was computed, never only hand-derived)

Python scripts in the scratchpad, using only the standard library (no SciPy):

1. **Square-law model** `i_d(k, u, v)` (linear vs saturation) and a **4th-order Runge–Kutta solver** for C dV/dt = −I(V).
2. **Lecture 25/26:**
   - Example 25.2: exact τ_PHL = 0.703 ns and τ_PLH = 1.882 ns, matching the simulation to 5 digits; average-current 0.734 and 1.96 ns; saturated segment 0.247 ns.
   - Fall and rise times: 1.63 and 4.29 ns.
   - Design k values and the capstone: 107, 215 and 112 ps.
   - Razavi 2.11: 26.6 ps and 0.38 ns.
   - New examples: PMOS 0.5 → 2.5 V = 2.68 ns; 3-stage rings at 129 and 193 MHz.
3. **Tutorial 8:** V_IL/V_IH found by bisection on the two lecture equation pairs, then confirmed by **sweeping the VTC numerically** and finding where the slope is −1 (1.064/1.553 V and 1.198/1.696 V). The hand-solvable quadratics (e.g. V_out² + 0.0667V_out − 9.898 = 0) were extracted for the written solution. Threshold-variation corners: 1.29–1.51 V, current −22 %/+24 %.
4. **Tutorial 9:**
   - Q1: 3.70 ns exact, 4.05 ns average.
   - Q2: k = 640 µA/V², V_T = 0.8 V, 0.253 ns.
   - Q3: three minimum-k constraints, giving W_n ≈ 4.8 and W_p ≈ 18.8 µm, rechecked.
   - Q4: the V_DD = 3.3 V rerun.
   - Q5: W_n > 6.00 µm; average rise/fall 0.68/0.62 ns.
5. **Lectures 28–31:**
   - V_th of INV/NOR2/NAND2: 1.385, 1.088, 1.727 V, plus VTC sweeps.
   - Sizing for V_th = 1.65 V: ratios 2.93, 11.7, 0.73.
   - (W/L)_eq = 7/3 and 1.
   - FO4 = 15 ps; 31-stage ring = 2.69 GHz; NOR-n parasitic n² + 2n.
   - T10 Q4 optimum by coordinate descent (ternary search), checked by random perturbation.
6. **Lectures 32–34:**
   - NAND3/NOR3 delays for h = 1 and 4.
   - Drives of X2/X4 gates.
   - Lecture 34 path: G = 20/9, F = 10, f̂ = 1.778, D = 13.1τ, sizes z = 25.3, y = 19.0, x = 17.8, with the back-check equal to 10.
   - Branching F = 36 = GBH.
   - Branched path: F = 80, f̂ = 4.31, D = 17.9τ, C_in 46.4 and 43.1.
   - Unsized path: 14.5τ.
   - Stage count for F = 1000: N = 5, D = 24.9τ.
   - Velocity saturation: 151 vs 115 µA at 0.3 V, and 604 vs 230 µA at 0.6 V.

---

## 4. Plan and teaching design

### 4.1 Structure of every guide

1. **Whole lecture in one page**: a numbered "story" of 8–10 steps plus "the one sentence to remember". (Lecture 25: "the output is a bucket, the transistors are taps; τ ≈ CΔV/I".)
2. **Start from zero** (added later): water analogy for V, I, R and C; units, including the shortcuts fF·V/µA = ns and kΩ·fF = ps; truth tables; De Morgan; the MOSFET in a paragraph; the inverter V_th formula reused later.
3. **Words and symbols that confuse**: a table of reused letters. In Lecture 30, k is a width and not μC_ox W/L; τ = 3RC is a time unit and not τ_PHL; C is a unit capacitance and not C_load; t_pdf = τ_PHL; C_out excludes the gate's own diffusion; and so on.
4. **One section per lecture, picture first**: each idea gets a figure, coloured boxes (blue = memorise, green = intuition, red = traps, purple = "say it out loud" memory hooks, amber = "only if asked / two conventions") and a labelled derivation.
5. **One master method** that unifies the formulas. Lecture 25: x = distance of V_out from the driving transistor's rail; split the trip at x = u; time the saturated piece as a bucket and the linear piece with the ln formula. Lectures 28–34: recipes A–I.
6. **"Which type of question is it?"**: a keyword table (question wording → type → section), a "first 60 seconds" five-step routine, recipe boxes and a "spot the type" drill (cover the answer, then check).
7. **Every tutorial question solved**, then extra practice, then Razavi-style problems.
8. **Exam variants** (Lecture 25): the twists an exam can add (slow input, ring with unequal C, chains, fanout, solving for V_DD), each with its fix.
9. **Open-book sheet plus top traps.**

### 4.2 The five-step template for every question

1. **In plain words**: what is physically happening.
2. **Theory**: which section and formula.
3. **Plan**: the numbers to get first (overdrive, V_DD/2, C in fF, k in µA/V²).
4. **Solve**: region check, then numbers, then a highlighted answer.
5. **Check**: units, the right transistor, sanity, a cross-check by another method or by simulation.

Every question has its full statement, its own figure and all five steps. A script counts the steps and figures per question to enforce this.

### 4.3 Labels

- **In lectures**: taught in the lectures; must know.
- **Beyond lectures**: asked in a tutorial but not taught; explained from scratch.
- **Optional**: Razavi or Weste & Harris extras.

---

## 5. Build pipeline (reproducible)

- `lecture25/build/figs.py`: SVG helpers (`line`, `poly`, `text`, `arrow`, `cap`, `res`, `gnd`, `vdd`, `nmos`, `pmos`, `inverter`, a `Plot` class with axes, bands and ticks, `sub()` for subscripts, `barh()`), the square-law model, the RK4 solver, the `vtc()` sweep, and every Lecture 25/26 figure. It fills `{{FIG_*}}` placeholders in `guide_src.html` and writes `Lecture25_Guide.html`.
- `lecture28_31/build/figs2.py`: imports `figs.py` and adds the gate symbols (inverter, NAND and NOR shapes), schematics, stick diagrams with a second-metal link layer, Euler graphs with numbered edges, RC models, Elmore ladders, logical effort and path figures. It assembles `head2.html` + `body.html` into `guide_src.html` and writes `Lectures28-34_Guide.html`. Content was written as separate HTML parts (`part_*.html`) and spliced in by anchor comments, with asserts that each anchor occurs exactly once.
- **Every curve is computed** (VTCs, discharges, I–V, delay vs W, delay vs N), so the figures match the numbers in the text.
- **HTML**: Inter font; KaTeX 0.16.9 from jsDelivr for maths; design tokens; tables become scrollable below 600 px; print CSS (A4, a page break before each h2, no breaks inside figures or boxes, headings kept with what follows, table rows not split).
- **PDF**: Playwright Chromium waits for KaTeX (`body.dataset.ready`), checks that no `.katex-error` exists, and prints A4 with a page-number footer.
- **Committed and pushed** to branch `claude/pensive-noether-0zmau3`. `.gitignore` excludes `__pycache__`.

---

## 6. Quality checks (repeated after every change)

1. **KaTeX errors = 0** on every build.
2. **Full-page screenshot review**: every PDF page rendered with `pdftoppm` (70–90 dpi), tiled three or four to an image, and read visually. Targeted 110 dpi renders were used for fixes.
3. **Phone check**: a Playwright viewport of 390 px. `scrollWidth` must equal 390. A script hides each top-level block in turn to find whichever one overflows.
4. **Figure preview pages**: all new figures rendered on one page before inserting them, then checked for overlaps.
5. **Structure audit**: a script lists every question with "NOFIG" and its number of steps.
6. **Number audit**: every answer in the text matched to the Python outputs in section 3.

### Student walkthroughs ("as a kid")

- **Pass 1:** clarified the Elmore wording; explained why τ = 3RC; added C_in/C_out to the glossary; noted that a letter at a gate means that input is wired there; added recipes A, C, D, G and H and the spot-the-type drill.
- **Pass 2:** put the recipes in A → I order; fixed table headers that turned "g" into "G" (text-transform); stated the exact initial and final inputs for every worst case; fixed phone overflow from the glossary table.
- **Pass 3** (readability and spotting): non-inverting functions (NAND + inverter, 2N transistors); the Euler odd-degree existence rule; sizing any gate by the longest-path rule; p ≈ output diffusion/3C; one-unit-system warning (C vs unit-inverter caps); rising contamination delay (R/N); full statements, figures and all five steps for every question; new practice P7 (size a complex gate) and P8 (two-gate path); the kΩ × fF = ps shortcut in the recipes.
- **Pass 4** (Lectures 32–34 update): the start-from-zero primer; the "which p should I use (Elmore vs table)" box; recipe I; four new traps; a too-wide formula replaced with words to fix phone overflow; tables allowed to break across PDF pages.

### Bugs found and fixed

- **MOSFET symbol (caught by the student):** the NMOS source arrow pointed inward and the PMOS had none. Fixed so the NMOS arrow points out and the PMOS arrow points in, keeping the gate bubble. Added a "How to read the symbol" box. Both guides share the symbol code, so both were fixed.
- **Figure overlaps:** VTC labels, the input/output lanes of the definitions figure, Euler node labels, stick-diagram legends, the NAND/NOR titles over V_DD, NOR-n and P7 annotations, the XOR table header, NAND3 ladder labels, and the branch figure's off-path text.
- **Content fixes:** the VTC solver near the rails (clamp outside conduction); the T10 Q4 figure redrawn with three NOR3 inputs and the formula recomputed with g = 7/3, p = 3; the wrong C_out wording in the fanout figure; the Q5 design units sentence; figure numbering re-sequenced.

---

## 7. Final contents

**`lecture25/Lecture25_Guide.pdf` (Lectures 23–26 + Tutorials 8–9):**
- A (10-minute summary) and B1–B9 (capacitance, switching, definitions, average-current and exact methods, rise/fall, a lone MOSFET, design, ring and power)
- B10 (Lecture 26) and the R refresher (L23–24)
- M (master method) and X (exam variants)
- Tutorial 8 (4 questions) and Tutorial 9 (5 questions)
- D (10 practice questions plus the mixed question) and E (sheet and traps)

**`lecture28_31/Lectures28-34_Guide.pdf` (Lectures 28–34 + Tutorial 10, 69 pp.):**
- 00 start from zero; 0 story and glossary
- 1 L28; 2 L29; 3 L30; 4 L31–32 (including NAND3/NOR3 with load); 5 L33 (linear delay model, g table, drive); 6 L34 (limitations, path effort, branching, minimum delay, optional best N)
- 7 recipes A–I with drill; 8 Tutorial 10 (all 9 questions)
- 9 practice P1–P15; 10 Razavi R1–R6; 11 pointer to Tutorials 8/9; 12 sheet and traps

---

## 8. Instructions for extending this guide to new lectures

1. Render each new page at 200 dpi, crop it into strips, and read every strip. Note every figure, formula, definition, worked number and convention.
2. Search the textbook PDF text for the topic. Render and read the matching pages. Record equation and figure numbers.
3. Recompute every lecture number in Python before writing. Simulate anything that has a differential equation.
4. Draw computed SVG figures with the existing helpers, then preview them on one page before inserting.
5. Write sections with the box system and questions with the five-step template. Label everything In lectures, Beyond lectures or Optional.
6. Update the contents, the glossary, the type table, the recipes, the drill, the formula sheet and the traps.
7. Rebuild and run every check in section 6, including two student walkthroughs and the phone overflow test. Then commit and push.
