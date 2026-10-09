"""Every number shown in the DIP lessons comes from here. Run: python3 num/dip.py  ->  num/answers.json (+ asserts vs the keys).
Conventions (Gonzalez & Woods 4e, as on the slides): x = row index (down), y = column index (right), origin top-left.
Correlation g(x,y) = sum w(s,t) f(x+s, y+t); convolution uses f(x-s, y-t) (kernel rotated 180 degrees)."""
import json, math, itertools
from collections import deque
import numpy as np

OUT = {}
def put(k, v):
    OUT[k] = v.tolist() if isinstance(v, np.ndarray) else v
def close(a, b, tol=1e-3):
    return abs(a - b) <= tol * max(1, abs(b))

# ---------------------------------------------------------------- filtering helpers
def pad(f, a, b, mode):
    f = np.asarray(f, float)
    if mode == 'zero': return np.pad(f, ((a, a), (b, b)), mode='constant')
    if mode == 'replicate': return np.pad(f, ((a, a), (b, b)), mode='edge')
    if mode == 'mirror': return np.pad(f, ((a, a), (b, b)), mode='symmetric')
    raise ValueError(mode)

def correlate(f, w, mode='zero'):
    f = np.asarray(f, float); w = np.asarray(w, float)
    a, b = w.shape[0] // 2, w.shape[1] // 2
    P = pad(f, a, b, mode); g = np.zeros_like(f)
    for x in range(f.shape[0]):
        for y in range(f.shape[1]):
            g[x, y] = np.sum(w * P[x:x + 2 * a + 1, y:y + 2 * b + 1])
    return g

def convolve(f, w, mode='zero'):
    return correlate(f, np.rot90(np.asarray(w, float), 2), mode)

def band_matrix(n, u, mode='zero', conv=False):
    """1-D correlation (conv=False) with kernel u (odd length) as an n x n matrix acting on columns: g = A f."""
    u = list(u); a = len(u) // 2
    if conv: u = u[::-1]
    A = np.zeros((n, n))
    for i in range(n):
        for s in range(-a, a + 1):
            j = i + s
            if 0 <= j < n: A[i, j] += u[s + a]
            elif mode == 'replicate': A[i, min(max(j, 0), n - 1)] += u[s + a]
            elif mode == 'mirror':
                jj = -j - 1 if j < 0 else 2 * n - 1 - j
                A[i, jj] += u[s + a]
    return A

def hist_eq(nk, L):
    nk = np.asarray(nk, float); MN = nk.sum(); p = nk / MN
    s = (L - 1) * np.cumsum(p)
    return p, s, np.floor(s + 0.5).astype(int)   # round half up (as the calculator's Rnd does)

def hist_of(img, L):
    img = np.asarray(img).ravel(); return np.array([(img == k).sum() for k in range(L)])

def apply_map(img, m):
    return np.vectorize(lambda v: int(m[int(v)]))(np.asarray(img))

def hist_match(nk, target_counts, L):
    p, s, sr = hist_eq(nk, L)
    pz = np.asarray(target_counts, float); pz = pz / pz.sum()
    G = (L - 1) * np.cumsum(pz); Gr = np.floor(G + 0.5).astype(int)
    zmap = []
    for sk in sr:
        d = np.abs(sk - Gr); zmap.append(int(np.argmin(d)))   # argmin returns the smallest minimiser (the convention)
    rz = [zmap[k] for k in range(L)]
    return dict(s=s, sr=sr, G=G, Gr=Gr, r_to_z=rz)

# ---------------------------------------------------------------- pixel relationships
def neighbors(p, kind):
    x, y = p
    n4 = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    nd = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
    return n4 if kind == 4 else nd if kind == 'D' else n4 + nd

def adjacent(I, p, q, V, kind):
    """p, q both in V; 4-, 8- or m-adjacency (as in G&W 2.5)."""
    inside = lambda r: 0 <= r[0] < I.shape[0] and 0 <= r[1] < I.shape[1]
    if not (inside(p) and inside(q) and I[p] in V and I[q] in V): return False
    if kind == 4: return q in neighbors(p, 4)
    if kind == 8: return q in neighbors(p, 8)
    if q in neighbors(p, 4): return True
    if q in neighbors(p, 'D'):
        common = set(neighbors(p, 4)) & set(neighbors(q, 4))
        return not any(inside(r) and I[r] in V for r in common)
    return False

