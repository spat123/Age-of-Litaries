#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рисунки во всё окно карточки: assets_src/cards_full/<рисунок>.png → web/assets/cards_full/<рисунок>.webp (768 точек).
Игра сама берёт такой рисунок вместо старого (вещь на ровном фоне), если он есть.
Рисунок на белом фоне (автор: «генерить без фона, чтобы фоны делать потом самим») вырезается по краю, а цвет фона,
на котором игра рисует лучи, берётся из COLORS; всё это пишется в web/assets/cards_full/cards_full.json.
Запуск из корня репозитория: python3 -I web/tools/prepare_card_full.py"""
import json, os, site, sys
sys.path.append(site.getusersitepackages())
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from cut_bg import cut

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SRC = os.path.join(ROOT, "assets_src", "cards_full")
OUT = os.path.join(ROOT, "web", "assets", "cards_full")
# цвет фона под вырезанным рисунком (лучи игра рисует светлее того же цвета)
COLORS = {"o_wooden_phone": "#6a45a8",  # фиолетовый: бирюзовое свечение телефона на нём видно
          "o_foil_hat": "#2f8f5b", "o_contract": "#b83a3a", "g_fist": "#d0452f", "g_run": "#3aa0d8",
          "g_sleep": "#2b3f8f", "g_pray": "#d6a12e", "o_letter": "#3f9a6e", "o_pig": "#e0732e",
          "o_stick": "#4f9a3a", "o_goose": "#3a86c8", "o_wooden_sword": "#c8442f", "o_scroll_speech": "#7a4fb0",
          "o_purse": "#2f7f6f", "g_write": "#b5523a", "o_battle_pass": "#d08a24", "o_guild_mages": "#4b2f80",
          "o_tin_armor": "#8a3a3a", "g_sing": "#e0a23a",
          "o_slate": "#3f8f7a", "o_barn": "#4f86c8", "o_birch_letter": "#c0504d", "o_church_book": "#5a3f8f",
          "o_quill_blot": "#c98a2e", "o_helmet_stone": "#6f9a3a", "o_closet": "#7a5a3a", "o_empty_book": "#2f6f9a",
          "o_shovel": "#4f9a5a", "o_tooth": "#d0607a", "o_salt_turnip": "#3a7ab0", "o_scroll_pass": "#8a3a9a",
          "o_pacifier": "#5ab0c8", "o_dragon_hoard": "#9a3a3a",
          "o_sand": "#3a6fb0"}  # песок жёлтый — на жёлтом фоне его не видно
DEFAULT = "#3b6fd1"
# если цвет не задан — берём из набора по имени рисунка, чтобы соседние карточки были разного цвета
PALETTE = ["#3b6fd1", "#c8442f", "#2f8f5b", "#7a4fb0", "#d08a24", "#2f7f8f", "#b5523a", "#4b6f2f", "#8a3a6a",
           "#3a86c8", "#c0504d", "#5a3f8f"]


def color_of(key):
    return COLORS.get(key) or PALETTE[sum(map(ord, key)) % len(PALETTE)]


# нарисованные фоны с лучами (assets_src/card_bg/<имя>.png): под рисунок кладётся фон, ближайший по цвету
BG_SRC = os.path.join(ROOT, "assets_src", "card_bg")
BG_OUT = os.path.join(ROOT, "web", "assets", "card_bg")
BG_REF = {"red": "#d23a2e", "orange": "#e8731f", "yellow": "#e8b21f", "green": "#3aa63a", "teal": "#1f8a8a",
          "blue": "#2f5fd0", "purple": "#7a3fb0", "pink": "#e04a9a"}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def nearest_bg(col, have):
    c = rgb(col)
    return min(have, key=lambda k: sum((a - b) ** 2 for a, b in zip(rgb(BG_REF[k]), c))) if have else None


def prepare_bgs():
    os.makedirs(BG_OUT, exist_ok=True)
    have = []
    if os.path.isdir(BG_SRC):
        for f in sorted(os.listdir(BG_SRC)):
            if f.endswith(".png") and f[:-4] in BG_REF:
                im = Image.open(os.path.join(BG_SRC, f)).convert("RGB")
                im.thumbnail((768, 768), Image.LANCZOS)
                im.save(os.path.join(BG_OUT, f[:-4] + ".webp"), quality=86, method=4)
                have.append(f[:-4])
    return have


def touches_edge(im):
    """Рисунок доходит до края картинки: на какой-нибудь стороне больше 6% точек не белые."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    sides = [[(x, 2) for x in range(0, w, 4)], [(x, h - 3) for x in range(0, w, 4)],
             [(2, y) for y in range(0, h, 4)], [(w - 3, y) for y in range(0, h, 4)]]
    return any(sum(min(rgb.getpixel(p)) < 225 for p in side) > len(side) * 0.06 for side in sides)


