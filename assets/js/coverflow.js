// Builds Cover Flow: drag, flick, scroll, or use the keys; click the center cover to flip it.
// Motion is deliberately slow and soft. Reduced-motion visitors get instant moves.
(function () {
  var root = document.querySelector('[data-coverflow]');
  if (!root) return;
  var stage = root.querySelector('.cf__stage');
  var C = [].slice.call(stage.querySelectorAll('.cf__cv'));
  var T = root.querySelector('.cf__t'), H = root.querySelector('.cf__h');
  var SC = root.querySelector('.cf__scrub'), N = root.querySelector('.cf__n');
  var n = C.length; if (!n) return;
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var EASE = still ? 1 : 0.075;          // share of the remaining distance covered per frame
  var S = 240, pos = Math.min(1, n - 1), target = pos, vel = 0, flipped = -1, raf = 0, shown = -1;

  function size() {
    S = Math.round(Math.min(260, Math.max(168, root.clientWidth * 0.24)));
    root.style.setProperty('--s', S + 'px');
  }
  function clampP(p) { return Math.max(0, Math.min(n - 1, p)); }
  function render() {
    var gap = S * 0.34, side = S * 0.7;
    for (var k = 0; k < n; k++) {
      var o = k - pos, a = Math.abs(o), cl = Math.max(-1, Math.min(1, o)), m = Math.min(a, 1);
      var x = o * gap + cl * side, ry = -cl * 58, z = (1 - m) * S * 0.2 - m * S * 0.12, sc = 1 - m * 0.06;
      var c = C[k];
      c.style.transform = 'translateX(' + x + 'px) translateZ(' + z + 'px) rotateY(' + ry + 'deg) scale(' + sc + ')';
      c.style.zIndex = 1000 - Math.round(a * 10);
      c.style.opacity = a > 5.5 ? 0 : 1;
      c.style.visibility = a > 6 ? 'hidden' : 'visible';
    }
    var i = Math.round(clampP(pos));
    if (i !== shown) {
      if (shown >= 0) C[shown].setAttribute('aria-selected', 'false');
      C[i].setAttribute('aria-selected', 'true');
      T.textContent = C[i].getAttribute('data-title');
      H.textContent = C[i].getAttribute('data-heading');
      SC.value = i; N.textContent = (i + 1) + ' / ' + n; shown = i;
    }
    if (flipped >= 0 && flipped !== i) { C[flipped].classList.remove('is-flipped'); flipped = -1; }
  }
  function loop() {
    var d = target - pos;
    pos += d * EASE;
    if (Math.abs(d) < 0.0006) { pos = target; raf = 0; render(); return; }
    render(); raf = requestAnimationFrame(loop);
  }
  function go(t) { target = clampP(t); if (!raf) raf = requestAnimationFrame(loop); }
  function stop() { cancelAnimationFrame(raf); raf = 0; }
  function toggle(k) {
    if (flipped === k) { C[k].classList.remove('is-flipped'); flipped = -1; }
    else { if (flipped >= 0) C[flipped].classList.remove('is-flipped'); C[k].classList.add('is-flipped'); flipped = k; }
  }

  var down = null;
  stage.addEventListener('pointerdown', function (e) {
    if (e.button > 0 || e.target.closest('a')) return;
    stop(); vel = 0;
    down = { x: e.clientX, p: pos, lx: e.clientX, lt: performance.now(), moved: 0, el: e.target.closest('.cf__cv') };
    stage.setPointerCapture(e.pointerId); stage.classList.add('is-dragging');
  });
  stage.addEventListener('pointermove', function (e) {
    if (!down) return;
    var dx = e.clientX - down.x, now = performance.now(), dt = Math.max(8, now - down.lt);
    down.moved = Math.max(down.moved, Math.abs(dx));
    vel = 0.75 * vel + 0.25 * ((e.clientX - down.lx) / dt);
    down.lx = e.clientX; down.lt = now;
    var p = down.p - dx / (S * 0.34);
    if (p < 0) p *= 0.3; if (p > n - 1) p = n - 1 + (p - (n - 1)) * 0.3;   // soft edges
    pos = target = p; render();
  });
  function up() {
    if (!down) return;
    stage.classList.remove('is-dragging');
    if (down.moved < 6) {
      if (down.el) { var k = C.indexOf(down.el); if (k === Math.round(pos)) toggle(k); else go(k); }
      else go(Math.round(pos));
    } else {
      var v = Math.max(-2, Math.min(2, vel));
      go(Math.round(pos + Math.max(-3, Math.min(3, -v * 160 / (S * 0.34)))));
    }
    down = null;
  }
  stage.addEventListener('pointerup', up);
  stage.addEventListener('pointercancel', up);

  var wt;
  stage.addEventListener('wheel', function (e) {
    var d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : 0;   // vertical wheel keeps scrolling the page
    if (!d) return;
    e.preventDefault(); stop();
    pos = target = Math.max(-0.3, Math.min(n - 0.7, pos + d / (S * 1.8))); render();
    clearTimeout(wt); wt = setTimeout(function () { go(Math.round(pos)); }, 160);
  }, { passive: false });
  stage.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { go(Math.round(target) + 1); e.preventDefault(); }
    else if (e.key === 'ArrowLeft') { go(Math.round(target) - 1); e.preventDefault(); }
    else if (e.key === 'Enter' || e.key === ' ') { toggle(Math.round(pos)); e.preventDefault(); }
  });
  root.querySelector('.cf__prev').addEventListener('click', function () { go(Math.round(target) - 1); });
  root.querySelector('.cf__next').addEventListener('click', function () { go(Math.round(target) + 1); });
  SC.addEventListener('input', function () { go(+SC.value); });
  window.addEventListener('resize', function () { size(); render(); });

  size(); render();
})();
