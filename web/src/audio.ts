// Музыка и настройки. Три мелодии: главное меню, деревня (главы 0–4), столица (главы 5–6).
// Браузер не даёт играть звук, пока человек ничего не нажал, поэтому музыка включается после первого нажатия.
const files = import.meta.glob("../assets/audio/*.mp3", { eager: true, query: "?url", import: "default" }) as Record<string, string>;
const URLS: Record<string, string> = {};
for (const [p, u] of Object.entries(files)) URLS[p.split("/").pop()!.replace(".mp3", "")] = u;

export type Settings = { music: boolean; volume: number };
const KEY = "sirbug.settings.v1";

export function loadSettings(): Settings {
  const s: Settings = { music: true, volume: 0.5 };
  try { Object.assign(s, JSON.parse(localStorage.getItem(KEY) || "{}")); } catch {}
  return s;
}
export function saveSettings(s: Settings) {
  try { localStorage.setItem(KEY, JSON.stringify(s)); } catch {}
  refresh();
}

let cur: HTMLAudioElement | null = null;
let curName = "";
let want = "";
let unlocked = false;

function fade(a: HTMLAudioElement, to: number, ms: number, done?: () => void) {
  const from = a.volume, t0 = performance.now();
  const step = () => {
    const k = Math.min(1, (performance.now() - t0) / ms);
    a.volume = Math.max(0, Math.min(1, from + (to - from) * k));
    if (k < 1) requestAnimationFrame(step);
    else done?.();
  };
  step();
}

/** Для проверки: что сейчас играет. В консоли браузера — `music()`. */
export const nowPlaying = () => ({ name: curName, playing: !!cur && !cur.paused, volume: cur ? +cur.volume.toFixed(2) : 0, time: cur ? +cur.currentTime.toFixed(1) : 0 });

/** Какая мелодия нужна в главе. */
export const trackFor = (chId: string | null | undefined) => (chId === "ch5" || chId === "ch6" ? "capital" : "village");

/** Включить мелодию по имени: menu, village, capital. Та же мелодия не начинается заново. */
export function play(name: string) {
  want = name;
  const s = loadSettings();
  if (!unlocked || !s.music || !URLS[name]) return;
  if (name === curName && cur) {
    if (cur.paused) cur.play().catch(() => {});
    return;
  }
  const old = cur;
  if (old) fade(old, 0, 500, () => old.pause());
  const a = new Audio(URLS[name]);
  a.loop = true;
  a.volume = 0;
  cur = a;
  curName = name;
  a.play().then(() => fade(a, s.volume, 800)).catch(() => {});
}

/** Первое нажатие в игре: теперь звук разрешён. */
export function unlock() {
  if (unlocked) return;
  unlocked = true;
  if (want) play(want);
}

/** Настройки изменились: выключить музыку, включить или поменять громкость. */
export function refresh() {
  const s = loadSettings();
  if (!s.music) {
    cur?.pause();
    cur = null;
    curName = "";
  } else if (cur) cur.volume = s.volume;
  else if (want) play(want);
}
