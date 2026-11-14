"""Tema: ¿Qué son las estrellas fugaces? (espacio; Leónidas, pico la noche del 17 al 18-nov-2026)

Datos verificados (14-nov-2026; ESA «About the Leonids», NASA, Wikipedia «Leonids», Asociación
Astronómica de España, Starwalk, IGN):
- Una estrella fugaz no es una estrella: es una mota de polvo (la mayoría más pequeña que un
  guisante; las más grandes de las Leónidas, ~1 cm y 0,5 g) que entra en la atmósfera y se pone
  incandescente al chocar con el aire. Se encienden a más de 100 km de altura (las Leónidas, ~155 km).
- Las Leónidas vienen del polvo que deja el cometa 55P/Tempel-Tuttle, que pasa cerca del Sol cada
  ~33 años. Cada noviembre la Tierra cruza ese rastro.
- Entran a ~71 km/s (unos 255.000 km/h): son de las más rápidas.
- Parecen salir de la constelación de Leo (el radiante): de ahí el nombre.
- 1966: tormenta de Leónidas de más de 40 meteoros por segundo.
- 2026: máximo la noche del 17 al 18 de noviembre, ~15 por hora en un año normal; mejor después de
  medianoche y lejos de las luces.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT

TITLE = "¿Qué son las estrellas fugaces?"
MUSIC_SEED = 20261114
MUSIC_KEY = 55
BOARD_SEED = 141


def stars(c, b, n=22):
    for k in range(n):
        x = (k * 53) % 176 + 2
        y = (k * 97) % 200 + 34
        tw = 0.5 + 0.5 * math.sin(b * 2 + k)
        c.rect(x, y, 1, 1, DIM if tw < 0.6 else AMBER)


def meteor(c, x, y, ang, length, t=1.0, col=AMBER):
    """Estela que se va apagando hacia atrás desde la cabeza (x, y)."""
    dx, dy = math.cos(ang), math.sin(ang)
    n = int(length)
    for i in range(n):
        f = i / max(1, n)
        c.rect(x - dx * i, y - dy * i, 1 if f > 0.3 else 2, 1 if f > 0.3 else 2, gfx.mix(HOT, col, f), a=t * (1 - f))
    c.disc(x, y, 2, HOT, a=t)


def comet(c, x, y, b, tail=40):
    for k in range(tail):
        f = k / tail
        c.disc(x + k * 1.2, y - k * 0.5 + math.sin(b * 3 + k * 0.3) * f * 2, 4 * (1 - f) + 1, gfx.mix(AMBER, DIM, f), a=0.8 * (1 - f))
    c.disc(x, y, 4, HOT)


def dust(c, cx, cy, s, col=ORANGE):
    pts = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
    for i, (px, py) in enumerate(pts):
        c.rect(cx + px * s * (0.8 + 0.2 * ((i * 7) % 3)), cy + py * s, s, s, col)
    c.rect(cx - s, cy - s, 2 * s, 2 * s, col)


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    stars(c, b)
    if l < 4:
        c.text("NO SON", 90, 34, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("ESTRELLAS", 90, 66, gfx.mix(RED, HOT, pulse * 0.3), 3, "center")
        c.ox = 0
        c.text("SON MOTAS", 90, 104, AMBER, 3, "center")
        c.text("DE POLVO", 90, 136, AMBER, 3, "center")
        meteor(c, 130, 200, math.radians(150) + math.pi, 60, 1.0)
        dust(c, 60, 206, 3)
        return
    c.text("¿QUÉ SON", 90, 40, AMBER, 3, "center")
    c.text("LAS", 90, 72, ORANGE, 3, "center")
    c.text("ESTRELLAS", 90, 104, ORANGE, 3, "center")
    c.text("FUGACES?", 90, 136, ORANGE, 3, "center")
    f = ((l - 4) / 3) % 1
    meteor(c, 40 + f * 110, 180 + f * 40, math.radians(20), 40, 1 - f * 0.5)


def s_cometa(c, l, d, b, h):
    stars(c, b, 12)
    c.disc(90, 130, 10, AMBER)
    c.ring(90, 130, 70, 1, DIM, a0=-180, a1=180)
    a = math.pi * 0.9 - l * 0.25
    x, y = 90 + math.cos(a) * 70, 130 + math.sin(a) * 40
    comet(c, x, y, b, 24)
    for k in range(30):
        aa = a + 0.05 * (k + 2)
        c.rect(90 + math.cos(aa) * 70, 130 + math.sin(aa) * 40, 1, 1, ORANGE, a=0.8)
    if l >= 1:
        c.text("COMETA", 90, 196, AMBER, 2, "center")
        c.text("TEMPEL-TUTTLE", 90, 214, ORANGE, 1, "center")
    if l >= 8:
        c.text("DEJA UN RASTRO DE POLVO", 90, 46, AMBER, 1, "center")


def s_cruce(c, l, d, b, h):
    stars(c, b, 12)
    c.disc(30, 130, 10, AMBER)
    c.ring(30, 130, 110, 1, DIM, a0=-60, a1=60)
    for k in range(70):
        y = 50 + k * 2.4
        c.rect(118 + math.sin(k) * 3, y, 1, 1, ORANGE)
    ang = math.radians(-50 + gfx.clamp01(l / 10) * 75)
    ex, ey = 30 + math.cos(ang) * 110, 130 + math.sin(ang) * 110
    c.disc(ex, ey, 6, ORANGE)
    c.disc(ex - 2, ey - 1, 2, DIM)
    c.text("TIERRA", ex - 10, ey - 3, AMBER, 1, "right")
    if l >= 0.5:
        c.text("CADA NOVIEMBRE", 90, 196, AMBER, 1, "center")
    if l >= 4.5:
        c.text("LO CRUZAMOS", 90, 210, ORANGE, 2, "center")


def s_velocidad(c, l, d, b, h):
    q = gfx.clamp01(l / 2)
    dust(c, 90 + math.sin(b * 30) * 1, 90, 4)
    for k in range(8):
        f = ((l * 2) + k / 8) % 1
        c.rect(20 + f * 140, 70 + k * 6, 14, 1, DIM)
    n = int(71 * q)
    c.text(f"{n} KM/S", 90, 130, RED, 4, "center")
    if l >= 4:
        c.text("= 255.000 KM/H", 90, 170, AMBER, 2, "center")


T_FIRE = 8.0


def s_fuego(c, l, d, b, h):
    c.rect(0, 112, 180, 1, DIM)
    c.text("ATMÓSFERA", 150, 116, DIM, 1, "center")
    if l < T_FIRE:
        t = gfx.clamp01(l / T_FIRE)
        x, y = 140 - t * 40, 50 + t * 58
        if l >= 3:
            heat = gfx.clamp01((l - 3) / 4)
            c.disc(x - 3, y + 4, 4 + heat * 4, gfx.mix(ORANGE, HOT, heat), a=0.5 * heat)
        dust(c, x, y, 3)
        if l >= 3:
            c.text("EL AIRE SE APLASTA", 60, 70, AMBER, 1, "center")
    else:
        q = gfx.clamp01((l - T_FIRE) / 3)
        x, y = 100 - q * 50, 108 + q * 90
        c.disc(x, y, 5, HOT, a=0.5 * (1 - q * 0.5))
        meteor(c, x, y, math.radians(119), 70, 1 - q * 0.6)
        c.text("¡SE ENCIENDE!", 90, 40, RED, 2, "center")
    if l >= 10.5:
        c.text("A MÁS DE 100 KM", 90, 60, AMBER, 1, "center")


LEO = [(40, 80), (62, 70), (80, 82), (96, 110), (130, 104), (148, 124), (124, 132), (80, 128)]


def s_leo(c, l, d, b, h):
    stars(c, b, 10)
    for k in range(len(LEO) - 1):
        c.line(*LEO[k], *LEO[k + 1], DIM)
    for (x, y) in LEO:
        c.disc(x, y, 2, AMBER)
    if l >= 2:
        for k in range(5):
            f = ((l * 0.5) + k / 5) % 1
            ang = k * 1.3
            meteor(c, 70 + math.cos(ang) * (20 + f * 80), 90 + math.sin(ang) * (20 + f * 80), ang, 14 + f * 20, 1 - f)
    c.text("LEO", 90, 46, ORANGE, 2, "center")
    if l >= 4:
        c.text("LEÓNIDAS", 90, 176, RED, 3, "center")


def s_1966(c, l, d, b, h):
    stars(c, b, 10)
    c.text("1966", 90, 42, AMBER, 3, "center")
    rate = 3 + int(gfx.clamp01((l - 2) / 4) * 40)
    for k in range(rate):
        f = ((l * 1.3) + k * 0.618) % 1
        sx = (k * 37) % 170 + 5
        meteor(c, sx + f * 30, 80 + f * 100 + (k % 5) * 6, math.radians(60), 12, 1 - f)
    if l >= 6:
        c.box(20, 180, 140, 36, PANEL, RED)
        c.text("MÁS DE 40", 90, 184, RED, 2, "center")
        c.text("POR SEGUNDO", 90, 204, AMBER, 1, "center")


def s_verlas(c, l, d, b, h):
    stars(c, b)
    c.rect(0, 200, 180, 20, DARK)
    for k in range(6):
        c.rect(10 + k * 30, 196 - (k % 3) * 4, 16, 8, DARK)
    c.text("17-18 NOV", 90, 42, RED, 3, "center")
    if l >= 2:
        c.text("UNAS 15 POR HORA", 90, 76, AMBER, 1, "center")
    if l >= 5:
        c.text("DESPUÉS DE MEDIANOCHE", 90, 92, ORANGE, 1, "center")
    if l >= 8:
        c.text("LEJOS DE LAS LUCES", 90, 108, ORANGE, 1, "center")
    f = (l / 2.5) % 1
    meteor(c, 40 + f * 100, 130 + f * 40, math.radians(25), 40, 1 - f)


COVER_LINES = ["ESTRELLAS", "FUGACES:", "¿QUÉ SON?"]


def cover_art(c, y):
    for k in range(6):
        c.rect((k * 61) % 170 + 5, y + (k * 23) % 60, 1, 1, AMBER)
    c.text("LEÓNIDAS 17-18 NOV", 90, y + 4, RED, 1, "center")
    meteor(c, 140, y + 62, math.radians(25), 100, 1.0)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 EL COMETA", s_cometa, False),
    (24, 38, "2 EL CRUCE", s_cruce, False),
    (38, 52, "3 A 71 KM/S", s_velocidad, True),
    (52, 66, "4 ¡FUEGO!", s_fuego, True),
    (66, 80, "5 LEÓNIDAS", s_leo, False),
    (80, 100, "6 EN 1966", s_1966, False),
    (100, 116, "7 MÍRALAS", s_verlas, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = [
    (0, "NO SON ESTRELLAS:", 0.6), (2, "SON MOTAS DE POLVO", 0.5), (4, "¿QUÉ SON LAS", 0.6), (5.8, "ESTRELLAS FUGACES?", 0.6),
    (9, "UN COMETA", 1), (11, "PASA CERCA DEL SOL", 0.8), (14, "Y VA SOLTANDO", 1), (16.5, "POLVO", 1),
    (18, "DEJA UN RASTRO", 1), (21, "EN SU ÓRBITA", 1),
    (24, "CADA NOVIEMBRE", 1), (26.5, "LA TIERRA", 1), (28.5, "CRUZA ESE RASTRO", 1), (32, "Y SE LLEVA", 1), (34.5, "EL POLVO", 1),
    (38, "ENTRA A 71", 1), (40.5, "KILÓMETROS", 1), (42, "POR SEGUNDO", 1), (44.5, "UNOS 255.000", 1), (47, "KM POR HORA", 1),
    (52, "EL AIRE DE DELANTE", 0.8), (55, "SE APLASTA", 1), (57, "Y SE CALIENTA", 1), (60, "¡Y SE ENCIENDE!", 1), (62.5, "A MÁS DE 100 KM", 0.8),
    (66, "PARECEN SALIR", 1), (68.5, "DE LA CONSTELACIÓN", 0.8), (71, "DE LEO", 1), (74, "POR ESO SE LLAMAN", 0.8), (77, "LEÓNIDAS", 1),
    (80, "EN 1966", 1), (83, "HUBO UNA TORMENTA", 1), (87, "DE ESTRELLAS", 1), (89.5, "FUGACES", 1), (92, "MÁS DE 40", 1), (95, "POR SEGUNDO", 1),
    (100, "ESTE AÑO,", 1), (102, "LA NOCHE DEL 17", 1), (105, "UNAS 15 POR HORA", 1), (108, "DESPUÉS DE", 1), (110, "MEDIANOCHE", 1),
    (112, "LEJOS DE LAS LUCES", 0.8),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3, "blip"), (4, "whoosh"), (4.2, "sweep_fast"), (5, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(9, "sweep_up"), (16, "bits"), (18, "ping")]
    + [(26.5, "sweep_up"), (29, "ping")]
    + [(38.5, "sweep_fast"), (42, "power_up"), (46, "ding")]
    + [(55, "power_up"), (60, "sweep_fast"), (60.2, "ding")]
    + [(68, "sweep_fast"), (70, "ping"), (74, "ding")]
    + [(82, "sweep_fast"), (84, "sweep_fast"), (86, "bits"), (92, "error")]
    + [(100.5, "ding"), (102, "blip_up"), (105, "blip_up"), (108, "blip_up"), (110, "sweep_fast")]
    + outro_sfx(116)
)
