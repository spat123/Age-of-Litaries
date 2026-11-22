#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Гербы титулов: assets_src/crests/<титул>.png (на белом) → web/assets/crests/<титул>.webp без фона, 320 точек.
Запуск из корня: python3 -I web/tools/prepare_crests.py"""
import os, site, sys
sys.path.append(site.getusersitepackages())
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from cut_bg import cut

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SRC, OUT = os.path.join(ROOT, "assets_src", "crests"), os.path.join(ROOT, "web", "assets", "crests")
os.makedirs(OUT, exist_ok=True)
for f in sorted(os.listdir(SRC)):
    if f.endswith(".png"):
        out, share, _ = cut(Image.open(os.path.join(SRC, f)), inner=True, size=320, margin=0.02)
        out.save(os.path.join(OUT, f[:-4] + ".webp"), quality=90, method=4)
        print(f[:-4], out.size, f"фон {share:.0%}")
