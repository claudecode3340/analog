"""Chapter 4, first half, rebuilt: convolution (linear / circular), Fourier transforms and sampling, the 1-D DFT.
Plain-words lessons with small worked numbers and pictures; past papers as step-by-step walks."""
import re
import numpy as np
from ch3lib import *

W4 = {0: '1', 1: '−i', 2: '−1', 3: 'i'}


def cf(z, d=4):
    z = complex(z); a, b = round(z.real, d) + 0.0, round(z.imag, d) + 0.0
    if abs(b) < 1e-9: return fmt(a)
    if abs(a) < 1e-9: return ('−' if b < 0 else '') + (fmt(abs(b)) if abs(abs(b) - 1) > 1e-9 else '') + 'i'
    return f'{fmt(a)} {"−" if b < 0 else "+"} {fmt(abs(b)) if abs(abs(b) - 1) > 1e-9 else ""}i'


def row(vals, cls=None, label=None, cell=46):
    return gsvg([[v if isinstance(v, str) else fmt(v) for v in vals]], {(0, j): c for j, c in (cls or {}).items()}, cell=cell, idx=False, label=label)


def rows(vals, cls=None, label=None, cell=46):
    return gsvg([[v if isinstance(v, str) else fmt(v) for v in r] for r in vals], cls or {}, cell=cell, idx=False, label=label)


def old_lab(old, kind, n=0):
    m = re.findall(r'<div class="lab" data-lab="%s" data-init=\'[^\']*\'></div>' % kind, old)
    return m[n] if len(m) > n else f'<div class="lab" data-lab="{kind}" data-init=\'{{}}\'></div>'


def old_block(old, start):
    i = old.find(start)
    if i < 0: return ''
    a, b = extract_div(old, i); return old[a:b]


def old_details(old):
    i = old.find('<details class="slides">')
    if i < 0: return ''
    return old[i:old.find('</details>', i) + 10]


