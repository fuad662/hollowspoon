#!/usr/bin/env python3
"""Baut die Startseite in allen vier Sprachen.

    python3 bauen.py

Eine Vorlage, ein Wortschatz je Sprache. Vier gleich aussehende Seiten von
Hand zu pflegen geht genau so lange gut, bis eine davon vergessen wird; die
Rechtsseite wird aus demselben Grund erzeugt und nicht getippt.

Deutsch liegt auf /, die anderen unter /en/, /fr/ und /es/.
"""

import io
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

SPRACHEN = ['de', 'en', 'fr', 'es']
PFAD = {'de': '/', 'en': '/en/', 'fr': '/fr/', 'es': '/es/'}

SHLAY_URL = {
    'de': 'https://apps.apple.com/de/app/shlayolotl/id6805653548',
    'en': 'https://apps.apple.com/app/shlayolotl/id6805653548',
    'fr': 'https://apps.apple.com/fr/app/shlayolotl/id6805653548',
    'es': 'https://apps.apple.com/es/app/shlayolotl/id6805653548',
}

T = {
    'de': dict(
        titel='Hollow Spoon',
        support_zeile='Schreib uns:',
        support_recht='Support und Datenschutzerkl&auml;rung',
        beschreibung='Hollow Spoon baut kleine Apps, die eine Sache koennen. '
                     'Shlayolotl im App Store, Wheresome in Vorbereitung.',
        nav_apps='Apps', nav_support='Support',
        h1='Ein L&ouml;ffel reicht.',
        lead='Wir bauen Apps, die eine Sache k&ouml;nnen. Und die richtig.',
        shlay_tag='Im App Store, kostenlos',
        shlay_text='Tic Tac Toe mit Axolotln. Schnelle Runden gegen den '
                   'Computer, gegen jemanden neben dir oder online.',
        badge_alt='Laden im App Store',
        where_tag='In Vorbereitung',
        where_text='Sag, wonach sich deine Reise anf&uuml;hlen soll: Meer, '
                   'Natur, Ruhe, ein Monat. Wheresome zeigt dir einen Ort, '
                   'mit der Begr&uuml;ndung daneben.',
        where_bald='Bald im App Store und bei Google Play.',
        ueber_titel='Wer dahintersteckt',
        ueber_text='Hollow Spoon ist eine kleine Firma. Wir bauen Apps, die '
                   'eine Sache richtig machen, statt vieler Dinge halb.',
        impressum='Impressum', datenschutz='Datenschutz',
        marken='Apple und das Apple-Logo sind Marken von Apple Inc., '
               'eingetragen in den USA und anderen L&auml;ndern. App Store '
               'ist eine Dienstleistungsmarke von Apple Inc.',
        shots=['Shlayolotl: ein Spielfeld mit drei mal drei Feldern, rosa und '
               'gr&uuml;ne Axolotl darauf',
               'Shlayolotl: ein gr&ouml;&szlig;eres Spielfeld mit vier mal '
               'vier Feldern',
               'Shlayolotl: der Bildschirm nach einem gewonnenen Spiel'],
    ),
    'en': dict(
        titel='Hollow Spoon',
        support_zeile='Just write to us:',
        support_recht='Support and privacy policy',
        beschreibung='Hollow Spoon builds small apps that do one thing. '
                     'Shlayolotl on the App Store, Wheresome in preparation.',
        nav_apps='Apps', nav_support='Support',
        h1='One spoon is enough.',
        lead='We build apps that do one thing. And do it properly.',
        shlay_tag='On the App Store, free',
        shlay_text='Tic tac toe with axolotls. Quick rounds against the '
                   'computer, against someone sitting next to you, or online.',
        badge_alt='Download on the App Store',
        where_tag='In preparation',
        where_text='Tell it how your trip should feel: sea, nature, quiet, a '
                   'month. Wheresome shows you one place, with the reasoning '
                   'right next to it.',
        where_bald='Coming soon to the App Store and Google Play.',
        ueber_titel='Who is behind this',
        ueber_text='Hollow Spoon is a small company. We build apps that do '
                   'one thing properly, rather than many things halfway.',
        impressum='Legal notice', datenschutz='Privacy',
        marken='Apple and the Apple logo are trademarks of Apple Inc., '
               'registered in the U.S. and other countries. App Store is a '
               'service mark of Apple Inc.',
        shots=['Shlayolotl: a three by three board with pink and green '
               'axolotls on it',
               'Shlayolotl: a larger board, four by four',
               'Shlayolotl: the screen after a won game'],
    ),
    'fr': dict(
        titel='Hollow Spoon',
        support_zeile='&Eacute;cris-nous&nbsp;:',
        support_recht='Assistance et politique de confidentialit&eacute;',
        beschreibung='Hollow Spoon cr&eacute;e de petites applications qui '
                     'font une chose. Shlayolotl sur l&rsquo;App Store, '
                     'Wheresome en pr&eacute;paration.',
        nav_apps='Applications', nav_support='Assistance',
        h1='Une cuill&egrave;re suffit.',
        lead='Nous cr&eacute;ons des applications qui font une chose. Et qui '
             'la font bien.',
        shlay_tag='Sur l&rsquo;App Store, gratuit',
        shlay_text='Le morpion avec des axolotls. Des parties rapides contre '
                   'l&rsquo;ordinateur, contre quelqu&rsquo;un &agrave; '
                   'c&ocirc;t&eacute; de toi, ou en ligne.',
        badge_alt='T&eacute;l&eacute;charger dans l&rsquo;App Store',
        where_tag='En pr&eacute;paration',
        where_text='Dis ce que ton voyage doit &eacute;voquer&nbsp;: la mer, '
                   'la nature, le calme, un mois. Wheresome te montre un '
                   'lieu, avec la raison juste &agrave; c&ocirc;t&eacute;.',
        where_bald='Bient&ocirc;t sur l&rsquo;App Store et Google Play.',
        ueber_titel='Qui est derri&egrave;re',
        ueber_text='Hollow Spoon est une petite entreprise. Nous cr&eacute;ons '
                   'des applications qui font bien une chose, plut&ocirc;t '
                   'que beaucoup de choses &agrave; moiti&eacute;.',
        impressum='Mentions l&eacute;gales', datenschutz='Confidentialit&eacute;',
        marken='Apple et le logo Apple sont des marques d&rsquo;Apple Inc., '
               'd&eacute;pos&eacute;es aux &Eacute;tats-Unis et dans '
               'd&rsquo;autres pays. App Store est une marque de service '
               'd&rsquo;Apple Inc.',
        shots=['Shlayolotl&nbsp;: une grille de trois sur trois avec des '
               'axolotls roses et verts',
               'Shlayolotl&nbsp;: une grille plus grande, quatre sur quatre',
               'Shlayolotl&nbsp;: l&rsquo;&eacute;cran apr&egrave;s une '
               'partie gagn&eacute;e'],
    ),
    'es': dict(
        titel='Hollow Spoon',
        support_zeile='Escr&iacute;benos:',
        support_recht='Soporte y pol&iacute;tica de privacidad',
        beschreibung='Hollow Spoon crea apps peque&ntilde;as que hacen una '
                     'cosa. Shlayolotl en el App Store, Wheresome en '
                     'preparaci&oacute;n.',
        nav_apps='Apps', nav_support='Soporte',
        h1='Basta una cuchara.',
        lead='Creamos apps que hacen una cosa. Y la hacen bien.',
        shlay_tag='En el App Store, gratis',
        shlay_text='Tres en raya con ajolotes. Partidas r&aacute;pidas contra '
                   'el ordenador, contra alguien a tu lado o en l&iacute;nea.',
        badge_alt='Consíguelo en el App Store',
        where_tag='En preparaci&oacute;n',
        where_text='Di c&oacute;mo quieres que se sienta tu viaje: mar, '
                   'naturaleza, calma, un mes. Wheresome te ense&ntilde;a un '
                   'lugar, con el motivo al lado.',
        where_bald='Pronto en el App Store y en Google Play.',
        ueber_titel='Qui&eacute;n est&aacute; detr&aacute;s',
        ueber_text='Hollow Spoon es una empresa peque&ntilde;a. Creamos apps '
                   'que hacen bien una cosa, en lugar de muchas a medias.',
        impressum='Aviso legal', datenschutz='Privacidad',
        marken='Apple y el logotipo de Apple son marcas comerciales de Apple '
               'Inc., registradas en EE.&nbsp;UU. y en otros pa&iacute;ses. '
               'App Store es una marca de servicio de Apple Inc.',
        shots=['Shlayolotl: un tablero de tres por tres con ajolotes rosas y '
               'verdes',
               'Shlayolotl: un tablero m&aacute;s grande, de cuatro por cuatro',
               'Shlayolotl: la pantalla despu&eacute;s de ganar una partida'],
    ),
}

