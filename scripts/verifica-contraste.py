#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica el contraste AA de la demo Maderas Lopez (bosque + madera).

Que hace:
  1. Comprueba los pares planos de la paleta (texto sobre su fondo).
  2. Recompone en Python el HERO tal y como lo pinta el CSS (foto con
     object-fit:cover + velo bosque) sobre las fotos reales del repo, y se
     queda con el PEOR PIXEL bajo el texto: el mas CLARO, porque el texto
     del hero es claro.
  3. Repite los velos contra una foto blanca pura (peor caso absoluto), para
     que cambiar la foto no pueda romper el contraste.

Los valores de abajo son espejo de assets/css/style.css: si se toca la
paleta o el velo del hero alli, hay que tocarlos aqui.

Uso:  python scripts/verifica-contraste.py
Sale con codigo 1 si algo baja de su minimo.
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'img')

AA = 4.5       # texto
AA_UI = 3.0    # foco visible y componentes graficos

P = dict(
    white='#ffffff', bg2='#f0f4ef',
    text='#14201a', ink2='#35443a', muted='#55645a',
    forest='#10301f', forest2='#184229',
    ondark='#f1f5ee', ondarkmuted='#afc2b3',
    g='#3f9a5f', gdark='#1f6a3d', gdeep='#175230', gleaf='#93d3a4', gchip='#e3efe5',
    w='#e3a557', whover='#d69441', wdeep='#7d4a10', wchip='#f8ecd9',
    wa='#25d366', waink='#0b2415',
)

fallos = []


# ----------------------------------------------------------------- WCAG ----
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lum(rgb):
    return 0.2126 * _lin(rgb[0]) + 0.7152 * _lin(rgb[1]) + 0.0722 * _lin(rgb[2])


def hex_rgb(hx):
    hx = hx.lstrip('#')
    return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))


def ratio(a, b):
    la, lb = lum(a), lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


def comprueba(etiqueta, r, minimo=AA):
    ok = r >= minimo
    if not ok:
        fallos.append(f'{etiqueta}: {r:.2f} (min {minimo})')
    print(f"    {etiqueta:<58} {r:6.2f}:1  {'OK' if ok else 'FALLA'}")


# ---- 1. PARES PLANOS -------------------------------------------------------
print("\n=== 1 - Paleta plana ===")
PARES = [  # (texto, fondo, minimo, uso)
    ('text', 'white', AA, 'titulares'),
    ('text', 'bg2', AA, 'titulares, seccion alterna'),
    ('ink2', 'white', AA, 'parrafos'),
    ('ink2', 'bg2', AA, 'parrafos, seccion alterna'),
    ('muted', 'white', AA, 'secundario'),
    ('muted', 'bg2', AA, 'secundario, seccion alterna'),
    ('muted', 'gchip', AA, 'secundario sobre chip verde'),
    ('gdark', 'white', AA, 'texto verde'),
    ('gdark', 'bg2', AA, 'texto verde, seccion alterna'),
    ('gdeep', 'white', AA, 'verde en hover'),
    ('gdeep', 'gchip', AA, 'texto sobre chip verde'),
    ('wdeep', 'white', AA, 'texto madera'),
    ('wdeep', 'bg2', AA, 'texto madera, seccion alterna'),
    ('wdeep', 'wchip', AA, 'texto sobre chip madera'),
    ('text', 'w', AA, 'boton madera y etiqueta DEMO'),
    ('text', 'whover', AA, 'boton madera en hover'),
    ('ondark', 'forest', AA, 'texto sobre bosque'),
    ('ondark', 'forest2', AA, 'texto sobre superficie bosque'),
    ('ondarkmuted', 'forest', AA, 'secundario sobre bosque'),
    ('ondarkmuted', 'forest2', AA, 'secundario sobre superficie bosque'),
    ('w', 'forest', AA, 'madera como texto sobre bosque'),
    ('w', 'forest2', AA, 'madera sobre superficie bosque'),
    ('gleaf', 'forest', AA, 'verde claro sobre bosque'),
    ('gleaf', 'forest2', AA, 'verde claro sobre superficie bosque'),
    ('white', 'gdark', AA, 'blanco sobre verde (seleccion)'),
    ('white', 'gdeep', AA, 'blanco sobre verde en hover'),
    ('gdark', 'white', AA_UI, 'foco visible sobre claro'),
    ('gdark', 'bg2', AA_UI, 'foco visible, seccion alterna'),
    ('w', 'forest', AA_UI, 'foco visible sobre bosque'),
    ('w', 'forest2', AA_UI, 'borde del aviso de propuesta'),
    ('g', 'white', AA_UI, 'borde y detalle verde (no texto)'),
]
for t, f, m, uso in PARES:
    comprueba(f'--{t} sobre --{f} - {uso}', ratio(hex_rgb(P[t]), hex_rgb(P[f])), m)


