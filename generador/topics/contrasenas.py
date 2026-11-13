"""Tema: ¿Cómo se guardan las contraseñas? (tecnología)

Datos verificados (13-nov-2026; OWASP Password Storage Cheat Sheet, Auth0, WorkOS, Authgear,
ExpressVPN; NordPass vía WeLiveSecurity, Xataka Móvil, Bankinter):
- Las webs bien hechas (Google incluida) no guardan tu contraseña: guardan su hash, una «huella»
  que sale de pasarla por una función matemática de un solo sentido (bcrypt, scrypt, Argon2id,
  PBKDF2). Del hash no se puede sacar la contraseña.
- Al iniciar sesión, la web calcula el hash de lo que escribes y lo compara con el guardado.
- La sal: datos al azar distintos para cada usuario que se mezclan antes del hash; así dos
  contraseñas iguales dan hashes distintos y no sirven las tablas precalculadas.
- Si roban la base de datos se llevan hashes, pero pueden probar millones de contraseñas por
  segundo: las débiles caen enseguida.
- NordPass: en España en 2025 las más usadas fueron «admin» y «123456»; se descifran en menos de
  un segundo.
- Si una web puede enviarte tu contraseña tal cual, es que no la guarda como hash: mala señal.
"""
import math
from engine import gfx
from engine.outro import s_outro, outro_sfx
from engine.gfx import ORANGE, AMBER, DIM, DARK, PANEL, RED, HOT

TITLE = "¿Cómo se guardan las contraseñas?"
MUSIC_SEED = 20261113
MUSIC_KEY = 52
BOARD_SEED = 131

HEXCH = "0123456789ABCDEF"


def hexstr(seed, n=12):
    out = ""
    x = seed * 2654435761 % 4294967296
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out += HEXCH[(x >> 16) % 16]
    return out


def pwbox(c, x, y, w, text, col=AMBER, stars=False):
    c.box(x, y, w, 18, PANEL, col)
    c.text("*" * len(text) if stars else text, x + w / 2, y + 5, col, 1, "center", shadow=False)


def padlock(c, cx, cy, s=1.0, col=AMBER, open_=0.0):
    c.ring(cx, cy - 8 * s - open_ * 6 * s, 7 * s, max(1, int(2 * s)), col, a0=-180, a1=0)
    c.rect(cx - 7 * s, cy - 8 * s - open_ * 6 * s, 2 * s, 8 * s * (1 - open_) + 1, col)
    c.rect(cx + 5 * s, cy - 8 * s - open_ * 6 * s, 2 * s, 8 * s + 1, col)
    c.box(cx - 10 * s, cy - 2 * s, 20 * s, 16 * s, col, DARK)
    c.rect(cx - 1 * s, cy + 3 * s, 2 * s, 5 * s, DARK)


def grinder(c, cx, cy, b, on=True):
    """Picadora: tolva arriba, engranajes en medio, salida abajo."""
    for i in range(14):
        w = 34 - i * 1.3
        c.rect(cx - w, cy - 34 + i, w * 2, 1, PANEL)
    c.box(cx - 22, cy - 20, 44, 34, PANEL, ORANGE, t=2)
    for k, gx in enumerate((cx - 9, cx + 9)):
        a0 = (b * 3 if on else 0) * (1 if k == 0 else -1)
        c.disc(gx, cy - 3, 6, DIM)
        for t in range(6):
            a = a0 + t * math.pi / 3
            c.line(gx, cy - 3, gx + math.cos(a) * 9, cy - 3 + math.sin(a) * 9, AMBER, t=2)
    c.rect(cx - 6, cy + 14, 12, 6, ORANGE)


def shaker(c, cx, cy, s=1.0):
    c.box(cx - 8 * s, cy - 6 * s, 16 * s, 22 * s, PANEL, AMBER)
    c.box(cx - 8 * s, cy - 12 * s, 16 * s, 6 * s, ORANGE, ORANGE)
    for k in range(3):
        c.rect(cx - 5 * s + k * 4 * s, cy - 11 * s, s, s, DARK)
    c.text("SAL", cx, cy + 1 * s, AMBER, 1, "center", shadow=False)


# ---------- escenas ----------

def s_title(c, l, d, b, h):
    pulse = math.exp(-(b % 1) * 5)
    if l < 5.0:
        c.text("NI GOOGLE", 90, 36, AMBER, 3, "center")
        c.text("SABE TU", 90, 68, AMBER, 3, "center")
        c.text("CONTRASEÑA", 90, 100, gfx.mix(RED, HOT, pulse * 0.35), 3, "center")
        pwbox(c, 40, 150, 100, "MICLAVE123", stars=True)
        padlock(c, 90, 214, 1.6, gfx.mix(AMBER, HOT, pulse * 0.4))
        return
    c.text("¿CÓMO", 90, 40, AMBER, 3, "center")
    c.text("GUARDAN", 90, 72, ORANGE, 3, "center")
    c.text("TU CLAVE?", 90, 104, ORANGE, 3, "center")
    padlock(c, 90, 196, 1.8)


