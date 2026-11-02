"""Voz en off opcional (español de España).
Un tema la activa definiendo VOICE = [(beat, "frase"), ...]. Cada frase se acelera
lo justo para terminar antes de la siguiente (máx. x1,4).
Motor: ElevenLabs si hay ELEVENLABS_API_KEY en el entorno (voz elegida por Pablo,
cambiable con ELEVENLABS_VOICE_ID); si no, SVOX Pico (`pico2wave -l es-ES`, calidad baja: solo para pruebas)."""
import json
import os
import subprocess
import tempfile
import urllib.request
import numpy as np

from . import audio

BASE_TEMPO = 1.0
MAX_TEMPO = 1.4
GAP = 0.15            # silencio mínimo entre frases (s)
DEFAULT_VOICE_ID = "PThYvS2VYRNVjFOlodls"   # voz de España elegida por Pablo (2-nov-2026)


def _pico(text, path):
    subprocess.run(["pico2wave", "-l", "es-ES", "-w", path, text], check=True)


def available():
    return bool(os.environ.get("ELEVENLABS_API_KEY"))


def _eleven(text, path, prev=None, nxt=None):
    """Sintetiza con ElevenLabs (modelo multilingüe) y guarda un mp3."""
    vid = os.environ.get("ELEVENLABS_VOICE_ID") or DEFAULT_VOICE_ID
    body = {"text": text, "model_id": os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
            "language_code": "es",
            "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}}
    if prev:
        body["previous_text"] = prev
    if nxt:
        body["next_text"] = nxt
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), method="POST",
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json",
                 "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
        f.write(r.read())


def synth(text, path, prev=None, nxt=None):
    if available():
        _eleven(text, path, prev, nxt)
    else:
        _pico(text, path)


def _load(path, tempo):
    filt = (f"highpass=f=80,atempo={tempo:.3f},"
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
            p = os.path.join(td, f"v{k}.{'mp3' if available() else 'wav'}")
            synth(text, p, lines[k - 1][1] if k else None, lines[k + 1][1] if k + 1 < len(lines) else None)
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
