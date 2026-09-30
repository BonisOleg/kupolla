/**
 * KUPOLLA — Main JS
 * Header scroll, burger menu, lang switcher,
 * modal, HTMX form validation, scroll reveal, mobile CTA, GA4 events
 */

document.addEventListener('DOMContentLoaded', () => {
  initHeader();
  initBurger();
  initLang();
  initModalTriggers();
  initReveal();
  initFieldValidation();
  initMobileCta();
  initSmoothScroll();
  initGa4CtaTracking();
  initHeroVideo();
});

/* ─── HEADER ─── */
function initHeader() {
  const header = document.getElementById('header');
  if (!header) return;
  const tick = () => {
    header.classList.toggle('scrolled', window.scrollY > 24);
  };
  window.addEventListener('scroll', tick, { passive: true });
  tick();
}

/* ─── BURGER / MOBILE MENU ─── */
function initBurger() {
  const btn  = document.getElementById('burgerBtn');
  const menu = document.getElementById('mobileMenu');
  if (!btn || !menu) return;

  btn.addEventListener('click', () => {
    menu.classList.contains('open') ? closeMobileMenu() : openMobileMenu();
  });

  menu.querySelectorAll('.kp-mobile-menu__link').forEach(l =>
    l.addEventListener('click', closeMobileMenu)
  );

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeMobileMenu(); closeConsultModal(); }
  });
}

function openMobileMenu() {
  const btn  = document.getElementById('burgerBtn');
  const menu = document.getElementById('mobileMenu');
  btn.classList.add('open');
  btn.setAttribute('aria-expanded', 'true');
  menu.classList.add('open');
  menu.setAttribute('aria-hidden', 'false');
  document.body.classList.add('is-locked');
}

function closeMobileMenu() {
  const btn  = document.getElementById('burgerBtn');
  const menu = document.getElementById('mobileMenu');
  btn.classList.remove('open');
  btn.setAttribute('aria-expanded', 'false');
  menu.classList.remove('open');
  menu.setAttribute('aria-hidden', 'true');
  if (!document.getElementById('consultModal')?.classList.contains('open')) {
    document.body.classList.remove('is-locked');
  }
}

window.closeMobileMenu = closeMobileMenu;

/* ─── LANGUAGE SWITCHER ─── */
function initLang() {
  const wrap    = document.getElementById('langSwitcher');
  const trigger = document.getElementById('langTrigger');
  const current = document.getElementById('currentLang');
  if (!wrap || !trigger) return;

  trigger.addEventListener('click', e => {
    e.stopPropagation();
    const open = wrap.classList.toggle('open');
    trigger.setAttribute('aria-expanded', String(open));
  });

  document.addEventListener('click', e => {
    if (!wrap.contains(e.target)) {
      wrap.classList.remove('open');
      trigger.setAttribute('aria-expanded', 'false');
    }
  });

  wrap.querySelectorAll('.kp-lang__option').forEach(opt => {
    opt.addEventListener('click', () => {
      wrap.classList.remove('open');
      trigger.setAttribute('aria-expanded', 'false');
    });
  });
}

/* ─── MODAL TRIGGERS ─── */
function initModalTriggers() {
  document.addEventListener('click', e => {
    const trigger = e.target.closest('[data-modal-trigger]');
    if (trigger) {
      const name = trigger.getAttribute('data-modal-trigger');
      if (name === 'consult') openConsultModal();
      return;
    }
    const closer = e.target.closest('[data-modal-close]');
    if (closer) {
      const name = closer.getAttribute('data-modal-close');
      if (name === 'consult') closeConsultModal();
    }
  });
}

function openConsultModal() {
  const modal = document.getElementById('consultModal');
  if (!modal) return;
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
  document.body.classList.add('is-locked');
  setTimeout(() => {
    const first = modal.querySelector('input');
    if (first) first.focus();
  }, 120);
  trackGa4('cta_click', { cta_type: 'consult_modal' });
}

function closeConsultModal() {
  const modal = document.getElementById('consultModal');
  if (!modal) return;
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
  const menuOpen = document.getElementById('mobileMenu')?.classList.contains('open');
  if (!menuOpen) document.body.classList.remove('is-locked');
}

window.openConsultModal  = openConsultModal;
window.closeConsultModal = closeConsultModal;

/* ─── SCROLL REVEAL ─── */
function initReveal() {
  const els = document.querySelectorAll('.kp-reveal');
  if (!els.length) return;

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('vis');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -32px 0px' });

  els.forEach(el => obs.observe(el));
}

/* ─── FIELD-LEVEL VALIDATION ─── */
const FORM_MSG = (() => {
  try {
    return JSON.parse(document.getElementById('kpFormMessages')?.textContent || '{}');
  } catch {
    return {};
  }
})();

