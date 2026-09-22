#!/usr/bin/env python3
"""Baut die Website in allen vier Sprachen.

    python3 bauen.py

Eine Vorlage, ein Wortschatz je Sprache. Vier gleich aussehende Seiten von
Hand zu pflegen geht genau so lange gut, bis eine davon vergessen wird; die
Rechtsseite wird aus demselben Grund erzeugt und nicht getippt.

Erzeugt werden die Startseite, je eine Seite fuer Shlayolotl und Wheresome,
Support, die Datenschutzerklaerung der Website und die sitemap.xml. Deutsch
liegt auf /, die anderen unter /en/, /fr/ und /es/. Die Rechtsseiten der
Apps (/shlayolotl und /wheresome, ohne Schraegstrich) kommen NICHT von hier,
sondern aus den App-Repositories (tool/make_legal_page.py --site).
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

SITE = 'https://hollowspoon.app'

# Die Produktseiten liegen MIT Schraegstrich: /shlayolotl/ ist die Seite ueber
# das Spiel, /shlayolotl (ohne) bleibt die Rechtsseite der App. Die ist bei
# Apple als Datenschutz- und Support-Adresse hinterlegt und wird aus dem
# App-Repository erzeugt, also nicht hier. Cloudflare haelt beide auseinander:
# shlayolotl.html bedient die kurze Adresse, shlayolotl/index.html die mit
# Schraegstrich, ohne Umleitung dazwischen (nachgelesen im Asset-Server).
APPS = ['shlayolotl', 'wheresome']
RECHT = {'shlayolotl': '/shlayolotl', 'wheresome': '/wheresome'}

# Datum fuer <lastmod> in der Sitemap. Bewusst von Hand: wer den Inhalt einer
# Seite aendert, setzt es hoch. Bei jedem Bau automatisch zu stempeln saehe
# fleissig aus und sagte Google nichts, weil es dann immer "heute" hiesse.
STAND = '2026-09-22'

OG_LOCALE = {'de': 'de_DE', 'en': 'en_US', 'fr': 'fr_FR', 'es': 'es_ES'}
OG_BILD = {'start': '/assets/img/og-hollow-spoon.png',
           'shlayolotl': '/assets/img/og-shlayolotl.png',
           'wheresome': '/assets/img/og-wheresome.png'}

T = {
    'de': dict(
        titel='Hollow Spoon | Apps &amp; Spiele',
        support_titel='Support: Shlayolotl und Wheresome | Hollow Spoon',
        support_zeile='Schreib uns:',
        support_recht='Support und Datenschutzerkl&auml;rung',
        beschreibung='Hollow Spoon baut Apps, die eine Sache k&ouml;nnen: '
                     'Shlayolotl, Tic Tac Toe mit Axolotln, im App Store. '
                     'Wheresome, ein Ort f&uuml;r deine Reise, in Vorbereitung.',
        support_beschreibung='Fragen zu Shlayolotl oder Wheresome? Schreib an '
                             'contact@hollowspoon.app. Hier stehen auch Support '
                             'und Datenschutzerkl&auml;rung je App.',
        ds_beschreibung='Datenschutzerkl&auml;rung der Website hollowspoon.app: '
                        'Auslieferung &uuml;ber Cloudflare, keine Cookies, keine '
                        'Analyse, Kontakt per E-Mail.',
        og_alt={'start': 'Schriftzug Hollow Spoon',
                'shlayolotl': 'Symbol der App Shlayolotl',
                'wheresome': 'Symbol der App Wheresome'},
        nav_apps='Apps', nav_support='Support',
        h1='Ein L&ouml;ffel reicht.',
        lead='Wir bauen Apps, die eine Sache k&ouml;nnen. Und die richtig.',
        studio='Hollow Spoon ist ein unabh&auml;ngiges Studio aus Bremen. Wir '
               'entwickeln eigene Apps und Spiele f&uuml;r iPhone, bald auch '
               'f&uuml;r Android.',
        mehr={'shlayolotl': 'Mehr zu Shlayolotl', 'wheresome': 'Mehr zu Wheresome'},
        shlay_text='Tic Tac Toe mit Axolotln. Schnelle Runden gegen den '
                   'Computer, gegen jemanden neben dir oder online.',
        badge_alt='Laden im App Store',
        where_tag='In Vorbereitung',
        where_text='Sag, wonach sich deine Reise anf&uuml;hlen soll: Meer, '
                   'Natur, Ruhe, ein Monat. Wheresome zeigt dir einen Ort, '
                   'mit der Begr&uuml;ndung daneben.',
        where_bald='Bald im App Store und bei Google Play.',
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
        titel='Hollow Spoon | Apps &amp; Games',
        support_titel='Support: Shlayolotl and Wheresome | Hollow Spoon',
        support_zeile='Just write to us:',
        support_recht='Support and privacy policy',
        beschreibung='Hollow Spoon builds apps that do one thing: Shlayolotl, '
                     'tic tac toe with axolotls, on the App Store. Wheresome, '
                     'one place for your trip, in preparation.',
        support_beschreibung='Questions about Shlayolotl or Wheresome? Write to '
                             'contact@hollowspoon.app. Support and privacy '
                             'policy for each app are linked here too.',
        ds_beschreibung='Privacy policy of the website hollowspoon.app: '
                        'delivery via Cloudflare, no cookies, no analytics, '
                        'contact by e-mail.',
        og_alt={'start': 'Hollow Spoon wordmark',
                'shlayolotl': 'Shlayolotl app icon',
                'wheresome': 'Wheresome app icon'},
        nav_apps='Apps', nav_support='Support',
        h1='One spoon is enough.',
        lead='We build apps that do one thing. And do it properly.',
        studio='Hollow Spoon is an independent studio in Bremen. We make our '
               'own apps and games for iPhone, soon for Android too.',
        mehr={'shlayolotl': 'More about Shlayolotl', 'wheresome': 'More about Wheresome'},
        shlay_text='Tic tac toe with axolotls. Quick rounds against the '
                   'computer, against someone sitting next to you, or online.',
        badge_alt='Download on the App Store',
        where_tag='In preparation',
        where_text='Tell it how your trip should feel: sea, nature, quiet, a '
                   'month. Wheresome shows you one place, with the reasoning '
                   'right next to it.',
        where_bald='Coming soon to the App Store and Google Play.',
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
        titel='Hollow Spoon | Applications et jeux',
        support_titel='Assistance&nbsp;: Shlayolotl et Wheresome | Hollow Spoon',
        support_zeile='&Eacute;cris-nous&nbsp;:',
        support_recht='Assistance et politique de confidentialit&eacute;',
        beschreibung='Hollow Spoon cr&eacute;e des applications qui font une '
                     'chose&nbsp;: Shlayolotl, le morpion avec des axolotls, '
                     'sur l&rsquo;App Store. Wheresome, un lieu pour ton '
                     'voyage, en pr&eacute;paration.',
        support_beschreibung='Une question sur Shlayolotl ou Wheresome&nbsp;? '
                             '&Eacute;cris &agrave; contact@hollowspoon.app. '
                             'L&rsquo;assistance et la politique de '
                             'confidentialit&eacute; de chaque application '
                             'sont li&eacute;es ici.',
        ds_beschreibung='Politique de confidentialit&eacute; du site '
                        'hollowspoon.app&nbsp;: diffusion par Cloudflare, aucun '
                        'cookie, aucune mesure d&rsquo;audience, contact par '
                        'e-mail.',
        og_alt={'start': 'Logotype Hollow Spoon',
                'shlayolotl': 'Ic&ocirc;ne de l&rsquo;application Shlayolotl',
                'wheresome': 'Ic&ocirc;ne de l&rsquo;application Wheresome'},
        nav_apps='Applications', nav_support='Assistance',
        h1='Une cuill&egrave;re suffit.',
        lead='Nous cr&eacute;ons des applications qui font une chose. Et qui '
             'la font bien.',
        studio='Hollow Spoon est un studio ind&eacute;pendant de Br&ecirc;me. '
               'Nous cr&eacute;ons nos propres applications et jeux pour '
               'iPhone, et bient&ocirc;t pour Android.',
        mehr={'shlayolotl': 'En savoir plus sur Shlayolotl',
              'wheresome': 'En savoir plus sur Wheresome'},
        shlay_text='Le morpion avec des axolotls. Des parties rapides contre '
                   'l&rsquo;ordinateur, contre quelqu&rsquo;un &agrave; '
                   'c&ocirc;t&eacute; de toi, ou en ligne.',
        badge_alt='T&eacute;l&eacute;charger dans l&rsquo;App Store',
        where_tag='En pr&eacute;paration',
        where_text='Dis ce que ton voyage doit &eacute;voquer&nbsp;: la mer, '
                   'la nature, le calme, un mois. Wheresome te montre un '
                   'lieu, avec la raison juste &agrave; c&ocirc;t&eacute;.',
        where_bald='Bient&ocirc;t sur l&rsquo;App Store et Google Play.',
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
        titel='Hollow Spoon | Apps y juegos',
        support_titel='Soporte: Shlayolotl y Wheresome | Hollow Spoon',
        support_zeile='Escr&iacute;benos:',
        support_recht='Soporte y pol&iacute;tica de privacidad',
        beschreibung='Hollow Spoon crea apps que hacen una cosa: Shlayolotl, '
                     'tres en raya con ajolotes, en el App Store. Wheresome, '
                     'un lugar para tu viaje, en preparaci&oacute;n.',
        support_beschreibung='&iquest;Dudas sobre Shlayolotl o Wheresome? '
                             'Escribe a contact@hollowspoon.app. Aqu&iacute; '
                             'est&aacute;n tambi&eacute;n el soporte y la '
                             'pol&iacute;tica de privacidad de cada app.',
        ds_beschreibung='Pol&iacute;tica de privacidad del sitio '
                        'hollowspoon.app: entrega a trav&eacute;s de Cloudflare, '
                        'sin cookies, sin anal&iacute;tica, contacto por correo.',
        og_alt={'start': 'Logotipo de Hollow Spoon',
                'shlayolotl': 'Icono de la app Shlayolotl',
                'wheresome': 'Icono de la app Wheresome'},
        nav_apps='Apps', nav_support='Soporte',
        h1='Basta una cuchara.',
        lead='Creamos apps que hacen una cosa. Y la hacen bien.',
        studio='Hollow Spoon es un estudio independiente de Bremen. Creamos '
               'nuestras propias apps y juegos para iPhone, y pronto '
               'tambi&eacute;n para Android.',
        mehr={'shlayolotl': 'M&aacute;s sobre Shlayolotl',
              'wheresome': 'M&aacute;s sobre Wheresome'},
        shlay_text='Tres en raya con ajolotes. Partidas r&aacute;pidas contra '
                   'el ordenador, contra alguien a tu lado o en l&iacute;nea.',
        badge_alt='Consíguelo en el App Store',
        where_tag='En preparaci&oacute;n',
        where_text='Di c&oacute;mo quieres que se sienta tu viaje: mar, '
                   'naturaleza, calma, un mes. Wheresome te ense&ntilde;a un '
                   'lugar, con el motivo al lado.',
        where_bald='Pronto en el App Store y en Google Play.',
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

# ---------------------------------------------------------------------------
# Die Produktseiten. Eine je App und Sprache, auf /shlayolotl/ und /wheresome/
# und darunter /en/, /fr/, /es/.
#
# Nur, was feststeht: fuer Shlayolotl die Spielarten, die zwei Spielfelder,
# das iPhone und "kein Konto" (steht so schon auf /shlayolotl-download), fuer
# Wheresome nur das, was auch die Startseite sagt. Keine Preise, keine
# Bewertungen, keine Downloadzahlen. Wheresome bleibt sichtbar "in
# Vorbereitung", die Seite ist trotzdem eine richtige Seite und nicht nur
# ein Platzhalter.
# ---------------------------------------------------------------------------

P = {
 'shlayolotl': {
  'de': dict(
   titel='Shlayolotl | Tic Tac Toe mit Axolotln',
   beschreibung='Tic Tac Toe mit Axolotln, gemacht f&uuml;rs Telefon. Spielfelder '
                'mit drei mal drei und vier mal vier Feldern, gegen den Computer, '
                'gegen jemanden neben dir oder online. Kein Konto n&ouml;tig.',
   erster='Rosa gegen Gr&uuml;n, wer zuerst eine Reihe voll hat, gewinnt. Eine '
          'Runde dauert kaum eine Minute, deshalb passt das Spiel in jede '
          'Wartezeit. Shlayolotl ist f&uuml;rs Telefon gemacht und l&auml;uft '
          'auf dem iPhone.',
   h2a='Drei Arten zu spielen',
   pa='Gegen den Computer, wenn du allein bist. Gegen jemanden, der neben dir '
      'sitzt. Oder online.',
   h2b='Zwei Spielfelder',
   pb='Das klassische Spielfeld mit drei mal drei Feldern, und ein '
      'gr&ouml;&szlig;eres mit vier mal vier.',
   letzter='Kein Konto, keine Anmeldung. Was das Spiel sich merkt, bleibt auf '
           'deinem Ger&auml;t.'),
  'en': dict(
   titel='Shlayolotl | Tic Tac Toe with Axolotls',
   beschreibung='Tic tac toe with axolotls, made for the phone. Three by three '
                'and four by four boards, against the computer, someone next to '
                'you, or online. No account needed.',
   erster='Pink against green, and whoever completes a line first wins. A '
          'round takes barely a minute, so the game fits into any wait. '
          'Shlayolotl is made for the phone and runs on iPhone.',
   h2a='Three ways to play',
   pa='Against the computer when you are on your own. Against someone sitting '
      'next to you. Or online.',
   h2b='Two boards',
   pb='The classic board with three by three squares, and a bigger one with '
      'four by four.',
   letzter='No account, no sign-up. Whatever the game remembers stays on your '
           'device.'),
  'fr': dict(
   titel='Shlayolotl | Le morpion avec des axolotls',
   beschreibung='Le morpion avec des axolotls, fait pour le t&eacute;l&eacute;phone. '
                'Grilles de trois sur trois et quatre sur quatre, contre '
                'l&rsquo;ordinateur, quelqu&rsquo;un &agrave; c&ocirc;t&eacute; de '
                'toi ou en ligne. Sans compte.',
   erster='Les roses contre les verts, et le premier qui aligne ses axolotls '
          'gagne. Une partie dure &agrave; peine une minute, alors le jeu se '
          'glisse dans n&rsquo;importe quelle attente. Shlayolotl est fait pour '
          'le t&eacute;l&eacute;phone et tourne sur iPhone.',
   h2a='Trois fa&ccedil;ons de jouer',
   pa='Contre l&rsquo;ordinateur quand tu es seul. Contre quelqu&rsquo;un assis '
      '&agrave; c&ocirc;t&eacute; de toi. Ou en ligne.',
   h2b='Deux grilles',
   pb='La grille classique de trois sur trois, et une plus grande de quatre '
      'sur quatre.',
   letzter='Pas de compte, pas d&rsquo;inscription. Ce que le jeu retient reste '
           'sur ton appareil.'),
  'es': dict(
   titel='Shlayolotl | Tres en raya con ajolotes',
   beschreibung='Tres en raya con ajolotes, hecho para el tel&eacute;fono. '
                'Tableros de tres por tres y cuatro por cuatro, contra el '
                'ordenador, alguien a tu lado o en l&iacute;nea. Sin cuenta.',
   erster='Rosas contra verdes, y gana quien complete primero una l&iacute;nea. '
          'Una partida dura apenas un minuto, as&iacute; que el juego cabe en '
          'cualquier espera. Shlayolotl est&aacute; hecho para el tel&eacute;fono '
          'y funciona en el iPhone.',
   h2a='Tres formas de jugar',
   pa='Contra el ordenador cuando est&aacute;s solo. Contra alguien sentado a tu '
      'lado. O en l&iacute;nea.',
   h2b='Dos tableros',
   pb='El tablero cl&aacute;sico de tres por tres, y uno m&aacute;s grande de '
      'cuatro por cuatro.',
   letzter='Sin cuenta, sin registro. Lo que el juego recuerda se queda en tu '
           'dispositivo.'),
 },
 'wheresome': {
  'de': dict(
   titel='Wheresome | Ein Ort, der zu deiner Reise passt',
   beschreibung='Wheresome zeigt dir einen Ort f&uuml;r deine Reise und '
                'erkl&auml;rt, warum er passt. Du sagst, was dir wichtig ist: '
                'Meer, Natur, Ruhe, ein Monat. In Vorbereitung, bald im App '
                'Store und bei Google Play.',
   erster='Wheresome hilft dir, einen Ort f&uuml;r eine Reise oder einen '
          'l&auml;ngeren Aufenthalt zu finden. Du sagst, was dir wichtig ist, '
          'zum Beispiel Meer oder Natur, Ruhe, oder in welchem Monat du fahren '
          'willst. Wheresome schl&auml;gt dir daraufhin einen Ort vor und '
          'erkl&auml;rt, warum er passt.',
   letzter='Die Begr&uuml;ndung steht direkt neben dem Vorschlag. So siehst du, '
           'warum gerade dieser Ort, und entscheidest, ob er f&uuml;r dich '
           'stimmt.',
   status='Wheresome ist noch in Vorbereitung.'),
  'en': dict(
   titel='Wheresome | A place that fits your trip',
   beschreibung='Wheresome shows you one place for your trip and explains why '
                'it fits. You say what matters: sea, nature, quiet, a month. In '
                'preparation, coming soon to the App Store and Google Play.',
   erster='Wheresome helps you find a place for a trip or a longer stay. You '
          'say what matters to you, for instance sea or nature, quiet, or which '
          'month you want to go. Wheresome then suggests a place and explains '
          'why it fits.',
   letzter='The reasoning sits right next to the suggestion, so you can see why '
           'this place, and decide whether it is right for you.',
   status='Wheresome is still in preparation.'),
  'fr': dict(
   titel='Wheresome | Un lieu qui correspond &agrave; ton voyage',
   beschreibung='Wheresome te montre un lieu pour ton voyage et explique '
                'pourquoi il convient. Tu dis ce qui compte&nbsp;: la mer, la '
                'nature, le calme, un mois. En pr&eacute;paration, bient&ocirc;t '
                'sur l&rsquo;App Store et Google Play.',
   erster='Wheresome t&rsquo;aide &agrave; trouver un lieu pour un voyage ou un '
          's&eacute;jour plus long. Tu dis ce qui compte pour toi, par exemple '
          'la mer ou la nature, le calme, ou le mois o&ugrave; tu veux partir. '
          'Wheresome te propose alors un lieu et explique pourquoi il convient.',
   letzter='La raison se trouve juste &agrave; c&ocirc;t&eacute; de la '
           'proposition&nbsp;: tu vois pourquoi ce lieu-l&agrave;, et tu '
           'd&eacute;cides s&rsquo;il te correspond.',
   status='Wheresome est encore en pr&eacute;paration.'),
  'es': dict(
   titel='Wheresome | Un lugar que encaja con tu viaje',
   beschreibung='Wheresome te ense&ntilde;a un lugar para tu viaje y explica por '
                'qu&eacute; encaja. Dices lo que te importa: mar, naturaleza, '
                'calma, un mes. En preparaci&oacute;n, pronto en el App Store y '
                'en Google Play.',
   erster='Wheresome te ayuda a encontrar un lugar para un viaje o una estancia '
          'm&aacute;s larga. Dices lo que te importa, por ejemplo mar o '
          'naturaleza, calma, o en qu&eacute; mes quieres ir. Wheresome te '
          'propone entonces un lugar y explica por qu&eacute; encaja.',
   letzter='El motivo est&aacute; justo al lado de la propuesta: ves por '
           'qu&eacute; ese lugar y decides si es para ti.',
   status='Wheresome todav&iacute;a est&aacute; en preparaci&oacute;n.'),
 },
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
  /* Ein Satz mehr unter dem Claim, leiser gesetzt: wer wir sind und wofuer
     wir bauen. Der Claim allein sagt einer Suchmaschine nichts. */
  .studio { font-size: 17px; line-height: 1.6; color: #8A909E; max-width: 32em; margin: 22px 0 0; }

  .band { padding: 74px 0; }
  .band.shlay { background: #0A0E24; color: #E7EAF6; }
  .band.where { background: #176F7A; color: #F0EDE4; }
  /* Symbol neben dem Namen statt schraeg darueber. Das kennt jeder aus dem
     App Store, und es sieht auf jeder Breite gleich gewollt aus.
     height:auto ist dabei nicht kosmetisch: ohne sie gewinnt das
     height-Attribut aus dem Markup und das Symbol steht gequetscht da. */
  .band .kopf { display: flex; align-items: center; gap: 22px; margin-bottom: 20px; }
  .band .kopf picture { flex: 0 0 auto; display: block; }
  .band .icon { width: 112px; height: auto; border-radius: 25px; flex: 0 0 auto; }
  .band .kopf .tag { margin: 0 0 6px; }
  .band .kopf h2 { margin: 0; }
  .band .tag { font-size: 11px; letter-spacing: .16em; text-transform: uppercase; opacity: .72; margin: 0 0 14px; }
  .band h2 { font-size: clamp(32px, 5vw, 50px); letter-spacing: -.025em; margin: 0 0 16px; font-weight: 800; }
  .band h2 a { color: inherit; text-decoration: none; }
  .band h2 a:hover { text-decoration: underline; text-underline-offset: 6px; text-decoration-thickness: 2px; }
  .band p { font-size: 17px; line-height: 1.65; margin: 0 0 24px; max-width: 30em; opacity: .88; }
  /* Der Weg zur Seite der App: ein Textlink, kein Knopf. */
  .band .mehr { margin-top: -8px; }
  .band .mehr a { color: inherit; text-decoration: underline; text-underline-offset: 3px; text-decoration-thickness: 1px; }

  /* Die Seite einer App: dasselbe Band wie auf der Startseite, nur traegt es
     hier die H1 und den ganzen Text. */
  .produkt .kopf { margin-bottom: 28px; }
  .produkt .kopf h1 { font-size: clamp(40px, 7vw, 72px); line-height: 1; letter-spacing: -.035em;
                      margin: 0; max-width: none; }
  .produkt h2 { font-size: 22px; letter-spacing: -.01em; margin: 34px 0 10px; }
  .produkt .text p { max-width: 34em; }
  .produkt .recht { margin: 30px 0 0; font-size: 15px; opacity: .8; }
  .produkt .recht a { color: inherit; }

  /* Der Knopf von Apple, unveraendert. Apples Richtlinien: nicht umfaerben,
     nicht drehen, nicht animieren, mindestens 40 px hoch, ringsum ein
     Viertel der Hoehe frei. */
  /* Der Knopf steht unter den Bildern: erst sehen, was es ist, dann laden. */
  .badge { display: inline-block; line-height: 0; padding: 12px; margin: 26px 0 0 -12px; }
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

  /* Die Punkte zeichnen wir selbst. ::scroll-marker waere schoener, aber
     Safari auf dem iPhone kennt es noch nicht, und dort fehlten sie ganz. */
  .punkte { display: none; }
  .punkte button { width: 8px; height: 8px; padding: 0; border: 0; border-radius: 50%;
                   background: rgba(255,255,255,.28); cursor: pointer; }
  .punkte button[aria-current="true"] { background: #fff; }


  footer { padding: 34px 0 14px; font-size: 13px; color: #8A909E;
           display: flex; gap: 20px; flex-wrap: wrap; border-top: 1px solid #E7E9ED; }
  footer a { color: #5C6270; text-decoration: none; }
  .marken { padding: 0 0 64px; font-size: 12px; line-height: 1.6; color: #A4AAB6; max-width: 46em; }

  @media (max-width: 720px) {
    .band .inner { grid-template-columns: 1fr; gap: 20px; }
    .band .icon { width: 132px; justify-self: start; }
    /* Auf dem Telefon passt ohnehin nur eines nebeneinander. Also gleich
       eines je Seite, mit den Punkten darunter. */
    .carousel { gap: 0; scrollbar-width: none; padding-bottom: 0; }
    .carousel::-webkit-scrollbar { display: none; }
    .carousel picture { flex: 0 0 100%; display: flex; justify-content: center; }
    .carousel img { width: auto; height: 58vh; max-width: 100%; }
    .punkte { display: flex; gap: 9px; justify-content: center; padding-top: 18px; }
    .band .icon { width: 84px; border-radius: 19px; }
    .band .kopf { gap: 16px; }
    nav .rechts a { margin-left: 18px; font-size: 13px; }
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


def symbol(app):
    """Das App-Symbol, klein als WebP und das PNG als Rueckfall. Es wird
    112 px breit gezeigt; das Shlayolotl-PNG allein hat 172 KB. Leerer
    Alt-Text, weil der Name direkt daneben steht."""
    return (
        '      <picture>\n'
        '        <source type="image/webp" srcset="/assets/img/%s-256.webp 256w, /assets/img/%s-512.webp 512w" sizes="112px">\n'
        '        <img class="icon" src="/assets/img/%s.png" alt="" width="256" height="256">\n'
        '      </picture>' % (app, app, app)
    )


def kopf(sprache, pfade, titel, beschreibung, bild='start'):
    """Die <head>-Zeilen, die jede Seite gleich braucht: Titel, Beschreibung,
    canonical auf sich selbst, hreflang auf die Geschwister, Open Graph fuer
    geteilte Links, die Symbole. `pfade` ordnet jeder Sprache ihren Pfad zu.
    x-default zeigt auf Englisch, wie bisher: wer keine der vier Sprachen
    spricht, versteht am ehesten die."""
    t = T[sprache]
    hreflang = '\n'.join(
        '<link rel="alternate" hreflang="%s" href="%s%s">' % (s, SITE, pfade[s])
        for s in SPRACHEN)
    hreflang += '\n<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, pfade['en'])
    andere = '\n'.join(
        '<meta property="og:locale:alternate" content="%s">' % OG_LOCALE[s]
        for s in SPRACHEN if s != sprache)
    return '''<title>%(titel)s</title>
<meta name="description" content="%(beschreibung)s">
<link rel="canonical" href="%(site)s%(pfad)s">
%(hreflang)s
<meta property="og:site_name" content="Hollow Spoon">
<meta property="og:type" content="website">
<meta property="og:title" content="%(titel)s">
<meta property="og:description" content="%(beschreibung)s">
<meta property="og:url" content="%(site)s%(pfad)s">
<meta property="og:image" content="%(site)s%(og_bild)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="%(og_alt)s">
<meta property="og:locale" content="%(locale)s">
%(andere)s
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">''' % dict(
        titel=titel, beschreibung=beschreibung, site=SITE, pfad=pfade[sprache],
        hreflang=hreflang, og_bild=OG_BILD[bild], og_alt=t['og_alt'][bild],
        locale=OG_LOCALE[sprache], andere=andere)


# Wer wir sind, fuer Maschinen: nur, was auch im Impressum steht. Keine
# Profile bei Diensten, die es nicht gibt. Echte Zeichen statt Entitaeten,
# weil das in <script> nicht mehr HTML ist, sondern JSON.
ORGANISATION = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Hollow Spoon",
  "legalName": "Hollow Spoon UG (haftungsbeschränkt)",
  "url": "https://hollowspoon.app/",
  "logo": "https://hollowspoon.app/assets/img/hollow-spoon-logo.png",
  "email": "contact@hollowspoon.app",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Gravensteiner Straße 33",
    "postalCode": "28219",
    "addressLocality": "Bremen",
    "addressCountry": "DE"
  }
}
</script>'''


NAMEN = {'de': 'Deutsch', 'en': 'English', 'fr': 'Fran&ccedil;ais', 'es': 'Espa&ntilde;ol'}


def sprachleiste(sprache, pfade):
    return ''.join(
        '<span class="hier">%s</span>' % NAMEN[s] if s == sprache
        else '<a href="%s" hreflang="%s">%s</a>' % (pfade[s], s, NAMEN[s])
        for s in SPRACHEN)


def seite(sprache):
    t = T[sprache]
    shots = '\n'.join(bild(sprache, i + 1, t['shots'][i]) for i in range(3))

    return '''<!DOCTYPE html>
<html lang="%(sprache)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
%(kopf)s
%(organisation)s
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
</div>

<main>
<div class="wrap">
  <div class="hero">
    <h1>%(h1)s</h1>
    <p class="lead">%(lead)s</p>
    <p class="studio">%(studio)s</p>
  </div>
</div>

<section class="band shlay" id="apps">
  <div class="wrap">
    <div class="kopf">
%(symbol_shlay)s
      <div>
        <h2><a href="%(pfad)sshlayolotl/">Shlayolotl</a></h2>
      </div>
    </div>
    <p>%(shlay_text)s</p>
    <p class="mehr"><a href="%(pfad)sshlayolotl/">%(mehr_shlay)s</a></p>
    <div class="carousel" id="shots">
%(shots)s
    </div>
    <div class="punkte" data-fuer="shots"></div>
    <a class="badge" href="%(shlay_url)s">
      <img src="/assets/img/appstore-%(sprache)s.svg" alt="%(badge_alt)s" width="120" height="40">
    </a>
  </div>
</section>

<section class="band where">
  <div class="wrap">
    <div class="kopf">
%(symbol_where)s
      <div>
        <p class="tag">%(where_tag)s</p>
        <h2><a href="%(pfad)swheresome/">Wheresome</a></h2>
      </div>
    </div>
    <p>%(where_text)s</p>
    <p class="mehr"><a href="%(pfad)swheresome/">%(mehr_where)s</a></p>
    <p class="soon">%(where_bald)s</p>
  </div>
</section>
</main>

<div class="wrap">
  <footer>
    <span>&copy; 2026 Hollow Spoon UG (haftungsbeschr&auml;nkt)</span>
    <a href="/impressum">%(impressum)s</a>
    <a href="%(ds_pfad)s">%(datenschutz)s</a>
    <a href="mailto:contact@hollowspoon.app">contact@hollowspoon.app</a>
  </footer>
  <p class="sprachen">%(sprachen)s</p>
  <p class="marken">%(marken)s</p>
</div>

<script>
  // Die Punkte unter der Bilderreihe. Anklicken springt zum Bild, beim
  // Wischen wandert der helle Punkt mit. Faellt das Skript aus, bleibt die
  // Leiste leer und gewischt werden kann trotzdem.
  document.querySelectorAll('.punkte').forEach(function (leiste) {
    var reihe = document.getElementById(leiste.dataset.fuer);
    if (!reihe) return;
    var bilder = Array.prototype.slice.call(reihe.children);
    var knoepfe = bilder.map(function (bild, i) {
      var k = document.createElement('button');
      k.type = 'button';
      k.setAttribute('aria-label', String(i + 1));
      k.addEventListener('click', function () {
        reihe.scrollTo({ left: bild.offsetLeft - reihe.offsetLeft, behavior: 'smooth' });
      });
      leiste.appendChild(k);
      return k;
    });
    function markiere() {
      var mitte = reihe.scrollLeft + reihe.clientWidth / 2;
      var naechster = 0, kleinster = Infinity;
      bilder.forEach(function (bild, i) {
        var d = Math.abs(bild.offsetLeft - reihe.offsetLeft + bild.offsetWidth / 2 - mitte);
        if (d < kleinster) { kleinster = d; naechster = i; }
      });
      knoepfe.forEach(function (k, i) { k.setAttribute('aria-current', String(i === naechster)); });
    }
    reihe.addEventListener('scroll', markiere, { passive: true });
    markiere();
  });
</script>
</body>
</html>
''' % dict(t, sprache=sprache, pfad=PFAD[sprache],
           kopf=kopf(sprache, PFAD, t['titel'], t['beschreibung']),
           organisation=ORGANISATION,
           sprachen=sprachleiste(sprache, PFAD), shots=shots, stil=STIL,
           symbol_shlay=symbol('shlayolotl'), symbol_where=symbol('wheresome'),
           mehr_shlay=t['mehr']['shlayolotl'], mehr_where=t['mehr']['wheresome'],
           ds_pfad=DS_PFAD[sprache], shlay_url=SHLAY_URL[sprache])


PUNKTE_SKRIPT = '''<script>
  // Die Punkte unter der Bilderreihe, wie auf der Startseite.
  document.querySelectorAll('.punkte').forEach(function (leiste) {
    var reihe = document.getElementById(leiste.dataset.fuer);
    if (!reihe) return;
    var bilder = Array.prototype.slice.call(reihe.children);
    var knoepfe = bilder.map(function (bild, i) {
      var k = document.createElement('button');
      k.type = 'button';
      k.setAttribute('aria-label', String(i + 1));
      k.addEventListener('click', function () {
        reihe.scrollTo({ left: bild.offsetLeft - reihe.offsetLeft, behavior: 'smooth' });
      });
      leiste.appendChild(k);
      return k;
    });
    function markiere() {
      var mitte = reihe.scrollLeft + reihe.clientWidth / 2;
      var naechster = 0, kleinster = Infinity;
      bilder.forEach(function (bild, i) {
        var d = Math.abs(bild.offsetLeft - reihe.offsetLeft + bild.offsetWidth / 2 - mitte);
        if (d < kleinster) { kleinster = d; naechster = i; }
      });
      knoepfe.forEach(function (k, i) { k.setAttribute('aria-current', String(i === naechster)); });
    }
    reihe.addEventListener('scroll', markiere, { passive: true });
    markiere();
  });
</script>'''


def produkt_pfade(app):
    return {s: PFAD[s] + app + '/' for s in SPRACHEN}


def produkt_seite(app, sprache):
    """Die Seite einer App. Fuer Shlayolotl mit den Bildern und dem Knopf von
    der Startseite, fuer Wheresome ohne, weil es noch nichts zu zeigen und
    nichts zu laden gibt. Unten der Link auf die Rechtsseite der App, die
    unter derselben Adresse ohne Schraegstrich liegt."""
    t = T[sprache]
    p = P[app][sprache]
    pfade = produkt_pfade(app)

    if app == 'shlayolotl':
        oben = ''
        text = ('      <p>%(erster)s</p>\n'
                '      <h2>%(h2a)s</h2>\n'
                '      <p>%(pa)s</p>\n'
                '      <h2>%(h2b)s</h2>\n'
                '      <p>%(pb)s</p>\n'
                '      <p>%(letzter)s</p>') % p
        unten = ('    <div class="carousel" id="shots">\n%s\n    </div>\n'
                 '    <div class="punkte" data-fuer="shots"></div>\n'
                 '    <a class="badge" href="%s">\n'
                 '      <img src="/assets/img/appstore-%s.svg" alt="%s" width="120" height="40">\n'
                 '    </a>' % ('\n'.join(bild(sprache, i + 1, t['shots'][i]) for i in range(3)),
                              SHLAY_URL[sprache], sprache, t['badge_alt']))
        lead = t['shlay_text']
        skript = PUNKTE_SKRIPT
    else:
        oben = '        <p class="tag">%s</p>\n' % t['where_tag']
        text = ('      <p>%(erster)s</p>\n'
                '      <p>%(letzter)s</p>') % p
        unten = '    <p class="soon">%s %s</p>' % (p['status'], t['where_bald'])
        lead = t['where_text']
        skript = ''

    return '''<!DOCTYPE html>
<html lang="%(sprache)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
%(kopf)s
<style>
%(stil)s
</style>
</head>
<body>

<div class="wrap">
  <nav>
    <span class="mark"><a href="%(startpfad)s"><img src="/assets/img/wortmarke-schwarz.png" alt="Hollow Spoon" width="1033" height="158" style="height:22px;width:auto"></a></span>
    <span class="rechts"><a href="%(startpfad)s#apps">%(nav_apps)s</a><a href="%(startpfad)ssupport/">%(nav_support)s</a></span>
  </nav>
</div>

<main>
<section class="band %(klasse)s produkt">
  <div class="wrap">
    <div class="kopf">
%(symbol)s
      <div>
%(oben)s        <h1>%(name)s</h1>
      </div>
    </div>
    <p>%(lead)s</p>
    <div class="text">
%(text)s
    </div>
%(unten)s
    <p class="recht"><a href="%(recht)s#%(sprache)s">%(support_recht)s</a></p>
  </div>
</section>
</main>

<div class="wrap">
  <footer>
    <span>&copy; 2026 Hollow Spoon UG (haftungsbeschr&auml;nkt)</span>
    <a href="/impressum">%(impressum)s</a>
    <a href="%(ds_pfad)s">%(datenschutz)s</a>
    <a href="mailto:contact@hollowspoon.app">contact@hollowspoon.app</a>
  </footer>
  <p class="sprachen">%(sprachen)s</p>
  <p class="marken">%(marken)s</p>
</div>
%(skript)s
</body>
</html>
''' % dict(t, sprache=sprache, startpfad=PFAD[sprache],
           kopf=kopf(sprache, pfade, p['titel'], p['beschreibung'], bild=app),
           stil=STIL, klasse='shlay' if app == 'shlayolotl' else 'where',
           symbol=symbol(app), oben=oben, name=app.capitalize(), lead=lead,
           text=text, unten=unten, recht=RECHT[app],
           sprachen=sprachleiste(sprache, pfade), ds_pfad=DS_PFAD[sprache],
           skript=skript)



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

def support_seite(sprache):
    """Support je Sprache statt einer Seite, auf der dieselbe Adresse viermal
    untereinander steht. Die Rechtsseiten der Apps tragen ohnehin alle vier."""
    t = T[sprache]
    pfade = {x: PFAD[x] + 'support/' for x in SPRACHEN}

    return VORLAGE_SUPPORT % dict(
        t, sprache=sprache, startpfad=PFAD[sprache],
        kopf=kopf(sprache, pfade, t['support_titel'],
                  t['support_beschreibung']),
        sprachen=sprachleiste(sprache, pfade), stil=SUPPORT_STIL,
        ds_pfad=DS_PFAD[sprache])


VORLAGE_SUPPORT = """<!DOCTYPE html>
<html lang="%(sprache)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
%(kopf)s
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
    zusammen = dict(t)
    zusammen.update(d)
    return VORLAGE_DS % dict(
        zusammen, sprache=sprache, startpfad=PFAD[sprache],
        kopf=kopf(sprache, DS_PFAD, d['titel'] + ' | Hollow Spoon',
                  t['ds_beschreibung']),
        sprachen=sprachleiste(sprache, DS_PFAD), stil=SUPPORT_STIL,
        stand=DS_STAND[sprache], anschrift=ANSCHRIFT, behoerde=BEHOERDE)


