extends RefCounted
class_name Act2Beats
## Акт 2 Биг Дата — канон act_2_city_choices.md (основная цепочка города).

const BG_CUSTOMS := "res://assets/art/backgrounds/bg_act2_customs.png"
const BG_CITY := "res://assets/art/backgrounds/bg_act2_city.png"
const BG_FORGE := "res://assets/art/backgrounds/bg_act2_forge.png"
const BG_TINDER := "res://assets/art/backgrounds/bg_act2_tinder.png"
const BG_GUILDS := "res://assets/art/backgrounds/bg_act2_guilds.png"
const BG_GUILD_WAR := "res://assets/art/backgrounds/bg_act2_guild_warriors.png"
const BG_GUILD_MAGE := "res://assets/art/backgrounds/bg_act2_guild_mages.png"
const BG_GUILD_THIEF := "res://assets/art/backgrounds/bg_act2_guild_thieves.png"
const BG_HR := "res://assets/art/backgrounds/bg_act2_hr.png"
const BG_ARENA := "res://assets/art/backgrounds/bg_act2_arena.png"
const CARD := "res://assets/art/cards/"


static func beats() -> Array:
	return [
		_customs(),
		_market(),
		_forge(),
		_guild_pick(),
		_warriors_audit(),
		_mages_bug(),
		_thieves_pitch(),
		_hr(),
		_tinder(),
		_arena(),
		_arena_r2(),
		_arena_final(),
		_apple_curse(),
	]


static func _customs() -> Dictionary:
	return {
		"id": "customs",
		"bg": BG_CUSTOMS,
		"speaker": "Стражник Face Control",
		"text": "Стражник блокирует ворота щитом на 9 квадратов. «Докажи, что ты человек! Выбери все квадраты со светофорами!»",
		"choices": [
			{
				"kind": "clarify",
				"label": "Чего?",
				"art": CARD + "card_act0_confused.png",
				"speaker": "Рассказчик",
				"clarify_text": "Рассказчик (шепотом): «Капча» — это тупой тест для идиотов и гоблинов. «Светофоры» — волшебные столбы будущего, которых в Средневековье нет. Стражник всё равно найдёт, за что взять налог. Классика Face Control.",
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] Попытаться пройти капчу",
				"art": CARD + "card_a2_captcha_lantern.png",
				"speaker": "Капча",
				"branch_text": "Вы вглядываетесь в картинки. Светофоров в Средневековье нет!",
				"choices": [
					{
						"kind": "clarify",
						"label": "Чего? Фонари?!",
						"art": CARD + "card_act0_confused.png",
						"speaker": "Рассказчик",
						"clarify_text": "Рассказчик (шепотом): Фонари на карете — это почти светофор, если очень хочется. Красные глаза инквизитора — тоже почти. Оба варианта кончаются налогом или алебардой. Выбирай стиль поражения.",
					},
					{
						"label": "Ткнуть в фонари на карете",
						"art": CARD + "card_a2_captcha_lantern.png",
						"aside": "Капча уровня Middle Ages.",
						"result": "«Это повозка премиум-класса, а не светофор. Налог на глупость!»",
						"effects": {"gold": -5, "crown": 2},
						"next": "market",
					},
					{
						"label": "Ткнуть в красные глаза инквизитора",
						"art": CARD + "card_a2_hr_lamp.png",
						"aside": "На фоне красные глаза. Соблазнительно.",
						"result": "«Красные глаза от недосыпа — это не светофор!» Алебарда подтверждает.",
						"effects": {"health": -2, "inquisition": -3},
						"next": "market",
					},
				],
			},
			{
				"label": "«Я не робот, я просто грязный»",
				"art": CARD + "card_a2_not_robot.png",
				"aside": "Честность — лучшая политика. Иногда.",
				"result": "Вас окатывает грязью из телеги мажоров.",
				"effects": {"health": -1, "people": -2},
				"next": "market",
			},
			{
				"label": "Дать стражнику в глаз",
				"art": CARD + "card_a2_punch_guard.png",
				"aside": "Дипломатия кулаком.",
				"result": "Сутки в КПЗ. Зато народный герой очереди.",
				"effects": {"health": -2, "crown": -5, "people": 4},
				"next": "market",
			},
			{
				"label": "[Скрытый] Ржавый Меч — прорыв с боем!",
				"art": CARD + "card_a2_buy_rusty.png",
				"aside": "Меч vs алебарда. Физика не на вашей стороне.",
				"result": "Вы бьёте стражника по шлему — меч разлетается на куски! Стражник даже не почесался и отправил вас в КПЗ.",
				"effects": {"health": -3, "crown": -5},
				"require_item": "rusty_sword",
				"remove_item": "rusty_sword",
				"next": "market",
			},
			{
				"label": "[Скрытый] Показать IT-бронь",
				"art": CARD + "card_phone_it_defer.png",
				"aside": "Кора с яблоком открывает VIP.",
				"result": "VIP-проход. Стражник кланяется гаджету.",
				"effects": {"crown": 5},
				"require_item": "wooden_phone",
				"next": "market",
			},
			{
				"label": "[Скрытый] Надеть шапочку из фольги",
				"art": CARD + "card_foil_hat.png",
				"aside": "Биометрия сбоит от блеска.",
				"result": "Стражник крестится: «Проходите, блаженный, только не облучайте нас».",
				"effects": {"mental": 3},
				"require_item": "foil_hat",
				"next": "market",
			},
		],
	}


