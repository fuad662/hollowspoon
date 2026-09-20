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

# Die Datenschutzerklaerung der WEBSITE (nicht die der Apps, die stehen auf
# /shlayolotl und /wheresome). Deutsch behaelt seine alte Adresse.
DS_PFAD = {'de': '/datenschutz', 'en': '/en/privacy/',
           'fr': '/fr/confidentialite/', 'es': '/es/privacidad/'}
DS_DATEI = {'de': 'datenschutz.html', 'en': 'en/privacy/index.html',
            'fr': 'fr/confidentialite/index.html', 'es': 'es/privacidad/index.html'}

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

  /* Am Rechner stehen alle drei Bilder nebeneinander. Da braucht es weder
     Punkte noch eine Aufforderung zu wischen: man sieht ja schon alles. */
  .carousel { display: flex; gap: 14px; margin-top: 30px; padding-bottom: 14px;
              overflow-x: auto; scroll-snap-type: x mandatory;
              -webkit-overflow-scrolling: touch;
              scrollbar-color: rgba(255,255,255,.35) transparent; scrollbar-width: thin; }
  .carousel::-webkit-scrollbar { height: 6px; }
  .carousel::-webkit-scrollbar-thumb { background: rgba(255,255,255,.3); border-radius: 99px; }
  .carousel picture { flex: 0 0 auto; scroll-snap-align: center; }
  .carousel img { width: 212px; height: auto; border-radius: 18px; }

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
    /* Auf dem Telefon passt ohnehin nur eines nebeneinander. Also gleich
       eines je Seite, und darunter die drei Punkte: der Browser setzt sie
       selbst, hebt den hervor, bei dem die Reihe steht, und springt beim
       Antippen dorthin. Ohne Skript. Wer einen Browser ohne diese
       Faehigkeit hat, sieht keine Punkte und kann trotzdem wischen. */
    .carousel { gap: 0; scroll-marker-group: after;
                scrollbar-width: none; padding-bottom: 0; }
    .carousel::-webkit-scrollbar { display: none; }
    .carousel picture { flex: 0 0 100%; display: flex; justify-content: center; }
    .carousel img { width: auto; height: 62vh; max-width: 100%; }
    .carousel::scroll-marker-group { display: flex; gap: 9px; justify-content: center;
                                     padding-top: 18px; }
    .carousel picture::scroll-marker { content: ''; width: 8px; height: 8px;
                                       border-radius: 50%; border: 0;
                                       background: rgba(255,255,255,.28); cursor: pointer; }
    .carousel picture::scroll-marker:target-current { background: #fff; }
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
    <span class="rechts"><a href="#apps">%(nav_apps)s</a><a href="%(pfad)ssupport/">%(nav_support)s</a></span>
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
    <a href="%(ds_pfad)s">%(datenschutz)s</a>
    <a href="mailto:contact@hollowspoon.app">contact@hollowspoon.app</a>
  </footer>
  <p class="sprachen">%(sprachen)s</p>
  <p class="marken">%(marken)s</p>
</div>

</body>
</html>
''' % dict(t, sprache=sprache, pfad=PFAD[sprache], hreflang=hreflang,
           sprachen=sprachen, shots=shots, stil=STIL,
           ds_pfad=DS_PFAD[sprache], shlay_url=SHLAY_URL[sprache])



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
        '<link rel="alternate" hreflang="%s" href="https://hollowspoon.app%ssupport/">' % (x, PFAD[x])
        for x in SPRACHEN)
    hreflang += ('\n<link rel="alternate" hreflang="x-default" '
                 'href="https://hollowspoon.app/en/support/">')
    sprachen = ''.join(
        '<span class="hier">%s</span>' % NAMEN[x] if x == sprache
        else '<a href="%ssupport/" hreflang="%s">%s</a>' % (PFAD[x], x, NAMEN[x])
        for x in SPRACHEN)

    return VORLAGE_SUPPORT % dict(
        t, sprache=sprache, pfad=PFAD[sprache] + 'support/', startpfad=PFAD[sprache],
        hreflang=hreflang, sprachen=sprachen, stil=SUPPORT_STIL,
        ds_pfad=DS_PFAD[sprache])


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
  <p><a href="/shlayolotl#%(sprache)s">%(support_recht)s</a></p>

  <h2>Wheresome</h2>
  <p><a href="/wheresome#%(sprache)s">%(support_recht)s</a></p>

  <footer>
    <span>&copy; 2026 Hollow Spoon UG (haftungsbeschr&auml;nkt)</span>
    <a href="/impressum">%(impressum)s</a>
    <a href="%(ds_pfad)s">%(datenschutz)s</a>
  </footer>
  <p class="sprachen">%(sprachen)s</p>
</div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Datenschutzerklaerung der Website
#
# Sie stand bis zum 20.9. nur auf Deutsch und nannte GitHub Pages als Hoster.
# Beides war ueberholt: die Seite wird von Cloudflare ausgeliefert, und sie
# wird in vier Sprachen angeboten. Wer Leute auf Franzoesisch anspricht, muss
# ihnen auch auf Franzoesisch sagen, was mit ihren Daten geschieht.
# ---------------------------------------------------------------------------

DS_STAND = {'de': 'Stand: 20. September 2026', 'en': 'Last updated: 20 September 2026',
            'fr': 'Mise &agrave; jour&nbsp;: 20 septembre 2026',
            'es': 'Actualizado: 20 de septiembre de 2026'}

DS = {
 'de': dict(
  titel='Datenschutzerkl&auml;rung',
  intro='Diese Datenschutzerkl&auml;rung gilt f&uuml;r diese Website. F&uuml;r die Apps '
        'von Hollow Spoon gelten eigene Erkl&auml;rungen, die auf den jeweiligen '
        'Seiten verlinkt sind.',
  h_verantwortlich='1. Verantwortlicher',
  h_hosting='2. Auslieferung &uuml;ber Cloudflare',
  hosting='Diese Website wird von Cloudflare Pages ausgeliefert, einem Dienst der '
          'Cloudflare, Inc., 101 Townsend Street, San Francisco, CA 94107, USA. Beim '
          'Aufruf erfasst Cloudflare technische Daten in Server-Protokollen, '
          'insbesondere die IP-Adresse, Datum und Uhrzeit, die aufgerufene Seite, den '
          'Browser und das Betriebssystem. Diese Daten dienen der Bereitstellung und '
          'der Sicherheit des Dienstes. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f '
          'DSGVO; unser berechtigtes Interesse liegt darin, diese Website sicher und '
          'zuverl&auml;ssig bereitzustellen, ohne eigene Server zu betreiben.',
  hosting2='Dabei k&ouml;nnen Daten in die USA gelangen. Cloudflare ist nach dem EU-US '
           'Data Privacy Framework zertifiziert (nachgesehen am 20. September 2026) '
           'und st&uuml;tzt sich erg&auml;nzend auf die Standardvertragsklauseln der '
           'Europ&auml;ischen Kommission. N&auml;heres in Cloudflares '
           'Datenschutzerkl&auml;rung unter cloudflare.com/privacypolicy.',
  h_cookies='3. Keine Cookies, keine Analyse',
  cookies='Diese Website setzt keine Cookies, verwendet keine Analyse-Werkzeuge und '
          'keine Werbedienste. Wir selbst erheben und speichern keine '
          'personenbezogenen Daten von Besuchern.',
  cookies2='Cloudflare ersetzt E-Mail-Adressen im Seitentext durch ein kleines Skript, '
           'damit sie nicht automatisch eingesammelt werden k&ouml;nnen. Das Skript '
           'kommt von dieser Website selbst und setzt keine Cookies.',
  h_kontakt='4. Kontaktaufnahme per E-Mail',
  kontakt='Wenn Sie uns schreiben, speichern wir Ihre Angaben, um die Anfrage zu '
          'bearbeiten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, sofern die '
          'Anfrage mit einem Vertrag zusammenh&auml;ngt, sonst Art. 6 Abs. 1 lit. f '
          'DSGVO. Wir l&ouml;schen die Daten, sobald sie nicht mehr erforderlich sind '
          'und keine Aufbewahrungspflichten entgegenstehen.',
  h_rechte='5. Ihre Rechte',
  rechte='Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), '
         'L&ouml;schung (Art. 17), Einschr&auml;nkung der Verarbeitung (Art. 18), '
         'Daten&uuml;bertragbarkeit (Art. 20) und Widerspruch (Art. 21).',
  rechte2='Au&szlig;erdem k&ouml;nnen Sie sich bei einer Aufsichtsbeh&ouml;rde '
          'beschweren. F&uuml;r uns zust&auml;ndig ist:',
  h_aenderung='6. &Auml;nderungen',
  aenderung='Wir passen diese Erkl&auml;rung an, wenn sich die rechtlichen '
            'Anforderungen oder die Website &auml;ndern. F&uuml;r Ihren erneuten '
            'Besuch gilt die dann aktuelle Fassung.'),
 'en': dict(
  titel='Privacy policy',
  intro='This privacy policy covers this website. The Hollow Spoon apps have their '
        'own policies, linked from their pages.',
  h_verantwortlich='1. Controller',
  h_hosting='2. Delivery via Cloudflare',
  hosting='This website is delivered by Cloudflare Pages, a service of Cloudflare, '
          'Inc., 101 Townsend Street, San Francisco, CA 94107, USA. When you open it, '
          'Cloudflare records technical data in server logs, in particular the IP '
          'address, date and time, the page requested, the browser and the operating '
          'system. That data serves the provision and the security of the service. '
          'The legal basis is Art. 6(1)(f) GDPR; our legitimate interest is providing '
          'this website securely and reliably without running servers of our own.',
  hosting2='Data can reach the United States in the process. Cloudflare is certified '
           'under the EU-U.S. Data Privacy Framework (checked on 20 September 2026) '
           'and additionally relies on the European Commission\'s standard '
           'contractual clauses. See Cloudflare\'s privacy policy at '
           'cloudflare.com/privacypolicy.',
  h_cookies='3. No cookies, no analytics',
  cookies='This website sets no cookies, uses no analytics tools and no advertising '
          'services. We ourselves collect and store no personal data about visitors.',
  cookies2='Cloudflare replaces e-mail addresses in the page text with a small script '
           'so they cannot be harvested automatically. The script comes from this '
           'website itself and sets no cookies.',
  h_kontakt='4. Contacting us by e-mail',
  kontakt='If you write to us, we store what you send in order to handle the request. '
          'The legal basis is Art. 6(1)(b) GDPR where the request relates to a '
          'contract, otherwise Art. 6(1)(f) GDPR. We delete the data once it is no '
          'longer needed and no retention duty stands in the way.',
  h_rechte='5. Your rights',
  rechte='You have the rights of access (Art. 15 GDPR), rectification (Art. 16), '
         'erasure (Art. 17), restriction of processing (Art. 18), data portability '
         '(Art. 20) and objection (Art. 21).',
  rechte2='You may also lodge a complaint with a supervisory authority. The one '
          'responsible for us is:',
  h_aenderung='6. Changes',
  aenderung='We adapt this policy when the legal requirements or the website change. '
            'The version current at the time of your visit applies.'),
 'fr': dict(
  titel='Politique de confidentialit&eacute;',
  intro='Cette politique concerne ce site. Les applications Hollow Spoon ont leurs '
        'propres politiques, li&eacute;es depuis leurs pages.',
  h_verantwortlich='1. Responsable du traitement',
  h_hosting='2. Diffusion par Cloudflare',
  hosting='Ce site est diffus&eacute; par Cloudflare Pages, un service de Cloudflare, '
          'Inc., 101 Townsend Street, San Francisco, CA 94107, &Eacute;tats-Unis. Lors '
          'de la consultation, Cloudflare enregistre des donn&eacute;es techniques '
          'dans des journaux de serveur, notamment l\'adresse IP, la date et '
          'l\'heure, la page demand&eacute;e, le navigateur et le syst&egrave;me '
          'd\'exploitation. Ces donn&eacute;es servent &agrave; fournir et &agrave; '
          's&eacute;curiser le service. La base juridique est l\'art. 6, par. 1, '
          'point f du RGPD&nbsp;; notre int&eacute;r&ecirc;t l&eacute;gitime est de '
          'fournir ce site de mani&egrave;re s&ucirc;re et fiable sans exploiter nos '
          'propres serveurs.',
  hosting2='Des donn&eacute;es peuvent ainsi parvenir aux &Eacute;tats-Unis. '
           'Cloudflare est certifi&eacute; au titre du cadre de protection des '
           'donn&eacute;es UE-&Eacute;tats-Unis (v&eacute;rifi&eacute; le 20 septembre '
           '2026) et s\'appuie en outre sur les clauses contractuelles types de la '
           'Commission europ&eacute;enne. Voir la politique de Cloudflare sur '
           'cloudflare.com/privacypolicy.',
  h_cookies='3. Aucun cookie, aucune mesure d\'audience',
  cookies='Ce site ne d&eacute;pose aucun cookie, n\'utilise aucun outil de mesure '
          'd\'audience et aucun service publicitaire. Nous ne collectons et ne '
          'conservons nous-m&ecirc;mes aucune donn&eacute;e personnelle des '
          'visiteurs.',
  cookies2='Cloudflare remplace les adresses e-mail dans le texte par un petit script, '
           'afin qu\'elles ne puissent pas &ecirc;tre collect&eacute;es '
           'automatiquement. Ce script provient de ce site lui-m&ecirc;me et ne '
           'd&eacute;pose aucun cookie.',
  h_kontakt='4. Nous &eacute;crire',
  kontakt='Si tu nous &eacute;cris, nous conservons ce que tu envoies pour traiter la '
          'demande. La base juridique est l\'art. 6, par. 1, point b du RGPD lorsque '
          'la demande se rapporte &agrave; un contrat, sinon l\'art. 6, par. 1, point '
          'f. Nous supprimons ces donn&eacute;es d&egrave;s qu\'elles ne sont plus '
          'n&eacute;cessaires et qu\'aucune obligation de conservation ne s\'y '
          'oppose.',
  h_rechte='5. Tes droits',
  rechte='Tu disposes des droits d\'acc&egrave;s (art. 15 du RGPD), de rectification '
         '(art. 16), d\'effacement (art. 17), de limitation du traitement (art. 18), '
         'de portabilit&eacute; (art. 20) et d\'opposition (art. 21).',
  rechte2='Tu peux &eacute;galement introduire une r&eacute;clamation aupr&egrave;s '
          'd\'une autorit&eacute; de contr&ocirc;le. Celle dont nous relevons '
          'est&nbsp;:',
  h_aenderung='6. Modifications',
  aenderung='Nous adaptons cette politique lorsque les exigences l&eacute;gales ou le '
            'site changent. La version en vigueur lors de ta visite s\'applique.'),
 'es': dict(
  titel='Pol&iacute;tica de privacidad',
  intro='Esta pol&iacute;tica se refiere a este sitio web. Las apps de Hollow Spoon '
        'tienen sus propias pol&iacute;ticas, enlazadas desde sus p&aacute;ginas.',
  h_verantwortlich='1. Responsable del tratamiento',
  h_hosting='2. Entrega a trav&eacute;s de Cloudflare',
  hosting='Este sitio lo sirve Cloudflare Pages, un servicio de Cloudflare, Inc., 101 '
          'Townsend Street, San Francisco, CA 94107, EE.&nbsp;UU. Al abrirlo, '
          'Cloudflare registra datos t&eacute;cnicos en los registros del servidor, en '
          'particular la direcci&oacute;n IP, la fecha y la hora, la p&aacute;gina '
          'solicitada, el navegador y el sistema operativo. Esos datos sirven para '
          'prestar y asegurar el servicio. La base jur&iacute;dica es el art. 6, apdo. '
          '1, letra f del RGPD; nuestro inter&eacute;s leg&iacute;timo es ofrecer este '
          'sitio de forma segura y fiable sin operar servidores propios.',
  hosting2='En ese proceso los datos pueden llegar a Estados Unidos. Cloudflare '
           'est&aacute; certificada conforme al Marco de Privacidad de Datos '
           'UE-EE.&nbsp;UU. (consultado el 20 de septiembre de 2026) y se apoya '
           'adem&aacute;s en las cl&aacute;usulas contractuales tipo de la '
           'Comisi&oacute;n Europea. M&aacute;s informaci&oacute;n en la '
           'pol&iacute;tica de Cloudflare en cloudflare.com/privacypolicy.',
  h_cookies='3. Sin cookies, sin anal&iacute;tica',
  cookies='Este sitio no utiliza cookies, ni herramientas de anal&iacute;tica, ni '
          'servicios publicitarios. Nosotros mismos no recogemos ni guardamos datos '
          'personales de los visitantes.',
  cookies2='Cloudflare sustituye las direcciones de correo del texto por un peque&ntilde;o '
           'script para que no puedan recogerse autom&aacute;ticamente. El script '
           'procede de este mismo sitio y no utiliza cookies.',
  h_kontakt='4. Escribirnos por correo',
  kontakt='Si nos escribes, guardamos lo que env&iacute;as para atender la solicitud. '
          'La base jur&iacute;dica es el art. 6, apdo. 1, letra b del RGPD cuando la '
          'solicitud guarda relaci&oacute;n con un contrato, y en los dem&aacute;s '
          'casos la letra f. Borramos los datos en cuanto dejan de ser necesarios y no '
          'existe obligaci&oacute;n de conservarlos.',
  h_rechte='5. Tus derechos',
  rechte='Tienes derecho de acceso (art. 15 del RGPD), rectificaci&oacute;n (art. 16), '
         'supresi&oacute;n (art. 17), limitaci&oacute;n del tratamiento (art. 18), '
         'portabilidad (art. 20) y oposici&oacute;n (art. 21).',
  rechte2='Adem&aacute;s puedes presentar una reclamaci&oacute;n ante una autoridad de '
          'control. La competente para nosotros es:',
  h_aenderung='6. Cambios',
  aenderung='Adaptamos esta pol&iacute;tica cuando cambian los requisitos legales o el '
            'sitio. Se aplica la versi&oacute;n vigente en el momento de tu visita.'),
}

ANSCHRIFT = ('Hollow Spoon UG (haftungsbeschränkt)<br>\n'
             'Gravensteiner Straße 33<br>\n28219 Bremen<br>\n'
             'E-Mail: <a href="mailto:contact@hollowspoon.app">contact@hollowspoon.app</a>')

BEHOERDE = ('Die Landesbeauftragte für Datenschutz und Informationsfreiheit<br>\n'
            'der Freien Hansestadt Bremen<br>\n'
            'Georgstraße 122-124<br>\n27570 Bremerhaven')


def datenschutz_seite(sprache):
    t = T[sprache]
    d = DS[sprache]
    hreflang = '\n'.join(
        '<link rel="alternate" hreflang="%s" href="https://hollowspoon.app%s">' % (x, DS_PFAD[x])
        for x in SPRACHEN)
    hreflang += ('\n<link rel="alternate" hreflang="x-default" '
                 'href="https://hollowspoon.app/en/privacy/">')
    sprachen = ''.join(
        '<span class="hier">%s</span>' % NAMEN[x] if x == sprache
        else '<a href="%s" hreflang="%s">%s</a>' % (DS_PFAD[x], x, NAMEN[x])
        for x in SPRACHEN)
    zusammen = dict(t)
    zusammen.update(d)
    return VORLAGE_DS % dict(
        zusammen, sprache=sprache, pfad=DS_PFAD[sprache], startpfad=PFAD[sprache],
        hreflang=hreflang, sprachen=sprachen, stil=SUPPORT_STIL,
        stand=DS_STAND[sprache], anschrift=ANSCHRIFT, behoerde=BEHOERDE)


VORLAGE_DS = """<!DOCTYPE html>
<html lang="%(sprache)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(titel)s</title>
<link rel="canonical" href="https://hollowspoon.app%(pfad)s">
%(hreflang)s
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>
%(stil)s
  h1 { font-size: 34px; margin: 48px 0 6px; }
  h2 { font-size: 13px; margin: 34px 0 8px; }
  .zeile { font-size: 15px; color: #8A909E; margin: 0 0 32px; }
  .text p { font-size: 16px; line-height: 1.7; margin: 0 0 12px; max-width: 42em; }
</style>
</head>
<body>
<div class="wrap">
  <nav>
    <span class="mark"><a href="%(startpfad)s"><img src="/assets/img/wortmarke-schwarz.png" alt="Hollow Spoon" width="1033" height="158"></a></span>
    <span class="rechts"><a href="%(startpfad)ssupport/">%(nav_support)s</a></span>
  </nav>

  <h1>%(titel)s</h1>
  <p class="zeile">%(stand)s</p>

  <div class="text">
    <p>%(intro)s</p>

    <h2>%(h_verantwortlich)s</h2>
    <p>%(anschrift)s</p>

    <h2>%(h_hosting)s</h2>
    <p>%(hosting)s</p>
    <p>%(hosting2)s</p>

    <h2>%(h_cookies)s</h2>
    <p>%(cookies)s</p>
    <p>%(cookies2)s</p>

    <h2>%(h_kontakt)s</h2>
    <p>%(kontakt)s</p>

    <h2>%(h_rechte)s</h2>
    <p>%(rechte)s</p>
    <p>%(rechte2)s</p>
    <p>%(behoerde)s</p>

    <h2>%(h_aenderung)s</h2>
    <p>%(aenderung)s</p>
  </div>

  <footer>
    <span>&copy; 2026 Hollow Spoon UG (haftungsbeschr&auml;nkt)</span>
    <a href="/impressum">%(impressum)s</a>
    <a href="%(startpfad)ssupport/">%(nav_support)s</a>
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
        (os.path.join(ROOT, DS_DATEI[s]), datenschutz_seite(s)),
    ):
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        assert not [c for c in html if c in '\u2013\u2014\u2212'], 'Gedankenstrich in ' + s
        io.open(ziel, 'w', encoding='utf-8').write(html)
        print('%-28s %6.1f KB' % (os.path.relpath(ziel, ROOT), len(html) / 1024))
