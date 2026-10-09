"""Chapter 4 picture assets: spectra, phase/magnitude swaps, frequency-domain filters, aliasing. Run after assets.py."""
import numpy as np
import json, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, '..', 'assets', 'src'); OUT = os.path.join(HERE, '..', 'assets'); META = {}
def load(name, size=None):
    im = Image.open(os.path.join(SRC, name)).convert('L')
    if size: im = im.resize(size, Image.LANCZOS)
    return np.asarray(im, dtype=float)
def save(key, a, q=88):
    a8 = np.clip(np.round(a), 0, 255).astype(np.uint8)
    Image.fromarray(a8).save(os.path.join(OUT, key + '.webp'), 'WEBP', quality=q, method=6); META[key] = dict(w=a8.shape[1], h=a8.shape[0])

cam = load('camera.png', (256, 256))
F = np.fft.fft2(cam)
def logspec(F):
    S = np.log1p(np.abs(np.fft.fftshift(F))); return 255 * S / S.max()
def lin(a):
    a = a - a.min(); return 255 * a / (a.max() or 1)
save('f_spec_uncentred', 255 * np.log1p(np.abs(F)) / np.log1p(np.abs(F)).max())
save('f_spec', logspec(F))
# phase only / magnitude only
save('f_phase_only', lin(np.real(np.fft.ifft2(np.exp(1j * np.angle(F))))))
save('f_mag_only', lin(np.log1p(np.abs(np.fft.fftshift(np.real(np.fft.ifft2(np.abs(F))))))))
# conjugate → 180° rotation
save('f_conj', np.real(np.fft.ifft2(np.conj(F))))
# translation: spectrum magnitude unchanged
sh = np.roll(cam, (60, 80), (0, 1)); save('f_shift_img', sh); save('f_shift_spec', logspec(np.fft.fft2(sh)))
# rotation
from PIL import Image
r = np.asarray(Image.fromarray(cam.astype(np.uint8)).rotate(30, resample=Image.BILINEAR), float)
sq = np.zeros((256, 256)); sq[96:160, 112:144] = 255
save('f_rect', sq); save('f_rect_spec', logspec(np.fft.fft2(sq)))
sqr = np.asarray(Image.fromarray(sq.astype(np.uint8)).rotate(30, resample=Image.BILINEAR), float)
save('f_rect_rot', sqr); save('f_rect_rot_spec', logspec(np.fft.fft2(sqr)))
# stripes
for w in (2, 4, 8):
    st = np.tile(((np.arange(256) // w) % 2) * 255.0, (256, 1))
    save(f'f_stripe{w}', st)
    sp = logspec(np.fft.fft2(st)); sp = (sp > 0.5 * sp.max()) * 255.0
    big = sp.copy()
    for dx in range(-4, 5):
        for dy in range(-4, 5): big = np.maximum(big, np.roll(sp, (dx, dy), (0, 1)))
    save(f'f_stripe{w}_spec', big)
# frequency-domain filters on the camera (padded)
P = 512; fp = np.zeros((P, P)); fp[:256, :256] = cam
Fp = np.fft.fftshift(np.fft.fft2(fp)); u = np.arange(P) - P / 2; D = np.hypot(*np.meshgrid(u, u, indexing='ij'))
def apply(H):
    return np.real(np.fft.ifft2(np.fft.ifftshift(Fp * H)))[:256, :256]
D0 = 30
ilp = (D <= D0).astype(float); glp = np.exp(-D ** 2 / (2 * D0 ** 2))
save('f_ilpf', apply(ilp)); save('f_glpf', apply(glp))
save('f_ghpf', lin(apply(1 - glp))); save('f_ihpf', lin(apply(1 - ilp)))
save('f_H_ilpf', 255 * ilp[128:384, 128:384]); save('f_H_glpf', 255 * glp[128:384, 128:384]); save('f_H_ghpf', 255 * (1 - glp[128:384, 128:384]))
# wraparound: circular filtering without padding vs with padding (big box blur)
k = 61; h = np.zeros((256, 256)); h[:k, :k] = 1 / k ** 2; h = np.roll(h, (-(k // 2), -(k // 2)), (0, 1))
save('f_wrap', np.real(np.fft.ifft2(np.fft.fft2(cam) * np.fft.fft2(h))))
hp = np.zeros((P, P)); hp[:k, :k] = 1 / k ** 2; hp = np.roll(hp, (-(k // 2), -(k // 2)), (0, 1))
save('f_nowrap', np.real(np.fft.ifft2(np.fft.fft2(fp) * np.fft.fft2(hp)))[:256, :256])
# aliasing: shrink by 4 without and with blur (then enlarge for display)
x = np.arange(256); X, Y = np.meshgrid(x, x, indexing='ij'); zone = 127.5 + 127.5 * np.cos(np.pi * (X ** 2 + Y ** 2) / 512)
save('f_zone', zone)
small = zone[::4, ::4]; save('f_zone_alias', np.kron(small, np.ones((4, 4))))
g = np.exp(-(np.fft.fftfreq(256)[:, None] ** 2 + np.fft.fftfreq(256)[None, :] ** 2) * 2 * np.pi ** 2 * 4)
smallb = np.real(np.fft.ifft2(np.fft.fft2(zone) * g))[::4, ::4]; save('f_zone_blur', np.kron(smallb, np.ones((4, 4))))
m = json.load(open(os.path.join(OUT, 'meta.json'))); m.update(META); json.dump(m, open(os.path.join(OUT, 'meta.json'), 'w'), indent=1)
print(sorted(META))
