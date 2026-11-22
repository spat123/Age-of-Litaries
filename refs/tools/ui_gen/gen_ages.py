# -*- coding: utf-8 -*-
# Рисунки с героем по возрасту (автор: «надо начальные переделать — типа мы ещё не знаем героя; после рождения, во время
# детства, должны быть картинки младенца»). Та же задумка, что у обычного рисунка, но герой другой:
#   __soul — до рождения (глава 0, «Сборка»): герой ещё не собран — серый безликий манекен-заготовка;
#   __baby — младенчество (глава 1): младенец с листа героя.
# Кладёт в assets_src/cards_full/<рисунок>__soul.png / __baby.png; игра берёт их по главе.
#   __teen — юность (глава 3), __adult — дорога, карьера, дракон (главы 4–6).
# Запуск из корня: python3 refs/tools/ui_gen/gen_ages.py [soul|baby|teen|adult] [имена через запятую]
import subprocess, sys

s = open("refs/tools/ui_gen/gen_card_art.py", encoding="utf-8").read()
ns = {}
exec(s[s.index("CLEAN = ("):s.index("JOBS_CLEAN = {")], ns)
TAIL = " No text, no letters, no numbers, no logos."
SOUL = ("the same idea and pose as in @img2, but the character is not born yet and has no identity: replace the boy with "
        "a plain smooth grey unfinished placeholder figure, like a featureless default mannequin, no hair, no clothes, "
        "only two simple dot eyes and a small mouth for expression, a few faint construction lines on it.")
BABY = ("the same idea and pose as in @img2, but the character is the baby from @img3: chubby, in linen swaddling "
        "clothes and the tiny patched cap, with baby proportions and baby hands.")
TEEN = ("the same idea and pose as in @img2, but the character is the lanky teenager of about fifteen from @img3: the same "
        "messy red-brown hair and patched cap, a vest now too small, longer limbs, teenage face.")
ADULT = ("the same idea and pose as in @img2, but the character is the young adult man of about twenty-five from @img3: "
         "the same messy red-brown hair and patched cap, a longer vest, a belt with a small pouch, adult face and hands.")
# автор: «Да, нарисуй» — подросток для главы 3 (юность), взрослый для глав 4–6 (дорога, карьера, дракон)
TEEN_JOBS = ["g_eyes", "g_mouth", "g_pray", "g_shout", "g_silence", "g_sit", "g_walk_by", "o_foil_hat", "o_wooden_sword"]
ADULT_JOBS = ["g_eyes", "g_fist", "g_hug", "g_mouth", "g_pray", "g_run", "g_shout", "g_silence", "g_sing", "g_sit",
              "g_walk_by", "o_foil_hat", "o_sand", "o_wooden_sword"]
SOUL_JOBS = ["g_eyes", "g_run", "g_pray", "g_hand_take", "g_sit", "g_point"]
BABY_JOBS = ["g_cry", "g_eyes", "g_hug", "g_mouth", "g_point", "g_run", "g_shout", "g_silence", "g_sing", "g_sit",
             "g_tongue"]
kind = sys.argv[1] if len(sys.argv) > 1 else "both"
todo = ([("soul", k) for k in SOUL_JOBS] if kind in ("soul", "both") else []) + \
       ([("baby", k) for k in BABY_JOBS] if kind in ("baby", "both") else []) + \
       ([("teen", k) for k in TEEN_JOBS] if kind == "teen" else []) + \
       ([("adult", k) for k in ADULT_JOBS] if kind == "adult" else [])
if len(sys.argv) > 2:
    todo = [t for t in todo if t[1] in sys.argv[2].split(",")]
for age, k in todo:
    src = "assets_src/cards_full/" + k + ".png"
    refs = ["--ref", "refs/ui_mock/cards/v3_arka.png", "--ref", src]
    if age != "soul":
        refs += ["--ref", "assets_src/hero/hero_ages.png"]
    what = {"soul": SOUL, "baby": BABY, "teen": TEEN, "adult": ADULT}[age]
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", f"assets_src/cards_full/{k}__{age}.png",
                        "--size", "square"] + refs + [ns["CLEAN"] + what + TAIL], capture_output=True, text=True)
    print(age, k, (r.stdout + r.stderr)[-25:], flush=True)
