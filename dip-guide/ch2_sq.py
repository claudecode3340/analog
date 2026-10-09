"""Chapter 2.4 rebuilt: sampling and quantisation, storage, spatial and intensity resolution, the matrix/linear index,
interpolation — each idea with plain words, numbers and a picture; Quiz-1 Q6 as a step-by-step walk."""
from lib import *
import re


def svgfigs(old):
    out = []
    for m in re.finditer(r'<div class="svgfig">', old):
        a, b = extract_div(old, m.start()); out.append(old[a:b])
    return out


def section(card, old):
    figs_old = svgfigs(old)
    samp = figs_old[0] if figs_old else ''
    bil = figs_old[1] if len(figs_old) > 1 else ''
    H = ['''<section class="topic" id="ch2-sq">
  <div class="eyebrow">Chapter 2.4 · Lectures 4–5</div>
  <h2>Sampling, quantisation, storage and interpolation</h2>
  <div class="meta"><span class="chip ">TB 2.4</span><span class="chip ">slides pp. 20–28</span><span class="chip hot">Quiz-1 Q6 type</span></div>
  <p class="lede">A camera sees a smooth, continuous scene. A computer can only store a <b>grid of numbers</b>. This section is about that conversion: where we measure (sampling), how finely we round the brightness (quantisation), how much memory the result takes, how to point at one pixel, and how to invent values <b>between</b> pixels when an image is enlarged or rotated (interpolation). Exam questions: storage and transmission time, linear index, bilinear interpolation of new pixels (Quiz-1 Q6), and older papers’ rms quantisation error.</p>''']

    # 1 sampling and quantisation
    H.append(lesson('Digitising = sampling + quantisation',
        'Two separate roundings turn a smooth picture into a digital image: <b>sampling</b> decides <b>where</b> we measure (only at a grid of points), <b>quantisation</b> decides <b>how precisely</b> we store each measured brightness (only L allowed levels).',
        '<div class="cols"><div>'
        '<p><b>Sampling</b> = measuring the brightness only at equally spaced points. More points per inch → finer detail (spatial resolution).</p>'
        '<p><b>Quantisation</b> = rounding each measured value to the nearest of L allowed grey levels 0, 1, …, L − 1. More levels → smoother shading (intensity resolution).</p>'
        '<p><b>Example.</b> A sensor reads brightness 0.537 on a 0 … 1 scale. With 3 bits there are 8 levels, 0/7, 1/7, …, 7/7. The nearest is 4/7 = 0.571, so the pixel is stored as <b>4</b>. The small difference (0.034) is the quantisation error.</p>'
        '</div><div>' + samp + '</div></div>',
        use='theory questions (“define sampling and quantisation”), and every storage and resolution calculation below.', tag='1'))

    # 2 storage
    H.append(lesson('How many levels, how many bits, how much memory',
        'With k bits per pixel you can count 2<sup>k</sup> different grey levels. The memory for the whole image is simply (number of pixels) × (bits per pixel).',
        '<div class="cols"><div>'
        '<div class="formula">\\(L=2^k\\) levels: 0, 1, …, L − 1<span class="say">k = 1 → 2 levels (black/white), k = 3 → 8, k = 8 → 256.</span></div>'
        '<div class="formula">\\(b=M\\times N\\times k\\) bits<span class="say">rows × columns × bits per pixel; ÷ 8 for bytes.</span></div>'
        '<p><b>Example.</b> A 1024 × 1024 image with 256 grey levels: k = 8, so b = 1024 × 1024 × 8 = 8,388,608 bits = 1,048,576 bytes = <b>1 MB</b>.</p>'
        '<p><b>Transmission time</b> = (all bits to send) ÷ (bits per second). If each 8-bit byte travels with a start bit and a stop bit, every pixel costs 10 bits (textbook 2.9).</p>'
        '</div><div>' + table(['k (bits)', 'L = 2^k levels', 'brightest value'], [[1, 2, 1], [2, 4, 3], [3, 8, 7], [4, 16, 15], [5, 32, 31], [8, 256, 255]]) + '</div></div>',
        use='Quiz-type “how many bits / how long to send” questions, and knowing L − 1 for every histogram and negative question.', tag='2'))

    # 3 spatial resolution
    H.append(lesson('Spatial resolution: how fine is the grid?',
        'Spatial resolution is the smallest detail you can see. It is measured as <b>dots (pixels) per inch</b> (dpi) or <b>line pairs per mm</b> (one dark + one light line = 2 pixels).',
        '<div class="cols"><div>'
        '<p>The same photo stored with fewer and fewer samples (all shown at the same size): detail disappears and edges become blocky.</p>'
        '<p><b>Typical values (your slide):</b> newspapers 150–200 dpi, books 300 dpi, art books 300–600 dpi.</p>'
        '<p><b>Example (textbook 2.5).</b> 2048 pixels must fit across 5 cm = 50 mm → 2048/50 = 40.96 pixels per mm = <b>20.48 line pairs per mm</b>. To fit 2048 pixels in 2 inches → <b>1024 dpi</b>.</p>'
        '</div><div>' + figs(img('cam', 150, '256 × 256'), img('cam_64', 150, '64 × 64'), img('cam_32', 150, '32 × 32')) + '</div></div>',
        tag='3'))

    # 4 intensity resolution
    H.append(lesson('Intensity resolution and false contouring',
        'Intensity resolution is the smallest change in brightness you can store. With too few levels, a smooth gradual change of brightness turns into visible flat <b>bands</b> with sudden steps — this artefact is called <b>false contouring</b>.',
        '<div class="cols"><div>'
        '<p>The same photo with 8, 4, 2 and 1 bits per pixel. At 4 bits and below the smooth sky breaks into bands (your slide: false contouring appears with 4 or fewer bits).</p>'
        '<p><b>Why:</b> with k bits each step between neighbouring levels is 256/2<sup>k</sup> of the 8-bit range. At 4 bits a step is 16 levels — big enough for the eye to see as an edge. (Textbook 2.12: if the eye notices steps bigger than 8 levels, contours appear for k ≤ 4.)</p>'
        '</div><div>' + figs(img('cam_bits8', 128, '8 bits (256 levels)'), img('cam_bits4', 128, '4 bits (16)'), img('cam_bits2', 128, '2 bits (4)'), img('cam_bits1', 128, '1 bit (2)')) + figs(img('ramp_bits8', 300, 'a smooth ramp, 8 bits'), img('ramp_bits3', 300, 'the same ramp, 3 bits: 8 flat bands')) + '</div></div>',
        tag='4'))

    # 5 indexing
    m, n = 3, 4
    alpha = [[m * y + x for y in range(n)] for x in range(m)]
    H.append(lesson('Pointing at a pixel: f(x, y), M<sub>f</sub>(i, j) and the linear index α',
        'There are three ways to name the same pixel, and your instructor uses all three. Mixing them up is the most common way to lose marks on an otherwise correct answer.',
        '<div class="cols"><div>'
        '<ul><li><b>f(x, y)</b>: x = row (going down), y = column (going right), <b>both counted from 0</b>. f(0, 0) is the top-left pixel.</li>'
        '<li><b>M<sub>f</sub>(i, j)</b>: the same image as a matrix, but <b>counted from 1</b> like normal maths matrices. So M<sub>f</sub>(i, j) = f(i − 1, j − 1). In Quiz-1, “M<sub>g</sub>(2, 2)” meant g at the second row and second column = position (½, ½) of the enlarged grid.</li>'
        '<li><b>α</b> (linear index): number the pixels one after another <b>going down each column</b>, then the next column (like MATLAB). With m rows: <b>α = m·y + x</b>.</li></ul>'
        '<p><b>Example</b> (picture: m = 3 rows, n = 4 columns). Pixel f(2, 1): α = 3·1 + 2 = <b>5</b>. Going back from α = 10: y = 10 ÷ 3 without the remainder = 3, x = remainder = 1 → f(1, 3).</p>'
        '</div><div>' + gsvg(alpha, {(2, 1): 'hl'}, label='each cell shows its α (column by column); highlighted: f(2, 1), α = 5') + '</div></div>',
        use='Quiz-1 2026 Q6 (“report M<sub>g</sub>(2,2)”) and Q3 (“F(1,1) = M<sub>F</sub>(2,2)”). Always read twice whether an index is from 0 or from 1.', tag='5'))

    # 6 interpolation
    H.append(lesson('Interpolation: inventing values between pixels',
        'When an image is enlarged, rotated or registered, the new pixel positions usually fall <b>between</b> the original pixels, where nothing was measured. Interpolation estimates a value there from the nearby known pixels.',
        '<div class="cols"><div>'
        '<p><b>Nearest neighbour</b>: copy the value of the closest pixel. Fast, but blocky.</p>'
        '<p><b>Bilinear</b>: a weighted average of the <b>4</b> surrounding pixels; the closer a pixel, the larger its weight. Smooth, a little blurry. Model: g = a·s + b·t + c·s·t + d.</p>'
        '<p><b>Bicubic</b>: uses the <b>16</b> surrounding pixels; sharpest, used in Photoshop.</p>'
        '<div class="formula">\\(g=(1-s)(1-t)\\,A+(1-s)\\,t\\,B+s\\,(1-t)\\,C+s\\,t\\,D\\)<span class="say">A = top-left, B = top-right, C = bottom-left, D = bottom-right pixel; s = how far down (0 … 1), t = how far across (0 … 1). Each weight is the area of the rectangle opposite that corner.</span></div>'
        '<p><b>Example.</b> A = 10, B = 20, C = 40, D = 50.<br>Exact centre (s = t = ½): every weight is ¼ → (10 + 20 + 40 + 50)/4 = <b>30</b>.<br>On the top edge midway (s = 0, t = ½): only A and B count → (10 + 20)/2 = <b>15</b>.<br>At s = 0.25, t = 0.5: 0.375·10 + 0.375·20 + 0.125·40 + 0.125·50 = <b>22.5</b>.</p>'
        '</div><div>' + bil + figs(img('interp_nearest', 150, 'nearest: blocky'), img('interp_bilinear', 150, 'bilinear: smooth'), img('interp_bicubic', 150, 'bicubic: sharpest')) +
        '<p style="font-size:.95rem;color:var(--muted)">A 64×64 image enlarged 4× three ways.</p></div></div>'
        '<p><b>How zooming works (your slide’s toy example):</b> to enlarge 500×500 to 1000×1000, imagine a 1000×1000 grid, shrink it so it lies exactly over the original image, give every grid point a value by interpolation, then stretch the grid back to full size.</p>',
        use='Quiz-1 2026 Q6 (enlarge a 4×3 image to 7×5, report one new pixel). At the exact centre the bilinear answer is just the average of the four corners.', tag='6'))
    H.append('<div class="lab" data-lab="interp" data-init=\'{"f": [[10, 20, 30], [40, 50, 60], [70, 80, 90], [100, 110, 120]], "pt": "0.5 0.5", "title": "Interpolation lab: any point, its weights, and the 2× enlargement"}\'></div>')

    H.append('<h3 id="ch2-sq-q">Questions on sampling, storage and interpolation</h3>')
    H.append(card('ex-lin'))
    big = [[10, 15, 20, 25, 30], [25, 30, 35, 40, 45], [40, 45, 50, 55, 60], [55, 60, 65, 70, 75], [70, 75, 80, 85, 90], [85, 90, 95, 100, 105], [100, 105, 110, 115, 120]]
    orig = {(i, j): 'in' for i in range(0, 7, 2) for j in range(0, 5, 2)}
    hz = {(i, j): 'n4' for i in range(0, 7, 2) for j in range(1, 5, 2)}
    vt = {(i, j): 'nd' for i in range(1, 7, 2) for j in range(0, 5, 2)}
    ct = {(i, j): 'n8' for i in range(1, 7, 2) for j in range(1, 5, 2)}
    q = card('qz6')
    q = set_solution(q, walk([
        ('Draw the enlarged grid', 'Insert a new row between every two rows and a new column between every two columns: 4×3 becomes 7×5. Blue = the 12 original pixels (unchanged). The new pixels are of three kinds.', gsvg([[v if (i % 2 == 0 and j % 2 == 0) else '?' for j, v in enumerate(r)] for i, r in enumerate(big)], {**orig, **hz, **vt, **ct}, cell=42, label='blue original · green between two across · red between two down · purple between four')),
        ('Translate the index', 'M<sub>g</sub>(2, 2) is counted <b>from 1</b>: second row, second column of the 7×5 grid. That is a purple pixel — between f(0,0), f(0,1), f(1,0), f(1,1) — at original-grid position (½, ½).', None),
        ('Bilinear through the four corners', 'Fit g = a x + b y + c x y + d through the four corners: (0,0) → 10 gives d = 10; (0,1) → 20 gives b = 10; (1,0) → 40 gives a = 30; (1,1) → 50 gives 30 + 10 + c + 10 = 50, so c = 0.', None),
        ('Evaluate at (½, ½)', 'g = 30·½ + 10·½ + 0 + 10 = 15 + 5 + 10 = <b>30</b>. (Shortcut: at the exact centre bilinear = average of the four corners = (10 + 20 + 40 + 50)/4 = 30.)', gsvg(big, {**orig, (1, 1): 'hl'}, cell=42, label='the whole enlarged image; highlighted: M_g(2,2) = 30')),
    ]) + '<div class="ansbig">M<sub>g</sub>(2, 2) = g(½, ½) = <b>30</b>.</div>')
    H.append(q)
    H.append(card_raw_tb25())
    for cid in ['tb2-9', 'dr-store', 'tb2-10', 'tb2-12']: H.append(card(cid))

    H.append(lesson('Quantisation error (older papers): rms error and rms SNR',
        'After quantisation every pixel is a little off. The <b>rms error</b> summarises how far off on average; the <b>rms signal-to-noise ratio</b> compares the size of the signal with the size of that error.',
        '<div class="cols"><div><ol class="how"><li>Quantise each value (4 bits on 0 … 255: keep the multiple of 16 just below it, i.e. drop the last 4 bits).</li><li>Error e = quantised − original for each pixel.</li><li><b>rms error</b> = √(average of e²).</li><li><b>rms SNR</b> = √( Σ quantised² ÷ Σ e² ).</li></ol></div>'
        '<div><p><b>Mini example:</b> values 37 and 250 → quantised 32 and 240 → errors −5, −10 → e² = 25, 100 → rms error = √(125/2) = <b>7.91</b>; SNR = √((32² + 240²)/125) = √(58624/125) = <b>21.66</b>.</p><p>State your quantiser in one line (truncation to multiples of 16, or mid-point +8) — the answer depends on it.</p></div></div>',
        use='Mid-sem 2018-19 Q6 and Mid-sem 2023 Q3 (both older instructor).', tag='7'))
    for cid in ['s18q6', 'm23q3']: H.append(card(cid))
    H.append('</section>')
    return '\n'.join(H)


def card_raw_tb25():
    return card_new('tb2-5', 'Textbook 2.5', 'Line pairs per mm and dots per inch for a 2048 × 2048 image',
        'A 2048 × 2048 image must be printed (a) in a 5 cm × 5 cm space: what resolution in line pairs per mm is needed? (b) in 2 × 2 inches: how many dpi?',
        '(a) 2048 pixels ÷ 50 mm = 40.96 pixels/mm → <b>20.48 line pairs/mm</b>. (b) 2048 ÷ 2 = <b>1024 dpi</b>.',
        kind='tb', secs=120,
        steps=['5 cm = 50 mm. Pixels per mm = 2048 ÷ 50 = 40.96.', 'A line pair is one dark and one light line = 2 pixels → 40.96 ÷ 2 = 20.48 line pairs per mm.', 'Dots per inch = 2048 pixels ÷ 2 inches = 1024.'],
        mis=['Forgetting that a line pair is 2 pixels.'])


from lib import card as card_new  # the card builder (the section’s “card” argument fetches existing cards)
