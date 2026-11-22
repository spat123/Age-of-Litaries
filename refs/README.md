# refs — образцы и страницы для просмотра

| Что | Где | В git |
|-----|-----|-------|
| Скриншоты 25 игр-образцов | `screens/<игра>/NN.jpg`, сведения в `screens/meta.json` | нет — чужие картинки |
| Страница с разбором образцов | `obraztsy.html` | нет — собирается скриптом |
| Страница с предложениями | `predlozheniya.html` | нет — собирается скриптом |
| Образцы интерфейса Hades II: кадры, крупные планы рамок и иконок | `screens/ui/hades2/`, качает `tools/fetch_hades2.py` | нет — чужие картинки |
| Страница с разбором Hades II | `hades2.html`, собирает `tools/build_hades2_page.py` | нет — собирается скриптом |
| Скрипты | `tools/` | да |

Текст разбора лежит в корне: [`references.md`](../references.md). Он тоже собирается скриптом — править текст нужно в `tools/build_refs_page.py`.

## Собрать заново

Из корня репозитория, нужен Python 3 с Pillow:

```bash
python3 refs/tools/fetch_screens.py
```

```bash
python3 refs/tools/build_refs_page.py
```

```bash
python3 refs/tools/build_proposals_page.py
```

Первая команда качает скриншоты со страниц Steam и itch.io. Вторая собирает `obraztsy.html` и `references.md`. Третья собирает `predlozheniya.html`: промпты берёт из `art_style.md`, остальной текст записан в самом скрипте и повторяет `rework_plan.md`.

## Посмотреть в приложении

В `.claude/launch.json` есть запись `refs-pages`: она раздаёт эту папку по адресу `http://localhost:8765`.
