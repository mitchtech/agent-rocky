const canvas = document.querySelector('#scope');
const ctx = canvas.getContext('2d');
const panel = canvas.closest('.spectrum-panel');
const notesNode = document.querySelector('#notes');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const status = document.querySelector('#audio-status');
const readout = {
  line: document.querySelector('#readout-line'),
  event: document.querySelector('#readout-event'),
  length: document.querySelector('#readout-length'),
};
const player = new Audio();
player.preload = 'auto';
let audioContext;
let analyzer;
let bins;
let activeButton;
let raf = 0;
let lastNotes = 0;

// Codex v2 atlas rows: [row, frames, label, first column].
const STATES = {
  idle: [0, 6, 'idle'], 'moving-right': [1, 8, 'moving right'], 'moving-left': [2, 8, 'moving left'], waving: [3, 4, 'waving'],
  jumping: [4, 5, 'jumping'], failure: [5, 8, 'blocked'], waiting: [6, 6, 'waiting for input'], working: [7, 6, 'working'], review: [8, 6, 'reviewing'],
};
const LOOKS = ['up', 'up-right 1', 'up-right 2', 'up-right 3', 'right', 'down-right 1', 'down-right 2', 'down-right 3',
  'down', 'down-left 1', 'down-left 2', 'down-left 3', 'left', 'up-left 1', 'up-left 2', 'up-left 3'];
LOOKS.forEach((name, direction) => { STATES[`look-${direction}`] = [9 + Math.floor(direction / 8), 1, `looking ${name}`, direction % 8]; });
const stageSprite = document.querySelector('#stage-sprite');
const stateLabel = document.querySelector('#state-label');
const motionButton = document.querySelector('#motion-toggle');
let stageState = 'idle';
let petTimer;
let petPaused = false;
function renderPet() {
  clearInterval(petTimer);
  const [row, count, , start = 0] = STATES[stageState];
  const scale = parseFloat(getComputedStyle(stageSprite).getPropertyValue('--scale')) || 1;
  const draw = column => { stageSprite.style.backgroundPosition = `${-column * 192 * scale}px ${-row * 208 * scale}px`; };
  let frame = 0;
  draw(start);
  if (!petPaused && !reducedMotion.matches && !document.hidden && count > 1) {
    petTimer = setInterval(() => { frame = (frame + 1) % count; draw(frame); }, 160);
  }
  motionButton.disabled = reducedMotion.matches;
  motionButton.textContent = reducedMotion.matches ? 'Reduced motion is on' : petPaused ? 'Resume animation' : 'Pause animation';
  motionButton.setAttribute('aria-pressed', String(petPaused || reducedMotion.matches));
}
document.querySelectorAll('[data-state]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-state]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  stageState = button.dataset.state;
  stateLabel.textContent = `Rocky is ${STATES[stageState][2]}`;
  renderPet();
}));
motionButton.addEventListener('click', () => { petPaused = !petPaused; renderPet(); });
reducedMotion.addEventListener('change', renderPet);
document.addEventListener('visibilitychange', renderPet);
new ResizeObserver(renderPet).observe(stageSprite);
renderPet();

// Each cue tints the spectrum: Tau Ceti gold for success, Astrophage red for alarms, xenonite teal for greetings.
const MOODS = {
  session_started: 'greet', prompt_submitted: 'work', annoyed: 'alarm', approval_required: 'question', input_required: 'question',
  ready_for_input: 'hum', turn_completed: 'success', out_of_astrophage: 'alarm', astrophage_low: 'warn', out_of_xenonite: 'warn', error: 'alarm',
  tool_failed: 'alarm', subagent_started: 'greet', context_compacting: 'hum', session_ended: 'hum', 'easter-egg': 'success',
};
const mood = event => (event.includes('destructive') ? 'alarm' : MOODS[event.split(' ')[0]] || 'question');
const color = name => getComputedStyle(panel).getPropertyValue(`--mood-${name}`).trim() || '#ffd58a';

const NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const note = frequency => {
  const midi = Math.round(69 + 12 * Math.log2(frequency / 440));
  return `${NAMES[((midi % 12) + 12) % 12]}${Math.floor(midi / 12) - 1}`;
};

function fit() {
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  const { width, height } = canvas.getBoundingClientRect();
  canvas.width = Math.round(width * ratio);
  canvas.height = Math.round(height * ratio);
}

function backdrop(fade = 1) {
  const { width, height } = canvas;
  ctx.fillStyle = `rgba(6, 8, 13, ${fade})`;
  ctx.fillRect(0, 0, width, height);
  // Faint octave lines, like a lab spectrum analyzer's graticule.
  ctx.strokeStyle = 'rgba(159, 201, 196, 0.08)';
  ctx.lineWidth = 1;
  for (let i = 1; i < 6; i++) {
    const y = (height * i) / 6;
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
    ctx.stroke();
  }
}

// Bars run from 80 Hz to 5 kHz on a log scale, so each octave gets equal width.
const BARS = 56;
const LOW = 80;
const HIGH = 5000;
function bars(levels, tint) {
  const { width, height } = canvas;
  const gap = width / BARS;
  ctx.save();
  ctx.fillStyle = tint;
  ctx.shadowColor = tint;
  ctx.shadowBlur = width / 50;
  levels.forEach((level, index) => {
    const h = Math.max(2, level * height * 0.86);
    const x = index * gap + gap * 0.18;
    ctx.beginPath();
    ctx.roundRect(x, height - h - height * 0.04, gap * 0.64, h, gap * 0.3);
    ctx.fill();
  });
  ctx.restore();
}

function showNotes(list) {
  notesNode.replaceChildren(...list.map(name => Object.assign(document.createElement('span'), { textContent: name })));
}

function idle() {
  cancelAnimationFrame(raf);
  backdrop();
  // Standby: a quiet five-note chord, one bar per side of the carapace.
  const levels = Array.from({ length: BARS }, (_, i) => ([10, 18, 25, 31, 40].includes(i) ? 0.22 : 0.015));
  bars(levels, color('hum'));
  showNotes(['standby']);
}

function live(tint) {
  analyzer.getFloatFrequencyData(bins);
  const nyquist = audioContext.sampleRate / 2;
  const level = frequency => {
    const value = bins[Math.min(bins.length - 1, Math.round((frequency / nyquist) * bins.length))];
    return Math.max(0, Math.min(1, (value + 90) / 70));
  };
  backdrop(0.4);
  bars(Array.from({ length: BARS }, (_, i) => level(LOW * (HIGH / LOW) ** (i / (BARS - 1)))), tint);
  // Label the three strongest spectral peaks a few times a second, so the notes stay readable.
  const now = performance.now();
  if (now - lastNotes > 220) {
    lastNotes = now;
    const peaks = [];
    for (let i = 2; i < bins.length - 1; i++) {
      const frequency = (i / bins.length) * nyquist;
      if (frequency < LOW || frequency > HIGH || bins[i] < -55) continue;
      if (bins[i] > bins[i - 1] && bins[i] >= bins[i + 1]) peaks.push([bins[i], frequency]);
    }
    const names = [...new Set(peaks.sort((a, b) => b[0] - a[0]).map(([, frequency]) => note(frequency)))].slice(0, 3);
    if (names.length) showNotes(names);
  }
  raf = requestAnimationFrame(() => live(tint));
}

// Reduced motion: draw the whole clip's loudness envelope once instead of animating.
async function envelope(url, tint) {
  const buffer = await audioContext.decodeAudioData(await (await fetch(url)).arrayBuffer());
  const channel = buffer.getChannelData(0);
  const step = Math.floor(channel.length / BARS) || 1;
  const levels = Array.from({ length: BARS }, (_, column) => {
    let peak = 0;
    for (let i = column * step; i < (column + 1) * step && i < channel.length; i++) peak = Math.max(peak, Math.abs(channel[i]));
    return peak;
  });
  backdrop();
  bars(levels, tint);
  showNotes(['envelope']);
}

