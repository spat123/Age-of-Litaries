#!/usr/bin/env python3
"""Собирает страницу refs/kartinki.html: все рисунки карточек, которые нужны игре, с готовыми запросами
для генератора картинок, по очереди важности. Заодно пишет тот же список в assets_src/CARDS.md.
Описания рисунков лежат в story/art.json. Скрипт проверяет, что описан каждый рисунок, который нужен сюжету.
Запуск из корня репозитория: python3 refs/tools/build_art_page.py"""
import glob, html, io, json, os, sys
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
STORY = os.path.join(ROOT, "story")
OUT = os.path.join(ROOT, "refs", "kartinki.html")
OUT_MD = os.path.join(ROOT, "assets_src", "CARDS.md")
HAVE_DIR = os.path.join(ROOT, "web", "assets", "cards")
E = html.escape
# Рисунки, которые есть, но их надо сделать заново, и почему.
REDO = {}
# Рисунки, которые стоят в игре, но их можно подтянуть, и почему.
MAYBE = {
    "o_goblin_box": "гоблин зелёный, с большими ушами и седыми клочками: может напомнить известного киногероя. "
                    "Спокойнее дать ему бороду, шапку и уши поменьше",
}

# Слова о рисовке — те же, что в art_style.md §6.
STYLE = ("Background and prop art for a 2D animated cartoon series. Clean, confident outlines of medium weight, drawn in a darker shade "
         "of each object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with "
         "hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, "
         "simplified shapes. Clear daylight from the upper left with flat cast shadows. Natural, balanced colours with neutral white "
         "balance: off-white, grey-brown wood, terracotta, moss green and clear blue; shadows are cool blue-grey.")
NEG = ("No text, no letters, no numbers, no logos, no brand marks, no watermark, no interface elements, no frame. No watercolour, "
       "no paper texture, no sketchy pencil lines, no painterly brush strokes. No yellow tint, no sepia cast over the picture. "
       "Not a photo, not a 3D render, not pixel art, no modern objects.")
REF = ("Use @img1 only as a style reference. Copy only its drawing style: clean outlines in a darker shade of each colour, flat opaque "
       "colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.")


def full_prompt(en):
    return (STYLE + "\n\nOne simple subject, alone in the centre of a plain white background, with only a small flat shadow under it: "
            + en + ". Square 1:1.\n\n" + NEG)


def ref_prompt(en):
    return REF + "\n\nDraw: " + en + ".\n\nAlone on a plain white background with a small flat shadow. Square 1:1. No text, no logos, no frame."


LIKE = ("Use @img1 as the model. Draw the same subject as in @img1, in exactly the same drawing style, with the same shapes, "
        "outline weight and colours, and change only this: ")


def like_prompt(en):
    """Запрос по образцу другого нашего рисунка: его и надо приложить как @img1."""
    return LIKE + en + ".\n\nAlone on a plain white background with a small flat shadow. Square 1:1. No text, no logos, no frame."


def load(name):
    return json.load(io.open(os.path.join(STORY, name), encoding="utf-8"))


def collect():
    use = defaultdict(list)

    def walk(cs):
        for c in cs:
            use[c["art"]].append(c["label"])
            if "then" in c:
                walk(c["then"]["choices"])
    for f in sorted(glob.glob(os.path.join(STORY, "ch*.json"))):
        for s in json.load(io.open(f, encoding="utf-8"))["scenes"]:
            walk(s.get("choices", []))
    after = load("afterlife.json")
    for k in ("microloan", "promotion", "hr"):
        walk(after[k].get("choices", []))
    cards = {k: v for k, v in load("cards.json").items() if k[0] != "_"}
    for v in cards.values():
        use[v["art"]].append("карточка «" + v["name"] + "»")
    return use


