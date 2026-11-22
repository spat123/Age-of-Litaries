#!/usr/bin/env python3
"""Готовит рисованные вещи интерфейса для игры: берёт картинки из assets_src/ui_new, убирает белый фон,
делит картинку с несколькими вещами на отдельные, у карточки вырезает окно под рисунок и кладёт всё в web/assets/ui.
Заодно пишет web/assets/ui/ui.json: размер каждой вещи и края, которые при растягивании не меняются.
Значки показателей кладёт в web/assets/icons (body, mind, rep, gold).

Запуск из корня репозитория: python3 web/tools/cut_ui.py
Края (поле SLICE) подобраны на глаз по картинкам 22.11.2026. Новая картинка — проверь края заново:
python3 web/tools/cut_ui.py --preview папка  — нарисует, как каждая вещь растягивается.
Нужны Pillow, numpy и scipy."""
import json, os, sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cut_bg import cut  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
# ui_new — первый набор (ui_*), ui_new2 — набор по наброску «Сцена с героями» (k_*, решение П32)
SRCS = [os.path.join(ROOT, "assets_src", "ui_new"), os.path.join(ROOT, "assets_src", "ui_new2")]
OUT = os.path.join(ROOT, "web", "assets", "ui")
ICONS = os.path.join(ROOT, "web", "assets", "icons")
MAX = 1100  # длинная сторона готовой вещи

# Картинки, на которых несколько вещей: в каком порядке они лежат и как их назвать.
# order: "rows" — сверху вниз, "cols" — слева направо, "grid" — по строкам слева направо.
SPLIT = {
    "ui_buttons": ("rows", ["ui_btn_wood", "ui_btn_green"]),
    "ui_plate_ribbon": ("rows", ["ui_plate", "ui_ribbon"]),
    "ui_stamps": ("cols", ["ui_stamp_great", "ui_stamp_ok", "ui_stamp_shame"]),
    "ui_icons": ("grid", ["icon_body", "icon_mind", "icon_rep", "icon_gold"]),
    # новые значки (ui_new2 режется после ui_new, поэтому они заменяют старые)
    "ui_icons2": ("grid", ["icon_body", "icon_mind", "icon_rep", "icon_gold"]),
    # значки, которые прислал автор («вот отсюда смело бери верхние иконки»): верхний ряд его листа
    # refs/ui_mock/primer_ikonki.png; режется после ui_icons2 и заменяет его; звезда — метка особого выбора
    "ui_icons3": ("cols", ["icon_body", "icon_mind", "icon_rep", "icon_gold", "icon_star"]),
}
# Края, которые не растягиваются, в долях от ширины (слева, справа) и высоты (сверху, снизу) готовой вещи.
SLICE = {
    "ui_sheet": (0.05, 0.05, 0.16, 0.2),
    "ui_card": None,           # карточка не растягивается по частям: её окно должно остаться на месте
    "ui_shelf": None,
    "ui_badge": (0.2, 0.2, 0.2, 0.1),
    "ui_board": (0.22, 0.22, 0.12, 0.08),
    "ui_btn_wood": (0.12, 0.12, 0.3, 0.38),
    "ui_btn_green": (0.12, 0.12, 0.3, 0.38),
    "ui_plate": (0.18, 0.18, 0.32, 0.4),
    "ui_ribbon": (0.16, 0.16, 0.32, 0.4),
    "ui_note": None,
    "ui_system": (0.1, 0.1, 0.16, 0.16),
    "ui_result": (0.08, 0.28, 0.28, 0.14),  # печать в правом верхнем углу целиком внутри угла
    "ui_stamp_great": (0.12, 0.12, 0.25, 0.25),
    "ui_stamp_ok": (0.12, 0.12, 0.25, 0.25),
    "ui_stamp_shame": (0.12, 0.12, 0.25, 0.25),
    # набор по наброску «Сцена с героями»
    "k_panel": (0.1, 0.1, 0.2, 0.2),
    "k_namesign": (0.3, 0.3, 0.3, 0.35),  # листья на концах целиком в неподвижных краях
    "k_ribbon": (0.2, 0.2, 0.3, 0.3),
    "k_card": None,
    "k_token": None,
    "k_shelf": None,
    "k_stats": None,
    "k_board": (0.2, 0.2, 0.12, 0.12),
    "k_panel2": (0.05, 0.05, 0.14, 0.14),  # тонкая рама окна диалога: латунь только в углах
    "k_avatar": None,
    "k_card2": None,  # карточка по примеру автора: доски, заклёпки, окно 1:1, табличка под текст
    "k_card2_gold": None,  # особая: та же, золотая, с печатью
    "k_slot2": None,
    "k_slot3": None,  # ячейка предмета без заклёпок, под цвет дерева карточек: прислал автор (снимок из Фигмы)
    "k_avatar_round": None,  # круглая рамка аватара, по форме портрета в кольце из Hades II  # закруглённая ячейка уникальной карточки, как иконки даров в Hades
    "k_slot": None,
    "k_btn": (0.2, 0.2, 0.3, 0.35),
    "k_btn_green": (0.2, 0.2, 0.3, 0.35),
}
WINDOW = {"ui_card", "k_card", "k_row", "k_avatar", "k_card2", "k_card2_gold", "k_slot2", "k_avatar_round", "k_slot3"}
# чертёж «системы»: светящиеся линии на чёрном, фон не вырезаем (в игре чёрное пропадает при сложении цветов)
BLACK = {"b_frame": None, "b_panel": (0.14, 0.14, 0.26, 0.26)}  # у этих вещей окно под рисунок делается прозрачным


