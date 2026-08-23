extends Node
## Канон HUD: ❤️ Health · 🧠 Mental · 💰 Gold
## Скрыто: crown / inquisition / people (Судный День на карте при 0/100)
## Кринж: скрытый буфер run_absurd_moments (Гоблин-ПМ) + Σ cringe_lifetime (Король Кринжа)
## Meta: total_bugs_found, run_index (NG+ дежавю), crypto_sins

signal stats_changed
signal inventory_changed
signal flags_changed
signal game_over(reason: StringName)

enum Perk { NONE, MILLENNIAL, OBEDIENT, FREAK, VETERAN, RELOCANT }
enum Guild { NONE, WARRIORS, THIEVES, MAGES }
enum DragonStance { UNKNOWN, ENEMY, COACH, PARTNER, STARTUP, RELOCATE }

const VITAL_MAX := 10
const FACTION_MIN := 0
const FACTION_MAX := 100
const GOLD_DEBT_DEATH := -50
const ABSURD_GOBLIN_AT := 3
const CRINGE_KING_AT := 10
const KPI_START_DAYS := 7
const GOBLIN_NARRATOR_TURNS := 5

signal goblin_takeover_triggered

## Бонус к макс. здоровью (Сэр Лаг и т.п.) — до health!
var vital_bonus: int = 0
## Дебафф «Кредит» с микрозайма: −1💰/ход, иначе −1❤️
var credit_active: bool = false
## Дней до KPI (Акт 3); −1 при ходе по карте после открытия замка
var kpi_days: int = -1
## Meta: найденные баги за все забеги (суммируется в HR после прохождения)
var total_bugs_found: int = 0
## Скрытый буфер абсурда за забег → событие Гоблина-ПМ (сброс на пороге 3)
var run_absurd_moments: int = 0
## Σ кринжа за забег (не сбрасывается Гоблином) → Король Кринжа на карте
var cringe_lifetime: int = 0
## Номер забега (NG+). 1 = первый релиз в прод; растёт при reset_new_game.
var run_index: int = 0

var health: int = 10:
	set(v):
		health = clampi(v, 0, VITAL_MAX + vital_bonus)
		stats_changed.emit()
		_check_game_over()

var mental: int = 10:
	set(v):
		mental = clampi(v, 0, VITAL_MAX)
		stats_changed.emit()
		_check_game_over()

## Может быть отрицательным (долг).
var gold: int = 0:
	set(v):
		gold = v
		stats_changed.emit()
		_check_game_over()

var crown: int = 50:
	set(v):
		crown = clampi(v, FACTION_MIN, FACTION_MAX)
		stats_changed.emit()

var inquisition: int = 50:
	set(v):
		inquisition = clampi(v, FACTION_MIN, FACTION_MAX)
		stats_changed.emit()

var people: int = 50:
	set(v):
		people = clampi(v, FACTION_MIN, FACTION_MAX)
		stats_changed.emit()

## После события абсурда: Гоблин-ПМ комментирует N следующих ходов
var goblin_narrator_turns: int = 0

var inventory: Dictionary = {}
var perk: Perk = Perk.NONE
var guild: Guild = Guild.NONE
var dragon_stance: DragonStance = DragonStance.UNKNOWN
var soul_subscription: bool = false

var unlocked_locations: Array[StringName] = [&"lower_wifi"]
var current_location: StringName = &"lower_wifi"
var completed_timelines: Array[StringName] = []
var flags: Dictionary = {}
## После рандома на карте продолжить выбранную локацию.
var pending_map_timeline: StringName = &""
var pending_map_title: String = ""
## После микрозайма вернуться к next-биту текущего таймлайна.
var microloan_resume_next: String = ""
## Meta / наследие (переживает смерть)
var crypto_sins: int = 0
var legacy_buffs: Dictionary = {}  # strong_junior / it_dynasty / anti_scam
## Титулы NG+: unlocked_* навсегда; equipped_title на забег
var unlocked_titles: Array = []  # Array of String
var equipped_title: String = ""
## Ментальный бэклог: pending pens → cooking → compiled ideas
var backlog_pending: Array = []  # String pen ids without pen_ prefix
var backlog_cooking: String = ""
var backlog_turns_left: int = 0
var compiled_ideas: Dictionary = {}  # id -> true
## Сквозная арка «Подписка на Героя» (см. main_quest.md)
var main_quest_stage: int = 0
## Защита от повторного game_over / двойных грехов
var run_over: bool = false
var sins_awarded: bool = false


func _ready() -> void:
	stats_changed.emit()


