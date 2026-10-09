"""Chapters 1–2.3 rebuilt: what DIP is, where images come from (EM spectrum), the eye, image formation, brightness
perception, light, colour models, sensors, illumination × reflectance — with drawn figures and worked numbers."""
from lib import *
import re


def oldfig(old, k):
    ms = list(re.finditer(r'<div class="svgfig">', old))
    if k >= len(ms): return ''
    a, b = extract_div(old, ms[k].start()); return old[a:b]


def svg_wrap(inner, w, h, label=None):
    return f'<figure class="gfig"><svg class="gsvg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{inner}</svg>' + (f'<figcaption>{label}</figcaption>' if label else '') + '</figure>'


def triangles():
    s = ('<line x1="20" y1="120" x2="520" y2="120" class="a-grid"/>'
         '<line x1="60" y1="40" x2="60" y2="120" stroke="#1C7A3B" stroke-width="6"/><text x="38" y="80" class="a-lab" text-anchor="end">15 m</text>'
         '<line x1="60" y1="40" x2="440" y2="120" stroke="#c2410c" stroke-width="1.6"/><line x1="440" y1="120" x2="500" y2="132.6" stroke="#c2410c" stroke-width="1.6"/>'
         '<line x1="500" y1="120" x2="500" y2="132.6" stroke="#1C7A3B" stroke-width="5"/><text x="508" y="132" class="a-lab">h</text>'
         '<ellipse cx="440" cy="120" rx="6" ry="22" fill="none" stroke="var(--muted)" stroke-width="2"/><text x="440" y="160" class="a-lab" text-anchor="middle">lens</text>'
         '<text x="250" y="140" class="a-lab" text-anchor="middle">100 m to the lens</text><text x="470" y="110" class="a-lab" text-anchor="middle">17 mm</text>')
    return svg_wrap(s, 540, 170, 'two similar triangles: 15/100 = h/17')


def mach():
    vals = [40, 70, 100, 130, 160, 190]
    s = ''.join(f'<rect x="{20 + 60 * k}" y="10" width="60" height="70" fill="rgb({v},{v},{v})"/>' for k, v in enumerate(vals))
    pts, ptp = [], []
    for k, v in enumerate(vals):
        x0 = 20 + 60 * k
        y = 170 - v * 0.35
        pts.append(f'{x0},{y:.0f} {x0 + 60},{y:.0f}')
        ptp.append(f'{x0},{y - 9 if k else y:.0f} {x0 + 8},{y:.0f} {x0 + 52},{y:.0f} {x0 + 60},{y + 9 if k < 5 else y:.0f}')
    s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="var(--muted)" stroke-width="2" stroke-dasharray="5 4"/>'
    s += f'<polyline points="{" ".join(ptp)}" fill="none" stroke="#c2410c" stroke-width="2.5"/>'
    s += '<text x="22" y="175" class="a-lab">dashed: true brightness (flat steps) · orange: what you see (over- and undershoot at every edge)</text>'
    return svg_wrap(s, 420, 185, 'Mach bands')


def simcon():
    s = ''
    for k, bg in enumerate([20, 128, 235]):
        s += f'<rect x="{10 + 135 * k}" y="10" width="120" height="120" fill="rgb({bg},{bg},{bg})"/><rect x="{45 + 135 * k}" y="45" width="50" height="50" fill="rgb(128,128,128)"/>'
    return svg_wrap(s, 420, 140, 'all three small squares are exactly the same grey')


def spectrum():
    bands = [('γ rays', '#7c3aed', 'nuclear medicine, astronomy'), ('X-rays', '#2563eb', 'CT, baggage'), ('UV', '#0891b2', 'fluorescence microscopy'),
             ('visible', 'url(#vis)', 'cameras, biometrics'), ('IR', '#b91c1c', 'night vision'), ('micro-wave', '#a16207', 'radar'), ('radio', '#4d7c0f', 'MRI, radio astronomy')]
    s = '<defs><linearGradient id="vis"><stop offset="0" stop-color="#7c3aed"/><stop offset=".3" stop-color="#2563eb"/><stop offset=".5" stop-color="#16a34a"/><stop offset=".7" stop-color="#eab308"/><stop offset="1" stop-color="#dc2626"/></linearGradient></defs>'
    for k, (name, col, use) in enumerate(bands):
        x = 10 + 128 * k
        s += f'<rect x="{x}" y="34" width="124" height="40" rx="6" fill="{col}"/><text x="{x + 62}" y="59" text-anchor="middle" style="fill:#fff;font-weight:700;font-size:14px">{name}</text>'
        s += f'<text x="{x + 62}" y="92" text-anchor="middle" class="a-lab">{use}</text>'
    s += '<text x="10" y="20" class="a-lab">← shorter wavelength, higher frequency, more energy per photon</text><text x="905" y="20" class="a-lab" text-anchor="end">longer wavelength →</text>'
    return svg_wrap(s, 910, 104, None)