def shortest_path(I, p, q, V, kind):
    I = np.asarray(I); prev = {p: None}; dq = deque([p])
    while dq:
        c = dq.popleft()
        if c == q: break
        for n in neighbors(c, 8):
            if n not in prev and adjacent(I, c, n, V, kind):
                prev[n] = c; dq.append(n)
    if q not in prev: return None
    path = [q]
    while prev[path[-1]] is not None: path.append(prev[path[-1]])
    return path[::-1]

def components(I, region, V, kind):
    pix = [p for p in region if I[p] in V]; seen = set(); comps = []
    for p in pix:
        if p in seen: continue
        comp = []; dq = deque([p]); seen.add(p)
        while dq:
            c = dq.popleft(); comp.append(c)
            for n in pix:
                if n not in seen and adjacent(I, c, n, V, kind): seen.add(n); dq.append(n)
        comps.append(comp)
    return comps

D_e = lambda p, q: math.hypot(p[0] - q[0], p[1] - q[1])
D_4 = lambda p, q: abs(p[0] - q[0]) + abs(p[1] - q[1])
D_8 = lambda p, q: max(abs(p[0] - q[0]), abs(p[1] - q[1]))

# ================================================================ Lecture 2: image fundamentals
# lens: palm tree (slide): 15/100 = h/17
put('palm_h_mm', 15 / 100 * 17)
# G&W Problem 2.2: smallest discernible dot at 0.2 m (fovea 1.5 mm square, 337,000 cones, cones and spaces equal)
cones = 337000; per_side = math.sqrt(cones); cells = 2 * per_side - 1; cone_mm = 1.5 / cells
put('p22', dict(per_side=per_side, cone_um=cone_mm * 1000, dot_mm=0.2e3 * cone_mm / 17))
# 2.3: 60 Hz wavelength
put('p23_km', 2.998e8 / 60 / 1000)
# storage: b = M N k
put('store_1024_8', 1024 * 1024 * 8)
# 2.9 baud: 500 images 1024x1024, 8 bits, packets of 10 bits per byte
bits = 500 * 1024 * 1024 * 10
put('p29', dict(bits=bits, t3M=bits / 3e6, t30G=bits / 30e9))
# 2.5: 2048 px in 5 cm -> line pairs per mm; in 2 inch -> dpi
put('p25', dict(lp_mm=2048 / 2 / 50, dpi=2048 / 2))
# 2.10 HDTV: 1125 lines, 16:9, 24 bits, 30 frames/s (two fields of 1/60 s), 2 h
w = 1125 * 16 / 9
put('p210_bits', 1125 * w * 24 * 30 * 2 * 3600)
# linear index alpha = m*y + x (column-major), m rows
put('lin_idx', dict(m=3, n=4, x=2, y=1, alpha=3 * 1 + 2))
# 2.12 false contouring: K = 255, eye detects 8-level jumps -> visible when 256/2^k > 8 -> k <= 4  (highest k with contouring = 4)
put('p212_k', max(k for k in range(1, 9) if 256 / 2 ** k > 8))

# quantization: 8-bit levels and false contouring
put('levels', {k: 2 ** k for k in [1, 2, 3, 4, 5, 8]})

# DIP-26 Quiz 1 Q6: bilinear on 4x3 image enlarged to 7x5
f6 = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90], [100, 110, 120]], float)
A = np.array([[0, 0, 0, 1], [0, 1, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]], float)   # rows: (x,y)=(0,0),(0,1),(1,0),(1,1); unknowns a,b,c,d
coef = np.linalg.solve(A, np.array([10, 20, 40, 50], float))
put('q26_6', dict(a=coef[0], b=coef[1], c=coef[2], d=coef[3], g=coef[0] * .5 + coef[1] * .5 + coef[2] * .25 + coef[3]))
assert close(OUT['q26_6']['g'], 30)
# full enlarged image (useful for the picture)
def enlarge(f):
    m, n = f.shape; g = np.zeros((2 * m - 1, 2 * n - 1))
    for X in range(2 * m - 1):
        for Y in range(2 * n - 1):
            x, y = X / 2, Y / 2; x0, y0 = min(int(x), m - 2), min(int(y), n - 2); dx, dy = x - x0, y - y0
            g[X, Y] = (f[x0, y0] * (1 - dx) * (1 - dy) + f[x0 + 1, y0] * dx * (1 - dy) + f[x0, y0 + 1] * (1 - dx) * dy + f[x0 + 1, y0 + 1] * dx * dy)
    return g
