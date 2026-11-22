#!/usr/bin/env python3
"""Собирает страницу refs/veshchi.html: запросы на рисованные вещи интерфейса с кнопкой «Скопировать».
Сами запросы берёт из ui_design.md, раздел 8 — там их и надо править. К каждой вещи показывает,
какую картинку из refs/ui_ref приложить как форму.
Запуск из корня репозитория: python3 refs/tools/build_ui_page.py"""
import glob, html, io, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SRC = os.path.join(ROOT, "ui_design.md")
OUT = os.path.join(ROOT, "refs", "veshchi.html")
E = html.escape

STYLE = ("Background and prop art for a 2D animated cartoon series. Clean, confident, thick outlines drawn in a darker shade of each "
         "object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with "
         "hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, "
         "simplified shapes. Natural, balanced colours with neutral white balance; shadows are cool blue-grey.")
NEG = ("No watercolour, no paper texture, no sketchy pencil lines, no painterly brush strokes. No yellow tint, no sepia cast. "
       "Not a photo, not a 3D render, not pixel art.")
SHAPE_LINE = "Take the shape, the proportions and the layout of the object from @img2, but redraw it completely in the drawing style of @img1."


def main():
    text = io.open(SRC, encoding="utf-8").read()
    items = re.findall(r"\*\*(И\d+)\. ([^*\n]+)\*\* · ([^·\n]+) · в игре будет `([^`]+)`\s*\n\n```\n(.*?)\n```", text, re.S)
    if not items:
        sys.exit("в ui_design.md не найдены запросы раздела 8")
    shapes = {int(os.path.basename(f).split("_")[1]): os.path.basename(f) for f in glob.glob(os.path.join(ROOT, "refs", "ui_ref", "shape_*.jpg"))}
    cards = []
    for num, name, ratio, fname, block in items:
        parts = block.split("\n\n")
        if len(parts) != 3 or not parts[1].startswith("Draw a game interface element: "):
            sys.exit("запрос %s записан не так, как остальные" % num)
        style, draw, tail = parts
        subject = draw[len("Draw a game interface element: "):]
        full = STYLE + "\n\nA single game interface element: " + subject + "\n\n" + tail + " " + NEG
        one = block
        two = style + " " + SHAPE_LINE + "\n\n" + draw + "\n\n" + tail
        shape = shapes.get(int(num[1:]), "")
        cards.append(
            f'<article class="pic"><header><h3>{E(num)}. {E(name.strip())}</h3><span class="file">{E(fname)}</span>'
            f'<span class="n">{E(ratio.strip())}</span></header>'
            f'<p class="where one" hidden>Приложи одну картинку: <code>refs/ui_ref/style_1_izba.png</code> — это <code>@img1</code>.</p>'
            f'<p class="where two" hidden>Приложи две картинки по порядку: сначала <code>refs/ui_ref/style_1_izba.png</code> (это <code>@img1</code>), потом <code>refs/ui_ref/{E(shape)}</code> (это <code>@img2</code>).</p>'
            f'<p class="where full">Картинки прикладывать не нужно.</p>'
            f'<pre class="p full">{E(full)}</pre><pre class="p one" hidden>{E(one)}</pre><pre class="p two" hidden>{E(two)}</pre>'
            f'<button type="button" class="copy">Скопировать запрос</button></article>')
    io.open(OUT, "w", encoding="utf-8").write(TEMPLATE.replace("{{BODY}}", "".join(cards)).replace("{{N}}", str(len(items))))
    print(f"готово: {os.path.relpath(OUT)} · вещей {len(items)}, набросков формы {len(shapes)}")


TEMPLATE = r'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Сэр Баг — вещи интерфейса</title>
<style>
:root{--bg:#f4efe4;--card:#fffdf7;--ink:#2a2118;--mute:#6f6253;--line:#d9cdb8;--acc:#9a3b1e;--ok:#2f6b3a}
@media (prefers-color-scheme:dark){:root{--bg:#1b1713;--card:#25201a;--ink:#efe6d6;--mute:#a99c88;--line:#3a3229;--acc:#e08a5c;--ok:#9bd0a2}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:28px 16px 80px}
h1{font:700 30px/1.15 Georgia,serif;margin:0 0 6px}
h3{font:700 18px/1.25 Georgia,serif;margin:0}
.lead{color:var(--mute);margin:0 0 16px;max-width:72ch}
ol{padding-left:22px;max-width:76ch} li{margin:5px 0}
code{background:var(--card);border:1px solid var(--line);border-radius:5px;padding:0 5px}
.sw{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 0;margin-bottom:18px;display:flex;gap:6px 18px;flex-wrap:wrap;align-items:center}
.sw label{cursor:pointer}
.pic{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:0 0 14px}
.pic header{display:flex;gap:6px 14px;flex-wrap:wrap;align-items:baseline}
.file{font:14px ui-monospace,Menlo,monospace;color:var(--acc)}
.n{font-size:14px;color:var(--mute)}
.where{margin:6px 0 8px;color:var(--mute);font-size:14px}
pre.p{white-space:pre-wrap;word-break:break-word;margin:0 0 10px;padding:10px 12px;background:var(--bg);border:1px solid var(--line);border-radius:8px;font:13px/1.45 ui-monospace,Menlo,monospace;max-height:11em;overflow:auto}
button.copy{font:600 15px inherit;color:#fff;background:var(--acc);border:0;border-radius:8px;padding:8px 14px;cursor:pointer}
button.copy.ok{background:var(--ok)}
</style></head><body><div class="wrap">
<h1>Сэр Баг — вещи интерфейса</h1>
<p class="lead">{{N}} вещей, из которых собран экран. Сейчас они нарисованы кодом; эти запросы — чтобы нарисовать их по-настоящему. Картинки-опоры лежат в папке <code>refs/ui_ref/</code>.</p>
<ol>
<li>Выбери вверху, сколько картинок прикладываешь. Под названием вещи написано, какие именно и в каком порядке.</li>
<li>Нажми «Скопировать запрос» и сгенерируй. Вещь должна быть видна спереди, на белом фоне, без букв.</li>
<li>Сохрани под именем из карточки и пришли мне. Я вырежу фон, нарежу края и подключу вместо кодовой.</li>
</ol>
<div class="sw"><b>Опоры:</b>
<label><input type="radio" name="v" value="full"> без картинок</label>
<label><input type="radio" name="v" value="one"> одна: <code>@img1</code> — рисовка</label>
<label><input type="radio" name="v" value="two" checked> две: <code>@img1</code> — рисовка, <code>@img2</code> — форма</label></div>
{{BODY}}
</div>
<script>
function show(){const v=document.querySelector('input[name=v]:checked').value;
  document.querySelectorAll('pre.p,.where').forEach(p=>p.hidden=!p.classList.contains(v));}
document.querySelectorAll('input[name=v]').forEach(r=>r.addEventListener('change',show));show();
document.addEventListener('click',e=>{const b=e.target.closest('button.copy');if(!b)return;
  const p=b.parentElement.querySelector('pre.p:not([hidden])');
  navigator.clipboard.writeText(p.textContent).then(()=>{b.textContent='Скопировано';b.classList.add('ok');
    setTimeout(()=>{b.textContent='Скопировать запрос';b.classList.remove('ok')},1500)});});
</script>
</body></html>'''

if __name__ == "__main__":
    main()
