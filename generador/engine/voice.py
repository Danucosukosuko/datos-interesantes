"""Voz en off opcional (español de España) con SVOX Pico (`pico2wave -l es-ES`).
Un tema la activa definiendo VOICE = [(beat, "frase"), ...]. Cada frase se acelera
lo justo para terminar antes de la siguiente (máx. x1,4)."""
import os
import subprocess
import tempfile
import numpy as np

from . import audio

BASE_TEMPO = 1.08     # Pico habla algo lento para el ritmo de un Reel
MAX_TEMPO = 1.4
GAP = 0.15            # silencio mínimo entre frases (s)


def _pico(text, path):
    subprocess.run(["pico2wave", "-l", "es-ES", "-w", path, text], check=True)


def _load(path, tempo):
    filt = (f"highpass=f=90,lowpass=f=7600,atempo={tempo:.3f},"
            "acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
            "loudnorm=I=-16:TP=-1.5:LRA=7")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-af", filt,
                          "-ar", str(audio.SR), "-ac", "1", "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def _trim(sig, thr=0.01):
    idx = np.flatnonzero(np.abs(sig) > thr)
    return sig[idx[0]:idx[-1] + 1] if len(idx) else sig


def track(lines):
    """Devuelve la pista de voz (float32, misma longitud que la música)."""
    buf = np.zeros(audio.TOTAL + audio.SR * 2, np.float32)
    lines = sorted(lines)
    with tempfile.TemporaryDirectory() as td:
        for k, (beat, text) in enumerate(lines):
            end = lines[k + 1][0] if k + 1 < len(lines) else audio.BEATS
            avail = (end - beat) * 60.0 / audio.BPM - GAP
            p = os.path.join(td, f"v{k}.wav")
            _pico(text, p)
            sig = _trim(_load(p, BASE_TEMPO))
            dur = len(sig) / audio.SR
            if dur > avail:
                tempo = min(MAX_TEMPO, BASE_TEMPO * dur / avail)
                sig = _trim(_load(p, tempo))
                dur = len(sig) / audio.SR
                if dur > avail:
                    print(f"  AVISO voz: «{text}» dura {dur:.2f} s y solo caben {avail:.2f} s; acórtala")
            i = audio.b2s(beat)
            j = min(len(buf), i + len(sig))
            buf[i:j] += sig[:j - i]
    return buf[:audio.TOTAL]


def duck_envelope(v, depth=0.7):
    """Ganancia para la música: baja `depth` mientras hay voz (ataque 40 ms, suelta 300 ms)."""
    hop = 441
    n = len(v) // hop + 1
    lvl = np.array([np.abs(v[i * hop:(i + 1) * hop]).max() if i * hop < len(v) else 0 for i in range(n)])
    on = (lvl > 0.02).astype(np.float32)
    g = np.empty(n, np.float32); cur = 0.0
    a_up, a_dn = 1 - np.exp(-1 / 4), 1 - np.exp(-1 / 30)
    for i in range(n):
        cur += (on[i] - cur) * (a_up if on[i] > cur else a_dn)
        g[i] = cur
    g = np.repeat(g, hop)[:len(v)]
    return 1.0 - depth * g
