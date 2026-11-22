// Вид интерфейса «Сцена и полка» (ui_design.md §0): жирный контур, плотный цвет, у каждой вещи есть толщина.
// Вещи нарисованы картинками из web/assets/ui (запросы — ui_design.md §8). Если картинки нет, вещь рисует код, как в наброске.
import Phaser from "phaser";
import "@fontsource/balsamiq-sans/latin-700.css";
import "@fontsource/balsamiq-sans/cyrillic-700.css";
import "@fontsource/alice/latin-400.css";
import "@fontsource/alice/cyrillic-400.css";
import "@fontsource/ruslan-display/latin-400.css";
import "@fontsource/ruslan-display/cyrillic-400.css";
import "@fontsource/pt-mono/latin-400.css";
import "@fontsource/pt-mono/cyrillic-400.css";

export const C = {
  ink: 0x2a1a10, white: 0xffffff, cream: 0xffe9b8,
  paper: 0xf9ebc8, paperLip: 0xecd6a2, pip: 0xcdb37c, note: 0xfff6a8,
  wood: 0xc07e44, woodLip: 0x8c5127, woodLight: 0xd99a5c, dwood: 0x5e3719, dwoodLip: 0x452610,
  red: 0xc9462f, redDark: 0x8f2a1b, green: 0x46a052, greenDark: 0x2f6b3a, blue: 0x2f6fa6, brown: 0x6a4a2c, gold: 0xffd35a, plum: 0x3b2433,
  picNormal: 0xffd98a, picSpecial: 0xbfe0f5, picHelper: 0xcfe8b8,
  sysBg: 0x0f2236, sysBody: 0x24384a, sysLine: 0x3fd6c8, sysLineDark: 0x2aa99d, sysText: 0xdff7f4,
};
export const hex = (n: number) => "#" + n.toString(16).padStart(6, "0");

// Шрифты: жирный рисованный — всё, что нажимается и считается; книжный — текст рассказа;
// вязь — штампы; ровный «казённый» — система.
export const F = {
  head: '"Balsamiq Sans", "Trebuchet MS", sans-serif',
  body: "Alice, Georgia, serif",
  stamp: '"Ruslan Display", Georgia, serif',
  mono: '"PT Mono", Menlo, monospace',
};
export function loadFonts(): Promise<unknown> {
  const sample = "Сэр Баг 123";
  const list = ['bold 32px "Balsamiq Sans"', '32px "Alice"', '32px "Ruslan Display"', '32px "PT Mono"'];
  return Promise.all(list.map((f) => document.fonts.load(f, sample))).catch(() => null);
}

type TxtOpt = { font?: keyof typeof F; wrap?: number; align?: string; gap?: number; style?: string };
export function txt(scene: Phaser.Scene, x: number, y: number, s: string, size: number, color = C.ink, o: TxtOpt = {}) {
  const font = o.font ?? "head";
  return scene.add.text(x, y, s, {
    fontFamily: F[font], fontSize: size + "px", color: hex(color), fontStyle: o.style ?? (font === "head" ? "bold" : "normal"), align: o.align ?? "left",
    wordWrap: o.wrap ? { width: o.wrap, useAdvancedWrap: true } : undefined, lineSpacing: o.gap ?? 4,
  });
}

type SlabOpt = { fill?: number; lip?: number; line?: number; lw?: number; r?: number; lipH?: number; shadow?: number };
/** Толстая вещь: жёсткая тень, заливка, тёмный нижний борт, жирный контур. Центр в (0, 0). */
export function slab(scene: Phaser.Scene, w: number, h: number, o: SlabOpt = {}) {
  const g = scene.add.graphics(), x = -w / 2, y = -h / 2;
  const r = Math.min(o.r ?? 20, w / 2, h / 2), lipH = o.lipH ?? 12, sh = o.shadow ?? 12;
  if (sh) g.fillStyle(0x000000, 0.45).fillRoundedRect(x, y + sh, w, h, r);
  g.fillStyle(o.lip ?? C.paperLip, 1).fillRoundedRect(x, y, w, h, r);
  g.fillStyle(o.fill ?? C.paper, 1).fillRoundedRect(x, y, w, h - lipH, Math.min(r, (h - lipH) / 2));
  g.lineStyle(o.lw ?? 8, o.line ?? C.ink, 1).strokeRoundedRect(x, y, w, h, r);
  return g;
}

