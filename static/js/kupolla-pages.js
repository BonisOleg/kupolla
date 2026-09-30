/**
 * KUPOLLA — Inner Pages JS
 * FAQ accordion, Gallery lightbox + filter, Blog filter, Catalog filter.
 * Форми: валідація і HTMX-submit централізовано в kupolla.js.
 */

document.addEventListener('DOMContentLoaded', () => {
  initAccordion();
  initGallery();
  initBlogFilter();
  initCatalogFilter();
});

/* ─── FAQ ACCORDION ─── */
function initAccordion() {
  document.querySelectorAll('.kp-acc-trigger').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.kp-acc-item');
      const accordion = btn.closest('.kp-accordion');
      const isOpen = item.classList.contains('open');

      accordion?.querySelectorAll('.kp-acc-item.open').forEach(el => {
        if (el === item) return;
        el.classList.remove('open');
        el.querySelector('.kp-acc-trigger')?.setAttribute('aria-expanded', 'false');
      });

      item.classList.toggle('open', !isOpen);
      btn.setAttribute('aria-expanded', String(!isOpen));
    });
  });
}

/* ─── GALLERY LIGHTBOX + FILTER ─── */
function initGallery() {
  initGalleryFilter();
  initLightbox();
}

function initGalleryFilter() {
  const tabs  = document.querySelectorAll('.kp-gallery-tab');
  const items = document.querySelectorAll('.kp-gallery-item');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const filter = tab.getAttribute('data-filter');

      items.forEach(item => {
        const cat = item.getAttribute('data-cat');
        const show = filter === 'all' || cat === filter;
        item.toggleAttribute('hidden', !show);
      });
    });
  });
}

function initLightbox() {
  const lb = document.getElementById('lightbox') || document.getElementById('kpLightbox');
  if (!lb) return;

  const lbImg     = lb.querySelector('#lightboxImg') || lb.querySelector('.kp-lightbox__img');
  const lbCaption = lb.querySelector('.kp-lightbox__caption');
  const lbClose   = lb.querySelector('.kp-lightbox__close') || document.getElementById('lightboxCloseBtn');
  const lbBackdrop = lb.querySelector('.kp-lightbox__bd') || lb;

  function showItem(item) {
    const btn     = item.querySelector('[data-lightbox]');
    const photo   = item.querySelector('.kp-gallery-item__img');
    const caption = item.getAttribute('data-caption')
      || btn?.getAttribute('data-alt')
      || photo?.getAttribute('alt')
      || '';

    if (!lbImg) return;
    if (btn) {
      lbImg.src = btn.getAttribute('data-lightbox') || '';
      lbImg.alt = btn.getAttribute('data-alt') || caption;
    } else if (photo) {
      lbImg.src = photo.currentSrc || photo.src;
      lbImg.alt = photo.alt || caption;
    } else {
      return;
    }

    if (lbCaption) lbCaption.textContent = caption;
    openLightbox(lb);
  }

  document.querySelectorAll('.kp-gallery-item').forEach(item => {
    const trigger = item.querySelector('.kp-gallery-item__btn') || item;
    trigger.addEventListener('click', e => {
      e.preventDefault();
      showItem(item);
    });
  });

  lbClose?.addEventListener('click', () => closeLightbox(lb));
  lbBackdrop?.addEventListener('click', e => { if (e.target === lbBackdrop || e.target === lb) closeLightbox(lb); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(lb); });
}

function openLightbox(lb) {
  const box = lb || document.getElementById('lightbox') || document.getElementById('kpLightbox');
  box?.classList.add('open');
  box?.setAttribute('aria-hidden', 'false');
  document.body.classList.add('is-locked');
}
function closeLightbox(lb) {
  const box = lb || document.getElementById('lightbox') || document.getElementById('kpLightbox');
  box?.classList.remove('open');
  box?.setAttribute('aria-hidden', 'true');
  document.body.classList.remove('is-locked');
}

