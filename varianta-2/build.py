"""Varianta 2 (svetlá, pokojná). Zostaví index.html + style.css s cache bustingom (?v=hash).
Obsah je rovnaký ako vo variante 1 (zo svetexbm.sk), obrázky sa berú z ../img/."""
import hashlib, json
from pathlib import Path
D = Path(__file__).parent
ROOT = D.parent

# id, názov, typy, obrázok, počet fotiek v galérii, popis — poradie: najskôr produkty pre domov
PRODUKTY = [
    ('exter', 'Tienenie exteriérové', ['Exteriérové žalúzie', 'Rolety', 'Screenové rolety', 'Markízy', 'Pergoly', 'Tienenie pre strešné okná'], 't-289.jpg', 71,
     'Proti prehriatiu domu, na úsporu energií aj pre súkromie.'),
    ('inter', 'Tienenie interiérové', ['Plisé', 'Roletky deň / noc', 'Klasické roletky', 'Rímske rolety', 'Japonské steny', 'Bambusové a drevené žalúzie', 'Horizontálne žalúzie', 'Vertikálne žalúzie', 'Garniže a koľajnice', 'Tienenie pre strešné okná'], 'duette.jpg', 162,
     'Pre každý štýl interiéru, šité na mieru.'),
    ('okna', 'Okná a dvere', ['Plastové', 'Hliníkové', 'Drevené', 'Drevo-hliníkové', 'Plast-hliníkové'], 't-115.jpg', 30,
     'Vyrábané presne na mieru, vrátane montáže a servisu.'),
    ('brany', 'Garážové brány', ['Sekčné', 'Posuvné', 'Dvojkrídlové', 'Rolovacie', 'Rýchlobežné', 'Priemyselné'], 'hero.jpg', 109,
     'Pre rodinné domy od Lomaxu, pre priemysel od Alfa portas.'),
    ('siete', 'Siete proti hmyzu', ['Pevné siete', 'Krídlové siete', 'Plisované siete', 'Posuvné siete', 'Rolovacie siete'], 't-418.jpg', 29,
     'Vetrajte bez nezvaných návštevníkov, aj bez vŕtania do rámu.'),
    ('somfy', 'Inteligentná domácnosť SOMFY', ['Rolety a žalúzie', 'Garážová brána', 'Vstupná brána'], 'somfy.jpg', 0,
     'Celú domácnosť ovládate jedným klikom v mobile. Sme expert partner Somfy.'),
    ('vjazd', 'Vjazdové systémy', ['Vstupné brány a pohony', 'Vjazdové závory', 'Dopravné stĺpy', 'Parkovacie systémy'], 't-158.jpg', 27,
     'Pre súkromné pozemky aj parkoviská, od Somfy a FAAC.'),
    ('mreze', 'Bezpečnostné mreže', ['Pevné', 'Rolovacie', 'Rozťahovacie'], 'mreza.jpg', 4,
     'Pre domy, chaty aj firemné prevádzky.'),
    ('naklad', 'Nakladacia technika', ['Predsadené nakladacie komory', 'Vyrovnávacie mostíky', 'Tesniace límce'], 'dock.jpg', 0,
     'Bezpečné nakladanie a menšie tepelné straty na rampe.'),
    ('poziar', 'Požiarne uzávery', ['Textilné', 'Rolovacie', 'Sekčné', 'Posuvné', 'Krídlové'], 'poziar.jpg', 0,
     'Certifikované podľa EN 13501-2, až do E 240, EW 120 a EI 120.'),
]
NAZOV_GAL = {'brany': 'Garážová brána', 'okna': 'Okná a dvere', 'exter': 'Exteriérové tienenie', 'inter': 'Interiérové tienenie',
             'siete': 'Sieť proti hmyzu', 'vjazd': 'Vjazdový systém', 'mreze': 'Bezpečnostná mreža'}
