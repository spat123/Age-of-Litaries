extends RefCounted
class_name Act1RoadBeats
## Акт 1.5 — Тракт Мемов: Лаг → Тролль → Инфоцыган.


const BG_ROAD_LAG := "res://assets/art/backgrounds/bg_act1_road_lag.png"
const BG_ROAD_TROLL := "res://assets/art/backgrounds/bg_act1_road_troll.png"
const BG_ROAD_CAMP := "res://assets/art/backgrounds/bg_act1_road_camp.png"
const CARD := "res://assets/art/cards/"


static func beats() -> Array:
	return [
		{
			"id": "sir_lag",
			"bg": BG_ROAD_LAG,
			"speaker": "Сэр Лаг",
			"text": "На обочине стоит рыцарь в тяжёлых доспехах. Он двигается рывками, раз в 5 секунд. «П-п-помоги… У м-меня высокий пинг… Я не могу дойти до Столицы».",
			"choices": [
				{
					"kind": "clarify",
					"label": "Чего?",
					"art": CARD + "card_act0_confused.png",
					"speaker": "Рассказчик",
					"clarify_text": "Рассказчик (шепотом): «Пинг» — это когда его доспех думает дольше, чем ты копаешь навоз. Он просит «Wi-Fi» — то есть подключить его железку к твоей коре с яблоком, чтобы перестал лагать. Бесплатный меч за техподдержку, если повезёт.",
				},
				{
					"label": "Нанять телохранителем (10 золота)",
					"art": CARD + "card_sir_lag_hire.png",
					"aside": "Контракт на танк с задержкой ввода.",
					"result": "Он берёт деньги. Атаки мимо, зато впитывает урон как губка.",
					"effects": {"gold": -10, "vital_bonus": 5},
					"require_gold": 10,
					"flag": "companion_sir_lag",
					"next": "troll_plaza",
				},
				{
					"label": "Ограбить лагающего рыцаря",
					"art": CARD + "card_sir_lag_rob.png",
					"aside": "Пинг работает в обе стороны. Карма тоже.",
					"result": "Ты снимаешь кошелёк. Он замечает это через минуту и орёт в пустоту.",
					"effects": {"gold": 15, "inquisition": -5, "people": -5},
					"next": "troll_plaza",
				},
				{
					"label": "Пройти мимо",
					"art": CARD + "card_sir_lag_ignore.png",
					"aside": "Сервер когда-нибудь перезагрузят. Или нет.",
					"result": "Ты игнорируешь его. Он так и остался стоять. Менталочка в норме.",
					"effects": {},
					"next": "troll_plaza",
				},
				{
					"label": "[Скрытый] Раздать Wi-Fi",
					"art": CARD + "card_phone_wifi.png",
					"aside": "4G-береста ловит один бар… иногда.",
					"result": "Доспех перестаёт лагать. Рыцарь клянётся в верности и отдаёт меч!",
					"effects": {"crown": 5, "item": "rusty_sword"},
					"require_item": "wooden_phone",
					"flag": "companion_sir_lag",
					"next": "troll_plaza",
				},
			],
		},
		{
			"id": "troll_plaza",
			"bg": BG_ROAD_TROLL,
			"speaker": "Тролль Платной Дороги",
			"text": "Вы подходите к мосту. На нём сидит жирный Тролль в будке «Толл-Плаза». «Проход платный! Гони 5 золотых или поставь лайк моей странице на бересте!»",
			"choices": [
				{
					"label": "Заплатить 5 золота",
					"art": CARD + "card_troll_pay.png",
					"aside": "Шлагбаум скрипит дороже совести.",
					"result": "Ты покорно отсчитываешь монеты. Тролль поднимает шлагбаум. Чувствуешь себя терпилой.",
					"effects": {"gold": -5, "mental": -1, "crown": 2},
					"require_gold": 5,
					"next": "infogypsy",
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Попытаться пройти силой",
					"art": CARD + "card_troll_fight.png",
					"speaker": "Тролль Платной Дороги",
					"branch_text": "Тролль смеётся, сотрясая мост: «А силёнок хватит, зумер?»",
					"choices": [
						{
							"label": "Полезть с кулаками",
							"art": CARD + "card_troll_fight.png",
							"aside": "Кулаки vs масса. Физика на стороне тролля.",
							"result": "Тролль просто садится на тебя. Буквально. Ты еле выползаешь из-под его зада.",
							"effects": {"health": -4, "people": 3},
							"next": "infogypsy",
						},
						{
							"label": "[Скрытый] Достать Ржавый Меч!",
							"art": CARD + "card_a2_buy_rusty.png",
							"aside": "Ржавчина убедительнее кулаков.",
							"result": "Ты тыкаешь тролля в пузо. Он визжит от страха подхватить столбняк и пропускает! Меч в зазубринах, но цел.",
							"effects": {"health": -1, "crown": 2},
							"require_item": "rusty_sword",
							"next": "infogypsy",
						},
					],
				},
				{
					"label": "Поставить «лайк» (спам)",
					"art": CARD + "card_troll_like.png",
					"aside": "Кровавый отпечаток на бересте. Подписка оформлена.",
					"result": "Теперь каждый день почтовые голуби несут рекламу казино.",
					"effects": {"mental": -3, "people": -2},
					"next": "infogypsy",
				},
				{
					"label": "[Скрытый] Показать фольгу",
					"art": CARD + "card_foil_troll.png",
					"aside": "Ведро на голове — антирекламный щит.",
					"result": "Тролль понимает, что инфокурсы не продать, и брезгливо пропускает бесплатно.",
					"effects": {"mental": 2},
					"require_item": "foil_hat",
					"next": "infogypsy",
				},
			],
		},
		{
			"id": "infogypsy",
			"bg": BG_ROAD_CAMP,
			"speaker": "Торговец Инфоцыганъ",
			"text": "Вы разбили лагерь. Из кустов выходит богато одетый бард. «Привет! Хочешь узнать, как я заработал этот камзол, сидя у костра 2 часа в день? Успешный успех сам себя не скачает!»",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] Поинтересоваться товаром",
					"art": CARD + "card_infogypsy_pass.png",
					"speaker": "Инфоцыганъ",
					"branch_text": "Бард достаёт блестящий свиток. «Это Базовый Боевой Пропуск! Удвоит харизму и откроет премиум-слоты. Всего 30 золотых!»",
					"choices": [
						{
							"kind": "clarify",
							"label": "Чего?",
							"art": CARD + "card_act0_confused.png",
							"clarify_text": "Рассказчик (шепотом): Он пытается продать тебе кусок бересты, обещая, что бабы будут любить тебя сильнее, а карманы станут шире. Развод на золото, классика.",
							"speaker": "Рассказчик"
						},
						{
							"label": "Купить Боевой Пропуск (30)",
							"art": CARD + "card_infogypsy_pass.png",
							"aside": "Блеск деревяшки ослепляет разум.",
							"result": "Деньги ушли. Взамен — деревяшка «Мамонт». Слотов не открылось. В бэклог: «Я — крипто-инвестор».",
							"no_gold_result": "У вас нет золота на пропуск. Бард цокает: «Приходи, когда mindset пополнит кошелёк».",
							"effects": {"gold": -30, "mental": -5, "item": "useless_pass", "pen": "crypto"},
							"require_gold": 30,
							"flag": "infogypsy_scammed",
							"unlock": "big_data",
							"next": "end",
						},
						{
							"label": "Попросить подешевле (15)",
							"art": CARD + "card_infogypsy_potion.png",
							"aside": "Зелье харизмы пахнет уксусом и амбициями.",
							"result": "На вкус как уксус. Ты так громко рыгаешь, что волки убегают.",
							"no_gold_result": "У вас нет золота даже на «подешевле». Бард уходит питчить волкам.",
							"effects": {"gold": -15, "health": -1, "people": 3, "pen": "crypto"},
							"require_gold": 15,
							"flag": "infogypsy_scammed",
							"unlock": "big_data",
							"next": "end",
						},
						{
							"kind": "return",
							"label": "Отказаться",
							"art": CARD + "card_skip.png",
							"next": "infogypsy"
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Спросить про подвох",
					"art": CARD + "card_infogypsy_disciple.png",
					"speaker": "Инфоцыганъ",
					"branch_text": "«Никакого подвоха! Я начинал грязекопателем. Потом изменил mindset! Покупай гайд или умри в нищете!»",
					"choices": [
						{
							"label": "Стать учеником (бесплатно)",
							"art": CARD + "card_infogypsy_disciple.png",
							"aside": "Ночь лекций про энергию денег. Утро без сапог.",
							"result": "Бард исчезает с твоими сапогами. Зато ты полон мотивации.",
							"effects": {"health": -2, "gold": -10, "mental": 4},
							"flag": "infogypsy_disciple",
							"unlock": "big_data",
							"next": "end",
						},
						{
							"label": "Разоблачить и пригрозить инквизицией",
							"art": CARD + "card_infogypsy_expose.png",
							"aside": "Слово «HR» действует сильнее пыток.",
							"result": "Бард бледнеет: «Ладно-ладно, только не HR!» Бросает мелочь и убегает в кусты.",
							"effects": {"gold": 15, "inquisition": 3, "crown": 2},
							"flag": "infogypsy_exposed",
							"unlock": "big_data",
							"next": "end",
						},
					],
				},
				{
					"kind": "narrative",
					"label": "[Сюжет] Взять тяжёлую палку",
					"art": CARD + "card_threat_stick.png",
					"speaker": "Инфоцыганъ",
					"branch_text": "Бард сглатывает. «Эй, у тебя мышление бедняка… Насилие не решает проблем бизнеса!»",
					"choices": [
						{
							"label": "Прогнать его прочь",
							"art": CARD + "card_threat_stick.png",
							"aside": "Токсичная среда — это когда палка длиннее питча.",
							"result": "Бард убегает, крича про токсичность. Ты спишь спокойно у костра.",
							"effects": {"mental": 2, "inquisition": 2},
							"flag": "infogypsy_chased",
							"unlock": "big_data",
							"next": "end",
						},
						{
							"label": "[Скрытый] Ударить смартфоном!",
							"art": CARD + "card_infogypsy_phone.png",
							"aside": "Кора с яблоком входит в критический удар.",
							"result": "Смартфон разлетается в щепки. Инфоцыган без сознания. Ты лутаешь камзол.",
							"effects": {"health": -1, "gold": 25, "people": -3, "item": "infogypsy_coat"},
							"require_item": "wooden_phone",
							"remove_item": "wooden_phone",
							"flag": "infogypsy_robbed",
							"unlock": "big_data",
							"next": "end",
						},
					],
				},
			],
		},
	]
