/* Command palette: press Cmd K (Ctrl K on Windows and Linux), or use the search button in the header,
   then type a few letters, use the arrow keys and press Enter to jump to any build, tab or page.
   The list is assets/data/palette.json, written at build time by scripts/build-cases.py from the same
   lists the pages are built from, and fetched the first time the palette opens. No dependencies. */
(function () {
  'use strict';
  var DATA_URL = '/assets/data/palette.json';
  var ORDER = ['Tabs', 'Builds', 'Work', 'Writing', 'Pages', 'More'];
  var isMac = /Mac|iPhone|iPad|iPod/.test(navigator.platform || navigator.userAgent || '');
  var keyLabel = isMac ? '⌘K' : 'Ctrl K';

  var items = null, pending = null, failed = false;
  var dialog, input, list, status, opener, lastFocus = null;
  var shown = [], active = 0;

  function load() {
    if (items || pending) return pending;
    pending = fetch(DATA_URL).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { items = d; if (dialog && dialog.open) render(); })
      .catch(function () { failed = true; pending = null; if (dialog && dialog.open) render(); });
    return pending;
  }

  /* ---------- search ---------- */
  function subsequence(q, text) {
    var i = 0;
    for (var j = 0; j < text.length && i < q.length; j++) if (text[j] === q[i]) i++;
    return i === q.length;
  }
  function score(it, q, words) {
    var t = it.t.toLowerCase();
    var hay = t + ' ' + (it.h || '').toLowerCase() + ' ' + (it.k || '') + ' ' + it.g.toLowerCase();
    if (!words.every(function (w) { return hay.indexOf(w) > -1; })) {
      return q.length > 1 && subsequence(q.replace(/\s+/g, ''), t) ? 5 : -1;
    }
    if (t.indexOf(q) === 0) return 100;
    if (t.split(/[^a-z0-9]+/).some(function (w) { return w.indexOf(words[0]) === 0; })) return 80;
    if (t.indexOf(q) > -1) return 60;
    return 30;
  }
  function filter(q) {
    q = q.trim().toLowerCase();
    if (!q) {
      return items.slice().sort(function (a, b) { return ORDER.indexOf(a.g) - ORDER.indexOf(b.g); });
    }
    var words = q.split(/\s+/);
    return items.map(function (it, i) { return { it: it, s: score(it, q, words), i: i }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s || a.i - b.i; })
      .map(function (x) { return x.it; });
  }

  /* ---------- markup ---------- */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function build() {
    dialog = el('dialog', 'palette');
    dialog.setAttribute('aria-label', 'Jump to a page');
    var bar = el('div', 'palette__bar');
    bar.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>';
    input = el('input', 'palette__input');
    input.type = 'text';
    input.placeholder = 'Jump to a build, tab or page';
    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-expanded', 'true');
    input.setAttribute('aria-controls', 'palette-list');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-label', 'Search builds, tabs and pages');
    input.autocomplete = 'off'; input.spellcheck = false;
    var close = el('button', 'palette__close', 'Esc');
    close.type = 'button';
    close.setAttribute('aria-label', 'Close');
    bar.appendChild(input); bar.appendChild(close);
    list = el('ul', 'palette__list');
    list.id = 'palette-list';
    list.setAttribute('role', 'listbox');
    list.setAttribute('aria-label', 'Results');
    status = el('p', 'visually-hidden');
    status.setAttribute('role', 'status');
    var foot = el('div', 'palette__foot');
    foot.innerHTML = '<span><kbd>↑</kbd> <kbd>↓</kbd> to move</span><span><kbd>Enter</kbd> to go</span><span><kbd>Esc</kbd> to close</span>';
    dialog.appendChild(bar); dialog.appendChild(list); dialog.appendChild(status); dialog.appendChild(foot);
    document.body.appendChild(dialog);

    input.addEventListener('input', function () { active = 0; render(); });
    close.addEventListener('click', closePalette);
    dialog.addEventListener('click', function (e) { if (e.target === dialog) closePalette(); });   // the backdrop
    dialog.addEventListener('cancel', function (e) { e.preventDefault(); closePalette(); });         // Esc
    dialog.addEventListener('keydown', onKey);
    list.addEventListener('mousemove', function (e) {
      var li = e.target.closest('[role=option]');
      if (li && +li.dataset.i !== active) { active = +li.dataset.i; mark(); }
    });
    list.addEventListener('click', function (e) {
      var li = e.target.closest('[role=option]');
      if (li) go(shown[+li.dataset.i]);
    });
  }

  function render() {
    list.textContent = '';
    if (failed) { list.appendChild(el('li', 'palette__empty', 'The list did not load. Try the Builds tab instead.')); shown = []; return; }
    if (!items) { list.appendChild(el('li', 'palette__empty', 'Loading')); shown = []; return; }
    shown = filter(input.value);
    if (!shown.length) {
      list.appendChild(el('li', 'palette__empty', 'Nothing matches "' + input.value.trim() + '"'));
      input.removeAttribute('aria-activedescendant');
      status.textContent = 'No results';
      return;
    }
    var grouped = !input.value.trim(), lastG = null;
    shown.forEach(function (it, i) {
      if (grouped && it.g !== lastG) {
        lastG = it.g;
        var gh = el('li', 'palette__group', it.g);
        gh.setAttribute('role', 'presentation');
        list.appendChild(gh);
      }
      var li = el('li', 'palette__item');
      li.id = 'palette-opt-' + i; li.dataset.i = i;
      li.setAttribute('role', 'option');
      if (it.m) {
        var img = el('img'); img.src = it.m; img.alt = ''; img.width = 24; img.height = 24; li.appendChild(img);
      } else {
        li.appendChild(el('span', 'palette__blank', it.g === 'Tabs' ? '#' : '→'));
        li.lastChild.setAttribute('aria-hidden', 'true');
      }
      li.appendChild(el('span', '', it.t));
      var hint = grouped ? (it.h || '') : (it.g + (it.h && it.h !== it.g ? ' · ' + it.h : ''));
      if (hint) li.appendChild(el('small', '', hint));
      list.appendChild(li);
    });
    status.textContent = shown.length + (shown.length === 1 ? ' result' : ' results');
    mark();
  }
  function mark() {
    var opts = list.querySelectorAll('[role=option]');
    for (var i = 0; i < opts.length; i++) opts[i].setAttribute('aria-selected', i === active ? 'true' : 'false');
    if (opts[active]) {
      input.setAttribute('aria-activedescendant', opts[active].id);
      opts[active].scrollIntoView({ block: 'nearest' });
    }
  }

  /* ---------- behavior ---------- */
  function onKey(e) {
    var n = shown.length;
    if (e.key === 'ArrowDown') { e.preventDefault(); if (n) { active = (active + 1) % n; mark(); } }
    else if (e.key === 'ArrowUp') { e.preventDefault(); if (n) { active = (active - 1 + n) % n; mark(); } }
    else if (e.key === 'Home' && e.target === input && !input.value) { e.preventDefault(); active = 0; mark(); }
    else if (e.key === 'End' && e.target === input && !input.value) { e.preventDefault(); active = Math.max(n - 1, 0); mark(); }
    else if (e.key === 'Enter') { if (e.target === input && shown[active]) { e.preventDefault(); go(shown[active]); } }
    else if (e.key === 'Escape') { e.preventDefault(); closePalette(); }
    else if (e.key === 'Tab') {               // keep focus inside: the search box and the close button
      var f = dialog.querySelectorAll('input, button');
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  }
  function go(it) {
    if (!it) return;
    var url = new URL(it.u, location.href);
    closePalette(true);
    if (url.pathname === location.pathname && url.hash) { location.hash = url.hash; }
    else location.href = url.href;
  }
  function openPalette() {
    if (dialog && dialog.open) return;
    if (document.querySelector('dialog[open]')) return;     // the live preview or a lightbox is open
    if (!dialog) build();
    lastFocus = document.activeElement;
    input.value = ''; active = 0;
    if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', '');
    load(); render();
    input.focus();
  }
  function closePalette(skipFocus) {
    if (!dialog || !dialog.open) return;
    if (typeof dialog.close === 'function') dialog.close(); else dialog.removeAttribute('open');
    if (skipFocus === true) return;
    var back = lastFocus && document.contains(lastFocus) ? lastFocus : opener;
    if (back && back.focus) back.focus();
  }

  document.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && !e.altKey && !e.shiftKey && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      if (dialog && dialog.open) closePalette(); else openPalette();
    }
  });

  /* a small, visible way in for people who do not know the shortcut */
  function addOpener() {
    var toggle = document.querySelector('.topnav .theme-toggle, .top .theme-toggle');
    if (!toggle) return;
    opener = el('button', 'palette-open');
    opener.type = 'button';
    opener.setAttribute('aria-label', 'Search the site (' + keyLabel + ')');
    opener.setAttribute('aria-haspopup', 'dialog');
    opener.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><kbd></kbd>';
    opener.querySelector('kbd').textContent = keyLabel;
    toggle.parentNode.insertBefore(opener, toggle);
    opener.addEventListener('click', openPalette);
    opener.addEventListener('pointerenter', load, { once: true });
    opener.addEventListener('focus', load, { once: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', addOpener); else addOpener();
})();
