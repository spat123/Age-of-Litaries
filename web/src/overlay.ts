// Длинные тексты, списки и простые меню показываем обычной вёрсткой поверх игры:
// личное дело, смерть, Небесная HR, список исправлений, настройки.
import { D, TAGS } from "./data";
import type { Life, Meta, PathMark } from "./rules";
import { loadSettings, saveSettings } from "./audio";

const el = (id: string) => document.getElementById(id)!;
const esc = (s: any) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" } as any)[c]);

/** Открыта ли сейчас страница поверх игры. */
export const overlayOpen = () => !el("overlay").hidden;

/** Страница с кнопками: первая главная, остальные потише. Возвращает номер нажатой кнопки. */
/** Печать на странице «Итог жизни»: красный оттиск в углу папки, падает с ударом (анимация — CSS .ov-stamp). */
export function lifeStamp(label: string) {
  const p = el("ov-panel");
  p.querySelector(".ov-stamp")?.remove();
  const s = document.createElement("div");
  s.className = "ov-stamp";
  s.textContent = label;
  p.appendChild(s);
  p.classList.remove("thud");
  void p.offsetWidth;
  p.classList.add("thud");
}

export function showButtons(title: string, html: string, labels: string[], system = false, wide = false, dossier = false): Promise<number> {
  return new Promise((res) => {
    el("ov-panel").querySelector(".ov-stamp")?.remove();
    el("ov-panel").className = (system ? "sys" : "") + (wide ? " wide" : "") + (dossier ? " dossier" : "");
    el("overlay").className = dossier ? "desk" : "";
    el("ov-title").textContent = title;
    el("ov-body").innerHTML = html;
    const main = el("ov-btn") as HTMLButtonElement, more = el("ov-more");
    main.textContent = labels[0];
    more.innerHTML = "";
    const done = (i: number) => {
      more.innerHTML = "";
      el("overlay").hidden = true;
      res(i);
    };
    main.onclick = () => done(0);
    labels.slice(1).forEach((l, i) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "ov-other";
      b.textContent = l;
      b.onclick = () => done(i + 1);
      more.appendChild(b);
    });
    el("overlay").hidden = false;
    main.focus();
  });
}

/** Страница с одной кнопкой. Ждёт, пока её нажмут. */
export const showPage = (title: string, html: string, label = "Дальше", system = false, dossier = false): Promise<void> =>
  showButtons(title, html, [label], system, false, dossier).then(() => undefined);

/** Страница с двумя кнопками. Возвращает true, если нажали главную. */
export const showChoice = (title: string, html: string, main: string, other: string): Promise<boolean> => showButtons(title, html, [main, other]).then((i) => i === 0);

/** Личное дело героя: все записи этой жизни и титул. */
export function showFile(L: Life): Promise<void> {
  const t = L.title();
  const head = t ? "<p><b>Титул: " + esc(TAGS[t].title) + ".</b></p>" : "<p>Титула пока нет: нужно четыре записи одного рода.</p>";
  const list = L.records.length
    ? "<ol>" + L.records.map((r) => {
        const rec = D.records[r] || { text: r };
        return "<li>" + esc(rec.text) + (rec.tag ? ' <span class="tag">' + esc(TAGS[rec.tag].title.toLowerCase()) + "</span>" : "") + "</li>";
      }).join("") + "</ol>"
    : "<p>Записей пока нет.</p>";
  return showPage("Личное дело", head + list, "Закрыть", false, true);
}

/** Что игрок уже видел за все жизни. Чего не видел — закрыто вопросами. */
export function showSeen(m: Meta): Promise<void> {
  const A = D.after;
  const block = (title: string, all: [string, string][], seen: string[]) =>
    "<p><b>" + title + ": " + all.filter(([id]) => seen.includes(id)).length + " из " + all.length + "</b></p><ul>" +
    all.map(([id, name]) => "<li>" + (seen.includes(id) ? esc(name) : "???") + "</li>").join("") + "</ul>";
  const named = (o: any) => Object.entries<any>(o || {}).filter(([k]) => k[0] !== "_").map(([k, v]) => [k, v.title] as [string, string]);
  const html = "<p>Прожито жизней: " + m.lives + ".</p>" + block("Концовки", named(A.endings), m.endings) + block("Смерти", named(A.deaths), m.deaths) + block("Титулы", named(TAGS), m.titles);
  return showPage("Что я уже видел", html, "Назад");
}

