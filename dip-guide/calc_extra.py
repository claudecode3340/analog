"""Calculator section upgrades: a 'think in matrices' lesson (how to split any question into matrices and why each one
goes where it goes), three new recipes, and key-path corrections from the Casio manual. All numbers checked in numpy."""
from lib import *

E = K('SHIFT', '8', bare=True)  # e
POW = '<span class="k">x<sup>■</sup></span>'

def ex(q, a):
    return f'<details class="s"><summary>{q}</summary><div>{a}</div></details>'

LESSON = '<div class="recipe" id="calc-think" style="border-left-color:var(--accent)"><h4>0 · Think in matrices — how to turn any question into matrix input</h4>' + \
'<p>Almost every DIP number is “multiply pairs, then add them up”: a filter output, a DFT value, a transformed point. A matrix product does exactly that, many times at once, without slips. Your whole job is to <b>line up the pairs</b>. Learn the four ideas below once and you can build the matrices for any variation of a question.</p>' + \
h3('Idea 1 · Row meets column') + \
'<p>In A·B, entry (i, j) of the answer = row i of A paired with column j of B: multiply first with first, second with second, …, and add.</p>' + \
MR(M([[1, 2, 3], [4, 5, 6]], 'A (2×3)', {(1, 0): 'h1', (1, 1): 'h1', (1, 2): 'h1'}), '<span class="op">×</span>', M([[1, 0], [0, 1], [2, 1]], 'B (3×2)', {(0, 0): 'h2', (1, 0): 'h2', (2, 0): 'h2'}), '<span class="op">=</span>', M([[7, 5], [16, 11]], 'A·B (2×2)', {(1, 0): 'h3'})) + \
'<p>Row 2 of A (4, 5, 6) meets column 1 of B (1, 0, 2): 4·1 + 5·0 + 6·2 = <b>16</b>. So to make the calculator compute Σ (weight × value), put the weights along a <b>row</b> of the left matrix and the values down a <b>column</b> of the right matrix (or the other way round), in the same order.</p>' + \
h3('Idea 2 · Check the sizes before you type anything') + \
'<p>(m×<b>n</b>)·(<b>n</b>×p) → m×p. The two inner numbers must be equal; the two outer numbers are the shape of the answer. Write the sizes under each matrix on your rough sheet:</p>' + \
table(['Product', 'Sizes', 'Answer is'], [
    ['row × window × column', '(1×3)(3×3)(3×1)', '1×1 — one filtered pixel'],
    ['T × image × Tᵀ', '(4×4)(4×4)(4×4)', '4×4 — the whole filtered image'],
    ['T<sub>u</sub> × image × T<sub>v</sub>ᵀ, 3×4 image', '(3×3)(3×4)(4×4)', '3×4'],
    ['[cos; sin] × image × [cos sin]', '(2×m)(m×n)(n×2)', '2×2 — the four pieces of one DFT value'],
    ['A × point', '(3×3)(3×1)', '3×1 — the moved point (x′, y′, 1)'],
]) + \
h3('Idea 3 · A matrix on the LEFT mixes rows; on the RIGHT it mixes columns') + \
'<p>Try it with the swap matrix P:</p>' + \
MR(M([[0, 1], [1, 0]], 'P'), '<span class="op">×</span>', M([[1, 2], [3, 4]], 'F'), '<span class="op">=</span>', M([[3, 4], [1, 2]], 'rows swapped'), '<span class="op">&nbsp;&nbsp;but&nbsp;&nbsp;</span>', M([[1, 2], [3, 4]], 'F'), '<span class="op">×</span>', M([[0, 1], [1, 0]], 'P'), '<span class="op">=</span>', M([[2, 1], [4, 3]], 'columns swapped')) + \
'<p>So an operation that combines pixels <b>above and below</b> each other (the x direction, down a column) goes on the <b>left</b>; one that combines pixels <b>left and right</b> (the y direction, along a row) goes on the <b>right</b>, transposed. A separable 2-D filter does both: T<sub>u</sub> · F · T<sub>v</sub>ᵀ.</p>' + \
h3('Idea 4 · How to build T from a 1-D kernel (and what padding does to it)') + \
'<p>Row i of T is the kernel (u₋₁, u₀, u₁) placed so that u₀ sits on the diagonal: T·F then makes row i of the answer = u₋₁·(row i−1) + u₀·(row i) + u₁·(row i+1) — exactly the 1-D filter run down every column. For u = (1, 2, 1) and a 4-row image:</p>' + \
MR(M([[2, 1, 0, 0], [1, 2, 1, 0], [0, 1, 2, 1], [0, 0, 1, 2]], 'zero padding', {(0, 0): 'h2', (3, 3): 'h2'}), M([[3, 1, 0, 0], [1, 2, 1, 0], [0, 1, 2, 1], [0, 0, 1, 3]], 'replicate padding', {(0, 0): 'h1', (3, 3): 'h1'}), M([[2, 2, 0, 0], [1, 2, 1, 0], [0, 1, 2, 1], [0, 0, 2, 2]], 'mirror (reflect, edge not repeated)', {(0, 1): 'h3', (3, 2): 'h3'})) + \
'<p><b>Why the corners change:</b> at the top row the weight u₋₁ falls on the padded row −1. Zero padding: that row is 0, so the weight simply disappears. Replicate: row −1 is a copy of row 0, so its weight is <b>added to row 0’s own weight</b> (2 + 1 = 3 in the corner). Mirror: row −1 is a copy of row 1, so the weight is added to the entry for row 1 (top row becomes 2, 2). Same at the bottom with u₁.</p>' + \
h3('Which pattern fits the question?') + \
table(['The question asks for …', 'Put the data in', 'Put the weights in', 'Type'], [
    ['one filtered pixel, separable kernel u vᵀ (box, 1-2-1, Gaussian, Sobel)', 'MatA = 3×3 window (padded as told)', 'MatB = row uᵀ (1×3), MatC = column v (3×1)', 'MatB×MatA×MatC, then ÷ normaliser'],
    ['one filtered pixel, any 3×3 kernel K', 'MatA = window W', 'MatB = K (rotated 180° for convolution)', 'Trn(MatA)×MatB, add the diagonal'],
    ['whole image ≤ 4×4, separable kernel', 'MatA = F', 'MatB = T<sub>u</sub>, MatC = T<sub>v</sub> (built as above)', 'MatB×MatA×Trn(MatC)'],
    ['whole image ≤ 4×4, Laplacian / any non-separable kernel', 'MatA = F', 'split the kernel into separable pieces (next table)', 'sum of the pieces'],
    ['a coefficient set (affine A, bilinear a,b,c,d, registration c₁…c₈)', 'known inputs as columns of X (or rows of an equation system)', 'known outputs Y', 'Y × X⁻¹, or Equation ▸ Simul Equation'],
    ['several geometric moves', 'the point (x, y, 1) as a column', 'one 3×3 matrix per move', 'last move × … × first move × point'],
    ['one DFT value F(u, v)', 'MatA = f', 'MatB = [cos; sin] rows for u, MatC = [cos sin] columns for v', 'MatB×MatA×MatC → Re = P₁₁ − P₂₂, Im = −(P₁₂ + P₂₁)'],
    ['an image bigger than 4×4', 'see “when the matrix is too big” below', '', ''],
]) + \
h3('Splitting a kernel that is not one row × one column') + \
'<p>A kernel is separable when every row is a multiple of one row (e.g. 1-2-1 / 2-4-2 / 1-2-1). If not, write it as a separable part plus a simple correction — usually only the centre or a cross is left over:</p>' + \
table(['Kernel', 'Split', 'Type'], [
    [r'\(\begin{bmatrix}0&1&0\\1&-4&1\\0&1&0\end{bmatrix}\) (4-neighbour Laplacian)', 'vertical second difference (1, −2, 1) + horizontal second difference', 'D×F + F×D with D = tridiag(1, −2, 1)'],
    [r'\(\begin{bmatrix}1&1&1\\1&-8&1\\1&1&1\end{bmatrix}\) (8-neighbour)', 'all-ones 3×3 (= (1,1,1)ᵀ(1,1,1)) minus 9 × centre', 'J×F×Trn(J) − 9F, J = tridiag(1, 1, 1)'],
    [r'\(\begin{bmatrix}.01&.1&.01\\.1&.56&.1\\.01&.1&.01\end{bmatrix}\) (Oct 2023 Filter-2)', '(0.1, 1, 0.1)ᵀ(0.1, 1, 0.1) has centre 1; the kernel’s centre is 0.56 → subtract 0.44 × centre', 'T×F×T − 0.44F, T = tridiag(0.1, 1, 0.1) → 9.95, 7.06, 1.55 / 7.06, 11.5, 7.06 / … (matches the key except its 6.99 slip)'],
    [r'\(\begin{bmatrix}1&2&1\\2&4&2\\1&2&1\end{bmatrix}\) (weighted mean)', 'already separable: (1,2,1)ᵀ(1,2,1)', 'T×F×T ÷ 16'],
    [r'\(\begin{bmatrix}-1&-2&-1\\0&0&0\\1&2&1\end{bmatrix}\) (Sobel gₓ)', 'difference (−1, 0, 1) down the columns × smoothing (1, 2, 1) along the rows', 'T<sub>d</sub>×F×Trn(T<sub>s</sub>), T<sub>d</sub> = tridiag(−1, 0, 1)'],
]) + \
note('<b>How to find the split yourself:</b> take the corner entry as u₁v₁ and the middle of the top row as u₁v₀, guess u = v from the symmetry, build u vᵀ, and subtract it from the kernel. Whatever is left (often only the centre) is the correction: a multiple of the centre is just “− c·F”.') + \
h3('When the question changes a little') + \
table(['If the question changes …', '… change only this'], [
    ['the kernel numbers', 'the entries of T (or u, v)'],
    ['a factor in front (1/16, 1/9, 1/14)', 'divide once at the end'],
    ['correlation ↔ convolution', 'reverse u and v (row (1, 2, 3) becomes (3, 2, 1)); symmetric kernels: nothing changes'],
    ['the padding', 'only the corner entries of T (Idea 4)'],
    ['the image is m×n, not square', 'two different T’s: T<sub>u</sub> is m×m (left), T<sub>v</sub> is n×n (right)'],
    ['only some outputs are asked (the diagonal, one row)', 'compute the full product anyway (≤ 4×4) and read them off — or use the window method for those pixels only'],
    ['5 taps instead of 3 (5×5 kernel)', 'T gets two more diagonals (u₋₂ … u₂)'],
    ['the image is bigger than 4×4', 'next box'],
]) + \
'<div class="warn"><b>When the matrix is too big (more than 4×4).</b> (1) Only the non-zero block matters? Use just that block with its true indices (Oct 2023: the 3×3 block inside a 5×5 of zeros, zero padding comes for free). (2) A box filter on a 5×5 (or up to 45×5) image: Spreadsheet recipe J below — one Sum( per output pixel. (3) Anything else: pixel by pixel with the 3×3 window (MatB×MatA×MatC), changing only MatA each time — use the calculation history (▲) to re-run the same product.</div>' + \
h3('Check yourself (open after trying)') + \
ex('1. Build T for the box kernel ⅓(1, 1, 1) on a 3-row image with replicate padding.', 'Ignore ⅓ (divide at the end): rows (2, 1, 0), (1, 1, 1), (0, 1, 2) — the corners get the extra 1 because row −1 copies row 0 and row 3 copies row 2.') + \
ex('2. B is 2×3, A is 3×4, C is 4×2. What is the size of B·A·C, and could you type A·B?', '2×2. A·B is (3×4)(2×3): the inner numbers 4 and 2 differ → Dimension ERROR.') + \
ex('3. For Sobel gᵧ = [−1 0 1; −2 0 2; −1 0 1] on a 4×4 image, which T goes left and which goes right?', 'Its rows are all multiples of (−1, 0, 1) and its columns of (1, 2, 1): smoothing (1, 2, 1) acts down the columns → T<sub>s</sub> on the left; the difference (−1, 0, 1) acts along the rows → T<sub>d</sub> on the right: T<sub>s</sub>×F×Trn(T<sub>d</sub>).') + \
ex('4. The kernel is ¼[0 1 0; 1 0 1; 0 1 0] (average of the 4 neighbours, excluding the pixel). How do you type it for a 4×4 image?', 'It is the Laplacian plus 4 × centre, all ÷ 4: (D×F + F×D + 4F) ÷ 4. Equivalently (N×F + F×N) ÷ 4 with N = tridiag(1, 0, 1).') + \
'</div>'

