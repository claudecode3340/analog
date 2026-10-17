/*
 * FSRS-6 core used by the INDEX 0 revision engine. This exact file is inlined at
 * the top of the app's pwp.js at build time, so verify.js tests what runs in the app.
 *
 *   - formulas and default weights: py-fsrs 6.x (open-spaced-repetition)
 *   - fuzz ranges: py-fsrs scheduler.py
 *   - load balancing: weights candidate days like Anki 24.11's load balancer
 *
 * Days are whole numbers (day 0, day 1, ...). Ratings: 1 Again, 2 Hard, 3 Good, 4 Easy.
 * Works in Node (require) and in the browser (window.FSRS6).
 */
(function (root) {
  "use strict";

  var DEFAULT_W = [0.212, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334, 3.0194, 0.001, 1.8722, 0.1666, 0.796,
    1.4835, 0.0614, 0.2629, 1.6483, 0.6014, 1.8729, 0.5425, 0.0912, 0.0658, 0.1542];
  // py-fsrs 6.3.2 LOWER_BOUNDS_PARAMETERS / UPPER_BOUNDS_PARAMETERS
  var LOWER = [0.001, 0.001, 0.001, 0.001, 1.0, 0.001, 0.001, 0.001, 0.0, 0.0, 0.001, 0.001, 0.001, 0.001, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.1];
  var UPPER = [100.0, 100.0, 100.0, 100.0, 10.0, 4.0, 4.0, 0.75, 4.5, 0.8, 3.5, 5.0, 0.25, 0.9, 4.0, 1.0, 6.0, 2.0, 2.0, 0.8, 0.8];

  var W, DECAY, FACTOR;
  var RETENTION = 0.9;   // default target: review when recall probability falls to 90%
  var MAX_IVL = 365;     // never wait more than a year

  // Returns a list of problems with the weights; empty means they're valid.
  function checkParams(p) {
    if (!p || p.length !== 21) return ["expected 21 numbers, got " + (p ? p.length : 0)];
    var errs = [];
    for (var i = 0; i < 21; i++) {
      if (typeof p[i] !== "number" || !isFinite(p[i])) errs.push("w" + i + " is not a number");
      else if (p[i] < LOWER[i] || p[i] > UPPER[i]) errs.push("w" + i + " = " + p[i] + " is outside [" + LOWER[i] + ", " + UPPER[i] + "]");
    }
    return errs;
  }
  // Switch to personalised weights (null = defaults). Invalid weights are refused.
  function setParams(p) {
    if (p && checkParams(p).length) return false;
    W = (p || DEFAULT_W).slice();
    DECAY = -W[20];
    FACTOR = Math.pow(0.9, 1 / DECAY) - 1;
    return true;
  }
  setParams(null);

  function clampD(d) { return Math.min(10, Math.max(1, d)); }

  // Initial difficulty (1 easy .. 10 hard) and stability (days until recall falls to 90%).
  function d0Raw(g) { return W[4] - Math.exp(W[5] * (g - 1)) + 1; }
  function d0(g) { return clampD(d0Raw(g)); }
  function s0(g) { return W[g - 1]; }

  // Forgetting curve: probability you still remember after t days with stability S.
  function retrievability(t, S) { return Math.pow(1 + FACTOR * Math.max(0, t) / S, DECAY); }

  // Exact (unrounded) number of days until retrievability drops to r.
  function rawInterval(S, r) { return S / FACTOR * (Math.pow(r || RETENTION, 1 / DECAY) - 1); }

  // Whole days until retrievability drops to r (default 90%), between 1 and MAX_IVL.
  function interval(S, r) {
    return Math.min(MAX_IVL, Math.max(1, Math.round(rawInterval(S, r))));
  }

  // Difficulty after a rating: Again/Hard push it up, Easy pulls it down, with mean reversion.
  function nextD(D, g) {
    var dd = -W[6] * (g - 3);
    var d1 = D + dd * (10 - D) / 9;
    return clampD(W[7] * d0Raw(4) + (1 - W[7]) * d1);
  }

  // Stability after a successful recall. Grows more when the card was harder to recall (low R),
  // when the card is easy (low D), and less as S is already large.
  function recallS(D, S, R, g) {
    var hard = g === 2 ? W[15] : 1, easy = g === 4 ? W[16] : 1;
    return S * (1 + Math.exp(W[8]) * (11 - D) * Math.pow(S, -W[9]) * (Math.exp((1 - R) * W[10]) - 1) * hard * easy);
  }

  // Stability after forgetting (Again).
  function forgetS(D, S, R) {
    var lt = W[11] * Math.pow(D, -W[12]) * (Math.pow(S + 1, W[13]) - 1) * Math.exp((1 - R) * W[14]);
    return Math.min(lt, S / Math.exp(W[17] * W[18]));
  }

  // Stability after a second review on the same day. The floor at 1 for Hard/Good/Easy
  // matches fsrs-rs (`if rating >= 2.0 { sinc.max(1.0) }`).
  function shortS(S, g) {
    var inc = Math.exp(W[17] * (g - 3 + W[18])) * Math.pow(S, -W[19]);
    if (g >= 2) inc = Math.max(inc, 1);
    return S * inc;
  }

  /**
   * Memory state after rating g on day `now` (card = null for a brand-new card).
   * Returns { S, D, reps, lapses, last, due } with an unfuzzed due date at 90% retention;
   * the engine replaces `due` using the owner's retention, fuzz and load balancing.
   */
  function schedule(card, g, now) {
    var c;
    if (!card) {
      c = { S: Math.max(0.01, s0(g)), D: d0(g), reps: 1, lapses: g === 1 ? 1 : 0, last: now };
    } else {
      var t = now - card.last, S;
      if (t <= 0) S = shortS(card.S, g);
      else {
        var R = retrievability(t, card.S);
        S = g === 1 ? forgetS(card.D, card.S, R) : recallS(card.D, card.S, R, g);
      }
      c = { S: Math.max(0.01, S), D: nextD(card.D, g), reps: card.reps + 1, lapses: card.lapses + (g === 1 ? 1 : 0), last: now };
    }
    c.due = now + (g === 1 ? 1 : interval(c.S));
    return c;
  }

  // ---------------------------------------------------------------- fuzz (py-fsrs)
  var FUZZ_RANGES = [
    { start: 2.5, end: 7.0, factor: 0.15 },
    { start: 7.0, end: 20.0, factor: 0.10 },
    { start: 20.0, end: Infinity, factor: 0.05 }
  ];
  // [min, max] whole-day interval for a whole-day interval `ivl`, or null when no fuzz applies (< 2.5 days).
  function fuzzRange(ivl, maxIvl) {
    if (ivl < 2.5) return null;
    var delta = 1.0;
    for (var i = 0; i < FUZZ_RANGES.length; i++) {
      var r = FUZZ_RANGES[i];
      delta += r.factor * Math.max(Math.min(ivl, r.end) - r.start, 0);
    }
    var lo = Math.max(2, Math.round(ivl - delta));
    var hi = Math.min(Math.round(ivl + delta), maxIvl || MAX_IVL);
    lo = Math.min(lo, hi);
    return { lo: lo, hi: hi, delta: delta };
  }

  // Uniform fuzz (py-fsrs draws uniformly; it can round up to hi + 1, ts-fsrs floors — we floor).
  function fuzz(ivl, rng) {
    var f = fuzzRange(ivl);
    if (!f) return ivl;
    return Math.min(f.hi, f.lo + Math.floor((rng || Math.random)() * (f.hi - f.lo + 1)));
  }

  /**
   * Load-balanced choice of an interval inside the fuzz range.
   *   ivl        unfuzzed whole-day interval
   *   dueOn(d)   how many cards are already due d days from now
   * Weight of each candidate: 1 / (dueOn + 1)^2 * exp(-|d - ivl| / (delta + 1)).
   */
  function balance(ivl, dueOn, rng) {
    var f = fuzzRange(ivl);
    if (!f) return ivl;
    var cands = [], total = 0;
    for (var d = f.lo; d <= f.hi; d++) {
      var w = 1 / Math.pow(dueOn(d) + 1, 2) * Math.exp(-Math.abs(d - ivl) / (f.delta + 1));
      cands.push([d, w]); total += w;
    }
    var x = (rng || Math.random)() * total;
    for (var i = 0; i < cands.length; i++) { x -= cands[i][1]; if (x <= 0) return cands[i][0]; }
    return cands[cands.length - 1][0];
  }

  var api = {
    DEFAULT_W: DEFAULT_W, LOWER: LOWER, UPPER: UPPER, RETENTION: RETENTION, MAX_IVL: MAX_IVL,
    get W() { return W; }, get DECAY() { return DECAY; }, get FACTOR() { return FACTOR; },
    checkParams: checkParams, setParams: setParams,
    d0: d0, s0: s0, nextD: nextD, retrievability: retrievability, rawInterval: rawInterval, interval: interval,
    recallS: recallS, forgetS: forgetS, shortS: shortS, schedule: schedule,
    FUZZ_RANGES: FUZZ_RANGES, fuzzRange: fuzzRange, fuzz: fuzz, balance: balance
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.FSRS6 = api;
})(this);
