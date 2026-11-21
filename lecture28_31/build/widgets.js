(function () {
  var C = { ink: '#1f2633', mute: '#7b8394', blue: '#2563eb', orange: '#ea580c', green: '#059669', red: '#dc2626', purple: '#7c3aed' };
  function el(id) { return document.getElementById(id); }
  function t(x, y, s, c, size, anchor, w) {
    return '<text x="' + x + '" y="' + y + '" fill="' + c + '" font-size="' + (size || 12) + '" text-anchor="' + (anchor || 'start') + '" font-weight="' + (w || 600) + '" font-family="Inter, sans-serif">' + s + '</text>';
  }
  function r(x, y, w, h, c, op) { return '<rect x="' + x + '" y="' + y + '" width="' + Math.max(0, w) + '" height="' + Math.max(0, h) + '" rx="3" fill="' + c + '" opacity="' + (op || 0.85) + '"/>'; }
  function svg(w, h, body) { return '<svg viewBox="0 0 ' + w + ' ' + h + '" width="100%" style="max-width:' + w + 'px">' + body + '</svg>'; }

  // ---- widget 1: Lecture 34 path ----
  if (el('w34')) {
    var g = [1, 5 / 3, 4 / 3, 1], p = [1, 2, 2, 1], names = ['INV', 'NOR2', 'NAND2', 'INV'];
    var draw34 = function () {
      var x = +el('w34x').value, y = +el('w34y').value, z = +el('w34z').value;
      el('w34xv').textContent = ' ' + x.toFixed(1); el('w34yv').textContent = ' ' + y.toFixed(1); el('w34zv').textContent = ' ' + z.toFixed(1);
      var cin = [10, x, y, z], cout = [x, y, z, 45], f = [], D = 0, s = '';
      for (var i = 0; i < 4; i++) { f[i] = g[i] * cout[i] / cin[i]; D += f[i] + p[i]; }
      var base = 160, sc = 14;
      for (i = 0; i < 4; i++) {
        var X = 40 + i * 110, fh = Math.min(f[i], 9);
        s += r(X, base - p[i] * sc, 60, p[i] * sc, C.orange, 0.5) + r(X, base - (p[i] + fh) * sc, 60, fh * sc, C.blue);
        s += t(X + 30, base - (p[i] + fh) * sc - 6, 'f=' + f[i].toFixed(2), C.blue, 12, 'middle', 700);
        s += t(X + 30, base + 16, names[i], C.ink, 12, 'middle');
      }
      s += '<line x1="30" y1="' + base + '" x2="470" y2="' + base + '" stroke="' + C.mute + '"/>';
      var best = 13.11, col = Math.abs(D - best) < 0.05 ? C.green : C.ink;
      s += t(500, 90, 'D = ' + D.toFixed(2) + ' τ', col, 18, 'start', 700);
      s += t(500, 116, 'minimum = 13.11 τ', C.mute, 12, 'start');
      s += t(500, 140, 'F = f₁f₂f₃f₄ = ' + (f[0] * f[1] * f[2] * f[3]).toFixed(2), C.purple, 12, 'start', 700);
      s += t(500, 160, '(always 10, whatever you do)', C.mute, 11, 'start');
      el('w34svg').innerHTML = svg(700, 190, s);
    };
    ['w34x', 'w34y', 'w34z'].forEach(function (k) { el(k).addEventListener('input', draw34); });
    el('w34opt').addEventListener('click', function () { el('w34x').value = 17.78; el('w34y').value = 18.97; el('w34z').value = 25.31; draw34(); });
    el('w34ten').addEventListener('click', function () { el('w34x').value = 10; el('w34y').value = 10; el('w34z').value = 10; draw34(); });
    draw34();
  }

  // ---- widget 2: number of stages ----
  if (el('wN')) {
    var drawN = function () {
      var F = +el('wNF').value, N = +el('wNN').value, s = '', base = 220, best = 1, bestD = 1e9;
      el('wNNv').textContent = ' ' + N;
      for (var n = 1; n <= 10; n++) { var d = n * Math.pow(F, 1 / n) + n; if (d < bestD) { bestD = d; best = n; } }
      var cap = Math.max(2 * bestD, 20), sc = 170 / cap;
      for (n = 1; n <= 10; n++) {
        var e = n * Math.pow(F, 1 / n), X = 30 + (n - 1) * 62, eh = Math.min(e, cap - n);
        var op = n === N ? 1 : 0.35;
        s += r(X, base - n * sc, 44, n * sc, C.orange, op) + r(X, base - (n + eh) * sc, 44, eh * sc, C.blue, op);
        s += t(X + 22, base + 16, 'N=' + n, n === best ? C.red : C.ink, 11, 'middle', n === N ? 700 : 500);
      }
      s += '<line x1="20" y1="' + base + '" x2="660" y2="' + base + '" stroke="' + C.mute + '"/>';
      var f = Math.pow(F, 1 / N), D = N * f + N;
      s += t(20, 18, 'N = ' + N + ':  f = F^(1/N) = ' + f.toFixed(2) + ',  D = ' + N + '·' + f.toFixed(2) + ' + ' + N + ' = ' + D.toFixed(1) + ' τ', C.ink, 13, 'start', 700);
      s += t(20, 38, 'best: N = ' + best + ' (D = ' + bestD.toFixed(1) + ' τ);  log₄F = ' + (Math.log(F) / Math.log(4)).toFixed(2), C.red, 12, 'start', 700);
      el('wNsvg').innerHTML = svg(680, 245, s);
    };
    el('wNF').addEventListener('change', drawN); el('wNN').addEventListener('input', drawN); drawN();
  }

  // ---- widget 3: pseudo-NMOS ratio ----
  if (el('wP')) {
    var VDD = 3.3, VTn = 0.6, VTp = 0.7;
    var I = function (k, u, v) { if (u <= 0) return 0; return v < u ? k * (u * v - v * v / 2) : k * u * u / 2; };
    var solve = function (kn, kp, vi) {
      if (vi <= VTn) return VDD;
      var lo = 0, hi = VDD;
      for (var i = 0; i < 60; i++) { var m = (lo + hi) / 2; if (I(kp, VDD - VTp, VDD - m) - I(kn, vi - VTn, m) > 0) lo = m; else hi = m; }
      return lo;
    };
    var drawP = function () {
      var ratio = +el('wPr').value; el('wPrv').textContent = ' ' + ratio;
      var kp = 1, kn = ratio, W = 600, H = 300, L = 50, B = 40, Tp = 45;
      var X = function (v) { return L + v / VDD * (W - L - 20); }, Y = function (v) { return H - B - v / 3.5 * (H - B - Tp); };
      var pts = [], cm = [];
      for (var i = 0; i <= 200; i++) { var vi = VDD * i / 200; pts.push(X(vi) + ',' + Y(solve(kn, kp, vi))); }
      var s = '<line x1="' + L + '" y1="' + (H - B) + '" x2="' + (W - 10) + '" y2="' + (H - B) + '" stroke="' + C.mute + '"/><line x1="' + L + '" y1="' + Tp + '" x2="' + L + '" y2="' + (H - B) + '" stroke="' + C.mute + '"/>';
      s += '<polyline points="' + pts.join(' ') + '" fill="none" stroke="' + C.blue + '" stroke-width="3"/>';
      var vol = solve(kn, kp, VDD);
      s += '<circle cx="' + X(VDD) + '" cy="' + Y(vol) + '" r="5" fill="' + C.red + '"/>';
      s += t(X(VDD) - 8, Y(vol) - 12, 'V_OL = ' + vol.toFixed(2) + ' V', C.red, 13, 'end', 700);
      s += t(L, 16, 'k_n/k_p = ' + ratio + ':   V_OL = ' + vol.toFixed(2) + ' V', C.ink, 13, 'start', 700);
      s += t(L, 34, 'the pull-up (rising-edge) current is only 1/' + ratio + ' of the NMOS strength, and it flows all the time the output is low', C.mute, 11.5, 'start', 600);
      s += t((L + W) / 2, H - 8, 'V_in (V)', C.ink, 12, 'middle') + t(L - 8, Y(3.3) + 4, '3.3', C.ink, 11, 'end') + t(L - 8, Y(0) + 4, '0', C.ink, 11, 'end') + t(X(3.3), H - B + 16, '3.3', C.ink, 11, 'middle');
      el('wPsvg').innerHTML = svg(W, H, s);
    };
    el('wPr').addEventListener('input', drawP); drawP();
  }
})();
