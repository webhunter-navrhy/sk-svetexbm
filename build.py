"""Zostaví index.html + style.css s cache bustingom (?v=hash). Obsah je zo svetexbm.sk (podklady/web)."""
import hashlib, json
from pathlib import Path
D = Path(__file__).parent

# id, názov, typy (z dopytového formulára na svetexbm.sk), obrázok, počet fotiek v ich galérii, krátky popis
PRODUKTY = [
    ('brany', 'Garážové brány', ['Sekčné', 'Posuvné', 'Dvojkrídlové', 'Rolovacie', 'Rýchlobežné', 'Priemyselné'], 't-165.jpg', 109,
     'Pre rodinné domy od Lomaxu, pre priemysel od Alfa portas.'),
    ('okna', 'Okná a dvere', ['Plastové', 'Hliníkové', 'Drevené', 'Drevo-hliníkové', 'Plast-hliníkové'], 't-115.jpg', 30,
     'Vyrábané presne na mieru, vrátane montáže a servisu.'),
    ('exter', 'Tienenie exteriérové', ['Exteriérové žalúzie', 'Rolety', 'Screenové rolety', 'Markízy', 'Pergoly', 'Tienenie pre strešné okná'], 't-289.jpg', 71,
     'Proti prehriatiu domu, na úsporu energií aj pre súkromie.'),
    ('inter', 'Tienenie interiérové', ['Plisé', 'Roletky deň / noc', 'Klasické roletky', 'Rímske rolety', 'Japonské steny', 'Bambusové a drevené žalúzie', 'Horizontálne žalúzie', 'Vertikálne žalúzie', 'Garniže a koľajnice', 'Tienenie pre strešné okná'], 'duette.jpg', 162,
     'Pre každý štýl interiéru, šité na mieru.'),
    ('siete', 'Siete proti hmyzu', ['Pevné siete', 'Krídlové siete', 'Plisované siete', 'Posuvné siete', 'Rolovacie siete'], 't-421.jpg', 29,
     'Vetrajte bez nezvaných návštevníkov, aj bez vŕtania do rámu.'),
    ('somfy', 'Inteligentná domácnosť SOMFY', ['Rolety a žalúzie', 'Garážová brána', 'Vstupná brána'], 'somfy.jpg', 0,
     'Celú domácnosť ovládate jedným klikom v mobile. Sme expert partner Somfy.'),
    ('vjazd', 'Vjazdové systémy', ['Vstupné brány a pohony', 'Vjazdové závory', 'Dopravné stĺpy', 'Parkovacie systémy'], 't-158.jpg', 27,
     'Pre súkromné pozemky aj parkoviská, od Somfy a FAAC.'),
    ('naklad', 'Nakladacia technika', ['Predsadené nakladacie komory', 'Vyrovnávacie mostíky', 'Tesniace límce'], 'dock.jpg', 0,
     'Bezpečné nakladanie a menšie tepelné straty na rampe.'),
    ('mreze', 'Bezpečnostné mreže', ['Pevné', 'Rolovacie', 'Rozťahovacie'], 'mreza.jpg', 4,
     'Pre domy, chaty aj firemné prevádzky.'),
    ('poziar', 'Požiarne uzávery', ['Textilné', 'Rolovacie', 'Sekčné', 'Posuvné', 'Krídlové'], 'poziar.jpg', 0,
     'Certifikované podľa EN 13501-2, až do E 240, EW 120 a EI 120.'),
]
NAZOV_GAL = {'brany': 'Garážová brána', 'okna': 'Okná a dvere', 'exter': 'Exteriérové tienenie', 'inter': 'Interiérové tienenie',
             'siete': 'Sieť proti hmyzu', 'vjazd': 'Vjazdový systém', 'mreze': 'Bezpečnostná mreža'}
