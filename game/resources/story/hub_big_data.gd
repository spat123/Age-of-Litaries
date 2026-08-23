extends RefCounted
class_name HubBigData
## Хаб столицы после Акта 2: таверна Ctrl+Ale, доска, кот, утка-кликер.

const BG_CITY := "res://assets/art/backgrounds/bg_act2_city.png"
const BG_TAVERN := "res://assets/art/backgrounds/bg_act2_tavern.png"
const BG_GUILDS := "res://assets/art/backgrounds/bg_act2_guilds.png"
const CARD := "res://assets/art/cards/"


static func hub() -> Array:
	return [
		{
			"id": "hub",
			"bg": BG_CITY,
			"speaker": "Биг Дата",
			"text": "Столица гудит. Можно снова в сюжет… или залипнуть в хабе: таверна, доска объявлений, кот-менеджер и утка-кликер.",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] Таверна Ctrl+Ale",
					"art": CARD + "card_ignore_sleep.png",
					"speaker": "Бармен",
					"bg": BG_TAVERN,
					"branch_text": "Пахнет элем и выгоранием. На стене: «Wi-Fi пароль: password123».",
					"choices": [
						{
							"label": "Кружка эля (−3💰, +2🧠)",
							"art": CARD + "card_ignore_sleep.png",
							"aside": "Локальный Lo-Fi.",
							"result": "Менталочка теплеет. KPI кажется дальше.",
							"effects": {"gold": -3, "mental": 2},
							"require_gold": 3,
							"next": "hub",
						},
						{
							"label": "Сплетни у стойки",
							"art": CARD + "card_podcast.png",
							"aside": "Крестьяне шепчут про дракона.",
							"result": "+к народу. Слухи про VPN-сосну.",
							"effects": {"people": 2, "mental": 1},
							"next": "hub",
						},
						{
							"kind": "return",
							"label": "Выйти на площадь",
							"art": CARD + "card_relocate_forest.png",
							"next": "hub",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Доска объявлений Короля",
					"art": CARD + "card_a2_hr_lamp.png",
					"speaker": "Доска",
					"branch_text": "Берёста: «Требуется герой. Опыт с драконами. Зарплата — идея.» Рядом — «Glassdoor Средневековья»: анонимные отзывы на гильдии и Короля.",
					"choices": [
						{
							"label": "Прочитать вакансию",
							"art": CARD + "card_act0_loyal.png",
							"aside": "Дедлайн вчера.",
							"result": "Мотивация падает. Корона кивает одобрительно.",
							"effects": {"mental": -1, "crown": 2},
							"next": "hub",
						},
						{
							"kind": "narrative",
							"label": "[Сюжет] Glassdoor на бересте",
							"art": CARD + "card_podcast.png",
							"speaker": "Анонимные отзывы",
							"branch_text": "Доска гудит. Кто-то уже поставил Королю две звезды из пяти.",
							"choices": [
								{
									"label": "Воины: ★☆☆☆☆",
									"art": CARD + "card_a2_warriors_door.png",
									"aside": "«Овертаймы на кабанах. ДМС нет. Значок вместо зарплаты.»",
									"result": "Подсказка усвоена: гильдия воинов бьёт по ❤️. Народ кивает.",
									"effects": {"people": 1, "mental": 1},
									"next": "hub",
								},
								{
									"label": "Маги: ★★★☆☆",
									"art": CARD + "card_a2_mages_door.png",
									"aside": "«Легаси-руны, мана в 404, платят криптой.»",
									"result": "Звучит как баг на проде. Мозг готовится.",
									"effects": {"mental": 1, "inquisition": 1},
									"next": "hub",
								},
								{
									"label": "Король-CEO: ★★☆☆☆",
									"art": CARD + "card_a2_hr_lamp.png",
									"aside": "«Опцион на полцарства. По факту — сова и KPI.»",
									"result": "Хвалебный комментарий от страха. Корона слышит.",
									"effects": {"crown": 2, "cringe": 1},
									"flag": "glassdoor_praised_king",
									"next": "hub",
								},
								{
									"label": "Слить инсайд (разгром)",
									"art": CARD + "card_threat_stick.png",
									"aside": "Пишешь: «Дедлайн вчера, бюджет — идея».",
									"result": "Народ репостит. Аудитор уже ищет автора.",
									"effects": {"people": 4, "crown": -8, "inquisition": -4},
									"flag": "glassdoor_leak",
									"next": "hub",
								},
								{
									"kind": "return",
									"label": "Закрыть бересту",
									"art": CARD + "card_skip.png",
									"next": "hub",
								},
							],
						},
						{
							"label": "Оторвать объявление про кота",
							"art": CARD + "card_act0_loot.png",
							"aside": "Награда: рыба и уважение.",
							"result": "Флаг «ищу кота». Кот-менеджер будет рад.",
							"effects": {"people": 1},
							"flag": "looking_for_cat",
							"next": "hub",
						},
						{
							"kind": "return",
							"label": "Отойти",
							"art": CARD + "card_skip.png",
							"next": "hub",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Кот-Менеджер",
					"art": CARD + "card_act0_twerk.png",
					"speaker": "Кот-Менеджер / Архитектор",
					"branch_text": "Кот в галстуке листает бересту-канбан: «Мяу. Дедлайны. Стейкхолдеры.» Это тот самый код-ревьюер с плеча — пока на фрилансе в хабе.",
					"choices": [
						{
							"label": "Погладить (риск)",
							"art": CARD + "card_act0_loot.png",
							"aside": "Он царапает KPI.",
							"result": "−1❤️, но +к менталке от милоты.",
							"effects": {"health": -1, "mental": 2},
							"next": "hub",
						},
						{
							"label": "[Скрытый] Вернуть объявление",
							"art": CARD + "card_act0_loyal.png",
							"aside": "«Я искал тебя.»",
							"result": "Кот мурлычет и даёт бафф: KPI +1 день.",
							"effects": {"mental": 3, "people": 2},
							"require_flag": "looking_for_cat",
							"flag": "met_cat_manager",
							"next": "hub_kpi_bonus",
						},
						{
							"label": "Спросить про дедлайн",
							"art": CARD + "card_a2_hr_lamp.png",
							"aside": "Он указывает лапой на солнце.",
							"result": "«Мяу» значит «успей до заката спринта».",
							"effects": {"mental": -1, "crown": 1},
							"next": "hub",
						},
						{
							"kind": "return",
							"label": "Уйти",
							"art": CARD + "card_skip.png",
							"next": "hub",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Утка-кликер",
					"art": CARD + "card_a2_tinder.png",
					"speaker": "Утка",
					"branch_text": "На площади резиновая утка. Табличка: «Кликай. Получай. Не думай.»",
					"choices": [
						{
							"label": "Клик ×1",
							"art": CARD + "card_agu.png",
							"aside": "Кря.",
							"result": "+1💰. Дофамин микродозой.",
							"effects": {"gold": 1},
							"next": "hub",
						},
						{
							"label": "Клик ×10 (кринж)",
							"art": CARD + "card_donate_cry.png",
							"aside": "Ты кликаешь как маньяк.",
							"result": "+8💰 и 😳+1. Народ смотрит.",
							"effects": {"gold": 8, "cringe": 1, "people": -1},
							"next": "hub",
						},
						{
							"label": "Сломать утку",
							"art": CARD + "card_threat_stick.png",
							"aside": "Антикликерская ярость.",
							"result": "Утка пищит ошибкой 404. Стража недовольна.",
							"effects": {"crown": -2, "mental": 1},
							"next": "hub",
						},
						{
							"kind": "return",
							"label": "Хватит кликать",
							"art": CARD + "card_skip.png",
							"next": "hub",
						},
					],
				},
				{
					"label": "Идти к замку / дальше по сюжету",
					"art": CARD + "card_relocate_forest.png",
					"aside": "Хаб подождёт.",
					"result": "Ты выбираешь карту. Биг Дата останется.",
					"effects": {},
					"next": "end",
				},
				{
					"kind": "clarify",
					"label": "Чего?",
					"art": CARD + "card_act0_confused.png",
					"speaker": "Рассказчик",
					"clarify_text": "Рассказчик (шепотом): Это побочный хаб столицы. Можно пить эль, кликать утку и гладить кота-менеджера, пока KPI не сгорит. Сюжет — через «идти дальше» или другие точки карты.",
				},
			],
		},
		{
			"id": "hub_kpi_bonus",
			"bg": BG_GUILDS,
			"speaker": "Кот-Менеджер",
			"text": "Кот ставит лапу на календарь. Один день дедлайна возвращается.",
			"choices": [
				{
					"label": "Поблагодарить",
					"art": CARD + "card_act0_loyal.png",
					"aside": "Мур.",
					"result": "KPI +1. Кот исчезает в канбане.",
					"effects": {},
					"kpi_bonus": 1,
					"next": "hub",
				},
			],
		},
	]
