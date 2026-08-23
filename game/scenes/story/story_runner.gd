extends Control
## Choice of Life:
## - narrative: без flip, меняет текст, открывает вложенные выборы
## - result: flip; на карточке result, сверху aside (контекст), без дубля
## Переходы: кроссфейд арта без чёрного затемнения; карточки по одной.
const STATS_HUD := preload("res://scenes/ui/stats_hud.tscn")
const CHOICE_CARD := preload("res://scenes/story/choice_card.tscn")
const StubStoryScript = preload("res://resources/story/stub_story.gd")
const TINDER_SWIPE := preload("res://scenes/story/tinder_swipe.tscn")
const SPRINT_DUEL := preload("res://scenes/story/sprint_duel.tscn")

const BG_CROSS_SEC := 0.22
## Пауза между стартом появления карточек (анимации перекрываются).
const CARD_STAGGER_SEC := 0.05
const CARD_ENTER_SEC := 0.16
const CHOICES_CLEAR_SEC := 0.1

@onready var _bg: TextureRect = %Background
@onready var _bg_next: TextureRect = %BackgroundNext
@onready var _speaker: Label = %Speaker
@onready var _body: RichTextLabel = %Body
@onready var _choices: HBoxContainer = %Choices
@onready var _title: Label = %LocationTitle

var _timeline_id: StringName = &""
var _beats: Array = []
var _beat_by_id: Dictionary = {}
var _current_id: String = ""
var _resolving: bool = false
var _pending_next: String = ""
var _current_bg_path: String = ""
var _first_beat: bool = true
## Dev: откат к предыдущему экрану выбора (снимки GameState + UI).
var _undo_stack: Array = []
var _undo_busy: bool = false
var _undo_btn: Button = null
const UNDO_STACK_MAX := 40


func apply_params(params: Dictionary) -> void:
	_timeline_id = StringName(str(params.get("timeline_id", "")))
	_title.text = str(params.get("title", ""))
	_start()


func _ready() -> void:
	add_child(STATS_HUD.instantiate())
	GameState.game_over.connect(_on_game_over)
	_prepare_bg_layers()
	_setup_dev_undo_ui()
	var params := SceneManager.take_pending_params()
	if not params.is_empty():
		apply_params(params)
	elif _timeline_id == &"":
		_timeline_id = &"act0_tutorial"
		_title.text = "Early Access"
		_start()


func _dev_undo_enabled() -> bool:
	return OS.is_debug_build()


func _setup_dev_undo_ui() -> void:
	if not _dev_undo_enabled():
		return
	_undo_btn = Button.new()
	_undo_btn.name = "DevUndo"
	_undo_btn.text = "← Отменить [Backspace]"
	_undo_btn.tooltip_text = "Dev: откат к предыдущему выбору (статы и экран). Пустой стек — ничего."
	_undo_btn.z_index = 80
	_undo_btn.focus_mode = Control.FOCUS_NONE
	_undo_btn.set_anchors_preset(Control.PRESET_TOP_LEFT)
	_undo_btn.offset_left = 16.0
	_undo_btn.offset_top = 12.0
	_undo_btn.offset_right = 260.0
	_undo_btn.offset_bottom = 48.0
	_undo_btn.pressed.connect(_dev_undo)
	add_child(_undo_btn)
	_refresh_undo_btn()


func _unhandled_input(event: InputEvent) -> void:
	if not _dev_undo_enabled():
		return
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_BACKSPACE:
			_dev_undo()
			get_viewport().set_input_as_handled()


func _push_undo_checkpoint() -> void:
	if not _dev_undo_enabled() or _undo_busy:
		return
	var choices := _snapshot_visible_choices()
	if choices.is_empty() and _current_id.is_empty():
		return
	_undo_stack.append({
		"game": GameState.to_save_dict(),
		"beat_id": _current_id,
		"speaker": _speaker.text,
		"body": _body.text,
		"bg": _current_bg_path,
		"choices": choices,
		"title": _title.text,
	})
	while _undo_stack.size() > UNDO_STACK_MAX:
		_undo_stack.pop_front()
	_refresh_undo_btn()


func _snapshot_visible_choices() -> Array:
	var out: Array = []
	for c in _choices.get_children():
		if c is ChoiceCard and is_instance_valid(c):
			out.append((c as ChoiceCard).get_choice().duplicate(true))
	return out


func _refresh_undo_btn() -> void:
	if _undo_btn == null:
		return
	var n := _undo_stack.size()
	_undo_btn.disabled = n == 0 or _undo_busy
	_undo_btn.text = "← Отменить [%d] Backspace" % n if n > 0 else "← Отменить [—]"


