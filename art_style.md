# Стиль графики — Сэр Баг

> **Статус: рисовка выбрана автором 14 ноября 2026 года, уточнена после первой пробы.** Чёткий контур и плотный цвет, как в мультфильме. Акварели нет.
> Что принято, а что ещё открыто — в [`decisions.md`](./decisions.md). Разбор игр-образцов — в [`references.md`](./references.md).

---

## 1. Что выбрал автор

Примеры автора лежат в `refs/author_refs/` (в git не идут).

**Первый заход.** Четыре предмета: холодильник, машина, ковёр, телефонная будка. Слова автора: «ближе конечно именно стиль рисовки будки — не цвет, а именно стиль рисовки».

**Первая проба.** По будке я описал стиль как «перо и акварель». Вышли лист младенца, будка тролля и деревянный смартфон (файлы `05`–`07`). Слова автора: **«в целом ок — но мне не нравится акварель»**. То есть сами придумки подошли, а способ закраски — нет.

**Второй заход.** Четыре образца рисовки (файлы `08`–`11`): два пустынных фона, дом на закате и та же будка, поставленная на пустынный фон. Дом на закате — это **наш собственный старый фон** `bg_act1_birth.png`. Значит, старые фоны игры уже нарисованы так, как нужно.

### Рисовка образцов, разобранная на части

| Что | Как на образцах |
|-----|-----------------|
| Контур | Чистый, уверенный, средней толщины. Тёмный оттенок цвета самого предмета: тёмно-коричневый на камне, тёмно-зелёный на кактусе. Не набросок |
| Цвет | Плотный, ровный, насыщенный. Бумага не просвечивает, разводов нет |
| Тень | Два-три ровных тона на форму. Край тени резкий. Полосы и пятна вместо плавных переходов |
| Фактура | Мелкое зерно внутри заливки. Трещины, доски, потёртости — линией и пятнами |
| Формы | Округлые, крупные, упрощённые |
| Свет | Ясный, с одной стороны. Тени от предметов — плоские пятна |
| Краски | Тёплые охры и кирпичный против чистого синего неба, зелень, редкие красные пятна |

**Третья проба.** Автор сделал фон избы по полному промпту без опорной картинки (`refs/author_refs/13_out_home_v1.jpg`) и спросил, не желтит ли. Желтит: тёплых точек 97% против 53% у старых фонов, холодных почти нет. Причина — моя строка про «тёплую палитру: охра, соломенный». В промптах она заменена на естественные краски с холодными тенями и добавлен запрет на жёлтый налёт. Готовую картинку можно поправить скриптом `python3 web/tools/fix_yellow.py вход выход`; исправленная изба уже стоит в игре.

### Что берём и что нет

- **Берём:** контур, плотный цвет, резкие тени, зерно, округлые формы. Подачу предмета как у будки: вид сверху-сбоку на белом.
- **Не берём:** акварель, набросочную линию, бумажную фактуру, общий жёлтый налёт. Пустыню, планеты и технику — это чужой мир, нам нужна только рисовка.
- **Придумки из первой пробы остаются:** младенец с вихром в зелёном одеяле, будка тролля с бирюзовым кристаллом, деревянный смартфон с резной репой, жуком и бечёвкой.
- **Вторая проба, смартфон** (`refs/author_refs/12_out_phone_v2.jpg`): рисовка получилась та, что нужна. Одно замечание: модель сама добавила блок из двух камер, как у известного телефона. Это узнаваемая черта чужого товара, поэтому в промптах теперь вместо камеры дырка от сучка.

## 2. Правила стиля «Контур и плотный цвет»

