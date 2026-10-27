"""Chiptune sintetizado a mano con numpy: pulso con duty, triángulo de 4 bits,
ruido LFSR tipo NES y batería por síntesis. 128 BPM, 32 compases = 60 s."""
import wave
import numpy as np

SR = 44100
BPM = 128
BEATS = 128
SPB = 60.0 / BPM * SR           # muestras por beat (no entero)
TOTAL = int(round(BEATS * SPB))  # 2.646.000 = 60 s exactos


def b2s(beat):
    return int(round(beat * SPB))


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


# ---------- osciladores ----------

def pulse(freq, n, duty=0.5, slide=0.0):
    f = freq * (1 + slide * np.arange(n) / max(1, n)) if slide else np.full(n, freq)
    ph = np.cumsum(f / SR) % 1.0
    return np.where(ph < duty, 1.0, -1.0).astype(np.float32)


def tri4(freq, n, slide=0.0):
    f = freq * (1 + slide * np.arange(n) / max(1, n)) if slide else np.full(n, freq)
    ph = np.cumsum(f / SR) % 1.0
    tri = 1 - 4 * np.abs(ph - 0.5)            # -1..1
    return (np.round((tri + 1) * 7.5) / 7.5 - 1).astype(np.float32)  # 16 niveles


def _lfsr(short=False):
    reg = 1; out = np.empty(32767, np.float32)
    tap = 6 if short else 1
    for i in range(32767):
        bit = (reg ^ (reg >> tap)) & 1
        reg = (reg >> 1) | (bit << 14)
        out[i] = 1.0 if reg & 1 else -1.0
    return out


NOISE_LONG = _lfsr(False)
NOISE_SHORT = _lfsr(True)


def noise(n, rate=22000.0, short=False, rate_end=None):
    src = NOISE_SHORT if short else NOISE_LONG
    if rate_end is None:
        idx = (np.arange(n) * rate / SR).astype(np.int64)
    else:
        r = np.linspace(rate, rate_end, n)
        idx = np.cumsum(r / SR).astype(np.int64)
    return src[idx % len(src)]


def env(n, a=0.002, d=0.15, s=0.0, r=0.0, hold=None):
    """Envolvente simple ataque-decaimiento exponencial (+ sostenido opcional)."""
    t = np.arange(n) / SR
    e = np.minimum(1.0, t / max(a, 1e-4))
    if s > 0:
        dec = s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4) * 3)
        e = e * np.where(t < a, 1.0, dec)
        if r > 0:
            e *= np.clip((n / SR - t) / r, 0, 1)
    else:
        e = e * np.exp(-np.maximum(0, t - a) / max(d, 1e-4) * 3)
    return e.astype(np.float32)


class Track:
    def __init__(self):
        self.buf = np.zeros(TOTAL + SR * 2, np.float32)

    def add(self, beat, sig, gain=1.0):
        i = b2s(beat)
        if i < 0:
            sig = sig[-i:]; i = 0
        j = min(len(self.buf), i + len(sig))
        self.buf[i:j] += sig[:j - i] * gain


# ---------- batería ----------

def kick():
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    f = 50 + 120 * np.exp(-t * 35)
    ph = np.cumsum(f / SR)
    body = np.sin(2 * np.pi * ph) * np.exp(-t * 14)
    click = noise(n, 30000) * np.exp(-t * 300) * 0.4
    return (body + click).astype(np.float32)


def snare():
    n = int(0.2 * SR)
    t = np.arange(n) / SR
    tone = tri4(185, n) * np.exp(-t * 30) * 0.5
    nz = noise(n, 26000) * np.exp(-t * 18)
    return (tone + nz).astype(np.float32)


def hat(open_=False):
    n = int((0.16 if open_ else 0.04) * SR)
    t = np.arange(n) / SR
    return (noise(n, 44000, short=True) * np.exp(-t * (14 if open_ else 90))).astype(np.float32)


def crash():
    n = int(1.2 * SR)
    t = np.arange(n) / SR
    return (noise(n, 40000) * np.exp(-t * 3.2)).astype(np.float32)


# ---------- efectos de sonido (SFX) ----------