func _dev_undo() -> void:
	if not _dev_undo_enabled() or _undo_busy:
		return
	if _undo_stack.is_empty():
		return
	_undo_busy = true
	_resolving = false
	_pending_next = ""
	## Закрыть мини-игру поверх, если есть
	for child in get_children():
		if child is Control and child.has_signal("finished") and child.has_method("setup"):
			child.queue_free()
	var snap: Dictionary = _undo_stack.pop_back()
	GameState.from_save_dict(snap.get("game", {}))
	_current_id = str(snap.get("beat_id", ""))
	_title.text = str(snap.get("title", _title.text))
	_first_beat = false
	await _clear_choices_quick()
	await _transition_to_scene(
		str(snap.get("speaker", "Рассказчик")),
		str(snap.get("body", "")),
		str(snap.get("bg", "")),
		false
	)
	await _spawn_choices(snap.get("choices", []))
	_undo_busy = false
	_refresh_undo_btn()


func _prepare_bg_layers() -> void:
	for layer in [_bg, _bg_next]:
		layer.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		layer.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		layer.stretch_mode = TextureRect.STRETCH_SCALE
		layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_bg.modulate.a = 1.0
	_bg_next.modulate.a = 0.0


func _start() -> void:
	# Пролог с Богом и Акт 1+ — один story-трек; меню/карта — hub
	AudioManager.play_bgm(&"story")
	_beats = StubStoryScript.get_beats(_timeline_id)
	_beat_by_id.clear()
	for beat in _beats:
		if beat is Dictionary and beat.has("id"):
			_beat_by_id[str(beat["id"])] = beat
	if _beats.is_empty():
		_finish_timeline()
		return
	_show_beat(_beats[0])


func _show_beat(beat: Dictionary) -> void:
	if beat.has("require_item") and not GameState.has_item(StringName(str(beat["require_item"]))):
		_goto_next(str(beat.get("skip_to", "end")))
		return

	_resolving = false
	_pending_next = ""
	_current_id = str(beat.get("id", ""))

	var body := str(beat.get("text", ""))
	if beat.get("dynamic_text", "") == "youth_review":
		body = StubStoryScript.get_youth_review_text()
	if _current_id == "shop":
		body += "\n\nУ вас Крипто-Грехов: %d." % GameState.crypto_sins
	var speaker := _maybe_goblin_speaker(str(beat.get("speaker", "Рассказчик")))
	if GameState.is_goblin_narrator() and str(beat.get("speaker", "Рассказчик")) in ["Рассказчик", ""]:
		body = _maybe_goblin_text(body)

	await _clear_choices_quick()
	await _transition_to_scene(
		speaker,
		body,
		str(beat.get("bg", "")),
		_first_beat
	)
	_first_beat = false
	if beat.has("auto_curse"):
		var did := await _try_auto_curse(beat["auto_curse"])
		if did and GameState.get_flag("pending_goblin_takeover"):
			await _trigger_goblin_takeover()
			## Квест не прерываем — дальше обычные выборы бита
	if str(beat.get("minigame", "")) == "tinder_swipe":
		await _run_tinder_swipe(str(beat.get("next", "arena")))
		return
	if str(beat.get("minigame", "")) == "sprint_duel":
		await _run_sprint_duel(str(beat.get("next", "end")), str(beat.get("duel_enemy", "Гоблин-Стажёр")), int(beat.get("duel_hp", 14)))
		return
	await _spawn_choices(beat.get("choices", []))


func _try_auto_curse(curse: Dictionary) -> bool:
	var item_need := str(curse.get("require_item", ""))
	if item_need.is_empty() or not GameState.has_item(StringName(item_need)):
		return false
	var once := str(curse.get("once_flag", ""))
	if not once.is_empty() and GameState.get_flag(StringName(once)):
		return false
	if not once.is_empty():
		GameState.set_flag(StringName(once), true)
	var effects: Dictionary = curse.get("effects", {})
	_apply_effects(effects)
	_speaker.text = str(curse.get("speaker", "Проклятие"))
	_body.text = str(curse.get("aside", ""))
	# Короткая пауза «авто-карточки»
	await get_tree().create_timer(0.8).timeout
	_body.text = str(curse.get("result", "Проклятие сработало."))
	var fx_line := _format_effects(effects, "")
	if not fx_line.is_empty():
		_body.text += "\n\n" + fx_line
	await get_tree().create_timer(1.2).timeout
	return true


