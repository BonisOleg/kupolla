/**
 * KUPOLLA — Model Page JS
 * Gallery slider. Форма запиту: валідація і HTMX-submit у kupolla.js.
 */

document.addEventListener('DOMContentLoaded', () => {
  initSlider();
});

/* ─── GALLERY SLIDER ─── */
function initSlider() {
  const slider = document.getElementById('modelSlider');
  if (!slider) return;

  const slides = slider.querySelectorAll('.kp-model__slide, .kp-slide');
  if (!slides.length) return;

  const thumbs = document.querySelectorAll('.kp-model__thumb');
  if (thumbs.length) {
    let current = 0;

    function goTo(idx) {
      const next = ((idx % slides.length) + slides.length) % slides.length;
      slides[current]?.classList.remove('active');
      thumbs[current]?.classList.remove('active');
      thumbs[current]?.setAttribute('aria-selected', 'false');
      current = next;
      slides[current]?.classList.add('active');
      thumbs[current]?.classList.add('active');
      thumbs[current]?.setAttribute('aria-selected', 'true');
    }

    thumbs.forEach((thumb, i) => {
      thumb.addEventListener('click', () => goTo(i));
    });
    return;
  }

  const dotsWrap = document.getElementById('sliderDots');
  const prevBtn = document.getElementById('slidePrev');
  const nextBtn = document.getElementById('slideNext');
  if (!dotsWrap) return;

  let current = 0;
  let autoTimer = null;

  slides.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'kp-slider__dot' + (i === 0 ? ' active' : '');
    dot.setAttribute('role', 'tab');
    dot.setAttribute('aria-label', `Слайд ${i + 1}`);
    dot.setAttribute('aria-selected', String(i === 0));
    dot.addEventListener('click', () => goTo(i));
    dotsWrap.appendChild(dot);
  });

  function goTo(idx) {
    slides[current]?.classList.remove('active');
    dotsWrap.children[current]?.classList.remove('active');
    dotsWrap.children[current]?.setAttribute('aria-selected', 'false');

    current = (idx + slides.length) % slides.length;

    slides[current]?.classList.add('active');
    dotsWrap.children[current]?.classList.add('active');
    dotsWrap.children[current]?.setAttribute('aria-selected', 'true');
  }

  function startAuto() {
    stopAuto();
    if (slides.length < 2) return;
    autoTimer = setInterval(() => goTo(current + 1), 5000);
  }

  function stopAuto() {
    if (autoTimer) { clearInterval(autoTimer); autoTimer = null; }
  }

  prevBtn?.addEventListener('click', () => { goTo(current - 1); stopAuto(); });
  nextBtn?.addEventListener('click', () => { goTo(current + 1); stopAuto(); });

  slider.addEventListener('mouseenter', stopAuto);
  slider.addEventListener('mouseleave', startAuto);
  slider.addEventListener('focusin', stopAuto);
  slider.addEventListener('focusout', startAuto);

  let touchX = 0;
  slider.addEventListener('touchstart', e => { touchX = e.touches[0].clientX; }, { passive: true });
  slider.addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 44) { goTo(dx < 0 ? current + 1 : current - 1); stopAuto(); }
  }, { passive: true });

  slider.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') { goTo(current - 1); stopAuto(); }
    if (e.key === 'ArrowRight') { goTo(current + 1); stopAuto(); }
  });

  startAuto();
}
