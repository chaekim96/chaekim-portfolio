/* Chae Kim — Portfolio: small, dependency-free interactions. */
(function () {
  const root = document.documentElement;

  /* ---------- Theme toggle (persists per browser) ---------- */
  const THEME_KEY = 'ck-theme';
  function applyTheme(t) {
    if (t) root.setAttribute('data-theme', t); else root.removeAttribute('data-theme');
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      const isDark = t === 'dark' || (!t && matchMedia('(prefers-color-scheme: dark)').matches);
      btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
      btn.dataset.mode = isDark ? 'dark' : 'light';
    });
  }
  let saved = null;
  try { saved = localStorage.getItem(THEME_KEY); } catch (e) {}
  applyTheme(saved);
  document.querySelectorAll('.theme-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const isDark = btn.dataset.mode === 'dark';
      const next = isDark ? 'light' : 'dark';
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
      applyTheme(next);
    });
  });

  /* ---------- Mobile nav ---------- */
  const burger = document.querySelector('.nav__burger');
  const links = document.querySelector('.nav__links');
  if (burger && links) {
    burger.addEventListener('click', () => {
      const open = links.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
    });
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('is-open')));
  }

  /* ---------- Project filters ---------- */
  const chips = document.querySelectorAll('[data-filter]');
  const cards = document.querySelectorAll('[data-cat]');
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.toggle('is-active', c === chip));
      const f = chip.dataset.filter;
      cards.forEach(card => {
        const cats = card.dataset.cat.split(' ');
        card.classList.toggle('is-hidden', !(f === 'all' || cats.includes(f)));
      });
    });
  });

  /* ---------- Reveal on scroll ---------- */
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('is-in'));
  }

  /* ---------- Case-study table of contents highlight ---------- */
  const tocLinks = document.querySelectorAll('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const map = new Map();
    tocLinks.forEach(a => { const id = a.getAttribute('href').slice(1); const h = document.getElementById(id); if (h) map.set(h, a); });
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { tocLinks.forEach(a => a.classList.remove('is-active')); map.get(e.target)?.classList.add('is-active'); }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    map.forEach((_, h) => io.observe(h));
  }

  /* ---------- Pencil-sketch thumbnails ---------- */
  // Clone each thumbnail into an inverted, blurred, color-dodge layer (the classic
  // Photoshop "pencil sketch" recipe). CSS handles the blend; hover fades it away.
  document.querySelectorAll('.card__media:not(.card__media--line) > img').forEach(img => {
    const layer = img.cloneNode(false);
    layer.className = 'sketch-layer';
    layer.alt = '';
    layer.setAttribute('aria-hidden', 'true');
    img.insertAdjacentElement('afterend', layer);
  });

  /* ---------- Live background: drifting color orbs + cursor-aware dot grid ---------- */
  const canvas = document.getElementById('bg');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (canvas && canvas.getContext) {
    const ctx = canvas.getContext('2d');
    let w, h, dpr, orbs = [], mouse = { x: -9999, y: -9999, tx: -9999, ty: -9999 };
    const PALETTE = [
      [36, 86, 255],   // accent blue
      [255, 226, 52],  // marker yellow
      [255, 122, 182], // pink
      [70, 220, 190],  // mint
      [140, 120, 255], // violet
      [255, 170, 80]   // orange
    ];
    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.width = Math.floor(innerWidth * dpr);
      h = canvas.height = Math.floor(innerHeight * dpr);
      canvas.style.width = innerWidth + 'px'; canvas.style.height = innerHeight + 'px';
    }
    function seed() {
      orbs = PALETTE.map((c, i) => ({
        c, r: (0.22 + Math.random() * 0.18) * Math.max(w, h),
        x: Math.random() * w, y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.25 * dpr, vy: (Math.random() - 0.5) * 0.25 * dpr,
        a: 0.16 + (i % 2) * 0.06
      }));
    }
    const isDark = () => root.getAttribute('data-theme') === 'dark';
    function draw(t) {
      ctx.clearRect(0, 0, w, h);
      // orbs
      const dark = isDark();
      ctx.globalCompositeOperation = dark ? 'screen' : 'multiply';
      orbs.forEach((o, i) => {
        if (!reduce) {
          o.x += o.vx + Math.sin(t / 4000 + i) * 0.15 * dpr;
          o.y += o.vy + Math.cos(t / 5000 + i * 1.7) * 0.15 * dpr;
          if (o.x < -o.r) o.x = w + o.r; if (o.x > w + o.r) o.x = -o.r;
          if (o.y < -o.r) o.y = h + o.r; if (o.y > h + o.r) o.y = -o.r;
        }
        const g = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
        const [r, gg, b] = o.c;
        g.addColorStop(0, `rgba(${r},${gg},${b},${dark ? o.a * 0.9 : o.a})`);
        g.addColorStop(1, `rgba(${r},${gg},${b},0)`);
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(o.x, o.y, o.r, 0, Math.PI * 2); ctx.fill();
      });
      // dot grid, gently pushed by the cursor
      ctx.globalCompositeOperation = 'source-over';
      mouse.x += (mouse.tx - mouse.x) * 0.08; mouse.y += (mouse.ty - mouse.y) * 0.08;
      const step = 28 * dpr, R = 160 * dpr;
      ctx.fillStyle = dark ? 'rgba(242,240,234,0.16)' : 'rgba(16,18,35,0.14)';
      for (let y = step / 2; y < h; y += step) {
        for (let x = step / 2; x < w; x += step) {
          const dx = x - mouse.x, dy = y - mouse.y, d = Math.hypot(dx, dy);
          let px = x, py = y, s = 1;
          if (d < R) { const k = (1 - d / R); px += (dx / (d || 1)) * k * 14 * dpr; py += (dy / (d || 1)) * k * 14 * dpr; s = 1 + k * 1.6; }
          ctx.beginPath(); ctx.arc(px, py, 1.1 * dpr * s, 0, Math.PI * 2); ctx.fill();
        }
      }
      if (!reduce) requestAnimationFrame(draw);
    }
    resize(); seed(); requestAnimationFrame(draw);
    let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { resize(); seed(); if (reduce) draw(0); }, 150); });
    addEventListener('pointermove', e => { mouse.tx = e.clientX * dpr; mouse.ty = e.clientY * dpr; }, { passive: true });
    addEventListener('pointerleave', () => { mouse.tx = -9999; mouse.ty = -9999; });
    if (reduce) { mouse.x = mouse.tx = -9999; }
  }

  /* ---------- Footer year ---------- */
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
