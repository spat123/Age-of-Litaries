# -*- coding: utf-8 -*-
# Пробный набор рисунков во всё окно карточки (автор: «попробуем сейчас сделать небольшой набор картинок для карточек,
# которые внутри»; образец — наброски карточек refs/ui_mock/cards/v3_arka.png). Квадрат 1:1, цветной фон с лучами,
# крупный план, движение. Кладёт в assets_src/cards_full/<рисунок>.png; в игру — web/tools/prepare_card_full.py.
# Запуск из корня репозитория: python3 refs/tools/ui_gen/gen_card_art.py [имена через запятую]
import os, subprocess, sys

OUT = "assets_src/cards_full"
os.makedirs(OUT, exist_ok=True)
REF = "refs/ui_mock/cards/v3_arka.png"
HEAD = ("@img1 shows choice cards from our game mockup. Draw one card picture in exactly the same drawing style as the "
        "pictures inside the cards in @img1: a 2D animated cartoon look, clean confident thick outlines in a darker shade of "
        "each colour, flat opaque colours with cel shading in two or three hard-edged tones, chunky rounded shapes, a big "
        "close-up full of motion, cropped by the picture edges, on a bold single-colour background with radiating speed "
        "lines. The picture is square and fills the whole image edge to edge: no frame, no border, no margin, no caption "
        "plate. The subject: ")
TAIL = " No text, no letters, no numbers, no logos."
JOBS = {
    "g_mouth": "a peasant boy's wide-open shouting mouth seen close up from the side, with a white speech bubble bursting "
               "out of it, on a bright red background.",
    "g_eyes": "a peasant boy's face in close-up with big curious eyes and one eyebrow raised, asking a question, a small "
              "question mark hovering beside him, on a bright blue background.",
    "g_silence": "the lower half of a peasant boy's face in close-up, a finger pressed to his lips to keep quiet, on a "
                 "purple background.",
    "o_birds": "a sly black crow looking through a small brass spyglass, spying, on a deep night-teal background.",
    # вторая пачка (автор: «Да, следующие») — самые частые рисунки в сюжете; где есть мальчик, опора — он же с g_eyes
    "g_coins": "a peasant boy's open hand, palm up, holding three shiny gold coins, coins glinting, on a warm orange "
               "background.",
    "g_sit": "the boy from @img2 sitting on a small crooked three-legged wooden stool, arms crossed, stubborn and not "
             "moving, on a green background.",
    "g_walk_by": "the boy from @img2 walking past with his nose in the air, pretending not to notice anything, a trail "
                 "of muddy footprints behind him, on a light blue background.",
    "g_hug": "the boy from @img2 hugging a big soft red heart with both arms, eyes closed, happy, on a pink background.",
    "g_shout": "the boy from @img2 shouting into a dented copper speaking trumpet, sound lines bursting out of it, on a "
               "yellow background.",
    "o_wooden_phone": "a smartphone carved from a slab of tree bark, with a cracked screen made of a thin slice of resin "
                      "glowing faintly, held in a peasant hand, on a teal background.",
    "g_point": "a peasant boy's hand pointing straight forward with the index finger, sleeve of rough linen, seen in "
               "strong perspective, on a bright blue background.",
    "g_hand_take": "a peasant boy's open hand reaching forward to grab something, fingers spread, in strong "
                   "perspective, on a bright green background.",
}
HERO = "assets_src/cards_full/g_eyes.png"

# Третья пачка (автор: «телефон без руки нужно, и в целом ужасно именно телефон получился… Я бы генерил без фона,
# чтобы фоны делать потом самим»): дальше рисуем без фона — на чистом белом; цветной фон с лучами ставит игра.
CLEAN = ("@img1 shows choice cards from our game mockup. Draw one card picture in exactly the same drawing style as the "
         "pictures inside the cards in @img1: a 2D animated cartoon look, clean confident thick outlines in a darker "
         "shade of each colour, flat opaque colours with cel shading in two or three hard-edged tones, chunky rounded "
         "shapes, full of character. Only the subject, centred, filling most of the square, on a plain pure white "
         "background: no coloured background, no speed lines, no rays, no frame, no shadow on the background. The subject: ")