# ═══════════════════════════ 4.2 convolution ═══════════════════════════
def conv(card, old):
    H = ['''<section class="topic" id="ch4-conv">
  <div class="eyebrow">Chapter 4.2 · Lectures 12–13</div>
  <h2>Impulses and convolution: linear and circular</h2>
  <div class="meta"><span class="chip ">TB 4.2</span><span class="chip ">slides pp. 3–12</span><span class="chip hot">Quiz-1 Q5</span></div>
  <p class="lede">Chapter 3 slid a kernel over an image. Chapter 4 writes the same idea as <b>convolution</b> and then moves to the frequency world, where everything repeats (is <b>periodic</b>) — so convolution there wraps around the ends: <b>circular convolution</b>. The skills you need: compute a short 1-D convolution, turn linear into circular (wrap the tail) and circular into linear (pad with zeros), and find one pixel of a 2-D circular convolution.</p>''']

    f = [3, 5, 7]
    H.append(lesson('The impulse δ: a single 1',
        'δ(x) is 1 at x = 0 and 0 everywhere else. Two facts make it useful: multiplying by a shifted impulse and adding <b>picks out one value</b> (sifting), and convolving with δ <b>changes nothing</b> (δ is the “1” of convolution). Convolving with δ(x − a) just shifts the signal by a.',
        '<div class="formula">\\(\\sum_x f(x)\\,\\delta(x-a)=f(a)\\qquad f*\\delta=f\\qquad f*\\delta(x-a)=f(x-a)\\)<span class="say">“δ at a picks f(a)”; “convolving with δ copies”; “convolving with a shifted δ shifts”.</span></div>'
        '<p><b>Example.</b> f = {3, 5, 7} at x = 0, 1, 2. Σ f(x)δ(x − 1) = 3·0 + 5·1 + 7·0 = <b>5</b>. And f ∗ δ(x − 2) = {0, 0, 3, 5, 7}: the same sequence moved 2 places right.</p>'
        + figs(row(f, label='f(x), x = 0, 1, 2'), row([0, 1, 0], {1: 'hl'}, 'δ(x − 1)'), row([0, 0, 3, 5, 7], {2: 'c1', 3: 'c1', 4: 'c1'}, 'f ∗ δ(x − 2)')) +
        '<p>Continuous version: \\(\\int f(t)\\delta(t-\\tau)dt=f(\\tau)\\), and \\(\\delta(\\alpha t)=\\delta(t)/|\\alpha|\\). The discrete unit step u(x) is the running sum of δ, and δ(x) = u(x) − u(x − 1).</p>',
        tag='1'))

    fl, hl = [1, 2, 3], [1, 0, 2]
    lin = np.convolve(fl, hl).tolist()
    tab = [[*([0] * k), *[fl[k] * v for v in hl], *([0] * (2 - k))] for k in range(3)] + [lin]
    cls = {(3, j): 'hl' for j in range(5)}
    H.append(lesson('Linear convolution: flip, slide, multiply, add',
        'For short sequences the easiest way is <b>shift and add</b>: each value f(k) makes a copy of h scaled by f(k) and shifted k places; add all the copies. The output length is L<sub>f</sub> + L<sub>h</sub> − 1, and it starts at (start of f) + (start of h).',
        '<div class="formula">\\(g(x)=\\sum_k f(k)\\,h(x-k)\\)<span class="say">every f(k) drops a copy of h starting at position k; add the copies.</span></div>'
        '<div class="cols"><div><p><b>Example (your slide).</b> f = {1, 2, 3}, h = {1, 0, 2}. Rows: 1·h at 0, 2·h at 1, 3·h at 2. Add the columns: <b>{1, 2, 5, 4, 6}</b> — length 3 + 3 − 1 = 5.</p>'
        '<p><b>Where is the origin?</b> If f starts at index −1 and h at index 0, g starts at −1 + 0 = −1. Mark it with ↑ in your answer.</p>'
        '<p>Rules: f ∗ h = h ∗ f, (f ∗ h) ∗ k = f ∗ (h ∗ k), and shifting either input shifts the output by the same amount.</p></div>'
        '<div>' + rows(tab, cls, 'rows 1–3: f(k) × h shifted k places; last row = their sum = f ∗ h') + '</div></div>',
        use='Slide examples pp. 9–12; part (c) of the slide card below.', tag='2'))

    wrapped = [lin[0] + lin[3], lin[1] + lin[4], lin[2]]
    Cf = [[fl[(i - j) % 3] for j in range(3)] for i in range(3)]
    H.append(lesson('Circular convolution: the tail wraps round to the start',
        'Circular (n-point) convolution treats both sequences as one period of a repeating signal. The result has only n samples, so whatever linear convolution puts at index n, n + 1, … is <b>added back onto</b> index 0, 1, …. This is what the DFT does when you multiply two spectra.',
        '<div class="formula">\\((f\\circledast h)(x)=\\sum_{k=0}^{n-1}f(k)\\,h\\big((x-k)\\bmod n\\big)\\)<span class="say">same as linear, but the index x − k wraps round: −1 means n − 1.</span></div>'
        '<div class="cols"><div><p><b>Method 1 — linear, then wrap</b> (fastest). Same f, h, n = 3: linear = {1, 2, 5, 4, 6}. Fold the part past index 2 back: {1 + 4, 2 + 6, 5} = <b>{5, 8, 5}</b>.</p>'
        + figs(row(lin, {3: 'nd', 4: 'nd'}, 'linear f ∗ h (red part wraps)'), row(wrapped, {0: 'hl', 1: 'hl'}, '3-point circular = {5, 8, 5}')) +
        '<p><b>Method 2 — circulant matrix.</b> Column j of C<sub>f</sub> is f shifted down j places (wrapping). Then g = C<sub>f</sub> h — one matrix product on the calculator (recipe F).</p>'
        + figs(rows(Cf, {(i, j): 'n4' for i in range(3) for j in range(3)}, 'C<sub>f</sub>'), rows([[v] for v in hl], {}, 'h'), rows([[v] for v in wrapped], {(i, 0): 'hl' for i in range(3)}, '= g')) +
        '</div><div><p><b>Method 3 — two circles</b> (the slide’s picture): f clockwise on the outer ring, h anticlockwise on the inner ring; multiply facing numbers and add → g(0); turn the inner ring one step → g(1), and so on.</p>'
        + old_block(old, '<div class="svgfig">') +
        '<div class="trap"><b>When is circular = linear?</b> Only if n ≥ L<sub>f</sub> + L<sub>h</sub> − 1 — then there is no tail to wrap. So to get linear convolution out of the DFT, <b>zero-pad both sequences to L<sub>f</sub> + L<sub>h</sub> − 1</b> first. Skipping this gives “wraparound error”.</div></div></div>',
        use='Quiz-1 Q5 (2-D), slide examples, every “why do we pad before DFT filtering” question.', tag='3'))
    H.append(old_lab(old, 'circ'))

    H.append(lesson('2-D circular convolution at one pixel',
        'Exactly the 1-D rule in both directions: g(x, y) = Σ f(k, l) · h((x − k) mod m, (y − l) mod n). For one output pixel, build the matching rearranged copy of h (call it h̃), multiply entry by entry with f, and add all the products.',
        '<div class="formula">\\(g(x,y)=\\sum_{k=0}^{m-1}\\sum_{l=0}^{n-1}f(k,l)\\,h\\big((x-k)\\bmod m,\\ (y-l)\\bmod n\\big)\\)<span class="say">for pixel (x, y): the h-entry that multiplies f(k, l) sits at row (x − k) mod m, column (y − l) mod n.</span></div>'
        '<ol class="how"><li>Write the row lookup: for k = 0, 1, 2 the h-row is (x − k) mod 3.</li><li>Write the column lookup: for l = 0, 1, 2 the h-column is (y − l) mod 3.</li><li>Fill h̃(k, l) = h(row lookup of k, column lookup of l).</li><li>Multiply f and h̃ entry by entry and add (calculator: trace of Trn(f) × h̃).</li></ol>'
        '<p><b>Shortcut:</b> h̃ is h rotated 180° and then rolled circularly; for (x, y) = (m − 1, n − 1) it is exactly h rotated 180°.</p>',
        use='Quiz-1 2026 Q5 — worked step by step below.', tag='4'))

    H.append('<h3 id="ch4-conv-q">Questions on convolution</h3>')
    f5 = np.array([[1, 0, 2], [3, 1, 0], [0, 4, 2]]); h5 = np.array([[0, 5, 7], [6, 8, 0], [1, 0, 5]])
    rk = [(0 - k) % 3 for k in range(3)]; cl = [(2 - l) % 3 for l in range(3)]
    ht = h5[np.ix_(rk, cl)]; pr = f5 * ht
    H.append(set_solution(card('qz5'), walk([
        ('What we compute', 'g(0, 2) = Σ<sub>k,l</sub> f(k, l) · h((0 − k) mod 3, (2 − l) mod 3). We need, for every f-entry, which h-entry it meets.', None),
        ('Lookup tables', f'Rows: k = 0, 1, 2 → (0 − k) mod 3 = <b>{", ".join(map(str, rk))}</b>. Columns: l = 0, 1, 2 → (2 − l) mod 3 = <b>{", ".join(map(str, cl))}</b>. So h̃ row 0 = h row 0 read in column order 2, 1, 0; h̃ row 1 = h row 2 (same order); h̃ row 2 = h row 1.',
         figs(rows(h5.tolist(), {(i, j): 'n4' for i in range(3) for j in range(3)}, 'h as given'), rows(ht.tolist(), {(i, j): 'n8' for i in range(3) for j in range(3)}, 'h̃ for pixel (0, 2)'))),
        ('Multiply entry by entry and add', f'Products: 1·7 + 3·5 + 4·8 + 2·6 (the rest are 0) = 7 + 15 + 32 + 12 = <b>{int(pr.sum())}</b>.',
         figs(rows(f5.tolist(), {}, 'f'), rows(pr.tolist(), {(i, j): 'hl' for i in range(3) for j in range(3) if pr[i, j]}, 'f × h̃'))),
    ]) + f'<div class="ansbig">g(0, 2) = {int(pr.sum())}.</div>'))

    lb = np.convolve([1, 0, 1, 1], [1, 2, 3, 1]).tolist() + [0]
    wb = [lb[i] + lb[i + 4] for i in range(4)]
    lc = np.convolve([2, 5, 0, 4], [4, 1, 3]).tolist()
    H.append(set_solution(card('sl-circ'), walk([
        ('(a) Circular, n = 3', 'Linear {1, 2, 3} ∗ {1, 0, 2} = {1, 2, 5, 4, 6}; wrap indices 3, 4 onto 0, 1 → {5, 8, 5}. (Or the circulant matrix in lesson 3.)', None),
        ('(b) Linear first', 'Shift-and-add f = {1, 0, 1, 1} with h = {1, 2, 3, 1}: length 4 + 4 − 1 = 7.', row(lb[:7], label='f ∗ h')),
        ('(b) Wrap to 4 points', 'Put the linear result in two rows of 4 (pad with a 0) and add the columns.',
         figs(rows([lb[:4], lb[4:8]], {(1, j): 'nd' for j in range(4)}, 'first 4 | the tail (red) under it'), row(wb, {j: 'hl' for j in range(4)}, '4-point circular'))),
        ('(c) Linear from circular: pad', 'Lengths 4 and 3 → pad both to 4 + 3 − 1 = 6. The 6-point circular convolution then has nothing to wrap, so it equals the linear one.',
         figs(row([2, 5, 0, 4, 0, 0], {4: 'out', 5: 'out'}, 'f padded'), row([4, 1, 3, 0, 0, 0], {3: 'out', 4: 'out', 5: 'out'}, 'h padded'), row(lc, {3: 'hl'}, 'result'))),
        ('(c) Put the origin back', 'f’s origin (↑ under 0) is at index 2, h’s (↑ under 1) at index 1, so the output origin is at index 2 + 1 = 3 → the value 31.', None),
    ]) + '<div class="ansbig">(a) {5, 8, 5}. (b) {1, 2, 4, 4, 5, 4, 1} → {6, 6, 5, 4}. (c) {8, 22, 11, 31↑, 4, 12}.</div>'))
    H.append(card('dr-circ4'))
    H.append('</section>')
    return '\n'.join(H)