func _trigger_goblin_takeover() -> void:
	## Абсурд накопился → событие: Рассказчик сдаёт микрофон Гоблину-ПМ.
	GameState.clear_goblin_takeover_pending()
	GameState.activate_goblin_narrator()
	for c in _choices.get_children():
		c.queue_free()

	_speaker.text = "Рассказчик"
	_body.text = "Всё, с меня хватит! Этот абсурд я комментировать не буду — я в отпуск!"
	await get_tree().create_timer(1.35).timeout

	_speaker.text = "Гоблин-ПМ (И.О. Рассказчика)"
	if _timeline_id in [&"act0_tutorial", &"act1_01_birth"]:
		_body.text = "Так, зумер из колыбели. Дедлайн горит, таска завалена. Теперь я И.О. Рассказчика. Погнали кранчить — и без кринжа, ок?"
	else:
		_body.text = "Так, зумер, дедлайн горит, таска завалена. Теперь я И.О. Рассказчика. Погнали кранчить!"
	await get_tree().create_timer(1.6).timeout


func _maybe_goblin_speaker(default_speaker: String) -> String:
	if GameState.is_goblin_narrator():
		return "Гоблин-ПМ (И.О. Рассказчика)"
	return default_speaker


func _maybe_goblin_text(text: String) -> String:
	if GameState.is_goblin_narrator() and not text.is_empty():
		return GameState.goblin_wrap(text)
	return text


func _run_tinder_swipe(next_id: String) -> void:
	## Снимок экрана свахи до мини-игры (можно откатить Backspace'ом)
	_push_undo_checkpoint()
	for c in _choices.get_children():
		c.queue_free()
	var mini: Control = TINDER_SWIPE.instantiate()
	add_child(mini)
	mini.setup(
		bool(GameState.get_flag("legacy_anti_scam")),
		GameState.has_item(&"wooden_phone"),
		next_id if next_id != "" else "arena"
	)
	var summary := "Свайпы готовы."
	var effects: Dictionary = {}
	var nxt := next_id if next_id != "" else "arena"
	var aborted := false
	mini.finished.connect(func(s: String, e: Dictionary, n: String, ab: bool) -> void:
		summary = s
		effects = e
		nxt = n
		aborted = ab
	, CONNECT_ONE_SHOT)
	await mini.finished
	mini.queue_free()
	if GameState.run_over:
		return
	GameState.apply_effects(effects)
	if GameState.run_over:
		return
	if GameState.get_flag("pending_goblin_takeover"):
		_speaker.text = "Бабка-сваха"
		_body.text = summary + "\n\nАбсурд зашкаливает — микрофон перехватывает Гоблин-ПМ."
		await get_tree().create_timer(0.4).timeout
		await _trigger_goblin_takeover()
		_goto_next(nxt)
		return
	if aborted:
		_speaker.text = "Бабка-сваха"
		_body.text = summary
		await get_tree().create_timer(0.35).timeout
		SceneManager.to_world_map()
		return
	_speaker.text = "Бабка-сваха"
	_body.text = summary
	await get_tree().create_timer(0.35).timeout
	_goto_next(nxt)


func _run_sprint_duel(next_id: String, enemy_name: String, enemy_hp: int) -> void:
	_push_undo_checkpoint()
	for c in _choices.get_children():
		c.queue_free()
	var mini: Control = SPRINT_DUEL.instantiate()
	add_child(mini)
	mini.setup(next_id if next_id != "" else "end", enemy_name, enemy_hp)
	var summary := "Спринт закрыт."
	var effects: Dictionary = {}
	var nxt := next_id if next_id != "" else "end"
	var aborted := false
	mini.finished.connect(func(s: String, e: Dictionary, n: String, ab: bool) -> void:
		summary = s
		effects = e
		nxt = n
		aborted = ab
	, CONNECT_ONE_SHOT)
	await mini.finished
	mini.queue_free()
	if GameState.run_over:
		return
	GameState.apply_effects(effects)
	GameState.save_game()
	_speaker.text = "Корпоратив-арена"
	_body.text = summary
	await get_tree().create_timer(0.45).timeout
	if aborted:
		if GameState.health <= 0:
			GameState.trigger_game_over(&"death")
			return
		SceneManager.to_world_map()
		return
	## Победа в прототипе: звание героя + билет в замок (как финал арены)
	GameState.advance_main_quest(3)
	GameState.unlock_location(&"castle_capital")
	GameState.set_flag(&"arena_champion", true)
	_goto_next(nxt)