JOBS_CLEAN = {
    # вторая попытка (автор: «у нас же телефон был больше похож на дерево с логотипом сзади»): как старый рисунок
    # assets_src/cards_new/o_wooden_phone.png — кусок коры сзади, вырезанная репка вместо логотипа, мох, жук
    "o_wooden_phone": "exactly the object from @img2, redrawn in our new style: a smartphone carved from a slab of grey "
                      "tree bark, seen from the back, with rounded corners, deep bark grooves, patches of green moss on "
                      "the corners and a crack stitched with twine. A turnip is carved into its back like a logo. In the "
                      "upper corner one round knot hole instead of a camera. A small bark beetle sits on its top edge. "
                      "A turquoise glow leaks from under its side. No camera lenses, no hands.",
    # третья пачка (автор: «Да, топ. Давай дальше делать»): @img2 — прежний рисунок этой вещи (держим задумку),
    # @img3 — лист героя в четырёх возрастах (assets_src/hero/hero_ages.png), где на рисунке герой
    "o_foil_hat": "exactly the idea of @img2 redrawn in our new style: the boy from @img3 (the eight-year-old) proudly "
                  "wearing a dented tin bucket upside down as a hat, tied under his chin with a rope, looking suspicious "
                  "and determined. Head and shoulders.",
    "o_contract": "exactly the idea of @img2 redrawn in our new style: a very long parchment scroll unrolling and "
                  "tumbling down in loops, covered with tiny illegible scribbles, a heavy red wax seal at the bottom.",
    "g_fist": "the boy from @img3 (the eight-year-old) raising a clenched fist high, fierce determined face, head, "
              "shoulders and the raised arm.",
    "g_run": "the boy from @img3 (the eight-year-old) running away as fast as he can, legs blurred, kicking up a small "
             "cloud of dust, looking back over his shoulder in panic. Full body.",
    "g_sleep": "the baby from @img3 fast asleep on a plump straw pillow, wearing a tiny pointed nightcap, three small sleep "
               "bubbles floating above.",
    "g_pray": "the boy from @img3 (the eight-year-old) with his hands pressed together in prayer, eyes closed, a hopeful "
              "face. Head, shoulders and hands.",
    "o_letter": "exactly the object from @img2 redrawn in our new style: a folded piece of birch bark tied with a red "
                "thread, slightly crumpled, one corner worn.",
    "o_pig": "exactly the idea of @img2 redrawn in our new style: a cheerful pink pig with a wooden shovel tied to its back "
             "with rope, trotting happily. Full body.",
    # четвёртая пачка (автор: «Да, дальше»)
    "o_stick": "exactly the object from @img2 redrawn in our new style: the perfect straight wooden stick with a small "
               "fork at the end and a strip of bark left on it, shown big and proud, with a tiny sparkle.",
    "o_goose": "exactly the idea of @img2 redrawn in our new style: a bossy white goose standing proudly with its chest "
               "out, looking sideways with one suspicious eye. Full body.",
    "o_wooden_sword": "the boy from @img3 (the eight-year-old) holding up a toy sword carved from one board, with a crooked "
                      "crossguard tied on with string, in a heroic pose. Head, shoulders and the sword.",
    "o_scroll_speech": "exactly the object from @img2 redrawn in our new style: a thick rolled paper scroll tied with a "
                       "ribbon, a second sheet sticking out.",
    "o_purse": "exactly the object from @img2 redrawn in our new style: a small leather drawstring purse, bulging, with "
               "two gold coins peeking out.",
    "g_write": "a peasant hand holding a goose quill and writing on a piece of birch bark covered with illegible "
               "scribbles, in close-up.",
    "o_battle_pass": "exactly the object from @img2 redrawn in our new style: a rectangular piece of birch bark with a "
                     "large round red wax seal and a bright ribbon hanging from it, covered with decorative illegible "
                     "marks.",
    "o_guild_mages": "exactly the object from @img2 redrawn in our new style: a glowing crystal ball on a carved wooden "
                     "stand, with a small hourglass floating inside it.",
    "o_tin_armor": "the teenager from @img3 wearing a dented, far too large iron breastplate with mismatched shoulder "
                   "plates and loose hanging straps, looking proud and awkward. Head and torso.",
    "g_sing": "the boy from @img3 (the eight-year-old) singing loudly with his mouth wide open and eyes closed, three "
              "musical notes flying out. Head and shoulders.",
    # пятая пачка (автор: «Да, дальше»): вещи, задумка — с прежнего рисунка @img2
    "o_slate": "exactly the object from @img2 redrawn in our new style: a wooden wax writing tablet with a stylus, the wax scratched with illegible marks.",
    "o_barn": "exactly the object from @img2 redrawn in our new style: a small crooked wooden shed with a thatched roof and a half-open door.",
    "o_birch_letter": "exactly the object from @img2 redrawn in our new style: a fresh strip of birch bark with a few scratched illegible lines and a small heart, a sharpened stick lying next to it.",
    "o_church_book": "exactly the object from @img2 redrawn in our new style: a very thick old record book with a leather cover, an iron clasp and many bookmarks sticking out.",
    "o_quill_blot": "exactly the object from @img2 redrawn in our new style: a goose quill lying next to a big ink blot on a piece of parchment.",
    "o_helmet_stone": "exactly the object from @img2 redrawn in our new style: a simple iron soldier's helmet lying next to a big round grey boulder.",
    "o_closet": "exactly the object from @img2 redrawn in our new style: a tiny low door under a wooden staircase, slightly open, a big iron key hanging on a nail beside it.",
    "o_empty_book": "exactly the object from @img2 redrawn in our new style: a thick open book with completely blank pages and a small red stamp mark at the bottom of each page.",
    "o_shovel": "exactly the object from @img2 redrawn in our new style: a wooden shovel with an iron-edged blade stuck into a small pile of earth.",
    "o_tooth": "exactly the object from @img2 redrawn in our new style: one small white baby tooth lying on a scrap of cloth.",
    "o_salt_turnip": "exactly the object from @img2 redrawn in our new style: a small cloth sack of salt, tied at the top, with a big yellow turnip leaning against it.",
    "o_scroll_pass": "exactly the object from @img2 redrawn in our new style: a fancy golden scroll with tassels, partly unrolled to show a clumsy drawing of a mammoth.",
    "o_pacifier": "exactly the object from @img2 redrawn in our new style: a wooden baby pacifier with a ring, a tiny price tag tied to the ring.",
    "o_dragon_hoard": "exactly the object from @img2 redrawn in our new style: an old tired dragon lying curled up on a pile of gold coins, chin resting on its paws, one eye half open.",
    # шестая пачка (автор: «Да, дальше»)
    "o_coffee": "exactly the object from @img2 redrawn in our new style: a clay cup of hot coffee with steam rising, standing on a small wooden saucer, two roasted coffee beans beside it.",
    "o_pitchfork": "exactly the object from @img2 redrawn in our new style: a wooden pitchfork with three prongs, mud on the tips.",
    "o_sack": "exactly the object from @img2 redrawn in our new style: a heavy bulging burlap sack tied with rope, a patch sewn on its side.",
    "o_guild_warriors": "exactly the object from @img2 redrawn in our new style: a round wooden shield with an iron boss and two crossed swords behind it.",
    "o_diploma": "exactly the object from @img2 redrawn in our new style: a rolled diploma scroll with a big beet-red wax seal on a ribbon.",
    "o_socks": "exactly the object from @img2 redrawn in our new style: a pair of thick hand-knitted woollen socks with a clumsy pattern, one slightly bigger than the other.",
    "o_well": "exactly the object from @img2 redrawn in our new style: a village stone well with a wooden roof, a rope and a bucket.",
    "g_tear": "the idea of @img2 redrawn in our new style; where a person or a hand is shown, it is the boy from @img3 (the eight-year-old): a sheet of birch bark torn in two halves, small scraps flying.",
    "g_cry": "the idea of @img2 redrawn in our new style; where a person or a hand is shown, it is the boy from @img3 (the eight-year-old): a squeezed-shut eye with big tears spraying out to both sides.",
    "g_tongue": "the idea of @img2 redrawn in our new style; where a person or a hand is shown, it is the boy from @img3 (the eight-year-old): a cheeky mouth sticking its tongue out.",
    "o_puddle": "exactly the object from @img2 redrawn in our new style: a muddy puddle with one coin glinting at the bottom.",
    "o_mud_castle": "exactly the object from @img2 redrawn in our new style: a lumpy castle built of mud with a twig for a flagpole and a leaf for a flag.",
    "o_potato_game": "exactly the object from @img2 redrawn in our new style: four little figurines carved from potatoes standing on a board marked with squares.",
    "o_nettle": "exactly the object from @img2 redrawn in our new style: a thick bush of stinging nettles.",
    "o_beetle": "exactly the object from @img2 redrawn in our new style: a small brown bark beetle on a piece of bark, with tiny tunnels gnawed around it.",
    "o_fence": "exactly the object from @img2 redrawn in our new style: a section of a tall wooden plank fence with one loose board swung aside.",
    "o_gate_knock": "exactly the object from @img2 redrawn in our new style: a heavy wooden gate with an iron ring knocker.",
    "o_guild_thieves": "exactly the object from @img2 redrawn in our new style: a dark hooded cloak hanging on a hook, a big ring of mismatched keys hanging beside it.",
    "o_portraits": "exactly the object from @img2 redrawn in our new style: three small portraits scratched on pieces of birch bark, laid out in a row, the faces simple and funny.",
    "o_kvass": "exactly the object from @img2 redrawn in our new style: a wooden mug of kvass with a thick cap of foam running over the edge.",
    # автор: «есть лопата отдельно и лопата со свиньёй — я бы сделал, чтобы лопата была одинаковая»
    "o_pig2": "the same cheerful pink pig as in @img2, trotting happily, with a shovel tied to its back with rope; the "
              "shovel must be exactly the shovel from @img3: the same wooden handle with the D-shaped grip, the same "
              "iron-edged blade, the same colours. Full body.",
    # седьмая пачка — последние (автор: «И давай дорисуем»)
    "o_bellows": "exactly the object from @img2 redrawn in our new style: a big leather blacksmith's bellows with wooden handles.",
    "o_jam": "exactly the object from @img2 redrawn in our new style: a clay jar of red jam covered with a cloth tied with string, a wooden spoon beside it.",
    "o_sand": "exactly the object from @img2 redrawn in our new style: a hand throwing a handful of sand, the grains flying in a fan.",
    "o_horse": "exactly the object from @img2 redrawn in our new style: an old tired grey horse with a sagging back and a patched saddle, standing half asleep.",
    "o_knight": "exactly the object from @img2 redrawn in our new style: a stout medieval knight in heavy, dented, patched plate armour, frozen in the middle of a step with one foot in the air, as if stuck. Closed helmet with a narrow visor and a bent feather, a small chipped shield on his back. Three faint turquoise after-images of his raised foot trail behind it.",
    "o_scar": "a new picture in our style (there is no earlier drawing): a bare forearm with a rolled-up sleeve of rough linen, the hand relaxed and open, an old pale zigzag scar with small stitch marks running across the forearm.",
    "o_remembered": "a new picture in our style (there is no earlier drawing): a simple wooden village bench with gifts left on it: a bunch of daisies tied with string, a round loaf of bread on a cloth and a small clay jug.",
    "o_potion": "exactly the object from @img2 redrawn in our new style: a small round glass bottle with a cork and a bubbling purple liquid, a blank paper label tied to its neck.",
    "o_lute": "exactly the object from @img2 redrawn in our new style: a worn lute with one broken string curling up.",
    "o_tent_gold": "exactly the object from @img2 redrawn in our new style: a small round fortune-teller's tent of gilded cloth with stars sewn on it and a curtain for a door.",
    "o_goblin_box": "exactly the object from @img2 redrawn in our new style: a tipsy old green goblin sitting by a ditch and thumping a rusty iron box with his fist.",
    "o_smoothie_cup": "exactly the object from @img2 redrawn in our new style: a clay mug filled with a thick green drink, a reed straw sticking out of it.",
    # первая попытка вышла непонятной (два круга с бровями) — лицо героя, зажмурившегося от страха
    # встречается только при рождении — значит, зажмуривается младенец
    "g_eyes_shut": "the baby from @img3 in linen swaddling clothes squeezing his eyes tightly shut, face scrunched up, "
                   "tiny fists pressed to his cheeks, waiting for it all to be over.",
    "o_shovels": "exactly the object from @img2 redrawn in our new style: a pile of five small children's wooden toy shovels thrown together.",
    "o_candy": "exactly the object from @img2 redrawn in our new style: a red sugar lollipop shaped like a rooster on a wooden stick.",
    "o_twig": "exactly the object from @img2 redrawn in our new style: a long thin flexible twig with two small leaves left on its tip.",
    "o_coin_splash": "exactly the object from @img2 redrawn in our new style: a single coin falling into dark water with a small round splash.",
    "o_cake": "exactly the object from @img2 redrawn in our new style: a round golden pie on a wooden board, one slice missing.",
    "o_plate": "exactly the object from @img2 redrawn in our new style: a full wooden plate with a roasted chicken leg, bread and a pickle, nothing eaten.",
    "o_signpost": "exactly the object from @img2 redrawn in our new style: a wooden signpost with two blank arrow boards pointing in opposite directions.",
}
# автор: «надо вырезать фон у тех, чтоб нормально вставлять» — первые 11 рисунков с нарисованным фоном
# перерисовываем той же картинкой на белом (прежние сохранены в assets_src/cards_full_bg/)
if len(sys.argv) > 1 and sys.argv[1] == "white":
    for n in sys.argv[2].split(","):
        old = "assets_src/cards_full_bg/" + n + ".png"
        p = ("@img1 is a picture from our game. Redraw exactly the same picture — the same subject, pose, crop, drawing "
             "style, outlines and colours — but remove the coloured background and the speed lines completely: only the "
             "subject on a plain pure white background, no shadow. No text, no letters, no logos.")
        r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", os.path.join(OUT, n + ".png"),
                            "--size", "square", "--ref", old, p], capture_output=True, text=True)
        print(n + ": " + (r.stdout + r.stderr).strip()[-40:], flush=True)
    sys.exit(0)