# ═══════════════════════════ 4.2–4.3 Fourier transforms, sampling ═══════════════════════════
def ft(card, old):
    H = ['''<section class="topic" id="ch4-ft">
  <div class="eyebrow">Chapter 4.2–4.3 · Lectures 13–14</div>
  <h2>Fourier transforms, sampling and aliasing</h2>
  <div class="meta"><span class="chip ">TB 4.2–4.3, 4.5.4</span><span class="chip ">slides pp. 13–29, 53–61</span><span class="chip hot">Mid-sem 2024 Q4 · Quiz 2021 Q3</span></div>
  <p class="lede">The one idea of this chapter: <b>every signal or image is a sum of waves</b> (sines and cosines) of different frequencies. The Fourier transform is the list of “how much of each wave”. Slow changes = low frequencies, edges and fine detail = high frequencies. Exams ask for the transform of a simple shape (a box, impulses) and about sampling: how fast to sample, and what goes wrong if you don’t (aliasing).</p>''']

    H.append(lesson('What a Fourier transform shows',
        'The spectrum is a map of frequencies: the centre is frequency 0 (the average brightness, called <b>DC</b>), and the further out a bright spot is, the faster that wave changes. Stripes are a single wave, so their spectrum is just a few dots: narrow stripes → dots far from the centre, wide stripes → dots close to the centre.',
        '<div class="cols"><div>' + figs(img('f_stripe2', 120, 'stripes 2 px wide'), img('f_stripe4', 120, '4 px wide'), img('f_stripe8', 120, '8 px wide')) + '<br>'
        + figs(img('f_stripe2_spec', 120, 'spectrum: dots far out'), img('f_stripe4_spec', 120, 'closer (+ harmonics)'), img('f_stripe8_spec', 120, 'closer still')) + '</div>'
        '<div><p><b>Read the dots.</b> The middle dot is DC (the average grey). The stripes only change left↔right, so all dots lie on the horizontal axis. Sharp black/white stripes are not pure cosines, so wider stripes also show extra “harmonic” dots at multiples of the main frequency.</p>'
        '<p><b>Narrow in one domain = wide in the other.</b> A small, sharp feature needs many high frequencies (a spread-out spectrum); a big smooth feature needs only low ones (a spectrum packed near the centre).</p>'
        + figs(img('cam', 130, 'image'), img('f_spec', 130, 'its spectrum (log scale): most energy near the centre')) + '</div></div>',
        tag='1'))

    H.append(lesson('Fourier series: a periodic signal as a sum of harmonics',
        'A signal that repeats every T seconds is built only from waves that fit a whole number of times into T: frequencies 1/T, 2/T, 3/T, … (the harmonics). The coefficient c<sub>k</sub> says how much of harmonic k there is.',
        '<div class="formula">\\(f(t)=\\sum_{k=-\\infty}^{\\infty}c_k\\,e^{ik\\omega_0t},\\qquad c_k=\\frac1T\\int_T f(t)\\,e^{-ik\\omega_0t}\\,dt,\\qquad \\omega_0=\\frac{2\\pi}{T}\\)<span class="say">c<sub>k</sub> = the average of f times the k-th wave over one period.</span></div>'
        '<p><b>Example.</b> f(t) = 3 + 2cos(2πt) (T = 1): since cos θ = (e<sup>iθ</sup> + e<sup>−iθ</sup>)/2, c<sub>0</sub> = 3, c<sub>1</sub> = c<sub>−1</sub> = 1, all others 0.</p>'
        '<p><b>Facts to quote.</b> Real f ⇒ c<sub>−k</sub> = c<sub>k</sub>* (conjugates). Dirichlet conditions (absolutely integrable over a period, finitely many maxima/minima and jumps) ⇒ the series equals f where f is continuous and gives the <b>midpoint</b> of the jump at a jump.</p>',
        tag='2'))

    H.append(lesson('The Fourier transform and the pairs to know',
        'For a signal that does not repeat, every frequency μ can appear, so the list becomes a function F(μ). Learn a handful of pairs and a handful of rules; exam questions are built from them.',
        '<div class="formula">\\(F(\\mu)=\\int_{-\\infty}^{\\infty}f(t)\\,e^{-i2\\pi\\mu t}\\,dt\\qquad f(t)=\\int_{-\\infty}^{\\infty}F(\\mu)\\,e^{i2\\pi\\mu t}\\,d\\mu\\)<span class="say">forward: minus sign; inverse: plus sign. μ in cycles per unit (ω = 2πμ).</span></div>'
        '<div class="cols"><div>' + table(['signal f(t)', 'transform F(μ)', 'in words'], [
            ['box: height A, width W, centred', 'AW · sin(πμW) / (πμW)', 'a box gives a sinc; zeros at μ = ±1/W, ±2/W, …'],
            ['impulse δ(t)', '1', 'one spike contains every frequency equally'],
            ['δ(t − a)', 'e<sup>−i2πμa</sup>', 'shifting only changes the phase'],
            ['cos(2πμ<sub>0</sub>t)', '½[δ(μ − μ<sub>0</sub>) + δ(μ + μ<sub>0</sub>)]', 'one wave = two spikes at ±μ<sub>0</sub>'],
            ['impulse train, spacing ΔT', 'impulse train, spacing 1/ΔT (× 1/ΔT)', 'close spikes ↔ far-apart spikes'],
            ['Gaussian', 'Gaussian', 'narrow ↔ wide']]) +
        '<p><b>Example.</b> Box of width W = 2, height 1: F(0) = 2 (the area), first zeros at μ = ±½.</p></div><div>'
        + table(['rule', 'what happens'], [
            ['convolution f ∗ h', 'product F · H (and product ↔ convolution)'],
            ['shift f(t − a)', 'F · e<sup>−i2πμa</sup> (|F| unchanged)'],
            ['scale f(αt)', 'F(μ/α)/|α| (squeeze ↔ stretch)'],
            ['modulate e<sup>i2πμ<sub>1</sub>t</sup> f', 'F(μ − μ<sub>1</sub>) (spectrum slides)']]) +
        figs(img('f_rect', 120, 'a white box'), img('f_rect_spec', 120, 'its spectrum: a 2-D sinc')) + '</div></div>',
        use='Mid-sem 2024 Q4 (box → sinc), Quiz 2021 Q3 (two impulses → cosine).', tag='3'))

    H.append(lesson('Sampled signals: the spectrum repeats (DTFT)',
        'Once a signal is a list of samples, its spectrum becomes <b>periodic</b>: copies of the original spectrum repeat every 1/ΔT (once per sampling rate). For samples at integer x that period is 2π in ω (1 in μ).',
        '<div class="formula">\\(F(e^{i\\omega})=\\sum_{x=-\\infty}^{\\infty}f(x)\\,e^{-i\\omega x}\\)<span class="say">discrete in space ⇒ periodic in frequency.</span></div>'
        '<p>Convergence: absolutely summable f ⇒ uniform convergence; square-summable ⇒ mean-square. Same rules as before: convolution ↔ product, shift ↔ phase factor.</p>',
        tag='4'))

    H.append(lesson('Sampling theorem and aliasing',
        'Sampling makes copies of the spectrum, spaced by the sampling rate. If the copies don’t overlap you can cut one out and get the signal back exactly. They don’t overlap when the sampling rate is <b>more than twice the highest frequency</b>. If you sample slower, a fast wave pretends to be a slow one: <b>aliasing</b>.',
        '<div class="formula">\\(\\frac{1}{\\Delta T}>2\\,\\mu_{max}\\qquad\\text{(2-D: also } \\tfrac{1}{\\Delta Z}>2\\,\\nu_{max})\\)<span class="say">samples per unit must exceed twice the highest frequency (the Nyquist rate).</span></div>'
        '<div class="cols"><div><p><b>Example 1.</b> f(t) = sin(2π·3t) + cos(2π·5t): frequencies 3 and 5 → highest 5 → sample faster than <b>10 per second</b>.</p>'
        '<p><b>Example 2 (reading the frequency).</b> sin(8πt) = sin(2π·<b>4</b>·t): divide the number in front of t by 2π → 4 Hz.</p>'
        '<p><b>Example 3 (the alias).</b> A 7 Hz cosine sampled 10 times per second gives the same samples as a |7 − 10| = <b>3 Hz</b> cosine.</p>'
        '<p><b>In images:</b> jagged edges, moiré on fine fabric, a fine checkerboard turning into a coarse one. Shrinking an image by dropping pixels causes it; <b>blur slightly first</b> (anti-aliasing). A finite image is never perfectly band-limited, so some aliasing always remains.</p></div>'
        '<div>' + figs(img('f_zone', 130, 'fine rings'), img('f_zone_alias', 130, 'every 4th pixel kept: fake rings appear (aliasing)'), img('f_zone_blur', 130, 'blurred first, then shrunk: too-fine rings just fade')) + '</div></div>'
        + old_details(old),
        use='Textbook 4.7, 4.10, 4.30; theory “explain aliasing / moiré”.', tag='5'))
    H.append(old_lab(old, 'alias'))

    H.append('<h3 id="ch4-ft-q">Questions on Fourier transforms</h3>')
    H.append(set_solution(card('m24q4'), walk([
        ('Write the image as a function', 'f(x, y) = 1 inside −L/2 ≤ x ≤ L/2 and −W/2 ≤ y ≤ W/2, 0 outside. It is (a box in x) × (a box in y), so the double integral splits into two single ones.',
         figs(img('f_rect', 120, 'the rectangle'), img('f_rect_spec', 120, '|F|: a 2-D sinc'))),
        ('The x integral', 'From −L/2 to L/2 of e<sup>−j2πux</sup> dx = [e<sup>jπuL</sup> − e<sup>−jπuL</sup>] / (j2πu) = sin(πuL)/(πu) = L · sin(πuL)/(πuL). (Uses e<sup>jθ</sup> − e<sup>−jθ</sup> = 2j sin θ.)', None),
        ('The y integral, then multiply', 'Same with W and v: W · sin(πvW)/(πvW). Multiply the two.', None),
        ('Sanity checks', 'At u = v = 0 the sinc factors are 1, so F(0, 0) = LW = the area of the rectangle ✓. Zeros where uL or vW is a non-zero integer. The longer side gives the narrower lobes.', None),
    ]) + '<div class="ansbig">F(u, v) = LW · [sin(πuL)/(πuL)] · [sin(πvW)/(πvW)].</div>'))
    H.append(set_solution(card('q21b3'), walk([
        ('Write the image', 'f(x, y) = δ(x − a, y) + δ(x + a, y): two spikes on the x-axis.', None),
        ('Transform each spike (sifting)', 'An impulse at (a, 0) picks the value of e<sup>−j2π(ux + vy)</sup> at x = a, y = 0: e<sup>−j2πua</sup>. The one at (−a, 0) gives e<sup>+j2πua</sup>.', None),
        ('Add', 'e<sup>−jθ</sup> + e<sup>jθ</sup> = 2cos θ with θ = 2πua. No v appears: the pattern is constant along v — vertical stripes (ridges) in the spectrum, closer together when a is larger.', None),
    ]) + '<div class="ansbig">F(u, v) = 2cos(2πua).</div>'))
    for cid in ['tb4-7', 'tb4-10', 'tb4-30']: H.append(card(cid))
    H.append('</section>')
    return '\n'.join(H)