function ensureAudio() {
  if (audioContext) return audioContext.resume();
  audioContext = new AudioContext();
  analyzer = audioContext.createAnalyser();
  analyzer.fftSize = 8192;
  analyzer.smoothingTimeConstant = 0.6;
  bins = new Float32Array(analyzer.frequencyBinCount);
  audioContext.createMediaElementSource(player).connect(analyzer);
  analyzer.connect(audioContext.destination);
  return audioContext.resume();
}

// Demo fuel: each preview burns Astrophage, the tanks refill slowly, and empty tanks get Rocky's verdict.
const BURN = 12;
const fuel = { value: 100, node: document.querySelector('#fuel') };
setInterval(() => {
  if (fuel.value < 100) { fuel.value = Math.min(100, fuel.value + 2); fuel.node.textContent = fuel.value; }
}, 1000);
const BROKE = {"clip": "not-enough", "line": "Not enough. Not enough.", "length": "1.00"};

function burn() {
  const chip = fuel.node.parentElement;
  if (fuel.value < BURN) {
    chip.classList.remove('empty');
    void chip.offsetWidth;
    chip.classList.add('empty');
    return false;
  }
  fuel.value -= BURN;
  fuel.node.textContent = fuel.value;
  chip.dataset.delta = `-${BURN}%`;
  chip.classList.remove('spent');
  void chip.offsetWidth;
  chip.classList.add('spent');
  return true;
}

function settle(message) {
  panel.classList.remove('live', 'annoyed');
  delete panel.dataset.mood;
  activeButton?.classList.remove('playing');
  activeButton = null;
  if (!reducedMotion.matches) idle();
  if (message) status.textContent = message;
}

async function play(source, { free = false } = {}) {
  let { clip, line, event, length } = source.dataset || source;
  if (!free && !burn()) {
    ({ clip, line, length } = BROKE);
    event = 'out_of_astrophage · the demo tanks are empty';
  }
  const button = source instanceof HTMLElement ? source : null;
  activeButton?.classList.remove('playing');
  activeButton = button;
  readout.line.textContent = line;
  readout.event.textContent = event;
  readout.length.textContent = `${length} s`;
  const url = `audio/${clip}.wav`;
  const feeling = mood(event);
  try {
    await ensureAudio();
    player.src = url;
    await player.play();
    if (activeButton !== button) return;
    button?.classList.add('playing');
    panel.classList.add('live');
    panel.dataset.mood = feeling;
    status.textContent = `Playing: ${line}`;
    cancelAnimationFrame(raf);
    if (reducedMotion.matches) await envelope(url, color(feeling));
    else live(color(feeling));
  } catch {
    if (activeButton === button) settle('Playback unavailable. Check your browser audio settings or try agent-rocky preview.');
  }
}

player.addEventListener('ended', () => settle('Preview finished. Question? Pick another line.'));
document.querySelectorAll('[data-clip]').forEach(button => button.addEventListener('click', () => play(button)));

// The spectrum answers like Rocky: questions at first, then the third click inside ten seconds gets an annoyed line.
const WHAT = [["what-problem", "What problem, question?", "1.50"], ["sampler-question", "Astrophage sampler in position, question?", "2.55"], ["who-is-grace-talking-to", "Who is Grace talking to, question?", "1.78"], ["eridian-question", "(Eridian: a fast rising question)", "0.92"], ["yes", "Yes?", "0.55"]];
const ANNOYED = [["room-for-garbage", "Is this room for garbage?", "1.25"], ["hate-mark", "Rocky hate Mark.", "1.33"], ["grace-look-disgust", "Grace look disgust when you eat.", "2.50"], ["this-room-boring", "This room boring.", "1.77"]];
const clicks = [];
let annoyedIndex = 0;
document.querySelector('#spectrum').addEventListener('click', () => {
  const now = Date.now();
  clicks.push(now);
  while (clicks.length && now - clicks[0] > 10000) clicks.shift();
  const annoyed = clicks.length >= 3;
  const [clip, line, length] = annoyed ? ANNOYED[annoyedIndex++ % ANNOYED.length] : WHAT[Math.floor(Math.random() * WHAT.length)];
  play({ clip, line, length, event: annoyed ? 'annoyed · third click inside 10 s' : 'input_required' }, { free: true }).then(() => {
    if (annoyed) panel.classList.add('annoyed');
  });
});