put('q26_6_full', enlarge(f6))
# nearest-neighbour toy: 2x2 -> 4x4
put('nn_demo', dict(f=[[10, 20], [30, 40]]))

# ---------------- neighbours / adjacency / paths
# G&W Problem 2.18 = Midsem 2019-20 Q1 (p bottom-left, q top-right)
I18 = np.array([[3, 1, 2, 1], [2, 2, 0, 2], [1, 2, 1, 1], [1, 0, 1, 2]])
P, Q = (3, 0), (0, 3)
r18 = {}
for V in ([0, 1], [1, 2]):
    for kind in (4, 8, 'm'):
        path = shortest_path(I18, P, Q, V, kind)
        r18[f"{''.join(map(str, V))}_{kind}"] = None if path is None else dict(len=len(path) - 1, path=path)
put('p218', r18)
assert r18['01_4'] is None and r18['01_8']['len'] == 4 and r18['01_m']['len'] == 5
assert r18['12_4']['len'] == 6 and r18['12_8']['len'] == 4 and r18['12_m']['len'] == 6

# Quiz-1 2021-22 (5x5, 3-bit): distances, LSB, negative, m-path V={1,2}, histogram, equalization
q21 = np.array([[4, 2, 3, 2, 5], [1, 1, 2, 3, 4], [1, 3, 2, 3, 4], [2, 2, 3, 1, 3], [2, 2, 1, 1, 4]])
p21, q21q = (3, 0), (0, 3)
put('q21_dist', dict(De=D_e(p21, q21q), D4=D_4(p21, q21q), D8=D_8(p21, q21q)))
put('q21_lsb', q21 % 2); put('q21_neg', 7 - q21)
mp = shortest_path(q21, p21, q21q, [1, 2], 'm'); put('q21_mpath', dict(len=len(mp) - 1, path=mp))
nk21 = hist_of(q21, 8); p_, s_, sr_ = hist_eq(nk21, 8)
put('q21_hist', dict(nk=nk21, s=s_, sr=sr_, eq_img=apply_map(q21, sr_), eq_hist=hist_of(apply_map(q21, sr_), 8)))
assert list(nk21) == [0, 6, 8, 6, 4, 1, 0, 0] and list(sr_) == [0, 2, 4, 6, 7, 7, 7, 7]

