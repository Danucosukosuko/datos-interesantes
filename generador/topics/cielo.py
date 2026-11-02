"""Tema: ¿Por qué el cielo es azul?

Datos verificados:
- La luz del Sol tarda de media unos 500 s (8 min 20 s) en llegar a la Tierra (~150 millones de km / ~300.000 km/s).
- La luz "blanca" del Sol contiene todos los colores; cada color es una onda con distinta longitud
  (rojo ~700 nm, azul ~450 nm, violeta ~400 nm).
- Las moléculas del aire (sobre todo nitrógeno y oxígeno, ~0,2-0,3 nm) son más de mil veces más
  pequeñas que esas ondas -> dispersión de Rayleigh, proporcional a 1/longitud de onda^4.
- (700/450)^4 ≈ 5,9 -> el azul se dispersa casi 6 veces más que el rojo.
- El violeta se dispersa aún más, pero el cielo no se ve violeta: el Sol emite menos violeta,
  parte se absorbe en la alta atmósfera y nuestros ojos son más sensibles al azul.
- Al atardecer la luz atraviesa mucho más aire; el azul se dispersa por el camino y llegan rojos y naranjas.
- En Marte el cielo de día es de color caramelo/marrón amarillento (polvo) y los atardeceres son
  azulados: el polvo dispersa el azul hacia delante. Curiosity lo fotografió el 15-04-2015.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT, BG

TITLE = "¿Por qué el cielo es azul?"
MUSIC_SEED = 20261102
MUSIC_KEY = 55   # Sol menor
BOARD_SEED = 44


# ---------- elementos reutilizables ----------

def sun(c, cx, cy, r, b, rays=True):
    if rays:
        rot = b * 0.4
        for k in range(8):
            a = rot + k * math.pi / 4
            c.line(cx + math.cos(a) * (r + 4), cy + math.sin(a) * (r + 4),
                   cx + math.cos(a) * (r + 11), cy + math.sin(a) * (r + 11), AMBER, t=2)
    c.disc(cx, cy, r, AMBER)
    c.disc(cx - r * 0.3, cy - r * 0.3, r * 0.35, HOT, a=0.6)


def wave(c, x0, x1, yc, amp, wl, ph, col, t=2):
    for x in range(int(x0), int(x1)):
        c.rect(x, yc + amp * math.sin(2 * math.pi * x / wl - ph) - t / 2, 1, t, col)


def molecule(c, x, y, col=ORANGE):
    c.disc(x - 2, y, 2.5, col)
    c.disc(x + 2, y, 2.5, col)


def eye_small(c, cx, cy, s=1.0):
    for x in range(-12, 13, 2):
        hh = 7 * (1 - (x / 12) ** 2) * s
        c.rect(cx + x, cy - hh - 1, 2, 2, ORANGE)
        c.rect(cx + x, cy + hh - 1, 2, 2, ORANGE)
    c.disc(cx, cy, 4, AMBER)
    c.disc(cx, cy, 1.5, BG)


PERSON = [".#.", "###", ".#.", "#.#"]


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    lines = [("¿POR QUÉ", AMBER), ("EL CIELO", AMBER), ("ES AZUL?", ORANGE)]
    for k, (txt, col) in enumerate(lines):
        st = k * 0.5
        if l < st:
            continue
        p = gfx.ease_out_back((l - st) * 3, 2.2)
        c.text(txt, 90, gfx.lerp(-40, 44 + k * 36, p), col, 3, "center")
    s = gfx.ease_out_back(l * 2, 1.8)
    c.oy += round((1 - s) * 80)
    sun(c, 90, 204, 14, b)
    c.oy -= round((1 - s) * 80)
    if l >= 3:
        p = gfx.ease_out_back((l - 3) * 3, 2.4)
        col = RED if int(b * 2) % 2 == 0 else ORANGE
        c.text("¿VIOLETA?", 90, gfx.lerp(330, 150, p), col, 2, "center")


COLORS = ["ROJO", "NARANJA", "AMARILLO", "VERDE", "AZUL", "AÑIL", "VIOLETA"]


def s_luz(c, l, d, b, h):
    if l < 8:
        sun(c, 30, 104, 14, b)
        c.disc(152, 104, 16, PANEL)
        c.ring(152, 104, 16, 2, ORANGE, a0=-180, a1=180)
        c.rect(144, 98, 8, 5, DIM)
        c.rect(154, 108, 9, 4, DIM)
        c.text("TIERRA", 152, 126, ORANGE, 1, "center")
        t = gfx.clamp01((l - 0.5) / 5)
        x = gfx.lerp(48, 134, t)
        for i in range(48, int(x), 4):
            c.rect(i, 103, 2, 2, AMBER)
        if t < 1:
            c.rect(x - 3, 102, 6, 4, HOT)
        secs = int(500 * t)
        c.text(f"{secs // 60} MIN {secs % 60:02d} S", 90, 150, AMBER if t >= 1 else ORANGE, 2, "center")
        return
    q = l - 8
    # luz blanca entra en un prisma y se abre en colores
    c.text("LUZ BLANCA", 40, 52, AMBER, 1, "center")
    c.rect(0, 148, 74, 3, HOT)
    px, py = 90, 150
    for k in range(18):
        w = k * 1.6
        c.rect(px - w / 2, py - 14 + k * 1.6, w, 2, DIM)
    c.line(px, py - 15, px - 15, py + 14, ORANGE)
    c.line(px, py - 15, px + 15, py + 14, ORANGE)
    c.rect(px - 15, py + 13, 31, 2, ORANGE)
    n = min(7, int(q * 1.5) + 1)
    for k in range(n):
        ty = 108 + k * 13
        col = gfx.mix(RED, AMBER, k / 6)
        c.line(px + 8, py, 124, ty + 3, col)
        c.text(COLORS[k], 128, ty, col, 1)


def s_ondas(c, l, d, b, h):
    ph = b * 2 * math.pi * 0.5
    rows = [(0, "ROJO", "700 NM", 64, RED), (4, "AZUL", "450 NM", 40, AMBER), (9, "VIOLETA", "400 NM", 34, ORANGE)]
    for k, (st, name, nm, wl, col) in enumerate(rows):
        if l < st:
            continue
        p = gfx.ease_out_cubic((l - st) * 1.5)
        yl = 52 + k * 56
        c.text(name, 10, yl, col, 2)
        c.text(nm, 170, yl + 4, ORANGE, 1, "right")
        wave(c, 10, 10 + 160 * p, yl + 32, 9, wl, ph, col)
    if l >= 6:
        c.text("ONDA CORTA", 90, 214, AMBER, 1, "center")


def s_aire(c, l, d, b, h):
    ph = b * 2 * math.pi * 0.5
    if l < 7:
        for k in range(26):
            x = (k * 53 + l * (6 + k % 5)) % 176 + 2
            y = 60 + (k * 37) % 150 + math.sin(l * 2 + k) * 3
            molecule(c, x, y, ORANGE if k % 3 else AMBER)
        if l >= 2:
            c.text("N2", 44, 92, AMBER, 2, "center")
            c.text("O2", 136, 168, AMBER, 2, "center")
        return
    q = l - 7
    p = gfx.ease_out_back(q * 2, 1.6)
    wave(c, 6, 174, 120, 30 * p, 168, ph, AMBER, t=3)
    c.text("ONDA DE LUZ", 90, 74, AMBER, 1, "center")
    molecule(c, 90, 180)
    c.line(90, 186, 90, 196, DIM)
    c.text("MOLÉCULA", 90, 198, ORANGE, 1, "center")
    if q >= 2:
        c.text("+1.000 VECES", 90, 214, AMBER, 2, "center")
        c.text("MÁS PEQUEÑA", 90, 50, ORANGE, 2, "center")


def s_rebote(c, l, d, b, h):
    ph = b * 2 * math.pi
    mx, my = 90, 120
    if l < 8:
        wave(c, 0, mx - 4, my - 18, 6, 44, ph, RED)
        wave(c, 0, mx - 4, my + 18, 6, 22, ph, AMBER)
        c.text("ROJO", 4, my - 38, RED, 1)
        c.text("AZUL", 4, my + 28, AMBER, 1)
        molecule(c, mx, my, HOT)
        if l >= 2:
            wave(c, mx + 6, 180, my - 18, 6, 44, ph, RED)
            for k in range(12):
                a = k * math.pi / 6 + 0.2
                r = ((l - 2) * 22 + k * 3) % 60 + 8
                c.rect(mx + math.cos(a) * r - 2, my + math.sin(a) * r - 2, 4, 4, AMBER, a=1 - r / 70)
        if l >= 4:
            c.text("¡REBOTA!", 140, my + 34, AMBER, 1, "center")
        return
    q = l - 8
    p = gfx.ease_out_back(q * 2, 2.4)
    c.text("¡CASI x6!", 90, gfx.lerp(-30, 60, p), AMBER, 3, "center")
    e = gfx.ease_out_cubic(q / 2)
    c.text("ROJO", 6, 130, RED, 1)
    c.rect(40, 130, 22 * e, 8, RED)
    c.text("AZUL", 6, 156, AMBER, 1)
    c.rect(40, 156, 130 * e, 8, AMBER)
    c.text("DISPERSIÓN", 90, 186, ORANGE, 1, "center")


ITEMS = [(2, "EL SOL EMITE", "MENOS VIOLETA"), (6, "LA ALTA ATMÓSFERA", "ABSORBE PARTE"), (10, "TUS OJOS VEN", "MEJOR EL AZUL")]


def s_violeta(c, l, d, b, h):
    p = gfx.ease_out_back(l * 2, 2)
    c.text("¿Y EL VIOLETA?", 90, gfx.lerp(-30, 48, p), RED, 2, "center")
    for k, (st, a, z) in enumerate(ITEMS):
        if l < st:
            continue
        q = gfx.ease_out_back((l - st) * 2.5, 1.8)
        c.ox += round((1 - q) * 180)
        y = 84 + k * 46
        if k == 0:
            sun(c, 22, y + 8, 7, b, rays=False)
        elif k == 1:
            for j in range(3):
                c.rect(10 + j * 8, y + 4 + (j % 2) * 4, 6, 3, ORANGE)
            c.rect(10, y + 14, 26, 2, DIM)
        else:
            eye_small(c, 23, y + 8)
        c.text(a, 44, y, AMBER, 1)
        c.text(z, 44, y + 11, ORANGE, 1)
        c.ox -= round((1 - q) * 180)


def s_atardecer(c, l, d, b, h):
    cx, cy, R, A = 90, 430, 240, 30
    eve = gfx.ease_in_out((l - 8) / 4)
    # cielo que se enrojece
    c.rect(0, 40, 180, 160, RED, a=0.28 * eve)
    c.ring(cx, cy, R, A, ORANGE, a=0.18, a0=-180, a1=0)
    c.disc(cx, cy, R, PANEL)
    c.ring(cx, cy, R, 2, ORANGE, a0=-180, a1=0)
    c.text("ATMÓSFERA", 170, 176, DIM, 1, "right")
    ox, oy = 88, 182
    c.sprite(PERSON, ox - 3, oy - 8, {"#": AMBER}, 2)
    ang = gfx.lerp(-90, -172, eve)
    sx = ox + math.cos(math.radians(ang)) * 80
    sy = oy + math.sin(math.radians(ang)) * 80
    sun(c, sx, sy, 10, b)
    # trayecto de la luz dentro de la atmósfera
    steps = 60
    for i in range(steps):
        f = i / steps
        x = gfx.lerp(sx, ox, f)
        y = gfx.lerp(sy, oy - 4, f)
        inside = (x - cx) ** 2 + (y - cy) ** 2 <= (R + A) ** 2
        col = (RED if eve > 0.5 else AMBER) if inside else DIM
        c.rect(x, y, 2, 2, col)
        if inside and eve > 0.5 and i % 6 == 0:
            r = ((l * 10 + i) % 14)
            c.rect(x, y - 4 - r, 2, 2, AMBER, a=1 - r / 14)
    if l < 8:
        c.text("POCO AIRE", 120, 150, AMBER, 1)
    if l >= 10:
        c.text("MUCHO MÁS AIRE", 90, 130, AMBER, 1, "center")
    if l >= 14:
        p = gfx.ease_out_back((l - 14) * 2, 2.2)
        c.text("ROJO Y NARANJA", 90, gfx.lerp(-30, 52, p), RED, 2, "center")


ROVER = ["..##....", "..##....", "########", "#.####.#", "########", ".#.##.#."]


def s_marte(c, l, d, b, h):
    sunset = l >= 7
    c.rect(0, 40, 180, 156, AMBER if not sunset else DARK, a=0.16 if not sunset else 0.5)
    p = gfx.ease_out_back(l * 2, 2)
    c.text("MARTE", 90, gfx.lerp(-30, 50, p), RED, 3, "center")
    # suelo con rocas
    c.rect(0, 196, 180, 40, PANEL)
    for k in range(9):
        x = (k * 41) % 170 + 4
        c.rect(x, 200 + (k * 7) % 22, 6 + k % 3 * 3, 3, DIM)
    c.sprite(ROVER, 22 + l * 2, 180, {"#": ORANGE}, 2)
    if not sunset:
        sun(c, 140, 100, 7, b, rays=False)
        c.text("CIELO DE DÍA:", 90, 132, ORANGE, 1, "center")
        c.text("CARAMELO", 90, 144, AMBER, 2, "center")
    else:
        q = l - 7
        sy = gfx.lerp(150, 186, gfx.ease_in_out(q / 9))
        for k in range(3):
            c.ring(130, sy, 9 + k * 6, 2, DIM, a=0.8 - k * 0.2, a0=-180, a1=180)
        c.disc(130, sy, 4, HOT)
        c.line(102, 116, 120, sy - 12, DIM)
        c.text("HALO AZUL", 70, 108, AMBER, 1, "center")
        c.text("ATARDECER", 90, 80, AMBER, 2, "center")
        c.text("(CURIOSITY, 2015)", 90, 124, ORANGE, 1, "center")


COVER_LINES = ["¿POR QUÉ", "EL CIELO", "ES AZUL?"]


def cover_art(c, y):
    cx, cy = 90, y + 36
    for k in range(12):
        a = k * math.pi / 6
        c.line(cx + math.cos(a) * 24, cy + math.sin(a) * 24,
               cx + math.cos(a) * 32, cy + math.sin(a) * 32, AMBER, t=3)
    c.disc(cx, cy, 19, AMBER)
    c.disc(cx - 6, cy - 6, 6, HOT, a=0.6)
    for (mx, my) in ((30, cy - 14), (150, cy + 10), (36, cy + 18), (146, cy - 18)):
        molecule(c, mx, my)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 LUZ", s_luz, False),
    (24, 38, "2 ONDAS", s_ondas, False),
    (38, 52, "3 AIRE", s_aire, False),
    (52, 66, "4 REBOTE", s_rebote, True),
    (66, 80, "5 VIOLETA", s_violeta, False),
    (80, 100, "6 ATARDECER", s_atardecer, False),
    (100, 116, "7 MARTE", s_marte, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = [
    (0, "LA FÍSICA DICE", 0.5), (3, "QUE DEBERÍA", 0.5), (5, "SER VIOLETA", 0.5),
    (8, "LA LUZ DEL SOL", 1), (11, "TARDA 8 MINUTOS", 1), (14, "EN LLEGAR", 1),
    (16, "PARECE BLANCA", 1), (19, "PERO LLEVA", 1), (21, "TODOS LOS COLORES", 1),
    (24, "CADA COLOR ES", 1), (27, "UNA ONDA", 1),
    (28, "EL ROJO: LARGA", 1), (31, "EL AZUL: CORTA", 1), (34, "EL VIOLETA,", 1), (35.5, "AÚN MÁS CORTA", 0.8),
    (38, "EL AIRE ESTÁ", 1), (41, "LLENO DE MOLÉCULAS", 1),
    (45, "MÁS DE MIL VECES", 1), (49, "MÁS PEQUEÑAS", 1),
    (52, "AL CHOCAR", 1), (54, "LAS ONDAS CORTAS", 1), (57, "REBOTAN MUCHO MÁS", 1),
    (60, "EL AZUL REBOTA", 1), (62.5, "CASI 6 VECES", 1), (65, "MÁS", 1),
    (66, "¿Y EL VIOLETA?", 1), (68, "EL SOL EMITE MENOS", 0.8),
    (72, "PARTE SE ABSORBE", 1), (76, "Y TUS OJOS VEN", 0.6), (78, "MEJOR EL AZUL", 0.6),
    (80, "AL ATARDECER", 1), (83, "LA LUZ CRUZA", 1), (86, "MUCHO MÁS AIRE", 1),
    (89, "EL AZUL SE PIERDE", 1), (93, "Y LLEGAN", 1), (95, "ROJOS Y NARANJAS", 1),
    (100, "EN MARTE", 1), (102, "ES AL REVÉS", 1),
    (104, "CIELO CARAMELO", 1), (107, "Y ATARDECERES", 1), (110, "AZULES", 1),
]

SFX = (
    [(0, "whoosh"), (0, "blip_up"), (0.5, "blip_up"), (1, "blip_up"), (1.5, "power_up"),
     (3, "error"), (5, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(8.5, "send")] + [(9 + k, "tick") for k in range(5)] + [(13.5, "ding")]
    + [(16, "sweep_up"), (17, "blip_up"), (17.7, "blip_up"), (18.3, "blip_up"), (19, "blip_up"),
       (19.7, "blip_up"), (20.3, "blip_up"), (21, "power_up")]
    + [(24.5, "sweep_up"), (28, "sweep_up"), (33, "sweep_fast"), (36, "ping")]
    + [(39, "bits"), (40, "blip"), (45, "power_down"), (47, "ping"), (49, "ding")]
    + [(53, "send"), (54, "ping"), (55, "ping"), (56, "ping"), (58, "ping"), (60, "power_up"), (62, "sweep_up")]
    + [(66.5, "error"), (68, "blip_up"), (72, "blip_up"), (76, "blip_up"), (78, "ding")]
    + [(84, "power_down"), (90, "sweep_up"), (94, "ding")]
    + [(100.5, "thud"), (102, "blip"), (104, "ding"), (107, "power_down"), (110, "power_up")]
    + outro_sfx(116)
)
