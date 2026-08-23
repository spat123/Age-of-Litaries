extends Control
## Мини-игра свахи: реальный свайп бересты ← отказать / → лайк.
## Drag на карте, тач, кнопки, стрелки ←→. Колода девушек + скрытые мэтчи.

signal finished(summary: String, effects: Dictionary, next: String, aborted: bool)

const SWIPE_THRESHOLD := 110.0
const SWIPE_VELOCITY := 700.0
const FLY_DIST := 1100.0
const CARD := "res://assets/art/cards/"

var _deck: Array[Dictionary] = []
var _index: int = 0
var _dragging: bool = false
var _drag_origin: Vector2 = Vector2.ZERO
var _card_origin: Vector2 = Vector2.ZERO
var _last_mouse: Vector2 = Vector2.ZERO
var _last_mouse_t: float = 0.0
var _velocity_x: float = 0.0
var _total_effects: Dictionary = {}
var _log: PackedStringArray = []
var _busy: bool = false
var _origin_ready: bool = false
var _next_after: String = "arena"

@onready var _hint: Label = $Hint
@onready var _progress: Label = $Progress
@onready var _name: Label = $Card/Margin/VBox/Name
@onready var _bio: Label = $Card/Margin/VBox/Bio
@onready var _art: TextureRect = $Card/Margin/VBox/Art
@onready var _card: Control = $Card
@onready var _next_card: Control = $NextCard
@onready var _next_art: TextureRect = $NextCard/Margin/VBox/Art
@onready var _next_name: Label = $NextCard/Margin/VBox/Name
@onready var _stamp_left: Label = $Card/StampLeft
@onready var _stamp_right: Label = $Card/StampRight


func setup(anti_scam: bool, has_phone: bool, next_after: String = "arena") -> void:
	_next_after = next_after if next_after != "" else "arena"
	_deck.clear()
	_index = 0
	_total_effects.clear()
	_log.clear()

	## Основная колода — девушки (и один «офисный брак»)
	if not anti_scam:
		_deck.append({
			"name": "Девица с губами-уточкой",
			"bio": "Ищет спонсора на Крестовый Поход.\n«Донать, если настоящий рыцарь.»",
			"art": CARD + "card_tinder_duck.png",
			"right": {"gold": -15, "mental": -2, "cringe": 1},
			"right_log": "Скам! Сняли золото на «поход».",
			"left_log": "Отказал уточке. Алгоритм обижен (−1🧠).",
			"left": {"mental": -1},
		})
	_deck.append({
		"name": "Дочь кузнеца",
		"bio": "Варит борщ. 0 донатов.\nЛечит раны молотком любви.\n(Премиум бабке: 10💰)",
		"art": CARD + "card_tinder_smith.png",
		"right": {"gold": -10, "health": 4, "people": 5},
		"right_log": "Мэтч! Дочь кузнеца кормит и лечит.",
		"left_log": "Пропустил лучший мэтч деревни.",
		"right_need_gold": 10,
	})
	_deck.append({
		"name": "Травница Подорожница",
		"bio": "Собирает антивирусный подорожник.\n«У меня есть DLC на здоровье.»",
		"art": CARD + "card_tinder_herb.png",
		"right": {"health": 2, "mental": 1, "item": "plantain"},
		"right_log": "Мэтч с травницей. В карман — подорожник.",
		"left_log": "Отказ травнице. Иммунитет сам себя не баффает.",
	})
	_deck.append({
		"name": "Бард-Инфлюенсерша",
		"bio": "Снимает кружочки на бересте.\nЛайк = коллаб. Дизлайк = хейт.",
		"art": CARD + "card_tinder_bard.png",
		"right": {"people": 6, "gold": -5, "mental": -1},
		"right_log": "Коллаб! Охваты выросли, кошель похудел.",
		"left_log": "Хейтнул инфлюенсершу. Тишина в ленте.",
	})
	_deck.append({
		"name": "Девица в фольге",
		"bio": "«Птицы — дроны Короля. Свайпни,\nесли тоже слышишь 5G.»",
		"art": CARD + "card_tinder_foil.png",
		"right": {"mental": 2, "inquisition": -3, "cringe": 1, "pen": "5g"},
		"right_log": "Мэтч заговорщицы. Загон 5G в бэклоге.",
		"left_log": "Отказался от фольги. Инквизиция одобряет.",
		"left": {"inquisition": 1},
	})
	_deck.append({
		"name": "Официантка Ctrl+Ale",
		"bio": "Наливает эль выгорающим рыцарям.\n«После дедлайна — всегда.»",
		"art": CARD + "card_tinder_tavern.png",
		"right": {"mental": 3, "gold": -3, "people": 2},
		"right_log": "Кружка эля и тёплая улыбка. Менталочка++.",
		"left_log": "Прошёл мимо таверны. Жалко.",
	})
	_deck.append({
		"name": "Монахиня-Аудитор",
		"bio": "Проверяет карму и лайки.\nСтрогая, но справедливая.",
		"art": CARD + "card_tinder_nun.png",
		"right": {"inquisition": 5, "mental": -2, "crown": 2},
		"right_log": "Свидание-аудит. Инквизиция в восторге.",
		"left_log": "Отказал аудитору. Карма на паузе.",
	})
	_deck.append({
		"name": "Релокантка из гамака",
		"bio": "Работает удалённо из Леса.\n«Переедем? У меня VPN-сосна.»",
		"art": CARD + "card_tinder_reloc.png",
		"right": {"mental": 2, "crown": -2, "people": 1},
		"right_log": "Мэтч релокантки. Чемоданы уже пакуются.",
		"left_log": "Остаёшься в Столице. Гамак свободен.",
	})
	_deck.append({
		"name": "«Женат на работе»",
		"bio": "Профиль: дедлайны, KPI, ноль свиданий.\nСвайп вправо = остепениться в офисе.",
		"art": CARD + "card_tinder_work.png",
		"right": {"crown": 4, "mental": -4},
		"right_log": "Остепенился на работе. Одиночество в комплекте.",
		"left_log": "Отказ от офисного брака. Свобода.",
	})
	if has_phone:
		_deck.append({
			"name": "Барон Венчур (через смартфон)",
			"bio": "Скрытый мэтч алгоритма.\nИнвестиции вместо чувств.",
			"art": CARD + "card_tinder_baron.png",
			"right": {"gold": 30, "crown": 2},
			"right_log": "Мэтч с Бароном. Деньги капают!",
			"left_log": "Отклонил венчурный мэтч.",
			"flag": "baron_venture",
		})

	_show_current()


