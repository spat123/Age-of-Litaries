# Промпты арта — Сэр Баг / Age of Litaries (Акты 0–2)

Стиль: **Choice of Life Middle Ages** — hand-drawn 2D cartoon, flat colors, clean outlines, whimsical satirical medieval.  
Промпты на английском (так стабильнее для генерации).

---

## Правило лица vs рубашки (важно!)

| Сторона | Файл | Что рисуем |
|---------|------|------------|
| **Лицо** | `card_foo.png` | Только **действие** |
| **Рубашка (flip)** | `card_foo_result.png` | **Исход** (то, что раньше ошибочно было на лице) |

В коде: если `result_art` не задан, берётся `art` с суффиксом `_result` перед `.png`.

В промпт лица: `FRONT (action only, NOT outcome)`  
В промпт рубашки: `BACK RESULT` / `OUTCOME`

### Шаблон фона (aspect **16:9**)
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. [СЦЕНА]. flat colors, clean ink outlines, whimsical satirical medieval, NO text, NO UI, NO letters.
```

### Шаблон карточки — ДЕЙСТВИЕ (aspect **1:1**)
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: [ДЕЙСТВИЕ в процессе]. flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```

---

## Фоны (16:9)

### `bg_act0_void.png` — Акт 0, общение с Богом
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed ethereal Early Access void with soft blue screen-of-death glow, floating pixel particles, giant floating bearded pixel God-Developer head watching from above, empty stage for dialogue, flat colors, clean ink outlines, whimsical satirical medieval, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act1_birth.png` — 1.0 Рождение
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed medieval village birthing room interior: wooden hut, straw bed, candlelight, quirky midwife with parchment and quill waiting, muddy village visible through open door, Wi-Fi symbols jokingly carved in wood beams, warm earthy palette, flat colors, clean ink outlines, whimsical satirical medieval, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act1_fair.png` — 1.4 Ярмарка
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Medieval village fair square at daytime: colorful wagon caravan, merchant in robe behind a wooden barrel stall with weird gadgets, peasants, mud street, thatched houses, funny tech satire vibe with wooden antennas, flat colors, clean outlines, whimsical, NO text, NO UI, NO letters.
```

### `bg_act1_bootcamp.png` — 1.5 Bootcamp
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Church parish school yard: stone chapel, monk teacher, dirt ground with fork marks like code, wooden benches, children with pitchforks as pens, satirical bootcamp vibe, soft daylight, flat colors, clean ink outlines, whimsical medieval, NO text, NO UI, NO letters.
```

### `bg_act1_windmill.png` — 1.6 Мельница 5G
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Village scene with a tall wooden windmill that looks suspiciously like a cell tower with glowing blue 5G vibes, scared peasants pointing, hills at dusk, purple-green sky, flat colors, clean outlines, whimsical satirical medieval, NO text, NO UI, NO letters.
```

### `bg_act1_first_word.png` — 1.1 Первое слово
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Cozy medieval wooden hut interior at night, wooden cradle in center, peasant mother and father leaning over baby, warm candlelight, thatched roof, muddy boots by door, flat colors, clean ink outlines, whimsical satirical medieval, NO text, NO UI, NO letters.
```

### `bg_act1_sandbox.png` — 1.2 Песочница
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Village mud sandbox playground, peasant children building a manure castle, wooden fence, thatched houses, daytime, dirt and puddles, flat colors, clean outlines, whimsical satirical medieval, NO text, NO UI, NO letters.
```

### `bg_act1_dig.png` — 1.3 Грязекопатель
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Rural farmyard, wooden fence, pig sty, father figure handing a shovel to a child, muddy field to dig, morning light, medieval village, flat colors, clean outlines, whimsical satirical medieval, NO text, NO UI, NO letters.
```

