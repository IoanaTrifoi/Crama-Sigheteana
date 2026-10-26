# -*- coding: utf-8 -*-
"""Generează paginile statice pentru Crama Sigheteană. Rulează: python3 build.py"""
import os, json, html

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(OUT, "images"), exist_ok=True)

PHONE_DISPLAY = "0755 674 569"
PHONE_TEL = "+40755674569"
EMAIL = "cramasigheteana@yahoo.com"
ADDRESS = "Strada Iuliu Maniu, nr. 16, Sighetu Marmației, 435500"
MAPS_Q = "Iuliu Maniu 16, Sighetu Marmației 435500"

# ---- Preparate: id, categorie, nume, descriere, fișier imagine -------------
# Numele/descrierile sunt deduse din fotografii; editează-le liber.
DISHES = [
    ("tartar", "aperitive", "Tartar de vită", "Carne tocată fin, gălbenuș, capere, ceapă, castraveți murați, boia și unt.", "tartar.jpg"),
    ("placinte", "aperitive", "Plăcinte prăjite", "Aluat pufos, prăjit auriu, făcute în bucătăria cramei.", "placinte-prajite.jpg"),
    ("fasole", "traditional", "Fasole bătută cu cârnați", "Piure de fasole cu ceapă călită în untură cu boia, murături și cârnați afumați.", "fasole-batuta.jpg"),
    ("chiftele", "traditional", "Chifteluțe în sos de roșii", "Chifteluțe fragede în sos de roșii, cu piure de cartofi și murături.", "chiftele-sos.jpg"),
    ("rulou", "traditional", "Rulou de pui cu șuncă și cașcaval", "Pane crocant, umplut cu șuncă, cașcaval și ardei; cu piure și sos de usturoi.", "rulou-pui.jpg"),
    ("snitel-pui", "traditional", "Șnițel de pui în aluat", "Șnițel auriu, în crustă pufoasă, servit cu piure și roșii.", "snitel-pui-aluat.jpg"),
    ("rosti", "traditional", "Lipii de cartofi cu salată de ouă", "Cartofi răzuiți rumeniți, salată cremoasă cu ouă fierte și boia.", "rosti-salata-oua.jpg"),
    ("pastrav", "gratar", "Păstrăv la grătar", "Păstrăv la grătar cu cartofi fierți cu pătrunjel și lămâie.", "pastrav-cordon.jpg"),
    ("piept-gratar", "gratar", "Piept de pui la grătar", "Piept la grătar cu orez cu legume și salată de varză.", "piept-gratar.jpg"),
    ("cotlet", "gratar", "Cotlet la grătar cu cartofi felii", "Cotlet suculent, cartofi prăjiți felii și sos picant.", "cotlet-cartofi.jpg"),
    ("snitel-pane", "gratar", "Șnițel de porc pane", "Șnițel mare pane, cartofi rustici, varză roșie și sos de usturoi.", "snitel-cartofi.jpg"),
    ("mix", "gratar", "Friptură cu ou ochi", "Friptură cu ou ochi, slănină, ardei copt, cartofi și salată.", "friptura-ou.jpg"),
    ("coaste", "gratar", "Coaste BBQ", "Coaste glazurate în sos BBQ, cu cartofi aurii.", "coaste-bbq-1.jpg"),
    ("snitel-crocant", "gratar", "Șnițele crocante", "Șnițele crocante de porc, cu lămâie și legume proaspete.", "snitel-pane-lamaie.jpg"),
    ("briose", "deserturi", "Brioșe cu fructe de pădure", "Brioșe pufoase cu zmeură și afine.", "briose.jpg"),
    ("casuta", "deserturi", "Prăjitura „Căsuța”", "Prăjitură în formă de căsuță, cu cremă fină, biscuiți și glazură de ciocolată sau frișcă.", "tort-casuta.jpg"),
    ("papanasi", "deserturi", "Papanași", "Papanași cu dulceață de fructe de pădure, smântână și zahăr pudră.", "papanasi.jpg"),
    ("inghetata", "deserturi", "Înghețată pane", "Înghețată în crustă crocantă, cu frișcă, portocală și topping de ciocolată.", "inghetata-pane.jpg"),
    ("parfait", "deserturi", "Parfait cu nucă", "Desert rece cu bucăți de nucă și ciocolată, cu felii de portocală.", "parfait.jpg"),
]
CATS = [("aperitive", "Aperitive"), ("traditional", "Tradițional"), ("gratar", "Grătar & Pește"), ("deserturi", "Deserturi")]
FEATURED = ["fasole", "snitel-pane", "coaste", "pastrav", "papanasi", "chiftele"]

