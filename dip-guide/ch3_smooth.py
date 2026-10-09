"""Chapter 3.5 rebuilt: smoothing — box, Gaussian, median — with photos and numbers; every smoothing past paper as a
step-by-step walk (window, kernel, products, sum, then the whole output)."""
from ch3lib import *
import math

I44 = [[1, 2, 4, 5], [5, 2, 5, 2], [1, 1, 3, 6], [2, 4, 6, 7]]
W121 = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
LAP = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
a07 = math.exp(-1 / (2 * 0.49))
G07 = [[a07 * a07, a07, a07 * a07], [a07, 1, a07], [a07 * a07, a07, a07 * a07]]


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
    H.append(set_solution(card('qz1'), walk([
        ('Build the kernel', 'σ = 0.7, c = 1: edge = e<sup>−1/(2·0.49)</sup> = 0.3604, corner = 0.3604² = 0.1299, centre 1. Sum = 1 + 4(0.3604) + 4(0.1299) = <b>2.9612</b>.', None),
        ('Build the window with replicate padding', 'g(0, 3) is the top-right pixel: the row above (−1) copies row 0, the column to the right (4) copies column 3. Window = [1 3.2 3.2; 1 3.2 3.2; π 2 2].', fig),
        ('Add the products, then normalise', f'Sum of products = {fmt(round(tot, 4))}; divide by the kernel sum: {fmt(round(tot, 4))} / 2.9612 = <b>2.6345</b>.', None),
    ]) + '<div class="ansbig">g(0, 3) = 2.6345.</div>'))

    for cid, A, B, pa, pb in [('m23q2', W121, LAP, 'zero', 'replicate'), ('m24q2', W121, LAP, 'replicate', 'zero')]:
        fa, ta = window_fig(I44, 0, 0, A, pa, label_kernel='weights 1 2 1 / 2 4 2 / 1 2 1')
        fb, tb = window_fig(I44, 0, 0, B, pb, label_kernel='Laplacian')
        ga = filt(I44, A, pa) / 16; gb = filt(I44, B, pb)
        H.append(set_solution(card(cid), walk([
            (f'(a) Weighted mean, {pa} padding — corner pixel (0, 0)', f'Sum of products = {fmt(ta)} → ÷16 = <b>{fmt(round(ta / 16, 4))}</b>. ' + ('Zero padding: the five outside weights multiply 0.' if pa == 'zero' else 'Replicate: the outside cells copy the edge pixels.'), fa),
            ('(a) the whole image', 'Same at all 16 pixels (calculator: T·F·Tᵀ ÷ 16 in one go, recipe C).', grid_out(ga, 'weighted mean')),
            (f'(b) Laplacian, {pb} padding — corner pixel (0, 0)', f'Neighbours up + down + left + right − 4 × centre = <b>{fmt(tb)}</b>.', fb),
            ('(b) the whole image', 'Positive = the pixel is darker than its neighbours, negative = brighter.', grid_out(gb, 'Laplacian', d=0)),
        ]) + '<div class="ansbig">The two 4×4 outputs in steps 2 and 4.</div>'))

    o = ANS['m2324_2']; blk = [[15, 7, 0], [7, 15, 7], [0, 7, 15]]
    F2 = [[.01, .1, .01], [.1, .56, .1], [.01, .1, .01]]
    f1, t1 = window_fig(blk, 1, 1, LAP, 'zero', label_kernel='Filter-1')
    f2, t2 = window_fig(blk, 0, 1, F2, 'zero', label_kernel='Filter-2')
    H.append(set_solution(card('o23q2'), walk([
        ('Identify the filters', 'Filter-1 = the 4-neighbour Laplacian (weights add to 0 → highpass, finds detail). Filter-2 = a Gaussian-like weighted average (weights add to 1 → lowpass, smooths).', None),
        ('Filter-1 at the centre', f'7 + 7 + 7 + 7 − 4·15 = <b>{fmt(t1)}</b>. (The zeros around the block act as zero padding.)', f1),
        ('Filter-2 at an edge pixel (0, 1)', f'Sum of products = <b>{fmt(round(t2, 4))}</b> (the official key prints 6.99: it dropped the 0.01 × 7 term).', f2),
        ('Both outputs', '', figs(grid_out(o['f1'], 'Filter-1', d=0), grid_out(o['f2'], 'Filter-2', d=2, cell=56))),
    ]) + '<div class="ansbig">Filter-1: [−46 2 14; 2 −32 2; 14 2 −46]. Filter-2: [9.95 7.06 1.55; 7.06 11.5 7.06; 1.55 7.06 9.95].</div>'))

    e25 = [[1, 2, 3, 2], [4, 2, 5, 1], [1, 2, 6, 3], [2, 6, 4, 7]]
    fbx, tbx = window_fig(e25, 0, 0, [[1, 1, 1]] * 3, 'replicate', label_kernel='box (÷ 9)')
    H.append(set_solution(card('d25q2b'), walk([
        ('Corner pixel with replicate padding', f'Sum = {fmt(tbx)} → ÷9 = {fmt(round(tbx / 9, 4))} → <b>2</b>.', fbx),
        ('All pixels, rounded', '', figs(grid_out(filt(e25, [[1, 1, 1]] * 3, 'replicate') / 9, 'exact averages', d=2, cell=52), gsvg(ANS['e25_2b']['r'], {(i, j): 'hl' for i in range(4) for j in range(4)}, cell=44, idx=False, label='rounded'))),
    ]) + '<div class="ansbig">[2 3 2 2; 2 3 3 3; 3 4 4 4; 3 4 5 5].</div>'))

    q = [[4, 2, 3, 2], [1, 1, 2, 3], [1, 3, 2, 3], [2, 2, 3, 1]]
    L2 = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
    fq1, tq1 = window_fig(q, 0, 0, W121, 'zero', label_kernel='weights (÷ 16)')
    fq2, tq2 = window_fig(q, 0, 0, L2, 'zero', label_kernel='Filter-ii')
    H.append(set_solution(card('q21b1'), walk([
        ('(i) Weighted average at (0, 0)', f'Sum = {fmt(tq1)} → ÷16 = {fmt(tq1 / 16)} → nearest integer <b>1</b>. Same at the other diagonal pixels: 1.875 → 2, 2.3125 → 2, 1.125 → 1.', fq1),
        ('(ii) Laplacian (centre +4) at (0, 0)', f'4·4 − (2 + 1) = <b>{fmt(tq2)}</b> (zero padding: up and left are 0). The official key prints 16 — it forgot to subtract the two neighbours. Other diagonal pixels: −4, −3, −2.', fq2),
    ]) + '<div class="ansbig">(i) 1, 2, 2, 1. (ii) 13, −4, −3, −2 (if the output must be 3-bit, clip: 7, 0, 0, 0).</div>'))

    H.append(set_solution(card('m23q6'), walk([
        ('Where does blurring change anything?', 'A 3×3 average of a region that is all black stays 0, all white stays 255. Only pixels whose 3×3 window <b>straddles a black/white boundary</b> get an in-between value: 3 white of 9 → 255·3/9 = 85; 6 white of 9 → 170; at a corner where four blocks meet, 4 or 5 white of 9 → 113.3 or 141.7.', None),
        ('Count the boundaries', 'The half-and-half image has one boundary line. The checkerboard has 3 vertical + 3 horizontal boundary lines and 9 points where four blocks meet. Far more boundary → far more grey pixels.', None),
        ('So the histograms differ', 'Before blurring both histograms are just “half 0, half 255”. After blurring the checkerboard has many more pixels at 85 and 170, and some at 113.3 and 141.7 that the other image does not have at all.', None),
    ]) + '<div class="ansbig">(a) No — blurring creates greys only along boundaries, and the checkerboard has much more boundary. (b) See the counts in the original answer box above (filter-where-the-window-fits or border-unchanged reading).</div>'))
    for cid in ['sl-gauss', 'dr-six', 'tb3-27', 'tb3-28', 'tb3-35', 'dr-med', 'tb3-29']: H.append(card(cid))
    H.append('</section>')
    return '\n'.join(H)