RECIPES = '<div class="recipe" id="calc-I"><h4>I · RMS error and SNR of quantised data — Statistics app</h4><div class="grid2"><div><b>What it does.</b> Σe² and Σf̂² without writing eight squares.</div><div><b>Why it works.</b> e<sub>rms</sub> = √(Σe²/N) and SNR<sub>rms</sub> = √(Σf̂²/Σe²): both need only sums of squares, which the Statistics app keeps (Σx²).</div></div><h5 class="wk">Worked on <a href="#s18q6">Mid-sem 2018-19 Q6</a></h5><div class="tw"><table class="t csteps"><tr><th>#</th><th class="l">Press</th><th class="l">What you enter — and what it means</th><th class="l">Screen</th></tr>' + \
f'<tr><td>1</td><td class="l">{K("HOME", ">Statistics", ">1-Variable")}</td><td class="l">x = the errors −15, −6, −1, −6, −2, −2, −2, −5 (negative sign: {K("SHIFT", "−")}).</td><td class="l"></td></tr>' + \
f'<tr><td>2</td><td class="l">{K("OK", ">1-Var Results", ">OK")}</td><td class="l">Scroll to Σx² and n.</td><td class="l">' + lcd('1-Var Results', 'Σx² = 335<br>n = 8') + '</td></tr>' + \
f'<tr><td>3</td><td class="l">main screen</td><td class="l">{K("√(", "335", "÷", "8", ")", "EXE")}</td><td class="l">' + lcd('', '6.471089553') + '</td></tr>' + \
'<tr><td>4</td><td class="l">editor again</td><td class="l">Replace the x column by the quantised values 240, 112, … (Σx² = 157440), then √(157440 ÷ 335).</td><td class="l">' + lcd('', '21.67879492') + '</td></tr></table></div><div class="anyq"><b>Do it on any question</b><ul><li>The errors of a “keep the top bits” quantiser are just −(f mod 2<sup>dropped bits</sup>).</li><li>dB if asked: 20·log₁₀(SNR<sub>rms</sub>) (log is [SHIFT][x²]).</li></ul></div></div>' + \
'<div class="recipe" id="calc-J"><h4>J · A whole 5×5 box filter at once — Spreadsheet app</h4><div class="grid2"><div><b>What it does.</b> every output of a 3×3 box (average) filter on an image up to 5 columns wide (the Matrix app stops at 4×4).</div><div><b>Why it works.</b> a box output is the plain sum of the 3×3 window ÷ 9. Sum(A1:C3) adds a 3×3 block, and Fill Formula shifts it to every position. With zero padding the window simply gets smaller at the borders, so the edges use smaller blocks. One formula per cell keeps you inside the spreadsheet’s ≈ 1,700-byte memory (two separate passes would not fit).</div></div><h5 class="wk">Worked on <a href="#s18q2">Mid-sem 2018-19 Q2</a> (5×5, zero padding)</h5><div class="tw"><table class="t csteps"><tr><th>#</th><th class="l">Press</th><th class="l">What you enter — and what it means</th><th class="l">Screen</th></tr>' + \
f'<tr><td>1</td><td class="l">{K("HOME", ">Spreadsheet")}</td><td class="l">Type the image into A1:E5 (each value + EXE). Rows 1–5 = image rows 0–4.</td><td class="l"></td></tr>' + \
f'<tr><td>2</td><td class="l">{K("TOOLS", ">Fill Formula")}</td><td class="l">Interior: Form <code>Sum(A1:C3)÷9</code>, Range <code>B8:D10</code>. (= is not needed in the Form line; Sum( and the colon are in {K("CATALOG", ">Spreadsheet")}; letters: {K("SHIFT", "4")} = A, {K("SHIFT", "5")} = B, {K("SHIFT", "6")} = C, {K("SHIFT", "1")} = D, {K("SHIFT", "2")} = E.)</td><td class="l"></td></tr>' + \
'<tr><td>3</td><td class="l">Fill Formula ×8 more</td><td class="l">Top edge B7:D7 <code>Sum(A1:C2)÷9</code> · bottom B11:D11 <code>Sum(A4:C5)÷9</code> · left A8:A10 <code>Sum(A1:B3)÷9</code> · right E8:E10 <code>Sum(D1:E3)÷9</code> · corners A7 <code>Sum(A1:B2)÷9</code>, E7 <code>Sum(D1:E2)÷9</code>, A11 <code>Sum(A4:B5)÷9</code>, E11 <code>Sum(D4:E5)÷9</code>.</td><td class="l">' + \
lcdmat('A7:E11 (× 9 shown)', [[16, 28, 26, 16, 4], [27, 41, 40, 27, 13], [20, 34, 33, 28, 14], [26, 39, 35, 28, 15], [15, 26, 21, 17, 6]]) + '</td></tr>' + \
'<tr><td>4</td><td class="l">read rows 7–11</td><td class="l">Outputs ÷ 9: 1.778, 3.111, 2.889, 1.778, 0.444 / 3, 4.556, … — round as the question says.</td><td class="l"></td></tr></table></div><div class="anyq"><b>Do it on any question</b><ul><li>Replicate padding: the border windows count the edge pixels twice — easiest by hand for the 16 border pixels, Spreadsheet for the 9 interior ones.</li><li>The relative references shift with the cell (Form typed for the top-left cell of the range), exactly like dragging a formula in Excel.</li><li><b>Turning the calculator off erases the spreadsheet</b> — finish and copy the numbers first.</li></ul></div></div>' + \
'<div class="recipe" id="calc-K"><h4>K · A non-separable kernel on a whole small image — split it (Matrix app)</h4><div class="grid2"><div><b>What it does.</b> the whole output of a kernel that is not one row × one column (Laplacians, Filter-2 of Oct 2023).</div><div><b>Why it works.</b> filtering is linear: filter(k₁ + k₂) = filter(k₁) + filter(k₂). Split the kernel into separable pieces plus a centre correction (Idea 4 table), compute each piece with T×F×Tᵀ, add.</div></div><h5 class="wk">Worked on <a href="#o23q2">Mid-sem Oct 2023 Q2, Filter-2</a></h5><div class="tw"><table class="t csteps"><tr><th>#</th><th class="l">Press</th><th class="l">What you enter — and what it means</th><th class="l">Screen</th></tr>' + \
f'<tr><td>1</td><td class="l">{K("TOOLS", ">MatA", ">Define New")} 3×3</td><td class="l">MatA = the non-zero block F:' + MR(M([[15, 7, 0], [7, 15, 7], [0, 7, 15]])) + '</td><td class="l"></td></tr>' + \
f'<tr><td>2</td><td class="l">{K("TOOLS", ">MatB", ">Define New")} 3×3</td><td class="l">MatB = T for u = (0.1, 1, 0.1), zero padding:' + MR(M([[1, 0.1, 0], [0.1, 1, 0.1], [0, 0.1, 1]])) + '</td><td class="l"></td></tr>' + \
f'<tr><td>3</td><td class="l">{K("MatB", "×", "MatA", "×", "MatB", "−", "0.44", "×", "MatA", "EXE")}</td><td class="l">T is symmetric, so Trn is not needed. −0.44F fixes the centre weight (1 → 0.56).</td><td class="l">' + lcdmat('MatAns', [[9.95, 7.06, 1.55], [7.06, 11.5, 7.06], [1.55, 7.06, 9.95]]) + '</td></tr></table></div><div class="anyq"><b>Do it on any question</b><ul><li>Laplacian (4-nbr): MatB = D = tridiag(1, −2, 1): MatB×MatA + MatA×MatB. Sharpened image: then MatA − MatAns.</li><li>Laplacian (8-nbr): MatB = J = tridiag(1, 1, 1): MatB×MatA×MatB − 9×MatA.</li><li>Replicate padding: change the corner entries of D or J exactly as in Idea 4 (D’s corner −2 becomes −1; J’s corner 1 becomes 2).</li></ul></div></div>'

