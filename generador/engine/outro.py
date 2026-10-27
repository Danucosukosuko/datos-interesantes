"""Cierre común a TODOS los vídeos: "¡SÍGUEME PARA MÁS DATOS CURIOSOS!".
Úsalo tal cual como última escena (beats 116-128) y añade outro_sfx() a SFX."""
import math
from . import gfx
from .gfx import AMBER, ORANGE, RED

LINES = [("¡SÍGUEME", AMBER), ("PARA MÁS", ORANGE), ("DATOS", AMBER), ("CURIOSOS!", ORANGE)]
HEART = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]


def s_outro(c, l, d, b, h):
    for k, (txt, col) in enumerate(LINES):
        st = 1 + k
        if l >= st:
            p = gfx.ease_out_back((l - st) * 2.5, 2.4)
            c.text(txt, 90, gfx.lerp(-40, 50 + k * 38, p), col, 3, "center")
    if l >= 5:
        pulse = math.exp(-(b % 1) * 4)
        s = 4 + (1 if pulse > 0.6 else 0)
        w = 7 * s
        c.sprite(HEART, 90 - w / 2, 214 - (s - 4) * 3, {"#": RED}, s)


def outro_sfx(start=116):
    return [(start, "whoosh"), (start + 1, "blip_up"), (start + 2, "blip_up"),
            (start + 3, "blip_up"), (start + 4, "power_up"), (start + 5, "ding"),
            (start + 8, "ding"), (start + 10, "end")]
