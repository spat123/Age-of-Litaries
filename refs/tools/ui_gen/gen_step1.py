# -*- coding: utf-8 -*-
# Шаг 1 (решение П33): тонкая рамка окна диалога и рамка аватара говорящего, по нынешней резной раме.
# Запуск из корня репозитория: python3 refs/tools/ui_gen/gen_step1.py [имена через запятую]
import os, subprocess, sys

OUT = "assets_src/ui_new2"
REF = "assets_src/ui_new2/k_panel.png"
HEAD = ("@img1 is a carved wooden frame with brass corner fittings from our game interface. Draw a new interface element "
        "in exactly the same drawing style, wood colour, brass and outline weight as @img1: ")
TAIL = (" Straight front view, flat, no perspective, centred, the whole object visible with a wide white margin around it. "
        "Plain pure white background, no shadow on the background. No text, no letters, no numbers, no symbols, no logos.")
JOBS = {
    "k_panel2": ("wide", "the same kind of frame for a dialogue box, but much lighter and slimmer: a thin carved wooden border, "
                         "about a third as thick as in @img1, with small brass caps only on the four corners and no carvings in "
                         "the middle of any edge. The cream parchment inside fills almost the whole frame and is completely "
                         "empty and evenly lit."),
    "k_avatar": ("square", "a small square frame for a character's portrait icon: a carved wooden border with brass caps on the "
                           "four corners and a small heart carving in the middle of the bottom edge. The opening inside is "
                           "filled with flat plain warm yellow, nothing else in it."),
}
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(JOBS)
for name in only:
    size, what = JOBS[name]
    print("==", name, flush=True)
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", os.path.join(OUT, name + ".png"), "--size", size,
                        "--ref", REF, HEAD + what + TAIL], capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-300:], flush=True)
print("готово")
