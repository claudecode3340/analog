"""Chapter 2.5 rebuilt: neighbours, adjacency (4, 8, m), paths, components, regions, distances — each idea with a picture
and a worked example; the past-paper solutions as step-by-step walks with a grid at every step."""
from lib import *

I18 = [[3, 1, 2, 1], [2, 2, 0, 2], [1, 2, 1, 1], [1, 0, 1, 2]]
def shade(img, V, extra=None):
    c = {(i, j): ('in' if v in V else 'out') for i, r in enumerate(img) for j, v in enumerate(r)}
    c.update(extra or {})
    return c

def section(card):
    H = []
    H.append('''<section class="topic" id="ch2-px">
  <div class="eyebrow">Chapter 2.5 · Lecture 5</div>
  <h2>Neighbours, adjacency, paths and distances</h2>
  <div class="meta"><span class="chip ">TB 2.5</span><span class="chip ">slides pp. 29–30, 51–52</span><span class="chip hot">past-paper favourite</span></div>
  <p class="lede">This topic answers three simple questions about pixels: <b>which pixels are “next to” each other</b>, <b>when you can walk from one pixel to another</b> using only certain grey values, and <b>how far apart two pixels are</b>. The exam asks: the shortest 4-, 8- and m-path between two pixels, how many connected pieces a set of pixels has, and D<sub>4</sub>, D<sub>8</sub>, D<sub>e</sub> between two pixels. Everything is done by hand on a small grid — no calculator, no formulas beyond counting.</p>''')
    H.append(note('<b>Coordinates used everywhere below:</b> a pixel is written (row, column), both counted from 0, row 0 at the top. So (3, 0) is the bottom-left pixel of a 4×4 image. This is the same as f(x, y) in your slides: x = row, y = column.'))

    # 1 neighbours
    nb = lambda S: {(1 + a, 1 + b): c for c, L in S for (a, b) in L}
    lbl = [['(x−1, y−1)', '(x−1, y)', '(x−1, y+1)'], ['(x, y−1)', 'p', '(x, y+1)'], ['(x+1, y−1)', '(x+1, y)', '(x+1, y+1)']]
    blank = [[''] * 3 for _ in range(3)]
    n4 = {(0, 1): 'n4', (1, 0): 'n4', (1, 2): 'n4', (2, 1): 'n4', (1, 1): 'ctr'}
    ndc = {(0, 0): 'nd', (0, 2): 'nd', (2, 0): 'nd', (2, 2): 'nd', (1, 1): 'ctr'}
    n8 = {**{k: 'n8' for k in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]}, (1, 1): 'ctr'}
    pv = [['', '', ''], ['', 'p', ''], ['', '', '']]
    H.append(lesson('Neighbours of a pixel: N<sub>4</sub>, N<sub>D</sub>, N<sub>8</sub>',
        'The neighbours of a pixel p are the pixels right around it. There are two kinds: the 4 that share a <b>side</b> with p, and the 4 that only touch p at a <b>corner</b>.',
        '<div class="cols"><div>'
        '<p><b>N<sub>4</sub>(p)</b> — the 4-neighbours: up, down, left, right.<br><b>N<sub>D</sub>(p)</b> — the diagonal neighbours: the 4 corners.<br><b>N<sub>8</sub>(p)</b> — the 8-neighbours: both together (the whole 3×3 block around p, without p).</p>'
        '<p><b>Example.</b> p = (2, 3).<br>N<sub>4</sub> = (1, 3), (3, 3), (2, 2), (2, 4)<br>N<sub>D</sub> = (1, 2), (1, 4), (3, 2), (3, 4)<br>N<sub>8</sub> = all eight of those.</p>'
        '<div class="trap"><b>Border pixels</b> have fewer neighbours: a corner pixel has only 2 four-neighbours and 3 eight-neighbours (the others would be outside the image).</div>'
        '</div><div>' + figs(gsvg(pv, n4, idx=False, label='N₄(p): shares a side'), gsvg(pv, ndc, idx=False, label='N_D(p): touches a corner'), gsvg(pv, n8, idx=False, label='N₈(p) = N₄ + N_D')) +
        gsvg(lbl, {(1, 1): 'ctr'}, cell=124, idx=False, label='the coordinates of all eight neighbours of p = (x, y)') + '</div></div>',
        use='adjacency and paths (below); N<sub>8</sub> + p is exactly the 3×3 window of every spatial filter in Chapter 3; N<sub>4</sub> is what the 4-neighbour Laplacian adds up.', tag='1'))

    # 2 adjacency 4/8
    A = [[1, 0, 1], [1, 1, 0], [0, 2, 1]]
    H.append(lesson('Adjacency: neighbours whose values are both “allowed”',
        'First you are told a set V of grey values that count (for example V = {1}: “the white pixels”, or V = {1, 2}: “pixels with value 1 or 2”). Two pixels are <b>adjacent</b> when both values are in V <b>and</b> they are neighbours.',
        '<div class="cols"><div>'
        '<p><b>4-adjacent</b>: both in V and side by side (q in N<sub>4</sub>(p)).<br><b>8-adjacent</b>: both in V and side by side <i>or</i> corner to corner (q in N<sub>8</sub>(p)).</p>'
        '<p><b>Example</b> (picture, V = {1}; blue = value in V):</p><ul>'
        '<li>(0, 0) and (1, 0): both 1, side by side → <b>4-adjacent</b> (and 8-adjacent).</li>'
        '<li>(1, 1) and (2, 2): both 1, only touch at a corner → <b>8-adjacent but not 4-adjacent</b>.</li>'
        '<li>(1, 1) and (2, 1): neighbours, but (2, 1) = 2 is not in V → <b>not adjacent</b>.</li>'
        '<li>(0, 0) and (0, 2): both 1, but not neighbours → <b>not adjacent</b>.</li></ul>'
        '</div><div>' + figs(gsvg(A, shade(A, {1}), links=[((0, 0), (1, 0)), ((1, 0), (1, 1))], label='4-adjacent pairs (side by side)'), gsvg(A, shade(A, {1}), links=[((0, 0), (1, 0)), ((1, 0), (1, 1)), ((1, 1), (2, 2)), ((0, 0), (1, 1)), ((0, 2), (1, 1))], label='8-adjacent pairs: corners count too')) + '</div></div>',
        use='every path and component question starts by shading the pixels whose value is in V.', tag='2'))

    # 3 m-adjacency
    G = [[0, 1, 1], [0, 1, 0], [0, 0, 1]]
    H.append(lesson('m-adjacency (mixed): 8-adjacency without the shortcuts that cause double paths',
        'With 8-adjacency a pixel can often be reached two ways at once — directly along a diagonal, and also round the corner through a shared neighbour. m-adjacency keeps only one of them: <b>a diagonal step is allowed only if neither of the two “corner” pixels is in V.</b>',
        '<div class="cols"><div>'
        '<p><b>The corner pixels of a diagonal step</b> from a to b are the two pixels that are side-neighbours of <i>both</i> a and b — the other two corners of the little 2×2 square.</p>'
        '<p><b>Example</b> (V = {1}):</p><ul>'
        '<li>Diagonal (1, 1) → (0, 2): its corner pixels are (0, 1) = <b>1</b> and (1, 2) = 0. One of them is in V, so you can already go round through (0, 1) → the diagonal is <b>not</b> m-adjacent.</li>'
        '<li>Diagonal (1, 1) → (2, 2): corners (1, 2) = 0 and (2, 1) = 0, neither in V. The diagonal is the only way through → it <b>is</b> m-adjacent.</li></ul>'
        '<ol class="how"><li>Every 4-adjacent pair is also m-adjacent.</li><li>For a diagonal pair, look at the 2 corner pixels.</li><li>If at least one corner is in V → <b>no</b> (go round). If both corners are outside V → <b>yes</b>.</li></ol>'
        '</div><div>' + figs(gsvg(G, shade(G, {1}), links=[((0, 1), (0, 2)), ((0, 1), (1, 1)), ((1, 1), (0, 2)), ((1, 1), (2, 2))], label='8-adjacency: (1,1)–(0,2) are linked twice (directly, and via (0,1)) — a double path'),
                             gsvg(G, shade(G, {1}), links=[((0, 1), (0, 2)), ((0, 1), (1, 1)), ((1, 1), (2, 2))], cross=[((1, 1), (0, 2))], ring=[(0, 1)], label='m-adjacency: that diagonal is removed (its corner (0,1) is in V); the diagonal to (2,2) stays')) + '</div></div>',
        use='“shortest m-path” questions (Mid-sem 2019 Q1, Quiz-1 2021 Q4). Remember it as <b>“diagonal only if there is no corner to go round”</b>.', tag='3'))

    # 4 paths and length
    P8 = [(3, 0), (3, 1), (2, 2), (1, 2), (0, 3)]
    H.append(lesson('Paths and their length',
        'A path from p to q is a chain of pixels, each one adjacent to the next (using 4-, 8- or m-adjacency, whichever the question says). Its <b>length = the number of steps</b> (= number of pixels − 1).',
        '<div class="cols"><div>'
        '<p>The picture shows an 8-path from p = (3, 0) to q = (0, 3) through pixels in V = {0, 1}. The small numbers are the order of the steps: it has 5 pixels, so its <b>length is 4</b>.</p>'
        '<p><b>How to find the shortest path by hand</b> (works for 4, 8 and m):</p><ol class="how">'
        '<li><b>Shade</b> every pixel whose value is in V. Check p and q are shaded — if not, no path exists.</li>'
        '<li>Write <b>0</b> on p. Write <b>1</b> on every allowed pixel you can reach in one step, <b>2</b> on every new pixel one step from a “1”, and so on (like ripples).</li>'
        '<li>The number that lands on q is the length of the shortest path. Walk back from q through decreasing numbers to write the path.</li>'
        '<li>If the ripples stop before reaching q, there is <b>no path</b> — say which pixels block it.</li></ol>'
        '</div><div>' + gsvg(I18, shade(I18, {0, 1}), path=P8, label='an 8-path of length 4 (V = {0, 1})') + '</div></div>',
        use='every “shortest 4-/8-/m-path” question. 4-paths are never shorter than 8-paths; m-paths are in between.', tag='4'))

    # 5 components, regions, boundaries
    E = [[1, 1, 0, 0, 0, 0], [1, 0, 0, 1, 1, 0], [0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 1, 1]]
    c4 = {}
    for k, comp in enumerate([[(0, 0), (0, 1), (1, 0)], [(1, 3), (1, 4), (2, 4)], [(2, 2)], [(4, 0), (4, 1)], [(4, 4), (4, 5)]]):
        for z in comp: c4[z] = f'c{k + 1}'
    c8 = {}
    for k, comp in enumerate([[(0, 0), (0, 1), (1, 0)], [(1, 3), (1, 4), (2, 2), (2, 4)], [(4, 0), (4, 1)], [(4, 4), (4, 5)]]):
        for z in comp: c8[z] = f'c{k + 1}'
    out = lambda d: {**{(i, j): 'out' for i in range(5) for j in range(6)}, **d}
    R = [[0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0], [0, 1, 1, 1, 1, 0], [0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0]]
    bnd = {(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3)}
    rc = {(i, j): ('block' if (i, j) in bnd else 'in') if R[i][j] else 'out' for i in range(5) for j in range(6)}
    H.append(lesson('Connected components, regions and boundaries',
        'Pixels of V that you can walk between form one <b>connected component</b> (one “blob”). Counting components = counting separate blobs. The answer depends on the adjacency: diagonal touching joins blobs under 8-adjacency but not under 4-adjacency.',
        '<div class="cols"><div>'
        '<p><b>Example</b> (V = {1}). With 4-adjacency there are <b>5</b> components (each colour is one). With 8-adjacency the single pixel (2, 2) touches (1, 3) at a corner, so those two blobs merge → <b>4</b> components.</p>'
        '<p><b>Region</b> = a connected set of pixels. <b>Two regions are adjacent</b> if together they form one connected set (some pixel of one is adjacent to some pixel of the other — say which adjacency).</p>'
        '<p><b>Boundary</b> of a region = its pixels that have at least one neighbour <i>outside</i> the region (red in the last picture; the one inside pixel (2, 2) is not on the boundary).</p>'
        '</div><div>' + figs(gsvg(E, out(c4), label='4-adjacency: 5 components'), gsvg(E, out(c8), label='8-adjacency: 4 components'), gsvg(R, rc, label='a region (blue) and its boundary (red)')) + '</div></div>',
        use='Quiz-1 2018-19 (components in S1 and S2, are S1 and S2 adjacent?). Method: shade V, then colour each blob with the chosen adjacency.', tag='5'))

    # 6 distances
    n = 7; c0 = 3
    d4 = [[abs(i - c0) + abs(j - c0) for j in range(n)] for i in range(n)]
    d8 = [[max(abs(i - c0), abs(j - c0)) for j in range(n)] for i in range(n)]
    de = [[fmt(round(((i - c0) ** 2 + (j - c0) ** 2) ** .5, 1)) if (i, j) != (3, 3) else 0 for j in range(n)] for i in range(n)]
    ring = lambda D, k: {(i, j): 'hl' for i in range(n) for j in range(n) if D[i][j] == k}
    H.append(lesson('Three ways to measure the distance between two pixels',
        'Distances only use the <b>coordinates</b> of the two pixels — the grey values do not matter. Take the row difference Δx and the column difference Δy (ignore their signs).',
        '<div class="cols"><div>'
        '<div class="formula">\\(D_e=\\sqrt{\\Delta x^2+\\Delta y^2}\\)<span class="say">Euclidean: the straight-line (ruler) distance.</span></div>'
        '<div class="formula">\\(D_4=|\\Delta x|+|\\Delta y|\\)<span class="say">City-block: walk only along rows and columns, like a taxi on a street grid. Pixels at D<sub>4</sub> = 1 are exactly N<sub>4</sub>(p).</span></div>'
        '<div class="formula">\\(D_8=\\max(|\\Delta x|,|\\Delta y|)\\)<span class="say">Chessboard: moves like a chess king (diagonal steps allowed). Pixels at D<sub>8</sub> = 1 are exactly N<sub>8</sub>(p).</span></div>'
        '<p><b>Example.</b> p = (1, 1), q = (4, 5): Δx = 3, Δy = 4.<br>D<sub>e</sub> = √(9 + 16) = <b>5</b>, D<sub>4</sub> = 3 + 4 = <b>7</b>, D<sub>8</sub> = max(3, 4) = <b>4</b>.</p>'
        '<p>Always D<sub>8</sub> ≤ D<sub>e</sub> ≤ D<sub>4</sub>. Pixels at the same D<sub>4</sub> form a <b>diamond</b>; at the same D<sub>8</sub> a <b>square</b>.</p>'
        '<div class="trap"><b>Different from paths:</b> D<sub>4</sub> and D<sub>8</sub> ignore pixel values. The textbook’s D<sub>m</sub> is the length of the shortest m-path, so it <i>does</i> depend on the values.</div>'
        '</div><div>' + figs(gsvg(d4, ring(d4, 2), cell=38, idx=False, label='D₄ from the centre: the 2s form a diamond'), gsvg(d8, ring(d8, 2), cell=38, idx=False, label='D₈: the 2s form a square'), gsvg(de, {(i, j): 'hl' for i in range(n) for j in range(n) if de[i][j] == 2}, cell=48, idx=False, label='Dₑ (1 decimal): circles')) + '</div></div>',
        use='Quiz-1 2021 Q1 (Euclidean and city-block), Quiz-1 2018-19 (D<sub>4</sub>, D<sub>8</sub>). Calculator only for D<sub>e</sub>.', tag='6'))

    H.append(h3('Check your own paths: the path lab'))
    H.append('<div class="lab" data-lab="path" data-init=\'{"f": [[3, 1, 2, 1], [2, 2, 0, 2], [1, 2, 1, 1], [1, 0, 1, 2]], "V": "0 1", "p": "3 0", "q": "0 3", "title": "Path lab: shortest 4-, 8- and m-paths"}\'></div>')

    # ── questions ──
    H.append('<h3 id="ch2-px-q">Questions on pixel relationships</h3>')
    V01 = shade(I18, {0, 1}); V12 = shade(I18, {1, 2})
    reach = {(3, 0), (2, 0), (3, 1), (3, 2), (2, 2), (1, 2), (2, 3)}
    H.append(set_solution(card('s19q1'), walk([
        ('Shade the pixels allowed by V = {0, 1}', 'Blue = value 0 or 1. p = (3, 0) and q = (0, 3) are both blue, so paths may exist.', gsvg(I18, V01, small={(3, 0): 'p', (0, 3): 'q'})),
        ('4-path (V = {0, 1}): none', 'Ripple out from p using only up/down/left/right steps: you reach the light-blue pixels and then get stuck. q’s only side-neighbours are (0, 2) = 2 and (1, 3) = 2, both outside V — nothing can step into q from the side. <b>So no 4-path exists.</b>', gsvg(I18, {**V01, **{z: 'c4' for z in reach}}, ring=[(0, 2), (1, 3)], small={(3, 0): 'p', (0, 3): 'q'})),
        ('8-path (V = {0, 1}): length 4', 'Diagonal steps are allowed, so the last step (1, 2) → (0, 3) can cut the corner. Shortest: (3,0) → (3,1) → (2,2) → (1,2) → (0,3), <b>4 steps</b>.', gsvg(I18, V01, path=[(3, 0), (3, 1), (2, 2), (1, 2), (0, 3)])),
        ('m-path (V = {0, 1}): check every diagonal of the 8-path', 'Diagonal (3,1) → (2,2): its corner pixels are (3,2) = 1 and (2,1) = 2. (3,2) is in V, so you must go round it → refused. Diagonal (1,2) → (0,3): corners (0,2) = 2 and (1,3) = 2, neither in V → allowed.', gsvg(I18, V01, cross=[((3, 1), (2, 2))], ring=[(3, 2)])),
        ('m-path (V = {0, 1}): length 5', 'Go round through (3, 2): (3,0) → (3,1) → (3,2) → (2,2) → (1,2) → (0,3), <b>5 steps</b> — one more than the 8-path.', gsvg(I18, V01, path=[(3, 0), (3, 1), (3, 2), (2, 2), (1, 2), (0, 3)])),
        ('Now V = {1, 2}: shade again, then the 4-path', 'Different pixels are blue now. Ripple with side steps: up the left column, then along the top: (3,0) → (2,0) → (1,0) → (1,1) → (0,1) → (0,2) → (0,3), <b>6 steps</b>.', gsvg(I18, V12, path=[(3, 0), (2, 0), (1, 0), (1, 1), (0, 1), (0, 2), (0, 3)])),
        ('8-path (V = {1, 2}): length 4', 'Two diagonals shorten it: (3,0) → (2,0) → (1,1) → (0,2) → (0,3), <b>4 steps</b>.', gsvg(I18, V12, path=[(3, 0), (2, 0), (1, 1), (0, 2), (0, 3)])),
        ('m-path (V = {1, 2}): length 6', 'Diagonal (2,0) → (1,1): corners (1,0) = 2 and (2,1) = 2 are in V → refused. Diagonal (1,1) → (0,2): corner (0,1) = 1 is in V → refused. With every shortcut refused, the m-path is the same as the 4-path: <b>6 steps</b>.', gsvg(I18, V12, cross=[((2, 0), (1, 1)), ((1, 1), (0, 2))], ring=[(1, 0), (2, 1), (0, 1)])),
    ]) + '<div class="ansbig">(a) V = {0, 1}: no 4-path (q’s side-neighbours are both 2); 8-path length 4; m-path length 5. (b) V = {1, 2}: 4-path length 6; 8-path length 4; m-path length 6.</div>'))

    G19 = [[0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [1, 0, 0, 1, 0, 0, 1, 0, 0, 1], [1, 0, 0, 1, 0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 1, 1, 1]]
    base = {(i, j): 'out' for i in range(4) for j in range(10)}
    S1 = [(1, 3), (2, 3), (3, 2), (3, 3), (3, 4)]
    S2a, S2b, S2c = [(0, 7), (0, 8)], [(1, 6), (2, 6), (2, 5)], [(3, 7), (3, 8)]
    col = lambda groups: {**base, **{z: c for c, g in groups for z in g}}
    H.append(set_solution(card('q19q2'), walk([
        ('Read the figure', 'S1 = columns 1–4, S2 = columns 5–8 (rows 0–3). Only pixels with value 1 count (V = {1}). Pixels outside the two boxes (columns 0 and 9) are ignored.', gsvg(G19, col([('c1', S1), ('c2', S2a + S2b + S2c)]), ring=[(3, 2), (0, 8)], cell=40, label='green = S1’s 1s, orange = S2’s 1s, red squares = the two boxed pixels')),
        ('Components in S1', 'Its 1s are (1,3), (2,3) going down, then (3,2), (3,3), (3,4) along the bottom: one connected L-shape with side steps → <b>1 component</b> with 4-adjacency, and also 1 with 8-adjacency.', gsvg(G19, col([('c1', S1)]), cell=40)),
        ('Components in S2', 'Three blobs that touch each other only at corners: {(0,7), (0,8)}, {(1,6), (2,6), (2,5)}, {(3,7), (3,8)}. With 4-adjacency corners do not join → <b>3 components</b>. With 8-adjacency (0,7)–(1,6) and (2,6)–(3,7) join them → <b>1 component</b>.', gsvg(G19, col([('c1', S2a), ('c2', S2b), ('c3', S2c)]), links=[((0, 7), (1, 6)), ((2, 6), (3, 7))], cell=40)),
        ('Are S1 and S2 adjacent?', 'Look across the border between column 4 and column 5: S1’s (3,4) and S2’s (2,5) touch only at a corner. Their corner pixels (2,4) and (3,5) are both 0. So they are <b>8-adjacent</b> (and m-adjacent, because no corner pixel is in V) but <b>not 4-adjacent</b>.', gsvg(G19, col([('c1', S1), ('c2', S2b)]), links=[((3, 4), (2, 5))], ring=[(2, 4), (3, 5)], cell=40)),
        ('Distances between the boxed pixels', 'Boxed pixels (3, 2) and (0, 8): Δx = 3 rows, Δy = 6 columns. D<sub>4</sub> = 3 + 6 = <b>9</b> (walk 3 up and 6 across); D<sub>8</sub> = max(3, 6) = <b>6</b> (3 diagonal steps, then 3 across). Values do not matter for distances.', gsvg(G19, base, ring=[(3, 2), (0, 8)], path=[(3, 2), (2, 3), (1, 4), (0, 5), (0, 6), (0, 7), (0, 8)], cell=40, label='a king’s walk: 6 moves = D₈')),
    ]) + '<div class="ansbig">S1: 1 component (4-) and 1 (8-). S2: 3 components (4-) and 1 (8-). S1 and S2 are 8-adjacent (and m-adjacent), not 4-adjacent. D<sub>4</sub> = 9, D<sub>8</sub> = 6.</div>'))

    st = [[''] * 5 for _ in range(4)]
    for cid in ['tb2-19', 'tb2-20', 'dr-dist']:
        c = card(cid)
        if cid == 'tb2-19':
            c = set_solution(c, walk([
                ('Why D₄ is a lower limit', 'Every side step changes either the row or the column by 1. To get from p to q you need |Δx| row-steps and |Δy| column-steps, so every 4-path has at least D<sub>4</sub> = |Δx| + |Δy| steps.', None),
                ('When the shortest 4-path equals D₄', 'Exactly when some path made only of allowed (V) pixels <b>never moves away from q</b> — a “staircase”. If every staircase is blocked by a pixel outside V, the path must detour and becomes longer than D<sub>4</sub>.', gsvg(st, {(3, 0): 'p', (0, 4): 'q'}, path=[(3, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 3), (0, 4)], label='one staircase from p to q: 7 steps = D₄')),
                ('Is it unique?', 'Usually <b>no</b>: the 3 “up” steps and 4 “right” steps can come in many orders (here 35 different staircases). It is unique only if p and q are in the same row or column, or if V leaves just one staircase open.', gsvg(st, {(3, 0): 'p', (0, 4): 'q'}, path=[(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (2, 4), (1, 4), (0, 4)], label='another staircase, also 7 steps')),
            ]) + '<div class="ansbig">(a) When a 4-path of pixels in V exists that only moves towards q (a staircase); its length is then D<sub>4</sub>. (b) Not unique in general; unique only in special cases (same row/column, or V allows a single staircase).</div>')
        H.append(c)
    H.append('</section>')
    return '\n'.join(H)