func _show_branch(from_choice: Dictionary) -> void:
	## Сюжетный выбор: новый текст ситуации + вложенные карточки, без flip.
	_resolving = false
	var speaker := _maybe_goblin_speaker(str(from_choice.get("speaker", _speaker.text)))
	var body := str(from_choice.get("branch_text", _body.text))
	if from_choice.get("dynamic_text", "") == "youth_review":
		body = StubStoryScript.get_youth_review_text()
	if GameState.is_goblin_narrator():
		body = _maybe_goblin_text(body)
	var bg := str(from_choice.get("bg", _current_bg_path))
	await _clear_choices_quick()
	await _transition_to_scene(speaker, body, bg, false)
	await _spawn_choices(from_choice.get("choices", []))


func _transition_to_scene(speaker: String, body: String, bg_path: String, is_first: bool) -> void:
	_speaker.text = speaker
	_body.text = body
	await _crossfade_bg(bg_path, is_first)


func _crossfade_bg(bg_path: String, is_first: bool) -> void:
	if bg_path.is_empty():
		return
	if not ResourceLoader.exists(bg_path):
		return
	var tex: Texture2D = load(bg_path) as Texture2D
	if tex == null:
		return

	# Первый показ или тот же арт — просто мягкое появление, без чёрного экрана
	if is_first or _current_bg_path.is_empty():
		_bg.texture = tex
		_bg.modulate.a = 0.0
		_bg_next.modulate.a = 0.0
		var tw0 := create_tween()
		tw0.tween_property(_bg, "modulate:a", 1.0, BG_CROSS_SEC).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
		await tw0.finished
		_current_bg_path = bg_path
		return

	if bg_path == _current_bg_path:
		return

	# Кроссфейд: новый проявляется поверх, старый гаснет
	_bg_next.texture = tex
	_bg_next.modulate.a = 0.0
	var tw := create_tween()
	tw.set_parallel(true)
	tw.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tw.tween_property(_bg, "modulate:a", 0.0, BG_CROSS_SEC)
	tw.tween_property(_bg_next, "modulate:a", 1.0, BG_CROSS_SEC)
	await tw.finished

	_bg.texture = tex
	_bg.modulate.a = 1.0
	_bg_next.modulate.a = 0.0
	_bg_next.texture = null
	_current_bg_path = bg_path


func _clear_choices_quick() -> void:
	var kids := _choices.get_children()
	if kids.is_empty():
		return
	for c in kids:
		if c is ChoiceCard and is_instance_valid(c):
			(c as ChoiceCard).disabled = true
	var tw := create_tween()
	tw.set_parallel(true)
	for c in kids:
		if is_instance_valid(c) and c is CanvasItem:
			tw.tween_property(c, "modulate:a", 0.0, CHOICES_CLEAR_SEC)
	await tw.finished
	for c in kids:
		if is_instance_valid(c):
			c.queue_free()
	await get_tree().process_frame


func _drop_other_cards(keep: ChoiceCard) -> void:
	## Мгновенно убираем невыбранные карты, чтобы выбранная не прыгала в HBox.
	var doomed: Array = []
	for c in _choices.get_children():
		if c == keep or not is_instance_valid(c):
			continue
		if c is ChoiceCard:
			(c as ChoiceCard).disabled = true
			(c as ChoiceCard).mouse_filter = Control.MOUSE_FILTER_IGNORE
		doomed.append(c)
	if doomed.is_empty():
		return
	var tw := create_tween()
	tw.set_parallel(true)
	for c in doomed:
		if is_instance_valid(c) and c is CanvasItem:
			tw.tween_property(c, "modulate:a", 0.0, 0.1)
			tw.tween_property(c, "scale", Vector2(0.88, 0.88), 0.1)
	await tw.finished
	for c in doomed:
		if is_instance_valid(c):
			c.queue_free()
	## Два кадра — HBox центрирует оставшуюся карту до flip
	await get_tree().process_frame
	await get_tree().process_frame
	if is_instance_valid(keep):
		keep.pivot_offset = keep.size * 0.5


