"""Tema: ¿Por qué la Luna tiene fases? (espacio) — vídeo especial de Pablo, 11-nov-2026, en las dos redes.

Datos verificados (11-nov-2026; Starwalk, Moongiant, SpaceWeatherLive, iCalendario):
- La Luna no tiene luz propia: refleja la del Sol. Siempre tiene media cara iluminada (la que mira
  al Sol).
- Al dar la vuelta a la Tierra cambia el ángulo Sol-Tierra-Luna y desde aquí vemos una parte
  distinta de esa mitad iluminada. Ciclo completo de fases (mes sinódico): ~29,5 días.
- Las fases NO son la sombra de la Tierra: la sombra de la Tierra solo cae sobre la Luna en los
  eclipses de Luna (y siempre en luna llena).
- «La Luna es mentirosa» (hemisferio norte): cuando forma una C está decreciendo (menguante) y
  cuando forma una D está creciendo.
- Noviembre 2026: luna nueva el 9-nov; el 11-nov está creciente; cuarto creciente el 17-nov;
  luna llena el 24-nov, y es superluna («Superluna del Castor»).
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT

TITLE = "¿Por qué la Luna tiene fases?"
MUSIC_SEED = 20261111
MUSIC_KEY = 60
BOARD_SEED = 111

CRATERS = [(-0.35, -0.3, 0.18), (0.3, 0.1, 0.22), (-0.1, 0.45, 0.14), (0.15, -0.5, 0.1), (-0.5, 0.2, 0.1)]


def moon(c, cx, cy, r, phase, lit=AMBER, glow=0.0):
    """Luna vista desde la Tierra. phase: 0 nueva, 0.25 cuarto creciente (luz a la derecha),
    0.5 llena, 0.75 cuarto menguante (luz a la izquierda), 1 nueva."""
    phase %= 1.0
    c.disc(cx, cy, r, DARK)
    col = gfx.mix(lit, HOT, glow)
    k = math.cos(2 * math.pi * phase)
    for i in range(int(-r), int(r) + 1):
        w = math.sqrt(max(0.0, r * r - i * i))
        if w <= 0:
            continue
        if phase <= 0.5:
            x0, x1 = w * k, w            # creciente: luz a la derecha
        else:
            x0, x1 = -w, -w * k          # menguante: luz a la izquierda
        if x1 > x0:
            c.rect(cx + x0, cy + i, x1 - x0, 1, col)
    for (dx, dy, rr) in CRATERS:
        x, y = cx + dx * r, cy + dy * r
        w = math.sqrt(max(0.0, r * r - (dy * r) ** 2))
        lit_here = (dx * r >= w * k) if phase <= 0.5 else (dx * r <= -w * k)
        if lit_here and rr * r >= 1:
            c.disc(x, y, rr * r, gfx.mix(col, DIM, 0.45))
    c.ring(cx, cy, r, 1, DIM, a0=-180, a1=180)


def half_moon_toward(c, x, y, r, sx):
    """Luna vista desde arriba: la mitad que mira al Sol (a la izquierda, x=sx) iluminada."""
    c.disc(x, y, r, DARK)
    for i in range(int(-r), int(r) + 1):
        w = math.sqrt(max(0.0, r * r - i * i))
        if sx < x:
            c.rect(x - w, y + i, w, 1, AMBER)
        else:
            c.rect(x, y + i, w, 1, AMBER)
    c.ring(x, y, r, 1, DIM, a0=-180, a1=180)


def sun_rays(c, x, b, n=7, y0=60, y1=220):
    """Sol asomando por el borde izquierdo y rayos de luz hacia la derecha."""
    cy = (y0 + y1) / 2
    c.disc(-6, cy, 24, AMBER)
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 9
        c.line(-6 + math.cos(a) * 27, cy + math.sin(a) * 27, -6 + math.cos(a) * 33, cy + math.sin(a) * 33, AMBER)
    c.text("SOL", 8, cy - 4, DARK, 1, "center", shadow=False)
    for k in range(n):
        y = y0 + k * (y1 - y0) / (n - 1)
        f = (b * 0.5 + k * 0.13) % 1
        c.rect(30 + f * 120, y, 10, 1, AMBER, a=0.6 * (1 - f))


def earth(c, x, y, r):
    c.disc(x, y, r, ORANGE)
    c.disc(x - r * 0.3, y - r * 0.2, r * 0.35, DIM)
    c.disc(x + r * 0.35, y + r * 0.3, r * 0.25, DIM)
    c.ring(x, y, r, 1, AMBER, a0=-180, a1=180)


def stars(c, b):
    for k in range(18):
        x = (k * 53) % 176 + 2
        y = (k * 97) % 210 + 34
        tw = 0.5 + 0.5 * math.sin(b * 2 + k)
        c.rect(x, y, 1, 1, DIM if tw < 0.6 else AMBER)


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    stars(c, b)
    if l < 6.1:
        c.text("NO ES LA", 90, 36, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("SOMBRA", 90, 68, gfx.mix(RED, HOT, pulse * 0.3), 4, "center")
        c.ox = 0
        c.text("DE LA", 90, 108, AMBER, 3, "center")
        c.text("TIERRA", 90, 140, AMBER, 3, "center")
        moon(c, 90, 204, 26, 0.18, glow=0.15 * pulse)
        return
    c.text("¿POR QUÉ", 90, 40, AMBER, 3, "center")
    c.text("LA LUNA", 90, 72, ORANGE, 3, "center")
    c.text("TIENE", 90, 104, ORANGE, 3, "center")
    c.text("FASES?", 90, 136, ORANGE, 3, "center")
    moon(c, 90, 204, 26, 0.12 + (l - 6.1) * 0.12)


T_REFLEJA, T_MEDIA = 2.6, 7.2


def s_luz(c, l, d, b, h):
    sun_rays(c, 0, b)
    moon_x = 128
    if l < T_REFLEJA:
        c.disc(moon_x, 140, 28, DARK)
        c.ring(moon_x, 140, 28, 1, DIM, a0=-180, a1=180)
        c.text("SIN LUZ PROPIA", moon_x, 180, DIM, 1, "center")
    else:
        half_moon_toward(c, moon_x, 140, 28, 0)
        c.text("REFLEJA EL SOL", moon_x, 180, AMBER, 1, "center")
    if l >= T_MEDIA:
        c.box(70, 196, 100, 30, PANEL, AMBER)
        c.text("SIEMPRE MEDIA", 120, 201, AMBER, 1, "center")
        c.text("ILUMINADA", 120, 213, ORANGE, 1, "center")


def s_orbita(c, l, d, b, h):
    sun_rays(c, -40, b, n=6, y0=70, y1=200)
    ex, ey, R = 104, 134, 50
    c.ring(ex, ey, R, 1, DIM, a0=-180, a1=180)
    earth(c, ex, ey, 11)
    a = math.pi - l * 0.42
    mx, my = ex + math.cos(a) * R, ey + math.sin(a) * R
    half_moon_toward(c, mx, my, 9, -100)
    if l >= 3.3:
        c.text("29,5 DÍAS", 104, 202, AMBER, 2, "center")
        c.text("POR VUELTA", 104, 220, ORANGE, 1, "center")


PHASES = [(0.0, "NUEVA"), (0.12, "CRECIENTE"), (0.25, "CUARTO"), (0.5, "LLENA")]
T_PH = [6.1, 7.3, 9.3, 11.3]


def s_ves(c, l, d, b, h):
    c.text("DESDE AQUÍ VES", 90, 44, AMBER, 1, "center")
    c.text("UN TROZO DISTINTO", 90, 56, AMBER, 1, "center")
    for k, ((ph, name), st) in enumerate(zip(PHASES, T_PH)):
        if l < st:
            continue
        p = gfx.ease_out_back((l - st) * 2.5, 2)
        x = 30 + k * 40
        moon(c, x, 120, 15 * p + 0.5, ph, glow=0.4 * math.exp(-(l - st) * 3))
        c.text(name, x, 146 + (k % 2) * 12, AMBER if ph == 0.5 else ORANGE, 1, "center")


def s_mengua(c, l, d, b, h):
    ph = 0.5 + gfx.clamp01((l - 0.8) / 6) * 0.5
    moon(c, 90, 128, 46, ph)
    name = "LLENA" if ph < 0.55 else ("MENGUANTE" if ph < 0.97 else "NUEVA")
    c.text(name, 90, 192, AMBER, 2, "center")


T_SOMBRA, T_ECLIPSE = 0.4, 3.1


def s_sombra(c, l, d, b, h):
    sun_rays(c, -40, b, n=5, y0=90, y1=180)
    earth(c, 92, 134, 14)
    if l >= T_SOMBRA:
        # cono de sombra de la Tierra, hacia la derecha
        for k in range(60):
            hw = 13 - k * 0.12
            c.rect(106 + k, 134 - hw, 1, hw * 2, DARK, a=0.85)
        c.text("SOMBRA", 140, 108, DIM, 1, "center")
    if l < T_ECLIPSE:
        c.text("¿ES LA SOMBRA?", 90, 46, AMBER, 2, "center")
        half_moon_toward(c, 92, 98, 9, 0)
    else:
        e = gfx.ease_out_cubic((l - T_ECLIPSE) / 1.5)
        mx = gfx.lerp(160, 150, e)
        c.disc(mx, 134, 9, gfx.mix(AMBER, RED, e))
        c.ring(mx, 134, 9, 1, DIM, a0=-180, a1=180)
        c.text("SOLO EN", 90, 46, RED, 2, "center")
        c.text("ECLIPSES", 90, 64, RED, 2, "center")
        if l >= 5.2:
            c.text("ECLIPSE DE LUNA", 90, 200, AMBER, 1, "center")


T_C, T_D = 5.6, 10.3


def s_mentirosa(c, l, d, b, h):
    c.text("LA LUNA ES", 90, 42, AMBER, 2, "center")
    if l >= 2.3:
        c.text("MENTIROSA", 90, 60, RED, 2, "center")
    if l >= T_C:
        moon(c, 50, 124, 26, 0.85)
        c.text("C", 50, 162, AMBER, 3, "center")
        c.text("DECRECE", 50, 190, ORANGE, 1, "center")
    if l >= T_D:
        moon(c, 130, 124, 26, 0.15)
        c.text("D", 130, 162, AMBER, 3, "center")
        c.text("CRECE", 130, 190, ORANGE, 1, "center")
    if l >= 12:
        c.text("(HEMISFERIO NORTE)", 90, 212, DIM, 1, "center")


T_HOY, T_SUPER = 0.3, 3.8


def s_hoy(c, l, d, b, h):
    stars(c, b)
    if l < T_SUPER:
        c.text("ESTA SEMANA", 90, 44, AMBER, 2, "center")
        moon(c, 90, 128, 40, 0.1 + l * 0.01)
        c.text("CRECIENDO", 90, 186, ORANGE, 2, "center")
    else:
        p = gfx.ease_out_back((l - T_SUPER) * 1.5, 1.6)
        moon(c, 90, 122, 30 + 18 * p, 0.5, glow=0.2 + 0.1 * math.sin(b * 3))
        c.text("24 NOV", 90, 40, RED, 3, "center")
        c.box(28, 182, 124, 22, RED, RED)
        c.text("¡SUPERLUNA!", 90, 186, HOT, 2, "center", shadow=False)


COVER_LINES = ["FASES DE", "LA LUNA", "¿POR QUÉ?"]


def cover_art(c, y):
    for k, ph in enumerate((0.12, 0.25, 0.5, 0.75, 0.88)):
        moon(c, 22 + k * 34, y + 30, 14 if k != 2 else 17, ph)
    c.text("NO ES LA SOMBRA", 90, y + 58, RED, 1, "center")


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 LA LUZ", s_luz, False),
    (24, 38, "2 LA VUELTA", s_orbita, False),
    (38, 52, "3 LO QUE VES", s_ves, True),
    (52, 66, "4 MENGUA", s_mengua, True),
    (66, 80, "5 ¿Y LA SOMBRA?", s_sombra, False),
    (80, 100, "6 MENTIROSA", s_mentirosa, False),
    (100, 116, "7 ESTE MES", s_hoy, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = []   # con voz se generan solos

VOICE = [
    (0, "[misterioso] Las fases de la Luna… ¡no son la sombra de la Tierra!"),
    (8, "[narrando] La Luna no brilla: refleja la luz del Sol. Y siempre tiene media cara iluminada."),
    (24, "[sereno] Mientras da la vuelta a la Tierra, cada veintinueve días y medio…"),
    (38, "[asombrado] desde aquí vemos un trozo distinto de esa mitad: nueva, creciente, cuarto… ¡llena!"),
    (52, "[pensativo] Y luego mengua, poco a poco, hasta desaparecer otra vez."),
    (66, "[cómplice] ¿Y la sombra de la Tierra? Solo la tapa en los eclipses."),
    (80, "[riendo] Y ojo, que la Luna es mentirosa: si forma una ce, decrece… y si forma una de, crece."),
    (100, "[intrigado] Esta semana está creciendo… ¡y el veinticuatro llega la superluna!"),
    (116, "[alegre] ¡Sígueme para más datos curiosos!"),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3.3, "blip"), (4.2, "blip"), (6.1, "whoosh"), (6.3, "blip_up"), (7, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(8 + T_REFLEJA, "power_up"), (8 + T_MEDIA, "ding")]
    + [(25.2, "sweep_up"), (27.3, "ping")]
    + [(38 + t, "blip_up") for t in T_PH] + [(38.5, "sweep_up")]
    + [(52.8, "power_down"), (58.6, "ping")]
    + [(66 + T_SOMBRA, "sweep_fast"), (66 + T_ECLIPSE, "power_down"), (71.2, "ping")]
    + [(80 + T_C, "blip_up"), (80 + T_D, "blip_up"), (82.5, "error")]
    + [(100 + T_HOY, "sweep_up"), (100 + T_SUPER, "power_up"), (105.9, "ding")]
    + outro_sfx(116)
)
