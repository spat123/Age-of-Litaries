extends RefCounted
class_name Act3Beats
## Акт 3–4 по канону act_3_dragon_choices.md

const BG_CASTLE := "res://assets/art/backgrounds/bg_act3_castle.png"
const BG_BALL := "res://assets/art/backgrounds/bg_act3_ball.png"
const BG_ROAD := "res://assets/art/backgrounds/bg_act3_road.png"
const BG_SCRUM := "res://assets/art/backgrounds/bg_act3_scrum.png"
const BG_CAVE := "res://assets/art/backgrounds/bg_act3_cave.png"
const BG_CAFE := "res://assets/art/backgrounds/bg_act3_cafe.png"
const BG_GLITCH := "res://assets/art/backgrounds/bg_act3_glitch.png"
const BG_BOARD := "res://assets/art/backgrounds/bg_act3_boardroom.png"
const CARD := "res://assets/art/cards/"


static func castle() -> Array:
	return [_briefing()]


static func dragon() -> Array:
	return [
		_ball(),
		_scrum(),
		_stealth_tamagotchi(),
		_princess(),
		_boss(),
		_epilogue_success(),
		_epilogue_burnout(),
		_cafe(),
		_cafe_peace(),
		_startup_ipo(),
		_relocate_ending(),
		_reset_civilization(),
	]


static func _ball() -> Dictionary:
	return {
		"id": "ball",
		"bg": BG_BALL,
		"speaker": "Дворцовый распорядитель",
		"text": "Перед логом — короткий бал. Цены на закуски растут в реальном времени. За троном розетка «молния» ни к чему.",
		"choices": [
			{
				"kind": "narrative",
				"label": "[Сюжет] Графиня CTR",
				"art": CARD + "card_a2_tinder.png",
				"speaker": "Графиня CTR",
				"branch_text": "Графиня меряет тебя взглядом A/B: «Свайпнешь вправо — или конверсия нулевая?»",
				"choices": [
					{
						"label": "Вариант A: комплимент",
						"art": CARD + "card_a2_tinder.png",
						"aside": "CTR растёт.",
						"result": "Она смеётся. Даёт визитку с QR из бересты.",
						"effects": {"people": 3, "mental": 1},
						"flag": "met_countess_ctr",
						"next": "scrum",
					},
					{
						"label": "Вариант B: про KPI",
						"art": CARD + "card_a2_hr_lamp.png",
						"aside": "Слишком корпоративно.",
						"result": "Она зевает. Конверсия свидания = 0.",
						"effects": {"mental": -1, "cringe": 1},
						"next": "scrum",
					},
				],
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] Барон Венчур",
				"art": CARD + "card_infogypsy_pass.png",
				"speaker": "Барон Венчур",
				"branch_text": "Толстый лорд жуёт крыло грифона: «50% доли души — и я инвестирую в твой квест.»",
				"choices": [
					{
						"label": "Взять инвестиции (доля души)",
						"art": CARD + "card_a2_lawyer_owl.png",
						"aside": "Term sheet кровью.",
						"result": "Мешок золота. Душа в питч-деке. Пригодится у дракона, если ты вор.",
						"effects": {"gold": 40, "mental": -2},
						"flag": "baron_venture",
						"next": "scrum",
					},
					{
						"label": "Отказать",
						"art": CARD + "card_threat_stick.png",
						"aside": "Equity — это ловушка.",
						"result": "Барон фыркает: «Без seed не взлетишь.»",
						"effects": {"mental": 1},
						"next": "scrum",
					},
				],
			},
			{
				"label": "Шут Алгоритм",
				"art": CARD + "card_act0_twerk.png",
				"aside": "Он генерит мемы про тебя.",
				"result": "Шут шепчет пасхалку про Святой Lightning за троном. Менталочка +1 от абсурда.",
				"effects": {"mental": 2, "people": 1},
				"flag": "met_jester_algo",
				"next": "scrum",
			},
			{
				"label": "Пропустить бал",
				"art": CARD + "card_relocate_forest.png",
				"aside": "Дедлайн важнее канапе.",
				"result": "Ты выходишь к дороге. Инфляция закусок тебя не догнала.",
				"effects": {},
				"next": "scrum",
			},
			{
				"kind": "clarify",
				"label": "Чего?",
				"art": CARD + "card_act0_confused.png",
				"speaker": "Рассказчик",
				"clarify_text": "Рассказчик (шепотом): Бал — это тусовка перед квестом. CTR — клики, Венчур — бабки за кусок души, Шут — клоун с нейросетью. Можно всё скипнуть и идти к дракону.",
			},
		],
	}


