"""Chapter 4 (up to 4.7 + the FFT on the slides): the slide homework 4.7, 4.10, 4.21, 4.36, 4.44, 4.48 and close textbook
problems. Numbers: tools/verify_new.py."""
from lib import *

SECTIONS = {}

SECTIONS['ch4-ft'] = [
h3('More questions on sampling and aliasing (homework + textbook)'),
card('tb4-7', 'Textbook 4.7 (homework)', 'Highest frequency and Nyquist rate of a sum of sinusoids',
 r'\(f(t)=A\sin(\pi t)+B\sin(4\pi t)+C\cos(8\pi t)\). (a) Highest frequency of f? (b) Nyquist rate? (c) At what rate would you sample for perfect recovery?',
 '(a) Frequencies: sin(πt) → 0.5 Hz, sin(4πt) → 2 Hz, cos(8πt) → 4 Hz → highest <b>4 Hz</b>. (b) Nyquist rate = 2 × 4 = <b>8 samples/s</b>. (c) <b>More than</b> 8 samples per second (strictly greater; e.g. 10).',
 kind='tb', secs=180,
 concept='In sin(2πμt) the frequency is μ: divide the number in front of t by 2π. Sampling must be faster than twice the highest frequency present.',
 steps=['πt = 2π(0.5)t → 0.5 Hz; 4πt = 2π(2)t → 2 Hz; 8πt = 2π(4)t → 4 Hz.', 'Period of the sum = LCM of 2 s, 0.5 s, 0.25 s = 2 s (the hint), but the highest frequency is what matters: 4 Hz.', 'Nyquist: 2 × 4 = 8; sample strictly faster.'],
 mis=['Reading 8π as 8 Hz (forgetting the 2π).', 'Sampling exactly at 8/s: the cos(8πt) samples could all land on the same phase.']),
card('tb4-10', 'Textbook 4.10 (homework)', 'Sampling sin(2πnt) above, below and exactly at Nyquist',
 r'\(f(t)=\sin(2\pi nt)\), n an integer. (a) Period? (b) Frequency? (c) Sampled faster than Nyquist? (d) Slower? (e) Exactly at the Nyquist rate with samples at t = 0, ±T, ±2T, …?',
 '(a) 1/n. (b) n. (c) The copies of its (purely imaginary) spectrum are separated → the function can be recovered; the samples trace a sine. (d) The copies overlap → <b>aliasing</b>: the samples look like a sine of a lower, wrong frequency. (e) Rate 2n, T = 1/(2n): every sample is sin(2πn·k/2n) = sin(πk) = <b>0</b> — all samples are zero and the sine is lost completely.',
 kind='tb', secs=240,
 concept='This is why Nyquist says strictly <b>more than</b> twice the highest frequency: exactly twice can land every sample on a zero crossing.'),
card('tb4-30', 'Textbook 4.30', 'Period and frequency of digital sequences',
 'Give the period and frequency (cycles per sample) of (a) 0 1 0 1 …, (b) 0 0 1 0 0 1 …, (c) 0 0 1 1 0 0 1 1 ….',
 '(a) period 2, frequency 1/2 (the highest a digital sequence can have). (b) period 3, frequency 1/3. (c) period 4, frequency 1/4.',
 kind='tb', secs=60,
 concept='Period = number of samples before the pattern repeats; frequency = 1/period cycles per sample.'),
]

SECTIONS['ch4-fft'] = [
h3('Practice on FLOP counts (your slide’s convention)'),
card('dr-flop', 'Practice (slide convention)', 'FLOPs for a 64-point DFT: direct, one level, full radix-2',
 'n = 64. Using your slides’ counts (direct: (n−1)² multiplications and n(n−1) additions; one decimation level adds n/2 multiplications and n additions to two n/2-point DFTs), find the counts for (a) the direct DFT, (b) one level of decimation, (c) full radix-2 FFT.',
 '(a) 63² = <b>3969</b> mult, 64·63 = <b>4032</b> add. (b) 2·31² + 32 = <b>1954</b> mult, 2·32·31 + 64 = <b>2048</b> add. (c) (n/2)log₂n = 32·6 = <b>192</b> mult, n log₂n = 64·6 = <b>384</b> add.',
 kind='dr', secs=180,
 concept='Each decimation level splits one n-point DFT into two n/2-point DFTs plus one round of “butterflies” (n/2 multiplications by W<sup>k</sup>, n additions). Doing it all the way down (log₂n levels) gives (n/2)log₂n and n log₂n.',
 steps=['Direct: (64 − 1)² = 3969; 64 × 63 = 4032.', 'One level: two 32-point direct DFTs cost 2 × 31² = 1922 mult and 2 × 32 × 31 = 1984 add; plus 32 mult and 64 add.', 'Full: log₂64 = 6 levels → 6 × 32 = 192 mult, 6 × 64 = 384 add.'],
 fast=['Check against the slide: n = 32 gives 961/992 direct and 466/512 with one level.']),
]

