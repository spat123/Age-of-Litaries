// Главный экран, вид «Сцена и полка» (ui_design.md §0): фон места на весь экран, лист с текстом сверху,
// карточки выбора стоят на деревянной полке снизу, слева пропуск с показателями и цель главы,
// справа доска с особыми карточками и личное дело.
import Phaser from "phaser";
import { D, STAT, SPEAK, TAGS, StatKey } from "./data";
import { Life, IO, Ctx, LogLine, Tick, Save, Meta, run, checkSave } from "./rules";
import { BG_FALLBACK, PLACEHOLDER, loadTextures } from "./assets";
// где на каждом портрете голова: квадрат [x, y, сторона] в точках картинки (готовит web/tools/cut_faces.py)
// какие рисунки во всё окно вырезаны без фона и какой цвет фона с лучами под ними (готовит web/tools/prepare_card_full.py)
const CUT: Record<string, { cut: boolean; bg: string; bottom?: boolean; full?: boolean; bgimg?: string | null }> =
  (Object.values(import.meta.glob("../assets/cards_full/cards_full.json", { eager: true, import: "default" }))[0] as any) || {};
const FACES: Record<string, [number, number, number]> =
  (Object.values(import.meta.glob("../assets/faces/faces.json", { eager: true, import: "default" }))[0] as any) || {};
import { showPage, showFile, showChoice, showButtons, showSeen, showSettings, showPath, overlayOpen } from "./overlay";
import { play, trackFor, unlock } from "./audio";
import { C, hex, txt, slab, sysPanel, plate, ribbonTag, plank, note, glow, stamp, makeShade, loadFonts, panel, artBox, artScale, hasArt, UI } from "./ui";

// Экран бывает двух видов: широкий (компьютер, 1920×1080) и высокий (телефон в руке, 1080×1920).
export let W = 1920;
export let H = 1080;
export let TALL = false;
let SHEET_W = 1240; // лист с текстом
let SHEET_TOP = 56;
let SHELF_Y = 1006; // верх полки
const LEFT_X = 143; // середина пропуска
let RIGHT_X = W - 143; // середина доски
let CARDS_L = 264; // карточки выбора живут между пропуском и доской
let SHEET_L = -1; // левый край листа; -1 — лист по середине экрана
/** Экран по наброску «Сцена с героями» (П32): есть все рисованные вещи набора k_*. Решается при запуске. */
let KIT = false;
const KIT_PARTS = ["k_panel", "k_card", "k_stats", "k_board", "k_shelf"];
let CARDS_R = W - 264;
/** Выбрать вид экрана. Вызывается один раз, до запуска игры. */
export function setStage(tall: boolean) {
  TALL = tall;
  W = tall ? 1080 : 1920;
  H = tall ? 1920 : 1080;
  SHEET_W = tall ? 1024 : 1240;
  SHEET_TOP = tall ? 304 : 56;
  SHELF_Y = tall ? 1700 : 1006;
  RIGHT_X = W - 143;
  CARDS_R = W - 264;
}
/** Размер букв: на высоком экране всё крупнее, чтобы читалось на телефоне. */
const fs = (n: number) => Math.round(n * (TALL ? 1.45 : 1));
const HUD_ORDER: StatKey[] = ["body", "mind", "rep", "gold"];
// ободок значка показателя: у каждого свой цвет, по длине ободка видно, сколько из десяти
const RIM: Record<StatKey, number> = { body: 0xe8483f, mind: 0xf183c4, rep: 0xa5d04a, gold: 0xffc63a };
// ряд показателей — посередине вверху (решение автора); слева вверху — только для пробы, адрес с ?stats=left
const STATS_LEFT = typeof location !== "undefined" && new URLSearchParams(location.search).get("stats") === "left";
const SAVE_KEY = "sirbug.save.v1"; // сохранение лежит в памяти браузера
const META_KEY = "sirbug.meta.v1"; // что игрок видел за все жизни; «Начать заново» это не стирает
function readMeta(): Meta {
  const m: Meta = { lives: 0, endings: [], deaths: [], titles: [] };
  try { Object.assign(m, JSON.parse(localStorage.getItem(META_KEY) || "{}")); } catch {}
  return m;
}
const sign = (d: number) => (d > 0 ? "+" : "−") + Math.abs(d);
/** «Система» говорит холодным прибором с экраном, мир — бумажным листом. */
const isSystem = (scene: any) => ["god", "goblin", "angel"].includes(scene.speaker) || scene.id === "promotion";

type Box = Phaser.GameObjects.Container;

export class GameScene extends Phaser.Scene {
  bg!: Phaser.GameObjects.Image;
  bgKey = "";
  panel!: Box;
  faceBox!: Box;
  sysFrame: Phaser.GameObjects.Image | null = null;
  cards!: Box;
  cardFx!: Phaser.GameObjects.Container; // свет позади особых карточек: ниже всех карточек, чтобы не ложился на соседние
  hud!: Box;
  side!: Box;
  hand!: Box;
  front!: Box;
  tip!: Box;
  life: Life | null = null;
  shown: Record<StatKey, number> | null = null;
  chosen: Box | null = null;
  panelBottom = 260;
  keyHandler: ((n: number) => void) | null = null;
  nextHandler: (() => void) | null = null;

  constructor() {
    super("game");
  }

  create() {
    Promise.all([loadTextures(this), loadFonts()]).then(() => {
      this.build();
      window.addEventListener("pointerdown", unlock);
      window.addEventListener("keydown", unlock);
      const io: IO = {
        pick: (L, opts, ctx) => this.pick(L, opts, ctx),
        result: (L, ctx, text, log) => this.result(L, ctx, text, log),
        verdict: (L, ctx, ticks, name, key, text, log) => this.verdict(L, ctx, ticks, name, key, text, log),
        page: (L, title, html, label, system) => {
          if (L) this.drawHud(L, null);
          return showPage(title, html, label, system, title.startsWith("Итог жизни"));
        },
        chapter: (L, ch) => {
          if (ch.id === "ch0") return Promise.resolve(); // сборка мира идёт без ленты: игрок ещё ничего не знает
          this.life = L;
          this.panel.removeAll(true);
          if (ch.place_bg) this.setBg(ch.place_bg);
          play(trackFor(ch.id));
          this.drawHud(L, null);
          const lead = "<p><b>" + ch.age + ".</b>" + (ch.goal ? " Цель главы: " + ch.goal + "." : "") + "</p>";
          return showPath("Глава " + ch.id.slice(2) + ". " + ch.title, lead, L, readMeta().path || [], (bg, x) => this.thumb(bg, x));
        },
        save: (s) => {
          try { localStorage.setItem(SAVE_KEY, JSON.stringify(s)); } catch {}
        },
        ask: (title, html, labels) => showButtons(title, html, labels),
        finish: () => {
          const m = readMeta();
          m.finished = true;
          try { localStorage.setItem(META_KEY, JSON.stringify(m)); localStorage.removeItem(SAVE_KEY); } catch {}
          location.reload();
        },
        lifeEnd: (L, alive) => {
          const m = readMeta();
          const add = (a: string[], x: string | null) => { if (x && !a.includes(x)) a.push(x); };
          m.lives = Math.max(m.lives, L.n);
          if (alive) add(m.endings, L.ending);
          else add(m.deaths, L.dead![0]);
          for (const t of L.titles()) add(m.titles, t);
          // отметка для ленты пути: где и чем кончилась эта жизнь
          m.path = (m.path || []).filter((p) => p.n !== L.n).concat({ n: L.n, ch: L.chId, how: alive ? L.ending || "" : L.dead![0], alive }).slice(-40);
          try { localStorage.setItem(META_KEY, JSON.stringify(m)); } catch {}
          return m;
        },
      };
      this.start(io);
    });
  }

  /** Главное меню: продолжить, новая игра, что я уже видел, настройки. Потом запускает игру. */
  async start(io: IO) {
    this.setBg("bg_act1_birth");
    play("menu");
    await this.splash();
    for (;;) {
      let saved: Save | null = null;
      try { saved = checkSave(JSON.parse(localStorage.getItem(SAVE_KEY) || "null")); } catch {}
      const what = await this.menu(saved);
      if (what === "seen") {
        await showSeen(readMeta());
        continue;
      }
      if (what === "settings") {
        await showSettings();
        continue;
      }
      if (what === "new" && saved) {
        const sure = await showChoice("Новая игра", "<p>Сохранённая игра (жизнь " + saved.life.n + ") будет стёрта. То, что ты уже видел, останется.</p>", "Начать заново", "Отмена");
        if (!sure) continue;
      }
      if (what === "new") {
        saved = null;
        const m = readMeta();
        m.path = []; // новая игра: отметки прошлых жизней на ленте пути начинаются заново
        try { localStorage.removeItem(SAVE_KEY); localStorage.setItem(META_KEY, JSON.stringify(m)); } catch {}
      }
      run(io, saved);
      return;
    }
  }

  /** Название игры на затемнённом фоне: основа заставки и главного меню. */
  titleBox(): Box {
    const veil = this.add.rectangle(W / 2, H / 2, W, H, 0x140a05, 0.62).setInteractive(); // закрывает игру под меню
    const title = txt(this, W / 2, TALL ? 330 : 230, "Сэр Баг", TALL ? 190 : 150, C.cream).setOrigin(0.5).setStroke(hex(C.ink), 18);
    const sub = txt(this, W / 2, TALL ? 480 : 352, "Исходный Код Средневековья", TALL ? 58 : 46, C.white).setOrigin(0.5).setStroke(hex(C.ink), 9);
    return this.add.container(0, 0, [veil, title, sub]).setDepth(60);
  }

  /** Заставка: ждёт любого нажатия. После него браузер разрешает звук, и в меню уже играет музыка. */
  splash(): Promise<void> {
    return new Promise((res) => {
      const box = this.titleBox();
      const hint = txt(this, W / 2, TALL ? 980 : 640, TALL ? "Коснись экрана, чтобы начать" : "Нажми любую клавишу или щёлкни мышью", fs(34), C.cream).setOrigin(0.5).setStroke(hex(C.ink), 8);
      box.add(hint);
      this.tweens.add({ targets: hint, alpha: 0.35, duration: 800, yoyo: true, repeat: -1 });
      const done = () => {
        this.keyHandler = null;
        this.nextHandler = null;
        box.destroy();
        res();
      };
      (box.list[0] as Phaser.GameObjects.Rectangle).once("pointerup", done);
      this.nextHandler = done;
      this.keyHandler = () => done();
    });
  }

