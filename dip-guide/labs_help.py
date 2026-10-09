"""A 'how to use this lab' box in front of every interactive lab, and a clearer path lab."""
import re

HELP = {
 'filter': ('A hand-filtering calculator. You type a small image and a kernel; it pads the image the way you choose, slides the kernel over every pixel and fills in the output — the same working you write in the exam.',
            ['Click any output number: the lab highlights the 3×3 window it used, shows the products and their sum.',
             'Change “Operation” from correlation to convolution with a lopsided kernel (put 1 2 3 in its first row) — the output changes, because convolution flips the kernel.',
             'Change the padding (zero → replicate): only the border outputs change; the inside stays the same.',
             'Paste a past-paper image and kernel to check your own answer.'],
            'Scale = the number in front of the kernel (1/16, 1/9, 1/14). Rounding is applied only to the final outputs.'),
 'hist': ('A histogram-equalisation and matching calculator. You type the pixel counts n<sub>k</sub> of each grey level; it builds the running total, s<sub>k</sub> = (L−1) × running total ÷ (number of pixels), rounds it, and shows the new histogram. Optionally give a target histogram to see histogram matching.',
          ['Type a “dark” histogram (big counts at the low levels, e.g. 50 40 20 5 2 1 1 1) and watch the equalised bars move to the right and spread out.',
           'Check that the equalised histogram is NOT flat: whole bars move together, they are never split.',
           'Read the mean and σ line: it is the same as the Statistics app with a Freq column.'],
          'L is taken from the number of counts you type (8 counts → 3-bit, L = 8).'),
 'dft': ('A DFT calculator. Type a row (1-D sequence) or a small image (rows on new lines); it shows every F(u) or F(u,v) — as a + bi, magnitude, or phase — computed with your slides’ formula (no 1/mn unless you choose it).',
         ['Click a coefficient: it expands into the sum it came from and the calculator trick for it.',
          'Switch “Order” to centred: the DC value F(0,0) moves to the middle — this is what “centre the spectrum” means.',
          'Type a constant image (all 1s): only F(0,0) is non-zero, and it equals the number of pixels.'],
         'Real images give F(n−u) = conjugate of F(u): the second half of the row mirrors the first.'),
 'bits': ('A bit-plane calculator. Type a small k-bit image; it writes each pixel in binary (or Gray code) and shows every bit plane as a 0/1 image, plus the image rebuilt from the top planes you keep.',
          ['Set “Keep top planes” to 1, 2, 3: watch the rebuilt image get closer to the original.',
           'Switch to Gray code: the MSB plane does not change, the lower planes do.',
           'Check: plane k = 1 exactly where (pixel ÷ 2<sup>k</sup>, decimals dropped) is odd.'],
          ''),
 'path': ('A path finder for small images. You type the image, the allowed values V, a start pixel p and an end pixel q. It shades the pixels whose value is in V, then finds the SHORTEST 4-path, 8-path and m-path from p to q and draws each one step by step.',
          ['Read each picture: numbered circles = the order of the steps; the length = the last number.',
           'If a path does not exist, the lab says which pixels next to q are not allowed, so you see where the route is cut.',
           'For the m-path it lists every diagonal it had to refuse and the corner pixel that caused it.',
           'Try V = 1 2 instead of 0 1 on the same image and compare.'],
          'Coordinates are (row, column), both from 0, row 0 at the top — the same as f(x, y) in your slides.'),
 'interp': ('An interpolation calculator. Type a small image and a point (x, y) that is between pixels (fractions allowed); it shows the four neighbouring pixels, the four weights, the bilinear value and the nearest-neighbour value, and the whole 2× enlarged image.',
            ['Try the exact centre of four pixels (x.5, y.5): all four weights are 0.25 → the plain average.',
             'Try a point on an edge (e.g. 0, 0.5): only two weights are non-zero → the average of two pixels.',
             'Move the point towards one corner: that corner’s weight grows towards 1.'],
            ''),
 'affine': ('An affine-map finder. Give three points and where they go; it solves for the 3×3 matrix A, checks it, and maps any other point you type.',
            ['Use the End-sem 2022-23 points and compare A with the question card.',
             'Change one target point and see which entries of A change.',
             'Map a point, then map the result back with the inverse mapping.'],
            ''),
 'circ': ('A convolution calculator for 1-D sequences: it shows the ordinary (linear) convolution, then folds it back to an n-point circular convolution, so you see exactly where wrap-around adds terms.',
          ['Leave n blank: you get the linear result.',
           'Set n smaller than len(f) + len(h) − 1: the tail wraps onto the start — those are the extra terms in circular convolution.',
           'Set n ≥ len(f) + len(h) − 1: no wrap, circular = linear (that is why we zero-pad before using the DFT).'],
          ''),
 'gauss': ('A Gaussian-kernel generator: pick the size, σ and c; it prints every weight, the sum, and the normalised kernel.',
           ['Compare σ = 0.7 and σ = 1: a smaller σ puts more weight on the centre (less blur).',
            'Check the corner = edge² rule shown under the kernel.'],
           ''),
 'freq': ('Shows what a small kernel does to each frequency: it plots |H(u,v)|, the kernel’s frequency response.',
          ['Type a smoothing kernel (1 1 1 / 1 1 1 / 1 1 1, scale 1/9): high at the centre (low frequencies pass) → lowpass.',
           'Type a Laplacian (0 1 0 / 1 −4 1 / 0 1 0): zero at the centre, big at the edges → highpass.'],
          ''),
 'alias': ('Draws a cosine and the samples you take of it. If you sample too slowly, the dots also fit a slower cosine (dashed) — that false, slower wave is aliasing.',
           ['Keep the sampling rate above 2 × the frequency: no dashed curve.',
            'Lower the rate below 2 × the frequency: the dashed alias appears.'],
           ''),
 'fft': ('Draws the radix-2 FFT butterfly diagram for 4 or 8 inputs and fills in every intermediate number.',
         ['Type f = 1 2 3 4: the last column should be 10, −2+2i, −2, −2−2i (the same as the 4-point DFT).',
          'Follow one butterfly: top = a + W·b, bottom = a − W·b.'],
         ''),
 'transform': ('Shows an intensity transformation s = T(r) as a curve and applies it to a grey ramp (black → white), so you can see what it does to every grey level at once.',
               ['Choose “negative”: the curve goes down; the bottom strip is the top strip reversed.',
                'Choose “gamma” with γ = 0.4 then γ = 2.5: below 1 brightens the dark part, above 1 darkens it.',
                'Choose “contrast stretch” and move r1, r2 closer together: the steep middle part = more contrast there.'],
               'Read the curve: input on the horizontal axis, output on the vertical. Steeper than the dashed 45° line = that range of greys gets more contrast; flatter = less.'),
}