/* ─── BLOG CATEGORY FILTER ─── */
function initBlogFilter() {
  const tabs  = document.querySelectorAll('.kp-blog-tab');
  const cards = document.querySelectorAll('.kp-blog-card[data-cat]');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const filter = tab.getAttribute('data-filter');

      cards.forEach(card => {
        const show = filter === 'all' || card.getAttribute('data-cat') === filter;
        card.toggleAttribute('hidden', !show);
      });
    });
  });
}

/* ─── CATALOG FILTER ─── */
const CATALOG_AREA_BOUNDS = {
  compact:  { min: 0,   max: 50         },
  standard: { min: 50,  max: 100        },
  spacious: { min: 100, max: Infinity   },
};
const CATALOG_PRICE_BOUNDS = {
  entry: { min: 0,      max: 50000      },
  mid:   { min: 50000,  max: 120000     },
  top:   { min: 120000, max: Infinity   },
};

function applyCatalogFiltersFromUrl() {
  const filters = document.getElementById('kpCatalogFilters');
  if (!filters) return;

  const params = new URLSearchParams(window.location.search);
  filters.querySelectorAll('[data-filter-group]').forEach(group => {
    const key = group.dataset.filterGroup;
    const val = params.has(key) ? (params.get(key) || '') : null;
    if (val === null) return;

    group.querySelectorAll('.kp-filter-btn').forEach(btn => {
      btn.classList.toggle('active', (btn.dataset.filterVal || '') === val);
    });
  });
}

function initCatalogFilter() {
  const filters = document.getElementById('kpCatalogFilters');
  if (!filters) return;

  document.querySelectorAll('#kpCatalogGrid .kp-reveal').forEach(el => {
    el.classList.add('vis');
  });

  applyCatalogFiltersFromUrl();

  filters.querySelectorAll('[data-filter-group]').forEach(group => {
    group.querySelectorAll('.kp-filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        group.querySelectorAll('.kp-filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        runCatalogFilter();
      });
    });
  });

  document.getElementById('kpCatalogReset')?.addEventListener('click', () => {
    filters.querySelectorAll('[data-filter-group]').forEach(group => {
      group.querySelectorAll('.kp-filter-btn').forEach((btn, i) => {
        btn.classList.toggle('active', i === 0);
      });
    });
    runCatalogFilter();
  });

  window.addEventListener('popstate', () => {
    applyCatalogFiltersFromUrl();
    runCatalogFilter();
  });

  runCatalogFilter();
}

function runCatalogFilter() {
  const filters = document.getElementById('kpCatalogFilters');
  if (!filters) return;

  const state = {};
  filters.querySelectorAll('[data-filter-group]').forEach(group => {
    const active = group.querySelector('.kp-filter-btn.active');
    state[group.dataset.filterGroup] = active?.dataset.filterVal || '';
  });

  const cards   = document.querySelectorAll('#kpCatalogGrid .kp-catalog-card');
  let   visible = 0;

  cards.forEach(card => {
    const purpose = card.dataset.purpose || '';
    const size    = card.dataset.size    || '';
    const area    = parseFloat(card.dataset.area)  || 0;
    const price   = parseFloat(card.dataset.price) || 0;

    let show = true;

    if (state.purpose) show = show && purpose === state.purpose;
    if (state.size)    show = show && size    === state.size;

    if (state.area && CATALOG_AREA_BOUNDS[state.area]) {
      const { min, max } = CATALOG_AREA_BOUNDS[state.area];
      show = show && area >= min && (max === Infinity || area <= max);
    }
    if (state.price && CATALOG_PRICE_BOUNDS[state.price]) {
      const { min, max } = CATALOG_PRICE_BOUNDS[state.price];
      show = show && price >= min && (max === Infinity || price <= max);
    }

    card.classList.toggle('is-filtered-out', !show);
    card.toggleAttribute('hidden', !show);
    if (show) visible++;
  });

  const empty = document.getElementById('kpCatalogEmpty');
  if (empty) empty.toggleAttribute('hidden', !(cards.length > 0 && visible === 0));

  const params = new URLSearchParams();
  Object.entries(state).forEach(([k, v]) => { if (v) params.set(k, v); });
  const qs = params.toString();
  history.replaceState(null, '', location.pathname + (qs ? '?' + qs : ''));
}