func reset_new_game() -> void:
	## Полный вайп ранa; крипто-грехи, наследие и титулы сохраняются.
	var keep_sins := crypto_sins
	var keep_bugs := total_bugs_found
	var keep_runs := run_index
	var keep_buffs: Dictionary = legacy_buffs.duplicate()
	var keep_titles: Array = unlocked_titles.duplicate()
	var keep_equip := equipped_title
	health = 10
	mental = 10
	gold = 0
	crown = 50
	inquisition = 50
	people = 50
	run_absurd_moments = 0
	cringe_lifetime = 0
	goblin_narrator_turns = 0
	inventory.clear()
	perk = Perk.NONE
	guild = Guild.NONE
	dragon_stance = DragonStance.UNKNOWN
	soul_subscription = false
	vital_bonus = 0
	credit_active = false
	kpi_days = -1
	main_quest_stage = 0
	run_over = false
	sins_awarded = false
	unlocked_locations = [&"lower_wifi"]
	current_location = &"lower_wifi"
	completed_timelines.clear()
	flags.clear()
	pending_map_timeline = &""
	pending_map_title = ""
	microloan_resume_next = ""
	backlog_pending.clear()
	backlog_cooking = ""
	backlog_turns_left = 0
	compiled_ideas.clear()
	crypto_sins = keep_sins
	total_bugs_found = keep_bugs
	run_index = maxi(1, keep_runs + 1)
	legacy_buffs = keep_buffs
	unlocked_titles = keep_titles
	equipped_title = keep_equip
	for t in unlocked_titles:
		flags[StringName("title_unlocked_%s" % str(t))] = true
	_apply_legacy_buffs()
	_apply_equipped_title()
	stats_changed.emit()
	inventory_changed.emit()
	flags_changed.emit()


func _apply_legacy_buffs() -> void:
	if legacy_buffs.get("strong_junior", false):
		add_vital_bonus(3)
	if legacy_buffs.get("it_dynasty", false):
		add_item(&"wooden_phone")
		# Act 0: скрытый лут в туториале (если NG+ снова проходит Early Access)
		set_flag(&"legacy_loot", true)
		advance_main_quest(1)
	if legacy_buffs.get("anti_scam", false):
		set_flag(&"legacy_anti_scam", true)
	## Проклятые реликвии NG+ (плюс + минус)
	if legacy_buffs.get("medusa_glove", false):
		add_item(&"medusa_glove")
		set_flag(&"relic_medusa", true)
	if legacy_buffs.get("hourglass_debt", false):
		add_item(&"hourglass_debt")
		set_flag(&"relic_hourglass", true)
		gold += 25
		credit_active = true
	if legacy_buffs.get("jester_mask", false):
		add_item(&"jester_mask")
		set_flag(&"relic_jester", true)
		run_absurd_moments = maxi(run_absurd_moments, 1)
		cringe_lifetime = maxi(cringe_lifetime, 3)
	if legacy_buffs.get("sir_success_debuff", false):
		set_flag(&"sir_success_debuff", true)
		set_flag(&"debuff_sir_success", true)


func advance_main_quest(stage: int) -> void:
	if stage > main_quest_stage:
		main_quest_stage = stage
		stats_changed.emit()
		flags_changed.emit()


func main_quest_objective() -> String:
	match main_quest_stage:
		0:
			return "Подписка: уйди из Early Access живым"
		1:
			return "Подписка: кто шлёт тебе пуши?"
		2:
			return "Подписка: отмени автосписание судьбы"
		3:
			return "Подписка: Герой Квартала → Замок"
		4:
			return "Подписка: закрой тикет «Дракон»"
		_:
			return "Подписка: выбери финал «Жизнь+»"


func build_version_label() -> String:
	var n := maxi(1, run_index)
	return "v0.9.%db" % n


func guild_label() -> String:
	match guild:
		Guild.WARRIORS:
			return "Воины"
		Guild.THIEVES:
			return "Воры"
		Guild.MAGES:
			return "Маги"
		_:
			return ""


