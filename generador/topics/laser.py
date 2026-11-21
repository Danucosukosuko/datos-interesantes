"""Tema: ¿Cómo funciona un medidor láser de distancia? (tecnología) — encargado por Pablo el 21-nov.

Datos verificados (21-nov-2026; fichas Bosch UniversalDistance 50 / GLM 150-27 C, Leica DISTO D1,
patentes de medidores láser de mano (USPTO 7456936, 7324218), Constructivo rc117):
- Emite un haz láser rojo (diodo de 635-650 nm, clase 2, < 1 mW) que se refleja en el objetivo y
  vuelve al aparato; un receptor lo capta.
- La luz va a ~300.000 km/s: recorre unos 30 cm en una milmillonésima de segundo (1 ns). Para medir
  1 mm habría que cronometrar unas 7 billonésimas de segundo (2 mm / c ≈ 6,7 ps).
- Por eso la mayoría de medidores de mano no cronometran un pulso: modulan la intensidad del haz (lo
  hacen «vibrar») y comparan la fase de la onda que vuelve con la que sale (medición por desfase).
- Usan varias frecuencias de modulación para saber cuántas ondas completas caben (resolver la
  ambigüedad).
- Distancia = (recorrido de ida y vuelta) / 2. Precisión típica ±1,5 a ±2 mm; alcance 40-50 m en
  modelos de casa.
- Funciones: área (largo × ancho = m²), volumen (m³) y medición indirecta con Pitágoras.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT

TITLE = "¿Cómo funciona un medidor láser de distancia?"
MUSIC_SEED = 20261122
MUSIC_KEY = 55
BOARD_SEED = 221


def meter(c, x, y, s=1.0, reading=None, on=False, b=0.0):
    """Medidor láser de mano visto de lado: cuerpo, pantalla y botones; el láser sale por la derecha."""
    w, h = 34 * s, 62 * s
    c.box(x, y, w, h, PANEL, ORANGE, t=max(1, int(2 * s)))
    c.box(x + 4 * s, y + 6 * s, w - 8 * s, 16 * s, DARK, AMBER)
    if reading:
        c.text(reading, x + w / 2, y + 10 * s, AMBER, 1, "center", shadow=False)
    c.disc(x + w / 2, y + 36 * s, 6 * s, RED if on else DIM)
    for k in range(2):
        c.rect(x + 7 * s + k * 13 * s, y + 48 * s, 8 * s, 5 * s, DIM)
    c.rect(x + w, y + 10 * s, 3 * s, 6 * s, RED if on else DIM)


def wall(c, x, y0=40, y1=220):
    c.rect(x, y0, 12, y1 - y0, PANEL)
    for k in range(int((y1 - y0) / 12)):
        off = 0 if k % 2 == 0 else 6
        c.rect(x, y0 + k * 12, 12, 1, DIM)
        c.rect(x + off, y0 + k * 12, 1, 12, DIM)


def beam(c, x0, x1, y, t=1.0, col=RED):
    if x1 > x0:
        c.rect(x0, y, (x1 - x0) * t, 2, col)
        c.rect(x0, y - 1, (x1 - x0) * t, 4, col, a=0.25)


def sine(c, x0, x1, y, amp, wl, phase, col=AMBER):
    prev = None
    for x in range(int(x0), int(x1)):
        yy = y + math.sin((x - x0) / wl * 2 * math.pi + phase) * amp
        if prev is not None:
            c.line(x - 1, prev, x, yy, col)
        prev = yy


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    if l < 6.2:
        c.text("MIDE", 90, 30, AMBER, 4, "center")
        c.text("CON LA", 90, 68, AMBER, 3, "center")
        c.text("VELOCIDAD", 90, 100, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("DE LA LUZ", 90, 132, gfx.mix(RED, HOT, pulse * 0.3), 3, "center")
        c.ox = 0
        meter(c, 18, 166, 0.9, "4,25", on=True)
        beam(c, 52, 160, 176)
        wall(c, 160, 160, 220)
        c.disc(160, 177, 3, HOT)
        return
    c.text("¿CÓMO FUNCIONA", 90, 44, AMBER, 2, "center")
    c.text("UN MEDIDOR", 90, 68, ORANGE, 2, "center")
    c.text("LÁSER?", 90, 92, RED, 3, "center")
    meter(c, 18, 150, 1.0, "4,25", on=True)
    beam(c, 56, 160, 162)
    wall(c, 160, 130, 220)


T_PULSA, T_REBOTA = 1.6, 4.8


def s_disparo(c, l, d, b, h):
    on = l >= T_PULSA
    meter(c, 14, 90, 1.0, None, on=on)
    wall(c, 158)
    if on:
        t = gfx.clamp01((l - T_PULSA) / 1.2)
        beam(c, 51, 158, 102, t)
        c.text("DIODO LÁSER ROJO", 90, 44, RED, 1, "center")
    if l >= T_REBOTA:
        c.disc(158, 103, 3 + math.sin(b * 8), HOT)
        q = ((l - T_REBOTA) * 0.8) % 1
        c.rect(158 - q * 106, 112, 8, 2, AMBER, a=0.8)
        c.text("REBOTA Y VUELVE", 90, 176, AMBER, 2, "center")


T_30CM, T_NS = 2.0, 4.6


def s_rapido(c, l, d, b, h):
    c.text("300.000 KM/S", 90, 44, RED, 2, "center")
    if l >= T_30CM:
        c.rect(30, 100, 120, 6, PANEL)
        q = gfx.clamp01((l - T_30CM) / 1.5)
        c.rect(30, 100, 120 * q, 6, RED)
        c.text("30 CM", 90, 112, AMBER, 2, "center")
    if l >= T_NS:
        c.text("EN UNA", 90, 146, AMBER, 1, "center")
        c.text("MILMILLONÉSIMA", 90, 158, ORANGE, 2, "center")
        c.text("DE SEGUNDO", 90, 178, AMBER, 1, "center")


T_VIBRA, T_COMPARA = 2.6, 7.6


def s_truco(c, l, d, b, h):
    c.text("EL TRUCO", 90, 40, AMBER, 2, "center")
    if l >= T_VIBRA:
        c.text("SALE", 18, 74, AMBER, 1, "left")
        sine(c, 18, 162, 96, 10, 40, -b * 4, AMBER)
    if l >= T_COMPARA:
        c.text("VUELVE", 18, 122, ORANGE, 1, "left")
        sine(c, 18, 162, 144, 10, 40, -b * 4 + 1.6, ORANGE)
        x = 18 + 40 - (1.6 / (2 * math.pi)) * 40
        c.line(58, 80, 58, 160, DIM)
        c.line(x, 80, x, 160, DIM)
        c.text("DESFASE", 90, 172, RED, 2, "center")


T_ONDAS = 0.3


def s_ondas(c, l, d, b, h):
    meter(c, 4, 70, 0.7)
    wall(c, 164, 40, 200)
    for k, wl in enumerate((60, 30, 12)):
        if l >= T_ONDAS + k * 0.7:
            sine(c, 30, 164, 92 + k * 34, 7, wl, 0, (AMBER, ORANGE, RED)[k])
    if l >= 5:
        c.text("¿CUÁNTAS CABEN?", 90, 40, AMBER, 2, "center")
    if l >= 7.2:
        c.text("¡LO SABE AL MM!", 90, 196, RED, 2, "center")


T_DIV, T_MM = 0.5, 5.4


def s_calculo(c, l, d, b, h):
    if l >= T_DIV:
        c.text("IDA + VUELTA", 90, 52, AMBER, 2, "center")
        c.text("/ 2", 90, 76, RED, 3, "center")
    meter(c, 64, 108, 1.5, "4,253 M" if l >= 3 else "...", on=True)
    if l >= T_MM:
        c.text("+/- 2 MM", 90, 210, RED, 2, "center")


T_LARGO, T_ANCHO, T_MULT = 3.0, 5.0, 7.6


def s_area(c, l, d, b, h):
    x0, y0, w, hh = 30, 60, 120, 80
    c.box(x0, y0, w, hh, DARK, ORANGE, t=2)
    if l >= T_LARGO:
        q = gfx.clamp01((l - T_LARGO) / 1.2)
        beam(c, x0, x0 + w, y0 + hh + 8, q)
        c.text("4 M", x0 + w / 2, y0 + hh + 14, AMBER, 1, "center")
    if l >= T_ANCHO:
        q = gfx.clamp01((l - T_ANCHO) / 1.2)
        c.rect(x0 - 10, y0, 2, hh * q, RED)
        c.text("3 M", x0 - 12, y0 + hh / 2, AMBER, 1, "right")
    if l >= T_MULT:
        c.rect(x0 + 2, y0 + 2, w - 4, hh - 4, AMBER, a=0.25)
        c.text("12 M2", x0 + w / 2, y0 + hh / 2 - 7, RED, 3, "center")
        c.text("4 X 3 = 12 METROS CUADRADOS", 90, 186, AMBER, 1, "center")


T_TRI, T_ALTO = 0.6, 3.4


def s_pitagoras(c, l, d, b, h):
    c.rect(130, 50, 12, 160, PANEL)
    meter(c, 20, 168, 0.6, None, on=True)
    if l >= T_TRI:
        q = gfx.clamp01((l - T_TRI) / 1.0)
        c.line(42, 176, 42 + (130 - 42) * q, 176 - (176 - 70) * q, RED, t=2)
        beam(c, 42, 130, 190, 1.0)
    if l >= T_ALTO:
        c.line(128, 70, 128, 190, AMBER, t=2)
        c.text("¡ALTURA SIN SUBIR!", 90, 202, AMBER, 1, "center")
        pass
    if l >= 0.5:
        c.text("PITÁGORAS", 90, 40, RED, 2, "center")


COVER_LINES = ["¿CÓMO", "MIDE CON", "UN LÁSER?"]


def cover_art(c, y):
    meter(c, 14, y + 4, 1.1, "4,25", on=True)
    beam(c, 54, 160, y + 16)
    wall(c, 160, y - 4, y + 70)
    c.disc(160, y + 17, 3, HOT)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 EL DISPARO", s_disparo, False),
    (24, 38, "2 LA LUZ", s_rapido, False),
    (38, 52, "3 EL TRUCO", s_truco, True),
    (52, 66, "4 VARIAS ONDAS", s_ondas, True),
    (66, 80, "5 EL CÁLCULO", s_calculo, False),
    (80, 100, "6 EN M2", s_area, False),
    (100, 116, "7 PITÁGORAS", s_pitagoras, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = []   # con voz se generan solos

VOICE = [
    (0, "[intrigado] Este medidor láser mide… ¡con la velocidad de la luz!"),
    (8, "[narrando] Al pulsar, lanza un rayo láser rojo que rebota en la pared y vuelve."),
    (24, "[asombrado] La luz recorre treinta centímetros en una milmillonésima de segundo."),
    (38, "[cómplice] El truco: hace vibrar la luz y compara la onda que sale con la que vuelve."),
    (52, "[pensativo] Con varias ondas distintas, sabe exactamente cuántas caben hasta la pared."),
    (66, "[enérgico] Divide entre dos, por la ida y la vuelta… ¡y acierta al milímetro!"),
    (80, "[cómplice] ¿Metros cuadrados? Mide el largo, mide el ancho… y los multiplica."),
    (100, "[sorprendido] Y con Pitágoras, hasta calcula alturas a las que no llegas."),
    (116, "[alegre] ¡Sígueme para más datos curiosos!"),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3, "blip"), (4.4, "whoosh"), (4.6, "blip_up"), (5.4, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(8 + T_PULSA, "power_up"), (8 + T_REBOTA, "ping")]
    + [(24.5, "sweep_fast"), (24 + T_30CM, "sweep_up"), (24 + T_NS, "ding")]
    + [(38 + T_VIBRA, "sweep_up"), (38 + T_COMPARA, "ping"), (46.5, "ding")]
    + [(52 + T_ONDAS + k * 0.7, "blip_up") for k in range(3)] + [(57, "ping"), (59.2, "ding")]
    + [(66 + T_DIV, "blip"), (68.8, "bits"), (66 + T_MM, "ding")]
    + [(80 + T_LARGO, "sweep_fast"), (80 + T_ANCHO, "sweep_fast"), (80 + T_MULT, "ding")]
    + [(100 + T_TRI, "sweep_up"), (100 + T_ALTO, "ping")]
    + outro_sfx(116)
)