func _spawn_choices(choices: Array) -> void:
	for c in _choices.get_children():
		c.queue_free()
	await get_tree().process_frame

	var spawned: Array[ChoiceCard] = []
	for choice in choices:
		# Золото НЕ скрывает карту: клик покажет «нет золота».
		if choice.has("require_mental") and GameState.mental < int(choice["require_mental"]):
			continue
		if choice.has("require_item") and not GameState.has_item(StringName(str(choice["require_item"]))):
			continue
		if choice.has("require_item_2") and not GameState.has_item(StringName(str(choice["require_item_2"]))):
			continue
		if choice.has("require_no_item") and GameState.has_item(StringName(str(choice["require_no_item"]))):
			continue
		if choice.has("require_flag") and not GameState.get_flag(StringName(str(choice["require_flag"]))):
			continue
		if choice.has("require_no_flag") and GameState.get_flag(StringName(str(choice["require_no_flag"]))):
			continue
		if choice.has("require_soul_sub") and not GameState.soul_subscription:
			continue
		if choice.has("require_sins") and GameState.crypto_sins < int(choice["require_sins"]):
			continue
		if choice.has("require_guild"):
			var need_g := str(choice["require_guild"])
			var ok := false
			match need_g:
				"warriors":
					ok = GameState.guild == GameState.Guild.WARRIORS
				"mages":
					ok = GameState.guild == GameState.Guild.MAGES
				"thieves":
					ok = GameState.guild == GameState.Guild.THIEVES
			if not ok:
				continue
		if choice.has("require_title") and str(choice["require_title"]) not in GameState.unlocked_titles:
			continue
		var card: ChoiceCard = CHOICE_CARD.instantiate() as ChoiceCard
		_choices.add_child(card)
		card.setup(choice)
		if _gold_blocked(choice):
			card.mark_unaffordable(int(choice["require_gold"]))
		card.modulate.a = 0.0
		card.disabled = true
		card.pressed.connect(_on_card_pressed.bind(card))
		spawned.append(card)

	# Дать контейнеру разложить карточки, потом анимировать по одной
	await get_tree().process_frame
	await get_tree().process_frame

	for i in spawned.size():
		var card: ChoiceCard = spawned[i]
		if not is_instance_valid(card):
			continue
		# Не ждём конец каждой — следующая стартует почти сразу
		if i == spawned.size() - 1:
			await card.play_enter(CARD_ENTER_SEC)
		else:
			card.play_enter(CARD_ENTER_SEC)
			await get_tree().create_timer(CARD_STAGGER_SEC).timeout

	if spawned.is_empty() and not choices.is_empty():
		_resolving = false
		_speaker.text = "Рассказчик"
		_body.text = "Вариантов нет (часто не хватает золота или предмета). Судьба тащит дальше…"
		await get_tree().create_timer(1.2).timeout
		_goto_next(str(choices[0].get("next", "end")))
	else:
		_resolving = false