### `bg_act1_military.png` — 1.8 Военкомат
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Village square with royal recruiter in armor holding a birch-bark draft notice scroll, nervous teenagers, wooden cart, banners, daytime medieval, flat colors, clean outlines, whimsical satirical medieval, NO text, NO UI, NO letters.
```

### `bg_act1_phone_curse.png` — авто-проклятие смартфона
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed cursed wooden smartphone nightmare scene: giant bark phone with painted apple hovering over a village bed, blue 4G ghostly glow, frightened sleeper silhouette, floating notification spirits as birds, flat colors, clean ink outlines, whimsical satirical medieval, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act1_road_lag.png` — Тракт: Сэр Лаг
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed medieval roadside at dusk: heavy knight in bulky armor frozen mid-lag stutter pose on dirt road shoulder, pixel-glitch sparks around joints, distant capital silhouette, birch trees, muddy track, soft orange-purple sky, flat colors, clean ink outlines, whimsical satirical medieval, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act1_road_troll.png` — Тракт: Толл-Плаза
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed wooden toll bridge over muddy river: fat troll in tiny toll-booth shack, wooden barrier boom gate lowered, meme-road vibe, birch bark posters, hills and dirt path, daytime, flat colors, clean ink outlines, whimsical satirical medieval, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act1_road_camp.png` — Тракт: ночной привал / Инфоцыган
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed night camp on meme tract road: glowing campfire, fancy-dressed bard merchant by bushes, travel wagon, stars, dirt road edge, warm firelight vs cool night, flat colors, clean ink outlines, whimsical, NO text, NO UI, NO letters, NO watermark.
```

---

## Карточки — ЛИЦО = действие (1:1)

> Перегенерены 2026-08-09 под правило action-only.

### `card_smoothie.png` — кричать про смузи
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: newborn baby in cradle angrily yelling and demanding a green smoothie cup held up, midwife listening, NO fighting NO nettles NO injury, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```

### `card_eula.png` — принять EULA
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: calm baby placing a handprint on a giant sealed parchment life contract, quiet acceptance pose, NO coins NO rewards shown, flat colors, clean outlines, whimsical medieval satire, scribbles instead of readable text, NO UI.
```

### `card_skip.png` — скип катсцены
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: baby squeezing eyes shut tightly trying to skip a cutscene, hands covering eyes, wooden cradle, NO bump NO injury NO stars of pain, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_agu.png` — сказать «Агу»
```
Hand-drawn 2D cartoon choice card, Choice of Life style. Square: cute medieval baby in cradle saying Agu, happy peasant parents smiling, flat colors, clean outlines, whimsical, NO text, NO UI.
```
Рубашка `card_agu_result.png`: скучный дефолт, родители рады, малыш банален.

### `card_blockchain.png` — сказать «Блокчейн»
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: baby in cradle proudly speaking a fancy tech word with confident open mouth, parents listening curiously, NOT fainting yet, medieval, flat colors, clean outlines, whimsical satire, NO readable text, NO UI.
```

### `card_birds_drones.png` — «Птицы — это дроны Короля!»
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: toddler in cradle pointing up at birds in the sky, conspiratorial wide-eyed face, birds look slightly mechanical with tiny crown badges or wooden propeller vibe (subtle, not sci-fi), peasant parents listening in shock, medieval village window, flat colors, clean outlines, whimsical satirical medieval, NO readable text, NO UI, NO letters.
```
Рубашка `card_birds_drones_result.png`:
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: peasant parents crossing themselves in horror while toddler smirks, birds circling outside like surveillance drones with tiny royal crowns, mental-pen idea vibe, flat colors, clean outlines, whimsical medieval satire, NO readable text, NO UI.
```

### `card_donate_cry.png` — потребовать донат
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: crying baby in cradle demanding a donation with outstretched hands, dramatic tantrum, father listening, NO coin placed yet, medieval, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_help_castle.png` — помочь строить замок
```
Hand-drawn 2D cartoon choice card, Choice of Life style. Square: child helping other kids build a manure castle in mud sandbox, teamwork, flat colors, clean outlines, whimsical medieval, NO text, NO UI.
```

### `card_coworking.png` — строить коворкинг
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: child carefully building a manure coworking with tiny desks and stools in sandbox, focused entrepreneur pose, other kids watching, NOT fighting yet, flat colors, clean outlines, whimsical satire, NO text, NO UI.
```

### `card_monopoly.png` — забрать лопатки
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: child gathering all toy shovels into a pile declaring monopoly, smug tiny tyrant pose, other kids empty-handed watching, NOT biting yet, mud sandbox, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_dig_silent.png` — копать молча
```
Hand-drawn 2D cartoon choice card, Choice of Life style. Square: tired peasant child digging silently with shovel near wooden fence, sore back, flat colors, clean outlines, whimsical medieval, NO text, NO UI.
```

### `card_pig_automation.png` — привязать лопату к свинье
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: child tying a shovel to a calm pig as automation experiment, hopeful inventor pose, fence intact, NOT rampaging yet, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```

### `card_delegate_brother.png` — делегировать брату
```
Hand-drawn 2D cartoon choice card, Choice of Life style. Square: older child giving candy lollipop to younger brother to dig instead, management vibe, farmyard, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_wooden_phone.png` — купить смартфон
```
Hand-drawn 2D cartoon choice card illustration, Choice of Life style. Square scene: wooden smartphone made of bark with a painted apple logo, child holding it proudly at a fair, flat colors, clean outlines, whimsical medieval tech satire, NO text, NO UI.
```

### `card_foil_hat.png` — надеть фольгу
```
Hand-drawn 2D cartoon choice card illustration, Choice of Life style. Square scene: child proudly wearing a shiny tin-foil hat made from an old kettle/pot, merchant laughing in background, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```

### `card_steal_gem.png` — красть камень
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: child secretly reaching to steal a shiny gem from merchant stall, sneaky pose mid-theft, NO dogs biting yet, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```

