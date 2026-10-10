"""Chapter 3.4 rebuilt: how spatial filtering works — the sliding window, correlation vs convolution, padding, separable
kernels — with window/kernel/product pictures; the filtering past papers as step-by-step walks."""
from ch3lib import *

I44 = [[1, 2, 4, 5], [5, 2, 5, 2], [1, 1, 3, 6], [2, 4, 6, 7]]
W121 = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]


def rounded3(g):
    return [[int(min(7, max(0, np.floor(v + 0.5)))) for v in r] for r in g]


# ── calculator helpers (every screen below is computed here with numpy) ──
def _q(A, d=4):
    return [[round(float(v), d) for v in r] for r in np.atleast_2d(np.asarray(A, float))]


def mdef(name, A, means):
    """one 'TOOLS → MatX → OK → Define New' line with the matrix screen"""
    A = np.atleast_2d(np.asarray(A, float))
    return cl(K('TOOLS', '>' + name, 'OK', '>Define New'), means, lcdmat(f'{name} = {A.shape[0]}×{A.shape[1]}', _q(A)))


def band(k, n, rep=False):
    """T: the 1-D kernel (a, b, c) on the diagonal band; replicate padding adds the outside weight to the corners"""
    a, b, c = k; T = np.zeros((n, n))
    for i in range(n):
        T[i, i] = b
        if i: T[i, i - 1] = a
        if i < n - 1: T[i, i + 1] = c
    if rep: T[0, 0] += a; T[-1, -1] += c
    return T


def Rrow(row, n):
    """for kernel row (a b c): R = [[b, a, 0], [c, b, a], [0, c, b]] (band extended for n columns)"""
    a, b, c = row; R = np.zeros((n, n))
    for j in range(n):
        R[j, j] = b
        if j: R[j - 1, j] = a
        if j < n - 1: R[j + 1, j] = c
    return R


TRN = cl(K('CATALOG', '>Matrix', '>Matrix Calc', '>Transposition (Trn)'), 'this is how you type Trn( — then MatA, close the bracket')
MAT_APP = cl(K('HOME', '>Matrix', 'OK'), 'opens the Matrix app (matrices up to 4×4)')


def trace_lines(win, ker, kname='MatB', div=None, rnd=None):
    """one pixel, any kernel: Trn(MatA) × kernel, add the diagonal"""
    P = np.asarray(win, float).T @ np.asarray(ker, float); t = float(np.trace(P))
    s = cl(K('Trn(MatA)', '×', kname, 'EXE'), f'multiplies the window by the kernel; the <b>diagonal</b> of the answer holds the three row-sums of window×kernel, the other entries are junk',
           lcdmat('MatAns', _q(P)))
    s += cl(K(*' + '.join(fmt(float(P[i, i])) for i in range(3)).split(' '), 'EXE'), f'add the diagonal = sum of the nine products = <b>{fmt(t)}</b>')
    if div: s += cl(K('Ans', '÷', str(div), 'EXE'), f'{fmt(t)} ÷ {div} = {fmt(round(t / div, 4))}' + (f' → round → <b>{rnd}</b>' if rnd is not None else ''))
    return s, t


def sep_lines(u, win, v, div=None):
    """one pixel, separable kernel u·vᵀ: row u × window × column v"""
    S = float(np.asarray(u, float) @ np.asarray(win, float) @ np.asarray(v, float))
    s = mdef('MatB', [u], 'u as a 1×3 row: the weights for the three window rows') + mdef('MatA', win, 'the 3×3 window around the pixel') + mdef('MatC', [[x] for x in v], 'v as a 3×1 column: the weights inside each row')
    s += cl(K('MatB', '×', 'MatA', '×', 'MatC', 'EXE'), 'MatA×MatC weights each row and adds it; MatB× weights those three row results and adds them = the sum of all nine products', lcdmat('MatAns', [[round(S, 4)]]))
    if div: s += cl(K('Ans', '÷', str(div), 'EXE'), f'{fmt(S)} ÷ {div} = <b>{fmt(round(S / div, 4))}</b>')
    return s, S