func _on_card_pressed(card: ChoiceCard) -> void:
	# Исход: клик продолжает сюжет (до проверки _resolving — иначе «залипает»).
	if card.is_flipped():
		card.acknowledge_result()
		return
	if _resolving or _undo_busy:
		return

	var choice: Dictionary = card.get_choice()
	var kind := str(choice.get("kind", "result"))

	_resolving = true
	AudioManager.play_sfx(&"choice")

	if kind == "clarify":
		## Карточка «Чего?»: сгорает, остальные остаются; текст = перевод с айтишного.
		_speaker.text = str(choice.get("speaker", "Рассказчик"))
		_body.text = str(choice.get("clarify_text", "Рассказчик тяжело вздыхает. Даже ему стыдно за этот сленг."))
		card.dismiss_away(0.0)
		await get_tree().create_timer(0.25).timeout
		_resolving = false
		return

	## Снимок до эффектов / смены экрана — для dev-отката
	_push_undo_checkpoint()

	## Остальные карты сбрасываем сразу (без слайда — иначе HBox дёргает выбранную)
	await _drop_other_cards(card)

	if kind == "narrative":
		# выбранная тоже уходит — остаются только вложенные
		card.dismiss_away(0.0)
		await get_tree().create_timer(0.16).timeout
		await _show_branch(choice)
		return

	if kind == "return":
		card.dismiss_away(0.0)
		await get_tree().create_timer(0.16).timeout
		var next_id := str(choice.get("next", _current_id))
		if _beat_by_id.has(next_id):
			_show_beat(_beat_by_id[next_id])
		else:
			_goto_next(next_id)
		return

	# --- resultative ---
	# «Нищебродский клик»: карта всегда кликабельна; без золота — унижение + абсурд.
	if _gold_blocked(choice):
		var need := int(choice["require_gold"])
		GameState.register_absurd_moment(1)
		var fail := str(choice.get(
			"no_gold_result",
			"Ты хлопаешь по карманам. Там только пыль и амбиции. Нужно %d, а есть %d. Торговец смеётся тебе в лицо." % [need, GameState.gold]
		))
		if choice.has("aside"):
			_speaker.text = "Рассказчик"
			_body.text = str(choice["aside"])
		else:
			_speaker.text = "Рассказчик"
			_body.text = "Попытка купить без денег — это тоже выбор. Плохой."
		_pending_next = str(choice.get("next_on_fail", _current_id if not _current_id.is_empty() else choice.get("next", "end")))
		if not card.result_acknowledged.is_connected(_on_result_continue):
			card.result_acknowledged.connect(_on_result_continue, CONNECT_ONE_SHOT)
		AudioManager.play_sfx(&"pauper")
		await card.show_result_side(fail, "🐛 баг в кармане · золото %d / нужно %d" % [GameState.gold, need])
		return

	var effects: Dictionary = choice.get("effects", {})
	_apply_effects(effects)
	if GameState.run_over:
		_resolving = false
		return
	if choice.has("unlock"):
		GameState.unlock_location(StringName(str(choice["unlock"])))
	if choice.has("flag"):
		GameState.set_flag(StringName(str(choice["flag"])), true)
	if choice.has("remove_items"):
		for rid in choice["remove_items"]:
			GameState.remove_item(StringName(str(rid)))
	elif choice.has("remove_item"):
		GameState.remove_item(StringName(str(choice["remove_item"])))

	if choice.has("set_guild"):
		match str(choice["set_guild"]):
			"warriors":
				GameState.guild = GameState.Guild.WARRIORS
			"mages":
				GameState.guild = GameState.Guild.MAGES
			"thieves":
				GameState.guild = GameState.Guild.THIEVES

	if choice.get("set_soul_sub", false):
		GameState.soul_subscription = true
		GameState.advance_main_quest(2)
	if choice.get("clear_soul_sub", false):
		GameState.soul_subscription = false
	if choice.has("set_dragon_stance"):
		GameState.set_dragon_stance_from_str(str(choice["set_dragon_stance"]))
		GameState.advance_main_quest(5)
	if choice.has("equip_title"):
		GameState.equip_title(str(choice["equip_title"]))
	if choice.has("kpi_bonus") and GameState.kpi_days >= 0:
		GameState.kpi_days += int(choice["kpi_bonus"])
		GameState.stats_changed.emit()

	if choice.has("spend_sins"):
		GameState.spend_sins(int(choice["spend_sins"]))
	if choice.has("legacy_buff"):
		GameState.legacy_buffs[str(choice["legacy_buff"])] = true
	if choice.get("clear_legacy", false):
		GameState.clear_legacy_buffs()
	if choice.has("main_quest"):
		GameState.advance_main_quest(int(choice["main_quest"]))

	var item_id := ""
	if choice.has("item"):
		item_id = str(choice["item"])
	elif effects.has("item"):
		item_id = str(effects["item"])
	if not item_id.is_empty():
		GameState.add_item(StringName(item_id))
		if item_id == "wooden_phone":
			GameState.advance_main_quest(1)
		## Apple-меч не двигает main_quest на 2 (это не подписка души)

	if choice.has("game_over"):
		if choice.has("aside"):
			_speaker.text = "Рассказчик"
			_body.text = str(choice["aside"])
		var go_text := str(choice.get("result", "GAME OVER."))
		var go_fx := _format_effects(effects, item_id)
		_pending_next = ""
		await card.show_result_side(go_text, go_fx)
		_resolving = false
		GameState.trigger_game_over(StringName(str(choice["game_over"])))
		return

	if choice.get("reincarnate", false):
		if choice.has("aside"):
			_speaker.text = "Рассказчик"
			_body.text = str(choice["aside"])
		var r_text := str(choice.get("result", "Реинкарнация…"))
		await card.show_result_side(r_text, "Крипто-Грехи: %d" % GameState.crypto_sins)
		_resolving = false
		GameState.reset_new_game()
		# IT-Династия: снова Early Access — открывает скрытый лут Act 0 (телефон уже в инвентаре с рождения)
		if GameState.legacy_buffs.get("it_dynasty", false):
			SceneManager.to_story(&"act0_tutorial", "Early Access (NG+)")
		else:
			SceneManager.to_story(&"act1_01_birth", "Нижние Вай-Файки")
		return

	# Сверху — контекст (aside), НЕ текст рубашки
	if choice.has("aside"):
		_speaker.text = _maybe_goblin_speaker("Рассказчик")
		_body.text = _maybe_goblin_text(str(choice["aside"]))
	# иначе оставляем текущий текст ситуации

	var result_text := _maybe_goblin_text(str(choice.get("result", "Последствия налицо.")))
	var effects_line := _format_effects(effects, item_id)
	_pending_next = str(choice.get("next", "end"))

	# Микрозаймы: ушли в минус → перехват коллектором
	if GameState.gold < 0 and _timeline_id != &"event_microloans" and not GameState.credit_active:
		GameState.microloan_resume_next = _pending_next
		_pending_next = "__microloan__"

	if not card.result_acknowledged.is_connected(_on_result_continue):
		card.result_acknowledged.connect(_on_result_continue, CONNECT_ONE_SHOT)
	await card.show_result_side(result_text, effects_line)


