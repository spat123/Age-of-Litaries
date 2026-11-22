# -*- coding: utf-8 -*-
# Новая рамка карточки выбора (автор: «Обычные карты рамки надо сделать как в примере… будет фон самих картинок
# 1 к 1 примерно — и место под неё надо оставить, и внизу место под текст»; «ворон классный в 3» — особая карта
# золотая, с печатью). Пример рамки, который прислал автор: refs/ui_mock/cards/primer_ramki.png.
# Запуск из корня репозитория: python3 refs/tools/ui_gen/gen_card2.py [имена через запятую]
import os, subprocess, sys

OUT = "assets_src/ui_new2"
TAIL = (" Straight front view, flat, no perspective, no tilt, centred, the whole object visible with a wide white margin "
        "around it. Plain pure white background, no shadow on the background. No text, no letters, no numbers, no symbols, "
        "no logos, no squiggles.")
SHAPE = ("The card is tall, about two units wide and three units tall. Upper part: a square picture opening, exactly as wide "
         "as it is tall, taking almost the whole width of the card, filled with flat plain warm yellow and nothing else. "
         "Lower part: below the opening, separated from it by one plank of the frame, a large cream parchment caption plate "
         "with a thin stitched border, about a third of the card's height, completely empty and evenly lit.")
JOBS = {
    "k_card2": ("refs/ui_mock/cards/primer_ramki.png",
                "@img1 shows a choice card from our game mockup. Draw one empty choice card frame as a clean game asset, in "
                "exactly the same drawing style, materials, colours and outline weight as the card in @img1: a sturdy frame "
                "of thick brown wooden planks with visible wood grain, joined at the corners, with a round dark iron rivet in "
                "each of the four corners. " + SHAPE),
    "k_card2_gold": ("assets_src/ui_new2/k_card2.png",
                     "@img1 is the choice card frame from our game. Draw the rare special version of exactly the same card, "
                     "with exactly the same shape, proportions, square opening and caption plate as @img1, in the same "
                     "drawing style and outline weight: the planks are polished gold with engraved ornament, a small red gem "
                     "sits in each corner instead of the iron rivet, and a round red wax seal is pressed onto the middle of "
                     "the bottom plank of the frame, inside the frame outline. " + SHAPE),
}
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(JOBS)
for name in only:
    ref, what = JOBS[name]
    print("==", name, flush=True)
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", os.path.join(OUT, name + ".png"), "--size", "tall",
                        "--ref", ref, what + TAIL], capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-300:], flush=True)
print("готово")