static func _briefing() -> Dictionary:
	return {
		"id": "briefing",
		"bg": BG_CASTLE,
		"speaker": "Король-CEO",
		"text": "Король чертит график: «Дракон украл Принцессу. Сын Маминой Подруги уже занял пост COO и спихнул таску на тебя. Закрой тикет — или билд отменят!»",
		"choices": [
			{
				"kind": "narrative",
				"label": "[Сюжет] Уточнить условия задачи",
				"art": CARD + "card_a2_hr_lamp.png",
				"speaker": "Король-CEO",
				"branch_text": "«А командировочные? Суточные? Страховка от ожогов?» Король морщится: «Мы тут семья, а не наёмники!»",
				"choices": [
					{
						"label": "«Сделаю всё ради Компании!»",
						"art": CARD + "card_act0_loyal.png",
						"aside": "Пластиковый значок «Работник месяца».",
						"result": "Самооценка падает, корпоративный дух растёт. Тикет «Дракон» назначен на тебя.",
						"effects": {"mental": -2, "crown": 4},
						"main_quest": 4,
						"unlock": "dragon_lair",
						"next": "end",
					},
					{
						"label": "Надавить и потребовать аванс",
						"art": CARD + "card_bribe_flatfoot.png",
						"aside": "Угроза профсоюзом.",
						"result": "Король бросает кошель, лишь бы не портить атмосферу.",
						"effects": {"gold": 20, "crown": -5},
						"main_quest": 4,
						"unlock": "dragon_lair",
						"next": "end",
					},
				],
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] Предложить оптимизацию",
				"art": CARD + "card_a2_mages_door.png",
				"speaker": "Король-CEO",
				"branch_text": "«Может, официальную ноту протеста?» Король бьёт кулаком: «Только хардкор! Только прямой экшен!»",
				"choices": [
					{
						"label": "Покорно взять ржавый кинжал",
						"art": CARD + "card_a2_buy_rusty.png",
						"aside": "Тупой. Зато бесплатно.",
						"result": "Кинжал в кармане. Бюджет всё ещё ноль.",
						"effects": {"gold": 5, "crown": -3, "item": "rusty_sword"},
						"main_quest": 4,
						"unlock": "dragon_lair",
						"next": "end",
					},
					{
						"label": "[Скрытый] Вылечить Короля подорожником",
						"art": CARD + "card_a2_plantain.png",
						"aside": "Антивирусный лист на лоб CEO.",
						"result": "Прилив сил! Король щедро спонсирует поход.",
						"effects": {"gold": 30, "crown": 5},
						"require_item": "plantain",
						"remove_item": "plantain",
						"main_quest": 4,
						"unlock": "dragon_lair",
						"next": "end",
					},
					{
						"label": "[Скрытый] Надеть шапочку из фольги",
						"art": CARD + "card_foil_hat.png",
						"aside": "Экранировать замок — стартап мечты.",
						"result": "«Гениально! Назначить CTO!» К дракону всё равно придётся.",
						"effects": {"crown": 5, "mental": 2},
						"require_item": "foil_hat",
						"main_quest": 4,
						"unlock": "dragon_lair",
						"next": "end",
					},
				],
			},
		],
	}


