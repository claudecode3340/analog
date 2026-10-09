"""Chapter 3.3 rebuilt: histograms, equalisation, matching, statistics — the table method taught once, then every past
paper as a step-by-step walk with tables and bar charts."""
from ch3lib import *


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
        ('Find k from the pixel count', 'Every pixel has some level, so all the counts add up to the number of pixels: k·(0 + 1 + … + 7) = k·28 = 50 × 70 = 3500 → <b>k = 125</b>. Counts: 0, 125, 250, …, 875.', bars([125 * r for r in range(8)], 'H(r) = 125 r', w=240)),
        ('Mean', 'p(r) = 125r/3500 = r/28. Mean = Σ r·p(r) = (0 + 1 + 4 + 9 + 16 + 25 + 36 + 49)/28 = 140/28 = <b>5</b>.', None),
        ('Standard deviation', 'Average of r² = Σ r²·r/28 = (0 + 1 + 8 + 27 + 64 + 125 + 216 + 343)/28 = 784/28 = 28. Variance = 28 − 5² = <b>3</b>; σ = √3 = <b>1.7321</b>.', None),
    ]) + '<div class="ansbig">(a) k = 125. (b) mean = 5, σ² = 3, σ = 1.7321.</div>'))
    H.append(card('m24q1'))
    H.append(set_solution(card('qz4'), walk([
        ('Build the table', 'L = 8 (3-bit), MN = 32 × 48 = 1536.', eq_table([24, 48, 96, 360, 420, 288, 192, 108])[0]),
        ('Move the counts', 'Each count goes to its rounded s; counts landing on the same s are added: s = 0 gets 24 + 48 = 72, s = 1 gets 96, s = 2 gets 360, s = 4 gets 420, s = 6 gets 288, s = 7 gets 192 + 108 = 300.', bars([72, 96, 360, 0, 420, 0, 288, 300], 'equalised histogram', w=240, hl={6})),
        ('Normalise the asked bar', 'p<sub>s</sub>(6) = 288 / 1536 = <b>0.1875</b>.', None),
    ]) + '<div class="ansbig">p<sub>s</sub>(6) = 0.1875.</div>'))
    I192 = [[0, 0, 1, 4, 5, 4], [0, 1, 2, 5, 4, 3], [1, 2, 3, 4, 3, 1], [4, 5, 4, 3, 1, 0], [5, 4, 3, 1, 0, 0], [4, 4, 3, 1, 0, 0]]
    m19 = ANS['m19_2']
    H.append(set_solution(card('s19q2'), walk([
        ('Count every grey level (tally)', 'Go through the 36 pixels and tally: 0 → 8, 1 → 7, 2 → 2, 3 → 6, 4 → 9, 5 → 4, 6 → 0, 7 → 0. Check: 8 + 7 + 2 + 6 + 9 + 4 = 36 ✓.', figs(gsvg(I192, {}, cell=34, idx=False, label='the image'), bars(m19['nk'], 'counts', w=220))),
        ('Equalisation table', 'L − 1 = 7, MN = 36.', eq_table(m19['nk'])[0]),
        ('Rewrite the image with the lookup table', 'r → s: 0→2, 1→3, 2→3, 3→4, 4→6, 5→7, 6→7, 7→7.', figs(gsvg(m19['img'], {}, cell=34, idx=False, label='equalised image'), bars(m19['eq_hist'], 'its histogram', w=220))),
    ]) + '<div class="ansbig">Lookup table 0→2, 1→3, 2→3, 3→4, 4→6, 5→7, 6→7, 7→7, and the image in step 3.</div>'))
    for cid in ['e23q3', 'c19ramp']: H.append(card(cid))

    q21 = [[4, 2, 3, 2, 5], [1, 1, 2, 3, 4], [1, 3, 2, 3, 4], [2, 2, 3, 1, 3], [2, 2, 1, 1, 4]]
    qh = ANS['q21_hist']
    V12 = {(i, j): ('in' if q21[i][j] in (1, 2) else 'out') for i in range(5) for j in range(5)}
    H.append(set_solution(card('q21a'), walk([
        ('1 · Distances between the underlined pixels', 'They are (0, 3) and (3, 0): Δx = 3, Δy = 3. Euclidean = √(9 + 9) = 3√2 = <b>4.2426</b>; city-block = 3 + 3 = <b>6</b>.', None),
        ('2 · LSB plane', 'The last binary digit = 1 for odd values, 0 for even.', gsvg(ANS['q21_lsb'], {(i, j): 'hl' for i in range(5) for j in range(5) if ANS['q21_lsb'][i][j]}, cell=36, idx=False)),
        ('3 · Negative', 'Every value r becomes 7 − r (3-bit).', gsvg(ANS['q21_neg'], {}, cell=36, idx=False)),
        ('4 · Shortest m-path, V = {1, 2}', 'Shade the 1s and 2s. (3,0) → (3,1) → (2,2) → (1,2) → (0,3): the two diagonals are allowed because their corner pixels are all 3s (not in V). <b>Length 4.</b>', gsvg(q21, V12, path=[(3, 0), (3, 1), (2, 2), (1, 2), (0, 3)], cell=40)),
        ('5 · Histogram', 'Counts for 0 … 7: 0, 6, 8, 6, 4, 1, 0, 0 (25 pixels).', bars(qh['nk'], 'n_k', w=240)),
        ('6 · Equalise', 'Table with L − 1 = 7, MN = 25, then move the counts.', eq_table(qh['nk'])[0] + figs(bars(qh['eq_hist'], 'equalised histogram', w=240), gsvg(qh['eq_img'], {}, cell=34, idx=False, label='equalised image'))),
    ]) + '<div class="ansbig">1: 4.2426 and 6. 2–3: the grids above. 4: length 4. 5: 0, 6, 8, 6, 4, 1, 0, 0. 6: r → s = 0, 2, 4, 6, 7, 7, 7, 7; new histogram 0, 0, 6, 0, 8, 0, 6, 5.</div>'))

    H.append(set_solution(card('sl-match'), walk([
        ('(a) Equalise the input', 'L − 1 = 7, MN = 4096.', eq_table(e35['nk'])[0]),
        ('(b) Equalise the target', 'Running total of p<sub>z</sub> = 0, 0, 0, 0.15, 0.35, 0.65, 0.85, 1.00 → × 7 = 0, 0, 0, 1.05, 2.45, 4.55, 5.95, 7 → rounded G = 0, 0, 0, 1, 2, 5, 6, 7.', None),
        ('Connect each s to the closest G', 'Rule: closest G; on a tie the smaller z.', table(['s', 'closest G', 'z'], [[1, 'G(3) = 1', '3'], [3, 'G(4) = 2', '4'], [5, 'G(5) = 5', '5'], [6, 'G(6) = 6', '6'], [7, 'G(7) = 7', '7']])),
        ('Chain r → s → z', 'r = 0 … 7 → s = 1, 3, 5, 6, 6, 7, 7, 7 → z = 3, 4, 5, 6, 6, 7, 7, 7.', None),
    ]) + '<div class="ansbig">(a) s = 1, 3, 5, 6, 6, 7, 7, 7. (b) r → z: 0→3, 1→4, 2→5, 3→6, 4→6, 5→7, 6→7, 7→7.</div>'))

    e25 = ANS['e25_3']
    H.append(set_solution(card('d25q3'), walk([
        ('Count the input levels', 'From the 8×8 image (64 pixels): n = 2, 3, 5, 6, 9, 12, 14, 13 for r = 0 … 7.', None),
        ('Equalise the input', '', eq_table(e25['nk'])[0]),
        ('Equalise the target (13, 12, 14, 14, 11, 0, 0, 0)', '', eq_table([13, 12, 14, 14, 11, 0, 0, 0])[0]),
        ('Connect each s to the closest G (tie → smaller z)', 'G rounded = 1, 3, 4, 6, 7, 7, 7, 7 for z = 0 … 7.', table(['s', 'distance to each G', 'z'], [[0, 'G(0) = 1 is closest (distance 1)', '0'], [1, 'G(0) = 1 exactly', '0'], [2, 'G(0) = 1 and G(1) = 3 are both 1 away → <b>tie → smaller z</b>', '0'], [3, 'G(1) = 3', '1'], [4, 'G(2) = 4', '2'], [6, 'G(3) = 6', '3'], [7, 'G(4) = 7 (and 5, 6, 7) → smallest', '4']])),
        ('Rewrite the image', 'r → z: 0→0, 1→0, 2→0, 3→0, 4→1, 5→2, 6→3, 7→4.', gsvg(e25['g'], {}, cell=34, idx=False, label='g(x, y)')),
    ]) + '<div class="ansbig">r → z: 0→0, 1→0, 2→0, 3→0, 4→1, 5→2, 6→3, 7→4, and g as in step 5. (The official key maps 3 → 1, breaking the slide’s tie rule, and has one typo at row 5, column 1.)</div>'))
    for cid in ['o24q2i', 'tb3-10', 'tb3-6', 'tb3-7', 'tb3-11', 'tb3-12', 'dr-stats', 'dr-local']: H.append(card(cid))
    H.append('</section>')
    return '\n'.join(H)
