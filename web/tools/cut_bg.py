#!/usr/bin/env python3
"""Готовит рисунки карточек для игры: берёт картинки из assets_src/cards_new, убирает белый фон,
обрезает лишние поля, уменьшает и кладёт в web/assets/cards под тем же именем (webp с прозрачным фоном:
он в шесть раз легче png, а на вид такой же).
Убирает и «дырки»: чисто-белые участки внутри предмета, сквозь которые виден фон (между ножек табуретки,
в ручке кружки). Белые части самого предмета не трогает: они у генератора не чисто-белые, а с оттенком.
Имя файла — имя рисунка из story/art.json, например g_coins.png.
Запуск из корня репозитория: python3 web/tools/cut_bg.py            — все новые картинки
                             python3 web/tools/cut_bg.py g_coins    — только названные
Нужны Pillow и numpy."""
import os, sys
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SRC = os.path.join(ROOT, "assets_src", "cards_new")
OUT = os.path.join(ROOT, "web", "assets", "cards")
SIZE = 512       # сторона готового рисунка
WHITE = 232      # всё светлее этого на краю считается фоном
PURE = 249       # участок внутри предмета считается дыркой, если он такой же чисто-белый, как фон,
HOLE = 150       # и в нём не меньше стольких точек
KEEP_INNER = set()   # имена рисунков, у которых белое внутри трогать нельзя (если скрипт ошибётся)
EXT = (".png", ".jpg", ".jpeg", ".webp")


def holes(rgb, bg, light):
    """Чисто-белые замкнутые участки внутри предмета: это фон, который виден насквозь. Возвращает маску и их число."""
    pure = (rgb.min(axis=2) >= PURE) & ((rgb.max(axis=2) - rgb.min(axis=2)) <= 5) & ~bg
    h, w = pure.shape
    seen = np.zeros((h, w), bool)
    out = np.zeros((h, w), bool)
    n = 0
    ys, xs = np.nonzero(pure)
    for y0, x0 in zip(ys.tolist(), xs.tolist()):
        if seen[y0, x0]:
            continue
        comp = [(y0, x0)]
        seen[y0, x0] = True
        i = 0
        while i < len(comp):
            y, x = comp[i]
            i += 1
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and pure[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    comp.append((ny, nx))
        if len(comp) >= HOLE:
            n += 1
            for y, x in comp:
                out[y, x] = True
    for _ in range(2):  # светлая кайма вокруг дырки: на две точки в стороны, но только по светлому
        g = out.copy()
        g[1:] |= out[:-1]
        g[:-1] |= out[1:]
        g[:, 1:] |= out[:, :-1]
        g[:, :-1] |= out[:, 1:]
        out = out | (g & light)
    return out, n


def cut(im, inner=True, size=SIZE, margin=0.03):
    """Белый фон, который касается края картинки, делаем прозрачным. Белое внутри предмета не трогаем,
    кроме чисто-белых «дырок» (см. holes)."""
    rgb = np.asarray(im.convert("RGB")).astype(np.int16)
    h, w = rgb.shape[:2]
    light = (rgb.min(axis=2) >= WHITE) & ((rgb.max(axis=2) - rgb.min(axis=2)) <= 14)
    bg = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if light[y, x] and not bg[y, x]:
                bg[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if light[y, x] and not bg[y, x]:
                bg[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and light[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True
                q.append((ny, nx))
    share = float(bg.mean())
    nh = 0
    if inner:
        hole, nh = holes(rgb, bg, light)
        bg = bg | hole
    alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))  # убираем белую кайму
    out = im.convert("RGBA")
    out.putalpha(alpha)
    box = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
    if box:
        m = int(max(out.size) * margin)
        box = (max(0, box[0] - m), max(0, box[1] - m), min(out.width, box[2] + m), min(out.height, box[3] + m))
        out = out.crop(box)
    if size:
        out.thumbnail((size, size), Image.LANCZOS)
    return out, share, nh


def main():
    if not os.path.isdir(SRC):
        os.makedirs(SRC)
        print("создана папка", os.path.relpath(SRC), "— клади в неё новые картинки")
        return
    only = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for f in sorted(os.listdir(SRC)):
        name, ext = os.path.splitext(f)
        if ext.lower() not in EXT or (only and name not in only):
            continue
        im = Image.open(os.path.join(SRC, f))
        out, share, nh = cut(im, inner=name not in KEEP_INNER)
        for e in EXT:  # старый рисунок с тем же именем убираем, чтобы в игре не было двух
            old = os.path.join(OUT, name + e)
            if os.path.exists(old):
                os.remove(old)
        out.save(os.path.join(OUT, name + ".webp"), quality=90, method=4)
        warn = "" if share > 0.15 else "  ← фона почти не нашлось: проверь, что он белый"
        print(f"{name}: {im.size} → {out.size}, фона убрано {share:.0%}" + (f", дырок внутри: {nh}" if nh else "") + warn)
        n += 1
    print("готово, рисунков:", n)


if __name__ == "__main__":
    main()