static func _scrum() -> Dictionary:
	return {
		"id": "scrum",
		"bg": BG_SCRUM,
		"speaker": "Скрам-Мастер",
		"text": "На выходе дорогу преграждает лесной Скрам-Мастер с бубном. «Стой! Прежде чем таску „Убить Дракона“, нужен дэйли и декомпозиция блокеров!»",
		"choices": [
			{
				"kind": "narrative",
				"label": "[Сюжет] Попробовать договориться",
				"art": CARD + "card_a2_hr_lamp.png",
				"speaker": "Скрам-Мастер",
				"branch_text": "«Дедлайн горит, пусти!» — «Без оценки в стори-поинтах никто никуда не пойдёт.»",
				"choices": [
					{
						"label": "Честно участвовать в дэйли",
						"art": CARD + "card_podcast.png",
						"aside": "4 часа про то, почему убийство не режется на 5 тасок.",
						"result": "Мозг плавится. Дэйли закрыт.",
						"effects": {"mental": -5, "health": -1},
						"next": "stealth",
					},
					{
						"label": "Заплатить, чтобы отстал (15)",
						"art": CARD + "card_bribe_flatfoot.png",
						"aside": "«Проведи дэйли сам с собой!»",
						"result": "Скрам уходит в рекурсию.",
						"effects": {"gold": -15, "mental": 2},
						"require_gold": 15,
						"next": "stealth",
					},
				],
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] Применить силу",
				"art": CARD + "card_threat_stick.png",
				"speaker": "Скрам-Мастер",
				"branch_text": "Вы хватаетесь за оружие. Он визжит: «Насилие не в Agile-манифесте!»",
				"choices": [
					{
						"label": "Ударить плашмя",
						"art": CARD + "card_a2_arena_sand.png",
						"aside": "Штраф в карму за токсичность.",
						"result": "Свободны и полны энергии.",
						"effects": {"mental": 3, "people": -4},
						"next": "stealth",
					},
					{
						"label": "[Скрытый] Бросить Тамагочи!",
						"art": CARD + "card_act0_loot.png",
						"aside": "«Покорми меня!» — новая таска.",
						"result": "Скрам убегает воспитывать питомца. Вы великолепны!",
						"effects": {"mental": 5, "people": 3},
						"require_item": "tamagotchi",
						"remove_item": "tamagotchi",
						"flag": "tamagotchi_thrown",
						"next": "stealth",
					},
				],
			},
		],
	}


static func _stealth_tamagotchi() -> Dictionary:
	## Без тамагочи — сразу к принцессе (не пустой бит «вариантов нет»).
	return {
		"id": "stealth",
		"bg": BG_ROAD,
		"speaker": "Стелс",
		"text": "Вы крадётесь мимо пещерных Гоблинов-Секьюрити. Идёте идеально тихо…",
		"require_item": "tamagotchi",
		"skip_to": "princess",
		"choices": [
			{
				"label": "Гомункул пищит из кармана",
				"art": CARD + "card_act0_loot.png",
				"aside": "«ПИ-ПИ-ПИ! Гомункул покакал!»",
				"result": "Гоблины просыпаются и жестоко избивают вас дубинками.",
				"effects": {"health": -5, "mental": -3},
				"require_item": "tamagotchi",
				"remove_item": "tamagotchi",
				"next": "princess",
			},
		],
	}


static func _princess() -> Dictionary:
	return {
		"id": "princess",
		"bg": BG_CAVE,
		"speaker": "Принцесса-Инфлюенсер",
		"text": "Принцесса снимает «кружочки» на зеркальце: «Ребятки, тут такой вайб в пещере!»",
		"auto_curse": {
			"require_item": "smoothie",
			"once_flag": "curse_smoothie_princess",
			"speaker": "Проклятие смузи",
			"aside": "Овсяное молоко + шаурма вспоминаются не вовремя.",
			"result": "Живот орёт как рвущийся пергамент! Народ в шоке от элитного конфуза.",
			"effects": {"people": -12, "cringe": 1, "mental": -1},
		},
		"choices": [
			{
				"label": "«Я пришёл спасать, пошли домой!»",
				"art": CARD + "card_a2_tinder.png",
				"aside": "Штатив свистит в воздухе.",
				"result": "Бьёт вас штативом за испорченные охваты.",
				"effects": {"health": -3, "mental": -2},
				"next": "boss",
			},
			{
				"label": "Предложить стать менеджером по рекламе",
				"art": CARD + "card_infogypsy_pass.png",
				"aside": "Таргет жрёт бюджет.",
				"result": "Забирает деньги на таргет.",
				"effects": {"gold": -20, "people": 5},
				"next": "boss",
			},
			{
				"label": "Игнорировать и пройти к Дракону",
				"art": CARD + "card_relocate_forest.png",
				"aside": "Она уже печатает пост.",
				"result": "Принцесса выкладывает гневный разоблачающий пост. Уважение народа падает.",
				"effects": {"people": -5},
				"next": "boss",
			},
			{
				"label": "[Скрытый] Подарить деревянный смартфон",
				"art": CARD + "card_wooden_phone.png",
				"aside": "Эко-френдли Дерево-Фон.",
				"result": "В восторге! Баффы восстанавливают здоровье.",
				"effects": {"health": 5, "people": 5},
				"require_item": "wooden_phone",
				"remove_item": "wooden_phone",
				"next": "boss",
			},
		],
	}


