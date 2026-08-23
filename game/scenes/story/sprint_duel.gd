extends Control
## Прототип боя «Дуэль Спринтов»: рука умений + телеграф врага.
## Победа / поражение → finished; урон по HP идёт в GameState.

signal finished(summary: String, effects: Dictionary, next: String, aborted: bool)

const BG := "res://assets/art/backgrounds/bg_act2_arena.png"

var _next_after: String = "end"
var _enemy_hp: int = 14
var _enemy_max: int = 14
var _enemy_name: String = "Гоблин-Стажёр"
var _block: int = 0
var _busy: bool = false
var _turn: int = 1
var _telegraph: Dictionary = {}
var _log: PackedStringArray = []

@onready var _title: Label = %Title
@onready var _enemy_label: Label = %EnemyLabel
@onready var _telegraph_label: Label = %Telegraph
@onready var _player_label: Label = %PlayerLabel
@onready var _log_label: RichTextLabel = %Log
@onready var _hand: HBoxContainer = %Hand
@onready var _flee_btn: Button = %FleeBtn


func setup(next_after: String = "end", enemy_name: String = "Гоблин-Стажёр", enemy_hp: int = 14) -> void:
	_next_after = next_after if next_after != "" else "end"
	_enemy_name = enemy_name
	_enemy_hp = enemy_hp
	_enemy_max = enemy_hp
	_block = 0
	_busy = false
	_turn = 1
	_log.clear()
	_refresh_ui()
	_roll_telegraph()
	_rebuild_hand()
	_flee_btn.pressed.connect(_on_flee)
	_append("Спринт начался. Телеграф врага виден сверху.")


func _ready() -> void:
	if _title:
		_title.text = "Дуэль Спринтов"
	var bg := get_node_or_null("%Background") as TextureRect
	if bg and ResourceLoader.exists(BG):
		bg.texture = load(BG) as Texture2D


func _player_atk_bonus() -> int:
	var bonus := 0
	if GameState.has_item(&"smart_sword"):
		bonus += 1
	if GameState.has_item(&"t800_module"):
		bonus += 2
	if GameState.get_flag(&"arena_duct_tape"):
		bonus += 0  # armor, not damage
	return bonus


func _abilities() -> Array[Dictionary]:
	return [
		{
			"id": "commit",
			"label": "Коммит силой\n(урон 3)",
			"dmg": 3,
			"block": 0,
			"cancel": false,
			"mental": 0,
		},
		{
			"id": "refactor",
			"label": "Рефактор\n(блок 3)",
			"dmg": 0,
			"block": 3,
			"cancel": false,
			"mental": 0,
		},
		{
			"id": "hotfix",
			"label": "Хотфикс в прод\n(урон 5, −1🧠)",
			"dmg": 5,
			"block": 0,
			"cancel": false,
			"mental": -1,
		},
		{
			"id": "wontfix",
			"label": "Won't Fix\n(сбить телеграф)",
			"dmg": 0,
			"block": 0,
			"cancel": true,
			"mental": 0,
		},
	]


func _rebuild_hand() -> void:
	for c in _hand.get_children():
		c.queue_free()
	for ab in _abilities():
		var btn := Button.new()
		btn.text = str(ab["label"])
		btn.custom_minimum_size = Vector2(150, 72)
		btn.pressed.connect(_on_ability.bind(ab))
		_hand.add_child(btn)


func _roll_telegraph() -> void:
	var pool := [
		{"id": "bug", "text": "📝 Запилить баг-репорт (урон 2)", "dmg": 2, "cringe": 0},
		{"id": "cringe", "text": "😳 Кринж-атака (урон 1 + абсурд)", "dmg": 1, "cringe": 1},
		{"id": "deadline", "text": "⏰ Дедлайн-молот (урон 4)", "dmg": 4, "cringe": 0},
		{"id": "tax", "text": "💰 Налог на стендап (урон 2, −2💰)", "dmg": 2, "gold": -2, "cringe": 0},
	]
	_telegraph = pool[randi() % pool.size()]
	_telegraph_label.text = "Телеграф: %s" % str(_telegraph.get("text", "?"))