T_GRIND, T_CODE, T_HASH = 1.9, 5.6, 8.1


def s_picadora(c, l, d, b, h):
    pwbox(c, 40, 40, 100, "MICLAVE123")
    if l >= T_GRIND:
        f = gfx.clamp01((l - T_GRIND) / 1.2)
        c.text("MICLAVE123", 90, gfx.lerp(62, 92, f), AMBER, 1, "center", a=1 - f)
    grinder(c, 90, 128, b, on=l >= T_GRIND)
    if l >= T_CODE:
        n = min(12, int((l - T_CODE) * 8) + 1)
        c.box(26, 162, 128, 18, DARK, ORANGE)
        c.text(hexstr(7)[:n], 90, 167, ORANGE, 1, "center", shadow=False)
    if l >= T_HASH:
        c.text("EL HASH", 90, 192, RED, 3, "center")


T_BACK = 2.4


def s_sin_vuelta(c, l, d, b, h):
    c.box(26, 50, 128, 18, DARK, ORANGE)
    c.text(hexstr(7), 90, 55, ORANGE, 1, "center", shadow=False)
    c.line(90, 74, 90, 118, AMBER, t=2)
    c.line(84, 80, 90, 74, AMBER, t=2)
    c.line(96, 80, 90, 74, AMBER, t=2)
    pwbox(c, 40, 124, 100, "?????????")
    if l >= T_BACK:
        q = gfx.clamp01((l - T_BACK) / 0.6)
        c.line(70, 82, 70 + 40 * q, 112 * q + 82 * (1 - q), RED, t=3)
        c.line(110, 82, 110 - 40 * q, 112 * q + 82 * (1 - q), RED, t=3)
        c.text("SIN MARCHA", 90, 170, RED, 2, "center")
        c.text("ATRÁS", 90, 188, RED, 2, "center")


T_TYPE, T_CMP, T_OK = 1.3, 3.4, 8.3


def s_entrar(c, l, d, b, h):
    typed = "MICLAVE123"[:max(0, min(10, int((l - T_TYPE) * 6)))]
    pwbox(c, 40, 40, 100, typed, stars=True)
    if l >= T_CMP:
        c.text("TU HASH", 50, 80, AMBER, 1, "center")
        c.text("GUARDADO", 130, 80, AMBER, 1, "center")
        c.box(8, 92, 84, 16, DARK, ORANGE)
        c.text(hexstr(7)[:8], 50, 96, ORANGE, 1, "center", shadow=False)
        c.box(88, 92, 84, 16, DARK, ORANGE)
        c.text(hexstr(7)[:8], 130, 96, ORANGE, 1, "center", shadow=False)
        c.text("=", 90, 116, AMBER, 3, "center")
    if l >= T_OK:
        padlock(c, 90, 190, 1.4, AMBER, open_=gfx.clamp01((l - T_OK) / 0.5))
        c.text("¡DENTRO!", 90, 216, AMBER, 2, "center")


T_SAL, T_DOS, T_DIFF = 1.3, 4.8, 7.4


def s_sal(c, l, d, b, h):
    if l >= T_SAL:
        shaker(c, 90, 64, 1.3)
        for k in range(5):
            f = ((l * 1.2) + k / 5) % 1
            c.rect(84 + (k % 3) * 5, 84 + f * 18, 1, 1, AMBER)
    for k, (x, salt) in enumerate(((46, 3), (134, 11))):
        if l < T_DOS:
            continue
        pwbox(c, x - 40, 108, 80, "123456")
        if l >= T_DIFF:
            c.box(x - 40, 150, 80, 18, DARK, ORANGE)
            c.text(hexstr(salt)[:9], x, 155, ORANGE, 1, "center", shadow=False)
            c.line(x, 128, x, 146, DIM, t=1)
    if l >= T_DIFF + 0.5:
        c.text("¡DISTINTOS!", 90, 182, RED, 2, "center")


T_ROBO, T_COD, T_PRUEBA = 0.4, 2.8, 5.5


def s_robo(c, l, d, b, h):
    if l >= T_ROBO:
        for k in range(5):
            c.box(28, 44 + k * 16, 124, 14, DARK, DIM)
            c.text(hexstr(20 + k)[:12], 90, 48 + k * 16, ORANGE, 1, "center", shadow=False)
    if l >= T_COD:
        c.text("SOLO CÓDIGOS", 90, 130, AMBER, 1, "center")
    if l >= T_PRUEBA:
        n = int(min(1, (l - T_PRUEBA) / 3) * 9_999_999)
        c.text(f"{n:,}".replace(",", "."), 90, 156, RED, 3, "center")
        c.text("PRUEBAS POR SEGUNDO", 90, 190, ORANGE, 1, "center")


T_ADMIN, T_123, T_SEG = 0.7, 2.3, 6.9


