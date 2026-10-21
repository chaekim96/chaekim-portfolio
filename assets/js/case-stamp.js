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
