#!/bin/sh
# Собирает папку refs/ui_ref: опоры для генератора картинок, когда рисуем вещи интерфейса.
#   style_*.png — наши фоны: с них генератор берёт рисовку;
#   shape_*.jpg — мои наброски вещей на белом фоне: с них он берёт форму.
# Запуск из корня репозитория: sh refs/tools/make_ui_refs.sh   (нужны node и Chrome)
set -e
OUT=refs/ui_ref
mkdir -p "$OUT"
shot() { # имя вещи, ширина, высота, номер
  SHOT_W=$2 SHOT_H=$3 node web/tools/shot.mjs "file://$PWD/refs/tools/ui_pieces.html?p=$1" "$OUT" "w700,s:shape_$4_$1" >/dev/null
}
shot sheet 2100 900 01
shot card 1200 1600 02
shot shelf 2100 900 03
shot badge 900 1600 04
shot board 900 1600 05
shot buttons 1600 900 06
shot plate_ribbon 1600 900 07
shot note 1200 1200 08
shot system 2100 900 09
shot result 1600 1200 10
shot stamps 1600 900 11
shot icons 1200 1200 12
# рисовка: три наших фона в полном размере
cp assets_src/art/backgrounds/bg_act1_birth.png "$OUT/style_1_izba.png"
cp assets_src/art/backgrounds/bg_act1_first_word.png "$OUT/style_2_kolybel.png"
cp assets_src/art/backgrounds/bg_act3_cave.png "$OUT/style_3_peschera.png"
ls "$OUT"