VORLAGE_DS = """<!DOCTYPE html>
<html lang="%(sprache)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
%(kopf)s
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


# ---------------------------------------------------------------------------
# Sitemap: nur die Seiten, die jemand suchen soll. Startseite und die beiden
# Produktseiten, je in vier Sprachen, jede mit ihren Geschwistern als
# xhtml:link. Impressum, Datenschutz, Support und die Rechtsseiten der Apps
# sind erreichbar und duerfen indexiert werden, stehen aber nicht hier: sie
# sind kein Suchziel, und die Sitemap soll sagen, was wichtig ist.
# ---------------------------------------------------------------------------

def sitemap():
    gruppen = [PFAD] + [produkt_pfade(app) for app in APPS]
    eintraege = []
    for pfade in gruppen:
        for s in SPRACHEN:
            links = ''.join(
                '\n    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (x, SITE, pfade[x])
                for x in SPRACHEN)
            links += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, pfade['en'])
            eintraege.append('  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>%s\n  </url>'
                             % (SITE, pfade[s], STAND, links))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + '\n'.join(eintraege) + '\n</urlset>\n')


def schreibe(ziel, inhalt):
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    assert not [c for c in inhalt if c in '\u2013\u2014\u2212'], 'Gedankenstrich in ' + ziel
    io.open(ziel, 'w', encoding='utf-8').write(inhalt)
    print('%-32s %6.1f KB' % (os.path.relpath(ziel, ROOT), len(inhalt) / 1024))


if __name__ == '__main__':
    for s in SPRACHEN:
        ordner = '' if s == 'de' else s + '/'
        schreibe(os.path.join(ROOT, ordner + 'index.html'), seite(s))
        for app in APPS:
            schreibe(os.path.join(ROOT, ordner + app + '/index.html'), produkt_seite(app, s))
        schreibe(os.path.join(ROOT, ordner + 'support/index.html'), support_seite(s))
        schreibe(os.path.join(ROOT, DS_DATEI[s]), datenschutz_seite(s))
    schreibe(os.path.join(ROOT, 'sitemap.xml'), sitemap())