def main():
    use = collect()
    art = {k: v for k, v in load("art.json").items() if k[0] != "_"}
    bad = sorted(k for k, v in art.items() if v.get("like") and v["like"] not in art)
    if bad:
        sys.exit("в story/art.json поле like указывает на рисунок, которого нет: " + ", ".join(bad))
    missing = sorted(set(use) - set(art))
    extra = sorted(set(art) - set(use))
    if missing:
        sys.exit("в story/art.json не описаны рисунки: " + ", ".join(missing))
    have = {os.path.splitext(f)[0] for f in os.listdir(HAVE_DIR)} if os.path.isdir(HAVE_DIR) else set()
    have -= set(REDO)   # такие считаем несделанными
    def state(k):
        if k in have:
            return "есть" + (", по желанию: " + MAYBE[k] if k in MAYBE else "")
        return REDO.get(k, "нет")

    order = sorted(use, key=lambda k: (-len(use[k]), k))
    total = sum(len(v) for v in use.values())

    # три пачки: половина всех мест, три четверти, остальное
    batches, acc, cur, cuts = [[], [], []], 0, 0, (0.5, 0.75)
    for k in order:
        batches[cur].append(k)
        acc += len(use[k])
        if cur < 2 and acc / total >= cuts[cur]:
            cur += 1
    names = ["Пачка 1. Самые частые: после неё рисунок будет на каждой второй карточке",
             "Пачка 2. После неё рисунок будет на трёх карточках из четырёх",
             "Пачка 3. Редкие и особые"]

    blocks, md = [], ["# Рисунки карточек", "",
                      "Список собран скриптом `refs/tools/build_art_page.py` из `story/art.json`. Руками не править.", "",
                      f"Всего рисунков: {len(order)}. Готово: {len([k for k in order if k in have])}.", ""]
    for bi, (title, ids) in enumerate(zip(names, batches)):
        cover = sum(len(use[k]) for b in batches[:bi + 1] for k in b)
        md += [f"## {title}", "", f"Рисунков: {len(ids)}. Вместе с прошлыми пачками закрывает {100 * cover // total}% мест.", "",
               "| Файл | Что нарисовано | Сколько раз нужен | Есть |", "|---|---|---|---|"]
        items = []
        for k in ids:
            a, n = art[k], len(use[k])
            where = "; ".join(dict.fromkeys(use[k]))
            like = a.get("like")
            md.append(f"| `{k}.png` | {a['ru']}" + (f" (по образцу `{like}`)" if like else "") + f" | {n} | {state(k)} |")
            items.append(
                f'<article class="pic{" done" if k in have else ""}"><header><h3>{E(a["ru"])}</h3>'
                f'<span class="file">{E(k)}.png</span><span class="n">нужен {n} раз</span>'
                f'<span class="st">{E(state(k))}</span></header>'
                f'<p class="where">{E(where[:260])}{"…" if len(where) > 260 else ""}</p>'
                + (f'<p class="where"><b>Этот рисунок делается по образцу другого нашего.</b> Возьми короткий запрос и приложи как '
                   f'<code>@img1</code> файл <code>assets_src/cards_new/{E(like)}.png</code>, а не образец рисовки.</p>' if like else "")
                + f'<pre class="p full">{E(full_prompt(a["en"]))}</pre><pre class="p ref" hidden>{E(like_prompt(a["en"]) if like else ref_prompt(a["en"]))}</pre>'
                f'<button type="button" class="copy">Скопировать запрос</button></article>')
        md.append("")
        blocks.append(f'<section><h2>{E(title)}</h2><p class="lead">Рисунков: {len(ids)}. Вместе с прошлыми пачками закрывает '
                      f'{100 * cover // total}% мест, где в игре нужен рисунок.</p>' + "".join(items) + "</section>")
    page = (TEMPLATE.replace("{{BODY}}", "\n".join(blocks)).replace("{{N}}", str(len(order)))
            .replace("{{HAVE}}", str(len([k for k in order if k in have]))).replace("{{USES}}", str(total)))
    io.open(OUT, "w", encoding="utf-8").write(page)
    io.open(OUT_MD, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"готово: {os.path.relpath(OUT)}, {os.path.relpath(OUT_MD)} · рисунков {len(order)}, готово {len([k for k in order if k in have])}, "
          f"пачки: {[len(b) for b in batches]}" + (f" · в art.json лишние: {extra}" if extra else ""))


