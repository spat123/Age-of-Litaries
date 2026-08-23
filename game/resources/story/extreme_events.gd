extends RefCounted
class_name ExtremeEvents
## Судный День + KPI + Король Кринжа (авто на карте).

const BG_HR := "res://assets/art/backgrounds/bg_act2_hr.png"
const BG_RIOT := "res://assets/art/backgrounds/bg_event_riot.png"
const BG_KPI := "res://assets/art/backgrounds/bg_event_kpi.png"
const CARD := "res://assets/art/cards/"


static func people_riot() -> Array:
	return [
		{
			"id": "riot",
			"bg": BG_RIOT,
			"speaker": "Бунт Народа",
			"text": "Крестьяне приносят вас на вилах к воротам Замка. «Веди нас! Ты наш новый CEO!»",
			"choices": [
				{
					"label": "«Я не лидер, у меня лапки!»",
					"art": CARD + "card_act0_confused.png",
					"aside": "Толпа разочарованно вздыхает.",
					"result": "Вас роняют в лужу. Шкала народа сбрасывается.",
					"effects": {"set_people": 50, "health": -2, "cringe": 1},
					"next": "end",
				},
				{
					"label": "Возглавить революцию!",
					"art": CARD + "card_a2_punch_guard.png",
					"aside": "Штурм! Арбалеты короля уже наведены.",
					"result": "Стража расстреливает вас. Слишком много демократии.",
					"effects": {},
					"game_over": "too_much_democracy",
					"next": "end",
				},
			],
		},
	]


static func inq_wrath() -> Array:
	return [
		{
			"id": "wrath",
			"bg": BG_HR,
			"speaker": "Аудитор Инквизиции",
			"text": "Ночью в палатку врывается элитный Аудитор. «Ваш баланс духовности отрицательный. Пройдёмте на костёр».",
			"choices": [
				{
					"label": "Оплатить индульгенцию (50)",
					"art": CARD + "card_bribe_flatfoot.png",
					"aside": "Чек пахнет ладаном и банкротством.",
					"result": "Спасены, но теперь нищие. ⛪ = 50.",
					"effects": {"gold": -50, "set_inquisition": 50},
					"require_gold": 50,
					"next": "end",
				},
				{
					"label": "Попытаться сбежать",
					"art": CARD + "card_relocate_forest.png",
					"aside": "Спотыкаетесь о собственные штаны.",
					"result": "Вас сжигают. Не прошли аудит.",
					"effects": {},
					"game_over": "audit_failed",
					"next": "end",
				},
			],
		},
	]


static func people_cancel() -> Array:
	return [
		{
			"id": "cancel",
			"bg": BG_RIOT,
			"speaker": "Культура отмены",
			"text": "Народ = 0. У колодца уже мем: «Сэр Баг? Не, мы его отменили». Вилы смотрят в твою сторону.",
			"choices": [
				{
					"label": "Извиниться в stories",
					"art": CARD + "card_act0_confused.png",
					"aside": "Поздно. Скриншоты уже в берестяном чате.",
					"result": "Вас выгоняют в Пустоши. Бан в реальности.",
					"effects": {},
					"game_over": "cancelled",
					"next": "end",
				},
			],
		},
	]


static func inq_monk() -> Array:
	return [
		{
			"id": "monk",
			"bg": BG_HR,
			"speaker": "Инквизиция",
			"text": "Инквизиция = 100. Вас бреют налысо и вручают рясу без Wi-Fi. «Принудительный постриг. Свобода воли отозвана.»",
			"choices": [
				{
					"label": "Принять постриг",
					"art": CARD + "card_act0_loyal.png",
					"aside": "Монастырь ждёт. Slack отключён навсегда.",
					"result": "GAME OVER: Монастырь без пароля от роутера.",
					"effects": {},
					"game_over": "monk_mode",
					"next": "end",
				},
			],
		},
	]


