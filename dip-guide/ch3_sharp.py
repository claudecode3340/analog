"""Chapter 3.6–3.8 rebuilt: sharpening — derivatives, Laplacian, unsharp masking, gradients — each with a plain-words
picture and numbers; the sharpening past papers as step-by-step walks."""
from ch3lib import *
import math
from ch3_filt import mdef, sep_lines, MAT_APP, _q

LAP4 = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
SOBX = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
SOBY = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
WIN = [[2, 3, 4], [3, 9, 5], [4, 5, 6]]


def all_cls(n, m, c):
    return {(i, j): c for i in range(n) for j in range(m)}


def profile_fig():
    f = ANS['fig344']['f']; n = len(f)
    d1 = [f[x + 1] - f[x] for x in range(n - 1)] + ['']
    d2 = [''] + [f[x + 1] - 2 * f[x] + f[x - 1] for x in range(1, n - 1)] + ['']
    cls = {}
    for j in range(n):
        for i, row in ((1, d1), (2, d2)):
            v = row[j]
            if v == '': cls[(i, j)] = 'out'
            elif v > 0: cls[(i, j)] = 'c1'
            elif v < 0: cls[(i, j)] = 'nd'
    # line plot of the profile, same column spacing as the grid below
    cell = 40; W = n * cell + 30; H = 130
    o = [f'<svg class="gsvg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" class="a-bg"/>']
    pts = ' '.join(f'{30 + j * cell + cell / 2:.0f},{H - 14 - v * 17:.0f}' for j, v in enumerate(f))
    o.append(f'<polyline points="{pts}" fill="none" stroke="#60a5fa" stroke-width="3"/>')
    for j, v in enumerate(f):
        o.append(f'<circle cx="{30 + j * cell + cell / 2:.0f}" cy="{H - 14 - v * 17:.0f}" r="4" fill="#60a5fa"/>')
    for lab, j in (('ramp', 5), ('flat', 11), ('step', 13.5)):
        o.append(f'<text x="{30 + j * cell + cell / 2:.0f}" y="16" class="a-lab" text-anchor="middle">{lab}</text>')
    o.append('</svg>')
    plot = f'<figure class="gfig">{"".join(o)}<figcaption>the intensity along one row of an image</figcaption></figure>'
    grid = gsvg([f, d1, d2], cls, cell=40, idx=False,
                label='row 1 = f, row 2 = 1st difference f(x+1) − f(x), row 3 = 2nd difference f(x+1) − 2f(x) + f(x−1). Green = positive, red = negative.')
    return f'<div style="display:flex;flex-direction:column;gap:10px;align-items:flex-start">{plot}{grid}</div>'


def unsharp_1d():
    f = [2, 2, 2, 2, 8, 8, 8, 8]
    fp = [f[0]] + f + [f[-1]]
    b = [round(sum(fp[k:k + 3]) / 3, 2) for k in range(len(f))]
    m = [round(f[k] - b[k], 2) for k in range(len(f))]
    g = [round(f[k] + m[k], 2) for k in range(len(f))]
    cls = {}
    for j in range(len(f)):
        if m[j] > 0: cls[(2, j)] = 'c1'
        if m[j] < 0: cls[(2, j)] = 'nd'
        if g[j] != f[j]: cls[(3, j)] = 'hl'
    return gsvg([[fmt(v) for v in r] for r in (f, b, m, g)], cls, cell=48, idx=False,
                label='rows: f (an edge 2 → 8), blur f̄ (3-point average), mask = f − f̄ (green +, red −), result g = f + mask. Yellow = overshoot that makes the edge look crisper.')


