# Вид интерфейса — Сэр Баг

> **Статус: выбран вид «Сцена и полка» (вариант Б), он собран в игре кодом.** Автор: «вариант б… В целом ок — но это всё равно набросок — нужно будет генерить нормально».
> Что принято — раздел 0 и П21, П22 в [`decisions.md`](./decisions.md). Запросы на рисованные вещи — раздел 8.
> Разделы 1–7 ниже — прежнее предложение (первый вид, отклонён). Из них в силе только общая мысль «каждая деталь — вещь из мира» и два вида «мир» и «система».
> Рисовка — в [`art_style.md`](./art_style.md).

---

## 0. Пересмотр: образцы и новые правила (14 ноября 2026)

Страница со скриншотами и разбором: `refs/ui_refs.html`. Собирается так:

```bash
python3 -I refs/tools/fetch_ui_screens.py        # скриншоты 47 игр в refs/screens/ui/
python3 -I refs/tools/build_ui_refs_page.py      # страница
```

### 0.1. Чем первый вид слабее образцов

1. Всё одного цвета и одной толщины: свиток, карточки и бирки — одинаковые кремовые прямоугольники с тонкой линией. Не видно, что главное.
2. Линия тоньше, чем в рисунках. Интерфейс смотрится как наклейка из другой игры.
3. Яркий фон на весь экран спорит со светлыми листами.
4. Карточки стоят по центру и закрывают героев сцены.
5. Карточки пустые: поле и смайлик.
6. Буквы мелкие и тонкие.
7. Показатели — четыре маленькие дощечки в углу.
8. Вещи висят в воздухе, ни к чему не прикреплены.

### 0.2. Главные образцы

| Игра | Что в ней сильного | Что берём |
|------|--------------------|-----------|
| Legends of Kingdom Rush | Событие — раскрытая книга: слева рисунок, справа текст, карточки выбора на нижнем крае, фон затемнён, по бокам показатели и запас | Схему целиком. Вещи рисуем свои |
| The Plucky Squire | Плоский цвет, жирный контур, крупные буквы на странице рядом с рисунком | Крупный заголовок сцены на странице |
| Monster Prom | Рисунок события в рамке, каждая плашка — бумажка | Рамку для рисунка сцены |
| Wildfrost, Floppy Knights, Dicey Dungeons | Карта — вещь: толстая рамка, значки на углах, цвет по виду, полка внизу | Вид карточки |
| Shop Titans | Толстая кнопка с бортом, цена в кружке на углу | Борт у кнопок, цену на углу |
| Lil' Guardsman | Итог показывает аппарат: тёмный экран, бирюзовый ровный шрифт, фото со штампом | Вид «системы» и штампы на делах |
| Storyteller | Оглавление с галочками, страница со штампами | Страницу «Личное дело» |
| Rogue Legacy 2 | Выбор наследника: лист с печатью | Экран наследника |

Остальные — на странице. Чужой вид один в один не берём: приём тот же, вещи свои.

### 0.3. Десять правил нового вида

1. **Три слоя.** Фон приглушён. На нём одна большая светлая вещь с текстом. Самое яркое — то, что можно нажать.
2. **Контур как в рисунках:** 7–8 точек у больших вещей, 5–6 у мелких, тёмно-коричневый `#2a1a10`.
3. **У вещи есть толщина:** нижний борт темнее, под вещью жёсткая тень без размытия. Кнопка при наведении приподнимается, при нажатии вдавливается.
4. **Жирный рисованный шрифт** для всего, что нажимается и считается. Предложение: Balsamiq Sans Bold (есть кириллица, пакет уже стоит в `web/`). Alice остаётся для текста рассказа. Подписи на карточках не мельче 30.
5. **Карточка — вещь:** рисунок в цветном окне, жирная подпись, цифра клавиши в кружке, значки «что заденет» в капсуле на верхнем крае. Цвет окна по виду выбора: обычный, особый, помощник. Выбранная карточка приподнята и светится.
6. **Показатели в одном месте.** Слева «пропуск» героя на шнурке: значок в кружке, крупное число, полоска из десяти делений. Справа доска с особыми карточками и кнопка «Личное дело».
7. **Ничего не висит в воздухе:** пропуск на шнурке, доска прибита, цель главы — записка на кнопке.
8. **Система выглядит иначе.** Когда говорит Бог-Разработчик, гоблин или Небесная HR, тёплая книга сменяется холодным прибором: тёмный экран, бирюзовый ровный шрифт.
9. **Итоги — отдельный лист** со штампом или печатью поверх затемнённого экрана и одна кнопка: приговор мамы, смерть, наследник.
10. **Рисунки, а не смайлики.** Пока рисунков нет, ставим простые значки в нашем контуре.

