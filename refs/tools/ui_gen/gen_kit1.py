# -*- coding: utf-8 -*-
# Набор вещей интерфейса по наброску «Сцена с героями»: каждую вещь Codex вынимает из самого наброска.
# Запуск из корня репозитория: python3 <этот файл> [имена через запятую]
import os, subprocess, sys

OUT = "assets_src/ui_new2"
os.makedirs(OUT, exist_ok=True)
REF = "refs/ui_mock/concepts/c1_scena_s_geroyami.png"
HEAD = ("@img1 is a mockup of our game screen. Draw only one interface element taken from it, exactly in the same drawing "
        "style, materials, colours and outline weight as in @img1, as a clean game asset: ")
TAIL = (" Straight front view, flat, no perspective, no tilt, centred, the whole object visible with a wide white margin "
        "around it. Plain pure white background, no shadow on the background. No text, no letters, no numbers, no symbols, "
        "no logos, no squiggles.")
KIT = {
    "k_panel": ("wide", "the dialogue frame: the thick carved wooden frame with brass corner fittings around the cream parchment "
                        "page. Without the name sign on top, without the red ribbon and without the speech tail. The parchment "
                        "is completely empty and evenly lit."),
    "k_namesign": ("wide", "the small carved wooden name sign with leaf carvings at both ends that sits on the top edge of the "
                           "dialogue frame. The sign is empty."),
    "k_ribbon": ("wide", "the red cloth ribbon banner with a stitched border and small embroidered sprigs at both ends, lying "
                         "flat and straight. The ribbon is empty."),
    "k_card": ("tall", "one choice card: the ornate carved wooden card frame with the small heart carving on top and the cream "
                       "caption plate with a stitched border in the lower part. The picture window in the upper part is filled "
                       "with flat plain warm yellow with no picture at all. No number token on the corner."),
    "k_token": ("square", "the round brass number token from the top-left corner of the cards, shown large. Its face is "
                          "completely smooth and empty."),
    "k_shelf": ("wide", "the long carved wooden shelf that the cards stand on, with the small heart carving in the middle of its "
                        "front edge. Show it long and straight."),
    "k_stats": ("wide", "the hanging carved wooden sign with two short ropes from the top left. The sign is completely empty: "
                        "no icons, no bars, no carvings in the middle."),
    "k_board": ("tall", "a tall carved wooden board in the same style as the board at the top right, but empty: only the carved "
                        "frame and the flat wooden surface inside, no slots, no button."),
    "k_slot": ("square", "one empty square slot from the board at the top right: a small carved wooden frame around a darker "
                         "recessed wooden square."),
    "k_btn": ("wide", "the small carved wooden button with brass end caps from under the board, shown large. The button is empty, "
                      "no icon."),
    "k_row": ("wide", "a wide horizontal version of the choice card for a phone screen, about four times wider than tall: the "
                      "same ornate carved wooden frame, but thinner, with a square picture window on the left filled with flat "
                      "plain warm yellow, and a long cream caption plate with a stitched border taking the rest of the width on "
                      "the right. No picture, no number token."),
    "k_btn_green": ("wide", "the small carved wooden button with brass end caps from under the board, shown large, but its wooden "
                            "face is painted a fresh grass green. The button is empty, no icon."),
}
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(KIT)
for name in only:
    size, what = KIT[name]
    print("==", name, flush=True)
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", os.path.join(OUT, name + ".png"), "--size", size,
                        "--ref", REF, HEAD + what + TAIL], capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-300:], flush=True)
print("готово")
