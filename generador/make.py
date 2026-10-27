"""Uso:
  python make.py wifi --preview out/wifi_preview.png
  python make.py wifi --render out/wifi.mp4
El tema es un módulo en topics/ con TITLE, SCENES, SUBS, SFX (todo medido en beats).
"""
import argparse
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine.render import Video  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--preview")
    ap.add_argument("--render")
    ap.add_argument("--beats", default="")
    ap.add_argument("--cover")
    a = ap.parse_args()
    T = importlib.import_module(f"topics.{a.topic}")
    v = Video(T)
    if a.preview:
        if a.beats:
            beats = [float(x) for x in a.beats.split(",")]
        else:
            beats = []
            for sc in T.SCENES:
                s, e = sc[0], sc[1]
                beats += [s + 0.6, (s + e) / 2, e - 1.0]
        os.makedirs(os.path.dirname(a.preview) or ".", exist_ok=True)
        print(v.preview(a.preview, beats))
    if a.cover:
        from engine.cover import render_cover
        os.makedirs(os.path.dirname(a.cover) or ".", exist_ok=True)
        print(render_cover(T, a.cover))
    if a.render:
        os.makedirs(os.path.dirname(a.render) or ".", exist_ok=True)
        wav = os.path.splitext(a.render)[0] + ".wav"
        print(v.render(a.render, wav))


if __name__ == "__main__":
    main()
