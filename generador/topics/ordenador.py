"""Tema: ¿Cómo funciona un ordenador? (publicado el 27-10-2026; vídeo hecho fuera de este generador).
Aquí solo se define la portada."""
from engine.gfx import AMBER, ORANGE, PANEL, DARK, DIM

TITLE = "¿Cómo funciona un ordenador?"
BOARD_SEED = 5
COVER_LINES = ["¿CÓMO", "FUNCIONA", "TU PC?"]


def cover_art(c, y):
    cx, cy = 90, y + 58
    s = 56
    x0, y0 = cx - s // 2, cy - s // 2
    # patillas
    for k in range(6):
        o = 6 + k * 9
        c.rect(x0 + o, y0 - 8, 3, 8, ORANGE)
        c.rect(x0 + o, y0 + s, 3, 8, ORANGE)
        c.rect(x0 - 8, y0 + o, 8, 3, ORANGE)
        c.rect(x0 + s, y0 + o, 8, 3, ORANGE)
    c.box(x0, y0, s, s, PANEL, AMBER, t=2)
    c.box(x0 + 10, y0 + 10, s - 20, s - 20, DARK, ORANGE)
    c.text("CPU", cx, cy - 10, AMBER, 2, "center")
    c.rect(x0 + 4, y0 + 4, 4, 4, DIM)
