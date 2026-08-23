extends RefCounted
class_name RandomEncounters
## Случайные встречи на глобальной карте (канон random_encounters_and_deaths.md).

const BG_ROAD := "res://assets/art/backgrounds/bg_act2_forest.png"
const BG_CITY := "res://assets/art/backgrounds/bg_act2_city.png"
const CARD := "res://assets/art/cards/"


static func pool_ids() -> Array[StringName]:
	return [&"random_rtx", &"random_rain_tax", &"random_plantain_scam", &"random_api_fatal"]


static func get_beats(id: StringName) -> Array:
	match id:
		&"random_rtx":
			return _rtx()
		&"random_rain_tax":
			return _rain()
		&"random_plantain_scam":
			return _plantain()
		&"random_api_fatal":
			return _api()
		_:
			return []


static func _rtx() -> Array:
	return [
		{
			"id": "rtx",
			"bg": BG_ROAD,
			"speaker": "Купец RTX",
			"text": "Разбитая телега. Купец плачет: разбойники украли партию дефицитных RTX-кристаллов для Гильдии Магов.",
			"choices": [
				{
					"label": "Помочь собрать уцелевшие кристаллы",
					"art": CARD + "card_a2_mages_door.png",
					"aside": "Доброе дело и осколки в кармане купца.",
					"result": "Купец благодарит и сыпет золотом.",
					"effects": {"gold": 15, "people": 2},
					"next": "end",
				},
				{
					"label": "Забрать застрявший RTX-кристалл",
					"art": CARD + "card_steal_gem.png",
					"aside": "Я.Маркет уже пишет гневный отзыв.",
					"result": "Кристалл твой. Репутация — нет.",
					"effects": {"people": -5, "item": "rtx_crystal"},
					"next": "end",
				},
			],
		},
	]


static func _rain() -> Array:
	return [
		{
			"id": "rain",
			"bg": BG_CITY,
			"speaker": "Королевский Мытарь",
			"text": "Из-за дерева выходит Мытарь с зонтиком: «С вас налог на вчерашний дождь. Вода государственная!»",
			"choices": [
				{
					"label": "Заплатить (10 золота)",
					"art": CARD + "card_bribe_flatfoot.png",
					"aside": "Закон есть закон. Даже мокрый.",
					"result": "Злитесь, но платите.",
					"effects": {"gold": -10, "mental": -2},
					"allow_debt": true,
					"next": "end",
				},
				{
					"label": "«Я пользовался пиратским дождём»",
					"art": CARD + "card_threat_stick.png",
					"aside": "Теневой водосток. Приставы уже тут.",
					"result": "Дубинки по почкам. Пиратство наказуемо.",
					"effects": {"health": -4, "people": -2},
					"next": "end",
				},
			],
		},
	]


static func _plantain() -> Array:
	return [
		{
			"id": "plantain_scam",
			"bg": BG_ROAD,
			"speaker": "Странствующий лекарь",
			"text": "Лекарь торгует «Антивирусным подорожником с подпиской на обновления».",
			"choices": [
				{
					"label": "Съесть бесплатный пробник",
					"art": CARD + "card_a2_plantain.png",
					"aside": "Троян со слабительным.",
					"result": "Пробник оказался с вирусом-слабительным! В животе произошёл Stack Overflow (переполнение), а от смущающих звуков упало уважение народа.",
					"effects": {"health": -3, "people": -3},
					"next": "end",
				},
				{
					"label": "Избить лекаря",
					"art": CARD + "card_a2_arena_sand.png",
					"aside": "Варварски, но эффективно.",
					"result": "Забираете настоящий лист. Совесть кусается.",
					"effects": {"mental": -2, "people": -4, "item": "plantain"},
					"require_no_item": "plantain",
					"next": "end",
				},
				{
					"label": "Уйти мимо",
					"art": CARD + "card_relocate_forest.png",
					"aside": "Не сегодня.",
					"result": "Лекарь орёт про FOMO вслед.",
					"effects": {"mental": 1},
					"next": "end",
				},
			],
		},
	]


static func _api() -> Array:
	return [
		{
			"id": "api",
			"bg": BG_ROAD,
			"speaker": "SYSTEM",
			"text": "У обочины два мага спорят: скрестить Огонь и Воду «без переходника». Кто-то протягивает вам оба свитка.",
			"choices": [
				{
					"label": "Попытаться скрестить магии",
					"art": CARD + "card_a2_mages_door.png",
					"aside": "Конфликт версий.",
					"result": "FATAL ERROR. Вас разорвало на пиксели. Несовместимость API.",
					"effects": {},
					"game_over": "api_fatal",
					"next": "end",
				},
				{
					"label": "Отказаться и уйти",
					"art": CARD + "card_relocate_forest.png",
					"aside": "Сениорный инстинкт.",
					"result": "Маги взрываются без вас. +🧠 за здравый смысл.",
					"effects": {"mental": 2},
					"next": "end",
				},
				{
					"kind": "clarify",
					"label": "Чего?",
					"art": CARD + "card_act0_confused.png",
					"speaker": "Рассказчик",
					"clarify_text": "Рассказчик (шепотом): Если смешать несовместимые заклинания без адаптера — будет как DLL hell. Можно просто уйти.",
				},
			],
		},
	]
