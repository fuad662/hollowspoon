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
# offline wie Wheresome: Produktseiten und Karte gibt es nur in der Vorschau. Auf der
# Support-Seite steht Freelancerito seit 7.10.2026 trotzdem, wie Mitrechner und Karma Farmer
# vor ihrem Start (User: "und auch die Supportseite"). Die Rechtsseite /freelancerito liegt trotzdem schon da (aus dem App-Repository,
# tool/rechtsseite.py --site), weil App Store Connect sie als Datenschutz- und
# Support-Adresse braucht.
OFFLINE = {'wheresome', 'freelancerito'}
# `python3 bauen.py --vorschau` baut alles, auch was offline ist, nach .vorschau/
# (nicht im Repository). So laesst sich eine Seite ansehen, bevor sie online geht.
VORSCHAU = '--vorschau' in sys.argv
AUS = set() if VORSCHAU else OFFLINE
APPS = [app for app in ['shlayolotl', 'mitrechner', 'karma-farmer', 'freelancerito', 'capyroo-run', 'fumuon', 'wimmelino', 'capyroo-world', 'wheresome']
        if app not in AUS]
RECHT = {'shlayolotl': '/shlayolotl', 'wheresome': '/wheresome', 'mitrechner': '/mitrechner',
         'karma-farmer': '/karma-farmer', 'freelancerito': '/freelancerito',
         'capyroo-run': '/capyroo-run', 'fumuon': '/fumuon',
         'wimmelino': '/wimmelino', 'capyroo-world': '/capyroo-world'}
# Sprachen der App selbst, wo es nicht alle vier der Website sind. Freelancerito gab es am
# 4.10.2026 zuerst nur auf Deutsch und Englisch; noch am selben Tag kamen Spanisch und
# Franzoesisch dazu (Englisch ist dort Hauptsprache und Rueckfall). Seitdem spricht jede App
# alle vier, die Rechtsseite /freelancerito hat #de, #en, #es und #fr, und jede Seite zeigt
# die Fotos in ihrer eigenen Sprache. Die Mechanik bleibt fuer eine kuenftige App mit weniger
# Sprachen.
APP_SPRACHEN = {}
# Dazu ein Hinweis am Link, damit niemand Franzoesisch erwartet und Englisch bekommt
# (app_sprache und recht_link, weiter unten bei galerie_html).
AUF_ENGLISCH = {'de': ' (auf Englisch)', 'en': '', 'fr': ' (en anglais)', 'es': ' (en ingl&eacute;s)'}
# Angezeigter Name je App (die Adresse /karma-farmer/ hat einen Bindestrich, der Name nicht).
NAME = {'karma-farmer': 'Karma Farmer', 'capyroo-run': 'Capyroo Run', 'fumuon': 'Fumuon',
        'wimmelino': 'Wimmelino', 'capyroo-world': 'Capyroo World'}
# Apple-ID von Mitrechner: 6818615754 (App Store Connect, 2.10.2026). Ohne Land in der
# Adresse leitet Apple in den Store des Besuchers weiter; das passt, weil die spanische
# Fassung fuer Mexiko geschrieben ist und eine /es/-Adresse nach Spanien fuehren wuerde.
# Google Play folgt, sobald die App dort ist (dann auch das Abzeichen, siehe knoepfe).
MITR_APPSTORE = {s: 'https://apps.apple.com/app/mitrechner/id6818615754' for s in ('de', 'en', 'fr', 'es')}
# Bis Apple die App freigibt, zeigt die Seite statt des Knopfes „Bald im App Store.“: ein
# Knopf, der ins Leere fuehrt, verwirrt (User 3.10.2026). Nach der Freigabe auf True.
MITR_IM_STORE = True
MITR_BALD = {'de': 'Bald im App Store.', 'en': 'Coming soon to the App Store.',
             'fr': 'Bient&ocirc;t sur l&rsquo;App Store.', 'es': 'Muy pronto en el App Store.'}
# Seit 14.10.2026 bei Apple und bei Google Play (User: "mitrechner und karma farmer sind
# nun sowohl im appstore als auch bei google play"), beide Eintraege an dem Tag geprueft.
MITR_PLAY = 'https://play.google.com/store/apps/details?id=app.hollowspoon.mitrechner'
# Karma Farmer (3.10.2026: "lade ... die datenschutzseite hoch sowie die marketing seite").
# Wie Mitrechner: online, bevor Apple die App freigibt, mit „Bald im App Store." statt
# Knopf. Nach der Freigabe die Apple-ID eintragen und KF_IM_STORE auf True.
# Apple-ID 6818803808 (iTunes-Lookup ueber die Bundle-ID, 14.10.2026), ohne Land wie bei
# Mitrechner.
KF_APPSTORE = 'https://apps.apple.com/app/karma-farmer/id6818803808'
KF_IM_STORE = True
KF_PLAY = 'https://play.google.com/store/apps/details?id=app.hollowspoon.karmafarmer'
# Capyroo Run (11.10.2026, "baue sofort eine produktseite"): noch nicht im Store, also
# "Bald im App Store." statt Knopf. Nach der Freigabe die Apple-ID eintragen und CR_IM_STORE
# auf True. Die Seite steht NICHT auf der Startseite und nicht im Support (nur unter
# /capyroo-run/product/ und in der Sitemap), damit die anderen Seiten bleiben, wie sie sind.
CR_APPSTORE = None
CR_IM_STORE = False
# Freelancerito (4.10.2026): noch in keinem Store, keine Apple-ID, nicht bei Google Play.
# Wie bei Mitrechner und Karma Farmer steht auf der Seite „Bald im App Store." statt eines
# Knopfes, der ins Leere fuehrt. Zwei Schritte, die nicht zusammenfallen muessen: zum
# Freischalten freelancerito aus OFFLINE nehmen und STAND hochsetzen (ob schon vor Apples
# Freigabe, wie bei Mitrechner und Karma Farmer, entscheidet der Inhaber); nach der Freigabe
# die App-Store-Adresse in FL_APPSTORE eintragen und FL_IM_STORE auf True. Google Play
# folgt, sobald die App dort ist.
FL_APPSTORE = None
FL_IM_STORE = False
FL_PLAY = None
# Fumuon (20.10.2026, "kannst du ... ne seite auf meiner webseite erstellen fuer fumuon?"): seit
# Oktober bei Google Play (Eintrag am 20.10. geprueft), bei Apple noch in der Pruefung. Wie Capyroo
# Run nur als eigene Seite unter /fumuon/product/ und in der Sitemap, nicht auf der Startseite.
# Nach Apples Freigabe die Apple-ID in FU_APPSTORE eintragen und FU_IM_STORE auf True.
FU_APPSTORE = None
FU_IM_STORE = False
FU_PLAY = 'https://play.google.com/store/apps/details?id=app.hollowspoon.fumuon'
# Wimmelino (20.10.2026, "seite fuer wimmelino und capyroo world auch schonmal hochladen"): seit
# 19.10.2026 im App Store (iTunes-Lookup ueber die Bundle-ID, Apple-ID 6821570689, ohne Land wie
# bei Mitrechner), noch nicht bei Google Play. Steht als neueste App ganz vorn auf der Startseite.
WI_APPSTORE = 'https://apps.apple.com/app/wimmelino-find-hidden-things/id6821570689'
# Capyroo World: noch in keinem Store (Apple prueft noch). Wie Capyroo Run nur als eigene Seite
# unter /capyroo-world/product/ und in der Sitemap. Nach Apples Freigabe die Adresse in
# CW_APPSTORE, CW_IM_STORE auf True und die App vorn in START_APPS eintragen.
CW_APPSTORE = None
CW_IM_STORE = False

# Datum fuer <lastmod> in der Sitemap. Bewusst von Hand: wer den Inhalt einer
# Seite aendert, setzt es hoch. Bei jedem Bau automatisch zu stempeln saehe
# fleissig aus und sagte Google nichts, weil es dann immer "heute" hiesse.
STAND = '2026-10-20'

OG_LOCALE = {'de': 'de_DE', 'en': 'en_US', 'fr': 'fr_FR', 'es': 'es_ES'}
OG_BILD = {'start': '/assets/img/og-hollow-spoon.png',
           'shlayolotl': '/assets/img/og-shlayolotl.png',
           'wheresome': '/assets/img/og-wheresome.png',
           'mitrechner': '/assets/img/og-mitrechner.png',
           'karma-farmer': '/assets/img/og-karma-farmer.png',
           'freelancerito': '/assets/img/og-freelancerito.png',
           'capyroo-run': '/assets/img/og-capyroo-run.png',
           'fumuon': '/assets/img/og-fumuon.png',
           'wimmelino': '/assets/img/og-wimmelino.png',
           'capyroo-world': '/assets/img/og-capyroo-world.png'}

