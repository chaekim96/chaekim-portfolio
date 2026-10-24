// Hover to play: on the three featured builds, hovering (or focusing) a card steps through
// real screenshots of the app inside its browser frame (on touch screens it plays while the card is in view).
// Reduced-motion visitors see the first frame only.
(function () {
  var root = document.querySelector('[data-play]');
  if (!root || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
  [].forEach.call(root.querySelectorAll('.feat__card'), function (card) {
    var frame = card.querySelector('.browser.play');
    if (!frame) return;
    var imgs = [].slice.call(frame.querySelectorAll('img'));
    if (imgs.length < 2) return;
    var bar = frame.querySelector('.browser__bar');
    if (bar) frame.style.setProperty('--bar-h', bar.offsetHeight + 'px');
    var dots = document.createElement('span'); dots.className = 'play__dots'; dots.setAttribute('aria-hidden', 'true');
    imgs.forEach(function () { dots.appendChild(document.createElement('i')); });
    frame.parentNode.appendChild(dots);
    var i = 0, t = 0;
    function show(k) {
      i = k;
      imgs.forEach(function (im, n) { im.classList.toggle('is-on', n === k); });
      [].forEach.call(dots.children, function (d, n) { d.classList.toggle('is-on', n === k); });
    }
    function start() { if (t) return; frame.classList.add('is-playing'); show(0); t = setInterval(function () { show((i + 1) % imgs.length); }, 1800); }
    function stop() { clearInterval(t); t = 0; frame.classList.remove('is-playing'); show(0); }
    card.addEventListener('mouseenter', start); card.addEventListener('mouseleave', stop);
    if (window.matchMedia && matchMedia('(hover: none)').matches && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? start() : stop(); }); }, { threshold: 0.6 }).observe(frame);
    }
    card.addEventListener('focusin', start); card.addEventListener('focusout', function (e) { if (!card.contains(e.relatedTarget)) stop(); });
    show(0);
  });
})();
