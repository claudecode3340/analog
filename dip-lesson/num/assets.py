"""Picture assets for the DIP lessons: every filtered image the lessons show is computed here with numpy, from
open-licensed test images (scikit-image data: camera CC0 by Lav Varshney, moon public domain, page/text public domain).
Point transforms (negative, gamma, log, stretching, bit planes, equalization) are NOT here: the lesson applies them
live with an SVG lookup table, so only the base image and its histogram are needed for those.
Run: python3 num/assets.py  →  assets/*.webp + assets/meta.json"""
import json, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'assets', 'src')
OUT = os.path.join(HERE, '..', 'assets')
rng = np.random.default_rng(435)
META = {}


def load(name, size=None):
    im = Image.open(os.path.join(SRC, name)).convert('L')
    if size: im = im.resize(size, Image.LANCZOS)
    return np.asarray(im, dtype=float)


def save(key, a, q=88, lossless=False):
    a8 = np.clip(np.round(a), 0, 255).astype(np.uint8)
    Image.fromarray(a8).save(os.path.join(OUT, key + '.webp'), 'WEBP', quality=q, lossless=lossless, method=6)
    META[key] = dict(w=a8.shape[1], h=a8.shape[0])
    return a8


def pad(f, a, b, mode):
    return np.pad(f, ((a, a), (b, b)), {'zero': 'constant', 'replicate': 'edge', 'mirror': 'symmetric'}[mode])


def correlate(f, w, mode='replicate'):
    w = np.asarray(w, float); p, q = w.shape; a, b = p // 2, q // 2
    fp = pad(f, a, b, mode); g = np.zeros_like(f, dtype=float)
    for s in range(p):
        for t in range(q):
            if w[s, t]: g += w[s, t] * fp[s:s + f.shape[0], t:t + f.shape[1]]
    return g


def median(f, n=3):
    a = n // 2; fp = pad(f, a, a, 'replicate')
    st = np.stack([fp[s:s + f.shape[0], t:t + f.shape[1]] for s in range(n) for t in range(n)])
    return np.median(st, axis=0)


def gauss_kernel(sig):
    n = int(np.ceil(6 * sig)) | 1; a = n // 2; s = np.arange(-a, a + 1)
    G = np.exp(-(s[:, None] ** 2 + s[None, :] ** 2) / (2 * sig ** 2)); return G / G.sum()


def scale_full(a):  # map min..max to 0..255 (how a Laplacian is shown)
    return (a - a.min()) / (a.max() - a.min()) * 255


cam = load('camera.png', (256, 256))
cam8 = save('cam', cam, q=92)
META['cam']['hist'] = np.bincount(cam8.ravel(), minlength=256).tolist()

# spatial resolution: fewer samples, shown at the same size
for n in [128, 64, 32]:
    small = Image.fromarray(cam8).resize((n, n), Image.BOX)
    save(f'cam_{n}', np.asarray(small.resize((256, 256), Image.NEAREST), float))
# interpolation: 64x64 enlarged 4x three ways
small = Image.fromarray(cam8).resize((64, 64), Image.BOX)
for k, m in [('nearest', Image.NEAREST), ('bilinear', Image.BILINEAR), ('bicubic', Image.BICUBIC)]:
    save(f'interp_{k}', np.asarray(small.resize((256, 256), m), float))

# averaging K noisy images: noise std falls as 1/sqrt(K)
sig = 50
for K in [1, 8, 64]:
    acc = np.zeros_like(cam)
    for _ in range(K): acc += cam + rng.normal(0, sig, cam.shape)
    save(f'avg_{K}', acc / K)
META['avg_sigma'] = sig

# salt-and-pepper: box vs median
sp = cam.copy(); u = rng.random(cam.shape); sp[u < 0.06] = 0; sp[u > 0.94] = 255
save('sp', sp); save('sp_box3', correlate(sp, np.ones((3, 3)) / 9)); save('sp_med3', median(sp, 3))
save('sp_box5', correlate(sp, np.ones((5, 5)) / 25)); save('sp_med5', median(sp, 5))