PATTERN = ('<div class="border-ornament" aria-hidden="true"></div>')

def esc(s): return html.escape(s, quote=True)

def head(title, desc, page, schema=True):
    ld = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "Restaurant"],
        "name": "Crama Sigheteană",
        "description": "Restaurant cu mâncare tradițională maramureșeană în Sighetu Marmației, din 2020.",
        "foundingDate": "2020",
        "servesCuisine": ["Românească", "Tradițională", "Maramureșeană"],
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "Strada Iuliu Maniu, nr. 16",
                    "addressLocality": "Sighetu Marmației", "addressRegion": "Maramureș",
                    "postalCode": "435500", "addressCountry": "RO"},
        "hasMenu": "meniu.html",
    }
    return f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#7a3f2e">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="restaurant">
<meta property="og:image" content="images/sala-boltita.jpg">
<link rel="icon" href="images/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=UnifrakturCook:wght@700&family=Nunito+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body data-page="{page}">
'''

def nav(page):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == page else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<header class="site-header">
  <div class="header-inner">
    <button class="burger" aria-label="Meniu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="main-nav" id="main-nav">
      {a("index.html","Acasă","home")}
      {a("meniu.html","Meniu","meniu")}
      {a("despre.html","Despre noi","despre")}
      {a("contact.html","Contact","contact")}
    </nav>
    <a class="logo" href="index.html" aria-label="Crama Sigheteană — acasă">
      <img src="images/logo.jpg" alt="Crama Sigheteană, din 2020" onerror="this.remove()">
      <span class="logo-text">Crama Sigheteană</span>
    </a>
    <a class="btn btn-red header-cta" href="tel:{PHONE_TEL}"><span class="ico">&#9742;</span> Comandă: {PHONE_DISPLAY}</a>
  </div>
  {PATTERN}
</header>
'''

def footer():
    return f'''{PATTERN}
<footer class="site-footer">
  <div class="footer-grid">
    <div>
      <h3 class="blackletter">Crama Sigheteană</h3>
      <p>Mâncare tradițională maramureșeană, din 2020.</p>
    </div>
    <div>
      <h4>Contact</h4>
      <p>{ADDRESS}</p>
      <p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div>
      <h4>Pagini</h4>
      <p><a href="meniu.html">Meniu</a></p>
      <p><a href="despre.html">Despre noi &amp; Cariere</a></p>
      <p><a href="contact.html">Contact &amp; rezervări</a></p>
    </div>
  </div>
  <p class="copy">&copy; <span id="yr">2026</span> Crama Sigheteană · Sighetu Marmației</p>
</footer>
<div class="cart-bar" id="cart-bar" hidden>
  <button id="cart-open" class="btn btn-red">Comanda ta (<span id="cart-count">0</span>)</button>
</div>
<aside class="cart-drawer" id="cart-drawer" aria-hidden="true">
  <div class="cart-head"><h3>Comanda ta</h3><button id="cart-close" aria-label="Închide">&times;</button></div>
  <ul id="cart-list"></ul>
  <p class="cart-note">Trimite lista telefonic sau pe email — confirmăm prețul și timpul de livrare.</p>
  <div class="cart-actions">
    <a class="btn btn-red" href="tel:{PHONE_TEL}">Sună: {PHONE_DISPLAY}</a>
    <a class="btn btn-outline" id="cart-mail" href="mailto:{EMAIL}">Trimite pe email</a>
    <button class="btn btn-outline" id="cart-copy">Copiază lista</button>
    <button class="btn-link" id="cart-clear">Golește</button>
  </div>
</aside>
<div class="lightbox" id="lightbox" hidden><button aria-label="Închide">&times;</button><img alt=""></div>
<script src="script.js"></script>
</body>
</html>
'''