func diploma_summary(reason: StringName = &"") -> String:
	## Берестяной лист увольнения (экран GAME OVER / концовка).
	var perk_s := perk_label()
	if perk_s.is_empty():
		perk_s = "без перка"
	var guild_s := guild_label()
	if guild_s.is_empty():
		guild_s = "без гильдии"
	var rank := "Стажёр стыда"
	if cringe_lifetime >= 10:
		rank = "Испанский Стыд Столицы"
	elif cringe_lifetime >= 6:
		rank = "Мем деревни"
	elif cringe_lifetime >= 3:
		rank = "Неловкий джун"
	var lines: PackedStringArray = [
		"📜 КОРОЛЕВСКИЙ ПРИКАЗ ОБ УВОЛЬНЕНИИ ИЗ ЖИЗНИ (%s)" % build_version_label(),
		"Сотрудник: Сэр Баг, Почётный Джуниор-Грязекопатель",
		"Перк: %s · Гильдия: %s" % [perk_s, guild_s],
		"🪵 Закрыто таймлайнов (костыли): %d" % completed_timelines.size(),
		"😳 Накоплено кринжа Σ: %d  (%s)" % [cringe_lifetime, rank],
		"📜 Прочитано пунктов EULA: 0%",
		"💸 Финальный баланс: %d золотых" % gold,
	]
	if not String(reason).is_empty():
		lines.append("Причина увольнения: %s" % String(reason))
	return "\n".join(lines)


func pending_judgement_timeline() -> StringName:
	## Судный День на карте. Пусто = нет ивента.
	if people >= FACTION_MAX:
		return &"event_people_riot"
	if people <= FACTION_MIN:
		return &"event_people_cancel"
	if inquisition <= FACTION_MIN:
		return &"event_inq_wrath"
	if inquisition >= FACTION_MAX:
		return &"event_inq_monk"
	if crown <= FACTION_MIN:
		return &"event_crown_execute"
	if crown >= FACTION_MAX:
		return &"event_crown_exile"
	if cringe_lifetime >= CRINGE_KING_AT and not get_flag(&"ending_cringe_king"):
		return &"event_cringe_king"
	return &""


func _apply_equipped_title() -> void:
	match equipped_title:
		"toilet_lord":
			set_flag(&"title_toilet_lord", true)
		"apple_victim":
			set_flag(&"title_apple_victim", true)
		"terpila":
			set_flag(&"title_terpila", true)
		_:
			pass


func unlock_title(title_id: String) -> void:
	if title_id.is_empty() or title_id in unlocked_titles:
		return
	unlocked_titles.append(title_id)
	set_flag(StringName("title_unlocked_%s" % title_id), true)


func equip_title(title_id: String) -> bool:
	if not title_id.is_empty() and title_id not in unlocked_titles:
		return false
	flags.erase(&"title_toilet_lord")
	flags.erase(&"title_apple_victim")
	flags.erase(&"title_terpila")
	equipped_title = title_id
	_apply_equipped_title()
	stats_changed.emit()
	return true


func register_death_title(reason: StringName) -> void:
	match reason:
		&"death", &"eco_death":
			unlock_title("toilet_lord")
		&"collectors":
			unlock_title("terpila")
		_:
			pass
	if get_flag(&"apple_broke"):
		unlock_title("apple_victim")


func queue_backlog_pen(pen_id: String) -> void:
	## pen_id без префикса pen_ (crypto, bird_drones, matrix_lite, 5g)
	if pen_id.is_empty():
		return
	if compiled_ideas.get(pen_id, false):
		return
	if pen_id in backlog_pending or backlog_cooking == pen_id:
		return
	backlog_pending.append(pen_id)
	stats_changed.emit()


func start_backlog_cook(pen_id: String) -> bool:
	if backlog_cooking != "":
		return false
	if pen_id not in backlog_pending:
		return false
	backlog_pending.erase(pen_id)
	backlog_cooking = pen_id
	backlog_turns_left = 3
	stats_changed.emit()
	return true


func _tick_backlog() -> void:
	if backlog_cooking.is_empty():
		return
	mental -= 1
	backlog_turns_left -= 1
	if backlog_turns_left > 0:
		return
	var done := backlog_cooking
	backlog_cooking = ""
	compiled_ideas[done] = true
	set_flag(StringName("idea_%s" % done), true)
	## Пассивки инсайта
	match done:
		"crypto":
			set_flag(&"idea_crypto_passive", true)
		"matrix_lite", "matrix":
			set_flag(&"idea_matrix_passive", true)
		"bird_drones", "birds":
			set_flag(&"idea_birds_passive", true)
		"5g":
			set_flag(&"idea_5g_passive", true)
	stats_changed.emit()


func pen_label(pen_id: String) -> String:
	match pen_id:
		"crypto":
			return "Я — Крипто-Инвестор"
		"matrix_lite", "matrix":
			return "Мир — Матрица на минималках"
		"bird_drones", "birds":
			return "Птицы — дроны Короля"
		"5g":
			return "Все болезни от 5G-мельниц"
		_:
			return pen_id


