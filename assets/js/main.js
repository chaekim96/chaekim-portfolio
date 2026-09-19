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

  /* ---------- Live background: wafting clouds on a soft sky ---------- */
  const canvas = document.getElementById('bg');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isDark = () => root.getAttribute('data-theme') === 'dark';
  if (canvas && canvas.getContext) {
    const ctx = canvas.getContext('2d');
    let w, h, dpr, clouds = [], wisps = [], mouse = { x: -9999, y: -9999, tx: -9999, ty: -9999 };
    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.width = Math.floor(innerWidth * dpr);
      h = canvas.height = Math.floor(innerHeight * dpr);
      canvas.style.width = innerWidth + 'px'; canvas.style.height = innerHeight + 'px';
    }
    function seed() {
      // big, faint sky-blue wisps (the "gradient")
      wisps = Array.from({ length: 5 }, (_, i) => ({
        r: (0.35 + Math.random() * 0.25) * Math.max(w, h),
        x: Math.random() * w, y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.12 * dpr, vy: (Math.random() - 0.5) * 0.08 * dpr,
        a: 0.10 + (i % 2) * 0.05, hue: i % 2 ? [30, 91, 255] : [120, 190, 255]
      }));
      // clouds: clusters of soft white puffs drifting left → right
      clouds = Array.from({ length: 9 }, () => makeCloud(Math.random() * w));
    }
    function makeCloud(x) {
      const scale = 0.5 + Math.random() * 0.9;
      const puffs = Array.from({ length: 5 + Math.floor(Math.random() * 4) }, (_, i) => ({
        dx: (i - 3) * 55 * scale * dpr + (Math.random() - 0.5) * 40 * dpr,
        dy: (Math.random() - 0.5) * 34 * scale * dpr,
        r: (48 + Math.random() * 42) * scale * dpr
      }));
      return { x, y: Math.random() * h, v: (0.12 + Math.random() * 0.25) * dpr * (0.6 + scale * 0.5), puffs, scale, a: 0.5 + Math.random() * 0.4, w: 260 * scale * dpr };
    }
    function draw(t) {
      ctx.clearRect(0, 0, w, h);
      const dark = isDark();
      // sky gradient
      const sky = ctx.createLinearGradient(0, 0, 0, h);
      if (dark) { sky.addColorStop(0, '#0f1320'); sky.addColorStop(1, '#0f1013'); }
      else { sky.addColorStop(0, '#eef4ff'); sky.addColorStop(0.55, '#f7faff'); sky.addColorStop(1, '#ffffff'); }
      ctx.fillStyle = sky; ctx.fillRect(0, 0, w, h);
      // wisps
      ctx.globalCompositeOperation = dark ? 'screen' : 'multiply';
      mouse.x += (mouse.tx - mouse.x) * 0.06; mouse.y += (mouse.ty - mouse.y) * 0.06;
      wisps.forEach((o, i) => {
        if (!reduce) {
          o.x += o.vx + Math.sin(t / 6000 + i) * 0.12 * dpr; o.y += o.vy + Math.cos(t / 7000 + i * 1.3) * 0.1 * dpr;
          if (mouse.tx > -9000) { o.x += (mouse.x - o.x) * 0.0008 * (i % 3 + 1); o.y += (mouse.y - o.y) * 0.0008 * (i % 3 + 1); }
          if (o.x < -o.r) o.x = w + o.r; if (o.x > w + o.r) o.x = -o.r; if (o.y < -o.r) o.y = h + o.r; if (o.y > h + o.r) o.y = -o.r;
        }
        const g = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
        const [r, gg, b] = o.hue;
        g.addColorStop(0, `rgba(${r},${gg},${b},${dark ? o.a * 0.8 : o.a})`); g.addColorStop(1, `rgba(${r},${gg},${b},0)`);
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(o.x, o.y, o.r, 0, Math.PI * 2); ctx.fill();
      });
      // clouds
      ctx.globalCompositeOperation = 'source-over';
      clouds.forEach(c => {
        if (!reduce) {
          c.x += c.v;
          // clouds near the cursor get a gentle nudge
          const dx = c.x - mouse.x, dy = c.y - mouse.y, d = Math.hypot(dx, dy);
          if (d < 260 * dpr) { c.x += (dx / d) * 0.6 * dpr; c.y += (dy / d) * 0.6 * dpr; }
          if (c.x - c.w > w) { Object.assign(c, makeCloud(-c.w)); }
        }
        c.puffs.forEach(pf => {
          const px = c.x + pf.dx, py = c.y + pf.dy;
          const g = ctx.createRadialGradient(px, py - pf.r * 0.15, pf.r * 0.1, px, py, pf.r);
          if (dark) { g.addColorStop(0, `rgba(180,200,255,${0.10 * c.a})`); g.addColorStop(1, 'rgba(180,200,255,0)'); }
          else { g.addColorStop(0, `rgba(255,255,255,${0.95 * c.a})`); g.addColorStop(0.6, `rgba(255,255,255,${0.55 * c.a})`); g.addColorStop(1, 'rgba(210,225,255,0)'); }
          ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px, py, pf.r, 0, Math.PI * 2); ctx.fill();
        });
      });
      if (!reduce) requestAnimationFrame(draw);
    }
    resize(); seed(); requestAnimationFrame(draw);
    let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { resize(); seed(); if (reduce) draw(0); }, 150); });
    addEventListener('pointermove', e => { mouse.tx = e.clientX * dpr; mouse.ty = e.clientY * dpr; }, { passive: true });
    addEventListener('pointerleave', () => { mouse.tx = -9999; mouse.ty = -9999; });
  }

  /* ---------- Motion: staggered hero words, parallax memoji, card tilt, magnetic buttons ---------- */
  document.querySelectorAll('[data-stagger]').forEach(el => {
    let i = 0;
    const walk = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            const sp = document.createElement('span'); sp.className = 'w'; sp.style.setProperty('--i', i++); sp.textContent = part; frag.appendChild(sp);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
    };
    walk(el);
  });

  const memoji = document.querySelector('.memoji');
  if (memoji && !reduce) {
    addEventListener('pointermove', e => {
      const x = (e.clientX / innerWidth - 0.5), y = (e.clientY / innerHeight - 0.5);
      memoji.style.transform = `translate(${x * 18}px, ${y * 14}px) rotate(${x * 6}deg)`;
    }, { passive: true });
  }

  if (!reduce && matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.card').forEach(card => {
      card.addEventListener('pointermove', e => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
        card.style.setProperty('--ry', `${px * 10}deg`); card.style.setProperty('--rx', `${-py * 8}deg`);
      });
      card.addEventListener('pointerleave', () => { card.style.setProperty('--ry', '0deg'); card.style.setProperty('--rx', '0deg'); });
    });
    document.querySelectorAll('.btn').forEach(btn => {
      btn.addEventListener('pointermove', e => {
        const r = btn.getBoundingClientRect();
        btn.style.setProperty('--mx', `${((e.clientX - r.left) / r.width - 0.5) * 10}px`);
        btn.style.setProperty('--my', `${((e.clientY - r.top) / r.height - 0.5) * 8}px`);
      });
      btn.addEventListener('pointerleave', () => { btn.style.setProperty('--mx', '0px'); btn.style.setProperty('--my', '0px'); });
    });
  }

  /* ---------- Email (assembled at runtime so it isn't in the HTML) ---------- */
  document.querySelectorAll('[data-user][data-domain]').forEach(el => {
    const addr = el.dataset.user + '@' + el.dataset.domain;
    if (el.tagName === 'A') el.href = 'mailto:' + addr;
    if (el.dataset.show !== undefined) el.textContent = addr;
  });

  /* ---------- Arcade + music: lazy-load only when the section is near the viewport ---------- */
  const arcade = document.getElementById('break');
  if (arcade) {
    let loaded = false;
    const load = () => {
      if (loaded) return; loaded = true;
      ['/assets/js/arcade.js?v=9', '/assets/js/music.js?v=9'].forEach(src => { const sc = document.createElement('script'); sc.src = src; sc.defer = true; document.body.appendChild(sc); });
    };
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { load(); io.disconnect(); } }, { rootMargin: '600px 0px' });
      io.observe(arcade);
    } else load();
    arcade.querySelectorAll('button').forEach(b => b.addEventListener('click', load, { once: true }));
  }

  /* ---------- Footer year ---------- */
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
