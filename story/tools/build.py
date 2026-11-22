#!/usr/bin/env python3
"""Проверяет сюжет первой части и собирает книгу для чтения.

Что делает:
  1. Читает story/*.json и ищет ошибки: несуществующие записи, карточки, сцены,
     условия, которые никогда не выполнятся, выборы без исхода.
  2. Проигрывает тысячи случайных жизней по тем же правилам, что будут в игре,
     и считает: как часто доходят до столицы, от чего умирают, что говорит мама,
     какие выборы никогда не выпадают.
  3. Пишет story/BOOK.md (читать в репозитории) и refs/kniga.html (читать в браузере).

Запуск из корня репозитория:  python3 story/tools/build.py
Это же — образец правил для будущего кода игры: см. класс Life.
"""
import html, json, os, random, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STORY = os.path.join(HERE, "..")
ROOT = os.path.join(STORY, "..")
STAT_NAMES = {"body": "Тело", "mind": "Менталка", "gold": "Золото", "rep": "Репутация"}
KIND_NAMES = {"anchor": "опорная", "deck": "из колоды", "compare": "сравнение", "auto": "сама", "event": "событие"}
TERM_NAMES = {"once": "разовая", "keep": "постоянная", "sub": "подписка"}
SPEAKERS = {"narrator": "Рассказчик", "god": "Бог-Разработчик", "mom": "Мама", "father": "Отец", "brother": "Брат",
            "rival": "Сын Маминой Подруги", "moms_friend": "Мамина подруга", "merchant": "Купец", "monk": "Монах",
            "clerk": "Дьячок", "recruiter": "Военком", "troll": "Тролль", "lag": "Сэр Лаг", "goblin": "Гоблин",
            "angel": "Ангел из Небесной HR", "tax_man": "Мытарь", "elder": "Староста", "miller": "Мельник", "guard": "Стражник", "inquisitor": "Инквизитор", "matchmaker": "Сваха", "landlady": "Хозяйка",
            "innkeeper": "Трактирщик", "smith": "Кузнец", "herald": "Глашатай",
            "king": "Король-директор", "dragon": "Дракон", "inspector": "Проверяющий"}


def load(name):
    with open(os.path.join(STORY, name), encoding="utf-8") as f:
        return json.load(f)


RULES = load("rules.json")
CARDS = {k: v for k, v in load("cards.json").items() if not k.startswith("_")}
RECORDS = {k: v for k, v in load("records.json").items() if not k.startswith("_")}
AFTER = load("afterlife.json")
CH_FILES = ["ch0_build.json", "ch1_baby.json", "ch2_childhood.json", "ch3_youth.json", "ch4_road.json", "ch5_career.json", "ch6_dragon.json"]
CHAPTERS = [load(f) for f in CH_FILES]
SCENES = {s["id"]: s for ch in CHAPTERS for s in ch["scenes"]}
SCENE_CH = {s["id"]: ch["id"] for ch in CHAPTERS for s in ch["scenes"]}
CH_IDS = [ch["id"] for ch in CHAPTERS]
TAGS = {k: v for k, v in RULES["tags"].items() if not k.startswith("_")}
UNIVERSAL = [k for k, v in CARDS.items() if v.get("universal")]   # помощники: можно позвать в любой сцене


def add_helpers(scene):
    """Исход помощника из поля helpers становится обычным скрытым выбором сцены."""
    for card, h in scene.get("helpers", {}).items():
        r = dict(h["result"])
        r.setdefault("stats", {})
        r.update({"take": card, "record": CARDS[card]["record"]})
        scene["choices"].append({"id": f"{scene['id']}__{card}", "label": h["label"], "art": CARDS[card]["art"],
                                 "requires": {"card": card}, "helper": card, "result": r})


for _s in list(SCENES.values()) + [AFTER["microloan"], AFTER["promotion"]]:
    add_helpers(_s)
SUBS = {k: v for k, v in RULES["subscriptions"].items() if not k.startswith("_")}


# ---------------------------------------------------------------- обход выборов
def walk_choices(choices, depth=0, parent=None):
    for c in choices:
        yield c, depth, parent
        if "then" in c:
            yield from walk_choices(c["then"]["choices"], depth + 1, c)


def all_choices():
    for sid, s in SCENES.items():
        for c, d, p in walk_choices(s.get("choices", [])):
            yield sid, c
    for ev in (AFTER["microloan"], AFTER["promotion"], AFTER["hr"]):
        for c, d, p in walk_choices(ev["choices"]):
            yield ev["id"], c


def all_results():
    """Все исходы: (сцена, выбор или None, исход)."""
    for sid, c in all_choices():
        if "result" in c:
            yield sid, c, c["result"]
    for sid, s in SCENES.items():
        for v in s.get("variants", []):
            yield sid, None, v["result"]


def conds():
    """Все условия в сюжете: (где, условие)."""
    for sid, s in SCENES.items():
        if "requires" in s:
            yield f"сцена {sid}", s["requires"]
        for t in s.get("text_add", []):
            yield f"текст сцены {sid}", t["if"]
        for t in s.get("ticks", []):
            yield f"галочка в {sid}", t["if"]
        for v in s.get("variants", []):
            yield f"вариант в {sid}", v["if"]
    for sid, c in all_choices():
        if "requires" in c:
            yield f"выбор {c['id']}", c["requires"]
        if "disabled_if" in c:
            yield f"запрет выбора {c['id']}", c["disabled_if"]["if"]
        for a in c.get("cost", {}).get("alt", []):
            yield f"цена выбора {c['id']}", a["if"]