// ------------------------------------------------------------ рисованные вещи
type UiMeta = { size: [number, number]; slice?: [number, number, number, number]; window?: [number, number, number, number]; line?: number; body_top?: number; keep_w?: boolean; paper_top?: number; content_top?: number; inner?: [number, number, number, number]; caption?: [number, number, number, number]; add?: boolean; fit_h?: boolean; tile_x?: boolean; scale?: number };
const uiJson = import.meta.glob("../assets/ui/ui.json", { eager: true, import: "default" }) as Record<string, any>;
/** Рисованные вещи: размер картинки, края, которые не растягиваются, толщина контура, окно карточки. */
export const UI: Record<string, UiMeta> = (Object.values(uiJson)[0] as any) || {};
/** Есть ли рисованная вещь с таким именем. */
export const hasArt = (scene: Phaser.Scene, key: string) => !!UI[key] && scene.textures.exists(key);
/** Толщина контура на экране, к которой приводятся рисованные вещи. */
const LINE = 7;

/** Рисованная вещь размером w×h с жёсткой тенью снизу. Центр в (0, 0). У вещи с краями растягивается только середина. */
/** Во сколько раз рисованная вещь key уменьшается на экране, если её растянуть до w×h. */
export function artScale(key: string, w: number, h: number) {
  const m = UI[key];
  if (!m.slice) return Math.min(w / m.size[0], h / m.size[1]);
  const [l, r, t, b] = m.slice;
  // scale: свой масштаб на экране (тонкая рама), но края всё равно не должны налезать друг на друга
  if (m.scale) return Math.min(m.scale, w / ((l + r) * 1.05), h / ((t + b) * 1.05));
  // keep_w: посередине вещи что-то нарисовано (ремешки), по ширине её можно только уменьшить целиком
  if (m.keep_w) return Math.min(w / m.size[0], h / ((t + b) * 1.05));
  // fit_h: вещь всегда во всю свою высоту (окно широкой карточки остаётся квадратным), растягивается только по ширине
  if (m.fit_h) return Math.min(h / m.size[1], w / ((l + r) * 1.05));
  // контур примерно в LINE точек, но края не должны налезать друг на друга
  return Math.min(m.line ? LINE / m.line : 0.6, w / ((l + r) * 1.05), h / ((t + b) * 1.05));
}

export function artBox(scene: Phaser.Scene, key: string, w: number, h: number, shadow = 12): Phaser.GameObjects.Container {
  const m = UI[key];
  const make = (tex: string): any => {
    if (!m.slice) return scene.add.image(0, 0, tex).setDisplaySize(w, h);
    const [l, r, t, b] = m.slice;
    const k = artScale(key, w, h);
    return scene.add.nineslice(0, 0, tex, undefined, w / k, h / k, l, r, t, b, !!m.tile_x).setScale(k);
  };
  const parts: Phaser.GameObjects.GameObject[] = [];
  // чертёж: чёрное пропадает при сложении цветов, тени у него нет
  if (m.add) return scene.add.container(0, 0, [make(key).setBlendMode(Phaser.BlendModes.ADD)]);
  if (shadow && scene.textures.exists(key + "_sh")) parts.push(make(key + "_sh").setAlpha(0.45).setPosition(0, shadow));
  parts.push(make(key));
  return scene.add.container(0, 0, parts);
}

/** Подложка размером w×h: рисованная вещь key, а если её нет — толстая вещь, нарисованная кодом. Центр в (0, 0). */
export function panel(scene: Phaser.Scene, key: string, w: number, h: number, o: SlabOpt = {}): Phaser.GameObjects.Container {
  if (hasArt(scene, key)) return artBox(scene, key, w, h, o.shadow ?? 12);
  return scene.add.container(0, 0, [slab(scene, w, h, o)]);
}

/** Холодный прибор с тёмным экраном: так говорит «система» — Бог-Разработчик, гоблин с кредитом, Небесная HR. */
export function sysPanel(scene: Phaser.Scene, w: number, h: number): Phaser.GameObjects.Container {
  if (hasArt(scene, "b_panel")) {
    // лист-чертёж: тёмная подложка и поверх светящиеся линии
    const g = scene.add.graphics();
    g.fillStyle(0x000000, 0.35).fillRoundedRect(-w / 2, -h / 2 + 12, w, h, 18);
    g.fillStyle(C.sysBg, 0.9).fillRoundedRect(-w / 2 + 8, -h / 2 + 8, w - 16, h - 16, 16);
    const lines = artBox(scene, "b_panel", w + 40, h + 40, 0);
    return scene.add.container(0, 0, [g, lines]);
  }
  if (hasArt(scene, "ui_system")) return artBox(scene, "ui_system", w, h, 14);
  const g = scene.add.graphics(), x = -w / 2, y = -h / 2;
  g.fillStyle(0x000000, 0.45).fillRoundedRect(x, y + 14, w, h, 20);
  g.fillStyle(C.sysLine, 0.16).fillRoundedRect(x - 16, y - 16, w + 32, h + 32, 32);
  g.fillStyle(C.sysBody, 1).fillRoundedRect(x, y, w, h, 20);
  g.fillStyle(C.sysBg, 1).fillRoundedRect(x + 14, y + 14, w - 28, h - 28, 10);
  g.lineStyle(4, C.sysLine, 1).strokeRoundedRect(x + 14, y + 14, w - 28, h - 28, 10);
  g.lineStyle(8, C.ink, 1).strokeRoundedRect(x, y, w, h, 20);
  return scene.add.container(0, 0, [g]);
}