STIL = '''  *, *::before, *::after { box-sizing: border-box; }
  body { margin: 0; background: #fff; color: #14161A;
         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  img { display: block; max-width: 100%; }
  .wrap { max-width: 1120px; margin: 0 auto; padding: 0 24px; }

  nav { display: flex; justify-content: space-between; align-items: center; gap: 20px;
        padding: 26px 0; font-size: 14px; }
  /* flex-shrink 0 und max-width none: sonst quetscht der Kopf den Schriftzug
     schmal, waehrend die feste Hoehe stehen bleibt. Auf dem Telefon sah er
     deshalb zusammengedrueckt aus. */
  nav .mark { flex: 0 0 auto; }
  nav .mark img { height: 22px; width: auto; max-width: none; display: block; }
  nav .rechts a { color: #5C6270; text-decoration: none; margin-left: 24px; white-space: nowrap; }
  nav .rechts a:hover { color: #14161A; }

  /* Die Sprachen stehen unten, nicht oben. Vier Kuerzel neben Apps und
     Support waren auf dem Telefon nicht zu verstehen und brachen um. */
  .sprachen { padding: 22px 0 0; font-size: 13px; color: #8A909E;
              display: flex; gap: 16px; flex-wrap: wrap; }
  .sprachen a { color: #5C6270; text-decoration: none; }
  .sprachen a:hover { color: #14161A; }
  .sprachen .hier { color: #14161A; font-weight: 600; }

  .hero { padding: 84px 0 68px; }
  h1 { font-size: clamp(52px, 12vw, 132px); line-height: .92; letter-spacing: -.05em;
       margin: 0 0 26px; font-weight: 800; max-width: 9em; }
  .lead { font-size: 21px; line-height: 1.55; color: #5C6270; max-width: 26em; margin: 0; }

  .band { padding: 74px 0; }
  .band.shlay { background: #0A0E24; color: #E7EAF6; }
  .band.where { background: #176F7A; color: #F0EDE4; }
  .band .inner { display: grid; grid-template-columns: 1fr 260px; gap: 46px; align-items: center; }
  /* height:auto ist nicht kosmetisch: ohne sie gewinnt das height-Attribut
     aus dem Markup, und das Symbol steht gequetscht da (132 breit, 256
     hoch statt quadratisch). Genau das ist am 20.9. live gegangen. */
  .band .icon { width: 200px; height: auto; border-radius: 44px; justify-self: end; }
  .band .tag { font-size: 11px; letter-spacing: .16em; text-transform: uppercase; opacity: .72; margin: 0 0 14px; }
  .band h2 { font-size: clamp(32px, 5vw, 50px); letter-spacing: -.025em; margin: 0 0 16px; font-weight: 800; }
  .band p { font-size: 17px; line-height: 1.65; margin: 0 0 24px; max-width: 30em; opacity: .88; }

  /* Der Knopf von Apple, unveraendert. Apples Richtlinien: nicht umfaerben,
     nicht drehen, nicht animieren, mindestens 40 px hoch, ringsum ein
     Viertel der Hoehe frei. */
  .badge { display: inline-block; line-height: 0; padding: 12px; margin: 0 0 0 -12px; }
  .badge img { height: 44px; width: auto; }
  .soon { font-size: 15px; font-weight: 600; opacity: .8; margin: 0; }

  /* Wischbar ohne Skript: die Leiste scrollt waagerecht und rastet ein. */
  .carousel { display: flex; gap: 14px; margin-top: 30px; padding-bottom: 14px;
              overflow-x: auto; scroll-snap-type: x mandatory;
              -webkit-overflow-scrolling: touch;
              scrollbar-color: rgba(255,255,255,.35) transparent; scrollbar-width: thin; }
  .carousel::-webkit-scrollbar { height: 6px; }
  .carousel::-webkit-scrollbar-thumb { background: rgba(255,255,255,.3); border-radius: 99px; }
  .carousel img { flex: 0 0 auto; scroll-snap-align: center; width: 212px; height: auto;
                  border-radius: 18px; }

  /* Die Punkte unter der Reihe. Der Browser setzt sie selbst und hebt den
     hervor, bei dem die Reihe gerade steht; anklicken springt dorthin. Kein
     Skript noetig. Browser, die das nicht koennen, zeigen keine Punkte, und
     das Wischen funktioniert trotzdem. */
  .carousel { scroll-marker-group: after; }
  .carousel::scroll-marker-group { display: flex; gap: 9px; justify-content: center;
                                   padding-top: 18px; }
  .carousel picture::scroll-marker { content: ''; width: 8px; height: 8px;
                                     border-radius: 50%; border: 0;
                                     background: rgba(255,255,255,.28); cursor: pointer; }
  .carousel picture::scroll-marker:target-current { background: #fff; }

  .about { padding: 76px 0; }
  .about h3 { font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: #8A909E; margin: 0 0 16px; }
  .about p { font-size: 19px; line-height: 1.65; max-width: 34em; margin: 0; }

  footer { padding: 34px 0 14px; font-size: 13px; color: #8A909E;
           display: flex; gap: 20px; flex-wrap: wrap; border-top: 1px solid #E7E9ED; }
  footer a { color: #5C6270; text-decoration: none; }
  .marken { padding: 0 0 64px; font-size: 12px; line-height: 1.6; color: #A4AAB6; max-width: 46em; }

  @media (max-width: 720px) {
    .band .inner { grid-template-columns: 1fr; gap: 20px; }
    .band .icon { width: 132px; justify-self: start; }
    .carousel img { width: 168px; }
  }'''


