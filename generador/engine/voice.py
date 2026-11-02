"""Voz en off opcional (español de España).
Un tema la activa definiendo VOICE = [(beat, "frase"), ...]. Cada frase se acelera
lo justo para terminar antes de la siguiente (máx. x1,4).
Motor: ElevenLabs si hay ELEVENLABS_API_KEY en el entorno (voz elegida por Pablo,
cambiable con ELEVENLABS_VOICE_ID); si no, SVOX Pico (`pico2wave -l es-ES`, calidad baja: solo para pruebas)."""
import base64
import hashlib
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


def _request(text, endpoint, prev=None, nxt=None):
    vid = os.environ.get("ELEVENLABS_VOICE_ID") or DEFAULT_VOICE_ID
    model = os.environ.get("ELEVENLABS_MODEL", "eleven_v3")
    body = {"text": text, "model_id": model, "language_code": "es"}
    if model == "eleven_v3":
        body["voice_settings"] = {"stability": 0.5, "similarity_boost": 0.8}   # v3: 0 / 0.5 / 1
    else:
        body["voice_settings"] = {"stability": 0.4, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}
        if prev:
            body["previous_text"] = prev
        if nxt:
            body["next_text"] = nxt
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}{endpoint}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), method="POST",
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def _eleven(text, path, prev=None, nxt=None):
    """Sintetiza con ElevenLabs y guarda un mp3. Modelo por defecto: Eleven v3, que entiende
    etiquetas de entonación entre corchetes dentro del texto: "[cálido] Hola."."""
    with open(path, "wb") as f:
        f.write(_request(text, "", prev, nxt))


def _eleven_ts(text, path, prev=None, nxt=None):
    """Como _eleven, pero devuelve [(segundo, palabra)] con el instante en que empieza cada palabra
    (las etiquetas [..] no cuentan como palabras)."""
    d = json.loads(_request(text, "/with-timestamps", prev, nxt))
    with open(path, "wb") as f:
        f.write(base64.b64decode(d["audio_base64"]))
    al = d.get("alignment") or d.get("normalized_alignment")
    words, cur, t0, tag = [], "", None, False
    for ch, t in zip(al["characters"], al["character_start_times_seconds"]):
        if ch == "[":
            tag = True
        if tag:
            if ch == "]":
                tag = False
            continue
        if ch.isspace():
            if cur.strip():
                words.append((t0, cur))
            cur, t0 = "", None
            continue
        if t0 is None:
            t0 = t
        cur += ch
    if cur.strip():
        words.append((t0, cur))
    return words


def synth(text, path, prev=None, nxt=None):
    if available():
        return _eleven_ts(text, path, prev, nxt)
    _pico(text, path)
    return None


def _load(path, tempo):
    filt = (f"highpass=f=80,atempo={tempo:.3f},"
            "acompressor=threshold=-20dB:ratio=3:attack=5:release=80,"
            "loudnorm=I=-16:TP=-1.5:LRA=7")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-af", filt,
                          "-ar", str(audio.SR), "-ac", "1", "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def _synth_cached(text, path, cache_dir, prev=None, nxt=None):
    """synth() con caché por frase: cambiar una frase no vuelve a pedir las demás a ElevenLabs."""
    if not cache_dir or not available():
        return synth(text, path, prev, nxt)
    key = hashlib.sha1(json.dumps([text, os.environ.get("ELEVENLABS_VOICE_ID") or DEFAULT_VOICE_ID,
                                   os.environ.get("ELEVENLABS_MODEL", "eleven_v3")]).encode()).hexdigest()[:16]
    mp3, js = os.path.join(cache_dir, f"frase_{key}.mp3"), os.path.join(cache_dir, f"frase_{key}.json")
    if not (os.path.exists(mp3) and os.path.exists(js)):
        os.makedirs(cache_dir, exist_ok=True)
        words = synth(text, mp3, prev, nxt)
        with open(js, "w") as f:
            json.dump(words, f)
    import shutil
    shutil.copy(mp3, path)
    with open(js) as f:
        return [tuple(w) for w in json.load(f)]