1. **Контур.** Чистый, уверенный, средней толщины, тёмный оттенок цвета предмета. Без чёрной обводки и без набросочных линий.
2. **Цвет.** Плотный, ровный, насыщенный.
3. **Тень.** Два-три ровных тона с резкой границей. Свет сверху слева.
4. **Фактура.** Мелкое зерно в заливке.
5. **Потёртость.** Вещи ношеные и чиненые: трещины, сколы краски, швы досок — линией и пятнами.
6. **Формы.** Округлые, крупные, чуть кривые.
7. **Краски.** Естественные, без общего жёлтого налёта: белёная штукатурка, серо-коричневое дерево, терракота, моховой зелёный, чистый синий. Тени холодные, серо-синие.
8. **Система светится.** Всё, что относится к «корпорации» — смартфон, мельница 5G, Бог-Разработчик, Небесная HR, подписки — светится бирюзовым. Свечения в картинке больше нигде нет. На первой пробе это сработало: кристалл в будке и свет из-под смартфона.
9. **Предметы.** Вид сверху-сбоку, один предмет на белом фоне, под ним маленькая плоская тень. Белый фон потом убирается.
10. **Люди.** Добрая карикатура: большая круглая голова, маленькое тело, большие круглые глаза. Тот же контур и та же закраска.
11. **Сцены.** Та же рисовка на весь кадр. Середина спокойная: поверх лягут свиток и карточки.

**Чего быть не должно:** акварели и разводов, бумажной фактуры, набросочных линий, букв и цифр, чужих знаков и логотипов, рамок внутри картинки, фотографичности, 3D, пикселей, современной одежды.

## 3. Состав графики (принято)

У выбора одна простая картинка, на обороте только текст — как в серии Choice of Life.

| Что | Формат | Сколько | Правило |
|-----|--------|---------|---------|
| Фон места | 16:9 | 1 на место, **старые 40 остаются** | Середина спокойная |
| Карточка-предмет | 1:1 | основная масса | Один предмет на белом фоне, вид сверху-сбоку |
| Карточка-жест | 1:1 | около 20 на первую часть | Рука с монетой, рот, ноги, кулак. Рисуется один раз, служит во многих сценах |
| Уникальная карточка | 1:1 | 23 в первой части | Тот же вид, что у карточки-предмета. Лежит в руке игрока |
| Оборот карточки | — | 0 картинок | Текст Рассказчика и значки изменений |
| Портрет говорящего | 1:1, в кружке | 10–12 | Лицо и плечи, белый фон |
| Герой | лист персонажа | 3 возраста | Младенец, ребёнок, взрослый |
| Значки | 1:1 | 4 показателя | Один предмет |

Для первой части нужно 64 картинки на карточки: 45 предметов и 19 жестов. Полный список — в конце [`story/BOOK.md`](./story/BOOK.md).

**Что перерисовать в старых фонах:** `bg_act1_phone_curse.png` (чужой логотип на смартфоне) и `bg_act0_void.png` (пиксели). Остальные подходят.

## 4. Герой: что не меняется

Два признака, по которым героя узнают в любом возрасте:

1. **Вихор-антенна** — одна прядь каштановых волос торчит вверх. У младенца это единственная прядь.
2. **Моховой зелёный цвет** — одеяло у младенца, рубаха у ребёнка и взрослого.

Остальное: круглое лицо, большие круглые глаза, маленький вздёрнутый нос. У ребёнка щель между передними зубами. У взрослого первый пушок усов и холщовая сумка.

## 5. Как держать один стиль в Magnific

Составлено по справке Magnific (Image Generator, разделы References и Custom Styles). В самом интерфейсе я это не проверял — если кнопка называется иначе, скажи.

1. **Опора стиля — наши же старые фоны.** К каждой генерации прикладывай один из них: References → Style → загрузить свою. Хорошо подходят `bg_act1_birth.png`, `bg_act1_fair.png`, `bg_act2_lawyer.png`. Чужие пустынные фоны как опору лучше не брать: рисовку мы уже описали словами, а своё надёжнее.
2. **Свой стиль.** Style → New Style, загрузить 15–20 лучших старых фонов (они 2752×1536, требование — от 2000 пикселей). После этого опору можно не прикладывать руками.
3. **Одна модель на всю игру.** Промпт 6.1 сделай на двух-трёх моделях, которые хорошо держат опорные изображения: Google Nano Banana Pro, GPT 2, Seedream 5 PRO. Выбери ту, что ближе к образцам, запиши её имя сюда и больше не меняй.
4. **Персонаж.** Сначала лист героя прикладываем как опорное изображение. Когда лист утверждён: Character → New character, 8–12 картинок героя, своя метка на каждый возраст (например `@bug_kid`, `@bug_adult`).
5. **Одинаковый текст.** Каждый промпт собран из трёх кусков: блок стиля (слово в слово) + что нарисовать + запреты (слово в слово). Меняется только середина.
6. **Пачками по месту.** Все картинки одного места делаем за один заход, с одними настройками.
7. **Приёмка каждой картинки** — семь вопросов:
   - контур чистый, не набросок и не чёрная обводка?
   - цвет плотный, без разводов?
   - тени резкие, в два-три тона?
   - герой узнаётся: вихор и зелёный цвет на месте?
   - нет букв, цифр, знаков, рамок?
   - читается в размере карточки (уменьшить до 300 пикселей и посмотреть)?
   - не желтит? Если сомневаешься, скрипт `web/tools/fix_yellow.py` печатает «жёлтость»: у старых фонов она около 20, выше 50 — заметно.

   Хоть одно «нет» — перегенерировать, а не чинить.