def bild(sprache, nr, alt):
    """Ein Bildschirmfoto in drei Fassungen: AVIF, WebP, und das WebP als
    Rueckfall. Der Browser nimmt das erste Format, das er kann, und von den
    zwei Breiten die, die zu seinem Bildschirm passt."""
    b = 'shlayolotl-%s-%d' % (sprache, nr)
    return (
        '        <picture>\n'
        '          <source type="image/avif" srcset="/assets/shots/%s-420.avif 420w, /assets/shots/%s-840.avif 840w" sizes="212px">\n'
        '          <source type="image/webp" srcset="/assets/shots/%s-420.webp 420w, /assets/shots/%s-840.webp 840w" sizes="212px">\n'
        '          <img src="/assets/shots/%s-420.webp" width="420" height="910" alt="%s" loading="lazy" decoding="async">\n'
        '        </picture>' % (b, b, b, b, b, alt)
    )


def seite(sprache):
    t = T[sprache]
    hreflang = '\n'.join(
        '<link rel="alternate" hreflang="%s" href="https://hollowspoon.app%s">' % (s, PFAD[s])
        for s in SPRACHEN)
    hreflang += '\n<link rel="alternate" hreflang="x-default" href="https://hollowspoon.app/en/">'

    namen = {'de': 'Deutsch', 'en': 'English', 'fr': 'Fran&ccedil;ais', 'es': 'Espa&ntilde;ol'}
    sprachen = ''.join(
        '<span class="hier">%s</span>' % namen[s] if s == sprache
        else '<a href="%s" hreflang="%s">%s</a>' % (PFAD[s], s, namen[s])
        for s in SPRACHEN)

    shots = '\n'.join(bild(sprache, i + 1, t['shots'][i]) for i in range(3))

    return '''<!DOCTYPE html>
<html lang="%(sprache)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(titel)s</title>
<meta name="description" content="%(beschreibung)s">
<link rel="canonical" href="https://hollowspoon.app%(pfad)s">
%(hreflang)s
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>
%(stil)s
</style>
</head>
<body>

<div class="wrap">
  <nav>
    <span class="mark"><a href="%(pfad)s"><img src="/assets/img/wortmarke-schwarz.png" alt="Hollow Spoon" width="1033" height="158" style="height:22px;width:auto"></a></span>
    <span class="rechts"><a href="#apps">%(nav_apps)s</a><a href="%(pfad)ssupport">%(nav_support)s</a></span>
  </nav>
  <div class="hero">
    <h1>%(h1)s</h1>
    <p class="lead">%(lead)s</p>
  </div>
</div>

<div class="band shlay" id="apps">
  <div class="wrap">
    <div class="inner">
      <div>
        <p class="tag">%(shlay_tag)s</p>
        <h2>Shlayolotl</h2>
        <p>%(shlay_text)s</p>
        <a class="badge" href="%(shlay_url)s">
          <img src="/assets/img/appstore-%(sprache)s.svg" alt="%(badge_alt)s" width="120" height="40">
        </a>
      </div>
      <img class="icon" src="/assets/img/shlayolotl.png" alt="" width="256" height="256">
    </div>
    <div class="carousel">
%(shots)s
    </div>
  </div>
</div>

<div class="band where">
  <div class="wrap">
    <div class="inner">
      <div>
        <p class="tag">%(where_tag)s</p>
        <h2>Wheresome</h2>
        <p>%(where_text)s</p>
        <p class="soon">%(where_bald)s</p>
      </div>
      <img class="icon" src="/assets/img/wheresome.png" alt="" width="256" height="256">
    </div>
  </div>
</div>

<div class="wrap">
  <div class="about">
    <h3>%(ueber_titel)s</h3>
    <p>%(ueber_text)s</p>
  </div>
  <footer>
    <span>&copy; 2026 Hollow Spoon UG (haftungsbeschr&auml;nkt)</span>
    <a href="/impressum">%(impressum)s</a>
    <a href="/datenschutz">%(datenschutz)s</a>
    <a href="mailto:contact@hollowspoon.app">contact@hollowspoon.app</a>
  </footer>
  <p class="sprachen">%(sprachen)s</p>
  <p class="marken">%(marken)s</p>
</div>

</body>
</html>
''' % dict(t, sprache=sprache, pfad=PFAD[sprache], hreflang=hreflang,
           sprachen=sprachen, shots=shots, stil=STIL, shlay_url=SHLAY_URL[sprache])