if len(sys.argv) > 1 and sys.argv[1] == "clean":
    for n in (sys.argv[2].split(",") if len(sys.argv) > 2 else list(JOBS_CLEAN)):
        old = "assets_src/cards_new/" + n + ".png"
        refs = ["--ref", REF, "--ref", old if os.path.exists(old) else REF]
        if "@img3" in JOBS_CLEAN[n]:
            refs += ["--ref", "assets_src/hero/hero_ages.png"]
        r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", os.path.join(OUT, n + ".png"),
                            "--size", "square"] + refs + [CLEAN + JOBS_CLEAN[n] + TAIL], capture_output=True, text=True)
        print(n + ": " + (r.stdout + r.stderr).strip()[-120:], flush=True)
    sys.exit(0)  # тот же мальчик на всех рисунках


def run(name):
    refs = ["--ref", REF] + (["--ref", HERO] if "@img2" in JOBS[name] else [])
    r = subprocess.run([sys.executable, "web/tools/codex_image.py", "--out", os.path.join(OUT, name + ".png"),
                        "--size", "square"] + refs + [HEAD + JOBS[name] + TAIL], capture_output=True, text=True)
    return name + ": " + (r.stdout + r.stderr).strip()[-200:]


only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(JOBS)
# строго по очереди: при одновременном запуске Codex путает картинки (две пришли копиями чужих)
for n in only:
    print(run(n), flush=True)
print("готово")