func award_sins_for_death() -> int:
	if sins_awarded:
		return 0
	sins_awarded = true
	var gained := 5 + completed_timelines.size() * 5
	gained += mini(20, maxi(0, gold / 5))
	if has_item(&"reality_lawsuit"):
		gained += 10
	if has_item(&"patch_1_0"):
		gained += 10
	crypto_sins += gained
	return gained


func spend_sins(amount: int) -> bool:
	if crypto_sins < amount:
		return false
	crypto_sins -= amount
	stats_changed.emit()
	return true


func clear_legacy_buffs() -> void:
	legacy_buffs.clear()
	flags.erase(&"legacy_anti_scam")
	flags.erase(&"legacy_loot")
	flags.erase(&"relic_medusa")
	flags.erase(&"relic_hourglass")
	flags.erase(&"relic_jester")
	remove_item(&"medusa_glove")
	remove_item(&"hourglass_debt")
	remove_item(&"jester_mask")


## Спец-концовка до HR; пусто = обычный GAME OVER.
func special_ending_timeline(reason: StringName) -> StringName:
	if reason == &"burnout" and not get_flag(&"ending_ctrl_ale_seen"):
		set_flag(&"ending_ctrl_ale_seen", true)
		return &"ending_ctrl_ale"
	if reason == &"collectors" and not get_flag(&"ending_bankruptcy_seen"):
		set_flag(&"ending_bankruptcy_seen", true)
		return &"ending_bankruptcy"
	if soul_subscription and not get_flag(&"ending_soul_sub_seen"):
		set_flag(&"ending_soul_sub_seen", true)
		return &"ending_soul_sub"
	return &""


func special_ending_title(timeline: StringName) -> String:
	match timeline:
		&"ending_ctrl_ale":
			return "Таверна Ctrl+Ale"
		&"ending_bankruptcy":
			return "Банкротство"
		&"ending_soul_sub":
			return "Подписка навсегда"
		_:
			return "Концовка"


func prepare_hr_game_over(reason: StringName) -> Dictionary:
	register_death_title(reason)
	var gained := award_sins_for_death()
	return {
		"gained": gained,
		"sins": crypto_sins,
		"bugs": calculate_run_bug_score(),
		"flavor": death_flavor(reason),
		"diploma": diploma_summary(reason),
	}


func death_flavor(reason: StringName) -> String:
	match reason:
		&"death":
			return "Баг кишечника / смертельный удар. Лекари искали драйверы — не нашли."
		&"burnout":
			return "Ментальное выгорание. Вы обросли мхом: «Холм Грустного Рыцаря»."
		&"collectors":
			return "Ипотечное рабство. Сбер-Телега оформила вам рефинансирование под 300%."
		&"cancelled":
			return "Культура отмены. Вас стёрли из БД. Теперь вы НПС у забора."
		&"executed":
			return "Корона на нуле. Казнь без appeal."
		&"tyrant_revolt":
			return "Слишком лояльны тирану. Народ принёс вилы."
		&"monk_mode":
			return "Инквизиция 100. Свобода воли отозвана. Монастырь ждёт."
		&"eco_death":
			return "Эко-смузи vs дракон. FATAL ERROR."
		&"api_fatal":
			return "Несовместимость API: огонь + вода без переходника. Вас разорвало на пиксели."
		&"kpi_fired":
			return "Сова-курьер унесла в HR. Уволен из Жизни за срыв KPI."
		&"audit_failed":
			return "Аудит Инквизиции провален. Костёр уже тлеет."
		&"too_much_democracy":
			return "Слишком много демократии. Арбалеты короля не ошибаются."
		&"coward_fired":
			return "Побег с тикета. Король подписал приказ: трус уволен из сюжета."
		_:
			return "Смерть зафиксирована небесным тикетом (%s)." % String(reason)


func vital_max() -> int:
	return VITAL_MAX + vital_bonus


func add_vital_bonus(amount: int) -> void:
	vital_bonus = maxi(0, vital_bonus + amount)
	health = clampi(health + amount, 0, vital_max())
	stats_changed.emit()


func register_absurd_moment(amount: int = 1) -> void:
	## Абсурдный выбор: копится скрыто; на пороге — событие Гоблина-ПМ.
	if amount <= 0:
		return
	if perk == Perk.FREAK and amount > 0:
		amount = maxi(1, amount - 1)
	cringe_lifetime += amount
	run_absurd_moments += amount
	if run_absurd_moments >= ABSURD_GOBLIN_AT:
		run_absurd_moments = 0
		flags[&"pending_goblin_takeover"] = true
		goblin_takeover_triggered.emit()
	stats_changed.emit()