def s_peores(c, l, d, b, h):
    c.text("LAS MÁS USADAS", 90, 40, AMBER, 1, "center")
    c.text("EN ESPAÑA", 90, 52, AMBER, 1, "center")
    for k, (st, word) in enumerate(((T_ADMIN, "ADMIN"), (T_123, "123456"))):
        if l < st:
            continue
        p = gfx.ease_out_back((l - st) * 2.5, 2)
        c.box(30, 70 + k * 40, 120, 30, PANEL, RED)
        c.text(f"{k + 1}", 42, 77 + k * 40, AMBER, 2, "center", shadow=False)
        c.text(word, 98, 77 + k * 40, gfx.mix(DIM, AMBER, p), 2, "center", shadow=False)
    if l >= T_SEG:
        c.text("MENOS DE", 90, 158, RED, 2, "center")
        c.text("1 SEGUNDO", 90, 176, RED, 3, "center")
    c.text("(NORDPASS 2025)", 90, 212, DIM, 1, "center")


T_FRASE, T_WEB, T_DESC = 2.2, 5.5, 10.4


def s_truco(c, l, d, b, h):
    if l >= T_FRASE:
        c.text("USA UNA FRASE", 90, 42, AMBER, 2, "center")
        c.box(10, 62, 160, 18, PANEL, AMBER)
        c.text("MI-GATO-COME-PIZZA-7", 90, 67, AMBER, 1, "center", shadow=False)
    if l >= T_WEB:
        c.box(18, 104, 144, 60, PANEL, RED)
        c.text("SI UNA WEB", 90, 112, AMBER, 2, "center")
        c.text("TE REENVÍA", 90, 128, AMBER, 2, "center")
        c.text("TU CLAVE...", 90, 144, AMBER, 2, "center")
        if l >= T_DESC:
            c.box(26, 176, 128, 26, RED, RED)
            c.text("¡DESCONFÍA!", 90, 182, HOT, 2, "center", shadow=False)


COVER_LINES = ["¿DÓNDE", "GUARDAN", "TU CLAVE?"]


def cover_art(c, y):
    padlock(c, 90, y + 46, 2.2)


SCENES = [
    (0, 8, None, s_title, False),
    (8, 24, "1 LA PICADORA", s_picadora, False),
    (24, 38, "2 SIN VUELTA", s_sin_vuelta, False),
    (38, 52, "3 AL ENTRAR", s_entrar, True),
    (52, 66, "4 LA SAL", s_sal, True),
    (66, 80, "5 SI LA ROBAN", s_robo, False),
    (80, 100, "6 LAS PEORES", s_peores, False),
    (100, 116, "7 EL TRUCO", s_truco, False),
    (116, 128, "FIN", s_outro, False),
]

SUBS = []   # con voz se generan solos

VOICE = [
    (0, "[misterioso] Ni Google sabe tu contraseña… ¡de verdad!"),
    (8, "[narrando] Al crearla, una picadora matemática la convierte en un código raro: el hash."),
    (24, "[cómplice] Y esa picadora no tiene marcha atrás: del código no se saca tu contraseña."),
    (38, "Cuando entras, pica lo que escribes y compara los dos códigos. ¿Iguales? ¡Dentro!"),
    (52, "[pensativo] Y le añaden sal: algo al azar, para que dos contraseñas iguales no se parezcan."),
    (66, "[serio] Si roban la web, se llevan códigos… pero prueban millones por segundo."),
    (80, "[sorprendido] Por eso admin o uno, dos, tres, cuatro, cinco, seis caen en menos de un segundo."),
    (100, "[cómplice] El truco: usa frases largas. Y si una web te reenvía tu contraseña… ¡desconfía!"),
    (116, "[alegre] ¡Sígueme para más datos curiosos!"),
]

SFX = (
    [(0, "power_up"), (1, "blip"), (2, "blip"), (3, "blip"), (4.6, "whoosh"), (4.8, "blip_up"), (5.6, "ding")]
    + [(s, "whoosh") for s in (8, 24, 38, 52, 66, 80, 100)]
    + [(8 + T_GRIND, "bits"), (8 + T_CODE, "blip_up"), (8 + T_HASH, "ding")]
    + [(24 + T_BACK, "error")]
    + [(38 + T_TYPE + k * 0.17, "tick") for k in range(10)] + [(38 + T_CMP, "ping"), (38 + T_OK, "power_up"), (38 + 6.2, "blip")]
    + [(52 + T_SAL, "sweep_fast"), (52 + T_DOS, "blip_up"), (52 + T_DIFF, "ping")]
    + [(66 + T_ROBO, "send"), (66 + T_COD, "blip"), (66 + T_PRUEBA, "bits")]
    + [(80 + T_ADMIN, "thud"), (80 + T_123, "thud"), (80 + T_SEG, "error")]
    + [(100 + T_FRASE, "blip_up"), (100 + T_WEB, "ping"), (100 + T_DESC, "error")]
    + outro_sfx(116)
)
