extends RefCounted
class_name StubStory
## Канон MD → биты.
## kind: "narrative" | "result" (по умолчанию result)
## result = текст НА РУБАШКЕ карточки
## aside = короткий контекст сверху (НЕ дублирует result)

const BG_BIRTH := "res://assets/art/backgrounds/bg_act1_birth.png"
const BG_FIRST_WORD := "res://assets/art/backgrounds/bg_act1_first_word.png"
const BG_SANDBOX := "res://assets/art/backgrounds/bg_act1_sandbox.png"
const BG_DIG := "res://assets/art/backgrounds/bg_act1_dig.png"
const BG_FAIR := "res://assets/art/backgrounds/bg_act1_fair.png"
const BG_BOOTCAMP := "res://assets/art/backgrounds/bg_act1_bootcamp.png"
const BG_WINDMILL := "res://assets/art/backgrounds/bg_act1_windmill.png"
const BG_MILITARY := "res://assets/art/backgrounds/bg_act1_military.png"
const BG_PHONE_CURSE := "res://assets/art/backgrounds/bg_act1_phone_curse.png"
const CARD := "res://assets/art/cards/"
const Act0BeatsScript = preload("res://resources/story/act0_beats.gd")
const Act1RoadBeatsScript = preload("res://resources/story/act1_road.gd")
const Act2BeatsScript = preload("res://resources/story/act2_beats.gd")
const Act2SidesScript = preload("res://resources/story/act2_sides.gd")
const Act3BeatsScript = preload("res://resources/story/act3_beats.gd")
const InfogypsyBeatsScript = preload("res://resources/story/infogypsy_beats.gd")
const ExtremeEventsScript = preload("res://resources/story/extreme_events.gd")
const RandomEncountersScript = preload("res://resources/story/random_encounters.gd")
const HeavenlyHRScript = preload("res://resources/story/heavenly_hr.gd")
const EndingBeatsScript = preload("res://resources/story/endings.gd")
const HubBigDataScript = preload("res://resources/story/hub_big_data.gd")
const ForgeServiceScript = preload("res://resources/story/forge_service.gd")


static func get_beats(timeline_id: StringName) -> Array:
	match timeline_id:
		&"act0_tutorial":
			return Act0BeatsScript.beats()
		&"act1_01_birth":
			return _act1_chain()
		&"act1_road_stub":
			return Act1RoadBeatsScript.beats()
		&"act2_city_stub":
			return Act2BeatsScript.beats()
		&"side_forest_stub":
			return Act2SidesScript.forest()
		&"side_swamp_stub":
			return Act2SidesScript.swamp()
		&"random_infogypsy":
			return InfogypsyBeatsScript.map_ambush()
		&"random_rtx", &"random_rain_tax", &"random_plantain_scam", &"random_api_fatal":
			return RandomEncountersScript.get_beats(timeline_id)
		&"event_microloans":
			return ExtremeEventsScript.microloans()
		&"event_people_riot":
			return ExtremeEventsScript.people_riot()
		&"event_people_cancel":
			return ExtremeEventsScript.people_cancel()
		&"event_inq_wrath":
			return ExtremeEventsScript.inq_wrath()
		&"event_inq_monk":
			return ExtremeEventsScript.inq_monk()
		&"event_crown_execute":
			return ExtremeEventsScript.crown_execute()
		&"event_crown_exile":
			return ExtremeEventsScript.crown_exile()
		&"event_kpi_deadline":
			return ExtremeEventsScript.kpi_deadline()
		&"event_cringe_king":
			return ExtremeEventsScript.cringe_king()
		&"heavenly_hr":
			return HeavenlyHRScript.interview()
		&"act3_castle_stub":
			return Act3BeatsScript.castle()
		&"act3_dragon_stub":
			return Act3BeatsScript.dragon()
		&"ending_ctrl_ale":
			return EndingBeatsScript.ctrl_ale()
		&"ending_bankruptcy":
			return EndingBeatsScript.bankruptcy()
		&"ending_soul_sub":
			return EndingBeatsScript.soul_sub()
		&"hub_big_data":
			return HubBigDataScript.hub()
		&"forge_service":
			return ForgeServiceScript.beats()
		_:
			return _generic(String(timeline_id))


static func _birth_text() -> String:
	if GameState.run_index >= 2:
		return "Вы успешно скомпилировались в утробе. Акушерка закатывает глаза: «Опять ты?! Сколько можно релизиться заново?» Ждёт вашего первого лога. Снова."
	return "Вы успешно скомпилировались в утробе. Акушерка ждёт вашего первого лога."