static func _market() -> Dictionary:
	return {
		"id": "market",
		"bg": BG_CITY,
		"speaker": "Эльф чёрного рынка",
		"text": "В подворотне эльф презентует «Умный Меч по подписке».",
		"choices": [
			{
				"label": "Подписка Apple-Калибур (15)",
				"art": CARD + "card_a2_apple_calibur.png",
				"aside": "Условия в мелком шрифте на бересте.",
				"result": "Меч гудит. Подписка активна. Пока.",
				"no_gold_result": "У вас нет золота на Apple-Калибур. Эльф закатывает глаза: «Без подписки — без меча».",
				"effects": {"gold": -15, "item": "apple_calibur"},
				"require_gold": 15,
				"next": "forge",
			},
			{
				"label": "Купить Ржавый Меч (5)",
				"art": CARD + "card_a2_buy_rusty.png",
				"aside": "Классика жанра без SaaS.",
				"result": "Ржавый, но твой. Без автопродления.",
				"no_gold_result": "У вас нет золота даже на ржавчину. Эльф: «Приходи с монетами».",
				"effects": {"gold": -5, "item": "rusty_sword"},
				"require_gold": 5,
				"next": "forge",
			},
			{
				"label": "Нотариус: пробный героизм (бесплатно)",
				"art": CARD + "card_a2_lawyer_owl.png",
				"aside": "7 дней «Жизнь+». Потом автопродление душой.",
				"result": "Подпись кровью. Подписка на Душу активна. Отписка — у Юриста в Лесу.",
				"effects": {"mental": -1},
				"set_soul_sub": true,
				"next": "forge",
			},
			{
				"label": "«Я дерусь на кулаках»",
				"art": CARD + "card_a2_fists.png",
				"aside": "Бюджет на оружие = 0.",
				"result": "Эльф пожимает плечами. Народ уважает.",
				"effects": {"people": 2},
				"next": "forge",
			},
			{
				"label": "Купить Гомункул-Тамагочи (8)",
				"art": CARD + "card_act0_loot.png",
				"aside": "Пищит «я покакал» в бою. Классика.",
				"result": "Крошечный гомункул в яйце. Корми смузи — вырастет качок.",
				"no_gold_result": "Ты хлопаешь по карманам. Тамагочи смотрит с презрением.",
				"effects": {"gold": -8, "item": "tamagotchi"},
				"require_gold": 8,
				"next": "forge",
			},
			{
				"label": "[Скрытый] Сбыть кристалл RTX (за 20)",
				"art": CARD + "card_steal_gem.png",
				"aside": "Эльф прищуривается: «Фермерский рендер?»",
				"result": "Кристалл уходит в чёрный рынок GPU. +20💰.",
				"effects": {"gold": 20, "people": -2},
				"require_item": "rtx_crystal",
				"remove_item": "rtx_crystal",
				"next": "forge",
			},
		],
	}