func _ready() -> void:
	_stamp_left.modulate.a = 0.0
	_stamp_right.modulate.a = 0.0
	_hint.text = "Тяни карту ← отказать  ·  → лайк\nКнопки или стрелки ← →"
	mouse_filter = Control.MOUSE_FILTER_STOP
	_card.gui_input.connect(_on_card_gui_input)
	_card.mouse_filter = Control.MOUSE_FILTER_STOP
	_next_card.mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_process_unhandled_input(true)
	await get_tree().process_frame
	_card_origin = _card.position
	_origin_ready = true


func _unhandled_input(event: InputEvent) -> void:
	if _busy:
		return
	if event is InputEventKey and event.pressed and not event.echo:
		var k := event as InputEventKey
		if k.keycode == KEY_LEFT or k.keycode == KEY_A:
			_commit(false)
			get_viewport().set_input_as_handled()
		elif k.keycode == KEY_RIGHT or k.keycode == KEY_D:
			_commit(true)
			get_viewport().set_input_as_handled()


func _on_card_gui_input(event: InputEvent) -> void:
	if _busy or _index >= _deck.size():
		return
	if event is InputEventScreenTouch:
		var st := event as InputEventScreenTouch
		if st.pressed:
			_begin_drag(st.position)
		else:
			_end_drag()
		_card.accept_event()
	elif event is InputEventScreenDrag:
		var sd := event as InputEventScreenDrag
		_move_drag(sd.position)
		_card.accept_event()
	elif event is InputEventMouseButton:
		var mb := event as InputEventMouseButton
		if mb.button_index == MOUSE_BUTTON_LEFT:
			if mb.pressed:
				_begin_drag(mb.position)
			else:
				_end_drag()
			_card.accept_event()
	elif event is InputEventMouseMotion and _dragging:
		var mm := event as InputEventMouseMotion
		_move_drag(mm.position)
		_card.accept_event()


func _begin_drag(local_pos: Vector2) -> void:
	if not _origin_ready:
		_card_origin = _card.position
		_origin_ready = true
	_dragging = true
	_drag_origin = local_pos
	_last_mouse = local_pos
	_last_mouse_t = Time.get_ticks_msec() / 1000.0
	_velocity_x = 0.0


func _move_drag(local_pos: Vector2) -> void:
	if not _dragging:
		return
	var now := Time.get_ticks_msec() / 1000.0
	var dt := maxf(0.001, now - _last_mouse_t)
	var dx_frame: float = local_pos.x - _last_mouse.x
	_velocity_x = dx_frame / dt
	_last_mouse = local_pos
	_last_mouse_t = now

	var dx: float = local_pos.x - _drag_origin.x
	_card.position = _card_origin + Vector2(dx, absf(dx) * 0.08)
	_card.rotation = clampf(dx / 700.0, -0.35, 0.35)
	_stamp_right.modulate.a = clampf(dx / SWIPE_THRESHOLD, 0.0, 1.0)
	_stamp_left.modulate.a = clampf(-dx / SWIPE_THRESHOLD, 0.0, 1.0)
	## Подсветка края
	if dx > 0:
		_card.modulate = Color(1.0, 1.0, 1.0, 1.0).lerp(Color(0.75, 1.0, 0.8, 1.0), clampf(dx / 200.0, 0.0, 1.0))
	else:
		_card.modulate = Color(1.0, 1.0, 1.0, 1.0).lerp(Color(1.0, 0.75, 0.75, 1.0), clampf(-dx / 200.0, 0.0, 1.0))


