#!/usr/bin/env python3
"""Готовит музыку для веб-игры: берёт мелодии из assets_src/audio/bgm, ужимает их
и кладёт в web/assets/audio под короткими именами. Нужен ffmpeg. Готовые файлы не перезаписываются.
Запуск из корня репозитория: python3 web/tools/prepare_audio.py"""
import os, subprocess

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SRC = os.path.join(ROOT, "assets_src", "audio", "bgm")
OUT = os.path.join(ROOT, "web", "assets", "audio")
# имя в игре: исходный файл. menu — главное меню, village — главы 0–4, capital — главы 5–6
TRACKS = {"menu": "foxfire_tavern_march.mp3", "village": "foxfire_tavern_march_b.mp3", "capital": "foxfire_corporate_crusade.mp3"}

os.makedirs(OUT, exist_ok=True)
for name, src in TRACKS.items():
    dst = os.path.join(OUT, name + ".mp3")
    if os.path.exists(dst):
        continue
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(SRC, src), "-vn", "-b:a", "80k", dst], check=True)
    print(name, os.path.getsize(dst) // 1024, "КБ")