VYPREDAJ = [
    ('Vchodové dvere', 'Salamander bluEvolution 82MD – RI OKNA', '1000 × 2325 mm · dub Montana, mliečne sklo', 2465, 1035, 58),
    ('Sekčná garážová brána', 'Delta – Lomax', '2550 × 2090 mm · biela / antracit · s pohonom MARANTEC', 1716, 858, 50),
    ('Balkónové dvere', 'RI Optimal line 3D – RI OKNA', '850 × 2430 mm · biela / biela', 640, 224, 65),
    ('Dvojkrídlové plastové okno', 'RI Optimal line 2D – RI OKNA', '1390 × 1345 mm · biela / zlatý dub', 442, 199, 55),
]
# galéria – najskôr najkrajšie domy, terasy a interiéry, potom zvyšok
NAJSKOR = [304, 17, 421, 87, 306, 289, 93, 63, 264, 115, 82, 272, 281, 241, 86, 259, 418, 165, 121, 286, 35, 222, 37, 158]

eur = lambda v: f'{v:,}'.replace(',', '&nbsp;') + '&nbsp;€'
nb = lambda s: s.replace(' a ', ' a&nbsp;').replace(' v ', ' v&nbsp;').replace(' s ', ' s&nbsp;').replace(' z ', ' z&nbsp;').replace(' o ', ' o&nbsp;')


def pcard(i, pid, nazov, typy, img, cnt, popis):
    big = i < 2
    return f'''      <article class="pcard{' pcard--big' if big else ''} fi">
        <a href="#dopyt" data-kat="{pid}" class="pcard__img" tabindex="-1" aria-hidden="true"><img src="../img/{img}" alt="" loading="lazy"></a>
        <div class="pcard__b">
          <h3>{nazov}</h3>
          <p class="pcard__p">{nb(popis)}</p>
          <p class="pcard__t">{' · '.join(typy)}</p>
          <div class="pcard__a">
            <a href="#dopyt" data-kat="{pid}" class="lnk">Cenová ponuka</a>
            {f'<a href="#realizacie" data-gf="{pid}" class="pcard__g">{cnt} fotiek</a>' if cnt else ''}
          </div>
        </div>
      </article>'''


produkty = '\n'.join(pcard(i, *p) for i, p in enumerate(PRODUKTY))

kategorie = ''.join(
    f'<label class="chip"><input type="radio" name="kat" value="{pid}" data-typy="{"|".join(typy)}"><span>{nazov}</span></label>'
    for pid, nazov, typy, *_ in PRODUKTY)

vypredaj = '\n'.join(
    f'''      <article class="sitem fi">
        <p class="sitem__z">−{z}&nbsp;%</p>
        <h3>{n}</h3>
        <p class="sitem__t">{t}</p>
        <p class="sitem__d">{d}</p>
        <p class="sitem__p"><s>{eur(p0)}</s><b>{eur(p1)}</b><small>bez DPH</small></p>
        <a href="#dopyt" class="lnk">Mám záujem</a>
      </article>''' for n, t, d, p0, p1, z in VYPREDAJ)

meta = json.load(open(ROOT / 'galeria.json'))
poradie = [str(n) for n in NAJSKOR] + [n for n in meta if int(n) not in NAJSKOR]
assert len(set(poradie)) == len(meta) and all(n in meta for n in poradie)
galeria = '\n'.join(
    f'      <figure class="gi" data-k="{meta[n][0]}" data-full="../img/g-{n}.jpg"><img src="../img/t-{n}.jpg" alt="{NAZOV_GAL[meta[n][0]]} – realizácia Svetex BM" loading="lazy" width="{meta[n][1]}" height="{meta[n][2]}"><figcaption>{NAZOV_GAL[meta[n][0]]}</figcaption></figure>'
    for n in poradie)

css = (D / 'fonts/fonts.css').read_text() + '\n' + (D / 'style.src.css').read_text()
(D / 'style.css').write_text(css)
h = lambda b: hashlib.md5(b).hexdigest()[:8]
html = (D / 'src.html').read_text()
for k, v in dict(produkty=produkty, kategorie=kategorie, vypredaj=vypredaj, galeria=galeria).items():
    html = html.replace('{{' + k + '}}', v)
html = html.replace('{{css}}', h(css.encode())).replace('{{js}}', h((D / 'main.js').read_bytes()))
assert '{{' not in html
(D / 'index.html').write_text(html)
print('ok', len(poradie), 'fotiek v galérii')
