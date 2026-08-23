extends CanvasLayer
## HUD: ❤️ Health · 🧠 Mental · 💰 Gold + мета (перк, KPI, гоблин, билд).

@onready var _health: Label = %Health
@onready var _gold: Label = %Gold
@onready var _mental: Label = %Mental

var _meta: Label
var _backlog_btn: Button


func _ready() -> void:
	GameState.stats_changed.connect(_refresh)
	_meta = Label.new()
	_meta.name = "Meta"
	_meta.add_theme_font_size_override("font_size", 14)
	_meta.add_theme_color_override("font_color", Color(0.95, 0.9, 0.75, 1))
	_meta.add_theme_color_override("font_outline_color", Color(0.05, 0.03, 0.02, 0.9))
	_meta.add_theme_constant_override("outline_size", 4)
	_meta.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	var row := get_node_or_null("Bar/Row")
	if row:
		row.add_child(_meta)
		_backlog_btn = Button.new()
		_backlog_btn.text = "Бэклог"
		_backlog_btn.custom_minimum_size = Vector2(72, 28)
		_backlog_btn.pressed.connect(_on_backlog_pressed)
		row.add_child(_backlog_btn)
	_refresh()


func _refresh() -> void:
	_health.text = "%d/%d" % [GameState.health, GameState.vital_max()]
	_mental.text = "%d/%d" % [GameState.mental, GameState.VITAL_MAX]
	_gold.text = "%d" % GameState.gold
	if _meta == null:
		return
	var bits: PackedStringArray = []
	var mq := GameState.main_quest_objective()
	if not mq.is_empty():
		bits.append(mq)
	var pl := GameState.perk_label()
	if not pl.is_empty():
		bits.append(pl)
	if GameState.get_flag(&"relic_medusa"):
		bits.append("Медуза")
	if GameState.get_flag(&"relic_hourglass"):
		bits.append("Часы")
	if GameState.get_flag(&"relic_jester"):
		bits.append("Шут")
	if not GameState.equipped_title.is_empty():
		bits.append("титул")
	if GameState.is_goblin_narrator():
		bits.append("👹ПМ %d" % GameState.goblin_narrator_turns)
	if GameState.kpi_days >= 0:
		bits.append("KPI %dд" % GameState.kpi_days)
	if GameState.credit_active:
		bits.append("Кредит")
	if GameState.run_index > 0:
		bits.append(GameState.build_version_label())
	if GameState.crypto_sins > 0:
		bits.append("Грехи %d" % GameState.crypto_sins)
	if GameState.total_bugs_found > 0:
		bits.append("🐛Σ%d" % GameState.total_bugs_found)
	if not GameState.backlog_cooking.is_empty():
		bits.append("💭%d" % GameState.backlog_turns_left)
	elif not GameState.backlog_pending.is_empty():
		bits.append("бэклог%d" % GameState.backlog_pending.size())
	_meta.text = " · ".join(bits)
	_meta.visible = not bits.is_empty()


func _on_backlog_pressed() -> void:
	var dlg := AcceptDialog.new()
	dlg.title = "Ментальный бэклог"
	dlg.min_size = Vector2(420, 280)
	var body := VBoxContainer.new()
	body.add_theme_constant_override("separation", 8)
	var info := Label.new()
	info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	if GameState.backlog_cooking != "":
		info.text = "Обдумывается: «%s» (%d хода, −1🧠/ход карты)." % [
			GameState.pen_label(GameState.backlog_cooking), GameState.backlog_turns_left
		]
	elif GameState.backlog_pending.is_empty() and GameState.compiled_ideas.is_empty():
		info.text = "Пусто. Идеи появляются из абсурда (инфоцыган, птицы-дроны, 5G, матрица…)."
	else:
		info.text = "Выбери идею — 3 хода карты на компиляцию (−1🧠/ход)."
	body.add_child(info)
	if GameState.backlog_cooking.is_empty():
		for pid in GameState.backlog_pending:
			var b := Button.new()
			b.text = "Обдумать: %s" % GameState.pen_label(str(pid))
			var pen := str(pid)
			b.pressed.connect(func() -> void:
				GameState.start_backlog_cook(pen)
				dlg.hide()
				dlg.queue_free()
			)
			body.add_child(b)
	if not GameState.compiled_ideas.is_empty():
		var done := Label.new()
		done.text = "Усвоено:"
		body.add_child(done)
		for k in GameState.compiled_ideas.keys():
			var l := Label.new()
			l.text = "• %s" % GameState.pen_label(str(k))
			body.add_child(l)
	dlg.add_child(body)
	add_child(dlg)
	dlg.popup_centered()
	dlg.confirmed.connect(dlg.queue_free)
	dlg.canceled.connect(dlg.queue_free)
