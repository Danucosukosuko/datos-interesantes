# Datos Interesantes

Generador de Shorts pixel-art (todo por código) y registro de temas publicados.

- `generador/engine/` — motor común: fuente 5x7 propia, gráficos, chiptune, render CRT + ffmpeg.
- `generador/topics/<tema>.py` — cada vídeo: `SCENES`, `SUBS` y `SFX` medidos en beats (128 BPM, 128 beats = 60 s).
- `temas_publicados.txt` — temas ya usados (no repetir nunca).
- Rama `videos` — solo el último vídeo subido (se sobrescribe cada día; Metricool guarda su propia copia).

Uso:

```
cd generador
python3 make.py wifi --preview out/preview.png   # hoja de fotogramas
python3 make.py wifi --render out/wifi.mp4       # vídeo final
```
