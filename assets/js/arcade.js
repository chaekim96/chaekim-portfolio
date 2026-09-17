/* Arcade: Snake + Galaga. Loaded lazily by main.js. */
(function () {
  const root = document.documentElement;
  /* ---------- Snake ---------- */
  (function snake() {
    const cv = document.getElementById('snake'); if (!cv) return;
    const c = cv.getContext('2d'), N = 20, S = cv.width / N;
    const wrap = cv.parentElement, scoreEl = document.getElementById('game-score'), bestEl = document.getElementById('game-best'), startBtn = document.getElementById('snake-start');
    window.__snake = { stop: () => { clearInterval(timer); timer = null; wrap.classList.remove('is-running'); }, show: () => { bestEl.textContent = best; scoreEl.textContent = score || 0; } };
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


  /* ---------- Galaga-lite ---------- */
  (function galaga() {
    const cv = document.getElementById('galaga'); if (!cv) return;
    const c = cv.getContext('2d'), W = cv.width, H = cv.height;
    const wrap = cv.parentElement, scoreEl = document.getElementById('game-score'), bestEl = document.getElementById('game-best'), startBtn = document.getElementById('galaga-start');
    let best = 0; try { best = +localStorage.getItem('ck-galaga-best') || 0; } catch (e) {}
    let ship, bullets, enemies, ebullets, particles, score, lives, wave, raf = null, last = 0, keys = {}, firing = false, cooldown = 0, formT = 0, running = false, stars;
    const rnd = (a, b) => a + Math.random() * (b - a);
    window.__galaga = { stop: () => { running = false; cancelAnimationFrame(raf); raf = null; wrap.classList.remove('is-running'); }, show: () => { bestEl.textContent = best; scoreEl.textContent = score || 0; } };
    function reset() {
      ship = { x: W / 2, y: H - 34, w: 26, h: 20 }; bullets = []; ebullets = []; particles = []; score = 0; lives = 3; wave = 1;
      stars = Array.from({ length: 60 }, () => ({ x: Math.random() * W, y: Math.random() * H, s: rnd(0.4, 1.6), z: rnd(0.3, 1) }));
      scoreEl.textContent = 0; spawnWave();
    }
    function spawnWave() {
      enemies = [];
      const cols = 8, rows = 4;
      for (let r = 0; r < rows; r++) for (let col = 0; col < cols; col++) {
        enemies.push({ hx: 52 + col * 42, hy: 56 + r * 34, x: -40 - r * 30, y: -30, type: r === 0 ? 2 : r === 1 ? 1 : 0, state: 'enter', t: col * 0.08 + r * 0.4, dive: null, alive: true, wob: Math.random() * 6 });
      }
    }
    function fire() { if (cooldown > 0 || bullets.length > 3) return; bullets.push({ x: ship.x, y: ship.y - 14 }); cooldown = 0.18; }
    function boom(x, y, col, n) { for (let i = 0; i < n; i++) particles.push({ x, y, vx: rnd(-140, 140), vy: rnd(-140, 140), life: rnd(0.3, 0.7), col }); }
    function update(dt) {
      cooldown -= dt; formT += dt;
      // ship
      const spd = 260;
      if (keys.left) ship.x -= spd * dt; if (keys.right) ship.x += spd * dt;
      if (ship.tx != null) ship.x += (ship.tx - ship.x) * Math.min(1, dt * 12);
      ship.x = Math.max(16, Math.min(W - 16, ship.x));
      if (firing || keys.space) fire();
      bullets.forEach(b => b.y -= 520 * dt); bullets = bullets.filter(b => b.y > -10);
      ebullets.forEach(b => { b.y += 200 * dt; }); ebullets = ebullets.filter(b => b.y < H + 10);
      // enemies
      const sway = Math.sin(formT * 1.2) * 18;
      enemies.forEach(e => {
        if (!e.alive) return;
        if (e.state === 'enter') {
          e.t -= dt; if (e.t > 0) return;
          const tx = e.hx + sway, ty = e.hy;
          e.x += (tx - e.x) * Math.min(1, dt * 3); e.y += (ty - e.y) * Math.min(1, dt * 3);
          if (Math.abs(e.x - tx) < 2 && Math.abs(e.y - ty) < 2) e.state = 'form';
        } else if (e.state === 'form') {
          e.x = e.hx + sway; e.y = e.hy + Math.sin(formT * 2 + e.wob) * 3;
          if (Math.random() < (0.0015 + wave * 0.0006) && enemies.filter(z => z.state === 'dive').length < 2) { e.state = 'dive'; e.dive = { t: 0, sx: e.x, dir: Math.random() < 0.5 ? -1 : 1 }; }
          if (Math.random() < 0.0008 * wave) ebullets.push({ x: e.x, y: e.y + 8 });
        } else if (e.state === 'dive') {
          e.dive.t += dt;
          e.y = e.hy + e.dive.t * (150 + wave * 15); e.x = e.dive.sx + Math.sin(e.dive.t * 3) * 70 * e.dive.dir;
          if (Math.random() < 0.02) ebullets.push({ x: e.x, y: e.y + 8 });
          if (e.y > H + 20) { e.state = 'enter'; e.x = e.hx; e.y = -30; e.t = 0.2; }
        }
      });
      // collisions
      bullets.forEach(b => { enemies.forEach(e => { if (e.alive && Math.abs(b.x - e.x) < 12 && Math.abs(b.y - e.y) < 12) { e.alive = false; b.y = -99; score += e.type === 2 ? 150 : e.type === 1 ? 80 : 50; scoreEl.textContent = score; boom(e.x, e.y, e.type === 2 ? '#ffe234' : e.type === 1 ? '#8ea0ff' : '#5dd6c0', 14); } }); });
      const hitShip = (x, y, r) => Math.abs(x - ship.x) < r && Math.abs(y - ship.y) < r;
      let hit = ebullets.some(b => hitShip(b.x, b.y, 12)) || enemies.some(e => e.alive && e.state === 'dive' && hitShip(e.x, e.y, 16));
      if (hit) { ebullets = []; enemies.forEach(e => { if (e.state === 'dive') { e.state = 'enter'; e.x = e.hx; e.y = -30; e.t = 0.4; } }); boom(ship.x, ship.y, '#ff7ab6', 26); lives--; if (lives <= 0) return gameOver(); }
      if (enemies.every(e => !e.alive)) { wave++; spawnWave(); }
      particles.forEach(p => { p.x += p.vx * dt; p.y += p.vy * dt; p.life -= dt; }); particles = particles.filter(p => p.life > 0);
      stars.forEach(st => { st.y += 30 * st.z * dt; if (st.y > H) { st.y = 0; st.x = Math.random() * W; } });
    }
    function drawShip(x, y) {
      c.fillStyle = '#fff'; c.beginPath(); c.moveTo(x, y - 12); c.lineTo(x + 12, y + 10); c.lineTo(x + 4, y + 6); c.lineTo(x, y + 10); c.lineTo(x - 4, y + 6); c.lineTo(x - 12, y + 10); c.closePath(); c.fill();
      c.fillStyle = '#1e5bff'; c.fillRect(x - 2, y - 4, 4, 8);
    }
    function drawEnemy(e) {
      const col = e.type === 2 ? '#ffe234' : e.type === 1 ? '#8ea0ff' : '#5dd6c0';
      c.fillStyle = col; const x = e.x, y = e.y;
      c.fillRect(x - 9, y - 4, 18, 8); c.fillRect(x - 5, y - 8, 10, 4); c.fillRect(x - 12, y - 1, 3, 6); c.fillRect(x + 9, y - 1, 3, 6);
      c.fillStyle = '#0e1120'; c.fillRect(x - 5, y - 2, 3, 3); c.fillRect(x + 2, y - 2, 3, 3);
      c.fillStyle = col; c.fillRect(x - 7, y + 4, 3, 4); c.fillRect(x + 4, y + 4, 3, 4);
    }
    function render() {
      c.fillStyle = '#0e1120'; c.fillRect(0, 0, W, H);
      stars.forEach(st => { c.fillStyle = `rgba(255,255,255,${0.25 + st.z * 0.6})`; c.fillRect(st.x, st.y, st.s, st.s); });
      enemies.forEach(e => { if (e.alive && (e.state !== 'enter' || e.t <= 0)) drawEnemy(e); });
      c.fillStyle = '#ffe234'; bullets.forEach(b => c.fillRect(b.x - 1.5, b.y - 6, 3, 10));
      c.fillStyle = '#ff7ab6'; ebullets.forEach(b => c.fillRect(b.x - 1.5, b.y, 3, 8));
      particles.forEach(p => { c.globalAlpha = Math.max(0, p.life * 1.6); c.fillStyle = p.col; c.fillRect(p.x, p.y, 3, 3); }); c.globalAlpha = 1;
      if (lives > 0) drawShip(ship.x, ship.y);
      for (let i = 0; i < lives - 1; i++) { c.save(); c.translate(16 + i * 22, H - 14); c.scale(0.5, 0.5); drawShip(0, 0); c.restore(); }
      c.fillStyle = 'rgba(255,255,255,.7)'; c.font = '600 11px Poppins, sans-serif'; c.textAlign = 'right'; c.fillText('WAVE ' + wave, W - 12, H - 10);
    }
    function loop(t) {
      if (!running) return;
      const dt = Math.min(0.033, (t - last) / 1000 || 0.016); last = t;
      update(dt); render(); raf = requestAnimationFrame(loop);
    }
    function gameOver() {
      running = false; cancelAnimationFrame(raf); raf = null; wrap.classList.remove('is-running');
      if (score > best) { best = score; try { localStorage.setItem('ck-galaga-best', best); } catch (e) {} }
      bestEl.textContent = best; startBtn.textContent = `Game over · ${score} — play again`;
      render(); c.fillStyle = 'rgba(14,17,32,.55)'; c.fillRect(0, 0, W, H);
    }
    function start() { reset(); running = true; wrap.classList.add('is-running'); cv.focus(); last = performance.now(); cancelAnimationFrame(raf); raf = requestAnimationFrame(loop); }
    startBtn.addEventListener('click', start);
    cv.addEventListener('keydown', e => {
      const k = e.key.toLowerCase();
      if (['arrowleft', 'a'].includes(k)) { keys.left = true; e.preventDefault(); }
      if (['arrowright', 'd'].includes(k)) { keys.right = true; e.preventDefault(); }
      if (k === ' ' || k === 'arrowup' || k === 'w') { keys.space = true; e.preventDefault(); if (!running) start(); }
    });
    cv.addEventListener('keyup', e => { const k = e.key.toLowerCase(); if (['arrowleft', 'a'].includes(k)) keys.left = false; if (['arrowright', 'd'].includes(k)) keys.right = false; if (k === ' ' || k === 'arrowup' || k === 'w') keys.space = false; });
    const toX = e => (e.clientX - cv.getBoundingClientRect().left) * (W / cv.getBoundingClientRect().width);
    cv.addEventListener('pointerdown', e => { if (!running) return; ship.tx = toX(e); firing = true; cv.setPointerCapture(e.pointerId); });
    cv.addEventListener('pointermove', e => { if (running && firing) ship.tx = toX(e); });
    cv.addEventListener('pointerup', () => { firing = false; ship.tx = null; });
    cv.addEventListener('pointercancel', () => { firing = false; ship.tx = null; });
    reset(); render(); bestEl.textContent = best;
  })();

  /* ---------- Game tabs ---------- */
  document.querySelectorAll('.gametab').forEach(tab => {
    tab.addEventListener('click', () => {
      const g = tab.dataset.game;
      document.querySelectorAll('.gametab').forEach(t => { t.classList.toggle('is-active', t === tab); t.setAttribute('aria-selected', String(t === tab)); });
      document.querySelectorAll('.game').forEach(el => el.classList.toggle('is-hidden', el.dataset.game !== g));
      (g === 'snake' ? window.__galaga : window.__snake)?.stop();
      (g === 'snake' ? window.__snake : window.__galaga)?.show();
    });
  });

})();