### 0.4. Два наброска экрана

Исходник — [`refs/tools/ui_mock.html`](./refs/tools/ui_mock.html) (`?v=a` и `?v=b`). Картинки снимает `node web/tools/shot.mjs`.

| | А. Книга дела — [`refs/ui_mock/a.jpg`](./refs/ui_mock/a.jpg) | Б. Сцена и полка — [`refs/ui_mock/b.jpg`](./refs/ui_mock/b.jpg) |
|---|---|---|
| Устройство | Раскрытая книга по центру: слева рисунок сцены, справа заголовок и текст. Карточки лежат на нижнем крае книги. Фон затемнён и размыт | Фон яркий, на весь экран. Лист с текстом сверху, карточки стоят на деревянной полке снизу |
| Плюсы | Героев сцены ничто не закрывает. Длинный текст помещается. Книга — это личное дело героя, попадает в сюжет. Смена книги на прибор сразу показывает «систему» | Фон виден целиком. Меньше переделок |
| Минусы | Фон показан в окне и обрезается по краям; новые фоны лучше рисовать ближе к квадрату | Карточки закрывают героев. При шести–девяти карточках сцены не видно. Светлый лист на пёстром фоне читается хуже |

**Автор выбрал вариант Б** и добавил две поправки:

- Текст рассказчика можно уменьшить. Сделано: 27 точек вместо 33, лист стал ниже.
- Итог заранее не показываем. Значки «что заденет выбор» на карточках видны, только когда герой получил определённые бонусы. Сделано: значки показывает карточка с полем `hint` в `story/cards.json`. Сейчас это «Деревянный смартфон» и мысль «Всё ненастоящее» — это моё предложение (Р26). Цена выбора в монетах видна всегда.

Было, для сравнения: [`refs/ui_mock/now_1.jpg`](./refs/ui_mock/now_1.jpg).

### 0.5. Что сделано и что дальше

Сделано: экран в `web/src/GameScene.ts` и `web/src/ui.ts` собран по варианту Б. Слева пропуск с показателями и записка с целью главы, справа доска с особыми карточками и «Личное дело», сверху лист с текстом, снизу полка с карточками выбора. Вещи нарисованы кодом, на карточках пока временные значки.

Дальше:

1. Автор рисует вещи по запросам из раздела 8.
2. Я вырезаю фон, нарезаю и подключаю рисованные вещи вместо кодовых. Подключение ещё не написано: нужно увидеть края первых картинок.

---

## 1. Главная мысль

**В интерфейсе нет «окон» и «кнопок». Каждая деталь — вещь из мира игры**, нарисованная в той же рисовке, что и всё остальное: чёткий контур, плотный цвет, резкая тень.

Откуда это: три первых макета автор назвал «просто UI для браузерной игры». Вывод был такой — вид должен держаться на рисунке. Значит, и интерфейс рисуем как вещи: бересту, дощечки, карточки, книгу.

## 2. Что чем становится

| Деталь | Вещь | Сейчас в игре | Картинка на замену |
|--------|------|---------------|--------------------|
| Текст сцены | Берестяной свиток со свёрнутыми краями | нарисован кодом | `ui_scroll.png` |
| Имя говорящего | Дощечка, прибитая к свитку | кодом | часть `ui_button.png` |
| Выбор | Карточка из плотной бумаги: полоса с подписью, окошко с картинкой, внизу значки | кодом | `ui_card.png` |
| Исход | Лист бумаги: карточка переворачивается и становится им | кодом | `ui_sheet.png` |
| Показатели | Четыре деревянные бирки | кодом, значки старые | `ui_tag.png`, `icons_stats.png` |
| Кнопки | Тёмная дощечка | кодом | `ui_button.png` |
| Рука | Маленькие карточки внизу слева | кодом | та же `ui_card.png`, мельче |
| Личное дело | Толстая книга дьячка | кнопка-дощечка | `ui_book.png` |
| Приговор мамы | Штамп поперёк листа: «Молодец», «Ну, сойдёт», «Позор семьи» | кодом | `stamps.png` |
| Глава и цель | Лента-закладка сверху | кодом | позже |
| Подсказка к карточке | Листок бумаги над ней | кодом | `ui_sheet.png` |

## 3. Два вида: мир и система

Главное правило рисовки — «тёплый мир, холодная система» — работает и в интерфейсе.

- **Мир** говорит берестой, деревом и бумагой. Шрифт книжный.
- **Система** говорит холодной светящейся табличкой: тёмно-синее стекло, бирюзовая кайма, ровный «казённый» шрифт. Так показаны Бог-Разработчик, гоблин с кредитом, гонец с повышением, Небесная HR и список исправлений.