static func _boss() -> Dictionary:
	return {
		"id": "boss",
		"bg": BG_CAVE,
		"speaker": "Выгоревший Дракон",
		"text": "Дракон лежит на горе пустых коробок от пиццы. «Слушай, просто убей меня. Я выгорел. Даже огонь изрыгать не хочу.»",
		"choices": [
			{
				"kind": "narrative",
				"label": "[Сюжет] Спросить, в чём дело",
				"art": CARD + "card_sir_lag_hire.png",
				"speaker": "Дракон",
				"branch_text": "«Король не даёт лицензию на крафтовую кофейню. Говорит, не по лору. Я устал быть злодеем.»",
				"choices": [
					{
						"label": "Провести коуч-сессию (нужно 🧠 ≥ 10)",
						"art": CARD + "card_podcast.png",
						"aside": "Рамки только в голове.",
						"result": "Дракон плачет от счастья и решает открыть ИП.",
						"effects": {"mental": 2, "people": 5},
						"require_mental": 10,
						"flag": "ending_downshift",
						"set_dragon_stance": "coach",
						"next": "cafe",
					},
					{
						"label": "[Скрытый] Стартап: pitch IPO пещеры",
						"art": CARD + "card_a2_thieves_door.png",
						"aside": "Воры + Венчур = unicorn.",
						"result": "Дракон как pitch-deck. Инвесторы аплодируют. Пещера идёт на биржу.",
						"effects": {"gold": 80, "crown": 3, "people": -2},
						"require_guild": "thieves",
						"require_flag": "baron_venture",
						"flag": "ending_startup",
						"set_dragon_stance": "startup",
						"next": "startup_ipo",
					},
					{
						"label": "[Скрытый] Релокация вдвоём",
						"art": CARD + "card_relocate_forest.png",
						"aside": "Без отчёта Королю.",
						"result": "Вы с драконом срываетесь в лес. KPI горит без вас.",
						"effects": {"mental": 4, "crown": -8, "people": 4},
						"require_flag": "perk_relocant",
						"flag": "ending_relocate",
						"set_dragon_stance": "relocate",
						"next": "relocate_duo",
					},
					{
						"label": "[Скрытый] Угостить смузи из подорожника",
						"art": CARD + "card_smoothie.png",
						"aside": "Эко. Безглютен. Смертельно.",
						"result": "Аллергия! Чихает пламенем. Пещера сгорает вместе с вами.",
						"effects": {},
						"require_item": "smoothie",
						"game_over": "eco_death",
						"next": "end",
					},
					{
						"label": "[Скрытый] Мир — это Матрица!",
						"art": CARD + "card_matrix.png",
						"aside": "Загон «Матрица на минималках».",
						"result": "Дракон ловит экзистенциальный кризис и De-Spawn. Король в шоке от эффективности.",
						"effects": {"crown": 10, "people": 5},
						"require_flag": "pen_matrix_lite",
						"flag": "ending_success",
						"set_dragon_stance": "partner",
						"next": "success_meeting",
					},
				],
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] Достать оружие",
				"art": CARD + "card_a2_buy_rusty.png",
				"speaker": "Дракон",
				"branch_text": "Дракон даже не шевелится. «Давай, руби. Только не по шее — там хондроз.»",
				"choices": [
					{
						"label": "Отрубить голову!",
						"art": CARD + "card_a2_arena_honest.png",
						"aside": "Премия и пустота внутри.",
						"result": "Король доволен. Вы Топ-Менеджер с язвой.",
						"effects": {"health": -4, "crown": 8, "gold": 40},
						"flag": "ending_success",
						"set_dragon_stance": "enemy",
						"next": "success_meeting",
					},
					{
						"label": "[Скрытый] Сэр Лаг принимает удар",
						"art": CARD + "card_sir_lag_hire.png",
						"aside": "Танк с пингом закрывает тебя щитом… через 5 секунд.",
						"result": "Лаг ловит пламя животом. Ты рубишь. Победа с меньшим уроном.",
						"effects": {"health": -1, "crown": 8, "gold": 40},
						"require_flag": "companion_sir_lag",
						"flag": "ending_success",
						"set_dragon_stance": "enemy",
						"next": "success_meeting",
					},
					{
						"label": "[Скрытый] Загуглить уязвимости (Смарт-Меч)",
						"art": CARD + "card_phone_it_defer.png",
						"aside": "«Бейте в левую пятку.»",
						"result": "Крит. Батарея меча садится навсегда. Победа без лишних ран.",
						"effects": {"crown": 8, "gold": 40},
						"require_item": "smart_sword",
						"remove_item": "smart_sword",
						"flag": "ending_success",
						"set_dragon_stance": "enemy",
						"next": "success_meeting",
					},
					{
						"label": "Передумать и убежать",
						"art": CARD + "card_relocate_forest.png",
						"aside": "Страх компилируется быстрее храбрости.",
						"result": "Король объявляет вас трусом. Увольнение без выходного.",
						"effects": {},
						"game_over": "coward_fired",
						"next": "end",
					},
					{
						"label": "[Скрытый] Патч 1.0 + Иск к Реальности",
						"art": CARD + "card_a2_patch.png",
						"aside": "Сброс цивилизации. Точка невозврата.",
						"result": "Мир откатывается к биту 0. Вы нажали кнопку, которую нельзя было нажимать.",
						"effects": {"mental": -2},
						"require_item": "patch_1_0",
						"require_item_2": "reality_lawsuit",
						"remove_items": ["patch_1_0", "reality_lawsuit"],
						"flag": "ending_reset",
						"next": "reset",
					},
				],
			},
		],
	}


