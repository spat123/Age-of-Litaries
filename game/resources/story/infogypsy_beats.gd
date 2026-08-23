extends RefCounted
class_name InfogypsyBeats
## Все добивки по Инфоцыгану: рандом на карте + общие константы.

const BG_FOREST := "res://assets/art/backgrounds/bg_act2_forest.png"
const CARD := "res://assets/art/cards/"


## Рандом при перемещении по карте (Лес / Болото / к замку).
static func map_ambush() -> Array:
	return [
		{
			"id": "stump",
			"bg": BG_FOREST,
			"speaker": "Инфоцыганъ",
			"text": "На пеньке сидит бард в дорогих сапогах. «Хочешь узнать, как я заработал на этот лут, работая всего 2 часа в неделю? Купи мой гайд на бересте!»",
			"choices": [
				{
					"label": "Купить гайд (20 золота)",
					"art": CARD + "card_infogypsy_pass.png",
					"aside": "Береста пахнет FOMO и кедровым маслом.",
					"result": "На бересте: «Продавай гайды дуракам». Депрессия компилируется.",
					"effects": {"gold": -20, "mental": -6, "pen": "crypto"},
					"require_gold": 20,
					"flag": "infogypsy_map_met",
					"next": "end",
				},
				{
					"label": "[Скрытый] Послать ментальный блок (фольга)",
					"art": CARD + "card_foil_hat.png",
					"aside": "Ведро на голове гудит. Mindset отскакивает.",
					"result": "Ментальные волны бьют в фольгу. Бард роняет кошелёк и сваливает.",
					"effects": {"gold": 30, "mental": 5},
					"require_item": "foil_hat",
					"flag": "infogypsy_map_met",
					"next": "end",
				},
				{
					"label": "Уйти без покупки",
					"art": CARD + "card_threat_stick.png",
					"aside": "Не сегодня, бро.",
					"result": "Он орёт вслед про scarcity mindset. Ты уже далеко.",
					"effects": {"mental": 1},
					"flag": "infogypsy_map_met",
					"next": "end",
				},
				{
					"label": "Нанять «партнёром по воронке»",
					"art": CARD + "card_infogypsy_expose.png",
					"aside": "Контракт на сарказм и скидки на воздух.",
					"result": "Он клянётся в лояльности. Когда-нибудь пригодится в кофейне.",
					"effects": {"gold": -5, "crown": 1},
					"require_gold": 5,
					"flag": "companion_infogypsy",
					"next": "end",
				},
			],
		},
	]