def parts(rgba, n, order):
    """Делит картинку с прозрачным фоном на n вещей по связным кускам."""
    a = np.asarray(rgba)[..., 3] > 16
    lab, k = ndi.label(a)
    sizes = ndi.sum(a, lab, range(1, k + 1))
    big = [i + 1 for i in np.argsort(sizes)[::-1][:n]]
    if len(big) < n or sizes[big[-1] - 1] < sizes[big[0] - 1] * 0.02:
        raise SystemExit("не нашёл %d отдельных вещей" % n)
    # мелкие куски (тень, крошки) прилипают к ближайшей большой вещи
    boxes = {i: ndi.find_objects((lab == i).astype(int))[0] for i in big}
    cent = {i: ((b[0].start + b[0].stop) / 2, (b[1].start + b[1].stop) / 2) for i, b in boxes.items()}
    owner = np.zeros_like(lab)
    for i in big:
        owner[lab == i] = i
    for j in range(1, k + 1):
        if j in big:
            continue
        ys, xs = np.nonzero(lab == j)
        cy, cx = ys.mean(), xs.mean()
        owner[lab == j] = min(big, key=lambda i: (cent[i][0] - cy) ** 2 + (cent[i][1] - cx) ** 2)
    if order == "rows":
        big.sort(key=lambda i: cent[i][0])
    elif order == "cols":
        big.sort(key=lambda i: cent[i][1])
    else:
        rows = sorted(big, key=lambda i: cent[i][0])
        half = len(rows) // 2
        big = sorted(rows[:half], key=lambda i: cent[i][1]) + sorted(rows[half:], key=lambda i: cent[i][1])
    out = []
    arr = np.asarray(rgba).copy()
    for i in big:
        one = arr.copy()
        one[..., 3] = np.where(owner == i, arr[..., 3], 0)
        im = Image.fromarray(one)
        box = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
        m = 6
        out.append(im.crop((max(0, box[0] - m), max(0, box[1] - m), min(im.width, box[2] + m), min(im.height, box[3] + m))))
    return out


