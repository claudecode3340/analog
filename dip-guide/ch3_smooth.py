"""Chapter 3.5 rebuilt: smoothing — box, Gaussian, median — with photos and numbers; every smoothing past paper as a
step-by-step walk (window, kernel, products, sum, then the whole output)."""
from ch3lib import *
import math
import numpy as np
from ch3_filt import mdef, band, trace_lines, sep_lines, m4_lines, MAT_APP, TRN, _q

I44 = [[1, 2, 4, 5], [5, 2, 5, 2], [1, 1, 3, 6], [2, 4, 6, 7]]
W121 = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
LAP = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
a07 = math.exp(-1 / (2 * 0.49))
G07 = [[a07 * a07, a07, a07 * a07], [a07, 1, a07], [a07 * a07, a07, a07 * a07]]


def hand_band(k, extra=''):
    a, b, c = k
    return f'type this band matrix in by hand (Define New): diagonal = {b}, just above and below the diagonal = {a}, everything else 0{extra}. (There is no “tridiag” key — you type every entry.)'


def grid_out(M, label, d=4, cell=46):
    return gsvg([[fmt(round(float(v), d)) for v in r] for r in M], {}, cell=cell, idx=False, label=label)


def section(card):
    H = ['''<section class="topic" id="ch3-smooth">
  <div class="eyebrow">Chapter 3.5 · Lecture 10</div>
  <h2>Smoothing filters: averaging away noise and detail</h2>
  <div class="meta"><span class="chip ">TB 3.5</span><span class="chip ">slides pp. 31–34</span><span class="chip hot">Quiz-1 Q1 · every mid-sem Q2</span></div>
  <p class="lede">Smoothing replaces each pixel by an average of its neighbourhood. Random noise averages out, sharp edges and fine detail get blurred. These are <b>lowpass</b> filters (they keep slow variations). Exam questions give you a small image and a kernel — box, weighted mean, Gaussian — and ask for one pixel or the whole output with a given padding; the median filter appears as theory.</p>''']

    H.append(lesson('Box filter: the plain average',
        'The p×q box kernel gives every pixel in the window the same weight 1/(pq). A 3×3 box filter replaces each pixel by the average of the 9 pixels around it.',
        '<div class="cols"><div><p><b>Example.</b> Window [3 7 6; 2 4 6; 4 7 2]: sum = 41, average = 41/9 = <b>4.56</b>.</p>'
        '<p><b>Bigger box = more blur.</b> The photos show 3×3, 11×11 and 21×21 boxes. Uses (your slide): reduce noise, remove “irrelevant” small detail, smooth false contours caused by too few grey levels.</p>'
        '<p><b>Weighted mean</b> ¹⁄₁₆[1 2 1; 2 4 2; 1 2 1]: the centre counts most, the corners least — it blurs less than the box and looks more natural. Its weights add up to 16, hence the ¹⁄₁₆.</p></div>'
        '<div>' + figs(img('cam', 130, 'original'), img('box_3', 130, 'box 3×3'), img('box_11', 130, 'box 11×11'), img('box_21', 130, 'box 21×21')) + '</div></div>',
        tag='1'))

    G1 = [[round(math.exp(-(s * s + t * t) / 2), 4) for t in (-1, 0, 1)] for s in (-1, 0, 1)]
    H.append(lesson('Gaussian filter: a smooth bell-shaped average',
        'The weight of each pixel depends only on its distance r from the centre, falling off like a bell curve: G = c·e<sup>−r²/2σ²</sup>. σ controls the width: bigger σ = wider bell = more blur. After computing the weights, divide by their sum so they add up to 1.',
        '<div class="cols"><div>'
        '<div class="formula">\\(G(s,t)=c\\,e^{-\\frac{s^2+t^2}{2\\sigma^2}}\\)<span class="say">s, t = row and column offset from the centre; s² + t² = r² (squared distance). For a 3×3 kernel: centre r² = 0, edges r² = 1, corners r² = 2.</span></div>'
        '<p><b>Example (your slide, c = 1, σ = 1):</b> centre e⁰ = 1, edge e<sup>−1/2</sup> = 0.6065, corner e<sup>−1</sup> = 0.3679 (corner = edge²). Sum = 1 + 4(0.6065) + 4(0.3679) = <b>4.8976</b>; divide every weight by it.</p>'
        '<p><b>Quiz-1 2026 (σ = 0.7):</b> edge e<sup>−1/(2·0.49)</sup> = 0.3604, corner 0.1299, sum = 2.9612.</p>'
        '<p><b>Kernel size rule:</b> the bell is essentially zero beyond 3σ, so use the smallest odd size ≥ 6σ (σ = 1 → 7×7). Gaussians are separable and look the same in every direction (the only kernels that are both).</p></div>'
        '<div>' + figs(gsvg(G1, {(i, j): 'n4' for i in range(3) for j in range(3)}, cell=76, idx=False, label='σ = 1 before dividing by 4.8976'), img('gauss_35', 150, 'Gaussian σ = 3.5 on the photo')) + '</div></div>',
        use='Quiz-1 2026 Q1 (σ = 0.7, replicate padding, one pixel), slide example, textbook 3.27–3.28.', tag='2'))
    H.append('<div class="lab" data-lab="gauss" data-init=\'{}\'></div>')

    H.append(lesson('Median filter: the middle value (nonlinear)',
        'Sort the window’s values and take the middle one. A few extreme values (salt-and-pepper noise) cannot move the middle, so they vanish — while edges stay much sharper than with averaging.',
        '<div class="cols"><div><p><b>Example.</b> Window 10, 12, 255, 11, 0, 13, 12, 14, 11 (one white and one black noise dot). Sorted: 0, 10, 11, 11, <b>12</b>, 12, 13, 14, 255 → median <b>12</b>. The mean would be 37.6 — dragged up by the 255.</p>'
        '<p>Other order-statistic filters: <b>max</b> (finds the brightest points) and <b>min</b> (darkest points). All are nonlinear.</p></div>'
        '<div>' + figs(img('sp', 130, 'salt-and-pepper noise'), img('sp_box3', 130, '3×3 box: smeared dots'), img('sp_med3', 130, '3×3 median: clean')) + '</div></div>',
        tag='3'))

    # ── questions ──
    H.append('<h3 id="ch3-smooth-q">Questions on smoothing</h3>')
    fq = [[2, 1.5, 1, 3.2], [4, 4.3, math.pi, 2], [3, 0.5, math.e, math.sqrt(2)]]
    fig, tot = window_fig(fq, 0, 3, G07, 'replicate', label_kernel='Gaussian weights (not yet divided)')
    vq = np.array([a07, 1, a07]); Wq = np.array([[1, 3.2, 3.2], [1, 3.2, 3.2], [math.pi, 2, 2]])
    prod = np.outer(vq, vq) * Wq; S = float(vq @ Wq @ vq); ksum = (1 + 2 * a07) ** 2
    H.append(set_solution(card('qz1'), walk([
        ('Build the kernel: only one number to compute',
         'On a 3×3 grid the squared distance s² + t² is 0 (centre), 1 (4 edges) or 2 (4 corners). So the weights are 1, a, a² with a = e<sup>−1/(2σ²)</sup> = e<sup>−1/0.98</sup> = <b>0.3604</b>, corner a² = 0.1299. Kernel sum = 1 + 4a + 4a² = (1 + 2a)² = <b>2.9615</b>.',
         gsvg([[fmt(round(v, 4)) for v in r] for r in G07], {(i, j): 'n4' for i in range(3) for j in range(3)}, cell=76, idx=False, label='weights before dividing'),
         cl(K('SHIFT', '8', 'x^■', '(', 'SHIFT', '−', '1', '÷', '(', '2', '×', '0.7', 'x²', ')', ')', 'EXE'), 'computes a = e<sup>−1/(2·0.7²)</sup>; screen shows 0.360447788')
         + cl(K('VARIABLE', '>A=', '>Store'), 'saves a in A, so you never retype the decimals')
         + cl(K('(', '1', '+', '2', 'A', ')', 'x²', 'EXE'), 'kernel sum (1 + 2a)² = 2.961481588 — the number you divide by at the end')),
        ('Write the kernel as column × row',
         'Because e<sup>−(s²+t²)/2σ²</sup> = e<sup>−s²/2σ²</sup> · e<sup>−t²/2σ²</sup>, the kernel is v·vᵀ with v = (a, 1, a). Check: a·a = corner, a·1 = edge, 1·1 = centre.',
         figs(gsvg([['a'], ['1'], ['a']], {}, cell=40, idx=False, label='v (column)'), gsvg([['a', '1', 'a']], {}, cell=40, idx=False, label='vᵀ (row)')),
         cl(K('HOME', '>Matrix', 'OK'), 'opens the Matrix app')
         + cl(K('TOOLS', '>MatB', 'OK', '>Define New'), '1×3, type A, 1, A (the letter A, not 0.36) — this is vᵀ')
         + cl(K('TOOLS', '>MatC', 'OK', '>Define New'), '3×1, type A, 1, A — this is v')),
        ('Build the window with replicate padding',
         'g(0, 3) is the top-right pixel. The row above (−1) copies row 0; the column to the right (4) copies column 3. Window = [1 3.2 3.2; 1 3.2 3.2; π 2 2].',
         fig,
         cl(K('TOOLS', '>MatA', 'OK', '>Define New'), '3×3, type 1, 3.2, 3.2, 1, 3.2, 3.2, π, 2, 2 — the window (red cells are the copied padding)', lcdmat('MatA = 3×3', [[1, 3.2, 3.2], [1, 3.2, 3.2], [3.1416, 2, 2]]))),
        ('Multiply and add all nine products in one go',
         f'MatA × MatC weights each window row by (a, 1, a) and adds it; MatB × that weights the three row results by (a, 1, a). Together that is the sum of the nine products = <b>{S:.4f}</b>.',
         gsvg([[fmt(round(v, 4)) for v in r] for r in prod], {(i, j): 'n8' for i in range(3) for j in range(3)}, cell=76, idx=False, label='the nine products being added'),
         cl(K('MatB', '×', 'MatA', '×', 'MatC', 'EXE'), 'sum of products, before normalising', lcdmat('MatAns', [[round(S, 9)]]))),
        ('Normalise: divide by the kernel sum',
         f'{S:.4f} ÷ {ksum:.4f} = <b>{S / ksum:.4f}</b>. (With weights rounded to 4 decimals you get 2.9612 as the sum; the answer is still 2.6345.)',
         None,
         cl(K('Ans', '÷', '(', '1', '+', '2', 'A', ')', 'x²', 'EXE'), f'screen shows {S / ksum:.9f} → report 2.6345')),
    ]) + '<div class="ansbig">g(0, 3) = 2.6345.</div>'))

    for cid, A, B, pa, pb in [('m23q2', W121, LAP, 'zero', 'replicate'), ('m24q2', W121, LAP, 'replicate', 'zero')]:
        fa, ta = window_fig(I44, 0, 0, A, pa, label_kernel='weights 1 2 1 / 2 4 2 / 1 2 1')
        fb, tb = window_fig(I44, 0, 0, B, pb, label_kernel='Laplacian')
        ga = filt(I44, A, pa) / 16; gb = filt(I44, B, pb)
        rp = pa == 'replicate'; T = band((1, 2, 1), 4, rp); Dm = band((1, -2, 1), 4, pb == 'replicate')
        assert np.allclose(T @ np.array(I44) @ T.T / 16, ga) and np.allclose(Dm @ np.array(I44) + np.array(I44) @ Dm, gb)
        c1, _ = sep_lines([1, 2, 1], pad(I44, 1, pa)[:3, :3], [1, 2, 1], 16)
        c3, _ = trace_lines(pad(I44, 1, pb)[:3, :3], B, 'MatB')
        H.append(set_solution(card(cid), walk([
            (f'(a) Weighted mean, {pa} padding — corner pixel (0, 0)', f'Sum of products = {fmt(ta)} → ÷16 = <b>{fmt(round(ta / 16, 4))}</b>. ' + ('Zero padding: the five outside weights multiply 0.' if pa == 'zero' else 'Replicate: the outside cells copy the edge pixels.') + ' The kernel is (1 2 1)ᵀ × (1 2 1), so the calculator does it as row × window × column.', fa,
             MAT_APP + c1),
            ('(a) the whole image', 'Same at all 16 pixels. Calculator: T·F·Tᵀ ÷ 16, where T is the 4×4 band matrix of (1 2 1): T·F adds rows i−1, i, i+1 of F with weights 1 2 1 (the vertical pass), ·Tᵀ does the same along each row (the horizontal pass). ' + ('Zero padding: plain band.' if not rp else 'Replicate padding: row −1 copies row 0, so its weight 1 lands on row 0 → the corners of T become 2 + 1 = 3.'), grid_out(ga, 'weighted mean'),
             mdef('MatA', I44, 'the image F') + mdef('MatB', T, 'T for the smoothing kernel (1 2 1): ' + hand_band((1, 2, 1), '; replicate padding: change the two corners to 3' if rp else '; zero padding: nothing else'))
             + cl(K('MatB', '×', 'MatA', '×', 'Trn(MatB)', '÷', '16', 'EXE'), 'vertical pass, horizontal pass, then the ¹⁄₁₆ — every output pixel at once (Trn( from CATALOG → Matrix → Matrix Calc)', lcdmat('MatAns', _q(ga)))),
            (f'(b) Laplacian, {pb} padding — corner pixel (0, 0)', f'Neighbours up + down + left + right − 4 × centre = <b>{fmt(tb)}</b>.', fb,
             mdef('MatA', pad(I44, 1, pb)[:3, :3], f'the window around (0, 0), {pb} padding') + mdef('MatB', B, 'the Laplacian kernel (replaces T; step 2 is done)') + TRN + c3),
            ('(b) Why the Laplacian is D·F + F·D (and not T·F·Tᵀ)', 'Each 1-D kernel gets its own band matrix: the smoothing kernel (1 2 1) gave T, the second-difference kernel (1 −2 1) gives D. '
             'D·F applies f(x−1, y) − 2f(x, y) + f(x+1, y) down every column (vertical 2nd difference); F·D applies f(x, y−1) − 2f(x, y) + f(x, y+1) along every row (horizontal 2nd difference). '
             'Adding them gives the 4 neighbours − 4·centre = the [0 1 0; 1 −4 1; 0 1 0] Laplacian (the −4 is −2 from each direction). The weighted mean was <b>one</b> kernel = column × row, so it was one product T·F·Tᵀ; the Laplacian is a <b>sum</b> of two directions, so it is D·F + F·D. '
             + ('Zero padding: plain D.' if pb == 'zero' else 'Replicate padding: the outside neighbour is a copy of the edge pixel, adding +1 to its −2 → D’s two corners become −1.'), None,
             mdef('MatA', I44, 'the image F again') + mdef('MatC', Dm, 'D for (1 −2 1): ' + hand_band((1, -2, 1), '; replicate padding: change the two corners to −1' if pb == 'replicate' else '; zero padding: nothing else'))
             + cl(K('MatC', '×', 'MatA', 'EXE'), 'D·F: the vertical second difference of every pixel', lcdmat('MatAns', _q(Dm @ np.array(I44, float))))
             + cl(K('MatA', '×', 'MatC', 'EXE'), 'F·D: the horizontal second difference of every pixel', lcdmat('MatAns', _q(np.array(I44, float) @ Dm)))),
            ('(b) the whole image', 'Add the two directions. Positive = the pixel is darker than its neighbours, negative = brighter.', grid_out(gb, 'Laplacian', d=0),
             cl(K('MatC', '×', 'MatA', '+', 'MatA', '×', 'MatC', 'EXE'), 'both directions in one line = the Laplacian of every pixel (matches the window method at (0, 0))', lcdmat('MatAns', _q(gb)))),
        ]) + '<div class="ansbig">The two 4×4 outputs in steps 2 and 5.</div>'))

    o = ANS['m2324_2']; blk = [[15, 7, 0], [7, 15, 7], [0, 7, 15]]
    F2 = [[.01, .1, .01], [.1, .56, .1], [.01, .1, .01]]
    f1, t1 = window_fig(blk, 1, 1, LAP, 'zero', label_kernel='Filter-1')
    f2, t2 = window_fig(blk, 0, 1, F2, 'zero', label_kernel='Filter-2')
    D3 = band((1, -2, 1), 3); assert np.allclose(D3 @ np.array(blk) + np.array(blk) @ D3, o['f1'])
    w01 = pad(blk, 1, 'zero')[0:3, 1:4]; c2, _ = trace_lines(w01, F2, 'MatB')
    c4, G2 = m4_lines(blk, F2, name='Filter-2 output'); assert np.allclose(G2, o['f2'])
    f5 = [[0] * 5, [0, 15, 7, 0, 0], [0, 7, 15, 7, 0], [0, 0, 7, 15, 0], [0] * 5]
    H.append(set_solution(card('o23q2'), walk([
        ('The image from Question 1', 'The question says “apply to the image given in Question-1”. That image (Oct 2023 Q1, 4-bit) is f = [0 0 0 0 0; 0 15 7 0 0; 0 7 15 7 0; 0 0 7 15 0; 0 0 0 0 0]. “The non-zero pixels” = the 3×3 block in rows 1–3, columns 1–3: [15 7 0; 7 15 7; 0 7 15]. The zeros around it act as zero padding, so filter just this block with zero padding.',
         gsvg(f5, {(i, j): 'hl' for i in range(1, 4) for j in range(1, 4)}, cell=38, idx=True, label='5×5 image of Q1; highlighted = the block to filter')),
        ('Identify the filters', 'Filter-1 = the 4-neighbour Laplacian (weights add to 0 → highpass, finds detail). Filter-2 = a Gaussian-like weighted average (weights add to 1 → lowpass, smooths).', None),
        ('Filter-1 at the centre', f'7 + 7 + 7 + 7 − 4·15 = <b>{fmt(t1)}</b>. (The zeros around the block act as zero padding.)', f1),
        ('Filter-1, whole block', 'D·F + F·D with the 3×3 band matrix D of (1 −2 1) (zero padding = plain band): D·F = up + down − 2·centre, F·D = left + right − 2·centre.', grid_out(o['f1'], 'Filter-1', d=0),
         MAT_APP + mdef('MatA', blk, 'the non-zero block F') + mdef('MatD', D3, 'D for (1 −2 1): ' + hand_band((1, -2, 1), ' (3×3, zero padding)'))
         + cl(K('MatD', '×', 'MatA', '+', 'MatA', '×', 'MatD', 'EXE'), 'the Laplacian of all nine pixels', lcdmat('MatAns', _q(o['f1'])))),
        ('Filter-2 at an edge pixel (0, 1)', f'Sum of products = <b>{fmt(round(t2, 4))}</b> (the official key prints 6.99: it dropped the 0.01 × 7 term).', f2,
         mdef('MatA', w01, 'the window around (0, 1) (top row is outside the block = 0)') + mdef('MatB', F2, 'Filter-2') + TRN + c2),
        ('Filter-2, whole block', 'Filter-2 is not a column × row (0.1·0.1/0.01 = 1 ≠ 0.56), so use the row-shift method: G = (F down)·R₀ + F·R₁ + (F up)·R₂, where R is built from one kernel row (a b c) as [b a 0; c b a; 0 c b]. Each product slides one kernel row along every image row; the shifted copies of F supply the row above / below each pixel.', grid_out(o['f2'], 'Filter-2', d=2, cell=56), c4),
    ]) + '<div class="ansbig">Filter-1: [−46 2 14; 2 −32 2; 14 2 −46]. Filter-2: [9.95 7.06 1.55; 7.06 11.5 7.06; 1.55 7.06 9.95].</div>'))

    e25 = [[1, 2, 3, 2], [4, 2, 5, 1], [1, 2, 6, 3], [2, 6, 4, 7]]
    fbx, tbx = window_fig(e25, 0, 0, [[1, 1, 1]] * 3, 'replicate', label_kernel='box (÷ 9)')
    Tb = band((1, 1, 1), 4, True); Gb = Tb @ np.array(e25) @ Tb.T / 9; assert np.allclose(Gb, filt(e25, [[1, 1, 1]] * 3, 'replicate') / 9)
    H.append(set_solution(card('d25q2b'), walk([
        ('Corner pixel with replicate padding', f'Sum = {fmt(tbx)} → ÷9 = {fmt(round(tbx / 9, 4))} → <b>2</b>. The box is (1 1 1)ᵀ × (1 1 1), so on the calculator it is row × window × column.', fbx,
         MAT_APP + sep_lines([1, 1, 1], pad(e25, 1, 'replicate')[:3, :3], [1, 1, 1], 9)[0]),
        ('All pixels, rounded', 'T·F·Tᵀ ÷ 9 with T = band of (1 1 1). Replicate padding: row −1 copies row 0, so its weight 1 adds onto row 0 → corners of T = 1 + 1 = 2. Then round each entry (halves up).', figs(grid_out(filt(e25, [[1, 1, 1]] * 3, 'replicate') / 9, 'exact averages', d=2, cell=52), gsvg(ANS['e25_2b']['r'], {(i, j): 'hl' for i in range(4) for j in range(4)}, cell=44, idx=False, label='rounded')),
         mdef('MatA', e25, 'the image F') + mdef('MatB', Tb, 'T for the box (1 1 1): ' + hand_band((1, 1, 1), '; replicate padding: change the two corners to 2'))
         + cl(K('MatB', '×', 'MatA', '×', 'Trn(MatB)', '÷', '9', 'EXE'), 'all 16 box averages at once; round each one', lcdmat('MatAns', _q(Gb)))),
    ]) + '<div class="ansbig">[2 3 2 2; 2 3 3 3; 3 4 4 4; 3 4 5 5].</div>'))

    q = [[4, 2, 3, 2], [1, 1, 2, 3], [1, 3, 2, 3], [2, 2, 3, 1]]
    L2 = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
    fq1, tq1 = window_fig(q, 0, 0, W121, 'zero', label_kernel='weights (÷ 16)')
    fq2, tq2 = window_fig(q, 0, 0, L2, 'zero', label_kernel='Filter-ii')
    T4 = band((1, 2, 1), 4); D4 = band((1, -2, 1), 4); Qa = np.array(q, float)
    Gq = T4 @ Qa @ T4.T / 16; Lq = -(D4 @ Qa + Qa @ D4)
    assert np.allclose(Gq, filt(q, W121) / 16) and np.allclose(Lq, filt(q, L2))
    H.append(set_solution(card('q21b1'), walk([
        ('(i) Weighted average at (0, 0)', f'Sum = {fmt(tq1)} → ÷16 = {fmt(tq1 / 16)} → nearest integer <b>1</b>. Same at the other diagonal pixels: 1.875 → 2, 2.3125 → 2, 1.125 → 1. Calculator: compute the whole image with T·F·Tᵀ ÷ 16 (T = band of 1 2 1, zero padding) and read the diagonal.', fq1,
         MAT_APP + mdef('MatA', q, 'the image F') + mdef('MatB', T4, 'T for (1 2 1): ' + hand_band((1, 2, 1), '; zero padding'))
         + cl(K('MatB', '×', 'MatA', '×', 'Trn(MatB)', '÷', '16', 'EXE'), 'all 16 weighted averages; you need only the diagonal: ' + ', '.join(fmt(float(Gq[i, i])) for i in range(4)), lcdmat('MatAns', _q(Gq)))),
        ('(ii) Laplacian (centre +4) at (0, 0)', f'4·4 − (2 + 1) = <b>{fmt(tq2)}</b> (zero padding: up and left are 0). The official key prints 16 — it forgot to subtract the two neighbours. Other diagonal pixels: −4, −3, −2. This kernel is minus the usual Laplacian, so the calculator line is −(D·F + F·D).', fq2,
         mdef('MatD', D4, 'D for (1 −2 1): ' + hand_band((1, -2, 1), '; zero padding'))
         + cl(K('SHIFT', '−', '(', 'MatD', '×', 'MatA', '+', 'MatA', '×', 'MatD', ')', 'EXE'), 'SHIFT − types the minus sign; minus (vertical + horizontal second differences); read the diagonal: ' + ', '.join(fmt(float(Lq[i, i])) for i in range(4)), lcdmat('MatAns', _q(Lq)))),
    ]) + '<div class="ansbig">(i) 1, 2, 2, 1. (ii) 13, −4, −3, −2 (if the output must be 3-bit, clip: 7, 0, 0, 0).</div>'))

    H.append(set_solution(card('m23q6'), walk([
        ('Where does blurring change anything?', 'A 3×3 average of a region that is all black stays 0, all white stays 255. Only pixels whose 3×3 window <b>straddles a black/white boundary</b> get an in-between value: 3 white of 9 → 255·3/9 = 85; 6 white of 9 → 170; at a corner where four blocks meet, 4 or 5 white of 9 → 113.3 or 141.7.', None),
        ('Count the boundaries', 'The half-and-half image has one boundary line. The checkerboard has 3 vertical + 3 horizontal boundary lines and 9 points where four blocks meet. Far more boundary → far more grey pixels.', None),
        ('So the histograms differ', 'Before blurring both histograms are just “half 0, half 255”. After blurring the checkerboard has many more pixels at 85 and 170, and some at 113.3 and 141.7 that the other image does not have at all.', None),
    ]) + '<div class="ansbig">(a) No — blurring creates greys only along boundaries, and the checkerboard has much more boundary. (b) See the counts in the original answer box above (filter-where-the-window-fits or border-unchanged reading).</div>'))
    a1 = math.exp(-0.5); s1 = (1 + 2 * a1) ** 2
    H.append(set_solution(card('sl-gauss'), walk([
        ('Three different weights', 'On a 3×3 grid s² + t² is 0 (centre), 1 (edges) or 2 (corners). With σ = 1: centre e⁰ = 1, edge a = e<sup>−1/2</sup> = <b>0.6065</b>, corner e<sup>−1</sup> = a² = <b>0.3679</b>.',
         gsvg([[fmt(round(v, 4)) for v in r] for r in [[a1 * a1, a1, a1 * a1], [a1, 1, a1], [a1 * a1, a1, a1 * a1]]], {(i, j): 'n4' for i in range(3) for j in range(3)}, cell=70, idx=False, label='weights before dividing'),
         cl(K('SHIFT', '8', 'x^■', 'SHIFT', '−', '0.5', 'EXE'), 'SHIFT 8 is e, x^■ the exponent: e<sup>−0.5</sup> = 0.6065306597')
         + cl(K('VARIABLE', '>A=', '>Store'), 'keep the edge weight a in A')),
        ('Sum of the weights', f'1 + 4a + 4a² = (1 + 2a)² = <b>{s1:.4f}</b> (the kernel is (a, 1, a)ᵀ × (a, 1, a)).', None,
         cl(K('(', '1', '+', '2', 'A', ')', 'x²', 'EXE'), f'kernel sum = {s1:.9f}')
         + cl(K('VARIABLE', '>B=', '>Store'), 'keep the sum in B')),
        ('Normalise', f'Divide every weight by the sum: centre 1/{s1:.4f} = <b>{1 / s1:.4f}</b>, edges a/sum = <b>{a1 / s1:.4f}</b>, corners a²/sum = <b>{a1 * a1 / s1:.4f}</b>. Check: 0.2042 + 4(0.1238) + 4(0.0751) ≈ 1.',
         MR(M([[0.0751, 0.1238, 0.0751], [0.1238, 0.2042, 0.1238], [0.0751, 0.1238, 0.0751]], 'normalised G')),
         cl(K('1', '÷', 'B', 'EXE'), f'centre = {1 / s1:.4f}') + cl(K('A', '÷', 'B', 'EXE'), f'edge = {a1 / s1:.4f}') + cl(K('A', 'x²', '÷', 'B', 'EXE'), f'corner = {a1 * a1 / s1:.4f}')),
    ]) + '<div class="ansbig">Centre 0.2042, edges 0.1238, corners 0.0751 (unnormalised sum 4.8976).</div>'))
    for cid in ['dr-six', 'tb3-27', 'tb3-28', 'tb3-35']: H.append(card(cid))
    dm = [10, 12, 255, 11, 0, 13, 12, 14, 11]
    H.append(set_solution(card('dr-med'), walk([
        ('Median: sort and take the middle', f'Sorted: {", ".join(str(v) for v in sorted(dm))} → 9 values, the middle one is the 5th: <b>{int(np.median(dm))}</b>. The 0 and the 255 sit at the two ends and cannot move the middle.', None,
         cl(K('HOME', '>Statistics', '>1-Variable'), 'opens the data list (column x)')
         + cl('10, 12, 255, 11, 0, 13, 12, 14, 11 (each + EXE)', 'the nine window values, in any order')
         + cl(K('OK', '>1-Var Results', 'OK'), 'scroll down to Med', lcd('1-Var Results', '<div>x̄ = 37.55555556</div><div>n = 9</div><div>min(x) = 0</div><div>Med = 12</div><div>max(x) = 255</div>'))),
        ('Mean', f'Sum = {sum(dm)} → ÷9 = <b>{sum(dm) / 9:.2f}</b> — pulled far up by the single 255.', None,
         cl('same screen, x̄', f'x̄ = {sum(dm) / 9:.4f} is the 3×3 mean-filter output')),
    ]) + '<div class="ansbig">Median 12, mean 37.56: the median ignores the salt (255) and pepper (0) pixels; the mean does not.</div>'))
    H.append(card('tb3-29'))
    H.append('</section>')
    return '\n'.join(H)
