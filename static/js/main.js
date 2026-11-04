/**
 * VillAxolote - Lógica Interactiva y Dinámica
 * Incluye: Carrusel Administrable con auto-play y clicks, Filtros de Tienda, Menú Móvil
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Inicialización del Carrusel
  initCarousel();

  // 2. Filtros de la Tienda
  initShopFilters();

  // 3. Menú Móvil
  initMobileMenu();

  // 4. Efecto de cabecera con Scroll
  initScrollHeader();

  // 5. Cierre de Alertas
  initAlerts();

  // 6. Modo Oscuro / Claro (Botón Flotante)
  initThemeToggle();

  // 7. Fondo Dinámico de Ajolotitos Nadando
  initDynamicAxolotlBg();
});

/* ==========================================================================
   CARRUSEL INTERACTIVO Y AUTOMÁTICO
   ========================================================================== */
function initCarousel() {
  const track = document.getElementById('carouselTrack');
  const slides = document.querySelectorAll('.carousel-slide');
  const prevBtn = document.getElementById('carouselPrev');
  const nextBtn = document.getElementById('carouselNext');
  const dotsContainer = document.getElementById('carouselDots');
  const container = document.querySelector('.carousel-container');

  if (!track || slides.length === 0) return;

  let currentIndex = 0;
  const totalSlides = slides.length;
  const AUTO_PLAY_INTERVAL = 5000; // 5 segundos
  let autoPlayTimer = null;

  // Generar indicadores (dots) dinámicamente si no están en el DOM
  dotsContainer.innerHTML = '';
  slides.forEach((_, idx) => {
    const dot = document.createElement('button');
    dot.className = `carousel-dot ${idx === 0 ? 'active' : ''}`;
    dot.setAttribute('aria-label', `Ir a diapositiva ${idx + 1}`);
    dot.addEventListener('click', () => {
      goToSlide(idx);
      resetAutoPlay();
    });
    dotsContainer.appendChild(dot);
  });

  const dots = document.querySelectorAll('.carousel-dot');

  function updateCarousel() {
    track.style.transform = `translateX(-${currentIndex * 100}%)`;
    dots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx === currentIndex);
    });
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

  // Eventos de botones
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

  // Auto-play (siempre limpia cualquier intervalo previo para evitar timers duplicados)
  let isHovered = false;

  function startAutoPlay() {
    stopAutoPlay();
    if (totalSlides > 1 && !isHovered) {
      autoPlayTimer = setInterval(nextSlide, AUTO_PLAY_INTERVAL);
    }
  }

  function stopAutoPlay() {
    if (autoPlayTimer !== null) {
      clearInterval(autoPlayTimer);
      autoPlayTimer = null;
    }
  }

  function resetAutoPlay() {
    stopAutoPlay();
    if (!isHovered) {
      startAutoPlay();
    }
  }

  // Pausar con hover (solo ratón) para que el usuario pueda leer con calma
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

    // Soporte para gestos táctiles (Swipe en móviles)
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
      handleSwipe();
      resetAutoPlay();
    }, { passive: true });

    function handleSwipe() {
      const threshold = 40;
      if (touchEndX < touchStartX - threshold) {
        nextSlide();
      } else if (touchEndX > touchStartX + threshold) {
        prevSlide();
      }
    }
  }

  // Navegación con teclado accesible
  document.addEventListener('keydown', (e) => {
    if (document.activeElement && document.activeElement.tagName === 'INPUT') return;
    if (e.key === 'ArrowRight') {
      nextSlide();
      resetAutoPlay();
    } else if (e.key === 'ArrowLeft') {
      prevSlide();
      resetAutoPlay();
    }
  });

  // Iniciar auto-play inicial
  startAutoPlay();
}

/* ==========================================================================
   FILTROS DE LA TIENDA
   ========================================================================== */
function initShopFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const productCards = document.querySelectorAll('.product-card');

  if (filterBtns.length === 0 || productCards.length === 0) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      productCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        if (filterValue === 'all' || cardCategory === filterValue) {
          card.style.display = 'flex';
          card.style.animation = 'fadeInUp 0.4s ease forwards';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   MENÚ MÓVIL
   ========================================================================== */
function initMobileMenu() {
  const toggleBtn = document.getElementById('mobileMenuBtn');
  const navLinks = document.getElementById('navLinks');

  if (!toggleBtn || !navLinks) return;

  toggleBtn.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    const isExpanded = navLinks.classList.contains('active');
    toggleBtn.setAttribute('aria-expanded', isExpanded);
    toggleBtn.innerHTML = isExpanded ? '✕' : '☰';
  });

  // Cerrar al hacer clic en un enlace
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('active');
      toggleBtn.innerHTML = '☰';
    });
  });
}

/* ==========================================================================
   EFECTO HEADER SCROLL
   ========================================================================== */
function initScrollHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

/* ==========================================================================
   ALERTAS
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

  // Auto descartar después de 6 segundos
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
   MODO OSCURO / CLARO (BOTÓN FLOTANTE EN LA ESQUINA)
   ========================================================================== */