# ---- 2. HERO: peor pixel real ----------------------------------------------
FOREST = hex_rgb(P['forest'])


def _stop(stops, t):
    """Interpola [(pos, alfa), ...] en t (0..1)."""
    if t <= stops[0][0]:
        return stops[0][1]
    for i in range(1, len(stops)):
        p0, a0 = stops[i - 1]
        p1, a1 = stops[i]
        if t <= p1:
            return a0 if p1 == p0 else a0 + (a1 - a0) * (t - p0) / (p1 - p0)
    return stops[-1][1]


def sobre(alfa, base):
    """Bosque con alfa (0..1) sobre un color opaco."""
    return tuple(FOREST[j] * alfa + base[j] * (1 - alfa) for j in range(3))


def cover(im, bw, bh):
    """object-fit:cover con object-position 50% 50% en una caja bw x bh."""
    W, H = im.size
    sc = max(bw / W, bh / H)
    sw, sh = max(bw, round(W * sc)), max(bh, round(H * sc))
    im = im.resize((sw, sh), Image.BILINEAR)
    x, y = (sw - bw) // 2, (sh - bh) // 2
    return im.crop((x, y, x + bw, y + bh))


def peor(im, capas, box, step=3):
    """Pixel mas CLARO de la banda tras componer las capas (la primera, arriba)."""
    W, H = im.size
    px = im.load()
    x0, y0, x1, y1 = box
    wl, worst = -1.0, None
    for y in range(int(y0 * H), max(int(y0 * H) + 1, int(y1 * H)), step):
        for x in range(int(x0 * W), int(x1 * W), step):
            base = px[x, y]
            for capa in reversed(capas):
                base = sobre(capa(x / W, y / H), base)
            l = lum(base)
            if l > wl:
                wl, worst = l, base
    return worst


def informe(nombre, rgb, textos):
    print(f"  {nombre} -> peor pixel rgb({rgb[0]:.0f},{rgb[1]:.0f},{rgb[2]:.0f})")
    for t in textos:
        comprueba(f'{nombre} - --{t}', ratio(hex_rgb(P[t]), rgb))


# Espejo de .hero-bg .scrim (solo la capa horizontal: la vertical unicamente
# oscurece, asi que ignorarla es el caso conservador) y de .nav.
SCRIM_DESKTOP = lambda fx, fy: _stop([(0.0, .97), (0.58, .96), (0.78, .6), (1.0, .24)], fx)
SCRIM_MOVIL = lambda fx, fy: _stop([(0.0, .93), (0.55, .9), (1.0, .96)], fy)
NAV = lambda fx, fy: .88
TEXTO_HASTA = 0.58      # la columna de texto nunca pasa del 58% del ancho
COPY_VW, COPY_MAX = 0.54, 620   # .hero-copy{max-width:min(620px,54vw)}
MAXW = 1240

HERO_TXT = ['ondark', 'ondarkmuted', 'w', 'gleaf']
NAV_TXT = ['ondark', 'ondarkmuted']