static func _forge() -> Dictionary:
	return {
		"id": "forge",
		"bg": BG_FORGE,
		"speaker": "Кузнец-Сисадмин",
		"text": "В подворотне гудит кузня. Здоровенный орк бьёт кувалдой по материнской плате. «Нужен апгрейд железа? Давай сюда свой лут!»",
		"choices": [
			{
				"kind": "narrative",
				"label": "[Сюжет] Показать Ржавый Меч",
				"art": CARD + "card_a2_buy_rusty.png",
				"require_item": "rusty_sword",
				"speaker": "Кузнец-Сисадмин",
				"branch_text": "Орк презрительно фыркает: «Это старьё даже гоблина не напугает. Есть что-то из умных технологий?»",
				"choices": [
					{
						"label": "Скрафтить Смарт-Меч",
						"art": CARD + "card_a2_apple_calibur.png",
						"aside": "Синяя изолента — магия инженерии.",
						"result": "Орк приматывает кору к эфесу. Меч светится!",
						"effects": {"item": "smart_sword"},
						"require_item": "wooden_phone",
						"remove_items": ["rusty_sword", "wooden_phone"],
						"next": "guild_pick",
					},
					{
						"label": "Заточить за 10 золота",
						"art": CARD + "card_a2_buy_rusty.png",
						"aside": "Без гарантии, бро.",
						"result": "Орк точит меч — он ломается пополам.",
						"effects": {"gold": -10, "cringe": 1},
						"require_gold": 10,
						"remove_item": "rusty_sword",
						"next": "guild_pick",
					},
				],
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] Показать фольгу",
				"art": CARD + "card_foil_hat.png",
				"require_item": "foil_hat",
				"speaker": "Кузнец-Сисадмин",
				"branch_text": "Орк кивает: «Отличный экран. Если добавим биологический модуль, сможешь ловить Wi-Fi от богов.»",
				"choices": [
					{
						"label": "Скрафтить Био-Антенну (фольга + подорожник)",
						"art": CARD + "card_foil_windmill.png",
						"aside": "Куст в фольге — следующий сезон моды.",
						"result": "Теперь на голове куст. Слышишь голоса предков. Био-Антенна готова.",
						"effects": {"item": "bio_antenna", "mental": 2},
						"require_item": "plantain",
						"remove_items": ["foil_hat", "plantain"],
						"next": "guild_pick",
					},
					{
						"label": "Нет подорожника — уйти",
						"art": CARD + "card_a2_plantain.png",
						"aside": "«Ищи антивирусный лист в Лесу Релокантов.»",
						"result": "Орк указывает на тропу в лес. Фольга пока твоя.",
						"effects": {},
						"require_no_item": "plantain",
						"next": "guild_pick",
					},
					{
						"label": "Отказаться",
						"art": CARD + "card_foil_hat.png",
						"aside": "Иногда меньше — лучше.",
						"result": "Уходишь. Шапочка надёжнее без био-хаков.",
						"effects": {},
						"next": "guild_pick",
					},
				],
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] Протеиновый Гомункул",
				"art": CARD + "card_smoothie.png",
				"require_item": "tamagotchi",
				"speaker": "Кузнец-Сисадмин",
				"branch_text": "Орк нюхает яйцо: «Если залить смузи — вырастет качок. Один раз спасёт жопу в бою.»",
				"choices": [
					{
						"label": "Скрафтить (Тамагочи + Смузи)",
						"art": CARD + "card_smoothie.png",
						"aside": "Качается под Lo-Fi.",
						"result": "Протеиновый Гомункул готов. Уйдёт в фитнес после первого сейва.",
						"effects": {"item": "protein_homunculus"},
						"require_item": "smoothie",
						"remove_items": ["tamagotchi", "smoothie"],
						"next": "guild_pick",
					},
					{
						"label": "Нет смузи — уйти",
						"art": CARD + "card_skip.png",
						"aside": "Кричи про смузи с рождения или купи… ой, уже поздно.",
						"result": "Орк: «Без протеина не растёт.» Тамагочи пищит.",
						"effects": {},
						"require_no_item": "smoothie",
						"next": "guild_pick",
					},
					{
						"label": "Отказаться",
						"art": CARD + "card_threat_stick.png",
						"aside": "Пусть пищит.",
						"result": "Уходишь с яйцом. Когда-нибудь.",
						"effects": {},
						"next": "guild_pick",
					},
				],
			},
			{
				"label": "Уйти без крафта",
				"art": CARD + "card_relocate_forest.png",
				"aside": "Кузня подождёт.",
				"result": "Орк машет кувалдой на прощание.",
				"effects": {},
				"next": "guild_pick",
			},
		],
	}


