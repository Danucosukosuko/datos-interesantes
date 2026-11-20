"""Tema: ¿Cómo funciona una inteligencia artificial? (tecnología; IA que escribe, tipo ChatGPT)

Datos verificados (20-nov-2026; Maldita Tecnología, Uppers, HackerNoon, Understanding AI, Impacto TIC):
- Los modelos de lenguaje (LLM, como ChatGPT) generan texto prediciendo cuál es el siguiente
  fragmento (token) más probable, teniendo en cuenta todo el texto anterior.
- Se entrenan con muchísimo texto (libros, webs…).
- Por dentro son redes neuronales con miles de millones de números (parámetros) que se ajustan en el
  entrenamiento: GPT-3 (2020) tenía 175.000 millones. OpenAI no ha publicado las cifras de los
  modelos posteriores.
- Entrenar = adivinar, comprobar el error, ajustar los números… y repetir muchísimas veces.
- Responde palabra a palabra (token a token), eligiendo entre las más probables.
- No comprueba si algo es verdad: puede inventarse cosas con total seguridad («alucinaciones»).
- Después, personas puntúan sus respuestas para que aprenda a ser útil (ajuste con humanos).
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT

TITLE = "¿Cómo funciona una inteligencia artificial?"
MUSIC_SEED = 20261120
MUSIC_KEY = 60
BOARD_SEED = 201

NODES = [[(30, 70 + k * 30) for k in range(4)], [(90, 55 + k * 30) for k in range(5)], [(150, 85 + k * 30) for k in range(3)]]


def brain_net(c, b, active=1.0, flow=0.0):
    for li in range(len(NODES) - 1):
        for (x0, y0) in NODES[li]:
            for (x1, y1) in NODES[li + 1]:
                w = 0.5 + 0.5 * math.sin(x0 * 0.3 + y1 * 0.17 + b * flow)
                c.line(x0, y0, x1, y1, gfx.mix(DIM, AMBER, w * active), a=0.6)
    for layer in NODES:
        for (x, y) in layer:
            c.disc(x, y, 5, PANEL)
            c.ring(x, y, 5, 1, AMBER, a0=-180, a1=180)
            c.disc(x, y, 2, gfx.mix(DIM, HOT, active * (0.5 + 0.5 * math.sin(b * 3 + x + y))))


def bubble(c, x, y, w, text, col=AMBER, typed=None):
    c.box(x, y, w, 18, PANEL, col)
    t = text if typed is None else text[:typed]
    c.text(t, x + 5, y + 5, col, 1, "left", shadow=False)


def bars(c, x, y, items, q):
    for k, (word, p) in enumerate(items):
        yy = y + k * 16
        c.text(word, x, yy + 2, AMBER if k == 0 else ORANGE, 1, "left")
        w = 70 * p / 100 * q
        c.rect(x + 50, yy + 1, w, 9, RED if k == 0 else DIM)
        c.text(f"{int(p * q)} %", x + 54 + w, yy + 2, AMBER, 1, "left")


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    if l < 5.0:
        c.text("LA IA SOLO", 90, 34, AMBER, 3, "center")
        c.text("ADIVINA LA", 90, 66, AMBER, 3, "center")
        c.text("SIGUIENTE", 90, 98, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("PALABRA", 90, 130, gfx.mix(RED, HOT, pulse * 0.3), 4, "center")
        c.ox = 0
        bubble(c, 30, 190, 120, "HOLA, ¿QUÉ TAL ?")
        c.rect(108, 194, 6, 10, HOT if int(b * 2) % 2 == 0 else PANEL)
        return
    c.text("¿CÓMO", 90, 44, AMBER, 3, "center")
    c.text("FUNCIONA", 90, 76, ORANGE, 3, "center")
    c.text("UNA IA?", 90, 108, ORANGE, 3, "center")
    bubble(c, 30, 190, 120, "HOLA, ¿QUÉ TAL?")


T_CIELO, T_BARS = 0.7, 5.8


def s_juego(c, l, d, b, h):
    if l >= T_CIELO:
        bubble(c, 20, 50, 140, "EL CIELO ES ...")
    if l >= T_BARS:
        bars(c, 26, 92, [("AZUL", 80), ("GRIS", 12), ("VERDE", 1)], gfx.ease_out_cubic((l - T_BARS) / 2))
    if l >= 11.5:
        c.text("¡PROBABILIDAD!", 90, 160, RED, 2, "center")


T_LIBROS = 4.8


def s_lectura(c, l, d, b, h):
    n = int(gfx.clamp01((l - 2.2) / 7) * 40)
    for k in range(n):
        x = 14 + (k % 10) * 16
        y = 150 - (k // 10) * 22
        c.box(x, y, 12, 20, PANEL, gfx.mix(ORANGE, AMBER, (k * 7 % 10) / 10))
        c.rect(x + 2, y + 4, 8, 1, DIM)
    if l >= T_LIBROS:
        c.text("LIBROS, WEBS...", 90, 44, AMBER, 2, "center")
    if l >= 2.2:
        c.text("MUCHÍSIMO", 90, 184, RED, 2, "center")
        c.text("TEXTO", 90, 202, RED, 2, "center")


T_RED, T_NUM = 1.4, 3.0


def s_red(c, l, d, b, h):
    if l >= T_RED:
        brain_net(c, b, gfx.clamp01((l - T_RED) / 2), 3)
    if l >= T_NUM:
        c.box(16, 186, 148, 34, PANEL, RED)
        c.text("GPT-3:", 90, 190, AMBER, 1, "center")
        c.text("175.000 MILLONES", 90, 202, RED, 1, "center")
        c.text("DE NÚMEROS", 90, 212, AMBER, 1, "center")


T_FALLA, T_AJUSTA, T_REPITE = 1.4, 2.7, 6.3


def s_entrena(c, l, d, b, h):
    if l < T_AJUSTA:
        bubble(c, 20, 60, 140, "EL GATO DICE ...")
        if l >= T_FALLA:
            c.text("GUAU", 70, 100, RED, 3, "center")
            c.text("X", 130, 100, RED, 3, "center")
    else:
        brain_net(c, b * 4, 1.0, 6)
        c.text("CORRIGE LOS NÚMEROS", 90, 192, AMBER, 1, "center")
    if l >= T_REPITE:
        n = int(min(1.0, (l - T_REPITE) / 6) * 9_000_000)
        c.text(f"X {n:,}".replace(",", "."), 90, 34, RED, 2, "center")


T_TYPE = 2.0
ANSWER = ["LA", "LUNA", "TIENE", "FASES", "PORQUE", "..."]


def s_palabra(c, l, d, b, h):
    bubble(c, 14, 44, 152, "¿POR QUÉ HAY FASES?", ORANGE)
    k = int(max(0, l - T_TYPE) / 1.4)
    shown = ANSWER[:min(len(ANSWER), k + 1)] if l >= T_TYPE else []
    y = 80
    lines = [""]
    for w in shown:
        cand = (lines[-1] + " " + w).strip()
        if len(cand) > 22:
            lines.append(w)
        else:
            lines[-1] = cand
    c.box(14, y, 152, 40, PANEL, AMBER)
    for i, ln in enumerate(lines[:2]):
        c.text(ln, 20, y + 6 + i * 12, AMBER, 1, "left", shadow=False)
    if l >= T_TYPE and int(b * 2) % 2 == 0:
        c.rect(22 + len(lines[-1]) * 6, y + 6 + (len(lines) - 1) * 12, 5, 8, HOT)
    if l >= 3.0:
        c.text("PALABRA", 90, 150, RED, 3, "center")
        c.text("A PALABRA", 90, 180, RED, 3, "center")


T_OJO, T_INVENTA = 0.3, 6.4


def s_inventa(c, l, d, b, h):
    if l >= T_OJO:
        c.text("¡OJO!", 90, 40, RED, 3, "center")
    if l >= 1.5:
        c.text("NO SABE SI ES", 90, 76, AMBER, 2, "center")
        c.text("VERDAD", 90, 94, AMBER, 2, "center")
    if l >= T_INVENTA:
        c.box(14, 124, 152, 34, PANEL, RED)
        c.text("SE LO PUEDE", 90, 130, RED, 1, "center")
        c.text("INVENTAR TAN TRANQUILA", 90, 142, RED, 1, "center")
    if l >= T_INVENTA + 2:
        c.text("ALUCINACIONES", 90, 176, ORANGE, 2, "center")


T_PERSONAS = 1.4


def s_humanos(c, l, d, b, h):
    for k in range(3):
        x = 40 + k * 50
        c.disc(x, 70, 9, AMBER)
        c.rect(x - 10, 82, 20, 18, ORANGE)
        if l >= T_PERSONAS + k * 0.8:
            stars = 3 + (k % 2) * 2
            for s in range(stars):
                c.text("*", x - 12 + s * 6, 108, HOT, 1, "left")
    if l >= 2.0:
        c.text("PERSONAS", 90, 132, AMBER, 2, "center")
        c.text("PUNTÚAN SUS", 90, 150, AMBER, 2, "center")
        c.text("RESPUESTAS", 90, 168, AMBER, 2, "center")
    if l >= 4.8:
        c.text("PARA QUE SEA ÚTIL", 90, 192, ORANGE, 1, "center")


COVER_LINES = ["¿CÓMO", "PIENSA", "UNA IA?"]


def cover_art(c, y):
    for li in range(len(NODES) - 1):
        for (x0, y0) in NODES[li]:
            for (x1, y1) in NODES[li + 1]:
                c.line(x0, y + 4 + (y0 - 55) * 0.55, x1, y + 4 + (y1 - 55) * 0.55, DIM, a=0.6)
    for layer in NODES:
        for (x, yy) in layer:
            c.disc(x, y + 4 + (yy - 55) * 0.55, 4, AMBER)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 EL JUEGO", s_juego, False),
    (24, 38, "2 LEYÓ MUCHO", s_lectura, False),
    (38, 52, "3 LA RED", s_red, True),
    (52, 66, "4 ENTRENAR", s_entrena, True),
    (66, 80, "5 AL RESPONDER", s_palabra, False),
    (80, 100, "6 ¡OJO!", s_inventa, False),
    (100, 116, "7 PERSONAS", s_humanos, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = []   # con voz se generan solos

VOICE = [
    (0, "[misterioso] La IA solo adivina… ¡la siguiente palabra!"),
    (8, "[cómplice] Si te digo «el cielo es…», tú piensas «azul». La IA hace lo mismo, con probabilidades."),
    (24, "[asombrado] Para aprender, leyó muchísimo texto: libros, webs, conversaciones…"),
    (38, "[pensativo] Dentro hay una red con miles de millones de números que se van ajustando."),
    (52, "[enérgico] Adivina, falla, corrige esos números… y repite millones de veces."),
    (66, "[sereno] Al contestarte, escribe palabra a palabra, eligiendo entre las más probables."),
    (80, "[serio] Pero ojo: no sabe si algo es verdad. A veces se lo inventa con total seguridad."),
    (100, "[cómplice] Por eso, personas puntúan sus respuestas para que aprenda a ser útil."),
    (116, "[alegre] ¡Sígueme para más datos curiosos!"),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3, "blip"), (4.6, "whoosh"), (4.8, "blip_up"), (5.6, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(8 + T_CIELO, "blip"), (8 + T_BARS, "sweep_up"), (19.5, "ding")]
    + [(26.2, "bits"), (24 + T_LIBROS, "ping")]
    + [(38 + T_RED, "power_up"), (38 + T_NUM, "ding")]
    + [(52 + T_FALLA, "error"), (52 + T_AJUSTA, "sweep_fast"), (52 + T_REPITE, "bits")]
    + [(66 + T_TYPE + k * 1.4, "tick") for k in range(6)] + [(69, "ding")]
    + [(80 + T_OJO, "error"), (81.5, "blip"), (80 + T_INVENTA, "ping")]
    + [(100 + T_PERSONAS + k * 0.8, "blip_up") for k in range(3)]
    + outro_sfx(116)
)