SUPPORT_STIL = """  body { margin: 0; background: #fff; color: #14161A;
         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  .wrap { max-width: 720px; margin: 0 auto; padding: 0 24px; }
  img { display: block; max-width: 100%; }
  nav { display: flex; justify-content: space-between; align-items: center; gap: 20px;
        padding: 26px 0; font-size: 14px; }
  nav .mark { flex: 0 0 auto; }
  nav .mark img { height: 22px; width: auto; max-width: none; display: block; }
  nav .rechts a { color: #5C6270; text-decoration: none; margin-left: 24px; white-space: nowrap; }
  h1 { font-size: 40px; letter-spacing: -.03em; margin: 56px 0 16px; }
  .zeile { font-size: 19px; line-height: 1.6; margin: 0 0 56px; }
  h2 { font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: #8A909E;
       margin: 32px 0 6px; }
  p { margin: 0; }
  a { color: #0F6E78; }
  footer { margin-top: 64px; padding-top: 20px; border-top: 1px solid #E7E9ED;
           font-size: 13px; color: #8A909E; display: flex; gap: 20px; flex-wrap: wrap; }
  footer a { color: #5C6270; text-decoration: none; }
  .sprachen { padding: 22px 0 64px; font-size: 13px; color: #8A909E;
              display: flex; gap: 16px; flex-wrap: wrap; }
  .sprachen a { color: #5C6270; text-decoration: none; }
  .sprachen .hier { color: #14161A; font-weight: 600; }"""