func _on_result_continue() -> void:
	if _pending_next.is_empty() and not _resolving:
		return
	var next := _pending_next
	_pending_next = ""
	_resolving = false
	if GameState.run_over:
		return
	if GameState.get_flag("pending_goblin_takeover"):
		await _trigger_goblin_takeover()
		_goto_next(next)
		return
	## Каждый результативный выбор съедает 1 ход И.О. Гоблина
	if GameState.is_goblin_narrator():
		if GameState.tick_goblin_narrator():
			_speaker.text = "Рассказчик"
			_body.text = "Так, я вернулся. Гоблин, пошёл вон из будки! Дальше комментирую я."
			await get_tree().create_timer(1.2).timeout
	GameState.save_game()
	_goto_next(next)


func _goto_next(next: String) -> void:
	if GameState.run_over:
		return
	if GameState.get_flag("pending_goblin_takeover"):
		await _trigger_goblin_takeover()
		## После передачи микрофона продолжаем квест (не на карту)
	if GameState.get_flag(&"goblin_just_left"):
		GameState.set_flag(&"goblin_just_left", false)
		_speaker.text = "Рассказчик"
		_body.text = "Так, я вернулся. Гоблин, пошёл вон из будки! Дальше комментирую я."
		await get_tree().create_timer(1.0).timeout
	if next == "__microloan__":
		var ml: Array = StubStoryScript.get_beats(&"event_microloans")
		if not ml.is_empty():
			var beat: Dictionary = (ml[0] as Dictionary).duplicate(true)
			var resume := GameState.microloan_resume_next
			if resume.is_empty():
				resume = "end"
			GameState.microloan_resume_next = ""
			for c in beat.get("choices", []):
				if c is Dictionary:
					c["next"] = resume
			_beat_by_id["microloans"] = beat
			_show_beat(beat)
			return
	if next == "end" or next == "":
		_finish_timeline()
	elif _beat_by_id.has(next):
		_show_beat(_beat_by_id[next])
	else:
		push_warning("StoryRunner: неизвестный next='%s' → end" % next)
		_finish_timeline()


func _format_effects(effects: Dictionary, item_id: String = "") -> String:
	var parts: PackedStringArray = []
	var keys := [
		["health", "❤️"], ["mental", "🧠"], ["gold", "💰"],
	]
	for pair in keys:
		var key: String = pair[0]
		if effects.has(key) and int(effects[key]) != 0:
			parts.append("%s %+d" % [pair[1], int(effects[key])])
	## Нарративные оси — без чисел в HUD, только flavor на карточке
	if effects.has("people") and int(effects["people"]) != 0:
		parts.append("🗣️ %s" % _narrative_delta("people", int(effects["people"])))
	if effects.has("crown") and int(effects["crown"]) != 0:
		parts.append("👑 %s" % _narrative_delta("crown", int(effects["crown"])))
	if effects.has("inquisition") and int(effects["inquisition"]) != 0:
		parts.append("⛪ %s" % _narrative_delta("inquisition", int(effects["inquisition"])))
	if effects.has("rating") and not effects.has("people"):
		parts.append("🗣️ %s" % _narrative_delta("people", int(effects["rating"])))
	if effects.has("cringe") and int(effects["cringe"]) != 0:
		parts.append("🐛 странный выбор")
	if effects.has("perk"):
		parts.append("перк: %s" % str(effects["perk"]))
	if effects.has("pen"):
		parts.append("загон: %s" % str(effects["pen"]))
	if effects.has("vital_bonus"):
		parts.append("❤️ пул %+d" % int(effects["vital_bonus"]))
	if not item_id.is_empty():
		parts.append("🎒 %s" % item_id)
	if parts.is_empty():
		return "без изменений статов"
	return " · ".join(parts)


func _narrative_delta(axis: String, delta: int) -> String:
	if delta > 0:
		match axis:
			"people":
				return "народ запомнил"
			"crown":
				return "Корона довольна"
			"inquisition":
				return "Инквизиция кивает"
			_:
				return "репутация +"
	else:
		match axis:
			"people":
				return "народ возмущён"
			"crown":
				return "Корона недовольна"
			"inquisition":
				return "Инквизиция хмурится"
			_:
				return "репутация −"


