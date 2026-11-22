#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает весь наш интерфейс в одну папку для Фигмы (автор: «где лежит UI весь наш — накидаю сам в Фигме»):
refs/ui_figma/ — PNG с прозрачным фоном (вещи интерфейса, значки, портреты, рисунки карт), фоны в JPG и README.
Берёт готовые файлы игры из web/assets/. Запуск из корня репозитория: python3 -I refs/tools/export_figma.py [кадры...]
Кадры экрана (jpg), если переданы, кладутся в 7_ekran_seychas/."""
import os, shutil, site, sys
sys.path.append(site.getusersitepackages())
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
A = os.path.join(ROOT, "web", "assets")
OUT = os.path.join(ROOT, "refs", "ui_figma")

# что стоит на экране сейчас: ключ — что это
NOW = {
    "k_panel2": "окно диалога (тонкая рама; тянется: края не растягивать, середину можно)",
    "k_namesign": "табличка с именем говорящего",
    "k_ribbon": "красная лента с названием сцены",
    "k_avatar_round": "круглая рамка аватара говорящего (окно внутри прозрачное)",
    "k_card2": "карточка выбора: окно под рисунок 1:1 и табличка под текст",
    "k_card2_gold": "особая карточка выбора: золото, камни, печать",
    "k_token": "латунная бляха с номером карточки",
    "k_slot2": "закруглённая ячейка уникальной карточки (столбик слева)",
    "k_btn": "деревянная кнопка («Личное дело», «Меню»)",
    "k_btn_green": "зелёная кнопка («Дальше»)",
    "ui_note": "записка «Цель главы»",
    "ui_sheet": "листок подсказки и рамка страниц",
    "ui_stamp_great": "печать «отлично» на итоге",
    "ui_stamp_ok": "печать «так себе» на итоге",
    "ui_stamp_shame": "печать «позор» на итоге",
    "k_row": "строка выбора на телефоне",
    "k_shelf": "резная полка внизу экрана телефона",
    "b_frame": "«система»: бирюзовая рамка-чертёж по краю экрана (линии на чёрном, в игре чёрное пропадает)",
    "b_panel": "«система»: окно-чертёж (линии на чёрном)",
    "ui_system": "рамка страниц «системы»",
    "d_desk": "стол чиновника под папкой «Личное дело»",
    "d_folder": "раскрытая папка «Личное дело»",
}
# нарисовано раньше, на экране сейчас не стоит
OLD = {
    "k_panel": "толстая резная рама окна диалога (была до шага 1)",
    "k_avatar": "квадратная рамка аватара (была до круглой)",
    "k_card": "резная карточка с сердцем (была до новой)",
    "k_board": "доска «Карточки» справа вверху",
    "k_stats": "вывеска с показателями на верёвках",
    "k_slot": "квадратная ячейка на доске",
    "ui_badge": "пропуск с показателями (первый набор)",
    "ui_board": "доска (первый набор)",
    "ui_btn_wood": "кнопка (первый набор)",
    "ui_btn_green": "зелёная кнопка (первый набор)",
    "ui_card": "карточка (первый набор)",
    "ui_plate": "табличка (первый набор)",
    "ui_ribbon": "лента (первый набор)",
    "ui_result": "лист итога с печатью (первый набор)",
    "ui_shelf": "полка (первый набор)",
}
STAT = {"body": "сердце — здоровье", "mind": "мозг — ум", "rep": "колосья — репутация", "gold": "монеты — деньги",
        "star": "серебряная звезда — метка особого выбора"}


def png(src, dst):
    Image.open(src).save(dst)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    lines = ["# Интерфейс «Сэр Баг» для Фигмы", "",
             "Собрано скриптом `refs/tools/export_figma.py` из готовых файлов игры (`web/assets/`). Всё с прозрачным фоном, "
             "кроме фонов и кадров. Имя файла — это имя вещи в коде, так проще вернуть вещь в игру.", "",
             "Шрифты игры (Google Fonts): Balsamiq Sans — подписи, кнопки и числа; Alice — текст сцен; Ruslan Display — "
             "заголовки; PT Mono — речь «системы».", ""]
    for folder, title, items in (("1_seychas_v_igre", "Стоит на экране сейчас", NOW), ("2_staroe", "Нарисовано раньше, сейчас не стоит", OLD)):
        os.makedirs(os.path.join(OUT, folder))
        lines += ["## " + title, "", "| Файл | Что это | Размер |", "|---|---|---|"]
        for k, what in items.items():
            src = os.path.join(A, "ui", k + ".webp")
            if not os.path.exists(src):
                continue
            dst = os.path.join(OUT, folder, k + ".png")
            png(src, dst)
            w, h = Image.open(dst).size
            lines.append(f"| `{folder}/{k}.png` | {what} | {w}×{h} |")
        lines.append("")
    os.makedirs(os.path.join(OUT, "3_znachki"))
    lines += ["## Значки показателей", "", "Ободок вокруг значка и число рядом рисует код.", ""]
    for k, what in STAT.items():
        shutil.copy(os.path.join(A, "icons", k + ".png"), os.path.join(OUT, "3_znachki", k + ".png"))
        lines.append(f"- `3_znachki/{k}.png` — {what}")
    lines.append("")
    os.makedirs(os.path.join(OUT, "4_portrety"))
    n = 0
    for f in sorted(os.listdir(os.path.join(A, "faces"))):
        if f.endswith(".webp"):
            png(os.path.join(A, "faces", f), os.path.join(OUT, "4_portrety", f[5:-5] + ".png"))
            n += 1
    lines += ["## Портреты говорящих", "", f"`4_portrety/` — {n} шт., во весь рост до пояса; в игре из них вырезается голова для аватара.", ""]
    os.makedirs(os.path.join(OUT, "5_risunki_kart"))
    n = 0
    for f in sorted(os.listdir(os.path.join(A, "cards"))):
        if f.endswith(".webp"):
            png(os.path.join(A, "cards", f), os.path.join(OUT, "5_risunki_kart", f[:-5] + ".png"))
            n += 1
    lines += ["## Рисунки на карточках", "", f"`5_risunki_kart/` — {n} шт. Это нынешние рисунки (вещь на прозрачном фоне); их ещё будут перерисовывать 1:1.", ""]
    os.makedirs(os.path.join(OUT, "6_fony"))
    n = 0
    for f in sorted(os.listdir(os.path.join(A, "bg"))):
        if f.endswith(".webp"):
            Image.open(os.path.join(A, "bg", f)).convert("RGB").save(os.path.join(OUT, "6_fony", f[:-5] + ".jpg"), quality=90)
            n += 1
    lines += ["## Фоны", "", f"`6_fony/` — {n} шт., 1920 точек в ширину.", ""]
    shots = sys.argv[1:]
    if shots:
        os.makedirs(os.path.join(OUT, "7_ekran_seychas"))
        for s in shots:
            shutil.copy(s, os.path.join(OUT, "7_ekran_seychas", os.path.basename(s)))
        lines += ["## Экран сейчас", "", "`7_ekran_seychas/` — кадры игры: широкий экран 1920×1080 и телефон 1080×1920.", ""]
    lines += ["## Откуда это и куда класть новое", "",
              "- Готовые вещи для игры: `web/assets/ui/*.webp` (+ `ui.json`: где окно, какие края не тянуть).",
              "- Исходники вещей, как их нарисовал Codex (белый фон): `assets_src/ui_new2/` (нынешний набор) и `assets_src/ui_new/` (первый).",
              "- Новую вещь из Фигмы класть в `assets_src/ui_new2/<имя>.png` на белом фоне и запускать `python3 web/tools/cut_ui.py` — он вырежет фон и найдёт окно.",
              ""]
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write("\n".join(lines))
    print("готово:", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
