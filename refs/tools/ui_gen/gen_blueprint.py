# -*- coding: utf-8 -*-
# Бирюзовый чертёж для «системы» по наброску «Мир в разработке»: рамка экрана, прибор-лист, портреты Бога и ангела.
# Всё рисуется светящимися линиями на чёрном: в игре чёрное становится прозрачным (сложение цветов).
# Запуск из корня репозитория: python3 <этот файл> [имена через запятую]
import os, subprocess, sys

REF = "refs/ui_mock/concepts/c3_mir_v_razrabotke.png"
HEAD = ("@img1 is a mockup of our game screen where the medieval world is an unfinished software build, with glowing "
        "turquoise blueprint lines. Draw a new element in exactly the same turquoise blueprint line style as in @img1: thin "
        "clean glowing turquoise lines, a few brighter accents, measurement ticks and arrows, corner brackets. ")
TAIL = (" Everything is drawn only with turquoise lines on a plain pure black background; no other colours, no fill, no "
        "scenery. No text, no letters, no numbers, no logos.")
JOBS = {
    "b_frame": ("assets_src/ui_new2", "wide", "A frame for the whole game screen: thin double turquoise border along all four "
                "edges with corner brackets in each corner, rows of small measurement ticks along the edges, a few dimension "
                "arrows, and a faint perspective grid only near the edges that fades out toward the centre. The centre of the "
                "picture is completely empty black."),
    "b_panel": ("assets_src/ui_new2", "wide", "A wide dialogue panel drawn as a wireframe: a rounded rectangle with a double "
                "outline, small square selection handles on its corners and in the middle of each side, a dimension line with "
                "arrows above its top edge and another one along its right edge. The inside of the panel is empty black."),
    "god": ("assets_src/faces", "tall", "A waist-up portrait of the God-Developer who builds this world: an old wise man with "
            "a long beard and a hooded robe, a halo that looks like a loading circle, holding a long quill like a stylus, "
            "turned three-quarters to the right as if talking to someone on the right, calm and a little tired. Drawn as a "
            "blueprint sketch with construction lines."),
    "angel": ("assets_src/faces", "tall", "A waist-up portrait of an angel clerk from the heavenly personnel office: neat "
              "short hair, small wings, a simple robe with a name-badge shape on the chest, holding a thick file folder and a "
              "pen, turned three-quarters to the right, politely smiling. Drawn as a blueprint sketch with construction lines."),
}
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(JOBS)
for name in only:
    out, size, what = JOBS[name]
    os.makedirs(out, exist_ok=True)
    print("==", name, flush=True)
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", os.path.join(out, name + ".png"), "--size", size,
                        "--ref", REF, HEAD + what + TAIL], capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-300:], flush=True)
print("готово")
