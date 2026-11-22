# -*- coding: utf-8 -*-
# Портреты говорящих по наброску «Сцена с героями». Codex рисует каждого по пояс, на белом фоне.
# Запуск из корня репозитория: python3 <этот файл> [имена через запятую]
import os, subprocess, sys

OUT = "assets_src/faces"
os.makedirs(OUT, exist_ok=True)
C1 = "refs/ui_mock/concepts/c1_scena_s_geroyami.png"
OLD = "assets_src/art/backgrounds_old/bg_act1_first_word.png"
CARDS = "assets_src/cards_new/"
HEAD = ("@img1 is a mockup of our game screen with a large portrait of the mother on the left. Draw a new character portrait "
        "for the same game, exactly in the drawing style of the mother in @img1: clean thick outlines in a darker shade of "
        "each colour, flat opaque colours, two or three hard-edged shading tones, fine grain, a friendly cartoon face with "
        "big expressive eyes. ")
TAIL = (" Waist-up portrait, the body turned three-quarters to the right as if talking to someone on the right, hands "
        "visible and gesturing, the figure fills the picture from the waist up with a white margin above the head. Alone on "
        "a plain pure white background, no shadow on the background, no scenery, no frame. No text, no letters, no logos.")
FACES = {
    "mom": ([C1], "The mother from @img1 herself, the same face, headscarf, brown dress and apron: proud and a little demanding, "
                  "one hand on her hip, the other pointing up as if saying 'and her son already did it'."),
    "father": ([C1, OLD], "The father of the family. Use @img2 only to see his look: a tired, kind peasant in his forties with a "
                          "short brown beard and a green-grey work tunic with rolled-up sleeves. He holds a thin tax ledger "
                          "under his arm and scratches the back of his head."),
    "merchant": ([C1], "A slick travelling village merchant: gaudy fur-trimmed coat, several rings, a thin moustache, a wide fake "
                       "friendly smile, holding out a small wooden toy on his palm as if it were a great bargain."),
    "clerk": ([C1], "A thin village church clerk: a dark cassock, small round glasses, a goose quill behind his ear, holding a "
                    "huge thick record book against his chest, prim and fussy."),
    "moms_friend": ([C1], "The mother's rich friend: a plump, well-dressed village woman with a lace collar, a fancy bonnet with "
                          "a feather and a string of beads, a smug smile, chin held high, fanning herself with a lace handkerchief."),
    "monk": ([C1], "A strict schoolmaster monk: brown habit with a rope belt, tonsure, bushy eyebrows, one eyebrow raised, "
                   "holding a long wooden pointer stick."),
    "recruiter": ([C1], "A stout village military recruiter: a big curled moustache, a dented iron helmet, a padded tunic with "
                        "brass buttons, holding a long scroll of names and a quill, looking pleased."),
    "troll": ([C1], "A big friendly bridge troll toll-collector: mossy grey-green skin, a big nose, small tusks, a tiny "
                    "toll-collector's cap, a leather coin pouch on his belt, rubbing his huge hands together."),
    "lag": ([C1, CARDS + "o_knight.png"], "Sir Lag, the knight from @img2: the same stout knight in dented, patched plate armour "
                                          "with a closed helmet and a feather, frozen mid-step as if stuck."),
}
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(FACES)
for name in only:
    refs, what = FACES[name]
    print("==", name, flush=True)
    cmd = [sys.executable, "web/tools/codex_image.py", "--out", os.path.join(OUT, name + ".png"), "--size", "tall"]
    for r in refs:
        cmd += ["--ref", r]
    r = subprocess.run(cmd + [HEAD + what + TAIL], capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-300:], flush=True)
print("готово")
