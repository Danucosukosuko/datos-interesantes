"""Tema: ¿Cómo viaja un mensaje por internet?

Datos verificados:
- Los datos se trocean en paquetes; en Ethernet la MTU típica es de 1.500 bytes
  (20 cabecera IP + 20 cabecera TCP + 1.460 de datos).
- Cada paquete lleva una cabecera con la IP de destino y de origen; TCP numera los datos
  (números de secuencia) para reordenarlos en destino y reenviar los que se pierden.
- Los routers leen la dirección y reenvían el paquete al siguiente salto; los paquetes
  pueden ir por caminos distintos y llegar desordenados.
- Los cables submarinos transportan más del 99 % de los datos internacionales (UIT);
  ~570 sistemas en servicio a principios de 2025 (TeleGeography).
- En la fibra (índice ~1,47) la luz va a ~204.000 km/s, unos 2/3 de la velocidad en el vacío.
- Madrid–Nueva York: ~5.770 km en línea recta -> ~28 ms mínimo teórico en fibra.
- Un parpadeo dura aproximadamente 100-400 ms.
IPs del vídeo: rangos reservados para documentación (RFC 5737), no son reales.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT, BG

TITLE = "¿Cómo viaja un mensaje por internet?"
MUSIC_SEED = 20261101
MUSIC_KEY = 52   # Mi menor
BOARD_SEED = 33


# ---------- elementos reutilizables ----------

def envelope(c, x, y, w, h, col=ORANGE):
    c.box(x, y, w, h, PANEL, col)
    c.line(x, y, x + w / 2, y + h * 0.55, col)
    c.line(x + w - 1, y, x + w / 2, y + h * 0.55, col)


def packet(c, x, y, n, col=AMBER, w=26, h=18):
    c.box(x, y, w, h, PANEL, col)
    c.rect(x, y, w, 4, col)
    c.text(str(n), x + w / 2, y + 7, col, 1, "center", shadow=False)


def packet_small(c, x, y, n, col=AMBER):
    c.box(x - 7, y - 6, 14, 12, PANEL, col)
    c.text(str(n), x, y - 3, col, 1, "center", shadow=False)


def node(c, x, y, lit, b=0.0):
    col = AMBER if lit else DIM
    c.box(x - 8, y - 6, 16, 12, PANEL, col)
    blink = lit and int(b * 4) % 2 == 0
    c.rect(x - 4, y - 1, 2, 2, HOT if blink else col)
    c.rect(x + 2, y - 1, 2, 2, col)


def fmt_int(v):
    return f"{int(v):,}".replace(",", ".")


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    lines = [("¿CÓMO", AMBER), ("VIAJA TU", AMBER), ("MENSAJE?", ORANGE)]
    for k, (txt, col) in enumerate(lines):
        st = k * 0.5
        if l < st:
            continue
        p = gfx.ease_out_back((l - st) * 3, 2.2)
        c.text(txt, 90, gfx.lerp(-40, 46 + k * 36, p), col, 3, "center")
    if l >= 1.5:
        p = gfx.ease_out_back((l - 1.5) * 3, 2)
        c.text("POR INTERNET", 90, gfx.lerp(330, 158, p), ORANGE, 2, "center")
    # sobre cruzando la pantalla desde el primer instante
    q = (l * 0.5) % 1
    x = gfx.lerp(-50, 200, gfx.ease_in_out(q))
    y = 192 + math.sin(q * math.pi * 2) * 6
    for i in range(1, 6):
        c.rect(x - 4 - i * 8, y + 9, 6, 2, AMBER, a=0.7 - i * 0.12)
    envelope(c, x, y, 32, 22, AMBER)


MSG = ["¡HO", "LA! ", "¿QUÉ", "TAL?"]


def s_paquetes(c, l, d, b, h):
    if l < 6:
        sh = math.sin(l * 40) * 2 if l >= 4 else 0
        p = gfx.ease_out_back(l * 2, 2)
        ey = gfx.lerp(-80, 74, p)
        envelope(c, 50 + sh, ey, 80, 54)
        c.text("¡HOLA! ¿QUÉ TAL?", 90 + sh, ey + 64, AMBER, 1, "center")
        if l >= 4:
            c.text("¡A TROCEAR!", 90, 52, RED, 2, "center")
        return
    q = l - 6
    for k in range(4):
        st = k * 0.5
        t = gfx.ease_out_back((q - st) * 2, 1.8) if q >= st else 0.0
        x = gfx.lerp(77, 10 + k * 42, t)
        y = gfx.lerp(84, 70, t)
        packet(c, x, y, k + 1)
        if t > 0.9:
            c.text(MSG[k], x + 13, y + 24, ORANGE, 1, "center")
    if q >= 5:
        p = gfx.ease_out_back((q - 5) * 2, 2)
        c.oy += round((1 - p) * 60)
        c.text("HASTA", 90, 130, ORANGE, 1, "center")
        c.text("1.500 BYTES", 90, 142, AMBER, 2, "center")
        c.text("CADA UNO", 90, 162, ORANGE, 1, "center")
        c.oy -= round((1 - p) * 60)


ROWS = [(2, "PARA:", "203.0.113.7"), (5, "DE:", "192.0.2.15"), (9, "PAQUETE:", "1 DE 4")]


def s_etiqueta(c, l, d, b, h):
    p = gfx.ease_out_back(l * 2, 1.8)
    x0, w, hh = 16, 148, 140
    y0 = gfx.lerp(-150, 50, p)
    c.box(x0, y0, w, hh, PANEL, AMBER, t=2)
    c.rect(x0 + 2, y0 + 2, w - 4, 18, RED)
    c.text("ETIQUETA", 90, y0 + 4, HOT, 2, "center", shadow=False)
    for k, (st, lab, val) in enumerate(ROWS):
        if l < st:
            continue
        yy = y0 + 24 + k * 28
        flash = math.exp(-(l - st) * 3)
        c.text(lab, x0 + 8, yy, ORANGE, 1, shadow=False)
        c.text(val, 90, yy + 11, gfx.mix(AMBER, HOT, flash), 2, "center")
    for row in range(2):
        s = "".join("1" if ((row * 19 + col + int(b * 3)) * 2654435761 >> 9) & 1 else "0" for col in range(22))
        c.text(s, 90, y0 + 114 + row * 10, DIM, 1, "center", shadow=False)


NODES = [(18, 140), (56, 92), (56, 188), (96, 140), (132, 92), (132, 188), (162, 140)]
EDGES = [(0, 1), (0, 2), (1, 3), (2, 3), (1, 4), (3, 4), (3, 5), (2, 5), (4, 6), (5, 6)]
PATH = [0, 1, 3, 4, 6]


def s_routers(c, l, d, b, h):
    hop = (l - 2) / 2
    steps = list(zip(PATH, PATH[1:]))
    for a, z in EDGES:
        col = DIM
        if (a, z) in steps and hop >= steps.index((a, z)):
            col = ORANGE
        (x0, y0), (x1, y1) = NODES[a], NODES[z]
        c.line(x0, y0, x1, y1, col, t=2)
    for i, (x, y) in enumerate(NODES):
        lit = i in PATH and hop >= PATH.index(i)
        node(c, x, y, lit, b)
    if 0 <= hop < 4:
        j = int(hop)
        f = gfx.ease_in_out(hop - j)
        (x0, y0), (x1, y1) = NODES[PATH[j]], NODES[PATH[j + 1]]
        px, py = gfx.lerp(x0, x1, f), gfx.lerp(y0, y1, f)
        c.box(px - 6, py - 4, 12, 8, AMBER, HOT)
    c.text("TÚ", 18, 154, AMBER, 1, "center")
    c.text("DESTINO", 176, 154, AMBER, 1, "right")
    if hop >= 4:
        c.text("¡LLEGÓ!", 90, 50, AMBER, 2, "center")
    elif hop >= 0:
        c.text(f"SALTO {int(hop) + 1}", 90, 50, AMBER, 2, "center")
    else:
        c.text("ROUTERS", 90, 50, ORANGE, 2, "center")


FISH = ["..##..#", ".######", "#.#####", ".######", "..##..#"]


def s_oceano(c, l, d, b, h):
    top, bed = 80, 206
    c.text("AMÉRICA", 4, top - 22, ORANGE, 1)
    c.text("EUROPA", 176, top - 22, ORANGE, 1, "right")
    c.rect(0, top - 8, 16, bed - top + 16, PANEL)
    c.rect(164, top - 8, 16, bed - top + 16, PANEL)
    c.rect(16, top, 148, bed - top, DARK, a=0.6)
    for x in range(16, 164, 2):
        c.rect(x, top + 2 * math.sin(x / 8 + b * 3) - 1, 2, 2, ORANGE)
    for x in range(16, 164, 4):
        c.rect(x, bed + math.sin(x * 0.3) * 2, 4, 6, PANEL)
    # cable en el fondo, de costa a costa
    c.rect(8, top - 8, 3, bed - top + 4, DIM)
    c.rect(169, top - 8, 3, bed - top + 4, DIM)
    c.rect(8, bed - 4, 164, 3, DIM)
    for k in range(5):
        px = 10 + (l * 34 + k * 33) % 158
        c.rect(px, bed - 4, 6, 3, AMBER)
        c.rect(px + 4, bed - 4, 2, 3, HOT)
    fx = 170 - (l * 12) % 170
    c.sprite(FISH, fx, 120 + math.sin(l * 2) * 4, {"#": ORANGE}, 2)
    if 2 <= l < 8:
        c.text("CABLE SUBMARINO", 90, 186, AMBER, 1, "center")
    if l >= 8:
        p = gfx.ease_out_back((l - 8) * 2, 2.4)
        c.oy += round((1 - p) * -120)
        c.rect(10, 96, 160, 80, BG, a=0.75)
        c.text("+99%", 90, 102, AMBER, 4, "center")
        c.text("DEL TRÁFICO", 90, 138, ORANGE, 2, "center")
        c.text("INTERNACIONAL", 90, 156, ORANGE, 2, "center")
        c.oy -= round((1 - p) * -120)


def zig(x):
    t = (x / 44) % 2
    return 108 + 44 * (t if t < 1 else 2 - t)


def s_luz(c, l, d, b, h):
    p = gfx.ease_out_back(l * 2, 2)
    c.text("FIBRA ÓPTICA", 90, gfx.lerp(-30, 52, p), AMBER, 2, "center")
    c.rect(0, 96, 180, 72, PANEL)
    c.rect(0, 104, 180, 56, DARK)
    c.rect(0, 96, 180, 2, ORANGE)
    c.rect(0, 166, 180, 2, ORANGE)
    for k in range(3):
        head = (l * 60 + k * 90) % 270 - 40
        for i in range(70):
            xx = head - i
            if 0 <= xx < 180:
                c.rect(xx, zig(xx), 2, 2, gfx.mix(HOT, ORANGE, i / 70), a=1 - i / 70)
    if l >= 6:
        q = gfx.ease_out_cubic((l - 6) / 4)
        c.text(fmt_int(200_000 * q) + " KM/S", 90, 182, AMBER if l >= 10 else ORANGE, 2, "center")
        c.text("DENTRO DEL CRISTAL", 90, 204, ORANGE, 1, "center")


OFF = [-72, 0, 62]
PK = [(1, 0, 0.5, 5.0), (2, 2, 1.0, 6.0), (3, 1, 1.5, 3.0), (4, 1, 2.0, 4.0)]
ARR = {3: 4.5, 1: 5.5, 4: 6.0}
RESEND = 14.5


def route_pt(r, t):
    return gfx.lerp(22, 158, t), 140 + OFF[r] * math.sin(math.pi * t)


def s_rutas(c, l, d, b, h):
    for r in range(3):
        for i in range(0, 41, 2):
            x, y = route_pt(r, i / 40)
            c.rect(x, y, 2, 2, DIM)
    node(c, 14, 140, True, b)
    node(c, 166, 140, l >= 4.5, b)
    for n, r, st, du in PK:
        t = (l - st) / du
        if n == 2:
            if 0 <= t < 0.5:
                packet_small(c, *route_pt(r, t), n)
            elif l >= st + du * 0.5 and l < 10 and int(b * 3) % 2 == 0:
                x, y = route_pt(r, 0.5)
                c.text("X", x, y - 7, RED, 2, "center")
            continue
        if 0 <= t < 1:
            packet_small(c, *route_pt(r, t), n)
    if RESEND <= l < RESEND + 3:
        packet_small(c, *route_pt(1, (l - RESEND) / 3), 2, HOT)
    # fila de llegada
    c.text("LLEGAN:" if l < 10 else "ORDEN:", 4, 51, ORANGE, 1)
    if l < 10:
        order = [n for n, a in sorted(ARR.items(), key=lambda kv: kv[1]) if l >= a]
    else:
        order = [1, 2, 3, 4]
    for k, n in enumerate(order):
        x = 50 + k * 24
        missing = n == 2 and l < RESEND + 3
        if missing:
            if int(b * 3) % 2 == 0:
                c.box(x, 46, 20, 18, PANEL, RED)
                c.text("?", x + 10, 48, RED, 2, "center", shadow=False)
            continue
        c.box(x, 46, 20, 18, PANEL, AMBER)
        c.text(str(n), x + 10, 48, AMBER, 2, "center", shadow=False)
    if l >= RESEND + 3.5:
        c.text("¡COMPLETO!", 90, 220, AMBER, 2, "center")


def s_velocidad(c, l, d, b, h):
    mad, ny = (150, 150), (30, 150)
    if l < 8:
        p = gfx.ease_out_back(l * 2, 2)
        c.text("5.770 KM", 90, gfx.lerp(-30, 50, p), AMBER, 2, "center")
        for x in range(10, 170, 2):
            c.rect(x, 176 + 2 * math.sin(x / 7 + b * 2), 2, 2, DIM)
        t = gfx.clamp01((l - 1) / 2)
        for i in range(0, 61, 2):
            f = i / 60
            x = gfx.lerp(mad[0], ny[0], f)
            y = 150 - 50 * math.sin(math.pi * f)
            c.rect(x, y, 2, 2, ORANGE if f <= t else DIM)
        c.disc(*mad, 4, AMBER)
        c.disc(*ny, 4, AMBER)
        c.text("MADRID", 150, 160, ORANGE, 1, "center")
        c.text("NUEVA YORK", 32, 160, ORANGE, 1, "center")
        if 1 <= l and t < 1:
            x = gfx.lerp(mad[0], ny[0], t)
            y = 150 - 50 * math.sin(math.pi * t)
            envelope(c, x - 8, y - 6, 16, 12, AMBER)
        if l >= 1:
            c.text(f"{int(28 * t)} MS", 90, 190, AMBER if t >= 1 else ORANGE, 4, "center")
        if l >= 3.5 and int(b * 2) % 2 == 0:
            c.text("*EN LÍNEA RECTA", 90, 224, RED, 1, "center")
        return
    q = l - 8
    p = gfx.ease_out_back(q * 2, 2)
    c.text("28 MS", 90, gfx.lerp(-30, 48, p), AMBER, 3, "center")
    c.text("VS", 90, 80, ORANGE, 2, "center")
    ph = q % 3
    open_ = 1.0 if ph > 0.5 else abs(math.cos(ph / 0.5 * math.pi))
    cx, cy = 90, 136
    for x in range(-40, 41, 2):
        hh = 20 * (1 - (x / 40) ** 2) * open_
        c.rect(cx + x, cy - hh - 1, 2, 2, ORANGE)
        c.rect(cx + x, cy + hh - 1, 2, 2, ORANGE)
    for x in range(-12, 13):
        lid = 20 * (1 - (x / 40) ** 2) * open_ - 1
        ih = min(math.sqrt(max(0, 144 - x * x)), lid)
        if ih > 0:
            c.rect(cx + x, cy - ih, 1, 2 * ih, AMBER)
        ph_ = min(math.sqrt(max(0, 25 - x * x)), lid)
        if ph_ > 0:
            c.rect(cx + x, cy - ph_, 1, 2 * ph_, BG)
    c.text("PARPADEO", 90, 170, ORANGE, 2, "center")
    c.text("100-400 MS", 90, 190, AMBER, 2, "center")


COVER_LINES = ["¿CÓMO", "VIAJA TU", "MENSAJE?"]


def cover_art(c, y):
    c.text("POR INTERNET", 90, y, ORANGE, 2, "center")
    gy = y + 46
    # globo
    c.ring(132, gy, 20, 3, ORANGE, a0=-180, a1=180)
    c.rect(112, gy - 1, 40, 2, DIM)
    c.rect(116, gy - 10, 32, 2, DIM)
    c.rect(116, gy + 9, 32, 2, DIM)
    c.rect(131, gy - 20, 2, 40, DIM)
    # sobre con estela
    for i in range(1, 5):
        c.rect(40 - i * 9, gy + 2, 7, 3, AMBER, a=0.9 - i * 0.18)
    envelope(c, 44, gy - 15, 44, 30, AMBER)
    for x in range(92, 108, 4):
        c.rect(x, gy, 2, 2, AMBER)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 PAQUETES", s_paquetes, True),
    (24, 38, "2 ETIQUETA", s_etiqueta, False),
    (38, 52, "3 ROUTERS", s_routers, True),
    (52, 66, "4 OCÉANO", s_oceano, True),
    (66, 80, "5 LUZ", s_luz, True),
    (80, 100, "6 CAMINOS", s_rutas, True),
    (100, 116, "7 VELOCIDAD", s_velocidad, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = [
    (0, "TU MENSAJE CRUZA", 0.5), (3, "EL OCÉANO", 0.5), (5, "EN UN PARPADEO", 0.5),
    (8, "TU MENSAJE NO", 1), (11, "VIAJA ENTERO", 1),
    (14, "SE TROCEA EN", 1), (17, "PAQUETES", 1),
    (19, "DE HASTA 1.500", 1), (21, "BYTES", 1),
    (24, "CADA PAQUETE", 1), (26, "LLEVA UNA ETIQUETA", 1),
    (30, "CON LA IP", 1), (32, "DE DESTINO", 1), (34, "Y SU NÚMERO", 1),
    (38, "LOS ROUTERS", 1), (40, "LEEN LA ETIQUETA", 1),
    (44, "Y LO PASAN", 1), (46, "AL SIGUIENTE SALTO", 1),
    (52, "PARA CRUZAR", 1), (54, "EL OCÉANO", 1),
    (56, "VA POR CABLES", 1), (58, "SUBMARINOS", 1),
    (60, "MÁS DEL 99 %", 1), (62, "DEL TRÁFICO", 1), (64, "INTERNACIONAL", 1),
    (66, "DENTRO VIAJA", 1), (68, "COMO PULSOS DE LUZ", 1),
    (72, "REBOTANDO EN", 1), (74, "EL CRISTAL", 1), (76, "A UNOS 200.000 KM/S", 1),
    (80, "CADA PAQUETE", 1), (82, "PUEDE IR", 1), (84, "POR UN CAMINO", 1),
    (86, "Y LLEGAR DESORDENADO", 1),
    (90, "EL DESTINO LOS", 1), (92, "ORDENA POR NÚMERO", 1),
    (95, "Y SI SE PIERDE UNO", 1), (97, "SE VUELVE A ENVIAR", 1),
    (100, "MADRID - NUEVA YORK", 1), (103, "SON 5.770 KM", 1),
    (105, "MÍNIMO 28", 1), (106.5, "MILISEGUNDOS", 1),
    (108, "MÁS RÁPIDO QUE", 1), (111, "UN PARPADEO", 1),
]

SFX = (
    [(0, "whoosh"), (0, "blip_up"), (0.5, "blip_up"), (1, "blip_up"), (1.5, "power_up"),
     (2, "send"), (4, "send"), (6, "send")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(9, "thud"), (12, "tick"), (13, "tick"), (14, "bits")]
    + [(14 + k * 0.5, "blip_up") for k in range(4)] + [(19, "power_up")]
    + [(24.5, "thud"), (26, "ping"), (29, "ping"), (33, "ding"), (35, "bits")]
    + [(40, "send"), (42, "ping"), (44, "ping"), (46, "ping"), (48, "ding")]
    + [(53, "sweep_up"), (56, "bits"), (58, "bits"), (60, "power_up")]
    + [(67, "sweep_fast"), (69, "sweep_fast"), (71, "sweep_fast"), (72, "sweep_up"), (76, "ding")]
    + [(80.5, "send"), (81, "send"), (81.5, "send"), (82, "send"), (84, "error"),
       (84.5, "ping"), (85.5, "ping"), (86, "ping"), (90, "bits"), (94.5, "send"),
       (97.5, "ding"), (98, "power_up")]
    + [(101, "send"), (101.5, "tick"), (102, "tick"), (102.5, "tick"), (103, "ding"),
       (108, "sweep_up"), (108.2, "blip"), (111.2, "blip"), (114.2, "blip")]
    + outro_sfx(116)
)
