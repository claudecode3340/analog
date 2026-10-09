"""Text improvements: a plain-language symbol decoder, notes on ambiguous questions, updated paper index and key errors."""
from lib import *

SYMBOLS = '''<section class="topic" id="symbols">
  <div class="eyebrow">Before the formulas</div>
  <h2>How to read the maths in this course (plain words)</h2>
  <div class="meta"><span class="chip hot">read once, refer back</span></div>
  <p class="lede">Every formula in DIP is built from about twenty symbols. Here is each one in words, with a tiny example you can check in your head. When a formula looks scary, read it aloud using this table.</p>
''' + table(['Symbol', 'Say it as', 'Tiny example'], [
    [r'\(f(x,y)\)', 'the brightness of the pixel in row x, column y (rows go down, columns go right, both start at 0)', 'f(0,0) = top-left pixel; f(2,1) = third row, second column'],
    [r'\(M_f(i,j)\)', 'the same image written as a matrix, but counted from 1 (your instructor’s convention)', r'\(M_f(2,2)=f(1,1)\)'],
    [r'\(r_k,\ n_k,\ p_r(r_k)\)', 'subscript k = “number k in the list”: the k-th grey level, how many pixels have it, and that count ÷ total pixels', 'n₃ = 360 → 360 pixels have level 3'],
    [r'\(L,\ L-1\)', 'L = how many grey levels there are; L − 1 = the brightest level', '3-bit: L = 8, levels 0…7'],
    [r'\(\sum_{j=0}^{k}a_j\)', '“add up a<sub>j</sub> for j = 0, 1, …, k” — a running total', r'\(\sum_{j=0}^{2}j=0+1+2=3\)'],
    [r'\(\sum_{s=-1}^{1}\sum_{t=-1}^{1}\)', 'two running totals inside each other = add over all 9 positions of a 3×3 window', 'the centre is s = t = 0'],
    [r'\(|x|\)', 'size of x, ignoring its sign', '|−3| = 3; for a complex number |a + bi| = √(a² + b²)'],
    [r'\(\max(a,b),\ \min(a,b)\)', 'the larger / smaller of the two', 'max(3, 6) = 6'],
    [r'\(\lfloor x\rfloor\), round(x)', 'floor = drop the decimals (go down); round = nearest whole number (.5 goes up)', '⌊3.7⌋ = 3, round(3.5) = 4'],
    [r'\(\in,\ \notin\)', '“is one of”, “is not one of”', r'\(r\in\{0,\dots,7\}\)'],
    [r'\(A\cup B,\ A\cap B,\ A^c\)', 'union (either/max), intersection (both/min), complement (everything not in A / L−1−z)', 'grey images: union = pixelwise max'],
    [r'\(\mapsto\), \(\to\)', '“is sent to” — what a transformation does to one value', r'\(r\mapsto L-1-r\) is the negative'],
    [r'\(T(r),\ s=T(r)\)', 'a rule that turns an input grey level r into an output level s', 'T(r) = 7 − r'],
    [r'\(w\star f,\ w*f\)', 'correlation (slide w as printed), convolution (rotate w by 180° first)', 'they are equal for symmetric kernels'],
    [r'\(f\circledast h\)', 'circular convolution: indices wrap around (mod n)', 'index −1 means n − 1'],
    [r'\(A\odot B\)', 'multiply matching entries (not the matrix product)', r'\(\begin{bmatrix}1&2\end{bmatrix}\odot\begin{bmatrix}3&4\end{bmatrix}=\begin{bmatrix}3&8\end{bmatrix}\)'],
    [r'\(A^T\), \(A^{-1}\)', 'transpose (rows become columns); inverse (the matrix that undoes A)', r'\(\begin{bmatrix}1&2\end{bmatrix}^T\) is a column'],
    [r'\(\nabla^2 f\)', '“del squared f”, the Laplacian: how much a pixel differs from its neighbours (sum of neighbours − 4 × pixel)', 'flat area → 0'],
    [r'\(\nabla f\), \(\partial f/\partial x\)', 'gradient: the slope of brightness; ∂/∂x = slope going down the rows', 'f(x+1, y) − f(x, y)'],
    [r'\(\sigma,\ \sigma^2,\ m,\ \bar z\)', 'standard deviation (spread), variance (spread²), mean (average)', 'mean of 2, 4 = 3; σ = 1'],
    [r'\(e^{-j2\pi ux/M}\), \(W_n\)', 'a unit arrow turned by −360°·ux/M (Euler: cos θ − j sin θ); W<sub>n</sub> = e<sup>−j2π/n</sup>', r'\(W_4=-j\)'],
    [r'\(F(u,v)\), \(|F|\), \(\phi\)', 'the DFT value at frequency (u, v), its size, its angle', 'F(0,0) = sum of all pixels (slides’ DFT)'],
    [r'\(\propto,\ \approx\)', 'grows in proportion to; is roughly', ''],
    [r'\(\forall,\ \Rightarrow,\ \iff\)', 'for every; therefore/implies; if and only if', ''],
]) + note('<b>Reading strategy.</b> (1) Find what is being computed (left of “=”). (2) Find what changes in the sum (the letter under Σ). (3) Write the first two terms out in full with numbers. After two terms the pattern is obvious and the symbols stop being scary.') + '\n</section>\n'