def shifted(F, rep=False):
    F = np.asarray(F, float); m = F.shape[1]
    top = F[:1] if rep else np.zeros((1, m)); bot = F[-1:] if rep else np.zeros((1, m))
    return np.vstack([top, F[:-1]]), np.vstack([F[1:], bot])


def m4_lines(F, w, div=None, name='G'):
    """whole image ≤ 4×4, any 3×3 kernel (correlation, zero padding): G = (F down)R₀ + F R₁ + (F up)R₂"""
    F = np.asarray(F, float); w = np.asarray(w, float); n = F.shape[1]
    dn, up = shifted(F); R0, R1, R2 = (Rrow(w[k], n) for k in range(3))
    L1 = dn @ R0 + F @ R1; G = L1 + up @ R2
    s = mdef('MatA', dn, 'F shifted <b>down</b> one row (top row = 0): row i holds the row above pixel i — what kernel row 0 sees')
    s += mdef('MatB', R0, f'R₀ from kernel row 0 ({" ".join(fmt(float(x)) for x in w[0])}): multiplying by it slides that row along each image row')
    s += mdef('MatC', F, 'F itself — what kernel row 1 (the middle row) sees')
    s += mdef('MatD', R1, f'R₁ from kernel row 1 ({" ".join(fmt(float(x)) for x in w[1])})')
    s += cl(K('MatA', '×', 'MatB', '+', 'MatC', '×', 'MatD', 'EXE'), 'contribution of kernel rows 0 and 1 for every pixel at once', lcdmat('MatAns', _q(L1)))
    s += mdef('MatA', up, 'redefine: F shifted <b>up</b> one row (bottom row = 0) — what kernel row 2 sees. Redefining does not change MatAns')
    s += mdef('MatB', Rrow(w[2], n), f'R₂ from kernel row 2 ({" ".join(fmt(float(x)) for x in w[2])})')
    s += cl(K('MatAns', '+', 'MatA', '×', 'MatB', 'EXE'), f'adds kernel row 2 → the whole filtered image {name}' + (f' (still × {div})' if div else ''), lcdmat('MatAns', _q(G)))
    if div: s += cl(K('MatAns', '÷', str(div), 'EXE'), 'divide every entry by the kernel factor, then round', lcdmat('MatAns', _q(G / div)))
    return s, G


