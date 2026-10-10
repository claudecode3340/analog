"""Chapter 3.3 rebuilt: histograms, equalisation, matching, statistics — the table method taught once, then every past
paper as a step-by-step walk with tables and bar charts."""
from ch3lib import *
from decimal import Decimal, ROUND_HALF_UP

LET = {'A': '4', 'B': '5', 'C': '6', 'D': '1', 'E': '2', 'F': '3'}
f4 = lambda v: str(Decimal(repr(float(v))).quantize(Decimal('0.0001'), ROUND_HALF_UP))
g10 = lambda v: f'{float(v):.10g}'
DEC = ' (if the screen shows a fraction, press FORMAT → Decimal)'
FIX4 = cl(K('SETTINGS', '>Calc Settings', '>Number Format'), 'optional, once: choose Fix → 4 so every result shows 4 decimals (Norm to undo)')


def sheet_eq(nk, MN=None, L=None, open_=True, show=True):
    """Spreadsheet route for equalisation: A = counts, B = running total, C = (L-1)·B/MN"""
    L = L or len(nk); MN = MN or sum(nk); n = len(nk)
    run = np.cumsum(nk); s = (L - 1) * run / MN
    o = cl(K('HOME', '>Spreadsheet', 'OK'), 'opens the sheet (cells A1:E45); the cursor is on A1') if open_ else ''
    o += cl(K(*[x for v in nk for x in (fmt(v), 'EXE')]), f'types the counts n<sub>k</sub> down column A (A1 … A{n}); each EXE moves one cell down')
    o += cl(K(fmt(nk[0]), 'EXE'), 'cursor to B1 first; B1 = the first running total, which is just the first count')
    o += cl(K('TOOLS', '>Fill Formula'), f'Form: <b>B1+A2</b> (B = SHIFT 5, A = SHIFT 4), Range: <b>B2:B{n}</b>, OK → every B cell = total above + its own count = the running total')
    o += cl(K('TOOLS', '>Fill Formula'), f'Form: <b>{L - 1}×B1÷{MN}</b>, Range: <b>C1:C{n}</b>, OK → column C = (L − 1) × running ÷ MN = s before rounding',
            lcdmat('A | B | C', [[fmt(v), int(r), f4(x)] for v, r, x in zip(nk, run, s)]) if show else '')
    return o


def arith(L1, run, MN):
    v = L1 * run / MN
    return cl(K(str(L1), '×', str(run), '÷', str(MN), 'EXE'), f'one row by plain arithmetic: (L − 1) × running ÷ MN; screen shows {g10(v)}{DEC} → rounds to <b>{half_up(v)}</b>')


def stats_cl(xs, fs, MN=None):
    xs = list(xs); fs = list(fs); x = np.array(xs, float); f = np.array(fs, float); n = f.sum()
    m = (x * f).sum() / n; sd = float(np.sqrt((x * x * f).sum() / n - m * m))
    o = cl(K('HOME', '>Statistics', '>1-Variable'), 'opens the Statistics app with an empty x column')
    o += cl(K('TOOLS', '>Frequency', '>On'), 'adds a Freq column: x = the grey level, Freq = how many pixels have it')
    o += cl(K(fmt(xs[0]), 'EXE', fmt(xs[1]), 'EXE', '…'), 'x column: ' + ', '.join(fmt(v) for v in xs) + ' (EXE after each); then the Freq column: ' + ', '.join(fmt(v) for v in fs) + '. Each row means “level x occurs Freq times” — exactly the histogram',
            lcdmat('x | Freq', [[a, b] for a, b in zip(xs, fs)]) if len(xs) <= 8 else lcdmat('x (top) | Freq (bottom)', [xs, fs]))
    o += cl(K('OK', '>1-Var Results', '>OK'), f'x̄ is the mean, σx the standard deviation (divides by n, the image formula). Do <b>not</b> use sx (divides by n − 1). Check n = {fmt(MN or n)} = number of pixels.',
            lcd('1-Var Results', f'x̄ = {g10(m)}<br>σx = {g10(sd)}<br>n = {fmt(n)}'))
    return o


def match_rows(sr, Gr):
    rows = []
    for s in sorted(set(sr)):
        d = [abs(s - g) for g in Gr]; best = min(d); z = d.index(best)
        ties = [k for k, v in enumerate(d) if v == best]
        rows.append([s, ', '.join(f'z={k}: G={Gr[k]}' for k in range(len(Gr)) if abs(s - Gr[k]) <= best + 0) + (' (tie → smallest z)' if len(ties) > 1 else ''), f'<b>{z}</b>'])
    return rows