  /** Рисует главное меню и ждёт, что выберет игрок. */
  menu(saved: Save | null): Promise<"continue" | "new" | "seen" | "settings"> {
    return new Promise((res) => {
      const box = this.titleBox();
      const done = (what: "continue" | "new" | "seen" | "settings") => {
        this.keyHandler = null;
        this.nextHandler = null;
        box.destroy();
        res(what);
      };
      const items: [string, "continue" | "new" | "seen" | "settings"][] = [];
      if (saved) {
        const ch = saved.phase === "life" ? D.chapters[saved.pos!.ci] : null;
        items.push(["Продолжить: жизнь " + saved.life.n + (ch ? ", глава " + ch.id.slice(2) : ""), "continue"]);
      }
      items.push(["Новая игра", "new"], ["Что я уже видел", "seen"], ["Настройки", "settings"]);
      if (readMeta().finished) box.add(txt(this, W / 2, TALL ? 580 : 416, "Игра пройдена. Можно жить дальше.", fs(28), C.gold).setOrigin(0.5).setStroke(hex(C.ink), 7));
      items.forEach(([label, what], i) => box.add(plank(this, W / 2, (TALL ? 720 : 500) + i * (TALL ? 160 : 108), TALL ? 880 : 620, TALL ? 128 : 88, label, () => done(what), fs(32), { green: i === 0 })));
      this.keyHandler = (n) => items[n - 1] && done(items[n - 1][1]);
      this.nextHandler = () => done(items[0][1]);
    });
  }

  /** Меню во время игры: настройки и выход в главное меню. Игра сохраняется сама. */
  async gameMenu() {
    for (;;) {
      const i = await showButtons("Меню", "<p>Игра сохраняется сама перед каждой сценой.</p>", ["Вернуться в игру", "Путь", "Настройки", "В главное меню"]);
      if (i === 1) {
        const L = this.life;
        await showPath("Путь", L ? "<p>Жизнь " + L.n + ".</p>" : "", L, readMeta().path || [], (bg, x) => this.thumb(bg, x), "Назад");
        continue;
      }
      if (i === 2) {
        await showSettings();
        continue;
      }
      if (i === 3) location.reload();
      return;
    }
  }

  /** Маленькая квадратная картинка из фона для остановки на ленте пути. x — какое место фона по ширине взять (0–1). */
  thumbs: Record<string, string> = {};
  thumb(key: string, x = 0.5): string {
    const id = key + ":" + x;
    if (this.thumbs[id]) return this.thumbs[id];
    if (!this.textures.exists(key)) return "";
    try {
      const img = this.textures.get(key).getSourceImage() as HTMLImageElement;
      const s = Math.min(img.width, img.height);
      const left = Math.max(0, Math.min(img.width - s, img.width * x - s / 2));
      const c = document.createElement("canvas");
      c.width = c.height = 180;
      c.getContext("2d")!.drawImage(img, left, (img.height - s) / 2, s, s, 0, 0, 180, 180);
      return (this.thumbs[id] = c.toDataURL("image/jpeg", 0.85));
    } catch {
      return "";
    }
  }

  build() {
    KIT = KIT_PARTS.every((k) => hasArt(this, k)) && (!TALL || hasArt(this, "k_row"));
    if (KIT && TALL) {
      // телефон: сверху вывеска и портрет, ниже лист во всю ширину, выборы строками
      SHEET_W = 1024;
      SHEET_L = 28;
      SHEET_TOP = 430;
    } else if (KIT) {
      // лист правее середины: слева встаёт портрет говорящего; сверху слева вывеска, справа доска
      // окно диалога выше и чуть уже (автор: «диалог сделай выше, именно само облачко, и чуть меньше»)
      SHEET_W = 940;
      SHEET_L = 500;
      SHEET_TOP = 112;
      CARDS_L = 470;
      CARDS_R = 1490;
    }
    this.bg = this.add.image(W / 2, H / 2, "bg_act0_void").setDepth(0);
    this.bg.setScale(Math.max(W / this.bg.width, H / this.bg.height));
    makeShade(this, H, TALL);
    this.add.image(W / 2, H / 2, "shade").setDisplaySize(W, H).setDepth(1);
    // полка, на которой стоят карточки
    const s = this.add.graphics().setDepth(5);
    if (KIT && TALL) {
      // телефон: резная доска полки во всю ширину, под ней тёмное дерево до низа экрана
      const m = UI.k_shelf, sh = ((W + 40) * m.size[1]) / m.size[0];
      s.fillStyle(C.dwoodLip, 1).fillRect(-10, SHELF_Y + sh / 2, W + 20, H - SHELF_Y);
      this.add.image(W / 2, SHELF_Y - 10 + sh / 2, "k_shelf").setDisplaySize(W + 40, sh).setDepth(5);
    } else if (KIT) {
      // полки нет: карточки стоят прямо в сцене (автор: «уберём подставку под карточками»)
    } else if (hasArt(this, "ui_shelf")) {
      // рисованная доска полки, под ней тёмное дерево до низа экрана
      const plankH = TALL ? 110 : 92;
      s.fillStyle(C.dwoodLip, 1).fillRect(-10, SHELF_Y + plankH - 10, W + 20, H - SHELF_Y);
      this.add.image(W / 2, SHELF_Y - 6 + plankH / 2, "ui_shelf").setDisplaySize(W + 40, plankH).setDepth(5);
    } else {
      s.fillStyle(C.wood, 1).fillRect(-10, SHELF_Y, W + 20, H - SHELF_Y + 10);
      s.fillStyle(C.woodLight, 1).fillRect(-10, SHELF_Y, W + 20, 12);
      s.fillStyle(C.woodLip, 1).fillRect(-10, SHELF_Y + 46, W + 20, 40);
      s.lineStyle(8, C.ink, 1).lineBetween(-10, SHELF_Y, W + 10, SHELF_Y);
    }
    this.faceBox = this.add.container(0, 0).setDepth(8);
    // когда говорит «система» или мир глючит, по краю экрана проступает бирюзовый чертёж
    if (hasArt(this, "b_frame")) this.sysFrame = this.add.image(W / 2, H / 2, "b_frame").setDisplaySize(W, H).setBlendMode(Phaser.BlendModes.ADD).setDepth(7).setAlpha(0);
    this.panel = this.add.container(0, 0).setDepth(10);
    this.cardFx = this.add.container(0, 0).setDepth(19);
    this.cards = this.add.container(0, 0).setDepth(20);
    this.hud = this.add.container(0, 0).setDepth(30);
    this.side = this.add.container(0, 0).setDepth(30);
    this.hand = this.add.container(0, 0).setDepth(30);
    this.front = this.add.container(0, 0).setDepth(40);
    this.tip = this.add.container(0, 0).setDepth(50);
    this.input.keyboard?.on("keydown", (e: KeyboardEvent) => {
      if (overlayOpen()) return; // поверх игры открыта страница: клавиши не для карточек
      if ((e.code === "Space" || e.code === "Enter") && this.nextHandler) this.nextHandler();
      const n = parseInt(e.key, 10);
      if (n >= 1 && n <= 9 && this.keyHandler) this.keyHandler(n);
    });
  }

  setBg(key: string) {
    let k = this.textures.exists(key) ? key : BG_FALLBACK[key];
    if (!k || !this.textures.exists(k)) k = "bg_act1_first_word";
    if (TALL && this.textures.exists(k + "_tall")) k += "_tall"; // у телефона свой, высокий рисунок, если он есть
    if (k === this.bgKey) return;
    this.bgKey = k;
    this.bg.setTexture(k);
    this.bg.setScale(Math.max(W / this.bg.width, H / this.bg.height));
    this.bg.setAlpha(0.35);
    this.tweens.add({ targets: this.bg, alpha: 1, duration: 350 });
  }

