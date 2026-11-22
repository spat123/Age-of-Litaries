// Снимает кадры игры в файлы: открывает страницу в Chrome без окна, нажимает клавиши и сохраняет картинки.
// Запуск: node web/tools/shot.mjs <адрес> <папка> <шаги>
// Шаги через запятую: число 1–9 — выбрать карточку, n — «Дальше» (пробел), w500 — подождать 500 мс,
// s:имя — сохранить кадр <папка>/<имя>.jpg, e:код — выполнить код на странице (без запятых), e:@файл — код из файла.
// Пример: node web/tools/shot.mjs http://localhost:5173 /tmp/shots "w2500,s:start,1,w900,s:result,n,w900,s:next"
import { spawn } from "node:child_process";
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [url, outDir, stepsArg = "w2500,s:shot"] = process.argv.slice(2);
if (!url || !outDir) { console.error("нужны адрес и папка"); process.exit(1); }
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9300 + Math.floor(Math.random() * 500);
const W = +(process.env.SHOT_W || 1920), H = +(process.env.SHOT_H || 1080);
const profile = mkdtempSync(join(tmpdir(), "shot-"));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn(CHROME, ["--headless=new", "--remote-debugging-port=" + PORT, "--user-data-dir=" + profile, "--window-size=" + W + "," + H,
  "--hide-scrollbars", "--force-device-scale-factor=1", "--no-first-run", "--mute-audio", "about:blank"], { stdio: "ignore" });

async function tab() {
  for (let i = 0; i < 60; i++) {
    try {
      const list = await (await fetch("http://127.0.0.1:" + PORT + "/json")).json();
      const t = list.find((x) => x.type === "page");
      if (t) return t;
    } catch {}
    await sleep(250);
  }
  throw new Error("Chrome не ответил");
}

let id = 0;
const waits = new Map();
let ws;
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; waits.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });

async function key(k, code, vk) {
  const base = { key: k, code, windowsVirtualKeyCode: vk, nativeVirtualKeyCode: vk };
  await send("Input.dispatchKeyEvent", { type: "keyDown", ...base, text: k });
  await send("Input.dispatchKeyEvent", { type: "keyUp", ...base });
}

try {
  const t = await tab();
  ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
  ws.onmessage = (m) => { const d = JSON.parse(m.data);
    // ошибки на странице печатаем сразу: так видно, если игра упала
    if (d.method === "Runtime.exceptionThrown") console.error("ошибка на странице:", d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text);
    const w = waits.get(d.id); if (w) { waits.delete(d.id); d.error ? w.rej(new Error(d.error.message)) : w.res(d.result); } };
  await send("Page.enable");
  await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 1, mobile: false });
  await send("Page.navigate", { url });
  mkdirSync(outDir, { recursive: true });
  for (const raw of stepsArg.split(",")) {
    const s = raw.trim();
    if (!s) continue;
    if (/^[1-9]$/.test(s)) await key(s, "Digit" + s, 48 + +s);
    else if (s === "n") {
      // «Дальше»: пробел в игре, а если открыта страница поверх игры — её кнопка
      const r = await send("Runtime.evaluate", { expression: "(()=>{const o=document.getElementById('overlay');if(o&&!o.hidden){document.getElementById('ov-btn').click();return 1}return 0})()", returnByValue: true });
      if (!r.result.value) await key(" ", "Space", 32);
    } else if (s[0] === "w") await sleep(+s.slice(1) || 500);
    else if (s.startsWith("e:")) {
      // e:@файл — код из файла (в нём можно писать запятые)
      const code = s[2] === "@" ? readFileSync(s.slice(3), "utf8") : s.slice(2);
      const r = await send("Runtime.evaluate", { expression: code, awaitPromise: true, returnByValue: true });
      if (r.exceptionDetails) console.error("ошибка в коде:", r.exceptionDetails.exception?.description || r.exceptionDetails.text);
      else if (r.result?.value !== undefined) console.log("ответ:", JSON.stringify(r.result.value));
    }
    else if (s.startsWith("s:")) {
      const r = await send("Page.captureScreenshot", { format: "jpeg", quality: 88 });
      const p = join(outDir, s.slice(2) + ".jpg");
      writeFileSync(p, Buffer.from(r.data, "base64"));
      console.log("кадр", p);
    } else console.error("непонятный шаг:", s);
  }
} catch (e) {
  console.error("ошибка:", e.message);
  process.exitCode = 1;
} finally {
  try { ws?.close(); } catch {}
  chrome.kill();
  await sleep(300);
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
