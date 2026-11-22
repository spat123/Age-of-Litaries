#!/usr/bin/env python3
"""Собирает страницу refs/fony.html: все фоны, которые нужны игре, с готовыми запросами для генератора картинок.
Заодно пишет тот же список в assets_src/BACKGROUNDS.md. Описания фонов лежат в story/bg.json.
Скрипт проверяет, что описан каждый фон, который нужен сюжету.
Запуск из корня репозитория: python3 refs/tools/build_bg_page.py"""
import glob, html, io, json, os, sys
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
STORY = os.path.join(ROOT, "story")
OUT = os.path.join(ROOT, "refs", "fony.html")
OUT_MD = os.path.join(ROOT, "assets_src", "BACKGROUNDS.md")
HAVE_DIR = os.path.join(ROOT, "web", "assets", "bg")
E = html.escape
# Фоны, которые надо сделать заново: причина по-русски и подсказка, которая дописывается к запросу.
FULLER = ("The middle is calm but not empty: the walls and the floor are filled with small everyday things, "
          "and nothing in the picture is a large bare surface")
REDO = {}   # имя фона: (причина по-русски, подсказка по-английски для запроса). 15.11.2026 все семь переделок приняты
# Фоны, которые можно оставить, но лучше подтянуть.
SIMPLE = ("Rich in small details, with fine hatching and wear on wood, stone and cloth, the same amount of detail as in @img1")
MAYBE = {}  # то же самое

# Слова о рисовке — те же, что в art_style.md §6.
STYLE = ("Background and prop art for a 2D animated cartoon series. Clean, confident outlines of medium weight, drawn in a darker shade "
         "of each object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with "
         "hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, "
         "simplified shapes. Clear light from the upper left with flat cast shadows. Age and wear are drawn with line and flat patches: "
         "cracks, chipped paint, plank seams, scuffs. Natural, balanced colours with neutral white balance: off-white plaster, "
         "grey-brown wood, terracotta, moss green and clear blue; shadows are cool blue-grey.")
NEG = ("No people, no characters. No text, no letters, no numbers, no logos, no brand marks, no watermark, no speech bubbles, "
       "no interface elements, no frame. No watercolour, no paper texture, no sketchy pencil lines, no painterly brush strokes. "
       "No yellow tint, no sepia cast over the picture. Not a photo, not a 3D render, not pixel art, no modern objects.")
REF = ("Use @img1 only as a style reference. Copy only its drawing style: clean outlines in a darker shade of each colour, flat opaque "
       "colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the place, the composition or any details from @img1.")
SHAPE = {"wide": "Wide 16:9. The middle of the picture is calm and uncluttered, the important details sit at the sides",
         "tall": "Tall 9:16 for a phone screen. The main subject sits in the middle third of the height; the top third and the bottom third are calm and uncluttered"}


def prompt(kind, shape, en, more=""):
    more = (" " + more + ".") if more else ""
    if kind == "full":
        return STYLE + "\n\nA background for a game scene, an empty place without people: " + en + ". " + SHAPE[shape] + "." + more + "\n\n" + NEG
    return REF + "\n\nDraw: " + en + ".\n\nAn empty place without people. " + SHAPE[shape] + "." + more + " No text, no letters, no logos, no frame."


def load(name):
    return json.load(io.open(os.path.join(STORY, name), encoding="utf-8"))


