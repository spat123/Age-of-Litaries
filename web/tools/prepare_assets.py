#!/usr/bin/env python3
"""Готовит картинки для веб-игры: берёт фоны и значки из assets_src/art и кладёт уменьшенные копии в web/assets.
Высокий фон для телефона называется так же, но с _tall на конце.

Запуск из корня репозитория: python3 web/tools/prepare_assets.py           — только новые фоны
                             python3 web/tools/prepare_assets.py bg_well   — названные фоны заново

Фон берётся из assets_src/art/backgrounds_x2 (увеличенный, его делает upscale_bg.py), а если увеличенного нет —
из assets_src/art/backgrounds. В игру он идёт шириной до 1920 точек в формате webp: он на четверть легче jpg.
Нужен Pillow. Берутся только фоны, которые названы в story/*.json. Готовые файлы не перезаписываются."""
import glob, json, os, sys
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
ART = os.path.join(ROOT, "assets_src", "art")
OUT = os.path.join(ROOT, "web", "assets")

bgs = set()
for f in glob.glob(os.path.join(ROOT, "story", "ch*.json")):
    for s in json.load(open(f, encoding="utf-8"))["scenes"]:
        bgs.add(s["bg"])
after = json.load(open(os.path.join(ROOT, "story", "afterlife.json"), encoding="utf-8"))
for k in ("microloan", "promotion", "hr"):
    bgs.add(after[k]["bg"])


def source(name):
    """Откуда брать фон: сначала увеличенный, потом исходный."""
    for p in (os.path.join(ART, "backgrounds_x2", name + ".jpg"), os.path.join(ART, "backgrounds", name + ".png")):
        if os.path.exists(p):
            return p
    return None


again = set(sys.argv[1:])   # эти фоны готовим заново, даже если они уже есть
wait = []
for b in sorted(bgs):
    for tail, box in (("", (1920, 1920)), ("_tall", (1080, 1920))):
        dst = os.path.join(OUT, "bg", b + tail + ".webp")
        old = os.path.join(OUT, "bg", b + tail + ".jpg")   # так фоны хранились раньше
        if (os.path.exists(dst) or os.path.exists(old)) and b not in again:
            continue  # готовый фон не трогаем: он мог быть исправлен вручную (например, fix_yellow.py)
        src = source(b + tail)
        if not src:
            if not tail:
                wait.append(b)
            continue
        im = Image.open(src).convert("RGB")
        im.thumbnail(box, Image.LANCZOS)
        im.save(dst, quality=82, method=4)
        if os.path.exists(old):
            os.remove(old)
        print(b + tail, im.size, f"{os.path.getsize(dst) // 1024} КБ", "· из увеличенного" if "backgrounds_x2" in src else "· из исходника")
if wait:
    print("ждут рисунка (пока в игре стоит запасной фон):", ", ".join(wait))

# значки показателей: старые значки прототипа
for name, src in {"body": "icon_health", "mind": "icon_mental", "gold": "icon_gold", "rep": "icon_people"}.items():
    if os.path.exists(os.path.join(OUT, "icons", name + ".png")):
        continue
    im = Image.open(os.path.join(ART, "icons", src + ".png")).convert("RGBA")
    im.thumbnail((128, 128))
    im.save(os.path.join(OUT, "icons", name + ".png"))