### `card_pentagram.png` — рисовать пентаграмму
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: child carefully drawing a glowing pentagram on dirt with a pitchfork, focused coding mistake vibe, NO demon yet NO stolen lunch, monastery yard, flat colors, clean outlines, whimsical satire, NO text, NO UI.
```

### `card_cheat.png` — списывать
```
Hand-drawn 2D cartoon choice card illustration, Choice of Life style. Square scene: child peeking at neighbor's slate to cheat during latin exam, monk looking away, school yard, flat colors, clean outlines, whimsical medieval satire, NO readable text, NO UI.
```

### `card_bribe_puppies.png` — давать взятку щенками
```
Hand-drawn 2D cartoon choice card illustration, Choice of Life style. Square scene: child offering cute borzoi puppy dogs as a bribe to a monk teacher, monk accepting with stamp auto-pass, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```

### `card_ddos_stick.png` — бить мельницу палкой
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: peasant child swinging a big stick at windmill blades in a DDoS attack pose, determined charge, NOT hit yet NO injury, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```

### `card_podcast.png` — писать подкаст
```
Hand-drawn 2D cartoon choice card illustration, Choice of Life style. Square scene: child recording a conspiracy podcast on birch bark scroll with quill near windmill, peasants listening, flat colors, clean outlines, whimsical medieval satire, NO readable text, NO UI.
```

### `card_ignore_sleep.png` — идти спать
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: child calmly going to sleep in bed under blanket, peaceful, NO nightmare NO Bill Gates NO chips in dream, flat colors, clean outlines, whimsical medieval, NO text, NO UI.
```

### `card_bribe_flatfoot.png` — давать взятку рекрутеру
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: teenager handing gold coins to armored royal recruiter as a bribe, negotiation pose, NO stamp NO medical paper result shown yet, flat colors, clean outlines, whimsical medieval satire, NO readable text, NO UI.
```

### `card_relocate_forest.png` — сбегать в лес
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: teenager starting to sneak away toward forest edge to escape draft, looking back nervously, action of fleeing beginning, NOT bitten by ticks yet, daytime into trees, flat colors, clean outlines, whimsical medieval, NO text, NO UI.
```

### `card_serve_proudly.png` — идти служить
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: proud teenager volunteering for royal crusade, saluting armored recruiter with chest out, eager enlistment pose, NOT exhausted NOT carrying stones yet, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```

---

## Акт 0 — туториал (карточки 1:1)

| Выбор | Лицо | Рубашка |
|-------|------|---------|
| Где я? Почему пиксели? | `card_act0_confused.png` | `card_act0_confused_result.png` |
| Скип / «В бой» | `card_act0_skip_fight.png` | `card_act0_skip_fight_result.png` |
| Слава Архитектору | `card_act0_loyal.png` | `card_act0_loyal_result.png` |
| Тверк перед Богом | `card_act0_twerk.png` | `card_act0_twerk_result.png` |
| Отказаться от приказа | `card_act0_defy.png` | `card_act0_defy_result.png` |
| [Скрытый] предмет | `card_act0_loot.png` | `card_act0_loot_result.png` |

## Новые карточки Акт 1 / 1.5
- ~~`card_birds_drones`~~ — промпт выше (лицо + рубашка); файлы уже в `cards/`
- `card_matrix` — «Мир — Матрица» *(промпта ещё нет)*
- `card_troll_*` — Толл-Плаза
- `card_sir_lag_*` — Сэр Лаг
- `card_infogypsy_*` — Инфоцыганъ

---

## Акт 2 — Биг Дата (фоны 16:9 + карточки 1:1)

> **Статус рубашек:** перегенерены 2026-08-09 (Cursor). Файлы в `cards/`.  
> **Новые фоны тракта / акта 3:** `bg_act1_road_*`, `bg_act1_phone_curse`, `bg_act3_*` — подключены в коде.

### Фоны Акта 2