def main():
    use = defaultdict(list)
    for f in sorted(glob.glob(os.path.join(STORY, "ch*.json"))):
        ch = json.load(io.open(f, encoding="utf-8"))
        for s in ch["scenes"]:
            use[s["bg"]].append("глава " + ch["id"][2:] + ", «" + s["title"] + "»")
    after = load("afterlife.json")
    for k in ("microloan", "promotion", "hr"):
        use[after[k]["bg"]].append("после жизни, «" + after[k].get("title", k) + "»")
    bg = {k: v for k, v in load("bg.json").items() if k[0] != "_"}
    missing = sorted(set(use) - set(bg))
    if missing:
        sys.exit("в story/bg.json не описаны фоны: " + ", ".join(missing))
    extra = sorted(set(bg) - set(use))
    have = {os.path.splitext(f)[0] for f in os.listdir(HAVE_DIR)} if os.path.isdir(HAVE_DIR) else set()

    def status(k):
        if k in REDO:
            return "redo", "переделать: " + REDO[k][0]
        if k in MAYBE and k in have:
            return "maybe", "по желанию: " + MAYBE[k][0]
        if k in have:
            return "have", "есть" + ("" if k + "_tall" in have else ", высокого для телефона нет")
        return "none", "нет своего рисунка, пока стоит «" + bg[bg[k]["now"]]["ru"] + "»" if bg[k].get("now") else "нет"

    order = sorted(use, key=lambda k: (-len(use[k]), k))
    groups = [("Нет своего фона", "Эти места сейчас показаны чужим фоном. Их стоит нарисовать первыми.", [k for k in order if status(k)[0] == "none"]),
              ("Переделать", "С рисунком что-то не так. Причина написана у каждого, а в запрос уже дописано, чего не хватило в прошлый раз.", [k for k in order if status(k)[0] == "redo"]),
              ("По желанию", "Эти фоны в игре стоят и смотрятся нормально, но рядом с остальными проигрывают. Переделывать не обязательно.", [k for k in order if status(k)[0] == "maybe"]),
              ("Есть", "Фоны на месте. Запрос нужен, если захочешь перерисовать фон или сделать высокий для телефона.", [k for k in order if status(k)[0] == "have"])]
    blocks, md = [], ["# Фоны", "", "Список собран скриптом `refs/tools/build_bg_page.py` из `story/bg.json`. Руками не править.", "",
                      f"Всего фонов: {len(order)}. Своего рисунка нет у {len(groups[0][2])}, переделать надо {len(groups[1][2])}, по желанию {len(groups[2][2])}.", ""]
    for title, lead, ids in groups:
        if not ids:
            continue
        md += [f"## {title}", "", lead, "", "| Файл | Место | В каких сценах | Состояние |", "|---|---|---|---|"]
        items = []
        for k in ids:
            st, text = status(k)
            where = "; ".join(use[k])
            md.append(f"| `{k}.png` | {bg[k]['ru']} | {where} | {text} |")
            more = (REDO.get(k) or MAYBE.get(k) or ("", ""))[1]
            pres = "".join(f'<pre class="p {kind} {shape}"{"" if (kind, shape) == ("ref", "wide") else " hidden"}>{E(prompt(kind, shape, bg[k]["en"], more))}</pre>'
                           for kind in ("full", "ref") for shape in ("wide", "tall"))
            items.append(f'<article class="pic {st}"><header><h3>{E(bg[k]["ru"])}</h3>'
                         f'<span class="file"><span class="fw">{E(k)}.png</span><span class="ft" hidden>{E(k)}_tall.png</span></span>'
                         f'<span class="n">сцен: {len(use[k])}</span><span class="st">{E(text)}</span></header>'
                         f'<p class="where">{E(where)}</p>{pres}<button type="button" class="copy">Скопировать запрос</button></article>')
        md.append("")
        blocks.append(f'<section><h2>{E(title)} — {len(ids)}</h2><p class="lead">{E(lead)}</p>' + "".join(items) + "</section>")
    page = (TEMPLATE.replace("{{BODY}}", "\n".join(blocks)).replace("{{N}}", str(len(order))).replace("{{NONE}}", str(len(groups[0][2])))
            .replace("{{REDO}}", str(len(groups[1][2]))).replace("{{MAYBE}}", str(len(groups[2][2]))))
    io.open(OUT, "w", encoding="utf-8").write(page)
    io.open(OUT_MD, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"готово: {os.path.relpath(OUT)}, {os.path.relpath(OUT_MD)} · фонов {len(order)}: нет своего {len(groups[0][2])}, переделать {len(groups[1][2])}, по желанию {len(groups[2][2])}, есть {len(groups[3][2])}"
          + (f" · в bg.json лишние: {extra}" if extra else ""))


