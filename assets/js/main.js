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

  /* ---------- Snake ---------- */
  (function snake() {
    const cv = document.getElementById('snake'); if (!cv) return;
    const c = cv.getContext('2d'), N = 20, S = cv.width / N;
    const wrap = cv.parentElement, scoreEl = document.getElementById('snake-score'), bestEl = document.getElementById('snake-best'), startBtn = document.getElementById('snake-start');
    let snake, dir, nextDir, food, score, best = 0, timer = null, speed, waiting = false;
    try { best = +localStorage.getItem('ck-snake-best') || 0; } catch (e) {}
    bestEl.textContent = best;
    const acc = () => getComputedStyle(root).getPropertyValue('--accent').trim() || '#1e5bff';
    function reset() {
      snake = [{ x: 9, y: 10 }, { x: 8, y: 10 }, { x: 7, y: 10 }]; dir = { x: 1, y: 0 }; nextDir = dir; score = 0; speed = 140;
      scoreEl.textContent = 0; placeFood(); render();
    }
    function placeFood() {
      do { food = { x: Math.floor(Math.random() * N), y: Math.floor(Math.random() * N) }; }
      while (snake.some(p => p.x === food.x && p.y === food.y));
    }
    function step() {
      if (waiting) return;
      dir = nextDir;
      const head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };
      if (head.x < 0 || head.y < 0 || head.x >= N || head.y >= N || snake.some(p => p.x === head.x && p.y === head.y)) return gameOver();
      snake.unshift(head);
      if (head.x === food.x && head.y === food.y) {
        score++; scoreEl.textContent = score; placeFood();
        if (score % 4 === 0 && speed > 70) { speed -= 8; clearInterval(timer); timer = setInterval(step, speed); }
      } else snake.pop();
      render();
    }
    function render() {
      c.clearRect(0, 0, cv.width, cv.height);
      c.fillStyle = 'rgba(30,91,255,.06)';
      for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) if ((i + j) % 2) c.fillRect(i * S, j * S, S, S);
      // food
      c.fillStyle = '#ffe234'; c.strokeStyle = '#101223'; c.lineWidth = 2;
      c.beginPath(); c.arc(food.x * S + S / 2, food.y * S + S / 2, S * 0.34, 0, Math.PI * 2); c.fill(); c.stroke();
      // snake
      snake.forEach((p, i) => {
        c.fillStyle = i === 0 ? '#101223' : acc();
        const r = S * 0.28; const x = p.x * S + 2, y = p.y * S + 2, sz = S - 4;
        c.beginPath(); c.roundRect(x, y, sz, sz, r); c.fill();
        if (i === 0) { c.fillStyle = '#fff'; const ex = dir.x, ey = dir.y; c.beginPath(); c.arc(x + sz / 2 + ex * 4 - ey * 4, y + sz / 2 + ey * 4 + ex * 4, 2.2, 0, 7); c.arc(x + sz / 2 + ex * 4 + ey * 4, y + sz / 2 + ey * 4 - ex * 4, 2.2, 0, 7); c.fill(); }
      });
    }
    function gameOver() {
      clearInterval(timer); timer = null; wrap.classList.remove('is-running');
      if (score > best) { best = score; bestEl.textContent = best; try { localStorage.setItem('ck-snake-best', best); } catch (e) {} }
      startBtn.textContent = `Game over · ${score} — play again`;
      c.fillStyle = 'rgba(255,255,255,.55)'; c.fillRect(0, 0, cv.width, cv.height);
    }
    function start() { reset(); waiting = true; wrap.classList.add('is-running'); cv.focus(); clearInterval(timer); timer = setInterval(step, speed); drawHint(); }
    function drawHint() { c.fillStyle = 'rgba(16,18,35,.55)'; c.font = '600 13px Poppins, sans-serif'; c.textAlign = 'center'; c.fillText('Press a direction to start', cv.width / 2, cv.height * 0.32); }
    function turn(x, y) { if (x === -dir.x && y === -dir.y) return; waiting = false; if (x === dir.x && y === dir.y) return; nextDir = { x, y }; }
    startBtn.addEventListener('click', start);
    cv.addEventListener('keydown', e => {
      const k = e.key.toLowerCase();
      const m = { arrowup: [0, -1], w: [0, -1], arrowdown: [0, 1], s: [0, 1], arrowleft: [-1, 0], a: [-1, 0], arrowright: [1, 0], d: [1, 0] }[k];
      if (m) { e.preventDefault(); if (!timer) start(); turn(m[0], m[1]); }
      if (k === ' ' && !timer) { e.preventDefault(); start(); }
    });
    // swipe
    let sx, sy;
    cv.addEventListener('pointerdown', e => { sx = e.clientX; sy = e.clientY; });
    cv.addEventListener('pointerup', e => {
      if (sx == null) return; const dx = e.clientX - sx, dy = e.clientY - sy; sx = sy = null;
      if (Math.abs(dx) < 18 && Math.abs(dy) < 18) { if (!timer) start(); return; }
      if (!timer) start();
      Math.abs(dx) > Math.abs(dy) ? turn(Math.sign(dx), 0) : turn(0, Math.sign(dy));
    });
    document.querySelectorAll('.snake__dpad button').forEach(b => b.addEventListener('click', () => { const [x, y] = b.dataset.dir.split(',').map(Number); if (!timer) start(); turn(x, y); }));
    reset();
  })();

  /* ---------- Music: generative lo-fi via Web Audio (no audio files) ---------- */
  (function music() {
    const panel = document.getElementById('music-panel'); if (!panel) return;
    const playBtn = document.getElementById('music-play'), prevBtn = document.getElementById('music-prev'), nextBtn = document.getElementById('music-next');
    const vol = document.getElementById('music-vol'), title = document.getElementById('music-title'), list = document.getElementById('music-list'), viz = document.getElementById('music-viz');
    const TRACKS = [
      { name: 'Cloud Nine', bpm: 72, root: 60, scale: [0, 2, 4, 7, 9], mood: 'lo-fi · warm', chords: [[0, 4, 7, 11], [5, 9, 12, 16], [2, 5, 9, 12], [7, 11, 14, 17]] },
      { name: 'Golden Hour', bpm: 84, root: 62, scale: [0, 2, 3, 5, 7, 9], mood: 'dorian · bright', chords: [[0, 3, 7, 10], [5, 9, 12, 15], [3, 7, 10, 14], [10, 14, 17, 21]] },
      { name: 'Late Study', bpm: 64, root: 57, scale: [0, 3, 5, 7, 10], mood: 'minor · slow', chords: [[0, 3, 7, 10], [8, 12, 15, 19], [5, 8, 12, 15], [3, 7, 10, 14]] }
    ];
    let ac, master, analyser, comp, delay, cur = 0, playing = false, nextTime = 0, beat = 0, lookahead, lastMel = 0;
    const mtof = m => 440 * Math.pow(2, (m - 69) / 12);
    function ensure() {
      if (ac) return;
      ac = new (window.AudioContext || window.webkitAudioContext)();
      master = ac.createGain(); master.gain.value = +vol.value;
      comp = ac.createDynamicsCompressor(); comp.threshold.value = -18; comp.ratio.value = 3;
      analyser = ac.createAnalyser(); analyser.fftSize = 128;
      delay = ac.createDelay(1.0); const fb = ac.createGain(); fb.gain.value = 0.32; const dfilt = ac.createBiquadFilter(); dfilt.type = 'lowpass'; dfilt.frequency.value = 1800;
      delay.connect(dfilt).connect(fb).connect(delay); const wet = ac.createGain(); wet.gain.value = 0.35; delay.connect(wet).connect(comp);
      master.connect(comp); comp.connect(analyser); analyser.connect(ac.destination);
      master.delaySend = ac.createGain(); master.delaySend.gain.value = 1; master.delaySend.connect(delay);
      // vinyl-ish noise bed
      const buf = ac.createBuffer(1, ac.sampleRate * 2, ac.sampleRate); const d = buf.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * 0.6;
      const noise = ac.createBufferSource(); noise.buffer = buf; noise.loop = true; const nf = ac.createBiquadFilter(); nf.type = 'bandpass'; nf.frequency.value = 900; nf.Q.value = 0.5;
      const ng = ac.createGain(); ng.gain.value = 0.012; noise.connect(nf).connect(ng).connect(master); noise.start();
    }
    function tone(freq, t, dur, type, gain, dest, detune) {
      const o = ac.createOscillator(), g = ac.createGain(); o.type = type; o.frequency.value = freq; if (detune) o.detune.value = detune;
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(gain, t + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g).connect(dest); o.start(t); o.stop(t + dur + 0.05);
    }
    function kick(t) { const o = ac.createOscillator(), g = ac.createGain(); o.frequency.setValueAtTime(140, t); o.frequency.exponentialRampToValueAtTime(42, t + 0.12); g.gain.setValueAtTime(0.5, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.28); o.connect(g).connect(master); o.start(t); o.stop(t + 0.3); }
    function hat(t, open) { const b = ac.createBuffer(1, ac.sampleRate * 0.1, ac.sampleRate), d = b.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; const s = ac.createBufferSource(); s.buffer = b; const f = ac.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = 7000; const g = ac.createGain(); g.gain.setValueAtTime(open ? 0.08 : 0.05, t); g.gain.exponentialRampToValueAtTime(0.001, t + (open ? 0.18 : 0.05)); s.connect(f).connect(g).connect(master); s.start(t); }
    function schedule() {
      const tr = TRACKS[cur], spb = 60 / tr.bpm; // seconds per beat (16 beats per chord cycle of 4 bars)
      while (nextTime < ac.currentTime + 0.25) {
        const bar = Math.floor(beat / 4) % 4, b = beat % 4, sub = beat; const chord = tr.chords[bar];
        // pad on bar start
        if (b === 0) chord.forEach((n, i) => { const f = mtof(tr.root + n); tone(f, nextTime, spb * 4.2, 'triangle', 0.045, master, i % 2 ? 6 : -6); tone(f / 2, nextTime, spb * 4.2, 'sine', 0.03, master); });
        // bass on 1 and 3
        if (b === 0 || b === 2) tone(mtof(tr.root + chord[0] - 12), nextTime, spb * 1.6, 'sine', 0.22, master);
        // drums: laid-back
        if (b === 0 || b === 2) kick(nextTime + (b === 2 ? 0.012 : 0)); 
        hat(nextTime, false); hat(nextTime + spb / 2, b === 3);
        if (b === 1 || b === 3) { const sn = ac.createBuffer(1, ac.sampleRate * 0.12, ac.sampleRate), d = sn.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length); const s = ac.createBufferSource(); s.buffer = sn; const g = ac.createGain(); g.gain.value = 0.10; const f = ac.createBiquadFilter(); f.type = 'bandpass'; f.frequency.value = 1800; s.connect(f).connect(g).connect(master); s.start(nextTime + 0.01); }
        // melody: random walk on the scale, sparse, with echo
        for (let k = 0; k < 2; k++) {
          if (Math.random() < 0.55) {
            lastMel = Math.max(-2, Math.min(9, lastMel + [-2, -1, -1, 0, 1, 1, 2][Math.floor(Math.random() * 7)]));
            const deg = ((lastMel % tr.scale.length) + tr.scale.length) % tr.scale.length, oct = Math.floor(lastMel / tr.scale.length);
            const f = mtof(tr.root + 12 + oct * 12 + tr.scale[deg]);
            const t = nextTime + k * spb / 2 + (Math.random() * 0.02);
            tone(f, t, spb * 0.9, 'triangle', 0.09, master); tone(f, t, spb * 0.9, 'triangle', 0.05, master.delaySend);
          }
        }
        nextTime += spb; beat++;
      }
    }
    function drawViz() {
      const c = viz.getContext('2d'); const W = viz.width, H = viz.height; c.clearRect(0, 0, W, H);
      const acc = getComputedStyle(root).getPropertyValue('--accent').trim() || '#1e5bff';
      if (analyser && playing) {
        const data = new Uint8Array(analyser.frequencyBinCount); analyser.getByteFrequencyData(data);
        const n = 40, bw = W / n;
        for (let i = 0; i < n; i++) { const v = data[Math.floor(i * data.length / n / 1.6)] / 255; const bh = Math.max(4, v * H * 0.9); c.fillStyle = i % 5 === 0 ? '#ffe234' : acc; c.globalAlpha = 0.35 + v * 0.65; c.beginPath(); c.roundRect(i * bw + 3, H - bh - 6, bw - 6, bh, 4); c.fill(); }
        c.globalAlpha = 1;
      } else {
        c.fillStyle = acc; c.globalAlpha = 0.25; const n = 40, bw = W / n;
        for (let i = 0; i < n; i++) { const bh = 6 + Math.abs(Math.sin(i * 0.7)) * 14; c.beginPath(); c.roundRect(i * bw + 3, H - bh - 6, bw - 6, bh, 4); c.fill(); }
        c.globalAlpha = 1;
      }
      requestAnimationFrame(drawViz);
    }
    function load(i, autoplay) {
      cur = (i + TRACKS.length) % TRACKS.length; title.textContent = TRACKS[cur].name; beat = 0; lastMel = 0;
      [...list.children].forEach((li, j) => li.classList.toggle('is-active', j === cur));
      if (autoplay && ac) { nextTime = ac.currentTime + 0.05; }
    }
    function play() { ensure(); if (ac.state === 'suspended') ac.resume(); playing = true; nextTime = ac.currentTime + 0.05; lookahead = setInterval(schedule, 60); panel.classList.add('is-playing'); panel.classList.remove('is-paused'); playBtn.setAttribute('aria-label', 'Pause'); }
    function pause() { playing = false; clearInterval(lookahead); panel.classList.remove('is-playing'); panel.classList.add('is-paused'); playBtn.setAttribute('aria-label', 'Play'); if (ac) ac.suspend(); }
    playBtn.addEventListener('click', () => playing ? pause() : play());
    prevBtn.addEventListener('click', () => { load(cur - 1, true); });
    nextBtn.addEventListener('click', () => { load(cur + 1, true); });
    vol.addEventListener('input', () => { if (master) master.gain.value = +vol.value; });
    TRACKS.forEach((t, i) => { const li = document.createElement('li'); li.innerHTML = `<span><span class="eq"><i></i><i></i><i></i></span>${t.name}</span><span>${t.mood} · ${t.bpm} bpm</span>`; li.addEventListener('click', () => { load(i, true); if (!playing) play(); }); list.appendChild(li); });
    load(0, false); drawViz();
  })();

  /* ---------- Footer year ---------- */
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
