# In-scope past questions (Ch 1-3) — raw data transcribed from the papers

## Midsem 2019-20 (Chittora) EEE F435_Q.pdf
Q1 Fig1 (rows top->bottom): 3 1 2 1(q) / 2 2 0 2 / 1 2 1 1 / (p)1 0 1 2 ; p bottom-left, q top-right.
 (a) V={0,1}: shortest 4-,8-,m-path p->q; (b) V={1,2}.
Q2 hist eq 3-bit 6x6 Fig2: 0 0 1 4 5 4 / 0 1 2 5 4 3 / 1 2 3 4 3 1 / 4 5 4 3 1 0 / 5 4 3 1 0 0 / 4 4 3 1 0 0 ; LUT + final image.
Q4 kernel K for g = f + c*Lap(f).
Q5 two binary images (half black/white vs checkerboard 4x4) same histogram; blur with 3x3 avg -> histograms differ.
Q6 piecewise linear: (0,0)-(30,20)-(180,210)-(255,255).
## Midsem 2018-19 DIP Midsem paper.pdf
Q2 border methods; average filter on 5x5 3-bit: 3 7 6 2 0 / 2 4 6 1 1 / 4 7 2 5 4 / 3 0 6 2 1 / 5 7 5 1 2
Q6 8 pixels {255,118,129,182,18,178,82,53} 4-bit uniform quantization: rms error, rms SNR.
## Midsem 2023-24 sem II (15/03/2024)
Q1 70x80, 4-bit, H(r)=k1 r 0..7 triangle peak at 7/8 down to 15 -> k1, mean, std.
Q2 image 1 2 4 5 / 5 2 5 2 / 1 1 3 6 / 2 4 6 7 ; (a) 1/16[1 2 1;2 4 2;1 2 1] replicate border; (b) [0 1 0;1 -4 1;0 1 0] zero pad.
## Midsem 2022-23 sem II (18/03/2023)
Q1 50x70 3-bit ramp H(r)=kr -> k, mean, std.
Q2 same image; (a) weighted mean zero pad; (b) Laplacian replicate.
Q3 (208,110,129,184,28,178,82,55) 4-bit quantization rms error & SNR.
Q6 64x64 binary images, 16x16 blocks, blur 3x3 -> histograms.
## Quiz-1 2018-19: S1|S2 subsets (5 rows x 10 cols incl. border col):
 0|0 0 0 0|0 0 1 [1] 0 / 1|0 0 1 0|0 1 0 0 1 / 1|0 0 1 0|1 1 0 0 0 / 0|0 [1] 1 1|0 0 1 1 1 / 0|0 1 1 1|0 0 1 1 1  (check figure) V={1}: # 4-/8-connected comps in S1,S2; adjacency; D4,D8 between boxed.
## Quiz-1 2021-22 (17/9/2021) 3-bit 5x5: 4 2 3 2(q) 5 / 1 1 2 3 4 / 1 3 2 3 4 / 2(p) 2 3 1 3 / 2 2 1 1 4
 Q1 Euclid & city-block p<->q ; Q2 LSB plane ; Q3 negative ; Q4 shortest m-path V={1,2} ; Q5 histogram ; Q6 hist eq.
## Quiz-2 2021-22: image 4 2 3 2 / 1 1 2 3 / 1 3 2 3 / 2 2 3 1 ; (i) 1/16[121;242;121] (ii) [0 -1 0;-1 4 -1;0 -1 0] on diagonal, zero pad, nearest int.
 KEY ERROR candidate: (ii) at (0,0) key says 16; 4*4-2-1 = 13.
 Q2 16x16 binary images blur -> key hist 114/14/14/114 vs 62/48/18/18/48/62.
 Q4 MATLAB 5x3 averaging loop.
## Midsem 2024-25 (Oct 4 2024): Q1 f=0 2 0/3 5 2/0 4 0, h=1/14[1 2 1;1 2 2;2 1 3] corr & conv zero pad 3-bit round.
 Q2(i) p_f=2-2r -> p_g=3z^2 continuous matching. Q3(i) LSB/MSB planes with Gray coding of 5x5 image.
## Midsem 2023-24 (Oct 10 2023) Q2: Filter-1 [0 1 0;1 -4 1;0 1 0], Filter-2 [.01 .1 .01;.1 .56 .1;.01 .1 .01] on non-zero 3x3 region of 5x5 image (0 0 0 0 0/0 15 7 0 0/0 7 15 7 0/0 0 7 15 0/0 0 0 0 0). Key: F1 -46 2 14/2 -32 2/14 2 -46 ; F2 9.95 6.99 1.55/...
## DIP-26 Quiz-1 (this year): Q1 Gaussian corr replicate g(0,3)=2.6345 ; Q2 bitplanes sum=576 ; Q4 hist eq ps(6)=0.1875 ; Q6 bilinear Mg(2,2)=30.