func clear_goblin_takeover_pending() -> void:
	run_absurd_moments = 0
	flags.erase(&"pending_goblin_takeover")
	stats_changed.emit()


func people_narrative_tone() -> String:
	if people >= 75:
		return "в деревне о тебе хорошо отзываются"
	if people >= 55:
		return "крестьяне к тебе нейтральны"
	if people >= 35:
		return "в чате избы о тебе шепчутся"
	return "тебя уже мемят у колодца"


func crown_narrative_tone() -> String:
	if crown >= 75:
		return "Корона считает тебя удобным винтиком"
	if crown >= 55:
		return "лояльность Короне на уровне «отработал спринт»"
	if crown >= 35:
		return "Корона на тебя косо смотрит"
	return "в протоколах ты уже «проблемный сотрудник»"


func calculate_run_bug_score() -> int:
	## Очки багов за забег: чем больше прошёл — тем выше счёт (для HR).
	var score := 0
	score += completed_timelines.size() * 3
	score += inventory.size() * 2
	score += main_quest_stage * 2
	for k in flags.keys():
		var sk := str(k)
		if sk.begins_with("pen_") or sk.begins_with("idea_") or sk.begins_with("title_"):
			score += 1
	score += run_absurd_moments
	score += cringe_lifetime
	return score


func award_bugs_for_run() -> int:
	if get_flag(&"bugs_awarded"):
		return 0
	set_flag(&"bugs_awarded", true)
	var gained := calculate_run_bug_score()
	total_bugs_found += gained
	stats_changed.emit()
	return gained


func is_goblin_narrator() -> bool:
	return goblin_narrator_turns > 0


func activate_goblin_narrator(turns: int = GOBLIN_NARRATOR_TURNS) -> void:
	goblin_narrator_turns = maxi(goblin_narrator_turns, turns)
	flags[&"goblin_narrator"] = true
	flags.erase(&"goblin_just_left")
	stats_changed.emit()


func tick_goblin_narrator() -> bool:
	## Минус 1 ход И.О. Рассказчика. true = Гоблин только что ушёл.
	if goblin_narrator_turns <= 0:
		return false
	goblin_narrator_turns -= 1
	if goblin_narrator_turns <= 0:
		goblin_narrator_turns = 0
		flags.erase(&"goblin_narrator")
		flags[&"goblin_just_left"] = true
		stats_changed.emit()
		return true
	stats_changed.emit()
	return false


func goblin_wrap(text: String) -> String:
	## Саркастичная рамка вокруг текста результата / aside.
	var prefixes: PackedStringArray = [
		"Ну и софт-скиллы… Короче: %s",
		"Записал в Jira как «Won't Fix». Итог: %s",
		"Стейкхолдеры в шоке. Факт: %s",
		"Бюджет сгорел, мораль на дне. Детали: %s",
		"По метрикам — epic fail. Дальше: %s",
		"Дедлайн горит, а ты вот это. Резюме: %s",
	]
	var i := int(Time.get_ticks_msec() / 17) % prefixes.size()
	return prefixes[i] % text


func on_perk_gained(new_perk: Perk) -> void:
	perk = new_perk
	match new_perk:
		Perk.VETERAN:
			add_vital_bonus(2)
		Perk.RELOCANT:
			unlock_location(&"relocant_forest")
			set_flag(&"perk_relocant", true)
		Perk.MILLENNIAL:
			set_flag(&"perk_millennial", true)
		Perk.OBEDIENT:
			set_flag(&"perk_obedient", true)
		Perk.FREAK:
			set_flag(&"perk_freak", true)
	stats_changed.emit()


func perk_label() -> String:
	match perk:
		Perk.MILLENNIAL:
			return "Миллениал"
		Perk.OBEDIENT:
			return "Послушный"
		Perk.FREAK:
			return "Фрик"
		Perk.VETERAN:
			return "Ветеран"
		Perk.RELOCANT:
			return "Релокант"
		_:
			return ""