def card(d, show_cart=True):
    id_, cat, name, desc, img = d
    btn = (f'<button class="add-btn" data-id="{id_}" data-name="{esc(name)}">+ Adaugă</button>' if show_cart else "")
    return f'''<article class="dish" data-cat="{cat}">
  <div class="dish-img"><img src="images/{img}" alt="{esc(name)}" loading="lazy" onerror="this.parentNode.classList.add('noimg')"></div>
  <div class="dish-body"><h3>{esc(name)}</h3><p>{esc(desc)}</p>{btn}</div>
</article>'''

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)

# ---------------- ACASĂ ----------------
by_id = {d[0]: d for d in DISHES}
feat = "".join(f'''<article class="feat">
  <div class="feat-img"><img src="images/{by_id[i][4]}" alt="{esc(by_id[i][2])}" loading="lazy" onerror="this.parentNode.classList.add('noimg')"><span class="steam s1"></span><span class="steam s2"></span></div>
  <div class="feat-info"><h3>{esc(by_id[i][2])}</h3><p>{esc(by_id[i][3])}</p></div>
</article>''' for i in FEATURED)

home = head("Crama Sigheteană — Restaurant în Sighetu Marmației | Mâncare tradițională",
            "Restaurant tradițional în Sighetu Marmației: mâncare maramureșeană, cramă cu boltă de cărămidă, livrare mâncare Sighet. Comenzi: 0755 674 569.", "home") + nav("home") + f'''
<main>
<section class="hero">
  <div class="steam-layer" aria-hidden="true"><span class="steam h1"></span><span class="steam h2"></span><span class="steam h3"></span></div>
  <div class="hero-content">
    <p class="kicker">Sighetu Marmației · Din 2020</p>
    <h1 class="blackletter">Gustul Maramureșului,<br>în crama noastră</h1>
    <p class="lead">Mâncare tradițională, gătită cu răbdare, într-o boltă de cărămidă și piatră.</p>
    <div class="hero-actions">
      <a class="btn btn-red" href="tel:{PHONE_TEL}">Comandă acum</a>
      <a class="btn btn-light" href="contact.html#rezervare">Rezervă o masă</a>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-title blackletter">Preparatele casei</h2>
  <p class="section-sub">O alegere din ceea ce se gătește cel mai des la noi.</p>
  <div class="carousel" id="carousel">{feat}</div>
  <p class="center"><a class="btn btn-outline" href="meniu.html">Vezi tot meniul</a></p>
</section>

{PATTERN}
<section class="section split">
  <div class="split-img"><img src="images/sala-boltita.jpg" alt="Sala cu boltă de cărămidă a Cramei Sigheteană" loading="lazy" onerror="this.parentNode.classList.add('noimg')"></div>
  <div class="split-text">
    <h2 class="blackletter">O cramă cu poveste</h2>
    <p>Din 2020, Crama Sigheteană primește oaspeții într-un spațiu cu bolți de cărămidă și pereți de piatră, printre fețe de masă cu motive maramureșene.</p>
    <p>Gătim ca acasă: ciorbe, grătar, preparate tradiționale și deserturi făcute în bucătăria noastră.</p>
    <a class="btn btn-outline" href="despre.html">Povestea noastră</a>
  </div>
</section>

<section class="section menu-day">
  <h2 class="section-title blackletter">Meniul zilei</h2>
  <p class="section-sub">De luni până vineri, supă, ciorbă și fel principal la tablă.</p>
  <p class="center"><a class="btn btn-red" href="meniu.html#meniul-zilei">Vezi meniul zilei</a></p>
</section>
</main>
''' + footer()
write("index.html", home)

# ---------------- MENIU ----------------
tabs = '<button class="tab is-on" data-filter="all">Toate</button>' + "".join(
    f'<button class="tab" data-filter="{k}">{v}</button>' for k, v in CATS) + '<button class="tab" data-filter="zilei">Meniul zilei</button>'
