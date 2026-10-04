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
import sys

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

# Zwei Adressen je App (4.10.2026, auf Vorschlag des Inhabers): /shlayolotl ist die
# Rechtsseite der App (Datenschutz und Support), bei Apple und Google hinterlegt und aus
# dem App-Repository erzeugt, also nicht hier; /shlayolotl/product/ ist die Seite ueber die
# App. Frueher lag die Produktseite auf /shlayolotl/, und ein einziger Schraegstrich
# entschied, welche der beiden Seiten man bekam. Jetzt haengt die Produktseite unter dem
# Namen der App. Die alten Adressen mit Schraegstrich gibt es nicht mehr (Cloudflare leitet
# /shlayolotl/ auf /shlayolotl um, also auf die Rechtsseite). Bei Shlayolotl steht bei Apple
# als Marketing-URL nur die Startseite (geprueft 4.10.2026), nichts bricht.
# Apps, die noch nicht im Store sind, stehen nirgends auf der Website: keine
# Karte auf der Startseite, keine Produktseite, kein Eintrag bei Support und in
# der Sitemap (2.10.2026: "das machen wir, wenn die app online ist"). Ihre
# Rechtsseite (/wheresome ohne Schraegstrich) bleibt erreichbar, nur unverlinkt:
# App Store Connect fuehrt sie als Datenschutz- und Support-Adresse, und Apple
# prueft den Link bei TestFlight und Review. Zum Freischalten hier austragen.
# Mitrechner seit 2.10.2026 online (User: "die seite auf der webseite sollst du sofort
# freischalten"), noch bevor Apple die App freigibt: der Knopf zeigt schon auf die
# App-Store-Adresse, die ab der Freigabe von selbst funktioniert.
# Freelancerito (4.10.2026) ist in keinem Store, weder bei Apple noch bei Google, also
# offline wie Wheresome: Produktseiten, Karte und Support-Eintrag gibt es nur in der
# Vorschau. Die Rechtsseite /freelancerito liegt trotzdem schon da (aus dem App-Repository,
# tool/rechtsseite.py --site), weil App Store Connect sie als Datenschutz- und
# Support-Adresse braucht.
OFFLINE = {'wheresome', 'freelancerito'}
# `python3 bauen.py --vorschau` baut alles, auch was offline ist, nach .vorschau/
# (nicht im Repository). So laesst sich eine Seite ansehen, bevor sie online geht.
VORSCHAU = '--vorschau' in sys.argv
AUS = set() if VORSCHAU else OFFLINE
APPS = [app for app in ['shlayolotl', 'mitrechner', 'karma-farmer', 'freelancerito', 'wheresome']
        if app not in AUS]
RECHT = {'shlayolotl': '/shlayolotl', 'wheresome': '/wheresome', 'mitrechner': '/mitrechner',
         'karma-farmer': '/karma-farmer', 'freelancerito': '/freelancerito'}
# Sprachen der App selbst, wo es nicht alle vier der Website sind. Freelancerito gibt es nur
# auf Deutsch und Englisch (4.10.2026), ein Geraet auf Franzoesisch oder Spanisch zeigt die
# App auf Englisch. Die Rechtsseite /freelancerito hat deshalb nur #de und #en: die
# franzoesische und spanische Seite verlinken /freelancerito#en (ein #fr ginge ins Leere,
# man landete oben auf der deutschen Fassung) und zeigen die englischen Bildschirmfotos.
APP_SPRACHEN = {'freelancerito': ('de', 'en')}
# Dazu ein Hinweis am Link, damit niemand Franzoesisch erwartet und Englisch bekommt.
AUF_ENGLISCH = {'de': ' (auf Englisch)', 'en': '', 'fr': ' (en anglais)', 'es': ' (en ingl&eacute;s)'}


def app_sprache(app, sprache):
    """Die Sprache, in der die App (und ihre Rechtsseite) einem Besucher dieser Seite begegnet."""
    return sprache if sprache in APP_SPRACHEN.get(app, SPRACHEN) else 'en'


def recht_link(app, sprache):
    """Adresse und Text des Links auf die Rechtsseite einer App, in der Sprache der Seite,
    soweit die Rechtsseite sie hat."""
    s = app_sprache(app, sprache)
    text = T[sprache]['support_recht'] + (AUF_ENGLISCH[sprache] if s != sprache else '')
    return '%s#%s' % (RECHT[app], s), text
# Angezeigter Name je App (die Adresse /karma-farmer/ hat einen Bindestrich, der Name nicht).
NAME = {'karma-farmer': 'Karma Farmer'}
# Apple-ID von Mitrechner: 6818615754 (App Store Connect, 2.10.2026). Ohne Land in der
# Adresse leitet Apple in den Store des Besuchers weiter; das passt, weil die spanische
# Fassung fuer Mexiko geschrieben ist und eine /es/-Adresse nach Spanien fuehren wuerde.
# Google Play folgt, sobald die App dort ist (dann auch das Abzeichen, siehe knoepfe).
MITR_APPSTORE = {s: 'https://apps.apple.com/app/mitrechner/id6818615754' for s in ('de', 'en', 'fr', 'es')}
# Bis Apple die App freigibt, zeigt die Seite statt des Knopfes „Bald im App Store.“: ein
# Knopf, der ins Leere fuehrt, verwirrt (User 3.10.2026). Nach der Freigabe auf True.
MITR_IM_STORE = False
MITR_BALD = {'de': 'Bald im App Store.', 'en': 'Coming soon to the App Store.',
             'fr': 'Bient&ocirc;t sur l&rsquo;App Store.', 'es': 'Muy pronto en el App Store.'}
MITR_PLAY = None
# Karma Farmer (3.10.2026: "lade ... die datenschutzseite hoch sowie die marketing seite").
# Wie Mitrechner: online, bevor Apple die App freigibt, mit „Bald im App Store." statt
# Knopf. Nach der Freigabe die Apple-ID eintragen und KF_IM_STORE auf True.
KF_APPSTORE = None
KF_IM_STORE = False
# Freelancerito (4.10.2026): noch in keinem Store, keine Apple-ID, nicht bei Google Play.
# Wie bei Mitrechner und Karma Farmer steht auf der Seite „Bald im App Store." statt eines
# Knopfes, der ins Leere fuehrt. Nach der Freigabe die Apple-ID eintragen, FL_IM_STORE auf
# True und freelancerito aus OFFLINE nehmen; Google Play folgt, sobald die App dort ist.
FL_APPSTORE = None
FL_IM_STORE = False
FL_PLAY = None

# Datum fuer <lastmod> in der Sitemap. Bewusst von Hand: wer den Inhalt einer
# Seite aendert, setzt es hoch. Bei jedem Bau automatisch zu stempeln saehe
# fleissig aus und sagte Google nichts, weil es dann immer "heute" hiesse.
STAND = '2026-10-03'

OG_LOCALE = {'de': 'de_DE', 'en': 'en_US', 'fr': 'fr_FR', 'es': 'es_ES'}
OG_BILD = {'start': '/assets/img/og-hollow-spoon.png',
           'shlayolotl': '/assets/img/og-shlayolotl.png',
           'wheresome': '/assets/img/og-wheresome.png',
           'mitrechner': '/assets/img/og-mitrechner.png',
           'karma-farmer': '/assets/img/og-karma-farmer.png',
           'freelancerito': '/assets/img/og-freelancerito.png'}