# ---------------------------------------------------------------- проверка
def validate():
    errors, warns = [], []
    seen = set()
    for sid, c in all_choices():
        if c["id"] in seen:
            errors.append(f"выбор {c['id']} встречается дважды")
        seen.add(c["id"])
        for key in ("label", "art"):
            if not c.get(key):
                errors.append(f"у выбора {c['id']} нет поля {key}")
        if ("then" in c) == ("result" in c):
            errors.append(f"у выбора {c['id']} должно быть ровно одно из: then, result")
        if len(c.get("label", "")) > 52:
            warns.append(f"длинная подпись ({len(c['label'])} знаков) у выбора {c['id']}")
    set_records, set_flags, given, subscribed = set(), set(), set(), set()
    for sid, c, r in all_results():
        where = c["id"] if c else sid
        if not r.get("text"):
            errors.append(f"у исхода {where} нет текста")
        elif len(r["text"]) > 330:
            warns.append(f"длинный исход ({len(r['text'])} знаков): {where}")
        if r.get("ending") and r["ending"] not in AFTER.get("endings", {}):
            errors.append(f"{where}: концовки {r['ending']} нет в afterlife.json")
        if "record" in r:
            if r["record"] not in RECORDS:
                errors.append(f"{where}: записи {r['record']} нет в records.json")
            set_records.add(r["record"])
        if r.get("flag"):
            set_flags.add(r["flag"])
        for _p in AFTER["patches"]["list"]:
            if "world_flag" in _p["effect"]:
                set_flags.add(_p["effect"]["world_flag"])
        for key in ("give", "take", "uses"):
            if key in r and r[key] not in CARDS:
                errors.append(f"{where}: карточки {r[key]} нет в cards.json")
        if "give" in r:
            given.add(r["give"])
        for key in ("subscribe", "unsubscribe"):
            if key in r and r[key] not in SUBS:
                errors.append(f"{where}: подписки {r[key]} нет в rules.json")
        if "subscribe" in r:
            subscribed.add(r["subscribe"])
        for st in r.get("stats", {}):
            if st not in STAT_NAMES:
                errors.append(f"{where}: неизвестный показатель {st}")
    heirs = {t["heir"] for t in TAGS.values()} | {"mom_pride"}
    for rid, rec in RECORDS.items():
        if rid not in set_records:
            warns.append(f"запись {rid} есть в records.json, но её никто не ставит")
        if "tag" in rec and rec["tag"] not in TAGS:
            errors.append(f"у записи {rid} неизвестный род {rec['tag']}")
    for where, cond in conds():
        for key in ("record", "no_record"):
            if key in cond and cond[key] not in set_records:
                errors.append(f"{where}: условие ждёт запись {cond[key]}, которую никто не ставит")
        for key in ("record_any", "no_record_any"):
            for rid in cond.get(key, []):
                if rid not in set_records:
                    errors.append(f"{where}: условие ждёт запись {rid}, которую никто не ставит")
        for key in ("card", "no_card"):
            if key in cond and cond[key] not in given | heirs:
                errors.append(f"{where}: условие ждёт карточку {cond[key]}, которую негде получить")
        for fl in ([cond["flag"]] if "flag" in cond else []) + cond.get("flag_any", []):
            if fl not in set_flags:
                errors.append(f"{where}: условие ждёт отметку {fl}, которую никто не ставит")
        if "sub" in cond and cond["sub"] not in subscribed:
            errors.append(f"{where}: условие ждёт подписку {cond['sub']}, которую негде оформить")
    for cid in CARDS:
        if cid not in given | heirs | subscribed:
            warns.append(f"карточку {cid} негде получить")
    for ch in CHAPTERS:
        ids = {s["id"] for s in ch["scenes"]}
        decks = [s for s in ch["scenes"] if s["kind"] == "deck"]
        if "flow" not in ch:
            errors.append(f"в главе {ch['id']} нет порядка сцен (flow)")
            continue
        for step in ch["flow"]:
            if step != "deck" and step not in ids:
                errors.append(f"в порядке главы {ch['id']} нет сцены {step}")
        free = [s for s in decks if "requires" not in s]
        if ch["flow"].count("deck") > len(free):
            errors.append(f"в главе {ch['id']} колода меньше, чем нужно сцен")
        for s in ch["scenes"]:
            if s["kind"] not in ("deck",) and s["id"] not in ch["flow"]:
                errors.append(f"сцена {s['id']} не стоит в порядке главы {ch['id']}")
    for card in UNIVERSAL:
        got = [(SCENE_CH[sid], sid) for sid, c, r in all_results() if r.get("give") == card and sid in SCENES]
        if not got:
            continue
        ch_i = min(CH_IDS.index(ch) for ch, _ in got)
        for i, ch in enumerate(CHAPTERS[ch_i:], ch_i):
            flow = ch["flow"]
            pos = min((flow.index(sid) for c, sid in got if c == ch["id"] and sid in flow), default=-1) if i == ch_i else -1
            later = set(flow[pos + 1:])
            for sc in ch["scenes"]:
                need = (sc["kind"] == "deck" and "deck" in later) or sc["id"] in later
                if need and sc["kind"] != "auto" and card not in sc.get("helpers", {}):
                    errors.append(f"в сцене {sc['id']} нет исхода для помощника {card}")
        for k in ("microloan", "promotion"):
            if card not in AFTER[k].get("helpers", {}):
                warns.append(f"в событии {k} нет исхода для помощника {card}")
        for k, d in AFTER["deaths"].items():
            if k != "death_rep_high" and card not in d.get("helpers", {}):
                warns.append(f"смерть {k}: помощник {card} не может спасти")
    return errors, warns


# ---------------------------------------------------------------- правила игры
def cond_ok(cond, L):
    """Проверка условия. L — жизнь (объект Life)."""
    if not cond:
        return True
    if "card" in cond and cond["card"] not in L.cards:
        return False
    if "no_card" in cond and cond["no_card"] in L.cards:
        return False
    if "record" in cond and cond["record"] not in L.records:
        return False
    if "no_record" in cond and cond["no_record"] in L.records:
        return False
    if "record_any" in cond and not any(r in L.records for r in cond["record_any"]):
        return False
    if "record_min" in cond and sum(r in L.records for r in cond["record_min"]["of"]) < cond["record_min"]["n"]:
        return False
    if "no_record_any" in cond and any(r in L.records for r in cond["no_record_any"]):
        return False
    if "flag" in cond and cond["flag"] not in L.flags:
        return False
    if "flag_any" in cond and not any(f in L.flags for f in cond["flag_any"]):
        return False
    if "no_flag" in cond and cond["no_flag"] in L.flags:
        return False
    for st, v in cond.get("stat_min", {}).items():
        if L.stats[st] < v + L.tick_raise.get((L.scene_id, st), 0):
            return False
    for st, v in cond.get("stat_max", {}).items():
        if L.stats[st] > v:
            return False
    if "life_min" in cond and L.n < cond["life_min"]:
        return False
    if cond.get("no_shame") and L.shame:
        return False
    if "sub" in cond and cond["sub"] not in L.subs:
        return False
    return True