### `bg_act2_customs.png` — 2.0 Таможня Face Control
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed medieval city gate customs checkpoint: giant shield divided into 9 captcha squares blocking the gate, armored guard with birch-bark scanner, queue of muddy peasants, timber-framed capital city "Big Data" beyond the gate, satirical tech-bureaucracy vibe, flat colors, clean ink outlines, whimsical satirical medieval, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act2_city.png` — рынок / подворотни Биг Дата
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed bustling medieval capital alley market: timber houses, banners, black-market elf stall with glowing "smart" swords, muddy cobbles, castle silhouette in distance, funny SaaS-medieval satire, daytime, flat colors, clean ink outlines, whimsical, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act2_guilds.png` — 2.2 Биржа труда
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed three fantastical doorways side by side: sweaty warrior guild hall with sweat towels and deadlines, sparking mage tower with bug-like sparks, shady thieves crypt with glowing NFT radish vibe, VIP door ajar with smug rich kid silhouette, medieval job fair satire, flat colors, clean outlines, whimsical, NO text, NO UI, NO letters.
```

### `bg_act2_hr.png` — 2.4 HR-Инквизиция
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed dark interrogation chamber: inquisitor-HR desk with harsh desk lamp shining into chair, birch-bark complaint scrolls, holy bureaucracy icons, cold stone walls, satirical HR inquisition mood, flat colors, clean ink outlines, whimsical medieval satire, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act2_arena.png` — 2.5 Турнир / корпоратив
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed medieval corporate arena: wooden stands full of nobles with laptops-as-scrolls joke vibe, sandy fighting pit, banners of the King, daylight spectacle, satirical office team-building as joust, flat colors, clean outlines, whimsical, NO text, NO UI, NO letters.
```

### `bg_act2_forest.png` — Лес Релокантов
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed dark relocant forest: hammocks in trees, bearded freelancers with moss smoothies, VPN-pine silhouette, campfire glow, remote-work bandit camp satire, cool greens and dusk light, flat colors, clean ink outlines, whimsical, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act2_swamp.png` — Болото Апдейтов
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed glitchy swamp: muddy water with vanishing pixels, frogs with autotune vibe, mist, broken UI-like lily pads, lordly armor silhouette rising from muck, version-control swamp satire, sickly greens and purples, flat colors, clean outlines, whimsical, NO text, NO UI, NO letters.
```

---

### Карточки Акта 2 — ЛИЦО + РУБАШКА

Шаблон лица / рубашки — как в шапке файла (`FRONT action only` / `BACK RESULT outcome`).

#### Таможня (2.0)

### `card_a2_captcha_lantern.png` — ткнуть в фонари
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: muddy hero poking a finger at carriage lanterns on a 9-square captcha shield, confused focus, guard watching, NOT punished yet, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```
### `card_a2_captcha_lantern_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: guard sighing and collecting a stupidity tax coin from the hero, premium carriage in background, embarrassed hero, flat colors, clean outlines, whimsical, NO readable text, NO UI.
```

### `card_a2_hr_lamp.png` — лампа / красные глаза / допрос
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: harsh desk lamp glaring into hero's face, inquisitor silhouette leaning in, tense interrogation pose, NOT verdict yet, flat colors, clean outlines, whimsical medieval HR satire, NO text, NO UI.
```
### `card_a2_hr_lamp_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: hero soaked or scolded under the lamp, inquisitor stamping a birch scroll, comic humiliation, flat colors, clean outlines, whimsical, NO readable text, NO UI.
```

### `card_a2_not_robot.png` — «я не робот, я грязный»
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: filthy peasant hero proudly pointing at himself claiming humanity, muddy clothes, customs gate behind, NOT splashed yet, flat colors, clean outlines, whimsical, NO text, NO UI.
```
### `card_a2_not_robot_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: hero completely soaked in mud from a noble cart splash, wetter and dirtier, peasants laughing, flat colors, clean outlines, whimsical satire, NO text, NO UI.
```

### `card_a2_punch_guard.png` — дать стражнику в глаз
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hero winding up a punch toward armored customs guard, mid-swing action, NOT landed yet, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```
### `card_a2_punch_guard_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: hero in stocks or tiny jail cell looking proud anyway, crowd of peasants cheering him as folk hero, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_a2_buy_rusty.png` — ржавый меч (купить / показать / прорыв)
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hero holding up a very rusty medieval sword proudly, negotiating or presenting it, action of offering the blade, NOT broken yet, flat colors, clean outlines, whimsical, NO text, NO UI.
```
### `card_a2_buy_rusty_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: rusty sword shattered into pieces on the ground after a failed charge, hero bruised in a tiny lockup, guard unimpressed, flat colors, clean outlines, whimsical satire, NO text, NO UI.
```

#### Рынок / кузня (2.1–2.8)

### `card_a2_apple_calibur.png` — Apple-Калибур / смарт-меч
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: elf presenting a glowing high-tech looking sword with a tiny wooden apple motif, hero reaching to subscribe/take it, SaaS weapon pitch in progress, NOT expired yet, flat colors, clean outlines, whimsical medieval tech satire, NO readable text, NO UI.
```
### `card_a2_apple_calibur_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: glowing sword suddenly dark and cracked with "subscription expired" vibe (no readable letters — use X stickers / broken glow), hero getting beaten in arena, comic SaaS curse, flat colors, clean outlines, whimsical, NO UI.
```

### `card_a2_lawyer_owl.png` — нотариус / юрист-филин
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: wise owl in glasses and tiny suit jacket offering a quill contract from a tree hollow, hero about to sign, legal satire pose, NOT stamped yet, flat colors, clean outlines, whimsical medieval, NO readable text, NO UI.
```
### `card_a2_lawyer_owl_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: owl stamping a red soul-subscription seal or handing a glowing red lawsuit folder, hero looking unsure, flat colors, clean outlines, whimsical satire, scribbles instead of readable text, NO UI.
```

### `card_a2_fists.png` — кулаки / «я дерусь на кулаках»
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: young hero raising bare fists confidently, no weapon, market alley behind, proud budget warrior pose, flat colors, clean outlines, whimsical, NO text, NO UI.
```
### `card_a2_fists_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: elf shrugging while peasants nod respectfully at fist-fighter hero, empty coin pouch joke, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_a2_plantain.png` — подорожник / био-модуль
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hero carefully picking a glowing antivirus plantain leaf from swampy forest ground, hopeful craft ingredient pose, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```
### `card_a2_plantain_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: foil hat upgraded into a bio-antenna bush-on-head, hero hearing ancestor voices (swirly comic spirits), orc smith proud, flat colors, clean outlines, whimsical, NO text, NO UI.
```

#### Гильдии (2.2–2.3)

### `card_a2_warriors_door.png` — дверь Воинов
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hero opening a sweaty armored guild door, manager in plate armor waiting with overtime scroll, action of entering, NOT hired outcome yet, flat colors, clean outlines, whimsical corporate-medieval satire, NO readable text, NO UI.
```
### `card_a2_warriors_door_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: exhausted hero in armor carrying huge rocks, smug rich kid laughing at his salary, overtime burnout comedy, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_a2_mages_door.png` — дверь Магов
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hero knocking on sparking mage tower door, bearded senior archmage with crystal ball, coding-magic vibe, NOT accepted yet, flat colors, clean outlines, whimsical satire, NO readable text, NO UI.
```
### `card_a2_mages_door_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: hero as junior coffee-mage carrying potion mugs, or hugging archmage after googling a spell, sparking firewall bug in background, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_a2_thieves_door.png` — дверь Воров / NFT
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hooded hacker whispering about a glowing NFT radish in a crypt startup den, hero listening, crypto-medieval pitch in progress, flat colors, clean outlines, whimsical satire, NO readable text, NO UI.
```
### `card_a2_thieves_door_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: hero either poorer holding worthless radish coin OR triumphant boss of thieves after scanning the radish with wooden phone, hacker freaking out, flat colors, clean outlines, whimsical, NO text, NO UI.
```

#### Тиндер / арена (2.5–2.7)

### `card_a2_tinder.png` — свайп свахи
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: old matchmaker granny holding birch-bark portrait cards, hero mid-swipe gesture, dating algorithm satire, NOT matched yet, flat colors, clean outlines, whimsical medieval, NO readable text, NO UI.
```
### `card_a2_tinder_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: either duck-lips scam asking for crusade donation OR happy match with blacksmith daughter OR accidental match with fat Venture Baron giving gold, comic outcome, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_a2_arena_honest.png` — драться честно
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hero fighting fairly in sandy arena with rusty or bare stance, noble duel pose mid-fight, NOT victory screen yet, flat colors, clean outlines, whimsical, NO text, NO UI.
```
### `card_a2_arena_honest_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: battered but victorious hero receiving a gold purse and crowd cheers, bruises visible, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```

### `card_a2_arena_sand.png` — песок в глаза / пинok
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hero scooping arena sand to throw at opponent's eyes, sneaky mid-action, NOT landed yet, flat colors, clean outlines, whimsical dirty-fighting satire, NO text, NO UI.
```
### `card_a2_arena_sand_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: opponent blinded rubbing eyes, crowd booing, hero grabbing prize money looking shameless, OR swamp lord kicked in the shin falling into mud (reuse vibe), flat colors, clean outlines, whimsical, NO text, NO UI.
```

#### Сайды: лес / болото (2.9–2.12)

### `card_a2_freelancers.png` — лагерь фрилансеров
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hero approaching campfire bandits reading birch task scrolls, asking for Lawyer Logovov, remote-robber camp, action of arriving, flat colors, clean outlines, whimsical relocant satire, NO readable text, NO UI.
```
### `card_a2_freelancers_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: bandits respectfully parting after seeing useless premium pass OR taking gold for express appointment, hero led toward VPN-pine hollow, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_a2_lord_rollback.png` — Лорд Отката
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: color-shifting armored knight rising from swamp challenging hero, hero raising weapon to strike from above, mid-swing, NOT 404 yet, flat colors, clean outlines, whimsical version-control satire, NO readable text, NO UI.
```
### `card_a2_lord_rollback_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: comic 404 glitch vibe (broken swing disappearing), then hero kicking lord in the shin into swamp while lord downloads updates, victory-by-bug, flat colors, clean outlines, whimsical, NO UI letters — use glitch shapes only.
```

### `card_a2_patch.png` — Патч 1.0
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hero reaching for a glowing floppy disk on a swamp temple altar labeled only with abstract holy tech symbols (no readable text), reverent loot pose, flat colors, clean outlines, whimsical, NO UI.
```
### `card_a2_patch_result.png`
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: glowing patch disk warm in hero's pocket/bag, soft hum aura, hopeful end-of-sidequest beat, flat colors, clean outlines, whimsical medieval tech satire, NO text, NO UI.
```

---

### Чеклист генерации Акта 2 (рубашки first)

1. ~~Сгенерировать все `card_a2_*_result.png`~~ ✅ 2026-08-09
2. По желанию реген лиц, если текущие слабые.
3. Фоны `bg_act2_*` — реген только если нужно выровнять стиль.
4. ~~Фоны тракта / phone curse / акт 3 castle-road-cave~~ ✅ подключены
5. После — уникальные **карточки** Акта 3 (`card_a3_*`).

### Фоны Акта 3 (уже сгенерены)

### `bg_act3_castle.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed royal Capital Castle interior throne hall: ornate medieval throne with corporate KPI tapestry vibe, stained glass with chart shapes, marble floor, satirical king startup castle, daylight, flat colors, clean ink outlines, whimsical, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act3_road.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed road to the dragon: winding path through hills toward smoking mountain cave mouth, royal banners on poles, late afternoon, flat colors, clean ink outlines, whimsical satirical medieval, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act3_cave.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed dragon lair cave: treasure piles mixed with floppy disks and glowing code runes, rocky cavern, distant dragon silhouette on gold, mystical teal-orange light, flat colors, clean ink outlines, whimsical, NO text, NO UI, NO letters, NO watermark.
```

---

## Дыры по фонам (аудит 2026-08-10) — где нужен УНИКАЛЬНЫЙ арт

> Сейчас в `backgrounds/` **34 файла**. Act 0–1.5 закрыты 1:1.  
> **P0 (10 шт.) — сгенерены 2026-08-10 и подключены в код.** Ниже — что ещё (P1/P2).

### Уже OK (не трогать) + P0 закрыто
| Зона | Фоны |
|------|------|
| Акт 0 | `bg_act0_void` |
| Акт 1 | birth / first_word / sandbox / dig / fair / bootcamp / windmill / military / phone_curse |
| Тракт 1.5 | road_lag / road_troll / road_camp |
| Акт 2 ядро | customs / city / guilds / hr / arena + **forge / tinder / tavern** ✅ + **warriors/mages/thieves** ✅ |
| Сайды | forest / swamp + **lawyer / swamp_lord / temple** ✅ |
| Акт 3 | castle / road / cave + **ball / scrum / cafe / glitch** ✅ + **boardroom** ✅ |
| Meta | **hr_shop / event_riot / event_kpi** ✅ |

### P0 — ~~срочно~~ ✅ готово

| Файл | Сцена | Статус |
|------|-------|--------|
| `bg_act2_forge.png` | Кузня | ✅ |
| `bg_act2_tinder.png` | Сваха | ✅ |
| `bg_act2_tavern.png` | Ctrl+Ale | ✅ |
| `bg_act3_ball.png` | Бал | ✅ |
| `bg_act3_scrum.png` | Скрам | ✅ |
| `bg_act3_cafe.png` | Кафе | ✅ |
| `bg_act3_glitch.png` | Сброс | ✅ |
| `bg_hr_shop.png` | Магазин HR | ✅ |
| `bg_event_riot.png` | Бунт | ✅ |
| `bg_event_kpi.png` | KPI | ✅ |

### P1 — ~~сильно желательно~~ ✅ готово

| Файл | Сцена | Статус |
|------|-------|--------|
| `bg_act2_guild_warriors.png` | Аудит воинов | ✅ |
| `bg_act2_guild_mages.png` | Баг магов | ✅ |
| `bg_act2_guild_thieves.png` | Питч воров | ✅ |
| `bg_act2_lawyer.png` | Юрист в дупле | ✅ |
| `bg_act2_swamp_lord.png` | Лорд Откат | ✅ |
| `bg_act2_temple.png` | Храм Патча 1.0 | ✅ |
| `bg_act3_boardroom.png` | Success / burnout / IPO | ✅ |

### P2 — опционально (ещё не сделано)
| Файл | Сцена | Сейчас |
|------|-------|--------|
| `bg_ending_debt.png` | Банкротство | `bg_act2_city` |
| `bg_ending_soul.png` | Подписка навсегда | `bg_act3_cave` |
|------|-------|--------|
| `bg_random_rtx.png` | Рандом RTX | forest |
| `bg_random_rain.png` | Налог на дождь | city |
| `bg_event_microloans.png` | Коллектор | dig |
| `bg_event_cringe_king.png` | Король Кринжа | arena |
| `bg_hub_duck.png` | Утка-кликер | guilds |
| Арена R1/R2/R3 | 3 врага | один `bg_act2_arena` — **OK** (одна локация, разные карточки врагов) |

### Промпты P0 (генерить в `backgrounds/`, 16:9)

### `bg_act2_forge.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed underground forge alley: huge orc smith hammering a glowing motherboard anvil, sparks, blue electrical tape, muddy cobbles, satirical sysadmin forge, warm forge light, flat colors, clean ink outlines, whimsical, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act2_tinder.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed cramped matchmaker hut interior: old witch-grandma with birch-bark portrait cards floating, candlelight, curtains, dating-app satire medieval, cozy cluttered room, flat colors, clean ink outlines, whimsical, NO text, NO UI, NO letters, NO watermark.
```

### `bg_act2_tavern.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed medieval tavern Ctrl+Ale: wooden bar, burnt-out knights drinking ale, chalkboard wifi joke as scribble shapes only, warm amber light, burnout satire, flat colors, clean ink outlines, whimsical, NO readable text, NO UI, NO watermark.
```

### `bg_act3_ball.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed royal ballroom before dragon quest: dancing nobles, snack tables with ridiculous price tags as abstract symbols, chandelier, throne with unused lightning-socket joke in background corner, festive but corporate, flat colors, clean ink outlines, whimsical, NO readable text, NO UI, NO watermark.
```

### `bg_act3_scrum.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed cave mouth standup meeting: sticky parchment task board, knights in circle, mountain cave entrance behind, late day light, agile medieval satire, flat colors, clean ink outlines, whimsical, NO readable text, NO UI, NO watermark.
```

### `bg_act3_cafe.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed cozy dragon cafe interior: small round tables, teacups, friendly small dragon barista wiping cups with tail, warm lamps, NOT a treasure hoard cave, peaceful satire, flat colors, clean ink outlines, whimsical, NO text, NO UI, NO watermark.
```

### `bg_act3_glitch.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed civilization reset glitch: broken medieval town dissolving into pixel holes and void cracks, surreal sky, floating UI-shapes without letters, apocalyptic whimsical satire, flat colors, clean ink outlines, NO readable text, NO UI chrome, NO watermark.
```

### `bg_hr_shop.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed heavenly HR legacy shop: white cloud office cubicles, glass display cases with cursed relics (stone glove, hourglass, jester mask), angel clerk silhouette, soft holy fluorescent light, flat colors, clean ink outlines, whimsical, NO readable text, NO UI, NO watermark.
```

### `bg_event_riot.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed peasant revolt at castle gates: pitchforks, angry crowd, hero lifted on shoulders, capital castle gates, daytime chaos satire, flat colors, clean ink outlines, whimsical, NO text, NO UI, NO watermark.
```

### `bg_event_kpi.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed KPI deadline scene: giant owl courier with HR folder, hero on open world map path, ominous hourglass sky, corporate doom satire, flat colors, clean ink outlines, whimsical, NO readable text, NO UI, NO watermark.
```

### Промпты P1 (кратко)

### `bg_act2_guild_warriors.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed sweaty warrior guild hall: armor racks, deadline banners as abstract shapes, sweat towels, training dummies, flat colors, clean outlines, whimsical, NO text, NO UI, NO watermark.
```

### `bg_act2_guild_mages.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed mage tower interior sparking with bug-like magic sparks, crystal balls, potion mugs, coding-magic satire, flat colors, clean outlines, whimsical, NO text, NO UI, NO watermark.
```

### `bg_act2_guild_thieves.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed thieves crypt startup: glowing radish NFT vibe, hooded hackers, candlelit vault, crypto satire medieval, flat colors, clean outlines, whimsical, NO text, NO UI, NO watermark.
```

### `bg_act2_lawyer.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed hollow under VPN-pine: owl lawyer in glasses at tiny desk with red lawsuit folders, forest light through roots, flat colors, clean outlines, whimsical, NO text, NO UI, NO watermark.
```

### `bg_act2_swamp_lord.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed swamp throne of Lord Rollback: muddy bog, broken swing 404 vibe, update frogs, flat colors, clean outlines, whimsical, NO text, NO UI, NO watermark.
```

### `bg_act2_temple.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed swamp patch temple altar with glowing version stone 1.0 vibe as abstract rune slab, pilgrims, misty bog, flat colors, clean outlines, whimsical, NO readable text, NO UI, NO watermark.
```

### `bg_act3_boardroom.png`
```
Hand-drawn 2D cartoon game background, Choice of Life Middle Ages style. Full-bleed endless corporate meeting hall: long table, charts as abstract shapes, exhausted nobles, success burnout satire, flat colors, clean outlines, whimsical, NO text, NO UI, NO watermark.
```

### Дыра Акта 1 (добить заодно)
### `card_kids_sandbox_result.png` — исход «к детям в песочнице»
```
Hand-drawn 2D cartoon choice card BACK RESULT (outcome), Choice of Life style. Square: kids finished manure castle together OR arguing after monopoly of toy shovels, muddy playground outcome, flat colors, clean outlines, whimsical medieval, NO text, NO UI.
```

---

## Акт 3 — карточки (промпты; файлы пока reuse Акта 0–2)

> Генерить в `cards/card_a3_*.png` + `_result`, затем заменить пути в `act3_beats.gd`.

### `card_a3_ball.png` — бал / двор
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: medieval royal ball with inflation snack prices vibe, nobles, hero entering hall, action of arriving, flat colors, clean outlines, whimsical satire, NO text, NO UI.
```

