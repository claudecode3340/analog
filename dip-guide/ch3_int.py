"""Chapter 3.1–3.2 rebuilt: intensity transformations and bit planes — plain words, curves, photos, numbers; bit-plane
past papers as step-by-step walks."""
from ch3lib import *
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
    for cid in ['s19q6', 'tb3-1', 'dr-thresh', 'dr-log']: H.append(card(cid))

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
        ('Keep the top 3 bit planes', 'Top 3 planes = keep the first three binary digits (worth 128, 64, 32) and set the rest to 0. Same as 32 × (value ÷ 32 with decimals dropped).<br>' + '<br>'.join(f'{v} = {format(v, "08b")} → {format(v, "08b")[:3]}00000 = <b>{t}</b>' for v, t in zip(q['M'][1], q['row1'])), gsvg(q['top3'], {(1, j): 'hl' for j in range(5)}, cell=50, label='g = the image rebuilt from the top 3 planes')),
        ('Add up row 1', '224 + 32 + 160 + 96 + 64 = <b>576</b>.', None),
    ]) + '<div class="ansbig">Row 1 of g = [224, 32, 160, 96, 64]; Σ g(1, y) = <b>576</b>.</div>'))

    img34 = [[0, 1, 8, 6], [2, 2, 1, 1], [1, 15, 14, 12], [3, 6, 9, 10]]
    p = ANS['p34']
    binv = [[format(v, '04b') for v in r] for r in img34]
    H.append(set_solution(card('tb3-4'), walk([
        ('(a) Method', 'Write every pixel as a 4-bit binary number (4-bit image: values 0 … 15). Plane 4 (MSB, worth 8) is the first digit of every pixel, plane 3 (worth 4) the second, plane 2 (worth 2) the third, plane 1 (LSB, worth 1) the last.', gsvg(binv, {}, cell=64, label='every pixel in binary')),
        ('(b) The four planes', 'Read one digit position from every pixel.', figs(gsvg(p['plane4'], {(i, j): 'hl' for i in range(4) for j in range(4) if p['plane4'][i][j]}, cell=34, idx=False, label='plane 4 (MSB, 8)'), gsvg(p['plane3'], {(i, j): 'hl' for i in range(4) for j in range(4) if p['plane3'][i][j]}, cell=34, idx=False, label='plane 3 (4)'), gsvg(p['plane2'], {(i, j): 'hl' for i in range(4) for j in range(4) if p['plane2'][i][j]}, cell=34, idx=False, label='plane 2 (2)'), gsvg(p['plane1'], {(i, j): 'hl' for i in range(4) for j in range(4) if p['plane1'][i][j]}, cell=34, idx=False, label='plane 1 (LSB, 1)'))),
        ('Check one pixel', '14 = 1110 → planes 4, 3, 2 are 1, plane 1 is 0: 8 + 4 + 2 = 14 ✓.', None),
    ]) + '<div class="ansbig">The four 0/1 images shown in step 2 (plane 4 = MSB … plane 1 = LSB).</div>'))

    o = ANS['m24_3']
    o_img = [[7, 6, 1, 0, 2], [5, 5, 2, 3, 1], [4, 3, 1, 0, 2], [2, 3, 4, 7, 7], [1, 2, 4, 6, 6]]
    H.append(set_solution(card('o24q3i'), walk([
        ('Make the Gray-code table once', 'Only 8 values exist (3-bit), so convert each once: g = b XOR (b shifted right). 0→000, 1→001, 2→011, 3→010, 4→110, 5→111, 6→101, 7→100.', None),
        ('Convert every pixel', 'Replace each value by its Gray code (shown as the decimal value of the Gray bits).', figs(gsvg(o_img, {}, cell=40, idx=False, label='the image'), gsvg(o['gray'], {}, cell=40, idx=False, label='its Gray codes (as numbers)'))),
        ('Read the two planes', 'LSB plane = last Gray bit (1 for values 1, 2, 5, 6). MSB plane = first Gray bit = the normal MSB (1 for values 4 … 7).', figs(gsvg(o['lsb'], {(i, j): 'hl' for i in range(5) for j in range(5) if o['lsb'][i][j]}, cell=40, idx=False, label='f_LSB (Gray)'), gsvg(o['msb'], {(i, j): 'hl' for i in range(5) for j in range(5) if o['msb'][i][j]}, cell=40, idx=False, label='f_MSB'))),
    ]) + '<div class="ansbig">f<sub>LSB</sub> and f<sub>MSB</sub> as in step 3. Shortcut: Gray LSB = 1 when the value is 1, 2, 5 or 6; MSB = 1 when the value is 4 or more.</div>'))
    for cid in ['tb3-3', 'tb3-5', 'dr-top', 'e23q3b', 'd25q6']: H.append(card(cid))
    H.append('</section>')
    return '\n'.join(H)