# ═══════════════════════════ 4.4 the DFT ═══════════════════════════
def dft(card, old):
    H = ['''<section class="topic" id="ch4-dft">
  <div class="eyebrow">Chapter 4.4 · Lectures 14–15</div>
  <h2>The DFT: n samples in, n frequencies out</h2>
  <div class="meta"><span class="chip ">TB 4.4, 4.6</span><span class="chip ">slides pp. 30–38</span><span class="chip hot">Quiz-1 Q3 · Oct 2023 Q1</span></div>
  <p class="lede">The DFT is the Fourier transform you can actually compute: n samples in, n numbers out. F(u) measures how strongly the sequence matches the u-th wave. On paper it is just a matrix times a vector, using the four (or three) “roots of unity” — numbers like 1, −i, −1, i.</p>''']

    H.append(lesson('The definition, and W: a point walking round a circle',
        'W<sub>n</sub> = e<sup>−i2π/n</sup> is the point on the unit circle one n-th of a turn <b>clockwise</b> from 1. Its powers W<sup>0</sup>, W<sup>1</sup>, W<sup>2</sup>, … keep stepping clockwise and come back to 1 after n steps. F(u) multiplies each sample f(x) by W<sup>ux</sup> and adds.',
        '<div class="formula">\\(F(u)=\\sum_{x=0}^{n-1}f(x)\\,W_n^{ux},\\qquad f(x)=\\frac1n\\sum_{u=0}^{n-1}F(u)\\,W_n^{-ux},\\qquad W_n=e^{-i2\\pi/n}\\)<span class="say">your slides: no 1/n in the forward DFT, 1/n in the inverse. (Oct 2023 printed 1/MN in front of the forward one — if a question prints a formula, use the printed one.)</span></div>'
        '<div class="cols"><div><p><b>n = 4:</b> W<sup>0</sup> = 1, W<sup>1</sup> = −i, W<sup>2</sup> = −1, W<sup>3</sup> = i (quarter turns clockwise).</p>'
        '<p><b>n = 3:</b> W<sup>0</sup> = 1, W<sup>1</sup> = −½ − (√3/2)i, W<sup>2</sup> = −½ + (√3/2)i (third-turns). Useful: 1 + W + W<sup>2</sup> = 0.</p>'
        '<p><b>Powers wrap:</b> W<sup>k+n</sup> = W<sup>k</sup>, so only the exponent mod n matters (W<sub>4</sub><sup>6</sup> = W<sub>4</sub><sup>2</sup> = −1). Conjugate: (W<sup>k</sup>)* = W<sup>−k</sup>.</p>'
        '<p><b>F(0) = sum of all samples</b> (W<sup>0</sup> = 1): the DC term.</p></div><div><p>Below: the powers of W for n = 4 and n = 3 drawn on the unit circle. “Down” on the picture is the negative imaginary direction, so W moves clockwise.</p></div></div>' + old_block(old, '<div class="svgfig">'),
        tag='1'))

    f = [1, 2, 3, 4]
    F = np.fft.fft(f)
    trs = [[f'{f[x]}·({W4[(u * x) % 4]})' if W4[(u * x) % 4] != '1' else f'{f[x]}·1' for x in range(4)] + [cf(F[u])] for u in range(4)]
    E4 = [[(u * x) % 4 for x in range(4)] for u in range(4)]
    E3 = [[(u * x) % 3 for x in range(3)] for u in range(3)]
    H.append(lesson('Computing it: the exponent table and the matrix D<sub>n</sub>',
        'Write the table of exponents ux mod n, replace each exponent by its W-value, and you have the matrix D<sub>n</sub>. Then F = D<sub>n</sub> f: row u of D<sub>n</sub> times the column f gives F(u).',
        '<div class="formula">\\(\\mathbf F=D_n\\,\\mathbf f,\\qquad D_n(u,x)=W_n^{ux},\\qquad D_n^{-1}=\\tfrac1n\\,D_n^{*}\\)<span class="say">D<sub>n</sub> is symmetric; its inverse is its conjugate divided by n.</span></div>'
        '<div class="cols"><div>'
        + figs(rows(E4, {(i, j): 'n8' for i in range(4) for j in range(4)}, 'exponents ux mod 4'),
               rows([[W4[e] for e in r] for r in E4], {(i, j): 'n4' for i in range(4) for j in range(4)}, 'D<sub>4</sub>'),
               rows(E3, {(i, j): 'n8' for i in range(3) for j in range(3)}, 'exponents ux mod 3 → D<sub>3</sub> = [1 1 1; 1 W W²; 1 W² W]')) +
        '</div><div><p><b>Example:</b> f = {1, 2, 3, 4}. Each row: multiply f(x) by the W-value and add.</p>'
        + table(['u', 'x = 0', 'x = 1', 'x = 2', 'x = 3', 'F(u)'], [[u] + r for u, r in enumerate(trs)]) +
        '<p>F(1) = 1 − 2i − 3 + 4i = <b>−2 + 2i</b>; F(3) is its conjugate — always true for real f (lesson 4).</p></div></div>',
        use='Every DFT question; calculator recipe: Re F = C<sub>n</sub> f, Im F = −S<sub>n</sub> f.', tag='2'))

    H.append(lesson('Which F(u) is which frequency, and centring',
        'F(0) is DC. F(1), F(2), … are rising positive frequencies up to the middle; after the middle they are the <b>negative</b> frequencies counted back down: F(n − 1) is frequency −1, F(n − 2) is −2. To display with DC in the middle, rotate the list by ⌊n/2⌋ (MATLAB “fftshift”).',
        figs(row(['F(0)', 'F(1)', 'F(2)', 'F(3)'], {0: 'hl'}, 'n = 4, natural order: frequencies 0, 1, ±2, −1', cell=58),
             row(['F(2)', 'F(3)', 'F(0)', 'F(1)'], {2: 'hl'}, 'centred: −2, −1, 0, 1', cell=58),
             row(['F(3)', 'F(4)', 'F(0)', 'F(1)', 'F(2)'], {2: 'hl'}, 'n = 5 centred: −2, −1, 0, 1, 2', cell=58)) +
        '<div class="trap"><b>The (−1)<sup>x</sup> trick only works for even n.</b> Multiplying f(x) by (−1)<sup>x</sup> shifts the spectrum by n/2. For odd n (like 5) that is 2.5 — not a whole number of places — so DC does not land in the centre. For odd n, rotate the list instead (Oct 2023 Q1).</div>',
        tag='3'))

    H.append(lesson('Properties: what changes in F when you change f',
        'Each row says “do this to the signal → this happens to the DFT”. Indices are always taken mod n.',
        table(['do this to f', 'the DFT becomes', 'in words'], [
            ['a f<sub>1</sub> + b f<sub>2</sub>', 'a F<sub>1</sub> + b F<sub>2</sub>', 'linear'],
            ['f(x − x<sub>0</sub>) (circular shift)', 'W<sup>u x<sub>0</sub></sup> F(u)', 'shift ⇒ only the phase changes; |F| stays'],
            ['W<sup>−u<sub>0</sub>x</sup> f(x)', 'F(u − u<sub>0</sub>)', 'multiply by a wave ⇒ spectrum slides'],
            ['f(−x) (reverse)', 'F(−u)', 'reverse ⇒ reverse'],
            ['f ⊛ h (circular conv.)', 'F · H', 'convolution ⇒ multiplication'],
            ['f · h', '(1/n) F ⊛ H', 'multiplication ⇒ convolution'],
            ['f*(x)', 'F*(−u)', 'conjugate ⇒ conjugate and reverse'],
            ['f real', 'F(n − u) = F*(u)', '|F| symmetric; second half mirrors the first'],
            ['f real and even', 'F real and even', ''],
            ['f real and odd', 'F imaginary and odd', '']]) +
        '<p><b>Example.</b> f = {1, 2, 3, 4} is real, so F(3) = F*(1) = −2 − 2i: you only had to compute F(0), F(1), F(2). For real f compute F(0) … F(⌊n/2⌋) and mirror the rest.</p>',
        tag='4'))
    H.append(old_lab(old, 'dft'))

    H.append('<h3 id="ch4-dft-q">Practice on the 1-D DFT</h3>')
    H.append(set_solution(card('dr-dft4'), walk([
        ('Write D<sub>4</sub>', 'Exponent table ux mod 4 → W-values 1, −i, −1, i (lesson 2).', rows([[W4[e] for e in r] for r in E4], {(i, j): 'n4' for i in range(4) for j in range(4)}, 'D<sub>4</sub>')),
        ('Row by row', 'F(0) = 1 + 2 + 3 + 4 = 10. F(1) = 1 + 2(−i) + 3(−1) + 4(i) = −2 + 2i. F(2) = 1 − 2 + 3 − 4 = −2. F(3) = 1 + 2i − 3 − 4i = −2 − 2i.',
         table(['u', 'x = 0', 'x = 1', 'x = 2', 'x = 3', 'F(u)'], [[u] + r for u, r in enumerate(trs)])),
        ('Check', 'Real f ⇒ F(3) must be F*(1): conj(−2 + 2i) = −2 − 2i ✓. F(0) = sum ✓.', None),
    ]) + '<div class="ansbig">F = {10, −2 + 2i, −2, −2 − 2i}.</div>'))
    H.append(card('sl-cs'))
    H.append('</section>')
    return '\n'.join(H)