## effects: health, mental, gold, crown, inquisition, people, vital_bonus, pen
## set_people / set_inquisition / set_gold — абсолютные значения
## устаревший ключ rating → people (миграция Акта 1)
func apply_effects(effects: Dictionary) -> void:
	if effects.has("vital_bonus"):
		add_vital_bonus(int(effects["vital_bonus"]))
	if effects.has("health"):
		health += _mod_health(int(effects["health"]))
	if effects.has("mental"):
		mental += _mod_mental(int(effects["mental"]))
	if effects.has("gold"):
		gold += _mod_gold(int(effects["gold"]))
	if effects.has("set_gold"):
		gold = int(effects["set_gold"])
	if effects.has("crown"):
		crown += _perk_mod("crown", int(effects["crown"]))
	if effects.has("inquisition"):
		inquisition += _perk_mod("inquisition", int(effects["inquisition"]))
	if effects.has("set_inquisition"):
		inquisition = int(effects["set_inquisition"])
	if effects.has("people"):
		people += _perk_mod("people", int(effects["people"]))
	if effects.has("set_people"):
		people = int(effects["set_people"])
	# legacy
	if effects.has("rating"):
		people += _perk_mod("people", int(effects["rating"]))
	if effects.has("pen"):
		var pid := str(effects["pen"])
		set_flag(StringName("pen_%s" % pid), true)
		queue_backlog_pen(pid)
	if effects.has("credit"):
		credit_active = bool(effects["credit"])
	if effects.has("cringe"):
		register_absurd_moment(int(effects["cringe"]))


func has_companion_lag() -> bool:
	return bool(get_flag(&"companion_sir_lag", false))


func _mod_health(delta: int) -> int:
	delta = _perk_mod("health", delta)
	if delta >= 0:
		return delta
	## Mitigation стакается, но максимум −2 к входящему урону (не «бессмертие»)
	var reduce := 0
	if has_companion_lag():
		reduce += 1
	if guild == Guild.WARRIORS:
		reduce += 1
	if get_flag(&"relic_medusa"):
		reduce += 1
	reduce = mini(2, reduce)
	return mini(-1, delta + reduce)


func _mod_mental(delta: int) -> int:
	delta = _perk_mod("mental", delta)
	## Маги: ментальный щит от багов
	if guild == Guild.MAGES and delta < 0:
		delta = mini(-1, delta + 1)
	return delta


func _mod_gold(delta: int) -> int:
	delta = _perk_mod("gold", delta)
	## Воры: +1 к приходу / −1 к расходу (мягче)
	if guild == Guild.THIEVES:
		if delta > 0:
			delta += 1
		elif delta < 0:
			delta = mini(-1, delta + 1)
	## Жертва Apple: цены рынка вдвое мягче
	if get_flag(&"title_apple_victim") and delta < 0:
		delta = int(ceili(float(delta) / 2.0))
	## Маска Шута: выигрыши золота ×1.5, но народные плюсы режутся в _perk_mod
	if get_flag(&"relic_jester") and delta > 0:
		delta = int(ceili(float(delta) * 1.5))
	return delta


func set_dragon_stance_from_str(s: String) -> void:
	match s:
		"enemy":
			dragon_stance = DragonStance.ENEMY
		"coach":
			dragon_stance = DragonStance.COACH
		"partner":
			dragon_stance = DragonStance.PARTNER
		"startup":
			dragon_stance = DragonStance.STARTUP
		"relocate":
			dragon_stance = DragonStance.RELOCATE
		_:
			dragon_stance = DragonStance.UNKNOWN


func try_protein_save() -> bool:
	## Протеиновый Гомункул: один раз спасает от смертельного HP.
	if not has_item(&"protein_homunculus"):
		return false
	remove_item(&"protein_homunculus")
	health = maxi(1, health)
	set_flag(&"protein_saved", true)
	stats_changed.emit()
	return true