static func crown_execute() -> Array:
	return [
		{
			"id": "execute",
			"bg": BG_RIOT,
			"speaker": "Король-CEO",
			"text": "Корона = 0. Приказ без appeal: «Сотрудник токсичен. Казнь в этот же спринт.»",
			"choices": [
				{
					"label": "Подписать round-up",
					"art": CARD + "card_a2_hr_lamp.png",
					"aside": "HR кивает. Топор уже в календаре.",
					"result": "Казнь за измену KPI. Без appeal.",
					"effects": {},
					"game_over": "executed",
					"next": "end",
				},
			],
		},
	]


static func crown_exile() -> Array:
	return [
		{
			"id": "exile",
			"bg": BG_RIOT,
			"speaker": "Король-CEO",
			"text": "Корона = 100. «Ты слишком хорош. Повышаю до Старшего Младшего Помощника и ссылаю в убыточный филиал.» Народ уже несёт вилы: слишком лоялен тирану.",
			"choices": [
				{
					"label": "Принять повышение в Сибирь",
					"art": CARD + "card_act0_loyal.png",
					"aside": "Реструктуризация. Филиал без бюджета.",
					"result": "Ссылка. Народ не прощает. Вилы догоняют в дороге.",
					"effects": {},
					"game_over": "tyrant_revolt",
					"next": "end",
				},
			],
		},
	]


static func kpi_deadline() -> Array:
	return [
		{
			"id": "kpi",
			"bg": BG_KPI,
			"speaker": "Сова-Курьер",
			"text": "Небо темнеет. Гигантская сова с письмом, заверенным кровью Короля-CEO.",
			"choices": [
				{
					"label": "Прочитать уведомление о KPI",
					"art": CARD + "card_a2_apple_calibur.png",
					"aside": "Расторжение контракта. Срыв сроков.",
					"result": "Сова уносит вас в HR на переработку. Уволен из Жизни.",
					"effects": {},
					"game_over": "kpi_fired",
					"next": "end",
				},
			],
		},
	]


static func cringe_king() -> Array:
	return [
		{
			"id": "cringe_king",
			"bg": "res://assets/art/backgrounds/bg_act2_arena.png",
			"speaker": "Король-CEO",
			"text": "Вы накопили 10 очков кринжа. Король в восторге: «Гений эпатажа! Бренд-Менеджер королевства — это ты!»",
			"choices": [
				{
					"label": "Принять корону кринжа",
					"art": CARD + "card_act0_twerk.png",
					"aside": "Роскошь. Все вас ненавидят. Идеальный fit.",
					"result": "Титры. Достижение «Король Кринжа». Живёте в роскоши под хейт.",
					"effects": {"gold": 100, "people": -20, "crown": 10},
					"flag": "ending_cringe_king",
					"next": "end",
				},
			],
		},
	]


static func microloans() -> Array:
	return [
		{
			"id": "microloans",
			"bg": "res://assets/art/backgrounds/bg_act1_dig.png",
			"speaker": "Гоблин-Коллектор",
			"text": "Кошелёк пуст. Из кустов выскакивает гоблин в дешёвом пиджаке: «Одобрено за 5 секунд! Берёшь займ покрыть долг?»",
			"choices": [
				{
					"label": "Подписать договор не глядя",
					"art": CARD + "card_bribe_flatfoot.png",
					"aside": "Мелкий шрифт кусается.",
					"result": "Долг закрыт. Каждый ход −1💰, а если нет золота — −1❤️. Дебафф «Кредит».",
					"effects": {"set_gold": 0, "credit": true},
					"next": "end",
				},
				{
					"label": "Убежать от коллектора",
					"art": CARD + "card_a2_arena_sand.png",
					"aside": "Бита «Пени и Штрафы».",
					"result": "Избивают. Долг аннулирован. Половина здоровья — нет.",
					"effects": {"set_gold": 0, "health": -5, "cringe": 1, "credit": false},
					"next": "end",
				},
				{
					"label": "[Скрытый] Показать Иск к Реальности",
					"art": CARD + "card_a2_lawyer_owl.png",
					"aside": "Гоблин читает… и седеет.",
					"result": "Растворяется. Долг списан как баг системы!",
					"effects": {"set_gold": 0, "mental": 5, "crown": 2, "credit": false},
					"require_item": "reality_lawsuit",
					"remove_item": "reality_lawsuit",
					"next": "end",
				},
			],
		},
	]
