/**
 * KUPOLLA — Model Page JS
 * Gallery slider logic + scroll reveal
 */

document.addEventListener('DOMContentLoaded', () => {
  initSlider();
  initModelForms();
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

/* ─── MODEL FORM SUBMISSION ─── */
function initModelForms() {
  const form = document.getElementById('modelInquiryForm');
  if (!form) return;
  form.addEventListener('submit', handleSubmit);

  form.querySelectorAll('.kp-form__inp, .kp-form__ta').forEach(field => {
    field.addEventListener('blur',  () => validateField(field));
    field.addEventListener('input', () => {
      if (field.classList.contains('err')) validateField(field);
    });
  });
}

function validateField(field) {
  const val  = field.value.trim();
  const type = field.type;
  let ok = true;
  if (field.hasAttribute('required') && !val) ok = false;
  else if (type === 'email' && val) ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
  else if (type === 'tel' && val)   ok = /^[+\d\s\-()\u00A0]{7,22}$/.test(val);
  field.classList.toggle('err', !ok);
  return ok;
}

function handleSubmit(e) {
  e.preventDefault();
  const form = e.target;
  let valid = true;

  form.querySelectorAll('.kp-form__inp, .kp-form__ta').forEach(f => {
    if (!validateField(f)) valid = false;
  });

  const gdpr = form.querySelector('input[name="gdpr"]');
  if (gdpr && !gdpr.checked) {
    valid = false;
    gdpr.closest('.kp-checkbox')?.classList.add('err');
  }

  if (!valid) { form.querySelector('.err')?.focus?.(); return; }

  const btn  = form.querySelector('[type="submit"]');
  const orig = btn.innerHTML;
  btn.disabled = true;
  btn.textContent = 'Надсилається…';

  setTimeout(() => {
    btn.textContent = '✓ Заявку надіслано!';
    btn.style.background = '#2a5040';
    setTimeout(() => {
      form.reset();
      btn.disabled = false;
      btn.innerHTML = orig;
      btn.style.background = '';
      if (form.closest('.kp-modal')) closeConsultModal?.();
    }, 2500);
  }, 1000);
}
