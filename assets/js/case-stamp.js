/* Case pages in the Stamp look: the Berkeley clock in the footer. Email, theme and TOC come from main.js. */
(function () {
  var clock = document.getElementById('clock'), icon = document.getElementById('clock-icon');
  if (!clock || !icon) return;
  var fmt = new Intl.DateTimeFormat('en-US', { hour: 'numeric', minute: '2-digit', timeZone: 'America/Los_Angeles' });
  var hr = new Intl.DateTimeFormat('en-US', { hour: 'numeric', hourCycle: 'h23', timeZone: 'America/Los_Angeles' });
  function tick() {
    var d = new Date(), h = parseInt(hr.format(d), 10);
    clock.textContent = fmt.format(d);
    clock.dateTime = d.toISOString();
    icon.dataset.night = String(h < 6 || h >= 19);
  }
  tick(); setInterval(tick, 30000);
})();

// Artifact screenshots: click (or Enter) to enlarge in a lightbox; click, Escape or × to close.
(function () {
  var imgs = [].filter.call(document.querySelectorAll('.artifacts img'), function (img) { return !img.closest('a'); });
  if (!imgs.length) return;
  var d = document.createElement('dialog');
  d.className = 'lightbox';
  d.setAttribute('aria-label', 'Enlarged image');
  d.innerHTML = '<button class="lightbox__close" type="button" aria-label="Close">×</button><figure><img alt=""><figcaption></figcaption></figure>';
  document.body.appendChild(d);
  var big = d.querySelector('img'), cap = d.querySelector('figcaption');
  function open(img) {
    var src = img.currentSrc || img.src;
    if (typeof d.showModal !== 'function') { window.open(src, '_blank', 'noopener'); return; }
    big.src = src;
    big.alt = img.alt;
    var fc = img.closest('figure') && img.closest('figure').querySelector('figcaption');
    cap.textContent = fc ? fc.textContent : '';
    cap.hidden = !fc;
    d.showModal();
  }
  imgs.forEach(function (img) {
    img.tabIndex = 0;
    img.setAttribute('role', 'button');
    img.setAttribute('aria-label', 'Enlarge: ' + (img.alt || 'image'));
    img.addEventListener('click', function () { open(img); });
    img.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(img); }
    });
  });
  d.addEventListener('click', function (e) {
    if (e.target === d || e.target === big || e.target.closest('.lightbox__close')) d.close();
  });
})();

// Project switcher: the row opens centered on the current build, and the name beside it follows hover and focus.
(function () {
  var bar = document.querySelector('.switcher__bar');
  if (!bar) return;
  var row = bar.querySelector('.switcher__row'), name = bar.querySelector('.switcher__name');
  var cur = row.querySelector('[aria-current]');
  if (cur) {
    var off = cur.offsetLeft - (row.clientWidth - cur.offsetWidth) / 2;
    row.style.scrollBehavior = 'auto'; row.scrollLeft = Math.max(off, 0); row.style.scrollBehavior = '';
  }
  if (!name) return;
  var home = name.textContent;
  function show(a) { name.textContent = a ? a.dataset.name : home; }
  row.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('pointerenter', function () { show(a); });
    a.addEventListener('focus', function () { show(a); });
    a.addEventListener('pointerleave', function () { show(null); });
    a.addEventListener('blur', function () { show(null); });
  });
})();