static func _epilogue_success() -> Dictionary:
	return {
		"id": "success_meeting",
		"bg": BG_BOARD,
		"speaker": "Советник",
		"text": "Трон. Тяжёлая корона. Советник вбегает: «Крестьяне бастуют, Инквизиция хочет костров, инвесторы просят ROI!»",
		"choices": [
			{
				"kind": "narrative",
				"label": "[Сюжет] Попытаться всем угодить",
				"art": CARD + "card_a2_hr_lamp.png",
				"speaker": "Совещание",
				"branch_text": "Вы жонглируете бумагами. Язва уже чешется.",
				"choices": [
					{
						"label": "Снизить налоги",
						"art": CARD + "card_bribe_flatfoot.png",
						"aside": "Народ счастлив. Инвесторы уходят.",
						"result": "Казна пустеет. Стресс растёт.",
						"effects": {"mental": -3, "crown": -5},
						"next": "burnout",
					},
					{
						"label": "Разогнать митинг инквизицией",
						"art": CARD + "card_a2_punch_guard.png",
						"aside": "Жестоко, но эффективно.",
						"result": "Власть сохранена. Душа — нет. Стресс растёт.",
						"effects": {"mental": -3, "people": -5},
						"next": "burnout",
					},
				],
			},
			{
				"label": "[Скрытый] Делегировать всё брату (смартфон)",
				"art": CARD + "card_wooden_phone.png",
				"aside": "Звонок в Нижние Вай-Файки.",
				"result": "Брат — новый CEO. Вы на Бали (Северные Пустоши). Золотой Парашют!",
				"effects": {"mental": 5, "gold": 50, "people": 5},
				"require_item": "wooden_phone",
				"flag": "ending_golden_parachute",
				"next": "end",
			},
		],
	}


static func _epilogue_burnout() -> Dictionary:
	return {
		"id": "burnout",
		"bg": BG_BOARD,
		"speaker": "Рассказчик",
		"text": "Вы хватаетесь за сердце. Бумаги падают на пол.",
		"choices": [
			{
				"label": "Принять инфаркт менеджера",
				"art": CARD + "card_a2_apple_calibur.png",
				"aside": "Богатство, слава, трон… и переработки.",
				"result": "Титры. Достижение «Раб Лампы». Вас запомнят как эффективного менеджера.",
				"effects": {"health": -10},
				"flag": "ending_lamp_slave",
				"next": "end",
			},
		],
	}