static func _guild_pick() -> Dictionary:
	return {
		"id": "guild_pick",
		"bg": BG_GUILDS,
		"speaker": "Биржа труда",
		"text": "Три двери. Гильдия Воинов пахнет потом и дедлайнами. Башня Магов искрит багами. В подвале Воров шумит крипто-стартап. Сын Маминой Подруги выходит из ВИП-комнаты с бейджиком «Сеньор-Директор».",
		"choices": [
			{
				"kind": "narrative",
				"label": "[Сюжет] Гильдия Воинов",
				"art": CARD + "card_a2_warriors_door.png",
				"speaker": "Менеджер в латах",
				"branch_text": "Менеджер спрашивает: «Готов работать по 14 часов ради компании Короля?»",
				"choices": [
					{
						"label": "«Живу ради переработок!»",
						"art": CARD + "card_a2_warriors_door.png",
						"aside": "Спина болит авансом.",
						"result": "Менеджер плачет от счастья. Ты принят. Сын Маминой Подруги смеётся над твоей зарплатой.",
						"effects": {"crown": 5, "mental": -3},
						"set_guild": "warriors",
						"next": "warriors_audit",
					},
					{
						"label": "Спросить про ДМС",
						"art": CARD + "card_help_castle.png",
						"aside": "Бесплатные подорожники в офисе.",
						"result": "Принят, но на карандаш.",
						"effects": {"health": 2, "crown": -2},
						"set_guild": "warriors",
						"next": "warriors_audit",
					},
				],
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] Башня Магов",
				"art": CARD + "card_a2_mages_door.png",
				"speaker": "Сеньор-архимаг",
				"branch_text": "Бородатый сеньор смотрит в шар: «Ты знаешь заклинание C++?»",
				"choices": [
					{
						"label": "«Пишу руны на Python»",
						"art": CARD + "card_a2_mages_door.png",
						"aside": "Питон — для укротителей змей.",
						"result": "Берут джуниором-кофеваром.",
						"effects": {"mental": 2, "crown": 2},
						"set_guild": "mages",
						"next": "mages_bug",
					},
					{
						"label": "«Умею гуглить заклинания»",
						"art": CARD + "card_phone_google.png",
						"aside": "Наконец-то профессионал.",
						"result": "Архимаг обнимает тебя.",
						"effects": {"mental": 4, "people": -2},
						"set_guild": "mages",
						"next": "mages_bug",
					},
				],
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] К Ворам",
				"art": CARD + "card_a2_thieves_door.png",
				"speaker": "Хакер в капюшоне",
				"branch_text": "Хакер шепчет: «Мы запускаем NFT-редиску. Вложишься?»",
				"choices": [
					{
						"label": "Отдать 5 золота",
						"art": CARD + "card_a2_thieves_door.png",
						"aside": "Мамонт, но в команде.",
						"result": "Ты в стартапе. Кошелёк легче.",
						"effects": {"gold": -5, "mental": -2},
						"require_gold": 5,
						"set_guild": "thieves",
						"next": "thieves_pitch",
					},
					{
						"label": "Украсть NFT-редиску",
						"art": CARD + "card_steal_gem.png",
						"aside": "Отличный mindset.",
						"result": "Хакер уважительно кивает.",
						"effects": {"gold": 10, "inquisition": -3},
						"set_guild": "thieves",
						"next": "thieves_pitch",
					},
					{
						"label": "[Скрытый] Отсканировать редиску смартфоном!",
						"art": CARD + "card_phone_google.png",
						"aside": "Правый клик → Сохранить как.",
						"result": "Хакер в ужасе: «Ты украл мой блокчейн!» Воры признают вас боссом.",
						"effects": {"gold": 20, "crown": -5, "mental": 4},
						"require_item": "wooden_phone",
						"set_guild": "thieves",
						"next": "thieves_pitch",
					},
					{
						"kind": "clarify",
						"label": "Чего? NFT?!",
						"art": CARD + "card_act0_confused.png",
						"speaker": "Рассказчик",
						"clarify_text": "Рассказчик (шепотом): NFT-редиска — картинка редиски, за которую просят золото. Сканер смартфона = украсть «уникальность». Воры это уважают.",
					},
				],
			},
		],
	}