PATCHES = [
    ('<section class="topic" id="plan">', SYMBOLS + '<section class="topic" id="plan">'),
    ('<a href="#rules" data-sec="rules">Conventions</a>', '<a href="#rules" data-sec="rules">Conventions</a><a href="#symbols" data-sec="symbols">Read the maths</a>'),
    # the blur-histogram question has two readings; the 2021 key used "border pixels unchanged"
    ('right {0: 1568, 85: 336, 113.33: 18, 141.67: 18, 170: 336, 255: 1568}.',
     'right {0: 1568, 85: 336, 113.33: 18, 141.67: 18, 170: 336, 255: 1568}. <i>Other reading</i> (border pixels kept unfiltered, 64×64): left {0: 1986, 85: 62, 170: 62, 255: 1986}; right {0: 1694, 85: 336, 113.33: 18, 141.67: 18, 170: 336, 255: 1694}. For the 16×16 Quiz-2 2021 version the key used this reading: {0: 114, 85: 14, 170: 14, 255: 114} and {0: 62, 85: 48, 113: 18, 142: 18, 170: 48, 255: 62}. State which reading you use.'),
    # paper index: newly solved items
    ('<td>Q3 rms error/SNR (fidelity criteria, Ch. 8), Q4 arithmetic coding, Q5 MATLAB</td>', '<td>Q4 arithmetic coding, Q5 MATLAB (also: Q3 rms error/SNR is solved anyway: <a href="#m23q3">Q3</a>)</td>'),
    ('<td>Q3 run-length + Huffman, Q6 MATLAB</td>', '<td>Q3 run-length + Huffman, Q6 MATLAB code (its transformation is solved: <a href="#s19q6">Q6</a>)</td>'),
    ('Q4 motion-blur degradation (Ch. 5), Q5 Huffman, Q6 rms SNR</td>', 'Q4 motion-blur degradation (Ch. 5), Q5 Huffman (Q6 rms SNR is solved anyway: <a href="#s18q6">Q6</a>)</td>'),
    ('<td>Q1 MATLAB, Q3(a)(ii)–(b) Huffman/RLE, Q5 Hotelling/Euler, Q6 Fourier descriptors, Q7 morphology</td>', '<td>Q1 MATLAB, Q3(a)(ii) Huffman, the RLE step of Q3(b) (its MSB plane is solved: <a href="#e23q3b">Q3(b)</a>), Q5 Hotelling/Euler, Q6 Fourier descriptors, Q7 morphology</td>'),
    ('<a href="#d25q4">Q4(b) (matrix-form part)</a></td><td>Q1 morphology, Q4(a) basis images (Ch. 7), Q5 LZW, Q6 segmentation</td>', '<a href="#d25q4a">Q4(a)</a> · <a href="#d25q4">Q4(b)</a> · <a href="#d25q6">Q6 (thresholding)</a></td><td>Q1 morphology, Q5 LZW</td>'),
    ('<td><a href="#tb3-4">3.4</a> · <a href="#tb3-10">3.10</a> · <a href="#tb3-18">3.18</a> · <a href="#tb3-20">3.20</a> · <a href="#tb3-22">3.22</a> · <a href="#tb3-44">3.44</a> (3.24 is the separable-kernel remark in <a href="#ch3-filt">3.4</a>) · also <a href="#s19q1">2.18</a>, <a href="#tb2-9">2.9</a>, <a href="#tb3-41">3.41</a>, <a href="#d25q2c">3.16</a>, <a href="#o24q2ii">4.47</a></td>',
     '<td><b>Ch 2 homework:</b> <a href="#tb2-2">2.2</a> · <a href="#tb2-4">2.4</a> · <a href="#tb2-19">2.19</a> · <a href="#tb2-23">2.23</a> · <a href="#tb2-26">2.26</a> · <a href="#tb2-36">2.36</a> · <a href="#tb2-37">2.37</a><br><b>Ch 3 homework:</b> <a href="#tb3-4">3.4</a> · <a href="#tb3-10">3.10</a> · <a href="#tb3-18">3.18</a> · <a href="#tb3-20">3.20</a> · <a href="#tb3-22">3.22</a> · <a href="#tb3-24">3.24</a> · <a href="#tb3-44">3.44</a><br><b>Ch 4 homework:</b> <a href="#tb4-7">4.7</a> · <a href="#tb4-10">4.10</a> · <a href="#tb4-21">4.21</a> · <a href="#tb4-36">4.36</a> · <a href="#tb4-44">4.44</a> · <a href="#o24q2ii">4.47</a> · <a href="#tb4-48">4.48</a><br><b>Other textbook problems:</b> <a href="#tb2-3">2.3</a>, <a href="#tb2-6">2.6</a>, <a href="#tb2-8">2.8</a>, <a href="#tb2-9">2.9</a>, <a href="#tb2-10">2.10</a>, <a href="#tb2-12">2.12</a>, <a href="#s19q1">2.18</a>, <a href="#tb2-20">2.20</a>, <a href="#tb2-24">2.24</a>, <a href="#tb2-25">2.25</a>, <a href="#tb2-29">2.29</a>, <a href="#tb3-1">3.1</a>, <a href="#tb3-3">3.3</a>, <a href="#tb3-5">3.5</a>, <a href="#tb3-6">3.6</a>, <a href="#tb3-7">3.7</a>, <a href="#tb3-11">3.11</a>, <a href="#tb3-12">3.12</a>, <a href="#d25q2c">3.16</a>, <a href="#tb3-27">3.27</a>, <a href="#tb3-28">3.28</a>, <a href="#tb3-29">3.29</a>, <a href="#tb3-31">3.31</a>, <a href="#tb3-35">3.35</a>, <a href="#tb3-38">3.38</a>, <a href="#tb3-40">3.40</a>, <a href="#tb3-41">3.41</a>, <a href="#tb3-42">3.42</a>, <a href="#tb4-29">4.29</a>, <a href="#tb4-30">4.30</a>, <a href="#tb4-43">4.43–45</a>, <a href="#tb4-50">4.50–51</a></td>'),
    ('<tr><td>Dec 2025 Q3</td>', '<tr><td>Dec 2025 Q4(a)</td><td>Rounds the coefficients 6.5, 1.5, 3.5, 0.5 to 7, 2, 4, 1 and the reconstruction to [[6, 6],[2, 2]].</td><td>Exact: t = 6.5, 1.5, 3.5, 0.5; f̂ = [[5, 5],[1.5, 1.5]].</td><td><a href="#d25q4a">→</a></td></tr>\n<tr><td>Dec 2025 Q3 (also)</td><td>One pixel of the printed g (row 5, column 1) is 1, but its input 7 maps to 4 everywhere else.</td><td>4 (a typo in the key matrix).</td><td><a href="#d25q3">→</a></td></tr>\n<tr><td>Dec 2025 Q3</td>'),
]

INSERTS = [] and [
    ('<div class="note"><b>Expect</b>', ''),  # marker check only
]

# MATLAB: not in this instructor's papers; say so where students look
PATCHES.append(('<div class="note"><b>Expect</b>', '<div class="warn"><b>MATLAB-code questions</b> appeared only in the older instructor’s papers (2018–2023). Your instructor’s Quiz-1 and his 2025 compre have none, so this guide skips them and spends that time on computation.</div><div class="note"><b>Expect</b>'))