  /** Картинка карточки или временный значок. */
  art(key: string, x: number, y: number, maxW: number, maxH: number): Phaser.GameObjects.GameObject {
    if (this.textures.exists(key)) {
      const im = this.add.image(x, y, key);
      return im.setScale(Math.min(maxW / im.width, maxH / im.height));
    }
    const size = Math.max(26, Math.min(maxH * 0.62, maxW * 0.6, 110));
    return this.add.text(x, y, PLACEHOLDER[key] || "🃏", { fontFamily: "sans-serif", fontSize: size + "px" }).setOrigin(0.5);
  }
  /** Значок показателя. */
  statIcon(k: StatKey, x: number, y: number, size: number) {
    return this.textures.exists("icon_" + k) ? this.add.image(x, y, "icon_" + k).setDisplaySize(size, size) : txt(this, x, y, STAT[k][0], size * 0.7).setOrigin(0.5);
  }
  /** Показатели в ряд: значок в тёмном кружке, цветной ободок — сколько из десяти, рядом число. */
  statRow(L: Life, x: number, y: number, center: boolean, R: number, animate: boolean) {
    // тёмный кружок ровно по внешнему краю кольца, чтобы снаружи кольца ничего не выступало
    const th = Math.max(5, Math.round(R * 0.2)), disc = R + th / 2, gap = Math.round(R * 0.75);
    const items = HUD_ORDER.map((key) => {
      const v = L.stats[key], bar = key !== "gold", low = bar && v <= 2;
      const col = low ? C.red : RIM[key];
      const c = this.add.container(0, 0);
      const g = this.add.graphics();
      // полупрозрачного сияния вокруг кружка больше нет (автор: «убери вторую рамку прозрачную у иконок»)
      g.fillStyle(0x2a1a10, 0.88).fillCircle(0, 0, disc);
      g.lineStyle(th, col, 0.28).strokeCircle(0, 0, R); // незаполненная часть кольца — бледная, в цвет значка
      const part = bar ? Math.max(0, Math.min(1, v / 10)) : 1;
      if (part > 0) {
        g.lineStyle(th, col, 1).beginPath();
        g.arc(0, 0, R, -Math.PI / 2, -Math.PI / 2 + part * Math.PI * 2, false);
        g.strokePath();
      }
      const color = key === "gold" ? C.gold : low ? 0xffb9a8 : C.white;
      const num = txt(this, disc + 8, 0, String(v), Math.round(R * 1.25), color).setOrigin(0, 0.5)
        .setStroke(hex(C.ink), Math.max(6, Math.round(R * 0.26)));
      c.add([g, this.statIcon(key, 0, 0, R * 1.42), num]);
      return { key, v, c, w: disc * 2 + 8 + num.width };
    });
    const total = items.reduce((a, it) => a + it.w, 0) + gap * (items.length - 1);
    const left = center ? x - total / 2 : x;
    let cx = left;
    for (const it of items) {
      const px = cx + disc;
      it.c.setPosition(px, y);
      this.hud.add(it.c);
      cx += it.w + gap;
      const d = this.shown ? it.v - this.shown[it.key] : 0;
      if (animate && d) {
        const pop = txt(this, px, y + disc + 4, sign(d), Math.round(R * 1.3), d > 0 ? 0x8be06a : 0xff8a70).setOrigin(0.5, 0).setStroke(hex(C.ink), 9);
        this.hud.add(pop);
        this.tweens.add({ targets: pop, y: pop.y + 50, alpha: 0, duration: 1600, ease: "Sine.Out", onComplete: () => pop.destroy() });
        this.tweens.add({ targets: it.c, scale: 1.15, duration: 110, yoyo: true });
      }
    }
    this.shown = { ...L.stats };
    return { left, right: left + total, bottom: y + disc + 7 };
  }
  /** Свет позади особой карточки: тёплое сияние, медленно крутятся лучи, вспыхивают искры.
   *  Временный: настоящие эффекты сделаем потом кодом или готовым VFX (решение П34, список мест — Р36 в decisions.md). */
  specialFx(w: number, h: number) {
    const fx = this.add.container(0, 0);
    const halo = this.add.graphics();
    for (let i = 6; i >= 1; i--) halo.fillStyle(0xffc94a, 0.1).fillRoundedRect(-w / 2 - i * 9, -h / 2 - i * 9, w + i * 18, h + i * 18, 26 + i * 9);
    const rays = this.add.graphics().setPosition(0, -h * 0.12).setBlendMode(Phaser.BlendModes.ADD);
    const R = Math.max(w, h) * 0.9, n = 18;
    for (let i = 0; i < n; i++) {
      const a = (i / n) * Math.PI * 2, da = Math.PI / n * 0.55;
      rays.fillStyle(0xffe08a, i % 2 ? 0.16 : 0.3);
      rays.fillTriangle(0, 0, Math.cos(a - da) * R, Math.sin(a - da) * R, Math.cos(a + da) * R, Math.sin(a + da) * R);
    }
    fx.add([rays, halo]);
    const tw: Phaser.Tweens.Tween[] = [];
    tw.push(this.tweens.add({ targets: rays, angle: 360, duration: 26000, repeat: -1 }));
    tw.push(this.tweens.add({ targets: halo, alpha: 0.55, duration: 900, yoyo: true, repeat: -1, ease: "Sine.InOut" }));
    for (let i = 0; i < 8; i++) {
      // искры по краю рамки
      const side = i % 4, t = Math.random();
      const x = side === 0 ? -w / 2 + t * w : side === 1 ? w / 2 + 6 : side === 2 ? -w / 2 + t * w : -w / 2 - 6;
      const y = side === 0 ? -h / 2 - 6 : side === 1 ? -h / 2 + t * h : side === 2 ? h / 2 + 6 : -h / 2 + t * h;
      const s = this.add.graphics().setPosition(x, y).setBlendMode(Phaser.BlendModes.ADD).setScale(0);
      const r = 9 + Math.random() * 7;
      const q = r * 0.28; // четырёхлучевая звёздочка из четырёх треугольников
      s.fillStyle(0xfff3c4, 1).fillTriangle(0, -r, q, 0, -q, 0).fillTriangle(0, r, q, 0, -q, 0)
        .fillTriangle(-r, 0, 0, -q, 0, q).fillTriangle(r, 0, 0, -q, 0, q);
      fx.add(s);
      tw.push(this.tweens.add({ targets: s, scale: 1, angle: 90, duration: 520, yoyo: true, repeat: -1, repeatDelay: 600 + Math.random() * 1400,
        delay: Math.random() * 1800, ease: "Sine.Out" }));
    }
    fx.once("destroy", () => tw.forEach((t) => t.remove()));
    return fx;
  }
  /** Ячейка уникальной карточки: закруглённая рамка (k_slot2), под её окном цвет вида карточки и рисунок. */
  handChip(L: Life, id: string | null, x: number, y: number, tile: number, onShow: (title: string, text: string) => void, onHide: () => void) {
    const chip = this.add.container(x, y);
    // ячейка автора (k_slot3, без заклёпок, под цвет карточек), иначе закруглённая по Hades (k_slot2)
    const sk = hasArt(this, "k_slot3") ? "k_slot3" : "k_slot2", fresh = hasArt(this, sk);
    const cd = id ? D.cards[id] : null;
    if (fresh) {
      const m = UI[sk], [sw, sh] = m.size, [wx, wy, ww, wh] = m.window!;
      const wl = -tile / 2 + (wx / sw) * tile, wt = -tile / 2 + (wy / sh) * tile, wW = (ww / sw) * tile, wH = (wh / sh) * tile;
      const g = this.add.graphics();
      g.fillStyle(cd ? (cd.universal ? C.picHelper : cd.term === "sub" ? C.picSpecial : C.picNormal) : 0x3a2616, 1)
        .fillRoundedRect(wl - 4, wt - 4, wW + 8, wH + 8, tile * 0.16);
      chip.add(g);
      if (cd) chip.add(this.art(cd.art, wl + wW / 2, wt + wH / 2, wW - 8, wH - 8));
      chip.add(this.add.image(0, 0, sk).setDisplaySize(tile, tile));
    } else {
      if (hasArt(this, "k_slot")) chip.add(this.add.image(0, 0, "k_slot").setDisplaySize(tile + 10, tile + 10));
      if (cd) {
        const g = this.add.graphics();
        g.fillStyle(cd.universal ? C.picHelper : cd.term === "sub" ? C.picSpecial : C.picNormal, 1).fillRoundedRect(-tile / 2 + 8, -tile / 2 + 8, tile - 16, tile - 16, 10);
        chip.add([g, this.art(cd.art, 0, 0, tile - 26, tile - 26)]);
      }
    }
    if (!id || !cd) return chip.setAlpha(0.55); // пустая ячейка — бледная
    let state = "";
    if (id in L.subs) {
      const free = L.subFree(id);
      state = free > 0 ? "Бесплатно ещё сцен: " + free + "." : "Сейчас берёт плату.";
      chip.add(this.dot(tile / 2 - 8, -tile / 2 + 8, tile > 110 ? 22 : 17, C.red, free > 0 ? String(free) : "!", tile > 110 ? 23 : 18));
    }
    const z = this.add.zone(0, 0, tile, tile).setInteractive({ useHandCursor: true });
    const show = () => {
      chip.setScale(1.08);
      onShow(cd.name, cd.text + (state ? " " + state : ""));
    };
    z.on("pointerover", show);
    z.on("pointerdown", show);
    z.on("pointerout", () => {
      chip.setScale(1);
      onHide();
    });
    chip.add(z);
    return chip;
  }
  /** Голова говорящего, вырезанная по кругу (для круглой рамки аватара). Делается один раз на портрет. */
  roundFace(face: string, box: [number, number, number]) {
    const key = face + "_round";
    if (this.textures.exists(key)) return key;
    // берём кусок портрета на треть больше головы — персонаж в кольце мельче, видны плечи (автор: «персонаж внутри
    // можно чуть уменьшить»); прибавку отдаём в основном вниз, чтобы макушку не срезало
    const S = 256, [bx, by, bs] = box, fs0 = Math.round(bs * 1.3);
    const fx = Math.round(bx - (fs0 - bs) / 2), fy = Math.round(by - (fs0 - bs) * 0.15);
    const t = this.textures.createCanvas(key, S, S)!;
    const c = t.getContext();
    c.save();
    c.beginPath();
    c.arc(S / 2, S / 2, S / 2, 0, Math.PI * 2);
    c.clip();
    c.drawImage(this.textures.get(face).getSourceImage() as CanvasImageSource, fx, fy, fs0, fs0, 0, 0, S, S);
    c.restore();
    t.refresh();
    return key;
  }
  /** Метка особого выбора: серебряная звезда (значок автора) в тёмном кружке; у помощника — зелёный кружок с конём. */
  specialMark(x: number, y: number, r: number, helper: boolean): Phaser.GameObjects.GameObject[] {
    if (helper || !this.textures.exists("icon_star")) return this.dot(x, y, r, helper ? C.green : C.blue, helper ? "♞" : "★", r + 1);
    const g = this.add.graphics();
    g.fillStyle(0x1d2a4a, 1).fillCircle(x, y, r + 2).lineStyle(5, C.ink, 1).strokeCircle(x, y, r + 2);
    return [g, this.add.image(x, y, "icon_star").setDisplaySize(r * 1.9, r * 1.9)];
  }
  /** Картинка, заполняющая прямоугольник целиком (лишнее по краям обрезается). x, y — левый верхний угол. */
  fullArt(key: string, x: number, y: number, w: number, h: number, plain = false): Phaser.GameObjects.GameObject {
    // plain — просто заполнить окно картинкой, без фона под ней
    const cut = !plain && key.startsWith("full_") ? CUT[key.slice(5)] : undefined;
    if (cut && cut.cut) {
      // рисунок без фона: под ним цветной фон с лучами, сам рисунок вписан целиком
      // фон: нарисованный с лучами ближайшего цвета, если он есть; иначе лучи рисует код
      const bk = cut.bgimg && this.textures.exists("cbg_" + cut.bgimg) ? "cbg_" + cut.bgimg : this.raysTexture(cut.bg);
      const bg = this.fullArt(bk, x, y, w, h);
      // рисунок упирается в край: заполняет окно целиком, край уходит под рамку
      if (cut.full) return this.add.container(0, 0, [bg, this.fullArt(key, x, y, w, h, true)]);
      const fig = this.add.image(x + w / 2, y + h / 2, key);
      if (cut.bottom) {
        // обрезан снизу (по пояс): стоит на нижнем краю окна во всю высоту
        fig.setOrigin(0.5, 1).setPosition(x + w / 2, y + h).setScale(Math.min(w / fig.width, (h * 0.96) / fig.height));
      } else fig.setScale(Math.min((w * 0.9) / fig.width, (h * 0.9) / fig.height));
      return this.add.container(0, 0, [bg, fig]);
    }
    const img = this.add.image(0, 0, key).setOrigin(0, 0);
    const iw = img.width, ih = img.height, s = Math.max(w / iw, h / ih), cw = w / s, chh = h / s, cx = (iw - cw) / 2, cy = (ih - chh) / 2;
    return img.setScale(s).setCrop(cx, cy, cw, chh).setPosition(x - cx * s, y - cy * s);
  }
  /** Квадрат цвета col с расходящимися лучами — фон под вырезанным рисунком карточки. */
  raysTexture(col: string) {
    const key = "rays_" + col.slice(1);
    if (this.textures.exists(key)) return key;
    const S = 512, t = this.textures.createCanvas(key, S, S)!, c = t.getContext();
    c.fillStyle = col;
    c.fillRect(0, 0, S, S);
    const cx = S / 2, cy = S * 0.56, n = 16, R = S;
    c.fillStyle = "rgba(255,255,255,0.22)";
    for (let i = 0; i < n; i++) {
      const a = (i / n) * Math.PI * 2, da = (Math.PI / n) * 0.5;
      c.beginPath();
      c.moveTo(cx, cy);
      c.lineTo(cx + Math.cos(a - da) * R, cy + Math.sin(a - da) * R);
      c.lineTo(cx + Math.cos(a + da) * R, cy + Math.sin(a + da) * R);
      c.closePath();
      c.fill();
    }
    t.refresh();
    return key;
  }
  /** Кружок с числом или знаком: клавиша карточки, счётчики. */
  dot(x: number, y: number, r: number, fill: number, label: string, size: number) {
    const g = this.add.graphics();
    g.fillStyle(fill, 1).fillCircle(x, y, r).lineStyle(r > 22 ? 7 : 5, C.ink, 1).strokeCircle(x, y, r);
    return [g, txt(this, x, y - 2, label, size, C.white).setOrigin(0.5).setStroke(hex(C.ink), 6)];
  }