// Command card: twelve hotkeys, one per cue worth hearing first.
const CARD = [["H", "Hello", "session_started", "hello-grace-friend", "Hello, Grace friend.", "0.88"], ["Y", "Yes", "prompt_submitted", "yes", "Yes?", "0.55"], ["F", "Fix", "prompt_submitted", "rocky-fix", "Rocky fix.", "1.15"], ["Q", "Question", "approval_required · any tool", "what-problem", "What problem, question?", "1.50"], ["A", "Amaze", "turn_completed", "amaze-amaze-amaze", "Amaze! Amaze! Amaze!", "1.33"], ["B", "Fist bump", "turn_completed", "fist-my-bump", "Fist my bump.", "1.80"], ["N", "Fuel", "out_of_astrophage", "not-enough", "Not enough. Not enough.", "1.00"], ["T", "Too much", "out_of_xenonite", "too-much", "Too much! Too much! Too much!", "1.00"], ["D", "Danger", "approval_required · destructive", "we-die", "We die. We die. We die.", "2.65"], ["S", "Subagent", "subagent_started", "saves-stars", "Grace Rocky save stars.", "2.70"], ["C", "Compact", "context_compacting", "cant-forget", "Rocky can't forget.", "2.20"], ["G", "Go home", "session_ended", "grace-go-home", "Grace go home.", "5.50"]];
const card = document.querySelector('#command-card');
const hotkeys = new Map();
card.replaceChildren(...CARD.map(([key, label, event, clip, line, length]) => {
  const button = document.createElement('button');
  button.className = 'cmd';
  Object.assign(button.dataset, { clip, line, event, length });
  button.setAttribute('aria-label', `${line} (${event}), hotkey ${key}`);
  button.setAttribute('aria-keyshortcuts', key);
  button.innerHTML = `<b aria-hidden="true">${key}</b><span aria-hidden="true">${label}</span>`;
  button.addEventListener('click', () => play(button));
  hotkeys.set(key.toLowerCase(), button);
  return button;
}));
document.addEventListener('keydown', event => {
  if (event.metaKey || event.ctrlKey || event.altKey || event.repeat) return;
  if (event.target instanceof Element && event.target.closest('input, textarea, select, [contenteditable]')) return;
  const button = hotkeys.get(event.key.toLowerCase());
  if (!button) return;
  event.preventDefault();
  button.focus({ preventScroll: true });
  play(button);
});
document.addEventListener('themechange', () => { if (!panel.classList.contains('live')) idle(); });

new ResizeObserver(() => { fit(); if (!panel.classList.contains('live')) idle(); }).observe(canvas);
fit();
idle();

document.querySelectorAll('[data-install]').forEach(button => button.addEventListener('click', () => {
  const choice = button.dataset.install;
  document.querySelectorAll('[data-install]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  document.querySelector('#sounds-install').hidden = choice === 'pet';
  document.querySelector('#pet-install').hidden = choice === 'sounds';
}));

document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
  const copyStatus = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText(document.getElementById(button.dataset.copy).innerText);
    copyStatus.textContent = 'Commands copied.';
    button.textContent = 'Copied';
    button.classList.add('copied');
    setTimeout(() => { button.textContent = 'Copy'; button.classList.remove('copied'); }, 2000);
  } catch { copyStatus.textContent = 'Clipboard unavailable. Select and copy the commands above.'; }
}));
