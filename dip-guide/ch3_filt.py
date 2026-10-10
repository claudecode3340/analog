"""Chapter 3.4 rebuilt: how spatial filtering works — the sliding window, correlation vs convolution, padding, separable
kernels — with window/kernel/product pictures; the filtering past papers as step-by-step walks."""
from ch3lib import *

I44 = [[1, 2, 4, 5], [5, 2, 5, 2], [1, 1, 3, 6], [2, 4, 6, 7]]
W121 = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]


def rounded3(g):
    return [[int(min(7, max(0, np.floor(v + 0.5)))) for v in r] for r in g]


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
    H.append(set_solution(card('o24q1'), walk([
        ('Work with 14·h, divide at the end', 'h = ¹⁄₁₄ × [1 2 1; 1 2 2; 2 1 3]. Use the whole numbers and divide every sum by 14.', None),
        ('Correlation at the centre (1, 1)', f'The window is the whole image. Sum of products = {fmt(ta)} → ÷14 = {fmt(round(ta / 14, 4))} → rounded <b>2</b>.', fa),
        ('Convolution at the centre: turn h first', f'Rotated kernel [3 1 2; 2 2 1; 1 2 1]. Sum = {fmt(tb)} → ÷14 = {fmt(round(tb / 14, 4))} → <b>2</b>.', fb),
        ('All nine pixels (zero padding)', 'Repeat at every pixel (corners use zeros outside). Sums ÷ 14, then round to the nearest integer in 0 … 7 (halves round up: 21/14 = 1.5 → 2):', figs(gsvg(m['corr14'], {}, cell=40, idx=False, label='correlation × 14'), gsvg(m['corr_q'], {(i, j): 'hl' for i in range(3) for j in range(3)}, cell=40, idx=False, label='correlation, 3-bit'), gsvg(m['conv14'], {}, cell=40, idx=False, label='convolution × 14'), gsvg(m['conv_q'], {(i, j): 'hl' for i in range(3) for j in range(3)}, cell=40, idx=False, label='convolution, 3-bit'))),
        ('Compare', 'The two results differ because h is not symmetric under a half-turn. For a symmetric kernel they would be identical.', None),
    ]) + '<div class="ansbig">Correlation [2 2 1; 2 2 1; 1 2 1], convolution [1 1 1; 1 2 2; 1 2 2] (3-bit, rounded); they differ because h is not 180°-symmetric.</div>'))

    f318 = np.zeros((5, 5)); f318[1:4, 2] = 1
    full = ANS['p318']['conv_full']
    fc, tc = window_fig(f318.tolist(), 1, 2, W121, 'zero')
    H.append(set_solution(card('tb3-18'), walk([
        ('Set up', 'f is a vertical line of three 1s. “Minimum zero padding” for the full result: pad by 2 on every side so every kernel entry meets every pixel → output 7×7.', None),
        ('One position (row 2, column 3, counted from 1 = (1, 2) from 0)', f'Window × kernel (the kernel is symmetric, so convolution = correlation): the window contains two of the line’s 1s (under the centre weight 4 and the weight 2 below it); sum = <b>{fmt(tc)}</b>.', fc),
        ('Whole result', 'Each 1 of the line drops a copy of the kernel centred on itself; the three copies overlap and add up.', gsvg([[int(v) for v in r] for r in full], {(i, j): 'hl' for i in range(7) for j in range(7) if full[i][j]}, cell=38, idx=False, label='full convolution (7×7)')),
    ]) + '<div class="ansbig">Columns 2–4 of the 7×7 result: rows 1–5 = (1 2 1), (3 6 3), (4 8 4), (3 6 3), (1 2 1); everything else 0. Correlation is the same (w is symmetric).</div>'))
    for cid in ['tb3-20', 'tb3-22', 'tb3-44', 'd25q2c']: H.append(card(cid))
    f18 = [[3, 7, 6, 2, 0], [2, 4, 6, 1, 1], [4, 7, 2, 5, 4], [3, 0, 6, 2, 1], [5, 7, 5, 1, 2]]
    box = [[1, 1, 1]] * 3
    fz, tz = window_fig(f18, 0, 0, box, 'zero', label_kernel='box (÷ 9)')
    fr, tr = window_fig(f18, 0, 0, box, 'replicate', label_kernel='box (÷ 9)')
    H.append(set_solution(card('s18q2'), walk([
        ('Border methods', '(1) zero padding, (2) replicate the edge pixels, (3) mirror the image, (4) leave the border pixels unfiltered or crop to where the window fits, (5) treat the image as periodic. Name the one you use.', None),
        ('Corner pixel with zero padding', f'Window around (0, 0); five of the nine values are padding zeros. Sum = {fmt(tz)} → ÷9 = {fmt(round(tz / 9, 4))} → <b>2</b>.', fz),
        ('Same corner with replicate padding', f'The padding copies the edge, so the corner pixel 3 counts four times. Sum = {fmt(tr)} → ÷9 = {fmt(round(tr / 9, 4))} → <b>4</b>.', fr),
        ('Whole image', 'Repeat for all 25 pixels (calculator: Spreadsheet recipe J does all of them).', figs(gsvg(ANS['m18_2_zero']['r'], {}, cell=36, idx=False, label='zero padding, rounded'), gsvg(ANS['m18_2_replicate']['r'], {}, cell=36, idx=False, label='replicate, rounded'))),
    ]) + '<div class="ansbig">Zero padding: rows 2 3 3 2 0 / 3 5 4 3 1 / 2 4 4 3 2 / 3 4 4 3 2 / 2 3 2 2 1. Replicate: 4 5 5 3 1 / 4 5 4 3 2 / 3 4 4 3 2 / 4 4 4 3 2 / 4 5 4 3 2.</div>'))
    for cid in ['sl-1d', 'sl-2d', 'tb3-24', 'dr-sep', 'tb3-31']: H.append(card(cid))
    H.append('</section>')
    return '\n'.join(H)
