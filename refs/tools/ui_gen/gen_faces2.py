# -*- coding: utf-8 -*-
# Торговец и монах как на присланных автором кадрах (refs/ui_mock/primer_torgovec.png, primer_monah.png): портрет в
# нашем виде — по пояс, на белом. Прежние портреты сохранены в assets_src/faces_old/.
# Запуск из корня: python3 refs/tools/ui_gen/gen_faces2.py; потом python3 web/tools/cut_faces.py merchant monk
import subprocess, sys

JOBS = {
    "merchant": ("refs/ui_mock/primer_torgovec.png", "the merchant from @img1: a plump bored trader with a big black "
                 "moustache and a short beard, a purple beret, a purple robe with yellow trim and a necklace of yellow "
                 "beads; eyes half closed, resting his cheek on his hand"),
    "monk": ("refs/ui_mock/primer_monah.png", "the monk from @img1: a bald round-faced monk with black eyebrows and a "
             "fringe of black hair, a big round nose, a black hooded habit with a rope belt; a sly thoughtful smile, "
             "his hand on his chin"),
}
for k, (ref, who) in JOBS.items():
    p = (f"Draw {who}. Keep exactly the same character design, face, clothes and colours as in @img1, but frame and "
         "draw him exactly like the portrait in @img2: waist-up, slightly turned, clean thick outlines, flat colours with "
         "cel shading, on a plain pure white background with no shadow. No text, no letters, no logos.")
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", f"assets_src/faces/{k}.png", "--size", "square",
                        "--ref", ref, "--ref", f"assets_src/faces_old/{k}.png", p], capture_output=True, text=True)
    print(k, (r.stdout + r.stderr)[-30:], flush=True)
