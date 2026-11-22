# -*- coding: utf-8 -*-
# Три варианта рисунка «песок» (автор: «рука с песком не очень, надо править. Давай несколько вариантов»).
# Кладёт в assets_src/cards_full_var/o_sand_v<N>.png; выбранный копируется в assets_src/cards_full/o_sand.png.
# Запуск из корня репозитория: python3 refs/tools/ui_gen/gen_sand_var.py
import subprocess, sys

s = open("refs/tools/ui_gen/gen_card_art.py", encoding="utf-8").read()
ns = {}
exec(s[s.index("CLEAN = ("):s.index("JOBS_CLEAN = {")], ns)
TAIL = " No text, no letters, no numbers, no logos."
VARS = {
    1: ("assets_src/cards_full/g_coins.png",
        "a peasant boy's hand in a rough linen sleeve seen from the side in the middle of a throw, drawn exactly like the "
        "hand in @img2: the arm swings forward, the fingers just opened, a cloud of golden sand bursting out in a wide arc "
        "with a few speed lines."),
    2: ("assets_src/cards_full/g_coins.png",
        "a peasant boy's hand drawn exactly like the hand in @img2, held up and slowly opening, a thin stream of golden "
        "sand pouring down from between the fingers into a small pile below, a few grains sparkling."),
    3: ("assets_src/hero/hero_ages.png",
        "the boy from @img2 (the eight-year-old) with a sly grin throwing a handful of sand straight at the viewer, the "
        "sand flying towards us in a big golden spray. Head, shoulders and the throwing arm."),
}
for n, (ref, what) in VARS.items():
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", f"assets_src/cards_full_var/o_sand_v{n}.png",
                        "--size", "square", "--ref", "refs/ui_mock/cards/v3_arka.png", "--ref", ref,
                        ns["CLEAN"] + what + TAIL], capture_output=True, text=True)
    print(n, (r.stdout + r.stderr)[-40:], flush=True)