Подписки в руке помечены бирюзовым кружком: цифра — сколько сцен ещё бесплатно, восклицательный знак — уже берёт плату.

## 4. Что видно на карточке выбора

- Сверху подпись: что сделать.
- В середине картинка: один предмет или жест.
- Внизу значки показателей, которые выбор заденет. Без слов и без направления. Если выбор стоит денег — монета и цена.
- Особый выбор (по карточке или записи в деле) — синяя кайма и звезда в углу.
- Помощник — зелёная кайма и свой значок в углу.
- Закрытый выбор — бледный, внизу написано почему.

## 5. Шрифты

Все четыре свободные, с кириллицей, лежат в игре.

| Где | Шрифт | Почему |
|-----|-------|--------|
| Подписи карточек, бирки, кнопки | Neucha | Рисованный от руки, подходит к рисовке |
| Текст сцен и исходов | Alice | Книжный, спокойный, хорошо читается |
| Штампы приговора | Ruslan Display | Вязь: один сильный акцент на экране |
| Всё «системное» | PT Mono | Ровный и казённый, спорит с рукописным миром |

## 6. Расположение на экране

Экран 16:9, по образцу серии Choice of Life.

- Сверху по центру — свиток с текстом.
- По центру — карточки выбора. До пяти в ряд, больше — в два ряда.
- Слева сверху — бирки показателей, два на два.
- Справа сверху — личное дело и титул.
- По самому верху — ленты: слева жизнь и глава, справа цель.
- Внизу слева — рука.

Длинные списки (личное дело, чтение дела в Небесной HR, список исправлений) открываются отдельным листом поверх игры.

## 7. Как заменим кодовые детали картинками

1. Автор генерирует деталь по промпту из раздела 8.
2. Картинку кладём в `web/assets/ui/` с именем из таблицы.
3. Я подключаю её вместо кодовой: для растягиваемых деталей (свиток, лист, табличка) размечаю края, чтобы углы не тянулись. Это небольшая правка на каждую деталь, и делается она после первой готовой картинки.

Порядок по пользе: значки показателей → карточка → свиток → бирка и кнопка → книга → остальное.

## 8. Запросы на рисованные вещи интерфейса

Автор: «это всё равно набросок — нужно будет генерить нормально». **22.11.2026 все двенадцать вещей нарисованы через Codex по этим запросам и стоят в игре** (исходники — `assets_src/ui_new/`, подготовка — `python3 web/tools/cut_ui.py`). Чтобы перерисовать вещь: `python3 web/tools/codex_image.py --out assets_src/ui_new/<имя>.png --ref refs/ui_ref/style_1_izba.png --ref refs/ui_ref/shape_<номер>_….jpg "запрос"`, потом `cut_ui.py`. Ниже запросы на те же вещи в нашей рисовке. Прежние запросы (берестяной свиток, бирки) удалены вместе с отклонённым видом.

**Где взять опоры.** Автор спросил: «а где мне взять референсы под UI». Они лежат в папке [`refs/ui_ref/`](./refs/ui_ref/README.md): `style_*.png` — три наших фона, с них берётся рисовка (в запросах это `@img1`); `shape_*.jpg` — мои наброски каждой вещи на белом фоне, с них берётся форма, номер совпадает с номером запроса ниже. Папку собирает `sh refs/tools/make_ui_refs.sh`.

**Как рисовать, чтобы вещь можно было вставить в игру:**

- Одна картинка — одна вещь (или несколько вещей с зазором, если так сказано).
- Вид строго спереди, без наклона, вещь по центру, вокруг белое поле. Белый фон я вырежу сам.
- На вещи нет букв и цифр: надписи ставит игра.
- Середина вещи пустая и ровная: туда встанут текст и рисунки, а лист и прибор игра растягивает под длину текста.
- Рисовку бери с опоры: приложи первой картинкой наш фон из `refs/ui_ref/` (`style_*.png`). В запросах он уже назван `@img1`, вписывать ничего не нужно. Запросы с кнопкой «Скопировать» и с вариантом на две опоры (рисовка и форма) — страница `refs/veshchi.html`, её собирает `python3 refs/tools/build_ui_page.py` из этого раздела.
- Размер — не меньше 2000 точек по длинной стороне.

Начать лучше с И2 (карточка), И1 (лист) и И12 (значки): они видны на каждом экране. Картинки называй как удобно и присылай сюда — я вырежу фон, нарежу и подключу.

