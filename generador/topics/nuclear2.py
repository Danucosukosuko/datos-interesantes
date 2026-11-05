"""Tema: Central nuclear, PARTE 2 — ¿Cómo funciona una central nuclear? (parte 1 en topics/nuclear1.py)

Datos verificados (5-nov-2026):
- El calor de la fisión del uranio calienta agua. El agua además frena (modera) los neutrones para
  que sigan partiendo núcleos de U-235.
- Las barras de control (boro, cadmio o hafnio) absorben neutrones: al meterlas, la reacción se
  frena; al sacarlas, se acelera.
- Ese calor produce vapor, el vapor mueve una turbina y la turbina un generador eléctrico (igual
  que una central térmica, pero sin quemar nada).
- Lo que sale de las torres de refrigeración es vapor de agua, no humo: no hay combustión (Maldita,
  Foro Nuclear).
- España: 7 reactores (Almaraz I y II, Ascó I y II, Cofrentes, Trillo, Vandellós II) produjeron
  algo más del 19 % de la electricidad en 2025 (Foro Nuclear / REE).
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT, BG
from topics.nuclear1 import nucleus, neutron, tower, plume

TITLE = "¿Cómo funciona una central nuclear? (Parte 2)"
MUSIC_SEED = 20261106
MUSIC_KEY = 52
BOARD_SEED = 77


def vessel(c, x, y, w, h, heat=0.5, rods_in=0.0, b=0.0):
    c.box(x, y, w, h, DARK, ORANGE, t=2)
    for k in range(int(w / 6)):
        yy = y + 8 + (k * 11 + int(b * 8)) % (h - 12)
        c.rect(x + 4 + k * 6, yy, 3, 1, DIM)
    n = 5
    for k in range(n):
        rx = x + 8 + k * (w - 16) / (n - 1) - 3
        c.rect(rx, y + 14, 6, h - 22, gfx.mix(ORANGE, HOT, heat * (0.6 + 0.4 * math.sin(b * 6 + k))))
    for k in range(n - 1):
        rx = x + 8 + (k + 0.5) * (w - 16) / (n - 1) - 2
        c.rect(rx, y - 30 + rods_in * (h - 10), 4, 40, DIM)
        c.rect(rx, y - 30 + rods_in * (h - 10), 4, 3, RED)


def turbine(c, cx, cy, r, ang):
    c.ring(cx, cy, r, 2, ORANGE, a0=-180, a1=180)
    for k in range(6):
        a = ang + k * math.pi / 3
        c.line(cx, cy, cx + math.cos(a) * (r - 3), cy + math.sin(a) * (r - 3), AMBER, t=2)
    c.disc(cx, cy, 3, AMBER)


BOLT = ["..##", ".##.", "####", ".##.", "##..", "#..."]


def s_title(c, l, d, b, h):
    if l < 5:
        pulse = math.exp(-(b % 1) * 5)
        c.text("LA NUCLEAR", 90, 40, AMBER, 3, "center")
        c.text("SOLO", 90, 74, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("HIERVE", 90, 106, gfx.mix(RED, HOT, pulse * 0.3), 4, "center")
        c.text("AGUA", 90, 142, gfx.mix(RED, HOT, pulse * 0.3), 4, "center")
        c.ox = 0
        tower(c, 90, 236, 50, 40)
        plume(c, 90, 186, b, 5)
        return
    c.box(44, 30, 92, 20, RED, RED)
    c.text("PARTE 2", 90, 33, HOT, 2, "center", shadow=False)
    c.text("¿CÓMO", 90, 64, AMBER, 3, "center")
    c.text("FUNCIONA?", 90, 98, ORANGE, 3, "center")
    tower(c, 90, 236, 60, 46)
    plume(c, 90, 176, b, 6)


def s_nucleo(c, l, d, b, h):
    vessel(c, 40, 70, 100, 130, heat=gfx.clamp01(l / 6), rods_in=0.0, b=b)
    c.text("NÚCLEO DEL REACTOR", 90, 210, ORANGE, 1, "center")
    if l >= 0.4:
        c.text("BARRAS DE URANIO", 90, 224, AMBER, 1, "center")


def s_frenos(c, l, d, b, h):
    ins = gfx.ease_in_out((l - 1.8) / 3) * 0.8 if l < 9 else 0.8 - gfx.ease_in_out((l - 9) / 3) * 0.5
    vessel(c, 40, 70, 100, 130, heat=1 - ins * 0.9, rods_in=ins, b=b)
    c.text("BARRAS DE CONTROL", 90, 210, RED, 1, "center")
    if l >= 2:
        c.text("SE TRAGAN NEUTRONES", 90, 224, AMBER, 1, "center")


def s_agua(c, l, d, b, h):
    c.box(20, 60, 140, 140, DARK, ORANGE, t=2)
    for k in range(9):
        yy = 66 + (k * 15 + int(b * 10)) % 130
        c.rect(26 + (k % 3) * 40, yy, 20, 2, ORANGE, a=0.5)
    for k in range(4):
        f = ((l * 0.4) + k / 4) % 1
        x = 24 + f * 132
        sp = 1 - f
        neutron(c, x, 90 + k * 25, gfx.mix(AMBER, HOT, sp))
        c.rect(x - 10 * sp - 2, 89 + k * 25, 10 * sp, 2, HOT, a=0.5)
    nucleus(c, 150, 130, 10, seed=4)
    c.text("EL AGUA FRENA", 90, 210, AMBER, 1, "center")
    if l >= 4:
        heat = gfx.clamp01((l - 4) / 4)
        c.rect(20, 60, 140, 140, RED, a=0.25 * heat)
        c.text("Y SE CALIENTA", 90, 222, RED, 1, "center")


def s_vapor(c, l, d, b, h):
    c.box(14, 120, 50, 80, DARK, ORANGE, t=2)
    c.rect(18, 160, 42, 36, RED, a=0.4)
    c.text("REACTOR", 39, 206, ORANGE, 1, "center")
    c.rect(64, 128, 70, 6, PANEL)
    c.rect(130, 70, 6, 64, PANEL)
    for k in range(6):
        f = ((l * 0.6) + k / 6) % 1
        if f < 0.5:
            x, y = 64 + f * 2 * 70, 131
        else:
            x, y = 133, 131 - (f - 0.5) * 2 * 60
        c.disc(x, y, 3, HOT, a=0.8)
    c.text("VAPOR", 100, 112, AMBER, 2, "center")
    if l >= 3.3:
        c.text("A TODA PRESIÓN", 90, 48, RED, 2, "center")


def s_turbina(c, l, d, b, h):
    spin = b * (1 + gfx.clamp01(l / 4) * 3)
    turbine(c, 54, 120, 30, spin)
    c.rect(84, 118, 22, 4, DIM)
    c.box(106, 104, 40, 32, PANEL, AMBER)
    c.text("GEN.", 126, 115, AMBER, 1, "center", shadow=False)
    c.text("TURBINA", 54, 160, ORANGE, 1, "center")
    if l >= 6.9:
        c.sprite(BOLT, 150, 70, {"#": AMBER}, 4)
        c.text("¡ELECTRICIDAD!", 90, 196, AMBER, 2, "center")


def s_torres(c, l, d, b, h):
    tower(c, 60, 216, 100, 60)
    tower(c, 132, 216, 84, 50)
    plume(c, 60, 116, b, 8)
    plume(c, 132, 132, b + 1.3, 6)
    if l >= 4:
        c.box(18, 46, 144, 40, PANEL, AMBER)
        c.text("NO ES HUMO:", 90, 50, RED, 2, "center")
        c.text("ES VAPOR DE AGUA", 90, 70, AMBER, 1, "center")
    if l >= 12:
        c.text("NO SE QUEMA NADA", 90, 224, ORANGE, 1, "center")


def s_espana(c, l, d, b, h):
    p = gfx.ease_out_back(l * 1.5, 2)
    c.text("ESPAÑA", 90, gfx.lerp(-30, 46, p), ORANGE, 2, "center")
    for k in range(7):
        x = 24 + k * 22
        lit = l >= 1 + k * 0.4
        c.disc(x, 92, 7, AMBER if lit else DIM)
    c.text("7 REACTORES", 90, 108, AMBER, 1, "center")
    if l >= 4:
        q = gfx.ease_out_cubic((l - 4) / 2)
        c.text(f"{int(19 * q)} %", 90, 136, AMBER, 4, "center")
        c.text("DE LA ELECTRICIDAD", 90, 174, ORANGE, 1, "center")
        c.text("(2025)", 90, 186, DIM, 1, "center")


COVER_LINES = ["CENTRAL", "NUCLEAR"]


def cover_art(c, y):
    c.box(44, y - 2, 92, 20, RED, RED)
    c.text("PARTE 2", 90, y + 1, HOT, 2, "center", shadow=False)
    tower(c, 70, y + 104, 72, 50)
    tower(c, 124, y + 104, 58, 40)
    for k in range(5):
        c.disc(70 + math.sin(k) * 6, y + 26 - k * 3, 9 + k * 2, DIM, a=0.6 - k * 0.1)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 EL NÚCLEO", s_nucleo, False),
    (24, 38, "2 FRENOS", s_frenos, False),
    (38, 52, "3 AGUA", s_agua, True),
    (52, 66, "4 VAPOR", s_vapor, True),
    (66, 80, "5 TURBINA", s_turbina, True),
    (80, 100, "6 LAS TORRES", s_torres, False),
    (100, 116, "7 EN ESPAÑA", s_espana, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = []   # con voz se generan solos

VOICE = [
    (0, "[intrigado] Una central nuclear… ¡solo hierve agua!"),
    (8, "[narrando] Las barras de uranio se calientan con la reacción en cadena."),
    (24, "[cómplice] Para frenarla, se meten barras de control que se tragan neutrones."),
    (38, "El agua frena los neutrones… y se calienta muchísimo."),
    (52, "[enérgico] Ese calor hace vapor, que sale a toda presión."),
    (66, "El vapor mueve una turbina, y la turbina un generador: ¡electricidad!"),
    (80, "[sorprendido] ¿Y esas nubes de las torres? No es humo… es vapor de agua."),
    (100, "[sereno] En España, siete reactores dan casi el veinte por ciento de la luz."),
    (116, "[alegre] ¡Sígueme para más datos curiosos!"),
]

SFX = (
    [(0, "power_up"), (1, "error"), (2, "error"), (3, "error"), (4, "whoosh"), (4.2, "blip_up"), (5, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(9, "power_up"), (11, "bits"), (14, "ping")]
    + [(25, "power_down"), (29, "power_down"), (33, "power_up")]
    + [(39, "sweep_fast"), (42, "sweep_up"), (46, "power_up")]
    + [(53, "sweep_up"), (55.3, "power_up")]
    + [(67, "sweep_up"), (68, "power_up"), (72.9, "ding")]
    + [(84, "ping"), (88, "ding")]
    + [(101, "blip_up"), (102, "blip_up"), (103, "blip_up"), (104, "power_up"), (106, "ding")]
    + outro_sfx(116)
)
