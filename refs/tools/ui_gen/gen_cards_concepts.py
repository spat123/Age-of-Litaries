# -*- coding: utf-8 -*-
# Три варианта карточек выбора с рисунком «как на наброске» и особой рамкой (автор выбрал «Карты и особая рамка»
# после образцов Hades II). Опоры: @img1 — набросок «Сцена с героями» (рисунок внутри карточек, который нравится
# автору), @img2 — нынешний экран игры (наша резная рама, полка, изба).
# Запуск из корня репозитория: python3 refs/tools/ui_gen/gen_cards_concepts.py [имена через запятую]
import os, subprocess, sys

OUT = "refs/ui_mock/cards"
os.makedirs(OUT, exist_ok=True)
REFS = ["refs/ui_mock/concepts/c1_scena_s_geroyami.png", "refs/ui_mock/now_mama.jpg"]

HEAD = ("A close-up mockup of the lower half of the game screen of a satirical medieval card-choice game, wide 3:2: "
        "four choice cards stand side by side on the carved wooden shelf from @img2, the cottage interior behind them "
        "is slightly darkened. Drawing style of @img1: a 2D animated cartoon look, clean confident thick outlines in a "
        "darker shade of each colour, flat opaque colours, cel shading with two or three hard-edged tones, chunky "
        "rounded shapes.\n\n"
        "The first three cards are ordinary choices, the fourth card on the right is a rare special card. Each picture "
        "is big, close-up and full of motion, cropped by the window edge, on a bold coloured background with radiating "
        "speed lines, like the cards in @img1: 1) a boy's wide-open shouting mouth with a speech bubble, on red; "
        "2) a hand pointing forward with a questioning gesture, on blue; 3) a finger pressed to lips, on purple; "
        "4) a black crow with a tiny brass spyglass, slyly watching, on deep night teal. Each card has a round brass "
        "token on its top-left corner, left blank.\n\n")
TAIL = ("\n\nNo readable text anywhere: the caption plates are blank, the tokens have no digits. No logos, no brand "
        "marks. Do not copy the interface or the cards of any existing game.")
JOBS = {
    "v1_reznaya": "Cards: each card keeps the carved wooden frame with a small heart carving on top from @img2 and a blank "
                  "parchment caption plate at the bottom, but the picture window is larger and the picture fills it "
                  "completely. The special card has the same shape, but its frame is gilded gold with small red gems, "
                  "it glows with a warm golden light, thin rays and sparkling dust come out from behind it, and a small "
                  "gold star medallion sits on its top edge.",
    "v2_vsya_karta": "Cards: each card is a full-art card. The picture fills the whole card edge to edge, framed only by a "
                     "thin carved wooden border with small brass corners. The caption is a blank cream ribbon laid across "
                     "the lower part of the picture, and a round wooden medallion sits at the bottom centre of the border. "
                     "The special card: its thin border is gold with gems on the corners, a glowing outline of warm magic "
                     "light runs around it with floating sparkles and a soft halo, and it stands a little higher than the "
                     "others.",
    "v3_arka": "Cards: each card is shaped like a tall arched window. The top of the painted wooden frame is a rounded "
               "arch with simple carving, the picture sits inside the arch, and the caption is a blank paper scroll "
               "across the bottom of the card. The special card: the arch is gold, a radiant sunburst of light rays "
               "fans out behind the card, small stars twinkle along the frame, and a red wax seal on a ribbon hangs from "
               "the bottom.",
}
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(JOBS)
for name in only:
    print("==", name, flush=True)
    cmd = [sys.executable, "web/tools/codex_image.py", "--out", os.path.join(OUT, name + ".png"), "--size", "wide"]
    for r in REFS:
        cmd += ["--ref", r]
    r = subprocess.run(cmd + [HEAD + JOBS[name] + TAIL], capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-300:], flush=True)
print("готово")
