# -*- coding: utf-8 -*-
# Гербы титулов (автор: «титулы я бы оформил нормально — тоже можно сгенерить в виде гербов»).
# Один герб на титул, в нашей рисовке значков; на белом. Кладёт в assets_src/crests/<титул>.png.
# Запуск из корня: python3 refs/tools/ui_gen/gen_crests.py [титулы через запятую]
import subprocess, sys

CRESTS = {
    "obey": "Obedient: a pale blue shield with a neatly folded pair of praying hands and a small halo above, a white "
            "ribbon below",
    "rebel": "Rebel: a dark red shield with a raised clenched fist breaking a chain, a torn black ribbon below",
    "deal": "Dealer: a green shield with a pair of scales and a stack of gold coins, a gold ribbon below",
    "invent": "Inventor: a purple shield with a pig carrying a wooden shovel and a cog wheel behind it, a ribbon below",
    "tinfoil": "Conspiracy believer: a dark teal shield with a tin bucket worn as a hat and a watchful eye, a ribbon below",
    "team": "Soul of the village: a warm orange shield with a little thatched hut and a big red heart above it, a "
            "ribbon below",
}
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(CRESTS)
for k in only:
    p = ("@img1 shows game icons in our style. Draw one heraldic coat of arms as a game badge in exactly the same drawing "
         "style: a 2D cartoon look, clean thick dark outline, bold flat colours with two-tone cel shading and crisp "
         "highlights. A sturdy shield with a carved wooden and brass rim, a small brass crown or helmet on top, a curling "
         "blank ribbon banner under it. The emblem: " + CRESTS[k] + ". Humorous medieval village heraldry, chunky and "
         "readable at small size. Centred on a plain pure white background, no shadow. No text, no letters on the ribbon, "
         "no numbers, no logos.")
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", f"assets_src/crests/{k}.png", "--size", "square",
                        "--ref", "refs/ui_mock/primer_ikonki.png", p], capture_output=True, text=True)
    print(k, (r.stdout + r.stderr)[-20:], flush=True)