**И1. Лист с текстом** · 21:9 или 16:9 · в игре будет `ui_sheet.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: a wide horizontal sheet of thick cream paper with slightly rounded corners and slightly uneven hand-cut edges. Thick dark brown outline. A darker cream strip along the bottom edge shows the thickness of the paper. The whole surface is empty flat cream with only a very faint paper grain.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И2. Карточка выбора** · 3:4 · в игре будет `ui_card.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: a blank playing card in portrait format made of thick cream paper, rounded corners, thick dark brown outline, a darker cream strip along the bottom edge. The upper half of the card is an empty rectangular window with rounded corners and its own dark brown outline, filled with flat warm yellow. The lower part is empty cream paper for a caption.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И3. Полка** · 21:9 · в игре будет `ui_shelf.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: a long wooden shelf plank seen straight from the front, running across the whole width of the image so that its left and right ends are cut off by the image borders. Warm brown wood, a lighter strip along the top edge, a darker strip below, a few simple grain lines and two knots, a thick dark brown line along the top edge.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И4. Пропуск героя** · 9:16 · в игре будет `ui_badge.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: a tall employee pass badge made of thick cream parchment: a tall rounded rectangle hanging on two short red cloth straps with a small grey metal clip at the top. Thick dark brown outline, a darker strip along the bottom edge, tiny hand stitches along the border. Medieval hand-made look. The surface is completely empty.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И5. Доска для карточек** · 9:16 · в игре будет `ui_board.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: a tall wooden notice board made of three vertical planks with rounded corners, held by two dark iron nails near the top corners. Warm brown wood with a few grain lines, thick dark brown outline, a darker strip along the bottom edge. The surface is empty.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И6. Кнопки** · 16:9 · в игре будет `ui_buttons.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: two chunky rounded rectangular buttons, one above the other with a clear gap between them. The upper one is warm brown wood, the lower one is wood painted fresh green. Each has a thick dark brown outline and a clearly darker strip along its bottom edge, so it looks thick and pressable. Both surfaces are empty.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И7. Дощечка имени и лента** · 16:9 · в игре будет `ui_plate_ribbon.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: two separate objects, one above the other with a clear gap: a small dark brown wooden name plate with rounded corners, and a red cloth ribbon banner with V-shaped notches cut into both ends. Thick dark brown outlines, darker strips along the bottom edges. Both are empty.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И8. Записка с целью** · 1:1 · в игре будет `ui_note.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: a square pale yellow paper note pinned with a round red pin at the top centre. Thick dark brown outline, one bottom corner slightly curled. The note is empty.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И9. Прибор «системы»** · 21:9 или 16:9 · в игре будет `ui_system.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: a wide cold-looking magical device, like a medieval computer terminal: a dark slate-blue metal frame with rounded corners and a few rivets around one large dark navy screen that takes up almost the whole area. A thin glowing turquoise line runs around the screen. Thick dark outline. The screen is completely empty.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И10. Лист исхода** · 4:3 · в игре будет `ui_result.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: a landscape sheet of thick cream paper with slightly torn uneven edges and a red wax seal with a smooth empty face in the top right corner. Thick dark brown outline, a darker cream strip along the bottom edge. The sheet is empty.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И11. Штампы** · 16:9 · в игре будет `ui_stamps.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: three empty rubber-stamp imprints in a row with clear gaps: rectangular frames with a double border and a rough, worn ink texture with small gaps. The first is dark green, the second is brown, the third is dark red. Nothing inside the frames.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

**И12. Значки показателей** · 1:1 · в игре будет `ui_icons.png`

```
Use @img1 only as a style reference. Copy only its drawing style: clean thick outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a game interface element: four simple icons in a two-by-two grid with wide gaps between them: a red heart; a pink brain; a sheaf of wheat crossed with a wooden pitchfork; a stack of gold coins. Thick dark brown outlines, flat colours, one hard shadow tone on each.

Straight front view, flat, no perspective, no tilt, perfectly centred, the whole object visible with a white margin around it. Plain pure white background, no shadow on the background. The surface is blank: no text, no letters, no numbers, no symbols, no logos.
```

Окно карточки я перекрашу сам: жёлтое — обычный выбор, голубое — особый, зелёное — помощник. Надписи на штампах («Молодец», «Ну, сойдёт», «Позор семьи») тоже ставит игра.

Рисунки на самих карточках выбора — отдельная пачка: список в конце `story/BOOK.md`, шаблон запроса в `art_style.md` §6.

## 9. Что ещё не решено

- Заставка и главное меню.
- Портреты говорящих: кружок у свитка или фигура в сцене.
- Движение: сейчас карточки выезжают и переворачиваются, показатели подпрыгивают. Остальное — позже.
- Звук.
- Вид на телефоне: сейчас экран просто уменьшается целиком.
