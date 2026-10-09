"""Chapter 2.6 rebuilt: the maths toolbox, one idea at a time, each with plain words, a small numeric example and a picture;
affine geometry drawn on a letter F; the past-paper solutions as step-by-step walks."""
from lib import *
import math

c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def section(card):
    H = ['''<section class="topic" id="ch2-math">
  <div class="eyebrow">Chapter 2.6 · Lecture 6</div>
  <h2>The maths toolbox: arithmetic, sets, geometry, transforms, statistics</h2>
  <div class="meta"><span class="chip ">TB 2.6</span><span class="chip ">slides pp. 31–52</span><span class="chip hot">affine questions</span></div>
  <p class="lede">These are the operations every later chapter uses. You do not need to memorise proofs — you need to know <b>what each operation does to an image</b>, and be able to do the small calculations the exam asks: decide whether an operation is linear, combine images with set or logic operations, move points with a matrix (rotate, scale, shift, shear), find that matrix from three point pairs, and compute a mean and a variance.</p>''']

    # 1 elementwise vs matrix
    A = [[1, 2], [3, 4]]; B = [[5, 6], [7, 8]]
    H.append(lesson('Image arithmetic is pixel by pixel',
        'When you add, subtract, multiply or divide two images, you do it to <b>matching pixels</b> — top-left with top-left, and so on. This is not the matrix product you learned in maths.',
        '<div class="cols"><div>'
        '<p><b>Example.</b> Multiply two 2×2 images pixel by pixel (the slides call this the <b>Hadamard product</b>, written A ⊙ B): 1×5 = 5, 2×6 = 12, 3×7 = 21, 4×8 = 32.</p>'
        '<p>The matrix product A·B would give something completely different (rows times columns: 1×5 + 2×7 = 19 …). In image processing “A × B” of two images means the pixel-by-pixel version unless the question says “matrix”.</p>'
        '</div><div>' + figs(gsvg(A, {}, label='A'), gsvg(B, {}, label='B'), gsvg([[5, 12], [21, 32]], {(i, j): 'hl' for i in range(2) for j in range(2)}, label='A ⊙ B (pixel by pixel)'), gsvg([[19, 22], [43, 50]], {(i, j): 'out' for i in range(2) for j in range(2)}, label='A·B matrix product — not this')) + '</div></div>',
        use='image averaging, subtraction, shading correction, masks (next block), and the “sum of the Hadamard product” that every filter output is.', tag='1'))

    # 2 the four arithmetic uses, with real pictures
    H.append(lesson('What the four arithmetic operations are used for',
        'Each arithmetic operation has one classic job. The pictures show them on a real photograph.',
        '<div class="mini wide">'
        '<div><h5>Add, then divide by K: remove noise</h5>' + figs(img('avg_1', 150, 'one noisy shot'), img('avg_64', 150, 'average of 64 shots')) +
        '<p>Each shot = true picture + random noise. Averaging keeps the picture and cancels the noise: the noise spread (standard deviation) shrinks by √K. Noise σ = 64, K = 16 shots → 64/√16 = <b>16</b>; K = 64 → <b>8</b>.</p></div>'
        '<div><h5>Subtract: find what changed</h5>' + figs(img('cam', 105, 'before'), img('cam_changed', 105, 'after'), img('diff', 105, 'after − before')) +
        '<p>Everything that stayed the same becomes 0 (black); only the change remains. Used for change detection and digital subtraction angiography (blood vessels after dye − before dye).</p></div>'
        '<div><h5>Divide: remove uneven lighting</h5>' + figs(img('shaded', 105, 'shaded photo'), img('shade', 105, 'the shading'), img('unshaded', 105, 'photo ÷ shading')) +
        '<p>A badly lit image = true image × shading pattern. If you know (or can measure) the shading, dividing by it gives the evenly lit image back.</p></div>'
        '<div><h5>Multiply by 0/1: keep only a region</h5>' + figs(img('roi_mask', 105, 'mask (1 = keep)'), img('roi', 105, 'photo × mask')) +
        '<p>A mask is 1 inside the region of interest and 0 outside; multiplying keeps the region and blacks out the rest.</p></div>'
        '</div>'
        '<p><b>Results outside 0 … 255?</b> Shift and stretch them back: subtract the smallest value, then multiply by K / (largest value). Example: values −20, 0, 30, 80 → subtract −20 → 0, 20, 50, 100 → × 255/100 → <b>0, 51, 127.5, 255</b>.</p>',
        use='theory questions (“how would you detect a missing part?”, “why does averaging reduce noise?”), textbook 2.25, 2.26, 2.29.', tag='2'))

    # 3 linear or not
    H.append(lesson('Linear or not? The one-test method',
        'An operation is <b>linear</b> if it treats a mixture of images the same way as the images themselves: doing it to (2 × image) gives 2 × the output, and doing it to (image1 + image2) gives output1 + output2. If you can find <b>one</b> small example where this fails, the operation is <b>nonlinear</b>.',
        '<div class="cols"><div>'
        '<p><b>How to test (always works):</b></p><ol class="how"><li>Pick two tiny images f₁, f₂ and two numbers a, b (use a = 1, b = −1 or a = 2).</li><li>Left side: mix first, then apply the operation: H(a f₁ + b f₂).</li><li>Right side: apply first, then mix: a H(f₁) + b H(f₂).</li><li>Equal for every choice → linear. Different once → nonlinear.</li></ol>'
        '<p><b>Example 1 — sum of the pixels</b> (linear): f₁ = [1 2], f₂ = [3 4]. Sum of (f₁ + f₂) = 4 + 6 = 10; sum f₁ + sum f₂ = 3 + 7 = 10 ✓. Always equal → linear.</p>'
        '<p><b>Example 2 — maximum</b> (nonlinear, the textbook’s example): f₁ = [0 2; 2 3], f₂ = [6 5; 4 7], a = 1, b = −1.<br>Mix first: f₁ − f₂ = [−6 −3; −2 −4] → max = <b>−2</b>.<br>Apply first: max f₁ − max f₂ = 3 − 7 = <b>−4</b>. Different → nonlinear.</p>'
        '<p><b>Example 3 — squaring each pixel</b> (your slide): (2f)² = 4f², but 2·(f²) = 2f² → nonlinear.</p>'
        '</div><div>' + table(['Linear (one test never fails)', 'Nonlinear (one example breaks it)'], [
            ['sum or average over a neighbourhood', 'max, min, median'],
            ['correlation, convolution (every filter with fixed weights)', 'thresholding, |value|, squaring'],
            ['the DFT, F ↦ A F A (your slide)', 'multiplying or dividing two input images'],
            ['adding / subtracting images', 'histogram equalisation (depends on the image itself)']]) + '</div></div>',
        use='“Is this operator linear? Justify.” — write the test with tiny numbers; one counter-example is a full answer for “nonlinear”.', tag='3'))

    for cid in ['tb2-23', 'tb2-24']: H.append(card(cid))

    # 4 set and logical
    a = [[1, 5], [7, 2]]; b = [[4, 3], [6, 6]]
    H.append(lesson('Set and logic operations on images',
        'Your slides treat an image as a set of points (x, y, z) — position and grey value. Then “complement”, “union” and “intersection” become simple pixel rules. For black-and-white (binary) images they are the familiar AND, OR, XOR, NOT.',
        '<div class="cols"><div>'
        '<p><b>Grey images (k bits, L = 2<sup>k</sup> levels):</b></p><ul>'
        '<li><b>Complement</b> A<sup>c</sup>: every pixel z becomes L − 1 − z — the <b>negative</b>.</li>'
        '<li><b>Union</b> A ∪ B: at each pixel keep the <b>larger</b> value (max).</li>'
        '<li><b>Intersection</b> A ∩ B: keep the <b>smaller</b> value (min).</li></ul>'
        '<p><b>Example</b> (3-bit, L − 1 = 7): A = [1 5; 7 2], B = [4 3; 6 6].</p>'
        '<p>De Morgan check: (A ∪ B)<sup>c</sup> = 7 − [4 5; 7 6] = [3 2; 0 1] = A<sup>c</sup> ∩ B<sup>c</sup> ✓.</p>'
        '</div><div>' + figs(gsvg(a, {}, label='A'), gsvg(b, {}, label='B'), gsvg([[6, 2], [0, 5]], {(i, j): 'n8' for i in range(2) for j in range(2)}, label='Aᶜ = 7 − A'), gsvg([[4, 5], [7, 6]], {(i, j): 'n4' for i in range(2) for j in range(2)}, label='A ∪ B = max'), gsvg([[1, 3], [6, 2]], {(i, j): 'nd' for i in range(2) for j in range(2)}, label='A ∩ B = min')) + '</div></div>'
        '<p style="margin-top:16px"><b>Binary images</b> (white = 1): A AND B is white only where both are white; A OR B where either is; A XOR B where exactly one is; NOT A swaps black and white; A \\ B (difference) = A AND (NOT B).</p>' +
        figs(img('bin_setA', 112, 'A'), img('bin_setB', 112, 'B'), img('bin_and', 112, 'A AND B'), img('bin_or', 112, 'A OR B'), img('bin_xor', 112, 'A XOR B'), img('bin_notA', 112, 'NOT A'), img('bin_aminusb', 112, 'A \\ B')),
        use='short computations on 2×2 or 3×3 grey images, and the negative (Chapter 3).', tag='4'))
    H.append(card('dr-sets'))

    # 5 three kinds of spatial operations
    avg = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    H.append(lesson('Three kinds of “spatial” operations',
        'Every operation in the spatial domain is one of three kinds, depending on how many input pixels decide one output pixel.',
        '<div class="mini">'
        '<div><h5>1 · Single pixel</h5><p>The output at a pixel depends only on that one input value: s = T(z). Example: the negative s = 255 − z turns 200 into 55. All of Chapter 3’s intensity transformations are this kind.</p></div>'
        '<div><h5>2 · Neighbourhood</h5><p>The output depends on a small window around the pixel. Example: the 3×3 average of the window on the right is (1 + 2 + … + 9)/9 = 45/9 = <b>5</b>. All filters are this kind.</p>' + gsvg(avg, {(i, j): 'n8' for i in range(3) for j in range(3)}, cell=36, idx=False) + '</div>'
        '<div><h5>3 · Geometric</h5><p>Pixels <b>move</b> to new positions (rotate, scale, shift, shear) and their values are filled in by interpolation. Next block.</p></div></div>',
        tag='5'))

    # 6 affine, explained from scratch
    S = [[1.5, 0, 0], [0, 1.5, 0], [0, 0, 1]]
    R90 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    R30 = [[c30, -s30, 0], [s30, c30, 0], [0, 0, 1]]
    T = [[1, 0, -1.5], [0, 1, 1.2], [0, 0, 1]]
    Sv = [[1, 0.7, 0], [0, 1, 0], [0, 0, 1]]
    Sh = [[1, 0, 0], [0.7, 1, 0], [0, 0, 1]]
    Rf = [[1, 0, 0], [0, -1, 0], [0, 0, 1]]
    H.append(lesson('Moving pixels with a matrix: the affine transformation',
        'A geometric transformation sends every pixel position (x, y) to a new position (x′, y′). The five basic moves — <b>scale, rotate, shift, shear, reflect</b> — each have a 3×3 matrix. To move a point you multiply the matrix by the point written as (x, y, 1).',
        '<p>Below, the grey letter F is the original and the orange F is the result (x = row, pointing <b>down</b>; y = column, pointing <b>right</b>; the dot is the origin):</p>'
        '<div class="mini">'
        '<div><h5>Scale by c<sub>x</sub>, c<sub>y</sub></h5>' + affine_svg(S) + '<p>\\(x\'=c_x x,\\ y\'=c_y y\\). Here both 1.5: bigger, same shape. ½ would shrink it.</p></div>'
        '<div><h5>Rotate by θ</h5>' + affine_svg(R30) + '<p>\\(x\'=x\\cos\\theta-y\\sin\\theta\\), \\(y\'=x\\sin\\theta+y\\cos\\theta\\). θ = 30°, positive = anticlockwise (your slides).</p></div>'
        '<div><h5>Shift (translate) by t<sub>x</sub>, t<sub>y</sub></h5>' + affine_svg(T) + '<p>\\(x\'=x+t_x,\\ y\'=y+t_y\\). Here up 1.5 rows, right 1.2 columns.</p></div>'
        '<div><h5>Vertical shear</h5>' + affine_svg(Sv) + '<p>\\(x\'=x+s_v y\\), \\(y\'=y\\): points move up/down by an amount that grows with their column → vertical lines stay vertical, horizontal lines tilt.</p></div>'
        '<div><h5>Horizontal shear</h5>' + affine_svg(Sh) + '<p>\\(x\'=x\\), \\(y\'=s_h x+y\\): points slide sideways by an amount that grows with their row → horizontal lines stay horizontal, vertical lines tilt.</p></div>'
        '<div><h5>Reflect</h5>' + affine_svg(Rf) + '<p>Scaling with one factor −1: here \\(y\'=-y\\), a mirror image about the x-axis.</p></div></div>'
        '<h4 style="margin-top:20px">Why the extra “1”?</h4>'
        '<div class="cols"><div><p>Scaling, rotation and shear only <b>multiply</b> x and y by numbers, so a 2×2 matrix is enough for them. A <b>shift adds a constant</b>, and multiplying never adds a constant. The trick: write the point as <b>(x, y, 1)</b>. Then the third column of the matrix gets multiplied by that 1 and simply <b>added</b>:</p>'
        '<div class="formula">\\(x\'=a_{11}x+a_{12}y+a_{13}\\cdot 1\\)<span class="say">so a<sub>13</sub> is exactly “add t<sub>x</sub>”, and a<sub>23</sub> is “add t<sub>y</sub>”. The bottom row 0 0 1 just keeps the 1 as 1, so the result can be fed into the next matrix.</span></div>'
        '<p><b>Example.</b> Shift (2, 3) by t<sub>x</sub> = 5, t<sub>y</sub> = −1: \\(\\begin{bmatrix}1&0&5\\\\0&1&-1\\\\0&0&1\\end{bmatrix}\\begin{bmatrix}2\\\\3\\\\1\\end{bmatrix}=\\begin{bmatrix}2+5\\\\3-1\\\\1\\end{bmatrix}=\\begin{bmatrix}7\\\\2\\\\1\\end{bmatrix}\\).</p></div>'
        '<div><p><b>Several moves in a row = multiply the matrices.</b> The move done <b>first</b> is written <b>last</b> (closest to the point): scale, then rotate, then shift = T · R · S.</p>'
        '<p><b>Example.</b> Scale ×2, then shift x by +1, applied to (1, 1): scale → (2, 2), shift → (3, 2). In matrices: T·S·(1, 1, 1) = (3, 2, 1). The other order S·T gives (4, 2) — <b>order matters</b>.</p>'
        '<p><b>Undoing a move</b> = the inverse matrix A<sup>−1</sup>: scale by 1/c, rotate by −θ (for rotation A<sup>−1</sup> = A<sup>T</sup>), shift by −t.</p></div></div>'
        '<h4 style="margin-top:20px">Finding A from three point pairs (the exam question)</h4>'
        '<div class="cols"><div><p>A has <b>6 unknown numbers</b> (the top two rows). Each point pair (where a point starts, where it lands) gives <b>2 equations</b> (one for x′, one for y′). So <b>3 pairs give 6 equations</b> — exactly enough. Two easy ways to solve:</p>'
        '<ol class="how"><li><b>By hand:</b> the first row (a, b, c) only appears in the x′ equations: a·x + b·y + c = x′ for the three points. Subtract the equations from each other to eliminate c. Do the same for the second row with the y′ values.</li>'
        '<li><b>By calculator:</b> put the three start points as columns of X (with a row of 1s), the three end points as columns of Y; then A = Y X<sup>−1</sup> (Matrix app, recipe F in the calculator section).</li></ol></div>'
        '<div><p><b>Forward vs inverse mapping</b> (how a rotated image is actually made). Going forward — “send each input pixel to its new place” — leaves holes and overlaps, because new places are not whole numbers. So programs go <b>backwards</b>: for every output pixel, compute where it came from with A<sup>−1</sup>, and interpolate the input there (nearest or bilinear, Section 2.4).</p></div></div>',
        use='End-sem 2022-23 Q2 (A from three pairs, then map a point), textbook 2.36–2.37 (composite moves, inverses), rotation of a point.', tag='6'))
    H.append('<div class="lab" data-lab="affine" data-init=\'{"P": "1 1\\n0 2\\n-1 1", "Q": "3 -4\\n-1 -1\\n1 0", "t": "6 -8", "title": "Affine lab: three point pairs → A, then map any point"}\'></div>')

    e = card('e23q2')
    e = set_solution(e, walk([
        ('What is unknown', r'A has six unknowns: \(A=\begin{bmatrix}a&b&c\\d&e&f\\0&0&1\end{bmatrix}\). The first row (a, b, c) makes x′, the second row (d, e, f) makes y′. Each of the 3 point pairs gives one equation for each row.', None),
        ('Row 1 from the three x′ values', 'f(1,1) → x′ = 3: a + b + c = 3. f(0,2) → x′ = −1: 2b + c = −1. f(−1,1) → x′ = 1: −a + b + c = 1.<br>First − third: 2a = 2 → <b>a = 1</b>. First − second: a − b = 4 → <b>b = −3</b>. Then c = 3 − 1 + 3 = <b>5</b>.', None),
        ('Row 2 from the three y′ values', 'y′ values −4, −1, 0: d + e + f = −4; 2e + f = −1; −d + e + f = 0.<br>First − third: 2d = −4 → <b>d = −2</b>. First − second: d − e = −3 → <b>e = 1</b>. Then f = −4 + 2 − 1 = <b>−3</b>.', None),
        ('Check one pair', '(0, 2): x′ = 1·0 − 3·2 + 5 = −1 ✓, y′ = −2·0 + 1·2 − 3 = −1 ✓.', None),
        ('(b) Map (6, −8)', 'x′ = 1·6 − 3·(−8) + 5 = 6 + 24 + 5 = <b>35</b>; y′ = −2·6 + 1·(−8) − 3 = −12 − 8 − 3 = <b>−23</b>.', None),
    ]) + r'<div class="ansbig">(a) \(A=\begin{bmatrix}1&-3&5\\-2&1&-3\\0&0&1\end{bmatrix}\). (b) f(6, −8) = (35, −23).</div>')
    H.append(e)
    r = card('dr-rot')
    r = set_solution(r, walk([
        ('Write the rotation for 30°', r'cos 30° = 0.8660, sin 30° = 0.5. \(x\'=0.866x-0.5y\), \(y\'=0.5x+0.866y\).', None),
        ('Forward: where does (4, 2) go?', "x′ = 0.866·4 − 0.5·2 = 3.4641 − 1 = <b>2.4641</b>; y′ = 0.5·4 + 0.866·2 = 2 + 1.7321 = <b>3.7321</b>.", None),
        ('Inverse: where did (4, 2) come from?', r'Undo the rotation = rotate by −30°, i.e. use \(A^{-1}=A^T\): \(x=0.866x\'+0.5y\'\), \(y=-0.5x\'+0.866y\'\). With (4, 2): x = 3.4641 + 1 = <b>4.4641</b>, y = −2 + 1.7321 = <b>−0.2679</b>.', None),
    ]) + '<div class="ansbig">Forward (2.4641, 3.7321); inverse (4.4641, −0.2679).</div>')
    H.append(r)
    for cid in ['tb2-36', 'tb2-37']: H.append(card(cid))

    # 7 registration
    H.append(lesson('Image registration: lining up two images of the same scene',
        'Two images of the same thing (e.g. MRI and PET of one patient, or satellite photos taken months apart) are slightly shifted, rotated or stretched relative to each other. Registration warps the <b>input</b> image so it lies exactly on top of the <b>reference</b> image.',
        '<div class="cols"><div><ol class="how"><li>Pick <b>tie points</b> (control points): the same feature seen in both images, e.g. a corner of a building. You know where it is in the input, (v, w), and in the reference, (x, y).</li>'
        '<li>Assume the <b>bilinear model</b>: \\(x=c_1v+c_2w+c_3vw+c_4\\), \\(y=c_5v+c_6w+c_7vw+c_8\\) — eight unknown numbers.</li>'
        '<li>Each tie point gives two equations (one for x, one for y) → <b>4 tie points</b> give the 8 equations needed.</li>'
        '<li>Use the fitted model to move every input pixel (with interpolation).</li></ol></div>'
        '<div><p><b>Example</b> (the practice card below): tie points (0,0)→(1,2), (0,10)→(2,13), (10,0)→(11,1), (10,10)→(13,12) give c₁…c₄ = 1, 0.1, 0.01, 1 and c₅…c₈ = −0.1, 1.1, 0, 2. So the input point (5, 5) belongs at (6.75, 7) in the reference.</p>'
        '<p><b>If the result is not good enough:</b> split the images into smaller pieces and register each piece with its own four tie points, or use a higher-order (polynomial) model.</p></div></div>',
        use='theory (why 4 tie points? what is the model?) and the c₁…c₈ computation (Equation app, Simul Equation with 4 unknowns, twice).', tag='7'))
    H.append(card('dr-reg'))

    # 8 transforms in matrix form
    H.append(lesson('Image transforms in matrix form (T = A F A)',
        'An image transform (the DFT is one) rewrites an image as a sum of fixed <b>pattern images</b>, with one coefficient per pattern saying “how much of this pattern is in the image”. When the transform is separable and symmetric, all coefficients come out of two matrix products.',
        '<div class="cols"><div>'
        '<div class="formula">\\(T=A\\,F\\,A\\)  (forward),   \\(F=B\\,T\\,B\\)  (inverse, \\(B=A^{-1}\\))<span class="say">F = the n×n image, A = the transform matrix (row u holds the 1-D pattern number u). Multiplying on the left transforms every column, on the right every row.</span></div>'
        '<p><b>Example (Haar, 2×2):</b> \\(A=\\tfrac1{\\sqrt2}\\begin{bmatrix}1&1\\\\1&-1\\end{bmatrix}\\), \\(F=\\begin{bmatrix}4&-1\\\\2&3\\end{bmatrix}\\). Then \\(T=AFA^T=\\begin{bmatrix}4&2\\\\-1&3\\end{bmatrix}\\). The top-left 4 is the average-type term: (4 − 1 + 2 + 3)/2.</p></div>'
        '<div><p><b>Basis images.</b> The same idea one pattern at a time: each coefficient = sum of (pattern × image) pixel by pixel. For 2×2 images the four patterns are “all +”, “left − right”, “top − bottom”, “checkerboard”. The image is rebuilt as Σ coefficient × pattern; keeping only the largest coefficients gives a good approximation — that is how transform compression works.</p>'
        '<p>The <b>DFT</b> is this with complex patterns (cosines and sines); its kernel is separable and symmetric, so F<sub>DFT</sub> = D<sub>m</sub> F D<sub>n</sub> (Chapter 4, Quiz-1 Q3).</p></div></div>',
        use='Compre 2025 Q4 (both parts), Quiz-1 2026 Q3 (DFT by matrices).', tag='8'))
    d = card('d25q4')
    d = set_solution(d, walk([
        ('Left product: transform the columns', r'\(HF=\tfrac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}\begin{bmatrix}4&-1\\2&3\end{bmatrix}=\tfrac1{\sqrt2}\begin{bmatrix}6&2\\2&-4\end{bmatrix}\)', None),
        ('Right product: transform the rows', r'\(\tfrac1{\sqrt2}\begin{bmatrix}6&2\\2&-4\end{bmatrix}\cdot\tfrac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix}=\tfrac12\begin{bmatrix}8&4\\-2&6\end{bmatrix}\)', None),
        ('Simplify', r'\(\tfrac12\begin{bmatrix}8&4\\-2&6\end{bmatrix}=\begin{bmatrix}4&2\\-1&3\end{bmatrix}\). (The two \(1/\sqrt2\) factors make ½.)', None),
    ]) + r'<div class="ansbig">\(F=\begin{bmatrix}4&2\\-1&3\end{bmatrix}\)</div>')
    H.append(d)
    H.append(card('d25q4a'))

    # 9 statistics
    H.append(lesson('Mean and variance of an image',
        'The mean is the average grey level (overall brightness). The variance (and its square root, the standard deviation σ) measures how spread out the grey levels are (contrast).',
        '<div class="cols"><div>'
        '<div class="formula">\\(m=\\dfrac{\\text{sum of all pixels}}{\\text{number of pixels}}\\), \\(\\sigma^2=\\text{average of }(z-m)^2\\)<span class="say">With a histogram: \\(m=\\sum_k r_k\\,p(r_k)\\), \\(\\sigma^2=\\sum_k (r_k-m)^2p(r_k)\\), where p(r<sub>k</sub>) = (number of pixels with level r<sub>k</sub>) ÷ (all pixels).</span></div>'
        '<p><b>Example.</b> Image [1 2; 3 6]: mean = 12/4 = <b>3</b>; differences from 3: −2, −1, 0, 3 → squares 4, 1, 0, 9 → average = 14/4 = <b>3.5</b> = σ²; σ = 1.87.</p></div>'
        '<div><p><b>Why it matters:</b> a dark image has a small mean; a washed-out (low-contrast) image has a small σ. Histogram questions ask for these (Mid-sem 2023 Q1, 2024 Q1).</p><p><b>Calculator:</b> Statistics app, 1-Variable, Freq column = the counts → x̄ and σx (use σx, not sx).</p></div></div>',
        tag='9'))
    for cid in ['tb2-26', 'tb2-25', 'tb2-29']: H.append(card(cid))

    # 10 norms
    H.append(lesson('Norms and distance functions (appendix of the slides)',
        'A <b>norm</b> measures the size of a vector; the distance between two points is the norm of their difference. The three norms in your slides are exactly the three pixel distances of Section 2.5.',
        '<div class="cols"><div>'
        '<p><b>Example</b> x = (3, −4):</p><ul><li>1-norm ‖x‖₁ = |3| + |−4| = <b>7</b> (→ D<sub>4</sub>)</li><li>2-norm ‖x‖₂ = √(9 + 16) = <b>5</b> (→ D<sub>e</sub>)</li><li>∞-norm ‖x‖<sub>∞</sub> = max(3, 4) = <b>4</b> (→ D<sub>8</sub>)</li></ul>'
        '<p>Always ‖x‖<sub>∞</sub> ≤ ‖x‖₂ ≤ ‖x‖₁ (4 ≤ 5 ≤ 7). The points with norm 1 form a diamond (1-norm), a circle (2-norm), a square (∞-norm).</p>'
        '<p><b>Frobenius norm</b> of a matrix: square every entry, add, take the square root (the 2-norm of the matrix written as one long vector).</p></div>'
        '<div><p><b>A distance function</b> (metric) must (1) never be negative and be 0 only for the same point, (2) be symmetric: d(p, q) = d(q, p), (3) obey the triangle rule: going via r is never shorter, d(p, q) ≤ d(p, r) + d(r, q). D<sub>e</sub>, D<sub>4</sub>, D<sub>8</sub> all satisfy these.</p>'
        '<p><b>Inner product</b> ⟨x, y⟩ = x₁y₁ + … + x<sub>n</sub>y<sub>n</sub>; ‖x‖₂ = √⟨x, x⟩.</p></div></div>',
        tag='10'))
    H.append('</section>')
    return '\n'.join(H)