static func _warriors_audit() -> Dictionary:
	return {
		"id": "warriors_audit",
		"bg": BG_GUILD_WAR,
		"speaker": "Ревизор Короля",
		"text": "В Гильдию приехал ревизор. Требует отчёт по убитым гоблинам.",
		"choices": [
			{
				"label": "Красивые графики",
				"art": CARD + "card_podcast.png",
				"aside": "PowerPoint на бересте.",
				"result": "Ревизор доволен. Коллеги ненавидят.",
				"effects": {"crown": 5, "people": -4},
				"next": "hr",
			},
			{
				"label": "Сказать правду (брага)",
				"art": CARD + "card_donate_cry.png",
				"aside": "Весь день пили. Честно.",
				"result": "Штраф, но народное уважение.",
				"effects": {"gold": -10, "crown": -4, "people": 5},
				"next": "hr",
			},
			{
				"label": "Спрятаться в шкафу",
				"art": CARD + "card_ignore_sleep.png",
				"aside": "AFK от аудита.",
				"result": "+1 кринж. Шкаф пахнет потом.",
				"effects": {"mental": -2, "cringe": 1},
				"next": "hr",
			},
		],
	}


static func _mages_bug() -> Dictionary:
	return {
		"id": "mages_bug",
		"bg": BG_GUILD_MAGE,
		"speaker": "Прод",
		"text": "Падает магический щит-файрвол перед Королём.",
		"choices": [
			{
				"label": "Свалить на алхимиков",
				"art": CARD + "card_cheat.png",
				"aside": "Классический blame-shift.",
				"result": "Бонус за «инцидент-менеджмент».",
				"effects": {"gold": 15, "crown": 2, "people": -3},
				"next": "hr",
			},
			{
				"label": "Перезагрузить посохом",
				"art": CARD + "card_ddos_stick.png",
				"aside": "Hard reset.",
				"result": "Щит моргнул. Спина тоже.",
				"effects": {"health": -2, "people": 4},
				"next": "hr",
			},
			{
				"label": "[Скрытый] Принять волну фольгой",
				"art": CARD + "card_foil_windmill.png",
				"aside": "Экран от магии богов.",
				"result": "Щит спасён! Фольга шипит.",
				"effects": {"crown": 6, "mental": 3},
				"require_item": "foil_hat",
				"next": "hr",
			},
		],
	}


static func _thieves_pitch() -> Dictionary:
	return {
		"id": "thieves_pitch",
		"bg": BG_GUILD_THIEF,
		"speaker": "Инвестор-лорд",
		"text": "Презентуете проект «Блокчейн-Лошадь» толстому лорду.",
		"choices": [
			{
				"label": "«Метавселенная» и «Синергия»",
				"art": CARD + "card_blockchain.png",
				"aside": "Buzzwords творят чудеса.",
				"result": "Инвестор пугается и даёт деньги.",
				"effects": {"gold": 25, "people": -2},
				"next": "hr",
			},
			{
				"label": "Признаться: деревянная лошадь",
				"art": CARD + "card_a2_fists.png",
				"aside": "Честность наказуема.",
				"result": "Вас бьют палками.",
				"effects": {"health": -3, "crown": -3},
				"next": "hr",
			},
			{
				"label": "[Скрытый] Презентация со смартфона",
				"art": CARD + "card_phone_google.png",
				"aside": "Пиксели убеждают лучше слов.",
				"result": "Инвестор покупает компанию.",
				"effects": {"gold": 40, "crown": 5},
				"require_item": "wooden_phone",
				"next": "hr",
			},
		],
	}