/** Настройки: музыка и громкость. Меняются сразу. */
export function showSettings(): Promise<void> {
  const s = loadSettings();
  const html =
    '<p><label class="set"><input type="checkbox" id="set-music"' + (s.music ? " checked" : "") + "> Музыка</label></p>" +
    '<p><label class="set">Громкость <input type="range" id="set-vol" min="0" max="100" value="' + Math.round(s.volume * 100) + '"></label></p>';
  const done = showPage("Настройки", html, "Готово");
  const music = el("set-music") as HTMLInputElement, vol = el("set-vol") as HTMLInputElement;
  const apply = () => saveSettings({ music: music.checked, volume: +vol.value / 100 });
  music.onchange = apply;
  vol.oninput = apply;
  return done;
}

/** Лента пути: остановки-главы, где герой сейчас и где кончились прошлые жизни.
 *  thumb(фон, место по ширине) отдаёт маленькую круглую картинку остановки. */
export function pathHtml(L: Life | null, marks: PathMark[], thumb: (bg: string, x: number) => string): string {
  const A = D.after;
  const n = L ? L.n : 1;
  const cur = L ? D.chapters.findIndex((c: any) => c.id === L.chId) : -1;
  const past = marks.filter((m) => m.n < n).sort((a, b) => a.n - b.n);
  const how = (m: PathMark) => (m.alive ? "концовка «" + (((A.endings || {})[m.how] || {}).title || "Жизнь прожита") + "»" : (A.deaths[m.how] || {}).title || "смерть");
  const stops = D.chapters.map((ch: any, i: number) => {
    const hr = i === 0 && n > 1; // со второй жизни путь начинается не в пустоте, а в Небесной HR
    const name = hr ? A.hr.place : ch.place || ch.title;
    const age = hr ? "между жизнями" : ch.age;
    const pic = thumb(hr ? A.hr.bg : ch.place_bg, hr ? A.hr.place_x : ch.place_x ?? 0.5);
    const cls = i === cur ? "here" : i < cur ? "done" : "next";
    const here = past.filter((m) => m.ch === ch.id);
    const badges =
      here.slice(-4).map((m) => '<span class="mark' + (m.alive ? " win" : "") + '" title="Жизнь ' + m.n + ": " + esc(how(m)) + '">' + (m.alive ? "★" : "✝") + " " + m.n + "</span>").join("") +
      (here.length > 4 ? '<span class="mark">+' + (here.length - 4) + "</span>" : "");
    return (
      '<li class="' + cls + '"><span class="pic"' + (pic ? ' style="background-image:url(' + pic + ')"' : "") + "></span>" +
      '<span class="txt"><span class="name">' + esc(name) + '</span><span class="age">' + esc(age) + "</span>" +
      (i === cur ? '<span class="here-tag">ты здесь</span>' : "") + (badges ? '<span class="marks">' + badges + "</span>" : "") + "</span></li>"
    );
  });
  const list = past.slice(-4).map((m) => {
    const ch = D.chapters.find((c: any) => c.id === m.ch);
    return "<li>Жизнь " + m.n + ": " + esc(ch ? ch.place || ch.title : "?") + " — " + esc(how(m)) + "</li>";
  });
  return '<ol class="path">' + stops.join("") + "</ol>" + (list.length ? '<p class="past-head">Чем кончились прошлые жизни (✝ — смерть, ★ — концовка):</p><ul class="past">' + list.join("") + "</ul>" : "");
}

/** Страница с лентой пути. lead — что написать над лентой. */
export const showPath = (title: string, lead: string, L: Life | null, marks: PathMark[], thumb: (bg: string, x: number) => string, label = "Дальше"): Promise<void> =>
  showButtons(title, lead + pathHtml(L, marks, thumb), [label], false, true).then(() => undefined);