print("\n=== 2 - HERO - peor pixel real bajo el texto ===")
im = Image.open(os.path.join(IMG, 'hero-pilas.jpg')).convert('RGB')
for vw, vh in ((901, 700), (1024, 768), (1280, 800), (1440, 900), (1920, 1080)):
    pad = 32 if vw > 900 else 22
    izq = max(0, (vw - MAXW) / 2) + pad
    fin = (izq + min(COPY_MAX, COPY_VW * vw)) / vw
    print(f"\n[{vw}x{vh} - escritorio] el texto llega al {fin:.1%} del ancho (limite {TEXTO_HASTA:.0%})")
    if fin > TEXTO_HASTA:
        fallos.append(f'hero {vw}: el texto se sale de la zona opaca del velo')
        print("    EL TEXTO SE SALE DE LA ZONA OPACA DEL VELO")
    caja = cover(im, vw, vh)
    informe(f'hero {vw}', peor(caja, [SCRIM_DESKTOP], (0.0, 0.0, TEXTO_HASTA, 1.0)), HERO_TXT)
    # En escritorio la nav lleva su texto a la derecha, sobre la parte clara
    # del velo: se mide a todo el ancho.
    informe(f'nav {vw}', peor(caja, [NAV, SCRIM_DESKTOP], (0.0, 0.0, 1.0, 84 / vh)), NAV_TXT)

im = Image.open(os.path.join(IMG, 'hero-pilas-900.jpg')).convert('RGB')
for vw, vh in ((360, 740), (390, 844), (600, 900), (768, 1024), (900, 700)):
    print(f"\n[{vw}x{vh} - movil] texto a todo el ancho, velo casi plano")
    caja = cover(im, vw, vh)
    informe(f'hero {vw}', peor(caja, [SCRIM_MOVIL], (0.0, 0.0, 1.0, 1.0)), HERO_TXT)
    informe(f'nav {vw}', peor(caja, [NAV, SCRIM_MOVIL], (0.0, 0.0, 1.0, 84 / vh)), NAV_TXT)

print("\n=== 3 - Peor caso absoluto - una foto blanca pura debajo ===")
blanca = Image.new('RGB', (200, 200), (255, 255, 255))
informe('hero escritorio sobre blanco', peor(blanca, [SCRIM_DESKTOP], (0.0, 0.0, TEXTO_HASTA, 1.0)), HERO_TXT)
informe('hero movil sobre blanco', peor(blanca, [SCRIM_MOVIL], (0, 0, 1, 1)), HERO_TXT)
informe('nav sobre blanco', peor(blanca, [NAV], (0, 0, 1, 1)), NAV_TXT)

# ---- 4. BURBUJA DE WHATSAPP ------------------------------------------------
# (Ninguna foto lleva texto encima: no hay pastillas que medir.)
# La burbuja es fija: pasa por encima de todas las secciones, claras y
# oscuras. El icono y la etiqueta van sobre fondos OPACOS (--wa y blanco),
# asi que su contraste no depende de lo que quede debajo. Lo que si depende
# es el contorno (WCAG 1.4.11, 3:1): por eso lleva dos anillos, bosque por
# dentro y blanco por fuera, y se mide cada uno contra su peor vecino.
print("\n=== 4 - BURBUJA DE WHATSAPP ===")
CLAROS = ['white', 'bg2', 'gchip', 'wchip']     # fondos de pagina claros
OSCUROS = ['forest', 'forest2']                 # hero, banda y pie
print("  icono y etiqueta (fondos opacos)")
comprueba('icono --waink sobre --wa', ratio(hex_rgb(P['waink']), hex_rgb(P['wa'])))
comprueba('etiqueta: --text sobre blanco', ratio(hex_rgb(P['text']), hex_rgb(P['white'])))
print("  contorno del boton")
comprueba('anillo --forest contra el relleno --wa', ratio(hex_rgb(P['forest']), hex_rgb(P['wa'])), AA_UI)
comprueba('anillo --forest contra el anillo blanco', ratio(hex_rgb(P['forest']), hex_rgb(P['white'])), AA_UI)
for f in OSCUROS:
    comprueba(f'anillo blanco sobre pagina --{f}', ratio(hex_rgb(P['white']), hex_rgb(P[f])), AA_UI)