class Life:
    """Одна жизнь. Образец правил для кода игры."""

    def __init__(self, n=1, carry=None, rng=None, policy="random"):
        self.n = n
        self.rng = rng or random
        self.policy = policy
        self.stats = {k: v["start"] for k, v in RULES["stats"].items()}
        self.cards, self.flags, self.records = set(), set(), []
        self.subs = {}            # подписка -> сколько сцен прошло
        self.sub_every = {}
        self.sub_trial = {}
        self.shame = False
        self.ending = None   # какой концовкой кончилась жизнь (если дошёл до пещеры)
        self.uses = Counter()
        self.taken = []           # выбранные исходы
        self.verdicts = []
        self.dead = None          # (причина, сцена)
        self.scene_id = None
        self.fired = 0            # сколько раз аукнулось прошлое
        self.overrides, self.disabled, self.tick_raise = {}, {}, {}
        self.bribe_mult = 1
        self.patch_notes = []
        carry = carry or {}
        for st, v in carry.get("next_life", {}).items():
            self.stats[st] += v
        for sid in carry.get("subs", []):
            self.subs[sid] = 99
        heir = carry.get("heir")
        if heir:
            self.cards.add(heir)
            for st, v in CARDS[heir].get("start", {}).items():
                self.stats[st] += v
            if heir == "three_coins":
                self.cards.discard(heir)
        self.apply_patches(carry.get("prev"))

    # ---- список исправлений
    def apply_patches(self, prev):
        if not prev:
            return
        hits = []
        for p in AFTER["patches"]["list"]:
            w = p["when"]
            ok = (w.get("always")
                  or ("record" in w and w["record"] in prev.records)
                  or ("records_min" in w and sum(r in prev.records for r in w["records_min"]["ids"]) >= w["records_min"]["n"])
                  or ("uses_min" in w and prev.uses[w["uses_min"]["card"]] >= w["uses_min"]["n"])
                  or ("died_in" in w and prev.dead and prev.dead[1] == w["died_in"])
                  or ("ending" in w and prev.ending == w["ending"]))
            if ok:
                hits.append(p)
        special = [p for p in hits if not p["when"].get("always") and not p.get("must")]
        self.rng.shuffle(special)
        # must — исправление срабатывает всегда, когда подходит (так мир помнит прошлую концовку)
        for p in special[:2] + [p for p in hits if p.get("must")] + [p for p in hits if p["when"].get("always")]:
            self.patch_notes.append(p["note"])
            e = p["effect"]
            if "choice" in e:
                if "disable" in e:
                    self.disabled[e["choice"]] = e["disable"]
                else:
                    self.overrides[e["choice"]] = e
            if "bribe_mult" in e:
                self.bribe_mult = e["bribe_mult"]
            for sid, t in e.get("sub_trial", {}).items():
                self.sub_trial[sid] = t
            if "tick_raise" in e:
                t = e["tick_raise"]
                self.tick_raise[(t["scene"], t["stat"])] = t["by"]
            if "world_flag" in e:   # отметка о мире: по ней сцены новой жизни идут иначе
                self.flags.add(e["world_flag"])

    # ---- показатели
    def change(self, stats):
        for st, d in stats.items():
            if st == "mind" and d <= -2 and "mom_pride" in self.cards:
                self.cards.discard("mom_pride")
                self.fired += 1
                continue
            self.stats[st] += d
            if st != "gold":
                self.stats[st] = min(self.stats[st], RULES["stats"][st]["max"])
        if self.stats["mind"] <= 0 and "well_talk" in self.cards:
            self.cards.discard("well_talk")
            self.stats["mind"] = 2
            self.fired += 1

    def check_death(self):
        if self.dead:
            return True
        for st in ("body", "mind", "rep"):
            if self.stats[st] <= 0:
                cause = RULES["stats"][st]["death_at_min"]
                if self.rescue(cause):
                    continue
                self.dead = (cause, self.scene_id)
                return True
        if self.stats["rep"] >= RULES["stats"]["rep"]["max"]:
            self.play_choices(AFTER["promotion"]["choices"])   # повышение: можно отказаться
            if self.dead:
                return True
            return self.check_death()
        return False

    def rescue(self, cause):
        """Помощник в руке спасает от смерти: показатель поднимается, карточка уходит."""
        for card in UNIVERSAL:
            h = AFTER["deaths"][cause].get("helpers", {}).get(card)
            if h and card in self.cards:
                self.cards.discard(card)
                self.stats.update(h["revive"])
                self.taken.append(f"{cause}__{card}")
                if CARDS[card]["record"] not in self.records:
                    self.records.append(CARDS[card]["record"])
                self.fired += 1
                return True
        return False

    # ---- цена и доступность
    def price(self, c):
        cost = c.get("cost")
        if not cost:
            return 0
        g = cost["gold"]
        for a in cost.get("alt", []):
            if cond_ok(a["if"], self):
                g = a["gold"]
                break
        return g * (self.bribe_mult if cost.get("bribe") else 1)

    def available(self, c):
        if c["id"] in self.disabled:
            return False
        if not cond_ok(c.get("requires"), self):
            return False
        if "disabled_if" in c and cond_ok(c["disabled_if"]["if"], self):
            return False
        if self.price(c) > max(self.stats["gold"], 0):
            return False
        if "then" in c and not any(self.available(x) for x in c["then"]["choices"]):
            return False
        return True

    # ---- выбор (за игрока решает случай или осторожность)
    def score(self, c):
        if "then" in c:
            opts = [x for x in c["then"]["choices"] if self.available(x)]
            return max(self.score(x) for x in opts) if opts else -99
        r = self.overrides.get(c["id"], c["result"])
        s = -0.3 * self.price(c)
        for st, d in r.get("stats", c["result"].get("stats", {})).items():
            v = self.stats[st]
            if st == "gold":
                s += 0.3 * d
            elif st == "rep":
                s += d * (3 if v <= 3 else 1) if v < 7 else -d * 3
            else:
                s += d * (3 if v <= 3 else 1.5 if v <= 5 else 1)
        return s + self.rng.random()

    def pick(self, choices):
        opts = [c for c in choices if self.available(c)]
        if not opts:
            return None
        if self.policy == "careful":
            return max(opts, key=self.score)
        return self.rng.choice(opts)

    def play_choices(self, choices):
        tried_back = set()
        while True:
            c = self.pick([x for x in choices if x["id"] not in tried_back])
            if c is None:
                return
            if "then" in c:
                if self.play_choices(c["then"]["choices"]) == "back":
                    tried_back.add(c["id"])
                    continue
                return
            self.stats["gold"] -= self.price(c)
            if c.get("requires") and c["requires"].keys() & {"card", "record", "sub"}:
                self.fired += 1
            r = dict(c["result"])
            r.update({k: v for k, v in self.overrides.get(c["id"], {}).items() if k in ("text", "stats", "flag")})
            self.taken.append(c["id"])
            if r.get("back"):
                return "back"
            self.apply(r)
            if r.get("again"):   # вопрос: исход засчитан, выбор в сцене продолжается
                tried_back.add(c["id"])
                continue
            return

    def apply(self, r):
        if r.get("ending"):
            self.ending = r["ending"]
        if "death" in r:
            self.dead = (r["death"], self.scene_id)
        if "set_gold" in r:
            self.stats["gold"] = r["set_gold"]
        self.change(r.get("stats", {}))
        if "record" in r and r["record"] not in self.records:
            self.records.append(r["record"])
        if r.get("flag"):
            self.flags.add(r["flag"])
        if "give" in r:
            self.cards.add(r["give"])
        if "take" in r:
            self.cards.discard(r["take"])
        if "uses" in r:
            self.uses[r["uses"]] += 1
        if "subscribe" in r:
            self.subs[r["subscribe"]] = 0
            self.cards.add(r["subscribe"])
        if "unsubscribe" in r:
            self.subs.pop(r["unsubscribe"], None)
            self.cards.discard(r["unsubscribe"])
        for sid, every in r.get("sub_every", {}).items():
            self.sub_every[sid] = every
        if r.get("shame"):
            self.shame = True
        if r.get("clear_shame"):
            self.shame = False

    # ---- подписки и долг
    def tick_subs(self):
        for sid in list(self.subs):
            spec = SUBS[sid]
            self.subs[sid] += 1
            paid = self.subs[sid] - self.sub_trial.get(sid, spec["trial"])
            every = self.sub_every.get(sid, spec["every"])
            if paid > 0 and paid % every == 0:
                fee = dict(spec["fee"])
                if "gold" in fee and self.stats["gold"] <= 0:
                    fee = {"body": -1}
                self.change(fee)
                if "payments" in spec and paid // every >= spec["payments"]:
                    self.subs.pop(sid)
                    self.cards.discard(sid)

    def debt(self):
        if self.stats["gold"] < 0:
            self.play_choices(AFTER["microloan"]["choices"])

    # ---- сцены
    def play_scene(self, s):
        self.scene_id = s["id"]
        self.change(s.get("enter", {}).get("stats", {}))
        for t in s.get("text_add", []):
            if cond_ok(t["if"], self):
                self.fired += 1
        if s["kind"] == "auto":
            for i, v in enumerate(s["variants"]):
                if cond_ok(v["if"], self):
                    if v["if"]:
                        self.fired += 1
                    self.apply(v["result"])
                    break
        elif s["kind"] == "compare":
            ticks = sum(cond_ok(t["if"], self) for t in s["ticks"])
            v = "great" if ticks >= 3 else "ok" if ticks >= 1 else "shame"
            if v == "shame" and "good_conduct_note" in self.cards:
                self.cards.discard("good_conduct_note")
                v = "ok"
                self.fired += 1
            self.verdicts.append((s["id"], v))
            spec = RULES["verdicts"][v]
            self.change(spec.get("stats", {}))
            if "give" in spec:
                self.cards.add(spec["give"])
            if not self.check_death():
                self.play_choices(s["choices"])
            self.shame = False
        else:
            self.play_choices(s["choices"])
        self.debt()
        self.tick_subs()
        return not self.check_death()

    def play(self):
        for ch in CHAPTERS:
            if ch["id"] == "ch0" and self.n > 1:
                continue
            queue = None
            for step in ch["flow"]:
                if step == "deck":
                    if queue is None:   # колода тянется один раз, на первом месте "deck"
                        pool = [s for s in ch["scenes"] if s["kind"] == "deck" and cond_ok(s.get("requires"), self)]
                        queue = self.rng.sample(pool, ch["flow"].count("deck"))
                        queue.sort(key=lambda s: not s.get("early"))
                    s = queue.pop(0)
                    if "requires" in s:
                        self.fired += 1
                else:
                    s = SCENES[step]
                    if "requires" in s and not cond_ok(s["requires"], self):
                        continue   # сцена с условием: если оно не выполнено, её в этой жизни нет
                if not self.play_scene(s):
                    return False
            for sid, spec in SUBS.items():
                if spec.get("ends_after_chapter") == ch["id"] and sid in self.subs:
                    self.subs.pop(sid)
                    self.cards.discard(sid)
        return True

    # ---- что уносим в следующую жизнь
    def title(self):
        cnt = Counter(RECORDS[r]["tag"] for r in self.records if "tag" in RECORDS.get(r, {}))
        best = [t for t, n in cnt.most_common() if n >= RULES["titles_need"]]
        return best[0] if best else None

    def carry(self):
        hr = self.rng.choice(AFTER["hr"]["choices"])
        self.taken.append(hr["id"])
        t = self.title()
        return {"next_life": hr["result"]["next_life"], "heir": TAGS[t]["heir"] if t else None,
                "subs": [s for s in self.subs if SUBS[s].get("survives_death")], "prev": self}