8. **Журнал.** Рядом с каждым принятым файлом записываем промпт, модель и какие опоры были приложены — в `assets_src/art/PROMPTS.md`.

## 6. Набор промптов (вторая проба)

Те же придумки, что в первой пробе, но с новой рисовкой. Промпты на английском: так модели работают стабильнее. Генерируй по 4 картинки на промпт и к каждому прикладывай наш старый фон как опору стиля. Чужие игры в промптах не называем.

**Блок стиля (в начало каждого промпта)**

```
Background and prop art for a 2D animated cartoon series. Clean, confident outlines of medium weight, drawn in a darker shade of each object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, simplified shapes. Clear daylight from the upper left with flat cast shadows. Age and wear are drawn with line and flat patches: cracks, chipped paint, plank seams, scuffs. Natural, balanced colours with neutral white balance: off-white plaster, grey-brown wood, terracotta, moss green and clear blue; shadows are cool blue-grey.
```

**Запреты (в конец каждого промпта)**

```
No text, no letters, no numbers, no logos, no brand marks, no watermark, no speech bubbles, no interface elements, no frame. No watercolour, no paper texture, no sketchy pencil lines, no painterly brush strokes. No yellow tint, no sepia cast over the picture. Not a photo, not a 3D render, not pixel art, no modern clothes.
```

**6.1. Опорный предмет — будка тролля** · `ref_style_toll_booth.png` · 1:1

```
Background and prop art for a 2D animated cartoon series. Clean, confident outlines of medium weight, drawn in a darker shade of each object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, simplified shapes. Clear daylight from the upper left with flat cast shadows. Age and wear are drawn with line and flat patches: cracks, chipped paint, plank seams, scuffs. Natural, balanced colours with neutral white balance: off-white plaster, grey-brown wood, terracotta, moss green and clear blue; shadows are cool blue-grey.

A single object seen from a three-quarter view from above, standing alone on a plain white background with only a small flat shadow under it: a crooked wooden toll booth from a medieval bridge. A small plank hut on a stubby post, with a thatched roof, an open window with a worn counter, a coin slot cut into the front plank, a striped barrier pole leaning beside it, a rusty bell on a hook, and childish chalk doodles on the side planks. Inside the window hangs one small magic crystal with a turquoise glow. Square 1:1.

No text, no letters, no numbers, no logos, no brand marks, no watermark, no speech bubbles, no interface elements, no frame. No watercolour, no paper texture, no sketchy pencil lines, no painterly brush strokes. No yellow tint, no sepia cast over the picture. Not a photo, not a 3D render, not pixel art, no modern clothes.
```

**6.2. Уникальная карточка — деревянный смартфон** · `card_obj_wooden_phone.png` · 1:1

```
Background and prop art for a 2D animated cartoon series. Clean, confident outlines of medium weight, drawn in a darker shade of each object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, simplified shapes. Clear daylight from the upper left with flat cast shadows. Age and wear are drawn with line and flat patches: cracks, chipped paint, plank seams, scuffs. Natural, balanced colours with neutral white balance: off-white plaster, grey-brown wood, terracotta, moss green and clear blue; shadows are cool blue-grey.

A single object seen from a three-quarter view from above, lying alone on a plain white background with only a small flat shadow under it: a smartphone carved from a slab of tree bark, with rounded corners and knife marks, its back plain wood with a small carved turnip, a crack mended with twine, a tiny bark beetle sitting on its edge. In the upper corner there is one round knot hole instead of a camera: no camera lenses, no camera block. A turquoise glow leaks from its side. Square 1:1.

No text, no letters, no numbers, no logos, no brand marks, no watermark, no speech bubbles, no interface elements, no frame. No watercolour, no paper texture, no sketchy pencil lines, no painterly brush strokes. No yellow tint, no sepia cast over the picture. Not a photo, not a 3D render, not pixel art, no modern clothes.
```

