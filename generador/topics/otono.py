"""Tema: ¿Por qué las hojas cambian de color en otoño? (naturaleza; temporada)

Datos verificados (8-nov-2026; Diario de Cuyo, UASLP, Muy Interesante, Telecinco, VOA):
- La clorofila (verde) capta la luz del sol para que la planta fabrique su alimento.
- Los carotenoides (amarillos y naranjas) están en la hoja TODO el año, tapados por la clorofila.
- En otoño hay menos horas de luz y más frío: el árbol deja de fabricar clorofila, el verde se
  degrada y aparecen los amarillos y naranjas que ya estaban.
- Los rojos y púrpuras (antocianinas) sí son nuevos: se fabrican en otoño a partir de los azúcares
  que quedan en la hoja y con luz solar. Por qué lo hace el árbol aún se discute (la teoría más
  aceptada: protegen la hoja mientras recupera nutrientes).
- Antes de soltar la hoja, el árbol recupera nutrientes valiosos como el nitrógeno.
- Después forma una capa de corte en la base del tallo (abscisión): la hoja cae y el árbol no
  pierde agua en invierno.
- El marrón de las hojas secas es de los taninos, que quedan al final.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT

TITLE = "¿Por qué las hojas cambian de color en otoño?"
MUSIC_SEED = 20261108
MUSIC_KEY = 55
BOARD_SEED = 88

GREEN = (104, 128, 38)    # verde oliva apagado, solo para la clorofila
BROWN = (120, 70, 30)


def leaf(c, cx, cy, s=1.0, col=AMBER, ang=0.0, edge=None):
    """Hoja ovalada con punta, nervio central y rabillo. ang inclina la hoja (radianes)."""
    L, W = 40 * s, 15 * s
    ca, sa = math.cos(ang), math.sin(ang)
    n = int(L * 2)
    for i in range(n):
        t = i / n
        w = W * math.sin(math.pi * t) ** 0.8
        x, y = cx + (t - 0.5) * L * 2 * sa, cy - (t - 0.5) * L * 2 * ca
        c.rect(x - w, y, w * 2, 1, col)
        if edge:
            c.rect(x - w, y, 1, 1, edge)
            c.rect(x + w - 1, y, 1, 1, edge)
    vein = gfx.mix(col, DARK, 0.45)
    c.line(cx - L * sa, cy + L * ca, cx + L * 0.9 * sa, cy - L * 0.9 * ca, vein, t=max(1, int(s)))
    for k in range(1, 4):
        t = k / 4
        x, y = cx + (t - 0.5) * L * 1.6 * sa, cy - (t - 0.5) * L * 1.6 * ca
        c.line(x, y, x - W * 0.7, y - W * 0.5, vein)
        c.line(x, y, x + W * 0.7, y - W * 0.5, vein)
    c.line(cx - L * sa, cy + L * ca, cx - L * 1.25 * sa, cy + L * 1.25 * ca, BROWN, t=max(1, int(s)))


def sun(c, cx, cy, r, b, col=AMBER):
    c.disc(cx, cy, r, col)
    for k in range(8):
        a = k * math.pi / 4 + b * 0.2
        c.line(cx + math.cos(a) * (r + 3), cy + math.sin(a) * (r + 3),
               cx + math.cos(a) * (r + 8), cy + math.sin(a) * (r + 8), col)


def branch(c, y=70):
    c.rect(0, y, 180, 5, BROWN)
    c.rect(0, y + 5, 180, 1, DARK)


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    if l < 4.5:
        c.text("LAS HOJAS", 90, 36, AMBER, 3, "center")
        c.text("YA ERAN", 90, 70, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("AMARILLAS", 90, 104, gfx.mix(RED, HOT, pulse * 0.3), 3, "center")
        c.ox = 0
        leaf(c, 62, 192, 1.0, GREEN, -0.3)
        c.text(">", 90, 186, AMBER, 3, "center")
        leaf(c, 122, 192, 1.0, AMBER, 0.3, edge=ORANGE)
        return
    c.text("¿POR QUÉ", 90, 44, AMBER, 3, "center")
    c.text("CAMBIAN", 90, 78, ORANGE, 3, "center")
    c.text("DE COLOR?", 90, 112, ORANGE, 3, "center")
    for k, col in enumerate((GREEN, AMBER, ORANGE, RED)):
        leaf(c, 30 + k * 40, 196 + math.sin(b * 2 + k) * 3, 0.6, col, -0.4 + k * 0.25)


def s_verde(c, l, d, b, h):
    sun(c, 150, 52, 12, b)
    p = gfx.ease_out_back(l * 1.5, 1.6)
    leaf(c, 84, 124, 1.35 * p + 0.01, GREEN, -0.2)
    if l >= 5.8:
        for k in range(3):
            f = ((l * 0.5) + k / 3) % 1
            c.disc(gfx.lerp(140, 96, f), gfx.lerp(62, 108, f), 2, HOT, a=1 - f * 0.5)
    c.text("CLOROFILA", 90, 200, GREEN if l < 2.6 else AMBER, 2, "center")
    if l >= 6:
        c.text("COME LUZ DEL SOL", 90, 220, AMBER, 1, "center")


def s_escondido(c, l, d, b, h):
    cover = 1 - gfx.ease_in_out((l - 2.2) / 2.5)
    leaf(c, 90, 132, 1.6, AMBER, 0.0, edge=ORANGE)
    if cover > 0.01:
        # la capa verde se levanta para enseñar lo que hay debajo
        c.oy = -round((1 - cover) * 30)
        leaf(c, 90, 132, 1.6, GREEN, 0.0)
        c.oy = 0
    if l >= 2.2:
        c.text("AMARILLOS Y NARANJAS", 90, 214, AMBER, 1, "center")
    if l >= 5.4:
        c.box(30, 40, 120, 20, RED, RED)
        c.text("¡TODO EL AÑO!", 90, 45, HOT, 1, "center", shadow=False)


def s_luz(c, l, d, b, h):
    q = gfx.clamp01(l / 7)
    sun(c, gfx.lerp(130, 150, q), gfx.lerp(44, 80, q), gfx.lerp(12, 8, q), b, gfx.mix(AMBER, DIM, q * 0.6))
    c.text("MENOS LUZ", 50, 44, AMBER, 1, "center")
    if l >= 1.7:
        c.text("+ FRÍO", 50, 56, ORANGE, 1, "center")
    g = gfx.ease_in_out((l - 4.5) / 5)
    leaf(c, 90, 146, 1.4, gfx.mix(GREEN, AMBER, g), 0.15, edge=ORANGE if g > 0.7 else None)
    if l >= 4.5:
        c.text("SIN CLOROFILA", 90, 220, RED if g < 0.9 else AMBER, 1, "center")


def s_rojo(c, l, d, b, h):
    r = gfx.ease_in_out((l - 0.4) / 3)
    leaf(c, 90, 142, 1.2, gfx.mix(AMBER, RED, r), -0.1, edge=gfx.mix(ORANGE, DARK, r))
    if l >= 0.3:
        c.text("EL ROJO", 90, 44, RED, 2, "center")
        c.text("SÍ ES NUEVO", 90, 62, AMBER, 2, "center")
    if l >= 5.6:
        for k in range(4):
            f = ((l * 0.6) + k / 4) % 1
            c.text("+", 60 + k * 20, 196 - f * 30, AMBER, 1, "center", a=1 - f)
        c.text("ANTOCIANINAS", 90, 206, RED, 1, "center")
        c.text("HECHAS CON AZÚCAR", 90, 218, AMBER, 1, "center")


def s_reciclaje(c, l, d, b, h):
    branch(c, 64)
    leaf(c, 90, 150, 1.3, gfx.mix(RED, DIM, gfx.clamp01(l / 12)), 0.0, edge=DARK)
    if l >= 3:
        for k in range(5):
            f = ((l * 0.7) + k / 5) % 1
            c.disc(90, gfx.lerp(160, 70, f), 2.5, AMBER, a=1 - f * 0.3)
        c.text("RECUPERA", 140, 110, AMBER, 1, "center")
        c.text("NUTRIENTES", 140, 120, AMBER, 1, "center")
    if l >= 5.8:
        c.text("COMO EL NITRÓGENO", 90, 218, ORANGE, 1, "center")


def s_cae(c, l, d, b, h):
    branch(c, 78)
    cut = 4.2
    if l < cut:
        leaf(c, 90, 128, 1.1, RED, 0.0, edge=DARK)
        if l >= 0.6 and int(b * 4) % 2 == 0:
            c.rect(84, 83, 12, 3, HOT)
        if l >= 0.6:
            c.text("SELLA EL TALLO", 90, 216, AMBER, 1, "center")
    else:
        q = l - cut
        y = 128 + q * 8
        x = 90 + math.sin(q * 1.8) * 26
        leaf(c, x, min(y, 172), 1.1, RED, math.sin(q * 1.8) * 0.8, edge=DARK)
        c.text("¡Y CAE!", 90, 38, RED, 3, "center")
        if l >= 7.3:
            c.box(20, 226, 140, 22, PANEL, AMBER)
            c.text("NO PIERDE AGUA", 90, 230, AMBER, 1, "center")
            c.text("EN INVIERNO", 90, 239, ORANGE, 1, "center")


def s_marron(c, l, d, b, h):
    p = gfx.clamp01(l / 3)
    for k in range(6):
        x = 22 + k * 27
        col = gfx.mix((AMBER, ORANGE, RED)[k % 3], BROWN, p)
        leaf(c, x, 186 + (k % 2) * 10, 0.55, col, -0.8 + k * 0.3, edge=DARK)
    if l >= 1.7:
        c.text("TANINOS", 90, 60, ORANGE, 3, "center")
        c.text("EL MARRÓN DEL FINAL", 90, 100, AMBER, 1, "center")


COVER_LINES = ["¿POR QUÉ", "CAMBIAN", "DE COLOR?"]


def cover_art(c, y):
    for k, (col, ang) in enumerate(((GREEN, -0.5), (AMBER, -0.15), (ORANGE, 0.2), (RED, 0.55))):
        leaf(c, 36 + k * 36, y + 44 + (k % 2) * 10, 0.7, col, ang, edge=DARK)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 EL VERDE", s_verde, False),
    (24, 38, "2 ESCONDIDOS", s_escondido, False),
    (38, 52, "3 MENOS LUZ", s_luz, True),
    (52, 66, "4 EL ROJO", s_rojo, True),
    (66, 80, "5 RECICLAJE", s_reciclaje, False),
    (80, 100, "6 ¡CORTE!", s_cae, False),
    (100, 116, "7 EL MARRÓN", s_marron, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = []   # con voz se generan solos

VOICE = [
    (0, "[intrigado] Las hojas… ¡ya eran amarillas!"),
    (8, "[narrando] En verano, la clorofila las pinta de verde: con ella comen luz del sol."),
    (24, "[cómplice] Pero debajo se esconden amarillos y naranjas… todo el año."),
    (38, "[pensativo] Con menos luz y más frío, el árbol deja de hacer clorofila… y el verde se va."),
    (52, "[asombrado] ¡El rojo sí es nuevo! Lo fabrican en otoño con el azúcar que queda."),
    (66, "Antes de soltarla, el árbol recupera lo valioso, como el nitrógeno."),
    (80, "[enérgico] Luego sella el tallo… ¡y la hoja cae! Así no pierde agua en invierno."),
    (100, "[sereno] Al final quedan los taninos: el marrón de las hojas secas."),
    (116, "[alegre] ¡Sígueme para más datos curiosos!"),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3, "blip"), (4.5, "whoosh"), (4.7, "blip_up"), (5.5, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(8.5, "sweep_up"), (9.5, "ping"), (13.8, "bits")]
    + [(26.2, "sweep_up"), (29.4, "ding")]
    + [(38.2, "power_down"), (42.8, "sweep_fast"), (45.4, "ping")]
    + [(52.4, "power_up"), (57.6, "bits"), (58.7, "ding")]
    + [(69, "sweep_up"), (71.9, "ping")]
    + [(80.6, "error"), (84.2, "send"), (87.3, "ding"), (92, "thud")]
    + [(101.7, "blip_up"), (103.8, "ping")]
    + outro_sfx(116)
)
