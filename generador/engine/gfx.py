"""Gráficos pixel-art sobre un lienzo de 180x320, fondo de placa base y post CRT."""
import math
import numpy as np
from . import font

W, H = 180, 320
SCALE = 6
OUT_W, OUT_H = W * SCALE, H * SCALE

# Paleta oscura + naranjas/ámbar (sin azules ni blancos puros)
BG = (14, 9, 6)
DARK = (34, 20, 11)
PANEL = (48, 28, 14)
TRACE = (62, 36, 17)
DIM = (110, 62, 26)
ORANGE = (255, 138, 28)
AMBER = (255, 192, 64)
RED = (222, 52, 30)
HOT = (255, 232, 170)  # solo para destellos


def lerp(a, b, t):
    return a + (b - a) * t


def clamp01(t):
    return max(0.0, min(1.0, t))


def ease_out_back(t, s=1.70158):
    t = clamp01(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def ease_out_cubic(t):
    t = clamp01(t)
    return 1 - (1 - t) ** 3


def ease_in_cubic(t):
    t = clamp01(t)
    return t ** 3


def ease_in_out(t):
    t = clamp01(t)
    return 3 * t * t - 2 * t * t * t


def bounce(t):
    """Rebote: sube con exceso y se asienta (0->1)."""
    t = clamp01(t)
    return 1 - math.cos(t * math.pi * 2.5) * math.exp(-5 * t) if t < 1 else 1.0


def mix(c1, c2, t):
    return tuple(lerp(a, b, clamp01(t)) for a, b in zip(c1, c2))


class Canvas:
    """Lienzo float32 (H, W, 3). Todas las coordenadas se desplazan por (ox, oy)."""

    def __init__(self, img):
        self.img = img
        self.ox = 0
        self.oy = 0

    def _clip(self, x, y, w, h):
        x = int(round(x + self.ox)); y = int(round(y + self.oy))
        w = int(round(w)); h = int(round(h))
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(W, x + w), min(H, y + h)
        return x0, y0, x1, y1

    def rect(self, x, y, w, h, col, a=1.0):
        x0, y0, x1, y1 = self._clip(x, y, w, h)
        if x1 <= x0 or y1 <= y0 or a <= 0:
            return
        reg = self.img[y0:y1, x0:x1]
        if a >= 1:
            reg[:] = col
        else:
            reg[:] = reg * (1 - a) + np.array(col, np.float32) * a

    def frame(self, x, y, w, h, col, t=1, a=1.0):
        self.rect(x, y, w, t, col, a)
        self.rect(x, y + h - t, w, t, col, a)
        self.rect(x, y + t, t, h - 2 * t, col, a)
        self.rect(x + w - t, y + t, t, h - 2 * t, col, a)

    def box(self, x, y, w, h, fill, border, t=1, a=1.0):
        self.rect(x, y, w, h, fill, a)
        self.frame(x, y, w, h, border, t, a)

    def px(self, x, y, col, a=1.0, s=1):
        self.rect(x, y, s, s, col, a)

    def line(self, x0, y0, x1, y1, col, a=1.0, t=1):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n):
            f = i / max(1, n - 1)
            self.rect(round(lerp(x0, x1, f)), round(lerp(y0, y1, f)), t, t, col, a)

    def ring(self, cx, cy, r, thick, col, a=1.0, a0=-180, a1=0):
        """Arco de anillo pixelado entre los ángulos a0..a1 (grados, 0=derecha, -90=arriba)."""
        if r <= 0 or a <= 0:
            return
        R = int(r + thick + 1)
        x0, y0, x1, y1 = self._clip(cx - R, cy - R, 2 * R + 1, 2 * R + 1)
        if x1 <= x0 or y1 <= y0:
            return
        ys, xs = np.mgrid[y0:y1, x0:x1]
        dx = xs - (cx + self.ox); dy = ys - (cy + self.oy)
        d = np.sqrt(dx * dx + dy * dy)
        ang = np.degrees(np.arctan2(dy, dx))
        m = (d >= r) & (d < r + thick) & (ang >= a0) & (ang <= a1)
        if not m.any():
            return
        reg = self.img[y0:y1, x0:x1]
        reg[m] = reg[m] * (1 - a) + np.array(col, np.float32) * a

    def disc(self, cx, cy, r, col, a=1.0):
        R = int(r + 1)
        x0, y0, x1, y1 = self._clip(cx - R, cy - R, 2 * R + 1, 2 * R + 1)
        if x1 <= x0 or y1 <= y0:
            return
        ys, xs = np.mgrid[y0:y1, x0:x1]
        m = (xs - (cx + self.ox)) ** 2 + (ys - (cy + self.oy)) ** 2 <= r * r
        reg = self.img[y0:y1, x0:x1]
        reg[m] = reg[m] * (1 - a) + np.array(col, np.float32) * a

    def text(self, s, x, y, col, scale=1, align="left", a=1.0, shadow=True):
        s = s.upper()
        w = font.text_width(s, scale)
        if align == "center":
            x = x - w / 2
        elif align == "right":
            x = x - w
        x = round(x); y = round(y)
        if shadow:
            self._text(s, x + scale, y + scale, BG, scale, a)
        self._text(s, x, y, col, scale, a)
        return w

    def _text(self, s, x, y, col, scale, a):
        cx = x
        colv = np.array(col, np.float32)
        for ch in s:
            m = font.glyph(ch)
            if scale > 1:
                m = np.repeat(np.repeat(m, scale, 0), scale, 1)
            h, w = m.shape
            X0 = int(cx + self.ox); Y0 = int(y + self.oy)
            x0, y0 = max(0, X0), max(0, Y0)
            x1, y1 = min(W, X0 + w), min(H, Y0 + h)
            if x1 > x0 and y1 > y0:
                sub = m[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0]
                reg = self.img[y0:y1, x0:x1]
                reg[sub] = reg[sub] * (1 - a) + colv * a
            cx += (m.shape[1] // scale + 1) * scale

    def sprite(self, rows, x, y, pal, scale=1, a=1.0):
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c in pal:
                    self.rect(x + i * scale, y + j * scale, scale, scale, pal[c], a)


# ---------- fondo de placa base ----------

def make_board(seed=7):
    rng = np.random.default_rng(seed)
    mask = np.zeros((H, W), bool)
    phase = np.zeros((H, W), np.float32)
    pads = np.zeros((H, W), bool)
    for _ in range(46):
        x = int(rng.integers(2, W // 4)) * 4
        y = int(rng.integers(2, H // 4)) * 4
        dist = 0
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        d = dirs[int(rng.integers(4))]
        start = (x, y)
        for _seg in range(int(rng.integers(2, 6))):
            L = int(rng.integers(3, 14)) * 4
            for _ in range(L):
                if 0 <= x < W and 0 <= y < H:
                    mask[y, x] = True
                    phase[y, x] = dist
                x += d[0]; y += d[1]; dist += 1
            d = dirs[int(rng.integers(4))] if rng.random() < 0.7 else d
        for (px_, py_) in (start, (x, y)):
            if 2 <= px_ < W - 2 and 2 <= py_ < H - 2:
                pads[py_ - 1:py_ + 2, px_ - 1:px_ + 2] = True
    # chips decorativos
    chips = np.zeros((H, W), bool)
    for _ in range(5):
        cx = int(rng.integers(10, W - 30)); cy = int(rng.integers(10, H - 30))
        w = int(rng.integers(12, 26)); h = int(rng.integers(8, 16))
        chips[cy:cy + h, cx:cx + w] = True
        chips[cy + 1:cy + h - 1, cx + 1:cx + w - 1] = False
    return mask, phase, pads, chips


class Board:
    def __init__(self, seed=7):
        self.mask, self.phase, self.pads, self.chips = make_board(seed)
        self.base = np.empty((H, W, 3), np.float32)
        self.base[:] = BG

    def draw(self, t_sec, pulse):
        img = self.base.copy()
        lum = 0.45 + 0.9 * pulse
        tr = np.array(TRACE, np.float32) * lum
        img[self.mask] = tr
        img[self.chips] = np.array(TRACE, np.float32) * 0.8
        img[self.pads] = np.array(DIM, np.float32) * (0.5 + 0.6 * pulse)
        # señales que recorren las pistas
        run = ((self.phase - t_sec * 70.0) % 90.0) < 5
        m = self.mask & run
        img[m] = np.array(ORANGE, np.float32) * (0.35 + 0.4 * pulse)
        return img


# ---------- post CRT ----------

class CRT:
    def __init__(self):
        yy = np.arange(OUT_H)[:, None]
        xx = np.arange(OUT_W)[None, :]
        scan = np.where((yy % SCALE) >= SCALE - 2, 0.62, 1.0).astype(np.float32)
        nx = (xx / OUT_W - 0.5) * 2
        ny = (yy / OUT_H - 0.5) * 2
        vig = np.clip(1.0 - 0.38 * (nx ** 2 * 0.9 + ny ** 2 * 0.55) ** 1.4, 0, 1).astype(np.float32)
        self.mask = (scan * vig)[:, :, None]
        self.shift = 3  # aberración cromática leve (px a resolución final)

    def apply(self, low):
        up = np.repeat(np.repeat(low, SCALE, 0), SCALE, 1)
        up = up * self.mask
        s = self.shift
        out = up.copy()
        out[:, s:, 0] = up[:, :-s, 0]
        out[:, :-s, 2] = up[:, s:, 2]
        return np.clip(out, 0, 255).astype(np.uint8)
