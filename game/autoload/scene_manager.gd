extends Node
## Переходы между сценами (меню → карта → стори-раннер).
## Смена сцены всегда отложенная — нельзя remove_child во время _ready дерева.
## Если переход уже идёт — следующий кладётся в очередь (не теряется).

signal scene_changed(path: String)

const MAIN_MENU := "res://scenes/ui/main_menu.tscn"
const WORLD_MAP := "res://scenes/map/world_map.tscn"
const STORY_RUNNER := "res://scenes/story/story_runner.tscn"

var _busy: bool = false
var _queue: Array = []  # Array of {path, params}
## Параметры для следующей сцены — читает сцена в _ready через take_pending_params().
var pending_params: Dictionary = {}


func go_to(path: String, params: Dictionary = {}) -> void:
	## Во время game over не уводим на карту поверх HR/концовки.
	if path == WORLD_MAP and GameState.run_over:
		return
	if _busy:
		_queue.append({"path": path, "params": params.duplicate()})
		return
	_busy = true
	pending_params = params.duplicate()
	call_deferred("_change_scene", path)


func _change_scene(path: String) -> void:
	var err := get_tree().change_scene_to_file(path)
	if err != OK:
		push_error("SceneManager: не удалось открыть %s (err %s)" % [path, err])
		_busy = false
		_drain_queue()
		return
	await get_tree().process_frame
	_busy = false
	scene_changed.emit(path)
	_drain_queue()


func _drain_queue() -> void:
	while not _queue.is_empty():
		var next: Dictionary = _queue.pop_front()
		var p := str(next.get("path", ""))
		if p == WORLD_MAP and GameState.run_over:
			continue
		go_to(p, next.get("params", {}))
		return


func take_pending_params() -> Dictionary:
	var p := pending_params.duplicate()
	pending_params.clear()
	return p


func to_main_menu() -> void:
	_queue.clear()
	GameState.save_game()
	go_to(MAIN_MENU)


func to_world_map() -> void:
	GameState.save_game()
	go_to(WORLD_MAP)


func to_story(timeline_id: StringName, title: String = "") -> void:
	go_to(STORY_RUNNER, {"timeline_id": String(timeline_id), "title": title})
