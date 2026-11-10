"""Tema: ¿Por qué los gatos caen de pie? (animales)

Datos verificados (10-nov-2026; Wikipedia «Cat righting reflex», Mental Floss, Excélsior, Billiken,
Univision, Petscare):
- Reflejo de enderezamiento: el oído interno (sistema vestibular) le dice al gato dónde está arriba.
- Dobla el cuerpo y gira por mitades: primero la parte de delante (con las patas delanteras
  recogidas para girar más rápido) y después la de atrás. Así gira sin apoyarse en nada, sin
  romper la conservación del momento angular. La columna es muy flexible.
- Aparece a las 3-4 semanas de vida y se perfecciona hacia las 7 semanas.
- 1894: Étienne-Jules Marey fotografió a un gato cayendo (cronofotografía) y la Academia de
  Ciencias de París debatió cómo podía girar sin apoyo.
- Velocidad límite de un gato: ~97 km/h (60 mph), «unos cien por hora»; en caídas largas abre las
  patas y el cuerpo como un paracaídas.
- Aterriza con las patas dobladas para amortiguar el golpe.
- No son invencibles: los veterinarios hablan de «síndrome de gran altura» (caídas desde ventanas y
  balcones); no hay ninguna altura totalmente segura.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT

TITLE = "¿Por qué los gatos caen de pie?"
MUSIC_SEED = 20261110
MUSIC_KEY = 57
BOARD_SEED = 99


def cat(c, cx, cy, af, ab, s=1.0, col=ORANGE, spread=0.0, tuck=0.0, bend=0.0):
    """Gato visto de lado. af/ab: giro de la mitad delantera/trasera alrededor del eje del cuerpo
    (0 = patas abajo, pi = patas arriba). spread abre las patas (paracaídas); tuck las recoge;
    bend dobla las patas al aterrizar."""
    df, db = math.cos(af), math.cos(ab)
    # cuerpo (dos mitades) con rayas
    c.disc(cx - 7 * s, cy, 7.5 * s, col)
    c.disc(cx + 6 * s, cy, 7.5 * s, col)
    c.rect(cx - 7 * s, cy - 7 * s, 13 * s, 14 * s, col)
    for k in range(3):
        c.rect(cx - 9 * s + k * 6 * s, cy - 3 * s, max(1, 1.5 * s), 6 * s, DIM)
    # cabeza y orejas
    hy = cy - 3 * s * df
    c.disc(cx + 17 * s, hy, 6 * s, col)
    for ex in (13, 20):
        c.line(cx + ex * s, hy - 3 * s * df, cx + (ex + 1) * s, hy - 10 * s * df, col, t=max(1, int(2 * s)))
    if df > 0.3:
        c.rect(cx + 18 * s, hy - 2 * s, max(1, s), max(1, s), DARK)
        c.rect(cx + 21 * s, hy - 2 * s, max(1, s), max(1, s), DARK)
    elif df < -0.3:
        c.rect(cx + 18 * s, hy + 1 * s, max(1, s), max(1, s), DARK)
    # patas
    lf = 10 * s * (1 - 0.6 * tuck) * (1 - 0.4 * bend)
    for x in (3, 9):
        x0, y0 = cx + x * s, cy + 5 * s * df
        c.line(x0, y0, x0 + spread * 7 * s, y0 + lf * df, col, t=max(1, int(2 * s)))
    lb = 10 * s * (1 - 0.4 * bend)
    for x in (-12, -6):
        x0, y0 = cx + x * s, cy + 5 * s * db
        c.line(x0, y0, x0 - spread * 7 * s, y0 + lb * db, col, t=max(1, int(2 * s)))
    # cola
    c.line(cx - 14 * s, cy, cx - 24 * s, cy - 10 * s * db, col, t=max(1, int(2 * s)))


def ground(c, y=214):
    c.rect(10, y, 160, 3, DIM)
    for k in range(8):
        c.rect(14 + k * 20, y + 5, 8, 1, DARK)


def arrow_up(c, x, y, col=AMBER):
    c.line(x, y + 14, x, y, col, t=2)
    c.line(x - 5, y + 5, x, y, col, t=2)
    c.line(x + 5, y + 5, x, y, col, t=2)


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    if l < 6.2:
        c.text("GIRA EN", 90, 34, AMBER, 3, "center")
        c.text("EL AIRE", 90, 66, AMBER, 3, "center")
        c.text("SIN TOCAR", 90, 98, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("NADA", 90, 128, gfx.mix(RED, HOT, pulse * 0.3), 4, "center")
        c.ox = 0
        cat(c, 92, 196, math.pi * 0.15, math.pi * 0.9, 1.4)
        return
    c.text("¿POR QUÉ", 90, 38, AMBER, 3, "center")
    c.text("LOS GATOS", 90, 70, ORANGE, 3, "center")
    c.text("CAEN", 90, 102, ORANGE, 3, "center")
    c.text("DE PIE?", 90, 134, ORANGE, 3, "center")
    cat(c, 92, 200, 0, 0, 1.4)


T_OIDO = 0.3


def s_oido(c, l, d, b, h):
    y = 70 + gfx.clamp01(l / 14) * 60
    cat(c, 90, y, math.pi, math.pi, 1.5)
    if l >= T_OIDO:
        flash = 0.5 + 0.5 * math.sin(b * 8)
        c.disc(116, y + 2, 4, gfx.mix(AMBER, HOT, flash))
        c.box(18, 160, 144, 36, PANEL, AMBER)
        c.text("OÍDO INTERNO", 90, 166, AMBER, 1, "center")
        c.text("¿DÓNDE ESTÁ EL SUELO?", 90, 180, ORANGE, 1, "center")
    if l >= 4.8:
        arrow_up(c, 24, 40)
        c.text("ARRIBA", 24, 60, AMBER, 1, "center")
    ground(c)


T_FRONT, T_BACK = 2.0, 6.6


def s_mitades(c, l, d, b, h):
    af = math.pi * (1 - gfx.ease_in_out((l - T_FRONT) / 2.5))
    ab = math.pi * (1 - gfx.ease_in_out((l - T_BACK) / 2.5))
    cat(c, 90, 120, af, ab, 1.8, tuck=0.6 if T_FRONT <= l < T_FRONT + 3 else 0.0)
    if l >= T_FRONT:
        c.text("1 DELANTE", 130, 172, AMBER if l < T_BACK else DIM, 1, "center")
    if l >= T_BACK:
        c.text("2 DETRÁS", 50, 172, AMBER, 1, "center")
    if l >= 10:
        c.text("¡GIRA POR MITADES!", 90, 52, RED, 1, "center")


T_TUCK = 1.6


def s_patas(c, l, d, b, h):
    q = gfx.clamp01((l - T_TUCK) / 1.5)
    spin = l * (1.2 + 2.0 * q)
    c.ox = 0
    cat(c, 90, 118, spin, spin, 1.6, tuck=q)
    c.text("RECOGE LAS PATAS", 90, 176, AMBER if q > 0.5 else DIM, 1, "center")
    if l >= 4.6:
        c.text("= GIRA MÁS RÁPIDO", 90, 190, ORANGE, 1, "center")
    if l >= 6.4:
        c.text("COMO UNA PATINADORA", 90, 52, AMBER, 1, "center")


def s_1894(c, l, d, b, h):
    c.text("1894", 90, 40, AMBER, 3, "center")
    n = 5
    for k in range(n):
        st = 3.9 + k * 0.35
        if l < st:
            continue
        x = 20 + k * 35
        c.box(x - 16, 80, 32, 56, PANEL, DIM)
        t = k / (n - 1)
        cat(c, x, 104 + k * 4, math.pi * (1 - min(1, t * 1.6)), math.pi * (1 - t), 0.55)
    if l >= 4.8:
        c.text("FOTOS DE UN GATO", 90, 150, AMBER, 1, "center")
        c.text("CAYENDO", 90, 162, AMBER, 1, "center")
    if l >= 6.5:
        c.text("LA CIENCIA", 90, 186, RED, 2, "center")
        c.text("ALUCINÓ", 90, 204, RED, 2, "center")


T_PARA = 3.2


def s_paracaidas(c, l, d, b, h):
    sp = gfx.ease_out_back((l - T_PARA) * 1.5, 1.6) if l >= T_PARA else 0.0
    for k in range(6):
        y = (k * 40 + l * 60) % 240
        c.rect(20 + k * 28, y, 1, 10, DIM)
    cat(c, 90, 100, 0, 0, 1.6, spread=sp)
    if l >= T_PARA:
        c.text("¡PARACAÍDAS!", 90, 46, AMBER, 2, "center")
    if l >= 6.8:
        c.text("COMO MUCHO, UNOS", 90, 150, ORANGE, 1, "center")
        c.text("100 KM/H", 90, 162, RED, 3, "center")


T_LAND = 1.2


def s_aterriza(c, l, d, b, h):
    ground(c, 190)
    if l < T_LAND:
        y = gfx.lerp(60, 166, gfx.ease_in_cubic(l / T_LAND))
        cat(c, 90, y, 0, 0, 1.6)
    else:
        q = l - T_LAND
        bend = math.exp(-q * 2) * abs(math.cos(q * 6)) if q < 3 else 0
        cat(c, 90, 166 + bend * 5, 0, 0, 1.6, bend=0.3 + bend * 0.7)
        if l >= 1.6:
            c.text("PATAS DOBLADAS", 90, 48, AMBER, 2, "center")
        if l >= 3.8:
            c.text("= MUELLES", 90, 70, ORANGE, 2, "center")


def s_cuidado(c, l, d, b, h):
    c.box(56, 40, 68, 90, PANEL, DIM)
    c.rect(56, 84, 68, 2, DIM)
    c.rect(89, 40, 2, 90, DIM)
    c.rect(50, 128, 80, 4, AMBER)
    cat(c, 90, 118, 0, 0, 0.9)
    if l >= 1.5:
        c.text("NO SON", 90, 146, AMBER, 2, "center")
        c.text("INVENCIBLES", 90, 164, RED, 2, "center")
    if l >= 4.3:
        c.box(18, 192, 144, 30, RED, RED)
        c.text("¡NINGUNA ALTURA", 90, 197, HOT, 1, "center", shadow=False)
        c.text("ES SEGURA!", 90, 209, HOT, 1, "center", shadow=False)


COVER_LINES = ["¿POR QUÉ", "CAEN", "DE PIE?"]


def cover_art(c, y):
    cat(c, 92, y + 34, 0, 0, 2.0)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 EL OÍDO", s_oido, False),
    (24, 38, "2 POR MITADES", s_mitades, False),
    (38, 52, "3 LAS PATAS", s_patas, True),
    (52, 66, "4 EN 1894", s_1894, False),
    (66, 80, "5 PARACAÍDAS", s_paracaidas, True),
    (80, 100, "6 ATERRIZAJE", s_aterriza, False),
    (100, 116, "7 ¡OJO!", s_cuidado, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = []   # con voz se generan solos

VOICE = [
    (0, "[intrigado] Un gato gira en el aire… ¡sin apoyarse en nada!"),
    (8, "[narrando] Su oído interno le dice al instante dónde está el suelo."),
    (24, "[asombrado] Dobla el cuerpo y gira primero la mitad de delante… y luego la de atrás."),
    (38, "[cómplice] El truco: recoge las patas para girar más rápido, como una patinadora."),
    (52, "[misterioso] En mil ochocientos noventa y cuatro, estas fotos dejaron a la ciencia alucinada."),
    (66, "[enérgico] En caídas largas se abre como un paracaídas: no pasa de unos cien por hora."),
    (80, "[sereno] Y aterriza con las patas dobladas, como muelles, para amortiguar el golpe."),
    (100, "[serio] Pero ojo: no son invencibles. Ninguna altura es segura para un gato."),
    (116, "[alegre] ¡Sígueme para más datos curiosos!"),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3, "blip"), (4.5, "whoosh"), (4.7, "blip_up"), (5.5, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(8 + T_OIDO, "ping"), (12.8, "blip_up")]
    + [(24 + T_FRONT, "sweep_up"), (24 + T_BACK, "sweep_up"), (32.5, "ding")]
    + [(38 + T_TUCK, "sweep_fast"), (42.6, "ding")]
    + [(55.9 + k * 0.35, "tick") for k in range(5)] + [(58.5, "ding")]
    + [(66 + T_PARA, "power_up"), (72.9, "ding")]
    + [(80 + T_LAND, "thud"), (83.8, "blip_up")]
    + [(101.5, "error"), (104.3, "ping")]
    + outro_sfx(116)
)
