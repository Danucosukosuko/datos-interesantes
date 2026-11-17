"""Tema: ¿Cómo funciona un microondas? (tecnología)

Datos verificados (17-nov-2026; Lemelson-MIT «Percy Spencer», Wikipedia «Percy Spencer»,
greatpatent.com, Xunta de Galicia (serendipia), física básica de ondas):
- Percy Spencer (Raytheon) trabajaba con magnetrones de radar cuando notó que se le había derretido
  una chocolatina en el bolsillo (algunas fuentes dicen barrita de cacahuete). Probó con maíz:
  palomitas. Patente solicitada el 8-oct-1945. El primer horno comercial (1947) medía casi 1,8 m y
  pesaba unos 340 kg.
- El magnetrón emite microondas de 2,45 GHz: 2.450 millones de oscilaciones por segundo; longitud de
  onda c/f ≈ 12 cm.
- Las moléculas de agua (polares) intentan girar con el campo que cambia de sentido y el roce
  produce calor.
- No cocina «desde dentro»: las microondas solo entran unos centímetros; el centro se calienta
  después por conducción (por eso conviene remover o dejar reposar).
- Dentro se forman ondas estacionarias con puntos calientes y fríos: por eso el plato gira.
- La rejilla de la puerta tiene agujeros mucho más pequeños que 12 cm: las microondas no salen,
  la luz (ondas diminutas) sí, y por eso ves la comida.
- Metales con puntas o bordes (tenedores, papel de aluminio arrugado) pueden hacer chispas.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT

TITLE = "¿Cómo funciona un microondas?"
MUSIC_SEED = 20261117
MUSIC_KEY = 52
BOARD_SEED = 171

BROWN = (120, 70, 30)


def oven(c, x, y, w=120, h=80, on=False, b=0.0, door=True):
    c.box(x, y, w, h, PANEL, ORANGE, t=2)
    c.box(x + 6, y + 6, w - 36, h - 12, DARK, DIM)
    if on:
        c.rect(x + 7, y + 7, w - 38, h - 14, AMBER, a=0.18 + 0.06 * math.sin(b * 6))
    if door:
        for i in range(int((w - 40) / 4)):
            for j in range(int((h - 16) / 4)):
                c.rect(x + 8 + i * 4, y + 8 + j * 4, 1, 1, DIM, a=0.6)
    for k in range(3):
        c.rect(x + w - 24, y + 10 + k * 10, 16, 6, DIM)
    c.rect(x + w - 24, y + h - 20, 16, 10, RED if on else DIM)


def choco(c, x, y, melt=0.0):
    c.box(x, y, 26, 12, BROWN, DARK)
    for k in range(3):
        c.rect(x + 2 + k * 8, y + 2, 6, 8, gfx.mix(BROWN, ORANGE, 0.2))
    if melt > 0:
        for k in range(4):
            c.rect(x + 3 + k * 6, y + 12, 3, 2 + melt * (6 + (k % 2) * 5), BROWN)


def wave(c, x0, x1, y, amp, freq, phase, col=AMBER, a=1.0):
    prev = None
    for x in range(int(x0), int(x1)):
        yy = y + math.sin((x - x0) * freq + phase) * amp
        if prev:
            c.line(x - 1, prev, x, yy, col, a=a)
        prev = yy


def water(c, cx, cy, ang, s=1.0):
    c.disc(cx, cy, 5 * s, ORANGE)
    for sgn in (-1, 1):
        a = ang + sgn * 0.9
        c.disc(cx + math.cos(a) * 6 * s, cy + math.sin(a) * 6 * s, 3 * s, AMBER)


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    if l < 4:
        c.text("NACIÓ", 90, 34, AMBER, 3, "center")
        c.text("POR UN", 90, 66, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("CHOCOLATE", 90, 98, gfx.mix(RED, HOT, pulse * 0.3), 3, "center")
        c.ox = 0
        c.text("DERRETIDO", 90, 130, AMBER, 3, "center")
        choco(c, 77, 180, 0.6 + 0.3 * pulse)
        return
    c.text("¿CÓMO FUNCIONA", 90, 50, AMBER, 2, "center")
    c.text("EL MICROONDAS?", 90, 72, ORANGE, 2, "center")
    oven(c, 30, 130, on=True, b=b)


def s_1945(c, l, d, b, h):
    c.text("1945", 90, 42, AMBER, 3, "center")
    c.box(24, 80, 50, 70, PANEL, DIM)
    c.text("RADAR", 49, 86, AMBER, 1, "center")
    for k in range(3):
        f = ((l * 0.8) + k / 3) % 1
        c.ring(49, 120, 6 + f * 20, 1, AMBER, a=1 - f, a0=-60, a1=60)
    melt = gfx.clamp01((l - 4) / 3)
    choco(c, 110, 108, melt)
    c.text("SU BOLSILLO", 123, 94, ORANGE, 1, "center")
    if l >= 14:
        for k in range(6):
            f = ((l * 1.5) + k / 6) % 1
            c.disc(70 + k * 14, 186 - math.sin(f * math.pi) * 20, 4, HOT)
        c.text("¡Y PALOMITAS!", 90, 206, RED, 2, "center")


def s_magnetron(c, l, d, b, h):
    c.box(14, 92, 40, 40, PANEL, ORANGE, t=2)
    c.disc(34, 112, 10, DIM)
    c.disc(34, 112, 4, AMBER)
    c.text("MAGNETRÓN", 34, 140, AMBER, 1, "center")
    wave(c, 56, 172, 112, 10, 0.5, -b * 6, AMBER)
    if l >= 7:
        c.text("2.450 MILLONES", 112, 60, RED, 1, "center")
        c.text("DE VECES", 112, 72, AMBER, 1, "center")
        c.text("POR SEGUNDO", 112, 84, AMBER, 1, "center")
    if l >= 10:
        c.text("2,45 GHZ", 90, 180, ORANGE, 3, "center")


def s_agua(c, l, d, b, h):
    flip = math.sin(b * 8) * (1 if l >= 2 else 0.05)
    for k in range(6):
        x, y = 34 + (k % 3) * 56, 78 + (k // 3) * 56
        water(c, x, y, -math.pi / 2 + flip * 1.4 + k, 1.5)
    if l >= 0.5:
        c.text("MOLÉCULAS DE AGUA", 90, 44, AMBER, 1, "center")
    if l >= 6:
        heat = gfx.clamp01((l - 6) / 4)
        c.rect(0, 50, 180, 140, RED, a=0.18 * heat)
        if l >= 8:
            c.text("¡GIRAN Y ROZAN!", 90, 200, RED, 2, "center")
    if l >= 10.5:
        c.text("= CALOR", 90, 220, AMBER, 1, "center")


def s_fuera(c, l, d, b, h):
    r = 46
    c.disc(90, 124, r, DIM)
    depth = gfx.clamp01((l - 4) / 3) * 14
    for i in range(int(-r), int(r) + 1):
        w = math.sqrt(max(0, r * r - i * i))
        inner = math.sqrt(max(0, (r - depth) ** 2 - i * i)) if abs(i) < r - depth else 0
        c.rect(90 - w, 124 + i, w - inner, 1, RED, a=0.85)
        c.rect(90 + inner, 124 + i, w - inner, 1, RED, a=0.85)
    if l >= 4:
        c.text("SOLO UNOS CM", 90, 44, AMBER, 2, "center")
    if l >= 8:
        c.text("EL CENTRO, FRÍO", 90, 186, ORANGE, 2, "center")
    if l >= 11.5:
        c.text("¡REMUEVE!", 90, 206, RED, 2, "center")


def s_plato(c, l, d, b, h):
    oven(c, 20, 60, 140, 96, on=True, b=b, door=False)
    for k in range(5):
        x = 32 + k * 20
        hot = k % 2 == 0
        c.disc(x, 108, 5, RED if hot else DIM, a=0.8)
    if l >= 2:
        c.text("PUNTOS CALIENTES", 80, 44, RED, 1, "center")
    ang = b * 2 if l >= 7.5 else 0
    c.ring(80, 140, 30, 2, AMBER, a0=-180, a1=180)
    c.disc(80 + math.cos(ang) * 18, 140 + math.sin(ang) * 6, 4, AMBER)
    if l >= 7.5:
        c.text("POR ESO GIRA", 90, 180, AMBER, 2, "center")


def s_rejilla(c, l, d, b, h):
    c.box(30, 50, 120, 110, PANEL, ORANGE, t=2)
    for i in range(14):
        for j in range(12):
            c.rect(36 + i * 8, 56 + j * 8, 4, 4, DARK)
    if l >= 6:
        c.text("AGUJEROS", 90, 170, AMBER, 2, "center")
        c.text("MÁS PEQUEÑOS", 90, 190, AMBER, 1, "center")
    if l >= 10:
        c.text("QUE LA ONDA (12 CM)", 90, 202, AMBER, 1, "center")
    if l >= 14:
        wave(c, 150, 178, 90, 8, 0.4, -b * 6, RED)
        c.text("X", 166, 70, RED, 2, "center")
        pass
    if l >= 16:
        c.text("LA LUZ SÍ SALE", 90, 218, ORANGE, 1, "center")


def s_metal(c, l, d, b, h):
    c.text("¡OJO CON", 90, 44, RED, 3, "center")
    c.text("EL METAL!", 90, 76, RED, 3, "center")
    c.line(70, 120, 110, 180, DIM, t=3)
    for k in range(4):
        c.line(100 + k * 4, 116, 104 + k * 4, 132, DIM, t=2)
    if l >= 8:
        for k in range(6):
            a = b * 10 + k
            if int(b * 6 + k) % 2 == 0:
                c.line(108, 114, 108 + math.cos(a) * 12, 114 + math.sin(a) * 12, HOT, t=1)
        c.text("¡CHISPAS!", 90, 196, AMBER, 2, "center")


COVER_LINES = ["¿CÓMO", "CALIENTA", "EL MICRO?"]


def cover_art(c, y):
    oven(c, 30, y + 6, on=True)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 EN 1945", s_1945, False),
    (24, 38, "2 EL MAGNETRÓN", s_magnetron, False),
    (38, 52, "3 EL AGUA", s_agua, True),
    (52, 66, "4 POR FUERA", s_fuera, True),
    (66, 80, "5 EL PLATO", s_plato, False),
    (80, 100, "6 LA REJILLA", s_rejilla, False),
    (100, 116, "7 ¡OJO!", s_metal, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = [
    (0, "NACIÓ POR UN", 0.6), (1.5, "CHOCOLATE DERRETIDO", 0.6), (4, "¿CÓMO FUNCIONA", 0.6), (6, "EL MICROONDAS?", 0.8),
    (8.5, "EN 1945,", 1), (10, "PERCY SPENCER", 1), (12, "PROBABA UN RADAR", 1),
    (14, "Y SE LE DERRITIÓ", 0.8), (16, "EL CHOCOLATE", 1), (18, "DEL BOLSILLO", 1),
    (20, "PROBÓ CON MAÍZ", 1), (22, "¡Y PALOMITAS!", 1),
    (24, "EL CORAZÓN", 1), (25.5, "ES EL MAGNETRÓN", 1), (28, "LANZA ONDAS QUE VIBRAN", 0.6),
    (31, "2.450 MILLONES", 1), (33, "DE VECES", 1), (34.5, "POR SEGUNDO", 1),
    (38, "ESAS ONDAS", 1), (40, "MUEVEN EL AGUA", 1), (42, "DE LA COMIDA", 1),
    (44, "SUS MOLÉCULAS", 1), (46, "GIRAN Y ROZAN", 1), (48.5, "Y ESO ES CALOR", 1),
    (52, "PERO NO COCINA", 1), (54, "DESDE DENTRO:", 1), (56, "SOLO ENTRA", 1), (57.5, "UNOS CENTÍMETROS", 0.8),
    (60, "EL CENTRO", 1), (61.5, "SE QUEDA FRÍO", 1), (63.5, "¡REMUEVE!", 1),
    (66, "DENTRO HAY", 1), (68, "PUNTOS CALIENTES", 1), (70, "Y PUNTOS FRÍOS", 1),
    (72, "POR ESO", 1), (73.5, "EL PLATO GIRA", 1),
    (80, "¿Y POR QUÉ", 1), (82, "NO SE ESCAPAN?", 1), (84, "LA REJILLA", 1),
    (86, "TIENE AGUJEROS", 1), (88, "MÁS PEQUEÑOS", 1), (90, "QUE LA ONDA", 1),
    (92, "LAS MICROONDAS", 1), (94, "NO PASAN", 1), (96, "PERO LA LUZ SÍ", 1),
    (100, "Y OJO:", 1), (102, "EL METAL", 1), (104, "CON PUNTAS", 1), (106, "PUEDE HACER", 1), (108, "CHISPAS", 1),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3, "blip"), (4, "whoosh"), (4.2, "blip_up"), (5, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(9, "sweep_up"), (12, "power_down"), (17, "ping"), (20, "bits"), (22, "ding")]
    + [(25.5, "power_up"), (28, "sweep_fast"), (33, "ping")]
    + [(40, "bits"), (43, "sweep_up"), (48.5, "ding")]
    + [(56, "power_down"), (60, "ping"), (63.5, "error")]
    + [(68, "ping"), (72, "sweep_up")]
    + [(84, "blip_up"), (87, "ping"), (92, "error"), (96, "ding")]
    + [(102, "error"), (104, "bits"), (108, "error")]
    + outro_sfx(116)
)
