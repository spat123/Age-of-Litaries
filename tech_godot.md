# Godot: архитектура и интеграция (единый техдок)

> **Живой код = правда:** `game/README.md`, `game/autoload/game_state.gd`, `story_runner.gd`.  
> Dialogic — **опциональный** будущий слой; сейчас работает свой StoryRunner.  
> **Dev:** в debug-сборке StoryRunner — кнопка «← Отменить» / **Backspace** откатывает последний выбор (статы + экран).


---

## 1. Autoload (как в проекте)

| Singleton | Роль |
|-----------|------|
| `GameState` | Статы, инвентарь, флаги, NG+, KPI, бэклог, `run_over` |
| `SceneManager` | Меню / карта / стори; очередь переходов |
| `AudioManager` | BGM / SFX |

*В старых черновиках было имя `GameManager` — не использовать; везде `GameState`.*

---

## 2. Статы (канон = код)

См. [`systems.md`](./systems.md) §1.  
Устарело: единый `Rating` → только `people` / фракции.

Смерть: `GameState.run_over` + сигнал `game_over` (без двойных грехов).

---

## 3. Сюжетный раннер (сейчас)

- Сцена: `scenes/story/story_runner.tscn`  
- Биты: `resources/story/*.gd` (`stub_story.get_beats`)  
- Карточки: narrative / result / clarify / return  
- Мини-игры: `tinder_swipe.tscn`  
- Карта: `world_map.gd` → extreme / random / hub  

Типы выборов (канон UI) — в [`MASTER.md`](./MASTER.md).

---

## 4. Dialogic (опционально, план)

Если когда-нибудь подключим Dialogic 2:

### Variables (черновик имён)

`Stats.Health|Mental|Gold|Crown|Inquisition|People|Cringe`  
Инвентарь лучше держать в `GameState`, в Dialogic — проверки через кастомные условия / сигналы.

### Таймлайны

Дробить по актам: `act1_birth.dtl`, `act2_customs.dtl`, …  
Нарратив = ветка без flip; результат = сигнал/сцена переворота карточки (кастомный UI поверх Dialogic или наоборот).

### Пример вложенности (идея)

```
Рассказчик: двор, брат / дети
- [Сюжет] С братом → подварианты без flip
  - [Результат] … → flip + статы
```

Полные `.dtl` пока не ведутся — источник карточек = `act_*.md` + GDScript-биты.

---

## 5. Инвентарь / бэклог / KPI (как в коде)

| Система | Где |
|---------|-----|
| `has_item` / `add_item` | GameState |
| Авто-проклятие бита | `auto_curse` в StoryRunner |
| Бэклог | `queue_backlog_pen` / HUD кнопка / `tick_map_turn` |
| KPI | `start_kpi_timer` после замка |
| NG+ | `heavenly_hr.gd` + `legacy_buffs` |

Детали дизайна: [`systems.md`](./systems.md).

---

## 6. Сейв (API готов, UI Continue — частично)

`GameState.to_save_dict` / `from_save_dict` включают статы, флаги, KPI, credit, main_quest, run_over.  
Меню «Продолжить» пока может открывать карту без полного restore — добить при нужде.

---

## 7. Что читать дальше

1. [`game/README.md`](./game/README.md) — запуск проекта  
2. [`systems.md`](./systems.md) — механики  
3. [`MASTER.md`](./MASTER.md) — индекс всего  
