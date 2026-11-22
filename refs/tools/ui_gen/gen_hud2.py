# -*- coding: utf-8 -*-
# Новые значки показателей и закруглённая ячейка под уникальные карточки (автор: «иконки надо перерисовать…
# карточки горизонтально слева внизу, как в Хейдес, и можно сделать рамки новые под них закруглённые, как в Хейдес —
# бери пример оттуда»). Пример формы ячейки — крупный план иконки дара из Hades II (refs/screens/ui/hades2/crops/).
# Запуск из корня репозитория: python3 refs/tools/ui_gen/gen_hud2.py [имена через запятую]
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

OUT = "assets_src/ui_new2"
TAIL = (" Plain pure white background, no shadow on the background. No text, no letters, no numbers, no logos. "
        "Do not copy any existing game's icons.")
JOBS = {
    # лист из четырёх значков 2×2 режет cut_ui.py (SPLIT "ui_icons2") в web/assets/icons/
    "ui_icons2": ("square", ["assets_src/ui_new/ui_icons.png", "refs/ui_mock/concepts/c1_scena_s_geroyami.png"],
                  "@img1 shows the four stat icons of our game: a heart (health), a brain (mind), a wheat sheaf crossed "
                  "with a pitchfork (reputation among the peasants) and a stack of gold coins (money). Redraw the same four "
                  "ideas as a new, better icon set in the drawing style of @img2: a 2D animated cartoon look, clean "
                  "confident thick outlines in a darker shade of each colour, flat opaque colours with cel shading in two or "
                  "three hard-edged tones and a crisp highlight, chunky rounded shapes. They are game HUD icons shown small, "
                  "about 48 pixels, next to a number, so each must read instantly as a bold simple silhouette with few inner "
                  "details, slightly turned, with a little volume. The heart is a plump glossy red heart; the brain is a "
                  "pink brain; the reputation icon is a golden wheat sheaf tied with a band, crossed with a wooden "
                  "pitchfork; the money icon is a small stack of three thick gold coins. Arrange them in a 2 by 2 grid: heart "
                  "top left, brain top right, wheat and pitchfork bottom left, coins bottom right, each well apart from the "
                  "others with plenty of white space. No circles or frames behind the icons."),
    "k_slot2": ("square", ["refs/screens/ui/hades2/crops/c_dar_ikonka.jpg", "assets_src/ui_new2/k_card2.png"],
                "@img1 is an example of an icon frame from another game, shown only for its shape. @img2 is a card frame "
                "from our game. Draw one empty icon frame for our game as a clean game asset. Its shape follows @img1: a "
                "square with strongly rounded corners and a thick, even rim. It is drawn in the materials, colours, "
                "drawing style and outline weight of @img2: the rim is dark polished wood with visible grain and a thin "
                "brass inner edge, with a thick dark outline. The opening inside the rim is filled with flat plain warm "
                "yellow and nothing else. Straight front view, flat, centred, the whole object visible with a wide white "
                "margin around it."),
}


def run(name):
    size, refs, what = JOBS[name]
    cmd = [sys.executable, "web/tools/codex_image.py", "--out", os.path.join(OUT, name + ".png"), "--size", size]
    for r in refs:
        cmd += ["--ref", r]
    r = subprocess.run(cmd + [what + TAIL], capture_output=True, text=True)
    return name + ": " + (r.stdout + r.stderr).strip()[-250:]


only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(JOBS)
with ThreadPoolExecutor(len(only)) as ex:
    for line in ex.map(run, only):
        print(line, flush=True)
print("готово")
