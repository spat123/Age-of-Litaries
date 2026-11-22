// Правила игры. Экрана здесь нет: всё, что надо показать или спросить, уходит в io.
// Это тот же порядок действий, что в story/tools/build.py (класс Life): правку правил вносим в оба места.
import { D, STAT, SUBS, TAGS, UNIVERSAL, SCENES, StatKey } from "./data";
import { crestImg } from "./overlay";

export type LogLine = { stat?: StatKey; d?: number; give?: string; take?: string; record?: string; note?: string };
export type Ctx = { scene: any; ch?: any; text: string; adds?: string[]; enter?: LogLine[]; then?: string | null };
export type Tick = { label: string; ok: boolean };

export interface IO {
  pick(L: Life, opts: any[], ctx: Ctx): Promise<any>;
  result(L: Life, ctx: Ctx, text: string, log: LogLine[]): Promise<void>;
  verdict(L: Life, ctx: Ctx, ticks: Tick[], name: string, key: string, text: string, log: LogLine[]): Promise<void>;
  /** Страница с длинным текстом. system — холодный «казённый» вид (Небесная HR, список исправлений). */
  page(L: Life | null, title: string, html: string, label?: string, system?: boolean): Promise<void>;
  /** Началась глава: экран может показать ленту пути. На правила не влияет, поэтому в build.py этого нет. Робот его не задаёт. */
  chapter?(L: Life, ch: any): Promise<void>;
  /** Запомнить место в игре. Вызывается перед каждой сценой и в конце жизни. Робот его не задаёт. */
  save?(s: Save): void;
  /** Жизнь кончилась: записать, что игрок уже видел за все жизни, и вернуть этот список. */
  lifeEnd?(L: Life, alive: boolean): Meta | null;
  /** Вопрос с несколькими кнопками. Возвращает номер нажатой. Робот его не задаёт. */
  ask?(title: string, html: string, labels: string[]): Promise<number>;
  /** Игрок закончил игру: стереть сохранение и вернуться в главное меню. */
  finish?(): void;
}

/** Что игрок видел за все жизни: концовки, смерти, титулы. Хранится отдельно от сохранения. */
export type Meta = { lives: number; endings: string[]; deaths: string[]; titles: string[]; finished?: boolean; path?: PathMark[] };
/** Отметка на ленте пути: в какой главе и чем кончилась жизнь номер n. */
export type PathMark = { n: number; ch: string; how: string; alive: boolean };

/** Место в жизни: номер главы, шаг в ней и сцены, которые ещё лежат в колоде главы. */
export type Pos = { ci: number; si: number; queue: string[] | null };
/** Сохранение. phase: «life» — идёт жизнь, «afterlife» — жизнь кончилась, впереди Небесная HR. */
export type Save = { v: 1; phase: "life" | "afterlife"; life: any; pos?: Pos; alive?: boolean };
const SNAP = ["n", "ending", "chId", "stats", "records", "subs", "subEvery", "subTrial", "shame", "uses", "verdicts", "dead", "overrides", "disabled", "tickRaise", "bribeMult", "patchNotes", "pigLine", "pigScene"] as const;

