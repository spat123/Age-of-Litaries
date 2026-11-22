# -*- coding: utf-8 -*-
# Круглая рамка аватара говорящего (автор: «рамку для аватар круглую сделаем», пример — портрет в кольце из Hades II:
# refs/ui_mock/primer_koltso.png). Форму берём из примера, материал и рисовку — из нашей рамки аватара.
# Запуск из корня репозитория: python3 refs/tools/ui_gen/gen_avatar_round.py
import subprocess, sys

PROMPT = ("@img1 is an example of a round portrait frame from another game, shown only for its shape. @img2 is the portrait "
          "frame from our game. Draw one empty round portrait frame for our game as a clean game asset. Its shape follows "
          "@img1: a perfect circle, a thick ring divided into ten separate segments by small even gaps, with a thin outer "
          "rim and a thin inner rim. It is drawn in the materials, colours, drawing style and outline weight of @img2: the "
          "segments are warm carved wood, the rims are polished brass, thick dark outlines, and a small carved heart sits "
          "on the bottom of the ring. The round opening inside the ring is filled with flat plain warm yellow and nothing "
          "else. Straight front view, flat, centred, the whole object visible with a wide white margin around it. Plain "
          "pure white background, no shadow on the background. No text, no letters, no numbers, no logos. Do not copy any "
          "existing game's interface.")
# Вторая попытка (автор: «рамка толстая»): та же рамка, кольцо примерно вдвое тоньше. Опора — первая, толстая рамка,
# она сохранена в refs/ui_mock/k_avatar_round_tolstaya.png. Запуск: python3 <этот файл> thin
if len(sys.argv) > 1 and sys.argv[1] == "thin":
    PROMPT = ("@img1 is the round portrait frame from our game. Draw exactly the same frame again, in exactly the same "
              "drawing style, materials, colours and outline weight, with the same ten carved wooden segments, the "
              "polished brass rims and the small carved heart at the bottom, but make the ring about half as thick, so "
              "the round opening inside becomes much larger. The round opening is filled with flat plain warm yellow and "
              "nothing else. Straight front view, flat, centred, the whole object visible with a wide white margin "
              "around it. Plain pure white background, no shadow on the background. No text, no letters, no numbers, "
              "no logos.")
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", "assets_src/ui_new2/k_avatar_round.png",
                        "--size", "square", "--ref", "refs/ui_mock/k_avatar_round_tolstaya.png", PROMPT],
                       capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-300:])
    sys.exit(0)
r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", "assets_src/ui_new2/k_avatar_round.png", "--size",
                    "square", "--ref", "refs/ui_mock/primer_koltso.png", "--ref", "assets_src/ui_new2/k_avatar.png", PROMPT],
                   capture_output=True, text=True)
print((r.stdout + r.stderr).strip()[-300:])
