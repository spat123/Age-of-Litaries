extends Button
class_name ChoiceCard
## Лицо = действие (art). Рубашка = исход (result_art) + статы. Flip по scale.x.

signal result_acknowledged

const HOVER_SCALE := 1.06
const HOVER_DURATION := 0.12

@onready var _front: Control = %Front
@onready var _back: Control = %Back
@onready var _title: Label = %Title
@onready var _art: TextureRect = %Art
@onready var _result_art: TextureRect = %ResultArt
@onready var _result_label: RichTextLabel = %ResultText
@onready var _effects_label: Label = %EffectsText
@onready var _continue_hint: Label = %ContinueHint

var _choice_data: Dictionary = {}
var _flipped: bool = false
var _busy: bool = false
var _ack_sent: bool = false
var _unaffordable_need: int = -1
var _hovering: bool = false
var _hover_tw: Tween


func _ready() -> void:
	pivot_offset = custom_minimum_size * 0.5
	_back.visible = false
	_front.visible = true
	_ignore_mouse_on_visuals(self)
	mouse_entered.connect(_on_mouse_entered)
	mouse_exited.connect(_on_mouse_exited)
	resized.connect(_update_pivot)


func setup(choice: Dictionary) -> void:
	_choice_data = choice
	_flipped = false
	_ack_sent = false
	_unaffordable_need = -1
	if is_node_ready():
		_apply_front()
	else:
		ready.connect(_apply_front, CONNECT_ONE_SHOT)


func mark_unaffordable(need: int) -> void:
	## Нищебродский клик: карта видна; клик без золота = унижение + кринж.
	_unaffordable_need = need
	if is_node_ready():
		_apply_unaffordable_look()


func _apply_unaffordable_look() -> void:
	if _unaffordable_need < 0:
		return
	var base := str(_choice_data.get("label", "..."))
	_title.text = "%s\n(пыль в карманах · нужно %d)" % [base, _unaffordable_need]
	modulate = Color(0.72, 0.72, 0.78, modulate.a)


func _apply_front() -> void:
	_front.visible = true
	_back.visible = false
	_title.text = str(_choice_data.get("label", "..."))
	_art.texture = _load_tex(str(_choice_data.get("art", "")))
	disabled = false
	modulate = Color.WHITE
	_kill_hover_tween()
	_hovering = false
	z_index = 0
	scale = Vector2.ONE
	_ack_sent = false
	_apply_unaffordable_look()


func get_choice() -> Dictionary:
	return _choice_data


func is_flipped() -> bool:
	return _flipped


func show_result_side(result_text: String, effects_line: String) -> void:
	_busy = true
	_ack_sent = false
	disabled = true
	_kill_hover_tween()
	_hovering = false
	z_index = 0
	_update_pivot()
	_result_label.text = result_text
	_effects_label.text = effects_line
	_continue_hint.text = "Нажми, чтобы продолжить"

	# result_art явно, иначе art с суффиксом _result, иначе оставляем пусто
	var result_path := str(_choice_data.get("result_art", ""))
	if result_path.is_empty():
		var front := str(_choice_data.get("art", ""))
		if front.ends_with(".png"):
			result_path = front.insert(front.length() - 4, "_result")
	_result_art.texture = _load_tex(result_path)

	var tw := create_tween()
	tw.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(self, "scale:x", 0.0, 0.18)
	await tw.finished

	_front.visible = false
	_back.visible = true
	_flipped = true

	tw = create_tween()
	tw.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(self, "scale:x", 1.0, 0.18)
	await tw.finished
	_busy = false
	disabled = false


func play_enter(duration: float = 0.16) -> void:
	## Появление: fade + лёгкий scale (быстро, контейнер сам раскладывает).
	disabled = true
	_kill_hover_tween()
	_hovering = false
	z_index = 0
	_update_pivot()
	var target_mod := Color(0.72, 0.72, 0.78, 1.0) if _unaffordable_need >= 0 else Color.WHITE
	modulate.a = 0.0
	scale = Vector2(0.82, 0.82)
	var tw := create_tween()
	tw.set_parallel(true)
	tw.set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	tw.tween_property(self, "modulate", target_mod, duration)
	tw.tween_property(self, "scale", Vector2.ONE, duration)
	await tw.finished
	disabled = false
	if _hovering and _can_hover():
		_apply_hover_scale(true)


func dismiss_away(_dir: float = 1.0) -> void:
	## Только fade+scale: сдвиг position внутри HBox ломает раскладку (особенно при 2 картах).
	disabled = true
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_kill_hover_tween()
	_hovering = false
	z_index = 0
	var tw := create_tween()
	tw.set_parallel(true)
	tw.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN)
	tw.tween_property(self, "modulate:a", 0.0, 0.16)
	tw.tween_property(self, "scale", Vector2(0.82, 0.82), 0.16)
	await tw.finished
	queue_free()


func acknowledge_result() -> void:
	if _busy or not _flipped or _ack_sent:
		return
	_ack_sent = true
	disabled = true
	result_acknowledged.emit()


func _load_tex(path: String) -> Texture2D:
	if path.is_empty() or not ResourceLoader.exists(path):
		return null
	return load(path) as Texture2D


func _pressed() -> void:
	if _busy:
		return
	if _flipped:
		acknowledge_result()


func _on_mouse_entered() -> void:
	_hovering = true
	_apply_hover_scale(true)


func _on_mouse_exited() -> void:
	_hovering = false
	_apply_hover_scale(false)


func _can_hover() -> bool:
	return not _busy and not disabled and not _flipped and mouse_filter != Control.MOUSE_FILTER_IGNORE


func _apply_hover_scale(hover: bool) -> void:
	if hover and not _can_hover():
		return
	_kill_hover_tween()
	_update_pivot()
	z_index = 10 if hover else 0
	var target := Vector2(HOVER_SCALE, HOVER_SCALE) if hover else Vector2.ONE
	_hover_tw = create_tween()
	_hover_tw.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
	_hover_tw.tween_property(self, "scale", target, HOVER_DURATION)


func _kill_hover_tween() -> void:
	if _hover_tw != null and is_instance_valid(_hover_tw):
		_hover_tw.kill()
	_hover_tw = null


func _update_pivot() -> void:
	pivot_offset = size * 0.5 if size.x > 0.0 else custom_minimum_size * 0.5


func _ignore_mouse_on_visuals(node: Node) -> void:
	## Декор не должен перехватывать клики у Button.
	for child in node.get_children():
		if child is Control and child != self:
			(child as Control).mouse_filter = Control.MOUSE_FILTER_IGNORE
		_ignore_mouse_on_visuals(child)
