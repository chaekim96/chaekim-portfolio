// Live previews: "Try it live" opens the real app in a dialog; closing it unloads the app.
(function () {
  var d = document.getElementById('live');
  if (!d || typeof d.showModal !== 'function') return; // no <dialog>: links open in a new tab
  var frame = document.getElementById('live-frame'), title = document.getElementById('live-title'),
      open = document.getElementById('live-open'), note = document.getElementById('live-note');
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-live]');
    if (!b || e.metaKey || e.ctrlKey || e.shiftKey) return; // modified clicks still open a tab
    e.preventDefault();
    title.textContent = b.dataset.liveTitle;
    frame.title = b.dataset.liveTitle + ', running live';
    open.href = b.dataset.live;
    note.textContent = b.dataset.liveNote || '';
    note.hidden = !b.dataset.liveNote;
    frame.src = b.dataset.live;
    d.showModal();
    document.documentElement.classList.add('live-open');
  });
  d.querySelector('.live__close').addEventListener('click', function () { d.close(); });
  d.addEventListener('click', function (e) { if (e.target === d) d.close(); }); // backdrop
  d.addEventListener('close', function () {
    frame.src = 'about:blank';
    document.documentElement.classList.remove('live-open');
  });
})();