function fieldMsg(field, key) {
  return field.dataset[`error${key.charAt(0).toUpperCase()}${key.slice(1)}`]
    || FORM_MSG[key]
    || '';
}

function setFieldError(field, message) {
  const wrap = field.closest('.kp-form__fld');
  if (!wrap) {
    field.classList.toggle('err', Boolean(message));
    return;
  }

  let errEl = wrap.querySelector('.kp-form__error');

  if (!message) {
    field.classList.remove('err');
    field.removeAttribute('aria-invalid');
    field.removeAttribute('aria-describedby');
    errEl?.remove();
    return;
  }

  field.classList.add('err');
  field.setAttribute('aria-invalid', 'true');

  if (!errEl) {
    errEl = document.createElement('p');
    errEl.className = 'kp-form__error';
    errEl.setAttribute('role', 'alert');
    wrap.appendChild(errEl);
  }

  const errId = `${field.id || field.name}-error`;
  errEl.id = errId;
  errEl.textContent = message;
  field.setAttribute('aria-describedby', errId);
}

function setCheckboxError(checkbox, message) {
  const wrap = checkbox.closest('.kp-checkbox');
  if (!wrap) return;

  wrap.classList.toggle('err', Boolean(message));
  let errEl = wrap.nextElementSibling?.classList?.contains('kp-form__error')
    ? wrap.nextElementSibling
    : wrap.parentElement?.querySelector('.kp-form__error--gdpr');

  if (!message) {
    errEl?.remove();
    return;
  }

  if (!errEl) {
    errEl = document.createElement('p');
    errEl.className = 'kp-form__error kp-form__error--gdpr';
    errEl.setAttribute('role', 'alert');
    wrap.insertAdjacentElement('afterend', errEl);
  }

  errEl.textContent = message;
}

function initFieldValidation() {
  document.querySelectorAll('.kp-form').forEach(form => {
    form.querySelectorAll('.kp-form__inp, .kp-form__ta').forEach(field => {
      field.addEventListener('blur',  () => validateField(field));
      field.addEventListener('input', () => {
        if (field.classList.contains('err')) validateField(field);
      });
    });
    const gdpr = form.querySelector('input[name="gdpr_consent"]');
    if (gdpr) {
      gdpr.addEventListener('change', () => {
        if (gdpr.checked) setCheckboxError(gdpr, '');
      });
    }
  });
}

function phoneDigits(val) {
  return val.replace(/\D/g, '');
}

function isValidPhone(val) {
  const trimmed = val.trim();
  if (!trimmed || !/^[+\d\s\-()\u00A0]+$/.test(trimmed)) return false;

  const digits = phoneDigits(trimmed);
  if (digits.length < 10 || digits.length > 15) return false;
  if (/^0+$/.test(digits) || /^(\d)\1+$/.test(digits)) return false;

  if (digits.startsWith('380')) {
    return digits.length === 12 && digits[3] !== '0';
  }
  if (digits.startsWith('0')) {
    return digits.length === 10 && digits[1] !== '0';
  }
  return /^[1-9]/.test(digits);
}

function validateField(field) {
  const val      = field.value.trim();
  const required = field.hasAttribute('required');
  const type     = field.type;
  let error      = '';

  if (required && !val) {
    error = fieldMsg(field, 'required');
  } else if (type === 'email' && val && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
    error = fieldMsg(field, 'email');
  } else if (type === 'tel' && val && !isValidPhone(val)) {
    error = fieldMsg(field, 'phone');
  }

  setFieldError(field, error);
  return !error;
}

function validateForm(form) {
  let valid = true;

  form.querySelectorAll('.kp-form__inp, .kp-form__ta').forEach(f => {
    if (!validateField(f)) valid = false;
  });

  const gdpr = form.querySelector('input[name="gdpr_consent"]');
  if (gdpr && !gdpr.checked) {
    valid = false;
    setCheckboxError(gdpr, fieldMsg(gdpr, 'gdpr'));
  } else if (gdpr) {
    setCheckboxError(gdpr, '');
  }

  if (!valid) {
    const firstErr = form.querySelector('.kp-form__inp.err, .kp-form__ta.err, .kp-checkbox.err input');
    firstErr?.focus?.();
  }
  return valid;
}

/* ─── HTMX FORM VALIDATION ─── */
document.addEventListener('htmx:before-request', e => {
  const form = e.target.closest('form.kp-form');
  if (!form) return;
  if (!validateForm(form)) {
    e.preventDefault();
  }
});