  // ------------------------------------------------------------ лист с текстом сцены
  drawPanel(ctx: Ctx): number {
    this.panel.removeAll(true);
    const sys = isSystem(ctx.scene);
    const ink = sys ? C.sysText : C.ink, font = sys ? "mono" : "body";
    const x0 = SHEET_L >= 0 ? SHEET_L : (W - SHEET_W) / 2;
    const kitPanel = KIT && !sys;
    let padX = sys ? 54 : 44, padT = sys ? 48 : 38, padB = sys ? 32 : 26, minH = 0;
    const pk = hasArt(this, "k_panel2") ? "k_panel2" : "k_panel"; // тонкая рама, если она есть
    if (kitPanel) {
      // поля — по пергаменту внутри резной рамы
      const m = UI[pk], k = artScale(pk, SHEET_W, 300), [ix, iy, , ih] = m.inner!;
      padX = ix * k + 24;
      padT = iy * k + 14;
      padB = (m.size[1] - iy - ih) * k + 12;
      minH = (m.slice![2] + m.slice![3]) * k * 1.08;
    }
    const inner = SHEET_W - padX * 2;
    const items: Phaser.GameObjects.GameObject[] = [];
    let y = SHEET_TOP + padT;
    for (const l of ctx.enter || []) {
      if (!l.stat) continue;
      const t = txt(this, x0 + padX, y, "В начале сцены: " + STAT[l.stat] + " " + sign(l.d!), fs(22), sys ? C.sysLine : l.d! > 0 ? C.greenDark : C.redDark);
      items.push(t);
      y += t.height + 6;
    }
    const long = ctx.text.length > 330;
    const size = fs(sys ? (long ? 21 : 23) : long ? 24 : 27);
    const main = txt(this, x0 + padX, y, ctx.text, size, ink, { font, wrap: inner, gap: 8 });
    items.push(main);
    y += main.height + 8;
    for (const a of ctx.adds || []) {
      const t = txt(this, x0 + padX + 20, y + 4, a, fs(sys ? 21 : 24), sys ? C.sysLine : C.blue, { font, wrap: inner - 20, gap: 6 });
      items.push(t, this.add.rectangle(x0 + padX + 4, y + 4 + t.height / 2, 6, t.height, sys ? C.sysLine : C.blue));
      y += t.height + 12;
    }
    if (ctx.then) {
      const t = txt(this, x0 + padX, y + 4, ctx.then, fs(sys ? 21 : 25), sys ? C.sysLine : C.brown, { font, wrap: inner, gap: 6 });
      items.push(t);
      y += t.height + 10;
    }
    const h = Math.max(y + padB - SHEET_TOP, minH);
    const bottom = SHEET_TOP + h;
    const back = (kitPanel ? artBox(this, pk, SHEET_W, h, 14) : sys ? sysPanel(this, SHEET_W, h) : panel(this, "ui_sheet", SHEET_W, h, { r: 22, shadow: 14 }))
      .setPosition(x0 + SHEET_W / 2, SHEET_TOP + h / 2);
    if (this.sysFrame) {
      const on = sys || ctx.scene.id === "glitch";
      this.tweens.killTweensOf(this.sysFrame);
      this.tweens.add({ targets: this.sysFrame, alpha: on ? 0.9 : 0, duration: on ? 500 : 250 });
    }
    // говорящий — аватаром в резной рамке рядом с окном диалога; у рассказчика аватара нет
    this.faceBox.removeAll(true);
    const who0 = ctx.scene.face || ctx.scene.speaker, face = "face_" + who0;
    const round = hasArt(this, "k_avatar_round"); // круглая рамка, как портрет в кольце в Hades II
    if (KIT && this.textures.exists(face) && (round || hasArt(this, "k_avatar")) && FACES[who0]) {
      const fk = round ? "k_avatar_round" : "k_avatar";
      const A = round ? (TALL ? 214 : 196) : TALL ? 200 : 176;
      const ax = TALL ? W - 28 - A / 2 : x0 - 14 - A / 2, ay = TALL ? SHEET_TOP - 24 - A / 2 : SHEET_TOP + A / 2 - 6;
      const m = UI[fk], [sw, shh] = m.size, [wx, wy, ww, wh] = m.window!;
      const wl = ax - A / 2 + (wx / sw) * A, wt = ay - A / 2 + (wy / shh) * A, wW = (ww / sw) * A, wH = (wh / shh) * A;
      const bgc = this.add.graphics();
      let img: Phaser.GameObjects.Image;
      if (round) {
        // окно круглое: лицо заранее вырезаем по кругу в отдельную картинку
        const d = Math.min(wW, wH), cx = wl + wW / 2, cy = wt + wH / 2;
        bgc.fillStyle(sys ? C.sysBg : 0xf3d9a4, 1).fillCircle(cx, cy, d / 2 + 3);
        img = this.add.image(cx, cy, this.roundFace(face, FACES[who0])).setDisplaySize(d + 4, d + 4);
      } else {
        bgc.fillStyle(sys ? C.sysBg : 0xf3d9a4, 1).fillRect(wl - 4, wt - 4, wW + 8, wH + 8);
        const [fx, fy, fs0] = FACES[who0];
        img = this.add.image(0, 0, face).setOrigin(0, 0).setCrop(fx, fy, fs0, fs0);
        const sc = Math.max(wW, wH) / fs0;
        img.setScale(sc).setPosition(wl - fx * sc + (wW - fs0 * sc) / 2, wt - fy * sc + (wH - fs0 * sc) / 2);
      }
      if (sys) img.setBlendMode(Phaser.BlendModes.ADD); // «система» нарисована линиями на чёрном
      const frame = artBox(this, fk, A, A, 10).setPosition(ax, ay);
      this.faceBox.add([bgc, img, frame]);
    } else if (KIT && this.textures.exists(face) && !hasArt(this, "k_avatar")) {
      const img = TALL ? this.add.image(W - 230, SHEET_TOP + 120, face).setOrigin(0.5, 1) : this.add.image(232, H + 16, face).setOrigin(0.5, 1);
      img.setScale(TALL ? Math.min(520 / img.height, 420 / img.width) : Math.min(820 / img.height, 480 / img.width));
      if (sys) img.setBlendMode(Phaser.BlendModes.ADD); // «система» нарисована линиями на чёрном
      this.faceBox.add(img);
    }
    // имя говорящего и название сцены сидят на верхнем крае листа
    const who = plate(this, SPEAK[ctx.scene.speaker] || "Рассказчик", fs(25), sys ? { fill: C.sysLine, lip: C.sysLineDark, color: C.sysBg } : {});
    who.setPosition(x0 + 40 + who.width / 2, SHEET_TOP - 4);
    const parts: Phaser.GameObjects.GameObject[] = [back, ...items, who];
    if (ctx.scene.title) {
      const tt = sys ? plate(this, ctx.scene.title, fs(22), { fill: C.sysBg, lip: 0x0a1826, color: C.sysLine }) : ribbonTag(this, ctx.scene.title, fs(23));
      parts.push(tt.setPosition(x0 + SHEET_W - 44 - tt.width / 2, SHEET_TOP - 4));
    }
    this.panel.add(parts);
    this.panelBottom = bottom + 14;
    return this.panelBottom;
  }

