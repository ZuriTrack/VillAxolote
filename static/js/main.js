/**
 * VillAxolote - Lógica Interactiva Completa (Stitch Frontend + Django Dinámico)
 * Incluye:
 * 1. Carrusel Hero Dinámico (sin descontrol de intervalos)
 * 2. Mini Reproductor Musical Interactivo (con sintetizador Web Audio real)
 * 3. Filtros de Tienda Oficial y Carrito Interactivo
 * 4. Modo Escenario Nocturno / Modo Pastel Pop sincronizado (Navbar + Botón Flotante)
 * 5. Fondo Dinámico de Ajolotitos Nadando + Burbujas
 */

document.addEventListener('DOMContentLoaded', () => {
  initCarousel();
  initAudioPlayer();
  initShopFilters();
  initShoppingCart();
  initAlerts();
  initThemeToggle();
  initDynamicAxolotlBg();
});

/* ==========================================================================
   1. CARRUSEL HERO INTERACTIVO Y AUTOMÁTICO (Deslizamiento + Barra Progreso)
   ========================================================================== */
function initCarousel() {
  const track = document.getElementById('carouselTrack');
  const slides = document.querySelectorAll('.carousel-slide-item');
  const prevBtn = document.getElementById('carouselPrev');
  const nextBtn = document.getElementById('carouselNext');
  const dotsContainer = document.getElementById('carouselDots');
  const progressBar = document.getElementById('carouselProgressBar');
  const container = document.querySelector('.carousel-container-stitch');

  if (!track || slides.length === 0) return;

  let currentIndex = 0;
  const totalSlides = slides.length;
  const AUTO_PLAY_INTERVAL = 5000;
  let autoPlayTimer = null;
  let isHovered = false;

  if (dotsContainer) {
    dotsContainer.innerHTML = '';
    slides.forEach((_, idx) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = idx === 0
        ? 'h-3 w-10 rounded-full bg-gradient-to-r from-primary-container to-[#ff4d79] transition-all duration-300 shadow-[0_0_12px_rgba(231,111,138,0.8)]'
        : 'h-3 w-3 rounded-full bg-white/40 hover:bg-white/75 transition-all duration-300';
      dot.setAttribute('aria-label', `Ir a diapositiva ${idx + 1}`);
      dot.addEventListener('click', () => {
        goToSlide(idx);
        resetAutoPlay();
      });
      dotsContainer.appendChild(dot);
    });
  }

  function animateProgressBar() {
    if (!progressBar || totalSlides <= 1) return;
    progressBar.style.transition = 'none';
    progressBar.style.width = '0%';
    // Forzar reflow para reiniciar transición limpia
    void progressBar.offsetWidth;
    if (!isHovered) {
      progressBar.style.transition = `width ${AUTO_PLAY_INTERVAL}ms linear`;
      progressBar.style.width = '100%';
    }
  }

  function updateCarousel() {
    track.style.transform = `translateX(-${currentIndex * 100}%)`;

    slides.forEach((slide, idx) => {
      slide.classList.toggle('is-active', idx === currentIndex);
    });

    if (dotsContainer) {
      const dots = dotsContainer.querySelectorAll('button');
      dots.forEach((dot, idx) => {
        dot.className = idx === currentIndex
          ? 'h-3 w-10 rounded-full bg-gradient-to-r from-primary-container to-[#ff4d79] transition-all duration-300 shadow-[0_0_12px_rgba(231,111,138,0.8)]'
          : 'h-3 w-3 rounded-full bg-white/40 hover:bg-white/75 transition-all duration-300';
      });
    }

    animateProgressBar();
  }

  function nextSlide() {
    currentIndex = (currentIndex + 1) % totalSlides;
    updateCarousel();
  }

  function prevSlide() {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    updateCarousel();
  }

  function goToSlide(index) {
    currentIndex = index;
    updateCarousel();
  }

  function stopAutoPlay() {
    if (autoPlayTimer !== null) {
      clearInterval(autoPlayTimer);
      autoPlayTimer = null;
    }
    if (progressBar) {
      progressBar.style.transition = 'none';
      progressBar.style.width = '0%';
    }
  }

  function startAutoPlay() {
    stopAutoPlay();
    if (totalSlides > 1 && !isHovered) {
      animateProgressBar();
      autoPlayTimer = setInterval(nextSlide, AUTO_PLAY_INTERVAL);
    }
  }

  function resetAutoPlay() {
    stopAutoPlay();
    if (!isHovered) {
      startAutoPlay();
    }
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      nextSlide();
      resetAutoPlay();
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      prevSlide();
      resetAutoPlay();
    });
  }

  if (container) {
    container.addEventListener('pointerenter', (e) => {
      if (e.pointerType === 'mouse') {
        isHovered = true;
        stopAutoPlay();
      }
    });

    container.addEventListener('pointerleave', (e) => {
      if (e.pointerType === 'mouse') {
        isHovered = false;
        startAutoPlay();
      }
    });

    // Soporte táctil Swipe en móviles
    let touchStartX = 0;
    let touchEndX = 0;
    let isSwiping = false;

    container.addEventListener('touchstart', (e) => {
      if (e.target.closest('button, a')) return;
      touchStartX = e.changedTouches[0].screenX;
      isSwiping = true;
      stopAutoPlay();
    }, { passive: true });

    container.addEventListener('touchend', (e) => {
      if (!isSwiping) return;
      isSwiping = false;
      touchEndX = e.changedTouches[0].screenX;
      const threshold = 40;
      if (touchEndX < touchStartX - threshold) {
        nextSlide();
      } else if (touchEndX > touchStartX + threshold) {
        prevSlide();
      }
      resetAutoPlay();
    }, { passive: true });
  }

  // Navegación con flechas del teclado
  document.addEventListener('keydown', (e) => {
    if (document.activeElement && ['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
    if (e.key === 'ArrowRight') {
      nextSlide();
      resetAutoPlay();
    } else if (e.key === 'ArrowLeft') {
      prevSlide();
      resetAutoPlay();
    }
  });

  startAutoPlay();
}

/* ==========================================================================
   2. MINI REPRODUCTOR DE AUDIO INTERACTIVO (Con Sintetizador Dream-Pop)
   ========================================================================== */
function initAudioPlayer() {
  const playBtn = document.getElementById('player-toggle-btn');
  const playIcon = document.getElementById('player-icon');
  const statusBadge = document.getElementById('player-status-badge');
  const trackNameEl = document.getElementById('player-track-name');
  const currentTimeEl = document.getElementById('track-current-time');
  const totalTimeEl = document.getElementById('track-total-time');
  const progressFill = document.getElementById('player-progress-fill');
  const progressBar = document.getElementById('player-progress-bar');
  const trackButtons = document.querySelectorAll('.track-btn');
  const playTriggers = document.querySelectorAll('.play-single-trigger');
  const waveBars = document.querySelectorAll('[class*="wave-bar-"]');

  if (!playBtn) return;

  let isPlaying = false;
  let elapsedSeconds = 0;
  let totalSeconds = 204; // 03:24
  let progressTimer = null;
  let synthTimer = null;
  let audioCtx = null;
  let noteStep = 0;

  // Acordes dream-pop / synth-wave para cada pista
  const trackMelodies = [
    [523.25, 659.25, 783.99, 987.77, 783.99, 659.25], // Cmaj7
    [440.00, 554.37, 659.25, 880.00, 659.25, 554.37], // Amaj
    [349.23, 440.00, 523.25, 659.25, 587.33, 523.25], // Fmaj7
    [392.00, 493.88, 587.33, 783.99, 659.25, 587.33]  // G6
  ];
  let currentTrackIdx = 0;

  function setWavesRunning(running) {
    waveBars.forEach(bar => {
      bar.style.animationPlayState = running ? 'running' : 'paused';
    });
  }

  // Inicialmente en pausa hasta que el usuario interactúe
  setWavesRunning(false);

  function formatTime(sec) {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }

  function playSynthNote() {
    try {
      if (!audioCtx) {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (!AudioContextClass) return;
        audioCtx = new AudioContextClass();
      }
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      const melody = trackMelodies[currentTrackIdx % trackMelodies.length];
      const freq = melody[noteStep % melody.length];
      noteStep++;

      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

      gain.gain.setValueAtTime(0.001, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.06, audioCtx.currentTime + 0.04);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.42);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.45);
    } catch (e) {}
  }

  function startPlayback() {
    isPlaying = true;
    if (playIcon) playIcon.textContent = 'pause';
    if (statusBadge) statusBadge.textContent = 'En Reproducción 🎵';
    setWavesRunning(true);

    clearInterval(progressTimer);
    progressTimer = setInterval(() => {
      elapsedSeconds = (elapsedSeconds + 1) % totalSeconds;
      if (currentTimeEl) currentTimeEl.textContent = formatTime(elapsedSeconds);
      if (progressFill) {
        const pct = Math.min(100, Math.round((elapsedSeconds / totalSeconds) * 100));
        progressFill.style.width = `${pct}%`;
      }
    }, 1000);

    clearInterval(synthTimer);
    playSynthNote();
    synthTimer = setInterval(playSynthNote, 460);
  }

  function pausePlayback() {
    isPlaying = false;
    if (playIcon) playIcon.textContent = 'play_arrow';
    if (statusBadge) statusBadge.textContent = 'En Pausa';
    setWavesRunning(false);
    clearInterval(progressTimer);
    clearInterval(synthTimer);
  }

  function togglePlayback() {
    if (isPlaying) {
      pausePlayback();
    } else {
      startPlayback();
    }
  }

  playBtn.addEventListener('click', togglePlayback);

  playTriggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      if (!isPlaying) startPlayback();
      const rep = document.getElementById('reproductor');
      if (rep) rep.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

  if (progressBar) {
    progressBar.addEventListener('click', (e) => {
      const rect = progressBar.getBoundingClientRect();
      const clickRatio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      elapsedSeconds = Math.floor(clickRatio * totalSeconds);
      if (currentTimeEl) currentTimeEl.textContent = formatTime(elapsedSeconds);
      if (progressFill) progressFill.style.width = `${Math.round(clickRatio * 100)}%`;
    });
  }

  trackButtons.forEach((btn, idx) => {
    btn.addEventListener('click', () => {
      currentTrackIdx = idx;
      noteStep = 0;
      elapsedSeconds = 0;
      const selected = btn.getAttribute('data-track');
      const dur = btn.getAttribute('data-duration') || '03:24';
      if (trackNameEl) trackNameEl.textContent = selected;
      if (totalTimeEl) totalTimeEl.textContent = dur;
      if (currentTimeEl) currentTimeEl.textContent = '00:00';
      if (progressFill) progressFill.style.width = '5%';

      trackButtons.forEach(b => {
        b.className = 'track-btn px-2.5 py-1 rounded-full bg-white/10 hover:bg-white/20 text-white shrink-0 transition-all text-xs';
      });
      btn.className = 'track-btn px-2.5 py-1 rounded-full bg-primary-container text-white font-bold shrink-0 transition-all text-xs';

      startPlayback();
    });
  });
}