def bayer():
    col = {'R': '#ef4444', 'G': '#22c55e', 'B': '#3b82f6'}
    pat = ['GRGR', 'BGBG', 'GRGR', 'BGBG']
    s = ''.join(f'<rect x="{10 + 44 * j}" y="{10 + 44 * i}" width="42" height="42" rx="4" fill="{col[c]}"/><text x="{31 + 44 * j}" y="{37 + 44 * i}" text-anchor="middle" style="fill:#fff;font-weight:800;font-size:16px">{c}</text>' for i, r in enumerate(pat) for j, c in enumerate(r))
    return svg_wrap(s, 190, 190, 'Bayer filter: 50 % green, 25 % red, 25 % blue')


def section(card, old):
    eye = oldfig(old, 0)
    H = ['''<section class="topic" id="ch2-eye">
  <div class="eyebrow">Chapters 1–2.3 · Lectures 1–4</div>
  <h2>What an image is, how we see it, and how a camera makes it</h2>
  <div class="meta"><span class="chip ">TB 1, 2.1–2.3</span><span class="chip ">slides: Overview; Fundamentals pp. 3–19</span><span class="chip hot">theory + one-line numbers</span></div>
  <p class="lede">The easiest marks in the paper: short facts and one-line calculations. This section explains what a digital image is, which kinds of radiation make images, how the human eye forms and perceives an image (and where it is fooled), and how a camera sensor captures one. The numbers you may be asked for: the size of an image on the retina, a wavelength from a frequency, and resolution of a camera.</p>''']

    H.append(lesson('What is a (digital) image, and what is DIP?',
        'An image is a <b>function</b>: give it a position (x, y) and it returns a brightness f(x, y). For a colour image it returns three numbers (red, green, blue). <b>Digital</b> means both the positions and the brightness values are whole-number steps; each little square is a <b>pixel</b>.',
        '<div class="cols"><div><p><b>Digital image processing</b> = using a computer to process, analyse and interpret images. Your slides split it into three levels:</p>'
        + table(['Level', 'Input → output', 'Examples'], [['Low', 'image → image', 'remove noise, sharpen, increase contrast'], ['Mid', 'image → attributes', 'find edges, segment objects, extract features'], ['High (computer vision)', 'image → meaning / decision', 'recognise a face, classify an object']]) +
        '<p>This course covers the <b>low and mid</b> levels.</p></div>'
        '<div><p><b>Why computers could do it (slide history):</b> the von Neumann architecture (1945: memory, arithmetic-logic unit, control unit, input, output), the transistor (Bell Labs, 1948), high-level languages and the integrated circuit (1950s–60s), Intel’s microprocessor (1970s), the IBM PC (1981), and ever smaller chips (LSI → VLSI → ULSI).</p></div></div>',
        tag='1'))

    H.append(lesson('Where images come from: the electromagnetic spectrum',
        'Most images are made by some kind of electromagnetic (EM) radiation. The bands differ only in wavelength — and each band shows different things, which is why each has its own uses.',
        spectrum() + '<div class="cols" style="margin-top:12px"><div><ul><li><b>Gamma rays</b>: nuclear medicine (a radioactive tracer shows tumours and bone infections), astronomy, cargo screening.</li><li><b>X-rays</b>: CT (computerised tomography) scans, baggage screening.</li><li><b>Ultraviolet</b>: fluorescence microscopy (cells, proteins), astronomy.</li><li><b>Visible and infrared</b>: everyday cameras, biometrics, licence plates, inspection, satellites; IR for night vision, missile tracking.</li></ul></div>'
        '<div><ul><li><b>Microwaves</b>: radar (it sees through clouds and darkness), ground-penetrating radar, industrial inspection.</li><li><b>Radio</b>: MRI, radio astronomy, long-range radar.</li><li><b>Not EM at all</b>: ultrasound (sound waves — pregnancy scans, heart, abdomen, muscles) and electron microscopy (a beam of electrons).</li></ul>'
        '<p><b>Memory hook:</b> “Gamma, X, UV, Visible, IR, Microwave, Radio” — energy falls from left to right.</p></div></div>',
        use='one-line theory questions (“give an application of X-ray / microwave imaging”).', tag='2'))

    H.append(lesson('The eye, part by part',
        'Light goes cornea → pupil → lens → retina; the retina turns it into nerve signals that travel along the optic nerve to the brain. Each part has a camera equivalent.',
        '<div class="cols"><div>' + table(['Part', 'What it does', 'Camera equivalent'], [
            ['Cornea', 'clear dome at the front; protects and bends (focuses) light', 'front glass'],
            ['Iris and pupil', 'the coloured ring and the hole in it; the hole’s size controls how much light enters', 'aperture'],
            ['Lens + ciliary muscles', 'the muscles change the lens’s shape to focus near or far', 'focusing lens'],
            ['Retina', 'light-sensitive layer with rods and cones', 'sensor'],
            ['Fovea (macula)', '≈ 1.5 mm centre of the retina, packed with cones: sharp, colour vision', 'the sharpest part of the sensor'],
            ['Blind spot (optic disc)', 'where the optic nerve leaves: no rods or cones, no image', '—'],
            ['Sclera', 'the white tough outer coat', 'camera body']]) + '</div><div>' + eye + '</div></div>'
        '<h4 style="margin-top:14px">Rods and cones</h4>' + table(['', 'Rods', 'Cones'], [
            ['How many', '≈ 90–120 million', '≈ 6–7 million'], ['Where', 'all over, none in the fovea', 'packed in the fovea'],
            ['Light needed', 'very little (they work in the dark)', 'bright light'], ['Vision', 'scotopic (night), no colour', 'photopic (day), colour'],
            ['Detail', 'low: many rods share one nerve end', 'high: one cone per nerve end']]) +
        '<p><b>Three cone types:</b> L (long wavelength, red-ish, 60–65 %), M (medium, green, 30–35 %), S (short, blue, 5–10 %). L and M are coded on the X chromosome, S on chromosome 7 — with two X chromosomes, women more often have an extra L/M variant, the slide’s explanation for better colour discrimination.</p>',
        use='“Compare rods and cones”, “what is the fovea / blind spot”. Memory hook: <b>rods = night, many, blurry; cones = colour, few, sharp</b>.', tag='3'))

    H.append(lesson('How big is the image on the retina? (similar triangles)',
        'The lens makes a small upside-down image on the retina. The object, the lens and its image form two similar triangles, so the ratios are equal.',
        '<div class="cols"><div>'
        '<div class="formula">\\(\\dfrac{\\text{object height}}{\\text{object distance}}=\\dfrac{\\text{image height}}{\\text{lens-to-retina distance}}\\)<span class="say">In the eye the lens-to-retina distance is fixed at about <b>17 mm</b>; the eye focuses by changing the lens shape (focal length). A camera does the opposite: fixed focal length, the sensor distance changes.</span></div>'
        '<p><b>Example (your slide).</b> A 15 m palm tree 100 m away: 15/100 = h/17 → h = 17 × 0.15 = <b>2.55 mm</b> (the slide writes 2.5 mm).</p>'
        '<p>The same triangle answers the camera questions (textbook 2.6, 2.8) with the camera’s focal length in place of 17 mm, and the smallest-visible-dot question (2.2).</p>'
        '</div><div>' + triangles() + '</div></div>',
        use='slide example, textbook 2.2, 2.6, 2.8. Keep both distances in the same units.', tag='4'))
    for cid in ['ex-tree', 'tb2-2']: H.append(card(cid))

    H.append(lesson('Brightness is not what the eye reports',
        'The eye does not measure light like a meter. It adapts to the average light level, and the brightness we perceive depends on the surroundings. Four effects from your slides:',
        '<div class="mini">'
        '<div><h5>Brightness adaptation</h5><p>The eye handles an enormous range of light (about 10<sup>10</sup> to 1), but not all at once: it shifts its sensitivity to the current level and only then distinguishes a small range around it. Perceived brightness grows roughly like the <b>log</b> of the light intensity.</p></div>'
        '<div><h5>Weber ratio ΔI<sub>c</sub>/I</h5><p>On a background of intensity I, ΔI<sub>c</sub> is the smallest extra brightness you notice half the time. <b>Small ratio = good discrimination.</b> Example: I = 100, ΔI<sub>c</sub> = 2 → 0.02 (good). In dim light (rods) the ratio is large; in bright light (cones) small.</p></div>'
        '<div><h5>Mach bands</h5>' + mach() + '<p>Next to each edge we see a dark and a light stripe that are not there — the visual system exaggerates edges.</p></div>'
        '<div><h5>Simultaneous contrast</h5>' + simcon() + '<p>The same grey looks darker on a white background and lighter on a black one: perceived brightness depends on the surroundings.</p></div></div>'
        '<p>Optical illusions (your slide) are the same idea: the brain fills in or distorts what the eye receives.</p>',
        use='theory questions (“explain Mach bands / simultaneous contrast / what a low Weber ratio means”).', tag='5'))

    H.append(lesson('Light: wavelength, frequency, energy',
        'All EM radiation travels at the speed of light c. A wave that wiggles faster (higher frequency) has a shorter wavelength and carries more energy per photon.',
        '<div class="cols"><div>'
        '<div class="formula">\\(c=\\lambda\\,\\nu\\)<span class="say">speed = wavelength × frequency, c = 2.998 × 10<sup>8</sup> m/s. So λ = c/ν.</span></div>'
        '<div class="formula">\\(E=h\\,\\nu\\)<span class="say">energy of one photon = Planck’s constant × frequency.</span></div>'
        '<p><b>Example (textbook 2.3).</b> 60 Hz mains electricity: λ = 2.998 × 10<sup>8</sup> / 60 = 5.0 × 10<sup>6</sup> m ≈ <b>5000 km</b>.</p>'
        '<p>Visible light is about 0.43 µm (violet) to 0.79 µm (red). Radio waves are about 10<sup>9</sup> times longer than visible light; gamma rays about 10<sup>7</sup> times shorter.</p></div>'
        '<div><p><b>Light words:</b> <b>radiance</b> = energy leaving the source; <b>luminance</b> = how much of it an observer perceives; <b>brightness</b> = the subjective impression. Light with no colour is <b>monochromatic</b>; its only property is intensity, measured in grey levels from black to white.</p>'
        '<p><b>Colour models:</b> <b>RGB</b> adds coloured light to black (screens); <b>CMYK</b> starts from white paper and adds inks that absorb light (printing); <b>HSV/HSI</b> describes colour as hue (which colour), saturation (how strong) and value/intensity (how bright) — handy for processing.</p></div></div>',
        tag='6'))
    H.append(card('tb2-3'))

    H.append(lesson('How a camera captures an image',
        'An image needs a source of energy, a scene that reflects or lets it through, and a sensor that turns the arriving energy into a voltage. Then sampling and quantisation (Section 2.4) turn the voltage into numbers.',
        '<div class="cols"><div>'
        '<p><b>Three sensor arrangements:</b></p><ul>'
        '<li><b>Single sensor</b> (a photodiode): one value at a time, so the sensor (or the scene) must move in both x and y. Slow but precise (high-precision scanners).</li>'
        '<li><b>Strip of sensors</b>: one whole line at a time; moving perpendicular to the strip gives the second direction (flatbed scanners, airborne imaging). A <b>ring</b> of sensors around the body plus reconstruction gives CT slices.</li>'
        '<li><b>2-D array</b> (CCD or CMOS): the whole image at once — every digital camera. Each element’s response is proportional to the total light it collected. CMOS sensors read out faster and use less power than CCDs.</li></ul>'
        '<p><b>Colour:</b> each sensor element sits under one colour filter (the <b>Bayer pattern</b>), so it measures only red, only green or only blue. <b>Demosaicing</b> fills in the two missing colours at every pixel from its neighbours.</p>'
        '</div><div>' + bayer() + '<p>Twice as many green filters because the eye is most sensitive to green. Larger sensors (full frame 864 mm², crop factor 1) gather more light than a phone sensor (≈ 70 mm², crop factor ≈ 3.5).</p></div></div>'
        '<h4 style="margin-top:14px">Illumination × reflectance</h4>'
        '<div class="cols"><div><div class="formula">\\(f(x,y)=i(x,y)\\cdot r(x,y)\\), with \\(0<i<\\infty\\), \\(0<r<1\\)<span class="say">what the camera records = light falling on the point × the fraction the point reflects.</span></div></div>'
        '<div><p><b>Example.</b> A white wall (r = 0.80) on a sunny day (i = 90,000 lx) gives f = 72,000; the same wall under a full moon (i = 0.1 lx) gives f = 0.08. Black velvet (r = 0.01) in the sun gives 900. This huge range is why cameras (and eyes) must adapt.</p></div></div>',
        use='theory (“how is a 2-D image acquired with a single sensor / strip / array?”, “what is demosaicing?”), and textbook 2.4, 2.6, 2.8 below.', tag='7'))
    for cid in ['tb2-4', 'tb2-6', 'tb2-8']: H.append(card(cid))

    H.append(h3('Quick recall (cover the right column)'))
    H.append(table(['Prompt', 'Answer'], [
        ['Light path through the eye', 'cornea → pupil → lens → retina → optic nerve → brain'], ['Fovea', 'centre of the retina, ≈ 1.5 mm, most cones, sharpest vision'],
        ['Blind spot', 'optic disc: no rods or cones'], ['Eye vs camera focusing', 'eye: lens–retina 17 mm fixed, lens shape changes; camera: focal length fixed, sensor distance changes'],
        ['Scotopic / photopic', 'night vision by rods / day colour vision by cones'], ['Small Weber ratio means', 'good brightness discrimination'],
        ['CMOS vs CCD', 'CMOS: faster readout, lower power'], ['f(x, y) =', 'illumination × reflectance, 0 < r < 1'], ['Demosaicing', 'rebuilding full RGB from the Bayer-filtered data']]))
    H.append('</section>')
    return '\n'.join(H)