  // ------------------------------------------------------------ карточки выбора
  makeCard(L: Life, c: any, w: number, h: number, index: number): Box {
    const why = L.whyNot(c);
    const box = this.add.container(0, 0);
    const hot = glow(this, w, h).setVisible(false);
    // окно с рисунком: цвет окна говорит, обычный это выбор, особый или помощник
    const winColor = c.helper ? C.picHelper : c.requires ? C.picSpecial : C.picNormal;
    let picH: number, picTop: number, picL: number, picW: number;
    const back: Phaser.GameObjects.GameObject[] = [];
    // карточка по примеру автора (k_card2); особая — та же, золотая, с лучами и искрами позади
    const special = !!(c.helper || c.requires);
    const ck = hasArt(this, "k_card2") ? (special && hasArt(this, "k_card2_gold") ? "k_card2_gold" : "k_card2")
      : hasArt(this, "k_card") ? "k_card" : hasArt(this, "ui_card") ? "ui_card" : "";
    if (ck === "k_card2_gold") {
      // свет живёт в своём слое под карточками; showCards ставит его туда и водит вместе с карточкой
      const fx = this.specialFx(w, h);
      box.setData("fx", fx);
      box.once("destroy", () => fx.destroy());
    }
    if (ck) {
      // рисованная карточка: окно в ней прозрачное, под ним рисуем цвет окна
      const [sw, sh] = UI[ck].size, [wx, wy, ww, wh] = UI[ck].window!;
      picL = -w / 2 + (wx / sw) * w;
      picTop = -h / 2 + (wy / sh) * h;
      picW = (ww / sw) * w;
      picH = (wh / sh) * h;
      const win = this.add.graphics();
      win.fillStyle(winColor, 1).fillRect(picL - 6, picTop - 6, picW + 12, picH + 12);
      const card = artBox(this, ck, w, h, 14);
      card.addAt(win, card.length - 1);
      // новый рисунок во всё окно — под рамкой, края прячутся под неё
      if (this.textures.exists("full_" + c.art)) card.addAt(this.fullArt("full_" + c.art, picL - 6, picTop - 6, picW + 12, picH + 12), card.length - 1);
      back.push(card);
    } else {
      const g = slab(this, w, h, { r: 24, lipH: 14, shadow: 14 });
      picH = Math.round(h * 0.55);
      picTop = -h / 2 + 12;
      picL = -w / 2 + 12;
      picW = w - 24;
      g.fillStyle(winColor, 1).fillRoundedRect(picL, picTop, picW, picH, 14);
      g.lineStyle(6, C.ink, 1).strokeRoundedRect(picL, picTop, picW, picH, 14);
      back.push(g);
    }
    const pic = this.textures.exists("full_" + c.art) && ck ? this.add.container(0, 0) : this.art(c.art, picL + picW / 2, picTop + picH / 2, picW - 28, picH - 24);
    // подпись; если выбор закрыт — под ней причина
    // у резной карточки подпись стоит на табличке внутри рамы
    let labTop = picTop + picH, labH = h / 2 - 14 - labTop, labW = w - 36;
    const cap = ck ? UI[ck].caption : null;
    if (cap) {
      const [sw, sh] = UI[ck].size;
      labTop = -h / 2 + (cap[1] / sh) * h + 4;
      labH = (cap[3] / sh) * h - 8;
      labW = (cap[2] / sw) * w - 22;
    }
    const big = ck.startsWith("k_card2"); // у новой карточки табличка под текст большая
    const lsize = big ? (c.label.length > 44 ? 22 : c.label.length > 28 ? 24 : 27)
      : cap ? (c.label.length > 30 ? 20 : 23) : w < 290 ? 23 : c.label.length > 34 ? 25 : 28;
    // подпись ужимаем, пока не влезет в табличку
    let lsz = lsize, lab = txt(this, 0, 0, c.label, lsz, C.ink, { wrap: labW, align: "center", gap: -2 }).setOrigin(0.5);
    while (big && lab.height > labH - 10 && lsz > 16) {
      lab.destroy();
      lsz -= 1;
      lab = txt(this, 0, 0, c.label, lsz, C.ink, { wrap: labW, align: "center", gap: -2 }).setOrigin(0.5);
    }
    box.add([hot, ...back, pic, lab]);
    if (why) {
      const t = txt(this, 0, h / 2 - 20, why, 18, C.redDark, { wrap: w - 30, align: "center", gap: 0 }).setOrigin(0.5, 1);
      lab.setY(labTop + (labH - t.height) / 2);
      box.add(t);
    } else {
      lab.setY(labTop + labH / 2);
      // на верхнем крае — цена. Что заденет выбор, заранее не видно: значки показывает только карточка-подсказчик
      const cost = L.price(c);
      const parts: { k: StatKey; s?: string }[] = [];
      if (cost) parts.push({ k: "gold", s: "−" + cost });
      if (L.hints()) for (const k of L.touches(c)) if (!(cost && k === "gold")) parts.push({ k });
      if (parts.length) {
        const objs: Phaser.GameObjects.GameObject[] = [];
        let cx = 14;
        for (const p of parts) {
          objs.push(this.statIcon(p.k, cx + 19, 0, 38));
          cx += 38;
          if (p.s) {
            const t = txt(this, cx + 4, -2, p.s, 26, C.gold).setOrigin(0, 0.5);
            objs.push(t);
            cx += 4 + t.width;
          }
          cx += 6;
        }
        const cg = this.add.graphics();
        cg.fillStyle(C.plum, 1).fillRoundedRect(0, -25, cx + 8, 50, 25).lineStyle(6, C.ink, 1).strokeRoundedRect(0, -25, cx + 8, 50, 25);
        box.add(this.add.container(w / 2 + 12 - (cx + 8), -h / 2 - 4, [cg, ...objs]));
      }
    }
    // метка особого выбора на углу окна
    if (c.helper || c.requires) {
      // у новой карточки — в правом верхнем углу окна, чтобы не закрывать подпись
      const [mx, my] = big ? [picL + picW - 20, picTop + 20] : [w / 2 - 26, labTop - 4];
      box.add(this.specialMark(mx, my, 20, !!c.helper));
    }
    // цифры 1, 2, 3 на углу карточки убраны (автор: «можно убрать с карточек цифры»); клавиши 1–9 по-прежнему работают
    if (!hasArt(this, "k_card2")) {
      if (hasArt(this, "k_token")) {
        box.add(this.add.image(-w / 2 + 10, -h / 2 + 10, "k_token").setDisplaySize(62, 62));
        box.add(txt(this, -w / 2 + 10, -h / 2 + 8, String(index + 1), 30, C.white).setOrigin(0.5).setStroke(hex(C.ink), 6));
      } else box.add(this.dot(-w / 2 + 8, -h / 2 + 8, 27, C.wood, String(index + 1), 27));
    }
    box.setSize(w, h);
    if (why) box.setAlpha(0.62);
    box.setData({ choice: c, open: !why, hot });
    return box;
  }

  showCards(L: Life, opts: any[], top: number, onPick: (box: Box) => void) {
    if (TALL) return this.showRows(L, opts, top, onPick);
    this.cards.removeAll(true);
    this.cardFx.setAlpha(1);
    const n = opts.length, rows = n > 5 ? 2 : 1, per = Math.ceil(n / rows), gap = 26;
    // новая карточка высокая: если в ряду четыре и больше, ряд шире полосы под окном, иначе карточки мелкие
    const span = hasArt(this, "k_card2") && per >= 4 ? Math.max(CARDS_R - CARDS_L, 1160) : CARDS_R - CARDS_L;
    const avail = SHELF_Y - top - 24;
    let ch = rows === 1 ? Math.min(404, avail) : Math.min(330, (avail - gap) / 2);
    let cw = Math.min(rows === 1 ? 320 : 280, (span - (per - 1) * gap) / per);
    if (hasArt(this, "k_card2")) {
      // новая карточка выше: окно 1:1 и табличка под текст; высоту берём по рисунку рамки
      const ratio = UI.k_card2.size[1] / UI.k_card2.size[0];
      ch = Math.min(Math.round(cw * ratio), rows === 1 ? avail : (avail - gap) / 2);
      cw = Math.min(cw, Math.round(ch / ratio));
    }
    const boxes: Box[] = [];
    opts.forEach((c, i) => {
      const r = Math.floor(i / per), k = i % per, inRow = r === rows - 1 ? n - per * (rows - 1) : per;
      const mid = (inRow - 1) / 2;
      const x = W / 2 + (k - mid) * (cw + gap);
      // один ряд стоит на полке веером; два ряда — ровно
      const fan = rows === 1 ? (k - mid) * (inRow <= 3 ? 2.4 : 1.3) : 0;
      const y = SHELF_Y + 4 - ch / 2 - (rows - 1 - r) * (ch + gap) + (rows === 1 ? Math.abs(k - mid) * 4 : 0);
      const box = this.makeCard(L, c, cw, ch, i).setPosition(x, y + 30).setAlpha(0).setAngle(fan);
      this.cards.add(box);
      boxes.push(box);
      const fx = box.getData("fx");
      if (fx) this.cardFx.add(fx.setPosition(x, y + 30).setAlpha(0).setAngle(fan));
      const tg = fx ? [box, fx] : box;
      const open = box.getData("open");
      this.tweens.add({ targets: tg, y, alpha: open ? 1 : 0.62, duration: 220, delay: i * 45, ease: "Back.Out" });
      if (!open) return;
      const z = this.add.zone(0, 0, cw, ch).setInteractive({ useHandCursor: true });
      box.add(z);
      z.on("pointerover", () => {
        this.cards.bringToTop(box);
        box.getData("hot").setVisible(true);
        this.tweens.add({ targets: tg, y: y - 26, scale: 1.04, angle: 0, duration: 90 });
      });
      z.on("pointerout", () => {
        box.getData("hot").setVisible(false);
        this.tweens.add({ targets: tg, y, scale: 1, angle: fan, duration: 90 });
      });
      z.on("pointerup", () => onPick(box));
    });
    this.keyHandler = (num) => {
      const box = boxes[num - 1];
      if (box && box.getData("open")) onPick(box);
    };
  }

  // ------------------------------------------------------------ высокий экран (телефон в руке)
  /** Выборы строками сверху вниз: так по ним удобно попадать пальцем. */
  showRows(L: Life, opts: any[], top: number, onPick: (box: Box) => void) {
    this.cards.removeAll(true);
    const n = opts.length, gap = 14, avail = SHELF_Y - 30 - top;
    const rh = Math.max(92, Math.min(200, (avail - (n - 1) * gap) / n)), rw = W - 56;
    const boxes: Box[] = [];
    opts.forEach((c, i) => {
      const y = top + 8 + rh / 2 + i * (rh + gap);
      const box = this.makeRow(L, c, rw, rh).setPosition(W / 2, y + 30).setAlpha(0);
      this.cards.add(box);
      boxes.push(box);
      const open = box.getData("open");
      this.tweens.add({ targets: box, y, alpha: open ? 1 : 0.62, duration: 200, delay: i * 40, ease: "Sine.Out" });
      if (!open) return;
      const z = this.add.zone(0, 0, rw, rh).setInteractive({ useHandCursor: true });
      box.add(z);
      z.on("pointerdown", () => box.setScale(0.98));
      z.on("pointerout", () => box.setScale(1));
      z.on("pointerup", () => onPick(box));
    });
    this.keyHandler = (num) => {
      const box = boxes[num - 1];
      if (box && box.getData("open")) onPick(box);
    };
  }