SECTIONS['ch4-2d'] = [
h3('More questions on the 2-D DFT (homework + textbook)'),
card('tb4-21', 'Textbook 4.21 (homework)', 'Spectrum of vertical stripes',
 'An image has alternating black/white vertical stripes, each 2 pixels wide; its spectrum shows the dc term and two spikes on the horizontal axis. (a) What if the stripes are 4 pixels wide? (b) Why are the spikes only on the horizontal axis? (c) What about 1-pixel stripes? (d) Are the dc terms the same?',
 '(a) The period doubles (4 → 8 pixels), so the spikes move <b>closer to the centre</b> (half the distance from the dc term). (b) The image changes only along the horizontal direction (each column is constant), so all its frequency content is on the horizontal frequency axis; vertical frequency is 0. (c) Period 2 pixels = the highest possible frequency: the spikes move to the <b>edges</b> of the spectrum (u = ±M/2; for a real image they coincide). (d) <b>Same</b>: the dc term is the sum (average) of the image, and every stripe pattern is half black, half white.',
 kind='tb', secs=240,
 concept='Spike position = (number of periods across the image). Wider stripes → fewer periods → spikes nearer the centre.',
 steps=['Check in 1-D with 16 pixels: 2-pixel stripes (period 4) → non-zero DFT at u = 0, 4, 12 (= ±4).', '1-pixel stripes (period 2) → non-zero at u = 0 and 8 (= M/2), the very edge.'],
 calc='Complex app check, M = 4, one period of 1 1 0 0: F(1) = 1 + 1∠−90 = 1 − i (non-zero), F(2) = 1 + 1∠−180 = 0.'),
card('tb4-36', 'Textbook 4.36 (homework)', 'Zero padding and the dc term',
 'An M×N image is zero-padded to P×Q (e.g. P = 2M, Q = 2N). (a) Ratio of the average values of the original and padded images? (b) Is F<sub>p</sub>(0,0) = F(0,0)?',
 '(a) Same sum S of pixel values, more pixels: average<sub>orig</sub>/average<sub>pad</sub> = (S/MN)/(S/PQ) = <b>PQ/(MN)</b> (= 4 for P = 2M, Q = 2N). (b) With your slides’ DFT (no 1/MN in front), F(0,0) = Σ f = S for both → <b>yes, equal</b>. If the transform has 1/(MN) in front (textbook Table 4.3 style), F is the average and then F(0,0)/F<sub>p</sub>(0,0) = PQ/(MN).',
 kind='tb', secs=180,
 concept='F(0,0) = sum of all pixels (no scaling) = MN × average. Zeros add nothing to the sum.'),
card('tb4-44', 'Textbook 4.44 (homework)', 'Negating the phase flips the image',
 'The image was obtained by multiplying the phase angle of the DFT by −1 and taking the inverse DFT. Why is it reflected about both axes?',
 r'Negating the phase gives \(|F|e^{-j\phi}=F^*(u,v)\). For a real image, \(F^*(u,v)=F(-u,-v)\), and the inverse DFT of F(−u, −v) is f(−x, −y): the image rotated by 180° = reflected about both axes (indices taken mod M, N). Verified numerically on a random 4×4 image.',
 kind='tb', secs=180,
 concept='Time/space reversal ↔ frequency reversal; for real images conjugating = reversing frequencies.',
 mis=['Saying the image becomes negative: that is what multiplying the <b>magnitude</b> by −1 does (4.45).']),
card('tb4-29', 'Textbook 4.29', 'Where is the 1/MN in a “canned” DFT program?',
 'A program computes a DFT pair, but you do not know whether 1/MN is in the forward transform, the inverse, or split as 1/√MN in both. How do you find out?',
 'Feed it a constant image f = 1 (M×N). Read F(0,0): <b>MN</b> → no factor in the forward transform (it is in the inverse); <b>1</b> → 1/MN is in the forward; <b>√MN</b> → split. (Equivalently, transform an impulse.)',
 kind='tb', secs=120),
card('tb4-43', 'Textbook 4.43–4.45 (style of Oct 2024 Q3)', 'Conjugate, negate the magnitude, add π',
 r'For a real image f with DFT \(F=|F|e^{j\phi}\): what is the inverse DFT of (a) \(F^*\), (b) \(-F\) (magnitude × −1, i.e. phase + π), (c) \(e^{j\pi/2}F\)?',
 r'(a) \(f(-x,-y)\) (180° rotation). (b) \(-f(x,y)\) (a negative-valued image; displayed after scaling it looks like the negative). (c) \(j\,f(x,y)\) (purely imaginary; its magnitude is f).',
 kind='tb', secs=150,
 concept='The DFT is linear: multiplying F by a constant multiplies f by the same constant. Only conjugation does something geometric.'),
]

