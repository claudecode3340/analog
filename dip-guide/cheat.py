"""The cheat sheet, rebuilt: one formula per row, typeset with MathJax, each with a short plain-words note;
topic blocks in two columns; the look-up tables (Gaussian weights, roots of unity, Gray code, D3/D4) as real tables."""
import math
from lib import table, gsvg

ALL = lambda n, m, c: {(i, j): c for i in range(n) for j in range(m)}


def F(label, tex, say=''):
    """one row: label | formula | plain words. tex starting with '!' is raw HTML, otherwise TeX (display style)."""
    v = tex[1:] if tex.startswith('!') else '\\(\\displaystyle ' + tex.replace('<', '\\lt ').replace('>', '\\gt ') + '\\)'
    return f'<div class="fx"><div class="fk">{label}</div><div class="fv">{v}</div><div class="fs">{say}</div></div>'


def B(title, *rows, tag='', extra='', wide=False):
    return f'<div class="sb{" sbw" if wide else ""}"><h4>{title}{f" <span class=sbt>{tag}</span>" if tag else ""}</h4>' + ''.join(rows) + extra + '</div>'


def side(title, *blocks):
    return f'<h3 class="sheet-side">{title}</h3><div class="sheet-grid">' + ''.join(blocks) + '</div>'


def gauss_table():
    rows = []
    for s in (0.5, 0.7, 0.8, 1, 1.5, 2):
        a = math.exp(-1 / (2 * s * s)); rows.append([f'σ = {s}', f'{a:.4f}', f'{a * a:.4f}', f'{(1 + 2 * a) ** 2:.4f}'])
    return table(['σ', 'edge a = e<sup>−1/2σ²</sup>', 'corner a²', 'sum (1 + 2a)²'], rows)


def roots_table():
    def w(n, k):
        z = complex(math.cos(2 * math.pi * k / n), -math.sin(2 * math.pi * k / n))
        a = round(z.real, 4) + 0.0; b = round(z.imag, 4) + 0.0
        g = lambda v: f'{abs(v):g}'
        if b == 0: return f'{a:g}'.replace('-', '−')
        im = ('' if abs(b) == 1 else g(b)) + 'i'
        if a == 0: return ('−' if b < 0 else '') + im
        return f'{a:g}'.replace('-', '−') + (' − ' if b < 0 else ' + ') + im
    rows = [[f'n = {n}'] + [w(n, k) for k in range(n)] + [''] * (8 - n) for n in (3, 4, 5, 6, 8)]
    return table(['W<sub>n</sub><sup>k</sup>'] + [f'k = {k}' for k in range(8)], rows)