func _end_drag() -> void:
	if not _dragging:
		return
	_dragging = false
	var dx: float = _card.position.x - _card_origin.x
	if dx >= SWIPE_THRESHOLD or _velocity_x >= SWIPE_VELOCITY:
		_commit(true)
	elif dx <= -SWIPE_THRESHOLD or _velocity_x <= -SWIPE_VELOCITY:
		_commit(false)
	else:
		var tw := create_tween()
		tw.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
		tw.tween_property(_card, "position", _card_origin, 0.22)
		tw.parallel().tween_property(_card, "rotation", 0.0, 0.22)
		tw.parallel().tween_property(_card, "modulate", Color.WHITE, 0.15)
		_stamp_left.modulate.a = 0.0
		_stamp_right.modulate.a = 0.0


func _show_current() -> void:
	if _index >= _deck.size():
		_finish_deck()
		return
	var p: Dictionary = _deck[_index]
	_name.text = str(p.get("name", "?"))
	_bio.text = str(p.get("bio", ""))
	_load_art(_art, str(p.get("art", "")))
	_progress.text = "%d / %d" % [_index + 1, _deck.size()]
	_card.position = _card_origin if _origin_ready else _card.position
	_card.rotation = 0.0
	_card.modulate = Color.WHITE
	_stamp_left.modulate.a = 0.0
	_stamp_right.modulate.a = 0.0
	_update_next_preview()
	if not _origin_ready:
		await get_tree().process_frame
		_card_origin = _card.position
		_origin_ready = true


func _update_next_preview() -> void:
	var ni := _index + 1
	if ni >= _deck.size():
		_next_card.visible = false
		return
	_next_card.visible = true
	var p: Dictionary = _deck[ni]
	_next_name.text = str(p.get("name", "?"))
	_load_art(_next_art, str(p.get("art", "")))


func _load_art(tex_rect: TextureRect, art_path: String) -> void:
	if art_path != "" and ResourceLoader.exists(art_path):
		tex_rect.texture = load(art_path) as Texture2D
	else:
		tex_rect.texture = null


func _on_left_pressed() -> void:
	if _busy:
		return
	_commit(false)


func _on_right_pressed() -> void:
	if _busy:
		return
	_commit(true)


func _commit(liked: bool) -> void:
	if _busy or _index >= _deck.size():
		return
	_busy = true
	_dragging = false
	var p: Dictionary = _deck[_index]
	var fly := FLY_DIST if liked else -FLY_DIST
	if liked:
		_stamp_right.modulate.a = 1.0
		_stamp_left.modulate.a = 0.0
	else:
		_stamp_left.modulate.a = 1.0
		_stamp_right.modulate.a = 0.0
	var tw := create_tween()
	tw.set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_CUBIC)
	tw.tween_property(_card, "position:x", _card_origin.x + fly, 0.22)
	tw.parallel().tween_property(_card, "rotation", 0.45 if liked else -0.45, 0.22)
	tw.parallel().tween_property(_card, "modulate:a", 0.0, 0.22)
	await tw.finished

	if liked:
		if p.has("right_need_gold") and GameState.gold < int(p["right_need_gold"]):
			_log.append("Лайкнут «%s», но нет %d💰 на премиум — мэтч сорвался." % [
				str(p.get("name", "?")), int(p["right_need_gold"])
			])
		else:
			_apply_swipe_fx(p.get("right", {}))
			if p.has("flag"):
				GameState.set_flag(StringName(str(p["flag"])), true)
			_log.append(str(p.get("right_log", "Лайк.")))
	else:
		_apply_swipe_fx(p.get("left", {}))
		_log.append(str(p.get("left_log", "Отказ.")))

	_index += 1
	_card.modulate = Color.WHITE
	_card.position = _card_origin
	_card.rotation = 0.0
	_busy = false

	if GameState.run_over:
		_finish_deck(true)
		return
	if GameState.get_flag("pending_goblin_takeover"):
		_log.append("Абсурд зашкаливает — Гоблин-ПМ перехватывает микрофон.")
		_finish_deck(true)
		return
	_show_current()


func _apply_swipe_fx(fx: Dictionary) -> void:
	## Сразу в GameState — смерть/кринж mid-deck; finished не дублирует эффекты.
	if fx.is_empty():
		return
	if fx.has("item"):
		GameState.add_item(StringName(str(fx["item"])))
	if fx.has("pen"):
		GameState.set_flag(StringName("pen_%s" % str(fx["pen"])), true)
		GameState.queue_backlog_pen(str(fx["pen"]))
	var stats := fx.duplicate()
	stats.erase("item")
	stats.erase("pen")
	if not stats.is_empty():
		GameState.apply_effects(stats)
		for k in stats.keys():
			if k == "cringe":
				continue
			_total_effects[k] = int(_total_effects.get(k, 0)) + int(stats[k])


func _finish_deck(aborted: bool = false) -> void:
	_next_card.visible = false
	var summary := "Свайпы закончены (%d портретов).\n" % _deck.size() + "\n".join(_log)
	if aborted:
		summary = "Свайпы прерваны.\n" + "\n".join(_log)
	elif _log.is_empty():
		summary = "Береста кончилась. Пора на арену."
	finished.emit(summary, {}, _next_after, aborted)