def keep_square(im):
    """Убрать белый фон, который касается края (и белые «дыры» крупнее мелочи), не обрезая квадрат."""
    import numpy as np
    from scipy import ndimage as ndi
    im = im.convert("RGB")
    im.thumbnail((768, 768), Image.LANCZOS)
    a = np.asarray(im).astype(int)
    light = (a.min(axis=2) >= 232) & ((a.max(axis=2) - a.min(axis=2)) <= 14)
    lab, n = ndi.label(light)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    bg = ndi.binary_dilation(bg, iterations=1) & (a.min(axis=2) >= 200)
    alpha = np.where(bg, 0, 255).astype("uint8")
    out = Image.fromarray(np.dstack([a.astype("uint8"), alpha]))
    return out


def white_bg(im):
    """Фон белый, если по краю картинки много белого (рисунок может доходить до краёв — песок, плечи, лицо)."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    # по всей рамке в 3 точки от края: если белого хотя бы пятая часть — фон белый
    pts = [(x, 3) for x in range(0, w, 8)] + [(x, h - 4) for x in range(0, w, 8)] + \
          [(3, y) for y in range(0, h, 8)] + [(w - 4, y) for y in range(0, h, 8)]
    return sum(min(rgb.getpixel(p)) > 235 for p in pts) > len(pts) * 0.2


def main():
    os.makedirs(OUT, exist_ok=True)
    bgs = prepare_bgs()
    meta = {}
    for f in sorted(os.listdir(SRC)):
        if not f.endswith(".png"):
            continue
        key = f[:-4]
        im = Image.open(os.path.join(SRC, f))
        if white_bg(im) and touches_edge(im):
            # рисунок упирается в край (плечи, лицо, рука из-за края): оставляем весь квадрат, убираем только белый
            # фон — в игре он заполняет окно целиком и край рисунка уходит под рамку, а не висит в воздухе
            out = keep_square(im)
            out.save(os.path.join(OUT, key + ".webp"), quality=90, method=4)
            meta[key] = {"cut": True, "full": True, "bg": color_of(key), "bgimg": nearest_bg(color_of(key), bgs)}
            print(key, out.size, "вырезан, во всё окно")
        elif white_bg(im):
            out, share, _ = cut(im, inner=True, size=768, margin=0.04)
            out.save(os.path.join(OUT, key + ".webp"), quality=90, method=4)
            # рисунок обрезан снизу (по пояс, по плечи) — в игре он стоит на нижнем краю окна, а не висит в воздухе
            a = out.getchannel("A")
            bx = a.getbbox()
            low = bx[3] - 12  # чуть выше нижней строки рисунка: самый край у вырезки полупрозрачный
            row = [a.getpixel((x, low)) for x in range(out.width)]
            bottom = sum(v > 128 for v in row) > (bx[2] - bx[0]) * 0.45
            meta[key] = {"cut": True, "bg": color_of(key), "bottom": bottom, "bgimg": nearest_bg(color_of(key), bgs)}
            print(key, out.size, "вырезан, фон убран", f"{share:.0%}")
        else:
            im = im.convert("RGB")
            im.thumbnail((768, 768), Image.LANCZOS)
            im.save(os.path.join(OUT, key + ".webp"), quality=88, method=4)
            print(key, im.size)
    balance(meta, bgs)
    json.dump(meta, open(os.path.join(OUT, "cards_full.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def balance(meta, bgs):
    """Цвета фонов поровну (автор: «Да, поровну»). Цвет, заданный в COLORS рукой (песок, телефон), не трогаем.
    Остальные идут в порядке, в каком рисунки встречаются в сюжете, и каждый получает самый редкий пока цвет,
    но не тот, что у предыдущего: соседние выборы обычно стоят в одной сцене."""
    import glob, re
    if not bgs:
        return
    order = []
    for f in sorted(glob.glob(os.path.join(ROOT, "story", "*.json"))):
        for m in re.finditer(r'"art"\s*:\s*"([^"]+)"', open(f, encoding="utf-8").read()):
            if m.group(1) not in order:
                order.append(m.group(1))
    keys = [k for k in order if k in meta and meta[k].get("cut")] + sorted(k for k in meta if meta[k].get("cut") and k not in order)
    count = {b: 0 for b in bgs}
    for k in keys:
        if k in COLORS:
            count[meta[k]["bgimg"]] += 1
    prev = None
    for k in keys:
        if k in COLORS:
            prev = meta[k]["bgimg"]
            continue
        pick = min((b for b in bgs if b != prev), key=lambda b: (count[b], bgs.index(b)))
        meta[k]["bgimg"] = pick
        meta[k]["bg"] = BG_REF[pick]
        count[pick] += 1
        prev = pick
    print("фоны:", count)


if __name__ == "__main__":
    main()
