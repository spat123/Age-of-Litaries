# -*- coding: utf-8 -*-
# Три наброска целого экрана в разной подаче, через Codex. Сцена — «Первое слово» (изба ночью, колыбель).
# Запуск из корня репозитория: python3 <этот файл> [номера через запятую]
import os, subprocess, sys

OUT = "refs/ui_mock/concepts"
os.makedirs(OUT, exist_ok=True)
SCENE = "assets_src/art/backgrounds/bg_act1_first_word.png"
PEOPLE = "assets_src/art/backgrounds_old/bg_act1_first_word.png"

STYLE = ("Drawing style of @img1: a 2D animated cartoon series look, clean confident thick outlines in a darker shade "
         "of each colour, flat opaque colours, cel shading with two or three hard-edged tones, fine grain texture, "
         "chunky rounded shapes.")
TAIL = ("Everything is drawn in one consistent style, the interface looks hand-crafted and belongs to the world. "
        "No readable text anywhere: all writing is illegible placeholder squiggles, all labels are blank. "
        "No logos, no brand marks. Do not copy the interface of any existing game.")

C1 = ("A complete screenshot mockup of the game screen of a satirical medieval card-choice game, wide 3:2. " + STYLE + "\n\n"
      "Use @img1 as the scene: the cottage interior at night with the cradle fills the whole screen as the background, "
      "slightly darkened, with a vignette. Use @img2 only to see what the mother looks like (headscarf, apron, kind but "
      "demanding face); redraw her in the style of @img1.\n\n"
      "Layout. On the left, a large waist-up portrait of the mother leans into the frame from the left edge and looks at the "
      "viewer with a demanding smile; she overlaps the left end of a big dialogue panel at the top. The dialogue panel is a "
      "thick carved wooden frame with brass corner fittings around a cream parchment page; her name is on a small painted "
      "wooden sign nailed to the top edge, the scene title on a red cloth ribbon at the right end. At the bottom, three tall "
      "choice cards stand in a slightly fanned row on a carved wooden shelf: each card has an ornate carved wooden frame, a "
      "large illustration inside a coloured window (an open talking mouth with a speech bubble; a pointing hand; a finger "
      "pressed to lips), a caption plate below, and a round brass number token on the top-left corner; the middle card is "
      "lifted and glows warmly as if hovered. Upper left: a hanging carved wooden sign with four stat icons (red heart, pink "
      "brain, wheat sheaf crossed with a pitchfork, stack of gold coins), each with a bold number and a segmented bar. Upper "
      "right: a small wooden board with three empty card slots and a chunky wooden button below it. Strong hierarchy: the "
      "panel, the mother and the cards are the brightest, most detailed things; rich crafted details: rivets, stitching, "
      "carved corners, small icons on buttons.\n\n" + TAIL)

C2 = ("A complete screenshot mockup of the game screen of a satirical medieval card-choice game, wide 3:2. " + STYLE + "\n\n"
      "Concept: the hero's life is a personnel file being reviewed in a heavenly office. The whole screen is the top of an "
      "old oak desk seen straight from above, lit by a warm candle. In the centre lies an open thick cardboard personnel "
      "folder with a metal clip. On its left page, an illustration of the current scene is attached with a paper clip like "
      "a photograph: the cottage interior from @img1, redrawn in the same style, with a small stamp in its corner. On its "
      "right page, a sheet with a bold heading and placeholder lines. Below the folder, three choice cards lie on the desk "
      "like official request slips, each with a small illustration box (an open talking mouth; a pointing hand; a finger "
      "pressed to lips), a checkbox and a round red wax seal, slightly overlapping; the middle one is lifted as if picked up. "
      "Around the folder, the hero's four stats are objects on the desk, each with a paper tag and a bold number: a red "
      "heart-shaped pincushion, a small glass jar with a pink brain, a wheat sheaf with a little pitchfork, a stack of gold "
      "coins. Top right: a cork board with three pinned cards. A rubber stamp, an inkwell with a goose quill and the candle "
      "complete the desk. Warm light, cool blue-grey shadows.\n\n" + TAIL)

C3 = ("A complete screenshot mockup of the game screen of a satirical medieval card-choice game, wide 3:2. " + STYLE + "\n\n"
      "Concept: the medieval world is an unfinished software build. The cottage interior at night from @img1 fills the screen "
      "as the background, but toward the screen edges the painted scene turns into thin glowing turquoise construction lines, "
      "grid and measurement marks, like a blueprint of the room. The interface is medieval craft mixed with these turquoise "
      "debug overlays. At the top, a big cream parchment dialogue panel with a thick dark brown outline; its right end is "
      "still unfinished: drawn only as a glowing turquoise wireframe outline, with small turquoise arrows, brackets and "
      "measurement ticks pointing at it; the speaker's name is on a wooden sign with a blank turquoise label stuck to it. At "
      "the bottom, three hand-made choice cards with wooden frames and illustrations in coloured windows (an open talking "
      "mouth; a pointing hand; a finger pressed to lips); the third card is only half finished: its lower half is a turquoise "
      "wireframe. On the left, the hero's stats on a cream pass badge hanging on red straps: four icons (red heart, pink brain, "
      "wheat sheaf crossed with a pitchfork, gold coins) with bold numbers and segmented bars, framed by small turquoise "
      "selection handles. A thin turquoise frame with corner brackets runs around the whole screen.\n\n" + TAIL)

JOBS = {1: ("c1_scena_s_geroyami.png", C1, [SCENE, PEOPLE]), 2: ("c2_lichnoe_delo.png", C2, [SCENE]), 3: ("c3_mir_v_razrabotke.png", C3, [SCENE])}
only = {int(x) for x in sys.argv[1].split(",")} if len(sys.argv) > 1 else set(JOBS)
for n in sorted(only):
    name, prompt, refs = JOBS[n]
    cmd = [sys.executable, "web/tools/codex_image.py", "--out", os.path.join(OUT, name), "--size", "wide"]
    for r in refs:
        cmd += ["--ref", r]
    print("==", name, flush=True)
    r = subprocess.run(cmd + [prompt], capture_output=True, text=True)
    print((r.stdout + r.stderr).strip(), flush=True)
print("готово")