def section(card):
    H = ['''<section class="topic" id="ch3-hist">
  <div class="eyebrow">Chapter 3.3 · Lectures 8–9</div>
  <h2>Histograms: counting grey levels, equalisation and matching</h2>
  <div class="meta"><span class="chip ">TB 3.3</span><span class="chip ">slides pp. 15–21</span><span class="chip hot">in every paper</span></div>
  <p class="lede">A histogram counts how many pixels have each grey level. It tells you at a glance whether an image is dark, bright, washed out or contrasty — and it is the basis of the most frequently examined computation in this course: <b>histogram equalisation</b> (spread the grey levels out) and <b>histogram matching</b> (give the image a histogram of a chosen shape). Learn the table method once and every one of these questions becomes mechanical.</p>''']

    # 1 histogram
    small = [[0, 1, 1, 2], [1, 2, 2, 3], [2, 2, 3, 3], [1, 2, 3, 3]]
    nk = [1, 4, 6, 5]
    H.append(lesson('What a histogram is',
        'For every grey level r<sub>k</sub>, count the pixels that have it: that count is n<sub>k</sub>. Divide by the total number of pixels (M×N) and you get p(r<sub>k</sub>), the fraction of the image at that level. The fractions add up to 1.',
        '<div class="cols"><div>'
        '<p><b>Example</b> (2-bit image, 16 pixels): level 0 appears once, 1 four times, 2 six times, 3 five times → n = 1, 4, 6, 5 and p = 1/16, 4/16, 6/16, 5/16 = 0.0625, 0.25, 0.375, 0.3125.</p>'
        '<p>A histogram forgets <b>where</b> the pixels are — very different images can have the same histogram (your slide; the blur question in Section 3.5 is built on this).</p>'
        '<p>Histograms are cheap to compute, which is why histogram methods are popular in real-time hardware.</p>'
        '</div><div>' + figs(gsvg(small, {}, cell=42, label='a 4×4, 2-bit image'), bars(nk, 'its histogram n_k', w=220)) + '</div></div>'
        '<h4 style="margin-top:16px">The shape of the histogram tells you how the image looks</h4>' +
        figs(photo_with_hist('cam_g25', 'dark: bars piled on the left'), photo_with_hist('cam_g04', 'bright: bars piled on the right'), photo_with_hist('cam_low', 'low contrast: a narrow hump'), photo_with_hist('cam', 'good contrast: spread over the whole range')),
        tag='1'))

    # 2 mean and variance
    H.append(lesson('Mean and standard deviation from a histogram',
        'Treat p(r<sub>k</sub>) as “how often level r<sub>k</sub> occurs”. The mean is the average level; the variance is the average squared distance from the mean.',
        '<div class="cols"><div><div class="formula">\\(m=\\sum_k r_k\\,p(r_k)\\), \\(\\sigma^2=\\sum_k r_k^2\\,p(r_k)-m^2\\)<span class="say">The second form (average of r² minus mean²) is fastest by hand.</span></div>'
        '<p><b>Example</b> (the 2-bit image above): m = (0·1 + 1·4 + 2·6 + 3·5)/16 = 31/16 = <b>1.9375</b>. Average of r² = (0 + 4 + 24 + 45)/16 = 73/16 = 4.5625; σ² = 4.5625 − 1.9375² = <b>0.8086</b>; σ = 0.8992.</p>'
        '<p><b>If the counts are given by a formula</b> (e.g. H(r) = k·r): first find k from “all counts add up to M×N” (Mid-sem 2023 and 2024 Q1).</p></div>'
        '<div><p><b>On the calculator:</b> Statistics app → 1-Variable → TOOLS → Frequency On; type the levels in x and the counts in Freq; OK → 1-Var Results: x̄ is the mean, σx the standard deviation (not sx).</p></div></div>',
        tag='2'))

    # 3 equalisation
    eqt, eqs = eq_table([24, 48, 96, 360, 420, 288, 192, 108])
    H.append(lesson('Histogram equalisation: spread the grey levels out',
        'Goal: use the whole range of grey levels, each roughly equally often, so the image gets more contrast. The rule sends each level to <b>“the fraction of pixels that are this dark or darker”</b>, scaled to the full range. Dark levels that hold many pixels get pulled apart; rare levels get squeezed.',
        '<div class="cols"><div>'
        '<div class="formula">\\(s_k=(L-1)\\displaystyle\\sum_{j=0}^{k}p_r(r_j)=(L-1)\\times\\frac{\\text{pixels with level}\\le r_k}{MN}\\)<span class="say">“running total of the counts, times (L − 1), divided by the number of pixels” — then round to the nearest whole level.</span></div>'
        '<p><b>The table method</b> (always the same five columns):</p><ol class="how">'
        '<li>Write r<sub>k</sub> and the counts n<sub>k</sub>. Check that the counts add up to M×N.</li>'
        '<li>Running total: add the counts from the top down.</li>'
        '<li>s = (L − 1) × running total ÷ MN.</li>'
        '<li>Round s to the nearest integer (0.5 goes up). This is the lookup table r → s.</li>'
        '<li>New histogram: move each count n<sub>k</sub> to its new level s; counts that land on the same level are added.</li></ol>'
        '<p><b>Why the result is not perfectly flat:</b> all pixels of one level move together — a bar can be moved but never split — and rounding can merge bars. Equalising a second time changes nothing (textbook 3.7).</p>'
        '</div><div><p><b>Worked (Quiz-1 2026, 3-bit, 32×48 = 1536 pixels):</b></p>' + eqt +
        figs(bars([24, 48, 96, 360, 420, 288, 192, 108], 'before', w=230), bars(moved_hist([24, 48, 96, 360, 420, 288, 192, 108], eqs), 'after: bars moved and merged', w=230, hl={6})) +
        '<p>Level 6 of the result receives only r = 5 (288 pixels) → p<sub>s</sub>(6) = 288/1536 = <b>0.1875</b>.</p></div></div>'
        '<h4 style="margin-top:12px">On a photo</h4>' + figs(photo_with_hist('cam_low', 'low-contrast original'), photo_with_hist('cam_low_eq', 'after equalisation: the histogram is spread over 0 … 255')),
        use='in almost every paper: Quiz-1 2026 Q4, Mid-sem 2019 Q2, Quiz-1 2021 Q6, End-sem 2023 Q3, Compre 2019 ramp. Calculator: the Spreadsheet does columns 2–3 in one Fill Formula (recipe B).', tag='3'))
    H.append('<div class="lab" data-lab="hist" data-init=\'{"nk": [24, 48, 96, 360, 420, 288, 192, 108]}\'></div>')

    # 4 matching
    e35 = ANS['ex35']; e37 = ANS['ex37']
    H.append(lesson('Histogram matching (specification): give the image a chosen histogram',
        'Sometimes you do not want a flat histogram but a <b>specific shape</b>. The trick: equalise the input, equalise the target shape, and connect the two through their equalised values — two pixels belong together if the same fraction of pixels is darker than them.',
        '<div class="cols"><div><p><b>The slide procedure (4 steps):</b></p><ol class="how">'
        '<li>Equalise the input: s<sub>k</sub> = (L − 1) × running fraction of the input, rounded.</li>'
        '<li>Do the same for the <b>target</b> histogram p<sub>z</sub>: G(z<sub>q</sub>) = (L − 1) × running fraction of the target, rounded.</li>'
        '<li>For every s<sub>k</sub>, find the z<sub>q</sub> whose G(z<sub>q</sub>) is <b>closest</b> to s<sub>k</sub>. <b>If two are equally close, take the smaller z</b> (your instructor’s rule).</li>'
        '<li>Chain them: r<sub>k</sub> → s<sub>k</sub> → z<sub>q</sub>. Rewrite the image with the z values.</li></ol>'
        '<p><b>Continuous version</b> (Mid-sem Oct 2024 Q2(i), textbook 3.11–3.12): s = T(r) = ∫p<sub>r</sub>, G(z) = ∫p<sub>z</sub>, set G(z) = T(r) and solve for z.</p></div>'
        '<div><p><b>Worked (your slide’s example):</b> input s = ' + ', '.join(str(v) for v in e35['sr']) + ' for r = 0 … 7; target G rounded = ' + ', '.join(str(v) for v in e37['Gr']) + ' for z = 0 … 7.</p>' +
        table(['s from step 1', 'closest G values', 'z'], [[1, 'G(z=3) = 1', '<b>3</b>'], [3, 'G(z=4) = 2 (distance 1)', '<b>4</b>'], [5, 'G(z=5) = 5', '<b>5</b>'], [6, 'G(z=6) = 6', '<b>6</b>'], [7, 'G(z=7) = 7', '<b>7</b>']]) +
        '<p>So r → z: 0→3, 1→4, 2→5, 3→6, 4→6, 5→7, 6→7, 7→7.</p></div></div>',
        use='Compre Dec 2025 Q3 (8×8 image), slide example, Mid-sem Oct 2024 Q2(i) (continuous).', tag='4'))

    # 5 local
    H.append(lesson('Local histogram processing and histogram statistics (textbook 3.3, brief)',
        'Global equalisation uses one histogram for the whole image, so small dark details can stay hidden. Local processing repeats the computation in a small window around every pixel.',
        '<div class="cols"><div><p><b>Local equalisation:</b> for each pixel, equalise using only the histogram of its neighbourhood (e.g. 3×3 or 7×7), and keep the new value of the centre pixel only. Hidden faint shapes inside dark areas appear.</p>'
        '<p><b>Local statistics rule</b> (textbook Example 3.12): multiply a pixel by a constant C only where its local mean is small (dark area) <b>and</b> its local standard deviation is small (low contrast): k₀m<sub>G</sub> ≤ m<sub>S</sub> ≤ k₁m<sub>G</sub> and k₂σ<sub>G</sub> ≤ σ<sub>S</sub> ≤ k₃σ<sub>G</sub>.</p></div>'
        '<div>' + figs(img('hidden', 140, 'original: four dark squares'), img('hidden_global', 140, 'global equalisation: noise, nothing new'), img('hidden_local', 140, 'local (7×7): the hidden inner squares appear')) + '</div></div>',
        tag='5'))

    # ── questions ──
    H.append('<h3 id="ch3-hist-q">Questions on histograms</h3>')
    H.append(set_solution(card('m23q1'), walk([
        ('Find k from the pixel count', 'Every pixel has some level, so all the counts add up to the number of pixels: k·(0 + 1 + … + 7) = k·28 = 50 × 70 = 3500 → <b>k = 125</b>. Counts: 0, 125, 250, …, 875.', bars([125 * r for r in range(8)], 'H(r) = 125 r', w=240),
         cl(K('50', '×', '70', '÷', '28', 'EXE'), 'number of pixels ÷ (0 + 1 + … + 7); screen shows 125 = k')),
        ('Mean', 'p(r) = 125r/3500 = r/28. Mean = Σ r·p(r) = (0 + 1 + 4 + 9 + 16 + 25 + 36 + 49)/28 = 140/28 = <b>5</b>.', None,
         stats_cl(range(8), [125 * r for r in range(8)], 3500)),
        ('Standard deviation', 'Average of r² = Σ r²·r/28 = (0 + 1 + 8 + 27 + 64 + 125 + 216 + 343)/28 = 784/28 = 28. Variance = 28 − 5² = <b>3</b>; σ = √3 = <b>1.7321</b>.', None,
         cl(K('OK', '>1-Var Results', '>OK'), 'read σx = 1.732050808 on the same screen: that is σ directly')
         + cl(K('1.732050808', 'x²', 'EXE'), 'squares σx → screen shows 3 = the variance')),
    ]) + '<div class="ansbig">(a) k = 125. (b) mean = 5, σ² = 3, σ = 1.7321.</div>'))
    H24 = [100 * r for r in range(8)] + [100 * (15 - r) for r in range(8, 16)]
    H.append(set_solution(card('m24q1'), walk([
        ('Read the figure as two straight lines', 'The line from (0, 0) rises as k₁r up to r = 7, stays at r = 8 and falls symmetrically to 0 at r = 15, i.e. H(r) = k₁(15 − r) for r ≥ 8. (If your figure is read differently, the same method applies.)', None),
        ('Find k₁ from the pixel count', 'All counts add up to 70 × 80 = 5600: k₁(0 + 1 + … + 7) + k₁(7 + 6 + … + 0) = 56k₁ = 5600 → <b>k₁ = 100</b>. So H = 0, 100, …, 700, 700, 600, …, 0.', bars(H24, 'H(r)', w=280),
         cl(K('70', '×', '80', '÷', '56', 'EXE'), 'number of pixels ÷ 56; screen shows 100 = k₁')),
        ('Mean and standard deviation', 'The histogram is symmetric about 7.5 → mean = <b>7.5</b>. σ² = Σ (r − 7.5)² H(r) / 5600 = <b>9.25</b> → σ = <b>3.0414</b>.', None,
         stats_cl(range(16), H24, 5600)
         + cl(K('3.041381265', 'x²', 'EXE'), 'squares σx → screen shows 9.25 = the variance')),
    ]) + '<div class="ansbig">(a) k₁ = 100; H = 0, 100, …, 700 for r = 0…7 and 700, 600, …, 0 for r = 8…15. (b) mean = 7.5, σ² = 9.25, σ = 3.0414.</div>'))
    nq4 = [24, 48, 96, 360, 420, 288, 192, 108]
    H.append(set_solution(card('qz4'), walk([
        ('Build the table', 'L = 8 (3-bit), MN = 32 × 48 = 1536. Running total of the counts, × 7 ÷ 1536, round (0.5 goes up).', eq_table(nq4)[0],
         cl(K('32', '×', '48', 'EXE'), 'MN = 1536 = the number of pixels (also the last running total — a free check)')
         + arith(7, 528, 1536) + FIX4 + sheet_eq(nq4)),
        ('Move the counts', 'Each count goes to its rounded s; counts landing on the same s are added: s = 0 gets 24 + 48 = 72, s = 1 gets 96, s = 2 gets 360, s = 4 gets 420, s = 6 gets 288, s = 7 gets 192 + 108 = 300.', bars([72, 96, 360, 0, 420, 0, 288, 300], 'equalised histogram', w=240, hl={6}),
         cl('round C', 'column C rounded: 0, 0, 1, 2, 4, 6, 7, 7. Only r = 5 lands on s = 6 (5.6328 → 6), so bar 6 holds just the 288 pixels of r = 5')),
        ('Normalise the asked bar', 'p<sub>s</sub>(6) = 288 / 1536 = <b>0.1875</b>.', None,
         cl(K('288', '÷', '1536', 'EXE'), 'count of bar 6 ÷ number of pixels; screen shows 3/16 → FORMAT → Decimal → 0.1875')),
    ]) + '<div class="ansbig">p<sub>s</sub>(6) = 0.1875.</div>'))
    I192 = [[0, 0, 1, 4, 5, 4], [0, 1, 2, 5, 4, 3], [1, 2, 3, 4, 3, 1], [4, 5, 4, 3, 1, 0], [5, 4, 3, 1, 0, 0], [4, 4, 3, 1, 0, 0]]
    m19 = ANS['m19_2']
    H.append(set_solution(card('s19q2'), walk([
        ('Count every grey level (tally)', 'Go through the 36 pixels and tally: 0 → 8, 1 → 7, 2 → 2, 3 → 6, 4 → 9, 5 → 4, 6 → 0, 7 → 0. Check: 8 + 7 + 2 + 6 + 9 + 4 = 36 ✓.', figs(gsvg(I192, {}, cell=34, idx=False, label='the image'), bars(m19['nk'], 'counts', w=220)),
         cl(K('8', '+', '7', '+', '2', '+', '6', '+', '9', '+', '4', 'EXE'), 'the tally check: screen must show 36 = 6 × 6, otherwise a pixel was missed')),
        ('Equalisation table', 'L − 1 = 7, MN = 36.', eq_table(m19['nk'])[0],
         arith(7, 15, 36) + sheet_eq(m19['nk'])
         + cl('round C', 'LUT 2, 3, 3, 4, 6, 7, 7, 7 (r = 6, 7 do not occur but still map to 7)')),
        ('Rewrite the image with the lookup table', 'r → s: 0→2, 1→3, 2→3, 3→4, 4→6, 5→7, 6→7, 7→7.', figs(gsvg(m19['img'], {}, cell=34, idx=False, label='equalised image'), bars(m19['eq_hist'], 'its histogram', w=220))),
    ]) + '<div class="ansbig">Lookup table 0→2, 1→3, 2→3, 3→4, 4→6, 5→7, 6→7, 7→7, and the image in step 3.</div>'))
    ne = [1813, 1506, 574, 203]
    H.append(set_solution(card('e23q3'), walk([
        ('Work with level numbers k = 0 … 3', 'Levels 0, ⅓, ⅔, 1 are k/3 for k = 0 … 3, so L = 4 and L − 1 = 3. MN = 64 × 64 = 4096; check 1813 + 1506 + 574 + 203 = 4096 ✓.', None,
         cl(K('1813', '+', '1506', '+', '574', '+', '203', 'EXE'), 'screen shows 4096 = 64 × 64 ✓')),
        ('Running totals and s', 'Running totals 1813, 3319, 3893, 4096; s = 3 × running ÷ 4096 = 1.3279, 2.4309, 2.8513, 3 → rounded 1, 2, 3, 3.', eq_table(ne)[0],
         cl(K('1813', '+', '1506', 'EXE'), 'second running total: 3319 (then + 574 → 3893)')
         + arith(3, 1813, 4096) + arith(3, 3319, 4096) + arith(3, 3893, 4096)),
        ('Back to normalised levels', 'k → s: 0 → 1, 1 → 2, 2 → 3, 3 → 3, i.e. 0 → ⅓, ⅓ → ⅔, ⅔ → 1, 1 → 1.', None),
        ('Equalised histogram', 'p(0) = 0, p(⅓) = 1813/4096 = <b>0.4426</b>, p(⅔) = 1506/4096 = <b>0.3677</b>, p(1) = (574 + 203)/4096 = <b>0.1897</b>.', bars([0, 1813, 1506, 777], 'equalised counts at s = 0, ⅓, ⅔, 1', w=200),
         cl(K('1813', '÷', '4096', 'EXE'), f'screen 0.4426 (FORMAT → Decimal if a fraction appears)')
         + cl(K('1506', '÷', '4096', 'EXE'), 'screen 0.3677')
         + cl(K('(', '574', '+', '203', ')', '÷', '4096', 'EXE'), 'the two merged bars together: 0.1897')),
    ]) + '<div class="ansbig">Levels map 0 → ⅓, ⅓ → ⅔, ⅔ → 1, 1 → 1. Equalised p(s): 0, 0.4426, 0.3677, 0.1897 at s = 0, ⅓, ⅔, 1.</div>'))
    nr = [125 * r for r in range(8)]
    H.append(set_solution(card('c19ramp'), walk([
        ('(c) The equalising table', 'Running counts 0, 125, 375, 750, 1250, 1875, 2625, 3500; s = 7 × running ÷ 3500 = 0, 0.25, 0.75, 1.5, 2.5, 3.75, 5.25, 7. Two values land exactly on .5: round half up → 2 and 3. T: r → 0, 0, 1, 2, 3, 4, 5, 7.', eq_table(nr)[0],
         arith(7, 750, 3500) + sheet_eq(nr)),
        ('(d) The new histogram', 'Move each count to its s: s = 0 gets 0 + 125, then 250, 375, 500, 625, 750 at s = 1 … 5, nothing at 6, 875 at 7.', bars([125, 250, 375, 500, 625, 750, 0, 875], 'H(s)', w=240)),
        ('(e) Mean and σ of the result', 'mean = <b>4.25</b>, σ = <b>2.0463</b>. The mean moves towards the middle and the spread goes up — more contrast.', None,
         stats_cl(range(8), [125, 250, 375, 500, 625, 750, 0, 875], 3500)),
    ]) + '<div class="ansbig">(c) s = 0, 0, 1, 2, 3, 4, 5, 7. (d) H(s) = 125, 250, 375, 500, 625, 750, 0, 875. (e) mean = 4.25, σ = 2.0463.</div>'))

    q21 = [[4, 2, 3, 2, 5], [1, 1, 2, 3, 4], [1, 3, 2, 3, 4], [2, 2, 3, 1, 3], [2, 2, 1, 1, 4]]
    qh = ANS['q21_hist']
    V12 = {(i, j): ('in' if q21[i][j] in (1, 2) else 'out') for i in range(5) for j in range(5)}
    H.append(set_solution(card('q21a'), walk([
        ('1 · Distances between the underlined pixels', 'They are (0, 3) and (3, 0): Δx = 3, Δy = 3. Euclidean = √(9 + 9) = 3√2 = <b>4.2426</b>; city-block = 3 + 3 = <b>6</b>.', None,
         cl(K('√(', '3', 'x²', '+', '3', 'x²', ')', 'EXE'), 'Euclidean distance; screen shows 3√2 → FORMAT → Decimal → 4.242640687')),
        ('2 · LSB plane', 'The last binary digit = 1 for odd values, 0 for even.', gsvg(ANS['q21_lsb'], {(i, j): 'hl' for i in range(5) for j in range(5) if ANS['q21_lsb'][i][j]}, cell=36, idx=False)),
        ('3 · Negative', 'Every value r becomes 7 − r (3-bit).', gsvg(ANS['q21_neg'], {}, cell=36, idx=False)),
        ('4 · Shortest m-path, V = {1, 2}', 'Shade the 1s and 2s. (3,0) → (3,1) → (2,2) → (1,2) → (0,3): the two diagonals are allowed because their corner pixels are all 3s (not in V). <b>Length 4.</b>', gsvg(q21, V12, path=[(3, 0), (3, 1), (2, 2), (1, 2), (0, 3)], cell=40)),
        ('5 · Histogram', 'Counts for 0 … 7: 0, 6, 8, 6, 4, 1, 0, 0 (25 pixels).', bars(qh['nk'], 'n_k', w=240),
         cl(K('6', '+', '8', '+', '6', '+', '4', '+', '1', 'EXE'), 'tally check: screen must show 25 = 5 × 5')),
        ('6 · Equalise', 'Table with L − 1 = 7, MN = 25, then move the counts.', eq_table(qh['nk'])[0] + figs(bars(qh['eq_hist'], 'equalised histogram', w=240), gsvg(qh['eq_img'], {}, cell=34, idx=False, label='equalised image')),
         arith(7, 14, 25) + sheet_eq(qh['nk'])
         + cl('round C', 'LUT 0, 2, 4, 6, 7, 7, 7, 7; then move the counts: 6 → s = 2, 8 → 4, 6 → 6, 4 + 1 → 7')),
    ]) + '<div class="ansbig">1: 4.2426 and 6. 2–3: the grids above. 4: length 4. 5: 0, 6, 8, 6, 4, 1, 0, 0. 6: r → s = 0, 2, 4, 6, 7, 7, 7, 7; new histogram 0, 0, 6, 0, 8, 0, 6, 5.</div>'))

    pz = [0, 0, 0, 0.15, 0.2, 0.3, 0.2, 0.15]; Gc = 7 * np.cumsum(pz)
    H.append(set_solution(card('sl-match'), walk([
        ('(a) Equalise the input', 'L − 1 = 7, MN = 4096.', eq_table(e35['nk'])[0],
         arith(7, 790, 4096) + sheet_eq(e35['nk'])
         + cl('round C', 'write it down: s = 1, 3, 5, 6, 6, 7, 7, 7')),
        ('(b) Equalise the target', 'Running total of p<sub>z</sub> = 0, 0, 0, 0.15, 0.35, 0.65, 0.85, 1.00 → × 7 = 0, 0, 0, 1.05, 2.45, 4.55, 5.95, 7 → rounded G = 0, 0, 0, 1, 2, 5, 6, 7.', None,
         cl('retype A1:A8', 'cursor to A1, type ' + ', '.join(fmt(v) for v in pz) + ' over the old counts (EXE after each); column B recalculates itself: it is now the running total of p<sub>z</sub>')
         + cl(K('TOOLS', '>Fill Formula'), 'Form: <b>7×B1</b>, Range: <b>C1:C8</b>, OK → no ÷ MN, because the p<sub>z</sub> already add up to 1', lcdmat('B | C', [[fmt(round(b, 4)), fmt(round(c, 4))] for b, c in zip(np.cumsum(pz), Gc)]))),
        ('Connect each s to the closest G', 'Rule: closest G; on a tie the smaller z.', table(['s', 'closest G', 'z'], [[1, 'G(3) = 1', '3'], [3, 'G(4) = 2', '4'], [5, 'G(5) = 5', '5'], [6, 'G(6) = 6', '6'], [7, 'G(7) = 7', '7']])),
        ('Chain r → s → z', 'r = 0 … 7 → s = 1, 3, 5, 6, 6, 7, 7, 7 → z = 3, 4, 5, 6, 6, 7, 7, 7.', None),
    ]) + '<div class="ansbig">(a) s = 1, 3, 5, 6, 6, 7, 7, 7. (b) r → z: 0→3, 1→4, 2→5, 3→6, 4→6, 5→7, 6→7, 7→7.</div>'))

    e25 = ANS['e25_3']; tg = [13, 12, 14, 14, 11, 0, 0, 0]
    H.append(set_solution(card('d25q3'), walk([
        ('Count the input levels', 'From the 8×8 image (64 pixels): n = 2, 3, 5, 6, 9, 12, 14, 13 for r = 0 … 7.', None,
         cl(K('2', '+', '3', '+', '5', '+', '6', '+', '9', '+', '12', '+', '14', '+', '13', 'EXE'), 'tally check: screen must show 64 = 8 × 8')),
        ('Equalise the input', 's = 7 × running ÷ 64, rounded: 0, 1, 1, 2, 3, 4, 6, 7.', eq_table(e25['nk'])[0],
         arith(7, 5, 64) + sheet_eq(e25['nk'])
         + cl('round C', 'write it down: s = 0, 1, 1, 2, 3, 4, 6, 7')),
        ('Equalise the target (13, 12, 14, 14, 11, 0, 0, 0)', 'Same formula, same MN = 64: G rounded = 1, 3, 4, 6, 7, 7, 7, 7.', eq_table(tg)[0],
         cl('retype A1:A8', 'cursor to A1, type 13, 12, 14, 14, 11, 0, 0, 0 over the old counts (EXE after each); B and C recalculate by themselves — column C is now G before rounding',
            lcdmat('A | B | C', [[v, int(r), f4(x)] for v, r, x in zip(tg, np.cumsum(tg), 7 * np.cumsum(tg) / 64)]))),
        ('Connect each s to the closest G (tie → smaller z)', 'G rounded = 1, 3, 4, 6, 7, 7, 7, 7 for z = 0 … 7.', table(['s', 'distance to each G', 'z'], [[0, 'G(0) = 1 is closest (distance 1)', '0'], [1, 'G(0) = 1 exactly', '0'], [2, 'G(0) = 1 and G(1) = 3 are both 1 away → <b>tie → smaller z</b>', '0'], [3, 'G(1) = 3', '1'], [4, 'G(2) = 4', '2'], [6, 'G(3) = 6', '3'], [7, 'G(4) = 7 (and 5, 6, 7) → smallest', '4']])),
        ('Rewrite the image', 'r → z: 0→0, 1→0, 2→0, 3→0, 4→1, 5→2, 6→3, 7→4.', gsvg(e25['g'], {}, cell=34, idx=False, label='g(x, y)')),
    ]) + '<div class="ansbig">r → z: 0→0, 1→0, 2→0, 3→0, 4→1, 5→2, 6→3, 7→4, and g as in step 5. (The official key maps 3 → 1, breaking the slide’s tie rule, and has one typo at row 5, column 1.)</div>'))

    H.append(set_solution(card('o24q2i'), walk([
        ('Equalise the input (its CDF)', 's = T(r) = ∫<sub>0</sub><sup>r</sup> (2 − 2w) dw = <b>2r − r²</b>. (On [0, 1] the (L − 1) factor is 1.)', None),
        ('Equalise the target (its CDF)', 'G(z) = ∫<sub>0</sub><sup>z</sup> 3w² dw = <b>z³</b>.', None),
        ('Set G(z) = T(r) and solve for z', 'z³ = 2r − r² → <b>z = (2r − r²)<sup>1/3</sup></b>. Check: r = 0 → z = 0, r = 1 → z = 1, and it increases in between ✓.', None),
        ('Sanity-check one point on the calculator', 'At r = 0.5: T = 0.75, z = 0.75<sup>1/3</sup> = 0.9086, and G(0.9086) = 0.75 ✓.', None,
         cl(K('2', '×', '0.5', '−', '0.5', 'x²', 'EXE'), 'T(0.5) = 2r − r²; screen shows 3/4 (FORMAT → Decimal → 0.75)')
         + cl(K('Ans', 'x^■', '(', '1', '÷', '3', ')', 'EXE'), 'z = T<sup>1/3</sup>; screen shows 0.9085602964')
         + cl(K('Ans', 'x^■', '3', 'EXE'), 'G(z) = z³ goes back to 0.75 ✓')),
    ]) + '<div class="ansbig">z = (2r − r²)<sup>1/3</sup>.</div>'))

    for cid in ['tb3-10', 'tb3-6', 'tb3-7', 'tb3-11', 'tb3-12']: H.append(card(cid))
    H.append(set_solution(card('dr-stats'), walk([
        ('Histogram → mean', 'Counts 6, 8, 6, 4, 1 for values 1 … 5 (25 pixels). Mean = (1·6 + 2·8 + 3·6 + 4·4 + 5·1)/25 = 61/25 = <b>2.44</b>.', bars([0, 6, 8, 6, 4, 1], 'counts for 0 … 5', w=200),
         stats_cl(range(1, 6), [6, 8, 6, 4, 1], 25)),
        ('Variance and σ', 'Average of r² = (6 + 32 + 54 + 64 + 25)/25 = 181/25 = 7.24. Variance = 7.24 − 2.44² = <b>1.2864</b>; σ = <b>1.1342</b> (divide by the number of pixels, not n − 1).', None,
         cl(K('1.13419575', 'x²', 'EXE'), 'squares σx → screen shows 1.2864 = the variance')),
    ]) + '<div class="ansbig">Mean = 2.44; variance = 1.2864; σ = 1.1342.</div>'))
    H.append(card('dr-local'))
    H.append('</section>')
    return '\n'.join(H)
