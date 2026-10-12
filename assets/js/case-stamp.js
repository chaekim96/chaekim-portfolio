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
