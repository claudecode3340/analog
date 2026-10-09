"""Numbers for every card added to the guide, computed independently. Run: python3 tools/verify_new.py"""
import numpy as np, math
np.set_printoptions(precision=4, suppress=True)
R = {}
# 2.2
cones = 337000; side = math.sqrt(cones); cells = 2 * side - 1; cone_mm = 1.5 / cells
R['tb2-2'] = dict(side=side, cells=cells, cone_um=cone_mm * 1000, dot_mm=200 * cone_mm / 17)
R['tb2-3'] = 2.998e8 / 60 / 1000
R['tb2-5'] = dict(lpmm=2048 / 50 / 2, dpi=2048 / 2)
fov = 7 * 500 / 35; R['tb2-6'] = dict(fov_mm=fov, px_mm=1024 / fov, lp_mm=1024 / fov / 2)
d = 500 * 200 / 1000; R['tb2-8'] = dict(elements=500 * 5 * 2, chip_mm=d)
R['tb2-10'] = 1125 * (1125 * 16 / 9) * 24 * 30 * 7200
R['tb2-12'] = max(k for k in range(1, 9) if 256 / 2 ** k > 8)
R['store'] = dict(bits=1024 * 1024 * 8, MB=1024 * 1024 * 8 / 8 / 2 ** 20)
# quantization rms (truncation to multiples of 16)
for key, data in [('s18q6', [255, 118, 129, 182, 18, 178, 82, 53]), ('m23q3', [208, 110, 129, 184, 28, 178, 82, 55])]:
    f = np.array(data, float)
    for nm, q in [('trunc', np.floor(f / 16) * 16), ('mid', np.floor(f / 16) * 16 + 8)]:
        e = q - f; R[f'{key}_{nm}'] = dict(q=q.astype(int).tolist(), e=e.astype(int).tolist(), sse=(e ** 2).sum(), rms=math.sqrt((e ** 2).mean()), snr=math.sqrt((q ** 2).sum() / (e ** 2).sum()), sumq2=(q ** 2).sum())
# composite affine example
S = np.diag([2, 2, 1.]); T = np.array([[1, 0, 1], [0, 1, 0], [0, 0, 1.]]); p = np.array([1, 1, 1.])
R['tb2-36'] = dict(TS=(T @ S @ p)[:2].tolist(), ST=(S @ T @ p)[:2].tolist())
# registration
V4 = [(0, 0), (0, 10), (10, 0), (10, 10)]; X4 = [(1, 2), (2, 13), (11, 1), (13, 12)]
M = np.array([[v, w, v * w, 1] for v, w in V4], float)
cx = np.linalg.solve(M, [a for a, _ in X4]); cy = np.linalg.solve(M, [b for _, b in X4])
R['dr-reg'] = dict(cx=cx.tolist(), cy=cy.tolist(), map55=[cx @ [5, 5, 25, 1], cy @ [5, 5, 25, 1]])
# end-sem 2025 Q4(a) basis images
H = [np.array(m) / 2 for m in ([[1, 1], [1, 1]], [[1, -1], [1, -1]], [[1, 1], [-1, -1]], [[1, -1], [-1, 1]])]
f = np.array([[6, 4], [2, 1.]]); t = [float((h * f).sum()) for h in H]
R['d25q4a'] = dict(t=t, recon=(t[0] * H[0] + t[2] * H[2]).tolist(), full=sum(ti * h for ti, h in zip(t, H)).tolist())
# median nonlinear
a = np.array([1, 5, 9]); b = np.array([4, 2, 2]); R['tb2-24'] = dict(med_sum=float(np.median(a + b)), sum_med=float(np.median(a) + np.median(b)))
# end-sem 2025 Q6
j = np.array([[3, 4, 3, 7, 7, 6], [4, 3, 4, 7, 6, 7], [0, 1, 0, 3, 4, 3], [0, 0, 1, 3, 3, 4], [1, 0, 0, 4, 4, 3], [3, 4, 3, 3, 4, 3]])
k = np.floor(j ** 2 / 7 + 0.5).astype(int)
R['d25q6'] = dict(J1=(j >= 5).astype(int).tolist(), J2=(j <= 1).astype(int).tolist(), k=k.tolist(), kvals={int(r): int(np.floor(r * r / 7 + .5)) for r in range(8)})
# e23 Q3b MSB plane
f4 = np.array([[1, 7, 10, 10], [6, 13, 15, 15], [6, 13, 15, 15], [1, 7, 10, 10]]); R['e23q3b'] = (f4 >> 3 & 1).tolist()
# piecewise linear 2019
def pw(r): pts = [(0, 0), (30, 20), (180, 210), (255, 255)]
pts = [(0, 0), (30, 20), (180, 210), (255, 255)]
def T(r):
    for (r1, s1), (r2, s2) in zip(pts, pts[1:]):
        if r <= r2: return s1 + (s2 - s1) * (r - r1) / (r2 - r1)