const rnd = (n: number) => Math.floor(Math.random() * n);
const pickOne = <T>(a: T[]) => a[rnd(a.length)];
const shuffle = <T>(a: T[]) => {
  for (let i = a.length - 1; i > 0; i--) {
    const j = rnd(i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};
const esc = (s: any) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" } as any)[c]);

export class Life {
  n: number;
  io: IO;
  stats: Record<StatKey, number> = {} as any;
  cards = new Set<string>();
  flags = new Set<string>();
  records: string[] = [];
  subs: Record<string, number> = {};
  subEvery: Record<string, number> = {};
  subTrial: Record<string, number> = {};
  shame = false;
  /** Какой концовкой кончилась жизнь, если герой дошёл до пещеры. */
  ending: string | null = null;
  /** Глава, до которой дожил герой. */
  chId: string | null = null;
  uses: Record<string, number> = {};
  verdicts: [string, string][] = [];
  dead: [string, string] | null = null;
  sceneId: string | null = null;
  overrides: Record<string, any> = {};
  disabled: Record<string, string> = {};
  tickRaise: Record<string, number> = {};
  bribeMult = 1;
  patchNotes: string[] = [];
  pigLine: string | null = null;
  pigScene: string | null = null;
  last: { text: string; log: LogLine[] } | null = null;

  constructor(n: number, carry: any, io: IO) {
    this.n = n;
    this.io = io;
    for (const [k, v] of Object.entries<any>(D.rules.stats)) this.stats[k as StatKey] = v.start;
    carry = carry || {};
    for (const [st, v] of Object.entries<number>(carry.nextLife || {})) this.stats[st as StatKey] += v;
    for (const s of carry.subs || []) {
      this.subs[s] = 99;
      this.cards.add(s);
    }
    if (carry.heir) {
      this.cards.add(carry.heir);
      for (const [st, v] of Object.entries<number>(D.cards[carry.heir].start || {})) this.stats[st as StatKey] += v;
      if (carry.heir === "three_coins") this.cards.delete(carry.heir);
    }
    if (carry.prev) this.applyPatches(carry.prev);
  }

  // ---- сохранение
  /** Всё, что нужно, чтобы продолжить эту жизнь после перезагрузки. */
  snapshot(): any {
    const o: any = { cards: [...this.cards], flags: [...this.flags] };
    for (const k of SNAP) o[k] = (this as any)[k];
    return JSON.parse(JSON.stringify(o));
  }
  /** Собирает жизнь из сохранения. Если в сохранении есть то, чего в игре уже нет, бросает ошибку. */
  static restore(snap: any, io: IO): Life {
    const L = new Life(snap.n, null, io);
    for (const k of SNAP) if (k in snap) (L as any)[k] = snap[k];
    L.cards = new Set(snap.cards);
    L.flags = new Set(snap.flags);
    for (const c of L.cards) if (!D.cards[c]) throw new Error("нет карточки " + c);
    for (const r of L.records) if (!D.records[r]) throw new Error("нет записи " + r);
    return L;
  }

  // ---- список исправлений между жизнями
  applyPatches(prev: Life) {
    const hits: any[] = D.after.patches.list.filter((p: any) => {
      const w = p.when;
      return (
        w.always ||
        (w.record && prev.records.includes(w.record)) ||
        (w.records_min && w.records_min.ids.filter((r: string) => prev.records.includes(r)).length >= w.records_min.n) ||
        (w.uses_min && (prev.uses[w.uses_min.card] || 0) >= w.uses_min.n) ||
        (w.died_in && prev.dead && prev.dead[1] === w.died_in) ||
        (w.ending && prev.ending === w.ending)
      );
    });
    const special: any[] = shuffle(hits.filter((p: any) => !p.when.always && !p.must)).slice(0, 2);
    // must — исправление срабатывает всегда, когда подходит (так мир помнит прошлую концовку)
    for (const p of special.concat(hits.filter((p: any) => p.must), hits.filter((p: any) => p.when.always))) {
      this.patchNotes.push(p.note);
      const e = p.effect;
      if (e.choice) {
        if (e.disable) this.disabled[e.choice] = e.disable;
        else this.overrides[e.choice] = e;
      }
      if (e.bribe_mult) this.bribeMult = e.bribe_mult;
      for (const [s, t] of Object.entries<number>(e.sub_trial || {})) this.subTrial[s] = t;
      if (e.tick_raise) this.tickRaise[e.tick_raise.scene + ":" + e.tick_raise.stat] = e.tick_raise.by;
      if (e.pig) this.pigLine = p.pig_line;
      if (e.world_flag) this.flags.add(e.world_flag); // отметка о мире: по ней сцены новой жизни идут иначе
    }
  }

  // ---- условия
  ok(c: any): boolean {
    if (!c) return true;
    const has = (r: string) => this.records.includes(r);
    if (c.card && !this.cards.has(c.card)) return false;
    if (c.no_card && this.cards.has(c.no_card)) return false;
    if (c.record && !has(c.record)) return false;
    if (c.no_record && has(c.no_record)) return false;
    if (c.record_any && !c.record_any.some(has)) return false;
    if (c.record_min && c.record_min.of.filter(has).length < c.record_min.n) return false;
    if (c.no_record_any && c.no_record_any.some(has)) return false;
    if (c.flag && !this.flags.has(c.flag)) return false;
    if (c.flag_any && !c.flag_any.some((f: string) => this.flags.has(f))) return false;
    if (c.no_flag && this.flags.has(c.no_flag)) return false;
    for (const [st, v] of Object.entries<number>(c.stat_min || {}))
      if (this.stats[st as StatKey] < v + (this.tickRaise[this.sceneId + ":" + st] || 0)) return false;
    for (const [st, v] of Object.entries<number>(c.stat_max || {})) if (this.stats[st as StatKey] > v) return false;
    if (c.life_min && this.n < c.life_min) return false;
    if (c.no_shame && this.shame) return false;
    if (c.sub && !(c.sub in this.subs)) return false;
    return true;
  }

  // ---- показатели
  change(stats: any, log?: LogLine[]) {
    for (const [st, d] of Object.entries<number>(stats || {})) {
      if (st === "mind" && d <= -2 && this.cards.has("mom_pride")) {
        this.cards.delete("mom_pride");
        log?.push({ note: "«Мамина гордость» сработала: потеря Менталки отменена. Карточка ушла." });
        continue;
      }
      this.stats[st as StatKey] += d;
      if (st !== "gold") this.stats[st as StatKey] = Math.min(this.stats[st as StatKey], D.rules.stats[st].max);
      if (d) log?.push({ stat: st as StatKey, d });
    }
    if (this.stats.mind <= 0 && this.cards.has("well_talk")) {
      this.cards.delete("well_talk");
      this.stats.mind = 2;
      log?.push({ note: "«Разговор у колодца» сработал: Менталка снова 2. Карточка ушла." });
    }
  }

  price(c: any): number {
    if (!c.cost) return 0;
    let g = c.cost.gold;
    for (const a of c.cost.alt || [])
      if (this.ok(a.if)) {
        g = a.gold;
        break;
      }
    return g * (c.cost.bribe ? this.bribeMult : 1);
  }

  /** Почему выбор закрыт. null — открыт. */
  whyNot(c: any): string | null {
    if (c.id in this.disabled) return this.disabled[c.id];
    if (c.disabled_if && this.ok(c.disabled_if.if)) return c.disabled_if.text;
    if (this.price(c) > Math.max(this.stats.gold, 0)) return "Не хватает монет: нужно " + this.price(c) + ".";
    if (c.then && !c.then.choices.some((x: any) => this.visible(x) && !this.whyNot(x))) return "Сейчас тут нечего выбрать.";
    return null;
  }
  visible(c: any) {
    return this.ok(c.requires);
  }
  result(c: any) {
    const o = this.overrides[c.id];
    const r = Object.assign({}, c.result);
    if (o) for (const k of ["text", "stats", "flag"]) if (k in o) r[k] = o[k];
    return r;
  }
  /** Какие показатели заденет выбор (без направления). */
  /** Видно ли заранее, какие показатели заденет выбор. Только если в руке есть карточка-подсказчик (поле hint в cards.json). */
  hints(): boolean {
    return [...this.cards].some((id) => D.cards[id]?.hint);
  }

  touches(c: any): StatKey[] {
    if (!c.result) return [];
    const st = Object.keys(this.result(c).stats || {}) as StatKey[];
    if (this.price(c) && !st.includes("gold")) st.push("gold");
    return st;
  }

  apply(r: any, log: LogLine[]) {
    if (r.death) this.dead = [r.death, this.sceneId!];
    if ("set_gold" in r) {
      this.stats.gold = r.set_gold;
      log.push({ note: "Золото теперь " + r.set_gold + "." });
    }
    this.change(r.stats, log);
    if (r.record && !this.records.includes(r.record)) {
      this.records.push(r.record);
      log.push({ record: r.record });
    }
    if (r.flag) this.flags.add(r.flag);
    if (r.ending) this.ending = r.ending;
    if (r.give) {
      this.cards.add(r.give);
      log.push({ give: r.give });
    }
    if (r.take) {
      this.cards.delete(r.take);
      log.push({ take: r.take });
    }
    if (r.uses) this.uses[r.uses] = (this.uses[r.uses] || 0) + 1;
    if (r.subscribe) {
      this.subs[r.subscribe] = 0;
      this.cards.add(r.subscribe);
      if (r.give !== r.subscribe) log.push({ give: r.subscribe });
    }
    if (r.unsubscribe) {
      delete this.subs[r.unsubscribe];
      this.cards.delete(r.unsubscribe);
      if (r.take !== r.unsubscribe) log.push({ take: r.unsubscribe });
    }
    for (const [s, e] of Object.entries<number>(r.sub_every || {})) this.subEvery[s] = e;
    if (r.shame) {
      this.shame = true;
      log.push({ note: "Это позор для семьи: мама запомнит до конца главы." });
    }
    if (r.clear_shame) this.shame = false;
  }

  // ---- подписки
  tickSubs(log: LogLine[]) {
    for (const s of Object.keys(this.subs)) {
      const spec = SUBS[s];
      this.subs[s] += 1;
      const paid = this.subs[s] - (s in this.subTrial ? this.subTrial[s] : spec.trial);
      const every = this.subEvery[s] || spec.every;
      if (paid > 0 && paid % every === 0) {
        let fee = Object.assign({}, spec.fee);
        if ("gold" in fee && this.stats.gold <= 0) fee = { body: -1 };
        const l: LogLine[] = [];
        this.change(fee, l);
        const what = l.filter((x) => x.stat).map((x) => STAT[x.stat!] + " " + (x.d! > 0 ? "+" : "−") + Math.abs(x.d!)).join(", ");
        log.push({ note: "«" + D.cards[s].name + "» берёт плату: " + what + "." });
        if (spec.payments && Math.floor(paid / every) >= spec.payments) {
          delete this.subs[s];
          this.cards.delete(s);
          log.push({ note: "«" + D.cards[s].name + "» выплачен." });
        }
      }
    }
  }
  /** Сколько сцен подписка ещё бесплатна (0 — уже берёт плату). */
  subFree(s: string) {
    const spec = SUBS[s];
    return Math.max(0, (s in this.subTrial ? this.subTrial[s] : spec.trial) - this.subs[s]);
  }

  rescue(cause: string) {
    for (const card of UNIVERSAL) {
      const h = (D.after.deaths[cause].helpers || {})[card];
      if (h && this.cards.has(card)) {
        this.cards.delete(card);
        Object.assign(this.stats, h.revive);
        const rec = D.cards[card].record;
        if (!this.records.includes(rec)) this.records.push(rec);
        return h;
      }
    }
    return null;
  }

/** Сколько записей каждого рода набралось за жизнь. */
  tagCounts(): Record<string, number> {
    const cnt: Record<string, number> = {};
    for (const r of this.records) {
      const t = (D.records[r] || {}).tag;
      if (t) cnt[t] = (cnt[t] || 0) + 1;
    }
    return cnt;
  }
  /** Все заработанные титулы: роды, в которых набралось нужное число записей. Первый — самый сильный. */
  titles(): string[] {
    return Object.entries(this.tagCounts()).filter(([, n]) => n >= D.rules.titles_need).sort((a, b) => b[1] - a[1]).map(([t]) => t);
  }
  title(): string | null {
    return this.titles()[0] || null;
  }

  // ---- ход сцены
  async choose(choices: any[], ctx: Ctx): Promise<any> {
    const back = new Set<string>();
    for (;;) {
      const opts = choices.filter((c) => this.visible(c) && !back.has(c.id));
      const c = await this.io.pick(this, opts, ctx);
      if (!c) return null;
      if (c.then) {
        const r = await this.choose(c.then.choices, { ...ctx, then: c.then.text });
        if (r === "back") {
          back.add(c.id);
          ctx = { ...ctx, then: null };
          continue;
        }
        return r;
      }
      const r = this.result(c);
      const log: LogLine[] = [];
      const cost = this.price(c);
      if (cost) {
        this.stats.gold -= cost;
        log.push({ stat: "gold", d: -cost });
      }
      if (r.back) {
        await this.io.result(this, ctx, r.text, []);
        return "back";
      }
      this.apply(r, log);
      if (r.again) {
        // вопрос: исход засчитан и показан, выбор в сцене продолжается без этой карточки
        await this.io.result(this, ctx, r.text, log);
        back.add(c.id);
        continue;
      }
      this.last = { text: r.text, log };
      return c;
    }
  }

  /** После выбора: долг, подписки, смерть. Потом показываем исход. */
  async after(ctx: Ctx, log: LogLine[]): Promise<boolean> {
    if (this.stats.gold < 0 && !this.dead) {
      await this.io.result(this, ctx, this.last!.text, this.last!.log.concat(log));
      log.length = 0;
      this.last = null;
      const ev = D.after.microloan;
      await this.choose(ev.choices, { scene: ev, ch: ctx.ch, text: ev.text });
    }
    this.tickSubs(log);
    const alive = await this.checkDeath(ctx, log);
    if (this.last) await this.io.result(this, ctx, this.last.text, this.last.log.concat(log));
    else if (log.length) await this.io.result(this, ctx, "", log);
    this.last = null;
    return alive;
  }

  async checkDeath(ctx: Ctx, log: LogLine[]): Promise<boolean> {
    if (this.dead) return false;
    for (const st of ["body", "mind", "rep"] as StatKey[]) {
      if (this.stats[st] <= 0) {
        const cause = D.rules.stats[st].death_at_min;
        const h = this.rescue(cause);
        if (h) {
          log.push({ note: h.text });
          continue;
        }
        this.dead = [cause, this.sceneId!];
        return false;
      }
    }
    if (this.stats.rep >= D.rules.stats.rep.max) {
      if (this.last) {
        await this.io.result(this, ctx, this.last.text, this.last.log.concat(log));
        log.length = 0;
        this.last = null;
      }
      const ev = D.after.promotion;
      await this.choose(ev.choices, { scene: ev, ch: ctx.ch, text: ev.text });
      if (this.dead) return false;
      return this.checkDeath(ctx, log);
    }
    return true;
  }

  async playScene(s: any, ch: any): Promise<boolean> {
    this.sceneId = s.id;
    const log: LogLine[] = [];
    this.change((s.enter || {}).stats, log);
    const adds: string[] = (s.text_add || []).filter((t: any) => this.ok(t.if)).map((t: any) => t.text);
    if (this.pigLine && this.pigScene === s.id) adds.push(this.pigLine);
    const ctx: Ctx = { scene: s, ch, text: s.text, adds, enter: log.slice() };
    log.length = 0;
    if (s.kind === "auto") {
      const v = s.variants.find((v: any) => this.ok(v.if));
      const l: LogLine[] = [];
      this.apply(v.result, l);
      this.last = { text: v.result.text, log: l };
    } else if (s.kind === "compare") {
      const ticks: Tick[] = s.ticks.map((t: any) => ({ label: t.label, ok: this.ok(t.if) }));
      const n = ticks.filter((t) => t.ok).length;
      let v = n >= 3 ? "great" : n >= 1 ? "ok" : "shame";
      const l: LogLine[] = [];
      if (v === "shame" && this.cards.has("good_conduct_note")) {
        this.cards.delete("good_conduct_note");
        v = "ok";
        l.push({ note: "Справка о хорошем поведении спасла от «Позор семьи». Карточка ушла." });
      }
      this.verdicts.push([s.id, v]);
      const spec = D.rules.verdicts[v];
      this.change(spec.stats, l);
      if (spec.give) {
        this.cards.add(spec.give);
        l.push({ give: spec.give });
      }
      await this.io.verdict(this, ctx, ticks, spec.name, v, s.verdict_text[v] + (s.text_after ? " " + s.text_after : ""), l);
      if (!(await this.checkDeath(ctx, log))) return false;
      await this.choose(s.choices, { ...ctx, text: "Как ответить?", adds: [], enter: [] });
      this.shame = false;
    } else {
      await this.choose(s.choices, ctx);
    }
    return this.after(ctx, log);
  }

  /** Проживает жизнь. from — место из сохранения; без него жизнь идёт с начала. */
  async play(from?: Pos): Promise<boolean> {
    if (!from) {
      const all = D.chapters.flatMap((ch: any) => ch.scenes.filter((s: any) => s.kind !== "compare" && s.kind !== "auto").map((s: any) => s.id));
      if (this.pigLine) this.pigScene = pickOne(all);
    }
    for (let ci = from ? from.ci : 0; ci < D.chapters.length; ci++) {
      const ch = D.chapters[ci];
      if (ch.id === "ch0" && this.n > 1) continue;
      this.chId = ch.id;
      const here = from && ci === from.ci;
      if (!(here && from!.si > 0)) await this.io.chapter?.(this, ch);
      let queue: any[] | null = here && from!.queue ? from!.queue.map((id) => SCENES[id]) : null;
      for (let si = here ? from!.si : 0; si < ch.flow.length; si++) {
        const step = ch.flow[si];
        let s: any;
        if (step === "deck") {
          if (!queue) {
            const pool = shuffle(ch.scenes.filter((x: any) => x.kind === "deck" && this.ok(x.requires)));
            queue = pool.slice(0, ch.flow.filter((x: string) => x === "deck").length).sort((a: any, b: any) => (b.early ? 1 : 0) - (a.early ? 1 : 0));
          }
          s = queue.shift();
        } else s = SCENES[step];
        // сцена с условием: если оно не выполнено, её в этой жизни нет
        if (step !== "deck" && s.requires && !this.ok(s.requires)) continue;
        // запоминаем место перед сценой: после перезагрузки она начнётся заново
        const rest = queue ? queue.map((x: any) => x.id) : null;
        this.io.save?.({ v: 1, phase: "life", life: this.snapshot(), pos: { ci, si, queue: step === "deck" ? [s.id, ...rest!] : rest } });
        if (!(await this.playScene(s, ch))) return false;
      }
      for (const [sid, spec] of Object.entries<any>(SUBS))
        if (spec.ends_after_chapter === ch.id && sid in this.subs) {
          delete this.subs[sid];
          this.cards.delete(sid);
        }
    }
    return true;
  }
}

/** Конец жизни по шагам: чем кончилась, итог жизни, Небесная HR, наследство.
 *  Возвращает то, что переходит в следующую жизнь. */
export async function afterlife(L: Life, io: IO, alive: boolean) {
  const A = D.after, hr = A.hr;
  const li = (rows: string[]) => "<ul>" + rows.map((r) => "<li>" + r + "</li>").join("") + "</ul>";

  // 1. чем кончилась жизнь
  let how: string;
  if (alive) {
    const e = (A.endings || {})[L.ending || ""] || { title: "Жизнь прожита", text: "Ты побывал в пещере дракона и вышел оттуда живым." };
    how = "концовка «" + e.title + "»";
    await io.page(L, "Концовка: " + e.title, "<p>" + esc(e.text) + "</p>", "Дальше");
  } else {
    const d = A.deaths[L.dead![0]];
    how = d.title;
    await io.page(L, d.title, "<p>" + esc(d.text) + "</p>", "Дальше");
  }

  // 2. итог жизни
  const seen = io.lifeEnd ? io.lifeEnd(L, alive) : null;
  const ch = D.chapters.find((c: any) => c.id === L.chId);
  const said = (k: string) => L.verdicts.filter((v) => v[1] === k).length;
  const cnt = L.tagCounts(), need = D.rules.titles_need;
  const rows = [
    "Чем кончилось: " + esc(how) + ".",
    ch ? "Дожил до главы " + ch.id.slice(2) + ": " + esc(ch.title) + " (" + esc(ch.age) + ")." : "",
    "Мама сказала: «Молодец» — " + said("great") + ", «Ну, сойдёт» — " + said("ok") + ", «Позор семьи» — " + said("shame") + ".",
    "Записей в личном деле: " + L.records.length + ".",
  ].filter(Boolean);
  const tags = Object.keys(TAGS).map((t) => ((cnt[t] || 0) >= need ? crestImg(t, 44) : "") + esc(TAGS[t].title) + ": " + (cnt[t] || 0) + " из " + need + ((cnt[t] || 0) >= need ? " — <b>титул</b>" : ""));
  let sum = li(rows) + "<p>Записи по родам. " + need + " записи одного рода дают титул и подарок на следующую жизнь:</p>" + li(tags);
  if (seen) {
    const all = Object.keys(A.endings || {}).filter((k) => k[0] !== "_").length;
    sum += "<p>За все жизни ты видел концовок: " + seen.endings.length + " из " + all + ".</p>";
  }
  await io.page(L, "Итог жизни " + L.n, sum, "В Небесную HR");

  // 2а. настоящий конец: кто перестал сравнивать, тому можно больше не рождаться
  const fin = A.final;
  if (alive && fin && L.records.includes(fin.record) && io.ask) {
    const i = await io.ask(fin.title, "<p>" + esc(fin.text) + "</p>", [fin.stop, fin.more]);
    if (i === 0) {
      const total = seen ? "<p>Прожито жизней: " + seen.lives + ". Концовок ты видел: " + seen.endings.length + " из " + Object.keys(A.endings || {}).filter((k) => k[0] !== "_").length + ".</p>" : "";
      await io.page(L, fin.end_title, "<p>" + esc(fin.end_text) + "</p>" + total, "В главное меню");
      io.finish?.();
      return new Promise<any>(() => {}); // игра окончена: дальше только главное меню
    }
  }

  // 3. Небесная HR: ангел читает дело и задаёт вопрос
  const file = L.records.map((r) => "<li>" + esc(D.records[r].text) + "</li>").join("");
  await io.page(L, hr.title, "<p>" + esc(hr.text) + "</p><ol>" + file + "</ol>", "Дальше", true);
  const ctx: Ctx = { scene: hr, text: hr.text_after_file.replace("{great}", String(said("great"))).replace("{chapters}", String(L.verdicts.length)) };
  const c = await io.pick(L, hr.choices, ctx);
  await io.result(L, ctx, c.result.text, []);

  // 4. наследство: подарок по титулу один; если титулов несколько, игрок выбирает
  const titles = L.titles();
  let heir: string | null = titles.length === 1 ? TAGS[titles[0]].heir : null;
  if (titles.length > 1) {
    const hctx: Ctx = { scene: hr, text: hr.titles_pick_text.replace("{titles}", titles.map((t) => TAGS[t].title).join(", ")) };
    const opts = titles.map((t) => {
      const card = D.cards[TAGS[t].heir];
      return { id: "heir_" + t, label: TAGS[t].title + ": «" + card.name + "»", art: card.art, heir: TAGS[t].heir, result: { text: A.heirs[TAGS[t].heir], stats: {} } };
    });
    const got = await io.pick(L, opts, hctx);
    heir = got.heir;
    await io.result(L, hctx, got.result.text, []);
  }
  const subs = Object.keys(L.subs).filter((x) => SUBS[x].survives_death);
  const pass: string[] = [];
  if (heir) pass.push("Подарок по титулу «" + esc(TAGS[titles.find((t) => TAGS[t].heir === heir)!].title) + "». " + esc(A.heirs[heir]));
  for (const x of subs) pass.push("Подписка «" + esc(D.cards[x].name) + "»: от неё ты так и не отказался.");
  for (const [st, v] of Object.entries<number>(c.result.next_life || {})) pass.push("От ангела: " + STAT[st as StatKey] + " " + (v > 0 ? "+" : "−") + Math.abs(v) + " на старте.");
  const head = titles.length === 0 ? "<p>" + esc(hr.no_title_text) + "</p>" : titles.length === 1 ? "<p>" + esc(hr.title_text.replace("{title}", TAGS[titles[0]].title)) + "</p>" : "";
  await io.page(L, hr.carry_title, head + li(pass.length ? pass : [esc(hr.carry_none)]) + "<p>" + esc(hr.carry_lost) + "</p>", "Дальше", true);
  return { nextLife: c.result.next_life, heir, subs, prev: L };
}

/** Проверяет сохранение: подходит ли оно к нынешнему сюжету. Возвращает его или null. */
export function checkSave(s: any): Save | null {
  try {
    if (!s || s.v !== 1 || !s.life) return null;
    Life.restore(s.life, null as any);
    if (s.phase === "afterlife") return s;
    const p = s.pos;
    if (s.phase !== "life" || !p || !D.chapters[p.ci] || p.si >= D.chapters[p.ci].flow.length) return null;
    if ((p.queue || []).some((id: string) => !SCENES[id])) return null;
    return s;
  } catch {
    return null;
  }
}

/** Бесконечная череда жизней. saved — сохранение, с которого надо продолжить. */
export async function run(io: IO, saved?: Save | null) {
  let carry: any = null, first = 1;
  if (saved) {
    const L = Life.restore(saved.life, io);
    let alive = !!saved.alive;
    if (saved.phase === "life") {
      alive = await L.play(saved.pos);
      io.save?.({ v: 1, phase: "afterlife", life: L.snapshot(), alive });
    }
    carry = await afterlife(L, io, alive);
    first = L.n + 1;
  }
  for (let n = first; ; n++) {
    const L = new Life(n, carry, io);
    if (n > 1)
      await io.page(
        L,
        "Что нового в мире",
        "<p>Пока тебя не было, Бог-Разработчик кое-что поправил:</p><ul>" + L.patchNotes.map((p) => "<li>" + esc(p) + "</li>").join("") + "</ul>",
        "Родиться заново",
        true,
      );
    const alive = await L.play();
    io.save?.({ v: 1, phase: "afterlife", life: L.snapshot(), alive });
    carry = await afterlife(L, io, alive);
  }
}

/** Проверка без экрана: прожить много жизней наугад и вернуть итоги. */
export async function autoplay(runs: number, lives = 1) {
  const robot: IO = {
    pick: (L, opts) => {
      const open = opts.filter((c) => !L.whyNot(c));
      return Promise.resolve(open.length ? pickOne(open) : null);
    },
    result: () => Promise.resolve(),
    verdict: () => Promise.resolve(),
    page: () => Promise.resolve(),
  };
  const out: any = { n: 0, alive: 0, deaths: {}, errors: 0 };
  for (let i = 0; i < runs; i++) {
    let carry: any = null;
    for (let n = 1; n <= lives; n++) {
      const L = new Life(n, carry, robot);
      try {
        const alive = await L.play();
        if (n === 1) {
          out.n++;
          if (alive) out.alive++;
          else out.deaths[L.dead![0]] = (out.deaths[L.dead![0]] || 0) + 1;
        }
        carry = await afterlife(L, robot, alive);
      } catch (e: any) {
        out.errors++;
        out.lastError = String((e && e.stack) || e);
        break;
      }
    }
  }
  return out;
}
