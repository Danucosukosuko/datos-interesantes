"""Portada 1080x1920 (JPG) con el mismo estilo que los vídeos.
Zona segura: todo lo importante entre y=50 y y=270 del lienzo (recorte 3:4 de la cuadrícula de Instagram).
Cada tema puede definir COVER_LINES (lista de líneas del título) y cover_art(c) (dibujo grande)."""
import math
import textwrap
import numpy as np
from PIL import Image

from . import gfx, font
from .gfx import Canvas, AMBER, ORANGE, RED, DARK, PANEL, HOT


def _lines(topic):
    if hasattr(topic, "COVER_LINES"):
        return topic.COVER_LINES
    words = topic.TITLE.upper().split()
    out, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.text_width(test, 3) <= 168:
            cur = test
        else:
            out.append(cur); cur = w
    out.append(cur)
    return out


def render_cover(topic, path):
    board = gfx.Board(getattr(topic, "BOARD_SEED", 7))
    img = board.draw(0.37, 0.8)
    c = Canvas(img)
    # marco de pantalla
    c.frame(3, 3, 174, 314, ORANGE, t=2)
    c.frame(7, 7, 166, 306, DARK)
    # etiqueta superior
    tag = "DATO CURIOSO"
    w = font.text_width(tag, 2)
    c.box(90 - w / 2 - 8, 52, w + 16, 24, RED, RED)
    c.text(tag, 90, 53, HOT, 2, "center")
    # título grande
    lines = _lines(topic)
    y = 92
    for k, ln in enumerate(lines):
        col = AMBER if k < len(lines) - 1 else ORANGE
        c.text(ln, 90, y, col, 3, "center")
        y += 34
    # dibujo del tema
    if hasattr(topic, "cover_art"):
        topic.cover_art(c, y + 4)
    # pie
    c.text("¡SÍGUEME PARA MÁS!", 90, 292, gfx.DIM, 1, "center", shadow=False)
    out = gfx.CRT().apply(img)
    Image.fromarray(out).save(path, quality=92)
    return path
