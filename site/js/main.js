(function () {
  'use strict';
  var d = document;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // year
  var y = d.getElementById('year'); if (y) y.textContent = new Date().getFullYear();

  // header scrolled state + scroll progress + hero parallax
  var header = d.querySelector('.site-header');
  var bar = d.querySelector('.progress');
  var heroBg = d.querySelector('.hero-bg');
  var ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () {
      var sc = window.scrollY, max = d.documentElement.scrollHeight - innerHeight;
      header.classList.toggle('scrolled', sc > 30);
      if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? sc / max : 0) + ')';
      if (heroBg && !reduce && sc < innerHeight * 1.2) heroBg.style.transform = 'translateY(' + sc * 0.25 + 'px) scale(1.05)';
      ticking = false;
    });
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // sliding nav pill
  var nav = d.getElementById('nav');
  var pill = nav && nav.querySelector('.pill');
  var links = nav ? [].slice.call(nav.querySelectorAll('a')) : [];
  function movePill(a) {
    if (!pill || !a) { if (pill) pill.style.opacity = 0; return; }
    pill.style.opacity = 1;
    pill.style.width = a.offsetWidth + 'px';
    pill.style.transform = 'translateX(' + a.offsetLeft + 'px)';
  }
  function resetPill() { movePill(nav.querySelector('a.active')); }
  if (nav) {
    links.forEach(function (a) {
      a.addEventListener('mouseenter', function () { movePill(a); });
      a.addEventListener('focus', function () { movePill(a); });
    });
    nav.addEventListener('mouseleave', resetPill);
    nav.addEventListener('focusout', resetPill);
    addEventListener('resize', resetPill);
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(resetPill);
    resetPill();
  }

  // mobile menu
  var burger = d.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); } });
  }

  // scroll reveal
  var rev = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    rev.forEach(function (el) { io.observe(el); });
  } else rev.forEach(function (el) { el.classList.add('in'); });

  // counters
  var counters = d.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, to = +el.dataset.count, suf = el.dataset.suffix || '', t0 = performance.now();
        (function step(t) {
          var p = Math.min((t - t0) / 1400, 1), eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(to * eased) + (p === 1 ? suf : '');
          if (p < 1 && !reduce) requestAnimationFrame(step); else el.textContent = to + suf;
        })(t0);
        co.unobserve(el);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { co.observe(c); });
  }

  // cursor spotlight on cards
  d.querySelectorAll('.spot').forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  // magnetic buttons
  if (!reduce && matchMedia('(hover:hover)').matches) {
    d.querySelectorAll('.magnetic').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * 0.18, yy = (e.clientY - r.top - r.height / 2) * 0.25;
        b.style.translate = x + 'px ' + yy + 'px';
      });
      b.addEventListener('pointerleave', function () { b.style.translate = ''; });
    });
  }

  // lightbox
  var lb = d.querySelector('.lightbox');
  if (lb) {
    var lbImg = lb.querySelector('.lb-img');
    function closeLb() { lb.hidden = true; d.body.style.overflow = ''; }
    d.querySelectorAll('.gallery .photo').forEach(function (p) {
      p.tabIndex = 0; p.setAttribute('role', 'button');
      function open() {
        var cs = getComputedStyle(p);
        lbImg.style.backgroundImage = cs.backgroundImage;
        lbImg.style.setProperty('--g', 'none');
        lbImg.setAttribute('aria-label', p.getAttribute('aria-label'));
        lb.hidden = false; d.body.style.overflow = 'hidden';
        lb.querySelector('.lb-close').focus();
      }
      p.addEventListener('click', open);
      p.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb-close')) closeLb(); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) closeLb(); });
  }

  // enquiry form -> WhatsApp (no backend needed)
  var form = d.getElementById('enquiry');
  if (form) {
    var today = new Date().toISOString().slice(0, 10);
    var ci = form.checkin, co2 = form.checkout;
    ci.min = today; co2.min = today;
    ci.addEventListener('change', function () { co2.min = ci.value || today; if (co2.value && co2.value < ci.value) co2.value = ci.value; });
    var q = new URLSearchParams(location.search).get('room');
    if (q) form.message.value = 'I am interested in: ' + q + '.';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      [form.name, form.phone, ci, co2, form.guests].forEach(function (f) {
        var bad = !f.value.trim(); f.classList.toggle('bad', bad); if (bad) ok = false;
      });
      var note = d.getElementById('form-note');
      if (!ok) { note.textContent = 'Please fill in the highlighted fields.'; return; }
      var msg = 'Hello ' + (window.PROP_NAME || '') + ',\n' +
        'Name: ' + form.name.value + '\nPhone: ' + form.phone.value +
        '\nCheck-in: ' + ci.value + '\nCheck-out: ' + co2.value +
        '\nGuests: ' + form.guests.value +
        (form.message.value ? '\nMessage: ' + form.message.value : '');
      note.textContent = 'Opening WhatsApp...';
      window.open('https://wa.me/' + window.WA_NUMBER + '?text=' + encodeURIComponent(msg), '_blank', 'noopener');
    });
  }
})();