grid = "\n".join(card(d) for d in DISHES)
meniu = head("Meniu — Crama Sigheteană | Restaurant tradițional Sighetu Marmației",
             "Meniul Cramei Sigheteană: aperitive, mâncare tradițională, grătar, deserturi și meniul zilei. Comenzi la 0755 674 569.", "meniu") + nav("meniu") + f'''
<main>
<section class="page-hero"><h1 class="blackletter">Meniu</h1><p>Adaugă preparatele în comandă și trimite-le rapid prin telefon sau email.</p></section>
<div class="tabs-wrap"><div class="tabs" id="tabs">{tabs}</div></div>
<section class="section" id="meniul-zilei-sec" data-block="zilei">
  <h2 class="section-title blackletter" id="meniul-zilei">Meniul zilei</h2>
  <p class="section-sub">Atingeți o imagine pentru a o mări. Meniul se schimbă săptămânal.</p>
  <div class="board-row">
    <figure class="board"><img src="images/meniul-zilei-1.jpg" alt="Meniul zilei, varianta 1" data-zoom loading="lazy" onerror="this.parentNode.classList.add('noimg')"></figure>
    <figure class="board"><img src="images/meniul-zilei-2.jpg" alt="Meniul zilei, varianta 2" data-zoom loading="lazy" onerror="this.parentNode.classList.add('noimg')"></figure>
  </div>
</section>
<section class="section" data-block="dishes">
  <div class="grid" id="grid">
{grid}
  </div>
  <p class="center small">Prețurile se confirmă la comandă. Pentru băuturi și oferte speciale, sunați la <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
</section>
</main>
''' + footer()
write("meniu.html", meniu)

# ---------------- DESPRE ----------------
gal = "".join(f'<figure class="g"><img src="images/{f}" alt="{a}" data-zoom loading="lazy" onerror="this.parentNode.classList.add(\'noimg\')"></figure>' for f, a in [
    ("sala-1.jpg", "Boltă de cărămidă"), ("sala-2.jpg", "Masă lungă în cramă"), ("sala-3.jpg", "Sala principală"), ("sala-4.jpg", "Perete de piatră cu tablou"), ("sala-boltita.jpg", "Sala cu boltă")])
jobs = [
    ("Bucătar / ajutor de bucătar", "Pregătirea preparatelor tradiționale și la grătar, respectarea normelor de igienă. Experiență în bucătărie este un avantaj."),
    ("Ospătar / ospătăriță", "Servirea oaspeților, preluarea comenzilor, o atitudine caldă și atenție la detalii."),
    ("Curier / livrări", "Livrarea comenzilor în Sighetu Marmației. Permis de conducere categoria B."),
]
jobs_html = "".join(f'<details class="job"><summary>{esc(t)}</summary><p>{esc(d)}</p></details>' for t, d in jobs)
despre = head("Despre noi & Cariere — Crama Sigheteană",
              "Povestea Cramei Sigheteană din Sighetu Marmației, din 2020: bucătari pasionați, mâncare tradițională și locuri de muncă disponibile.", "despre") + nav("despre") + f'''
<main>
<section class="page-hero"><h1 class="blackletter">Despre noi</h1><p>Din 2020, la Sighet</p></section>
<section class="section split">
  <div class="split-text">
    <h2 class="blackletter">Povestea Cramei</h2>
    <p>Crama Sigheteană s-a deschis în 2020 cu o idee simplă: mâncare gătită cinstit, ca la masa din Maramureș, într-un loc în care te simți bine.</p>
    <p>Pivnița cu bolți de cărămidă și pereți de piatră ne oferă un decor care nu se imită, iar în bucătărie lucrează oameni care gătesc cu pasiune: de la ciorbe și fasole bătută, la grătar, coaste BBQ și deserturi făcute în casă.</p>
    <p>Vă așteptăm pentru prânz, cină, aniversări și mese în grup.</p>
  </div>
  <div class="split-img"><img src="images/sala-3.jpg" alt="Interiorul Cramei Sigheteană" loading="lazy" onerror="this.parentNode.classList.add('noimg')"></div>
</section>
<section class="section"><div class="gallery">{gal}</div></section>
{PATTERN}
<section class="section narrow" id="cariere">
  <h2 class="section-title blackletter">Cariere</h2>
  <p class="section-sub">Vrei să faci parte din echipă? Alege un post și trimite-ne datele tale.</p>
  <div class="jobs">{jobs_html}</div>
  <form class="form" id="job-form" novalidate>
    <h3>Aplică acum</h3>
    <label>Nume și prenume<input name="nume" required autocomplete="name"></label>
    <label>Telefon<input name="telefon" type="tel" required autocomplete="tel"></label>
    <label>Postul dorit
      <select name="post"><option>Bucătar / ajutor de bucătar</option><option>Ospătar / ospătăriță</option><option>Curier / livrări</option><option>Alt post</option></select></label>
    <label>Mesaj scurt<textarea name="mesaj" rows="4"></textarea></label>
    <p class="small">Atașați CV-ul în emailul care se deschide (nu putem încărca fișiere direct de pe site).</p>
    <label class="check"><input type="checkbox" name="gdpr" required> Sunt de acord cu prelucrarea datelor personale în scopul recrutării.</label>
    <button class="btn btn-red" type="submit">Trimite aplicația</button>
    <p class="form-msg" role="status"></p>
  </form>
</section>
</main>
''' + footer()
write("despre.html", despre)