def section(card):
    H = ['''<section class="topic" id="ch3-filt">
  <div class="eyebrow">Chapter 3.4 · Lectures 9–10</div>
  <h2>Spatial filtering: the sliding window</h2>
  <div class="meta"><span class="chip ">TB 3.4</span><span class="chip ">slides pp. 22–30</span><span class="chip hot">every paper</span></div>
  <p class="lede">A spatial filter computes every output pixel from a small <b>window</b> of input pixels around it, using a small grid of weights called the <b>kernel</b>. Smoothing, sharpening and edge detection are all this one operation with different kernels — so once you can do one output pixel by hand, you can do every filtering question. This section is the mechanics: the sliding window, correlation vs convolution, what to do at the border (padding), and separable kernels.</p>''']

    fig, tot = window_fig(I44, 1, 1, W121, 'zero', label_kernel='kernel (1 2 1 / 2 4 2 / 1 2 1)')
    H.append(lesson('One output pixel = multiply the window by the kernel, entry by entry, and add',
        'Put the kernel’s centre on the pixel you want. The 3×3 block of image pixels under the kernel is the <b>window</b>. Multiply each window value by the kernel weight on top of it, add the nine products, and multiply by the factor in front of the kernel (if any). That number is the output at that pixel. Then slide to the next pixel and repeat.',
        '<p><b>Example</b> (Mid-sem 2023-24 image, kernel ¹⁄₁₆[1 2 1; 2 4 2; 1 2 1], output at pixel (1, 1)):</p>' + fig +
        f'<p>Sum of the products = {fmt(tot)}; times ¹⁄₁₆ → <b>{fmt(tot / 16)}</b>. Every output pixel is computed the same way, always from the <b>original</b> image (never from outputs already computed).</p>'
        '<div class="cols"><div><p><b>Words from the slides:</b> the kernel is also called a <b>mask</b> or <b>window</b>, and it is the filter’s <b>impulse response</b> (what the filter outputs for an image that is a single 1). A filter is <b>linear</b> if the output is a weighted sum like this; the median filter (Section 3.5) is <b>nonlinear</b>.</p></div>'
        '<div><p><b>Calculator for one pixel (separable kernel w = u·vᵀ):</b> MatB = u written as a <b>1×3 row</b>, MatA = the 3×3 window, MatC = v as a <b>3×1 column</b>. Then MatB × MatA × MatC gives a 1×1 answer = the sum of the nine products (before the ¹⁄₁₆). Why: MatA × MatC weights each window row by v and adds it (a column of 3 row sums); MatB × that weights those 3 sums by u and adds them.</p>'
        '<p><b>Here:</b> u = v = (1, 2, 1). Window × [1; 2; 1] = [1+4+4; 5+4+5; 1+2+3] = [9; 14; 6]; then [1 2 1] × [9; 14; 6] = 9 + 28 + 6 = <b>43</b> ✓ → × ¹⁄₁₆ = 2.6875. Not separable? Use Trn(MatA) × MatB and add the diagonal, or type the nine products.</p></div></div>',
        use='every filtering question: weighted mean, box, Gaussian, Laplacian, Sobel — only the kernel changes.', tag='1'))

    L = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    H.append(lesson('Correlation vs convolution: is the kernel turned round?',
        '<b>Correlation</b> (☆) uses the kernel exactly as printed. <b>Convolution</b> (∗) first turns the kernel round by 180° (flip it left↔right and top↔bottom), then does exactly the same sliding sum. For kernels that look the same after the half-turn (symmetric ones, like 1-2-1 or the Laplacian), both give the same answer.',
        '<div class="cols"><div>'
        '<div class="formula">\\((w\\star f)(x,y)=\\sum_{s,t}w(s,t)\\,f(x+s,\\,y+t)\\)<span class="say">correlation: weight w(s, t) multiplies the pixel s rows down and t columns right.</span></div>'
        '<div class="formula">\\((w*f)(x,y)=\\sum_{s,t}w(s,t)\\,f(x-s,\\,y-t)\\)<span class="say">convolution: the minus signs are the half-turn of the kernel.</span></div>'
        '<p><b>Why convolution exists:</b> convolving with a single 1 (an impulse) copies the kernel exactly; correlation copies it upside down (Section 3.4 slide example). Convolution also has nicer algebra: f ∗ g = g ∗ f, (f ∗ g) ∗ h = f ∗ (g ∗ h), and f ∗ (g + h) = f ∗ g + f ∗ h. Correlation only has the last one.</p>'
        '<p><b>Test to tell which one a chip does</b> (Compre 2025): feed it an image with a single 1 and a lopsided kernel; convolution returns the kernel itself, correlation returns it rotated.</p>'
        '</div><div>' + figs(gsvg(L, {(i, j): 'n4' for i in range(3) for j in range(3)}, cell=44, idx=False, label='a lopsided kernel w (used as is for correlation)'), gsvg(np.rot90(np.array(L), 2).tolist(), {(i, j): 'nd' for i in range(3) for j in range(3)}, cell=44, idx=False, label='w turned 180° (used for convolution)')) + '</div></div>',
        use='Mid-sem Oct 2024 Q1 (“perform correlation and convolution and compare”), Compre 2025 Q2(c), textbook 3.16–3.18.', tag='2'))

    f2 = [[1, 2], [3, 4]]
    zp = np.pad(f2, 1).tolist(); rp = np.pad(f2, 1, 'edge').tolist(); mp = np.pad(f2, 1, 'symmetric').tolist()
    border = lambda n: {(i, j): 'block' for i in range(n) for j in range(n) if i in (0, n - 1) or j in (0, n - 1)}
    H.append(lesson('Padding: what is outside the image?',
        'At the border, part of the window hangs outside the image. The question must tell you what to pretend is there. The three choices on your slides:',
        '<div class="cols"><div><ul>'
        '<li><b>Zero padding</b>: outside = 0. Border outputs come out darker (some weights multiply zeros).</li>'
        '<li><b>Replicate padding</b>: outside = a copy of the nearest edge pixel. Older papers call this “reflecting (repeating) the border pixels”.</li>'
        '<li><b>Symmetric (mirror) padding</b>: reflect the image at its edge (for a 3×3 kernel this is the same as replicate).</li></ul>'
        '<p>Other choices: leave the border pixels unfiltered, crop the output to where the window fits, or treat the image as periodic (circular).</p>'
        '<p><b>Output size:</b> “filtering” keeps the m×n size (pad by 1 for a 3×3 kernel). The <b>extended</b> (“full”) result lets every kernel entry meet every pixel: size (m + p − 1) × (n + q − 1).</p></div>'
        '<div>' + figs(gsvg(zp, border(4), cell=40, idx=False, label='zero padding'), gsvg(rp, border(4), cell=40, idx=False, label='replicate padding'), gsvg(mp, border(4), cell=40, idx=False, label='symmetric (mirror) padding')) + '<p style="color:var(--muted)">red = the added padding around the 2×2 image [1 2; 3 4].</p></div></div>',
        use='read the padding in every question; zero vs replicate only changes the border outputs.', tag='3'))
    H.append('<div class="lab" data-lab="filter" data-init=\'{"f": [[1, 2, 4, 5], [5, 2, 5, 2], [1, 1, 3, 6], [2, 4, 6, 7]], "w": [[1, 2, 1], [2, 4, 2], [1, 2, 1]], "scale": "1/16", "pad": "zero", "title": "Filtering lab: slide the kernel yourself"}\'></div>')

    H.append(lesson('Separable kernels: a column times a row',
        'Some kernels are a column vector times a row vector: w = u vᵀ. Then filtering with w is the same as filtering with u down the columns and then with vᵀ along the rows — two cheap 1-D passes instead of one 2-D pass.',
        '<div class="cols"><div><p><b>Test:</b> every row of the kernel is a multiple of the same row. 1-2-1 / 2-4-2 / 1-2-1 = (1, 2, 1)ᵀ (1, 2, 1) ✓. Box kernels and Gaussians are separable; the Laplacian is not.</p>'
        '<p><b>Speed-up:</b> a p×q kernel needs p·q multiplications per pixel; two passes need p + q. Ratio C = pq/(p + q): 3×3 → 1.5×, 11×11 → 5.5×.</p>'
        '<p><b>Use on the calculator:</b> for a small image, the whole filtered image is T<sub>u</sub> · F · T<sub>v</sub>ᵀ (calculator section, “Think in matrices”).</p></div>'
        '<div>' + figs(gsvg([[1], [2], [1]], {}, cell=40, idx=False, label='u (column)'), gsvg([[1, 2, 1]], {}, cell=40, idx=False, label='vᵀ (row)'), gsvg(W121, {(i, j): 'n4' for i in range(3) for j in range(3)}, cell=40, idx=False, label='u vᵀ: row i = u(i) × the row')) + '</div></div>',
        use='textbook 3.20, 3.22, 3.24, 3.44; the calculator matrix trick.', tag='4'))

    H.append(lesson('The frequency view of filtering (slides “Basics of filtering”)',
        'Any image can be built from waves (sinusoids) of different frequencies: slowly varying regions are low frequencies, edges and fine detail are high frequencies. Filtering means keeping or removing some frequencies.',
        '<p>A <b>lowpass</b> filter keeps the slow variations and removes the fast ones → <b>smoothing / blurring</b> (Section 3.5). A <b>highpass</b> filter keeps the fast variations → <b>sharpening / edges</b> (Section 3.6). The key fact linking the two views: <b>convolution in space = multiplication in frequency</b> (Chapter 4).</p>',
        tag='5'))

    # ── questions ──
    H.append('<h3 id="ch3-filt-q">Questions on filtering mechanics</h3>')
    f241 = [[0, 2, 0], [3, 5, 2], [0, 4, 0]]; h241 = [[1, 2, 1], [1, 2, 2], [2, 1, 3]]
    m = ANS['m2425_1']
    fa, ta = window_fig(f241, 1, 1, h241, 'zero', label_kernel='14·h')
    fb, tb = window_fig(f241, 1, 1, h241, 'zero', conv=True, label_kernel='14·h')
    H14 = np.array(h241, float); H14r = np.rot90(H14, 2)
    ca, _ = trace_lines(f241, H14, 'MatB', 14, 2)
    cb, _ = trace_lines(f241, H14r, 'MatC', 14, 2)
    cc, Gc = m4_lines(f241, H14, 14, 'correlation × 14')
    cv, Gv = m4_lines(f241, H14r, 14, 'convolution × 14')
    H.append(set_solution(card('o24q1'), walk([
        ('Work with 14·h, divide at the end', 'h = ¹⁄₁₄ × [1 2 1; 1 2 2; 2 1 3]. Use the whole numbers and divide every sum by 14. For convolution you need the kernel turned 180° (read it backwards from the bottom-right corner): [3 1 2; 2 2 1; 1 2 1].', None,
         MAT_APP + mdef('MatB', H14, '14·h, the kernel for correlation') + mdef('MatC', H14r, '14·h rotated 180°, the kernel for convolution')),
        ('Correlation at the centre (1, 1)', f'The window is the whole image. Sum of products = {fmt(ta)} → ÷14 = {fmt(round(ta / 14, 4))} → rounded <b>2</b>.', fa,
         mdef('MatA', f241, 'the 3×3 window around (1, 1) — here the whole image') + TRN + ca),
        ('Convolution at the centre: turn h first', f'Rotated kernel [3 1 2; 2 2 1; 1 2 1]. Sum = {fmt(tb)} → ÷14 = {fmt(round(tb / 14, 4))} → <b>2</b>.', fb, cb),
        ('All nine pixels, correlation (zero padding)', 'Repeat at every pixel (corners use zeros outside). On paper: slide the window. On the calculator: the whole 3×3 output in two lines (row-shift method). Then ÷ 14 and round to the nearest integer in 0 … 7 (halves round up: 21/14 = 1.5 → 2):', figs(gsvg(m['corr14'], {}, cell=40, idx=False, label='correlation × 14'), gsvg(m['corr_q'], {(i, j): 'hl' for i in range(3) for j in range(3)}, cell=40, idx=False, label='correlation, 3-bit')), cc),
        ('All nine pixels, convolution', 'Same two lines, but the R matrices are built from the rows of the <b>rotated</b> kernel (3 1 2 / 2 2 1 / 1 2 1). Round the same way.', figs(gsvg(m['conv14'], {}, cell=40, idx=False, label='convolution × 14'), gsvg(m['conv_q'], {(i, j): 'hl' for i in range(3) for j in range(3)}, cell=40, idx=False, label='convolution, 3-bit')), cv),
        ('Compare', 'The two results differ because h is not symmetric under a half-turn. For a symmetric kernel they would be identical.', None),
    ]) + '<div class="ansbig">Correlation [2 2 1; 2 2 1; 1 2 1], convolution [1 1 1; 1 2 2; 1 2 2] (3-bit, rounded); they differ because h is not 180°-symmetric.</div>'))
    assert np.allclose(Gc, m['corr14']) and np.allclose(Gv, m['conv14'])

    f318 = np.zeros((5, 5)); f318[1:4, 2] = 1
    full = ANS['p318']['conv_full']
    fc, tc = window_fig(f318.tolist(), 1, 2, W121, 'zero')
    H.append(set_solution(card('tb3-18'), walk([
        ('Set up', 'f is a vertical line of three 1s. “Minimum zero padding” for the full result: pad by 2 on every side so every kernel entry meets every pixel → output 7×7.', None),
        ('One position (row 2, column 3, counted from 1 = (1, 2) from 0)', f'Window × kernel (the kernel is symmetric, so convolution = correlation): the window contains two of the line’s 1s (under the centre weight 4 and the weight 2 below it); sum = <b>{fmt(tc)}</b>.', fc,
         MAT_APP + mdef('MatA', [[0, 0, 0], [0, 1, 0], [0, 1, 0]], 'the window at that position') + mdef('MatB', W121, 'the kernel w') + TRN + trace_lines([[0, 0, 0], [0, 1, 0], [0, 1, 0]], W121)[0]),
        ('Whole result', 'Each 1 of the line drops a copy of the kernel centred on itself; the three copies overlap and add up.', gsvg([[int(v) for v in r] for r in full], {(i, j): 'hl' for i in range(7) for j in range(7) if full[i][j]}, cell=38, idx=False, label='full convolution (7×7)')),
    ]) + '<div class="ansbig">Columns 2–4 of the 7×7 result: rows 1–5 = (1 2 1), (3 6 3), (4 8 4), (3 6 3), (1 2 1); everything else 0. Correlation is the same (w is symmetric).</div>'))
    H.append(set_solution(card('tb3-20'), walk([
        ('(a) Split w into a column times a row', 'w = [1 2 1; 2 4 2; 1 2 1]: every row is a multiple of (1 2 1), with multipliers 1, 2, 1. So w = w₁ w₂ with w₁ = [1 2 1]ᵀ (column) and w₂ = [1 2 1] (row). Convolution is associative, so w ★ f = w₂ ★ (w₁ ★ f).', None,
         MAT_APP + mdef('MatB', [[1], [2], [1]], 'w₁, the 3×1 column') + mdef('MatC', [[1, 2, 1]], 'w₂, the 1×3 row')
         + cl(K('MatB', '×', 'MatC', 'EXE'), 'column × row = the outer product; it must give back w', lcdmat('MatAns', W121))),
        ('(b) Column pass w₁ ★ f', 'Only the middle column of f is non-zero: [0 1 1 1 0]ᵀ. Convolving it with (1 2 1) down the column (full size, zero padding) gives [0 1 3 4 3 1 0]ᵀ: e.g. the middle entry = 1·1 + 2·1 + 1·1 = 4. The result is 7×5 with 1, 3, 4, 3, 1 down the middle column.', None),
        ('(c) Row pass w₂ ★ (w₁ ★ f)', 'Each value c of that column spreads across three columns as (c, 2c, c) → rows (1 2 1), (3 6 3), (4 8 4), (3 6 3), (1 2 1). Identical to 3.18(b), with 3 + 3 = 6 multiplications per pixel instead of 9.', gsvg([[int(v) for v in r] for r in full], {(i, j): 'hl' for i in range(7) for j in range(7) if full[i][j]}, cell=38, idx=False, label='same 7×7 result as 3.18')),
    ]) + '<div class="ansbig">w₁ = [1 2 1]ᵀ (column), w₂ = [1 2 1] (row). (b) w₁ ★ f puts 1, 3, 4, 3, 1 down the middle column (7×5). (c) Then w₂ spreads each row as (1, 2, 1) → the same 7×7 result as 3.18(b).</div>'))
    DET = cl(K('CATALOG', '>Matrix', '>Matrix Calc', '>Determinant'), 'types Det( — then the matrix name and close the bracket')
    H.append(set_solution(card('tb3-22'), walk([
        ('(a) v wᵀ is a column times a row', 'Separable means exactly “kernel = column × row” (rank 1). v wᵀ is built that way, so it is separable — a 3×4 kernel.', None,
         MAT_APP + mdef('MatB', [[1], [2], [1]], 'v, 3×1') + mdef('MatC', [[2, 1, 1, 3]], 'wᵀ, 1×4')
         + cl(K('MatB', '×', 'MatC', 'EXE'), 'the kernel v wᵀ: every row is a multiple of (2 1 1 3)', lcdmat('MatAns', [[2, 1, 1, 3], [4, 2, 2, 6], [2, 1, 1, 3]]))),
        ('(b) Check rank 1', 'Row 2 = 2 × row 1, so every 2×2 block has determinant 0 → rank 1 → separable.', None,
         mdef('MatA', [[1, 3], [2, 6]], 'a 2×2 block of w (first two columns)') + DET + cl(K('Det(MatA)', 'EXE'), 'screen 0 → the rows are proportional', lcdmat('Det', [[0]]))),
        ('(b) Read off the two pieces', 'Column 1 = [1 2]ᵀ is w₁; row 1 = [1 3 1] is w₂ (because w₁’s first entry is 1). Check: [1 2]ᵀ × [1 3 1] = [1 3 1; 2 6 2] ✓.', None,
         mdef('MatB', [[1], [2]], 'w₁, 2×1') + mdef('MatC', [[1, 3, 1]], 'w₂, 1×3') + cl(K('MatB', '×', 'MatC', 'EXE'), 'gives back w', lcdmat('MatAns', [[1, 3, 1], [2, 6, 2]]))),
    ]) + '<div class="ansbig">(a) Yes — any outer product u vᵀ is rank 1, hence separable (here 3×4). (b) w₁ = [1 2]ᵀ, w₂ = [1 3 1].</div>'))
    SX = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]; SY = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    H.append(set_solution(card('tb3-44'), walk([
        ('The test', 'A kernel is separable ⇔ it is a column times a row ⇔ all its rows are multiples of one row (rank 1) ⇔ every 2×2 block has determinant 0. One non-zero 2×2 determinant is enough to say “not separable”.', None),
        ('Laplacians', '4-neighbour rows (0 1 0) and (1 −4 1) are not proportional. The block [0 1; 1 −4] has determinant −1 ≠ 0 → rank ≥ 2 → <b>not separable</b>. The 8-neighbour one: rows (1 1 1), (1 −8 1) — same conclusion (block [1 1; 1 −8], det −9).', None,
         MAT_APP + mdef('MatA', [[0, 1], [1, -4]], 'top-left 2×2 block of the 4-neighbour Laplacian') + DET + cl(K('Det(MatA)', 'EXE'), 'screen −1 ≠ 0 → not rank 1', lcdmat('Det', [[-1]]))),
        ('Roberts', '[−1 0; 0 1] (and [0 −1; 1 0]) have determinant ≠ 0 → rank 2 → <b>not separable</b>.', None,
         mdef('MatA', [[-1, 0], [0, 1]], 'the Roberts kernel') + cl(K('Det(MatA)', 'EXE'), 'screen −1 ≠ 0', lcdmat('Det', [[-1]]))),
        ('Sobel', 'Rows of the first Sobel are (−1)(1 2 1), 0·(1 2 1), (+1)(1 2 1) → rank 1: a derivative [−1 0 1]ᵀ down the column times a smoothing [1 2 1] along the row. The second Sobel is its transpose: [1 2 1]ᵀ × [−1 0 1].', None,
         mdef('MatB', [[-1], [0], [1]], 'v = derivative column') + mdef('MatC', [[1, 2, 1]], 'wᵀ = smoothing row') + cl(K('MatB', '×', 'MatC', 'EXE'), 'gives the first Sobel kernel ✓', lcdmat('MatAns', SX))
         + cl(K('Trn(MatAns)', 'EXE'), 'its transpose is the other Sobel kernel ([1 2 1]ᵀ × [−1 0 1])', lcdmat('MatAns', SY))),
    ]) + '<div class="ansbig">Laplacians: no (rank 2). Roberts: no (rank 2). Sobel: yes — [−1 −2 −1; 0 0 0; 1 2 1] = [−1 0 1]ᵀ [1 2 1] and [−1 0 1; −2 0 2; −1 0 1] = [1 2 1]ᵀ [−1 0 1].</div>'))
    H.append(card('d25q2c'))
    f18 = [[3, 7, 6, 2, 0], [2, 4, 6, 1, 1], [4, 7, 2, 5, 4], [3, 0, 6, 2, 1], [5, 7, 5, 1, 2]]
    box = [[1, 1, 1]] * 3
    fz, tz = window_fig(f18, 0, 0, box, 'zero', label_kernel='box (÷ 9)')
    fr, tr = window_fig(f18, 0, 0, box, 'replicate', label_kernel='box (÷ 9)')
    H.append(set_solution(card('s18q2'), walk([
        ('Border methods', '(1) zero padding, (2) replicate the edge pixels, (3) mirror the image, (4) leave the border pixels unfiltered or crop to where the window fits, (5) treat the image as periodic. Name the one you use.', None),
        ('Corner pixel with zero padding', f'Window around (0, 0); five of the nine values are padding zeros. Sum = {fmt(tz)} → ÷9 = {fmt(round(tz / 9, 4))} → <b>2</b>.', fz,
         cl(K('3', '+', '7', '+', '2', '+', '4', 'EXE'), 'the four real pixels in the window (the padding adds 0) = 16')
         + cl(K('Ans', '÷', '9', 'EXE'), '1.777… → round → 2')),
        ('Same corner with replicate padding', f'The padding copies the edge, so the corner pixel 3 counts four times. Sum = {fmt(tr)} → ÷9 = {fmt(round(tr / 9, 4))} → <b>4</b>.', fr,
         cl(K('4', '×', '3', '+', '2', '×', '7', '+', '2', '×', '2', '+', '4', 'EXE'), 'corner 3 four times, its neighbours 7 and 2 twice each, the diagonal 4 once = 34')
         + cl(K('Ans', '÷', '9', 'EXE'), '3.777… → round → 4')),
        ('Whole image (zero padding) — Spreadsheet app', 'The Matrix app stops at 4×4, so use the Spreadsheet: one Sum( per output pixel adds its window (with zero padding the window just gets smaller at the borders). The screen shows the window sums S; the output is S ÷ 9 rounded. Quick rounding: S rounds to k when S is within 4 of 9k (e.g. 28 → 27 = 9·3 → 3; 13 → 9 → 1; 41 → 45 → 5).', figs(gsvg(ANS['m18_2_zero']['r'], {}, cell=36, idx=False, label='zero padding, rounded'), gsvg(ANS['m18_2_replicate']['r'], {}, cell=36, idx=False, label='replicate, rounded')),
         cl(K('HOME', '>Spreadsheet'), 'type the image into A1:E5 (each value + EXE); rows 1–5 = image rows 0–4')
         + cl(K('TOOLS', '>Fill Formula'), 'interior pixels: Form <b>Sum(A1:C3)</b>, Range <b>B8:D10</b> (no “=” in Form; Sum( and the colon are in CATALOG → Spreadsheet; letters A–E = SHIFT 4, 5, 6, 1, 2). The formula shifts with the cell, so each cell adds its own 3×3 window')
         + cl(K('TOOLS', '>Fill Formula'), 'borders, one Fill Formula each: top B7:D7 Sum(A1:C2) · bottom B11:D11 Sum(A4:C5) · left A8:A10 Sum(A1:B3) · right E8:E10 Sum(D1:E3) · corners A7 Sum(A1:B2), E7 Sum(D1:E2), A11 Sum(A4:B5), E11 Sum(D4:E5)',
              lcdmat('A7:E11 = window sums S', [[int(v) for v in r] for r in filt(f18, box, 'zero')]))
         + cl('read rows 7–11', 'S ÷ 9, rounded = the zero-padding answer. Replicate padding: the 9 interior sums are the same; for the 16 border pixels add the copied edge values by hand as in step 3')),
    ]) + '<div class="ansbig">Zero padding: rows 2 3 3 2 0 / 3 5 4 3 1 / 2 4 4 3 2 / 3 4 4 3 2 / 2 3 2 2 1. Replicate: 4 5 5 3 1 / 4 5 4 3 2 / 3 4 4 3 2 / 4 4 4 3 2 / 4 5 4 3 2.</div>'))
    for cid in ['sl-1d', 'sl-2d', 'tb3-24', 'dr-sep', 'tb3-31']: H.append(card(cid))
    H.append('</section>')
    return '\n'.join(H)