SECTIONS['ch4-filt'] = [
h3('More questions on frequency-domain filters (homework + textbook)'),
card('tb4-48', 'Textbook 4.48 (homework)', 'Gaussian lowpass: from H(μ,ν) to the spatial kernel',
 r'\(H(\mu,\nu)=Ae^{-(\mu^2+\nu^2)/2\sigma^2}\). Show that the spatial kernel is \(h(t,z)=A\,2\pi\sigma^2e^{-2\pi^2\sigma^2(t^2+z^2)}\).',
 r'H separates: \(Ae^{-\mu^2/2\sigma^2}\cdot e^{-\nu^2/2\sigma^2}\). In 1-D, the inverse FT of \(e^{-\mu^2/2\sigma^2}\) is \(\sqrt{2\pi}\sigma e^{-2\pi^2\sigma^2t^2}\) (a Gaussian of the reciprocal width). Multiply the two 1-D results: \(h=A(\sqrt{2\pi}\sigma)^2e^{-2\pi^2\sigma^2(t^2+z^2)}=A\,2\pi\sigma^2e^{-2\pi^2\sigma^2(t^2+z^2)}\).',
 kind='tb', secs=300,
 concept='A Gaussian transforms into a Gaussian; narrow in one domain = wide in the other (σ in H ↔ 1/(2πσ) in h).',
 steps=[r'Use \(\int e^{-a\mu^2}e^{j2\pi\mu t}d\mu=\sqrt{\pi/a}\,e^{-\pi^2t^2/a}\) with \(a=1/2\sigma^2\): \(\sqrt{2\pi}\sigma\,e^{-2\pi^2\sigma^2t^2}\).', 'The 2-D inverse FT of a product of a μ-only and a ν-only function is the product of the 1-D inverses.'],
 fast=['Narrower H (small σ, stronger blur) ↔ wider h — check that your answer has σ² multiplying t² in the exponent.']),
card('tb4-50', 'Textbook 4.50–4.51', 'H(u,v) of a difference and of the Laplacian kernel',
 r'Find H for (a) \(g_x=f(x+1,y)-f(x,y)\), (b) the 4-neighbour Laplacian \(f(x+1,y)+f(x-1,y)+f(x,y+1)+f(x,y-1)-4f(x,y)\). Lowpass or highpass?',
 r'Use the shift property \(f(x+x_0)\leftrightarrow e^{j2\pi ux_0/M}F\). (a) \(H_x=e^{j2\pi u/M}-1\); \(|H_x|=2|\sin(\pi u/M)|\): 0 at u = 0 → <b>highpass</b>. (b) \(H=2\cos\frac{2\pi u}{M}+2\cos\frac{2\pi v}{N}-4\): H(0,0) = 0 and |H| grows to 8 at u = M/2, v = N/2 → <b>highpass</b>.',
 kind='tb', secs=240,
 concept='Same method as the N₄-average question: each shifted copy of f becomes an exponential factor; ± pairs combine into cosines.',
 mis=['Sign of the exponent: f(x + 1) ↔ e<sup>+j2πu/M</sup> with your slides’ DFT (minus sign in the forward kernel).']),
]

SECTIONS['ch4-conv'] = [
h3('One more practice on circular vs linear convolution'),
card('dr-circ4', 'Practice (slide methods)', 'Circular from linear by wrapping, and how much padding avoids wrap-around',
 'f = {1, 2, 0, 1}, h = {2, 1, 0, 0}. (a) Linear convolution f ∗ h. (b) 4-point circular convolution f ⊛ h by wrapping (a). (c) Minimum length to zero-pad both so that circular = linear?',
 '(a) f ∗ h = {2, 5, 2, 2, 1, 0, 0} (non-zero part {2, 5, 2, 2, 1}). (b) Fold everything beyond index 3 back onto the start: {2+1, 5+0, 2+0, 2} = <b>{3, 5, 2, 2}</b>. (c) n₁ + n₂ − 1 = <b>7</b> (or 5 using only the non-zero lengths 4 and 2).',
 kind='dr', secs=240,
 concept='Circular convolution = linear convolution with the tail wrapped around onto the start (period n). Padding to at least n₁ + n₂ − 1 leaves room for the whole linear result, so nothing wraps.',
 steps=['Linear: slide h = (2, 1) over f: 2·1, 2·2 + 1·1, 2·0 + 1·2, 2·1 + 1·0, 1·1 → 2, 5, 2, 2, 1.', 'Wrap index 4 onto index 0: 2 + 1 = 3 → {3, 5, 2, 2}.', 'Check by the cyclic definition: g(0) = f(0)h(0) + f(3)h(1) = 2 + 1 = 3 ✓.'],
 calc='Recipe F in the calculator section: circulant matrix of f (4×4) × h (4×1).'),
]
