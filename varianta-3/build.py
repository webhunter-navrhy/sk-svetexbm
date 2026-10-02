"""Varianta 3 (podľa zadania p. Bendíka 2. 10.): zostaví index.html + style.css s cache bustingom (?v=hash).
Texty sú zo svetexbm.sk (podklady/web), fotky z ich galérie (spracuj_foto.py)."""
import hashlib, json
from pathlib import Path
D = Path(__file__).parent

# Pre domov: id, názov, fotka, popis, možnosti, kde sa hodí
DOMOV = [
    ('brany', 'Garážové brány', 'p-brany',
     'Brány vyrábame presne na mieru otvoru, pre novostavby aj do existujúcej garáže. Vyberiete si povrch, farbu, presklenie aj spôsob ovládania: diaľkový ovládač, kódovú klávesnicu, odtlačok prsta alebo mobil.',
     ['Sekčné', 'Posuvné', 'Dvojkrídlové', 'Rolovacie'], 'Rodinné domy, samostatné garáže, rad garáží'),
    ('vstupne', 'Vstupné brány a pohony', 'p-vstupne',
     'Posuvné aj krídlové brány na pozemok, od manuálnych po plne automatické. Pohon vieme prepojiť s ovládaním garážovej brány aj s inteligentnou domácnosťou.',
     ['Posuvné brány', 'Krídlové brány', 'Pohony Somfy a FAAC', 'GSM ovládanie'], 'Vjazd na pozemok, dvory, areály'),
    ('okna', 'Okná a dvere', 'p-okna',
     'Okná a dvere pre novostavby aj rekonštrukcie, vyrábané na mieru. Poradíme s materiálom, zasklením aj farbou a postaráme sa o montáž a servis.',
     ['Plastové', 'Hliníkové', 'Drevené', 'Drevo-hliníkové', 'Plasto-hliníkové'], 'Domy, byty, chaty'),
    ('exter', 'Exteriérové tienenie', 'p-exter',
     'Exteriérové žalúzie, rolety a screenové rolety chránia dom pred prehrievaním a dávajú súkromie. S motorom a senzormi sa vedia zatiahnuť samé, podľa slnka alebo vetra.',
     ['Exteriérové žalúzie', 'Rolety', 'Screenové rolety', 'Tienenie strešných okien'], 'Južné a západné fasády, veľké presklenia'),
    ('pergoly', 'Pergoly a markízy', 'p-pergoly',
     'Tieň a príjemné miesto na terase. Markízy aj pergoly navrhneme podľa rozmerov terasy a dajú sa ovládať motorom, diaľkovým ovládačom alebo z mobilu.',
     ['Markízy', 'Pergoly', 'Motorické ovládanie', 'Veterný senzor'], 'Terasy, balkóny, záhrady'),
    ('inter', 'Interiérové tienenie', 'p-inter',
     'Plisé, roletky deň/noc, rímske rolety, japonské steny aj žalúzie. Vyrábame ich na mieru oknu vrátane strešných a atypických okien.',
     ['Plisé', 'Roletky deň / noc', 'Rímske rolety', 'Japonské steny', 'Žalúzie', 'Garniže'], 'Obývačky, spálne, podkrovia, kancelárie'),
    ('siete', 'Siete proti hmyzu', 'p-siete',
     'Vetrajte bez nezvaných návštevníkov. Siete vyrobíme na okná, dvere aj strešné okná, aj v prevedení bez vŕtania do rámu.',
     ['Pevné', 'Krídlové', 'Plisované', 'Posuvné', 'Rolovacie'], 'Okná, balkónové a terasové dvere'),
    ('somfy', 'Inteligentné ovládanie', 'p-somfy',
     'Rolety, žalúzie, markízy aj brány ovládate z mobilu alebo podľa scenárov, napríklad jedným tlačidlom pri odchode z domu. Sme expert partner Somfy a systém TaHoma vám nastavíme na mieru.',
     ['Somfy TaHoma', 'Ovládanie z mobilu', 'Scenáre', 'Senzory slnka a vetra'], 'Novostavby aj doplnenie do existujúceho domu'),
]

