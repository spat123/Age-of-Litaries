import Phaser from "phaser";
import { GameScene, W, H, setStage } from "./GameScene";
import { autoplay } from "./rules";
import { nowPlaying } from "./audio";
import { TEX } from "./assets";
import { UI } from "./ui";

// Рамка страниц поверх игры — те же рисованные вещи, что в игре: лист для обычных страниц, прибор для «системы».
// В CSS это border-image; края берутся из web/assets/ui/ui.json.
function cssFrame(name: string, key: string, line: number) {
  const m = UI[key];
  if (!m || !m.slice || !TEX[key]) return;
  const [l, r, t, b] = m.slice, k = m.line ? line / m.line : 0.5;
  const root = document.documentElement.style;
  root.setProperty("--" + name + "-img", 'url("' + TEX[key] + '")');
  root.setProperty("--" + name + "-slice", t + " " + r + " " + b + " " + l);
  root.setProperty("--" + name + "-w", [t, r, b, l].map((v) => Math.round(v * k) + "px").join(" "));
  document.body.classList.add("art-" + name);
}
cssFrame("sheet", "ui_sheet", 6);
// стол и папка для страниц «Личное дело» и «Итог жизни»
for (const [name, key] of [["desk", "d_desk"], ["folder", "d_folder"]]) {
  if (!TEX[key]) continue;
  document.documentElement.style.setProperty("--" + name + "-img", 'url("' + TEX[key] + '")');
  document.body.classList.add("art-" + name);
}
cssFrame("sys", "ui_system", 5);

// Телефон держат стоймя: для него у игры высокий экран. Вид выбирается один раз, при запуске.
const isTall = () => window.innerHeight > window.innerWidth;
const startedTall = isTall();
setStage(startedTall);
// Телефон повернули: вид экрана другой. Игра сохранена, поэтому просто открываем её заново.
let turn = 0;
window.addEventListener("resize", () => {
  clearTimeout(turn);
  turn = window.setTimeout(() => {
    if (isTall() !== startedTall) location.reload();
  }, 500);
});
// Маленький экран, который держат боком: буквы выйдут мелкими, подсказываем повернуть.
if (!startedTall && window.innerHeight < 520) {
  const hint = document.getElementById("hint");
  if (hint) {
    hint.hidden = false;
    window.setTimeout(() => (hint.hidden = true), 6000);
  }
}

const game = new Phaser.Game({
  type: Phaser.AUTO,
  parent: "game",
  backgroundColor: "#17110b",
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH, width: W, height: H },
  scene: [GameScene],
});

// Проверка правил без экрана: в консоли браузера `await autoplay(1000, 3)`.
(window as any).autoplay = autoplay;
(window as any).music = nowPlaying; // для проверки: что сейчас играет
(window as any).game = game; // для проверки: game.scene.getScene("game")