def simulate(runs=3000, lives=3, policy="random", seed=7):
    rng = random.Random(seed)
    out = {"survive": Counter(), "n": Counter(), "death": Counter(), "death_ch": Counter(), "verdict": defaultdict(Counter),
           "title": Counter(), "ending": Counter(), "taken": Counter(), "final": defaultdict(list), "fired": [], "patches": Counter(), "great_all": 0}
    for _ in range(runs):
        carry = None
        for n in range(1, lives + 1):
            L = Life(n, carry, rng, policy)
            alive = L.play()
            out["n"][n] += 1
            out["survive"][n] += alive
            if not alive:
                out["death"][L.dead[0]] += 1
                out["death_ch"][SCENE_CH.get(L.dead[1], "?")] += 1
            else:
                out["ending"][L.ending or "—"] += 1
                for st, v in L.stats.items():
                    out["final"][st].append(v)
            for sid, v in L.verdicts:
                out["verdict"][sid][v] += 1
            out["title"][L.title() or "—"] += 1
            out["taken"].update(L.taken)
            out["fired"].append(L.fired)
            out["patches"].update(L.patch_notes)
            carry = L.carry()
            out["taken"].update(L.taken[-1:])
    return out


# ---------------------------------------------------------------- текст для людей
def cond_text(cond):
    if not cond:
        return ""
    parts = []
    rec = lambda r: "«" + RECORDS[r]["text"].rstrip(".") + "»"
    if "card" in cond:
        parts.append(f"есть карточка «{CARDS[cond['card']]['name']}»")
    if "sub" in cond:
        parts.append(f"действует подписка «{CARDS[cond['sub']]['name']}»")
    if "record" in cond:
        parts.append(f"в деле записано: {rec(cond['record'])}")
    if "record_any" in cond:
        parts.append("в деле есть одна из записей: " + "; ".join(rec(r) for r in cond["record_any"]))
    if "no_record" in cond:
        parts.append(f"в деле нет записи {rec(cond['no_record'])}")
    if "no_record_any" in cond:
        parts.append("в деле нет записей: " + "; ".join(rec(r) for r in cond["no_record_any"]))
    if "flag" in cond or "flag_any" in cond:
        names = {"spoke_word": "сказал настоящее слово", "diploma": "есть диплом", "fame": "есть слава", "job": "есть работа", "arena_win": "победил на турнире", "cafe": "открыл кофейню"}
        fl = ([cond["flag"]] if "flag" in cond else []) + cond.get("flag_any", [])
        parts.append(" или ".join(names.get(f, f) for f in fl))
    if "record_min" in cond:
        parts.append(f"в деле есть хотя бы {cond['record_min']['n']} из записей: " + "; ".join(rec(r) for r in cond["record_min"]["of"]))
    if "no_flag" in cond:
        parts.append({"job": "нет работы"}.get(cond["no_flag"], "нет отметки " + cond["no_flag"]))
    for st, v in cond.get("stat_min", {}).items():
        parts.append(f"{STAT_NAMES[st]} {v} или больше")
    if "life_min" in cond:
        parts.append("не первая жизнь" if cond["life_min"] == 2 else f"жизнь {cond['life_min']} или позже")
    if cond.get("no_shame"):
        parts.append("в этой главе не было позора")
    return ", ".join(parts)