T = {
    'de': dict(
        titel='Hollow Spoon | Apps &amp; Spiele',
        support_titel='Support | Hollow Spoon',
        support_zeile='Schreib uns:',
        support_recht='Support und Datenschutzerkl&auml;rung',
        beschreibung='Hollow Spoon baut Apps, die eine Sache k&ouml;nnen: '
                     'Shlayolotl, Tic Tac Toe mit Axolotln, im App Store.',
        support_beschreibung='Fragen zu unseren Apps? Schreib an '
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
        support_titel='Support | Hollow Spoon',
        support_zeile='Just write to us:',
        support_recht='Support and privacy policy',
        beschreibung='Hollow Spoon builds apps that do one thing: Shlayolotl, '
                     'tic tac toe with axolotls, on the App Store.',
        support_beschreibung='Questions about our apps? Write to '
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
        support_titel='Assistance | Hollow Spoon',
        support_zeile='&Eacute;cris-nous&nbsp;:',
        support_recht='Assistance et politique de confidentialit&eacute;',
        beschreibung='Hollow Spoon cr&eacute;e des applications qui font une '
                     'chose&nbsp;: Shlayolotl, le morpion avec des axolotls, '
                     'sur l&rsquo;App Store.',
        support_beschreibung='Une question sur nos apps&nbsp;? '
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
        support_titel='Soporte | Hollow Spoon',
        support_zeile='Escr&iacute;benos:',
        support_recht='Soporte y pol&iacute;tica de privacidad',
        beschreibung='Hollow Spoon crea apps que hacen una cosa: Shlayolotl, '
                     'tres en raya con ajolotes, en el App Store.',
        support_beschreibung='&iquest;Dudas sobre nuestras apps? '
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
# Die Produktseiten. Eine je App und Sprache, auf /shlayolotl/product/ und
# /wheresome/product/ und davor /en/, /fr/, /es/.
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
  /* Mitrechner: ein dunkles Gruen aus dem App-Symbol, weisse Schrift darauf liest sich. */
  .band.mitr { background: #146B4E; color: #F2FBF6; }
  /* Karma Farmer: der Morgenhimmel der App (lib/himmel.dart), dunkle Schrift darauf. */
  .band.karma { background: linear-gradient(180deg, #F7C9A6 0%, #FBE3C8 40%, #F6F1E4 100%); color: #3D2C1E; }
''' + ('' if 'freelancerito' in AUS else
       # Nur im Stil, wenn Freelancerito gebaut wird: solange die App in OFFLINE ist, bleiben
       # die Live-Seiten Zeichen fuer Zeichen, wie sie sind.
       '  /* Freelancerito: das Tintenblau des Schiebereglers aus dem App-Symbol, darauf das warme\n'
       '     Off-White der App. Ruhig und ohne Verlauf, wie die App selbst. */\n'
       '  .band.freel { background: #2F5175; color: #F7F5F0; }\n') + '''  /* Symbol neben dem Namen statt schraeg darueber. Das kennt jeder aus dem
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
  .punkte + .soon { margin-top: 26px; }

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


# ---------------------------------------------------------------------------
# Mitrechner (2.10.2026). Nur, was die App wirklich kann: Gesamtsumme sofort,
# Mengen mit Komma, Plus mit Budget, Listen, Verlauf und Statistik, vier
# Sprachen, Waehrung nach Land (nicht fuer jedes Land der Welt, darum "zum
# Beispiel"), kein Konto, keine Werbung. Keine Preise, keine Bewertungen.
# ---------------------------------------------------------------------------

for _s, (_og, _mehr, _text, _play, _start) in {
    'de': ('Symbol der App Mitrechner', 'Mehr zu Mitrechner',
           'Die Einkaufsliste mit &Uuml;berblick. Du wei&szlig;t beim Einkaufen immer, was alles zusammen kostet.',
           'Jetzt bei Google Play',
           ' Mitrechner, die Einkaufsliste mit &Uuml;berblick, f&uuml;r iPhone.'),
    'en': ('Mitrechner app icon', 'More about Mitrechner',
           'The shopping list that keeps track. You always know what your shopping costs while you are still in the store.',
           'Get it on Google Play',
           ' Mitrechner, the shopping list that keeps track of your total, for iPhone.'),
    'fr': ('Ic&ocirc;ne de l&rsquo;application Mitrechner', 'En savoir plus sur Mitrechner',
           'La liste de courses qui affiche ton total. Tu sais toujours combien co&ucirc;tent tes courses, d&eacute;j&agrave; dans le magasin.',
           'Disponible sur Google Play',
           ' Mitrechner, la liste de courses qui affiche ton total, pour iPhone.'),
    'es': ('Icono de la app Mitrechner', 'M&aacute;s sobre Mitrechner',
           'La lista de compras que te dice cu&aacute;nto llevas. Siempre sabes cu&aacute;nto vas a pagar, desde que est&aacute;s en la tienda.',
           'Disponible en Google Play',
           ' Mitrechner, la lista de compras que te dice cu&aacute;nto llevas, para iPhone.'),
}.items():
    T[_s]['og_alt']['mitrechner'] = _og
    T[_s]['mehr']['mitrechner'] = _mehr
    T[_s]['mitr_text'] = _text
    T[_s]['badge_play_alt'] = _play
    if 'mitrechner' not in AUS:
        T[_s]['beschreibung'] += _start

# Im Ton des Inhabers, einfach gehalten: Ueberblick beim Einkaufen, vielleicht sogar sparen
# (2.10.2026: "möglichst einfach zu verstehen ... Überblick ... vielleicht sogar Geld
# sparen"). Dieselben Saetze wie im Store (mitrechner/tool/store.py). Beim Sparen bewusst
# "vielleicht": ein festes Sparversprechen liesse sich nicht belegen.
P['mitrechner'] = {
  'de': dict(
   titel='Mitrechner | Einkaufsliste mit &Uuml;berblick',
   beschreibung='Mitrechner zeigt dir beim Einkaufen sofort, was alles zusammen kostet. So beh&auml;ltst du den &Uuml;berblick. Kein Konto, keine Werbung, f&uuml;r iPhone.',
   erster='Du tippst ein, was du kaufst, wie viel davon und was es kostet. Mitrechner rechnet sofort mit und zeigt oben die Summe. Du siehst schon im Laden, wenn es zu viel wird, und kannst noch etwas zur&uuml;cklegen. Vielleicht sparst du so sogar Geld.',
   h2a='Mitrechner Plus',
   pa='Setz dir ein Budget, dann siehst du immer, wie viel noch &uuml;brig ist. Schreib deine Listen schon zu Hause. Und schau dir sp&auml;ter an, was du in jedem Monat ausgegeben hast und was du am meisten kaufst. Plus kaufst du einmal, ein Abo gibt es nicht.',
   h2b='In deiner Sprache',
   pb='Mitrechner gibt es auf Deutsch, Englisch, Spanisch und Franz&ouml;sisch. Die W&auml;hrung richtet sich nach deinem Land, also zum Beispiel Euro, Dollar oder Pesos.',
   letzter='Kein Konto, keine Werbung. Was du eintippst, bleibt auf deinem Handy.',
   shots=['Mitrechner: eine Einkaufsliste mit Gesamtsumme und Budget', 'Mitrechner: Ausgaben je Monat und die teuersten Artikel', 'Mitrechner: vorbereitete Einkaufslisten']),
  'en': dict(
   titel='Mitrechner | Know your total as you shop',
   beschreibung='Mitrechner shows you right away what your shopping costs, so you keep track of your spending. No account, no ads, for iPhone.',
   erster='Type in what you buy, how many and what it costs. Mitrechner does the math right away and shows the total at the top. You can see in the store when it is getting to be too much, and still put something back. You might even save some money that way.',
   h2a='Mitrechner Plus',
   pa='Set a budget and always see how much is left. Write your lists at home. And later, see what you spent each month and what you buy most. You buy Plus once, there is no subscription.',
   h2b='In your language',
   pb='Mitrechner is available in English, German, Spanish and French. The currency goes by your country, so for example dollars, euros or pesos.',
   letzter='No account, no ads. What you type in stays on your phone.',
   shots=['Mitrechner: a shopping list with total and budget', 'Mitrechner: spending per month and the priciest items', 'Mitrechner: shopping lists written ahead of time']),
  'fr': dict(
   titel='Mitrechner | Ton total pendant tes courses',
   beschreibung='Mitrechner te montre tout de suite combien co&ucirc;tent tes courses, pour garder le contr&ocirc;le. Sans compte, sans pub, pour iPhone.',
   erster='Tu notes ce que tu ach&egrave;tes, combien et le prix. Mitrechner calcule tout de suite et affiche le total en haut. Tu vois au magasin quand &ccedil;a fait trop, et tu peux encore reposer quelque chose. Tu peux m&ecirc;me faire des &eacute;conomies.',
   h2a='Mitrechner Plus',
   pa='Fixe-toi un budget et vois toujours ce qu&rsquo;il te reste. Pr&eacute;pare tes listes &agrave; la maison. Et ensuite, regarde ce que tu as d&eacute;pens&eacute; chaque mois et ce que tu ach&egrave;tes le plus. Plus, tu l&rsquo;ach&egrave;tes une fois, il n&rsquo;y a pas d&rsquo;abonnement.',
   h2b='Dans ta langue',
   pb='Mitrechner existe en fran&ccedil;ais, anglais, allemand et espagnol. La monnaie d&eacute;pend de ton pays, par exemple euros, dollars ou pesos.',
   letzter='Pas de compte, pas de pub. Ce que tu notes reste sur ton t&eacute;l&eacute;phone.',
   shots=['Mitrechner&nbsp;: une liste de courses avec total et budget', 'Mitrechner&nbsp;: d&eacute;penses par mois et articles les plus chers', 'Mitrechner&nbsp;: listes de courses pr&eacute;par&eacute;es']),
  'es': dict(
   titel='Mitrechner | Sabe cu&aacute;nto llevas al comprar',
   beschreibung='Mitrechner te dice al momento cu&aacute;nto cuesta todo lo que compras, as&iacute; no pierdes la cuenta. Sin registro, sin anuncios, para iPhone.',
   erster='Anotas lo que compras, cu&aacute;ntos y cu&aacute;nto cuesta. Mitrechner hace las cuentas al momento y arriba ves el total. Ves en la tienda cuando ya es mucho, y todav&iacute;a puedes regresar algo. As&iacute; hasta puedes ahorrar un poco.',
   h2a='Mitrechner Plus',
   pa='Ponte un presupuesto y siempre ves cu&aacute;nto te queda. Escribe tus listas desde la casa. Y despu&eacute;s ves cu&aacute;nto gastaste cada mes y qu&eacute; compras m&aacute;s. Plus lo pagas una vez, no hay suscripci&oacute;n.',
   h2b='En tu idioma',
   pb='Mitrechner est&aacute; en espa&ntilde;ol, ingl&eacute;s, alem&aacute;n y franc&eacute;s. La moneda va seg&uacute;n tu pa&iacute;s, por ejemplo pesos, d&oacute;lares o euros.',
   letzter='Sin cuenta, sin anuncios. Lo que anotas se queda en tu celular.',
   shots=['Mitrechner: una lista de compras con total y presupuesto', 'Mitrechner: gastos por mes y los art&iacute;culos m&aacute;s caros', 'Mitrechner: listas de compras preparadas']),
}


# ---------------------------------------------------------------------------
# Karma Farmer (3.10.2026). Dieselben Saetze wie im Store (karma_farmer/tool/store.py),
# im Ton des Inhabers. Nur, was die App wirklich kann: eine Mission am Tag in fuenf
# Bereichen, 20 Stufen, 200 Missionen, Streak, Reflexionen auf dem Geraet, Erinnerung nur
# auf Wunsch, Glow als Einmalkauf (kein Abo), kein Konto, keine Werbung.
# ---------------------------------------------------------------------------

for _s, (_og, _mehr, _text, _start) in {
    'de': ('Symbol der App Karma Farmer', 'Mehr zu Karma Farmer',
           'Jeden Tag eine kleine Mission: mal f&uuml;rs Klima, mal f&uuml;r andere, mal f&uuml;r dich. '
           'Du machst sie, und deine Pflanze w&auml;chst mit.',
           ' Karma Farmer, jeden Tag eine gute Tat, f&uuml;r iPhone.'),
    'en': ('Karma Farmer app icon', 'More about Karma Farmer',
           'One small mission a day: something for the planet, for others or for yourself. '
           'You do it, and your plant grows with you.',
           ' Karma Farmer, one good deed a day, for iPhone.'),
    'fr': ('Ic&ocirc;ne de l&rsquo;application Karma Farmer', 'En savoir plus sur Karma Farmer',
           'Une petite mission par jour&nbsp;: pour la plan&egrave;te, pour les autres ou pour toi. '
           'Tu la fais, et ta plante grandit avec toi.',
           ' Karma Farmer, une bonne action par jour, pour iPhone.'),
    'es': ('Icono de la app Karma Farmer', 'M&aacute;s sobre Karma Farmer',
           'Una peque&ntilde;a misi&oacute;n al d&iacute;a: algo por el planeta, por los dem&aacute;s o por ti. '
           'La haces y tu planta crece contigo.',
           ' Karma Farmer, una buena acci&oacute;n al d&iacute;a, para iPhone.'),
}.items():
    T[_s]['og_alt']['karma-farmer'] = _og
    T[_s]['mehr']['karma-farmer'] = _mehr
    T[_s]['kf_text'] = _text
    if 'karma-farmer' not in AUS:
        T[_s]['beschreibung'] += _start

P['karma-farmer'] = {
  'de': dict(
   titel='Karma Farmer | Jeden Tag eine gute Tat',
   beschreibung='Karma Farmer gibt dir jeden Tag eine kleine Mission. Du machst sie, und deine '
                'Pflanze w&auml;chst mit. Ohne Konto, ohne Werbung, f&uuml;r iPhone.',
   erster='Du schaust, was heute dran ist, machst es und tippst auf &bdquo;Mission '
          'abschlie&szlig;en&ldquo;. Daf&uuml;r gibt&rsquo;s Karma. Es gibt 20 Stufen, vom kleinen '
          'Samen bis zum Weltbaum, und 200 Missionen in f&uuml;nf Bereichen. Du suchst dir aus, '
          'was dir wichtig ist.',
   h2a='Karma Farmer Glow',
   pa='Glow kaufst du einmal, ein Abo gibt es nicht. Damit kannst du einmal pro Woche einen '
      'verpassten Tag reparieren und einmal pro Woche deine Mission wechseln. Dazu kommen die '
      'Galerie mit allen deinen Pflanzen und eine Statistik.',
   h2b='In deiner Sprache',
   pb='Karma Farmer gibt es auf Deutsch, Englisch, Spanisch und Franz&ouml;sisch. Eine '
      'Erinnerung gibt&rsquo;s auch, zu der Uhrzeit, die du willst (und nur wenn du willst).',
   letzter='Kein Konto, keine Werbung. Was du schreibst, bleibt auf deinem Ger&auml;t.',
   shots=['Karma Farmer: die Mission des Tages und deine Pflanze',
          'Karma Farmer: eine neue Stufe',
          'Karma Farmer: deine Reflexionen']),
  'en': dict(
   titel='Karma Farmer | One good deed a day',
   beschreibung='Karma Farmer gives you one small mission every day. You do it, and your plant '
                'grows with you. No account, no ads, for iPhone.',
   erster='You check what&rsquo;s up today, do it and tap &ldquo;Complete '
          'mission&rdquo;. You get Karma for it. There are 20 levels, from a tiny seed to the '
          'World Tree, and 200 missions in five areas. You pick what matters to you.',
   h2a='Karma Farmer Glow',
   pa='You buy Glow once, there&rsquo;s no subscription. With it you can repair a missed day '
      'once a week and swap your mission once a week. You also get the gallery with all your '
      'plants and your stats.',
   h2b='In your language',
   pb='Karma Farmer speaks English, German, Spanish and French. There&rsquo;s a reminder too, '
      'at the time you want (and only if you want it).',
   letzter='No account, no ads. What you write stays on your device.',
   shots=['Karma Farmer: today&rsquo;s mission and your plant',
          'Karma Farmer: a new level',
          'Karma Farmer: your reflections']),
  'fr': dict(
   titel='Karma Farmer | Une bonne action par jour',
   beschreibung='Karma Farmer te donne une petite mission chaque jour. Tu la fais, et ta plante '
                'grandit avec toi. Sans compte, sans publicit&eacute;, pour iPhone.',
   erster='Tu regardes ce qu&rsquo;il y a aujourd&rsquo;hui, tu le fais et tu touches '
          '&laquo;&nbsp;Terminer la mission&nbsp;&raquo;. Tu gagnes du Karma. Il y a 20 niveaux, '
          'de la petite graine &agrave; l&rsquo;Arbre monde, et 200 missions dans cinq domaines. '
          'Tu choisis ce qui compte pour toi.',
   h2a='Karma Farmer Glow',
   pa='Glow, tu l&rsquo;ach&egrave;tes une fois, il n&rsquo;y a pas d&rsquo;abonnement. Avec '
      'lui, tu peux r&eacute;parer un jour manqu&eacute; une fois par semaine et changer ta '
      'mission une fois par semaine. Tu as aussi la galerie avec toutes tes plantes et tes '
      'statistiques.',
   h2b='Dans ta langue',
   pb='Karma Farmer parle fran&ccedil;ais, anglais, allemand et espagnol. Il y a aussi un '
      'rappel, &agrave; l&rsquo;heure que tu veux (et seulement si tu veux).',
   letzter='Pas de compte, pas de pub. Ce que tu &eacute;cris reste sur ton appareil.',
   shots=['Karma Farmer&nbsp;: la mission du jour et ta plante',
          'Karma Farmer&nbsp;: un nouveau niveau',
          'Karma Farmer&nbsp;: tes r&eacute;flexions']),
  'es': dict(
   titel='Karma Farmer | Una buena acci&oacute;n al d&iacute;a',
   beschreibung='Karma Farmer te da una peque&ntilde;a misi&oacute;n cada d&iacute;a. La haces '
                'y tu planta crece contigo. Sin cuenta, sin anuncios, para iPhone.',
   erster='Ves qu&eacute; toca hoy, lo haces y tocas &laquo;Completar misi&oacute;n&raquo;. Ganas Karma. Hay '
          '20 niveles, de una semillita al &Aacute;rbol del mundo, y 200 misiones en cinco '
          '&aacute;reas. T&uacute; eliges lo que te importa.',
   h2a='Karma Farmer Glow',
   pa='Glow lo pagas una vez, no hay suscripci&oacute;n. Con &eacute;l puedes reparar un '
      'd&iacute;a perdido una vez por semana y cambiar tu misi&oacute;n una vez por semana. '
      'Adem&aacute;s tienes la galer&iacute;a con todas tus plantas y tus estad&iacute;sticas.',
   h2b='En tu idioma',
   pb='Karma Farmer habla espa&ntilde;ol, ingl&eacute;s, alem&aacute;n y franc&eacute;s. '
      'Tambi&eacute;n hay un recordatorio, a la hora que quieras (y solo si quieres).',
   letzter='Sin cuenta, sin anuncios. Lo que escribes se queda en tu dispositivo.',
   shots=['Karma Farmer: la misi&oacute;n del d&iacute;a y tu planta',
          'Karma Farmer: un nivel nuevo',
          'Karma Farmer: tus reflexiones']),
}


# ---------------------------------------------------------------------------
# Freelancerito (4.10.2026). Nur, was die App wirklich kann (lib/l10n/app_de.arb und README im
# App-Projekt): Stundenwert, Aufwand in fuenf Teilen, direkte Kosten, Puffer, daraus
# Mindestpreis, Zielpreis und Premium, alles aus den eigenen Werten und ausdruecklich keine
# Marktpreise. Simulator, Rabatt und Mehraufwand kostenlos und ohne Grenzen, Plus als
# Einmalkauf (kein Abo). Keine Steuern, kein Konto, keine Werbung, kein Tracking, keine KI.
# Kein Kaufpreis fuer Plus, wie bei den anderen Apps. Das Rechenbeispiel ist das aus der
# README der App, nachgerechnet. Die App spricht nur Deutsch und Englisch: die franzoesische
# und spanische Seite sagen das offen, statt "in deiner Sprache" zu versprechen.
# ---------------------------------------------------------------------------

for _s, (_og, _mehr, _text, _start) in {
    'de': ('Symbol der App Freelancerito', 'Mehr zu Freelancerito',
           'Finde heraus, was du f&uuml;r einen Auftrag verlangen solltest, bevor du zusagst. '
           'Gerechnet wird mit deinen eigenen Werten, nicht mit Marktpreisen.',
           ' Freelancerito, der Preisrechner f&uuml;r Freelancer und Selbstst&auml;ndige, f&uuml;r iPhone.'),
    'en': ('Freelancerito app icon', 'More about Freelancerito',
           'Find out what to charge for a job before you say yes. '
           'It works with your own values, not with market prices.',
           ' Freelancerito, the price calculator for freelancers and the self-employed, for iPhone.'),
    'fr': ('Ic&ocirc;ne de l&rsquo;application Freelancerito', 'En savoir plus sur Freelancerito',
           'D&eacute;couvre combien demander pour une mission avant de dire oui. '
           'Le calcul part de tes propres valeurs, pas des prix du march&eacute;.',
           ' Freelancerito, le calculateur de prix pour freelances et ind&eacute;pendants, pour iPhone.'),
    'es': ('Icono de la app Freelancerito', 'M&aacute;s sobre Freelancerito',
           'Descubre cu&aacute;nto cobrar por un trabajo antes de decir que s&iacute;. '
           'Con tus propios valores, no con precios de mercado.',
           ' Freelancerito, la calculadora de precios para freelancers e independientes, para iPhone.'),
}.items():
    T[_s]['og_alt']['freelancerito'] = _og
    T[_s]['mehr']['freelancerito'] = _mehr
    T[_s]['fl_text'] = _text
    if 'freelancerito' not in AUS:
        T[_s]['beschreibung'] += _start

# Ein Abschnitt mehr als bei den anderen Apps (h2sim, psim): der Simulator. Er ist kostenlos und
# steht deshalb vor Plus. Die Alt-Texte der Fotos sind geschrieben, bevor es die Fotos gibt:
# sobald sie da sind, gegen die Bilder pruefen.
P['freelancerito'] = {
  'de': dict(
   titel='Freelancerito | Preisrechner f&uuml;r Freelancer und Selbstst&auml;ndige',
   beschreibung='Freelancerito rechnet dir aus, was du f&uuml;r einen Auftrag verlangen solltest: '
                'Mindestpreis, Zielpreis und Premium, aus deinen eigenen Werten. Ohne Konto, ohne '
                'Werbung, f&uuml;r iPhone.',
   erster='Du tr&auml;gst ein, was dir eine Stunde deiner Zeit wert sein soll. Dann, wie viel Arbeit '
          'wirklich im Auftrag steckt, auch Kommunikation, Vorbereitung und Korrekturen. Dazu kommen '
          'die direkten Kosten, etwa Material oder Fahrten, und ein Sicherheitspuffer f&uuml;r das '
          'Unerwartete. Daraus werden drei Preise. Unter dem Mindestpreis liegst du unter deiner '
          'eigenen Kalkulation. Mit dem Zielpreis gehst du in dein Angebot. Premium l&auml;sst dir '
          'mehr Spielraum, wenn der Auftrag besonders wertvoll, eilig oder anspruchsvoll ist. '
          'Steuern rechnet Freelancerito bewusst nicht mit.',
   h2sim='Preis testen',
   psim='Im Simulator schiebst du den Preis zwischen Mindestpreis und Premium hin und her und '
        'siehst sofort den effektiven Wert deiner Zeit: was nach den direkten Kosten pro Stunde '
        'Aufwand bleibt. Du kannst einen Rabatt ausprobieren, bevor du ihn gibst, und sehen, was '
        'passiert, wenn es l&auml;nger dauert. Ein Beispiel: 60&nbsp;&euro; pro Stunde, 11 Stunden '
        'Aufwand, 80&nbsp;&euro; Kosten und 15&nbsp;% Puffer ergeben 850, 890 und 1.050&nbsp;&euro;. '
        'Bei 890&nbsp;&euro; ist deine Stunde 73,64&nbsp;&euro; wert. Mit 100&nbsp;&euro; Rabatt sind '
        'es noch 64,55&nbsp;&euro;, mit zwei Stunden mehr 62,31&nbsp;&euro;.',
   h2a='Freelancerito Plus',
   pa='Der ganze Rechner und alle Simulatoren sind kostenlos, ohne Grenzen. Plus kaufst du einmal, '
      'ein Abo gibt es nicht. Damit speicherst du Kalkulationen und findest sie im Verlauf wieder. '
      'Du legst eigene Standardwerte und Kostenarten an, h&auml;ltst Szenarien fest und teilst eine '
      'Kalkulation als PDF oder Text.',
   h2b='In deiner Sprache',
   pb='Freelancerito gibt es auf Deutsch und Englisch. Du rechnest in Euro, Schweizer Franken, Pfund '
      'oder Dollar.',
   letzter='Kein Konto, keine Werbung, kein Tracking, keine KI. Freelancerito funktioniert ohne '
           'Internet, und was du eintr&auml;gst, bleibt auf deinem Ger&auml;t.',
   shots=['Freelancerito: Mindestpreis, Zielpreis und Premium f&uuml;r einen Auftrag',
          'Freelancerito: der Simulator mit dem effektiven Wert deiner Zeit',
          'Freelancerito: der Aufwand eines Auftrags, Schritt f&uuml;r Schritt']),
  'en': dict(
   titel='Freelancerito | Price calculator for freelancers',
   beschreibung='Freelancerito works out what you should charge for a job: a minimum price, a target '
                'price and a premium, all from your own values. No account, no ads, for iPhone.',
   erster='You enter what one hour of your time should be worth to you. Then how much work the job '
          'really involves, including communication, preparation and corrections. Add the direct '
          'costs, such as materials or travel, and a safety buffer for the unexpected. That gives '
          'you three prices. Below the minimum price, you fall below your own calculation. The '
          'target price is a sensible price to start your offer with. The premium gives you more '
          'room when the job is especially valuable, urgent or demanding. Freelancerito deliberately '
          'leaves taxes out.',
   h2sim='Test your price',
   psim='In the simulator you move the price between minimum and premium and see the effective '
        'value of your time right away: what is left per hour of effort after direct costs. You can '
        'try out a discount before you give it, and see what happens if the job takes longer. An '
        'example: &euro;60 an hour, 11 hours of effort, &euro;80 in costs and a 15% buffer give you '
        '&euro;850, &euro;890 and &euro;1,050. At &euro;890 your hour is worth &euro;73.64. With a '
        '&euro;100 discount it drops to &euro;64.55, with two extra hours to &euro;62.31.',
   h2a='Freelancerito Plus',
   pa='The whole calculator and all simulators are free, without limits. You buy Plus once, there '
      'is no subscription. With it you save your calculations and find them again in your history. '
      'You set your own defaults and cost types, keep scenarios and share a calculation as a PDF or '
      'as text.',
   h2b='In your language',
   pb='Freelancerito is available in English and German. You can work in euros, Swiss francs, '
      'pounds or dollars.',
   letzter='No account, no ads, no tracking, no AI. Freelancerito works offline, and what you enter '
           'stays on your device.',
   shots=['Freelancerito: minimum price, target price and premium for a job',
          'Freelancerito: the simulator with the effective value of your time',
          'Freelancerito: the effort of a job, step by step']),
  'fr': dict(
   titel='Freelancerito | Calculateur de prix pour freelances',
   beschreibung='Freelancerito calcule ce que tu devrais demander pour une mission&nbsp;: prix '
                'minimum, prix cible et premium, &agrave; partir de tes propres valeurs. Sans compte, '
                'sans publicit&eacute;, pour iPhone.',
   erster='Tu indiques ce que doit valoir une heure de ton temps. Puis le travail que la mission '
          'demande vraiment, communication, pr&eacute;paration et corrections comprises. Ensuite '
          'les co&ucirc;ts directs, comme le mat&eacute;riel ou les d&eacute;placements, et une marge '
          'de s&eacute;curit&eacute; pour l&rsquo;impr&eacute;vu. Tu obtiens trois prix. Sous le prix '
          'minimum, tu passes sous ton propre calcul. Le prix cible est un prix raisonnable pour '
          'commencer ton offre. Le premium te laisse plus de marge quand la mission est '
          'particuli&egrave;rement pr&eacute;cieuse, urgente ou exigeante. Freelancerito ne calcule '
          'volontairement pas les imp&ocirc;ts.',
   h2sim='Tester ton prix',
   psim='Dans le simulateur, tu d&eacute;places le prix entre le minimum et le premium et tu vois '
        'tout de suite la valeur effective de ton temps&nbsp;: ce qui reste par heure de travail '
        'apr&egrave;s les co&ucirc;ts directs. Tu peux essayer une remise avant de l&rsquo;accorder, '
        'et voir ce qui se passe si la mission prend plus de temps. Un exemple&nbsp;: 60&nbsp;&euro; '
        'de l&rsquo;heure, 11 heures de travail, 80&nbsp;&euro; de co&ucirc;ts et 15&nbsp;% de marge '
        'donnent 850, 890 et 1&nbsp;050&nbsp;&euro;. &Agrave; 890&nbsp;&euro;, ton heure vaut '
        '73,64&nbsp;&euro;. Avec 100&nbsp;&euro; de remise, elle tombe &agrave; 64,55&nbsp;&euro;, '
        'avec deux heures de plus &agrave; 62,31&nbsp;&euro;.',
   h2a='Freelancerito Plus',
   pa='Le calculateur et tous les simulateurs sont gratuits, sans limite. Plus, tu l&rsquo;ach&egrave;tes '
      'une fois, il n&rsquo;y a pas d&rsquo;abonnement. Avec lui, tu enregistres tes calculs et tu les '
      'retrouves dans l&rsquo;historique. Tu d&eacute;finis tes propres valeurs par d&eacute;faut et '
      'types de co&ucirc;ts, tu gardes des sc&eacute;narios et tu partages un calcul en PDF ou en '
      'texte.',
   h2b='En anglais et en allemand',
   pb='Freelancerito existe en anglais et en allemand, pas encore en fran&ccedil;ais. Sur un appareil '
      'r&eacute;gl&eacute; en fran&ccedil;ais, l&rsquo;application s&rsquo;affiche en anglais. Tu peux '
      'compter en euros, francs suisses, livres ou dollars.',
   letzter='Pas de compte, pas de pub, pas de pistage, pas d&rsquo;IA. Freelancerito fonctionne hors '
           'ligne, et ce que tu saisis reste sur ton appareil.',
   shots=['Freelancerito&nbsp;: prix minimum, prix cible et premium pour une mission',
          'Freelancerito&nbsp;: le simulateur avec la valeur effective de ton temps',
          'Freelancerito&nbsp;: le travail d&rsquo;une mission, &eacute;tape par &eacute;tape']),
  'es': dict(
   titel='Freelancerito | Calculadora de precios para freelancers',
   beschreibung='Freelancerito calcula cu&aacute;nto deber&iacute;as cobrar por un trabajo: precio '
                'm&iacute;nimo, precio objetivo y premium, a partir de tus propios valores. Sin cuenta, '
                'sin anuncios, para iPhone.',
   erster='Anotas cu&aacute;nto quieres que valga una hora de tu tiempo. Despu&eacute;s, cu&aacute;nto '
          'trabajo lleva de verdad el encargo, incluidas la comunicaci&oacute;n, la preparaci&oacute;n '
          'y las correcciones. Luego los gastos directos, como material o traslados, y un margen de '
          'seguridad para lo inesperado. Con eso obtienes tres precios. Por debajo del precio '
          'm&iacute;nimo, quedas por debajo de tu propio c&aacute;lculo. El precio objetivo es un '
          'precio razonable para empezar tu oferta. El premium te deja m&aacute;s margen cuando el '
          'trabajo es especialmente valioso, urgente o exigente. Freelancerito no calcula impuestos, '
          'a prop&oacute;sito.',
   h2sim='Prueba tu precio',
   psim='En el simulador mueves el precio entre el m&iacute;nimo y el premium y ves al momento el '
        'valor efectivo de tu tiempo: lo que queda por hora de trabajo despu&eacute;s de los gastos '
        'directos. Puedes probar un descuento antes de darlo y ver qu&eacute; pasa si el trabajo '
        'lleva m&aacute;s tiempo. Un ejemplo: 60&nbsp;&euro; la hora, 11 horas de trabajo, '
        '80&nbsp;&euro; de gastos y un margen del 15&nbsp;% dan 850, 890 y 1050&nbsp;&euro;. A '
        '890&nbsp;&euro;, tu hora vale 73,64&nbsp;&euro;. Con 100&nbsp;&euro; de descuento baja a '
        '64,55&nbsp;&euro;, con dos horas m&aacute;s a 62,31&nbsp;&euro;.',
   h2a='Freelancerito Plus',
   pa='La calculadora y todos los simuladores son gratis, sin l&iacute;mites. Plus lo pagas una vez, '
      'no hay suscripci&oacute;n. Con &eacute;l guardas tus c&aacute;lculos y los encuentras en el '
      'historial. Defines tus propios valores predeterminados y tipos de gastos, guardas escenarios '
      'y compartes un c&aacute;lculo como PDF o como texto.',
   h2b='En ingl&eacute;s y alem&aacute;n',
   pb='Freelancerito est&aacute; en ingl&eacute;s y alem&aacute;n, todav&iacute;a no en espa&ntilde;ol. '
      'En un dispositivo en espa&ntilde;ol, la app se muestra en ingl&eacute;s. Puedes calcular en '
      'euros, francos suizos, libras o d&oacute;lares.',
   letzter='Sin cuenta, sin anuncios, sin rastreo, sin IA. Freelancerito funciona sin conexi&oacute;n, '
           'y lo que anotas se queda en tu dispositivo.',
   shots=['Freelancerito: precio m&iacute;nimo, precio objetivo y premium para un trabajo',
          'Freelancerito: el simulador con el valor efectivo de tu tiempo',
          'Freelancerito: el trabajo de un encargo, paso a paso']),
}


def bild(sprache, nr, alt, app='shlayolotl'):
    """Ein Bildschirmfoto in drei Fassungen: AVIF, WebP, und das WebP als
    Rueckfall. Der Browser nimmt das erste Format, das er kann, und von den
    zwei Breiten die, die zu seinem Bildschirm passt."""
    b = '%s-%d' % (app + '-' + sprache, nr)
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
        <h2><a href="%(pfad)sshlayolotl/product/">Shlayolotl</a></h2>
      </div>
    </div>
    <p>%(shlay_text)s</p>
    <p class="mehr"><a href="%(pfad)sshlayolotl/product/">%(mehr_shlay)s</a></p>
    <div class="carousel" id="shots">
%(shots)s
    </div>
    <div class="punkte" data-fuer="shots"></div>
    <a class="badge" href="%(shlay_url)s">
      <img src="/assets/img/appstore-%(sprache)s.svg" alt="%(badge_alt)s" width="120" height="40">
    </a>
  </div>
</section>

%(mitr_abschnitt)s%(kf_abschnitt)s%(fl_abschnitt)s%(where_abschnitt)s</main>

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
           mehr_shlay=t['mehr']['shlayolotl'],
           mitr_abschnitt='' if 'mitrechner' in AUS else MITR_ABSCHNITT % dict(
               t, pfad=PFAD[sprache], symbol_mitr=symbol('mitrechner'),
               mehr_mitr=t['mehr']['mitrechner'], shots_mitr=galerie_html('mitrechner', sprache, 'shots-mitr'),
               knoepfe_mitr=knoepfe('mitrechner', sprache)),
           kf_abschnitt='' if 'karma-farmer' in AUS else KF_ABSCHNITT % dict(
               t, pfad=PFAD[sprache], symbol_kf=symbol('karma-farmer'),
               mehr_kf=t['mehr']['karma-farmer'], shots_kf=galerie_html('karma-farmer', sprache, 'shots-kf'),
               knoepfe_kf=knoepfe('karma-farmer', sprache)),
           fl_abschnitt='' if 'freelancerito' in AUS else FL_ABSCHNITT % dict(
               t, pfad=PFAD[sprache], symbol_fl=symbol('freelancerito'),
               mehr_fl=t['mehr']['freelancerito'], unten_fl=unten_html('freelancerito', sprache, 'shots-fl')),
           where_abschnitt='' if 'wheresome' in AUS else WHERE_ABSCHNITT % dict(
               t, pfad=PFAD[sprache], symbol_where=symbol('wheresome'),
               mehr_where=t['mehr']['wheresome']),
           ds_pfad=DS_PFAD[sprache], shlay_url=SHLAY_URL[sprache])


# Die Wheresome-Karte der Startseite, solange die App noch nicht im Store ist
# ausgeblendet (siehe OFFLINE).
MITR_ABSCHNITT = '''<section class="band mitr">
  <div class="wrap">
    <div class="kopf">
%(symbol_mitr)s
      <div>
        <h2><a href="%(pfad)smitrechner/product/">Mitrechner</a></h2>
      </div>
    </div>
    <p>%(mitr_text)s</p>
    <p class="mehr"><a href="%(pfad)smitrechner/product/">%(mehr_mitr)s</a></p>
%(shots_mitr)s
%(knoepfe_mitr)s
  </div>
</section>
'''


KF_ABSCHNITT = '''<section class="band karma">
  <div class="wrap">
    <div class="kopf">
%(symbol_kf)s
      <div>
        <h2><a href="%(pfad)skarma-farmer/product/">Karma Farmer</a></h2>
      </div>
    </div>
    <p>%(kf_text)s</p>
    <p class="mehr"><a href="%(pfad)skarma-farmer/product/">%(mehr_kf)s</a></p>
%(shots_kf)s
%(knoepfe_kf)s
  </div>
</section>
'''


# Freelancerito, solange die App in keinem Store ist, nur in der Vorschau (siehe OFFLINE).
FL_ABSCHNITT = '''<section class="band freel">
  <div class="wrap">
    <div class="kopf">
%(symbol_fl)s
      <div>
        <h2><a href="%(pfad)sfreelancerito/product/">Freelancerito</a></h2>
      </div>
    </div>
    <p>%(fl_text)s</p>
    <p class="mehr"><a href="%(pfad)sfreelancerito/product/">%(mehr_fl)s</a></p>
%(unten_fl)s
  </div>
</section>
'''


WHERE_ABSCHNITT = '''<section class="band where">
  <div class="wrap">
    <div class="kopf">
%(symbol_where)s
      <div>
        <p class="tag">%(where_tag)s</p>
        <h2><a href="%(pfad)swheresome/product/">Wheresome</a></h2>
      </div>
    </div>
    <p>%(where_text)s</p>
    <p class="mehr"><a href="%(pfad)swheresome/product/">%(mehr_where)s</a></p>
    <p class="soon">%(where_bald)s</p>
  </div>
</section>
'''


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


def galerie_html(app, sprache, kennung):
    """Die drei Bildschirmfotos einer App als Bilderreihe mit Punkten darunter.
    Die Fotos sind in der Sprache, in der die App dem Besucher begegnet (app_sprache).
    Leer, solange es die Fotos noch nicht gibt (Freelancerito, 4.10.2026): lieber keine
    Bilderreihe als drei kaputte Bilder."""
    alts = T[sprache]['shots'] if app == 'shlayolotl' else P[app][sprache]['shots']
    foto = app_sprache(app, sprache)
    if not all(os.path.exists(os.path.join(ROOT, 'assets', 'shots', '%s-%s-%d-420.webp' % (app, foto, i + 1)))
               for i in range(3)):
        return ''
    return ('    <div class="carousel" id="%s">\n%s\n    </div>\n'
            '    <div class="punkte" data-fuer="%s"></div>'
            % (kennung, '\n'.join(bild(foto, i + 1, alts[i], app) for i in range(3)), kennung))


def unten_html(app, sprache, kennung):
    """Bilderreihe und Knopf (oder „Bald im App Store."), ohne Leerzeile, wenn die Bilder fehlen."""
    return '\n'.join(x for x in (galerie_html(app, sprache, kennung), knoepfe(app, sprache)) if x)


# Googles Markenhinweis, nur auf Seiten, die das Abzeichen zeigen.
PLAY_MARKEN = {
    'de': 'Google Play und das Google-Play-Logo sind Marken von Google LLC.',
    'en': 'Google Play and the Google Play logo are trademarks of Google LLC.',
    'fr': 'Google Play et le logo Google Play sont des marques de Google LLC.',
    'es': 'Google Play y el logotipo de Google Play son marcas de Google LLC.',
}


def play_abzeichen(app, sprache):
    return app == 'mitrechner' and os.path.exists(
        os.path.join(ROOT, 'assets', 'img', 'googleplay-%s.png' % sprache))


def knoepfe(app, sprache):
    """App Store, und fuer Mitrechner auch Google Play, sobald das offizielle
    Abzeichen unter assets/img/googleplay-<sprache>.png liegt.

    Das Abzeichen gibt es nur im Partner Marketing Hub von Google, hinter
    deren Bedingungen; die nimmt der Inhaber selbst an (Stand 2.10.2026).
    Googles Regeln dafuer: Original, unveraendert, in der Sprache der Seite,
    Link auf den echten Play-Eintrag, Freiraum ein Viertel der Hoehe, und
    neben anderen Store-Abzeichen mindestens gleich gross. Die Bilder aus dem
    Hub haben oft einen durchsichtigen Rand: dann sichtbar nachmessen und die
    Hoehe so setzen, dass das sichtbare Abzeichen nicht kleiner ist als das
    von Apple."""
    t = T[sprache]
    if ((app == 'mitrechner' and not MITR_IM_STORE) or (app == 'karma-farmer' and not KF_IM_STORE)
            or (app == 'freelancerito' and not FL_IM_STORE)):
        return '    <p class="soon">%s</p>' % MITR_BALD[sprache]
    ziel = {'shlayolotl': SHLAY_URL[sprache], 'mitrechner': MITR_APPSTORE[sprache],
            'karma-farmer': KF_APPSTORE, 'freelancerito': FL_APPSTORE}.get(app) or '#'
    html = ('    <a class="badge" href="%s">\n'
            '      <img src="/assets/img/appstore-%s.svg" alt="%s" width="120" height="40">\n'
            '    </a>' % (ziel, sprache, t['badge_alt']))
    if play_abzeichen(app, sprache):
        html += ('\n    <a class="badge" href="%s">\n'
                 '      <img src="/assets/img/googleplay-%s.png" alt="%s" width="135" height="40">\n'
                 '    </a>' % (MITR_PLAY or '#', sprache, t['badge_play_alt']))
    return html


def produkt_pfade(app):
    return {s: PFAD[s] + app + '/product/' for s in SPRACHEN}


def produkt_seite(app, sprache):
    """Die Seite einer App. Fuer Shlayolotl mit den Bildern und dem Knopf von
    der Startseite, fuer Wheresome ohne, weil es noch nichts zu zeigen und
    nichts zu laden gibt. Unten der Link auf die Rechtsseite der App, die
    unter derselben Adresse ohne Schraegstrich liegt."""
    t = T[sprache]
    p = P[app][sprache]
    pfade = produkt_pfade(app)

    if app in ('shlayolotl', 'mitrechner', 'karma-farmer', 'freelancerito'):
        oben = ''
        text = ('      <p>%(erster)s</p>\n'
                + ('      <h2>%(h2sim)s</h2>\n'
                   '      <p>%(psim)s</p>\n' if 'h2sim' in p else '')
                + '      <h2>%(h2a)s</h2>\n'
                  '      <p>%(pa)s</p>\n'
                  '      <h2>%(h2b)s</h2>\n'
                  '      <p>%(pb)s</p>\n'
                  '      <p>%(letzter)s</p>') % p
        reihe = galerie_html(app, sprache, 'shots')
        unten = unten_html(app, sprache, 'shots')
        lead = {'shlayolotl': t['shlay_text'], 'mitrechner': t['mitr_text'], 'karma-farmer': t['kf_text'],
                'freelancerito': t['fl_text']}[app]
        # Ohne Bilderreihe keine Punkte, also auch kein Skript dafuer.
        skript = PUNKTE_SKRIPT if reihe else ''
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
    <p class="recht"><a href="%(recht_href)s">%(recht_text)s</a></p>
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
           stil=STIL, klasse={'shlayolotl': 'shlay', 'mitrechner': 'mitr', 'karma-farmer': 'karma',
                              'freelancerito': 'freel'}.get(app, 'where'),
           symbol=symbol(app), oben=oben, name=NAME.get(app, app.capitalize()), lead=lead,
           text=text, unten=unten, recht_href=recht_link(app, sprache)[0], recht_text=recht_link(app, sprache)[1],
           sprachen=sprachleiste(sprache, pfade), ds_pfad=DS_PFAD[sprache],
           skript=skript,
           marken=t['marken'] + (' ' + PLAY_MARKEN[sprache] if play_abzeichen(app, sprache) else ''))



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
    untereinander steht. Die Rechtsseiten der Apps tragen ohnehin alle vier (Freelancerito
    nur Deutsch und Englisch, siehe APP_SPRACHEN)."""
    t = T[sprache]
    pfade = {x: PFAD[x] + 'support/' for x in SPRACHEN}

    return VORLAGE_SUPPORT % dict(
        t, sprache=sprache, startpfad=PFAD[sprache],
        kopf=kopf(sprache, pfade, t['support_titel'],
                  t['support_beschreibung']),
        sprachen=sprachleiste(sprache, pfade), stil=SUPPORT_STIL,
        ds_pfad=DS_PFAD[sprache],
        support_wheresome='' if 'wheresome' in AUS else
        '  <h2>Wheresome</h2>\n  <p><a href="/wheresome#%s">%s</a></p>\n' % (sprache, t['support_recht']),
        support_freelancerito='' if 'freelancerito' in AUS else
        '  <h2>Freelancerito</h2>\n  <p><a href="%s">%s</a></p>\n\n' % recht_link('freelancerito', sprache))


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

  <h2>Mitrechner</h2>
  <p><a href="/mitrechner#%(sprache)s">%(support_recht)s</a></p>

  <h2>Karma Farmer</h2>
  <p><a href="/karma-farmer#%(sprache)s">%(support_recht)s</a></p>

%(support_freelancerito)s  <h2>Shlayolotl</h2>
  <p><a href="/shlayolotl#%(sprache)s">%(support_recht)s</a></p>

%(support_wheresome)s
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

DS_STAND = {'de': 'Stand: 2. Oktober 2026', 'en': 'Last updated: 2 October 2026',
            'fr': 'Mise &agrave; jour&nbsp;: 2 octobre 2026',
            'es': 'Actualizado: 2 de octubre de 2026'}

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
  kontakt2='E-Mails an contact@hollowspoon.app leitet die Cloudflare, Inc. (Anschrift siehe '
           'oben) in unserem Auftrag an unser Postfach bei Gmail weiter. Gmail ist ein Dienst '
           'der Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland; Google '
           'verarbeitet die Nachricht dort nach seiner eigenen Datenschutzerkl&auml;rung '
           '(policies.google.com/privacy) und kann sie auch auf Servern in den USA speichern. '
           'Cloudflare, Inc. und Google LLC sind nach dem EU-US Data Privacy Framework '
           'zertifiziert (nachgesehen am 2. Oktober 2026).',
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
  kontakt2='E-mails to contact@hollowspoon.app are forwarded on our behalf by Cloudflare, '
           'Inc. (address above) to our mailbox at Gmail. Gmail is a service of Google '
           'Ireland Limited, Gordon House, Barrow Street, Dublin 4, Ireland; Google '
           'processes the message there under its own privacy policy '
           '(policies.google.com/privacy) and may also store it on servers in the United '
           'States. Cloudflare, Inc. and Google LLC are certified under the EU-U.S. Data '
           'Privacy Framework (checked on 2 October 2026).',
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
  kontakt2='Les e-mails adress&eacute;s &agrave; contact@hollowspoon.app sont transf&eacute;r&eacute;s '
           'pour notre compte par Cloudflare, Inc. (adresse ci-dessus) vers notre bo&icirc;te '
           'de r&eacute;ception Gmail. Gmail est un service de Google Ireland Limited, Gordon '
           'House, Barrow Street, Dublin 4, Irlande&nbsp;; Google y traite le message selon sa '
           'propre politique de confidentialit&eacute; (policies.google.com/privacy) et peut '
           'aussi le stocker sur des serveurs aux &Eacute;tats-Unis. Cloudflare, Inc. et Google '
           'LLC sont certifi&eacute;es au titre du cadre de protection des donn&eacute;es '
           'UE-&Eacute;tats-Unis (v&eacute;rifi&eacute; le 2 octobre 2026).',
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
  kontakt2='Los correos a contact@hollowspoon.app los reenv&iacute;a, por encargo nuestro, '
           'Cloudflare, Inc. (direcci&oacute;n arriba) a nuestro buz&oacute;n de Gmail. Gmail es un '
           'servicio de Google Ireland Limited, Gordon House, Barrow Street, Dubl&iacute;n 4, '
           'Irlanda; Google trata all&iacute; el mensaje seg&uacute;n su propia pol&iacute;tica de '
           'privacidad (policies.google.com/privacy) y tambi&eacute;n puede almacenarlo en '
           'servidores de Estados Unidos. Cloudflare, Inc. y Google LLC est&aacute;n '
           'certificadas conforme al Marco de Privacidad de Datos UE-EE. UU. (comprobado el '
           '2 de octubre de 2026).',
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

BEHOERDE = ('Der Landesbeauftragte für Datenschutz und Informationsfreiheit<br>\n'
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
    <p>%(kontakt2)s</p>

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
    ZIEL = os.path.join(ROOT, '.vorschau') if VORSCHAU else ROOT
    if VORSCHAU:
        os.makedirs(ZIEL, exist_ok=True)
        for teil in ('assets', 'mitrechner.html', 'karma-farmer.html', 'freelancerito.html', 'shlayolotl.html',
                     'wheresome.html', 'impressum.html'):
            verweis = os.path.join(ZIEL, teil)
            if not os.path.lexists(verweis):
                os.symlink(os.path.join(ROOT, teil), verweis)
    for s in SPRACHEN:
        ordner = '' if s == 'de' else s + '/'
        schreibe(os.path.join(ZIEL, ordner + 'index.html'), seite(s))
        for app in APPS:
            schreibe(os.path.join(ZIEL, ordner + app + '/product/index.html'), produkt_seite(app, s))
        schreibe(os.path.join(ZIEL, ordner + 'support/index.html'), support_seite(s))
        schreibe(os.path.join(ZIEL, DS_DATEI[s]), datenschutz_seite(s))
    schreibe(os.path.join(ZIEL, 'sitemap.xml'), sitemap())