print("  contorno de la etiqueta")
comprueba('borde --forest contra el relleno blanco', ratio(hex_rgb(P['forest']), hex_rgb(P['white'])), AA_UI)
for f in OSCUROS:
    comprueba(f'anillo blanco sobre pagina --{f}', ratio(hex_rgb(P['white']), hex_rgb(P[f])), AA_UI)
print("  sobre claro el anillo blanco se funde con la pagina: manda el bosque")
for f in CLAROS:
    comprueba(f'anillo --forest visto contra pagina --{f}', ratio(hex_rgb(P['forest']), hex_rgb(P[f])), AA_UI)
print("  foco visible (anillo bosque entre dos blancos)")
for f in CLAROS:
    comprueba(f'foco --forest sobre pagina --{f}', ratio(hex_rgb(P['forest']), hex_rgb(P[f])), AA_UI)
for f in OSCUROS:
    comprueba(f'foco: halo blanco sobre pagina --{f}', ratio(hex_rgb(P['white']), hex_rgb(P[f])), AA_UI)
print("  enlaces del pie y de «Como consultar»")
comprueba('--gleaf sobre --forest - enlace del aviso legal', ratio(hex_rgb(P['gleaf']), hex_rgb(P['forest'])))
comprueba('--gdark sobre --bg2 - telefono y correo del paso 2', ratio(hex_rgb(P['gdark']), hex_rgb(P['bg2'])))

# ---- 5. LOGO DE LA NAV -----------------------------------------------------
# El logo es oscuro y va sobre una pastilla blanca opaca. Se mide la tinta
# real del rotulo (media de sus pixeles oscuros en el original), la pastilla
# contra la nav y el anillo de foco, que va por fuera de la pastilla, sobre
# la nav. "Peor caso" es la nav al .88 con una foto blanca pura debajo.
print("\n=== 5 - LOGO DE LA NAV ===")
logo = Image.open(os.path.join(ROOT, 'assets', 'logo-maderas-lopez.jpeg')).convert('RGB')
rotulo = [p for p in logo.crop((550, 150, 1545, 350)).get_flattened_data() if sum(p) < 200]
tinta = tuple(sum(p[i] for p in rotulo) / len(rotulo) for i in range(3))
BLANCO = hex_rgb(P['white'])
NAV_PEOR = sobre(.88, (255, 255, 255))
print(f"  tinta del rotulo -> rgb({tinta[0]:.0f},{tinta[1]:.0f},{tinta[2]:.0f}) - nav en su peor caso -> rgb({NAV_PEOR[0]:.0f},{NAV_PEOR[1]:.0f},{NAV_PEOR[2]:.0f})")
comprueba('rotulo del logo sobre la pastilla blanca', ratio(tinta, BLANCO))
comprueba('pastilla blanca contra --forest', ratio(BLANCO, FOREST), AA_UI)
comprueba('pastilla blanca contra la nav en su peor caso', ratio(BLANCO, NAV_PEOR), AA_UI)
comprueba('etiqueta DEMO: --text sobre --w', ratio(hex_rgb(P['text']), hex_rgb(P['w'])))
comprueba('foco --w contra --forest', ratio(hex_rgb(P['w']), FOREST), AA_UI)
comprueba('foco --w contra la nav en su peor caso', ratio(hex_rgb(P['w']), NAV_PEOR), AA_UI)

# ---------------------------------------------------------------------------
print()
if fallos:
    print(f"RESULTADO: {len(fallos)} comprobacion(es) por debajo de su minimo")
    for f in fallos:
        print("  - " + f)
    sys.exit(1)
print("RESULTADO: 0 fallos - todo el texto por encima de 4.5:1 (AA)")