/** Дощечка с надписью: имя говорящего. Размер — в width и height. */
export function plate(scene: Phaser.Scene, label: string, size = 25, o: { fill?: number; lip?: number; color?: number } = {}) {
  const t = txt(scene, 0, -4, label, size, o.color ?? C.cream).setOrigin(0.5);
  const kit = o.fill === undefined && hasArt(scene, "k_namesign");
  // у резной дощечки по краям листья: тексту нужны поля пошире
  const h = size + (kit ? 40 : 30);
  // резные листья на концах дощечки не растягиваются: поля — ровно по ним
  const w = t.width + (kit ? 2 * UI.k_namesign.slice![0] * (h / ((UI.k_namesign.slice![2] + UI.k_namesign.slice![3]) * 1.05)) + 20 : 48);
  const back = kit ? artBox(scene, "k_namesign", w, h, 8) : o.fill === undefined && hasArt(scene, "ui_plate") ? artBox(scene, "ui_plate", w, h, 8)
    : slab(scene, w, h, { fill: o.fill ?? C.dwood, lip: o.lip ?? C.dwoodLip, lw: 7, r: 14, lipH: 8, shadow: 8 });
  const c = scene.add.container(0, 0, [back, t]);
  return c.setSize(w, h);
}

/** Красная лента с вырезами по краям: название сцены. */
export function ribbonTag(scene: Phaser.Scene, label: string, size = 23) {
  const t = txt(scene, 0, -2, label, size, C.white).setOrigin(0.5);
  const w = t.width + 80, h = size + 28, n = 18;
  if (hasArt(scene, "k_ribbon")) {
    // веточки на концах ленты не растягиваются: поля — ровно по ним
    const s = UI.k_ribbon.slice!, rh = size + 38, rw = t.width + 2 * s[0] * (rh / ((s[2] + s[3]) * 1.05)) + 20;
    return scene.add.container(0, 0, [artBox(scene, "k_ribbon", rw, rh, 8), t]).setSize(rw, rh);
  }
  if (hasArt(scene, "ui_ribbon")) return scene.add.container(0, 0, [artBox(scene, "ui_ribbon", w, h, 8), t]).setSize(w, h);
  const pts = [[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2 - n, 0], [w / 2, h / 2], [-w / 2, h / 2], [-w / 2 + n, 0]].map(([x, y]) => new Phaser.Math.Vector2(x, y));
  const g = scene.add.graphics();
  g.fillStyle(0x000000, 0.4).fillPoints(pts.map((p) => new Phaser.Math.Vector2(p.x, p.y + 8)), true);
  g.fillStyle(C.red, 1).fillPoints(pts, true);
  g.lineStyle(7, C.ink, 1).strokePoints(pts, true, true);
  return scene.add.container(0, 0, [g, t]).setSize(w, h);
}

/** Толстая кнопка: при наведении приподнимается, при нажатии вдавливается. */
export function plank(scene: Phaser.Scene, x: number, y: number, w: number, h: number, label: string, onClick: () => void, size = 30, o: { green?: boolean } = {}) {
  const c = scene.add.container(x, y);
  const t = txt(scene, 0, -6, label, size, C.white, { align: "center", gap: -2 }).setOrigin(0.5).setStroke(hex(C.ink), 7);
  const z = scene.add.zone(0, 0, w, h).setInteractive({ useHandCursor: true });
  z.on("pointerover", () => c.setY(y - 4));
  z.on("pointerout", () => c.setY(y));
  z.on("pointerdown", () => c.setY(y + 4));
  z.on("pointerup", () => { c.setY(y); onClick(); });
  const key = o.green ? (hasArt(scene, "k_btn_green") ? "k_btn_green" : "ui_btn_green") : hasArt(scene, "k_btn") ? "k_btn" : "ui_btn_wood";
  const back = hasArt(scene, key) ? artBox(scene, key, w, h, 10) : slab(scene, w, h, o.green ? { fill: C.green, lip: C.greenDark, shadow: 10 } : { fill: C.wood, lip: C.woodLip, shadow: 10 });
  c.add([back, t, z]);
  return c;
}

