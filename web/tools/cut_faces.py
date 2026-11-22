#!/usr/bin/env python3
"""Готовит портреты говорящих: берёт картинки из assets_src/faces (имя файла — как говорящий в поле speaker,
например mom.png), убирает белый фон и кладёт в web/assets/faces/face_<имя>.webp.
Игра показывает портрет слева от листа с текстом (экран «Сцена с героями», решение П32).
Запуск из корня репозитория: python3 web/tools/cut_faces.py [имена]
Нужны Pillow, numpy и scipy."""
import json, os, sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cut_bg import cut  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SRC = os.path.join(ROOT, "assets_src", "faces")
OUT = os.path.join(ROOT, "web", "assets", "faces")
# говорящие от «системы» нарисованы бирюзовыми линиями на чёрном: фон не вырезаем, игра складывает цвета
BLACK = {"god", "angel"}
# ручные квадраты для аватара там, где голову не найти по верху фигуры (у Бога сверху рамка чертежа)
HEAD = {"god": [127, 150, 413]}


def head_box(im):
    """Квадрат с головой для аватара: по верхней части фигуры. Для чертежа на чёрном — по светлым линиям."""
    a = np.asarray(im.convert("RGBA"))
    mask = a[..., 3] > 128 if im.mode == "RGBA" else a[..., :3].max(axis=2) > 60
    h, w = mask.shape
    rows = np.nonzero(mask.any(axis=1))[0]
    top = int(rows[0]) if len(rows) else 0
    band = mask[top: top + int(h * 0.22)]
    xs = np.nonzero(band.any(axis=0))[0]
    cx = int((xs[0] + xs[-1]) / 2) if len(xs) else w // 2
    s = int(min(w, h) * 0.62)
    x0 = max(0, min(w - s, cx - s // 2))
    y0 = max(0, top - int(s * 0.06))
    return [x0, y0, s]


def main():
    only = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    meta_path = os.path.join(OUT, "faces.json")
    meta = json.load(open(meta_path, encoding="utf-8")) if os.path.exists(meta_path) else {}
    n = 0
    for f in sorted(os.listdir(SRC)):
        name, ext = os.path.splitext(f)
        if ext.lower() not in (".png", ".jpg", ".jpeg", ".webp") or (only and name not in only):
            continue
        if name in BLACK:
            out = Image.open(os.path.join(SRC, f)).convert("RGB")
            out.thumbnail((1000, 1000), Image.LANCZOS)
            out.save(os.path.join(OUT, "face_" + name + ".webp"), quality=90, method=4)
            meta[name] = HEAD.get(name) or head_box(out)
            print(f"{name}: {out.size}, чертёж на чёрном")
            n += 1
            continue
        out, share, nh = cut(Image.open(os.path.join(SRC, f)), inner=True, size=1000, margin=0.01)
        out.save(os.path.join(OUT, "face_" + name + ".webp"), quality=90, method=4)
        meta[name] = head_box(out)
        print(f"{name}: {out.size}, фона убрано {share:.0%}" + (f", дырок внутри: {nh}" if nh else ""))
        n += 1
    json.dump(meta, open(meta_path, "w", encoding="utf-8"), indent=1)
    print("готово, портретов:", n)


if __name__ == "__main__":
    main()