**6.3. Уникальная карточка — Сэр Лаг** · `card_sir_lag.png` · 1:1

Новая карточка-помощник: рыцарь, который отстаёт.

```
Background and prop art for a 2D animated cartoon series. Clean, confident outlines of medium weight, drawn in a darker shade of each object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, simplified shapes. Clear daylight from the upper left with flat cast shadows. Age and wear are drawn with line and flat patches: cracks, chipped paint, plank seams, scuffs. Natural, balanced colours with neutral white balance: off-white plaster, grey-brown wood, terracotta, moss green and clear blue; shadows are cool blue-grey. Characters are drawn the same way: clean outline, flat colours, cel shading. They are gentle caricatures with large round heads, small bodies, big round eyes and broad comic expressions.

A single character seen from a three-quarter view, standing alone on a plain white background with only a small flat shadow under him: a stout medieval knight in heavy, dented, patched plate armour, frozen in the middle of a step with one foot in the air, as if stuck. A closed helmet with a narrow visor and a bent feather, a kind and confused look in the visor slit, a small chipped shield on his back. Three faint turquoise after-images of his raised foot trail behind it. Square 1:1.

No text, no letters, no numbers, no logos, no brand marks, no watermark, no speech bubbles, no interface elements, no frame. No watercolour, no paper texture, no sketchy pencil lines, no painterly brush strokes. No yellow tint, no sepia cast over the picture. Not a photo, not a 3D render, not pixel art, no modern clothes.
```

**6.4. Герой — младенец** · `hero_baby_sheet.png` · 16:9

```
Background and prop art for a 2D animated cartoon series. Clean, confident outlines of medium weight, drawn in a darker shade of each object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, simplified shapes. Clear daylight from the upper left with flat cast shadows. Age and wear are drawn with line and flat patches: cracks, chipped paint, plank seams, scuffs. Natural, balanced colours with neutral white balance: off-white plaster, grey-brown wood, terracotta, moss green and clear blue; shadows are cool blue-grey. Characters are drawn the same way: clean outline, flat colours, cel shading. They are gentle caricatures with large round heads, small bodies, big round eyes and broad comic expressions.

Character sheet on a plain white background: the same baby drawn four times in a row — lying in a patched wooden cradle, sitting up, crying with the mouth wide open, and grinning slyly. A chubby medieval peasant baby with a round face, huge round eyes, a small upturned nose and one single tuft of chestnut hair sticking straight up like an antenna, wrapped in a worn moss-green blanket. The same face and the same proportions in all four drawings. Wide 16:9.

No text, no letters, no numbers, no logos, no brand marks, no watermark, no speech bubbles, no interface elements, no frame. No watercolour, no paper texture, no sketchy pencil lines, no painterly brush strokes. No yellow tint, no sepia cast over the picture. Not a photo, not a 3D render, not pixel art, no modern clothes.
```

**6.5. Герой — ребёнок 10 лет** · `hero_child_sheet.png` · 16:9

```
Background and prop art for a 2D animated cartoon series. Clean, confident outlines of medium weight, drawn in a darker shade of each object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, simplified shapes. Clear daylight from the upper left with flat cast shadows. Age and wear are drawn with line and flat patches: cracks, chipped paint, plank seams, scuffs. Natural, balanced colours with neutral white balance: off-white plaster, grey-brown wood, terracotta, moss green and clear blue; shadows are cool blue-grey. Characters are drawn the same way: clean outline, flat colours, cel shading. They are gentle caricatures with large round heads, small bodies, big round eyes and broad comic expressions.

Character sheet on a plain white background: the same ten-year-old peasant boy drawn four times in a row — standing front view, three-quarter view, side view, and laughing. Round face, large round eyes, small upturned nose, a gap between the front teeth, messy chestnut hair with one tuft sticking straight up like an antenna. A patched moss-green tunic with a rope belt, mended brown trousers, bare muddy feet. The same face, clothes and proportions in all four drawings. Wide 16:9.

No text, no letters, no numbers, no logos, no brand marks, no watermark, no speech bubbles, no interface elements, no frame. No watercolour, no paper texture, no sketchy pencil lines, no painterly brush strokes. No yellow tint, no sepia cast over the picture. Not a photo, not a 3D render, not pixel art, no modern clothes.
```