static func _act1_chain() -> Array:
	return [
		{
			"id": "birth",
			"bg": BG_BIRTH,
			"speaker": "Акушерка",
			"text": _birth_text(),
			"choices": [
				{
					"label": "«Где мой смузи?!»",
					"art": CARD + "card_smoothie.png",
					"aside": "В избе пахнет крапивой и чужим разочарованием.",
					"result": "Акушерка вздыхает, наливает в берестяной стаканчик овсяный раф с крапивой и подносит берестяной QR-код для чаевых. Добро пожаловать в суровый мир, миллениал.",
					"effects": {"health": -1, "mental": -2, "people": -1, "perk": "millennial", "item": "smoothie"},
					"next": "first_word",
				},
				{
					"label": "Принять EULA жизни молча",
					"art": CARD + "card_eula.png",
					"aside": "Свиток шуршит. Никто не читает условия — и это норма.",
					"result": "Ты даже не прочитал EULA. Господь любит послушных юзеров и начисляет кэшбек. (А Сын Маминой Подруги подписал EULA ещё в утробе и уже получил статуэтку «Юзер Года»).",
					"effects": {"gold": 10, "crown": 2, "perk": "obedient"},
					"next": "first_word",
				},
				{
					"label": "Скипнуть катсцену",
					"art": CARD + "card_skip.png",
					"aside": "Кнопка Skip мигает… и не работает. Как всегда.",
					"result": "Жизнь нельзя скипнуть, приятель. Ты так напрягся и зажмурился, пытаясь пропустить интро, что пукнул и обделался прямо в колыбели. Акушерка аплодирует первому краш-репорту.",
					"effects": {"health": -2, "mental": -1},
					"next": "first_word",
				},
			],
		},
		{
			"id": "first_word",
			"bg": BG_FIRST_WORD,
			"speaker": "Родители",
			"text": "Родители склонились над колыбелью. «Скажи Ма-ма! Скажи Па-па!»",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] Сказать что-то обычное",
					"art": CARD + "card_agu.png",
					"speaker": "Вы",
					"branch_text": "Вы открываете рот, чтобы сказать «Агу».",
					"choices": [
						{
							"label": "Сказать «Агу»",
							"art": CARD + "card_agu.png",
							"aside": "Классика жанра. Родители ждут чуда, а получают дефолт.",
							"result": "Как скучно. Родители рады, но ты чувствуешь себя банальностью.",
							"effects": {"people": 3, "mental": -1},
							"next": "bridge_sandbox",
						},
						{
							"label": "Заплакать и потребовать донат",
							"art": CARD + "card_donate_cry.png",
							"aside": "Монетизация стартует с колыбели. Инвесторы были бы горды.",
							"result": "Отец умиляется предпринимательской жилке и кладёт в колыбель медный грош.",
							"effects": {"gold": 5, "mental": 1},
							"next": "bridge_sandbox",
						},
						{
							"label": "Прогугукать тему Windows",
							"art": CARD + "card_podcast.png",
							"aside": "Из колыбели раздаётся знакомый полифонический запуск системы.",
							"result": "Родители замирают в священном трепете. Отец крестится, а мать решает, что в избу вошла чистая магия.",
							"effects": {"mental": 2, "people": 2, "inquisition": -1},
							"next": "bridge_sandbox",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Сказать что-то умное",
					"art": CARD + "card_blockchain.png",
					"speaker": "Вы",
					"branch_text": "Вы набираете побольше воздуха в лёгкие…",
					"choices": [
						{
							"label": "Сказать «Блокчейн»",
							"art": CARD + "card_blockchain.png",
							"aside": "В воздухе повисло слово, которого ещё не изобрели.",
							"result": "Мать падает в обморок, а отец решает, что ты вырастешь сборщиком податей.",
							"effects": {"crown": 3, "people": -3},
							"next": "bridge_sandbox",
						},
						{
							"label": "«Птицы — это дроны Короля!»",
							"art": CARD + "card_birds_drones.png",
							"aside": "За окном чирикает что-то подозрительно синхронное.",
							"result": "Родители в ужасе крестятся. Мысль плотно засела в голове.",
							"effects": {"cringe": 1, "inquisition": -2, "pen": "bird_drones", "perk": "freak"},
							"next": "bridge_sandbox",
						},
						{
							"label": "«Агу-с, господа. Согласно теореме…»",
							"art": CARD + "card_podcast.png",
							"aside": "Ты откашливаешься и толкаешь вступительную речь к докторской диссертации.",
							"result": "Родители в шоке вызывают инквизитора. Инквизитор внимательно слушает, конспектирует и ставит тебе 5 за доклад.",
							"effects": {"inquisition": 3, "crown": 2, "mental": 1},
							"next": "bridge_sandbox",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Сохранить гордое молчание",
					"art": CARD + "card_ignore_sleep.png",
					"speaker": "Вы",
					"branch_text": "Вы гордо молчите, скрестив маленькие ручки на груди…",
					"choices": [
						{
							"label": "Посмотреть на них как на джунов",
							"art": CARD + "card_ignore_sleep.png",
							"aside": "Родители засуетились. Кажется, они не прошли твой собеседовательный отбор.",
							"result": "Отец чувствует себя некомфортно и уходит перечитывать документацию по воспитанию.",
							"effects": {"mental": 2, "people": -2, "perk": "relocant"},
							"next": "bridge_sandbox",
						},
						{
							"label": "Молча выдать им баг-репорт",
							"art": CARD + "card_act0_confused.png",
							"aside": "Твой взгляд выражает глубокое разочарование в архитектуре этой семьи.",
							"result": "Мать решает, что ребёнок растёт слишком системным, и присваивает тебе позывной Сэр Баг.",
							"effects": {"crown": 2},
							"next": "bridge_sandbox",
						},
					],
				},
			],
		},
		# 1.2 — Мостик: Детство
		{
			"id": "bridge_sandbox",
			"bg": BG_SANDBOX,
			"speaker": "Рассказчик",
			"text": "Шли годы. Вы подросли, научились уверенно ходить на двух ногах и освоили деревенский огород. Наступило время первых серьезных социальных связей — в песочнице у избы...",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] «Выйти во двор к детям»",
					"art": CARD + "card_kids_sandbox.png",
					"speaker": "Вы",
					"branch_text": "Вы открываете низкую резную дверь избы и ступаете на солнечный двор...",
					"choices": [
						{
							"label": "Подойти к песочнице",
							"art": CARD + "card_kids_sandbox.png",
							"aside": "Песочница гудит, как утренний коворкинг.",
							"result": "Вы встаёте посреди песочницы.",
							"next": "sandbox",
						},
					],
				},
			],
		},
		{
			"id": "sandbox",
			"bg": BG_SANDBOX,
			"speaker": "Двор",
			"text": "Тебя выпустили во двор. Старший брат зовёт играть в рыцарей, а крестьянские дети лепят замок. В стороне Сын Маминой Подруги (Сэр Успешный) уже строит франшизу из песка.",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] Играть с братом",
					"art": CARD + "card_play_dragon.png",
					"speaker": "Старший брат",
					"branch_text": "Брат даёт тебе палку: «Ты будешь драконом, а я буду тебя бить!»",
					"choices": [
						{
							"label": "Терпеливо отыгрывать дракона",
							"art": CARD + "card_play_dragon.png",
							"aside": "Тимбилдинг по-деревенски: один рычит, другой бьёт.",
							"result": "Ты послушно рычишь. Сэр Успешный смотрит с жалостью и продаёт твою палку за 2 золотых.",
							"effects": {"health": -2, "mental": -1, "crown": 2},
							"next": "bridge_dig",
						},
						{
							"label": "Ударить брата палкой в ответ!",
							"art": CARD + "card_hit_brother.png",
							"aside": "Ты ломаешь баланс ролей. Босс-файт начался раньше патча.",
							"result": "Брат ревёт, тебя в угол. Сэр Успешный одобрительно кивает бунту.",
							"effects": {"health": -1, "mental": 3, "crown": -2},
							"next": "bridge_dig",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Играть одному",
					"art": CARD + "card_ignore_sleep.png",
					"speaker": "Вы",
					"branch_text": "Ты уходишь в дальний угол песочницы. Соло-разработка — твой сознательный выбор.",
					"choices": [
						{
							"label": "Пет-проект из грязи и палок",
							"art": CARD + "card_kids_sandbox.png",
							"aside": "Соло-проект в песочнице. Архитектура держится на соплях и надежде.",
							"result": "Проект развалился от дождя. Сын Маминой Подруги выпускает про тебя видео 'Почему соло-дев обречён' и собирает 500 лайков.",
							"effects": {"mental": 3, "health": -1, "cringe": 1},
							"next": "bridge_dig",
						},
						{
							"label": "Писать свой движок с нуля",
							"art": CARD + "card_matrix.png",
							"aside": "Зачем использовать чужой песок, если можно выкопать свой с нуля?",
							"result": "Твой движок рендерит ровно одну песчинку. Сын Маминой Подруги смотрит свысока и продаёт тебе готовый фреймворк из глины.",
							"effects": {"mental": 2, "cringe": 1},
							"next": "bridge_dig",
						},
						{
							"label": "Искать баг в текстуре лужи",
							"art": CARD + "card_act0_confused.png",
							"aside": "Ты час тычешь пальцем в воду, пытаясь провалиться сквозь текстуру мира.",
							"result": "Нашёл 2 медных гроша в луже! Сын Маминой Подруги тут же объявляет лужу 'Финтех-платформой' и берёт 20% комиссии.",
							"effects": {"gold": 2, "health": -1},
							"next": "bridge_dig",
						},
						{
							"label": "Запитчить проект Сэру Успешному",
							"art": CARD + "card_podcast.png",
							"aside": "Первый стартап-питч прямо над куличом из песка.",
							"result": "Сын Маминой Подруги критикует твои архитектурные грехи, но выкупает проект за 5 золотых, переименовывает в 'SandBox AI' и выходит на IPO.",
							"effects": {"gold": 5, "crown": 2, "mental": -1},
							"next": "bridge_dig",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] К крестьянским детям",
					"art": CARD + "card_kids_sandbox.png",
					"speaker": "Дети деревни",
					"branch_text": "Дети сосредоточенно лепят из грязи башни. Чем займёшься?",
					"choices": [
						{
							"label": "Помочь строить замок",
							"art": CARD + "card_help_castle.png",
							"aside": "Грязь под ногтями — это тоже networking.",
							"result": "Отличный тимплеер. Сэр Успешный объявляет замок нерентабельным.",
							"effects": {"people": 4},
							"next": "bridge_dig",
						},
						{
							"label": "Построить коворкинг из навоза",
							"art": CARD + "card_coworking.png",
							"aside": "Стартап в песочнице. Pitch deck пахнет.",
							"result": "Дети не оценили стартап и побили тебя лопатками. Зато идеалы целы.",
							"effects": {"health": -2, "mental": 3, "people": -2},
							"next": "bridge_dig",
						},
						{
							"label": "Монополия на лопатки",
							"art": CARD + "card_monopoly.png",
							"aside": "Рынок игрушек захвачен за три минуты.",
							"result": "Дети кусают за ноги. Сэр Успешный пишет кейс в блог. Загон: птицы = дроны.",
							"effects": {"health": -1, "crown": 4, "people": -4, "cringe": 1, "pen": "bird_drones"},
							"next": "bridge_dig",
						},
					],
				},
			],
		},
		# 1.3 — Мостик: Первый Труд
		{
			"id": "bridge_dig",
			"bg": BG_DIG,
			"speaker": "Рассказчик",
			"text": "Детство пролетело мгновенно, как один бессмысленный дебаг-сеанс. Вам исполнилось 10 лет. Беззаботные игры в песочнице сменились суровым трудовым воспитанием на деревенском огороде...",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] «Вздохнуть и взять лопату»",
					"art": CARD + "card_dig_silent.png",
					"speaker": "Вы",
					"branch_text": "Отец ждёт вас у забора с лопатой в руках...",
					"choices": [
						{
							"label": "Подойти к отцу",
							"art": CARD + "card_dig_silent.png",
							"aside": "Забор длинный, огород бесконечный.",
							"result": "Отец протягивает тяжелую деревянную лопату.",
							"next": "dig",
						},
					],
				},
			],
		},
		{
			"id": "dig",
			"bg": BG_DIG,
			"speaker": "Отец",
			"text": "Тебе 10 лет. Отец вручает лопату: «Пора работать, сынок. Копай от забора и до обеда».",
			"choices": [
				{
					"label": "Копать молча",
					"art": CARD + "card_dig_silent.png",
					"aside": "Солнце печёт. Лопата тяжёлая. Дедлайн — обед.",
					"result": "Ты копаешь. Спина болит. Мимо на карете с золотыми колёсами проезжает Сын Маминой Подруги: «Всё копаешь, джун? А я уже на Бали-деревне!»",
					"effects": {"health": -1, "mental": -2, "people": 3},
					"next": "father_send_fair",
				},
				{
					"label": "Привязать лопату к свинье",
					"art": CARD + "card_pig_automation.png",
					"aside": "Автоматизация 1.0: живой движок и ноль документации.",
					"result": "Свинья снесла забор. Тебя выпороли, но Инквизиция заинтересовалась умом.",
					"effects": {"health": -2, "inquisition": 3},
					"next": "father_send_fair",
				},
				{
					"label": "Делегировать брату за леденец",
					"art": CARD + "card_delegate_brother.png",
					"aside": "Менеджмент младшего звена. KPI — леденец.",
					"result": "Классический аутсорс! Брат счастлив сусальному леденцу и копает за тебя до ночи. Твои руки чистые, а ты уже чувствуешь себя настоящим тимлидом.",
					"effects": {"gold": -5, "mental": 3, "crown": 2},
					"allow_debt": true,
					"next": "father_send_fair",
				},
			],
		},
		{
			"id": "father_send_fair",
			"bg": BG_DIG,
			"speaker": "Отец",
			"text": "Отец вытирает пот со лба и оглядывает вскопанное поле: «Ладно, с таской справились. На, держи 10 монет бюджета. Сходи на ярмарку, купи соли и репы. И смотри, не спусти деньги на всякие глупости!»",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] «Взять монеты и пойти на ярмарку»",
					"art": CARD + "card_act0_loot.png",
					"speaker": "Вы",
					"branch_text": "Ты звенящими монетами в кармане шагаешь в центр деревни, где гремит ярмарка.",
					"choices": [
						{
							"label": "Отправиться на торговую площадь",
							"art": CARD + "card_act0_loot.png",
							"aside": "В воздухе пахнет жареными поросятами, элем и свежим маркетингом.",
							"result": "Ты приходишь на ярмарку. В центре площади яркий караван купца.",
							"effects": {"gold": 10},
							"next": "fair",
						},
					],
				},
			],
		},
		{
			"id": "fair",
			"bg": BG_FAIR,
			"speaker": "Купец-инфоцыган",
			"text": "В деревню приехал караван. Хитрый купец раскладывает странные товары на бочке. «Подходи, налетай! Инновации из-за моря!»",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] Посмотреть на «Деревянный Смартфон»",
					"art": CARD + "card_wooden_phone.png",
					"speaker": "Купец",
					"branch_text": "Купец шепчет: «Это флагман! Без яблока на задней крышке, зато не разряжается. Всего 10 золота.»",
					"choices": [
						{
							"label": "Купить (10 золота)",
							"art": CARD + "card_wooden_phone.png",
							"aside": "Последние сбережения уходят в кору.",
							"result": "Кусок коры твой. Чувствуешь себя элитой. Купец: «Ещё увидимся на тракте…»",
							"effects": {"gold": -10, "item": "wooden_phone"},
							"allow_debt": true,
							"flag": "met_fair_infogypsy",
							"next": "bridge_bootcamp",
						},
						{
							"kind": "return",
							"label": "Подождать следующую модель",
							"art": CARD + "card_skip.png",
							"next": "fair",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Спросить про странное металлическое ведро",
					"art": CARD + "card_foil_hat.png",
					"speaker": "Купец",
					"branch_text": "Купец надевает ведро на голову: «Это „Шапочка из фольги“. Экранирует от магии, налогов и здравого смысла. Отдам за 5 золота.»",
					"choices": [
						{
							"label": "Заплатить 5 золота",
							"art": CARD + "card_foil_hat.png",
							"aside": "Мир тускнеет. Мозг в безопасности.",
							"result": "Шапочка твоя. Народ косится, но 5G уже не страшен.",
							"effects": {"gold": -5, "mental": 4, "people": -3, "item": "foil_hat", "pen": "5g"},
							"allow_debt": true,
							"flag": "met_fair_infogypsy",
							"next": "bridge_bootcamp",
						},
						{
							"label": "Украсть шапочку, пока отвернулся!",
							"art": CARD + "card_steal_gem.png",
							"aside": "Собаки купца уже в стартовых колодках.",
							"result": "Ведро твоё! Пятки искусаны, но лут на голове.",
							"effects": {"health": -2, "inquisition": -3, "mental": 4, "item": "foil_hat", "pen": "5g"},
							"flag": "met_fair_infogypsy",
							"next": "bridge_bootcamp",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Пойти в «Бакалею» за едой",
					"art": CARD + "card_act0_loot.png",
					"speaker": "Бакалейщик",
					"branch_text": "В лавке пахнет сушеной рыбой, мочеными яблоками и агрессивным монетизационным дизайном.",
					"choices": [
						{
							"label": "Купить соль и репу по списку отца (5 золота)",
							"art": CARD + "card_act0_loot.png",
							"aside": "Отцовский наказ выполнен, а 5 золота еще осталось на карманные расходы.",
							"result": "Ты берешь мешок соли и связку репы. Отец будет гордиться твоим compliance!",
							"effects": {"gold": -5, "respect": 1, "item": "turnip_and_salt"},
							"allow_debt": false,
							"flag": "met_fair_infogypsy",
							"next": "bridge_bootcamp",
						},
						{
							"label": "Купить «Берестяной Battle Pass» вместо еды (8 золота)",
							"art": CARD + "card_useless_pass.png",
							"aside": "Сезон 1: Деревенская Жатва! 100 уровней наград, а репа — это мейнстрим.",
							"result": "Ты отдаешь 8 золота за кусок бересты с надписью «Season Pass». Батя будет в шоке, зато у тебя теперь VIP-статус на деревне!",
							"effects": {"gold": -8, "cringe": 1, "item": "useless_pass"},
							"allow_debt": true,
							"flag": "met_fair_infogypsy",
							"next": "bridge_bootcamp",
						},
					],
				},
			],
		},
		# 1.5 — Мостик: Школа IT-Ремесла
		{
			"id": "bridge_bootcamp",
			"bg": BG_BOOTCAMP,
			"speaker": "Рассказчик",
			"text": "Окончив дела на ярмарке, вы вернулись домой. Отец оглядел ваши приобретения и решил, что вам пора получить полноценное системное образование. Так вы оказались у дубовых ворот местной церковно-приходской Школы IT-Ремесла...",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] «Толкнуть тяжелую дверь школы»",
					"art": CARD + "card_pentagram.png",
					"speaker": "Вы",
					"branch_text": "Из классов доносится хор учеников, зазубривающих синтаксис латыни и древнего ассемблера...",
					"choices": [
						{
							"label": "Зайти в класс",
							"art": CARD + "card_pentagram.png",
							"aside": "Запах мела, бересты и детского выгорания.",
							"result": "Монах-сеньор грозно смотрит на вас поверх деревянных очков.",
							"next": "bootcamp",
						},
					],
				},
			],
		},
		{
			"id": "bootcamp",
			"bg": BG_BOOTCAMP,
			"speaker": "Монах-сеньор",
			"text": "Монах-сеньор заставляет писать «Hello, World» вилами на земле. Завтра экзамен по латыни.",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] Сдать честно",
					"art": CARD + "card_pentagram.png",
					"speaker": "Экзамен",
					"branch_text": "Вы берёте вилы и начинаете чертить буквы. Монах смотрит пристально.",
					"choices": [
						{
							"label": "Написать код с ошибкой",
							"art": CARD + "card_pentagram.png",
							"aside": "Вилы чертят лишний символ. Компилятор недоволен.",
							"result": "Синтаксическая ошибка! Ты случайно нарисовал пентаграмму. Демон украл твой обед.",
							"effects": {"health": -2, "inquisition": -3},
							"next": "bridge_windmill",
						},
						{
							"label": "Взятка монаху (5 золота)",
							"art": CARD + "card_bribe_puppies.png",
							"aside": "Коррупция пахнет щенячьим кормом и индульгенциями.",
							"result": "Монах ставит «автомат». Коррупция спасёт мир!",
							"effects": {"gold": -5, "inquisition": -4, "crown": 2},
							"allow_debt": true,
							"next": "bridge_windmill",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Схитрить",
					"art": CARD + "card_cheat.png",
					"speaker": "Экзамен",
					"branch_text": "Экзамен — симуляция. Если взломать систему, можно не учиться!",
					"choices": [
						{
							"label": "Списать у соседа",
							"art": CARD + "card_cheat.png",
							"aside": "Сосед пишет уверенно. Ты тоже — почти.",
							"result": "Ты получил диплом, но ни черта не знаешь. Сын Маминой Подруги сдал экзамен до его начала и уже преподаёт на вашей кафедре.",
							"effects": {"mental": 2, "people": 1},
							"next": "bridge_windmill",
						},
						{
							"label": "Мир — это Матрица!",
							"art": CARD + "card_matrix.png",
							"aside": "Ложки нет. Указки у монаха — есть.",
							"result": "Ты кричишь, что ложки не существует. Монах бьёт указкой, но ты начинаешь видеть код мира.",
							"effects": {"cringe": 1, "health": -1, "pen": "matrix_lite"},
							"next": "bridge_windmill",
						},
						{
							"label": "[Скрытый] Нагуглить ответы",
							"art": CARD + "card_phone_google.png",
							"aside": "Палец водит по коре. Связь 0G, но вера сильна.",
							"result": "Монах думает, что это скрижали, и ставит пятёрку!",
							"effects": {"inquisition": 4, "mental": 3},
							"require_item": "wooden_phone",
							"next": "bridge_windmill",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Отчислиться и запустить стартап",
					"art": CARD + "card_coworking.png",
					"speaker": "Джун-Фаундер",
					"branch_text": "Зачем 4 года учить латынь, когда можно прямо сейчас задеплоить стартап в сарае!",
					"choices": [
						{
							"label": "Сделать AI-модель предсказания урожая репы",
							"art": CARD + "card_blockchain.png",
							"aside": "Инвесторы-крестьяне слушают про инновации с открытыми ртами.",
							"result": "Ты поднял 10 золотых раунда Pre-Seed! Правда, твоя AI-модель предсказывает только дождь, который и так идёт.",
							"effects": {"gold": 10, "mental": 3, "cringe": 1},
							"next": "bridge_windmill",
						},
						{
							"label": "Нанять брата за леденец и делать кликеры",
							"art": CARD + "card_delegate_brother.png",
							"aside": "Геймдев из сарая — быстро, дёшево и сердито.",
							"result": "Брат нарисовал 50 уровней «Три в ряд с картошкой». Сын Маминой Подруги клонирует вашу игру за вечер и выходит на IPO.",
							"effects": {"gold": 5, "respect": 1, "people": 2},
							"next": "bridge_windmill",
						},
					],
				},
			],
		},
		# 1.6 — Мостик: 5G-Мельница
		{
			"id": "bridge_windmill",
			"bg": BG_WINDMILL,
			"speaker": "Рассказчик",
			"text": "Окончив учебу (или забросив её ради первого стартапа), вы отправились на край деревни. На холме со страшным гулом вращала крылья знаменитая 5G-Мельница, о которой ходили жуткие слухи...",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] «Подняться на холм к мельнице»",
					"art": CARD + "card_ddos_stick.png",
					"speaker": "Вы",
					"branch_text": "Вокруг мельницы уже собралась толпа испуганных крестьян во главе со старостой...",
					"choices": [
						{
							"label": "Подойти к толпе",
							"art": CARD + "card_ddos_stick.png",
							"aside": "В воздухе пахнет озоном и паникой.",
							"result": "Староста в панике машет руками.",
							"next": "windmill",
						},
					],
				},
			],
		},
		{
			"id": "windmill",
			"bg": BG_WINDMILL,
			"speaker": "Староста",
			"text": "Староста орёт, что новая мельница — вышка 5G, облучающая крестьян чипами.",
			"choices": [
				{
					"label": "DDoS палкой!",
					"art": CARD + "card_ddos_stick.png",
					"aside": "Ты бежишь к лопастям как к серверу без rate-limit.",
					"result": "Мельница даёт сдачи лопастью. Но народ считает тебя героем!",
					"effects": {"health": -4, "people": 5, "crown": -3},
					"next": "bridge_phone_curse",
				},
				{
					"label": "Записать разоблачающий подкаст на бересте",
					"art": CARD + "card_podcast.png",
					"aside": "Нацарапал 2-часовой спецвыпуск «Тайны 5G-мельниц и рептилоидный налог на репу».",
					"result": "Ты зачитываешь бересту на площади: «Мельница ворует мысли крестьян!» Народ в восторге ставит угольки-лайки, но Стража выписывает штраф 5 золота за «Нелицензированный подкастинг и дискредитацию Королевской Мельницы».",
					"effects": {"gold": -5, "mental": 3, "people": 2, "cringe": 1},
					"allow_debt": true,
					"next": "bridge_phone_curse",
				},
				{
					"label": "Игнорировать и спать",
					"art": CARD + "card_ignore_sleep.png",
					"aside": "Иногда лучший патч — выключить глаза.",
					"result": "Ты просыпаешься с чувством, что Билл Гейтс знает, где ты живёшь.",
					"effects": {"mental": -4},
					"next": "bridge_phone_curse",
				},
				{
					"label": "[Скрытый] Надеть фольгу!",
					"art": CARD + "card_foil_windmill.png",
					"aside": "Ты торжественно водружаешь чайник из фольги на голову. Внутри звенит эхо собственного величия.",
					"result": "Лопасти мельницы крутятся, «5G» бьёт по тебе… и рикошетит в соседскую свинью. Свинья начинает стримить. Крестьяне падают на колени: «Святой Анти-Чип!» Староста просит автограф на ведре.",
					"effects": {"mental": 5, "people": 3},
					"require_item": "foil_hat",
					"next": "bridge_phone_curse",
				},
			],
		},
		# 1.7 — Мостик: Вечерний Двор
		{
			"id": "bridge_phone_curse",
			"bg": BG_PHONE_CURSE,
			"speaker": "Рассказчик",
			"text": "Солнце клонилось к закату. Отойдя от мельницы, вы присели на завалинку у крапивы, чтобы перевести дух после дневных подвигов и поиграть с местными мальчишками в прятки...",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] «Залезть поглубже в крапиву»",
					"art": CARD + "card_phone_curse.png",
					"speaker": "Вы",
					"branch_text": "Вы затаили дыхание в густой крапиве. Шаги хулиганов затихают вдалеке...",
					"choices": [
						{
							"label": "Замереть и не дышать",
							"art": CARD + "card_phone_curse.png",
							"aside": "Засада удалась на 100%. Если только ничего не зазвонит...",
							"result": "Вы сидите в тишине.",
							"next": "phone_curse",
						},
					],
				},
			],
		},
		{
			"id": "phone_curse",
			"bg": BG_PHONE_CURSE,
			"speaker": "Прятки",
			"text": "Ты играешь с хулиганами в прятки. Идеально спрятался в крапиве. Они тебя никогда не найдут!",
			"require_item": "wooden_phone",
			"skip_to": "father_adulthood",
			"choices": [
				{
					"label": "Продолжить…",
					"art": CARD + "card_phone_curse.png",
					"aside": "В тишине кустов что-то пиликает. Это не сверчок.",
					"result": "«Смартфон» орёт (жук-короед). Хулиганы находят тебя и бьют крапивой. Страдай.",
					"effects": {"health": -3, "people": -2},
					"next": "father_adulthood",
				},
			],
		},
		{
			"id": "father_adulthood",
			"bg": BG_DIG,
			"speaker": "Отец",
			"text": "Тебе исполняется 18 лет. Отец сдерживает скупую слезу, откладывает лопату и кладёт руку тебе на плечо: «Ну вот ты и вырос, сынок. Пора из избы на площадь — там уже кого-то прислали из Столицы. Пойдём, узнаем, к какому труду ты годен.»",
			"choices": [
				{
					"label": "Пойти с отцом на площадь",
					"art": CARD + "card_act0_loot.png",
					"aside": "За огородом гудит толпа. Пахнет указом и страхом джунов.",
					"result": "Вы выходите из избы. На площади уже разобрали помост и красные знамёна Короны.",
					"effects": {},
					"next": "distribution_center",
				},
			],
		},
		# 1.8 — Распределительный Центр (персонализированный обзор юности)
		{
			"id": "distribution_center",
			"bg": BG_DIG,
			"speaker": "Табельный Чиновник",
			"dynamic_text": "youth_review",
			"text": "",
			"choices": [
				{
					"label": "Выйти на площадь к Военкому",
					"art": CARD + "card_serve_proudly.png",
					"aside": "Личное дело подшито. На площади уже зачитывают указ Короны.",
					"result": "Ты отходишь от столика Чиновника и ступаешь на брусчатку центральной площади...",
					"effects": {},
					"next": "military",
				},
			],
		},
		# 1.8b — Военкомат на площади (арт BG_MILITARY + все выборы карьеры/службы)
		{
			"id": "military",
			"bg": BG_MILITARY,
			"speaker": "Военком Короны",
			"text": "Площадь гудит. На помосте рыцарь в латах зачитывает берестяной указ: «Крестовый Поход 0.9b! Набор в галеру-стартап Его Величества. Печеньки, плоская структура, ноль бюрократии!» Нервные юноши мнутся у фонтана. Над площадью — замок и красные знамёна с короной.",
			"choices": [
				{
					"label": "Взятка по плоскостопию (10 золота)",
					"art": CARD + "card_bribe_flatfoot.png",
					"aside": "Золото звенит убедительнее любой справки.",
					"result": "Военком забирает золото и ставит штамп «Не годен к релизу». Свобода!",
					"effects": {"gold": -10, "mental": 2},
					"allow_debt": true,
					"unlock": "meme_tract",
					"next": "end",
				},
				{
					"label": "Сбежать в лес (релокация)",
					"art": CARD + "card_relocate_forest.png",
					"aside": "Горизонт манит. Клещи тоже.",
					"result": "Ты срываешься и уходишь в релоканты. Ночью холодно. Корона недовольна.",
					"effects": {"health": -3, "crown": -4, "perk": "relocant"},
					"unlock": "meme_tract",
					"next": "end",
				},
				{
					"label": "Гордо пойти служить!",
					"art": CARD + "card_serve_proudly.png",
					"aside": "Военком нахлобучивает тебе каску из бересты: «Добро пожаловать в семью!»",
					"result": "«Печеньками» оказались плесневелые сухари, а «ноль бюрократии» — когда ты копаешь окоп вилами, пока старшина орёт: «Где коммит?!» Сын Маминой Подруги служил в той же роте, но стал генералом за 2 недели. Ты выжил и получил перк Ветеран!",
					"effects": {"health": -5, "mental": -4, "crown": 5, "perk": "veteran"},
					"unlock": "meme_tract",
					"flag": "served_crusade",
					"next": "end",
				},
				{
					"label": "[Скрытый] IT-бронь",
					"art": CARD + "card_phone_it_defer.png",
					"aside": "Ты достаёшь кору. Военком бледнеет от технологий.",
					"result": "Оформляет отсрочку как ценному IT-специалисту!",
					"effects": {"crown": 5, "mental": 5},
					"require_item": "wooden_phone",
					"unlock": "meme_tract",
					"next": "end",
				},
				{
					"label": "[Скрытый] Надеть шапочку из фольги",
					"art": CARD + "card_foil_hat.png",
					"aside": "5G-облучение Короны! Военком в шоке.",
					"result": "Штамп: «Шизофреник. К строевой не годен».",
					"effects": {"mental": 3, "crown": -3},
					"require_item": "foil_hat",
					"unlock": "meme_tract",
					"next": "end",
				},
			],
		},
	]