# smoothing: box sizes and a Gaussian
for n in [3, 11, 21]: save(f'box_{n}', correlate(cam, np.ones((n, n)) / n ** 2))
save('gauss_35', correlate(cam, gauss_kernel(3.5)))
txt = load('page.png'); save('page', txt)
save('page_box9', correlate(txt, np.ones((9, 9)) / 81))
# shading correction: f * shading, then divide by the (known) shading
yy, xx = np.mgrid[0:256, 0:256] / 255
shade = 0.25 + 0.75 * (0.6 * xx + 0.4 * (1 - yy))
save('shaded', cam * shade); save('shade', shade * 255); save('unshaded', cam * shade / shade)
# subtraction: a small change appears only in the difference
cam2 = cam.copy(); cam2[60:78, 180:200] = np.clip(cam2[60:78, 180:200] + 90, 0, 255)
save('cam_changed', cam2); save('diff', np.abs(cam2 - cam) * 2.5)
# region of interest: multiply by a mask
mask = np.zeros_like(cam); mask[30:200, 40:170] = 1
save('roi_mask', mask * 255, lossless=True); save('roi', cam * mask)

# sharpening on the moon
moon = load('moon.png', (256, 256))
moon_b = correlate(moon, gauss_kernel(1.2))
save('moon_blur', moon_b)
L4 = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]]); L8 = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
lap4 = correlate(moon_b, L4); lap8 = correlate(moon_b, L8)
save('moon_lap4', scale_full(lap4)); save('moon_lap8', scale_full(lap8))
save('moon_sharp4', moon_b - 3 * lap4); save('moon_sharp8', moon_b - 3 * lap8)
# unsharp masking and highboost on text
tb = correlate(txt, gauss_kernel(2.0))
save('page_blur', tb); m = txt - tb
save('page_mask', np.clip(m * 3 + 128, 0, 255)); save('page_unsharp', txt + m); save('page_highboost', txt + 4.5 * m)
# gradient (Sobel) magnitude
SX = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]); SY = SX.T
gx = correlate(cam, SX); gy = correlate(cam, SY)
save('cam_gx', np.clip(np.abs(gx), 0, 255)); save('cam_gy', np.clip(np.abs(gy), 0, 255)); save('cam_grad', np.clip(np.abs(gx) + np.abs(gy), 0, 255))

# local vs global histogram equalization (a G&W Fig 3.32-like test image: dark squares hiding faint shapes)
T = np.full((200, 200), 128.0)
for (r, c) in [(25, 25), (25, 120), (120, 25), (120, 120)]:
    T[r:r + 55, c:c + 55] = 12
    T[r + 18:r + 37, c + 18:c + 37] = 20  # faint inner square
T += rng.normal(0, 2.5, T.shape)
T = np.clip(T, 0, 255); save('hidden', T)
h = np.bincount(np.round(T).astype(int).ravel(), minlength=256); cdf = np.cumsum(h) / h.sum()
save('hidden_global', 255 * cdf[np.round(T).astype(int)])
a = 3; Tp = pad(np.round(T), a, a, 'mirror'); loc = np.zeros_like(T)
for i in range(T.shape[0]):
    for j in range(T.shape[1]):
        win = Tp[i:i + 2 * a + 1, j:j + 2 * a + 1]; loc[i, j] = 255 * (win <= Tp[i + a, j + a]).mean()
save('hidden_local', loc)

# binary shapes for set and logical operations
y, x = np.mgrid[0:160, 0:160]
A = ((x - 62) ** 2 + (y - 80) ** 2 < 48 ** 2); B = (abs(x - 104) < 40) & (abs(y - 80) < 34)
for k, v in [('setA', A), ('setB', B), ('and', A & B), ('or', A | B), ('xor', A ^ B), ('notA', ~A), ('aminusb', A & ~B)]:
    save('bin_' + k, v * 255.0, lossless=True)

json.dump(META, open(os.path.join(OUT, 'meta.json'), 'w'))
print('assets:', len([k for k in META if isinstance(META[k], dict)]), 'images,', sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.endswith('.webp')) // 1024, 'KB')
