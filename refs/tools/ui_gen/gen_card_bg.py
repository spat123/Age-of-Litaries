# -*- coding: utf-8 -*-
# Фоны с лучами под рисунки карточек (автор: «можешь делать фоны в таком стиле, как тут фоны — просто попробуем»;
# образец — первые рисунки с нарисованным фоном, refs/ui_mock/primer_fony_luchi.png). По одному фону на цвет;
# игра берёт фон ближайшего цвета. Кладёт в assets_src/card_bg/<цвет>.png. Запуск: python3 refs/tools/ui_gen/gen_card_bg.py
import subprocess, sys

COLS = {"red": "bright red", "orange": "bright orange", "yellow": "warm golden yellow", "green": "bright grass green",
        "teal": "deep teal", "blue": "bright royal blue", "purple": "rich purple", "pink": "hot pink"}
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(COLS)
for k in only:
    p = ("@img1 shows card pictures from our game. Draw only the background of such a card picture, in exactly the same "
         f"drawing style as the backgrounds in @img1: a {COLS[k]} square filled edge to edge, with bold radiating speed "
         "lines bursting from a point slightly below the centre, the lines are sharp tapered spikes in lighter tints of "
         "the same colour and a few in pale cream yellow, a brighter glow at the centre, slightly darker towards the "
         "corners, a subtle paper grain. No subject, no object, no character, no frame, no border. No text, no letters, "
         "no numbers, no logos.")
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", f"assets_src/card_bg/{k}.png", "--size", "square",
                        "--ref", "refs/ui_mock/primer_fony_luchi.png", p], capture_output=True, text=True)
    print(k, (r.stdout + r.stderr)[-30:], flush=True)
