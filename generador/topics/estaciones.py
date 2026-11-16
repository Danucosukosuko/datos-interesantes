"""Tema: ¿Por qué existen las estaciones? (espacio)

Datos verificados (16-nov-2026; IGN «El invierno», Starwalk, Enterat, NASA Space Place):
- La Tierra está MÁS cerca del Sol a principios de enero (perihelio, ~147 millones de km) y más
  lejos a principios de julio (afelio, ~152 millones de km). En pleno invierno del hemisferio norte
  estamos más cerca: la distancia NO explica las estaciones.
- Prueba: cuando aquí es invierno, en Australia es verano (hemisferios al revés).
- La causa es la inclinación del eje de la Tierra (~23,4°): durante el año cada hemisferio se
  inclina hacia el Sol o se aleja.
- Hacia el Sol: los rayos llegan más rectos (la misma luz se concentra en menos superficie) y los
  días son más largos. En Madrid, ~15 h de luz en junio y ~9 h en diciembre.
- Solsticio de invierno 2026: lunes 21 de diciembre, 21:50 (hora peninsular): el día más corto;
  desde ahí los días empiezan a alargarse.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT

TITLE = "¿Por qué existen las estaciones?"
MUSIC_SEED = 20261116
MUSIC_KEY = 57
BOARD_SEED = 161

TILT = math.radians(23.4)


def sun(c, cx, cy, r, b):
    c.disc(cx, cy, r, AMBER)
    for k in range(10):
        a = k * math.pi / 5 + b * 0.2
        c.line(cx + math.cos(a) * (r + 3), cy + math.sin(a) * (r + 3),
               cx + math.cos(a) * (r + 7), cy + math.sin(a) * (r + 7), AMBER)


def earth(c, cx, cy, r, tilt=TILT, lit_side=None, b=0.0):
    """Tierra con eje inclinado. lit_side: -1 luz por la izquierda, 1 por la derecha, None todo."""
    c.disc(cx, cy, r, ORANGE)
    c.disc(cx - r * 0.3, cy - r * 0.25, r * 0.32, DIM)
    c.disc(cx + r * 0.35, cy + r * 0.3, r * 0.25, DIM)
    if lit_side is not None:
        for i in range(int(-r), int(r) + 1):
            w = math.sqrt(max(0, r * r - i * i))
            if lit_side > 0:
                c.rect(cx - w, cy + i, w, 1, DARK, a=0.65)
            else:
                c.rect(cx, cy + i, w, 1, DARK, a=0.65)
    dx, dy = math.sin(tilt), -math.cos(tilt)
    c.line(cx - dx * (r + 6), cy - dy * (r + 6), cx + dx * (r + 6), cy + dy * (r + 6), AMBER, t=1)
    ex, ey = -dy, dx
    c.line(cx - ex * r, cy - ey * r, cx + ex * r, cy + ey * r, DIM, t=1)


def ground_beam(c, x, y, w, ang, col=AMBER, label=None):
    """Haz de linterna que llega al suelo con un ángulo: más inclinado = mancha más larga."""
    spread = w / max(0.25, math.sin(ang))
    c.rect(x - spread / 2, y, spread, 4, col, a=0.85)
    top = y - 60
    for k in range(int(w)):
        f = k / w
        x0 = x - w / 2 + k - math.cos(ang) * 60
        x1 = x - spread / 2 + f * spread
        c.line(x0, top, x1, y, col, a=0.35)
    if label:
        c.text(label, x, y + 8, col, 1, "center")


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    if l < 4:
        c.text("EN ENERO", 90, 34, AMBER, 3, "center")
        c.text("ESTAMOS", 90, 66, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("MÁS CERCA", 90, 98, gfx.mix(RED, HOT, pulse * 0.3), 3, "center")
        c.ox = 0
        c.text("DEL SOL", 90, 130, AMBER, 3, "center")
        sun(c, 56, 204, 18, b)
        earth(c, 128, 204, 12)
        return
    c.text("¿POR QUÉ", 90, 44, AMBER, 3, "center")
    c.text("HAY", 90, 76, ORANGE, 3, "center")
    c.text("ESTACIONES?", 90, 110, ORANGE, 2, "center")
    sun(c, 56, 200, 18, b)
    earth(c, 128, 200, 12)


def s_distancia(c, l, d, b, h):
    cx, cy, a, bb = 96, 128, 70, 44
    for k in range(120):
        t = k / 120 * 2 * math.pi
        c.rect(cx + math.cos(t) * a, cy + math.sin(t) * bb, 1, 1, DIM)
    sun(c, cx - 18, cy, 12, b)
    t = math.pi + l * 0.35
    earth(c, cx + math.cos(t) * a, cy + math.sin(t) * bb, 7)
    if l >= 5:
        c.text("ENERO", 26, 172, AMBER, 1, "center")
        c.text("147 M KM", 26, 182, AMBER, 1, "center")
    if l >= 9:
        c.text("JULIO", 154, 172, ORANGE, 1, "center")
        c.text("152 M KM", 154, 182, ORANGE, 1, "center")
    if l >= 12:
        c.text("¡MÁS CERCA EN ENERO!", 90, 46, RED, 1, "center")


def s_no_es(c, l, d, b, h):
    c.text("DICIEMBRE", 90, 42, AMBER, 2, "center")
    c.box(14, 66, 70, 80, PANEL, DIM)
    c.text("ESPAÑA", 49, 72, AMBER, 1, "center")
    for k in range(6):
        f = ((l * 0.6) + k / 6) % 1
        c.rect(22 + k * 10, 86 + f * 50, 2, 2, AMBER)
    c.text("FRÍO", 49, 132, ORANGE, 1, "center")
    if l >= 5.5:
        c.box(96, 66, 70, 80, PANEL, AMBER)
        c.text("AUSTRALIA", 131, 72, AMBER, 1, "center")
        sun(c, 131, 104, 9, b)
        c.text("PLAYA", 131, 132, RED, 1, "center")
    if l >= 9.5:
        c.text("SI FUERA LA DISTANCIA,", 90, 168, AMBER, 1, "center")
        c.text("SERÍA IGUAL EN TODAS", 90, 180, AMBER, 1, "center")
        c.text("¡NO ES ESO!", 90, 200, RED, 2, "center")


def s_eje(c, l, d, b, h):
    q = gfx.ease_in_out((l - 2) / 3)
    earth(c, 90, 120, 40, TILT * q)
    c.line(90, 60, 90, 180, DIM)
    if l >= 8:
        c.text("23,4 GRADOS", 90, 186, RED, 2, "center")
    if l >= 2:
        c.text("EL EJE ESTÁ", 90, 42, AMBER, 2, "center")
        c.text("INCLINADO", 90, 58, AMBER, 2, "center")


def s_rayos(c, l, d, b, h):
    c.rect(10, 150, 160, 2, DIM)
    ground_beam(c, 50, 150, 22, math.radians(80), AMBER, "VERANO")
    if l >= 6:
        ground_beam(c, 128, 150, 22, math.radians(30), ORANGE, "INVIERNO")
    if l >= 4:
        c.text("RECTOS = MÁS CALOR", 90, 46, AMBER, 1, "center")
    if l >= 9:
        c.text("TORCIDOS = SE REPARTE", 90, 58, ORANGE, 1, "center")


def s_dias(c, l, d, b, h):
    c.text("MADRID", 90, 40, AMBER, 2, "center")
    for k, (lab, hours, col, st) in enumerate((("JUNIO", 15, AMBER, 5.5), ("DICIEMBRE", 9, DIM, 9))):
        if l < st:
            continue
        q = gfx.ease_out_cubic((l - st) / 2)
        y = 80 + k * 60
        c.text(lab, 90, y, col, 1, "center")
        w = 150 * hours / 24 * q
        c.box(15, y + 12, 150, 14, DARK, DIM)
        c.rect(15, y + 12, w, 14, col)
        c.text(f"{int(hours * q)} H DE LUZ", 90, y + 30, col, 1, "center")


def s_reves(c, l, d, b, h):
    sun(c, 30, 128, 18, b)
    earth(c, 120, 128, 34, TILT, lit_side=-1)
    c.text("NORTE", 140, 76, AMBER, 1, "center")
    c.text("SUR", 100, 182, AMBER, 1, "center")
    if l >= 7:
        c.text("INVIERNO", 150, 64, ORANGE, 1, "center")
    if l >= 11:
        c.text("VERANO", 90, 194, RED, 1, "center")
    if l >= 13.5:
        c.text("NAVIDAD EN LA PLAYA", 90, 46, AMBER, 1, "center")


def s_solsticio(c, l, d, b, h):
    c.text("21 DIC", 90, 44, RED, 4, "center")
    if l >= 2.5:
        c.text("DÍA MÁS CORTO", 90, 86, AMBER, 2, "center")
    if l >= 6:
        c.text("EMPIEZA EL INVIERNO", 90, 110, ORANGE, 1, "center")
    if l >= 11:
        q = gfx.clamp01((l - 11) / 4)
        c.box(15, 140, 150, 14, DARK, DIM)
        c.rect(15, 140, 150 * (9 + q) / 24, 14, AMBER)
        c.text("Y LOS DÍAS CRECEN", 90, 160, AMBER, 1, "center")


COVER_LINES = ["¿POR QUÉ", "HAY", "INVIERNO?"]


def cover_art(c, y):
    sun(c, 50, y + 40, 20, 0)
    earth(c, 130, y + 40, 22, TILT, lit_side=-1)
    c.text("NO ES LA DISTANCIA", 90, y + 74, RED, 1, "center")


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 LA DISTANCIA", s_distancia, False),
    (24, 38, "2 ¡NO ES ESO!", s_no_es, False),
    (38, 52, "3 EL EJE", s_eje, True),
    (52, 66, "4 LOS RAYOS", s_rayos, True),
    (66, 80, "5 DÍAS LARGOS", s_dias, False),
    (80, 100, "6 AL REVÉS", s_reves, False),
    (100, 116, "7 EL 21 DE DIC.", s_solsticio, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = [
    (0, "EN ENERO", 0.6), (1.5, "ESTAMOS MÁS CERCA", 0.5), (3, "DEL SOL", 0.5), (4, "¿POR QUÉ HAY", 0.6), (6, "ESTACIONES?", 1),
    (8.5, "LA TIERRA GIRA", 1), (11, "ALREDEDOR DEL SOL", 0.8),
    (13, "EN ENERO ESTÁ", 1), (15, "A 147 MILLONES DE KM", 0.6),
    (17, "EN JULIO, A 152", 1), (20, "¡MÁS CERCA EN ENERO!", 0.8),
    (24, "Y AUN ASÍ", 1), (26, "EN DICIEMBRE", 1), (27.5, "AQUÍ HACE FRÍO", 1),
    (29.5, "Y EN AUSTRALIA", 1), (31.5, "ES VERANO", 1), (33.5, "LA DISTANCIA", 1), (35.5, "NO ES LA CAUSA", 1),
    (38, "LA CAUSA:", 1), (40, "EL EJE DE LA TIERRA", 0.8), (43, "ESTÁ INCLINADO", 1), (46, "23,4 GRADOS", 1),
    (52, "EN VERANO", 1), (54, "LOS RAYOS LLEGAN", 1), (56, "MÁS RECTOS", 1),
    (58, "EN INVIERNO,", 1), (59.5, "TORCIDOS", 1), (61, "Y LA LUZ", 1), (62.5, "SE REPARTE", 1),
    (66, "Y LOS DÍAS", 1), (68, "SON MÁS LARGOS", 1), (70, "EN MADRID:", 1),
    (71.5, "15 HORAS EN JUNIO", 0.8), (75, "9 EN DICIEMBRE", 1),
    (80, "POR ESO", 1), (82, "LOS HEMISFERIOS", 1), (84.5, "VAN AL REVÉS", 1),
    (87, "CUANDO EL NORTE", 1), (89, "MIRA AL SOL", 1), (91, "EL SUR SE ALEJA", 1),
    (93.5, "NAVIDAD", 1), (95, "EN LA PLAYA", 1),
    (100, "EL 21 DE DICIEMBRE", 0.8), (102.5, "LLEGA EL DÍA", 1), (104.5, "MÁS CORTO", 1),
    (106, "EMPIEZA EL INVIERNO", 0.8), (109, "Y DESDE AHÍ", 1), (111, "LOS DÍAS CRECEN", 1),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3, "blip"), (4, "whoosh"), (4.2, "blip_up"), (5, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(11, "ping"), (15, "blip_up"), (19, "blip_up"), (20, "ding")]
    + [(27, "blip_up"), (31, "ping"), (35.5, "error")]
    + [(38.5, "sweep_up"), (41, "ding"), (46, "ping")]
    + [(53, "sweep_fast"), (56, "power_up"), (59, "power_down")]
    + [(67, "sweep_up"), (71, "sweep_up"), (75, "ping")]
    + [(83, "sweep_fast"), (89, "ping"), (93.5, "ding")]
    + [(100.5, "power_down"), (102, "ding"), (109, "sweep_up"), (111, "power_up")]
    + outro_sfx(116)
)