func _apply_effects(effects: Dictionary) -> void:
	GameState.apply_effects(effects)
	match str(effects.get("perk", "")):
		"millennial":
			GameState.on_perk_gained(GameState.Perk.MILLENNIAL)
		"obedient":
			GameState.on_perk_gained(GameState.Perk.OBEDIENT)
		"freak":
			GameState.on_perk_gained(GameState.Perk.FREAK)
		"veteran":
			GameState.on_perk_gained(GameState.Perk.VETERAN)
		"relocant":
			GameState.on_perk_gained(GameState.Perk.RELOCANT)


func _finish_timeline() -> void:
	if GameState.run_over:
		return
	GameState.mark_timeline_done(_timeline_id)
	GameState.save_game()
	match _timeline_id:
		&"act0_tutorial":
			SceneManager.to_story(&"act1_01_birth", "Нижние Вай-Файки")
		&"act1_01_birth":
			GameState.unlock_location(&"meme_tract")
			SceneManager.to_world_map()
		&"act1_road_stub":
			GameState.unlock_location(&"big_data")
			GameState.unlock_location(&"forge_service")
			SceneManager.to_world_map()
		&"act2_city_stub":
			GameState.unlock_location(&"castle_capital")
			GameState.unlock_location(&"relocant_forest")
			GameState.unlock_location(&"update_swamp")
			GameState.unlock_location(&"forge_service")
			GameState.set_flag(&"big_data_hub_open", true)
			# KPI стартует после брифинга в Замке (Акт 3), не после города
			SceneManager.to_world_map()
		&"act3_castle_stub":
			GameState.unlock_location(&"dragon_lair")
			GameState.start_kpi_timer()
			SceneManager.to_world_map()
		&"event_kpi_deadline":
			GameState.set_flag(&"pending_kpi_deadline", false)
			_continue_pending_or_map()
		&"event_people_riot", &"event_people_cancel", &"event_inq_wrath", &"event_inq_monk", &"event_crown_execute", &"event_crown_exile", &"event_cringe_king", &"event_microloans":
			_continue_pending_or_map()
		&"random_infogypsy", &"random_rtx", &"random_rain_tax", &"random_plantain_scam", &"random_api_fatal":
			_continue_pending_or_map()
		&"hub_big_data":
			SceneManager.to_world_map()
		&"forge_service":
			SceneManager.to_world_map()
		&"heavenly_hr":
			SceneManager.to_main_menu()
		&"ending_ctrl_ale", &"ending_bankruptcy", &"ending_soul_sub":
			GameState.register_death_title(&"burnout" if _timeline_id == &"ending_ctrl_ale" else (&"collectors" if _timeline_id == &"ending_bankruptcy" else &"death"))
			GameState.award_sins_for_death()
			SceneManager.to_story(&"heavenly_hr", "Небесная HR")
		&"side_forest_stub":
			GameState.unlock_location(&"update_swamp")
			SceneManager.to_world_map()
		&"side_swamp_stub":
			SceneManager.to_world_map()
		_:
			SceneManager.to_world_map()


func _continue_pending_or_map() -> void:
	var cont := GameState.pending_map_timeline
	var title := GameState.pending_map_title
	GameState.pending_map_timeline = &""
	GameState.pending_map_title = ""
	if cont != &"":
		SceneManager.to_story(cont, title)
	else:
		SceneManager.to_world_map()


func _on_game_over(reason: StringName) -> void:
	if _timeline_id == &"heavenly_hr":
		_speaker.text = "SYSTEM HALT"
		_body.text = "Даже смерть сломалась: %s." % String(reason)
		return
	var special := GameState.special_ending_timeline(reason)
	if special != &"":
		SceneManager.to_story(special, GameState.special_ending_title(special))
		return
	var go: Dictionary = GameState.prepare_hr_game_over(reason)
	_speaker.text = "GAME OVER"
	_body.text = "%s\n\n%s\n\nКрипто-Грехи: +%d (всего %d).\n🐛 Баги забега: ~%d (зачтут в HR).\nПереход в Небесную HR…" % [
		str(go["flavor"]),
		str(go["diploma"]),
		int(go["gained"]), int(go["sins"]),
		int(go["bugs"]),
	]
	for c in _choices.get_children():
		c.queue_free()
	var btn := Button.new()
	btn.text = "В Небесную канцелярию"
	btn.custom_minimum_size = Vector2(240, 48)
	btn.pressed.connect(func() -> void:
		SceneManager.to_story(&"heavenly_hr", "Небесная HR")
	)
	_choices.add_child(btn)


func _gold_blocked(choice: Dictionary) -> bool:
	if not choice.has("require_gold"):
		return false
	if choice.get("allow_debt", false):
		return false
	return GameState.gold < int(choice["require_gold"])


func _on_back_pressed() -> void:
	if _resolving or _undo_busy:
		return
	SceneManager.to_world_map()
