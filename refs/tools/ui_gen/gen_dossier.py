# -*- coding: utf-8 -*-
# Стол небесного чиновника и раскрытая папка (набросок «Личное дело», решение П32): для страниц «Личное дело» и «Итог жизни».
# Запуск из корня репозитория: python3 <этот файл> [имена через запятую]
import os, subprocess, sys

REF = "refs/ui_mock/concepts/c2_lichnoe_delo.png"
HEAD = ("@img1 is a mockup of our game screen: a personnel file on an old oak desk. Draw a new picture in exactly the same "
        "drawing style, materials and colours as in @img1: clean thick outlines in a darker shade of each colour, flat opaque "
        "colours, two or three hard-edged shading tones, fine grain. ")
JOBS = {
    "d_desk": ("wide", "The empty top of the same old oak desk seen straight from above, filling the whole picture: warm wood "
               "planks with grain. Only along the edges lie a few objects: a candle in a brass holder in the bottom right corner, "
               "an inkwell with a goose quill and a wooden rubber stamp in the top right corner, a small stack of blank papers in "
               "the top left corner, a few loose paper clips. The whole middle of the desk is empty wood. Warm candle light, cool "
               "shadows. No text, no letters, no numbers, no logos."),
    "d_folder": ("wide", "The same open thick cardboard personnel folder with a metal clip at the top centre, seen straight from "
                 "above, alone on a plain pure white background: two wide blank cream paper pages side by side, slightly worn "
                 "edges, a few paper tabs sticking out on the right side. Both pages are completely empty. No paper clip, no "
                 "photo, no stamps. No text, no letters, no numbers, no logos."),
}
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(JOBS)
os.makedirs("assets_src/ui_new2", exist_ok=True)
for name in only:
    size, what = JOBS[name]
    print("==", name, flush=True)
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", os.path.join("assets_src/ui_new2", name + ".png"),
                        "--size", size, "--ref", REF, HEAD + what], capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-300:], flush=True)
print("готово")
