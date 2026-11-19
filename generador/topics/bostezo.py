"""Tema: ¿Por qué bostezamos? (cuerpo humano)

Datos verificados (19-nov-2026; Maldita Ciencia, Infobae 2025-2026, Meteored, El Universo/NYT):
- Los fetos bostezan dentro del útero, sin respirar por los pulmones: eso descarta la vieja idea de
  que bostezamos «por falta de oxígeno».
- Una de las teorías con más apoyo (Andrew Gallup): el bostezo ayuda a enfriar el cerebro (aire más
  fresco y más riego al estirar la mandíbula) para estar más alerta. No está cerrado.
- Un estudio (Viena) vio más bostezos contagiosos en invierno (45 %) que en verano (24 %).
- Entre el 40 % y el 60 % de las personas se contagian al ver bostezar a otro.
- El contagio es más frecuente entre familiares y amigos que entre desconocidos (Frontiers in
  Psychology).
- También se contagian chimpancés, bonobos, ratas, periquitos… y perros con bostezos humanos.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT

TITLE = "¿Por qué bostezamos?"
MUSIC_SEED = 20261119
MUSIC_KEY = 55
BOARD_SEED = 191


def face(c, cx, cy, r, yawn=0.0, col=AMBER, eyes_closed=None):
    c.disc(cx, cy, r, col)
    c.ring(cx, cy, r, 1, ORANGE, a0=-180, a1=180)
    closed = yawn > 0.5 if eyes_closed is None else eyes_closed
    for sx in (-1, 1):
        ex, ey = cx + sx * r * 0.38, cy - r * 0.18
        if closed:
            c.line(ex - r * 0.14, ey, ex + r * 0.14, ey, DARK, t=max(1, int(r / 14)))
        else:
            c.disc(ex, ey, max(1, r * 0.09), DARK)
    mh = r * (0.08 + 0.5 * yawn)
    mw = r * (0.35 - 0.1 * yawn)
    for i in range(int(-mh), int(mh) + 1):
        w = mw * math.sqrt(max(0, 1 - (i / max(mh, 1)) ** 2))
        c.rect(cx - w, cy + r * 0.38 + i, w * 2, 1, DARK)
    if yawn > 0.6:
        c.rect(cx - mw * 0.5, cy + r * 0.38 + mh * 0.4, mw, max(1, mh * 0.3), RED)


def fetus(c, cx, cy, s, yawn):
    c.ring(cx, cy, 34 * s, 2, ORANGE, a0=-180, a1=180)
    c.disc(cx, cy + 6 * s, 16 * s, gfx.mix(AMBER, ORANGE, 0.3))
    face(c, cx - 6 * s, cy - 10 * s, 11 * s, yawn)


def dog(c, cx, cy, s, yawn):
    c.disc(cx, cy, 14 * s, ORANGE)
    c.disc(cx - 12 * s, cy - 10 * s, 6 * s, DIM)
    c.disc(cx + 12 * s, cy - 10 * s, 6 * s, DIM)
    c.disc(cx - 5 * s, cy - 3 * s, 1.5 * s, DARK)
    c.disc(cx + 5 * s, cy - 3 * s, 1.5 * s, DARK)
    c.disc(cx, cy + 4 * s, 2.5 * s, DARK)
    mh = 2 * s + 8 * s * yawn
    c.rect(cx - 4 * s, cy + 7 * s, 8 * s, mh, DARK)
    if yawn > 0.5:
        c.rect(cx - 2 * s, cy + 7 * s + mh * 0.5, 4 * s, mh * 0.4, RED)


def yawn_curve(l, start, dur=2.5):
    t = (l - start) / dur
    if t < 0 or t > 1:
        return 0.0
    return math.sin(t * math.pi) ** 0.7


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    if l < 4:
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("BOSTEZAS", 90, 34, gfx.mix(RED, HOT, pulse * 0.3), 3, "center")
        c.ox = 0
        c.text("ANTES DE", 90, 66, AMBER, 3, "center")
        c.text("NACER", 90, 98, AMBER, 4, "center")
        fetus(c, 90, 190, 1.2, 0.85)
        return
    c.text("¿POR QUÉ", 90, 46, AMBER, 3, "center")
    c.text("BOSTEZAMOS?", 90, 80, ORANGE, 2, "center")
    face(c, 90, 180, 34, yawn_curve(l, 4.2, 3.5))


def s_oxigeno(c, l, d, b, h):
    c.text("¿FALTA DE", 90, 42, AMBER, 2, "center")
    c.text("OXÍGENO?", 90, 60, AMBER, 2, "center")
    if l >= 4:
        fetus(c, 90, 132, 1.1, yawn_curve(l, 4.5, 3) or 0.2)
    if l >= 8:
        c.text("NO RESPIRA AIRE", 90, 180, ORANGE, 1, "center")
        c.text("Y BOSTEZA", 90, 192, ORANGE, 1, "center")
    if l >= 12:
        c.box(30, 206, 120, 20, RED, RED)
        c.text("¡DESCARTADO!", 90, 211, HOT, 1, "center", shadow=False)


def s_frio(c, l, d, b, h):
    y = yawn_curve(l, 1.5, 6)
    face(c, 90, 120, 40, y)
    if l >= 1.5:
        for k in range(5):
            f = ((l * 0.8) + k / 5) % 1
            c.rect(150 - f * 40, 132 + k * 3, 8, 1, AMBER, a=1 - f)
    if l >= 4:
        c.text("UNA TEORÍA:", 90, 44, AMBER, 1, "center")
        c.text("ENFRÍA EL CEREBRO", 90, 56, RED, 1, "center")
    if l >= 9:
        c.text("PARA ESTAR ALERTA", 90, 184, ORANGE, 1, "center")


def s_invierno(c, l, d, b, h):
    c.text("UN ESTUDIO", 90, 42, AMBER, 1, "center")
    for k, (lab, pct, col, st) in enumerate((("INVIERNO", 45, AMBER, 2), ("VERANO", 24, DIM, 6))):
        if l < st:
            continue
        q = gfx.ease_out_cubic((l - st) / 2)
        x = 52 + k * 76
        hgt = 110 * pct / 50 * q
        c.rect(x - 16, 180 - hgt, 32, hgt, col)
        c.text(f"{int(pct * q)} %", x, 186, col, 2, "center")
        c.text(lab, x, 204, col, 1, "center")
    if l >= 10:
        c.text("MÁS EN INVIERNO", 90, 56, RED, 1, "center")


def s_contagio(c, l, d, b, h):
    for k in range(3):
        st = 1 + k * 2.2
        face(c, 36 + k * 54, 110, 21, yawn_curve(l, st, 2.5))
    if l >= 7:
        c.text("40 A 60 %", 90, 160, RED, 3, "center")
        c.text("SE CONTAGIA", 90, 190, AMBER, 2, "center")


def s_amigos(c, l, d, b, h):
    face(c, 54, 110, 26, yawn_curve(l, 0.5, 3))
    face(c, 126, 110, 26, yawn_curve(l, 2.5, 3))
    if l >= 2:
        c.disc(90, 74, 6, RED)
        c.disc(98, 74, 6, RED)
        for i in range(8):
            c.rect(84 + i, 76 + i, 20 - i * 2, 1, RED)
    if l >= 5:
        c.text("MÁS ENTRE", 90, 160, AMBER, 2, "center")
        c.text("AMIGOS Y FAMILIA", 90, 180, AMBER, 1, "center")


def s_perros(c, l, d, b, h):
    face(c, 50, 112, 26, yawn_curve(l, 1, 3))
    dog(c, 132, 116, 1.6, yawn_curve(l, 4, 3))
    if l >= 4:
        c.text("¡Y TU PERRO!", 90, 46, RED, 2, "center")
    if l >= 9:
        c.text("TAMBIÉN CHIMPANCÉS,", 90, 168, AMBER, 1, "center")
        c.text("RATAS Y PERIQUITOS", 90, 180, AMBER, 1, "center")


def s_final(c, l, d, b, h):
    face(c, 90, 108, 40, yawn_curve(l, 2, 4))
    c.text("¿BOSTEZASTE", 90, 168, AMBER, 2, "center")
    c.text("VIENDO ESTO?", 90, 186, ORANGE, 2, "center")


COVER_LINES = ["BOSTEZOS:", "¿POR QUÉ", "SE PEGAN?"]


def cover_art(c, y):
    face(c, 90, y + 40, 34, 0.9)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 ¿OXÍGENO?", s_oxigeno, False),
    (24, 38, "2 ¿ENFRIAR?", s_frio, False),
    (38, 52, "3 EN INVIERNO", s_invierno, True),
    (52, 66, "4 CONTAGIOSO", s_contagio, True),
    (66, 80, "5 AMIGOS", s_amigos, False),
    (80, 100, "6 PERROS", s_perros, False),
    (100, 116, "7 ¿Y TÚ?", s_final, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = [
    (0, "BOSTEZAS", 0.8), (1.5, "ANTES DE NACER", 0.6), (4, "¿POR QUÉ", 0.8), (6, "BOSTEZAMOS?", 1),
    (8.5, "SIEMPRE SE DIJO", 1), (11, "QUE ERA POR", 1), (13, "FALTA DE OXÍGENO", 0.8),
    (15, "PERO LOS FETOS", 1), (17, "NO RESPIRAN AIRE", 1), (19, "Y BOSTEZAN", 1), (21, "¡DESCARTADO!", 1),
    (24, "UNA TEORÍA:", 1), (26, "EL BOSTEZO", 1), (28, "ENFRÍA EL CEREBRO", 0.8),
    (31, "CON AIRE FRESCO", 1), (33, "PARA ESTAR", 1), (34.5, "MÁS ALERTA", 1),
    (38, "UN ESTUDIO", 1), (40, "EN INVIERNO:", 1), (42, "45 % BOSTEZÓ", 1),
    (44, "EN VERANO,", 1), (46, "SOLO EL 24 %", 1), (48, "MÁS EN INVIERNO", 1),
    (52, "Y ES CONTAGIOSO", 1), (55, "ENTRE EL 40", 1), (57, "Y EL 60 %", 1),
    (59, "BOSTEZA AL VER", 1), (61.5, "A OTRO BOSTEZAR", 1),
    (66, "SE CONTAGIA MÁS", 1), (69, "ENTRE AMIGOS", 1), (71.5, "Y FAMILIA", 1),
    (74, "QUE ENTRE", 1), (76, "DESCONOCIDOS", 1),
    (80, "¡Y HASTA", 1), (82, "TU PERRO", 1), (84, "SE CONTAGIA", 1), (86, "DE TUS BOSTEZOS!", 1),
    (89, "TAMBIÉN", 1), (90.5, "CHIMPANCÉS,", 1), (92.5, "RATAS", 1), (94, "Y PERIQUITOS", 1),
    (100, "Y AHORA", 1), (102, "DIME LA VERDAD:", 1), (105, "¿HAS BOSTEZADO", 1), (108, "VIENDO ESTO?", 1),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3, "blip"), (4, "whoosh"), (4.2, "sweep_up"), (5.5, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(12, "ping"), (12.5, "sweep_up"), (16, "blip_up"), (20, "error")]
    + [(25.5, "sweep_up"), (28, "ping"), (33, "ding")]
    + [(40, "sweep_up"), (44, "sweep_up"), (48, "ding")]
    + [(53, "sweep_up"), (55.2, "sweep_up"), (57.4, "sweep_up"), (59, "ding")]
    + [(66.5, "sweep_up"), (68, "ping"), (68.5, "sweep_up")]
    + [(81, "sweep_up"), (84, "sweep_up"), (84.5, "ding"), (89, "blip_up")]
    + [(102, "sweep_up"), (105, "ping")]
    + outro_sfx(116)
)
