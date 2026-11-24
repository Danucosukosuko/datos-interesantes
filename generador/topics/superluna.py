"""Tema: ¿Qué es una superluna? (espacio; superluna del 24-nov-2026, «Superluna del Castor»)

Datos verificados (24-nov-2026; Star Walk, Bindi, Space.com, NASA «What is a supermoon», N+):
- La órbita de la Luna es ovalada: en el punto más cercano (perigeo) está a unos 356.000-370.000 km
  y en el más lejano (apogeo) a unos 405.000 km.
- Superluna = luna llena cerca del perigeo. Hoy 24-nov la Luna está a ~360.800 km: más de
  40.000 km más cerca que en el apogeo.
- Se ve ~6,5 % más grande y ~13,5 % más brillante que una luna llena media (Star Walk).
- La luna llena es hoy a las 15:53 (hora peninsular); mejor verla al salir, al anochecer, por el este.
- La Luna parece enorme en el horizonte, pero es una ilusión del cerebro («ilusión lunar»): su
  tamaño en el cielo es el mismo (compruébalo tapándola con el pulgar).
- La superluna más grande de 2026 será la del 24 de diciembre (Nochebuena), a ~356.740 km.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT
from topics.luna import moon, earth, stars

TITLE = "¿Qué es una superluna?"
MUSIC_SEED = 20261124
MUSIC_KEY = 57
BOARD_SEED = 241


def city(c, y=210):
    for k in range(9):
        h = 8 + (k * 7) % 14
        c.rect(6 + k * 19, y - h, 15, h + 20, DARK)
        for j in range(2):
            c.rect(9 + k * 19 + j * 6, y - h + 3, 2, 2, AMBER if (k + j) % 3 else DIM)


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    stars(c, b)
    if l < 4:
        c.text("HOY LA", 90, 32, AMBER, 3, "center")
        c.text("LUNA ESTÁ", 90, 64, AMBER, 3, "center")
        c.text("40.000 KM", 90, 96, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("MÁS CERCA", 90, 128, gfx.mix(RED, HOT, pulse * 0.3), 3, "center")
        c.ox = 0
        moon(c, 90, 200, 30, 0.5, glow=0.25 * pulse)
        return
    c.text("¿QUÉ ES", 90, 46, AMBER, 3, "center")
    c.text("UNA", 90, 78, ORANGE, 3, "center")
    c.text("SUPERLUNA?", 90, 110, RED, 3, "center")
    moon(c, 90, 196, 32, 0.5, glow=0.2)


def s_orbita(c, l, d, b, h):
    cx, cy = 90, 128
    for k in range(140):
        t = k / 140 * 2 * math.pi
        c.rect(cx + 10 + math.cos(t) * 70, cy + math.sin(t) * 58, 1, 1, DIM)
    earth(c, cx - 4, cy, 10)
    t = l * 0.4
    moon(c, cx + 10 + math.cos(t) * 70, cy + math.sin(t) * 58, 6, 0.5)
    if l >= 4.5:
        c.text("ÓRBITA OVALADA", 90, 42, AMBER, 1, "center")
    if l >= 8:
        c.text("CERCA:", 40, 196, AMBER, 1, "center")
        c.text("360.000 KM", 40, 206, AMBER, 1, "center")
    if l >= 12:
        c.text("LEJOS:", 140, 196, ORANGE, 1, "center")
        c.text("405.000 KM", 140, 206, ORANGE, 1, "center")


def s_super(c, l, d, b, h):
    stars(c, b)
    c.text("LUNA LLENA", 90, 50, AMBER, 2, "center")
    if l >= 2.5:
        c.text("+", 90, 74, AMBER, 2, "center")
        c.text("MUY CERCA", 90, 96, AMBER, 2, "center")
    if l >= 7:
        c.text("=", 90, 120, RED, 2, "center")
        p = gfx.ease_out_back((l - 7) * 1.5, 1.6)
        c.text("SUPERLUNA", 90, 144, RED, 3, "center")
        moon(c, 90, 200, 18 + 6 * p, 0.5, glow=0.3)


def s_grande(c, l, d, b, h):
    q = gfx.ease_out_cubic(gfx.clamp01((l - 2) / 3))
    moon(c, 52, 120, 30, 0.5)
    c.text("NORMAL", 52, 160, DIM, 1, "center")
    moon(c, 128, 120, 30 * (1 + 0.065 * q * 3), 0.5)
    c.text("SUPER", 128, 160, AMBER, 1, "center")
    if l >= 2:
        c.text("6,5 %", 90, 40, RED, 3, "center")
        c.text("MÁS GRANDE", 90, 66, RED, 2, "center")
    c.text("(EXAGERADO PARA QUE SE VEA)", 90, 188, DIM, 1, "center")


def s_brillo(c, l, d, b, h):
    q = gfx.clamp01((l - 0.5) / 3)
    c.rect(0, 30, 180, 200, AMBER, a=0.05 + 0.12 * q)
    moon(c, 90, 140, 40, 0.5, glow=0.5 * q)
    if l >= 0.5:
        c.text("13,5 % MÁS", 90, 46, RED, 2, "center")
        c.text("BRILLANTE", 90, 66, RED, 2, "center")


def s_ilusion(c, l, d, b, h):
    stars(c, b)
    city(c, 210)
    r = 36 if l < 8 else 36 - gfx.clamp01((l - 8) / 2) * 22
    moon(c, 120, 186, r, 0.5, glow=0.15)
    if l >= 1.5:
        c.text("¿ENORME?", 60, 46, AMBER, 2, "center")
    if l >= 5.5:
        c.text("ES UNA ILUSIÓN", 90, 70, RED, 2, "center")
    if l >= 8:
        c.text("TÁPALA CON EL PULGAR", 90, 92, AMBER, 1, "center")


def s_diciembre(c, l, d, b, h):
    stars(c, b)
    c.text("LA MÁS GRANDE", 90, 46, AMBER, 2, "center")
    c.text("DEL AÑO:", 90, 64, AMBER, 2, "center")
    if l >= 8:
        c.text("24 DIC", 90, 96, RED, 4, "center")
        moon(c, 90, 178, 30, 0.5, glow=0.3)
    if l >= 11:
        c.text("NOCHEBUENA", 90, 216, ORANGE, 2, "center")


def s_hoy(c, l, d, b, h):
    stars(c, b)
    city(c, 210)
    rise = gfx.ease_out_cubic(gfx.clamp01(l / 8))
    moon(c, 130, 230 - rise * 90, 22, 0.5, glow=0.25)
    c.text("ESTA NOCHE", 70, 46, RED, 2, "center")
    if l >= 2:
        c.text("AL ANOCHECER", 70, 66, AMBER, 1, "center")
    if l >= 5:
        c.text("MIRA AL ESTE", 70, 78, AMBER, 1, "center")


COVER_LINES = ["HOY HAY", "SUPERLUNA"]


def cover_art(c, y):
    moon(c, 90, y + 44, 40, 0.5, glow=0.25)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 LA ÓRBITA", s_orbita, False),
    (24, 38, "2 LA RECETA", s_super, False),
    (38, 52, "3 MÁS GRANDE", s_grande, True),
    (52, 66, "4 MÁS BRILLO", s_brillo, True),
    (66, 80, "5 LA ILUSIÓN", s_ilusion, False),
    (80, 100, "6 LA MEJOR", s_diciembre, False),
    (100, 116, "7 ¡MÍRALA!", s_hoy, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = [
    (0, "HOY LA LUNA", 0.6), (1.5, "ESTÁ 40.000 KM", 0.6), (3, "MÁS CERCA", 0.5), (4, "¿QUÉ ES UNA", 0.6), (6, "SUPERLUNA?", 1),
    (8.5, "LA LUNA NO GIRA", 1), (11, "EN CÍRCULO:", 1), (12.5, "SU ÓRBITA", 1), (14, "ES OVALADA", 1),
    (16, "CERCA, A UNOS", 1), (17.5, "360.000 KM", 1), (20, "LEJOS, A 405.000", 1),
    (24, "SI ESTÁ LLENA", 1), (26.5, "Y MUY CERCA", 1), (29, "DE LA TIERRA...", 1), (31, "¡ES UNA", 1), (32.5, "SUPERLUNA!", 1),
    (38, "SE VE UN", 1), (40, "6,5 % MÁS GRANDE", 1), (43, "QUE UNA LUNA", 1), (45, "LLENA NORMAL", 1),
    (52, "Y UN 13,5 %", 1), (54.5, "MÁS BRILLANTE", 1), (57, "¡ILUMINA", 1), (59, "MÁS LA NOCHE!", 1),
    (66, "AL SALIR", 1), (67.5, "PARECE ENORME", 1), (70, "PERO ES", 1), (71.5, "UNA ILUSIÓN", 1),
    (74, "TÁPALA", 1), (75.5, "CON EL PULGAR", 1),
    (80, "Y OJO:", 1), (82, "LA MÁS GRANDE", 1), (84, "DEL AÑO", 1), (86, "LLEGA EL", 1), (88, "24 DE DICIEMBRE", 1),
    (91, "¡EN NOCHEBUENA!", 1),
    (100, "ESTA NOCHE", 1), (102, "AL ANOCHECER", 1), (105, "MIRA AL ESTE", 1), (108, "Y BÚSCALA", 1),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3, "blip"), (4, "whoosh"), (4.2, "blip_up"), (5, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(11, "sweep_up"), (14, "ping"), (17, "blip_up"), (20, "blip_up")]
    + [(27, "blip_up"), (30, "blip_up"), (32.5, "power_up")]
    + [(40, "sweep_up"), (43, "ding")]
    + [(54, "sweep_up"), (57, "ding")]
    + [(67.5, "ping"), (72, "power_down"), (75.5, "blip")]
    + [(84, "sweep_up"), (88, "ding"), (91, "power_up")]
    + [(100.5, "sweep_up"), (105, "ping")]
    + outro_sfx(116)
)