def section(card):
    H = ['''<section class="topic" id="ch3-sharp">
  <div class="eyebrow">Chapter 3.6–3.8 · Lecture 11</div>
  <h2>Sharpening filters: finding and boosting edges</h2>
  <div class="meta"><span class="chip ">TB 3.6–3.8</span><span class="chip ">slides pp. 33–41</span><span class="chip hot">Mid-sem 2019 Q4 · End-sem 2023 Q4 · Laplacian in every Q2</span></div>
  <p class="lede">Smoothing <b>averages</b> neighbours; sharpening takes <b>differences</b> between neighbours. A difference is 0 where the image is flat and large where it changes — at edges, fine detail and noise. So difference kernels <b>find</b> edges, and adding that edge picture back onto the image makes edges look crisper. Every kernel here has weights that <b>add up to 0</b> (that is why flat areas give 0). Exam questions: build a sharpening kernel, apply a Laplacian or Sobel to a small image, or explain unsharp masking.</p>''']

    H.append(lesson('Derivatives on pixels: just subtract neighbours',
        'On a grid, “derivative” means: next pixel minus this pixel. The second derivative is the change of that change. Read the picture: the 1st difference is non-zero along the whole ramp (thick edge); the 2nd difference fires only where the ramp starts and stops, and at a step it gives a +5 then −5 pair (a <b>zero crossing</b> — the sign flips exactly at the edge).',
        '<div class="formula">\\(\\text{1st: } f(x+1)-f(x)\\qquad \\text{2nd: } f(x+1)-2f(x)+f(x-1)\\)<span class="say">1st = right neighbour minus me. 2nd = right neighbour + left neighbour − 2 × me.</span></div>'
        + profile_fig() +
        '<div class="cols"><div><p><b>1st derivative</b> → thick edges (the whole ramp lights up). Used by the <b>gradient</b> (Sobel) for edge detection.</p></div>'
        '<div><p><b>2nd derivative</b> → thin, double edges and fine detail, but also stronger reaction to noise. Used by the <b>Laplacian</b> for sharpening.</p></div></div>',
        use='Slide p. 34 profile (card “First and second differences along a profile” below); theory questions “compare 1st and 2nd derivatives”.', tag='1'))

    fa, ta = window_fig(WIN, 1, 1, LAP4, label_kernel='Laplacian (centre −4)')
    H.append(lesson('The Laplacian and Laplacian sharpening',
        'The Laplacian adds the 2nd difference down the column and along the row: up + down + left + right − 4 × centre. Result: 0 in flat areas; strongly <b>negative</b> on a bright dot or the bright side of an edge, <b>positive</b> on the dark side. Subtracting it from the image pushes bright sides brighter and dark sides darker → sharper edges.',
        '<div class="formula">\\(\\nabla^2 f=f(x{+}1,y)+f(x{-}1,y)+f(x,y{+}1)+f(x,y{-}1)-4f(x,y)\\)<span class="say">“the 4 neighbours minus 4 times me”. Diagonal version: all 8 neighbours minus 8 times me.</span></div>'
        '<p><b>Example.</b> Window [2 3 4; 3 <b>9</b> 5; 4 5 6]: ∇²f = 3 + 5 + 3 + 5 − 4·9 = <b>−20</b> (the centre is brighter than its neighbours). Sharpened: g = f − ∇²f = 9 − (−20) = <b>29</b> — the bright detail gets brighter.</p>'
        + fa +
        '<div class="cols"><div>'
        '<p><b>The four kernels you will see:</b></p>'
        + figs(gsvg(LAP4, all_cls(3, 3, 'n4'), cell=40, idx=False, label='centre −4'),
               gsvg([[1, 1, 1], [1, -8, 1], [1, 1, 1]], all_cls(3, 3, 'n4'), cell=40, idx=False, label='centre −8 (with diagonals)'),
               gsvg([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], all_cls(3, 3, 'n8'), cell=40, idx=False, label='centre +4'),
               gsvg([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], all_cls(3, 3, 'n8'), cell=40, idx=False, label='centre +8')) +
        '<div class="trap"><b>The sign rule.</b> Centre <b>negative</b> (−4, −8) → <b>subtract</b>: g = f − ∇²f. Centre <b>positive</b> (+4, +8) → <b>add</b>: g = f + ∇²f. Either way the bright side must get brighter. Folded into one kernel: [0 −1 0; −1 <b>5</b> −1; 0 −1 0] or [−1 −1 −1; −1 <b>9</b> −1; −1 −1 −1] (the identity’s 1 plus 4 or 8 in the centre).</div>'
        '</div><div>' + figs(img('moon_blur', 150, 'blurry moon'), img('moon_lap4', 150, 'its Laplacian (edges only)'), img('moon_sharp4', 150, 'f − 3∇²f (centre −4)'), img('moon_sharp8', 150, 'f − 3∇²f (centre −8): sharper')) + '</div></div>',
        use='Mid-sem 2019 Q4, every Q2 “filter-ii”, Quiz 2021 Laplacian, textbook 3.40.', tag='2'))

    H.append(lesson('Unsharp masking and highboost: image − blur = edges',
        'Blur the image; what the blur removed (image − blur) is exactly the edges and fine detail — the “mask”. Add the mask back on top of the original and edges stand out. c = 1 is unsharp masking; c &gt; 1 is highboost (even stronger).',
        '<div class="formula">\\(g_{mask}=f-\\bar f,\\qquad g=f+c\\cdot g_{mask}\\)<span class="say">f̄ = the blurred image. Mask = original − blurred. Result = original + c × mask.</span></div>'
        '<div class="cols"><div><p><b>One edge, step by step.</b> Look at the yellow cells: just before the edge the result dips below 2 and just after it jumps above 8. That overshoot is what the eye reads as “sharper”.</p>'
        + unsharp_1d() +
        '<p><b>Example at one pixel.</b> Window [2 3 4; 3 9 5; 4 5 6] with a 3×3 box blur: f̄ = 41/9 = 4.556, mask = 9 − 4.556 = 4.444, unsharp (c = 1) = 13.444, highboost (c = 3) = 22.333.</p>'
        '<p><b>As one kernel</b> (3×3 box blur): g = f + c(f − f̄) = (1 + c)·f − c·f̄ → centre 1 + c − c/9, all other entries −c/9. c = 1: centre 17/9, others −1/9 = ¹⁄₉[−1 −1 −1; −1 17 −1; −1 −1 −1].</p>'
        '<p><b>Link to the Laplacian</b> (textbook 3.42): f − ∇²f with the −8 kernel = f + 9(f − f̄) = highboost with c = 9. Laplacian sharpening is unsharp masking in disguise.</p></div>'
        '<div>' + figs(img('page', 230, 'original text'), img('page_blur', 230, 'blurred f̄'), img('page_mask', 230, 'mask f − f̄'), img('page_unsharp', 230, 'unsharp (c = 1)'), img('page_highboost', 230, 'highboost (c = 4.5)')) + '</div></div>',
        use='Textbook 3.41, 3.42; theory “explain unsharp masking”.', tag='3'))

    z = ANS['sobel_patch']
    H.append(lesson('The gradient: Roberts and Sobel (edge detection)',
        'The gradient measures how fast the image changes in each direction: g<sub>x</sub> = change going down the rows, g<sub>y</sub> = change going across the columns. Its size M is the edge strength — big on edges, 0 on flat areas. Sobel takes a difference in one direction and a 1-2-1 smoothing in the other, so noise bothers it less.',
        '<div class="formula">\\(M=\\sqrt{g_x^2+g_y^2}\\;\\approx\\;|g_x|+|g_y|\\)<span class="say">edge strength = length of the arrow (g<sub>x</sub>, g<sub>y</sub>). The exam often accepts the cheaper |g<sub>x</sub>| + |g<sub>y</sub>|.</span></div>'
        '<div class="cols"><div>'
        + figs(gsvg(SOBX, all_cls(3, 3, 'n4'), cell=44, idx=False, label='Sobel g<sub>x</sub>: bottom row − top row (fires on horizontal edges)'),
               gsvg(SOBY, all_cls(3, 3, 'n8'), cell=44, idx=False, label='Sobel g<sub>y</sub>: right column − left column (fires on vertical edges)'),
               gsvg(z['z'], {}, cell=44, idx=False, label='example window z')) +
        f'<p><b>Example</b> on z = [1 2 3; 4 5 6; 7 8 9]: g<sub>x</sub> = (7 + 2·8 + 9) − (1 + 2·2 + 3) = 32 − 8 = <b>{z["gx"]}</b>; g<sub>y</sub> = (3 + 2·6 + 9) − (1 + 2·4 + 7) = 24 − 16 = <b>{z["gy"]}</b>; M = √(24² + 8²) = <b>{z["M"]:.2f}</b> ≈ |24| + |8| = {z["M1"]}.</p>'
        '<p><b>Roberts</b> (2×2, diagonal differences): g<sub>x</sub> = z<sub>9</sub> − z<sub>5</sub>, g<sub>y</sub> = z<sub>8</sub> − z<sub>6</sub> — kernels [−1 0; 0 1] and [0 −1; 1 0]. Tiny, but very sensitive to noise and has no centre pixel.</p>'
        '<div class="trap"><b>Which is x?</b> In this course x = row (down). So g<sub>x</sub> compares the row below with the row above and lights up on <b>horizontal</b> edges. Read the kernel, not the name: rows differ → horizontal edges.</div>'
        '</div><div>' + figs(img('cam', 130, 'image'), img('cam_gx', 130, '|g<sub>x</sub>|: horizontal edges'), img('cam_gy', 130, '|g<sub>y</sub>|: vertical edges'), img('cam_grad', 130, 'M: all edges')) + '</div></div>',
        use='End-sem 2023 Q4 (Sobel on a square), practice card below, theory “why Sobel uses weight 2”.', tag='4'))

    H.append(lesson('Highpass, bandreject, bandpass — built from a lowpass',
        'A lowpass (smoothing) kernel keeps slow changes. The identity kernel δ (a single 1 in the centre) keeps everything. So “everything minus the slow part” = the fast part: <b>highpass = δ − lowpass</b>.',
        '<div class="formula">\\(hp=\\delta-lp,\\qquad br=lp_1+hp_2,\\qquad bp=\\delta-br\\)<span class="say">bandreject = keep the lows (lp₁) plus the highs (hp₂), dropping the middle; bandpass = everything minus bandreject.</span></div>'
        + figs(gsvg([[0, 0, 0], [0, 1, 0], [0, 0, 0]], all_cls(3, 3, 'n4'), cell=44, idx=False, label='δ (keeps everything)'),
               gsvg([['1/9'] * 3] * 3, all_cls(3, 3, 'n8'), cell=44, idx=False, label='box lowpass'),
               gsvg([['−1/9', '−1/9', '−1/9'], ['−1/9', '8/9', '−1/9'], ['−1/9', '−1/9', '−1/9']], all_cls(3, 3, 'c2'), cell=52, idx=False, label='δ − box = highpass (a scaled Laplacian, centre +8)')),
        use='Textbook 3.7 theory; “design a highpass kernel from a lowpass one”.', tag='5'))

    H.append('<div class="lab" data-lab="freq" data-init=\'{"w": [[0, 1, 0], [1, -4, 1], [0, 1, 0]], "scale": "1", "title": "What a kernel does to frequencies (try the Laplacian, the box, Sobel)"}\'></div>')

    # ── questions ──
    H.append('<h3 id="ch3-sharp-q">Questions on sharpening</h3>')
    D = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    H.append(set_solution(card('s19q4'), walk([
        ('Write each part as a kernel', 'The image itself is “filter with δ” (a 1 in the centre, 0 elsewhere — it copies every pixel). The Laplacian is “filter with L”.',
         figs(gsvg(D, all_cls(3, 3, 'n4'), cell=44, idx=False, label='δ: f = δ ★ f'), gsvg(LAP4, all_cls(3, 3, 'n8'), cell=44, idx=False, label='L: ∇²f = L ★ f'))),
        ('Filtering is linear, so kernels add', 'g = δ★f + c·(L★f) = (δ + c·L)★f. So K = δ + c·L: multiply every entry of L by c, then add 1 to the centre.',
         gsvg([[0, 'c', 0], ['c', '1 − 4c', 'c'], [0, 'c', 0]], all_cls(3, 3, 'hl'), cell=60, idx=False, label='K = δ + cL')),
        ('Plug in the sharpening value', 'With the −4 Laplacian, sharpening needs g = f − ∇²f, i.e. c = −1: centre 1 − 4(−1) = 5, others −1. (8-neighbour Laplacian: centre 1 − 8c, all others c; c = −1 gives centre 9.)',
         gsvg([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], all_cls(3, 3, 'c2'), cell=44, idx=False, label='c = −1')),
    ]) + '<div class="ansbig">K = [0 c 0; c 1−4c c; 0 c 0]. For sharpening (c = −1): [0 −1 0; −1 5 −1; 0 −1 0].</div>'))

    e = ANS['e23_4']; im = e['img']; g = e['g']
    sq = {(i, j): 'in' for i in range(10) for j in range(10) if im[i][j]}
    fw, tw = window_fig(im, 2, 4, SOBX, label_kernel='Sobel H<sub>y</sub> (as printed)')
    fc, tc = window_fig(im, 2, 2, SOBX, label_kernel='Sobel H<sub>y</sub>')
    wA = pad(im, 1, 'zero')[2:5, 4:7]; wB = pad(im, 1, 'zero')[2:5, 2:5]
    assert (wA * np.array(SOBX)).sum() == tw and (wB * np.array(SOBX)).sum() == tc
    gc = {(i, j): ('c1' if g[i][j] > 0 else 'nd') for i in range(10) for j in range(10) if g[i][j]}
    H.append(set_solution(card('e23q4'), walk([
        ('Picture the image and read the kernel', 'The white 4×4 square sits in rows 3–6, columns 3–6 (0-based). H<sub>y</sub> = (row below, weights 1 2 1) − (row above, weights 1 2 1). So it fires only where the row below differs from the row above: on the <b>top and bottom</b> edges of the square. Left and right edges give 0.',
         gsvg([[int(v) for v in r] for r in im], sq, cell=34, idx=True, label='10×10 input, square = 1')),
        ('One pixel just above the top edge: (2, 4)', f'Row above (row 1) is all 0. Row below (row 3) has 1 1 1 under the window. Sum = 1·1 + 2·1 + 1·1 = <b>{fmt(tw)}</b>. H<sub>y</sub> = (−1, 0, 1)ᵀ × (1, 2, 1), so the calculator does one pixel as row × window × column.', fw,
         MAT_APP + sep_lines([-1, 0, 1], wA, [1, 2, 1])[0]),
        ('A pixel at the corner: (2, 2)', f'Only the right-most cell of the row below is inside the square: 1 × 1 = <b>{fmt(tc)}</b>. Moving right along row 2 the window covers 1, then 2, then 3 cells of the square → 1, 3, 4, 4, 3, 1.', fc,
         mdef('MatA', wB, 'only the window changes; MatB and MatC stay')
         + cl(K('MatB', '×', 'MatA', '×', 'MatC', 'EXE'), 'the response at (2, 2)', lcdmat('MatAns', [[int(tc)]]))),
        ('Row 3 too', 'At row 3 the row above (2) is 0 and the row below (4) is inside the square → the same 1 3 4 4 3 1. Rows 4–5: above and below are both inside → 0. Rows 6–7 mirror the top edge with the opposite sign (row below is 0, row above is 1).', None),
        ('The whole output', 'Green = positive (dark above, bright below), red = negative. Every row in the interior of the square and everything far away is 0. If you use convolution instead of correlation the kernel flips and all signs swap — magnitudes stay the same.',
         gsvg([[int(v) for v in r] for r in g], gc, cell=38, idx=True, label='Sobel H<sub>y</sub> output (correlation, zero padding)')),
    ]) + '<div class="ansbig">Rows 2 and 3: 0 0 1 3 4 4 3 1 0 0. Rows 6 and 7: 0 0 −1 −3 −4 −4 −3 −1 0 0. All other rows 0.</div>'))

    H.append(set_solution(card('tb3-41'), walk([
        ('Write unsharp masking as kernels', 'g = f + (f − f̄) = 2·f − f̄. “2·f” is the kernel 2δ (a 2 in the centre). “f̄” is the box kernel, 1/9 everywhere.', None),
        ('Subtract the kernels entry by entry', 'Centre: 2 − 1/9 = <b>17/9</b>. Every other entry: 0 − 1/9 = <b>−1/9</b>. Check: the weights add to 17/9 − 8/9 = 1, so flat areas keep their brightness.',
         figs(gsvg([[0, 0, 0], [0, 2, 0], [0, 0, 0]], all_cls(3, 3, 'n4'), cell=44, idx=False, label='2δ'),
              gsvg([['1/9'] * 3] * 3, all_cls(3, 3, 'n8'), cell=44, idx=False, label='box'),
              gsvg([['−1/9', '−1/9', '−1/9'], ['−1/9', '17/9', '−1/9'], ['−1/9', '−1/9', '−1/9']], all_cls(3, 3, 'hl'), cell=52, idx=False, label='2δ − box')),
         cl(K('2', '−', '1', '÷', '9', 'EXE'), 'centre weight; the calculator shows the fraction 17/9')
         + cl(K('17', '÷', '9', '−', '8', '÷', '9', 'EXE'), 'check: all nine weights add to 1')),
        ('Highboost in general', 'g = f + c(f − f̄) → centre 1 + c − c/9, others −c/9.', None),
    ]) + '<div class="ansbig">¹⁄₉ [−1 −1 −1; −1 17 −1; −1 −1 −1].</div>'))

    H.append('<h3>More questions on derivatives and sharpening</h3>')
    for cid in ['sl-deriv', 'tb3-38', 'tb3-40', 'tb3-42', 'dr-unsharp']: H.append(card(cid))
    Z = [[1, 2, 3], [4, 5, 6], [9, 9, 9]]
    cgx, gx = sep_lines([-1, 0, 1], Z, [1, 2, 1]); cgy, gy = sep_lines([1, 2, 1], Z, [-1, 0, 1])
    assert (gx, gy) == (28, 6)
    H.append(set_solution(card('dr-sobel'), walk([
        ('g<sub>x</sub>: bottom row − top row, weights 1 2 1', f'(9 + 2·9 + 9) − (1 + 2·2 + 3) = 36 − 8 = <b>{fmt(gx)}</b>. The kernel is (−1, 0, 1)ᵀ × (1, 2, 1): row weights −1, 0, 1 (top, middle, bottom), column weights 1, 2, 1.', None,
         MAT_APP + cgx),
        ('g<sub>y</sub>: right column − left column, weights 1 2 1', f'(3 + 2·6 + 9) − (1 + 2·4 + 9) = 24 − 18 = <b>{fmt(gy)}</b>. Kernel (1, 2, 1)ᵀ × (−1, 0, 1): swap the roles of the row and the column.', None,
         mdef('MatB', [[1, 2, 1]], 'new row weights (1 2 1)') + mdef('MatC', [[-1], [0], [1]], 'new column weights (−1 0 1)')
         + cl(K('MatB', '×', 'MatA', '×', 'MatC', 'EXE'), 'MatA (the window) is unchanged', lcdmat('MatAns', [[int(gy)]]))),
        ('Magnitude and the cheap approximation', f'M = √(28² + 6²) = √820 = <b>{math.hypot(gx, gy):.3f}</b>; |g<sub>x</sub>| + |g<sub>y</sub>| = <b>{int(abs(gx) + abs(gy))}</b> (bigger than M — it overestimates diagonal-ish gradients).', None,
         cl(K('CATALOG', '>Angle/Coord/Sexa', '>Rect to Polar'), 'types Pol( — enter 28, 6 (comma = SHIFT )) and EXE: r is the magnitude M')
         + cl(K('√', '28', 'x²', '+', '6', 'x²', ')', 'EXE'), f'or directly: {math.hypot(gx, gy):.6f}')),
        ('Roberts cross-gradients', 'Number the window z₁ … z₉ row by row, so z₅ = 5 is the centre. Roberts: z₉ − z₅ = 9 − 5 = <b>4</b> and z₈ − z₆ = 9 − 6 = <b>3</b> (diagonal differences — by hand).', None),
    ]) + '<div class="ansbig">g<sub>x</sub> = 28, g<sub>y</sub> = 6, M = 28.636, |g<sub>x</sub>| + |g<sub>y</sub>| = 34; Roberts 4 and 3.</div>'))
    H.append('</section>')
    return '\n'.join(H)
