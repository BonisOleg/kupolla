/**
 * KUPOLLA Configurator — static configurator.html
 * Потребує kupolla-config.js (window.KupollaCfg)
 */

const LEGACY_SCALES = { S: 0.78, M: 1.0, L: 1.18 };

document.addEventListener('DOMContentLoaded', () => {
  if (!document.getElementById('previewDomeSvg')) return;
  initLegacyConfigurator();
});

function getCfg() {
  return window.KupollaCfg?.cfg;
}

function legacyRefresh() {
  window.KupollaCfg?.updatePreviewBg();
  updateLegacySvg();
}

function initLegacyConfigurator() {
  syncLegacyFromDom();
  bindLegacyInputs();
  updateLegacyPrice();
  updateLegacySummary();
  legacyRefresh();

  document.getElementById('cfgFormEl')?.addEventListener('submit', e => {
    e.preventDefault();
    syncLegacyHidden();
    alert('Заявку надіслано (демо). Підключіть HTMX/API для продакшену.');
  });
}

function syncLegacyFromDom() {
  const cfg = getCfg();
  if (!cfg) return;
  const model = document.querySelector('input[name="model"]:checked');
  if (model) {
    cfg.model = model.value;
    cfg.basePrice = parseInt(model.dataset.price, 10)
      || window.KupollaCfg.BASE_PRICES[model.value] || 0;
  }
  const tier = document.querySelector('input[name="tier"]:checked');
  if (tier) cfg.tier = tier.value;
  const diam = document.querySelector('input[name="diameter"]:checked');
  if (diam) cfg.diameter = diam.value;
  cfg.addons = new Set(
    [...document.querySelectorAll('input[name="options"]:checked')].map(cb => cb.value)
  );
}

function bindLegacyInputs() {
  const onChange = () => {
    syncLegacyFromDom();
    legacyRefresh();
    updateLegacyPrice();
    updateLegacySummary();
    syncLegacyHidden();
  };
  document.querySelectorAll('input[name="model"], input[name="diameter"], input[name="tier"]')
    .forEach(r => r.addEventListener('change', onChange));
  document.querySelectorAll('input[name="options"]')
    .forEach(cb => cb.addEventListener('change', onChange));
}

function goStep(n) {
  document.querySelectorAll('.kp-cfg-step[data-step]').forEach(s => {
    s.classList.toggle('active', parseInt(s.dataset.step, 10) === n);
  });
  document.querySelectorAll('.kp-csi__item[data-step]').forEach(el => {
    const step = parseInt(el.dataset.step, 10);
    el.classList.toggle('active', step === n);
    el.classList.toggle('done', step < n);
  });
  legacyRefresh();
  const target = document.querySelector(`.kp-cfg-step[data-step="${n}"]`);
  if (!target) return;
  const hh = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--hh')) || 72;
  window.scrollTo({
    top: target.getBoundingClientRect().top + window.scrollY - hh - 16,
    behavior: 'smooth',
  });
}
window.goStep = goStep;

function calcLegacyTotal() {
  const cfg = getCfg();
  let total = cfg?.basePrice || 0;
  const diam = document.querySelector('input[name="diameter"]:checked');
  if (diam) total += parseInt(diam.dataset.extra, 10) || 0;
  const tier = document.querySelector('input[name="tier"]:checked');
  if (tier) total += parseInt(tier.dataset.extra, 10) || 0;
  document.querySelectorAll('input[name="options"]:checked').forEach(cb => {
    total += parseInt(cb.dataset.price, 10) || 0;
  });
  return total;
}

function updateLegacyPrice() {
  const el = document.getElementById('priceDisplay');
  if (!el) return;
  el.textContent = '€\u202f' + calcLegacyTotal().toLocaleString('de-DE');
  el.classList.remove('updated');
  void el.offsetWidth;
  el.classList.add('updated');
}

function updateLegacySummary() {
  const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
  const model = document.querySelector('input[name="model"]:checked');
  set('sumModel', model ? `KUPOLLA ${model.value}` : '—');
  const diam = document.querySelector('input[name="diameter"]:checked');
  set('sumDiam', diam ? `${diam.value} м` : '—');
  const tier = document.querySelector('input[name="tier"]:checked');
  const tierNames = { base: 'Базова', standard: 'Стандарт', premium: 'Преміум' };
  set('sumTier', tier ? (tierNames[tier.value] || tier.value) : '—');
  const opts = [...document.querySelectorAll('input[name="options"]:checked')];
  const row = document.getElementById('sumOptsRow');
  if (row) row.style.display = opts.length ? '' : 'none';
  set('sumOpts', opts.length ? opts.map(o => o.dataset.label || o.value).join(', ') : '—');
}

function syncLegacyHidden() {
  const cfg = getCfg();
  const el = document.getElementById('cfgHiddenData');
  if (!el || !cfg) return;
  el.value = JSON.stringify({
    model: cfg.model,
    diameter: cfg.diameter,
    tier: cfg.tier,
    options: [...cfg.addons],
    price: '€' + calcLegacyTotal().toLocaleString('de-DE'),
  });
}

function setOpacity(id, val) {
  const el = document.getElementById(id);
  if (el) el.style.opacity = val;
}

function updateLegacySvg() {
  const cfg = getCfg();
  const svg = document.getElementById('previewDomeSvg');
  if (!cfg || !svg) return;

  const scale = LEGACY_SCALES[cfg.model] || 1.0;
  const domeGroup = document.getElementById('domeGroup');
  if (domeGroup) domeGroup.style.transform = `scale(${scale})`;

  const tier = (cfg.tier || 'standard').toLowerCase();
  const opts = [...cfg.addons];
  const isPremium = tier === 'premium';
  const isStandard = tier === 'standard' || isPremium;

  setOpacity('prevGlow', isPremium ? '1' : '0');
  setOpacity('prevPanoramic', isStandard ? '1' : '0');
  setOpacity('prevPanoramicGlare', isStandard ? '1' : '0');
  setOpacity('prevExtraWin', opts.includes('windows') ? '1' : '0');
  setOpacity('prevTerrace', (opts.includes('terrace') || isStandard) ? '1' : '0');
  setOpacity('prevEngineering', opts.includes('engineering') ? '1' : '0');
  setOpacity('prevSmart', (opts.includes('smart') || isPremium) ? '1' : '0');
  setOpacity('prevSolar', opts.includes('solar') ? '1' : '0');
  setOpacity('prevFoundation', opts.includes('foundation') ? '1' : '0');

  const domeBody = document.getElementById('domeBody');
  if (domeBody) {
    domeBody.style.fill = isPremium ? 'rgba(202,187,172,.14)' : 'rgba(14,35,25,.32)';
  }

  const badge = document.getElementById('modelBadge');
  if (badge) badge.textContent = `KUPOLLA ${cfg.model || 'M'}`;

  const diamText = document.getElementById('diamText');
  if (diamText && cfg.diameter) diamText.textContent = `⌀ ${cfg.diameter} м`;

  const tierBadge = document.getElementById('tierBadge');
  if (tierBadge) {
    const labels = { base: 'БАЗОВА', standard: 'СТАНДАРТ', premium: 'ПРЕМІУМ' };
    tierBadge.textContent = labels[tier] || tier.toUpperCase();
  }

  svg.classList.remove('changed');
  void svg.offsetWidth;
  svg.classList.add('changed');
}
