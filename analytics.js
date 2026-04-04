/**
 * analytics.js — Unified analytics layer for jarvis.ripper234.com
 * 
 * Stack:
 *   - Plausible Analytics (quantitative: views, referrers, funnels, goals)
 *   - Microsoft Clarity (qualitative: heatmaps, session recordings, scroll maps)
 *   - GitHub Traffic API (14-day repo stats, used in admin dashboard)
 *
 * Setup:
 *   1. Create Plausible account → add site "jarvis.ripper234.com"
 *   2. Create Clarity project → get project ID
 *   3. Set window.ANALYTICS_CONFIG before loading this script, or it auto-detects from <meta> tags
 *
 * Usage:
 *   <meta name="plausible-domain" content="jarvis.ripper234.com">
 *   <meta name="clarity-project" content="YOUR_CLARITY_ID">
 *   <script src="analytics.js" defer></script>
 *
 *   // Custom events (from any page):
 *   window.analytics?.track('cta-click', { page: 'balance', target: 'whatsapp' });
 *
 * Event naming convention:
 *   category-action  e.g. cta-click, section-expand, prompt-copy, link-external
 *   Props always include { page: 'balance' | 'academy' | ... }
 */

(function () {
  'use strict';

  // --- Config ---
  var config = window.ANALYTICS_CONFIG || {};
  var plausibleDomain = config.plausible || getMeta('plausible-domain') || '';
  var clarityId = config.clarity || getMeta('clarity-project') || '';

  function getMeta(name) {
    var el = document.querySelector('meta[name="' + name + '"]');
    return el ? el.getAttribute('content') : '';
  }

  // --- Plausible ---
  if (plausibleDomain) {
    var ps = document.createElement('script');
    ps.defer = true;
    ps.dataset.domain = plausibleDomain;
    ps.dataset.api = 'https://plausible.io/api/event';
    ps.src = 'https://plausible.io/js/script.file-downloads.outbound-links.tagged-events.js';
    document.head.appendChild(ps);

    // Plausible custom event queue (fires before script loads)
    window.plausible = window.plausible || function () {
      (window.plausible.q = window.plausible.q || []).push(arguments);
    };
  }

  // --- Microsoft Clarity ---
  if (clarityId) {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', clarityId);
  }

  // --- Public API ---
  var pageName = detectPage();

  window.analytics = {
    /**
     * Track a custom event.
     * @param {string} event - Event name (e.g. 'cta-click', 'section-expand')
     * @param {object} [props] - Additional properties
     */
    track: function (event, props) {
      props = props || {};
      props.page = props.page || pageName;

      // Plausible custom event
      if (window.plausible) {
        window.plausible(event, { props: props });
      }

      // Clarity custom tag
      if (window.clarity) {
        window.clarity('set', event, props.page + ':' + (props.target || props.section || ''));
      }
    }
  };

  // --- Auto-tracking ---

  // 1. Scroll depth (25%, 50%, 75%, 90%)
  var scrollTracked = {};
  var scrollThresholds = [25, 50, 75, 90];
  window.addEventListener('scroll', debounce(function () {
    var scrollPct = getScrollPercent();
    scrollThresholds.forEach(function (t) {
      if (scrollPct >= t && !scrollTracked[t]) {
        scrollTracked[t] = true;
        window.analytics.track('scroll-depth', { depth: t + '%' });
      }
    });
  }, 200));

  // 2. CTA button clicks (any element with .cta-button or [data-track="cta"])
  document.addEventListener('click', function (e) {
    var cta = e.target.closest('.cta-button, [data-track="cta"]');
    if (cta) {
      var target = cta.getAttribute('href') || cta.textContent.trim().substring(0, 50);
      window.analytics.track('cta-click', { target: target });
    }
  });

  // 3. Outbound link clicks (handled by Plausible's outbound-links extension)
  //    We add Clarity tagging on top
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href]');
    if (link && link.hostname !== window.location.hostname) {
      window.analytics.track('link-external', { target: link.hostname });
    }
  });

  // 4. Section expand/collapse (for accordion-style pages like Academy)
  document.addEventListener('click', function (e) {
    var toggle = e.target.closest('.section-toggle, [data-track="expand"]');
    if (toggle) {
      var label = toggle.textContent.trim().split('\n')[0].replace('▶', '').trim().substring(0, 60);
      window.analytics.track('section-expand', { section: label });
    }
  });

  // 5. Copy events (prompt copy, etc.)
  document.addEventListener('click', function (e) {
    var copyBtn = e.target.closest('[data-track="copy"], .copy-btn');
    if (copyBtn) {
      var context = copyBtn.closest('[data-track-context]');
      window.analytics.track('prompt-copy', {
        target: context ? context.getAttribute('data-track-context') : 'unknown'
      });
    }
  });

  // 6. Time on page (30s, 60s, 120s, 300s)
  var timeThresholds = [30, 60, 120, 300];
  var timeStart = Date.now();
  var timeTracked = {};
  setInterval(function () {
    var elapsed = Math.floor((Date.now() - timeStart) / 1000);
    timeThresholds.forEach(function (t) {
      if (elapsed >= t && !timeTracked[t]) {
        timeTracked[t] = true;
        window.analytics.track('time-on-page', { seconds: t + 's' });
      }
    });
  }, 5000);

  // --- Utilities ---
  function getScrollPercent() {
    var h = document.documentElement;
    var b = document.body;
    var st = h.scrollTop || b.scrollTop;
    var sh = (h.scrollHeight || b.scrollHeight) - h.clientHeight;
    return sh > 0 ? Math.round((st / sh) * 100) : 0;
  }

  function debounce(fn, ms) {
    var timer;
    return function () {
      clearTimeout(timer);
      timer = setTimeout(fn, ms);
    };
  }

  function detectPage() {
    var path = window.location.pathname;
    if (path.includes('balance')) return 'balance';
    if (path.includes('learn')) return 'academy';
    if (path.includes('methodology')) return 'methodology';
    if (path.includes('setup')) return 'setup';
    if (path.includes('tiny-pr')) return 'tiny-pr-bot';
    if (path.includes('request-for-startups')) return 'rfs';
    if (path.includes('projects')) return 'projects';
    if (path.includes('dev-practices')) return 'dev-practices';
    if (path.includes('admin')) return 'admin';
    if (path.includes('academy-marketing')) return 'academy-marketing';
    if (path === '/' || path.includes('index')) return 'home';
    return 'other';
  }
})();
