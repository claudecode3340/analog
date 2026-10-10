"""Chapter 3.1–3.2 rebuilt: intensity transformations and bit planes — plain words, curves, photos, numbers; bit-plane
past papers as step-by-step walks."""
from ch3lib import *
from ch3_hist import stats_cl, DEC
import math

c_log = 255 / math.log10(256)
pw = [(0, 0), (30, 20), (180, 210), (255, 255)]
def pwf(r):
    for (r1, s1), (r2, s2) in zip(pw, pw[1:]):
        if r <= r2: return s1 + (s2 - s1) * (r - r1) / (r2 - r1)
    return 255


def section(card):
    H = ['''<section class="topic" id="ch3-int">
  <div class="eyebrow">Chapter 3.1–3.2 · Lectures 7–8</div>
  <h2>Intensity transformations: changing each pixel’s brightness</h2>
  <div class="meta"><span class="chip ">TB 3.1–3.2</span><span class="chip ">slides pp. 3–14</span><span class="chip hot">Quiz-1 Q2 · bit planes</span></div>
  <p class="lede">An intensity transformation changes every pixel by the <b>same rule</b>, looking only at that pixel’s own value: new value s = T(old value r). It is the simplest kind of image processing — no neighbours involved. You will be asked for: the negative, a log or gamma value, a piecewise-linear (contrast-stretching) transformation, thresholding, slicing, and especially <b>bit planes</b> (including Gray code and “keep the top k planes”).</p>''']

    # 1 the idea and how to read a curve
    H.append(lesson('The idea: a rule s = T(r), drawn as a curve',
        'Because T only looks at one value, it is just a lookup table: for every possible input level r (0 … L − 1) it says the output level s. Drawing that table gives a curve — and the curve tells you at a glance what happens to the image.',
        '<div class="cols"><div>'
        '<p><b>How to read a transformation curve:</b></p><ol class="how">'
        '<li>Input r is on the horizontal axis, output s on the vertical axis. The dashed diagonal is “do nothing” (s = r).</li>'
        '<li>Curve <b>above</b> the diagonal → those pixels get brighter; <b>below</b> → darker.</li>'
        '<li>Where the curve is <b>steeper</b> than the diagonal, nearby grey levels are pushed apart → <b>more contrast</b> in that range. Where it is <b>flatter</b>, levels are squeezed together → less contrast.</li></ol>'
        '<p>Your slides call the general form \\(g(x,y)=T\\{f(j,k)\\mid(j,k)\\in S_{xy}\\}\\) — the output at (x, y) computed from a neighbourhood S<sub>xy</sub>. An intensity transformation is the special case where S<sub>xy</sub> is just the single pixel (1×1).</p>'
        '<p><b>Monotonic</b> (slide term): a curve that never goes down (r₁ &lt; r₂ ⇒ T(r₁) ≤ T(r₂)) keeps the brightness order of pixels. <b>Strictly</b> monotonic (always going up) also never merges two levels into one, so it can be undone.</p>'
        '</div><div>' + figs(tcurve(lambda r: 255 * (r / 255) ** 0.5, 'above the diagonal: brighter, dark parts stretched'), tcurve(lambda r: 255 * (r / 255) ** 2, 'below the diagonal: darker, bright parts stretched')) + '</div></div>',
        tag='1'))

    # 2 the basic transformations
    H.append(lesson('The basic transformations, one by one',
        'Each one has a typical use. Every example below is the same photograph run through the curve next to it.',
        '<div class="mini wide">'
        '<div><h5>Negative: s = L − 1 − r</h5>' + figs(tcurve(lambda r: 255 - r), img('cam_neg', 150)) + '<p>Black ↔ white. 8-bit: r = 200 → s = 255 − 200 = <b>55</b>. Used to see white or grey detail inside dark regions (mammograms).</p></div>'
        '<div><h5>Log: s = c · log(1 + r)</h5>' + figs(tcurve(lambda r: c_log * math.log10(1 + r)), img('cam_log', 150)) + f'<p>Spreads out the dark levels, squeezes the bright ones. Choose c so 255 → 255: c = 255 / log(256) = <b>105.89</b> (with log₁₀). Then r = 10 → 105.89·log₁₀11 = <b>110.3</b>; r = 100 → <b>212.2</b>. Used to display Fourier spectra (values from 0 to millions).</p></div>'
        '<div><h5>Power law (gamma): s = c · r<sup>γ</sup></h5>' + figs(tcurve(lambda r: 255 * (r / 255) ** 0.4, 'γ = 0.4'), tcurve(lambda r: 255 * (r / 255) ** 2.5, 'γ = 2.5')) + figs(img('cam_g04', 130, 'γ = 0.4: brighter'), img('cam_g25', 130, 'γ = 2.5: darker')) + '<p>Work with r scaled to 0 … 1, then multiply back by 255. γ &lt; 1 brightens the dark parts; γ &gt; 1 darkens. Example r = 64: (64/255)<sup>0.4</sup> × 255 = <b>147</b>; (64/255)<sup>2.5</sup> × 255 = <b>8</b>. Used for gamma correction of displays and for MRI contrast (your slide).</p></div>'
        '<div><h5>Linear (affine): s = a·r + b</h5><p>Scale and shift: a &gt; 1 increases contrast, b brightens. Example a = 1.5, b = −20: r = 100 → 130. Values that leave 0 … 255 are clipped.</p></div></div>',
        use='one-line calculations (Quiz style) and “what does this curve do?” questions.', tag='2'))
    H.append('<div class="lab" data-lab="transform" data-init=\'{}\'></div>')

    # 3 piecewise linear
    H.append(lesson('Piecewise-linear transformations: contrast stretching, thresholding, slicing',
        'Instead of a formula, the curve is made of straight pieces joining a few given points. You can then shape exactly which range of greys gets more contrast.',
        '<div class="cols"><div>'
        '<p><b>Contrast stretching</b> through (r₁, s₁) and (r₂, s₂): the middle piece is steep (more contrast between r₁ and r₂), the outer pieces flat.</p>'
        '<ul><li><b>Full stretch</b> (your slide): (r₁, s₁) = (r<sub>min</sub>, 0), (r₂, s₂) = (r<sub>max</sub>, L − 1): the darkest pixel becomes 0, the brightest L − 1. Formula: \\(s=(L-1)\\dfrac{r-r_{min}}{r_{max}-r_{min}}\\).</li>'
        '<li><b>Thresholding</b>: r₁ = r₂ (a vertical jump), s₁ = 0, s₂ = L − 1 → a black-and-white image. Your slide thresholds at the mean intensity.</li>'
        '<li><b>Identity</b>: r₁ = s₁, r₂ = s₂ (nothing changes).</li></ul>'
        '<p><b>Evaluating any broken line (exam method):</b> find which piece r is in; slope = Δs/Δr of that piece; s = s<sub>start</sub> + slope × (r − r<sub>start</sub>). Example with the Mid-sem 2019 points (0,0), (30,20), (180,210), (255,255): r = 100 is in the middle piece, slope 190/150 = 1.267 → s = 20 + 1.267 × 70 = <b>108.67</b>.</p>'
        '<p><b>Low contrast comes from</b> poor lighting, a sensor with little dynamic range, or a wrong lens aperture (your slide).</p>'
        '</div><div>' + figs(tcurve(pwf, 'the Mid-sem 2019 broken line', pts=[(30, 20, '(30,20)'), (180, 210, '(180,210)')]), tcurve(lambda r: 255 if r >= 128 else 0, 'thresholding at 128')) +
        figs(img('cam_low', 130, 'low contrast'), img('cam_stretch', 130, 'after full stretch'), img('cam_thresh', 130, 'thresholded at the mean')) + '</div></div>'
        '<h4 style="margin-top:16px">Intensity-level slicing: highlight one range of greys</h4>'
        '<div class="cols"><div><ul><li><b>Binary slicing</b>: one value (e.g. white) for the range of interest [A, B], another (black) for everything else.</li>'
        '<li><b>With background preserved</b>: brighten (or darken) only [A, B]; every other level stays as it was.</li></ul><p>Your slide’s example: highlighting the blood vessels in an aortic angiogram.</p></div>'
        '<div>' + figs(tcurve(lambda r: 255 if 100 <= r <= 160 else 40, 'binary slicing of 100–160'), tcurve(lambda r: 255 if 100 <= r <= 160 else r, 'background preserved'), img('cam_slice2', 130, 'background preserved')) + '</div></div>',
        use='Mid-sem 2019 Q6 (the broken line), textbook 3.1 (full stretch), Compre 2025 Q6 (thresholds), slicing theory.', tag='3'))
    H.append(set_solution(card('s19q6'), walk([
        ('Slope of each piece', 'Slope = Δs/Δr: piece 1 (0 → 30): 20/30 = 2/3; piece 2 (30 → 180): 190/150 = 19/15 ≈ 1.2667; piece 3 (180 → 255): 45/75 = 0.6. So T(r) = ⅔r for r ≤ 30; 20 + (19/15)(r − 30) for 30 &lt; r ≤ 180; 210 + 0.6(r − 180) above.', tcurve(pwf, 'the broken line', pts=[(30, 20, '(30,20)'), (180, 210, '(180,210)')]),
         cl(K('190', '÷', '150', 'EXE'), 'middle slope; screen shows 19/15 → FORMAT → Decimal → 1.266666667')
         + cl(K('45', '÷', '75', 'EXE'), 'top slope; screen shows 3/5 = 0.6')),
        ('T(10): first piece', '10 ≤ 30, so s = ⅔ × 10 = <b>6.67 → 7</b>.', None,
         cl(K('2', '÷', '3', '×', '10', 'EXE'), 'screen shows 20/3 → FORMAT → Decimal → 6.666666667')),
        ('T(100): middle piece', '30 &lt; 100 ≤ 180: s = 20 + 1.2667 × (100 − 30) = <b>108.67 → 109</b>.', None,
         cl(K('20', '+', '19', '÷', '15', '×', '(', '100', '−', '30', ')', 'EXE'), 'start of the piece + slope × distance into the piece; screen shows 326/3 → Decimal 108.6666667')),
        ('T(200): last piece', '200 &gt; 180: s = 210 + 0.6 × 20 = <b>222</b>.', None,
         cl(K('210', '+', '0.6', '×', '(', '200', '−', '180', ')', 'EXE'), 'screen shows 222')),
        ('What it does', 'A <b>contrast stretch</b>: the middle range 30–180 has slope &gt; 1 (more contrast), the dark (0–30) and bright (180–255) ends have slope &lt; 1 (compressed).', None,
         cl(K('HOME', '>Table'), 'optional, for many values at once: in the Table app use TOOLS → Define f(x)/g(x) → Define f(x), f(x) = 20 + 19÷15×(x − 30), table from 30 to 180 step 10 → every middle-piece value in one list')),
    ]) + '<div class="ansbig">Slopes 2/3, 19/15 ≈ 1.267, 3/5. T(10) = 6.67 → 7, T(100) = 108.67 → 109, T(200) = 222. A contrast stretch of the mid-range 30–180.</div>'))
    H.append(card('tb3-1'))
    q21i = [[4, 2, 3, 2, 5], [1, 1, 2, 3, 4], [1, 3, 2, 3, 4], [2, 2, 3, 1, 3], [2, 2, 1, 1, 4]]
    th = [[7 if v >= 3 else 0 for v in r] for r in q21i]
    H.append(set_solution(card('dr-thresh'), walk([
        ('Mean of the image', 'Counts: 1 × 6, 2 × 8, 3 × 6, 4 × 4, 5 × 1 (25 pixels). Mean = 61/25 = <b>2.44</b>.', gsvg(q21i, {}, cell=36, idx=False, label='the 5×5 image'),
         stats_cl(range(1, 6), [6, 8, 6, 4, 1], 25)),
        ('Apply the threshold', 'r₁ = r₂ = 2.44: a pixel above the mean becomes L − 1 = 7, below it becomes 0. No pixel equals 2.44, so every 3, 4, 5 → <b>7</b> and every 1, 2 → 0.', gsvg(th, {(i, j): 'hl' for i in range(5) for j in range(5) if th[i][j]}, cell=36, idx=False, label='thresholded')),
    ]) + '<div class="ansbig">Mean = 61/25 = 2.44 → every pixel with value ≥ 3 becomes 7, the rest 0.</div>'))
    H.append(set_solution(card('dr-log'), walk([
        ('(a) Choose c so 255 → 255', 'c · log₁₀(1 + 255) = 255 → c = 255 / log₁₀ 256 = <b>105.89</b>. (With ln: 45.99 — same mapping; the base does not matter once c is fixed.)', tcurve(lambda r: c_log * math.log10(1 + r), 's = c·log(1 + r)'),
         cl(K('255', '÷', 'SHIFT', 'x²', '256', ')', 'EXE'), 'SHIFT x² is log₁₀; screen shows 105.886458')
         + cl(K('VARIABLE', '>A=', '>Store'), 'stores c in A so you never retype it')
         + cl(K('255', '÷', 'SHIFT', 'log■□', '256', ')', 'EXE'), 'optional: the ln version, 45.98590443')),
        ('(a) s for r = 100', 's = 105.89 × log₁₀(101) = <b>212.2</b>: a dark level 100 is pushed far up.', None,
         cl(K('A', '×', 'SHIFT', 'x²', '101', ')', 'EXE'), 'c × log(1 + r); screen shows 212.230491')),
        ('(b) γ = 0.4 on r = 0.5', '0.5<sup>0.4</sup> = <b>0.758</b> &gt; 0.5 → brighter (× 255 ≈ 193).', tcurve(lambda r: 255 * (r / 255) ** 0.4, 'γ = 0.4'),
         cl(K('0.5', 'x^■', '0.4', 'EXE'), 'r<sup>γ</sup>; screen shows 0.7578582833')
         + cl(K('Ans', '×', '255', 'EXE'), 'back to 8-bit: 193.2538622')),
        ('(b) γ = 2.5 on r = 100/255', '(100/255)<sup>2.5</sup> = <b>0.0963</b> &lt; 0.392 → darker (× 255 ≈ 24.6).', tcurve(lambda r: 255 * (r / 255) ** 2.5, 'γ = 2.5'),
         cl(K('(', '100', '÷', '255', ')', 'x^■', '2.5', 'EXE'), 'normalise first, then the power; screen shows 0.09630515818')
         + cl(K('Ans', '×', '255', 'EXE'), 'back to 8-bit: 24.55781534')),
    ]) + '<div class="ansbig">(a) c = 255/log₁₀256 = 105.89; s(100) = 212.2. (b) 0.5<sup>0.4</sup> = 0.758 → brighter (≈ 193); (100/255)<sup>2.5</sup> = 0.0963 → darker (≈ 24.6).</div>'))

    # 4 bit planes
    H.append(lesson('Bit planes: splitting an image by binary digit',
        'Every pixel is stored as a binary number. An 8-bit pixel has 8 binary digits; take the same digit from every pixel and you get a black-and-white image called a <b>bit plane</b>. Plane 7 (the most significant bit, MSB) is worth 128, plane 0 (the least significant bit, LSB) is worth 1.',
        '<div class="cols"><div>'
        '<p><b>Example.</b> 214 = 128 + 64 + 16 + 4 + 2 = <b>1101 0110</b>. So this pixel is 1 in planes 7, 6, 4, 2, 1 and 0 in planes 5, 3 and 0 (read the digits left to right as planes 7 … 0).</p>'
        '<p><b>Bit k of r without converting the whole number:</b> divide r by 2<sup>k</sup>, drop the decimals; if the result is odd, bit k is 1. Example bit 4 of 214: 214/16 = 13.4 → 13 is odd → 1.</p>'
        '<p><b>Rebuild the image:</b> r = Σ 2<sup>k</sup> × (plane k). Keeping only the <b>top t planes</b> = keep the top t binary digits, set the rest to 0 = 2<sup>8−t</sup> × ⌊r / 2<sup>8−t</sup>⌋. Example top 3 planes of 214: 32 × ⌊214/32⌋ = 32 × 6 = <b>192</b> (1100 0000).</p>'
        '<p><b>Why bother?</b> The top planes carry the visible structure, the bottom planes look like noise. Keeping only the top 4 planes already looks almost like the original — 50 % less storage (your slide’s compression question).</p>'
        '</div><div>' + figs(img('cam_plane7', 120, 'plane 7 (MSB)'), img('cam_plane6', 120, 'plane 6'), img('cam_plane5', 120, 'plane 5'), img('cam_plane4', 120, 'plane 4'), img('cam_plane0', 120, 'plane 0 (LSB): noise-like')) + figs(img('cam_top2', 150, 'top 2 planes'), img('cam_top3', 150, 'top 3 planes'), img('cam', 150, 'all 8 planes')) + '</div></div>'
        '<h4 style="margin-top:16px">Gray code (asked in Mid-sem Oct 2024)</h4>'
        '<div class="cols"><div><p>In Gray code, neighbouring values differ in exactly <b>one</b> bit, so a tiny change in brightness flips only one bit plane. Rule: g = b XOR (b shifted right by one place). XOR gives 1 where the two bits differ.</p>'
        '<p><b>Example</b> 6 = 110: shifted = 011; 110 XOR 011 = <b>101</b>. The Gray MSB always equals the normal MSB.</p></div><div>' +
        table(['value', 'binary', 'Gray code'], [[v, format(v, '03b'), format(v ^ (v >> 1), '03b')] for v in range(8)]) + '</div></div>',
        use='Quiz-1 2026 Q2 (top 3 planes, sum of a row), textbook 3.4 (all planes of a 4-bit image), Mid-sem Oct 2024 Q3(i) (LSB/MSB with Gray code).', tag='4'))
    H.append('<div class="lab" data-lab="bits" data-init=\'{}\'></div>')

    H.append('<h3 id="ch3-int-q">Questions on intensity transformations and bit planes</h3>')
    q = ANS['q26_2']
    orig1 = ['223.78', '45.3', '166.9', '95.87', '71.4']
    H.append(set_solution(card('qz2'), walk([
        ('Quantise to 8 bits = round every value', 'Each value is rounded to the nearest whole number 0 … 255. Row 1 (the second row, counted from 0): ' + ', '.join(f'{a} → {b}' for a, b in zip(orig1, q['M'][1])) + '.', gsvg(q['M'], {(1, j): 'hl' for j in range(5)}, cell=50, label='after rounding; row 1 highlighted')),
        ('Keep the top 3 bit planes', 'Top 3 planes = keep the first three binary digits (worth 128, 64, 32) and set the rest to 0. Same as 32 × (value ÷ 32 with decimals dropped).<br>' + '<br>'.join(f'{v} = {format(v, "08b")} → {format(v, "08b")[:3]}00000 = <b>{t}</b>' for v, t in zip(q['M'][1], q['row1'])), gsvg(q['top3'], {(1, j): 'hl' for j in range(5)}, cell=50, label='g = the image rebuilt from the top 3 planes'),
         ''.join(cl(K(str(v), '÷', '32', 'EXE'), f'{v} ÷ 32 = ' + (f'{v // 32}' if v % 32 == 0 else f'{v / 32:g}') + f' → drop decimals → {v // 32} → × 32 = <b>{t}</b>' + (' (FORMAT → Decimal if a fraction appears)' if k == 1 else '')) for k, (v, t) in enumerate(zip(q['M'][1], q['row1'])))
         + cl(K('HOME', '>Base-N', 'OK'), 'optional check: type 167 in Dec, press FORMAT until Bin → 10100111; top three digits 101 → 10100000 = 160 ✓')),
        ('Add up row 1', '224 + 32 + 160 + 96 + 64 = <b>576</b>.', None,
         cl(K('224', '+', '32', '+', '160', '+', '96', '+', '64', 'EXE'), 'screen shows 576')),
    ]) + '<div class="ansbig">Row 1 of g = [224, 32, 160, 96, 64]; Σ g(1, y) = <b>576</b>.</div>'))

    img34 = [[0, 1, 8, 6], [2, 2, 1, 1], [1, 15, 14, 12], [3, 6, 9, 10]]
    p = ANS['p34']
    binv = [[format(v, '04b') for v in r] for r in img34]
    H.append(set_solution(card('tb3-4'), walk([
        ('(a) Method', 'Write every pixel as a 4-bit binary number (4-bit image: values 0 … 15). Plane 4 (MSB, worth 8) is the first digit of every pixel, plane 3 (worth 4) the second, plane 2 (worth 2) the third, plane 1 (LSB, worth 1) the last.', gsvg(binv, {}, cell=64, label='every pixel in binary'),
         cl(K('HOME', '>Base-N', 'OK'), 'opens Base-N in Dec')
         + cl(K('14', 'EXE', 'FORMAT'), 'type a value, press FORMAT until Bin: 14 → 1110; read the last 4 digits (leading zeros are just more 0s)')
         + cl('repeat for 15, 12, 9, 10, 8, 6, 3', '15 = 1111, 12 = 1100, 9 = 1001, 10 = 1010, 8 = 1000, 6 = 0110, 3 = 0011 — the small ones (0, 1, 2) you know by heart')),
        ('(b) The four planes', 'Read one digit position from every pixel.', figs(gsvg(p['plane4'], {(i, j): 'hl' for i in range(4) for j in range(4) if p['plane4'][i][j]}, cell=34, idx=False, label='plane 4 (MSB, 8)'), gsvg(p['plane3'], {(i, j): 'hl' for i in range(4) for j in range(4) if p['plane3'][i][j]}, cell=34, idx=False, label='plane 3 (4)'), gsvg(p['plane2'], {(i, j): 'hl' for i in range(4) for j in range(4) if p['plane2'][i][j]}, cell=34, idx=False, label='plane 2 (2)'), gsvg(p['plane1'], {(i, j): 'hl' for i in range(4) for j in range(4) if p['plane1'][i][j]}, cell=34, idx=False, label='plane 1 (LSB, 1)'))),
        ('Check one pixel', '14 = 1110 → planes 4, 3, 2 are 1, plane 1 is 0: 8 + 4 + 2 = 14 ✓.', None),
    ]) + '<div class="ansbig">The four 0/1 images shown in step 2 (plane 4 = MSB … plane 1 = LSB).</div>'))

    o = ANS['m24_3']
    o_img = [[7, 6, 1, 0, 2], [5, 5, 2, 3, 1], [4, 3, 1, 0, 2], [2, 3, 4, 7, 7], [1, 2, 4, 6, 6]]
    H.append(set_solution(card('o24q3i'), walk([
        ('Make the Gray-code table once', 'Only 8 values exist (3-bit), so convert each once: g = b XOR (b shifted right). 0→000, 1→001, 2→011, 3→010, 4→110, 5→111, 6→101, 7→100.', table(['b', 'binary', 'b shifted right', 'Gray = XOR'], [[v, format(v, '03b'), format(v >> 1, '03b'), format(v ^ (v >> 1), '03b')] for v in range(8)]),
         cl(K('HOME', '>Base-N', 'OK'), 'opens Base-N; press FORMAT until Bin so you type and read binary')
         + cl(K('110', 'CATALOG', '>Logic Operation', '>xor', '11', 'EXE'), 'Gray code of 6: 110 XOR 011 (6 shifted right = 3 = 11); screen shows 101')
         + cl('repeat for the other 7 values', 'only 8 values exist, so make the table once and read every pixel from it')),
        ('Convert every pixel', 'Replace each value by its Gray code (shown as the decimal value of the Gray bits).', figs(gsvg(o_img, {}, cell=40, idx=False, label='the image'), gsvg(o['gray'], {}, cell=40, idx=False, label='its Gray codes (as numbers)'))),
        ('Read the two planes', 'LSB plane = last Gray bit (1 for values 1, 2, 5, 6). MSB plane = first Gray bit = the normal MSB (1 for values 4 … 7).', figs(gsvg(o['lsb'], {(i, j): 'hl' for i in range(5) for j in range(5) if o['lsb'][i][j]}, cell=40, idx=False, label='f_LSB (Gray)'), gsvg(o['msb'], {(i, j): 'hl' for i in range(5) for j in range(5) if o['msb'][i][j]}, cell=40, idx=False, label='f_MSB'))),
    ]) + '<div class="ansbig">f<sub>LSB</sub> and f<sub>MSB</sub> as in step 3. Shortcut: Gray LSB = 1 when the value is 1, 2, 5 or 6; MSB = 1 when the value is 4 or more.</div>'))
    for cid in ['tb3-3', 'tb3-5']: H.append(card(cid))
    H.append(set_solution(card('dr-top'), walk([
        ('(a) 214 in binary', '214 = 128 + 64 + 16 + 4 + 2 = <b>1101 0110</b>.', None,
         cl(K('HOME', '>Base-N', 'OK'), 'opens Base-N; type 214 in Dec')
         + cl(K('214', 'EXE', 'FORMAT'), 'press FORMAT until Bin is shown: the screen reads 11010110 (ignore leading zeros)')),
        ('(b) Keep the top t planes', 'Keep the first t binary digits, set the rest to 0: top 2 → 11 000000 = <b>192</b>; top 3 → 110 00000 = <b>192</b> (the third digit is 0); top 4 → 1101 0000 = <b>208</b>.', None,
         cl(K('214', 'CATALOG', '>Logic Operation', '>and', '224', 'EXE'), 'AND with the mask 11100000 (= 224) keeps only the top 3 digits → 192; mask 192 for top 2 → 192, mask 240 for top 4 → 208')
         + cl(K('214', '÷', '16', 'EXE'), 'without Base-N (top 4): 214 ÷ 2<sup>4</sup> = 13.375 → drop decimals → 13 × 16 = 208')),
        ('(c) Rebuild and compression', 'Rebuild: r = Σ 2<sup>k</sup> · b<sub>k</sub> — multiply plane k by 2<sup>k</sup> and add. Compression: keeping only the top 4 planes stores 4 of 8 bits (≥ 50 % saving) and still looks almost the same, because the top planes carry the visible structure.', None),
    ]) + '<div class="ansbig">(a) 214 = 11010110. (b) top 2 → 192; top 3 → 192; top 4 → 208. (c) r = Σ 2<sup>k</sup>b<sub>k</sub>; top 4 planes ≈ same picture at half the bits.</div>'))
    for cid in ['e23q3b', 'd25q6']: H.append(card(cid))
    H.append('</section>')
    return '\n'.join(H)