NAMEN = {'de': 'Deutsch', 'en': 'English', 'fr': 'Fran&ccedil;ais', 'es': 'Espa&ntilde;ol'}


def support_seite(sprache):
    """Support je Sprache statt einer Seite, auf der dieselbe Adresse viermal
    untereinander steht. Die Rechtsseiten der Apps tragen ohnehin alle vier."""
    t = T[sprache]
    hreflang = '\n'.join(
        '<link rel="alternate" hreflang="%s" href="https://hollowspoon.app%ssupport">' % (x, PFAD[x])
        for x in SPRACHEN)
    hreflang += ('\n<link rel="alternate" hreflang="x-default" '
                 'href="https://hollowspoon.app/en/support">')
    sprachen = ''.join(
        '<span class="hier">%s</span>' % NAMEN[x] if x == sprache
        else '<a href="%ssupport" hreflang="%s">%s</a>' % (PFAD[x], x, NAMEN[x])
        for x in SPRACHEN)

    return VORLAGE_SUPPORT % dict(
        t, sprache=sprache, pfad=PFAD[sprache] + 'support', startpfad=PFAD[sprache],
        hreflang=hreflang, sprachen=sprachen, stil=SUPPORT_STIL)


VORLAGE_SUPPORT = """<!DOCTYPE html>
<html lang="%(sprache)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(nav_support)s</title>
<meta name="description" content="%(nav_support)s: Hollow Spoon, Shlayolotl, Wheresome.">
<link rel="canonical" href="https://hollowspoon.app%(pfad)s">
%(hreflang)s
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>
%(stil)s
</style>
</head>
<body>
<div class="wrap">
  <nav>
    <span class="mark"><a href="%(startpfad)s"><img src="/assets/img/wortmarke-schwarz.png" alt="Hollow Spoon" width="1033" height="158"></a></span>
    <span class="rechts"><a href="%(startpfad)s#apps">%(nav_apps)s</a></span>
  </nav>

  <h1>%(nav_support)s</h1>
  <p class="zeile">%(support_zeile)s <a href="mailto:contact@hollowspoon.app">contact@hollowspoon.app</a></p>

  <h2>Shlayolotl</h2>
  <p><a href="/shlayolotl">%(support_recht)s</a></p>

  <h2>Wheresome</h2>
  <p><a href="/wheresome">%(support_recht)s</a></p>

  <footer>
    <span>&copy; 2026 Hollow Spoon UG (haftungsbeschr&auml;nkt)</span>
    <a href="/impressum">%(impressum)s</a>
    <a href="/datenschutz">%(datenschutz)s</a>
  </footer>
  <p class="sprachen">%(sprachen)s</p>
</div>
</body>
</html>
"""


for s in SPRACHEN:
    for ziel, html in (
        (os.path.join(ROOT, 'index.html' if s == 'de' else '%s/index.html' % s), seite(s)),
        (os.path.join(ROOT, ('' if s == 'de' else s + '/') + 'support/index.html'),
         support_seite(s)),
    ):
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        assert not [c for c in html if c in '\u2013\u2014\u2212'], 'Gedankenstrich in ' + s
        io.open(ziel, 'w', encoding='utf-8').write(html)
        print('%-28s %6.1f KB' % (os.path.relpath(ziel, ROOT), len(html) / 1024))