function replaceFormWithSuccess(target, successEl) {
  const form = document.querySelector(`form.kp-form[hx-target="#${target.id}"]`);
  if (!form) return null;

  if (form.contains(target)) {
    form.innerHTML = successEl.outerHTML;
    form.classList.add('kp-form--success');
    return form;
  }

  const successClone = successEl.cloneNode(true);
  target.innerHTML = '';
  form.replaceWith(successClone);

  if (form.id === 'cfgForm') {
    document.getElementById('cfgNext')?.closest('div')?.setAttribute('hidden', '');
  }
  return successClone;
}

/* ─── HTMX FORM SUCCESS — GA4 ─── */
document.addEventListener('htmx:after-settle', e => {
  const target = e.detail.target;
  if (!target) return;
  const successEl = target.querySelector('.kp-form__success');
  if (!successEl) return;

  const form = document.querySelector(`form.kp-form[hx-target="#${target.id}"]`);
  const formType = form?.querySelector('input[name="form_type"]')?.value || 'unknown';
  const resultEl = replaceFormWithSuccess(target, successEl);
  trackGa4('form_submit', { form_type: formType });

  if (resultEl?.closest('.kp-modal')) {
    setTimeout(closeConsultModal, 2000);
  }
});

/* ─── MOBILE CTA — hide when hero is visible ─── */
function initMobileCta() {
  const cta  = document.getElementById('mobileCta');
  const hero = document.getElementById('hero');
  if (!cta || !hero) return;

  const obs = new IntersectionObserver(entries => {
    cta.classList.toggle('is-faded', entries[0].isIntersecting);
  }, { threshold: 0.25 });

  obs.observe(hero);
}

/* ─── SMOOTH SCROLL for anchor links ─── */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      const hh = parseInt(
        getComputedStyle(document.documentElement).getPropertyValue('--hh')
      ) || 72;
      const top = target.getBoundingClientRect().top + window.scrollY - hh - 16;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
}

/* ─── GA4 CTA CLICK TRACKING ─── */
function initGa4CtaTracking() {
  document.querySelectorAll('.kp-btn--primary, .kp-btn--gold').forEach(btn => {
    btn.addEventListener('click', () => {
      const label = btn.textContent.trim().slice(0, 60);
      trackGa4('cta_click', { cta_label: label });
    });
  });
}

/* ─── HERO BACKGROUND VIDEO (Фаза 7) ───
 * Прогресивне покращення: <video> у DOM без src, поверх завжди лежить
 * статичне фото. Вмикаємо відео лише коли всі умови ОК; будь-яка відмова —
 * просто нічого не робимо, фото лишається видимим.
 *
 * iOS Safari специфіка:
 *  - autoplay спрацьовує лише з muted + playsinline (інакше повноекранний
 *    плеєр або мовчазна відмова) — атрибути вже прописані в HTML.
 *  - Low Power Mode / Low Data Mode можуть мовчки заблокувати play() —
 *    ловимо Promise-відмову та відкатуємось на фото, без помилок у консолі.
 *  - на слабких мобільних мережах відео просто не підвантажуємо взагалі
 *    (Data Saver / effectiveType 2g|slow-2g), щоб не палити трафік користувача.
 *  - призупиняємо відео, коли вкладка неактивна або hero вийшов з екрана —
 *    економія батареї, важливо саме для мобільних iOS-пристроїв.
 */
function initHeroVideo() {
  const video = document.getElementById('heroVideo');
  if (!video) return;

  const src = video.dataset.src;
  if (!src) return;

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const conn = navigator.connection || navigator.webkitConnection || navigator.mozConnection;
  if (conn && (conn.saveData || /2g/.test(conn.effectiveType || ''))) return;

  video.src = src;
  video.load();

  const bg = video.closest('.kp-hero__bg, .kp-about-hero__bg');

  const markPlaying = () => {
    video.classList.add('is-active');
    if (bg) bg.classList.add('is-video-on');
  };

  const tryPlay = () => {
    const p = video.play();
    if (p && typeof p.catch === 'function') {
      p.then(markPlaying).catch(() => {
        /* autoplay заблоковано (Low Power Mode тощо) — лишаємо статичне фото */
      });
    } else {
      markPlaying();
    }
  };

  video.addEventListener('canplay', tryPlay, { once: true });

  if (!('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        if (video.paused && video.readyState >= 3) tryPlay();
      } else {
        video.pause();
      }
    });
  }, { threshold: 0.1 });
  observer.observe(video);

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      video.pause();
    } else if (video.getBoundingClientRect().top < window.innerHeight) {
      tryPlay();
    }
  });
}

/* ─── GA4 HELPER ─── */
function trackGa4(event, params) {
  if (typeof gtag === 'undefined') return;
  gtag('event', event, params || {});
}