func _perk_mod(stat: String, delta: int) -> int:
	if delta == 0:
		return 0
	## Титулы
	if get_flag(&"title_toilet_lord"):
		if stat == "people" and delta < 0:
			delta *= 2
	if get_flag(&"title_terpila"):
		if stat == "inquisition" and delta < 0:
			return 0
		if stat == "gold" and delta > 0:
			delta = maxi(1, delta - 1)
	## Перчатка Медузы: народ каменеет от страха — плюсы 🧑‍ вдвое слабее
	if get_flag(&"relic_medusa") and stat == "people" and delta > 0:
		delta = maxi(1, int(floor(float(delta) / 2.0)))
	## Маска Шута: народные плюсы не копятся (ты мем, не лидер)
	if get_flag(&"relic_jester") and stat == "people" and delta > 0:
		return 0
	## Скомпилированные загоны
	if get_flag(&"idea_matrix_passive") and stat == "mental" and delta < 0:
		return 0
	if get_flag(&"idea_birds_passive") and stat == "crown" and delta < 0:
		delta = mini(-1, delta + 1)
	if get_flag(&"idea_crypto_passive"):
		if stat == "gold" and delta > 0:
			delta *= 2
		if stat == "people" and delta > 0:
			return 0
	if get_flag(&"idea_5g_passive") and stat == "inquisition" and delta > 0:
		delta += 1
	match perk:
		Perk.MILLENNIAL:
			## Меньше ментального урона от абсурда; +1 кIncoming золоту
			if stat == "mental" and delta < 0:
				return mini(-1, delta + 1)
			if stat == "gold" and delta > 0:
				return delta + 1
		Perk.OBEDIENT:
			## Корона любит послушных; потери короны мягче
			if stat == "crown" and delta > 0:
				return delta + 1
			if stat == "crown" and delta < 0:
				return mini(-1, delta + 1)
		Perk.VETERAN:
			## Закалён: −1 к потере HP (не ниже −1)
			if stat == "health" and delta < 0:
				return mini(-1, delta + 1)
		Perk.RELOCANT:
			## Дешевле жить «на чемоданах»: траты золота −2 (мягче минус)
			if stat == "gold" and delta < 0:
				return mini(-1, delta + 2)
		Perk.FREAK:
			## Народ сторонится, менталка от абсурда почти не падает
			if stat == "mental" and delta < 0:
				return 0
			if stat == "people" and delta > 0:
				return maxi(0, delta - 1)
		_:
			pass
	return delta


func has_item(item_id: StringName) -> bool:
	return inventory.get(item_id, false) == true


func add_item(item_id: StringName) -> void:
	inventory[item_id] = true
	inventory_changed.emit()


func remove_item(item_id: StringName) -> void:
	if inventory.erase(item_id):
		inventory_changed.emit()


func set_flag(flag_id: StringName, value: Variant = true) -> void:
	flags[flag_id] = value
	flags_changed.emit()


func get_flag(flag_id: StringName, default: Variant = false) -> Variant:
	return flags.get(flag_id, default)


func unlock_location(location_id: StringName) -> void:
	if location_id not in unlocked_locations:
		unlocked_locations.append(location_id)


func mark_timeline_done(timeline_id: StringName) -> void:
	if timeline_id not in completed_timelines:
		completed_timelines.append(timeline_id)


const SAVE_PATH := "user://sir_bug_save.json"


func to_save_dict() -> Dictionary:
	return {
		"health": health,
		"mental": mental,
		"gold": gold,
		"crown": crown,
		"inquisition": inquisition,
		"people": people,
		"run_absurd_moments": run_absurd_moments,
		"cringe_lifetime": cringe_lifetime,
		"run_index": run_index,
		"total_bugs_found": total_bugs_found,
		"goblin_narrator_turns": goblin_narrator_turns,
		"inventory": inventory.duplicate(),
		"perk": perk,
		"guild": guild,
		"dragon_stance": dragon_stance,
		"soul_subscription": soul_subscription,
		"vital_bonus": vital_bonus,
		"unlocked_locations": unlocked_locations.duplicate(),
		"current_location": String(current_location),
		"completed_timelines": completed_timelines.duplicate(),
		"flags": flags.duplicate(),
		"crypto_sins": crypto_sins,
		"legacy_buffs": legacy_buffs.duplicate(),
		"unlocked_titles": unlocked_titles.duplicate(),
		"equipped_title": equipped_title,
		"backlog_pending": backlog_pending.duplicate(),
		"backlog_cooking": backlog_cooking,
		"backlog_turns_left": backlog_turns_left,
		"compiled_ideas": compiled_ideas.duplicate(),
		"main_quest_stage": main_quest_stage,
		"credit_active": credit_active,
		"kpi_days": kpi_days,
		"run_over": run_over,
		"sins_awarded": sins_awarded,
		"pending_map_timeline": String(pending_map_timeline),
		"pending_map_title": pending_map_title,
		"microloan_resume_next": microloan_resume_next,
	}


func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)


func save_game() -> bool:
	## Автосейв забега на диск (Continue из меню).
	var payload := {
		"version": 1,
		"saved_at": Time.get_datetime_string_from_system(false, true),
		"game": to_save_dict(),
	}
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f == null:
		push_warning("GameState: не удалось писать сейв (%s)" % FileAccess.get_open_error())
		return false
	f.store_string(JSON.stringify(payload, "\t"))
	f.close()
	return true


func load_game() -> bool:
	if not has_save():
		return false
	var f := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if f == null:
		push_warning("GameState: не удалось читать сейв")
		return false
	var text := f.get_as_text()
	f.close()
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("GameState: битый сейв")
		return false
	var root: Dictionary = parsed
	var data: Dictionary = root.get("game", root)
	if data.is_empty():
		return false
	from_save_dict(data)
	return true


