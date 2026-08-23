extends Node
## BGM: меню+карта = tavern; пролог/главы = march_b.
## Переключение по пути файла (не по id) + фейд, без резких обрывов.

signal bgm_changed(track_id: StringName)

const HUB_PATH := "res://assets/audio/bgm/foxfire_tavern_march.mp3"
const STORY_PATH := "res://assets/audio/bgm/foxfire_tavern_march_b.mp3"
## Запасной трек (пока не в ротации меню/пролога)
const ALT_PATH := "res://assets/audio/bgm/foxfire_corporate_crusade.mp3"

const BGM_PATHS: Dictionary = {
	&"menu": HUB_PATH,
	&"hub": HUB_PATH,
	&"map": HUB_PATH,
	&"village": HUB_PATH,
	&"road": HUB_PATH,
	&"city": HUB_PATH,
	&"castle": HUB_PATH,
	&"intro": STORY_PATH,
	&"story": STORY_PATH,
	&"dragon": STORY_PATH,
	&"game_over": HUB_PATH,
	&"alt": ALT_PATH,
}

const SFX_PATHS: Dictionary = {
	&"ui_click": "res://assets/audio/sfx/ui_click.ogg",
	&"choice": "res://assets/audio/sfx/choice.ogg",
	&"stat_up": "res://assets/audio/sfx/stat_up.ogg",
	&"stat_down": "res://assets/audio/sfx/stat_down.ogg",
	## Нищебродский клик — пока тот же «провал стата»; позже отдельный вуууп.
	&"pauper": "res://assets/audio/sfx/stat_down.ogg",
}

var _bgm: AudioStreamPlayer
var _sfx: AudioStreamPlayer
var _current_bgm: StringName = &""
var _current_path: String = ""
var _fade_tween: Tween
var _play_gen: int = 0


func _ready() -> void:
	_bgm = AudioStreamPlayer.new()
	_sfx = AudioStreamPlayer.new()
	_bgm.bus = &"Master"
	_sfx.bus = &"Master"
	add_child(_bgm)
	add_child(_sfx)


func play_bgm(track_id: StringName, fade_sec: float = 1.0) -> void:
	var path: String = str(BGM_PATHS.get(track_id, ""))
	if path.is_empty():
		return

	# Тот же файл уже играет (menu↔map) — не рестартим
	if path == _current_path and _bgm.playing:
		_current_bgm = track_id
		return

	_play_gen += 1
	var gen := _play_gen

	if not ResourceLoader.exists(path):
		await stop_bgm(fade_sec)
		if gen != _play_gen:
			return
		_current_bgm = track_id
		_current_path = ""
		bgm_changed.emit(track_id)
		return

	var stream: AudioStream = load(path) as AudioStream
	if stream == null:
		return
	_enable_loop(stream)

	_kill_fade()
	if _bgm.playing and fade_sec > 0.0:
		_fade_tween = create_tween()
		_fade_tween.tween_property(_bgm, "volume_db", -40.0, fade_sec)
		await _fade_tween.finished
		if gen != _play_gen:
			return

	_bgm.stop()
	_bgm.stream = stream
	_bgm.volume_db = -40.0
	_bgm.play()
	_current_bgm = track_id
	_current_path = path
	bgm_changed.emit(track_id)

	_kill_fade()
	_fade_tween = create_tween()
	_fade_tween.tween_property(_bgm, "volume_db", 0.0, maxf(fade_sec * 0.75, 0.35))


func stop_bgm(fade_sec: float = 0.6) -> void:
	if not _bgm.playing:
		_current_bgm = &""
		_current_path = ""
		return
	_kill_fade()
	if fade_sec > 0.0:
		_fade_tween = create_tween()
		_fade_tween.tween_property(_bgm, "volume_db", -40.0, fade_sec)
		await _fade_tween.finished
	_bgm.stop()
	_current_bgm = &""
	_current_path = ""


func play_sfx(sfx_id: StringName) -> void:
	var path: String = str(SFX_PATHS.get(sfx_id, ""))
	if path.is_empty() or not ResourceLoader.exists(path):
		return
	var stream: AudioStream = load(path) as AudioStream
	if stream == null:
		return
	_sfx.stream = stream
	_sfx.play()


func _kill_fade() -> void:
	if _fade_tween != null and _fade_tween.is_valid():
		_fade_tween.kill()
	_fade_tween = null


func _enable_loop(stream: AudioStream) -> void:
	if stream is AudioStreamMP3:
		(stream as AudioStreamMP3).loop = true
	elif stream is AudioStreamOggVorbis:
		(stream as AudioStreamOggVorbis).loop = true