# Quiz-1 2018-19: S1, S2 components (V={1}), adjacency, D4/D8 between boxed pixels
G19 = np.array([[0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [1, 0, 0, 1, 0, 0, 1, 0, 0, 1], [1, 0, 0, 1, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 1, 1, 1], [0, 0, 1, 1, 1, 0, 0, 1, 1, 1]])
S1 = [(x, y) for x in range(4) for y in range(1, 5)]; S2 = [(x, y) for x in range(4) for y in range(5, 9)]
res = {}
for kind in (4, 8, 'm'):
    res[f'S1_{kind}'] = len(components(G19, S1, [1], kind)); res[f'S2_{kind}'] = len(components(G19, S2, [1], kind))
    res[f'adj_{kind}'] = any(adjacent(G19, a, b, [1], kind) for a in S1 for b in S2)
b1, b2 = (3, 2), (0, 8)
res.update(D4=D_4(b1, b2), D8=D_8(b1, b2), De=D_e(b1, b2))
put('q19', res)
assert res['S1_4'] == 1 and res['S2_4'] == 3 and res['S2_8'] == 1 and not res['adj_4'] and res['adj_8'] and res['D4'] == 9 and res['D8'] == 6

# G&W Problem 2.14 (S1, S2 dashed boxes span all 5 rows in the book)
S1b = [(x, y) for x in range(5) for y in range(1, 5)]; S2b = [(x, y) for x in range(5) for y in range(5, 9)]
put('p214', {k: any(adjacent(G19, a, b, [1], k) for a in S1b for b in S2b) for k in (4, 8, 'm')})

# ---------------- mathematical tools
# set ops on grayscale: complement, union = max, intersection = min (3-bit)
Aset = np.array([[1, 5], [7, 2]]); Bset = np.array([[4, 3], [6, 6]])
put('sets', dict(A=Aset, B=Bset, Ac=7 - Aset, union=np.maximum(Aset, Bset), inter=np.minimum(Aset, Bset)))
# linear vs nonlinear: max is nonlinear (slide example style)
f1 = np.array([[0, 2], [2, 3]]); f2 = np.array([[6, 5], [4, 7]])
put('lin_test', dict(f1=f1, f2=f2, lhs=int((1 * f1 + (-1) * f2).max()), rhs=int(1 * f1.max() + (-1) * f2.max())))
# noise averaging: variance / K
put('avg_noise', dict(sigma=64, K=[1, 5, 10, 20, 50, 100], std=[64 / math.sqrt(K) for K in [1, 5, 10, 20, 50, 100]]))
# Endsem 2022-23 Q2: affine f(1,1)=(3,-4), f(0,2)=(-1,-1), f(-1,1)=(1,0)
X = np.array([[1, 0, -1], [1, 2, 1], [1, 1, 1]], float); Y = np.array([[3, -1, 1], [-4, -1, 0], [1, 1, 1]], float)
Aff = Y @ np.linalg.inv(X)
put('e23_affine', dict(A=Aff, f68=(Aff @ np.array([6, -8, 1.0]))[:2]))
# rotation by 30 degrees of (1, 0); scaling / translation composites
th = math.radians(30)
put('rot30', dict(c=math.cos(th), s=math.sin(th), p=[math.cos(th), math.sin(th)]))
# image registration: 4 tie points -> c1..c8 (illustrative)
V4 = [(0, 0), (0, 10), (10, 0), (10, 10)]; X4 = [(1, 2), (2, 13), (11, 1), (13, 12)]
M = np.array([[v, w_, v * w_, 1] for v, w_ in V4], float)
put('reg', dict(V=V4, X=X4, cx=np.linalg.solve(M, [x for x, _ in X4]), cy=np.linalg.solve(M, [y for _, y in X4])))

# ================================================================ Lecture 3: intensity transformations
L8 = 256
put('log_c', 255 / math.log10(256)); put('log_c_ln', 255 / math.log(256))
put('gamma_demo', dict(r=[0, 64, 128, 192, 255], g04=[round(255 * (r / 255) ** 0.4) for r in [0, 64, 128, 192, 255]],
                       g25=[round(255 * (r / 255) ** 2.5) for r in [0, 64, 128, 192, 255]]))
# Midsem 2019-20 Q6 piecewise linear (0,0)-(30,20)-(180,210)-(255,255)
pw = [(0, 0), (30, 20), (180, 210), (255, 255)]
def pwl(r):
    for (r1, s1), (r2, s2) in zip(pw, pw[1:]):
        if r <= r2: return s1 + (s2 - s1) * (r - r1) / (r2 - r1)
put('pw19', dict(pts=pw, slopes=[(s2 - s1) / (r2 - r1) for (r1, s1), (r2, s2) in zip(pw, pw[1:])], s100=pwl(100), s200=pwl(200)))
# bit planes: G&W Problem 3.4(b) 4-bit image
I34 = np.array([[0, 1, 8, 6], [2, 2, 1, 1], [1, 15, 14, 12], [3, 6, 9, 10]])
put('p34', {f'plane{k}': (I34 >> (k - 1)) & 1 for k in range(1, 5)})
put('bit194', dict(bits=format(194, '08b')))
# DIP-26 Quiz 1 Q2: quantize (round) then keep the top 3 bit planes; sum of row 1
f2q = np.array([[37.45, 214.02, 88.95, 155.72, 12.32], [223.78, 45.3, 166.9, 95.87, 71.4], [103.2, 251, 65, 129.7, 221], [18.1, 175.8, 92, 235.6, 53]])
Mq = np.floor(f2q + 0.5).astype(int); top3 = Mq & 0b11100000
put('q26_2', dict(M=Mq, top3=top3, row1=top3[1], sum=int(top3[1].sum())))
assert OUT['q26_2']['sum'] == 576
# Midsem 2024-25 Q3(i): Gray-coded LSB and MSB planes of a 3-bit 5x5 image
I243 = np.array([[7, 6, 1, 0, 2], [5, 5, 2, 3, 1], [4, 3, 1, 0, 2], [2, 3, 4, 7, 7], [1, 2, 4, 6, 6]])
gray = I243 ^ (I243 >> 1)
put('m24_3', dict(gray=gray, lsb=gray & 1, msb=(gray >> 2) & 1, bin_lsb=I243 & 1, bin_msb=(I243 >> 2) & 1))

# ---------------- histograms
# G&W Example 3.5 (3-bit 64x64)
nk35 = [790, 1023, 850, 656, 329, 245, 122, 81]
p35, s35, r35 = hist_eq(nk35, 8)
eqh = np.zeros(8, int)
for k in range(8): eqh[r35[k]] += nk35[k]
put('ex35', dict(nk=nk35, p=p35, s=s35, sr=r35, eq_nk=eqh, eq_p=eqh / 4096))
assert list(r35) == [1, 3, 5, 6, 6, 7, 7, 7]
# G&W Example 3.7 (matching)
pz37 = [0, 0, 0, .15, .20, .30, .20, .15]
m37 = hist_match(nk35, [int(x * 1000) for x in pz37], 8)
act = np.zeros(8, int)
for k in range(8): act[m37['r_to_z'][k]] += nk35[k]
put('ex37', dict(pz=pz37, G=m37['G'], Gr=m37['Gr'], r_to_z=m37['r_to_z'], s_to_z={int(s): m37['r_to_z'][k] for k, s in enumerate(r35)}, actual=act / 4096))
assert list(m37['Gr']) == [0, 0, 0, 1, 2, 5, 6, 7]
# DIP-26 Quiz 1 Q4: 3-bit 32x48
nk4 = [24, 48, 96, 360, 420, 288, 192, 108]; p4, s4, r4 = hist_eq(nk4, 8)
h4 = np.zeros(8, int)
for k in range(8): h4[r4[k]] += nk4[k]
put('q26_4', dict(nk=nk4, p=p4, s=s4, sr=r4, eq_nk=h4, ps6=h4[6] / 1536))
assert close(OUT['q26_4']['ps6'], 0.1875)
# Midsem 2019-20 Q2: 6x6 3-bit
I192 = np.array([[0, 0, 1, 4, 5, 4], [0, 1, 2, 5, 4, 3], [1, 2, 3, 4, 3, 1], [4, 5, 4, 3, 1, 0], [5, 4, 3, 1, 0, 0], [4, 4, 3, 1, 0, 0]])
nk192 = hist_of(I192, 8); p192, s192, r192 = hist_eq(nk192, 8)
put('m19_2', dict(nk=nk192, s=s192, sr=r192, img=apply_map(I192, r192), eq_hist=hist_of(apply_map(I192, r192), 8)))
# Endsem 2022-23 Q3a: 2-bit, 64x64
nk233 = [1813, 1506, 574, 203]; p233, s233, r233 = hist_eq(nk233, 4)
h233 = np.zeros(4, int)
for k in range(4): h233[r233[k]] += nk233[k]
put('e23_3', dict(nk=nk233, p=p233, s=s233, sr=r233, eq_p=h233 / 4096))
assert np.allclose(np.round(h233 / 4096, 2), [0, .44, .37, .19])
# Endsem 2025-26 Q3: histogram matching on an 8x8 3-bit image
F25 = np.array([[1, 5, 6, 7, 6, 4, 6, 5], [1, 6, 5, 4, 3, 6, 4, 2], [3, 2, 7, 6, 5, 7, 5, 7], [0, 5, 3, 3, 2, 3, 3, 6],
                [5, 2, 7, 5, 7, 5, 6, 5], [4, 7, 4, 2, 5, 4, 1, 4], [7, 4, 6, 6, 6, 7, 7, 7], [7, 6, 7, 5, 4, 6, 0, 6]])
tgt = [13, 12, 14, 14, 11, 0, 0, 0]
nk25 = hist_of(F25, 8); m25 = hist_match(nk25, tgt, 8)
g25 = apply_map(F25, m25['r_to_z'])
put('e25_3', dict(nk=nk25, s=m25['s'], sr=m25['sr'], G=m25['G'], Gr=m25['Gr'], r_to_z=m25['r_to_z'], g=g25))
key_g = np.array([[0, 2, 3, 4, 3, 1, 3, 2], [0, 3, 2, 1, 1, 3, 1, 0], [1, 0, 4, 3, 2, 4, 2, 4], [0, 2, 1, 1, 0, 1, 1, 3],
                  [2, 0, 4, 2, 4, 2, 3, 2], [1, 1, 1, 0, 2, 1, 0, 1], [4, 1, 3, 3, 3, 4, 4, 4], [4, 3, 4, 2, 1, 3, 0, 3]])
put('e25_3_keydiff', int((g25 != key_g).sum()))
# histogram statistics: ramp (2022-23 Q1) and triangle (2023-24 Q1)
r = np.arange(8); k23 = 3500 / r.sum(); H = k23 * r
m = (r * H).sum() / H.sum(); var = ((r - m) ** 2 * H).sum() / H.sum()
put('m23_1', dict(k=k23, mean=m, var=var, std=math.sqrt(var)))
assert close(k23, 125) and close(m, 5) and close(var, 3)
rr = np.arange(16); H24 = np.where(rr <= 7, rr, 15 - rr).astype(float); k24 = 5600 / H24.sum(); H24 *= k24
m24 = (rr * H24).sum() / H24.sum(); v24 = ((rr - m24) ** 2 * H24).sum() / H24.sum()
put('m24_1', dict(k=k24, H=H24, mean=m24, var=v24, std=math.sqrt(v24)))
# continuous matching (Midsem 2024-25 Q2(i)): p_r = 2-2r, p_z = 3z^2  -> s = 2r - r^2, G(z) = z^3 -> z = (2r - r^2)^(1/3)
put('m2425_2', dict(r=0.5, z=(2 * .5 - .25) ** (1 / 3)))
# G&W 3.11: p_r = 2r/(L-1)^2 -> s = r^2/(L-1)

# ================================================================ spatial filtering
# G&W Fig 3.29: 1-D correlation / convolution of an impulse
f1d = [0, 0, 0, 1, 0, 0, 0, 0]; w1d = [1, 2, 4, 2, 8]
c = np.correlate(np.pad(f1d, 2), w1d, 'valid'); v = np.convolve(f1d, w1d, 'same')
put('fig329', dict(corr=c, conv=v, full_corr=np.correlate(np.pad(f1d, 4), w1d, 'valid'), full_conv=np.convolve(f1d, w1d)))
# Midsem 2024-25 Q1: correlation vs convolution, zero padding, round to 3-bit (clip 0..7)
f241 = [[0, 2, 0], [3, 5, 2], [0, 4, 0]]; h241 = np.array([[1, 2, 1], [1, 2, 2], [2, 1, 3]]) / 14
cr = correlate(f241, h241); cv = convolve(f241, h241)
q3 = lambda g: np.clip(np.floor(g + 0.5), 0, 7).astype(int)
put('m2425_1', dict(corr=cr, conv=cv, corr_q=q3(cr), conv_q=q3(cv), corr14=correlate(f241, h241 * 14), conv14=convolve(f241, h241 * 14)))
# G&W 3.18 (impulse-like image) convolution with [1 2 1;2 4 2;1 2 1]
f318 = np.zeros((5, 5)); f318[1:4, 2] = 1; w121 = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
put('p318', dict(conv_full=np.array(__import__('numpy').round(np.real(np.fft.ifft2(np.fft.fft2(f318, (7, 7)) * np.fft.fft2(w121, (7, 7)))))), conv=convolve(f318, w121)))
# separable: [1 2 1;2 4 2;1 2 1] = [1 2 1]^T [1 2 1]; advantage C = pq/(p+q)
put('sep_adv', {f'{p}x{p}': p * p / (2 * p) for p in [3, 5, 11, 21]})
put('p322b', dict(w=[[1, 3, 1], [2, 6, 2]], v=[1, 2], wt=[1, 3, 1]))
put('p322a_rank', int(np.linalg.matrix_rank(np.outer([1, 2, 1], [2, 1, 1, 3]))))
# Gaussian kernel: c = 1, sigma = 1 (3x3) and sigma = 0.7 (Quiz)
def gauss(sig, n=3):
    a = n // 2; s = np.arange(-a, a + 1)
    G = np.exp(-(s[:, None] ** 2 + s[None, :] ** 2) / (2 * sig ** 2)); return G, G.sum()
G1, S1g = gauss(1.0); put('gauss1', dict(G=G1, sum=S1g))
G07, S07 = gauss(0.7); put('gauss07', dict(G=G07, sum=S07, v=[math.exp(-1 / (2 * .49)), 1, math.exp(-1 / (2 * .49))]))
assert close(S1g, 4.8976) and close(S07, 2.9612)
# DIP-26 Quiz 1 Q1: Gaussian (sigma 0.7) correlation with replicate padding, g(0,3)
fq1 = np.array([[2, 1.5, 1, 3.2], [4, 4.3, math.pi, 2], [3, 0.5, math.e, math.sqrt(2)]])
gq1 = correlate(fq1, G07 / S07, 'replicate'); put('q26_1', dict(g=gq1, g03=gq1[0, 3]))
assert close(gq1[0, 3], 2.6345, 1e-4)
vv = np.array(OUT['gauss07']['v']); Ar = band_matrix(3, vv, 'replicate'); Ac = band_matrix(4, vv, 'replicate')
assert np.allclose(Ar @ fq1 @ Ac.T / vv.sum() ** 2, gq1)
put('q26_1_mat', dict(Ar=Ar, Ac=Ac, scale=vv.sum() ** 2))
# 6-sigma rule
put('six_sigma', {s: (lambda n: n if n % 2 else n + 1)(math.ceil(6 * s)) for s in [0.5, 1, 1.5, 3.5, 7]})

# 4x4 image used by the 2022-23 and 2023-24 midsems
I4 = np.array([[1, 2, 4, 5], [5, 2, 5, 2], [1, 1, 3, 6], [2, 4, 6, 7]], float)
W16 = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16; LAP4 = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
put('i4', dict(img=I4))
for name, f_, w_, mode in [('m23_2a', I4, W16, 'zero'), ('m23_2b', I4, LAP4, 'replicate'), ('m24_2a', I4, W16, 'replicate'), ('m24_2b', I4, LAP4, 'zero')]:
    put(name, correlate(f_, w_, mode))
# matrix (calculator) forms: smoothing = A F A^T ; Laplacian = D F + F D^T
for mode in ('zero', 'replicate'):
    A = band_matrix(4, [1, 2, 1], mode) / 4; D = band_matrix(4, [1, -2, 1], mode)
    put(f'mat121_{mode}', A); put(f'matD_{mode}', D)
    assert np.allclose(A @ I4 @ A.T, correlate(I4, W16, mode)) and np.allclose(D @ I4 + I4 @ D.T, correlate(I4, LAP4, mode))
J = band_matrix(4, [1, 1, 1], 'zero'); LAP8 = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
assert np.allclose(J @ I4 @ J.T - 9 * I4, correlate(I4, LAP8))
# Midsem 2018-19 Q2: 3x3 averaging on a 5x5 3-bit image (zero and replicate padding), rounded
I18b = np.array([[3, 7, 6, 2, 0], [2, 4, 6, 1, 1], [4, 7, 2, 5, 4], [3, 0, 6, 2, 1], [5, 7, 5, 1, 2]])
box = np.ones((3, 3)) / 9
for mode in ('zero', 'replicate', 'mirror'):
    g = correlate(I18b, box, mode); put(f'm18_2_{mode}', dict(g=g, r=np.floor(g + 0.5).astype(int)))
# Endsem 2025-26 Q2b: 3x3 average, replicate padding, round
F252 = np.array([[1, 2, 3, 2], [4, 2, 5, 1], [1, 2, 6, 3], [2, 6, 4, 7]])
g252 = correlate(F252, box, 'replicate'); put('e25_2b', dict(g=g252, r=np.floor(g252 + 0.5).astype(int)))
assert (np.floor(g252 + 0.5).astype(int) == np.array([[2, 3, 2, 2], [2, 3, 3, 3], [3, 4, 4, 4], [3, 4, 5, 5]])).all()
A3 = band_matrix(4, [1, 1, 1], 'replicate') / 3; assert np.allclose(A3 @ F252 @ A3.T, g252); put('e25_2b_A', A3 * 3)
# Quiz-2 2021-22 Q1: weighted average and Laplacian (centre +4) on the diagonal, zero padding, nearest integer
Iq2 = np.array([[4, 2, 3, 2], [1, 1, 2, 3], [1, 3, 2, 3], [2, 2, 3, 1]])
ga = correlate(Iq2, W16); gl = correlate(Iq2, -LAP4)
put('q21b_1', dict(avg=ga, lap=gl, avg_diag=[ga[i, i] for i in range(4)], lap_diag=[gl[i, i] for i in range(4)],
                   avg_diag_r=[int(np.floor(ga[i, i] + .5)) for i in range(4)]))
assert OUT['q21b_1']['avg_diag_r'] == [1, 2, 2, 1] and OUT['q21b_1']['lap_diag'][0] == 13   # the key prints 16 here
# Midsem 2023-24 Q2: Filter-1 (Laplacian) and Filter-2 on the non-zero 3x3 block of a 5x5 image
I5 = np.array([[0, 0, 0, 0, 0], [0, 15, 7, 0, 0], [0, 7, 15, 7, 0], [0, 0, 7, 15, 0], [0, 0, 0, 0, 0]])
F2 = np.array([[.01, .1, .01], [.1, .56, .1], [.01, .1, .01]])
g1 = correlate(I5, LAP4)[1:4, 1:4]; g2 = correlate(I5, F2)[1:4, 1:4]
put('m2324_2', dict(f1=g1, f2=g2, f2sum=F2.sum()))
assert (g1 == np.array([[-46, 2, 14], [2, -32, 2], [14, 2, -46]])).all() and close(g2[1, 1], 11.5)
# Midsem 2019-20 Q4: g = f + c * Laplacian -> K = delta + c * L (two Laplacian conventions)
put('m19_4', dict(K4=[[0, 'c', 0], ['c', '1-4c', 'c'], [0, 'c', 0]]))
# binary images with equal histograms, blurred with a 3x3 box (boundary pixels left as they are = the 2021 key)
def blur_hist(img, keep_border=True):
    g = correlate(img, box, 'zero')
    if keep_border:
        g[0, :], g[-1, :], g[:, 0], g[:, -1] = img[0, :], img[-1, :], img[:, 0], img[:, -1]
    vals, cnt = np.unique(np.floor(g + 0.5).astype(int), return_counts=True); return dict(zip(map(int, vals), map(int, cnt)))
def halves(n): a = np.zeros((n, n)); a[:, : n // 2] = 255; return a
def checker(n, blk): return np.array([[255 * (((x // blk) + (y // blk)) % 2 == 0) for y in range(n)] for x in range(n)], float)
q2h = blur_hist(halves(16)); q2c = blur_hist(checker(16, 4))
put('q21b_2', dict(halves=q2h, checker=q2c))
assert q2h == {0: 114, 85: 14, 170: 14, 255: 114} and q2c == {0: 62, 85: 48, 113: 18, 142: 18, 170: 48, 255: 62}
put('m23_6', dict(halves=blur_hist(halves(64)), checker=blur_hist(checker(64, 16))))
# derivatives of the G&W Fig 3.44 scan line
sl = [6, 6, 6, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6]
put('fig344', dict(f=sl, d1=[sl[i + 1] - sl[i] for i in range(1, len(sl) - 1)], d2=[sl[i + 1] + sl[i - 1] - 2 * sl[i] for i in range(1, len(sl) - 1)]))
# median example (G&W): (10,20,20,20,15,20,20,25,100) -> 20 ; salt-and-pepper demo
put('median', dict(vals=[10, 20, 20, 20, 15, 20, 20, 25, 100], med=int(np.median([10, 20, 20, 20, 15, 20, 20, 25, 100])), mean=float(np.mean([10, 20, 20, 20, 15, 20, 20, 25, 100]))))
# unsharp masking single kernel (G&W 3.41): g = f + k(f - box(f)) -> (1+k) delta - k box
put('unsharp_k1', (2 * np.eye(3)[1][:, None] * np.eye(3)[1][None, :] - box) * 9)
# Endsem 2022-23 Q4: Sobel Hy on a 10x10 image with a central 4x4 block of ones (zero padding, correlation)
B10 = np.zeros((10, 10)); B10[3:7, 3:7] = 1
Hy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
gy = correlate(B10, Hy); put('e23_4', dict(img=B10, g=gy))
key = np.zeros((10, 10)); key[2:4, 2:8] = [[1, 3, 4, 4, 3, 1]] * 2; key[6:8, 2:8] = [[-1, -3, -4, -4, -3, -1]] * 2
put('e23_4_matches_key', bool(np.allclose(gy, key)))
put('e23_4_conv', convolve(B10, Hy))
# Compre 2023-24 Q1: Sobel as two 1-D masks
put('c23_1', dict(gx1=[-1, 0, 1], gx2=[1, 2, 1]))
assert np.allclose(np.outer([-1, 0, 1], [1, 2, 1]), Hy)
# Roberts / Sobel on a 3x3 patch (gradient magnitude, |gx|+|gy|)
z = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
gx = (z[2, 0] + 2 * z[2, 1] + z[2, 2]) - (z[0, 0] + 2 * z[0, 1] + z[0, 2]); gyv = (z[0, 2] + 2 * z[1, 2] + z[2, 2]) - (z[0, 0] + 2 * z[1, 0] + z[2, 0])
put('sobel_patch', dict(z=z, gx=gx, gy=gyv, M=math.hypot(gx, gyv), M1=abs(gx) + abs(gyv)))
# Endsem 2025 Q2a: h with centre 8 -> sum 0 -> output mean 0
put('kernel_sum_zero', dict(h=[[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], sum=0))

json.dump(OUT, open(__file__.replace('dip.py', 'answers.json'), 'w'), indent=0, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
print('ok', len(OUT), 'entries; e25_3 differences from the key:', OUT['e25_3_keydiff'], '; e23_4 matches key:', OUT['e23_4_matches_key'])
