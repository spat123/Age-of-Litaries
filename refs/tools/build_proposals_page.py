#!/usr/bin/env python3
"""Собирает refs/predlozheniya.html — страницу с предложениями на одобрение:
стиль, состав графики, сюжет, свои механики, список решений.
Промпты берёт из art_style.md, картинки — из refs/screens и assets_src/art.
Запуск из корня: python3 refs/tools/build_proposals_page.py"""
import base64, html, io, os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
SCREENS = os.path.join(HERE, "..", "screens")
ART = os.path.join(ROOT, "assets_src", "art")
OUT = os.path.join(HERE, "..", "predlozheniya.html")
E = html.escape

def img(path, width=560, alt="", cap=""):
    im = Image.open(path).convert("RGB")
    im.thumbnail((width, width))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=70, optimize=True)
    src = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    c = f"<figcaption>{E(cap)}</figcaption>" if cap else ""
    return f'<figure><img src="{src}" alt="{E(alt or cap)}">{c}</figure>'

def shot(key, n, cap):
    return img(os.path.join(SCREENS, key, f"{n:02d}.jpg"), cap=cap)

def own(rel, cap, width=560):
    return img(os.path.join(ART, rel), width=width, cap=cap)

def prompts():
    """Достаёт промпты из art_style.md: {заголовок: текст}."""
    s = open(os.path.join(ROOT, "art_style.md"), encoding="utf-8").read()
    res = {}
    for m in re.finditer(r"^\*\*([^*\n]+)\*\*[^\n]*\n(?:(?!\*\*|```)[^\n]*\n)*```\n(.*?)\n```", s, re.S | re.M):
        res[m.group(1).strip()] = m.group(2).strip()
    return res

def prompt_box(title, text, note=""):
    n = f'<span class="pn">{E(note)}</span>' if note else ""
    return f'<div class="prompt"><div class="ph"><b>{E(title)}</b>{n}<button type="button" class="copy">Скопировать</button></div><pre>{E(text)}</pre></div>'

def main():
    P = prompts()
    def p(prefix):
        for k, v in P.items():
            if k.startswith(prefix):
                return k, v
        raise KeyError(prefix)

    AUTH = os.path.join(HERE, "..", "author_refs")
    tried = "".join(img(os.path.join(AUTH, f), 420, cap=c) for f, c in [
        ("05_out_baby_watercolor.jpg", "младенец: придумка подошла"), ("06_out_booth_watercolor.jpg", "будка тролля: придумка подошла"),
        ("07_out_phone_watercolor.jpg", "смартфон: придумка подошла")])
    style = "".join(img(os.path.join(AUTH, f), 560, cap=c) for f, c in [
        ("08_style_desert_a.jpg", "образец рисовки"), ("09_style_desert_b.jpg", "образец рисовки"),
        ("10_style_cottage.jpg", "образец рисовки — это наш старый фон bg_act1_birth"), ("11_style_booth_on_desert.jpg", "будка на таком фоне смотрится своей")])
    one_pic = (shot("col_middle_ages", 4, "Choice of Life: две карточки, на каждой простая картинка")
               + shot("col_middle_ages", 5, "После выбора: оборот, только текст"))
    mom = shot("chinese_parents", 8, "Chinese Parents: мама сравнивает с чужими детьми")
    brante = shot("sir_brante", 4, "Sir Brante: детские качества складываются во взрослые")
    hr = shot("death_and_taxes", 1, "Death and Taxes: загробная контора")
    notes = {"6.1": "1:1", "6.2": "1:1", "6.3": "1:1 · новая карточка", "6.4": "16:9", "6.5": "16:9", "6.6": "16:9", "6.7": "16:9"}
    prompts_html = "".join(prompt_box(k, v, notes.get(k[:3], "")) for k, v in P.items() if re.match(r"6\.\d", k))

    page = TEMPLATE
    for k, v in {
        "TRIED": tried, "STYLE": style, "ONE_PIC": one_pic,
        "MOM": mom, "BRANTE": brante, "HR": hr, "PROMPTS": prompts_html,
    }.items():
        page = page.replace("{{" + k + "}}", v)
    open(OUT, "w", encoding="utf-8").write(page)
    print("готово:", os.path.relpath(OUT), f"{os.path.getsize(OUT)/1e6:.1f} МБ; промптов: {len(P)}")