static func _hr() -> Dictionary:
	return {
		"id": "hr",
		"bg": BG_HR,
		"speaker": "Инквизитор-HR",
		"text": "На вас донос: лайкнули оппозиционную фреску. Инквизитор светит лампой в лицо.",
		"choices": [
			{
				"kind": "narrative",
				"label": "[Сюжет] Оправдаться",
				"art": CARD + "card_a2_hr_lamp.png",
				"speaker": "Инквизитор-HR",
				"branch_text": "«Это не я! Аккаунт взломали гоблины!» Инквизитор: «Докажи. Испытание водой!»",
				"choices": [
					{
						"label": "Испытание водой",
						"art": CARD + "card_a2_hr_lamp.png",
						"aside": "Чан холодный. Лёгкие тоже.",
						"result": "Не утонул — не ведьма. Воспаление лёгких в подарок.",
						"effects": {"health": -3, "people": 5, "inquisition": -2},
						"next": "tinder",
					},
					{
						"label": "Покаянное видео",
						"art": CARD + "card_podcast.png",
						"aside": "Извинения за лайк в прямом эфире.",
						"result": "Народ презирает. Инквизиция довольна.",
						"effects": {"mental": -4, "inquisition": 5, "people": -5},
						"next": "tinder",
					},
				],
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] Намекнуть на взятку",
				"art": CARD + "card_bribe_flatfoot.png",
				"speaker": "Инквизитор-HR",
				"branch_text": "Подмигиваете: «Досудебно?» Инквизитор показывает три пальца.",
				"choices": [
					{
						"label": "Дать 30 золота",
						"art": CARD + "card_bribe_flatfoot.png",
						"aside": "Коррупция — скрепа.",
						"result": "«Ошибка, вы кристально чисты».",
						"effects": {"gold": -30, "inquisition": 2},
						"require_gold": 30,
						"next": "tinder",
					},
					{
						"label": "Дать 3 золота",
						"art": CARD + "card_bribe_puppies.png",
						"aside": "Оскорбление должностного лица.",
						"result": "Розги. Много розог.",
						"effects": {"health": -4, "gold": -3, "crown": -4},
						"require_gold": 3,
						"next": "tinder",
					},
				],
			},
			{
				"kind": "narrative",
				"label": "[Сюжет] Молчать",
				"art": CARD + "card_act0_defy.png",
				"speaker": "Инквизитор-HR",
				"branch_text": "Каменное лицо. Инквизитор нервничает: «Ты что, из айтишников?»",
				"choices": [
					{
						"label": "Кивнуть",
						"art": CARD + "card_act0_loyal.png",
						"aside": "Они сервер держат.",
						"result": "Отпускают с предупреждением.",
						"effects": {"mental": 2, "crown": 2, "inquisition": -3},
						"next": "tinder",
					},
					{
						"label": "[Скрытый] Надеть шапочку из фольги",
						"art": CARD + "card_foil_hat.png",
						"aside": "Металл + лампа HR = риск, но щит от мыслей.",
						"result": "Инквизитор не читает мысли. Отпускает нервно. 🧠 в норме.",
						"effects": {"mental": 4, "inquisition": -2},
						"require_item": "foil_hat",
						"next": "tinder",
					},
					{
						"label": "[Скрытый] Показать смартфон",
						"art": CARD + "card_phone_it_defer.png",
						"aside": "Высшее Руководство в кармане.",
						"result": "Инквизитор на коленях: «Простите!»",
						"effects": {"crown": 5, "inquisition": 5, "mental": 3},
						"require_item": "wooden_phone",
						"next": "tinder",
					},
				],
			},
		],
	}


static func _tinder() -> Dictionary:
	return {
		"id": "tinder",
		"bg": BG_TINDER,
		"speaker": "Бабка-сваха",
		"text": "Решаете остепениться. Бабка-сваха кидает портреты на бересте. Свайпай: вправо — лайк, влево — отказ.",
		"minigame": "tinder_swipe",
		"next": "arena",
		"choices": [],
	}


static func _arena() -> Dictionary:
	## Прототип боя «Дуэль Спринтов» вместо чисто-нарративных раундов 1–2.
	return {
		"id": "arena",
		"bg": BG_ARENA,
		"speaker": "Корпоратив-арена",
		"text": "Турнир «Герой Квартала». Против тебя — Гоблин-Стажёр. В ВИП-ложе Сын Маминой Подруги машет «1/10». Начинается Дуэль Спринтов: смотри телеграф и бей карточками умений!",
		"minigame": "sprint_duel",
		"duel_enemy": "Гоблин-Стажёр",
		"duel_hp": 14,
		"next": "end",
		"choices": [],
	}