T = {
    'de': dict(
        titel='Hollow Spoon | Eine App. Eine Sache. Richtig gut.',
        support_titel='Support | Hollow Spoon',
        support_zeile='Schreib uns:',
        support_recht='Support und Datenschutzerkl&auml;rung',
        beschreibung='Kleine Apps mit Charakter: Axolotl zocken, Capybara '
                     'h&uuml;pfen, Pflanze wachsen lassen. Von Hollow Spoon aus Bremen.',
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
               'entwickeln eigene Apps und Spiele f&uuml;r iPhone und '
               'Android.',
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
               'own apps and games for iPhone and Android.',
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
               'iPhone et Android.',
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
               'nuestras propias apps y juegos para iPhone '
               'y Android.',
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

# Das Menue "Apps" oben rechts (14.10.2026: "oben ist dann ein dropdown reiter 'apps' wo
# alle apps stehen"). Ein <details>, also auch ohne Skript bedienbar; das Skript schliesst
# es nur beim Klick daneben.
MENUE_STIL = '''
  .rechts .menue { position: relative; display: inline-block; margin-left: 24px; }
  .menue summary { list-style: none; cursor: pointer; color: #5C6270; white-space: nowrap; }
  .menue summary::-webkit-details-marker { display: none; }
  .menue summary::after { content: ''; display: inline-block; width: 6px; height: 6px;
                          margin: 0 0 3px 7px; border-right: 1.5px solid currentColor;
                          border-bottom: 1.5px solid currentColor; transform: rotate(45deg); }
  .menue[open] summary::after { transform: rotate(-135deg); margin-bottom: -1px; }
  .menue summary:hover, .menue[open] summary { color: #14161A; }
  .menue .liste { position: absolute; right: 0; top: calc(100% + 12px); z-index: 20;
                  min-width: 210px; padding: 8px; background: #fff; border: 1px solid #E7E9ED;
                  border-radius: 14px; box-shadow: 0 12px 32px rgba(20,22,26,.12); }
  nav .rechts .menue .liste a { display: flex; align-items: center; gap: 12px; margin: 0;
                                padding: 8px 12px; border-radius: 9px; color: #14161A;
                                font-size: 15px; }
  .menue .liste a:hover { background: #F2F3F5; }
  .menue .liste img { width: 28px; height: 28px; border-radius: 7px; }
  @media (max-width: 720px) {
    .rechts .menue { margin-left: 18px; font-size: 13px; }
  }
'''

# Die Apps stehen auf der Startseite nebeneinander statt untereinander (14.10.2026: "ich
# will nicht, dass man immer tiefer scrollen muss"). Weiter geht es mit den Pfeilen, den
# Punkten darunter oder per Wischen. Die Baender sind gleich hoch, damit beim Blaettern
# nichts springt.
APPS_STIL = '''
  .apps { position: relative; }
  .apps-reihe { display: flex; overflow-x: auto; overflow-y: hidden; scroll-snap-type: x mandatory;
                scrollbar-width: none; -webkit-overflow-scrolling: touch; }
  .apps-reihe::-webkit-scrollbar { display: none; }
  .apps-reihe > .band { flex: 0 0 100%; min-width: 0; scroll-snap-align: start; scroll-snap-stop: always; }
  /* Wer durch die Bildschirmfotos wischt, blaettert nicht aus Versehen die App weiter. */
  .apps .carousel { overscroll-behavior-x: contain; }
  /* Die Pfeile auf Hoehe von Symbol und Name: sichtbar, sobald die App anfaengt, und am
     Rechner neben der Textspalte statt darauf. */
  .apps-pfeil { position: absolute; top: 94px; transform: translateY(-50%); z-index: 2;
                width: 46px; height: 46px; padding: 0; border: 0; border-radius: 50%;
                background: rgba(255,255,255,.9); color: #14161A; cursor: pointer;
                box-shadow: 0 4px 14px rgba(0,0,0,.18); }
  .apps-pfeil:hover { background: #fff; }
  .apps-pfeil::before { content: ''; position: absolute; top: 50%; left: 50%; width: 11px; height: 11px;
                        border-top: 2.5px solid currentColor; border-right: 2.5px solid currentColor; }
  .apps-pfeil.zurueck { left: max(12px, calc(50% - 620px)); }
  .apps-pfeil.zurueck::before { transform: translate(-35%, -50%) rotate(-135deg); }
  .apps-pfeil.weiter { right: max(12px, calc(50% - 620px)); }
  .apps-pfeil.weiter::before { transform: translate(-65%, -50%) rotate(45deg); }
  .punkte.apps-punkte { display: flex; gap: 10px; justify-content: center; padding: 22px 0 8px; }
  .apps-punkte button { width: 10px; height: 10px; background: #D3D6DC; }
  .apps-punkte button[aria-current="true"] { background: #14161A; }
  @media (min-width: 721px) and (max-width: 1263px) {
    .apps .band .wrap { padding: 0 76px; }
  }
  @media (max-width: 720px) {
    .apps-pfeil { display: none; }
    .apps .carousel img { height: 48vh; }
  }
  /* Kompakt (14.10.2026: "irgendwie ist das zu gigantisch", dann "der bereich ist einfach
     zu hoch ... nur zwei bilder nutzen und die nach rechts"): auf der Startseite zwei
     Bilder rechts neben dem Text, schon ab Tablet-Breite (130 px waren
     dann "etwas zu klein", jetzt 170). Die Produktseiten zeigen
     weiter alle drei. */
  .apps .band { padding: 40px 0; }
  .apps .band .icon { width: 64px; border-radius: 15px; }
  .apps .band .kopf { gap: 16px; margin-bottom: 14px; }
  .apps .band h2 { font-size: clamp(28px, 3vw, 36px); }
  .apps .band p { margin-bottom: 18px; }
  .apps-pfeil { top: 50%; }
  @media (min-width: 721px) {
    .apps .band .wrap { display: grid; grid-template-columns: minmax(0, 1fr) auto;
                        grid-template-rows: auto 1fr; column-gap: 40px; align-items: start; }
    .apps .band .info { grid-column: 1; grid-row: 1; }
    .apps .band .kaufen { grid-column: 1; grid-row: 2; }
    .apps .band .carousel { grid-column: 2; grid-row: 1 / span 2; gap: 14px; margin-top: 0; padding-bottom: 0; }
    .apps .carousel img { width: 170px; }
    .apps .band .kaufen .badge { margin-top: 0; }
  }
'''


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
  .play { font-size: 15px; font-weight: 600; margin: 0; }
  .play a { color: inherit; }
  .punkte + .soon { margin-top: 26px; }
  .punkte + .knoepfe .soon, .text + .knoepfe .soon { margin-top: 26px; }

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
  }

  /* Die Seite einer App auf breiten Bildschirmen (User 20.10.2026: "aufm pc ist die seite
     scheisse ... nicht nur eine haelfte"): Text links, die drei Bilder rechts gross und
     aufgefaechert, beim Lesen mitlaufend. Nur auf den Produktseiten (.produkt), die Startseite
     bleibt, wie sie ist; Seiten ohne Bilder (Wheresome) haben nur die Textspalte. */
  @media (min-width: 980px) {
    .produkt .wrap { display: grid; grid-template-columns: minmax(0, 1fr) 470px; column-gap: 64px;
                     align-items: start; }
    .produkt .wrap > * { grid-column: 1; }
    .produkt .wrap > .carousel { grid-column: 2; grid-row: 1 / span 12; position: sticky; top: 48px;
                                 display: block; height: 640px; margin: 0; padding: 0; overflow: visible; }
    .produkt .carousel picture { position: absolute; top: 56px; transition: transform .3s ease; }
    .produkt .carousel img { width: 250px; border-radius: 22px;
                             box-shadow: 0 28px 60px rgba(0,0,0,.42), 0 0 0 1px rgba(255,255,255,.12); }
    .produkt .carousel picture:nth-child(1) { left: 110px; top: 0; z-index: 3; }
    .produkt .carousel picture:nth-child(2) { left: 0; transform: rotate(-7deg); z-index: 2; }
    .produkt .carousel picture:nth-child(3) { left: 220px; transform: rotate(7deg); z-index: 1; }
    .produkt .carousel:hover picture:nth-child(2) { transform: rotate(-9deg) translateX(-14px); }
    .produkt .carousel:hover picture:nth-child(3) { transform: rotate(9deg) translateX(14px); }
  }''' + MENUE_STIL + APPS_STIL


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
           ' Mitrechner, die Einkaufsliste mit &Uuml;berblick, f&uuml;r iPhone und Android.'),
    'en': ('Mitrechner app icon', 'More about Mitrechner',
           'The shopping list that keeps track. You always know what your shopping costs while you are still in the store.',
           'Get it on Google Play',
           ' Mitrechner, the shopping list that keeps track of your total, for iPhone and Android.'),
    'fr': ('Ic&ocirc;ne de l&rsquo;application Mitrechner', 'En savoir plus sur Mitrechner',
           'La liste de courses qui affiche ton total. Tu sais toujours combien co&ucirc;tent tes courses, d&eacute;j&agrave; dans le magasin.',
           'Disponible sur Google Play',
           ' Mitrechner, la liste de courses qui affiche ton total, pour iPhone et Android.'),
    'es': ('Icono de la app Mitrechner', 'M&aacute;s sobre Mitrechner',
           'La lista de compras que te dice cu&aacute;nto llevas. Siempre sabes cu&aacute;nto vas a pagar, desde que est&aacute;s en la tienda.',
           'Disponible en Google Play',
           ' Mitrechner, la lista de compras que te dice cu&aacute;nto llevas, para iPhone y Android.'),
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
   beschreibung='Mitrechner zeigt dir beim Einkaufen sofort, was alles zusammen kostet. So beh&auml;ltst du den &Uuml;berblick. Kein Konto, keine Werbung, f&uuml;r iPhone und Android.',
   erster='Du tippst ein, was du kaufst, wie viel davon und was es kostet. Mitrechner rechnet sofort mit und zeigt oben die Summe. Du siehst schon im Laden, wenn es zu viel wird, und kannst noch etwas zur&uuml;cklegen. Vielleicht sparst du so sogar Geld.',
   h2a='Mitrechner Plus',
   pa='Setz dir ein Budget, dann siehst du immer, wie viel noch &uuml;brig ist. Schreib deine Listen schon zu Hause. Und schau dir sp&auml;ter an, was du in jedem Monat ausgegeben hast und was du am meisten kaufst. Plus kaufst du einmal, ein Abo gibt es nicht.',
   h2b='In deiner Sprache',
   pb='Mitrechner gibt es auf Deutsch, Englisch, Spanisch und Franz&ouml;sisch. Die W&auml;hrung richtet sich nach deinem Land, also zum Beispiel Euro, Dollar oder Pesos.',
   letzter='Kein Konto, keine Werbung. Was du eintippst, bleibt auf deinem Handy.',
   shots=['Mitrechner: eine Einkaufsliste mit Gesamtsumme und Budget', 'Mitrechner: Ausgaben je Monat und die teuersten Artikel', 'Mitrechner: vorbereitete Einkaufslisten']),
  'en': dict(
   titel='Mitrechner | Know your total as you shop',
   beschreibung='Mitrechner shows you right away what your shopping costs, so you keep track of your spending. No account, no ads, for iPhone and Android.',
   erster='Type in what you buy, how many and what it costs. Mitrechner does the math right away and shows the total at the top. You can see in the store when it is getting to be too much, and still put something back. You might even save some money that way.',
   h2a='Mitrechner Plus',
   pa='Set a budget and always see how much is left. Write your lists at home. And later, see what you spent each month and what you buy most. You buy Plus once, there is no subscription.',
   h2b='In your language',
   pb='Mitrechner is available in English, German, Spanish and French. The currency goes by your country, so for example dollars, euros or pesos.',
   letzter='No account, no ads. What you type in stays on your phone.',
   shots=['Mitrechner: a shopping list with total and budget', 'Mitrechner: spending per month and the priciest items', 'Mitrechner: shopping lists written ahead of time']),
  'fr': dict(
   titel='Mitrechner | Ton total pendant tes courses',
   beschreibung='Mitrechner te montre tout de suite combien co&ucirc;tent tes courses, pour garder le contr&ocirc;le. Sans compte, sans pub, pour iPhone et Android.',
   erster='Tu notes ce que tu ach&egrave;tes, combien et le prix. Mitrechner calcule tout de suite et affiche le total en haut. Tu vois au magasin quand &ccedil;a fait trop, et tu peux encore reposer quelque chose. Tu peux m&ecirc;me faire des &eacute;conomies.',
   h2a='Mitrechner Plus',
   pa='Fixe-toi un budget et vois toujours ce qu&rsquo;il te reste. Pr&eacute;pare tes listes &agrave; la maison. Et ensuite, regarde ce que tu as d&eacute;pens&eacute; chaque mois et ce que tu ach&egrave;tes le plus. Plus, tu l&rsquo;ach&egrave;tes une fois, il n&rsquo;y a pas d&rsquo;abonnement.',
   h2b='Dans ta langue',
   pb='Mitrechner existe en fran&ccedil;ais, anglais, allemand et espagnol. La monnaie d&eacute;pend de ton pays, par exemple euros, dollars ou pesos.',
   letzter='Pas de compte, pas de pub. Ce que tu notes reste sur ton t&eacute;l&eacute;phone.',
   shots=['Mitrechner&nbsp;: une liste de courses avec total et budget', 'Mitrechner&nbsp;: d&eacute;penses par mois et articles les plus chers', 'Mitrechner&nbsp;: listes de courses pr&eacute;par&eacute;es']),
  'es': dict(
   titel='Mitrechner | Sabe cu&aacute;nto llevas al comprar',
   beschreibung='Mitrechner te dice al momento cu&aacute;nto cuesta todo lo que compras, as&iacute; no pierdes la cuenta. Sin registro, sin anuncios, para iPhone y Android.',
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
           ' Karma Farmer, jeden Tag eine gute Tat, f&uuml;r iPhone und Android.'),
    'en': ('Karma Farmer app icon', 'More about Karma Farmer',
           'One small mission a day: something for the planet, for others or for yourself. '
           'You do it, and your plant grows with you.',
           ' Karma Farmer, one good deed a day, for iPhone and Android.'),
    'fr': ('Ic&ocirc;ne de l&rsquo;application Karma Farmer', 'En savoir plus sur Karma Farmer',
           'Une petite mission par jour&nbsp;: pour la plan&egrave;te, pour les autres ou pour toi. '
           'Tu la fais, et ta plante grandit avec toi.',
           ' Karma Farmer, une bonne action par jour, pour iPhone et Android.'),
    'es': ('Icono de la app Karma Farmer', 'M&aacute;s sobre Karma Farmer',
           'Una peque&ntilde;a misi&oacute;n al d&iacute;a: algo por el planeta, por los dem&aacute;s o por ti. '
           'La haces y tu planta crece contigo.',
           ' Karma Farmer, una buena acci&oacute;n al d&iacute;a, para iPhone y Android.'),
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
                'Pflanze w&auml;chst mit. Ohne Konto, ohne Werbung, f&uuml;r iPhone und Android.',
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
                'grows with you. No account, no ads, for iPhone and Android.',
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
                'grandit avec toi. Sans compte, sans publicit&eacute;, pour iPhone et Android.',
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
                'y tu planta crece contigo. Sin cuenta, sin anuncios, para iPhone y Android.',
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
# Capyroo Run (11.10.2026). Dieselben Saetze wie im Store (capyroo_runner/tools/store/store.py),
# nur, was das Spiel wirklich kann: ein Finger, Doppelsprung, Besucher am Himmel, zwoelf
# Landschaften, 15 Skins, 15 Glueh­wuermchen, 20 Spuren, 48 Missionen, Tageslauf, Werbung nur
# zwischen zwei Laeufen, Werbefrei als Einmalkauf, kein Konto.
# ---------------------------------------------------------------------------

for _s, (_og, _text, _start) in {
    'de': ('Symbol der App Capyroo Run',
           'Ein Capybara, ein kleiner Planet, ein Finger. Wie weit kommst du?', ''),
    'en': ('Capyroo Run app icon',
           'One capybara, one tiny planet, one finger. How far will you get?', ''),
    'fr': ('Ic&ocirc;ne de l&rsquo;application Capyroo Run',
           'Un capybara, une petite plan&egrave;te, un doigt. Jusqu&rsquo;o&ugrave; iras-tu&nbsp;?', ''),
    'es': ('Icono de la app Capyroo Run',
           'Un carpincho, un planeta peque&ntilde;o, un dedo. &iquest;Hasta d&oacute;nde llegar&aacute;s?', ''),
}.items():
    T[_s]['og_alt']['capyroo-run'] = _og
    T[_s]['cr_text'] = _text

P['capyroo-run'] = {
  'de': dict(
   titel='Capyroo Run | Ein Tipp, und Capyroo fliegt',
   beschreibung='Capyroo rennt um einen kleinen Planeten, und du springst mit einem Finger. '
                'Ohne Konto, f&uuml;r iPhone.',
   erster='Capyroo rennt um einen kleinen Planeten. Tippen hei&szlig;t springen, Halten hei&szlig;t '
          'h&ouml;her, und in der Luft noch mal tippen ist der Doppelsprung. Unterwegs warten '
          'Baumst&auml;mme, L&uuml;cken, Felsen und Plattformen in zwei H&ouml;hen, und je weiter du '
          'kommst, desto schneller wird es.',
   h2a='&Uuml;ber dir ist was los',
   pa='Ein Wal zieht vorbei, ein Delfin, ein Astronaut, ein Ballon, und ganze Planeten gehen am '
      'Horizont auf. Dazu zw&ouml;lf Landschaften, vom Morgenrot bis zum Polarlicht.',
   h2b='Mach Capyroo zu deinem',
   pb='Mit deinen Funken holst du dir 15 Skins, 15 Gl&uuml;hw&uuml;rmchen, 20 Spuren und eigene '
      'Tricks. Dazu vier Power-ups in f&uuml;nf Stufen, 48 Missionen und jeden Tag ein Tageslauf, '
      'der f&uuml;r alle gleich ist. Funken kann man nicht kaufen, die erspielst du. Ein paar '
      'besondere Skins, Tricks und eine Spur gibt es einzeln, und mit &bdquo;Werbung '
      'entfernen&ldquo; (einmal kaufen, kein Abo) ist die Werbung weg.',
   letzter='Kein Konto. Werbung kommt nur zwischen zwei L&auml;ufen, nie beim Laufen. Capyroo Run '
           'gibt es auf Deutsch, Englisch, Franz&ouml;sisch und Spanisch.',
   shots=['Capyroo Run: ein Salto unterm Wal',
          'Capyroo Run: Planeten gehen vor dir auf',
          'Capyroo Run: hoch oben im Pilzwald']),
  'en': dict(
   titel='Capyroo Run | One tap and Capyroo flies',
   beschreibung='Capyroo runs around a tiny planet, and you jump with one finger. No account, '
                'for iPhone.',
   erster='Capyroo runs around a tiny planet. Tap to jump, hold to jump higher, and tap again '
          'in the air for the double jump. On the way come logs, gaps, rocks and platforms on two '
          'levels, and the further you get, the faster it goes.',
   h2a='Something&rsquo;s always going on above you',
   pa='A whale drifts by, a dolphin, an astronaut, a balloon, and whole planets rise on the '
      'horizon. Plus twelve landscapes, from dawn to northern lights.',
   h2b='Make Capyroo your own',
   pb='With your Sparks you get 15 skins, 15 fireflies, 20 trails and your own tricks. Plus four '
      'power-ups in five levels, 48 missions and every day a daily run that&rsquo;s the same for '
      'everyone. Sparks can&rsquo;t be bought, you earn them. A few special skins, tricks and a '
      'trail can be bought one by one, and with &ldquo;Remove Ads&rdquo; (buy once, no '
      'subscription) the ads are gone.',
   letzter='No account. Ads only come between two runs, never while you run. Capyroo Run is '
           'available in English, German, French and Spanish.',
   shots=['Capyroo Run: a flip under a whale',
          'Capyroo Run: planets rise ahead of you',
          'Capyroo Run: high up in the mushroom forest']),
  'fr': dict(
   titel='Capyroo Run | Une touche et Capyroo s&rsquo;envole',
   beschreibung='Capyroo court autour d&rsquo;une petite plan&egrave;te, et tu sautes avec un '
                'doigt. Sans compte, pour iPhone.',
   erster='Capyroo court autour d&rsquo;une petite plan&egrave;te. Touche pour sauter, maintiens '
          'pour sauter plus haut, et touche encore en l&rsquo;air pour le double saut. En chemin, '
          'il y a des troncs, des trous, des rochers et des plateformes sur deux hauteurs, et plus '
          'tu vas loin, plus &ccedil;a va vite.',
   h2a='Au-dessus de toi, il se passe toujours quelque chose',
   pa='Une baleine passe, un dauphin, un astronaute, une montgolfi&egrave;re, et des plan&egrave;tes '
      'enti&egrave;res se l&egrave;vent &agrave; l&rsquo;horizon. En plus, douze paysages, de '
      'l&rsquo;aube &agrave; l&rsquo;aurore bor&eacute;ale.',
   h2b='Ton Capyroo &agrave; toi',
   pb='Avec tes &eacute;tincelles, tu obtiens 15 skins, 15 lucioles, 20 tra&icirc;n&eacute;es et '
      'tes propres figures. En plus, quatre bonus sur cinq niveaux, 48 missions et chaque jour une '
      'course du jour, la m&ecirc;me pour tout le monde. Les &eacute;tincelles ne s&rsquo;ach&egrave;'
      'tent pas, tu les gagnes en jouant. Quelques skins, figures et une tra&icirc;n&eacute;e '
      's&rsquo;ach&egrave;tent &agrave; l&rsquo;unit&eacute;, et avec &laquo;&nbsp;Supprimer les '
      'pubs&nbsp;&raquo; (un seul achat, sans abonnement), la pub dispara&icirc;t.',
   letzter='Sans compte. La pub ne vient qu&rsquo;entre deux courses, jamais pendant que tu cours. '
           'Capyroo Run est disponible en fran&ccedil;ais, anglais, allemand et espagnol.',
   shots=['Capyroo Run&nbsp;: un salto sous la baleine',
          'Capyroo Run&nbsp;: des plan&egrave;tes se l&egrave;vent',
          'Capyroo Run&nbsp;: tout en haut de la for&ecirc;t de champignons']),
  'es': dict(
   titel='Capyroo Run | Un toque y Capyroo vuela',
   beschreibung='Capyroo corre alrededor de un planeta peque&ntilde;o y t&uacute; saltas con un '
                'dedo. Sin cuenta, para iPhone.',
   erster='Capyroo corre alrededor de un planeta peque&ntilde;o. Toca para saltar, mant&eacute;n '
          'pulsado para saltar m&aacute;s alto, y toca otra vez en el aire para el doble salto. En '
          'el camino hay troncos, huecos, rocas y plataformas en dos alturas, y cuanto m&aacute;s '
          'lejos llegas, m&aacute;s r&aacute;pido va.',
   h2a='Arriba siempre pasa algo',
   pa='Una ballena pasa flotando, un delf&iacute;n, un astronauta, un globo, y planetas enteros '
      'salen en el horizonte. Adem&aacute;s, doce paisajes, del amanecer a la aurora boreal.',
   h2b='Haz tuyo a Capyroo',
   pb='Con tus chispas consigues 15 aspectos, 15 luci&eacute;rnagas, 20 estelas y tus propios '
      'trucos. Adem&aacute;s, cuatro potenciadores en cinco niveles, 48 misiones y cada d&iacute;a '
      'una carrera diaria que es igual para todos. Las chispas no se compran, se ganan jugando. '
      'Algunos aspectos, trucos y una estela especiales se pueden comprar sueltos, y con '
      '&laquo;Quitar anuncios&raquo; (una sola compra, sin suscripci&oacute;n) se van los anuncios.',
   letzter='Sin cuenta. Los anuncios solo aparecen entre dos carreras, nunca mientras corres. '
           'Capyroo Run est&aacute; en espa&ntilde;ol, ingl&eacute;s, alem&aacute;n y franc&eacute;s.',
   shots=['Capyroo Run: un mortal bajo la ballena',
          'Capyroo Run: planetas salen ante ti',
          'Capyroo Run: arriba en el bosque de setas']),
}

# Der Stil der Capyroo-Seite gehoert nur zu dieser Seite: so aendert sich keine andere.
CAPY_STIL = """
  /* Capyroo Run: der Abendhimmel der App, hell auf dunklem Violett. */
  .band.capy { background: linear-gradient(180deg, #1B1646 0%, #3C2A74 55%, #6A3E8C 100%); color: #F6F1FF; }
"""


# ---------------------------------------------------------------------------
# Fumuon (20.10.2026). Dieselben Aussagen wie im Store (rhythm_game/tools/store/store.py), nur,
# was das Spiel wirklich kann: vier Bahnen, jede Note sitzt auf einem Ton, verpasst fehlt der Ton
# kurz (abschaltbar), 116 eigene Songs, 20 gratis, 96 in zehn Paketen (Einmalkauf, vorher
# anhoeren), drei Stufen, auf Schwer zwei Haende, Einzaehlen, Klopftest, kein Konto, keine
# Werbung, Spielstand bleibt auf dem Geraet. Die Bilder sind die Store-Bilder 1, 3 und 4.
# ---------------------------------------------------------------------------

for _s, (_og, _text) in {
    'de': ('Symbol der App Fumuon',
           'Bei Fumuon spielst du die Melodie. Triffst du die Note, h&ouml;rst du den Ton.'),
    'en': ('Fumuon app icon',
           'In Fumuon you play the melody. Hit the note and you hear it.'),
    'fr': ('Ic&ocirc;ne de l&rsquo;application Fumuon',
           'Dans Fumuon, tu joues la m&eacute;lodie. Tu touches la note, tu l&rsquo;entends.'),
    'es': ('Icono de la app Fumuon',
           'En Fumuon tocas la melod&iacute;a. Si aciertas la nota, la oyes.'),
}.items():
    T[_s]['og_alt']['fumuon'] = _og
    T[_s]['fu_text'] = _text

for _s, (_mehr, _start) in {
    'de': ('Mehr zu Fumuon', ''),
    'en': ('More about Fumuon', ' Fumuon, the rhythm game where you play the melody.'),
    'fr': ('En savoir plus sur Fumuon', ' Fumuon, le jeu de rythme o&ugrave; tu joues la m&eacute;lodie.'),
    'es': ('M&aacute;s sobre Fumuon', ' Fumuon, el juego de ritmo en el que t&uacute; tocas la melod&iacute;a.'),
}.items():
    T[_s]['mehr']['fumuon'] = _mehr
    if 'fumuon' not in AUS:
        T[_s]['beschreibung'] += _start

P['fumuon'] = {
  'de': dict(
   titel='Fumuon | Du spielst die Melodie',
   beschreibung='Ein Rhythmusspiel, bei dem du die Melodie selbst spielst: Triffst du die Note, '
                'h&ouml;rst du den Ton. 116 eigene Songs, ohne Konto, ohne Werbung.',
   erster='Die Noten fallen auf vier Bahnen herunter, und jede sitzt genau auf einem Ton des Songs. '
          'Triffst du, h&ouml;rst du ihn. Verpasst du eine, fehlt der Ton kurz (das kannst du auch '
          'abschalten). So h&ouml;rst du sofort, wie gut du gerade spielst.',
   h2a='116 Songs, alle von uns',
   pa='Alle Songs haben wir extra f&uuml;r Fumuon gemacht. 20 davon sind gratis dabei: Synthwave, '
      'Future Bass, Drum &amp; Bass, Trance und mehr. Die anderen 96 gibt es in zehn Songpaketen, von '
      'Pop &uuml;ber Jazz und Klassik bis Post-Hardcore und Hip-Hop. Jedes Paket kannst du vorher '
      'anh&ouml;ren und dann einmal kaufen, ohne Abo.',
   h2b='Drei Stufen, auf Schwer mit zwei H&auml;nden',
   pb='Tippen, halten, zwei Bahnen auf einmal, wischen. Jeder Song hat drei Stufen, und auf jeder '
      'spielst du die ganze Melodie. Auf Schwer kommen beide H&auml;nde dazu, rechts die Melodie, '
      'links das Schlagzeug. Vor jedem Song z&auml;hlt dir das Spiel vier Schl&auml;ge ein, und '
      'f&uuml;r Kopfh&ouml;rer mit Verz&ouml;gerung gibt es einen kurzen Klopftest.',
   letzter='Kein Konto, keine Werbung. Dein Spielstand bleibt auf deinem Handy. Fumuon gibt es auf '
           'Deutsch, Englisch, Franz&ouml;sisch und Spanisch, f&uuml;r iPhone und Android.',
   shots=['Fumuon: du spielst die Melodie',
          'Fumuon: auf Schwer mit zwei H&auml;nden',
          'Fumuon: die Songliste zum Anh&ouml;ren']),
  'en': dict(
   titel='Fumuon | You play the melody',
   beschreibung='A rhythm game where you play the melody yourself: hit the note and you hear it. '
                '116 original songs, no account, no ads.',
   erster='Notes fall down four lanes, and each one sits exactly on a note of the song. Hit it and '
          'you hear it. Miss one and that note drops out for a moment (you can turn that off too). '
          'So you always hear how well you&rsquo;re playing.',
   h2a='116 songs, all made by us',
   pa='We made every song just for Fumuon. 20 of them are free: synthwave, future bass, drum &amp; '
      'bass, trance and more. The other 96 come in ten song packs, from pop to jazz and classical to '
      'post-hardcore and hip-hop. You can listen to every pack first and then buy it once, no '
      'subscription.',
   h2b='Three levels, on Hard with both hands',
   pb='Tap, hold, two lanes at once, swipe. Every song has three levels, and on each one you play '
      'the whole melody. On Hard you use both hands, the melody on the right, the drums on the left. '
      'Before every song the game counts you in with four beats, and for headphones with a delay '
      'there&rsquo;s a quick tap test.',
   letzter='No account, no ads. Your progress stays on your phone. Fumuon is available in English, '
           'German, French and Spanish, for iPhone and Android.',
   shots=['Fumuon: you play the melody',
          'Fumuon: on Hard with both hands',
          'Fumuon: the song list, ready to listen']),
  'fr': dict(
   titel='Fumuon | Tu joues la m&eacute;lodie',
   beschreibung='Un jeu de rythme o&ugrave; tu joues toi-m&ecirc;me la m&eacute;lodie&nbsp;: tu '
                'touches la note, tu l&rsquo;entends. 116 morceaux maison, sans compte, sans pub.',
   erster='Les notes descendent sur quatre pistes, et chacune tombe pile sur un son du morceau. Tu '
          'la touches, tu l&rsquo;entends. Tu en rates une&nbsp;: ce son dispara&icirc;t un instant '
          '(tu peux aussi d&eacute;sactiver &ccedil;a). Comme &ccedil;a, tu entends tout de suite si '
          'tu joues bien.',
   h2a='116 morceaux, tous faits maison',
   pa='Tous les morceaux, on les a faits rien que pour Fumuon. 20 sont gratuits&nbsp;: synthwave, '
      'future bass, drum &amp; bass, trance et plus encore. Les 96 autres sont dans dix packs, de la '
      'pop au jazz et au classique jusqu&rsquo;au post-hardcore et au hip-hop. Tu peux &eacute;couter '
      'chaque pack avant, puis l&rsquo;acheter une fois, sans abonnement.',
   h2b='Trois niveaux, en Difficile &agrave; deux mains',
   pb='Taper, maintenir, deux pistes &agrave; la fois, glisser. Chaque morceau a trois niveaux, et '
      'sur chacun tu joues toute la m&eacute;lodie. En Difficile, tu joues &agrave; deux mains, la '
      'm&eacute;lodie &agrave; droite, la batterie &agrave; gauche. Avant chaque morceau, le jeu te '
      'compte quatre temps, et pour les &eacute;couteurs avec un d&eacute;calage, il y a un petit '
      'test de tapotement.',
   letzter='Pas de compte, pas de pub. Ta progression reste sur ton t&eacute;l&eacute;phone. Fumuon '
           'est disponible en fran&ccedil;ais, anglais, allemand et espagnol, pour iPhone et Android.',
   shots=['Fumuon&nbsp;: tu joues la m&eacute;lodie',
          'Fumuon&nbsp;: en Difficile &agrave; deux mains',
          'Fumuon&nbsp;: la liste des morceaux &agrave; &eacute;couter']),
  'es': dict(
   titel='Fumuon | T&uacute; tocas la melod&iacute;a',
   beschreibung='Un juego de ritmo en el que t&uacute; tocas la melod&iacute;a: si aciertas la nota, '
                'la oyes. 116 canciones originales, sin cuenta, sin anuncios.',
   erster='Las notas caen por cuatro carriles, y cada una cae justo en un tono de la canci&oacute;n. '
          'Si aciertas, lo oyes. Si fallas una, ese tono se calla un momento (tambi&eacute;n puedes '
          'desactivarlo). As&iacute; oyes al instante qu&eacute; tan bien est&aacute;s tocando.',
   h2a='116 canciones, todas hechas por nosotros',
   pa='Hicimos todas las canciones solo para Fumuon. 20 son gratis: synthwave, future bass, drum '
      '&amp; bass, trance y m&aacute;s. Las otras 96 vienen en diez packs, del pop al jazz y la '
      'cl&aacute;sica hasta el post-hardcore y el hip-hop. Puedes escuchar cada pack antes y comprarlo '
      'una sola vez, sin suscripci&oacute;n.',
   h2b='Tres niveles, en Dif&iacute;cil con las dos manos',
   pb='Tocar, mantener, dos carriles a la vez, deslizar. Cada canci&oacute;n tiene tres niveles, y en '
      'cada uno tocas la melod&iacute;a entera. En Dif&iacute;cil usas las dos manos, la melod&iacute;a '
      'a la derecha y la bater&iacute;a a la izquierda. Antes de cada canci&oacute;n el juego te '
      'cuenta cuatro tiempos, y para auriculares con retardo hay una prueba r&aacute;pida de toques.',
   letzter='Sin cuenta, sin anuncios. Tu progreso se queda en tu celular. Fumuon est&aacute; en '
           'espa&ntilde;ol, ingl&eacute;s, alem&aacute;n y franc&eacute;s, para iPhone y Android.',
   shots=['Fumuon: t&uacute; tocas la melod&iacute;a',
          'Fumuon: en Dif&iacute;cil con las dos manos',
          'Fumuon: la lista de canciones para escuchar']),
}

# Der Stil der Fumuon-Seite gehoert nur zu dieser Seite: so aendert sich keine andere.
FUMU_STIL = """
  /* Fumuon: der Nachthimmel hinter den Bahnen, hell auf tiefem Blau und Violett. */
  .band.fumu { background: linear-gradient(180deg, #060A1E 0%, #15184A 55%, #34195E 100%); color: #F3F1FF; }
"""


def _html(s):
    """Text mit Umlauten und Sonderzeichen als HTML-Zeichenreferenzen, wie im Rest der Datei."""
    return s.replace('&', '&amp;').encode('ascii', 'xmlcharrefreplace').decode('ascii')


def _seite(**felder):
    return {k: ([_html(x) for x in v] if isinstance(v, list) else _html(v)) for k, v in felder.items()}


# ---------------------------------------------------------------------------
# Wimmelino (20.10.2026). Dieselben Aussagen wie im Store (wimmelbild/store/texte.md): 14 Staedte,
# 15 Dinge je Stadt, Hinweise, jeder zwanzigste Fehltipp versteckt ein Ding wieder, lebendige
# Staedte, Musik je Stadt, Hamburg und Tokio gratis, drei Pakete, Werbung nach dem Level (mit Paket
# weg), kein Konto. Bilder: Google-Play-Fotos 1, 3 und 4 (Hamburg mit Liste, Tokio mit Liste, Tokio).
# ---------------------------------------------------------------------------

for _s, (_og, _mehr, _text, _start) in {
    'de': ('Symbol der App Wimmelino', 'Mehr zu Wimmelino',
           'Wimmelbilder kennst du noch von fr&uuml;her? Wimmelino ist das Ganze in gro&szlig;: 14 '
           'illustrierte St&auml;dte, und in jeder ist richtig viel versteckt.', ''),
    'en': ('Wimmelino app icon', 'More about Wimmelino',
           'Remember seek-and-find pictures from back then? Wimmelino is the big version: 14 '
           'illustrated cities, and every one of them is packed with hidden things.',
           ' Wimmelino, hidden objects in 14 illustrated cities, for iPhone.'),
    'fr': ('Ic&ocirc;ne de l&rsquo;application Wimmelino', 'En savoir plus sur Wimmelino',
           'Tu te souviens des cherche et trouve d&rsquo;avant&nbsp;? Wimmelino, c&rsquo;est la version '
           'en grand&nbsp;: 14 villes illustr&eacute;es, et chacune cache plein de choses.',
           ' Wimmelino, des objets cach&eacute;s dans 14 villes illustr&eacute;es, pour iPhone.'),
    'es': ('Icono de la app Wimmelino', 'M&aacute;s sobre Wimmelino',
           '&iquest;Te acuerdas de los dibujos de buscar y encontrar? Wimmelino es la versi&oacute;n en '
           'grande: 14 ciudades ilustradas, y cada una esconde un mont&oacute;n de cosas.',
           ' Wimmelino, objetos escondidos en 14 ciudades ilustradas, para iPhone.'),
}.items():
    T[_s]['og_alt']['wimmelino'] = _og
    T[_s]['mehr']['wimmelino'] = _mehr
    T[_s]['wi_text'] = _text
    if 'wimmelino' not in AUS:
        T[_s]['beschreibung'] += _start

P['wimmelino'] = {
  'de': _seite(
   titel='Wimmelino | Wimmelbilder aus 14 Städten',
   beschreibung='Wimmelbilder für alle: 14 riesige illustrierte Städte voller Verstecktem. Reinzoomen, '
                'suchen, finden. Hamburg und Tokio gratis, für iPhone.',
   erster='Hamburg, Tokio, Paris, London, Rom, Venedig, New York, Rio, Istanbul, Kairo, Bangkok, Seoul, '
          'Shanghai und Singapur. Unten steht, was du suchst (15 Dinge pro Stadt, manche gleich mehrmals). '
          'Reinzoomen, umschauen, antippen. Zoomen und Verschieben geht wie bei den Fotos auf deinem Handy.',
   h2a='Die Städte leben',
   pa='Boote fahren, Leute laufen rum und quatschen, Vögel fliegen auf, wenn du sie antippst. Überall '
      'gibt es kleine Szenen und Sehenswürdigkeiten zu entdecken, und jede Stadt hat ihre eigene Musik. '
      'Also genau das Richtige für abends auf dem Sofa oder für ein paar Minuten in der Bahn.',
   h2b='Hilfe, wenn du sie brauchst',
   pb='Tippst du auf ein Bild in der Liste, sagt dir das Spiel, wo du ungefähr schauen musst. Und wenn '
      'gar nichts mehr geht, hast du drei Hinweise pro Runde. Wild rumtippen bringt übrigens nichts: '
      'Jedes zwanzigste Mal daneben wird ein gefundenes Ding wieder versteckt.',
   letzter='Hamburg und Tokio sind gratis, die anderen zwölf Städte gibt es in drei Paketen (Europa, '
           'Weltreise, Asien), einmal kaufen, kein Abo. Nach einem geschafften Level kommt Werbung, mit '
           'einem Paket ist sie weg. Kein Konto, dein Spielstand bleibt auf deinem Gerät. Wimmelino gibt '
           'es auf Deutsch, Englisch, Französisch und Spanisch, für iPhone.',
   shots=['Wimmelino: Hamburg, unten die Suchliste',
          'Wimmelino: Tokio, unten die Suchliste',
          'Wimmelino: Tokio von oben']),
  'en': _seite(
   titel='Wimmelino | Hidden objects in 14 cities',
   beschreibung='Seek and find for everyone: 14 huge illustrated cities packed with hidden things. Zoom '
                'in, look, find. Hamburg and Tokyo free, for iPhone.',
   erster='Hamburg, Tokyo, Paris, London, Rome, Venice, New York, Rio, Istanbul, Cairo, Bangkok, Seoul, '
          'Shanghai and Singapore. The list at the bottom shows what you’re looking for (15 things per '
          'city, some of them more than once). Zoom in, look around, tap. Zooming and panning work just '
          'like the photos on your phone.',
   h2a='The cities are alive',
   pa='Boats move, people walk around and chat, birds fly off when you tap them. There are little '
      'scenes and sights to discover everywhere, and every city has its own music. Just right for the '
      'couch in the evening or a few minutes on the train.',
   h2b='Help when you need it',
   pb='Tap a picture in the list and the game tells you roughly where to look. And if you’re really '
      'stuck, you get three hints per round. Tapping around wildly won’t help, by the way: every 20 '
      'misses, one thing you found gets hidden again.',
   letzter='Hamburg and Tokyo are free, the other twelve cities come in three packs (Europe, World Tour, '
           'Asia), buy once, no subscription. After a finished level there’s an ad, and with any pack '
           'it’s gone. No account, your progress stays on your device. Wimmelino is available in '
           'English, German, French and Spanish, for iPhone.',
   shots=['Wimmelino: Hamburg, with the list at the bottom',
          'Wimmelino: Tokyo, with the list at the bottom',
          'Wimmelino: Tokyo from above']),
  'fr': _seite(
   titel='Wimmelino | Objets cachés dans 14 villes',
   beschreibung='Du cherche et trouve pour tout le monde : 14 immenses villes illustrées pleines '
                'd’objets cachés. Zoome, cherche, trouve. Hambourg et Tokyo gratuites, pour iPhone.',
   erster='Hambourg, Tokyo, Paris, Londres, Rome, Venise, New York, Rio, Istanbul, Le Caire, Bangkok, '
          'Séoul, Shanghai et Singapour. La liste en bas te montre ce que tu cherches (15 objets par '
          'ville, certains plusieurs fois). Tu zoomes, tu regardes, tu touches. Zoomer et se déplacer '
          'marche comme avec les photos de ton téléphone.',
   h2a='Les villes sont vivantes',
   pa='Les bateaux avancent, les gens se promènent et discutent, les oiseaux s’envolent quand tu les '
      'touches. Partout, il y a de petites scènes et des monuments à découvrir, et chaque ville a sa '
      'propre musique. Parfait pour le soir sur le canapé ou quelques minutes dans le train.',
   h2b='De l’aide quand il en faut',
   pb='Touche une image de la liste et le jeu te dit à peu près où regarder. Et si tu bloques vraiment, '
      'tu as trois indices par partie. Toucher partout au hasard ne sert à rien, d’ailleurs : tous '
      'les 20 ratés, un objet trouvé se cache à nouveau.',
   letzter='Hambourg et Tokyo sont gratuites, les douze autres villes sont réunies en trois packs '
           '(Europe, Tour du monde, Asie), un seul achat, sans abonnement. Après un niveau réussi, il y a '
           'une pub, et avec un pack, elle disparaît. Pas de compte, ta progression reste sur ton '
           'appareil. Wimmelino est disponible en français, anglais, allemand et espagnol, pour iPhone.',
   shots=['Wimmelino : Hambourg, la liste en bas',
          'Wimmelino : Tokyo, la liste en bas',
          'Wimmelino : Tokyo vu d’en haut']),
  'es': _seite(
   titel='Wimmelino | Objetos escondidos en 14 ciudades',
   beschreibung='Buscar y encontrar para todos: 14 ciudades enormes ilustradas llenas de cosas '
                'escondidas. Haz zoom, busca, encuentra. Hamburgo y Tokio gratis, para iPhone.',
   erster='Hamburgo, Tokio, París, Londres, Roma, Venecia, Nueva York, Río, Estambul, El Cairo, Bangkok, '
          'Seúl, Shanghái y Singapur. La lista de abajo te muestra lo que buscas (15 objetos por ciudad, '
          'algunos más de una vez). Haces zoom, miras, tocas. Hacer zoom y moverte funciona igual que con '
          'las fotos de tu celular.',
   h2a='Las ciudades están vivas',
   pa='Los barcos se mueven, la gente pasea y charla, los pájaros salen volando cuando los tocas. Por '
      'todas partes hay pequeñas escenas y monumentos por descubrir, y cada ciudad tiene su propia '
      'música. Justo lo que necesitas para la noche en el sofá o unos minutos en el tren.',
   h2b='Ayuda cuando la necesitas',
   pb='Toca una imagen de la lista y el juego te dice más o menos dónde mirar. Y si te atascas de verdad, '
      'tienes tres pistas por partida. Por cierto, tocar a lo loco no sirve de nada: cada 20 fallos, un '
      'objeto encontrado se vuelve a esconder.',
   letzter='Hamburgo y Tokio son gratis, las otras doce ciudades vienen en tres paquetes (Europa, Vuelta '
           'al mundo, Asia), una sola compra, sin suscripción. Después de superar un nivel hay un anuncio, '
           'y con cualquier paquete desaparece. Sin cuenta, tu progreso se queda en tu dispositivo. '
           'Wimmelino está en español, inglés, alemán y francés, para iPhone.',
   shots=['Wimmelino: Hamburgo, abajo la lista',
          'Wimmelino: Tokio, abajo la lista',
          'Wimmelino: Tokio desde arriba']),
}

WIMM_STIL = """
  /* Wimmelino: das Hafenwasser der Staedte, hell auf tiefem Blau. */
  .band.wimm { background: linear-gradient(180deg, #0C3F66 0%, #155A8C 55%, #1F72A8 100%); color: #F2F8FC; }
"""


# ---------------------------------------------------------------------------
# Capyroo World (20.10.2026). Dieselben Aussagen wie im Store (anime_ar_companion/store/texte.md):
# AR auf dem eigenen Boden, Tippen zum Hinlaufen und Aufs-Sofa-Huepfen, Baelle, High Five, Verstecken
# hinter Moebeln (LiDAR), Zimmer einrichten, Spaziergaenge, Studio ohne AR, Streicheln, Fuettern,
# Anziehen, Wunsch des Tages, Orakel, kleine Spiele, Level, kosmetische Einmalkaeufe, kein Konto,
# keine Werbung, kein Tracking, kein gespeichertes Kamerabild. Noch nicht im Store, also nur diese
# Seite. Bilder: Store-Bilder 1, 2 und 5.
# ---------------------------------------------------------------------------

for _s, (_og, _text) in {
    'de': ('Symbol der App Capyroo World',
           'Hol Capyroo in dein Zimmer. Mit AR steht er auf deinem Boden, so gro&szlig;, wie du ihn haben willst.'),
    'en': ('Capyroo World app icon',
           'Bring Capyroo into your room. In AR he stands on your floor, as big as you like.'),
    'fr': ('Ic&ocirc;ne de l&rsquo;application Capyroo World',
           'Fais venir Capyroo dans ta chambre. En RA, il se tient sur ton sol, de la taille que tu veux.'),
    'es': ('Icono de la app Capyroo World',
           'Trae a Capyroo a tu cuarto. Con la RA est&aacute; de pie en tu suelo, del tama&ntilde;o que quieras.'),
}.items():
    T[_s]['og_alt']['capyroo-world'] = _og
    T[_s]['cw_text'] = _text

P['capyroo-world'] = {
  'de': _seite(
   titel='Capyroo World | Dein Capybara zu Hause',
   beschreibung='Hol Capyroo in dein Zimmer: Mit AR läuft er über deinen Boden, hüpft aufs Sofa und '
                'versteckt sich hinter Möbeln. Ohne Konto, ohne Werbung.',
   erster='Du tippst auf den Boden, und er läuft hin. Du tippst aufs Sofa, und er hüpft rauf. Er holt '
          'Bälle, gibt dir High Five und versteckt sich hinter Möbeln (mit LiDAR). Dazu richtest du sein '
          'Zimmer ein: Deko hinstellen, drehen, verschieben. Ab und zu geht er von allein spazieren und '
          'bringt dir was mit.',
   h2a='Keine Lust auf AR?',
   pa='Kein Problem, Capyroo wohnt auch in einem gemütlichen Studio. Dort kannst du ihn streicheln, '
      'kitzeln, anziehen und mit ihm spielen, und füttern (es gibt jede Menge Leckereien, manche haben '
      'eine Wirkung). Jeden Tag hat er einen Wunsch, und das Capyroo-Orakel ist auch jeden Tag neu.',
   h2b='Kleine Spiele und neue Sachen',
   pb='Für zwischendurch gibt es ein paar kleine Spiele, zum Beispiel ein Retro-Abenteuer mit Oma '
      'Schildkröte. Capyroo steigt im Level auf und schaltet Neues frei, zum Beispiel Hüte und '
      'Hintergründe. Pakete mit Deko, Kostümen und Hintergründen gibt es einzeln (einmal kaufen, kein '
      'Abo), das ist nur Optik.',
   letzter='Kein Konto, keine Werbung, kein Tracking. Was du machst, bleibt auf deinem Handy, und die App '
           'speichert nie ein Kamerabild. Capyroo World gibt es auf Deutsch, Englisch, Spanisch und '
           'Französisch, für iPhone.',
   shots=['Capyroo World: Capyroo in deinem Wohnzimmer',
          'Capyroo World: sein Zimmer einrichten',
          'Capyroo World: ein Retro-Abenteuer mit Oma Schildkröte']),
  'en': _seite(
   titel='Capyroo World | Your capybara at home',
   beschreibung='Bring Capyroo into your room: in AR he walks across your floor, hops onto the sofa and '
                'hides behind furniture. No account, no ads.',
   erster='You tap the floor and he walks over. You tap the sofa and he hops up. He fetches balls, gives '
          'you a high five and hides behind furniture (with LiDAR). You also furnish his room: place '
          'decor, turn it, move it. Now and then he goes for a walk on his own and brings you something '
          'back.',
   h2a='Not into AR?',
   pa='No problem, Capyroo also lives in a cozy studio. There you can pet him, tickle him, dress him up, '
      'play with him and feed him (there are loads of treats, some with an effect). Every day he has a '
      'wish, and the Capyroo Oracle is new every day too.',
   h2b='Small games and new things',
   pb='For in between there are a few small games, like a retro adventure with Granny Turtle. Capyroo '
      'levels up and unlocks new things, like hats and backgrounds. Packs with decor, costumes and '
      'backgrounds are optional one-time purchases (no subscription), and they are only for looks.',
   letzter='No account, no ads, no tracking. What you do stays on your phone, and the app never saves a '
           'camera image. Capyroo World is available in English, German, Spanish and French, for iPhone.',
   shots=['Capyroo World: Capyroo in your living room',
          'Capyroo World: furnishing his room',
          'Capyroo World: a retro adventure with Granny Turtle']),
  'fr': _seite(
   titel='Capyroo World | Ton capybara à la maison',
   beschreibung='Fais venir Capyroo dans ta chambre : en RA, il marche sur ton sol, saute sur le '
                'canapé et se cache derrière les meubles. Sans compte, sans pub.',
   erster='Tu touches le sol et il y va. Tu touches le canapé et il saute dessus. Il rapporte des balles, '
          'te tape dans la main et se cache derrière les meubles (avec LiDAR). Tu aménages aussi sa '
          'chambre : poser la déco, la tourner, la déplacer. De temps en temps, il part se promener '
          'tout seul et te rapporte quelque chose.',
   h2a='La RA, ce n’est pas ton truc ?',
   pa='Pas de souci, Capyroo vit aussi dans un studio tout doux. Là, tu peux le caresser, le chatouiller, '
      'l’habiller, jouer avec lui et le nourrir (il y a plein de gourmandises, certaines ont un effet). '
      'Chaque jour, il a un vœu, et l’Oracle de Capyroo change aussi chaque jour.',
   h2b='Petits jeux et nouveautés',
   pb='Pour passer le temps, il y a quelques petits jeux, par exemple une aventure rétro avec Mamie '
      'Tortue. Capyroo monte de niveau et débloque des nouveautés, par exemple des chapeaux et des fonds. '
      'Les packs de déco, de costumes et de fonds sont des achats uniques facultatifs (sans abonnement), '
      'c’est seulement de l’apparence.',
   letzter='Sans compte, sans pub, sans suivi. Ce que tu fais reste sur ton téléphone, et l’app '
           'n’enregistre jamais d’image de la caméra. Capyroo World existe en français, anglais, allemand '
           'et espagnol, pour iPhone.',
   shots=['Capyroo World : Capyroo dans ton salon',
          'Capyroo World : aménager sa chambre',
          'Capyroo World : une aventure rétro avec Mamie Tortue']),
  'es': _seite(
   titel='Capyroo World | Tu carpincho en casa',
   beschreibung='Trae a Capyroo a tu cuarto: con la RA camina por tu suelo, salta al sofá y se esconde '
                'detrás de los muebles. Sin cuenta, sin anuncios.',
   erster='Tocas el suelo y él va hacia allí. Tocas el sofá y salta encima. Trae pelotas, te choca esos '
          'cinco y se esconde detrás de los muebles (con LiDAR). Además decoras su cuarto: colocar, girar '
          'y mover la decoración. De vez en cuando sale a pasear solo y te trae algo.',
   h2a='¿No te va la RA?',
   pa='No pasa nada, Capyroo también vive en un estudio acogedor. Allí puedes acariciarlo, hacerle '
      'cosquillas, vestirlo, jugar con él y darle de comer (hay un montón de chuches, algunas con '
      'efecto). Cada día tiene un deseo, y el Oráculo de Capyroo también es nuevo cada día.',
   h2b='Juegos pequeños y cosas nuevas',
   pb='Para ratos libres hay unos cuantos juegos pequeños, por ejemplo una aventura retro con la abuela '
      'tortuga. Capyroo sube de nivel y desbloquea cosas nuevas, por ejemplo sombreros y fondos. Los '
      'paquetes de decoración, disfraces y fondos son compras únicas opcionales (sin suscripción), y son '
      'solo aspecto.',
   letzter='Sin cuenta, sin anuncios, sin seguimiento. Lo que haces se queda en tu celular, y la app nunca '
           'guarda una imagen de la cámara. Capyroo World está en español, inglés, alemán y francés, para '
           'iPhone.',
   shots=['Capyroo World: Capyroo en tu sala',
          'Capyroo World: decorar su cuarto',
          'Capyroo World: una aventura retro con la abuela tortuga']),
}

CWLD_STIL = """
  /* Capyroo World: der Abendhimmel der Store-Bilder, hell auf warmem Violett. */
  .band.cwld { background: linear-gradient(180deg, #1E0F33 0%, #3B1C57 55%, #5E2A78 100%); color: #F7F1FF; }
"""


# ---------------------------------------------------------------------------
# Freelancerito (4.10.2026). Nur, was die App wirklich kann (lib/l10n/app_de.arb und README im
# App-Projekt): Stundenwert, Aufwand in fuenf Teilen, direkte Kosten, Puffer, daraus
# Mindestpreis, Zielpreis und Premium, alles aus den eigenen Werten und ausdruecklich keine
# Marktpreise. Simulator, Rabatt und Mehraufwand kostenlos und ohne Grenzen, Plus als
# Einmalkauf (kein Abo). Keine Steuern, kein Konto, keine Werbung, kein Tracking, keine KI.
# Kein Kaufpreis fuer Plus, wie bei den anderen Apps. Das Rechenbeispiel ist das aus der
# README der App, nachgerechnet. Die App spricht Englisch, Deutsch, Spanisch und
# Franzoesisch, mit denselben Begriffen wie hier (lib/l10n/app_es.arb, app_fr.arb).
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
   erster='Du tr&auml;gst ein, was dir eine Stunde deiner Zeit wert sein soll und wie viel Arbeit '
          'wirklich im Auftrag steckt, auch Kommunikation, Vorbereitung und Korrekturen. Dazu kommen '
          'die direkten Kosten, etwa Material oder Fahrten, und ein Sicherheitspuffer f&uuml;r das '
          'Unerwartete. Daraus ergeben sich drei Preise. Unter dem Mindestpreis liegst du unter deiner '
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
        'es noch 64,55&nbsp;&euro;. Ohne Rabatt, aber mit zwei Stunden mehr, sind es 62,31&nbsp;&euro;.',
   h2a='Freelancerito Plus',
   pa='Der ganze Rechner und alle Simulatoren sind kostenlos, ohne Grenzen. Plus kaufst du einmal, '
      'ein Abo gibt es nicht. Damit speicherst du Kalkulationen und findest sie im Verlauf wieder. '
      'Du legst eigene Standardwerte und Kostenarten an, h&auml;ltst Szenarien fest und teilst eine '
      'Kalkulation als PDF oder Text.',
   h2b='In deiner Sprache',
   pb='Freelancerito gibt es auf Deutsch, Englisch, Spanisch und Franz&ouml;sisch. Du rechnest in '
      'Euro, Schweizer Franken, Pfund oder Dollar.',
   letzter='Kein Konto, keine Werbung, kein Tracking, keine KI. Freelancerito funktioniert ohne '
           'Internet, und was du eintr&auml;gst, bleibt auf deinem Ger&auml;t.',
   shots=['Freelancerito: Mindestpreis, Zielpreis und Premium f&uuml;r einen Auftrag',
          'Freelancerito: der Simulator mit dem effektiven Wert deiner Zeit',
          'Freelancerito: der Aufwand eines Auftrags, Schritt f&uuml;r Schritt']),
  'en': dict(
   titel='Freelancerito | Price calculator for freelancers',
   beschreibung='Freelancerito works out what you should charge for a job: a minimum price, a target '
                'price and a premium, all from your own values. No account, no ads, for iPhone.',
   erster='You enter what one hour of your time should be worth to you and how much work the job '
          'really involves, including communication, preparation and corrections. Add the direct '
          'costs, such as materials or travel, and a safety buffer for the unexpected. That gives '
          'you three prices. Below the minimum price, you fall below your own calculation. The '
          'target price is a sensible price to start your offer with. The premium gives you more '
          'room when the job is especially valuable, urgent or demanding. Freelancerito deliberately '
          'leaves taxes out.',
   h2sim='Test your price',
   psim='In the simulator you move the price between minimum and premium and see the effective '
        'value of your time right away: what is left per hour of effort after direct costs. You can '
        'try out a discount before you offer it, and see what happens if the job takes longer. An '
        'example: &euro;60 an hour, 11 hours of effort, &euro;80 in costs and a 15% buffer give you '
        '&euro;850, &euro;890 and &euro;1,050. At &euro;890 your hour is worth &euro;73.64. With a '
        '&euro;100 discount it drops to &euro;64.55. Without the discount but with two extra hours, '
        'it is &euro;62.31.',
   h2a='Freelancerito Plus',
   pa='The whole calculator and all simulators are free, without limits. You buy Plus once, there '
      'is no subscription. With it you save your calculations and find them again in your history. '
      'You set your own defaults and cost types, keep scenarios and share a calculation as a PDF or '
      'as text.',
   h2b='In your language',
   pb='Freelancerito is available in English, German, Spanish and French. You can work in euros, '
      'Swiss francs, pounds or dollars.',
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
   erster='Tu indiques ce que doit valoir une heure de ton temps et le travail que la mission '
          'demande vraiment, communication, pr&eacute;paration et corrections comprises. '
          'S&rsquo;y ajoutent les co&ucirc;ts directs, comme le mat&eacute;riel ou les '
          'd&eacute;placements, et une marge de s&eacute;curit&eacute; pour l&rsquo;impr&eacute;vu. '
          'Tu obtiens trois prix. En dessous du prix minimum, tu passes sous ton propre calcul. Le '
          'prix cible est un prix raisonnable pour ton devis. Le premium te laisse plus de marge quand '
          'la mission est particuli&egrave;rement importante, urgente ou exigeante. Freelancerito ne '
          'calcule volontairement pas les imp&ocirc;ts.',
   h2sim='Tester ton prix',
   psim='Dans le simulateur, tu d&eacute;places le prix entre le minimum et le premium et tu vois '
        'tout de suite la valeur effective de ton temps&nbsp;: ce qui reste par heure de travail '
        'apr&egrave;s les co&ucirc;ts directs. Tu peux essayer une remise avant de l&rsquo;accorder '
        'et voir ce qui se passe si la mission prend plus de temps. Un exemple&nbsp;: 60&nbsp;&euro; '
        'de l&rsquo;heure, 11 heures de travail, 80&nbsp;&euro; de co&ucirc;ts et 15&nbsp;% de marge '
        'donnent 850, 890 et 1&nbsp;050&nbsp;&euro;. &Agrave; 890&nbsp;&euro;, ton heure vaut '
        '73,64&nbsp;&euro;. Avec 100&nbsp;&euro; de remise, elle tombe &agrave; 64,55&nbsp;&euro;. '
        'Sans remise, mais avec deux heures de plus, elle vaut 62,31&nbsp;&euro;.',
   h2a='Freelancerito Plus',
   pa='Le calculateur et tous les simulateurs sont gratuits, sans limite. Plus, tu l&rsquo;ach&egrave;tes '
      'une fois, il n&rsquo;y a pas d&rsquo;abonnement. Avec lui, tu enregistres tes calculs et tu les '
      'retrouves dans l&rsquo;historique. Tu d&eacute;finis tes propres valeurs par d&eacute;faut et '
      'types de co&ucirc;ts, tu gardes des sc&eacute;narios et tu partages un calcul en PDF ou en '
      'texte.',
   h2b='Dans ta langue',
   pb='Freelancerito existe en fran&ccedil;ais, anglais, allemand et espagnol. Tu peux calculer en '
      'euros, en francs suisses, en livres ou en dollars.',
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
   erster='Anotas cu&aacute;nto quieres que valga una hora de tu tiempo y cu&aacute;nto trabajo lleva '
          'de verdad el encargo, incluidas la comunicaci&oacute;n, la preparaci&oacute;n y las '
          'correcciones. A eso se suman los costes directos, como material o traslados, y un margen de '
          'seguridad para lo inesperado. Con eso obtienes tres precios. Por debajo del precio '
          'm&iacute;nimo, quedas por debajo de tu propio c&aacute;lculo. El precio objetivo es un '
          'precio razonable para tu oferta. El premium te deja m&aacute;s margen cuando el trabajo es '
          'especialmente valioso, urgente o exigente. Freelancerito deja fuera los impuestos a '
          'prop&oacute;sito.',
   h2sim='Prueba tu precio',
   psim='En el simulador mueves el precio entre el m&iacute;nimo y el premium y ves al momento el '
        'valor efectivo de tu tiempo: lo que queda por hora de trabajo despu&eacute;s de los costes '
        'directos. Puedes probar un descuento antes de ofrecerlo y ver qu&eacute; pasa si el trabajo '
        'lleva m&aacute;s tiempo. Un ejemplo: 60&nbsp;&euro; la hora, 11 horas de trabajo, '
        '80&nbsp;&euro; de costes y un margen del 15&nbsp;% dan 850, 890 y 1050&nbsp;&euro;. A '
        '890&nbsp;&euro;, tu hora vale 73,64&nbsp;&euro;. Con 100&nbsp;&euro; de descuento baja a '
        '64,55&nbsp;&euro;. Sin descuento, pero con dos horas m&aacute;s, se queda en 62,31&nbsp;&euro;.',
   h2a='Freelancerito Plus',
   pa='La calculadora y todos los simuladores son gratis, sin l&iacute;mites. Plus lo pagas una vez, '
      'no hay suscripci&oacute;n. Con &eacute;l guardas tus c&aacute;lculos y vuelves a abrirlos desde '
      'el historial. Defines tus propios valores predeterminados y tipos de coste, guardas escenarios '
      'y compartes un c&aacute;lculo como PDF o como texto.',
   h2b='En tu idioma',
   pb='Freelancerito est&aacute; en espa&ntilde;ol, ingl&eacute;s, alem&aacute;n y franc&eacute;s. '
      'Puedes calcular en euros, francos suizos, libras o d&oacute;lares.',
   letzter='Sin cuenta, sin anuncios, sin rastreo, sin IA. Freelancerito funciona sin conexi&oacute;n, '
           'y lo que anotas se queda en tu dispositivo.',
   shots=['Freelancerito: precio m&iacute;nimo, precio objetivo y premium para un trabajo',
          'Freelancerito: el simulador con el valor efectivo de tu tiempo',
          'Freelancerito: el trabajo de un encargo, paso a paso']),
}


def bild(sprache, nr, alt, app='shlayolotl', faul=True, breite=212):
    """Ein Bildschirmfoto in drei Fassungen: AVIF, WebP, und das WebP als
    Rueckfall. Der Browser nimmt das erste Format, das er kann, und von den
    zwei Breiten die, die zu seinem Bildschirm passt."""
    b = '%s-%d' % (app + '-' + sprache, nr)
    return (
        '        <picture>\n'
        '          <source type="image/avif" srcset="/assets/shots/%s-420.avif 420w, /assets/shots/%s-840.avif 840w" sizes="%dpx">\n'
        '          <source type="image/webp" srcset="/assets/shots/%s-420.webp 420w, /assets/shots/%s-840.webp 840w" sizes="%dpx">\n'
        '          <img src="/assets/shots/%s-420.webp" width="420" height="910" alt="%s"%s decoding="async">\n'
        '        </picture>' % (b, b, breite, b, b, breite, b, alt, ' loading="lazy"' if faul else '')
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


# Startseite deutsch: eigene kurze Beschreibung (max. ca. 155 Zeichen), ohne die je App
# angehaengten Saetze oben. Die Namen der Apps stehen drin, damit man sie findet.
T['de']['beschreibung'] = ('Kleine Apps mit Charakter: Wimmelino, Fumuon, Karma Farmer, Mitrechner und '
                           'Shlayolotl. St&auml;dte durchsuchen, Melodie spielen, Pflanze wachsen lassen.')


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


# Reihenfolge der Apps auf der Startseite und im Menue "Apps". Capyroo Run fehlt mit
# Absicht: die Seite steht nur unter /capyroo-run/product/ (siehe CR_APPSTORE).
# Seit 20.10.2026 steht die neueste App immer zuerst (User: "und die neuste app immer zu erst"),
# auf der Startseite und im Menue. Wer neu online geht, kommt also nach vorn; Freelancerito und
# Wheresome stehen deshalb schon vorn, solange sie offline (und damit ausgeblendet) sind.
START_APPS = [a for a in ('wheresome', 'freelancerito', 'wimmelino', 'fumuon', 'karma-farmer', 'mitrechner',
                           'shlayolotl')
              if a not in AUS]

MENUE_SKRIPT = '''<script>
  document.addEventListener('click', function (e) {
    document.querySelectorAll('details.menue[open]').forEach(function (m) {
      if (!m.contains(e.target) || e.target.closest('.liste a')) m.removeAttribute('open');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') document.querySelectorAll('details.menue[open]').forEach(function (m) { m.removeAttribute('open'); });
  });
</script>'''


for _s, (_z, _w) in {'de': ('Vorige App', 'N&auml;chste App'), 'en': ('Previous app', 'Next app'),
                     'fr': ('Application pr&eacute;c&eacute;dente', 'Application suivante'),
                     'es': ('App anterior', 'App siguiente')}.items():
    T[_s]['app_zurueck'] = _z
    T[_s]['app_weiter'] = _w


def apps_menue(sprache):
    """Das Menue "Apps": jede App der Startseite mit Symbol, der Link fuehrt dort zu ihr.
    Seit 14.10.2026 steht oben nur noch dieses Menue. "Support" ist aus der Leiste raus
    (User: "die seite weiter bestehen lassen aber oben aus der leiste entfernen"); die
    Seite selbst bleibt, falls sie irgendwo als Adresse eingetragen ist."""
    eintraege = ''.join(
        '<a href="%s#%s"><img src="/assets/img/%s-256.webp" alt="" width="28" height="28">%s</a>'
        % (PFAD[sprache], app, app, NAME.get(app, app.capitalize())) for app in START_APPS)
    return ('<details class="menue"><summary>%s</summary><div class="liste">%s</div></details>%s'
            % (T[sprache]['nav_apps'], eintraege, MENUE_SKRIPT))


def seite(sprache):
    t = T[sprache]

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
    <div class="rechts">%(menue)s</div>
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

<div class="apps" id="apps">
<div class="apps-reihe" id="apps-reihe">
%(abschnitte)s</div>
<button class="apps-pfeil zurueck" type="button" aria-label="%(app_zurueck)s"></button>
<button class="apps-pfeil weiter" type="button" aria-label="%(app_weiter)s"></button>
</div>
<div class="punkte apps-punkte" data-fuer="apps-reihe"></div>
%(capyroo_abschnitt)s</main>

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
      k.setAttribute('aria-label', bild.dataset.name || String(i + 1));
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
<script>
  // Pfeile blaettern zur naechsten App (nach der letzten wieder zur ersten), und ein
  // Sprungziel wie /#mitrechner aus dem Menue zeigt gleich die richtige App.
  (function () {
    var reihe = document.getElementById('apps-reihe');
    if (!reihe) return;
    var apps = Array.prototype.slice.call(reihe.children);
    var pfeile = document.querySelectorAll('.apps-pfeil');
    if (apps.length < 2) { pfeile.forEach(function (p) { p.hidden = true; }); return; }
    function jetzt() { return Math.round(reihe.scrollLeft / reihe.clientWidth); }
    function zeige(i, sanft) {
      i = (i + apps.length) %% apps.length;
      reihe.scrollTo({ left: apps[i].offsetLeft - reihe.offsetLeft, behavior: sanft ? 'smooth' : 'auto' });
    }
    pfeile[0].addEventListener('click', function () { zeige(jetzt() - 1, true); });
    pfeile[1].addEventListener('click', function () { zeige(jetzt() + 1, true); });
    function ausSprungziel() {
      var i = apps.indexOf(document.getElementById(decodeURIComponent(location.hash.slice(1))));
      if (i >= 0) zeige(i, false);
    }
    window.addEventListener('hashchange', ausSprungziel);
    ausSprungziel();
  })();
</script>
</body>
</html>
''' % dict(t, sprache=sprache, pfad=PFAD[sprache],
           kopf=kopf(sprache, PFAD, t['titel'], t['beschreibung']),
           organisation=ORGANISATION,
           sprachen=sprachleiste(sprache, PFAD), stil=STIL + FUMU_STIL + WIMM_STIL + CAPYHAUS_STIL,
           capyroo_abschnitt=capyroo_abschnitt(sprache),
           abschnitte=''.join(start_abschnitte(sprache)[app] for app in START_APPS),
           ds_pfad=DS_PFAD[sprache], menue=apps_menue(sprache))


# Capyroo bekommt unter der App-Reihe einen eigenen Abschnitt (User 20.10.2026: "capyroo bitte als
# eigene Section, etwas darunter ... wir werden naemlich irgendwann mehrere capy games haben"). Alle
# Capyroo-Spiele stehen hier und nicht in der App-Reihe, auch wenn sie spaeter im Store sind; die
# Knoepfe zeigen dann von selbst App Store und Google Play statt "Bald im App Store.". Ein neues
# Capyroo-Spiel kommt vorn in diese Liste (neueste zuerst, wie in START_APPS), die Karten brechen
# von selbst in mehrere Reihen um.
CAPYROO_SPIELE = ('capyroo-world', 'capyroo-run')

for _s, (_titel, _zeile, _mehr_cw, _mehr_cr) in {
    'de': ('Capyroo', 'Unser Capybara bekommt eigene Spiele. Hier siehst du sie zuerst.',
           'Mehr zu Capyroo World', 'Mehr zu Capyroo Run'),
    'en': ('Capyroo', 'Our capybara is getting games of his own. You see them here first.',
           'More about Capyroo World', 'More about Capyroo Run'),
    'fr': ('Capyroo', 'Notre capybara a bient&ocirc;t ses propres jeux. Tu les vois ici en premier.',
           'En savoir plus sur Capyroo World', 'En savoir plus sur Capyroo Run'),
    'es': ('Capyroo', 'Nuestro carpincho tendr&aacute; sus propios juegos. Aqu&iacute; los ves primero.',
           'M&aacute;s sobre Capyroo World', 'M&aacute;s sobre Capyroo Run'),
}.items():
    T[_s]['capy_titel'] = _titel
    T[_s]['capy_zeile'] = _zeile
    T[_s]['mehr']['capyroo-world'] = _mehr_cw
    T[_s]['mehr']['capyroo-run'] = _mehr_cr


def capyroo_abschnitt(sprache):
    t = T[sprache]
    text = {'capyroo-world': t['cw_text'], 'capyroo-run': t['cr_text']}
    karten = ''.join(
        '      <article class="karte">\n'
        '        <a class="karte-kopf" href="%(pfad)s%(app)s/product/">\n'
        '          <img src="/assets/img/%(app)s-256.webp" alt="" width="84" height="84">\n'
        '          <h3>%(name)s</h3>\n'
        '        </a>\n'
        '        <p>%(text)s</p>\n'
        '        <p class="mehr"><a href="%(pfad)s%(app)s/product/">%(mehr)s</a></p>\n'
        '        <div class="knoepfe">\n%(knoepfe)s\n        </div>\n'
        '      </article>\n'
        % dict(pfad=PFAD[sprache], app=app, name=NAME[app], text=text[app], mehr=t['mehr'][app],
               knoepfe=knoepfe(app, sprache))
        for app in CAPYROO_SPIELE if app in APPS)
    if not karten:
        return ''
    return ('<section class="band capyhaus" id="capyroo">\n'
            '  <div class="wrap">\n'
            '    <h2>%s</h2>\n'
            '    <p class="zeile">%s</p>\n'
            '    <div class="karten">\n%s    </div>\n'
            '  </div>\n'
            '</section>\n' % (t['capy_titel'], t['capy_zeile'], karten))


CAPYHAUS_STIL = """
  /* Der Capyroo-Abschnitt unter der App-Reihe: Abendhimmel wie in den Spielen, zwei Karten. */
  .band.capyhaus { background: linear-gradient(180deg, #1B1646 0%, #3C2A74 60%, #5E2A78 100%); color: #F6F1FF;
                   margin-top: 56px; }
  .capyhaus .zeile { font-size: 19px; margin: 0 0 34px; opacity: .9; }
  .capyhaus .karten { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; }
  .capyhaus .karte { background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.14);
                     border-radius: 26px; padding: 28px; }
  .capyhaus .karte-kopf { display: flex; align-items: center; gap: 18px; color: inherit; text-decoration: none;
                          margin-bottom: 16px; }
  .capyhaus .karte-kopf img { width: 84px; height: 84px; border-radius: 19px; }
  .capyhaus .karte-kopf h3 { font-size: 28px; letter-spacing: -.02em; margin: 0; }
  .capyhaus .karte p { margin-bottom: 16px; }
  .capyhaus .karte .soon { margin: 6px 0 0; }
  .capyhaus .karte .badge { margin-top: 4px; }
  @media (max-width: 720px) {
    .capyhaus .karten { grid-template-columns: 1fr; }
    .capyhaus .karte { padding: 22px; }
  }
"""


def start_abschnitte(sprache):
    """Die Karte jeder App auf der Startseite, als Woerterbuch; die Reihenfolge bestimmt START_APPS."""
    t = T[sprache]
    shots = '\n'.join(bild(sprache, n, t['shots'][n - 1], faul=False, breite=170)
                      for n in START_BILDER['shlayolotl'])
    return dict(
           shlayolotl=SHLAY_ABSCHNITT % dict(
               t, sprache=sprache, pfad=PFAD[sprache], symbol_shlay=symbol('shlayolotl'),
               mehr_shlay=t['mehr']['shlayolotl'], shots=shots, shlay_url=SHLAY_URL[sprache]),
           wimmelino='' if 'wimmelino' in AUS else WI_ABSCHNITT % dict(
               t, pfad=PFAD[sprache], symbol_wi=symbol('wimmelino'),
               mehr_wi=t['mehr']['wimmelino'], shots_wi=galerie_html('wimmelino', sprache, 'shots-wi', start=True),
               knoepfe_wi=knoepfe('wimmelino', sprache)),
           fumuon='' if 'fumuon' in AUS else FU_ABSCHNITT % dict(
               t, pfad=PFAD[sprache], symbol_fu=symbol('fumuon'),
               mehr_fu=t['mehr']['fumuon'], shots_fu=galerie_html('fumuon', sprache, 'shots-fu', start=True),
               knoepfe_fu=knoepfe('fumuon', sprache)),
           mitrechner='' if 'mitrechner' in AUS else MITR_ABSCHNITT % dict(
               t, pfad=PFAD[sprache], symbol_mitr=symbol('mitrechner'),
               mehr_mitr=t['mehr']['mitrechner'], shots_mitr=galerie_html('mitrechner', sprache, 'shots-mitr', start=True),
               knoepfe_mitr=knoepfe('mitrechner', sprache)),
           **{'karma-farmer': '' if 'karma-farmer' in AUS else KF_ABSCHNITT % dict(
               t, pfad=PFAD[sprache], symbol_kf=symbol('karma-farmer'),
               mehr_kf=t['mehr']['karma-farmer'], shots_kf=galerie_html('karma-farmer', sprache, 'shots-kf', start=True),
               knoepfe_kf=knoepfe('karma-farmer', sprache))},
           freelancerito='' if 'freelancerito' in AUS else FL_ABSCHNITT % dict(
               t, pfad=PFAD[sprache], symbol_fl=symbol('freelancerito'),
               mehr_fl=t['mehr']['freelancerito'], shots_fl=galerie_html('freelancerito', sprache, 'shots-fl', start=True),
               knoepfe_fl=knoepfe('freelancerito', sprache)),
           wheresome='' if 'wheresome' in AUS else WHERE_ABSCHNITT % dict(
               t, pfad=PFAD[sprache], symbol_where=symbol('wheresome'),
               mehr_where=t['mehr']['wheresome']))


SHLAY_ABSCHNITT = '''<section class="band shlay" id="shlayolotl" data-name="Shlayolotl">
  <div class="wrap">
    <div class="info">
    <div class="kopf">
%(symbol_shlay)s
      <div>
        <h2><a href="%(pfad)sshlayolotl/product/">Shlayolotl</a></h2>
      </div>
    </div>
    <p>%(shlay_text)s</p>
    <p class="mehr"><a href="%(pfad)sshlayolotl/product/">%(mehr_shlay)s</a></p>
    </div>
    <div class="carousel" id="shots">
%(shots)s
    </div>
    <div class="punkte" data-fuer="shots"></div>
    <div class="kaufen">
    <a class="badge" href="%(shlay_url)s">
      <img src="/assets/img/appstore-%(sprache)s.svg" alt="%(badge_alt)s" width="120" height="40">
    </a>
    </div>
  </div>
</section>

'''

WI_ABSCHNITT = '''<section class="band wimm" id="wimmelino" data-name="Wimmelino">
  <div class="wrap">
    <div class="info">
    <div class="kopf">
%(symbol_wi)s
      <div>
        <h2><a href="%(pfad)swimmelino/product/">Wimmelino</a></h2>
      </div>
    </div>
    <p>%(wi_text)s</p>
    <p class="mehr"><a href="%(pfad)swimmelino/product/">%(mehr_wi)s</a></p>
    </div>
%(shots_wi)s
    <div class="kaufen">
%(knoepfe_wi)s
    </div>
  </div>
</section>
'''

FU_ABSCHNITT = '''<section class="band fumu" id="fumuon" data-name="Fumuon">
  <div class="wrap">
    <div class="info">
    <div class="kopf">
%(symbol_fu)s
      <div>
        <h2><a href="%(pfad)sfumuon/product/">Fumuon</a></h2>
      </div>
    </div>
    <p>%(fu_text)s</p>
    <p class="mehr"><a href="%(pfad)sfumuon/product/">%(mehr_fu)s</a></p>
    </div>
%(shots_fu)s
    <div class="kaufen">
%(knoepfe_fu)s
    </div>
  </div>
</section>
'''


# Die Wheresome-Karte der Startseite, solange die App noch nicht im Store ist
# ausgeblendet (siehe OFFLINE).
MITR_ABSCHNITT = '''<section class="band mitr" id="mitrechner" data-name="Mitrechner">
  <div class="wrap">
    <div class="info">
    <div class="kopf">
%(symbol_mitr)s
      <div>
        <h2><a href="%(pfad)smitrechner/product/">Mitrechner</a></h2>
      </div>
    </div>
    <p>%(mitr_text)s</p>
    <p class="mehr"><a href="%(pfad)smitrechner/product/">%(mehr_mitr)s</a></p>
    </div>
%(shots_mitr)s
    <div class="kaufen">
%(knoepfe_mitr)s
    </div>
  </div>
</section>
'''


KF_ABSCHNITT = '''<section class="band karma" id="karma-farmer" data-name="Karma Farmer">
  <div class="wrap">
    <div class="info">
    <div class="kopf">
%(symbol_kf)s
      <div>
        <h2><a href="%(pfad)skarma-farmer/product/">Karma Farmer</a></h2>
      </div>
    </div>
    <p>%(kf_text)s</p>
    <p class="mehr"><a href="%(pfad)skarma-farmer/product/">%(mehr_kf)s</a></p>
    </div>
%(shots_kf)s
    <div class="kaufen">
%(knoepfe_kf)s
    </div>
  </div>
</section>
'''


# Freelancerito, solange die App in keinem Store ist, nur in der Vorschau (siehe OFFLINE).
FL_ABSCHNITT = '''<section class="band freel" id="freelancerito" data-name="Freelancerito">
  <div class="wrap">
    <div class="info">
    <div class="kopf">
%(symbol_fl)s
      <div>
        <h2><a href="%(pfad)sfreelancerito/product/">Freelancerito</a></h2>
      </div>
    </div>
    <p>%(fl_text)s</p>
    <p class="mehr"><a href="%(pfad)sfreelancerito/product/">%(mehr_fl)s</a></p>
    </div>
%(shots_fl)s
    <div class="kaufen">
%(knoepfe_fl)s
    </div>
  </div>
</section>
'''


WHERE_ABSCHNITT = '''<section class="band where" id="wheresome" data-name="Wheresome">
  <div class="wrap">
    <div class="info">
    <div class="kopf">
%(symbol_where)s
      <div>
        <p class="tag">%(where_tag)s</p>
        <h2><a href="%(pfad)swheresome/product/">Wheresome</a></h2>
      </div>
    </div>
    <p>%(where_text)s</p>
    <p class="mehr"><a href="%(pfad)swheresome/product/">%(mehr_where)s</a></p>
    </div>
    <div class="kaufen">
    <p class="soon">%(where_bald)s</p>
    </div>
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


def app_sprache(app, sprache):
    """Die Sprache, in der die App (und ihre Rechtsseite) einem Besucher dieser Seite begegnet."""
    return sprache if sprache in APP_SPRACHEN.get(app, SPRACHEN) else 'en'


def recht_link(app, sprache):
    """Adresse und Text des Links auf die Rechtsseite einer App, in der Sprache der Seite,
    soweit die Rechtsseite sie hat."""
    s = app_sprache(app, sprache)
    text = T[sprache]['support_recht'] + (AUF_ENGLISCH[sprache] if s != sprache else '')
    return '%s#%s' % (RECHT[app], s), text


# Welche zwei Bilder auf der Startseite stehen (Nummern 1 bis 3). Bei Shlayolotl das
# Spielfeld und der Sieg statt zweimal Spielfeld.
START_BILDER = {'shlayolotl': (1, 3)}


def galerie_html(app, sprache, kennung, start=False):
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
            % (kennung, '\n'.join(bild(foto, i + 1, alts[i], app) for i in range(3)) if not start else
               # Auf der Startseite sofort laden: faul geladen blieb die Karte nach dem
               # Weiterblaettern kurz leer.
               '\n'.join(bild(foto, n, alts[n - 1], app, faul=False, breite=170)
                         for n in START_BILDER.get(app, (1, 2))), kennung))


def unten_html(app, sprache, kennung):
    """Bilderreihe und Knopf (oder „Bald im App Store."), ohne Leerzeile, wenn die Bilder fehlen.
    Die Knoepfe stehen in einem eigenen Kasten: im Raster am Rechner waere sonst jeder Knopf eine
    eigene Zeile, und App Store und Google Play stuenden untereinander statt nebeneinander."""
    return '\n'.join(x for x in (galerie_html(app, sprache, kennung),
                                  '    <div class="knoepfe">\n%s\n    </div>' % knoepfe(app, sprache)) if x)


# Googles Markenhinweis, nur auf Seiten, die das Abzeichen zeigen.
PLAY_MARKEN = {
    'de': 'Google Play und das Google-Play-Logo sind Marken von Google LLC.',
    'en': 'Google Play and the Google Play logo are trademarks of Google LLC.',
    'fr': 'Google Play et le logo Google Play sont des marques de Google LLC.',
    'es': 'Google Play y el logotipo de Google Play son marcas de Google LLC.',
}


PLAY_URL = {'mitrechner': MITR_PLAY, 'karma-farmer': KF_PLAY, 'freelancerito': FL_PLAY, 'fumuon': FU_PLAY}
# Solange das offizielle Abzeichen fehlt, ein schlichter Textlink (den Namen im Text zu
# nennen erlaubt Google ohne Abzeichen-Bedingungen).
PLAY_TEXT = {'de': 'Auch bei Google Play', 'en': 'Also on Google Play',
             'fr': 'Aussi sur Google Play', 'es': 'Tambi&eacute;n en Google Play'}


def im_play(app):
    return bool(PLAY_URL.get(app))


def play_abzeichen(app, sprache):
    return im_play(app) and os.path.exists(
        os.path.join(ROOT, 'assets', 'img', 'googleplay-%s.png' % sprache))


def knoepfe(app, sprache):
    """App Store, und fuer Mitrechner auch Google Play, sobald das offizielle
    Abzeichen unter assets/img/googleplay-<sprache>.png liegt. Seit 20.10.2026 liegt es da: der
    Inhaber hat es im Partner Marketing Hub geladen (GetItOnGooglePlay_Badge_Web_color_<Sprache>,
    478 x 142, ohne durchsichtigen Rand, Spanisch in der Fassung fuer Lateinamerika), die Dateien
    sind unveraendert kopiert. Gezeigt mit 44 px Hoehe wie Apples Knopf, also nicht kleiner; der
    Freiraum ist das Polster von .badge (12 px, mehr als ein Viertel der Hoehe).

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
            or (app == 'freelancerito' and not FL_IM_STORE)
            or (app == 'capyroo-run' and not CR_IM_STORE) or (app == 'fumuon' and not FU_IM_STORE)
            or (app == 'capyroo-world' and not CW_IM_STORE)):
        html = '    <p class="soon">%s</p>' % MITR_BALD[sprache]
        # Schon bei Google Play, aber noch nicht bei Apple (Fumuon): Google Play steht trotzdem da,
        # als Abzeichen, sobald es vorliegt, sonst als Textlink.
        if play_abzeichen(app, sprache):
            html += ('\n    <a class="badge" href="%s">\n'
                     '      <img src="/assets/img/googleplay-%s.png" alt="%s" width="135" height="40">\n'
                     '    </a>' % (PLAY_URL[app], sprache, t['badge_play_alt']))
        elif im_play(app):
            html += '\n    <p class="play"><a href="%s">%s</a></p>' % (PLAY_URL[app], PLAY_TEXT[sprache])
        return html
    ziel = {'shlayolotl': SHLAY_URL[sprache], 'mitrechner': MITR_APPSTORE[sprache],
            'karma-farmer': KF_APPSTORE, 'freelancerito': FL_APPSTORE,
            'capyroo-run': CR_APPSTORE, 'fumuon': FU_APPSTORE, 'wimmelino': WI_APPSTORE,
            'capyroo-world': CW_APPSTORE}.get(app) or '#'
    html = ('    <a class="badge" href="%s">\n'
            '      <img src="/assets/img/appstore-%s.svg" alt="%s" width="120" height="40">\n'
            '    </a>' % (ziel, sprache, t['badge_alt']))
    if play_abzeichen(app, sprache):
        html += ('\n    <a class="badge" href="%s">\n'
                 '      <img src="/assets/img/googleplay-%s.png" alt="%s" width="135" height="40">\n'
                 '    </a>' % (PLAY_URL[app], sprache, t['badge_play_alt']))
    elif im_play(app):
        html += '\n    <p class="play"><a href="%s">%s</a></p>' % (PLAY_URL[app], PLAY_TEXT[sprache])
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

    if app in ('shlayolotl', 'mitrechner', 'karma-farmer', 'freelancerito', 'capyroo-run', 'fumuon',
               'wimmelino', 'capyroo-world'):
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
                'freelancerito': t['fl_text'], 'capyroo-run': t['cr_text'], 'fumuon': t['fu_text'],
                'wimmelino': t['wi_text'], 'capyroo-world': t['cw_text']}[app]
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
    <div class="rechts">%(menue)s</div>
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
           stil=STIL + {'capyroo-run': CAPY_STIL, 'fumuon': FUMU_STIL, 'wimmelino': WIMM_STIL,
                         'capyroo-world': CWLD_STIL}.get(app, ''),
           klasse={'shlayolotl': 'shlay', 'mitrechner': 'mitr', 'karma-farmer': 'karma',
                   'freelancerito': 'freel', 'capyroo-run': 'capy', 'fumuon': 'fumu',
                   'wimmelino': 'wimm', 'capyroo-world': 'cwld'}.get(app, 'where'),
           symbol=symbol(app), oben=oben, name=NAME.get(app, app.capitalize()), lead=lead,
           text=text, unten=unten, recht_href=recht_link(app, sprache)[0], recht_text=recht_link(app, sprache)[1],
           sprachen=sprachleiste(sprache, pfade), ds_pfad=DS_PFAD[sprache],
           skript=skript, menue=apps_menue(sprache),
           marken=t['marken'] + (' ' + PLAY_MARKEN[sprache] if im_play(app) else ''))



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

SUPPORT_STIL += MENUE_STIL


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
        ds_pfad=DS_PFAD[sprache], menue=apps_menue(sprache),
        support_wheresome='' if 'wheresome' in AUS else
        '  <h2>Wheresome</h2>\n  <p><a href="/wheresome#%s">%s</a></p>\n' % (sprache, t['support_recht']),
        support_freelancerito=
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
    <div class="rechts">%(menue)s</div>
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
        sprachen=sprachleiste(sprache, DS_PFAD), stil=SUPPORT_STIL, menue=apps_menue(sprache), ds_pfad=DS_PFAD[sprache],
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
    <div class="rechts">%(menue)s</div>
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
    <a href="%(ds_pfad)s">%(datenschutz)s</a>
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
        for teil in ('assets', 'mitrechner.html', 'karma-farmer.html', 'freelancerito.html', 'capyroo-run.html', 'fumuon.html', 'wimmelino.html', 'capyroo-world.html', 'shlayolotl.html',
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
