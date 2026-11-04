"""Tema: ¿Cómo sabe el GPS dónde estás?

Datos verificados (4-nov-2026):
- La constelación GPS tiene más de 30 satélites operativos (31 en julio de 2023 según gps.gov;
  ~32 en 2026) a unos 20.200 km de altura; cada uno da dos vueltas a la Tierra al día.
- Cada satélite emite continuamente su posición y la hora exacta de su reloj atómico. El receptor
  solo escucha: no envía nada, así que la posición se calcula sin internet ni datos (el mapa sí
  hay que tenerlo descargado; el A-GPS solo usa datos para arrancar más rápido).
- La señal viaja a la velocidad de la luz: 20.200 km / 300.000 km/s ≈ 0,067 s.
- Distancia = tiempo de viaje × velocidad de la luz. Con 3 distancias queda un único punto;
  hace falta un 4.º satélite para corregir el reloj del móvil (1 microsegundo de error ≈ 300 m).
- Relatividad: los relojes de los satélites se adelantan unos 38 µs al día (+45 µs por la menor
  gravedad, −7 µs por la velocidad). Sin corregirlo, el error crecería en más de 10 km al día.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT, BG

TITLE = "¿Cómo sabe el GPS dónde estás?"
MUSIC_SEED = 20261104
MUSIC_KEY = 57   # La menor
BOARD_SEED = 55


# ---------- elementos ----------

def satellite(c, x, y, s=1.0, col=AMBER):
    w = 8 * s
    c.box(x - w / 2, y - w / 2, w, w, PANEL, col)
    pw, ph = 12 * s, 5 * s
    c.box(x - w / 2 - pw - 1, y - ph / 2, pw, ph, DARK, ORANGE)
    c.box(x + w / 2 + 1, y - ph / 2, pw, ph, DARK, ORANGE)
    c.rect(x - 1, y + w / 2, 2, 3 * s, col)


def earth(c, cx, cy, r):
    c.disc(cx, cy, r, PANEL)
    c.ring(cx, cy, r, 2, ORANGE, a0=-180, a1=180)
    for k in range(5):
        c.rect(cx - r * 0.6 + k * r * 0.25, cy - r * 0.3 + (k % 2) * r * 0.4, r * 0.3, r * 0.15, DIM)


def phone(c, x, y, w=24, h=42, col=AMBER):
    c.box(x, y, w, h, DARK, col, t=2)
    c.rect(x + 3, y + 6, w - 6, h - 12, PANEL)
    c.rect(x + w / 2 - 3, y + 2, 6, 2, DIM)


def pin(c, x, y, s=1.0, col=RED):
    c.disc(x, y - 6 * s, 5 * s, col)
    c.disc(x, y - 6 * s, 2 * s, BG)
    for k in range(int(6 * s)):
        c.rect(x - (6 * s - k) * 0.5, y - 3 * s + k, (6 * s - k), 1, col)


def clock(c, cx, cy, r, ang, col=AMBER):
    c.ring(cx, cy, r, 2, col, a0=-180, a1=180)
    c.line(cx, cy, cx + math.cos(ang) * (r - 3), cy + math.sin(ang) * (r - 3), col, t=2)
    c.disc(cx, cy, 2, col)


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    # Gancho visible desde el fotograma 0
    if l < 4:
        pulse = math.exp(-(b % 1) * 5)
        c.text("TU MÓVIL", 90, 40, AMBER, 3, "center")
        c.text("SABE DÓNDE", 90, 74, AMBER, 3, "center")
        c.text("ESTÁS SIN", 90, 108, AMBER, 3, "center")
        c.ox = round(math.sin(b * 40) * 2 * pulse)
        c.text("INTERNET", 90, 142, gfx.mix(RED, HOT, pulse * 0.3), 3, "center")
        c.ox = 0
        phone(c, 78, 180, 24, 42)
        pin(c, 90, 206, 1.3)
        return
    c.text("¿CÓMO", 90, 44, AMBER, 3, "center")
    c.text("FUNCIONA", 90, 78, AMBER, 3, "center")
    c.text("EL GPS?", 90, 112, ORANGE, 3, "center")
    for k in range(3):
        a = b * 0.6 + k * 2.1
        satellite(c, 90 + math.cos(a) * 60, 196 + math.sin(a) * 26, 0.8)
    phone(c, 78, 172, 24, 42)
    pin(c, 90, 198, 1.3)


def s_satelites(c, l, d, b, h):
    earth(c, 90, 250, 70)
    p = gfx.ease_out_back(l * 1.5, 1.6)
    n = min(8, int(l * 1.2) + 1)
    for k in range(n):
        a = b * 0.25 + k * math.pi / 4
        x = 90 + math.cos(a) * 82
        y = 250 + math.sin(a) * 160
        if y < 236:
            satellite(c, x, y, 0.8)
    c.text("+30", 90, gfx.lerp(-40, 40, p), AMBER, 4, "center")
    c.text("SATÉLITES", 90, gfx.lerp(-40, 96, p), ORANGE, 2, "center")
    if l >= 3:
        c.line(150, 104, 150, 176, DIM)
        c.text("20.200 KM", 146, 130, AMBER, 1, "right")
    if l >= 10:
        c.text("2 VUELTAS AL DÍA", 90, 186, AMBER, 1, "center")


def s_senal(c, l, d, b, h):
    satellite(c, 90, 64, 1.4)
    phone(c, 76, 182, 28, 48)
    for k in range(4):
        r = (l * 22 + k * 30) % 100
        c.ring(90, 72, r + 6, 2, ORANGE, a=max(0, 1 - r / 100), a0=30, a1=150)
    if l >= 0.8:
        c.box(20, 92, 140, 34, PANEL, AMBER)
        c.text("SOY EL SATÉLITE 7", 90, 96, AMBER, 1, "center")
        c.text("HORA: 12:00:00,000000", 90, 110, ORANGE, 1, "center")
    if l >= 3.5:
        c.text("TU MÓVIL", 90, 136, AMBER, 2, "center")
        c.text("SOLO ESCUCHA", 90, 154, RED, 2, "center")


def s_tiempo(c, l, d, b, h):
    satellite(c, 30, 60, 1.0)
    phone(c, 140, 170, 24, 42)
    t = gfx.clamp01((l - 1) / 5)
    x = gfx.lerp(40, 150, t)
    y = gfx.lerp(70, 176, t)
    for i in range(12):
        f = max(0.0, t - i * 0.02)
        c.rect(gfx.lerp(40, 150, f), gfx.lerp(70, 176, f), 3, 3, AMBER, a=1 - i / 12)
    if t < 1:
        c.rect(x - 2, y - 2, 5, 5, HOT)
    c.text(f"0,{int(67 * t):03d} S", 90, 104, AMBER if t >= 1 else ORANGE, 3, "center")
    if l >= 0.5:
        c.text("TIEMPO x VELOCIDAD", 90, 140, ORANGE, 1, "center")
        c.text("DE LA LUZ", 90, 152, ORANGE, 1, "center")
        if l >= 4:
            c.text("= DISTANCIA", 90, 214, AMBER, 2, "center")


SATS = [(40, 120, 58), (138, 104, 66), (92, 196, 52)]


def s_circulos(c, l, d, b, h):
    px, py = 92, 144
    for k, (x, y, r) in enumerate(SATS):
        st = 0.3 + k * 1.0
        if l < st:
            continue
        e = gfx.ease_out_cubic((l - st) / 1.5)
        c.ring(x, y, r * e, 2, AMBER if k == 2 else ORANGE, a0=-180, a1=180)
        satellite(c, x, y, 0.6)
    c.text("1 DISTANCIA = 1 CÍRCULO", 90, 46, ORANGE, 1, "center")
    if l >= 4.5:
        pin(c, px, py + 4, 1.4)
        c.text("¡AQUÍ ESTÁS!", 90, 218, RED, 2, "center")


def s_cuarto(c, l, d, b, h):
    for k, (x, y) in enumerate(((30, 70), (90, 56), (150, 70))):
        satellite(c, x, y, 0.7)
    if l >= 2:
        p = gfx.ease_out_back((l - 2) * 2, 2)
        satellite(c, 90, gfx.lerp(-20, 96, p), 0.9, HOT)
        c.text("EL 4", 112, gfx.lerp(-20, 92, p), HOT, 1)
    clock(c, 90, 150, 18, b * math.pi)
    if l >= 0.3:
        c.text("1 MICROSEGUNDO", 90, 180, AMBER, 2, "center")
    if l >= 3.2:
        c.text("= 300 M DE ERROR", 90, 200, RED, 2, "center")


def s_einstein(c, l, d, b, h):
    c.text("SATÉLITE", 46, 48, ORANGE, 1, "center")
    c.text("TIERRA", 134, 48, ORANGE, 1, "center")
    clock(c, 46, 80, 20, b * math.pi * 1.06, AMBER)
    clock(c, 134, 80, 20, b * math.pi, DIM)
    if l >= 0.5:
        c.text("MENOS GRAVEDAD: +45", 90, 112, AMBER, 1, "center")
    if l >= 1.2:
        c.text("MÁS VELOCIDAD: -7", 90, 126, ORANGE, 1, "center")
    if l >= 2:
        p = gfx.ease_out_back((l - 2) * 2, 2.2)
        c.text("+0,000038 S", 90, gfx.lerp(330, 146, p), AMBER, 2, "center")
        c.text("AL DÍA", 90, gfx.lerp(330, 164, p), ORANGE, 1, "center")
    if l >= 3.9:
        c.text("SIN CORREGIR:", 90, 188, ORANGE, 1, "center")
        c.text("+10 KM AL DÍA", 90, 200, RED, 2, "center")


def s_precision(c, l, d, b, h):
    # mapa con cuadrícula y chincheta
    c.box(20, 52, 140, 150, DARK, ORANGE)
    for k in range(1, 7):
        c.rect(20 + k * 20, 52, 1, 150, PANEL)
        c.rect(20, 52 + k * 21, 140, 1, PANEL)
    c.rect(20, 120, 140, 4, DIM)
    c.rect(86, 52, 4, 150, DIM)
    bounce = abs(math.sin(b * math.pi)) * 6
    pin(c, 88, 124 - bounce, 1.6)
    if l >= 4:
        c.box(26, 172, 128, 24, PANEL, AMBER)
        c.text("SIN DATOS: OK", 90, 177, AMBER, 2, "center")
    if l >= 1.5:
        c.text("SOLO NECESITA", 90, 212, ORANGE, 1, "center")
        c.text("VER EL CIELO", 90, 224, AMBER, 2, "center")


COVER_LINES = ["¿CÓMO", "SABE EL", "GPS"]


def cover_art(c, y):
    c.text("DÓNDE ESTÁS?", 90, y - 6, ORANGE, 2, "center")
    cy = y + 46
    satellite(c, 40, cy - 14, 1.0)
    satellite(c, 140, cy - 20, 1.0)
    for k in range(3):
        c.ring(40, cy - 14, 10 + k * 9, 2, ORANGE, a=0.8 - k * 0.2, a0=0, a1=80)
        c.ring(140, cy - 20, 10 + k * 9, 2, ORANGE, a=0.8 - k * 0.2, a0=100, a1=180)
    phone(c, 76, cy - 6, 28, 46)
    pin(c, 90, cy + 26, 1.6)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 SATÉLITES", s_satelites, False),
    (24, 38, "2 SEÑAL", s_senal, False),
    (38, 52, "3 TIEMPO", s_tiempo, False),
    (52, 66, "4 CÍRCULOS", s_circulos, False),
    (66, 80, "5 EL CUARTO", s_cuarto, False),
    (80, 100, "6 EINSTEIN", s_einstein, False),
    (100, 116, "7 SIN DATOS", s_precision, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = [
    (0, "TU MÓVIL SABE DÓNDE", 0.5), (2, "ESTÁS SIN INTERNET", 0.5), (4, "¿CÓMO FUNCIONA EL GPS?", 0.6),
    (8, "MÁS DE 30", 1), (10, "SATÉLITES", 1), (12, "A 20.200 KM", 1), (15, "DE ALTURA", 1),
    (18, "DAN 2 VUELTAS", 1), (21, "AL DÍA", 1),
    (24, "CADA UNO GRITA", 1), (27, "QUIÉN ES", 1), (29, "Y SU HORA EXACTA", 1),
    (33, "TU MÓVIL", 1), (35, "SOLO ESCUCHA", 1),
    (38, "LA SEÑAL TARDA", 1), (41, "7 CENTÉSIMAS", 1),
    (45, "TIEMPO POR VELOCIDAD", 1), (48, "DE LA LUZ = DISTANCIA", 0.8),
    (52, "CADA DISTANCIA", 1), (55, "ES UN CÍRCULO", 1),
    (58, "TRES CÍRCULOS", 1), (61, "SE CRUZAN EN", 1), (63, "UN PUNTO: TÚ", 0.8),
    (66, "UN CUARTO SATÉLITE", 1), (69, "CORRIGE EL RELOJ", 1), (72, "DE TU MÓVIL", 1),
    (74, "1 MICROSEGUNDO", 1), (76.5, "= 300 METROS", 1),
    (80, "Y AQUÍ ENTRA", 1), (82, "EINSTEIN", 1),
    (83, "EN EL SATÉLITE", 1), (86, "EL TIEMPO VA MÁS RÁPIDO", 0.6),
    (89, "+38 MICROSEGUNDOS", 1), (91, "AL DÍA", 1),
    (93, "SIN CORREGIRLO", 1), (95, "+10 KM DE ERROR", 1), (97.5, "CADA DÍA", 0.8),
    (100, "Y NO GASTA DATOS:", 1), (103, "SOLO ESCUCHA", 1),
    (106, "EL MAPA SÍ", 1), (108, "HAY QUE DESCARGARLO", 0.8),
    (110, "SOLO NECESITA", 1), (112, "VER EL CIELO", 1),
]

SFX = (
    [(0, "power_up"), (1, "error"), (2, "error"), (3, "error"), (4, "whoosh"), (4.2, "blip_up"), (5, "ping")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(8.8 + k * 0.83, "blip_up") for k in range(8)] + [(11, "sweep_up"), (18, "ding")]
    + [(25, "ping"), (26, "bits"), (28, "bits"), (27.5, "ping"), (33, "power_down")]
    + [(39, "send"), (40, "tick"), (41, "tick"), (42, "tick"), (43, "tick"), (44, "ding"), (45, "sweep_up")]
    + [(52.3, "sweep_up"), (53.3, "sweep_up"), (54.3, "sweep_up"), (56.5, "ding"), (57, "power_up")]
    + [(68, "power_up"), (66.3, "blip"), (69.2, "error")]
    + [(81, "blip_up"), (83, "ping"), (86, "ping"), (82, "power_up"), (83.9, "error"), (84.4, "error")]
    + [(101, "thud"), (103, "ding"), (101.6, "power_up")]
    + outro_sfx(116)
)

# Voz en off (compacta para que los créditos lleguen a todos los vídeos del mes)
VOICE = [
    (0, "[intrigado] Tu móvil sabe dónde estás… ¡sin internet!"),
    (8, "Más de treinta satélites, a veinte mil kilómetros."),
    (24, "[misterioso] Cada uno dice su hora exacta. Tu móvil solo escucha."),
    (38, "Tiempo por velocidad de la luz… distancia."),
    (52, "[cómplice] Tres distancias se cruzan en un punto: ¡tú!"),
    (66, "Un microsegundo de error son trescientos metros."),
    (80, "[asombrado] Y por Einstein, sin corregir, ¡diez kilómetros de error al día!"),
    (100, "[sereno] Solo necesita ver el cielo."),
    (116, "[alegre] ¡Sígueme para más datos curiosos!"),
]