static func _arena_r2() -> Dictionary:
	## Раунд 2: мидл-менеджер
	return {
		"id": "arena_r2",
		"bg": BG_ARENA,
		"speaker": "Корпоратив-арена · Раунд 2",
		"text": "Раунд 2: Рыцарь Среднего Звена. Копьё с табличкой «Стори-поинты», щит из Excel-бересты. «Синканемся асинхронно!»",
		"choices": [
			{
				"label": "Драться в лоб",
				"art": CARD + "card_a2_arena_honest.png",
				"aside": "Честь vs дедлайн.",
				"result": "Ты пробиваешь бересту. Он пишет тебе фидбек на 4 страницы прямо в песке.",
				"effects": {"health": -3, "mental": -1, "crown": 2},
				"next": "arena_final",
			},
			{
				"label": "Закидать его песком «блокеров»",
				"art": CARD + "card_a2_arena_sand.png",
				"aside": "Статус: Blocked by sand.",
				"result": "Мидл кашляет и уходит в асинхрон. Толпа делится на лайки и дизлайки.",
				"effects": {"health": -1, "people": -3, "gold": 5},
				"next": "arena_final",
			},
			{
				"label": "[Скрытый] Лаг танчит мидла",
				"art": CARD + "card_sir_lag_hire.png",
				"aside": "«Сначала я, потом урон» — его жизненное кредо.",
				"result": "Копьё вязнет в лаге. Мидл эскалирует на тимлида воздуха.",
				"effects": {"health": -1, "crown": 3, "people": 1},
				"require_flag": "companion_sir_lag",
				"next": "arena_final",
			},
			{
				"label": "[Скрытый] Смарт-Меч по копью",
				"art": CARD + "card_a2_apple_calibur.png",
				"aside": "Изолента + кора = вайб.",
				"result": "Копьё «стори-поинтов» рассыпается на таски. Зал молчит от уважения.",
				"effects": {"crown": 3, "mental": 1},
				"require_item": "smart_sword",
				"next": "arena_final",
			},
		],
	}


static func _arena_final() -> Dictionary:
	## Раунд 3: финал турнира / Apple-ветка
	return {
		"id": "arena_final",
		"bg": BG_ARENA,
		"speaker": "Корпоратив-арена · Финал",
		"text": "Финал: Чемпион прошлых спринтов — Барон Венчур в позолоченных латах. Ставка — звание Героя Квартала и билет в Замок.",
		"choices": [
			{
				"label": "Драться честно до конца",
				"art": CARD + "card_a2_arena_honest.png",
				"aside": "Кровь, пот, квартальный бонус.",
				"result": "Победа. Король репостит: «Наш герой закрыл спринт». Подписка на тебя оформлена публично.",
				"effects": {"health": -4, "gold": 30, "crown": 4, "people": 4},
				"main_quest": 3,
				"unlock": "castle_capital",
				"flag": "arena_champion",
				"next": "end",
			},
			{
				"label": "Песок в глаза барону",
				"art": CARD + "card_a2_arena_sand.png",
				"aside": "Грязный трюк, толстый кошелёк.",
				"result": "Победа. Народ орёт «читер». Корона всё равно ставит лайк.",
				"effects": {"health": -1, "gold": 30, "crown": 2, "people": -6},
				"main_quest": 3,
				"unlock": "castle_capital",
				"flag": "arena_champion",
				"next": "end",
			},
			{
				"label": "[Скрытый] Сэр Лаг на финале",
				"art": CARD + "card_sir_lag_hire.png",
				"aside": "Он закрывает тебя щитом… с задержкой 5 сек.",
				"result": "Лаг ловит удар вместо тебя. Толпа: «лаг компенсирован!» Ты — Герой Квартала.",
				"effects": {"health": -2, "gold": 30, "crown": 5, "people": 2},
				"require_flag": "companion_sir_lag",
				"main_quest": 3,
				"unlock": "castle_capital",
				"flag": "arena_champion",
				"next": "end",
			},
			{
				"label": "[Скрытый] Ударить Apple-Калибуром",
				"art": CARD + "card_a2_apple_calibur.png",
				"aside": "Подписка ещё активна… кажется.",
				"result": "Клинок вспыхивает — и экран подписки мигает прямо над ареной.",
				"effects": {},
				"require_item": "apple_calibur",
				"next": "apple_curse",
			},
		],
	}


static func _apple_curse() -> Dictionary:
	return {
		"id": "apple_curse",
		"bg": BG_ARENA,
		"speaker": "Автосписание",
		"text": "Подписка на Apple-Калибур истекла прямо на арене. Финал турнира превращается в демо-версию боли.",
		"require_item": "apple_calibur",
		"skip_to": "end",
		"choices": [
			{
				"label": "Осознать SaaS",
				"art": CARD + "card_a2_apple_calibur.png",
				"aside": "Меч гаснет. Толпа не гаснет.",
				"result": "Вас избивают. Меч сломан. Подписка — зло. Но король всё равно зовёт в Замок: «контент топ».",
				"effects": {"health": -6, "crown": -4, "people": -6},
				"remove_item": "apple_calibur",
				"flag": "apple_broke",
				"main_quest": 3,
				"unlock": "castle_capital",
				"next": "end",
			},
		],
	}