  /** Одна строка выбора: слева рисунок в цветном окне, справа подпись, на правом крае цена. */
  makeRow(L: Life, c: any, w: number, h: number): Box {
    const why = L.whyNot(c);
    const box = this.add.container(0, 0);
    const hot = glow(this, w, h).setVisible(false);
    const winColor = c.helper ? C.picHelper : c.requires ? C.picSpecial : C.picNormal;
    let ps = h - 26, pl = -w / 2 + 12, pt = -h / 2 + 10, textL = -w / 2 + ps + 34; // окно с рисунком и где начинается подпись
    let pic: Phaser.GameObjects.GameObject;
    if (hasArt(this, "k_row")) {
      // резная широкая карточка: окно в ней прозрачное, под ним цвет окна
      const m = UI.k_row, k = artScale("k_row", w, h), [wx, wy, ww, wh] = m.window!;
      pl = -w / 2 + wx * k;
      pt = -h / 2 + wy * k;
      ps = Math.min(ww, wh) * k;
      textL = -w / 2 + m.slice![0] * k + 6;
      const win = this.add.graphics();
      win.fillStyle(winColor, 1).fillRect(pl - 6, pt - 6, ww * k + 12, wh * k + 12);
      const card = artBox(this, "k_row", w, h, 10);
      card.addAt(win, card.length - 1);
      const fk = "full_" + c.art;
      if (this.textures.exists(fk)) card.addAt(this.fullArt(fk, pl - 6, pt - 6, ww * k + 12, wh * k + 12), card.length - 1);
      pic = this.textures.exists(fk) ? this.add.container(0, 0) : this.art(c.art, pl + (ww * k) / 2, pt + (wh * k) / 2, ww * k - 16, wh * k - 16);
      box.add([hot, card, pic]);
    } else {
      const sheet = panel(this, "ui_sheet", w, h, { r: 22, lipH: 10, shadow: 10 });
      const g = this.add.graphics();
      g.fillStyle(winColor, 1).fillRoundedRect(pl, pt, ps, ps, 12);
      g.lineStyle(5, C.ink, 1).strokeRoundedRect(pl, pt, ps, ps, 12);
      pic = this.art(c.art, pl + ps / 2, pt + ps / 2, ps - 18, ps - 18);
      box.add([hot, sheet, g, pic]);
    }
    // цена на правом крае; что заденет выбор, видно только с карточкой-подсказчиком
    let right = w / 2 - 24;
    if (!why) {
      const cost = L.price(c);
      const parts: { k: StatKey; s?: string }[] = [];
      if (cost) parts.push({ k: "gold", s: "−" + cost });
      if (L.hints()) for (const k of L.touches(c)) if (!(cost && k === "gold")) parts.push({ k });
      if (parts.length) {
        const objs: Phaser.GameObjects.GameObject[] = [];
        let cx = 16;
        for (const p of parts) {
          objs.push(this.statIcon(p.k, cx + 24, 0, 48));
          cx += 48;
          if (p.s) {
            const t = txt(this, cx + 4, -2, p.s, 34, C.gold).setOrigin(0, 0.5);
            objs.push(t);
            cx += 4 + t.width;
          }
          cx += 8;
        }
        const cw = cx + 8, cg = this.add.graphics();
        cg.fillStyle(C.plum, 1).fillRoundedRect(0, -31, cw, 62, 31).lineStyle(6, C.ink, 1).strokeRoundedRect(0, -31, cw, 62, 31);
        box.add(this.add.container(w / 2 - 16 - cw, 0, [cg, ...objs]));
        right = w / 2 - 16 - cw - 16;
      }
    }
    const tx = textL, tw = right - tx;
    const lab = txt(this, tx, 0, c.label, h < 118 ? 28 : c.label.length > 40 ? 32 : 37, C.ink, { wrap: tw, gap: 0 }).setOrigin(0, 0.5);
    box.add(lab);
    if (why) {
      const t = txt(this, tx, h / 2 - 14, why, 22, C.redDark, { wrap: tw, gap: 0 }).setOrigin(0, 1);
      lab.setY(-t.height / 2 - 2);
      box.add(t);
    }
    if (c.helper || c.requires) box.add(this.specialMark(pl + ps - 6, pt + ps - 6, 20, !!c.helper));
    box.setSize(w, h);
    if (why) box.setAlpha(0.62);
    box.setData({ choice: c, open: !why, hot });
    return box;
  }

  /** Показатели в ряд сверху, особые карточки и личное дело на полке снизу. */
  drawHudTall(L: Life, ctx: Ctx | null, animate = false) {
    if (KIT) return this.drawHudTallKit(L, ctx, animate);
    this.life = L;
    const ch = ctx?.ch;
    this.hud.removeAll(true);
    HUD_ORDER.forEach((k, i) => {
      const v = L.stats[k], low = k !== "gold" && v <= 2;
      const x = 30 + 123 + i * 258, y = 88;
      const c = this.add.container(x, y);
      const g = this.add.graphics();
      g.fillStyle(0xfff1cf, 1).fillCircle(-64, -6, 46).lineStyle(6, low ? C.red : C.ink, 1).strokeCircle(-64, -6, 46);
      const num = String(v);
      c.add([panel(this, "ui_sheet", 246, 128, { r: 30, lipH: 10, shadow: 8 }), g, this.statIcon(k, -64, -6, 64),
        txt(this, 50, -10, num, num.length > 2 ? 44 : num.length > 1 ? 56 : 68, k === "gold" ? C.gold : low ? 0xffb9a8 : C.white).setOrigin(0.5).setStroke(hex(C.ink), 10)]);
      this.hud.add(c);
      const d = this.shown ? v - this.shown[k] : 0;
      if (animate && d) {
        const pop = txt(this, x, y + 70, sign(d), 60, d > 0 ? 0x8be06a : 0xff8a70).setOrigin(0.5, 0).setStroke(hex(C.ink), 10);
        this.hud.add(pop);
        this.tweens.add({ targets: pop, y: y + 130, alpha: 0, duration: 1600, ease: "Sine.Out", onComplete: () => pop.destroy() });
        this.tweens.add({ targets: c, scale: 1.1, duration: 110, yoyo: true });
      }
    });
    this.shown = { ...L.stats };
    this.hud.add(txt(this, 30, 172, "Жизнь " + L.n + (ch ? " · Глава " + ch.id.slice(2) + ". " + ch.title : ""), 30, C.cream).setStroke(hex(C.ink), 6));
    if (ch?.goal) this.hud.add(txt(this, 30, 214, "Цель: " + ch.goal, 28, C.gold, { wrap: W - 250, gap: 0 }).setStroke(hex(C.ink), 6));
    this.hud.add(plank(this, W - 110, 212, 170, 70, "Меню", () => this.gameMenu(), 30));

    this.hand.removeAll(true);
    this.side.removeAll(true);
    const cards = [...L.cards];
    const tile = cards.length > 5 ? 96 : 130, y = SHELF_Y + 112;
    cards.forEach((id, i) => {
      const cd = D.cards[id], x = 36 + tile / 2 + i * (tile + 12);
      const chip = this.add.container(x, y);
      chip.add([slab(this, tile, tile, { fill: cd.universal ? C.picHelper : cd.term === "sub" ? C.picSpecial : C.picNormal, lw: 6, r: 14, lipH: 6, shadow: 6 }),
        this.art(cd.art, 0, -3, tile - 26, tile - 30)]);
      let state = "";
      if (id in L.subs) {
        const free = L.subFree(id);
        state = free > 0 ? "Бесплатно ещё сцен: " + free + "." : "Сейчас берёт плату.";
        chip.add(this.dot(tile / 2 - 4, -tile / 2 + 4, 22, C.red, free > 0 ? String(free) : "!", 23));
      }
      const z = this.add.zone(0, 0, tile, tile).setInteractive({ useHandCursor: true });
      // на телефоне нет наведения: подсказка появляется по касанию и сама уходит
      z.on("pointerdown", () => this.showTip(W / 2, SHELF_Y - 200, cd.name, cd.text + (state ? " " + state : "")));
      z.on("pointerup", () => this.time.delayedCall(3000, () => this.hideTip()));
      chip.add(z);
      this.hand.add(chip);
    });
    const fx = W - 150;
    this.side.add(plank(this, fx, y, 250, 120, "Личное\nдело", () => showFile(L), 34));
    if (L.records.length) this.side.add(this.dot(fx + 116, y - 58, 26, C.red, String(L.records.length), L.records.length > 9 ? 22 : 26));
  }

  pick(L: Life, opts: any[], ctx: Ctx): Promise<any> {
    this.life = L;
    this.chosen = null;
    this.setBg(ctx.scene.bg);
    if (ctx.ch) play(trackFor(ctx.ch.id));
    const top = this.drawPanel(ctx);
    this.drawHud(L, ctx);
    return new Promise((res) => {
      let done = false;
      this.showCards(L, opts, top, (box) => {
        if (done) return;
        done = true;
        this.keyHandler = null;
        this.hideTip();
        this.chosen = box;
        box.getData("hot").setVisible(false);
        for (const o of this.cards.list as Box[]) o.each((ch: any) => ch.input && ch.disableInteractive());
        res(box.getData("choice"));
      });
    });
  }