TEMPLATE = r'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Сэр Баг — фоны</title>
<style>
:root{--bg:#f4efe4;--card:#fffdf7;--ink:#2a2118;--mute:#6f6253;--line:#d9cdb8;--acc:#9a3b1e;--ok:#2f6b3a;--warn:#a05a00}
@media (prefers-color-scheme:dark){:root{--bg:#1b1713;--card:#25201a;--ink:#efe6d6;--mute:#a99c88;--line:#3a3229;--acc:#e08a5c;--ok:#9bd0a2;--warn:#e0b060}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:28px 16px 80px}
h1{font:700 30px/1.15 Georgia,serif;margin:0 0 6px}
h2{font:700 22px/1.25 Georgia,serif;margin:44px 0 4px;padding-top:14px;border-top:2px solid var(--ink)}
h3{font:700 18px/1.25 Georgia,serif;margin:0}
.lead{color:var(--mute);margin:0 0 16px;max-width:72ch}
ol{padding-left:22px;max-width:76ch} li{margin:5px 0}
code{background:var(--card);border:1px solid var(--line);border-radius:5px;padding:0 5px}
.sw{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 0;display:grid;gap:4px}
.sw div{display:flex;gap:6px 18px;flex-wrap:wrap;align-items:center}
.sw label{cursor:pointer}
.pic{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:0 0 14px}
.pic header{display:flex;gap:6px 14px;flex-wrap:wrap;align-items:baseline}
.file{font:14px ui-monospace,Menlo,monospace;color:var(--acc)}
.n,.st{font-size:14px;color:var(--mute)}
.pic.have .st{color:var(--ok)} .pic.redo .st,.pic.none .st{color:var(--warn);font-weight:600} .pic.maybe .st{color:var(--warn)}
.where{margin:6px 0 8px;color:var(--mute);font-size:14px}
pre.p{white-space:pre-wrap;word-break:break-word;margin:0 0 10px;padding:10px 12px;background:var(--bg);border:1px solid var(--line);border-radius:8px;font:13px/1.45 ui-monospace,Menlo,monospace;max-height:11em;overflow:auto}
button.copy{font:600 15px inherit;color:#fff;background:var(--acc);border:0;border-radius:8px;padding:8px 14px;cursor:pointer}
button.copy.ok{background:var(--ok)}
</style></head><body><div class="wrap">
<h1>Сэр Баг — фоны</h1>
<p class="lead">Игре нужно {{N}} фонов. Переделать надо {{REDO}}, по желанию можно подтянуть ещё {{MAYBE}}, без своего рисунка осталось {{NONE}}. Остальные на месте.</p>
<ol>
<li>Выбери вверху вид запроса и форму картинки. Нажми «Скопировать запрос» и сгенерируй фон.</li>
<li>Сохрани картинку под именем из карточки, например <code>bg_well.png</code>, в папку <code>assets_src/art/backgrounds/</code>. Высокий фон для телефона называется так же, но с <code>_tall</code> на конце.</li>
<li>Скажи мне. Я запущу скрипт, который уменьшит фон и положит его в игру. Если фон выйдет жёлтым, поправлю его другим скриптом.</li>
</ol>
<div class="sw">
<div><b>Запрос:</b>
<label><input type="radio" name="kind" value="ref" checked> короткий, с опорой <code>@img1</code></label>
<label><input type="radio" name="kind" value="full"> полный, без опорной картинки</label></div>
<div><b>Форма:</b>
<label><input type="radio" name="shape" value="wide" checked> широкий 16:9, для компьютера</label>
<label><input type="radio" name="shape" value="tall"> высокий 9:16, для телефона</label></div>
</div>
{{BODY}}
</div>
<script>
const val=n=>document.querySelector('input[name='+n+']:checked').value;
function show(){const k=val('kind'),s=val('shape');
  document.querySelectorAll('pre.p').forEach(p=>p.hidden=!(p.classList.contains(k)&&p.classList.contains(s)));
  document.querySelectorAll('.fw').forEach(e=>e.hidden=s!=='wide');document.querySelectorAll('.ft').forEach(e=>e.hidden=s!=='tall');}
document.querySelectorAll('.sw input').forEach(r=>r.addEventListener('change',show));
document.addEventListener('click',e=>{const b=e.target.closest('button.copy');if(!b)return;
  const p=b.parentElement.querySelector('pre.p:not([hidden])');
  navigator.clipboard.writeText(p.textContent).then(()=>{b.textContent='Скопировано';b.classList.add('ok');
    setTimeout(()=>{b.textContent='Скопировать запрос';b.classList.remove('ok')},1500)});});
</script>
</body></html>'''

if __name__ == "__main__":
    main()
