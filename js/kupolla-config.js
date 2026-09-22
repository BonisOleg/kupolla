/**
 * KUPOLLA Configurator JS
 * Single-page: select filling → price + photo update instantly
 */

const BASE_PRICE = 55000;
const PRODUCT_MODEL = 'kupolla-s';

const CFG_PREVIEW_PHOTOS = {
  'base':     '/static/images/models/kupolla-s-exterior-forest.png',
  'standard': '/static/images/gallery/glamping-forest-kupolla-s.png',
  'premium':  '/static/images/hero/kupolla-dome-forest.png',
};

const cfg = {
  model: PRODUCT_MODEL,
  diameter: '6.8m',
  tier: null,
  addons: new Set(),
  basePrice: BASE_PRICE,
};

document.addEventListener('DOMContentLoaded', () => {
  initConfigurator();
});

window.KupollaCfg = { cfg, updatePreviewPhoto, CFG_PREVIEW_PHOTOS, BASE_PRICE };

function initConfigurator() {
  const root = document.getElementById('kpConfigurator');
  if (root) {
    cfg.model = root.getAttribute('data-product-model') || PRODUCT_MODEL;
    cfg.basePrice = parseFloat(root.getAttribute('data-base-price') || BASE_PRICE);
    cfg.diameter = root.getAttribute('data-diameter') || cfg.diameter;
  }
  const photosEl = document.getElementById('cfgPreviewPhotos');
  if (photosEl) {
    try {
      Object.assign(CFG_PREVIEW_PHOTOS, JSON.parse(photosEl.textContent));
    } catch (err) {
      /* лишаємо дефолтні фото Prime */
    }
  }
  bindTierInputs();
  bindAddonInputs();
  syncCfgFromDom();
  refreshPreview();
  updateSummaryPanel();
  updatePrice();
}

function syncCfgFromDom() {
  const tierRadio = document.querySelector('input[name="cfg_tier"]:checked');
  if (tierRadio) cfg.tier = tierRadio.value;
  cfg.addons = new Set(
    [...document.querySelectorAll('input[name="cfg_addon"]:checked')].map(cb => cb.value)
  );
}

function bindTierInputs() {
  document.querySelectorAll('input[name="cfg_tier"]').forEach(r => {
    r.addEventListener('change', () => {
      cfg.tier = r.value;
      refreshPreview();
      updatePrice();
      updateSummaryPanel();
      syncHiddenField();
      autoScrollToSection('cfgAddonsSection');
    });
  });
}

function autoScrollToSection(id) {
  const section = document.getElementById(id);
  if (!section) return;
  const hh = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--hh')) || 72;
  setTimeout(() => {
    window.scrollTo({
      top: section.getBoundingClientRect().top + window.scrollY - hh - 16,
      behavior: 'smooth',
    });
  }, 350);
}

function bindAddonInputs() {
  document.querySelectorAll('input[name="cfg_addon"]').forEach(cb => {
    cb.addEventListener('change', () => {
      cfg.addons[cb.checked ? 'add' : 'delete'](cb.value);
      refreshPreview();
      updatePrice();
      updateSummaryPanel();
      syncHiddenField();
    });
  });
}

function calcTotal() {
  let total = cfg.basePrice || BASE_PRICE;
  document.querySelectorAll('input[name="cfg_tier"]:checked').forEach(r => {
    total += parseFloat(r.closest('[data-delta]')?.getAttribute('data-delta') || 0);
  });
  document.querySelectorAll('input[name="cfg_addon"]:checked').forEach(cb => {
    total += parseFloat(cb.closest('[data-delta]')?.getAttribute('data-delta') || 0);
  });
  return total;
}

function updatePrice() {
  const total = calcTotal();
  const formatted = total > 0 ? '€\u202f' + total.toLocaleString('de-DE') : '—';
  const el = document.getElementById('cfgTotal');
  if (el) {
    el.textContent = formatted;
    el.classList.remove('updated');
    void el.offsetWidth;
    el.classList.add('updated');
  }
  const bar = document.getElementById('cfgBarTotal');
  if (bar) bar.textContent = formatted;
}

function syncHiddenField() {
  const el = document.getElementById('cfgHiddenData');
  if (!el) return;
  const tier = document.querySelector('input[name="cfg_tier"]:checked')
    ?.closest('[data-code]')?.getAttribute('data-code') || cfg.tier || '—';
  el.value = JSON.stringify({
    model: cfg.model,
    diameter: cfg.diameter || '6.8m',
    tier,
    addons: [...cfg.addons],
    price: calcTotal() > 0 ? '€' + calcTotal().toLocaleString('de-DE') : '—',
  });
}

/* ═══ PREVIEW ═══ */
function refreshPreview() {
  updatePreviewPhoto();
  updateDomeSvg();
}

function updatePreviewPhoto() {
  const img = document.getElementById('cfgPreviewImg');
  if (!img) return;

  const tier = (cfg.tier || '').toLowerCase();
  const url = CFG_PREVIEW_PHOTOS[tier] || CFG_PREVIEW_PHOTOS['base'] || '';
  if (!url) return;

  const loaded = img.getAttribute('data-loaded') || '';
  if (loaded === url) return;

  img.classList.add('is-changing');
  const preload = new Image();
  preload.onload = () => {
    img.src = url;
    img.setAttribute('data-loaded', url);
    img.classList.remove('is-changing');
  };
  preload.onerror = () => img.classList.remove('is-changing');
  preload.src = url;
}

function updateDomeSvg() {
  const svg = document.getElementById('cfgDomeSvg');
  if (!svg) return;

  const addons = [...cfg.addons];
  const hasTerrace   = addons.some(c => /terrace|тераса/i.test(c));
  const hasPanoramic = addons.some(c => /panoramic|панорам/i.test(c));
  const hasSolar     = addons.some(c => /solar|сонячн/i.test(c));
  const hasSmartHome = addons.some(c => /smarthome|smart.?home|смарт/i.test(c));
  const isPremium    = /premium|преміум/i.test(cfg.tier || '');

  const set = (id, visible) => {
    const el = document.getElementById(id);
    if (el) el.classList.toggle('is-on', visible);
  };

  set('cfgTerrace',   hasTerrace);
  set('cfgWindow',    hasPanoramic || isPremium);
  set('cfgSolar',     hasSolar);
  set('cfgSmartHome', hasSmartHome);

  const domeBody = document.getElementById('domeBody');
  if (domeBody) {
    domeBody.classList.toggle('is-premium', isPremium);
  }

  svg.classList.remove('changed');
  void svg.offsetWidth;
  svg.classList.add('changed');
}

function updateSummaryPanel() {
  const tierEl = document.getElementById('sumTier');
  const addonsEl = document.getElementById('sumAddons');

  if (tierEl) {
    const radio = document.querySelector('input[name="cfg_tier"]:checked');
    tierEl.textContent = radio
      ? (radio.closest('.kp-cfg-tier')?.querySelector('.kp-cfg-tier__name')?.textContent?.trim() || radio.value)
      : '—';
  }
  if (addonsEl) {
    const names = [...document.querySelectorAll('input[name="cfg_addon"]:checked')].map(cb =>
      cb.closest('.kp-cfg-opt')?.querySelector('.kp-cfg-opt__name')?.textContent?.trim() || cb.value
    );
    addonsEl.textContent = names.length ? names.join(', ') : '—';
  }
}