static func _generic(id: String) -> Array:
	return [
		{
			"id": "generic",
			"speaker": "Рассказчик",
			"text": "Заглушка «%s»." % id,
			"choices": [
				{
					"label": "На карту",
					"aside": "Пока здесь пусто.",
					"result": "Ладно, пошли дальше.",
					"effects": {},
					"next": "end",
				},
			],
		},
	]


static func get_youth_review_text() -> String:
	var review := "Тебе исполнилось 18. На площадь Нижних Вай-Фаек приехал Военком Короны в латах — с берестяным указом и красным знаменем. Рядом развернули столик «Распределительного Центра»: чиновник поправляет пенсне и листает твоё личное дело.\n\n«Так-с… подвиги и косяки за юность.»\n\n"
	var items_found := 0

	if GameState.has_item(&"wooden_phone"):
		review += "• [Гаджеты] С младенчества залипаешь в деревянный смартфон. Обнаружена тяжелая IT-зависимость.\n"
		items_found += 1
	if GameState.has_item(&"foil_hat"):
		review += "• [Защита] Носишь на голове металлический чайник. Зафиксирована запущенная 5G-паранойя.\n"
		items_found += 1
	if GameState.has_item(&"turnip_and_salt"):
		review += "• [Воспитание] Принёс отцу репу и соль. Послушный исполнитель, идеальный винтик системы.\n"
		items_found += 1
	if GameState.has_item(&"useless_pass"):
		review += "• [Финансы] Спустил деньги на Берестяной Battle Pass. Жертва агрессивного маркетинга.\n"
		items_found += 1

	if items_found == 0:
		review += "• [Имущество] На руках ни копейки и ни одного гаджета. Гол как сокол.\n"

	review += "\n"
	if GameState.run_absurd_moments >= 2 or GameState.get_flag(&"goblin_narrator"):
		review += "• [Репутация] За юность накопилось много странных решений — %s.\n" % GameState.people_narrative_tone()
	else:
		review += "• [Репутация] В целом %s.\n" % GameState.people_narrative_tone()

	if GameState.crown >= 60 or GameState.crown <= 40:
		review += "• [Корона] %s.\n" % GameState.crown_narrative_tone()

	if GameState.gold >= 10:
		review += "• [Капитал] Баланс %d золота! Умеешь крутить монеты.\n" % GameState.gold
	elif GameState.gold < 0:
		review += "• [Долги] Баланс %d золота. Гоблины-коллекторы уже держат биту наготове.\n" % GameState.gold
	else:
		review += "• [Капитал] Наличных %d золота.\n" % GameState.gold

	if GameState.mental >= 8:
		review += "• [Интеллект] Мозги на месте (Менталочка %d/10). Способен к анализу и рефакторингу.\n" % GameState.mental
	elif GameState.mental <= 4:
		review += "• [Интеллект] Выгорание %d/10. Типичный миллениал еще до первого оффера.\n" % GameState.mental

	review += "\nВердикт: «Личное дело сформировано. Выбирай карьерный путь — пока Военком не заскучал на помосте!»"
	return review
