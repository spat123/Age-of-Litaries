#!/usr/bin/env python3
"""Увеличивает фоны вдвое программой Upscayl и кладёт их в assets_src/art/backgrounds_x2.
Исходники в assets_src/art/backgrounds не меняются. После этого запусти prepare_assets.py:
он берёт увеличенный фон, если тот есть, и делает из него картинку для игры.

Запуск из корня репозитория:
    python3 web/tools/upscale_bg.py                 — все фоны, у которых увеличенного ещё нет
    python3 web/tools/upscale_bg.py bg_well         — названные фоны заново
    python3 web/tools/upscale_bg.py --model high-fidelity-4x bg_well

Модели Upscayl:
    digital-art-4x    — чистый контур и ровная заливка, зерно в заливках пропадает. Стоит по умолчанию.
    high-fidelity-4x  — ближе к исходнику, зерно остаётся, контур мягче. Работает втрое дольше.

Нужны Pillow и установленный Upscayl (https://upscayl.org). Путь к нему можно задать переменной UPSCAYL."""
import os, subprocess, sys, tempfile, time
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SRC = os.path.join(ROOT, "assets_src", "art", "backgrounds")
OUT = os.path.join(ROOT, "assets_src", "art", "backgrounds_x2")
APP = os.environ.get("UPSCAYL", "/Applications/Upscayl.app/Contents/Resources")
BIN = os.path.join(APP, "bin", "upscayl-bin")
BIG = 1900   # фон такой ширины и больше увеличивать не надо


def main():
    args = sys.argv[1:]
    model = "digital-art-4x"
    if "--model" in args:
        i = args.index("--model")
        model = args[i + 1]
        del args[i:i + 2]
    if not os.path.exists(BIN):
        sys.exit("не нашёл Upscayl: " + BIN)
    if not os.path.exists(os.path.join(APP, "models", model + ".param")):
        sys.exit("нет такой модели: " + model)
    os.makedirs(OUT, exist_ok=True)
    only = set(args)
    names = sorted(f[:-4] for f in os.listdir(SRC) if f.endswith(".png"))
    done = 0
    for n in names:
        dst = os.path.join(OUT, n + ".jpg")
        if only and n not in only:
            continue
        if not only and os.path.exists(dst):
            continue
        src = os.path.join(SRC, n + ".png")
        w, h = Image.open(src).size
        if max(w, h) >= BIG:
            print(n, "уже большой:", (w, h))
            continue
        t = time.time()
        with tempfile.TemporaryDirectory() as tmp:
            big = os.path.join(tmp, "x2.png")
            r = subprocess.run([BIN, "-i", src, "-o", big, "-s", "2", "-m", os.path.join(APP, "models"), "-n", model, "-f", "png"],
                               capture_output=True, text=True)
            if r.returncode or not os.path.exists(big):
                print(n, "ОШИБКА:", (r.stderr or r.stdout)[-300:])
                continue
            im = Image.open(big).convert("RGB")
            im.save(dst, quality=95, subsampling=0)
        done += 1
        print(f"{n}: {(w, h)} → {im.size}, {model}, {time.time() - t:.0f} с", flush=True)
    print("готово, увеличено фонов:", done)


if __name__ == "__main__":
    main()