function initThemeToggle() {
  const toggleBtn = document.getElementById('themeToggleBtn');
  const iconEl = document.getElementById('themeToggleIcon');
  const labelEl = document.getElementById('themeToggleLabel');

  if (!toggleBtn) return;

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem('villaxolote_theme', theme);
    } catch (e) {}

    if (theme === 'dark') {
      if (iconEl) iconEl.textContent = '☀️';
      if (labelEl) labelEl.textContent = 'Modo Claro';
      toggleBtn.classList.add('active');
    } else {
      if (iconEl) iconEl.textContent = '🌙';
      if (labelEl) labelEl.textContent = 'Modo Oscuro';
      toggleBtn.classList.remove('active');
    }
  }

  // Leer estado inicial
  let currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
  try {
    const stored = localStorage.getItem('villaxolote_theme');
    if (stored === 'dark' || stored === 'light') {
      currentTheme = stored;
    }
  } catch (e) {}

  applyTheme(currentTheme);

  toggleBtn.addEventListener('click', () => {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(currentTheme);
  });
}

/* ==========================================================================
   FONDO DINÁMICO DE VARIOS AJOLOTITOS NADANDO
   ========================================================================== */
function initDynamicAxolotlBg() {
  const container = document.getElementById('axolotlBgContainer');
  const toggleBtn = document.getElementById('axolotlBgToggleBtn');
  const labelEl = document.getElementById('axolotlBgLabel');

  if (!container) return;

  // Paletas pastel para distintos ajolotitos
  const palettes = [
    { body: '#ffd6e0', stroke: '#f497b6', gills: '#e76f8a', cheek: '#ff8fab' },
    { body: '#fde2e4', stroke: '#f8a5c2', gills: '#c44569', cheek: '#ffb3c6' },
    { body: '#f3d1f4', stroke: '#d998ed', gills: '#b56576', cheek: '#f78fb3' },
    { body: '#ffe5ec', stroke: '#fbb1bd', gills: '#e66767', cheek: '#ff99ac' }
  ];

  function createCuteAxolotlSVG(palette) {
    return `
      <svg class="bg-axolotl-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180" width="100%" height="100%">
        <!-- Cola nadadora -->
        <g class="axolotl-tail">
          <path d="M90 120 Q90 165 110 172 Q75 162 76 120 Z" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2.5" opacity="0.9"/>
        </g>
        <!-- Cuerpecito y patitas -->
        <ellipse cx="64" cy="118" rx="11" ry="6.5" transform="rotate(-25 64 118)" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2"/>
        <ellipse cx="116" cy="118" rx="11" ry="6.5" transform="rotate(25 116 118)" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2"/>
        <ellipse cx="68" cy="138" rx="10" ry="6" transform="rotate(-15 68 138)" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2"/>
        <ellipse cx="112" cy="138" rx="10" ry="6" transform="rotate(15 112 138)" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2"/>
        <ellipse cx="90" cy="120" rx="25" ry="30" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="2.5"/>
        <!-- Branquias (Gills) -->
        <g class="axolotl-gills">
          <path d="M44 68 C16 52 16 34 40 46 C26 26 44 18 56 38 C56 14 74 20 72 42" fill="${palette.gills}" opacity="0.9"/>
          <path d="M136 68 C164 52 164 34 140 46 C154 26 136 18 124 38 C124 14 106 20 108 42" fill="${palette.gills}" opacity="0.9"/>
        </g>
        <!-- Cabeza -->
        <ellipse cx="90" cy="76" rx="46" ry="36" fill="${palette.body}" stroke="${palette.stroke}" stroke-width="3"/>
        <!-- Mejillas sonrojadas -->
        <circle cx="58" cy="84" r="9" fill="${palette.cheek}" opacity="0.75"/>
        <circle cx="122" cy="84" r="9" fill="${palette.cheek}" opacity="0.75"/>
        <!-- Ojitos brillantes -->
        <circle cx="68" cy="72" r="5.5" fill="#4a192c"/>
        <circle cx="112" cy="72" r="5.5" fill="#4a192c"/>
        <circle cx="66.2" cy="70.2" r="2" fill="#ffffff"/>
        <circle cx="110.2" cy="70.2" r="2" fill="#ffffff"/>
        <!-- Sonrisa tierna -->
        <path d="M81 84 Q90 92 99 84" fill="none" stroke="#4a192c" stroke-width="2.8" stroke-linecap="round"/>
      </svg>
    `;
  }

  // Posiciones distribuidas por la pantalla para que naden armoniosamente
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

  // Crear los ajolotitos
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

  // Crear burbujitas acuáticas flotantes
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

  // Estado activo/inactivo del fondo dinámico
  let isBgActive = true;
  try {
    const savedBg = localStorage.getItem('villaxolote_dynamic_bg');
    if (savedBg === 'off') {
      isBgActive = false;
    }
  } catch (e) {}

  function updateBgState() {
    container.classList.toggle('hidden', !isBgActive);
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
