extends Node
## Точка входа: сразу в главное меню.

func _ready() -> void:
	# Нельзя менять сцену прямо в _ready бута — дерево ещё «занято».
	SceneManager.to_main_menu()
