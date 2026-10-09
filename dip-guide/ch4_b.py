"""Chapter 4, second half, rebuilt: FFT, the 2-D DFT and its properties, filtering in the frequency domain.
Plain-words lessons with small worked numbers and pictures; past papers as step-by-step walks."""
import math
import numpy as np
from ch3lib import *
from ch4_a import cf, row, rows, old_lab, old_details, W4

ALL = lambda n, m, c: {(i, j): c for i in range(n) for j in range(m)}


def butterfly_svg():
    """4-point decimation-in-time FFT of f = {1, 2, 3, 4}, with every intermediate value."""
    ys = [40, 110, 180, 250]; X0, X1, X2 = 90, 330, 600
    ins = ['f(0) = 1', 'f(2) = 3', 'f(1) = 2', 'f(3) = 4']
    mid = ['G(0) = 4', 'G(1) = −2', 'H(0) = 6', 'H(1) = −2']
    out = ['F(0) = 10', 'F(1) = −2 + 2i', 'F(2) = −2', 'F(3) = −2 − 2i']
    o = [f'<svg class="gsvg" viewBox="0 0 760 300" width="760" height="300"><rect width="760" height="300" class="a-bg"/>']
    L = lambda x1, y1, x2, y2, c='#60a5fa': o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="2.2"/>')
    for a, b in ((0, 1), (2, 3)):
        L(X0 + 50, ys[a], X1 - 70, ys[a]); L(X0 + 50, ys[b], X1 - 70, ys[b]); L(X0 + 50, ys[a], X1 - 70, ys[b]); L(X0 + 50, ys[b], X1 - 70, ys[a])
    for k in (0, 1):
        a, b = k, k + 2
        L(X1 + 70, ys[a], X2 - 80, ys[a], '#f59e0b'); L(X1 + 70, ys[b], X2 - 80, ys[b], '#f59e0b'); L(X1 + 70, ys[a], X2 - 80, ys[b], '#f59e0b'); L(X1 + 70, ys[b], X2 - 80, ys[a], '#f59e0b')
        o.append(f'<text x="{X1}" y="{ys[b] + 24}" text-anchor="middle" class="a-lab">× W{"⁰ = 1" if k == 0 else "¹ = −i"}</text>')
    for i, y in enumerate(ys):
        for x, t in ((X0, ins[i]), (X1, mid[i]), (X2, out[i])):
            o.append(f'<text x="{x}" y="{y + 5}" text-anchor="middle" style="font-size:14px;fill:var(--ink);font-family:var(--font-mono)">{t}</text>')
    for x, t in ((X0, 'inputs, bit-reversed order'), (X1, 'two 2-point DFTs'), (X2, 'butterflies → outputs')):
        o.append(f'<text x="{x}" y="290" text-anchor="middle" class="a-lab">{t}</text>')
    o.append('</svg>')
    return f'<figure class="gfig">{"".join(o)}<figcaption>4-point FFT of f = {{1, 2, 3, 4}}: blue = 2-point DFTs (a + b, a − b), orange = butterflies (top: a + Wb, bottom: a − Wb)</figcaption></figure>'