**6.6. Герой — взрослый 18 лет** · `hero_adult_sheet.png` · 16:9

```
Background and prop art for a 2D animated cartoon series. Clean, confident outlines of medium weight, drawn in a darker shade of each object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, simplified shapes. Clear daylight from the upper left with flat cast shadows. Age and wear are drawn with line and flat patches: cracks, chipped paint, plank seams, scuffs. Natural, balanced colours with neutral white balance: off-white plaster, grey-brown wood, terracotta, moss green and clear blue; shadows are cool blue-grey. Characters are drawn the same way: clean outline, flat colours, cel shading. They are gentle caricatures with large round heads, small bodies, big round eyes and broad comic expressions.

Character sheet on a plain white background: the same eighteen-year-old peasant youth drawn four times in a row — standing front view, three-quarter view, side view, and shrugging with a sheepish smile. Tall and lanky, the same round face and large round eyes as in childhood, small upturned nose, first thin fuzz of a moustache, messy chestnut hair with one tuft sticking straight up like an antenna. A patched moss-green tunic with a rope belt, brown trousers, worn boots, a canvas shoulder bag. The same face, clothes and proportions in all four drawings. Wide 16:9.

No text, no letters, no numbers, no logos, no brand marks, no watermark, no speech bubbles, no interface elements, no frame. No watercolour, no paper texture, no sketchy pencil lines, no painterly brush strokes. No yellow tint, no sepia cast over the picture. Not a photo, not a 3D render, not pixel art, no modern clothes.
```

**6.7. Фон — изба героя днём** · `bg_home_day.png` · 16:9

Этого фона сейчас нет, а он нужен часто: дом, стол, приход маминой подруги.

```
Background and prop art for a 2D animated cartoon series. Clean, confident outlines of medium weight, drawn in a darker shade of each object's own colour rather than black. Flat, opaque colours. Cel shading: two or three flat tones per surface with hard-edged shadow shapes and no soft gradients. A fine grainy speckle texture inside the colour fills. Rounded, chunky, simplified shapes. Clear daylight from the upper left with flat cast shadows. Age and wear are drawn with line and flat patches: cracks, chipped paint, plank seams, scuffs. Natural, balanced colours with neutral white balance: off-white plaster, grey-brown wood, terracotta, moss green and clear blue; shadows are cool blue-grey.

A full scene without people: the inside of a poor but cosy medieval peasant hut in daytime. A rough wooden table with two stools in the middle, a clay stove on the left, a patched wooden cradle in the corner, bunches of herbs and onions hanging from the beams, a small window with sunlight falling on the table in a hard-edged patch of light, a door slightly open to a muddy yard. The middle of the picture is calm and uncluttered. Full-bleed, wide 16:9.

No text, no letters, no numbers, no logos, no brand marks, no watermark, no speech bubbles, no interface elements, no frame. No watercolour, no paper texture, no sketchy pencil lines, no painterly brush strokes. No yellow tint, no sepia cast over the picture. Not a photo, not a 3D render, not pixel art, no modern clothes.
```

### Короткие промпты с опорой через @

Автор попросил промпты, где рисовка берётся с опорной картинки, а сама картинка указывается в тексте через «@». В запросах опора названа `@img1`: так Magnific называет первую приложенную картинку. Вписывать её имя в каждый запрос не нужно. Как опору бери картинку в правильной рисовке: наш старый фон или новый смартфон (`refs/author_refs/12_out_phone_v2.jpg`).

**Шаблон: своё описание вместо скобок**

```
Use @img1 only as a style reference. Copy only its drawing style: clean outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw: [ЧТО НАРИСОВАТЬ]

[ПОДАЧА]. No text, no logos, no frame.
```

Подача на выбор:

- предмет: `Three-quarter view from above, alone on a plain white background with a small flat shadow. Square 1:1`
- лист персонажа: `Character sheet on a plain white background: the same character four times in a row. Wide 16:9`
- фон: `A full scene without people, the middle calm and uncluttered. Wide 16:9`

**Короткий 1. Сэр Лаг** · 1:1

```
Use @img1 only as a style reference. Copy only its drawing style: clean outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw: a stout medieval knight in heavy, dented, patched plate armour, frozen in the middle of a step with one foot in the air, as if stuck. Closed helmet with a narrow visor and a bent feather, a small chipped shield on his back. Three faint turquoise after-images of his raised foot trail behind it.

Three-quarter view, alone on a plain white background with a small flat shadow. Square 1:1. No text, no logos, no frame.
```

**Короткий 2. Герой — ребёнок 10 лет** · 16:9

```
Use @img1 only as a style reference. Copy only its drawing style: clean outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a character sheet: the same ten-year-old medieval peasant boy four times in a row — front view, three-quarter view, side view, and laughing. Big round head, small body, large round eyes, small upturned nose, a gap between the front teeth, messy chestnut hair with one tuft sticking straight up like an antenna. Patched moss-green tunic with a rope belt, mended brown trousers, bare muddy feet. The same face and clothes in all four.

Plain white background. Wide 16:9. No text, no logos, no frame.
```

**Короткий 3. Фон — изба героя днём** · 16:9

```
Use @img1 only as a style reference. Copy only its drawing style: clean outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the object, the composition or any details from @img1.

Draw a full scene without people: the inside of a poor but cosy medieval peasant hut in daytime. A rough wooden table with two stools in the middle, a clay stove on the left, a patched wooden cradle in the corner, herbs and onions hanging from the beams, a small window with a hard-edged patch of sunlight on the table, a door slightly open to a muddy yard. Keep the middle calm and uncluttered.

Wide 16:9. No text, no logos, no frame.
```

**Короткий 4. Деревянный смартфон без камеры** · 1:1

```
Use @img1 only as a style reference. Copy only its drawing style: clean outlines in a darker shade of each colour, flat opaque colours, hard-edged shadows in two or three tones, fine grain texture. Do not copy the composition from @img1.

Draw: a smartphone carved from a slab of tree bark, with rounded corners, patches of moss and a crack stitched with twine. A turnip is carved into its back. In the upper corner there is one round knot hole instead of a camera. A small bark beetle sits on its edge. A turquoise glow leaks from under its side. No camera lenses, no camera block.

Three-quarter view from above, alone on a plain white background with a small flat shadow. Square 1:1. No text, no logos, no frame.
```

### Что прислать после генерации

Лучший вариант каждой картинки и одно слово: «хорошо» или что не так.

## 7. Что дальше по графике

После «хорошо»:

1. Закрепляю правила из раздела 2 окончательно.
2. Портреты постоянных персонажей: мама, отец, брат, Сын Маминой Подруги, Мамина подруга, Бог-Разработчик, купец, король, дракон, гоблин.
3. Значки четырёх показателей.
4. Остальные уникальные карточки первой части.
5. Карточки-предметы и жесты первой части — по списку из `story/BOOK.md`.
6. Замена двух старых фонов (логотип и пиксели).
7. Переписать `assets_src/art/PROMPTS.md` под новые правила.

## 8. Что было не так раньше

- **Карточки (152 штуки)** в пяти с лишним стилях: пиксельный Бог на белом фоне, дети в современной одежде, рамки то есть, то нет, английские надписи внутри картинок.
- На деревянном смартфоне был чужой логотип. Теперь там резная репа.
- По правилу «лицо и рубашка» каждому выбору нужны были две полные сцены.
- В старых промптах стиль задан ссылкой на чужую игру.

## 9. История выбора

1. Три направления на выбор: «Тёплая книга», «Рукопись», «Лубок». Ни одно не выбрано.
2. Примеры автора, первый заход: рисовка будки. Я описал её как перо и акварель — ошибся в закраске.
3. Первая проба: придумки подошли, акварель нет.
4. Примеры автора, второй заход: мультяшные фоны с чётким контуром и плотным цветом, среди них наш старый фон. Это действующие правила.
