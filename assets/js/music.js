/* Generative lo-fi player (Web Audio). Loaded lazily by main.js. Never autoplays: audio starts only on a click. */
(function () {
  const root = document.documentElement;
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

})();
