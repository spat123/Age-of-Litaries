// Картинки игры. Чтобы добавить новую, достаточно положить файл с нужным именем:
//   web/assets/bg/<имя фона>.webp      — фон сцены, имя как в story/*.json (поле bg)
//   web/assets/cards/<имя картинки>.png — картинка карточки, имя как в story/*.json (поле art)
//   web/assets/icons/<показатель>.png   — значок показателя: body, mind, gold, rep
//   web/assets/ui/<вещь>.webp           — рисованная вещь интерфейса, её края — в web/assets/ui/ui.json (готовит web/tools/cut_ui.py)
// Пока картинки карточки нет, на её месте стоит временный значок из таблицы ниже.
import bgInfo from "../../story/bg.json";
import Phaser from "phaser";

const globs = {
  ...import.meta.glob("../assets/bg/*.{jpg,png,webp}", { eager: true, query: "?url", import: "default" }),
  ...import.meta.glob("../assets/cards/*.{jpg,png,webp}", { eager: true, query: "?url", import: "default" }),
  ...import.meta.glob("../assets/ui/*.{png,webp}", { eager: true, query: "?url", import: "default" }),
  ...import.meta.glob("../assets/faces/*.{png,webp}", { eager: true, query: "?url", import: "default" }),
} as Record<string, string>;
const icons = import.meta.glob("../assets/icons/*.png", { eager: true, query: "?url", import: "default" }) as Record<string, string>;

const name = (p: string) => p.split("/").pop()!.replace(/\.[a-z]+$/, "");
export const TEX: Record<string, string> = {};
for (const [p, u] of Object.entries(globs)) TEX[name(p)] = u;
for (const [p, u] of Object.entries(icons)) TEX["icon_" + name(p)] = u;
// рисунок во всё окно карточки (новый, 1:1, с цветным фоном): web/assets/cards_full/<рисунок>.webp → «full_<рисунок>»
const full = import.meta.glob("../assets/cards_full/*.{png,webp}", { eager: true, query: "?url", import: "default" }) as Record<string, string>;
for (const [p, u] of Object.entries(full)) TEX["full_" + name(p)] = u;
// нарисованные фоны с лучами под рисунки без фона: web/assets/card_bg/<цвет>.webp → «cbg_<цвет>»
const cbg = import.meta.glob("../assets/card_bg/*.webp", { eager: true, query: "?url", import: "default" }) as Record<string, string>;
for (const [p, u] of Object.entries(cbg)) TEX["cbg_" + name(p)] = u;
// значки уникальных карточек для ячеек (готовые 192 точки): web/assets/card_icons/<рисунок>.webp → «cico_<рисунок>»
const cico = import.meta.glob("../assets/card_icons/*.webp", { eager: true, query: "?url", import: "default" }) as Record<string, string>;
for (const [p, u] of Object.entries(cico)) TEX["cico_" + name(p)] = u;
// гербы титулов: web/assets/crests/<титул>.webp → «crest_<титул>» (готовит web/tools/prepare_crests.py)
const crest = import.meta.glob("../assets/crests/*.webp", { eager: true, query: "?url", import: "default" }) as Record<string, string>;
for (const [p, u] of Object.entries(crest)) TEX["crest_" + name(p)] = u;

/** Фон, которого ещё нет, заменяется похожим. */
// Запасной фон: что показывать, пока своего рисунка у места нет. Берётся из story/bg.json (поле now).
export const BG_FALLBACK: Record<string, string> = { bg_home_day: "bg_act1_first_word" };
for (const [k, v] of Object.entries<any>(bgInfo)) if (v && v.now) BG_FALLBACK[k] = v.now;

/** Чёрный силуэт рисованной вещи: из него делается её жёсткая тень. Имя — с «_sh» на конце. */
function shadowOf(scene: Phaser.Scene, key: string, img: HTMLImageElement) {
  const c = document.createElement("canvas");
  c.width = img.width;
  c.height = img.height;
  const x = c.getContext("2d")!;
  x.drawImage(img, 0, 0);
  x.globalCompositeOperation = "source-in";
  x.fillStyle = "#000";
  x.fillRect(0, 0, c.width, c.height);
  scene.textures.addCanvas(key + "_sh", c);
}

/** Загружает все картинки. Работает и с обычными адресами, и со вшитыми в файл. */
export function loadTextures(scene: Phaser.Scene): Promise<void[]> {
  return Promise.all(
    Object.entries(TEX).map(
      ([key, url]) =>
        new Promise<void>((res) => {
          const img = new Image();
          img.onload = () => {
            scene.textures.addImage(key, img);
            if (key.startsWith("ui_")) shadowOf(scene, key, img);
            res();
          };
          img.onerror = () => res();
          img.src = url;
        }),
    ),
  );
}

/** Временные значки вместо картинок карточек. */
export const PLACEHOLDER: Record<string, string> = {
  g_coins: "🪙", g_cry: "😭", g_eyes: "👀", g_eyes_shut: "😣", g_fist: "✊", g_hand_take: "🤲", g_hug: "🤗", g_mouth: "💬", g_point: "👉", g_pray: "🙏",
  g_run: "🏃", g_shout: "📢", g_silence: "🤫", g_sing: "🎵", g_sit: "🪑", g_sleep: "😴", g_tear: "💔", g_tongue: "😛", g_walk_by: "🚶", g_write: "✍️",
  o_barn: "🛖", o_battle_pass: "🏷️", o_beetle: "🪲", o_birch_letter: "💌", o_birds: "🐦", o_cake: "🥧", o_candy: "🍭", o_church_book: "📖",
  o_coin_splash: "💧", o_contract: "📜", o_fence: "🪜", o_foil_hat: "🪣", o_gate_knock: "🚪", o_goblin_box: "📦", o_goose: "🦢",
  o_helmet_stone: "🪨", o_knight: "🛡️", o_letter: "✉️", o_lute: "🪕", o_mud_castle: "🏰", o_nettle: "🌿", o_pacifier: "🍼", o_pig: "🐖",
  o_pitchfork: "🔱", o_potato_game: "🥔", o_potion: "🧪", o_puddle: "💦", o_purse: "👛", o_quill_blot: "🪶", o_sack: "💰",
  o_salt_turnip: "🧂", o_scroll_pass: "📃", o_scroll_speech: "📣", o_shovel: "⛏️", o_shovels: "🧹", o_slate: "📝", o_smoothie_cup: "🥤",
  o_stick: "🥢", o_tent_gold: "⛺", o_tooth: "🦷", o_twig: "🌾", o_well: "🪣", o_wooden_phone: "📱", o_wooden_sword: "🗡️",
  o_guild_warriors: "⚔️", o_guild_mages: "🔮", o_guild_thieves: "🗝️", o_tin_armor: "🛡️", o_closet: "🚪", o_diploma: "🎓", o_socks: "🧦",
  o_jam: "🍯", o_empty_book: "📕", o_sand: "⏳", o_kvass: "🍺", o_barrel: "🛢️", o_bellows: "🔨", o_portraits: "🖼️",
  o_scar: "🩹", o_remembered: "💐", o_horse: "🐴", o_plate: "🍽️", o_signpost: "🪧", o_dragon_hoard: "🐉", o_coffee: "☕",
};