### `card_a3_countess.png` — Графиня CTR
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: elegant countess with A/B clipboard birch bark measuring hero with sharp eyes, flirt-corporate pose, flat colors, clean outlines, whimsical, NO readable text, NO UI.
```

### `card_a3_venture.png` — Барон Венчур
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: fat baron offering gold bag for soul share contract, greedy investor pose, flat colors, clean outlines, whimsical medieval satire, NO text, NO UI.
```

### `card_a3_dragon_coach.png` — коуч-сессия с драконом
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: depressed dragon on pizza boxes listening to hero coaching with pointer stick, therapy-in-cave, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_a3_startup.png` — IPO пещеры
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: dragon in chain necktie presenting pitch deck cave IPO, hero and venture baron clapping, flat colors, clean outlines, whimsical satire, NO readable text, NO UI.
```

### `card_a3_relocate.png` — релокация с драконом
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: hero and small dragon sneaking into relocant forest hammocks, escape pose, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_a3_ctrl_ale.png` — таверна Ctrl+Ale
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: cozy burnout tavern with ale mugs and Wi-Fi joke vibe, tired hero at bar, flat colors, clean outlines, whimsical medieval satire, NO readable text, NO UI.
```

### `card_a3_duck.png` — утка-кликер
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: rubber duck on city square with clicker addiction pose, hero tapping it frantically, flat colors, clean outlines, whimsical, NO text, NO UI.
```

### `card_a3_cat_pm.png` — кот-менеджер
```
Hand-drawn 2D cartoon choice card FRONT (action only, NOT outcome), Choice of Life style. Square: cat in tiny necktie holding kanban birch scroll, judgmental manager stare, flat colors, clean outlines, whimsical satire, NO text, NO UI.
```

---

## HUD-иконки статов (1:1) — `icons/`

Папка: `game/assets/art/icons/`. Подключены в `stats_hud.tscn` (28×28).

| Файл | Стат |
|------|------|
| `icon_health.png` | ❤️ Health |
| `icon_mental.png` | 🧠 Mental |
| `icon_gold.png` | 💰 Gold |
| `icon_crown.png` | 👑 Crown |
| `icon_inquisition.png` | ⛪ Inquisition |
| `icon_people.png` | 🧑‍🌾 People |
| `icon_cringe.png` | 😳 Cringe |

### Шаблон
```
Game UI icon, Choice of Life medieval cartoon style. [СИМВОЛ], clean flat colors, thick outline, centered on plain cream parchment background, simple HUD asset, NO text.
```

---

*Привязка файлов к сценам: [`README.md`](./README.md)*