R['s19q6'] = dict(slopes=[(s2 - s1) / (r2 - r1) for (r1, s1), (r2, s2) in zip(pts, pts[1:])], T10=T(10), T100=T(100), T200=T(200))
# contrast stretch of the 2021 quiz image
q21 = np.array([[4, 2, 3, 2, 5], [1, 1, 2, 3, 4], [1, 3, 2, 3, 4], [2, 2, 3, 1, 3], [2, 2, 1, 1, 4]])
R['dr-stretch'] = np.floor(7 * (q21 - 1) / 4 + 0.5).astype(int).tolist()
R['dr-thresh'] = dict(mean=q21.mean(), img=(q21 > q21.mean()).astype(int).tolist())
R['dr-stats'] = dict(mean=q21.mean(), var=q21.var(), std=q21.std())
# log / gamma
R['dr-log'] = dict(c10=255 / math.log10(256), s100=255 / math.log10(256) * math.log10(101), cln=255 / math.log(256))
R['dr-gamma'] = dict(s=255 * 0.5 ** 0.4, s25=255 * (100 / 255) ** 2.5)
# bit plane reconstruction
R['dr-top'] = dict(r=214, bin=format(214, '08b'), top2=214 & 0b11000000, top3=214 & 0b11100000, top4=214 & 0b11110000)
# equalize twice
nk = np.array([24, 48, 96, 360, 420, 288, 192, 108])
def eq(nk): s = np.floor(7 * np.cumsum(nk) / nk.sum() + 0.5).astype(int); h = np.zeros(8, int); np.add.at(h, s, nk); return s, h
s1, h1 = eq(nk); s2, h2 = eq(h1); R['tb3-7'] = dict(s1=s1.tolist(), h1=h1.tolist(), s2=s2.tolist(), h2=h2.tolist())
# local enhancement (G&W Ex 3.12 style)
mG, sG = 161, 103; k0, k1, k2, k3, C = 0, 0.25, 0, 0.1, 22.8
cases = [(50, 5), (50, 20), (200, 8)]
R['dr-local'] = [dict(m=m, s=s, boost=(k0 * mG <= m <= k1 * mG) and (k2 * sG <= s <= k3 * sG)) for m, s in cases]
# separable advantage
R['dr-sep'] = {n: n * n / (2 * n) for n in [3, 7, 11, 21]}
# 1-D correlation/convolution (slide figure)
f1 = np.array([0, 0, 0, 1, 0, 0, 0, 0]); w1 = np.array([1, 2, 4, 2, 8])
fp = np.pad(f1, 2); corr = np.array([sum(w1[s + 2] * fp[x + 2 + s] for s in range(-2, 3)) for x in range(8)])
conv = np.array([sum(w1[s + 2] * fp[x + 2 - s] for s in range(-2, 3)) for x in range(8)])
R['sl-1d'] = dict(corr=corr.tolist(), conv=conv.tolist(), full_len=8 + 5 - 1)
# 2-D impulse with w = 1..9
f2 = np.zeros((5, 5)); f2[2, 2] = 1; w2 = np.arange(1, 10).reshape(3, 3)
fp2 = np.pad(f2, 1); c2 = np.array([[(w2 * fp2[i:i + 3, j:j + 3]).sum() for j in range(5)] for i in range(5)])
cv2 = np.array([[(np.rot90(w2, 2) * fp2[i:i + 3, j:j + 3]).sum() for j in range(5)] for i in range(5)])
R['sl-2d'] = dict(corr=c2[1:4, 1:4].astype(int).tolist(), conv=cv2[1:4, 1:4].astype(int).tolist())
# Gaussian kernels
s = np.arange(-1, 2); G1 = np.exp(-(s[:, None] ** 2 + s[None, :] ** 2) / 2)
R['sl-gauss'] = dict(G=G1.tolist(), sum=G1.sum(), norm=(G1 / G1.sum()).tolist())
R['tb3-27'] = dict(sigma=math.sqrt(4), size=3 + 3 * 2)
R['tb3-28'] = dict(sigma=math.sqrt(1.5 ** 2 + 2 ** 2 + 4 ** 2), size=3 + 5 + 7 - 2)
R['six'] = {sg: (lambda n: n if n % 2 else n + 1)(math.ceil(6 * sg)) for sg in [0.7, 1, 1.5, 3.5]}
R['tb3-35'] = {q: (lambda n: n if n % 2 else n + 1)(math.ceil(q * math.sqrt(10))) for q in [3, 5, 9]}
# median
P = np.array([[10, 12, 255], [11, 0, 13], [12, 14, 11]]); R['dr-med'] = dict(med=float(np.median(P)), mean=P.mean())
# derivatives (slide/book Fig 3.44 profile)
prof = np.array([6, 6, 6, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6])
R['sl-deriv'] = dict(d1=(prof[1:] - prof[:-1]).tolist(), d2=(prof[2:] - 2 * prof[1:-1] + prof[:-2]).tolist())
# highboost from Laplacian (tb3-42)
patch = np.array([[2, 3, 4], [3, 9, 5], [4, 5, 6]], float)
lap8 = patch.sum() - 9 * patch[1, 1]; box = patch.mean()
R['tb3-42'] = dict(f_minus_lap=patch[1, 1] - lap8, highboost9=patch[1, 1] + 9 * (patch[1, 1] - box))
# unsharp / highboost at one pixel with a 3x3 box
R['dr-unsharp'] = dict(box=box, mask=patch[1, 1] - box, k1=patch[1, 1] + (patch[1, 1] - box), k3=patch[1, 1] + 3 * (patch[1, 1] - box))
# Sobel + Roberts at one pixel
z = np.array([[1, 2, 3], [4, 5, 6], [9, 9, 9]], float)
gx = (z[2] * [1, 2, 1]).sum() - (z[0] * [1, 2, 1]).sum(); gy = (z[:, 2] * [1, 2, 1]).sum() - (z[:, 0] * [1, 2, 1]).sum()
R['dr-sobel'] = dict(gx=gx, gy=gy, M=math.hypot(gx, gy), approx=abs(gx) + abs(gy), rob=[z[2, 2] - z[1, 1], z[2, 1] - z[1, 2]])
# Laplacian of single pixel sharpen
R['dr-lapsharp'] = dict(lap4=patch[0, 1] + patch[2, 1] + patch[1, 0] + patch[1, 2] - 4 * patch[1, 1])
# Ch4
R['tb4-7'] = dict(freqs=[0.5, 2, 4], nyq=8)
R['tb4-30'] = dict(periods=[2, 3, 4], freqs=[1 / 2, 1 / 3, 1 / 4])
R['tb4-36'] = dict(P=2 * 3, ratio='PQ/MN')
# tb4-21 stripes: period 4 px in M=... spikes at u = M/4
M = 16; x = np.arange(M); str2 = ((x // 2) % 2).astype(float); F = np.abs(np.fft.fft(str2)); R['tb4-21'] = dict(nonzero=[int(u) for u in np.nonzero(F > 1e-9)[0]], F=F.round(3).tolist())
str1 = (x % 2).astype(float); F1 = np.abs(np.fft.fft(str1)); R['tb4-21b'] = [int(u) for u in np.nonzero(F1 > 1e-9)[0]]
# tb4-44: conj phase reflects
f = np.random.default_rng(1).integers(0, 9, (4, 4)).astype(float); Fz = np.fft.fft2(f); g = np.real(np.fft.ifft2(np.abs(Fz) * np.exp(-1j * np.angle(Fz))))
R['tb4-44'] = bool(np.allclose(g, np.roll(np.flip(f), 1, axis=(0, 1))))
# tb4-50 / 4-51
R['tb4-51'] = 'H = -4 + 2cos(2pi u/M) + 2cos(2pi v/N)'
for k, v in R.items(): print(k, v)