def effects_text(r, cost=None):
    parts = []
    if cost:
        parts.append(f"Золото −{cost}")
    for st in ("body", "mind", "gold", "rep"):
        d = r.get("stats", {}).get(st)
        if d:
            parts.append(f"{STAT_NAMES[st]} {'+' if d > 0 else '−'}{abs(d)}")
    if "set_gold" in r:
        parts.append("Золото становится 0")
    if "death" in r:
        parts.append("конец жизни: «" + AFTER["deaths"][r["death"]]["title"] + "»")
    if "give" in r:
        parts.append(f"получена карточка «{CARDS[r['give']]['name']}» ({TERM_NAMES[CARDS[r['give']]['term']]})")
    if "take" in r:
        parts.append(f"карточка «{CARDS[r['take']]['name']}» уходит")
    if "subscribe" in r and r.get("give") != r["subscribe"]:
        parts.append(f"оформлена подписка «{CARDS[r['subscribe']]['name']}»")
    if "unsubscribe" in r:
        parts.append(f"подписка «{CARDS[r['unsubscribe']]['name']}» прекращена")
    if "sub_every" in r:
        parts.append("подписка списывает реже")
    if r.get("flag") == "diploma":
        parts.append("получен диплом")
    if r.get("flag") == "fame":
        parts.append("получена слава")
    if r.get("shame"):
        parts.append("позор для семьи")
    if r.get("clear_shame"):
        parts.append("позор этой главы снят")
    if "next_life" in r:
        parts += [f"в следующей жизни {STAT_NAMES[s]} +{v}" for s, v in r["next_life"].items()]
    if "record" in r:
        rec = RECORDS[r["record"]]
        tag = f" · род: {TAGS[rec['tag']]['title'].lower()}" if "tag" in rec else ""
        parts.append(f"в личное дело: «{rec['text']}»{tag}")
    return parts