# ---------------- CONTACT ----------------
contact = head("Contact & Rezervări — Crama Sigheteană, Iuliu Maniu 16, Sighetu Marmației",
               "Contact Crama Sigheteană: Iuliu Maniu nr. 16, Sighetu Marmației 435500. Telefon 0755 674 569, email cramasigheteana@yahoo.com. Rezervări și comenzi.", "contact") + nav("contact") + f'''
<main>
<section class="page-hero"><h1 class="blackletter">Contact</h1><p>Comenzi, rezervări și întrebări</p></section>
<section class="section contact-split">
  <div class="contact-info">
    <ul class="info-list">
      <li><span class="ico-c">&#9906;</span><div><strong>Adresă</strong><br>{ADDRESS}</div></li>
      <li><span class="ico-c">&#9742;</span><div><strong>Telefon comenzi</strong><br><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div></li>
      <li><span class="ico-c">&#9993;</span><div><strong>Email</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
      <li><span class="ico-c">&#9719;</span><div><strong>Program</strong><br><span id="hours">Sunați pentru program</span></div></li>
    </ul>
    <a class="btn btn-red" href="tel:{PHONE_TEL}">Sună acum</a>
    <a class="btn btn-outline" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination={MAPS_Q.replace(" ", "+")}">Deschide în Google Maps</a>
  </div>
  <div class="map"><iframe title="Harta Crama Sigheteană" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={MAPS_Q.replace(" ", "+")}&output=embed"></iframe></div>
</section>
<section class="section narrow" id="rezervare">
  <h2 class="section-title blackletter">Rezervare / mesaj</h2>
  <form class="form" id="contact-form" novalidate>
    <label>Nume<input name="nume" required autocomplete="name"></label>
    <label>Telefon<input name="telefon" type="tel" required autocomplete="tel"></label>
    <div class="row2">
      <label>Data<input name="data" type="date"></label>
      <label>Nr. persoane<input name="persoane" type="number" min="1" max="60"></label>
    </div>
    <label>Mesaj<textarea name="mesaj" rows="4"></textarea></label>
    <label class="check"><input type="checkbox" name="gdpr" required> Sunt de acord cu prelucrarea datelor pentru a primi răspuns.</label>
    <button class="btn btn-red" type="submit">Trimite</button>
    <p class="form-msg" role="status"></p>
  </form>
</section>
</main>
''' + footer()
write("contact.html", contact)

# imagini: listă de nume așteptate
names = sorted({d[4] for d in DISHES} | {"logo.jpg", "sala-boltita.jpg", "sala-1.jpg", "sala-2.jpg", "sala-3.jpg", "sala-4.jpg", "meniul-zilei-1.jpg", "meniul-zilei-2.jpg"})
with open(os.path.join(OUT, "images", "LISTA-IMAGINI.txt"), "w", encoding="utf-8") as f:
    f.write("Pune în acest folder imaginile cu următoarele nume (JPG, de preferat max. 1600 px lățime, sub 300 KB):\n\n" + "\n".join(names) + "\n")
print("OK", len(names), "imagini așteptate")