def section(card, old):
    H = ['''<section class="topic" id="sheet">
  <div class="eyebrow">Allowed: one handwritten A4 sheet — both sides</div>
  <h2>Formula sheet</h2>
  <div class="meta"><span class="chip hot">one formula per line</span><span class="chip ok">side 1 = Ch 1–3 · side 2 = Ch 4 + calculator</span></div>
  <p class="lede">Every formula the exam needs, written out properly, one per line, with what it means in plain words. Copy the formulas (middle column) onto your A4 sheet; the grey notes are for you to understand them. The tables at the end of each side (Gaussian weights, roots of unity, Gray code) save the most time in the exam.</p>''']

    H.append(side('Side 1 · Chapters 1–3',
        B('Conventions (read these first)',
          F('coordinates', '!x = row (going <b>down</b>), y = column (going <b>right</b>), both from 0', 'f(0, 0) is the top-left pixel'),
          F('matrix vs image', 'M_f(i,j)=f(i-1,\\,j-1)', 'matrix indices start at 1, image indices at 0'),
          F('linear index', '\\alpha = m\\,y + x', 'column-major: go down column 0 first'),
          F('grey levels', 'L = 2^k,\\quad r\\in\\{0,\\dots,L-1\\}', 'k bits per pixel'),
          F('storage', 'b = M\\,N\\,k\\ \\text{bits}', '÷ 8 for bytes'),
          F('correlation / convolution', '!☆ correlation: kernel <b>as printed</b>; ∗ convolution: kernel <b>rotated 180°</b>', 'identical when the kernel looks the same after a half-turn'),
          F('rounding', '!keep 4 decimals, round only at the very end', '')),
        B('Padding a row a b c …',
          F('zero', '!0 0 | a b c', 'outside = 0'),
          F('replicate', '!a a | a b c', 'copy the edge (“reflect / repeat the border” in old papers)'),
          F('symmetric', '!b a | a b c', 'mirror including the edge; for a 3×3 kernel = replicate'),
          F('output size', '\\text{same: } m\\times n\\qquad \\text{full: } (m+p-1)\\times(n+q-1)', 'p × q kernel')),
        B('Eye and image formation',
          F('rods', '!90–120 million · periphery · dim light (scotopic) · no colour', ''),
          F('cones', '!6–7 million · fovea · bright light (photopic) · colour', 'L 60–65 %, M 30–35 %, S 5–10 %'),
          F('image on retina', '\\frac{H}{d}=\\frac{h}{17\\,\\text{mm}}', 'object height H at distance d; lens–retina 17 mm'),
          F('thin lens', '\\frac1f=\\frac1{d_o}+\\frac1{d_i}', 'eye: d<sub>i</sub> fixed, f changes; camera: f fixed'),
          F('Weber ratio', '\\frac{\\Delta I_c}{I}', 'small = good brightness discrimination'),
          F('light', 'c=\\lambda\\nu,\\qquad E=h\\nu', 'γ, X, UV, visible, IR, microwave, radio'),
          F('image model', 'f=i\\cdot r,\\quad 0<r<1', 'illumination × reflectance'),
          F('illusions', '!Mach bands (over/undershoot at edges), simultaneous contrast', ''),
          F('sampling / quantisation', '!≤ 4 bits ⇒ false contours; Bayer filter 50 % green', '')),
        B('Interpolation',
          F('nearest neighbour', '(\\text{round}\\,u,\\ \\text{round}\\,v)', ''),
          F('bilinear', 'g=(1-s)(1-t)A+(1-s)t\\,B+s(1-t)\\,C+st\\,D', 'A top-left, B top-right, C bottom-left, D bottom-right; s down, t right'),
          F('bilinear (system)', 'g=a\\,u+b\\,v+c\\,uv+d', '4 neighbours → 4 equations'),
          F('quick values', '!centre of 4 pixels = their mean; midpoint of an edge = mean of 2', ''),
          F('bicubic', 'g=\\sum_{j=0}^{3}\\sum_{k=0}^{3}a_{jk}\\,u^j v^k', '16 neighbours')),
        B('Neighbours, paths, distances',
          F('N₄, N<sub>D</sub>, N₈', '!N₄: up/down/left/right · N<sub>D</sub>: 4 diagonals · N₈ = both', ''),
          F('m-adjacency', '!q ∈ N₄(p), <b>or</b> q ∈ N<sub>D</sub>(p) and N₄(p) ∩ N₄(q) has no pixel from V', 'takes a diagonal only when no 4-route exists'),
          F('Euclidean', 'D_e=\\sqrt{(x-s)^2+(y-t)^2}', 'circle'),
          F('city-block', 'D_4=|x-s|+|y-t|', 'diamond'),
          F('chessboard', 'D_8=\\max(|x-s|,\\,|y-t|)', 'square'),
          F('order', 'D_8\\le D_e\\le D_4', '')),
        B('Maths tools',
          F('linear operator', 'H[a f_1+b f_2]=a\\,H[f_1]+b\\,H[f_2]', 'max, median, |·|, square, threshold are NOT linear'),
          F('averaging K noisy images', '\\sigma^2_{\\bar g}=\\frac{\\sigma^2}{K}', 'noise std drops by √K'),
          F('scale to 0…K', 'f_s=K\\,\\frac{f-\\min f}{\\max(f-\\min f)}', ''),
          F('set ops on grey images', 'A^c=L-1-z,\\quad A\\cup B=\\max,\\quad A\\cap B=\\min', ''),
          F('mean, variance', 'm=\\sum z\\,p(z),\\qquad \\sigma^2=\\sum z^2p(z)-m^2', 'population variance (σ<sub>x</sub>, not s<sub>x</sub>)')),
        B('Affine transforms (homogeneous coordinates)',
          F('general', '\\begin{bmatrix}x\'\\\\y\'\\\\1\\end{bmatrix}=A\\begin{bmatrix}x\\\\y\\\\1\\end{bmatrix}', ''),
          F('scale / reflect', '\\begin{bmatrix}c_x&0&0\\\\0&c_y&0\\\\0&0&1\\end{bmatrix}', 'reflection: a −1'),
          F('rotate θ', '\\begin{bmatrix}\\cos\\theta&-\\sin\\theta&0\\\\\\sin\\theta&\\cos\\theta&0\\\\0&0&1\\end{bmatrix}', ''),
          F('translate', '\\begin{bmatrix}1&0&t_x\\\\0&1&t_y\\\\0&0&1\\end{bmatrix}', ''),
          F('shear', '\\begin{bmatrix}1&s_v&0\\\\0&1&0\\\\0&0&1\\end{bmatrix}\\quad\\begin{bmatrix}1&0&0\\\\s_h&1&0\\\\0&0&1\\end{bmatrix}', 'x′ = x + s<sub>v</sub>y · y′ = s<sub>h</sub>x + y'),
          F('A from 3 point pairs', 'A=Y\\,X^{-1}', 'points as columns with a row of 1s'),
          F('inverse mapping', '(x,y)=A^{-1}(x\',y\')', 'then interpolate in the input'),
          F('registration', 'x=c_1v+c_2w+c_3vw+c_4', 'same form for y; 4 tie points')),
        B('Intensity transforms',
          F('negative', 's=L-1-r', ''),
          F('log', 's=c\\,\\log(1+r)', 'expands dark values'),
          F('power (gamma)', 's=c\\,r^{\\gamma}', 'γ < 1 brightens, γ > 1 darkens'),
          F('contrast stretch', 's=(L-1)\\,\\frac{r-r_{min}}{r_{max}-r_{min}}', ''),
          F('threshold', '!r₁ = r₂, s₁ = 0, s₂ = L − 1', ''),
          F('bit plane k', 'b_k=\\left\\lfloor r/2^k\\right\\rfloor \\bmod 2', 'LSB = r odd; MSB = r ≥ 2<sup>k−1</sup>'),
          F('keep top t planes', '2^{k-t}\\left\\lfloor r/2^{k-t}\\right\\rfloor', '8-bit, t = 3 → multiples of 32'),
          F('Gray code', 'g=b\\oplus(b\\gg 1)', 'table below')),
        B('Histograms',
          F('equalisation', 's_k=\\text{round}\\!\\left[\\frac{L-1}{MN}\\sum_{j=0}^{k}n_j\\right]', 'running total × (L−1)/MN; round half up; merge equal s'),
          F('continuous', 's=(L-1)\\int_0^r p_r(w)\\,dw', 'output pdf uniform'),
          F('matching', 'G(z_q)=\\text{round}\\!\\left[(L-1)\\sum_{i=0}^{q}p_z(z_i)\\right]', 'for each s<sub>k</sub> pick the z with G(z) closest; <b>tie → smallest z</b>'),
          F('mapping', 'z=G^{-1}\\big(T(r)\\big)', 'r → s → z'),
          F('useful sums', '\\sum_{r=0}^{n} r=\\tfrac{n(n+1)}{2},\\quad \\sum r^2=\\tfrac{n(n+1)(2n+1)}{6}', ''),
          F('local enhancement', '!use local mean m<sub>S</sub> and σ<sub>S</sub> vs global m<sub>G</sub>, σ<sub>G</sub>: E·f if m<sub>S</sub> ≤ k₀m<sub>G</sub> and k₁σ<sub>G</sub> ≤ σ<sub>S</sub> ≤ k₂σ<sub>G</sub>', '')),
        B('Spatial filtering',
          F('correlation', 'g(x,y)=\\sum_{s,t}w(s,t)\\,f(x+s,\\,y+t)', ''),
          F('convolution', 'g(x,y)=\\sum_{s,t}w(s,t)\\,f(x-s,\\,y-t)', ''),
          F('separable', 'w=u\\,v^{T}', 'rank 1, every row a multiple of one row; cost ratio pq/(p+q)'),
          F('box', '\\tfrac19\\begin{bmatrix}1&1&1\\\\1&1&1\\\\1&1&1\\end{bmatrix}', ''),
          F('weighted mean', '\\tfrac1{16}\\begin{bmatrix}1&2&1\\\\2&4&2\\\\1&2&1\\end{bmatrix}=\\tfrac14[1\\,2\\,1]^T\\cdot\\tfrac14[1\\,2\\,1]', ''),
          F('Gaussian', 'G(s,t)=c\\,e^{-\\frac{s^2+t^2}{2\\sigma^2}}', 'divide by the sum; size ≈ 6σ; values below'),
          F('median', '!sort the window, take the middle value', 'kills salt-and-pepper noise; nonlinear')),
        B('Sharpening',
          F('1st difference', '\\frac{\\partial f}{\\partial x}=f(x+1)-f(x)', 'non-zero along ramps: thick edges'),
          F('2nd difference', '\\frac{\\partial^2 f}{\\partial x^2}=f(x+1)-2f(x)+f(x-1)', 'only at ramp start/end; zero crossing; double edge'),
          F('Laplacian', '\\nabla^2 f=f(x{+}1,y)+f(x{-}1,y)+f(x,y{+}1)+f(x,y{-}1)-4f(x,y)', '[0 1 0; 1 −4 1; 0 1 0]; with diagonals centre −8'),
          F('sharpen', 'g=f-\\nabla^2 f\\ \\ \\Rightarrow\\ \\begin{bmatrix}0&-1&0\\\\-1&5&-1\\\\0&-1&0\\end{bmatrix}', 'centre −4/−8 → subtract; centre +4/+8 → add'),
          F('kernel for f + c∇²f', 'K=\\delta+c\\,L', 'centre 1 − 4c, others c'),
          F('unsharp / highboost', 'g=f+c\\,(f-\\bar f)', 'c = 1 unsharp, c > 1 highboost'),
          F('one-pass unsharp (3×3 box)', '\\text{centre } 1+c-\\tfrac c9,\\ \\text{others } -\\tfrac c9', 'c = 1: ¹⁄₉[−1 … 17 … −1]'),
          F('gradient magnitude', 'M=\\sqrt{g_x^2+g_y^2}\\approx|g_x|+|g_y|', ''),
          F('Sobel', 'g_x=\\begin{bmatrix}-1&-2&-1\\\\0&0&0\\\\1&2&1\\end{bmatrix}\\quad g_y=\\begin{bmatrix}-1&0&1\\\\-2&0&2\\\\-1&0&1\\end{bmatrix}', 'g<sub>x</sub> (rows differ) finds horizontal edges'),
          F('Roberts', '\\begin{bmatrix}-1&0\\\\0&1\\end{bmatrix}\\quad\\begin{bmatrix}0&-1\\\\1&0\\end{bmatrix}', ''),
          F('highpass from lowpass', 'hp=\\delta-lp,\\quad br=lp_1+hp_2,\\quad bp=\\delta-br', 'derivative kernels sum to 0')),
        B('Look-up tables for side 1',
          '<p class="fs">Gaussian 3×3 kernel (c = 1): centre 1, edges a, corners a².</p>' + gauss_table() +
          '<p class="fs">3-bit Gray code (binary → Gray):</p>' + table(['b', '0', '1', '2', '3', '4', '5', '6', '7'], [['Gray', '000', '001', '011', '010', '110', '111', '101', '100']]) +
          '<p class="fs">Blurring 0/255 images with a 3×3 mean: 3 of 9 white → 85, 6 of 9 → 170 (straight edges); 4 or 5 of 9 → 113.3 / 141.7 (corners of four blocks).</p>', wide=True),
    ))

    H.append(side('Side 2 · Chapter 4, calculator, traps',
        B('Impulses and convolution',
          F('sifting', '\\sum_x f(x)\\,\\delta(x-a)=f(a)', 'δ picks one value'),
          F('identity', 'f*\\delta=f,\\qquad \\delta(\\alpha t)=\\frac{\\delta(t)}{|\\alpha|}', ''),
          F('linear convolution', 'g(x)=\\sum_k f(k)\\,h(x-k)', 'length L₁ + L₂ − 1; start = sum of starts'),
          F('circular (n-point)', '(f\\circledast h)(x)=\\sum_{k=0}^{n-1}f(k)\\,h\\big((x-k)\\bmod n\\big)', '= linear, with the tail added back onto the start'),
          F('circulant matrix', 'g=C_f\\,h', 'column j of C<sub>f</sub> = f shifted down j places'),
          F('linear from circular', 'n\\ge L_1+L_2-1', 'zero-pad both first'),
          F('2-D, one pixel', 'g(x,y)=\\sum_{k,l}f(k,l)\\,h\\big((x-k)\\bmod m,\\,(y-l)\\bmod n\\big)', 'build h̃, multiply entry-wise, add')),
        B('Fourier series and transforms',
          F('series coefficient', 'c_k=\\frac1T\\int_T f(t)\\,e^{-ik\\omega_0 t}\\,dt,\\quad \\omega_0=\\frac{2\\pi}{T}', 'real f: c<sub>−k</sub> = c<sub>k</sub>*; at a jump → midpoint'),
          F('Fourier transform', 'F(\\mu)=\\int_{-\\infty}^{\\infty}f(t)\\,e^{-i2\\pi\\mu t}\\,dt', ''),
          F('box ↔ sinc', 'A\\,\\text{rect}_W(t)\\ \\leftrightarrow\\ AW\\,\\frac{\\sin(\\pi\\mu W)}{\\pi\\mu W}', 'zeros at μ = k/W'),
          F('2-D rectangle L × W', 'F(u,v)=LW\\,\\frac{\\sin(\\pi uL)}{\\pi uL}\\,\\frac{\\sin(\\pi vW)}{\\pi vW}', ''),
          F('impulses', '\\delta(t)\\leftrightarrow 1,\\qquad \\delta(x\\mp a)\\leftrightarrow e^{\\mp j2\\pi ua}', 'pair at ±a → 2cos(2πua)'),
          F('cosine', '\\cos(2\\pi\\mu_0 t)\\leftrightarrow \\tfrac12\\big[\\delta(\\mu-\\mu_0)+\\delta(\\mu+\\mu_0)\\big]', ''),
          F('impulse train', '\\sum_n\\delta(t-n\\Delta T)\\leftrightarrow\\frac1{\\Delta T}\\sum_n\\delta\\!\\left(\\mu-\\frac{n}{\\Delta T}\\right)', ''),
          F('rules', 'f*h\\leftrightarrow FH,\\quad f(t-a)\\leftrightarrow e^{-i2\\pi\\mu a}F,\\quad f(\\alpha t)\\leftrightarrow \\tfrac1{|\\alpha|}F(\\mu/\\alpha)', 'narrow ↔ wide'),
          F('DTFT', 'F(e^{i\\omega})=\\sum_x f(x)\\,e^{-i\\omega x}', 'periodic, period 2π')),
        B('Sampling',
          F('Nyquist', '\\frac1{\\Delta T}>2\\,\\mu_{max}', 'strictly more than twice the highest frequency'),
          F('reading a frequency', '\\sin(2\\pi\\mu t)\\ \\Rightarrow\\ \\mu=\\frac{\\text{coefficient of }t}{2\\pi}', 'sin(8πt) → 4 Hz'),
          F('alias', '\\mu_{alias}=|\\mu_0-k\\,f_s|', '7 Hz at 10/s looks like 3 Hz'),
          F('in images', '!jaggies, moiré; blur before shrinking (anti-aliasing)', 'a finite image is never band-limited')),
        B('DFT (1-D)',
          F('forward', 'F(u)=\\sum_{x=0}^{n-1}f(x)\\,W_n^{ux},\\qquad W_n=e^{-i2\\pi/n}', 'no 1/n in front (your slides) — a printed formula wins'),
          F('inverse', 'f(x)=\\frac1n\\sum_{u=0}^{n-1}F(u)\\,W_n^{-ux}', ''),
          F('matrix form', '\\mathbf F=D_n\\mathbf f,\\quad D_n(u,x)=W_n^{\\,ux \\bmod n},\\quad D_n^{-1}=\\tfrac1n D_n^*', ''),
          F('D₄', 'D_4=\\begin{bmatrix}1&1&1&1\\\\1&-i&-1&i\\\\1&-1&1&-1\\\\1&i&-1&-i\\end{bmatrix}', ''),
          F('D₃', 'D_3=\\begin{bmatrix}1&1&1\\\\1&W&W^2\\\\1&W^2&W\\end{bmatrix},\\ W=-\\tfrac12-\\tfrac{\\sqrt3}2 i', '1 + W + W² = 0'),
          F('DC', 'F(0)=\\sum_x f(x)', ''),
          F('real f', 'F(n-u)=F^*(u)', 'compute F(0) … F(⌊n/2⌋) only'),
          F('centring', '!rotate by ⌊n/2⌋; (−1)<sup>x</sup> works only for even n', '')),
        B('DFT properties',
          F('shift', 'f([x-x_0]_n)\\leftrightarrow W_n^{u x_0}F(u)', '|F| unchanged'),
          F('modulation', 'W_n^{-u_0x}f(x)\\leftrightarrow F([u-u_0]_n)', ''),
          F('reversal', 'f([-x]_n)\\leftrightarrow F([-u]_n)', ''),
          F('convolution', 'f\\circledast h\\leftrightarrow F\\,H,\\qquad f\\,h\\leftrightarrow \\tfrac1n F\\circledast H', ''),
          F('conjugate', 'f^*(x)\\leftrightarrow F^*([-u]_n)', ''),
          F('symmetry', '!real & even ⇒ F real & even · real & odd ⇒ F imaginary & odd', '')),
        B('2-D DFT',
          F('definition', 'F(u,v)=\\sum_{x}\\sum_{y}f(x,y)\\,W_m^{ux}\\,W_n^{vy}', ''),
          F('matrix form', 'M_F=D_m\\,M_f\\,D_n', 'one entry: (row u of D<sub>m</sub>) · f · (column v of D<sub>n</sub>)'),
          F('indices', 'F(u,v)=M_F(u+1,\\,v+1)', ''),
          F('DC', 'F(0,0)=\\sum f=mn\\cdot\\text{mean}', ''),
          F('centring', '(-1)^{x+y}f(x,y)\\leftrightarrow F\\!\\left(u-\\tfrac M2,\\ v-\\tfrac N2\\right)', 'M, N even'),
          F('phase changes', 'F^*\\to f(-x,-y),\\quad -F\\to -f,\\quad jF\\to jf', '180° rotation / negative / imaginary'),
          F('frequency spacing', '\\Delta u=\\frac1{M\\,\\Delta T}', ''),
          F('pictures', '!shift: |F| same · rotate f ⇒ F rotates · phase carries the shapes · display log(1 + |F|)', '')),
        B('FFT',
          F('direct DFT', '(n-1)^2\\ \\text{mult},\\quad n(n-1)\\ \\text{add}', ''),
          F('radix-2 FFT', '\\tfrac n2\\log_2 n\\ \\text{mult},\\quad n\\log_2 n\\ \\text{add}', ''),
          F('one split', '2\\left(\\tfrac n2-1\\right)^2+\\tfrac n2\\ \\text{mult}', 'n = 32: 466 mult, 512 add'),
          F('butterfly (DIT)', 'F(k)=G(k)+W_n^kH(k),\\quad F\\!\\left(k+\\tfrac n2\\right)=G(k)-W_n^kH(k)', 'G = even samples, H = odd'),
          F('bit reversal (n = 8)', '!0 4 2 6 1 5 3 7', 'DIT input order'),
          F('DIF', 'g=f(x)+f\\!\\left(x+\\tfrac n2\\right),\\quad h=W_n^x\\left[f(x)-f\\!\\left(x+\\tfrac n2\\right)\\right]', 'output bit-reversed'),
          F('mixed radix n = kℓ', '!fill rows → DFT columns → × W<sub>n</sub><sup>pq</sup> → DFT rows → read columns', '')),
        B('Filtering in frequency (4.7)',
          F('filtering', 'g=\\mathcal F^{-1}\\{H\\,F\\}', ''),
          F('DC gain', 'H(0,0)=\\sum h', 'sum 0 ⇒ output mean 0'),
          F('kernel → H', 'w(s,t)\\ \\to\\ w\\,e^{\\,j2\\pi(us/M+vt/N)}', 'pairs: e<sup>jθ</sup> + e<sup>−jθ</sup> = 2cos θ; e<sup>jθ</sup> − e<sup>−jθ</sup> = 2j sin θ'),
          F('N₄ average', 'H=\\tfrac12\\left(\\cos\\tfrac{2\\pi u}{M}+\\cos\\tfrac{2\\pi v}{N}\\right)', 'lowpass'),
          F('Laplacian', 'H=2\\cos\\tfrac{2\\pi u}{M}+2\\cos\\tfrac{2\\pi v}{N}-4', 'highpass'),
          F('[1 2 1] / [−1 0 1]', '2+2\\cos\\psi\\qquad 2j\\sin\\theta', ''),
          F('Gaussian pair', 'A\\,e^{-\\mu^2/2\\sigma^2}\\leftrightarrow\\sqrt{2\\pi}\\,\\sigma A\\,e^{-2\\pi^2\\sigma^2t^2}', 'widths reciprocal'),
          F('steps', '!pad to 2M × 2N · × (−1)<sup>x+y</sup> · DFT · × H · IDFT · real part · × (−1)<sup>x+y</sup> · crop', '')),
        B('fx-991CW one-liners',
          F('define a matrix', '!TOOLS → MatA → OK → Define New', 'max 4 × 4, real numbers only'),
          F('one filtered pixel', '!Trn(W) × K, then add the diagonal', 'window W, kernel K'),
          F('whole image, separable kernel', 'T_u\\,f\\,T_v^{T}', 'T = tridiagonal band of the 1-D kernel'),
          F('Gaussian pixel', '\\frac{[a\\ 1\\ a]\\,W\\,[a\\ 1\\ a]^T}{(1+2a)^2}', ''),
          F('DFT coefficient', '\\text{Re}=C f,\\quad \\text{Im}=-S f', 'C, S = cos and sin tables'),
          F('roots of unity', '!Complex app, Degree: W<sub>n</sub><sup>k</sup> = 1∠(−360k/n)', ''),
          F('mean and σ', '!Statistics → 1-Var Results (turn Frequency on)', 'use σ<sub>x</sub>'),
          F('affine', 'A=Y\\times X^{-1}', '')),
        B('Look-up table for side 2 and traps',
          '<p class="fs">Roots of unity W<sub>n</sub><sup>k</sup> = cos(2πk/n) − i·sin(2πk/n):</p>' + roots_table() +
          '<ul class="traps"><li>Which index base: 0 or 1?</li><li>Correlation or convolution?</li><li>Which padding?</li><li>Divide the kernel by its sum.</li><li>2σ² (not σ²) in the Gaussian.</li>'
          '<li>DFT with or without 1/mn — the printed formula wins.</li><li>W has a minus sign.</li><li>Histogram: check Σn = MN.</li><li>Matching tie → smallest z.</li><li>Round only at the end; clip to 0…L−1 if the output is k-bit.</li>'
          '<li>Odd size: centring ≠ (−1)<sup>x+y</sup>.</li><li>Use σ<sub>x</sub>, not s<sub>x</sub>.</li></ul>', wide=True),
    ))
    H.append('</section>')
    return '\n'.join(H)


CSS = '''
.sheet-side{margin:28px 0 12px;font-size:1.25rem}
.sheet-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(36rem,1fr));gap:20px;align-items:start}
.sb{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 18px 10px}
.sb h4{margin:0 0 8px;font-size:1.08rem;color:var(--accent)}
.fx{display:grid;grid-template-columns:10.5rem 1fr;column-gap:16px;padding:9px 0;border-top:1px dashed var(--line);align-items:center}
.fx:first-of-type{border-top:0}
.fk{font-weight:600;font-size:.95rem}
.fv{font-size:1.05rem;line-height:1.5}
.fs{grid-column:2;color:var(--muted);font-size:.9rem;margin-top:2px}
.fs:empty{display:none}
.sb > p.fs{margin:10px 0 4px}
.sb .tw{margin:4px 0 8px}
.sbw{grid-column:1/-1}.sbw td{white-space:nowrap}
ul.traps{columns:3!important}
ul.traps{columns:2;margin:10px 0 4px;padding-left:1.2rem}
ul.traps li{margin:3px 0}
'''
