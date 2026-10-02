(() => {
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];

  // navigácia
  const nav = $('#nav'), burger = $('#burger');
  const onScroll = () => nav.classList.toggle('is-solid', scrollY > 20);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const setMenu = open => { nav.classList.toggle('is-open', open); burger.setAttribute('aria-expanded', open); document.body.style.overflow = open ? 'hidden' : ''; };
  burger.addEventListener('click', () => setMenu(!nav.classList.contains('is-open')));
  $$('#menu a').forEach(a => a.addEventListener('click', () => setMenu(false)));

  // jemné objavenie pri skrolovaní
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  $$('.fi').forEach(el => {
    const sib = [...el.parentElement.children].filter(c => c.classList.contains('fi'));
    const idx = sib.indexOf(el); if (idx > 0) el.style.transitionDelay = Math.min(idx, 4) * 0.09 + 's';
    io.observe(el);
  });

  // galéria – filter, ďalšie, lightbox
  const items = $$('.gi'), more = $('#more'), LIMIT = 12;
  let filter = 'all', showAll = false;
  const visible = () => items.filter(i => filter === 'all' || i.dataset.k === filter);
  const render = () => {
    const vis = visible();
    items.forEach(i => { i.classList.add('is-hidden'); i.classList.remove('pop'); });
    vis.forEach((i, n) => {
      if (!(showAll || n < LIMIT)) return;
      i.classList.remove('is-hidden'); void i.offsetWidth; i.classList.add('pop');
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
  items.forEach(g => g.addEventListener('click', () => { list = items.filter(i => !i.classList.contains('is-hidden')); show(list.indexOf(g)); lb.hidden = false; document.body.style.overflow = 'hidden'; }));
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