def help_box(kind):
    what, tries, note = HELP[kind]
    t = ''.join(f'<li>{x}</li>' for x in tries)
    n = f'<p style="margin:8px 0 0;color:var(--muted)">{note}</p>' if note else ''
    return f'<div class="lab-help"><b>What this lab is.</b> {what}<br><b>Try this:</b><ol>{t}</ol>{n}</div>'


def add_help(s):
    return re.sub(r'(<div class="lab" data-lab="([a-z]+)")', lambda m: help_box(m.group(2)) + m.group(1), s)


# ── a path lab that explains itself ──
PATH_JS = r'''function labPath(el){const d=initData(el);
  el.innerHTML='<div class="ctl"><label>Image (rows on new lines)<textarea class="f">'+M2T(d.f||[[3,1,2,1],[2,2,0,2],[1,2,1,1],[1,0,1,2]])+'</textarea></label><label>V (allowed values)<input class="V" value="'+(d.V||'0 1')+'" size="8"></label><label>p = start (row col)<input class="p" value="'+(d.p||'3 0')+'" size="6"></label><label>q = end (row col)<input class="q" value="'+(d.q||'0 3')+'" size="6"></label></div><div class="out"></div>';
  lab(el,d.title||'Path lab: shortest 4-, 8- and m-paths','adjacency · paths · D4 · D8 · De');
  const run=()=>{const out=$('.out',el);try{const f=parseM($('.f',el).value);const V=new Set(parseV($('.V',el).value));const p=parseV($('.p',el).value),q=parseV($('.q',el).value);const M=f.length,N=f[0].length;
    const inV=(r,c)=>r>=0&&c>=0&&r<M&&c<N&&V.has(f[r][c]);const n4=(r,c)=>[[r+1,c],[r-1,c],[r,c+1],[r,c-1]],nd=(r,c)=>[[r+1,c+1],[r+1,c-1],[r-1,c+1],[r-1,c-1]];
    const corner=(a,b)=>[[a[0],b[1]],[b[0],a[1]]];
    const nb=(r,c,kind)=>{const o=n4(r,c).filter(z=>inV(...z));if(kind!==4)nd(r,c).forEach(z=>{if(!inV(...z))return;if(kind==='m'&&corner([r,c],z).some(s=>inV(...s)))return;o.push(z);});return o;};
    const bfs=kind=>{if(!inV(...p)||!inV(...q))return {path:null,seen:new Set()};const key=z=>z.join(',');const prev={[key(p)]:null};const Q=[p];while(Q.length){const u=Q.shift();if(key(u)===key(q))break;for(const v of nb(...u,kind))if(!(key(v) in prev)){prev[key(v)]=u;Q.push(v);}}const seen=new Set(Object.keys(prev));if(!(key(q) in prev))return {path:null,seen};const path=[q];while(prev[key(path[0])])path.unshift(prev[key(path[0])]);return {path,seen};};
    const cs=40,pad=22;let gid=0;
    const svg=(P,seen,ring)=>{gid++;const W=pad+N*cs+4,H=pad+M*cs+4,X=j=>pad+j*cs+cs/2,Y=i=>pad+i*cs+cs/2;let s='<svg class="gsvg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'"><defs><marker id="lp'+gid+(el.id||'')+'" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" class="g-arrowhead"/></marker></defs>';
      for(let j=0;j<N;j++)s+='<text x="'+X(j)+'" y="'+(pad-8)+'" class="g-idx">'+j+'</text>';for(let i=0;i<M;i++)s+='<text x="'+(pad-11)+'" y="'+(Y(i)+5)+'" class="g-idx">'+i+'</text>';
      const on=new Set((P||[]).map(z=>z.join(',')));
      for(let i=0;i<M;i++)for(let j=0;j<N;j++){const k=i+','+j;const c=on.has(k)?'path':(seen&&seen.has(k)&&!P)?'c4':(V.has(f[i][j])?'in':'out');s+='<rect x="'+(pad+j*cs)+'" y="'+(pad+i*cs)+'" width="'+cs+'" height="'+cs+'" class="g-cell g-'+c+'"/><text x="'+X(j)+'" y="'+(Y(i)+6)+'" class="g-val '+(c==='out'?'mu':'dk')+'">'+f[i][j]+'</text>';}
      (ring||[]).forEach(([i,j])=>{s+='<rect x="'+(pad+j*cs+3)+'" y="'+(pad+i*cs+3)+'" width="'+(cs-6)+'" height="'+(cs-6)+'" rx="6" class="g-ring"/>';});
      if(P){for(let k=1;k<P.length;k++){const [i0,j0]=P[k-1],[i1,j1]=P[k];const x0=X(j0),y0=Y(i0),x1=X(j1),y1=Y(i1);s+='<line x1="'+(x0+(x1-x0)*.3)+'" y1="'+(y0+(y1-y0)*.3)+'" x2="'+(x1-(x1-x0)*.3)+'" y2="'+(y1-(y1-y0)*.3)+'" class="g-arrow" marker-end="url(#lp'+gid+(el.id||'')+')"/>';}
        P.forEach(([i,j],k)=>{s+='<circle cx="'+(pad+j*cs+cs-9)+'" cy="'+(pad+i*cs+9)+'" r="7.5" class="g-stepc"/><text x="'+(pad+j*cs+cs-9)+'" y="'+(pad+i*cs+13)+'" class="g-step">'+k+'</text>';});}
      return s+'</svg>';};
    const P2=z=>'('+z.join(', ')+')';
    let h='<div class="legend"><span><i style="background:#cfe8ff"></i>value is in V (allowed)</span><span><i style="background:var(--surface-2)"></i>not allowed</span><span><i style="background:#ffe08a"></i>the shortest path</span><span><i style="background:#a7dcf5"></i>everything reachable from p (shown when q cannot be reached)</span><span><i style="border:3px solid #d92d20"></i>corner pixel that forbids a diagonal step</span></div>';
    h+='<div class="msg">Distances ignore pixel values: D<sub>e</sub> = √('+(p[0]-q[0])+'² + '+(p[1]-q[1])+'²) = '+nf(Math.hypot(p[0]-q[0],p[1]-q[1]),4)+' · D<sub>4</sub> = |'+(p[0]-q[0])+'| + |'+(p[1]-q[1])+'| = '+(Math.abs(p[0]-q[0])+Math.abs(p[1]-q[1]))+' · D<sub>8</sub> = max = '+Math.max(Math.abs(p[0]-q[0]),Math.abs(p[1]-q[1]))+'</div><div class="figrow">';
    if(!inV(...p)||!inV(...q)){out.innerHTML=h+'</div><div class="msg">p = '+P2(p)+' has value '+f[p[0]][p[1]]+', q = '+P2(q)+' has value '+f[q[0]][q[1]]+'. Both must be in V for any path to exist.</div>';return;}
    const r8=bfs(8);
    for(const kind of [4,8,'m']){const r=bfs(kind),P=r.path;let why='',ring=[];
      if(!P){const qn=(kind===4?n4(...q):n4(...q).concat(nd(...q))).filter(z=>z[0]>=0&&z[1]>=0&&z[0]<M&&z[1]<N);const bad=qn.filter(z=>!inV(...z));why='No '+kind+'-path. Starting at p and taking only allowed '+(kind===4?'up/down/left/right':'')+' steps, you can reach only the light-blue pixels; q is never reached'+(kind===4?' — its 4-neighbours '+qn.map(z=>P2(z)+'='+f[z[0]][z[1]]).join(', ')+(bad.length===qn.length?' are all outside V, so nothing can step into q.':'.'):'.');}
      else{why='Length '+(P.length-1)+' (count the steps, not the pixels): '+P.map(P2).join(' → ')+'.';
        if(kind==='m'&&r8.path&&r8.path.length<P.length){const rej=[];for(let k=1;k<r8.path.length;k++){const a=r8.path[k-1],b=r8.path[k];if(a[0]!==b[0]&&a[1]!==b[1]){const cc=corner(a,b).filter(s=>inV(...s));if(cc.length){rej.push('diagonal '+P2(a)+'→'+P2(b)+' refused: corner '+cc.map(z=>P2(z)+'='+f[z[0]][z[1]]).join(' and ')+' is in V, so you must go round it');ring=ring.concat(cc);}}}if(rej.length)why+=' Longer than the 8-path because '+rej.join('; ')+'.';}
        if(kind==='m'&&r8.path&&r8.path.length===P.length)why+=' Same length as the 8-path: every diagonal it uses has both corner pixels outside V.';}
      h+='<figure class="gfig">'+svg(P,r.seen,ring)+'<figcaption style="max-width:400px;text-align:left"><b>'+kind+'-path.</b> '+why+'</figcaption></figure>';}
    out.innerHTML=h+'</div>';}catch(e){out.innerHTML='<div class="msg">'+e.message+'</div>';}};'''


def patch_path_lab(s):
    i = s.find('function labPath(el){')
    j = s.find('}catch(e){out.innerHTML=', i)
    j = s.find('};', j) + 2
    assert i > 0 and j > i
    return s[:i] + PATH_JS + s[j:]