TEMPLATE = r'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Сэр Баг — предложения</title>
<style>
:root{--bg:#f4efe4;--card:#fffdf7;--ink:#2a2118;--mute:#6f6253;--line:#d9cdb8;--acc:#9a3b1e;--take:#2f6b3a;--takebg:#e6f0e2;--skip:#8a3324;--skipbg:#f5e3dc;--code:#f0e9da;--rec:#b8860b}
@media (prefers-color-scheme:dark){:root{--bg:#1b1713;--card:#25201a;--ink:#efe6d6;--mute:#a99c88;--line:#3a3229;--acc:#e08a5c;--take:#9bd0a2;--takebg:#1f2e22;--skip:#e9a493;--skipbg:#33201b;--code:#1f1b16;--rec:#e0b84a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:28px 16px 90px}
h1{font:700 30px/1.15 Georgia,"Times New Roman",serif;margin:0 0 6px}
h2{font:700 24px/1.2 Georgia,serif;margin:52px 0 6px;padding-top:14px;border-top:2px solid var(--ink)}
h3{font:700 19px/1.25 Georgia,serif;margin:0 0 4px}
h4{font:700 15px/1.3 -apple-system,sans-serif;margin:14px 0 4px;color:var(--mute);text-transform:uppercase;letter-spacing:.04em}
p{margin:0 0 10px}
.lead{color:var(--mute);margin:0 0 18px;max-width:72ch}
a{color:var(--acc)}
nav{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 0;margin:14px 0 0;display:flex;gap:6px 16px;flex-wrap:wrap;font-size:14px}
nav a{text-decoration:none;white-space:nowrap}
.box{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0 0 16px}
.box.rec{border:2px solid var(--rec)}
.tag{display:inline-block;font-size:12px;font-weight:700;padding:2px 8px;border-radius:99px;background:var(--rec);color:#fff;margin-left:8px;vertical-align:middle}
.pics{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;margin:12px 0}
.pics.small{grid-template-columns:repeat(auto-fill,minmax(130px,1fr))}
.pics.two{grid-template-columns:repeat(2,1fr)}
figure{margin:0}
figure img{width:100%;display:block;border-radius:6px;border:1px solid var(--line);cursor:zoom-in;background:#000}
.pics:not(.small):not(.free) figure img{aspect-ratio:16/9;object-fit:cover}
figcaption{font-size:13px;color:var(--mute);margin-top:3px;line-height:1.3}
ul{margin:0 0 10px;padding-left:20px}
li{margin:4px 0}
.pm{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}
.pm div{padding:8px 12px;border-radius:8px;font-size:15px}
.plus{background:var(--takebg)} .plus b{color:var(--take)}
.minus{background:var(--skipbg)} .minus b{color:var(--skip)}
table{border-collapse:collapse;width:100%;margin:8px 0 12px;font-size:15px}
th,td{text-align:left;vertical-align:top;padding:7px 10px;border-bottom:1px solid var(--line)}
th{color:var(--mute);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:.03em}
.tw{overflow-x:auto}
.prompt{border:1px solid var(--line);border-radius:8px;margin:10px 0;overflow:hidden}
.ph{display:flex;align-items:center;gap:10px;padding:7px 10px;background:var(--code);font-size:14px}
.pn{color:var(--mute)}
.copy{margin-left:auto;font:inherit;font-size:13px;padding:4px 12px;border-radius:6px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.copy.ok{background:var(--takebg);color:var(--take)}
pre{margin:0;padding:10px 12px;white-space:pre-wrap;word-break:break-word;font:13px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;max-height:220px;overflow:auto;background:var(--card)}
details{margin:10px 0}
summary{cursor:pointer;font-weight:600;padding:6px 0}
.mech{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px}
.mech .box{margin:0}
.mech dl{margin:8px 0 0;display:grid;grid-template-columns:86px 1fr;gap:5px 10px;font-size:15px}
.mech dt{color:var(--mute);font-size:13px;padding-top:2px}
.mech dd{margin:0}
.big{font:400 20px/1.4 Georgia,serif;margin:0 0 12px;max-width:60ch}
.ask{counter-reset:q;list-style:none;padding:0;margin:0}
.ask li{counter-increment:q;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px 10px 52px;margin:0 0 8px;position:relative}
.ask li::before{content:"Р" counter(q);position:absolute;left:12px;top:10px;font:700 15px Georgia,serif;color:var(--acc)}
.ask small{display:block;color:var(--mute);font-size:14px}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.88);display:none;align-items:center;justify-content:center;z-index:20;cursor:zoom-out;padding:12px}
#lb img{max-width:100%;max-height:100%;border-radius:6px}
#lb.on{display:flex}
@media (max-width:760px){.pm{grid-template-columns:1fr}.pics.two{grid-template-columns:1fr}h1{font-size:25px}.mech{grid-template-columns:1fr}}
</style></head><body><div class="wrap">
<h1>Сэр Баг — стиль, сюжет, механики</h1>
<p class="lead">Обновлено после первой пробы картинок: акварель убрана, рисовка — чёткий контур и плотный цвет. Сэр Лаг стал карточкой-помощником. Полные тексты лежат в репозитории: <code>art_style.md</code>, <code>rework_plan.md</code>, <code>decisions.md</code>. Тексты сцен, код и старые картинки не менялись.</p>
<nav><a href="#style">1. Стиль</a><a href="#gfx">2. Состав графики</a><a href="#story">3. Сюжет</a><a href="#mech">4. Свои механики</a><a href="#scope">5. Объём</a><a href="#ask">6. Что принято</a></nav>

<section id="style"><h2>1. Стиль: чёткий контур и плотный цвет</h2>
<p class="lead">Первая проба показала: сами придумки подошли, а акварель нет. Ты прислал образцы рисовки — мультяшные фоны. Один из них оказался нашим собственным старым фоном, значит старые 40 фонов остаются как есть.</p>
<h4>Что вышло в первой пробе</h4>
<div class="pics free">{{TRIED}}</div>
<h4>Образцы рисовки</h4>
<div class="pics">{{STYLE}}</div>
<div class="box rec"><h3>Что именно берём с образцов</h3>
<div class="tw"><table>
<tr><th>Что</th><th>Как на образцах</th></tr>
<tr><td>Контур</td><td>Чистый, уверенный, средней толщины. Тёмный оттенок цвета самого предмета, не чёрный. Не набросок</td></tr>
<tr><td>Цвет</td><td>Плотный, ровный, насыщенный. Никаких разводов и просвечивающей бумаги</td></tr>
<tr><td>Тень</td><td>Два-три ровных тона на форму, край тени резкий</td></tr>
<tr><td>Фактура</td><td>Мелкое зерно внутри заливки. Трещины и потёртости — линией и пятнами</td></tr>
<tr><td>Формы</td><td>Округлые, крупные, упрощённые</td></tr>
<tr><td>Краски</td><td>Охра, соломенный, кирпичный, зелёный против чистого синего неба</td></tr>
</table></div>
<div class="pm"><div class="plus"><b>Остаётся из первой пробы:</b> младенец с вихром в зелёном одеяле, будка с бирюзовым кристаллом, смартфон с резной репой, жуком и бечёвкой. Правило «всё корпоративное светится бирюзовым» тоже остаётся: на пробе оно сработало.</div>
<div class="minus"><b>Убираем:</b> акварель, набросочную линию, бумажную фактуру. Из образцов не берём пустыню, планеты и технику — только рисовку.</div></div></div>

<div class="box"><h3>Промпты для второй пробы</h3>
<p class="lead">Семь промптов, по 4 картинки на каждый. К каждому приложи как опору стиля наш старый фон, например <code>bg_act1_birth.png</code> (References → Style). Новая здесь одна картинка — карточка Сэра Лага.</p>
{{PROMPTS}}
<h4>Как держать один стиль</h4>
<p class="lead">Составлено по справке Magnific. В самом интерфейсе я это не проверял.</p>
<ul>
<li><b>Опора стиля — наши же старые фоны.</b> Подходят <code>bg_act1_birth.png</code>, <code>bg_act1_fair.png</code>, <code>bg_act2_lawyer.png</code>.</li>
<li><b>Свой стиль.</b> Style → New Style, загрузить 15–20 лучших старых фонов. Тогда опору не надо прикладывать руками.</li>
<li><b>Одна модель на всю игру.</b> Промпт 6.1 сделай на двух-трёх моделях (Google Nano Banana Pro, GPT 2, Seedream 5 PRO), выбери ту, что ближе к образцам, и больше не меняй.</li>
<li><b>Персонаж.</b> Лист героя сначала как опорное изображение, после утверждения — Character → New character со своей меткой на каждый возраст.</li>
<li><b>Приёмка.</b> Шесть вопросов к каждой картинке: контур чистый; цвет плотный, без разводов; тени резкие; герой узнаётся; нет букв и знаков; читается в размере 300 пикселей. Хоть одно «нет» — перегенерировать.</li>
</ul>
<p><b>Что перерисовать в старых фонах:</b> <code>bg_act1_phone_curse.png</code> (чужой логотип) и <code>bg_act0_void.png</code> (пиксели). Остальные подходят.</p></div>
</section>

<section id="gfx"><h2>2. Состав графики</h2>
<p class="lead">Главная находка разбора: в серии Choice of Life у выбора одна простая картинка, а на обороте только текст. У нас по правилу «лицо и рубашка» каждому выбору нужны две полные сцены.</p>
<div class="pics two">{{ONE_PIC}}</div>
<div class="box"><div class="tw"><table>
<tr><th>Что</th><th>Сколько</th><th>Правило</th></tr>
<tr><td>Фон места, 16:9</td><td>один на место, есть 40</td><td>Середина спокойная: поверх лягут свиток и карточки</td></tr>
<tr><td>Карточка-предмет, 1:1</td><td>основная масса</td><td>Один предмет на ровном фоне</td></tr>
<tr><td>Карточка-жест, 1:1</td><td>около 30 на всю игру</td><td>Рука с монетой, рот, ноги, кулак. Рисуется один раз, служит во многих сценах</td></tr>
<tr><td>Карточка-сценка, 1:1</td><td>только для главных выборов</td><td>Одна-две фигуры, фон почти пустой</td></tr>
<tr><td>Оборот карточки</td><td>ноль картинок</td><td>Текст Рассказчика и значки изменений</td></tr>
<tr><td>Портрет говорящего</td><td>10–12</td><td>Лицо и плечи в кружке у свитка</td></tr>
<tr><td>Герой</td><td>3 возраста</td><td>Портрет на экране меняется с возрастом и титулом</td></tr>
</table></div>
<p><b>Итог:</b> вместо примерно 670 полных сцен — 150–200 простых картинок, из них около 30 повторяемых.</p></div>
</section>

<section id="story"><h2>3. Сюжет: что меняем</h2>
<p class="lead">Мир, тон, Рассказчик, лучшие сцены и финал с кофейней остаются. Меняется каркас: у героя появляется желание, у жизни — главы, у решений — последствия.</p>
<div class="box"><h4>Игра в одной фразе</h4>
<p class="big">Ты рождаешься крестьянином в средневековье, которое устроено как IT-корпорация, и всю жизнь пытаешься доказать маме, что ты не хуже Сына Маминой Подруги. Умер — Небесная HR листает твоё личное дело и отправляет жить заново.</p>
<div class="pm"><div class="plus"><b>Герой хочет:</b> услышать от мамы «молодец». Для этого надо обогнать соперника.</div>
<div class="minus"><b>Герою нужно:</b> перестать с ним меряться. Настоящая концовка — та, где он выходит из гонки.</div></div>
<h4>Что связывает маму, корпорацию и дракона</h4>
<p><b>Гонка за «успешным успехом» делает из людей драконов.</b></p>
<ul>
<li>Сын Маминой Подруги обгоняет героя не потому, что лучше. Его мама оплатила ему подписку «Жизнь+ Премиум» ещё до рождения. У героя бесплатная пробная версия с багами.</li>
<li>Дракон — это Сын Маминой Подруги прошлого поколения. Выиграл гонку, получил всё, выгорел и лёг на золото.</li>
<li>Убить дракона и занять его место — значит стать следующим драконом. В следующей жизни в пещере может сидеть твой прошлый герой.</li>
</ul></div>

<div class="box"><h3>Одна жизнь — шесть глав</h3>
<p>Каждая глава: опорная сцена (есть всегда) → две-три случайные сцены из колоды возраста → «Мамина подруга зашла в гости» (итог и сравнение).</p>
<div class="tw"><table>
<tr><th>Глава</th><th>Опорные сцены — из уже написанных</th><th>Цель на экране</th></tr>
<tr><td>0. Сборка</td><td>Бог-Разработчик. Подробно только в первой жизни</td><td>—</td></tr>
<tr><td>1. Младенец</td><td>Рождение, первое слово</td><td>Заговори раньше, чем Сын Маминой Подруги</td></tr>
<tr><td>2. Детство</td><td>Песочница, ярмарка</td><td>Заработай первую монету</td></tr>
<tr><td>3. Отрочество</td><td>Школа-буткемп, мельница 5G</td><td>Получи диплом или славу</td></tr>
<tr><td>4. Совершеннолетие</td><td>Военкомат, две встречи на Тракте</td><td>Доберись до столицы</td></tr>
<tr><td>5. Карьера</td><td>Таможня, гильдия, HR-инквизиция</td><td>Займи должность выше, чем у него</td></tr>
<tr><td>6. Задача «Дракон»</td><td>Король, бал, дракон</td><td>Закрой задачу — или откажись</td></tr>
</table></div></div>

<div class="box"><h3>Решения детства возвращаются</h3>
<div class="tw"><table>
<tr><th>Решение в детстве</th><th>Что возвращается</th></tr>
<tr><td>Ударил брата палкой в песочнице</td><td>В 18 лет брат — писарь у Военкома. Взятка вдвое дороже</td></tr>
<tr><td>Терпел роль дракона</td><td>Брат заступается на площади</td></tr>
<tr><td>Отобрал лопатки</td><td>Один из тех детей проводит собеседование в гильдии</td></tr>
<tr><td>Привязал лопату к свинье</td><td>Гильдия Магов берёт без экзамена, но HR-инквизиция уже следит</td></tr>
<tr><td>Купил Battle Pass вместо репы</td><td>Отец не даёт денег на дорогу</td></tr>
<tr><td>Украл шапочку на ярмарке</td><td>Купец с ярмарки и Инфоцыганъ на Тракте — один человек. Он тебя узнаёт</td></tr>
</table></div>
<p>Купец и брат становятся постоянными персонажами: история связнее, рисовать меньше лиц. Всего постоянных десять: мама, отец, брат, Сын Маминой Подруги, Мамина подруга, Бог-Разработчик, купец, король, дракон, гоблин.</p></div>

<div class="box"><h3>Юмор: пять источников вместо одного</h3>
<p>Правило: в сцене не больше одной шутки «старина плюс айтишное слово». Остальное берём отсюда:</p>
<ul>
<li><b>Мама.</b> «А вот сын маминой подруги», «шапку надень».</li>
<li><b>Рассказчик.</b> Спорит с игроком, обижается, оправдывается перед Богом-Разработчиком.</li>
<li><b>Контора на том свете.</b> Справки, очереди, собеседование по итогам жизни.</li>
<li><b>Шутки, которые возвращаются.</b> Свинья, брат, купец: чем позже аукнулось, тем смешнее.</li>
<li><b>Рисунок.</b> Айтишная вещь нарисована всерьёз и светится холодным голубым.</li>
</ul></div>
</section>

<section id="mech"><h2>4. Свои механики</h2>
<p class="lead">Уникальные карточки, о которых ты спросил, в плане были, но растворились в «подписках». Теперь это отдельная и главная механика М0. К ней четыре новые и одна в запасе. Основа остаётся как в Choice of Life: фон, свиток, карточки, переворот.</p>
<div class="box rec"><h3>М0. «Уникальные карточки» <span class="tag">остаётся главной</span></h3>
<p>В некоторых сценах можно получить особую карточку: вещь (деревянный смартфон, шапочка из фольги, ржавый меч), бумагу (Иск к Реальности, Берестяной Battle Pass) или навязчивую мысль («Птицы — дроны Короля»). Карточка остаётся у тебя и может сработать через много сцен: в нужном месте появляется скрытый вариант выбора.</p>
<div class="tw"><table>
<tr><th>Что добавляем</th><th>Зачем</th></tr>
<tr><td>Карточки лежат «в руке» внизу экрана</td><td>Видно, что у тебя есть и чего ждать</td></tr>
<tr><td>Три срока: разовая, постоянная, подписка</td><td>Разовая сгорает, когда сработала. Подписка — самая сильная вещь с платой (М3)</td></tr>
<tr><td>Часть карточек открывается только записями в личном деле и прошлыми жизнями</td><td>Есть за чем возвращаться</td></tr>
<tr><td>Редкую карточку можно унести в следующую жизнь через Небесную HR</td><td>Это нынешние «реликвии»</td></tr>
<tr><td><b>Помощники.</b> Кому помог по сюжету, тот остаётся карточкой. Её можно сыграть в любой сцене: помощник решает дело и уходит в сброс</td><td>Твоя идея с рыцарем. Сэр Лаг уже работает так во всех сценах Тракта и может спасти от смерти</td></tr>
</table></div>
<p><b>Цена:</b> скрытые варианты по вещам уже работают в прототипе. Нужно показать руку карточек и завести три срока.</p></div>
<div class="mech">
<div class="box"><h3>М1. «Мамина подруга зашла в гости»</h3>
<p>В конце каждого возраста — сравнение: слева ты, справа Сын Маминой Подруги. Мама выносит приговор: «Позор семьи», «Ну, сойдёт» или «Молодец».</p>
<dl><dt>Даёт</dt><dd>Приговор становится настроением на следующий возраст: «Мамин вздох» или «Мамина гордость». Планка соперника зависит от прошлых жизней.</dd>
<dt>Лечит</dt><dd>У героя нет желания, у жизни нет ритма.</dd>
<dt>Цена</dt><dd>Один экран, пять коротких текстов на возраст, три портрета.</dd></dl>
<div class="pics two" style="grid-template-columns:1fr">{{MOM}}</div></div>

<div class="box"><h3>М2. «Личное дело»</h3>
<p>Важные решения ставят запись со штампом в книгу. Запись открывает и закрывает варианты во взрослой жизни. Три записи одного рода дают титул на гербе. После смерти Небесная HR зачитывает дело как собеседование и по нему решает, кем ты родишься.</p>
<dl><dt>Лечит</dt><dd>Детство из отдельных скетчей; выбор вслепую.</dd>
<dt>Цена</dt><dd>Метка на выборе, экран книги, 10–12 возвратов на первую часть.</dd></dl>
<div class="pics two" style="grid-template-columns:1fr">{{BRANTE}}</div></div>

<div class="box"><h3>М3. «Подписки»</h3>
<p>Самые сильные уникальные карточки не покупаются, а оформляются как подписка. Несколько сцен бесплатно и с пользой, потом каждую сцену списывается золото или менталка. Отписаться можно только через сцену-лабиринт «Вы уверены? Нам будет вас не хватать».</p>
<dl><dt>На экране</dt><dd>Ряд значков: «ещё 2 сцены бесплатно», «−1 за сцену».</dd>
<dt>Лечит</dt><dd>Смартфон и шапочка из фольги дают лучший исход почти везде. Теперь у них есть цена. Остальные карточки остаются бесплатными.</dd>
<dt>Сюжет</dt><dd>Вся жизнь героя — пробная подписка «Жизнь+», у соперника — премиум.</dd>
<dt>Цена</dt><dd>Список активных эффектов и списание раз в сцену.</dd></dl></div>

<div class="box"><h3>М4. «Список исправлений между жизнями»</h3>
<p>Мир в раннем доступе. После смерти Бог-Разработчик его чинит: решения, которыми ты пользовался чаще всего, ослаблены или заменены, в колоды добавлены новые сцены. Перед новой жизнью — три строки «Что нового в версии 0.9c».</p>
<dl><dt>Пример</dt><dd>«Шапочка из фольги больше не отражает налоги. Тролль принимает оплату только лайками. Добавлена свинья».</dd>
<dt>Лечит</dt><dd>Сцены в одном порядке; одна вещь на все случаи.</dd>
<dt>Цена</dt><dd>Счётчик решений, по запасному варианту на 8–10 главных сцен, экран списка.</dd></dl>
<div class="pics two" style="grid-template-columns:1fr">{{HR}}</div></div>
</div>
<div class="box" style="margin-top:16px"><h3>В запасе: М5. «Рассказчик с настроением»</h3>
<p>Подсказки «что заденет выбор» — это слова Рассказчика. Пока он в духе, подсказки точные. Довёл его глупостями — он уходит на перекур, ведёт гоблин-стажёр, и подсказки путаются. Добавляем после того, как заработают обычные подсказки.</p></div>
<div class="box"><h3>Показатели</h3>
<p><b>Тело · Менталка · Золото · Репутация</b> — все четыре видны. Перед выбором видно, какие он заденет, но не видно, насколько. Корона, Инквизиция и Народ сливаются в Репутацию. Репутация губит и на нуле, и на максимуме: «слишком хорош — повышен и сослан в Северные Пустоши».</p></div>
</section>

<section id="scope"><h2>5. Объём: что откладываем и что делаем первым</h2>
<div class="pm">
<div class="minus"><b>Откладываем,</b> пока ядро не заработало: бой, крафт, Микро-Гвинт и остальные мини-игры, доску миссий, три фракции, шкалу дедлайна, мутаторы, свободную ходьбу по карте. Карта остаётся лентой пути.</div>
<div class="plus"><b>Делаем первым</b> срез «Жизнь до столицы»: главы 0–4, от рождения до ворот Биг Даты. Дальше не идём, пока он не станет игрой.</div>
</div>
<div class="box"><h3>Срез готов, когда</h3>
<ul>
<li>одна жизнь проходится за 10–15 минут;</li>
<li>вторая жизнь заметно другая: другие сцены, сработал список исправлений, сработала запись из личного дела;</li>
<li>четыре показателя видны, подсказки работают;</li>
<li>смерть ведёт в Небесную HR и в новую жизнь;</li>
<li>уникальная карточка получена в одной главе и сработала в другой;</li>
<li>каждая из четырёх новых механик сработала хотя бы раз;</li>
<li>все картинки в одном стиле.</li>
</ul>
<p><b>Проверка «это уже игра»:</b> посторонний человек проходит две жизни подряд без объяснений и сам запускает третью.</p></div>
</section>

<section id="ask"><h2>6. Что принято и что осталось</h2>
<div class="pm">
<div class="plus"><b>Принято с твоих слов.</b> Рисовка: чёткий контур и плотный цвет, без акварели. Придумки первой пробы. Уникальные карточки и помощники вроде Сэра Лага. Тексты простым языком. Одна картинка на выбор, четыре показателя, шесть глав, механики М1–М4, поворот с драконом, первая часть до ворот столицы.</div>
<div class="minus"><b>Осталось.</b> Вторая проба картинок. Какая модель Magnific станет единственной. Прочитать переписанные тексты первой части. Движок: Godot или веб.</div>
</div>
</section>
</div>
<div id="lb"><img alt=""></div>
<script>
const lb=document.getElementById('lb'),li=lb.querySelector('img');
document.addEventListener('click',e=>{const t=e.target;
 if(t.matches('figure img')){li.src=t.src;lb.classList.add('on');return}
 if(lb.classList.contains('on')){lb.classList.remove('on');return}
 if(t.matches('.copy')){const txt=t.closest('.prompt').querySelector('pre').textContent;
  const done=()=>{t.textContent='Скопировано';t.classList.add('ok');setTimeout(()=>{t.textContent='Скопировать';t.classList.remove('ok')},1500)};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(done,()=>fallback(txt,done))}else{fallback(txt,done)}}});
function fallback(txt,done){const a=document.createElement('textarea');a.value=txt;document.body.appendChild(a);a.select();try{document.execCommand('copy');done()}catch(e){}a.remove()}
document.addEventListener('keydown',e=>{if(e.key==='Escape')lb.classList.remove('on')});
</script>
</body></html>'''

if __name__ == "__main__":
    main()
