# Age of Litaries — Godot 4

Каркас повествовательной 2D-игры **«Сэр Баг»**.

> Дизайн-канон и все MD-документы: [`../MASTER.md`](../MASTER.md)

## Как открыть

1. Установи [Godot 4.3+](https://godotengine.org/download) (Standard).
2. **Project → Import** → укажи папку `game/` (файл `project.godot`).
3. F5 — запуск: меню → карта → карточки выборов.

CLI Godot на машине пока не найден — импорт через редактор.

## Структура

```
game/
  autoload/          GameState, SceneManager, AudioManager
  scenes/
    boot/            вход
    ui/              меню + HUD статов
    map/             глобальная карта
    story/           карточный раннер (заглушка до Dialogic)
  resources/
    locations/       LocationData
    story/           StubStory — временные биты из сюжета
  assets/audio/      bgm/ + sfx/ (пока пусто)
  addons/            сюда AssetLib → Dialogic 2
```

## Что уже работает

- ❤️10/10 · 🧠10/10 · 💰0 (долг ок) · 👑⛪🧑‍ фермер по 50 · 😳0/3
- инвентарь + флаги + перки
- карта с разблокировкой локаций
- заглушка Акта 1 + flip карточек + рассказчик
- AudioManager с id-треками (файлы можно кидать в `assets/audio/bgm`)

## Следующий шаг: Dialogic 2

1. AssetLib → найти **Dialogic** → Install в `addons/`.
2. Project → Project Settings → Plugins → включить Dialogic.
3. Variables: `Stats.Health/Mental/Gold/Crown/Inquisition/People/Cringe` (см. [`../tech_godot.md`](../tech_godot.md) §4).
4. Заменить `StubStory` на `Dialogic.start(timeline_id)`.

## Музыка

Слоты BGM: `menu`, `village`, `road`, `city`, `castle`, `dragon`, `game_over`.  
Формат: `.ogg` предпочтительно. Имена файлов — как в `AudioManager.BGM_PATHS`.
