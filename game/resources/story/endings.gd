extends RefCounted
class_name EndingBeats
## Спец-концовки до Небесной HR (банкротство / Ctrl+Ale / подписка души).

const BG_CITY := "res://assets/art/backgrounds/bg_act2_city.png"
const BG_TAVERN := "res://assets/art/backgrounds/bg_act2_tavern.png"
const BG_CAVE := "res://assets/art/backgrounds/bg_act3_cave.png"
const BG_VOID := "res://assets/art/backgrounds/bg_act0_void.png"
const CARD := "res://assets/art/cards/"


static func _to_hr_beat(system_text: String, aside: String, result: String) -> Dictionary:
	return {
		"id": "to_hr",
		"bg": BG_VOID,
		"speaker": "SYSTEM",
		"text": system_text,
		"choices": [
			{
				"label": "В Небесную канцелярию",
				"art": CARD + "card_act0_loyal.png",
				"aside": aside,
				"result": result,
				"effects": {},
				"next": "end",
			},
		],
	}


static func ctrl_ale() -> Array:
	return [
		{
			"id": "tavern",
			"bg": BG_TAVERN,
			"speaker": "Рассказчик",
			"text": "Менталочка упала в ноль. Ты отказываешься от квестов, KPI и драконов. На вывеске криво написано: «Ctrl+Ale».",
			"choices": [
				{
					"label": "Открыть таверну и жить",
					"art": CARD + "card_ignore_sleep.png",
					"aside": "Пиво вместо дедлайнов.",
					"result": "Концовка «Выгорел в Средневековье». Крестьяне ходят на эль. Король орёт без ответа. Титры пахнут хмелем.",
					"effects": {"mental": 1, "people": 3},
					"flag": "ending_ctrl_ale",
					"next": "to_hr",
				},
			],
		},
		_to_hr_beat(
			"Даже выгорание — это смерть с точки зрения Небесной HR. Грехи всё равно начислят.",
			"NG+ манит.",
			"Документы о выгорании подписаны кровью и элем."
		),
	]


static func bankruptcy() -> Array:
	return [
		{
			"id": "organs",
			"bg": BG_CITY,
			"speaker": "Рассказчик",
			"text": "Долг пробил дно. Алхимики из «Органы&Co» уже меряют тебя портновским метром.",
			"choices": [
				{
					"label": "Признать банкротство",
					"art": CARD + "card_a2_lawyer_owl.png",
					"aside": "ROI отрицательный. Навсегда.",
					"result": "Концовка «Банкротство». Тебя продали на органы. Из печени сделали эликсир продуктивности для СМП.",
					"effects": {},
					"flag": "ending_bankruptcy",
					"next": "to_hr",
				},
			],
		},
		_to_hr_beat(
			"Даже без печени душа обязана явиться в Небесную HR.",
			"Долги списывают… почти.",
			"Крипто-Грехи всё равно капают."
		),
	]


static func soul_sub() -> Array:
	return [
		{
			"id": "forever",
			"bg": BG_CAVE,
			"speaker": "Нотариус (эхо)",
			"text": "Ты умер. Титры идут. Но «Жизнь+» никто не отменял. Списания продолжаются.",
			"choices": [
				{
					"label": "Смотреть титры под автопродлением",
					"art": CARD + "card_a2_lawyer_owl.png",
					"aside": "Подписка навсегда.",
					"result": "Концовка «Подписка навсегда». Из загробной кассы капает −1💰/вечность. Юрист Логововъ недоступен.",
					"effects": {},
					"flag": "ending_soul_forever",
					"next": "to_hr",
				},
			],
		},
		_to_hr_beat(
			"Небесная HR тоже на подписке. Ирония закрыта.",
			"EULA бессмертна.",
			"Вы принимаете условия посмертно."
		),
	]
