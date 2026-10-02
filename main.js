(() => {
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];

  // hero – slová postupne (po otvorení lamiel)
  const h1 = $('[data-words]');
  if (h1) {
    let i = 0;
    const wrap = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(t => {
          if (!t) return;
          if (/^\s+$/.test(t)) { frag.append(' '); return; }
          const w = document.createElement('span'); w.className = 'w';
          const s = document.createElement('span'); s.textContent = t; s.style.animationDelay = (1.6 + i++ * 0.07) + 's';
          w.append(s); frag.append(w);
        });
        n.replaceWith(frag);
      } else wrap(n);
    });
    wrap(h1);
  }

  // navigácia
  const nav = $('#nav'), hero = $('.hero');
  const onScroll = () => nav.classList.toggle('is-solid', scrollY > (hero ? hero.offsetHeight - 90 : 40));
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const burger = $('#burger');
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open); document.body.style.overflow = open ? 'hidden' : '';
  });
  $$('#menu a').forEach(a => a.addEventListener('click', () => { nav.classList.remove('is-open'); document.body.style.overflow = ''; }));

  // reveal
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -10% 0px' });
  $$('.rv, .clip').forEach(el => {
    const sib = el.parentElement ? [...el.parentElement.children].filter(c => c.classList.contains('rv')) : [];
    const idx = sib.indexOf(el); if (idx > 0) el.style.transitionDelay = Math.min(idx, 5) * 0.08 + 's';
    io.observe(el);
  });

  // počítadlá
  const fmt = n => n.toLocaleString('sk-SK').replace(/ /g, ' ');
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return; cio.unobserve(e.target);
    const el = e.target, to = +el.dataset.count, t0 = performance.now(), d = 1800;
    const step = t => { const p = Math.min(1, (t - t0) / d); el.textContent = fmt(Math.round(to * (1 - Math.pow(1 - p, 4)))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  }), { threshold: .6 });
  $$('[data-count]').forEach(el => { el.textContent = '0'; cio.observe(el); });

  // produkty – náhľad fotky pri kurzore
  const pv = $('#ppv'), pvi = pv && $('img', pv);
  if (pv && matchMedia('(hover:hover) and (min-width:961px)').matches) {
    let x = 0, y = 0, cx = 0, cy = 0, raf = 0, on = false;
    const loop = () => { cx += (x - cx) * .16; cy += (y - cy) * .16; pv.style.transform = `translate(${cx}px,${cy}px)`;
      raf = (on || Math.abs(x - cx) > .5 || Math.abs(y - cy) > .5) ? requestAnimationFrame(loop) : 0; };
    $$('.prow').forEach(r => {
      r.addEventListener('mouseenter', e => { pvi.src = r.dataset.img; on = true; pv.classList.add('is-on'); x = e.clientX + 230; y = e.clientY; if (!cx) { cx = x; cy = y; } if (!raf) raf = requestAnimationFrame(loop); });
      r.addEventListener('mousemove', e => { if (e.target.closest('.prow__a')) { pv.classList.remove('is-on'); return; } pv.classList.add('is-on'); x = e.clientX + 230; y = e.clientY; if (!raf) raf = requestAnimationFrame(loop); });
      r.addEventListener('mouseleave', () => { on = false; pv.classList.remove('is-on'); });
    });
  }

  // galéria – filter, viac, lightbox
  const items = $$('.gi'), more = $('#more'), LIMIT = 14;
  let filter = 'all', showAll = false;
  const visible = () => items.filter(i => filter === 'all' || i.dataset.k === filter);
  const render = () => {
    const vis = visible();
    items.forEach(i => { i.classList.remove('is-in', 'big', 'tall'); i.classList.add('is-hidden'); });
    vis.forEach((i, n) => {
      if (!(showAll || n < LIMIT)) return;
      i.classList.remove('is-hidden');
      const img = $('img', i), portrait = img.height > img.width * 1.05;
      if (portrait) i.classList.add('tall'); else if (n % 7 === 0) i.classList.add('big');
      void i.offsetWidth; i.classList.add('is-in'); i.style.animationDelay = (n % LIMIT) * 0.03 + 's';
    });
    more.parentElement.hidden = showAll || vis.length <= LIMIT;
  };
  const setFilter = f => { filter = f; showAll = false; $$('.filters button').forEach(x => x.classList.toggle('is-on', x.dataset.f === f)); render(); };
  $$('.filters button').forEach(b => b.addEventListener('click', () => setFilter(b.dataset.f)));
  $$('[data-gf]').forEach(a => a.addEventListener('click', () => setFilter(a.dataset.gf)));
  more.addEventListener('click', () => { showAll = true; render(); });
  render();

  const lb = $('#lb'), lbimg = $('#lbimg'), lbcap = $('#lbcap'); let cur = 0, list = [];
  const show = n => { cur = (n + list.length) % list.length; const g = list[cur]; lbimg.src = g.dataset.full; lbimg.alt = $('img', g).alt; lbcap.textContent = $('figcaption', g).textContent + '  ·  ' + (cur + 1) + ' / ' + list.length; };
  items.forEach(g => g.addEventListener('click', () => { list = visible().filter(i => !i.classList.contains('is-hidden')); show(list.indexOf(g)); lb.hidden = false; document.body.style.overflow = 'hidden'; }));
  const close = () => { lb.hidden = true; document.body.style.overflow = ''; };
  $('#lbx').addEventListener('click', close);
  lb.addEventListener('click', e => { if (e.target === lb) close(); });
  $('#lbp').addEventListener('click', () => show(cur - 1));
  $('#lbn').addEventListener('click', () => show(cur + 1));
  addEventListener('keydown', e => { if (lb.hidden) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') show(cur - 1); if (e.key === 'ArrowRight') show(cur + 1); });

  // dopytový formulár – podľa produktu sa ukážu typy
  const typ = $('#typ');
  const pickKat = inp => {
    const typy = inp.dataset.typy.split('|');
    typ.innerHTML = typy.concat('Neviem – nechám si poradiť').map(t => `<label class="chip"><input type="radio" name="typ" value="${t}"><span>${t}</span></label>`).join('');
    typ.hidden = false;
  };
  $$('#kat input').forEach(inp => inp.addEventListener('change', () => pickKat(inp)));
  $$('[data-kat]').forEach(a => a.addEventListener('click', () => {
    const inp = $(`#kat input[value="${a.dataset.kat}"]`); if (inp) { inp.checked = true; pickKat(inp); }
  }));
  $('#dopyt').addEventListener('submit', e => { e.preventDefault(); $('#formok').hidden = false; });
})();
