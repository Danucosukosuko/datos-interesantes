"""Timeline en BEATS compartida por vídeo y música. Dibuja cada fotograma,
aplica motion blur por supersampling temporal, post CRT y envía rawvideo a ffmpeg."""
import math
import subprocess
import numpy as np
from PIL import Image

from . import gfx, audio
from .gfx import Canvas, W, H, OUT_W, OUT_H
from . import font

FPS = 30
DUR = 60.0
BPS = audio.BPM / 60.0


class Video:
    def __init__(self, topic):
        self.T = topic
        self.board = gfx.Board(getattr(topic, "BOARD_SEED", 7))
        self.crt = gfx.CRT()
        self.scenes = topic.SCENES
        self.subs = sorted(topic.SUBS, key=lambda s: s[0])
        self.sfx = sorted(topic.SFX, key=lambda s: s[0])
        self.sfx_beats = np.array([s[0] for s in self.sfx], np.float32)
        self.sfx_w = np.array([0.4 if k in ("tick", "blip", "bit0", "bit1") else 1.0
                               for _, k in self.sfx], np.float32)

    # ---------- utilidades de timeline ----------
    def scene_index(self, b):
        for i, sc in enumerate(self.scenes):
            if sc[0] <= b < sc[1]:
                return i
        return len(self.scenes) - 1

    def hit(self, b):
        d = b - self.sfx_beats
        m = (d >= 0) & (d < 1.5)
        if not m.any():
            return 0.0
        return float(min(1.0, (np.exp(-d[m] * 7) * self.sfx_w[m]).sum()))

    def samples_for(self, b):
        i = self.scene_index(b)
        s, e = self.scenes[i][0], self.scenes[i][1]
        fast = self.scenes[i][4] if len(self.scenes[i]) > 4 else False
        if b - s < 1.0 or e - b < 0.6:
            return 8          # transiciones: más submuestras
        if fast:
            return 5          # bucles veloces
        return 2

    # ---------- dibujo ----------
    def draw(self, t):
        b = t * BPS
        frac = b - math.floor(b)
        pulse = math.exp(-frac * 5.0)
        img = self.board.draw(t, pulse)
        c = Canvas(img)
        i = self.scene_index(b)
        s, e, header, fn = self.scenes[i][:4]
        local = b - s
        last = i == len(self.scenes) - 1
        # entrada (desliza con rebote) / salida (acelera fuera)
        ox = 0.0
        if local < 1.0 and i > 0:
            ox = (1 - gfx.ease_out_back(local / 1.0, 1.4)) * W * (1 if i % 2 else -1)
        if not last and e - b < 0.5:
            ox = -gfx.ease_in_cubic((0.5 - (e - b)) / 0.5) * W * (1 if i % 2 == 0 else -1)
        h = self.hit(b)
        c.ox = ox
        c.oy = round(math.sin(b * 37.0) * h * 1.6)
        fn(c, local, e - s, b, h)
        c.ox = 0; c.oy = 0
        self.draw_header(c, header, i, local)
        self.draw_subs(c, b, s, e)
        # barra de progreso inferior
        c.rect(0, H - 3, W, 3, gfx.DARK)
        c.rect(0, H - 3, W * b / audio.BEATS, 3, gfx.ORANGE)
        if h > 0:
            img += h * 16.0
        return img

    def draw_header(self, c, header, i, local):
        if not header:
            return
        y = gfx.lerp(-30, 6, gfx.ease_out_back(local * 1.5, 2.0))
        w = font.text_width(header, 2)
        c.box(90 - w / 2 - 7, y, w + 14, 24, gfx.DARK, gfx.ORANGE)
        c.text(header, 90, y + 1, gfx.AMBER, 2, "center")
        n = len(self.scenes)
        c.text(f"{i + 1:02d}/{n:02d}", 176, 36, gfx.DIM, 1, "right", shadow=False)

    def draw_subs(self, c, b, s, e):
        cur = None
        for st, txt, step in self.subs:
            if s <= st <= b + 0.25 and st < e:
                cur = (st, txt, step)
        if cur is None:
            return
        st, txt, step = cur
        words = txt.split()
        sc = 2
        space = (font.glyph(" ").shape[1] + 1) * sc
        maxw = 162
        lines, line, lw = [], [], 0
        for k, wd in enumerate(words):
            ww = font.text_width(wd, sc)
            add = ww if not line else lw + space + ww
            if line and add > maxw:
                lines.append((line, lw)); line, lw = [(k, wd, ww)], ww
            else:
                line.append((k, wd, ww)); lw = add
        if line:
            lines.append((line, lw))
        lh = 24
        boxh = len(lines) * lh + 10
        y0 = 300 - boxh
        appear = gfx.ease_out_back((b - st + 0.25) * 3, 1.5)
        c.oy = round((1 - appear) * 30)
        c.box(5, y0, 170, boxh, gfx.PANEL, gfx.ORANGE, a=0.9)
        c.frame(5, y0, 170, boxh, gfx.ORANGE)
        active = min(len(words) - 1, int(math.floor((b - st) / step))) if b >= st else -1
        for li, (ln, lw) in enumerate(lines):
            x = 90 - lw / 2
            y = y0 + 4 + li * lh
            for k, wd, ww in ln:
                wb = st + k * step
                if k == active:
                    pop = max(0.0, 1 - (b - wb) / 0.35)
                    col = gfx.mix(gfx.ORANGE, gfx.HOT, pop)
                    c.rect(x - 2, y + 4, ww + 4, 18, col)
                    c.text(wd, x, y - round(pop * 2), gfx.BG, sc, shadow=False)
                elif k < active or (k == active):
                    c.text(wd, x, y, gfx.ORANGE, sc)
                else:
                    c.text(wd, x, y, gfx.DIM, sc)
                x += ww + space
        c.oy = 0

    def frame(self, f):
        t = f / FPS
        n = self.samples_for(t * BPS)
        if n == 1:
            low = self.draw(t)
        else:
            acc = np.zeros((H, W, 3), np.float32)
            for k in range(n):
                acc += self.draw(t + ((k + 0.5) / n - 0.5) / FPS)
            low = acc / n
        return self.crt.apply(low)

    # ---------- salidas ----------
    def preview(self, path, beats, cols=6):
        tiles = []
        for b in beats:
            f = int(round(b / BPS * FPS))
            img = Image.fromarray(self.frame(f)).resize((216, 384), Image.LANCZOS)
            tiles.append(img)
        rows = math.ceil(len(tiles) / cols)
        sheet = Image.new("RGB", (cols * 216, rows * 384), (0, 0, 0))
        for k, im in enumerate(tiles):
            sheet.paste(im, ((k % cols) * 216, (k // cols) * 384))
        sheet.save(path)
        return path

    def render(self, out_mp4, wav_path):
        audio.render(self.sfx, wav_path, getattr(self.T, "MUSIC_SEED", 1), getattr(self.T, "MUSIC_KEY", 57))
        cmd = ["ffmpeg", "-y", "-loglevel", "error",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OUT_W}x{OUT_H}", "-r", str(FPS), "-i", "-",
               "-i", wav_path,
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.3f}", "-movflags", "+faststart", out_mp4]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        total = int(DUR * FPS)
        for f in range(total):
            p.stdin.write(self.frame(f).tobytes())
            if f % 150 == 0:
                print(f"  fotograma {f}/{total}", flush=True)
        p.stdin.close()
        p.wait()
        if p.returncode:
            raise RuntimeError("ffmpeg falló")
        return out_mp4