def sfx(kind):
    S = SR
    if kind == "blip":
        n = int(0.07 * S); return pulse(mtof(84), n, 0.25) * env(n, d=0.06)
    if kind == "blip_up":
        n = int(0.09 * S); return pulse(mtof(76), n, 0.5, slide=1.0) * env(n, d=0.08)
    if kind == "tick":
        n = int(0.03 * S); return noise(n, 40000, True) * env(n, d=0.02)
    if kind == "ding":
        n = int(0.35 * S)
        return (tri4(mtof(88), n) * 0.7 + pulse(mtof(100), n, 0.125) * 0.25) * env(n, d=0.25)
    if kind == "power_up":
        out = []
        for k, m in enumerate([60, 64, 67, 72, 76, 79, 84]):
            n = int(0.035 * S); out.append(pulse(mtof(m), n, 0.25) * (0.6 + k * 0.05))
        s = np.concatenate(out); return s * env(len(s), d=0.5, s=0.8, r=0.03)
    if kind == "power_down":
        n = int(0.32 * S); return pulse(mtof(76), n, 0.5, slide=-0.7) * env(n, d=0.3, s=0.6, r=0.05)
    if kind == "whoosh":
        n = int(0.28 * S); t = np.arange(n) / S
        return noise(n, 4000, rate_end=30000) * np.sin(np.pi * t / t[-1]) * 0.7
    if kind == "sweep_up":
        n = int(0.5 * S); return pulse(mtof(55), n, 0.125, slide=3.0) * env(n, d=0.6, s=0.7, r=0.08) * 0.8
    if kind == "sweep_fast":
        n = int(0.2 * S); return pulse(mtof(67), n, 0.25, slide=3.0) * env(n, d=0.2, s=0.7, r=0.03) * 0.8
    if kind == "ping":
        n = int(0.25 * S); return tri4(mtof(91), n) * env(n, d=0.18)
    if kind == "send":
        n = int(0.12 * S); return pulse(mtof(72), n, 0.25, slide=0.6) * env(n, d=0.1)
    if kind == "bit1":
        n = int(0.07 * S); return pulse(mtof(88), n, 0.5) * env(n, d=0.06)
    if kind == "bit0":
        n = int(0.07 * S); return pulse(mtof(76), n, 0.5) * env(n, d=0.06)
    if kind == "bits":
        rng = np.random.default_rng(3); parts = []
        for _ in range(6):
            n = int(0.03 * S); parts.append(pulse(mtof(int(rng.integers(76, 96))), n, 0.25))
        s = np.concatenate(parts); return s * env(len(s), d=0.3, s=0.8, r=0.02) * 0.8
    if kind == "thud":
        n = int(0.3 * S); t = np.arange(n) / S
        return (np.sin(2 * np.pi * np.cumsum((90 * np.exp(-t * 8) + 40) / S)) * np.exp(-t * 10)
                + noise(n, 8000) * np.exp(-t * 25) * 0.6).astype(np.float32)
    if kind == "error":
        n = int(0.18 * S); return pulse(mtof(52), n, 0.5) * env(n, d=0.15, s=0.8, r=0.02) * 0.7
    if kind == "end":
        out = []
        for m in [72, 76, 79, 84]:
            n = int(0.09 * S); out.append(pulse(mtof(m), n, 0.5))
        n = int(0.6 * S); out.append(tri4(mtof(84), n) * env(n, d=0.5) + pulse(mtof(96), n, 0.125) * env(n, d=0.4) * 0.3)
        s = np.concatenate(out); return s * 0.8
    raise ValueError(kind)


SFX_GAIN = {"tick": 0.25, "blip": 0.2, "whoosh": 0.35, "bit1": 0.2, "bit0": 0.2}

# ---------- composición ----------

MINOR = [0, 2, 3, 5, 7, 8, 10]


def chord_tones(root, quality):
    return [root, root + (3 if quality == "m" else 4), root + 7]


