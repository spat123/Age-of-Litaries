# -*- coding: utf-8 -*-
# Главный герой в четырёх возрастах (автор: «нужно сделать главного героя в младенчестве, маленьким, подростком и
# взрослым по тому, что ты сделал»). Опора — мальчик с рисунка «вопрос» (assets_src/cards_full/g_eyes.png).
# Без фона. Кладёт в assets_src/hero/hero_ages.png. Запуск из корня: python3 refs/tools/ui_gen/gen_hero.py
import os, subprocess, sys

os.makedirs("assets_src/hero", exist_ok=True)
PROMPT = ("@img1 is the main hero of our game as a boy of about eight. Draw a character sheet of the same hero at four ages, "
          "standing side by side in a row, full body, front three-quarter view, in exactly the same drawing style, "
          "colours and outline weight as @img1: a 2D animated cartoon look, clean thick outlines, flat colours with "
          "cel shading. Keep his features recognisable at every age: messy red-brown hair, round nose, big expressive "
          "eyes, a patched beige linen cap, a brown peasant vest over a rough linen shirt. From left to right: 1) a baby "
          "in linen swaddling clothes with a tiny version of the patched cap, sitting; 2) a small boy of about eight, "
          "exactly like @img1; 3) a lanky teenager of about fifteen, a bit awkward, the same cap and vest now too small; "
          "4) a young adult man of about twenty-five, the same cap, a longer vest and a belt with a small pouch. Plain "
          "pure white background, no shadow on the background, the four figures well apart from each other. No text, "
          "no letters, no numbers, no logos.")
r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", "assets_src/hero/hero_ages.png", "--size", "wide",
                    "--ref", "assets_src/cards_full/g_eyes.png", PROMPT], capture_output=True, text=True)
print((r.stdout + r.stderr).strip()[-200:])
