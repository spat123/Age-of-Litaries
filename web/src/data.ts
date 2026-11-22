// Сюжет и правила берутся прямо из папки story/ — единственного места, где они хранятся.
import rules from "../../story/rules.json";
import cardsRaw from "../../story/cards.json";
import recordsRaw from "../../story/records.json";
import after from "../../story/afterlife.json";
import ch0 from "../../story/ch0_build.json";
import ch1 from "../../story/ch1_baby.json";
import ch2 from "../../story/ch2_childhood.json";
import ch3 from "../../story/ch3_youth.json";
import ch4 from "../../story/ch4_road.json";
import ch5 from "../../story/ch5_career.json";
import ch6 from "../../story/ch6_dragon.json";

const strip = (o: any) => Object.fromEntries(Object.entries(o).filter(([k]) => k[0] !== "_"));

export const D: any = {
  rules,
  cards: strip(cardsRaw),
  records: strip(recordsRaw),
  after,
  chapters: [ch0, ch1, ch2, ch3, ch4, ch5, ch6],
};

export type StatKey = "body" | "mind" | "gold" | "rep";
export const STAT: Record<StatKey, string> = { body: "Тело", mind: "Менталка", gold: "Золото", rep: "Репутация" };
export const STAT_ORDER: StatKey[] = ["body", "mind", "gold", "rep"];

export const SPEAK: Record<string, string> = {
  narrator: "Рассказчик", god: "Бог-Разработчик", mom: "Мама", father: "Отец", brother: "Брат", rival: "Сын Маминой Подруги",
  moms_friend: "Мамина подруга", merchant: "Купец", monk: "Монах", clerk: "Дьячок", recruiter: "Военком", troll: "Тролль",
  lag: "Сэр Лаг", goblin: "Гоблин", angel: "Ангел из Небесной HR", tax_man: "Сборщик налогов", elder: "Староста", miller: "Мельник",
  guard: "Стражник", inquisitor: "Инквизитор", matchmaker: "Сваха", landlady: "Хозяйка", innkeeper: "Трактирщик", smith: "Кузнец", herald: "Глашатай", king: "Король-директор", dragon: "Дракон", inspector: "Проверяющий",
};

export const TAGS: any = strip(D.rules.tags);
export const SUBS: any = strip(D.rules.subscriptions);
export const UNIVERSAL: string[] = Object.keys(D.cards).filter((k) => D.cards[k].universal);

export const SCENES: Record<string, any> = {};
for (const ch of D.chapters) for (const s of ch.scenes) SCENES[s.id] = s;

// Исход помощника из поля helpers становится обычным скрытым выбором сцены.
function addHelpers(scene: any) {
  for (const [card, h] of Object.entries<any>(scene.helpers || {})) {
    if (scene.choices.some((c: any) => c.id === scene.id + "__" + card)) continue; // уже добавлен
    const r = Object.assign({ stats: {} }, h.result, { take: card, record: D.cards[card].record });
    scene.choices.push({ id: scene.id + "__" + card, label: h.label, art: D.cards[card].art, requires: { card }, helper: card, result: r });
  }
}
Object.values(SCENES).forEach(addHelpers);
addHelpers(D.after.microloan);
addHelpers(D.after.promotion);