PATCHES = [
    ('<div class="recipe" id="calc-A">', LESSON + '<div class="recipe" id="calc-A">'),
    ('<div class="warn">These recipes were checked', RECIPES + '<div class="warn">These recipes were checked'),
    ('<li>Round only the final answer (your instructor reports 4 decimals).</li></ul></div>',
     '<li>Round only the final answer (your instructor reports 4 decimals). To see 4 decimals everywhere: ' + K('SETTINGS', '>Calc Settings', '>Number Format', '>Fix', '>4') + '; back to normal with Norm 1.</li>'
     '<li>Keys that are easy to miss: negative sign (−) = ' + K('SHIFT', '−') + ' · comma = ' + K('SHIFT', ')') + ' · = (in Solver/Spreadsheet) = ' + K('SHIFT', '(') + ' · e = ' + K('SHIFT', '8') + ' then ' + POW + ' for e<sup>x</sup> · log₁₀ = ' + K('SHIFT', 'x²') + ' · ln = ' + K('SHIFT', 'log■□') + ' · x⁻¹ = ' + K('SHIFT', 'x<sup>■</sup>') + ' · decimal result ≈ = ' + K('SHIFT', 'EXE') + '.</li>'
     '<li>Re-use: ▲ on the main screen scrolls back through earlier calculations; edit one number and press EXE again (perfect for “same formula, next pixel”).</li></ul></div>'),
    ('<span class="k m">Define New</span></span> → choose rows, columns → type each cell + EXE (expressions like √3÷2, cos(120), π are fine).</li>',
     '<span class="k m">Define New</span></span> → choose rows, columns → <span class="k m">Confirm</span> → type each cell + EXE (expressions like √3÷2, cos(120), π are fine). <i>Define New</i> only appears if that matrix already holds something; a new one goes straight to the size screen.</li>'),
    ('<td class="l"><span class="keys"><span class="k">HOME</span><span class="arrow">→</span><span class="k m">Table</span></span> → Define f(x)</td>',
     '<td class="l"><span class="keys"><span class="k">HOME</span><span class="arrow">→</span><span class="k m">Table</span></span>, then ' + K('TOOLS', '>Define f(x)/g(x)', '>Define f(x)') + '</td>'),
    ('<td class="l">type <code>1 + 2×1∠−90 + 3×1∠−180 + 4×1∠−270</code>', '<td class="l">type <code>1 + 2×1∠−90 + 3×1∠−180 + 4×1∠−270</code> (∠ is ' + K('CATALOG', '>Complex', '>∠') + ')'),
]
INSERTS = []