def render(sim_r, sim_c, errors, warns):
    """Возвращает (markdown, html)."""
    md, h = [], []
    n_scenes = len(SCENES)
    n_choices = sum(1 for _ in all_choices())
    n_results = sum(1 for _ in all_results())
    arts = sorted({c["art"] for _, c in all_choices()} | {c["art"] for c in CARDS.values()})
    gestures = [a for a in arts if a.startswith("g_")]
    objects = [a for a in arts if a.startswith("o_")]
    bgs = sorted({s["bg"] for s in SCENES.values()} | {AFTER["hr"]["bg"]})
    callbacks = sum(1 for _ in conds())
    pct = lambda a, b: f"{100 * a / b:.0f}%" if b else "—"
    sr, sc = sim_r, sim_c

    def both(m, x=None):
        md.append(m)
        h.append(x if x is not None else f"<p>{html.escape(m)}</p>")

    E = html.escape
    md += ["# Книга сцен — первая часть: от рождения до ворот столицы", "",
           "> Собрано скриптом `story/tools/build.py` из файлов `story/*.json`. Править текст нужно в тех файлах, не здесь.", ""]
    md += ["## Коротко", "",
           f"- Сцен: **{n_scenes}**, выборов: **{n_choices}**, исходов: **{n_results}**.",
           f"- Уникальных карточек: **{len(CARDS)}**, строк личного дела: **{len(RECORDS)}**.",
           f"- Мест, где прошлое возвращается (условия по записям, карточкам и прошлым жизням): **{callbacks}**.",
           f"- Картинок для карточек выбора: **{len(arts)}** — {len(objects)} предметов и {len(gestures)} жестов, которые повторяются.",
           f"- Фонов: **{len(bgs)}**, из них новый один — `bg_home_day` (изба).",
           "", "### Проверка на случайных жизнях", "",
           f"Скрипт прожил {sum(sr['n'].values())} жизней наугад и {sum(sc['n'].values())} осторожно.", "",
           "| | Наугад | Осторожно |", "|---|---|---|",
           f"| Доживает до пещеры дракона в первой жизни | {pct(sr['survive'][1], sr['n'][1])} | {pct(sc['survive'][1], sc['n'][1])} |",
           f"| Доживает до пещеры дракона в третьей жизни | {pct(sr['survive'][3], sr['n'][3])} | {pct(sc['survive'][3], sc['n'][3])} |",
           f"| Прошлое аукнулось за жизнь, в среднем раз | {sum(sr['fired']) / len(sr['fired']):.1f} | {sum(sc['fired']) / len(sc['fired']):.1f} |",
           ""]
    tot_d = sum(sr["death"].values())
    md += ["От чего умирают, если играть наугад: " + ", ".join(
        f"{AFTER['deaths'][k]['title'].lower()} — {pct(v, tot_d)}" for k, v in sr["death"].most_common()) + ".", ""]
    ch_title = {ch["id"]: ch["title"] for ch in CHAPTERS}
    md += ["В какой главе: " + ", ".join(f"«{ch_title[k]}» — {pct(v, tot_d)}" for k, v in sorted(sr["death_ch"].items())) + ".", ""]
    md += ["Что говорит мама (наугад / осторожно):", "", "| Глава | Молодец | Ну, сойдёт | Позор семьи |", "|---|---|---|---|"]
    for ch in CHAPTERS:
        for s in ch["scenes"]:
            if s["kind"] == "compare":
                a, b = sr["verdict"][s["id"]], sc["verdict"][s["id"]]
                ta, tb = sum(a.values()), sum(b.values())
                md.append(f"| {ch['title']} | {pct(a['great'], ta)} / {pct(b['great'], tb)} | {pct(a['ok'], ta)} / {pct(b['ok'], tb)} | {pct(a['shame'], ta)} / {pct(b['shame'], tb)} |")
    tt = sum(sr["title"].values())
    md += ["", "Титулы к концу жизни (наугад): " + ", ".join(
        f"{TAGS[k]['title'] if k in TAGS else 'без титула'} — {pct(v, tt)}" for k, v in sr["title"].most_common()) + ".", ""]
    never = [c["id"] for _, c in all_choices() if "result" in c and sr["taken"][c["id"]] + sc["taken"][c["id"]] == 0]
    md += [("Выборы, которые не выпали ни разу: " + ", ".join(never) + ".") if never else "Каждый выбор выпал хотя бы раз.", ""]
    if errors:
        md += ["### Ошибки", ""] + [f"- {e}" for e in errors] + [""]
    if warns:
        md += ["### Замечания", ""] + [f"- {w}" for w in warns] + [""]

    # ---- главы
    def choice_md(c, L, depth):
        ind = "  " * depth
        tags = []
        if "requires" in c:
            tags.append(("помощник: " if c.get("helper") else "скрытый: ") + cond_text(c["requires"]))
        cost = c.get("cost")
        if cost:
            tags.append(f"цена {cost['gold']}" + "".join(f"; {a['gold']}, если {cond_text(a['if'])}" for a in cost.get("alt", [])))
        tag = f" *({'; '.join(tags)})*" if tags else ""
        md.append(f"{ind}- **{c['label']}**{tag}")
        cls = " hidden" if "requires" in c else ""
        h.append(f'<div class="choice{cls}"><div class="lab">{E(c["label"])}' + (f'<span class="req">{E("; ".join(tags))}</span>' if tags else "") + "</div>")
        if "disabled_if" in c:
            d = c["disabled_if"]
            md.append(f"{ind}  - Закрыт, если {cond_text(d['if'])}: {d['text']}")
            h.append(f'<p class="closed">Закрыт, если {E(cond_text(d["if"]))}: {E(d["text"])}</p>')
        if "then" in c:
            md.append(f"{ind}  - {c['then']['text']}")
            h.append(f'<p class="then">{E(c["then"]["text"])}</p><div class="nest">')
            for x in c["then"]["choices"]:
                choice_md(x, L, depth + 2)
            h.append("</div>")
        else:
            r = c["result"]
            if r.get("back"):
                md.append(f"{ind}  - {r['text']} *(возврат к выбору)*")
                h.append(f'<p class="res">{E(r["text"])} <i>(возврат к выбору)</i></p>')
            else:
                ef = effects_text(r)
                md.append(f"{ind}  - {r['text']}")
                h.append(f'<p class="res">{E(r["text"])}</p>')
                if ef:
                    md.append(f"{ind}  - *{' · '.join(ef)}*")
                    h.append('<p class="ef">' + " · ".join(E(x) for x in ef) + "</p>")
        h.append("</div>")

    def scene_md(s):
        kind = KIND_NAMES[s["kind"]]
        req = f" Выпадает, если {cond_text(s['requires'])}." if "requires" in s else ""
        md.extend([f"### {s['title']}", "", f"*Сцена {kind}. Говорит: {SPEAKERS.get(s.get('speaker'), '—')}. Фон: `{s['bg']}`.{req}*", ""])
        h.append(f'<section class="scene k-{s["kind"]}"><h3>{E(s["title"])}</h3><p class="meta">{E(kind)} · говорит {E(SPEAKERS.get(s.get("speaker"), "—"))} · фон {E(s["bg"])}{E(req)}</p>')
        if "enter" in s:
            ef = " · ".join(effects_text(s["enter"]))
            md.extend([f"*В начале сцены: {ef}.*", ""])
            h.append(f'<p class="ef">В начале сцены: {E(ef)}</p>')
        md.extend([s["text"], ""])
        h.append(f'<p class="txt">{E(s["text"])}</p>')
        for t in s.get("text_add", []):
            md.extend([f"> Если {cond_text(t['if'])}: {t['text']}", ""])
            h.append(f'<p class="add"><b>Если {E(cond_text(t["if"]))}:</b> {E(t["text"])}</p>')
        if s["kind"] == "auto":
            for v in s["variants"]:
                head = f"Если {cond_text(v['if'])}" if v["if"] else "Иначе"
                ef = " · ".join(effects_text(v["result"]))
                md.extend([f"- **{head}.** {v['result']['text']}", f"  - *{ef}*"])
                h.append(f'<div class="choice"><div class="lab">{E(head)}</div><p class="res">{E(v["result"]["text"])}</p><p class="ef">{E(ef)}</p></div>')
            md.append("")
        if s["kind"] == "compare":
            md.extend(["**Три галочки мамы:**", ""] + [f"{i}. {t['label']}" for i, t in enumerate(s["ticks"], 1)] + [""])
            h.append('<div class="ticks"><b>Три галочки мамы</b><ol>' + "".join(f"<li>{E(t['label'])}</li>" for t in s["ticks"]) + "</ol></div>")
            for key in ("great", "ok", "shame"):
                v = RULES["verdicts"][key]
                ef = " · ".join(effects_text(v))
                md.append(f"- **{v['name']}.** {s['verdict_text'][key]}" + (f" *{ef}*" if ef else ""))
                h.append(f'<div class="choice v-{key}"><div class="lab">{E(v["name"])}</div><p class="res">{E(s["verdict_text"][key])}</p>' + (f'<p class="ef">{E(ef)}</p>' if ef else "") + "</div>")
            md.append("")
            if "text_after" in s:
                md.extend([s["text_after"], ""])
                h.append(f'<p class="txt">{E(s["text_after"])}</p>')
            md.extend(["**Как ответить:**", ""])
            h.append('<p class="meta">Как ответить</p>')
        for c in s.get("choices", []):
            choice_md(c, None, 0)
        md.append("")
        h.append("</section>")

    for ch in CHAPTERS:
        goal = f" Цель: **{ch['goal']}**." if ch.get("goal") else ""
        flow = " → ".join("сцена из колоды" if x == "deck" else f"«{SCENES[x]['title']}»" for x in ch["flow"])
        md.extend([f"## Глава {ch['id'][2:]}. {ch['title']}", "", f"Возраст: {ch['age']}.{goal}", "", f"Порядок: {flow}.", ""])
        h.append(f'<h2 id="{ch["id"]}">Глава {ch["id"][2:]}. {E(ch["title"])}</h2><p class="lead">Возраст: {E(ch["age"])}.' + (f' Цель на экране: <b>{E(ch["goal"])}</b>.' if ch.get("goal") else "") + f'<br>Порядок: {E(flow)}.</p>')
        order = [x for x in ch["flow"] if x != "deck"]
        deck = [s for s in ch["scenes"] if s["kind"] == "deck"]
        first_deck = ch["flow"].index("deck") if "deck" in ch["flow"] else None
        done_deck = False
        for step in ch["flow"]:
            if step == "deck":
                if not done_deck:
                    md.extend([f"*Колода главы: {len(deck)} сцен, в жизни выпадают две.*", ""])
                    h.append(f'<p class="deckhead">Колода главы: {len(deck)} сцен, в жизни выпадают две</p>')
                    for s in deck:
                        scene_md(s)
                    done_deck = True
            else:
                scene_md(SCENES[step])

    # ---- вне глав
    md.extend(["## После смерти и между жизнями", ""])
    h.append('<h2 id="after">После смерти и между жизнями</h2>')
    ev = dict(AFTER["microloan"]); ev["title"] = "Долг: " + ev["title"]
    scene_md(ev)
    ev = dict(AFTER["promotion"]); ev["title"] = "Репутация дошла до 10: " + ev["title"]
    scene_md(ev)
    md.extend(["### Концовки", "", "Жизнь, в которой герой дошёл до пещеры, кончается одной из концовок. Потом всё равно Небесная HR и новая жизнь.", ""])
    h.append('<section class="scene"><h3>Концовки</h3>')
    for e in AFTER.get("endings", {}).values():
        if isinstance(e, dict):
            md.append(f"- **{e['title']}.** {e['text']}")
            h.append(f'<div class="choice"><div class="lab">{E(e["title"])}</div><p class="res">{E(e["text"])}</p></div>')
    md.append("")
    h.append("</section>")
    md.extend(["### Смерти", ""])
    h.append('<section class="scene"><h3>Смерти</h3>')
    for d in AFTER["deaths"].values():
        md.append(f"- **{d['title']}.** {d['text']}")
        h.append(f'<div class="choice"><div class="lab">{E(d["title"])}</div><p class="res">{E(d["text"])}</p>')
        for card, hp in d.get("helpers", {}).items():
            back = ", ".join(f"{STAT_NAMES[k]} становится {v}" for k, v in hp["revive"].items())
            md.append(f"  - *Если в руке «{CARDS[card]['name']}»:* {hp['text']} *({back}, карточка уходит)*")
            h.append(f'<p class="add"><b>Если в руке «{E(CARDS[card]["name"])}»:</b> {E(hp["text"])} <i>({E(back)}, карточка уходит)</i></p>')
        h.append("</div>")
    md.append("")
    h.append("</section>")
    hr = dict(AFTER["hr"])
    hr["text"] = hr["text"] + " " + hr["text_after_file"].replace("{great}", "…").replace("{chapters}", "…")
    scene_md(hr)
    md.extend(["### Титулы и наследство", "", "Четыре записи одного рода за жизнь дают титул. К титулу полагается карточка, с которой начнётся следующая жизнь.", "",
               "| Род записей | Титул | Наследство |", "|---|---|---|"])
    h.append('<section class="scene"><h3>Титулы и наследство</h3><p class="txt">Четыре записи одного рода за жизнь дают титул. К титулу полагается карточка, с которой начнётся следующая жизнь.</p><table><tr><th>Титул</th><th>Наследство</th></tr>')
    for t, v in TAGS.items():
        md.append(f"| {t} | {v['title']} | {AFTER['heirs'][v['heir']]} |")
        h.append(f"<tr><td>{E(v['title'])}</td><td>{E(AFTER['heirs'][v['heir']])}</td></tr>")
    md.extend(["", "### Список исправлений", "", "Перед новой жизнью показываем до трёх строк.", "", "| Когда | Строка в списке |", "|---|---|"])
    h.append('</table></section><section class="scene"><h3>Список исправлений</h3><p class="txt">Перед новой жизнью показываем до трёх строк: две по прошлой жизни и всегда строку про свинью.</p><table><tr><th>Когда</th><th>Строка</th></tr>')
    for p in AFTER["patches"]["list"]:
        w = p["when"]
        when = ("всегда" if w.get("always") else
                f"в прошлой жизни: «{RECORDS[w['record']]['text'].rstrip('.')}»" if "record" in w else
                f"в прошлой жизни {w['uses_min']['n']} раза сработала «{CARDS[w['uses_min']['card']]['name']}»" if "uses_min" in w else
                "в прошлой жизни давал взятки дважды" if "records_min" in w else
                f"прошлая жизнь кончилась концовкой «{AFTER['endings'][w['ending']]['title']}»" if "ending" in w else
                f"в прошлой жизни умер в сцене «{SCENES[w['died_in']]['title']}»")
        md.append(f"| {when} | {p['note']} |")
        h.append(f"<tr><td>{E(when)}</td><td>{E(p['note'])}</td></tr>")
    md.extend(["", "## Уникальные карточки", "", "| Карточка | Срок | Что это |", "|---|---|---|"])
    h.append('</table></section><h2 id="cards">Уникальные карточки</h2><table><tr><th>Карточка</th><th>Срок</th><th>Что это</th></tr>')
    for c in CARDS.values():
        md.append(f"| {c['name']} | {TERM_NAMES[c['term']]} | {c['text']} |")
        h.append(f"<tr><td>{E(c['name'])}</td><td>{E(TERM_NAMES[c['term']])}</td><td>{E(c['text'])}</td></tr>")
    md.extend(["", "## Картинки, которые нужны для первой части", "",
               f"**Предметы ({len(objects)}):** " + ", ".join(f"`{a}`" for a in objects), "",
               f"**Жесты ({len(gestures)}):** " + ", ".join(f"`{a}`" for a in gestures), "",
               f"**Фоны ({len(bgs)}):** " + ", ".join(f"`{a}`" for a in bgs), ""])
    h.append("</table>")
    return "\n".join(md) + "\n", "\n".join(h), md