/* ==========================================================================
   3. FILTROS DE LA TIENDA OFICIAL (Stitch Pills + Categorías Django)
   ========================================================================== */
function initShopFilters() {
  const filterButtons = document.querySelectorAll('.store-filter-btn');
  const productCards = document.querySelectorAll('.product-card-stitch');

  if (filterButtons.length === 0 || productCards.length === 0) return;

  filterButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const filter = btn.getAttribute('data-filter');

      filterButtons.forEach((b) => {
        b.classList.remove('bg-primary-container', 'text-on-primary', 'font-bold', 'shadow-md');
        b.classList.add('bg-surface-container', 'dark:bg-inverse-surface', 'text-on-surface-variant', 'dark:text-surface-container-high');
      });

      btn.classList.remove('bg-surface-container', 'dark:bg-inverse-surface', 'text-on-surface-variant', 'dark:text-surface-container-high');
      btn.classList.add('bg-primary-container', 'text-on-primary', 'font-bold', 'shadow-md');

      productCards.forEach((card) => {
        const category = card.getAttribute('data-category');
        if (filter === 'all' || category === filter) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   4. CARRITO DE COMPRAS INTERACTIVO CON NOTIFICACIÓN TOAST
   ========================================================================== */
function initShoppingCart() {
  const cartBadge = document.getElementById('cart-count-badge');
  const addButtons = document.querySelectorAll('.add-to-cart-btn');

  let cartCount = 0;
  try {
    cartCount = parseInt(localStorage.getItem('villaxolote_cart_count') || '0', 10) || 0;
  } catch (e) {}

  if (cartBadge) cartBadge.textContent = String(cartCount);

  function showToast(message) {
    const existing = document.getElementById('villaxolote-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.id = 'villaxolote-toast';
    toast.className = 'fixed bottom-24 left-6 z-[1300] bg-primary text-white px-5 py-3 rounded-2xl shadow-2xl border border-white/20 flex items-center gap-2.5 text-sm font-bold transition-all duration-300';
    toast.innerHTML = `<span class="material-symbols-outlined text-lg">shopping_bag</span><span>${message}</span>`;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  addButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const name = btn.getAttribute('data-name') || 'Artículo';
      const price = btn.getAttribute('data-price') || '';
      cartCount++;
      if (cartBadge) cartBadge.textContent = String(cartCount);
      try {
        localStorage.setItem('villaxolote_cart_count', String(cartCount));
      } catch (e) {}
      showToast(`¡"${name}" ($${price}) agregado a tu bolsa! (${cartCount} en carrito)`);
    });
  });
}

/* ==========================================================================
   5. CIERRE DE ALERTAS DJANGO
   ========================================================================== */
function initAlerts() {
  const closeBtns = document.querySelectorAll('.alert-close');
  closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const alert = btn.closest('.alert');
      if (alert) {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        alert.style.transition = 'all 0.3s ease';
        setTimeout(() => alert.remove(), 300);
      }
    });
  });

  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      if (alert && alert.parentElement) {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        alert.style.transition = 'all 0.4s ease';
        setTimeout(() => alert.remove(), 400);
      }
    }, 6000);
  });
}