# Pre firmy: názov, fotka, popis, parametre
FIRMY = [
    ('Priemyselné sekčné brány', 'f-priem-k',
     'Pre haly a sklady s intenzívnou prevádzkou. Vyrábané na mieru otvoru, s presklením alebo dverami v bráne.',
     ['Otváranie indukčnou slučkou alebo radarom', 'Bezpečnostné prvky podľa prevádzky']),
    ('Rýchlobežné brány', 'f-rychlo',
     'Rýchle otváranie šetrí čas obsluhy a znižuje tepelné straty v hale. Fóliové aj špirálové prevedenie.',
     ['Rýchlosť otvárania až 2 m/s', 'Transparentné fólie, vlastná potlač']),
    ('Požiarne uzávery', 'f-poziar',
     'Textilné, rolovacie, sekčné, posuvné aj krídlové uzávery pre haly, logistické centrá, nemocnice, školy či parkovacie domy.',
     ['Klasifikácia podľa EN 13501-2', 'Až E 240, EW 120 a EI 120', 'Napojenie na EPS']),
    ('Nakladacia technika', 'f-naklad',
     'Predsadené nakladacie komory, vyrovnávacie mostíky a tesniace límce pre bezpečné nakladanie a menšie straty tepla.',
     ['Hydraulické aj mechanické mostíky', 'Mechanické aj nafukovacie límce']),
    ('Vjazdové systémy', 'f-vjazd',
     'Závory, dopravné stĺpy a parkovacie systémy pre firemné areály, parkoviská a prístupové cesty.',
     ['Ovládanie ovládačom, aplikáciou alebo GSM', 'Pre súkromný aj priemyselný sektor']),
    ('Bezpečnostné mreže', 'f-mreze',
     'Ochrana prevádzok, obchodov a skladov mimo otváracích hodín, aj pre domy a chaty.',
     ['Pevné, rolovacie, rozťahovacie', 'Na mieru otvoru']),
]

# z loga klientov na svetexbm.sk
KLIENTI = ['Letisko Poprad-Tatry', 'Nemocnica Poprad', 'Mesto Poprad', 'Mesto Kežmarok', 'Aqua city Poprad', 'Chemosvit',
           'Tatravagónka', 'Slovnaft', 'ŽSR', 'NDS', 'Spolbyt Poprad', 'Hotel Borovica – Štrbské Pleso', 'Hrebienok resort', 'Coop Jednota']

# realizácie: kategória, štítok, fotka, názov, riešenie (len to, čo je vidieť na fotke)
REAL = [
    ('firma', 'Firma', 'r-hala', 'Výrobná hala', 'Priemyselné sekčné brány s pásom presklenia po celej dĺžke haly.'),
    ('domov', 'Domácnosť', 'r-markiza', 'Rodinný dom', 'Markíza nad vstupom na terasu, chráni pred slnkom aj dažďom.'),
    ('firma', 'Firma', 'r-polaris', 'Predajňa a showroom', 'Exteriérové žalúzie na presklenej fasáde obchodnej budovy.'),
    ('firma', 'Verejná budova', 'r-hasici', 'Hasičská zbrojnica', 'Sekčná brána v červenej farbe s nápisom na mieru.'),
    ('domov', 'Domácnosť', 'r-dom', 'Drevostavba', 'Exteriérové tienenie na rohovom presklení.'),
    ('firma', 'Firma', 'r-depo', 'Areál s dielňami', 'Rad priemyselných sekčných brán s presklením pre veľké vozidlá.'),
]

VYPREDAJ = [
    ('Vchodové dvere', 'Salamander bluEvolution 82MD – RI OKNA', '1000 × 2325 mm · dub Montana, mliečne sklo', 2465, 1035),
    ('Sekčná garážová brána', 'Delta – Lomax, s pohonom MARANTEC', '2550 × 2090 mm · biela / antracit', 1716, 858),
    ('Balkónové dvere', 'RI Optimal line 3D – RI OKNA', '850 × 2430 mm · biela / biela', 640, 224),
    ('Dvojkrídlové plastové okno', 'RI Optimal line 2D – RI OKNA', '1390 × 1345 mm · biela / zlatý dub', 442, 199),
]

eur = lambda v: f'{v:,}'.replace(',', ' ') + ' €'

