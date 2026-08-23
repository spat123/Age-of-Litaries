extends RefCounted
class_name Act2Sides
## Сайды Акта 2: Лес Релокантов + Болото Апдейтов (+ подорожник).

const BG_FOREST := "res://assets/art/backgrounds/bg_act2_forest.png"
const BG_LAWYER := "res://assets/art/backgrounds/bg_act2_lawyer.png"
const BG_LORD := "res://assets/art/backgrounds/bg_act2_swamp_lord.png"
const BG_TEMPLE := "res://assets/art/backgrounds/bg_act2_temple.png"
const CARD := "res://assets/art/cards/"


static func forest() -> Array:
	return [
		{
			"id": "freelancers",
			"bg": BG_FOREST,
			"speaker": "Лагерь фрилансеров",
			"text": "Поляна. У костра суровые разбойники. Один не отрывается от бересты: «Мы работаем удалённо, грабим асинхронно. Ты по таске или просто мимо шёл?»",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] Ищу Юриста Логовова",
					"art": CARD + "card_a2_freelancers.png",
					"speaker": "Разбойник",
					"branch_text": "Кивает: «Он в дупле под VPN-сосной. Но к нему только по записи.»",
					"choices": [
						{
							"label": "Ускоренная запись (15 золота)",
							"art": CARD + "card_a2_freelancers.png",
							"aside": "Классика очередей.",
							"result": "Проводят без очереди. VIP для бедных.",
							"effects": {"gold": -15},
							"require_gold": 15,
							"next": "lawyer",
						},
						{
							"label": "[Скрытый] Бесполезный Пропуск",
							"art": CARD + "card_infogypsy_pass.png",
							"aside": "Премиум-аккаунт Инфоцыгана.",
							"result": "«О, премиум!» — расступаются уважительно.",
							"effects": {},
							"require_item": "useless_pass",
							"next": "lawyer",
						},
					],
				},
				{
					"label": "Собрать антивирусный подорожник",
					"art": CARD + "card_a2_plantain.png",
					"aside": "У костра растёт лечащая трава 1.0.",
					"result": "Сорвал лист. Пахнет апдейтом иммунитета.",
					"effects": {"item": "plantain"},
					"require_no_item": "plantain",
					"next": "freelancers_after_herb",
				},
				{
					"label": "Просто мимо",
					"art": CARD + "card_relocate_forest.png",
					"aside": "Не по таске.",
					"result": "Кивают и снова смотрят в бересту.",
					"effects": {"mental": 1},
					"unlock": "update_swamp",
					"next": "end",
				},
			],
		},
		{
			"id": "freelancers_after_herb",
			"bg": BG_FOREST,
			"speaker": "Лагерь фрилансеров",
			"text": "Подорожник в кармане. Разбойники всё ещё тут. Что дальше?",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] Ищу Юриста Логовова",
					"art": CARD + "card_a2_freelancers.png",
					"speaker": "Разбойник",
					"branch_text": "«Дупло под VPN-сосной. Только по записи.»",
					"choices": [
						{
							"label": "Ускоренная запись (15 золота)",
							"art": CARD + "card_a2_freelancers.png",
							"aside": "Плати — иди.",
							"result": "Без очереди к филину.",
							"effects": {"gold": -15},
							"require_gold": 15,
							"next": "lawyer",
						},
						{
							"label": "[Скрытый] Бесполезный Пропуск",
							"art": CARD + "card_infogypsy_pass.png",
							"aside": "Премиум решает.",
							"result": "Проход открыт.",
							"effects": {},
							"require_item": "useless_pass",
							"next": "lawyer",
						},
					],
				},
				{
					"label": "Уйти к болоту",
					"art": CARD + "card_relocate_forest.png",
					"aside": "Тропа к Апдейтам.",
					"result": "Лес редеет. Впереди кваканье с автотюном.",
					"effects": {},
					"unlock": "update_swamp",
					"next": "end",
				},
			],
		},
		{
			"id": "lawyer",
			"bg": BG_LAWYER,
			"speaker": "Юрист Логововъ",
			"text": "В дупле филин в очках. «Решаю карму и отписки от дьявольских контрактов. Что нужно?»",
			"choices": [
				{
					"label": "Расторгнуть Подписку на Душу",
					"art": CARD + "card_a2_lawyer_owl.png",
					"aside": "Отписка от «Жизнь+».",
					"result": "Печать стоит. Золото больше не списывается само.",
					"effects": {},
					"require_soul_sub": true,
					"clear_soul_sub": true,
					"unlock": "update_swamp",
					"next": "end",
				},
				{
					"label": "Иск к Реальности (50 золота)",
					"art": CARD + "card_a2_lawyer_owl.png",
					"aside": "Красная папка. Ломает четвёртую стену.",
					"result": "«Только в крайнем случае». Папка тёплая и злая.",
					"effects": {"gold": -50, "item": "reality_lawsuit"},
					"require_gold": 50,
					"unlock": "update_swamp",
					"next": "end",
				},
				{
					"label": "Ничего, просто совет",
					"art": CARD + "card_a2_lawyer_owl.png",
					"aside": "Консультация бесплатна. Почти.",
					"result": "«Не подписывай EULA без лупы». Мудро.",
					"effects": {"mental": 1},
					"unlock": "update_swamp",
					"next": "end",
				},
			],
		},
	]