func _refresh_ui() -> void:
	_enemy_label.text = "%s  ❤️ %d / %d" % [_enemy_name, _enemy_hp, _enemy_max]
	var armor := " · блок %d" % _block if _block > 0 else ""
	var tape := " · изолента" if GameState.get_flag(&"arena_duct_tape") else ""
	_player_label.text = "Ты  ❤️ %d · 🧠 %d%s%s · ход %d" % [
		GameState.health, GameState.mental, armor, tape, _turn
	]
	_log_label.text = "\n".join(_log)


func _append(line: String) -> void:
	_log.append(line)
	if _log.size() > 8:
		_log = _log.slice(_log.size() - 8)
	_refresh_ui()


func _on_ability(ab: Dictionary) -> void:
	if _busy:
		return
	_busy = true
	_set_hand_disabled(true)

	var dmg := int(ab.get("dmg", 0)) + (_player_atk_bonus() if int(ab.get("dmg", 0)) > 0 else 0)
	var blk := int(ab.get("block", 0))
	var mental_cost := int(ab.get("mental", 0))
	var cancel := bool(ab.get("cancel", false))

	if mental_cost < 0 and GameState.mental + mental_cost < 1:
		_append("Не хватает 🧠 на хотфикс.")
		_busy = false
		_set_hand_disabled(false)
		return

	if blk > 0:
		_block += blk
		_append("Рефактор: блок +%d." % blk)
	if dmg > 0:
		_enemy_hp = maxi(0, _enemy_hp - dmg)
		_append("%s: %d урона по врагу." % [str(ab.get("id", "hit")), dmg])
	if mental_cost != 0:
		GameState.apply_effects({"mental": mental_cost})
	if cancel:
		_append("Won't Fix: телеграф отклонён.")
		_telegraph = {}
		_telegraph_label.text = "Телеграф: —— (сбит)"

	_refresh_ui()
	await get_tree().create_timer(0.35).timeout

	if _enemy_hp <= 0:
		await _win()
		return

	await _enemy_turn(cancel)
	if GameState.run_over or GameState.health <= 0:
		await _lose()
		return

	_turn += 1
	_roll_telegraph()
	_busy = false
	_set_hand_disabled(false)
	_refresh_ui()


func _enemy_turn(cancelled: bool) -> void:
	if cancelled or _telegraph.is_empty():
		_append("Враг в ступоре от Won't Fix.")
		await get_tree().create_timer(0.25).timeout
		return
	var raw := int(_telegraph.get("dmg", 0))
	if GameState.get_flag(&"arena_duct_tape"):
		raw = maxi(0, raw - 1)
	var absorbed := mini(_block, raw)
	_block = maxi(0, _block - raw)
	var dealt := raw - absorbed
	if dealt > 0:
		GameState.apply_effects({"health": -dealt})
	var bits: PackedStringArray = ["Враг бьёт на %d" % raw]
	if absorbed > 0:
		bits.append("блок съел %d" % absorbed)
	if dealt > 0:
		bits.append("ты −%d❤️" % dealt)
	else:
		bits.append("ты цел")
	_append(". ".join(bits) + ".")
	if int(_telegraph.get("cringe", 0)) > 0:
		GameState.register_absurd_moment(int(_telegraph["cringe"]))
		_append("Абсурдная атака — странный выбор зафиксирован.")
	if _telegraph.has("gold"):
		GameState.apply_effects({"gold": int(_telegraph["gold"])})
		_append("Стендап стоил золота.")
	await get_tree().create_timer(0.35).timeout


func _win() -> void:
	_append("Победа спринта!")
	var fx := {
		"gold": 20,
		"mental": 2,
	}
	var summary := "Ты закрыл спринт против «%s». Толпа орёт «ship it!». Сын Маминой Подруги ставит дизлайк." % _enemy_name
	finished.emit(summary, fx, _next_after, false)


func _lose() -> void:
	var summary := "Спринт провален. %s тебя задеплоил в лужу." % _enemy_name
	finished.emit(summary, {}, _next_after, true)


func _on_flee() -> void:
	if _busy:
		return
	_busy = true
	finished.emit("Ты слил спринт и выбежал с арены. Сэр Успешный снимает stories.", {"mental": -1}, _next_after, true)


func _set_hand_disabled(v: bool) -> void:
	for c in _hand.get_children():
		if c is Button:
			(c as Button).disabled = v
	_flee_btn.disabled = v