/** Жёлтая записка на кнопке: цель главы. */
export function note(scene: Phaser.Scene, head: string, text: string, wrap = 170) {
  const a = txt(scene, 0, 0, head, 16, C.redDark);
  const b = txt(scene, 0, 0, text, 21, C.ink, { wrap, gap: 1 });
  if (hasArt(scene, "ui_note")) {
    // на рисованной записке сверху булавка, снизу загнутый угол: тексту нужны поля пошире
    const w = Math.max(a.width, b.width) + 48, h = a.height + b.height + 74;
    a.setPosition(-w / 2 + 24, -h / 2 + 36);
    b.setPosition(-w / 2 + 24, -h / 2 + 38 + a.height);
    return scene.add.container(0, 0, [artBox(scene, "ui_note", w, h, 8), a, b]).setSize(w, h);
  }
  const w = Math.max(a.width, b.width) + 32, h = a.height + b.height + 36;
  a.setPosition(-w / 2 + 16, -h / 2 + 18);
  b.setPosition(-w / 2 + 16, -h / 2 + 20 + a.height);
  const g = scene.add.graphics();
  g.fillStyle(0x000000, 0.35).fillRect(-w / 2, -h / 2 + 8, w, h);
  g.fillStyle(C.note, 1).fillRect(-w / 2, -h / 2, w, h);
  g.lineStyle(5, C.ink, 1).strokeRect(-w / 2, -h / 2, w, h);
  g.fillStyle(C.red, 1).fillCircle(0, -h / 2 + 2, 11).lineStyle(5, C.ink, 1).strokeCircle(0, -h / 2 + 2, 11);
  return scene.add.container(0, 0, [g, a, b]).setSize(w, h);
}

/** Тёплое свечение вокруг выбранной карточки. */
export function glow(scene: Phaser.Scene, w: number, h: number, r = 24) {
  const g = scene.add.graphics();
  for (let i = 5; i >= 1; i--) g.fillStyle(0xffd66e, 0.14).fillRoundedRect(-w / 2 - i * 7, -h / 2 - i * 7, w + i * 14, h + i * 14, r + i * 7);
  return g;
}

/** Затемнение сверху и снизу, чтобы лист и карточки читались на ярком фоне. Картинка «shade». */
export function makeShade(scene: Phaser.Scene, h: number, tall = false) {
  if (scene.textures.exists("shade")) return;
  const t = scene.textures.createCanvas("shade", 8, h)!;
  const ctx = t.getContext();
  const gr = ctx.createLinearGradient(0, 0, 0, h);
  gr.addColorStop(0, "rgba(12,6,3,0.78)");
  const [a, b, c] = tall ? [760, 900, 1500] : [330, 520, 940]; // где кончается верхнее затемнение и где начинается нижнее
  gr.addColorStop(a / h, "rgba(12,6,3,0)");
  gr.addColorStop(b / h, "rgba(12,6,3,0)");
  gr.addColorStop(c / h, "rgba(12,6,3,0.9)");
  gr.addColorStop(1, "rgba(12,6,3,0.9)");
  ctx.fillStyle = gr;
  ctx.fillRect(0, 0, 8, h);
  t.refresh();
}

/** Штамп поперёк листа: приговор мамы. */
export function stamp(scene: Phaser.Scene, label: string, color: number) {
  const t = txt(scene, 0, 0, label.toUpperCase(), 50, color, { font: "stamp" }).setOrigin(0.5);
  const w = t.width + 56, h = 86;
  const key = color === C.greenDark ? "ui_stamp_great" : color === C.redDark ? "ui_stamp_shame" : "ui_stamp_ok";
  if (hasArt(scene, key)) {
    const c = scene.add.container(0, 0, [artBox(scene, key, w + 20, h + 16, 0), t]).setAngle(-4);
    c.setSize(w + 20, h + 16);
    return c;
  }
  const g = scene.add.graphics();
  g.fillStyle(color, 0.07).fillRoundedRect(-w / 2, -h / 2, w, h, 12);
  g.lineStyle(6, color, 0.95).strokeRoundedRect(-w / 2, -h / 2, w, h, 12);
  g.lineStyle(2, color, 0.8).strokeRoundedRect(-w / 2 + 9, -h / 2 + 9, w - 18, h - 18, 6);
  const c = scene.add.container(0, 0, [g, t]).setAngle(-4);
  c.setSize(w, h);
  return c;
}
