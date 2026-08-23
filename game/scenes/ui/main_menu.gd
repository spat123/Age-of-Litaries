extends Control
## Главное меню.

@onready var _title: Label = %Title
@onready var _subtitle: Label = %Subtitle
@onready var _continue_btn: Button = $Center/Continue


func _ready() -> void:
	AudioManager.play_bgm(&"menu")
	_title.text = "Сэр Баг"
	_subtitle.text = "Исходный Код Средневековья"
	_refresh_continue()


func _refresh_continue() -> void:
	var ok := GameState.has_save()
	_continue_btn.disabled = not ok
	_continue_btn.text = "Продолжить" if ok else "Продолжить (нет сейва)"


func _on_new_game_pressed() -> void:
	AudioManager.play_sfx(&"ui_click")
	GameState.reset_new_game()
	GameState.clear_save()
	SceneManager.to_story(&"act0_tutorial", "Early Access")


func _on_continue_pressed() -> void:
	AudioManager.play_sfx(&"ui_click")
	if not GameState.load_game():
		_refresh_continue()
		return
	if GameState.run_over:
		SceneManager.to_story(&"heavenly_hr", "Небесная HR")
		return
	SceneManager.to_world_map()


func _on_quit_pressed() -> void:
	GameState.save_game()
	get_tree().quit()