def window(card, seed=(0.3, 0.5), least=0.15):
    """Окно карточки: ровная жёлтая заливка. seed — где внутри окна начать искать (доли высоты и ширины).
    Делает окно прозрачным, возвращает его рамку."""
    arr = np.asarray(card).copy()
    h, w = arr.shape[:2]
    rgb = arr[..., :3].astype(int)
    sy, sx = int(h * seed[0]), int(w * seed[1])
    seed = rgb[sy, sx]
    near = (np.abs(rgb - seed).sum(axis=2) < 70) & (arr[..., 3] > 200)
    lab, _ = ndi.label(near)
    reg = lab == lab[sy, sx]
    reg = ndi.binary_fill_holes(reg)
    ys, xs = np.nonzero(reg)
    if reg.mean() < least:
        raise SystemExit("окно карточки не нашлось")
    grow = ndi.binary_dilation(reg, iterations=2) & (np.abs(rgb - seed).sum(axis=2) < 140)
    arr[..., 3] = np.where(grow | reg, 0, arr[..., 3])
    return Image.fromarray(arr), [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def line_width(im):
    """Толщина контура: сколько тёмных точек подряд от края вещи внутрь, медиана по нескольким строкам и столбцам."""
    arr = np.asarray(im).astype(int)
    a, luma = arr[..., 3], (arr[..., 0] * 299 + arr[..., 1] * 587 + arr[..., 2] * 114) // 1000
    h, w = a.shape
    runs = []
    for frac in (0.4, 0.5, 0.6):
        for line, al in ((luma[int(h * frac)], a[int(h * frac)]), (luma[:, int(w * frac)], a[:, int(w * frac)])):
            for seq, sa in ((line, al), (line[::-1], al[::-1])):
                idx = np.nonzero(sa > 200)[0]
                if not len(idx):
                    continue
                i, n = idx[0], 0
                while i + n < len(seq) and seq[i + n] < 95:
                    n += 1
                if 2 <= n <= 60:
                    runs.append(n)
    return int(np.median(runs)) if runs else None


def inner_rect(im):
    """Ровная светлая середина вещи (пергамент в раме): её рамка в точках картинки."""
    arr = np.asarray(im).astype(float)
    h, w = arr.shape[:2]
    rgb = ndi.uniform_filter(arr[..., :3], size=(11, 11, 1))
    seed = rgb[h // 2, w // 2]
    near = (np.abs(rgb - seed).sum(axis=2) < 55) & (arr[..., 3] > 200)
    lab, _ = ndi.label(near)
    reg = ndi.binary_fill_holes(lab == lab[h // 2, w // 2])
    ys, xs = np.nonzero(reg)
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def nine(im, sl, W, H):
    """Растягивает картинку по девяти кускам до W×H (для предпросмотра)."""
    w, h = im.size
    l, r, t, b = int(sl[0] * w), int(sl[1] * w), int(sl[2] * h), int(sl[3] * h)
    xs, ys, X, Y = [0, l, w - r, w], [0, t, h - b, h], [0, l, W - r, W], [0, t, H - b, H]
    out = Image.new("RGBA", (W, H))
    for i in range(3):
        for j in range(3):
            if xs[i + 1] > xs[i] and ys[j + 1] > ys[j] and X[i + 1] > X[i] and Y[j + 1] > Y[j]:
                out.paste(im.crop((xs[i], ys[j], xs[i + 1], ys[j + 1])).resize((X[i + 1] - X[i], Y[j + 1] - Y[j]), Image.LANCZOS), (X[i], Y[j]))
    return out


def main():
    preview = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    files = [(d, f) for d in SRCS if os.path.isdir(d) for f in sorted(os.listdir(d))]
    for src, f in files:
        name, ext = os.path.splitext(f)
        if ext.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        if name == "d_desk":
            # стол — это фон страницы: ничего не вырезаем
            im = Image.open(os.path.join(src, f)).convert("RGB")
            im.thumbnail((1600, 1600), Image.LANCZOS)
            im.save(os.path.join(OUT, name + ".webp"), quality=86, method=4)
            meta[name] = {"size": list(im.size)}
            print(f"{name}: {im.size} (фон страницы)")
            continue
        if name in BLACK:
            im = Image.open(os.path.join(src, f)).convert("RGB")
            if BLACK[name]:
                # лист-чертёж: обрезаем чёрные поля вокруг линий, иначе края растягиваются не там
                box = im.convert("L").point(lambda v: 255 if v > 40 else 0).getbbox()
                if box:
                    m = 6
                    im = im.crop((max(0, box[0] - m), max(0, box[1] - m), min(im.width, box[2] + m), min(im.height, box[3] + m)))
            im.thumbnail((MAX, MAX), Image.LANCZOS)
            im.save(os.path.join(OUT, name + ".webp"), quality=92, method=4)
            info = {"size": list(im.size), "add": True}
            if BLACK[name]:
                sl = BLACK[name]
                info["slice"] = [round(sl[0] * im.width), round(sl[1] * im.width), round(sl[2] * im.height), round(sl[3] * im.height)]
            meta[name] = info
            print(f"{name}: {im.size} (чертёж, фон чёрный)")
            continue
        # у папки страницы светлые: белое внутри не трогаем
        rgba, share, nh = cut(Image.open(os.path.join(src, f)), inner=name != "d_folder", size=None, margin=0.004)
        pieces = list(zip(SPLIT[name][1], parts(rgba, len(SPLIT[name][1]), SPLIT[name][0]))) if name in SPLIT else [(name, rgba)]
        for key, im in pieces:
            if max(im.size) > MAX:
                im.thumbnail((MAX, MAX), Image.LANCZOS)
            info = {"size": list(im.size)}
            lw = line_width(im)
            if lw:
                info["line"] = lw
            if key in WINDOW:
                im, info["window"] = window(im, *(((0.5, 0.12), 0.05) if key == "k_row" else ((0.3, 0.5), 0.15)))
            if key == "k_row":
                # широкая карточка растягивается только в середине таблички; окно слева целиком в неподвижном крае
                wx, wy, ww, wh = info["window"]
                info["slice"] = [wx + ww + int(im.width * 0.03), int(im.width * 0.07), int(im.height * 0.42), int(im.height * 0.42)]
                info["fit_h"] = True
                info["tile_x"] = True  # середина с резным сердцем повторяется, а не растягивается
            if key == "ui_result":
                # печать торчит над листом: где начинается сам лист и где кончается печать (ниже неё можно писать)
                arr = np.asarray(im).astype(int)
                al = arr[..., 3] > 128
                wide = np.nonzero(al.sum(axis=1) > im.width * 0.6)[0]
                red = al & (arr[..., 0] > 150) & (arr[..., 1] < 110) & (arr[..., 2] < 110)
                rows = np.nonzero(red.sum(axis=1) > 3)[0]
                info["paper_top"] = int(wide[0]) if len(wide) else 0
                info["content_top"] = int(rows.max()) if len(rows) else info["paper_top"]
            if key in ("k_card", "k_card2", "k_card2_gold"):
                # табличка для подписи: светлое место под окном
                arr = np.asarray(im).astype(float)
                rgb = ndi.uniform_filter(arr[..., :3], size=(9, 9, 1))
                wy2 = info["window"][1] + info["window"][3]
                sy, sx = int(wy2 + (im.height - wy2) * 0.45), im.width // 2
                near = (np.abs(rgb - rgb[sy, sx]).sum(axis=2) < 60) & (arr[..., 3] > 200)
                lab, _ = ndi.label(near)
                ys, xs = np.nonzero(ndi.binary_fill_holes(lab == lab[sy, sx]))
                info["caption"] = [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]
            if key == "k_panel2":
                info["inner"] = inner_rect(im)
                info["scale"] = 0.62  # тонкая рама: на экране мельче картинки, рамка в 20 с небольшим точек
            if key == "k_panel":
                info["inner"] = inner_rect(im)
                info["keep_w"] = True  # посередине верхнего и нижнего края резьба: по ширине рамку не растягиваем
            if key == "k_stats":
                # где кончаются верёвки и начинается сама вывеска
                al = np.asarray(im)[..., 3] > 128
                wide = np.nonzero(al.sum(axis=1) > im.width * 0.75)[0]
                info["body_top"] = int(wide[0]) if len(wide) else 0
            if key == "ui_badge":
                # где начинается сам пропуск: первая строка, где он шире трёх четвертей картинки
                al = np.asarray(im)[..., 3] > 128
                wide = np.nonzero(al.sum(axis=1) > im.width * 0.75)[0]
                info["body_top"] = int(wide[0]) if len(wide) else 0
                info["keep_w"] = True  # ремешки и зажим посередине: по ширине пропуск не растягиваем и не сжимаем
            sl = SLICE.get(key)
            if sl:
                info["slice"] = [round(sl[0] * im.width), round(sl[1] * im.width), round(sl[2] * im.height), round(sl[3] * im.height)]
            if key.startswith("icon_"):
                im.thumbnail((256, 256), Image.LANCZOS)
                im.save(os.path.join(ICONS, key[5:] + ".png"))
                print(f"{key}: {im.size} → web/assets/icons/{key[5:]}.png")
                continue
            im.save(os.path.join(OUT, key + ".webp"), quality=92, method=4)
            meta[key] = info
            print(f"{key}: {im.size}" + (f", края {info['slice']}" if "slice" in info else "") + (f", окно {info['window']}" if "window" in info else ""))
            if preview and sl:
                os.makedirs(preview, exist_ok=True)
                w, h = im.size
                sizes = [(w, h), (int(w * 1.8), h), (w, int(h * 1.7)), (int(w * 0.7), int(h * 0.7))]
                sheet = Image.new("RGBA", (sum(s[0] for s in sizes) + 40 * len(sizes), max(s[1] for s in sizes) + 20), (120, 60, 140, 255))
                x = 10
                for s in sizes:
                    p = nine(im, sl, *s)
                    sheet.alpha_composite(p, (x, 10))
                    x += s[0] + 40
                sheet.convert("RGB").save(os.path.join(preview, key + ".jpg"), quality=85)
    old = {}
    if os.path.exists(os.path.join(OUT, "ui.json")):
        old = json.load(open(os.path.join(OUT, "ui.json"), encoding="utf-8"))
    old.update(meta)
    json.dump(old, open(os.path.join(OUT, "ui.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("готово, вещей:", len(meta))


if __name__ == "__main__":
    main()
