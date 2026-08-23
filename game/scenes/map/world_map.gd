extends Node2D
## Глобальная карта прогресса. Клики по локациям → StoryRunner (позже Dialogic).

const STATS_HUD := preload("res://scenes/ui/stats_hud.tscn")
const RandomEncounters = preload("res://resources/story/random_encounters.gd")

@onready var _nodes_root: Node2D = %LocationNodes
@onready var _hint: Label = %Hint

var _locations: Array[LocationData] = []


func _ready() -> void:
	add_child(STATS_HUD.instantiate())
	AudioManager.play_bgm(&"map")
	## Миграция сейвов: кузня рядом с Биг Дата
	if &"big_data" in GameState.unlocked_locations:
		GameState.unlock_location(&"forge_service")
	_build_locations()
	_spawn_nodes()
	_hint.text = "Акт 1–2 + сайды (лес / болото / кузня). Выбери точку на карте."
	GameState.game_over.connect(_on_game_over)
	GameState.save_game()


func _build_locations() -> void:
	_locations = [
		_loc(&"lower_wifi", "Нижние Вай-Файки", "Родина грязекопателей.", Vector2(180, 420), &"act1_01_birth", &"village", [&"meme_tract"]),
		_loc(&"meme_tract", "Тракт Мемов", "Дорога в столицу и случайные встречи.", Vector2(420, 360), &"act1_road_stub", &"road", [&"big_data"]),
		_loc(&"big_data", "Биг Дата", "Гильдии, HR, ипотека.", Vector2(680, 300), &"act2_city_stub", &"city", [&"castle_capital", &"relocant_forest", &"update_swamp", &"forge_service"]),
		_loc(&"forge_service", "Кузня-Сисадмин", "Крафт, мусор и брифинг перед ареной.", Vector2(760, 400), &"forge_service", &"city", []),
		_loc(&"relocant_forest", "Лес Релокантов", "Фрилансеры и Юрист Логововъ.", Vector2(520, 520), &"side_forest_stub", &"road", [&"update_swamp"]),
		_loc(&"update_swamp", "Болото Апдейтов", "Лорд Отката и Патч 1.0.", Vector2(860, 480), &"side_swamp_stub", &"road", []),
		_loc(&"castle_capital", "Замок Капитал", "Король-CEO.", Vector2(960, 220), &"act3_castle_stub", &"castle", [&"dragon_lair"]),
		_loc(&"dragon_lair", "Логово Дракона", "Финальная психологическая сессия.", Vector2(1120, 360), &"act3_dragon_stub", &"dragon", []),
	]


func _loc(
	id: StringName,
	title: String,
	desc: String,
	pos: Vector2,
	timeline: StringName,
	bgm: StringName,
	unlocks: Array
) -> LocationData:
	var d := LocationData.new()
	d.id = id
	d.title = title
	d.description = desc
	d.map_position = pos
	d.timeline_id = timeline
	d.bgm_id = bgm
	for u in unlocks:
		d.unlocks.append(StringName(str(u)))
	return d


func _spawn_nodes() -> void:
	for child in _nodes_root.get_children():
		child.queue_free()

	for loc in _locations:
		var btn := Button.new()
		btn.text = loc.title
		btn.position = loc.map_position
		btn.custom_minimum_size = Vector2(160, 40)
		btn.disabled = loc.id not in GameState.unlocked_locations
		btn.tooltip_text = loc.description
		btn.pressed.connect(_on_location_pressed.bind(loc))
		_nodes_root.add_child(btn)


func _on_location_pressed(loc: LocationData) -> void:
	AudioManager.play_sfx(&"ui_click")
	GameState.current_location = loc.id
	GameState.tick_map_turn()
	if _try_extreme_event(loc):
		return
	if _try_random_encounter(loc):
		return
	if loc.id == &"big_data" and GameState.get_flag(&"big_data_hub_open"):
		SceneManager.to_story(&"hub_big_data", "Биг Дата — хаб")
		return
	SceneManager.to_story(loc.timeline_id, loc.title)


func _try_extreme_event(loc: LocationData) -> bool:
	if GameState.get_flag("pending_kpi_deadline"):
		GameState.pending_map_timeline = loc.timeline_id
		GameState.pending_map_title = loc.title
		SceneManager.to_story(&"event_kpi_deadline", "Дедлайн KPI")
		return true
	var judgement: StringName = GameState.pending_judgement_timeline()
	if judgement != &"":
		GameState.pending_map_timeline = loc.timeline_id
		GameState.pending_map_title = loc.title
		var titles := {
			&"event_people_riot": "Бунт Народа",
			&"event_people_cancel": "Отмена",
			&"event_inq_wrath": "Гнев Инквизиции",
			&"event_inq_monk": "Постриг",
			&"event_crown_execute": "Казнь",
			&"event_crown_exile": "Реструктуризация",
			&"event_cringe_king": "Король Кринжа",
		}
		SceneManager.to_story(judgement, str(titles.get(judgement, "Судный День")))
		return true
	return false


func _try_random_encounter(loc: LocationData) -> bool:
	if loc.id == &"lower_wifi":
		return false
	if randf() > 0.40:
		return false
	var pool: Array[StringName] = RandomEncounters.pool_ids().duplicate()
	## API — реже, чем бытовые рандомы
	if randf() > 0.35:
		pool.erase(&"random_api_fatal")
	if not GameState.get_flag("infogypsy_map_met") and loc.id in [&"relocant_forest", &"update_swamp", &"castle_capital", &"meme_tract"]:
		pool.append(&"random_infogypsy")
	if pool.is_empty():
		return false
	var pick: StringName = pool[randi() % pool.size()]
	GameState.pending_map_timeline = loc.timeline_id
	GameState.pending_map_title = loc.title
	var titles := {
		&"random_rtx": "Корован RTX",
		&"random_rain_tax": "Налог на дождь",
		&"random_plantain_scam": "Скам-подорожник",
		&"random_infogypsy": "Инфоцыган на пеньке",
		&"random_api_fatal": "Конфликт API",
	}
	SceneManager.to_story(pick, str(titles.get(pick, "Случайная встреча")))
	return true


func _on_game_over(reason: StringName) -> void:
	var special := GameState.special_ending_timeline(reason)
	if special != &"":
		SceneManager.to_story(special, GameState.special_ending_title(special))
		return
	var go: Dictionary = GameState.prepare_hr_game_over(reason)
	_hint.text = "GAME OVER: %s\n%s\n(+%d грехов, 🐛~%d багов в HR)." % [
		str(go["flavor"]),
		str(go["diploma"]),
		int(go["gained"]), int(go["bugs"]),
	]
	SceneManager.to_story(&"heavenly_hr", "Небесная HR")


func _on_menu_pressed() -> void:
	SceneManager.to_main_menu()