def compose(seed=1, key=57):
    """Devuelve la pista de música (sin SFX). key = nota MIDI de la tónica (57 = La3)."""
    rng = np.random.default_rng(seed)
    # progresiones en grados de la escala menor (raíz relativa, calidad)
    progA_opts = [[(0, "m"), (8, "M"), (3, "M"), (10, "M")],   # i VI III VII
                  [(0, "m"), (5, "m"), (8, "M"), (10, "M")],   # i iv VI VII
                  [(0, "m"), (10, "M"), (8, "M"), (10, "M")]]  # i VII VI VII
    progB_opts = [[(8, "M"), (10, "M"), (7, "m"), (0, "m")],
                  [(5, "m"), (10, "M"), (3, "M"), (7, "M")]]
    progA = progA_opts[int(rng.integers(len(progA_opts)))]
    progB = progB_opts[int(rng.integers(len(progB_opts)))]

    bars = []  # (bar, root_semis, quality, section)
    for b in range(32):
        if b < 4:
            sec = "intro"; ch = progA[b % 4]
        elif b < 12:
            sec = "A"; ch = progA[b % 4]
        elif b < 20:
            sec = "B"; ch = progB[b % 4]
        elif b < 28:
            sec = "A2"; ch = progA[b % 4]
        else:
            sec = "outro"; ch = progA[b % 4] if b < 31 else (0, "m")
        bars.append((b, ch[0], ch[1], sec))

    lead, arp, bass, drum = Track(), Track(), Track(), Track()
    K, S_, Hc, Ho, C = kick(), snare(), hat(False), hat(True), crash()

    # motivos melódicos (ritmo en corcheas: onset, duración) + contorno
    rhythms = [[(0, 2), (2, 1), (3, 1), (4, 2), (6, 2)],
               [(0, 1), (1, 1), (2, 2), (4, 1), (5, 1), (6, 2)],
               [(0, 3), (3, 1), (4, 1), (5, 1), (6, 2)],
               [(0, 1), (1, 2), (3, 1), (4, 3), (7, 1)]]
    motifs = []
    for _ in range(3):
        r = rhythms[int(rng.integers(len(rhythms)))]
        contour = [int(x) for x in rng.integers(0, 6, len(r))]
        motifs.append((r, contour))

    def tones_for(root, q, octave_base):
        ct = chord_tones(root, q)
        out = []
        for o in (0, 12):
            out += [key + 12 + octave_base + c + o for c in ct]
        return sorted(out)

    for (b, root, q, sec) in bars:
        beat0 = b * 4
        ct = chord_tones(root, q)
        # bajo: triángulo 4 bits, corcheas raíz/octava
        for e in range(8):
            m = key - 12 + root + (12 if e % 2 else 0)
            if sec == "outro" and b == 31 and e > 1:
                break
            n = int(SPB / 2 * 0.9)
            bass.add(beat0 + e / 2, tri4(mtof(m), n) * env(n, d=0.25, s=0.6, r=0.01), 0.55)
        # arpegio: pulso duty 12.5 %, semicorcheas
        if sec != "intro" or b >= 2:
            for e in range(16):
                m = key + 12 + ct[e % 3] + (12 if (e // 3) % 2 else 0)
                n = int(SPB / 4 * 0.8)
                arp.add(beat0 + e / 4, pulse(mtof(m), n, 0.125) * env(n, d=0.08), 0.12)
        # melodía
        if sec in ("A", "B", "A2") or (sec == "outro" and b < 31):
            if sec == "B":
                mot = motifs[2] if b % 2 == 0 else motifs[1]
            else:
                mot = motifs[0] if b % 4 != 3 else motifs[1]
            r, contour = mot
            tones = tones_for(root, q, 12 if sec == "A2" else 0)
            duty = 0.5 if sec == "A2" else 0.25
            for (on, du), ci in zip(r, contour):
                m = tones[ci % len(tones)]
                n = int(SPB / 2 * du * 0.92)
                vib = pulse(mtof(m), n, duty)
                lead.add(beat0 + on / 2, vib * env(n, a=0.004, d=0.35, s=0.5, r=0.02), 0.22)
        if sec == "outro" and b == 31:
            n = int(SPB * 3)
            lead.add(beat0, pulse(mtof(key + 24), n, 0.25) * env(n, d=1.2, s=0.4, r=0.3), 0.22)
        # batería: bombo a negras (muy marcado), caja en 2 y 4, charles a corcheas
        for k in range(4):
            if sec == "outro" and b == 31 and k > 0:
                break
            drum.add(beat0 + k, K, 0.9)
            if k in (1, 3) and sec != "intro":
                drum.add(beat0 + k, S_, 0.45)
            if sec == "intro" and k == 3 and b == 3:
                for f in range(4):
                    drum.add(beat0 + 3 + f / 4, S_, 0.25 + f * 0.08)
        for e in range(8):
            if sec == "outro" and b == 31:
                break
            openh = sec in ("B", "A2") and e % 2 == 1
            drum.add(beat0 + e / 2, Ho if openh else Hc, 0.18 if openh else 0.22)
        if b in (4, 12, 20, 28):
            drum.add(beat0, C, 0.22)

    mus = lead.buf + arp.buf + bass.buf + drum.buf
    return mus


def render(sfx_list, path, seed=1, key=57):
    mus = compose(seed, key)
    fx = Track()
    for beat, kind in sfx_list:
        fx.add(beat, sfx(kind), SFX_GAIN.get(kind, 0.32))
    mixd = mus * 0.8 + fx.buf
    mixd = np.tanh(mixd * 1.1)
    mixd = mixd[:TOTAL]
    mixd *= 0.89 / max(1e-6, np.abs(mixd).max())
    st = np.stack([mixd, mixd], 1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return path