# výpredaj zo svetexbm.sk/vypredaj (ceny bez DPH)
VYPREDAJ = [
    ('Vchodové dvere', 'Salamander bluEvolution 82MD – RI OKNA', '1000 × 2325 mm · dub Montana, mliečne sklo', 2465, 1035, 58),
    ('Sekčná garážová brána', 'Delta – Lomax', '2550 × 2090 mm · biela / antracit · s pohonom MARANTEC', 1716, 858, 50),
    ('Balkónové dvere', 'RI Optimal line 3D – RI OKNA', '850 × 2430 mm · biela / biela', 640, 224, 65),
    ('Dvojkrídlové plastové okno', 'RI Optimal line 2D – RI OKNA', '1390 × 1345 mm · biela / zlatý dub', 442, 199, 55),
]

eur = lambda v: f'{v:,}'.replace(',', ' ') + ' €'

lamely = ''.join(f'<i style="--i:{i}"></i>' for i in range(10))

mq_items = [p[1] for p in PRODUKTY]
marquee = ''.join(f'<span>{t}</span><b>✦</b>' for t in mq_items) * 2

produkty = '\n'.join(
    f'''      <li class="prow rv" data-img="img/{img}">
        <span class="prow__n">{i:02d}</span>
        <div class="prow__m">
          <h3>{nazov}</h3>
          <p>{popis}</p>
          <ul class="prow__t">{''.join(f'<li>{t}</li>' for t in typy[:6])}{f'<li>+ {len(typy) - 6}</li>' if len(typy) > 6 else ''}</ul>
        </div>
        <img class="prow__img" src="img/{img}" alt="" loading="lazy">
        <div class="prow__a">
          {f'<a href="#realizacie" data-gf="{pid}" class="prow__g">{cnt} fotiek realizácií</a>' if cnt else ''}
          <a href="#dopyt" data-kat="{pid}" class="prow__c">Chcem ponuku <span aria-hidden="true">→</span></a>
        </div>
      </li>''' for i, (pid, nazov, typy, img, cnt, popis) in enumerate(PRODUKTY, 1))

kategorie = ''.join(
    f'<label class="chip"><input type="radio" name="kat" value="{pid}" data-typy="{"|".join(typy)}"><span>{nazov}</span></label>'
    for pid, nazov, typy, *_ in PRODUKTY)

vypredaj = '\n'.join(
    f'''      <article class="scard rv">
        <span class="scard__z">−{z} %</span>
        <h3>{n}</h3>
        <p class="scard__t">{t}</p>
        <p class="scard__d">{d}</p>
        <p class="scard__p"><s>{eur(p0)}</s><b>{eur(p1)}</b><small>bez DPH</small></p>
        <a href="#dopyt" class="scard__a">Mám záujem <span aria-hidden="true">→</span></a>
      </article>''' for n, t, d, p0, p1, z in VYPREDAJ)

# galéria – kategórie na striedačku, nech je pestrá
meta = json.load(open(D / 'galeria.json'))
po_kat = {}
for n, (k, *_r) in meta.items(): po_kat.setdefault(k, []).append(n)
poradie = []
while any(po_kat.values()):
    for k in ('brany', 'exter', 'okna', 'inter', 'vjazd', 'siete', 'mreze'):
        if po_kat.get(k): poradie.append(po_kat[k].pop(0))
galeria = '\n'.join(
    f'      <figure class="gi" data-k="{meta[n][0]}" data-full="img/g-{n}.jpg"><img src="img/t-{n}.jpg" alt="{NAZOV_GAL[meta[n][0]]} – realizácia Svetex BM" loading="lazy" width="{meta[n][1]}" height="{meta[n][2]}"><figcaption>{NAZOV_GAL[meta[n][0]]}</figcaption></figure>'
    for n in poradie)

css = (D / 'fonts/fonts.css').read_text() + '\n' + (D / 'style.src.css').read_text()
(D / 'style.css').write_text(css)
h = lambda b: hashlib.md5(b).hexdigest()[:8]
html = (D / 'src.html').read_text()
for k, v in dict(lamely=lamely, marquee=marquee, produkty=produkty, kategorie=kategorie, vypredaj=vypredaj, galeria=galeria).items():
    html = html.replace('{{' + k + '}}', v)
html = html.replace('{{css}}', h(css.encode())).replace('{{js}}', h((D / 'main.js').read_bytes()))
assert '{{' not in html
(D / 'index.html').write_text(html)
print('ok', len(poradie), 'fotiek v galérii')
