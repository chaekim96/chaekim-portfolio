// A mark's white detail moves only while the mark is hovered or focused (the case-hero mark also moves with its
// "Try it live" link). At rest, and always under reduced motion, the plain static mark stays.
// The animated files are assets/img/brand/live/. Marks opt in with data-spark; a link around the mark is its host.
(function () {
  var marks = document.querySelectorAll('img[data-spark]');
  if (!marks.length) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var live = document.querySelector('.live-btn');
  Array.prototype.forEach.call(marks, function (img) {
    var rest = img.getAttribute('src');
    new Image().src = img.dataset.spark; // fetch early so the first hover doesn't flash
    function play(on) { img.setAttribute('src', on ? img.dataset.spark : rest); }
    var hosts = [img.closest('a') || img];
    if (live && img.classList.contains('case-hero__mark')) hosts.push(live);
    hosts.forEach(function (h) {
      h.addEventListener('pointerenter', function () { play(true); });
      h.addEventListener('pointerleave', function () { play(false); });
      h.addEventListener('focus', function () { play(true); });
      h.addEventListener('blur', function () { play(false); });
    });
  });
})();
