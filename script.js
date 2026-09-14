/* Kuber Estate — site behaviour
   1. Mobile nav toggle
   2. Reveal-on-scroll (IntersectionObserver, respects reduced motion)
   3. Enquiry form → WhatsApp pre-filled message (+ Netlify Forms capture when hosted on Netlify)
*/
(function () {
  'use strict';

  var WA_NUMBER = '918637721112';

  /* ---------- 1. Mobile nav ---------- */
  var nav = document.getElementById('nav');
  var toggle = document.getElementById('navToggle');
  if (nav && toggle) {
    var setOpen = function (open) {
      nav.setAttribute('data-open', open ? 'true' : 'false');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    toggle.addEventListener('click', function () {
      setOpen(nav.getAttribute('data-open') !== 'true');
    });
    // Close after choosing a section
    nav.querySelectorAll('.nav__links a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  /* ---------- 2. Reveal on scroll ---------- */
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var reveals = document.querySelectorAll('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- 2a. Hero video: respect reduced motion, save data when hidden ---------- */
  var heroVideo = document.getElementById('heroVideo');
  if (heroVideo) {
    if (reduced) {
      heroVideo.removeAttribute('autoplay');
      heroVideo.pause();
    } else {
      var playHero = function () { var p = heroVideo.play(); if (p && p.catch) p.catch(function () {}); };
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (en) { en.isIntersecting ? playHero() : heroVideo.pause(); });
        }, { threshold: 0.1 }).observe(heroVideo);
      } else { playHero(); }
    }
  }

  /* ---------- 2b. Subsections (accordion) ---------- */
  var subs = Array.prototype.slice.call(document.querySelectorAll('.fold'));
  var setSub = function (sub, open) {
    var body = sub.querySelector('.fold__body'), head = sub.querySelector('.fold__head');
    if (open) {
      sub.classList.add('is-open'); head.setAttribute('aria-expanded', 'true');
      body.style.height = body.scrollHeight + 'px';
      var done = function () { body.style.height = 'auto'; body.removeEventListener('transitionend', done); };
      body.addEventListener('transitionend', done);
      sub.dispatchEvent(new CustomEvent('fold:open'));
    } else {
      body.style.height = body.scrollHeight + 'px';
      void body.offsetHeight;
      sub.classList.remove('is-open'); head.setAttribute('aria-expanded', 'false');
      body.style.height = '0px';
    }
  };
  subs.forEach(function (sub) {
    var body = sub.querySelector('.fold__body');
    if (sub.classList.contains('is-open')) body.style.height = 'auto';
    sub.querySelector('.fold__head').addEventListener('click', function () {
      var open = !sub.classList.contains('is-open');
      setSub(sub, open);
      if (open) setTimeout(function () {
        var top = sub.getBoundingClientRect().top + window.scrollY - 96;
        if (sub.getBoundingClientRect().top < 0) window.scrollTo({ top: top, behavior: reduced ? 'auto' : 'smooth' });
      }, 50);
    });
  });
  // keep open bodies sized when content reflows (fonts, images)
  window.addEventListener('resize', function () { subs.forEach(function (s) { if (s.classList.contains('is-open')) s.querySelector('.fold__body').style.height = 'auto'; }); });

  /* ---------- 2c. Process stepper (click-through deck) ---------- */
  var deck = document.getElementById('deck');
  if (deck) {
    var cards = Array.prototype.slice.call(deck.querySelectorAll('.dcard'));
    var STEPS = cards.length;
    var count = document.getElementById('processCount');
    var navItems = Array.prototype.slice.call(document.querySelectorAll('#stepsNav li'));
    var cur = 0, s = 0, target = 0, raf = null;
    var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var layout = function (sv) {
      cards.forEach(function (card, i) {
        var o = i - sv, y, z, sc, rx, bg, vis;
        if (o >= 0) { y = -58 * o; z = -120 * o; sc = 1 - 0.05 * o; rx = 0; vis = 'visible'; bg = 'hsl(0 0% ' + (100 - 9 * o).toFixed(1) + '%)'; }
        else { var a = -o; y = 120 * a + 900 * a * a; z = 120 * a; sc = 1 + 0.03 * a; rx = -25 * a; bg = '#ffffff'; vis = a > 0.97 ? 'hidden' : 'visible'; }
        card.style.transform = 'translate3d(0,' + y.toFixed(1) + 'px,' + z.toFixed(1) + 'px) rotateX(' + rx.toFixed(2) + 'deg) scale(' + sc.toFixed(3) + ')';
        card.style.backgroundColor = bg; card.style.visibility = vis;
        card.style.zIndex = o < 0 ? '200' : String(100 - Math.round(o * 10));
        card.classList.toggle('is-front', Math.abs(o) < 0.5);
      });
    };
    var setStep = function (i) {
      cur = i;
      navItems.forEach(function (li, k) { li.classList.toggle('is-active', k === i); li.classList.toggle('is-done', k < i); });
      if (count) count.textContent = pad(i + 1) + ' / ' + pad(STEPS);
    };
    var tick = function () {
      var d = target - s;
      if (Math.abs(d) < 0.002) { s = target; layout(s); raf = null; return; }
      s += d * (reduced ? 1 : 0.14);
      layout(s); raf = window.requestAnimationFrame(tick);
    };
    var go = function (i) {
      target = clamp(i, 0, STEPS - 1); setStep(target);
      if (!raf) raf = window.requestAnimationFrame(tick);
    };
    navItems.forEach(function (li) { li.querySelector('button').addEventListener('click', function () { go(parseInt(li.getAttribute('data-i'), 10) || 0); }); });
    var prev = document.getElementById('stepPrev'), next = document.getElementById('stepNext');
    if (prev) prev.addEventListener('click', function () { go(cur - 1); });
    if (next) next.addEventListener('click', function () { go(cur + 1 >= STEPS ? 0 : cur + 1); });
    layout(0); setStep(0);
  }

  /* ---------- 2d. Keystone story (autoplay on view) ---------- */
  var ks = document.getElementById('keystone');
  if (ks) {
    var lines = Array.prototype.slice.call(ks.querySelectorAll('.ks__lines li'));
    var timers = [], played = false;
    var stage = function (i) {
      ks.setAttribute('data-stage', String(i));
      lines.forEach(function (l, k) { l.classList.toggle('is-on', k <= i); });
    };
    var play = function () {
      timers.forEach(clearTimeout); timers = [];
      stage(-1); lines.forEach(function (l) { l.classList.remove('is-on'); });
      var gaps = reduced ? [0, 0, 0, 0] : [200, 1500, 3100, 4600];
      gaps.forEach(function (t, i) { timers.push(setTimeout(function () { stage(i); }, t)); });
    };
    var replay = document.getElementById('ksReplay');
    if (replay) replay.addEventListener('click', play);
    var tryPlay = function () { if (!played) { played = true; play(); } };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) tryPlay(); }); }, { threshold: 0.35 }).observe(ks);
    } else { tryPlay(); }
    var ksSub = ks.closest('.fold');
    if (ksSub) ksSub.addEventListener('fold:open', function () { played = false; setTimeout(tryPlay, 300); });
  }

  /* ---------- 2e. Dock: highlight the current panel ---------- */
  var dockLinks = Array.prototype.slice.call(document.querySelectorAll('.dock a[data-p]'));
  var panels = dockLinks.map(function (a) { return document.getElementById(a.getAttribute('data-p')); });
  if (dockLinks.length && 'IntersectionObserver' in window) {
    var current = null;
    var setDock = function (id) {
      if (id === current) return; current = id;
      dockLinks.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('data-p') === id); });
    };
    var onScrollDock = function () {
      var mid = window.innerHeight * 0.45, best = null, bestD = Infinity;
      panels.forEach(function (p) {
        if (!p) return; var r = p.getBoundingClientRect();
        var d = r.top <= mid && r.bottom >= mid ? 0 : Math.min(Math.abs(r.top - mid), Math.abs(r.bottom - mid));
        if (d < bestD) { bestD = d; best = p.id; }
      });
      if (best) setDock(best);
    };
    if (panels.some(function (p) { return !!p; })) { window.addEventListener('scroll', onScrollDock, { passive: true }); onScrollDock(); }
    dockLinks.forEach(function (a) {
      a.addEventListener('click', function (e) {
        var p = document.getElementById(a.getAttribute('data-p'));
        if (!p) return; e.preventDefault();
        window.scrollTo({ top: p.getBoundingClientRect().top + window.scrollY - 72, behavior: reduced ? 'auto' : 'smooth' });
      });
    });
  }

  /* ---------- 2f. Sub-pages: back button + process timeline play-on-view ---------- */
  var backBtn = document.getElementById('backBtn');
  if (backBtn) {
    backBtn.addEventListener('click', function (e) {
      var sameOrigin = document.referrer && (document.referrer.indexOf(location.origin) === 0 || location.protocol === 'file:');
      if (sameOrigin && window.history.length > 1) { e.preventDefault(); e.stopPropagation(); document.body.classList.add('is-leaving'); setTimeout(function () { window.history.back(); }, 200); }
    });
  }
  var psteps = Array.prototype.slice.call(document.querySelectorAll('.pstep, .tcard, .amenx'));
  if (psteps.length) {
    if (reduced || !('IntersectionObserver' in window)) { psteps.forEach(function (p) { p.classList.add('is-front'); }); }
    else {
      var pio = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-front'); pio.unobserve(e.target); } }); }, { threshold: 0.25 });
      psteps.forEach(function (p) { pio.observe(p); });
    }
  }

  /* ---------- 2g. Page transitions: fade out before navigating to another page ---------- */
  if (!reduced) {
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (!a || a.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.defaultPrevented) return;
      var url;
      try { url = new URL(a.getAttribute('href'), location.href); } catch (err) { return; }
      if (url.protocol !== location.protocol || url.host !== location.host) return;
      if (url.pathname === location.pathname && url.hash) return;   // same-page anchor
      e.preventDefault();
      document.body.classList.add('is-leaving');
      setTimeout(function () { location.href = url.href; }, 220);
    });
    window.addEventListener('pageshow', function () { document.body.classList.remove('is-leaving'); });
  }

  /* ---------- 2h. Connect menu (Instagram / WhatsApp) ---------- */
  var connect = document.getElementById('connect');
  var connectBtn = document.getElementById('connectBtn');
  if (connect && connectBtn) {
    var setConnect = function (open) {
      connect.setAttribute('data-open', open ? 'true' : 'false');
      connectBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      var dockEl = connect.closest('.dock');
      if (dockEl) dockEl.classList.toggle('dock--connect', open);
    };
    connectBtn.addEventListener('click', function (e) { e.stopPropagation(); setConnect(connect.getAttribute('data-open') !== 'true'); });
    document.addEventListener('click', function (e) { if (!connect.contains(e.target)) setConnect(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setConnect(false); });
    connect.querySelectorAll('.connect__menu a').forEach(function (a) {
      a.addEventListener('click', function (e) {
        setConnect(false);
        var target = document.getElementById('contact');
        if (a.classList.contains('connect__contact') && target) {
          e.preventDefault(); e.stopPropagation();
          window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 72, behavior: reduced ? 'auto' : 'smooth' });
        }
      });
    });
  }

  /* ---------- 2i. Property carousel: arrows + auto-advance ---------- */
  Array.prototype.slice.call(document.querySelectorAll('[data-carousel]')).forEach(function (car) {
    var track = car.querySelector('[data-track]');
    var tiles = track ? Array.prototype.slice.call(track.children) : [];
    if (!track || tiles.length < 2) return;
    var prev = car.querySelector('[data-prev]'), next = car.querySelector('[data-next]'), count = car.querySelector('[data-count]');
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var step = function () { return tiles[1].offsetLeft - tiles[0].offsetLeft; };
    var index = function () { return Math.round(track.scrollLeft / Math.max(1, step())); };
    var maxIndex = function () { return Math.max(0, Math.round((track.scrollWidth - track.clientWidth) / Math.max(1, step()))); };
    var cur = 0, settle = null;
    var goTo = function (i) {
      var m = maxIndex();
      if (i > m) i = 0; if (i < 0) i = m;
      cur = i;
      track.scrollTo({ left: i * step(), behavior: reduced ? 'auto' : 'smooth' });
      update();
    };
    var update = function () { if (count) count.textContent = pad(Math.min(tiles.length, cur + 1)) + ' / ' + pad(tiles.length); };
    // user swipes: adopt the tile they landed on once scrolling settles
    track.addEventListener('scroll', function () { clearTimeout(settle); settle = setTimeout(function () { cur = index(); update(); }, 160); }, { passive: true });
    if (prev) prev.addEventListener('click', function () { goTo(cur - 1); rest(); });
    if (next) next.addEventListener('click', function () { goTo(cur + 1); rest(); });
    // auto-advance, paused while the user is looking at / touching it
    var timer = null, paused = false;
    var tick = function () { if (!paused && !document.hidden && isVisible()) goTo(cur + 1); };
    var isVisible = function () { var r = car.getBoundingClientRect(); return r.bottom > 0 && r.top < window.innerHeight; };
    var start = function () { if (reduced) return; stop(); timer = setInterval(tick, 4500); };
    var stop = function () { if (timer) { clearInterval(timer); timer = null; } };
    var rest = function () { stop(); setTimeout(start, 9000); };   // after a manual click, wait longer before resuming
    ['mouseenter', 'focusin', 'pointerdown', 'touchstart'].forEach(function (ev) { car.addEventListener(ev, function () { paused = true; }, { passive: true }); });
    ['mouseleave', 'focusout'].forEach(function (ev) { car.addEventListener(ev, function () { paused = false; }); });
    car.addEventListener('touchend', function () { setTimeout(function () { paused = false; }, 6000); }, { passive: true });
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    update(); start();
  });

  /* ---------- 3. Enquiry form ---------- */
  var form = document.getElementById('enquiryForm');
  var status = document.getElementById('formStatus');
  var submitBtn = document.getElementById('submitBtn');

  function showStatus(msg) {
    if (!status) return;
    status.textContent = msg;
    status.setAttribute('data-show', 'true');
  }

  function buildMessage(data) {
    var lines = [
      'Hi Kuber Estate, new enquiry from the website:',
      '',
      'Name: ' + (data.name || '-'),
      'Phone: ' + (data.phone || '-'),
      'Email: ' + (data.email || '-'),
      'Looking to: ' + (data.purpose || '-'),
      'Budget: ' + (data.budget || '-')
    ];
    if (data.message) lines.push('', 'Details: ' + data.message);
    return lines.join('\n');
  }

  function encodeForm(fd) {
    var pairs = [];
    fd.forEach(function (v, k) { pairs.push(encodeURIComponent(k) + '=' + encodeURIComponent(v)); });
    return pairs.join('&');
  }

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Native validation with a friendly message
      if (!form.checkValidity()) {
        var firstInvalid = form.querySelector(':invalid');
        if (firstInvalid) firstInvalid.focus();
        showStatus('Please fill in your name, phone number and what you\'re looking for.');
        return;
      }

      var fd = new FormData(form);
      var data = {};
      fd.forEach(function (v, k) { data[k] = String(v).trim(); });
      if (data['bot-field']) return; // honeypot

      var waUrl = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(buildMessage(data));

      // Open WhatsApp right away (must happen inside the click/submit gesture so mobile browsers allow it)
      var win = window.open(waUrl, '_blank', 'noopener');

      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending…';

      // Also capture on the host (Netlify Forms). On other hosts this simply fails silently.
      var done = function (emailed) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send enquiry';
        form.reset();
        showStatus(emailed
          ? 'Thanks — your enquiry is in. We\'ve opened WhatsApp with your details; we\'ll get back within one working day.'
          : 'Thanks — we\'ve opened WhatsApp with your details. If it didn\'t open, message us at +91 86377 21112.');
        if (!win) {
          // Pop-up blocked: give the user a direct link
          var a = document.createElement('a');
          a.href = waUrl; a.target = '_blank'; a.rel = 'noopener';
          a.textContent = ' Open WhatsApp';
          status.appendChild(a);
        }
      };

      if (window.fetch) {
        fetch('/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: encodeForm(fd)
        }).then(function (r) { done(r.ok); }).catch(function () { done(false); });
      } else {
        done(false);
      }
    });
  }

  /* ---------- Footer year ---------- */
  var year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