def _trim(sig, thr=0.01):
    """Quita silencios al principio y al final; devuelve (señal, muestras quitadas al principio)."""
    idx = np.flatnonzero(np.abs(sig) > thr)
    return (sig[idx[0]:idx[-1] + 1], int(idx[0])) if len(idx) else (sig, 0)


def track(lines, cache_dir=None):
    """Devuelve (pista de voz float32 de la misma longitud que la música, palabras).
    palabras = [(nº de frase, beat en que empieza, palabra)] o None si el motor no da tiempos.
    Con cache_dir, el resultado se guarda y no se vuelve a pedir a ElevenLabs (ahorra créditos)."""
    lines = sorted(lines)
    key = hashlib.sha1(json.dumps([lines, available(), os.environ.get("ELEVENLABS_VOICE_ID") or DEFAULT_VOICE_ID,
                                   os.environ.get("ELEVENLABS_MODEL", "eleven_v3")]).encode()).hexdigest()[:16]
    cpath = os.path.join(cache_dir, f"voz_{key}.npz") if cache_dir else None
    if cpath and os.path.exists(cpath):
        z = np.load(cpath, allow_pickle=False)
        words = json.loads(str(z["words"]))
        return z["buf"], ([tuple(w) for w in words] if words is not None else None)
    buf = np.zeros(audio.TOTAL + audio.SR * 2, np.float32)
    all_words = []
    bps = audio.BPM / 60.0
    with tempfile.TemporaryDirectory() as td:
        for k, (beat, text) in enumerate(lines):
            end = lines[k + 1][0] if k + 1 < len(lines) else audio.BEATS
            avail = (end - beat) / bps - GAP
            p = os.path.join(td, f"v{k}.{'mp3' if available() else 'wav'}")
            words = _synth_cached(text, p, cache_dir, lines[k - 1][1] if k else None,
                                  lines[k + 1][1] if k + 1 < len(lines) else None)
            tempo = BASE_TEMPO
            sig, off = _trim(_load(p, tempo))
            dur = len(sig) / audio.SR
            if dur > avail:
                tempo = min(MAX_TEMPO, BASE_TEMPO * dur / avail)
                sig, off = _trim(_load(p, tempo))
                dur = len(sig) / audio.SR
                if dur > avail:
                    print(f"  AVISO voz: «{text}» dura {dur:.2f} s y solo caben {avail:.2f} s; acórtala")
            i = audio.b2s(beat)
            j = min(len(buf), i + len(sig))
            buf[i:j] += sig[:j - i]
            if words is not None:
                for t, w in words:
                    ts = max(0.0, t / tempo - off / audio.SR)
                    all_words.append((k, beat + ts * bps, w))
    buf = buf[:audio.TOTAL]
    words_out = all_words if available() else None
    if cpath:
        os.makedirs(cache_dir, exist_ok=True)
        np.savez(cpath, buf=buf, words=np.array(json.dumps(words_out)))
    return buf, words_out


def _clean(word, font):
    word = word.replace("…", "...").replace(";", ",").replace("—", "-").replace("–", "-")
    return "".join(ch for ch in word.upper() if font.has(ch))


def subs_from_words(words, until=116, max_words=4, max_chars=20):
    """Convierte las palabras con tiempo en SUBS del karaoke: [(beat, "TEXTO", [beat de cada palabra])].
    Corta en trozos de pocas palabras y siempre tras un punto, interrogación o exclamación."""
    from . import font
    subs, cur, cur_b, cur_line = [], [], [], None

    def flush():
        if cur:
            subs.append((cur_b[0], " ".join(cur), list(cur_b)))
        cur.clear(); cur_b.clear()

    for line, b, w in words:
        if b >= until:
            continue
        w = _clean(w, font)
        if not w:
            continue
        if line != cur_line or len(cur) >= max_words or len(" ".join(cur + [w])) > max_chars:
            flush()
        cur_line = line
        cur.append(w); cur_b.append(b)
        if w[-1] in ".?!":
            flush()
    flush()
    return subs


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
