# -*- coding: utf-8 -*-
# Отдельные значки для ячеек уникальных карточек, где большой рисунок мелко не читается (автор: «Можно просто зуб
# сделать. Просто ноты. Рука — ХЗ»). Одна вещь крупно, на белом; prepare_card_full.py берёт их вместо рисунка.
# Кладёт в assets_src/card_icons_src/<рисунок>.png. Запуск из корня: python3 refs/tools/ui_gen/gen_card_icons.py
import subprocess, sys

JOBS = {
    "o_tooth": "one small white baby tooth, big and simple, slightly shiny, with a tiny sparkle.",
    "g_sing": "three colourful musical notes flying together, bold and simple.",
    "o_scar": "an old jagged scar mark like a crooked line with a few cross stitches, on a small patch of skin, as a "
              "simple bold emblem.",
    # автор: «ооо, давай иконку ворона и телефона тогда тоже поменяем, хорошо получилось»
    # автор: «нужно сделать мини-иконку ведра на голову»
    "o_foil_hat": "a dented grey tin bucket turned upside down to be worn as a hat, with a rope chin strap, bold and "
                  "simple, no person.",
    "o_birds": "the head of a sly black crow peeking through a small brass spyglass, bold and simple.",
    "o_wooden_phone": "a small smartphone made of grey tree bark seen from the back, with a carved turnip on it and a "
                      "knot hole for a camera, a turquoise glow at its edge, bold and simple.",
    # автор: «меню сделать шестерёнкой как-то или ещё как — делаю меню иконку»; кладётся в web/assets/icons/menu.png
    "menu_gear": "a round button of dark polished wood with a thin brass rim, a bold cream-white gear cog in the middle.",
    # автор: «можно не делать круг, а просто гайку с деревянной текстурой — сейчас выбивается»
    "menu_gear2": "a single gear cog carved from warm brown wood with visible wood grain, eight chunky teeth and a round "
                  "hole in the middle, slightly turned, no circle or button behind it.",
}
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(JOBS)
for k, what in [(k, JOBS[k]) for k in only]:
    p = ("@img1 shows game icons in our style. Draw one small game item icon in exactly the same drawing style: a 2D "
         "cartoon look, clean thick dark outline, flat bright colours with two tones of cel shading, a crisp highlight; "
         "a bold simple silhouette that reads at 64 pixels: " + what + " Centred, filling most of the square, on a plain "
         "pure white background, no shadow. No text, no letters, no numbers, no logos.")
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", f"assets_src/card_icons_src/{k}.png",
                        "--size", "square", "--ref", "refs/ui_mock/primer_ikonki.png", p], capture_output=True, text=True)
    print(k, (r.stdout + r.stderr)[-20:], flush=True)