TEMPLATE = r'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Сэр Баг — рисунки карточек</title>
<style>
:root{--bg:#f4efe4;--card:#fffdf7;--ink:#2a2118;--mute:#6f6253;--line:#d9cdb8;--acc:#9a3b1e;--ok:#2f6b3a;--okbg:#e6f0e2}
@media (prefers-color-scheme:dark){:root{--bg:#1b1713;--card:#25201a;--ink:#efe6d6;--mute:#a99c88;--line:#3a3229;--acc:#e08a5c;--ok:#9bd0a2;--okbg:#1f2e22}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:28px 16px 80px}
h1{font:700 30px/1.15 Georgia,serif;margin:0 0 6px}
h2{font:700 22px/1.25 Georgia,serif;margin:44px 0 4px;padding-top:14px;border-top:2px solid var(--ink)}
h3{font:700 18px/1.25 Georgia,serif;margin:0}
.lead{color:var(--mute);margin:0 0 16px;max-width:72ch}
ol{padding-left:22px;max-width:74ch} li{margin:5px 0}
code{background:var(--card);border:1px solid var(--line);border-radius:5px;padding:0 5px}
.sw{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 0;display:flex;gap:18px;flex-wrap:wrap;align-items:center}
.sw label{cursor:pointer}
.pic{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:0 0 14px}
.pic.done{border-color:var(--ok)}
.pic header{display:flex;gap:10px 14px;flex-wrap:wrap;align-items:baseline}
.file{font:14px ui-monospace,Menlo,monospace;color:var(--acc)}
.n,.st{font-size:14px;color:var(--mute)}
.pic.done .st{color:var(--ok);font-weight:700}
.where{margin:6px 0 8px;color:var(--mute);font-size:14px}
pre.p{white-space:pre-wrap;word-break:break-word;margin:0 0 10px;padding:10px 12px;background:var(--bg);border:1px solid var(--line);border-radius:8px;font:13px/1.45 ui-monospace,Menlo,monospace;max-height:9.5em;overflow:auto}
button.copy{font:600 15px inherit;color:#fff;background:var(--acc);border:0;border-radius:8px;padding:8px 14px;cursor:pointer}
button.copy.ok{background:var(--ok)}
</style></head><body><div class="wrap">
<h1>Сэр Баг — рисунки карточек</h1>
<p class="lead">Игре нужно {{N}} рисунков, они стоят в {{USES}} местах. Готово: {{HAVE}}. Рисунки идут по очереди важности: чем выше, тем чаще он виден в игре.</p>
<ol>
<li>Нажми «Скопировать запрос» и сгенерируй картинку 1:1. Предмет один, на белом фоне.</li>
<li>Сохрани картинку под именем из карточки, например <code>g_coins.png</code>, в папку <code>assets_src/cards_new/</code>.</li>
<li>Скажи мне. Я запущу скрипт: он уберёт белый фон и положит рисунок в игру.</li>
</ol>
<div class="sw"><b>Какой запрос показывать:</b>
<label><input type="radio" name="v" value="full" checked> полный, без опорной картинки</label>
<label><input type="radio" name="v" value="ref"> короткий, с опорой <code>@img1</code></label></div>
{{BODY}}
</div>
<script>
document.querySelectorAll('input[name=v]').forEach(r=>r.addEventListener('change',()=>{
  document.querySelectorAll('pre.p').forEach(p=>p.hidden=!p.classList.contains(r.value));}));
document.addEventListener('click',e=>{const b=e.target.closest('button.copy');if(!b)return;
  const p=b.parentElement.querySelector('pre.p:not([hidden])');
  navigator.clipboard.writeText(p.textContent).then(()=>{b.textContent='Скопировано';b.classList.add('ok');
    setTimeout(()=>{b.textContent='Скопировать запрос';b.classList.remove('ok')},1500)});});
</script>
</body></html>'''

if __name__ == "__main__":
    main()