PAGE = r'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Сэр Баг — книга сцен</title><style>
:root{--bg:#f4efe4;--card:#fffdf7;--ink:#2a2118;--mute:#6f6253;--line:#d9cdb8;--acc:#9a3b1e;--take:#2f6b3a;--takebg:#e6f0e2;--skip:#8a3324;--skipbg:#f5e3dc;--hid:#e9eef5;--hidb:#5a7aa5}
@media (prefers-color-scheme:dark){:root{--bg:#1b1713;--card:#25201a;--ink:#efe6d6;--mute:#a99c88;--line:#3a3229;--acc:#e08a5c;--take:#9bd0a2;--takebg:#1f2e22;--skip:#e9a493;--skipbg:#33201b;--hid:#1c2531;--hidb:#7fa3d6}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:28px 16px 90px}
h1{font:700 29px/1.15 Georgia,serif;margin:0 0 6px}h2{font:700 24px/1.2 Georgia,serif;margin:50px 0 6px;padding-top:14px;border-top:2px solid var(--ink)}
h3{font:700 19px/1.25 Georgia,serif;margin:0 0 2px}p{margin:0 0 8px}.lead{color:var(--mute);margin:0 0 16px}
nav{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 0;margin:12px 0 0;display:flex;gap:6px 14px;flex-wrap:wrap;font-size:14px}nav a{color:var(--acc);text-decoration:none;white-space:nowrap}
.scene{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:0 0 14px}
.scene.k-deck{border-style:dashed}.scene.k-compare{border:2px solid var(--acc)}
.meta{color:var(--mute);font-size:13px;margin:0 0 8px}.txt{font:17px/1.5 Georgia,serif}.add{background:var(--hid);border-left:3px solid var(--hidb);padding:6px 10px;border-radius:0 6px 6px 0;font-size:15px}
.choice{border-top:1px solid var(--line);padding:8px 0 2px}.choice.hidden>.lab{color:var(--hidb)}
.lab{font-weight:650}.req{font-weight:400;font-size:13px;color:var(--mute);margin-left:8px}
.then{color:var(--mute);font-style:italic;margin:4px 0}.nest{margin-left:18px;border-left:2px solid var(--line);padding-left:12px}
.res{margin:3px 0}.ef{font-size:13.5px;color:var(--mute);margin:0 0 6px}.closed{font-size:14px;color:var(--skip)}
.ticks{background:var(--takebg);border-radius:8px;padding:8px 12px;margin:8px 0}.ticks ol{margin:4px 0 0;padding-left:20px}
.v-great>.lab{color:var(--take)}.v-shame>.lab{color:var(--skip)}.deckhead{font-weight:650;color:var(--mute);margin:18px 0 8px}
table{border-collapse:collapse;width:100%;font-size:15px;margin:8px 0}th,td{text-align:left;vertical-align:top;padding:6px 9px;border-bottom:1px solid var(--line)}th{color:var(--mute);font-size:13px}
.sum{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:14px 0}.sum div{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}.sum b{display:block;font:700 22px Georgia,serif}.sum span{color:var(--mute);font-size:14px}
</style></head><body><div class="wrap"><h1>Сэр Баг — книга сцен</h1>
<p class="lead">Главы 0–6: от рождения до пещеры дракона. Синим отмечены скрытые выборы — они появляются, если у тебя есть нужная карточка или запись в личном деле. Пунктирная рамка — сцена из колоды: в каждой жизни выпадают две из пяти и больше.</p>
<div class="sum">{{SUM}}</div><nav>{{NAV}}</nav>{{BODY}}</div></body></html>'''


def main():
    errors, warns = validate()
    for e in errors:
        print("ОШИБКА:", e)
    for w in warns:
        print("замечание:", w)
    if errors:
        sys.exit(1)
    sr = simulate(policy="random")
    sc = simulate(policy="careful")
    md, body, _ = render(sr, sc, errors, warns)
    with open(os.path.join(STORY, "BOOK.md"), "w", encoding="utf-8") as f:
        f.write(md)
    pct = lambda a, b: f"{100 * a / b:.0f}%"
    arts = {c["art"] for _, c in all_choices()} | {c["art"] for c in CARDS.values()}
    cards = [(str(len(SCENES)), "сцен"), (str(sum(1 for _ in all_choices())), "выборов"),
             (str(sum(1 for _ in conds())), "мест, где возвращается прошлое"), (str(len(CARDS)), "уникальных карточек"),
             (str(len(arts)), "картинок для карточек"),
             (pct(sr["survive"][1], sr["n"][1]) + " / " + pct(sc["survive"][1], sc["n"][1]), "доживают до пещеры дракона: наугад / осторожно")]
    nav = "".join(f'<a href="#{ch["id"]}">{ch["id"][2:]}. {html.escape(ch["title"])}</a>' for ch in CHAPTERS) + '<a href="#after">После смерти</a><a href="#cards">Карточки</a>'
    page = PAGE.replace("{{SUM}}", "".join(f"<div><b>{a}</b><span>{html.escape(b)}</span></div>" for a, b in cards)).replace("{{NAV}}", nav).replace("{{BODY}}", body)
    out = os.path.join(ROOT, "refs", "kniga.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"готово: story/BOOK.md, refs/kniga.html · сцен {len(SCENES)}, выборов {cards[1][0]}")
    print(f"до пещеры дракона в первой жизни: наугад {cards[5][0]}")
    print("концовки наугад:", dict(sr["ending"].most_common()), "| осторожно:", dict(sc["ending"].most_common()))
    tot = sum(sr["death"].values())
    print("смерти наугад:", {k: f"{100 * v / tot:.0f}%" for k, v in sr["death"].most_common()})
    print("смерти по главам:", dict(sorted(sr["death_ch"].items())))
    for sid, v in sr["verdict"].items():
        t = sum(v.values())
        print(" ", sid, {k: f"{100 * x / t:.0f}%" for k, x in v.items()}, "| осторожно:", {k: f"{100 * x / sum(sc['verdict'][sid].values()):.0f}%" for k, x in sc["verdict"][sid].items()})
    print("титулы:", {k: f"{100 * v / sum(sr['title'].values()):.0f}%" for k, v in sr["title"].most_common()})
    for st, vals in sr["final"].items():
        print(f"  в конце {st}: в среднем {sum(vals) / len(vals):.1f}")
    never = [c["id"] for _, c in all_choices() if "result" in c and sr["taken"][c["id"]] + sc["taken"][c["id"]] == 0]
    print("не выпали ни разу:", never)


if __name__ == "__main__":
    main()