domov_tabs = ''.join(
    f'<button role="tab" id="t-{pid}" aria-controls="p-{pid}" aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else " tabindex=\"-1\""}><i>{i + 1:02d}</i>{n}</button>'
    for i, (pid, n, *_r) in enumerate(DOMOV))
domov_panels = '\n'.join(f'''        <div class="panel{' is-on' if i == 0 else ''}" role="tabpanel" id="p-{pid}" aria-labelledby="t-{pid}"{'' if i == 0 else ' hidden'}>
          <figure class="panel__img"><img src="img/{img}.jpg" alt="{n} – realizácia Svetex BM" loading="{'eager' if i == 0 else 'lazy'}"></figure>
          <div class="panel__b">
            <h3>{n}</h3>
            <p>{popis}</p>
            <p class="panel__k">Možnosti</p>
            <ul class="tags">{''.join(f'<li>{m}</li>' for m in moz)}</ul>
            <p class="panel__k">Kde sa hodí</p>
            <p class="panel__w">{kde}</p>
            <div class="panel__a">
              <a href="#kontakt" class="btn btn--o" data-typ="domov" data-kat="{n}">Chcem ponuku <span aria-hidden="true">→</span></a>
              <a href="#domov" class="lnk">Viac o produkte</a>
            </div>
          </div>
        </div>''' for i, (pid, n, img, popis, moz, kde) in enumerate(DOMOV))

firmy = '\n'.join(f'''      <article class="fcard rv">
        <div class="fcard__img"><img src="img/{img}.jpg" alt="{n}" loading="lazy"></div>
        <h3>{n}</h3>
        <p>{popis}</p>
        <ul>{''.join(f'<li>{s}</li>' for s in spec)}</ul>
        <a href="#kontakt" class="lnk lnk--o" data-typ="firma" data-kat="{n}">Dopyt <span aria-hidden="true">→</span></a>
      </article>''' for n, img, popis, spec in FIRMY)

klienti = ''.join(f'<li>{k}</li>' for k in KLIENTI)

realizacie = '\n'.join(f'''      <article class="case rv" data-k="{k}">
        <div class="case__img"><img src="img/{img}.jpg" alt="{n} – {ries}" loading="lazy"><span class="case__tag">{tag}</span></div>
        <h3>{n}</h3>
        <dl>
          <div class="todo"><dt>Potreba</dt><dd>Čo zákazník potreboval – doplníme</dd></div>
          <div><dt>Riešenie</dt><dd>{ries}</dd></div>
          <div class="todo"><dt>Realizácia</dt><dd>Rozsah a priebeh – doplníme</dd></div>
        </dl>
      </article>''' for k, tag, img, n, ries in REAL)

vypredaj = '\n'.join(f'''      <article class="srow rv">
        <div><h3>{n}</h3><p>{t}</p></div>
        <p class="srow__d">{d}</p>
        <p class="srow__p"><s>{eur(p0)}</s><b>{eur(p1)}</b></p>
        <a href="#kontakt" class="lnk" data-typ="domov" data-kat="Výpredaj: {n}">Mám záujem <span aria-hidden="true">→</span></a>
      </article>''' for n, t, d, p0, p1 in VYPREDAJ)

KAT = {'domov': [d[1] for d in DOMOV], 'firma': [f[0] for f in FIRMY],
       'servis': ['Garážová brána', 'Vstupná brána / pohon', 'Okná a dvere', 'Tienenie', 'Priemyselná brána', 'Iné']}

css = (D / 'fonts/fonts.css').read_text() + '\n' + (D / 'style.src.css').read_text()
(D / 'style.css').write_text(css)
js = (D / 'main.src.js').read_text().replace('/*KAT*/null', json.dumps(KAT, ensure_ascii=False))
(D / 'main.js').write_text(js)
h = lambda b: hashlib.md5(b).hexdigest()[:8]
html = (D / 'src.html').read_text()
for k, v in dict(domov_tabs=domov_tabs, domov_panels=domov_panels, firmy=firmy, klienti=klienti,
                 realizacie=realizacie, vypredaj=vypredaj).items():
    html = html.replace('{{' + k + '}}', v)
html = html.replace('{{css}}', h(css.encode())).replace('{{js}}', h(js.encode()))
assert '{{' not in html
(D / 'index.html').write_text(html)
print('ok')
