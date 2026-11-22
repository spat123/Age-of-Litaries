#!/usr/bin/env python3
"""Рисует одну картинку через Codex (он входит в приложение ChatGPT и работает от его аккаунта) и кладёт её в нужный файл.

Запуск из корня репозитория:
    python3 web/tools/codex_image.py --out assets_src/cards_new/g_eyes_shut.png --ref assets_src/cards_new/g_eyes.png "запрос"
    python3 web/tools/codex_image.py --out ... --prompt-file запрос.txt --size wide

--ref  — опорная картинка, можно несколько. В запросе их можно называть @img1, @img2, как на страницах refs/kartinki.html
         и refs/fony.html: скрипт заменит это на «первая/вторая приложенная картинка».
--size — square (1:1, по умолчанию), wide (3:2), tall (2:3).

Каждая картинка тратит лимит аккаунта ChatGPT. Codex запускается так, что ничего не может менять на диске: он только рисует.
Готовая картинка у Codex лежит в ~/.codex/generated_images, скрипт копирует её в --out."""
import argparse, os, shutil, subprocess, sys, tempfile, time

CODEX = os.environ.get("CODEX", "/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex")
GEN = os.path.expanduser("~/.codex/generated_images")
SHAPE = {"square": "square 1:1 (1024x1024)", "wide": "landscape 3:2 (1536x1024)", "tall": "portrait 2:3 (1024x1536)"}
WRAP = ("Generate exactly one image with your image generation tool. Shape: {shape}.\n"
        "Do not run shell commands and do not create, edit or delete any files. "
        "When the image is ready, answer with the single word DONE.\n\nThe image:\n{prompt}")


def images():
    out = {}
    for root, _, files in os.walk(GEN):
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                p = os.path.join(root, f)
                out[p] = os.path.getmtime(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="?")
    ap.add_argument("--prompt-file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--size", choices=SHAPE, default="square")
    ap.add_argument("--timeout", type=int, default=600)
    a = ap.parse_args()
    prompt = open(a.prompt_file, encoding="utf-8").read() if a.prompt_file else a.prompt
    if not prompt:
        sys.exit("нужен запрос")
    if not os.path.exists(CODEX):
        sys.exit("не нашёл Codex: " + CODEX)
    for i, r in enumerate(a.ref, 1):
        if not os.path.exists(r):
            sys.exit("нет опорной картинки: " + r)
        prompt = prompt.replace("@img%d" % i, ("the first", "the second", "the third", "the fourth")[min(i, 4) - 1] + " attached image")
    before = images()
    t = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [CODEX, "exec", "--skip-git-repo-check", "-s", "read-only", "-C", tmp, "--color", "never"]
        for r in a.ref:
            cmd += ["-i", os.path.abspath(r)]
        cmd += ["-o", os.path.join(tmp, "last.txt"), WRAP.format(shape=SHAPE[a.size], prompt=prompt)]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=a.timeout, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            sys.exit("Codex не успел за %d с" % a.timeout)
        last = open(os.path.join(tmp, "last.txt"), encoding="utf-8").read().strip() if os.path.exists(os.path.join(tmp, "last.txt")) else ""
    new = sorted((m, p) for p, m in images().items() if p not in before or before[p] != m)
    if not new:
        sys.exit("картинки нет. Ответ Codex: " + (last or (r.stderr or r.stdout)[-800:]))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    shutil.copyfile(new[-1][1], a.out)
    print("готово за %d с: %s (из %s)" % (time.time() - t, a.out, new[-1][1]) + ("" if len(new) == 1 else "; Codex нарисовал %d, взята последняя" % len(new)))


if __name__ == "__main__":
    main()
