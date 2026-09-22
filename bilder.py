#!/usr/bin/env python3
"""Erzeugt die abgeleiteten Bilder aus dem, was in assets/img schon liegt.

    python3 bilder.py

Zwei Sorten. Erstens die Vorschaukarten fuer geteilte Links (og:image,
1200 x 630): der Schriftzug auf Weiss fuer die Startseite, das App-Symbol
auf der Bandfarbe der jeweiligen App. Nichts Neues, nur neu angeordnet.
Zweitens kleine WebP-Fassungen der App-Symbole: das Shlayolotl-PNG hat
172 KB und wird auf der Seite 112 px breit gezeigt.
"""

import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, 'assets', 'img')


def rund(bild, radius):
    """Das Symbol mit abgerundeten Ecken, wie es der App Store zeigt."""
    maske = Image.new('L', bild.size, 0)
    ImageDraw.Draw(maske).rounded_rectangle((0, 0) + bild.size, radius, fill=255)
    aus = bild.convert('RGBA')
    aus.putalpha(maske)
    return aus


def karte(name, farbe, motiv, breite):
    karte = Image.new('RGB', (1200, 630), farbe)
    motiv = motiv.resize((breite, int(motiv.height * breite / motiv.width)), Image.LANCZOS)
    x = (1200 - motiv.width) // 2
    y = (630 - motiv.height) // 2
    karte.paste(motiv, (x, y), motiv if motiv.mode == 'RGBA' else None)
    ziel = os.path.join(IMG, 'og-%s.png' % name)
    karte.save(ziel, optimize=True)
    print('%-32s %6.1f KB' % (os.path.relpath(ziel, ROOT), os.path.getsize(ziel) / 1024))


def klein(name, breiten):
    quelle = Image.open(os.path.join(IMG, name + '.png')).convert('RGB')
    for b in breiten:
        ziel = os.path.join(IMG, '%s-%d.webp' % (name, b))
        quelle.resize((b, b), Image.LANCZOS).save(ziel, quality=82, method=6)
        print('%-32s %6.1f KB' % (os.path.relpath(ziel, ROOT), os.path.getsize(ziel) / 1024))


wortmarke = Image.open(os.path.join(IMG, 'wortmarke-schwarz.png')).convert('RGBA')
shlay = Image.open(os.path.join(IMG, 'shlayolotl.png')).convert('RGB')
where = Image.open(os.path.join(IMG, 'wheresome.png')).convert('RGB')

karte('hollow-spoon', '#FFFFFF', wortmarke, 720)
karte('shlayolotl', '#0A0E24', rund(shlay, 112), 380)
karte('wheresome', '#176F7A', rund(where, 112), 380)
klein('shlayolotl', (256, 512))
klein('wheresome', (256, 512))
