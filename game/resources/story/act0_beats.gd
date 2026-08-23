extends RefCounted
class_name Act0Beats
## Акт 0 — Early Access / туториал.


const BG := "res://assets/art/backgrounds/bg_act0_void.png"
const CARD := "res://assets/art/cards/"


static func beats() -> Array:
	return [
		{
			"id": "welcome",
			"bg": BG,
			"speaker": "Бог-Разработчик",
			"text": _welcome_text(),
			"choices": [
				{
					"label": "Где я? Почему пиксели?",
					"art": CARD + "card_act0_confused.png",
					"aside": "Гигантская бородатая голова зависает в пустоте и тяжело вздыхает.",
					"result": "«Ты — Сэр Баг. А в пикселях — потому что кончился бюджет на 3D-моделлера».",
					"effects": {"mental": -1},
					"next": "cringe_test",
				},
				{
					"label": "Скип диалогов! Где «В бой»?",
					"art": CARD + "card_act0_skip_fight.png",
					"aside": "Палец Бога щёлкает. В воздухе пахнет озоном и баг-репортом.",
					"result": "Тебя бьёт током. «Читай мануал, токсик!» Здесь лучше не дерзить.",
					"effects": {"health": -1, "crown": -2},
					"next": "cringe_test",
				},
				{
					"label": "Слава Архитектору! Готов служить!",
					"art": CARD + "card_act0_loyal.png",
					"aside": "Бог довольно кивает — редкий кадр лояльного билда.",
					"result": "«Вот это правильный майндсет. Держи аванс».",
					"effects": {"gold": 5, "crown": 2},
					"next": "cringe_test",
				},
			],
		},
		{
			"id": "cringe_test",
			"bg": BG,
			"speaker": "Бог-Разработчик",
			"text": "Есть Здоровье, Золото, Менталочка и три фракции. До нуля — труп. А теперь проверим Очки Кринжа: сделай что-нибудь глупое.",
			"choices": [
				{
					"label": "Тверк перед Богом",
					"art": CARD + "card_act0_twerk.png",
					"aside": "Пиксельный зад входит в Early Access. Мир отводит глаза.",
					"result": "Бог закрывает лицо. «Это было ужасно». +1 Кринж. Набери 3 — и сцена сгорит от стыда.",
					"effects": {"cringe": 1},
					"next": "end",
				},
				{
					"label": "Отказаться выполнять тупой приказ",
					"art": CARD + "card_act0_defy.png",
					"aside": "Консоль мигает. Админ не любит споры.",
					"result": "Бог снижает тебе здоровье командой. «Не спорь с админом».",
					"effects": {"health": -3},
					"next": "end",
				},
				{
					"label": "[Скрытый] Можно просто предмет?",
					"art": CARD + "card_act0_loot.png",
					"aside": "Небесная Канцелярия шепчет: у тебя уже куплен стартовый бафф.",
					"result": "Бог лениво кидает кусок коры. «На, подавись лутом».",
					"effects": {"item": "wooden_phone"},
					"require_flag": "legacy_loot",
					"next": "end",
				},
			],
		},
	]


static func _welcome_text() -> String:
	var base := "О, ещё один тестер скомпилировался. Я Бог-Разработчик. Средневековье %s.\nТебя уже подписали на пробную «Жизнь+» без галочки согласия. Задача — понять, чья это подписка… и не умереть до релиза." % GameState.build_version_label()
	if GameState.run_index >= 2:
		base += "\n\n«Стоп. Merge conflict. Мы это уже компилировали. Пелёнки в стирке кончились, джун. В этот раз хотя бы EULA прочитай.»"
	return base
