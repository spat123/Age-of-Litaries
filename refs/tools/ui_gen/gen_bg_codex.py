# -*- coding: utf-8 -*-
# Проба: фоны мест через Codex (автор: «посмотри, насколько хорошо Codex делает фоны, и сгенерируем парочку — может
# получиться лучше»). Опора @img1 — нынешний фон этого же места (состав и рисовка), описание — из story/bg.json.
# Кладёт в refs/ui_mock/bg_codex/<фон>.png. Запуск из корня: python3 refs/tools/ui_gen/gen_bg_codex.py [фоны через запятую]
import json, subprocess, sys

BG = json.load(open("story/bg.json", encoding="utf-8"))
REF = {"bg_act1_fair": "assets_src/art/backgrounds/bg_act1_fair.png",
       "bg_home_day": "assets_src/art/backgrounds/bg_act1_first_word.png"}
# Вторая попытка (автор: «пробуем ещё, может, не так промпты написали?»). Что мешало в первой: слова «clean, flat»
# дали глянцевую мобильную картинку, а «нижняя треть пустая» — голую траву. Теперь: две опоры — тот же фон и второй
# наш фон для рисовки; упор на ручную тушь, штриховку, неровную линию, фактуру бумаги; низ не пустой, а с предметами
# по краям и землёй с фактурой; кадр 16:9 сразу. Запуск: python3 <этот файл> v2 [фоны]
# Четвёртая попытка (автор: «слишком мультяшно вышло; поставь в пример задник дома ночью и днём — может, так выйдет»):
# опоры — наши же фоны: дом снаружи в сумерках (bg_act1_birth) и изба днём (bg_home_day); автор: «у нас есть избы наши». Запуск: python3 <этот файл> v4 [фоны]
REF["bg_act1_road_camp"] = "assets_src/art/backgrounds/bg_act1_road_camp.png"
if len(sys.argv) > 1 and sys.argv[1] == "v4":
    for k in (sys.argv[2].split(",") if len(sys.argv) > 2 else ["bg_act1_fair", "bg_act1_road_camp"]):
        p = ("@img1 and @img2 are two backgrounds from our game (a cottage outside at dusk and a cottage inside by day). Draw a new "
             "background in exactly their drawing style, as if by the same artist on the same day: the same outline "
             "weight, the same amount of detail and texture, the same colour palette and lighting approach. Wide 16:9 "
             "landscape, eye-level view with depth, objects at the left and right edges in the foreground, the bottom "
             "of the picture is ground with a few small details. No people, no animals. The place: " + BG[k]["en"] +
             ". No text, no letters, no signs with writing, no logos.")
        r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", f"refs/ui_mock/bg_codex/{k}_v4.png",
                            "--size", "wide", "--ref", "assets_src/art/backgrounds/bg_act1_birth.png",
                            "--ref", "assets_src/art/backgrounds/bg_home_day.png", p], capture_output=True, text=True)
        print(k, (r.stdout + r.stderr)[-30:], flush=True)
    sys.exit(0)
# Третья попытка (автор: «стало ещё хуже; приводи в пример рисовку персонажей и предметов»): опоры — портрет мамы и
# два рисунка карточек (рисовка), третья — нынешний фон места (только что где стоит). Запуск: python3 <этот файл> v3
if len(sys.argv) > 1 and sys.argv[1] == "v3":
    for k in (sys.argv[2].split(",") if len(sys.argv) > 2 else list(REF)):
        p = ("@img1 is a character and @img2 and @img3 are objects from our game. Draw a background for our game in "
             "exactly the same drawing style as these: the same thick dark brown outline, the same chunky rounded "
             "cartoon shapes, the same flat warm colours with two-tone cel shading and small crisp highlights, the "
             "same amount of detail. @img4 shows only what this place contains and where things stand — do not copy "
             "its drawing style. Wide 16:9 landscape, eye-level view with depth: some objects in the foreground at the "
             "left and right edges; the bottom of the picture is ground or floor with a few small details. No people, "
             "no animals. The place: " + BG[k]["en"] + ". No text, no letters, no signs with writing, no logos.")
        r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", f"refs/ui_mock/bg_codex/{k}_v3.png",
                            "--size", "wide", "--ref", "assets_src/faces/mom.png", "--ref", "assets_src/cards_full/o_barn.png",
                            "--ref", "assets_src/cards_full/o_well.png", "--ref", REF[k], p], capture_output=True, text=True)
        print(k, (r.stdout + r.stderr)[-30:], flush=True)
    sys.exit(0)
V2 = len(sys.argv) > 1 and sys.argv[1] == "v2"
if V2:
    sys.argv.pop(1)
STYLE2 = "assets_src/art/backgrounds/bg_act2_city.png"
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(REF)
if V2:
    for k in only:
        p = ("@img1 and @img2 are backgrounds from our game. Draw a new background in exactly their drawing style, as if "
             "by the same artist: hand-inked dark brown outlines of slightly uneven weight, lots of fine ink hatching "
             "and cross-hatching in the shadows, textured wood grain, stone and plaster drawn with small strokes, "
             "muted earthy palette with a few warm accents, a subtle paper grain over everything; storybook comic "
             "illustration, not glossy, not a mobile game, no airbrush. Wide 16:9 landscape, eye-level view with real "
             "depth: objects in the foreground at the left and right edges, the place in the middle distance, sky or "
             "back wall far behind. The bottom of the picture is textured ground or floor with small details (stones, "
             "straw, cracks), not an empty flat area. No people, no animals. The place: " + BG[k]["en"] +
             ". No text, no letters, no signs with writing, no logos.")
        r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", f"refs/ui_mock/bg_codex/{k}_v2.png",
                            "--size", "wide", "--ref", REF[k], "--ref", STYLE2, p], capture_output=True, text=True)
        print(k, (r.stdout + r.stderr)[-30:], flush=True)
    sys.exit(0)
for k in only:
    p = ("@img1 is a background from our game. Draw a new background for our game in exactly the same drawing style as "
         "@img1: a 2D animated cartoon look, clean confident dark outlines, flat opaque colours with cel shading, chunky "
         "rounded shapes, rich hand-made details, warm light. Wide landscape, 16:9 composition, eye-level view, the "
         "lower third of the picture fairly calm and empty because game cards will cover it. No people, no animals. "
         "The place: " + BG[k]["en"] + ". No text, no letters, no signs with writing, no logos.")
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", f"refs/ui_mock/bg_codex/{k}.png", "--size",
                        "wide", "--ref", REF[k], p], capture_output=True, text=True)
    print(k, (r.stdout + r.stderr)[-30:], flush=True)