/* ==========================================================================
   6. MODO ESCENARIO NOCTURNO / MODO PASTEL POP (Sincronizado Navbar + Esquina)
   ========================================================================== */
function initThemeToggle() {
  const cornerBtn = document.getElementById('themeToggleBtn');
  const cornerIcon = document.getElementById('themeToggleIcon');
  const cornerLabel = document.getElementById('themeToggleLabel');

  const navBtn = document.getElementById('theme-stage-toggle');
  const navIcon = document.getElementById('theme-icon');
  const navLabel = document.getElementById('theme-label');

  function applyTheme(theme) {
    const isDark = theme === 'dark';
    document.documentElement.classList.toggle('dark', isDark);
    document.documentElement.setAttribute('data-theme', theme);

    try {
      localStorage.setItem('villaxolote_theme', theme);
    } catch (e) {}

    if (isDark) {
      if (cornerIcon) cornerIcon.textContent = '☀️';
      if (cornerLabel) cornerLabel.textContent = 'Modo Claro';
      if (cornerBtn) cornerBtn.classList.add('active');

      if (navIcon) navIcon.textContent = 'light_mode';
      if (navLabel) navLabel.textContent = '☀️ Modo Pastel Pop';
    } else {
      if (cornerIcon) cornerIcon.textContent = '🌙';
      if (cornerLabel) cornerLabel.textContent = 'Modo Oscuro';
      if (cornerBtn) cornerBtn.classList.remove('active');

      if (navIcon) navIcon.textContent = 'dark_mode';
      if (navLabel) navLabel.textContent = '🌙 Modo Escenario Nocturno';
    }
  }

  let currentTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  try {
    const stored = localStorage.getItem('villaxolote_theme');
    if (stored === 'dark' || stored === 'light') {
      currentTheme = stored;
    }
  } catch (e) {}

  applyTheme(currentTheme);

  function toggleTheme() {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(currentTheme);
  }

  if (cornerBtn) cornerBtn.addEventListener('click', toggleTheme);
  if (navBtn) navBtn.addEventListener('click', toggleTheme);
}