func clear_save() -> void:
	if not has_save():
		return
	var dir := DirAccess.open("user://")
	if dir:
		dir.remove("sir_bug_save.json")


func from_save_dict(data: Dictionary) -> void:
	vital_bonus = int(data.get("vital_bonus", 0))
	health = int(data.get("health", 10))
	mental = int(data.get("mental", 10))
	gold = int(data.get("gold", 0))
	crown = int(data.get("crown", 50))
	inquisition = int(data.get("inquisition", 50))
	people = int(data.get("people", data.get("rating", 50)))
	run_absurd_moments = int(data.get("run_absurd_moments", data.get("cringe", 0)))
	cringe_lifetime = int(data.get("cringe_lifetime", 0))
	run_index = int(data.get("run_index", 0))
	total_bugs_found = int(data.get("total_bugs_found", total_bugs_found))
	goblin_narrator_turns = int(data.get("goblin_narrator_turns", 0))
	inventory = data.get("inventory", {}).duplicate()
	perk = int(data.get("perk", Perk.NONE)) as Perk
	guild = int(data.get("guild", Guild.NONE)) as Guild
	dragon_stance = int(data.get("dragon_stance", DragonStance.UNKNOWN)) as DragonStance
	soul_subscription = bool(data.get("soul_subscription", false))
	unlocked_locations.clear()
	for loc in data.get("unlocked_locations", ["lower_wifi"]):
		unlocked_locations.append(StringName(str(loc)))
	current_location = StringName(str(data.get("current_location", "lower_wifi")))
	completed_timelines.clear()
	for t in data.get("completed_timelines", []):
		completed_timelines.append(StringName(str(t)))
	flags = data.get("flags", {}).duplicate()
	crypto_sins = int(data.get("crypto_sins", crypto_sins))
	legacy_buffs = data.get("legacy_buffs", legacy_buffs).duplicate()
	unlocked_titles = data.get("unlocked_titles", []).duplicate()
	equipped_title = str(data.get("equipped_title", ""))
	backlog_pending = data.get("backlog_pending", []).duplicate()
	backlog_cooking = str(data.get("backlog_cooking", ""))
	backlog_turns_left = int(data.get("backlog_turns_left", 0))
	compiled_ideas = data.get("compiled_ideas", {}).duplicate()
	main_quest_stage = int(data.get("main_quest_stage", 0))
	credit_active = bool(data.get("credit_active", false))
	kpi_days = int(data.get("kpi_days", -1))
	run_over = bool(data.get("run_over", false))
	sins_awarded = bool(data.get("sins_awarded", false))
	pending_map_timeline = StringName(str(data.get("pending_map_timeline", "")))
	pending_map_title = str(data.get("pending_map_title", ""))
	microloan_resume_next = str(data.get("microloan_resume_next", ""))
	stats_changed.emit()
	inventory_changed.emit()
	flags_changed.emit()


func tick_map_turn() -> void:
	## Вызывать при каждом ходе по глобальной карте.
	if credit_active:
		if gold > 0:
			gold -= 1
		else:
			health -= 1
	## Песочные часы долга: тикают нервы (плата за +KPI дней)
	if get_flag(&"relic_hourglass") and mental > 1:
		mental -= 1
	if has_item(&"bio_antenna") and mental < VITAL_MAX:
		mental += 1
	elif guild == Guild.MAGES and mental < VITAL_MAX:
		mental += 1
	_tick_backlog()
	tick_goblin_narrator()
	if kpi_days > 0:
		kpi_days -= 1
		if kpi_days == 0:
			flags[&"pending_kpi_deadline"] = true


func start_kpi_timer() -> void:
	if kpi_days < 0:
		kpi_days = KPI_START_DAYS
		## Песочные часы: +3 дня к KPI, но ментальный налог каждый ход карты
		if get_flag(&"relic_hourglass"):
			kpi_days += 3
			stats_changed.emit()


func _check_game_over() -> void:
	if run_over:
		return
	if health <= 0:
		if try_protein_save():
			return
		_emit_game_over(&"death")
	elif mental <= 0:
		_emit_game_over(&"burnout")
	elif gold < GOLD_DEBT_DEATH:
		_emit_game_over(&"collectors")


func trigger_game_over(reason: StringName) -> void:
	_emit_game_over(reason)


func _emit_game_over(reason: StringName) -> void:
	if run_over:
		return
	run_over = true
	game_over.emit(reason)
