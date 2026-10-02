(() => {
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const KAT = {"domov": ["Garážové brány", "Vstupné brány a pohony", "Okná a dvere", "Exteriérové tienenie", "Pergoly a markízy", "Interiérové tienenie", "Siete proti hmyzu", "Inteligentné ovládanie"], "firma": ["Priemyselné sekčné brány", "Rýchlobežné brány", "Požiarne uzávery", "Nakladacia technika", "Vjazdové systémy", "Bezpečnostné mreže"], "servis": ["Garážová brána", "Vstupná brána / pohon", "Okná a dvere", "Tienenie", "Priemyselná brána", "Iné"]};

  // nadpis – slová postupne
  const h1 = $('[data-words]');
  if (h1) {
    let i = 0;
    const wrap = node => [...node.childNodes].forEach(n => {
      if (n.nodeType !== 3) return wrap(n);
      const frag = document.createDocumentFragment();
      n.textContent.split(/([ \n]+)/).forEach(t => {
        if (!t) return;
        if (/^[ \n]+$/.test(t)) { frag.append(' '); return; }
        const w = document.createElement('span'); w.className = 'w';
        const s = document.createElement('span'); s.textContent = t; s.style.animationDelay = (.1 + i++ * .06) + 's';
        w.append(s); frag.append(w);
      });
      n.replaceWith(frag);
    });
    wrap(h1);
  }

  // navigácia
  const nav = $('#nav'), burger = $('#burger');
  const onScroll = () => nav.classList.toggle('is-solid', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const closeMenu = () => { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; };
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open); document.body.style.overflow = open ? 'hidden' : '';
  });
  $$('#menu a').forEach(a => a.addEventListener('click', closeMenu));

  // odhalenie pri skrolovaní
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  $$('.rv').forEach(el => {
    const sib = [...el.parentElement.children].filter(c => c.classList.contains('rv'));
    const idx = sib.indexOf(el); if (idx > 0) el.style.transitionDelay = Math.min(idx, 5) * .07 + 's';
    io.observe(el);
  });

  // pre domov – záložky
  const tabs = $$('[role="tab"]');
  const pick = t => {
    tabs.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
      const p = $('#' + x.getAttribute('aria-controls')); p.hidden = !on; p.classList.toggle('is-on', on); });
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => pick(t));
    t.addEventListener('keydown', e => {
      const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key]; if (!d) return;
      e.preventDefault(); const n = tabs[(i + d + tabs.length) % tabs.length]; pick(n); n.focus();
    });
  });

  // realizácie – filter
  $$('.real__f button').forEach(b => b.addEventListener('click', () => {
    $$('.real__f button').forEach(x => x.classList.toggle('is-on', x === b));
    $$('.case').forEach(c => c.classList.toggle('is-hidden', b.dataset.f !== 'all' && c.dataset.k !== b.dataset.f));
  }));

  // dopytový formulár – oblasť → produkty
  const kat = $('#kat'), katL = $('#kat-l'), msgL = $('#msg-l');
  const fillKat = (oblast, vyber) => {
    const list = KAT[oblast].concat(oblast === 'servis' ? [] : ['Neviem – nechám si poradiť']);
    if (vyber && !list.includes(vyber)) list.unshift(vyber);
    kat.innerHTML = list.map(t => `<label><input type="radio" name="kat" value="${t}"${t === vyber ? ' checked' : ''}><span>${t}</span></label>`).join('');
    katL.textContent = oblast === 'servis' ? 'Čoho sa servis týka?' : 'O aký produkt ide?';
    msgL.textContent = oblast === 'servis' ? 'Čo sa deje? Typ výrobku, kedy bol namontovaný…' : oblast === 'firma' ? 'Typ prevádzky, rozmery otvorov, počet kusov, termín…' : 'Rozmery, počet kusov, farba, otázky…';
  };
  const setOblast = (oblast, vyber) => { const r = $(`#seg input[value="${oblast}"]`); if (r) r.checked = true; fillKat(oblast, vyber); };
  $$('#seg input').forEach(r => r.addEventListener('change', () => fillKat(r.value)));
  $$('[data-typ]').forEach(a => a.addEventListener('click', () => setOblast(a.dataset.typ, a.dataset.kat)));
  $$('a[href="#servis"].door').forEach(a => a.addEventListener('click', () => setOblast('servis')));
  fillKat('domov');
  $('#dopyt').addEventListener('submit', e => { e.preventDefault(); $('#formok').hidden = false; });
})();
