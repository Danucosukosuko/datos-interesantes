"""Tema: ¿Cómo funciona el WiFi?

Datos verificados:
- El router emite ondas de radio en las bandas de 2,4 GHz, 5 GHz (y 6 GHz en WiFi 6E/7).
- 2,4 GHz = 2.400 millones de oscilaciones por segundo.
- Los datos se codifican modulando la onda (amplitud y fase, QAM) y viajan en paquetes
  con la dirección (MAC) del dispositivo de destino.
- 2,4 GHz tiene más alcance y atraviesa mejor las paredes; 5 GHz es más rápida pero llega menos.
- WiFi 7 (IEEE 802.11be): hasta ~46 Gbit/s teóricos.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT, BG, TRACE

TITLE = "¿Cómo funciona el WiFi?"
MUSIC_SEED = 11
MUSIC_KEY = 57   # La menor
BOARD_SEED = 21


# ---------- elementos reutilizables ----------

def router(c, x, y, b, on=True):
    c.rect(x + 6, y - 16, 3, 16, ORANGE)
    c.rect(x + 39, y - 16, 3, 16, ORANGE)
    c.rect(x + 5, y - 19, 5, 3, AMBER)
    c.rect(x + 38, y - 19, 5, 3, AMBER)
    c.box(x, y, 48, 16, PANEL, ORANGE)
    pat = int(b * 4)
    for k in range(4):
        lit = on and ((pat >> k) & 1 or k == 0)
        c.rect(x + 7 + k * 6, y + 7, 3, 3, AMBER if lit else DIM)
    c.rect(x + 34, y + 6, 9, 5, DARK)
    c.rect(x + 4, y + 16, 6, 2, DIM)
    c.rect(x + 38, y + 16, 6, 2, DIM)


def phone(c, x, y, w, h, bars=0):
    c.box(x, y, w, h, DARK, ORANGE, t=2)
    c.rect(x + 4, y + 9, w - 8, h - 18, PANEL)
    c.rect(x + w / 2 - 5, y + 4, 10, 2, DIM)
    c.rect(x + w / 2 - 3, y + h - 6, 6, 3, DIM)
    for k in range(4):
        bh = 2 + k * 2
        c.rect(x + w - 8 - (3 - k) * 3, y + 9 + 9 - bh, 2, bh, AMBER if k < bars else DIM)


def wifi_icon(c, cx, cy, lit=3, glow=0.0):
    for k in range(3):
        col = gfx.mix(ORANGE, HOT, glow) if k < lit else DIM
        c.ring(cx, cy, 7 + k * 8, 4, col, a0=-135, a1=-45)
    c.disc(cx, cy, 3, AMBER if lit > 0 else DIM)


def fmt_int(v):
    return f"{int(v):,}".replace(",", ".")


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    lines = [("¿CÓMO", AMBER), ("FUNCIONA", AMBER), ("EL WIFI?", ORANGE)]
    for k, (txt, col) in enumerate(lines):
        if l < k:
            continue
        p = gfx.ease_out_back((l - k) * 2.5, 2.2)
        y = gfx.lerp(-40, 52 + k * 38, p)
        c.text(txt, 90, y, col, 3, "center")
    lit = max(0, min(3, int(l - 3)))
    glow = math.exp(-(l % 1) * 4) if l >= 4 else 0
    s = gfx.ease_out_back((l - 3) * 2, 1.8) if l >= 3 else 0
    if s > 0:
        c.oy += round((1 - s) * 60)
        wifi_icon(c, 90, 215, lit, glow)
        c.oy -= round((1 - s) * 60)


def s_router(c, l, d, b, h):
    rx, ry = 66, 128
    on = l >= 1
    # cable de internet que entra por abajo
    c.rect(88, 146, 4, 82, DIM)
    c.text("INTERNET", 90, 230, AMBER, 1, "center")
    if on:
        for k in range(6):
            p = (l * 1.2 + k / 6) % 1
            y = 226 - p * 78
            c.rect(87, y, 6, 3, AMBER, a=0.4 + 0.6 * p)
    router(c, rx, ry, b, on)
    if on and l < 8:
        c.text("ROUTER", 90, 92, ORANGE, 2, "center")
    if l >= 8:
        q = l - 8
        for k in range(5):
            r = (q * 16 + k * 13) % 65
            a = max(0.0, 1 - r / 65)
            c.ring(90, 108, r + 4, 3, ORANGE, a=a, a0=-160, a1=-20)
        c.text("ONDAS DE RADIO", 90, 48, AMBER, 2, "center", a=gfx.clamp01(q * 3))


def s_ondas(c, l, d, b, h):
    wl = gfx.lerp(64, 22, gfx.ease_in_out(l / 8))
    ph = b * 2 * math.pi * 0.75
    for x in range(0, 180, 2):
        y = 122 + 24 * math.sin(2 * math.pi * x / wl - ph)
        c.rect(x, y - 2, 2, 4, ORANGE)
    val = 2_400_000_000 * gfx.ease_out_cubic(l / 7)
    col = AMBER if l >= 7 else ORANGE
    c.text(fmt_int(val), 90, 162, col, 2, "center")
    c.text("VIBRACIONES POR SEGUNDO", 90, 186, DIM if l < 7 else ORANGE, 1, "center")
    if l >= 8:
        p = gfx.ease_out_back((l - 8) * 2, 2.5)
        y = gfx.lerp(-50, 48, p)
        c.text("2,4 GHZ", 90, y, AMBER, 4, "center")


BITS = "10110010"


def s_bits(c, l, d, b, h):
    act = int(l) % 8 if l < 8 else int(l * 2) % 8
    for i, ch in enumerate(BITS):
        x = 10 + i * 20
        on = i == act
        c.box(x + 1, 52, 18, 26, ORANGE if on else PANEL, AMBER if on else DIM)
        c.text(ch, x + 10, 54, BG if on else AMBER, 2, "center", shadow=not on)
    ph = b * 2 * math.pi
    for x in range(10, 170):
        i = (x - 10) // 20
        amp = 26 if BITS[i] == "1" else 8
        y = 140 + amp * math.sin(2 * math.pi * x / 20 - ph)
        col = AMBER if i == act else (ORANGE if i < act or l >= 8 else DIM)
        c.rect(x, y - 1, 1, 4, col)
    xa = 10 + act * 20 + 10
    for yy in range(82, 110, 4):
        c.rect(xa - 1, yy, 2, 2, AMBER)
    if l >= 8:
        p = gfx.ease_out_back((l - 8) * 2, 2)
        c.oy += round((1 - p) * 40)
        c.text("1 = ONDA ALTA", 90, 182, AMBER, 1, "center")
        c.text("0 = ONDA BAJA", 90, 196, ORANGE, 1, "center")
        c.oy -= round((1 - p) * 40)


def s_paquetes(c, l, d, b, h):
    router(c, 6, 170, b)
    bars = 4 if l >= 2 else int(l * 2)
    phone(c, 138, 120, 34, 64, bars)
    for k in range(1, 14):
        p = l - k
        if 0 <= p < 1:
            e = gfx.ease_in_out(p)
            x = gfx.lerp(76, 152, e)
            y = 160 - math.sin(p * math.pi) * 52
            c.box(x - 17, y - 8, 34, 16, PANEL, AMBER)
            c.text("DATOS", x, y - 5, ORANGE, 1, "center", shadow=False)
            if l >= 6:
                c.box(x - 15, y - 19, 30, 11, RED, RED)
                c.text(">MÓVIL", x, y - 21, HOT, 1, "center", shadow=False)
    if l >= 6:
        p = gfx.ease_out_back((l - 6) * 2, 2)
        c.text("DIRECCIÓN", 90, gfx.lerp(-30, 48, p), AMBER, 2, "center")


def s_movil(c, l, d, b, h):
    px, py, pw, ph_ = 60, 66, 60, 124
    for k in range(5):
        r = (l * 26 + k * 28) % 140
        a = max(0.0, 1 - r / 140) * 0.9
        c.ring(-10, 30, r + 6, 3, ORANGE, a=a, a0=0, a1=90)
    bars = min(4, int(l / 1.5))
    phone(c, px, py, pw, ph_, bars)
    if 1 <= l < 7:
        c.text("ANTENA", 152, 52, AMBER, 1, "center")
        c.line(140, 60, 118, 70, AMBER)
    sx, sy = px + 6, py + 22
    if 7 <= l < 11:
        for row in range(7):
            s = "".join("1" if ((row * 7 + col + int(b * 4)) * 2654435761 >> 7) & 1 else "0" for col in range(7))
            c.text(s, sx + 2, sy + row * 12, AMBER if row % 2 else ORANGE, 1, shadow=False)
    if l >= 11:
        p = gfx.ease_out_back((l - 11) * 2, 2.2)
        c.oy += round((1 - p) * 30)
        c.rect(sx + 2, sy + 6, 44, 50, DARK)
        c.disc(sx + 34, sy + 18, 5, AMBER)
        for i in range(22):
            c.rect(sx + 4 + i, sy + 48 - i, 1, i + 6, ORANGE)
            c.rect(sx + 24 + i // 2, sy + 40 - i // 2, 1, i // 2 + 14, RED)
        c.text("¡LISTO!", 90, sy + 66, AMBER, 1, "center")
        c.oy -= round((1 - p) * 30)


def meter(c, y, label, v, col):
    c.text(label, 10, y, DIM, 1, shadow=False)
    c.rect(70, y + 3, 100, 6, DARK)
    c.rect(70, y + 3, 100 * v, 6, col)


def s_bandas(c, l, d, b, h):
    cx, cy = 34, 150
    if l < 12:
        five = l >= 6
        q = (l - 6) if five else l
        maxr, sp, spd = (78, 10, 40) if five else (150, 24, 18)
        for k in range(10):
            r = (q * spd + k * sp) % maxr
            a = max(0.0, 1 - r / maxr)
            c.ring(cx, cy, r + 8, 3, AMBER if five else ORANGE, a=a, a0=-70, a1=70)
        router(c, 10, 160, b)
        lab = "5 GHZ" if five else "2,4 GHZ"
        p = gfx.ease_out_back(q * 2.5, 2)
        c.text(lab, 90, gfx.lerp(-40, 46, p), AMBER, 3, "center")
        e = gfx.ease_out_cubic(q * 1.5)
        meter(c, 196, "ALCANCE", (0.45 if five else 0.92) * e, ORANGE)
        meter(c, 212, "VELOCIDAD", (0.95 if five else 0.42) * e, AMBER)
    else:
        q = l - 12
        for k in range(7):
            r = (q * 22 + k * 22) % 160
            a = max(0.0, 1 - r / 160)
            c.ring(cx, cy, r + 8, 3, ORANGE, a=a, a0=-70, a1=70)
        router(c, 10, 160, b)
        p = gfx.ease_out_back(q * 2, 2.4)
        wy = gfx.lerp(-140, 70, p)
        c.rect(118, wy, 62, 150, BG, a=0.72)
        for row in range(15):
            off = 0 if row % 2 else 6
            for col in range(2):
                c.box(104 + off + col * 6 - (6 if off else 0), wy + row * 10, 12, 10, PANEL, DIM)
        c.rect(104, wy, 14, 150, PANEL, a=0.0)
        c.text("PARED", 112, wy - 14, AMBER, 1, "center")
        if q >= 2:
            c.text("SEÑAL DÉBIL", 150, 112, RED, 1, "center")


def s_record(c, l, d, b, h):
    p = gfx.ease_out_back(l * 2, 2.2)
    c.text("WIFI 7", 90, gfx.lerp(-40, 40, p), AMBER, 3, "center")
    gx, gy, r = 90, 160, 56
    c.ring(gx, gy, r, 5, DARK, a0=-180, a1=0)
    v = 46 * gfx.ease_out_back(gfx.clamp01((l - 1) / 4), 1.3)
    ang = -180 + 180 * min(v, 50) / 50
    c.ring(gx, gy, r, 5, ORANGE, a0=-180, a1=ang)
    for k in range(11):
        a_ = math.radians(-180 + k * 18)
        c.rect(gx + math.cos(a_) * (r - 6), gy + math.sin(a_) * (r - 6), 2, 2, DIM)
    na = math.radians(ang)
    c.line(gx, gy, gx + math.cos(na) * 46, gy + math.sin(na) * 46, AMBER, t=2)
    c.disc(gx, gy, 4, AMBER)
    c.text(str(int(round(min(max(v, 0), 46)))), 90, 166, AMBER if l >= 5 else ORANGE, 4, "center")
    c.text("GBPS", 90, 208, ORANGE, 2, "center")
    if l >= 8 and int(b * 2) % 2 == 0:
        c.text("*TEÓRICO", 90, 76, RED, 2, "center")


COVER_LINES = ["¿CÓMO", "FUNCIONA", "EL WIFI?"]


def cover_art(c, y):
    cx, cy = 90, y + 66
    for k in range(4):
        c.ring(cx, cy, 10 + k * 13, 7, AMBER if k < 3 else ORANGE, a0=-135, a1=-45)
    c.disc(cx, cy, 6, AMBER)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 ROUTER", s_router, True),
    (24, 38, "2 ONDAS", s_ondas, False),
    (38, 52, "3 BITS", s_bits, False),
    (52, 66, "4 PAQUETES", s_paquetes, True),
    (66, 80, "5 MÓVIL", s_movil, False),
    (80, 100, "6 BANDAS", s_bandas, True),
    (100, 116, "7 RÉCORD", s_record, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = [
    (8, "TU ROUTER RECIBE", 1), (11, "INTERNET POR CABLE", 1),
    (16, "Y LO CONVIERTE", 1), (19, "EN ONDAS DE RADIO", 1),
    (24, "VIBRAN 2.400", 1), (26, "MILLONES DE VECES", 1), (29, "POR SEGUNDO", 1),
    (32, "¡ESO ES 2,4 GHZ!", 1),
    (38, "EL ROUTER CAMBIA", 1), (41, "LA FORMA DE LA ONDA", 1),
    (46, "PARA LLEVAR", 1), (48, "UNOS Y CEROS", 1),
    (52, "LOS DATOS VIAJAN", 1), (55, "EN PAQUETES", 1),
    (58, "CON LA DIRECCIÓN", 1), (61, "DE TU MÓVIL", 1),
    (66, "TU MÓVIL LOS CAPTA", 1), (70, "CON SU ANTENA", 1),
    (73, "Y LOS VUELVE", 1), (76, "A CONVERTIR EN BITS", 1),
    (80, "2,4 GHZ:", 1), (82, "LLEGA MÁS LEJOS", 1),
    (86, "5 GHZ:", 1), (88, "VA MÁS RÁPIDO", 1),
    (92, "LAS PAREDES", 1), (94, "DEBILITAN LA SEÑAL", 1),
    (100, "WIFI 7: HASTA", 1), (103, "46 GIGABITS", 1), (105, "POR SEGUNDO", 1),
    (108, "(MÁXIMO TEÓRICO)", 1),
]

SFX = (
    [(0, "blip_up"), (1, "blip_up"), (2, "blip_up"), (3, "power_up"),
     (4, "ding"), (5, "ding"), (6, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(9, "power_up")] + [(b, "bits") for b in (10, 12, 14)]
    + [(16, "sweep_up"), (18, "ping"), (20, "ping"), (22, "ping")]
    + [(24 + k, "tick") for k in range(1, 8)] + [(32, "power_up")]
    + [(38 + k, "bit1" if BITS[k] == "1" else "bit0") for k in range(1, 8)]
    + [(46, "bits"), (48, "bits"), (50, "blip")]
    + [(52 + k, "send") for k in range(1, 14)] + [(58, "blip_up")]
    + [(67, "ping"), (69, "ping"), (71, "ping"), (73, "bits"), (75, "bits"), (77, "power_up")]
    + [(81, "sweep_up"), (86, "sweep_fast"), (87, "sweep_fast"), (92, "thud"), (94, "power_down"), (96, "power_down")]
    + [(101, "sweep_up"), (105, "power_up"), (108, "error")]
    + outro_sfx(116)
)