/* ==========================================================================
   7. FONDO DINÁMICO DE VARIOS AJOLOTITOS NADANDO
   ========================================================================== */
function initDynamicAxolotlBg() {
  const container = document.getElementById('axolotlBgContainer');
  const stitchBackdrop = document.getElementById('axolotl-canvas-layer');
  const toggleBtn = document.getElementById('axolotlBgToggleBtn');
  const labelEl = document.getElementById('axolotlBgLabel');

  if (!container) return;

  const palettes = [
    { body: '#ffd6e0', stroke: '#f497b6', gills: '#e76f8a', cheek: '#ff8fab' },
    { body: '#fde2e4', stroke: '#f8a5c2', gills: '#c44569', cheek: '#ffb3c6' },
    { body: '#f3d1f4', stroke: '#d998ed', gills: '#b56576', cheek: '#f78fb3' },
    { body: '#ffe5ec', stroke: '#fbb1bd', gills: '#e66767', cheek: '#ff99ac' }
  ];

  function createCuteAxolotlSVG(palette) {
    return `
      <svg class="bg-axolotl-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180" width="100%" height="100%">
        <g class="axolotl-tail">
          <path d="M90 120 Q90 165 110 172 Q75 162 76 120 Z" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2.5" opacity="0.9"/>
        </g>
        <ellipse cx="64" cy="118" rx="11" ry="6.5" transform="rotate(-25 64 118)" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2"/>
        <ellipse cx="116" cy="118" rx="11" ry="6.5" transform="rotate(25 116 118)" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2"/>
        <ellipse cx="68" cy="138" rx="10" ry="6" transform="rotate(-15 68 138)" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2"/>
        <ellipse cx="112" cy="138" rx="10" ry="6" transform="rotate(15 112 138)" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2"/>
        <ellipse cx="90" cy="120" rx="25" ry="30" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2.5"/>
        <g class="axolotl-gills">
          <path d="M44 68 C16 52 16 34 40 46 C26 26 44 18 56 38 C56 14 74 20 72 42" fill="${palette.gills}" opacity="0.9"/>
          <path d="M136 68 C164 52 164 34 140 46 C154 26 136 18 124 38 C124 14 106 20 108 42" fill="${palette.gills}" opacity="0.9"/>
        </g>
        <ellipse cx="90" cy="76" rx="46" ry="36" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="3"/>
        <circle cx="58" cy="84" r="9" fill="${palette.cheek}" opacity="0.75"/>
        <circle cx="122" cy="84" r="9" fill="${palette.cheek}" opacity="0.75"/>
        <circle cx="68" cy="72" r="5.5" fill="#4a192c"/>
        <circle cx="112" cy="72" r="5.5" fill="#4a192c"/>
        <circle cx="66.2" cy="70.2" r="2" fill="#ffffff"/>
        <circle cx="110.2" cy="70.2" r="2" fill="#ffffff"/>
        <path d="M81 84 Q90 92 99 84" fill="none" stroke="#4a192c" stroke-width="2.8" stroke-linecap="round"/>
      </svg>
    `;
  }

  const axolotlConfigs = [
    { top: '7%',  left: '4%',  size: 86,  dxMid: '55px',  dyMid: '30px',  dxEnd: '-25px', dyEnd: '45px',  dur: '22s', delay: '0s',    flip: 1 },
    { top: '14%', left: '86%', size: 95,  dxMid: '-60px', dyMid: '35px',  dxEnd: '20px',  dyEnd: '-30px', dur: '26s', delay: '-4s',   flip: -1 },
    { top: '32%', left: '10%', size: 72,  dxMid: '45px',  dyMid: '-40px', dxEnd: '-30px', dyEnd: '25px',  dur: '20s', delay: '-8s',   flip: 1 },
    { top: '44%', left: '88%', size: 80,  dxMid: '-50px', dyMid: '-30px', dxEnd: '25px',  dyEnd: '35px',  dur: '24s', delay: '-2s',   flip: -1 },
    { top: '58%', left: '3%',  size: 92,  dxMid: '65px',  dyMid: '25px',  dxEnd: '-15px', dyEnd: '-35px', dur: '28s', delay: '-11s',  flip: 1 },
    { top: '68%', left: '82%', size: 76,  dxMid: '-45px', dyMid: '40px',  dxEnd: '30px',  dyEnd: '-25px', dur: '21s', delay: '-6s',   flip: -1 },
    { top: '82%', left: '12%', size: 84,  dxMid: '50px',  dyMid: '-35px', dxEnd: '-25px', dyEnd: '20px',  dur: '25s', delay: '-14s',  flip: 1 },
    { top: '86%', left: '72%', size: 68,  dxMid: '-55px', dyMid: '-25px', dxEnd: '35px',  dyEnd: '20px',  dur: '19s', delay: '-9s',   flip: -1 },
    { top: '24%', left: '46%', size: 64,  dxMid: '40px',  dyMid: '30px',  dxEnd: '-40px', dyEnd: '-25px', dur: '27s', delay: '-12s',  flip: 1 },
    { top: '74%', left: '48%', size: 70,  dxMid: '-40px', dyMid: '-30px', dxEnd: '40px',  dyEnd: '30px',  dur: '23s', delay: '-5s',   flip: -1 }
  ];

  container.innerHTML = '';

  axolotlConfigs.forEach((cfg, idx) => {
    const item = document.createElement('div');
    item.className = 'bg-axolotl-item';
    item.style.top = cfg.top;
    item.style.left = cfg.left;
    item.style.width = `${cfg.size}px`;
    item.style.height = `${cfg.size}px`;
    item.style.setProperty('--dx-mid', cfg.dxMid);
    item.style.setProperty('--dy-mid', cfg.dyMid);
    item.style.setProperty('--dx-end', cfg.dxEnd);
    item.style.setProperty('--dy-end', cfg.dyEnd);
    item.style.setProperty('--swim-duration', cfg.dur);
    item.style.setProperty('--swim-delay', cfg.delay);
    item.style.setProperty('--flip', cfg.flip);
    item.style.setProperty('--bob-duration', `${3.8 + (idx % 4) * 0.6}s`);

    const inner = document.createElement('div');
    inner.className = 'bg-axolotl-inner';
    inner.innerHTML = createCuteAxolotlSVG(palettes[idx % palettes.length]);

    item.appendChild(inner);
    container.appendChild(item);
  });

  for (let i = 0; i < 14; i++) {
    const bubble = document.createElement('div');
    bubble.className = 'bg-bubble-item';
    const size = 10 + (i % 5) * 6;
    bubble.style.width = `${size}px`;
    bubble.style.height = `${size}px`;
    bubble.style.left = `${(i * 7.3 + 4) % 96}%`;
    bubble.style.setProperty('--bubble-duration', `${12 + (i % 6) * 3}s`);
    bubble.style.setProperty('--bubble-delay', `-${i * 1.7}s`);
    bubble.style.setProperty('--bubble-drift', `${(i % 2 === 0 ? 1 : -1) * (20 + (i % 4) * 10)}px`);
    container.appendChild(bubble);
  }

  let isBgActive = true;
  try {
    const savedBg = localStorage.getItem('villaxolote_dynamic_bg');
    if (savedBg === 'off') {
      isBgActive = false;
    }
  } catch (e) {}

  function updateBgState() {
    container.classList.toggle('hidden', !isBgActive);
    if (stitchBackdrop) {
      stitchBackdrop.style.opacity = isBgActive ? '0.9' : '0.15';
    }
    if (toggleBtn) {
      toggleBtn.classList.toggle('active', isBgActive);
      toggleBtn.setAttribute('aria-pressed', String(isBgActive));
    }
    if (labelEl) {
      labelEl.textContent = isBgActive ? 'Ajolotitos: ON' : 'Ajolotitos: OFF';
    }
    try {
      localStorage.setItem('villaxolote_dynamic_bg', isBgActive ? 'on' : 'off');
    } catch (e) {}
  }

  updateBgState();

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      isBgActive = !isBgActive;
      updateBgState();
    });
  }
}