  // ------------------------------------------------------------ исход
  /** Строки исхода: сначала плашки показателей в ряд, потом остальное текстом. */
  addLog(add: (o: Phaser.GameObjects.GameObject, h: number) => void, log: LogLine[]) {
    const stats = log.filter((l) => l.stat);
    if (stats.length) {
      const row = this.add.container(0, 0);
      let x = 0;
      for (const l of stats) {
        const up = l.d! > 0;
        const t = txt(this, 0, 0, sign(l.d!), 30, up ? C.greenDark : C.redDark).setOrigin(0, 0.5);
        const w = 54 + t.width + 22;
        const g = this.add.graphics();
        g.fillStyle(up ? 0xd9efcf : 0xf8d9cf, 1).fillRoundedRect(x, -26, w, 52, 26).lineStyle(5, C.ink, 1).strokeRoundedRect(x, -26, w, 52, 26);
        row.add([g, this.statIcon(l.stat!, x + 30, 0, 36), t.setPosition(x + 54, -2)]);
        x += w + 12;
      }
      const k = TALL ? 1.4 : 1; // на высоком экране плашки крупнее
      row.setScale(k);
      row.setData("top", 26 * k);
      add(row, 52 * k);
    }
    for (const l of log) {
      if (l.stat) continue;
      const [s, color] = l.give ? ["＋ Карточка: «" + D.cards[l.give].name + "»", C.greenDark]
        : l.take ? ["－ Карточка «" + D.cards[l.take].name + "» ушла", C.redDark]
        : l.record ? ["✎ В личное дело: «" + D.records[l.record].text + "»", C.brown]
        : [l.note || "", C.ink];
      const t = txt(this, 0, 0, s as string, fs(23), color as number, { wrap: (TALL ? 1000 : 900) - 68, gap: 2 });
      add(t, t.height);
    }
  }

  /** Большой лист по центру. Ждёт «Дальше». from — карточка, которая переворачивается. */
  bigCard(build: (add: (o: any, h: number) => void) => void, from: Box | null): Promise<void> {
    // у резной рамы поля шире: лист шире ровно на столько, чтобы строки остались той же длины
    const rk = hasArt(this, "k_panel2") ? "k_panel2" : "k_panel"; // лист исхода — в той же раме, что окно диалога
    const pad = KIT ? UI[rk].inner![0] * artScale(rk, 900, 400) + 22 : 36;
    const w = (TALL ? 1000 : 900) + (pad - 36) * 2;
    const parts: any[] = [];
    let y = 0;
    build((o, h) => {
      o.setPosition(-w / 2 + pad + (o.getData?.("dx") ?? 0), y + (o.getData?.("top") ?? 0));
      parts.push(o);
      y += h + 12;
    });
    let h = y + pad * 2 + (TALL ? 124 : 88);
    // на рисованном листе исхода печать торчит над листом и заходит на него: текст начинается ниже печати
    let sheet: Phaser.GameObjects.Container;
    let below = 0;
    if (KIT) {
      const m = UI[rk], ka = artScale(rk, w, h), [, iy] = m.inner!;
      below = Math.max(0, iy * ka + 14 - pad);
      h = Math.max(h + below, (m.slice![2] + m.slice![3]) * ka * 1.08);
      sheet = artBox(this, rk, w, h, 16);
    } else if (hasArt(this, "ui_result")) {
      const m = UI.ui_result, ka = artScale("ui_result", w, h);
      const above = (m.paper_top || 0) * ka;
      below = Math.max(0, ((m.content_top || 0) - (m.paper_top || 0)) * ka - pad + 8);
      h += below;
      sheet = artBox(this, "ui_result", w, h + above, 16).setPosition(0, -above / 2);
    } else sheet = panel(this, "ui_result", w, h, { r: 26, lipH: 14, shadow: 16 });
    // лист встаёт между текстом сцены и низом экрана; если не помещается — чуть уменьшается
    const room = H - 30 - this.panelBottom;
    const k = Math.min(1, room / h);
    const box = this.add.container(SHEET_L >= 0 ? SHEET_L + SHEET_W / 2 : W / 2, this.panelBottom + room / 2);
    parts.forEach((p) => p.setY(p.y - h / 2 + pad + below));
    box.add([sheet, ...parts]);
    this.front.add(box);
    return new Promise((res) => {
      let done = false;
      const go = () => {
        if (done) return;
        done = true;
        this.nextHandler = null;
        this.tweens.add({ targets: box, alpha: 0, duration: 120, onComplete: () => { box.destroy(); res(); } });
      };
      box.add(plank(this, 0, h / 2 - pad - (TALL ? 48 : 32), TALL ? 560 : 360, TALL ? 104 : 70, "Дальше", go, fs(30), { green: true }));
      this.nextHandler = go;
      const appear = () => {
        box.setScale(0, k);
        this.tweens.add({ targets: box, scaleX: k, duration: 170, ease: "Sine.Out" });
      };
      this.tweens.add({ targets: this.cardFx, alpha: 0, duration: 150 });
      if (from) {
        for (const o of this.cards.list as Box[]) if (o !== from) this.tweens.add({ targets: o, alpha: 0, duration: 150 });
        this.tweens.add({ targets: from, x: box.x, y: box.y, angle: 0, duration: 170, ease: "Sine.In" });
        this.tweens.add({ targets: from, scaleX: 0, duration: 170, ease: "Sine.In", onComplete: () => { this.cards.removeAll(true); appear(); } });
        box.setScale(0, k);
      } else {
        this.cards.removeAll(true);
        appear();
      }
    });
  }

  result(L: Life, ctx: Ctx, text: string, log: LogLine[]): Promise<void> {
    const from = this.chosen;
    this.chosen = null;
    if (!from) {
      this.setBg(ctx.scene.bg);
      this.drawPanel(ctx);
    }
    this.drawHud(L, ctx, true);
    return this.bigCard((add) => {
      if (text) {
        const t = txt(this, 0, 0, text, fs(text.length > 300 ? 26 : 29), C.ink, { font: "body", wrap: (TALL ? 1000 : 900) - 72, gap: 9 });
        add(t, t.height);
      }
      this.addLog(add, log);
    }, from);
  }

  verdict(L: Life, ctx: Ctx, ticks: Tick[], name: string, key: string, text: string, log: LogLine[]): Promise<void> {
    this.chosen = null;
    this.setBg(ctx.scene.bg);
    this.drawPanel(ctx);
    this.drawHud(L, ctx, true);
    const color = key === "great" ? C.greenDark : key === "shame" ? C.redDark : C.brown;
    return this.bigCard((add) => {
      const head = txt(this, 0, 0, "Мама смотрит на три вещи:", fs(25), C.brown);
      add(head, head.height);
      for (const t of ticks) {
        const line = txt(this, 0, 0, (t.ok ? "✓  " : "✗  ") + t.label, fs(27), t.ok ? C.greenDark : C.redDark);
        add(line, line.height);
      }
      const st = stamp(this, name, color);
      st.setData({ dx: st.width / 2 + 6, top: st.height / 2 + 6 });
      add(st, st.height + 14);
      const body = txt(this, 0, 0, text, fs(27), C.ink, { font: "body", wrap: (TALL ? 1000 : 900) - 72, gap: 9 });
      add(body, body.height);
      this.addLog(add, log);
    }, null);
  }