static func _cafe() -> Dictionary:
	return {
		"id": "cafe",
		"bg": BG_CAFE,
		"speaker": "Кофейня «Жареный Рыцарь»",
		"text": "Дверь открывается. Входит старый знакомый — Торговец-Инфоцыган. «О, привет! Сделаешь скидку по старой дружбе?»",
		"choices": [
			{
				"kind": "narrative",
				"label": "[Сюжет] Поприветствовать гостя",
				"art": CARD + "card_infogypsy_expose.png",
				"speaker": "Касса",
				"branch_text": "Вы улыбаетесь и протираете стойку.",
				"choices": [
					{
						"label": "Налить латте за счёт заведения",
						"art": CARD + "card_infogypsy_expose.png",
						"aside": "Молочная пенка — кармическая терапия.",
						"result": "Слеза. «Ты первый, кто не пытался мне что-то продать.» Щедрые чаевые.",
						"effects": {"gold": 10, "mental": 5},
						"next": "cafe_peace",
					},
					{
						"label": "«Успешный Эспрессо» за 100",
						"art": CARD + "card_infogypsy_pass.png",
						"aside": "Кармическая месть.",
						"result": "Обычный кофе по цене крыла грифона. Дракон пыхает одобрительно.",
						"effects": {"gold": 100, "crown": 2},
						"next": "cafe_peace",
					},
				],
			},
			{
				"label": "[Скрытый] Скидка компаньону",
				"art": CARD + "card_infogypsy_disciple.png",
				"aside": "Бывший партнёр по воронке.",
				"result": "Чаевые и визитка «скидки на воздух».",
				"effects": {"gold": 25, "mental": 4, "people": 3},
				"require_flag": "companion_infogypsy",
				"next": "cafe_peace",
			},
			{
				"label": "[Скрытый] Прийти в его камзоле",
				"art": CARD + "card_infogypsy_phone.png",
				"aside": "Он узнаёт ткань.",
				"result": "Awkward. Платит двойной счёт и не возвращается.",
				"effects": {"gold": 40, "people": -2, "mental": 2},
				"require_item": "infogypsy_coat",
				"next": "cafe_peace",
			},
		],
	}


static func _cafe_peace() -> Dictionary:
	return {
		"id": "cafe_peace",
		"bg": BG_CAFE,
		"speaker": "Дракон-бариста",
		"text": "День к концу. Дракон вытирает чашки хвостом. «Знаешь, без убийств и KPI жизнь приятнее.»",
		"choices": [
			{
				"label": "Найти свой Исходный Код",
				"art": CARD + "card_act0_loyal.png",
				"aside": "Lo-Fi. Без ипотеки.",
				"result": "Жили долго и счастливо. Достижение «Свободный Человек». Истинная концовка.",
				"effects": {"mental": 5, "people": 5},
				"flag": "ending_free_human",
				"set_dragon_stance": "partner",
				"next": "end",
			},
		],
	}


static func _startup_ipo() -> Dictionary:
	return {
		"id": "startup_ipo",
		"bg": BG_BOARD,
		"speaker": "Барон Венчур",
		"text": "Биржа орёт. Акции «DragonCave Inc.» взлетают. Дракон в галстуке из цепей.",
		"choices": [
			{
				"label": "Выйти в кэш на пике",
				"art": CARD + "card_infogypsy_pass.png",
				"aside": "Exit strategy.",
				"result": "Концовка «Стартап». Ты богат, душа на 50% у Венчура, дракон — CEO. Король покупает подписку на отчёты.",
				"effects": {"gold": 50, "mental": -2},
				"flag": "ending_startup_done",
				"next": "end",
			},
		],
	}


static func _relocate_ending() -> Dictionary:
	return {
		"id": "relocate_duo",
		"bg": BG_ROAD,
		"speaker": "Рассказчик",
		"text": "Лес. Гамаки. Дракон жарит зефир огнём на минимум. Королевские гонцы не находят VPN-сосну.",
		"choices": [
			{
				"label": "Остаться релокантами",
				"art": CARD + "card_relocate_forest.png",
				"aside": "Без отчёта. Без трона.",
				"result": "Концовка «Релокация вдвоём». Вы живёте off-grid. KPI Короля красный. Вы — зелёные.",
				"effects": {"mental": 5, "people": 2},
				"flag": "ending_relocate_done",
				"next": "end",
			},
		],
	}


static func _reset_civilization() -> Dictionary:
	return {
		"id": "reset",
		"bg": BG_GLITCH,
		"speaker": "SYSTEM",
		"text": "Мир мигает. Патч 1.0 + Иск к Реальности. Четвёртая стена трещит.",
		"choices": [
			{
				"label": "Принять Сброс Цивилизации",
				"art": CARD + "card_a2_patch.png",
				"aside": "Ctrl+Z на всё Средневековье.",
				"result": "Титры глючат. Достижение «Кнопка, которую нельзя было нажимать».",
				"effects": {},
				"flag": "ending_civilization_reset",
				"next": "end",
			},
		],
	}
