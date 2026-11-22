#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает страницу refs/hades2.html: образцы интерфейса Hades II — рамки, иконки, карты — и что из них можно взять.
Картинки качает refs/tools/fetch_hades2.py. Запуск из корня: python3 -I refs/tools/build_hades2_page.py"""
import base64, html, io, os, site, sys
sys.path.append(site.getusersitepackages())
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "screens", "ui", "hades2")
OUT = os.path.join(HERE, "..", "hades2.html")
E = html.escape

SUMMARY = [
    "Всё собрано из одного набора: тёмная плашка, фигурный край, кованые уголки. Окно разговора, строки выбора и плитки — родня друг другу.",
    "Важное выделено рамой, цветом и светом, а не размером: редкий дар — другим цветом строки, важный говорящий — золотой рамой, включённая карта — свечением.",
    "Иконка всегда сидит в своей рамке, а в углу рамки — маленький знак, откуда она.",
    "Пустого места мало: рисунок занимает всю карту, текст плотный и короткий.",
    "Подача тёмная. Наша игра светлая и тёплая, поэтому берём формы и приёмы, а не темноту. Вещи и героев не берём.",
]

# (якорь, заголовок, картинки, что сильного, что можно взять к нам)
SECTIONS = [
    ("talk", "Окно разговора", ["crops/i_gekata_okno", "video/04_razgovor_dora", "steam/02"],
     "Окно — тёмная плашка с фигурным краем: сверху завитки-«рога», по углам кованые уголки. Табличка с именем вросла "
     "в верхний край окна, это одна вещь, а не две. Под именем — звание мелкими буквами другого цвета. У имени свой "
     "узорный шрифт. Герой стоит слева крупно, окно — справа внизу.",
     "Звание под именем говорящего (например, «Мама — главный аналитик сравнений»). Табличку имени сделать частью рамы окна, "
     "а не отдельной дощечкой. Фигурный край окна — из нашего резного дерева."),
    ("gold", "Своя рама у важных", ["crops/a_zevs_rama", "video/01_razgovor_zevs_zolotaya_rama"],
     "У Зевса окно другое: светлый мрамор в золотой лавровой раме. С первого взгляда ясно, что говорит кто-то важный, "
     "ещё до того, как прочтёшь имя.",
     "У особых говорящих — Бога-Разработчика, Небесного отдела кадров, дракона — своя рама окна. То же правило для "
     "особых карточек: своя рама сразу говорит «это редкое»."),
    ("boons", "Выбор даров", ["crops/b_dary_stroki", "crops/c_dar_ikonka", "video/02_vybor_darov"],
     "Выбор — три широкие строки с рваным краем, как чернильное пятно. Слева иконка в квадратной рамке со скруглёнными "
     "углами, в углу рамки — завиток-знак бога, от которого дар. Редкий дар — строка другого цвета и слово «Epic» справа. "
     "Название крупно, под ним одна строка пояснения, под ней цифры.",
     "Карточка выбора может быть строкой — на телефоне у нас уже так. Знак источника в углу иконки. Редкость — цветом "
     "строки и коротким словом."),
    ("arcana", "Карты Арканы", ["crops/e_arkana_karty", "crops/f_arkana_bolshaya_karta", "crops/l_vspyshka_karty",
                                "crops/d_arkana_rannyaya_karty"],
     "Рисунок во всю карту, без пустого поля. Номер — римской цифрой в медальоне внизу, цена — в кружке в верхнем углу. "
     "Включённая карта цветная и в светящейся зелёной раме, выключенная — серая, одной краской. Когда карту включаешь, "
     "по соседним клеткам бежит белая вспышка. На последней картинке ранняя версия: карты пустые, с одной цифрой, и "
     "смотрятся бедно. К выпуску их дорисовали — у нас сейчас похожий шаг.",
     "Рисунок во всю карточку — это наш следующий шаг. Особая карточка — светящаяся рама и вспышка, когда её получаешь. "
     "Закрытая или недоступная карточка — серая, одной краской."),
    ("oaths", "Плитки клятв", ["crops/g_klyatvy_plitki", "video/11_klyatvy_plitki"],
     "Каждая клятва — плитка: цветная иконка, подпись и деления уровня под ней, «+1» в углу. Сетка 4×4 читается сразу, "
     "пустые плитки серые.",
     "Для «Личного дела» и титулов — плитки с иконкой и делениями вместо списка строк."),
    ("trial", "Рама с цепями", ["video/12_ispytanie_rama_s_tsepyami", "crops/n_ispytanie_zagolovok",
                                "crops/m_ispytanie_kartochki"],
     "Тяжёлая рама с самоцветами по углам. Заголовок — на табличке, подвешенной на цепях. Слева список в кристалле, "
     "у карточек выбора — круглое окошко под рисунок.",
     "Для экрана главы или итога жизни — заголовок на подвешенной табличке (вывеска на верёвках у нас уже есть). "
     "Круглое окошко под картинку на карточке."),
    ("shop", "Список в лавке", ["crops/h_lavka_stroki", "video/13_perekrestok_lavka"],
     "Строки с ячейкой-иконкой слева. Выбранная строка светлее и в зелёной рамке. Цена — в отдельной рамке под списком.",
     "Если появится лавка или длинный список — делать так."),
    ("bars", "Полоски и портрет в кольце", ["crops/j_poloski", "crops/k_portret_v_koltse"],
     "Здоровье и магия — тонкие капсулы, число «35/55» прямо внутри, значок слева в кружке. Места занимают мало. "
     "Портрет героини — в кольце из делений с числом «8/10».",
     "Наши четыре показателя можно сделать капсулами с числом внутри — это меньше, чем нынешняя вывеска. Аватар "
     "говорящего или героя — в кольце-счётчике."),
    ("path", "Выбор пути", ["video/15_vybor_puti"],
     "Развилка — две круглые «линзы», в каждой вид места, куда ведёт дорога.",
     "Для ленты пути и развилок между главами."),
]

TEMPLATE = r'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Образцы Hades II</title>
<style>
:root{--bg:#f4efe4;--card:#fffdf7;--ink:#2a2118;--mute:#6f6253;--line:#d9cdb8;--acc:#9a3b1e;--take:#2f6b3a;--takebg:#e6f0e2}
@media (prefers-color-scheme:dark){:root{--bg:#1b1713;--card:#25201a;--ink:#efe6d6;--mute:#a99c88;--line:#3a3229;--acc:#e08a5c;--take:#9bd0a2;--takebg:#1f2e22}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:28px 16px 80px}
h1{font:700 30px/1.15 Georgia,"Times New Roman",serif;margin:0 0 6px}
h2{font:700 23px/1.2 Georgia,serif;margin:40px 0 8px;padding-top:14px;border-top:2px solid var(--ink)}
section{scroll-margin-top:60px}
.lead{color:var(--mute);margin:0 0 14px;max-width:76ch}
a{color:var(--acc)}
nav{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 0;margin:14px 0 0;display:flex;gap:6px 16px;flex-wrap:wrap;font-size:14px}
nav a{text-decoration:none;white-space:nowrap}
.sum{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px 20px 10px 34px;margin:14px 0}
.sum li{margin:6px 0}
.shots{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px;margin:10px 0}
.shots img{width:100%;border-radius:6px;border:1px solid var(--line);cursor:zoom-in;background:#000;display:block}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.two>div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 16px}
.two>div.take{background:var(--takebg)}
.two b{display:block;margin-bottom:4px}.take b{color:var(--take)}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:20;cursor:zoom-out;padding:12px}
#lb img{max-width:100%;max-height:100%;border-radius:6px}
#lb.on{display:flex}
@media (max-width:760px){.two{grid-template-columns:1fr}h1{font-size:25px}}
</style></head><body><div class="wrap">
<h1>Образцы: интерфейс Hades II</h1>
<p class="lead">Рамки, иконки, карты и окна разговора из Hades II — что в них сильного и что можно взять к нам. Кадры — со страницы игры в Steam и из двух роликов там же, собраны 22 ноября 2026 года. Крупная надпись сверху на кадрах из роликов — заставка ролика, к игре она не относится. Нажми на картинку, чтобы увеличить.</p>
<p class="lead">Отдельных иконок файлами нет: вики игры не отдаёт картинки скриптам (там проверка от роботов), обходить её я не стал. Иконки видно на крупных планах.</p>
<nav>{{NAV}}</nav>
<section id="sum"><h2>Главное</h2><ul class="sum">{{SUM}}</ul></section>
{{SECTIONS}}
</div>
<div id="lb" onclick="this.classList.remove('on')"><img alt=""></div>
<script>
document.querySelectorAll('.shots img').forEach(function(i){i.addEventListener('click',function(){var b=document.getElementById('lb');b.querySelector('img').src=i.src;b.classList.add('on');});});
</script>
</body></html>'''


def img64(rel):
    im = Image.open(os.path.join(SRC, rel + ".jpg")).convert("RGB")
    im.thumbnail((1280, 1280))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    nav, secs = [], []
    for key, title, shots, strong, take in SECTIONS:
        nav.append(f'<a href="#{key}">{E(title)}</a>')
        imgs = "".join(f'<img src="{img64(s)}" alt="{E(title)}" loading="lazy">' for s in shots)
        secs.append(f'<section id="{key}"><h2>{E(title)}</h2><div class="shots">{imgs}</div>'
                    f'<div class="two"><div><b>Что тут сильного</b>{E(strong)}</div>'
                    f'<div class="take"><b>Что можно взять к нам</b>{E(take)}</div></div></section>')
    page = (TEMPLATE.replace("{{NAV}}", '<a href="#sum">Главное</a>' + "".join(nav))
            .replace("{{SUM}}", "".join(f"<li>{E(s)}</li>" for s in SUMMARY))
            .replace("{{SECTIONS}}", "\n".join(secs)))
    open(OUT, "w", encoding="utf-8").write(page)
    print("готово:", os.path.relpath(OUT), f"{os.path.getsize(OUT) / 1e6:.1f} МБ")


if __name__ == "__main__":
    main()
