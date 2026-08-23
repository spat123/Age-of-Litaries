extends Resource
class_name LocationData
## Точка на глобальной карте.

@export var id: StringName = &""
@export var title: String = ""
@export var description: String = ""
@export var map_position: Vector2 = Vector2.ZERO
@export var timeline_id: StringName = &""
@export var bgm_id: StringName = &"village"
@export var unlocks: Array[StringName] = []
