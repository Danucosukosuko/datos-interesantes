"""Tema: Central nuclear, PARTE 1 — ¿Por qué uranio? (serie de 2; la parte 2 es topics/nuclear2.py)

Datos verificados (5-nov-2026):
- El U-235 es el único isótopo fisible que existe en la naturaleza en cantidad útil (Britannica).
  Tiene 92 protones y 143 neutrones.
- Al absorber un neutrón lento se parte en dos núcleos más pequeños, suelta 2 o 3 neutrones y
  ~200 MeV de energía. Esos neutrones pueden partir otros núcleos: reacción en cadena.
- El uranio natural solo tiene ~0,7 % de U-235 (el resto es U-238); los reactores de agua ligera
  usan uranio enriquecido al 3-5 %.
- Una pastilla de combustible (del tamaño de la yema de un dedo, unos 10 g) da tanta energía como
  ~1 tonelada de carbón (NEI; es una aproximación que depende del reactor).
- ¿Por qué no otro? El plutonio-239 también es fisible pero no existe en la naturaleza: se fabrica
  dentro de los reactores a partir del U-238. El torio-232 no es fisible: es «fértil», hay que
  convertirlo antes en U-233 con neutrones.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT, BG

TITLE = "¿Por qué las centrales nucleares usan uranio? (Parte 1)"
MUSIC_SEED = 20261105
MUSIC_KEY = 60
BOARD_SEED = 66


# ---------- elementos (también los usa nuclear2) ----------

def nucleus(c, cx, cy, r, seed=3, glow=0.0):
    """Núcleo: bolitas de protones (ámbar) y neutrones (naranja) apretadas."""
    n = int(r * r / 6)
    for k in range(n):
        a = k * 2.399963 + seed
        d = r * math.sqrt((k + 0.5) / n)
        col = AMBER if (k * 7 + seed) % 2 else ORANGE
        c.disc(cx + math.cos(a) * d, cy + math.sin(a) * d, 2.6, gfx.mix(col, HOT, glow))


def neutron(c, x, y, col=HOT):
    c.disc(x, y, 2.5, col)


def pellet(c, x, y, s=1.0):
    w, h = 14 * s, 18 * s
    c.box(x - w / 2, y, w, h, PANEL, AMBER, t=max(1, int(s)))
    c.rect(x - w / 2, y, w, 3 * s, AMBER)
    c.rect(x - w / 2 + 2 * s, y + 5 * s, 2 * s, h - 8 * s, ORANGE)


def coal(c, cx, base, w=60, h=34):
    for row in range(int(h / 6)):
        y = base - row * 6
        half = w / 2 * (1 - row * 6 / h)
        for k in range(int(half * 2 / 7)):
            x = cx - half + k * 7 + (row % 2) * 3
            c.box(x, y - 6, 7, 6, DARK, DIM)


def flash(c, cx, cy, t, r=30):
    if 0 <= t < 1:
        c.disc(cx, cy, r * t, HOT, a=1 - t)


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    if l < 5.2:
        pulse = math.exp(-(b % 1) * 5)
        c.text("ESTO", 90, 36, AMBER, 3, "center")
        c.text("DA LO QUE", 90, 68, AMBER, 3, "center")
        c.text("1 TONELADA", 90, 100, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("DE CARBÓN", 90, 132, gfx.mix(RED, HOT, pulse * 0.3), 3, "center")
        c.ox = 0
        pellet(c, 52, 178, 1.8)
        c.text("=", 90, 192, AMBER, 3, "center")
        coal(c, 134, 222, 56, 32)
        return
    c.box(44, 30, 92, 20, RED, RED)
    c.text("PARTE 1", 90, 33, HOT, 2, "center", shadow=False)
    c.text("¿POR QUÉ", 90, 64, AMBER, 3, "center")
    c.text("URANIO?", 90, 98, ORANGE, 3, "center")
    nucleus(c, 90, 186, 26, glow=0.2 * math.exp(-(b % 1) * 4))


def s_atomo(c, l, d, b, h):
    p = gfx.ease_out_back(l * 1.5, 1.6)
    nucleus(c, 90, 132, 40 * p, seed=5)
    for k in range(3):
        a = b * (0.7 + k * 0.3) + k * 2
        c.ring(90, 132, 62 + k * 4, 1, DIM, a0=-180, a1=180)
        c.disc(90 + math.cos(a) * (62 + k * 4), 132 + math.sin(a) * (62 + k * 4), 2, ORANGE)
    c.text("URANIO-235", 90, 46, AMBER, 2, "center")
    if l >= 5:
        c.text("92 PROTONES", 90, 206, AMBER, 1, "center")
        c.text("143 NEUTRONES", 90, 218, ORANGE, 1, "center")


def s_fision(c, l, d, b, h):
    hit = 3.3
    if l < hit:
        x = gfx.lerp(-10, 72, gfx.ease_in_cubic(l / hit))
        neutron(c, x, 130)
        c.text("NEUTRÓN", x, 116, HOT, 1, "center")
        nucleus(c, 90, 130, 28, seed=7)
    else:
        q = l - hit
        e = gfx.ease_out_cubic(q / 2)
        nucleus(c, 90 - 34 * e, 130 - 20 * e, 20, seed=1)
        nucleus(c, 90 + 34 * e, 130 + 20 * e, 20, seed=9)
        flash(c, 90, 130, q / 1.2, 46)
        for k in range(3):
            a = -1.2 + k * 1.2
            r = 20 + q * 26
            if r < 120:
                neutron(c, 90 + math.cos(a) * r, 130 + math.sin(a) * r)
        if q >= 1:
            c.text("¡SE PARTE EN DOS!", 90, 48, RED, 2, "center")
            c.text("+ ENERGÍA", 90, 200, AMBER, 2, "center")


def s_cadena(c, l, d, b, h):
    levels = [[(90, 60)], [(50, 112), (130, 112)], [(26, 168), (70, 168), (110, 168), (154, 168)]]
    for li, row in enumerate(levels):
        st = li * 1.8
        for (x, y) in row:
            if l < st:
                nucleus(c, x, y, 10, seed=int(x))
            else:
                q = l - st
                e = gfx.ease_out_cubic(q)
                nucleus(c, x - 8 * e, y, 7, seed=int(x))
                nucleus(c, x + 8 * e, y, 7, seed=int(y))
                flash(c, x, y, q / 0.8, 18)
                if li + 1 < len(levels):
                    for (nx, ny) in levels[li + 1]:
                        if abs(nx - x) < 50:
                            f = gfx.clamp01(q / 1.8)
                            neutron(c, gfx.lerp(x, nx, f), gfx.lerp(y, ny, f))
    if l >= 5.6:
        c.text("REACCIÓN", 90, 196, RED, 2, "center")
        c.text("EN CADENA", 90, 214, RED, 2, "center")


def s_energia(c, l, d, b, h):
    p = gfx.ease_out_back(l * 1.5, 2)
    pellet(c, 42, gfx.lerp(-60, 96, p), 2.2)
    c.text("1 PASTILLA", 42, 150, AMBER, 1, "center")
    if l >= 2.8:
        c.text("=", 90, 112, AMBER, 4, "center")
        e = gfx.ease_out_cubic((l - 2.8) / 2)
        coal(c, 138, 140, 70 * e + 2, 50 * e + 2)
        c.text("1 TONELADA", 138, 150, ORANGE, 1, "center")
        c.text("DE CARBÓN", 138, 160, ORANGE, 1, "center")
    if l >= 7:
        c.text("¡CASI LO MISMO!", 90, 196, AMBER, 2, "center")


def s_pureza(c, l, d, b, h):
    c.text("URANIO NATURAL", 90, 46, ORANGE, 1, "center")
    on = 0
    for k in range(140):
        x = 21 + (k % 14) * 10
        y = 60 + (k // 14) * 10
        special = k in (17, 62, 103) or (k == 131 and l >= 6)
        col = AMBER if special and l >= 2 else DIM
        c.disc(x, y, 3, col)
        on += special
    if l >= 3.7:
        c.text("SOLO 0,7 %", 90, 168, AMBER, 2, "center")
        c.text("ES URANIO-235", 90, 186, AMBER, 1, "center")
    if l >= 8:
        c.text("SE ENRIQUECE AL 3-5 %", 90, 210, RED, 1, "center")


CARDS = [(2.6, "PLUTONIO", "NO EXISTE EN", "LA NATURALEZA"), (7.4, "TORIO", "NO SE PARTE", "SOLO"),
         (10, "URANIO-235", "EL ÚNICO NATURAL", "QUE SE PARTE")]


def s_otros(c, l, d, b, h):
    p = gfx.ease_out_back(l * 2, 2)
    c.text("¿Y POR QUÉ", 90, gfx.lerp(-30, 44, p), AMBER, 2, "center")
    c.text("NO OTRO?", 90, gfx.lerp(-30, 62, p), AMBER, 2, "center")
    for k, (st, name, a, z) in enumerate(CARDS):
        if l < st:
            continue
        q = gfx.ease_out_back((l - st) * 2.5, 1.8)
        c.ox += round((1 - q) * 180)
        y = 84 + k * 46
        good = k == 2
        c.box(14, y, 152, 40, PANEL, AMBER if good else DIM)
        nucleus(c, 34, y + 20, 10, seed=k * 3, glow=0.3 if good else 0)
        c.text(name, 52, y + 5, AMBER if good else ORANGE, 2)
        c.text(a, 52, y + 22, AMBER if good else ORANGE, 1)
        c.text(z, 52, y + 31, AMBER if good else ORANGE, 1)
        if not good:
            c.text("X", 154, y + 13, RED, 2, "center", shadow=False)
        c.ox -= round((1 - q) * 180)


def tower(c, cx, base, h=90, w=50):
    for i in range(int(h)):
        t = i / h
        ww = w * (0.62 + 0.38 * (2 * t - 1) ** 2)
        y = base - i
        c.rect(cx - ww / 2, y, ww, 1, PANEL)
        c.rect(cx - ww / 2, y, 2, 1, ORANGE)
        c.rect(cx + ww / 2 - 2, y, 2, 1, ORANGE)


def plume(c, cx, top, b, n=7):
    for k in range(n):
        f = ((b * 0.25) + k / n) % 1
        c.disc(cx + math.sin(k * 1.7 + f * 3) * 8, top - f * 70, 10 + f * 14, DIM, a=0.55 * (1 - f))


def s_continuara(c, l, d, b, h):
    tower(c, 90, 220, 90, 60)
    plume(c, 90, 130, b)
    c.text("¿CÓMO SE", 90, 40, AMBER, 2, "center")
    c.text("CONVIERTE", 90, 58, AMBER, 2, "center")
    c.text("EN LUZ?", 90, 76, AMBER, 2, "center")
    if l >= 5 and int(b * 2) % 2 == 0:
        c.box(26, 108, 128, 22, RED, RED)
        c.text("PARTE 2 MAÑANA", 90, 112, HOT, 1, "center", shadow=False)


COVER_LINES = ["¿POR QUÉ", "URANIO?"]


def cover_art(c, y):
    c.box(44, y - 2, 92, 20, RED, RED)
    c.text("PARTE 1", 90, y + 1, HOT, 2, "center", shadow=False)
    nucleus(c, 62, y + 62, 22, seed=1, glow=0.2)
    nucleus(c, 120, y + 62, 22, seed=9, glow=0.2)
    c.disc(91, y + 62, 10, HOT, a=0.7)
    for k in range(3):
        neutron(c, 91 + math.cos(k * 2.1) * 18, y + 62 + math.sin(k * 2.1) * 18)
    c.text("CENTRAL NUCLEAR", 90, y + 100, ORANGE, 1, "center")


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 EL ÁTOMO", s_atomo, False),
    (24, 38, "2 FISIÓN", s_fision, True),
    (38, 52, "3 CADENA", s_cadena, True),
    (52, 66, "4 ENERGÍA", s_energia, False),
    (66, 80, "5 SOLO EL 0,7 %", s_pureza, False),
    (80, 100, "6 ¿Y OTROS?", s_otros, False),
    (100, 116, "7 CONTINUARÁ", s_continuara, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = []   # con voz se generan solos

VOICE = [
    (0, "[intrigado] Esta pastilla vale… ¡una tonelada de carbón!"),
    (8, "[narrando] Todo empieza en el núcleo de un átomo de uranio."),
    (24, "[asombrado] Le das con un neutrón… ¡y se parte en dos!"),
    (38, "Suelta más neutrones, que rompen otros átomos: ¡reacción en cadena!"),
    (52, "[cómplice] Por eso una pastilla así… equivale a una tonelada de carbón."),
    (66, "[pensativo] Pero del uranio natural solo sirve el cero coma siete por ciento."),
    (80, "[misterioso] ¿Y por qué no otro? El plutonio no existe en la naturaleza… y el torio no se parte solo."),
    (100, "[intrigado] ¿Y cómo se convierte en la luz de tu casa? Mañana, la segunda parte."),
    (116, "[alegre] ¡Sígueme para más datos curiosos!"),
]

SFX = (
    [(0, "power_up"), (1, "error"), (2, "error"), (3, "error"), (4, "whoosh"), (4.2, "blip_up"), (5, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(8.5, "sweep_up"), (13, "ping")]
    + [(24.5, "send"), (27.3, "thud"), (27.5, "power_up"), (29, "ping")]
    + [(38.2, "thud"), (40, "thud"), (41.8, "thud"), (43.6, "power_up")]
    + [(52.5, "blip_up"), (54.8, "ding"), (59, "power_up")]
    + [(69.7, "ping"), (74, "blip")]
    + [(82.6, "error"), (87.4, "error"), (90, "ding")]
    + [(101, "sweep_up"), (105, "power_up"), (107, "ding")]
    + outro_sfx(116)
)
