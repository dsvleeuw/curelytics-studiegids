(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (_) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (_) {} }
  };
  var root = document.documentElement;

  // thema
  $$('[data-theme-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = root.dataset.theme === 'dark' ? 'light' : 'dark';
      root.dataset.theme = t;
      try { localStorage.setItem('cl-theme', t); } catch (_) {}
    });
  });

  // niveau (junior / senior / beide)
  function setLevel(l) {
    root.dataset.level = l;
    $$('.seg [data-level]').forEach(function (b) { b.classList.toggle('on', b.dataset.level === l); });
    store.set('cl-level', l);
  }
  $$('.seg [data-level]').forEach(function (b) {
    b.addEventListener('click', function () { setLevel(b.dataset.level); });
  });
  setLevel(store.get('cl-level', 'beide'));

  // flashcards omdraaien
  document.addEventListener('click', function (ev) {
    var f = ev.target.closest('.flash');
    if (f && f.id !== 'quiz-card') f.classList.toggle('flip');
  });

  // gekend
  var known = store.get('cl-known', []);
  function renderKnown() {
    $$('[data-known]').forEach(function (b) {
      var on = known.indexOf(b.dataset.known) > -1;
      b.classList.toggle('on', on);
      b.innerHTML = on ? '<span class="ic">✓</span> Gekend' : '<span class="ic">○</span> Markeer als gekend';
    });
    $$('.nav-f').forEach(function (a) { a.classList.toggle('known', known.indexOf(a.dataset.id) > -1); });
    var total = $$('.nav-f').length;
    $$('[data-progress]').forEach(function (p) {
      var sid = p.dataset.progress;
      var items = $$('.nav-f[data-id^="' + sid + '-"]');
      var k = items.filter(function (a) { return a.classList.contains('known'); }).length;
      p.textContent = k + '/' + items.length;
      var bar = $('[data-bar="' + sid + '"]');
      if (bar) bar.style.width = (items.length ? 100 * k / items.length : 0) + '%';
    });
    if (total) {
      var k = $$('.nav-f.known').length;
      var pct = Math.round(100 * k / total);
      var ring = $('#ring');
      if (ring) ring.style.strokeDashoffset = 97.4 * (1 - pct / 100);
      var rt = $('#ring-t'); if (rt) rt.textContent = pct + '%';
      var sk = $('[data-stat="known"]'); if (sk) sk.textContent = k;
    }
  }
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-known]');
    if (!b) return;
    var id = b.dataset.known, i = known.indexOf(id);
    if (i > -1) known.splice(i, 1); else known.push(id);
    store.set('cl-known', known);
    renderKnown();
  });
  renderKnown();

  // ---------------- alleen in de studiegids (app) ----------------
  // ---------- vergroten: knop op elke visual opent een tijdelijk venster ----------
  var zoomBox = null, zoomFrom = null;
  function closeZoom() {
    if (!zoomBox) return;
    zoomBox.remove(); zoomBox = null;
    document.body.classList.remove('zoomed');
    if (zoomFrom) zoomFrom.focus();
  }
  function openZoom(fig, btn) {
    closeZoom();
    zoomFrom = btn;
    var svg = $('svg', fig), cap = $('figcaption', fig);
    zoomBox = document.createElement('div');
    zoomBox.className = 'zoom-overlay';
    zoomBox.innerHTML = '<div class="zoom-win" role="dialog" aria-modal="true" aria-label="Vergrote visual">' +
      '<div class="zoom-head"><b></b><button type="button" class="icon-btn" data-zoom-close aria-label="Sluiten">✕</button></div>' +
      '<div class="zoom-body"></div><p class="zoom-cap"></p></div>';
    $('b', zoomBox).textContent = svg.getAttribute('aria-label') || '';
    $('.zoom-body', zoomBox).appendChild(svg.cloneNode(true));
    if (cap && cap.textContent.trim()) $('.zoom-cap', zoomBox).innerHTML = cap.innerHTML; else $('.zoom-cap', zoomBox).remove();
    zoomBox.addEventListener('click', function (ev) {
      if (ev.target === zoomBox || ev.target.closest('[data-zoom-close]')) closeZoom();
    });
    document.body.appendChild(zoomBox);
    document.body.classList.add('zoomed');
    $('[data-zoom-close]', zoomBox).focus();
  }
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-zoom]');
    if (b) openZoom(b.closest('figure'), b);
  });
  document.addEventListener('keydown', function (ev) {
    if (zoomBox && ev.key === 'Escape') { ev.preventDefault(); closeZoom(); }
  }, true);

  if (!document.body.classList.contains('app')) return;
  var fiches = $$('.fiche');
  var ids = fiches.map(function (f) { return f.id; });
  var sc = $('[data-stat="cards"]'); if (sc) sc.textContent = $$('.fiche .flash').length;

  function show(id) {
    var target = id || 'home';
    var isFiche = ids.indexOf(target) > -1;
    if (!isFiche && target !== 'quiz') target = 'home';
    $$('.view').forEach(function (v) { v.classList.toggle('on', v.id === target); });
    fiches.forEach(function (f) { f.classList.toggle('on', f.id === target); });
    $$('.nav-f, .nav-top').forEach(function (a) { a.classList.toggle('on', a.dataset.id === target); });
    var pager = $('.pager');
    pager.classList.toggle('hidden', !isFiche);
    if (isFiche) {
      var i = ids.indexOf(target);
      var prev = $('[data-prev]'), next = $('[data-next]');
      prev.href = '#' + (ids[i - 1] || ''); prev.classList.toggle('off', i === 0);
      next.href = '#' + (ids[i + 1] || ''); next.classList.toggle('off', i === ids.length - 1);
      $('[data-pos]').textContent = (i + 1) + ' / ' + ids.length;
      var active = $('.nav-f.on');
      if (active) {
        active.closest('.nav-sec').classList.remove('closed');
        active.scrollIntoView({ block: 'nearest' });
      }
      document.title = target.toUpperCase() + ' · ' + $('#' + target).dataset.titel;
    } else {
      document.title = 'CureLytics – studiegids';
    }
    if (target === 'quiz') startQuiz();
    document.body.classList.remove('menu');
    window.scrollTo(0, 0);
  }
  function route() {
    var h = location.hash.slice(1);
    // ankers binnen een fiche (bv. bi-003-praktijk) → open fiche en scroll
    var base = h.match(/^([a-z]+-\d{3})-/);
    if (base && ids.indexOf(base[1]) > -1) {
      if (!$('#' + base[1]).classList.contains('on')) show(base[1]);
      var el = document.getElementById(h);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
      return;
    }
    show(h);
  }
  window.addEventListener('hashchange', route);
  route();

  // sectie in-/uitklappen
  $$('.nav-h').forEach(function (h) {
    h.addEventListener('click', function () { h.parentNode.classList.toggle('closed'); });
  });
  $('.menu-btn').addEventListener('click', function () { document.body.classList.toggle('menu'); });

  // zijbalk in-/uitklappen (desktop), onthouden per browser
  function setSide(closed) {
    document.body.classList.toggle('side-closed', closed);
    store.set('cl-side-closed', closed);
  }
  if (store.get('cl-side-closed', false)) document.body.classList.add('side-closed');
  $$('[data-side-toggle]').forEach(function (b) {
    b.addEventListener('click', function () { setSide(!document.body.classList.contains('side-closed')); });
  });

  // zoeken
  var q = $('#q');
  q.addEventListener('input', function () {
    var term = q.value.trim().toLowerCase();
    $$('.nav-f').forEach(function (a) { a.classList.toggle('hide', term && a.dataset.search.indexOf(term) === -1); });
    $$('.nav-sec').forEach(function (s) {
      if (term) s.classList.toggle('closed', !$$('.nav-f:not(.hide)', s).length);
    });
  });

  // ---------------- quiz ----------------
  var deck = [], pos = 0, filter = 'alle';
  var qc = $('#quiz-card');
  function startQuiz() {
    deck = $$('.fiche .flash').filter(function (f) {
      return filter === 'alle' || f.dataset.fiche.indexOf(filter + '-') === 0;
    }).filter(function (f) {
      return known.indexOf(f.dataset.fiche) === -1 || filter !== 'alle';
    }).map(function (f) { return { q: f.dataset.q, a: f.dataset.a, src: f.dataset.fiche }; });
    for (var i = deck.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = deck[i]; deck[i] = deck[j]; deck[j] = t; }
    pos = 0; drawQuiz();
  }
  function drawQuiz() {
    qc.classList.remove('flip');
    var card = deck[pos];
    $('.quiz-progress i').style.width = (deck.length ? 100 * pos / deck.length : 100) + '%';
    if (!card) {
      $('.qq').textContent = deck.length ? 'Klaar! Alles doorlopen 🎉' : 'Geen kaarten in deze selectie.';
      $('.qa').textContent = 'Kies een andere map of start opnieuw.';
      $('.quiz-count').textContent = '';
      return;
    }
    $('.qq').textContent = card.q;
    $('.qa').textContent = card.a;
    $('.quiz-count').textContent = 'Kaart ' + (pos + 1) + ' van ' + deck.length + ' · uit ' + card.src.toUpperCase();
    $('[data-qsrc]').href = '#' + card.src;
  }
  qc.addEventListener('click', function () { qc.classList.toggle('flip'); });
  $$('[data-qa]').forEach(function (b) {
    b.addEventListener('click', function () { answer(b.dataset.qa); });
  });
  function answer(kind) {
    if (!deck[pos]) return startQuiz();
    if (kind === 'again') deck.push(deck[pos]);
    pos++; drawQuiz();
  }
  $$('[data-qf]').forEach(function (b) {
    b.addEventListener('click', function () {
      filter = b.dataset.qf;
      $$('[data-qf]').forEach(function (x) { x.classList.toggle('on', x === b); });
      startQuiz();
    });
  });

  // toetsenbord
  document.addEventListener('keydown', function (ev) {
    if (zoomBox) return;
    if (ev.target.matches('input, textarea')) { if (ev.key === 'Escape') ev.target.blur(); return; }
    if (ev.key === '/') {
      ev.preventDefault();
      if (document.body.classList.contains('side-closed')) setSide(false);
      q.focus(); return;
    }
    if (ev.key === '[') { setSide(!document.body.classList.contains('side-closed')); return; }
    var inQuiz = $('#quiz').classList.contains('on');
    if (inQuiz) {
      if (ev.key === ' ') { ev.preventDefault(); qc.classList.toggle('flip'); }
      if (ev.key === 'ArrowRight') answer('know');
      if (ev.key === 'ArrowLeft') answer('again');
      return;
    }
    var cur = ids.indexOf(location.hash.slice(1));
    if (cur < 0) return;
    if (ev.key === 'ArrowRight' && ids[cur + 1]) location.hash = ids[cur + 1];
    if (ev.key === 'ArrowLeft' && ids[cur - 1]) location.hash = ids[cur - 1];
  });
})();