  // ------------------------------------------------------------ пропуск, доска, личное дело
  drawHud(L: Life, ctx: Ctx | null, animate = false) {
    if (TALL) return this.drawHudTall(L, ctx, animate);
    if (KIT) return this.drawHudKit(L, ctx, animate);
    this.life = L;
    const ch = ctx?.ch;

    // слева: пропуск на шнурке с четырьмя показателями
    this.hud.removeAll(true);
    if (hasArt(this, "ui_badge")) {
      // рисованный пропуск: сам пропуск от y=30 до y=596, ремешки уходят за верхний край экрана
      const k = artScale("ui_badge", 174, 640), top = 30 - (UI.ui_badge.body_top || 0) * k;
      this.hud.add(artBox(this, "ui_badge", 174, 596 - top, 10).setPosition(LEFT_X, (top + 596) / 2));
    } else {
      const cord = this.add.graphics();
      for (const x of [LEFT_X - 26, LEFT_X + 26]) {
        cord.lineStyle(17, C.ink, 1).lineBetween(x, -6, x, 42);
        cord.lineStyle(8, C.red, 1).lineBetween(x, -6, x, 42);
      }
      this.hud.add([cord, slab(this, 174, 566, { r: 24, shadow: 10 }).setPosition(LEFT_X, 313),
        slab(this, 72, 28, { fill: 0xa9b6bf, lip: 0x7f8c95, lw: 7, r: 9, lipH: 5, shadow: 0 }).setPosition(LEFT_X, 34)]);
    }
    HUD_ORDER.forEach((k, i) => {
      const v = L.stats[k], bar = k !== "gold", low = bar && v <= 2;
      const top = 66 + i * 132;
      const c = this.add.container(LEFT_X, top);
      const g = this.add.graphics();
      g.fillStyle(0x000000, 0.35).fillCircle(-38, 53, 41).fillStyle(0xfff1cf, 1).fillCircle(-38, 47, 41).lineStyle(6, low ? C.red : C.ink, 1).strokeCircle(-38, 47, 41);
      const num = String(v);
      c.add([g, this.statIcon(k, -38, 47, 58),
        txt(this, 42, 45, num, num.length > 2 ? 38 : num.length > 1 ? 50 : 60, k === "gold" ? C.gold : low ? 0xffb9a8 : C.white).setOrigin(0.5).setStroke(hex(C.ink), 10)]);
      if (bar) {
        const pw = (130 - 27) / 10, on = low ? C.red : v <= 5 ? 0xff9d2e : 0x5fc24a;
        for (let j = 0; j < 10; j++) g.fillStyle(j < v ? on : C.pip, 1).fillRoundedRect(-66 + j * (pw + 3), 98, pw, 16, 4).lineStyle(2, C.ink, 1).strokeRoundedRect(-66 + j * (pw + 3), 98, pw, 16, 4);
      }
      c.add(txt(this, -1, bar ? 126 : 108, STAT[k].toUpperCase(), 18, C.brown).setOrigin(0.5));
      this.hud.add(c);
      const d = this.shown ? v - this.shown[k] : 0;
      if (animate && d) {
        const pop = txt(this, LEFT_X + 104, top + 46, sign(d), 52, d > 0 ? 0x8be06a : 0xff8a70).setOrigin(0, 0.5).setStroke(hex(C.ink), 10);
        this.hud.add(pop);
        this.tweens.add({ targets: pop, x: LEFT_X + 150, alpha: 0, duration: 1600, ease: "Sine.Out", onComplete: () => pop.destroy() });
        this.tweens.add({ targets: c, scale: 1.1, duration: 110, yoyo: true });
      }
    });
    this.shown = { ...L.stats };
    // под пропуском: цель главы, записка на кнопке
    if (ch?.goal) {
      const nt = note(this, "ЦЕЛЬ ГЛАВЫ", ch.goal);
      this.hud.add(nt.setPosition(LEFT_X + 6, 640 + nt.height / 2).setAngle(-2));
    }

    // справа: доска с особыми карточками
    this.hand.removeAll(true);
    const cards = [...L.cards];
    const big = cards.length <= 3, tile = big ? 120 : 76, cols = big ? 1 : 2, step = tile + (big ? 22 : 10);
    const rowsN = Math.max(big ? 3 : 2, Math.ceil(cards.length / cols));
    const boardH = 78 + rowsN * step + 10;
    const nails = this.add.graphics();
    if (!hasArt(this, "ui_board")) nails.fillStyle(C.dwood, 1).fillCircle(RIGHT_X - 62, 52, 7).fillCircle(RIGHT_X + 62, 52, 7);
    this.hand.add([panel(this, "ui_board", 174, boardH, { fill: C.wood, lip: C.woodLip, r: 18, lipH: 14, shadow: 10 }).setPosition(RIGHT_X, 30 + boardH / 2), nails,
      txt(this, RIGHT_X, 66, "КАРТОЧКИ", 22, C.white).setOrigin(0.5).setStroke(hex(C.ink), 7)]);
    for (let i = 0; i < rowsN * cols; i++) {
      const x = RIGHT_X + (cols === 1 ? 0 : (i % cols - 0.5) * (tile + 10)), y = 98 + tile / 2 + Math.floor(i / cols) * step;
      const id = cards[i];
      if (!id) {
        // пустое место под карточку
        const e = this.add.graphics();
        e.fillStyle(C.dwood, 0.28).fillRoundedRect(x - tile / 2, y - tile / 2, tile, tile, 14).lineStyle(4, C.woodLip, 1).strokeRoundedRect(x - tile / 2, y - tile / 2, tile, tile, 14);
        this.hand.add(e);
        continue;
      }
      const cd = D.cards[id];
      const chip = this.add.container(x, y);
      chip.add([slab(this, tile, tile, { fill: cd.universal ? C.picHelper : cd.term === "sub" ? C.picSpecial : C.picNormal, lw: 6, r: 14, lipH: 6, shadow: 6 }),
        this.art(cd.art, 0, -3, tile - 26, tile - 30)]);
      let state = "";
      if (id in L.subs) {
        const free = L.subFree(id);
        state = free > 0 ? "Бесплатно ещё сцен: " + free + "." : "Сейчас берёт плату.";
        chip.add(this.dot(tile / 2 - 4, -tile / 2 + 4, big ? 20 : 16, C.red, free > 0 ? String(free) : "!", big ? 21 : 17));
      }
      const z = this.add.zone(0, 0, tile, tile).setInteractive({ useHandCursor: true });
      const show = () => {
        chip.setScale(1.08);
        this.showTip(RIGHT_X - 100 - 230, y, cd.name, cd.text + (state ? " " + state : ""));
      };
      z.on("pointerover", show);
      z.on("pointerup", show);
      z.on("pointerout", () => {
        chip.setScale(1);
        this.hideTip();
      });
      chip.add(z);
      this.hand.add(chip);
    }

    // под доской: личное дело и титул; на полке слева: какая жизнь и глава
    this.side.removeAll(true);
    const by = 30 + boardH + 30 + 43;
    this.side.add(plank(this, RIGHT_X, by, 206, 86, "Личное\nдело", () => showFile(L), 25));
    if (L.records.length) this.side.add(this.dot(RIGHT_X + 96, by - 42, 23, C.red, String(L.records.length), L.records.length > 9 ? 20 : 24));
    const t = L.title();
    if (t) {
      const tt = txt(this, 0, -4, "Титул:\n" + TAGS[t].title, 20, C.ink, { align: "center", gap: 0 }).setOrigin(0.5);
      this.side.add(this.add.container(RIGHT_X, by + 43 + 26 + (tt.height + 26) / 2, [panel(this, "ui_sheet", 206, tt.height + 26, { r: 14, lw: 6, lipH: 8, shadow: 8 }), tt]));
    }
    this.side.add(plank(this, W - 104, SHELF_Y + 38, 164, 52, "Меню", () => this.gameMenu(), 22));
    this.side.add(txt(this, 30, SHELF_Y + 43, "Жизнь " + L.n + (ch ? "  ·  Глава " + ch.id.slice(2) + ". " + ch.title + " (" + ch.age + ")" : ""), 24, C.cream).setOrigin(0, 0.5).setStroke(hex(C.ink), 6));
  }

  /** Телефон по наброску «Сцена с героями»: вывеска слева сверху, под ней жизнь и цель, внизу полка с карточками и кнопками. */
  drawHudTallKit(L: Life, ctx: Ctx | null, animate = false) {
    this.life = L;
    const ch = ctx?.ch;
    this.hud.removeAll(true);
    // показатели — маленькими значками в ряд сверху
    const row = STATS_LEFT ? this.statRow(L, 28, 56, false, 28, animate) : this.statRow(L, W / 2, 56, true, 28, animate);
    const info = txt(this, 30, row.bottom + 8, "Жизнь " + L.n + (ch ? " · Глава " + ch.id.slice(2) + ". " + ch.title : ""), 30, C.cream).setStroke(hex(C.ink), 6);
    this.hud.add(info);
    if (ch?.goal) this.hud.add(txt(this, 30, info.y + info.height + 4, "Цель: " + ch.goal, 28, C.gold, { wrap: W - 60, gap: 0 }).setStroke(hex(C.ink), 6));

    // внизу на полке: особые карточки в резных ячейках, справа личное дело и меню
    this.hand.removeAll(true);
    this.side.removeAll(true);
    const cards = [...L.cards];
    const tile = cards.length > 5 ? 96 : 124, y = SHELF_Y + 120;
    cards.forEach((id, i) => {
      const x = 30 + tile / 2 + i * (tile + 12);
      this.hand.add(this.handChip(L, id, x, y, tile, (t, tx) => this.showTip(W / 2, SHELF_Y - 200, t, tx),
        () => this.time.delayedCall(3000, () => this.hideTip())));
    });
    const fx = W - 160;
    this.side.add(plank(this, fx, SHELF_Y + 82, 280, 92, "Личное дело", () => showFile(L), 32));
    if (L.records.length) this.side.add(this.dot(fx + 132, SHELF_Y + 40, 26, C.red, String(L.records.length), L.records.length > 9 ? 22 : 26));
    this.side.add(plank(this, fx, SHELF_Y + 184, 280, 80, "Меню", () => this.gameMenu(), 30));
  }

  /** Экран по наброску «Сцена с героями»: вывеска с показателями слева сверху, доска с карточками справа сверху. */
  drawHudKit(L: Life, ctx: Ctx | null, animate = false) {
    this.life = L;
    const ch = ctx?.ch;
    this.hud.removeAll(true);
    // показатели — маленькими значками в ряд посередине вверху, как счётчики в Hades II
    if (STATS_LEFT) this.statRow(L, 26, 46, false, 25, animate);
    else this.statRow(L, SHEET_L + SHEET_W / 2, 46, true, 25, animate);
    // цель главы — записка справа вверху, где раньше была доска с карточками
    let ry = 40;
    if (ch?.goal) {
      const nt = note(this, "ЦЕЛЬ ГЛАВЫ", ch.goal, 260);
      this.hud.add(nt.setPosition(W - 30 - nt.width / 2, 20 + nt.height / 2).setAngle(2));
      ry = 20 + nt.height + 14;
    }

    // уникальные карточки — в ряд слева внизу, как дары в Hades; по три в ряд, лишние встают рядом выше
    this.hand.removeAll(true);
    const cards = [...L.cards];
    const tile = 88, gap = 12, perCol = 5, n = Math.max(3, cards.length);
    for (let i = 0; i < n; i++) {
      const x = 30 + tile / 2 + Math.floor(i / perCol) * (tile + gap), y = H - 30 - tile / 2 - (i % perCol) * (tile + gap);
      this.hand.add(this.handChip(L, cards[i] || null, x, y, tile, (t, tx) => this.showTip(x + 300, y - 60, t, tx), () => this.hideTip()));
    }

    // под запиской: личное дело и титул; внизу справа: какая жизнь и меню
    this.side.removeAll(true);
    const bx = W - 30 - 135, fy = ry + 40;
    this.side.add(plank(this, bx, fy, 270, 78, "Личное дело", () => showFile(L), 27));
    if (L.records.length) this.side.add(this.dot(bx + 128, fy - 36, 23, C.red, String(L.records.length), L.records.length > 9 ? 20 : 24));
    const t = L.title();
    if (t) this.side.add(plate(this, "Титул: " + TAGS[t].title, 22).setPosition(bx, fy + 84));
    this.side.add(plank(this, W - 110, H - 46, 170, 62, "Меню", () => this.gameMenu(), 24));
    const life = "Жизнь " + L.n + (ch ? "  ·  Глава " + ch.id.slice(2) + ". " + ch.title + " (" + ch.age + ")" : "");
    this.side.add(txt(this, W - 214, H - 44, life, 22, C.cream).setOrigin(1, 0.5).setStroke(hex(C.ink), 6));
  }

  /** Листок с подсказкой; середина в (x, y), за край экрана не выходит. */
  showTip(x: number, y: number, title: string, text: string) {
    this.hideTip();
    const w = TALL ? 900 : 460;
    const a = txt(this, 0, 0, title, fs(25), C.redDark);
    const b = txt(this, 0, 0, text, fs(22), C.ink, { font: "body", wrap: w - 44, gap: 6 });
    const h = a.height + b.height + 50;
    a.setPosition(-w / 2 + 22, -h / 2 + 16);
    b.setPosition(-w / 2 + 22, -h / 2 + 22 + a.height);
    const cx = Phaser.Math.Clamp(x, w / 2 + 20, W - w / 2 - 20), cy = Phaser.Math.Clamp(y, h / 2 + 20, H - h / 2 - 20);
    this.tip.add(this.add.container(cx, cy, [panel(this, "ui_sheet", w, h, { r: 16, lw: 6, lipH: 10, shadow: 10 }), a, b]));
  }
  hideTip() {
    this.tip.removeAll(true);
  }
}