static func swamp() -> Array:
	return [
		{
			"id": "lord_rollback",
			"bg": BG_LORD,
			"speaker": "Лорд Отката",
			"text": "Из трясины поднимается рыцарь — броня меняет цвет. «Я Лорд Отката! Хранитель старых версий! Сразись со мной!»",
			"choices": [
				{
					"kind": "narrative",
					"label": "[Сюжет] Достать оружие и атаковать",
					"art": CARD + "card_a2_lord_rollback.png",
					"speaker": "Бой",
					"branch_text": "Вы замахиваетесь мечом…",
					"choices": [
						{
							"kind": "narrative",
							"label": "Ударить сверху!",
							"art": CARD + "card_a2_lord_rollback.png",
							"speaker": "SYSTEM",
							"branch_text": "⚠ ОШИБКА 404: УДАР НЕ НАЙДЕН.\nЛорд хохочет: «Откатил сервер на 5 секунд! Выбирай снова!»\nКнопка «сверху» исчезла. Остался низкий удар.",
							"choices": [
								{
									"label": "Пнуть в голень!",
									"art": CARD + "card_a2_arena_sand.png",
									"aside": "Баг эксплуатации версии.",
									"result": "Он падает в болото и грузит обновления. Победа багом!",
									"effects": {"crown": 3, "gold": 20},
									"next": "patch_temple",
								},
							],
						},
					],
				},
				{
					"label": "Ничего не делать (AFK)",
					"art": CARD + "card_ignore_sleep.png",
					"aside": "Timeout strategy.",
					"result": "Он ждёт… ждёт… «AFK? Нечестно!» — и уходит под воду.",
					"effects": {"mental": 2},
					"next": "patch_temple",
				},
			],
		},
		{
			"id": "patch_temple",
			"bg": BG_TEMPLE,
			"speaker": "Храм Патча",
			"text": "На алтаре светящаяся дискета: «Патч 1.0. Исправляет все ошибки вашей жизни».",
			"choices": [
				{
					"label": "Взять Патч 1.0",
					"art": CARD + "card_a2_patch.png",
					"aside": "Тёплый. Гудит. Опасный.",
					"result": "Патч в кармане. Вместе с Иском к Реальности в финале — «Сброс Цивилизации».",
					"effects": {"item": "patch_1_0"},
					"flag": "has_patch_1_0",
					"next": "end",
				},
				{
					"label": "Оставить на алтаре",
					"art": CARD + "card_a2_patch.png",
					"aside": "Иногда патч хуже бага.",
					"result": "Уходишь. Дискета мигает обиженно.",
					"effects": {"mental": 1},
					"next": "end",
				},
			],
		},
	]
