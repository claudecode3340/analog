"""Builds the improved DIP mid-sem guide from the original (orig.html).
   python3 build.py  ->  DIP_Mid-sem_Master_Guide.html
   Every number in the added cards is computed in tools/verify_new.py."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *  # noqa
import cards_ch2, cards_ch3, cards_ch4, calc_extra, prose, labs_help, style_extra, ch2_px, ch2_math, ch2_sq, ch2_eye, ch3_int, ch3_hist, ch3_filt, ch3_smooth, ch3_sharp, ch4_a, ch4_b

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, 'orig.html'), encoding='utf-8').read()


def sub(old, new, count=None):
    """replace exactly; fail loudly if the original text is not there"""
    global s
    n = s.count(old)
    if n == 0 or (count is not None and n != count):
        raise SystemExit(f'patch failed ({n} hits): {old[:90]!r}')
    s = s.replace(old, new)


# ── 1. errors in the original ───────────────────────────────────────────────
# End-sem 2022-23 Q2: second row of A is (−2, 1, −3) (check: −2·1 + 1·1 − 3 = −4 = y of f(1,1))
sub(r'\begin{bmatrix}1&-3&5\\2&1&-3\\0&0&1\end{bmatrix}', r'\begin{bmatrix}1&-3&5\\-2&1&-3\\0&0&1\end{bmatrix}', 2)
sub('<div class="">5</div><div class="">2</div><div class="">1</div><div class="">−3</div>', '<div class="">5</div><div class="">−2</div><div class="">1</div><div class="">−3</div>', 2)
sub('<span class="mcol" id="cvs"></span>', '<span class="mcol cvs"></span>', 1)
sub("$('#cvs',out)", "$('.cvs',out)", 1)
# calculator keys that do not exist on the fx-991CW (checked in the Casio manual)
sub('<span class="k">OPTN</span><span class="arrow">→</span><span class="k m">1-Var Results</span>',
    '<span class="k">OK</span><span class="arrow">→</span><span class="k m">1-Var Results</span><span class="arrow">→</span><span class="k">OK</span>')
sub('<span class="k">STO</span><span class="k">A</span>', K('VARIABLE', '>A=', '>Store', bare=True))
sub('<span class="k">MatA</span><span class="k">x⁻¹</span>', '<span class="k">MatA</span><span class="k">SHIFT</span><span class="k">x<sup>■</sup></span><span class="k m">(x⁻¹)</span>')
sub('<td class="l">mode key → Bin</td>', '<td class="l">press <span class="keys"><span class="k">FORMAT</span></span> until the mode reads Binary (each press cycles Decimal → Hexadecimal → Binary → Octal)</td>')
sub('<span class="k m">Matrix Calc</span></span> → Transposition (Trn) / x⁻¹ / Determinant.',
    '<span class="k m">Matrix Calc</span></span> → Transposition (Trn) / Inverse Matrix / Determinant. Faster inverse: right after a matrix, press <span class="keys"><span class="k">SHIFT</span><span class="k">x<sup>■</sup></span></span> (x⁻¹).')
for old, new in prose.PATCHES:
    sub(old, new)

# ── 2. new content inserted at the end of each topic section ────────────────
def insert_end(sec_id, html_block):
    global s
    i = s.find(f'<section class="topic" id="{sec_id}"')
    if i < 0: raise SystemExit('no section ' + sec_id)
    j = s.find('<section class="topic"', i + 10)
    k = s.rfind('</section>', i, j) if j > 0 else -1
    at = k if k > 0 else j
    s = s[:at] + html_block + '\n' + s[at:]


def insert_after(marker, html_block):
    global s
    i = s.find(marker)
    if i < 0: raise SystemExit('marker missing: ' + marker[:80])
    i += len(marker)
    s = s[:i] + html_block + s[i:]


for mod in (cards_ch2, cards_ch3, cards_ch4):
    for sec, blocks in mod.SECTIONS.items():
        insert_end(sec, '\n'.join(blocks))
for marker, block in prose.INSERTS:
    insert_after(marker, block)
for marker, block in calc_extra.INSERTS:
    insert_after(marker, block)
for old, new in calc_extra.PATCHES:
    sub(old, new)

# ── 3. rebuilt sections (teaching rewritten, cards kept with new solutions) ──
def card_by_id(cid):
    i = s.find(f'<div class="prob" id="{cid}"')
    if i < 0: raise SystemExit('card missing: ' + cid)
    a, b = extract_div(s, i)
    return s[a:b]


def replace_section(sec_id, builder):
    global s
    i = s.find(f'<section class="topic" id="{sec_id}"')
    j = s.find('<section class="topic"', i + 10)
    new = builder(card_by_id) if builder.__code__.co_argcount == 1 else builder(card_by_id, s[i:j])
    s = s[:i] + new + '\n' + s[j:]


replace_section("ch2-px", ch2_px.section)
replace_section("ch2-math", ch2_math.section)
replace_section("ch2-sq", ch2_sq.section)
replace_section("ch2-eye", ch2_eye.section)
replace_section("ch3-int", ch3_int.section)
replace_section("ch3-hist", ch3_hist.section)
replace_section("ch3-filt", ch3_filt.section)
replace_section("ch3-smooth", ch3_smooth.section)
replace_section("ch3-sharp", ch3_sharp.section)
replace_section("ch4-conv", ch4_a.conv)
replace_section("ch4-ft", ch4_a.ft)
replace_section("ch4-dft", ch4_a.dft)
replace_section("ch4-fft", ch4_b.fft)
replace_section("ch4-2d", ch4_b.twod)
replace_section("ch4-filt", ch4_b.filt)
# ── 4. global: lab help boxes, the clearer path lab, extra CSS ──
s = labs_help.add_help(s)
s = labs_help.patch_path_lab(s)
s = s.replace('</style></head>', style_extra.CSS + '</style></head>', 1)

out = os.path.join(HERE, 'DIP_Mid-sem_Master_Guide.html')
open(out, 'w', encoding='utf-8').write(s)
print('wrote', out, f'{len(s) / 1e6:.2f} MB', s.count('<div class="prob" id='), 'question cards')