# ═══════════════════════════ FFT ═══════════════════════════
def fft(card, old):
    H = ['''<section class="topic" id="ch4-fft">
  <div class="eyebrow">Chapter 4.11 (on your slides) · Lecture 15</div>
  <h2>The FFT: the same DFT, much less work</h2>
  <div class="meta"><span class="chip ">slides pp. 39–52</span><span class="chip ">TB 4.11</span><span class="chip hot">flop counts · butterflies · mixed radix</span></div>
  <p class="lede">The FFT gives exactly the same numbers as the DFT; it just reuses work. Split the samples into even and odd positions, do two half-size DFTs, then combine them with “butterflies”. Repeat the split until the DFTs are 2 points long. Exam questions: count the operations, draw or use a butterfly, and the mixed-radix example from your slides.</p>''']

    cost = [[n, (n - 1) ** 2, n * (n - 1), 2 * (n // 2 - 1) ** 2 + n // 2, 2 * (n // 2) * (n // 2 - 1) + n, n // 2 * int(math.log2(n)), n * int(math.log2(n))] for n in (8, 32, 64, 1024)]
    H.append(lesson('Why bother: the operation count',
        'A direct n-point DFT multiplies every sample by every W: about n² operations. Each level of even/odd splitting halves the work of what is left; after log₂n levels only (n/2)·log₂n multiplications remain.',
        '<div class="formula">\\(\\text{direct: }(n-1)^2\\text{ mult},\\ n(n-1)\\text{ add}\\)<br>\\(\\text{one split: }2\\big(\\tfrac n2-1\\big)^2+\\tfrac n2\\text{ mult},\\ 2\\cdot\\tfrac n2\\big(\\tfrac n2-1\\big)+n\\text{ add}\\)<br>\\(\\text{full radix-2: }\\tfrac n2\\log_2n\\text{ mult},\\ n\\log_2n\\text{ add}\\)<span class="say">your slides’ counting: multiplications by W<sup>0</sup> = 1 are not counted.</span></div>'
        + table(['n', 'direct mult', 'direct add', 'one split mult', 'one split add', 'FFT mult', 'FFT add'], cost) +
        '<p>Check against your slide: n = 32 → 961 / 992 direct, 466 / 512 with one split. At n = 1024 the FFT needs about 200× fewer multiplications.</p>',
        tag='1'))

    H.append(lesson('Decimation in time: even and odd samples, then butterflies',
        'G = DFT of the even samples f(0), f(2), …; H = DFT of the odd samples f(1), f(3), …. Both are half-length. Then every pair of outputs comes from one <b>butterfly</b>: top = G + W·H, bottom = G − W·H.',
        '<div class="formula">\\(F(k)=G(k)+W_n^{k}H(k),\\qquad F\\big(k+\\tfrac n2\\big)=G(k)-W_n^{k}H(k),\\qquad k=0,\\dots,\\tfrac n2-1\\)<span class="say">works because W<sub>n</sub><sup>2</sup> = W<sub>n/2</sub> and W<sub>n</sub><sup>k+n/2</sup> = −W<sub>n</sub><sup>k</sup>.</span></div>'
        '<div class="cols"><div><p><b>Worked: f = {1, 2, 3, 4}, n = 4.</b></p><ol class="how">'
        '<li>Even samples {1, 3} → G = {1 + 3, 1 − 3} = {4, −2}. Odd samples {2, 4} → H = {6, −2}.</li>'
        '<li>k = 0 (W<sup>0</sup> = 1): F(0) = 4 + 6 = <b>10</b>, F(2) = 4 − 6 = <b>−2</b>.</li>'
        '<li>k = 1 (W<sup>1</sup> = −i): W·H(1) = (−i)(−2) = 2i → F(1) = −2 + 2i, F(3) = −2 − 2i.</li></ol>'
        '<p>Same answer as the matrix method in Section 4.4 ✓.</p>'
        '<p><b>Bit-reversed input order.</b> Splitting repeatedly reorders the inputs: write the index in binary and read it backwards.</p>'
        + table(['index', '0', '1', '2', '3', '4', '5', '6', '7'], [['binary', '000', '001', '010', '011', '100', '101', '110', '111'], ['reversed', '000', '100', '010', '110', '001', '101', '011', '111'], ['input order', '0', '4', '2', '6', '1', '5', '3', '7']]) +
        '</div><div>' + butterfly_svg() + '</div></div>'
        '<p><b>Decimation in frequency</b> is the mirror image: split the <i>outputs</i> into even and odd F. First form g(x) = f(x) + f(x + n/2) and h(x) = W<sup>x</sup>[f(x) − f(x + n/2)]; natural-order inputs, bit-reversed outputs. <b>Inverse FFT:</b> use W<sup>−1</sup> instead of W and divide by n.</p>'
        + old_details(old),
        use='Butterfly diagrams on slides pp. 42–46; “compute this 4- or 8-point DFT with the FFT”.', tag='2'))

    H.append(lesson('Mixed radix: n = k × ℓ with any factors',
        'When n is not a power of 2 (like 12 = 4 × 3), arrange the samples in a k × ℓ table, do small DFTs down the columns, fix up with “twiddle factors”, do small DFTs along the rows, and read the answer down the columns.',
        '<ol class="how"><li><b>Fill</b> a k × ℓ matrix S row by row with f.</li><li><b>Columns:</b> k-point DFT of every column.</li>'
        '<li><b>Twiddle:</b> multiply entry (p, q) by W<sub>n</sub><sup>p·q</sup> (0-based p, q).</li><li><b>Rows:</b> ℓ-point DFT of every row.</li>'
        '<li><b>Read column by column:</b> column 0 gives F(0 … k − 1), column 1 gives F(k … 2k − 1), ….</li></ol>'
        '<p>Mnemonic: <b>fill rows → DFT columns → twiddle → DFT rows → read columns.</b> Worked in full on your slide example below.</p>',
        tag='3'))
    H.append(old_lab(old, 'fft'))

    H.append('<h3 id="ch4-fft-q">Questions on the FFT</h3>')
    f = np.array([1, 4, 5, 2, 6, 3, 7, 3, 6, 2, 5, 4.]); S = f.reshape(4, 3)
    F1 = np.fft.fft(S, axis=0); W = np.exp(-2j * np.pi / 12)
    E = np.array([[W ** (p * q) for q in range(3)] for p in range(4)]); F2 = F1 * E; F3 = np.fft.fft(F2, axis=1)
    G = lambda A, lab, c='n4', cell=None: f'<figure class="gfig">' + table(['', 'q = 0', 'q = 1', 'q = 2'], [[f'p = {p}'] + [cf(v, 4) for v in r] for p, r in enumerate(A)]) + f'<figcaption>{lab}</figcaption></figure>'
    H.append(set_solution(card('sl-mr'), walk([
        ('Fill a 4 × 3 table row by row', 'k = 4 rows, ℓ = 3 columns.', rows(S.astype(int).tolist(), ALL(4, 3, 'n8'), 'S')),
        ('4-point DFT of every column', 'Column 0 = (1, 2, 7, 2): sum 12; with (1, −i, −1, i): 1 − 2i − 7 + 2i = −6; alternating: 1 − 2 + 7 − 2 = 4; last = conjugate of the second → −6. Same for the other two columns.', G(F1, 'F̂<sub>1</sub>')),
        ('Twiddle: multiply (p, q) by W<sub>12</sub><sup>pq</sup>', 'Row 0 and column 0 are unchanged (exponent 0). E.g. (1, 1): (1 − i)·W<sub>12</sub><sup>1</sup>.', G(F2, 'F̂<sub>2</sub> = F̂<sub>1</sub> × E', 'c4', 120)),
        ('3-point DFT of every row', 'Row p gives F(p), F(p + 4), F(p + 8).', G(F3, 'rows transformed', 'hl', 100)),
        ('Read down the columns', 'Column 0 → F(0 … 3), column 1 → F(4 … 7), column 2 → F(8 … 11). The result is real and symmetric because f is real and even under circular reversal (f(x) = f(12 − x)).', row([cf(v, 4) for v in F3.T.flatten()], {0: 'hl'}, 'F(0) … F(11)', cell=70)),
    ]) + '<div class="ansbig">F = {48, −5.2679, 0, −4, −6, −8.7321, 12, −8.7321, −6, −4, 0, −5.2679}.</div>'))
    H.append(card('dr-flop'))
    H.append('</section>')
    return '\n'.join(H)


# ═══════════════════════════ 2-D DFT ═══════════════════════════
def twod(card, old):
    H = ['''<section class="topic" id="ch4-2d">
  <div class="eyebrow">Chapter 4.5–4.6 · Lectures 16–17</div>
  <h2>The 2-D DFT and what its properties do to a picture</h2>
  <div class="meta"><span class="chip ">TB 4.5–4.6</span><span class="chip ">slides pp. 53–64</span><span class="chip hot">Quiz-1 Q3 · Oct 2023 Q1 · Oct 2024 Q3 · Dec 2025 Q2(d)</span></div>
  <p class="lede">A 2-D DFT is two 1-D DFTs: one down every column, then one along every row. In matrices that is just F = D<sub>m</sub> f D<sub>n</sub>. Most exam questions are either one coefficient F(u, v) by hand, or “what happens to the image if I do this to its spectrum” — answered with the property table, no calculation.</p>''']

    f2 = np.array([[1, 2], [3, 4]]); D2 = np.array([[1, 1], [1, -1]])
    H.append(lesson('Computing it: F = D<sub>m</sub> · f · D<sub>n</sub>',
        'Left-multiplying by D<sub>m</sub> transforms every column; right-multiplying by D<sub>n</sub> transforms every row. For a single coefficient you only need one row of D<sub>m</sub> and one column of D<sub>n</sub>.',
        '<div class="formula">\\(F(u,v)=\\sum_{x=0}^{m-1}\\sum_{y=0}^{n-1}f(x,y)\\,W_m^{ux}\\,W_n^{vy}\\quad\\Longleftrightarrow\\quad M_F=D_m\\,M_f\\,D_n\\)<span class="say">one entry: F(u, v) = (row u of D<sub>m</sub>) × f × (column v of D<sub>n</sub>). Inverse: f = (1/mn) D<sub>m</sub>* F D<sub>n</sub>*.</span></div>'
        '<div class="cols"><div><p><b>Example.</b> f = [1 2; 3 4], D<sub>2</sub> = [1 1; 1 −1]. D<sub>2</sub>f = [4 6; −2 −2] (column sums and differences); then × D<sub>2</sub> = <b>[10 −2; −4 0]</b> (row sums and differences).</p>'
        '<p>F(0, 0) = 10 = sum of all pixels = mn × average. F(1, 0) = −4: top row minus bottom row (change going down). F(0, 1) = −2: left column minus right column.</p>'
        '<div class="trap"><b>Indices.</b> F(u, v) is 0-based; the matrix entry is M<sub>F</sub>(u + 1, v + 1). Quiz-1 asked for F(1, 1) = M<sub>F</sub>(2, 2), not the corner.</div></div><div>'
        + figs(rows(f2.tolist(), {}, 'f'), rows((D2 @ f2).tolist(), ALL(2, 2, 'n8'), 'D<sub>2</sub> f'), rows((D2 @ f2 @ D2).tolist(), ALL(2, 2, 'hl'), 'F = D<sub>2</sub> f D<sub>2</sub>')) + '</div></div>',
        use='Quiz-1 2026 Q3 (one coefficient of a 3 × 4 image).', tag='1'))

    H.append(lesson('Looking at a spectrum',
        'The spectrum |F| has a huge range (DC is enormous), so it is shown with a log transform. Uncentred, the low frequencies sit in the four corners; centred (rotated by half the size), DC is in the middle and low frequencies cluster around it.',
        figs(img('cam', 150, 'image'), img('f_spec_uncentred', 150, 'log |F|, uncentred: bright corners'), img('f_spec', 150, 'centred: DC in the middle')) +
        '<p><b>Centring</b> = circular shift by ⌊m/2⌋, ⌊n/2⌋. For even sizes this is the same as multiplying the image by the ±1 checkerboard (−1)<sup>x+y</sup> first (Dec 2025 Q2(d)). The bright lines through the centre come from strong straight edges in the image, at right angles to the edges.</p>'
        '<p><b>Spacing:</b> one step in u is Δu = 1/(M ΔT), one over the total width of the image in space. More samples → finer frequency steps.</p>',
        tag='2'))

    H.append(lesson('Properties you see in pictures',
        'Each property is the 1-D one applied in both directions. These pictures are what the exam’s theory parts describe.',
        '<div class="cols"><div>' + table(['do this to the image', 'the spectrum…'], [
            ['add a constant / brighten', 'only F(0, 0) changes (F(0,0) = Σf = mn × average)'],
            ['shift (translate) it', '|F| unchanged; the phase tilts'],
            ['rotate it by θ', '|F| rotates by θ too'],
            ['multiply by (−1)<sup>x+y</sup>', 'shifts by (m/2, n/2): centres it'],
            ['rotate 180°: f(−x, −y)', 'becomes F(−u, −v) = F* for real f'],
            ['convolve with h (circularly)', 'is multiplied by H'],
            ['multiply by h', 'is convolved with H, ÷ mn'],
            ['real image', 'F(u, v) = F*(−u, −v): |F| symmetric about the centre']]) +
        '<p><b>Phase vs magnitude.</b> F = |F|e<sup>jφ</sup>. The magnitude says <i>how much</i> of each wave; the phase says <i>where</i> the waves line up — it carries the shapes. Rebuild from phase only and you still see the man; from magnitude only you see nothing recognisable.</p>'
        '<p><b>Changing the phase (Oct 2024 Q3, TB 4.43–4.45):</b> φ → −φ gives F* → image rotated 180°; φ + π multiplies F by −1 → −f; φ + π/2 multiplies by j → j f.</p></div><div>'
        + figs(img('f_shift_img', 115, 'shifted image'), img('f_shift_spec', 115, 'same |F| as the original'), img('f_rect_rot', 115, 'box rotated 30°'), img('f_rect_rot_spec', 115, 'its spectrum rotated 30°'),
               img('f_phase_only', 115, 'phase only: shapes survive'), img('f_mag_only', 115, 'magnitude only: nothing'), img('f_conj', 115, 'inverse of F*: rotated 180°')) + '</div></div>',
        use='Oct 2024 Q3(ii)–(v), Dec 2025 Q2(d), TB 4.21, 4.36, 4.43–4.45.', tag='3'))
    H.append(old_lab(old, 'dft'))

    H.append('<h3 id="ch4-2d-q">Questions on the 2-D DFT</h3>')
    fq = np.array([[0, 0, 1, 1], [0, 0, 1, 1], [1, 1, 0, 0]])
    c4 = np.array([1, -1j, -1, 1j]); col = fq @ c4
    Wc = np.exp(-2j * np.pi / 3); r3 = np.array([1, Wc, Wc ** 2]); F11 = r3 @ col
    H.append(set_solution(card('qz3'), walk([
        ('Pick one row and one column', 'F(1, 1) = (row u = 1 of D<sub>3</sub>) × M<sub>f</sub> × (column v = 1 of D<sub>4</sub>). Row of D<sub>3</sub>: (1, W, W²) with W = −½ − (√3/2)i. Column of D<sub>4</sub>: (1, −i, −1, i).', None),
        ('Do the 4-point side first (no arithmetic)', 'Each image row times (1, −i, −1, i): row [0 0 1 1] → 0 + 0 − 1 + i = −1 + i; row 1 the same; row [1 1 0 0] → 1 − i.',
         figs(rows(fq.tolist(), {}, 'M<sub>f</sub>'), rows([[cf(v)] for v in col], ALL(3, 1, 'n8'), 'M<sub>f</sub> × column', cell=80))),
        ('Then the 3-point side', 'F(1, 1) = 1·(−1 + i) + W·(−1 + i) + W²·(1 − i) = (−1 + i)(1 + W) + (1 − i)W². Since 1 + W + W² = 0, 1 + W = −W², so F = (−1 + i)(−W²) + (1 − i)W² = 2(1 − i)W².', None),
        ('Magnitude', f'|W²| = 1 and |1 − i| = √2, so |F(1, 1)| = 2√2 = <b>{abs(F11):.4f}</b>. (Explicitly F(1, 1) = {cf(F11)}.)', None),
    ]) + '<div class="ansbig">|F(1, 1)| = 2√2 ≈ 2.8284.</div>'))

    fo = np.array([[0, 0, 0, 0, 0], [0, 15, 7, 0, 0], [0, 7, 15, 7, 0], [0, 0, 7, 15, 0], [0, 0, 0, 0, 0]])
    Gc = np.abs(np.fft.fftshift(np.fft.fft2(fo) / 25))
    H.append(set_solution(card('o23q1'), walk([
        ('Note the printed formula', 'This paper puts 1/MN = 1/25 in front of the forward DFT — use it. DC: F(0, 0) = (15·3 + 7·4)/25 = 73/25 = <b>2.92</b>.', rows(fo.tolist(), {(i, j): 'in' for i in range(5) for j in range(5) if fo[i, j]}, 'f (5 × 5)')),
        ('How to centre an odd size', 'n = 5 is odd, so (−1)<sup>x+y</sup> does not work (it shifts by 2.5). Rotate instead by ⌊5/2⌋ = 2: display row i shows u = (i − 2) mod 5 → rows show u = 3, 4, 0, 1, 2; same for columns.',
         figs(row(['u=3', 'u=4', 'u=0', 'u=1', 'u=2'], {2: 'hl'}, 'display order (rows and columns)', cell=54))),
        ('Compute |F(u, v)| and place it', 'Use |F(u, v)| = |F(5 − u, 5 − v)| (real image) to halve the work. Each value goes to display position ((u + 2) mod 5, (v + 2) mod 5).',
         gsvg([[fmt(round(v, 4)) for v in r] for r in Gc], {**{(i, j): 'hl' for i in range(3) for j in range(5)}, (2, 2): 'c1'}, cell=84, idx=True, label='centred |F|; first three rows asked (yellow), DC in green')),
        ('About the official key', 'The key multiplied by (−1)<sup>x+y</sup> anyway, so its “centre” is 1.877, not the DC value 2.92 — it is sampling between the DFT frequencies. With the slides’ ordering the answer is the table above.', None),
    ]) + '<div class="ansbig">Rows 0–2: [0.0647 0.6508 0.2639 0.6908 0.8939], [0.6508 0.0247 1.7039 2.1461 0.6908], [0.2639 1.7039 2.92 1.7039 0.2639].</div>'))

    fl = [[0, 1, 1, 0, 1], [1, 1, 1, 0, 1], [0, 0, 1, 0, 1], [1, 0, 0, 0, 0], [1, 1, 0, 1, 1]]
    H.append(set_solution(card('o24q3'), walk([
        ('The idea', 'No DFT needs computing. Each change to F is a known change to the image. Translate each one with the property table (lesson 3).', None),
        ('(ii) Conjugate → rotate 180°', 'f*(x, y) ↔ F*(−u, −v). Swap u → −u: F*(u, v) ↔ f*(−x, −y) = f(−x, −y) because f is real. With x, y from −2 to 2 that is the image turned 180° about its centre pixel.',
         figs(rows(fl, {(i, j): 'in' for i in range(5) for j in range(5) if fl[i][j]}, 'f<sub>LSB</sub>'), rows([r[::-1] for r in fl[::-1]], {(i, j): 'in' for i in range(5) for j in range(5) if fl[4 - i][4 - j]}, 'g<sub>1</sub> = f<sub>LSB</sub>(−x, −y)'))),
        ('(iii) Phase + π', 'e<sup>jπ</sup> = −1, so the spectrum is −F<sub>MSB</sub> → the image is <b>−f<sub>MSB</sub></b> (linearity).', None),
        ('(iv) Phase + π/2', 'e<sup>jπ/2</sup> = j → j F<sub>LSB</sub> → <b>j f<sub>LSB</sub></b>: a purely imaginary image with the same magnitude.', None),
        ('(v) DFT then inverse DFT', 'They cancel: you get back what went in, e<sup>−jπ/2</sup>f = <b>−j f</b>.', None),
    ]) + '<div class="ansbig">(ii) f<sub>LSB</sub>(−x, −y), the 180° rotation; (iii) −f<sub>MSB</sub>; (iv) j f<sub>LSB</sub>; (v) −j f.</div>'))

    H.append(set_solution(card('d25q2d'), walk([
        ('Write the checkerboard as a formula', 'It starts with +1 at (0, 0) and flips sign at every step in either direction: (−1)<sup>m+n</sup>. So g(m, n) = (−1)<sup>m+n</sup> f(m, n).', None),
        ('Write (−1) as a wave', '(−1)<sup>m</sup> = e<sup>jπm</sup> = W<sub>M</sub><sup>−m·M/2</sup>: multiplying by a wave of half the sampling rate. The modulation property slides the spectrum by (M/2, N/2).', None),
        ('Result', 'G(u, v) = F(u − M/2, v − N/2) for even M, N — the spectrum is centred.', figs(img('f_spec_uncentred', 120, 'F'), img('f_spec', 120, 'G: shifted by half the size'))),
    ]) + '<div class="ansbig">g = (−1)<sup>m+n</sup> f; G(u, v) = F(u − M/2, v − N/2).</div>'))
    for cid in ['tb4-21', 'tb4-36', 'tb4-44', 'tb4-29', 'tb4-43']: H.append(card(cid))
    H.append('</section>')
    return '\n'.join(H)


# ═══════════════════════════ filtering in frequency ═══════════════════════════
def filt(card, old):
    H = ['''<section class="topic" id="ch4-filt">
  <div class="eyebrow">Chapter 4.7 (textbook; slides being updated)</div>
  <h2>Filtering in the frequency domain</h2>
  <div class="meta"><span class="chip ">TB 4.7</span><span class="chip hot">Oct 2024 Q2(ii) · Dec 2025 Q2(a) · Compre 2023 Q1</span></div>
  <p class="lede">Filtering in Chapter 3 meant sliding a kernel. In the frequency domain it means <b>multiplying the spectrum by a filter H(u, v)</b> — keep some frequencies, weaken others. The exam skill: turn a small spatial kernel into its H(u, v), or back, and say whether it is lowpass (smooths) or highpass (sharpens).</p>''']

    H.append(lesson('Filtering = multiplying the spectrum',
        'H(u, v) is a gain for every frequency. Lowpass: H ≈ 1 near the centre and small far out → blurs. Highpass: small at the centre → keeps edges and removes the average. Convolving with a kernel h in space is exactly multiplying by its H.',
        '<div class="formula">\\(g=\\mathcal F^{-1}\\{H\\cdot F\\}\\quad\\Longleftrightarrow\\quad g=h\\circledast f\\qquad H(0,0)=\\sum h\\)<span class="say">H at DC = sum of the kernel entries = what happens to the average brightness.</span></div>'
        + figs(img('f_H_ilpf', 110, 'ideal lowpass H (sharp circle)'), img('f_ilpf', 110, 'result: blur with ringing'), img('f_H_glpf', 110, 'Gaussian lowpass H'), img('f_glpf', 110, 'smooth blur, no ringing'), img('f_H_ghpf', 110, 'Gaussian highpass = 1 − lowpass'), img('f_ghpf', 110, 'edges only (mean removed)')) +
        '<p><b>Zero-phase filters:</b> if H is real and symmetric it scales the real and imaginary parts of F equally, so the phase (where things are) is untouched — no shifting or distortion. A sharp-edged (ideal) H causes ringing because its spatial kernel is a sinc with ripples.</p>',
        tag='1'))

    H.append(lesson('The recipe (textbook 4.7.3), and why we pad',
        'The DFT treats the image as periodic, so filtering wraps around: the bottom rows bleed into the top. Padding with zeros to double size gives the wrap-around somewhere harmless to go.',
        '<ol class="how"><li>Pad the M × N image to P × Q with zeros (P ≥ 2M − 1, Q ≥ 2N − 1; usually 2M × 2N).</li><li>Multiply by (−1)<sup>x+y</sup> to centre the spectrum.</li><li>DFT → F(u, v).</li>'
        '<li>Multiply by a real, symmetric H centred at (P/2, Q/2).</li><li>Inverse DFT, keep the real part.</li><li>Multiply by (−1)<sup>x+y</sup> again.</li><li>Crop the top-left M × N.</li></ol>'
        + figs(img('f_wrap', 140, 'big blur without padding: the far side bleeds in at the borders'), img('f_nowrap', 140, 'with padding: borders just darken (zeros came in)')) +
        '<p>Mnemonic: <b>pad, centre, DFT, multiply, IDFT, real part, un-centre, crop.</b></p>',
        tag='2'))

    ps = 8; uu = np.arange(ps)
    H121 = 2 + 2 * np.cos(2 * np.pi * uu / ps)
    H.append(lesson('From a kernel to H(u, v): the exam skill',
        'Put the kernel centre at the origin. A weight w at offset (s, t) means “w × the image shifted by (s, t)”, and a shift becomes the factor e<sup>j2π(us/M + vt/N)</sup>. Then pair up opposite taps: equal weights → a cosine, opposite weights → j·sine.',
        '<div class="formula">\\(e^{j\\theta}+e^{-j\\theta}=2\\cos\\theta\\qquad e^{j\\theta}-e^{-j\\theta}=2j\\sin\\theta\\qquad \\theta=\\frac{2\\pi u}{M},\\ \\psi=\\frac{2\\pi v}{N}\\)<span class="say">a symmetric pair gives 2cos; an antisymmetric pair gives 2j·sin. A symmetric kernel therefore has a real H.</span></div>'
        '<div class="cols"><div><p><b>Worked: the row kernel [1 2 1]</b> (taps at y − 1, y, y + 1). Centre 2 → 2. The pair of 1s → e<sup>jψ</sup> + e<sup>−jψ</sup> = 2cos ψ. So <b>H = 2 + 2cos ψ</b>: 4 at DC, 0 at the highest frequency (ψ = π) → lowpass.</p>'
        + table(['v (N = 8)'] + [str(v) for v in uu], [['H = 2 + 2cos(2πv/8)'] + [fmt(round(h, 3)) for h in H121]]) +
        '</div><div>' + table(['kernel', 'H(u, v)', 'type'], [
            ['average of 4 neighbours', '½(cos θ + cos ψ)', 'lowpass'],
            ['4-neighbour Laplacian', '2cos θ + 2cos ψ − 4', 'highpass (0 at DC)'],
            ['[1 2 1]', '2 + 2cos ψ', 'lowpass'],
            ['f(x + 1) − f(x − 1)', '2j sin θ', 'highpass, odd'],
            ['f(x + 1) − f(x)', 'e<sup>jθ</sup> − 1, |H| = 2|sin(θ/2)|', 'highpass']]) + '</div></div>',
        use='Oct 2024 Q2(ii) = TB 4.47, Dec 2025 Q2(a), Compre 2023 Q1, TB 4.50–4.51.', tag='3'))

    H.append(lesson('Gaussian ↔ Gaussian',
        'A Gaussian H transforms to a Gaussian kernel, with reciprocal width: a narrow H (strong blur) is a wide spatial kernel. Difference of two Gaussians gives a highpass or bandpass.',
        '<div class="formula">\\(H(\\mu)=A\\,e^{-\\mu^2/2\\sigma^2}\\quad\\Longleftrightarrow\\quad h(t)=\\sqrt{2\\pi}\\,\\sigma A\\,e^{-2\\pi^2\\sigma^2t^2}\\)<span class="say">σ in H appears as 1/(2πσ) width in h. 2-D: square the √(2π)σ factor.</span></div>',
        tag='4'))
    H.append(old_lab(old, 'freq'))

    H.append('<h3 id="ch4-filt-q">Questions on frequency-domain filters</h3>')
    M8 = 8; th = 2 * np.pi * np.arange(M8) / M8
    Hv = [[0.5 * (math.cos(a) + math.cos(b)) for b in th[:5]] for a in th[:5]]
    H.append(set_solution(card('o24q2ii'), walk([
        ('Write the filter in space', 'g(x, y) = ¼[f(x + 1, y) + f(x − 1, y) + f(x, y + 1) + f(x, y − 1)] — the centre pixel itself has weight 0.',
         rows([['0', '¼', '0'], ['¼', '0', '¼'], ['0', '¼', '0']], {(0, 1): 'n4', (1, 0): 'n4', (1, 2): 'n4', (2, 1): 'n4'}, 'kernel')),
        ('Each shift becomes an exponential', 'f(x ± 1, y) → e<sup>±j2πu/M</sup> F; f(x, y ± 1) → e<sup>±j2πv/N</sup> F.', None),
        ('Pair them into cosines', 'H = ¼[(e<sup>jθ</sup> + e<sup>−jθ</sup>) + (e<sup>jψ</sup> + e<sup>−jψ</sup>)] = ¼[2cos θ + 2cos ψ] = ½(cos θ + cos ψ).', None),
        ('Decide the type', 'H(0, 0) = 1: the average passes unchanged. Moving away from DC, H falls (to 0 at θ = ψ = π/2 and −1 at the highest frequency). Low frequencies pass, high are weakened → <b>lowpass</b>.',
         gsvg([[fmt(round(v, 3)) for v in r] for r in Hv], {(0, 0): 'c1'}, cell=62, idx=True, label='H(u, v) for M = N = 8, u, v = 0 … 4')),
    ]) + '<div class="ansbig">H(u, v) = ½[cos(2πu/M) + cos(2πv/N)] — a lowpass (smoothing) filter.</div>'))

    H.append(set_solution(card('d25q2a'), walk([
        ('Spot the centring', 'The cosines contain u − 3/2 and v − 3/2: H is written in centred coordinates (shifted by M/2 = 3/2). Rename u − 3/2 → u, v − 3/2 → v; note u + v − 3 = (u − 3/2) + (v − 3/2).', None),
        ('Uncentred H', 'H = 8 − 2cos(2πu/3) − 2cos(2πv/3) − 2cos(2π(u + v)/3) − 2cos(2π(u − v)/3).', None),
        ('Read the taps', 'Constant 8 → centre tap 8. Each −2cos(…) is a symmetric pair of −1 taps: along u → (±1, 0); along v → (0, ±1); u + v → (1, 1) and (−1, −1); u − v → (1, −1) and (−1, 1).',
         rows([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], {**ALL(3, 3, 'nd'), (1, 1): 'c1'}, 'h')),
        ('Mean of the output', 'The output mean = H(0, 0) × input mean. H(0, 0) = 8 − 8 = 0 (the kernel sums to 0), so the mean is 0.', None),
    ]) + '<div class="ansbig">h = [−1 −1 −1; −1 8 −1; −1 −1 −1]; output mean = 0.</div>'))

    H.append(set_solution(card('c23q1'), walk([
        ('Split each Sobel mask', 'g<sub>x</sub> rows are −1, 0, +1 times (1 2 1): column [−1 0 1]ᵀ times row [1 2 1]. g<sub>y</sub> is the transpose idea: column [1 2 1]ᵀ times row [−1 0 1].',
         figs(rows([[-1], [0], [1]], ALL(3, 1, 'n8'), 'g<sub>x2</sub>'), rows([[1, 2, 1]], ALL(1, 3, 'n4'), 'g<sub>x1</sub>'), rows([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], ALL(3, 3, 'hl'), '= g<sub>x</sub>'))),
        ('Spatial expressions', 'g<sub>x1</sub>: f(x, y − 1) + 2f(x, y) + f(x, y + 1). g<sub>x2</sub>: f(x + 1, y) − f(x − 1, y). Likewise g<sub>y1</sub>: f(x, y + 1) − f(x, y − 1), g<sub>y2</sub>: f(x − 1, y) + 2f(x, y) + f(x + 1, y).', None),
        ('Each to H', '[1 2 1] along y → 2 + 2cos ψ. [−1 0 1] along x → e<sup>jθ</sup> − e<sup>−jθ</sup> = 2j sin θ.', None),
        ('Multiply', 'H<sub>x</sub> = 2j sin θ · 2(1 + cos ψ) = 4j sin(2πu/M)(1 + cos(2πv/N)); H<sub>y</sub> = 4j sin(2πv/N)(1 + cos(2πu/M)). Highpass across the edge direction, lowpass along it. (With true convolution every derivative flips sign — magnitudes unchanged.)', None),
    ]) + '<div class="ansbig">H<sub>x</sub> = 4j sin(2πu/M)[1 + cos(2πv/N)], H<sub>y</sub> = 4j sin(2πv/N)[1 + cos(2πu/M)].</div>'))
    for cid in ['tb4-48', 'tb4-50']: H.append(card(cid))
    H.append('</section>')
    return '\n'.join(H)
